"""Provenance-bearing calibration from matched handwritten route attempts."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional

from sympy import Matrix, Rational

from .cost import AdmissionBoundary, COST_AXES, construct_admission_boundary


@dataclass(frozen=True)
class PairedRouteObservation:
    """One matched direct/proposed attempt on the same problem or variant."""

    sample_id: str
    problem_id: str
    boundary: AdmissionBoundary
    direct_seconds: Fraction
    proposed_seconds: Fraction
    direct_correct: bool
    proposed_correct: bool
    provenance: str
    order_control: str
    participant_id: str = "unspecified"
    session_id: str = "unspecified"

    def __post_init__(self) -> None:
        for label, value in (
            ("sample_id", self.sample_id),
            ("problem_id", self.problem_id),
            ("provenance", self.provenance),
            ("order_control", self.order_control),
            ("participant_id", self.participant_id),
            ("session_id", self.session_id),
        ):
            if not value.strip():
                raise ValueError(f"{label} must be nonempty.")
        if self.problem_id != self.boundary.baseline.problem_id:
            raise ValueError("Observation problem_id must match its route boundary.")
        expected = construct_admission_boundary(
            self.boundary.baseline,
            self.boundary.proposed,
        )
        if self.boundary != expected:
            raise ValueError("Observation boundary must be derived from its routes.")
        direct_seconds = Fraction(self.direct_seconds)
        proposed_seconds = Fraction(self.proposed_seconds)
        if direct_seconds <= 0 or proposed_seconds <= 0:
            raise ValueError("Observed route times must be strictly positive.")
        object.__setattr__(self, "direct_seconds", direct_seconds)
        object.__setattr__(self, "proposed_seconds", proposed_seconds)
        if not isinstance(self.direct_correct, bool) or not isinstance(
            self.proposed_correct, bool
        ):
            raise ValueError("Route correctness fields must be Boolean.")

    @property
    def time_delta(self) -> Fraction:
        return self.proposed_seconds - self.direct_seconds

    @property
    def both_correct(self) -> bool:
        return self.direct_correct and self.proposed_correct

    @property
    def execution_substrate(self) -> str:
        return self.boundary.baseline.execution_substrate


@dataclass(frozen=True)
class CalibrationObstruction:
    kind: str
    message: str
    unidentified_axes: tuple[str, ...] = ()


@dataclass(frozen=True)
class CalibratedCostProfile:
    name: str
    axis_weights: dict[str, Fraction]
    identified_axes: tuple[str, ...]
    provenance: str
    participant_id: str
    execution_substrate: str
    training_sample_ids: tuple[str, ...]
    training_problem_ids: tuple[str, ...]
    residual_sum_squares: Fraction


@dataclass(frozen=True)
class CalibrationResult:
    status: str
    profile: Optional[CalibratedCostProfile]
    obstruction: Optional[CalibrationObstruction]
    used_sample_ids: tuple[str, ...]
    excluded_sample_ids: tuple[str, ...]


@dataclass(frozen=True)
class HeldOutRouteEvaluation:
    status: str
    reason: str
    predicted_route: Optional[str]
    observed_best_route: Optional[str]
    predicted_time_delta: Optional[Fraction]
    unidentified_axes: tuple[str, ...] = ()


def _refusal(
    kind: str,
    message: str,
    used: tuple[str, ...],
    excluded: tuple[str, ...],
    unidentified_axes: tuple[str, ...] = (),
) -> CalibrationResult:
    return CalibrationResult(
        status="refused",
        profile=None,
        obstruction=CalibrationObstruction(kind, message, unidentified_axes),
        used_sample_ids=used,
        excluded_sample_ids=excluded,
    )


def _to_sympy(value: Fraction) -> Rational:
    return Rational(value.numerator, value.denominator)


def _to_fraction(value: Rational) -> Fraction:
    return Fraction(int(value.p), int(value.q))


def calibrate_paired_route_costs(
    profile_name: str,
    observations: tuple[PairedRouteObservation, ...],
) -> CalibrationResult:
    """Fit positive seconds-per-unit weights from correct paired differences.

    The paired model is ``t_proposed-t_direct = delta_cost dot weight``. Problem
    difficulty common to both routes cancels. Only axes spanned independently by
    the correct training pairs are returned.
    """

    if not profile_name.strip():
        raise ValueError("A calibrated profile requires a nonempty name.")
    sample_ids = tuple(item.sample_id for item in observations)
    if len(sample_ids) != len(set(sample_ids)):
        raise ValueError("Calibration sample ids must be unique.")
    substrates = {item.execution_substrate for item in observations}
    if len(substrates) > 1:
        raise ValueError("Calibration observations must use one execution substrate.")
    participants = {item.participant_id for item in observations}
    if len(participants) > 1:
        raise ValueError("A personal calibration profile requires one participant.")

    eligible = tuple(item for item in observations if item.both_correct)
    excluded = tuple(item.sample_id for item in observations if not item.both_correct)
    used = tuple(item.sample_id for item in eligible)
    if not eligible:
        return _refusal(
            "no_correct_pairs",
            "Calibration requires at least one pair in which both routes are correct.",
            used,
            excluded,
        )

    active_indices = tuple(
        index
        for index in range(len(COST_AXES))
        if any(item.boundary.delta[index] != 0 for item in eligible)
    )
    active_axes = tuple(COST_AXES[index] for index in active_indices)
    if not active_indices:
        return _refusal(
            "no_cost_variation",
            "Correct route pairs do not differ on any cost axis.",
            used,
            excluded,
        )

    design = Matrix(
        [[item.boundary.delta[index] for index in active_indices] for item in eligible]
    )
    if design.rank() < len(active_indices):
        return _refusal(
            "insufficient_rank",
            "Paired differences do not independently identify every varying axis.",
            used,
            excluded,
            active_axes,
        )

    observed = Matrix([_to_sympy(item.time_delta) for item in eligible])
    normal = design.T * design
    fitted = normal.inv() * design.T * observed
    weights = tuple(_to_fraction(value) for value in fitted)
    if any(weight <= 0 for weight in weights):
        return _refusal(
            "nonpositive_fit",
            "The unconstrained paired fit contradicts strictly positive axis costs.",
            used,
            excluded,
            tuple(axis for axis, weight in zip(active_axes, weights) if weight <= 0),
        )

    residual = observed - design * fitted
    residual_sum_squares = _to_fraction((residual.T * residual)[0])
    provenance = " | ".join(dict.fromkeys(item.provenance for item in eligible))
    profile = CalibratedCostProfile(
        name=profile_name,
        axis_weights=dict(zip(active_axes, weights)),
        identified_axes=active_axes,
        provenance=(
            "Paired correct-route least squares; "
            f"order controls: {' | '.join(dict.fromkeys(item.order_control for item in eligible))}; "
            f"sources: {provenance}"
        ),
        participant_id=eligible[0].participant_id,
        execution_substrate=eligible[0].execution_substrate,
        training_sample_ids=used,
        training_problem_ids=tuple(dict.fromkeys(item.problem_id for item in eligible)),
        residual_sum_squares=residual_sum_squares,
    )
    return CalibrationResult(
        status="calibrated",
        profile=profile,
        obstruction=None,
        used_sample_ids=used,
        excluded_sample_ids=excluded,
    )


def evaluate_held_out_route(
    profile: CalibratedCostProfile,
    observation: PairedRouteObservation,
) -> HeldOutRouteEvaluation:
    """Compare a profile prediction with one genuinely held-out observation."""

    if observation.problem_id in profile.training_problem_ids:
        return HeldOutRouteEvaluation(
            "refused",
            "training_problem_leakage",
            None,
            None,
            None,
        )
    if observation.participant_id != profile.participant_id:
        return HeldOutRouteEvaluation(
            "refused",
            "participant_mismatch",
            None,
            None,
            None,
        )
    if observation.execution_substrate != profile.execution_substrate:
        return HeldOutRouteEvaluation(
            "refused",
            "execution_substrate_mismatch",
            None,
            None,
            None,
        )

    required_axes = tuple(
        axis
        for axis, coefficient in zip(COST_AXES, observation.boundary.delta)
        if coefficient != 0
    )
    unidentified = tuple(
        axis for axis in required_axes if axis not in profile.axis_weights
    )
    if unidentified:
        return HeldOutRouteEvaluation(
            "refused",
            "unidentified_prediction_axis",
            None,
            None,
            None,
            unidentified,
        )

    predicted_delta = sum(
        (
            profile.axis_weights[axis] * coefficient
            for axis, coefficient in zip(COST_AXES, observation.boundary.delta)
            if coefficient != 0
        ),
        Fraction(0),
    )
    if predicted_delta > 0:
        predicted = "direct"
    elif predicted_delta < 0:
        predicted = "proposed"
    else:
        predicted = "tie"

    if observation.direct_correct and not observation.proposed_correct:
        observed_best = "direct"
    elif observation.proposed_correct and not observation.direct_correct:
        observed_best = "proposed"
    elif not observation.direct_correct and not observation.proposed_correct:
        return HeldOutRouteEvaluation(
            "refused",
            "no_correct_route",
            predicted,
            None,
            predicted_delta,
        )
    elif observation.time_delta > 0:
        observed_best = "direct"
    elif observation.time_delta < 0:
        observed_best = "proposed"
    else:
        observed_best = "tie"

    if predicted == "tie" or observed_best == "tie":
        status = "indeterminate"
        reason = "predicted_or_observed_tie"
    elif predicted == observed_best:
        status = "matched"
        reason = "predicted_cheaper_correct_route"
    else:
        status = "missed"
        reason = "prediction_disagrees_with_cheaper_correct_route"
    return HeldOutRouteEvaluation(
        status,
        reason,
        predicted,
        observed_best,
        predicted_delta,
    )

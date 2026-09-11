"""Auditable Pareto comparison of complete handwritten exam routes."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional


ACTION_KINDS = frozenset({"relation", "symbolic", "branch", "representation", "return"})
EXECUTION_SUBSTRATES = frozenset({"handwritten", "tool_assisted"})
COST_AXES = (
    "relations_selected",
    "hidden_quantities",
    "peak_live_relations",
    "symbolic_actions",
    "branch_checks",
    "representation_changes",
    "return_checks",
)


@dataclass(frozen=True)
class ExamAction:
    kind: str
    description: str
    live_relations: int = 0
    symbolic_subjects: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.kind not in ACTION_KINDS:
            raise ValueError(
                f"Unknown exam action kind {self.kind!r}; expected one of "
                f"{sorted(ACTION_KINDS)}."
            )
        if not self.description.strip():
            raise ValueError("An exam action requires a description.")
        if (
            not isinstance(self.live_relations, int)
            or isinstance(self.live_relations, bool)
            or self.live_relations < 0
        ):
            raise ValueError("live_relations must be a nonnegative integer.")
        if self.kind == "symbolic":
            if not self.symbolic_subjects:
                raise ValueError(
                    "A symbolic action requires symbolic_subjects so bundled "
                    "handwritten work cannot be counted as one unit."
                )
            if any(not subject.strip() for subject in self.symbolic_subjects):
                raise ValueError("symbolic_subjects must be nonempty names.")
            if len(self.symbolic_subjects) != len(set(self.symbolic_subjects)):
                raise ValueError("A symbolic subject is listed more than once.")
        elif self.symbolic_subjects:
            raise ValueError("Only symbolic actions may declare symbolic_subjects.")

    @property
    def atomic_units(self) -> int:
        """Return one unit per explicit action or per symbolic result subject."""

        return len(self.symbolic_subjects) if self.kind == "symbolic" else 1


@dataclass(frozen=True)
class RouteCost:
    relations_selected: int
    hidden_quantities: int
    peak_live_relations: int
    symbolic_actions: int
    branch_checks: int
    representation_changes: int
    return_checks: int

    def as_tuple(self) -> tuple[int, ...]:
        return tuple(getattr(self, axis) for axis in COST_AXES)


@dataclass(frozen=True)
class HandwrittenRoute:
    problem_id: str
    target: str
    hidden_quantities: tuple[str, ...]
    actions: tuple[ExamAction, ...]
    execution_substrate: str = "handwritten"

    def __post_init__(self) -> None:
        if not self.problem_id.strip() or not self.target.strip():
            raise ValueError("A handwritten route requires a problem id and target.")
        if not self.actions:
            raise ValueError("A handwritten route requires at least one action.")
        if any(not name.strip() for name in self.hidden_quantities):
            raise ValueError("Hidden-quantity names must be nonempty.")
        if len(self.hidden_quantities) != len(set(self.hidden_quantities)):
            raise ValueError("A hidden quantity is listed more than once.")
        if self.execution_substrate not in EXECUTION_SUBSTRATES:
            raise ValueError(
                f"Unknown execution substrate {self.execution_substrate!r}; expected "
                f"one of {sorted(EXECUTION_SUBSTRATES)}."
            )

    @property
    def cost(self) -> RouteCost:
        counts = {
            kind: sum(
                action.atomic_units for action in self.actions if action.kind == kind
            )
            for kind in ACTION_KINDS
        }
        return RouteCost(
            relations_selected=counts["relation"],
            hidden_quantities=len(self.hidden_quantities),
            peak_live_relations=max(action.live_relations for action in self.actions),
            symbolic_actions=counts["symbolic"],
            branch_checks=counts["branch"],
            representation_changes=counts["representation"],
            return_checks=counts["return"],
        )


@dataclass(frozen=True)
class RouteComparison:
    status: str
    baseline: HandwrittenRoute
    proposed: HandwrittenRoute
    proposed_better: tuple[str, ...]
    proposed_worse: tuple[str, ...]


@dataclass(frozen=True)
class CostProfile:
    """Declared positive action costs; provenance prevents silent calibration."""

    name: str
    weights: tuple[Fraction, ...]
    provenance: str
    max_peak_live_relations: Optional[int] = None

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.provenance.strip():
            raise ValueError("A cost profile requires a name and provenance.")
        if len(self.weights) != len(COST_AXES):
            raise ValueError(f"A cost profile requires {len(COST_AXES)} weights.")
        normalized = tuple(Fraction(weight) for weight in self.weights)
        if any(weight <= 0 for weight in normalized):
            raise ValueError("Every cost weight must be strictly positive.")
        object.__setattr__(self, "weights", normalized)
        if self.max_peak_live_relations is not None and (
            not isinstance(self.max_peak_live_relations, int)
            or isinstance(self.max_peak_live_relations, bool)
            or self.max_peak_live_relations < 1
        ):
            raise ValueError(
                "max_peak_live_relations must be a positive integer or None."
            )


@dataclass(frozen=True)
class AdmissionBoundary:
    baseline: HandwrittenRoute
    proposed: HandwrittenRoute
    delta: tuple[int, ...]
    classification: str
    proposed_cheaper_when: str


@dataclass(frozen=True)
class AdmissionDecision:
    status: str
    boundary: AdmissionBoundary
    profile: CostProfile
    weighted_delta: Fraction
    reason: str


def compare_exam_routes(
    baseline: HandwrittenRoute,
    proposed: HandwrittenRoute,
) -> RouteComparison:
    """Compare two routes by Pareto order without choosing metric weights."""

    if baseline.problem_id != proposed.problem_id:
        raise ValueError("Exam routes must belong to the same problem.")
    if baseline.target != proposed.target:
        raise ValueError("Exam routes must compute the same physical target.")
    if baseline.execution_substrate != proposed.execution_substrate:
        raise ValueError("Exam routes must use the same execution substrate.")

    base = baseline.cost.as_tuple()
    prop = proposed.cost.as_tuple()
    better = tuple(
        axis for axis, left, right in zip(COST_AXES, prop, base) if left < right
    )
    worse = tuple(
        axis for axis, left, right in zip(COST_AXES, prop, base) if left > right
    )
    if not better and not worse:
        status = "tie"
    elif better and not worse:
        status = "proposed_win"
    elif worse and not better:
        status = "baseline_win"
    else:
        status = "tradeoff"
    return RouteComparison(
        status=status,
        baseline=baseline,
        proposed=proposed,
        proposed_better=better,
        proposed_worse=worse,
    )


def _weighted_term(coefficient: int, axis: str) -> str:
    prefix = "" if coefficient == 1 else f"{coefficient}*"
    return f"{prefix}w_{axis}"


def _proposed_cheaper_inequality(delta: tuple[int, ...]) -> str:
    debt = [
        _weighted_term(value, axis)
        for axis, value in zip(COST_AXES, delta)
        if value > 0
    ]
    saving = [
        _weighted_term(-value, axis)
        for axis, value in zip(COST_AXES, delta)
        if value < 0
    ]
    return f"{' + '.join(debt)} < {' + '.join(saving)}"


def construct_admission_boundary(
    baseline: HandwrittenRoute,
    proposed: HandwrittenRoute,
) -> AdmissionBoundary:
    """Construct the exact positive-weight region where a route is cheaper."""

    comparison = compare_exam_routes(baseline, proposed)
    delta = tuple(
        proposed_value - baseline_value
        for baseline_value, proposed_value in zip(
            baseline.cost.as_tuple(), proposed.cost.as_tuple()
        )
    )
    if comparison.status == "baseline_win":
        classification = "always_direct"
        inequality = "impossible for strictly positive weights"
    elif comparison.status == "proposed_win":
        classification = "always_proposed"
        inequality = "all strictly positive weight profiles"
    elif comparison.status == "tie":
        classification = "equivalent"
        inequality = "never strictly cheaper; equal for all profiles"
    else:
        classification = "conditional"
        inequality = _proposed_cheaper_inequality(delta)
    return AdmissionBoundary(
        baseline=baseline,
        proposed=proposed,
        delta=delta,
        classification=classification,
        proposed_cheaper_when=inequality,
    )


def evaluate_route_admission(
    boundary: AdmissionBoundary,
    profile: CostProfile,
) -> AdmissionDecision:
    """Evaluate a declared learner/tool profile without hiding its provenance."""

    weighted_delta = sum(
        (
            weight * coefficient
            for weight, coefficient in zip(profile.weights, boundary.delta)
        ),
        Fraction(0),
    )
    if (
        profile.max_peak_live_relations is not None
        and boundary.proposed.cost.peak_live_relations > profile.max_peak_live_relations
    ):
        status = "use_direct"
        reason = "proposed_exceeds_peak_budget"
    elif weighted_delta < 0:
        status = "use_proposed"
        reason = "declared_profile_is_inside_proposed_cheaper_region"
    elif weighted_delta > 0:
        status = "use_direct"
        reason = "declared_profile_is_inside_direct_cheaper_region"
    else:
        status = "indifferent"
        reason = "declared_profile_lies_on_break_even_boundary"
    return AdmissionDecision(
        status=status,
        boundary=boundary,
        profile=profile,
        weighted_delta=weighted_delta,
        reason=reason,
    )

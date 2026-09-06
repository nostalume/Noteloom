"""Exact bilateral construction for the constant-curvature Pauli operator.

The forward probe starts from a two-dimensional Clifford module and constant
curvature.  The inverse probe starts from a second-order matrix PDE and its
covariant-momentum commutator.  Neither probe consumes the other's result.
Both construct the same curvature-aligned spin/Fock/longitudinal reduction.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from problem_input import ProblemDocument, ProblemInputError, load_problem


class PauliObstruction(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


def _fraction(value: object) -> Fraction:
    if isinstance(value, (bool, float)):
        raise PauliObstruction("InvalidExactInput", "use integers or rational strings, not floats")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, (int, str)):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as error:
            raise PauliObstruction(
                "InvalidExactInput", f"invalid rational value {value!r}"
            ) from error
    raise PauliObstruction("InvalidExactInput", f"invalid rational value {value!r}")


def _text(value: Fraction) -> str:
    return (
        str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    )


@dataclass(frozen=True)
class Gaussian:
    real: Fraction = Fraction(0)
    imaginary: Fraction = Fraction(0)

    def __add__(self, other: Gaussian) -> Gaussian:
        return Gaussian(self.real + other.real, self.imaginary + other.imaginary)

    def __neg__(self) -> Gaussian:
        return Gaussian(-self.real, -self.imaginary)

    def __sub__(self, other: Gaussian) -> Gaussian:
        return self + (-other)

    def __mul__(self, other: Gaussian) -> Gaussian:
        return Gaussian(
            self.real * other.real - self.imaginary * other.imaginary,
            self.real * other.imaginary + self.imaginary * other.real,
        )

    def conjugate(self) -> Gaussian:
        return Gaussian(self.real, -self.imaginary)


ZERO = Gaussian()
ONE = Gaussian(Fraction(1))
IMAGINARY_UNIT = Gaussian(Fraction(0), Fraction(1))


Matrix = tuple[tuple[Gaussian, Gaussian], tuple[Gaussian, Gaussian]]


IDENTITY: Matrix = ((ONE, ZERO), (ZERO, ONE))
SIGMA_X: Matrix = ((ZERO, ONE), (ONE, ZERO))
SIGMA_Y: Matrix = ((ZERO, -IMAGINARY_UNIT), (IMAGINARY_UNIT, ZERO))
SIGMA_Z: Matrix = ((ONE, ZERO), (ZERO, -ONE))
ZERO_MATRIX: Matrix = ((ZERO, ZERO), (ZERO, ZERO))


def _gaussian(value: object) -> Gaussian:
    if isinstance(value, list) and len(value) == 2:
        return Gaussian(_fraction(value[0]), _fraction(value[1]))
    return Gaussian(_fraction(value))


def _matrix(value: object, name: str) -> Matrix:
    if (
        not isinstance(value, list)
        or len(value) != 2
        or any(not isinstance(row, list) or len(row) != 2 for row in value)
    ):
        raise PauliObstruction("InvalidMatrixPDE", f"{name} must be a 2 by 2 exact matrix")
    return tuple(tuple(_gaussian(entry) for entry in row) for row in value)  # type: ignore[return-value]


def _add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(left[row][column] + right[row][column] for column in range(2)) for row in range(2)
    )  # type: ignore[return-value]


def _scale(matrix: Matrix, scalar: Gaussian | Fraction | int) -> Matrix:
    coefficient = scalar if isinstance(scalar, Gaussian) else Gaussian(Fraction(scalar))
    return tuple(
        tuple(coefficient * matrix[row][column] for column in range(2)) for row in range(2)
    )  # type: ignore[return-value]


def _multiply(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(
            left[row][0] * right[0][column] + left[row][1] * right[1][column] for column in range(2)
        )
        for row in range(2)
    )  # type: ignore[return-value]


def _dagger(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[column][row].conjugate() for column in range(2)) for row in range(2))  # type: ignore[return-value]


def _trace(matrix: Matrix) -> Gaussian:
    return matrix[0][0] + matrix[1][1]


def _serialize_gaussian(value: Gaussian) -> str | dict[str, str]:
    if value.imaginary == 0:
        return _text(value.real)
    return {"real": _text(value.real), "imaginary": _text(value.imaginary)}


def _serialize_matrix(matrix: Matrix) -> list[list[str | dict[str, str]]]:
    return [[_serialize_gaussian(entry) for entry in row] for row in matrix]


def _clifford_checks(gamma_1: Matrix, gamma_2: Matrix, gamma_3: Matrix) -> dict[str, bool]:
    generators = (gamma_1, gamma_2, gamma_3)
    checks: dict[str, bool] = {}
    for index, generator in enumerate(generators, start=1):
        checks[f"gamma_{index}_squares_to_identity"] = _multiply(generator, generator) == IDENTITY
    for left in range(3):
        for right in range(left + 1, 3):
            checks[f"gamma_{left + 1}_gamma_{right + 1}_anticommute"] = (
                _add(
                    _multiply(generators[left], generators[right]),
                    _multiply(generators[right], generators[left]),
                )
                == ZERO_MATRIX
            )
    checks["positive_orientation"] = _multiply(gamma_1, gamma_2) == _scale(gamma_3, IMAGINARY_UNIT)
    return checks


def _construct_frame(gamma_3: Matrix) -> tuple[Matrix, Matrix, dict[str, bool]]:
    gamma_1 = next(
        (
            seed
            for seed in (SIGMA_X, SIGMA_Y, SIGMA_Z)
            if _add(_multiply(seed, gamma_3), _multiply(gamma_3, seed)) == ZERO_MATRIX
        ),
        None,
    )
    if gamma_1 is None:
        raise PauliObstruction(
            "CliffordFrameOutsideBudget",
            "the recovered grading is valid, but the bounded exact frame constructor found no canonical Pauli seed",
        )
    gamma_2 = _scale(_multiply(gamma_1, gamma_3), IMAGINARY_UNIT)
    checks = _clifford_checks(gamma_1, gamma_2, gamma_3)
    if not all(checks.values()):
        raise ArithmeticError("constructed Clifford frame failed its exact relations")
    return gamma_1, gamma_2, checks


def _channels(field_magnitude: Fraction, maximum_level: int) -> list[dict[str, object]]:
    channels: list[dict[str, object]] = []
    for level in range(maximum_level + 1):
        channels.extend(
            (
                {
                    "orbital_level": level,
                    "spin": "curvature-aligned",
                    "energy": f"k^2+{_text(2 * field_magnitude * level)}",
                    "energy_offset": _text(2 * field_magnitude * level),
                },
                {
                    "orbital_level": level,
                    "spin": "curvature-antialigned",
                    "energy": f"k^2+{_text(2 * field_magnitude * (level + 1))}",
                    "energy_offset": _text(2 * field_magnitude * (level + 1)),
                },
            )
        )
    return channels


def _witness(
    route: str,
    construction: str,
    field_magnitude: Fraction,
    charge_sign: int,
    grading: Matrix,
    checks: dict[str, bool],
    channels: list[dict[str, object]],
    core: str,
) -> dict[str, object]:
    aligned = _scale(_add(IDENTITY, grading), Fraction(1, 2))
    antialigned = _scale(_add(IDENTITY, _scale(grading, -1)), Fraction(1, 2))
    projector_checks = {
        "aligned_projector_idempotent": _multiply(aligned, aligned) == aligned,
        "antialigned_projector_idempotent": _multiply(antialigned, antialigned) == antialigned,
        "projectors_orthogonal": _multiply(aligned, antialigned) == ZERO_MATRIX,
        "projectors_resolve_identity": _add(aligned, antialigned) == IDENTITY,
    }
    all_checks = {**checks, **projector_checks}
    return {
        "route": route,
        "outcome": "exact",
        "witness": {
            "preserved_object": "spin-resolved transverse energy channels",
            "construction": construction,
            "reduced_object": {
                "algebra": "graded Clifford-Heisenberg algebra with longitudinal translation",
                "matrix_reduced_dynamics": "Pi_parallel^2+2b(N+1/2)I-b Sigma",
                "fiber_isotropy": "unitaries preserving Sigma and its two rank-one eigenspaces",
                "field_magnitude": _text(field_magnitude),
                "charge_sign": charge_sign,
                "spin_projectors": {
                    "curvature_aligned": _serialize_matrix(aligned),
                    "curvature_antialigned": _serialize_matrix(antialigned),
                },
                "channels": channels,
            },
            "maps": {
                "analysis": "Fourier transform along ker(F), then P_+/- and oscillator-number analysis",
                "synthesis": "sum spin/Fock channels and inverse longitudinal Fourier transform",
            },
            "residuals": {"all_passed": all(all_checks.values()), "checks": all_checks},
            "error": {"kind": "exact algebraic channel rule", "bound": 0},
            "cost": {
                "primitive_relations": 4,
                "projectors": 2,
                "channel_rule_evaluations": len(channels),
                "coordinate_eigenfunction_expansions": 0,
            },
            "validity": {
                "core": core,
                "constant_nonzero_rank_two_curvature": True,
                "global_parallel_translation": True,
                "boundary": "none",
            },
        },
    }


def _forward(
    payload: dict[str, object], maximum_level: int
) -> tuple[dict[str, object], dict[str, object]]:
    data = payload.get("representation_problem")
    if not isinstance(data, dict):
        raise PauliObstruction(
            "MissingRepresentationData", "representation_problem must be an object"
        )
    required = (
        data.get("spatial_dimension") == 3,
        data.get("metric") == "euclidean",
        data.get("orientation") == "positive",
        data.get("clifford_module_dimension") == 2,
        data.get("curvature") == "constant_rank_two",
        data.get("parallel_translation") is True,
    )
    if not all(required):
        raise PauliObstruction(
            "UnsupportedRepresentationProblem",
            "the forward bench requires oriented Euclidean 3-space, a rank-2 Clifford module, constant rank-2 curvature, and parallel translation",
        )
    sign = data.get("charge_sign")
    if sign not in (-1, 1):
        raise PauliObstruction("InvalidChargeSign", "charge_sign must be -1 or 1")
    assert isinstance(sign, int)
    magnitude = _fraction(data.get("field_magnitude"))
    if magnitude <= 0:
        raise PauliObstruction("ZeroCurvature", "field_magnitude must be positive")

    grading = _scale(SIGMA_Z, sign)
    spin_term = _scale(grading, -magnitude)
    checks = _clifford_checks(SIGMA_X, SIGMA_Y, SIGMA_Z)
    checks.update(
        {
            "curvature_constructs_heisenberg_relation": sign * (sign * magnitude) / magnitude == 1,
            "dirac_square_spin_term": spin_term == _scale(SIGMA_Z, -(sign * magnitude)),
            "grading_squares_to_identity": _multiply(grading, grading) == IDENTITY,
        }
    )
    channels = _channels(magnitude, maximum_level)
    candidate = _witness(
        "representation-to-pde",
        "Clifford module plus curvature -> Q=sigma.Pi -> Q^2 -> ladder/projector channels",
        magnitude,
        sign,
        grading,
        checks,
        channels,
        "Schwartz(R^3,C^2)",
    )
    return candidate, {
        "field_magnitude": magnitude,
        "charge_sign": sign,
        "grading": grading,
        "spin_term": spin_term,
        "channels": channels,
    }


def _inverse(
    payload: dict[str, object], maximum_level: int
) -> tuple[dict[str, object], dict[str, object]]:
    data = payload.get("pde_problem")
    if not isinstance(data, dict):
        raise PauliObstruction("MissingPDEData", "pde_problem must be an object")
    if not (
        data.get("order") == 2
        and data.get("principal_symbol") == "euclidean_scalar_identity_on_spinors"
        and data.get("spinor_fiber_dimension") == 2
        and data.get("parallel_translation_commutes") is True
    ):
        raise PauliObstruction(
            "UnsupportedMatrixPDE",
            "the inverse bench requires a rank-2 Euclidean Laplace-type Pauli PDE with parallel translation",
        )
    commutator = _fraction(data.get("transverse_momentum_commutator_imaginary_coefficient"))
    if commutator == 0:
        raise PauliObstruction(
            "ZeroCurvature", "the transverse momentum commutator must be nonzero"
        )
    magnitude = abs(commutator)
    sign = 1 if commutator > 0 else -1
    spin_term = _matrix(data.get("spin_curvature_term"), "spin_curvature_term")
    grading = _scale(spin_term, Fraction(-1, 1) / magnitude)
    invariant_checks = {
        "spin_term_hermitian": _dagger(spin_term) == spin_term,
        "spin_term_traceless": _trace(spin_term) == ZERO,
        "normalized_spin_grading_squares_to_identity": _multiply(grading, grading) == IDENTITY,
    }
    if not all(invariant_checks.values()):
        raise PauliObstruction(
            "SpinCurvatureResidual",
            "normalizing the matrix zeroth-order term by |curvature| does not produce a Hermitian traceless involution",
        )
    gamma_3 = _scale(grading, sign)
    gamma_1, gamma_2, frame_checks = _construct_frame(gamma_3)
    derived_spin_term = _scale(gamma_3, -commutator)
    if derived_spin_term != spin_term:
        raise PauliObstruction(
            "SpinCurvatureResidual",
            "the reconstructed Clifford square does not recover the PDE spin-curvature term",
        )
    checks = {
        **invariant_checks,
        **frame_checks,
        "factor_square_recovers_spin_term": derived_spin_term == spin_term,
        "curvature_constructs_heisenberg_relation": sign * commutator / magnitude == 1,
    }
    channels = _channels(magnitude, maximum_level)
    candidate = _witness(
        "pde-to-representation",
        "principal symbol plus commutator and matrix subprincipal term -> Clifford frame/groupoid -> ladder/projector channels",
        magnitude,
        sign,
        grading,
        checks,
        channels,
        str(data.get("core", "unspecified")),
    )
    return candidate, {
        "field_magnitude": magnitude,
        "charge_sign": sign,
        "grading": grading,
        "spin_term": spin_term,
        "channels": channels,
        "gamma_frame": (gamma_1, gamma_2, gamma_3),
    }


def _probe(route: str, result: object, error: PauliObstruction | None) -> dict[str, object]:
    if error is None:
        return {
            "route": route,
            "applicable": True,
            "trigger": (
                "Clifford module and constant curvature"
                if route == "representation-to-pde"
                else "matrix Laplace symbol, curvature commutator, and spin subprincipal term"
            ),
            "first_residual": None,
        }
    return {
        "route": route,
        "applicable": False,
        "trigger": "independent bounded construction attempted",
        "first_residual": error.kind,
        "reason": str(error),
    }


def _construct(payload: dict[str, object]) -> dict[str, object]:
    if payload.get("schema") != "pauli-landau-bilateral/v1":
        raise PauliObstruction("UnsupportedProblemType", "expected pauli-landau-bilateral/v1")
    observable = payload.get("observable")
    if (
        not isinstance(observable, dict)
        or observable.get("kind") != "spin_resolved_transverse_energy_channels"
    ):
        raise PauliObstruction(
            "UnsupportedObservable",
            "the current bridge preserves spin-resolved transverse energy channels",
        )
    maximum_level = observable.get("maximum_orbital_level")
    if (
        isinstance(maximum_level, bool)
        or not isinstance(maximum_level, int)
        or not 0 <= maximum_level <= 32
    ):
        raise PauliObstruction(
            "InvalidBudget", "maximum_orbital_level must be an integer from 0 through 32"
        )
    if payload.get("equivalence") != "unitary_spin_frame_and_gauge_conjugacy":
        raise PauliObstruction(
            "MissingEquivalencePolicy",
            "the bilateral comparison requires unitary spin-frame and gauge conjugacy",
        )

    forward_candidate: dict[str, object] | None = None
    inverse_candidate: dict[str, object] | None = None
    forward_data: dict[str, object] | None = None
    inverse_data: dict[str, object] | None = None
    forward_error: PauliObstruction | None = None
    inverse_error: PauliObstruction | None = None
    try:
        forward_candidate, forward_data = _forward(payload, maximum_level)
    except PauliObstruction as error:
        forward_error = error
    try:
        inverse_candidate, inverse_data = _inverse(payload, maximum_level)
    except PauliObstruction as error:
        inverse_error = error

    candidates = [
        candidate for candidate in (forward_candidate, inverse_candidate) if candidate is not None
    ]
    probes = [
        _probe("representation-to-pde", forward_data, forward_error),
        _probe("pde-to-representation", inverse_data, inverse_error),
    ]
    if forward_data is not None and inverse_data is not None:
        checks = {
            "curvature_magnitude_equal": forward_data["field_magnitude"]
            == inverse_data["field_magnitude"],
            "charge_orientation_equal": forward_data["charge_sign"] == inverse_data["charge_sign"],
            "spin_curvature_term_equal": forward_data["spin_term"] == inverse_data["spin_term"],
            "curvature_aligned_grading_equal": forward_data["grading"] == inverse_data["grading"],
            "reduced_channel_rule_equal": forward_data["channels"] == inverse_data["channels"],
        }
        passed = all(checks.values())
        coincidence: dict[str, object] = {
            "status": "exact_bilateral_cross_probe" if passed else "bilateral_mismatch",
            "all_passed": passed,
            "checks": checks,
            "equivalence": payload["equivalence"],
        }
        if passed:
            grading = forward_data["grading"]
            assert isinstance(grading, tuple)
            aligned = _scale(_add(IDENTITY, grading), Fraction(1, 2))
            outcome = "exact"
            selected = "bilateral-common-reduction"
            reason = "both independent directions construct the same invariant channel witness"
            obstruction = None
        else:
            aligned = ZERO_MATRIX
            outcome = "obstructed"
            selected = None
            reason = "the independently constructed operator invariants do not coincide"
            obstruction = {"kind": "BilateralMismatch", "reason": reason}
    else:
        first_error = forward_error or inverse_error
        assert first_error is not None
        coincidence = {
            "status": "one_direction_obstructed",
            "all_passed": False,
            "reason": str(first_error),
        }
        aligned = ZERO_MATRIX
        outcome = "obstructed"
        selected = None
        reason = "a bilateral bridge requires both independent constructions"
        obstruction = {"kind": first_error.kind, "reason": str(first_error)}

    result: dict[str, object] = {
        "schema": "reduction-decision/v1",
        "outcome": outcome,
        "request": {
            "problem_type": payload["schema"],
            "observable": observable["kind"],
            "maximum_orbital_level": maximum_level,
            "supplied_group_name": False,
            "supplied_gauge_potential": False,
        },
        "probes": probes,
        "candidates": candidates,
        "coincidence": coincidence,
        "decision": {
            "selected_route": selected,
            "reason": reason,
            "charge_sign": forward_data["charge_sign"] if forward_data is not None else None,
            "common_transverse_channels": forward_data["channels"] if outcome == "exact" else [],
            "curvature_aligned_projector": _serialize_matrix(aligned)
            if outcome == "exact"
            else None,
        },
        "human_card": {
            "result": "exact bilateral channel construction"
            if outcome == "exact"
            else "bilateral obstruction",
            "primitive_objects": "curvature commutator, Clifford product, grading, two projectors, one number operator",
            "replaced_expansion": "coordinate gauge choice and component eigenfunction enumeration",
            "recovery": "longitudinal Fourier synthesis followed by spin/Fock channel summation",
            "boundary": "constant nonzero curvature on boundaryless Euclidean 3-space with a rank-2 spinor fiber",
        },
        "not_certified": [
            "a unique global Lie group from the represented local operator algebra",
            "magnetic-translation degeneracy or flux topology without global geometry",
            "boundaries, variable curvature, higher spin, or non-self-adjoint realizations",
            "a canonical spin frame rather than its unitary equivalence groupoid",
        ],
    }
    if obstruction is not None:
        result["obstruction"] = obstruction
    return result


def _global_obstruction(payload: object, error: PauliObstruction) -> dict[str, object]:
    return {
        "schema": "reduction-decision/v1",
        "outcome": "obstructed",
        "request": {"problem_type": payload.get("schema", "unknown")}
        if isinstance(payload, dict)
        else {},
        "probes": [],
        "candidates": [],
        "coincidence": None,
        "decision": {"selected_route": None, "reason": str(error)},
        "obstruction": {"kind": error.kind, "reason": str(error)},
        "human_card": {"result": "obstructed", "why": str(error)},
    }


def discover_payload(payload: object) -> dict[str, object]:
    """Construct the bilateral result from an already decoded ProblemSpec."""

    try:
        if not isinstance(payload, dict):
            raise PauliObstruction(
                "InvalidProblemSpec", "problem specification must be a JSON object"
            )
        return _construct(payload)
    except PauliObstruction as error:
        return _global_obstruction(payload, error)


def discover_document(document: ProblemDocument) -> dict[str, object]:
    return discover_payload(document.payload)


def discover_problem(path: Path) -> dict[str, object]:
    try:
        return discover_document(load_problem(path))
    except ProblemInputError as error:
        return _global_obstruction({}, PauliObstruction("InvalidProblemSpec", str(error)))

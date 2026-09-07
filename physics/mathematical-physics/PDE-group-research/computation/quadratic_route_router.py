"""Backend-independent route discovery for a bounded quadratic PDE family.

The admitted problem is

    H_L = -Delta + x^T L^2 x

on Schwartz(R^3), together with a one-excitation preparation and its survival
amplitude.  The input supplies the PDE stiffness K and an action L, but no
eigenbasis, group, or reduction route.  This tool verifies L^2=K, constructs the
full-mode and observable-cyclic candidates, proves equality of their finite
spectral measures, and selects relative to the preparation.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from fractions import Fraction
from pathlib import Path

from cyclic_reduce import AdmissibilityError, CyclicReduction, reduce_symmetric_matrix
from problem_input import ProblemDocument, ProblemInputError, load_problem

Matrix = tuple[tuple[Fraction, ...], ...]
Vector = tuple[Fraction, ...]


class RouteObstruction(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


def _fraction(value: object) -> Fraction:
    if isinstance(value, (bool, float)):
        raise RouteObstruction("InvalidExactInput", "use integers or rational strings, not floats")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, (int, str)):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as error:
            raise RouteObstruction(
                "InvalidExactInput", f"invalid rational value {value!r}"
            ) from error
    raise RouteObstruction("InvalidExactInput", f"invalid rational value {value!r}")


def _matrix(values: object, name: str) -> Matrix:
    if not isinstance(values, list) or len(values) != 3:
        raise RouteObstruction("UnsupportedDimension", f"{name} must be a 3 by 3 matrix")
    rows = tuple(
        tuple(_fraction(value) for value in row) for row in values if isinstance(row, list)
    )
    if len(rows) != 3 or any(len(row) != 3 for row in rows):
        raise RouteObstruction("UnsupportedDimension", f"{name} must be a 3 by 3 matrix")
    if rows != _transpose(rows):
        raise RouteObstruction("NonSelfAdjointInput", f"{name} must be symmetric")
    return rows


def _vector(values: object) -> Vector:
    if not isinstance(values, list) or len(values) != 3:
        raise RouteObstruction(
            "UnsupportedDimension", "one-excitation preparation must have dimension 3"
        )
    vector = tuple(_fraction(value) for value in values)
    if all(value == 0 for value in vector):
        raise RouteObstruction("ZeroPreparation", "one-excitation preparation must be nonzero")
    return vector


def _identity() -> Matrix:
    return tuple(tuple(Fraction(int(i == j)) for j in range(3)) for i in range(3))


def _zero() -> Matrix:
    return tuple(tuple(Fraction(0) for _ in range(3)) for _ in range(3))


def _transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[j][i] for j in range(3)) for i in range(3))


def _multiply(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(sum((left[i][k] * right[k][j] for k in range(3)), Fraction(0)) for j in range(3))
        for i in range(3)
    )


def _matvec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(sum((row[j] * vector[j] for j in range(3)), Fraction(0)) for row in matrix)


def _subtract(left: Matrix, right: Matrix) -> Matrix:
    return tuple(tuple(left[i][j] - right[i][j] for j in range(3)) for i in range(3))


def _add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(tuple(left[i][j] + right[i][j] for j in range(3)) for i in range(3))


def _scale(matrix: Matrix, coefficient: Fraction) -> Matrix:
    return tuple(tuple(coefficient * value for value in row) for row in matrix)


def _trace(matrix: Matrix) -> Fraction:
    return sum((matrix[i][i] for i in range(3)), Fraction(0))


def _determinant(matrix: Matrix) -> Fraction:
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def _positive_definite(matrix: Matrix) -> bool:
    first = matrix[0][0]
    second = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return first > 0 and second > 0 and _determinant(matrix) > 0


def _integer_divisors(value: int) -> list[int]:
    value = abs(value)
    if value == 0:
        return [1]
    divisors: set[int] = set()
    for candidate in range(1, math.isqrt(value) + 1):
        if value % candidate == 0:
            divisors.add(candidate)
            divisors.add(value // candidate)
    return sorted(divisors)


def _evaluate_descending(coefficients: Sequence[Fraction], value: Fraction) -> Fraction:
    result = Fraction(0)
    for coefficient in coefficients:
        result = result * value + coefficient
    return result


def _rational_roots(coefficients: Sequence[Fraction]) -> list[Fraction]:
    remaining = list(coefficients)
    roots: list[Fraction] = []
    while len(remaining) > 2:
        if remaining[-1] == 0:
            root = Fraction(0)
        else:
            denominator = math.lcm(*(value.denominator for value in remaining))
            integers = [int(value * denominator) for value in remaining]
            candidates = {
                Fraction(sign * numerator, divisor)
                for numerator in _integer_divisors(integers[-1])
                for divisor in _integer_divisors(integers[0])
                for sign in (-1, 1)
            }
            root = next(
                (
                    candidate
                    for candidate in sorted(candidates)
                    if _evaluate_descending(remaining, candidate) == 0
                ),
                None,
            )
            if root is None:
                raise RouteObstruction(
                    "NonRationalSpectrum",
                    "the bounded exact factor probe requires a rationally split spectrum",
                )
        quotient = [remaining[0]]
        for coefficient in remaining[1:-1]:
            quotient.append(coefficient + root * quotient[-1])
        roots.append(root)
        remaining = quotient
    roots.append(-remaining[1] / remaining[0])
    return sorted(roots)


def _eigenvalues(matrix: Matrix) -> list[Fraction]:
    trace = _trace(matrix)
    square_trace = _trace(_multiply(matrix, matrix))
    second = (trace * trace - square_trace) / 2
    return _rational_roots((Fraction(1), -trace, second, -_determinant(matrix)))


def _spectral_projectors(matrix: Matrix, eigenvalues: Sequence[Fraction]) -> list[Matrix]:
    if len(set(eigenvalues)) != 3:
        raise RouteObstruction(
            "DegenerateSpectrumOutsideBench",
            "the bounded factor probe requires three distinct frequencies",
        )
    projectors: list[Matrix] = []
    identity = _identity()
    for eigenvalue in eigenvalues:
        projector = identity
        for other in eigenvalues:
            if other != eigenvalue:
                projector = _scale(
                    _multiply(projector, _subtract(matrix, _scale(identity, other))),
                    1 / (eigenvalue - other),
                )
        projectors.append(projector)
    if _sum_matrices(projectors) != identity:
        raise ArithmeticError("spectral projectors do not resolve the identity")
    for i, projector in enumerate(projectors):
        for j, other in enumerate(projectors):
            expected = projector if i == j else _zero()
            if _multiply(projector, other) != expected:
                raise ArithmeticError("spectral projectors fail exact orthogonality")
    return projectors


def _sum_matrices(matrices: Iterable[Matrix]) -> Matrix:
    result = _zero()
    for matrix in matrices:
        result = _add(result, matrix)
    return result


def _pair(left: Vector, metric: Matrix, right: Vector) -> Fraction:
    image = _matvec(metric, right)
    return sum((left[i] * image[i] for i in range(3)), Fraction(0))


def _fraction_text(value: Fraction) -> str:
    return (
        str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    )


def _serialize_vector(vector: Vector) -> list[str]:
    return [_fraction_text(value) for value in vector]


def _serialize_matrix(matrix: Matrix) -> list[list[str]]:
    return [_serialize_vector(row) for row in matrix]


def _polynomial_at(coefficients: Sequence[Fraction], value: Fraction) -> Fraction:
    return sum(
        (coefficient * value**power for power, coefficient in enumerate(coefficients)), Fraction(0)
    )


def _factor_moments(
    operator: Matrix, metric: Matrix, preparation: Vector, count: int
) -> tuple[Fraction, ...]:
    norm = _pair(preparation, metric, preparation)
    state = preparation
    moments: list[Fraction] = []
    for _ in range(count):
        moments.append(_pair(preparation, metric, state) / norm)
        state = _matvec(operator, state)
    return tuple(moments)


def _request_summary(payload: dict[str, object], budget: int) -> dict[str, object]:
    operator = payload["operator"]
    preparation = payload["preparation"]
    observable = payload["observable"]
    assert (
        isinstance(operator, dict)
        and isinstance(preparation, dict)
        and isinstance(observable, dict)
    )
    return {
        "problem_type": payload["schema"],
        "operator": "H_L=-Delta+x^T L^2 x",
        "dimension": 3,
        "core": operator.get("core", "unspecified"),
        "preparation": "one excitation W(u)",
        "observable": observable["kind"],
        "reuse": payload["reuse"],
        "max_cyclic_steps": budget,
        "shared_resource": "verified rational frequency action L with L^2=K",
    }


def _obstructed(payload: object, error: RouteObstruction) -> dict[str, object]:
    return {
        "schema": "reduction-decision/v1",
        "outcome": "obstructed",
        "request": {"problem_type": payload.get("schema", "unknown")}
        if isinstance(payload, dict)
        else {},
        "probes": [
            {"route": "full-modes", "applicable": False, "first_residual": error.kind},
            {"route": "observable-cyclic", "applicable": False, "first_residual": error.kind},
        ],
        "candidates": [],
        "coincidence": None,
        "decision": {"selected_route": None, "reason": str(error)},
        "obstruction": {"kind": error.kind, "reason": str(error)},
        "human_card": {
            "result": "obstructed",
            "why": str(error),
            "reentry": "supply data satisfying the stated bounded quadratic contract",
        },
    }


def _cyclic_candidate(cyclic: CyclicReduction) -> dict[str, object]:
    raw = cyclic.to_dict()
    exact = cyclic.status == "ExactCyclicReduction"
    return {
        "route": "observable-cyclic",
        "outcome": "exact" if exact else "formal",
        "witness": {
            "preserved_object": "one-excitation survival amplitude",
            "construction": "preparation-generated L-metric Krylov carrier",
            "reduced_object": {
                "kind": "Jacobi recurrence",
                "dimension": cyclic.carrier_dimension,
                "recurrence": raw["recurrence"],
            },
            "maps": raw["analysis_synthesis"],
            "residuals": {"all_passed": True, "checks": raw["certificates"]},
            "error": (
                {"kind": "exact", "bound": 0}
                if exact
                else {"kind": "uncertified boundary", "truncation": raw["truncation"]}
            ),
            "cost": raw["costs"],
            "validity": raw["validity"],
        },
    }


def _factor_candidate(
    frequency: Matrix,
    preparation: Vector,
    ground_energy: Fraction,
) -> tuple[dict[str, object], list[dict[str, str]], list[Fraction], list[Matrix]]:
    frequencies = _eigenvalues(frequency)
    if any(value <= 0 for value in frequencies):
        raise RouteObstruction(
            "NonPositiveFrequencyAction", "L must be positive for the lowest-weight carrier"
        )
    projectors = _spectral_projectors(frequency, frequencies)
    if any(
        _multiply(frequency, projector) != _scale(projector, value)
        for value, projector in zip(frequencies, projectors)
    ):
        raise ArithmeticError("factor probe failed its eigenprojector residual")

    norm = _pair(preparation, frequency, preparation)
    spectral_measure: list[dict[str, str]] = []
    visible_energies: list[Fraction] = []
    for value, projector in zip(frequencies, projectors):
        component = _matvec(projector, preparation)
        weight = _pair(component, frequency, component) / norm
        if weight:
            energy = ground_energy + 2 * value
            visible_energies.append(energy)
            spectral_measure.append(
                {"energy": _fraction_text(energy), "weight": _fraction_text(weight)}
            )

    return (
        {
            "route": "full-modes",
            "outcome": "exact",
            "witness": {
                "preserved_object": "one-excitation survival amplitude",
                "construction": "positive frequency action -> primitive spectral projectors",
                "reduced_object": {
                    "kind": "complete one-excitation mode decomposition",
                    "dimension": 3,
                    "frequencies": [_fraction_text(value) for value in frequencies],
                    "visible_spectral_measure": spectral_measure,
                },
                "maps": {
                    "analysis": [_serialize_matrix(projector) for projector in projectors],
                    "synthesis": "sum the three spectral components",
                },
                "residuals": {"all_passed": True},
                "error": {"kind": "exact", "bound": 0},
                "cost": {
                    "spectral_projectors": 3,
                    "retained_directions": 3,
                    "semantic_steps": 4,
                },
                "validity": {
                    "dimension": 3,
                    "distinct_positive_rational_frequencies": True,
                },
            },
        },
        spectral_measure,
        visible_energies,
        projectors,
    )


def _construct(payload: dict[str, object]) -> dict[str, object]:
    if payload.get("schema") != "quadratic-schrodinger/v1":
        raise RouteObstruction("UnsupportedProblemType", "expected quadratic-schrodinger/v1")
    operator = payload.get("operator")
    preparation_data = payload.get("preparation")
    observable = payload.get("observable")
    resources = payload.get("resource_budget", {})
    if not all(
        isinstance(value, dict) for value in (operator, preparation_data, observable, resources)
    ):
        raise RouteObstruction(
            "InvalidProblemSpec",
            "operator, preparation, observable, and resource_budget must be objects",
        )
    assert isinstance(operator, dict)
    assert isinstance(preparation_data, dict)
    assert isinstance(observable, dict)
    assert isinstance(resources, dict)
    if operator.get("kinetic") != "identity":
        raise RouteObstruction(
            "UnsupportedKineticForm", "the current bench admits identity kinetic form only"
        )
    if observable.get("kind") != "one_excitation_survival_amplitude":
        raise RouteObstruction(
            "UnsupportedObservable", "the current bench preserves one-excitation survival amplitude"
        )
    reuse = payload.get("reuse")
    if reuse not in {"single_preparation", "many_preparations", "full_spectrum"}:
        raise RouteObstruction(
            "InvalidReusePolicy",
            "reuse must be single_preparation, many_preparations, or full_spectrum",
        )

    stiffness = _matrix(operator.get("stiffness"), "stiffness")
    if not _positive_definite(stiffness):
        raise RouteObstruction(
            "NonPositiveStiffness", "the PDE is not in the positive confining quadratic class"
        )
    if "frequency_action" not in operator:
        raise RouteObstruction(
            "MissingFrequencyAction",
            "constructing the positive square root from stiffness is unimplemented and may erase cyclic leverage",
        )
    frequency = _matrix(operator["frequency_action"], "frequency_action")
    if _multiply(frequency, frequency) != stiffness:
        raise RouteObstruction(
            "FrequencyActionResidual", "the supplied action does not satisfy L^2=K"
        )
    if not _positive_definite(frequency):
        raise RouteObstruction(
            "NonPositiveFrequencyAction", "L must be positive for the lowest-weight carrier"
        )

    preparation = _vector(preparation_data.get("one_excitation"))
    budget_value = resources.get("max_cyclic_steps", 3)
    if (
        isinstance(budget_value, bool)
        or not isinstance(budget_value, int)
        or not 1 <= budget_value <= 3
    ):
        raise RouteObstruction(
            "InvalidBudget", "max_cyclic_steps must be an integer from 1 through 3"
        )

    ground_energy = _trace(frequency)
    reduced_operator = _add(_scale(_identity(), ground_energy), _scale(frequency, Fraction(2)))
    norm = _pair(preparation, frequency, preparation)
    if norm <= 0:
        raise RouteObstruction("NonPositivePreparation", "preparation has nonpositive L-norm")

    try:
        cyclic = reduce_symmetric_matrix(
            reduced_operator,
            preparation,
            metric=frequency,
            budget=budget_value,
        )
    except AdmissibilityError as error:
        raise RouteObstruction("CyclicProbeRefusal", str(error)) from error

    cyclic_exact = cyclic.status == "ExactCyclicReduction"
    cyclic_candidate = _cyclic_candidate(cyclic)
    factor_error: RouteObstruction | None = None
    factor_candidate: dict[str, object] | None = None
    spectral_measure: list[dict[str, str]] | None = None
    try:
        factor_candidate, spectral_measure, visible_energies, projectors = _factor_candidate(
            frequency, preparation, ground_energy
        )
    except RouteObstruction as error:
        factor_error = error

    if factor_candidate is not None:
        factor_moments = _factor_moments(
            reduced_operator,
            frequency,
            preparation,
            len(cyclic.normalized_moments),
        )
        recurrence_roots_match = cyclic.minimal_polynomial is not None and all(
            _polynomial_at(cyclic.minimal_polynomial, energy) == 0 for energy in visible_energies
        )
        checks = {
            "frequency_action_squares_to_stiffness": True,
            "factor_projectors_resolve_identity": _sum_matrices(projectors) == _identity(),
            "spectral_weights_sum_to_one": sum(
                (Fraction(item["weight"]) for item in spectral_measure), Fraction(0)
            )
            == 1,
            "factor_and_cyclic_moments_equal": factor_moments == cyclic.normalized_moments,
            "visible_support_equals_cyclic_degree": len(visible_energies)
            == cyclic.carrier_dimension,
            "cyclic_minimal_polynomial_has_visible_energies": recurrence_roots_match,
        }
        if not all(checks.values()):
            raise ArithmeticError("factor and cyclic observable witnesses do not coincide")
        coincidence: dict[str, object] = {
            "status": "exact_cross_probe",
            "all_passed": True,
            "checks": checks,
            "common_spectral_measure": spectral_measure,
            "moments_checked_through": len(factor_moments) - 1,
        }
        candidates = [factor_candidate, cyclic_candidate]
    else:
        coincidence = {
            "status": "single_applicable_route",
            "all_passed": True,
            "reason": "the cyclic witness is exact; the bounded factor probe returned an obstruction",
        }
        candidates = [cyclic_candidate]

    if cyclic_exact and factor_candidate is None:
        selected = "observable-cyclic"
        reason = "the cyclic witness is exact and the bounded factor probe is inapplicable"
    elif cyclic_exact and cyclic.carrier_dimension < 3 and reuse == "single_preparation":
        selected = "observable-cyclic"
        reason = "exact cyclic termination removes preparation-invisible directions"
    else:
        selected = "full-modes" if factor_candidate is not None else None
        reason = (
            "the cyclic carrier has no dimension gain"
            if cyclic_exact and cyclic.carrier_dimension == 3
            else "reuse policy or incomplete cyclic termination favors the complete mode construction"
        )

    eliminated = 3 - cyclic.carrier_dimension if cyclic_exact else 0
    outcome = "exact" if selected is not None else "formal"
    probes = [
        (
            {
                "route": "full-modes",
                "applicable": True,
                "trigger": "verified positive frequency action with rationally split spectrum",
                "first_residual": None,
            }
            if factor_error is None
            else {
                "route": "full-modes",
                "applicable": False,
                "trigger": "exact rational spectral split attempted",
                "first_residual": factor_error.kind,
                "reason": str(factor_error),
            }
        ),
        {
            "route": "observable-cyclic",
            "applicable": True,
            "trigger": "one preparation and survival observable define a cyclic carrier",
            "first_residual": None,
        },
    ]
    return {
        "schema": "reduction-decision/v1",
        "outcome": outcome,
        "request": _request_summary(payload, budget_value),
        "probes": probes,
        "candidates": candidates,
        "coincidence": coincidence,
        "decision": {
            "selected_route": selected,
            "reason": reason,
            "ambient_dimension": 3,
            "visible_dimension": cyclic.carrier_dimension,
            "reuse": reuse,
            "shared_cost": "verify/apply L and lift H to tr(L)I+2L",
            "comparison_overhead": (
                "both candidates were constructed for this audit"
                if factor_candidate is not None
                else "the bounded factor probe stopped at its first obstruction"
            ),
        },
        "human_card": {
            "result": f"select {selected}",
            "applies_because": (
                "both routes exactly intertwine the one-excitation coefficient dynamics"
                if factor_candidate is not None
                else "the cyclic recurrence terminates exactly without a rational spectral split"
            ),
            "eliminated_directions": eliminated,
            "retained_object": (
                f"Jacobi recurrence of length {cyclic.carrier_dimension}"
                if selected == "observable-cyclic"
                else "three primitive frequency projectors"
            ),
            "recovery": "evaluate the selected finite spectral measure against exp(-it lambda)",
            "certificate": (
                "factor and cyclic moments plus visible support coincide exactly"
                if factor_candidate is not None
                else "exact Krylov termination and moment recovery"
            ),
            "boundary": "dimension 3, rational exact arithmetic, supplied L with verified L^2=K, one-excitation observable",
        },
        "not_certified": [
            "a cheap construction of L from an opaque stiffness K",
            "a full-mode witness for irrational or repeated frequency spectra",
            "higher-excitation or nonlinear observables",
            "automatic routing outside quadratic-schrodinger/v1",
        ],
    }


def discover_document(document: ProblemDocument) -> dict[str, object]:
    """Discover and compare admitted routes from an admitted document."""

    payload: object = document.payload
    try:
        return _construct(payload)
    except RouteObstruction as error:
        return _obstructed(payload, error)


def discover_problem(path: Path) -> dict[str, object]:
    """Compatibility adapter for direct path-based callers."""

    try:
        return discover_document(load_problem(path))
    except ProblemInputError as error:
        return _obstructed({}, RouteObstruction("InvalidProblemSpec", str(error)))

"""Exact observable-cyclic reduction for finite self-adjoint operator actions.

The semantic output is an orthogonal three-term recurrence.  Coordinates are
retained only as a machine-checkable certificate; no eigendecomposition is used.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

Vector = tuple[Fraction, ...]
Matrix = tuple[tuple[Fraction, ...], ...]
Action = Callable[[Vector], Sequence[Fraction | int | str]]
InnerProduct = Callable[[Vector, Vector], Fraction]


class AdmissibilityError(ValueError):
    """The supplied data do not satisfy the exact reduction contract."""


def _fraction(value: Fraction | int | str) -> Fraction:
    if isinstance(value, (bool, float)):
        raise AdmissibilityError(
            "exact rational mode accepts integers, rational strings, or Fraction values"
        )
    if isinstance(value, Fraction):
        return value
    if isinstance(value, (int, str)):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as error:
            raise AdmissibilityError(f"invalid exact rational value: {value!r}") from error
    raise AdmissibilityError(
        "exact rational mode accepts integers, rational strings, or Fraction values"
    )


def _vector(values: Iterable[Fraction | int | str], dimension: int) -> Vector:
    result = tuple(_fraction(value) for value in values)
    if len(result) != dimension:
        raise AdmissibilityError(
            f"vector dimension {len(result)} does not match declared dimension {dimension}"
        )
    return result


def _dot(left: Vector, right: Vector) -> Fraction:
    return sum((x * y for x, y in zip(left, right)), Fraction(0))


def _add_scaled(*terms: tuple[Fraction, Vector]) -> Vector:
    dimension = len(terms[0][1])
    return tuple(
        sum((scale * vector[index] for scale, vector in terms), Fraction(0))
        for index in range(dimension)
    )


def _is_zero(vector: Vector) -> bool:
    return all(value == 0 for value in vector)


def _poly_step(
    current: tuple[Fraction, ...],
    previous: tuple[Fraction, ...],
    alpha: Fraction,
    backward: Fraction,
) -> tuple[Fraction, ...]:
    result = [Fraction(0)] * (len(current) + 1)
    for index, coefficient in enumerate(current):
        result[index] -= alpha * coefficient
        result[index + 1] += coefficient
    for index, coefficient in enumerate(previous):
        result[index] -= backward * coefficient
    return tuple(result)


def _matvec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(_dot(row, vector) for row in matrix)


def _identity(dimension: int) -> Matrix:
    return tuple(
        tuple(Fraction(int(row == column)) for column in range(dimension))
        for row in range(dimension)
    )


def _matrix(values: Sequence[Sequence[Fraction | int | str]], name: str) -> Matrix:
    dimension = len(values)
    if dimension == 0:
        raise AdmissibilityError(f"{name} must be nonempty")
    rows = tuple(tuple(_fraction(value) for value in row) for row in values)
    if any(len(row) != dimension for row in rows):
        raise AdmissibilityError(f"{name} must be square")
    return rows


def _transpose(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[row][column] for row in range(len(matrix))) for column in range(len(matrix))
    )


def _matmul(left: Matrix, right: Matrix) -> Matrix:
    right_t = _transpose(right)
    return tuple(tuple(_dot(row, column) for column in right_t) for row in left)


def _is_symmetric(matrix: Matrix) -> bool:
    return matrix == _transpose(matrix)


def _check_positive_definite(metric: Matrix) -> None:
    """Exact LDL^T test; positivity of every pivot certifies SPD."""

    if not _is_symmetric(metric):
        raise AdmissibilityError("metric must be symmetric")
    dimension = len(metric)
    lower = [[Fraction(0) for _ in range(dimension)] for _ in range(dimension)]
    diagonal = [Fraction(0) for _ in range(dimension)]
    for row in range(dimension):
        lower[row][row] = Fraction(1)
        pivot = metric[row][row] - sum(
            (lower[row][k] * lower[row][k] * diagonal[k] for k in range(row)),
            Fraction(0),
        )
        if pivot <= 0:
            raise AdmissibilityError("metric must be positive definite")
        diagonal[row] = pivot
        for target in range(row + 1, dimension):
            numerator = metric[target][row] - sum(
                (lower[target][k] * lower[row][k] * diagonal[k] for k in range(row)),
                Fraction(0),
            )
            lower[target][row] = numerator / pivot


def _fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _json_value(value):
    if isinstance(value, Fraction):
        return _fraction_text(value)
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    return value


@dataclass(frozen=True)
class CyclicReduction:
    status: str
    ambient_dimension: int
    carrier_dimension: int
    basis: tuple[Vector, ...]
    gram_diagonal: tuple[Fraction, ...]
    alpha: tuple[Fraction, ...]
    beta_squared: tuple[Fraction, ...]
    reduced_operator: Matrix
    minimal_polynomial: tuple[Fraction, ...] | None
    boundary_residual: Vector | None
    boundary_beta_squared: Fraction | None
    error_bound_squared: Fraction | None
    time_horizon: Fraction | None
    tolerance: Fraction | None
    normalized_moments: tuple[Fraction, ...]
    certificates: dict[str, object]
    costs: dict[str, int]

    @property
    def no_dimension_gain(self) -> bool | None:
        if self.minimal_polynomial is None:
            return None
        return self.carrier_dimension == self.ambient_dimension

    @property
    def dimension_verdict(self) -> str:
        if self.minimal_polynomial is None:
            return "budget_truncation_not_invisibility"
        if self.no_dimension_gain:
            return "exact_no_dimension_gain"
        return "exact_invisible_directions_removed"

    def summary(self) -> str:
        """Return the compact human object: recurrence, certificate, and boundary."""

        alpha = ", ".join(_fraction_text(value) for value in self.alpha)
        beta = ", ".join(_fraction_text(value) for value in self.beta_squared)
        lines = [
            (f"{self.status}: ambient {self.ambient_dimension} -> cyclic {self.carrier_dimension}"),
            f"recurrence alpha: [{alpha}]",
            f"recurrence beta^2: [{beta}]",
        ]
        if self.minimal_polynomial is not None:
            polynomial = ", ".join(_fraction_text(value) for value in self.minimal_polynomial)
            lines.append(f"minimal polynomial coefficients: [{polynomial}]")
        else:
            lines.append(
                "boundary beta^2: " + _fraction_text(self.boundary_beta_squared or Fraction(0))
            )
            if self.error_bound_squared is not None:
                lines.append(
                    "certified survival-error bound squared at time horizon "
                    + _fraction_text(self.time_horizon or Fraction(0))
                    + ": "
                    + _fraction_text(self.error_bound_squared)
                    + " <= tolerance squared "
                    + _fraction_text((self.tolerance or Fraction(0)) ** 2)
                )
        removed = self.ambient_dimension - self.carrier_dimension
        if self.minimal_polynomial is None:
            lines.append(
                "selection: budget truncation; excluded directions are not certified invisible"
            )
        elif removed:
            noun = "dimension" if removed == 1 else "dimensions"
            lines.append(f"selection: removes {removed} invisible {noun}")
        else:
            lines.append("selection: no ambient dimension gain")
        lines.extend(
            [
                (
                    "checks: exact recurrence; reduced metric self-adjoint; "
                    f"moments k=0..{self.certificates['moment_match_through']} recovered"
                ),
                "ambiguity: this visible recurrence does not determine a unique group",
            ]
        )
        return "\n".join(lines)

    def to_dict(self) -> dict[str, object]:
        return _json_value(
            {
                "schema_version": 1,
                "arithmetic": "exact_rational",
                "status": self.status,
                "ambient_dimension": self.ambient_dimension,
                "carrier_dimension": self.carrier_dimension,
                "no_dimension_gain": self.no_dimension_gain,
                "dimension_verdict": self.dimension_verdict,
                "recurrence": {
                    "alpha": self.alpha,
                    "beta_squared": self.beta_squared,
                    "convention": ("H q_j = q_(j+1) + alpha_j q_j + beta_squared_j q_(j-1)"),
                },
                "reduced_operator": self.reduced_operator,
                "minimal_polynomial": self.minimal_polynomial,
                "analysis_synthesis": {
                    "basis": self.basis,
                    "gram_diagonal": self.gram_diagonal,
                    "analysis": "A(x)_j=<q_j,x>/<q_j,q_j>",
                    "synthesis": "S(c)=sum_j c_j q_j",
                },
                "truncation": {
                    "boundary_residual": self.boundary_residual,
                    "boundary_beta_squared": self.boundary_beta_squared,
                    "error_bound_squared": self.error_bound_squared,
                    "time_horizon": self.time_horizon,
                    "tolerance": self.tolerance,
                    "bound": (
                        "|survival_full(t)-survival_reduced(t)| <= |t| sqrt(boundary_beta_squared)"
                        if self.boundary_beta_squared is not None
                        else None
                    ),
                },
                "observable_recovery": {
                    "normalized_moments": self.normalized_moments,
                    "meaning": "<psi,H^k psi>/<psi,psi>",
                },
                "certificates": self.certificates,
                "costs": self.costs,
                "validity": {
                    "operator_class": "finite-dimensional self-adjoint",
                    "coefficient_domain": "rational",
                    "zero_policy": "exact",
                    "observable": "spectral response of the supplied preparation",
                },
                "ambiguity": (
                    "the recurrence determines the visible cyclic representation, "
                    "not a unique Lie group or invisible multiplicities"
                ),
            }
        )


def cyclic_reduce(
    action: Action,
    preparation: Sequence[Fraction | int | str],
    *,
    dimension: int,
    budget: int | None = None,
    inner_product: InnerProduct | None = None,
    self_adjoint_certificate: str,
    time_horizon: Fraction | int | str | None = None,
    tolerance: Fraction | int | str | None = None,
) -> CyclicReduction:
    """Construct an exact cyclic recurrence from an operator-action oracle.

    ``self_adjoint_certificate`` is supplied metadata at this boundary.  Use
    :func:`reduce_symmetric_matrix` when the finite matrix should be checked by
    the tool itself.
    """

    if dimension <= 0:
        raise AdmissibilityError("dimension must be positive")
    if budget is None:
        budget = dimension
    if isinstance(budget, bool) or not isinstance(budget, int) or not 1 <= budget <= dimension:
        raise AdmissibilityError("budget must be an integer between 1 and dimension")
    if not self_adjoint_certificate:
        raise AdmissibilityError("a self-adjointness certificate is required")
    if (time_horizon is None) != (tolerance is None):
        raise AdmissibilityError("time_horizon and tolerance must be supplied together")
    horizon = _fraction(time_horizon) if time_horizon is not None else None
    target = _fraction(tolerance) if tolerance is not None else None
    if horizon is not None and (horizon < 0 or target is None or target < 0):
        raise AdmissibilityError("time_horizon and tolerance must be nonnegative")

    psi = _vector(preparation, dimension)
    raw_pairing = inner_product or _dot

    def pairing(left: Vector, right: Vector) -> Fraction:
        return _fraction(raw_pairing(left, right))

    psi_norm = pairing(psi, psi)
    if psi_norm <= 0:
        raise AdmissibilityError("preparation must have positive norm")

    basis: list[Vector] = []
    norms: list[Fraction] = []
    alphas: list[Fraction] = []
    backward_coefficients: list[Fraction] = []
    action_values: list[Vector] = []
    polynomial_previous: tuple[Fraction, ...] = ()
    polynomial_current: tuple[Fraction, ...] = (Fraction(1),)
    minimal_polynomial: tuple[Fraction, ...] | None = None
    boundary_residual: Vector | None = None
    boundary_beta_squared: Fraction | None = None

    previous = tuple(Fraction(0) for _ in range(dimension))
    previous_norm = Fraction(1)
    current = psi

    for index in range(budget):
        current_norm = pairing(current, current)
        if current_norm <= 0:
            raise AdmissibilityError("inner product is not positive on the generated carrier")
        basis.append(current)
        norms.append(current_norm)

        image = _vector(action(current), dimension)
        action_values.append(image)
        alpha = pairing(current, image) / current_norm
        alphas.append(alpha)
        backward = Fraction(0) if index == 0 else current_norm / previous_norm
        if index > 0:
            backward_coefficients.append(backward)

        following = _add_scaled(
            (Fraction(1), image),
            (-alpha, current),
            (-backward, previous),
        )
        next_polynomial = _poly_step(
            polynomial_current,
            polynomial_previous,
            alpha,
            backward,
        )

        for old in basis:
            if pairing(old, following) != 0:
                raise AdmissibilityError(
                    "generated recurrence is not orthogonal; "
                    "the supplied action may not be self-adjoint"
                )

        if _is_zero(following):
            minimal_polynomial = next_polynomial
            break
        if index + 1 == budget:
            boundary_residual = following
            following_norm = pairing(following, following)
            if following_norm <= 0:
                raise AdmissibilityError("boundary residual has nonpositive norm")
            boundary_beta_squared = following_norm / current_norm
            break

        previous, previous_norm = current, current_norm
        current = following
        polynomial_previous, polynomial_current = polynomial_current, next_polynomial

    carrier_dimension = len(basis)
    reduced = [[Fraction(0) for _ in range(carrier_dimension)] for _ in range(carrier_dimension)]
    for column, alpha in enumerate(alphas):
        reduced[column][column] = alpha
        if column > 0:
            reduced[column - 1][column] = backward_coefficients[column - 1]
        if column + 1 < carrier_dimension:
            reduced[column + 1][column] = Fraction(1)
    reduced_operator = tuple(tuple(row) for row in reduced)

    recurrence_ok = True
    for column, image in enumerate(action_values):
        coefficients = tuple(reduced[row][column] for row in range(carrier_dimension))
        reconstructed = tuple(
            sum(
                (basis[row][coordinate] * coefficients[row] for row in range(carrier_dimension)),
                Fraction(0),
            )
            for coordinate in range(dimension)
        )
        expected_residual = (
            boundary_residual
            if boundary_residual is not None and column + 1 == carrier_dimension
            else tuple(Fraction(0) for _ in range(dimension))
        )
        if image != _add_scaled((Fraction(1), reconstructed), (Fraction(1), expected_residual)):
            recurrence_ok = False

    moment_order = 2 * carrier_dimension - 1
    full_state = psi
    reduced_state = tuple(Fraction(int(index == 0)) for index in range(carrier_dimension))
    normalized_moments: list[Fraction] = []
    reduced_moments: list[Fraction] = []
    for order in range(moment_order + 1):
        normalized_moments.append(pairing(psi, full_state) / psi_norm)
        reduced_moments.append(reduced_state[0])
        if order < moment_order:
            full_state = _vector(action(full_state), dimension)
            reduced_state = _matvec(reduced_operator, reduced_state)
    moment_recovery = tuple(normalized_moments) == tuple(reduced_moments)

    reduced_gram = tuple(
        tuple(norms[row] if row == column else Fraction(0) for column in range(carrier_dimension))
        for row in range(carrier_dimension)
    )
    reduced_metric_self_adjoint = _matmul(_transpose(reduced_operator), reduced_gram) == _matmul(
        reduced_gram, reduced_operator
    )
    if not (recurrence_ok and moment_recovery and reduced_metric_self_adjoint):
        raise ArithmeticError("internal cyclic-reduction certificate failed")

    error_bound_squared = None
    if minimal_polynomial is not None:
        status = "ExactCyclicReduction"
    else:
        if horizon is not None and boundary_beta_squared is not None:
            error_bound_squared = horizon * horizon * boundary_beta_squared
        if (
            error_bound_squared is not None
            and target is not None
            and error_bound_squared <= target * target
        ):
            status = "ControlledCyclicReduction"
        else:
            status = "FormalTruncation"

    certificates: dict[str, object] = {
        "self_adjoint": self_adjoint_certificate,
        "orthogonal_basis": True,
        "three_term_recurrence": recurrence_ok,
        "reduced_metric_self_adjoint": reduced_metric_self_adjoint,
        "moment_recovery": moment_recovery,
        "moment_match_through": moment_order,
        "exact_termination": minimal_polynomial is not None,
    }
    costs = {
        "construction_action_calls": carrier_dimension,
        "moment_certificate_action_calls": moment_order,
        "stored_ambient_vectors": carrier_dimension + int(boundary_residual is not None),
    }
    return CyclicReduction(
        status=status,
        ambient_dimension=dimension,
        carrier_dimension=carrier_dimension,
        basis=tuple(basis),
        gram_diagonal=tuple(norms),
        alpha=tuple(alphas),
        beta_squared=tuple(backward_coefficients),
        reduced_operator=reduced_operator,
        minimal_polynomial=minimal_polynomial,
        boundary_residual=boundary_residual,
        boundary_beta_squared=boundary_beta_squared,
        error_bound_squared=error_bound_squared,
        time_horizon=horizon,
        tolerance=target,
        normalized_moments=tuple(normalized_moments),
        certificates=certificates,
        costs=costs,
    )


def reduce_symmetric_matrix(
    matrix: Sequence[Sequence[Fraction | int | str]],
    preparation: Sequence[Fraction | int | str],
    *,
    metric: Sequence[Sequence[Fraction | int | str]] | None = None,
    budget: int | None = None,
    time_horizon: Fraction | int | str | None = None,
    tolerance: Fraction | int | str | None = None,
) -> CyclicReduction:
    """Validate a rational matrix realization, then run the action-level reducer."""

    operator = _matrix(matrix, "matrix")
    dimension = len(operator)
    gram = _identity(dimension) if metric is None else _matrix(metric, "metric")
    if len(gram) != dimension:
        raise AdmissibilityError("metric dimension must match matrix dimension")
    _check_positive_definite(gram)
    if _matmul(_transpose(operator), gram) != _matmul(gram, operator):
        raise AdmissibilityError("matrix must be symmetric with respect to the supplied metric")

    def pairing(left: Vector, right: Vector) -> Fraction:
        return _dot(left, _matvec(gram, right))

    return cyclic_reduce(
        lambda vector: _matvec(operator, vector),
        preparation,
        dimension=dimension,
        budget=budget,
        inner_product=pairing,
        self_adjoint_certificate="verified_exact_matrix",
        time_horizon=time_horizon,
        tolerance=tolerance,
    )


def _main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Construct an exact rational observable-cyclic reduction."
    )
    parser.add_argument("input", type=Path, help="JSON request file")
    parser.add_argument(
        "--format",
        choices=("json", "summary"),
        default="json",
        help="machine certificate or compact human recurrence",
    )
    arguments = parser.parse_args(argv)
    try:
        payload = json.loads(arguments.input.read_text(encoding="utf-8"))
        result = reduce_symmetric_matrix(
            payload["matrix"],
            payload["preparation"],
            metric=payload.get("metric"),
            budget=payload.get("budget"),
            time_horizon=payload.get("time_horizon"),
            tolerance=payload.get("tolerance"),
        )
    except (AdmissibilityError, KeyError, json.JSONDecodeError, OSError) as error:
        print(json.dumps({"status": "Refused", "reason": str(error)}, indent=2))
        return 2
    if arguments.format == "summary":
        print(result.summary())
    else:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(_main())

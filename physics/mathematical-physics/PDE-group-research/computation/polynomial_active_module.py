"""Exact G19 polynomial active-module construction on one certified local chart."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import comb

import sympy as sp
from sympy.polys.domains import QQ_I
from sympy.polys.matrices import DomainMatrix

import exact_gaussian_matrix as gaussian
from exact_polynomial_matrix import ExactPolynomialError, horner_interval, term_count
from gaussian_reachable_module import (
    Apply,
    ReachableModuleBudget,
    ReachableModuleCost,
    ReachableModuleError,
    ReachableNode,
    construct_reachable_module,
)
from polynomial_active_module_input import PolynomialProblem


class PolynomialReductionError(ValueError):
    def __init__(self, kind: str, reason: str, details: dict[str, object] | None = None):
        super().__init__(reason)
        self.kind = kind
        self.details = details or {}


@dataclass(frozen=True)
class IntervalAttempt:
    box: tuple[tuple[Fraction, Fraction], ...]
    enclosure: tuple[Fraction, Fraction]


@dataclass(frozen=True)
class RankChart:
    pivot_rows: tuple[int, ...]
    pivot_transform: sp.ImmutableMatrix
    certified_box: tuple[tuple[Fraction, Fraction], ...]
    pivot_minor: sp.Expr
    norm_square: sp.Expr
    attempts: tuple[IntervalAttempt, ...]


@dataclass(frozen=True)
class RationalMatrix:
    numerator: sp.ImmutableMatrix
    denominator: sp.Expr


@dataclass(frozen=True)
class PolynomialReductionCost:
    reachability: ReachableModuleCost
    polynomial_differentiations: int
    polynomial_multiplications: int
    peak_polynomial_terms: int
    interval_evaluations: int
    product_rule_summands: int
    leakage_nonzero_coefficients: int


@dataclass(frozen=True)
class ReductionWitness:
    ambient_dimension: int
    active_dimension: int
    provenance: tuple[ReachableNode, ...]
    raw_frame: sp.ImmutableMatrix
    frame: sp.ImmutableMatrix
    gram: sp.ImmutableMatrix
    left_inverse: RationalMatrix
    projector: RationalMatrix
    reduced_coefficients: dict[tuple[int, ...], RationalMatrix]
    residual_coefficients: dict[tuple[int, ...], RationalMatrix]
    preparation_coordinates: RationalMatrix
    compressed_effect: sp.ImmutableMatrix
    rank_chart: RankChart
    leakage_is_zero: bool
    domain_contract: str
    cost: PolynomialReductionCost
    checks: dict[str, bool]


def _sympy_rational(value: Fraction) -> sp.Rational:
    return sp.Rational(value.numerator, value.denominator)


def _gaussian(value: sp.Expr) -> gaussian.Gaussian:
    real, imaginary = sp.expand(value).as_real_imag()
    if not (real.is_Rational and imaginary.is_Rational):
        raise PolynomialReductionError("NonGaussianBaseValue", "base evaluation left QQ(i)")
    return gaussian.Gaussian(
        Fraction(int(real.p), int(real.q)), Fraction(int(imaginary.p), int(imaginary.q))
    )


def _point_matrix(matrix: sp.MatrixBase, substitutions: dict[sp.Symbol, sp.Rational]):
    return tuple(
        tuple(_gaussian(matrix[row, column].subs(substitutions)) for column in range(matrix.cols))
        for row in range(matrix.rows)
    )


def _point_vector(matrix: sp.MatrixBase, substitutions: dict[sp.Symbol, sp.Rational]):
    return tuple(_gaussian(matrix[row, 0].subs(substitutions)) for row in range(matrix.rows))


def _expanded(matrix: sp.MatrixBase) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(matrix.applyfunc(sp.expand))


def _matrix_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.cancel(entry) == 0 for entry in matrix)


def _check_terms(
    matrix: sp.MatrixBase,
    problem: PolynomialProblem,
    peak: int,
) -> int:
    current = term_count(matrix, problem.coordinates)
    peak = max(peak, current)
    if current > problem.budget.maximum_polynomial_terms:
        raise PolynomialReductionError(
            "PolynomialTermBudgetExceeded",
            "an intermediate canonical polynomial matrix exceeds the term budget",
            {"observed_terms": current, "maximum_terms": problem.budget.maximum_polynomial_terms},
        )
    return peak


def _certify_chart(
    frame: sp.ImmutableMatrix,
    pivot_rows: tuple[int, ...],
    problem: PolynomialProblem,
    transform: sp.ImmutableMatrix,
) -> RankChart:
    pivot = frame.extract(pivot_rows, range(frame.cols))
    minor = sp.expand(pivot.det())
    norm_square = sp.expand(sp.conjugate(minor) * minor)
    attempts: list[IntervalAttempt] = []
    for refinement in range(problem.budget.maximum_rank_refinements):
        scale = Fraction(1, 2**refinement)
        box = tuple(
            (
                base + (lower - base) * scale,
                base + (upper - base) * scale,
            )
            for base, (lower, upper) in zip(problem.base_point, problem.region, strict=True)
        )
        try:
            enclosure = horner_interval(norm_square, problem.coordinates, box)
        except ExactPolynomialError as error:
            raise PolynomialReductionError("IntervalDomainResidual", str(error)) from error
        attempts.append(IntervalAttempt(box, enclosure))
        if enclosure[0] > 0:
            return RankChart(pivot_rows, transform, box, minor, norm_square, tuple(attempts))
    raise PolynomialReductionError(
        "RankRegionUnresolved",
        "exact interval refinement did not certify a positive pivot minor",
        {"attempts": tuple(attempts)},
    )


def _derivative(matrix: sp.MatrixBase, alpha: tuple[int, ...], coordinates):
    result = matrix
    for coordinate, order in zip(coordinates, alpha, strict=True):
        if order:
            result = result.diff(coordinate, order)
    return _expanded(result)


def _multi_indices(alpha: tuple[int, ...]):
    return product(*(range(order + 1) for order in alpha))


def construct_reduction(problem: PolynomialProblem) -> ReductionWitness:
    coordinates = problem.coordinates
    substitutions = {
        coordinate: _sympy_rational(value)
        for coordinate, value in zip(coordinates, problem.base_point, strict=True)
    }
    point_coefficients = tuple(
        _point_matrix(term.coefficient, substitutions) for term in problem.operator_terms
    )
    try:
        module = construct_reachable_module(
            point_coefficients,
            _point_vector(problem.preparation, substitutions),
            ReachableModuleBudget(
                problem.budget.maximum_carrier_dimension,
                problem.budget.maximum_active_dimension,
            ),
        )
    except ReachableModuleError as error:
        raise PolynomialReductionError(error.kind, str(error)) from error

    columns: list[sp.ImmutableMatrix] = [problem.preparation]
    for node in module.provenance[1:]:
        assert isinstance(node, Apply)
        columns.append(
            _expanded(
                problem.operator_terms[node.generator_index].coefficient
                * columns[node.parent_index]
            )
        )
    raw_frame = _expanded(sp.Matrix.hstack(*columns))
    raw_point = raw_frame.subs(substitutions)
    pivot_rows = tuple(raw_point.T.rref()[1])
    if len(pivot_rows) != raw_frame.cols:
        raise PolynomialReductionError(
            "BaseRankResidual", "reachable basis lost rank during replay"
        )
    pivot_at_base = raw_point.extract(pivot_rows, range(raw_frame.cols))
    transform = sp.ImmutableMatrix(pivot_at_base.inv())
    frame = _expanded(raw_frame * transform)
    peak = _check_terms(frame, problem, term_count(raw_frame, coordinates))
    chart = _certify_chart(frame, pivot_rows, problem, transform)

    dagger = _expanded(frame.conjugate().T)
    gram = _expanded(dagger * frame)
    peak = _check_terms(gram, problem, peak)
    ring = QQ_I.poly_ring(*coordinates)
    gram_domain = DomainMatrix.from_Matrix(gram, fmt="sparse").convert_to(ring)
    inverse_domain, denominator_domain = gram_domain.inv_den()
    inverse_numerator = _expanded(inverse_domain.to_Matrix())
    denominator = sp.expand(ring.to_sympy(denominator_domain))
    analysis_numerator = _expanded(inverse_numerator * dagger)
    projector_numerator = _expanded(frame * analysis_numerator)
    peak = _check_terms(projector_numerator, problem, peak)

    coefficients = {term.derivative: term.coefficient for term in problem.operator_terms}
    betas = sorted({beta for alpha in coefficients for beta in _multi_indices(alpha)})
    reduced: dict[tuple[int, ...], RationalMatrix] = {}
    residual: dict[tuple[int, ...], RationalMatrix] = {}
    ambient_coefficients: dict[tuple[int, ...], sp.ImmutableMatrix] = {}
    derivative_cache: dict[tuple[int, ...], sp.ImmutableMatrix] = {}
    differentiations = multiplications = summands = 0
    identity = sp.eye(problem.preparation.rows)
    for beta in betas:
        ambient = sp.zeros(problem.preparation.rows, frame.cols)
        for alpha, coefficient in coefficients.items():
            if any(left < right for left, right in zip(alpha, beta, strict=True)):
                continue
            order = tuple(left - right for left, right in zip(alpha, beta, strict=True))
            if order not in derivative_cache:
                derivative_cache[order] = _derivative(frame, order, coordinates)
                differentiations += sum(order)
            factor = sp.prod(comb(left, right) for left, right in zip(alpha, beta, strict=True))
            ambient += factor * coefficient * derivative_cache[order]
            multiplications += 1
            summands += 1
        ambient = _expanded(ambient)
        ambient_coefficients[beta] = ambient
        peak = _check_terms(ambient, problem, peak)
        reduced_numerator = _expanded(analysis_numerator * ambient)
        residual_numerator = _expanded((denominator * identity - projector_numerator) * ambient)
        peak = _check_terms(reduced_numerator, problem, peak)
        peak = _check_terms(residual_numerator, problem, peak)
        reduced[beta] = RationalMatrix(reduced_numerator, denominator)
        residual[beta] = RationalMatrix(residual_numerator, denominator)

    preparation_numerator = _expanded(analysis_numerator * problem.preparation)
    compressed_effect = _expanded(frame.conjugate().T * problem.effect * frame)
    leakage_is_zero = all(_matrix_zero(value.numerator) for value in residual.values())
    checks = {
        "pivot_is_identity_at_base": frame.subs(substitutions).extract(
            pivot_rows, range(frame.cols)
        )
        == sp.eye(frame.cols),
        "left_inverse_recovers_frame": _matrix_zero(
            analysis_numerator * frame - denominator * sp.eye(frame.cols)
        ),
        "projector_is_idempotent": _matrix_zero(
            projector_numerator * projector_numerator - denominator * projector_numerator
        ),
        "preparation_recovers": _matrix_zero(
            frame * preparation_numerator - denominator * problem.preparation
        ),
        "residual_is_horizontal": all(
            _matrix_zero(analysis_numerator * value.numerator) for value in residual.values()
        ),
        "product_rule_reconstructs": all(
            _matrix_zero(
                denominator * ambient_coefficients[beta]
                - frame * reduced[beta].numerator
                - residual[beta].numerator
            )
            for beta in betas
        ),
    }
    # Compare columns without converting symbolic matrices back through a second admission path.
    checks["provenance_replays_base_basis"] = all(
        tuple(_gaussian(raw_point[row, column]) for row in range(raw_point.rows))
        == module.basis[column]
        for column in range(raw_point.cols)
    )
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise PolynomialReductionError(
            "ReductionIdentityResidual", f"construction fails at {failed}"
        )
    leakage_count = sum(not _matrix_zero(value.numerator) for value in residual.values())
    return ReductionWitness(
        problem.preparation.rows,
        frame.cols,
        module.provenance,
        raw_frame,
        frame,
        gram,
        RationalMatrix(analysis_numerator, denominator),
        RationalMatrix(projector_numerator, denominator),
        reduced,
        residual,
        RationalMatrix(preparation_numerator, denominator),
        compressed_effect,
        chart,
        leakage_is_zero,
        problem.domain_contract,
        PolynomialReductionCost(
            module.cost,
            differentiations,
            multiplications,
            peak,
            len(chart.attempts),
            summands,
            leakage_count,
        ),
        checks,
    )

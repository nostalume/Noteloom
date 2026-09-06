"""Exact finite construction for a metric carrier linked to a Hermitian carrier."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt

import exact_gaussian_matrix as gaussian
from adjoint_algebra import (
    Matrix as RealMatrix,
)
from adjoint_algebra import (
    add as real_add,
)
from adjoint_algebra import (
    flat as real_flat,
)
from adjoint_algebra import (
    inverse as real_inverse,
)
from adjoint_algebra import (
    multiply as real_multiply,
)
from adjoint_algebra import (
    scale as real_scale,
)
from adjoint_algebra import (
    transpose as real_transpose,
)
from adjoint_algebra import (
    zero as real_zero,
)
from linear_defect_compiler import (
    CandidateBracket,
    DefectBlock,
    DefectBudget,
    DefectCompilation,
    LinearMap,
    compile_defects,
)


@dataclass(frozen=True)
class CandidatePair:
    base: RealMatrix
    fiber: gaussian.ComplexMatrix


@dataclass(frozen=True)
class CoupledPlan:
    base_dimension: int
    fiber_dimension: int
    candidate_dimension: int
    residual_dimension: int
    bracket_upper_bound: int


@dataclass(frozen=True)
class CoupledConstruction:
    pairs: tuple[CandidatePair, ...]
    compilation: DefectCompilation


def plan(metric: RealMatrix, links: tuple[gaussian.ComplexMatrix, ...]) -> CoupledPlan:
    base_dimension = len(metric)
    fiber_dimension = len(links[0])
    candidates = base_dimension**2 + fiber_dimension**2
    residuals = base_dimension * (base_dimension + 1) // 2 + base_dimension * fiber_dimension**2
    return CoupledPlan(
        base_dimension,
        fiber_dimension,
        candidates,
        residuals,
        candidates**3 + 4 * candidates**2,
    )


def admission_refusal(value: CoupledPlan, budget: DefectBudget) -> tuple[str, str] | None:
    checks = (
        (value.candidate_dimension, budget.maximum_candidate_dimension, "CandidateBudgetExceeded"),
        (
            value.residual_dimension,
            budget.maximum_residual_coordinates,
            "ResidualBudgetExceeded",
        ),
        (value.bracket_upper_bound, budget.maximum_bracket_checks, "BracketBudgetExceeded"),
    )
    for required, available, kind in checks:
        if required > available:
            return kind, f"required {required} exceeds budget {available}"
    return None


def clifford_checks(
    metric: RealMatrix, links: tuple[gaussian.ComplexMatrix, ...]
) -> dict[str, bool]:
    unit = gaussian.identity(len(links[0]))
    return {
        f"anticommutator:{left},{right}": gaussian.add(
            gaussian.multiply(links[left], links[right]),
            gaussian.multiply(links[right], links[left]),
        )
        == gaussian.scale(unit, 2 * metric[left][right])
        for left in range(len(links))
        for right in range(left, len(links))
    }


def _base_units(dimension: int) -> tuple[tuple[str, RealMatrix], ...]:
    return tuple(
        (
            f"base:E{row}{column}",
            tuple(
                tuple(Fraction(i == row and j == column) for j in range(dimension))
                for i in range(dimension)
            ),
        )
        for row in range(dimension)
        for column in range(dimension)
    )


def _candidates(value: CoupledPlan) -> tuple[tuple[str, ...], tuple[CandidatePair, ...]]:
    base_zero = real_zero(value.base_dimension)
    fiber_zero = gaussian.zero(value.fiber_dimension)
    base = _base_units(value.base_dimension)
    fiber = gaussian.skew_hermitian_basis(value.fiber_dimension)
    labels = tuple(label for label, _ in (*base, *fiber))
    pairs = tuple(CandidatePair(item, fiber_zero) for _, item in base) + tuple(
        CandidatePair(base_zero, item) for _, item in fiber
    )
    return labels, pairs


def _metric_block(metric: RealMatrix, pairs: tuple[CandidatePair, ...]) -> DefectBlock:
    dimension = len(metric)
    labels = tuple(
        f"metric:{row},{column}" for row in range(dimension) for column in range(row, dimension)
    )
    columns = []
    for pair in pairs:
        residual = real_add(
            real_multiply(real_transpose(pair.base), metric),
            real_multiply(metric, pair.base),
        )
        columns.append(
            tuple(
                residual[row][column]
                for row in range(dimension)
                for column in range(row, dimension)
            )
        )
    return DefectBlock("base-metric-preservation", labels, tuple(columns))


def _hermitian_labels(prefix: str, dimension: int) -> tuple[str, ...]:
    labels = [f"{prefix}:diag:{index}" for index in range(dimension)]
    for row in range(dimension):
        for column in range(row + 1, dimension):
            labels.extend((f"{prefix}:real:{row},{column}", f"{prefix}:imag:{row},{column}"))
    return tuple(labels)


def _covariance_block(
    links: tuple[gaussian.ComplexMatrix, ...], pairs: tuple[CandidatePair, ...]
) -> DefectBlock:
    labels = tuple(
        label
        for index in range(len(links))
        for label in _hermitian_labels(f"link:{index}", len(links[0]))
    )
    columns: list[tuple[Fraction, ...]] = []
    for pair in pairs:
        coordinates: list[Fraction] = []
        for index, link in enumerate(links):
            induced = gaussian.linear_combination(
                tuple(pair.base[row][index] for row in range(len(links))), links
            )
            residual = gaussian.add(
                gaussian.bracket(pair.fiber, link), gaussian.scale(induced, Fraction(-1))
            )
            coordinates.extend(gaussian.hermitian_coordinates(residual))
        columns.append(tuple(coordinates))
    return DefectBlock("link-commutator-covariance", labels, tuple(columns))


def _real_bracket(left: RealMatrix, right: RealMatrix) -> RealMatrix:
    return real_add(
        real_multiply(left, right), real_scale(real_multiply(right, left), Fraction(-1))
    )


def _candidate_bracket(pairs: tuple[CandidatePair, ...]) -> CandidateBracket:
    return CandidateBracket(
        "componentwise-commutator",
        tuple(
            tuple(
                (
                    *real_flat(_real_bracket(left.base, right.base)),
                    *gaussian.skew_hermitian_coordinates(gaussian.bracket(left.fiber, right.fiber)),
                )
                for right in pairs
            )
            for left in pairs
        ),
    )


def construct(
    metric: RealMatrix,
    links: tuple[gaussian.ComplexMatrix, ...],
    value: CoupledPlan,
    budget: DefectBudget,
) -> CoupledConstruction:
    labels, pairs = _candidates(value)
    compilation = compile_defects(
        candidate_labels=labels,
        blocks=(_metric_block(metric, pairs), _covariance_block(links, pairs)),
        visible_action=LinearMap(
            "base-visible-action",
            tuple(
                f"base:{row},{column}"
                for row in range(len(metric))
                for column in range(len(metric))
            ),
            tuple(real_flat(pair.base) for pair in pairs),
        ),
        bracket=_candidate_bracket(pairs),
        budget=budget,
    )
    return CoupledConstruction(pairs, compilation)


def combine_pair(
    coefficients: tuple[Fraction, ...], pairs: tuple[CandidatePair, ...]
) -> CandidatePair:
    base = real_zero(len(pairs[0].base))
    fiber = gaussian.zero(len(pairs[0].fiber))
    for coefficient, pair in zip(coefficients, pairs, strict=True):
        base = real_add(base, real_scale(pair.base, coefficient))
        fiber = gaussian.add(fiber, gaussian.scale(pair.fiber, coefficient))
    return CandidatePair(base, fiber)


def serialize_pair(pair: CandidatePair) -> dict[str, object]:
    return {
        "base": [[gaussian.rational_text(entry) for entry in row] for row in pair.base],
        "fiber": gaussian.serialize(pair.fiber),
    }


def _square_root(value: Fraction) -> Fraction:
    if value <= 0:
        raise ValueError("the observable covector must have positive norm")
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator**2 != value.numerator or denominator**2 != value.denominator:
        raise ValueError("the exact covector norm is not rational")
    return Fraction(numerator, denominator)


def symbol_projectors(
    metric: RealMatrix,
    links: tuple[gaussian.ComplexMatrix, ...],
    covector: tuple[Fraction, ...],
) -> dict[str, object]:
    inverse_metric = real_inverse(metric)
    raised = tuple(
        sum(
            (inverse_metric[row][column] * covector[column] for column in range(len(metric))),
            Fraction(0),
        )
        for row in range(len(metric))
    )
    norm_squared = sum(
        (covector[index] * raised[index] for index in range(len(metric))), Fraction(0)
    )
    norm = _square_root(norm_squared)
    symbol = gaussian.linear_combination(covector, links)
    unit = gaussian.identity(len(links[0]))
    normalized = gaussian.scale(symbol, Fraction(1, 1) / norm)
    plus = gaussian.scale(gaussian.add(unit, normalized), Fraction(1, 2))
    minus = gaussian.scale(
        gaussian.add(unit, gaussian.scale(normalized, Fraction(-1))), Fraction(1, 2)
    )
    checks = {
        "clifford_square": gaussian.multiply(symbol, symbol) == gaussian.scale(unit, norm_squared),
        "plus_idempotent": gaussian.multiply(plus, plus) == plus,
        "minus_idempotent": gaussian.multiply(minus, minus) == minus,
        "orthogonal": gaussian.multiply(plus, minus) == gaussian.zero(len(unit)),
        "synthesis": gaussian.add(plus, minus) == unit,
        "plus_symbol_intertwining": gaussian.multiply(symbol, plus) == gaussian.scale(plus, norm),
        "minus_symbol_intertwining": gaussian.multiply(symbol, minus)
        == gaussian.scale(minus, -norm),
    }
    return {
        "kind": "exact-linked-symbol-projectors",
        "covector": [gaussian.rational_text(item) for item in covector],
        "norm": gaussian.rational_text(norm),
        "projectors": {"plus": gaussian.serialize(plus), "minus": gaussian.serialize(minus)},
        "checks": checks,
    }

"""Exact ordered-coefficient covariance lift for constructed carrier actions."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

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
    multiply as real_multiply,
)
from adjoint_algebra import (
    transpose as real_transpose,
)
from coupled_covariance_core import CandidatePair
from linear_defect_compiler import (
    CandidateBracket,
    DefectBlock,
    DefectBudget,
    DefectCompilation,
    LinearMap,
    compile_defects,
)


@dataclass(frozen=True)
class FullOperatorPlan:
    candidate_dimension: int
    residual_dimension: int
    bracket_upper_bound: int


def plan(
    pairs: tuple[CandidatePair, ...],
    curvature: RealMatrix,
    first_order: tuple[gaussian.ComplexMatrix, ...],
    zero_order: gaussian.ComplexMatrix,
) -> FullOperatorPlan:
    base_dimension = len(curvature)
    fiber_dimension = len(zero_order)
    candidates = len(pairs)
    residuals = (
        base_dimension * (base_dimension - 1) // 2
        + base_dimension * fiber_dimension**2
        + fiber_dimension**2
    )
    return FullOperatorPlan(candidates, residuals, candidates**3 + 4 * candidates**2)


def admission_refusal(value: FullOperatorPlan, budget: DefectBudget) -> tuple[str, str] | None:
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


def _curvature_block(curvature: RealMatrix, pairs: tuple[CandidatePair, ...]) -> DefectBlock:
    dimension = len(curvature)
    labels = tuple(
        f"curvature:{row},{column}"
        for row in range(dimension)
        for column in range(row + 1, dimension)
    )
    columns = []
    for pair in pairs:
        residual = real_add(
            real_multiply(real_transpose(pair.base), curvature),
            real_multiply(curvature, pair.base),
        )
        columns.append(
            tuple(
                residual[row][column]
                for row in range(dimension)
                for column in range(row + 1, dimension)
            )
        )
    return DefectBlock("curvature-covariance", labels, tuple(columns))


def _hermitian_labels(prefix: str, dimension: int) -> tuple[str, ...]:
    labels = [f"{prefix}:diag:{index}" for index in range(dimension)]
    for row in range(dimension):
        for column in range(row + 1, dimension):
            labels.extend((f"{prefix}:real:{row},{column}", f"{prefix}:imag:{row},{column}"))
    return tuple(labels)


def _first_order_block(
    first_order: tuple[gaussian.ComplexMatrix, ...], pairs: tuple[CandidatePair, ...]
) -> DefectBlock:
    labels = tuple(
        label
        for index in range(len(first_order))
        for label in _hermitian_labels(f"first:{index}", len(first_order[0]))
    )
    columns = []
    for pair in pairs:
        coordinates: list[Fraction] = []
        for index, coefficient in enumerate(first_order):
            induced = gaussian.linear_combination(
                tuple(pair.base[row][index] for row in range(len(first_order))), first_order
            )
            residual = gaussian.add(
                gaussian.bracket(pair.fiber, coefficient),
                gaussian.scale(induced, Fraction(-1)),
            )
            coordinates.extend(gaussian.hermitian_coordinates(residual))
        columns.append(tuple(coordinates))
    return DefectBlock("first-order-covariance", labels, tuple(columns))


def _zero_order_block(
    zero_order: gaussian.ComplexMatrix, pairs: tuple[CandidatePair, ...]
) -> DefectBlock:
    labels = _hermitian_labels("zero", len(zero_order))
    return DefectBlock(
        "zeroth-order-covariance",
        labels,
        tuple(
            gaussian.hermitian_coordinates(gaussian.bracket(pair.fiber, zero_order))
            for pair in pairs
        ),
    )


def construct(
    pairs: tuple[CandidatePair, ...],
    quotient_bracket_table: tuple[tuple[tuple[Fraction, ...], ...], ...],
    curvature: RealMatrix,
    first_order: tuple[gaussian.ComplexMatrix, ...],
    zero_order: gaussian.ComplexMatrix,
    budget: DefectBudget,
) -> DefectCompilation:
    labels = tuple(f"constructed-action:{index}" for index in range(len(pairs)))
    return compile_defects(
        candidate_labels=labels,
        blocks=(
            _curvature_block(curvature, pairs),
            _first_order_block(first_order, pairs),
            _zero_order_block(zero_order, pairs),
        ),
        visible_action=LinearMap(
            "full-operator-base-action",
            tuple(
                f"base:{row},{column}"
                for row in range(len(curvature))
                for column in range(len(curvature))
            ),
            tuple(real_flat(pair.base) for pair in pairs),
        ),
        bracket=CandidateBracket("inherited-quotient-commutator", quotient_bracket_table),
        budget=budget,
    )

"""Construct irreducible carriers and reduce quadratic differential symbols."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import exact_gaussian_matrix as gaussian
from exact_gaussian_linear import Vector, coordinates, determinant, rank
from exact_rational_linear import coordinates as rational_coordinates
from represented_star_algebra import IsotypicBlock, RepresentedStarAlgebra, StarGenerator
from semisimple_coefficient_algebra import AlgebraBudget, AlgebraError, Generator, construct


class RealizationError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


@dataclass(frozen=True)
class RealizationBudget:
    maximum_splitter_candidates: int
    maximum_factor_candidates: int


@dataclass(frozen=True)
class IrreducibleModel:
    source: RepresentedStarAlgebra
    block: IsotypicBlock
    multiplicity_projectors: tuple[gaussian.ComplexMatrix, ...]
    selected_projector: gaussian.ComplexMatrix
    embedding_columns: tuple[Vector, ...]
    reduced_generators: tuple[StarGenerator, ...]
    splitter_candidates_checked: int
    checks: dict[str, bool]

    @property
    def carrier_dimension(self) -> int:
        return self.block.irreducible_dimension

    @property
    def multiplicity(self) -> int:
        return self.block.multiplicity


@dataclass(frozen=True)
class QuadraticSymbol:
    second_order: gaussian.ComplexMatrix
    first_order: gaussian.ComplexMatrix
    zeroth_order: gaussian.ComplexMatrix


@dataclass(frozen=True)
class SymbolCost:
    construction_proxy: int
    baseline_per_query: int
    reduced_per_query: int
    recovery_per_query: int
    break_even_queries: int


@dataclass(frozen=True)
class QuadraticSymbolWitness:
    momentum: Fraction
    full_value: gaussian.ComplexMatrix
    reduced_value: gaussian.ComplexMatrix
    full_determinant: gaussian.Gaussian
    reduced_determinant: gaussian.Gaussian
    cost: SymbolCost
    checks: dict[str, bool]


def _compress(
    projector: gaussian.ComplexMatrix, value: gaussian.ComplexMatrix
) -> gaussian.ComplexMatrix:
    return gaussian.multiply(gaussian.multiply(projector, value), projector)


def _matrix_sum(
    values: tuple[gaussian.ComplexMatrix, ...], dimension: int
) -> gaussian.ComplexMatrix:
    result = gaussian.zero(dimension)
    for value in values:
        result = gaussian.add(result, value)
    return result


def _columns(value: gaussian.ComplexMatrix) -> tuple[Vector, ...]:
    return tuple(
        tuple(value[row][column] for row in range(len(value))) for column in range(len(value))
    )


def _independent_columns(projector: gaussian.ComplexMatrix, count: int) -> tuple[Vector, ...]:
    selected: list[Vector] = []
    for column in _columns(projector):
        if rank((*selected, column)) > len(selected):
            selected.append(column)
        if len(selected) == count:
            return tuple(selected)
    raise RealizationError("EmbeddingRankResidual", "primitive projector has insufficient rank")


def _matvec(value: gaussian.ComplexMatrix, vector: Vector) -> Vector:
    return tuple(
        sum((value[row][column] * vector[column] for column in range(len(vector))), gaussian.ZERO)
        for row in range(len(value))
    )


def _reduce_matrix(
    model: IrreducibleModel, value: gaussian.ComplexMatrix
) -> gaussian.ComplexMatrix:
    columns: list[Vector] = []
    for vector in model.embedding_columns:
        result = coordinates(_matvec(value, vector), model.embedding_columns)
        if result is None:
            raise RealizationError(
                "CoefficientLeavesIrreducibleCarrier",
                "coefficient does not preserve the constructed primitive slice",
            )
        columns.append(result)
    dimension = model.carrier_dimension
    return tuple(
        tuple(columns[column][row] for column in range(dimension)) for row in range(dimension)
    )


def _require_algebra_coefficient(model: IrreducibleModel, value: gaussian.ComplexMatrix) -> None:
    if (
        not gaussian.is_hermitian(value)
        or rational_coordinates(
            gaussian.vector_coordinates(value),
            tuple(
                gaussian.vector_coordinates(basis) for basis in model.source.algebra_hermitian_basis
            ),
        )
        is None
    ):
        raise RealizationError(
            "CoefficientOutsideRepresentedAlgebra",
            "quadratic-symbol coefficient is outside the represented Hermitian algebra",
        )


def _split_multiplicity(
    algebra: RepresentedStarAlgebra,
    block: IsotypicBlock,
    budget: RealizationBudget,
) -> tuple[tuple[gaussian.ComplexMatrix, ...], int]:
    if block.multiplicity == 1:
        return (block.projector,), 0
    candidates = algebra.commutant_hermitian_basis[: budget.maximum_splitter_candidates]
    for checked, candidate in enumerate(candidates, start=1):
        splitter = _compress(block.projector, candidate)
        try:
            split = construct(
                (Generator("central", block.projector), Generator("splitter", splitter)),
                AlgebraBudget(
                    len(block.projector),
                    2,
                    budget.maximum_factor_candidates,
                ),
            )
        except AlgebraError:
            continue
        projectors = tuple(sector.projector for sector in split.sectors if sector.character[0] == 1)
        if len(projectors) == block.multiplicity and all(
            sector.multiplicity == block.irreducible_dimension
            for sector in split.sectors
            if sector.character[0] == 1
        ):
            return projectors, checked
    raise RealizationError(
        "MultiplicitySplitterUnavailable",
        "no rationally split primitive commutant projector was found within budget",
    )


def construct_irreducible_model(
    algebra: RepresentedStarAlgebra,
    block_index: int,
    budget: RealizationBudget,
) -> IrreducibleModel:
    if budget.maximum_splitter_candidates < 0 or budget.maximum_factor_candidates < 0:
        raise RealizationError("InvalidRealizationBudget", "realization budget is invalid")
    if block_index < 0 or block_index >= len(algebra.blocks):
        raise RealizationError("InvalidIsotypicBlock", "block index is outside the decomposition")
    block = algebra.blocks[block_index]
    projectors, checked = _split_multiplicity(algebra, block, budget)
    selected = projectors[0]
    embedding = _independent_columns(selected, block.irreducible_dimension)
    provisional = IrreducibleModel(
        algebra,
        block,
        projectors,
        selected,
        embedding,
        (),
        checked,
        {},
    )
    reduced = tuple(
        StarGenerator(generator.label, _reduce_matrix(provisional, generator.value))
        for generator in algebra.generators
    )
    zero = gaussian.zero(len(selected))
    checks = {
        "multiplicity_projectors_resolve_block": _matrix_sum(projectors, len(selected))
        == block.projector,
        "primitive_projector_commutes_with_algebra": all(
            gaussian.bracket(selected, generator.value) == zero for generator in algebra.generators
        ),
        "embedding_has_irreducible_rank": rank(embedding) == block.irreducible_dimension,
        "generator_intertwiners_hold": all(
            _matvec(generator.value, vector)
            == tuple(
                sum(
                    (
                        embedding[column][row] * reduced_generator.value[column][index]
                        for column in range(block.irreducible_dimension)
                    ),
                    gaussian.ZERO,
                )
                for row in range(len(selected))
            )
            for generator, reduced_generator in zip(algebra.generators, reduced, strict=True)
            for index, vector in enumerate(embedding)
        ),
    }
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise RealizationError("IrreducibleRealizationResidual", f"construction fails at {failed}")
    return IrreducibleModel(
        algebra, block, projectors, selected, embedding, reduced, checked, checks
    )


def _quadratic_value(symbol: QuadraticSymbol, momentum: Fraction) -> gaussian.ComplexMatrix:
    return gaussian.add(
        gaussian.add(
            gaussian.scale(symbol.second_order, momentum * momentum),
            gaussian.scale(symbol.first_order, momentum),
        ),
        symbol.zeroth_order,
    )


def _gaussian_power(value: gaussian.Gaussian, exponent: int) -> gaussian.Gaussian:
    result = gaussian.ONE
    for _ in range(exponent):
        result = result * value
    return result


def evaluate_quadratic_symbol(
    model: IrreducibleModel,
    symbol: QuadraticSymbol,
    momentum: Fraction,
) -> QuadraticSymbolWitness:
    if model.block.carrier_dimension != len(model.source.generators[0].value):
        raise RealizationError(
            "SymbolRequiresSingleIsotypicBlock",
            "determinant recovery currently requires one full isotypic carrier",
        )
    coefficients = (symbol.second_order, symbol.first_order, symbol.zeroth_order)
    for coefficient in coefficients:
        _require_algebra_coefficient(model, coefficient)
    reduced_coefficients = tuple(_reduce_matrix(model, value) for value in coefficients)
    reduced_symbol = QuadraticSymbol(*reduced_coefficients)
    full_value = _quadratic_value(symbol, momentum)
    reduced_value = _quadratic_value(reduced_symbol, momentum)
    full_determinant = determinant(full_value)
    reduced_determinant = determinant(reduced_value)
    expected = _gaussian_power(reduced_determinant, model.multiplicity)
    if full_determinant != expected:
        raise RealizationError(
            "MultiplicityDeterminantResidual",
            "full symbol determinant is not the multiplicity power of the reduced determinant",
        )
    full_dimension = model.block.carrier_dimension
    reduced_dimension = model.carrier_dimension
    construction = (
        model.source.commutator_system_entries
        + model.splitter_candidates_checked * full_dimension**4
        + full_dimension * reduced_dimension**2
    )
    baseline = full_dimension**3
    reduced = reduced_dimension**3
    recovery = max(1, model.multiplicity.bit_length())
    saving = baseline - reduced - recovery
    break_even = (construction + saving - 1) // saving if saving > 0 else 0
    checks = {
        "carrier_dimension_reduced": reduced_dimension < full_dimension,
        "determinant_reconstructed_with_multiplicity": full_determinant == expected,
        "per_query_proxy_reduced": saving > 0,
    }
    return QuadraticSymbolWitness(
        Fraction(momentum),
        full_value,
        reduced_value,
        full_determinant,
        reduced_determinant,
        SymbolCost(construction, baseline, reduced, recovery, break_even),
        checks,
    )

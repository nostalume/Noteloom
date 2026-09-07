"""Exact isotypic decomposition of finite represented complex star-algebras."""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt

import exact_gaussian_matrix as gaussian
from exact_rational_linear import independent_basis, nullspace, rank
from semisimple_coefficient_algebra import (
    AlgebraBudget,
    AlgebraError,
    Generator,
)
from semisimple_coefficient_algebra import construct as construct_center


class StarAlgebraError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


@dataclass(frozen=True)
class StarGenerator:
    label: str
    value: gaussian.ComplexMatrix


@dataclass(frozen=True)
class StarAlgebraBudget:
    maximum_carrier_dimension: int
    maximum_generators: int
    maximum_hermitian_dimension: int
    maximum_factor_candidates: int


@dataclass(frozen=True)
class IsotypicBlock:
    projector: gaussian.ComplexMatrix
    carrier_dimension: int
    algebra_dimension: int
    commutant_dimension: int
    irreducible_dimension: int
    multiplicity: int


@dataclass(frozen=True)
class RepresentedStarAlgebra:
    generators: tuple[StarGenerator, ...]
    algebra_hermitian_basis: tuple[gaussian.ComplexMatrix, ...]
    commutant_hermitian_basis: tuple[gaussian.ComplexMatrix, ...]
    center_hermitian_basis: tuple[gaussian.ComplexMatrix, ...]
    blocks: tuple[IsotypicBlock, ...]
    factor_candidate_checks: int
    commutator_system_entries: int
    checks: dict[str, bool]

    @property
    def algebra_dimension(self) -> int:
        return len(self.algebra_hermitian_basis)

    @property
    def commutant_dimension(self) -> int:
        return len(self.commutant_hermitian_basis)

    @property
    def center_dimension(self) -> int:
        return len(self.center_hermitian_basis)


@dataclass(frozen=True)
class CentralCoefficientDecomposition:
    block_values: tuple[gaussian.ComplexMatrix, ...]
    direct_value: gaussian.ComplexMatrix
    projector_synthesis: gaussian.ComplexMatrix


def _commutant(
    ambient: tuple[gaussian.ComplexMatrix, ...],
    constraints: tuple[gaussian.ComplexMatrix, ...],
) -> tuple[gaussian.ComplexMatrix, ...]:
    residual_columns = [
        tuple(
            coordinate
            for constraint in constraints
            for coordinate in gaussian.vector_coordinates(gaussian.bracket(candidate, constraint))
        )
        for candidate in ambient
    ]
    rows = [
        [column[index] for column in residual_columns] for index in range(len(residual_columns[0]))
    ]
    return tuple(
        gaussian.linear_combination(coefficients, ambient)
        for coefficients in nullspace(rows, len(ambient))
    )


def _intersection(
    left: tuple[gaussian.ComplexMatrix, ...],
    right: tuple[gaussian.ComplexMatrix, ...],
) -> tuple[gaussian.ComplexMatrix, ...]:
    columns = [gaussian.vector_coordinates(value) for value in left] + [
        tuple(-entry for entry in gaussian.vector_coordinates(value)) for value in right
    ]
    rows = [[column[index] for column in columns] for index in range(len(columns[0]))]
    candidates = tuple(
        gaussian.linear_combination(coefficients[: len(left)], left)
        for coefficients in nullspace(rows, len(columns))
    )
    independent_vectors = independent_basis(
        tuple(gaussian.vector_coordinates(value) for value in candidates)
    )
    by_vector = {gaussian.vector_coordinates(value): value for value in candidates}
    return tuple(by_vector[vector] for vector in independent_vectors)


def _matrix_sum(
    values: tuple[gaussian.ComplexMatrix, ...], dimension: int
) -> gaussian.ComplexMatrix:
    result = gaussian.zero(dimension)
    for value in values:
        result = gaussian.add(result, value)
    return result


def _projector_rank(projector: gaussian.ComplexMatrix) -> int:
    trace = sum((projector[index][index] for index in range(len(projector))), gaussian.ZERO)
    if trace.imaginary or trace.real.denominator != 1 or trace.real <= 0:
        raise StarAlgebraError("ProjectorRankResidual", "central projector rank is not integral")
    return int(trace.real)


def _compressed_dimension(
    space: tuple[gaussian.ComplexMatrix, ...], projector: gaussian.ComplexMatrix
) -> int:
    compressed = tuple(
        gaussian.vector_coordinates(
            gaussian.multiply(gaussian.multiply(projector, value), projector)
        )
        for value in space
    )
    return rank(compressed)


def _square_root(value: int, kind: str) -> int:
    root = isqrt(value)
    if root * root != value:
        raise StarAlgebraError(
            "DoubleCentralizerDimensionObstruction",
            f"{kind} block dimension {value} is not a square",
        )
    return root


def _validate(generators: tuple[StarGenerator, ...], budget: StarAlgebraBudget) -> tuple[int, int]:
    if not generators or any(not generator.label for generator in generators):
        raise StarAlgebraError("InvalidStarGenerators", "generator labels must be nonempty")
    if len({generator.label for generator in generators}) != len(generators):
        raise StarAlgebraError("InvalidStarGenerators", "generator labels must be unique")
    if (
        budget.maximum_carrier_dimension <= 0
        or budget.maximum_generators <= 0
        or budget.maximum_hermitian_dimension <= 0
        or budget.maximum_factor_candidates < 0
    ):
        raise StarAlgebraError("InvalidStarAlgebraBudget", "star-algebra budget is invalid")
    dimension = len(generators[0].value)
    if any(
        len(generator.value) != dimension or any(len(row) != dimension for row in generator.value)
        for generator in generators
    ):
        raise StarAlgebraError("StarGeneratorDimensionMismatch", "generator dimensions differ")
    hermitian_dimension = dimension * dimension
    if (
        dimension > budget.maximum_carrier_dimension
        or len(generators) > budget.maximum_generators
        or hermitian_dimension > budget.maximum_hermitian_dimension
    ):
        raise StarAlgebraError(
            "StarAlgebraBudgetExceeded",
            "carrier, generator, or Hermitian ambient-space budget exceeded",
        )
    if any(not gaussian.is_hermitian(generator.value) for generator in generators):
        raise StarAlgebraError(
            "NonStarClosedGenerators",
            "Hermitian generators are required to construct a unital star-algebra",
        )
    return dimension, hermitian_dimension


def construct(
    generators: tuple[StarGenerator, ...], budget: StarAlgebraBudget
) -> RepresentedStarAlgebra:
    dimension, hermitian_dimension = _validate(generators, budget)
    ambient = gaussian.hermitian_basis(dimension)
    commutant = _commutant(ambient, tuple(generator.value for generator in generators))
    algebra = _commutant(ambient, commutant)
    center = _intersection(algebra, commutant)
    try:
        central_algebra = construct_center(
            tuple(Generator(f"Z{index}", value) for index, value in enumerate(center)),
            AlgebraBudget(
                dimension,
                len(center),
                budget.maximum_factor_candidates,
            ),
        )
    except AlgebraError as error:
        raise StarAlgebraError(error.kind, str(error)) from error

    blocks: list[IsotypicBlock] = []
    for sector in central_algebra.sectors:
        carrier_dimension = _projector_rank(sector.projector)
        algebra_dimension = _compressed_dimension(algebra, sector.projector)
        commutant_dimension = _compressed_dimension(commutant, sector.projector)
        irreducible_dimension = _square_root(algebra_dimension, "algebra")
        multiplicity = _square_root(commutant_dimension, "commutant")
        if carrier_dimension != irreducible_dimension * multiplicity:
            raise StarAlgebraError(
                "DoubleCentralizerDimensionObstruction",
                "central block rank does not equal irreducible dimension times multiplicity",
            )
        blocks.append(
            IsotypicBlock(
                sector.projector,
                carrier_dimension,
                algebra_dimension,
                commutant_dimension,
                irreducible_dimension,
                multiplicity,
            )
        )

    projectors = tuple(block.projector for block in blocks)
    zero = gaussian.zero(dimension)
    checks = {
        "commutant_commutes_with_generators": all(
            gaussian.bracket(value, generator.value) == zero
            for value in commutant
            for generator in generators
        ),
        "algebra_commutes_with_commutant": all(
            gaussian.bracket(left, right) == zero for left in algebra for right in commutant
        ),
        "central_basis_is_mutual": all(
            gaussian.bracket(center_value, value) == zero
            for center_value in center
            for value in (*algebra, *commutant)
        ),
        "central_projectors_resolve_identity": _matrix_sum(projectors, dimension)
        == gaussian.identity(dimension),
        "central_projectors_commute_with_generators": all(
            gaussian.bracket(projector, generator.value) == zero
            for projector in projectors
            for generator in generators
        ),
        "generators_reconstruct_from_blocks": all(
            _matrix_sum(
                tuple(
                    gaussian.multiply(gaussian.multiply(projector, generator.value), projector)
                    for projector in projectors
                ),
                dimension,
            )
            == generator.value
            for generator in generators
        ),
        "global_block_dimensions_reconstruct": (
            sum(block.algebra_dimension for block in blocks) == len(algebra)
            and sum(block.commutant_dimension for block in blocks) == len(commutant)
            and sum(block.carrier_dimension for block in blocks) == dimension
        ),
        "double_centralizer_dimensions_hold": all(
            block.algebra_dimension == block.irreducible_dimension**2
            and block.commutant_dimension == block.multiplicity**2
            and block.carrier_dimension == block.irreducible_dimension * block.multiplicity
            for block in blocks
        ),
    }
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise StarAlgebraError("StarAlgebraResidual", f"construction fails at {failed}")
    system_entries = (
        hermitian_dimension * 2 * dimension * dimension * (len(generators) + len(commutant))
    )
    return RepresentedStarAlgebra(
        generators,
        algebra,
        commutant,
        center,
        tuple(blocks),
        central_algebra.factor_candidate_checks,
        system_entries,
        checks,
    )


def decompose_coefficient(
    algebra: RepresentedStarAlgebra, value: gaussian.ComplexMatrix
) -> CentralCoefficientDecomposition:
    dimension = len(algebra.generators[0].value)
    if len(value) != dimension or any(len(row) != dimension for row in value):
        raise StarAlgebraError("CoefficientDimensionMismatch", "coefficient dimension differs")
    block_values = tuple(
        gaussian.multiply(gaussian.multiply(block.projector, value), block.projector)
        for block in algebra.blocks
    )
    synthesis = _matrix_sum(block_values, dimension)
    if synthesis != value:
        raise StarAlgebraError(
            "CoefficientMixesIsotypicBlocks",
            "coefficient has nonzero off-diagonal central blocks",
        )
    return CentralCoefficientDecomposition(block_values, value, synthesis)

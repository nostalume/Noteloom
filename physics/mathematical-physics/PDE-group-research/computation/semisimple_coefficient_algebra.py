"""Exact split commutative Hermitian coefficient algebras without eigenvectors."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import exact_gaussian_matrix as gaussian
from exact_rational_linear import coordinates
from rational_polynomial import FactorizationError, split_linear_roots


class AlgebraError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


@dataclass(frozen=True)
class Generator:
    label: str
    value: gaussian.ComplexMatrix


@dataclass(frozen=True)
class AlgebraBudget:
    maximum_carrier_dimension: int
    maximum_generators: int
    maximum_factor_candidates: int


@dataclass(frozen=True)
class Sector:
    character: tuple[Fraction, ...]
    projector: gaussian.ComplexMatrix
    multiplicity: int


@dataclass(frozen=True)
class RefinementStep:
    generator: str
    roots: tuple[Fraction, ...]
    input_sectors: int
    output_sectors: int


@dataclass(frozen=True)
class FiniteCoefficientAlgebra:
    generators: tuple[Generator, ...]
    minimal_polynomials: tuple[tuple[Fraction, ...], ...]
    sectors: tuple[Sector, ...]
    refinement: tuple[RefinementStep, ...]
    factor_candidate_checks: int
    checks: dict[str, bool]

    @property
    def dimension(self) -> int:
        return len(self.sectors)

    @property
    def separates_carrier(self) -> bool:
        return all(sector.multiplicity == 1 for sector in self.sectors)


@dataclass(frozen=True)
class PolynomialTerm:
    coefficient: Fraction
    powers: tuple[int, ...]


@dataclass(frozen=True)
class PolynomialDecomposition:
    sector_values: tuple[Fraction, ...]
    direct_value: gaussian.ComplexMatrix
    projector_synthesis: gaussian.ComplexMatrix


def _minimal_polynomial(value: gaussian.ComplexMatrix) -> tuple[Fraction, ...]:
    unit = gaussian.identity(len(value))
    powers = [unit]
    power = unit
    for _degree in range(1, len(value) + 1):
        power = gaussian.multiply(power, value)
        power_coordinates = coordinates(
            gaussian.vector_coordinates(power),
            tuple(gaussian.vector_coordinates(basis_value) for basis_value in powers),
        )
        if power_coordinates is not None:
            return (*(-entry for entry in power_coordinates), Fraction(1))
        powers.append(power)
    raise AlgebraError(
        "MinimalPolynomialResidual", "Cayley-Hamilton dependence was not constructed"
    )


def _root_projector(
    value: gaussian.ComplexMatrix, root: Fraction, roots: tuple[Fraction, ...]
) -> gaussian.ComplexMatrix:
    unit = gaussian.identity(len(value))
    result = unit
    for other in roots:
        if other == root:
            continue
        factor = gaussian.add(value, gaussian.scale(unit, -other))
        result = gaussian.scale(gaussian.multiply(result, factor), Fraction(1, 1) / (root - other))
    return result


def _trace_rank(projector: gaussian.ComplexMatrix) -> int:
    trace = sum((projector[index][index] for index in range(len(projector))), gaussian.ZERO)
    if trace.imaginary or trace.real.denominator != 1 or trace.real <= 0:
        raise AlgebraError("ProjectorRankResidual", "projector trace is not a positive integer")
    return int(trace.real)


def _matrix_polynomial(
    coefficients: tuple[Fraction, ...], value: gaussian.ComplexMatrix
) -> gaussian.ComplexMatrix:
    result = gaussian.zero(len(value))
    for coefficient in reversed(coefficients):
        result = gaussian.add(
            gaussian.multiply(result, value),
            gaussian.scale(gaussian.identity(len(value)), coefficient),
        )
    return result


def _sum_matrices(
    values: tuple[gaussian.ComplexMatrix, ...], dimension: int
) -> gaussian.ComplexMatrix:
    result = gaussian.zero(dimension)
    for value in values:
        result = gaussian.add(result, value)
    return result


def construct(generators: tuple[Generator, ...], budget: AlgebraBudget) -> FiniteCoefficientAlgebra:
    if not generators or any(not generator.label for generator in generators):
        raise AlgebraError("InvalidCoefficientGenerators", "generator labels must be nonempty")
    if len({generator.label for generator in generators}) != len(generators):
        raise AlgebraError("InvalidCoefficientGenerators", "generator labels must be unique")
    if (
        budget.maximum_carrier_dimension <= 0
        or budget.maximum_generators <= 0
        or budget.maximum_factor_candidates < 0
    ):
        raise AlgebraError("InvalidCoefficientBudget", "coefficient algebra budget is invalid")
    dimension = len(generators[0].value)
    if dimension > budget.maximum_carrier_dimension or len(generators) > budget.maximum_generators:
        raise AlgebraError(
            "CoefficientAlgebraBudgetExceeded", "carrier or generator budget exceeded"
        )
    if any(len(generator.value) != dimension for generator in generators):
        raise AlgebraError("CoefficientDimensionMismatch", "coefficient dimensions differ")
    if any(not gaussian.is_hermitian(generator.value) for generator in generators):
        raise AlgebraError(
            "NonHermitianCoefficient", "all coefficient generators must be Hermitian"
        )
    zero = gaussian.zero(dimension)
    if any(
        gaussian.bracket(left.value, right.value) != zero
        for index, left in enumerate(generators)
        for right in generators[index + 1 :]
    ):
        raise AlgebraError(
            "NoncommutingCoefficientAlgebra", "coefficient generators do not commute"
        )

    minimal_polynomials = tuple(_minimal_polynomial(generator.value) for generator in generators)
    root_families = []
    factor_candidate_checks = 0
    try:
        for polynomial in minimal_polynomials:
            roots, checks = split_linear_roots(
                polynomial, budget.maximum_factor_candidates - factor_candidate_checks
            )
            root_families.append(roots)
            factor_candidate_checks += checks
    except FactorizationError as error:
        raise AlgebraError(error.kind, str(error)) from error
    partial = [((), gaussian.identity(dimension))]
    refinement: list[RefinementStep] = []
    for generator, roots in zip(generators, root_families, strict=True):
        root_projectors = tuple(_root_projector(generator.value, root, roots) for root in roots)
        refined: list[tuple[tuple[Fraction, ...], gaussian.ComplexMatrix]] = []
        for character, projector in partial:
            for root, root_projector in zip(roots, root_projectors, strict=True):
                intersection = gaussian.multiply(projector, root_projector)
                if intersection != zero:
                    refined.append(((*character, root), intersection))
        refinement.append(RefinementStep(generator.label, roots, len(partial), len(refined)))
        partial = refined

    sectors = tuple(
        Sector(character, projector, _trace_rank(projector)) for character, projector in partial
    )
    unit = gaussian.identity(dimension)
    checks = {
        "minimal_polynomials_annihilate_generators": all(
            _matrix_polynomial(polynomial, generator.value) == zero
            for polynomial, generator in zip(minimal_polynomials, generators, strict=True)
        ),
        "projectors_hermitian": all(gaussian.is_hermitian(sector.projector) for sector in sectors),
        "projectors_idempotent": all(
            gaussian.multiply(sector.projector, sector.projector) == sector.projector
            for sector in sectors
        ),
        "projectors_orthogonal": all(
            gaussian.multiply(left.projector, right.projector) == zero
            for index, left in enumerate(sectors)
            for right in sectors[index + 1 :]
        ),
        "projectors_resolve_identity": _sum_matrices(
            tuple(sector.projector for sector in sectors), dimension
        )
        == unit,
        "generators_reconstructed": all(
            _sum_matrices(
                tuple(
                    gaussian.scale(sector.projector, sector.character[index]) for sector in sectors
                ),
                dimension,
            )
            == generator.value
            for index, generator in enumerate(generators)
        ),
    }
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise AlgebraError("CoefficientAlgebraResidual", f"construction fails at {failed}")
    return FiniteCoefficientAlgebra(
        generators,
        minimal_polynomials,
        sectors,
        tuple(refinement),
        factor_candidate_checks,
        checks,
    )


def _matrix_power(value: gaussian.ComplexMatrix, exponent: int) -> gaussian.ComplexMatrix:
    result = gaussian.identity(len(value))
    factor = value
    while exponent:
        if exponent & 1:
            result = gaussian.multiply(result, factor)
        factor = gaussian.multiply(factor, factor)
        exponent //= 2
    return result


def decompose_polynomial(
    algebra: FiniteCoefficientAlgebra, terms: tuple[PolynomialTerm, ...]
) -> PolynomialDecomposition:
    dimension = len(algebra.generators[0].value)
    if any(
        len(term.powers) != len(algebra.generators)
        or any(
            not isinstance(power, int) or isinstance(power, bool) or power < 0
            for power in term.powers
        )
        for term in terms
    ):
        raise AlgebraError("InvalidCoefficientPolynomial", "polynomial powers are invalid")
    direct = gaussian.zero(dimension)
    for term in terms:
        monomial = gaussian.identity(dimension)
        for generator, power in zip(algebra.generators, term.powers, strict=True):
            monomial = gaussian.multiply(monomial, _matrix_power(generator.value, power))
        direct = gaussian.add(direct, gaussian.scale(monomial, Fraction(term.coefficient)))
    values = tuple(
        sum(
            (
                Fraction(term.coefficient) * _character_monomial(sector.character, term.powers)
                for term in terms
            ),
            Fraction(0),
        )
        for sector in algebra.sectors
    )
    synthesis = _sum_matrices(
        tuple(
            gaussian.scale(sector.projector, value)
            for sector, value in zip(algebra.sectors, values, strict=True)
        ),
        dimension,
    )
    if direct != synthesis:
        raise AlgebraError(
            "PolynomialSynthesisResidual",
            "sector evaluation does not reconstruct the matrix polynomial",
        )
    return PolynomialDecomposition(values, direct, synthesis)


def _character_monomial(character: tuple[Fraction, ...], powers: tuple[int, ...]) -> Fraction:
    result = Fraction(1)
    for value, power in zip(character, powers, strict=True):
        result *= value**power
    return result

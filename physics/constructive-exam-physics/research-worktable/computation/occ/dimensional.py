"""Exact dimensional-quotient construction for typed physical quantities."""

from dataclasses import dataclass
from functools import reduce
from math import gcd, lcm
from typing import Optional

from sympy import Integer, Matrix, Rational, Symbol
from sympy.core.expr import Expr

from .records import Certificate
from .semantic import Dimension, QuantitySemantics


ZERO_DIMENSION = Dimension(0, 0, 0, 0)


@dataclass(frozen=True)
class DimensionlessGroup:
    identifier: str
    exponents: tuple[int, ...]
    expression: Expr
    dimension: Dimension


@dataclass(frozen=True)
class DimensionalObstruction:
    code: str
    message: str


@dataclass(frozen=True)
class DimensionalReductionResult:
    status: str
    quantity_symbols: tuple[Symbol, ...]
    dimension_rank: int
    nullity: int
    groups: tuple[DimensionlessGroup, ...] = ()
    certificates: tuple[Certificate, ...] = ()
    obstruction: Optional[DimensionalObstruction] = None


def _dimension_tuple(dimension: Dimension) -> tuple[int, int, int, int]:
    return (
        dimension.mass,
        dimension.length,
        dimension.time,
        dimension.current,
    )


def _primitive_integer_vector(vector: Matrix) -> tuple[int, ...]:
    rationals = tuple(Rational(value) for value in vector)
    denominator = lcm(*(int(value.q) for value in rationals))
    integers = tuple(int(value * denominator) for value in rationals)
    divisor = reduce(gcd, (abs(value) for value in integers if value), 0)
    primitive = tuple(value // divisor for value in integers)
    first = next(value for value in primitive if value)
    return tuple(-value for value in primitive) if first < 0 else primitive


def _group_dimension(
    quantities: tuple[QuantitySemantics, ...],
    exponents: tuple[int, ...],
) -> Dimension:
    dimension = ZERO_DIMENSION
    for quantity, exponent in zip(quantities, exponents, strict=True):
        dimension += exponent * quantity.dimension
    return dimension


def construct_dimensionless_groups(
    quantities: tuple[QuantitySemantics, ...],
    *,
    max_groups: int = 8,
) -> DimensionalReductionResult:
    """Construct primitive integer representatives of the dimension-kernel basis."""

    if (
        not isinstance(max_groups, int)
        or isinstance(max_groups, bool)
        or max_groups < 1
    ):
        raise ValueError("max_groups must be a positive integer.")
    if not quantities:
        raise ValueError("At least one dimensional quantity is required.")
    if any(not isinstance(quantity.symbol, Symbol) for quantity in quantities):
        raise TypeError("Every dimensional quantity must use a SymPy Symbol.")
    if any(not quantity.physical_name.strip() for quantity in quantities):
        raise ValueError("Every dimensional quantity requires a physical name.")
    if any(not isinstance(quantity.dimension, Dimension) for quantity in quantities):
        raise TypeError("Every quantity requires a four-base Dimension.")
    symbols = tuple(quantity.symbol for quantity in quantities)
    if len(symbols) != len(set(symbols)):
        raise ValueError("Dimensional quantity symbols must be unique.")

    matrix = Matrix(
        list(
            zip(
                *(_dimension_tuple(quantity.dimension) for quantity in quantities),
                strict=True,
            )
        )
    )
    rank = matrix.rank()
    nullity = len(quantities) - rank
    if nullity == 0:
        return DimensionalReductionResult(
            status="irreducible",
            quantity_symbols=symbols,
            dimension_rank=rank,
            nullity=0,
            obstruction=DimensionalObstruction(
                "no_dimensionless_group",
                "The supplied dimensions have no nonconstant invariant monomial.",
            ),
        )
    if nullity > max_groups:
        return DimensionalReductionResult(
            status="refused",
            quantity_symbols=symbols,
            dimension_rank=rank,
            nullity=nullity,
            obstruction=DimensionalObstruction(
                "group_budget_exceeded",
                "The dimension kernel exceeds the declared group budget.",
            ),
        )

    exponent_vectors = tuple(
        _primitive_integer_vector(vector) for vector in matrix.nullspace()
    )
    groups = tuple(
        DimensionlessGroup(
            identifier=f"pi_{index}",
            exponents=exponents,
            expression=reduce(
                lambda left, item: left * item[0].symbol ** item[1],
                zip(quantities, exponents, strict=True),
                Integer(1),
            ),
            dimension=_group_dimension(quantities, exponents),
        )
        for index, exponents in enumerate(exponent_vectors, start=1)
    )
    kernel_passed = all(group.dimension == ZERO_DIMENSION for group in groups)
    primitive_passed = all(
        reduce(gcd, (abs(value) for value in group.exponents if value), 0) == 1
        for group in groups
    )
    certificates = (
        Certificate(
            name="rank_nullity",
            passed=rank + len(groups) == len(quantities),
            witness="dimension rank plus returned nullity equals quantity count",
        ),
        Certificate(
            name="dimension_kernel",
            passed=kernel_passed,
            witness="every returned exponent vector has zero four-base dimension",
        ),
        Certificate(
            name="primitive_integer_representatives",
            passed=primitive_passed,
            witness="each rational nullspace basis vector has primitive integer scale",
        ),
    )
    if not all(certificate.passed for certificate in certificates):
        return DimensionalReductionResult(
            status="refused",
            quantity_symbols=symbols,
            dimension_rank=rank,
            nullity=nullity,
            obstruction=DimensionalObstruction(
                "certificate_failed",
                "The constructed dimensional basis failed an internal certificate.",
            ),
        )
    return DimensionalReductionResult(
        status="constructed",
        quantity_symbols=symbols,
        dimension_rank=rank,
        nullity=nullity,
        groups=groups,
        certificates=certificates,
    )

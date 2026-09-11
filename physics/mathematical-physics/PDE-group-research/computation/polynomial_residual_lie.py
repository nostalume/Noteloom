"""Exact G20 construction from a G19 residual line to a local Lie lift."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import comb

import sympy as sp
from sympy.polys.domains import QQ_I
from sympy.polys.matrices import DomainMatrix

from exact_polynomial_matrix import polynomial_coefficients, term_count
from linear_defect_compiler import DefectBlock, DefectBudget, DefectCompilation, compile_defects
from polynomial_active_module import RationalMatrix, ReductionWitness
from polynomial_active_module_input import PolynomialProblem


class ResidualLieError(ValueError):
    def __init__(self, kind: str, reason: str, details: dict[str, object] | None = None):
        super().__init__(reason)
        self.kind = kind
        self.details = details or {}


@dataclass(frozen=True)
class ResidualDirection:
    vector: tuple[sp.Expr, ...]
    normal_factor: RationalMatrix
    exact_rank: int
    pivot_coordinate: int
    checks: dict[str, bool]


@dataclass(frozen=True)
class ResidualLieCost:
    first_order_scalar_entries: int
    candidate_dimension: int
    residual_coordinates: int
    polynomial_differentiations: int
    polynomial_terms: int


@dataclass(frozen=True)
class ResidualLieWitness:
    direction: ResidualDirection
    internal_generator: sp.ImmutableMatrix
    internal_ambiguity: tuple[sp.ImmutableMatrix, ...]
    candidate_coordinates: tuple[Fraction, ...]
    compilation: DefectCompilation
    cost: ResidualLieCost
    checks: dict[str, bool]
    domain_contract: str


def _zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.cancel(entry) == 0 for entry in matrix)


def _expanded(matrix: sp.MatrixBase) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(matrix.applyfunc(sp.expand))


def _primitive(values: list[sp.Expr], coordinates: tuple[sp.Symbol, ...]):
    denominators = [sp.denom(sp.cancel(value)) for value in values]
    scale = sp.lcm(denominators)
    result = [sp.expand(scale * value) for value in values]
    content = sp.gcd_list(result)
    if content != 0:
        result = [sp.cancel(value / content) for value in result]
    first = next(value for value in result if value != 0)
    leading = sp.Poly(first, *coordinates, domain=QQ_I).LC()
    return tuple(sp.expand(value / leading) for value in result)


def _real_primitive(values: tuple[sp.Expr, ...], coordinates: tuple[sp.Symbol, ...]):
    for left in values:
        for right in values:
            if sp.expand(left * sp.conjugate(right) - sp.conjugate(left) * right) != 0:
                raise ResidualLieError(
                    "ComplexDirectionNoRealForm",
                    "the rank-one residual line has no real polynomial representative",
                )
    pivot = next(value for value in values if value != 0)
    real_values = [sp.expand(value * sp.conjugate(pivot)) for value in values]
    if any(sp.expand(value).as_real_imag()[1] != 0 for value in real_values):
        raise ResidualLieError(
            "ComplexDirectionNoRealForm",
            "the rank-one residual line has no real polynomial representative",
        )
    return _primitive(real_values, coordinates)


def construct_direction(
    witness: ReductionWitness, coordinates: tuple[sp.Symbol, ...]
) -> ResidualDirection:
    """Factor all nonzero first-order leakage through one real polynomial direction."""

    residuals = witness.residual_coefficients
    nonzero = {alpha: value for alpha, value in residuals.items() if not _zero(value.numerator)}
    higher = [alpha for alpha in nonzero if sum(alpha) > 1]
    if higher:
        raise ResidualLieError(
            "HigherOrderResidualNotVectorField",
            "nonzero leakage above first derivative order is not a vector-field direction",
            {"derivatives": tuple(higher)},
        )
    denominators = [value.denominator for value in residuals.values()]
    denominator = denominators[0]
    if any(sp.cancel(value - denominator) != 0 for value in denominators[1:]):
        raise RuntimeError("G19 residual coefficients violated their common-denominator contract")
    rows = witness.ambient_dimension * witness.active_dimension
    columns: list[sp.MatrixBase] = []
    for index in range(len(coordinates)):
        alpha = tuple(int(index == other) for other in range(len(coordinates)))
        value = residuals.get(alpha)
        columns.append(sp.zeros(rows, 1) if value is None else value.numerator.reshape(rows, 1))
    flat = sp.Matrix.hstack(*columns)
    field = QQ_I.frac_field(*coordinates)
    rank = DomainMatrix.from_Matrix(flat).convert_to(field).rank()
    if rank == 0:
        raise ResidualLieError(
            "NoDirectionalLeakage", "the residual has no nonzero first-order directional part"
        )
    if rank != 1:
        raise ResidualLieError(
            "ResidualNotLineGenerated",
            f"the first-order residual has exact function-field rank {rank}, not one",
            {"rank": rank},
        )
    source_row = next(list(flat.row(index)) for index in range(rows) if any(flat.row(index)))
    direction = _real_primitive(_primitive(source_row, coordinates), coordinates)
    pivot = next(index for index, value in enumerate(direction) if value != 0)
    factors = [sp.cancel(flat[row, pivot] / direction[pivot]) for row in range(rows)]
    scale = sp.lcm([sp.denom(value) for value in factors])
    normal_numerator = _expanded(
        sp.Matrix(rows, 1, [sp.expand(scale * value) for value in factors])
    )
    normal_numerator = normal_numerator.reshape(witness.ambient_dimension, witness.active_dimension)
    normal = RationalMatrix(_expanded(normal_numerator), sp.expand(denominator * scale))
    reconstruction = all(
        _zero(
            residuals.get(
                tuple(int(index == other) for other in range(len(coordinates))),
                RationalMatrix(sp.zeros(*normal.numerator.shape), denominator),
            ).numerator
            * normal.denominator
            - normal.numerator * direction[index] * denominator
        )
        for index in range(len(coordinates))
    )
    checks = {
        "exact_function_field_rank_one": rank == 1,
        "direction_is_real": all(sp.expand(value).as_real_imag()[1] == 0 for value in direction),
        "normal_factor_reconstructs": reconstruction,
    }
    if not all(checks.values()):
        raise RuntimeError("residual-line factorization failed its exact reconstruction check")
    return ResidualDirection(direction, normal, rank, pivot, checks)


def _derivative(matrix: sp.MatrixBase, alpha, coordinates):
    result = matrix
    for coordinate, order in zip(coordinates, alpha, strict=True):
        if order:
            result = result.diff(coordinate, order)
    return result


def commutator_coefficients(
    problem: PolynomialProblem,
    direction: tuple[sp.Expr, ...],
    internal: sp.MatrixBase,
):
    result: dict[tuple[int, ...], sp.Matrix] = {}
    zero = (0,) * len(problem.coordinates)
    derivative_cache: dict[tuple[int, tuple[int, ...]], sp.MatrixBase] = {}
    has_direction = any(value != 0 for value in direction)
    for term in problem.operator_terms:
        alpha, coefficient = term.derivative, term.coefficient
        value = internal * coefficient - coefficient * internal
        if has_direction:
            value -= sum(
                (
                    direction[index] * coefficient.diff(coordinate)
                    for index, coordinate in enumerate(problem.coordinates)
                    if direction[index] != 0
                ),
                sp.zeros(*coefficient.shape),
            )
        result[alpha] = result.get(alpha, sp.zeros(*coefficient.shape)) + value
        if not has_direction:
            continue
        for delta in product(*(range(order + 1) for order in alpha)):
            if delta == zero:
                continue
            factor = sp.prod(comb(order, used) for order, used in zip(alpha, delta, strict=True))
            for index, component in enumerate(direction):
                if component == 0:
                    continue
                key = index, delta
                if key not in derivative_cache:
                    derivative_cache[key] = _derivative(component, delta, problem.coordinates)
                differentiated = derivative_cache[key]
                gamma = tuple(
                    order - used + int(index == other)
                    for other, (order, used) in enumerate(zip(alpha, delta, strict=True))
                )
                result[gamma] = result.get(gamma, sp.zeros(*coefficient.shape))
                result[gamma] += factor * coefficient * differentiated
    return {alpha: _expanded(value) for alpha, value in result.items()}


def _differentiation_cost(problem: PolynomialProblem, direction):
    active = sum(value != 0 for value in direction)
    coefficient_cost = active * len(problem.operator_terms)
    deltas = {
        delta
        for term in problem.operator_terms
        for delta in product(*(range(order + 1) for order in term.derivative))
        if any(delta)
    }
    return coefficient_cost + active * sum(sum(delta) for delta in deltas)


def _unitary_basis(dimension: int):
    basis: list[sp.ImmutableMatrix] = []
    labels: list[str] = []
    for row in range(dimension):
        value = sp.zeros(dimension)
        value[row, row] = sp.I
        basis.append(sp.ImmutableMatrix(value))
        labels.append(f"internal:imag-diagonal:{row}")
    for row in range(dimension):
        for column in range(row + 1, dimension):
            real = sp.zeros(dimension)
            real[row, column], real[column, row] = 1, -1
            basis.append(sp.ImmutableMatrix(real))
            labels.append(f"internal:real-skew:{row},{column}")
            imaginary = sp.zeros(dimension)
            imaginary[row, column] = imaginary[column, row] = sp.I
            basis.append(sp.ImmutableMatrix(imaginary))
            labels.append(f"internal:imag-symmetric:{row},{column}")
    return tuple(basis), tuple(labels)


def _coordinate_block(candidates, problem: PolynomialProblem):
    sparse: list[dict[tuple, Fraction]] = []
    labels: set[tuple] = set()
    terms = 0
    for candidate in candidates:
        column: dict[tuple, Fraction] = {}
        for alpha, matrix in sorted(candidate.items()):
            current_terms = term_count(matrix, problem.coordinates)
            terms += current_terms
            if current_terms > problem.budget.maximum_polynomial_terms:
                raise ResidualLieError(
                    "PolynomialTermBudgetExceeded",
                    "commutator coefficients exceed the polynomial-term budget",
                    {
                        "observed_terms": current_terms,
                        "maximum_terms": problem.budget.maximum_polynomial_terms,
                    },
                )
            for row in range(matrix.rows):
                for column_index in range(matrix.cols):
                    for powers, real, imaginary in polynomial_coefficients(
                        matrix[row, column_index], problem.coordinates
                    ):
                        if real:
                            key = (alpha, row, column_index, powers, "real")
                            column[key] = real
                            labels.add(key)
                        if imaginary:
                            key = (alpha, row, column_index, powers, "imaginary")
                            column[key] = imaginary
                            labels.add(key)
        sparse.append(column)
    ordered = tuple(sorted(labels))
    names = tuple(repr(value) for value in ordered)
    columns = tuple(tuple(column.get(label, Fraction(0)) for label in ordered) for column in sparse)
    return DefectBlock("full-operator-commutator", names, columns), terms


def _internal_combination(coefficients, basis):
    dimension = basis[0].rows
    return _expanded(
        sum(
            (
                sp.Rational(value.numerator, value.denominator) * item
                for value, item in zip(coefficients, basis, strict=True)
            ),
            sp.zeros(dimension),
        )
    )


def construct_lift(
    problem: PolynomialProblem, witness: ReductionWitness, budget: DefectBudget
) -> ResidualLieWitness:
    """Construct a visible local infinitesimal symmetry or return a typed refusal."""

    direction = construct_direction(witness, problem.coordinates)
    internal_basis, internal_labels = _unitary_basis(witness.ambient_dimension)
    labels = ("base-direction", *internal_labels)
    if len(labels) > budget.maximum_candidate_dimension:
        raise ResidualLieError(
            "CandidateBudgetExceeded",
            f"candidate dimension {len(labels)} exceeds budget {budget.maximum_candidate_dimension}",
        )
    zero_direction = (sp.S.Zero,) * len(problem.coordinates)
    candidates = [
        commutator_coefficients(problem, direction.vector, sp.zeros(witness.ambient_dimension))
    ]
    candidates.extend(
        commutator_coefficients(problem, zero_direction, value) for value in internal_basis
    )
    block, terms = _coordinate_block(candidates, problem)
    compilation = compile_defects(candidate_labels=labels, blocks=(block,), budget=budget)
    if compilation.outcome != "exact":
        raise ResidualLieError(
            compilation.obstruction_kind or "ResidualLieCompilationUnresolved",
            compilation.obstruction_reason or "residual Lie compilation was unresolved",
            {"compilation": compilation},
        )
    visible = next((value for value in compilation.kernel_basis if value[0]), None)
    if visible is None:
        raise ResidualLieError(
            "NoInfinitesimalLift",
            "the exact commutator kernel has no generator visible on the base direction",
            {"compilation": compilation},
        )
    visible = tuple(value / visible[0] for value in visible)
    internal = _internal_combination(visible[1:], internal_basis)
    ambiguity_vectors = []
    for value in compilation.kernel_basis:
        projected = tuple(value[index] - value[0] * visible[index] for index in range(len(visible)))
        if any(projected[1:]):
            ambiguity_vectors.append(projected)
    ambiguity = tuple(
        _internal_combination(value[1:], internal_basis) for value in ambiguity_vectors
    )
    commutator_zero = all(
        _zero(value)
        for value in commutator_coefficients(problem, direction.vector, internal).values()
    )
    checks = {
        **direction.checks,
        "internal_generator_is_skew_hermitian": _zero(internal.conjugate().T + internal),
        "full_operator_commutator_vanishes": commutator_zero,
        "internal_ambiguity_commutes": all(
            all(
                _zero(value)
                for value in commutator_coefficients(problem, zero_direction, item).values()
            )
            for item in ambiguity
        ),
    }
    if not all(checks.values()):
        raise RuntimeError("residual Lie lift failed an exact construction check")
    return ResidualLieWitness(
        direction,
        internal,
        ambiguity,
        visible,
        compilation,
        ResidualLieCost(
            witness.ambient_dimension * witness.active_dimension * len(problem.coordinates),
            len(labels),
            len(block.target_labels),
            _differentiation_cost(problem, direction.vector),
            terms,
        ),
        checks,
        problem.domain_contract,
    )

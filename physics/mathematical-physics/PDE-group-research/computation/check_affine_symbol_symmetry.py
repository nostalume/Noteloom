"""Exact G22 probe: construct affine PDE symmetries from the principal symbol."""

from __future__ import annotations

import json
import unittest
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import sympy as sp

from exact_polynomial_matrix import polynomial_coefficients, term_count
from linear_defect_compiler import (
    CandidateBracket,
    DefectBlock,
    DefectBudget,
    LinearMap,
    compile_defects,
)
from polynomial_active_module import construct_reduction
from polynomial_active_module_input import (
    OperatorTerm,
    PolynomialBudget,
    PolynomialLiftRequest,
    PolynomialProblem,
    parse,
)
from polynomial_residual_lie import commutator_coefficients, construct_lift

HERE = Path(__file__).resolve().parent


class AffineSymbolError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


@dataclass(frozen=True)
class Lift:
    direction: tuple[sp.Expr, ...]
    internal: sp.ImmutableMatrix
    label: str


@dataclass(frozen=True)
class AffineSymmetry:
    principal_symbol: sp.ImmutableMatrix
    base_candidate_dimension: int
    candidate_dimension: int
    kernel_dimension: int
    visible_dimension: int
    ambiguity_dimension: int
    representatives: tuple[Lift, ...]
    quotient_bracket_table: tuple[tuple[tuple[Fraction, ...], ...], ...]
    residual_coordinates: int
    polynomial_terms: int
    bracket_checks: int
    checks: dict[str, bool]


def _fraction(value: sp.Expr, kind: str) -> Fraction:
    value = sp.cancel(value)
    if value.is_Rational is not True:
        raise AffineSymbolError(kind, "the principal symbol must have rational real constants")
    return Fraction(int(value.p), int(value.q))


def _scalar_constant(matrix: sp.MatrixBase, coordinates) -> Fraction:
    if any(entry.free_symbols.intersection(coordinates) for entry in matrix):
        raise AffineSymbolError(
            "VariablePrincipalSymbol", "the affine constructor requires a constant principal symbol"
        )
    scalar = matrix[0, 0]
    if any(
        sp.cancel(matrix[row, column] - (scalar if row == column else 0)) != 0
        for row in range(matrix.rows)
        for column in range(matrix.cols)
    ):
        raise AffineSymbolError(
            "NonScalarPrincipalSymbol",
            "each second-order coefficient must be scalar on the carrier",
        )
    return _fraction(scalar, "NonRationalPrincipalSymbol")


def _principal_symbol(problem: PolynomialProblem) -> sp.ImmutableMatrix:
    dimension = len(problem.coordinates)
    carrier = problem.preparation.rows
    if any(sum(term.derivative) > 2 for term in problem.operator_terms):
        raise AffineSymbolError("HigherOrderOperator", "the affine constructor is second-order")
    coefficients = {
        term.derivative: term.coefficient
        for term in problem.operator_terms
        if sum(term.derivative) == 2
    }
    if not coefficients:
        raise AffineSymbolError("MissingSecondOrderSymbol", "no second-order symbol is present")
    metric = sp.zeros(dimension)
    zero = sp.zeros(carrier)
    for left in range(dimension):
        diagonal = tuple(2 * int(index == left) for index in range(dimension))
        metric[left, left] = -sp.Rational(
            _scalar_constant(coefficients.get(diagonal, zero), problem.coordinates)
        )
        for right in range(left + 1, dimension):
            mixed = tuple(int(index in (left, right)) for index in range(dimension))
            value = -sp.Rational(
                _scalar_constant(coefficients.get(mixed, zero), problem.coordinates), 2
            )
            metric[left, right] = metric[right, left] = value
    if metric.det() == 0:
        raise AffineSymbolError(
            "DegeneratePrincipalSymbol",
            "a degenerate symbol does not bound polynomial symmetries by affine Killing fields",
        )
    return sp.ImmutableMatrix(metric)


def _affine_candidates(metric: sp.MatrixBase, coordinates) -> tuple[Lift, ...]:
    dimension = len(coordinates)
    carrier_zero = sp.ImmutableMatrix([[0]])
    candidates = [
        Lift(
            tuple(sp.S.One if index == target else sp.S.Zero for index in range(dimension)),
            carrier_zero,
            f"translation:{target}",
        )
        for target in range(dimension)
    ]
    position = sp.Matrix(coordinates)
    for left in range(dimension):
        for right in range(left + 1, dimension):
            skew = sp.zeros(dimension)
            skew[left, right], skew[right, left] = 1, -1
            direction = sp.ImmutableMatrix(metric * skew) * position
            candidates.append(
                Lift(
                    tuple(map(sp.expand, direction)),
                    carrier_zero,
                    f"metric-rotation:{left},{right}",
                )
            )
    return tuple(candidates)


def _unitary_candidates(dimension: int, coordinate_dimension: int) -> tuple[Lift, ...]:
    zero = (sp.S.Zero,) * coordinate_dimension
    candidates: list[Lift] = []
    for row in range(dimension):
        value = sp.zeros(dimension)
        value[row, row] = sp.I
        candidates.append(Lift(zero, sp.ImmutableMatrix(value), f"internal:iE{row}{row}"))
    for row in range(dimension):
        for column in range(row + 1, dimension):
            real = sp.zeros(dimension)
            real[row, column], real[column, row] = 1, -1
            candidates.append(
                Lift(zero, sp.ImmutableMatrix(real), f"internal:E{row}{column}-E{column}{row}")
            )
            imaginary = sp.zeros(dimension)
            imaginary[row, column] = imaginary[column, row] = sp.I
            candidates.append(
                Lift(zero, sp.ImmutableMatrix(imaginary), f"internal:iS{row}{column}")
            )
    return tuple(candidates)


def _with_carrier(lift: Lift, carrier: int) -> Lift:
    if lift.internal.shape == (carrier, carrier):
        return lift
    return Lift(lift.direction, sp.ImmutableMatrix(sp.zeros(carrier)), lift.label)


def _bracket(left: Lift, right: Lift, coordinates) -> Lift:
    direction = tuple(
        sp.expand(
            sum(
                left.direction[index] * sp.diff(right.direction[target], coordinate)
                - right.direction[index] * sp.diff(left.direction[target], coordinate)
                for index, coordinate in enumerate(coordinates)
            )
        )
        for target in range(len(coordinates))
    )
    internal = -(left.internal * right.internal - right.internal * left.internal)
    return Lift(direction, sp.ImmutableMatrix(internal), "bracket")


def _sparse_lift(lift: Lift, coordinates) -> dict[tuple, Fraction]:
    result: dict[tuple, Fraction] = {}
    expressions = (*lift.direction, *tuple(lift.internal))
    for index, expression in enumerate(expressions):
        for powers, real, imaginary in polynomial_coefficients(expression, coordinates):
            if real:
                result[index, powers, "real"] = real
            if imaginary:
                result[index, powers, "imaginary"] = imaginary
    return result


def _candidate_bracket(candidates: tuple[Lift, ...], coordinates) -> CandidateBracket:
    sparse_basis = tuple(_sparse_lift(candidate, coordinates) for candidate in candidates)
    labels = tuple(sorted(set().union(*(value.keys() for value in sparse_basis))))
    basis = sp.Matrix(
        [[column.get(label, Fraction(0)) for column in sparse_basis] for label in labels]
    )

    def coordinates_of(value: Lift) -> tuple[Fraction, ...]:
        sparse = _sparse_lift(value, coordinates)
        if any(label not in labels for label in sparse):
            raise RuntimeError("the intrinsic affine candidate space is not bracket closed")
        solution = basis.gauss_jordan_solve(
            sp.Matrix([sparse.get(label, Fraction(0)) for label in labels])
        )[0]
        return tuple(_fraction(entry, "NonRationalBracket") for entry in solution)

    table = tuple(
        tuple(coordinates_of(_bracket(left, right, coordinates)) for right in candidates)
        for left in candidates
    )
    return CandidateBracket("affine-killing-plus-unitary", table)


def _defect_block(
    problem: PolynomialProblem, candidates: tuple[Lift, ...]
) -> tuple[DefectBlock, int]:
    columns: list[dict[tuple, Fraction]] = []
    labels: set[tuple] = set()
    terms = 0
    for candidate in candidates:
        column: dict[tuple, Fraction] = {}
        residual = commutator_coefficients(problem, candidate.direction, candidate.internal)
        for derivative, matrix in sorted(residual.items()):
            current_terms = term_count(matrix, problem.coordinates)
            terms += current_terms
            if current_terms > problem.budget.maximum_polynomial_terms:
                raise AffineSymbolError(
                    "PolynomialTermBudgetExceeded",
                    "one commutator coefficient exceeds the polynomial-term budget",
                )
            if terms > problem.budget.maximum_output_terms:
                raise AffineSymbolError(
                    "OutputTermBudgetExceeded",
                    "the commutator family exceeds the output-term budget",
                )
            for row in range(matrix.rows):
                for column_index in range(matrix.cols):
                    for powers, real, imaginary in polynomial_coefficients(
                        matrix[row, column_index], problem.coordinates
                    ):
                        if real:
                            key = (derivative, row, column_index, powers, "real")
                            column[key] = real
                            labels.add(key)
                        if imaginary:
                            key = (derivative, row, column_index, powers, "imaginary")
                            column[key] = imaginary
                            labels.add(key)
        columns.append(column)
    ordered = tuple(sorted(labels))
    return (
        DefectBlock(
            "full-operator-commutator",
            tuple(map(repr, ordered)),
            tuple(tuple(column.get(label, Fraction(0)) for label in ordered) for column in columns),
        ),
        terms,
    )


def _combine(vector, candidates: tuple[Lift, ...]) -> Lift:
    values = tuple(sp.Rational(value.numerator, value.denominator) for value in vector)
    direction = tuple(
        sp.expand(sum(value * lift.direction[index] for value, lift in zip(values, candidates)))
        for index in range(len(candidates[0].direction))
    )
    internal = sum(
        (value * lift.internal for value, lift in zip(values, candidates)),
        sp.zeros(candidates[0].internal.rows),
    )
    return Lift(direction, sp.ImmutableMatrix(internal), "kernel-representative")


def construct_affine_symmetry(problem: PolynomialProblem, budget: DefectBudget) -> AffineSymmetry:
    metric = _principal_symbol(problem)
    carrier = problem.preparation.rows
    base = tuple(
        _with_carrier(lift, carrier) for lift in _affine_candidates(metric, problem.coordinates)
    )
    candidates = (*base, *_unitary_candidates(carrier, len(problem.coordinates)))
    visible = LinearMap(
        "base-vector-field",
        tuple(lift.label for lift in base),
        tuple(
            tuple(Fraction(int(index == target)) for target in range(len(base)))
            if index < len(base)
            else (Fraction(0),) * len(base)
            for index in range(len(candidates))
        ),
    )
    block, terms = _defect_block(problem, candidates)
    compilation = compile_defects(
        candidate_labels=tuple(lift.label for lift in candidates),
        blocks=(block,),
        budget=budget,
        visible_action=visible,
        bracket=_candidate_bracket(candidates, problem.coordinates),
    )
    if compilation.outcome != "exact":
        raise AffineSymbolError(
            compilation.obstruction_kind or "AffineCompilationUnresolved",
            compilation.obstruction_reason or "affine symmetry compilation did not certify",
        )
    representatives = tuple(
        _combine(vector, candidates) for vector in compilation.effective_representatives
    )
    lower_metric = metric.inv()
    killing = all(
        (
            sp.Matrix(lift.direction).jacobian(problem.coordinates).T * lower_metric
            + lower_metric * sp.Matrix(lift.direction).jacobian(problem.coordinates)
        ).is_zero_matrix
        for lift in base
    )
    kernel_zero = all(
        all(
            matrix.is_zero_matrix
            for matrix in commutator_coefficients(problem, lift.direction, lift.internal).values()
        )
        for lift in (_combine(vector, candidates) for vector in compilation.kernel_basis)
    )
    checks = {
        "affine_candidates_satisfy_killing_equation": killing,
        "full_kernel_commutes_with_operator": kernel_zero,
        "kernel_and_ambiguity_quotient_are_lie_certified": compilation.closure_status == "closed",
    }
    if not all(checks.values()):
        raise RuntimeError("affine principal-symbol construction failed an exact check")
    return AffineSymmetry(
        metric,
        len(base),
        len(candidates),
        compilation.kernel_dimension,
        compilation.effective_dimension,
        len(compilation.ineffective_basis),
        representatives,
        compilation.quotient_bracket_table,
        len(block.target_labels),
        terms,
        compilation.bracket_checks,
        checks,
    )


def _problem(
    dimension: int,
    carrier: int,
    potential: sp.MatrixBase,
    metric: sp.MatrixBase | None = None,
) -> PolynomialProblem:
    coordinates = tuple(sp.symbols(f"x0:{dimension}", real=True))
    identity = sp.eye(carrier)
    metric = sp.eye(dimension) if metric is None else metric
    terms = [OperatorTerm((0,) * dimension, sp.ImmutableMatrix(potential))]
    for left in range(dimension):
        diagonal = tuple(2 * int(index == left) for index in range(dimension))
        terms.append(OperatorTerm(diagonal, sp.ImmutableMatrix(-metric[left, left] * identity)))
        for right in range(left + 1, dimension):
            if metric[left, right] == 0:
                continue
            mixed = tuple(int(index in (left, right)) for index in range(dimension))
            terms.append(
                OperatorTerm(mixed, sp.ImmutableMatrix(-2 * metric[left, right] * identity))
            )
    return PolynomialProblem(
        coordinates,
        tuple(terms),
        sp.ImmutableMatrix([1, *((0,) * (carrier - 1))]),
        sp.ImmutableMatrix(identity),
        (Fraction(0),) * dimension,
        ((Fraction(-1), Fraction(1)),) * dimension,
        "decompose-with-residual",
        PolynomialBudget(carrier, carrier, 2, 1024, 1, 4096),
        "C_c^infinity(region; C^n), boundary none",
    )


class AffineSymbolSymmetryChecks(unittest.TestCase):
    budget = DefectBudget(20, 2000, 10_000)

    def test_radial_matrix_pde_constructs_so3_without_supplied_generators(self):
        coordinates = sp.symbols("x0:3", real=True)
        position = sp.Matrix(coordinates)
        result = construct_affine_symmetry(_problem(3, 3, position * position.T), self.budget)

        self.assertEqual(result.base_candidate_dimension, 6)
        self.assertEqual(result.candidate_dimension, 15)
        self.assertEqual(result.kernel_dimension, 4)
        self.assertEqual(result.visible_dimension, 3)
        self.assertEqual(result.ambiguity_dimension, 1)
        self.assertTrue(all(result.checks.values()))

    def test_free_and_anisotropic_scalar_pdes_are_filtered_by_lower_order_terms(self):
        x, y = sp.symbols("x0:2", real=True)
        free = construct_affine_symmetry(_problem(2, 1, sp.zeros(1)), self.budget)
        sheared_metric = sp.Matrix([[2, 1], [1, 1]])
        sheared = construct_affine_symmetry(
            _problem(2, 1, sp.zeros(1), sheared_metric), self.budget
        )
        anisotropic = construct_affine_symmetry(
            _problem(2, 1, sp.Matrix([[x**2 + 2 * y**2]])), self.budget
        )

        self.assertEqual((free.visible_dimension, free.ambiguity_dimension), (3, 1))
        self.assertEqual(sheared.principal_symbol, sheared_metric)
        self.assertEqual((sheared.visible_dimension, sheared.ambiguity_dimension), (3, 1))
        self.assertEqual((anisotropic.visible_dimension, anisotropic.ambiguity_dimension), (0, 1))

    def test_principal_symbol_and_residual_routes_coincide_on_public_fixture(self):
        payload = json.loads(
            (HERE / "examples" / "polynomial-lie-lift.json").read_text(encoding="utf-8")
        )
        request = parse(payload)
        self.assertIsInstance(request, PolynomialLiftRequest)
        assert isinstance(request, PolynomialLiftRequest)
        residual_lift = construct_lift(
            request.problem, construct_reduction(request.problem), request.budget
        )
        affine = construct_affine_symmetry(request.problem, self.budget)
        direct = affine.representatives[0].direction
        matrix = sp.Matrix.hstack(sp.Matrix(direct), sp.Matrix(residual_lift.direction.vector))

        self.assertEqual(affine.visible_dimension, 1)
        self.assertEqual(affine.ambiguity_dimension, 1)
        self.assertEqual(matrix.rank(), 1)

    def test_degenerate_symbol_is_a_typed_refusal_not_no_symmetry(self):
        x, y = sp.symbols("x0:2", real=True)
        problem = PolynomialProblem(
            (x, y),
            (OperatorTerm((0, 2), sp.ImmutableMatrix([[-1]])),),
            sp.ImmutableMatrix([1]),
            sp.ImmutableMatrix([[1]]),
            (Fraction(0), Fraction(0)),
            ((Fraction(-1), Fraction(1)),) * 2,
            "decompose-with-residual",
            PolynomialBudget(1, 1, 2, 64, 1, 64),
            "C_c^infinity(region; C^n), boundary none",
        )

        with self.assertRaises(AffineSymbolError) as caught:
            construct_affine_symmetry(problem, self.budget)

        self.assertEqual(caught.exception.kind, "DegeneratePrincipalSymbol")


if __name__ == "__main__":
    unittest.main()

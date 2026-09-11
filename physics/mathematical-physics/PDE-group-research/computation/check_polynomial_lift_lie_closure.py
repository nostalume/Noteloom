"""Exact G21 probe for Lie closure of polynomial infinitesimal lift pairs."""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from fractions import Fraction
from itertools import product

import sympy as sp

from exact_polynomial_matrix import polynomial_coefficients
from polynomial_active_module_input import OperatorTerm, PolynomialBudget, PolynomialProblem
from polynomial_residual_lie import commutator_coefficients


@dataclass(frozen=True)
class Lift:
    direction: tuple[sp.Expr, ...]
    internal: sp.ImmutableMatrix
    provenance: str


@dataclass(frozen=True)
class Closure:
    outcome: str
    basis: tuple[Lift, ...]
    structure: tuple[tuple[tuple[Fraction, ...], ...], ...]
    quotient_structure: tuple[tuple[tuple[Fraction, ...], ...], ...]
    visible_dimension: int
    ambiguity_dimension: int
    bracket_evaluations: int
    checks: dict[str, bool]


def _zero_coefficients(problem: PolynomialProblem, lift: Lift) -> bool:
    return all(
        all(sp.cancel(entry) == 0 for entry in value)
        for value in commutator_coefficients(problem, lift.direction, lift.internal).values()
    )


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
    return Lift(direction, sp.ImmutableMatrix(internal), f"[{left.provenance},{right.provenance}]")


def _columns(lifts: tuple[Lift, ...], coordinates):
    sparse = []
    labels = set()
    for lift in lifts:
        column = {}
        expressions = (*lift.direction, *tuple(lift.internal))
        for index, expression in enumerate(expressions):
            for powers, real, imaginary in polynomial_coefficients(expression, coordinates):
                if real:
                    column[index, powers, "real"] = real
                    labels.add((index, powers, "real"))
                if imaginary:
                    column[index, powers, "imaginary"] = imaginary
                    labels.add((index, powers, "imaginary"))
        sparse.append(column)
    ordered = tuple(sorted(labels))
    return sp.Matrix([[column.get(label, Fraction(0)) for column in sparse] for label in ordered])


def _rank(lifts: tuple[Lift, ...], coordinates) -> int:
    return _columns(lifts, coordinates).rank() if lifts else 0


def _coordinates(lift: Lift, basis: tuple[Lift, ...], coordinates):
    matrix = _columns((*basis, lift), coordinates)
    solution = matrix[:, :-1].gauss_jordan_solve(matrix[:, -1])[0]
    return tuple(Fraction(int(value.p), int(value.q)) for value in solution)


def _combine(coefficients, basis: tuple[Lift, ...]) -> Lift:
    rational = tuple(sp.Rational(value.numerator, value.denominator) for value in coefficients)
    direction = tuple(
        sp.expand(sum(value * lift.direction[index] for value, lift in zip(rational, basis)))
        for index in range(len(basis[0].direction))
    )
    internal = sum(
        (value * lift.internal for value, lift in zip(rational, basis)),
        sp.zeros(basis[0].internal.rows),
    )
    return Lift(direction, sp.ImmutableMatrix(internal), "linear-kernel")


def _jacobi(table) -> bool:
    dimension = len(table)
    for left in range(dimension):
        for middle in range(dimension):
            for right in range(dimension):
                for target in range(dimension):
                    value = sum(
                        table[middle][right][index] * table[left][index][target]
                        + table[right][left][index] * table[middle][index][target]
                        + table[left][middle][index] * table[right][index][target]
                        for index in range(dimension)
                    )
                    if value:
                        return False
    return True


def close_lifts(problem: PolynomialProblem, seeds: tuple[Lift, ...], budget: int) -> Closure:
    if budget <= 0:
        raise ValueError("ClosureBudgetMustBePositive")
    if any(not _zero_coefficients(problem, lift) for lift in seeds):
        raise ValueError("SeedNotFullOperatorSymmetry")
    basis: list[Lift] = []
    for seed in seeds:
        if _rank((*basis, seed), problem.coordinates) > len(basis):
            if len(basis) == budget:
                return Closure("unresolved", tuple(basis), (), (), 0, 0, 0, {})
            basis.append(seed)
    checks: set[tuple[int, int]] = set()
    evaluations = 0
    while True:
        added = False
        for left in range(len(basis)):
            for right in range(left + 1, len(basis)):
                if (left, right) in checks:
                    continue
                checks.add((left, right))
                evaluations += 1
                candidate = _bracket(basis[left], basis[right], problem.coordinates)
                if _rank((*basis, candidate), problem.coordinates) == len(basis):
                    continue
                if len(basis) == budget:
                    return Closure("unresolved", tuple(basis), (), (), 0, 0, evaluations, {})
                assert _zero_coefficients(problem, candidate)
                basis.append(candidate)
                added = True
        if not added:
            break
    frozen = tuple(basis)
    zero_internal = sp.ImmutableMatrix(sp.zeros(problem.preparation.rows))
    visible_representatives: list[Lift] = []
    for lift in frozen:
        direction_only = Lift(lift.direction, zero_internal, lift.provenance)
        if _rank((*visible_representatives, direction_only), problem.coordinates) > len(
            visible_representatives
        ):
            visible_representatives.append(lift)
    projection = _columns(
        tuple(Lift(lift.direction, zero_internal, lift.provenance) for lift in frozen),
        problem.coordinates,
    )
    ambiguity = tuple(
        _combine(tuple(Fraction(int(value.p), int(value.q)) for value in kernel), frozen)
        for kernel in projection.nullspace()
    )
    adapted = (*visible_representatives, *ambiguity)
    structure = tuple(
        tuple(
            _coordinates(_bracket(left, right, problem.coordinates), adapted, problem.coordinates)
            for right in adapted
        )
        for left in adapted
    )
    visible_dimension = len(visible_representatives)
    quotient = tuple(
        tuple(value[:visible_dimension] for value in row[:visible_dimension])
        for row in structure[:visible_dimension]
    )
    ideal = all(
        _rank((*ambiguity, _bracket(lift, internal, problem.coordinates)), problem.coordinates)
        == len(ambiguity)
        for lift in adapted
        for internal in ambiguity
    )
    return Closure(
        "exact",
        adapted,
        structure,
        quotient,
        visible_dimension,
        len(ambiguity),
        evaluations,
        {
            "ambiguity_is_ideal": ideal,
            "quotient_is_antisymmetric": all(
                tuple(
                    quotient[left][right][target] + quotient[right][left][target]
                    for target in range(visible_dimension)
                )
                == (Fraction(0),) * visible_dimension
                for left in range(visible_dimension)
                for right in range(visible_dimension)
            ),
            "quotient_satisfies_jacobi": _jacobi(quotient),
        },
    )


def _problem(*, radial: bool) -> PolynomialProblem:
    if radial:
        coordinates = sp.symbols("x y z", real=True)
        position = sp.Matrix(coordinates)
        identity = sp.eye(3)
        terms = [OperatorTerm((0, 0, 0), sp.ImmutableMatrix(position * position.T))]
        terms.extend(
            OperatorTerm(tuple(2 * int(i == j) for i in range(3)), sp.ImmutableMatrix(-identity))
            for j in range(3)
        )
        preparation = sp.ImmutableMatrix([1, 0, 0])
    else:
        coordinates = sp.symbols("x y", real=True)
        terms = [OperatorTerm((0, 2), sp.ImmutableMatrix([[-1]]))]
        preparation = sp.ImmutableMatrix([1])
    dimension = preparation.rows
    return PolynomialProblem(
        coordinates,
        tuple(terms),
        preparation,
        sp.ImmutableMatrix(sp.eye(dimension)),
        (Fraction(0),) * len(coordinates),
        ((Fraction(-1), Fraction(1)),) * len(coordinates),
        "decompose-with-residual",
        PolynomialBudget(dimension, dimension, 2, 512, 1, 512),
        "C_c^infinity(region; C^n), boundary none",
    )


def _rotation(problem: PolynomialProblem, left: int, right: int) -> Lift:
    matrix = sp.zeros(3)
    matrix[left, right], matrix[right, left] = -1, 1
    position = sp.Matrix(problem.coordinates)
    return Lift(tuple(matrix * position), sp.ImmutableMatrix(matrix), f"R{left}{right}")


class PolynomialLiftLieClosureChecks(unittest.TestCase):
    def test_non_degenerate_scalar_symbol_forces_affine_killing_fields(self):
        dimension = 3
        coordinates = sp.symbols("x y z", real=True)
        powers = tuple(value for value in product(range(3), repeat=dimension) if sum(value) <= 2)
        coefficients = sp.symbols(f"c0:{dimension * len(powers)}", real=True)
        directions = tuple(
            sum(
                coefficients[target * len(powers) + index]
                * sp.prod(x**power for x, power in zip(coordinates, alpha))
                for index, alpha in enumerate(powers)
            )
            for target in range(dimension)
        )
        equations = []
        for left in range(dimension):
            for right in range(left, dimension):
                expression = sp.diff(directions[right], coordinates[left])
                expression += sp.diff(directions[left], coordinates[right])
                equations.extend(sp.Poly(expression, *coordinates).coeffs())
        matrix, _ = sp.linear_eq_to_matrix(equations, coefficients)
        kernel = matrix.nullspace()
        quadratic = tuple(index for index, alpha in enumerate(powers) if sum(alpha) == 2)

        self.assertEqual(len(kernel), dimension * (dimension + 1) // 2)
        self.assertTrue(
            all(
                vector[target * len(powers) + index] == 0
                for vector in kernel
                for target in range(dimension)
                for index in quadratic
            )
        )

    def test_two_rotation_lifts_generate_so3_with_scalar_ambiguity(self):
        problem = _problem(radial=True)
        scalar = Lift((0, 0, 0), sp.ImmutableMatrix(sp.I * sp.eye(3)), "iI")
        result = close_lifts(
            problem, (_rotation(problem, 0, 1), _rotation(problem, 1, 2), scalar), 4
        )

        self.assertEqual(result.outcome, "exact")
        self.assertEqual(len(result.basis), 4)
        self.assertEqual(result.visible_dimension, 3)
        self.assertEqual(result.ambiguity_dimension, 1)
        self.assertTrue(all(result.checks.values()))
        self.assertEqual(result.quotient_structure[0][1], (0, 0, 1))
        self.assertEqual(result.quotient_structure[1][2], (1, 0, 0))
        self.assertTrue(all(_zero_coefficients(problem, lift) for lift in result.basis))

    def test_constant_span_closure_can_exceed_a_finite_budget(self):
        problem = _problem(radial=False)
        x, _ = problem.coordinates
        zero = sp.ImmutableMatrix([[0]])
        seeds = (
            Lift((x**2, 0), zero, "x2"),
            Lift((x**3, 0), zero, "x3"),
        )

        result = close_lifts(problem, seeds, 5)

        self.assertEqual(result.outcome, "unresolved")
        self.assertEqual(len(result.basis), 5)
        self.assertEqual(result.basis[2].direction, (x**4, 0))
        self.assertTrue(all(_zero_coefficients(problem, lift) for lift in result.basis))

    def test_invalid_seed_is_refused_before_closure(self):
        problem = _problem(radial=True)
        bad = _rotation(problem, 0, 1)
        bad = Lift(bad.direction, sp.ImmutableMatrix(sp.zeros(3)), "missing-internal-lift")

        with self.assertRaisesRegex(ValueError, "SeedNotFullOperatorSymmetry"):
            close_lifts(problem, (bad,), 3)


if __name__ == "__main__":
    unittest.main()

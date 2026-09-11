"""Exact exploratory checks for the G20 residual-to-Lie inquiry."""

from __future__ import annotations

import json
import unittest
from itertools import product
from math import comb
from pathlib import Path

import sympy as sp

from polynomial_active_module import ReductionWitness, construct_reduction
from polynomial_active_module_input import PolynomialProblem, parse

HERE = Path(__file__).resolve().parent


def _payload(name: str) -> dict[str, object]:
    return json.loads((HERE / "examples" / name).read_text(encoding="utf-8"))


def _nonzero(matrix: sp.MatrixBase) -> bool:
    return any(sp.cancel(entry) != 0 for entry in matrix)


def _first_order_flat(witness: ReductionWitness, dimension: int) -> sp.Matrix:
    shape = (witness.ambient_dimension * witness.active_dimension, 1)
    columns = []
    for index in range(dimension):
        alpha = tuple(int(index == other) for other in range(dimension))
        value = witness.residual_coefficients.get(alpha)
        columns.append(sp.zeros(*shape) if value is None else value.numerator.reshape(*shape))
    return sp.Matrix.hstack(*columns)


def _primitive_line(matrix: sp.Matrix, coordinates: tuple[sp.Symbol, ...]):
    row = matrix.rowspace()[0]
    denominators = [sp.denom(sp.cancel(entry)) for entry in row]
    scale = sp.lcm(denominators)
    values = [sp.expand(scale * entry) for entry in row]
    content = sp.gcd_list(values)
    values = [sp.cancel(entry / content) for entry in values]
    first = next(entry for entry in values if entry != 0)
    leading = sp.Poly(first, *coordinates).LC()
    return tuple(sp.expand(entry / leading) for entry in values)


def _derivative(matrix: sp.MatrixBase, alpha, coordinates):
    result = matrix
    for coordinate, order in zip(coordinates, alpha, strict=True):
        result = result.diff(coordinate, order)
    return result


def _commutator_coefficients(
    problem: PolynomialProblem,
    direction: tuple[sp.Expr, ...],
    internal: sp.Matrix,
):
    coefficients: dict[tuple[int, ...], sp.Matrix] = {}
    zero = (0,) * len(problem.coordinates)
    for term in problem.operator_terms:
        alpha, coefficient = term.derivative, term.coefficient
        residual = internal * coefficient - coefficient * internal
        residual -= sum(
            (
                direction[index] * coefficient.diff(coordinate)
                for index, coordinate in enumerate(problem.coordinates)
            ),
            sp.zeros(*coefficient.shape),
        )
        coefficients[alpha] = coefficients.get(alpha, sp.zeros(*coefficient.shape)) + residual
        for delta in product(*(range(order + 1) for order in alpha)):
            if delta == zero:
                continue
            differentiated = tuple(
                _derivative(component, delta, problem.coordinates) for component in direction
            )
            factor = sp.prod(comb(order, used) for order, used in zip(alpha, delta, strict=True))
            for index, value in enumerate(differentiated):
                gamma = tuple(
                    order - used + int(index == other)
                    for other, (order, used) in enumerate(zip(alpha, delta, strict=True))
                )
                coefficients[gamma] = (
                    coefficients.get(gamma, sp.zeros(*coefficient.shape))
                    + factor * coefficient * value
                )
    return {alpha: matrix.applyfunc(sp.expand) for alpha, matrix in coefficients.items()}


def _lift_kernel(problem: PolynomialProblem, direction: tuple[sp.Expr, ...]):
    lam, a, b, c = sp.symbols("lambda a b c", real=True)
    internal = sp.Matrix([[0, -a, -b], [a, 0, -c], [b, c, 0]])
    residuals = _commutator_coefficients(
        problem, tuple(lam * value for value in direction), internal
    )
    equations = []
    for matrix in residuals.values():
        for entry in matrix:
            equations.extend(sp.Poly(entry, *problem.coordinates).coeffs())
    linear, _ = sp.linear_eq_to_matrix(equations, (lam, a, b, c))
    return linear.nullspace()


def _scalar_broken_rotation() -> dict[str, object]:
    value = _payload("polynomial-active-variable.json")
    value["operator_terms"][0]["coefficient"]["terms"].append(
        {"powers": [1, 0], "matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]}
    )
    return value


def _rank_two_preparation() -> dict[str, object]:
    value = _payload("polynomial-active-variable.json")
    value["operator_terms"] = value["operator_terms"][1:]
    value["preparation"] = {
        "terms": [
            {"powers": [0, 0], "vector": [1, 0, 0]},
            {"powers": [1, 0], "vector": [0, 1, 0]},
            {"powers": [0, 1], "vector": [0, 0, 1]},
        ]
    }
    value["base_point"] = ["0", "0"]
    value["region"] = [["-1", "1"], ["-1", "1"]]
    return value


class ResidualDirectionLiftChecks(unittest.TestCase):
    def test_rotation_residual_constructs_one_line_and_one_lift(self):
        problem = parse(_payload("polynomial-active-variable.json"))
        witness = construct_reduction(problem)
        flat = _first_order_flat(witness, len(problem.coordinates))
        x, y = problem.coordinates

        self.assertEqual(flat.rank(), 1)
        self.assertEqual(_primitive_line(flat, problem.coordinates), (y, -x))
        self.assertEqual(
            _lift_kernel(problem, (y, -x)),
            [sp.Matrix([-1, 0, 0, 1])],
        )

    def test_variable_reduced_gauge_preserves_the_direction_line(self):
        problem = parse(_payload("polynomial-active-variable.json"))
        witness = construct_reduction(problem)
        flat = _first_order_flat(witness, 2)
        x, _ = problem.coordinates
        gauge = sp.Matrix([[1, x], [0, 1]])
        transformed = sp.Matrix.hstack(
            *[
                witness.residual_coefficients[alpha].numerator.multiply(gauge).reshape(6, 1)
                for alpha in ((1, 0), (0, 1))
            ]
        )

        self.assertEqual(flat.rref()[0], transformed.rref()[0])

    def test_same_direction_can_fail_the_full_operator_lift(self):
        problem = parse(_scalar_broken_rotation())
        flat = _first_order_flat(construct_reduction(problem), 2)
        x, y = problem.coordinates

        self.assertEqual(flat.rank(), 1)
        self.assertEqual(_primitive_line(flat, problem.coordinates), (y, -x))
        self.assertEqual(_lift_kernel(problem, (y, -x)), [])

    def test_rank_two_leakage_has_no_common_direction_line(self):
        problem = parse(_rank_two_preparation())
        flat = _first_order_flat(construct_reduction(problem), 2)

        self.assertEqual(flat.rank(), 2)

    def test_zero_order_escape_does_not_invent_a_direction(self):
        value = _payload("polynomial-active-escape.json")
        value["requested_capability"] = "decompose-with-residual"
        problem = parse(value)
        witness = construct_reduction(problem)

        self.assertEqual(_first_order_flat(witness, 1).rank(), 0)
        self.assertTrue(_nonzero(witness.residual_coefficients[(0,)].numerator))


if __name__ == "__main__":
    unittest.main()

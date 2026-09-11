"""Construction laws for the G20 residual-line Lie lift."""

from __future__ import annotations

import copy
import json
import unittest
from dataclasses import replace
from pathlib import Path

import sympy as sp

from linear_defect_compiler import DefectBudget
from polynomial_active_module import RationalMatrix, construct_reduction
from polynomial_active_module_input import parse
from polynomial_residual_lie import (
    ResidualLieError,
    commutator_coefficients,
    construct_direction,
    construct_lift,
)

HERE = Path(__file__).resolve().parent


def payload(name: str = "polynomial-active-variable.json") -> dict[str, object]:
    return json.loads((HERE / "examples" / name).read_text(encoding="utf-8"))


def problem_and_witness(value=None):
    problem = parse(value or payload())
    return problem, construct_reduction(problem)


def rank_two_payload():
    value = payload()
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


class PolynomialResidualLieTests(unittest.TestCase):
    def test_real_rank_one_direction_and_full_lift_are_constructed(self) -> None:
        problem, reduction = problem_and_witness()

        result = construct_lift(problem, reduction, DefectBudget(10, 100))

        self.assertEqual(result.direction.vector, (problem.coordinates[1], -problem.coordinates[0]))
        self.assertEqual(
            result.internal_generator,
            sp.ImmutableMatrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]]),
        )
        self.assertEqual(result.candidate_coordinates[0], 1)
        self.assertEqual(len(result.internal_ambiguity), 1)
        self.assertEqual(result.internal_ambiguity[0], sp.I * sp.eye(3))
        self.assertTrue(all(result.checks.values()))

    def test_direction_is_invariant_under_reduced_gauge(self) -> None:
        problem, reduction = problem_and_witness()
        x, _ = problem.coordinates
        gauge = sp.ImmutableMatrix([[1, x], [0, 1]])
        residuals = {
            alpha: RationalMatrix(sp.ImmutableMatrix(value.numerator * gauge), value.denominator)
            for alpha, value in reduction.residual_coefficients.items()
        }

        transformed = construct_direction(
            replace(reduction, residual_coefficients=residuals), problem.coordinates
        )

        self.assertEqual(
            transformed.vector, construct_direction(reduction, problem.coordinates).vector
        )
        self.assertTrue(transformed.checks["normal_factor_reconstructs"])

        carrier = sp.ImmutableMatrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
        carrier_residuals = {
            alpha: RationalMatrix(sp.ImmutableMatrix(carrier * value.numerator), value.denominator)
            for alpha, value in reduction.residual_coefficients.items()
        }
        carrier_direction = construct_direction(
            replace(reduction, residual_coefficients=carrier_residuals), problem.coordinates
        )
        self.assertEqual(carrier_direction.vector, transformed.vector)

        affine_residuals = dict(reduction.residual_coefficients)
        affine_residuals[(1, 0)] = RationalMatrix(
            sp.ImmutableMatrix(2 * affine_residuals[(1, 0)].numerator),
            affine_residuals[(1, 0)].denominator,
        )
        affine_residuals[(0, 1)] = RationalMatrix(
            sp.ImmutableMatrix(3 * affine_residuals[(0, 1)].numerator),
            affine_residuals[(0, 1)].denominator,
        )
        affine_direction = construct_direction(
            replace(reduction, residual_coefficients=affine_residuals), problem.coordinates
        )
        self.assertEqual(affine_direction.vector, (problem.coordinates[1], -3 * x / 2))

    def test_higher_rank_complex_and_higher_order_residuals_are_distinct(self) -> None:
        problem, reduction = problem_and_witness(rank_two_payload())
        with self.assertRaises(ResidualLieError) as caught:
            construct_direction(reduction, problem.coordinates)
        self.assertEqual(caught.exception.kind, "ResidualNotLineGenerated")

        problem, reduction = problem_and_witness()
        shape = (reduction.ambient_dimension, reduction.active_dimension)
        first = sp.zeros(*shape)
        first[0, 0] = 1
        imaginary = sp.zeros(*shape)
        imaginary[0, 0] = sp.I
        complex_residuals = {
            (1, 0): RationalMatrix(sp.ImmutableMatrix(first), sp.S.One),
            (0, 1): RationalMatrix(sp.ImmutableMatrix(imaginary), sp.S.One),
        }
        with self.assertRaises(ResidualLieError) as caught:
            construct_direction(
                replace(reduction, residual_coefficients=complex_residuals), problem.coordinates
            )
        self.assertEqual(caught.exception.kind, "ComplexDirectionNoRealForm")

        higher_residuals = {
            (2, 0): RationalMatrix(sp.ImmutableMatrix(first), sp.S.One),
        }
        with self.assertRaises(ResidualLieError) as caught:
            construct_direction(
                replace(reduction, residual_coefficients=higher_residuals), problem.coordinates
            )
        self.assertEqual(caught.exception.kind, "HigherOrderResidualNotVectorField")

        phase_residuals = {
            alpha: RationalMatrix(sp.ImmutableMatrix(sp.I * value.numerator), value.denominator)
            for alpha, value in reduction.residual_coefficients.items()
        }
        phase_direction = construct_direction(
            replace(reduction, residual_coefficients=phase_residuals), problem.coordinates
        )
        self.assertEqual(phase_direction.vector, (problem.coordinates[1], -problem.coordinates[0]))

    def test_commutator_formula_matches_direct_operator_composition(self) -> None:
        value = payload()
        value["operator_terms"].append(
            {
                "derivative": [1, 1],
                "coefficient": {
                    "terms": [{"powers": [1, 0], "matrix": [[1, 0, 0], [0, 2, 0], [0, 0, 3]]}]
                },
            }
        )
        problem = parse(value)
        x, y = problem.coordinates
        direction = (y + x**2, -x + x * y)
        internal = sp.ImmutableMatrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]])
        probe = sp.Matrix([1 + x**2 * y, x * y**2, y + x**3])

        def derivative(vector, alpha):
            result = vector
            for coordinate, order in zip(problem.coordinates, alpha, strict=True):
                result = result.diff(coordinate, order)
            return result

        def operator(vector):
            return sum(
                (
                    term.coefficient * derivative(vector, term.derivative)
                    for term in problem.operator_terms
                ),
                sp.zeros(3, 1),
            )

        def generator(vector):
            return (
                sum(
                    (
                        component * vector.diff(coordinate)
                        for component, coordinate in zip(
                            direction, problem.coordinates, strict=True
                        )
                    ),
                    sp.zeros(3, 1),
                )
                - internal * vector
            )

        direct = operator(generator(probe)) - generator(operator(probe))
        coefficients = commutator_coefficients(problem, direction, internal)
        compiled = sum(
            (matrix * derivative(probe, alpha) for alpha, matrix in coefficients.items()),
            sp.zeros(3, 1),
        )
        self.assertTrue(all(sp.expand(value) == 0 for value in direct - compiled))

    def test_direction_without_visible_lift_is_obstructed(self) -> None:
        value = copy.deepcopy(payload())
        value["operator_terms"][0]["coefficient"]["terms"].append(
            {"powers": [1, 0], "matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]}
        )
        problem, reduction = problem_and_witness(value)

        with self.assertRaises(ResidualLieError) as caught:
            construct_lift(problem, reduction, DefectBudget(10, 100))

        self.assertEqual(caught.exception.kind, "NoInfinitesimalLift")

    def test_zero_order_escape_and_resource_bounds_are_typed(self) -> None:
        value = payload("polynomial-active-escape.json")
        value["requested_capability"] = "decompose-with-residual"
        problem, reduction = problem_and_witness(value)
        with self.assertRaises(ResidualLieError) as caught:
            construct_direction(reduction, problem.coordinates)
        self.assertEqual(caught.exception.kind, "NoDirectionalLeakage")

        problem, reduction = problem_and_witness()
        with self.assertRaises(ResidualLieError) as caught:
            construct_lift(problem, reduction, DefectBudget(9, 100))
        self.assertEqual(caught.exception.kind, "CandidateBudgetExceeded")
        with self.assertRaises(ResidualLieError) as caught:
            construct_lift(problem, reduction, DefectBudget(10, 1))
        self.assertEqual(caught.exception.kind, "ResidualBudgetExceeded")

        limited_problem = replace(
            problem,
            budget=replace(problem.budget, maximum_polynomial_terms=1),
        )
        with self.assertRaises(ResidualLieError) as caught:
            construct_lift(limited_problem, reduction, DefectBudget(10, 100))
        self.assertEqual(caught.exception.kind, "PolynomialTermBudgetExceeded")


if __name__ == "__main__":
    unittest.main()

"""Admission boundaries for exact polynomial active-module problems."""

from __future__ import annotations

import copy
import unittest

from polynomial_active_module_input import PolynomialInputError, PolynomialLiftRequest, parse


def problem() -> dict[str, object]:
    budget = {
        "maximum_carrier_dimension": 4,
        "maximum_active_dimension": 3,
        "maximum_derivative_order": 2,
        "maximum_polynomial_terms": 128,
        "maximum_rank_refinements": 4,
        "maximum_output_terms": 2048,
    }
    return {
        "schema": "polynomial-active-module/v1",
        "coordinates": ["x", "y"],
        "operator_terms": [
            {
                "derivative": [0, 0],
                "coefficient": {
                    "terms": [
                        {"powers": [0, 0], "matrix": [[1, 0], [0, 0]]},
                        {"powers": [1, 0], "matrix": [[0, 1], [1, 0]]},
                    ]
                },
            }
        ],
        "preparation": {"terms": [{"powers": [0, 0], "vector": [1, 0]}]},
        "effect": {"terms": [{"powers": [0, 0], "matrix": [[1, 0], [0, 0]]}]},
        "base_point": ["1", "0"],
        "region": [["1/2", "3/2"], ["-1", "1"]],
        "domain": {"core": "compact-supported-smooth", "boundary": "none"},
        "requested_capability": "decompose-with-residual",
        "resource_budget": budget,
    }


class PolynomialActiveModuleInputTests(unittest.TestCase):
    def test_sparse_exact_problem_is_canonical_and_typed(self) -> None:
        result = parse(problem())

        self.assertEqual(tuple(str(item) for item in result.coordinates), ("x", "y"))
        self.assertEqual(result.operator_terms[0].derivative, (0, 0))
        self.assertEqual(str(result.operator_terms[0].coefficient[0, 0]), "1")
        self.assertEqual(str(result.operator_terms[0].coefficient[0, 1]), "x")
        self.assertEqual(str(result.base_point[0]), "1")
        self.assertEqual(result.domain_contract, "C_c^infinity(region; C^n), boundary none")

    def test_inexact_and_domain_inputs_are_distinct_refusals(self) -> None:
        inexact = copy.deepcopy(problem())
        inexact["base_point"][0] = 1.0
        with self.assertRaises(PolynomialInputError) as caught:
            parse(inexact)
        self.assertEqual(caught.exception.kind, "InvalidExactInput")

        boundary = copy.deepcopy(problem())
        boundary["domain"]["boundary"] = "dirichlet"
        with self.assertRaises(PolynomialInputError) as caught:
            parse(boundary)
        self.assertEqual(caught.exception.kind, "DomainContractMismatch")

    def test_shape_region_and_budget_fail_before_construction(self) -> None:
        outside = copy.deepcopy(problem())
        outside["base_point"][0] = "2"
        with self.assertRaises(PolynomialInputError) as caught:
            parse(outside)
        self.assertEqual(caught.exception.kind, "InvalidRegion")

        limited = copy.deepcopy(problem())
        limited["resource_budget"]["maximum_polynomial_terms"] = 1
        with self.assertRaises(PolynomialInputError) as caught:
            parse(limited)
        self.assertEqual(caught.exception.kind, "PolynomialTermBudgetExceeded")

        duplicate = copy.deepcopy(problem())
        duplicate["coordinates"] = ["x", "x"]
        with self.assertRaises(PolynomialInputError) as caught:
            parse(duplicate)
        self.assertEqual(caught.exception.kind, "InvalidCoordinates")

        nonhermitian = copy.deepcopy(problem())
        nonhermitian["effect"]["terms"][0]["matrix"] = [[0, 1], [0, 0]]
        with self.assertRaises(PolynomialInputError) as caught:
            parse(nonhermitian)
        self.assertEqual(caught.exception.kind, "NonHermitianEffect")

    def test_residual_lie_capability_has_a_tagged_nested_budget(self) -> None:
        value = problem()
        value["requested_capability"] = "construct-local-infinitesimal-symmetry"
        value["resource_budget"]["residual_lie"] = {
            "maximum_candidate_dimension": 10,
            "maximum_residual_coordinates": 100,
        }

        result = parse(value)

        self.assertIsInstance(result, PolynomialLiftRequest)
        assert isinstance(result, PolynomialLiftRequest)
        self.assertEqual(result.budget.maximum_candidate_dimension, 10)
        self.assertEqual(result.problem.requested_capability, value["requested_capability"])

    def test_residual_lie_budget_is_required_and_exact(self) -> None:
        value = problem()
        value["requested_capability"] = "construct-local-infinitesimal-symmetry"
        with self.assertRaises(PolynomialInputError) as caught:
            parse(value)
        self.assertEqual(caught.exception.kind, "MissingResidualLieBudget")

        value["resource_budget"]["residual_lie"] = {
            "maximum_candidate_dimension": True,
            "maximum_residual_coordinates": 100,
        }
        with self.assertRaises(PolynomialInputError) as caught:
            parse(value)
        self.assertEqual(caught.exception.kind, "InvalidResidualLieBudget")


if __name__ == "__main__":
    unittest.main()

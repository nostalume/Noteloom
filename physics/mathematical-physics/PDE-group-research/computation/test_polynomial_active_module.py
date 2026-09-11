"""Exact laws and discriminating benches for the G19 constructor."""

from __future__ import annotations

import copy
import unittest
from dataclasses import replace

import sympy as sp

from polynomial_active_module import PolynomialReductionError, construct_reduction
from polynomial_active_module_input import parse
from test_polynomial_active_module_input import problem


def _constant_problem() -> dict[str, object]:
    value = problem()
    value["coordinates"] = ["x"]
    value["operator_terms"] = [
        {
            "derivative": [2],
            "coefficient": {"terms": [{"powers": [0], "matrix": [[-1, 0], [0, -1]]}]},
        },
        {
            "derivative": [0],
            "coefficient": {"terms": [{"powers": [0], "matrix": [[1, 0], [0, 2]]}]},
        },
    ]
    value["preparation"] = {"terms": [{"powers": [0], "vector": [1, 0]}]}
    value["effect"] = {"terms": [{"powers": [0], "matrix": [[1, 0], [0, 0]]}]}
    value["base_point"] = ["0"]
    value["region"] = [["-1", "1"]]
    return value


def _variable_problem() -> dict[str, object]:
    value = problem()
    h_terms = [
        {"powers": [0, 0], "matrix": [[1, 0, 0], [0, 0, 0], [0, 0, 0]]},
        {"powers": [1, 0], "matrix": [[0, 1, 0], [1, 0, 0], [0, 0, 0]]},
        {"powers": [0, 1], "matrix": [[0, 0, 1], [0, 0, 0], [1, 0, 0]]},
        {"powers": [2, 0], "matrix": [[0, 0, 0], [0, 1, 0], [0, 0, 0]]},
        {"powers": [1, 1], "matrix": [[0, 0, 0], [0, 0, 1], [0, 1, 0]]},
        {"powers": [0, 2], "matrix": [[0, 0, 0], [0, 0, 0], [0, 0, 1]]},
    ]
    value["operator_terms"] = [
        {"derivative": [0, 0], "coefficient": {"terms": h_terms}},
        {
            "derivative": [2, 0],
            "coefficient": {
                "terms": [{"powers": [0, 0], "matrix": [[-1, 0, 0], [0, -1, 0], [0, 0, -1]]}]
            },
        },
        {
            "derivative": [0, 2],
            "coefficient": {
                "terms": [{"powers": [0, 0], "matrix": [[-1, 0, 0], [0, -1, 0], [0, 0, -1]]}]
            },
        },
    ]
    value["preparation"] = {"terms": [{"powers": [0, 0], "vector": [1, 0, 0]}]}
    value["effect"] = {"terms": [{"powers": [0, 0], "matrix": [[1, 0, 0], [0, 0, 0], [0, 0, 0]]}]}
    value["resource_budget"]["maximum_carrier_dimension"] = 3
    value["resource_budget"]["maximum_active_dimension"] = 3
    value["resource_budget"]["maximum_polynomial_terms"] = 512
    return value


class PolynomialActiveModuleTests(unittest.TestCase):
    def test_constant_family_recovers_exact_closed_reduction(self) -> None:
        result = construct_reduction(parse(_constant_problem()))

        self.assertEqual(result.active_dimension, 1)
        self.assertTrue(result.leakage_is_zero)
        self.assertEqual(result.frame, sp.ImmutableMatrix([[1], [0]]))
        self.assertTrue(all(result.checks.values()))

    def test_nonpauli_variable_module_reports_product_rule_leakage(self) -> None:
        result = construct_reduction(parse(_variable_problem()))
        x, y = sorted(result.frame.free_symbols, key=str)

        self.assertEqual(result.active_dimension, 2)
        self.assertEqual(result.frame, sp.ImmutableMatrix([[1, 0], [0, x], [0, y]]))
        self.assertFalse(result.leakage_is_zero)
        self.assertGreater(result.cost.product_rule_summands, 0)
        self.assertTrue(all(result.checks.values()))

    def test_coefficient_escape_does_not_enlarge_provenance(self) -> None:
        value = _constant_problem()
        value["operator_terms"] = [
            {
                "derivative": [0],
                "coefficient": {
                    "terms": [
                        {"powers": [0], "matrix": [[0, 1, 0], [1, 0, 0], [0, 0, 0]]},
                        {"powers": [1], "matrix": [[0, 0, 0], [0, 0, 1], [0, 1, 0]]},
                    ]
                },
            }
        ]
        value["preparation"] = {"terms": [{"powers": [0], "vector": [1, 0, 0]}]}
        value["effect"] = {"terms": [{"powers": [0], "matrix": [[1, 0, 0], [0, 0, 0], [0, 0, 0]]}]}
        value["resource_budget"]["maximum_carrier_dimension"] = 3
        admitted = parse(value)
        result = construct_reduction(admitted)

        self.assertEqual(result.active_dimension, 2)
        self.assertEqual(len(result.provenance), 2)
        self.assertFalse(result.leakage_is_zero)
        x = admitted.coordinates[0]
        self.assertEqual(
            result.residual_coefficients[(0,)].numerator,
            sp.ImmutableMatrix([[0, 0], [0, 0], [0, x]]),
        )

    def test_exhausted_rank_enclosure_is_unresolved_not_jump(self) -> None:
        value = _constant_problem()
        value["operator_terms"] = [
            {
                "derivative": [0],
                "coefficient": {
                    "terms": [
                        {"powers": [0], "matrix": [[0, 1], [1, 0]]},
                        {"powers": [1], "matrix": [[0, -4], [-4, 0]]},
                    ]
                },
            }
        ]
        value["region"] = [["-1/2", "1/2"]]
        value["resource_budget"]["maximum_rank_refinements"] = 1

        with self.assertRaises(PolynomialReductionError) as caught:
            construct_reduction(parse(value))
        self.assertEqual(caught.exception.kind, "RankRegionUnresolved")
        self.assertNotIn("jump", str(caught.exception).lower())

    def test_exact_closed_request_does_not_change_math_witness(self) -> None:
        value = _variable_problem()
        value["requested_capability"] = "exact-closed-reduction"
        result = construct_reduction(parse(copy.deepcopy(value)))
        self.assertFalse(result.leakage_is_zero)

    def test_constant_unitary_carrier_change_preserves_constructed_identity(self) -> None:
        original = parse(_variable_problem())
        unitary = sp.ImmutableMatrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
        transformed = replace(
            original,
            operator_terms=tuple(
                replace(term, coefficient=unitary * term.coefficient * unitary.T)
                for term in original.operator_terms
            ),
            preparation=unitary * original.preparation,
            effect=unitary * original.effect * unitary.T,
        )

        left, right = construct_reduction(original), construct_reduction(transformed)
        self.assertEqual(right.frame, unitary * left.frame)
        self.assertEqual(right.active_dimension, left.active_dimension)
        self.assertEqual(right.leakage_is_zero, left.leakage_is_zero)
        self.assertTrue(all(right.checks.values()))


if __name__ == "__main__":
    unittest.main()

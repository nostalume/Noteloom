from __future__ import annotations

import unittest
from pathlib import Path

from natural_tensor_stabilizer import discover_payload, discover_problem
from problem_router import discover_problem as discover_routed_problem

HERE = Path(__file__).resolve().parent
EXAMPLES = HERE / "examples"


class NaturalTensorStabilizerTests(unittest.TestCase):
    def test_generic_problem_router_admits_the_frozen_transfer_schema(self) -> None:
        result = discover_routed_problem(EXAMPLES / "natural-tensor-elasticity.json")

        self.assertEqual(result["outcome"], "controlled")
        self.assertEqual(result["decision"]["selected_route"], "natural-tensor-structured-seed")

    def test_isotropic_elasticity_constructs_stabilizer_and_wave_channels(self) -> None:
        result = discover_problem(EXAMPLES / "natural-tensor-elasticity.json")

        self.assertEqual(result["outcome"], "controlled")
        decision = result["decision"]
        self.assertEqual(decision["candidate_dimension"], 3)
        self.assertEqual(decision["raw_candidate_dimension"], 9)
        self.assertEqual(decision["stabilizer_dimension"], 3)
        self.assertEqual(decision["stabilizer_closure"], "closed")
        self.assertEqual(decision["tensor_rank_drops"], [0])
        self.assertEqual(decision["structured_target_dimensions"], [21])
        self.assertEqual(decision["raw_target_dimensions"], [9, 81])
        self.assertEqual(result["coincidence"]["generator_spans"], "exact_equal")
        relation_plan = result["relation_plan"]
        self.assertEqual(
            relation_plan["execution_policy"],
            "selected-plus-explicit-raw-span-audit",
        )
        self.assertEqual(relation_plan["selected_route"], "natural-tensor-structured-seed")
        self.assertEqual(
            [operation["rule"] for operation in relation_plan["selected_operations"]],
            [
                "metric-kernel",
                "compositional-quotient",
                "simultaneous-defect-kernel",
                "visible-quotient",
                "bracket-closure",
            ],
        )
        self.assertEqual(
            [fact["permutation_generator_count"] for fact in relation_plan["facts"]],
            [1, 3],
        )
        self.assertEqual(
            relation_plan["materialized_routes"],
            ["natural-tensor-structured-seed", "natural-tensor-raw-endomorphism"],
        )
        structured_plan = relation_plan["routes"][1]
        self.assertEqual(structured_plan["planning_cost"], 21)
        self.assertEqual(structured_plan["estimated_total_cost"], 138)
        self.assertEqual(
            result["coincidence"]["quotient_coordinates"], "exact_equal_to_orbit_audit"
        )
        self.assertEqual(result["coincidence"]["quotient_audit_checks"], 648)
        use = result["use_witness"]
        self.assertEqual(use["channel_dimensions"], {"transverse": 2, "longitudinal": 1})
        self.assertEqual(use["eigenvalues"], {"transverse": "9", "longitudinal": "27"})
        self.assertTrue(use["exact_projector_checks_passed"])
        self.assertLessEqual(use["observable_error"], use["tolerance"])
        self.assertEqual(use["cost"]["one_time_stabilizer_proxy"], 117)
        self.assertEqual(use["cost"]["one_time_relation_planning_proxy"], 21)
        self.assertEqual(use["cost"]["one_time_selected_route_proxy"], 138)
        self.assertEqual(use["cost"]["stabilizer_only_break_even_query_count"], 8)
        self.assertEqual(use["cost"]["break_even_query_count"], 9)

    def test_axis_tensor_reduces_the_same_seed_to_one_generator(self) -> None:
        result = discover_problem(EXAMPLES / "natural-tensor-elasticity-axis.json")

        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["stabilizer_dimension"], 1)
        self.assertEqual(result["decision"]["tensor_rank_drops"], [0, 2])
        self.assertEqual(result["coincidence"]["generator_spans"], "exact_equal")

    def test_structured_seed_succeeds_when_raw_candidate_budget_is_too_small(self) -> None:
        result = discover_problem(EXAMPLES / "natural-tensor-elasticity-small-budget.json")

        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["candidate_dimension"], 3)
        routes = {candidate["route"]: candidate["outcome"] for candidate in result["candidates"]}
        self.assertEqual(routes["natural-tensor-raw-endomorphism"], "unresolved")
        self.assertEqual(routes["natural-tensor-structured-seed"], "exact")
        self.assertEqual(
            result["relation_plan"]["execution_policy"],
            "selected-route-only-after-symbolic-admission",
        )
        self.assertEqual(
            result["relation_plan"]["materialized_routes"],
            ["natural-tensor-structured-seed"],
        )

    def test_budget_below_structured_seed_is_not_false_no_symmetry(self) -> None:
        result = discover_problem(
            EXAMPLES / "natural-tensor-elasticity-structured-small-budget.json"
        )

        self.assertEqual(result["outcome"], "unresolved")
        self.assertEqual(result["obstruction"]["kind"], "CandidateBudgetExceeded")
        self.assertEqual(result["relation_plan"]["materialized_routes"], [])

    def test_metric_seed_does_not_require_an_orthonormal_input_basis(self) -> None:
        result = discover_payload(
            {
                "schema": "natural-tensor-stabilizer/v1",
                "dimension": 3,
                "tensors": [
                    {
                        "kind": "metric",
                        "matrix": [[2, 0, 0], [0, 3, 0], [0, 0, 5]],
                    },
                    {"kind": "isotropic_elasticity", "lambda": 1, "mu": 1},
                ],
                "resource_budget": {
                    "maximum_candidate_dimension": 9,
                    "maximum_residual_coordinates": 90,
                    "maximum_bracket_checks": 1200,
                },
                "audit_raw_comparison": True,
            }
        )

        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["candidate_dimension"], 3)
        self.assertEqual(result["coincidence"]["generator_spans"], "exact_equal")


if __name__ == "__main__":
    unittest.main()

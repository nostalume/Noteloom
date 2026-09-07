from __future__ import annotations

import unittest
from pathlib import Path

from problem_router import discover_problem

EXAMPLES = Path(__file__).resolve().parent / "examples"


class CoupledRelationStabilizerTests(unittest.TestCase):
    def test_rank_three_link_constructs_effective_covariance_algebra_and_projectors(self) -> None:
        result = discover_problem(EXAMPLES / "coupled-carrier-clifford-r3.json")

        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["selected_route"], "coupled-relation-kernel")
        witness = result["candidates"][0]["witness"]
        self.assertEqual(witness["dimensions"]["candidate"], 13)
        self.assertEqual(witness["dimensions"]["kernel"], 4)
        self.assertEqual(witness["dimensions"]["ineffective"], 1)
        self.assertEqual(witness["dimensions"]["effective"], 3)
        self.assertEqual(witness["closure"], "closed")
        self.assertEqual(len(witness["generators"]["effective"]), 3)
        self.assertEqual(len(witness["generators"]["ineffective"]), 1)
        self.assertTrue(
            all(
                entry == "0"
                for row in witness["generators"]["ineffective"][0]["base"]
                for entry in row
            )
        )
        self.assertEqual(witness["human_compression"]["relation_law_count"], 2)
        self.assertTrue(all(witness["relations"]["clifford_checks"].values()))
        self.assertTrue(all(witness["use"]["checks"].values()))
        self.assertEqual(witness["use"]["norm"], "3")

    def test_rank_two_link_transfers_without_changing_the_constructor(self) -> None:
        result = discover_problem(EXAMPLES / "coupled-carrier-clifford-r2.json")

        self.assertEqual(result["outcome"], "exact")
        witness = result["candidates"][0]["witness"]
        self.assertEqual(witness["dimensions"]["candidate"], 8)
        self.assertEqual(witness["dimensions"]["kernel"], 2)
        self.assertEqual(witness["dimensions"]["ineffective"], 1)
        self.assertEqual(witness["dimensions"]["effective"], 1)
        self.assertTrue(all(witness["use"]["checks"].values()))
        self.assertEqual(witness["use"]["norm"], "5")

    def test_requested_clifford_capability_refuses_a_broken_link(self) -> None:
        result = discover_problem(EXAMPLES / "coupled-carrier-clifford-broken.json")

        self.assertEqual(result["outcome"], "obstructed")
        self.assertEqual(result["obstruction"]["kind"], "CliffordRelationViolation")
        self.assertIsNone(result["decision"]["selected_route"])

    def test_candidate_budget_refuses_before_materialization(self) -> None:
        result = discover_problem(EXAMPLES / "coupled-carrier-clifford-small-budget.json")

        self.assertEqual(result["outcome"], "unresolved")
        self.assertEqual(result["obstruction"]["kind"], "CandidateBudgetExceeded")
        self.assertFalse(result["planning"]["materialized"])
        self.assertEqual(result["planning"]["candidate_dimension"], 13)


if __name__ == "__main__":
    unittest.main()

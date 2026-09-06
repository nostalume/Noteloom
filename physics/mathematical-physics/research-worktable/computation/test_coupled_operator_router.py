from __future__ import annotations

import unittest
from pathlib import Path

from problem_router import discover_problem

EXAMPLES = Path(__file__).resolve().parent / "examples"


class CoupledOperatorRouterTests(unittest.TestCase):
    def test_operator_covariance_is_available_without_a_pauli_observable(self) -> None:
        result = discover_problem(EXAMPLES / "coupled-operator-covariance-only.json")

        self.assertEqual(result["outcome"], "exact")
        witness = result["candidates"][0]["witness"]
        self.assertEqual(witness["operator_stage"]["dimensions"]["effective"], 1)
        self.assertIsNone(witness["use"])
        self.assertIsNone(result["request"]["observable"])
        self.assertEqual(result["decision"]["common_transverse_channels"], [])
        self.assertIsNone(result["decision"]["curvature_aligned_projector"])

    def test_generated_action_lifts_through_every_operator_layer(self) -> None:
        result = discover_problem(EXAMPLES / "coupled-pauli-operator-positive.json")
        baseline = discover_problem(EXAMPLES / "pauli-landau-positive.json")

        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["selected_route"], "coupled-full-operator-kernel")
        witness = result["candidates"][0]["witness"]
        self.assertEqual(witness["relation_stage"]["effective_dimension"], 3)
        self.assertEqual(
            witness["operator_stage"]["dimensions"], {"candidate": 3, "kernel": 1, "effective": 1}
        )
        ledger = witness["operator_stage"]["defect_ledger"]
        self.assertEqual(
            [(entry["name"], entry["rank_drop"]) for entry in ledger],
            [
                ("curvature-covariance", 2),
                ("first-order-covariance", 0),
                ("zeroth-order-covariance", 0),
            ],
        )
        self.assertEqual(witness["operator_stage"]["closure"], "closed")
        self.assertTrue(all(witness["domain"]["checks"].values()))
        self.assertTrue(all(witness["use"]["checks"].values()))
        self.assertEqual(
            result["decision"]["common_transverse_channels"],
            baseline["decision"]["common_transverse_channels"],
        )
        self.assertEqual(
            result["decision"]["curvature_aligned_projector"],
            baseline["decision"]["curvature_aligned_projector"],
        )

    def test_charge_reversal_transfers_without_a_preferred_spin_component(self) -> None:
        positive = discover_problem(EXAMPLES / "coupled-pauli-operator-positive.json")
        negative = discover_problem(EXAMPLES / "coupled-pauli-operator-negative.json")
        baseline = discover_problem(EXAMPLES / "pauli-landau-negative.json")

        self.assertEqual(negative["outcome"], "exact")
        self.assertEqual(
            negative["decision"]["common_transverse_channels"],
            positive["decision"]["common_transverse_channels"],
        )
        self.assertNotEqual(
            negative["decision"]["curvature_aligned_projector"],
            positive["decision"]["curvature_aligned_projector"],
        )
        self.assertEqual(
            negative["decision"]["curvature_aligned_projector"],
            baseline["decision"]["curvature_aligned_projector"],
        )

    def test_incompatible_zero_order_term_kills_the_constructed_action(self) -> None:
        result = discover_problem(EXAMPLES / "coupled-pauli-operator-broken-lower.json")

        self.assertEqual(result["outcome"], "obstructed")
        self.assertEqual(result["obstruction"]["kind"], "NoEffectiveOperatorSymmetry")
        self.assertEqual(result["probes"][0]["first_residual"], "zeroth-order-covariance")
        self.assertIsNone(result["decision"]["selected_route"])

    def test_unmatched_domain_contract_refuses_analytic_promotion(self) -> None:
        result = discover_problem(EXAMPLES / "coupled-pauli-operator-wrong-domain.json")

        self.assertEqual(result["outcome"], "obstructed")
        self.assertEqual(result["obstruction"]["kind"], "DomainContractMismatch")
        self.assertIsNone(result["decision"]["selected_route"])


if __name__ == "__main__":
    unittest.main()

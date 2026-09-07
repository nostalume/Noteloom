from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path

from problem_router import discover_problem

EXAMPLES = Path(__file__).resolve().parent / "examples"


class CoupledOperatorRouterTests(unittest.TestCase):
    def test_nonzero_longitudinal_drift_is_recovered_exactly(self) -> None:
        result = discover_problem(EXAMPLES / "coupled-pauli-operator-longitudinal-drift.json")

        self.assertEqual(result["outcome"], "exact")
        witness = result["candidates"][0]["witness"]
        self.assertEqual(witness["operator_stage"]["dimensions"]["effective"], 1)
        self.assertEqual(
            [
                (entry["name"], entry["rank_drop"])
                for entry in witness["operator_stage"]["defect_ledger"]
            ],
            [
                ("curvature-covariance", 2),
                ("first-order-covariance", 0),
                ("zeroth-order-covariance", 0),
            ],
        )
        use = witness["use"]
        self.assertEqual(use["parallel_axis"], ["0", "0", "1"])
        self.assertEqual(
            use["longitudinal_transport"],
            {"linear_coefficient": "2", "momentum_shift": "1", "energy_shift": "-1"},
        )
        first = use["transport_channels"][0]
        self.assertEqual(
            first["energy_polynomial"], {"quadratic": "1", "linear": "2", "constant": "0"}
        )
        self.assertEqual(first["completed_square_constant"], "-1")
        self.assertEqual(
            result["decision"]["longitudinal_transport_channels"], use["transport_channels"]
        )
        momentum = Fraction(5, 2)
        polynomial = momentum**2 + Fraction(2) * momentum
        completed = (momentum + Fraction(1)) ** 2 + Fraction(-1)
        self.assertEqual(polynomial, completed)

    def test_rotated_field_transfers_without_a_preferred_axis(self) -> None:
        axial = discover_problem(EXAMPLES / "coupled-pauli-operator-longitudinal-drift.json")
        rotated = discover_problem(EXAMPLES / "coupled-pauli-operator-rotated-drift.json")

        self.assertEqual(rotated["outcome"], "exact")
        use = rotated["candidates"][0]["witness"]["use"]
        self.assertEqual(use["parallel_axis"], ["1", "0", "0"])
        self.assertEqual(
            use["longitudinal_transport"],
            axial["candidates"][0]["witness"]["use"]["longitudinal_transport"],
        )
        self.assertEqual(
            rotated["decision"]["common_transverse_channels"],
            axial["decision"]["common_transverse_channels"],
        )

    def test_transverse_drift_is_removed_by_the_generic_first_order_defect(self) -> None:
        result = discover_problem(EXAMPLES / "coupled-pauli-operator-transverse-drift.json")

        self.assertEqual(result["outcome"], "obstructed")
        self.assertEqual(result["obstruction"]["kind"], "NoEffectiveOperatorSymmetry")
        self.assertEqual(result["probes"][0]["first_residual"], "first-order-covariance")

    def test_matrix_valued_axial_drift_constructs_a_two_sector_coefficient_algebra(self) -> None:
        result = discover_problem(EXAMPLES / "coupled-pauli-operator-matrix-drift.json")

        self.assertEqual(result["outcome"], "exact")
        use = result["candidates"][0]["witness"]["use"]
        algebra = use["coefficient_algebra"]
        self.assertEqual(algebra["dimension"], 2)
        self.assertEqual(algebra["basis"], ["I", "Sigma_F"])
        self.assertEqual(algebra["coefficient_coordinates"], {"identity": "0", "grading": "2"})
        self.assertEqual(
            algebra["sector_eigenvalues"], {"curvature_aligned": "2", "curvature_antialigned": "-2"}
        )
        self.assertEqual(algebra["minimal_polynomial"], ["-4", "0", "1"])
        self.assertEqual(algebra["projectors_from_coefficient"], use["projectors"])
        self.assertEqual(
            use["longitudinal_transport"],
            {
                "sector_linear_coefficients": {
                    "curvature_aligned": "2",
                    "curvature_antialigned": "-2",
                }
            },
        )
        self.assertEqual(
            [channel["energy"] for channel in use["transport_channels"]],
            ["k^2+2*k+0", "k^2-2*k+6", "k^2+2*k+6", "k^2-2*k+12"],
        )

    def test_rotated_matrix_transport_preserves_the_abstract_algebra_and_channels(self) -> None:
        axial = discover_problem(EXAMPLES / "coupled-pauli-operator-matrix-drift.json")
        rotated = discover_problem(EXAMPLES / "coupled-pauli-operator-rotated-matrix-drift.json")

        self.assertEqual(rotated["outcome"], "exact")
        axial_use = axial["candidates"][0]["witness"]["use"]
        rotated_use = rotated["candidates"][0]["witness"]["use"]
        self.assertEqual(rotated_use["parallel_axis"], ["1", "0", "0"])
        self.assertEqual(
            rotated_use["coefficient_algebra"]["minimal_polynomial"],
            axial_use["coefficient_algebra"]["minimal_polynomial"],
        )
        self.assertEqual(rotated_use["transport_channels"], axial_use["transport_channels"])
        self.assertNotEqual(rotated_use["projectors"], axial_use["projectors"])

    def test_operator_covariance_is_available_without_a_pauli_observable(self) -> None:
        result = discover_problem(EXAMPLES / "coupled-operator-covariance-only.json")

        self.assertEqual(result["outcome"], "exact")
        witness = result["candidates"][0]["witness"]
        self.assertEqual(witness["operator_stage"]["dimensions"]["effective"], 1)
        self.assertIsNone(witness["use"])
        self.assertEqual(witness["maps"], {"analysis": None, "synthesis": None})
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

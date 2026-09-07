import subprocess
import sys
import unittest
from pathlib import Path

from singular_interbasis_probe import build_interbasis_probe

HERE = Path(__file__).resolve().parent
INPUT = HERE / "examples" / "singular-isotropic-e2.json"
TRANSFER_INPUT = HERE / "examples" / "singular-isotropic-transfer-e2.json"
FREQUENCY_TRANSFER_INPUT = HERE / "examples" / "singular-isotropic-frequency-transfer-e2.json"


class SingularInterbasisProbeTests(unittest.TestCase):
    def test_every_certified_level_has_exact_route_coincidence(self):
        for level in range(5):
            with self.subTest(level=level):
                result = build_interbasis_probe(INPUT, level=level)
                self.assertEqual(result["status"], "ExactInterbasisCoincidence")
                self.assertTrue(all(result["coincidence_checks"].values()))

    def test_independent_routes_construct_the_same_jacobi_operator(self):
        result = build_interbasis_probe(INPUT, level=2)

        self.assertEqual(result["status"], "ExactInterbasisCoincidence")
        self.assertEqual(result["level"], 2)
        self.assertTrue(all(result["coincidence_checks"].values()))
        self.assertEqual(
            result["polynomial_route"]["jacobi_data"],
            result["factor_enveloping_route"]["jacobi_data"],
        )
        self.assertEqual(result["polynomial_route"]["A_spectrum"], ["17/2", "41/2", "73/2"])

    def test_overlap_probabilities_are_normalized_and_exact(self):
        result = build_interbasis_probe(INPUT, level=1)

        expected = [["7/12", "5/12"], ["5/12", "7/12"]]
        self.assertEqual(result["observable"]["transition_probabilities"], expected)
        self.assertTrue(result["observable"]["row_sums_one"])
        self.assertTrue(result["observable"]["column_sums_one"])

    def test_same_interface_transfers_to_different_indicial_weights(self):
        result = build_interbasis_probe(TRANSFER_INPUT, level=2)

        self.assertEqual(result["status"], "ExactInterbasisCoincidence")
        self.assertEqual(
            result["factor_enveloping_route"]["factor_labels"], {"k_x": "3/2", "k_y": "2"}
        )
        self.assertEqual(
            result["factor_enveloping_route"]["A_spectrum"], ["47/4", "103/4", "175/4"]
        )
        self.assertTrue(all(result["coincidence_checks"].values()))

    def test_same_interface_is_covariant_under_frequency_rescaling(self):
        result = build_interbasis_probe(FREQUENCY_TRANSFER_INPUT, level=2)

        self.assertEqual(result["status"], "ExactInterbasisCoincidence")
        self.assertEqual(result["factor_enveloping_route"]["energy"], "20")
        self.assertEqual(
            result["factor_enveloping_route"]["jacobi_data"]["B_eigenvalues"],
            ["5", "9", "13"],
        )
        self.assertTrue(all(result["coincidence_checks"].values()))

    def test_cost_audit_retains_both_non_dominating_routes(self):
        result = build_interbasis_probe(INPUT, level=2)

        self.assertEqual(result["route_evaluation"]["decision"], "ParetoRetainBoth")
        self.assertIn("parent Lie", result["route_evaluation"]["factor_distinct_capability"])
        self.assertIn(
            "relative-complete", result["route_evaluation"]["polynomial_distinct_capability"]
        )

    def test_level_outside_the_certified_representation_budget_is_refused(self):
        result = build_interbasis_probe(INPUT, level=5)

        self.assertEqual(result["status"], "Refused")
        self.assertIn("between 0 and 4", result["reason"])

    def test_cli_reports_level_and_coincidence(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(HERE / "singular_interbasis_probe.py"),
                str(INPUT),
                "--level",
                "2",
                "--summary",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0)
        self.assertIn("N=2", completed.stdout)
        self.assertIn("3 x 3 overlap probabilities", completed.stdout)
        self.assertIn("ParetoRetainBoth", completed.stdout)


if __name__ == "__main__":
    unittest.main()

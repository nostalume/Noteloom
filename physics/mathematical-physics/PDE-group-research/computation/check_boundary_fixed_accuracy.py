import subprocess
import sys
import unittest
from pathlib import Path

from boundary_fixed_accuracy import build_fixed_accuracy_comparison

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "boundary_fixed_accuracy.py"
BENCHMARK = HERE / "examples" / "disk-fixed-accuracy.json"
UNRESOLVED = HERE / "examples" / "disk-unresolved-accuracy.json"


class BoundaryFixedAccuracyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = build_fixed_accuracy_comparison(BENCHMARK)

    def test_both_routes_recover_the_same_continuum_observable_at_tolerance(self):
        self.assertEqual(self.result["status"], "FixedAccuracyComparison")
        self.assertEqual(len(self.result["continuum_reference"]["eigenvalues"]), 6)
        for route in ("representation_route", "cartesian_sparse_baseline"):
            self.assertTrue(self.result[route]["tolerance_met"])
            self.assertLessEqual(self.result[route]["max_relative_error"], 0.08)
            self.assertLessEqual(self.result[route]["max_relative_residual"], 1e-8)

    def test_sector_frontier_is_constructed_without_using_reference_zeros(self):
        selection = self.result["representation_route"]["sector_selection"]

        self.assertFalse(selection["uses_continuum_reference"])
        self.assertEqual(selection["lower_bound"], "lambda >= m^2")
        self.assertTrue(selection["frontier_certified"])
        self.assertGreaterEqual(selection["maximum_abs_m_constructed"], 2)
        self.assertGreater(
            selection["first_unconstructed_sector_lower_bound"],
            selection["computed_kth_upper_bound"],
        )

    def test_fixed_accuracy_cost_includes_setup_solve_and_recovery(self):
        representation = self.result["representation_route"]
        cartesian = self.result["cartesian_sparse_baseline"]
        audit = self.result["route_evaluation"]

        self.assertIn("assembly_seconds", representation["measured_cost"])
        self.assertIn("solve_seconds", representation["measured_cost"])
        self.assertIn("recovery_seconds", representation["measured_cost"])
        self.assertLess(
            representation["active_degrees_of_freedom"], cartesian["active_degrees_of_freedom"]
        )
        self.assertEqual(audit["decision"], "RepresentationReductionAtTolerance")
        self.assertEqual(
            audit["same_observable"],
            "first 6 continuum Dirichlet-disk eigenvalues with multiplicity",
        )
        self.assertLess(audit["observed_ratios"]["active_unknowns"], 1.0)
        self.assertLess(audit["observed_ratios"]["assembled_nonzeros"], 1.0)

    def test_multiplicity_labels_are_recovered_not_discarded(self):
        labels = self.result["representation_route"]["eigenvalue_labels"]

        self.assertEqual(len(labels), 6)
        self.assertEqual(labels[0]["multiplicity_copy"], 1)
        self.assertTrue(any(label["multiplicity_copy"] == 2 for label in labels))

    def test_unattained_accuracy_is_reported_without_route_selection(self):
        result = build_fixed_accuracy_comparison(UNRESOLVED)

        self.assertEqual(result["status"], "UnresolvedAccuracyWithinBudget")
        self.assertEqual(result["route_evaluation"]["decision"], "NoAccuracyMatchedComparison")

    def test_cli_emits_the_same_machine_readable_contract(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(BENCHMARK), "--summary"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("FixedAccuracyComparison", completed.stdout)
        self.assertIn("RepresentationReductionAtTolerance", completed.stdout)


if __name__ == "__main__":
    unittest.main()

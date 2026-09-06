import subprocess
import sys
import unittest
from pathlib import Path

from warped_axis_quotient_pde import build_warped_axis_comparison

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "warped_axis_quotient_pde.py"
BENCHMARK = HERE / "examples" / "warped-axis-manufactured.json"
CONTROL = HERE / "examples" / "warped-axis-wrong-regularity.json"


class WarpedAxisQuotientPDETests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = build_warped_axis_comparison(BENCHMARK)

    def test_warped_domain_retains_only_axial_rotation(self):
        self.assertEqual(self.result["status"], "StratifiedBoundaryQuotientComparison")
        self.assertEqual(self.result["symmetry_discovery"]["connected_stabilizer"], "SO(2)")
        self.assertTrue(self.result["physical_boundary"]["nonproduct_warp"])

    def test_isotropy_generates_weight_dependent_axis_conditions(self):
        axis = self.result["orbit_stratification"]["fixed_axis"]

        self.assertEqual(axis["isotropy"], "SO(2)")
        self.assertEqual(axis["quotient_role"], "singular boundary stratum")
        self.assertEqual(axis["conditions"]["0"], "partial_r u_0=0")
        self.assertEqual(axis["conditions"]["1"], "u_1=O(r^1)")
        self.assertEqual(axis["conditions"]["2"], "u_2=O(r^2)")
        self.assertTrue(axis["manufactured_profile_checks"])

    def test_sector_pdes_reconstruct_the_full_discrete_problem(self):
        witness = self.result["reduction_witness"]

        self.assertLessEqual(witness["analysis_residual"], 1e-12)
        self.assertLessEqual(witness["synthesis_residual"], 1e-9)
        self.assertLessEqual(witness["full_vs_reconstructed_relative_l2"], 1e-9)

    def test_fixed_accuracy_reduction_includes_boundary_and_axis_cost(self):
        full = self.result["full_3d_route"]
        reduced = self.result["quotient_sector_route"]

        self.assertTrue(full["tolerance_met"])
        self.assertTrue(reduced["tolerance_met"])
        self.assertEqual(self.result["route_evaluation"]["accuracy_target"], 0.02)
        self.assertLessEqual(full["relative_l2_error"], 0.02)
        self.assertLessEqual(reduced["relative_l2_error"], 0.02)
        self.assertLess(reduced["solved_degrees_of_freedom"], full["solved_degrees_of_freedom"])
        self.assertLess(reduced["assembled_nonzeros"], full["assembled_nonzeros"])
        self.assertTrue(reduced["measured_cost"]["includes_axis_and_warp_construction"])

    def test_wrong_uniform_axis_policy_is_an_obstruction(self):
        result = build_warped_axis_comparison(CONTROL)

        self.assertEqual(result["status"], "AxisRegularityObstruction")
        self.assertIn("isotropy", result["reason"])

    def test_cli_reports_stratified_reduction(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(BENCHMARK), "--summary"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("StratifiedBoundaryQuotientComparison", completed.stdout)
        self.assertIn("axis=isotropy-generated", completed.stdout)


if __name__ == "__main__":
    unittest.main()

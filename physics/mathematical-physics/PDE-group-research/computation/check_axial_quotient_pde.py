import subprocess
import sys
import unittest
from pathlib import Path

from axial_quotient_pde import build_axial_quotient_comparison

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "axial_quotient_pde.py"
BENCHMARK = HERE / "examples" / "axial-nonseparable-manufactured.json"
CONTROL = HERE / "examples" / "axial-theta-dependent-control.json"
TRANSFER = HERE / "examples" / "axial-coupling-mode-transfer.json"


class AxialQuotientPDETests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = build_axial_quotient_comparison(BENCHMARK)

    def test_group_is_constructed_from_operator_domain_and_boundary(self):
        discovery = self.result["symmetry_discovery"]

        self.assertEqual(self.result["status"], "FixedAccuracyQuotientPDEComparison")
        self.assertFalse(discovery["supplied_group"])
        self.assertEqual(discovery["connected_stabilizer"], "SO(2)")
        self.assertEqual(discovery["surviving_generators"], ["J_z"])
        self.assertEqual(len(discovery["rejected_euclidean_generators"]), 5)

    def test_reduction_stops_at_two_dimensional_pdes(self):
        quotient = self.result["orbit_space"]

        self.assertEqual(quotient["ambient_dimension"], 3)
        self.assertEqual(quotient["generic_orbit_dimension"], 1)
        self.assertEqual(quotient["quotient_dimension"], 2)
        self.assertEqual(quotient["reduced_object"], "second-order PDE on (r,z)")
        self.assertTrue(quotient["nonseparation_certificate"]["mixed_dependence_nonzero"])

    def test_source_support_selects_finitely_many_irreps_without_catalogue(self):
        sectors = self.result["sector_selection"]

        self.assertEqual(sectors["active_abs_weights"], [0, 1, 2])
        self.assertEqual(sectors["selection_origin"], "forcing character support")
        self.assertFalse(sectors["uses_special_function_catalogue"])

    def test_analysis_solve_and_synthesis_reconstruct_full_discrete_solution(self):
        witness = self.result["reduction_witness"]

        self.assertLessEqual(witness["analysis_residual"], 1e-12)
        self.assertLessEqual(witness["synthesis_residual"], 1e-10)
        self.assertLessEqual(witness["full_vs_reconstructed_relative_l2"], 1e-9)

    def test_same_continuum_error_target_has_lower_solve_dimension(self):
        full = self.result["full_3d_route"]
        reduced = self.result["quotient_sector_route"]

        self.assertTrue(full["tolerance_met"])
        self.assertTrue(reduced["tolerance_met"])
        self.assertEqual(self.result["route_evaluation"]["accuracy_target"], 0.02)
        self.assertLessEqual(full["relative_l2_error"], 0.02)
        self.assertLessEqual(reduced["relative_l2_error"], 0.02)
        self.assertLess(reduced["solved_degrees_of_freedom"], full["solved_degrees_of_freedom"])
        self.assertLess(reduced["assembled_nonzeros"], full["assembled_nonzeros"])
        for route in (full, reduced):
            self.assertIn("assembly_seconds", route["measured_cost"])
            self.assertIn("solve_seconds", route["measured_cost"])
            self.assertIn("recovery_seconds", route["measured_cost"])

    def test_theta_dependent_coefficient_refuses_exact_orbit_reduction(self):
        result = build_axial_quotient_comparison(CONTROL)

        self.assertEqual(result["status"], "NoExactOrbitReduction")
        self.assertIn("theta", result["obstruction"])

    def test_same_constructor_transfers_to_new_coefficients_and_character_support(self):
        result = build_axial_quotient_comparison(TRANSFER)

        self.assertEqual(result["status"], "FixedAccuracyQuotientPDEComparison")
        self.assertEqual(result["sector_selection"]["active_abs_weights"], [1, 3])
        self.assertEqual(result["quotient_sector_route"]["active_real_modes"], 2)
        self.assertLessEqual(
            result["reduction_witness"]["full_vs_reconstructed_relative_l2"],
            1e-9,
        )

    def test_cli_reports_the_route_and_quotient_dimension(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(BENCHMARK), "--summary"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("FixedAccuracyQuotientPDEComparison", completed.stdout)
        self.assertIn("3D->2D", completed.stdout)


if __name__ == "__main__":
    unittest.main()

import subprocess
import sys
import unittest
from pathlib import Path

from boundary_symmetry_reduction import build_boundary_reduction

HERE = Path(__file__).resolve().parent
DISK = HERE / "examples" / "dirichlet-disk-polynomial.json"
ELLIPSE = HERE / "examples" / "dirichlet-ellipse-polynomial.json"
DISK_P32 = HERE / "examples" / "dirichlet-disk-p32.json"


class BoundarySymmetryReductionTests(unittest.TestCase):
    def test_disk_boundary_removes_translations_but_retains_rotation(self):
        result = build_boundary_reduction(DISK)

        self.assertEqual(result["status"], "ExactBoundaryCompatibleReduction")
        symmetry = result["domain_symmetry"]
        self.assertEqual(symmetry["differential_expression_killing_dimension"], 3)
        self.assertEqual(symmetry["boundary_compatible_killing_dimension"], 1)
        self.assertEqual(symmetry["generator"], "x*d_y-y*d_x")
        self.assertTrue(all(symmetry["certificates"].values()))

    def test_same_galerkin_space_is_partitioned_into_exact_angular_blocks(self):
        result = build_boundary_reduction(DISK)

        galerkin = result["galerkin"]
        self.assertEqual(galerkin["full_dimension"], 28)
        self.assertEqual(
            [
                (sector["abs_m"], sector["radial_dimension"], sector["multiplicity"])
                for sector in galerkin["sectors"]
            ],
            [(0, 4, 1), (1, 3, 2), (2, 3, 2), (3, 2, 2), (4, 2, 2), (5, 1, 2), (6, 1, 2)],
        )
        self.assertTrue(galerkin["dimension_identity"])
        self.assertTrue(galerkin["unequal_weights_vanish_by_character_orthogonality"])
        self.assertTrue(all(galerkin["matrix_certificates"].values()))

    def test_exact_block_entries_are_generated_without_cartesian_expansion(self):
        result = build_boundary_reduction(DISK)
        radial_block = result["galerkin"]["sectors"][0]

        self.assertEqual(
            radial_block["mass_over_pi"][:2],
            [["1/3", "1/12", "1/30", "1/60"], ["1/12", "1/30", "1/60", "1/105"]],
        )
        self.assertEqual(
            [row[:2] for row in radial_block["stiffness_over_pi"][:2]],
            [["2", "2/3"], ["2/3", "2/3"]],
        )

    def test_cost_audit_counts_whole_dense_and_reduced_routes(self):
        result = build_boundary_reduction(DISK)
        cost = result["complexity"]

        self.assertEqual(cost["full_dense"]["solve_cubic_proxy"], 28**3)
        self.assertEqual(cost["representation_reduced"]["solve_cubic_proxy"], 136)
        self.assertEqual(cost["full_dense"]["matrix_storage_proxy"], 28**2)
        self.assertEqual(cost["representation_reduced"]["matrix_storage_proxy"], 44)
        self.assertEqual(cost["representation_reduced"]["parallel_critical_path_proxy"], 64)
        self.assertEqual(cost["asymptotic"]["full_solve"], "Theta(p^6)")
        self.assertEqual(cost["asymptotic"]["reduced_solve"], "Theta(p^4)")
        self.assertEqual(cost["asymptotic"]["parallel_critical_path"], "Theta(p^3)")
        self.assertEqual(result["route_evaluation"]["decision"], "RepresentationReduction")

    def test_ellipse_is_a_boundary_obstruction_not_a_false_rotation_group(self):
        result = build_boundary_reduction(ELLIPSE)

        self.assertEqual(result["status"], "NoContinuousBoundarySymmetry")
        self.assertEqual(result["domain_symmetry"]["boundary_compatible_killing_dimension"], 0)
        self.assertIn("boundary", result["reason"])
        self.assertNotIn("galerkin", result)

    def test_exact_complexity_formula_scales_without_building_a_full_pencil(self):
        result = build_boundary_reduction(DISK_P32)
        cost = result["complexity"]

        self.assertEqual(result["galerkin"]["full_dimension"], 561)
        self.assertEqual(cost["full_dense"]["solve_cubic_proxy"], 176558481)
        self.assertEqual(cost["representation_reduced"]["solve_cubic_proxy"], 41905)
        self.assertEqual(cost["representation_reduced"]["matrix_storage_proxy"], 3281)
        self.assertEqual(cost["representation_reduced"]["parallel_critical_path_proxy"], 4913)

    def test_cli_reports_reduction_and_cost_ratio(self):
        completed = subprocess.run(
            [sys.executable, str(HERE / "boundary_symmetry_reduction.py"), str(DISK), "--summary"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0)
        self.assertIn("ExactBoundaryCompatibleReduction", completed.stdout)
        self.assertIn("28 -> 7", completed.stdout)
        self.assertIn("RepresentationReduction", completed.stdout)


if __name__ == "__main__":
    unittest.main()

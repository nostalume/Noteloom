import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from singular_polynomial_closure import build_polynomial_closure

HERE = Path(__file__).resolve().parent
INPUT = HERE / "examples" / "singular-isotropic-e2.json"
TRANSFER_INPUT = HERE / "examples" / "singular-isotropic-transfer-e2.json"
FREQUENCY_TRANSFER_INPUT = HERE / "examples" / "singular-isotropic-frequency-transfer-e2.json"


class SingularPolynomialClosureTests(unittest.TestCase):
    def test_group_free_constructor_finds_a_genuine_polynomial_closure(self):
        result = build_polynomial_closure(INPUT)

        self.assertEqual(result["status"], "ExactPolynomialClosure")
        self.assertEqual(result["centralizer"]["quadratic_kernel_dimension"], 3)
        self.assertEqual(result["centralizer"]["hidden_quotient_dimension"], 2)
        self.assertEqual(result["closure"]["classification"], "PolynomialAlgebra")
        self.assertFalse(result["closure"]["linear_closure"])
        self.assertTrue(result["closure"]["quadratic_closure"])
        self.assertEqual(result["closure"]["commutator_order"], 3)
        self.assertTrue(all(result["certificates"].values()))

    def test_polynomial_terms_are_required_not_merely_available(self):
        result = build_polynomial_closure(INPUT)

        nonlinear = result["closure"]["nonlinear_coefficients"]
        self.assertTrue(nonlinear)
        self.assertTrue(
            any(label in {"H^2", "H*A", "H*B", "A^2", "{A,B}", "B^2"} for label in nonlinear)
        )
        self.assertEqual(result["group_integration"]["status"], "NotApplicable")

    def test_same_energy_observable_selects_factorization_after_both_routes_compute_it(self):
        result = build_polynomial_closure(INPUT)

        self.assertEqual(result["spectrum_baseline"]["energy_family"], "E_N=2*N+6")
        self.assertEqual(result["spectrum_baseline"]["degeneracy"], "N+1")
        self.assertEqual(
            result["route_evaluation"]["selected_for_energy"], "separated_factorization"
        )
        self.assertTrue(result["route_evaluation"]["same_spectrum_recovered"])

    def test_closure_generates_positive_finite_representations_and_recurrence(self):
        result = build_polynomial_closure(INPUT)

        representation = result["representation"]
        self.assertEqual(representation["status"], "ExactPositiveFiniteRepresentations")
        self.assertEqual(representation["levels"][2]["energy_candidates"], ["5", "10"])
        self.assertEqual(representation["levels"][2]["selected_energy"], "10")
        self.assertEqual(
            representation["off_diagonal_squared"],
            "u_(n+1)^2=4(n+1)(n+2*k_x)(N-n)(N-n+2*k_y-1)",
        )
        self.assertIn("P_(n+1)", representation["interbasis_recurrence"])
        self.assertTrue(all(representation["certificates"].values()))

    def test_representation_labels_are_generated_from_new_couplings(self):
        result = build_polynomial_closure(TRANSFER_INPUT)

        representation = result["representation"]
        self.assertEqual(
            representation["parameters"],
            {"omega": "1", "nu_x": "2", "nu_y": "3", "k_x": "3/2", "k_y": "2"},
        )
        self.assertEqual(representation["levels"][2]["selected_energy"], "11")
        self.assertIn("k_x", representation["B_lattice"])

    def test_representation_formulae_respect_frequency_rescaling(self):
        result = build_polynomial_closure(FREQUENCY_TRANSFER_INPUT)

        representation = result["representation"]
        self.assertEqual(representation["parameters"]["omega"], "2")
        self.assertEqual(representation["levels"][2]["selected_energy"], "20")
        self.assertEqual(representation["levels"][2]["B_eigenvalues"], ["5", "9", "13"])
        self.assertEqual(
            representation["A_diagonal"],
            "a_n=(E*b_n-b_n^2)/omega^2-1/4",
        )
        self.assertEqual(
            representation["off_diagonal_squared"],
            "u_(n+1)^2=4(n+1)(n+2*k_x)(N-n)(N-n+2*k_y-1)",
        )

    def test_anisotropy_removes_the_second_hidden_integral(self):
        payload = {
            "omega_x_squared": "1",
            "omega_y_squared": "4",
            "g_x": "2",
            "g_y": "6",
            "domain": "positive-quadrant-essentially-self-adjoint",
        }
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "anisotropic.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            result = build_polynomial_closure(path)

        self.assertEqual(result["status"], "CommutingQuadraticFamily")
        self.assertEqual(result["centralizer"]["quadratic_kernel_dimension"], 2)
        self.assertEqual(result["centralizer"]["hidden_quotient_dimension"], 1)

    def test_domain_ambiguity_is_refused_before_formal_closure(self):
        payload = {
            "omega_x_squared": "1",
            "omega_y_squared": "1",
            "g_x": "0",
            "g_y": "6",
            "domain": "positive-quadrant-essentially-self-adjoint",
        }
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "ambiguous-endpoint.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            result = build_polynomial_closure(path)

        self.assertEqual(result["status"], "Refused")
        self.assertIn("boundary-extension ambiguity", result["reason"])

    def test_cli_prints_compact_classification(self):
        completed = subprocess.run(
            [sys.executable, str(HERE / "singular_polynomial_closure.py"), str(INPUT), "--summary"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0)
        self.assertIn("kernel 6 -> 3", completed.stdout)
        self.assertIn("PolynomialAlgebra", completed.stdout)
        self.assertIn("selected separated_factorization for energy", completed.stdout)


if __name__ == "__main__":
    unittest.main()

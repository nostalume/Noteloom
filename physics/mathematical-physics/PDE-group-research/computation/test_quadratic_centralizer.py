import json
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from quadratic_centralizer import Poly, generate, load_potential, reconstruct_lower_term

HERE = Path(__file__).resolve().parent


class QuadraticCentralizerTests(unittest.TestCase):
    def test_rotated_quartic_discovers_one_hidden_quadratic_generator(self):
        potential = load_potential(HERE / "examples" / "rotated-quartic.json")
        result = generate(potential)

        self.assertEqual(result["status"], "NontrivialQuadraticCentralizer")
        self.assertEqual(result["killing_module_dimension"], 6)
        self.assertEqual(result["kernel_dimension"], 2)
        self.assertEqual(result["hidden_quotient_dimension"], 1)
        self.assertEqual(result["killing_module_parameter_order"], ["a", "b", "c", "d", "e", "f"])
        self.assertEqual(result["cost"]["linear_unknowns"], 6)
        self.assertTrue(result["compatibility_system"])
        self.assertTrue(result["certificates"]["all_six_basis_tensors_satisfy_killing_equation"])
        self.assertTrue(result["certificates"]["all_formal_quantum_commutators_zero"])

        hidden = result["generators"][1]
        self.assertEqual(
            hidden["parameters_abcdef"],
            ["0", "0", "0", "0", "0", "1"],
        )

        x = Poly.monomial((1, 0))
        y = Poly.monomial((0, 1))
        u = x + y
        v = x - y
        expected_lower = u * u * u * u + u.scale(3) - (v * v * v * v).scale(2)
        actual_lower = reconstruct_lower_term(
            potential,
            (Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(1)),
        )
        self.assertEqual(actual_lower, expected_lower)

    def test_generic_polynomial_has_only_the_metric_quadratic_integral(self):
        potential = load_potential(HERE / "examples" / "generic-polynomial.json")
        result = generate(potential)

        self.assertEqual(result["status"], "MetricOnly")
        self.assertEqual(result["kernel_dimension"], 1)
        self.assertEqual(result["hidden_quotient_dimension"], 0)

    def test_metric_generator_reconstructs_the_hamiltonian(self):
        potential = Poly({(2, 0): Fraction(3), (0, 2): Fraction(5)})
        result = generate(potential)
        metric = result["generators"][0]

        self.assertEqual(
            metric["parameters_abcdef"],
            ["0", "0", "1", "0", "1", "0"],
        )
        self.assertTrue(metric["commutator_zero"])

    def test_symmetry_enhancement_enlarges_the_generated_kernel(self):
        anisotropic = generate(Poly({(2, 0): Fraction(1), (0, 2): Fraction(2)}))
        isotropic = generate(Poly({(2, 0): Fraction(1), (0, 2): Fraction(1)}))
        free = generate(Poly({}))

        self.assertEqual(anisotropic["kernel_dimension"], 2)
        self.assertEqual(isotropic["kernel_dimension"], 4)
        self.assertEqual(free["kernel_dimension"], 6)

    def test_cli_refuses_inexact_coefficients(self):
        payload = {"potential": [{"powers": [2, 0], "coefficient": 0.5}]}
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "invalid.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(HERE / "quadratic_centralizer.py"), str(path)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(json.loads(completed.stdout)["status"], "Refused")


if __name__ == "__main__":
    unittest.main()

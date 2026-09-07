import json
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from radial_quadratic_centralizer import RadialExpr, generate, load_potential

HERE = Path(__file__).resolve().parent


class RadialQuadraticCentralizerTests(unittest.TestCase):
    def test_coulomb_full_module_discovers_three_hidden_quadratic_integrals(self):
        result = generate(load_potential(HERE / "examples" / "coulomb-radial.json"))

        self.assertEqual(result["status"], "NontrivialQuadraticCentralizer")
        self.assertEqual(result["kernel_dimension"], 4)
        self.assertEqual(result["hidden_quotient_dimension"], 3)
        self.assertEqual(result["first_order_kernel_dimension"], 1)
        self.assertTrue(result["certificates"]["all_formal_quantum_commutators_zero"])
        self.assertTrue(result["certificates"]["all_first_order_commutators_zero"])
        self.assertEqual(
            result["first_order_symmetries"][0]["parameters_translation_x_translation_y_rotation"],
            ["0", "0", "1"],
        )

        parameter_vectors = {
            tuple(generator["parameters_abcdef"]) for generator in result["generators"]
        }
        self.assertIn(("1", "0", "0", "0", "0", "0"), parameter_vectors)
        self.assertIn(("0", "1", "0", "0", "0", "0"), parameter_vectors)
        self.assertIn(("0", "0", "0", "1", "0", "0"), parameter_vectors)

    def test_coulomb_lower_terms_are_generated_not_supplied(self):
        result = generate(load_potential(HERE / "examples" / "coulomb-radial.json"))
        by_parameters = {
            tuple(generator["parameters_abcdef"]): generator for generator in result["generators"]
        }

        a_y = by_parameters[("0", "1", "0", "0", "0", "0")]
        a_x = by_parameters[("0", "0", "0", "1", "0", "0")]
        self.assertEqual(
            a_y["W"],
            [{"powers": [0, 1], "radius_squared_power": "-1/2", "coefficient": "-1"}],
        )
        self.assertEqual(
            a_x["W"],
            [{"powers": [1, 0], "radius_squared_power": "-1/2", "coefficient": "-1"}],
        )

    def test_radial_perturbation_removes_only_runge_lenz_directions(self):
        result = generate(load_potential(HERE / "examples" / "coulomb-plus-r2.json"))

        self.assertEqual(result["kernel_dimension"], 2)
        self.assertEqual(result["hidden_quotient_dimension"], 1)
        self.assertEqual(result["first_order_kernel_dimension"], 1)
        parameter_vectors = {
            tuple(generator["parameters_abcdef"]) for generator in result["generators"]
        }
        self.assertIn(("1", "0", "0", "0", "0", "0"), parameter_vectors)

    def test_radial_backend_recovers_polynomial_transfer(self):
        result = generate(load_potential(HERE / "examples" / "rotated-quartic.json"))

        self.assertEqual(result["kernel_dimension"], 2)
        self.assertEqual(result["hidden_quotient_dimension"], 1)
        self.assertTrue(result["certificates"]["all_formal_quantum_commutators_zero"])

    def test_radius_relation_has_exact_canonical_normal_form(self):
        x_squared = RadialExpr.monomial(x_power=2)
        expected = RadialExpr.monomial(s_power=1) - RadialExpr.monomial(y_power=2)

        self.assertEqual(x_squared, expected)
        self.assertEqual(
            RadialExpr.monomial(s_power=Fraction(-1, 2)).derivative_x(),
            RadialExpr.monomial(x_power=1, s_power=Fraction(-3, 2), coefficient=-1),
        )

    def test_cli_refuses_inexact_coefficients(self):
        payload = {
            "potential": [
                {
                    "powers": [0, 0],
                    "radius_squared_power": "-1/2",
                    "coefficient": 0.5,
                }
            ]
        }
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "invalid.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(HERE / "radial_quadratic_centralizer.py"), str(path)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(json.loads(completed.stdout)["status"], "Refused")

    def test_non_half_integer_radial_power_is_refused(self):
        with self.assertRaisesRegex(ValueError, "half-integers"):
            RadialExpr.monomial(s_power=Fraction(1, 3))


if __name__ == "__main__":
    unittest.main()

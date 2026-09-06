import json
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from radial_quadratic_centralizer_e3 import NDExpr, generate, load_potential

HERE = Path(__file__).resolve().parent


class RadialQuadraticCentralizerE3Tests(unittest.TestCase):
    def test_complete_e3_module_is_quotiented_before_coulomb_selection(self):
        result = generate(load_potential(HERE / "examples" / "coulomb-radial-e3.json"))

        self.assertEqual(result["quadratic_presented_dimension"], 21)
        self.assertEqual(result["quadratic_module_dimension"], 20)
        self.assertEqual(result["presentation_redundancy_dimension"], 1)
        redundancy = result["presentation_redundancies"][0]
        nonzero = {
            label: value
            for label, value in zip(redundancy["basis"], redundancy["coefficients"])
            if value != "0"
        }
        self.assertEqual(
            nonzero,
            {"P_x*R_x": "1", "P_y*R_y": "1", "P_z*R_z": "1"},
        )

    def test_coulomb_selects_rotations_rotation_quadratics_and_runge_lenz(self):
        result = generate(load_potential(HERE / "examples" / "coulomb-radial-e3.json"))

        self.assertEqual(result["status"], "NontrivialQuadraticCentralizer")
        self.assertEqual(result["first_order_kernel_dimension"], 3)
        self.assertEqual(result["quadratic_kernel_dimension"], 10)
        self.assertEqual(result["hidden_quotient_dimension"], 9)
        self.assertTrue(result["certificates"]["all_first_order_commutators_zero"])
        self.assertTrue(result["certificates"]["all_quadratic_commutators_with_H_zero"])

        lower_terms = [generator["W"] for generator in result["generators"]]
        for index in range(3):
            positive = {
                "powers": [1 if coordinate_index == index else 0 for coordinate_index in range(3)],
                "radius_squared_power": "-1/2",
                "coefficient": "1/2",
            }
            negative = {**positive, "coefficient": "-1/2"}
            self.assertTrue([positive] in lower_terms or [negative] in lower_terms)

    def test_radial_perturbation_removes_exactly_runge_lenz_sector(self):
        result = generate(load_potential(HERE / "examples" / "coulomb-plus-r2-e3.json"))

        self.assertEqual(result["first_order_kernel_dimension"], 3)
        self.assertEqual(result["quadratic_kernel_dimension"], 7)
        self.assertEqual(result["hidden_quotient_dimension"], 6)
        self.assertTrue(result["certificates"]["all_quadratic_commutators_with_H_zero"])

    def test_rotated_anisotropic_oscillator_selects_three_mode_integrals(self):
        result = generate(load_potential(HERE / "examples" / "rotated-anisotropic-e3.json"))

        self.assertEqual(result["first_order_kernel_dimension"], 0)
        self.assertEqual(result["quadratic_module_dimension"], 20)
        self.assertEqual(result["quadratic_kernel_dimension"], 3)
        self.assertEqual(result["hidden_quotient_dimension"], 2)
        self.assertTrue(result["certificates"]["all_quadratic_commutators_with_H_zero"])

    def test_radius_relation_and_derivative_are_exact(self):
        x_squared = NDExpr.monomial(3, powers=(2, 0, 0))
        expected = NDExpr.monomial(3, s_power=1)
        expected -= NDExpr.monomial(3, powers=(0, 2, 0))
        expected -= NDExpr.monomial(3, powers=(0, 0, 2))

        self.assertEqual(x_squared, expected)
        self.assertEqual(
            NDExpr.monomial(3, s_power=Fraction(-1, 2)).derivative(2),
            NDExpr.monomial(3, powers=(0, 0, 1), s_power=Fraction(-3, 2), coefficient=-1),
        )

    def test_cli_refuses_inexact_coefficients(self):
        payload = {
            "potential": [
                {
                    "powers": [0, 0, 0],
                    "radius_squared_power": "-1/2",
                    "coefficient": 0.5,
                }
            ]
        }
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "invalid.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(HERE / "radial_quadratic_centralizer_e3.py"), str(path)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(json.loads(completed.stdout)["status"], "Refused")

    def test_non_half_integer_radial_power_is_refused(self):
        with self.assertRaisesRegex(ValueError, "half-integers"):
            NDExpr.monomial(3, s_power=Fraction(1, 3))


if __name__ == "__main__":
    unittest.main()

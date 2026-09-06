import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from oscillator_cross_probe import build_cross_probe

HERE = Path(__file__).resolve().parent
INPUT = HERE / "examples" / "rotated-anisotropic-e3.json"


class OscillatorCrossProbeTests(unittest.TestCase):
    def test_independent_routes_construct_the_same_reduction_witness(self):
        result = build_cross_probe(INPUT)

        self.assertEqual(result["status"], "ExactCrossProbeSelection")
        self.assertEqual(result["selected_route"], "factor")
        self.assertEqual(result["centralizer"]["first_order_kernel_dimension"], 0)
        self.assertEqual(result["centralizer"]["quadratic_kernel_dimension"], 3)
        self.assertTrue(all(result["coincidence_checks"].values()))

    def test_projectors_are_constructed_exactly_without_supplied_axes(self):
        result = build_cross_probe(INPUT)

        self.assertEqual(
            result["factor_witness"]["mode_projectors"],
            [
                [["9/25", "12/25", "0"], ["12/25", "16/25", "0"], ["0", "0", "0"]],
                [["16/25", "-12/25", "0"], ["-12/25", "9/25", "0"], ["0", "0", "0"]],
                [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "1"]],
            ],
        )
        self.assertEqual(
            result["centralizer_witness"]["mode_projectors"],
            result["factor_witness"]["mode_projectors"],
        )

    def test_both_routes_recover_the_same_spectrum_and_heat_trace(self):
        result = build_cross_probe(INPUT)

        expected = {
            "frequencies": ["1", "sqrt(2)", "sqrt(3)"],
            "energy_family": "E_(n1,n2,n3)=sum_i (n_i+1/2) omega_i",
            "heat_trace": "product_i exp(-t omega_i/2)/(1-exp(-t omega_i))",
        }
        self.assertEqual(result["factor_witness"]["observable"], expected)
        self.assertEqual(result["centralizer_witness"]["observable"], expected)
        self.assertEqual(
            result["centralizer_witness"]["representation"],
            result["factor_witness"]["representation"],
        )
        self.assertEqual(
            result["factor_witness"]["representation"]["relations"][0],
            "[a_i^-,a_j^+]=2 omega_i delta_ij",
        )

    def test_enhanced_first_order_symmetry_is_outside_minimal_cross_probe(self):
        payload = {
            "potential": [
                {"powers": [2, 0, 0], "coefficient": "1/2"},
                {"powers": [0, 2, 0], "coefficient": "1/2"},
                {"powers": [0, 0, 2], "coefficient": "1/2"},
            ]
        }
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "isotropic.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            result = build_cross_probe(path)

        self.assertEqual(result["status"], "Refused")
        self.assertIn("distinct positive", result["reason"])

    def test_cli_reports_the_route_selection(self):
        completed = subprocess.run(
            [sys.executable, str(HERE / "oscillator_cross_probe.py"), str(INPUT), "--summary"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0)
        self.assertIn("factor == centralizer on 3 projectors", completed.stdout)
        self.assertIn("selected factor", completed.stdout)


if __name__ == "__main__":
    unittest.main()

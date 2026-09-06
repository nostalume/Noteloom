import json
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from cyclic_reduce import AdmissibilityError, cyclic_reduce, reduce_symmetric_matrix

HERE = Path(__file__).resolve().parent


class CyclicReduceTests(unittest.TestCase):
    def test_exact_one_dimensional_carrier_returns_relative_minimal_polynomial(self):
        result = reduce_symmetric_matrix([[2, 0], [0, 3]], [1, 0])

        self.assertEqual(result.status, "ExactCyclicReduction")
        self.assertEqual(result.carrier_dimension, 1)
        self.assertEqual(result.alpha, (Fraction(2),))
        self.assertEqual(result.minimal_polynomial, (Fraction(-2), Fraction(1)))
        self.assertTrue(result.certificates["moment_recovery"])

    def test_hidden_ambient_sector_is_removed_without_diagonalizing(self):
        result = reduce_symmetric_matrix(
            [[0, 1, 0], [1, 0, 0], [0, 0, 7]],
            [1, 0, 0],
        )

        self.assertEqual(result.status, "ExactCyclicReduction")
        self.assertEqual(result.carrier_dimension, 2)
        self.assertFalse(result.no_dimension_gain)
        self.assertEqual(
            result.reduced_operator,
            ((Fraction(0), Fraction(1)), (Fraction(1), Fraction(0))),
        )
        self.assertEqual(
            result.minimal_polynomial,
            (Fraction(-1), Fraction(0), Fraction(1)),
        )

    def test_full_carrier_reports_no_dimension_gain(self):
        result = reduce_symmetric_matrix(
            [[1, 0, 0], [0, 2, 0], [0, 0, 3]],
            [1, 1, 1],
        )

        self.assertEqual(result.status, "ExactCyclicReduction")
        self.assertEqual(result.carrier_dimension, 3)
        self.assertTrue(result.no_dimension_gain)

    def test_budgeted_truncation_is_controlled_only_when_duhamel_bound_fits(self):
        controlled = reduce_symmetric_matrix(
            [[0, 1], [1, 0]],
            [1, 0],
            budget=1,
            time_horizon=Fraction(1, 10),
            tolerance=Fraction(1, 5),
        )
        formal = reduce_symmetric_matrix(
            [[0, 1], [1, 0]],
            [1, 0],
            budget=1,
            time_horizon=Fraction(1, 10),
            tolerance=Fraction(1, 20),
        )

        self.assertEqual(controlled.status, "ControlledCyclicReduction")
        self.assertEqual(controlled.boundary_beta_squared, Fraction(1))
        self.assertEqual(controlled.error_bound_squared, Fraction(1, 100))
        self.assertEqual(controlled.time_horizon, Fraction(1, 10))
        self.assertEqual(controlled.tolerance, Fraction(1, 5))
        self.assertEqual(controlled.to_dict()["truncation"]["time_horizon"], "1/10")
        self.assertIsNone(controlled.no_dimension_gain)
        self.assertIn(
            "budget truncation; excluded directions are not certified invisible",
            controlled.summary(),
        )
        self.assertEqual(formal.status, "FormalTruncation")

    def test_matrix_free_action_is_the_semantic_core(self):
        def action(vector):
            return (vector[1], vector[0], 7 * vector[2])

        result = cyclic_reduce(
            action,
            [1, 0, 0],
            dimension=3,
            budget=3,
            self_adjoint_certificate="supplied",
        )

        self.assertEqual(result.carrier_dimension, 2)
        self.assertEqual(result.certificates["self_adjoint"], "supplied")

    def test_non_euclidean_metric_preserves_physical_pairing_exactly(self):
        result = reduce_symmetric_matrix(
            [[0, 1], [2, 0]],
            [1, 0],
            metric=[[2, 0], [0, 1]],
        )

        self.assertEqual(result.status, "ExactCyclicReduction")
        self.assertEqual(result.beta_squared, (Fraction(2),))
        self.assertEqual(
            result.minimal_polynomial,
            (Fraction(-2), Fraction(0), Fraction(1)),
        )
        self.assertTrue(result.certificates["reduced_metric_self_adjoint"])

    def test_non_symmetric_matrix_is_refused(self):
        with self.assertRaisesRegex(AdmissibilityError, "symmetric"):
            reduce_symmetric_matrix([[0, 1], [0, 0]], [1, 0])

    def test_non_positive_metric_is_refused(self):
        with self.assertRaisesRegex(AdmissibilityError, "positive definite"):
            reduce_symmetric_matrix(
                [[1, 0], [0, 1]],
                [1, 0],
                metric=[[1, 0], [0, -1]],
            )

    def test_float_input_is_refused_in_exact_mode(self):
        with self.assertRaisesRegex(AdmissibilityError, "exact rational"):
            reduce_symmetric_matrix([[0.0, 1], [1, 0]], [1, 0])

    def test_cli_refusal_is_structured_and_nonzero(self):
        payload = {"matrix": [[0, 1], [0, 0]], "preparation": [1, 0]}
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "invalid.json"
            input_path.write_text(json.dumps(payload), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(HERE / "cyclic_reduce.py"), str(input_path)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(completed.returncode, 2)
        output = json.loads(completed.stdout)
        self.assertEqual(output["status"], "Refused")
        self.assertIn("symmetric", output["reason"])

    def test_cli_emits_machine_readable_certificate(self):
        payload = {
            "matrix": [[0, 1, 0], [1, 0, 0], [0, 0, 7]],
            "preparation": [1, 0, 0],
            "budget": 3,
        }
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "input.json"
            input_path.write_text(json.dumps(payload), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(HERE / "cyclic_reduce.py"), str(input_path)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        output = json.loads(completed.stdout)
        self.assertEqual(output["status"], "ExactCyclicReduction")
        self.assertEqual(output["carrier_dimension"], 2)
        self.assertEqual(output["minimal_polynomial"], ["-1", "0", "1"])

    def test_human_summary_retains_recurrence_and_selection_boundary(self):
        result = reduce_symmetric_matrix(
            [[0, 1, 0], [1, 0, 0], [0, 0, 7]],
            [1, 0, 0],
        )

        summary = result.summary()
        self.assertIn("ambient 3 -> cyclic 2", summary)
        self.assertIn("minimal polynomial coefficients: [-1, 0, 1]", summary)
        self.assertIn("removes 1 invisible dimension", summary)
        self.assertIn("does not determine a unique group", summary)


if __name__ == "__main__":
    unittest.main()

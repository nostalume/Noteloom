"""Contract smoke test for the reproducible G17 cost instrument."""

from __future__ import annotations

import unittest

from benchmark_active_subspace import benchmark_case


class ActiveSubspaceBenchmarkTests(unittest.TestCase):
    def test_case_compares_same_prepared_problem_and_reports_separate_costs(self) -> None:
        result = benchmark_case(2, 1, repetitions=1)

        self.assertEqual(result["active_dimensions"], [3])
        self.assertEqual(result["family_active_dimension"], 3)
        self.assertLessEqual(result["observable_error"], 1e-11)
        self.assertLessEqual(result["family_observable_error"], 1e-11)
        self.assertEqual(result["full_exponential_cubic_proxy"], 4**3)
        self.assertEqual(result["active_exponential_cubic_proxy"], 3**3)
        self.assertGreater(result["exact_coordinate_solves"], 0)
        self.assertGreater(result["dense_median_seconds"], 0)
        self.assertGreater(result["active_median_seconds"], 0)
        self.assertGreater(result["family_median_seconds"], 0)


if __name__ == "__main__":
    unittest.main()

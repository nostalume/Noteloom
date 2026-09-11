"""Laws for the exact preparation-reachable matrix module."""

from __future__ import annotations

import unittest

import exact_gaussian_matrix as gaussian
from gaussian_reachable_module import (
    Apply,
    ReachableModuleBudget,
    ReachableModuleError,
    Seed,
    construct_reachable_module,
)


class GaussianReachableModuleTests(unittest.TestCase):
    def test_nonhermitian_family_has_deterministic_provenance_and_actions(self) -> None:
        raising = gaussian.matrix([[0, 1], [0, 0]], "raising")
        selector = gaussian.matrix([[1, 0], [0, 0]], "selector")

        result = construct_reachable_module(
            (raising, selector),
            (gaussian.ZERO, gaussian.ONE),
            ReachableModuleBudget(2, 2),
        )

        self.assertEqual(
            result.basis,
            ((gaussian.ZERO, gaussian.ONE), (gaussian.ONE, gaussian.ZERO)),
        )
        self.assertEqual(result.provenance, (Seed(), Apply(0, 0)))
        self.assertEqual(
            result.reduced_actions,
            (
                gaussian.matrix([[0, 0], [1, 0]], "raising reduced"),
                gaussian.matrix([[0, 0], [0, 1]], "selector reduced"),
            ),
        )
        self.assertEqual(result.cost.generator_actions, 4)
        self.assertEqual(result.cost.exact_coordinate_solves, 4)
        self.assertEqual(result.cost.admitted_nodes, 2)
        self.assertEqual(result.cost.rejected_dependent_actions, 3)
        self.assertTrue(all(result.checks.values()))

    def test_active_dimension_budget_refuses_before_appending(self) -> None:
        with self.assertRaises(ReachableModuleError) as caught:
            construct_reachable_module(
                (gaussian.matrix([[0, 1], [0, 0]], "raising"),),
                (gaussian.ZERO, gaussian.ONE),
                ReachableModuleBudget(2, 1),
            )

        self.assertEqual(caught.exception.kind, "ActiveSubspaceBudgetExceeded")


if __name__ == "__main__":
    unittest.main()

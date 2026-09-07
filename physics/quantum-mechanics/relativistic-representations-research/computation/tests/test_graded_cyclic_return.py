from copy import copy
import unittest

import numpy as np

from fieldcalc.graded_return import compile_graded_cyclic_return
from fieldcalc.impurity import AndersonRequest, compile_anderson
from fieldcalc.perturbative_return import compile_perturbative_return


class GradedCyclicReturnTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.system = compile_anderson(AndersonRequest(
            impurity_energy=-1.0,
            interaction=2.0,
            bath_energies=(-0.75, 0.75),
            hybridizations=(1.0 / 3.0, 1.0 / 3.0),
            beta=2.0,
            matsubara_index=0,
            coefficient_order=4,
            quadrature_order=12,
            provenance="node 47 graded cyclic-module probe",
            resource_budget=500_000_000,
        )).system
        cls.full = compile_perturbative_return(
            cls.system,
            moment_order=12,
            resource_budget=20_000_000,
        ).model

    def test_action_generates_a_graded_closed_module(self):
        result = compile_graded_cyclic_return(
            self.full,
            resource_budget=20_000_000,
        )
        self.assertTrue(result.accepted, result.refusal)
        model = result.model

        self.assertEqual(model.filtration_ranks[0], 2)
        self.assertEqual(tuple(sorted(model.filtration_ranks)), model.filtration_ranks)
        self.assertEqual(max(model.valuations), self.system.request.coefficient_order)
        self.assertLess(model.rank, model.cost.ambient_operator_dimension)
        self.assertLess(model.free_closure_residual, 2e-10)
        self.assertLess(model.graded_interaction_residual, 2e-10)
        self.assertLess(
            model.cost.retained_complex_scalars,
            model.cost.source_packet_complex_scalars,
        )

        ranks = tuple(
            compile_graded_cyclic_return(
                self.full,
                resource_budget=20_000_000,
                tolerance=tolerance,
            ).model.filtration_ranks
            for tolerance in (1e-8, 1e-10, 1e-12)
        )
        self.assertEqual(ranks, (ranks[0], ranks[0], ranks[0]))

    def test_one_reduced_packet_recovers_multiple_frequency_coefficients(self):
        model = compile_graded_cyclic_return(
            self.full,
            resource_budget=20_000_000,
        ).model

        for z in (
            1j * self.system.matsubara_frequency,
            0.35 + 0.20j,
            40j,
        ):
            expected = self.full.green_coefficients(z)
            actual = model.green_coefficients(z)
            for order in range(5):
                with self.subTest(z=z, order=order):
                    self.assertLess(abs(actual[order] - expected[order]), 2e-10)

    def test_reduced_query_has_a_finite_complete_break_even(self):
        model = compile_graded_cyclic_return(
            self.full,
            resource_budget=20_000_000,
        ).model

        self.assertLess(
            model.cost.reduced_query_operations,
            model.cost.full_query_operations,
        )
        self.assertIsNotNone(model.cost.break_even_queries)
        self.assertGreater(model.cost.break_even_queries, 0)

    def test_invalid_action_tolerance_budget_and_real_axis_are_refused(self):
        compiled = compile_graded_cyclic_return(
            self.full,
            resource_budget=20_000_000,
        )
        with self.assertRaisesRegex(ValueError, "off-axis"):
            compiled.model.green_coefficients(0.35)

        nonhermitian = copy(self.full)
        invalid_system = copy(self.system)
        invalid_system.hybridization_action = (
            invalid_system.hybridization_action
            + 0.1j * np.eye(invalid_system.hybridization_action.shape[0])
        )
        object.__setattr__(nonhermitian, "system", invalid_system)

        invalid = compile_graded_cyclic_return(
            nonhermitian,
            resource_budget=20_000_000,
        )
        unresolved = compile_graded_cyclic_return(
            self.full,
            resource_budget=20_000_000,
            tolerance=0.0,
        )
        bounded = compile_graded_cyclic_return(
            self.full,
            resource_budget=100,
        )

        self.assertFalse(invalid.accepted)
        self.assertEqual(invalid.refusal.reason, "return action is not Hermitian")
        self.assertFalse(unresolved.accepted)
        self.assertEqual(unresolved.refusal.reason, "rank tolerance must be positive")
        self.assertFalse(bounded.accepted)
        self.assertEqual(bounded.refusal.reason, "graded return budget exceeded")


if __name__ == "__main__":
    unittest.main()

import unittest

import numpy as np

from fieldcalc.impurity import AndersonRequest, compile_anderson
from fieldcalc.perturbative_return import compile_perturbative_return


class PerturbativeCorrelationReturnTests(unittest.TestCase):
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
            provenance="node 46 perturbative correlation probe",
            resource_budget=500_000_000,
        )).system

    def test_endpoint_functional_recovers_time_domain_coefficients(self):
        result = compile_perturbative_return(
            self.system,
            moment_order=12,
            resource_budget=20_000_000,
        )
        self.assertTrue(result.accepted, result.refusal)

        z = 1j * self.system.matsubara_frequency
        generated = result.model.green_coefficients(z)
        baseline = self.system.green_coefficients()
        for order in range(5):
            with self.subTest(order=order):
                self.assertLess(abs(generated[order] - baseline.values[order]), 2e-9)

        self.assertLess(abs(generated[1]), 2e-11)
        self.assertLess(abs(generated[3]), 2e-11)
        self.assertEqual(result.model.cost.endpoint_exponential_actions, 1)
        self.assertEqual(result.model.cost.resolvent_actions_per_query, 5)
        self.assertLess(
            result.model.cost.endpoint_exponential_actions,
            baseline.cost.exponentials,
        )

    def test_moment_and_resolvent_branches_share_large_frequency_expansion(self):
        result = compile_perturbative_return(
            self.system,
            moment_order=12,
            resource_budget=20_000_000,
        )
        z = 40j
        exact = result.model.green_coefficients(z)
        asymptotic = result.model.moment_green_coefficients(z, count=12)

        for order in range(5):
            with self.subTest(order=order):
                self.assertLess(abs(exact[order] - asymptotic[order]), 2e-10)

    def test_decoupled_hankel_rank_defect_is_exposed(self):
        result = compile_perturbative_return(
            self.system,
            moment_order=12,
            resource_budget=20_000_000,
        )

        self.assertLess(result.model.zeroth_hankel_rank(depth=6), 6)
        self.assertEqual(result.model.zeroth_hankel_rank(depth=6), 2)

    def test_real_axis_invalid_order_and_budget_are_refused(self):
        result = compile_perturbative_return(
            self.system,
            moment_order=12,
            resource_budget=20_000_000,
        )
        with self.assertRaisesRegex(ValueError, "off-axis"):
            result.model.green_coefficients(0.35)

        invalid = compile_perturbative_return(
            self.system,
            moment_order=0,
            resource_budget=20_000_000,
        )
        bounded = compile_perturbative_return(
            self.system,
            moment_order=12,
            resource_budget=100,
        )
        unsupported = compile_perturbative_return(
            self.system,
            moment_order=12,
            resource_budget=20_000_000,
            coefficient_order=7,
        )

        self.assertFalse(invalid.accepted)
        self.assertEqual(invalid.refusal.reason, "moment order must be positive")
        self.assertFalse(bounded.accepted)
        self.assertEqual(bounded.refusal.reason, "perturbative return budget exceeded")
        self.assertFalse(unsupported.accepted)
        self.assertEqual(
            unsupported.refusal.reason,
            "coefficient order lies outside the perturbative return boundary",
        )


if __name__ == "__main__":
    unittest.main()

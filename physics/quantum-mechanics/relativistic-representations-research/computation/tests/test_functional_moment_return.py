from dataclasses import replace
import unittest

from fieldcalc.impurity import AndersonRequest, compile_anderson
from fieldcalc.moment_return import (
    anderson_correlation_problem,
    compile_moment_return,
)
from fieldcalc.return_reduction import (
    anderson_state_metric_problem,
    anderson_thermal_problem,
    compile_cyclic_return,
)


class FunctionalMomentReturnTests(unittest.TestCase):
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
            provenance="node 45 functional moment probe",
            resource_budget=500_000_000,
        )).system

    def test_functional_moments_equal_native_metric_moments(self):
        functional = anderson_correlation_problem(self.system, coupling=0.12)
        native = anderson_state_metric_problem(self.system, coupling=0.12)
        values = functional.source
        for order in range(21):
            with self.subTest(order=order):
                expected = native.inner(native.source, values)[0, 0]
                self.assertLess(abs(functional.correlate(values) - expected), 2e-11)
            values = functional.apply_generator(values)

    def test_moment_recurrence_recovers_the_same_reduced_return(self):
        functional = anderson_correlation_problem(self.system, coupling=0.12)
        native = anderson_state_metric_problem(self.system, coupling=0.12)
        moment_result = compile_moment_return(
            functional, depth=10, resource_budget=4_000_000,
        )
        native_result = compile_cyclic_return(
            native, depth=10, resource_budget=80_000_000,
        )

        self.assertTrue(moment_result.accepted, moment_result.refusal)
        self.assertEqual(moment_result.model.rank, native_result.model.rank)
        self.assertLess(max(moment_result.model.moment_residuals(20)), 2e-9)
        for z in (1j * self.system.matsubara_frequency, 0.35 + 0.20j):
            with self.subTest(z=z):
                self.assertLess(
                    abs(moment_result.model.evaluate(z)[0, 0]
                        - native_result.model.evaluate(z)[0, 0]),
                    2e-9,
                )
                certificate = moment_result.model.certified_evaluate(z)
                exact = anderson_thermal_problem(
                    self.system, coupling=0.12,
                ).evaluate(z)[0, 0]
                self.assertLessEqual(
                    abs(certificate.value[0, 0] - exact),
                    certificate.error_bound,
                )

    def test_functional_route_reduces_native_and_transition_setup(self):
        functional = anderson_correlation_problem(self.system, coupling=0.12)
        functional_result = compile_moment_return(
            functional, depth=10, resource_budget=4_000_000,
        )
        native_result = compile_cyclic_return(
            anderson_state_metric_problem(self.system, coupling=0.12),
            depth=10,
            resource_budget=80_000_000,
        )
        transition_result = compile_cyclic_return(
            anderson_thermal_problem(self.system, coupling=0.12),
            depth=10,
            resource_budget=4_000_000,
        )

        self.assertEqual(functional.thermal_actions, 2)
        self.assertLess(
            functional_result.model.cost.estimated_setup_operations,
            native_result.model.cost.estimated_setup_operations,
        )
        self.assertLess(
            functional_result.model.cost.estimated_setup_operations,
            transition_result.model.cost.estimated_setup_operations,
        )

    def test_nonpositive_functional_and_budget_are_refused(self):
        functional = anderson_correlation_problem(self.system, coupling=0.12)
        nonpositive = replace(
            functional,
            correlate=lambda values: -functional.correlate(values),
        )

        invalid = compile_moment_return(
            nonpositive, depth=3, resource_budget=4_000_000,
        )
        bounded = compile_moment_return(
            functional, depth=10, resource_budget=100,
        )

        self.assertFalse(invalid.accepted)
        self.assertEqual(invalid.refusal.reason, "correlation functional is not positive")
        self.assertFalse(bounded.accepted)
        self.assertEqual(bounded.refusal.reason, "moment return budget exceeded")


if __name__ == "__main__":
    unittest.main()

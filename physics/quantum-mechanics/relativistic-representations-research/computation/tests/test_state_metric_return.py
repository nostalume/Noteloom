import unittest
from dataclasses import replace

import numpy as np

from fieldcalc.impurity import AndersonRequest, compile_anderson
from fieldcalc.return_reduction import (
    anderson_state_metric_problem,
    anderson_thermal_problem,
    compile_cyclic_return,
)


class StateMetricReturnTests(unittest.TestCase):
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
            provenance="node 44 native state-metric probe",
            resource_budget=500_000_000,
        )).system

    def test_state_generates_positive_metric_and_self_adjoint_liouvillian(self):
        problem = anderson_state_metric_problem(self.system, coupling=0.12)
        source = problem.source
        tangent = source + 0.3j * problem.apply_generator(source)

        self.assertAlmostEqual(problem.inner(source, source)[0, 0].real, 1.0)
        self.assertGreater(problem.inner(tangent, tangent)[0, 0].real, 0.0)
        self.assertLess(problem.hermitian_residual, 2e-12)
        self.assertLess(abs(
            problem.inner(source, problem.apply_generator(tangent))[0, 0]
            - problem.inner(problem.apply_generator(source), tangent)[0, 0]
        ), 2e-11)

    def test_native_projection_recovers_transition_projection_without_transitions(self):
        native = anderson_state_metric_problem(self.system, coupling=0.12)
        spectral = anderson_thermal_problem(self.system, coupling=0.12)
        native_result = compile_cyclic_return(
            native, depth=10, resource_budget=80_000_000,
        )
        spectral_result = compile_cyclic_return(
            spectral, depth=10, resource_budget=4_000_000,
        )

        self.assertTrue(native_result.accepted, native_result.refusal)
        self.assertEqual(native_result.model.rank, spectral_result.model.rank)
        for z in (1j * self.system.matsubara_frequency, 0.35 + 0.20j):
            with self.subTest(z=z):
                self.assertLess(
                    abs(native_result.model.evaluate(z)[0, 0]
                        - spectral_result.model.evaluate(z)[0, 0]),
                    2e-9,
                )
                certificate = native_result.model.certified_evaluate(z)
                self.assertLessEqual(
                    abs(certificate.value[0, 0] - native.evaluate(z)[0, 0]),
                    certificate.error_bound,
                )

    def test_native_metric_cost_is_compared_with_complete_spectral_adapter(self):
        problem = anderson_state_metric_problem(self.system, coupling=0.12)
        result = compile_cyclic_return(
            problem, depth=10, resource_budget=80_000_000,
        )

        self.assertGreater(result.model.cost.metric_operations, 0)
        self.assertGreater(
            result.model.cost.estimated_setup_operations,
            result.model.cost.baseline_setup_operations,
        )

    def test_nonpositive_metrics_and_insufficient_work_are_refused(self):
        problem = anderson_state_metric_problem(self.system, coupling=0.12)
        nonpositive = replace(
            problem,
            apply_metric=lambda values: -values,
            hermitian_residual=0.0,
        )

        invalid = compile_cyclic_return(
            nonpositive, depth=2, resource_budget=80_000_000,
        )
        bounded = compile_cyclic_return(
            problem, depth=10, resource_budget=1_000,
        )

        self.assertFalse(invalid.accepted)
        self.assertEqual(invalid.refusal.reason, "return metric is not positive")
        self.assertFalse(bounded.accepted)
        self.assertEqual(bounded.refusal.reason, "cyclic return budget exceeded")


if __name__ == "__main__":
    unittest.main()

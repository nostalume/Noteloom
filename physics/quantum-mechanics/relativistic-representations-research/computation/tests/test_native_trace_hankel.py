import unittest

import numpy as np

from fieldcalc.impurity import AndersonRequest, compile_anderson
from fieldcalc.native_car import (
    compile_native_graded_reachability,
    native_to_matrix,
)
from fieldcalc.native_hankel import (
    behavioral_observability,
    compile_native_trace_hankel,
)
from fieldcalc.native_dual import native_functional_seeds
from fieldcalc.perturbative_return import compile_perturbative_return


class NativeTraceHankelTests(unittest.TestCase):
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
            provenance="node 54 native trace Hankel",
            resource_budget=500_000_000,
        )).system
        cls.native = compile_native_graded_reachability(
            cls.system,
            coefficient_order=4,
            tolerance=1e-10,
            resource_budget=20_000_000,
        ).model
        cls.full = compile_perturbative_return(
            cls.system,
            moment_order=12,
            resource_budget=20_000_000,
        ).model
        cls.diagnostic = compile_native_trace_hankel(
            cls.system,
            cls.native,
            thermal_order=4,
            tolerance=1e-10,
            coefficient_budget=100_000,
            resource_budget=500_000_000,
        )

    def test_diagnostic_quotient_recovers_but_does_not_compress_the_packet(self):
        self.assertTrue(self.diagnostic.accepted, self.diagnostic.refusal)
        model = self.diagnostic.model
        self.assertEqual(model.prefix_ranks_by_grade, (10, 16, 26, 32, 36))
        self.assertEqual(model.behavioral_ranks_by_grade, (10, 16, 26, 32, 36))
        self.assertEqual(model.total_prefix_rank, 120)
        self.assertEqual(model.total_behavioral_rank, 120)
        self.assertEqual(model.output_count, 31)
        self.assertEqual(model.retained_prefix_coefficients, 18_283)
        self.assertEqual(model.estimated_construction_operations, 407_361_547)
        self.assertLess(model.closure_residual, 2e-9)
        self.assertLess(model.quotient_residual, 2e-9)

        actual = model.thermal_packet(self.system.request.beta).coefficients
        dense = self.system.thermal_coefficients(self.system.request.beta)
        seeds, _, _ = native_functional_seeds(self.native, self.system)
        expected = np.asarray([
            [
                np.trace(coefficient @ native_to_matrix(seed, 4))
                for seed in seeds
            ]
            for coefficient in dense
        ])
        self.assertLess(np.linalg.norm(actual - expected), 2e-8)

    def test_frozen_behavioral_probe_refuses_before_grade_four(self):
        result = compile_native_trace_hankel(
            self.system,
            self.native,
            thermal_order=4,
            tolerance=1e-10,
            coefficient_budget=100_000,
            resource_budget=100_000_000,
        )
        self.assertFalse(result.accepted)
        self.assertEqual(
            result.refusal.reason,
            "native trace-Hankel resource budget exceeded",
        )
        self.assertEqual(result.boundary.active_phase, "prefix grade 3")
        self.assertEqual(
            result.boundary.prefix_ranks_by_grade,
            (10, 16, 26, 32, 0),
        )
        self.assertEqual(
            result.boundary.prefix_support_by_grade,
            (512, 1_776, 4_324, 5_340, 0),
        )
        self.assertEqual(result.boundary.resource_used, 100_838_570)

    def test_final_green_query_still_observes_the_whole_thermal_module(self):
        model = self.diagnostic.model
        z = 1j * self.system.matsubara_frequency
        resolvent = z * np.eye(30) - self.native.free_generator
        response = [np.linalg.solve(resolvent, self.native.reduced_source)]
        for _ in range(4):
            response.append(np.linalg.solve(
                resolvent,
                self.native.interaction_generator @ response[-1],
            ))

        rows = []
        for total in range(5):
            rows.append(model.output_covectors_by_grade[total][0])
            rows.append(sum(
                response[total - grade]
                @ model.output_covectors_by_grade[grade][1:]
                for grade in range(total + 1)
            ))
        row_matrix = np.asarray(rows)
        observable = behavioral_observability(
            (model.free_action, model.interaction_action),
            row_matrix,
            tolerance=1e-10,
        )

        self.assertEqual(np.linalg.matrix_rank(row_matrix, tol=1e-10), 4)
        self.assertEqual(observable.rank, model.total_behavioral_rank)
        self.assertLess(observable.closure_residual, 2e-9)

        packet = model.thermal_packet(self.system.request.beta).coefficients
        partition = packet[:, 0]
        numerator = [
            sum(
                response[total - grade] @ packet[grade, 1:]
                for grade in range(total + 1)
            )
            for total in range(5)
        ]
        green = []
        for total, value in enumerate(numerator):
            correction = sum(
                partition[grade] * green[total - grade]
                for grade in range(1, total + 1)
            )
            green.append((value - correction) / partition[0])
        self.assertLess(
            np.linalg.norm(np.asarray(green) - self.full.green_coefficients(z)),
            2e-8,
        )


class BehavioralObservabilityTests(unittest.TestCase):
    def test_small_invariant_output_space_and_invalid_inputs(self):
        action = np.diag([1.0, 2.0, 3.0])
        result = behavioral_observability(
            (action,),
            np.asarray([[1.0, 0.0, 0.0]]),
            tolerance=1e-10,
        )
        self.assertEqual(result.rank, 1)
        self.assertEqual(result.closure_residual, 0.0)

        with self.assertRaisesRegex(ValueError, "tolerance"):
            behavioral_observability((action,), np.eye(3), tolerance=0.0)
        with self.assertRaisesRegex(ValueError, "shape"):
            behavioral_observability((np.eye(2),), np.eye(3), tolerance=1e-10)


if __name__ == "__main__":
    unittest.main()

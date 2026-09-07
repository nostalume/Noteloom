import unittest

import numpy as np

from fieldcalc.graded_return import compile_graded_cyclic_return
from fieldcalc.impurity import AndersonRequest, car_annihilator, compile_anderson
from fieldcalc.native_car import compile_native_graded_reachability, multiply_car_words
from fieldcalc.perturbative_return import compile_perturbative_return


class NativeCarReachabilityTests(unittest.TestCase):
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
            provenance="node 52 native CAR reachability",
            resource_budget=500_000_000,
        )).system
        source = compile_perturbative_return(
            cls.system,
            moment_order=12,
            resource_budget=20_000_000,
        ).model
        cls.baseline = compile_graded_cyclic_return(
            source,
            resource_budget=20_000_000,
        ).model

    def test_normal_word_product_matches_serialized_car_action(self):
        mode_count = 3
        annihilators = tuple(
            car_annihilator(mode, mode_count) for mode in range(mode_count)
        )

        def matrix(label):
            creation, annihilation = label
            value = np.eye(1 << mode_count, dtype=complex)
            for mode in range(mode_count):
                if creation & (1 << mode):
                    value @= annihilators[mode].conj().T
            for mode in reversed(range(mode_count)):
                if annihilation & (1 << mode):
                    value @= annihilators[mode]
            return value

        cases = (
            ((0, 1), (1, 0)),
            ((0, 2), (1, 0)),
            ((3, 0), (0, 3)),
            ((1, 2), (4, 1)),
        )
        for left, right in cases:
            product = multiply_car_words(left, right, mode_count, update_budget=1_000)
            actual = sum(
                coefficient * matrix(label)
                for label, coefficient in product.terms
            )
            self.assertLess(np.linalg.norm(actual - matrix(left) @ matrix(right)), 1e-12)

    def test_native_closure_recovers_matrix_filtration_with_sparse_support(self):
        result = compile_native_graded_reachability(
            self.system,
            coefficient_order=4,
            tolerance=1e-10,
            resource_budget=20_000_000,
        )
        self.assertTrue(result.accepted, result.refusal)
        model = result.model
        self.assertEqual(model.filtration_ranks, self.baseline.filtration_ranks)
        self.assertEqual(model.support_by_grade, (2, 20, 26, 146, 100))
        self.assertEqual(model.retained_coefficients, 294)
        self.assertEqual(model.estimated_construction_operations, 128_000)
        self.assertEqual(model.normal_order_updates, 1_944)
        self.assertLess(model.free_recovery_residual, 2e-10)
        self.assertLess(model.interaction_recovery_residual, 2e-10)
        self.assertLess(
            model.retained_coefficients,
            model.matrix_retained_coefficients,
        )
        self.assertLess(
            model.estimated_construction_operations,
            self.baseline.cost.estimated_construction_operations,
        )
        self.assertEqual(len(model.directions), model.filtration_ranks[-1])
        self.assertEqual(model.free_generator.shape, (30, 30))
        self.assertEqual(model.interaction_generator.shape, (30, 30))
        self.assertEqual(model.reduced_source.shape, (30,))
        self.assertLess(model.native_closure_residual, 2e-10)

    def test_native_support_budget_is_refused(self):
        result = compile_native_graded_reachability(
            self.system,
            coefficient_order=4,
            tolerance=1e-10,
            resource_budget=1,
        )
        self.assertFalse(result.accepted)
        self.assertEqual(result.refusal.reason, "native CAR reachability budget exceeded")


if __name__ == "__main__":
    unittest.main()

import unittest

import numpy as np

from fieldcalc.car_words import (
    car_audited_endpoint_functional,
    decompose_charge_homogeneous,
)
from fieldcalc.graded_return import FunctionalPortRefusal, compile_graded_cyclic_return
from fieldcalc.impurity import AndersonRequest, car_annihilator, compile_anderson
from fieldcalc.perturbative_return import compile_perturbative_return


class GaussianCarConsumabilityTests(unittest.TestCase):
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
            provenance="node 50 Gaussian CAR consumability",
            resource_budget=500_000_000,
        )).system
        cls.source = compile_perturbative_return(
            cls.system,
            moment_order=12,
            resource_budget=20_000_000,
        ).model
        cls.endpoint = compile_graded_cyclic_return(
            cls.source,
            resource_budget=20_000_000,
        ).model

    def test_retained_insertions_have_stable_sparse_car_words(self):
        result = compile_graded_cyclic_return(
            self.source,
            resource_budget=20_000_000,
            functional_factory=car_audited_endpoint_functional(
                self.source,
                valuations=self.endpoint.valuations,
                local_dimension=4,
                word_budget=10_000,
            ),
        )
        self.assertTrue(result.accepted, result.refusal)
        receipt = result.model.functional_metadata

        self.assertTrue(receipt.count_stable)
        self.assertLess(receipt.maximum_recovery_residual, 2e-9)
        self.assertLess(receipt.total_word_occurrences, receipt.dense_word_bound)
        self.assertLessEqual(receipt.maximum_word_degree, 8)
        self.assertEqual(len(receipt.occurrences_by_valuation), 5)

    def test_car_recomposition_preserves_the_green_packet(self):
        car_model = compile_graded_cyclic_return(
            self.source,
            resource_budget=20_000_000,
            functional_factory=car_audited_endpoint_functional(
                self.source,
                valuations=self.endpoint.valuations,
                local_dimension=4,
                word_budget=10_000,
            ),
        ).model
        for z in (1j * self.system.matsubara_frequency, 0.35 + 0.20j):
            for actual, expected in zip(
                car_model.green_coefficients(z),
                self.endpoint.green_coefficients(z),
                strict=True,
            ):
                self.assertLess(abs(actual - expected), 2e-9)

    def test_mixed_charge_and_word_budget_are_refused(self):
        identity = np.eye(16)
        mixed = identity + car_annihilator(0, 4).conj().T
        with self.assertRaisesRegex(FunctionalPortRefusal, "mixed charge"):
            decompose_charge_homogeneous(mixed, mode_count=4, tolerance=1e-10)

        bounded = compile_graded_cyclic_return(
            self.source,
            resource_budget=20_000_000,
            functional_factory=car_audited_endpoint_functional(
                self.source,
                valuations=self.endpoint.valuations,
                local_dimension=4,
                word_budget=1,
            ),
        )
        self.assertFalse(bounded.accepted)
        self.assertEqual(bounded.refusal.reason, "Gaussian CAR word budget exceeded")


if __name__ == "__main__":
    unittest.main()

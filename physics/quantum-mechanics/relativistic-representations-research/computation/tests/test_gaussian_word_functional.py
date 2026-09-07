import unittest

import numpy as np

from fieldcalc.gaussian_functional import (
    LinearCarAction,
    anderson_word_native_functional,
    thermal_wick_expectation,
)
from fieldcalc.graded_return import compile_graded_cyclic_return
from fieldcalc.impurity import AndersonRequest, car_annihilator, compile_anderson
from fieldcalc.perturbative_return import compile_perturbative_return


class GaussianWordFunctionalTests(unittest.TestCase):
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
            provenance="node 51 word-native Gaussian functional",
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

    def test_wick_operation_matches_a_direct_free_bath_trace(self):
        energies = (-0.75, 0.75)
        beta = 2.0
        actions = (
            LinearCarAction(False, (1.0, 0.0), 0.7),
            LinearCarAction(True, (0.4, -0.2), 0.3),
            LinearCarAction(False, (0.0, 1.0), 0.0),
            LinearCarAction(True, (0.0, 1.0), 0.0),
        )
        actual = thermal_wick_expectation(actions, energies, beta).value

        annihilators = tuple(car_annihilator(mode, 2) for mode in range(2))
        numbers = tuple(action.conj().T @ action for action in annihilators)
        hamiltonian = sum(energy * number for energy, number in zip(energies, numbers))
        thermal = np.diag(np.exp(-beta * np.diag(hamiltonian).real))
        product = np.eye(4, dtype=complex)
        for action in actions:
            operator = sum(
                coefficient * (
                    annihilator.conj().T if action.creation else annihilator
                )
                for coefficient, annihilator in zip(
                    action.coefficients, annihilators, strict=True,
                )
            )
            evolved = np.exp(
                action.time * (
                    np.diag(hamiltonian).real[:, None]
                    - np.diag(hamiltonian).real[None, :]
                )
            ) * operator
            product @= evolved
        expected = np.trace(thermal @ product) / np.trace(thermal)
        self.assertLess(abs(actual - expected), 2e-12)
        self.assertEqual(
            thermal_wick_expectation(actions[:3], energies, beta).value,
            0j,
        )

    def test_word_native_port_preserves_the_reduced_green_packet(self):
        result = compile_graded_cyclic_return(
            self.source,
            resource_budget=500_000_000,
            functional_factory=anderson_word_native_functional(
                self.system,
                valuations=self.endpoint.valuations,
                local_dimension=4,
                quadrature_order=3,
                resource_budget=200_000_000,
                word_budget=10_000,
            ),
        )
        self.assertTrue(result.accepted, result.refusal)
        model = result.model
        receipt = model.functional_metadata
        self.assertEqual(model.materialized_endpoint_matrices, 0)
        self.assertEqual(receipt.reconstructed_bath_matrices, 0)
        self.assertEqual(receipt.word_occurrences, 182)
        self.assertEqual(receipt.distinct_word_count, 66)
        self.assertEqual(receipt.combined_word_terms, 182)
        self.assertEqual(receipt.quadrature_cells, 152)
        self.assertEqual(receipt.event_cells, 27_302)
        self.assertEqual(receipt.wick_evaluations, 74_446)
        self.assertEqual(receipt.cache_hits, 74_220)
        self.assertGreater(
            receipt.estimated_operations,
            receipt.endpoint_baseline_operations,
        )
        for z in (1j * self.system.matsubara_frequency, 0.35 + 0.20j, 40j):
            for actual, expected in zip(
                model.green_coefficients(z),
                self.endpoint.green_coefficients(z),
                strict=True,
            ):
                self.assertLess(abs(actual - expected), 5e-3)

    def test_invalid_quadrature_and_resource_budget_are_refused(self):
        coarse = compile_graded_cyclic_return(
            self.source,
            resource_budget=20_000_000,
            functional_factory=anderson_word_native_functional(
                self.system,
                valuations=self.endpoint.valuations,
                local_dimension=4,
                quadrature_order=2,
                resource_budget=20_000_000,
                word_budget=10_000,
            ),
        )
        bounded = compile_graded_cyclic_return(
            self.source,
            resource_budget=20_000_000,
            functional_factory=anderson_word_native_functional(
                self.system,
                valuations=self.endpoint.valuations,
                local_dimension=4,
                quadrature_order=3,
                resource_budget=1,
                word_budget=10_000,
            ),
        )
        word_bounded = compile_graded_cyclic_return(
            self.source,
            resource_budget=20_000_000,
            functional_factory=anderson_word_native_functional(
                self.system,
                valuations=self.endpoint.valuations,
                local_dimension=4,
                quadrature_order=3,
                resource_budget=20_000_000,
                word_budget=1,
            ),
        )
        self.assertFalse(coarse.accepted)
        self.assertEqual(
            coarse.refusal.reason,
            "word-native quadrature order must be at least three",
        )
        self.assertFalse(bounded.accepted)
        self.assertEqual(
            bounded.refusal.reason,
            "word-native functional budget exceeded",
        )
        self.assertFalse(word_bounded.accepted)
        self.assertEqual(
            word_bounded.refusal.reason,
            "word-native CAR word budget exceeded",
        )


if __name__ == "__main__":
    unittest.main()

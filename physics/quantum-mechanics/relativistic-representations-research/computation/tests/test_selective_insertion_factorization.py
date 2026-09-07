import unittest

from fieldcalc.graded_return import compile_graded_cyclic_return
from fieldcalc.impurity import AndersonRequest, compile_anderson
from fieldcalc.operator_factorization import audited_endpoint_functional
from fieldcalc.perturbative_return import compile_perturbative_return


class SelectiveInsertionFactorizationTests(unittest.TestCase):
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
            provenance="node 49 selective factorization",
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

    def test_generated_insertions_have_stable_selective_factorizations(self):
        result = compile_graded_cyclic_return(
            self.source,
            resource_budget=20_000_000,
            functional_factory=audited_endpoint_functional(
                self.source,
                local_dimension=4,
                factor_budget=480,
            ),
        )
        self.assertTrue(result.accepted, result.refusal)
        receipt = result.model.functional_metadata

        self.assertLess(receipt.maximum_recovery_residual, 2e-10)
        self.assertTrue(receipt.rank_stable)
        self.assertEqual(len(receipt.carrier_ranks), result.model.rank)
        self.assertEqual(len(receipt.insertion_ranks), result.model.rank)
        self.assertLess(receipt.total_insertion_factors, receipt.dense_local_bound)

    def test_recomposition_preserves_the_functional_target(self):
        factorized = compile_graded_cyclic_return(
            self.source,
            resource_budget=20_000_000,
            functional_factory=audited_endpoint_functional(
                self.source,
                local_dimension=4,
                factor_budget=480,
            ),
        ).model

        for z in (1j * self.system.matsubara_frequency, 0.35 + 0.20j):
            for actual, expected in zip(
                factorized.green_coefficients(z),
                self.endpoint.green_coefficients(z),
                strict=True,
            ):
                self.assertLess(abs(actual - expected), 2e-10)

    def test_factor_budget_and_dimension_mismatch_are_refused(self):
        bounded = compile_graded_cyclic_return(
            self.source,
            resource_budget=20_000_000,
            functional_factory=audited_endpoint_functional(
                self.source,
                local_dimension=4,
                factor_budget=1,
            ),
        )
        mismatched = compile_graded_cyclic_return(
            self.source,
            resource_budget=20_000_000,
            functional_factory=audited_endpoint_functional(
                self.source,
                local_dimension=5,
                factor_budget=480,
            ),
        )

        self.assertFalse(bounded.accepted)
        self.assertEqual(bounded.refusal.reason, "selective factor budget exceeded")
        self.assertFalse(mismatched.accepted)
        self.assertEqual(
            mismatched.refusal.reason,
            "local dimension does not divide the Hilbert dimension",
        )


if __name__ == "__main__":
    unittest.main()

import unittest

from fieldcalc.graded_return import compile_graded_cyclic_return
from fieldcalc.impurity import AndersonRequest, compile_anderson
from fieldcalc.path_functional import anderson_closed_path_functional
from fieldcalc.perturbative_return import compile_perturbative_return


class FunctionalPortTransferTests(unittest.TestCase):
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
            provenance="node 48 functional-port transfer",
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
        cls.path_result = compile_graded_cyclic_return(
            cls.source,
            resource_budget=500_000_000,
            functional_factory=anderson_closed_path_functional(
                cls.system,
                quadrature_order=5,
                resource_budget=450_000_000,
            ),
        )

    def test_closed_paths_supply_the_same_reduced_functional_port(self):
        self.assertTrue(self.path_result.accepted, self.path_result.refusal)
        path = self.path_result.model

        self.assertEqual(path.functional_kind, "closed interaction paths")
        self.assertEqual(path.materialized_endpoint_matrices, 0)
        self.assertGreater(path.functional_cells, 0)
        self.assertGreater(path.functional_error, 0.0)
        self.assertLess(path.functional_error, 2e-5)
        self.assertEqual(path.filtration_ranks, self.endpoint.filtration_ranks)

    def test_unchanged_recurrence_recovers_three_frequency_families(self):
        path = self.path_result.model
        tolerance = 4 * path.functional_error
        for z in (
            1j * self.system.matsubara_frequency,
            0.35 + 0.20j,
            40j,
        ):
            expected = self.endpoint.green_coefficients(z)
            actual = path.green_coefficients(z)
            for order in range(5):
                with self.subTest(z=z, order=order):
                    self.assertLess(abs(actual[order] - expected[order]), tolerance)

    def test_path_budget_and_quadrature_boundary_are_refused(self):
        too_coarse = compile_graded_cyclic_return(
            self.source,
            resource_budget=20_000_000,
            functional_factory=anderson_closed_path_functional(
                self.system,
                quadrature_order=2,
                resource_budget=20_000_000,
            ),
        )
        bounded = compile_graded_cyclic_return(
            self.source,
            resource_budget=20_000_000,
            functional_factory=anderson_closed_path_functional(
                self.system,
                quadrature_order=5,
                resource_budget=100,
            ),
        )

        self.assertFalse(too_coarse.accepted)
        self.assertEqual(
            too_coarse.refusal.reason,
            "closed-path quadrature order must be at least three",
        )
        self.assertFalse(bounded.accepted)
        self.assertEqual(bounded.refusal.reason, "closed-path functional budget exceeded")


if __name__ == "__main__":
    unittest.main()

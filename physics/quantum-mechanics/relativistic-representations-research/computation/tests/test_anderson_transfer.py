import math
import unittest

import numpy as np

from fieldcalc.impurity import (
    AndersonRequest,
    compile_anderson,
)
from fieldcalc.impurity_expansion import (
    compress_fermion_contractions,
    determinant_green_coefficients,
)


class AndersonTransferTests(unittest.TestCase):
    def setUp(self):
        result = compile_anderson(AndersonRequest(
            impurity_energy=-1.0,
            interaction=2.0,
            bath_energies=(-0.75, 0.75),
            hybridizations=(1.0 / 3.0, 1.0 / 3.0),
            beta=2.0,
            matsubara_index=0,
            coefficient_order=4,
            quadrature_order=12,
            provenance="node 41 frozen Anderson bench",
            resource_budget=500_000_000,
        ))
        self.assertTrue(result.accepted, result.refusal)
        self.system = result.system

    def test_car_action_generates_relations_and_hermitian_model(self):
        certificate = self.system.car_certificate()

        self.assertLess(certificate.maximum_residual, 1e-14)
        self.assertLess(
            np.linalg.norm(self.system.hamiltonian(0.37).conj().T
                           - self.system.hamiltonian(0.37)),
            1e-14,
        )

    def test_quadratic_bath_elimination_keeps_local_interaction(self):
        z = 0.4 + 0.7j
        expected = (1.0 / 9.0) * (
            1.0 / (z + 0.75) + 1.0 / (z - 0.75)
        )

        self.assertAlmostEqual(self.system.hybridization(z), expected)
        self.assertEqual(self.system.request.interaction, 2.0)

    def test_car_recurrence_generates_the_determinant_quotient(self):
        kernel = np.array([
            [1.0 + 0.2j, -0.3, 0.7],
            [0.1, 0.9 - 0.4j, -0.2],
            [0.6, 0.5, -0.8 + 0.1j],
        ])
        receipt = compress_fermion_contractions(kernel)

        self.assertAlmostEqual(receipt.expanded, receipt.determinant)
        self.assertEqual(receipt.graph_count, math.factorial(3))
        self.assertEqual(receipt.kernel_entries, 9)

    def test_block_coefficients_are_even_and_reconstruct_exact_green(self):
        coefficients = self.system.green_coefficients()

        self.assertLess(abs(coefficients.values[1]), 2e-11)
        self.assertLess(abs(coefficients.values[3]), 2e-11)
        coupling = 0.12
        truncated = sum(
            value * coupling**order
            for order, value in enumerate(coefficients.values)
        )
        exact = self.system.green(coupling)
        self.assertLess(abs(exact - truncated), 2e-7)
        self.assertGreater(coefficients.cost.block_dimension, 64)
        self.assertGreater(coefficients.cost.exponentials, 0)

    def test_action_factored_determinant_route_reaches_same_green_coefficients(self):
        block = self.system.green_coefficients()
        determinant = determinant_green_coefficients(
            self.system,
            quadrature_order=3,
        )

        for order in (0, 2, 4):
            with self.subTest(order=order):
                self.assertLess(
                    abs(determinant.values[order] - block.values[order]),
                    9e-4,
                )
        self.assertEqual(determinant.values[1], 0j)
        self.assertEqual(determinant.values[3], 0j)
        self.assertEqual(determinant.cost.quadrature_points, 1_389)
        self.assertEqual(determinant.cost.determinant_cells, 47_016)
        self.assertEqual(determinant.cost.pairing_histories, 62_568)

    def test_determinant_route_refuses_unbounded_time_cell_growth(self):
        bounded = compile_anderson(AndersonRequest(
            impurity_energy=-1.0,
            interaction=2.0,
            bath_energies=(-0.75, 0.75),
            hybridizations=(1.0 / 3.0, 1.0 / 3.0),
            beta=2.0,
            matsubara_index=0,
            coefficient_order=4,
            quadrature_order=12,
            provenance="bounded determinant route",
            resource_budget=1_000_000,
        )).system

        with self.assertRaisesRegex(ValueError, "transfer budget exceeded"):
            determinant_green_coefficients(bounded, quadrature_order=8)

    def test_invalid_requests_are_refused(self):
        result = compile_anderson(AndersonRequest(
            impurity_energy=-1.0,
            interaction=2.0,
            bath_energies=(-0.75,),
            hybridizations=(1.0 / 3.0, 1.0 / 4.0),
            beta=2.0,
            matsubara_index=0,
            coefficient_order=4,
            quadrature_order=12,
            provenance="invalid adapter",
            resource_budget=10,
        ))

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.refusal.reason,
            "bath energies and hybridizations have different lengths",
        )


if __name__ == "__main__":
    unittest.main()

import unittest

import numpy as np
from scipy.optimize import brentq

from fieldcalc.impurity import AndersonRequest, compile_anderson
from fieldcalc.pauli_fierz import PauliFierzRequest, compile_pauli_fierz
from fieldcalc.return_reduction import (
    ReturnProblem,
    anderson_thermal_problem,
    compile_cyclic_return,
    pauli_fierz_problem,
)


class CyclicReturnReductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pauli_fierz = compile_pauli_fierz(PauliFierzRequest(
            primitive_dimension=28,
            matter_levels=6,
            photon_frequencies=(0.65, 1.10),
            field_coefficients=(0.30, 0.16),
            photon_cutoff=2,
            coupling=0.08,
            resolution=0.20,
            provenance="node 43 Pauli-Fierz transfer",
            resource_budget=2_000_000,
        )).system
        cls.anderson = compile_anderson(AndersonRequest(
            impurity_energy=-1.0,
            interaction=2.0,
            bath_energies=(-0.75, 0.75),
            hybridizations=(1.0 / 3.0, 1.0 / 3.0),
            beta=2.0,
            matsubara_index=0,
            coefficient_order=4,
            quadrature_order=12,
            provenance="node 43 Anderson transfer",
            resource_budget=500_000_000,
        )).system

    def test_projection_preserves_generated_moments(self):
        spectrum = np.array([-1.7, -0.4, 0.2, 0.9, 1.8, 2.6])
        source = np.array([1.0, -0.3, 0.7, 0.2, -0.5, 0.4])[:, None]
        problem = ReturnProblem.from_diagonal(
            spectrum,
            source,
            provenance="exact moment fixture",
        )

        result = compile_cyclic_return(problem, depth=3, resource_budget=100_000)

        self.assertTrue(result.accepted, result.refusal)
        self.assertEqual(result.model.rank, 3)
        self.assertLess(max(result.model.moment_residuals(6)), 2e-11)

    def test_pauli_fierz_adapter_reduces_the_visible_q_return(self):
        problem = pauli_fierz_problem(self.pauli_fierz)
        result = compile_cyclic_return(problem, depth=4, resource_budget=2_000_000)

        self.assertTrue(result.accepted, result.refusal)
        self.assertLess(result.model.rank, problem.dimension)
        self.assertLess(max(result.model.moment_residuals(8)), 2e-9)
        z = self.pauli_fierz.matter_ground_energy + 0.82 + 0.20j
        self.assertLess(
            np.linalg.norm(result.model.evaluate(z) - problem.evaluate(z)),
            1e-6,
        )
        certificate = result.model.certified_evaluate(z)
        actual_return_error = np.linalg.norm(certificate.value - problem.evaluate(z), 2)
        self.assertLessEqual(actual_return_error, certificate.error_bound)

        retained = self.pauli_fierz.hamiltonian[np.ix_(
            self.pauli_fierz.retained,
            self.pauli_fierz.retained,
        )]

        def determinant(energy):
            return float(np.linalg.det(
                energy * np.eye(3) - retained - result.model.evaluate(energy)
            ).real)

        grid = np.linspace(
            self.pauli_fierz.matter_ground_energy - 0.5,
            self.pauli_fierz.matter_ground_energy + 0.5,
            257,
        )
        bracket = next(
            pair for pair in zip(grid, grid[1:])
            if determinant(pair[0]) * determinant(pair[1]) <= 0
        )
        pole = brentq(determinant, *bracket)
        incoming = np.array([1.0, 1.0j]) / np.sqrt(2.0)
        outgoing = np.array([1.0, -1.0]) / np.sqrt(2.0)
        source = np.r_[0j, incoming]
        detector = np.r_[0j, outgoing]
        reduced = detector.conj() @ np.linalg.solve(
            z * np.eye(3) - retained - result.model.evaluate(z),
            source,
        )
        exact_open = self.pauli_fierz.open_receipt(
            self.pauli_fierz.matter_ground_energy + 0.82,
            incoming,
            outgoing,
        ).full_value

        self.assertLess(abs(pole - self.pauli_fierz.bound_receipt().full_energy), 2e-9)
        self.assertLess(abs(reduced - exact_open), 7e-6)
        self.assertLess(
            result.model.cost.estimated_setup_operations,
            result.model.cost.baseline_setup_operations,
        )
        self.assertEqual(result.model.cost.break_even_queries, 1)
        self.assertEqual(result.model.cost.certified_break_even_queries, 1)

    def test_anderson_adapter_constructs_the_same_thermal_green_function(self):
        coupling = 0.12
        problem = anderson_thermal_problem(self.anderson, coupling)
        z = 1j * self.anderson.matsubara_frequency

        self.assertLess(abs(problem.evaluate(z) - self.anderson.green(coupling)), 2e-13)
        self.assertAlmostEqual(float(np.linalg.norm(problem.source) ** 2), 1.0)

        result = compile_cyclic_return(problem, depth=10, resource_budget=4_000_000)
        self.assertTrue(result.accepted, result.refusal)
        self.assertLess(result.model.rank, problem.dimension)
        self.assertLess(abs(result.model.evaluate(z) - problem.evaluate(z)), 2e-6)
        self.assertLess(
            abs(result.model.evaluate(0.35 + 0.20j) - problem.evaluate(0.35 + 0.20j)),
            1.2e-4,
        )
        self.assertGreater(result.model.cost.baseline_setup_operations, 0)
        self.assertGreater(result.model.cost.break_even_queries, 200)
        certificate = result.model.certified_evaluate(0.35 + 0.20j)
        actual_error = abs(certificate.value[0, 0] - problem.evaluate(0.35 + 0.20j)[0, 0])
        self.assertLessEqual(actual_error, certificate.error_bound)
        self.assertGreater(result.model.cost.certified_break_even_queries, 200)

        with self.assertRaisesRegex(ValueError, "off-axis"):
            result.model.certified_evaluate(0.35)

    def test_invalid_generators_and_budgets_are_refused(self):
        nonhermitian = ReturnProblem.from_dense(
            np.array([[0.0, 1.0], [0.0, 0.0]]),
            np.ones((2, 1)),
            provenance="invalid generator",
        )
        invalid = compile_cyclic_return(nonhermitian, depth=2, resource_budget=100)
        valid = ReturnProblem.from_diagonal(
            np.arange(8.0),
            np.ones((8, 1)),
            provenance="budget fixture",
        )
        bounded = compile_cyclic_return(valid, depth=4, resource_budget=10)

        self.assertFalse(invalid.accepted)
        self.assertEqual(invalid.refusal.reason, "return generator is not Hermitian")
        self.assertFalse(bounded.accepted)
        self.assertEqual(bounded.refusal.reason, "cyclic return budget exceeded")


if __name__ == "__main__":
    unittest.main()

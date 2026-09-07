import unittest

from sympy import Matrix, diag

from fieldcalc.fermion_line import (
    compile_fermion_line_amplitude,
    compile_fermion_ward_boundary,
)


class FermionSubsetTransferTests(unittest.TestCase):
    def setUp(self):
        self.metric = diag(1, 1, 1)
        self.initial = Matrix((1, 2, 1))
        self.momenta = tuple(Matrix(vector) for vector in (
            (1, 0, 1), (0, 1, 1), (1, -1, 0), (-1, 1, 2),
        ))
        self.polarizations = tuple(Matrix(vector) for vector in (
            (0, 1, 0), (1, 0, -1), (1, 1, 1), (2, -1, 0),
        ))

    def test_subset_grade_state_recovers_all_ordered_histories(self):
        subset = compile_fermion_line_amplitude(
            self.metric,
            self.initial,
            self.momenta,
            self.polarizations,
            1,
            state_budget=32,
            route="subset grade",
        )
        direct = compile_fermion_line_amplitude(
            self.metric,
            self.initial,
            self.momenta,
            self.polarizations,
            1,
            state_budget=32,
            route="ordered histories",
        )

        self.assertTrue(subset.accepted)
        self.assertTrue(direct.accepted)
        self.assertEqual(subset.amplitude, direct.amplitude)
        self.assertEqual(subset.states_visited, 16)
        self.assertEqual(subset.ordered_histories, 24)
        self.assertEqual(subset.transition_terms, 32)
        self.assertEqual(direct.history_steps, 96)
        self.assertLess(subset.total_updates, direct.total_updates)

    def test_subset_grade_state_preserves_the_endpoint_ward_identity(self):
        for label in range(4):
            ward = compile_fermion_ward_boundary(
                self.metric,
                self.initial,
                self.momenta,
                self.polarizations,
                1,
                contracted_label=label,
                state_budget=32,
            )

            self.assertTrue(ward.accepted)
            self.assertEqual(ward.residual.term_count, 0)

    def test_reduction_grows_after_the_two_photon_boundary(self):
        momenta = self.momenta + (Matrix((2, 1, -1)),)
        polarizations = self.polarizations + (Matrix((-1, 2, 1)),)
        subset_costs = []
        direct_costs = []
        for count in range(1, 6):
            subset = compile_fermion_line_amplitude(
                self.metric, self.initial, momenta[:count], polarizations[:count], 1,
                state_budget=128, route="subset grade",
            )
            direct = compile_fermion_line_amplitude(
                self.metric, self.initial, momenta[:count], polarizations[:count], 1,
                state_budget=128, route="ordered histories",
            )
            self.assertEqual(subset.amplitude, direct.amplitude)
            subset_costs.append(subset.total_updates)
            direct_costs.append(direct.total_updates)

        self.assertEqual(subset_costs, [2, 37, 263, 1025, 3317])
        self.assertEqual(direct_costs, [2, 37, 351, 2490, 18292])

    def test_subset_route_refuses_an_insufficient_state_budget(self):
        result = compile_fermion_line_amplitude(
            self.metric,
            self.initial,
            self.momenta,
            self.polarizations,
            1,
            state_budget=15,
            route="subset grade",
        )

        self.assertFalse(result.accepted)
        self.assertEqual(result.refusal.reason, "fermion subset state budget exceeded")


if __name__ == "__main__":
    unittest.main()

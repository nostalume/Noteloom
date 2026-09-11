from fractions import Fraction
import unittest

from occ.linear import construct_observable_closure


Q = Fraction


def transpose(matrix):
    return tuple(tuple(row[j] for row in matrix) for j in range(len(matrix[0])))


def matvec(matrix, vector):
    return tuple(
        sum((entry * value for entry, value in zip(row, vector)), Q(0))
        for row in matrix
    )


def dot(left, right):
    return sum((a * b for a, b in zip(left, right)), Q(0))


class ObservableClosureTests(unittest.TestCase):
    def test_center_of_mass_closes_without_constructing_normal_modes(self):
        restoring_map = (
            (Q(6), Q(-1), Q(0), Q(-1)),
            (Q(-1), Q(6), Q(-1), Q(0)),
            (Q(0), Q(-1), Q(6), Q(-1)),
            (Q(-1), Q(0), Q(-1), Q(6)),
        )
        center_of_mass = (Q(1, 4),) * 4

        result = construct_observable_closure(
            restoring_map,
            center_of_mass,
            max_dimension=2,
        )

        self.assertEqual(result.status, "closed")
        self.assertEqual(result.closure_dimension, 1)
        self.assertEqual(result.basis, (center_of_mass,))
        self.assertEqual(result.reduced_second_order_operator, ((Q(4),),))
        self.assertEqual(result.cost.full_unknowns, 4)
        self.assertEqual(result.cost.reduced_unknowns, 1)
        self.assertEqual(result.cost.law_actions, 1)
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_generated_reduction_recovers_the_same_observable_acceleration(self):
        restoring_map = (
            (Q(1), Q(0), Q(0), Q(0)),
            (Q(0), Q(1), Q(0), Q(0)),
            (Q(0), Q(0), Q(4), Q(0)),
            (Q(0), Q(0), Q(0), Q(4)),
        )
        mean_position = (Q(1, 4),) * 4
        state = (Q(2), Q(-1), Q(3), Q(5))

        result = construct_observable_closure(restoring_map, mean_position)

        self.assertEqual(result.status, "closed")
        self.assertEqual(result.closure_dimension, 2)
        self.assertEqual(
            result.reduced_second_order_operator,
            ((Q(0), Q(1)), (Q(-4), Q(5))),
        )
        reduced_state = result.project(state)
        full_acceleration = -dot(
            mean_position,
            matvec(restoring_map, state),
        )
        reduced_acceleration = -dot(
            result.reduced_second_order_operator[0],
            reduced_state,
        )
        self.assertEqual(reduced_acceleration, full_acceleration)
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_transfer_to_irregular_reciprocal_couplings_preserves_scalar_closure(self):
        restoring_map = (
            (Q(7), Q(-2), Q(-1), Q(0)),
            (Q(-2), Q(9), Q(-3), Q(0)),
            (Q(-1), Q(-3), Q(8), Q(0)),
            (Q(0), Q(0), Q(0), Q(4)),
        )
        center_of_mass = (Q(1, 4),) * 4

        result = construct_observable_closure(restoring_map, center_of_mass)

        self.assertEqual(result.status, "closed")
        self.assertEqual(result.closure_dimension, 1)
        self.assertEqual(result.reduced_second_order_operator, ((Q(4),),))

    def test_mass_weighted_observable_closes_for_unequal_masses(self):
        restoring_map = (
            (Q(6), Q(-2), Q(0)),
            (Q(-1), Q(13, 2), Q(-3, 2)),
            (Q(0), Q(-1), Q(5)),
        )
        center_of_mass = (Q(1, 6), Q(1, 3), Q(1, 2))

        result = construct_observable_closure(restoring_map, center_of_mass)

        self.assertEqual(result.status, "closed")
        self.assertEqual(result.closure_dimension, 1)
        self.assertEqual(result.reduced_second_order_operator, ((Q(4),),))

    def test_broken_common_restoring_frequency_exposes_next_observable(self):
        restoring_map = (
            (Q(4), Q(0), Q(0)),
            (Q(0), Q(5), Q(0)),
            (Q(0), Q(0), Q(6)),
        )
        mean_position = (Q(1, 3),) * 3

        result = construct_observable_closure(
            restoring_map,
            mean_position,
            max_dimension=1,
        )

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "closure_budget_exceeded")
        self.assertEqual(result.obstruction.required_dimension_at_least, 2)
        self.assertEqual(
            result.obstruction.next_observable,
            (Q(4, 3), Q(5, 3), Q(2)),
        )

    def test_zero_observable_is_rejected(self):
        result = construct_observable_closure(
            ((Q(1), Q(0)), (Q(0), Q(1))),
            (Q(0), Q(0)),
        )

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "zero_observable")

    def test_noninteger_equation_budget_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "positive integer"):
            construct_observable_closure(
                ((Q(1), Q(0)), (Q(0), Q(1))),
                (Q(1), Q(0)),
                max_dimension=1.5,
            )


if __name__ == "__main__":
    unittest.main()

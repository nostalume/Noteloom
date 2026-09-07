import unittest
from itertools import permutations
from math import factorial

from sympy import Matrix, Rational, eye, symbols

from fieldcalc.grammar import compile_scalar_metric_jet


class OffShellGraphCompletionTests(unittest.TestCase):
    def test_action_ports_generate_the_normalized_one_particle_irreducible_packet(self):
        # Two labelled cubic vertices, each with two interchangeable scalar ports.
        cubic_scalar_ports = tuple(
            (vertex, port) for vertex in range(2) for port in range(2)
        )
        external_assignments = tuple(permutations(cubic_scalar_ports, 2))
        rainbow_histories = tuple(
            assignment
            for assignment in external_assignments
            if assignment[0][0] != assignment[1][0]
        )
        reducible_histories = tuple(
            assignment
            for assignment in external_assignments
            if assignment[0][0] == assignment[1][0]
        )
        cubic_denominator = factorial(2) * factorial(2) ** 2

        # One contact vertex: two external assignments and one h self-pairing.
        contact_histories = factorial(2)
        contact_denominator = factorial(2) * factorial(2)

        self.assertEqual(len(external_assignments), 12)
        self.assertEqual(len(rainbow_histories), 8)
        self.assertEqual(len(reducible_histories), 4)
        self.assertEqual(Rational(len(rainbow_histories), cubic_denominator), 1)
        self.assertEqual(
            Rational(len(reducible_histories), cubic_denominator), Rational(1, 2)
        )
        self.assertEqual(
            -Rational(contact_histories, contact_denominator), Rational(-1, 2)
        )

    def test_second_scalar_action_jet_is_generated_from_metric_deformation(self):
        deformation = Matrix.diag(2, -1)

        jet = compile_scalar_metric_jet(deformation, order=2)

        self.assertEqual(jet.volume, (1, Rational(1, 2), Rational(-9, 8)))
        self.assertEqual(
            jet.inverse_metric,
            (eye(2), Matrix.diag(-2, 1), Matrix.diag(4, 1)),
        )
        self.assertEqual(
            jet.densitized_inverse,
            (
                eye(2),
                Matrix.diag(Rational(-3, 2), Rational(3, 2)),
                Matrix.diag(Rational(15, 8), Rational(3, 8)),
            ),
        )
        self.assertEqual(
            jet.inverse_metric[1] + deformation * jet.inverse_metric[0],
            Matrix.zeros(2),
        )
        self.assertEqual(
            jet.inverse_metric[2] + deformation * jet.inverse_metric[1],
            Matrix.zeros(2),
        )
        trace_one = deformation.trace()
        trace_two = (deformation**2).trace()
        self.assertEqual(2 * jet.volume[1], trace_one)
        self.assertEqual(
            jet.volume[1] ** 2 + 2 * jet.volume[2],
            (trace_one**2 - trace_two) / 2,
        )
        self.assertEqual(
            jet.densitized_inverse[2],
            jet.inverse_metric[2]
            + jet.volume[1] * jet.inverse_metric[1]
            + jet.volume[2] * jet.inverse_metric[0],
        )

    def test_action_jet_transfers_to_a_nilpotent_deformation(self):
        deformation = Matrix([[0, 1, 0], [0, 0, 1], [0, 0, 0]])

        jet = compile_scalar_metric_jet(deformation, order=2)

        self.assertEqual(jet.volume, (1, 0, 0))
        self.assertEqual(jet.inverse_metric[2], deformation**2)
        self.assertEqual(jet.densitized_inverse, jet.inverse_metric)

    def test_action_jet_refuses_an_unavailable_order(self):
        zeroth_jet = compile_scalar_metric_jet(eye(2), order=0)
        self.assertEqual(zeroth_jet.volume, (1,))
        self.assertEqual(len(zeroth_jet.inverse_metric), 1)
        self.assertEqual(len(zeroth_jet.densitized_inverse), 1)
        with self.assertRaisesRegex(ValueError, "orders 0 through 2"):
            compile_scalar_metric_jet(eye(2), order=3)

    def test_action_jet_refuses_a_nonendomorphism(self):
        with self.assertRaisesRegex(ValueError, "square endomorphism"):
            compile_scalar_metric_jet(Matrix.zeros(2, 3), order=2)

    def test_scalar_vertex_divergence_factors_through_inverse_kernels(self):
        p_squared, prime_squared, scalar_product, mass_squared = symbols(
            "p2 pp2 s m2"
        )

        # Coefficients in the invariant basis (P_p, P_p').
        candidate_divergence = Matrix(
            [prime_squared - scalar_product, scalar_product - p_squared]
        )
        metric_repair_divergence = Matrix(
            [scalar_product - mass_squared, mass_squared - scalar_product]
        )
        compiled_divergence = candidate_divergence + metric_repair_divergence
        inverse_kernel_syzygy = Matrix(
            [prime_squared - mass_squared, -(p_squared - mass_squared)]
        )

        self.assertEqual(compiled_divergence, inverse_kernel_syzygy)
        self.assertEqual(
            compiled_divergence.subs(
                {p_squared: mass_squared, prime_squared: mass_squared}
            ),
            Matrix.zeros(2, 1),
        )

    def test_longitudinal_contraction_collapses_an_internal_scalar_edge(self):
        internal_inverse, external_inverse = symbols("E_k E_p", nonzero=True)
        scalar_edge = 1 / internal_inverse
        ward_residual = Matrix([internal_inverse, -external_inverse])

        off_shell_composite = scalar_edge * ward_residual
        on_shell_composite = off_shell_composite.subs(external_inverse, 0)

        self.assertEqual(
            off_shell_composite,
            Matrix([1, -external_inverse / internal_inverse]),
        )
        self.assertEqual(on_shell_composite, Matrix([1, 0]))

    def test_action_contact_closes_internal_ward_descendants(self):
        external_left, external_right, scalar_edge = symbols("E_L E_R Delta")
        internal_left, internal_right = symbols("X_L X_R")
        boundary_left, boundary_right = symbols("Y_L Y_R")
        rainbow_variation = (
            internal_left
            + internal_right
            - scalar_edge
            * (external_left * boundary_left + external_right * boundary_right)
        )
        weighted_contact_variation = -internal_left - internal_right

        packet_variation = rainbow_variation + weighted_contact_variation

        self.assertEqual(
            packet_variation,
            -scalar_edge
            * (external_left * boundary_left + external_right * boundary_right),
        )
        self.assertEqual(
            packet_variation.subs({external_left: 0, external_right: 0}), 0
        )


if __name__ == "__main__":
    unittest.main()

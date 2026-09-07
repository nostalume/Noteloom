import unittest

from sympy import Matrix, Rational

from fieldcalc.grammar import compile_scalar_metric_vertex


class ScalarMetricVertexTests(unittest.TestCase):
    def test_cubic_vertex_generates_the_inverse_kernel_ward_identity(self):
        metric = Matrix.diag(1, -1)
        incoming = Matrix([2, 1])
        outgoing = Matrix([3, -1])
        gauge_vector = Matrix([1, 2])
        transfer = outgoing - incoming
        transfer_covector = metric * transfer
        gauge_covector = metric * gauge_vector
        gauge_deformation = (
            transfer * gauge_covector.T + gauge_vector * transfer_covector.T
        )
        mass_squared = Rational(2)

        vertex = compile_scalar_metric_vertex(
            metric,
            incoming,
            outgoing,
            mass_squared,
            (gauge_deformation,),
        )

        def dot(left, right):
            return (left.T * metric * right)[0]

        expected = (
            (dot(outgoing, outgoing) - mass_squared) * dot(incoming, gauge_vector)
            - (dot(incoming, incoming) - mass_squared) * dot(outgoing, gauge_vector)
        )
        self.assertEqual(vertex.value, expected)

    def test_contact_vertex_is_the_polarization_of_the_action_jet(self):
        metric = Matrix.eye(2)
        incoming = Matrix([2, -1])
        outgoing = Matrix([1, 3])
        mass_squared = Rational(3)
        left = Matrix([[1, 2], [2, 0]])
        right = Matrix([[0, 1], [1, 3]])

        mixed = compile_scalar_metric_vertex(
            metric, incoming, outgoing, mass_squared, (left, right)
        )
        combined = compile_scalar_metric_vertex(
            metric, incoming, outgoing, mass_squared, (left + right, left + right)
        )
        left_diagonal = compile_scalar_metric_vertex(
            metric, incoming, outgoing, mass_squared, (left, left)
        )
        right_diagonal = compile_scalar_metric_vertex(
            metric, incoming, outgoing, mass_squared, (right, right)
        )

        self.assertEqual(
            mixed.value,
            (combined.value - left_diagonal.value - right_diagonal.value) / 2,
        )
        self.assertEqual(
            mixed.densitized_inverse,
            compile_scalar_metric_vertex(
                metric, incoming, outgoing, mass_squared, (right, left)
            ).densitized_inverse,
        )

    def test_vertex_edge_packet_is_invariant_under_field_rescaling(self):
        metric = Matrix.eye(2)
        incoming = Matrix([2, -1])
        outgoing = Matrix([1, 3])
        mass_squared = Rational(3)
        deformation = Matrix([[1, 2], [2, 0]])
        scale = Rational(3)

        cubic = compile_scalar_metric_vertex(
            metric, incoming, outgoing, mass_squared, (deformation,)
        ).value
        contact = compile_scalar_metric_vertex(
            metric, incoming, outgoing, mass_squared, (deformation, deformation)
        ).value
        scaled_cubic = compile_scalar_metric_vertex(
            metric, incoming, outgoing, mass_squared, (deformation / scale,)
        ).value
        scaled_contact = compile_scalar_metric_vertex(
            metric,
            incoming,
            outgoing,
            mass_squared,
            (deformation / scale, deformation / scale),
        ).value
        scaled_edge = scale**2

        self.assertEqual(scaled_cubic, cubic / scale)
        self.assertEqual(scaled_contact, contact / scale**2)
        self.assertEqual(scaled_cubic**2 * scaled_edge, cubic**2)
        self.assertEqual(scaled_contact * scaled_edge, contact)

    def test_vertex_compiler_refuses_an_unsupported_action_order(self):
        with self.assertRaisesRegex(ValueError, "one or two metric deformations"):
            compile_scalar_metric_vertex(
                Matrix.eye(2), Matrix([1, 0]), Matrix([0, 1]), 1, ()
            )

    def test_vertex_compiler_refuses_a_nonsymmetric_metric_deformation(self):
        with self.assertRaisesRegex(ValueError, "metric-self-adjoint"):
            compile_scalar_metric_vertex(
                Matrix.eye(2),
                Matrix([1, 0]),
                Matrix([0, 1]),
                1,
                (Matrix([[0, 1], [0, 0]]),),
            )


if __name__ == "__main__":
    unittest.main()

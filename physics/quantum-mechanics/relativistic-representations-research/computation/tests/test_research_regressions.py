import unittest

from sympy import Matrix, Rational, sqrt, symbols

from fieldcalc.exact import kernel_certificate
from fieldcalc.measures import curvature_threshold_power
from fieldcalc.residual import (
    ResidualRequest,
    compare_carrier_costs,
    resolve_residual,
    source_adapter_inverse,
)


class ResearchRegressionTests(unittest.TestCase):
    def test_curvature_threshold_power_is_generated(self):
        self.assertEqual(curvature_threshold_power(spatial_dimension=3, spin=0), 1)
        self.assertEqual(curvature_threshold_power(spatial_dimension=3, spin=2), 5)

    def test_direct_constrained_route_has_no_generic_cost_gain(self):
        verdict = compare_carrier_costs(spin=3)
        self.assertEqual(verdict.preferred, "compensated")
        self.assertGreater(verdict.direct_load, verdict.compensated_load)

    def test_single_layer_preparation_is_presentation_neutral(self):
        verdict = compare_carrier_costs(spin=2, active_layers=1)
        self.assertEqual(verdict.preferred, "tie")
        self.assertEqual(verdict.active_direct_solves, verdict.active_compensated_solves)

    def test_spin_two_traceful_source_forces_the_generated_adapter(self):
        # Basis: (U sigma, P_p^2 Q_p^(-1) sigma), not spacetime components.
        divergence = Matrix([[2, 2]])
        trace = Matrix([[8, 2]])
        pairing = Matrix([[8, 2], [2, 2]])
        source = kernel_certificate(divergence).basis[0]

        self.assertNotEqual(trace * source, Matrix.zeros(1, 1))
        inverse = source_adapter_inverse(spin=2, adapter_coefficient=Rational(-1, 4))
        trace_insert = Matrix([[8, 2], [0, 0]])
        adapted = Matrix.eye(2) + inverse.coefficient * trace_insert

        unadapted_edge = (source.T * pairing * source)[0]
        adapted_edge = (source.T * pairing * adapted * source)[0]
        self.assertEqual(inverse.coefficient, Rational(-1, 4))
        self.assertEqual(
            inverse.operation.terms,
            {(): Rational(1), ("U", "T"): Rational(-1, 4)},
        )
        self.assertEqual(inverse.residual, (0,))
        self.assertEqual(unadapted_edge, 6)
        self.assertEqual(adapted_edge, -3)

    def test_curvature_readout_annihilates_the_same_adapter(self):
        inverse = source_adapter_inverse(spin=2, adapter_coefficient=Rational(-1, 4))
        trace_insert = Matrix([[8, 2], [0, 0]])
        adapted = Matrix.eye(2) + inverse.coefficient * trace_insert
        curvature_readout = Matrix([[0, 1]])

        self.assertEqual(curvature_readout * adapted, curvature_readout)

    def test_source_adapter_refuses_a_traceless_rank_boundary(self):
        with self.assertRaisesRegex(ValueError, "traceful spin cell"):
            source_adapter_inverse(spin=1, adapter_coefficient=Rational(-1, 4))

    def test_source_adapter_refuses_a_singular_trace_action(self):
        with self.assertRaisesRegex(ValueError, "singular"):
            source_adapter_inverse(spin=2, adapter_coefficient=Rational(-1, 8))

    def test_scalar_vertex_is_generated_but_retains_improvement_freedom(self):
        scalar_product, mass_squared, transfer_square, improvement = symbols(
            "s m2 q2 xi"
        )
        obstruction = scalar_product - mass_squared
        repair = resolve_residual(
            ResidualRequest(
                channels=(obstruction,),
                correction_columns=((2,),),
                names=("metric insertion",),
                provenance="on-shell scalar spin-two vertex",
            )
        )

        self.assertTrue(repair.accepted)
        self.assertEqual(repair.coefficients, ((mass_squared - scalar_product) / 2,))
        self.assertEqual(repair.remaining, (0,))
        self.assertEqual(2 * transfer_square - 2 * transfer_square, 0)
        trace = 2 * scalar_product - 4 * obstruction - 6 * improvement * transfer_square
        self.assertEqual(trace, 4 * mass_squared - 2 * scalar_product - 6 * improvement * transfer_square)

    def test_two_scalar_spin_two_vertices_generate_three_external_orbits(self):
        labels = (1, 2, 3, 4)
        first = labels[0]
        partitions = set()
        for mate in labels[1:]:
            remainder = tuple(label for label in labels if label not in (first, mate))
            pairs = tuple(sorted((tuple(sorted((first, mate))), tuple(sorted(remainder)))))
            partitions.add(pairs)

        self.assertEqual(
            partitions,
            {
                ((1, 2), (3, 4)),
                ((1, 3), (2, 4)),
                ((1, 4), (2, 3)),
            },
        )

    def test_fixed_scalar_exchange_matches_the_component_baseline(self):
        metric = Matrix.diag(1, -1, -1, -1)
        mass = Rational(1)
        momentum = Rational(1, 2)
        energy = sqrt(mass**2 + momentum**2)
        p1 = Matrix([energy, 0, 0, momentum])
        p2 = Matrix([energy, 0, 0, -momentum])
        p3 = Matrix([energy, momentum, 0, 0])
        p4 = Matrix([energy, -momentum, 0, 0])

        def dot(left, right):
            return (left.T * metric * right)[0]

        def current(incoming, outgoing):
            scalar = dot(incoming, outgoing) - mass**2
            return incoming * outgoing.T + outgoing * incoming.T - metric * scalar

        left = current(p1, p3)
        right = current(p2, p4)
        component_pairing = sum(
            (metric * left * metric)[row, column] * right[row, column]
            for row in range(4)
            for column in range(4)
        )
        left_trace = sum(
            metric[row, column] * left[row, column]
            for row in range(4)
            for column in range(4)
        )
        right_trace = sum(
            metric[row, column] * right[row, column]
            for row in range(4)
            for column in range(4)
        )
        textbook_numerator = component_pairing - left_trace * right_trace / 2

        transfer_square = dot(p3 - p1, p3 - p1)
        mandelstam_s = dot(p1 + p2, p1 + p2)
        mandelstam_u = 4 * mass**2 - mandelstam_s - transfer_square
        a = (mandelstam_s - 2 * mass**2) / 2
        b = mass**2 - mandelstam_u / 2
        compiled_numerator = a**2 + b**2 - mass**4 - transfer_square**2 / 4

        self.assertEqual(transfer_square, Rational(-1, 2))
        self.assertEqual(compiled_numerator, Rational(11, 4))
        self.assertEqual(textbook_numerator / 2, compiled_numerator)
        self.assertEqual(compiled_numerator / transfer_square, Rational(-11, 2))


if __name__ == "__main__":
    unittest.main()

import unittest

from sympy import Matrix, Rational, diag, simplify, symbols

from fieldcalc.grammar import compile_trace_reversal


class GaugeHomotopyTests(unittest.TestCase):
    def setUp(self):
        self.q_squared = symbols("Q", nonzero=True)
        self.gauge_map = Matrix([[1], [0]])
        self.gauge_condition = Matrix([[self.q_squared, 0]])
        self.identity = diag(1, 1)

    def test_de_donder_identity_generates_complementary_projectors(self):
        gauge_projector = (
            self.gauge_map * self.gauge_condition / self.q_squared
        )
        transverse_projector = self.identity - gauge_projector

        self.assertEqual(
            self.gauge_condition * self.gauge_map, Matrix([[self.q_squared]])
        )
        self.assertEqual(gauge_projector * gauge_projector, gauge_projector)
        self.assertEqual(transverse_projector * transverse_projector, transverse_projector)
        self.assertEqual(self.gauge_condition * transverse_projector, Matrix([[0, 0]]))
        self.assertEqual(transverse_projector * self.gauge_map, Matrix([[0], [0]]))

    def test_generated_green_family_inverts_the_gauge_fixed_kernel(self):
        alpha = symbols("alpha", nonzero=True)
        gauge_projector = self.gauge_map * self.gauge_condition / self.q_squared
        transverse_projector = self.identity - gauge_projector
        kinetic = self.q_squared * transverse_projector
        transverse_green = transverse_projector / self.q_squared

        gauge_fixed = kinetic + self.gauge_map * self.gauge_condition / alpha
        green = (
            transverse_green
            + alpha
            * self.gauge_map
            * self.gauge_condition
            / self.q_squared**2
        )

        self.assertEqual(gauge_fixed * green, self.identity)
        self.assertEqual(green * gauge_fixed, self.identity)

    def test_gauge_parameter_change_is_exact_and_dies_in_source_quotient(self):
        alpha, beta, external_inverse, witness, physical = symbols(
            "alpha beta E Y J", nonzero=True
        )
        gauge_projector = self.gauge_map * self.gauge_condition / self.q_squared
        transverse_projector = self.identity - gauge_projector
        transverse_green = transverse_projector / self.q_squared

        def green(parameter):
            return (
                transverse_green
                + parameter
                * self.gauge_map
                * self.gauge_condition
                / self.q_squared**2
            )

        difference = green(alpha) - green(beta)
        exact_difference = (
            (alpha - beta)
            * self.gauge_map
            * self.gauge_condition
            / self.q_squared**2
        )
        source = Matrix([external_inverse * witness, physical])
        source_variation = (source.T * difference * source)[0]

        self.assertEqual(difference.applyfunc(simplify), exact_difference)
        self.assertEqual(
            simplify(source_variation),
            (alpha - beta) * external_inverse**2 * witness**2 / self.q_squared,
        )
        self.assertEqual(source_variation.subs(external_inverse, 0), 0)

    def test_trace_reversal_generates_its_dimension_continued_inverse(self):
        dimension = symbols("d")

        trace_reversal = compile_trace_reversal(dimension)
        left = trace_reversal.coefficient
        right = trace_reversal.inverse_coefficient

        self.assertEqual(left, -Rational(1, 2))
        self.assertEqual(right, -1 / (dimension - 2))
        self.assertEqual(simplify(left + right + dimension * left * right), 0)
        self.assertEqual(
            trace_reversal.involution_residual,
            (dimension - 4) / 4,
        )
        self.assertEqual(trace_reversal.involution_residual.subs(dimension, 4), 0)

    def test_trace_reversal_refuses_the_singular_dimension(self):
        with self.assertRaisesRegex(ValueError, "singular in dimension two"):
            compile_trace_reversal(2)

    def test_common_boundary_value_algebra_preserves_the_green_inverse(self):
        alpha = symbols("alpha", nonzero=True)

        # Write L=Q I+c N and G=D1 I+b N D2 with
        # N^2=Q N, Q D1=1, and Q D2=D1.  The identity part is one;
        # this is the remaining coefficient of N D1.
        kernel_coefficient = 1 / alpha - 1
        green_coefficient = alpha - 1
        residual = (
            green_coefficient
            + kernel_coefficient
            + kernel_coefficient * green_coefficient
        )

        self.assertEqual(simplify(residual), 0)


if __name__ == "__main__":
    unittest.main()

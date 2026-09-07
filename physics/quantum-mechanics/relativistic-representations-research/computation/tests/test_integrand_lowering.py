import unittest

from sympy import Poly, factor, symbols

from fieldcalc.lowering import (
    compile_scalar_spin2_numerator,
    lower_two_point_numerator,
)


class IntegrandLoweringTests(unittest.TestCase):
    def setUp(self):
        self.p2, self.k2, self.pk, self.m2, self.d = symbols(
            "p2 k2 pk m2 d"
        )

    def test_spin_two_packet_lowers_to_two_dimreg_integral_sectors(self):
        trace_shift = self.pk - self.m2
        unreduced_pairing = (
            2 * self.p2 * self.k2
            + 2 * self.pk**2
            - 4 * trace_shift * self.pk
            + self.d * trace_shift**2
        )
        numerator = compile_scalar_spin2_numerator(
            self.p2, self.k2, self.pk, self.m2, self.d
        )

        result = lower_two_point_numerator(
            numerator,
            self.k2,
            self.pk,
            self.p2,
            self.m2,
        )

        self.assertTrue(result.accepted)
        self.assertEqual(Poly(unreduced_pairing, self.k2, self.pk).total_degree(), 2)
        self.assertEqual(Poly(numerator, self.k2, self.pk).total_degree(), 1)
        self.assertEqual(result.input_degree, 1)
        self.assertEqual(result.denominator_degree, 1)
        self.assertEqual(result.reconstruction_residual, 0)
        sectors = {sector.name: sector for sector in result.sectors}
        self.assertEqual(
            factor(sectors["bubble"].coefficient),
            factor(4 * self.p2 * self.m2 - 4 * self.m2**2 / (self.d - 2)),
        )
        self.assertEqual(sectors["massive tadpole"].coefficient, -2 * self.m2)
        self.assertEqual(
            sectors["massless tadpole"].coefficient,
            2 * (self.p2 + self.m2),
        )
        self.assertEqual(
            tuple(sector.name for sector in result.dimreg_sectors),
            ("bubble", "massive tadpole"),
        )

    def test_affine_invariant_numerator_transfers_through_same_map(self):
        a, b, c = symbols("a b c")
        numerator = a * self.k2 + b * self.pk + c

        result = lower_two_point_numerator(
            numerator,
            self.k2,
            self.pk,
            self.p2,
            self.m2,
        )

        sectors = {sector.name: sector for sector in result.sectors}
        self.assertTrue(result.accepted)
        self.assertEqual(
            factor(
                sectors["bubble"].coefficient
                - (a * self.m2 + b * (self.p2 + self.m2) / 2 + c)
            ),
            0,
        )
        self.assertEqual(sectors["massive tadpole"].coefficient, -b / 2)
        self.assertEqual(sectors["massless tadpole"].coefficient, a + b / 2)
        self.assertEqual(result.reconstruction_residual, 0)

    def test_higher_denominator_degree_is_refused_not_hidden(self):
        result = lower_two_point_numerator(
            self.pk**2,
            self.k2,
            self.pk,
            self.p2,
            self.m2,
        )

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.refusal.reason,
            "numerator exceeds affine denominator span",
        )

    def test_trace_reversal_refuses_dimension_two(self):
        with self.assertRaisesRegex(ValueError, "singular in dimension two"):
            compile_scalar_spin2_numerator(
                self.p2, self.k2, self.pk, self.m2, 2
            )


if __name__ == "__main__":
    unittest.main()

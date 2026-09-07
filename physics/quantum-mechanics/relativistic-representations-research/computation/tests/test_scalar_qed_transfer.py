import unittest

from sympy import Matrix, simplify, symbols

from fieldcalc.residual import ResidualRequest, resolve_residual


class ScalarQEDTransferTests(unittest.TestCase):
    def setUp(self):
        mass_squared, incoming_energy, photon_pairing = symbols(
            "m2 a b", nonzero=True
        )
        self.mass_squared = mass_squared
        self.gram = Matrix([
            [mass_squared, incoming_energy, incoming_energy - photon_pairing],
            [incoming_energy, 0, photon_pairing],
            [incoming_energy - photon_pairing, photon_pairing, 0],
        ])
        self.p = Matrix([1, 0, 0])
        self.k = Matrix([0, 1, 0])
        self.k_prime = Matrix([0, 0, 1])
        self.p_prime = self.p + self.k - self.k_prime

    def dot(self, left, right):
        return simplify((left.T * self.gram * right)[0])

    def test_internal_denominators_are_partial_kinetic_defects(self):
        r_s = self.p + self.k
        r_u = self.p - self.k_prime
        d_s = simplify(self.dot(r_s, r_s) - self.mass_squared)
        d_u = simplify(self.dot(r_u, r_u) - self.mass_squared)

        self.assertEqual(self.dot(self.p, self.p), self.mass_squared)
        self.assertEqual(self.dot(self.p_prime, self.p_prime), self.mass_squared)
        self.assertEqual(self.dot(self.k, self.k), 0)
        self.assertEqual(self.dot(self.k_prime, self.k_prime), 0)
        self.assertEqual(d_s, 2 * self.gram[0, 1])
        self.assertEqual(d_u, -2 * self.gram[0, 2])

    def test_action_contact_is_forced_by_both_ward_residuals(self):
        d_s = simplify(self.dot(self.p + self.k, self.p + self.k) - self.mass_squared)
        d_u = simplify(
            self.dot(self.p - self.k_prime, self.p - self.k_prime)
            - self.mass_squared
        )
        exchange_terms = (
            (-1 / d_s, 2 * self.p + self.k, 2 * self.p_prime + self.k_prime),
            (-1 / d_u, 2 * self.p_prime - self.k, 2 * self.p - self.k_prime),
        )

        incoming_residual = sum(
            (weight * self.dot(self.k, left) * right for weight, left, right in exchange_terms),
            Matrix.zeros(3, 1),
        ).applyfunc(simplify)
        outgoing_residual = sum(
            (weight * self.dot(self.k_prime, right) * left for weight, left, right in exchange_terms),
            Matrix.zeros(3, 1),
        ).applyfunc(simplify)

        self.assertEqual(incoming_residual, -2 * self.k)
        self.assertEqual(outgoing_residual, -2 * self.k_prime)

        completion = resolve_residual(ResidualRequest(
            channels=(-2, -2),
            correction_columns=((1, 1),),
            names=("metric contact",),
            provenance="scalar-QED Compton transfer",
        ))

        self.assertTrue(completion.accepted)
        self.assertEqual(completion.coefficients, (2,))
        self.assertEqual(completion.remaining, (0, 0))
        self.assertEqual(incoming_residual + 2 * self.k, Matrix.zeros(3, 1))
        self.assertEqual(outgoing_residual + 2 * self.k_prime, Matrix.zeros(3, 1))


if __name__ == "__main__":
    unittest.main()

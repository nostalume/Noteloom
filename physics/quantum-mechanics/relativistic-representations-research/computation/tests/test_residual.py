import unittest

from sympy import Matrix, Rational

from fieldcalc.exact import kernel_certificate
from fieldcalc.residual import ResidualRequest, resolve_residual


class ResidualTests(unittest.TestCase):
    def test_exact_coefficients_are_generated_from_residual(self):
        request = ResidualRequest(
            channels=(Rational(2, 3), Rational(-5, 7)),
            correction_columns=((1, 0), (0, 1)),
            names=("trace repair", "divergence repair"),
        )
        result = resolve_residual(request)
        self.assertTrue(result.accepted)
        self.assertEqual(result.coefficients, (Rational(-2, 3), Rational(5, 7)))
        self.assertEqual(result.remaining, (0, 0))

    def test_insufficient_basis_returns_residual_channels(self):
        request = ResidualRequest(
            channels=(1, 1), correction_columns=((1, 0),), names=("first",)
        )
        result = resolve_residual(request)
        self.assertFalse(result.accepted)
        self.assertEqual(result.refusal.reason, "residual outside correction span")
        self.assertNotEqual(result.refusal.residual, (0, 0))

    def test_kernel_certificate_preserves_rank_nullity(self):
        certificate = kernel_certificate(Matrix([[1, 1, 0], [0, 1, 1]]))
        self.assertEqual(certificate.rank, 2)
        self.assertEqual(certificate.nullity, 1)
        self.assertEqual(certificate.matrix * certificate.basis[0], Matrix([0, 0]))


if __name__ == "__main__":
    unittest.main()

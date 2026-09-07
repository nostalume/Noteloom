import unittest

from scipy.integrate import quad
from sympy import N, Rational, diff, limit, log, oo, simplify, symbols

from fieldcalc.spectral import (
    compile_subtracted_bubble,
    compile_threshold_window,
)


class BubbleBoundaryTests(unittest.TestCase):
    def test_subtracted_boundary_reconstructs_its_dispersion_measure(self):
        result = compile_subtracted_bubble(2, subtraction_point=0)
        self.assertTrue(result.accepted)
        boundary = result.boundary
        spectral_parameter = 1.0

        dispersive, error = quad(
            lambda energy: boundary.density(energy)
            / ((energy - spectral_parameter) * energy),
            boundary.threshold,
            oo,
            epsabs=1e-12,
            epsrel=1e-12,
        )
        dispersive *= spectral_parameter

        self.assertAlmostEqual(
            float(N(boundary.subtracted(spectral_parameter))),
            dispersive,
            places=11,
        )
        self.assertLess(error, 1e-10)

    def test_density_and_boundary_derivative_have_same_threshold(self):
        mu = symbols("mu", positive=True)
        z, energy = symbols("z energy", positive=True)
        result = compile_subtracted_bubble(mu, subtraction_point=0)
        boundary = result.boundary

        self.assertEqual(
            simplify(boundary.density(energy) - (1 - mu / energy)),
            0,
        )
        self.assertEqual(
            simplify(
                diff(boundary.primitive(z), z)
                - boundary.derivative(z)
            ),
            0,
        )
        self.assertEqual(limit(boundary.primitive(z), z, 0), 0)
        self.assertEqual(limit(boundary.derivative(z), z, mu, dir="-"), oo)

    def test_scalar_spin_two_density_exposes_the_threshold_collision(self):
        mu = symbols("mu", positive=True)
        energy = symbols("energy", positive=True)
        boundary = compile_subtracted_bubble(mu, subtraction_point=0).boundary

        packet_density = boundary.scalar_spin2_density(energy, dimension=4)
        diagnostic = boundary.diagnose_shell(mu, dimension=4)

        self.assertEqual(limit(packet_density, energy, mu, dir="+"), 0)
        self.assertEqual(
            limit(packet_density / (energy - mu), energy, mu, dir="+"),
            2 * mu,
        )
        self.assertEqual(diagnostic.status, "threshold collision")
        self.assertEqual(diagnostic.nonlocal_coefficient, 2 * mu**2)
        self.assertFalse(diagnostic.isolated_pole_admissible)

    def test_below_threshold_probe_is_analytic_but_not_a_generated_pole(self):
        boundary = compile_subtracted_bubble(2, subtraction_point=0).boundary

        diagnostic = boundary.diagnose_shell(1, dimension=4)

        self.assertEqual(diagnostic.status, "below continuum")
        self.assertTrue(diagnostic.isolated_pole_admissible)
        self.assertIn("does not solve the pole equation", diagnostic.reason)

    def test_subtraction_on_or_above_the_cut_is_refused(self):
        result = compile_subtracted_bubble(2, subtraction_point=2)

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.refusal.reason,
            "subtraction point must lie below the bubble threshold",
        )

    def test_detector_window_is_the_compiled_spectral_cell(self):
        mu, delta, scale = symbols("mu delta scale", positive=True)
        boundary = compile_subtracted_bubble(mu).boundary

        result = compile_threshold_window(
            boundary,
            resolution=delta,
            reference_resolution=2 * delta,
            normalization=scale,
        )

        self.assertTrue(result.accepted)
        window = result.window
        expected = 2 * scale * mu * (
            delta**2
            - mu * delta
            + mu**2 * log(1 + delta / mu)
        )
        self.assertEqual(window.interval, (mu, mu + delta))
        self.assertEqual(simplify(window.response - expected), 0)
        self.assertEqual(
            simplify(
                diff(window.response, delta)
                - scale * boundary.scalar_spin2_density(mu + delta)
            ),
            0,
        )
        self.assertEqual(limit(window.response / delta**2, delta, 0), scale * mu)

    def test_nested_windows_generate_a_normalization_free_fraction(self):
        boundary = compile_subtracted_bubble(2).boundary
        result = compile_threshold_window(
            boundary,
            resolution=1,
            reference_resolution=3,
            normalization=7,
        )

        window = result.window
        fraction = float(N(window.conditional_fraction))
        self.assertGreater(fraction, 0)
        self.assertLess(fraction, 1)
        self.assertEqual(
            simplify(
                window.conditional_fraction
                - window.unnormalized_response
                / window.unnormalized_reference_response
            ),
            0,
        )

    def test_three_dimensions_transfer_to_a_cubic_threshold_cell(self):
        delta = symbols("delta", positive=True)
        boundary = compile_subtracted_bubble(2).boundary
        result = compile_threshold_window(
            boundary,
            resolution=delta,
            reference_resolution=2 * delta,
            dimension=3,
        )

        self.assertEqual(
            limit(result.window.response / delta**3, delta, 0),
            Rational(4, 3),
        )

    def test_nonphysical_window_requests_are_refused(self):
        boundary = compile_subtracted_bubble(2).boundary

        cases = (
            (0, 1, 1, 4, "resolution must be positive"),
            (2, 1, 1, 4, "reference resolution must contain the detector window"),
            (1, 2, -1, 4, "spectral normalization must be positive"),
            (1, 2, 1, 2, "positive spin-two window requires dimension at least three"),
        )
        for resolution, reference, scale, dimension, reason in cases:
            with self.subTest(reason=reason):
                result = compile_threshold_window(
                    boundary,
                    resolution=resolution,
                    reference_resolution=reference,
                    normalization=scale,
                    dimension=dimension,
                )
                self.assertFalse(result.accepted)
                self.assertEqual(result.refusal.reason, reason)


if __name__ == "__main__":
    unittest.main()

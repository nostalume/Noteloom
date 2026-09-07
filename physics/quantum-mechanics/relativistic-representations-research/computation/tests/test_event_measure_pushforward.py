import math
import unittest

from sympy import Rational, pi, simplify, sqrt, symbols

from fieldcalc.amplitude import (
    compile_characteristic_scalar_amplitude,
    compile_scalar_compton_kinematics,
)
from fieldcalc.measures import (
    PreparedEventEffect,
    PreparedEventMeasureRequest,
    compile_prepared_event_effect,
    compile_prepared_event_measure,
)
from fieldcalc.rewrite import Refusal


class PreparedEventMeasureTests(unittest.TestCase):
    @staticmethod
    def compton_effect():
        t = symbols("t", real=True)
        kinematics = compile_scalar_compton_kinematics(1, 1, t)
        amplitude = compile_characteristic_scalar_amplitude(
            kinematics.metric,
            kinematics.initial_momentum,
            kinematics.photon_momenta,
            kinematics.polarizations,
            kinematics.mass_squared,
            state_budget=4,
        )
        effect = compile_prepared_event_effect(amplitude, Rational(1))
        return t, kinematics, amplitude, effect

    def test_compton_effect_pushes_to_positive_normalized_aperture_measure(self):
        t, kinematics, amplitude, effect = self.compton_effect()
        self.assertTrue(kinematics.accepted)
        self.assertEqual(kinematics.shell_residual, 0)
        self.assertEqual(kinematics.phase_space_residual, 0)
        self.assertEqual(kinematics.polarization_norm_residuals, (0, 0))
        self.assertTrue(amplitude.accepted)
        self.assertTrue(effect.accepted)
        self.assertEqual(simplify(amplitude.value + 2 * (t**2 - 1) / (t**2 + 1)), 0)

        phase_density = kinematics.phase_space_density
        result = compile_prepared_event_measure(PreparedEventMeasureRequest(
            effect=effect,
            parameter=t,
            phase_space_density=phase_density,
            support=(0.0, math.inf),
            provenance="unit scalar Compton reflection quotient",
        ))
        self.assertTrue(result.accepted)
        measure = result.measure
        expected_density = (
            2 * (1 - t**2) ** 2
            / (pi * (1 + t**2) ** 2 * (1 + 3 * t**2))
        )
        self.assertEqual(simplify(measure.density - expected_density), 0)

        total = measure.total_mass()
        aperture = measure.aperture((0.0, 1.0))
        fraction = measure.fraction((0.0, 1.0))
        expected_total = -2 + 4 * sqrt(3) / 3
        expected_aperture = -1 - 1 / pi + 8 * sqrt(3) / 9
        expected_fraction = (
            Rational(7, 6) + sqrt(3) / 3
            - (sqrt(3) + Rational(3, 2)) / pi
        )
        self.assertAlmostEqual(total.value, float(expected_total), places=11)
        self.assertAlmostEqual(aperture.value, float(expected_aperture), places=11)
        self.assertAlmostEqual(fraction.value, float(expected_fraction), places=11)
        self.assertLess(max(total.error, aperture.error, fraction.error), 1e-10)
        self.assertEqual(total.measure_id, aperture.measure_id)
        self.assertEqual(aperture.measure_id, fraction.measure_id)
        self.assertGreater(total.evaluations, 0)

    def test_measure_compiler_refuses_unphysical_or_unbound_input(self):
        t, _, _, effect = self.compton_effect()
        unavailable = PreparedEventEffect(refusal=Refusal("unavailable"))
        cases = (
            (unavailable, 1, "prepared event effect is unavailable"),
            (effect, -1, "phase-space density must be provably nonnegative"),
            (effect, symbols("u", real=True) ** 2, "phase-space density has unbound symbols"),
        )
        for candidate, density, reason in cases:
            with self.subTest(reason=reason):
                result = compile_prepared_event_measure(PreparedEventMeasureRequest(
                    effect=candidate,
                    parameter=t,
                    phase_space_density=density,
                    support=(0.0, 1.0),
                    provenance="refusal witness",
                ))
                self.assertFalse(result.accepted)
                self.assertEqual(result.refusal.reason, reason)

        invalid_support = compile_prepared_event_measure(PreparedEventMeasureRequest(
            effect=effect,
            parameter=t,
            phase_space_density=1,
            support=(1.0, 0.0),
            provenance="invalid support witness",
        ))
        self.assertFalse(invalid_support.accepted)
        self.assertEqual(invalid_support.refusal.reason, "invalid event-measure support")

        nonreal_parameter = compile_prepared_event_measure(PreparedEventMeasureRequest(
            effect=effect,
            parameter=symbols("z"),
            phase_space_density=1,
            support=(0.0, 1.0),
            provenance="untyped parameter witness",
        ))
        self.assertFalse(nonreal_parameter.accepted)
        self.assertEqual(
            nonreal_parameter.refusal.reason,
            "event parameter must be one real symbol",
        )

        invalid_scale = compile_scalar_compton_kinematics(0, 1, t)
        self.assertFalse(invalid_scale.accepted)
        self.assertEqual(
            invalid_scale.refusal.reason,
            "mass and incoming energy must be provably positive",
        )


if __name__ == "__main__":
    unittest.main()

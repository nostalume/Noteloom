import math
import unittest

from sympy import Rational, pi, simplify, sqrt, symbols

from fieldcalc.amplitude import compile_scalar_compton_kinematics
from fieldcalc.fermion import compile_fermion_compton_effect
from fieldcalc.measures import (
    PreparedEventMeasureRequest,
    compile_prepared_event_measure,
)


class FermionComptonTransferTests(unittest.TestCase):
    def setUp(self):
        self.parameter = symbols("t", real=True)
        self.kinematics = compile_scalar_compton_kinematics(
            1, 1, self.parameter
        )

    def test_exterior_quotient_reaches_the_same_aperture_more_directly(self):
        result = compile_fermion_compton_effect(self.kinematics)
        baseline = compile_fermion_compton_effect(
            self.kinematics, trace_backend="shared recurrence"
        )
        self.assertTrue(result.accepted)
        self.assertTrue(baseline.accepted)
        self.assertEqual(result.ward_residuals, (0, 0))
        self.assertEqual(result.projector_residuals, (0, 0))

        t = self.parameter
        expected_effect = (
            (2 * t**3 - t) ** 2 + 1
        ) / ((1 + t**2) ** 2 * (1 + 3 * t**2))
        self.assertEqual(simplify(result.trace_value - expected_effect), 0)
        self.assertEqual(result.trace_value, baseline.trace_value)
        self.assertEqual(simplify(result.effect.value - expected_effect), 0)
        self.assertIs(result.effect.value.is_nonnegative, True)
        self.assertEqual(baseline.recurrence_updates, 462)
        self.assertEqual(baseline.trace_backend, "shared recurrence")
        self.assertEqual(result.trace_backend, "exterior grade")
        self.assertEqual(result.normal_form_terms, 6)
        self.assertEqual(result.contraction_updates, 119)
        self.assertEqual(
            result.total_updates,
            result.contraction_updates + result.ward_updates,
        )
        self.assertEqual(result.total_updates, 293)
        self.assertEqual(baseline.total_updates, 1386)
        self.assertLess(
            result.total_updates, baseline.total_updates
        )
        self.assertEqual(result.normal_form_residual, 0)

        compiled = compile_prepared_event_measure(PreparedEventMeasureRequest(
            effect=result.effect,
            parameter=t,
            phase_space_density=self.kinematics.phase_space_density,
            support=(0.0, math.inf),
            provenance="unit fermion Compton parity-double",
        ))
        self.assertTrue(compiled.accepted)
        total = compiled.measure.total_mass()
        aperture = compiled.measure.aperture((0.0, 1.0))
        fraction = compiled.measure.fraction((0.0, 1.0))
        expected_total = -Rational(7, 16) + 11 * sqrt(3) / 36
        expected_aperture = (-207 + pi * (-189 + 176 * sqrt(3))) / (864 * pi)
        expected_fraction = expected_aperture / expected_total
        self.assertAlmostEqual(total.value, float(expected_total), places=11)
        self.assertAlmostEqual(aperture.value, float(expected_aperture), places=11)
        self.assertAlmostEqual(fraction.value, float(expected_fraction), places=11)
        self.assertLess(max(total.error, aperture.error, fraction.error), 1e-10)

    def test_unresolved_odd_trace_sector_is_refused(self):
        result = compile_fermion_compton_effect(
            self.kinematics, parity_doubled=False
        )
        self.assertFalse(result.accepted)
        self.assertEqual(
            result.refusal.reason,
            "single-parity odd Clifford trace is not generated",
        )


if __name__ == "__main__":
    unittest.main()

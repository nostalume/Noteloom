import unittest

from sympy import Rational, cos, simplify, sin, sqrt, symbols, tan

from occ.impact import (
    FrictionalImpactRequest,
    construct_frictional_impact,
)
from worktable.impact_cases import run_a15_impact


class FrictionalImpactTests(unittest.TestCase):
    def test_projection_constructs_sticking_and_sliding_branches(self):
        mass, normal, tangent, friction, restitution = symbols(
            "m u_n u_t mu e", positive=True, real=True
        )
        result = construct_frictional_impact(
            FrictionalImpactRequest(
                "generic-impact", mass, normal, tangent, friction, restitution
            )
        )
        threshold = friction * (1 + restitution) * normal

        self.assertEqual(result.status, "constructed")
        self.assertEqual(result.normal_impulse, mass * (1 + restitution) * normal)
        self.assertEqual(result.sticking.condition, tangent <= threshold)
        self.assertEqual(result.sticking.tangential_impulse, -mass * tangent)
        self.assertEqual(result.sticking.outgoing_tangential_speed, 0)
        self.assertEqual(result.sliding.condition, tangent > threshold)
        self.assertEqual(
            result.sliding.tangential_impulse,
            -mass * threshold,
        )
        self.assertEqual(
            simplify(result.sliding.outgoing_tangential_speed - (tangent - threshold)),
            0,
        )
        self.assertIsNone(result.selected_regime)
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_exact_numeric_inputs_select_regime_without_changing_the_law(self):
        sticking = construct_frictional_impact(
            FrictionalImpactRequest("stick", 2, 3, 1, Rational(1, 2), Rational(1, 2))
        )
        sliding = construct_frictional_impact(
            FrictionalImpactRequest("slide", 2, 3, 4, Rational(1, 2), Rational(1, 2))
        )

        self.assertEqual(sticking.selected_regime, "sticking")
        self.assertEqual(sticking.outgoing_tangential_speed, 0)
        self.assertEqual(sticking.outgoing_speed, Rational(3, 2))
        self.assertEqual(sliding.selected_regime, "sliding")
        self.assertEqual(sliding.outgoing_tangential_speed, Rational(7, 4))
        self.assertEqual(sliding.outgoing_speed, sqrt(85) / 4)
        self.assertEqual(sliding.reflection_tangent, Rational(7, 6))

    def test_frictionless_limit_preserves_tangential_speed(self):
        result = construct_frictional_impact(
            FrictionalImpactRequest("smooth", 2, 3, 4, 0, Rational(1, 2))
        )

        self.assertEqual(result.selected_regime, "sliding")
        self.assertEqual(result.sliding.tangential_impulse, 0)
        self.assertEqual(result.outgoing_tangential_speed, 4)

    def test_a15_wall_impact_returns_speed_and_angle_in_both_regimes(self):
        case = run_a15_impact()
        speed = case.incident_speed
        angle = case.incidence_angle
        friction = case.friction_coefficient
        restitution = case.restitution_coefficient
        slip_tangent = tan(angle) - friction * (1 + restitution)

        self.assertEqual(
            case.sticking_condition,
            tan(angle) <= friction * (1 + restitution),
        )
        self.assertEqual(case.sticking_speed, restitution * speed * cos(angle))
        self.assertEqual(case.sticking_angle, 0)
        self.assertEqual(
            simplify(tan(case.sliding_angle) - slip_tangent / restitution),
            0,
        )
        expected_sliding_squared = speed**2 * (
            restitution**2 * cos(angle) ** 2
            + (sin(angle) - friction * (1 + restitution) * cos(angle)) ** 2
        )
        self.assertEqual(
            simplify(case.sliding_speed**2 - expected_sliding_squared),
            0,
        )
        self.assertEqual(case.admission.classification, "always_direct")

    def test_nonphysical_parameters_are_rejected_at_admission(self):
        valid = ("invalid", 1, 1, 1, Rational(1, 2), Rational(1, 2))
        replacements = {
            1: 0,
            2: 0,
            3: -1,
            4: -1,
            5: 0,
        }
        for index, invalid in replacements.items():
            with self.subTest(index=index):
                arguments = list(valid)
                arguments[index] = invalid
                with self.assertRaises(ValueError):
                    FrictionalImpactRequest(*arguments)


if __name__ == "__main__":
    unittest.main()

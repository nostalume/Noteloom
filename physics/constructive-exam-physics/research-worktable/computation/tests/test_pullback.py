from fractions import Fraction
import unittest

from occ.pullback import (
    pullback_linear,
    pullback_quadratic,
)


Q = Fraction


class ObservablePullbackTests(unittest.TestCase):
    def test_a617_2025_dielectric_structure_pulls_voltage_to_flux_coefficient(self):
        field_from_displacement = ((Q(1),), (Q(2),), (Q(3),))
        voltage_functional = (Q(1), Q(1), Q(1))

        result = pullback_linear(
            (field_from_displacement,),
            voltage_functional,
        )

        self.assertEqual(result.source_covector, (Q(6),))
        self.assertEqual(result.dimensions, (1, 3))
        self.assertEqual(result.evaluate_source((Q(5),)), Q(30))
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_linear_pullback_respects_reverse_composition(self):
        first = ((Q(1),), (Q(2),))
        second = (
            (Q(1), Q(0)),
            (Q(0), Q(1)),
            (Q(1), Q(1)),
        )
        final_observable = (Q(2), Q(-1), Q(3))

        result = pullback_linear((first, second), final_observable)

        self.assertEqual(result.source_covector, (Q(9),))
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_a617_2024_solenoid_structure_pulls_heating_to_current_rate(self):
        field_from_current_rate = ((Q(1),), (Q(2),))
        joule_form = ((Q(1), Q(0)), (Q(0), Q(3)))

        result = pullback_quadratic(
            (field_from_current_rate,),
            joule_form,
        )

        self.assertEqual(result.source_form, ((Q(13),),))
        self.assertEqual(result.evaluate_source((Q(3),)), Q(117))
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_a617_2023_rotating_coil_structure_pulls_joule_power_to_emf(self):
        impedance_inverse = (
            (Q(3, 25), Q(4, 25)),
            (Q(-4, 25), Q(3, 25)),
        )
        average_joule_form = (
            (Q(3, 2), Q(0)),
            (Q(0), Q(3, 2)),
        )

        result = pullback_quadratic(
            (impedance_inverse,),
            average_joule_form,
        )

        self.assertEqual(
            result.source_form,
            ((Q(3, 50), Q(0)), (Q(0), Q(3, 50))),
        )

    def test_incompatible_map_chain_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "chain dimensions"):
            pullback_linear(
                (
                    ((Q(1),), (Q(2),)),
                    ((Q(1), Q(0), Q(0)),),
                ),
                (Q(1),),
            )


if __name__ == "__main__":
    unittest.main()

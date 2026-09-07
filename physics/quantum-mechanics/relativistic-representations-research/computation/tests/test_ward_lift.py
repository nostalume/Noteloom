import unittest

from sympy import Rational, integrate, log, simplify, symbols

from fieldcalc.residual import (
    ObservableDescentRequest,
    WardLiftRequest,
    descend_observable,
    lift_ward_packet,
)
from fieldcalc.spectral import compile_subtracted_bubble, compile_threshold_window


class WardLiftTests(unittest.TestCase):
    def setUp(self):
        delta, left_witness, right_witness = symbols("Delta Y_L Y_R")
        self.external = (-delta * left_witness, -delta * right_witness)

    def request(self, **changes):
        data = {
            "internal_channels": ("left collapse", "right collapse"),
            "external_generators": ("E(p_L)", "E(p_R)"),
            "primary_internal": (1, 1),
            "primary_external": self.external,
            "correction_internal": ((2, 2),),
            "correction_external": ((0, 0),),
            "correction_names": ("order-two action jet",),
            "budget": 1,
            "provenance": "scalar two-point Ward lift",
        }
        data.update(changes)
        return WardLiftRequest(**data)

    def test_action_jet_is_generated_as_the_unique_packet_repair(self):
        result = lift_ward_packet(self.request())

        self.assertTrue(result.accepted)
        self.assertEqual(result.weights, (1, Rational(-1, 2)))
        self.assertEqual(result.remaining_internal, (0, 0))
        self.assertEqual(result.external_coefficients, self.external)
        self.assertEqual(result.external_generators, ("E(p_L)", "E(p_R)"))

    def test_missing_contact_jet_returns_the_internal_obstruction(self):
        result = lift_ward_packet(
            self.request(
                correction_internal=(),
                correction_external=(),
                correction_names=(),
            )
        )

        self.assertFalse(result.accepted)
        self.assertEqual(result.remaining_internal, (1, 1))
        self.assertEqual(result.refusal.reason, "no correction operations")

    def test_incompatible_action_jet_is_not_forced_into_closure(self):
        result = lift_ward_packet(
            self.request(correction_internal=((1, -1),))
        )

        self.assertFalse(result.accepted)
        self.assertEqual(result.refusal.reason, "residual outside correction span")

    def test_repair_budget_is_an_explicit_boundary(self):
        result = lift_ward_packet(self.request(budget=0))

        self.assertFalse(result.accepted)
        self.assertEqual(result.refusal.reason, "Ward repair budget exceeded")

    def test_independent_repairs_transfer_through_the_same_interface(self):
        left_mark, right_mark = symbols("a b")
        result = lift_ward_packet(
            self.request(
                primary_internal=(3, 5),
                primary_external=(0, 0),
                correction_internal=((1, 0), (0, 1)),
                correction_external=((left_mark, 0), (0, right_mark)),
                correction_names=("left repair", "right repair"),
                budget=2,
            )
        )

        self.assertTrue(result.accepted)
        self.assertEqual(result.weights, (1, -3, -5))
        self.assertEqual(result.remaining_internal, (0, 0))
        self.assertEqual(
            result.external_coefficients,
            (-3 * left_mark, -5 * right_mark),
        )


class ObservableDescentTests(unittest.TestCase):
    def request(self, **changes):
        data = {
            "external_generators": ("E(p)",),
            "primary_on_ideal": (0,),
            "correction_on_ideal": (),
            "correction_names": (),
            "budget": 0,
            "provenance": "scalar cut-to-effect admission",
        }
        data.update(changes)
        return ObservableDescentRequest(**data)

    def test_shell_evaluation_descends_directly_to_the_external_quotient(self):
        x = symbols("x")
        result = descend_observable(
            self.request(primary_on_ideal=(x.subs(x, 0),))
        )

        self.assertTrue(result.accepted)
        self.assertEqual(result.kind, "direct quotient")
        self.assertEqual(result.weights, (1,))
        self.assertEqual(result.remaining, (0,))

    def test_finite_window_exposes_a_nonzero_external_ideal_witness(self):
        x, delta = symbols("x delta", positive=True)
        window_on_generator = integrate(x, (x, 0, delta))

        result = descend_observable(
            self.request(primary_on_ideal=(window_on_generator,))
        )

        self.assertFalse(result.accepted)
        self.assertEqual(result.remaining, (delta**2 / 2,))
        self.assertEqual(
            result.refusal.reason,
            "observable does not annihilate external ideal",
        )

    def test_compiled_threshold_window_is_refused_by_the_bare_packet_quotient(self):
        boundary = compile_subtracted_bubble(2).boundary
        window = compile_threshold_window(boundary, 1, 3).window

        result = descend_observable(
            self.request(primary_on_ideal=(window.external_ideal_witness,))
        )
        coarse = compile_threshold_window(boundary, 3, 3).window

        self.assertFalse(result.accepted)
        expected = Rational(44, 3) - 32 * log(Rational(3, 2))
        self.assertEqual(simplify(result.remaining[0] - expected), 0)
        self.assertNotEqual(
            window.external_ideal_witness * coarse.response,
            window.response * coarse.external_ideal_witness,
        )

    def test_available_external_operations_generate_a_compensated_effect(self):
        left, right = symbols("left right")
        result = descend_observable(
            self.request(
                external_generators=("E(p_L)", "E(p_R)"),
                primary_on_ideal=(left, right),
                correction_on_ideal=((-1, 0), (0, -1)),
                correction_names=("left external dressing", "right external dressing"),
                budget=2,
            )
        )

        self.assertTrue(result.accepted)
        self.assertEqual(result.kind, "compensated quotient")
        self.assertEqual(result.weights, (1, left, right))
        self.assertEqual(result.remaining, (0, 0))

    def test_effect_repair_respects_its_resource_budget(self):
        result = descend_observable(
            self.request(
                primary_on_ideal=(1,),
                correction_on_ideal=((-1,),),
                correction_names=("external dressing",),
                budget=0,
            )
        )

        self.assertFalse(result.accepted)
        self.assertEqual(result.refusal.reason, "observable repair budget exceeded")


if __name__ == "__main__":
    unittest.main()

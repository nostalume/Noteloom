import unittest

from sympy import ImmutableMatrix, Rational, diag

from fieldcalc.amplitude import (
    compile_characteristic_scalar_amplitude,
)
from fieldcalc.measures import compile_prepared_event_effect


class PreparedEventEffectTests(unittest.TestCase):
    def setUp(self):
        self.metric = ImmutableMatrix(diag(-1, 1, 1))
        self.initial = ImmutableMatrix([1, 0, 0])
        self.k = ImmutableMatrix([1, 1, 0])
        self.epsilon = ImmutableMatrix([0, 0, 1])

    def dot(self, left, right):
        return (left.T * self.metric * right)[0]

    def histories(self, labels):
        if not labels:
            return ((),)
        generated = []
        for index, label in enumerate(labels):
            remainder = labels[:index] + labels[index + 1:]
            generated.extend(
                ((label,),) + history for history in self.histories(remainder)
            )
        for left_index, left in enumerate(labels):
            for right_index in range(left_index + 1, len(labels)):
                right = labels[right_index]
                remainder = tuple(
                    label for index, label in enumerate(labels)
                    if index not in {left_index, right_index}
                )
                generated.extend(
                    ((left, right),) + history
                    for history in self.histories(remainder)
                )
        return tuple(generated)

    def amputated_history(self, history, initial, momenta, polarizations, mass):
        momentum = initial
        value = 1
        for position, event in enumerate(history):
            before = momentum
            for label in event:
                momentum += momenta[label]
            if len(event) == 1:
                label = event[0]
                value *= self.dot(before + momentum, polarizations[label])
            else:
                left, right = event
                value *= -2 * self.dot(polarizations[left], polarizations[right])
            if position + 1 < len(history):
                value /= mass + self.dot(momentum, momentum)
        return value

    def amplitude(self, *, initial=None, momenta=None, polarizations=None):
        return compile_characteristic_scalar_amplitude(
            self.metric,
            self.initial if initial is None else initial,
            (self.k, -self.k) if momenta is None else momenta,
            (self.epsilon, self.epsilon)
            if polarizations is None else polarizations,
            1,
            state_budget=4,
        )

    def test_forward_compton_channel_generates_a_positive_event_effect(self):
        amplitude = self.amplitude()
        effect = compile_prepared_event_effect(amplitude, Rational(3, 5))
        shifted_amplitude = self.amplitude(polarizations=(
            self.epsilon + 2 * self.k,
            self.epsilon + 3 * self.k,
        ))
        shifted_effect = compile_prepared_event_effect(
            shifted_amplitude, Rational(3, 5)
        )
        baseline = sum(
            self.amputated_history(
                history, self.initial, (self.k, -self.k),
                (self.epsilon, self.epsilon), 1,
            )
            for history in self.histories((0, 1))
        )

        self.assertTrue(amplitude.accepted)
        self.assertEqual(amplitude.value, baseline)
        self.assertEqual(amplitude.value, -2)
        self.assertTrue(effect.accepted, effect.refusal)
        self.assertEqual(effect.value, Rational(12, 5))
        self.assertEqual(shifted_effect.value, effect.value)
        self.assertEqual(effect.gauge_residuals, (0, 0))
        self.assertEqual(effect.cost.baseline_operations, 7)
        self.assertEqual(effect.cost.compiled_operations, 21)
        self.assertFalse(effect.cost.advantage)

    def test_event_effect_refuses_unphysical_or_unproved_inputs(self):
        off_shell = self.amplitude(initial=ImmutableMatrix([2, 0, 0]))
        massive_photons = self.amplitude(
            momenta=(ImmutableMatrix([1, 0, 0]), ImmutableMatrix([-1, 0, 0]))
        )
        nontransverse = self.amplitude(
            polarizations=(ImmutableMatrix([1, 0, 0]), self.epsilon)
        )

        self.assertEqual(
            compile_prepared_event_effect(off_shell, 1).refusal.reason,
            "scalar endpoints are not characteristic",
        )
        self.assertEqual(
            compile_prepared_event_effect(massive_photons, 1).refusal.reason,
            "photon momenta are not characteristic",
        )
        self.assertEqual(
            compile_prepared_event_effect(nontransverse, 1).refusal.reason,
            "prepared polarizations are not transverse",
        )
        self.assertEqual(
            compile_prepared_event_effect(self.amplitude(), -1).refusal.reason,
            "detector weight must be provably nonnegative",
        )

    def test_five_photon_shell_fixture_retains_complete_route_advantage(self):
        momenta = tuple(ImmutableMatrix(item) for item in (
            (-5, -3, -4),
            (-5, 3, -4),
            (1, 1, 0),
            (4, Rational(-12, 5), Rational(16, 5)),
            (5, Rational(7, 5), Rational(24, 5)),
        ))
        polarizations = tuple(
            ImmutableMatrix([0, -momentum[2], momentum[1]])
            for momentum in momenta
        )
        amplitude = compile_characteristic_scalar_amplitude(
            self.metric, self.initial, momenta, polarizations, 1, state_budget=32,
        )
        effect = compile_prepared_event_effect(amplitude, 1)
        baseline = sum(
            self.amputated_history(
                history, self.initial, momenta, polarizations, 1,
            )
            for history in self.histories(tuple(range(5)))
        )

        self.assertTrue(effect.accepted, effect.refusal)
        self.assertEqual(amplitude.value, baseline)
        self.assertEqual(effect.value, Rational(829688677836489, 56668278601))
        self.assertEqual(effect.cost.baseline_operations, 1832)
        self.assertEqual(effect.cost.compiled_operations, 1522)
        self.assertTrue(effect.cost.advantage)


if __name__ == "__main__":
    unittest.main()

import unittest

from sympy import ImmutableMatrix, Matrix, Rational, simplify

from fieldcalc.amplitude import (
    compile_characteristic_amplitude_cost,
    compile_characteristic_scalar_amplitude,
)


class CharacteristicScalarAmplitudeTests(unittest.TestCase):
    def setUp(self):
        dimension = 9
        self.metric = ImmutableMatrix(dimension, dimension, lambda i, j: (
            20 if i == j else Rational(1, 2 + i + j)
        ))
        basis = tuple(
            ImmutableMatrix.eye(dimension)[:, index] for index in range(dimension)
        )
        self.initial = basis[0]
        self.momenta = basis[1:5]
        self.polarizations = basis[5:9]
        self.mass_squared = Rational(3)

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

    def history_value(self, history):
        momentum = self.initial
        initial_kernel = self.mass_squared + self.dot(momentum, momentum)
        value = 1 / initial_kernel
        for event in history:
            before = momentum
            momentum = before + sum(
                (self.momenta[index] for index in event),
                Matrix.zeros(before.rows, 1),
            )
            if len(event) == 1:
                index = event[0]
                vertex = self.dot(before + momentum, self.polarizations[index])
            else:
                left, right = event
                vertex = -2 * self.dot(
                    self.polarizations[left], self.polarizations[right]
                )
            value *= vertex / (
                self.mass_squared + self.dot(momentum, momentum)
            )
        return value

    def test_amputated_subset_result_recovers_histories_and_descends(self):
        histories = self.histories(tuple(range(4)))
        baseline = sum(self.history_value(history) for history in histories)
        final = self.initial + sum(
            self.momenta, Matrix.zeros(self.initial.rows, 1)
        )
        endpoints = (
            self.mass_squared + self.dot(self.initial, self.initial),
            self.mass_squared + self.dot(final, final),
        )

        result = compile_characteristic_scalar_amplitude(
            self.metric, self.initial, self.momenta, self.polarizations,
            self.mass_squared, state_budget=16,
        )

        self.assertTrue(result.accepted)
        self.assertEqual(simplify(result.value - endpoints[0] * endpoints[1] * baseline), 0)
        self.assertEqual(result.endpoint_generators, endpoints)
        self.assertEqual(len(result.ward_certificates), 4)
        self.assertTrue(all(item.residual == 0 for item in result.ward_certificates))
        self.assertEqual(result.cost.amplitude_transition_terms, 56)
        self.assertEqual(result.cost.ward_transition_terms, 368)
        self.assertEqual(result.cost.complete_transition_terms, 424)
        self.assertFalse(result.cost.complete_advantage)

        five_photon = compile_characteristic_amplitude_cost(5)
        self.assertEqual(five_photon.history_event_terms, 1830)
        self.assertEqual(five_photon.complete_transition_terms, 1520)
        self.assertTrue(five_photon.complete_advantage)

    def test_characteristic_endpoints_are_quotiented_not_inverted(self):
        result = compile_characteristic_scalar_amplitude(
            ImmutableMatrix([[1]]), ImmutableMatrix([1]),
            (ImmutableMatrix([1]), ImmutableMatrix([-3])),
            (ImmutableMatrix([2]), ImmutableMatrix([3])), -1, state_budget=4,
        )

        self.assertTrue(result.accepted)
        self.assertEqual(result.endpoint_generators, (0, 0))
        self.assertTrue(all(item.contraction == 0 for item in result.ward_certificates))
        self.assertTrue(all(item.residual == 0 for item in result.ward_certificates))

    def test_internal_characteristic_and_resource_bound_are_refused(self):
        internal = compile_characteristic_scalar_amplitude(
            ImmutableMatrix([[1]]), ImmutableMatrix([0]),
            (ImmutableMatrix([1]), ImmutableMatrix([1])),
            (ImmutableMatrix([2]), ImmutableMatrix([3])), -1, state_budget=4,
        )
        budget = compile_characteristic_scalar_amplitude(
            self.metric, self.initial, self.momenta, self.polarizations,
            self.mass_squared, state_budget=15,
        )

        self.assertEqual(
            internal.refusal.reason,
            "amputated scalar line crosses an internal characteristic",
        )
        self.assertEqual(
            budget.refusal.reason,
            "characteristic-amplitude state budget exceeded",
        )


if __name__ == "__main__":
    unittest.main()

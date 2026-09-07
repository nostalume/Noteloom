import unittest

from sympy import ImmutableMatrix, Matrix, Rational, simplify

from fieldcalc.worldline import evaluate_scalar_line_amplitude


class ScalarLineAmplitudeTests(unittest.TestCase):
    def setUp(self):
        dimension = 9
        self.gram = ImmutableMatrix(dimension, dimension, lambda i, j: (
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
        return (left.T * self.gram * right)[0]

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
        value = 1 / (self.mass_squared + self.dot(momentum, momentum))
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

    def test_four_photon_subset_evaluator_recovers_all_histories(self):
        histories = self.histories(tuple(range(4)))
        baseline = sum(self.history_value(history) for history in histories)

        evaluation = evaluate_scalar_line_amplitude(
            self.gram,
            self.initial,
            self.momenta,
            self.polarizations,
            self.mass_squared,
            state_budget=16,
        )

        self.assertEqual(len(histories), 66)
        self.assertTrue(evaluation.accepted)
        self.assertEqual(simplify(evaluation.value - baseline), 0)
        self.assertEqual(evaluation.states_visited, 16)
        self.assertEqual(evaluation.ordered_histories, 66)
        self.assertEqual(evaluation.transition_terms, 56)
        self.assertEqual(evaluation.history_event_terms, 216)

    def test_scalar_line_evaluator_refuses_budget_and_characteristic(self):
        budget_refusal = evaluate_scalar_line_amplitude(
            self.gram,
            self.initial,
            self.momenta,
            self.polarizations,
            self.mass_squared,
            state_budget=15,
        )
        self.assertFalse(budget_refusal.accepted)
        self.assertEqual(
            budget_refusal.refusal.reason,
            "scalar-line state budget exceeded",
        )

        characteristic_refusal = evaluate_scalar_line_amplitude(
            ImmutableMatrix([[1]]),
            ImmutableMatrix([1]),
            (),
            (),
            -1,
            state_budget=1,
        )
        self.assertFalse(characteristic_refusal.accepted)
        self.assertEqual(
            characteristic_refusal.refusal.reason,
            "scalar line crosses characteristic denominator",
        )

    def test_ward_contraction_is_the_difference_of_endpoint_lines(self):
        ward = evaluate_scalar_line_amplitude(
            self.gram,
            self.initial,
            self.momenta[:2],
            (self.momenta[0], self.polarizations[1]),
            self.mass_squared,
            state_budget=4,
        )
        initial_endpoint = evaluate_scalar_line_amplitude(
            self.gram,
            self.initial,
            (self.momenta[1],),
            (self.polarizations[1],),
            self.mass_squared,
            state_budget=2,
        )
        final_endpoint = evaluate_scalar_line_amplitude(
            self.gram,
            self.initial + self.momenta[0],
            (self.momenta[1],),
            (self.polarizations[1],),
            self.mass_squared,
            state_budget=2,
        )

        self.assertEqual(
            simplify(
                ward.value - initial_endpoint.value + final_endpoint.value
            ),
            0,
        )

if __name__ == "__main__":
    unittest.main()

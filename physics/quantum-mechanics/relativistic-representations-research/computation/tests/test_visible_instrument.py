import unittest

from sympy import Matrix, Rational, eye, zeros

from fieldcalc.instrument import (
    VisibleInstrumentRequest,
    compile_visible_instrument,
)


class VisibleInstrumentTests(unittest.TestCase):
    def setUp(self):
        self.departure = Matrix([
            [1, 0],
            [0, 1],
            [1, 1],
        ])
        self.left = Matrix.diag(1, 0, 0)
        self.rest = Matrix.diag(0, 1, 1)
        self.coherent = Rational(1, 2) * Matrix([
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 0],
        ])
        self.request = VisibleInstrumentRequest(
            departure=self.departure,
            effects={
                "left": self.left,
                "rest": self.rest,
                "coherent": self.coherent,
            },
            partition=("left", "rest"),
            provenance="post-freeze three-channel bench",
            resource_budget=100,
        )

    def test_one_map_generates_inclusive_partition_and_coherent_returns(self):
        result = compile_visible_instrument(self.request)

        self.assertTrue(result.accepted)
        instrument = result.instrument
        self.assertEqual(instrument.inclusive, self.departure.H * self.departure)
        self.assertEqual(
            sum(instrument.channel_cells.values(), zeros(2)),
            instrument.inclusive,
        )
        self.assertEqual(instrument.partition_residual, zeros(3))
        self.assertEqual(
            instrument.effect_returns["coherent"],
            self.departure.H * self.coherent * self.departure,
        )
        self.assertTrue(all(instrument.effect_certificates.values()))
        self.assertEqual(instrument.cyclic_rank, 3)
        self.assertEqual(instrument.resource_cost, 33)

    def test_same_inclusive_return_can_hide_a_coherent_channel(self):
        plus = Matrix([1, 1]) / 2**Rational(1, 2)
        minus = Matrix([1, -1]) / 2**Rational(1, 2)
        coherent = plus * plus.H

        self.assertEqual(plus.H * plus, minus.H * minus)
        self.assertEqual((plus.H * coherent * plus)[0], 1)
        self.assertEqual((minus.H * coherent * minus)[0], 0)

    def test_postfreeze_phase_orbit_defeats_every_scalar_channel_summary(self):
        phase = Matrix.diag(1, -1, 1)
        rotated_departure = phase * self.departure
        coordinate_effects = {
            f"coordinate-{index}": Matrix.diag(*(
                1 if row == index else 0 for row in range(3)
            ))
            for index in range(3)
        }
        effects = coordinate_effects | {"coherent": self.coherent}
        requests = tuple(
            VisibleInstrumentRequest(
                departure=departure,
                effects=effects,
                partition=tuple(coordinate_effects),
                provenance="postfreeze coherent information falsifier",
                resource_budget=100,
            )
            for departure in (self.departure, rotated_departure)
        )
        instruments = tuple(
            compile_visible_instrument(request).instrument
            for request in requests
        )
        original, rotated = instruments

        self.assertEqual(original.inclusive, rotated.inclusive)
        for name in coordinate_effects:
            self.assertEqual(
                original.effect_returns[name],
                rotated.effect_returns[name],
            )
        self.assertNotEqual(
            original.effect_returns["coherent"],
            rotated.effect_returns["coherent"],
        )
        self.assertNotEqual(
            original.open_kernel(eye(2)).value,
            rotated.open_kernel(eye(2)).value,
        )
        self.assertEqual((original.cyclic_rank, rotated.cyclic_rank), (3, 3))

    def test_detector_partition_is_optional(self):
        result = compile_visible_instrument(VisibleInstrumentRequest(
            departure=self.departure,
            effects={"coherent": self.coherent},
            partition=(),
            provenance="coherent detector without a channel partition",
            resource_budget=20,
        ))

        self.assertTrue(result.accepted)
        self.assertEqual(result.instrument.channel_cells, {})
        self.assertIsNone(result.instrument.partition_residual)

    def test_same_departure_reconstructs_the_open_kernel(self):
        result = compile_visible_instrument(self.request)
        retained_resolvent = Matrix([[2, 1], [1, 3]])

        kernel = result.instrument.open_kernel(retained_resolvent)

        self.assertTrue(kernel.accepted)
        self.assertEqual(
            kernel.value,
            self.departure * retained_resolvent * self.departure.H,
        )
        self.assertEqual(
            result.instrument.open_kernel(eye(3)).refusal.reason,
            "resolvent shape does not match the retained space",
        )
        self.assertEqual(
            result.instrument.compress(eye(2)).refusal.reason,
            "observable shape does not match the channel fiber",
        )

    def test_invalid_effect_partition_shape_and_budget_are_refused(self):
        cases = (
            (
                {"bad": Matrix([[1, 1, 0], [0, 1, 0], [0, 0, 1]])},
                ("bad",),
                100,
                "effect must be Hermitian",
            ),
            (
                {"bad": Matrix.diag(1, -1, 1)},
                ("bad",),
                100,
                "effect positivity is not certified",
            ),
            (
                {"bad": Matrix.diag(2, 0, 0)},
                ("bad",),
                100,
                "effect upper bound is not certified",
            ),
            (
                {"left": self.left},
                ("left",),
                100,
                "detector partition must sum to the channel identity",
            ),
            (
                {"bad-shape": eye(2)},
                ("bad-shape",),
                100,
                "effect shape does not match the channel fiber",
            ),
            (
                {"identity": eye(3)},
                ("missing",),
                100,
                "partition effect is unavailable",
            ),
            (
                {"identity": eye(3)},
                ("identity",),
                1,
                "visible-instrument budget exceeded",
            ),
        )

        for effects, partition, budget, reason in cases:
            with self.subTest(reason=reason):
                result = compile_visible_instrument(VisibleInstrumentRequest(
                    departure=self.departure,
                    effects=effects,
                    partition=partition,
                    provenance="refusal bench",
                    resource_budget=budget,
                ))
                self.assertFalse(result.accepted)
                self.assertEqual(result.refusal.reason, reason)

        unavailable = compile_visible_instrument(VisibleInstrumentRequest(
            departure=Matrix(0, 0, []),
            effects={},
            partition=(),
            provenance="missing departure",
            resource_budget=1,
        ))
        self.assertFalse(unavailable.accepted)
        self.assertEqual(unavailable.refusal.reason, "departure map is unavailable")


if __name__ == "__main__":
    unittest.main()

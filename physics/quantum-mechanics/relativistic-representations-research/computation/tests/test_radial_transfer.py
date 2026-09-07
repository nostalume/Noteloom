import math
import unittest
from dataclasses import replace

from fieldcalc.measures import compile_visible_measure
from fieldcalc.models import ScalarModel, scalar_radial_data
from fieldcalc.numeric import Quadrature
from fieldcalc.radial import (
    RadialData,
    RadialDepartureRequest,
    compile_radial_departure,
)


class RadialMeasureAdapterTransferTests(unittest.TestCase):
    def setUp(self):
        model = ScalarModel(2.0, 1.0, 1.0, 0.2, 1.4)
        self.data = RadialData(
            amplitude=lambda radius: (
                model.coupling / (1.0 + (radius / model.cutoff) ** 2) ** 2
            ),
            energy=model.energy,
            threshold=model.boson_mass,
            level_gap=model.level_gap,
            support=(0.0, math.inf),
            provenance="algebraic-tail radial transfer",
        )
        result = compile_visible_measure(self.data.measure_request())
        self.assertTrue(result.accepted)
        self.continuum = result.measure

    def compile(self, cells=32):
        result = compile_radial_departure(RadialDepartureRequest(
            self.data, 12.0, cells, "algebraic-tail bench", 256, 1e-12,
        ))
        self.assertTrue(result.accepted)
        return result.radial

    def test_unchanged_compiler_transfers_to_an_algebraic_tail(self):
        continuum_bound = self.continuum.resolvent(0.0)
        continuum_open = self.continuum.open_event(0.5, self.data.level_gap)
        radial = [self.compile(cells) for cells in (16, 32, 64)]
        bound = [item.resolvent(0.0) for item in radial]
        opened = [item.open_event(0.5) for item in radial]

        for item, bound_result, open_result in zip(radial, bound, opened):
            self.assertEqual(item.continuum_measure_id, self.continuum.measure_id)
            self.assertGreater(item.mass_error_bound, 0.0)
            self.assertGreater(item.tail_mass_bound, 0.0)
            self.assertAlmostEqual(
                float((item.departure.H * item.departure)[0]),
                item.truncated_mass,
                places=14,
            )
            self.assertLessEqual(
                abs(bound_result.value - continuum_bound.value),
                bound_result.error_bound + continuum_bound.error,
            )
            self.assertLessEqual(
                abs(open_result.value - continuum_open.value),
                open_result.error_bound + continuum_open.error,
            )

        self.assertTrue(all(
            right.error_bound < left.error_bound
            for left, right in zip(bound, bound[1:])
        ))
        self.assertTrue(all(
            right.error_bound < left.error_bound
            for left, right in zip(opened, opened[1:])
        ))

    def test_gaussian_adapter_retains_an_exact_mass_operation(self):
        data = scalar_radial_data(ScalarModel(2.0, 1.0, 1.0, 0.2, 1.4))
        result = compile_radial_departure(RadialDepartureRequest(
            data, 5.0, 32, "Gaussian adapter regression", 256, 1e-13,
        ))

        self.assertTrue(result.accepted)
        self.assertEqual(result.radial.mass_error_bound, 0.0)

    def test_invalid_adapter_contracts_are_refused(self):
        cases = (
            (
                replace(self.data, support=(math.nan, math.inf)), 1e-12,
                "invalid radial channel domain",
            ),
            (
                replace(self.data, threshold=math.nan), 1e-12,
                "invalid radial channel domain",
            ),
            (
                replace(self.data, monotone_energy=False), 1e-12,
                "radial energy must be declared monotone",
            ),
            (
                replace(self.data, energy=lambda radius: 0.5), 1e-12,
                "radial threshold does not bound channel energy",
            ),
            (
                self.data, 0.0,
                "radial tolerance must be finite and positive",
            ),
            (
                replace(
                    self.data,
                    mass_operation=lambda left, right: Quadrature(
                        math.nan, 0.0, 0
                    ),
                ),
                1e-12,
                "radial cell mass is numerically unresolved",
            ),
        )

        for data, tolerance, reason in cases:
            with self.subTest(reason=reason):
                result = compile_radial_departure(RadialDepartureRequest(
                    data, 12.0, 8, "invalid adapter", 32, tolerance,
                ))
                self.assertFalse(result.accepted)
                self.assertEqual(result.refusal.reason, reason)


if __name__ == "__main__":
    unittest.main()

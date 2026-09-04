import math
import unittest

from fieldcalc.measures import MeasureRequest, compile_visible_measure
from fieldcalc.models import ScalarModel, scalar_departure_request


class VisibleMeasureTests(unittest.TestCase):
    def setUp(self):
        self.model = ScalarModel(
            particle_mass=2.0,
            boson_mass=1.0,
            cutoff=1.0,
            coupling=0.2,
            level_gap=1.4,
        )
        result = compile_visible_measure(scalar_departure_request(self.model))
        self.assertTrue(result.accepted)
        self.measure = result.measure

    def test_field_departure_mass_matches_gaussian_integral(self):
        mass = self.measure.total_mass()
        expected = self.model.coupling**2 * math.pi**1.5 * self.model.cutoff**3
        self.assertAlmostEqual(mass.value, expected, places=8)
        self.assertLess(mass.error, 1e-8)

    def test_bound_and_open_queries_reuse_identical_measure(self):
        bound = self.measure.resolvent(0.0)
        opened = self.measure.open_event(time=0.5, gap=self.model.level_gap)
        self.assertEqual(bound.measure_id, opened.measure_id)
        self.assertLess(bound.value, 0.0)
        self.assertGreaterEqual(opened.value, 0.0)
        self.assertLess(bound.error, 1e-8)
        self.assertLess(opened.error, 1e-8)

    def test_unpartitioned_nonmonotone_energy_is_refused(self):
        request = MeasureRequest(
            weight=lambda r: math.exp(-r),
            energy=lambda r: (r - 1.0) ** 2,
            support=(0.0, 3.0),
            provenance="nonmonotone witness",
        )
        result = compile_visible_measure(request)
        self.assertFalse(result.accepted)
        self.assertEqual(result.refusal.reason, "energy map is not monotone")


if __name__ == "__main__":
    unittest.main()

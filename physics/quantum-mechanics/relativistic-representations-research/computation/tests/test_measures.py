import math
import unittest

from fieldcalc.measures import MeasureRequest, compile_visible_measure
from fieldcalc.models import (
    ScalarModel,
    scalar_departure_request,
    scalar_radial_data,
)
from fieldcalc.radial import (
    RadialDepartureRequest,
    compile_radial_departure,
)


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


class RadialDepartureCompletionTests(unittest.TestCase):
    def setUp(self):
        self.model = ScalarModel(2.0, 1.0, 1.0, 0.2, 1.4)
        continuum = compile_visible_measure(scalar_departure_request(self.model))
        self.continuum = continuum.measure

    def compile(self, cells=32, radial_cutoff=5.0, budget=256):
        return compile_radial_departure(RadialDepartureRequest(
            data=scalar_radial_data(self.model),
            radial_cutoff=radial_cutoff,
            cell_count=cells,
            provenance="node 11 radial completion bench",
            resource_budget=budget,
        ))

    def test_cell_masses_generate_the_finite_fock_departure(self):
        result = self.compile()

        self.assertTrue(result.accepted)
        radial = result.radial
        departure_mass = float((radial.departure.H * radial.departure)[0])
        analytic_total = self.model.coupling**2 * math.pi**1.5 * self.model.cutoff**3
        self.assertAlmostEqual(departure_mass, radial.truncated_mass, places=14)
        self.assertAlmostEqual(
            radial.truncated_mass + radial.tail_mass,
            analytic_total,
            places=14,
        )
        self.assertEqual(radial.continuum_measure_id, self.continuum.measure_id)
        self.assertTrue(radial.departure_compilation.closed)

    def test_one_error_law_contains_bound_and_open_transform_errors(self):
        continuum_bound = self.continuum.resolvent(0.0)
        continuum_open = self.continuum.open_event(time=0.5, gap=self.model.level_gap)
        approximations = [self.compile(cells).radial for cells in (16, 32, 64)]
        bound_results = [item.resolvent(0.0) for item in approximations]
        open_results = [item.open_event(0.5) for item in approximations]

        for bound in bound_results:
            self.assertLessEqual(
                abs(bound.value - continuum_bound.value),
                bound.error_bound + continuum_bound.error,
            )
        for opened in open_results:
            self.assertLessEqual(
                abs(opened.value - continuum_open.value),
                opened.error_bound + continuum_open.error,
            )
        self.assertTrue(all(
            right.error_bound < left.error_bound
            for left, right in zip(bound_results, bound_results[1:])
        ))
        self.assertTrue(all(
            right.error_bound < left.error_bound
            for left, right in zip(open_results, open_results[1:])
        ))

    def test_normalization_is_robust_under_model_parameters(self):
        model = ScalarModel(3.0, 0.7, 0.8, 0.15, 1.1)
        result = compile_radial_departure(RadialDepartureRequest(
            scalar_radial_data(model), 4.0, 24,
            "second Gaussian parameter fixture", 64,
        ))

        self.assertTrue(result.accepted)
        radial = result.radial
        expected = model.coupling**2 * math.pi**1.5 * model.cutoff**3
        self.assertAlmostEqual(
            float((radial.departure.H * radial.departure)[0]),
            radial.truncated_mass,
            places=14,
        )
        self.assertAlmostEqual(radial.truncated_mass + radial.tail_mass, expected, places=14)

    def test_invalid_cutoff_cells_coupling_and_budget_are_refused(self):
        requests = (
            (RadialDepartureRequest(
                scalar_radial_data(self.model), 0.0, 8, "cutoff", 32,
             ), "radial cutoff must be finite and inside support"),
            (RadialDepartureRequest(
                scalar_radial_data(self.model), math.inf, 8, "infinite", 32,
             ), "radial cutoff must be finite and inside support"),
            (RadialDepartureRequest(
                scalar_radial_data(self.model), 4.0, 0, "cells", 32,
             ),
             "radial cell count must be a positive integer"),
            (RadialDepartureRequest(
                scalar_radial_data(self.model), 4.0, 1.5, "fractional", 32,
             ),
             "radial cell count must be a positive integer"),
            (RadialDepartureRequest(
                scalar_radial_data(ScalarModel(2.0, 1.0, 1.0, 0.0, 1.4)),
                4.0, 8, "zero", 32,
             ), "radial cell mass is numerically unresolved"),
            (RadialDepartureRequest(
                scalar_radial_data(self.model), 4.0, 8, "budget", 1,
             ),
             "departure compilation budget exceeded"),
        )

        for request, reason in requests:
            with self.subTest(reason=reason):
                result = compile_radial_departure(request)
                self.assertFalse(result.accepted)
                self.assertEqual(result.refusal.reason, reason)


if __name__ == "__main__":
    unittest.main()

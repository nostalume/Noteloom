import unittest

from fieldcalc.measures import compile_visible_measure
from fieldcalc.models import (
    ScalarModel,
    scalar_departure_request,
    scalar_radial_data,
)
from fieldcalc.radial import (
    RadialDepartureRequest,
    compile_radial_departure,
)


class MomentPreservingRadialTests(unittest.TestCase):
    def setUp(self):
        self.model = ScalarModel(2.0, 1.0, 1.0, 0.2, 1.4)
        self.continuum = compile_visible_measure(
            scalar_departure_request(self.model)
        ).measure

    def compile(self, cells):
        result = compile_radial_departure(RadialDepartureRequest(
            scalar_radial_data(self.model), 5.0, cells,
            "moment-preserving radial bench", 256,
        ))
        self.assertTrue(result.accepted)
        return result.radial

    def test_moment_centering_generates_a_common_second_order_certificate(self):
        continuum_bound = self.continuum.resolvent(0.0)
        continuum_open = self.continuum.open_event(0.5, self.model.level_gap)
        radial = [self.compile(cells) for cells in (16, 32, 64)]
        bound = [item.resolvent(0.0) for item in radial]
        opened = [item.open_event(0.5) for item in radial]

        for compiled, bound_result, open_result in zip(radial, bound, opened):
            self.assertGreater(compiled.centered_second_moment_bound, 0.0)
            self.assertGreater(compiled.moment_evaluations, 0)
            self.assertLessEqual(
                abs(bound_result.value - continuum_bound.value),
                bound_result.error_bound + continuum_bound.error,
            )
            self.assertLessEqual(
                abs(open_result.value - continuum_open.value),
                open_result.error_bound + continuum_open.error,
            )
            self.assertLess(
                bound_result.moment_bound,
                bound_result.variation_bound,
            )
            self.assertLess(
                open_result.moment_bound,
                open_result.variation_bound,
            )

        self.assertTrue(all(
            right.error_bound < 0.3 * left.error_bound
            for left, right in zip(bound, bound[1:])
        ))
        self.assertTrue(all(
            right.error_bound < 0.3 * left.error_bound
            for left, right in zip(opened, opened[1:])
        ))

    def test_cost_receipt_includes_preprocessing_and_direct_queries(self):
        radial = self.compile(32)
        bound = radial.resolvent(0.0)
        opened = radial.open_event(0.5)
        direct_bound = self.continuum.resolvent(
            0.0, absolute_tolerance=bound.error_bound
        )
        direct_open = self.continuum.open_event(
            0.5, self.model.level_gap,
            absolute_tolerance=opened.error_bound,
        )

        self.assertGreater(direct_bound.evaluations, 0)
        self.assertGreater(direct_open.evaluations, 0)
        self.assertLessEqual(direct_bound.error, bound.error_bound)
        self.assertLessEqual(direct_open.error, opened.error_bound)
        self.assertEqual(radial.query_evaluations, 32)
        self.assertGreater(radial.moment_evaluations, radial.query_evaluations)
        direct_batch = direct_bound.evaluations + direct_open.evaluations
        compiled_batch = 2 * radial.query_evaluations
        self.assertGreater(direct_batch, compiled_batch)
        break_even = radial.moment_evaluations // (direct_batch - compiled_batch) + 1
        self.assertGreaterEqual(
            radial.moment_evaluations + (break_even - 1) * compiled_batch,
            (break_even - 1) * direct_batch,
        )
        self.assertLess(
            radial.moment_evaluations + break_even * compiled_batch,
            break_even * direct_batch,
        )

    def test_certificate_is_robust_within_the_gaussian_family(self):
        model = ScalarModel(3.0, 0.7, 0.8, 0.15, 1.1)
        continuum = compile_visible_measure(scalar_departure_request(model)).measure
        result = compile_radial_departure(RadialDepartureRequest(
            scalar_radial_data(model), 4.0, 24,
            "moment robustness fixture", 64,
        ))

        self.assertTrue(result.accepted)
        bound = result.radial.resolvent(0.0)
        opened = result.radial.open_event(0.4)
        self.assertLessEqual(
            abs(bound.value - continuum.resolvent(0.0).value),
            bound.error_bound + continuum.resolvent(0.0).error,
        )
        self.assertLessEqual(
            abs(opened.value - continuum.open_event(0.4, model.level_gap).value),
            opened.error_bound + continuum.open_event(0.4, model.level_gap).error,
        )

    def test_numerically_unresolved_cells_are_refused(self):
        result = compile_radial_departure(RadialDepartureRequest(
            scalar_radial_data(self.model), 100.0, 8,
            "underflow fixture", 32,
        ))

        self.assertFalse(result.accepted)
        self.assertEqual(
            result.refusal.reason, "radial cell mass is numerically unresolved"
        )

    def test_direct_tolerance_must_be_finite_and_positive(self):
        for tolerance in (0.0, float("inf")):
            with self.subTest(tolerance=tolerance):
                with self.assertRaisesRegex(
                    ValueError, "absolute tolerance must be finite and positive"
                ):
                    self.continuum.resolvent(
                        0.0, absolute_tolerance=tolerance
                    )


if __name__ == "__main__":
    unittest.main()

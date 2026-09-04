import unittest

from fieldcalc.measures import curvature_threshold_power
from fieldcalc.residual import compare_carrier_costs


class ResearchRegressionTests(unittest.TestCase):
    def test_curvature_threshold_power_is_generated(self):
        self.assertEqual(curvature_threshold_power(spatial_dimension=3, spin=0), 1)
        self.assertEqual(curvature_threshold_power(spatial_dimension=3, spin=2), 5)

    def test_direct_constrained_route_has_no_generic_cost_gain(self):
        verdict = compare_carrier_costs(spin=3)
        self.assertEqual(verdict.preferred, "compensated")
        self.assertGreater(verdict.direct_load, verdict.compensated_load)

    def test_single_layer_preparation_is_presentation_neutral(self):
        verdict = compare_carrier_costs(spin=2, active_layers=1)
        self.assertEqual(verdict.preferred, "tie")
        self.assertEqual(verdict.active_direct_solves, verdict.active_compensated_solves)


if __name__ == "__main__":
    unittest.main()

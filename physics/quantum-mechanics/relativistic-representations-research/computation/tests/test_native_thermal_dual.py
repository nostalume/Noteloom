import unittest

from fieldcalc.impurity import AndersonRequest, compile_anderson
from fieldcalc.native_car import compile_native_graded_reachability
from fieldcalc.native_dual import compile_native_thermal_dual


class NativeThermalDualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.system = compile_anderson(AndersonRequest(
            impurity_energy=-1.0,
            interaction=2.0,
            bath_energies=(-0.75, 0.75),
            hybridizations=(1.0 / 3.0, 1.0 / 3.0),
            beta=2.0,
            matsubara_index=0,
            coefficient_order=4,
            quadrature_order=12,
            provenance="node 53 native thermal dual",
            resource_budget=500_000_000,
        )).system
        cls.native = compile_native_graded_reachability(
            cls.system,
            coefficient_order=4,
            tolerance=1e-10,
            resource_budget=20_000_000,
        ).model

    def test_native_dual_exposes_a_bounded_resource_obstruction(self):
        result = compile_native_thermal_dual(
            self.system,
            self.native,
            thermal_order=4,
            tolerance=1e-10,
            coefficient_budget=100_000,
            resource_budget=100_000_000,
        )
        self.assertFalse(result.accepted)
        self.assertEqual(
            result.refusal.reason,
            "native thermal-dual resource budget exceeded",
        )
        self.assertIsNotNone(result.boundary)
        self.assertEqual(result.boundary.active_grade, 1)
        self.assertEqual(result.boundary.ranks_by_grade, (136, 76, 0, 0, 0))
        self.assertEqual(result.boundary.support_by_grade, (5_394, 11_495, 0, 0, 0))
        self.assertEqual(result.boundary.retained_coefficients, 16_889)
        self.assertAlmostEqual(
            result.boundary.commutator_module_escape,
            0.5527707983925674,
        )
        self.assertEqual(result.boundary.resource_used, 101_866_899)

    def test_native_dual_refuses_a_tiny_coefficient_budget(self):
        result = compile_native_thermal_dual(
            self.system,
            self.native,
            thermal_order=4,
            tolerance=1e-10,
            coefficient_budget=1,
            resource_budget=100_000_000,
        )
        self.assertFalse(result.accepted)
        self.assertEqual(result.refusal.reason, "native thermal-dual support exceeded")


if __name__ == "__main__":
    unittest.main()

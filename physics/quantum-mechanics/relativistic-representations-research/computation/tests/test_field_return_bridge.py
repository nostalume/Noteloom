import cmath
import unittest

from fieldcalc.return_bridge import (
    FieldReturnRequest,
    compile_field_return,
)


class FieldReturnBridgeTests(unittest.TestCase):
    def setUp(self):
        self.request = FieldReturnRequest(
            bare_energy=-0.5,
            coupling=0.25,
            form_factor_squared=lambda _energy: 1.0,
            band=(0.0, 1.0),
            provenance="flat single-channel field bench",
            mode_budget=256,
        )
        result = compile_field_return(self.request)
        self.assertTrue(result.accepted)
        self.return_ = result.return_

    def test_one_measure_generates_bound_and_open_outputs(self):
        bound = self.return_.bound_state((-0.75, -0.25))
        opened = self.return_.open_channel(0.25)

        self.assertEqual(bound.measure_id, opened.measure_id)
        self.assertLess(bound.energy, 0.0)
        self.assertGreater(bound.residue, 0.0)
        self.assertLess(bound.residue, 1.0)
        self.assertLess(abs(opened.unitarity_residual), 1e-12)

    def test_flat_measure_reconstructs_the_analytic_return(self):
        z = -0.3 + 0.4j
        expected = self.request.coupling**2 * cmath.log(z / (z - 1.0))

        self.assertAlmostEqual(self.return_.self_energy(z).real, expected.real, places=10)
        self.assertAlmostEqual(self.return_.self_energy(z).imag, expected.imag, places=10)

    def test_reduced_and_direct_finite_mode_routes_have_same_target(self):
        comparison = self.return_.compare_finite_modes(-0.2 + 0.3j, mode_count=48)

        self.assertLess(comparison.residual, 1e-11)
        self.assertLess(comparison.reduced_operations, comparison.direct_operations)
        self.assertEqual(comparison.reduced_operations, comparison.expert_operations)
        self.assertFalse(comparison.advantage_over_expert)
        self.assertEqual(comparison.observable, "projected-resolvent")

    def test_continuum_error_and_resource_boundary_are_explicit(self):
        comparison = self.return_.compare_finite_modes(-0.2 + 0.3j, mode_count=256)
        refused = self.return_.compare_finite_modes(-0.2 + 0.3j, mode_count=257)

        self.assertLess(comparison.continuum_error, 2e-6)
        self.assertFalse(refused.accepted)
        self.assertEqual(refused.refusal.reason, "finite-mode budget exceeded")

    def test_finite_mode_family_converges_to_the_same_continuum_return(self):
        errors = [
            self.return_.compare_finite_modes(-0.2 + 0.3j, count).continuum_error
            for count in (16, 32, 64, 128, 256)
        ]

        self.assertTrue(all(right < left for left, right in zip(errors, errors[1:])))

    def test_invalid_or_nonbound_requests_are_refused(self):
        invalid = compile_field_return(FieldReturnRequest(
            bare_energy=0.5,
            coupling=-0.25,
            form_factor_squared=lambda _energy: 1.0,
            band=(0.0, 1.0),
            provenance="invalid coupling",
        ))
        missing_pole = self.return_.bound_state((-2.0, -1.0))

        self.assertFalse(invalid.accepted)
        self.assertEqual(invalid.refusal.reason, "coupling must be nonnegative")
        self.assertFalse(missing_pole.accepted)
        self.assertEqual(missing_pole.refusal.reason, "bound pole is not bracketed")


if __name__ == "__main__":
    unittest.main()

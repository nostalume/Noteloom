import unittest

from sympy import Rational, log, pi, simplify

from fieldcalc.soft_channel import compile_leading_soft_bin_transfer


class LeadingSoftBinTransferTests(unittest.TestCase):
    def test_three_photon_endpoints_generate_one_normalized_bin_transfer(self):
        hard_density = 1 / (128 * pi)
        endpoint = 1 / (1024 * pi**3)
        coupling_squared = Rational(1, 1000)
        infrared = Rational(1, 100)
        resolution = Rational(1, 20)
        soft_ceiling = Rational(1, 5)

        result = compile_leading_soft_bin_transfer(
            hard_density=hard_density,
            photon_phase_coefficient=1 / (8 * pi**2),
            current_weights=(1, 1),
            observed_power_residues=(endpoint, endpoint),
            observed_log_residues=(-endpoint, -endpoint),
            infrared_scale=infrared,
            detector_resolution=resolution,
            soft_ceiling=soft_ceiling,
            coupling_squared=coupling_squared,
        )

        self.assertTrue(result.accepted)
        self.assertEqual(result.generated_power_residues, (endpoint, endpoint))
        self.assertEqual(result.factorization_residuals, (0, 0))
        self.assertEqual(result.distinct_kernel_count, 1)
        self.assertEqual(simplify(result.transfer_residual), 0)
        self.assertEqual(simplify(result.normalization_residual), 0)
        self.assertEqual(
            simplify(result.lower_bin_correction + result.resolved_correction), 0
        )
        self.assertEqual(
            simplify(
                result.resolved_correction
                - 2
                * coupling_squared
                * endpoint
                * (1 / resolution - 1 / soft_ceiling)
            ),
            0,
        )
        self.assertEqual(
            simplify(
                result.unmatched_real_log
                + 2
                * coupling_squared
                * endpoint
                * log(resolution / infrared)
            ),
            0,
        )
        self.assertFalse(result.singularly_complete)

    def test_compiler_refuses_unmatched_endpoint_or_invalid_scale_order(self):
        endpoint = 1 / (1024 * pi**3)
        common = dict(
            hard_density=1 / (128 * pi),
            photon_phase_coefficient=1 / (8 * pi**2),
            current_weights=(1, 1),
            observed_log_residues=(-endpoint, -endpoint),
            coupling_squared=Rational(1, 1000),
        )

        mismatch = compile_leading_soft_bin_transfer(
            **common,
            observed_power_residues=(endpoint, 2 * endpoint),
            infrared_scale=Rational(1, 100),
            detector_resolution=Rational(1, 20),
            soft_ceiling=Rational(1, 5),
        )
        self.assertFalse(mismatch.accepted)
        self.assertEqual(
            mismatch.refusal.reason,
            "observed soft pole does not factor through the hard event",
        )

        invalid_order = compile_leading_soft_bin_transfer(
            **common,
            observed_power_residues=(endpoint, endpoint),
            infrared_scale=Rational(1, 10),
            detector_resolution=Rational(1, 20),
            soft_ceiling=Rational(1, 5),
        )
        self.assertFalse(invalid_order.accepted)
        self.assertEqual(
            invalid_order.refusal.reason,
            "soft scales must satisfy 0 < infrared < resolution < ceiling",
        )

        uncontrolled = compile_leading_soft_bin_transfer(
            **{**common, "coupling_squared": 1},
            observed_power_residues=(endpoint, endpoint),
            infrared_scale=Rational(1, 100),
            detector_resolution=Rational(1, 20),
            soft_ceiling=Rational(1, 5),
        )
        self.assertFalse(uncontrolled.accepted)
        self.assertEqual(
            uncontrolled.refusal.reason,
            "leading-soft no-jump weight leaves the perturbative regime",
        )


if __name__ == "__main__":
    unittest.main()

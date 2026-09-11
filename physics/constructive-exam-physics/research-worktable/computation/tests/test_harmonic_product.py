import unittest

from sympy import I, cos, simplify, sin, symbols

from occ.harmonic_product import (
    HarmonicProductRequest,
    construct_harmonic_product,
)
from worktable.harmonic_product_cases import run_a11_coil, run_a23_coil


class HarmonicProductTests(unittest.TestCase):
    def test_product_constructs_exact_dc_and_second_harmonic_channels(self):
        omega, time = symbols("omega time", positive=True, real=True)
        left_real, left_imaginary, right_real, right_imaginary, scale = symbols(
            "a_r a_i b_r b_i s", real=True
        )
        left = left_real + I * left_imaginary
        right = right_real + I * right_imaginary
        request = HarmonicProductRequest(
            problem_id="two-phasor-fixture",
            product_name="bilinear observable",
            left_phasor=left,
            right_phasor=right,
            angular_frequency=omega,
            time=time,
            scale=scale,
        )

        result = construct_harmonic_product(request)

        expected_dc = (
            scale * (left_real * right_real + left_imaginary * right_imaginary) / 2
        )
        expected_second = (
            scale
            * (
                left_real * right_real
                - left_imaginary * right_imaginary
                + I * (left_real * right_imaginary + left_imaginary * right_real)
            )
            / 2
        )
        self.assertEqual(result.status, "constructed")
        self.assertEqual(simplify(result.dc_component - expected_dc), 0)
        self.assertEqual(simplify(result.second_harmonic_phasor - expected_second), 0)
        self.assertEqual(
            simplify(
                result.time_signal
                - expected_dc
                - expected_second.as_real_imag()[0] * cos(2 * omega * time)
                + expected_second.as_real_imag()[1] * sin(2 * omega * time)
            ),
            0,
        )
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_a23_coil_composes_response_and_product_into_all_requested_returns(self):
        case = run_a23_coil()
        scale = case.flux_scale
        resistance = case.resistance
        inductance = case.inductance
        omega = case.angular_frequency
        time = case.time
        denominator = resistance**2 + (omega * inductance) ** 2
        expected_current = (
            -scale * omega * (omega * inductance + I * resistance) / denominator
        )

        self.assertEqual(case.response.status, "constructed")
        self.assertEqual(
            simplify(case.emf_signal - scale * omega * sin(omega * time)), 0
        )
        self.assertEqual(
            simplify(case.response.observables[0].phasor - expected_current), 0
        )
        self.assertEqual(case.torque.status, "constructed")
        self.assertEqual(
            simplify(
                case.torque.dc_component
                - scale**2 * omega * resistance / (2 * denominator)
            ),
            0,
        )
        self.assertEqual(
            simplify(
                case.torque.second_harmonic_phasor
                - scale**2
                * omega
                * (-resistance + I * omega * inductance)
                / (2 * denominator)
            ),
            0,
        )
        self.assertEqual(case.average_power_balance_residual, 0)
        self.assertEqual(case.admission.classification, "always_direct")

    def test_a11_coil_transfers_unchanged_product_to_zero_inductance_limit(self):
        case = run_a11_coil()
        scale = case.flux_scale
        resistance = case.resistance
        omega = case.angular_frequency
        time = case.time

        self.assertEqual(case.response.status, "constructed")
        self.assertEqual(
            simplify(
                case.response.observables[0].time_signal
                - scale * omega * sin(omega * time) / resistance
            ),
            0,
        )
        self.assertEqual(
            simplify(case.torque.dc_component - scale**2 * omega / (2 * resistance)),
            0,
        )
        self.assertEqual(
            simplify(
                case.torque.second_harmonic_phasor + scale**2 * omega / (2 * resistance)
            ),
            0,
        )
        self.assertEqual(
            simplify(
                case.torque.time_signal
                - scale**2 * omega * (1 - cos(2 * omega * time)) / (2 * resistance)
            ),
            0,
        )

    def test_product_admission_rejects_time_dependence_and_nonphysical_scalars(self):
        omega, time = symbols("omega time", positive=True, real=True)
        cases = (
            {"left_phasor": time, "scale": 1, "angular_frequency": omega},
            {"left_phasor": 1, "scale": I, "angular_frequency": omega},
            {"left_phasor": 1, "scale": 1, "angular_frequency": 0},
        )

        for values in cases:
            with self.subTest(values=values), self.assertRaises(ValueError):
                HarmonicProductRequest(
                    problem_id="invalid-product",
                    product_name="invalid",
                    left_phasor=values["left_phasor"],
                    right_phasor=1,
                    angular_frequency=values["angular_frequency"],
                    time=time,
                    scale=values["scale"],
                )


if __name__ == "__main__":
    unittest.main()

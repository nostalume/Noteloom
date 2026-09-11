import unittest

from sympy import I, Rational, cos, exp, pi, simplify, sin, sqrt, symbols

from occ.harmonic import (
    HarmonicObservable,
    HarmonicResponseRequest,
    construct_harmonic_response,
)
from occ.harmonic_pattern import (
    SpatialHarmonicRequest,
    construct_spatial_harmonic_pattern,
)
from worktable.harmonic_cases import run_a21_wave, run_a25_rlc


class HarmonicResponseTests(unittest.TestCase):
    def test_exact_linear_phasor_preserves_magnitude_phase_and_real_return(self):
        response = symbols("response")
        omega, time = symbols("omega time", positive=True, real=True)
        request = HarmonicResponseRequest(
            problem_id="linear-phasor-fixture",
            laws=((3 + 4 * I) * response - 10,),
            unknowns=(response,),
            observables=(HarmonicObservable("response", response, reference=10),),
            angular_frequency=omega,
            time=time,
        )

        result = construct_harmonic_response(request)

        self.assertEqual(result.status, "constructed")
        observed = result.observables[0]
        self.assertEqual(observed.phasor, Rational(6, 5) - Rational(8, 5) * I)
        self.assertEqual(observed.magnitude_squared, 4)
        self.assertEqual(
            observed.time_signal,
            Rational(6, 5) * cos(omega * time) + Rational(8, 5) * sin(omega * time),
        )
        self.assertEqual(observed.reference_phase_cosine, Rational(3, 5))
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_finite_spatial_response_constructs_exact_nodes_and_antinodes(self):
        amplitude, coordinate = symbols("A theta", positive=True, real=True)
        request = SpatialHarmonicRequest(
            phasor=2 * I * amplitude * cos(coordinate),
            coordinate=coordinate,
            lower=0,
            upper=Rational(11, 2) * pi,
        )

        result = construct_spatial_harmonic_pattern(request)

        self.assertEqual(result.status, "constructed")
        self.assertEqual(
            result.nodes,
            tuple(Rational(2 * index + 1, 2) * pi for index in range(6)),
        )
        self.assertEqual(result.antinodes, tuple(index * pi for index in range(6)))
        self.assertEqual(result.maximum_magnitude_squared, 4 * amplitude**2)
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_a21_wave_constructs_reflection_pattern_and_requested_point_signal(self):
        case = run_a21_wave()

        self.assertEqual(case.response.status, "constructed")
        self.assertEqual(case.reflected_phasor, I * case.amplitude)
        self.assertEqual(
            case.response.observables[0].phasor,
            2 * I * case.amplitude * cos(case.coordinate),
        )
        self.assertEqual(case.pattern.status, "constructed")
        self.assertEqual(
            case.pattern.nodes,
            tuple(Rational(2 * index + 1, 2) * pi for index in range(6)),
        )
        self.assertEqual(
            case.pattern.antinodes, tuple(index * pi for index in range(6))
        )
        self.assertEqual(
            case.q_signal,
            -2 * case.amplitude * sin(case.angular_frequency * case.time),
        )

    def test_a25_rlc_transfers_same_constructor_and_preserves_leading_phase(self):
        case = run_a25_rlc()
        observed = case.response.observables[0]
        discriminant = 15_676_369

        self.assertEqual(case.response.status, "constructed")
        self.assertEqual(case.impedance, 30 - Rational(3937, 14) * I)
        self.assertEqual(observed.magnitude_squared, Rational(7_840_000, discriminant))
        self.assertEqual(
            simplify(observed.reference_phase_cosine - 420 / sqrt(discriminant)),
            0,
        )
        self.assertGreater(observed.phasor.as_real_imag()[1], 0)
        self.assertEqual(case.admission.classification, "always_direct")

    def test_nonlinear_and_underdetermined_phasor_laws_are_distinct_refusals(self):
        first, second = symbols("first second")
        omega, time = symbols("omega time", positive=True, real=True)
        nonlinear = construct_harmonic_response(
            HarmonicResponseRequest(
                "nonlinear",
                (first**2 - 1,),
                (first,),
                (HarmonicObservable("first", first),),
                omega,
                time,
            )
        )
        underdetermined = construct_harmonic_response(
            HarmonicResponseRequest(
                "underdetermined",
                (first + second - 1,),
                (first, second),
                (HarmonicObservable("first", first),),
                omega,
                time,
            )
        )

        self.assertEqual(nonlinear.obstruction.code, "nonlinear_phasor_law")
        self.assertEqual(
            underdetermined.obstruction.code,
            "underdetermined_phasor_response",
        )

    def test_nonfinite_spatial_pattern_is_refused(self):
        coordinate = symbols("theta", real=True)
        request = SpatialHarmonicRequest(
            phasor=exp(I * coordinate),
            coordinate=coordinate,
            lower=0,
            upper=2 * pi,
        )

        result = construct_spatial_harmonic_pattern(request)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "nonfinite_spatial_pattern")

    def test_zero_phase_reference_returns_a_typed_refusal(self):
        response = symbols("response")
        omega, time = symbols("omega time", positive=True, real=True)
        request = HarmonicResponseRequest(
            "zero-reference",
            (response - 1,),
            (response,),
            (HarmonicObservable("response", response, reference=0),),
            omega,
            time,
        )

        result = construct_harmonic_response(request)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "undefined_phase_reference")


if __name__ == "__main__":
    unittest.main()

import math
import unittest

from sympy import Matrix, Rational, diag, diff, limit, pi, simplify, sqrt, symbols

from fieldcalc.clifford import clifford_scalar, clifford_vector
from fieldcalc.exterior import compile_exterior_normal_form, exterior_product
from fieldcalc.fermion_line import compile_fermion_line_amplitude
from fieldcalc.measures import (
    PreparedEventMeasureRequest,
    compile_prepared_event_measure,
)
from fieldcalc.multiphoton import (
    compile_fermion_three_photon_event,
    compile_resolved_three_photon_slice,
)
from fieldcalc.soft_channel import (
    compile_leading_soft_bin_transfer,
    compile_soft_effect_jet,
)


class FermionMultiphotonEventTests(unittest.TestCase):
    def setUp(self):
        self.parameter = symbols("u", positive=True)
        self.kinematics = compile_resolved_three_photon_slice(
            self.parameter, resolution=Rational(1, 10)
        )

    def measure(self, event):
        return compile_prepared_event_measure(PreparedEventMeasureRequest(
            effect=event.effect,
            parameter=self.parameter,
            phase_space_density=self.kinematics.phase_space_density,
            support=(0.0, math.inf),
            provenance="resolved three-photon fermion slice",
        ))

    def unresolved_left_soft_event(self):
        x = symbols("x", positive=True)
        y = (1 - 2 * x) / (2 * (1 - x))
        metric = diag(-1, 1, 1)
        initial = Matrix((1, 0, 0))
        momenta = (
            Matrix((1, 1, 0)), Matrix((-x, 0, -x)), Matrix((-y, 0, y)),
        )
        vectors = (Matrix((0, 0, 1)), Matrix((0, -1, 0)), Matrix((0, 1, 0)))
        amplitude = compile_fermion_line_amplitude(
            metric, initial, momenta, vectors, 1,
            state_budget=8, route="subset grade",
        )
        self.assertTrue(amplitude.accepted, amplitude.refusal)
        final = initial + sum(momenta, Matrix.zeros(3, 1))
        initial_projector = compile_exterior_normal_form(
            Rational(1, 2) * (clifford_scalar(1) + clifford_vector(initial)),
            metric,
        ).operator
        final_projector = compile_exterior_normal_form(
            Rational(1, 2) * (clifford_scalar(1) + clifford_vector(final)),
            metric,
        ).operator
        phase_density = 1 / (128 * pi**3 * (1 - x))
        return (
            x, y, amplitude.amplitude, initial_projector, final_projector,
            phase_density,
        )

    def test_shell_generates_a_positive_soft_excluded_slice(self):
        result = self.kinematics
        u = self.parameter

        self.assertTrue(result.accepted, result.refusal)
        self.assertEqual(result.shell_residuals, (0, 0, 0, 0, 0))
        self.assertEqual(result.transversality_residuals, (0, 0, 0))
        self.assertEqual(result.resolution_residuals, (0, 0, 0, 0, 0))
        self.assertEqual(result.exchange_map, Rational(81, 50) / u)
        self.assertEqual(
            simplify(result.first_energy - (40 * u + 9) / (90 * (u + 1))), 0
        )
        self.assertEqual(
            simplify(result.second_energy - (5 * u + 36) / (50 * u + 81)), 0
        )
        self.assertEqual(
            simplify(
                result.phase_space_density
                - 31 / (128 * pi**3 * (u + 1) * (50 * u + 81))
            ),
            0,
        )
        self.assertIs(result.phase_space_density.is_nonnegative, True)

    def test_subset_and_history_routes_recover_one_detector_measure(self):
        subset = compile_fermion_three_photon_event(
            self.kinematics, state_budget=8, route="subset grade"
        )
        direct = compile_fermion_three_photon_event(
            self.kinematics, state_budget=8, route="ordered histories"
        )

        self.assertTrue(subset.accepted, subset.refusal)
        self.assertTrue(direct.accepted, direct.refusal)
        self.assertEqual(subset.effect.value, direct.effect.value)
        self.assertEqual(subset.ward_residuals, (0, 0, 0))
        self.assertEqual(direct.ward_residuals, (0, 0, 0))
        self.assertEqual(subset.exchange_residual, 0)
        self.assertEqual(direct.exchange_residual, 0)
        self.assertLess(subset.total_updates, direct.total_updates)

        subset_measure = self.measure(subset)
        direct_measure = self.measure(direct)
        self.assertTrue(subset_measure.accepted, subset_measure.refusal)
        self.assertTrue(direct_measure.accepted, direct_measure.refusal)
        self.assertEqual(subset_measure.measure.density, direct_measure.measure.density)
        self.assertEqual(subset_measure.measure.measure_id, direct_measure.measure.measure_id)
        total = subset_measure.measure.total_mass()
        balanced = subset_measure.measure.fraction((0.0, float(9 * sqrt(2) / 10)))
        self.assertGreater(total.value, 0)
        self.assertGreater(balanced.value, 0)
        self.assertLess(balanced.value, 1)
        self.assertAlmostEqual(balanced.value, 0.5, places=11)
        self.assertLess(max(total.error, balanced.error), 1e-9)

    def test_resolution_is_a_physical_boundary_not_a_silent_regulator(self):
        unresolved = compile_resolved_three_photon_slice(
            self.parameter, resolution=0
        )

        self.assertFalse(unresolved.accepted)
        self.assertEqual(
            unresolved.refusal.reason,
            "detector resolution must exclude both soft boundaries",
        )
        odd_sector = compile_fermion_three_photon_event(
            self.kinematics,
            state_budget=8,
            parity_doubled=False,
        )
        self.assertFalse(odd_sector.accepted)
        self.assertEqual(
            odd_sector.refusal.reason,
            "single-parity odd Clifford trace is not generated",
        )

    def test_unresolved_density_exposes_both_soft_poles(self):
        (
            x, y, amplitude, initial_projector, final_projector, phase_density,
        ) = self.unresolved_left_soft_event()
        product = exterior_product(final_projector, amplitude)
        product = exterior_product(product.operator, initial_projector)
        product = exterior_product(product.operator, amplitude.adjoint())
        density = simplify(2 * product.operator.scalar_part * phase_density)

        left_power = limit(x**2 * density, x, 0, dir="+")
        left_log = limit(
            x * (density - left_power / x**2), x, 0, dir="+"
        )
        right_density = simplify(density / (-diff(y, x)))
        right_power = limit(
            y**2 * right_density, x, Rational(1, 2), dir="-"
        )
        right_log = limit(
            y * (right_density - right_power / y**2),
            x,
            Rational(1, 2),
            dir="-",
        )
        endpoint = 1 / (1024 * pi**3)

        self.assertEqual((left_power, right_power), (endpoint, endpoint))
        self.assertEqual((left_log, right_log), (-endpoint, -endpoint))

        transfer = compile_leading_soft_bin_transfer(
            hard_density=1 / (128 * pi),
            photon_phase_coefficient=1 / (8 * pi**2),
            current_weights=(1, 1),
            observed_power_residues=(left_power, right_power),
            observed_log_residues=(left_log, right_log),
            infrared_scale=Rational(1, 100),
            detector_resolution=Rational(1, 20),
            soft_ceiling=Rational(1, 5),
            coupling_squared=Rational(1, 1000),
        )
        self.assertTrue(transfer.accepted, transfer.refusal)
        self.assertEqual(transfer.factorization_residuals, (0, 0))
        self.assertEqual(transfer.transfer_residual, 0)
        self.assertFalse(transfer.singularly_complete)

    def test_soft_effect_jet_constructs_the_logarithmic_obstruction(self):
        (
            x, _, amplitude, initial_projector, final_projector, phase_density,
        ) = self.unresolved_left_soft_event()
        result = compile_soft_effect_jet(
            parameter=x,
            amplitude=amplitude,
            initial_projector=initial_projector,
            final_projector=final_projector,
            phase_density=phase_density,
        )
        endpoint = 1 / (1024 * pi**3)

        self.assertTrue(result.accepted, result.refusal)
        self.assertEqual(result.density_power_residue, endpoint)
        self.assertEqual(result.phase_tangent_contribution, endpoint)
        self.assertEqual(result.response_tangent_contribution, -2 * endpoint)
        self.assertEqual(result.density_log_residue, -endpoint)
        self.assertEqual(result.certificate_residuals, (0, 0))

    def test_soft_effect_jet_refuses_absent_or_higher_poles(self):
        x = symbols("x", positive=True)
        metric = diag(-1, 1, 1)
        projector = compile_exterior_normal_form(clifford_scalar(1), metric).operator

        regular = compile_exterior_normal_form(clifford_scalar(1 + x), metric).operator
        absent = compile_soft_effect_jet(
            parameter=x,
            amplitude=regular,
            initial_projector=projector,
            final_projector=projector,
            phase_density=1,
        )
        self.assertFalse(absent.accepted)
        self.assertEqual(
            absent.refusal.reason, "amplitude has no generated simple soft pole"
        )

        double = compile_exterior_normal_form(clifford_scalar(x**-2), metric).operator
        excessive = compile_soft_effect_jet(
            parameter=x,
            amplitude=double,
            initial_projector=projector,
            final_projector=projector,
            phase_density=1,
        )
        self.assertFalse(excessive.accepted)
        self.assertEqual(
            excessive.refusal.reason,
            "soft jet exceeds the admitted first-order boundary",
        )


if __name__ == "__main__":
    unittest.main()

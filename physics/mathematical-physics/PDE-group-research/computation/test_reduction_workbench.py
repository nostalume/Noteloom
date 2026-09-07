import json
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXAMPLES = HERE / "examples"


class ReductionWorkbenchTests(unittest.TestCase):
    def test_registry_exposes_three_distinct_reduction_families(self):
        from reduction_workbench import available_backends

        self.assertEqual(
            available_backends(),
            ("cyclic", "factor-centralizer", "stratified-orbit"),
        )

    def test_factor_centralizer_result_has_common_exact_envelope(self):
        from reduction_workbench import run_request

        result = run_request(
            {
                "backend": "factor-centralizer",
                "input": EXAMPLES / "rotated-anisotropic-e3.json",
                "observable": "full discrete spectrum and heat trace",
            }
        )

        self.assertEqual(result["schema"], "reduction-witness/v1")
        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["selected_route"], "factor")
        self.assertTrue(result["witness"]["residuals"]["all_passed"])
        self.assertIn("detail", result)

    def test_cyclic_results_distinguish_exact_and_controlled(self):
        from reduction_workbench import run_request

        exact = run_request(
            {
                "backend": "cyclic",
                "input": EXAMPLES / "hidden-sector.json",
                "observable": "preparation spectral response",
            }
        )
        controlled = run_request(
            {
                "backend": "cyclic",
                "input": EXAMPLES / "controlled-truncation.json",
                "observable": "finite-time survival amplitude",
            }
        )

        self.assertEqual(exact["outcome"], "exact")
        self.assertEqual(controlled["outcome"], "controlled")
        self.assertEqual(exact["witness"]["reduced_object"]["dimension"], 2)
        self.assertEqual(controlled["witness"]["error"]["tolerance"], "1/5")
        self.assertTrue(controlled["witness"]["residuals"]["all_passed"])

    def test_stratified_orbit_obstruction_uses_same_envelope(self):
        from reduction_workbench import run_request

        result = run_request(
            {
                "backend": "stratified-orbit",
                "input": EXAMPLES / "warped-axis-wrong-regularity.json",
                "observable": "Dirichlet solution at fixed relative L2 accuracy",
            }
        )

        self.assertEqual(result["outcome"], "obstructed")
        self.assertEqual(result["witness"], None)
        self.assertIn("isotropy", result["obstruction"]["reason"])

    def test_stratified_orbit_success_preserves_numerical_contract(self):
        from reduction_workbench import run_request

        result = run_request(
            {
                "backend": "stratified-orbit",
                "input": EXAMPLES / "warped-axis-manufactured.json",
                "observable": "Dirichlet solution at fixed relative L2 accuracy",
            }
        )

        self.assertEqual(result["outcome"], "controlled")
        self.assertEqual(result["witness"]["reduced_object"]["weights"], [0, 1, 2])
        self.assertTrue(result["witness"]["residuals"]["all_passed"])
        self.assertLess(result["witness"]["cost"]["solved_dof_ratio"], 1)

    def test_unknown_backend_is_a_typed_refusal(self):
        from reduction_workbench import run_request

        result = run_request({"backend": "imaginary", "input": EXAMPLES / "hidden-sector.json"})

        self.assertEqual(result["outcome"], "obstructed")
        self.assertEqual(result["obstruction"]["kind"], "UnknownBackend")

    def test_backend_refuses_an_observable_it_does_not_recover(self):
        from reduction_workbench import run_request

        result = run_request(
            {
                "backend": "factor-centralizer",
                "input": EXAMPLES / "rotated-anisotropic-e3.json",
                "observable": "scattering phase",
            }
        )

        self.assertEqual(result["outcome"], "obstructed")
        self.assertEqual(result["obstruction"]["kind"], "UnsupportedObservable")

    def test_cli_emits_compact_summary(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(HERE / "reduction_workbench.py"),
                "cyclic",
                str(EXAMPLES / "hidden-sector.json"),
                "--observable",
                "preparation spectral response",
                "--summary",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertEqual(set(summary), {"backend", "decision", "outcome", "schema", "witness"})
        self.assertNotIn("detail", summary)

    def test_discovery_selects_cyclic_when_preparation_hides_modes(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "quadratic-survival-compressed.json")

        self.assertEqual(result["schema"], "reduction-decision/v1")
        self.assertNotIn("backend", result["request"])
        self.assertEqual(
            {probe["route"] for probe in result["probes"]},
            {"full-modes", "observable-cyclic"},
        )
        self.assertTrue(all(probe["applicable"] for probe in result["probes"]))
        self.assertTrue(result["coincidence"]["all_passed"])
        self.assertEqual(result["decision"]["selected_route"], "observable-cyclic")
        self.assertEqual(result["decision"]["visible_dimension"], 1)
        self.assertEqual(result["human_card"]["eliminated_directions"], 2)

    def test_discovery_selects_full_modes_when_cyclic_degree_is_full(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "quadratic-survival-full.json")

        self.assertEqual(result["outcome"], "exact")
        self.assertTrue(result["coincidence"]["all_passed"])
        self.assertEqual(result["decision"]["visible_dimension"], 3)
        self.assertEqual(result["decision"]["selected_route"], "full-modes")
        self.assertEqual(result["human_card"]["eliminated_directions"], 0)

    def test_discovery_refuses_nonconfining_quadratic_problem(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "quadratic-survival-indefinite.json")

        self.assertEqual(result["outcome"], "obstructed")
        self.assertEqual(result["obstruction"]["kind"], "NonPositiveStiffness")
        self.assertTrue(all(not probe["applicable"] for probe in result["probes"]))

    def test_discovery_keeps_cyclic_when_exact_factor_probe_cannot_split(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "quadratic-survival-cyclic-only.json")

        probes = {probe["route"]: probe for probe in result["probes"]}
        self.assertEqual(result["outcome"], "exact")
        self.assertFalse(probes["full-modes"]["applicable"])
        self.assertEqual(probes["full-modes"]["first_residual"], "NonRationalSpectrum")
        self.assertTrue(probes["observable-cyclic"]["applicable"])
        self.assertEqual(result["decision"]["selected_route"], "observable-cyclic")
        self.assertEqual(result["decision"]["visible_dimension"], 2)
        self.assertEqual(result["coincidence"]["status"], "single_applicable_route")

    def test_discovery_cli_needs_no_backend_name(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(HERE / "reduction_workbench.py"),
                "discover",
                str(EXAMPLES / "quadratic-survival-compressed.json"),
                "--summary",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertEqual(summary["decision"]["selected_route"], "observable-cyclic")
        self.assertEqual(summary["human_card"]["eliminated_directions"], 2)
        self.assertNotIn("candidates", summary)

    def test_spinor_bilateral_discovery_constructs_the_same_channels(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "pauli-landau-positive.json")

        self.assertEqual(result["schema"], "reduction-decision/v1")
        self.assertEqual(result["outcome"], "exact")
        self.assertNotIn("backend", result["request"])
        self.assertEqual(
            {probe["route"] for probe in result["probes"]},
            {"representation-to-pde", "pde-to-representation"},
        )
        self.assertTrue(all(probe["applicable"] for probe in result["probes"]))
        self.assertTrue(result["coincidence"]["all_passed"])
        self.assertEqual(result["decision"]["selected_route"], "bilateral-common-reduction")
        channels = result["decision"]["common_transverse_channels"]
        self.assertEqual(
            [(item["orbital_level"], item["spin"], item["energy_offset"]) for item in channels],
            [
                (0, "curvature-aligned", "0"),
                (0, "curvature-antialigned", "6"),
                (1, "curvature-aligned", "6"),
                (1, "curvature-antialigned", "12"),
                (2, "curvature-aligned", "12"),
                (2, "curvature-antialigned", "18"),
            ],
        )
        self.assertEqual(
            result["candidates"][1]["witness"]["reduced_object"]["algebra"],
            "graded Clifford-Heisenberg algebra with longitudinal translation",
        )

    def test_spinor_bilateral_transfer_reverses_the_zero_mode_projector(self):
        from reduction_workbench import discover_problem

        positive = discover_problem(EXAMPLES / "pauli-landau-positive.json")
        negative = discover_problem(EXAMPLES / "pauli-landau-negative.json")

        self.assertEqual(negative["outcome"], "exact")
        self.assertEqual(negative["decision"]["charge_sign"], -1)
        self.assertEqual(
            negative["decision"]["common_transverse_channels"],
            positive["decision"]["common_transverse_channels"],
        )
        self.assertEqual(
            positive["decision"]["curvature_aligned_projector"],
            [["1", "0"], ["0", "0"]],
        )
        self.assertEqual(
            negative["decision"]["curvature_aligned_projector"],
            [["0", "0"], ["0", "1"]],
        )

    def test_spinor_inverse_refuses_a_broken_spin_curvature_term_independently(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "pauli-landau-inconsistent.json")

        probes = {probe["route"]: probe for probe in result["probes"]}
        self.assertEqual(result["outcome"], "obstructed")
        self.assertTrue(probes["representation-to-pde"]["applicable"])
        self.assertFalse(probes["pde-to-representation"]["applicable"])
        self.assertEqual(
            probes["pde-to-representation"]["first_residual"],
            "SpinCurvatureResidual",
        )
        self.assertEqual(len(result["candidates"]), 1)
        self.assertEqual(result["decision"]["selected_route"], None)

    def test_global_pauli_promotion_constructs_measure_degeneracy_and_heat_density(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "pauli-landau-global-positive.json")

        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["selected_route"], "global-landau-fourier")
        self.assertEqual(result["analytic_witness"]["topology"]["chern_number"], 2)
        self.assertEqual(
            result["analytic_witness"]["magnetic_translation_representation"]["dimension"],
            2,
        )
        self.assertEqual(result["analytic_witness"]["direct_integral"]["measure"], "dk/(2*pi)")
        observable = result["analytic_witness"]["observable"]
        self.assertEqual(
            observable["exact_formula"],
            "2*coth(3*t)/(2*sqrt(pi*t))",
        )
        self.assertLessEqual(
            observable["finite_level_audit"]["tail_bound"],
            observable["finite_level_audit"]["requested_tolerance"],
        )
        self.assertAlmostEqual(
            observable["numeric_value"],
            observable["finite_level_audit"]["partial_sum"]
            + observable["finite_level_audit"]["exact_tail"],
            places=14,
        )
        self.assertTrue(result["analytic_witness"]["residuals"]["all_passed"])

    def test_global_pauli_charge_reversal_conjugates_topology_but_preserves_heat_density(self):
        from reduction_workbench import discover_problem

        positive = discover_problem(EXAMPLES / "pauli-landau-global-positive.json")
        negative = discover_problem(EXAMPLES / "pauli-landau-global-negative.json")

        self.assertEqual(negative["outcome"], "exact")
        self.assertEqual(negative["analytic_witness"]["topology"]["chern_number"], -2)
        self.assertEqual(negative["analytic_witness"]["topology"]["landau_multiplicity"], 2)
        self.assertAlmostEqual(
            positive["analytic_witness"]["observable"]["numeric_value"],
            negative["analytic_witness"]["observable"]["numeric_value"],
            places=14,
        )

    def test_global_pauli_refuses_nonintegral_flux_after_local_bridge_succeeds(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "pauli-landau-global-nonintegral.json")

        probes = {probe["route"]: probe for probe in result["probes"]}
        self.assertEqual(result["outcome"], "obstructed")
        self.assertTrue(probes["representation-to-pde"]["applicable"])
        self.assertTrue(probes["pde-to-representation"]["applicable"])
        self.assertFalse(probes["global-analytic-promotion"]["applicable"])
        self.assertEqual(
            probes["global-analytic-promotion"]["first_residual"],
            "FluxQuantizationObstruction",
        )
        self.assertEqual(len(result["candidates"]), 2)

    def test_global_pauli_refuses_an_unrecognized_self_adjoint_domain_contract(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "pauli-landau-global-wrong-domain.json")

        self.assertEqual(result["outcome"], "obstructed")
        self.assertEqual(result["obstruction"]["kind"], "DomainContractObstruction")
        self.assertEqual(result["decision"]["selected_route"], None)

    def test_global_pauli_reports_unresolved_when_heat_audit_budget_is_too_small(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "pauli-landau-global-small-budget.json")

        self.assertEqual(result["outcome"], "unresolved")
        self.assertEqual(result["obstruction"]["kind"], "HeatTailBudgetExceeded")
        self.assertEqual(len(result["candidates"]), 2)
        self.assertEqual(result["probes"][-1]["first_residual"], "HeatTailBudgetExceeded")

    def test_su3_outer_multiplicity_changes_the_transition_route(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "su-adjoint-transition-su3.json")

        self.assertEqual(result["schema"], "reduction-decision/v1")
        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["selected_route"], "two-channel-outer-multiplicity")
        self.assertEqual(result["decision"]["group_channel_dimension"], 2)
        self.assertEqual(result["decision"]["visible_channel_dimension"], 2)
        self.assertEqual(
            result["decision"]["observable"],
            {
                "ordered": "5",
                "exchange_reversed": "1",
                "antisymmetric_part": "2",
                "symmetric_part": "3",
            },
        )
        probes = {probe["route"]: probe for probe in result["probes"]}
        self.assertTrue(probes["multiplicity-aware-natural-operations"]["applicable"])
        self.assertFalse(probes["single-antisymmetric-channel"]["applicable"])
        self.assertEqual(
            probes["single-antisymmetric-channel"]["first_residual"],
            "VisibleSymmetricChannel",
        )
        self.assertFalse(probes["single-symmetric-channel"]["applicable"])
        self.assertEqual(
            probes["single-symmetric-channel"]["first_residual"],
            "VisibleAntisymmetricChannel",
        )
        witness = result["candidates"][0]["witness"]
        self.assertTrue(witness["residuals"]["all_passed"])
        self.assertEqual(witness["cost"]["stored_dynamics_coefficients"], 2)
        self.assertEqual(witness["cost"]["uncompressed_component_coefficients"], 512)

    def test_su2_control_removes_the_jordan_channel_and_selects_one_copy(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "su-adjoint-transition-su2.json")

        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["selected_route"], "single-antisymmetric-channel")
        self.assertEqual(result["decision"]["group_channel_dimension"], 1)
        self.assertEqual(result["decision"]["visible_channel_dimension"], 1)
        self.assertEqual(
            result["decision"]["observable"],
            {
                "ordered": "4",
                "exchange_reversed": "-4",
                "antisymmetric_part": "4",
                "symmetric_part": "0",
            },
        )
        certificate = result["candidates"][0]["witness"]["residuals"]["checks"]
        self.assertTrue(certificate["rank_two_cayley_hamilton_kills_jordan_channel"])

    def test_su_adjoint_router_refuses_nontraceless_carrier_data(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "su-adjoint-transition-nontraceless.json")

        self.assertEqual(result["outcome"], "obstructed")
        self.assertEqual(result["obstruction"]["kind"], "CarrierViolation")
        self.assertEqual(result["decision"]["selected_route"], None)

    def test_su3_adjoint_pde_reduces_exactly_on_the_matrix_coefficient_core(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "su-adjoint-pde-su3.json")

        self.assertEqual(result["schema"], "reduction-decision/v1")
        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(
            result["decision"]["selected_route"],
            "adjoint-coefficient-pde-reduction",
        )
        self.assertEqual(result["decision"]["adjoint_casimir"], "3")
        self.assertEqual(result["decision"]["differential_source_factor"], "4")
        self.assertEqual(
            result["decision"]["observable"],
            {
                "ordered": "5",
                "exchange_reversed": "1",
                "antisymmetric_part": "2",
                "symmetric_part": "3",
            },
        )
        witness = result["candidates"][0]["witness"]
        self.assertTrue(witness["residuals"]["all_passed"])
        self.assertEqual(
            witness["maps"]["analysis"],
            "A(q_Y)=Y on the adjoint matrix-coefficient core",
        )
        self.assertEqual(
            witness["maps"]["synthesis"],
            "S(Y)=q_Y with q_Y(g)=Ad_(g^-1)Y",
        )
        self.assertEqual(
            result["analytic_witness"]["domain"],
            "H^2(SU(3),sl_3(C)) -> L^2(SU(3),sl_3(C))",
        )
        self.assertEqual(witness["cost"]["coordinate_charts"], 0)
        self.assertEqual(witness["cost"]["carrier_dimension_reduction"], 0)
        self.assertEqual(witness["cost"]["spatial_differential_solves_on_visible_core"], 0)

    def test_su2_adjoint_pde_transfer_keeps_only_the_bracket_channel(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "su-adjoint-pde-su2.json")

        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["adjoint_casimir"], "2")
        self.assertEqual(result["decision"]["differential_source_factor"], "3")
        self.assertEqual(result["decision"]["group_channel_dimension"], 1)
        self.assertEqual(result["decision"]["visible_channel_dimension"], 1)
        self.assertEqual(
            result["decision"]["observable"],
            {
                "ordered": "4",
                "exchange_reversed": "-4",
                "antisymmetric_part": "4",
                "symmetric_part": "0",
            },
        )

    def test_su_adjoint_pde_refuses_an_inadequate_operator_domain(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "su-adjoint-pde-wrong-domain.json")

        self.assertEqual(result["outcome"], "obstructed")
        self.assertEqual(result["obstruction"]["kind"], "DomainContractObstruction")
        self.assertEqual(result["decision"]["selected_route"], None)

    def test_matrix_pde_inverse_closes_to_sl3_and_matches_forward_observable(self):
        from reduction_workbench import discover_problem

        inverse_path = EXAMPLES / "matrix-pde-inverse-sl3.json"
        inverse_payload = json.loads(inverse_path.read_text(encoding="utf-8"))
        inverse = discover_problem(inverse_path)
        forward = discover_problem(EXAMPLES / "su-adjoint-pde-su3.json")

        self.assertNotIn("group_family", inverse_payload)
        self.assertEqual(inverse["outcome"], "exact")
        self.assertEqual(inverse["decision"]["effective_complex_lie_algebra"], "sl_3(C)")
        self.assertEqual(inverse["decision"]["closure_dimension"], 8)
        self.assertEqual(inverse["decision"]["global_group"], "unresolved")
        self.assertEqual(inverse["decision"]["observable"], forward["decision"]["observable"])
        self.assertTrue(inverse["coincidence"]["all_passed"])

    def test_matrix_pde_inverse_transfers_to_sl2_and_loses_jordan_channel(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "matrix-pde-inverse-sl2.json")

        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["effective_complex_lie_algebra"], "sl_2(C)")
        self.assertEqual(result["decision"]["closure_dimension"], 3)
        self.assertEqual(result["decision"]["group_channel_dimension"], 1)
        self.assertEqual(result["decision"]["visible_channel_dimension"], 1)
        self.assertEqual(
            result["decision"]["observable"],
            {
                "ordered": "4",
                "exchange_reversed": "-4",
                "antisymmetric_part": "4",
                "symmetric_part": "0",
            },
        )

    def test_matrix_pde_inverse_refuses_a_nonspanning_seed_family(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "matrix-pde-inverse-incomplete.json")

        self.assertEqual(result["outcome"], "obstructed")
        self.assertEqual(result["obstruction"]["kind"], "IncompleteCoefficientAlgebra")
        self.assertEqual(result["decision"]["selected_route"], None)

    def test_matrix_symbol_generates_covariance_and_casimir_without_labels(self):
        from matrix_symbol_covariance_router import discover_problem as discover_symbol
        from reduction_workbench import discover_problem

        path = EXAMPLES / "matrix-symbol-covariance-sl3.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        result = discover_problem(path)
        self.assertEqual(discover_symbol(path), result)
        prior = discover_problem(EXAMPLES / "matrix-pde-inverse-sl3.json")

        self.assertNotIn("group_family", payload)
        self.assertNotIn("coefficient_differential_action", payload)
        self.assertNotIn("effective_lie_algebra", payload)
        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["effective_complex_lie_algebra"], "sl_3(C)")
        self.assertEqual(result["decision"]["covariance_generator_dimension"], 8)
        self.assertEqual(result["decision"]["derived_coefficient_eigenvalue"], "3")
        self.assertEqual(result["decision"]["observable"], prior["decision"]["observable"])
        checks = result["coincidence"]["checks"]
        self.assertTrue(checks["principal_pairing_is_covariant"])
        self.assertTrue(checks["generated_derivations_form_a_lie_representation"])
        self.assertTrue(checks["pairing_dual_square_is_scalar_on_linear_coefficients"])

    def test_matrix_symbol_casimir_transfers_to_rank_two(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "matrix-symbol-covariance-sl2.json")

        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["effective_complex_lie_algebra"], "sl_2(C)")
        self.assertEqual(result["decision"]["covariance_generator_dimension"], 3)
        self.assertEqual(result["decision"]["derived_coefficient_eigenvalue"], "2")
        self.assertEqual(result["decision"]["group_channel_dimension"], 1)
        self.assertEqual(result["decision"]["visible_channel_dimension"], 1)

    def test_matrix_symbol_refuses_a_noninvariant_principal_pairing(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "matrix-symbol-covariance-broken-pairing.json")

        self.assertEqual(result["outcome"], "obstructed")
        self.assertEqual(result["obstruction"]["kind"], "PrincipalSymbolCovarianceObstruction")
        self.assertEqual(result["decision"]["selected_route"], None)

    def test_matrix_adjoint_semigroup_promotes_to_effective_compact_carrier(self):
        from reduction_workbench import discover_problem

        path = EXAMPLES / "matrix-adjoint-semigroup-sl3.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        result = discover_problem(path)
        local = discover_problem(EXAMPLES / "matrix-symbol-covariance-sl3.json")

        self.assertNotIn("group_family", payload)
        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["constructed_simply_connected_group"], "SU(3)")
        self.assertEqual(result["decision"]["observable_effective_group"], "PSU(3)")
        self.assertEqual(result["decision"]["center_order"], 3)
        self.assertEqual(result["decision"]["adjoint_eigenvalue"], "3")
        self.assertEqual(result["decision"]["heat_matrix_element_symbolic"], "exp(-3/2)")
        self.assertAlmostEqual(
            result["decision"]["heat_matrix_element_numeric"], 0.22313016014842982
        )
        self.assertEqual(result["decision"]["exchange_observable"], local["decision"]["observable"])
        self.assertTrue(result["coincidence"]["checks"]["central_quotient_observable_coincidence"])

    def test_matrix_adjoint_semigroup_transfers_to_rank_two(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "matrix-adjoint-semigroup-sl2.json")

        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["constructed_simply_connected_group"], "SU(2)")
        self.assertEqual(result["decision"]["observable_effective_group"], "PSU(2)")
        self.assertEqual(result["decision"]["center_order"], 2)
        self.assertEqual(result["decision"]["heat_matrix_element_symbolic"], "exp(-2/3)")

    def test_matrix_adjoint_semigroup_refuses_noncompact_real_form_data(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "matrix-adjoint-semigroup-wrong-real-form.json")

        self.assertEqual(result["outcome"], "obstructed")
        self.assertEqual(result["obstruction"]["kind"], "RealFormPositivityObstruction")
        self.assertEqual(result["local_stage"]["outcome"], "exact")

    def test_matrix_adjoint_semigroup_refuses_inadequate_laplacian_domain(self):
        from reduction_workbench import discover_problem

        result = discover_problem(EXAMPLES / "matrix-adjoint-semigroup-wrong-domain.json")

        self.assertEqual(result["outcome"], "obstructed")
        self.assertEqual(result["obstruction"]["kind"], "DomainContractObstruction")
        self.assertEqual(result["local_stage"]["outcome"], "exact")


if __name__ == "__main__":
    unittest.main()

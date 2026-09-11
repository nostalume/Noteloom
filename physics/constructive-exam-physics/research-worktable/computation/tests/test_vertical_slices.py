import math
import unittest
from fractions import Fraction

from occ.parameterized import compile_problem


def mechanics_problem(**parameter_changes):
    parameters = {
        "angular_speed_rad_s": 7.2921159e-5,
        "latitude_rad": math.pi / 4,
        "velocity_enu_m_s": [0.0, 2.0, 0.0],
        "cross_channel_enu": [1.0, 0.0, 0.0],
        "width_m": 100.0,
        "gravity_m_s2": 9.81,
    }
    parameters.update(parameter_changes)
    return {
        "objects": ["rotating_frame", "steady_free_surface"],
        "observable": "signed_surface_height_difference",
        "parameters": parameters,
    }


def zeeman_problem(**changes):
    problem = {
        "objects": [
            "ls_term",
            "electric_dipole_transition",
            "weak_magnetic_field",
        ],
        "observable": "zeeman_line_shifts",
        "parameters": {
            "upper": {"L": 1, "S": "1/2", "J": "3/2", "parity": "odd"},
            "lower": {"L": 0, "S": "1/2", "J": "1/2", "parity": "even"},
            "zeeman_to_fine_ratio": 0.01,
            "weak_ratio_max": 0.1,
        },
    }
    problem["parameters"].update(changes)
    return problem


def electromagnetic_problem(observable="rms_current_density_ratio", **changes):
    parameters = {
        "conductivity_s_m": 5.8e7,
        "permittivity_f_m": 8.8541878128e-12,
        "angular_frequency_rad_s": 1.0e3,
    }
    parameters.update(changes)
    return {
        "objects": [
            "linear_isotropic_medium",
            "time_harmonic_electric_field",
            "conduction_current",
            "displacement_current",
        ],
        "observable": observable,
        "parameters": parameters,
    }


def phonon_count_problem(**changes):
    parameters = {
        "spatial_dimension": 3,
        "basis_atom_count": 2,
        "population_count": 100,
        "population_kind": "atoms",
        "stable_translation_modes": True,
    }
    parameters.update(changes)
    return {
        "objects": ["bravais_lattice", "basis", "harmonic_displacements"],
        "observable": "phonon_mode_count",
        "parameters": parameters,
    }


class MechanicsVerticalSliceTests(unittest.TestCase):
    def test_m_r_compiles_coriolis_height_with_certificates(self):
        problem = mechanics_problem()

        result = compile_problem(problem)

        expected = (
            2
            * problem["parameters"]["angular_speed_rad_s"]
            * 2.0
            * math.sin(math.pi / 4)
            * 100.0
            / 9.81
        )
        self.assertEqual(result.status, "solved")
        self.assertEqual(result.adapter, "mechanics.rotating_free_surface")
        self.assertAlmostEqual(
            result.value["signed_height_difference_m"], expected, places=15
        )
        self.assertEqual(
            [step.operation for step in result.route],
            [
                "construct_rotation_vector",
                "coriolis_cross_product",
                "steady_free_surface_balance",
                "project_across_channel",
            ],
        )
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_m_i_reversing_cross_channel_orientation_reverses_sign(self):
        eastward = compile_problem(mechanics_problem())
        westward = compile_problem(
            mechanics_problem(cross_channel_enu=[-1.0, 0.0, 0.0])
        )

        self.assertAlmostEqual(
            westward.value["signed_height_difference_m"],
            -eastward.value["signed_height_difference_m"],
            places=15,
        )

    def test_m_i_transfers_from_northward_to_eastward_flow(self):
        problem = mechanics_problem(
            velocity_enu_m_s=[3.0, 0.0, 0.0],
            cross_channel_enu=[0.0, 1.0, 0.0],
        )

        result = compile_problem(problem)

        expected = (
            -2
            * problem["parameters"]["angular_speed_rad_s"]
            * 3.0
            * math.sin(math.pi / 4)
            * 100.0
            / 9.81
        )
        self.assertEqual(result.status, "solved")
        self.assertAlmostEqual(
            result.value["signed_height_difference_m"], expected, places=15
        )

    def test_m_x_missing_latitude_returns_smallest_missing_datum(self):
        problem = mechanics_problem()
        del problem["parameters"]["latitude_rad"]

        result = compile_problem(problem)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "missing_field")
        self.assertEqual(result.obstruction.fields, ("latitude_rad",))


class AtomicVerticalSliceTests(unittest.TestCase):
    def test_q_r_constructs_six_zeeman_lines(self):
        result = compile_problem(zeeman_problem())

        self.assertEqual(result.status, "solved")
        self.assertEqual(result.adapter, "atomic.weak_field_zeeman")
        self.assertEqual(
            result.value["g_factors"],
            {"upper": Fraction(4, 3), "lower": Fraction(2, 1)},
        )
        self.assertEqual(result.value["transition_count"], 6)
        self.assertEqual(
            result.value["shift_coefficients"],
            [
                Fraction(-5, 3),
                Fraction(-1, 1),
                Fraction(-1, 3),
                Fraction(1, 3),
                Fraction(1, 1),
                Fraction(5, 3),
            ],
        )
        self.assertEqual(result.value["polarization_counts"], {"pi": 2, "sigma": 4})
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_q_i_transfers_to_a_different_ls_transition(self):
        result = compile_problem(
            zeeman_problem(
                upper={"L": 2, "S": "1/2", "J": "5/2", "parity": "even"},
                lower={"L": 1, "S": "1/2", "J": "3/2", "parity": "odd"},
            )
        )

        self.assertEqual(result.status, "solved")
        self.assertEqual(
            result.value["g_factors"],
            {"upper": Fraction(6, 5), "lower": Fraction(4, 3)},
        )
        self.assertEqual(result.value["transition_count"], 12)
        self.assertEqual(
            result.value["shift_coefficients"],
            [
                Fraction(-7, 5),
                Fraction(-19, 15),
                Fraction(-17, 15),
                Fraction(-1, 1),
                Fraction(-1, 5),
                Fraction(-1, 15),
                Fraction(1, 15),
                Fraction(1, 5),
                Fraction(1, 1),
                Fraction(17, 15),
                Fraction(19, 15),
                Fraction(7, 5),
            ],
        )

    def test_q_x_refuses_missing_or_nonweak_regime(self):
        missing = zeeman_problem()
        del missing["parameters"]["zeeman_to_fine_ratio"]

        missing_result = compile_problem(missing)
        strong_result = compile_problem(zeeman_problem(zeeman_to_fine_ratio=0.5))

        self.assertEqual(missing_result.status, "refused")
        self.assertEqual(missing_result.obstruction.code, "missing_field")
        self.assertEqual(missing_result.obstruction.fields, ("zeeman_to_fine_ratio",))
        self.assertEqual(strong_result.status, "refused")
        self.assertEqual(strong_result.obstruction.code, "unsupported_regime")

    def test_q_x_refuses_same_parity_electric_dipole_terms(self):
        result = compile_problem(
            zeeman_problem(lower={"L": 0, "S": "1/2", "J": "1/2", "parity": "odd"})
        )

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "forbidden_transition")


class ElectromagneticVerticalSliceTests(unittest.TestCase):
    def test_e_r_compiles_scalar_current_ratio(self):
        problem = electromagnetic_problem()

        result = compile_problem(problem)

        expected = 5.8e7 / (1.0e3 * 8.8541878128e-12)
        self.assertEqual(result.status, "solved")
        self.assertEqual(result.adapter, "electromagnetism.harmonic_response")
        self.assertAlmostEqual(result.value["rms_ratio"], expected, places=6)
        self.assertAlmostEqual(result.value["phase_difference_rad"], math.pi / 2)
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_e_i_recovers_crossover_frequency_from_same_constitutive_pair(self):
        result = compile_problem(
            electromagnetic_problem(observable="crossover_angular_frequency")
        )

        self.assertEqual(result.status, "solved")
        self.assertAlmostEqual(
            result.value["angular_frequency_rad_s"],
            5.8e7 / 8.8541878128e-12,
            places=6,
        )

    def test_e_x_refuses_tensor_medium_without_directional_observable(self):
        problem = {
            "objects": [
                "linear_anisotropic_medium",
                "time_harmonic_electric_field",
                "conduction_current",
                "displacement_current",
            ],
            "observable": "rms_current_density_ratio",
            "parameters": {
                "conductivity_tensor_s_m": [[2.0, 0.0], [0.0, 1.0]],
                "permittivity_tensor_f_m": [[1.0, 0.0], [0.0, 3.0]],
                "angular_frequency_rad_s": 2.0,
            },
        }

        result = compile_problem(problem)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "nonunique_observable")
        self.assertEqual(result.obstruction.fields, ("field_direction", "norm"))


class CondensedMatterVerticalSliceTests(unittest.TestCase):
    def test_c_r_compiles_diamond_branch_and_atom_count(self):
        result = compile_problem(phonon_count_problem())

        self.assertEqual(result.status, "solved")
        self.assertEqual(result.adapter, "condensed_matter.phonon_count")
        self.assertEqual(
            result.value,
            {
                "total_branches": 6,
                "acoustic_branches": 3,
                "optical_branches": 3,
                "total_modes": 300,
                "population_kind": "atoms",
            },
        )
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_c_i_transfers_to_general_dimension_and_basis(self):
        result = compile_problem(
            phonon_count_problem(
                spatial_dimension=2,
                basis_atom_count=3,
                population_count=40,
                population_kind="primitive_cells",
            )
        )

        self.assertEqual(result.status, "solved")
        self.assertEqual(result.value["total_branches"], 6)
        self.assertEqual(result.value["acoustic_branches"], 2)
        self.assertEqual(result.value["optical_branches"], 4)
        self.assertEqual(result.value["total_modes"], 240)

    def test_c_x_refuses_ambiguous_population_count(self):
        problem = phonon_count_problem()
        del problem["parameters"]["population_kind"]

        result = compile_problem(problem)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "ambiguous_count")
        self.assertEqual(result.obstruction.fields, ("population_kind",))


class CrossDomainCompositionTests(unittest.TestCase):
    def test_x_c_composes_phonon_measure_with_bose_thermal_response(self):
        result = compile_problem(
            {
                "objects": [
                    "phonon_frequency_measure",
                    "bosonic_thermal_ensemble",
                ],
                "observable": "constant_volume_heat_capacity",
                "parameters": {
                    "frequencies_rad_s": [math.log(2.0)],
                    "degeneracies": [3],
                    "temperature_k": 1.0,
                    "hbar_j_s": 1.0,
                    "boltzmann_j_k": 1.0,
                },
            }
        )

        self.assertEqual(result.status, "solved")
        self.assertEqual(result.adapter, "composition.phonon_heat_capacity")
        self.assertAlmostEqual(
            result.value["heat_capacity_j_k"],
            6.0 * math.log(2.0) ** 2,
        )
        self.assertEqual(result.value["represented_modes"], 3)
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_x_c_transfers_across_equivalent_energy_temperature_scaling(self):
        base = {
            "objects": ["phonon_frequency_measure", "bosonic_thermal_ensemble"],
            "observable": "constant_volume_heat_capacity",
            "parameters": {
                "frequencies_rad_s": [0.5, 2.0],
                "degeneracies": [1, 2],
                "temperature_k": 4.0,
                "hbar_j_s": 1.0,
                "boltzmann_j_k": 1.0,
            },
        }
        scaled = {
            **base,
            "parameters": {
                **base["parameters"],
                "frequencies_rad_s": [1.0, 4.0],
                "temperature_k": 8.0,
            },
        }

        first = compile_problem(base)
        second = compile_problem(scaled)

        self.assertEqual(first.status, "solved")
        self.assertEqual(second.status, "solved")
        self.assertAlmostEqual(
            first.value["heat_capacity_j_k"],
            second.value["heat_capacity_j_k"],
        )

    def test_x_c_refuses_mode_count_without_frequency_measure(self):
        result = compile_problem(
            {
                "objects": ["phonon_mode_count", "bosonic_thermal_ensemble"],
                "observable": "constant_volume_heat_capacity",
                "parameters": {
                    "total_modes": 300,
                    "temperature_k": 100.0,
                },
            }
        )

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "insufficient_port")
        self.assertEqual(
            result.obstruction.fields,
            ("frequencies_rad_s", "degeneracies"),
        )


class KernelBoundaryTests(unittest.TestCase):
    def test_unknown_semantic_types_refuse_without_guessing_a_law(self):
        result = compile_problem(
            {
                "objects": ["unknown_medium"],
                "observable": "unknown_observable",
                "parameters": {},
            }
        )

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "no_adapter")


if __name__ == "__main__":
    unittest.main()

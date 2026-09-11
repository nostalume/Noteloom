from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).parents[1]
COMMANDS = {
    "corpus-audit": (
        "total: 126",
        "  symbolic-differential-operator: 1",
    ),
    "polynomial-batch": (
        "A25-03\tcomplete\t1 targets\tcertificate=pass",
        "batch: 19/19 passed",
    ),
    "route-benchmark": (
        "problem\tstatus\tbaseline\tproposed\tbetter\tworse",
        "verdict\texam_leverage_not_established",
    ),
    "route-admission": (
        "problem\tclass\tproposed cheaper when\tunit probe",
        "verdict\tconditional_admission_constructed_weights_unmeasured",
    ),
    "calibration-probe": (
        "empirical_observations\t0",
        "message\tCalibration requires at least one pair in which both routes are correct.",
    ),
    "study-audit": (
        "pairs\t6",
        "12\tA11-03\tA11-03-A\tproposed",
    ),
    "micro-study-audit": (
        "contract\tC-human-v2",
        "verdict\thuman_benefit_unobserved",
    ),
    "dimensional-transfer": (
        "problem\tarea\tstatus\trank\tnullity\tgroup\tuse",
        "summary\t3_cross_area_groups\t1_irreducible\tall_constructed_groups_certified",
    ),
    "network-condensation": (
        "problem\tarea\tstatus\tboundary\tinternal\tresponse\treconstruction",
        "summary\t3_cross_area_condensations\t2_refusals\tall_constructed_cases_certified",
    ),
    "network-ordering": (
        "strategy\tarea\torder\tfill_edges\talgebraic_updates\tcertificates",
        "summary\tfill_6_to_1\tupdates_19_to_5\tstructural_savings_only",
    ),
    "network-human-boundary": (
        "case\tclassification\tdelta\tcheaper_when\tspeed\tlearnability",
        "summary\t1_conditional\t1_always_direct\t0_human_observations",
    ),
    "network-study-audit": (
        "contract\tC-network-study-v1",
        "verdict\texpert_review_and_learner_execution_required",
    ),
    "network-admission-audit": (
        "contract\tC-network-admission-v1",
        "verdict\texpert_review_and_disjoint_recognition_cohort_required",
    ),
    "event-transfer": (
        "problem\tA15-01",
        "admission\talways_direct",
    ),
    "impact-transfer": (
        "problem\tregime\tcondition\treflected_speed\treflection_angle",
        "summary\t1_source_problem\t2_physical_regimes\timpulse_projection_certified",
    ),
    "path-transfer": (
        "construction\tconstructed",
        "A10-06\tobstruction\tno_scalar_potential_certificate",
    ),
    "harmonic-transfer": (
        "problem\toperation\tresult",
        "summary\t2_source_problems\tphase_preserved",
    ),
    "harmonic-product": (
        "problem\toperation\tresult",
        "summary\t2_source_problems\tdc_and_second_harmonic_certified",
    ),
    "composition-benchmark": (
        "problem\troot\tconsumer\tstatus\tparent",
        "summary\t2_typed_chains\tlineage_and_certificates_preserved",
    ),
    "routing-benchmark": (
        "problem\toperator\tstatus\tsource_status\tobstruction\tadmission",
        "summary\t10_constructed\t2_bounded_non_success",
    ),
}


class WorktableCommandTests(unittest.TestCase):
    def test_every_command_preserves_its_public_output_boundary(self):
        for command, (first, last) in COMMANDS.items():
            with self.subTest(command=command):
                completed = subprocess.run(
                    [sys.executable, "-m", "worktable", command],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertEqual(completed.stderr, "")
                lines = completed.stdout.splitlines()
                self.assertEqual(lines[0], first)
                self.assertEqual(lines[-1], last)


if __name__ == "__main__":
    unittest.main()

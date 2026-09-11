import unittest

from sympy import I, simplify, symbols

from occ.harmonic import (
    HarmonicObservable,
    HarmonicResponseRequest,
)
from occ.composition import (
    HarmonicProductStep,
    ProblemPipelineCard,
    compile_problem_pipeline,
)
from occ.routing import ProblemCard
from worktable.composition_cases import (
    build_a14_composition_card,
    build_a23_composition_card,
)
from worktable.harmonic_product_cases import run_a23_coil
from worktable.path_cases import run_path_transfer


class CompositionTests(unittest.TestCase):
    def test_a23_response_to_product_preserves_lineage_and_exact_torque(self):
        card = build_a23_composition_card()

        result = compile_problem_pipeline(card)

        expected = run_a23_coil().torque
        self.assertEqual(result.status, "constructed")
        self.assertEqual(result.root_result.status, "constructed")
        self.assertEqual(
            result.output_artifact.parents, (result.root_artifact.reference,)
        )
        self.assertEqual(result.output_artifact.problem_id, "A23-05")
        self.assertEqual(
            result.output_artifact.provenance, result.root_artifact.provenance
        )
        self.assertEqual(result.output_artifact.operation, "harmonic_product")
        self.assertEqual(
            simplify(result.output_artifact.payload.time_signal - expected.time_signal),
            0,
        )
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_a14_path_to_circuit_uses_the_same_composition_envelope(self):
        card = build_a14_composition_card()

        result = compile_problem_pipeline(card)

        expected = run_path_transfer().circuit
        self.assertEqual(result.status, "constructed")
        self.assertEqual(
            result.output_artifact.parents, (result.root_artifact.reference,)
        )
        self.assertEqual(result.output_artifact.problem_id, "A14-06")
        self.assertEqual(result.output_artifact.operation, "two_path_circuit")
        self.assertEqual(
            simplify(
                result.output_artifact.payload.terminal_voltage
                - expected.terminal_voltage
            ),
            0,
        )
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_failed_root_stops_before_the_downstream_operation(self):
        first, second = symbols("first second")
        omega, time = symbols("omega time", positive=True, real=True)
        root = ProblemCard(
            problem_id="failed-root",
            observable="first response",
            provenance="adversarial exact fixture",
            request=HarmonicResponseRequest(
                problem_id="failed-root",
                laws=(first + second - 1,),
                unknowns=(first, second),
                observables=(HarmonicObservable("first response", first),),
                angular_frequency=omega,
                time=time,
            ),
        )
        card = ProblemPipelineCard(
            root=root,
            output_observable="product",
            step=HarmonicProductStep(
                source_observable="first response",
                right_phasor=-I,
                angular_frequency=omega,
                time=time,
            ),
        )

        result = compile_problem_pipeline(card)

        self.assertEqual(result.status, "refused")
        self.assertEqual(
            result.obstruction.code,
            "upstream_underdetermined_phasor_response",
        )
        self.assertIsNone(result.root_artifact)
        self.assertIsNone(result.output_artifact)

    def test_incompatible_or_missing_ports_are_explicit_refusals(self):
        omega, time = symbols("omega time", positive=True, real=True)
        path_card = build_a14_composition_card()
        wrong_step = ProblemPipelineCard(
            root=path_card.root,
            output_observable="invalid product",
            step=HarmonicProductStep(
                source_observable="path work",
                right_phasor=1,
                angular_frequency=omega,
                time=time,
            ),
        )
        harmonic_card = build_a23_composition_card()
        missing_port = ProblemPipelineCard(
            root=harmonic_card.root,
            output_observable="invalid torque",
            step=HarmonicProductStep(
                source_observable="missing response",
                right_phasor=-I,
                angular_frequency=omega,
                time=time,
            ),
        )

        incompatible = compile_problem_pipeline(wrong_step)
        missing = compile_problem_pipeline(missing_port)

        self.assertEqual(incompatible.status, "refused")
        self.assertEqual(incompatible.obstruction.code, "incompatible_pipeline_step")
        self.assertEqual(missing.status, "refused")
        self.assertEqual(missing.obstruction.code, "missing_parent_observable")


if __name__ == "__main__":
    unittest.main()

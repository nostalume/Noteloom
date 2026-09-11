"""Cross-family typed composition bench from A617 pages 9 and 28."""

from __future__ import annotations

from dataclasses import dataclass

from sympy import I

from occ.composition import (
    HarmonicProductStep,
    ProblemPipelineCard,
    ProblemPipelineResult,
    TwoPathCircuitStep,
    compile_problem_pipeline,
)
from occ.routing import ProblemCard

from .harmonic_product_cases import build_a23_coil_case
from .path_cases import build_a14_case


@dataclass(frozen=True)
class CompositionBenchResult:
    harmonic: ProblemPipelineResult
    path: ProblemPipelineResult


def build_a23_composition_card() -> ProblemPipelineCard:
    case = build_a23_coil_case()
    return ProblemPipelineCard(
        root=ProblemCard(
            problem_id=case.problem_id,
            observable="induced current",
            provenance=case.provenance,
            request=case.request,
        ),
        output_observable="applied torque along the rotation direction",
        step=HarmonicProductStep(
            source_observable="induced current",
            right_phasor=-I,
            angular_frequency=case.angular_frequency,
            time=case.time,
            scale=case.flux_scale,
        ),
    )


def build_a14_composition_card() -> ProblemPipelineCard:
    case = build_a14_case()
    return ProblemPipelineCard(
        root=ProblemCard(
            problem_id=case.problem_id,
            observable="oriented path work and length",
            provenance=("A617 PDF page 28; induced field along arc and chord"),
            request=case.request,
        ),
        output_observable="two-path terminal voltage and branch current",
        step=TwoPathCircuitStep(
            first_path="minor arc",
            second_path="straight chord",
            resistance_per_length=case.parameters["rho"],
        ),
    )


def run_composition_bench() -> CompositionBenchResult:
    return CompositionBenchResult(
        harmonic=compile_problem_pipeline(build_a23_composition_card()),
        path=compile_problem_pipeline(build_a14_composition_card()),
    )


def command_composition_benchmark() -> None:
    result = run_composition_bench()
    print("problem\troot\tconsumer\tstatus\tparent")
    for problem_id, pipeline in (
        ("A23-05", result.harmonic),
        ("A14-06", result.path),
    ):
        output = pipeline.output_artifact
        parent = output.parents[0].artifact_id if output is not None else "-"
        operation = output.operation if output is not None else "-"
        print(
            f"{problem_id}\t{pipeline.root_result.operator}\t{operation}\t"
            f"{pipeline.status}\t{parent}"
        )
    print("summary\t2_typed_chains\tlineage_and_certificates_preserved")

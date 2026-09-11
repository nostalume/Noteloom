"""Typed one-successor composition of independently certified constructions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TypeAlias

from sympy import Expr, Symbol, sympify

from .harmonic import HarmonicResponseResult
from .harmonic_product import (
    HarmonicProductRequest,
    HarmonicProductResult,
    construct_harmonic_product,
)
from .impact import FrictionalImpactResult
from .path import (
    PathFunctionalResult,
    TwoPathCircuitResult,
    construct_two_path_circuit,
)
from .records import Certificate
from .routing import ProblemCard, RoutedProblemResult, compile_problem_card


@dataclass(frozen=True)
class HarmonicProductStep:
    source_observable: str
    right_phasor: Expr
    angular_frequency: Expr
    time: Symbol
    scale: Expr = sympify(1)

    def __post_init__(self) -> None:
        if not self.source_observable.strip():
            raise ValueError("A harmonic-product step requires a source observable.")
        right = sympify(self.right_phasor)
        omega = sympify(self.angular_frequency)
        scale = sympify(self.scale)
        if not isinstance(self.time, Symbol) or self.time.is_real is not True:
            raise TypeError("The pipeline time coordinate must be a real symbol.")
        if omega.is_positive is not True:
            raise ValueError("The pipeline angular frequency must be positive.")
        if scale.is_real is not True:
            raise ValueError("The pipeline physical scale must be real.")
        if self.time in (right.free_symbols | scale.free_symbols):
            raise ValueError("Downstream factor and scale must be time independent.")
        object.__setattr__(self, "right_phasor", right)
        object.__setattr__(self, "angular_frequency", omega)
        object.__setattr__(self, "scale", scale)


@dataclass(frozen=True)
class TwoPathCircuitStep:
    first_path: str
    second_path: str
    resistance_per_length: Expr

    def __post_init__(self) -> None:
        if not self.first_path.strip() or not self.second_path.strip():
            raise ValueError("A circuit step requires two named path ports.")
        if self.first_path == self.second_path:
            raise ValueError("A circuit step requires two distinct paths.")
        object.__setattr__(
            self, "resistance_per_length", sympify(self.resistance_per_length)
        )


PipelineStep: TypeAlias = HarmonicProductStep | TwoPathCircuitStep
ArtifactPayload: TypeAlias = (
    HarmonicResponseResult
    | PathFunctionalResult
    | HarmonicProductResult
    | TwoPathCircuitResult
    | FrictionalImpactResult
)


@dataclass(frozen=True)
class ArtifactReference:
    artifact_id: str
    problem_id: str
    observable: str
    operation: str


@dataclass(frozen=True)
class ConstructionArtifact:
    artifact_id: str
    problem_id: str
    observable: str
    provenance: tuple[str, ...]
    operation: str
    payload: ArtifactPayload
    certificates: tuple[Certificate, ...]
    parents: tuple[ArtifactReference, ...] = ()

    @property
    def reference(self) -> ArtifactReference:
        return ArtifactReference(
            self.artifact_id, self.problem_id, self.observable, self.operation
        )


@dataclass(frozen=True)
class ProblemPipelineCard:
    root: ProblemCard
    output_observable: str
    step: PipelineStep

    def __post_init__(self) -> None:
        if not isinstance(self.root, ProblemCard):
            raise TypeError("A problem pipeline requires one admitted root card.")
        if not self.output_observable.strip():
            raise ValueError("A problem pipeline requires an output observable.")
        if not isinstance(self.step, (HarmonicProductStep, TwoPathCircuitStep)):
            raise TypeError("The problem pipeline contains an unsupported step.")


@dataclass(frozen=True)
class PipelineObstruction:
    code: str
    message: str
    next_action: str = ""


@dataclass(frozen=True)
class ProblemPipelineResult:
    status: str
    card: ProblemPipelineCard
    root_result: RoutedProblemResult
    root_artifact: Optional[ConstructionArtifact] = None
    output_artifact: Optional[ConstructionArtifact] = None
    certificates: tuple[Certificate, ...] = ()
    obstruction: Optional[PipelineObstruction] = None


def _refused(
    card: ProblemPipelineCard,
    root_result: RoutedProblemResult,
    code: str,
    message: str,
    *,
    root_artifact: Optional[ConstructionArtifact] = None,
    next_action: str = "",
) -> ProblemPipelineResult:
    return ProblemPipelineResult(
        status="refused",
        card=card,
        root_result=root_result,
        root_artifact=root_artifact,
        obstruction=PipelineObstruction(code, message, next_action),
    )


def _root_artifact(
    card: ProblemPipelineCard, result: RoutedProblemResult
) -> ConstructionArtifact:
    return ConstructionArtifact(
        artifact_id=f"{card.root.problem_id}:root:{result.operator}",
        problem_id=card.root.problem_id,
        observable=card.root.observable,
        provenance=(card.root.provenance,),
        operation=result.operator,
        payload=result.construction,
        certificates=result.certificates,
    )


def _finish(
    card: ProblemPipelineCard,
    root_result: RoutedProblemResult,
    root: ConstructionArtifact,
    operation: str,
    payload: HarmonicProductResult | TwoPathCircuitResult,
) -> ProblemPipelineResult:
    lineage = Certificate(
        "composition_parent_preserved",
        True,
        f"Output consumes exactly parent artifact {root.artifact_id}.",
    )
    certificates = root.certificates + payload.certificates + (lineage,)
    output = ConstructionArtifact(
        artifact_id=f"{card.root.problem_id}:output:{operation}",
        problem_id=card.root.problem_id,
        observable=card.output_observable,
        provenance=root.provenance,
        operation=operation,
        payload=payload,
        certificates=certificates,
        parents=(root.reference,),
    )
    return ProblemPipelineResult(
        status="constructed",
        card=card,
        root_result=root_result,
        root_artifact=root,
        output_artifact=output,
        certificates=certificates,
    )


def compile_problem_pipeline(card: ProblemPipelineCard) -> ProblemPipelineResult:
    """Run one routed construction followed by one compatible typed consumer."""

    root_result = compile_problem_card(card.root)
    if root_result.status != "constructed":
        obstruction = root_result.obstruction
        code = "upstream_construction_failed"
        message = "The root construction did not produce a composable artifact."
        next_action = "Inspect the root semantic request and its obstruction."
        if obstruction is not None:
            code = f"upstream_{obstruction.code}"
            message = obstruction.message
            next_action = obstruction.next_action
        return _refused(card, root_result, code, message, next_action=next_action)
    root = _root_artifact(card, root_result)
    if not all(certificate.passed for certificate in root.certificates):
        return _refused(
            card,
            root_result,
            "upstream_certificate_failed",
            "A constructed root carries a failed certificate.",
            root_artifact=root,
            next_action="Repair the root construction before composition.",
        )

    match root.payload, card.step:
        case HarmonicResponseResult() as response, HarmonicProductStep() as step:
            sources = tuple(
                observable
                for observable in response.observables
                if observable.name == step.source_observable
            )
            if len(sources) != 1:
                return _refused(
                    card,
                    root_result,
                    "missing_parent_observable",
                    f"Root response has no unique observable {step.source_observable!r}.",
                    root_artifact=root,
                    next_action="Use one named observable generated by the root response.",
                )
            product = construct_harmonic_product(
                HarmonicProductRequest(
                    problem_id=card.root.problem_id,
                    product_name=card.output_observable,
                    left_phasor=sources[0].phasor,
                    right_phasor=step.right_phasor,
                    angular_frequency=step.angular_frequency,
                    time=step.time,
                    scale=step.scale,
                )
            )
            if product.status != "constructed":
                return _refused(
                    card,
                    root_result,
                    f"downstream_{product.obstruction.code}",
                    product.obstruction.message,
                    root_artifact=root,
                    next_action=product.obstruction.next_action,
                )
            return _finish(card, root_result, root, "harmonic_product", product)
        case PathFunctionalResult() as paths, TwoPathCircuitStep() as step:
            try:
                circuit = construct_two_path_circuit(
                    paths,
                    step.first_path,
                    step.second_path,
                    step.resistance_per_length,
                )
            except KeyError as error:
                return _refused(
                    card,
                    root_result,
                    "missing_parent_path",
                    f"Root path result has no path {error.args[0]!r}.",
                    root_artifact=root,
                    next_action="Use two path names generated by the root construction.",
                )
            if circuit.status != "constructed":
                return _refused(
                    card,
                    root_result,
                    f"downstream_{circuit.obstruction.code}",
                    circuit.obstruction.message,
                    root_artifact=root,
                )
            return _finish(card, root_result, root, "two_path_circuit", circuit)
        case _:
            return _refused(
                card,
                root_result,
                "incompatible_pipeline_step",
                "The downstream step cannot consume the routed root payload.",
                root_artifact=root,
                next_action="Choose a step whose input type matches the root operation.",
            )

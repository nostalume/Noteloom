"""One typed entry point for the bounded observable-relation operators."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TypeAlias

from .adaptive import (
    AdaptiveConstructionResult,
    AdaptiveRelationRequest,
    construct_target_relation,
)
from .cost import AdmissionBoundary, HandwrittenRoute, construct_admission_boundary
from .event import EventConstructionResult, EventProblem, construct_event
from .harmonic import (
    HarmonicResponseRequest,
    HarmonicResponseResult,
    construct_harmonic_response,
)
from .impact import (
    FrictionalImpactRequest,
    FrictionalImpactResult,
    construct_frictional_impact,
)
from .linear import construct_observable_closure
from .path import (
    PathFunctionalRequest,
    PathFunctionalResult,
    construct_path_functionals,
)
from .records import Certificate, ClosureResult, Matrix, Vector
from .semantic import (
    PhysicalRelationPacket,
    SemanticCompilationResult,
    compile_single_source_functional,
)


@dataclass(frozen=True)
class FunctionalRelationRequest:
    """A physical functional packet and its extraction resource bound."""

    packet: PhysicalRelationPacket
    max_fields: Optional[int] = None

    def __post_init__(self) -> None:
        if not isinstance(self.packet, PhysicalRelationPacket):
            raise TypeError("packet must be a PhysicalRelationPacket.")
        if self.max_fields is not None and (
            not isinstance(self.max_fields, int)
            or isinstance(self.max_fields, bool)
            or self.max_fields < 1
        ):
            raise ValueError("max_fields must be a positive integer or None.")


@dataclass(frozen=True)
class LinearDynamicsRequest:
    """Finite rational second-order dynamics and one requested observable."""

    restoring_map: Matrix
    observable: Vector
    max_dimension: Optional[int] = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "restoring_map",
            tuple(tuple(row) for row in self.restoring_map),
        )
        object.__setattr__(self, "observable", tuple(self.observable))


@dataclass(frozen=True)
class RouteAlternatives:
    """Independently authored same-observable handwritten routes."""

    direct: HandwrittenRoute
    proposed: HandwrittenRoute


ProblemRequest: TypeAlias = (
    AdaptiveRelationRequest
    | FunctionalRelationRequest
    | LinearDynamicsRequest
    | HarmonicResponseRequest
    | FrictionalImpactRequest
    | EventProblem
    | PathFunctionalRequest
)

ProblemConstruction: TypeAlias = (
    AdaptiveConstructionResult
    | SemanticCompilationResult
    | ClosureResult
    | HarmonicResponseResult
    | FrictionalImpactResult
    | EventConstructionResult
    | PathFunctionalResult
)


@dataclass(frozen=True)
class ProblemCard:
    """A human-validated semantic request with physical identity and provenance."""

    problem_id: str
    observable: str
    provenance: str
    request: ProblemRequest
    routes: Optional[RouteAlternatives] = None

    def __post_init__(self) -> None:
        if not self.problem_id.strip():
            raise ValueError("A problem card requires a problem id.")
        if not self.observable.strip():
            raise ValueError("A problem card requires an observable.")
        if not self.provenance.strip():
            raise ValueError("A problem card requires provenance.")
        admitted = (
            AdaptiveRelationRequest,
            FunctionalRelationRequest,
            LinearDynamicsRequest,
            HarmonicResponseRequest,
            FrictionalImpactRequest,
            EventProblem,
            PathFunctionalRequest,
        )
        if not isinstance(self.request, admitted):
            raise TypeError("The problem card contains an unsupported request type.")
        if isinstance(
            self.request,
            (
                AdaptiveRelationRequest,
                EventProblem,
                HarmonicResponseRequest,
                FrictionalImpactRequest,
            ),
        ):
            if self.request.problem_id != self.problem_id:
                raise ValueError(
                    "The card and semantic request problem ids must match."
                )
        if self.routes is not None:
            route_ids = (self.routes.direct.problem_id, self.routes.proposed.problem_id)
            if any(problem_id != self.problem_id for problem_id in route_ids):
                raise ValueError(
                    "Every handwritten route must match the problem card id."
                )
            route_targets = (self.routes.direct.target, self.routes.proposed.target)
            if any(target != self.observable for target in route_targets):
                raise ValueError(
                    "Every handwritten route must compute the card observable."
                )


@dataclass(frozen=True)
class RoutingObstruction:
    operator: str
    code: str
    message: str
    next_action: str = ""


@dataclass(frozen=True)
class RoutedProblemResult:
    status: str
    card: ProblemCard
    operator: str
    selection_witness: str
    source_status: str
    construction: ProblemConstruction
    certificates: tuple[Certificate, ...] = ()
    admission: Optional[AdmissionBoundary] = None
    obstruction: Optional[RoutingObstruction] = None


def _admission(card: ProblemCard) -> Optional[AdmissionBoundary]:
    if card.routes is None:
        return None
    return construct_admission_boundary(card.routes.direct, card.routes.proposed)


def _routed_result(
    card: ProblemCard,
    *,
    operator: str,
    selection_witness: str,
    success_status: str,
    construction: ProblemConstruction,
    certificates: tuple[Certificate, ...],
) -> RoutedProblemResult:
    source_status = construction.status
    if source_status == success_status:
        return RoutedProblemResult(
            status="constructed",
            card=card,
            operator=operator,
            selection_witness=selection_witness,
            source_status=source_status,
            construction=construction,
            certificates=certificates,
            admission=_admission(card),
        )
    obstruction = construction.obstruction
    if obstruction is None:
        raise RuntimeError(f"{operator} lost its obstruction.")
    status = "ambiguous" if "ambiguous" in obstruction.code else "refused"
    return RoutedProblemResult(
        status=status,
        card=card,
        operator=operator,
        selection_witness=selection_witness,
        source_status=source_status,
        construction=construction,
        certificates=certificates,
        obstruction=RoutingObstruction(
            operator,
            obstruction.code,
            obstruction.message,
            getattr(obstruction, "next_action", ""),
        ),
    )


def _compile_adaptive(
    card: ProblemCard, request: AdaptiveRelationRequest
) -> RoutedProblemResult:
    construction = construct_target_relation(request)
    if construction.status == "constructed" and construction.elimination is not None:
        free_symbols = set().union(
            *(law.relation.free_symbols for law in construction.selected_laws)
        )
        hidden = free_symbols - set(request.givens) - {request.target}
        direct = len(construction.selected_laws) == 1 and not hidden
        operator = "direct_relation" if direct else "polynomial_relation"
        witness = (
            "The smallest constraining packet has one law and no hidden quantity."
            if direct
            else "The smallest constraining packet requires exact hidden-variable projection."
        )
        return _routed_result(
            card,
            operator=operator,
            selection_witness=witness,
            success_status="constructed",
            construction=construction,
            certificates=construction.elimination.certificates,
        )
    return _routed_result(
        card,
        operator="relation_projection",
        selection_witness="The card supplies an unordered exact relation bag.",
        success_status="constructed",
        construction=construction,
        certificates=(),
    )


def compile_problem_card(card: ProblemCard) -> RoutedProblemResult:
    """Select one existing semantic operator and preserve its evidence boundary."""

    match card.request:
        case AdaptiveRelationRequest() as request:
            return _compile_adaptive(card, request)
        case FunctionalRelationRequest(packet=packet, max_fields=max_fields):
            construction = compile_single_source_functional(
                packet, max_fields=max_fields
            )
            operator = "source_functional"
            witness = "The card supplies one source-to-field functional packet."
            success_status = "compiled"
        case LinearDynamicsRequest(
            restoring_map=restoring_map,
            observable=observable,
            max_dimension=max_dimension,
        ):
            construction = construct_observable_closure(
                restoring_map, observable, max_dimension=max_dimension
            )
            operator = "linear_closure"
            witness = "The card supplies repeated finite linear dynamics."
            success_status = "closed"
        case EventProblem() as request:
            construction = construct_event(request)
            operator = "event_relation"
            witness = "The card supplies a zero-event predicate and physical domain."
            success_status = "constructed"
        case HarmonicResponseRequest() as request:
            construction = construct_harmonic_response(request)
            operator = "harmonic_response"
            witness = "The card supplies exact finite linear phasor laws."
            success_status = "constructed"
        case FrictionalImpactRequest() as request:
            construction = construct_frictional_impact(request)
            operator = "frictional_impact"
            witness = "The card supplies restitution and a bounded Coulomb impulse."
            success_status = "constructed"
        case PathFunctionalRequest() as request:
            construction = construct_path_functionals(request)
            operator = "path_functional"
            witness = "The card supplies an oriented path-dependent observable."
            success_status = "constructed"
        case _:
            raise RuntimeError("ProblemCard admission and routing variants diverged.")
    return _routed_result(
        card,
        operator=operator,
        selection_witness=witness,
        success_status=success_status,
        construction=construction,
        certificates=construction.certificates,
    )

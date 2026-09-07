"""Plan and lazily materialize finite natural-tensor defect routes."""

from __future__ import annotations

from dataclasses import dataclass

import tensor_seed_compression as seed
from linear_defect_compiler import CandidateBracket, DefectBlock, DefectBudget, LinearMap
from tensor_seed_compression import CovariantTensor, Matrix

METRIC_SEED_CAPABILITY = "nondegenerate-symmetric-bilinear-form"


@dataclass(frozen=True)
class RelationFact:
    name: str
    rank: int
    permutation_generator_count: int
    capabilities: tuple[str, ...]
    certificate: str | None


@dataclass(frozen=True)
class PlanOperation:
    rule: str
    source: str | None = None
    target_dimension: int | None = None


@dataclass(frozen=True)
class TargetBlueprint:
    tensor: CovariantTensor
    mode: str
    dimension: int


@dataclass(frozen=True)
class TensorRoutePlan:
    route: str
    outcome: str
    candidate_kind: str = ""
    candidate_dimension: int = 0
    seed_tensor: CovariantTensor | None = None
    targets: tuple[TargetBlueprint, ...] = ()
    operations: tuple[PlanOperation, ...] = ()
    certificates: tuple[str, ...] = ()
    estimated_cost: int | None = None
    planning_cost: int = 0
    estimated_total_cost: int | None = None
    obstruction_kind: str | None = None
    obstruction_reason: str | None = None


@dataclass(frozen=True)
class RelationPlanning:
    facts: tuple[RelationFact, ...]
    routes: tuple[TensorRoutePlan, ...]
    preferred_route: str


@dataclass(frozen=True)
class RouteAdmission:
    outcome: str
    obstruction_kind: str | None = None
    obstruction_reason: str | None = None


@dataclass(frozen=True)
class MaterializedRoute:
    candidate_labels: tuple[str, ...]
    candidates: tuple[Matrix, ...]
    blocks: tuple[DefectBlock, ...]
    visible_action: LinearMap
    bracket: CandidateBracket


def _bracket_bound(candidate_dimension: int) -> int:
    return candidate_dimension**3 + 3 * candidate_dimension**2


def _compiler_cost(candidate_dimension: int, dimensions: tuple[int, ...]) -> int:
    return candidate_dimension * sum(dimensions) + _bracket_bound(candidate_dimension)


def _final_operations() -> tuple[PlanOperation, ...]:
    return tuple(
        PlanOperation(rule)
        for rule in ("simultaneous-defect-kernel", "visible-quotient", "bracket-closure")
    )


def _raw_plan(tensors: tuple[CovariantTensor, ...]) -> TensorRoutePlan:
    dimension = tensors[0].dimension
    targets = tuple(TargetBlueprint(tensor, "raw", dimension**tensor.rank) for tensor in tensors)
    dimensions = tuple(target.dimension for target in targets)
    cost = _compiler_cost(dimension**2, dimensions)
    return TensorRoutePlan(
        route="natural-tensor-raw-endomorphism",
        outcome="planned",
        candidate_kind="endomorphism",
        candidate_dimension=dimension**2,
        targets=targets,
        operations=(
            PlanOperation("raw-endomorphism-seed"),
            *(
                PlanOperation("full-tensor-targets", target.tensor.name, target.dimension)
                for target in targets
            ),
            *_final_operations(),
        ),
        certificates=("endomorphism-seed-complete", "full-coordinate-targets-complete"),
        estimated_cost=cost,
        planning_cost=sum(dimensions),
        estimated_total_cost=cost + sum(dimensions),
    )


def _reject(kind: str, reason: str) -> TensorRoutePlan:
    return TensorRoutePlan(
        route="natural-tensor-structured-seed",
        outcome="rejected",
        obstruction_kind=kind,
        obstruction_reason=reason,
    )


def _structured_plan(tensors: tuple[CovariantTensor, ...]) -> TensorRoutePlan:
    sources = tuple(t for t in tensors if METRIC_SEED_CAPABILITY in t.capabilities)
    if not sources:
        return _reject("MissingSeedRelation", f"no tensor certifies {METRIC_SEED_CAPABILITY}")
    if len(sources) > 1:
        return _reject(
            "AmbiguousSeedRelation", f"{len(sources)} tensors certify {METRIC_SEED_CAPABILITY}"
        )
    source = sources[0]
    if source.rank != 2 or source.relation_certificate is None:
        return _reject("UncertifiedSeedRelation", "the metric seed relation is not certified")
    remaining = tuple(tensor for tensor in tensors if tensor is not source)
    missing = next((tensor for tensor in remaining if tensor.quotient is None), None)
    if missing is not None:
        return _reject(
            "MissingQuotientConstructor",
            f"tensor {missing.name!r} has no compositional quotient expression",
        )
    if any(tensor.relation_certificate is None for tensor in remaining):
        return _reject("UndeclaredPermutationSymmetry", "a quotient relation lacks a certificate")
    targets = tuple(
        TargetBlueprint(
            tensor,
            "quotient",
            seed.quotient_dimension(tensor.quotient, tensor.dimension),
        )
        for tensor in remaining
        if tensor.quotient is not None
    )
    candidate_dimension = source.dimension * (source.dimension - 1) // 2
    dimensions = tuple(target.dimension for target in targets)
    cost = _compiler_cost(candidate_dimension, dimensions)
    return TensorRoutePlan(
        route="natural-tensor-structured-seed",
        outcome="planned",
        candidate_kind="metric-kernel",
        candidate_dimension=candidate_dimension,
        seed_tensor=source,
        targets=targets,
        operations=(
            PlanOperation("metric-kernel", source.name, candidate_dimension),
            *(
                PlanOperation("compositional-quotient", target.tensor.name, target.dimension)
                for target in targets
            ),
            *_final_operations(),
        ),
        certificates=(
            f"metric-kernel-complete:{source.name}",
            *(f"compositional-quotient-complete:{target.tensor.name}" for target in targets),
        ),
        estimated_cost=cost,
        planning_cost=sum(dimensions),
        estimated_total_cost=cost + sum(dimensions),
    )


def plan_tensor_relations(tensors: tuple[CovariantTensor, ...]) -> RelationPlanning:
    if not tensors:
        raise ValueError("at least one tensor relation is required")
    dimension = tensors[0].dimension
    if dimension < 2 or any(tensor.dimension != dimension for tensor in tensors):
        raise ValueError("tensor relations require one common carrier of dimension at least two")
    facts = tuple(
        RelationFact(
            tensor.name,
            tensor.rank,
            len(tensor.permutation_generators),
            tuple(sorted(tensor.capabilities)),
            tensor.relation_certificate,
        )
        for tensor in tensors
    )
    routes = (_raw_plan(tensors), _structured_plan(tensors))
    planned = tuple(route for route in routes if route.outcome == "planned")
    preferred = min(planned, key=lambda route: route.estimated_total_cost or 10**30)
    return RelationPlanning(facts, routes, preferred.route)


def admit_route(route: TensorRoutePlan, budget: DefectBudget) -> RouteAdmission:
    checks = (
        (route.candidate_dimension, budget.maximum_candidate_dimension, "CandidateBudgetExceeded"),
        (
            sum(target.dimension for target in route.targets),
            budget.maximum_residual_coordinates,
            "ResidualBudgetExceeded",
        ),
        (
            _bracket_bound(route.candidate_dimension),
            budget.maximum_bracket_checks,
            "BracketBudgetExceeded",
        ),
    )
    for required, available, kind in checks:
        if required > available:
            return RouteAdmission(
                "unresolved", kind, f"required {required} exceeds budget {available}"
            )
    return RouteAdmission("admitted")


def _tensor_matrix(tensor: CovariantTensor) -> Matrix:
    return tuple(
        tuple(tensor.value((row, column)) for column in range(tensor.dimension))
        for row in range(tensor.dimension)
    )


def materialize_route(route: TensorRoutePlan) -> MaterializedRoute:
    if route.outcome != "planned":
        raise ValueError("only a planned route can be materialized")
    carrier = route.targets[0].tensor if route.targets else route.seed_tensor
    if carrier is None:
        raise ValueError("route has no carrier")
    dimension = carrier.dimension
    if route.candidate_kind == "endomorphism":
        candidates = seed.endomorphism_candidates(dimension)
        labels = seed.endomorphism_candidate_labels(dimension)
        bracket = seed.endomorphism_bracket(dimension)
    elif route.candidate_kind == "metric-kernel" and route.seed_tensor is not None:
        metric = _tensor_matrix(route.seed_tensor)
        labels, candidates = seed.metric_candidates(metric)
        bracket = seed.metric_bracket(metric, candidates)
    else:
        raise ValueError("unsupported candidate blueprint")
    blocks = tuple(
        seed.tensor_defect(
            target.tensor,
            candidates,
            seed.raw_targets(target.tensor)
            if target.mode == "raw"
            else seed.quotient_coordinates(target.tensor.quotient, target.tensor.dimension),
        )
        for target in route.targets
    )
    return MaterializedRoute(labels, candidates, blocks, seed.standard_action(candidates), bracket)


def quotient_audit(route: TensorRoutePlan) -> tuple[bool, int]:
    checks = 0
    for target in route.targets:
        if target.mode != "quotient" or target.tensor.quotient is None:
            continue
        quotient = seed.quotient_coordinates(target.tensor.quotient, target.tensor.dimension)
        orbit = seed.structured_targets(target.tensor)
        if quotient != orbit:
            return False, checks
        checks += target.tensor.dimension**target.tensor.rank * len(
            seed.permutation_group(target.tensor.rank, target.tensor.permutation_generators)
        )
    return True, checks


def planning_json(
    planning: RelationPlanning,
    selected_route: str | None,
    execution_policy: str,
    admissions: dict[str, RouteAdmission],
    materialized_routes: tuple[str, ...],
) -> dict[str, object]:
    selected = next((route for route in planning.routes if route.route == selected_route), None)
    return {
        "execution_policy": execution_policy,
        "preferred_route": planning.preferred_route,
        "selected_route": selected_route,
        "materialized_routes": list(materialized_routes),
        "facts": [
            {
                "name": fact.name,
                "rank": fact.rank,
                "permutation_generator_count": fact.permutation_generator_count,
                "capabilities": list(fact.capabilities),
                "certificate": fact.certificate,
            }
            for fact in planning.facts
        ],
        "routes": [
            {
                "route": route.route,
                "outcome": route.outcome,
                "candidate_dimension": route.candidate_dimension,
                "target_dimensions": [target.dimension for target in route.targets],
                "estimated_cost": route.estimated_cost,
                "planning_cost": route.planning_cost,
                "estimated_total_cost": route.estimated_total_cost,
                "admission": admissions.get(route.route, RouteAdmission(route.outcome)).outcome,
                "obstruction": None
                if route.outcome == "planned"
                else {"kind": route.obstruction_kind, "reason": route.obstruction_reason},
            }
            for route in planning.routes
        ],
        "selected_operations": [
            {
                "rule": operation.rule,
                "source": operation.source,
                "target_dimension": operation.target_dimension,
            }
            for operation in (() if selected is None else selected.operations)
        ],
    }

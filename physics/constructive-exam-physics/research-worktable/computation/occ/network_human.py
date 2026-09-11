"""Deductive human-cost boundary for sparse network elimination."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .cost import (
    AdmissionBoundary,
    ExamAction,
    HandwrittenRoute,
    RouteComparison,
    compare_exam_routes,
    construct_admission_boundary,
)
from .network import LinearNetworkRequest
from .network_order import (
    NetworkEliminationPlan,
    NetworkPlanningObstruction,
    plan_network_elimination,
)
from .records import Certificate


REQUIRED_NETWORK_HUMAN_EVIDENCE = (
    "independent_route_key_review",
    "matched_correct_execution",
    "participant_clustered_timing",
    "delayed_retention",
    "unseen_topology_transfer",
)

SPEED_DISPOSITIONS = {
    "conditional": "conditional_weights_unmeasured",
    "always_proposed": "structural_model_favors_sparse",
    "always_direct": "structural_model_favors_declared",
    "equivalent": "structural_model_tie",
}


@dataclass(frozen=True)
class NetworkHumanBoundaryResult:
    status: str
    problem_id: str
    target: str
    declared_route: Optional[HandwrittenRoute] = None
    sparse_route: Optional[HandwrittenRoute] = None
    comparison: Optional[RouteComparison] = None
    admission_boundary: Optional[AdmissionBoundary] = None
    fill_delta: Optional[int] = None
    speed_disposition: str = "not_applicable"
    learnability_disposition: str = "not_applicable"
    required_evidence: tuple[str, ...] = REQUIRED_NETWORK_HUMAN_EVIDENCE
    certificates: tuple[Certificate, ...] = ()
    obstruction: Optional[NetworkPlanningObstruction] = None
    provenance: str = ""


def _route_from_plan(
    request: LinearNetworkRequest,
    plan: NetworkEliminationPlan,
    *,
    problem_id: str,
    target: str,
    charge_order_selection: bool,
) -> HandwrittenRoute:
    actions = [
        ExamAction(
            "relation",
            "write the admitted reciprocal boundary/internal balance",
            live_relations=len(request.variables),
        )
    ]
    for index, step in enumerate(plan.steps):
        live = len(request.variables) - index
        if charge_order_selection:
            actions.append(
                ExamAction(
                    "representation",
                    f"inspect current fill before eliminating {step.eliminated_symbol}",
                    live_relations=live,
                )
            )
        if step.algebraic_updates:
            subjects = tuple(
                f"{step.eliminated_symbol}:local-update:{index}"
                for index in range(1, step.algebraic_updates + 1)
            )
            actions.append(
                ExamAction(
                    "symbolic",
                    f"apply local elimination of {step.eliminated_symbol}",
                    live_relations=live,
                    symbolic_subjects=subjects,
                )
            )
    actions.append(
        ExamAction(
            "return",
            "check the boundary law and reverse only requested hidden states",
            live_relations=len(request.boundary_symbols),
        )
    )
    names_by_symbol = {
        variable.symbol: variable.physical_name for variable in request.variables
    }
    hidden = tuple(
        f"{names_by_symbol[symbol]} ({symbol})" for symbol in plan.internal_symbols
    )
    return HandwrittenRoute(
        problem_id=problem_id,
        target=target,
        hidden_quantities=hidden,
        actions=tuple(actions),
    )


def _symbolic_units(route: HandwrittenRoute) -> int:
    return sum(
        action.atomic_units for action in route.actions if action.kind == "symbolic"
    )


def construct_network_human_boundary(
    request: LinearNetworkRequest,
    *,
    problem_id: str,
    target: str,
    max_steps: int = 8,
) -> NetworkHumanBoundaryResult:
    """Construct a model-relative speed region without promoting a human claim."""

    if not problem_id.strip():
        raise ValueError("problem_id must be nonempty.")
    if not target.strip():
        raise ValueError("target must be nonempty.")
    declared = plan_network_elimination(
        request, strategy="declared", max_steps=max_steps
    )
    sparse = plan_network_elimination(request, strategy="min_fill", max_steps=max_steps)
    for plan in (declared, sparse):
        if plan.status != "constructed":
            return NetworkHumanBoundaryResult(
                status="refused",
                problem_id=problem_id,
                target=target,
                obstruction=plan.obstruction,
                provenance=request.provenance,
            )

    declared_route = _route_from_plan(
        request,
        declared,
        problem_id=problem_id,
        target=target,
        charge_order_selection=False,
    )
    sparse_route = _route_from_plan(
        request,
        sparse,
        problem_id=problem_id,
        target=target,
        charge_order_selection=True,
    )
    comparison = compare_exam_routes(declared_route, sparse_route)
    boundary = construct_admission_boundary(declared_route, sparse_route)
    certificates = (
        Certificate(
            name="same_observable_boundary",
            passed=declared.condensed_matrix == sparse.condensed_matrix
            and declared.condensed_source == sparse.condensed_source,
            witness="declared and sparse routes return the same boundary relation",
        ),
        Certificate(
            name="atomic_update_accounting",
            passed=_symbolic_units(declared_route) == declared.total_algebraic_updates
            and _symbolic_units(sparse_route) == sparse.total_algebraic_updates,
            witness="route symbolic units equal generated nonzero local updates",
        ),
        Certificate(
            name="recognition_debt_exposed",
            passed=sparse_route.cost.representation_changes == len(sparse.steps),
            witness="each greedy pivot decision contributes one visible setup unit",
        ),
        Certificate(
            name="cost_boundary_reproducible",
            passed=boundary.baseline == declared_route
            and boundary.proposed == sparse_route,
            witness="the speed region is derived from the two returned action ledgers",
        ),
    )
    if not all(certificate.passed for certificate in certificates):
        return NetworkHumanBoundaryResult(
            status="refused",
            problem_id=problem_id,
            target=target,
            obstruction=NetworkPlanningObstruction(
                "certificate_failed",
                "The human-cost boundary failed an accounting or equality certificate.",
            ),
            provenance=request.provenance,
        )
    return NetworkHumanBoundaryResult(
        status="constructed",
        problem_id=problem_id,
        target=target,
        declared_route=declared_route,
        sparse_route=sparse_route,
        comparison=comparison,
        admission_boundary=boundary,
        fill_delta=sparse.total_fill_edges - declared.total_fill_edges,
        speed_disposition=SPEED_DISPOSITIONS[boundary.classification],
        learnability_disposition="human_observations_required",
        certificates=certificates,
        provenance=request.provenance,
    )

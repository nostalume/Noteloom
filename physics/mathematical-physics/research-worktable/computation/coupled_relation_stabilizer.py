"""Public adapter for exact coupled-carrier covariance construction."""

from __future__ import annotations

from pathlib import Path

import exact_gaussian_matrix as gaussian
from adjoint_algebra import Matrix as RealMatrix
from adjoint_algebra import inverse as real_inverse
from adjoint_algebra import transpose as real_transpose
from coupled_covariance_core import (
    CoupledPlan,
    admission_refusal,
    clifford_checks,
    combine_pair,
    construct,
    plan,
    serialize_pair,
    symbol_projectors,
)
from linear_defect_compiler import DefectBudget
from problem_input import ProblemDocument, ProblemInputError, load_problem

ROUTE = "coupled-relation-kernel"
CAPABILITY = "metric-clifford-link"


class CoupledRelationObstruction(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


def _real_matrix(value: object, name: str) -> RealMatrix:
    if not isinstance(value, list) or not value or any(not isinstance(row, list) for row in value):
        raise CoupledRelationObstruction("InvalidRelationInput", f"{name} must be a square matrix")
    dimension = len(value)
    if any(len(row) != dimension for row in value):
        raise CoupledRelationObstruction("InvalidRelationInput", f"{name} must be a square matrix")
    try:
        return tuple(tuple(gaussian.rational(entry) for entry in row) for row in value)
    except (ValueError, ZeroDivisionError) as error:
        raise CoupledRelationObstruction("InvalidExactInput", str(error)) from error


def _budget(payload: dict[str, object]) -> DefectBudget:
    value = payload.get("resource_budget")
    if not isinstance(value, dict):
        raise CoupledRelationObstruction(
            "MissingResourceBudget", "resource_budget must be an object"
        )
    try:
        return DefectBudget(
            int(value["maximum_candidate_dimension"]),
            int(value["maximum_residual_coordinates"]),
            int(value["maximum_bracket_checks"]),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise CoupledRelationObstruction(
            "InvalidResourceBudget", "resource_budget requires three integer bounds"
        ) from error


def _parse(
    payload: dict[str, object],
) -> tuple[
    RealMatrix,
    tuple[gaussian.ComplexMatrix, ...],
    tuple[str, ...],
    DefectBudget,
]:
    metric = _real_matrix(payload.get("base_metric"), "base_metric")
    if metric != real_transpose(metric):
        raise CoupledRelationObstruction("MetricRelationViolation", "base_metric is not symmetric")
    try:
        real_inverse(metric)
    except ValueError as error:
        raise CoupledRelationObstruction(
            "MetricRelationViolation", "base_metric is degenerate"
        ) from error
    raw_links = payload.get("link_matrices")
    if not isinstance(raw_links, list) or len(raw_links) != len(metric):
        raise CoupledRelationObstruction(
            "InvalidRelationInput", "link_matrices must contain one matrix per base dimension"
        )
    try:
        links = tuple(
            gaussian.matrix(value, f"link_matrices[{index}]")
            for index, value in enumerate(raw_links)
        )
    except (ValueError, ZeroDivisionError) as error:
        raise CoupledRelationObstruction("InvalidExactInput", str(error)) from error
    fiber_dimension = len(links[0])
    if any(len(link) != fiber_dimension for link in links):
        raise CoupledRelationObstruction(
            "InvalidRelationInput", "all link matrices must have one common fiber dimension"
        )
    if any(not gaussian.is_hermitian(link) for link in links):
        raise CoupledRelationObstruction(
            "HermitianRelationViolation", "every link matrix must be Hermitian"
        )
    raw_capabilities = payload.get("required_capabilities", [])
    if not isinstance(raw_capabilities, list) or any(
        not isinstance(item, str) for item in raw_capabilities
    ):
        raise CoupledRelationObstruction(
            "InvalidRelationInput", "required_capabilities must be a list of strings"
        )
    capabilities = tuple(raw_capabilities)
    unsupported = tuple(item for item in capabilities if item != CAPABILITY)
    if unsupported:
        raise CoupledRelationObstruction(
            "UnsupportedRelationCapability", f"unsupported capabilities: {', '.join(unsupported)}"
        )
    return metric, links, capabilities, _budget(payload)


def _planning(value: CoupledPlan, *, materialized: bool) -> dict[str, object]:
    return {
        "policy": "symbolic-admission-before-materialization",
        "candidate_dimension": value.candidate_dimension,
        "residual_dimension": value.residual_dimension,
        "bracket_upper_bound": value.bracket_upper_bound,
        "materialized": materialized,
    }


def _failure(
    outcome: str, kind: str, reason: str, value: CoupledPlan | None = None
) -> dict[str, object]:
    return {
        "schema": "reduction-decision/v1",
        "outcome": outcome,
        "request": {"problem_type": "coupled-carrier-covariance/v1"},
        "planning": None if value is None else _planning(value, materialized=False),
        "probes": [{"route": ROUTE, "outcome": outcome, "first_residual": kind}],
        "candidates": [],
        "coincidence": None,
        "decision": {"selected_route": None, "reason": reason},
        "obstruction": {"kind": kind, "reason": reason},
        "human_card": {"result": outcome, "why": reason},
    }


def _observable(
    payload: dict[str, object], metric: RealMatrix, links: tuple[gaussian.ComplexMatrix, ...]
) -> dict[str, object] | None:
    observable = payload.get("observable")
    if observable is None:
        return None
    if not isinstance(observable, dict) or observable.get("kind") != "linked-symbol-projectors":
        raise CoupledRelationObstruction(
            "UnsupportedObservable", "only linked-symbol-projectors is admitted"
        )
    raw_covector = observable.get("covector")
    if not isinstance(raw_covector, list) or len(raw_covector) != len(metric):
        raise CoupledRelationObstruction(
            "InvalidObservable", "observable covector has the wrong dimension"
        )
    try:
        covector = tuple(gaussian.rational(item) for item in raw_covector)
        return symbol_projectors(metric, links, covector)
    except (ValueError, ZeroDivisionError) as error:
        raise CoupledRelationObstruction("ProjectorNormObstruction", str(error)) from error


def discover_payload(payload: dict[str, object]) -> dict[str, object]:
    value: CoupledPlan | None = None
    try:
        if payload.get("schema") != "coupled-carrier-covariance/v1":
            raise CoupledRelationObstruction("UnsupportedProblemType", "unexpected schema")
        metric, links, capabilities, budget = _parse(payload)
        value = plan(metric, links)
        refusal = admission_refusal(value, budget)
        if refusal is not None:
            kind, reason = refusal
            return _failure("unresolved", kind, reason, value)
        relation_checks = clifford_checks(metric, links)
        if CAPABILITY in capabilities and not all(relation_checks.values()):
            failed = next(name for name, passed in relation_checks.items() if not passed)
            return _failure(
                "obstructed",
                "CliffordRelationViolation",
                f"requested Clifford relation fails at {failed}",
                value,
            )
        built = construct(metric, links, value, budget)
        compilation = built.compilation
        if compilation.outcome != "exact":
            return _failure(
                compilation.outcome,
                compilation.obstruction_kind or "CoupledCompilationFailure",
                compilation.obstruction_reason or "coupled relation compilation failed",
                value,
            )
        use = _observable(payload, metric, links)
    except CoupledRelationObstruction as error:
        return _failure("obstructed", error.kind, str(error), value)
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        return _failure("obstructed", "InvalidRelationInput", str(error), value)

    ledger = [
        {
            "name": entry.name,
            "target_dimension": entry.target_dimension,
            "residual_rank": entry.residual_rank,
            "kernel_dimension": entry.kernel_dimension,
        }
        for entry in compilation.ledger
    ]
    effective = [
        serialize_pair(combine_pair(coefficients, built.pairs))
        for coefficients in compilation.effective_representatives
    ]
    ineffective = [
        serialize_pair(combine_pair(coefficients, built.pairs))
        for coefficients in compilation.ineffective_basis
    ]
    witness = {
        "preserved_object": "metric-linked carrier covariance and requested symbol channels",
        "construction": "intrinsic End(V) plus u(S) seed; simultaneous relation kernel; ineffective quotient",
        "dimensions": {
            "base": value.base_dimension,
            "fiber": value.fiber_dimension,
            "candidate": compilation.candidate_dimension,
            "kernel": compilation.kernel_dimension,
            "ineffective": len(compilation.ineffective_basis),
            "effective": compilation.effective_dimension,
        },
        "relations": {"clifford_checks": relation_checks, "defect_ledger": ledger},
        "generators": {"effective": effective, "ineffective": ineffective},
        "closure": compilation.closure_status,
        "quotient_bracket_table": [
            [[gaussian.rational_text(item) for item in bracket] for bracket in row]
            for row in compilation.quotient_bracket_table
        ],
        "residuals": {"all_exact": True},
        "error": {"kind": "exact", "bound": 0},
        "use": use,
        "human_compression": {
            "primitive_generator_count": value.candidate_dimension,
            "relation_law_count": 2,
            "semantic_transformation_depth": 3,
            "effective_generator_count": compilation.effective_dimension,
            "coordinate_expansion_depth": 0,
            "retained_operations": [
                "metric preservation",
                "link covariance",
                "ineffective quotient",
                "bracket closure",
            ],
        },
        "validity": {
            "field": "Gaussian rationals",
            "base_metric": "nondegenerate symmetric",
            "fiber": "finite Hermitian",
            "global_group_integrated": False,
        },
    }
    return {
        "schema": "reduction-decision/v1",
        "outcome": "exact",
        "request": {
            "problem_type": payload["schema"],
            "supplied_group_name": False,
            "required_capabilities": list(capabilities),
        },
        "planning": _planning(value, materialized=True),
        "probes": [{"route": ROUTE, "outcome": "exact", "first_residual": None}],
        "candidates": [{"route": ROUTE, "outcome": "exact", "witness": witness}],
        "coincidence": {"status": "single_constructed_route"},
        "decision": {
            "selected_route": ROUTE,
            "reason": "the coupled relation kernel is exact, effective, and closed",
        },
        "human_card": {
            "result": "exact coupled-carrier covariance algebra",
            "primitive_objects": "one metric, one link, two relation laws, one quotient",
            "dimensions": f"{value.candidate_dimension}->{compilation.kernel_dimension}->{compilation.effective_dimension}",
            "boundary": "finite exact local carriers; no global integration or analytic completion",
        },
    }


def discover_document(document: ProblemDocument) -> dict[str, object]:
    return discover_payload(document.payload)


def discover_problem(path: Path) -> dict[str, object]:
    try:
        return discover_document(load_problem(path))
    except ProblemInputError as error:
        return _failure("obstructed", "InvalidProblemInput", str(error))

"""Lift a group-free coupled carrier action through a full operator package."""

from __future__ import annotations

from pathlib import Path

from coupled_covariance_core import (
    admission_refusal as relation_admission_refusal,
)
from coupled_covariance_core import clifford_checks, combine_pair, serialize_pair
from coupled_covariance_core import construct as construct_relation
from coupled_covariance_core import plan as plan_relation
from coupled_operator_input import SCHEMA, OperatorInputError, parse
from coupled_relation_input import CAPABILITY
from full_operator_covariance import (
    admission_refusal as operator_admission_refusal,
)
from full_operator_covariance import construct as construct_operator
from full_operator_covariance import plan as plan_operator
from pauli_operator_channels import PauliChannelError
from pauli_operator_channels import construct as construct_pauli_use
from problem_input import ProblemDocument, ProblemInputError, load_problem

ROUTE = "coupled-full-operator-kernel"


class LiftError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


def _planning(relation: object = None, operator: object = None) -> dict[str, object]:
    def record(value: object) -> dict[str, object] | None:
        if value is None:
            return None
        return {
            "candidate_dimension": value.candidate_dimension,
            "residual_dimension": value.residual_dimension,
            "bracket_upper_bound": value.bracket_upper_bound,
        }

    return {
        "policy": "admission-before-materialization-at-each-stage",
        "relation": record(relation),
        "operator": record(operator),
    }


def _failure(
    payload: object,
    kind: str,
    reason: str,
    *,
    planning: dict[str, object] | None = None,
    first_residual: str | None = None,
) -> dict[str, object]:
    outcome = "unresolved" if kind.endswith("BudgetExceeded") else "obstructed"
    return {
        "schema": "reduction-decision/v1",
        "outcome": outcome,
        "request": {
            "problem_type": payload.get("schema", "unknown")
            if isinstance(payload, dict)
            else "unknown",
            "supplied_group_name": False,
        },
        "planning": planning,
        "probes": [
            {
                "route": ROUTE,
                "outcome": outcome,
                "first_residual": first_residual or kind,
            }
        ],
        "candidates": [],
        "coincidence": None,
        "decision": {"selected_route": None, "reason": reason},
        "obstruction": {"kind": kind, "reason": reason},
        "human_card": {"result": "full-operator lift refused", "why": reason},
    }


def _raise_compilation(compilation: object, fallback: str) -> None:
    if compilation.outcome != "exact":
        raise LiftError(
            compilation.obstruction_kind or fallback,
            compilation.obstruction_reason or f"{fallback} failed",
        )


def _ledger(compilation: object) -> list[dict[str, object]]:
    return [
        {
            "name": entry.name,
            "target_dimension": entry.target_dimension,
            "residual_rank": entry.residual_rank,
            "rank_drop": entry.rank_drop,
            "kernel_dimension": entry.kernel_dimension,
        }
        for entry in compilation.ledger
    ]


def discover_payload(payload: object) -> dict[str, object]:
    relation_plan = None
    operator_plan = None
    use_error: PauliChannelError | None = None
    try:
        data = parse(payload)
        relation_plan = plan_relation(data.metric, data.links)
        refusal = relation_admission_refusal(relation_plan, data.relation_budget)
        if refusal is not None:
            raise LiftError(*refusal)
        relations = clifford_checks(data.metric, data.links)
        if CAPABILITY in data.capabilities and not all(relations.values()):
            failed = next(name for name, passed in relations.items() if not passed)
            raise LiftError(
                "CliffordRelationViolation", f"requested Clifford relation fails at {failed}"
            )
        relation = construct_relation(data.metric, data.links, relation_plan, data.relation_budget)
        _raise_compilation(relation.compilation, "CoupledCompilationFailure")
        relation_pairs = tuple(
            combine_pair(coefficients, relation.pairs)
            for coefficients in relation.compilation.effective_representatives
        )

        operator_plan = plan_operator(
            relation_pairs, data.curvature, data.first_order, data.zero_order
        )
        refusal = operator_admission_refusal(operator_plan, data.operator_budget)
        if refusal is not None:
            raise LiftError(*refusal)
        lifted = construct_operator(
            relation_pairs,
            relation.compilation.quotient_bracket_table,
            data.curvature,
            data.first_order,
            data.zero_order,
            data.operator_budget,
        )
        _raise_compilation(lifted, "FullOperatorCompilationFailure")
        if lifted.effective_dimension == 0:
            residual = next(entry.name for entry in lifted.ledger if entry.kernel_dimension == 0)
            return _failure(
                payload,
                "NoEffectiveOperatorSymmetry",
                f"the constructed action is killed by {residual}",
                planning=_planning(relation_plan, operator_plan),
                first_residual=residual,
            )
        use = None
        if data.maximum_level is not None:
            try:
                use = construct_pauli_use(
                    data.metric,
                    data.links,
                    data.curvature,
                    data.first_order,
                    data.zero_order,
                    data.maximum_level,
                )
            except PauliChannelError as error:
                use_error = error
    except (OperatorInputError, LiftError) as error:
        return _failure(
            payload,
            error.kind,
            str(error),
            planning=_planning(relation_plan, operator_plan),
        )
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        return _failure(
            payload,
            "InvalidOperatorInput",
            str(error),
            planning=_planning(relation_plan, operator_plan),
        )

    surviving_pairs = [
        serialize_pair(combine_pair(coefficients, relation_pairs))
        for coefficients in lifted.effective_representatives
    ]
    witness = {
        "preserved_object": "full coupled operator and any requested observable channels",
        "construction": "G4 coupled action followed by ordered coefficient defects and domain matching",
        "relation_stage": {
            "candidate_dimension": relation.compilation.candidate_dimension,
            "kernel_dimension": relation.compilation.kernel_dimension,
            "ineffective_dimension": len(relation.compilation.ineffective_basis),
            "effective_dimension": relation.compilation.effective_dimension,
        },
        "operator_stage": {
            "dimensions": {
                "candidate": lifted.candidate_dimension,
                "kernel": lifted.kernel_dimension,
                "effective": lifted.effective_dimension,
            },
            "defect_ledger": _ledger(lifted),
            "closure": lifted.closure_status,
            "generators": surviving_pairs,
        },
        "domain": data.domain_witness,
        "maps": {
            "analysis": (
                None
                if use is None
                else "parallel Fourier, curvature grading, and oscillator-number analysis"
            ),
            "synthesis": (
                None
                if use is None
                else "spin/Fock channel sum and inverse parallel Fourier transform"
            ),
        },
        "use": use,
        "residuals": {"all_exact": True},
        "error": {"kind": "exact algebraic/common-core", "bound": 0},
        "human_compression": {
            "relation_laws": 2,
            "ordered_operator_defects": 3,
            "effective_dimensions": f"{relation.compilation.effective_dimension}->{lifted.effective_dimension}",
            "coordinate_eigenfunction_expansions": 0,
        },
        "validity": {
            "field": "Gaussian rationals",
            "coefficients": "constant covariant-momentum normal form",
            "domain": "matched boundaryless Schwartz common core",
            "self_adjoint_completion": False,
            "global_group_integrated": False,
        },
    }
    observable_blocked = use_error is not None
    result = {
        "schema": "reduction-decision/v1",
        "outcome": "obstructed" if observable_blocked else "exact",
        "request": {
            "problem_type": SCHEMA,
            "observable": None
            if data.maximum_level is None
            else "spin_resolved_transverse_energy_channels",
            "supplied_group_name": False,
            "supplied_generators": False,
        },
        "planning": _planning(relation_plan, operator_plan),
        "probes": [
            {
                "route": ROUTE,
                "outcome": "obstructed" if observable_blocked else "exact",
                "first_residual": "observable-recovery" if observable_blocked else None,
            }
        ],
        "candidates": [{"route": ROUTE, "outcome": "exact", "witness": witness}],
        "coincidence": (
            None if observable_blocked else {"status": "external_bilateral_regression_target"}
        ),
        "decision": {
            "selected_route": None if observable_blocked else ROUTE,
            "reason": (
                str(use_error)
                if observable_blocked
                else "the generated action survives every operator layer and the domain contract"
            ),
            "common_transverse_channels": [] if use is None else use["channels"],
            "longitudinal_transport_channels": ([] if use is None else use["transport_channels"]),
            "curvature_aligned_projector": (
                None if use is None else use["projectors"]["curvature_aligned"]
            ),
        },
        "human_card": {
            "result": (
                "operator exact; requested observable refused"
                if observable_blocked
                else "exact group-free full-operator lift"
            ),
            "dimensions": f"{relation.compilation.effective_dimension}->{lifted.effective_dimension}",
            "replaced_expansion": "component PDE diagonalization and supplied rotation generators",
            "boundary": "constant Euclidean rank-three Pauli operators on the matched common core",
        },
    }
    if use_error is not None:
        result["obstruction"] = {"kind": use_error.kind, "reason": str(use_error)}
    return result


def discover_document(document: ProblemDocument) -> dict[str, object]:
    return discover_payload(document.payload)


def discover_problem(path: Path) -> dict[str, object]:
    try:
        return discover_document(load_problem(path))
    except ProblemInputError as error:
        return _failure({}, "InvalidProblemInput", str(error))

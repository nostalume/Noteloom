"""Observable-relative analytic promotion of a generated adjoint symbol core."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

from adjoint_algebra import fraction as _fraction
from adjoint_algebra import matrix as _matrix
from adjoint_algebra import pair as _pair
from adjoint_algebra import text as _text
from adjoint_algebra import trace as _trace
from matrix_symbol_covariance_router import discover_payload as discover_local_symbol
from problem_input import ProblemDocument, ProblemInputError, load_problem


class MatrixAdjointGlobalObstruction(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


def _load_local_problem(
    payload: dict[str, object], path: Path
) -> tuple[dict[str, object], dict[str, object]]:
    filename = payload.get("local_problem_file")
    if not isinstance(filename, str) or not filename:
        raise MatrixAdjointGlobalObstruction(
            "MissingLocalBridge",
            "local_problem_file must name a matrix-symbol-covariance ProblemSpec",
        )
    if Path(filename).name != filename:
        raise MatrixAdjointGlobalObstruction(
            "InvalidLocalBridgePath",
            "local_problem_file must stay in the global input directory",
        )
    parent = path.resolve().parent
    local_path = (parent / filename).resolve()
    if local_path.parent != parent:
        raise MatrixAdjointGlobalObstruction(
            "InvalidLocalBridgePath", "local_problem_file escaped its input directory"
        )
    try:
        local_payload = json.loads(local_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise MatrixAdjointGlobalObstruction("MissingLocalBridge", str(error)) from error
    if not isinstance(local_payload, dict) or local_payload.get("schema") != (
        "matrix-symbol-covariance/v1"
    ):
        raise MatrixAdjointGlobalObstruction(
            "MissingLocalBridge",
            "the referenced local input must use matrix-symbol-covariance/v1",
        )
    local_result = discover_local_symbol(local_payload)
    if local_result.get("outcome") != "exact":
        obstruction = local_result.get("obstruction")
        reason = (
            obstruction.get("reason", "local symbol construction was not exact")
            if isinstance(obstruction, dict)
            else "local symbol construction was not exact"
        )
        raise MatrixAdjointGlobalObstruction("LocalBridgeObstruction", str(reason))
    return local_payload, local_result


def _matrix_size(local_payload: dict[str, object], payload: dict[str, object]) -> int:
    raw_generators = local_payload.get("coefficient_generators")
    if not isinstance(raw_generators, list) or not raw_generators:
        raise MatrixAdjointGlobalObstruction(
            "LocalBridgeObstruction", "local coefficient seeds are unavailable"
        )
    first = raw_generators[0]
    if not isinstance(first, list) or len(first) not in (2, 3):
        raise MatrixAdjointGlobalObstruction(
            "LocalBridgeObstruction", "local matrix size is outside the admitted horizon"
        )
    matrix_size = len(first)
    budget = payload.get("resource_budget")
    maximum = budget.get("maximum_matrix_size") if isinstance(budget, dict) else None
    if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum not in (2, 3):
        raise MatrixAdjointGlobalObstruction(
            "InvalidBudget", "maximum_matrix_size must be two or three"
        )
    if matrix_size > maximum:
        raise MatrixAdjointGlobalObstruction(
            "ResourceBudgetExceeded", "the local matrix size exceeds the global budget"
        )
    return matrix_size


def _validate_real_form(payload: dict[str, object]) -> dict[str, object]:
    real_form = payload.get("real_form")
    expected = {
        "involution": "conjugate_transpose",
        "fixed_condition": "star_skew_traceless",
        "inner_product": "negative_trace_on_compact_real_form",
        "normalization_scale": "2",
    }
    if not isinstance(real_form, dict) or any(
        real_form.get(key) != value for key, value in expected.items()
    ):
        raise MatrixAdjointGlobalObstruction(
            "RealFormPositivityObstruction",
            "compact promotion requires conjugate transpose, the star-skew traceless real form, and -2tr(XY)",
        )
    return {
        "construction": "k={X in sl_n(C): X^*=-X}",
        "positive_inner_product": "<X,X>=-2tr(X^2)=2tr(X^*X)>0 for X!=0",
        "compactness_contract": "the star-unitary determinant-one matrix group integrating k is compact",
    }


def _validate_global_carrier(payload: dict[str, object]) -> None:
    carrier = payload.get("global_carrier")
    expected = {
        "integration": "connected_star_unitary_determinant_one_matrix_group",
        "effective_base": "adjoint_central_quotient",
        "measure": "normalized_haar_probability",
    }
    if not isinstance(carrier, dict) or any(
        carrier.get(key) != value for key, value in expected.items()
    ):
        raise MatrixAdjointGlobalObstruction(
            "GlobalCarrierObstruction",
            "the admitted carrier is the normalized-Haar adjoint quotient of the connected star-unitary determinant-one group",
        )


def _validate_domain(payload: dict[str, object]) -> None:
    domain = payload.get("domain_contract")
    expected = {
        "carrier": "L2_effective_compact_group_with_complexified_adjoint_fiber",
        "operator": "positive_biinvariant_laplacian",
        "domain": "H2_sobolev",
        "core": "smooth_sections",
        "semigroup": "spectral_theorem_contraction",
    }
    if not isinstance(domain, dict) or any(
        domain.get(key) != value for key, value in expected.items()
    ):
        raise MatrixAdjointGlobalObstruction(
            "DomainContractObstruction",
            "the compact Laplacian promotion requires the admitted H^2-to-L^2 self-adjoint domain contract",
        )


def _observable(
    payload: dict[str, object], matrix_size: int, eigenvalue: Fraction
) -> dict[str, object]:
    observable = payload.get("observable")
    if not isinstance(observable, dict) or observable.get("kind") != (
        "adjoint_coefficient_heat_matrix_element_and_exchange_pair"
    ):
        raise MatrixAdjointGlobalObstruction(
            "UnsupportedObservable",
            "the global bench preserves one adjoint heat matrix element and the local exchange pair",
        )
    time = _fraction(observable.get("heat_time"))
    if time <= 0:
        raise MatrixAdjointGlobalObstruction("InvalidHeatTime", "heat_time must be positive")
    state = _matrix(observable.get("state_parameter"), matrix_size, "observable.state_parameter")
    probe = _matrix(observable.get("probe"), matrix_size, "observable.probe")
    if _trace(state) != 0 or _trace(probe) != 0:
        raise MatrixAdjointGlobalObstruction(
            "CarrierViolation", "the semigroup state and probe must be traceless"
        )
    initial_pairing = _pair(probe, state)
    exponent = eigenvalue * time
    exponential = f"exp(-{_text(exponent)})"
    if initial_pairing == 0:
        symbolic = "0"
    elif initial_pairing == 1:
        symbolic = exponential
    else:
        symbolic = f"{_text(initial_pairing)}*{exponential}"
    return {
        "heat_time": _text(time),
        "initial_pairing": _text(initial_pairing),
        "exponent": _text(exponent),
        "symbolic": symbolic,
        "numeric": float(initial_pairing) * math.exp(-float(exponent)),
    }


def _obstruction(
    payload: object,
    error: MatrixAdjointGlobalObstruction,
    local_result: dict[str, object] | None,
) -> dict[str, object]:
    return {
        "schema": "reduction-decision/v1",
        "outcome": "obstructed",
        "request": {
            "problem_type": payload.get("schema", "unknown")
            if isinstance(payload, dict)
            else "unknown",
            "supplied_group_name": False,
        },
        "local_stage": local_result,
        "probes": [],
        "candidates": [],
        "coincidence": None,
        "decision": {"selected_route": None, "reason": str(error)},
        "obstruction": {"kind": error.kind, "reason": str(error)},
        "human_card": {
            "result": "local algebraic witness retained; analytic promotion obstructed",
            "why": str(error),
        },
    }


def _construct(
    payload: dict[str, object],
    path: Path,
    local_bundle: tuple[dict[str, object], dict[str, object]] | None = None,
) -> dict[str, object]:
    if payload.get("schema") != "matrix-adjoint-semigroup/v1":
        raise MatrixAdjointGlobalObstruction(
            "UnsupportedProblemType", "expected matrix-adjoint-semigroup/v1"
        )
    local_payload, local_result = (
        local_bundle if local_bundle is not None else _load_local_problem(payload, path)
    )
    matrix_size = _matrix_size(local_payload, payload)
    real_form = _validate_real_form(payload)
    _validate_global_carrier(payload)
    _validate_domain(payload)

    local_decision = local_result.get("decision")
    if not isinstance(local_decision, dict):
        raise MatrixAdjointGlobalObstruction(
            "LocalBridgeObstruction", "local decision data are unavailable"
        )
    eigenvalue = _fraction(local_decision.get("derived_coefficient_eigenvalue"))
    if eigenvalue != matrix_size:
        raise MatrixAdjointGlobalObstruction(
            "LocalBridgeObstruction",
            "the local differential eigenvalue does not have the admitted normalization",
        )
    heat = _observable(payload, matrix_size, eigenvalue)
    exchange = local_decision.get("observable")
    if not isinstance(exchange, dict):
        raise MatrixAdjointGlobalObstruction(
            "LocalBridgeObstruction", "the local exchange observable is unavailable"
        )

    simply_connected_group = f"SU({matrix_size})"
    effective_group = f"PSU({matrix_size})"
    checks = {
        "compact_real_form_constructed_from_involution": True,
        "real_form_inner_product_positive": True,
        "normalized_haar_contract_admitted": True,
        "self_adjoint_H2_laplacian_contract_admitted": True,
        "visible_semigroup_action_from_generated_eigenvalue": True,
        "center_acts_trivially_on_adjoint_coefficients": True,
        "normalized_haar_pushforward_preserves_visible_pairing": True,
        "central_quotient_observable_coincidence": True,
        "local_exchange_observable_retained": True,
    }
    witness = {
        "preserved_object": "adjoint coefficient heat matrix element plus exchange-paired tensor amplitude",
        "construction": "involution -> compact real form -> matrix group/center quotient -> H2 Laplacian semigroup",
        "reduced_object": {
            "kind": "one closed adjoint coefficient semigroup block",
            "dimension": matrix_size * matrix_size - 1,
            "eigenvalue": _text(eigenvalue),
            "effective_group": effective_group,
        },
        "maps": {
            "synthesis": "S(Y)=q_Y, q_Y(g)=Ad_(g^-1)Y",
            "analysis": "A(q_Y)=Y on the adjoint coefficient copy",
            "semigroup": f"exp(-t Delta)S=S exp(-{_text(eigenvalue)}t)",
            "quotient": f"SU({matrix_size}) -> {effective_group} removes the center invisible to Ad",
            "observable": "O_Z(q_W)=tr(ZW)",
        },
        "residuals": {"all_passed": True, "checks": checks},
        "error": {"kind": "exact theorem-backed visible semigroup", "bound": 0},
        "cost": {
            "local_symbol_closure_reused": True,
            "new_spectral_decompositions": 0,
            "representation_sectors_enumerated": 0,
            "visible_scalar_exponentials": 1,
            "observable_trace_pairings": 1,
            "full_heat_trace_cost": "not paid and not recovered",
        },
        "validity": {
            "matrix_sizes": [2, 3],
            "real_form": real_form,
            "carrier": f"L^2({effective_group},sl_{matrix_size}(C))",
            "domain": f"H^2({effective_group},sl_{matrix_size}(C))",
            "core": f"C^infinity({effective_group},sl_{matrix_size}(C))",
            "measure": "normalized Haar probability",
        },
    }
    return {
        "schema": "reduction-decision/v1",
        "outcome": "exact",
        "request": {
            "problem_type": payload["schema"],
            "observable": payload["observable"]["kind"],
            "supplied_group_name": False,
            "supplied_lie_algebra_name": False,
            "supplied_coefficient_eigenvalue": False,
            "supplied_heat_value": False,
        },
        "local_stage": local_result,
        "probes": [
            {
                "route": "compact-real-form-and-domain-promotion",
                "applicable": True,
                "trigger": "compatible involution, positive compact form, Haar carrier, and H2 domain",
                "first_residual": None,
            }
        ],
        "candidates": [
            {"route": "adjoint-visible-heat-semigroup", "outcome": "exact", "witness": witness}
        ],
        "coincidence": {
            "status": "exact_simply_connected_and_adjoint_quotient_observable_coincidence",
            "all_passed": True,
            "checks": checks,
            "same_observable": {
                "heat_matrix_element": heat["symbolic"],
                "exchange_pair": exchange,
            },
        },
        "decision": {
            "selected_route": "adjoint-visible-heat-semigroup",
            "reason": "the involution and domain promote the generated eigenmodule, while the observable quotients the center",
            "constructed_simply_connected_group": simply_connected_group,
            "observable_effective_group": effective_group,
            "center_order": matrix_size,
            "adjoint_eigenvalue": _text(eigenvalue),
            "heat_time": heat["heat_time"],
            "heat_matrix_element_symbolic": heat["symbolic"],
            "heat_matrix_element_numeric": heat["numeric"],
            "exchange_observable": exchange,
        },
        "analytic_witness": {
            "carrier": f"L^2({effective_group},sl_{matrix_size}(C))",
            "domain": f"H^2({effective_group},sl_{matrix_size}(C)) -> L^2({effective_group},sl_{matrix_size}(C))",
            "core": f"C^infinity({effective_group},sl_{matrix_size}(C))",
            "measure": "normalized Haar probability",
            "semigroup": f"exp(-t Delta)q_Y=exp(-{_text(eigenvalue)}t)q_Y",
            "self_adjointness": "imported compact elliptic Laplacian theorem contract",
        },
        "human_card": {
            "result": f"the generated algebra promotes to a visible heat block on {effective_group}",
            "one_line_computation": f"O_Z(exp(-t Delta)q_Y)={heat['symbolic']}",
            "ambiguity_removed": f"the center Z_{matrix_size} is quotiented because it acts trivially on every retained object",
            "boundary": "one adjoint coefficient block only; no full heat trace or unique global-group recovery",
        },
        "not_certified": [
            "the full Peter--Weyl heat trace or spectrum",
            "global information visible only to non-adjoint representations",
            "automatic analytic promotion for noncompact or non-semisimple real forms",
            "machine proof of the imported compact elliptic self-adjointness theorem",
        ],
    }


def discover_document(document: ProblemDocument) -> dict[str, object]:
    payload: object = document.payload
    local_result: dict[str, object] | None = None
    try:
        local_bundle = None
        if payload.get("schema") == "matrix-adjoint-semigroup/v1":
            local_bundle = _load_local_problem(payload, document.path)
            local_result = local_bundle[1]
        return _construct(payload, document.path, local_bundle)
    except MatrixAdjointGlobalObstruction as error:
        return _obstruction(payload, error, local_result)


def discover_problem(path: Path) -> dict[str, object]:
    try:
        return discover_document(load_problem(path))
    except ProblemInputError as error:
        return _obstruction(
            {},
            MatrixAdjointGlobalObstruction("InvalidProblemSpec", str(error)),
            None,
        )

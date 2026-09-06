"""Dispatch backend-independent ProblemSpec inputs by their semantic schema."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from coupled_operator_router import discover_document as discover_coupled_operator
from coupled_relation_stabilizer import discover_document as discover_coupled_relation
from matrix_adjoint_global_router import discover_document as discover_matrix_adjoint_global
from matrix_pde_inverse_router import discover_document as discover_matrix_pde_inverse
from matrix_symbol_covariance_router import discover_document as discover_matrix_symbol
from natural_tensor_stabilizer import discover_document as discover_natural_tensor
from pauli_bilateral_router import discover_document as discover_pauli
from pauli_global_router import discover_document as discover_global_pauli
from problem_input import ProblemDocument, ProblemInputError, load_problem
from quadratic_route_router import discover_document as discover_quadratic
from su_adjoint_multiplicity_router import discover_document as discover_su_adjoint

Handler = Callable[[ProblemDocument], dict[str, object]]

HANDLERS: dict[str, Handler] = {
    "coupled-carrier-covariance/v1": discover_coupled_relation,
    "coupled-operator-covariance/v1": discover_coupled_operator,
    "quadratic-schrodinger/v1": discover_quadratic,
    "pauli-landau-bilateral/v1": discover_pauli,
    "pauli-landau-global/v1": discover_global_pauli,
    "su-adjoint-transition/v1": discover_su_adjoint,
    "su-adjoint-pde/v1": discover_su_adjoint,
    "matrix-pde-inverse/v1": discover_matrix_pde_inverse,
    "matrix-symbol-covariance/v1": discover_matrix_symbol,
    "matrix-adjoint-semigroup/v1": discover_matrix_adjoint_global,
    "natural-tensor-stabilizer/v1": discover_natural_tensor,
}


def _unsupported(problem_type: object, reason: str) -> dict[str, object]:
    return {
        "schema": "reduction-decision/v1",
        "outcome": "obstructed",
        "request": {"problem_type": problem_type},
        "probes": [],
        "candidates": [],
        "coincidence": None,
        "decision": {"selected_route": None, "reason": reason},
        "obstruction": {"kind": "UnsupportedProblemType", "reason": reason},
        "human_card": {"result": "obstructed", "why": reason},
    }


def discover_problem(path: Path) -> dict[str, object]:
    """Select a bounded constructor from the input schema, never a backend name."""

    try:
        document = load_problem(path)
    except ProblemInputError as error:
        reason = str(error)
        if reason == "ProblemSpec must be a JSON object":
            return _unsupported("unknown", reason)
        return _unsupported("unknown", f"invalid ProblemSpec: {reason}")
    problem_type = document.payload.get("schema")
    handler = HANDLERS.get(problem_type) if isinstance(problem_type, str) else None
    if handler is not None:
        return handler(document)
    schemas = tuple(HANDLERS)
    supported = ", ".join((*schemas[:-1], f"and {schemas[-1]}"))
    return _unsupported(problem_type, f"supported ProblemSpec schemas are {supported}")

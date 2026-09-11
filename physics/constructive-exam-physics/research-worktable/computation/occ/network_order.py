"""Sparse scalar-elimination plans for reciprocal linear networks."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Optional

from sympy import Matrix, Symbol, simplify, sympify
from sympy.core.expr import Expr

from .network import (
    LinearNetworkRequest,
    _validate_request,
    condense_linear_network,
)
from .records import Certificate


@dataclass(frozen=True)
class RecoveryCoefficient:
    symbol: Symbol
    coefficient: Expr


@dataclass(frozen=True)
class ScalarEliminationStep:
    eliminated_symbol: Symbol
    pivot: Expr
    active_neighbors: tuple[Symbol, ...]
    fill_edges_added: int
    algebraic_updates: int
    recovery_coefficients: tuple[RecoveryCoefficient, ...]
    recovery_offset: Expr


@dataclass(frozen=True)
class NetworkPlanningObstruction:
    code: str
    message: str


@dataclass(frozen=True)
class NetworkEliminationPlan:
    status: str
    strategy: str
    area: str
    state_kind: str
    boundary_symbols: tuple[Symbol, ...]
    internal_symbols: tuple[Symbol, ...]
    elimination_order: tuple[Symbol, ...] = ()
    steps: tuple[ScalarEliminationStep, ...] = ()
    condensed_matrix: tuple[tuple[Expr, ...], ...] = ()
    condensed_source: tuple[Expr, ...] = ()
    total_fill_edges: int = 0
    total_algebraic_updates: int = 0
    certificates: tuple[Certificate, ...] = ()
    obstruction: Optional[NetworkPlanningObstruction] = None
    provenance: str = ""

    def reconstruct_internal(
        self, boundary_values: tuple[object, ...]
    ) -> tuple[Expr, ...]:
        if self.status != "constructed":
            raise ValueError("Internal states require a constructed elimination plan.")
        if len(boundary_values) != len(self.boundary_symbols):
            raise ValueError(
                "Boundary-value count must match the boundary symbol count."
            )
        known = {
            symbol: sympify(value)
            for symbol, value in zip(
                self.boundary_symbols, boundary_values, strict=True
            )
        }
        for step in reversed(self.steps):
            known[step.eliminated_symbol] = simplify(
                step.recovery_offset
                + sum(
                    term.coefficient * known[term.symbol]
                    for term in step.recovery_coefficients
                )
            )
        return tuple(known[symbol] for symbol in self.internal_symbols)


def _is_zero(value: Expr) -> bool:
    return simplify(value).is_zero is True


def _matrix_tuple(matrix: Matrix) -> tuple[tuple[Expr, ...], ...]:
    return tuple(
        tuple(simplify(matrix[row, column]) for column in range(matrix.cols))
        for row in range(matrix.rows)
    )


def _vector_tuple(vector: Matrix) -> tuple[Expr, ...]:
    return tuple(simplify(value) for value in vector)


def _candidate_shape(matrix: Matrix, pivot_index: int) -> tuple[tuple[int, ...], int]:
    neighbors = tuple(
        index
        for index in range(matrix.rows)
        if index != pivot_index and not _is_zero(matrix[index, pivot_index])
    )
    pivot = simplify(matrix[pivot_index, pivot_index])
    fill_edges = 0
    for first, second in combinations(neighbors, 2):
        before = matrix[first, second]
        after = simplify(
            before - matrix[first, pivot_index] * matrix[pivot_index, second] / pivot
        )
        fill_edges += _is_zero(before) and not _is_zero(after)
    return neighbors, fill_edges


def _refusal(common, code: str, message: str) -> NetworkEliminationPlan:
    return NetworkEliminationPlan(
        status="refused",
        obstruction=NetworkPlanningObstruction(code, message),
        **common,
    )


def plan_network_elimination(
    request: LinearNetworkRequest,
    *,
    strategy: str = "min_fill",
    max_steps: int = 8,
) -> NetworkEliminationPlan:
    """Construct a sparse, reversible scalar-elimination route."""

    if strategy not in {"min_fill", "declared"}:
        raise ValueError("strategy must be 'min_fill' or 'declared'.")
    if not isinstance(max_steps, int) or isinstance(max_steps, bool) or max_steps < 0:
        raise ValueError("max_steps must be a nonnegative integer.")
    response, source = _validate_request(request)
    state_kind = request.variables[0].state_kind
    common = {
        "strategy": strategy,
        "area": request.area,
        "state_kind": state_kind,
        "boundary_symbols": request.boundary_symbols,
        "internal_symbols": request.internal_symbols,
        "provenance": request.provenance,
    }
    if any(not _is_zero(value) for value in response - response.T):
        return _refusal(
            common,
            "nonreciprocal_response",
            "The sparse human planner currently requires an exact symmetric response.",
        )
    if not request.internal_symbols:
        block = condense_linear_network(request, max_internal=0)
        return NetworkEliminationPlan(
            status="irreducible",
            condensed_matrix=block.condensed_matrix,
            condensed_source=block.condensed_source,
            obstruction=NetworkPlanningObstruction(
                "no_internal_variables", "The packet has no hidden state to order."
            ),
            **common,
        )
    if len(request.internal_symbols) > max_steps:
        return _refusal(
            common,
            "elimination_step_budget_exceeded",
            "The hidden-state count exceeds the declared scalar-step budget.",
        )

    block = condense_linear_network(request, max_internal=max_steps)
    if block.status != "constructed":
        return _refusal(common, block.obstruction.code, block.obstruction.message)

    active_symbols = [variable.symbol for variable in request.variables]
    remaining_internal = list(request.internal_symbols)
    declared_rank = {
        symbol: index for index, symbol in enumerate(request.internal_symbols)
    }
    current_matrix = response
    current_source = source
    steps: list[ScalarEliminationStep] = []

    while remaining_internal:
        candidates = []
        for symbol in remaining_internal:
            pivot_index = active_symbols.index(symbol)
            pivot = simplify(current_matrix[pivot_index, pivot_index])
            if pivot.is_zero is not False:
                continue
            neighbors, fill_edges = _candidate_shape(current_matrix, pivot_index)
            candidates.append(
                (
                    fill_edges,
                    len(neighbors),
                    declared_rank[symbol],
                    symbol,
                    pivot_index,
                    pivot,
                    neighbors,
                )
            )

        if strategy == "declared":
            next_symbol = remaining_internal[0]
            candidates = [item for item in candidates if item[3] == next_symbol]
        if not candidates:
            return _refusal(
                common,
                "no_provable_scalar_pivot",
                "No remaining scalar diagonal pivot is provably nonzero.",
            )

        chosen = min(candidates, key=lambda item: item[:3])
        fill_edges, _, _, symbol, pivot_index, pivot, neighbor_indices = chosen
        retained_indices = [
            index for index in range(len(active_symbols)) if index != pivot_index
        ]
        retained_symbols = [active_symbols[index] for index in retained_indices]
        recovery_coefficients = tuple(
            RecoveryCoefficient(
                active_symbols[index],
                simplify(-current_matrix[pivot_index, index] / pivot),
            )
            for index in retained_indices
            if not _is_zero(current_matrix[pivot_index, index])
        )
        recovery_offset = simplify(current_source[pivot_index, 0] / pivot)
        neighbor_symbols = tuple(active_symbols[index] for index in neighbor_indices)
        neighbor_count = len(neighbor_indices)
        coefficient_updates = neighbor_count * (neighbor_count + 1) // 2
        source_updates = (
            neighbor_count if not _is_zero(current_source[pivot_index, 0]) else 0
        )
        algebraic_updates = coefficient_updates + source_updates
        steps.append(
            ScalarEliminationStep(
                eliminated_symbol=symbol,
                pivot=pivot,
                active_neighbors=neighbor_symbols,
                fill_edges_added=fill_edges,
                algebraic_updates=algebraic_updates,
                recovery_coefficients=recovery_coefficients,
                recovery_offset=recovery_offset,
            )
        )

        next_matrix = Matrix(
            [
                [
                    simplify(
                        current_matrix[row, column]
                        - current_matrix[row, pivot_index]
                        * current_matrix[pivot_index, column]
                        / pivot
                    )
                    for column in retained_indices
                ]
                for row in retained_indices
            ]
        )
        next_source = Matrix(
            [
                simplify(
                    current_source[row, 0]
                    - current_matrix[row, pivot_index]
                    * current_source[pivot_index, 0]
                    / pivot
                )
                for row in retained_indices
            ]
        )
        current_matrix = next_matrix
        current_source = next_source
        active_symbols = retained_symbols
        remaining_internal.remove(symbol)

    boundary_indices = [
        active_symbols.index(symbol) for symbol in request.boundary_symbols
    ]
    condensed_matrix = current_matrix.extract(boundary_indices, boundary_indices)
    condensed_source = current_source.extract(boundary_indices, [0])
    matrix_tuple = _matrix_tuple(condensed_matrix)
    source_tuple = _vector_tuple(condensed_source)

    provisional = NetworkEliminationPlan(
        status="constructed",
        elimination_order=tuple(step.eliminated_symbol for step in steps),
        steps=tuple(steps),
        condensed_matrix=matrix_tuple,
        condensed_source=source_tuple,
        total_fill_edges=sum(step.fill_edges_added for step in steps),
        total_algebraic_updates=sum(step.algebraic_updates for step in steps),
        **common,
    )
    sequential_recovery = provisional.reconstruct_internal(request.boundary_symbols)
    block_recovery = block.reconstruct_internal(request.boundary_symbols)
    certificates = (
        Certificate(
            name="block_condensation_equivalence",
            passed=matrix_tuple == block.condensed_matrix
            and source_tuple == block.condensed_source,
            witness="sequential scalar elimination equals the exact block result",
        ),
        Certificate(
            name="reverse_recovery_equivalence",
            passed=all(
                simplify(sequential - direct) == 0
                for sequential, direct in zip(
                    sequential_recovery, block_recovery, strict=True
                )
            ),
            witness="reverse local recovery equals the block affine recovery map",
        ),
        Certificate(
            name="provable_scalar_pivots",
            passed=len(steps) == len(request.internal_symbols)
            and all(step.pivot.is_zero is False for step in steps),
            witness="every local division uses a pivot proved nonzero",
        ),
    )
    if not all(certificate.passed for certificate in certificates):
        return _refusal(
            common,
            "certificate_failed",
            "The scalar route failed equivalence or recovery certification.",
        )
    return NetworkEliminationPlan(
        status=provisional.status,
        elimination_order=provisional.elimination_order,
        steps=provisional.steps,
        condensed_matrix=provisional.condensed_matrix,
        condensed_source=provisional.condensed_source,
        total_fill_edges=provisional.total_fill_edges,
        total_algebraic_updates=provisional.total_algebraic_updates,
        certificates=certificates,
        **common,
    )

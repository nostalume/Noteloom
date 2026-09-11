"""Exact boundary condensation for finite linear physical networks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from sympy import Matrix, Symbol, simplify, sympify
from sympy.core.expr import Expr

from .records import Certificate


@dataclass(frozen=True)
class NetworkVariable:
    """Area-preserving meaning attached to one network state symbol."""

    symbol: Symbol
    physical_name: str
    state_kind: str


@dataclass(frozen=True)
class LinearNetworkRequest:
    """A finite balance law K x = f and its observable/hidden partition."""

    area: str
    variables: tuple[NetworkVariable, ...]
    boundary_symbols: tuple[Symbol, ...]
    internal_symbols: tuple[Symbol, ...]
    response_matrix: tuple[tuple[object, ...], ...]
    source_vector: tuple[object, ...]
    provenance: str


@dataclass(frozen=True)
class NetworkObstruction:
    code: str
    message: str


@dataclass(frozen=True)
class NetworkCondensationResult:
    status: str
    area: str
    state_kind: str
    boundary_symbols: tuple[Symbol, ...]
    internal_symbols: tuple[Symbol, ...]
    condensed_matrix: tuple[tuple[Expr, ...], ...] = ()
    condensed_source: tuple[Expr, ...] = ()
    reconstruction_matrix: tuple[tuple[Expr, ...], ...] = ()
    reconstruction_offset: tuple[Expr, ...] = ()
    certificates: tuple[Certificate, ...] = ()
    obstruction: Optional[NetworkObstruction] = None
    provenance: str = ""

    def reconstruct_internal(
        self, boundary_values: tuple[object, ...]
    ) -> tuple[Expr, ...]:
        """Apply the returned affine recovery map to boundary-state values."""

        if self.status != "constructed":
            raise ValueError(
                "Internal states can be reconstructed only after construction."
            )
        if len(boundary_values) != len(self.boundary_symbols):
            raise ValueError(
                "Boundary-value count must match the boundary symbol count."
            )
        values = Matrix(tuple(sympify(value) for value in boundary_values))
        recovered = Matrix(self.reconstruction_matrix) * values + Matrix(
            self.reconstruction_offset
        )
        return tuple(simplify(value) for value in recovered)


def _matrix_tuple(matrix: Matrix) -> tuple[tuple[Expr, ...], ...]:
    return tuple(
        tuple(simplify(matrix[row, column]) for column in range(matrix.cols))
        for row in range(matrix.rows)
    )


def _vector_tuple(vector: Matrix) -> tuple[Expr, ...]:
    return tuple(simplify(value) for value in vector)


def _zero_matrix(matrix: Matrix) -> bool:
    return all(simplify(value) == 0 for value in matrix)


def _validate_request(request: LinearNetworkRequest) -> tuple[Matrix, Matrix]:
    if not request.area.strip():
        raise ValueError("A network area is required.")
    if not request.provenance.strip():
        raise ValueError("Network provenance is required.")
    if not request.variables:
        raise ValueError("At least one network variable is required.")
    if any(not isinstance(variable.symbol, Symbol) for variable in request.variables):
        raise TypeError("Every network variable must use a SymPy Symbol.")
    if any(not variable.physical_name.strip() for variable in request.variables):
        raise ValueError("Every network variable requires a physical name.")
    if any(not variable.state_kind.strip() for variable in request.variables):
        raise ValueError("Every network variable requires a state kind.")

    declared = tuple(variable.symbol for variable in request.variables)
    if len(declared) != len(set(declared)):
        raise ValueError("Network variable symbols must be unique.")
    state_kinds = {variable.state_kind for variable in request.variables}
    if len(state_kinds) != 1:
        raise ValueError("One network packet must use one shared state kind.")
    partition = request.boundary_symbols + request.internal_symbols
    if not request.boundary_symbols:
        raise ValueError("The network partition requires a nonempty boundary.")
    if len(partition) != len(set(partition)) or set(partition) != set(declared):
        raise ValueError(
            "The boundary/internal partition must cover each variable once."
        )

    size = len(declared)
    if len(request.response_matrix) != size or any(
        len(row) != size for row in request.response_matrix
    ):
        raise ValueError("The response matrix must be square over all variables.")
    if len(request.source_vector) != size:
        raise ValueError("The source vector must match the variable count.")
    return Matrix(request.response_matrix), Matrix(request.source_vector)


def condense_linear_network(
    request: LinearNetworkRequest,
    *,
    max_internal: int = 8,
) -> NetworkCondensationResult:
    """Eliminate hidden states by an exact, certified Schur complement."""

    if (
        not isinstance(max_internal, int)
        or isinstance(max_internal, bool)
        or max_internal < 0
    ):
        raise ValueError("max_internal must be a nonnegative integer.")
    response, source = _validate_request(request)
    state_kind = request.variables[0].state_kind
    declared = tuple(variable.symbol for variable in request.variables)
    positions = {symbol: index for index, symbol in enumerate(declared)}
    boundary_indices = [positions[symbol] for symbol in request.boundary_symbols]
    internal_indices = [positions[symbol] for symbol in request.internal_symbols]

    common = {
        "area": request.area,
        "state_kind": state_kind,
        "boundary_symbols": request.boundary_symbols,
        "internal_symbols": request.internal_symbols,
        "provenance": request.provenance,
    }
    boundary_response = response.extract(boundary_indices, boundary_indices)
    boundary_source = source.extract(boundary_indices, [0])
    if not internal_indices:
        return NetworkCondensationResult(
            status="irreducible",
            condensed_matrix=_matrix_tuple(boundary_response),
            condensed_source=_vector_tuple(boundary_source),
            obstruction=NetworkObstruction(
                "no_internal_variables",
                "The packet has no hidden state to eliminate.",
            ),
            **common,
        )
    if len(internal_indices) > max_internal:
        return NetworkCondensationResult(
            status="refused",
            obstruction=NetworkObstruction(
                "internal_budget_exceeded",
                "The hidden-state count exceeds the declared exact-elimination budget.",
            ),
            **common,
        )

    boundary_internal = response.extract(boundary_indices, internal_indices)
    internal_boundary = response.extract(internal_indices, boundary_indices)
    internal_response = response.extract(internal_indices, internal_indices)
    internal_source = source.extract(internal_indices, [0])
    determinant = simplify(internal_response.det())
    if determinant.is_zero is True:
        return NetworkCondensationResult(
            status="refused",
            obstruction=NetworkObstruction(
                "internal_block_singular",
                "The hidden-state block is singular, so recovery is not unique.",
            ),
            **common,
        )
    if determinant.is_zero is None:
        return NetworkCondensationResult(
            status="refused",
            obstruction=NetworkObstruction(
                "internal_invertibility_undetermined",
                "Hidden-block invertibility is not established by the assumptions.",
            ),
            **common,
        )

    inverse = internal_response.inv()
    recovery_matrix = (-(inverse * internal_boundary)).applyfunc(simplify)
    recovery_offset = (inverse * internal_source).applyfunc(simplify)
    condensed_response = (
        boundary_response + boundary_internal * recovery_matrix
    ).applyfunc(simplify)
    condensed_source = (
        boundary_source - boundary_internal * recovery_offset
    ).applyfunc(simplify)
    certificates = (
        Certificate(
            name="hidden_balance_recovery",
            passed=_zero_matrix(internal_boundary + internal_response * recovery_matrix)
            and _zero_matrix(internal_response * recovery_offset - internal_source),
            witness="substitution of the affine recovery map satisfies the hidden block",
        ),
        Certificate(
            name="boundary_law_return",
            passed=_zero_matrix(
                boundary_response
                + boundary_internal * recovery_matrix
                - condensed_response
            )
            and _zero_matrix(
                boundary_source - boundary_internal * recovery_offset - condensed_source
            ),
            witness="substitution returns the stated boundary response and source",
        ),
        Certificate(
            name="semantic_partition_preserved",
            passed=set(request.boundary_symbols).isdisjoint(request.internal_symbols)
            and all(
                variable.state_kind == state_kind for variable in request.variables
            ),
            witness="observable and hidden symbols remain disjoint under one state kind",
        ),
    )
    if not all(certificate.passed for certificate in certificates):
        return NetworkCondensationResult(
            status="refused",
            obstruction=NetworkObstruction(
                "certificate_failed",
                "The candidate condensation failed an internal return certificate.",
            ),
            **common,
        )
    return NetworkCondensationResult(
        status="constructed",
        condensed_matrix=_matrix_tuple(condensed_response),
        condensed_source=_vector_tuple(condensed_source),
        reconstruction_matrix=_matrix_tuple(recovery_matrix),
        reconstruction_offset=_vector_tuple(recovery_offset),
        certificates=certificates,
        **common,
    )

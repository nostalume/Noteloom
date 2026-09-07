"""Generate a finite Hamiltonian departure from matter--boson action terms."""

from __future__ import annotations

from dataclasses import dataclass

from sympy import ImmutableMatrix, sqrt, sympify, zeros
from sympy.matrices import MatrixBase

from .rewrite import Refusal


@dataclass(frozen=True)
class FockState:
    matter: str
    occupations: tuple[int, ...]


@dataclass(frozen=True)
class MatterBosonVertex:
    source_matter: str
    target_matter: str
    mode: int
    action: str
    coefficient: object
    origin: str


@dataclass(frozen=True)
class DepartureRequest:
    preparations: tuple[FockState, ...]
    channels: tuple[FockState, ...]
    vertices: tuple[MatterBosonVertex, ...]
    provenance: str
    resource_budget: int


@dataclass(frozen=True)
class DepartureCompilation:
    departure: MatrixBase | None = None
    bose_factors: tuple[object, ...] = ()
    applied_origins: tuple[str, ...] = ()
    resource_cost: int = 0
    closed: bool = False
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def _refuse(
    request: DepartureRequest,
    reason: str,
    residual: tuple = (),
) -> DepartureCompilation:
    return DepartureCompilation(refusal=Refusal(
        reason,
        residual=residual,
        provenance=request.provenance,
    ))


def _validate_basis(
    request: DepartureRequest,
) -> tuple[int, DepartureCompilation | None]:
    if not request.preparations:
        return 0, _refuse(request, "preparation basis is empty")
    if not request.channels:
        return 0, _refuse(request, "channel basis is empty")
    if len(set(request.preparations)) != len(request.preparations):
        return 0, _refuse(request, "preparation basis contains duplicates")
    if len(set(request.channels)) != len(request.channels):
        return 0, _refuse(request, "channel basis contains duplicates")
    if set(request.preparations) & set(request.channels):
        return 0, _refuse(request, "retained and channel bases overlap")

    states = request.preparations + request.channels
    mode_count = len(states[0].occupations)
    if any(len(state.occupations) != mode_count for state in states):
        return 0, _refuse(request, "occupation tuples have inconsistent lengths")
    if any(
        not isinstance(number, int) or isinstance(number, bool) or number < 0
        for state in states
        for number in state.occupations
    ):
        return 0, _refuse(request, "occupations must be nonnegative integers")
    return mode_count, None


def compile_departure(request: DepartureRequest) -> DepartureCompilation:
    mode_count, invalid = _validate_basis(request)
    if invalid is not None:
        return invalid

    for vertex in request.vertices:
        if vertex.action not in {"create", "annihilate"}:
            return _refuse(request, "vertex action is not supported", (vertex.origin,))
        if not 0 <= vertex.mode < mode_count:
            return _refuse(
                request,
                "vertex mode lies outside the occupation basis",
                (vertex.origin, vertex.mode),
            )

    resource_cost = (
        len(request.preparations) * len(request.vertices)
        + len(request.preparations) * len(request.channels)
    )
    if resource_cost > request.resource_budget:
        return _refuse(
            request,
            "departure compilation budget exceeded",
            (resource_cost, request.resource_budget),
        )

    channel_rows = {state: row for row, state in enumerate(request.channels)}
    retained = set(request.preparations)
    departure = zeros(len(request.channels), len(request.preparations))
    factors: list[object] = []
    origins: list[str] = []
    for column, state in enumerate(request.preparations):
        for vertex in request.vertices:
            coefficient = sympify(vertex.coefficient)
            if vertex.source_matter != state.matter or coefficient == 0:
                continue
            occupations = list(state.occupations)
            population = occupations[vertex.mode]
            if vertex.action == "annihilate":
                if population == 0:
                    continue
                occupations[vertex.mode] -= 1
                factor = sqrt(population)
            else:
                occupations[vertex.mode] += 1
                factor = sqrt(population + 1)
            target = FockState(vertex.target_matter, tuple(occupations))
            if target in retained:
                continue
            if target not in channel_rows:
                return _refuse(
                    request,
                    "channel basis omits a generated state",
                    (vertex.origin, target),
                )
            departure[channel_rows[target], column] += coefficient * factor
            factors.append(factor)
            origins.append(vertex.origin)

    if departure == zeros(*departure.shape):
        return _refuse(request, "interaction generates no departure")
    return DepartureCompilation(
        departure=ImmutableMatrix(departure),
        bose_factors=tuple(factors),
        applied_origins=tuple(origins),
        resource_cost=resource_cost,
        closed=True,
    )

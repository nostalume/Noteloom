from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, NamedTuple


@dataclass(frozen=True, slots=True)
class Certificate:
    name: str
    passed: bool
    witness: str


@dataclass(frozen=True, slots=True)
class Obstruction:
    code: str
    message: str
    fields: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RouteStep:
    operation: str
    witness: str


@dataclass(frozen=True, slots=True)
class CompilationResult:
    status: str
    adapter: str | None = None
    value: Mapping[str, Any] = field(default_factory=dict)
    route: tuple[RouteStep, ...] = ()
    certificates: tuple[Certificate, ...] = ()
    obstruction: Obstruction | None = None


class ParameterizedHeader(NamedTuple):
    objects: frozenset[str]
    observable: Any
    parameters: Any


def solved(
    adapter: str,
    value: Mapping[str, Any],
    route: tuple[RouteStep, ...],
    certificates: tuple[Certificate, ...],
) -> CompilationResult:
    return CompilationResult(
        status="solved",
        adapter=adapter,
        value=value,
        route=route,
        certificates=certificates,
    )


def refused(adapter: str | None, obstruction: Obstruction) -> CompilationResult:
    return CompilationResult(
        status="refused",
        adapter=adapter,
        obstruction=obstruction,
    )

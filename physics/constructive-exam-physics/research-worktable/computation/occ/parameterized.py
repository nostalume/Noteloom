from collections.abc import Mapping
from typing import Any

from ._parameterized_contracts import (
    CompilationResult,
    Obstruction,
    ParameterizedHeader,
    refused,
)


def _no_adapter() -> CompilationResult:
    return refused(
        None,
        Obstruction(
            "no_adapter", "No adapter supports the supplied objects and observable."
        ),
    )


def compile_problem(problem: Mapping[str, Any]) -> CompilationResult:
    """Admit once, select one fixed owner, and return its result directly."""
    header = ParameterizedHeader(
        frozenset(problem.get("objects", ())),
        problem.get("observable"),
        problem.get("parameters", {}),
    )
    match header.observable:
        case "signed_surface_height_difference":
            from .free_surface import admit, solve
        case "zeeman_line_shifts":
            from .zeeman import admit, solve
        case "rms_current_density_ratio" | "crossover_angular_frequency":
            from .harmonic_current import admit, solve
        case "phonon_mode_count" | "constant_volume_heat_capacity":
            from .phonon import admit, solve
        case _:
            return _no_adapter()
    request = admit(header)
    return _no_adapter() if request is None else solve(request)

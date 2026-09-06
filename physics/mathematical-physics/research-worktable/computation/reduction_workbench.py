"""Common executable envelope for heterogeneous reduction certificates.

The scientific backends keep ownership of their mathematics.  This module owns
only the shared request, outcome, witness, cost, and refusal vocabulary needed
to compare them without flattening their route-specific evidence.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path

from cyclic_reduce import AdmissibilityError, reduce_symmetric_matrix
from oscillator_cross_probe import build_cross_probe
from problem_router import discover_problem

SCHEMA = "reduction-witness/v1"
Backend = Callable[[Path, str], dict[str, object]]


def _request(backend: str, path: Path, observable: str) -> dict[str, object]:
    return {
        "backend": backend,
        "input": str(path),
        "observable": observable,
    }


def _obstruction(
    backend: str,
    path: Path,
    observable: str,
    *,
    kind: str,
    reason: str,
    detail: object | None = None,
) -> dict[str, object]:
    result: dict[str, object] = {
        "schema": SCHEMA,
        "backend": backend,
        "outcome": "obstructed",
        "request": _request(backend, path, observable),
        "witness": None,
        "decision": {"selected_route": None, "reason": reason},
        "obstruction": {"kind": kind, "reason": reason},
    }
    if detail is not None:
        result["detail"] = detail
    return result


def _factor_centralizer(path: Path, observable: str) -> dict[str, object]:
    raw = build_cross_probe(path)
    if raw.get("status") != "ExactCrossProbeSelection":
        return _obstruction(
            "factor-centralizer",
            path,
            observable,
            kind="BackendRefusal",
            reason=str(raw.get("reason", raw.get("status", "unknown refusal"))),
            detail=raw,
        )

    checks = raw["coincidence_checks"]
    assert isinstance(checks, dict)
    selected = str(raw["selected_route"])
    selected_witness = raw[f"{selected}_witness"]
    return {
        "schema": SCHEMA,
        "backend": "factor-centralizer",
        "outcome": "exact",
        "request": _request("factor-centralizer", path, observable),
        "witness": {
            "preserved_object": observable,
            "construction": "independent factor and filtered-centralizer routes",
            "reduced_object": {
                "kind": "primitive normal-mode projectors",
                "dimension": len(selected_witness["mode_projectors"]),
            },
            "maps": {
                "analysis": selected_witness["analysis"],
                "synthesis": selected_witness["synthesis"],
            },
            "residuals": {"all_passed": all(checks.values()), "checks": checks},
            "error": {"kind": "exact", "bound": 0},
            "cost": raw["cost_comparison"],
            "validity": raw["input"],
        },
        "decision": {
            "selected_route": selected,
            "reason": raw["selection_reason"],
        },
        "limitations": raw["not_certified"],
        "detail": raw,
    }


def _cyclic(path: Path, observable: str) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        reduction = reduce_symmetric_matrix(
            payload["matrix"],
            payload["preparation"],
            metric=payload.get("metric"),
            budget=payload.get("budget"),
            time_horizon=payload.get("time_horizon"),
            tolerance=payload.get("tolerance"),
        )
    except (AdmissibilityError, KeyError, OSError, json.JSONDecodeError) as error:
        return _obstruction(
            "cyclic",
            path,
            observable,
            kind="BackendRefusal",
            reason=str(error),
        )

    raw = reduction.to_dict()
    outcome = {
        "ExactCyclicReduction": "exact",
        "ControlledCyclicReduction": "controlled",
        "FormalTruncation": "formal",
    }[reduction.status]
    truncation = raw["truncation"]
    residual_keys = (
        "orthogonal_basis",
        "three_term_recurrence",
        "reduced_metric_self_adjoint",
        "moment_recovery",
    )
    return {
        "schema": SCHEMA,
        "backend": "cyclic",
        "outcome": outcome,
        "request": _request("cyclic", path, observable),
        "witness": {
            "preserved_object": observable,
            "construction": "observable-generated orthogonal Krylov recurrence",
            "reduced_object": {
                "kind": "finite Jacobi recurrence",
                "dimension": reduction.carrier_dimension,
                "ambient_dimension": reduction.ambient_dimension,
            },
            "maps": raw["analysis_synthesis"],
            "residuals": {
                "all_passed": all(raw["certificates"][key] is True for key in residual_keys),
                "checks": raw["certificates"],
            },
            "error": {
                "kind": "exact" if outcome == "exact" else "finite-time bound",
                "bound_squared": truncation["error_bound_squared"],
                "time_horizon": truncation["time_horizon"],
                "tolerance": truncation["tolerance"],
            },
            "cost": raw["costs"],
            "validity": raw["validity"],
        },
        "decision": {
            "selected_route": "cyclic",
            "reason": raw["dimension_verdict"],
        },
        "limitations": [raw["ambiguity"]],
        "detail": raw,
    }


def _stratified_orbit(path: Path, observable: str) -> dict[str, object]:
    # Keep the exact symbolic backends dependency-free.  Numerical orbit
    # reduction owns NumPy/SciPy and loads only when this route is requested.
    from warped_axis_quotient_pde import build_warped_axis_comparison

    raw = build_warped_axis_comparison(path)
    status = raw.get("status")
    if status in {"AxisRegularityObstruction", "Refused"}:
        return _obstruction(
            "stratified-orbit",
            path,
            observable,
            kind=str(status),
            reason=str(raw.get("reason", status)),
            detail=raw,
        )
    if status == "UnresolvedAccuracyWithinBudget":
        outcome = "unresolved"
    elif status == "StratifiedBoundaryQuotientComparison":
        outcome = "controlled"
    else:
        return _obstruction(
            "stratified-orbit",
            path,
            observable,
            kind="BackendRefusal",
            reason=f"unrecognized backend status: {status}",
            detail=raw,
        )

    route = raw["route_evaluation"]
    reduction = raw["reduction_witness"]
    residual_values = [
        reduction["analysis_residual"],
        reduction["synthesis_residual"],
        reduction["full_vs_reconstructed_relative_l2"],
    ]
    return {
        "schema": SCHEMA,
        "backend": "stratified-orbit",
        "outcome": outcome,
        "request": _request("stratified-orbit", path, observable),
        "witness": {
            "preserved_object": observable,
            "construction": "joint operator-domain stabilizer and isotropy-stratified quotient",
            "reduced_object": {
                "kind": "source-visible quotient PDE sectors",
                "weights": raw["sector_selection"]["active_abs_weights"],
            },
            "maps": {
                "analysis": "SO(2) character projection",
                "synthesis": "Fourier reconstruction",
            },
            "residuals": {
                "all_passed": all(value <= route["accuracy_target"] for value in residual_values),
                "analysis": reduction["analysis_residual"],
                "synthesis": reduction["synthesis_residual"],
                "reconstruction": reduction["full_vs_reconstructed_relative_l2"],
            },
            "error": {
                "kind": "fixed continuum accuracy comparison",
                "tolerance": route["accuracy_target"],
            },
            "cost": {
                "full": raw["full_3d_route"]["measured_cost"],
                "reduced": raw["quotient_sector_route"]["measured_cost"],
                "solved_dof_ratio": route["solved_dof_ratio"],
                "nonzero_ratio": route["nonzero_ratio"],
            },
            "validity": {
                "symmetry": raw["symmetry_discovery"],
                "boundary": raw["physical_boundary"],
                "stratification": raw["orbit_stratification"],
            },
        },
        "decision": {
            "selected_route": "stratified-orbit" if outcome == "controlled" else None,
            "reason": route["decision"],
        },
        "limitations": raw["not_certified"],
        "detail": raw,
    }


_BACKENDS: Mapping[str, Backend] = {
    "cyclic": _cyclic,
    "factor-centralizer": _factor_centralizer,
    "stratified-orbit": _stratified_orbit,
}

_OBSERVABLES: Mapping[str, tuple[str, ...]] = {
    "cyclic": ("preparation spectral response", "finite-time survival amplitude"),
    "factor-centralizer": ("full discrete spectrum and heat trace",),
    "stratified-orbit": ("Dirichlet solution at fixed relative L2 accuracy",),
}


def available_backends() -> tuple[str, ...]:
    """Return canonical backend names in stable order."""

    return tuple(sorted(_BACKENDS))


def run_request(request: Mapping[str, object]) -> dict[str, object]:
    """Run one typed request and return the common witness envelope."""

    backend = str(request.get("backend", ""))
    path = Path(request.get("input", ""))
    observable = str(request.get("observable", "unspecified observable"))
    operation = _BACKENDS.get(backend)
    if operation is None:
        return _obstruction(
            backend,
            path,
            observable,
            kind="UnknownBackend",
            reason=f"unknown backend {backend!r}; choose one of {', '.join(available_backends())}",
        )
    supported = _OBSERVABLES[backend]
    if observable == "unspecified observable":
        observable = supported[0]
    elif observable not in supported:
        return _obstruction(
            backend,
            path,
            observable,
            kind="UnsupportedObservable",
            reason=(
                f"backend {backend!r} does not recover {observable!r}; "
                f"supported: {', '.join(supported)}"
            ),
        )
    return operation(path, observable)


def _summary(result: Mapping[str, object]) -> dict[str, object]:
    return {key: result[key] for key in ("backend", "decision", "outcome", "schema", "witness")}


def _discovery_summary(result: Mapping[str, object]) -> dict[str, object]:
    return {
        key: result[key]
        for key in ("coincidence", "decision", "human_card", "outcome", "probes", "schema")
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("backend", choices=("discover", *available_backends()))
    parser.add_argument("input", type=Path)
    parser.add_argument("--observable", default="unspecified observable")
    parser.add_argument("--summary", action="store_true")
    arguments = parser.parse_args(argv)
    if arguments.backend == "discover":
        result = discover_problem(arguments.input)
        rendered = _discovery_summary(result) if arguments.summary else result
    else:
        result = run_request(
            {
                "backend": arguments.backend,
                "input": arguments.input,
                "observable": arguments.observable,
            }
        )
        rendered = _summary(result) if arguments.summary else result
    print(json.dumps(rendered, indent=2, sort_keys=True))
    return {"exact": 0, "controlled": 0, "formal": 0, "obstructed": 2, "unresolved": 3}[
        str(result["outcome"])
    ]


if __name__ == "__main__":
    raise SystemExit(main())

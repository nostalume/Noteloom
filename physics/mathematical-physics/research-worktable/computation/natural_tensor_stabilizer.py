"""Natural-tensor stabilizer and elasticity use witness without a group label."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

import tensor_seed_compression as seed
from linear_defect_compiler import DefectBudget, compile_defects
from natural_relation_planner import (
    RouteAdmission,
    admit_route,
    materialize_route,
    plan_tensor_relations,
    planning_json,
    quotient_audit,
)
from natural_tensor_input import exact_fraction, exact_vector, parse_natural_tensor_input
from problem_input import ProblemDocument, ProblemInputError, load_problem
from tensor_seed_compression import Matrix


def _identity(dimension: int) -> Matrix:
    return tuple(
        tuple(Fraction(row == column) for column in range(dimension)) for row in range(dimension)
    )


def _elasticity_use(
    use: object,
    metric: Matrix,
    lam: Fraction,
    mu: Fraction,
    stabilizer_cost: int,
    planning_cost: int,
) -> dict[str, object]:
    dimension = len(metric)
    if metric != _identity(dimension):
        raise ValueError("the frozen elasticity use witness requires the Euclidean metric")
    if not isinstance(use, dict) or use.get("kind") != "elastic_plane_wave_propagator":
        raise ValueError("use.kind must be elastic_plane_wave_propagator")
    wave = exact_vector(use.get("wave_covector"), dimension, "use.wave_covector")
    preparation = exact_vector(use.get("preparation"), dimension, "use.preparation")
    probe = exact_vector(use.get("probe"), dimension, "use.probe")
    time = exact_fraction(use.get("time"), "use.time")
    tolerance = exact_fraction(use.get("tolerance"), "use.tolerance")
    if not any(wave) or time < 0 or tolerance <= 0:
        raise ValueError(
            "wave covector, time, and tolerance must define a nonzero positive use case"
        )

    norm_squared = sum((value * value for value in wave), Fraction(0))
    longitudinal = tuple(
        tuple(wave[row] * wave[column] / norm_squared for column in range(dimension))
        for row in range(dimension)
    )
    transverse = seed.add(_identity(dimension), seed.scale(longitudinal, Fraction(-1)))
    transverse_eigenvalue = mu * norm_squared
    longitudinal_eigenvalue = (lam + 2 * mu) * norm_squared
    symbol = seed.add(
        seed.scale(_identity(dimension), transverse_eigenvalue),
        seed.scale(longitudinal, longitudinal_eigenvalue - transverse_eigenvalue),
    )
    zero = tuple(tuple(Fraction(0) for _ in range(dimension)) for _ in range(dimension))
    projector_checks = (
        seed.multiply(longitudinal, longitudinal) == longitudinal,
        seed.multiply(transverse, transverse) == transverse,
        seed.multiply(longitudinal, transverse) == zero,
        seed.add(longitudinal, transverse) == _identity(dimension),
        seed.multiply(symbol, longitudinal) == seed.scale(longitudinal, longitudinal_eigenvalue),
        seed.multiply(symbol, transverse) == seed.scale(transverse, transverse_eigenvalue),
    )

    symbol_float = np.array([[float(value) for value in row] for row in symbol], dtype=float)
    eigenvalues, eigenvectors = np.linalg.eigh(symbol_float)
    full_propagator = (
        eigenvectors @ np.diag(np.cos(float(time) * np.sqrt(eigenvalues))) @ eigenvectors.T
    )
    longitudinal_float = np.array(
        [[float(value) for value in row] for row in longitudinal], dtype=float
    )
    transverse_float = np.eye(dimension) - longitudinal_float
    reduced_propagator = (
        math.cos(float(time) * math.sqrt(float(transverse_eigenvalue))) * transverse_float
        + math.cos(float(time) * math.sqrt(float(longitudinal_eigenvalue))) * longitudinal_float
    )
    preparation_float = np.array([float(value) for value in preparation])
    probe_float = np.array([float(value) for value in probe])
    baseline_observable = float(probe_float @ full_propagator @ preparation_float)
    reduced_observable = float(probe_float @ reduced_propagator @ preparation_float)
    error = abs(baseline_observable - reduced_observable)
    if not all(projector_checks):
        raise ArithmeticError("elasticity projector certificate failed")

    baseline_per_query = dimension**3
    reduced_per_query = dimension**2 + 2
    saving = baseline_per_query - reduced_per_query
    total_cost = stabilizer_cost + planning_cost
    break_even = math.ceil(total_cost / saving) if saving > 0 else None
    return {
        "kind": "controlled plane-wave propagator matrix element",
        "wave_covector": [str(value) for value in wave],
        "symbol": seed.matrix_json(symbol),
        "projectors": {
            "transverse": seed.matrix_json(transverse),
            "longitudinal": seed.matrix_json(longitudinal),
        },
        "channel_dimensions": {"transverse": dimension - 1, "longitudinal": 1},
        "eigenvalues": {
            "transverse": str(transverse_eigenvalue),
            "longitudinal": str(longitudinal_eigenvalue),
        },
        "maps": {
            "analysis": "u -> (P_T u, P_L u)",
            "synthesis": "(u_T,u_L) -> u_T+u_L",
        },
        "exact_projector_checks_passed": all(projector_checks),
        "baseline_observable": baseline_observable,
        "reduced_observable": reduced_observable,
        "observable_error": error,
        "tolerance": float(tolerance),
        "cost": {
            "model": "dense-eigensolve versus generated two-projector arithmetic proxy",
            "one_time_stabilizer_proxy": stabilizer_cost,
            "one_time_relation_planning_proxy": planning_cost,
            "one_time_selected_route_proxy": total_cost,
            "stabilizer_only_break_even_query_count": (
                math.ceil(stabilizer_cost / saving) if saving > 0 else None
            ),
            "baseline_per_wavevector_proxy": baseline_per_query,
            "reduced_per_wavevector_proxy": reduced_per_query,
            "break_even_query_count": break_even,
            "runtime_dominance_measured": False,
        },
    }


def _result_from_payload(payload: dict[str, object]) -> dict[str, object]:
    parsed = parse_natural_tensor_input(payload)
    metric = parsed.metric
    tensors = parsed.tensors
    elasticity_parameters = parsed.elasticity_parameters

    raw_budget = payload.get("resource_budget")
    if not isinstance(raw_budget, dict):
        raise ValueError("resource_budget is required")
    budget_values = []
    for name in (
        "maximum_candidate_dimension",
        "maximum_residual_coordinates",
        "maximum_bracket_checks",
    ):
        value = raw_budget.get(name)
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"resource_budget.{name} must be an integer")
        budget_values.append(value)
    budget = DefectBudget(*budget_values)
    planning = plan_tensor_relations(tensors)
    plans = {route.route: route for route in planning.routes}
    admissions = {
        route.route: (
            admit_route(route, budget)
            if route.outcome == "planned"
            else RouteAdmission("rejected", route.obstruction_kind, route.obstruction_reason)
        )
        for route in planning.routes
    }
    admitted = tuple(
        route for route in planning.routes if admissions[route.route].outcome == "admitted"
    )
    audit = payload.get("audit_raw_comparison", False)
    if not isinstance(audit, bool):
        raise ValueError("audit_raw_comparison must be boolean")
    if not admitted:
        failed = admissions.get(
            "natural-tensor-structured-seed",
            admissions["natural-tensor-raw-endomorphism"],
        )
        return {
            "schema": "reduction-decision/v1",
            "outcome": failed.outcome,
            "request": {"problem_type": payload["schema"], "supplied_group_name": False},
            "probes": [],
            "candidates": [
                {
                    "route": route.route,
                    "outcome": admissions[route.route].outcome,
                    "candidate_dimension": route.candidate_dimension,
                    "target_dimensions": [target.dimension for target in route.targets],
                    "obstruction": {
                        "kind": admissions[route.route].obstruction_kind,
                        "reason": admissions[route.route].obstruction_reason,
                    },
                }
                for route in planning.routes
            ],
            "coincidence": None,
            "decision": {"selected_route": None},
            "relation_plan": planning_json(
                planning,
                None,
                "selected-route-only-after-symbolic-admission",
                admissions,
                (),
            ),
            "obstruction": {
                "kind": failed.obstruction_kind,
                "reason": failed.obstruction_reason,
            },
            "human_card": {
                "result": failed.outcome,
                "why": failed.obstruction_reason,
            },
        }
    selected_plan = next(
        (route for route in admitted if route.route == planning.preferred_route),
        min(admitted, key=lambda route: route.estimated_total_cost or 10**30),
    )
    selected_route = selected_plan.route
    execute = [selected_plan]
    raw_plan = plans["natural-tensor-raw-endomorphism"]
    if audit and admissions[raw_plan.route].outcome == "admitted" and raw_plan not in execute:
        execute.append(raw_plan)
    materialized = {route.route: materialize_route(route) for route in execute}
    compilations = {
        route.route: compile_defects(
            candidate_labels=materialized[route.route].candidate_labels,
            blocks=materialized[route.route].blocks,
            visible_action=materialized[route.route].visible_action,
            bracket=materialized[route.route].bracket,
            budget=budget,
        )
        for route in execute
    }
    selected_material = materialized[selected_route]
    selected_candidates = selected_material.candidates
    selected_blocks = selected_material.blocks
    compilation = compilations[selected_route]
    if compilation.outcome != "exact":
        raise ArithmeticError(compilation.obstruction_reason or "selected route failed")
    stabilizer_cost = (
        len(selected_candidates) * sum(len(block.target_labels) for block in selected_blocks)
        + compilation.bracket_checks
    )
    generator_spans = "raw_not_executed"
    quotient_status = "not-audited"
    quotient_checks = 0
    if audit and selected_plan.candidate_kind == "metric-kernel":
        quotient_ok, quotient_checks = quotient_audit(selected_plan)
        if not quotient_ok:
            raise ArithmeticError("compositional and orbit quotient coordinates differ")
        quotient_status = "exact_equal_to_orbit_audit"
    raw_compilation = compilations.get(raw_plan.route)
    if (
        selected_plan.candidate_kind == "metric-kernel"
        and raw_compilation is not None
        and raw_compilation.outcome == "exact"
    ):
        raw_generators = seed.generated_vectors(
            raw_compilation.kernel_basis, materialized[raw_plan.route].candidates
        )
        structured_generators = seed.generated_vectors(
            compilation.kernel_basis, selected_candidates
        )
        if not seed.same_span(raw_generators, structured_generators):
            raise ArithmeticError("raw and structured stabilizer spans differ")
        generator_spans = "exact_equal"

    tensor_rank_drops = [entry.rank_drop for entry in compilation.ledger]
    use_witness = None
    outcome = "exact"
    if payload.get("use") is not None:
        if elasticity_parameters is None:
            raise ValueError(
                "elastic_plane_wave_propagator requires an isotropic elasticity tensor"
            )
        use_witness = _elasticity_use(
            payload["use"],
            metric,
            *elasticity_parameters,
            stabilizer_cost,
            selected_plan.planning_cost,
        )
        outcome = "controlled"

    return {
        "schema": "reduction-decision/v1",
        "outcome": outcome,
        "request": {
            "problem_type": payload["schema"],
            "supplied_group_name": False,
            "supplied_lie_algebra_name": False,
            "supplied_stabilizer_basis": False,
            "supplied_projectors": False,
        },
        "probes": [
            {
                "route": "typed-natural-relation-planner",
                "applicable": True,
                "first_residual": None,
            }
        ],
        "candidates": [
            {
                "route": route.route,
                "outcome": (
                    outcome
                    if route.route == selected_route
                    else (
                        compilations[route.route].outcome
                        if route.route in compilations
                        else admissions[route.route].outcome
                    )
                ),
                "candidate_dimension": route.candidate_dimension,
                "target_dimensions": [target.dimension for target in route.targets],
                "cost_proxy": route.estimated_cost,
                "obstruction": (
                    None
                    if admissions[route.route].outcome == "admitted"
                    else {
                        "kind": admissions[route.route].obstruction_kind,
                        "reason": admissions[route.route].obstruction_reason,
                    }
                ),
            }
            for route in planning.routes
        ],
        "coincidence": {
            "status": ("controlled_same_observable" if use_witness is not None else "exact_action"),
            "generator_spans": generator_spans,
            "quotient_coordinates": quotient_status,
            "quotient_audit_checks": quotient_checks,
            "all_passed": (
                use_witness is None or use_witness["observable_error"] <= use_witness["tolerance"]
            ),
        },
        "relation_plan": planning_json(
            planning,
            selected_route,
            (
                "selected-plus-explicit-raw-span-audit"
                if audit
                else "selected-route-only-after-symbolic-admission"
            ),
            admissions,
            tuple(materialized),
        ),
        "decision": {
            "selected_route": selected_route,
            "candidate_dimension": len(selected_candidates),
            "raw_candidate_dimension": raw_plan.candidate_dimension,
            "stabilizer_dimension": compilation.kernel_dimension,
            "effective_dimension": compilation.effective_dimension,
            "stabilizer_closure": compilation.closure_status,
            "tensor_rank_drops": tensor_rank_drops,
            "tensor_blocks": [entry.name for entry in compilation.ledger],
            "structured_target_dimensions": [
                target.dimension for target in plans["natural-tensor-structured-seed"].targets
            ],
            "raw_target_dimensions": [target.dimension for target in raw_plan.targets],
        },
        "constructed_action": {
            "basis_matrices": seed.basis_matrices_json(
                compilation.kernel_basis, selected_candidates
            ),
            "quotient_bracket": [
                [[str(value) for value in bracket] for bracket in row]
                for row in compilation.quotient_bracket_table
            ],
            "bracket_checks": compilation.bracket_checks,
            "ineffective_dimension": len(compilation.ineffective_basis),
        },
        "use_witness": use_witness,
        "human_card": {
            "result": (
                f"{len(selected_candidates)} structurally generated candidates -> "
                f"{compilation.kernel_dimension} tensor-preserving generators"
            ),
            "retained_objects": (
                "metric-kernel seed, tensor-symmetry targets, simultaneous kernel, "
                "quotient bracket, two projectors"
            ),
            "boundary": (
                "finite exact symmetric-power grammar; raw comparison requires audit; "
                "analytic Fourier inversion not claimed"
            ),
        },
    }


def _obstruction(payload: object, error: Exception) -> dict[str, object]:
    problem_type = payload.get("schema") if isinstance(payload, dict) else "unknown"
    return {
        "schema": "reduction-decision/v1",
        "outcome": "obstructed",
        "request": {"problem_type": problem_type},
        "probes": [],
        "candidates": [],
        "coincidence": None,
        "decision": {"selected_route": None},
        "obstruction": {"kind": type(error).__name__, "reason": str(error)},
        "human_card": {"result": "obstructed", "why": str(error)},
    }


def discover_payload(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict):
        return _obstruction(payload, ValueError("ProblemSpec must be a JSON object"))
    try:
        return _result_from_payload(payload)
    except (ArithmeticError, ValueError) as error:
        return _obstruction(payload, error)


def discover_document(document: ProblemDocument) -> dict[str, object]:
    return discover_payload(document.payload)


def discover_problem(path: Path) -> dict[str, object]:
    try:
        return discover_document(load_problem(path))
    except ProblemInputError as error:
        return _obstruction({}, error)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    arguments = parser.parse_args()
    result = discover_problem(arguments.input)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["outcome"] in {"exact", "controlled", "formal"}:
        return 0
    return 2 if result["outcome"] == "obstructed" else 3


if __name__ == "__main__":
    raise SystemExit(main())

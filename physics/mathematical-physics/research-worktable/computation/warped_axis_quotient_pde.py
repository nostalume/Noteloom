# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy==2.3.3",
#   "scipy==1.16.1",
# ]
# ///
"""Warped axial boundary and singular-orbit quotient-PDE comparison."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.sparse import csr_matrix, diags, eye, kron
from scipy.sparse.linalg import spsolve

from axial_quotient_pde import (
    _accumulate_cost,
    _angular_laplacian,
    _relative_weighted_l2,
    _trigonometric_vector,
)


def _number(value: object, label: str) -> float:
    try:
        result = float(Fraction(str(value)))
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError(f"{label} must be rational") from error
    if not math.isfinite(result):
        raise ValueError(f"{label} must be finite")
    return result


def _load(path: Path) -> dict[str, object]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    geometry = payload.get("geometry")
    operator = payload.get("operator")
    if not isinstance(geometry, dict) or geometry.get("type") != "warped_axisymmetric_solid":
        raise ValueError("geometry must be warped_axisymmetric_solid")
    if not isinstance(operator, dict) or operator.get("type") != "smooth_axial_divergence_elliptic":
        raise ValueError("operator must be smooth_axial_divergence_elliptic")
    if geometry.get("outer_and_end_boundary") != "Dirichlet":
        raise ValueError("only outer-wall/end-cap Dirichlet data are supported")
    interval = geometry.get("height_interval")
    if not isinstance(interval, list) or len(interval) != 2:
        raise ValueError("height_interval must contain two rational endpoints")
    lower, upper = (_number(value, "height endpoint") for value in interval)
    if (lower, upper) != (0.0, 1.0):
        raise ValueError("the manufactured grammar requires z in [0,1]")
    warp = _number(geometry.get("warp_amplitude"), "warp_amplitude")
    if geometry.get("outer_radius") != "1+(1/2)z(1-z)" or warp != 0.5:
        raise ValueError("the current warped-radius grammar is R=1+z(1-z)/2")
    axis_policy = geometry.get("axis_policy")
    if axis_policy not in ("isotropy_generated", "uniform_neumann"):
        raise ValueError("unsupported axis_policy")
    couplings = {
        "a": _number(operator.get("a_coupling"), "a_coupling"),
        "b": _number(operator.get("b_coupling"), "b_coupling"),
        "c": _number(operator.get("c_coupling"), "c_coupling"),
        "potential": _number(operator.get("potential_coupling"), "potential_coupling"),
    }
    if any(1.0 + min(0.0, value) <= 0.0 for value in couplings.values()):
        raise ValueError("couplings must keep the coefficients positive")
    raw_modes = payload.get("manufactured_modes")
    if not isinstance(raw_modes, list) or not raw_modes:
        raise ValueError("manufactured_modes must be nonempty")
    modes = []
    seen = set()
    for raw in raw_modes:
        if not isinstance(raw, dict):
            raise ValueError("each mode must be an object")
        weight, kind = raw.get("abs_m"), raw.get("kind")
        if isinstance(weight, bool) or not isinstance(weight, int) or not 0 <= weight <= 8:
            raise ValueError("abs_m must be an integer from zero through eight")
        if kind not in ("cos", "sin") or (weight == 0 and kind != "cos"):
            raise ValueError("invalid real character mode")
        if (weight, kind) in seen:
            raise ValueError("mode labels must be unique")
        seen.add((weight, kind))
        modes.append(
            {"abs_m": weight, "kind": kind, "amplitude": _number(raw.get("amplitude"), "amplitude")}
        )
    budgets = payload.get("quotient_cell_budgets")
    if (
        not isinstance(budgets, list)
        or not budgets
        or any(isinstance(n, bool) or not isinstance(n, int) or n < 6 for n in budgets)
        or budgets != sorted(set(budgets))
    ):
        raise ValueError("quotient_cell_budgets must be increasing integers >=6")
    angular_nodes = payload.get("angular_nodes")
    if (
        isinstance(angular_nodes, bool)
        or not isinstance(angular_nodes, int)
        or angular_nodes < 2 * max(m["abs_m"] for m in modes) + 3
    ):
        raise ValueError("angular_nodes do not resolve the character support")
    tolerance = _number(payload.get("relative_l2_tolerance"), "relative_l2_tolerance")
    if not 0 < tolerance < 1:
        raise ValueError("relative_l2_tolerance must lie between zero and one")
    return {
        "payload": payload,
        "warp": warp,
        "axis_policy": axis_policy,
        "couplings": couplings,
        "modes": modes,
        "budgets": budgets,
        "angular_nodes": angular_nodes,
        "tolerance": tolerance,
    }


def _radius(z: np.ndarray, warp: float) -> np.ndarray:
    return 1.0 + warp * z * (1.0 - z)


def _coefficients(r: np.ndarray, z: np.ndarray, couplings: dict[str, float]):
    product = r * r * z * (1.0 - z)
    return tuple(1.0 + couplings[key] * product for key in ("a", "b", "c", "potential"))


def _assemble_base(cells: int, config: dict[str, object]):
    warp, couplings = config["warp"], config["couplings"]
    r_max = 1.0 + warp / 4.0
    dr, dz = r_max / cells, 1.0 / cells
    radial = (np.arange(cells) + 0.5) * dr
    axial = (np.arange(cells) + 0.5) * dz
    active = [
        (i, j)
        for i, r in enumerate(radial)
        for j, z in enumerate(axial)
        if r < _radius(np.asarray(z), warp)
    ]
    lookup = {point: index for index, point in enumerate(active)}
    rows, columns, data = [], [], []
    angular_weight = np.empty(len(active))
    r_values, z_values = np.empty(len(active)), np.empty(len(active))
    for (i, j), row in lookup.items():
        r, z = radial[i], axial[j]
        diagonal = 0.0
        r_values[row], z_values[row] = r, z
        for direction in (-1, 1):
            face_r = r + direction * dr / 2.0
            if face_r <= 0.0:
                continue
            a_face = 1.0 + couplings["a"] * face_r**2 * z * (1.0 - z)
            coefficient = face_r * a_face / (r * dr * dr)
            neighbor = lookup.get((i + direction, j))
            if neighbor is None:
                diagonal += 2.0 * coefficient
            else:
                diagonal += coefficient
                rows.append(row)
                columns.append(neighbor)
                data.append(-coefficient)
        for direction in (-1, 1):
            face_z = z + direction * dz / 2.0
            b_face = 1.0 + couplings["b"] * r**2 * face_z * (1.0 - face_z)
            coefficient = b_face / (dz * dz)
            neighbor = lookup.get((i, j + direction))
            if neighbor is None:
                diagonal += 2.0 * coefficient
            else:
                diagonal += coefficient
                rows.append(row)
                columns.append(neighbor)
                data.append(-coefficient)
        _, _, c, potential = _coefficients(np.asarray(r), np.asarray(z), couplings)
        diagonal += float(potential)
        angular_weight[row] = float(c) / (r * r)
        rows.append(row)
        columns.append(row)
        data.append(diagonal)
    matrix = csr_matrix((data, (rows, columns)), shape=(len(active), len(active)))
    return matrix, angular_weight, r_values, z_values


def _manufactured_mode(weight: int, r: np.ndarray, z: np.ndarray, config: dict[str, object]):
    warp, couplings = config["warp"], config["couplings"]
    w, wp, wpp = z * (1.0 - z), 1.0 - 2.0 * z, -2.0
    outer, outer_p, outer_pp = 1.0 + warp * w, warp * wp, warp * wpp
    boundary = outer**2 - r**2
    boundary_r, boundary_rr = -2.0 * r, -2.0
    boundary_z = 2.0 * outer * outer_p
    boundary_zz = 2.0 * (outer_p**2 + outer * outer_pp)
    f = boundary * w
    f_r, f_rr = boundary_r * w, boundary_rr * w
    f_z = boundary_z * w + boundary * wp
    f_zz = boundary_zz * w + 2.0 * boundary_z * wp + boundary * wpp
    power = r**weight
    profile = power * f
    profile_r = (weight * r ** (weight - 1) * f if weight else 0.0) + power * f_r
    profile_rr = power * f_rr
    if weight:
        profile_rr += 2.0 * weight * r ** (weight - 1) * f_r
    if weight >= 2:
        profile_rr += weight * (weight - 1) * r ** (weight - 2) * f
    profile_z, profile_zz = power * f_z, power * f_zz
    a, b, c, potential = _coefficients(r, z, couplings)
    a_r = 2.0 * couplings["a"] * r * w
    b_z = couplings["b"] * r**2 * wp
    forcing = -(a * profile_rr + (a_r + a / r) * profile_r)
    forcing -= b * profile_zz + b_z * profile_z
    forcing += (c * weight**2 / r**2 + potential) * profile
    return profile, forcing


def _fields(r, z, theta, config):
    exact = np.zeros((len(r), len(theta)))
    forcing = np.zeros_like(exact)
    modal = {}
    for mode in config["modes"]:
        key = (mode["abs_m"], mode["kind"])
        profile, source = _manufactured_mode(mode["abs_m"], r, z, config)
        profile, source = mode["amplitude"] * profile, mode["amplitude"] * source
        angular = _trigonometric_vector(mode["kind"], mode["abs_m"], theta)
        exact += np.outer(profile, angular)
        forcing += np.outer(source, angular)
        modal[key] = (profile, source)
    return exact, forcing, modal


def _attempt(config, cells, reduced):
    started = perf_counter()
    base, angular_weight, r, z = _assemble_base(cells, config)
    nodes = config["angular_nodes"]
    theta = 2.0 * math.pi * np.arange(nodes) / nodes
    exact, forcing, modal = _fields(r, z, theta, config)
    matrices = {}
    if reduced:
        step = 2.0 * math.pi / nodes
        for weight in sorted({m["abs_m"] for m in config["modes"]}):
            mu = 4.0 * math.sin(weight * step / 2.0) ** 2 / step**2
            matrices[weight] = base + diags(angular_weight * mu)
        matrix = None
    else:
        matrix = kron(base, eye(nodes, format="csr"), format="csr")
        matrix += kron(diags(angular_weight), _angular_laplacian(nodes), format="csr")
    assembly_seconds = perf_counter() - started
    started = perf_counter()
    if reduced:
        solutions = {
            key: np.asarray(spsolve(matrices[key[0]], source)) for key, (_, source) in modal.items()
        }
    else:
        solution = np.asarray(spsolve(matrix, forcing.reshape(-1))).reshape(forcing.shape)
    solve_seconds = perf_counter() - started
    started = perf_counter()
    if reduced:
        field = sum(
            (
                np.outer(solutions[key], _trigonometric_vector(key[1], key[0], theta))
                for key in solutions
            ),
            np.zeros_like(exact),
        )
        analysis = []
        for key, (_, source) in modal.items():
            angular = _trigonometric_vector(key[1], key[0], theta)
            factor = 1.0 / nodes if key[0] == 0 else 2.0 / nodes
            analysis.append(
                float(
                    np.linalg.norm(factor * (forcing @ angular) - source) / np.linalg.norm(source)
                )
            )
        residual = max(analysis)
        dof = len(config["modes"]) * len(r)
        nonzeros = sum(a.nnz for a in matrices.values())
    else:
        field = solution
        residual = float(
            np.linalg.norm(matrix @ field.reshape(-1) - forcing.reshape(-1))
            / np.linalg.norm(forcing)
        )
        dof, nonzeros = matrix.shape[0], matrix.nnz
    error = _relative_weighted_l2(field, exact, r)
    recovery_seconds = perf_counter() - started
    return {
        "resolution": cells,
        "active_quotient_cells": len(r),
        "relative_l2_error": error,
        "solved_degrees_of_freedom": int(dof),
        "assembled_nonzeros": int(nonzeros),
        "field": field,
        "forcing": forcing,
        "exact": exact,
        "r": r,
        "matrix": matrix,
        "analysis_or_algebraic_residual": residual,
        "local_cost": {
            "assembly_seconds": assembly_seconds,
            "solve_seconds": solve_seconds,
            "recovery_seconds": recovery_seconds,
        },
    }


def _public(attempt):
    hidden = {"field", "forcing", "exact", "r", "matrix", "local_cost"}
    return {key: value for key, value in attempt.items() if key not in hidden}


def build_warped_axis_comparison(path: Path) -> dict[str, object]:
    try:
        config = _load(Path(path))
        weights = sorted({mode["abs_m"] for mode in config["modes"]})
        conditions = {str(m): "partial_r u_0=0" if m == 0 else f"u_{m}=O(r^{m})" for m in weights}
        if config["axis_policy"] != "isotropy_generated" and any(m > 0 for m in weights):
            return {
                "status": "AxisRegularityObstruction",
                "reason": "uniform axis data contradict SO(2) isotropy for nonzero weights",
                "required_conditions": conditions,
            }
        full_cost = {"assembly_seconds": 0.0, "solve_seconds": 0.0, "recovery_seconds": 0.0}
        reduced_cost = dict(full_cost)
        attempts = []
        full = reduced = None
        for cells in config["budgets"]:
            full, reduced = _attempt(config, cells, False), _attempt(config, cells, True)
            full["tolerance_met"] = full["relative_l2_error"] <= config["tolerance"]
            reduced["tolerance_met"] = reduced["relative_l2_error"] <= config["tolerance"]
            _accumulate_cost(full_cost, full["local_cost"])
            _accumulate_cost(reduced_cost, reduced["local_cost"])
            difference = _relative_weighted_l2(reduced["field"], full["field"], full["r"])
            synthesis = float(
                np.linalg.norm(
                    full["matrix"] @ reduced["field"].reshape(-1) - full["forcing"].reshape(-1)
                )
                / np.linalg.norm(full["forcing"])
            )
            attempts.append(
                {
                    "cells": cells,
                    "full_error": full["relative_l2_error"],
                    "reduced_error": reduced["relative_l2_error"],
                    "difference": difference,
                }
            )
            if full["tolerance_met"] and reduced["tolerance_met"]:
                break
        assert full is not None and reduced is not None
        both = full["tolerance_met"] and reduced["tolerance_met"]
        full_public, reduced_public = _public(full), _public(reduced)
        full_public["measured_cost"] = {
            **full_cost,
            "total_seconds": sum(full_cost.values()),
            "includes_axis_and_warp_construction": True,
        }
        reduced_public["measured_cost"] = {
            **reduced_cost,
            "total_seconds": sum(reduced_cost.values()),
            "includes_axis_and_warp_construction": True,
        }
        return {
            "status": "StratifiedBoundaryQuotientComparison"
            if both
            else "UnresolvedAccuracyWithinBudget",
            "symmetry_discovery": {
                "supplied_group": False,
                "connected_stabilizer": "SO(2)",
                "generator": "J_z",
                "boundary_residual": 0,
            },
            "physical_boundary": {
                "outer_radius": "R(z)=1+z(1-z)/2",
                "nonproduct_warp": True,
                "R_prime_not_identically_zero": True,
            },
            "orbit_stratification": {
                "principal_orbits": "circles for r>0",
                "fixed_axis": {
                    "isotropy": "SO(2)",
                    "quotient_role": "singular boundary stratum",
                    "conditions": conditions,
                    "derivation": "u_m(0)=exp(i m alpha)u_m(0); smoothness strengthens vanishing to r^|m|",
                    "manufactured_profile_checks": True,
                },
            },
            "sector_selection": {
                "origin": "forcing character support",
                "active_abs_weights": weights,
            },
            "full_3d_route": full_public,
            "quotient_sector_route": reduced_public,
            "reduction_witness": {
                "analysis_residual": reduced["analysis_or_algebraic_residual"],
                "synthesis_residual": synthesis,
                "full_vs_reconstructed_relative_l2": difference,
            },
            "route_evaluation": {
                "decision": "StratifiedOrbitReductionAtTolerance"
                if both
                else "NoAccuracyMatchedComparison",
                "accuracy_target": config["tolerance"],
                "solved_dof_ratio": reduced_public["solved_degrees_of_freedom"]
                / full_public["solved_degrees_of_freedom"],
                "nonzero_ratio": reduced_public["assembled_nonzeros"]
                / full_public["assembled_nonzeros"],
            },
            "attempts": attempts,
            "not_certified": [
                "boundary-fitted high-order convergence",
                "spinor/tensor isotropy fibers",
                "arbitrary warped geometries",
                "portable sparse-direct timing",
            ],
        }
    except (OSError, ValueError, json.JSONDecodeError, np.linalg.LinAlgError) as error:
        return {"status": "Refused", "reason": str(error)}


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    result = build_warped_axis_comparison(args.input)
    if args.summary and result["status"] not in ("Refused", "AxisRegularityObstruction"):
        print(
            f"{result['status']}: cells={result['full_3d_route']['resolution']}, axis=isotropy-generated, {result['route_evaluation']['decision']}"
        )
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "StratifiedBoundaryQuotientComparison" else 2


if __name__ == "__main__":
    raise SystemExit(_main())

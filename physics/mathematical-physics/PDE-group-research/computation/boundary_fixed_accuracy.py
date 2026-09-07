# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy==2.3.3",
#   "scipy==1.16.1",
# ]
# ///
"""Fixed-accuracy boundary spectral comparison.

The continuum observable is the first K Dirichlet-disk eigenvalues with
multiplicity.  A constructed rotation-sector finite-volume route is compared with
a Cartesian five-point sparse partial-spectrum baseline at the same tolerance.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh
from scipy.special import jn_zeros

from boundary_symmetry_reduction import build_boundary_reduction


def _positive_integer_list(value: object, label: str) -> list[int]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a nonempty integer list")
    if any(isinstance(item, bool) or not isinstance(item, int) or item < 3 for item in value):
        raise ValueError(f"{label} must contain integers >=3")
    if value != sorted(set(value)):
        raise ValueError(f"{label} must be strictly increasing")
    return value


def _load(path: Path) -> dict[str, object]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    target = payload.get("target_eigenvalues")
    if isinstance(target, bool) or not isinstance(target, int) or not 1 <= target <= 20:
        raise ValueError("target_eigenvalues must lie between 1 and 20")
    tolerance = Fraction(str(payload.get("relative_tolerance")))
    solver_tolerance = Fraction(str(payload.get("solver_tolerance")))
    if not 0 < tolerance < 1:
        raise ValueError("relative_tolerance must lie between 0 and 1")
    if not 0 < solver_tolerance < tolerance:
        raise ValueError("solver_tolerance must be positive and smaller than the target tolerance")
    radial = _positive_integer_list(payload.get("radial_cell_budgets"), "radial_cell_budgets")
    cartesian = _positive_integer_list(
        payload.get("cartesian_interval_budgets"), "cartesian_interval_budgets"
    )
    boundary_name = payload.get("boundary_problem")
    if not isinstance(boundary_name, str):
        raise ValueError("boundary_problem must be a relative JSON path")
    boundary_path = (Path(path).parent / boundary_name).resolve()
    boundary = build_boundary_reduction(boundary_path)
    if boundary.get("status") != "ExactBoundaryCompatibleReduction":
        raise ValueError("fixed-accuracy probe requires the certified unit-disk reduction")
    return {
        "payload": payload,
        "target": target,
        "tolerance": float(tolerance),
        "solver_tolerance": float(solver_tolerance),
        "radial_budgets": radial,
        "cartesian_budgets": cartesian,
        "boundary_certificate": boundary,
    }


def _continuum_reference(target: int) -> tuple[list[float], list[dict[str, int]]]:
    candidates: list[tuple[float, int, int, int]] = []
    weight = 0
    while True:
        zeros = jn_zeros(weight, target)
        for radial_index, zero in enumerate(zeros, start=1):
            value = float(zero * zero)
            candidates.append((value, weight, radial_index, 1))
            if weight:
                candidates.append((value, weight, radial_index, 2))
        selected = sorted(candidates)[:target]
        if len(selected) == target and (weight + 1) ** 2 > selected[-1][0]:
            break
        weight += 1
        if weight > 4 * target + 8:
            raise RuntimeError("continuum reference frontier did not terminate")
    return (
        [item[0] for item in selected],
        [
            {
                "abs_m": item[1],
                "radial_index": item[2],
                "multiplicity_copy": item[3],
            }
            for item in selected
        ],
    )


def _radial_tridiagonal(weight: int, cells: int) -> tuple[np.ndarray, np.ndarray]:
    """Cell-centered finite volume for -4(s^(m+1)v')'=lambda*s^m*v."""

    step = 1.0 / cells
    mass = np.empty(cells)
    for index in range(cells):
        left = index * step
        right = (index + 1) * step
        mass[index] = (right ** (weight + 1) - left ** (weight + 1)) / (weight + 1)
    stiffness_diagonal = np.zeros(cells)
    stiffness_off = np.empty(cells - 1)
    for face in range(1, cells):
        coefficient = 4.0 * (face * step) ** (weight + 1) / step
        stiffness_diagonal[face - 1] += coefficient
        stiffness_diagonal[face] += coefficient
        stiffness_off[face - 1] = -coefficient
    stiffness_diagonal[-1] += 8.0 / step
    diagonal = stiffness_diagonal / mass
    off = stiffness_off / np.sqrt(mass[:-1] * mass[1:])
    return diagonal, off


def _tridiagonal_residuals(
    diagonal: np.ndarray,
    off: np.ndarray,
    values: np.ndarray,
    vectors: np.ndarray,
) -> list[float]:
    residuals = []
    for column, value in enumerate(values):
        vector = vectors[:, column]
        applied = diagonal * vector
        applied[:-1] += off * vector[1:]
        applied[1:] += off * vector[:-1]
        residuals.append(float(np.linalg.norm(applied - value * vector) / max(1.0, abs(value))))
    return residuals


def _radial_attempt(cells: int, target: int, solver_tolerance: float) -> dict[str, object]:
    candidates: list[tuple[float, int, int, int, float]] = []
    assembly_seconds = 0.0
    solve_seconds = 0.0
    weight = 0
    scalar_nonzeros = 0
    while True:
        started = perf_counter()
        diagonal, off = _radial_tridiagonal(weight, cells)
        assembly_seconds += perf_counter() - started
        scalar_nonzeros += len(diagonal) + 2 * len(off)
        count = min(target, cells)
        started = perf_counter()
        values, vectors = eigh_tridiagonal(
            diagonal,
            off,
            eigvals_only=False,
            select="i",
            select_range=(0, count - 1),
            tol=solver_tolerance,
            lapack_driver="stebz",
            check_finite=True,
        )
        solve_seconds += perf_counter() - started
        residuals = _tridiagonal_residuals(diagonal, off, values, vectors)
        for radial_index, (value, residual) in enumerate(zip(values, residuals), start=1):
            candidates.append((float(value), weight, radial_index, 1, residual))
            if weight:
                candidates.append((float(value), weight, radial_index, 2, residual))
        selected = sorted(candidates)[:target]
        frontier = len(selected) == target and (weight + 1) ** 2 > selected[-1][0]
        if frontier:
            break
        weight += 1
        if weight > 4 * target + 8:
            raise RuntimeError("radial sector frontier did not terminate")
    recovery_started = perf_counter()
    eigenvalues = [item[0] for item in selected]
    labels = [
        {
            "abs_m": item[1],
            "radial_index": item[2],
            "multiplicity_copy": item[3],
        }
        for item in selected
    ]
    max_residual = max(item[4] for item in selected)
    recovery_seconds = perf_counter() - recovery_started
    return {
        "resolution": cells,
        "eigenvalues": eigenvalues,
        "eigenvalue_labels": labels,
        "max_relative_residual": max_residual,
        "active_degrees_of_freedom": cells * (weight + 1),
        "assembled_scalar_nonzeros": scalar_nonzeros,
        "sector_selection": {
            "uses_continuum_reference": False,
            "lower_bound": "lambda >= m^2",
            "maximum_abs_m_constructed": weight,
            "first_unconstructed_abs_m": weight + 1,
            "first_unconstructed_sector_lower_bound": float((weight + 1) ** 2),
            "computed_kth_upper_bound": eigenvalues[-1],
            "frontier_certified": frontier,
        },
        "local_cost": {
            "assembly_seconds": assembly_seconds,
            "solve_seconds": solve_seconds,
            "recovery_seconds": recovery_seconds,
        },
    }


def _cartesian_matrix(intervals: int) -> tuple[csr_matrix, float]:
    step = 2.0 / intervals
    points = []
    for row in range(1, intervals):
        y = -1.0 + row * step
        for column in range(1, intervals):
            x = -1.0 + column * step
            if x * x + y * y < 1.0:
                points.append((row, column))
    lookup = {point: index for index, point in enumerate(points)}
    rows: list[int] = []
    columns: list[int] = []
    data: list[float] = []
    scale = 1.0 / (step * step)
    for point, index in lookup.items():
        rows.append(index)
        columns.append(index)
        data.append(4.0 * scale)
        row, column = point
        for neighbor in (
            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1),
        ):
            neighbor_index = lookup.get(neighbor)
            if neighbor_index is not None:
                rows.append(index)
                columns.append(neighbor_index)
                data.append(-scale)
    return csr_matrix((data, (rows, columns)), shape=(len(points), len(points))), step


def _cartesian_attempt(intervals: int, target: int, solver_tolerance: float) -> dict[str, object]:
    started = perf_counter()
    matrix, step = _cartesian_matrix(intervals)
    assembly_seconds = perf_counter() - started
    if matrix.shape[0] <= target:
        raise ValueError("Cartesian budget has too few interior points")
    initial = np.linspace(1.0, 2.0, matrix.shape[0])
    started = perf_counter()
    values, vectors = eigsh(
        matrix,
        k=target,
        sigma=0.0,
        which="LM",
        tol=solver_tolerance,
        v0=initial,
        ncv=min(matrix.shape[0], max(2 * target + 1, 20)),
        return_eigenvectors=True,
    )
    solve_seconds = perf_counter() - started
    order = np.argsort(values)
    values = values[order]
    vectors = vectors[:, order]
    recovery_started = perf_counter()
    residuals = [
        float(
            np.linalg.norm(matrix @ vectors[:, index] - value * vectors[:, index])
            / max(1.0, abs(value))
        )
        for index, value in enumerate(values)
    ]
    eigenvalues = [float(value) for value in values]
    recovery_seconds = perf_counter() - recovery_started
    return {
        "resolution": intervals,
        "grid_step": step,
        "eigenvalues": eigenvalues,
        "max_relative_residual": max(residuals),
        "active_degrees_of_freedom": matrix.shape[0],
        "assembled_scalar_nonzeros": int(matrix.nnz),
        "local_cost": {
            "assembly_seconds": assembly_seconds,
            "solve_seconds": solve_seconds,
            "recovery_seconds": recovery_seconds,
        },
    }


def _run_schedule(
    budgets: list[int],
    attempt: Callable[[int], dict[str, object]],
    reference: list[float],
    tolerance: float,
) -> dict[str, object]:
    cumulative = {"assembly_seconds": 0.0, "solve_seconds": 0.0, "recovery_seconds": 0.0}
    summaries = []
    selected = None
    for budget in budgets:
        current = attempt(budget)
        relative_errors = [
            abs(value - exact) / exact for value, exact in zip(current["eigenvalues"], reference)
        ]
        current["relative_errors"] = relative_errors
        current["max_relative_error"] = max(relative_errors)
        current["tolerance_met"] = current["max_relative_error"] <= tolerance
        for key in cumulative:
            cumulative[key] += current["local_cost"][key]
        summaries.append(
            {
                "resolution": budget,
                "active_degrees_of_freedom": current["active_degrees_of_freedom"],
                "max_relative_error": current["max_relative_error"],
                "tolerance_met": current["tolerance_met"],
            }
        )
        selected = current
        if current["tolerance_met"]:
            break
    assert selected is not None
    selected["attempts"] = summaries
    selected["measured_cost"] = {
        **cumulative,
        "total_seconds": sum(cumulative.values()),
        "includes_failed_refinements": True,
    }
    del selected["local_cost"]
    return selected


def build_fixed_accuracy_comparison(path: Path) -> dict[str, object]:
    """Run both numerical routes and compare with one continuum oracle."""

    try:
        config = _load(Path(path))
        reference_started = perf_counter()
        reference, reference_labels = _continuum_reference(config["target"])
        reference_seconds = perf_counter() - reference_started
        representation = _run_schedule(
            config["radial_budgets"],
            lambda cells: _radial_attempt(cells, config["target"], config["solver_tolerance"]),
            reference,
            config["tolerance"],
        )
        cartesian = _run_schedule(
            config["cartesian_budgets"],
            lambda intervals: _cartesian_attempt(
                intervals, config["target"], config["solver_tolerance"]
            ),
            reference,
            config["tolerance"],
        )
        both_met = representation["tolerance_met"] and cartesian["tolerance_met"]
        observed_ratios = {
            "active_unknowns": representation["active_degrees_of_freedom"]
            / cartesian["active_degrees_of_freedom"],
            "assembled_nonzeros": representation["assembled_scalar_nonzeros"]
            / cartesian["assembled_scalar_nonzeros"],
            "measured_total_seconds": representation["measured_cost"]["total_seconds"]
            / cartesian["measured_cost"]["total_seconds"],
        }
        decision = (
            "RepresentationReductionAtTolerance"
            if both_met
            and representation["active_degrees_of_freedom"] < cartesian["active_degrees_of_freedom"]
            else "NoAccuracyMatchedComparison"
        )
        return {
            "status": "FixedAccuracyComparison" if both_met else "UnresolvedAccuracyWithinBudget",
            "input": config["payload"],
            "analytic_problem": "(-Delta,H^1_0(unit disk))",
            "continuum_reference": {
                "origin": "lambda_(m,k)=j_(m,k)^2; used only for error measurement",
                "eigenvalues": reference,
                "labels": reference_labels,
                "construction_seconds": reference_seconds,
            },
            "representation_route": representation,
            "cartesian_sparse_baseline": cartesian,
            "route_evaluation": {
                "decision": decision,
                "same_observable": f"first {config['target']} continuum Dirichlet-disk eigenvalues with multiplicity",
                "accuracy_target": config["tolerance"],
                "decision_basis": "both routes meet the target; compare active unknowns and retain measured setup/solve/recovery separately",
                "timing_boundary": "single-process wall times are observations, not portable complexity laws",
                "observed_ratios": observed_ratios,
            },
            "certificates": {
                "boundary_symmetry_constructed_before_sector_solve": True,
                "reference_not_used_for_sector_selection": not representation["sector_selection"][
                    "uses_continuum_reference"
                ],
                "same_ordered_continuum_target": len(reference)
                == len(representation["eigenvalues"])
                == len(cartesian["eigenvalues"]),
                "solver_residuals_below_target": representation["max_relative_residual"]
                < config["tolerance"]
                and cartesian["max_relative_residual"] < config["tolerance"],
            },
            "not_certified": [
                "a priori continuum error without the Bessel-zero validation oracle",
                "optimality against every sparse discretization or preconditioner",
                "portable wall-clock speedup",
                "generic nonsymmetric boundaries or variable coefficients",
            ],
        }
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as error:
        return {"status": "Refused", "reason": str(error)}


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--summary", action="store_true")
    arguments = parser.parse_args()
    result = build_fixed_accuracy_comparison(arguments.input)
    if arguments.summary and result["status"] != "Refused":
        print(
            f"{result['status']}: radial={result['representation_route']['resolution']}, "
            f"Cartesian={result['cartesian_sparse_baseline']['resolution']}; "
            f"{result['route_evaluation']['decision']}"
        )
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "FixedAccuracyComparison" else 2


if __name__ == "__main__":
    raise SystemExit(_main())

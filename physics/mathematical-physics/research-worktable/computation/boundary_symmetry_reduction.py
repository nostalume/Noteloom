"""Boundary-compatible symmetry reduction for a bounded polynomial Galerkin probe.

The semantic object is the Dirichlet operator, not its differential expression
alone.  For the unit disk the discovered rotation weight block-diagonalizes the
exact polynomial Ritz pencil without expanding into Cartesian monomials.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from fractions import Fraction
from pathlib import Path

from linear_defect_compiler import (
    CandidateBracket,
    DefectBlock,
    DefectBudget,
    LinearMap,
    compile_defects,
)

MAXIMUM_DEGREE = 32


def _exact_fraction(value: object, label: str) -> Fraction:
    if isinstance(value, (bool, float)):
        raise ValueError(f"{label} must be an exact integer or rational string")
    if not isinstance(value, (int, str)):
        raise ValueError(f"{label} must be an exact integer or rational string")
    return Fraction(value)


def _load(path: Path) -> tuple[list[list[Fraction]], int, dict[str, object]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("operator") != "negative_laplacian":
        raise ValueError("only the negative Laplacian is in this probe")
    if payload.get("boundary_condition") != "dirichlet":
        raise ValueError("only the Dirichlet form domain is in this probe")
    raw_matrix = payload.get("boundary_quadratic")
    if not isinstance(raw_matrix, list) or len(raw_matrix) != 2:
        raise ValueError("boundary_quadratic must be a 2 x 2 exact matrix")
    matrix: list[list[Fraction]] = []
    for row_index, row in enumerate(raw_matrix):
        if not isinstance(row, list) or len(row) != 2:
            raise ValueError("boundary_quadratic must be a 2 x 2 exact matrix")
        matrix.append([_exact_fraction(value, f"boundary_quadratic[{row_index}]") for value in row])
    if matrix[0][1] != matrix[1][0]:
        raise ValueError("boundary_quadratic must be symmetric")
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] ** 2
    if matrix[0][0] <= 0 or determinant <= 0:
        raise ValueError("boundary_quadratic must be positive definite")
    degree = payload.get("polynomial_degree")
    if isinstance(degree, bool) or not isinstance(degree, int):
        raise ValueError("polynomial_degree must be an integer")
    if not 0 <= degree <= MAXIMUM_DEGREE:
        raise ValueError(f"polynomial_degree must lie between 0 and {MAXIMUM_DEGREE}")
    return matrix, degree, payload


def _serialize_matrix(matrix: Iterable[Iterable[Fraction]]) -> list[list[str]]:
    return [[str(value) for value in row] for row in matrix]


def _mass_entry(weight: int, row: int, column: int) -> Fraction:
    radial_power = weight + row + column
    return Fraction(
        2,
        (radial_power + 1) * (radial_power + 2) * (radial_power + 3),
    )


def _stiffness_entry(weight: int, row: int, column: int) -> Fraction:
    radial_power = weight + row + column
    holomorphic_power = weight + column
    antiholomorphic_power = column
    leading = Fraction(
        (holomorphic_power + 1) * (antiholomorphic_power + 1),
        (radial_power + 1) * (radial_power + 2),
    )
    trailing = Fraction(0)
    if holomorphic_power * antiholomorphic_power:
        trailing = Fraction(
            holomorphic_power * antiholomorphic_power,
            radial_power * (radial_power + 1),
        )
    return 4 * (leading - trailing)


def _positive_definite(matrix: list[list[Fraction]]) -> bool:
    """Exact unpivoted LDL^T test; valid because positivity is the claim checked."""

    size = len(matrix)
    lower = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    diagonal = [Fraction(0) for _ in range(size)]
    for row in range(size):
        lower[row][row] = Fraction(1)
        pivot = matrix[row][row] - sum(
            lower[row][index] ** 2 * diagonal[index] for index in range(row)
        )
        if pivot <= 0:
            return False
        diagonal[row] = pivot
        for following in range(row + 1, size):
            numerator = matrix[following][row] - sum(
                lower[following][index] * lower[row][index] * diagonal[index]
                for index in range(row)
            )
            lower[following][row] = numerator / pivot
    return True


def _make_sector(weight: int, degree: int) -> dict[str, object]:
    radial_dimension = (degree - weight) // 2 + 1
    mass = [
        [_mass_entry(weight, row, column) for column in range(radial_dimension)]
        for row in range(radial_dimension)
    ]
    stiffness = [
        [_stiffness_entry(weight, row, column) for column in range(radial_dimension)]
        for row in range(radial_dimension)
    ]
    return {
        "abs_m": weight,
        "radial_dimension": radial_dimension,
        "multiplicity": 1 if weight == 0 else 2,
        "basis": "(1-r^2)*z^m*(z*zbar)^j, j=0,...,d_m-1",
        "mass_over_pi": _serialize_matrix(mass),
        "stiffness_over_pi": _serialize_matrix(stiffness),
        "certificates": {
            "mass_hermitian": mass == [list(row) for row in zip(*mass)],
            "stiffness_hermitian": stiffness == [list(row) for row in zip(*stiffness)],
            "mass_positive_definite": _positive_definite(mass),
            "stiffness_positive_definite": _positive_definite(stiffness),
        },
    }


def _domain_symmetry(matrix: list[list[Fraction]]) -> dict[str, object]:
    g00, g01 = matrix[0]
    _, g11 = matrix[1]
    defect_result = compile_defects(
        candidate_labels=("d_x", "d_y", "x*d_y-y*d_x"),
        blocks=(
            DefectBlock(
                name="boundary-tangency",
                target_labels=("x", "y", "x^2", "x*y", "y^2"),
                columns=(
                    (2 * g00, 2 * g01, 0, 0, 0),
                    (2 * g01, 2 * g11, 0, 0, 0),
                    (0, 0, 2 * g01, 2 * (g11 - g00), -2 * g01),
                ),
            ),
        ),
        visible_action=LinearMap(
            name="rotation-character-action",
            target_labels=("rotation-weight",),
            columns=((0,), (0,), (1,)),
        ),
        bracket=CandidateBracket(
            name="e2",
            table=(
                ((0, 0, 0), (0, 0, 0), (0, -1, 0)),
                ((0, 0, 0), (0, 0, 0), (1, 0, 0)),
                ((0, 1, 0), (-1, 0, 0), (0, 0, 0)),
            ),
        ),
        budget=DefectBudget(3, 5, maximum_bracket_checks=64),
    )
    if defect_result.outcome != "exact":
        raise AssertionError("the fixed affine boundary defect budget was refused")
    scalar_metric = matrix[0][1] == 0 and matrix[1][0] == 0 and matrix[0][0] == matrix[1][1]
    kernel_dimension = defect_result.kernel_dimension
    return {
        "differential_expression_killing_dimension": 3,
        "differential_expression_generators": ["d_x", "d_y", "x*d_y-y*d_x"],
        "boundary_compatible_killing_dimension": kernel_dimension,
        "generator": "x*d_y-y*d_x" if kernel_dimension == 1 else None,
        "identity_component": "SO(2)" if kernel_dimension == 1 else "trivial",
        "construction": "intersect Euclidean Killing fields with X(rho)=0 on rho=x^T*G*x-1",
        "rotation_obstruction": "G*J-J*G",
        "defect_compilation": {
            "block": defect_result.ledger[0].name,
            "rank_drop": defect_result.ledger[0].rank_drop,
            "closure": defect_result.closure_status,
            "effective_dimension": defect_result.effective_dimension,
            "kernel_basis": [
                [str(coefficient) for coefficient in vector]
                for vector in defect_result.kernel_basis
            ],
        },
        "certificates": {
            "positive_boundary_form_removes_translations": True,
            "rotation_tangent_exactly_when_G_commutes_with_J": True,
            "dirichlet_trace_preserved_by_tangent_isometry": scalar_metric,
        },
    }


def _complexity(degree: int, sectors: list[dict[str, object]]) -> dict[str, object]:
    dimension = (degree + 1) * (degree + 2) // 2
    sizes = [int(sector["radial_dimension"]) for sector in sectors]
    full_storage = dimension**2
    reduced_storage = sum(size**2 for size in sizes)
    full_assembly = dimension * (dimension + 1)
    reduced_assembly = sum(size * (size + 1) for size in sizes)
    full_solve = dimension**3
    reduced_solve = sum(size**3 for size in sizes)
    parallel_critical_path = max(size**3 for size in sizes)
    discovery = 9
    labeling = dimension
    recovery = dimension
    full_total = full_assembly + full_solve + recovery
    reduced_total = discovery + labeling + reduced_assembly + reduced_solve + recovery
    return {
        "cost_model": "dense generalized-eigensolve arithmetic/storage proxies on one fixed Ritz space",
        "full_dense": {
            "assembly_scalar_entries": full_assembly,
            "solve_cubic_proxy": full_solve,
            "matrix_storage_proxy": full_storage,
            "recovery_labels": recovery,
            "whole_route_proxy": full_total,
        },
        "representation_reduced": {
            "boundary_symmetry_constraints": discovery,
            "weight_labeling": labeling,
            "assembly_scalar_entries": reduced_assembly,
            "solve_cubic_proxy": reduced_solve,
            "parallel_critical_path_proxy": parallel_critical_path,
            "matrix_storage_proxy": reduced_storage,
            "recovery_labels": recovery,
            "whole_route_proxy": reduced_total,
        },
        "ratios_reduced_over_full": {
            "solve": str(Fraction(reduced_solve, full_solve)),
            "storage": str(Fraction(reduced_storage, full_storage)),
            "whole_route": str(Fraction(reduced_total, full_total)),
        },
        "asymptotic": {
            "full_dimension": "Theta(p^2)",
            "full_assembly": "Theta(p^4)",
            "reduced_assembly": "Theta(p^3)",
            "full_solve": "Theta(p^6)",
            "reduced_solve": "Theta(p^4)",
            "parallel_critical_path": "Theta(p^3)",
            "full_storage": "Theta(p^4)",
            "reduced_storage": "Theta(p^3)",
            "observable_recovery": "Theta(p^2)",
        },
        "boundary": "these exponents are for dense all-eigenpair pencils; sparse/iterative, partial-spectrum, and conditioning costs require separate audits",
    }


def build_boundary_reduction(path: Path) -> dict[str, object]:
    """Construct the continuous domain symmetry and its exact Galerkin blocks."""

    try:
        matrix, degree, payload = _load(Path(path))
        symmetry = _domain_symmetry(matrix)
        common = {
            "input": payload,
            "semantic_operator": "(-Delta, H^1_0(Omega_G)); Omega_G={x:x^T G x<1}",
            "domain_symmetry": symmetry,
        }
        if symmetry["boundary_compatible_killing_dimension"] == 0:
            return {
                **common,
                "status": "NoContinuousBoundarySymmetry",
                "reason": "the differential expression has Euclidean symmetries, but the boundary domain removes every connected generator",
                "route_evaluation": {
                    "decision": "NoRepresentationReduction",
                    "discrete_or_non-group_reductions": "not searched within this continuous Lie budget",
                },
            }
        if matrix != [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]:
            return {
                **common,
                "status": "Refused",
                "reason": "the exact Galerkin formula budget currently covers the unit disk only",
            }
        sectors = [_make_sector(weight, degree) for weight in range(degree + 1)]
        dimension = (degree + 1) * (degree + 2) // 2
        represented_dimension = sum(
            int(sector["multiplicity"]) * int(sector["radial_dimension"]) for sector in sectors
        )
        matrix_certificates = {
            key: all(bool(sector["certificates"][key]) for sector in sectors)
            for key in (
                "mass_hermitian",
                "stiffness_hermitian",
                "mass_positive_definite",
                "stiffness_positive_definite",
            )
        }
        complexity = _complexity(degree, sectors)
        return {
            **common,
            "status": "ExactBoundaryCompatibleReduction",
            "observable": "all Ritz eigenvalues of the Dirichlet Laplacian in V_p=(1-r^2)P_p",
            "galerkin": {
                "polynomial_degree": degree,
                "full_dimension": dimension,
                "full_basis": "(1-x^2-y^2)*x^a*y^b, a+b<=p",
                "represented_basis": "(1-r^2)*z^a*zbar^b, a+b<=p",
                "basis_change": "z=x+i*y, zbar=x-i*y; determinant=-2*i",
                "sectors": sectors,
                "dimension_identity": represented_dimension == dimension,
                "unequal_weights_vanish_by_character_orthogonality": True,
                "matrix_certificates": matrix_certificates,
                "pencil_equality_witness": "the invertible complex coordinate change preserves V_p; angular character orthogonality makes both Gram forms the displayed direct sum",
            },
            "complexity": complexity,
            "route_evaluation": {
                "decision": "RepresentationReduction"
                if complexity["representation_reduced"]["whole_route_proxy"]
                < complexity["full_dense"]["whole_route_proxy"]
                else "NoMeasuredGain",
                "same_observable": "the complete Ritz spectrum with angular multiplicities",
                "gain": "block construction reduces dense solve Theta(p^6)->Theta(p^4) and storage Theta(p^4)->Theta(p^3)",
                "human_compression": "one character label m and one radial index j replace Cartesian coefficient coupling",
            },
            "not_certified": [
                "continuum eigenvalue error as p grows",
                "conditioning improvement of the monomial radial blocks",
                "complexity exponents for sparse or partial-spectrum solvers",
                "usefulness when the boundary has no connected symmetry",
            ],
        }
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return {"status": "Refused", "reason": str(error)}


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--summary", action="store_true")
    arguments = parser.parse_args()
    result = build_boundary_reduction(arguments.input)
    if arguments.summary:
        if result["status"] == "ExactBoundaryCompatibleReduction":
            galerkin = result["galerkin"]
            print(
                f"{result['status']}: {galerkin['full_dimension']} -> "
                f"{len(galerkin['sectors'])} blocks; "
                f"{result['route_evaluation']['decision']}"
            )
        else:
            print(f"{result['status']}: {result['reason']}")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "ExactBoundaryCompatibleReduction" else 2


if __name__ == "__main__":
    raise SystemExit(_main())

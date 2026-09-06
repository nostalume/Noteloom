"""Exact cross-probe witness for a rotated positive quadratic oscillator.

The factor route splits the stiffness matrix directly. The centralizer route
first consumes the complete E^3 quadratic-centralizer kernel, selects a
simple-spectrum element of that commutative algebra, and splits that element.
Their primitive projectors are compared exactly before a route is selected.
"""

from __future__ import annotations

import argparse
import json
import math
from collections.abc import Iterable
from fractions import Fraction
from pathlib import Path

from radial_quadratic_centralizer_e3 import (
    NDDiffOp,
    NDExpr,
    generate,
    hamiltonian,
    load_potential,
    quantum_operator,
    reconstruct_lower_term,
    solve_linear,
)

Matrix = tuple[tuple[Fraction, ...], ...]
Vector = tuple[Fraction, ...]


def _identity(dimension: int) -> Matrix:
    return tuple(tuple(Fraction(int(i == j)) for j in range(dimension)) for i in range(dimension))


def _zero(dimension: int) -> Matrix:
    return tuple(tuple(Fraction(0) for _ in range(dimension)) for _ in range(dimension))


def _transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[j][i] for j in range(len(matrix))) for i in range(len(matrix)))


def _subtract(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(left[i][j] - right[i][j] for j in range(len(left))) for i in range(len(left))
    )


def _scale(matrix: Matrix, coefficient: Fraction) -> Matrix:
    return tuple(tuple(coefficient * value for value in row) for row in matrix)


def _multiply(left: Matrix, right: Matrix) -> Matrix:
    dimension = len(left)
    return tuple(
        tuple(
            sum((left[i][k] * right[k][j] for k in range(dimension)), Fraction(0))
            for j in range(dimension)
        )
        for i in range(dimension)
    )


def _trace(matrix: Matrix) -> Fraction:
    return sum((matrix[i][i] for i in range(len(matrix))), Fraction(0))


def _determinant_three(matrix: Matrix) -> Fraction:
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def _outer(vector: Vector) -> Matrix:
    return tuple(tuple(left * right for right in vector) for left in vector)


def _serialize_matrix(matrix: Matrix) -> list[list[str]]:
    return [[str(value) for value in row] for row in matrix]


def _integer_divisors(value: int) -> list[int]:
    value = abs(value)
    if value == 0:
        return [0]
    result: set[int] = set()
    for divisor in range(1, math.isqrt(value) + 1):
        if value % divisor == 0:
            result.add(divisor)
            result.add(value // divisor)
    return sorted(result)


def _evaluate_polynomial(coefficients: list[Fraction], value: Fraction) -> Fraction:
    result = Fraction(0)
    for coefficient in coefficients:
        result = result * value + coefficient
    return result


def _rational_roots(coefficients: list[Fraction]) -> list[Fraction]:
    remaining = list(coefficients)
    roots: list[Fraction] = []
    while len(remaining) > 2:
        if remaining[-1] == 0:
            root = Fraction(0)
        else:
            common_denominator = math.lcm(*(value.denominator for value in remaining))
            integers = [int(value * common_denominator) for value in remaining]
            candidates = {
                Fraction(sign * numerator, denominator)
                for numerator in _integer_divisors(integers[-1])
                for denominator in _integer_divisors(integers[0])
                for sign in (-1, 1)
                if denominator
            }
            root = next(
                (
                    value
                    for value in sorted(candidates)
                    if _evaluate_polynomial(remaining, value) == 0
                ),
                None,
            )
            if root is None:
                raise ValueError("characteristic polynomial does not split over the rationals")
        quotient = [remaining[0]]
        for coefficient in remaining[1:-1]:
            quotient.append(coefficient + root * quotient[-1])
        if remaining[-1] + root * quotient[-1] != 0:
            raise AssertionError("synthetic division produced a nonzero remainder")
        roots.append(root)
        remaining = quotient
    roots.append(-remaining[1] / remaining[0])
    return sorted(roots)


def _rational_eigenvalues(matrix: Matrix) -> list[Fraction]:
    if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
        raise ValueError("cross-probe spectral splitting is bounded to dimension three")
    trace = _trace(matrix)
    square_trace = _trace(_multiply(matrix, matrix))
    second = (trace * trace - square_trace) / 2
    coefficients = [Fraction(1), -trace, second, -_determinant_three(matrix)]
    roots = _rational_roots(coefficients)
    if len(roots) != 3:
        raise ValueError(
            "the dimension-three characteristic polynomial must have three rational roots"
        )
    return roots


def _sum_matrices(matrices: Iterable[Matrix]) -> Matrix:
    items = list(matrices)
    if not items:
        raise ValueError("at least one matrix is required")
    result = items[0]
    for matrix in items[1:]:
        result = tuple(
            tuple(result[i][j] + matrix[i][j] for j in range(len(result)))
            for i in range(len(result))
        )
    return result


def _spectral_projectors(matrix: Matrix, eigenvalues: list[Fraction]) -> list[Matrix]:
    dimension = len(matrix)
    identity = _identity(dimension)
    projectors: list[Matrix] = []
    for eigenvalue in eigenvalues:
        projector = identity
        for other in eigenvalues:
            if other == eigenvalue:
                continue
            projector = _multiply(projector, _subtract(matrix, _scale(identity, other)))
            projector = _scale(projector, Fraction(1, 1) / (eigenvalue - other))
        projectors.append(projector)
    if _sum_matrices(projectors) != identity:
        raise AssertionError("spectral projectors do not resolve the identity")
    for index, projector in enumerate(projectors):
        if _multiply(projector, projector) != projector or _trace(projector) != 1:
            raise AssertionError("spectral projector is not a primitive rank-one idempotent")
        for other_index, other in enumerate(projectors):
            expected = projector if index == other_index else _zero(dimension)
            if _multiply(projector, other) != expected:
                raise AssertionError("spectral projectors are not mutually orthogonal")
    return projectors


def _sqrt_fraction(value: Fraction) -> Fraction:
    if value <= 0:
        raise ValueError("normalization norm must be positive")
    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        raise ValueError("the benchmark requires rationally normalized eigendirections")
    return Fraction(numerator, denominator)


def _axis_from_projector(projector: Matrix) -> Vector:
    dimension = len(projector)
    for column in range(dimension):
        candidate = tuple(projector[row][column] for row in range(dimension))
        norm_squared = sum((value * value for value in candidate), Fraction(0))
        if not norm_squared:
            continue
        norm = _sqrt_fraction(norm_squared)
        axis = tuple(value / norm for value in candidate)
        first_nonzero = next(value for value in axis if value)
        if first_nonzero < 0:
            axis = tuple(-value for value in axis)
        if _outer(axis) != projector:
            raise AssertionError("canonical axis does not reconstruct its projector")
        return axis
    raise AssertionError("zero projector has no eigendirection")


def _axes_matrix(projectors: list[Matrix]) -> Matrix:
    axes = [_axis_from_projector(projector) for projector in projectors]
    return tuple(
        tuple(axes[column][row] for column in range(len(axes))) for row in range(len(axes))
    )


def _constant_from_expression(payload: list[dict[str, object]]) -> Fraction:
    if not payload:
        return Fraction(0)
    if len(payload) != 1:
        raise ValueError("centralizer splitter must have constant tensor coefficients")
    term = payload[0]
    if term["powers"] != [0, 0, 0] or term["radius_squared_power"] != "0":
        raise ValueError("centralizer splitter must have constant tensor coefficients")
    return Fraction(str(term["coefficient"]))


def _tensor_matrix(payload: list[list[list[dict[str, object]]]]) -> Matrix:
    return tuple(
        tuple(_constant_from_expression(payload[i][j]) for j in range(3)) for i in range(3)
    )


def _constant_expression(expression: NDExpr) -> Fraction:
    if not expression.terms:
        return Fraction(0)
    constant_key = ((0, 0, 0), Fraction(0))
    if set(expression.terms) != {constant_key}:
        raise ValueError("quadratic Hessian must have constant coefficients")
    return expression.terms[constant_key]


def _stiffness_from_potential(potential: NDExpr) -> Matrix:
    stiffness = tuple(
        tuple(_constant_expression(potential.derivative(i).derivative(j)) for j in range(3))
        for i in range(3)
    )
    coordinates = [
        NDExpr.monomial(3, powers=tuple(int(index == i) for index in range(3))) for i in range(3)
    ]
    reconstructed = NDExpr.zero(3)
    for i in range(3):
        for j in range(3):
            reconstructed += (coordinates[i] * coordinates[j]).scale(stiffness[i][j] / 2)
    if reconstructed != potential:
        raise ValueError("input potential must be a homogeneous quadratic form")
    return stiffness


def _projector_membership(projector: Matrix, basis: list[Matrix]) -> bool:
    rows = [(i, j) for i in range(3) for j in range(i, 3)]
    matrix = [[candidate[i][j] for candidate in basis] for i, j in rows]
    target = [projector[i][j] for i, j in rows]
    return solve_linear(matrix, target) is not None


def _projector_tensor(projector: Matrix):
    return tuple(tuple(NDExpr.constant(3, projector[i][j]) for j in range(3)) for i in range(3))


def _sum_operators(operators: list[NDDiffOp]) -> NDDiffOp:
    return sum(operators[1:], operators[0])


def _frequency_label(eigenvalue: Fraction) -> str:
    numerator = math.isqrt(eigenvalue.numerator)
    denominator = math.isqrt(eigenvalue.denominator)
    if (
        numerator * numerator == eigenvalue.numerator
        and denominator * denominator == eigenvalue.denominator
    ):
        return str(Fraction(numerator, denominator))
    return f"sqrt({eigenvalue})"


def _mode_representation(
    eigenvalues: list[Fraction], projectors: list[Matrix]
) -> dict[str, object]:
    axes = [_axis_from_projector(projector) for projector in projectors]
    modes = [
        {
            "axis": [str(value) for value in axis],
            "frequency_squared": str(eigenvalue),
            "frequency": _frequency_label(eigenvalue),
            "lowering": f"a_{index}^-=partial_(v_{index})+omega_{index} z_{index}",
            "raising": f"a_{index}^+=-partial_(v_{index})+omega_{index} z_{index}",
            "hamiltonian": f"H_{index}=a_{index}^+ a_{index}^-/2+omega_{index}/2",
        }
        for index, (eigenvalue, axis) in enumerate(zip(eigenvalues, axes), start=1)
    ]
    return {
        "modes": modes,
        "relations": [
            "[a_i^-,a_j^+]=2 omega_i delta_ij",
            "[H_i,a_j^+]=omega_i delta_ij a_j^+",
            "[H_i,a_j^-]=-omega_i delta_ij a_j^-",
        ],
        "lowest_weight": "a_i^- psi_0=0 for every i",
    }


def _observable(representation: dict[str, object]) -> dict[str, object]:
    frequencies = [mode["frequency"] for mode in representation["modes"]]
    return {
        "frequencies": frequencies,
        "energy_family": "E_(n1,n2,n3)=sum_i (n_i+1/2) omega_i",
        "heat_trace": "product_i exp(-t omega_i/2)/(1-exp(-t omega_i))",
    }


def _witness(
    route: str,
    stiffness: Matrix,
    eigenvalues: list[Fraction],
    projectors: list[Matrix],
    observable: dict[str, object],
) -> dict[str, object]:
    synthesis = _axes_matrix(projectors)
    analysis = _transpose(synthesis)
    representation = _mode_representation(eigenvalues, projectors)
    reduced = tuple(
        tuple(eigenvalues[i] if i == j else Fraction(0) for j in range(3)) for i in range(3)
    )
    return {
        "route": route,
        "status": "ExactReduction",
        "original_carrier": "Schwartz(R^3_x)",
        "reduced_carrier": "tensor_i Schwartz(R_(z_i))",
        "original_operator": "H=-Delta_x/2+x^T K x/2",
        "reduced_operator": "H_red=sum_i (-partial_(z_i)^2+lambda_i z_i^2)/2",
        "analysis": _serialize_matrix(analysis),
        "synthesis": _serialize_matrix(synthesis),
        "reduced_stiffness": _serialize_matrix(reduced),
        "mode_projectors": [_serialize_matrix(projector) for projector in projectors],
        "coordinate_actions": {
            "analysis": "z=A x",
            "synthesis": "x=S z",
            "wavefunction_analysis": "(U f)(z)=f(S z)",
            "wavefunction_synthesis": "(U^-1 g)(x)=g(A x)",
        },
        "representation": representation,
        "observable": observable,
        "visible_projector": "identity",
        "ambiguity": "projectors are canonical; each normalized axis has a removed sign choice",
        "residuals": {
            "analysis_synthesis_zero": _multiply(analysis, synthesis) == _identity(3),
            "synthesis_analysis_zero": _multiply(synthesis, analysis) == _identity(3),
            "potential_intertwining_zero": _multiply(_multiply(analysis, stiffness), synthesis)
            == reduced,
            "kinetic_intertwining_zero": _multiply(analysis, synthesis) == _identity(3),
        },
    }


def build_cross_probe(path: Path) -> dict[str, object]:
    """Construct and compare factor and centralizer witnesses."""

    try:
        potential = load_potential(path)
        stiffness = _stiffness_from_potential(potential)
        eigenvalues = _rational_eigenvalues(stiffness)
        if len(set(eigenvalues)) != 3 or any(value <= 0 for value in eigenvalues):
            raise ValueError("benchmark requires three distinct positive stiffness eigenvalues")

        factor_projectors = _spectral_projectors(stiffness, eigenvalues)
        for value, projector in zip(eigenvalues, factor_projectors):
            if _multiply(stiffness, projector) != _scale(projector, value):
                raise AssertionError("factor projector does not diagonalize the stiffness")

        generated = generate(potential)
        if generated["first_order_kernel_dimension"] != 0:
            raise ValueError("cross-probe requires no continuous first-order spatial symmetry")
        if generated["quadratic_kernel_dimension"] != 3:
            raise ValueError("cross-probe requires a minimal three-dimensional quadratic kernel")
        centralizer_basis = [
            _tensor_matrix(generator["tensor"]) for generator in generated["generators"]
        ]

        splitter = None
        splitter_eigenvalues: list[Fraction] | None = None
        for candidate in centralizer_basis:
            try:
                roots = _rational_eigenvalues(candidate)
            except ValueError:
                continue
            if len(set(roots)) == 3:
                splitter = candidate
                splitter_eigenvalues = roots
                break
        if splitter is None or splitter_eigenvalues is None:
            raise ValueError(
                "generated centralizer has no admitted rational simple-spectrum splitter"
            )

        unsorted_projectors = _spectral_projectors(splitter, splitter_eigenvalues)
        paired = sorted(
            (
                (_trace(_multiply(projector, stiffness)), projector)
                for projector in unsorted_projectors
            ),
            key=lambda item: item[0],
        )
        centralizer_eigenvalues = [value for value, _ in paired]
        centralizer_projectors = [projector for _, projector in paired]
        if not all(
            _projector_membership(projector, centralizer_basis)
            for projector in centralizer_projectors
        ):
            raise AssertionError("primitive projector is outside the generated centralizer kernel")

        mode_operators = []
        h_op = hamiltonian(potential)
        for projector in centralizer_projectors:
            tensor = _projector_tensor(projector)
            lower = reconstruct_lower_term(potential, tensor)
            mode_operators.append(quantum_operator(tensor, lower))
        operator_sum_zero = not (_sum_operators(mode_operators) - h_op).terms
        pairwise_commutators_zero = all(
            not (left.compose(right) - right.compose(left)).terms
            for left in mode_operators
            for right in mode_operators
        )

        factor_representation = _mode_representation(eigenvalues, factor_projectors)
        centralizer_representation = _mode_representation(
            centralizer_eigenvalues, centralizer_projectors
        )
        observable = _observable(factor_representation)
        centralizer_observable = _observable(centralizer_representation)
        factor_witness = _witness("factor", stiffness, eigenvalues, factor_projectors, observable)
        centralizer_witness = _witness(
            "centralizer",
            stiffness,
            centralizer_eigenvalues,
            centralizer_projectors,
            centralizer_observable,
        )
        coincidence_checks = {
            "primitive_projectors_equal": factor_projectors == centralizer_projectors,
            "analysis_maps_equal": factor_witness["analysis"] == centralizer_witness["analysis"],
            "synthesis_maps_equal": factor_witness["synthesis"] == centralizer_witness["synthesis"],
            "reduced_dynamics_equal": factor_witness["reduced_stiffness"]
            == centralizer_witness["reduced_stiffness"],
            "oscillator_representations_equal": factor_witness["representation"]
            == centralizer_witness["representation"],
            "observable_equal": factor_witness["observable"] == centralizer_witness["observable"],
            "factor_residuals_zero": all(factor_witness["residuals"].values()),
            "centralizer_residuals_zero": all(centralizer_witness["residuals"].values()),
            "mode_operator_sum_zero": operator_sum_zero,
            "mode_operators_commute": pairwise_commutators_zero,
        }
        if not all(coincidence_checks.values()):
            raise AssertionError("factor and centralizer witnesses do not coincide")

        return {
            "status": "ExactCrossProbeSelection",
            "input": {
                "dimension": 3,
                "stiffness": _serialize_matrix(stiffness),
                "stiffness_eigenvalues": [str(value) for value in eigenvalues],
                "core": "Schwartz(R^3)",
                "observable": "full discrete spectrum and heat trace",
            },
            "factor_witness": factor_witness,
            "centralizer_witness": centralizer_witness,
            "centralizer": {
                "first_order_kernel_dimension": generated["first_order_kernel_dimension"],
                "quadratic_presented_dimension": generated["quadratic_presented_dimension"],
                "quadratic_module_dimension": generated["quadratic_module_dimension"],
                "quadratic_kernel_dimension": generated["quadratic_kernel_dimension"],
                "splitter": _serialize_matrix(splitter),
                "splitter_eigenvalues": [str(value) for value in splitter_eigenvalues],
            },
            "coincidence_checks": coincidence_checks,
            "cost_comparison": {
                "factor": {
                    "compatibility_columns": 0,
                    "spectral_projectors": 3,
                    "semantic_steps": 4,
                },
                "centralizer": {
                    "presented_tensors": generated["quadratic_presented_dimension"],
                    "independent_tensors": generated["quadratic_module_dimension"],
                    "compatibility_columns": generated["quadratic_module_dimension"],
                    "spectral_projectors": 3,
                    "semantic_steps": 7,
                },
                "common_downstream_work": "same three modes, factor pairs, spectrum, and heat trace",
                "dominance_witness": {
                    "same_downstream_artifact": True,
                    "factor_only_operations": [],
                    "centralizer_extra_operations": [
                        "generate 21 Killing-tensor presentations",
                        "quotient to a 20-dimensional module",
                        "solve the 20-column compatibility kernel",
                        "split a generated commutant element",
                    ],
                },
            },
            "selected_route": "factor",
            "selection_reason": (
                "For the requested spectrum and heat trace, factorization reaches the identical "
                "projectors without constructing a 20-column compatibility kernel. Retain the "
                "centralizer as the relative-completeness and commutant certificate."
            ),
            "not_certified": [
                "a universal ordering of route costs outside this observable and model class",
                "oscillator spectral completeness beyond the imported one-dimensional theorem",
                "higher-order resonant centralizers",
            ],
        }
    except (AssertionError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        return {"status": "Refused", "reason": str(error)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--summary", action="store_true")
    arguments = parser.parse_args()
    result = build_cross_probe(arguments.input)
    if arguments.summary and result["status"] == "ExactCrossProbeSelection":
        centralizer = result["centralizer"]
        print(
            f"{result['status']}: factor == centralizer on 3 projectors; "
            f"kernel {centralizer['quadratic_module_dimension']} -> "
            f"{centralizer['quadratic_kernel_dimension']}; selected {result['selected_route']}"
        )
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "ExactCrossProbeSelection" else 2


if __name__ == "__main__":
    raise SystemExit(main())

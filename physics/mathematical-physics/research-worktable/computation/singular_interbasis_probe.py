"""Exact interbasis cross-probe for the singular E2 oscillator.

One route consumes the PDE-generated polynomial presentation.  The independent
route consumes the two one-dimensional positive su(1,1) modules and constructs
the angular integral from their coproduct Casimir.  Equality of their Jacobi data
implies equality of the normalized transition probabilities up to phase signs.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

from singular_polynomial_closure import build_polynomial_closure


def _sqrt_fraction(value: Fraction, label: str) -> Fraction:
    if value < 0:
        raise ValueError(f"{label} must be nonnegative")
    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        raise ValueError(f"{label} must have a rational square root")
    return Fraction(numerator, denominator)


def _serialize(values: list[Fraction]) -> list[str]:
    return [str(value) for value in values]


def _serialize_matrix(matrix: list[list[Fraction]]) -> list[list[str]]:
    return [[str(value) for value in row] for row in matrix]


def _evaluate_characteristic(
    diagonal: list[Fraction], off_diagonal_squared: list[Fraction], value: Fraction
) -> Fraction:
    previous = Fraction(0)
    current = Fraction(1)
    for index, diagonal_value in enumerate(diagonal):
        coupling = Fraction(0) if index == 0 else off_diagonal_squared[index - 1]
        following = (value - diagonal_value) * current - coupling * previous
        previous, current = current, following
    return current


def _transition_probabilities(
    diagonal: list[Fraction],
    off_diagonal_squared: list[Fraction],
    spectrum: list[Fraction],
) -> list[list[Fraction]]:
    columns: list[list[Fraction]] = []
    for eigenvalue in spectrum:
        previous_polynomial = Fraction(0)
        polynomial = Fraction(1)
        product = Fraction(1)
        component_squares = [Fraction(1)]
        for index in range(len(diagonal) - 1):
            coupling = Fraction(0) if index == 0 else off_diagonal_squared[index - 1]
            following = (eigenvalue - diagonal[index]) * polynomial - coupling * previous_polynomial
            product *= off_diagonal_squared[index]
            component_squares.append(following * following / product)
            previous_polynomial, polynomial = polynomial, following
        normalization = sum(component_squares, Fraction(0))
        columns.append([value / normalization for value in component_squares])
    return [
        [columns[column][row] for column in range(len(columns))] for row in range(len(diagonal))
    ]


def _factor_enveloping_route(input_data: dict[str, object], level: int) -> dict[str, object]:
    omega_x_squared = Fraction(str(input_data["omega_x_squared"]))
    omega_y_squared = Fraction(str(input_data["omega_y_squared"]))
    if omega_x_squared != omega_y_squared:
        raise ValueError("interbasis probe requires isotropic confinement")
    omega = _sqrt_fraction(omega_x_squared, "omega_squared")
    g_x = Fraction(str(input_data["g_x"]))
    g_y = Fraction(str(input_data["g_y"]))
    nu_x = _sqrt_fraction(g_x + Fraction(1, 4), "g_x+1/4")
    nu_y = _sqrt_fraction(g_y + Fraction(1, 4), "g_y+1/4")
    k_x = (1 + nu_x) / 2
    k_y = (1 + nu_y) / 2
    energy = 2 * omega * (level + k_x + k_y)
    b_eigenvalues = [2 * omega * (n + k_x) for n in range(level + 1)]
    c_x = k_x * (k_x - 1)
    c_y = k_y * (k_y - 1)
    shift = Fraction(1, 2) - (g_x + g_y) / 2
    diagonal = [
        2 * (c_x + c_y + 2 * (n + k_x) * (level - n + k_y)) + shift for n in range(level + 1)
    ]
    off_diagonal_squared = [
        4 * (n + 1) * (n + 2 * k_x) * (level - n) * (level - n + 2 * k_y - 1) for n in range(level)
    ]
    spectrum = [2 * (k_x + k_y + q) * (k_x + k_y + q - 1) + shift for q in range(level + 1)]
    probabilities = _transition_probabilities(diagonal, off_diagonal_squared, spectrum)
    return {
        "origin": "two positive discrete su(1,1) factors and their coproduct Casimir",
        "factor_labels": {"k_x": str(k_x), "k_y": str(k_y)},
        "operator_identification": "B=2*omega*K0_x; A=2*C_coproduct+1/2-(g_x+g_y)/2",
        "energy": str(energy),
        "jacobi_data": {
            "B_eigenvalues": _serialize(b_eigenvalues),
            "A_diagonal": _serialize(diagonal),
            "A_off_diagonal_squared": _serialize(off_diagonal_squared),
        },
        "A_spectrum": _serialize(spectrum),
        "transition_probabilities": _serialize_matrix(probabilities),
        "raw": {
            "diagonal": diagonal,
            "off_diagonal_squared": off_diagonal_squared,
            "spectrum": spectrum,
            "probabilities": probabilities,
        },
    }


def _polynomial_route(closure_result: dict[str, object], level: int) -> dict[str, object]:
    representation = closure_result.get("representation")
    if not representation or representation["status"] != "ExactPositiveFiniteRepresentations":
        raise ValueError("polynomial closure did not construct a positive finite representation")
    levels = representation["levels"]
    if level < 0 or level >= len(levels):
        raise ValueError(f"level must lie between 0 and {len(levels) - 1}")
    data = levels[level]
    diagonal = [Fraction(value) for value in data["A_diagonal"]]
    off_diagonal_squared = [Fraction(value) for value in data["A_off_diagonal_squared"][:-1]]
    factor = _factor_enveloping_route(closure_result["input"], level)
    candidate_spectrum = factor["raw"]["spectrum"]
    if not all(
        _evaluate_characteristic(diagonal, off_diagonal_squared, eigenvalue) == 0
        for eigenvalue in candidate_spectrum
    ):
        raise AssertionError(
            "coproduct spectrum does not annihilate the generated characteristic recurrence"
        )
    probabilities = _transition_probabilities(diagonal, off_diagonal_squared, candidate_spectrum)
    return {
        "origin": "PDE-generated quadratic closure and positivity recurrence",
        "energy": data["selected_energy"],
        "jacobi_data": {
            "B_eigenvalues": data["B_eigenvalues"],
            "A_diagonal": data["A_diagonal"],
            "A_off_diagonal_squared": data["A_off_diagonal_squared"][:-1],
        },
        "A_spectrum": _serialize(candidate_spectrum),
        "spectrum_witness": "all coproduct eigenvalues are exact zeros of the generated monic characteristic recurrence",
        "transition_probabilities": _serialize_matrix(probabilities),
        "raw": {
            "diagonal": diagonal,
            "off_diagonal_squared": off_diagonal_squared,
            "spectrum": candidate_spectrum,
            "probabilities": probabilities,
        },
    }


def build_interbasis_probe(path: Path, level: int) -> dict[str, object]:
    """Compare polynomial and factor/enveloping constructions on one eigenspace."""

    try:
        closure_result = build_polynomial_closure(Path(path))
        if closure_result["status"] != "ExactPolynomialClosure":
            raise ValueError("input does not produce the required exact polynomial closure")
        factor = _factor_enveloping_route(closure_result["input"], level)
        polynomial = _polynomial_route(closure_result, level)
        factor.pop("raw")
        polynomial_raw = polynomial.pop("raw")
        probabilities = polynomial_raw["probabilities"]
        row_sums_one = all(sum(row, Fraction(0)) == 1 for row in probabilities)
        column_sums_one = all(
            sum((probabilities[row][column] for row in range(len(probabilities))), Fraction(0)) == 1
            for column in range(len(probabilities))
        )
        coincidence = {
            "energy_equal": polynomial["energy"] == factor["energy"],
            "B_lattice_equal": polynomial["jacobi_data"]["B_eigenvalues"]
            == factor["jacobi_data"]["B_eigenvalues"],
            "A_diagonal_equal": polynomial["jacobi_data"]["A_diagonal"]
            == factor["jacobi_data"]["A_diagonal"],
            "A_off_diagonal_norms_equal": polynomial["jacobi_data"]["A_off_diagonal_squared"]
            == factor["jacobi_data"]["A_off_diagonal_squared"],
            "A_spectrum_equal": polynomial["A_spectrum"] == factor["A_spectrum"],
            "transition_probabilities_equal": polynomial["transition_probabilities"]
            == factor["transition_probabilities"],
            "probability_rows_normalized": row_sums_one,
            "probability_columns_normalized": column_sums_one,
        }
        if not all(coincidence.values()):
            raise AssertionError("interbasis constructions do not coincide")
        return {
            "status": "ExactInterbasisCoincidence",
            "level": level,
            "dimension": level + 1,
            "observable": {
                "meaning": "phase-insensitive transition probabilities |<n_B|q_A>|^2",
                "transition_probabilities": polynomial["transition_probabilities"],
                "row_sums_one": row_sums_one,
                "column_sums_one": column_sums_one,
                "phase_boundary": "basis-vector signs are not fixed and are invisible to this observable",
            },
            "polynomial_route": polynomial,
            "factor_enveloping_route": factor,
            "coincidence_checks": coincidence,
            "route_evaluation": {
                "decision": "ParetoRetainBoth",
                "common_downstream_work": "one finite Jacobi recurrence and its spectral weights",
                "factor_distinct_capability": "constructs the parent Lie representation and explains tensor-product coupling",
                "polynomial_distinct_capability": "discovers a relative-complete quadratic centralizer without prior separability or group input",
                "factor_extra_presumption": "the visible Cartesian split admits two singular-oscillator su(1,1) factors",
                "polynomial_extra_cost": "six-column compatibility kernel plus exact differential closure",
                "verdict": "neither route dominates once discovery provenance and parent-structure explanation are both valued",
            },
            "not_certified": [
                "coordinate-wavefunction phase convention",
                "direct evaluation of Cartesian-angular overlap integrals",
                "a route ranking independent of the requested observable and reusable prior structure",
                "levels above the bounded polynomial-representation certificate",
            ],
        }
    except (AssertionError, KeyError, TypeError, ValueError) as error:
        return {"status": "Refused", "reason": str(error)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--level", type=int, default=2)
    parser.add_argument("--summary", action="store_true")
    arguments = parser.parse_args()
    result = build_interbasis_probe(arguments.input, arguments.level)
    if arguments.summary and result["status"] == "ExactInterbasisCoincidence":
        dimension = result["dimension"]
        print(
            f"{result['status']}: N={result['level']}; {dimension} x {dimension} "
            f"overlap probabilities; {result['route_evaluation']['decision']}"
        )
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "ExactInterbasisCoincidence" else 2


if __name__ == "__main__":
    raise SystemExit(main())

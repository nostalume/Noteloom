"""Exact quadratic-centralizer generator for radial-Laurent coefficients on E^2.

The coefficient algebra is

    Q[x,y,s^(1/2),s^(-1/2)] / (s-x^2-y^2)

with finite support.  Normal forms have x-degree at most one.  The tool applies
the complete six-dimensional Euclidean rank-two Killing module, reconstructs the
lower term, and verifies divergence-ordered quantum commutators exactly.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from quadratic_centralizer import nullspace, ordered_kernel_basis, parse_fraction, rank

Key = tuple[int, int, Fraction]
Derivative = tuple[int, int]


@dataclass(frozen=True)
class RadialExpr:
    terms: dict[Key, Fraction]

    def __post_init__(self) -> None:
        pending = [(key, Fraction(value)) for key, value in self.terms.items() if value]
        reduced: dict[Key, Fraction] = {}
        while pending:
            (x_power, y_power, s_power), coefficient = pending.pop()
            if not coefficient:
                continue
            if x_power < 0 or y_power < 0:
                raise ValueError("coordinate powers must be nonnegative")
            if s_power.denominator not in (1, 2):
                raise ValueError("radius-squared powers must be half-integers")
            if x_power >= 2:
                pending.append(((x_power - 2, y_power, s_power + 1), coefficient))
                pending.append(((x_power - 2, y_power + 2, s_power), -coefficient))
                continue
            key = (x_power, y_power, s_power)
            reduced[key] = reduced.get(key, Fraction(0)) + coefficient
        object.__setattr__(self, "terms", {key: value for key, value in reduced.items() if value})

    @staticmethod
    def constant(value: int | Fraction) -> RadialExpr:
        coefficient = Fraction(value)
        return RadialExpr({(0, 0, Fraction(0)): coefficient}) if coefficient else RadialExpr({})

    @staticmethod
    def monomial(
        x_power: int = 0,
        y_power: int = 0,
        s_power: int | Fraction = 0,
        coefficient: int | Fraction = 1,
    ) -> RadialExpr:
        return RadialExpr({(x_power, y_power, Fraction(s_power)): Fraction(coefficient)})

    def __add__(self, other: RadialExpr) -> RadialExpr:
        terms = dict(self.terms)
        for key, coefficient in other.terms.items():
            terms[key] = terms.get(key, Fraction(0)) + coefficient
        return RadialExpr(terms)

    def __neg__(self) -> RadialExpr:
        return RadialExpr({key: -coefficient for key, coefficient in self.terms.items()})

    def __sub__(self, other: RadialExpr) -> RadialExpr:
        return self + (-other)

    def __mul__(self, other: RadialExpr) -> RadialExpr:
        terms: dict[Key, Fraction] = {}
        for (xi, yi, si), left in self.terms.items():
            for (xj, yj, sj), right in other.terms.items():
                key = (xi + xj, yi + yj, si + sj)
                terms[key] = terms.get(key, Fraction(0)) + left * right
        return RadialExpr(terms)

    def scale(self, value: int | Fraction) -> RadialExpr:
        coefficient = Fraction(value)
        return RadialExpr({key: coefficient * item for key, item in self.terms.items()})

    def derivative_x(self) -> RadialExpr:
        result = RadialExpr.constant(0)
        for (x_power, y_power, s_power), coefficient in self.terms.items():
            if x_power:
                result += RadialExpr.monomial(x_power - 1, y_power, s_power, coefficient * x_power)
            if s_power:
                result += RadialExpr.monomial(
                    x_power + 1, y_power, s_power - 1, 2 * coefficient * s_power
                )
        return result

    def derivative_y(self) -> RadialExpr:
        result = RadialExpr.constant(0)
        for (x_power, y_power, s_power), coefficient in self.terms.items():
            if y_power:
                result += RadialExpr.monomial(x_power, y_power - 1, s_power, coefficient * y_power)
            if s_power:
                result += RadialExpr.monomial(
                    x_power, y_power + 1, s_power - 1, 2 * coefficient * s_power
                )
        return result

    def derivative(self, dx: int = 0, dy: int = 0) -> RadialExpr:
        result = self
        for _ in range(dx):
            result = result.derivative_x()
        for _ in range(dy):
            result = result.derivative_y()
        return result

    def to_json(self) -> list[dict[str, object]]:
        return [
            {
                "powers": [x_power, y_power],
                "radius_squared_power": str(s_power),
                "coefficient": str(coefficient),
            }
            for (x_power, y_power, s_power), coefficient in sorted(self.terms.items(), reverse=True)
        ]


ZERO = RadialExpr.constant(0)
ONE = RadialExpr.constant(1)
X = RadialExpr.monomial(x_power=1)
Y = RadialExpr.monomial(y_power=1)


@dataclass(frozen=True)
class RadialDiffOp:
    terms: dict[Derivative, RadialExpr]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "terms", {key: value for key, value in self.terms.items() if value.terms}
        )

    @staticmethod
    def multiplication(coefficient: RadialExpr) -> RadialDiffOp:
        return RadialDiffOp({(0, 0): coefficient})

    @staticmethod
    def derivative(dx: int = 0, dy: int = 0) -> RadialDiffOp:
        return RadialDiffOp({(dx, dy): ONE})

    def __add__(self, other: RadialDiffOp) -> RadialDiffOp:
        terms = dict(self.terms)
        for derivative, coefficient in other.terms.items():
            terms[derivative] = terms.get(derivative, ZERO) + coefficient
        return RadialDiffOp(terms)

    def __neg__(self) -> RadialDiffOp:
        return RadialDiffOp(
            {derivative: coefficient.scale(-1) for derivative, coefficient in self.terms.items()}
        )

    def __sub__(self, other: RadialDiffOp) -> RadialDiffOp:
        return self + (-other)

    def scale(self, value: int | Fraction) -> RadialDiffOp:
        return RadialDiffOp(
            {derivative: coefficient.scale(value) for derivative, coefficient in self.terms.items()}
        )

    def compose(self, other: RadialDiffOp) -> RadialDiffOp:
        terms: dict[Derivative, RadialExpr] = {}
        for (ax, ay), left in self.terms.items():
            for (bx, by), right in other.terms.items():
                for gx in range(ax + 1):
                    for gy in range(ay + 1):
                        coefficient = (left * right.derivative(gx, gy)).scale(
                            math.comb(ax, gx) * math.comb(ay, gy)
                        )
                        derivative = (ax - gx + bx, ay - gy + by)
                        terms[derivative] = terms.get(derivative, ZERO) + coefficient
        return RadialDiffOp(terms)

    def to_json(self) -> list[dict[str, object]]:
        return [
            {"derivative": list(derivative), "coefficient": coefficient.to_json()}
            for derivative, coefficient in sorted(self.terms.items(), reverse=True)
        ]


DX = RadialDiffOp.derivative(dx=1)
DY = RadialDiffOp.derivative(dy=1)


def killing_tensor(parameters: tuple[Fraction, ...]) -> tuple[RadialExpr, RadialExpr, RadialExpr]:
    a, b, c, d, e, f = parameters
    kxx = (Y * Y).scale(a) + Y.scale(2 * b) + ONE.scale(c)
    kyy = (X * X).scale(a) + X.scale(2 * d) + ONE.scale(e)
    kxy = (X * Y).scale(-a) + X.scale(-b) + Y.scale(-d) + ONE.scale(f)
    return kxx, kxy, kyy


def compatible_one_form(
    potential: RadialExpr, parameters: tuple[Fraction, ...]
) -> tuple[RadialExpr, RadialExpr]:
    kxx, kxy, kyy = killing_tensor(parameters)
    vx = potential.derivative_x()
    vy = potential.derivative_y()
    return kxx * vx + kxy * vy, kxy * vx + kyy * vy


def compatibility_obstruction(
    potential: RadialExpr, parameters: tuple[Fraction, ...]
) -> RadialExpr:
    omega_x, omega_y = compatible_one_form(potential, parameters)
    return omega_y.derivative_x() - omega_x.derivative_y()


def killing_vector(parameters: tuple[Fraction, ...]) -> tuple[RadialExpr, RadialExpr]:
    translation_x, translation_y, rotation = parameters
    return (
        ONE.scale(translation_x) + Y.scale(-rotation),
        ONE.scale(translation_y) + X.scale(rotation),
    )


def first_order_obstruction(potential: RadialExpr, parameters: tuple[Fraction, ...]) -> RadialExpr:
    vector_x, vector_y = killing_vector(parameters)
    return vector_x * potential.derivative_x() + vector_y * potential.derivative_y()


def vector_field_operator(parameters: tuple[Fraction, ...]) -> RadialDiffOp:
    vector_x, vector_y = killing_vector(parameters)
    return RadialDiffOp.multiplication(vector_x).compose(DX) + RadialDiffOp.multiplication(
        vector_y
    ).compose(DY)


def solve_linear(matrix: list[list[Fraction]], target: list[Fraction]) -> list[Fraction] | None:
    if len(matrix) != len(target):
        raise ValueError("linear system shape mismatch")
    columns = len(matrix[0]) if matrix else 0
    rows = [list(row) + [value] for row, value in zip(matrix, target)]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(columns):
        selected = next((row for row in range(pivot_row, len(rows)) if rows[row][column]), None)
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        pivot = rows[pivot_row][column]
        rows[pivot_row] = [value / pivot for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row != pivot_row and rows[row][column]:
                factor = rows[row][column]
                rows[row] = [
                    rows[row][index] - factor * rows[pivot_row][index]
                    for index in range(columns + 1)
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    if any(not any(row[:columns]) and row[-1] for row in rows):
        return None
    solution = [Fraction(0) for _ in range(columns)]
    for row, column in enumerate(pivot_columns):
        solution[column] = rows[row][-1]
    return solution


def reconstruct_lower_term(potential: RadialExpr, parameters: tuple[Fraction, ...]) -> RadialExpr:
    omega_x, omega_y = compatible_one_form(potential, parameters)
    if not omega_x.terms and not omega_y.terms:
        return ZERO

    candidate_keys: set[Key] = set()
    for x_power, y_power, s_power in omega_x.terms:
        candidate_keys.update(RadialExpr.monomial(x_power + 1, y_power, s_power).terms)
        if x_power == 1:
            candidate_keys.update(RadialExpr.monomial(0, y_power, s_power + 1).terms)
    for x_power, y_power, s_power in omega_y.terms:
        candidate_keys.update(RadialExpr.monomial(x_power, y_power + 1, s_power).terms)
        if y_power:
            candidate_keys.update(RadialExpr.monomial(x_power, y_power - 1, s_power + 1).terms)
    candidate_keys.discard((0, 0, Fraction(0)))
    candidates = [RadialExpr({key: Fraction(1)}) for key in sorted(candidate_keys)]

    derivatives = [(candidate.derivative_x(), candidate.derivative_y()) for candidate in candidates]
    row_keys = sorted(
        {(0, key) for key in omega_x.terms}
        | {(1, key) for key in omega_y.terms}
        | {
            (component, key)
            for derivative_pair in derivatives
            for component, derivative in enumerate(derivative_pair)
            for key in derivative.terms
        }
    )
    matrix = [
        [
            derivatives[column][component].terms.get(key, Fraction(0))
            for column in range(len(candidates))
        ]
        for component, key in row_keys
    ]
    target = [
        (omega_x if component == 0 else omega_y).terms.get(key, Fraction(0))
        for component, key in row_keys
    ]
    solution = solve_linear(matrix, target)
    if solution is None:
        raise AssertionError("closed radial one-form was not reconstructed in the admitted algebra")
    lower = sum(
        (candidate.scale(coefficient) for candidate, coefficient in zip(candidates, solution)),
        ZERO,
    )
    if lower.derivative_x() != omega_x or lower.derivative_y() != omega_y:
        raise AssertionError("lower term does not reconstruct K dV")
    return lower


def quantum_operator(parameters: tuple[Fraction, ...], lower: RadialExpr) -> RadialDiffOp:
    kxx, kxy, kyy = killing_tensor(parameters)
    kinetic = (
        DX.compose(RadialDiffOp.multiplication(kxx)).compose(DX)
        + DX.compose(RadialDiffOp.multiplication(kxy)).compose(DY)
        + DY.compose(RadialDiffOp.multiplication(kxy)).compose(DX)
        + DY.compose(RadialDiffOp.multiplication(kyy)).compose(DY)
    ).scale(Fraction(-1, 2))
    return kinetic + RadialDiffOp.multiplication(lower)


def hamiltonian(potential: RadialExpr) -> RadialDiffOp:
    return (DX.compose(DX) + DY.compose(DY)).scale(Fraction(-1, 2)) + RadialDiffOp.multiplication(
        potential
    )


def generate(potential: RadialExpr) -> dict[str, object]:
    unit_vectors = [
        tuple(Fraction(1 if index == column else 0) for index in range(6)) for column in range(6)
    ]
    obstructions = [compatibility_obstruction(potential, vector) for vector in unit_vectors]
    monomials = sorted({key for obstruction in obstructions for key in obstruction.terms})
    matrix = [
        [obstruction.terms.get(key, Fraction(0)) for obstruction in obstructions]
        for key in monomials
    ]
    kernel = ordered_kernel_basis(nullspace(matrix, 6))
    h_op = hamiltonian(potential)

    first_unit_vectors = [
        tuple(Fraction(1 if index == column else 0) for index in range(3)) for column in range(3)
    ]
    first_obstructions = [
        first_order_obstruction(potential, vector) for vector in first_unit_vectors
    ]
    first_monomials = sorted(
        {key for obstruction in first_obstructions for key in obstruction.terms}
    )
    first_matrix = [
        [obstruction.terms.get(key, Fraction(0)) for obstruction in first_obstructions]
        for key in first_monomials
    ]
    first_kernel = nullspace(first_matrix, 3)
    first_generators = []
    all_first_commute = True
    for parameters in first_kernel:
        operator = vector_field_operator(parameters)
        commutator = h_op.compose(operator) - operator.compose(h_op)
        commutes = not commutator.terms
        all_first_commute = all_first_commute and commutes
        vector_x, vector_y = killing_vector(parameters)
        first_generators.append(
            {
                "parameters_translation_x_translation_y_rotation": [
                    str(value) for value in parameters
                ],
                "vector_field": {"x": vector_x.to_json(), "y": vector_y.to_json()},
                "operator": operator.to_json(),
                "commutator_zero": commutes,
            }
        )
    generators = []
    all_commute = True
    for index, parameters in enumerate(kernel):
        lower = reconstruct_lower_term(potential, parameters)
        operator = quantum_operator(parameters, lower)
        commutator = h_op.compose(operator) - operator.compose(h_op)
        commutes = not commutator.terms
        all_commute = all_commute and commutes
        kxx, kxy, kyy = killing_tensor(parameters)
        generators.append(
            {
                "role": "hamiltonian" if index == 0 else "hidden",
                "parameters_abcdef": [str(value) for value in parameters],
                "K": {"xx": kxx.to_json(), "xy": kxy.to_json(), "yy": kyy.to_json()},
                "W": lower.to_json(),
                "quantum_operator": operator.to_json(),
                "commutator_zero": commutes,
            }
        )

    hidden_dimension = len(kernel) - 1
    return {
        "status": "NontrivialQuadraticCentralizer" if hidden_dimension else "MetricOnly",
        "coefficient_domain": "Q[x,y,s^(1/2),s^(-1/2)]/(s-x^2-y^2), finite support",
        "potential": potential.to_json(),
        "killing_module_dimension": 6,
        "first_order_killing_module_dimension": 3,
        "first_order_kernel_dimension": len(first_kernel),
        "first_order_compatibility_rank": rank(first_matrix),
        "first_order_compatibility_system": [
            {
                "monomial": {
                    "powers": [key[0], key[1]],
                    "radius_squared_power": str(key[2]),
                },
                "row": [str(value) for value in row],
            }
            for key, row in zip(first_monomials, first_matrix)
        ],
        "first_order_symmetries": first_generators,
        "kernel_dimension": len(kernel),
        "hidden_quotient_dimension": hidden_dimension,
        "compatibility_rank": rank(matrix),
        "compatibility_system": [
            {
                "monomial": {
                    "powers": [key[0], key[1]],
                    "radius_squared_power": str(key[2]),
                },
                "row": [str(value) for value in row],
            }
            for key, row in zip(monomials, matrix)
        ],
        "generators": generators,
        "certificates": {
            "canonical_normal_form": "x-degree < 2 using x^2=s-y^2",
            "complete_killing_module": "constant-curvature theorem contract",
            "closed_one_form_reconstruction": True,
            "all_formal_quantum_commutators_zero": all_commute,
            "all_first_order_commutators_zero": all_first_commute,
        },
        "not_certified": [
            "behavior at the puncture s=0",
            "self-adjoint extensions and strong commutation",
            "global spectral completeness",
            "integrals outside the scalar even quadratic class",
        ],
    }


def load_potential(path: Path) -> RadialExpr:
    payload = json.loads(path.read_text(encoding="utf-8"))
    terms: dict[Key, Fraction] = {}
    for item in payload["potential"]:
        powers = item["powers"]
        if (
            not isinstance(powers, list)
            or len(powers) != 2
            or not all(isinstance(value, int) and value >= 0 for value in powers)
        ):
            raise ValueError("powers must be two nonnegative integers")
        s_power = Fraction(item.get("radius_squared_power", "0"))
        if s_power.denominator not in (1, 2):
            raise ValueError("radius-squared powers must be half-integers")
        key = (powers[0], powers[1], s_power)
        terms[key] = terms.get(key, Fraction(0)) + parse_fraction(item["coefficient"])
    return RadialExpr(terms)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--summary", action="store_true")
    arguments = parser.parse_args()
    try:
        result = generate(load_potential(arguments.input))
    except (AssertionError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "Refused", "reason": str(error)}, indent=2))
        return 2
    if arguments.summary:
        print(
            f"{result['status']}: six Killing tensors -> kernel "
            f"{result['kernel_dimension']} -> hidden quotient "
            f"{result['hidden_quotient_dimension']}; quantum commutators: "
            f"{result['certificates']['all_formal_quantum_commutators_zero']}"
        )
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

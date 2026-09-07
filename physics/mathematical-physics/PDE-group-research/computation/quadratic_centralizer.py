"""Exact quadratic-centralizer generator for polynomial potentials on E^2.

This tool constructs the complete six-parameter rank-two Killing tensor module,
computes the Bertrand--Darboux kernel, reconstructs scalar lower terms, and checks
the divergence-ordered quantum commutators exactly.  It uses only the standard
library and rational arithmetic.
"""

from __future__ import annotations

import argparse
import json
import math
from collections.abc import Iterable
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from linear_defect_compiler import DefectBlock, DefectBudget, compile_defects

Power = tuple[int, int]
Derivative = tuple[int, int]


def parse_fraction(value: object) -> Fraction:
    if isinstance(value, (bool, float)):
        raise ValueError("coefficients must be exact integers or rational strings")
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    raise ValueError("coefficients must be exact integers or rational strings")


@dataclass(frozen=True)
class Poly:
    terms: dict[Power, Fraction]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "terms", {key: value for key, value in self.terms.items() if value}
        )

    @staticmethod
    def constant(value: int | Fraction) -> Poly:
        coefficient = Fraction(value)
        return Poly({(0, 0): coefficient}) if coefficient else Poly({})

    @staticmethod
    def monomial(power: Power, coefficient: int | Fraction = 1) -> Poly:
        return Poly({power: Fraction(coefficient)})

    def __add__(self, other: Poly) -> Poly:
        terms = dict(self.terms)
        for power, coefficient in other.terms.items():
            terms[power] = terms.get(power, Fraction(0)) + coefficient
        return Poly(terms)

    def __neg__(self) -> Poly:
        return Poly({power: -coefficient for power, coefficient in self.terms.items()})

    def __sub__(self, other: Poly) -> Poly:
        return self + (-other)

    def __mul__(self, other: Poly) -> Poly:
        terms: dict[Power, Fraction] = {}
        for (ix, iy), left in self.terms.items():
            for (jx, jy), right in other.terms.items():
                power = (ix + jx, iy + jy)
                terms[power] = terms.get(power, Fraction(0)) + left * right
        return Poly(terms)

    def scale(self, value: int | Fraction) -> Poly:
        coefficient = Fraction(value)
        return Poly({power: coefficient * item for power, item in self.terms.items()})

    def derivative(self, dx: int = 0, dy: int = 0) -> Poly:
        result = self
        for _ in range(dx):
            result = Poly(
                {
                    (ix - 1, iy): coefficient * ix
                    for (ix, iy), coefficient in result.terms.items()
                    if ix
                }
            )
        for _ in range(dy):
            result = Poly(
                {
                    (ix, iy - 1): coefficient * iy
                    for (ix, iy), coefficient in result.terms.items()
                    if iy
                }
            )
        return result

    def integrate_x(self) -> Poly:
        return Poly(
            {(ix + 1, iy): coefficient / (ix + 1) for (ix, iy), coefficient in self.terms.items()}
        )

    def integrate_y(self) -> Poly:
        return Poly(
            {(ix, iy + 1): coefficient / (iy + 1) for (ix, iy), coefficient in self.terms.items()}
        )

    def to_json(self) -> list[dict[str, object]]:
        return [
            {"powers": [ix, iy], "coefficient": str(coefficient)}
            for (ix, iy), coefficient in sorted(self.terms.items(), reverse=True)
        ]


ZERO = Poly.constant(0)
ONE = Poly.constant(1)
X = Poly.monomial((1, 0))
Y = Poly.monomial((0, 1))


@dataclass(frozen=True)
class DiffOp:
    terms: dict[Derivative, Poly]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "terms", {key: value for key, value in self.terms.items() if value.terms}
        )

    @staticmethod
    def multiplication(coefficient: Poly) -> DiffOp:
        return DiffOp({(0, 0): coefficient})

    @staticmethod
    def derivative(dx: int = 0, dy: int = 0) -> DiffOp:
        return DiffOp({(dx, dy): ONE})

    def __add__(self, other: DiffOp) -> DiffOp:
        terms = dict(self.terms)
        for derivative, coefficient in other.terms.items():
            terms[derivative] = terms.get(derivative, ZERO) + coefficient
        return DiffOp(terms)

    def __neg__(self) -> DiffOp:
        return DiffOp(
            {derivative: coefficient.scale(-1) for derivative, coefficient in self.terms.items()}
        )

    def __sub__(self, other: DiffOp) -> DiffOp:
        return self + (-other)

    def scale(self, value: int | Fraction) -> DiffOp:
        return DiffOp(
            {derivative: coefficient.scale(value) for derivative, coefficient in self.terms.items()}
        )

    def compose(self, other: DiffOp) -> DiffOp:
        terms: dict[Derivative, Poly] = {}
        for (ax, ay), left in self.terms.items():
            for (bx, by), right in other.terms.items():
                for gx in range(ax + 1):
                    for gy in range(ay + 1):
                        coefficient = (left * right.derivative(gx, gy)).scale(
                            math.comb(ax, gx) * math.comb(ay, gy)
                        )
                        derivative = (ax - gx + bx, ay - gy + by)
                        terms[derivative] = terms.get(derivative, ZERO) + coefficient
        return DiffOp(terms)

    def to_json(self) -> list[dict[str, object]]:
        return [
            {"derivative": list(derivative), "coefficient": coefficient.to_json()}
            for derivative, coefficient in sorted(self.terms.items(), reverse=True)
        ]


DX = DiffOp.derivative(dx=1)
DY = DiffOp.derivative(dy=1)


def killing_tensor(parameters: tuple[Fraction, ...]) -> tuple[Poly, Poly, Poly]:
    a, b, c, d, e, f = parameters
    kxx = (Y * Y).scale(a) + Y.scale(2 * b) + ONE.scale(c)
    kyy = (X * X).scale(a) + X.scale(2 * d) + ONE.scale(e)
    kxy = (X * Y).scale(-a) + X.scale(-b) + Y.scale(-d) + ONE.scale(f)
    return kxx, kxy, kyy


def compatibility_obstruction(potential: Poly, parameters: tuple[Fraction, ...]) -> Poly:
    kxx, kxy, kyy = killing_tensor(parameters)
    vx = potential.derivative(dx=1)
    vy = potential.derivative(dy=1)
    omega_x = kxx * vx + kxy * vy
    omega_y = kxy * vx + kyy * vy
    return omega_y.derivative(dx=1) - omega_x.derivative(dy=1)


def reconstruct_lower_term(potential: Poly, parameters: tuple[Fraction, ...]) -> Poly:
    kxx, kxy, kyy = killing_tensor(parameters)
    vx = potential.derivative(dx=1)
    vy = potential.derivative(dy=1)
    omega_x = kxx * vx + kxy * vy
    omega_y = kxy * vx + kyy * vy
    provisional = omega_x.integrate_x()
    remainder = omega_y - provisional.derivative(dy=1)
    if remainder.derivative(dx=1).terms:
        raise AssertionError("closed one-form reconstruction failed")
    lower = provisional + remainder.integrate_y()
    if lower.derivative(dx=1) != omega_x or lower.derivative(dy=1) != omega_y:
        raise AssertionError("lower term does not reconstruct K dV")
    return lower


def nullspace(matrix: list[list[Fraction]], columns: int) -> list[tuple[Fraction, ...]]:
    rows = [list(row) for row in matrix if any(row)]
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
                    rows[row][index] - factor * rows[pivot_row][index] for index in range(columns)
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break

    free_columns = [column for column in range(columns) if column not in pivot_columns]
    basis: list[tuple[Fraction, ...]] = []
    for free in free_columns:
        vector = [Fraction(0) for _ in range(columns)]
        vector[free] = Fraction(1)
        for row, pivot in enumerate(pivot_columns):
            vector[pivot] = -rows[row][free]
        basis.append(tuple(vector))
    return basis


def rank(vectors: Iterable[tuple[Fraction, ...]]) -> int:
    rows = [list(vector) for vector in vectors]
    if not rows:
        return 0
    return len(rows[0]) - len(nullspace(rows, len(rows[0])))


def ordered_kernel_basis(kernel: list[tuple[Fraction, ...]]) -> list[tuple[Fraction, ...]]:
    metric = (Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(1), Fraction(0))
    ordered = [metric]
    current_rank = 1
    for vector in kernel:
        candidate_rank = rank([*ordered, vector])
        if candidate_rank > current_rank:
            ordered.append(vector)
            current_rank = candidate_rank
    if len(ordered) != len(kernel):
        raise AssertionError("metric was not contained in compatibility kernel")
    return ordered


def quantum_operator(parameters: tuple[Fraction, ...], lower: Poly) -> DiffOp:
    kxx, kxy, kyy = killing_tensor(parameters)
    kinetic = (
        DX.compose(DiffOp.multiplication(kxx)).compose(DX)
        + DX.compose(DiffOp.multiplication(kxy)).compose(DY)
        + DY.compose(DiffOp.multiplication(kxy)).compose(DX)
        + DY.compose(DiffOp.multiplication(kyy)).compose(DY)
    ).scale(Fraction(-1, 2))
    return kinetic + DiffOp.multiplication(lower)


def hamiltonian(potential: Poly) -> DiffOp:
    return (DX.compose(DX) + DY.compose(DY)).scale(Fraction(-1, 2)) + DiffOp.multiplication(
        potential
    )


def generate(potential: Poly) -> dict[str, object]:
    unit_vectors = [
        tuple(Fraction(1 if index == column else 0) for index in range(6)) for column in range(6)
    ]
    obstructions = [compatibility_obstruction(potential, vector) for vector in unit_vectors]
    killing_checks = []
    for vector in unit_vectors:
        kxx, kxy, kyy = killing_tensor(vector)
        killing_checks.extend(
            [
                not kxx.derivative(dx=1).terms,
                not kyy.derivative(dy=1).terms,
                not (kxy.derivative(dx=1).scale(2) + kxx.derivative(dy=1)).terms,
                not (kyy.derivative(dx=1) + kxy.derivative(dy=1).scale(2)).terms,
            ]
        )
    monomials = sorted({power for obstruction in obstructions for power in obstruction.terms})
    matrix = [
        [obstruction.terms.get(power, Fraction(0)) for obstruction in obstructions]
        for power in monomials
    ]
    defect_result = compile_defects(
        candidate_labels=("a", "b", "c", "d", "e", "f"),
        blocks=(
            DefectBlock(
                name="bertrand-darboux-compatibility",
                target_labels=tuple(str(power) for power in monomials),
                columns=tuple(
                    tuple(obstruction.terms.get(power, Fraction(0)) for power in monomials)
                    for obstruction in obstructions
                ),
            ),
        ),
        budget=DefectBudget(6, len(monomials)),
    )
    if defect_result.outcome != "exact":
        raise AssertionError("the fixed quadratic-centralizer defect budget was refused")
    kernel = ordered_kernel_basis(list(defect_result.kernel_basis))
    h_op = hamiltonian(potential)
    generators = []
    all_commute = True
    for index, parameters in enumerate(kernel):
        lower = reconstruct_lower_term(potential, parameters)
        operator = quantum_operator(parameters, lower)
        commutator = h_op.compose(operator) - operator.compose(h_op)
        commutes = not commutator.terms
        all_commute = all_commute and commutes
        generators.append(
            {
                "role": "hamiltonian" if index == 0 else "hidden",
                "parameters_abcdef": [str(value) for value in parameters],
                "K": {
                    "xx": killing_tensor(parameters)[0].to_json(),
                    "xy": killing_tensor(parameters)[1].to_json(),
                    "yy": killing_tensor(parameters)[2].to_json(),
                },
                "W": lower.to_json(),
                "quantum_operator": operator.to_json(),
                "commutator_zero": commutes,
            }
        )

    hidden_dimension = len(kernel) - 1
    return {
        "status": "NontrivialQuadraticCentralizer" if hidden_dimension else "MetricOnly",
        "coefficient_domain": "Q[x,y]",
        "potential": potential.to_json(),
        "killing_module_dimension": 6,
        "killing_module_parameter_order": ["a", "b", "c", "d", "e", "f"],
        "killing_module_basis_parameters": [
            [str(value) for value in vector] for vector in unit_vectors
        ],
        "compatibility_system": [
            {
                "monomial": list(power),
                "row": [str(value) for value in row],
            }
            for power, row in zip(monomials, matrix)
        ],
        "compatibility_rank": defect_result.ledger[0].residual_rank,
        "kernel_dimension": len(kernel),
        "hidden_quotient_dimension": hidden_dimension,
        "defect_compilation": {
            "block": defect_result.ledger[0].name,
            "target_dimension": defect_result.ledger[0].target_dimension,
            "rank_drop": defect_result.ledger[0].rank_drop,
        },
        "generators": generators,
        "certificates": {
            "all_six_basis_tensors_satisfy_killing_equation": all(killing_checks),
            "complete_killing_module": "constant-curvature generation theorem plus displayed six-parameter solution",
            "closed_one_form_reconstruction": True,
            "all_formal_quantum_commutators_zero": all_commute,
        },
        "not_certified": [
            "operator closure and strong commutation on a Hilbert-space domain",
            "self-adjoint extensions and boundary conditions",
            "spectral completeness or numerical advantage",
            "integrals outside the scalar even quadratic class",
        ],
        "cost": {
            "candidate_module_dimension": 6,
            "compatibility_equations": len(matrix),
            "linear_unknowns": 6,
        },
    }


def load_potential(path: Path) -> Poly:
    payload = json.loads(path.read_text(encoding="utf-8"))
    terms: dict[Power, Fraction] = {}
    for item in payload["potential"]:
        powers = item["powers"]
        if (
            not isinstance(powers, list)
            or len(powers) != 2
            or not all(isinstance(value, int) and value >= 0 for value in powers)
        ):
            raise ValueError("powers must be two nonnegative integers")
        power = (powers[0], powers[1])
        terms[power] = terms.get(power, Fraction(0)) + parse_fraction(item["coefficient"])
    return Poly(terms)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--summary", action="store_true")
    arguments = parser.parse_args()
    try:
        result = generate(load_potential(arguments.input))
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
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

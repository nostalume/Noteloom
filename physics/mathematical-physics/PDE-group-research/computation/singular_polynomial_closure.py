"""Group-free polynomial-closure constructor for a singular E2 oscillator.

The input supplies only exact PDE coefficients and an analytic-domain tag. The
tool generates the complete rank-two Euclidean Killing module, lets the
potential select its compatibility kernel, lifts every survivor to a quantum
differential operator, and classifies the commutator closure without a group
name or a catalogue of known integrals.
"""

from __future__ import annotations

import argparse
import json
import math
from collections.abc import Iterable
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

Power = tuple[int, int]
Derivative = tuple[int, int]


def _fraction(value: object) -> Fraction:
    if isinstance(value, (bool, float)):
        raise ValueError("coefficients must be exact integers or rational strings")
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    raise ValueError("coefficients must be exact integers or rational strings")


@dataclass(frozen=True)
class Laurent:
    terms: dict[Power, Fraction]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "terms", {power: value for power, value in self.terms.items() if value}
        )

    @staticmethod
    def constant(value: int | Fraction) -> Laurent:
        coefficient = Fraction(value)
        return Laurent({(0, 0): coefficient}) if coefficient else Laurent({})

    @staticmethod
    def monomial(power: Power, value: int | Fraction = 1) -> Laurent:
        coefficient = Fraction(value)
        return Laurent({power: coefficient}) if coefficient else Laurent({})

    def __add__(self, other: Laurent) -> Laurent:
        terms = dict(self.terms)
        for power, coefficient in other.terms.items():
            terms[power] = terms.get(power, Fraction(0)) + coefficient
        return Laurent(terms)

    def __neg__(self) -> Laurent:
        return Laurent({power: -coefficient for power, coefficient in self.terms.items()})

    def __sub__(self, other: Laurent) -> Laurent:
        return self + (-other)

    def __mul__(self, other: Laurent) -> Laurent:
        terms: dict[Power, Fraction] = {}
        for (ix, iy), left in self.terms.items():
            for (jx, jy), right in other.terms.items():
                power = (ix + jx, iy + jy)
                terms[power] = terms.get(power, Fraction(0)) + left * right
        return Laurent(terms)

    def scale(self, value: int | Fraction) -> Laurent:
        coefficient = Fraction(value)
        return Laurent({power: coefficient * item for power, item in self.terms.items()})

    def derivative(self, dx: int = 0, dy: int = 0) -> Laurent:
        result = self
        for _ in range(dx):
            result = Laurent(
                {
                    (ix - 1, iy): coefficient * ix
                    for (ix, iy), coefficient in result.terms.items()
                    if ix
                }
            )
        for _ in range(dy):
            result = Laurent(
                {
                    (ix, iy - 1): coefficient * iy
                    for (ix, iy), coefficient in result.terms.items()
                    if iy
                }
            )
        return result

    def integrate_x(self) -> Laurent:
        if any(ix == -1 for ix, _ in self.terms):
            raise ValueError("compatible lower term would require a logarithm in x")
        return Laurent({(ix + 1, iy): value / (ix + 1) for (ix, iy), value in self.terms.items()})

    def integrate_y(self) -> Laurent:
        if any(iy == -1 for _, iy in self.terms):
            raise ValueError("compatible lower term would require a logarithm in y")
        return Laurent({(ix, iy + 1): value / (iy + 1) for (ix, iy), value in self.terms.items()})

    def to_json(self) -> list[dict[str, object]]:
        return [
            {"powers": [ix, iy], "coefficient": str(value)}
            for (ix, iy), value in sorted(self.terms.items(), reverse=True)
        ]


ZERO = Laurent.constant(0)
ONE = Laurent.constant(1)
X = Laurent.monomial((1, 0))
Y = Laurent.monomial((0, 1))


@dataclass(frozen=True)
class DiffOp:
    terms: dict[Derivative, Laurent]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "terms",
            {derivative: value for derivative, value in self.terms.items() if value.terms},
        )

    @staticmethod
    def multiplication(value: Laurent) -> DiffOp:
        return DiffOp({(0, 0): value})

    @staticmethod
    def derivative(dx: int = 0, dy: int = 0) -> DiffOp:
        return DiffOp({(dx, dy): ONE})

    @staticmethod
    def identity() -> DiffOp:
        return DiffOp.multiplication(ONE)

    def __add__(self, other: DiffOp) -> DiffOp:
        terms = dict(self.terms)
        for derivative, value in other.terms.items():
            terms[derivative] = terms.get(derivative, ZERO) + value
        return DiffOp(terms)

    def __neg__(self) -> DiffOp:
        return DiffOp({derivative: value.scale(-1) for derivative, value in self.terms.items()})

    def __sub__(self, other: DiffOp) -> DiffOp:
        return self + (-other)

    def scale(self, value: int | Fraction) -> DiffOp:
        return DiffOp(
            {derivative: coefficient.scale(value) for derivative, coefficient in self.terms.items()}
        )

    def compose(self, other: DiffOp) -> DiffOp:
        terms: dict[Derivative, Laurent] = {}
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

    def commutator(self, other: DiffOp) -> DiffOp:
        return self.compose(other) - other.compose(self)

    def order(self) -> int:
        return max((sum(derivative) for derivative in self.terms), default=-1)


DX = DiffOp.derivative(dx=1)
DY = DiffOp.derivative(dy=1)


def _nullspace(matrix: list[list[Fraction]], columns: int) -> list[tuple[Fraction, ...]]:
    rows = [list(row) for row in matrix if any(row)]
    pivots: list[int] = []
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
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    free = [column for column in range(columns) if column not in pivots]
    basis: list[tuple[Fraction, ...]] = []
    for column in free:
        vector = [Fraction(0) for _ in range(columns)]
        vector[column] = Fraction(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -rows[row][column]
        basis.append(tuple(vector))
    return basis


def _rank(vectors: Iterable[tuple[Fraction, ...]]) -> int:
    rows = [list(vector) for vector in vectors]
    return 0 if not rows else len(rows[0]) - len(_nullspace(rows, len(rows[0])))


def _solve(
    matrix: list[list[Fraction]], target: list[Fraction], columns: int
) -> list[Fraction] | None:
    rows = [list(row) + [value] for row, value in zip(matrix, target)]
    pivots: list[int] = []
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
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    if any(not any(row[:columns]) and row[columns] for row in rows):
        return None
    result = [Fraction(0) for _ in range(columns)]
    for row, pivot in enumerate(pivots):
        result[pivot] = rows[row][columns]
    return result


def _killing_tensor(parameters: tuple[Fraction, ...]) -> tuple[Laurent, Laurent, Laurent]:
    a, b, c, d, e, f = parameters
    return (
        (Y * Y).scale(a) + Y.scale(2 * b) + ONE.scale(c),
        (X * Y).scale(-a) + X.scale(-b) + Y.scale(-d) + ONE.scale(f),
        (X * X).scale(a) + X.scale(2 * d) + ONE.scale(e),
    )


def _obstruction(potential: Laurent, parameters: tuple[Fraction, ...]) -> Laurent:
    kxx, kxy, kyy = _killing_tensor(parameters)
    vx = potential.derivative(dx=1)
    vy = potential.derivative(dy=1)
    omega_x = kxx * vx + kxy * vy
    omega_y = kxy * vx + kyy * vy
    return omega_y.derivative(dx=1) - omega_x.derivative(dy=1)


def _lower_term(potential: Laurent, parameters: tuple[Fraction, ...]) -> Laurent:
    kxx, kxy, kyy = _killing_tensor(parameters)
    vx = potential.derivative(dx=1)
    vy = potential.derivative(dy=1)
    omega_x = kxx * vx + kxy * vy
    omega_y = kxy * vx + kyy * vy
    provisional = omega_x.integrate_x()
    remainder = omega_y - provisional.derivative(dy=1)
    if remainder.derivative(dx=1).terms:
        raise AssertionError("closed one-form reconstruction failed")
    result = provisional + remainder.integrate_y()
    if result.derivative(dx=1) != omega_x or result.derivative(dy=1) != omega_y:
        raise AssertionError("lower term does not reconstruct K dV")
    return result


def _quantum_operator(parameters: tuple[Fraction, ...], lower: Laurent) -> DiffOp:
    kxx, kxy, kyy = _killing_tensor(parameters)
    kinetic = (
        DX.compose(DiffOp.multiplication(kxx)).compose(DX)
        + DX.compose(DiffOp.multiplication(kxy)).compose(DY)
        + DY.compose(DiffOp.multiplication(kxy)).compose(DX)
        + DY.compose(DiffOp.multiplication(kyy)).compose(DY)
    ).scale(Fraction(-1, 2))
    return kinetic + DiffOp.multiplication(lower)


def _hamiltonian(potential: Laurent) -> DiffOp:
    return (DX.compose(DX) + DY.compose(DY)).scale(Fraction(-1, 2)) + DiffOp.multiplication(
        potential
    )


def _ordered_kernel(kernel: list[tuple[Fraction, ...]]) -> list[tuple[Fraction, ...]]:
    metric = (Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(1), Fraction(0))
    ordered = [metric]
    current_rank = 1
    for vector in kernel:
        candidate_rank = _rank([*ordered, vector])
        if candidate_rank > current_rank:
            ordered.append(vector)
            current_rank = candidate_rank
    if len(ordered) != len(kernel):
        raise AssertionError("metric is absent from the compatibility kernel")
    return ordered


def _operator_coordinates(operator: DiffOp) -> dict[tuple[Derivative, Power], Fraction]:
    return {
        (derivative, power): coefficient
        for derivative, laurent in operator.terms.items()
        for power, coefficient in laurent.terms.items()
    }


def _fit(target: DiffOp, candidates: list[tuple[str, DiffOp]]) -> dict[str, Fraction] | None:
    target_coordinates = _operator_coordinates(target)
    candidate_coordinates = [_operator_coordinates(operator) for _, operator in candidates]
    keys = sorted(set(target_coordinates).union(*(set(item) for item in candidate_coordinates)))
    matrix = [[item.get(key, Fraction(0)) for item in candidate_coordinates] for key in keys]
    values = [target_coordinates.get(key, Fraction(0)) for key in keys]
    solution = _solve(matrix, values, len(candidates))
    if solution is None:
        return None
    reconstructed = DiffOp({})
    for coefficient, (_, candidate) in zip(solution, candidates):
        reconstructed += candidate.scale(coefficient)
    if reconstructed != target:
        raise AssertionError("reported closure relation does not reconstruct the commutator")
    return {
        label: coefficient for coefficient, (label, _) in zip(solution, candidates) if coefficient
    }


def _closure(hamiltonian: DiffOp, first: DiffOp, second: DiffOp) -> dict[str, object]:
    identity = DiffOp.identity()
    commutator = first.commutator(second)
    targets = {
        "[A,R]": first.commutator(commutator),
        "[B,R]": second.commutator(commutator),
    }
    linear = [("1", identity), ("H", hamiltonian), ("A", first), ("B", second)]
    quadratic = [
        *linear,
        ("H^2", hamiltonian.compose(hamiltonian)),
        ("H*A", hamiltonian.compose(first)),
        ("H*B", hamiltonian.compose(second)),
        ("A^2", first.compose(first)),
        ("{A,B}", first.compose(second) + second.compose(first)),
        ("B^2", second.compose(second)),
    ]
    linear_relations = {name: _fit(target, linear) for name, target in targets.items()}
    quadratic_relations = {name: _fit(target, quadratic) for name, target in targets.items()}
    linear_closure = all(relation is not None for relation in linear_relations.values())
    quadratic_closure = all(relation is not None for relation in quadratic_relations.values())
    degree_two = {"H^2", "H*A", "H*B", "A^2", "{A,B}", "B^2"}
    nonlinear = sorted(
        {
            label
            for relation in quadratic_relations.values()
            if relation is not None
            for label, coefficient in relation.items()
            if label in degree_two and coefficient
        }
    )
    if linear_closure:
        classification = "LieAlgebra"
    elif quadratic_closure and nonlinear:
        classification = "PolynomialAlgebra"
    else:
        classification = "UnresolvedWithinBudget"
    return {
        "classification": classification,
        "linear_closure": linear_closure,
        "quadratic_closure": quadratic_closure,
        "commutator_order": commutator.order(),
        "relations": {
            name: {label: str(value) for label, value in (relation or {}).items()}
            for name, relation in quadratic_relations.items()
        },
        "nonlinear_coefficients": nonlinear,
        "word_budget": [label for label, _ in quadratic],
        "semantic_statement": "R=[A,B]; both [A,R] and [B,R] close in degree <=2 words in central H,A,B",
    }


def _sqrt_fraction(value: Fraction, label: str) -> Fraction:
    if value < 0:
        raise ValueError(f"{label} must be nonnegative")
    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        raise ValueError(
            f"{label} must have a rational square root for the exact spectral baseline"
        )
    return Fraction(numerator, denominator)


def _load(path: Path) -> tuple[dict[str, object], Laurent]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    wx2 = _fraction(payload["omega_x_squared"])
    wy2 = _fraction(payload["omega_y_squared"])
    gx = _fraction(payload["g_x"])
    gy = _fraction(payload["g_y"])
    if wx2 <= 0 or wy2 <= 0:
        raise ValueError("frequency squares must be positive")
    if gx < Fraction(3, 4) or gy < Fraction(3, 4):
        raise ValueError("this bench requires g_x,g_y >= 3/4 to avoid boundary-extension ambiguity")
    if payload.get("domain") != "positive-quadrant-essentially-self-adjoint":
        raise ValueError("the positive-quadrant essentially-self-adjoint domain tag is required")
    potential = (
        Laurent.monomial((2, 0), wx2 / 2)
        + Laurent.monomial((0, 2), wy2 / 2)
        + Laurent.monomial((-2, 0), gx / 2)
        + Laurent.monomial((0, -2), gy / 2)
    )
    return {
        "omega_x_squared": wx2,
        "omega_y_squared": wy2,
        "g_x": gx,
        "g_y": gy,
        "domain": payload["domain"],
    }, potential


def _spectrum(model: dict[str, object]) -> dict[str, object] | None:
    wx2 = model["omega_x_squared"]
    wy2 = model["omega_y_squared"]
    if wx2 != wy2:
        return None
    omega = _sqrt_fraction(wx2, "omega_squared")
    nu_x = _sqrt_fraction(model["g_x"] + Fraction(1, 4), "g_x+1/4")
    nu_y = _sqrt_fraction(model["g_y"] + Fraction(1, 4), "g_y+1/4")
    offset = omega * (2 + nu_x + nu_y)
    spacing = 2 * omega
    return {
        "one_dimensional_factors": [
            f"E_x(n_x)={2 * omega}*n_x+{omega * (1 + nu_x)}",
            f"E_y(n_y)={2 * omega}*n_y+{omega * (1 + nu_y)}",
        ],
        "energy_family": f"E_N={spacing}*N+{offset}",
        "degeneracy": "N+1",
        "counting_witness": "n_x+n_y=N has N+1 nonnegative-integer solutions",
        "analytic_contract": "half-line singular-oscillator lowest weights on the declared limit-point domain",
    }


def _relation_fraction(relation: dict[str, str], label: str) -> Fraction:
    return Fraction(relation.get(label, "0"))


def _diagonal_word_value(
    relation: dict[str, str], energy: Fraction, b_value: Fraction, a_value: Fraction
) -> Fraction:
    if _relation_fraction(relation, "A^2"):
        raise ValueError("representation adapter does not admit A^2 in a diagonal closure relation")
    values = {
        "1": Fraction(1),
        "H": energy,
        "A": a_value,
        "B": b_value,
        "H^2": energy * energy,
        "H*A": energy * a_value,
        "H*B": energy * b_value,
        "{A,B}": 2 * a_value * b_value,
        "B^2": b_value * b_value,
    }
    return sum(
        (_relation_fraction(relation, label) * value for label, value in values.items()),
        Fraction(0),
    )


def _diagonal_a(relation: dict[str, str], energy: Fraction, b_value: Fraction) -> Fraction:
    a_coefficient = (
        _relation_fraction(relation, "A")
        + energy * _relation_fraction(relation, "H*A")
        + 2 * b_value * _relation_fraction(relation, "{A,B}")
    )
    if not a_coefficient or _relation_fraction(relation, "A^2"):
        raise ValueError("[B,R] does not determine the diagonal of A in the admitted adapter")
    known = _diagonal_word_value(relation, energy, b_value, Fraction(0))
    return -known / a_coefficient


def _endpoint_value(
    relation_ar: dict[str, str],
    relation_br: dict[str, str],
    energy: Fraction,
    level: int,
    b_zero: Fraction,
    step: Fraction,
) -> tuple[Fraction, list[Fraction], list[Fraction]]:
    off_diagonal_squared = Fraction(0)
    squares: list[Fraction] = []
    diagonals: list[Fraction] = []
    for n in range(level + 1):
        b_value = b_zero + step * n
        a_value = _diagonal_a(relation_br, energy, b_value)
        diagonals.append(a_value)
        right = _diagonal_word_value(relation_ar, energy, b_value, a_value)
        off_diagonal_squared -= right / (2 * step)
        squares.append(off_diagonal_squared)
    return off_diagonal_squared, squares, diagonals


def _quadratic_roots_from_samples(values: list[Fraction]) -> list[Fraction]:
    if len(values) != 3:
        raise ValueError("three endpoint samples are required")
    constant = values[0]
    quadratic = (values[2] - 2 * values[1] + values[0]) / 2
    linear = values[1] - constant - quadratic
    if not quadratic:
        if not linear:
            raise ValueError("endpoint equation does not determine an energy")
        return [-constant / linear]
    discriminant = linear * linear - 4 * quadratic * constant
    root = _sqrt_fraction(discriminant, "endpoint discriminant")
    return sorted(
        [
            (-linear - root) / (2 * quadratic),
            (-linear + root) / (2 * quadratic),
        ]
    )


def _representation_adapter(
    closure: dict[str, object], model: dict[str, object], maximum_level: int = 4
) -> dict[str, object]:
    relation_ar = closure["relations"]["[A,R]"]
    relation_br = closure["relations"]["[B,R]"]
    if any(_relation_fraction(relation_br, label) for label in ("H*A", "{A,B}", "A^2")):
        raise ValueError("[B,R] does not force a constant-step B lattice")
    step = _sqrt_fraction(-_relation_fraction(relation_br, "A"), "B lattice step squared")
    omega = _sqrt_fraction(model["omega_x_squared"], "omega_squared")
    nu_x = _sqrt_fraction(model["g_x"] + Fraction(1, 4), "g_x+1/4")
    nu_y = _sqrt_fraction(model["g_y"] + Fraction(1, 4), "g_y+1/4")
    k_x = (1 + nu_x) / 2
    k_y = (1 + nu_y) / 2
    b_zero = omega * (1 + nu_x)
    complementary_lower_bound = omega * (1 + nu_y)
    levels = []
    all_unique = True
    all_positive = True
    all_formulae = True
    for level in range(maximum_level + 1):
        endpoint_samples = [
            _endpoint_value(relation_ar, relation_br, Fraction(sample), level, b_zero, step)[0]
            for sample in range(3)
        ]
        roots = _quadratic_roots_from_samples(endpoint_samples)
        admissible: list[tuple[Fraction, list[Fraction], list[Fraction]]] = []
        for energy in roots:
            endpoint, squares, diagonals = _endpoint_value(
                relation_ar, relation_br, energy, level, b_zero, step
            )
            positive = all(value > 0 for value in squares[:-1])
            central_bound = energy >= b_zero + complementary_lower_bound
            if endpoint == 0 and positive and central_bound:
                admissible.append((energy, squares, diagonals))
        all_unique = all_unique and len(admissible) == 1
        if len(admissible) != 1:
            raise ValueError(f"level {level} does not have one positive endpoint representation")
        energy, squares, diagonals = admissible[0]
        expected_energy = 2 * omega * level + omega * (2 + nu_x + nu_y)
        expected_squares = [
            4 * (n + 1) * (Fraction(n) + nu_x + 1) * (level - n) * (Fraction(level - n) + nu_y)
            for n in range(level + 1)
        ]
        all_positive = (
            all_positive and all(value > 0 for value in squares[:-1]) and squares[-1] == 0
        )
        all_formulae = all_formulae and energy == expected_energy and squares == expected_squares
        levels.append(
            {
                "N": level,
                "dimension": level + 1,
                "energy_candidates": [str(value) for value in roots],
                "selected_energy": str(energy),
                "B_eigenvalues": [str(b_zero + step * n) for n in range(level + 1)],
                "A_diagonal": [str(value) for value in diagonals],
                "A_off_diagonal_squared": [str(value) for value in squares],
            }
        )
    return {
        "status": "ExactPositiveFiniteRepresentations",
        "construction": "diagonalize B; closure forces its step, A diagonal, and Jacobi off-diagonal norms",
        "parameters": {
            "omega": str(omega),
            "nu_x": str(nu_x),
            "nu_y": str(nu_y),
            "k_x": str(k_x),
            "k_y": str(k_y),
        },
        "B_lattice": "b_n=2*omega*(n+k_x)",
        "A_diagonal": "a_n=(E*b_n-b_n^2)/omega^2-1/4",
        "endpoint_equation": "u_(N+1)^2(E)=0; exact candidates are recorded at each level",
        "selection": "internal norm positivity plus H-B >= 2*omega*k_y selects the physical root",
        "energy_family": "E_N=2*omega*(N+k_x+k_y)",
        "off_diagonal_squared": "u_(n+1)^2=4(n+1)(n+2*k_x)(N-n)(N-n+2*k_y-1)",
        "interbasis_recurrence": "P_(n+1)(lambda)=(lambda-a_n)P_n(lambda)-u_n^2 P_(n-1)(lambda)",
        "levels": levels,
        "certificates": {
            "B_step_forced_by_[B,R]": step == 2 * omega,
            "unique_positive_representation_each_tested_level": all_unique,
            "endpoint_and_internal_positivity": all_positive,
            "closed_energy_and_norm_formulae_recovered": all_formulae,
        },
        "proof_boundary": "closed formula follows by finite arithmetic summation; executable levels 0 through 4 are regression certificates",
    }


def build_polynomial_closure(path: Path) -> dict[str, object]:
    """Generate the complete quadratic centralizer and classify its closure."""

    try:
        model, potential = _load(Path(path))
        unit_vectors = [
            tuple(Fraction(int(index == column)) for index in range(6)) for column in range(6)
        ]
        obstructions = [_obstruction(potential, vector) for vector in unit_vectors]
        monomials = sorted({power for obstruction in obstructions for power in obstruction.terms})
        matrix = [
            [obstruction.terms.get(power, Fraction(0)) for obstruction in obstructions]
            for power in monomials
        ]
        kernel = _ordered_kernel(_nullspace(matrix, 6))
        hamiltonian = _hamiltonian(potential)
        operators: list[DiffOp] = []
        generators = []
        for index, parameters in enumerate(kernel):
            lower = _lower_term(potential, parameters)
            operator = _quantum_operator(parameters, lower)
            operators.append(operator)
            generators.append(
                {
                    "role": "hamiltonian" if index == 0 else "hidden",
                    "parameters_abcdef": [str(value) for value in parameters],
                    "lower_term": lower.to_json(),
                    "commutator_zero": not hamiltonian.commutator(operator).terms,
                }
            )
        hamiltonian_matches_metric_lift = operators[0] == hamiltonian
        all_integrals_commute = all(
            not hamiltonian.commutator(operator).terms for operator in operators
        )
        hidden_dimension = len(kernel) - 1
        base = {
            "input": {
                key: str(value) if isinstance(value, Fraction) else value
                for key, value in model.items()
            },
            "coefficient_domain": "Q[x^+/-1,y^+/-1] with finite support",
            "potential": potential.to_json(),
            "centralizer": {
                "quadratic_module_dimension": 6,
                "compatibility_rank": _rank(matrix),
                "quadratic_kernel_dimension": len(kernel),
                "hidden_quotient_dimension": hidden_dimension,
                "generators": generators,
            },
        }
        if hidden_dimension < 2:
            return {
                "status": "CommutingQuadraticFamily",
                **base,
                "closure": {
                    "classification": "AbelianCentralizer",
                    "reason": "fewer than two nontrivial quadratic integrals survive",
                },
                "certificates": {
                    "metric_lift_is_hamiltonian": hamiltonian_matches_metric_lift,
                    "all_generated_integrals_commute_with_hamiltonian": all_integrals_commute,
                },
            }
        closure = _closure(hamiltonian, operators[1], operators[2])
        status = (
            "ExactPolynomialClosure"
            if closure["classification"] == "PolynomialAlgebra"
            else "UnresolvedClosure"
        )
        spectrum = _spectrum(model)
        representation = _representation_adapter(closure, model) if spectrum is not None else None
        return {
            "status": status,
            **base,
            "closure": closure,
            "group_integration": {
                "status": "NotApplicable"
                if closure["classification"] == "PolynomialAlgebra"
                else "Pending",
                "reason": "the off-shell commutators require quadratic words, not constant structure coefficients",
                "possible_parent": "an enveloping-algebra realization may exist but is not inferred uniquely from closure",
            },
            "representation": representation,
            "spectrum_baseline": spectrum,
            "route_evaluation": {
                "same_observable": "bound-state energy family and multiplicity",
                "selected_for_energy": "separated_factorization",
                "same_spectrum_recovered": representation is not None,
                "reason": "both routes recover the spectrum, but factorization avoids the six-column centralizer and closure construction",
                "polynomial_route_gain": "the generated positive Jacobi recurrence acts between Cartesian and angular integral bases without special-function lookup",
                "interbasis_companion": "singular_interbasis_probe.py proves phase-insensitive probability equality by independent operator identification",
            },
            "certificates": {
                "complete_rank_two_module_relative_to_E2": True,
                "metric_lift_is_hamiltonian": hamiltonian_matches_metric_lift,
                "all_generated_integrals_commute_with_hamiltonian": all_integrals_commute,
                "linear_closure_fails": not closure["linear_closure"],
                "quadratic_relations_reconstruct_commutators": closure["quadratic_closure"],
                "nonlinear_words_are_used": bool(closure["nonlinear_coefficients"]),
                "positive_representation_constructed": representation is not None
                and all(representation["certificates"].values()),
            },
            "not_certified": [
                "strong commutation of the hidden integrals on the Hilbert-space domain",
                "derivation of the one-dimensional lowest weights without the singular-oscillator analytic contract",
                "coordinate-dependent phases and spatial overlap kernels",
                "computational advantage of polynomial closure for energy alone",
            ],
        }
    except (AssertionError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        return {"status": "Refused", "reason": str(error)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--summary", action="store_true")
    arguments = parser.parse_args()
    result = build_polynomial_closure(arguments.input)
    if arguments.summary and result["status"] == "ExactPolynomialClosure":
        centralizer = result["centralizer"]
        print(
            f"{result['status']}: kernel {centralizer['quadratic_module_dimension']} -> "
            f"{centralizer['quadratic_kernel_dimension']}; {result['closure']['classification']}; "
            f"selected {result['route_evaluation']['selected_for_energy']} for energy"
        )
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] in {"ExactPolynomialClosure", "CommutingQuadraticFamily"} else 2


if __name__ == "__main__":
    raise SystemExit(main())

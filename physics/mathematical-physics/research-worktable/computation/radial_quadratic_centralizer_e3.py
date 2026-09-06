"""Complete first-/second-order radial centralizer generator on punctured E^3.

The candidate modules come from the six Euclidean Killing vectors.  Their 21
symmetric products are reduced to the 20-dimensional rank-two Killing-tensor
module before the supplied potential is used.  Coefficients lie in the finite
half-Laurent radial algebra with s=x^2+y^2+z^2.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from quadratic_centralizer import nullspace, parse_fraction, rank

Exponents = tuple[int, ...]
Key = tuple[Exponents, Fraction]
Tensor = tuple[tuple["NDExpr", ...], ...]
Vector = tuple["NDExpr", ...]


@dataclass(frozen=True)
class NDExpr:
    dimension: int
    terms: dict[Key, Fraction]

    def __post_init__(self) -> None:
        if self.dimension < 2:
            raise ValueError("dimension must be at least two")
        pending = [(key, Fraction(value)) for key, value in self.terms.items() if value]
        reduced: dict[Key, Fraction] = {}
        while pending:
            (powers, s_power), coefficient = pending.pop()
            if len(powers) != self.dimension or any(power < 0 for power in powers):
                raise ValueError("coordinate powers do not match the dimension")
            if s_power.denominator not in (1, 2):
                raise ValueError("radius-squared powers must be half-integers")
            if powers[0] >= 2:
                lowered = list(powers)
                lowered[0] -= 2
                pending.append(((tuple(lowered), s_power + 1), coefficient))
                for index in range(1, self.dimension):
                    shifted = list(lowered)
                    shifted[index] += 2
                    pending.append(((tuple(shifted), s_power), -coefficient))
                continue
            key = (powers, s_power)
            reduced[key] = reduced.get(key, Fraction(0)) + coefficient
        object.__setattr__(self, "terms", {key: value for key, value in reduced.items() if value})

    @staticmethod
    def zero(dimension: int) -> NDExpr:
        return NDExpr(dimension, {})

    @staticmethod
    def constant(dimension: int, value: int | Fraction) -> NDExpr:
        coefficient = Fraction(value)
        if not coefficient:
            return NDExpr.zero(dimension)
        return NDExpr(dimension, {((0,) * dimension, Fraction(0)): coefficient})

    @staticmethod
    def monomial(
        dimension: int,
        powers: Exponents | None = None,
        s_power: int | Fraction = 0,
        coefficient: int | Fraction = 1,
    ) -> NDExpr:
        return NDExpr(
            dimension,
            {
                ((0,) * dimension if powers is None else powers, Fraction(s_power)): Fraction(
                    coefficient
                )
            },
        )

    def _same_dimension(self, other: NDExpr) -> None:
        if self.dimension != other.dimension:
            raise ValueError("coefficient dimensions differ")

    def __add__(self, other: NDExpr) -> NDExpr:
        self._same_dimension(other)
        terms = dict(self.terms)
        for key, coefficient in other.terms.items():
            terms[key] = terms.get(key, Fraction(0)) + coefficient
        return NDExpr(self.dimension, terms)

    def __neg__(self) -> NDExpr:
        return NDExpr(self.dimension, {key: -value for key, value in self.terms.items()})

    def __sub__(self, other: NDExpr) -> NDExpr:
        return self + (-other)

    def __mul__(self, other: NDExpr) -> NDExpr:
        self._same_dimension(other)
        terms: dict[Key, Fraction] = {}
        for (left_powers, left_s), left in self.terms.items():
            for (right_powers, right_s), right in other.terms.items():
                powers = tuple(
                    left_powers[index] + right_powers[index] for index in range(self.dimension)
                )
                key = (powers, left_s + right_s)
                terms[key] = terms.get(key, Fraction(0)) + left * right
        return NDExpr(self.dimension, terms)

    def scale(self, value: int | Fraction) -> NDExpr:
        coefficient = Fraction(value)
        return NDExpr(
            self.dimension,
            {key: coefficient * item for key, item in self.terms.items()},
        )

    def derivative(self, index: int) -> NDExpr:
        if not 0 <= index < self.dimension:
            raise ValueError("derivative index out of range")
        result = NDExpr.zero(self.dimension)
        for (powers, s_power), coefficient in self.terms.items():
            if powers[index]:
                lowered = list(powers)
                lowered[index] -= 1
                result += NDExpr.monomial(
                    self.dimension,
                    tuple(lowered),
                    s_power,
                    coefficient * powers[index],
                )
            if s_power:
                raised = list(powers)
                raised[index] += 1
                result += NDExpr.monomial(
                    self.dimension,
                    tuple(raised),
                    s_power - 1,
                    2 * coefficient * s_power,
                )
        return result

    def derivative_multi(self, orders: Exponents) -> NDExpr:
        result = self
        for index, order in enumerate(orders):
            for _ in range(order):
                result = result.derivative(index)
        return result

    def to_json(self) -> list[dict[str, object]]:
        return [
            {
                "powers": list(powers),
                "radius_squared_power": str(s_power),
                "coefficient": str(coefficient),
            }
            for (powers, s_power), coefficient in sorted(self.terms.items(), reverse=True)
        ]


@dataclass(frozen=True)
class NDDiffOp:
    dimension: int
    terms: dict[Exponents, NDExpr]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "terms",
            {
                derivative: coefficient
                for derivative, coefficient in self.terms.items()
                if coefficient.terms
            },
        )

    @staticmethod
    def multiplication(coefficient: NDExpr) -> NDDiffOp:
        return NDDiffOp(coefficient.dimension, {(0,) * coefficient.dimension: coefficient})

    @staticmethod
    def derivative(dimension: int, index: int) -> NDDiffOp:
        orders = [0] * dimension
        orders[index] = 1
        return NDDiffOp(dimension, {tuple(orders): NDExpr.constant(dimension, 1)})

    def __add__(self, other: NDDiffOp) -> NDDiffOp:
        if self.dimension != other.dimension:
            raise ValueError("operator dimensions differ")
        terms = dict(self.terms)
        zero = NDExpr.zero(self.dimension)
        for derivative, coefficient in other.terms.items():
            terms[derivative] = terms.get(derivative, zero) + coefficient
        return NDDiffOp(self.dimension, terms)

    def __neg__(self) -> NDDiffOp:
        return NDDiffOp(
            self.dimension,
            {derivative: coefficient.scale(-1) for derivative, coefficient in self.terms.items()},
        )

    def __sub__(self, other: NDDiffOp) -> NDDiffOp:
        return self + (-other)

    def scale(self, value: int | Fraction) -> NDDiffOp:
        return NDDiffOp(
            self.dimension,
            {
                derivative: coefficient.scale(value)
                for derivative, coefficient in self.terms.items()
            },
        )

    def compose(self, other: NDDiffOp) -> NDDiffOp:
        if self.dimension != other.dimension:
            raise ValueError("operator dimensions differ")
        zero = NDExpr.zero(self.dimension)
        terms: dict[Exponents, NDExpr] = {}
        for left_order, left in self.terms.items():
            gamma_ranges = [range(order + 1) for order in left_order]
            gammas: list[Exponents] = [()]
            for values in gamma_ranges:
                gammas = [prefix + (value,) for prefix in gammas for value in values]
            for right_order, right in other.terms.items():
                for gamma in gammas:
                    factor = math.prod(
                        math.comb(left_order[index], gamma[index])
                        for index in range(self.dimension)
                    )
                    derivative = tuple(
                        left_order[index] - gamma[index] + right_order[index]
                        for index in range(self.dimension)
                    )
                    coefficient = (left * right.derivative_multi(gamma)).scale(factor)
                    terms[derivative] = terms.get(derivative, zero) + coefficient
        return NDDiffOp(self.dimension, terms)

    def to_json(self) -> list[dict[str, object]]:
        return [
            {"derivative": list(derivative), "coefficient": coefficient.to_json()}
            for derivative, coefficient in sorted(self.terms.items(), reverse=True)
        ]


def zero_vector(dimension: int) -> Vector:
    return tuple(NDExpr.zero(dimension) for _ in range(dimension))


def coordinate(dimension: int, index: int) -> NDExpr:
    powers = [0] * dimension
    powers[index] = 1
    return NDExpr.monomial(dimension, tuple(powers))


def euclidean_killing_vectors() -> tuple[tuple[str, Vector], ...]:
    dimension = 3
    zero = NDExpr.zero(dimension)
    one = NDExpr.constant(dimension, 1)
    x, y, z = (coordinate(dimension, index) for index in range(dimension))
    return (
        ("P_x", (one, zero, zero)),
        ("P_y", (zero, one, zero)),
        ("P_z", (zero, zero, one)),
        ("R_x", (zero, -z, y)),
        ("R_y", (z, zero, -x)),
        ("R_z", (-y, x, zero)),
    )


def vector_linear_combination(coefficients: tuple[Fraction, ...], vectors: list[Vector]) -> Vector:
    dimension = len(vectors[0])
    return tuple(
        sum(
            (vectors[column][index].scale(coefficients[column]) for column in range(len(vectors))),
            NDExpr.zero(dimension),
        )
        for index in range(dimension)
    )


def symmetric_tensor(left: Vector, right: Vector) -> Tensor:
    dimension = len(left)
    return tuple(
        tuple(
            (left[i] * right[j] + right[i] * left[j]).scale(Fraction(1, 2))
            for j in range(dimension)
        )
        for i in range(dimension)
    )


def tensor_add(left: Tensor, right: Tensor) -> Tensor:
    return tuple(
        tuple(left[i][j] + right[i][j] for j in range(len(left))) for i in range(len(left))
    )


def tensor_scale(tensor: Tensor, value: int | Fraction) -> Tensor:
    return tuple(tuple(item.scale(value) for item in row) for row in tensor)


def tensor_linear_combination(coefficients: tuple[Fraction, ...], tensors: list[Tensor]) -> Tensor:
    dimension = len(tensors[0])
    zero = NDExpr.zero(dimension)
    return tuple(
        tuple(
            sum(
                (
                    tensors[column][i][j].scale(coefficients[column])
                    for column in range(len(tensors))
                ),
                zero,
            )
            for j in range(dimension)
        )
        for i in range(dimension)
    )


def tensor_representation_matrix(
    tensors: list[Tensor],
) -> tuple[list[tuple[int, int, Key]], list[list[Fraction]]]:
    row_keys = sorted(
        {
            (i, j, key)
            for tensor in tensors
            for i in range(len(tensor))
            for j in range(i, len(tensor))
            for key in tensor[i][j].terms
        }
    )
    matrix = [
        [tensor[i][j].terms.get(key, Fraction(0)) for tensor in tensors] for i, j, key in row_keys
    ]
    return row_keys, matrix


def pivot_columns(matrix: list[list[Fraction]], columns: int) -> list[int]:
    rows = [list(row) for row in matrix]
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
    return pivots


def compatibility_one_form(potential: NDExpr, tensor: Tensor) -> Vector:
    gradient = tuple(potential.derivative(index) for index in range(potential.dimension))
    return tuple(
        sum(
            (tensor[i][j] * gradient[j] for j in range(potential.dimension)),
            NDExpr.zero(potential.dimension),
        )
        for i in range(potential.dimension)
    )


def compatibility_obstruction(potential: NDExpr, tensor: Tensor) -> tuple[NDExpr, ...]:
    one_form = compatibility_one_form(potential, tensor)
    return tuple(
        one_form[j].derivative(i) - one_form[i].derivative(j)
        for i in range(potential.dimension)
        for j in range(i + 1, potential.dimension)
    )


def first_order_obstruction(potential: NDExpr, vector: Vector) -> NDExpr:
    return sum(
        (vector[index] * potential.derivative(index) for index in range(potential.dimension)),
        NDExpr.zero(potential.dimension),
    )


def solve_linear(matrix: list[list[Fraction]], target: list[Fraction]) -> list[Fraction] | None:
    if len(matrix) != len(target):
        raise ValueError("linear system shape mismatch")
    columns = len(matrix[0]) if matrix else 0
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
    if any(not any(row[:columns]) and row[-1] for row in rows):
        return None
    solution = [Fraction(0) for _ in range(columns)]
    for row, column in enumerate(pivots):
        solution[column] = rows[row][-1]
    return solution


def reconstruct_lower_term(potential: NDExpr, tensor: Tensor) -> NDExpr:
    one_form = compatibility_one_form(potential, tensor)
    dimension = potential.dimension
    if not any(component.terms for component in one_form):
        return NDExpr.zero(dimension)
    candidate_keys: set[Key] = set()
    for index, component in enumerate(one_form):
        for powers, s_power in component.terms:
            raised = list(powers)
            raised[index] += 1
            candidate_keys.update(NDExpr.monomial(dimension, tuple(raised), s_power).terms)
            if powers[index]:
                lowered = list(powers)
                lowered[index] -= 1
                candidate_keys.update(NDExpr.monomial(dimension, tuple(lowered), s_power + 1).terms)
    candidate_keys.discard(((0,) * dimension, Fraction(0)))
    candidates = [NDExpr(dimension, {key: Fraction(1)}) for key in sorted(candidate_keys)]
    derivatives = [
        tuple(candidate.derivative(index) for index in range(dimension)) for candidate in candidates
    ]
    row_keys = sorted(
        {(index, key) for index, component in enumerate(one_form) for key in component.terms}
        | {
            (index, key)
            for derivative_vector in derivatives
            for index, component in enumerate(derivative_vector)
            for key in component.terms
        }
    )
    matrix = [
        [
            derivatives[column][index].terms.get(key, Fraction(0))
            for column in range(len(candidates))
        ]
        for index, key in row_keys
    ]
    target = [one_form[index].terms.get(key, Fraction(0)) for index, key in row_keys]
    solution = solve_linear(matrix, target)
    if solution is None:
        raise AssertionError("closed one-form was not reconstructed in the admitted carrier")
    lower = sum(
        (candidate.scale(value) for candidate, value in zip(candidates, solution)),
        NDExpr.zero(dimension),
    )
    if any(lower.derivative(index) != one_form[index] for index in range(dimension)):
        raise AssertionError("lower term does not reconstruct K dV")
    return lower


def vector_operator(vector: Vector) -> NDDiffOp:
    dimension = len(vector)
    result = NDDiffOp(dimension, {})
    for index, coefficient in enumerate(vector):
        result += NDDiffOp.multiplication(coefficient).compose(
            NDDiffOp.derivative(dimension, index)
        )
    return result


def quantum_operator(tensor: Tensor, lower: NDExpr) -> NDDiffOp:
    dimension = len(tensor)
    result = NDDiffOp(dimension, {})
    for i in range(dimension):
        for j in range(dimension):
            result += (
                NDDiffOp.derivative(dimension, i)
                .compose(NDDiffOp.multiplication(tensor[i][j]))
                .compose(NDDiffOp.derivative(dimension, j))
            )
    return result.scale(Fraction(-1, 2)) + NDDiffOp.multiplication(lower)


def hamiltonian(potential: NDExpr) -> NDDiffOp:
    dimension = potential.dimension
    kinetic = NDDiffOp(dimension, {})
    for index in range(dimension):
        derivative = NDDiffOp.derivative(dimension, index)
        kinetic += derivative.compose(derivative)
    return kinetic.scale(Fraction(-1, 2)) + NDDiffOp.multiplication(potential)


def ordered_kernel(
    kernel: list[tuple[Fraction, ...]], seed: tuple[Fraction, ...]
) -> list[tuple[Fraction, ...]]:
    ordered = [seed]
    current_rank = 1
    for vector in kernel:
        candidate_rank = rank([*ordered, vector])
        if candidate_rank > current_rank:
            ordered.append(vector)
            current_rank = candidate_rank
    if len(ordered) != len(kernel):
        raise AssertionError("distinguished Hamiltonian was not in the kernel")
    return ordered


def generate(potential: NDExpr) -> dict[str, object]:
    if potential.dimension != 3:
        raise ValueError("this generator is specialized to dimension three")
    named_vectors = euclidean_killing_vectors()
    vector_names = [name for name, _ in named_vectors]
    vectors = [vector for _, vector in named_vectors]

    first_obstructions = [first_order_obstruction(potential, vector) for vector in vectors]
    first_keys = sorted({key for item in first_obstructions for key in item.terms})
    first_matrix = [
        [item.terms.get(key, Fraction(0)) for item in first_obstructions] for key in first_keys
    ]
    first_kernel = nullspace(first_matrix, len(vectors))

    pair_labels: list[str] = []
    presented_tensors: list[Tensor] = []
    pair_indices: list[tuple[int, int]] = []
    for left in range(len(vectors)):
        for right in range(left, len(vectors)):
            pair_labels.append(f"{vector_names[left]}*{vector_names[right]}")
            pair_indices.append((left, right))
            presented_tensors.append(symmetric_tensor(vectors[left], vectors[right]))
    _, representation_matrix = tensor_representation_matrix(presented_tensors)
    redundancies = nullspace(representation_matrix, len(presented_tensors))
    independent_indices = pivot_columns(representation_matrix, len(presented_tensors))
    module_tensors = [presented_tensors[index] for index in independent_indices]
    module_labels = [pair_labels[index] for index in independent_indices]

    obstructions = [compatibility_obstruction(potential, tensor) for tensor in module_tensors]
    obstruction_keys = sorted(
        {
            (component, key)
            for obstruction in obstructions
            for component, expression in enumerate(obstruction)
            for key in expression.terms
        }
    )
    compatibility_matrix = [
        [obstruction[component].terms.get(key, Fraction(0)) for obstruction in obstructions]
        for component, key in obstruction_keys
    ]
    kernel = nullspace(compatibility_matrix, len(module_tensors))
    metric = [Fraction(0) for _ in module_tensors]
    for translation_name in ("P_x*P_x", "P_y*P_y", "P_z*P_z"):
        metric[module_labels.index(translation_name)] = Fraction(1)
    kernel = ordered_kernel(kernel, tuple(metric))

    h_op = hamiltonian(potential)
    first_generators = []
    for coefficients in first_kernel:
        vector = vector_linear_combination(coefficients, vectors)
        operator = vector_operator(vector)
        first_generators.append(
            {
                "coefficients": [str(value) for value in coefficients],
                "basis": vector_names,
                "vector": [component.to_json() for component in vector],
                "commutator_zero": not (h_op.compose(operator) - operator.compose(h_op)).terms,
            }
        )

    generators = []
    all_commute = True
    for index, coefficients in enumerate(kernel):
        tensor = tensor_linear_combination(coefficients, module_tensors)
        lower = reconstruct_lower_term(potential, tensor)
        operator = quantum_operator(tensor, lower)
        commutes = not (h_op.compose(operator) - operator.compose(h_op)).terms
        all_commute = all_commute and commutes
        generators.append(
            {
                "role": "hamiltonian" if index == 0 else "hidden",
                "coefficients": [str(value) for value in coefficients],
                "basis": module_labels,
                "tensor": [[tensor[i][j].to_json() for j in range(3)] for i in range(3)],
                "W": lower.to_json(),
                "operator": operator.to_json(),
                "commutator_zero": commutes,
            }
        )

    return {
        "status": "NontrivialQuadraticCentralizer" if len(kernel) > 1 else "MetricOnly",
        "dimension": 3,
        "coefficient_domain": "finite Q[x,y,z,s^(1/2),s^(-1/2)]/(s-x^2-y^2-z^2)",
        "first_order_presented_dimension": 6,
        "first_order_kernel_dimension": len(first_kernel),
        "first_order_generators": first_generators,
        "quadratic_presented_dimension": len(presented_tensors),
        "quadratic_module_dimension": len(module_tensors),
        "presentation_redundancy_dimension": len(redundancies),
        "presentation_redundancies": [
            {"basis": pair_labels, "coefficients": [str(value) for value in vector]}
            for vector in redundancies
        ],
        "quadratic_basis": module_labels,
        "quadratic_kernel_dimension": len(kernel),
        "hidden_quotient_dimension": len(kernel) - 1,
        "generators": generators,
        "certificates": {
            "presentation_rank": len(module_tensors),
            "all_first_order_commutators_zero": all(
                generator["commutator_zero"] for generator in first_generators
            ),
            "all_quadratic_commutators_with_H_zero": all_commute,
        },
        "not_certified": [
            "self-adjoint domains at the puncture and infinity",
            "strong commutation and bound-state completeness",
            "higher-order or spinorial centralizers",
        ],
    }


def load_potential(path: Path) -> NDExpr:
    payload = json.loads(path.read_text(encoding="utf-8"))
    dimension = 3
    terms: dict[Key, Fraction] = {}
    for item in payload["potential"]:
        powers = item["powers"]
        if (
            not isinstance(powers, list)
            or len(powers) != dimension
            or not all(isinstance(value, int) and value >= 0 for value in powers)
        ):
            raise ValueError("powers must be three nonnegative integers")
        s_power = Fraction(item.get("radius_squared_power", "0"))
        if s_power.denominator not in (1, 2):
            raise ValueError("radius-squared powers must be half-integers")
        key = (tuple(powers), s_power)
        terms[key] = terms.get(key, Fraction(0)) + parse_fraction(item["coefficient"])
    return NDExpr(dimension, terms)


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
            f"{result['status']}: Sym^2(e3) {result['quadratic_presented_dimension']} "
            f"-> module {result['quadratic_module_dimension']} -> kernel "
            f"{result['quadratic_kernel_dimension']}; first-order kernel "
            f"{result['first_order_kernel_dimension']}"
        )
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

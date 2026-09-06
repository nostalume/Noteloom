"""Parse the admitted natural-tensor problem grammar into certified relations."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction
from itertools import product

from natural_relation_planner import METRIC_SEED_CAPABILITY
from tensor_seed_compression import (
    CovariantTensor,
    Index,
    Matrix,
    Permutation,
    SlotQuotient,
    SymmetricPowerQuotient,
    TensorQuotient,
)

SYMMETRIC_TWO = SymmetricPowerQuotient(SlotQuotient(), 2)
ELASTICITY_QUOTIENT = SymmetricPowerQuotient(SYMMETRIC_TWO, 2)


@dataclass(frozen=True)
class NaturalTensorInput:
    dimension: int
    metric: Matrix
    tensors: tuple[CovariantTensor, ...]
    elasticity_parameters: tuple[Fraction, Fraction] | None


def exact_fraction(value: object, name: str) -> Fraction:
    if isinstance(value, (bool, float)) or not isinstance(value, (int, str)):
        raise ValueError(f"{name} must be an exact integer or rational string")
    return Fraction(value)


def exact_vector(value: object, dimension: int, name: str) -> tuple[Fraction, ...]:
    if not isinstance(value, list) or len(value) != dimension:
        raise ValueError(f"{name} must have dimension {dimension}")
    return tuple(exact_fraction(item, f"{name}[{index}]") for index, item in enumerate(value))


def _matrix(value: object, dimension: int, name: str) -> Matrix:
    if not isinstance(value, list) or len(value) != dimension:
        raise ValueError(f"{name} must be a {dimension} by {dimension} exact matrix")
    rows: list[tuple[Fraction, ...]] = []
    for row_index, row in enumerate(value):
        if not isinstance(row, list) or len(row) != dimension:
            raise ValueError(f"{name} must be a {dimension} by {dimension} exact matrix")
        rows.append(
            tuple(
                exact_fraction(item, f"{name}[{row_index}][{column}]")
                for column, item in enumerate(row)
            )
        )
    return tuple(rows)


def _positive_definite(metric: Matrix) -> bool:
    work = [list(row) for row in metric]
    for pivot in range(len(work)):
        if work[pivot][pivot] <= 0:
            return False
        value = work[pivot][pivot]
        for row in range(pivot + 1, len(work)):
            factor = work[row][pivot] / value
            for column in range(pivot + 1, len(work)):
                work[row][column] -= factor * work[pivot][column]
    return True


def _tensor(
    name: str,
    dimension: int,
    rank: int,
    function: Callable[[Index], Fraction],
    *,
    permutation_generators: tuple[Permutation, ...],
    capabilities: frozenset[str] = frozenset(),
    relation_certificate: str,
    quotient: TensorQuotient,
) -> CovariantTensor:
    indices = tuple(product(range(dimension), repeat=rank))
    return CovariantTensor(
        name=name,
        dimension=dimension,
        rank=rank,
        components=tuple(function(index) for index in indices),
        permutation_generators=permutation_generators,
        capabilities=capabilities,
        relation_certificate=relation_certificate,
        quotient=quotient,
    )


def _metric_tensor(metric: Matrix) -> CovariantTensor:
    dimension = len(metric)
    return _tensor(
        "metric",
        dimension,
        2,
        lambda index: metric[index[0]][index[1]],
        permutation_generators=((1, 0),),
        capabilities=frozenset({METRIC_SEED_CAPABILITY}),
        relation_certificate="checked symmetric positive-definite input",
        quotient=SYMMETRIC_TWO,
    )


def _elasticity_tensor(metric: Matrix, lam: Fraction, mu: Fraction) -> CovariantTensor:
    dimension = len(metric)

    def component(index: Index) -> Fraction:
        i, j, k, ell = index
        return (
            lam * metric[i][j] * metric[k][ell]
            + mu * metric[i][k] * metric[j][ell]
            + mu * metric[i][ell] * metric[j][k]
        )

    return _tensor(
        "isotropic-elasticity",
        dimension,
        4,
        component,
        permutation_generators=((1, 0, 2, 3), (0, 1, 3, 2), (2, 3, 0, 1)),
        relation_certificate="constructed from a symmetric bilinear form",
        quotient=ELASTICITY_QUOTIENT,
    )


def _axis_tensor(axis: tuple[Fraction, ...]) -> CovariantTensor:
    return _tensor(
        "axis-dyad",
        len(axis),
        2,
        lambda index: axis[index[0]] * axis[index[1]],
        permutation_generators=((1, 0),),
        relation_certificate="constructed as a covector dyad",
        quotient=SYMMETRIC_TWO,
    )


def parse_natural_tensor_input(payload: dict[str, object]) -> NaturalTensorInput:
    if payload.get("schema") != "natural-tensor-stabilizer/v1":
        raise ValueError("schema must be natural-tensor-stabilizer/v1")
    dimension = payload.get("dimension")
    if isinstance(dimension, bool) or not isinstance(dimension, int) or dimension <= 0:
        raise ValueError("dimension must be a positive integer")
    raw_tensors = payload.get("tensors")
    if not isinstance(raw_tensors, list) or not raw_tensors:
        raise ValueError("tensors must be a nonempty list")
    raw_metric = next(
        (item for item in raw_tensors if isinstance(item, dict) and item.get("kind") == "metric"),
        None,
    )
    if not isinstance(raw_metric, dict):
        raise ValueError("one metric tensor is required")
    metric = _matrix(raw_metric.get("matrix"), dimension, "metric.matrix")
    if metric != tuple(
        tuple(metric[column][row] for column in range(dimension)) for row in range(dimension)
    ):
        raise ValueError("metric must be symmetric")
    if not _positive_definite(metric):
        raise ValueError("metric must be positive definite")

    tensors: list[CovariantTensor] = []
    elasticity_parameters: tuple[Fraction, Fraction] | None = None
    for index, item in enumerate(raw_tensors):
        if not isinstance(item, dict):
            raise ValueError(f"tensors[{index}] must be an object")
        kind = item.get("kind")
        if kind == "metric":
            tensors.append(_metric_tensor(metric))
        elif kind == "isotropic_elasticity":
            lam = exact_fraction(item.get("lambda"), f"tensors[{index}].lambda")
            mu = exact_fraction(item.get("mu"), f"tensors[{index}].mu")
            if mu <= 0 or lam + 2 * mu <= 0:
                raise ValueError("elasticity parameters must give positive wave channels")
            elasticity_parameters = (lam, mu)
            tensors.append(_elasticity_tensor(metric, lam, mu))
        elif kind == "axis_dyad":
            axis = exact_vector(item.get("axis"), dimension, f"tensors[{index}].axis")
            if not any(axis):
                raise ValueError("axis_dyad requires a nonzero axis")
            tensors.append(_axis_tensor(axis))
        else:
            raise ValueError(f"unsupported natural tensor kind {kind!r}")
    return NaturalTensorInput(
        dimension=dimension,
        metric=metric,
        tensors=tuple(tensors),
        elasticity_parameters=elasticity_parameters,
    )

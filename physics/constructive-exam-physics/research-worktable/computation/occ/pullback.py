from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction

from .records import Certificate, Matrix, Vector


def _fraction(value: object) -> Fraction:
    if isinstance(value, bool):
        raise TypeError("Boolean values are not rational coefficients.")
    if isinstance(value, (int, Fraction)):
        return Fraction(value)
    raise TypeError("Pullback coefficients must be integers or Fractions.")


def _matrix(value: Sequence[Sequence[object]]) -> Matrix:
    if isinstance(value, (str, bytes)) or not value:
        raise ValueError("A physical map must be a nonempty matrix.")
    matrix = tuple(tuple(_fraction(entry) for entry in row) for row in value)
    if not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("A physical map must be rectangular.")
    return matrix


def _transpose(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[row][column] for row in range(len(matrix)))
        for column in range(len(matrix[0]))
    )


def _matmul(left: Matrix, right: Matrix) -> Matrix:
    if len(left[0]) != len(right):
        raise ValueError("Matrix dimensions do not compose.")
    return tuple(
        tuple(
            sum(
                (
                    left[row][inner] * right[inner][column]
                    for inner in range(len(right))
                ),
                Fraction(0),
            )
            for column in range(len(right[0]))
        )
        for row in range(len(left))
    )


def _matvec(matrix: Matrix, vector: Vector) -> Vector:
    if len(matrix[0]) != len(vector):
        raise ValueError("Matrix and vector dimensions do not match.")
    return tuple(
        sum((entry * value for entry, value in zip(row, vector)), Fraction(0))
        for row in matrix
    )


def _dot(left: Vector, right: Vector) -> Fraction:
    if len(left) != len(right):
        raise ValueError("Vector dimensions do not match.")
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def _normalize_chain(
    maps: Sequence[Sequence[Sequence[object]]],
) -> tuple[tuple[Matrix, ...], tuple[int, ...]]:
    if not maps:
        raise ValueError("At least one physical map is required.")
    chain = tuple(_matrix(item) for item in maps)
    for previous, following in zip(chain, chain[1:]):
        if len(following[0]) != len(previous):
            raise ValueError("Physical-map chain dimensions do not compose.")
    dimensions = (len(chain[0][0]),) + tuple(len(item) for item in chain)
    return chain, dimensions


def _compose(chain: tuple[Matrix, ...]) -> Matrix:
    composite = chain[0]
    for item in chain[1:]:
        composite = _matmul(item, composite)
    return composite


@dataclass(frozen=True)
class LinearPullbackResult:
    source_covector: Vector
    dimensions: tuple[int, ...]
    certificates: tuple[Certificate, ...]

    def evaluate_source(self, source: Vector) -> Fraction:
        return _dot(self.source_covector, source)


@dataclass(frozen=True)
class QuadraticPullbackResult:
    source_form: Matrix
    dimensions: tuple[int, ...]
    certificates: tuple[Certificate, ...]

    def evaluate_source(self, source: Vector) -> Fraction:
        return _dot(source, _matvec(self.source_form, source))


def pullback_linear(
    maps: Sequence[Sequence[Sequence[object]]],
    target_covector: Sequence[object],
) -> LinearPullbackResult:
    """Pull a final linear observable back through a composable map chain."""
    chain, dimensions = _normalize_chain(maps)
    target = tuple(_fraction(entry) for entry in target_covector)
    if len(target) != dimensions[-1]:
        raise ValueError("The target observable does not match the final space.")

    pulled = target
    for item in reversed(chain):
        pulled = _matvec(_transpose(item), pulled)
    direct = _matvec(_transpose(_compose(chain)), target)
    certificates = (
        Certificate(
            name="contravariant_linear_composition",
            passed=pulled == direct,
            witness="Sequential reverse pullback equals pullback through the composed map.",
        ),
    )
    return LinearPullbackResult(pulled, dimensions, certificates)


def pullback_quadratic(
    maps: Sequence[Sequence[Sequence[object]]],
    target_form: Sequence[Sequence[object]],
) -> QuadraticPullbackResult:
    """Pull a final quadratic observable y^T Q y back to the source space."""
    chain, dimensions = _normalize_chain(maps)
    target = _matrix(target_form)
    if len(target) != dimensions[-1] or len(target[0]) != dimensions[-1]:
        raise ValueError("The target quadratic form does not match the final space.")
    if target != _transpose(target):
        raise ValueError("The target quadratic form must be symmetric.")

    pulled = target
    for item in reversed(chain):
        pulled = _matmul(_transpose(item), _matmul(pulled, item))
    composite = _compose(chain)
    direct = _matmul(_transpose(composite), _matmul(target, composite))
    certificates = (
        Certificate(
            name="contravariant_quadratic_composition",
            passed=pulled == direct,
            witness="Sequential reverse pullback equals C^T Q C for the composed map C.",
        ),
    )
    return QuadraticPullbackResult(pulled, dimensions, certificates)

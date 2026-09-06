"""Exact Gaussian-rational matrices for finite Hermitian carrier relations."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


def rational(value: object) -> Fraction:
    if isinstance(value, (bool, float)):
        raise ValueError("use integers or rational strings, not booleans or floats")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, (int, str)):
        return Fraction(value)
    raise ValueError(f"invalid rational value {value!r}")


def rational_text(value: Fraction) -> str:
    return (
        str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    )


@dataclass(frozen=True)
class Gaussian:
    real: Fraction = Fraction(0)
    imaginary: Fraction = Fraction(0)

    def __add__(self, other: Gaussian) -> Gaussian:
        return Gaussian(self.real + other.real, self.imaginary + other.imaginary)

    def __neg__(self) -> Gaussian:
        return Gaussian(-self.real, -self.imaginary)

    def __sub__(self, other: Gaussian) -> Gaussian:
        return self + (-other)

    def __mul__(self, other: Gaussian) -> Gaussian:
        return Gaussian(
            self.real * other.real - self.imaginary * other.imaginary,
            self.real * other.imaginary + self.imaginary * other.real,
        )

    def conjugate(self) -> Gaussian:
        return Gaussian(self.real, -self.imaginary)


ZERO = Gaussian()
ONE = Gaussian(Fraction(1))
IMAGINARY_UNIT = Gaussian(Fraction(0), Fraction(1))
ComplexMatrix = tuple[tuple[Gaussian, ...], ...]


def scalar(value: object) -> Gaussian:
    if isinstance(value, Gaussian):
        return value
    if isinstance(value, list) and len(value) == 2:
        return Gaussian(rational(value[0]), rational(value[1]))
    return Gaussian(rational(value))


def matrix(value: object, name: str) -> ComplexMatrix:
    if not isinstance(value, list) or not value or any(not isinstance(row, list) for row in value):
        raise ValueError(f"{name} must be a nonempty square exact matrix")
    dimension = len(value)
    if any(len(row) != dimension for row in value):
        raise ValueError(f"{name} must be a nonempty square exact matrix")
    return tuple(tuple(scalar(entry) for entry in row) for row in value)


def zero(dimension: int) -> ComplexMatrix:
    return tuple(tuple(ZERO for _ in range(dimension)) for _ in range(dimension))


def identity(dimension: int) -> ComplexMatrix:
    return tuple(
        tuple(ONE if row == column else ZERO for column in range(dimension))
        for row in range(dimension)
    )


def add(left: ComplexMatrix, right: ComplexMatrix) -> ComplexMatrix:
    return tuple(
        tuple(left[row][column] + right[row][column] for column in range(len(left)))
        for row in range(len(left))
    )


def scale(value: ComplexMatrix, coefficient: Fraction | Gaussian) -> ComplexMatrix:
    factor = coefficient if isinstance(coefficient, Gaussian) else Gaussian(coefficient)
    return tuple(tuple(factor * entry for entry in row) for row in value)


def multiply(left: ComplexMatrix, right: ComplexMatrix) -> ComplexMatrix:
    dimension = len(left)
    return tuple(
        tuple(
            sum(
                (left[row][inner] * right[inner][column] for inner in range(dimension)),
                ZERO,
            )
            for column in range(dimension)
        )
        for row in range(dimension)
    )


def bracket(left: ComplexMatrix, right: ComplexMatrix) -> ComplexMatrix:
    return add(multiply(left, right), scale(multiply(right, left), Fraction(-1)))


def dagger(value: ComplexMatrix) -> ComplexMatrix:
    return tuple(
        tuple(value[column][row].conjugate() for column in range(len(value)))
        for row in range(len(value))
    )


def is_hermitian(value: ComplexMatrix) -> bool:
    return dagger(value) == value


def hermitian_coordinates(value: ComplexMatrix) -> tuple[Fraction, ...]:
    if not is_hermitian(value):
        raise ValueError("matrix is not Hermitian")
    dimension = len(value)
    coordinates = [value[index][index].real for index in range(dimension)]
    for row in range(dimension):
        for column in range(row + 1, dimension):
            coordinates.extend((value[row][column].real, value[row][column].imaginary))
    return tuple(coordinates)


def skew_hermitian_basis(dimension: int) -> tuple[tuple[str, ComplexMatrix], ...]:
    basis: list[tuple[str, ComplexMatrix]] = []
    for index in range(dimension):
        entries = [[ZERO for _ in range(dimension)] for _ in range(dimension)]
        entries[index][index] = IMAGINARY_UNIT
        basis.append((f"fiber:iE{index}{index}", tuple(tuple(row) for row in entries)))
    for row in range(dimension):
        for column in range(row + 1, dimension):
            real_entries = [[ZERO for _ in range(dimension)] for _ in range(dimension)]
            real_entries[row][column] = ONE
            real_entries[column][row] = -ONE
            basis.append((f"fiber:R{row}{column}", tuple(tuple(item) for item in real_entries)))
            imaginary_entries = [[ZERO for _ in range(dimension)] for _ in range(dimension)]
            imaginary_entries[row][column] = IMAGINARY_UNIT
            imaginary_entries[column][row] = IMAGINARY_UNIT
            basis.append(
                (f"fiber:I{row}{column}", tuple(tuple(item) for item in imaginary_entries))
            )
    return tuple(basis)


def skew_hermitian_coordinates(value: ComplexMatrix) -> tuple[Fraction, ...]:
    if dagger(value) != scale(value, Fraction(-1)):
        raise ValueError("matrix is not skew-Hermitian")
    dimension = len(value)
    coordinates = [value[index][index].imaginary for index in range(dimension)]
    for row in range(dimension):
        for column in range(row + 1, dimension):
            coordinates.extend((value[row][column].real, value[row][column].imaginary))
    return tuple(coordinates)


def linear_combination(
    coefficients: tuple[Fraction, ...], basis: tuple[ComplexMatrix, ...]
) -> ComplexMatrix:
    if not basis:
        raise ValueError("a matrix basis must be nonempty")
    result = zero(len(basis[0]))
    for coefficient, value in zip(coefficients, basis, strict=True):
        result = add(result, scale(value, coefficient))
    return result


def serialize(value: ComplexMatrix) -> list[list[str | dict[str, str]]]:
    return [
        [
            rational_text(entry.real)
            if entry.imaginary == 0
            else {
                "real": rational_text(entry.real),
                "imaginary": rational_text(entry.imaginary),
            }
            for entry in row
        ]
        for row in value
    ]

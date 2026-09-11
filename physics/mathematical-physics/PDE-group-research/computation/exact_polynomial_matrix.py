"""Canonical exact Gaussian-rational polynomial matrices and wire values."""

from __future__ import annotations

from fractions import Fraction

import sympy as sp
from sympy.polys.domains import QQ_I

import exact_gaussian_matrix as gaussian


class ExactPolynomialError(ValueError):
    pass


def fraction(value: object, name: str) -> Fraction:
    try:
        return gaussian.rational(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ExactPolynomialError(f"{name}: {error}") from error


def scalar(value: object, name: str) -> sp.Expr:
    if isinstance(value, dict) and set(value) == {"real", "imaginary"}:
        real = fraction(value["real"], f"{name}.real")
        imaginary = fraction(value["imaginary"], f"{name}.imaginary")
    elif not isinstance(value, dict):
        real, imaginary = fraction(value, name), Fraction(0)
    else:
        raise ExactPolynomialError(f"{name} must be a rational or Gaussian-rational object")
    return sp.Rational(real.numerator, real.denominator) + sp.I * sp.Rational(
        imaginary.numerator, imaginary.denominator
    )


def polynomial_array(value, coordinates, *, vector: bool, name: str) -> sp.ImmutableMatrix:
    if (
        not isinstance(value, dict)
        or not isinstance(value.get("terms"), list)
        or not value["terms"]
    ):
        raise ExactPolynomialError(f"{name}.terms must be a nonempty list")
    result, shape = None, None
    key = "vector" if vector else "matrix"
    for term_index, term in enumerate(value["terms"]):
        if not isinstance(term, dict):
            raise ExactPolynomialError(f"{name}.terms[{term_index}] must be an object")
        powers = term.get("powers")
        if (
            not isinstance(powers, list)
            or len(powers) != len(coordinates)
            or any(
                isinstance(item, bool) or not isinstance(item, int) or item < 0 for item in powers
            )
        ):
            raise ExactPolynomialError(f"{name}.terms[{term_index}].powers must match coordinates")
        raw = term.get(key)
        if vector:
            if not isinstance(raw, list) or not raw:
                raise ExactPolynomialError(f"{name} term must be a nonempty vector")
            rows = [[entry] for entry in raw]
        else:
            if (
                not isinstance(raw, list)
                or not raw
                or any(not isinstance(row, list) or not row for row in raw)
                or any(len(row) != len(raw[0]) for row in raw)
            ):
                raise ExactPolynomialError(f"{name} term must be a rectangular matrix")
            rows = raw
        current_shape = (len(rows), len(rows[0]))
        if shape is None:
            shape, result = current_shape, sp.zeros(*current_shape)
        elif current_shape != shape:
            raise ExactPolynomialError(f"{name} term shapes differ")
        monomial = sp.prod(symbol**power for symbol, power in zip(coordinates, powers, strict=True))
        entries = [
            scalar(entry, f"{name}.terms[{term_index}].{key}[{row}][{column}]")
            for row, values in enumerate(rows)
            for column, entry in enumerate(values)
        ]
        assert result is not None and shape is not None
        result += sp.Matrix(*shape, entries) * monomial
    return sp.ImmutableMatrix(result.applyfunc(sp.expand))


def term_count(matrix: sp.MatrixBase, coordinates: tuple[sp.Symbol, ...]) -> int:
    return sum(
        len(sp.Poly(sp.expand(entry), *coordinates, domain=QQ_I).terms()) for entry in matrix
    )


def rational_fraction(value: sp.Expr) -> Fraction:
    value = sp.cancel(value)
    if not value.is_Rational:
        raise ExactPolynomialError("value is not rational-real")
    return Fraction(int(value.p), int(value.q))


def _interval_multiply(left, right):
    products = tuple(a * b for a in left for b in right)
    return min(products), max(products)


def horner_interval(expression, coordinates, box):
    if not coordinates:
        value = rational_fraction(expression)
        return value, value
    result = (Fraction(0), Fraction(0))
    for coefficient in sp.Poly(expression, coordinates[0]).all_coeffs():
        multiplied = _interval_multiply(result, box[0])
        added = horner_interval(coefficient, coordinates[1:], box[1:])
        result = multiplied[0] + added[0], multiplied[1] + added[1]
    return result


def fraction_text(value: Fraction) -> str:
    return (
        str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    )


def polynomial_coefficients(expression: sp.Expr, coordinates: tuple[sp.Symbol, ...]):
    """Yield canonical powers and exact real/imaginary coefficient parts."""

    for powers, coefficient in sp.Poly(sp.expand(expression), *coordinates, domain=QQ_I).terms():
        real, imaginary = sp.expand(coefficient).as_real_imag()
        yield powers, rational_fraction(real), rational_fraction(imaginary)


def serialize_polynomial(expression: sp.Expr, coordinates: tuple[sp.Symbol, ...]):
    result = []
    for powers, real, imaginary in polynomial_coefficients(expression, coordinates):
        real_text = fraction_text(real)
        value = real_text
        if imaginary:
            value = {"real": real_text, "imaginary": fraction_text(imaginary)}
        result.append({"powers": list(powers), "coefficient": value})
    return result


def serialize_matrix(matrix: sp.MatrixBase, coordinates: tuple[sp.Symbol, ...]):
    return [
        [serialize_polynomial(matrix[row, column], coordinates) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]

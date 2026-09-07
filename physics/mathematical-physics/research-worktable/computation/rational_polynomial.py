"""Bounded exact splitting of rational polynomials into linear factors."""

from __future__ import annotations

from fractions import Fraction
from math import gcd, isqrt, lcm


class FactorizationError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


def evaluate(coefficients: tuple[Fraction, ...], value: Fraction) -> Fraction:
    result = Fraction(0)
    for coefficient in reversed(coefficients):
        result = result * value + coefficient
    return result


def _consume(state: list[int], maximum_candidates: int) -> None:
    if state[0] >= maximum_candidates:
        raise FactorizationError(
            "FactorizationBudgetExceeded",
            "rational factor search exceeds the declared candidate budget",
        )
    state[0] += 1


def _divisors(value: int, state: list[int], maximum_candidates: int) -> tuple[int, ...]:
    result: set[int] = set()
    for candidate in range(1, isqrt(abs(value)) + 1):
        _consume(state, maximum_candidates)
        if value % candidate == 0:
            result.update((candidate, abs(value) // candidate))
    return tuple(sorted(result))


def _divide_linear(coefficients: tuple[Fraction, ...], root: Fraction) -> tuple[Fraction, ...]:
    quotient = [Fraction(0) for _ in range(len(coefficients) - 1)]
    quotient[-1] = coefficients[-1]
    for index in range(len(quotient) - 1, 0, -1):
        quotient[index - 1] = coefficients[index] + root * quotient[index]
    if coefficients[0] + root * quotient[0]:
        raise FactorizationError(
            "PolynomialDivisionResidual", "linear factor division is not exact"
        )
    return tuple(quotient)


def _rational_square_root(value: Fraction) -> Fraction | None:
    if value < 0:
        return None
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator**2 != value.numerator or denominator**2 != value.denominator:
        return None
    return Fraction(numerator, denominator)


def split_linear_roots(
    coefficients: tuple[Fraction, ...], maximum_candidates: int
) -> tuple[tuple[Fraction, ...], int]:
    remaining = coefficients
    roots: list[Fraction] = []
    state = [0]
    while len(remaining) > 1:
        if len(remaining) == 2:
            root = -remaining[0] / remaining[1]
        elif len(remaining) == 3:
            constant, linear, quadratic = remaining
            square_root = _rational_square_root(linear**2 - 4 * quadratic * constant)
            if square_root is None:
                raise FactorizationError(
                    "CoefficientFieldExtensionRequired",
                    "the minimal polynomial does not split over the rational field",
                )
            root = (-linear - square_root) / (2 * quadratic)
        elif remaining[0] == 0:
            root = Fraction(0)
        else:
            denominator = lcm(*(entry.denominator for entry in remaining))
            integral = [int(entry * denominator) for entry in remaining]
            common = gcd(*(abs(entry) for entry in integral if entry))
            integral = [entry // common for entry in integral]
            numerators = _divisors(integral[0], state, maximum_candidates)
            denominators = _divisors(integral[-1], state, maximum_candidates)
            candidate_upper_bound = 2 * len(numerators) * len(denominators)
            if state[0] + candidate_upper_bound > maximum_candidates:
                raise FactorizationError(
                    "FactorizationBudgetExceeded",
                    "rational root candidates exceed the declared search budget",
                )
            candidates = sorted(
                {
                    sign * Fraction(numerator, divisor)
                    for numerator in numerators
                    for divisor in denominators
                    for sign in (-1, 1)
                }
            )
            root = None
            for candidate in candidates:
                _consume(state, maximum_candidates)
                if evaluate(remaining, candidate) == 0:
                    root = candidate
                    break
            if root is None:
                raise FactorizationError(
                    "CoefficientFieldExtensionRequired",
                    "the minimal polynomial does not split over the rational field",
                )
        if root in roots:
            raise FactorizationError(
                "NonSemisimpleCoefficientAlgebra", "the minimal polynomial has a repeated root"
            )
        roots.append(root)
        remaining = remaining[1:] if root == 0 else _divide_linear(remaining, root)
    return tuple(sorted(roots)), state[0]

"""Gap-aware two-channel calibration constructed from an exact mode-bundle jet."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt, sin

import exact_gaussian_matrix as gaussian
from exact_gaussian_linear import Vector
from mode_bundle_jet import ModeBundleJet


class LeakageBoundError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


@dataclass(frozen=True)
class LeakageWindow:
    momentum: Fraction
    slow_scale: Fraction
    gap: Fraction
    time: Fraction
    prepared_column: int


@dataclass(frozen=True)
class LeakageBoundWitness:
    window: LeakageWindow
    off_block_vector: Vector
    coupling_squared: Fraction
    coupling: Fraction
    hamiltonian: gaussian.ComplexMatrix
    frequency_squared: Fraction
    frequency: Fraction
    transition_coefficient: Fraction
    phase: Fraction
    observed_probability: float
    short_time_bound: Fraction
    gap_bound: Fraction
    probability_bound: Fraction
    domain_contract: str
    observable: str
    construction_coordinates: int
    recovery_dimension: int
    checks: dict[str, bool]


def _admit_rational(value: object, label: str) -> Fraction:
    try:
        return gaussian.rational(value)
    except ValueError as error:
        raise LeakageBoundError("InexactWindowDatum", f"{label}: {error}") from error


def _exact_sqrt(value: Fraction, kind: str) -> Fraction:
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        raise LeakageBoundError(kind, f"{value} has no square root in Q")
    return Fraction(numerator, denominator)


def _combine_leakage(jet: ModeBundleJet, momentum: Fraction, column: int) -> Vector:
    first = jet.first_leakage_columns[column]
    second = jet.second_leakage_columns[column]
    factor = gaussian.Gaussian(2 * momentum)
    return tuple(
        factor * first_entry + second_entry
        for first_entry, second_entry in zip(first, second, strict=True)
    )


def _norm_squared(vector: Vector) -> Fraction:
    return sum(
        (entry.real * entry.real + entry.imaginary * entry.imaginary for entry in vector),
        Fraction(0),
    )


def construct_leakage_bound(jet: ModeBundleJet, window: LeakageWindow) -> LeakageBoundWitness:
    momentum = _admit_rational(window.momentum, "momentum")
    slow_scale = _admit_rational(window.slow_scale, "slow_scale")
    gap = _admit_rational(window.gap, "gap")
    time = _admit_rational(window.time, "time")
    column = window.prepared_column
    if gap <= 0:
        raise LeakageBoundError("ClosingGapObstruction", "the supplied gap must be positive")
    if slow_scale < 0:
        raise LeakageBoundError("NegativeSlowScale", "slow scale must be nonnegative")
    if time < 0:
        raise LeakageBoundError("NegativePropagationTime", "time must be nonnegative")
    if (
        isinstance(column, bool)
        or not isinstance(column, int)
        or not 0 <= column < len(jet.first_leakage_columns)
    ):
        raise LeakageBoundError("PreparedColumnMismatch", "prepared column is outside the carrier")

    raw_vector = _combine_leakage(jet, momentum, column)
    off_block_vector = tuple(gaussian.Gaussian(slow_scale) * entry for entry in raw_vector)
    coupling_squared = _norm_squared(off_block_vector)
    coupling = _exact_sqrt(coupling_squared, "ExactLeakageNormFieldExtensionRequired")
    half_gap = gap / 2
    frequency_squared = half_gap * half_gap + coupling_squared
    frequency = _exact_sqrt(frequency_squared, "ExactFrequencyFieldExtensionRequired")
    hamiltonian = gaussian.matrix(
        [[-half_gap, coupling], [coupling, half_gap]], "calibration Hamiltonian"
    )
    square_target = gaussian.scale(gaussian.identity(2), frequency_squared)
    transition_coefficient = coupling_squared / frequency_squared
    phase = frequency * time
    observed_probability = float(transition_coefficient) * sin(float(phase)) ** 2
    short_time_bound = coupling_squared * time * time
    gap_bound = 4 * coupling_squared / (gap * gap)
    probability_bound = min(Fraction(1), short_time_bound, gap_bound)
    zero_vector = tuple(gaussian.ZERO for _ in off_block_vector)
    checks = {
        "hamiltonian_is_hermitian": gaussian.is_hermitian(hamiltonian),
        "hamiltonian_square_identity": gaussian.multiply(hamiltonian, hamiltonian) == square_target,
        "transition_coefficient_is_probability_weight": Fraction(0) <= transition_coefficient <= 1,
        "observable_obeys_constructed_bound": 0.0
        <= observed_probability
        <= float(probability_bound) + 1e-15,
        "zero_leakage_recovers_zero_error": off_block_vector != zero_vector
        or (observed_probability == 0.0 and probability_bound == 0),
    }
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise LeakageBoundError("LeakageBoundResidual", f"construction fails at {failed}")
    return LeakageBoundWitness(
        window=LeakageWindow(momentum, slow_scale, gap, time, column),
        off_block_vector=off_block_vector,
        coupling_squared=coupling_squared,
        coupling=coupling,
        hamiltonian=hamiltonian,
        frequency_squared=frequency_squared,
        frequency=frequency,
        transition_coefficient=transition_coefficient,
        phase=phase,
        observed_probability=observed_probability,
        short_time_bound=short_time_bound,
        gap_bound=gap_bound,
        probability_bound=probability_bound,
        domain_contract="finite-dimensional bounded two-channel carrier",
        observable="transition probability from retained to leakage channel",
        construction_coordinates=len(off_block_vector),
        recovery_dimension=2,
        checks=checks,
    )

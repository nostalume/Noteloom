"""Reproducible solve-stage benchmark for G17 active propagation."""

from __future__ import annotations

import json
import platform
import sys
from dataclasses import replace
from fractions import Fraction
from importlib.metadata import version
from math import isfinite
from statistics import median
from time import perf_counter

from active_window_propagation import (
    construct_prepared_active_window,
    construct_prepared_coefficient_family_active_window,
    evaluate_active_window_at_time,
)
from coefficient_projector_jet import construct_projector_jet
from complete_route_bench import repeated_pauli_problem
from finite_window_propagation import construct_off_block_prepared_window, propagate_prepared_window
from gaussian_active_subspace import ActiveSubspaceBudget
from off_block_differential import construct_off_block_differential


def _prepared_problem(multiplicity: int, window_size: int):
    problem = repeated_pauli_problem(multiplicity, window_size)
    projector = construct_projector_jet(problem.coefficient_jet, problem.projector_budget)
    differential = construct_off_block_differential(
        problem.model,
        projector.projector,
        projector.first_off_block_operator,
        projector.second_off_block_operator,
        "G14 coefficient-derived projector jet",
    )
    prepared = construct_off_block_prepared_window(problem.model, differential, problem.window)
    return (
        problem,
        differential,
        prepared,
        ActiveSubspaceBudget(2 * multiplicity, 2 * multiplicity),
    )


def _retime(prepared, time: Fraction):
    coupling = sum(block.preparation_coupling_squared for block in prepared.blocks)
    short_bound = time * time * coupling / prepared.total_norm_squared
    probability_bound = min(Fraction(1), short_bound, prepared.gap_bound)
    return replace(
        prepared,
        window=replace(prepared.window, time=time),
        short_time_bound=short_bound,
        probability_bound=probability_bound,
    )


def _timing_summary(samples: list[float]) -> dict:
    if not samples or any(sample < 0 or not isfinite(sample) for sample in samples):
        raise ValueError("timing samples must be nonempty, finite, and nonnegative")
    center = median(samples)
    return {
        "sample_count": len(samples),
        "median_seconds": center,
        "median_absolute_deviation_seconds": median(abs(sample - center) for sample in samples),
        "minimum_seconds": min(samples),
        "maximum_seconds": max(samples),
    }


def _reuse_benchmark(prepared, budget, queries: int, repetitions: int) -> dict:
    times = tuple(Fraction(index + 1, queries) for index in range(queries))
    dense_samples = []
    active_samples = []
    for index in range(repetitions):
        order = ("dense", "active") if index % 2 == 0 else ("active", "dense")
        for route in order:
            started = perf_counter()
            if route == "dense":
                for time in times:
                    propagate_prepared_window(_retime(prepared, time))
                dense_samples.append(perf_counter() - started)
            else:
                active = construct_prepared_active_window(_retime(prepared, times[0]), budget)
                for time in times[1:]:
                    evaluate_active_window_at_time(active, time)
                active_samples.append(perf_counter() - started)
    dense_median = median(dense_samples)
    active_median = median(active_samples)
    return {
        "queries": queries,
        "dense_median_seconds": dense_median,
        "active_median_seconds": active_median,
        "active_over_dense_runtime_ratio": active_median / dense_median,
    }


def benchmark_case(multiplicity: int, window_size: int, repetitions: int = 5) -> dict:
    if repetitions <= 0:
        raise ValueError("repetitions must be positive")
    problem, differential, prepared, budget = _prepared_problem(multiplicity, window_size)
    dense = propagate_prepared_window(prepared)
    active = construct_prepared_active_window(prepared, budget)
    family = construct_prepared_coefficient_family_active_window(prepared, differential, budget)
    observable_error = abs(dense.full_transition_probability - active.active_probability)
    family_observable_error = abs(dense.full_transition_probability - family.active_probability)
    dense_times: list[float] = []
    active_times: list[float] = []
    family_times: list[float] = []
    for index in range(repetitions):
        orders = (
            ("dense", "active", "family"),
            ("active", "family", "dense"),
            ("family", "dense", "active"),
        )
        order = orders[index % len(orders)]
        for route in order:
            started = perf_counter()
            if route == "dense":
                propagate_prepared_window(prepared)
                dense_times.append(perf_counter() - started)
            elif route == "active":
                construct_prepared_active_window(prepared, budget)
                active_times.append(perf_counter() - started)
            else:
                construct_prepared_coefficient_family_active_window(prepared, differential, budget)
                family_times.append(perf_counter() - started)
    dense_median = median(dense_times)
    active_median = median(active_times)
    family_median = median(family_times)
    timing_summaries = {
        "dense": _timing_summary(dense_times),
        "pointwise_active": _timing_summary(active_times),
        "family": _timing_summary(family_times),
    }
    return {
        "multiplicity": multiplicity,
        "ambient_dimension": 2 * multiplicity,
        "window_size": window_size,
        "active_dimensions": list(active.active_dimensions),
        "family_active_dimension": family.active_dimension,
        "observable_error": observable_error,
        "family_observable_error": family_observable_error,
        "dense_median_seconds": dense_median,
        "active_median_seconds": active_median,
        "family_median_seconds": family_median,
        "timing_summaries": timing_summaries,
        "active_over_dense_runtime_ratio": active_median / dense_median,
        "family_over_pointwise_runtime_ratio": family_median / active_median,
        "full_exponential_cubic_proxy": active.cost.full_exponential_cubic_proxy,
        "active_exponential_cubic_proxy": active.cost.active_exponential_cubic_proxy,
        "exact_hamiltonian_actions": active.cost.hamiltonian_actions,
        "exact_coordinate_solves": active.cost.exact_coordinate_solves,
        "family_exact_coordinate_solves": family.cost.exact_coordinate_solves,
        "family_over_pointwise_coordinate_solve_ratio": (
            family.cost.exact_coordinate_solves / active.cost.exact_coordinate_solves
        ),
        "gram_and_effect_pairings": active.cost.gram_and_effect_pairings,
        "reuse": [_reuse_benchmark(prepared, budget, queries, repetitions) for queries in (16, 64)],
    }


def benchmark_family(repetitions: int = 5) -> dict:
    return {
        "contract": {
            "shared_before_timing": "G14 projector construction and exact Hamiltonian assembly",
            "dense_route": "full-carrier exponential and complement recovery",
            "active_route": "exact Krylov construction, compressed effect, reduced exponential",
            "family_route": "one coefficient-algebra closure, exact specialization, reduced exponential",
            "observable": "same norm-weighted finite-window complement probability",
            "interpretation": "solve-stage timing; exact and floating operation ledgers stay separate",
        },
        "environment": {
            "python": sys.version.split()[0],
            "numpy": version("numpy"),
            "scipy": version("scipy"),
            "platform": platform.platform(),
            "timer": "time.perf_counter",
            "repetitions": repetitions,
        },
        "cases": [
            benchmark_case(multiplicity, window_size, repetitions)
            for multiplicity in (2, 3)
            for window_size in (1, 4)
        ],
    }


if __name__ == "__main__":
    print(json.dumps(benchmark_family(), indent=2))

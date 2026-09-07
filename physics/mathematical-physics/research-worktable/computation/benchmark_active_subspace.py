"""Reproducible solve-stage benchmark for G17 active propagation."""

from __future__ import annotations

import json
import platform
import sys
from dataclasses import replace
from fractions import Fraction
from importlib.metadata import version
from statistics import median
from time import perf_counter

from active_window_propagation import (
    construct_prepared_active_window,
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
    return prepared, ActiveSubspaceBudget(2 * multiplicity, 2 * multiplicity)


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
    prepared, budget = _prepared_problem(multiplicity, window_size)
    dense = propagate_prepared_window(prepared)
    active = construct_prepared_active_window(prepared, budget)
    observable_error = abs(dense.full_transition_probability - active.active_probability)
    dense_times: list[float] = []
    active_times: list[float] = []
    for index in range(repetitions):
        order = ("dense", "active") if index % 2 == 0 else ("active", "dense")
        for route in order:
            started = perf_counter()
            if route == "dense":
                propagate_prepared_window(prepared)
                dense_times.append(perf_counter() - started)
            else:
                construct_prepared_active_window(prepared, budget)
                active_times.append(perf_counter() - started)
    dense_median = median(dense_times)
    active_median = median(active_times)
    return {
        "multiplicity": multiplicity,
        "ambient_dimension": 2 * multiplicity,
        "window_size": window_size,
        "active_dimensions": list(active.active_dimensions),
        "observable_error": observable_error,
        "dense_median_seconds": dense_median,
        "active_median_seconds": active_median,
        "active_over_dense_runtime_ratio": active_median / dense_median,
        "full_exponential_cubic_proxy": active.cost.full_exponential_cubic_proxy,
        "active_exponential_cubic_proxy": active.cost.active_exponential_cubic_proxy,
        "exact_hamiltonian_actions": active.cost.hamiltonian_actions,
        "exact_coordinate_solves": active.cost.exact_coordinate_solves,
        "gram_and_effect_pairings": active.cost.gram_and_effect_pairings,
        "reuse": [_reuse_benchmark(prepared, budget, queries, repetitions) for queries in (16, 64)],
    }


def benchmark_family(repetitions: int = 5) -> dict:
    return {
        "contract": {
            "shared_before_timing": "G14 projector construction and exact Hamiltonian assembly",
            "dense_route": "full-carrier exponential and complement recovery",
            "active_route": "exact Krylov construction, compressed effect, reduced exponential",
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

"""Selective local--bath factorization of generated graded insertions."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .graded_return import FunctionalPortRefusal, FunctionalRestrictionPacket
from .perturbative_return import PerturbativeReturnModel


@dataclass(frozen=True)
class SelectiveFactorizationReceipt:
    carrier_ranks: tuple[int, ...]
    insertion_ranks: tuple[int, ...]
    ranks_by_tolerance: tuple[tuple[int, ...], ...]
    total_carrier_factors: int
    total_insertion_factors: int
    dense_local_bound: int
    maximum_recovery_residual: float
    rank_stable: bool


def _factorize(
    operator: np.ndarray,
    local_dimension: int,
    tolerance: float,
) -> tuple[int, np.ndarray, float]:
    dimension = operator.shape[0]
    bath_dimension = dimension // local_dimension
    coefficient_map = operator.reshape(
        bath_dimension,
        local_dimension,
        bath_dimension,
        local_dimension,
    ).transpose(1, 3, 0, 2).reshape(
        local_dimension**2,
        bath_dimension**2,
    )
    left, singular_values, right = np.linalg.svd(
        coefficient_map,
        full_matrices=False,
    )
    scale = max(1.0, float(singular_values[0]))
    rank = int(np.count_nonzero(singular_values > tolerance * scale))
    reconstructed_map = (
        left[:, :rank] * singular_values[:rank]
    ) @ right[:rank]
    reconstructed = reconstructed_map.reshape(
        local_dimension,
        local_dimension,
        bath_dimension,
        bath_dimension,
    ).transpose(2, 0, 3, 1).reshape(dimension, dimension)
    residual = float(np.linalg.norm(operator - reconstructed))
    return rank, reconstructed, residual


def audited_endpoint_functional(
    source: PerturbativeReturnModel,
    local_dimension: int,
    factor_budget: int,
):
    """Audit generated operators, then evaluate their recomposed insertions."""
    def evaluate(operators: tuple[np.ndarray, ...]) -> FunctionalRestrictionPacket:
        dimension = source.system.free_hamiltonian.shape[0]
        if local_dimension < 1 or dimension % local_dimension:
            raise FunctionalPortRefusal(
                "local dimension does not divide the Hilbert dimension",
            )
        creation = source.system.impurity_annihilator.conj().T
        insertions = tuple(
            operator @ creation + creation @ operator
            for operator in operators
        )

        tolerance_rows = []
        carrier_ranks = insertion_ranks = ()
        reconstructed_insertions = ()
        maximum_residual = 0.0
        for tolerance in (1e-8, 1e-10, 1e-12):
            carrier_results = tuple(
                _factorize(operator, local_dimension, tolerance)
                for operator in operators
            )
            insertion_results = tuple(
                _factorize(operator, local_dimension, tolerance)
                for operator in insertions
            )
            ranks = tuple(result[0] for result in insertion_results)
            tolerance_rows.append(ranks)
            if tolerance == 1e-10:
                carrier_ranks = tuple(result[0] for result in carrier_results)
                insertion_ranks = ranks
                reconstructed_insertions = tuple(
                    result[1] for result in insertion_results
                )
                maximum_residual = max(
                    *(result[2] for result in carrier_results),
                    *(result[2] for result in insertion_results),
                )

        total_insertion = sum(insertion_ranks)
        if total_insertion > factor_budget:
            raise FunctionalPortRefusal("selective factor budget exceeded")
        restrictions = tuple(
            tuple(
                complex(np.trace(thermal @ insertion))
                for insertion in reconstructed_insertions
            )
            for thermal in source.thermal_coefficients
        )
        receipt = SelectiveFactorizationReceipt(
            carrier_ranks=carrier_ranks,
            insertion_ranks=insertion_ranks,
            ranks_by_tolerance=tuple(tolerance_rows),
            total_carrier_factors=sum(carrier_ranks),
            total_insertion_factors=total_insertion,
            dense_local_bound=local_dimension**2 * len(operators),
            maximum_recovery_residual=maximum_residual,
            rank_stable=len(set(tolerance_rows)) == 1,
        )
        return FunctionalRestrictionPacket(
            partition_coefficients=source.partition_coefficients,
            restrictions=restrictions,
            kind="factor-audited endpoint",
            error=maximum_residual,
            cells=0,
            materialized_endpoint_matrices=2 * len(source.thermal_coefficients),
            metadata=receipt,
        )

    return evaluate

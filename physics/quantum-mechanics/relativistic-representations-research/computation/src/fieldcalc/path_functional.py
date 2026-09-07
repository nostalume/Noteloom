"""Closed interaction-path realization of a reduced thermal functional port."""

from __future__ import annotations

import numpy as np

from .graded_return import FunctionalPortRefusal, FunctionalRestrictionPacket
from .impurity import AndersonSystem
from .numeric import ordered_simplex


def anderson_closed_path_functional(
    system: AndersonSystem,
    quadrature_order: int,
    resource_budget: int,
):
    """Return a factory evaluating only scalar Dyson-path restrictions."""
    def evaluate(operators: tuple[np.ndarray, ...]) -> FunctionalRestrictionPacket:
        if quadrature_order < 3:
            raise FunctionalPortRefusal(
                "closed-path quadrature order must be at least three",
            )
        free = system.free_hamiltonian
        interaction = system.hybridization_action
        if np.linalg.norm(free - np.diag(np.diag(free))) > 1e-12:
            raise FunctionalPortRefusal("closed-path v1 requires diagonal free propagation")
        if max(
            np.linalg.norm(free - free.conj().T),
            np.linalg.norm(interaction - interaction.conj().T),
        ) > 1e-12:
            raise FunctionalPortRefusal("closed-path action is not Hermitian")

        order = system.request.coefficient_order
        rank = len(operators)
        cell_estimate = (rank + 1) * sum(
            quadrature**degree
            for quadrature in (quadrature_order, quadrature_order + 2)
            for degree in range(order + 1)
        )
        if cell_estimate > resource_budget:
            raise FunctionalPortRefusal("closed-path functional budget exceeded")

        energies = np.diag(free).real
        creation = system.impurity_annihilator.conj().T
        insertions = np.asarray([
            operator @ creation + creation @ operator
            for operator in operators
        ])

        def integrate(size: int):
            partitions = np.zeros(order + 1, dtype=complex)
            restrictions = np.zeros((order + 1, rank), dtype=complex)
            cells = 0
            for degree in range(order + 1):
                sign = (-1) ** degree
                quadrature_cells = list(ordered_simplex(
                    system.request.beta,
                    degree,
                    size,
                ))
                for start in range(0, len(quadrature_cells), 128):
                    batch = quadrature_cells[start:start + 128]
                    times = np.asarray([cell[0] for cell in batch], dtype=float)
                    weights = sign * np.asarray([cell[1] for cell in batch])
                    if degree == 0:
                        times = np.empty((1, 0))
                    left_edges = (
                        np.full(len(batch), system.request.beta)
                        if degree == 0 else system.request.beta - times[:, 0]
                    )
                    diagonal = np.exp(-left_edges[:, None] * energies[None, :])
                    chain = np.zeros(
                        (len(batch), len(energies), len(energies)),
                        dtype=complex,
                    )
                    diagonal_indices = np.arange(len(energies))
                    chain[:, diagonal_indices, diagonal_indices] = diagonal
                    for vertex in range(degree):
                        right_edge = (
                            times[:, vertex + 1]
                            if vertex + 1 < degree else np.zeros(len(batch))
                        )
                        interval = times[:, vertex] - right_edge
                        chain = np.matmul(chain, interaction)
                        chain *= np.exp(
                            -interval[:, None] * energies[None, :],
                        )[:, None, :]
                    partitions[degree] += np.sum(
                        weights * np.trace(chain, axis1=1, axis2=2),
                    )
                    restrictions[degree] += np.einsum(
                        "b,bij,kji->k",
                        weights,
                        chain,
                        insertions,
                    )
                    cells += len(batch)
            return partitions, restrictions, cells

        low_partition, low_restrictions, low_cells = integrate(quadrature_order)
        high_partition, high_restrictions, high_cells = integrate(quadrature_order + 2)
        error = float(max(
            np.max(abs(high_partition - low_partition)),
            np.max(abs(high_restrictions - low_restrictions)),
        ))
        return FunctionalRestrictionPacket(
            partition_coefficients=tuple(complex(value) for value in high_partition),
            restrictions=tuple(
                tuple(complex(value) for value in row)
                for row in high_restrictions
            ),
            kind="closed interaction paths",
            error=error,
            cells=low_cells + high_cells,
            materialized_endpoint_matrices=0,
        )

    return evaluate

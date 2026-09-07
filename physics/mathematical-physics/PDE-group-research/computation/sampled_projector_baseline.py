"""Three-sample numerical projector jet and finite-carrier propagation baseline."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.linalg import expm

import exact_gaussian_matrix as gaussian
from coefficient_projector_jet import CoefficientJet
from finite_window_propagation import FinitePropagationWindow
from simple_block_pde import IrreducibleModel


class SampledProjectorError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


@dataclass(frozen=True)
class SampledRouteWitness:
    probability: float
    cluster_rank: int
    projector_residual: float
    maximum_unitarity_residual: float


def _numpy_matrix(value: gaussian.ComplexMatrix) -> np.ndarray:
    return np.array(
        [[complex(float(entry.real), float(entry.imaginary)) for entry in row] for row in value],
        dtype=np.complex128,
    )


def _numpy_vector(value) -> np.ndarray:
    return np.array(
        [complex(float(entry.real), float(entry.imaginary)) for entry in value],
        dtype=np.complex128,
    )


def _spectral_projector(
    value: np.ndarray, selected_value: float, rank_: int | None, tolerance: float
) -> tuple[np.ndarray, int]:
    eigenvalues, eigenvectors = np.linalg.eigh(value)
    distances = np.abs(eigenvalues - selected_value)
    if rank_ is None:
        selected = np.flatnonzero(distances <= tolerance)
        if not len(selected) or len(selected) == len(eigenvalues):
            raise SampledProjectorError(
                "SampledClusterUnseparated",
                "central sampled cluster is absent or has no separated complement",
            )
        rank_ = len(selected)
    else:
        order = np.argsort(distances)
        selected = order[:rank_]
        if (
            rank_ == len(eigenvalues)
            or distances[order[rank_]] - distances[order[rank_ - 1]] <= tolerance
        ):
            raise SampledProjectorError(
                "SampledClusterAmbiguous", "sampled side cluster is not uniquely rank-separated"
            )
    frame = eigenvectors[:, selected]
    return frame @ frame.conj().T, rank_


def _projector_jet(
    jet: CoefficientJet, step: float, cluster_tolerance: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    value = _numpy_matrix(jet.value)
    first = _numpy_matrix(jet.first_derivative)
    second = _numpy_matrix(jet.second_derivative)
    selected = float(jet.selected_eigenvalue)
    central, rank_ = _spectral_projector(value, selected, None, cluster_tolerance)

    def sample(offset: float) -> np.ndarray:
        return value + offset * first + 0.5 * offset * offset * second

    plus, _ = _spectral_projector(sample(step), selected, rank_, cluster_tolerance)
    minus, _ = _spectral_projector(sample(-step), selected, rank_, cluster_tolerance)
    derivative = (plus - minus) / (2 * step)
    acceleration = (plus - 2 * central + minus) / (step * step)
    complement = np.eye(len(value)) - central
    return (
        central,
        complement @ derivative @ central,
        complement @ acceleration @ central,
        rank_,
    )


def construct_sampled_route(
    model: IrreducibleModel,
    coefficient_jet: CoefficientJet,
    window: FinitePropagationWindow,
    finite_difference_step: float,
    cluster_tolerance: float,
) -> SampledRouteWitness:
    projector, first, second, cluster_rank = _projector_jet(
        coefficient_jet, finite_difference_step, cluster_tolerance
    )
    complement = np.eye(len(projector)) - projector
    embedding = np.column_stack(tuple(_numpy_vector(vector) for vector in model.embedding_columns))
    numerator = 0.0
    total_norm = 0.0
    maximum_unitarity_residual = 0.0
    for momentum, gap, preparation in zip(
        window.momenta,
        window.gaps,
        window.preparations,
        strict=True,
    ):
        arrow = float(window.slow_scale) * (2 * float(momentum) * first + second)
        baseline = float(gap) * (np.eye(len(projector)) - 2 * projector) / 2
        hamiltonian = baseline + arrow + arrow.conj().T
        state0 = embedding @ _numpy_vector(preparation)
        norm = float(np.vdot(state0, state0).real)
        propagator = expm(-1j * float(window.time) * hamiltonian)
        state = propagator @ state0
        numerator += float(np.vdot(state, complement @ state).real)
        total_norm += norm
        maximum_unitarity_residual = max(
            maximum_unitarity_residual,
            float(np.linalg.norm(propagator.conj().T @ propagator - np.eye(len(projector)))),
        )
    if not total_norm:
        raise SampledProjectorError("ZeroComparisonPreparation", "preparation must be nonzero")
    return SampledRouteWitness(
        probability=numerator / total_norm,
        cluster_rank=cluster_rank,
        projector_residual=float(np.linalg.norm(projector @ projector - projector)),
        maximum_unitarity_residual=maximum_unitarity_residual,
    )

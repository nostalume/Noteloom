"""Finite Anderson adapter and independently generated response coefficients."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from scipy.linalg import eigh
from scipy.sparse import csc_matrix, eye as sparse_eye, kron as sparse_kron
from scipy.sparse.linalg import expm_multiply

from .rewrite import Refusal


@dataclass(frozen=True)
class AndersonRequest:
    impurity_energy: float
    interaction: float
    bath_energies: tuple[float, ...]
    hybridizations: tuple[complex, ...]
    beta: float
    matsubara_index: int
    coefficient_order: int
    quadrature_order: int
    provenance: str
    resource_budget: int


@dataclass(frozen=True)
class CoefficientCost:
    block_dimension: int
    exponentials: int
    quadrature_nodes: int


@dataclass(frozen=True)
class GreenCoefficients:
    values: tuple[complex, ...]
    cost: CoefficientCost


@dataclass(frozen=True)
class CarCertificate:
    maximum_residual: float


@dataclass(frozen=True)
class AndersonCompilation:
    system: "AndersonSystem | None" = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def car_annihilator(mode: int, mode_count: int) -> np.ndarray:
    """Serialize CAR action; the prefix occupation generates every sign."""
    dimension = 1 << mode_count
    action = np.zeros((dimension, dimension), dtype=complex)
    prefix = (1 << mode) - 1
    for state in range(dimension):
        if state & (1 << mode):
            target = state ^ (1 << mode)
            action[target, state] = (-1) ** ((state & prefix).bit_count())
    return action


class AndersonSystem:
    def __init__(
        self,
        request: AndersonRequest,
        annihilators: tuple[np.ndarray, ...],
        free_hamiltonian: np.ndarray,
        hybridization_action: np.ndarray,
    ):
        self.request = request
        self.annihilators = annihilators
        self.free_hamiltonian = free_hamiltonian
        self.hybridization_action = hybridization_action
        self.impurity_annihilator = annihilators[0]

    def car_certificate(self) -> CarCertificate:
        identity = np.eye(self.free_hamiltonian.shape[0])
        maximum = 0.0
        for left, annihilator_left in enumerate(self.annihilators):
            for right, annihilator_right in enumerate(self.annihilators):
                residual = (
                    annihilator_left @ annihilator_right.conj().T
                    + annihilator_right.conj().T @ annihilator_left
                    - (identity if left == right else 0.0)
                )
                maximum = max(maximum, float(np.linalg.norm(residual)))
        return CarCertificate(maximum)

    def hamiltonian(self, coupling: float) -> np.ndarray:
        return self.free_hamiltonian + coupling * self.hybridization_action

    def hybridization(self, spectral_parameter: complex) -> complex:
        return sum(
            abs(coupling) ** 2 / (spectral_parameter - energy)
            for energy, coupling in zip(
                self.request.bath_energies,
                self.request.hybridizations,
                strict=True,
            )
        )

    @property
    def matsubara_frequency(self) -> float:
        return (
            (2 * self.request.matsubara_index + 1)
            * math.pi
            / self.request.beta
        )

    def green(self, coupling: float) -> complex:
        """Full-Hilbert Lehmann value; no graph or coefficient route is used."""
        energies, vectors = eigh(self.hamiltonian(coupling))
        boltzmann = np.exp(-self.request.beta * energies)
        partition = boltzmann.sum()
        impurity = vectors.conj().T @ self.impurity_annihilator @ vectors
        denominator = (
            1j * self.matsubara_frequency
            + energies[:, None]
            - energies[None, :]
        )
        numerator = boltzmann[:, None] + boltzmann[None, :]
        return complex(np.sum(numerator * abs(impurity) ** 2 / denominator) / partition)

    def thermal_coefficients(self, time: float) -> tuple[np.ndarray, ...]:
        """Generate coupling coefficients of ``exp(-time H(lambda))`` once."""
        order = self.request.coefficient_order
        dimension = self.free_hamiltonian.shape[0]
        block = csc_matrix(-self.free_hamiltonian)
        descent = csc_matrix(-self.hybridization_action)
        generator = sparse_kron(sparse_eye(order + 1), block, format="csc")
        shift = csc_matrix(
            (np.ones(order), (np.arange(1, order + 1), np.arange(order))),
            shape=(order + 1, order + 1),
        )
        generator += sparse_kron(shift, descent, format="csc")
        seed = np.zeros(((order + 1) * dimension, dimension), dtype=complex)
        seed[:dimension] = np.eye(dimension)
        trace = -(order + 1) * np.trace(self.free_hamiltonian)
        evolved = expm_multiply(generator * time, seed, traceA=trace * time)
        return tuple(
            evolved[index * dimension:(index + 1) * dimension]
            for index in range(order + 1)
        )

    def green_coefficients(self) -> GreenCoefficients:
        """Coefficients generated by the block Dyson recurrence in node 41."""
        order = self.request.coefficient_order
        beta = self.request.beta
        nodes, weights = np.polynomial.legendre.leggauss(
            self.request.quadrature_order,
        )
        times = 0.5 * beta * (nodes + 1.0)
        weights = 0.5 * beta * weights
        thermal_beta = self.thermal_coefficients(beta)
        partition = np.array([np.trace(matrix) for matrix in thermal_beta])
        numerator = np.zeros(order + 1, dtype=complex)
        creation = self.impurity_annihilator.conj().T
        for time, weight in zip(times, weights, strict=True):
            left = self.thermal_coefficients(beta - time)
            right = self.thermal_coefficients(time)
            phase = np.exp(1j * self.matsubara_frequency * time)
            for total in range(order + 1):
                value = sum(
                    np.trace(
                        left[left_order]
                        @ self.impurity_annihilator
                        @ right[total - left_order]
                        @ creation
                    )
                    for left_order in range(total + 1)
                )
                numerator[total] -= weight * phase * value
        values = np.zeros(order + 1, dtype=complex)
        for total in range(order + 1):
            correction = sum(
                partition[index] * values[total - index]
                for index in range(1, total + 1)
            )
            values[total] = (numerator[total] - correction) / partition[0]
        dimension = self.free_hamiltonian.shape[0]
        return GreenCoefficients(
            tuple(complex(value) for value in values),
            CoefficientCost(
                block_dimension=(order + 1) * dimension,
                exponentials=2 * self.request.quadrature_order + 1,
                quadrature_nodes=self.request.quadrature_order,
            ),
        )

def _refuse(request: AndersonRequest, reason: str) -> AndersonCompilation:
    return AndersonCompilation(refusal=Refusal(reason, provenance=request.provenance))


def compile_anderson(request: AndersonRequest) -> AndersonCompilation:
    if len(request.bath_energies) != len(request.hybridizations):
        return _refuse(request, "bath energies and hybridizations have different lengths")
    if not request.bath_energies:
        return _refuse(request, "bath is empty")
    real_parameters = (
        request.impurity_energy,
        request.interaction,
        request.beta,
        *request.bath_energies,
    )
    if any(not math.isfinite(value) for value in real_parameters):
        return _refuse(request, "real model parameters must be finite")
    if any(
        not math.isfinite(complex(value).real)
        or not math.isfinite(complex(value).imag)
        for value in request.hybridizations
    ):
        return _refuse(request, "hybridizations must be finite")
    if request.beta <= 0:
        return _refuse(request, "inverse temperature must be positive")
    if request.matsubara_index < 0:
        return _refuse(request, "Matsubara index must be nonnegative")
    if request.coefficient_order < 0 or request.coefficient_order > 6:
        return _refuse(request, "coefficient order lies outside the bounded adapter")
    if request.quadrature_order < 4:
        return _refuse(request, "quadrature order must be at least four")

    mode_count = 2 + 2 * len(request.bath_energies)
    dimension = 1 << mode_count
    block_dimension = (request.coefficient_order + 1) * dimension
    estimated_storage_work = (
        (2 * request.quadrature_order + 1) * block_dimension * dimension
    )
    if estimated_storage_work > request.resource_budget:
        return _refuse(request, "Anderson transfer budget exceeded")

    annihilators = tuple(car_annihilator(mode, mode_count) for mode in range(mode_count))
    numbers = tuple(action.conj().T @ action for action in annihilators)
    free = (
        request.impurity_energy * (numbers[0] + numbers[1])
        + request.interaction * numbers[0] @ numbers[1]
    )
    hybridization = np.zeros((dimension, dimension), dtype=complex)
    for bath, (energy, coupling) in enumerate(zip(
        request.bath_energies,
        request.hybridizations,
        strict=True,
    )):
        for spin in range(2):
            bath_mode = 2 + 2 * bath + spin
            free += energy * numbers[bath_mode]
            impurity = annihilators[spin]
            bath_action = annihilators[bath_mode]
            hybridization += (
                coupling * bath_action.conj().T @ impurity
                + complex(coupling).conjugate() * impurity.conj().T @ bath_action
            )
    return AndersonCompilation(AndersonSystem(
        request,
        annihilators,
        np.asarray(free, dtype=complex),
        hybridization,
    ))

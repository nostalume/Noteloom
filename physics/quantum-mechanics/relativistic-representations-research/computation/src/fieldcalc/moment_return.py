"""Scalar return construction from a source correlation functional."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import math

import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import expm_multiply

from .impurity import AndersonSystem
from .return_reduction import ReturnCertificate
from .rewrite import Refusal


VectorAction = Callable[[np.ndarray], np.ndarray]
Correlation = Callable[[np.ndarray], complex]


@dataclass(frozen=True)
class FunctionalReturnProblem:
    dimension: int
    source: np.ndarray
    apply_generator: VectorAction
    correlate: Correlation
    hermitian_residual: float
    thermal_actions: int
    action_cost_per_vector: int
    correlation_cost: int
    construction_cost: int
    baseline_setup_cost: int
    direct_query_cost: int
    provenance: str


@dataclass(frozen=True)
class MomentCost:
    thermal_actions: int
    generator_actions: int
    correlation_evaluations: int
    estimated_setup_operations: int
    baseline_setup_operations: int
    direct_query_operations: int
    certified_query_operations: int
    certified_break_even_queries: int | None


@dataclass(frozen=True)
class MomentReturnModel:
    problem: FunctionalReturnProblem
    moments: tuple[complex, ...]
    jacobi: np.ndarray
    eigenvalues: np.ndarray
    spectral_source: np.ndarray
    terminal_beta: float
    cost: MomentCost

    @property
    def rank(self) -> int:
        return self.jacobi.shape[0]

    def evaluate(self, z: complex) -> np.ndarray:
        value = np.sum(abs(self.spectral_source) ** 2 / (z - self.eigenvalues))
        return np.array([[value]], dtype=complex)

    def certified_evaluate(self, z: complex) -> ReturnCertificate:
        distance = abs(complex(z).imag)
        if distance == 0:
            raise ValueError("resolvent certificate requires an off-axis query")
        coefficients = np.linalg.solve(
            z * np.eye(self.rank) - self.jacobi,
            np.r_[math.sqrt(self.moments[0].real), np.zeros(self.rank - 1)],
        )
        residual = self.terminal_beta * abs(coefficients[-1])
        return ReturnCertificate(
            self.evaluate(z),
            residual,
            math.sqrt(self.moments[0].real) * residual / distance,
        )

    def moment_residuals(self, count: int) -> tuple[float, ...]:
        if count < 1 or count > len(self.moments):
            raise ValueError("moment count lies outside the generated packet")
        source = np.r_[math.sqrt(self.moments[0].real), np.zeros(self.rank - 1)]
        power = source.copy()
        residuals = []
        for order in range(count):
            reduced = source.conj() @ power
            residuals.append(abs(self.moments[order] - reduced))
            power = self.jacobi @ power
        return tuple(float(value) for value in residuals)


@dataclass(frozen=True)
class MomentReturnCompilation:
    model: MomentReturnModel | None = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def _refuse(
    problem: FunctionalReturnProblem,
    reason: str,
) -> MomentReturnCompilation:
    return MomentReturnCompilation(
        refusal=Refusal(reason, provenance=problem.provenance),
    )


def _moment_inner(left, right, moments) -> complex:
    return sum(
        left[index].conjugate() * right[other] * moments[index + other]
        for index in range(len(left))
        for other in range(len(right))
    )


def compile_moment_return(
    problem: FunctionalReturnProblem,
    depth: int,
    resource_budget: int,
    tolerance: float = 1e-11,
) -> MomentReturnCompilation:
    if depth < 1:
        return _refuse(problem, "moment depth must be positive")
    if problem.hermitian_residual > tolerance:
        return _refuse(problem, "return generator is not Hermitian")
    if tolerance <= 0 or not math.isfinite(tolerance):
        return _refuse(problem, "moment tolerance must be finite and positive")

    generator_actions = 2 * depth
    correlation_evaluations = 2 * depth + 1
    setup_operations = (
        problem.construction_cost
        + generator_actions * problem.action_cost_per_vector
        + correlation_evaluations * problem.correlation_cost
        + depth**3
    )
    if setup_operations > resource_budget:
        return _refuse(problem, "moment return budget exceeded")

    moments = []
    power = problem.source.copy()
    for _ in range(correlation_evaluations):
        value = complex(problem.correlate(power))
        if abs(value.imag) > tolerance * max(1.0, abs(value.real)):
            return _refuse(problem, "correlation moments are not Hermitian")
        moments.append(complex(value.real))
        power = problem.apply_generator(power)
    if moments[0].real <= tolerance:
        return _refuse(problem, "correlation functional is not positive")

    width = depth + 1
    previous = np.zeros(width, dtype=complex)
    current = np.zeros(width, dtype=complex)
    current[0] = 1.0 / math.sqrt(moments[0].real)
    previous_beta = 0.0
    diagonal: list[float] = []
    off_diagonal: list[float] = []
    terminal_beta = 0.0
    for step in range(depth):
        shifted = np.roll(current, 1)
        shifted[0] = 0.0
        alpha = float(_moment_inner(current, shifted, moments).real)
        residual = shifted - alpha * current - previous_beta * previous
        norm_squared = float(_moment_inner(residual, residual, moments).real)
        if norm_squared < -tolerance:
            return _refuse(problem, "correlation functional is not positive")
        beta = math.sqrt(max(0.0, norm_squared))
        diagonal.append(alpha)
        terminal_beta = beta
        if step == depth - 1 or beta <= tolerance:
            break
        off_diagonal.append(beta)
        previous, current = current, residual / beta
        previous_beta = beta

    rank = len(diagonal)
    jacobi = np.diag(diagonal)
    if rank > 1:
        edges = np.asarray(off_diagonal[:rank - 1])
        jacobi += np.diag(edges, 1) + np.diag(edges, -1)
    eigenvalues, eigenvectors = np.linalg.eigh(jacobi)
    projected_source = np.r_[math.sqrt(moments[0].real), np.zeros(rank - 1)]
    spectral_source = eigenvectors.conj().T @ projected_source
    certified_query = 2 * rank
    saving = problem.direct_query_cost - certified_query
    extra_setup = setup_operations - problem.baseline_setup_cost
    break_even = (
        None if saving <= 0
        else 1 if extra_setup <= 0
        else math.floor(extra_setup / saving) + 1
    )
    return MomentReturnCompilation(MomentReturnModel(
        problem,
        tuple(moments),
        jacobi,
        eigenvalues,
        spectral_source,
        terminal_beta,
        MomentCost(
            problem.thermal_actions,
            generator_actions,
            correlation_evaluations,
            setup_operations,
            problem.baseline_setup_cost,
            problem.direct_query_cost,
            certified_query,
            break_even,
        ),
    ))


def anderson_correlation_problem(
    system: AndersonSystem,
    coupling: float,
) -> FunctionalReturnProblem:
    hamiltonian = system.hamiltonian(coupling)
    hilbert_dimension = hamiltonian.shape[0]
    source_operator = system.impurity_annihilator
    sparse_hamiltonian = csc_matrix(hamiltonian)
    left = expm_multiply(
        -system.request.beta * sparse_hamiltonian,
        source_operator,
    )
    right = expm_multiply(
        -system.request.beta * sparse_hamiltonian,
        source_operator.conj().T,
    ).conj().T
    dual = left + right
    normalization = complex(np.vdot(dual, source_operator))
    source = source_operator.reshape(-1, 1)

    def liouvillian(values):
        operators = values.reshape(
            hilbert_dimension,
            hilbert_dimension,
            values.shape[1],
        )
        acted_right = np.einsum("ijk,jl->ilk", operators, hamiltonian)
        acted_left = np.einsum("ij,jlk->ilk", hamiltonian, operators)
        return (acted_right - acted_left).reshape(
            hilbert_dimension**2,
            values.shape[1],
        )

    def correlate(values):
        if values.shape != source.shape:
            raise ValueError("correlation functional accepts one operator")
        return complex(np.vdot(dual, values.reshape(source_operator.shape)) / normalization)

    nonzero_entries = int(np.count_nonzero(abs(hamiltonian) > 1e-14))
    return FunctionalReturnProblem(
        dimension=hilbert_dimension**2,
        source=source,
        apply_generator=liouvillian,
        correlate=correlate,
        hermitian_residual=float(np.linalg.norm(
            hamiltonian - hamiltonian.conj().T,
        )),
        thermal_actions=2,
        action_cost_per_vector=2 * nonzero_entries * hilbert_dimension,
        correlation_cost=hilbert_dimension**2,
        construction_cost=2 * hilbert_dimension**3,
        baseline_setup_cost=2 * hilbert_dimension**3,
        direct_query_cost=hilbert_dimension**2,
        provenance=f"{system.request.provenance}: correlation-functional return",
    )

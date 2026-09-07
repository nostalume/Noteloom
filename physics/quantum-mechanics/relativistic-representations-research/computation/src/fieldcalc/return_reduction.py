"""Observable-cyclic projection for finite Hermitian return problems."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import math

import numpy as np
from scipy.linalg import eigh, expm

from .impurity import AndersonSystem
from .pauli_fierz import PauliFierzSystem
from .rewrite import Refusal


MatrixAction = Callable[[np.ndarray], np.ndarray]
ReturnEvaluator = Callable[[complex], np.ndarray]


@dataclass(frozen=True)
class ReturnProblem:
    dimension: int
    source: np.ndarray
    apply_generator: MatrixAction
    apply_metric: MatrixAction
    evaluate: ReturnEvaluator
    hermitian_residual: float
    action_cost_per_vector: int
    metric_cost_per_vector: int
    construction_cost: int
    baseline_setup_cost: int
    direct_query_cost: int
    provenance: str

    @classmethod
    def from_dense(cls, generator, source, provenance: str) -> "ReturnProblem":
        matrix = np.asarray(generator, dtype=complex)
        port = _as_source(source)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("return generator must be square")
        if port.shape[0] != matrix.shape[0]:
            raise ValueError("return source has the wrong generator dimension")

        def action(values):
            return matrix @ values

        def evaluator(z):
            return port.conj().T @ np.linalg.solve(
                z * np.eye(matrix.shape[0]) - matrix,
                port,
            )

        dimension = matrix.shape[0]
        return cls(
            dimension=dimension,
            source=port,
            apply_generator=action,
            apply_metric=lambda values: values,
            evaluate=evaluator,
            hermitian_residual=float(np.linalg.norm(matrix - matrix.conj().T)),
            action_cost_per_vector=dimension**2,
            metric_cost_per_vector=0,
            construction_cost=0,
            baseline_setup_cost=dimension**3,
            direct_query_cost=dimension * port.shape[1] ** 2,
            provenance=provenance,
        )

    @classmethod
    def from_diagonal(
        cls,
        spectrum,
        source,
        provenance: str,
        construction_cost: int = 0,
        baseline_setup_cost: int = 0,
    ) -> "ReturnProblem":
        values = np.asarray(spectrum, dtype=complex)
        port = _as_source(source)
        if values.ndim != 1:
            raise ValueError("return spectrum must be one-dimensional")
        if port.shape[0] != values.size:
            raise ValueError("return source has the wrong spectrum dimension")

        def action(vectors):
            return values[:, None] * vectors

        def evaluator(z):
            return port.conj().T @ (port / (z - values)[:, None])

        dimension = values.size
        return cls(
            dimension=dimension,
            source=port,
            apply_generator=action,
            apply_metric=lambda vectors: vectors,
            evaluate=evaluator,
            hermitian_residual=float(np.linalg.norm(values.imag)),
            action_cost_per_vector=dimension,
            metric_cost_per_vector=0,
            construction_cost=construction_cost,
            baseline_setup_cost=baseline_setup_cost,
            direct_query_cost=dimension * port.shape[1] ** 2,
            provenance=provenance,
        )

    def inner(self, left, right) -> np.ndarray:
        left_values = _as_source(left)
        right_values = _as_source(right)
        if left_values.shape[0] != self.dimension or right_values.shape[0] != self.dimension:
            raise ValueError("metric input has the wrong generator dimension")
        return left_values.conj().T @ self.apply_metric(right_values)


@dataclass(frozen=True)
class CyclicCost:
    generator_actions: int
    metric_operations: int
    estimated_setup_operations: int
    baseline_setup_operations: int
    direct_query_operations: int
    reduced_query_operations: int
    break_even_queries: int | None
    certified_query_operations: int
    certified_break_even_queries: int | None


@dataclass(frozen=True)
class ReturnCertificate:
    value: np.ndarray
    residual_bound: float
    error_bound: float


@dataclass(frozen=True)
class CyclicReturnModel:
    problem: ReturnProblem
    basis: np.ndarray
    projected_generator: np.ndarray
    projected_source: np.ndarray
    eigenvalues: np.ndarray
    eigenvectors: np.ndarray
    spectral_source: np.ndarray
    source_norm: float
    residual_gram: np.ndarray
    cost: CyclicCost

    @property
    def rank(self) -> int:
        return self.projected_generator.shape[0]

    def evaluate(self, z: complex) -> np.ndarray:
        return self.spectral_source.conj().T @ (
            self.spectral_source / (z - self.eigenvalues)[:, None]
        )

    def certified_evaluate(self, z: complex) -> ReturnCertificate:
        distance = abs(complex(z).imag)
        if distance == 0:
            raise ValueError("resolvent certificate requires an off-axis query")
        spectral_coefficients = (
            self.spectral_source / (z - self.eigenvalues)[:, None]
        )
        coefficients = np.vstack((
            np.eye(self.problem.source.shape[1]),
            self._projected_coefficients(spectral_coefficients),
        ))
        residual_gram = coefficients.conj().T @ self.residual_gram @ coefficients
        residual_bound = math.sqrt(max(
            0.0,
            float(np.linalg.eigvalsh(
                (residual_gram + residual_gram.conj().T) / 2.0,
            )[-1].real),
        ))
        return ReturnCertificate(
            self.evaluate(z),
            residual_bound,
            self.source_norm * residual_bound / distance,
        )

    def _projected_coefficients(self, spectral_coefficients: np.ndarray) -> np.ndarray:
        return self.eigenvectors @ spectral_coefficients

    def moment_residuals(self, count: int) -> tuple[float, ...]:
        if count < 1:
            raise ValueError("moment count must be positive")
        full_power = self.problem.source.copy()
        reduced_power = self.projected_source.copy()
        residuals = []
        for _ in range(count):
            full = self.problem.inner(self.problem.source, full_power)
            reduced = self.projected_source.conj().T @ reduced_power
            residuals.append(float(np.linalg.norm(full - reduced)))
            full_power = self.problem.apply_generator(full_power)
            reduced_power = self.projected_generator @ reduced_power
        return tuple(residuals)


@dataclass(frozen=True)
class CyclicReturnCompilation:
    model: CyclicReturnModel | None = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def _as_source(source) -> np.ndarray:
    values = np.asarray(source, dtype=complex)
    if values.ndim == 1:
        values = values[:, None]
    if values.ndim != 2 or not values.shape[1]:
        raise ValueError("return source must be a nonempty matrix")
    return values


def _refuse(problem: ReturnProblem, reason: str) -> CyclicReturnCompilation:
    return CyclicReturnCompilation(
        refusal=Refusal(reason, provenance=problem.provenance),
    )


def _metric_basis(
    raw: np.ndarray,
    weighted_raw: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray]:
    norms = np.sqrt(np.maximum(
        0.0,
        np.real(np.sum(raw.conj() * weighted_raw, axis=0)),
    ))
    reference = max(1.0, float(norms.max()))
    basis: list[np.ndarray] = []
    weighted_basis: list[np.ndarray] = []
    for column in range(raw.shape[1]):
        vector = raw[:, column].copy()
        weighted = weighted_raw[:, column].copy()
        for _ in range(2):
            if basis:
                frame = np.column_stack(basis)
                weighted_frame = np.column_stack(weighted_basis)
                coefficients = frame.conj().T @ weighted
                vector -= frame @ coefficients
                weighted -= weighted_frame @ coefficients
        norm_squared = float(np.vdot(vector, weighted).real)
        if norm_squared < -(tolerance * reference) ** 2:
            raise ValueError("return metric is not positive")
        norm = math.sqrt(max(0.0, norm_squared))
        if norm > tolerance * reference:
            basis.append(vector / norm)
            weighted_basis.append(weighted / norm)
    if not basis:
        raise ValueError("return source has zero metric norm")
    return np.column_stack(basis), np.column_stack(weighted_basis)


def compile_cyclic_return(
    problem: ReturnProblem,
    depth: int,
    resource_budget: int,
    rank_tolerance: float = 1e-12,
) -> CyclicReturnCompilation:
    if problem.hermitian_residual > rank_tolerance:
        return _refuse(problem, "return generator is not Hermitian")
    if depth < 1:
        return _refuse(problem, "cyclic depth must be positive")
    if rank_tolerance <= 0 or not math.isfinite(rank_tolerance):
        return _refuse(problem, "rank tolerance must be finite and positive")
    if not np.isfinite(problem.source).all() or not np.linalg.norm(problem.source):
        return _refuse(problem, "return source must be finite and nonzero")

    port_dimension = problem.source.shape[1]
    maximum_rank = min(problem.dimension, depth * port_dimension)
    maximum_generator_actions = (depth - 1) * port_dimension + maximum_rank
    maximum_metric_actions = depth * port_dimension + maximum_rank
    setup_bound = (
        problem.construction_cost
        + maximum_generator_actions * problem.action_cost_per_vector
        + maximum_metric_actions * problem.metric_cost_per_vector
        + 2 * problem.dimension * maximum_rank**2
        + maximum_rank**3
    )
    if setup_bound > resource_budget:
        return _refuse(problem, "cyclic return budget exceeded")

    blocks = [problem.source]
    for _ in range(1, depth):
        blocks.append(problem.apply_generator(blocks[-1]))
    raw = np.hstack(blocks)
    weighted_raw = problem.apply_metric(raw)
    try:
        basis, weighted_basis = _metric_basis(
            raw,
            weighted_raw,
            rank_tolerance,
        )
    except ValueError as error:
        return _refuse(problem, str(error))
    rank = basis.shape[1]
    generated = problem.apply_generator(basis)
    weighted_generated = problem.apply_metric(generated)
    projected = basis.conj().T @ weighted_generated
    projected = (projected + projected.conj().T) / 2.0
    metric_source = weighted_raw[:, :port_dimension]
    projected_source = basis.conj().T @ metric_source
    eigenvalues, eigenvectors = eigh(projected)
    spectral_source = eigenvectors.conj().T @ projected_source
    source_gram = problem.source.conj().T @ metric_source
    source_norm = math.sqrt(max(
        0.0,
        float(np.linalg.eigvalsh(
            (source_gram + source_gram.conj().T) / 2.0,
        )[-1].real),
    ))
    source_residual = problem.source - basis @ projected_source
    weighted_source_residual = metric_source - weighted_basis @ projected_source
    invariance_defect = generated - basis @ projected
    weighted_invariance_defect = weighted_generated - weighted_basis @ projected
    residual_vectors = np.hstack((source_residual, invariance_defect))
    weighted_residuals = np.hstack((
        weighted_source_residual,
        weighted_invariance_defect,
    ))
    residual_gram = residual_vectors.conj().T @ weighted_residuals
    residual_gram = (residual_gram + residual_gram.conj().T) / 2.0

    generator_actions = (depth - 1) * port_dimension + rank
    metric_operations = depth * port_dimension + rank
    setup_operations = (
        problem.construction_cost
        + generator_actions * problem.action_cost_per_vector
        + metric_operations * problem.metric_cost_per_vector
        + 2 * problem.dimension * rank**2
        + rank**3
    )
    reduced_query = rank * port_dimension**2
    certified_query = reduced_query + rank * port_dimension

    def break_even(query_cost):
        saving = problem.direct_query_cost - query_cost
        extra_setup = setup_operations - problem.baseline_setup_cost
        if saving <= 0:
            return None
        if extra_setup <= 0:
            return 1
        return math.floor(extra_setup / saving) + 1

    return CyclicReturnCompilation(CyclicReturnModel(
        problem,
        basis,
        projected,
        projected_source,
        eigenvalues,
        eigenvectors,
        spectral_source,
        source_norm,
        residual_gram,
        CyclicCost(
            generator_actions,
            metric_operations,
            setup_operations,
            problem.baseline_setup_cost,
            problem.direct_query_cost,
            reduced_query,
            break_even(reduced_query),
            certified_query,
            break_even(certified_query),
        ),
    ))


def pauli_fierz_problem(system: PauliFierzSystem) -> ReturnProblem:
    channels = system.channels
    retained = system.retained
    generator = system.hamiltonian[np.ix_(channels, channels)]
    source = system.hamiltonian[np.ix_(channels, retained)]
    return ReturnProblem.from_dense(
        generator,
        source,
        provenance=f"{system.request.provenance}: Q return",
    )


def anderson_thermal_problem(
    system: AndersonSystem,
    coupling: float,
) -> ReturnProblem:
    energies, vectors = eigh(system.hamiltonian(coupling))
    impurity = vectors.conj().T @ system.impurity_annihilator @ vectors
    shifted_weights = np.exp(
        -system.request.beta * (energies - energies[0]),
    )
    thermal_pair = (
        shifted_weights[:, None] + shifted_weights[None, :]
    ) / shifted_weights.sum()
    spectrum = energies[None, :] - energies[:, None]
    source = np.sqrt(thermal_pair) * impurity
    return ReturnProblem.from_diagonal(
        spectrum.ravel(),
        source.ravel()[:, None],
        provenance=f"{system.request.provenance}: thermal transition return",
        construction_cost=2 * system.free_hamiltonian.shape[0] ** 3,
        baseline_setup_cost=2 * system.free_hamiltonian.shape[0] ** 3,
    )


def anderson_state_metric_problem(
    system: AndersonSystem,
    coupling: float,
) -> ReturnProblem:
    hamiltonian = system.hamiltonian(coupling)
    hilbert_dimension = hamiltonian.shape[0]
    thermal = expm(-system.request.beta * hamiltonian)
    thermal = (thermal + thermal.conj().T) / 2.0
    density = thermal / np.trace(thermal)
    source = system.impurity_annihilator.reshape(-1, 1)

    def as_operators(values):
        return values.reshape(hilbert_dimension, hilbert_dimension, values.shape[1])

    def as_vectors(values):
        return values.reshape(hilbert_dimension**2, values.shape[2])

    def liouvillian(values):
        operators = as_operators(values)
        right = np.einsum("ijk,jl->ilk", operators, hamiltonian)
        left = np.einsum("ij,jlk->ilk", hamiltonian, operators)
        return as_vectors(right - left)

    def metric(values):
        operators = as_operators(values)
        left = np.einsum("ij,jlk->ilk", density, operators)
        right = np.einsum("ijk,jl->ilk", operators, density)
        return as_vectors(left + right)

    spectral_cache: dict[str, np.ndarray] = {}

    def evaluator(z):
        if not spectral_cache:
            energies, vectors = eigh(hamiltonian)
            impurity = vectors.conj().T @ system.impurity_annihilator @ vectors
            shifted = np.exp(-system.request.beta * (energies - energies[0]))
            spectral_cache["spectrum"] = (
                energies[None, :] - energies[:, None]
            ).ravel()
            spectral_cache["weights"] = (
                ((shifted[:, None] + shifted[None, :]) / shifted.sum())
                * abs(impurity) ** 2
            ).ravel()
        value = np.sum(
            spectral_cache["weights"] / (z - spectral_cache["spectrum"]),
        )
        return np.array([[value]], dtype=complex)

    stationarity = float(np.linalg.norm(
        density @ hamiltonian - hamiltonian @ density,
    ))
    hermitian_residual = (
        float(np.linalg.norm(hamiltonian - hamiltonian.conj().T))
        + float(np.linalg.norm(density - density.conj().T))
        + stationarity
    )
    nonzero_entries = int(np.count_nonzero(abs(hamiltonian) > 1e-14))
    return ReturnProblem(
        dimension=hilbert_dimension**2,
        source=source,
        apply_generator=liouvillian,
        apply_metric=metric,
        evaluate=evaluator,
        hermitian_residual=hermitian_residual,
        action_cost_per_vector=2 * nonzero_entries * hilbert_dimension,
        metric_cost_per_vector=2 * hilbert_dimension**3,
        construction_cost=hilbert_dimension**3,
        baseline_setup_cost=2 * hilbert_dimension**3,
        direct_query_cost=hilbert_dimension**2,
        provenance=f"{system.request.provenance}: native state-metric return",
    )

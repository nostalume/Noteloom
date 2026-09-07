"""Regulated Pauli--Fierz action and its shared bound/open return."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import math

import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq

from .rewrite import Refusal


@dataclass(frozen=True)
class PauliFierzRequest:
    primitive_dimension: int
    matter_levels: int
    photon_frequencies: tuple[float, ...]
    field_coefficients: tuple[float, ...]
    photon_cutoff: int
    coupling: float
    resolution: float
    provenance: str
    resource_budget: int


@dataclass(frozen=True)
class ActionReceipt:
    expansion_residual: float
    linear_norm: float
    contact_norm: float


@dataclass(frozen=True)
class ReturnReceipt:
    residual: float
    direct_operations: int
    reduced_operations: int
    expert_operations: int
    advantage_over_expert: bool


@dataclass(frozen=True)
class SecondOrderReceipt:
    total_residual: float
    open_sector_residual: float
    contact_norm: float
    zero_photon_norm: float
    two_photon_norm: float


@dataclass(frozen=True)
class BoundReceipt:
    full_energy: float
    reduced_pole: float
    residual: float
    return_id: str


@dataclass(frozen=True)
class OpenReceipt:
    full_value: complex
    reduced_value: complex
    residual: float
    return_id: str


@dataclass(frozen=True)
class PauliFierzCompilation:
    system: "PauliFierzSystem | None" = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def _annihilator(dimension: int) -> np.ndarray:
    action = np.zeros((dimension, dimension), dtype=complex)
    for number in range(1, dimension):
        action[number - 1, number] = math.sqrt(number)
    return action


def _field_basis(mode_count: int, cutoff: int) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted(
        (
            state for state in product(range(cutoff + 1), repeat=mode_count)
            if sum(state) <= cutoff
        ),
        key=lambda state: (sum(state), state),
    ))


def _field_annihilator(
    basis: tuple[tuple[int, ...], ...],
    mode: int,
) -> np.ndarray:
    rows = {state: index for index, state in enumerate(basis)}
    action = np.zeros((len(basis), len(basis)), dtype=complex)
    for column, state in enumerate(basis):
        if state[mode]:
            target = list(state)
            target[mode] -= 1
            action[rows[tuple(target)], column] = math.sqrt(state[mode])
    return action


class PauliFierzSystem:
    def __init__(
        self,
        request: PauliFierzRequest,
        matter_energies: np.ndarray,
        trk_defect: float,
        field_basis: tuple[tuple[int, ...], ...],
        h0: np.ndarray,
        linear: np.ndarray,
        contact: np.ndarray,
        hamiltonian: np.ndarray,
        action_residual: float,
        retained: tuple[int, ...],
    ):
        self.request = request
        self.matter_energies = matter_energies
        self.trk_defect = trk_defect
        self.field_basis = field_basis
        self.h0 = h0
        self.linear = linear
        self.contact = contact
        self.hamiltonian = hamiltonian
        self.action_residual = action_residual
        self.retained = retained
        self.channels = tuple(
            index for index in range(hamiltonian.shape[0]) if index not in retained
        )
        self.return_id = (
            f"pf:{request.matter_levels}:{len(request.photon_frequencies)}:"
            f"{request.photon_cutoff}:{request.coupling}"
        )

    @property
    def matter_ground_energy(self) -> float:
        return float(self.matter_energies[0])

    def action_receipt(self) -> ActionReceipt:
        return ActionReceipt(
            self.action_residual,
            float(np.linalg.norm(self.linear)),
            float(np.linalg.norm(self.contact)),
        )

    def _blocks(self, operator: np.ndarray):
        pp = operator[np.ix_(self.retained, self.retained)]
        pq = operator[np.ix_(self.retained, self.channels)]
        qp = operator[np.ix_(self.channels, self.retained)]
        qq = operator[np.ix_(self.channels, self.channels)]
        return pp, pq, qp, qq

    def _effective_return(self, z: complex):
        pp, pq, qp, qq = self._blocks(self.hamiltonian)
        q_resolvent = np.linalg.solve(z * np.eye(len(self.channels)) - qq, np.eye(len(self.channels)))
        effective = pp + pq @ q_resolvent @ qp
        reduced = np.linalg.solve(
            z * np.eye(len(self.retained)) - effective,
            np.eye(len(self.retained)),
        )
        return effective, reduced

    def _return(self, z: complex):
        effective, reduced = self._effective_return(z)
        full = np.linalg.solve(
            z * np.eye(self.hamiltonian.shape[0]) - self.hamiltonian,
            np.eye(self.hamiltonian.shape[0]),
        )[np.ix_(self.retained, self.retained)]
        return effective, reduced, full

    def return_receipt(self, z: complex) -> ReturnReceipt:
        _, reduced, full = self._return(z)
        full_dimension = self.hamiltonian.shape[0]
        retained_dimension = len(self.retained)
        channel_dimension = len(self.channels)
        reduced_cost = channel_dimension**3 + retained_dimension**3
        return ReturnReceipt(
            residual=float(np.linalg.norm(full - reduced)),
            direct_operations=full_dimension**3,
            reduced_operations=reduced_cost,
            expert_operations=reduced_cost,
            advantage_over_expert=False,
        )

    def second_order_receipt(self, z: complex) -> SecondOrderReceipt:
        contact, _, _, _ = self._blocks(self.contact)
        _, p_to_q, q_to_p, _ = self._blocks(self.linear)
        energies = np.diag(self.h0)[list(self.channels)]
        direct = p_to_q @ np.diag(1.0 / (z - energies)) @ q_to_p
        sectors = {number: np.zeros_like(direct) for number in range(3)}
        field_dimension = len(self.field_basis)
        for position, full_index in enumerate(self.channels):
            photon_number = sum(self.field_basis[full_index % field_dimension])
            if photon_number <= 2:
                sectors[photon_number] += (
                    np.outer(p_to_q[:, position], q_to_p[position, :])
                    / (z - energies[position])
                )
        recovered = sum(sectors.values(), np.zeros_like(direct))
        open_slice = np.s_[1:, 1:]
        return SecondOrderReceipt(
            total_residual=float(np.linalg.norm(direct - recovered)),
            open_sector_residual=float(np.linalg.norm(
                (contact + direct)[open_slice]
                - (contact + sectors[0] + sectors[2])[open_slice]
            )),
            contact_norm=float(np.linalg.norm(contact[open_slice])),
            zero_photon_norm=float(np.linalg.norm(sectors[0][open_slice])),
            two_photon_norm=float(np.linalg.norm(sectors[2][open_slice])),
        )

    def bound_receipt(self) -> BoundReceipt:
        full_energy = float(eigh(self.hamiltonian, eigvals_only=True)[0])
        _, _, _, qq = self._blocks(self.hamiltonian)
        upper = min(
            self.matter_ground_energy + 0.5,
            float(eigh(qq, eigvals_only=True)[0]) - 1e-8,
        )
        lower = self.matter_ground_energy - 0.5

        def determinant(energy):
            effective, _ = self._effective_return(energy)
            return float(np.linalg.det(
                energy * np.eye(len(self.retained)) - effective,
            ).real)

        grid = np.linspace(lower, upper, 257)
        bracket = next(
            (pair for pair in zip(grid, grid[1:]) if determinant(pair[0]) * determinant(pair[1]) <= 0),
            None,
        )
        if bracket is None:
            raise ValueError("bound pole is not bracketed")
        pole = float(brentq(determinant, *bracket, xtol=1e-13))
        return BoundReceipt(full_energy, pole, abs(full_energy - pole), self.return_id)

    def open_receipt(self, energy: float, incoming, outgoing) -> OpenReceipt:
        incoming = np.asarray(incoming, dtype=complex)
        outgoing = np.asarray(outgoing, dtype=complex)
        mode_count = len(self.request.photon_frequencies)
        if incoming.shape != (mode_count,) or outgoing.shape != (mode_count,):
            raise ValueError("open wave packet has the wrong mode dimension")
        _, reduced, full = self._return(energy + 1j * self.request.resolution)
        source = np.concatenate(([0j], incoming))
        detector = np.concatenate(([0j], outgoing))
        full_value = complex(detector.conj() @ full @ source)
        reduced_value = complex(detector.conj() @ reduced @ source)
        return OpenReceipt(
            full_value,
            reduced_value,
            abs(full_value - reduced_value),
            self.return_id,
        )


def _refuse(request: PauliFierzRequest, reason: str) -> PauliFierzCompilation:
    return PauliFierzCompilation(refusal=Refusal(reason, provenance=request.provenance))


def compile_pauli_fierz(request: PauliFierzRequest) -> PauliFierzCompilation:
    if request.matter_levels > request.primitive_dimension:
        return _refuse(request, "matter level count exceeds primitive basis")
    if request.matter_levels < 2 or request.primitive_dimension < 4:
        return _refuse(request, "matter basis is underresolved")
    if request.photon_cutoff < 2:
        return _refuse(request, "photon cutoff omits order-two sectors")
    if len(request.photon_frequencies) != len(request.field_coefficients):
        return _refuse(request, "field data have different lengths")
    if not request.photon_frequencies:
        return _refuse(request, "field has no modes")
    if any(frequency <= 0 or not math.isfinite(frequency) for frequency in request.photon_frequencies):
        return _refuse(request, "photon frequencies must be finite and positive")
    if any(not math.isfinite(value) for value in (*request.field_coefficients, request.coupling)):
        return _refuse(request, "couplings must be finite")
    if request.resolution <= 0 or not math.isfinite(request.resolution):
        return _refuse(request, "resolution must be positive")

    field_basis = _field_basis(len(request.photon_frequencies), request.photon_cutoff)
    dimension = request.matter_levels * len(field_basis)
    primitive_dimension = request.primitive_dimension * len(field_basis)
    work = dimension**3 + primitive_dimension**2
    if work > request.resource_budget:
        return _refuse(request, "Pauli-Fierz compilation budget exceeded")

    lowering = _annihilator(request.primitive_dimension)
    position = (lowering + lowering.conj().T) / math.sqrt(2.0)
    momentum = 1j * (lowering.conj().T - lowering) / math.sqrt(2.0)
    potential = position @ position / 2.0 + np.linalg.matrix_power(position, 4) / 20.0
    matter_hamiltonian = momentum @ momentum / 2.0 + potential
    matter_energies, matter_vectors = eigh(matter_hamiltonian)
    projection = matter_vectors[:, :request.matter_levels]
    projected_position = projection.conj().T @ position @ projection
    projected_momentum = projection.conj().T @ momentum @ projection
    trk_sum = sum(
        (matter_energies[index] - matter_energies[0])
        * abs(projected_position[0, index]) ** 2
        for index in range(1, request.matter_levels)
    )
    trk_defect = abs(1.0 - 2.0 * trk_sum)

    field_actions = tuple(
        _field_annihilator(field_basis, mode)
        for mode in range(len(request.photon_frequencies))
    )
    field_hamiltonian = sum(
        (
            frequency * action.conj().T @ action
            for frequency, action in zip(
                request.photon_frequencies, field_actions, strict=True,
            )
        ),
        np.zeros((len(field_basis), len(field_basis)), dtype=complex),
    )
    field_port = sum(
        (
            coefficient * (action + action.conj().T)
            for coefficient, action in zip(
                request.field_coefficients, field_actions, strict=True,
            )
        ),
        np.zeros_like(field_hamiltonian),
    )
    matter_identity = np.eye(request.matter_levels)
    field_identity = np.eye(len(field_basis))
    h0 = (
        np.kron(np.diag(matter_energies[:request.matter_levels]), field_identity)
        + np.kron(matter_identity, field_hamiltonian)
    )
    linear = -np.kron(projected_momentum, field_port)
    contact = np.kron(matter_identity, field_port @ field_port) / 2.0
    hamiltonian = h0 + request.coupling * linear + request.coupling**2 * contact

    primitive_identity = np.eye(request.primitive_dimension)
    kinetic = (
        np.kron(momentum, field_identity)
        - request.coupling * np.kron(primitive_identity, field_port)
    )
    primitive_hamiltonian = (
        kinetic @ kinetic / 2.0
        + np.kron(potential, field_identity)
        + np.kron(primitive_identity, field_hamiltonian)
    )
    product_projection = np.kron(projection, field_identity)
    direct = product_projection.conj().T @ primitive_hamiltonian @ product_projection
    action_residual = float(np.linalg.norm(direct - hamiltonian))

    vacuum = field_basis.index((0,) * len(request.photon_frequencies))
    one_photon = tuple(
        field_basis.index(tuple(1 if index == mode else 0 for index in range(len(field_actions))))
        for mode in range(len(field_actions))
    )
    retained = (vacuum, *one_photon)
    return PauliFierzCompilation(PauliFierzSystem(
        request,
        matter_energies[:request.matter_levels],
        float(trk_defect),
        field_basis,
        h0,
        linear,
        contact,
        hamiltonian,
        action_residual,
        retained,
    ))

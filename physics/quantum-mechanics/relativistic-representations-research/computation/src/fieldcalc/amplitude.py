"""Construct scalar-QED amplitudes that descend through endpoint kernels."""

from dataclasses import dataclass
from math import comb

from sympy import ImmutableMatrix, diag, pi, simplify, sympify

from .rewrite import Refusal
from .worldline import compile_open_line_quotient, evaluate_scalar_line_amplitude


@dataclass(frozen=True)
class WardDescentCertificate:
    photon: int
    contraction: object
    ideal_coefficients: tuple[object, object]
    reconstructed: object
    residual: object


@dataclass(frozen=True)
class CharacteristicAmplitudeCost:
    ordered_histories: int = 0
    history_event_terms: int = 0
    amplitude_transition_terms: int = 0
    ward_transition_terms: int = 0

    @property
    def complete_transition_terms(self) -> int:
        return self.amplitude_transition_terms + self.ward_transition_terms

    @property
    def use_advantage(self) -> bool:
        return self.amplitude_transition_terms < self.history_event_terms

    @property
    def complete_advantage(self) -> bool:
        return self.complete_transition_terms < self.history_event_terms


@dataclass(frozen=True)
class CharacteristicScalarAmplitude:
    value: object | None = None
    endpoint_generators: tuple[object, object] = (0, 0)
    photon_generators: tuple[object, ...] = ()
    transversality_residuals: tuple[object, ...] = ()
    ward_certificates: tuple[WardDescentCertificate, ...] = ()
    state_bound: int = 0
    states_visited: int = 0
    certificate_states_visited: int = 0
    cost: CharacteristicAmplitudeCost | None = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


@dataclass(frozen=True)
class ScalarComptonKinematics:
    metric: object | None = None
    initial_momentum: object | None = None
    photon_momenta: tuple[object, object] = (None, None)
    polarizations: tuple[object, object] = (None, None)
    parameter: object | None = None
    mass_squared: object | None = None
    outgoing_energy: object | None = None
    phase_space_density: object | None = None
    shell_residual: object | None = None
    phase_space_residual: object | None = None
    polarization_norm_residuals: tuple[object, object] = (None, None)
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def compile_scalar_compton_kinematics(
    mass, incoming_energy, parameter,
) -> ScalarComptonKinematics:
    """Generate a 2+1 lab-frame shell family and its reflection-quotient density."""
    mass = sympify(mass)
    incoming_energy = sympify(incoming_energy)
    provenance = "2+1 scalar Compton shell"
    if mass.is_positive is not True or incoming_energy.is_positive is not True:
        return ScalarComptonKinematics(refusal=Refusal(
            "mass and incoming energy must be provably positive",
            residual=(mass, incoming_energy), provenance=provenance,
        ))
    if not (getattr(parameter, "is_Symbol", False) and parameter.is_real is True):
        return ScalarComptonKinematics(refusal=Refusal(
            "Compton parameter must be one real symbol", provenance=provenance,
        ))

    t = parameter
    cosine = (1 - t**2) / (1 + t**2)
    sine = 2 * t / (1 + t**2)
    denominator = simplify(mass + incoming_energy * (1 - cosine))
    outgoing_energy = simplify(mass * incoming_energy / denominator)
    metric = diag(-1, 1, 1)
    initial = ImmutableMatrix([mass, 0, 0])
    momenta = (
        ImmutableMatrix([incoming_energy, incoming_energy, 0]),
        -outgoing_energy * ImmutableMatrix([1, cosine, sine]),
    )
    polarizations = (ImmutableMatrix([0, 0, 1]), ImmutableMatrix([0, sine, -cosine]))

    def dot(left, right):
        return (left.T * metric * right)[0]

    final = initial + momenta[0] + momenta[1]
    shell_residual = simplify(mass**2 + dot(final, final))
    norm_residuals = tuple(
        simplify(dot(vector, vector) - 1) for vector in polarizations
    )
    angular_density = 1 / (8 * pi * denominator)
    transformed_density = simplify(2 * angular_density * 2 / (1 + t**2))
    phase_density = 1 / (2 * pi * (mass + (mass + 2 * incoming_energy) * t**2))
    return ScalarComptonKinematics(
        metric, initial, momenta, polarizations, t, mass**2, outgoing_energy,
        phase_density, shell_residual, simplify(transformed_density - phase_density),
        norm_residuals,
    )


def compile_characteristic_amplitude_cost(photon_count: int) -> CharacteristicAmplitudeCost:
    """Count direct histories and the subset route including Ward certificates."""
    quotient = compile_open_line_quotient(photon_count)

    def transitions(count):
        return sum(
            comb(count, size) * (size + comb(size, 2))
            for size in range(1, count + 1)
        )

    amplitude = transitions(photon_count)
    ward = photon_count * (amplitude + 2 * transitions(photon_count - 1))
    return CharacteristicAmplitudeCost(
        ordered_histories=quotient.ordered_histories,
        history_event_terms=sum(
            cell.ordered_histories * (photon_count - cell.pair_count)
            for cell in quotient.cells
        ),
        amplitude_transition_terms=amplitude,
        ward_transition_terms=ward,
    )


def compile_characteristic_scalar_amplitude(
    metric,
    initial_momentum,
    photon_momenta,
    polarizations,
    mass_squared,
    *,
    state_budget: int,
) -> CharacteristicScalarAmplitude:
    """Amputate both endpoints and exhibit every Ward image in their ideal."""
    metric = ImmutableMatrix(metric)
    initial_momentum = ImmutableMatrix(initial_momentum)
    photon_momenta = tuple(ImmutableMatrix(item) for item in photon_momenta)
    polarizations = tuple(ImmutableMatrix(item) for item in polarizations)
    mass_squared = sympify(mass_squared)
    photon_count = len(photon_momenta)
    state_bound = 2**photon_count
    cost = compile_characteristic_amplitude_cost(photon_count)
    if photon_count == 0:
        return CharacteristicScalarAmplitude(
            state_bound=state_bound,
            cost=cost,
            refusal=Refusal(
                "characteristic amplitude requires at least one insertion",
                provenance="scalar-QED characteristic quotient",
            ),
        )

    main = evaluate_scalar_line_amplitude(
        metric,
        initial_momentum,
        photon_momenta,
        polarizations,
        mass_squared,
        state_budget=state_budget,
        amputate_initial=True,
        amputate_final=True,
    )
    if not main.accepted:
        reason = main.refusal.reason
        if reason == "scalar line crosses characteristic denominator":
            reason = "amputated scalar line crosses an internal characteristic"
        elif reason == "scalar-line state budget exceeded":
            reason = "characteristic-amplitude state budget exceeded"
        return CharacteristicScalarAmplitude(
            state_bound=main.state_bound,
            cost=cost,
            refusal=Refusal(
                reason,
                residual=main.refusal.residual,
                provenance="scalar-QED characteristic quotient",
            ),
        )

    def dot(left, right):
        return (left.T * metric * right)[0]

    final_momentum = initial_momentum
    for momentum in photon_momenta:
        final_momentum += momentum
    endpoint_generators = (
        mass_squared + dot(initial_momentum, initial_momentum),
        mass_squared + dot(final_momentum, final_momentum),
    )
    photon_generators = tuple(dot(momentum, momentum) for momentum in photon_momenta)
    transversality = tuple(
        dot(momentum, vector)
        for momentum, vector in zip(photon_momenta, polarizations)
    )

    certificates = []
    certificate_states = 0
    for photon in range(photon_count):
        contracted_vectors = list(polarizations)
        contracted_vectors[photon] = photon_momenta[photon]
        contraction = evaluate_scalar_line_amplitude(
            metric,
            initial_momentum,
            photon_momenta,
            tuple(contracted_vectors),
            mass_squared,
            state_budget=state_budget,
            amputate_initial=True,
            amputate_final=True,
        )
        remaining_momenta = tuple(
            momentum for index, momentum in enumerate(photon_momenta)
            if index != photon
        )
        remaining_vectors = tuple(
            vector for index, vector in enumerate(polarizations)
            if index != photon
        )
        initial_side = evaluate_scalar_line_amplitude(
            metric,
            initial_momentum,
            remaining_momenta,
            remaining_vectors,
            mass_squared,
            state_budget=state_budget,
            amputate_initial=True,
        )
        final_side = evaluate_scalar_line_amplitude(
            metric,
            final_momentum,
            tuple(-momentum for momentum in remaining_momenta),
            remaining_vectors,
            mass_squared,
            state_budget=state_budget,
            amputate_initial=True,
        )
        evaluations = (contraction, initial_side, final_side)
        failed = next((item for item in evaluations if not item.accepted), None)
        if failed is not None:
            return CharacteristicScalarAmplitude(
                value=main.value,
                endpoint_generators=endpoint_generators,
                photon_generators=photon_generators,
                transversality_residuals=transversality,
                state_bound=state_bound,
                states_visited=main.states_visited,
                cost=cost,
                refusal=failed.refusal,
            )

        coefficients = (-final_side.value, initial_side.value)
        reconstructed = sum(
            generator * coefficient
            for generator, coefficient in zip(endpoint_generators, coefficients)
        )
        certificates.append(WardDescentCertificate(
            photon=photon,
            contraction=contraction.value,
            ideal_coefficients=coefficients,
            reconstructed=reconstructed,
            residual=simplify(contraction.value - reconstructed),
        ))
        certificate_states += sum(item.states_visited for item in evaluations)

    return CharacteristicScalarAmplitude(
        value=main.value,
        endpoint_generators=endpoint_generators,
        photon_generators=photon_generators,
        transversality_residuals=transversality,
        ward_certificates=tuple(certificates),
        state_bound=state_bound,
        states_visited=main.states_visited,
        certificate_states_visited=certificate_states,
        cost=cost,
    )

"""Consume exterior fermion lines in one resolved three-photon event."""

from dataclasses import dataclass

from sympy import (
    ImmutableMatrix, Rational, diff, factor, oo, pi, simplify, sympify,
)

from .clifford import clifford_scalar, clifford_vector
from .exterior import (
    ExteriorOperator, compile_exterior_normal_form, exterior_product,
)
from .fermion_line import compile_fermion_line_amplitude
from .measures import PreparedEventEffect
from .rewrite import Refusal

@dataclass(frozen=True)
class ResolvedThreePhotonSlice:
    metric: ImmutableMatrix | None = None
    initial_momentum: ImmutableMatrix | None = None
    photon_momenta: tuple[ImmutableMatrix, ...] = ()
    polarizations: tuple[ImmutableMatrix, ...] = ()
    final_momentum: ImmutableMatrix | None = None
    mass_squared: object | None = None
    parameter: object | None = None
    resolution: object | None = None
    first_energy: object | None = None
    second_energy: object | None = None
    exchange_map: object | None = None
    phase_space_density: object | None = None
    shell_residuals: tuple[object, ...] = ()
    transversality_residuals: tuple[object, ...] = ()
    resolution_residuals: tuple[object, ...] = ()
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None

@dataclass(frozen=True)
class FermionThreePhotonEvent:
    amplitude: ExteriorOperator | None = None
    effect: PreparedEventEffect | None = None
    route: str | None = None
    normal_form_terms: int = 0
    amplitude_updates: int = 0
    effect_updates: int = 0
    ward_updates: int = 0
    total_updates: int = 0
    ward_residuals: tuple[object, ...] = ()
    exchange_residual: object | None = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None

def compile_resolved_three_photon_slice(
    parameter,
    *,
    resolution,
    mass=1,
    incoming_energy=1,
) -> ResolvedThreePhotonSlice:
    """Generate a soft-excluded nonlinear-Compton slice from the final shell."""
    provenance = "resolved three-photon nonlinear-Compton slice"
    parameter = sympify(parameter)
    resolution = sympify(resolution)
    mass = sympify(mass)
    incoming_energy = sympify(incoming_energy)

    def refuse(reason, residual=()):
        return ResolvedThreePhotonSlice(
            parameter=parameter,
            resolution=resolution,
            refusal=Refusal(reason, residual=tuple(residual), provenance=provenance),
        )

    if getattr(parameter, "is_Symbol", False) is not True \
            or parameter.is_positive is not True:
        return refuse("slice parameter must be one positive symbol")
    if mass.is_positive is not True or incoming_energy.is_positive is not True:
        return refuse("mass and incoming energy must be provably positive")
    if resolution.is_positive is not True:
        return refuse("detector resolution must exclude both soft boundaries")

    energy_sum = simplify(mass + incoming_energy)
    denominator = simplify(energy_sum - 2 * resolution)
    if denominator == 0:
        return refuse("detector resolution leaves no generated energy interval")
    upper = simplify(
        (mass * incoming_energy - resolution * energy_sum) / denominator
    )
    span = simplify(upper - resolution)
    if span.is_positive is not True:
        return refuse(
            "detector resolution leaves no generated energy interval", (span,)
        )

    first_energy = simplify(resolution + span * parameter / (1 + parameter))
    second_energy = simplify(
        (mass * incoming_energy - energy_sum * first_energy)
        / (energy_sum - 2 * first_energy)
    )
    exchange_map = simplify(
        (energy_sum - 2 * resolution) ** 2
        / ((energy_sum**2 - 2 * mass * incoming_energy) * parameter)
    )
    metric = ImmutableMatrix.diag(-1, 1, 1)
    initial = ImmutableMatrix((mass, 0, 0))
    photon_momenta = (
        ImmutableMatrix((incoming_energy, incoming_energy, 0)),
        ImmutableMatrix((-first_energy, 0, -first_energy)),
        ImmutableMatrix((-second_energy, 0, second_energy)),
    )
    polarizations = (
        ImmutableMatrix((0, 0, 1)),
        ImmutableMatrix((0, -1, 0)),
        ImmutableMatrix((0, 1, 0)),
    )
    final = initial + sum(
        photon_momenta, ImmutableMatrix.zeros(metric.rows, 1)
    )

    def dot(left, right):
        return (left.T * metric * right)[0]

    shell = tuple(simplify(item) for item in (
        mass**2 + dot(initial, initial),
        mass**2 + dot(final, final),
        *(dot(momentum, momentum) for momentum in photon_momenta),
    ))
    transverse = tuple(simplify(dot(momentum, vector)) for momentum, vector in zip(
        photon_momenta, polarizations
    ))
    resolution_checks = (
        simplify(first_energy.subs(parameter, 0) - resolution),
        simplify(second_energy.limit(parameter, oo) - resolution),
        simplify(first_energy.subs(parameter, exchange_map) - second_energy),
        simplify(second_energy.subs(parameter, exchange_map) - first_energy),
        simplify(exchange_map.subs(parameter, exchange_map) - parameter),
    )
    phase_density = factor(simplify(
        diff(first_energy, parameter)
        / (64 * pi**3 * (energy_sum - 2 * first_energy))
    ))
    residuals = shell + transverse + resolution_checks
    if any(item != 0 for item in residuals):
        return refuse("generated slice fails its shell or detector boundary", residuals)
    final_energy = factor(final[0])
    if final_energy.is_positive is not True \
            or phase_density.is_nonnegative is not True:
        return refuse(
            "generated slice has no certified positive phase density",
            (final_energy, phase_density),
        )
    return ResolvedThreePhotonSlice(
        metric=metric,
        initial_momentum=initial,
        photon_momenta=photon_momenta,
        polarizations=polarizations,
        final_momentum=final,
        mass_squared=mass**2,
        parameter=parameter,
        resolution=resolution,
        first_energy=first_energy,
        second_energy=second_energy,
        exchange_map=exchange_map,
        phase_space_density=phase_density,
        shell_residuals=shell,
        transversality_residuals=transverse,
        resolution_residuals=resolution_checks,
    )


def compile_fermion_three_photon_event(
    kinematics,
    *,
    state_budget: int,
    route: str = "subset grade",
    parity_doubled: bool = True,
) -> FermionThreePhotonEvent:
    """Project a three-photon line to a positive parity-even detector effect."""
    provenance = "resolved parity-even three-photon fermion event"

    def refuse(reason, residual=()):
        return FermionThreePhotonEvent(
            route=route,
            refusal=Refusal(reason, residual=tuple(residual), provenance=provenance),
        )

    if not kinematics.accepted:
        return refuse("three-photon kinematics is unavailable")
    if not parity_doubled:
        return refuse("single-parity odd Clifford trace is not generated")
    if any(value != 0 for value in (
        kinematics.shell_residuals + kinematics.transversality_residuals
    )):
        return refuse("three-photon preparation is not physical")

    amplitude = compile_fermion_line_amplitude(
        kinematics.metric,
        kinematics.initial_momentum,
        kinematics.photon_momenta,
        kinematics.polarizations,
        kinematics.mass_squared,
        state_budget=state_budget,
        route=route,
    )
    if not amplitude.accepted:
        return FermionThreePhotonEvent(route=route, refusal=amplitude.refusal)

    mass = sympify(kinematics.mass_squared) ** Rational(1, 2)
    initial_projector = Rational(1, 2) * (clifford_scalar(1)
        + (1 / mass) * clifford_vector(kinematics.initial_momentum))
    final_projector = Rational(1, 2) * (clifford_scalar(1)
        + (1 / mass) * clifford_vector(kinematics.final_momentum))
    normal_initial = compile_exterior_normal_form(
        initial_projector, kinematics.metric
    )
    normal_final = compile_exterior_normal_form(final_projector, kinematics.metric)
    failed = next(
        (item for item in (normal_initial, normal_final) if not item.accepted), None
    )
    if failed is not None:
        return FermionThreePhotonEvent(route=route, refusal=failed.refusal)

    first = exterior_product(normal_final.operator, amplitude.amplitude)
    second = exterior_product(first.operator, normal_initial.operator)
    third = exterior_product(second.operator, amplitude.amplitude.adjoint())
    effect_value = factor(simplify(2 * third.operator.scalar_part))
    effect_updates = (
        normal_initial.product_updates + normal_final.product_updates
        + first.product_updates + second.product_updates + third.product_updates
    )

    ward_residuals = []
    ward_updates = 0
    for label, momentum in enumerate(kinematics.photon_momenta):
        vectors = list(kinematics.polarizations)
        vectors[label] = momentum
        contracted = compile_fermion_line_amplitude(
            kinematics.metric,
            kinematics.initial_momentum,
            kinematics.photon_momenta,
            tuple(vectors),
            kinematics.mass_squared,
            state_budget=state_budget,
            route=route,
        )
        if not contracted.accepted:
            return FermionThreePhotonEvent(route=route, refusal=contracted.refusal)
        left = exterior_product(normal_final.operator, contracted.amplitude)
        projected = exterior_product(left.operator, normal_initial.operator)
        residual = projected.operator.terms
        ward_residuals.append(0 if not residual else residual)
        ward_updates += (
            contracted.total_updates + left.product_updates
            + projected.product_updates
        )

    if any(value != 0 for value in ward_residuals):
        return refuse("three-photon amplitude does not descend to the Ward quotient")
    if effect_value.is_nonnegative is not True:
        return refuse(
            "three-photon spin effect has no certified positive form", (effect_value,)
        )
    event_density = simplify(effect_value * kinematics.phase_space_density)
    exchange_jacobian = simplify(
        -diff(kinematics.exchange_map, kinematics.parameter)
    )
    exchange_residual = simplify(
        event_density
        - event_density.subs(
            kinematics.parameter, kinematics.exchange_map
        ) * exchange_jacobian
    )
    if exchange_residual != 0:
        return refuse(
            "outgoing-arm exchange does not preserve the detector measure",
            (exchange_residual,),
        )
    effect = PreparedEventEffect(
        value=effect_value,
        amplitude_value=amplitude.amplitude,
        detector_weight=1,
        gauge_residuals=tuple(ward_residuals),
    )
    return FermionThreePhotonEvent(
        amplitude=amplitude.amplitude,
        effect=effect,
        route=route,
        normal_form_terms=amplitude.amplitude.term_count,
        amplitude_updates=amplitude.total_updates,
        effect_updates=effect_updates,
        ward_updates=ward_updates,
        total_updates=amplitude.total_updates + effect_updates + ward_updates,
        ward_residuals=tuple(ward_residuals),
        exchange_residual=exchange_residual,
    )

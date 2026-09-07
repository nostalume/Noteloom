"""Generate leading-soft detector-bin transfer from one positive kernel."""

from __future__ import annotations

from dataclasses import dataclass

from sympy import limit, log, nan, oo, simplify, sympify, zoo

from .exterior import ExteriorOperator, exterior_product
from .rewrite import Refusal


@dataclass(frozen=True)
class LeadingSoftBinTransfer:
    generated_power_residues: tuple[object, ...] = ()
    factorization_residuals: tuple[object, ...] = ()
    virtual_correction: object | None = None
    unresolved_correction: object | None = None
    resolved_correction: object | None = None
    lower_bin_correction: object | None = None
    no_jump_effect: object | None = None
    unmatched_real_log: object | None = None
    transfer_residual: object | None = None
    normalization_residual: object | None = None
    distinct_kernel_count: int = 0
    singularly_complete: bool = False
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


@dataclass(frozen=True)
class SoftEffectJet:
    amplitude_pole: ExteriorOperator | None = None
    amplitude_finite: ExteriorOperator | None = None
    effect_power_residue: object | None = None
    effect_projector_tangent: object | None = None
    effect_interference_tangent: object | None = None
    density_power_residue: object | None = None
    phase_tangent_contribution: object | None = None
    response_tangent_contribution: object | None = None
    density_log_residue: object | None = None
    certificate_residuals: tuple[object, object] = ()
    product_updates: int = 0
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def compile_soft_effect_jet(
    *,
    parameter,
    amplitude,
    initial_projector,
    final_projector,
    phase_density,
) -> SoftEffectJet:
    """Generate the first two density poles from exterior-operator jets.

    The amplitude is assumed to have at most a simple pole at the positive soft
    parameter's zero boundary. A direct density limit is retained only as a
    certificate for the generated jet convolution.
    """
    provenance = "exterior soft-effect jet"
    parameter = sympify(parameter)
    phase_density = sympify(phase_density)

    def refuse(reason, residual=()):
        return SoftEffectJet(refusal=Refusal(
            reason,
            residual=tuple(residual),
            provenance=provenance,
        ))

    if getattr(parameter, "is_Symbol", False) is not True \
            or parameter.is_positive is not True:
        return refuse("soft parameter must be one positive symbol")
    operators = (amplitude, initial_projector, final_projector)
    if any(not isinstance(item, ExteriorOperator) for item in operators):
        return refuse("soft effect requires exterior-operator inputs")
    if len({item.diagonal for item in operators}) != 1:
        return refuse("soft effect inputs require one admitted exterior frame")

    def boundary(value):
        return simplify(limit(value, parameter, 0, dir="+"))

    def is_finite(value):
        return not value.has(oo, -oo, zoo, nan) and value.is_finite is not False

    def operator_jet(operator, pole_order):
        base_items = []
        tangent_items = []
        failures = []
        for mask, coefficient in operator.terms:
            regularized = simplify(parameter**pole_order * coefficient)
            base = boundary(regularized)
            tangent = boundary((regularized - base) / parameter)
            if not is_finite(base) or not is_finite(tangent):
                failures.append((mask, base, tangent))
                continue
            if base != 0:
                base_items.append((mask, base))
            if tangent != 0:
                tangent_items.append((mask, tangent))
        return (
            ExteriorOperator(tuple(base_items), operator.diagonal),
            ExteriorOperator(tuple(tangent_items), operator.diagonal),
            tuple(failures),
        )

    amplitude_pole, amplitude_finite, amplitude_failures = operator_jet(
        amplitude, 1
    )
    initial_base, initial_tangent, initial_failures = operator_jet(
        initial_projector, 0
    )
    final_base, final_tangent, final_failures = operator_jet(final_projector, 0)
    failures = amplitude_failures + initial_failures + final_failures
    if failures:
        return refuse("soft jet exceeds the admitted first-order boundary", failures)
    if not amplitude_pole.terms:
        return refuse("amplitude has no generated simple soft pole")

    phase_base = boundary(phase_density)
    phase_tangent = boundary((phase_density - phase_base) / parameter)
    if not is_finite(phase_base) or not is_finite(phase_tangent):
        return refuse(
            "phase density exceeds the admitted first-order boundary",
            (phase_base, phase_tangent),
        )

    def scalar_chain(*items):
        value = items[0]
        updates = 0
        for item in items[1:]:
            product = exterior_product(value, item)
            value = product.operator
            updates += product.product_updates
        return value.scalar_part, updates

    pole_adjoint = amplitude_pole.adjoint()
    finite_adjoint = amplitude_finite.adjoint()
    leading, leading_updates = scalar_chain(
        final_base, amplitude_pole, initial_base, pole_adjoint
    )
    final_shift, final_updates = scalar_chain(
        final_tangent, amplitude_pole, initial_base, pole_adjoint
    )
    initial_shift, initial_updates = scalar_chain(
        final_base, amplitude_pole, initial_tangent, pole_adjoint
    )
    left_interference, left_updates = scalar_chain(
        final_base, amplitude_finite, initial_base, pole_adjoint
    )
    right_interference, right_updates = scalar_chain(
        final_base, amplitude_pole, initial_base, finite_adjoint
    )
    effect_power = simplify(2 * leading)
    effect_projector_tangent = simplify(2 * (final_shift + initial_shift))
    effect_interference_tangent = simplify(
        2 * (left_interference + right_interference)
    )
    density_power = simplify(phase_base * effect_power)
    phase_contribution = simplify(phase_tangent * effect_power)
    response_contribution = simplify(
        phase_base * (effect_projector_tangent + effect_interference_tangent)
    )
    density_log = simplify(phase_contribution + response_contribution)

    direct_effect, direct_updates = scalar_chain(
        final_projector, amplitude, initial_projector, amplitude.adjoint()
    )
    direct_density = simplify(2 * phase_density * direct_effect)
    direct_power = boundary(parameter**2 * direct_density)
    direct_log = boundary(
        parameter * (direct_density - direct_power / parameter**2)
    )
    residuals = (
        simplify(density_power - direct_power),
        simplify(density_log - direct_log),
    )
    return SoftEffectJet(
        amplitude_pole=amplitude_pole,
        amplitude_finite=amplitude_finite,
        effect_power_residue=effect_power,
        effect_projector_tangent=effect_projector_tangent,
        effect_interference_tangent=effect_interference_tangent,
        density_power_residue=density_power,
        phase_tangent_contribution=phase_contribution,
        response_tangent_contribution=response_contribution,
        density_log_residue=density_log,
        certificate_residuals=residuals,
        product_updates=(
            leading_updates + final_updates + initial_updates + left_updates
            + right_updates + direct_updates
        ),
    )


def compile_leading_soft_bin_transfer(
    *,
    hard_density,
    photon_phase_coefficient,
    current_weights,
    observed_power_residues,
    observed_log_residues,
    infrared_scale,
    detector_resolution,
    soft_ceiling,
    coupling_squared=1,
) -> LeadingSoftBinTransfer:
    """Factor soft poles and generate virtual/unresolved/resolved bin weights.

    The virtual sign is the leading-soft unitarity contract. This constructor
    does not generate finite loop terms or subleading soft matching.
    """
    provenance = "leading-soft detector-bin transfer"
    hard = sympify(hard_density)
    phase = sympify(photon_phase_coefficient)
    weights = tuple(sympify(value) for value in current_weights)
    power = tuple(sympify(value) for value in observed_power_residues)
    logarithmic = tuple(sympify(value) for value in observed_log_residues)
    infrared = sympify(infrared_scale)
    resolution = sympify(detector_resolution)
    ceiling = sympify(soft_ceiling)
    coupling = sympify(coupling_squared)

    def refuse(reason, residual=()):
        return LeadingSoftBinTransfer(refusal=Refusal(
            reason,
            residual=tuple(residual),
            provenance=provenance,
        ))

    if not weights or len(weights) != len(power) or len(power) != len(logarithmic):
        return refuse("soft endpoint data must have one common nonempty arity")
    if hard.is_positive is not True or phase.is_positive is not True:
        return refuse("hard density and photon phase coefficient must be positive")
    if coupling.is_nonnegative is not True:
        return refuse("squared coupling must be nonnegative")
    if any(weight.is_nonnegative is not True for weight in weights):
        return refuse("eikonal current weights must be nonnegative")
    scale_checks = (
        infrared,
        resolution - infrared,
        ceiling - resolution,
    )
    if any(value.is_positive is not True for value in scale_checks):
        return refuse(
            "soft scales must satisfy 0 < infrared < resolution < ceiling",
            scale_checks,
        )

    generated = tuple(simplify(hard * phase * weight) for weight in weights)
    factorization = tuple(
        simplify(observed - expected)
        for observed, expected in zip(power, generated)
    )
    if any(value != 0 for value in factorization):
        return refuse(
            "observed soft pole does not factor through the hard event",
            factorization,
        )

    def intensity(left, right):
        return simplify(
            coupling
            * phase
            * sum(weights)
            * (1 / left - 1 / right)
        )

    total_intensity = intensity(infrared, ceiling)
    unresolved_intensity = intensity(infrared, resolution)
    resolved_intensity = intensity(resolution, ceiling)
    virtual = simplify(-hard * total_intensity)
    unresolved = simplify(hard * unresolved_intensity)
    resolved = simplify(hard * resolved_intensity)
    lower_bin = simplify(virtual + unresolved)
    no_jump = simplify(hard + virtual)
    if no_jump.is_nonnegative is not True:
        return refuse(
            "leading-soft no-jump weight leaves the perturbative regime",
            (no_jump,),
        )
    transfer_residual = simplify(virtual + unresolved + resolved)
    normalization_residual = simplify(no_jump + unresolved + resolved - hard)
    unmatched_log = simplify(
        coupling * sum(logarithmic) * log(resolution / infrared)
    )

    return LeadingSoftBinTransfer(
        generated_power_residues=generated,
        factorization_residuals=factorization,
        virtual_correction=virtual,
        unresolved_correction=unresolved,
        resolved_correction=resolved,
        lower_bin_correction=lower_bin,
        no_jump_effect=no_jump,
        unmatched_real_log=unmatched_log,
        transfer_residual=transfer_residual,
        normalization_residual=normalization_residual,
        distinct_kernel_count=len(set(generated)),
        singularly_complete=all(value == 0 for value in logarithmic),
    )

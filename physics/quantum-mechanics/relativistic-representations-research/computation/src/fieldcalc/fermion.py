"""Generate parity-even fermion-line effects from Clifford operations."""

from dataclasses import dataclass

from sympy import (
    Poly, Rational, cancel, expand, fraction, simplify, sqrt,
)

from .clifford import (
    CliffordOperator, CliffordTrace, clifford_scalar, clifford_trace,
    clifford_vector,
)
from .exterior import compile_exterior_normal_form, exterior_product
from .measures import PreparedEventEffect
from .rewrite import Refusal


@dataclass(frozen=True)
class FermionComptonCompilation:
    amplitude: CliffordOperator | None = None
    trace_value: object | None = None
    ward_residuals: tuple[object, object] = (None, None)
    projector_residuals: tuple[object, object] = (None, None)
    trace_terms: int = 0
    pairing_terms: int = 0
    recurrence_updates: int = 0
    pfaffian_update_bound: int = 0
    elimination_updates: int = 0
    pivot_conditions: tuple[object, ...] = ()
    trace_backend: str | None = None
    normal_form_terms: int = 0
    contraction_updates: int = 0
    ward_updates: int = 0
    total_updates: int = 0
    normal_form_residual: object | None = None
    effect: PreparedEventEffect | None = None
    positivity_square: object | None = None
    positivity_remainder: object | None = None
    positivity_residual: object | None = None
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def _positive_completion(value, parameter):
    numerator, denominator = fraction(cancel(value))
    polynomial = Poly(numerator, parameter)
    if polynomial.degree() < 0 or polynomial.degree() % 2:
        return None
    half_degree = polynomial.degree() // 2
    leading = sqrt(polynomial.LC())
    if leading.is_real is not True:
        return None
    square = leading * parameter**half_degree
    for degree in range(2 * half_degree - 1, half_degree - 1, -1):
        residual = Poly(expand(numerator - square**2), parameter)
        coefficient = residual.coeff_monomial(parameter**degree)
        square += simplify(coefficient / (2 * leading)) * parameter**(
            degree - half_degree
        )
    remainder = simplify(numerator - square**2)
    denominator = simplify(denominator)
    if remainder.is_positive is not True or denominator.is_positive is not True:
        return None
    witness = simplify((square**2 + remainder) / denominator)
    return simplify(square), remainder, witness, simplify(value - witness)


def compile_fermion_compton_effect(
    kinematics, *, parity_doubled: bool = True,
    trace_backend: str = "exterior grade",
) -> FermionComptonCompilation:
    """Construct a spin-averaged Compton effect without choosing gamma matrices."""
    provenance = "parity-even abstract-Clifford Compton transfer"
    if not kinematics.accepted:
        return FermionComptonCompilation(refusal=Refusal(
            "Compton kinematics is unavailable", provenance=provenance,
        ))
    if not parity_doubled:
        return FermionComptonCompilation(refusal=Refusal(
            "single-parity odd Clifford trace is not generated",
            provenance=provenance,
        ))
    if trace_backend not in ("exterior grade", "shared recurrence"):
        return FermionComptonCompilation(refusal=Refusal(
            "unknown Clifford trace backend", provenance=provenance,
        ))

    metric = kinematics.metric
    mass = sqrt(kinematics.mass_squared)
    initial = kinematics.initial_momentum
    first, second = kinematics.photon_momenta
    first_vector, second_vector = kinematics.polarizations
    final = initial + first + second

    def dot(left, right):
        return (left.T * metric * right)[0]

    def propagator(momentum):
        denominator = simplify(mass**2 + dot(momentum, momentum))
        if denominator == 0:
            return None
        numerator = clifford_vector(momentum) + mass * clifford_scalar(1)
        return (-1 / denominator) * numerator

    first_internal = propagator(initial + first)
    second_internal = propagator(initial + second)
    if first_internal is None or second_internal is None:
        return FermionComptonCompilation(refusal=Refusal(
            "fermion line crosses an internal characteristic", provenance=provenance,
        ))

    def ordered_amplitude(left, right):
        left_vertex = clifford_vector(left)
        right_vertex = clifford_vector(right)
        return (
            right_vertex * first_internal * left_vertex
            + left_vertex * second_internal * right_vertex
        )

    amplitude = ordered_amplitude(first_vector, second_vector)
    initial_projector = Rational(1, 2) * (
        clifford_scalar(1) + (1 / mass) * clifford_vector(initial)
    )
    final_projector = Rational(1, 2) * (
        clifford_scalar(1) + (1 / mass) * clifford_vector(final)
    )
    normal_initial = normal_final = None
    if trace_backend == "exterior grade":
        normal_initial = compile_exterior_normal_form(initial_projector, metric)
        normal_final = compile_exterior_normal_form(final_projector, metric)

    def projected_effect(operator):
        if trace_backend == "shared recurrence":
            product = (
                final_projector * operator
                * initial_projector * operator.adjoint()
            )
            return clifford_trace(product, metric)
        normal = compile_exterior_normal_form(operator, metric)
        first_product = exterior_product(normal_final.operator, normal.operator)
        second_product = exterior_product(
            first_product.operator, normal_initial.operator
        )
        third_product = exterior_product(
            second_product.operator, normal.operator.adjoint()
        )
        updates = (
            normal_initial.product_updates + normal_final.product_updates
            + normal.product_updates + first_product.product_updates
            + second_product.product_updates + third_product.product_updates
        )
        return CliffordTrace(
            third_product.operator.scalar_part,
            normal.operator.term_count,
            0,
            normal_form_terms=normal.operator.term_count,
            contraction_updates=updates,
            normal_form_residual=normal.relation_residual,
        )

    trace = projected_effect(amplitude)
    trace_value = simplify(2 * trace.value)
    ward_traces = (
        projected_effect(ordered_amplitude(first, second_vector)),
        projected_effect(ordered_amplitude(first_vector, second)),
    )
    ward = tuple(simplify(2 * item.value) for item in ward_traces)
    ward_updates = sum(
        item.contraction_updates + item.recurrence_updates
        for item in ward_traces
    )
    total_updates = (
        trace.contraction_updates + trace.recurrence_updates + ward_updates
    )
    projectors = (
        simplify(-(mass**2 + dot(initial, initial)) / (4 * mass**2)),
        simplify(-(mass**2 + dot(final, final)) / (4 * mass**2)),
    )
    completion = _positive_completion(trace_value, kinematics.parameter)
    if completion is None:
        return FermionComptonCompilation(
            amplitude=amplitude,
            trace_value=trace_value,
            ward_residuals=ward,
            projector_residuals=projectors,
            refusal=Refusal(
                "spin effect has no certified positive completion",
                residual=(trace_value,), provenance=provenance,
            ),
        )
    square, remainder, witness, residual = completion
    effect = PreparedEventEffect(
        value=witness,
        amplitude_value=amplitude,
        detector_weight=1,
        gauge_residuals=ward,
    )
    return FermionComptonCompilation(
        amplitude=amplitude,
        trace_value=trace_value,
        ward_residuals=ward,
        projector_residuals=projectors,
        trace_terms=trace.word_terms,
        pairing_terms=trace.pairing_terms,
        recurrence_updates=trace.recurrence_updates,
        pfaffian_update_bound=trace.pfaffian_update_bound,
        elimination_updates=trace.elimination_updates,
        pivot_conditions=trace.pivot_conditions,
        trace_backend=trace_backend,
        normal_form_terms=trace.normal_form_terms,
        contraction_updates=trace.contraction_updates,
        ward_updates=ward_updates,
        total_updates=total_updates,
        normal_form_residual=trace.normal_form_residual,
        effect=effect,
        positivity_square=square,
        positivity_remainder=remainder,
        positivity_residual=residual,
    )

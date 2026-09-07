"""Merge ordered fermion-line histories into exterior-valued subset states."""

from dataclasses import dataclass
from itertools import permutations
from math import factorial

from sympy import ImmutableMatrix, simplify, sqrt, sympify

from .clifford import clifford_scalar, clifford_vector
from .exterior import (
    ExteriorOperator,
    compile_exterior_normal_form,
    exterior_product,
    exterior_scale,
    exterior_sum,
)
from .rewrite import Refusal


@dataclass(frozen=True)
class FermionLineCompilation:
    amplitude: ExteriorOperator | None = None
    state_bound: int = 0
    states_visited: int = 0
    ordered_histories: int = 0
    transition_terms: int = 0
    history_steps: int = 0
    construction_updates: int = 0
    evaluation_updates: int = 0
    total_updates: int = 0
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


@dataclass(frozen=True)
class FermionWardCompilation:
    residual: ExteriorOperator | None = None
    total_updates: int = 0
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def compile_fermion_line_amplitude(
    metric,
    initial_momentum,
    photon_momenta,
    polarizations,
    mass_squared,
    *,
    state_budget: int,
    route: str = "subset grade",
) -> FermionLineCompilation:
    """Generate an endpoint-amputated line by subsets or ordered histories."""
    provenance = "exterior-grade fermion-line subset transfer"
    metric = ImmutableMatrix(metric)
    initial = ImmutableMatrix(initial_momentum)
    momenta = tuple(ImmutableMatrix(item) for item in photon_momenta)
    vectors = tuple(ImmutableMatrix(item) for item in polarizations)
    count = len(momenta)
    state_bound = 2**count
    history_count = factorial(count)
    transition_terms = count * 2 ** max(count - 1, 0) if count else 0
    history_steps = count * history_count
    if route not in ("subset grade", "ordered histories"):
        return FermionLineCompilation(refusal=Refusal(
            "unknown fermion-line route", provenance=provenance,
        ))
    if metric.rows != metric.cols or metric.T != metric:
        raise ValueError("metric must be square and symmetric")
    dimension = metric.rows
    if initial.shape != (dimension, 1) or len(vectors) != count or any(
        item.shape != (dimension, 1) for item in momenta + vectors
    ):
        raise ValueError("fermion-line data must belong to one metric space")
    required = state_bound if route == "subset grade" else history_count
    if state_budget < required:
        reason = (
            "fermion subset state budget exceeded"
            if route == "subset grade"
            else "fermion ordered-history budget exceeded"
        )
        return FermionLineCompilation(
            state_bound=state_bound,
            ordered_histories=history_count,
            transition_terms=transition_terms,
            history_steps=history_steps,
            refusal=Refusal(
                reason, residual=(required - state_budget,), provenance=provenance,
            ),
        )

    def dot(left, right):
        return (left.T * metric * right)[0]

    accumulated = [initial]
    for mask in range(1, state_bound):
        bit = mask & -mask
        index = bit.bit_length() - 1
        accumulated.append(accumulated[mask ^ bit] + momenta[index])
    denominators = tuple(
        sympify(mass_squared) + dot(momentum, momentum)
        for momentum in accumulated
    )
    singular = next((
        mask for mask in range(1, state_bound - 1)
        if denominators[mask] == 0
    ), None)
    if singular is not None:
        return FermionLineCompilation(refusal=Refusal(
            "fermion line crosses an internal characteristic",
            residual=(singular,), provenance=provenance,
        ))

    mass = sqrt(sympify(mass_squared))
    identity = compile_exterior_normal_form(clifford_scalar(1), metric)
    if not identity.accepted:
        return FermionLineCompilation(refusal=identity.refusal)
    vertex_forms = tuple(
        compile_exterior_normal_form(clifford_vector(vector), metric)
        for vector in vectors
    )
    propagator_forms = {}
    for mask in range(1, state_bound - 1):
        numerator = clifford_vector(accumulated[mask]) + mass * clifford_scalar(1)
        operator = (-1 / denominators[mask]) * numerator
        propagator_forms[mask] = compile_exterior_normal_form(operator, metric)
    construction_updates = identity.product_updates + sum(
        form.product_updates for form in vertex_forms
    ) + sum(form.product_updates for form in propagator_forms.values())

    transitions = {}
    for before in range(state_bound):
        for index in range(count):
            if before & (1 << index):
                continue
            if before == 0:
                transitions[index, before] = vertex_forms[index].operator
            else:
                product = exterior_product(
                    vertex_forms[index].operator,
                    propagator_forms[before].operator,
                )
                transitions[index, before] = product.operator
                construction_updates += product.product_updates

    evaluation_updates = 0
    if route == "subset grade":
        states = [identity.operator]
        for mask in range(1, state_bound):
            contributions = []
            for index in range(count):
                bit = 1 << index
                if not mask & bit:
                    continue
                before = mask ^ bit
                product = exterior_product(transitions[index, before], states[before])
                contributions.append(product.operator)
                evaluation_updates += product.product_updates
            states.append(exterior_sum(*contributions))
        amplitude = states[-1]
        states_visited = len(states)
    else:
        histories = []
        for ordering in permutations(range(count)):
            value = identity.operator
            before = 0
            for index in ordering:
                product = exterior_product(transitions[index, before], value)
                value = product.operator
                evaluation_updates += product.product_updates
                before |= 1 << index
            histories.append(value)
        amplitude = exterior_sum(*histories)
        states_visited = 0
    return FermionLineCompilation(
        amplitude=amplitude,
        state_bound=state_bound,
        states_visited=states_visited,
        ordered_histories=history_count,
        transition_terms=transition_terms,
        history_steps=history_steps,
        construction_updates=construction_updates,
        evaluation_updates=evaluation_updates,
        total_updates=construction_updates + evaluation_updates,
    )


def compile_fermion_ward_boundary(
    metric,
    initial_momentum,
    photon_momenta,
    polarizations,
    mass_squared,
    *,
    contracted_label: int,
    state_budget: int,
) -> FermionWardCompilation:
    """Compute the endpoint-ideal residual of one contracted photon."""
    metric = ImmutableMatrix(metric)
    initial = ImmutableMatrix(initial_momentum)
    momenta = tuple(ImmutableMatrix(item) for item in photon_momenta)
    vectors = list(ImmutableMatrix(item) for item in polarizations)
    if not 0 <= contracted_label < len(momenta):
        return FermionWardCompilation(refusal=Refusal(
            "contracted photon label is outside the line",
            provenance="fermion endpoint Ward boundary",
        ))
    vectors[contracted_label] = momenta[contracted_label]
    contracted = compile_fermion_line_amplitude(
        metric, initial, momenta, tuple(vectors), mass_squared,
        state_budget=state_budget, route="subset grade",
    )
    other_momenta = tuple(
        item for index, item in enumerate(momenta) if index != contracted_label
    )
    other_vectors = tuple(
        item for index, item in enumerate(polarizations) if index != contracted_label
    )
    shifted = initial + momenta[contracted_label]
    left_line = compile_fermion_line_amplitude(
        metric, initial, other_momenta, other_vectors, mass_squared,
        state_budget=state_budget, route="subset grade",
    )
    right_line = compile_fermion_line_amplitude(
        metric, shifted, other_momenta, other_vectors, mass_squared,
        state_budget=state_budget, route="subset grade",
    )
    failed = next(
        (item for item in (contracted, left_line, right_line) if not item.accepted),
        None,
    )
    if failed is not None:
        return FermionWardCompilation(refusal=failed.refusal)

    def dot(left, right):
        return (left.T * metric * right)[0]

    mass = sqrt(sympify(mass_squared))
    final = initial + sum(momenta, ImmutableMatrix.zeros(metric.rows, 1))
    without = initial + sum(other_momenta, ImmutableMatrix.zeros(metric.rows, 1))

    def lower(operator):
        return compile_exterior_normal_form(operator, metric)

    def propagator(momentum):
        denominator = sympify(mass_squared) + dot(momentum, momentum)
        return lower((-1 / denominator) * (
            clifford_vector(momentum) + mass * clifford_scalar(1)
        ))

    final_kinetic = lower(clifford_vector(final) + (-mass) * clifford_scalar(1))
    initial_kinetic = lower(
        clifford_vector(initial) + (-mass) * clifford_scalar(1)
    )
    left_prop = propagator(without)
    right_prop = propagator(shifted)
    left_first = exterior_product(final_kinetic.operator, left_prop.operator)
    left = exterior_product(left_first.operator, left_line.amplitude)
    right_first = exterior_product(right_line.amplitude, right_prop.operator)
    right = exterior_product(right_first.operator, initial_kinetic.operator)
    residual = exterior_sum(
        contracted.amplitude,
        exterior_scale(-1, left.operator),
        right.operator,
    )
    boundary_updates = sum(
        item.product_updates
        for item in (final_kinetic, initial_kinetic, left_prop, right_prop)
    ) + sum(item.product_updates for item in (
        left_first, left, right_first, right,
    ))
    return FermionWardCompilation(
        residual=residual,
        total_updates=(
            contracted.total_updates + left_line.total_updates
            + right_line.total_updates + boundary_updates
        ),
    )

"""Compile open-line insertion histories into a matching-kernel quotient."""

from dataclasses import dataclass
from functools import cache
from math import comb, factorial

from sympy import ImmutableMatrix, sympify

from .rewrite import Refusal


@dataclass(frozen=True)
class InsertionCell:
    pair_count: int
    master_monomials: int
    ordering_chambers: int
    ordered_histories: int


@dataclass(frozen=True)
class OpenLineQuotient:
    photon_count: int
    cells: tuple[InsertionCell, ...]
    master_monomials: int
    ordered_histories: int
    pair_kernel_entries: int
    subset_state_bound: int
    provenance: str


@dataclass(frozen=True)
class MatchingEvaluation:
    value: object | None = None
    state_bound: int = 0
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


@dataclass(frozen=True)
class ScalarLineEvaluation:
    value: object | None = None
    state_bound: int = 0
    states_visited: int = 0
    ordered_histories: int = 0
    transition_terms: int = 0
    history_event_terms: int = 0
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None


def compile_open_line_quotient(photon_count: int) -> OpenLineQuotient:
    """Count matching monomials and their ordered scalar-line chambers."""
    if photon_count < 0:
        raise ValueError("photon count must be nonnegative")

    cells = []
    for pair_count in range(photon_count // 2 + 1):
        singles = photon_count - 2 * pair_count
        matching_count = factorial(photon_count) // (
            2**pair_count * factorial(pair_count) * factorial(singles)
        )
        chambers = factorial(photon_count - pair_count)
        cells.append(InsertionCell(
            pair_count=pair_count,
            master_monomials=matching_count,
            ordering_chambers=chambers,
            ordered_histories=matching_count * chambers,
        ))

    return OpenLineQuotient(
        photon_count=photon_count,
        cells=tuple(cells),
        master_monomials=sum(cell.master_monomials for cell in cells),
        ordered_histories=sum(cell.ordered_histories for cell in cells),
        pair_kernel_entries=comb(photon_count, 2),
        subset_state_bound=2**photon_count,
        provenance="singleton/pair matching quotient of ordered scalar-line events",
    )


def evaluate_matching_kernel(
    linear_weights: tuple[object, ...],
    pair_weights: tuple[tuple[object, ...], ...],
    *,
    state_budget: int,
) -> MatchingEvaluation:
    """Evaluate the multilinear Gaussian coefficient by subset recurrence."""
    photon_count = len(linear_weights)
    if len(pair_weights) != photon_count or any(
        len(row) != photon_count for row in pair_weights
    ):
        raise ValueError("pair kernel must be square on the photon labels")
    if any(
        pair_weights[i][j] != pair_weights[j][i]
        for i in range(photon_count)
        for j in range(i)
    ):
        raise ValueError("pair kernel must be symmetric")

    state_bound = 2**photon_count
    if state_budget < state_bound:
        return MatchingEvaluation(
            state_bound=state_bound,
            refusal=Refusal(
                "matching state budget exceeded",
                residual=(state_bound - state_budget,),
                provenance="worldline multilinear coefficient",
            ),
        )

    @cache
    def reduce_subset(mask: int):
        if mask == 0:
            return 1
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        remainder = mask ^ first_bit
        value = linear_weights[first] * reduce_subset(remainder)
        partners = remainder
        while partners:
            partner_bit = partners & -partners
            partner = partner_bit.bit_length() - 1
            value += pair_weights[first][partner] * reduce_subset(
                remainder ^ partner_bit
            )
            partners ^= partner_bit
        return value

    return MatchingEvaluation(
        value=reduce_subset((1 << photon_count) - 1),
        state_bound=state_bound,
    )


def evaluate_scalar_line_amplitude(
    metric,
    initial_momentum,
    photon_momenta,
    polarizations,
    mass_squared,
    *,
    state_budget: int,
    amputate_initial: bool = False,
    amputate_final: bool = False,
) -> ScalarLineEvaluation:
    """Evaluate a scalar line, optionally cancelling either endpoint kernel."""
    metric = ImmutableMatrix(metric)
    initial_momentum = ImmutableMatrix(initial_momentum)
    photon_momenta = tuple(ImmutableMatrix(item) for item in photon_momenta)
    polarizations = tuple(ImmutableMatrix(item) for item in polarizations)
    mass_squared = sympify(mass_squared)
    photon_count = len(photon_momenta)
    state_bound = 2**photon_count
    quotient = compile_open_line_quotient(photon_count)
    history_count = quotient.ordered_histories
    transition_terms = sum(
        comb(photon_count, subset_size)
        * (subset_size + comb(subset_size, 2))
        for subset_size in range(photon_count + 1)
    )
    history_event_terms = sum(
        cell.ordered_histories * (photon_count - cell.pair_count)
        for cell in quotient.cells
    )

    if metric.rows != metric.cols or metric.T != metric:
        raise ValueError("metric must be square and symmetric")
    dimension = metric.rows
    if initial_momentum.shape != (dimension, 1):
        raise ValueError("initial momentum must belong to the metric space")
    if len(polarizations) != photon_count:
        raise ValueError("every photon momentum needs one polarization")
    if any(
        vector.shape != (dimension, 1)
        for vector in photon_momenta + polarizations
    ):
        raise ValueError("photon data must belong to the metric space")
    if state_budget < state_bound:
        return ScalarLineEvaluation(
            state_bound=state_bound,
            ordered_histories=history_count,
            transition_terms=transition_terms,
            history_event_terms=history_event_terms,
            refusal=Refusal(
                "scalar-line state budget exceeded",
                residual=(state_bound - state_budget,),
                provenance="Euclidean open-line subset transfer",
            ),
        )

    def dot(left, right):
        return (left.T * metric * right)[0]

    momenta = [initial_momentum]
    for mask in range(1, state_bound):
        last_bit = mask & -mask
        index = last_bit.bit_length() - 1
        momenta.append(momenta[mask ^ last_bit] + photon_momenta[index])
    denominators = tuple(
        mass_squared + dot(momentum, momentum) for momentum in momenta
    )
    inverted_masks = range(state_bound)
    singular = next((
        mask for mask in inverted_masks
        if denominators[mask] == 0
        and not (amputate_initial and mask == 0)
        and not (amputate_final and mask == state_bound - 1)
    ), None)
    if singular is not None:
        return ScalarLineEvaluation(
            state_bound=state_bound,
            ordered_histories=history_count,
            transition_terms=transition_terms,
            history_event_terms=history_event_terms,
            refusal=Refusal(
                "scalar line crosses characteristic denominator",
                residual=(singular,),
                provenance="Euclidean open-line subset transfer",
            ),
        )

    @cache
    def transfer(mask: int):
        if mask == 0:
            return 1 if amputate_initial else 1 / denominators[0]
        after = momenta[mask]
        value = 0
        available = tuple(
            index for index in range(photon_count) if mask & (1 << index)
        )
        for index in available:
            before_mask = mask ^ (1 << index)
            vertex = dot(
                momenta[before_mask] + after,
                polarizations[index],
            )
            value += vertex * transfer(before_mask)
        for left_position, left in enumerate(available):
            for right in available[left_position + 1:]:
                before_mask = mask ^ (1 << left) ^ (1 << right)
                contact = -2 * dot(polarizations[left], polarizations[right])
                value += contact * transfer(before_mask)
        if amputate_final and mask == state_bound - 1:
            return value
        return value / denominators[mask]

    value = transfer(state_bound - 1)
    return ScalarLineEvaluation(
        value=value,
        state_bound=state_bound,
        states_visited=transfer.cache_info().currsize,
        ordered_histories=history_count,
        transition_terms=transition_terms,
        history_event_terms=history_event_terms,
    )

"""Frozen tasks and schedules for matched direct/sparse network work."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from typing import Optional

from sympy import Matrix, simplify, sympify
from sympy.core.expr import Expr

from .network import LinearNetworkRequest, condense_linear_network
from .network_human import construct_network_human_boundary
from .network_order import NetworkEliminationPlan, plan_network_elimination
from .records import Certificate


NETWORK_STUDY_PHASES = (
    "immediate_assisted",
    "delayed_same_topology",
    "unseen_topology",
)
NETWORK_STUDY_COLUMNS = (
    "observation_id",
    "participant_id",
    "session_id",
    "sequence_id",
    "trial_order",
    "phase",
    "pair_id",
    "variant_id",
    "assigned_route",
    "strip_available",
    "hours_since_immediate",
    "interpretation_seconds",
    "setup_seconds",
    "computation_seconds",
    "return_seconds",
    "independent_total_seconds",
    "phase_timing_reliable",
    "completion",
    "submitted_answer",
    "error_codes",
    "route_adherent",
    "prior_familiarity",
    "provenance",
)
NETWORK_STUDY_REVIEW_COLUMNS = (
    "review_id",
    "reviewer_id",
    "variant_id",
    "declared_expertise",
    "independently_solved",
    "blinded_to_authored_routes",
    "blinded_to_peer_reviews",
    "exact_answer_agrees",
    "direct_route_valid",
    "sparse_route_valid",
    "baseline_competent",
    "notes",
    "provenance",
)


@dataclass(frozen=True)
class NetworkStudyVariant:
    variant_id: str
    topology_family: str
    prompt: str
    request: LinearNetworkRequest
    boundary_values: tuple[object, ...]
    provenance: str

    def __post_init__(self) -> None:
        for name in ("variant_id", "topology_family", "prompt", "provenance"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be nonempty.")
        if len(self.boundary_values) != len(self.request.boundary_symbols):
            raise ValueError("Boundary values must match the observable boundary.")


@dataclass(frozen=True)
class NetworkStudyAnswer:
    status: str
    variant_id: str
    target_value: Optional[Expr] = None
    structural_disposition: str = "not_applicable"
    declared_plan: Optional[NetworkEliminationPlan] = None
    sparse_plan: Optional[NetworkEliminationPlan] = None
    certificates: tuple[Certificate, ...] = ()
    obstruction: str = ""


@dataclass(frozen=True)
class NetworkStudyPair:
    pair_id: str
    phase: str
    topology_family: str
    variant_a: NetworkStudyVariant
    variant_b: NetworkStudyVariant
    provenance: str

    def __post_init__(self) -> None:
        if self.phase not in NETWORK_STUDY_PHASES:
            raise ValueError(f"Unknown network-study phase {self.phase!r}.")
        if not self.pair_id.strip() or not self.provenance.strip():
            raise ValueError("Pair identity and provenance must be nonempty.")
        variants = (self.variant_a, self.variant_b)
        if variants[0].variant_id == variants[1].variant_id:
            raise ValueError("A network pair requires distinct variants.")
        if any(item.topology_family != self.topology_family for item in variants):
            raise ValueError("Pair variants must preserve the topology family.")


@dataclass(frozen=True)
class NetworkStudyTrial:
    order: int
    phase: str
    pair_id: str
    variant_id: str
    assigned_route: str


@dataclass(frozen=True)
class NetworkStudySchedule:
    sequence_id: str
    trials: tuple[NetworkStudyTrial, ...]


@dataclass(frozen=True)
class NetworkStudyObservation:
    observation_id: str
    participant_id: str
    session_id: str
    sequence_id: str
    trial_order: int
    phase: str
    pair_id: str
    variant_id: str
    assigned_route: str
    strip_available: bool
    hours_since_immediate: Fraction
    interpretation_seconds: Fraction
    setup_seconds: Fraction
    computation_seconds: Fraction
    return_seconds: Fraction
    independent_total_seconds: Fraction
    phase_timing_reliable: bool
    completion: str
    submitted_answer: Optional[Expr]
    expected_answer: Expr
    error_codes: tuple[str, ...]
    route_adherent: bool
    prior_familiarity: str
    provenance: str

    @property
    def total_seconds(self) -> Fraction:
        return self.independent_total_seconds

    @property
    def correct(self) -> bool:
        return (
            self.completion == "complete"
            and self.submitted_answer is not None
            and simplify(self.submitted_answer - self.expected_answer) == 0
            and not self.error_codes
        )


@dataclass(frozen=True)
class NetworkStudyPhaseDiagnostics:
    phase: str
    participant_count: int
    observed_attempts: int
    direct_correct: int
    sparse_correct: int
    eligible_pairs: int
    ineligible_pairs: int
    complete_participant_clusters: int
    mean_cluster_time_delta: Optional[Fraction]
    sample_variance_cluster_time_delta: Optional[Fraction]


@dataclass(frozen=True)
class NetworkStudyDiagnostics:
    status: str
    phases: tuple[NetworkStudyPhaseDiagnostics, ...]
    speed_disposition: str = "not_evaluated"
    retention_disposition: str = "not_evaluated"
    transfer_disposition: str = "not_evaluated"


@dataclass(frozen=True)
class NetworkStudyReview:
    review_id: str
    reviewer_id: str
    variant_id: str
    declared_expertise: str
    independently_solved: bool
    blinded_to_authored_routes: bool
    blinded_to_peer_reviews: bool
    exact_answer_agrees: bool
    direct_route_valid: bool
    sparse_route_valid: bool
    baseline_competent: bool
    notes: str
    provenance: str


@dataclass(frozen=True)
class NetworkStudyKeyAudit:
    status: str
    total_variants: int
    reviewed_variants: int
    needs_review: tuple[str, ...]
    revision_required: tuple[str, ...]


@lru_cache(maxsize=None)
def solve_network_study_variant(variant: NetworkStudyVariant) -> NetworkStudyAnswer:
    """Construct the exact answer independently of either handwritten route."""

    condensed = condense_linear_network(variant.request)
    declared = plan_network_elimination(variant.request, strategy="declared")
    sparse = plan_network_elimination(variant.request, strategy="min_fill")
    if condensed.status != "constructed" or any(
        item.status != "constructed" for item in (declared, sparse)
    ):
        codes = tuple(
            item.obstruction.code
            for item in (condensed, declared, sparse)
            if item.status != "constructed" and item.obstruction is not None
        )
        return NetworkStudyAnswer(
            "refused", variant.variant_id, obstruction=";".join(codes)
        )
    boundary = Matrix(tuple(sympify(value) for value in variant.boundary_values))
    injection = Matrix(condensed.condensed_matrix) * boundary - Matrix(
        condensed.condensed_source
    )
    human = construct_network_human_boundary(
        variant.request,
        problem_id=variant.variant_id,
        target="first-boundary injection",
    )
    target = simplify(injection[0])
    certificates = (
        Certificate(
            "route_independent_key",
            declared.condensed_matrix
            == sparse.condensed_matrix
            == condensed.condensed_matrix
            and declared.condensed_source
            == sparse.condensed_source
            == condensed.condensed_source,
            "block, declared scalar, and sparse scalar routes return one boundary law",
        ),
        Certificate(
            "observable_target_extracted",
            target == simplify(injection[0]),
            "the key is the first component of K_boundary*x_boundary-f_boundary",
        ),
    )
    if human.status != "constructed" or not all(item.passed for item in certificates):
        return NetworkStudyAnswer(
            "refused", variant.variant_id, obstruction="key_certificate_failed"
        )
    return NetworkStudyAnswer(
        "constructed",
        variant.variant_id,
        target,
        human.admission_boundary.classification,
        declared,
        sparse,
        certificates,
    )


def validate_network_study_pairs(pairs: tuple[NetworkStudyPair, ...]) -> None:
    pair_ids = tuple(item.pair_id for item in pairs)
    variant_ids = tuple(
        variant.variant_id
        for pair in pairs
        for variant in (pair.variant_a, pair.variant_b)
    )
    if len(pair_ids) != len(set(pair_ids)) or len(variant_ids) != len(set(variant_ids)):
        raise ValueError("Network-study pair and variant ids must be unique.")
    groups = {
        phase: tuple(item for item in pairs if item.phase == phase)
        for phase in NETWORK_STUDY_PHASES
    }
    if any(len(group) != 2 for group in groups.values()):
        raise ValueError("The frozen network study requires two pairs per phase.")
    immediate = {item.topology_family for item in groups["immediate_assisted"]}
    delayed = {item.topology_family for item in groups["delayed_same_topology"]}
    unseen = {item.topology_family for item in groups["unseen_topology"]}
    if immediate != delayed or immediate & unseen:
        raise ValueError(
            "Delayed topologies must repeat training; unseen topologies must be disjoint."
        )


def network_study_variant_map(
    pairs: tuple[NetworkStudyPair, ...],
) -> dict[str, NetworkStudyVariant]:
    return {
        variant.variant_id: variant
        for pair in pairs
        for variant in (pair.variant_a, pair.variant_b)
    }


def build_network_study_schedules(
    pairs: tuple[NetworkStudyPair, ...],
) -> tuple[NetworkStudySchedule, NetworkStudySchedule]:
    """Counterbalance routes and variants independently inside each phase."""

    validate_network_study_pairs(pairs)
    blocks: dict[str, list[NetworkStudyTrial]] = {"N1": [], "N2": []}
    for phase in NETWORK_STUDY_PHASES:
        group = tuple(item for item in pairs if item.phase == phase)
        offset = len(blocks["N1"])
        for sequence, reverse in (("N1", False), ("N2", True)):
            first = []
            second = []
            for index, pair in enumerate(group):
                swap = (index % 2 == 1) ^ reverse
                direct = pair.variant_b if swap else pair.variant_a
                sparse = pair.variant_a if swap else pair.variant_b
                first.append((pair, direct, "direct"))
                second.append((pair, sparse, "sparse"))
            blocks[sequence].extend(
                NetworkStudyTrial(
                    offset + order,
                    pair.phase,
                    pair.pair_id,
                    variant.variant_id,
                    route,
                )
                for order, (pair, variant, route) in enumerate(
                    (*first, *second), start=1
                )
            )
    return tuple(
        NetworkStudySchedule(key, tuple(value)) for key, value in blocks.items()
    )

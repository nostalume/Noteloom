"""Unassigned adaptive-route decisions for reciprocal network problems."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache

from .network import LinearNetworkRequest
from .network_human import construct_network_human_boundary
from .records import Certificate


NETWORK_ADMISSION_PHASES = (
    "immediate_unassisted",
    "delayed_same_topology",
    "unseen_topology",
)
NETWORK_ADMISSION_DECISIONS = frozenset(
    {"direct_gate", "conditional_candidate", "refuse"}
)
NETWORK_ADMISSION_COLUMNS = (
    "observation_id",
    "participant_id",
    "session_id",
    "sequence_id",
    "trial_order",
    "phase",
    "task_id",
    "selected_decision",
    "decision_seconds",
    "hours_since_training",
    "completion",
    "justification",
    "provenance",
)
NETWORK_ADMISSION_REVIEW_COLUMNS = (
    "review_id",
    "reviewer_id",
    "task_id",
    "declared_expertise",
    "independently_classified",
    "blinded_to_authored_key",
    "blinded_to_peer_reviews",
    "expected_decision_agrees",
    "prompt_unambiguous",
    "notes",
    "provenance",
)


@dataclass(frozen=True)
class NetworkAdmissionTask:
    task_id: str
    phase: str
    topology_family: str
    prompt: str
    request: LinearNetworkRequest
    provenance: str

    def __post_init__(self) -> None:
        if self.phase not in NETWORK_ADMISSION_PHASES:
            raise ValueError(f"Unknown admission-study phase {self.phase!r}.")
        for name in ("task_id", "topology_family", "prompt", "provenance"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be nonempty.")


@dataclass(frozen=True)
class NetworkAdmissionKey:
    status: str
    task_id: str
    expected_decision: str
    decision_witness: str
    obstruction_code: str = ""
    certificates: tuple[Certificate, ...] = ()


@dataclass(frozen=True)
class NetworkAdmissionTrial:
    order: int
    phase: str
    task_id: str


@dataclass(frozen=True)
class NetworkAdmissionSchedule:
    sequence_id: str
    trials: tuple[NetworkAdmissionTrial, ...]


@dataclass(frozen=True)
class NetworkAdmissionObservation:
    observation_id: str
    participant_id: str
    session_id: str
    sequence_id: str
    trial_order: int
    phase: str
    task_id: str
    selected_decision: str
    expected_decision: str
    decision_seconds: Fraction
    hours_since_training: Fraction
    completion: str
    justification: str
    provenance: str

    @property
    def correct(self) -> bool:
        return (
            self.completion == "complete"
            and self.selected_decision == self.expected_decision
        )


@dataclass(frozen=True)
class NetworkAdmissionPhaseDiagnostics:
    phase: str
    participant_count: int
    observed_decisions: int
    correct_decisions: int
    complete_participant_clusters: int
    mean_participant_accuracy: Fraction | None
    mean_participant_decision_seconds: Fraction | None
    selection_counts: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class NetworkAdmissionDiagnostics:
    status: str
    phases: tuple[NetworkAdmissionPhaseDiagnostics, ...]
    recognition_disposition: str = "not_evaluated"
    retention_disposition: str = "not_evaluated"
    transfer_disposition: str = "not_evaluated"


@dataclass(frozen=True)
class NetworkAdmissionReview:
    review_id: str
    reviewer_id: str
    task_id: str
    declared_expertise: str
    independently_classified: bool
    blinded_to_authored_key: bool
    blinded_to_peer_reviews: bool
    expected_decision_agrees: bool
    prompt_unambiguous: bool
    notes: str
    provenance: str


@dataclass(frozen=True)
class NetworkAdmissionKeyAudit:
    status: str
    total_tasks: int
    reviewed_tasks: int
    needs_review: tuple[str, ...]
    revision_required: tuple[str, ...]


@lru_cache(maxsize=None)
def construct_network_admission_key(task: NetworkAdmissionTask) -> NetworkAdmissionKey:
    """Classify what the exact positive-weight boundary permits before solving."""

    result = construct_network_human_boundary(
        task.request,
        problem_id=task.task_id,
        target="terminal response",
    )
    if result.status == "refused":
        code = result.obstruction.code
        return NetworkAdmissionKey(
            "constructed",
            task.task_id,
            "refuse",
            f"planner obstruction: {code}",
            code,
            (
                Certificate(
                    "typed_refusal_preserved",
                    bool(code),
                    "the learner key preserves the scalar planner obstruction",
                ),
            ),
        )
    classification = result.admission_boundary.classification
    decision = {
        "always_direct": "direct_gate",
        "conditional": "conditional_candidate",
    }.get(classification)
    if decision is None:
        raise ValueError(
            f"Admission task {task.task_id!r} has unsupported class {classification!r}."
        )
    witness = (
        "strictly positive weights always favor direct"
        if decision == "direct_gate"
        else result.admission_boundary.proposed_cheaper_when
    )
    return NetworkAdmissionKey(
        "constructed",
        task.task_id,
        decision,
        witness,
        certificates=(
            Certificate(
                "decision_restored_from_boundary",
                decision
                == {
                    "always_direct": "direct_gate",
                    "conditional": "conditional_candidate",
                }[classification],
                "the three-valued key is derived from the exact cost boundary",
            ),
            Certificate(
                "human_claim_not_promoted",
                result.learnability_disposition == "human_observations_required",
                "the task key does not turn a structural class into human evidence",
            ),
        ),
    )


def validate_network_admission_tasks(tasks: tuple[NetworkAdmissionTask, ...]) -> None:
    task_ids = tuple(task.task_id for task in tasks)
    if len(task_ids) != len(set(task_ids)):
        raise ValueError("Network-admission task ids must be unique.")
    groups = {
        phase: tuple(task for task in tasks if task.phase == phase)
        for phase in NETWORK_ADMISSION_PHASES
    }
    if any(len(group) != 3 for group in groups.values()):
        raise ValueError("The frozen admission study requires three tasks per phase.")
    for phase, group in groups.items():
        decisions = {
            construct_network_admission_key(task).expected_decision for task in group
        }
        if decisions != NETWORK_ADMISSION_DECISIONS:
            raise ValueError(f"Phase {phase!r} must cover all three decision classes.")
    immediate = {task.topology_family for task in groups["immediate_unassisted"]}
    delayed = {task.topology_family for task in groups["delayed_same_topology"]}
    unseen = {task.topology_family for task in groups["unseen_topology"]}
    if immediate != delayed or immediate & unseen:
        raise ValueError(
            "Delayed tasks must repeat trained families; unseen families must be disjoint."
        )


def build_network_admission_schedules(
    tasks: tuple[NetworkAdmissionTask, ...],
) -> tuple[NetworkAdmissionSchedule, NetworkAdmissionSchedule]:
    """Reverse task order within each phase without exposing the key."""

    validate_network_admission_tasks(tasks)
    blocks = {"A1": [], "A2": []}
    for phase in NETWORK_ADMISSION_PHASES:
        group = tuple(task for task in tasks if task.phase == phase)
        offset = len(blocks["A1"])
        for sequence, ordered in (("A1", group), ("A2", tuple(reversed(group)))):
            blocks[sequence].extend(
                NetworkAdmissionTrial(offset + index, phase, task.task_id)
                for index, task in enumerate(ordered, start=1)
            )
    return tuple(
        NetworkAdmissionSchedule(sequence, tuple(trials))
        for sequence, trials in blocks.items()
    )

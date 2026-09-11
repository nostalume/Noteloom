"""Strict ingestion for adaptive network-admission observations and reviews."""

import csv
from fractions import Fraction
from pathlib import Path

from .network_admission import (
    NETWORK_ADMISSION_COLUMNS,
    NETWORK_ADMISSION_DECISIONS,
    NETWORK_ADMISSION_REVIEW_COLUMNS,
    NetworkAdmissionObservation,
    NetworkAdmissionReview,
    NetworkAdmissionSchedule,
    NetworkAdmissionTask,
    construct_network_admission_key,
    validate_network_admission_tasks,
)

_COMPLETION = frozenset({"complete", "timeout", "abandoned"})


def _parse_bool(value: str, name: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "false"}:
        return normalized == "true"
    raise ValueError(f"{name} must be true or false.")


def load_network_admission_observation_tsv(
    path: Path,
    tasks: tuple[NetworkAdmissionTask, ...],
    schedules: tuple[NetworkAdmissionSchedule, ...],
) -> tuple[NetworkAdmissionObservation, ...]:
    """Restore task assignments and exact decisions from the frozen schedule."""

    validate_network_admission_tasks(tasks)
    task_by_id = {task.task_id: task for task in tasks}
    trials = {
        (schedule.sequence_id, trial.order): trial
        for schedule in schedules
        for trial in schedule.trials
    }
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != NETWORK_ADMISSION_COLUMNS:
            raise ValueError(
                "Network-admission TSV columns do not match the frozen schema."
            )
        observations = [_restore_observation(row, trials, task_by_id) for row in reader]
    _validate_observation_relations(observations)
    return tuple(observations)


def _restore_observation(row, trials, task_by_id) -> NetworkAdmissionObservation:
    sequence = row["sequence_id"].strip()
    order = int(row["trial_order"].strip())
    if (sequence, order) not in trials:
        raise ValueError("Observation does not name a frozen schedule trial.")
    trial = trials[(sequence, order)]
    supplied = (row["phase"].strip(), row["task_id"].strip())
    if supplied != (trial.phase, trial.task_id):
        raise ValueError("Observation conflicts with the frozen schedule.")
    selected = row["selected_decision"].strip()
    if selected not in NETWORK_ADMISSION_DECISIONS:
        raise ValueError(f"Unknown selected decision {selected!r}.")
    seconds = Fraction(row["decision_seconds"].strip())
    if seconds <= 0:
        raise ValueError("Decision time must be positive.")
    delay = Fraction(row["hours_since_training"].strip())
    if delay < 0 or (trial.phase == "immediate_unassisted" and delay != 0):
        raise ValueError("Immediate recognition defines the zero-delay reference.")
    if trial.phase != "immediate_unassisted" and delay <= 0:
        raise ValueError("Delayed and unseen recognition require a positive delay.")
    completion = row["completion"].strip()
    if completion not in _COMPLETION:
        raise ValueError(f"Unknown completion status {completion!r}.")
    task = task_by_id[trial.task_id]
    key = construct_network_admission_key(task)
    return NetworkAdmissionObservation(
        row["observation_id"].strip(),
        row["participant_id"].strip(),
        row["session_id"].strip(),
        sequence,
        order,
        trial.phase,
        trial.task_id,
        selected,
        key.expected_decision,
        seconds,
        delay,
        completion,
        row["justification"].strip(),
        f"{task.provenance}; {row['provenance'].strip()}",
    )


def _validate_observation_relations(
    observations: list[NetworkAdmissionObservation],
) -> None:
    ids = [item.observation_id for item in observations]
    slots = [
        (item.participant_id, item.sequence_id, item.trial_order)
        for item in observations
    ]
    if len(ids) != len(set(ids)) or len(slots) != len(set(slots)):
        raise ValueError("Duplicate admission observation or participant trial.")
    if any(
        not text.strip()
        for item in observations
        for text in (
            item.observation_id,
            item.participant_id,
            item.session_id,
            item.provenance,
        )
    ):
        raise ValueError("Admission identity and provenance must be nonempty.")
    for participant in {item.participant_id for item in observations}:
        rows = [item for item in observations if item.participant_id == participant]
        if len({item.sequence_id for item in rows}) != 1:
            raise ValueError("Each participant must use one admission sequence.")
        phase_sessions, session_phases, phase_delays = {}, {}, {}
        for item in rows:
            phase_sessions.setdefault(item.phase, set()).add(item.session_id)
            session_phases.setdefault(item.session_id, set()).add(item.phase)
            phase_delays.setdefault(item.phase, set()).add(item.hours_since_training)
        relations = (
            *phase_sessions.values(),
            *session_phases.values(),
            *phase_delays.values(),
        )
        if any(len(values) != 1 for values in relations):
            raise ValueError("Each admission phase requires one session and delay.")
        if (
            "delayed_same_topology" in phase_delays
            and "unseen_topology" in phase_delays
        ):
            delayed = next(iter(phase_delays["delayed_same_topology"]))
            unseen = next(iter(phase_delays["unseen_topology"]))
            if unseen <= delayed:
                raise ValueError(
                    "Unseen recognition must occur after delayed recognition."
                )


def load_network_admission_review_tsv(
    path: Path, tasks: tuple[NetworkAdmissionTask, ...]
) -> tuple[NetworkAdmissionReview, ...]:
    task_ids = {task.task_id for task in tasks}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != NETWORK_ADMISSION_REVIEW_COLUMNS:
            raise ValueError(
                "Network-admission review columns do not match the frozen schema."
            )
        reviews = tuple(_restore_review(row) for row in reader)
    if any(review.task_id not in task_ids for review in reviews):
        raise ValueError("Admission review names an unknown task.")
    ids = [review.review_id for review in reviews]
    slots = [(review.reviewer_id, review.task_id) for review in reviews]
    if len(ids) != len(set(ids)) or len(slots) != len(set(slots)):
        raise ValueError("Duplicate admission review or reviewer/task slot.")
    return reviews


def _restore_review(row) -> NetworkAdmissionReview:
    return NetworkAdmissionReview(
        row["review_id"].strip(),
        row["reviewer_id"].strip(),
        row["task_id"].strip(),
        row["declared_expertise"].strip(),
        *(
            _parse_bool(row[name], name)
            for name in (
                "independently_classified",
                "blinded_to_authored_key",
                "blinded_to_peer_reviews",
                "expected_decision_agrees",
                "prompt_unambiguous",
            )
        ),
        row["notes"].strip(),
        row["provenance"].strip(),
    )

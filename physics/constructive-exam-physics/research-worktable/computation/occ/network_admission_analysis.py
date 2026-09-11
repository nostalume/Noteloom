"""Clustered diagnostics and blinded-key audit for adaptive route recognition."""

from __future__ import annotations

from fractions import Fraction

from .network_admission import (
    NETWORK_ADMISSION_DECISIONS,
    NETWORK_ADMISSION_PHASES,
    NetworkAdmissionDiagnostics,
    NetworkAdmissionKeyAudit,
    NetworkAdmissionObservation,
    NetworkAdmissionPhaseDiagnostics,
    NetworkAdmissionReview,
    NetworkAdmissionTask,
)


def construct_network_admission_diagnostics(
    observations: tuple[NetworkAdmissionObservation, ...],
    tasks: tuple[NetworkAdmissionTask, ...],
) -> NetworkAdmissionDiagnostics:
    """Summarize complete participant-phase recognition clusters without verdict."""

    task_by_id = {task.task_id: task for task in tasks}
    if len(task_by_id) != len(tasks):
        raise ValueError("Admission task ids must be unique.")
    for item in observations:
        if (
            item.task_id not in task_by_id
            or item.phase != task_by_id[item.task_id].phase
        ):
            raise ValueError("Admission observation conflicts with its frozen task.")
    phases = tuple(
        _diagnose_phase(phase, observations, tasks)
        for phase in NETWORK_ADMISSION_PHASES
    )
    if not observations:
        status = "unobserved"
    elif all(item.complete_participant_clusters >= 2 for item in phases):
        status = "design_inputs_observed"
    else:
        status = "incomplete_design_inputs"
    return NetworkAdmissionDiagnostics(status, phases)


def _diagnose_phase(phase, observations, tasks):
    task_ids = {task.task_id for task in tasks if task.phase == phase}
    rows = tuple(item for item in observations if item.phase == phase)
    participants = tuple(sorted({item.participant_id for item in rows}))
    accuracy, mean_times = [], []
    for participant in participants:
        cluster = tuple(item for item in rows if item.participant_id == participant)
        if (
            len(cluster) == len(task_ids)
            and {item.task_id for item in cluster} == task_ids
            and all(item.completion == "complete" for item in cluster)
        ):
            accuracy.append(
                Fraction(sum(item.correct for item in cluster), len(cluster))
            )
            mean_times.append(
                sum((item.decision_seconds for item in cluster), Fraction())
                / len(cluster)
            )
    mean_accuracy = sum(accuracy, Fraction()) / len(accuracy) if accuracy else None
    mean_seconds = sum(mean_times, Fraction()) / len(mean_times) if mean_times else None
    return NetworkAdmissionPhaseDiagnostics(
        phase=phase,
        participant_count=len(participants),
        observed_decisions=len(rows),
        correct_decisions=sum(item.correct for item in rows),
        complete_participant_clusters=len(accuracy),
        mean_participant_accuracy=mean_accuracy,
        mean_participant_decision_seconds=mean_seconds,
        selection_counts=tuple(
            (decision, sum(item.selected_decision == decision for item in rows))
            for decision in sorted(NETWORK_ADMISSION_DECISIONS)
        ),
    )


def audit_network_admission_key(
    reviews: tuple[NetworkAdmissionReview, ...],
    tasks: tuple[NetworkAdmissionTask, ...],
) -> NetworkAdmissionKeyAudit:
    """Require two independent blinded agreements for every recognition task."""

    task_ids = tuple(task.task_id for task in tasks)
    if len(task_ids) != len(set(task_ids)):
        raise ValueError("Admission task ids must be unique.")
    if any(review.task_id not in set(task_ids) for review in reviews):
        raise ValueError("Admission review names an unknown task.")
    needs_review, revision, reviewed = [], [], 0
    for task_id in task_ids:
        admitted = tuple(
            review
            for review in reviews
            if review.task_id == task_id
            and review.review_id.strip()
            and review.reviewer_id.strip()
            and review.declared_expertise.strip()
            and review.provenance.strip()
            and review.independently_classified
            and review.blinded_to_authored_key
            and review.blinded_to_peer_reviews
        )
        if any(
            not (review.expected_decision_agrees and review.prompt_unambiguous)
            for review in admitted
        ):
            revision.append(task_id)
        elif len({review.reviewer_id for review in admitted}) < 2:
            needs_review.append(task_id)
        else:
            reviewed += 1
    status = (
        "revision_required"
        if revision
        else "additional_review_required"
        if needs_review
        else "ready_for_pilot"
    )
    return NetworkAdmissionKeyAudit(
        status,
        len(task_ids),
        reviewed,
        tuple(needs_review),
        tuple(revision),
    )


def validate_disjoint_network_cohorts(
    recognition: tuple[NetworkAdmissionObservation, ...],
    execution: tuple[object, ...],
) -> None:
    """Prevent recognition vocabulary from priming the matched execution cohort."""

    recognition_ids = {item.participant_id for item in recognition}
    execution_ids = {item.participant_id for item in execution}
    overlap = tuple(sorted(recognition_ids & execution_ids))
    if overlap:
        raise ValueError(
            "Network recognition and execution cohorts must be disjoint; "
            f"overlap={overlap!r}."
        )

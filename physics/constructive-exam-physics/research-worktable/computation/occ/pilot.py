"""Preflight evidence for the selective micro-tool learner pilot."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from .micro_study import (
    DIAGNOSIS_ROUTES,
    MICRO_STUDY_PHASES,
    MicroToolObservation,
    MicroToolPair,
    RouteRecognitionObservation,
    RouteRecognitionSchedule,
    RouteRecognitionTask,
    construct_micro_tool_outcomes,
    validate_disjoint_micro_tool_cohorts,
)


ROUTE_KEY_REVIEW_COLUMNS = (
    "review_id",
    "reviewer_id",
    "task_id",
    "selected_route",
    "rationale",
    "provenance",
)
ROUTE_KEY_REVIEWER_COLUMNS = (
    "reviewer_id",
    "sequence_id",
    "expertise_domain",
    "authored_key_blinded",
    "peer_reviews_blinded",
    "provenance",
)


@dataclass(frozen=True)
class RouteKeyReview:
    review_id: str
    reviewer_id: str
    task_id: str
    selected_route: str
    rationale: str
    provenance: str


@dataclass(frozen=True)
class RouteKeyReviewer:
    reviewer_id: str
    sequence_id: str
    expertise_domain: str
    authored_key_blinded: bool
    peer_reviews_blinded: bool
    provenance: str

    @property
    def admitted(self) -> bool:
        return self.authored_key_blinded and self.peer_reviews_blinded


@dataclass(frozen=True)
class RouteKeyAudit:
    task_id: str
    expected_route: str
    status: str
    reviewer_count: int
    excluded_review_count: int
    selected_routes: tuple[str, ...]


@dataclass(frozen=True)
class RouteKeyPreflight:
    status: str
    admitted_task_ids: tuple[str, ...]
    needs_review_task_ids: tuple[str, ...]
    revision_task_ids: tuple[str, ...]


@dataclass(frozen=True)
class MicroPilotSummary:
    status: str
    route_key_agreed_tasks: int
    route_key_blocked_tasks: int
    recognition_participants: int
    recognition_rows: int
    recognition_scored_rows: int
    recognition_correct_rows: int
    execution_participants: int
    execution_rows: int
    execution_correct_rows: int
    execution_route_adherent_rows: int
    phase_reliable_rows: int
    eligible_pairs: int
    operator_faster_pairs: int
    operator_slower_pairs: int
    tied_pairs: int
    speed_disposition: str


@dataclass(frozen=True)
class MicroPilotPhaseDiagnostics:
    phase: str
    participant_count: int
    observed_rows: int
    direct_attempts: int
    operator_attempts: int
    direct_correct: int
    operator_correct: int
    complete_attempts: int
    adherent_attempts: int
    reliable_timing_attempts: int
    expected_pair_slots: int
    eligible_pairs: int
    ineligible_pairs: int
    missing_pairs: int
    complete_timing_clusters: int
    mean_cluster_time_delta: Fraction | None
    sample_variance_cluster_time_delta: Fraction | None
    reliable_phase_clusters: int
    mean_cluster_phase_deltas: tuple[Fraction, Fraction, Fraction, Fraction] | None
    maximum_variant_route_imbalance: int
    unobserved_variants: int


@dataclass(frozen=True)
class MicroPilotDiagnostics:
    status: str
    phases: tuple[MicroPilotPhaseDiagnostics, ...]


def load_route_key_review_tsv(
    path: Path,
    tasks: tuple[RouteRecognitionTask, ...],
) -> tuple[RouteKeyReview, ...]:
    """Load independent route-key judgments against the authored task set."""

    task_ids = {task.task_id for task in tasks}
    if len(task_ids) != len(tasks):
        raise ValueError("Recognition task ids must be unique.")
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != ROUTE_KEY_REVIEW_COLUMNS:
            raise ValueError("Route-key TSV columns do not match the frozen schema.")
        reviews = []
        for row in reader:
            task_id = row["task_id"].strip()
            if task_id not in task_ids:
                raise ValueError(f"Unknown route-key task {task_id!r}.")
            selected_route = row["selected_route"].strip()
            if selected_route not in DIAGNOSIS_ROUTES:
                raise ValueError(f"Unknown route-key selection {selected_route!r}.")
            review = RouteKeyReview(
                review_id=row["review_id"].strip(),
                reviewer_id=row["reviewer_id"].strip(),
                task_id=task_id,
                selected_route=selected_route,
                rationale=row["rationale"].strip(),
                provenance=row["provenance"].strip(),
            )
            if any(
                not getattr(review, field)
                for field in ("review_id", "reviewer_id", "rationale", "provenance")
            ):
                raise ValueError(
                    "Route-key identity, rationale, and provenance are required."
                )
            reviews.append(review)

    for field_name, values in (
        ("review id", [review.review_id for review in reviews]),
        (
            "reviewer task",
            [(review.reviewer_id, review.task_id) for review in reviews],
        ),
    ):
        if len(values) != len(set(values)):
            raise ValueError(f"Duplicate route-key {field_name}.")
    return tuple(reviews)


def _parse_bool(value: str, column: str) -> bool:
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ValueError(f"{column} must be true or false.")


def load_route_key_reviewer_tsv(
    path: Path,
    schedules: tuple[RouteRecognitionSchedule, ...],
) -> tuple[RouteKeyReviewer, ...]:
    """Load reviewer-level qualification and blinding witnesses."""

    sequence_ids = {schedule.sequence_id for schedule in schedules}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != ROUTE_KEY_REVIEWER_COLUMNS:
            raise ValueError("Route-key reviewer columns do not match the schema.")
        reviewers = []
        for row in reader:
            sequence_id = row["sequence_id"].strip()
            if sequence_id not in sequence_ids:
                raise ValueError(f"Unknown reviewer sequence {sequence_id!r}.")
            reviewer = RouteKeyReviewer(
                reviewer_id=row["reviewer_id"].strip(),
                sequence_id=sequence_id,
                expertise_domain=row["expertise_domain"].strip(),
                authored_key_blinded=_parse_bool(
                    row["authored_key_blinded"], "authored_key_blinded"
                ),
                peer_reviews_blinded=_parse_bool(
                    row["peer_reviews_blinded"], "peer_reviews_blinded"
                ),
                provenance=row["provenance"].strip(),
            )
            if any(
                not getattr(reviewer, field)
                for field in ("reviewer_id", "expertise_domain", "provenance")
            ):
                raise ValueError(
                    "Reviewer identity, expertise, and provenance are required."
                )
            reviewers.append(reviewer)
    reviewer_ids = [reviewer.reviewer_id for reviewer in reviewers]
    if len(reviewer_ids) != len(set(reviewer_ids)):
        raise ValueError("Route-key reviewer ids must be unique.")
    return tuple(reviewers)


def audit_route_key(
    tasks: tuple[RouteRecognitionTask, ...],
    reviews: tuple[RouteKeyReview, ...],
    reviewers: tuple[RouteKeyReviewer, ...],
    *,
    minimum_reviewers: int = 2,
) -> tuple[RouteKeyAudit, ...]:
    """Classify key agreement without treating absent review as support."""

    if minimum_reviewers < 2:
        raise ValueError("Route-key ambiguity requires at least two reviewers.")
    task_by_id = {task.task_id: task for task in tasks}
    if len(task_by_id) != len(tasks):
        raise ValueError("Recognition task ids must be unique.")
    reviewer_by_id = {reviewer.reviewer_id: reviewer for reviewer in reviewers}
    if len(reviewer_by_id) != len(reviewers):
        raise ValueError("Route-key reviewer ids must be unique.")
    grouped = {task_id: [] for task_id in task_by_id}
    for review in reviews:
        if review.task_id not in grouped:
            raise ValueError(f"Unknown reviewed task {review.task_id!r}.")
        grouped[review.task_id].append(review)

    audits = []
    for task in tasks:
        all_task_reviews = grouped[task.task_id]
        task_reviews = [
            review
            for review in all_task_reviews
            if review.reviewer_id in reviewer_by_id
            and reviewer_by_id[review.reviewer_id].admitted
        ]
        excluded_review_count = len(all_task_reviews) - len(task_reviews)
        selected_routes = tuple(
            sorted({review.selected_route for review in task_reviews})
        )
        if not task_reviews and excluded_review_count:
            status = "protocol_invalid"
        elif not task_reviews:
            status = "unreviewed"
        elif len(task_reviews) < minimum_reviewers:
            status = "insufficient_review"
        elif len(selected_routes) > 1:
            status = "ambiguous"
        elif selected_routes == (task.expected_route,):
            status = "agreed"
        else:
            status = "key_disputed"
        audits.append(
            RouteKeyAudit(
                task_id=task.task_id,
                expected_route=task.expected_route,
                status=status,
                reviewer_count=len(task_reviews),
                excluded_review_count=excluded_review_count,
                selected_routes=selected_routes,
            )
        )
    return tuple(audits)


def evaluate_route_key_preflight(
    tasks: tuple[RouteRecognitionTask, ...],
    audits: tuple[RouteKeyAudit, ...],
) -> RouteKeyPreflight:
    """Apply frozen consequences before learner outcomes can influence the key."""

    task_ids = tuple(task.task_id for task in tasks)
    audit_by_id = {audit.task_id: audit for audit in audits}
    if not task_ids or len(set(task_ids)) != len(task_ids):
        raise ValueError("Preflight tasks must be nonempty and unique.")
    if len(audit_by_id) != len(audits) or set(audit_by_id) != set(task_ids):
        raise ValueError("Preflight requires exactly one audit for every task.")
    review_statuses = {"unreviewed", "protocol_invalid", "insufficient_review"}
    revision_statuses = {"ambiguous", "key_disputed"}
    known_statuses = review_statuses | revision_statuses | {"agreed"}
    unknown_statuses = {
        audit.status for audit in audits if audit.status not in known_statuses
    }
    if unknown_statuses:
        raise ValueError(f"Unknown route-key audit statuses: {unknown_statuses!r}.")

    admitted = tuple(
        task_id for task_id in task_ids if audit_by_id[task_id].status == "agreed"
    )
    needs_review = tuple(
        task_id
        for task_id in task_ids
        if audit_by_id[task_id].status in review_statuses
    )
    revision = tuple(
        task_id
        for task_id in task_ids
        if audit_by_id[task_id].status in revision_statuses
    )
    if revision:
        status = "contract_revision_required"
    elif needs_review:
        status = "additional_review_required"
    else:
        status = "ready_for_learner_pilot"
    return RouteKeyPreflight(status, admitted, needs_review, revision)


def _fraction_mean(values: tuple[Fraction, ...]) -> Fraction:
    return sum(values, start=Fraction(0)) / len(values)


def construct_micro_pilot_diagnostics(
    observations: tuple[MicroToolObservation, ...],
    pairs: tuple[MicroToolPair, ...],
) -> MicroPilotDiagnostics:
    """Construct participant-clustered pilot inputs without a benefit verdict."""

    pair_by_id = {pair.pair_id: pair for pair in pairs}
    if len(pair_by_id) != len(pairs):
        raise ValueError("Pilot diagnostic pair ids must be unique.")
    phase_pairs = {
        phase: tuple(pair for pair in pairs if pair.phase == phase)
        for phase in MICRO_STUDY_PHASES
    }
    if not all(phase_pairs.values()):
        raise ValueError("Pilot diagnostics require pairs in every study phase.")
    for phase, items in phase_pairs.items():
        families = tuple(pair.family_id for pair in items)
        if len(families) != len(set(families)):
            raise ValueError(f"Pilot phase {phase!r} contains duplicate families.")
    variant_ids = tuple(
        variant.variant_id
        for pair in pairs
        for variant in (pair.variant_a, pair.variant_b)
    )
    if len(variant_ids) != len(set(variant_ids)):
        raise ValueError("Pilot diagnostic variant ids must be unique.")

    observation_by_id = {item.observation_id: item for item in observations}
    if len(observation_by_id) != len(observations):
        raise ValueError("Pilot diagnostic observation ids must be unique.")
    for item in observations:
        pair = pair_by_id.get(item.pair_id)
        if pair is None:
            raise ValueError(f"Unknown diagnostic pair {item.pair_id!r}.")
        if item.phase != pair.phase:
            raise ValueError("Diagnostic observation phase conflicts with its pair.")
        if item.variant_id not in {
            pair.variant_a.variant_id,
            pair.variant_b.variant_id,
        }:
            raise ValueError("Diagnostic observation names a variant outside its pair.")
        if item.assigned_route not in {"direct", pair.operator_route}:
            raise ValueError("Diagnostic observation has an invalid assigned route.")

    outcomes = construct_micro_tool_outcomes(observations, pairs)
    outcome_by_key = {
        (item.participant_id, item.phase, item.pair_id): item for item in outcomes
    }
    component_fields = (
        "interpretation_seconds",
        "setup_seconds",
        "computation_seconds",
        "return_seconds",
    )
    diagnostics = []
    for phase in MICRO_STUDY_PHASES:
        rows = tuple(item for item in observations if item.phase == phase)
        participants = tuple(sorted({item.participant_id for item in rows}))
        pairs_in_phase = phase_pairs[phase]
        pair_ids = tuple(pair.pair_id for pair in pairs_in_phase)
        phase_outcomes = tuple(item for item in outcomes if item.phase == phase)
        expected_pair_slots = len(participants) * len(pair_ids)
        cluster_deltas = []
        reliable_cluster_deltas = []
        for participant_id in participants:
            cluster = tuple(
                outcome_by_key.get((participant_id, phase, pair_id))
                for pair_id in pair_ids
            )
            if any(item is None or item.status != "eligible" for item in cluster):
                continue
            admitted_cluster = tuple(item for item in cluster if item is not None)
            deltas = tuple(item.time_delta for item in admitted_cluster)
            if any(delta is None for delta in deltas):
                raise ValueError("Eligible pilot timing pairs require time deltas.")
            cluster_deltas.append(
                _fraction_mean(tuple(delta for delta in deltas if delta is not None))
            )

            observation_pairs = tuple(
                (
                    observation_by_id[item.direct_observation_id],
                    observation_by_id[item.operator_observation_id],
                )
                for item in admitted_cluster
                if item.direct_observation_id is not None
                and item.operator_observation_id is not None
            )
            if len(observation_pairs) != len(pair_ids) or not all(
                direct.phase_timing_reliable and operator.phase_timing_reliable
                for direct, operator in observation_pairs
            ):
                continue
            reliable_cluster_deltas.append(
                tuple(
                    _fraction_mean(
                        tuple(
                            getattr(operator, field) - getattr(direct, field)
                            for direct, operator in observation_pairs
                        )
                    )
                    for field in component_fields
                )
            )

        cluster_delta_tuple = tuple(cluster_deltas)
        cluster_mean = (
            _fraction_mean(cluster_delta_tuple) if cluster_delta_tuple else None
        )
        cluster_variance = None
        if len(cluster_delta_tuple) >= 2 and cluster_mean is not None:
            cluster_variance = sum(
                ((value - cluster_mean) ** 2 for value in cluster_delta_tuple),
                start=Fraction(0),
            ) / (len(cluster_delta_tuple) - 1)
        phase_delta_mean = None
        if reliable_cluster_deltas:
            phase_delta_mean = tuple(
                _fraction_mean(
                    tuple(vector[index] for vector in reliable_cluster_deltas)
                )
                for index in range(len(component_fields))
            )

        phase_variant_ids = tuple(
            variant.variant_id
            for pair in pairs_in_phase
            for variant in (pair.variant_a, pair.variant_b)
        )
        variant_counts = {
            variant_id: (
                sum(
                    item.variant_id == variant_id and item.assigned_route == "direct"
                    for item in rows
                ),
                sum(
                    item.variant_id == variant_id and item.assigned_route != "direct"
                    for item in rows
                ),
            )
            for variant_id in phase_variant_ids
        }
        diagnostics.append(
            MicroPilotPhaseDiagnostics(
                phase=phase,
                participant_count=len(participants),
                observed_rows=len(rows),
                direct_attempts=sum(item.assigned_route == "direct" for item in rows),
                operator_attempts=sum(item.assigned_route != "direct" for item in rows),
                direct_correct=sum(
                    item.assigned_route == "direct" and item.correct for item in rows
                ),
                operator_correct=sum(
                    item.assigned_route != "direct" and item.correct for item in rows
                ),
                complete_attempts=sum(item.completion == "complete" for item in rows),
                adherent_attempts=sum(item.route_adherent for item in rows),
                reliable_timing_attempts=sum(
                    item.phase_timing_reliable for item in rows
                ),
                expected_pair_slots=expected_pair_slots,
                eligible_pairs=sum(
                    item.status == "eligible" for item in phase_outcomes
                ),
                ineligible_pairs=sum(
                    item.status == "ineligible" for item in phase_outcomes
                ),
                missing_pairs=expected_pair_slots - len(phase_outcomes),
                complete_timing_clusters=len(cluster_delta_tuple),
                mean_cluster_time_delta=cluster_mean,
                sample_variance_cluster_time_delta=cluster_variance,
                reliable_phase_clusters=len(reliable_cluster_deltas),
                mean_cluster_phase_deltas=phase_delta_mean,
                maximum_variant_route_imbalance=max(
                    abs(direct - operator)
                    for direct, operator in variant_counts.values()
                ),
                unobserved_variants=sum(
                    direct + operator == 0
                    for direct, operator in variant_counts.values()
                ),
            )
        )

    phase_diagnostics = tuple(diagnostics)
    if not observations:
        status = "unobserved"
    elif all(item.complete_timing_clusters >= 2 for item in phase_diagnostics):
        status = "design_inputs_observed"
    else:
        status = "design_inputs_incomplete"
    return MicroPilotDiagnostics(status, phase_diagnostics)


def summarize_micro_pilot(
    tasks: tuple[RouteRecognitionTask, ...],
    key_audits: tuple[RouteKeyAudit, ...],
    recognition: tuple[RouteRecognitionObservation, ...],
    execution: tuple[MicroToolObservation, ...],
    pairs: tuple[MicroToolPair, ...],
) -> MicroPilotSummary:
    """Return descriptive counts without a confirmatory benefit decision."""

    validate_disjoint_micro_tool_cohorts(recognition, execution)
    task_ids = tuple(task.task_id for task in tasks)
    audit_by_id = {audit.task_id: audit for audit in key_audits}
    if len(audit_by_id) != len(key_audits) or set(audit_by_id) != set(task_ids):
        raise ValueError("Pilot summary requires exactly one audit for every task.")
    agreed_ids = {audit.task_id for audit in key_audits if audit.status == "agreed"}
    scored = tuple(item for item in recognition if item.task_id in agreed_ids)
    outcomes = construct_micro_tool_outcomes(execution, pairs)
    eligible = tuple(item for item in outcomes if item.status == "eligible")
    deltas = tuple(item.time_delta for item in eligible)
    if any(delta is None for delta in deltas):
        raise ValueError("Eligible micro-tool outcomes require a time difference.")
    return MicroPilotSummary(
        status="descriptive_only" if recognition or execution else "unobserved",
        route_key_agreed_tasks=len(agreed_ids),
        route_key_blocked_tasks=len(tasks) - len(agreed_ids),
        recognition_participants=len({item.participant_id for item in recognition}),
        recognition_rows=len(recognition),
        recognition_scored_rows=len(scored),
        recognition_correct_rows=sum(item.correct for item in scored),
        execution_participants=len({item.participant_id for item in execution}),
        execution_rows=len(execution),
        execution_correct_rows=sum(item.correct for item in execution),
        execution_route_adherent_rows=sum(item.route_adherent for item in execution),
        phase_reliable_rows=sum(item.phase_timing_reliable for item in execution),
        eligible_pairs=len(eligible),
        operator_faster_pairs=sum(delta < 0 for delta in deltas if delta is not None),
        operator_slower_pairs=sum(delta > 0 for delta in deltas if delta is not None),
        tied_pairs=sum(delta == 0 for delta in deltas if delta is not None),
        speed_disposition="not_evaluated",
    )

"""Strict TSV ingestion for the frozen network acquisition contract."""

from __future__ import annotations

import csv
from fractions import Fraction
from pathlib import Path

from sympy import sympify

from .network_study import (
    NETWORK_STUDY_COLUMNS,
    NETWORK_STUDY_REVIEW_COLUMNS,
    NetworkStudyObservation,
    NetworkStudyPair,
    NetworkStudyReview,
    NetworkStudySchedule,
    network_study_variant_map,
    solve_network_study_variant,
    validate_network_study_pairs,
)

_COMPLETION = frozenset({"complete", "timeout", "abandoned"})
_FAMILIARITY = frozenset({"unseen", "same_structure_seen"})
_ERRORS = frozenset(
    {"target", "law", "representation", "algebra", "sign", "unit", "return", "timeout"}
)


def _parse_bool(value: str, name: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "false"}:
        return normalized == "true"
    raise ValueError(f"{name} must be true or false.")


def load_network_study_observation_tsv(
    path: Path,
    pairs: tuple[NetworkStudyPair, ...],
    schedules: tuple[NetworkStudySchedule, ...],
) -> tuple[NetworkStudyObservation, ...]:
    """Restore assignments and exact correctness from a frozen network study."""

    validate_network_study_pairs(pairs)
    variants = network_study_variant_map(pairs)
    trials = {
        (schedule.sequence_id, trial.order): trial
        for schedule in schedules
        for trial in schedule.trials
    }
    answers = {
        key: solve_network_study_variant(value) for key, value in variants.items()
    }
    if any(item.status != "constructed" for item in answers.values()):
        raise ValueError("Every frozen study variant requires a constructed exact key.")
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != NETWORK_STUDY_COLUMNS:
            raise ValueError(
                "Network-study TSV columns do not match the frozen schema."
            )
        observations = [
            _restore_observation(row, trials, variants, answers) for row in reader
        ]
    _validate_observation_relations(observations)
    return tuple(observations)


def _restore_observation(row, trials, variants, answers) -> NetworkStudyObservation:
    key = (row["sequence_id"].strip(), int(row["trial_order"].strip()))
    if key not in trials:
        raise ValueError("Observation does not name a frozen schedule trial.")
    trial = trials[key]
    supplied = tuple(
        row[name].strip()
        for name in ("phase", "pair_id", "variant_id", "assigned_route")
    )
    expected = (trial.phase, trial.pair_id, trial.variant_id, trial.assigned_route)
    if supplied != expected:
        raise ValueError("Observation conflicts with the frozen schedule.")
    strip = _parse_bool(row["strip_available"], "strip_available")
    expected_strip = (
        trial.phase == "immediate_assisted" and trial.assigned_route == "sparse"
    )
    if strip != expected_strip:
        raise ValueError("Observation conflicts with frozen card visibility.")
    delay = Fraction(row["hours_since_immediate"].strip())
    if delay < 0 or (trial.phase == "immediate_assisted" and delay != 0):
        raise ValueError("Immediate work defines the zero-delay reference.")
    if trial.phase != "immediate_assisted" and delay <= 0:
        raise ValueError("Delayed and unseen work require a positive delay.")
    phase_times = tuple(
        Fraction(row[name].strip())
        for name in (
            "interpretation_seconds",
            "setup_seconds",
            "computation_seconds",
            "return_seconds",
        )
    )
    total = Fraction(row["independent_total_seconds"].strip())
    reliable = _parse_bool(row["phase_timing_reliable"], "phase_timing_reliable")
    if any(value < 0 for value in phase_times) or total <= 0:
        raise ValueError("Timing values must be nonnegative with a positive total.")
    if reliable and sum(phase_times) != total:
        raise ValueError("Reliable phase times must equal the independent total.")
    completion = row["completion"].strip()
    familiarity = row["prior_familiarity"].strip()
    if completion not in _COMPLETION or familiarity not in _FAMILIARITY:
        raise ValueError("Unknown completion or prior-familiarity value.")
    errors = tuple(
        value.strip() for value in row["error_codes"].split(";") if value.strip()
    )
    if len(errors) != len(set(errors)) or any(value not in _ERRORS for value in errors):
        raise ValueError("Unknown or duplicate network-study error code.")
    submitted = row["submitted_answer"].strip()
    return NetworkStudyObservation(
        row["observation_id"].strip(),
        row["participant_id"].strip(),
        row["session_id"].strip(),
        key[0],
        key[1],
        trial.phase,
        trial.pair_id,
        trial.variant_id,
        trial.assigned_route,
        strip,
        delay,
        *phase_times,
        total,
        reliable,
        completion,
        sympify(submitted) if submitted else None,
        answers[trial.variant_id].target_value,
        errors,
        _parse_bool(row["route_adherent"], "route_adherent"),
        familiarity,
        f"{variants[trial.variant_id].provenance}; {row['provenance'].strip()}",
    )


def _validate_observation_relations(
    observations: list[NetworkStudyObservation],
) -> None:
    ids = [item.observation_id for item in observations]
    slots = [
        (item.participant_id, item.sequence_id, item.trial_order)
        for item in observations
    ]
    if len(ids) != len(set(ids)) or len(slots) != len(set(slots)):
        raise ValueError("Duplicate network-study observation or participant trial.")
    if any(
        not value.strip()
        for item in observations
        for value in (
            item.observation_id,
            item.participant_id,
            item.session_id,
            item.provenance,
        )
    ):
        raise ValueError("Observation identity and provenance must be nonempty.")
    for participant in {item.participant_id for item in observations}:
        rows = [item for item in observations if item.participant_id == participant]
        if len({item.sequence_id for item in rows}) != 1:
            raise ValueError("Each participant must use one network-study sequence.")
        phase_session, session_phase, phase_delay = {}, {}, {}
        for item in rows:
            phase_session.setdefault(item.phase, set()).add(item.session_id)
            session_phase.setdefault(item.session_id, set()).add(item.phase)
            phase_delay.setdefault(item.phase, set()).add(item.hours_since_immediate)
        relations = (
            *phase_session.values(),
            *session_phase.values(),
            *phase_delay.values(),
        )
        if any(len(value) != 1 for value in relations):
            raise ValueError("Each phase requires one distinct session and one delay.")
        if "delayed_same_topology" in phase_delay and "unseen_topology" in phase_delay:
            delayed = next(iter(phase_delay["delayed_same_topology"]))
            unseen = next(iter(phase_delay["unseen_topology"]))
            if unseen <= delayed:
                raise ValueError(
                    "Unseen-topology work must occur after delayed retention work."
                )


def load_network_study_review_tsv(
    path: Path, pairs: tuple[NetworkStudyPair, ...]
) -> tuple[NetworkStudyReview, ...]:
    variants = network_study_variant_map(pairs)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != NETWORK_STUDY_REVIEW_COLUMNS:
            raise ValueError(
                "Network-key review TSV columns do not match the frozen schema."
            )
        reviews = tuple(_restore_review(row) for row in reader)
    if any(item.variant_id not in variants for item in reviews):
        raise ValueError("Review names an unknown network-study variant.")
    ids = [item.review_id for item in reviews]
    slots = [(item.reviewer_id, item.variant_id) for item in reviews]
    if len(ids) != len(set(ids)) or len(slots) != len(set(slots)):
        raise ValueError(
            "Duplicate network-key review identity or reviewer/variant slot."
        )
    return reviews


def _restore_review(row) -> NetworkStudyReview:
    return NetworkStudyReview(
        row["review_id"].strip(),
        row["reviewer_id"].strip(),
        row["variant_id"].strip(),
        row["declared_expertise"].strip(),
        *(
            _parse_bool(row[name], name)
            for name in (
                "independently_solved",
                "blinded_to_authored_routes",
                "blinded_to_peer_reviews",
                "exact_answer_agrees",
                "direct_route_valid",
                "sparse_route_valid",
                "baseline_competent",
            )
        ),
        row["notes"].strip(),
        row["provenance"].strip(),
    )

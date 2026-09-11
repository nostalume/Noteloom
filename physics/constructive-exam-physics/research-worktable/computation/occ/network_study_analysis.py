"""Participant-clustered diagnostics and key preflight for network study data."""

from __future__ import annotations

from fractions import Fraction

from .network_study import (
    NETWORK_STUDY_PHASES,
    NetworkStudyDiagnostics,
    NetworkStudyKeyAudit,
    NetworkStudyObservation,
    NetworkStudyPair,
    NetworkStudyPhaseDiagnostics,
    NetworkStudyReview,
    network_study_variant_map,
    validate_network_study_pairs,
)


def construct_network_study_diagnostics(
    observations: tuple[NetworkStudyObservation, ...],
    pairs: tuple[NetworkStudyPair, ...],
) -> NetworkStudyDiagnostics:
    """Cluster eligible time differences by participant without a benefit verdict."""

    validate_network_study_pairs(pairs)
    pair_by_id = {item.pair_id: item for item in pairs}
    grouped = {}
    for item in observations:
        if item.pair_id not in pair_by_id:
            raise ValueError("Observation names an unknown network-study pair.")
        pair = pair_by_id[item.pair_id]
        if item.phase != pair.phase or item.variant_id not in {
            pair.variant_a.variant_id,
            pair.variant_b.variant_id,
        }:
            raise ValueError("Observation conflicts with its network-study pair.")
        grouped.setdefault((item.participant_id, item.phase, item.pair_id), []).append(
            item
        )
    diagnostics = tuple(
        _diagnose_phase(phase, observations, pairs, grouped)
        for phase in NETWORK_STUDY_PHASES
    )
    if not observations:
        status = "unobserved"
    elif all(item.complete_participant_clusters >= 2 for item in diagnostics):
        status = "design_inputs_observed"
    else:
        status = "incomplete_design_inputs"
    return NetworkStudyDiagnostics(status, diagnostics)


def _diagnose_phase(phase, observations, pairs, grouped):
    phase_pairs = tuple(item for item in pairs if item.phase == phase)
    rows = tuple(item for item in observations if item.phase == phase)
    participants = tuple(sorted({item.participant_id for item in rows}))
    eligible, ineligible = {}, 0
    for key, items in grouped.items():
        if key[1] != phase:
            continue
        by_route = {item.assigned_route: item for item in items}
        direct, sparse = by_route.get("direct"), by_route.get("sparse")
        if (
            len(items) == 2
            and direct is not None
            and sparse is not None
            and direct.correct
            and sparse.correct
            and direct.route_adherent
            and sparse.route_adherent
        ):
            eligible[key] = sparse.total_seconds - direct.total_seconds
        else:
            ineligible += 1
    clusters = []
    for participant in participants:
        values = [
            eligible.get((participant, phase, pair.pair_id)) for pair in phase_pairs
        ]
        if all(value is not None for value in values):
            clusters.append(sum(values, Fraction()) / len(values))
    mean = sum(clusters, Fraction()) / len(clusters) if clusters else None
    variance = None
    if len(clusters) >= 2:
        variance = sum((value - mean) ** 2 for value in clusters) / (len(clusters) - 1)
    return NetworkStudyPhaseDiagnostics(
        phase,
        len(participants),
        len(rows),
        sum(item.assigned_route == "direct" and item.correct for item in rows),
        sum(item.assigned_route == "sparse" and item.correct for item in rows),
        len(eligible),
        ineligible,
        len(clusters),
        mean,
        variance,
    )


def audit_network_study_key(
    reviews: tuple[NetworkStudyReview, ...], pairs: tuple[NetworkStudyPair, ...]
) -> NetworkStudyKeyAudit:
    """Require two independent blinded positive reviews for every variant."""

    variants = tuple(network_study_variant_map(pairs))
    needs_review, revision, reviewed = [], [], 0
    for variant_id in variants:
        admitted = tuple(
            item
            for item in reviews
            if item.variant_id == variant_id
            and item.independently_solved
            and item.blinded_to_authored_routes
            and item.blinded_to_peer_reviews
            and item.review_id.strip()
            and item.reviewer_id.strip()
            and item.declared_expertise.strip()
            and item.provenance.strip()
        )
        if any(
            not all(
                (
                    item.exact_answer_agrees,
                    item.direct_route_valid,
                    item.sparse_route_valid,
                    item.baseline_competent,
                )
            )
            for item in admitted
        ):
            revision.append(variant_id)
        elif len({item.reviewer_id for item in admitted}) < 2:
            needs_review.append(variant_id)
        else:
            reviewed += 1
    status = (
        "revision_required"
        if revision
        else "additional_review_required"
        if needs_review
        else "ready_for_pilot"
    )
    return NetworkStudyKeyAudit(
        status, len(variants), reviewed, tuple(needs_review), tuple(revision)
    )

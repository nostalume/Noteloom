"""Matched-variant study objects and observation ingestion."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from sympy import Expr

from .calibration import PairedRouteObservation
from .cost import AdmissionBoundary, construct_admission_boundary


STUDY_ROLES = frozenset({"calibration", "holdout"})
ROUTES = frozenset({"direct", "proposed"})
OBSERVATION_COLUMNS = (
    "sample_id",
    "participant_id",
    "session_id",
    "problem_id",
    "direct_variant_id",
    "proposed_variant_id",
    "direct_seconds",
    "proposed_seconds",
    "direct_correct",
    "proposed_correct",
    "route_order",
    "provenance",
)


@dataclass(frozen=True)
class StudyVariant:
    variant_id: str
    prompt: str
    regime: str
    answers: tuple[tuple[str, Expr], ...]

    def __post_init__(self) -> None:
        if (
            not self.variant_id.strip()
            or not self.prompt.strip()
            or not self.regime.strip()
        ):
            raise ValueError("A study variant requires an id, prompt, and regime.")
        names = tuple(name for name, _ in self.answers)
        if not names or any(not name.strip() for name in names):
            raise ValueError("A study variant requires named answers.")
        if len(names) != len(set(names)):
            raise ValueError("Study-variant answer names must be unique.")

    def answer(self, name: str) -> Expr:
        for answer_name, value in self.answers:
            if answer_name == name:
                return value
        raise KeyError(name)


@dataclass(frozen=True)
class MatchedVariantPair:
    pair_id: str
    source_problem_id: str
    pdf_page: int
    study_role: str
    variant_a: StudyVariant
    variant_b: StudyVariant
    boundary: AdmissionBoundary
    provenance: str

    def __post_init__(self) -> None:
        if not self.pair_id.strip() or not self.source_problem_id.strip():
            raise ValueError("A matched pair requires pair and source-problem ids.")
        if self.pdf_page < 1:
            raise ValueError("A matched pair requires a positive PDF page.")
        if self.study_role not in STUDY_ROLES:
            raise ValueError(f"Unknown study role {self.study_role!r}.")
        if self.variant_a.variant_id == self.variant_b.variant_id:
            raise ValueError("Matched variants require distinct ids.")
        if not self.provenance.strip():
            raise ValueError("A matched pair requires provenance.")
        if self.boundary.baseline.problem_id != self.source_problem_id:
            raise ValueError("Matched-pair boundary must belong to its source problem.")
        if self.boundary != construct_admission_boundary(
            self.boundary.baseline,
            self.boundary.proposed,
        ):
            raise ValueError("Matched-pair boundary must be derived from its routes.")


@dataclass(frozen=True)
class StudyTrial:
    order: int
    pair_id: str
    source_problem_id: str
    variant_id: str
    route: str
    study_role: str

    def __post_init__(self) -> None:
        if self.order < 1:
            raise ValueError("Study-trial order must be positive.")
        if self.route not in ROUTES:
            raise ValueError(f"Unknown study route {self.route!r}.")


@dataclass(frozen=True)
class CounterbalancedSchedule:
    sequence_id: str
    trials: tuple[StudyTrial, ...]


def _trial(
    order: int,
    pair: MatchedVariantPair,
    variant: StudyVariant,
    route: str,
) -> StudyTrial:
    return StudyTrial(
        order,
        pair.pair_id,
        pair.source_problem_id,
        variant.variant_id,
        route,
        pair.study_role,
    )


def build_two_sequence_schedule(
    pairs: tuple[MatchedVariantPair, ...],
) -> tuple[CounterbalancedSchedule, CounterbalancedSchedule]:
    """Construct a two-sequence route/order/variant counterbalance."""

    ids = tuple(pair.pair_id for pair in pairs)
    if len(ids) != len(set(ids)):
        raise ValueError("Matched-pair ids must be unique.")
    sequence_one_blocks: tuple[
        list[tuple[MatchedVariantPair, StudyVariant, str]], ...
    ] = (
        [],
        [],
    )
    sequence_two_blocks: tuple[
        list[tuple[MatchedVariantPair, StudyVariant, str]], ...
    ] = (
        [],
        [],
    )
    for index, pair in enumerate(pairs):
        if index % 2 == 0:
            s1_first = (pair.variant_a, "direct")
            s1_second = (pair.variant_b, "proposed")
            s2_first = (pair.variant_a, "proposed")
            s2_second = (pair.variant_b, "direct")
        else:
            s1_first = (pair.variant_b, "proposed")
            s1_second = (pair.variant_a, "direct")
            s2_first = (pair.variant_b, "direct")
            s2_second = (pair.variant_a, "proposed")
        sequence_one_blocks[0].append((pair, *s1_first))
        sequence_one_blocks[1].append((pair, *s1_second))
        sequence_two_blocks[0].append((pair, *s2_first))
        sequence_two_blocks[1].append((pair, *s2_second))

    def assemble(
        blocks: tuple[list[tuple[MatchedVariantPair, StudyVariant, str]], ...],
    ) -> tuple[StudyTrial, ...]:
        assignments = blocks[0] + blocks[1]
        return tuple(
            _trial(order, pair, variant, route)
            for order, (pair, variant, route) in enumerate(assignments, start=1)
        )

    return (
        CounterbalancedSchedule("S1", assemble(sequence_one_blocks)),
        CounterbalancedSchedule("S2", assemble(sequence_two_blocks)),
    )


def _parse_bool(value: str, column: str) -> bool:
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ValueError(f"{column} must be true or false.")


def load_paired_observation_tsv(
    path: Path,
    pairs: tuple[MatchedVariantPair, ...],
) -> tuple[PairedRouteObservation, ...]:
    """Load completed study rows and restore their derived route boundaries."""

    pair_by_problem = {pair.source_problem_id: pair for pair in pairs}
    if len(pair_by_problem) != len(pairs):
        raise ValueError("Study pairs require unique source problem ids.")
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != OBSERVATION_COLUMNS:
            raise ValueError("Observation TSV columns do not match the study schema.")
        observations = []
        for row in reader:
            problem_id = row["problem_id"].strip()
            if problem_id not in pair_by_problem:
                raise ValueError(f"Unknown study problem id {problem_id!r}.")
            pair = pair_by_problem[problem_id]
            supplied_variants = {
                row["direct_variant_id"].strip(),
                row["proposed_variant_id"].strip(),
            }
            expected_variants = {
                pair.variant_a.variant_id,
                pair.variant_b.variant_id,
            }
            if supplied_variants != expected_variants:
                raise ValueError(
                    "Direct and proposed attempts must use the two distinct matched variants."
                )
            route_order = row["route_order"].strip()
            if route_order not in {"direct_then_proposed", "proposed_then_direct"}:
                raise ValueError("route_order is not a declared counterbalanced order.")
            provenance = (
                f"participant={row['participant_id'].strip()}; "
                f"session={row['session_id'].strip()}; "
                f"pair={pair.pair_id}; source={pair.provenance}; "
                f"observation={row['provenance'].strip()}"
            )
            observations.append(
                PairedRouteObservation(
                    sample_id=row["sample_id"].strip(),
                    problem_id=problem_id,
                    boundary=pair.boundary,
                    direct_seconds=Fraction(row["direct_seconds"].strip()),
                    proposed_seconds=Fraction(row["proposed_seconds"].strip()),
                    direct_correct=_parse_bool(row["direct_correct"], "direct_correct"),
                    proposed_correct=_parse_bool(
                        row["proposed_correct"], "proposed_correct"
                    ),
                    provenance=provenance,
                    order_control=route_order,
                    participant_id=row["participant_id"].strip(),
                    session_id=row["session_id"].strip(),
                )
            )
    return tuple(observations)

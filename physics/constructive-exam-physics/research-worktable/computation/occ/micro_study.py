"""Phase-aware observations for a selective handwritten micro-tool study."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from .study import StudyVariant


MICRO_STUDY_PHASES = ("assisted", "internalized", "delayed_unseen")
MICRO_TOOL_ROUTES = frozenset({"direct", "slice", "projection", "path", "product"})
DIAGNOSIS_ROUTES = MICRO_TOOL_ROUTES | frozenset(
    {"event", "harmonic", "symmetry", "refuse-card"}
)
COMPLETION_STATUSES = frozenset({"complete", "timeout", "abandoned"})
PRIOR_FAMILIARITIES = frozenset({"unseen", "same_structure_seen"})
MICRO_ERROR_CODES = frozenset(
    {
        "target",
        "law",
        "representation",
        "algebra",
        "branch",
        "sign",
        "unit",
        "return",
        "timeout",
    }
)
MICRO_OBSERVATION_COLUMNS = (
    "observation_id",
    "participant_id",
    "session_id",
    "sequence_id",
    "trial_order",
    "phase",
    "pair_id",
    "variant_id",
    "assigned_route",
    "card_available",
    "hours_since_assisted",
    "interpretation_seconds",
    "setup_seconds",
    "computation_seconds",
    "return_seconds",
    "independent_total_seconds",
    "phase_timing_reliable",
    "completion",
    "correct",
    "error_codes",
    "route_adherent",
    "prior_familiarity",
    "provenance",
)
RECOGNITION_OBSERVATION_COLUMNS = (
    "observation_id",
    "participant_id",
    "session_id",
    "sequence_id",
    "task_order",
    "task_id",
    "selected_route",
    "decision_seconds",
    "provenance",
)


@dataclass(frozen=True)
class MicroToolPair:
    pair_id: str
    family_id: str
    phase: str
    card_id: str
    operator_route: str
    variant_a: StudyVariant
    variant_b: StudyVariant
    provenance: str

    def __post_init__(self) -> None:
        for label in ("pair_id", "family_id", "card_id", "provenance"):
            if not getattr(self, label).strip():
                raise ValueError(f"{label} must be nonempty.")
        if self.phase not in MICRO_STUDY_PHASES:
            raise ValueError(f"Unknown micro-study phase {self.phase!r}.")
        if self.operator_route not in MICRO_TOOL_ROUTES - {"direct"}:
            raise ValueError(f"Unknown micro-tool route {self.operator_route!r}.")
        if self.variant_a.variant_id == self.variant_b.variant_id:
            raise ValueError("A micro-tool pair requires two distinct variants.")


@dataclass(frozen=True)
class MicroToolTrial:
    order: int
    phase: str
    pair_id: str
    variant_id: str
    assigned_route: str


@dataclass(frozen=True)
class MicroToolSchedule:
    sequence_id: str
    trials: tuple[MicroToolTrial, ...]


@dataclass(frozen=True)
class MicroToolObservation:
    observation_id: str
    participant_id: str
    session_id: str
    sequence_id: str
    trial_order: int
    phase: str
    pair_id: str
    variant_id: str
    assigned_route: str
    card_available: bool
    hours_since_assisted: Fraction
    interpretation_seconds: Fraction
    setup_seconds: Fraction
    computation_seconds: Fraction
    return_seconds: Fraction
    independent_total_seconds: Fraction
    phase_timing_reliable: bool
    completion: str
    correct: bool
    error_codes: tuple[str, ...]
    route_adherent: bool
    prior_familiarity: str
    provenance: str

    @property
    def total_seconds(self) -> Fraction:
        return self.independent_total_seconds


@dataclass(frozen=True)
class MicroToolOutcome:
    participant_id: str
    phase: str
    pair_id: str
    family_id: str
    status: str
    reason: str
    direct_observation_id: str | None
    operator_observation_id: str | None
    time_delta: Fraction | None


@dataclass(frozen=True)
class RouteRecognitionTask:
    task_id: str
    prompt: str
    expected_route: str
    provenance: str

    def __post_init__(self) -> None:
        for label in ("task_id", "prompt", "provenance"):
            if not getattr(self, label).strip():
                raise ValueError(f"{label} must be nonempty.")
        if self.expected_route not in DIAGNOSIS_ROUTES:
            raise ValueError(f"Unknown recognition route {self.expected_route!r}.")


@dataclass(frozen=True)
class RouteRecognitionSchedule:
    sequence_id: str
    task_ids: tuple[str, ...]


@dataclass(frozen=True)
class RouteRecognitionObservation:
    observation_id: str
    participant_id: str
    session_id: str
    sequence_id: str
    task_order: int
    task_id: str
    selected_route: str
    expected_route: str
    decision_seconds: Fraction
    provenance: str

    @property
    def correct(self) -> bool:
        return self.selected_route == self.expected_route


def _trial(
    order: int,
    pair: MicroToolPair,
    variant: StudyVariant,
    route: str,
) -> MicroToolTrial:
    return MicroToolTrial(order, pair.phase, pair.pair_id, variant.variant_id, route)


def build_micro_tool_schedules(
    pairs: tuple[MicroToolPair, ...],
) -> tuple[MicroToolSchedule, MicroToolSchedule]:
    """Counterbalance direct/operator routes independently inside three phases."""

    pair_ids = tuple(pair.pair_id for pair in pairs)
    if len(pair_ids) != len(set(pair_ids)):
        raise ValueError("Micro-tool pair ids must be unique.")
    phase_groups = {
        phase: tuple(pair for pair in pairs if pair.phase == phase)
        for phase in MICRO_STUDY_PHASES
    }
    family_sets = {
        phase: {pair.family_id for pair in group}
        for phase, group in phase_groups.items()
    }
    if (
        not all(phase_groups.values())
        or len({frozenset(items) for items in family_sets.values()}) != 1
    ):
        raise ValueError("Every micro-study phase must contain the same families.")
    if any(
        len(group) != len(family_sets[phase]) for phase, group in phase_groups.items()
    ):
        raise ValueError("Each phase requires one pair per micro-tool family.")

    sequence_blocks: dict[str, list[MicroToolTrial]] = {"M1": [], "M2": []}
    order_offsets = {"M1": 0, "M2": 0}
    for phase in MICRO_STUDY_PHASES:
        group = phase_groups[phase]
        first_blocks: dict[str, list[tuple[MicroToolPair, StudyVariant, str]]] = {
            "M1": [],
            "M2": [],
        }
        second_blocks: dict[str, list[tuple[MicroToolPair, StudyVariant, str]]] = {
            "M1": [],
            "M2": [],
        }
        for index, pair in enumerate(group):
            if index % 2 == 0:
                first_blocks["M1"].append((pair, pair.variant_a, "direct"))
                second_blocks["M1"].append((pair, pair.variant_b, pair.operator_route))
                first_blocks["M2"].append((pair, pair.variant_a, pair.operator_route))
                second_blocks["M2"].append((pair, pair.variant_b, "direct"))
            else:
                first_blocks["M1"].append((pair, pair.variant_b, pair.operator_route))
                second_blocks["M1"].append((pair, pair.variant_a, "direct"))
                first_blocks["M2"].append((pair, pair.variant_b, "direct"))
                second_blocks["M2"].append((pair, pair.variant_a, pair.operator_route))
        for sequence_id in ("M1", "M2"):
            assignments = first_blocks[sequence_id] + second_blocks[sequence_id]
            offset = order_offsets[sequence_id]
            sequence_blocks[sequence_id].extend(
                _trial(offset + index, pair, variant, route)
                for index, (pair, variant, route) in enumerate(assignments, start=1)
            )
            order_offsets[sequence_id] += len(assignments)

    return tuple(
        MicroToolSchedule(sequence_id, tuple(sequence_blocks[sequence_id]))
        for sequence_id in ("M1", "M2")
    )


def build_recognition_schedules(
    tasks: tuple[RouteRecognitionTask, ...],
) -> tuple[RouteRecognitionSchedule, RouteRecognitionSchedule]:
    """Counterbalance recognition order without exposing solution work."""

    task_ids = tuple(task.task_id for task in tasks)
    if not task_ids or len(task_ids) != len(set(task_ids)):
        raise ValueError("Recognition task ids must be nonempty and unique.")
    return (
        RouteRecognitionSchedule("R1", task_ids),
        RouteRecognitionSchedule("R2", tuple(reversed(task_ids))),
    )


def _parse_bool(value: str, column: str) -> bool:
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ValueError(f"{column} must be true or false.")


def _parse_errors(value: str) -> tuple[str, ...]:
    errors = tuple(code.strip() for code in value.split(";") if code.strip())
    if len(errors) != len(set(errors)):
        raise ValueError("Micro-study error codes must be unique.")
    unknown = tuple(code for code in errors if code not in MICRO_ERROR_CODES)
    if unknown:
        raise ValueError(f"Unknown micro-study error codes: {unknown!r}.")
    return errors


def load_micro_tool_observation_tsv(
    path: Path,
    pairs: tuple[MicroToolPair, ...],
    schedules: tuple[MicroToolSchedule, ...],
) -> tuple[MicroToolObservation, ...]:
    """Load partial or complete observations against frozen schedule assignments."""

    pair_by_id = {pair.pair_id: pair for pair in pairs}
    if len(pair_by_id) != len(pairs):
        raise ValueError("Micro-tool pair ids must be unique.")
    trial_by_key = {
        (schedule.sequence_id, trial.order): trial
        for schedule in schedules
        for trial in schedule.trials
    }
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != MICRO_OBSERVATION_COLUMNS:
            raise ValueError("Micro-study TSV columns do not match the frozen schema.")
        observations = []
        for row in reader:
            sequence_id = row["sequence_id"].strip()
            trial_order = int(row["trial_order"].strip())
            key = (sequence_id, trial_order)
            if key not in trial_by_key:
                raise ValueError("Observation does not name a frozen schedule trial.")
            trial = trial_by_key[key]
            supplied = (
                row["phase"].strip(),
                row["pair_id"].strip(),
                row["variant_id"].strip(),
                row["assigned_route"].strip(),
            )
            expected = (
                trial.phase,
                trial.pair_id,
                trial.variant_id,
                trial.assigned_route,
            )
            if supplied != expected:
                raise ValueError("Observation conflicts with the frozen schedule.")
            pair = pair_by_id[trial.pair_id]
            card_available = _parse_bool(row["card_available"], "card_available")
            expected_card = (
                trial.phase == "assisted" and trial.assigned_route != "direct"
            )
            if card_available != expected_card:
                raise ValueError("Observation conflicts with frozen card visibility.")
            hours_since_assisted = Fraction(row["hours_since_assisted"].strip())
            if hours_since_assisted < 0:
                raise ValueError("Hours since assisted work must be nonnegative.")
            if trial.phase == "assisted" and hours_since_assisted != 0:
                raise ValueError("Assisted trials define the zero-delay reference.")
            if trial.phase == "delayed_unseen" and hours_since_assisted <= 0:
                raise ValueError("A delayed-unseen trial requires a positive delay.")
            phase_times = tuple(
                Fraction(row[column].strip())
                for column in (
                    "interpretation_seconds",
                    "setup_seconds",
                    "computation_seconds",
                    "return_seconds",
                )
            )
            if any(value < 0 for value in phase_times):
                raise ValueError("Phase times must be nonnegative.")
            independent_total = Fraction(row["independent_total_seconds"].strip())
            if independent_total <= 0:
                raise ValueError("Independent total time must be positive.")
            phase_timing_reliable = _parse_bool(
                row["phase_timing_reliable"], "phase_timing_reliable"
            )
            if phase_timing_reliable and sum(phase_times) != independent_total:
                raise ValueError(
                    "Reliable phase times must equal the independent total."
                )
            completion = row["completion"].strip()
            if completion not in COMPLETION_STATUSES:
                raise ValueError(f"Unknown completion status {completion!r}.")
            correct = _parse_bool(row["correct"], "correct")
            errors = _parse_errors(row["error_codes"])
            if correct and (completion != "complete" or errors):
                raise ValueError(
                    "A correct attempt must be complete with no unresolved error."
                )
            familiarity = row["prior_familiarity"].strip()
            if familiarity not in PRIOR_FAMILIARITIES:
                raise ValueError(f"Unknown prior familiarity {familiarity!r}.")
            observations.append(
                MicroToolObservation(
                    observation_id=row["observation_id"].strip(),
                    participant_id=row["participant_id"].strip(),
                    session_id=row["session_id"].strip(),
                    sequence_id=sequence_id,
                    trial_order=trial_order,
                    phase=trial.phase,
                    pair_id=trial.pair_id,
                    variant_id=trial.variant_id,
                    assigned_route=trial.assigned_route,
                    card_available=card_available,
                    hours_since_assisted=hours_since_assisted,
                    interpretation_seconds=phase_times[0],
                    setup_seconds=phase_times[1],
                    computation_seconds=phase_times[2],
                    return_seconds=phase_times[3],
                    independent_total_seconds=independent_total,
                    phase_timing_reliable=phase_timing_reliable,
                    completion=completion,
                    correct=correct,
                    error_codes=errors,
                    route_adherent=_parse_bool(row["route_adherent"], "route_adherent"),
                    prior_familiarity=familiarity,
                    provenance=f"{pair.provenance}; {row['provenance'].strip()}",
                )
            )
    for field_name, values in (
        ("observation_id", [item.observation_id for item in observations]),
        (
            "participant schedule trial",
            [
                (item.participant_id, item.sequence_id, item.trial_order)
                for item in observations
            ],
        ),
    ):
        if len(values) != len(set(values)):
            raise ValueError(f"Duplicate micro-study {field_name}.")
    required_text = (
        "observation_id",
        "participant_id",
        "session_id",
        "provenance",
    )
    if any(
        not getattr(item, field).strip()
        for item in observations
        for field in required_text
    ):
        raise ValueError("Micro-study identity and provenance fields must be nonempty.")
    phase_sessions: dict[tuple[str, str], set[str]] = {}
    session_phases: dict[tuple[str, str], set[str]] = {}
    phase_delays: dict[tuple[str, str], set[Fraction]] = {}
    for item in observations:
        phase_sessions.setdefault((item.participant_id, item.phase), set()).add(
            item.session_id
        )
        session_phases.setdefault((item.participant_id, item.session_id), set()).add(
            item.phase
        )
        phase_delays.setdefault((item.participant_id, item.phase), set()).add(
            item.hours_since_assisted
        )
    if any(len(session_ids) != 1 for session_ids in phase_sessions.values()):
        raise ValueError("Each participant must use one session per phase.")
    if any(len(phases) != 1 for phases in session_phases.values()):
        raise ValueError("A participant session cannot span micro-study phases.")
    if any(len(delays) != 1 for delays in phase_delays.values()):
        raise ValueError("Each participant must record one delay per phase.")
    for participant_id in {item.participant_id for item in observations}:
        internalized = phase_delays.get((participant_id, "internalized"))
        delayed = phase_delays.get((participant_id, "delayed_unseen"))
        if internalized and delayed and next(iter(delayed)) <= next(iter(internalized)):
            raise ValueError(
                "Delayed-unseen work must occur later than internalized work."
            )
    participant_sequences: dict[str, set[str]] = {}
    for item in observations:
        participant_sequences.setdefault(item.participant_id, set()).add(
            item.sequence_id
        )
    if any(len(sequence_ids) != 1 for sequence_ids in participant_sequences.values()):
        raise ValueError("Each participant must use exactly one micro-study sequence.")
    return tuple(observations)


def load_route_recognition_observation_tsv(
    path: Path,
    tasks: tuple[RouteRecognitionTask, ...],
    schedules: tuple[RouteRecognitionSchedule, ...],
) -> tuple[RouteRecognitionObservation, ...]:
    """Load route decisions against frozen tasks without solution-route priming."""

    task_by_id = {task.task_id: task for task in tasks}
    if len(task_by_id) != len(tasks):
        raise ValueError("Recognition task ids must be unique.")
    scheduled_by_key = {
        (schedule.sequence_id, order): task_id
        for schedule in schedules
        for order, task_id in enumerate(schedule.task_ids, start=1)
    }
    if any(task_id not in task_by_id for task_id in scheduled_by_key.values()):
        raise ValueError("Recognition schedule names an unknown task.")

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != RECOGNITION_OBSERVATION_COLUMNS:
            raise ValueError("Recognition TSV columns do not match the frozen schema.")
        observations = []
        for row in reader:
            sequence_id = row["sequence_id"].strip()
            task_order = int(row["task_order"].strip())
            key = (sequence_id, task_order)
            if key not in scheduled_by_key:
                raise ValueError(
                    "Recognition row does not name a frozen task position."
                )
            task_id = row["task_id"].strip()
            if task_id != scheduled_by_key[key]:
                raise ValueError("Recognition row conflicts with the frozen schedule.")
            selected_route = row["selected_route"].strip()
            if selected_route not in DIAGNOSIS_ROUTES:
                raise ValueError(f"Unknown selected route {selected_route!r}.")
            decision_seconds = Fraction(row["decision_seconds"].strip())
            if decision_seconds <= 0:
                raise ValueError("Recognition decision time must be positive.")
            task = task_by_id[task_id]
            observations.append(
                RouteRecognitionObservation(
                    observation_id=row["observation_id"].strip(),
                    participant_id=row["participant_id"].strip(),
                    session_id=row["session_id"].strip(),
                    sequence_id=sequence_id,
                    task_order=task_order,
                    task_id=task_id,
                    selected_route=selected_route,
                    expected_route=task.expected_route,
                    decision_seconds=decision_seconds,
                    provenance=f"{task.provenance}; {row['provenance'].strip()}",
                )
            )

    for field_name, values in (
        ("observation_id", [item.observation_id for item in observations]),
        (
            "participant schedule task",
            [
                (item.participant_id, item.sequence_id, item.task_order)
                for item in observations
            ],
        ),
    ):
        if len(values) != len(set(values)):
            raise ValueError(f"Duplicate recognition {field_name}.")
    required_text = ("observation_id", "participant_id", "session_id", "provenance")
    if any(
        not getattr(item, field).strip()
        for item in observations
        for field in required_text
    ):
        raise ValueError("Recognition identity and provenance fields must be nonempty.")
    participant_sequences: dict[str, set[str]] = {}
    for item in observations:
        participant_sequences.setdefault(item.participant_id, set()).add(
            item.sequence_id
        )
    if any(len(sequence_ids) != 1 for sequence_ids in participant_sequences.values()):
        raise ValueError("Each participant must use exactly one recognition sequence.")
    return tuple(observations)


def validate_disjoint_micro_tool_cohorts(
    recognition: tuple[RouteRecognitionObservation, ...],
    execution: tuple[MicroToolObservation, ...],
) -> None:
    """Refuse undeclared training leakage between the two D3 instruments."""

    recognition_ids = {item.participant_id for item in recognition}
    execution_ids = {item.participant_id for item in execution}
    overlap = tuple(sorted(recognition_ids & execution_ids))
    if overlap:
        raise ValueError(
            "D3 recognition and execution require disjoint cohorts; "
            f"overlap={overlap!r}."
        )


def construct_micro_tool_outcomes(
    observations: tuple[MicroToolObservation, ...],
    pairs: tuple[MicroToolPair, ...],
) -> tuple[MicroToolOutcome, ...]:
    """Pair matched routes without turning failures into timing evidence."""

    pair_by_id = {pair.pair_id: pair for pair in pairs}
    grouped: dict[tuple[str, str, str], list[MicroToolObservation]] = {}
    for observation in observations:
        if observation.pair_id not in pair_by_id:
            raise ValueError(
                f"Unknown observed micro-tool pair {observation.pair_id!r}."
            )
        key = (observation.participant_id, observation.phase, observation.pair_id)
        grouped.setdefault(key, []).append(observation)

    outcomes = []
    for (participant_id, phase, pair_id), items in grouped.items():
        pair = pair_by_id[pair_id]
        by_route = {item.assigned_route: item for item in items}
        direct = by_route.get("direct")
        operator = by_route.get(pair.operator_route)
        common = {
            "participant_id": participant_id,
            "phase": phase,
            "pair_id": pair_id,
            "family_id": pair.family_id,
            "direct_observation_id": direct.observation_id if direct else None,
            "operator_observation_id": operator.observation_id if operator else None,
        }
        if len(items) != 2 or direct is None or operator is None:
            outcomes.append(
                MicroToolOutcome(
                    **common,
                    status="ineligible",
                    reason="missing_route",
                    time_delta=None,
                )
            )
            continue
        if not direct.route_adherent or not operator.route_adherent:
            outcomes.append(
                MicroToolOutcome(
                    **common,
                    status="ineligible",
                    reason="route_nonadherence",
                    time_delta=None,
                )
            )
            continue
        if (
            direct.completion != "complete"
            or operator.completion != "complete"
            or not direct.correct
            or not operator.correct
        ):
            outcomes.append(
                MicroToolOutcome(
                    **common,
                    status="ineligible",
                    reason="incorrect_or_incomplete",
                    time_delta=None,
                )
            )
            continue
        outcomes.append(
            MicroToolOutcome(
                **common,
                status="eligible",
                reason="both_correct_complete_adherent",
                time_delta=operator.total_seconds - direct.total_seconds,
            )
        )
    return tuple(outcomes)

from collections import Counter
from dataclasses import dataclass
import csv
from pathlib import Path
import re
from typing import Iterable


EVIDENCE_LEVELS = frozenset(
    {
        "executed-full",
        "executed-partial",
        "executed-shape-only",
        "candidate-unexecuted",
        "outside-current-grammar",
        "qualitative-only",
    }
)

REQUIRED_COLUMNS = (
    "problem_id",
    "year",
    "number",
    "pdf_page",
    "area",
    "family",
    "evidence",
    "next_operator",
    "synopsis",
)


@dataclass(frozen=True)
class CorpusEntry:
    problem_id: str
    year: int
    number: int
    pdf_page: int
    area: str
    family: str
    evidence: str
    next_operator: str
    synopsis: str


@dataclass(frozen=True)
class CorpusSummary:
    total: int
    years: tuple[int, ...]
    by_year: dict[int, int]
    by_area: dict[str, int]
    by_family: dict[str, int]
    by_evidence: dict[str, int]
    by_next_operator: dict[str, int]


def load_corpus_index(path: str | Path) -> tuple[CorpusEntry, ...]:
    """Load and validate the page-bound A617 top-level problem inventory."""

    with Path(path).open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if tuple(reader.fieldnames or ()) != REQUIRED_COLUMNS:
            raise ValueError(
                f"Corpus columns must be {REQUIRED_COLUMNS}; got {reader.fieldnames}."
            )
        rows = tuple(
            _entry_from_row(row, line=index + 2) for index, row in enumerate(reader)
        )

    ids = [entry.problem_id for entry in rows]
    if len(ids) != len(set(ids)):
        duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
        raise ValueError(f"Duplicate problem ids: {duplicates}.")
    return rows


def summarize_corpus(entries: Iterable[CorpusEntry]) -> CorpusSummary:
    rows = tuple(entries)
    by_year = dict(sorted(Counter(row.year for row in rows).items(), reverse=True))
    return CorpusSummary(
        total=len(rows),
        years=tuple(by_year),
        by_year=by_year,
        by_area=_counts(row.area for row in rows),
        by_family=_counts(row.family for row in rows),
        by_evidence=_counts(row.evidence for row in rows),
        by_next_operator=_counts(row.next_operator for row in rows),
    )


def _counts(values: Iterable[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items(), key=lambda item: (-item[1], item[0])))


def _entry_from_row(row: dict[str, str], *, line: int) -> CorpusEntry:
    try:
        entry = CorpusEntry(
            problem_id=row["problem_id"].strip(),
            year=int(row["year"]),
            number=int(row["number"]),
            pdf_page=int(row["pdf_page"]),
            area=row["area"].strip(),
            family=row["family"].strip(),
            evidence=row["evidence"].strip(),
            next_operator=row["next_operator"].strip(),
            synopsis=row["synopsis"].strip(),
        )
    except (AttributeError, KeyError, ValueError) as error:
        raise ValueError(f"Malformed corpus row at line {line}: {error}.") from error

    match = re.fullmatch(r"A(\d{2})-(\d{2})", entry.problem_id)
    if match is None:
        raise ValueError(f"Invalid problem id at line {line}: {entry.problem_id}.")
    if 2000 + int(match.group(1)) != entry.year:
        raise ValueError(
            f"Problem id/year mismatch at line {line}: {entry.problem_id}."
        )
    if int(match.group(2)) != entry.number or entry.number < 1:
        raise ValueError(
            f"Problem id/number mismatch at line {line}: {entry.problem_id}."
        )
    if not 1 <= entry.pdf_page <= 36:
        raise ValueError(f"Invalid PDF page at line {line}: {entry.pdf_page}.")
    if entry.evidence not in EVIDENCE_LEVELS:
        raise ValueError(f"Invalid evidence level at line {line}: {entry.evidence}.")
    for name in ("area", "family", "next_operator", "synopsis"):
        if not getattr(entry, name):
            raise ValueError(f"Empty {name} at line {line}.")
    return entry

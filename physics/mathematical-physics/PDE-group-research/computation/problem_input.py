"""Single-pass admission for source-backed ProblemSpec documents."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProblemDocument:
    """A decoded JSON object together with the path that gives it identity."""

    path: Path
    payload: dict[str, object]


class ProblemInputError(ValueError):
    """A source could not be decoded as a ProblemSpec JSON object."""


def load_problem(path: Path) -> ProblemDocument:
    """Read and decode one ProblemSpec exactly once."""

    source = Path(path)
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ProblemInputError(str(error)) from error
    if not isinstance(payload, dict):
        raise ProblemInputError("ProblemSpec must be a JSON object")
    return ProblemDocument(source, payload)

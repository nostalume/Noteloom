"""Black-box contracts for the public reduction workbench CLI."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

from coupled_operator_router import discover_problem as discover_coupled_operator
from coupled_relation_stabilizer import discover_problem as discover_coupled_relation
from matrix_adjoint_global_router import discover_problem as discover_matrix_global
from matrix_pde_inverse_router import discover_problem as discover_matrix_inverse
from matrix_symbol_covariance_router import discover_problem as discover_matrix_symbol
from natural_tensor_stabilizer import discover_problem as discover_natural_tensor
from pauli_bilateral_router import discover_problem as discover_pauli
from pauli_global_router import discover_problem as discover_pauli_global
from problem_router import discover_problem
from quadratic_route_router import discover_problem as discover_quadratic
from su_adjoint_multiplicity_router import discover_problem as discover_su_adjoint

COMPUTATION = Path(__file__).resolve().parent
REPOSITORY = Path(__file__).resolve().parents[4]
SCRIPT = COMPUTATION / "reduction_workbench.py"
EXAMPLES = COMPUTATION / "examples"


@dataclass(frozen=True)
class Case:
    arguments: tuple[str, ...]
    schema: str
    outcome: str
    exit_code: int
    selected_route: str | None
    summary_keys: frozenset[str]


DISCOVERY_KEYS = frozenset({"coincidence", "decision", "human_card", "outcome", "probes", "schema"})
DIRECT_KEYS = frozenset({"backend", "decision", "outcome", "schema", "witness"})


CASES = (
    Case(
        (
            "discover",
            str(EXAMPLES / "coupled-pauli-operator-positive.json"),
            "--summary",
        ),
        "reduction-decision/v1",
        "exact",
        0,
        "coupled-full-operator-kernel",
        DISCOVERY_KEYS,
    ),
    Case(
        (
            "discover",
            str(EXAMPLES / "coupled-carrier-clifford-r3.json"),
            "--summary",
        ),
        "reduction-decision/v1",
        "exact",
        0,
        "coupled-relation-kernel",
        DISCOVERY_KEYS,
    ),
    Case(
        (
            "discover",
            str(EXAMPLES / "coupled-carrier-clifford-small-budget.json"),
            "--summary",
        ),
        "reduction-decision/v1",
        "unresolved",
        3,
        None,
        DISCOVERY_KEYS,
    ),
    Case(
        (
            "discover",
            str(EXAMPLES / "quadratic-survival-compressed.json"),
            "--summary",
        ),
        "reduction-decision/v1",
        "exact",
        0,
        "observable-cyclic",
        DISCOVERY_KEYS,
    ),
    Case(
        (
            "discover",
            str(EXAMPLES / "natural-tensor-elasticity.json"),
            "--summary",
        ),
        "reduction-decision/v1",
        "controlled",
        0,
        "natural-tensor-structured-seed",
        DISCOVERY_KEYS,
    ),
    Case(
        (
            "discover",
            str(EXAMPLES / "natural-tensor-elasticity-small-budget.json"),
            "--summary",
        ),
        "reduction-decision/v1",
        "exact",
        0,
        "natural-tensor-structured-seed",
        DISCOVERY_KEYS,
    ),
    Case(
        (
            "discover",
            str(EXAMPLES / "natural-tensor-elasticity-structured-small-budget.json"),
            "--summary",
        ),
        "reduction-decision/v1",
        "unresolved",
        3,
        None,
        DISCOVERY_KEYS,
    ),
    Case(
        (
            "cyclic",
            str(EXAMPLES / "controlled-truncation.json"),
            "--summary",
        ),
        "reduction-witness/v1",
        "controlled",
        0,
        "cyclic",
        DIRECT_KEYS,
    ),
    Case(
        (
            "discover",
            str(EXAMPLES / "pauli-landau-global-wrong-domain.json"),
            "--summary",
        ),
        "reduction-decision/v1",
        "obstructed",
        2,
        None,
        DISCOVERY_KEYS,
    ),
    Case(
        (
            "discover",
            str(EXAMPLES / "pauli-landau-global-small-budget.json"),
            "--summary",
        ),
        "reduction-decision/v1",
        "unresolved",
        3,
        None,
        DISCOVERY_KEYS,
    ),
)

DIRECT_DISCOVERY_CASES = (
    (discover_coupled_operator, "coupled-pauli-operator-positive.json"),
    (discover_coupled_relation, "coupled-carrier-clifford-r3.json"),
    (discover_quadratic, "quadratic-survival-compressed.json"),
    (discover_pauli, "pauli-landau-positive.json"),
    (discover_pauli_global, "pauli-landau-global-positive.json"),
    (discover_su_adjoint, "su-adjoint-transition-su3.json"),
    (discover_matrix_inverse, "matrix-pde-inverse-sl3.json"),
    (discover_matrix_symbol, "matrix-symbol-covariance-sl3.json"),
    (discover_matrix_global, "matrix-adjoint-semigroup-sl3.json"),
    (discover_natural_tensor, "natural-tensor-elasticity.json"),
)


class WorkbenchCliContractTests(unittest.TestCase):
    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            cwd=REPOSITORY,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_summary_outcome_route_and_exit_contracts(self):
        for case in CASES:
            with self.subTest(arguments=case.arguments):
                completed = self.run_cli(*case.arguments)
                self.assertEqual(completed.stderr, "")
                result = json.loads(completed.stdout)
                self.assertEqual(completed.returncode, case.exit_code)
                self.assertEqual(frozenset(result), case.summary_keys)
                self.assertEqual(result["schema"], case.schema)
                self.assertEqual(result["outcome"], case.outcome)
                self.assertEqual(result["decision"]["selected_route"], case.selected_route)

    def test_malformed_and_non_object_problem_specs_are_refused(self):
        for content in ("{", "[]"):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as root:
                problem = Path(root) / "invalid.json"
                problem.write_text(content, encoding="utf-8")
                completed = self.run_cli("discover", str(problem))
                result = json.loads(completed.stdout)
                self.assertEqual(completed.returncode, 2)
                self.assertEqual(result["outcome"], "obstructed")
                self.assertEqual(result["obstruction"]["kind"], "UnsupportedProblemType")

    def test_common_discovery_reads_top_level_problem_once(self):
        problem = EXAMPLES / "quadratic-survival-compressed.json"
        original = Path.read_text
        reads = 0

        def counted(path: Path, *args: object, **kwargs: object) -> str:
            nonlocal reads
            if path == problem:
                reads += 1
            return original(path, *args, **kwargs)

        with patch.object(Path, "read_text", counted):
            result = discover_problem(problem)
        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(reads, 1)

    def test_direct_discovery_adapters_match_common_dispatch(self):
        for direct, filename in DIRECT_DISCOVERY_CASES:
            with self.subTest(filename=filename):
                path = EXAMPLES / filename
                self.assertEqual(direct(path), discover_problem(path))


if __name__ == "__main__":
    unittest.main()

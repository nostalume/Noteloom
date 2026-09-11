"""Public outcome contract for the polynomial active-module route."""

from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path

from polynomial_active_module_router import discover_payload

EXAMPLES = Path(__file__).resolve().parent / "examples"


class PolynomialActiveModuleRouterTests(unittest.TestCase):
    def payload(self, name: str) -> dict[str, object]:
        return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))

    def test_four_discriminating_public_dispositions(self) -> None:
        cases = {
            "polynomial-active-constant.json": ("exact", None),
            "polynomial-active-variable.json": ("formal", None),
            "polynomial-active-escape.json": ("obstructed", "CoefficientOrDerivativeEscape"),
            "polynomial-active-rank-unresolved.json": ("unresolved", "RankRegionUnresolved"),
        }
        for filename, (outcome, kind) in cases.items():
            with self.subTest(filename=filename):
                result = discover_payload(self.payload(filename))
                self.assertEqual(result["outcome"], outcome)
                self.assertEqual(result.get("obstruction", {}).get("kind"), kind)

    def test_g19_public_outputs_remain_byte_stable(self) -> None:
        expected = {
            "polynomial-active-variable.json": "dad4237f43bda66ab73e4458b91db75e75c2bf8ed88355fa7a50758b44c9ec02",
            "polynomial-active-constant.json": "045ac934f4d40fc98964d6173261debb4f36657216a202908953090414fb252a",
            "polynomial-active-rank-unresolved.json": "cd05e4a333404c6d95c5c250904d281ccce57f57099dfa94cdfa2f5a6c0f36a5",
            "polynomial-active-escape.json": "26c7b1a8091691108430c6f214ebb5df9f68b18d3696fdcc88d8e694fcf00322",
        }
        for filename, digest in expected.items():
            with self.subTest(filename=filename):
                output = json.dumps(
                    discover_payload(self.payload(filename)), sort_keys=True, separators=(",", ":")
                ).encode()
                self.assertEqual(hashlib.sha256(output).hexdigest(), digest)

    def test_output_budget_exhaustion_is_unresolved(self) -> None:
        payload = self.payload("polynomial-active-variable.json")
        payload["resource_budget"]["maximum_output_terms"] = 1
        result = discover_payload(payload)

        self.assertEqual(result["outcome"], "unresolved")
        self.assertEqual(result["obstruction"]["kind"], "OutputTermBudgetExceeded")

    def test_residual_lie_success_selects_the_new_route(self) -> None:
        result = discover_payload(self.payload("polynomial-lie-lift.json"))

        self.assertEqual(result["outcome"], "exact")
        self.assertEqual(result["decision"]["selected_route"], "polynomial-residual-lie-lift")
        lift = result["candidates"][1]["witness"]
        self.assertEqual(lift["direction"][0][0]["powers"], [0, 1])
        self.assertTrue(all(lift["checks"].values()))

    def test_lift_refusals_retain_the_constructed_g19_witness(self) -> None:
        cases = (
            ("polynomial-lie-no-lift.json", "NoInfinitesimalLift"),
            ("polynomial-lie-rank-two.json", "ResidualNotLineGenerated"),
            ("polynomial-lie-coefficient-only.json", "NoDirectionalLeakage"),
        )
        for filename, kind in cases:
            with self.subTest(kind=kind):
                result = discover_payload(self.payload(filename))
                self.assertEqual(result["outcome"], "obstructed")
                self.assertEqual(result["obstruction"]["kind"], kind)
                self.assertEqual(result["candidates"][0]["route"], "polynomial-active-module")
                self.assertIn("witness", result["candidates"][0])

    def test_lift_resource_exhaustion_is_unresolved_after_g19(self) -> None:
        payload = copy.deepcopy(self.payload("polynomial-lie-lift.json"))
        payload["resource_budget"]["residual_lie"]["maximum_candidate_dimension"] = 9

        result = discover_payload(payload)

        self.assertEqual(result["outcome"], "unresolved")
        self.assertEqual(result["obstruction"]["kind"], "CandidateBudgetExceeded")
        self.assertEqual(len(result["candidates"]), 1)


if __name__ == "__main__":
    unittest.main()

"""Public outcome contract for the polynomial active-module route."""

from __future__ import annotations

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

    def test_output_budget_exhaustion_is_unresolved(self) -> None:
        payload = self.payload("polynomial-active-variable.json")
        payload["resource_budget"]["maximum_output_terms"] = 1
        result = discover_payload(payload)

        self.assertEqual(result["outcome"], "unresolved")
        self.assertEqual(result["obstruction"]["kind"], "OutputTermBudgetExceeded")


if __name__ == "__main__":
    unittest.main()

import unittest

from sympy import symbols

from occ.problem import (
    PhysicalLaw,
    PolynomialProblemPacket,
    TargetRequest,
    compile_polynomial_problem,
)


class PolynomialProblemCompilerTests(unittest.TestCase):
    def test_compiles_multiple_targets_from_one_provenance_preserving_packet(self):
        source, hidden, linear, quadratic = symbols("source hidden linear quadratic")
        packet = PolynomialProblemPacket(
            problem_id="fixture-multi",
            pdf_page=1,
            laws=(
                PhysicalLaw("adapter", hidden - 2 * source, "test law"),
                PhysicalLaw("linear target", linear - 3 * hidden, "test target"),
                PhysicalLaw(
                    "quadratic target",
                    quadratic - hidden**2,
                    "test target",
                ),
            ),
            targets=(
                TargetRequest(
                    name="linear",
                    target=linear,
                    eliminate=(hidden, quadratic),
                    retain=(source, linear),
                ),
                TargetRequest(
                    name="quadratic",
                    target=quadratic,
                    eliminate=(hidden, linear),
                    retain=(source, quadratic),
                ),
            ),
            regime=("exact finite fixture",),
            branch_obligations=(),
        )

        result = compile_polynomial_problem(packet)

        self.assertEqual(result.status, "complete")
        self.assertTrue(result.target("linear").implies(linear - 6 * source))
        self.assertTrue(result.target("quadratic").implies(quadratic - 4 * source**2))
        self.assertEqual(
            tuple(law.provenance for law in result.packet.laws),
            ("test law", "test target", "test target"),
        )

    def test_reports_partial_when_one_declared_target_is_not_constrained(self):
        given, hidden, solved, missing = symbols("given hidden solved missing")
        packet = PolynomialProblemPacket(
            problem_id="fixture-partial",
            pdf_page=1,
            laws=(
                PhysicalLaw("map", hidden - given, "test law"),
                PhysicalLaw("solved", solved - hidden, "test target"),
            ),
            targets=(
                TargetRequest(
                    name="solved",
                    target=solved,
                    eliminate=(hidden, missing),
                    retain=(given, solved),
                ),
                TargetRequest(
                    name="missing",
                    target=missing,
                    eliminate=(hidden, solved),
                    retain=(given, missing),
                ),
            ),
            regime=(),
            branch_obligations=(),
        )

        result = compile_polynomial_problem(packet)

        self.assertEqual(result.status, "partial")
        self.assertEqual(result.target("solved").status, "constrained")
        self.assertEqual(result.target("missing").status, "underdetermined")

    def test_target_selects_only_the_laws_needed_for_its_projection(self):
        source, hidden, target, unrelated = symbols("source hidden target unrelated")
        packet = PolynomialProblemPacket(
            problem_id="fixture-law-selection",
            pdf_page=1,
            laws=(
                PhysicalLaw("map", hidden - 2 * source, "test map"),
                PhysicalLaw("target", target - 3 * hidden, "test target"),
                PhysicalLaw("unrelated", unrelated**2 - 2, "other subpart"),
            ),
            targets=(
                TargetRequest(
                    name="target",
                    target=target,
                    eliminate=(hidden,),
                    retain=(source, target),
                    law_names=("map", "target"),
                ),
            ),
            regime=(),
            branch_obligations=(),
        )

        result = compile_polynomial_problem(packet)

        self.assertEqual(result.status, "complete")
        self.assertTrue(result.target("target").implies(target - 6 * source))

    def test_duplicate_target_names_are_rejected_before_elimination(self):
        given, target = symbols("given target")
        request = TargetRequest(
            name="same",
            target=target,
            eliminate=(given,),
            retain=(target,),
        )

        with self.assertRaisesRegex(ValueError, "target name"):
            PolynomialProblemPacket(
                problem_id="fixture-duplicate",
                pdf_page=1,
                laws=(PhysicalLaw("law", target - given, "test"),),
                targets=(request, request),
                regime=(),
                branch_obligations=(),
            )


if __name__ == "__main__":
    unittest.main()

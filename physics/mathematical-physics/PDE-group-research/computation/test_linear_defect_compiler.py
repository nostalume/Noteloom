from __future__ import annotations

import unittest
from fractions import Fraction

from adjoint_algebra import (
    adjoint_matrices,
    commutator_closure,
    inverse,
    multiply,
    pair,
    transpose,
)
from linear_defect_compiler import (
    CandidateBracket,
    DefectBlock,
    DefectBudget,
    LinearMap,
    compile_defects,
)
from quadratic_centralizer import Poly, compatibility_obstruction


class LinearDefectCompilerTests(unittest.TestCase):
    def test_quadratic_centralizer_kernel_matches_compatibility_map(self) -> None:
        potential = Poly({(2, 0): Fraction(1), (0, 2): Fraction(2)})
        units = tuple(tuple(Fraction(index == column) for index in range(6)) for column in range(6))
        residuals = tuple(compatibility_obstruction(potential, vector) for vector in units)
        targets = sorted({power for residual in residuals for power in residual.terms})
        block = DefectBlock(
            name="bertrand-darboux",
            target_labels=tuple(str(power) for power in targets),
            columns=tuple(
                tuple(residual.terms.get(power, Fraction(0)) for power in targets)
                for residual in residuals
            ),
        )

        result = compile_defects(
            candidate_labels=("a", "b", "c", "d", "e", "f"),
            blocks=(block,),
            budget=DefectBudget(6, 32),
        )

        self.assertEqual(result.outcome, "exact")
        self.assertEqual(result.kernel_dimension, 2)
        self.assertEqual(result.ledger[0].name, "bertrand-darboux")
        self.assertEqual(result.ledger[0].rank_drop, 4)

    def test_boundary_constraints_distinguish_disk_and_ellipse(self) -> None:
        def boundary_block(g00: int, g01: int, g11: int) -> DefectBlock:
            return DefectBlock(
                name="boundary-tangency",
                target_labels=("x", "y", "x2", "xy", "y2"),
                columns=(
                    (Fraction(2 * g00), Fraction(2 * g01), 0, 0, 0),
                    (Fraction(2 * g01), Fraction(2 * g11), 0, 0, 0),
                    (
                        0,
                        0,
                        Fraction(2 * g01),
                        Fraction(2 * (g11 - g00)),
                        Fraction(-2 * g01),
                    ),
                ),
            )

        disk = compile_defects(
            candidate_labels=("translation-x", "translation-y", "rotation"),
            blocks=(boundary_block(1, 0, 1),),
            budget=DefectBudget(3, 5),
        )
        ellipse = compile_defects(
            candidate_labels=("translation-x", "translation-y", "rotation"),
            blocks=(boundary_block(1, 0, 2),),
            budget=DefectBudget(3, 5),
        )

        self.assertEqual(disk.kernel_basis, ((Fraction(0), Fraction(0), Fraction(1)),))
        self.assertEqual(ellipse.kernel_dimension, 0)

    def test_matrix_pairing_covariance_uses_the_same_kernel_contract(self) -> None:
        e = ((Fraction(0), Fraction(1)), (Fraction(0), Fraction(0)))
        f = ((Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)))
        closure, _, _ = commutator_closure([e, f], maximum_dimension=3)
        gram = tuple(tuple(pair(left, right) for right in closure) for left in closure)
        actions = adjoint_matrices(closure, inverse(gram))

        def covariance_block(metric: tuple[tuple[Fraction, ...], ...]) -> DefectBlock:
            residuals = tuple(
                tuple(
                    value
                    for row in (
                        tuple(
                            multiply(transpose(action), metric)[i][j]
                            + multiply(metric, action)[i][j]
                            for j in range(len(closure))
                        )
                        for i in range(len(closure))
                    )
                    for value in row
                )
                for action in actions
            )
            return DefectBlock(
                name="principal-pairing-covariance",
                target_labels=tuple(
                    f"{i},{j}" for i in range(len(closure)) for j in range(len(closure))
                ),
                columns=residuals,
            )

        invariant = compile_defects(
            candidate_labels=tuple(f"ad-{index}" for index in range(len(closure))),
            blocks=(covariance_block(gram),),
            budget=DefectBudget(3, 9),
        )
        coordinate_identity = tuple(
            tuple(Fraction(i == j) for j in range(len(closure))) for i in range(len(closure))
        )
        broken = compile_defects(
            candidate_labels=tuple(f"ad-{index}" for index in range(len(closure))),
            blocks=(covariance_block(coordinate_identity),),
            budget=DefectBudget(3, 9),
        )

        self.assertEqual(invariant.kernel_dimension, len(closure))
        self.assertLess(broken.kernel_dimension, len(closure))

    def test_resource_bound_returns_unresolved_result(self) -> None:
        result = compile_defects(
            candidate_labels=("x", "y"),
            blocks=(
                DefectBlock(
                    name="one-row",
                    target_labels=("r",),
                    columns=((Fraction(1),), (Fraction(0),)),
                ),
            ),
            budget=DefectBudget(1, 1),
        )

        self.assertEqual(result.outcome, "unresolved")
        self.assertEqual(result.obstruction_kind, "CandidateBudgetExceeded")

    def test_closed_kernel_and_ineffective_ideal_produce_quotient(self) -> None:
        zero = (Fraction(0), Fraction(0), Fraction(0))
        heisenberg = CandidateBracket(
            name="heisenberg",
            table=(
                (zero, (Fraction(0), Fraction(0), Fraction(1)), zero),
                ((Fraction(0), Fraction(0), Fraction(-1)), zero, zero),
                (zero, zero, zero),
            ),
        )
        result = compile_defects(
            candidate_labels=("x", "y", "z"),
            blocks=(),
            visible_action=LinearMap(
                name="visible-plane-action",
                target_labels=("x-visible", "y-visible"),
                columns=((1, 0), (0, 1), (0, 0)),
            ),
            bracket=heisenberg,
            budget=DefectBudget(3, 2, maximum_bracket_checks=64),
        )

        self.assertEqual(result.outcome, "exact")
        self.assertEqual(result.ineffective_basis, ((Fraction(0), Fraction(0), Fraction(1)),))
        self.assertEqual(result.effective_dimension, 2)
        self.assertEqual(result.closure_status, "closed")
        self.assertTrue(
            all(
                all(coefficient == 0 for coefficient in bracket_value)
                for row in result.quotient_bracket_table
                for bracket_value in row
            )
        )

    def test_nonideal_visible_kernel_is_an_obstruction(self) -> None:
        zero = (Fraction(0), Fraction(0))
        affine = CandidateBracket(
            name="affine-line",
            table=(
                (zero, (Fraction(0), Fraction(1))),
                ((Fraction(0), Fraction(-1)), zero),
            ),
        )
        result = compile_defects(
            candidate_labels=("h", "e"),
            blocks=(),
            visible_action=LinearMap(
                name="e-visible",
                target_labels=("visible",),
                columns=((0,), (1,)),
            ),
            bracket=affine,
            budget=DefectBudget(2, 1, maximum_bracket_checks=32),
        )

        self.assertEqual(result.outcome, "obstructed")
        self.assertEqual(result.obstruction_kind, "IneffectiveSubspaceNotIdeal")

    def test_nonclosed_defect_kernel_is_an_obstruction(self) -> None:
        zero = (Fraction(0), Fraction(0), Fraction(0))
        euclidean = CandidateBracket(
            name="e2",
            table=(
                (zero, zero, (0, -1, 0)),
                (zero, zero, (1, 0, 0)),
                ((0, 1, 0), (-1, 0, 0), zero),
            ),
        )
        result = compile_defects(
            candidate_labels=("translation-x", "translation-y", "rotation"),
            blocks=(
                DefectBlock(
                    name="remove-y-only",
                    target_labels=("y-defect",),
                    columns=((0,), (1,), (0,)),
                ),
            ),
            bracket=euclidean,
            budget=DefectBudget(3, 1, maximum_bracket_checks=64),
        )

        self.assertEqual(result.outcome, "obstructed")
        self.assertEqual(result.obstruction_kind, "KernelClosureObstruction")


if __name__ == "__main__":
    unittest.main()

from fractions import Fraction
import unittest

from sympy import Rational, factor, simplify, symbols

from occ.linear import construct_observable_closure
from occ.relation import eliminate_polynomial_relations
from occ.pullback import (
    pullback_linear,
    pullback_quadratic,
)


def exact(value):
    return Rational(value.numerator, value.denominator)


class ObservableRelationEliminationTests(unittest.TestCase):
    def test_deterministic_map_pullback_is_relation_elimination(self):
        x1, x2, y1, y2, z = symbols("x1 x2 y1 y2 z")
        result = eliminate_polynomial_relations(
            (
                y1 - x1 - 2 * x2,
                y2 - 3 * x1 - 4 * x2,
                z - 5 * y1 - 7 * y2,
            ),
            eliminate=(y1, y2),
            retain=(x1, x2, z),
            target=z,
        )
        fast_path = pullback_linear((((1, 2), (3, 4)),), (5, 7))
        fast_relation = z - sum(
            exact(coefficient) * variable
            for coefficient, variable in zip(fast_path.source_covector, (x1, x2))
        )

        self.assertEqual(result.status, "constrained")
        self.assertTrue(result.implies(fast_relation))
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_quadratic_observable_reduces_without_retaining_field_components(self):
        u, e1, e2, power = symbols("u e1 e2 power")
        result = eliminate_polynomial_relations(
            (e1 - u, e2 - 2 * u, power - e1**2 - 3 * e2**2),
            eliminate=(e1, e2),
            retain=(u, power),
            target=power,
        )
        fast_path = pullback_quadratic(
            (((1,), (2,)),),
            ((1, 0), (0, 3)),
        )
        fast_relation = power - exact(fast_path.source_form[0][0]) * u**2

        self.assertEqual(result.status, "constrained")
        self.assertTrue(result.implies(fast_relation))

    def test_linear_observable_closure_is_the_same_projection(self):
        x1, x2, a1, a2 = symbols("x1 x2 a1 a2")
        y0, y1, b0, b1 = symbols("y0 y1 b0 b1")
        closure = construct_observable_closure(
            ((1, 0), (0, 4)),
            (Fraction(1, 2), Fraction(1, 2)),
        )
        full_positions = (x1, x2)
        full_accelerations = (a1, a2)
        reduced_positions = (y0, y1)
        reduced_accelerations = (b0, b1)
        projection_relations = tuple(
            reduced_positions[index]
            - sum(
                exact(weight) * coordinate
                for weight, coordinate in zip(row, full_positions)
            )
            for index, row in enumerate(closure.basis)
        ) + tuple(
            reduced_accelerations[index]
            - sum(
                exact(weight) * acceleration
                for weight, acceleration in zip(row, full_accelerations)
            )
            for index, row in enumerate(closure.basis)
        )
        result = eliminate_polynomial_relations(
            (a1 + x1, a2 + 4 * x2) + projection_relations,
            eliminate=(x1, x2, a1, a2),
            retain=(y0, y1, b0, b1),
            target=b0,
        )

        self.assertEqual(result.status, "constrained")
        for index, acceleration in enumerate(reduced_accelerations):
            fast_relation = acceleration + sum(
                exact(coefficient) * coordinate
                for coefficient, coordinate in zip(
                    closure.reduced_second_order_operator[index],
                    reduced_positions,
                )
            )
            self.assertTrue(result.implies(fast_relation))

    def test_a617_orbit_produces_both_turning_points_before_branch_selection(self):
        alpha, rho, energy, angular_momentum = symbols(
            "alpha rho energy angular_momentum"
        )
        result = eliminate_polynomial_relations(
            (
                2 * energy - alpha**2 + 2,
                angular_momentum - alpha,
                2 * energy * rho**2 - angular_momentum**2 + 2 * rho,
            ),
            eliminate=(energy, angular_momentum),
            retain=(alpha, rho),
            target=rho,
        )

        expected = (rho - 1) * ((alpha**2 - 2) * rho + alpha**2)
        self.assertEqual(result.status, "constrained")
        self.assertTrue(result.implies(expected))
        self.assertEqual(
            {factor(candidate) for candidate in result.target_candidates()},
            {1, -(alpha**2) / (alpha**2 - 2)},
        )
        lifted_hidden = {
            energy: alpha**2 / 2 - 1,
            angular_momentum: alpha,
        }
        for candidate in result.target_candidates():
            lift = lifted_hidden | {rho: candidate}
            for relation in (
                2 * energy - alpha**2 + 2,
                angular_momentum - alpha,
                2 * energy * rho**2 - angular_momentum**2 + 2 * rho,
            ):
                self.assertEqual(simplify(relation.subs(lift)), 0)

    def test_missing_target_relation_reports_underdetermination(self):
        given, hidden, target = symbols("given hidden target")
        result = eliminate_polynomial_relations(
            (hidden - given,),
            eliminate=(hidden,),
            retain=(given, target),
            target=target,
        )

        self.assertEqual(result.status, "underdetermined")
        self.assertEqual(result.obstruction.code, "target_not_constrained")
        self.assertEqual(result.target_candidates(), ())

    def test_variable_budget_refuses_before_elimination(self):
        a, b, c, d = symbols("a b c d")
        result = eliminate_polynomial_relations(
            (d - a - b - c,),
            eliminate=(b, c),
            retain=(a, d),
            target=d,
            max_variables=3,
        )

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "variable_budget_exceeded")

    def test_inconsistent_physical_relations_are_reported(self):
        hidden, target = symbols("hidden target")
        result = eliminate_polynomial_relations(
            (hidden, hidden - 1),
            eliminate=(hidden,),
            retain=(target,),
            target=target,
        )

        self.assertEqual(result.status, "inconsistent")
        self.assertEqual(result.obstruction.code, "inconsistent_relations")

    def test_direct_target_relation_needs_no_artificial_hidden_variable(self):
        given, target = symbols("given target")

        result = eliminate_polynomial_relations(
            (target - 2 * given,),
            eliminate=(),
            retain=(given, target),
            target=target,
        )

        self.assertEqual(result.status, "constrained")
        self.assertTrue(result.implies(target - 2 * given))


if __name__ == "__main__":
    unittest.main()

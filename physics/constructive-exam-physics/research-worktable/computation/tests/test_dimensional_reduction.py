import unittest

from sympy import pi, simplify, sqrt, symbols

from occ.semantic import (
    Dimension,
    QuantitySemantics,
)
from occ.dimensional import construct_dimensionless_groups


ZERO = Dimension(0, 0, 0, 0)
MASS = Dimension(1, 0, 0, 0)
LENGTH = Dimension(0, 1, 0, 0)
TIME = Dimension(0, 0, 1, 0)
ACCELERATION = Dimension(0, 1, -2, 0)
DENSITY = Dimension(1, -3, 0, 0)
VELOCITY = Dimension(0, 1, -1, 0)
VISCOSITY = Dimension(1, -1, -1, 0)
RESISTANCE = Dimension(1, 2, -3, -2)
CAPACITANCE = Dimension(-1, -2, 4, 2)


def quantity(symbol, name, dimension):
    return QuantitySemantics(symbol, name, dimension)


class DimensionalReductionTests(unittest.TestCase):
    def test_pendulum_constructs_primitive_dimensionless_group(self):
        period, length, gravity = symbols("T L g", positive=True)

        result = construct_dimensionless_groups(
            (
                quantity(period, "period", TIME),
                quantity(length, "length", LENGTH),
                quantity(gravity, "gravitational acceleration", ACCELERATION),
            )
        )

        self.assertEqual(result.status, "constructed")
        self.assertEqual(result.dimension_rank, 2)
        self.assertEqual(result.nullity, 1)
        self.assertEqual(result.groups[0].exponents, (2, -1, 1))
        self.assertEqual(
            simplify(result.groups[0].expression - period**2 * gravity / length),
            0,
        )
        self.assertEqual(
            simplify(
                result.groups[0].expression.subs(
                    period, 2 * pi * sqrt(length / gravity)
                )
            ),
            4 * pi**2,
        )
        self.assertTrue(all(item.passed for item in result.certificates))

    def test_same_constructor_transfers_to_fluid_and_circuit_packets(self):
        density, speed, length, viscosity = symbols("rho v L mu", positive=True)
        fluid = construct_dimensionless_groups(
            (
                quantity(density, "density", DENSITY),
                quantity(speed, "speed", VELOCITY),
                quantity(length, "length", LENGTH),
                quantity(viscosity, "dynamic viscosity", VISCOSITY),
            )
        )
        time, resistance, capacitance = symbols("t R C", positive=True)
        circuit = construct_dimensionless_groups(
            (
                quantity(time, "elapsed time", TIME),
                quantity(resistance, "resistance", RESISTANCE),
                quantity(capacitance, "capacitance", CAPACITANCE),
            )
        )

        self.assertEqual(fluid.groups[0].exponents, (1, 1, 1, -1))
        self.assertEqual(
            simplify(fluid.groups[0].expression - density * speed * length / viscosity),
            0,
        )
        self.assertEqual(circuit.groups[0].exponents, (1, -1, -1))
        self.assertEqual(
            simplify(circuit.groups[0].expression - time / (resistance * capacitance)),
            0,
        )

    def test_dimensionally_independent_quantities_return_irreducible(self):
        mass, length = symbols("m L")

        result = construct_dimensionless_groups(
            (
                quantity(mass, "mass", MASS),
                quantity(length, "length", LENGTH),
            )
        )

        self.assertEqual(result.status, "irreducible")
        self.assertEqual(result.groups, ())
        self.assertEqual(result.obstruction.code, "no_dimensionless_group")

    def test_group_budget_refuses_before_returning_partial_basis(self):
        first, second, third = symbols("a b c")

        result = construct_dimensionless_groups(
            (
                quantity(first, "first ratio", ZERO),
                quantity(second, "second ratio", ZERO),
                quantity(third, "third ratio", ZERO),
            ),
            max_groups=2,
        )

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.groups, ())
        self.assertEqual(result.obstruction.code, "group_budget_exceeded")

    def test_duplicate_quantity_symbol_is_rejected(self):
        shared = symbols("x")

        with self.assertRaisesRegex(ValueError, "symbols must be unique"):
            construct_dimensionless_groups(
                (
                    quantity(shared, "mass", MASS),
                    quantity(shared, "length", LENGTH),
                )
            )


if __name__ == "__main__":
    unittest.main()

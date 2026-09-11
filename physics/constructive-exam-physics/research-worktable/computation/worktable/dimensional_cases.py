"""Cross-area dimensional-quotient witnesses."""

from __future__ import annotations

from sympy import pi, simplify, sqrt, symbols

from occ.semantic import (
    Dimension,
    QuantitySemantics,
)
from occ.dimensional import construct_dimensionless_groups


MASS = Dimension(1, 0, 0, 0)
LENGTH = Dimension(0, 1, 0, 0)
TIME = Dimension(0, 0, 1, 0)
ACCELERATION = Dimension(0, 1, -2, 0)
DENSITY = Dimension(1, -3, 0, 0)
VELOCITY = Dimension(0, 1, -1, 0)
VISCOSITY = Dimension(1, -1, -1, 0)
RESISTANCE = Dimension(1, 2, -3, -2)
CAPACITANCE = Dimension(-1, -2, 4, 2)


def _quantity(symbol, name, dimension):
    return QuantitySemantics(symbol, name, dimension)


def command_dimensional_transfer() -> None:
    period, pendulum_length, gravity = symbols("T L g", positive=True)
    density, speed, fluid_length, viscosity = symbols("rho v ell mu", positive=True)
    time, resistance, capacitance = symbols("t R C", positive=True)
    mass, independent_length = symbols("m x", positive=True)
    cases = (
        (
            "pendulum",
            "mechanics",
            (
                _quantity(period, "period", TIME),
                _quantity(pendulum_length, "length", LENGTH),
                _quantity(gravity, "gravitational acceleration", ACCELERATION),
            ),
            lambda group: simplify(
                group.subs(period, 2 * pi * sqrt(pendulum_length / gravity))
            ),
        ),
        (
            "reynolds",
            "fluid",
            (
                _quantity(density, "density", DENSITY),
                _quantity(speed, "speed", VELOCITY),
                _quantity(fluid_length, "length", LENGTH),
                _quantity(viscosity, "dynamic viscosity", VISCOSITY),
            ),
            lambda group: "regime_coordinate",
        ),
        (
            "rc-time",
            "circuit",
            (
                _quantity(time, "elapsed time", TIME),
                _quantity(resistance, "resistance", RESISTANCE),
                _quantity(capacitance, "capacitance", CAPACITANCE),
            ),
            lambda group: simplify(group.subs(time, resistance * capacitance)),
        ),
        (
            "independent",
            "boundary",
            (
                _quantity(mass, "mass", MASS),
                _quantity(independent_length, "length", LENGTH),
            ),
            lambda group: "not_applicable",
        ),
    )

    print("problem\tarea\tstatus\trank\tnullity\tgroup\tuse")
    constructed = 0
    irreducible = 0
    all_certified = True
    for problem, area, quantities, consume in cases:
        result = construct_dimensionless_groups(quantities)
        expression = result.groups[0].expression if result.groups else None
        use = consume(expression) if expression is not None else "-"
        group = str(expression) if expression is not None else "-"
        print(
            f"{problem}\t{area}\t{result.status}\t{result.dimension_rank}"
            f"\t{result.nullity}\t{group}\t{use}"
        )
        constructed += result.status == "constructed"
        irreducible += result.status == "irreducible"
        all_certified &= all(item.passed for item in result.certificates)
    certificate_status = (
        "all_constructed_groups_certified" if all_certified else "failed"
    )
    print(
        f"summary\t{constructed}_cross_area_groups\t{irreducible}_irreducible"
        f"\t{certificate_status}"
    )

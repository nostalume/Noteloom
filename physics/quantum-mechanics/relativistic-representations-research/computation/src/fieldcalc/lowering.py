"""Semantic lowering from invariant two-point numerators to integral sectors."""

from dataclasses import dataclass

from sympy import Dummy, Poly, expand, simplify, sympify
from sympy.polys.polyerrors import PolynomialError

from .rewrite import Refusal


@dataclass(frozen=True)
class IntegralSector:
    name: str
    denominator_powers: tuple[int, int]
    coefficient: object
    scaleless_in_dimreg: bool = False


@dataclass(frozen=True)
class TwoPointLowering:
    sectors: tuple[IntegralSector, ...] = ()
    input_degree: int = 0
    denominator_degree: int = 0
    reconstruction_residual: object = 0
    refusal: Refusal | None = None

    @property
    def accepted(self) -> bool:
        return self.refusal is None

    @property
    def dimreg_sectors(self) -> tuple[IntegralSector, ...]:
        return tuple(
            sector
            for sector in self.sectors
            if not sector.scaleless_in_dimreg and sector.coefficient != 0
        )


def compile_scalar_spin2_numerator(
    external_square,
    loop_square,
    loop_dot_external,
    mass_squared,
    dimension,
):
    """Contract two minimal scalar currents through dimension-d trace reversal."""
    external_square = sympify(external_square)
    loop_square = sympify(loop_square)
    loop_dot_external = sympify(loop_dot_external)
    mass_squared = sympify(mass_squared)
    dimension = sympify(dimension)
    if dimension == 2:
        raise ValueError("spin-two trace reversal is singular in dimension two")

    trace_shift = loop_dot_external - mass_squared
    current_pairing = (
        2 * external_square * loop_square
        + 2 * loop_dot_external**2
        - 4 * trace_shift * loop_dot_external
        + dimension * trace_shift**2
    )
    current_trace = 2 * loop_dot_external - dimension * trace_shift
    return simplify(current_pairing - current_trace**2 / (dimension - 2))


def lower_two_point_numerator(
    numerator,
    loop_square,
    loop_dot_external,
    external_square,
    mass_squared,
) -> TwoPointLowering:
    """Rewrite an affine two-point numerator in its propagator-denominator basis."""
    numerator = sympify(numerator)
    loop_square = sympify(loop_square)
    loop_dot_external = sympify(loop_dot_external)
    external_square = sympify(external_square)
    mass_squared = sympify(mass_squared)
    try:
        input_degree = Poly(
            numerator, loop_square, loop_dot_external
        ).total_degree()
    except PolynomialError:
        return TwoPointLowering(
            refusal=Refusal(
                "numerator is not polynomial in declared loop invariants",
                provenance="two-point denominator quotient",
            )
        )

    massive = Dummy("D_massive")
    exchange = Dummy("D_exchange")
    denominator_numerator = simplify(
        numerator.subs(
            {
                loop_square: massive + mass_squared,
                loop_dot_external: (
                    external_square + massive + mass_squared - exchange
                )
                / 2,
            },
            simultaneous=True,
        )
    )
    try:
        polynomial = Poly(denominator_numerator, massive, exchange)
    except PolynomialError:
        return TwoPointLowering(
            input_degree=input_degree,
            refusal=Refusal(
                "denominator quotient did not produce a polynomial",
                provenance="two-point denominator quotient",
            ),
        )
    denominator_degree = polynomial.total_degree()
    if denominator_degree > 1:
        return TwoPointLowering(
            input_degree=input_degree,
            denominator_degree=denominator_degree,
            refusal=Refusal(
                "numerator exceeds affine denominator span",
                residual=(denominator_numerator,),
                provenance="two-point denominator quotient",
            ),
        )

    bubble = simplify(polynomial.coeff_monomial(1))
    massless_tadpole = simplify(polynomial.coeff_monomial(massive))
    massive_tadpole = simplify(polynomial.coeff_monomial(exchange))
    sectors = (
        IntegralSector("bubble", (1, 1), bubble),
        IntegralSector("massive tadpole", (1, 0), massive_tadpole),
        IntegralSector("massless tadpole", (0, 1), massless_tadpole, True),
    )
    massive_denominator = loop_square - mass_squared
    exchange_denominator = (
        external_square + loop_square - 2 * loop_dot_external
    )
    reconstructed = (
        bubble
        + massless_tadpole * massive_denominator
        + massive_tadpole * exchange_denominator
    )
    return TwoPointLowering(
        sectors=sectors,
        input_degree=input_degree,
        denominator_degree=denominator_degree,
        reconstruction_residual=expand(simplify(numerator - reconstructed)),
    )

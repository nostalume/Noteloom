"""N10u: compile a curvature detector's visible one-particle measure.

The code retains the complete coefficient through order g^2.  It constructs the
frequency power from the null-orbit measure and the derivative degree of K_s;
it does not accept that power as input.  No component polarization basis, gamma
matrix, dressed Fock diagonalization, resonance, or S matrix is used.
"""

from __future__ import annotations

from dataclasses import dataclass
import cmath
import math

from angular_response import (
    ConstructionRefusal,
    DetectorContraction,
    compile_angular_response,
)


SPATIAL_DIMENSION = 3
CUTOFF = 2.0
LEVEL_GAP = 1.2
COUPLING = 0.005
FREQUENCY_LIMIT = 8.0 * CUTOFF
DETECTOR = DetectorContraction(plus_norm_squared=0.6, minus_norm_squared=0.4)


def simpson(function, left: float, right: float, intervals: int = 160_000):
    if intervals <= 0 or intervals % 2:
        raise ValueError("Simpson interval count must be positive and even")
    step = (right - left) / intervals
    total = function(left) + function(right)
    total += 4.0 * sum(function(left + step * index) for index in range(1, intervals, 2))
    total += 2.0 * sum(function(left + step * index) for index in range(2, intervals, 2))
    return total * step / 3.0


@dataclass(frozen=True)
class CurvatureDetectorMeasure:
    """Scalar measure seen by one compiled, isotropically smeared detector.

    The detector supplies its contraction on the two physical chiral summands.
    The angular response is generated from the covariant projector average.
    """

    spin: int
    cutoff: float
    detector: DetectorContraction

    def __post_init__(self) -> None:
        if self.spin < 1:
            raise ValueError("the N10u bench treats positive integer helicity")
        if self.cutoff <= 0.0:
            raise ValueError("the spatial cutoff must be positive")
        compile_angular_response(self.spin, self.detector)

    @property
    def angular_compilation(self):
        return compile_angular_response(self.spin, self.detector)

    @property
    def angular_response(self) -> float:
        return self.angular_compilation.response

    @property
    def shell_power(self) -> int:
        # d^d p/(2|p|), after angular integration, scales as
        # omega^(d-2) d omega.
        return SPATIAL_DIMENSION - 2

    @property
    def curvature_power(self) -> int:
        # K_s has derivative degree s; a spectral weight is an amplitude square.
        return 2 * self.spin

    @property
    def density_power(self) -> int:
        return self.shell_power + self.curvature_power

    def smearing_squared(self, frequency: float) -> float:
        return math.exp(-(frequency / self.cutoff) ** 2)

    def shell_jacobian(self, frequency: float) -> float:
        return 0.5 * frequency**self.shell_power

    def curvature_amplitude_squared(self, frequency: float) -> float:
        return self.angular_response * frequency**self.curvature_power

    def density_from_factors(self, frequency: float) -> float:
        if frequency < 0.0:
            return 0.0
        return (
            self.shell_jacobian(frequency)
            * self.curvature_amplitude_squared(frequency)
            * self.smearing_squared(frequency)
        )

    def compiled_density(self, frequency: float) -> float:
        if frequency < 0.0:
            return 0.0
        return (
            0.5
            * self.angular_response
            * frequency**self.density_power
            * self.smearing_squared(frequency)
        )

    def integrate(self, function, intervals: int = 160_000):
        return simpson(
            lambda frequency: self.compiled_density(frequency) * function(frequency),
            0.0,
            FREQUENCY_LIMIT,
            intervals,
        )

    def analytic_mass(self) -> float:
        # int_0^infinity w^(2s+1) exp[-(w/Lambda)^2] dw
        #   = Lambda^(2s+2) Gamma(s+1)/2.
        return (
            0.25
            * self.angular_response
            * self.cutoff ** (2 * self.spin + 2)
            * math.factorial(self.spin)
        )


def transition_kernel(detuning: float, time: float) -> float:
    argument = 0.5 * detuning * time
    if abs(argument) < 1e-7:
        sinc = 1.0 - argument**2 / 6.0 + argument**4 / 120.0
        return time * time * sinc * sinc
    return 4.0 * math.sin(argument) ** 2 / detuning**2


def bound_shift(measure: CurvatureDetectorMeasure) -> float:
    return -(COUPLING**2) * measure.integrate(
        lambda frequency: 1.0 / (LEVEL_GAP + frequency)
    )


def bound_residue(measure: CurvatureDetectorMeasure) -> float:
    return 1.0 - (COUPLING**2) * measure.integrate(
        lambda frequency: 1.0 / (LEVEL_GAP + frequency) ** 2
    )


def emitted_probability(measure: CurvatureDetectorMeasure, time: float) -> float:
    intervals = max(160_000, int(2_500 * max(1.0, time)))
    if intervals % 2:
        intervals += 1
    return (COUPLING**2) * measure.integrate(
        lambda frequency: transition_kernel(LEVEL_GAP - frequency, time),
        intervals=intervals,
    )


def boundary_rate(measure: CurvatureDetectorMeasure) -> float:
    return 2.0 * math.pi * COUPLING**2 * measure.compiled_density(LEVEL_GAP)


def memory(measure: CurvatureDetectorMeasure, time: float) -> complex:
    return (COUPLING**2) * measure.integrate(
        lambda frequency: cmath.exp(-1j * frequency * time)
    )


def main() -> None:
    measures = {
        spin: CurvatureDetectorMeasure(spin, CUTOFF, DETECTOR)
        for spin in (1, 2)
    }

    print("curvature detector measure compiler")
    print(f"spatial dimension             = {SPATIAL_DIMENSION}")
    print(f"detector gap Omega            = {LEVEL_GAP:.12f}")
    print(f"Gaussian cutoff Lambda        = {CUTOFF:.12f}")
    print(f"coupling g                    = {COUPLING:.12f}")
    print(f"detector chiral norm^2         = {DETECTOR.total_norm_squared:.12f}")

    for spin, measure in measures.items():
        numerical_mass = measure.integrate(lambda frequency: 1.0)
        analytic_mass = measure.analytic_mass()
        mass_error = abs(numerical_mass - analytic_mass) / analytic_mass
        factor_error = max(
            abs(measure.compiled_density(frequency) - measure.density_from_factors(frequency))
            for frequency in (0.2, 0.7, LEVEL_GAP, 2.5)
        )
        shift = bound_shift(measure)
        residue = bound_residue(measure)
        rate = boundary_rate(measure)
        rate_probe_time = 160.0
        probability = emitted_probability(measure, rate_probe_time)
        rate_error = abs(probability / rate_probe_time - rate) / rate
        secular_parameter = rate * rate_probe_time

        print(f"\nspin {spin}")
        print(f"rotation irrep dimension       = {measure.angular_compilation.irrep_dimension}")
        print(f"generated angular response     = {measure.angular_response:.15f}")
        print(f"generated density power       = {measure.density_power}")
        print(f"measure mass                  = {numerical_mass:.15f}")
        print(f"analytic mass                 = {analytic_mass:.15f}")
        print(f"factorization error           = {factor_error:.3e}")
        print(f"order-g^2 ground shift        = {shift:.15e}")
        print(f"order-g^2 ground residue      = {residue:.15f}")
        print(f"open boundary rate            = {rate:.15e}")
        print(
            f"P_emit^(2)({rate_probe_time:.0f})/{rate_probe_time:.0f}"
            f"            = {probability / rate_probe_time:.15e}"
        )
        print(f"relative boundary-rate error  = {rate_error:.3e}")
        print(f"Gamma*t                       = {secular_parameter:.3e}")

        assert factor_error < 1e-14
        assert mass_error < 1e-11
        assert shift < 0.0
        assert 0.0 < residue < 1.0
        assert rate > 0.0
        assert rate_error < 0.05
        assert secular_parameter < 0.25

    spin_one = measures[1]
    spin_two = measures[2]
    density_ratio = spin_two.compiled_density(LEVEL_GAP) / spin_one.compiled_density(
        LEVEL_GAP
    )
    expected_ratio = (
        spin_two.angular_response / spin_one.angular_response
    ) * LEVEL_GAP**2

    # The same measure also owns the finite-time kernel.  At t=0 its memory is
    # the measure mass; this catches accidental use of a second prescribed bath.
    memory_error = abs(
        memory(spin_two, 0.0) - COUPLING**2 * spin_two.analytic_mass()
    )

    assert spin_one.density_power == 3
    assert spin_two.density_power == 5
    assert abs(density_ratio - expected_ratio) < 1e-13
    assert memory_error < 1e-12

    anisotropic_refusal = None
    try:
        CurvatureDetectorMeasure(
            2,
            CUTOFF,
            DetectorContraction(0.5, 0.5, isotropic_smearing=False),
        )
    except ConstructionRefusal as error:
        anisotropic_refusal = str(error)
    blind_refusal = None
    try:
        CurvatureDetectorMeasure(2, CUTOFF, DetectorContraction(0.0, 0.0))
    except ConstructionRefusal as error:
        blind_refusal = str(error)
    assert anisotropic_refusal is not None
    assert blind_refusal is not None

    print("\ntransfer and same-measure checks")
    print(f"rho_2(Omega)/rho_1(Omega)      = {density_ratio:.15f}")
    print(f"generated expectation          = {expected_ratio:.15f}")
    print(f"memory mass error              = {memory_error:.3e}")
    print(f"anisotropic scalar refusal     = {anisotropic_refusal}")
    print(f"blind detector refusal         = {blind_refusal}")
    print("all curvature-detector acceptance checks passed")


if __name__ == "__main__":
    main()

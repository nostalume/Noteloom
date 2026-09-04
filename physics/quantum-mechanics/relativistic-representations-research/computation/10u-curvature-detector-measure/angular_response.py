"""Invariant angular-response compiler for the N10u curvature detector.

The detector supplies its squared norms in the two chiral spin-s summands.  The
compiler derives the sphere-average coefficient from covariance and trace; it
does not accept the final angular response as input.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


class ConstructionRefusal(ValueError):
    """The requested scalar angular quotient is not justified by the inputs."""


@dataclass(frozen=True)
class DetectorContraction:
    plus_norm_squared: float
    minus_norm_squared: float
    isotropic_smearing: bool = True

    def __post_init__(self) -> None:
        if self.plus_norm_squared < 0.0 or self.minus_norm_squared < 0.0:
            raise ValueError("chiral squared norms must be nonnegative")

    @property
    def total_norm_squared(self) -> float:
        return self.plus_norm_squared + self.minus_norm_squared


@dataclass(frozen=True)
class ScalarDetectorContraction:
    norm_squared: float
    isotropic_smearing: bool = True

    def __post_init__(self) -> None:
        if self.norm_squared < 0.0:
            raise ValueError("the scalar squared norm must be nonnegative")


@dataclass(frozen=True)
class AngularResponse:
    spin: int
    irrep_dimension: int
    sphere_volume: float
    frame_constant: float
    detector_norm_squared: float
    response: float
    certificate: str


def compile_angular_response(
    spin: int, detector: DetectorContraction
) -> AngularResponse:
    if spin < 1:
        raise ConstructionRefusal("positive integer spin is required")
    if not detector.isotropic_smearing:
        raise ConstructionRefusal(
            "anisotropic smearing does not commute with rotations; retain the "
            "direction-dependent positive operator instead of a scalar response"
        )
    if detector.total_norm_squared == 0.0:
        raise ConstructionRefusal(
            "the detector contraction is zero on both physical chiral summands"
        )

    # Each chiral curvature summand restricts to the irreducible spin-s rotation
    # module.  The sphere average of its covariant rank-one shell projectors
    # commutes with that action, hence is c I.  Taking the trace constructs c.
    irrep_dimension = 2 * spin + 1
    sphere_volume = 4.0 * math.pi
    frame_constant = sphere_volume / irrep_dimension
    response = frame_constant * detector.total_norm_squared

    return AngularResponse(
        spin=spin,
        irrep_dimension=irrep_dimension,
        sphere_volume=sphere_volume,
        frame_constant=frame_constant,
        detector_norm_squared=detector.total_norm_squared,
        response=response,
        certificate=(
            "covariance makes the shell-projector average an intertwiner; "
            "irreducibility makes it scalar; trace fixes 4*pi/(2s+1)"
        ),
    )


def compile_scalar_angular_response(
    detector: ScalarDetectorContraction,
) -> AngularResponse:
    if not detector.isotropic_smearing:
        raise ConstructionRefusal(
            "anisotropic scalar smearing retains its directional weight"
        )
    if detector.norm_squared == 0.0:
        raise ConstructionRefusal(
            "the detector contraction is zero on the scalar physical fiber"
        )

    sphere_volume = 4.0 * math.pi
    return AngularResponse(
        spin=0,
        irrep_dimension=1,
        sphere_volume=sphere_volume,
        frame_constant=sphere_volume,
        detector_norm_squared=detector.norm_squared,
        response=sphere_volume * detector.norm_squared,
        certificate=(
            "the scalar physical fiber is one-dimensional; integrating its "
            "identity shell projector gives 4*pi without duplicating chiral lines"
        ),
    )

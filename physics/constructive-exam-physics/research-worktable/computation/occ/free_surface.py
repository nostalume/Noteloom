import math
from collections.abc import Sequence

from ._parameterized_contracts import (
    Certificate,
    CompilationResult,
    Obstruction,
    ParameterizedHeader,
    RouteStep,
    refused,
    solved,
)


_ADAPTER = "mechanics.rotating_free_surface"
_OBJECTS = {"rotating_frame", "steady_free_surface"}
_OBSERVABLE = "signed_surface_height_difference"
_FIELDS = (
    "angular_speed_rad_s",
    "latitude_rad",
    "velocity_enu_m_s",
    "cross_channel_enu",
    "width_m",
    "gravity_m_s2",
)
_ROUTE = (
    RouteStep(
        operation="construct_rotation_vector",
        witness="Earth rotation in ENU is (0, Omega cos(latitude), Omega sin(latitude)).",
    ),
    RouteStep(
        operation="coriolis_cross_product",
        witness="The rotating-frame acceleration is -2 Omega cross velocity.",
    ),
    RouteStep(
        operation="steady_free_surface_balance",
        witness="Constant surface pressure gives horizontal grad(h)=a_horizontal/g.",
    ),
    RouteStep(
        operation="project_across_channel",
        witness="The signed height is grad(h) dotted with the cross-channel displacement.",
    ),
)


def admit(header: ParameterizedHeader) -> ParameterizedHeader | None:
    if not _OBJECTS.issubset(header.objects) or header.observable != _OBSERVABLE:
        return None
    return header


def _cross(left: Sequence[float], right: Sequence[float]) -> tuple[float, float, float]:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def _dot(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def _norm(vector: Sequence[float]) -> float:
    return math.sqrt(_dot(vector, vector))


def _invalid(message: str, *fields: str) -> CompilationResult:
    return refused(
        _ADAPTER,
        Obstruction(code="invalid_field", message=message, fields=tuple(fields)),
    )


def solve(request: ParameterizedHeader) -> CompilationResult:
    parameters = request.parameters
    missing = tuple(field for field in _FIELDS if field not in parameters)
    if missing:
        return refused(
            _ADAPTER,
            Obstruction(
                code="missing_field",
                message="The rotating free-surface balance is underdetermined.",
                fields=missing,
            ),
        )

    try:
        angular_speed = float(parameters["angular_speed_rad_s"])
        latitude = float(parameters["latitude_rad"])
        velocity = tuple(float(value) for value in parameters["velocity_enu_m_s"])
        cross_channel = tuple(float(value) for value in parameters["cross_channel_enu"])
        width = float(parameters["width_m"])
        gravity = float(parameters["gravity_m_s2"])
    except (TypeError, ValueError):
        return _invalid("Mechanics parameters must be real numeric values.", *_FIELDS)

    if len(velocity) != 3 or len(cross_channel) != 3:
        return _invalid(
            "ENU vectors must have exactly three components.",
            "velocity_enu_m_s",
            "cross_channel_enu",
        )
    if not all(
        math.isfinite(value)
        for value in (
            angular_speed,
            latitude,
            width,
            gravity,
            *velocity,
            *cross_channel,
        )
    ):
        return _invalid("Mechanics parameters must be finite.", *_FIELDS)
    if angular_speed < 0 or width <= 0 or gravity <= 0:
        return _invalid(
            "Angular speed must be nonnegative; width and gravity must be positive.",
            "angular_speed_rad_s",
            "width_m",
            "gravity_m_s2",
        )
    if abs(velocity[2]) > 1e-12:
        return _invalid(
            "The present slice admits horizontal flow only.", "velocity_enu_m_s"
        )
    if abs(cross_channel[2]) > 1e-12 or not math.isclose(
        _norm(cross_channel), 1.0, rel_tol=0.0, abs_tol=1e-12
    ):
        return _invalid(
            "The cross-channel direction must be a horizontal unit vector.",
            "cross_channel_enu",
        )

    rotation = (
        0.0,
        angular_speed * math.cos(latitude),
        angular_speed * math.sin(latitude),
    )
    omega_cross_v = _cross(rotation, velocity)
    coriolis = tuple(-2.0 * component for component in omega_cross_v)
    horizontal_acceleration = (coriolis[0], coriolis[1], 0.0)
    surface_gradient = tuple(
        component / gravity for component in horizontal_acceleration
    )
    displacement = tuple(width * component for component in cross_channel)
    height_difference = _dot(surface_gradient, displacement)
    projected_acceleration = _dot(horizontal_acceleration, cross_channel)
    residual = gravity * height_difference / width - projected_acceleration

    certificates = (
        Certificate(
            name="free_surface_residual",
            passed=math.isclose(residual, 0.0, rel_tol=0.0, abs_tol=1e-15),
            witness=f"g*Delta_h/width - a_horizontal.cross_direction = {residual!r}",
        ),
        Certificate(
            name="horizontal_geometry",
            passed=abs(surface_gradient[2]) <= 1e-15,
            witness="The computed free-surface gradient has zero vertical component.",
        ),
        Certificate(
            name="finite_observable",
            passed=math.isfinite(height_difference),
            witness=f"signed height difference = {height_difference!r} m",
        ),
    )
    return solved(
        adapter=_ADAPTER,
        value={
            "signed_height_difference_m": height_difference,
            "surface_gradient_enu": surface_gradient,
            "coriolis_acceleration_enu_m_s2": coriolis,
        },
        route=_ROUTE,
        certificates=certificates,
    )

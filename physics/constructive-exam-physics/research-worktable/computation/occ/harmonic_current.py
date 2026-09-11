import math

from ._parameterized_contracts import (
    Certificate,
    CompilationResult,
    Obstruction,
    ParameterizedHeader,
    RouteStep,
    refused,
    solved,
)


_ADAPTER = "electromagnetism.harmonic_response"
_ISOTROPIC = "linear_isotropic_medium"
_ANISOTROPIC = "linear_anisotropic_medium"
_COMMON_OBJECTS = {
    "time_harmonic_electric_field",
    "conduction_current",
    "displacement_current",
}
_OBSERVABLES = {"rms_current_density_ratio", "crossover_angular_frequency"}
_CONSTITUTIVE_ROUTE = (
    RouteStep(
        operation="construct_constitutive_pair",
        witness="J_cond=sigma E and J_disp=d(epsilon E)/dt are evaluated on one field.",
    ),
    RouteStep(
        operation="phasor_time_derivative",
        witness="Time differentiation multiplies the field phasor by i*omega.",
    ),
)
_RATIO_STEP = RouteStep(
    operation="recover_rms_magnitude_ratio",
    witness="The common field magnitude and RMS factor cancel.",
)
_CROSSOVER_STEP = RouteStep(
    operation="solve_equal_magnitude_condition",
    witness="|sigma E|=|i omega epsilon E| gives omega=sigma/epsilon.",
)


def admit(header: ParameterizedHeader) -> ParameterizedHeader | None:
    objects = header.objects
    has_medium = _ISOTROPIC in objects or _ANISOTROPIC in objects
    if not (
        has_medium
        and _COMMON_OBJECTS.issubset(objects)
        and header.observable in _OBSERVABLES
    ):
        return None
    return header


def _refuse(code: str, message: str, *fields: str) -> CompilationResult:
    return refused(
        _ADAPTER,
        Obstruction(code=code, message=message, fields=tuple(fields)),
    )


def solve(request: ParameterizedHeader) -> CompilationResult:
    objects = request.objects
    observable = request.observable
    if _ANISOTROPIC in objects and observable == "rms_current_density_ratio":
        return _refuse(
            "nonunique_observable",
            "Tensor response does not define one scalar ratio without a field direction and norm.",
            "field_direction",
            "norm",
        )
    if _ANISOTROPIC in objects:
        return _refuse(
            "unsupported_representation",
            "The present executable slice admits scalar constitutive response only.",
        )

    parameters = request.parameters
    required = ["conductivity_s_m", "permittivity_f_m"]
    if observable == "rms_current_density_ratio":
        required.append("angular_frequency_rad_s")
    missing = tuple(field for field in required if field not in parameters)
    if missing:
        return _refuse(
            "missing_field",
            "The harmonic-response observable is underdetermined.",
            *missing,
        )
    try:
        conductivity = float(parameters["conductivity_s_m"])
        permittivity = float(parameters["permittivity_f_m"])
        angular_frequency = (
            float(parameters["angular_frequency_rad_s"])
            if observable == "rms_current_density_ratio"
            else None
        )
    except (TypeError, ValueError):
        return _refuse("invalid_field", "Constitutive parameters must be real scalars.")

    scalars = [conductivity, permittivity]
    if angular_frequency is not None:
        scalars.append(angular_frequency)
    if not all(math.isfinite(value) and value > 0 for value in scalars):
        return _refuse(
            "invalid_field",
            "Conductivity, permittivity, and any supplied frequency must be finite and positive.",
        )

    if observable == "rms_current_density_ratio":
        assert angular_frequency is not None
        ratio = conductivity / (angular_frequency * permittivity)
        residual = ratio * angular_frequency * permittivity - conductivity
        value = {"rms_ratio": ratio, "phase_difference_rad": math.pi / 2}
        route = _CONSTITUTIVE_ROUTE + (_RATIO_STEP,)
    else:
        crossover = conductivity / permittivity
        residual = crossover * permittivity - conductivity
        value = {"angular_frequency_rad_s": crossover}
        route = _CONSTITUTIVE_ROUTE + (_CROSSOVER_STEP,)

    certificates = (
        Certificate(
            name="constitutive_scalar_domain",
            passed=_ISOTROPIC in objects,
            witness="Both constitutive maps are positive scalar multiplications.",
        ),
        Certificate(
            name="observable_recovery_residual",
            passed=math.isclose(
                residual + conductivity,
                conductivity,
                rel_tol=1e-15,
                abs_tol=1e-15,
            ),
            witness=(
                "Recovered constitutive equality normalized residual = "
                f"{residual / conductivity!r}."
            ),
        ),
    )
    return solved(_ADAPTER, value, route, certificates)

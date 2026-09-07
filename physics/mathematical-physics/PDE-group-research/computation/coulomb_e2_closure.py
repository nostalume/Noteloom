"""Exact closure/Casimir certificate consuming the generated E^2 Coulomb centralizer."""

from __future__ import annotations

import json
from fractions import Fraction

from radial_quadratic_centralizer import (
    ONE,
    RadialDiffOp,
    RadialExpr,
    generate,
    hamiltonian,
    quantum_operator,
    reconstruct_lower_term,
    vector_field_operator,
)

ROTATION = (Fraction(0), Fraction(0), Fraction(1))
RUNGE_LENZ_Y = (
    Fraction(0),
    Fraction(1),
    Fraction(0),
    Fraction(0),
    Fraction(0),
    Fraction(0),
)
RUNGE_LENZ_X = (
    Fraction(0),
    Fraction(0),
    Fraction(0),
    Fraction(1),
    Fraction(0),
    Fraction(0),
)


def build_certificate(kappa: Fraction = Fraction(1)) -> dict[str, object]:
    if kappa <= 0:
        return {"status": "Refused", "reason": "kappa must be positive"}
    potential = RadialExpr.monomial(s_power=Fraction(-1, 2), coefficient=-kappa)
    generated = generate(potential)
    parameter_vectors = {
        tuple(Fraction(value) for value in generator["parameters_abcdef"])
        for generator in generated["generators"]
    }
    required = {RUNGE_LENZ_X, RUNGE_LENZ_Y}
    if not required.issubset(parameter_vectors):
        return {
            "status": "Refused",
            "reason": "full centralizer did not generate both Runge--Lenz directions",
        }

    h_op = hamiltonian(potential)
    rotation = vector_field_operator(ROTATION)
    a_x = quantum_operator(RUNGE_LENZ_X, reconstruct_lower_term(potential, RUNGE_LENZ_X))
    a_y = quantum_operator(RUNGE_LENZ_Y, reconstruct_lower_term(potential, RUNGE_LENZ_Y))
    identity = RadialDiffOp.multiplication(ONE)
    physical_l_squared = rotation.compose(rotation).scale(-1)

    checks = {
        "[J0,A_x]=-A_y": not (rotation.compose(a_x) - a_x.compose(rotation) + a_y).terms,
        "[J0,A_y]=A_x": not (rotation.compose(a_y) - a_y.compose(rotation) - a_x).terms,
        "[A_x,A_y]=-2 H J0": not (
            a_x.compose(a_y) - a_y.compose(a_x) + h_op.compose(rotation).scale(2)
        ).terms,
        "A^2=2H(L^2+1/4)+kappa^2": not (
            a_x.compose(a_x)
            + a_y.compose(a_y)
            - h_op.compose(physical_l_squared + identity.scale(Fraction(1, 4))).scale(2)
            - identity.scale(kappa * kappa)
        ).terms,
    }
    return {
        "status": "Passed" if all(checks.values()) else "Failed",
        "input": {"dimension": 2, "kappa": str(kappa), "units": "mu=hbar=1"},
        "generated_kernel_dimension": generated["kernel_dimension"],
        "generated_first_order_dimension": generated["first_order_kernel_dimension"],
        "checks": checks,
        "energy_shell_output": {
            "negative_energy_real_form": "so(3)",
            "casimir": "j(j+1)=-1/4-kappa^2/(2E)",
            "energy": "E_j=-kappa^2/(2(j+1/2)^2)",
            "scalar_single_valued_labels": "j=0,1,2,...",
            "degeneracy": "2j+1",
        },
        "not_certified": [
            "existence and completeness of the bound eigenspaces",
            "self-adjoint domains at r=0 and infinity",
            "the three-dimensional so(4) transfer",
        ],
    }


if __name__ == "__main__":
    certificate = build_certificate()
    print(json.dumps(certificate, indent=2, sort_keys=True))
    raise SystemExit(0 if certificate["status"] == "Passed" else 1)

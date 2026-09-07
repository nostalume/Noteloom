"""Exact so(4) closure/Casimir certificate from the generated E^3 centralizer."""

from __future__ import annotations

import json
from fractions import Fraction

from quadratic_centralizer import rank
from radial_quadratic_centralizer_e3 import (
    NDDiffOp,
    NDExpr,
    compatibility_obstruction,
    coordinate,
    euclidean_killing_vectors,
    generate,
    hamiltonian,
    quantum_operator,
    reconstruct_lower_term,
    symmetric_tensor,
    tensor_add,
    tensor_scale,
    vector_operator,
)


def _commutator(left: NDDiffOp, right: NDDiffOp) -> NDDiffOp:
    return left.compose(right) - right.compose(left)


def _sum_operators(operators: list[NDDiffOp]) -> NDDiffOp:
    if not operators:
        raise ValueError("at least one operator is required")
    return sum(operators[1:], operators[0])


def _levi_civita(i: int, j: int, k: int) -> int:
    if len({i, j, k}) < 3:
        return 0
    return 1 if (i, j, k) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1


def _coefficient_vector(basis: list[str], terms: dict[str, int]) -> tuple[Fraction, ...]:
    return tuple(Fraction(terms.get(label, 0)) for label in basis)


def build_certificate(kappa: Fraction = Fraction(1)) -> dict[str, object]:
    if kappa <= 0:
        return {"status": "Refused", "reason": "kappa must be positive"}

    dimension = 3
    radial_inverse = NDExpr.monomial(dimension, s_power=Fraction(-1, 2))
    potential = radial_inverse.scale(-kappa)
    generated = generate(potential)
    if (
        generated["quadratic_module_dimension"] != 20
        or generated["quadratic_kernel_dimension"] != 10
    ):
        return {
            "status": "Refused",
            "reason": "complete centralizer did not return the 20-to-10 Coulomb reduction",
        }

    vectors = dict(euclidean_killing_vectors())
    rotations = [vector_operator(vectors[name]) for name in ("R_x", "R_y", "R_z")]
    runge_lenz_specs = (
        (("P_y", "R_z", 2), ("P_z", "R_y", -2)),
        (("P_z", "R_x", 2), ("P_x", "R_z", -2)),
        (("P_x", "R_y", 2), ("P_y", "R_x", -2)),
    )
    runge_lenz_tensors = []
    for terms in runge_lenz_specs:
        left = tensor_scale(
            symmetric_tensor(vectors[terms[0][0]], vectors[terms[0][1]]), terms[0][2]
        )
        right = tensor_scale(
            symmetric_tensor(vectors[terms[1][0]], vectors[terms[1][1]]), terms[1][2]
        )
        runge_lenz_tensors.append(tensor_add(left, right))

    lower_terms = [reconstruct_lower_term(potential, tensor) for tensor in runge_lenz_tensors]
    expected_lower_terms = [
        coordinate(dimension, index) * radial_inverse.scale(-kappa) for index in range(dimension)
    ]
    runge_lenz = [
        quantum_operator(tensor, lower) for tensor, lower in zip(runge_lenz_tensors, lower_terms)
    ]
    h_op = hamiltonian(potential)
    identity = NDDiffOp.multiplication(NDExpr.constant(dimension, 1))

    module_basis = generated["quadratic_basis"]
    named_coefficient_vectors = (
        _coefficient_vector(module_basis, {"P_y*R_z": 2, "P_z*R_y": -2}),
        _coefficient_vector(module_basis, {"P_z*R_x": 2, "P_x*R_z": -2}),
        _coefficient_vector(module_basis, {"P_x*R_y": 2, "P_y*R_x": -2}),
    )
    discovered_kernel = [
        tuple(Fraction(value) for value in generator["coefficients"])
        for generator in generated["generators"]
    ]
    runge_lenz_in_discovered_kernel = all(
        rank([*discovered_kernel, vector]) == len(discovered_kernel)
        for vector in named_coefficient_vectors
    )

    checks: dict[str, bool] = {
        "Sym^2(e3):21->20": generated["quadratic_presented_dimension"] == 21
        and generated["presentation_redundancy_dimension"] == 1,
        "Coulomb:20->10": generated["quadratic_kernel_dimension"] == 10,
        "three_rotations_selected": generated["first_order_kernel_dimension"] == 3,
        "Runge--Lenz_in_discovered_kernel": runge_lenz_in_discovered_kernel,
        "dW=K_dV": lower_terms == expected_lower_terms
        and all(
            not any(component.terms for component in compatibility_obstruction(potential, tensor))
            for tensor in runge_lenz_tensors
        ),
        "[H,A_i]=0": all(not _commutator(h_op, operator).terms for operator in runge_lenz),
    }

    for i in range(3):
        for j in range(3):
            rotation_target = _sum_operators(
                [rotations[k].scale(-_levi_civita(i, j, k)) for k in range(3)]
            )
            vector_target = _sum_operators(
                [runge_lenz[k].scale(-_levi_civita(i, j, k)) for k in range(3)]
            )
            hidden_target = _sum_operators(
                [h_op.compose(rotations[k]).scale(-2 * _levi_civita(i, j, k)) for k in range(3)]
            )
            checks[f"[J_{i},J_{j}]=-epsilon J"] = not (
                _commutator(rotations[i], rotations[j]) - rotation_target
            ).terms
            checks[f"[J_{i},A_{j}]=-epsilon A"] = not (
                _commutator(rotations[i], runge_lenz[j]) - vector_target
            ).terms
            checks[f"[A_{i},A_{j}]=-2H epsilon J"] = not (
                _commutator(runge_lenz[i], runge_lenz[j]) - hidden_target
            ).terms

    physical_l_squared = _sum_operators(
        [rotation.compose(rotation).scale(-1) for rotation in rotations]
    )
    runge_lenz_squared = _sum_operators([operator.compose(operator) for operator in runge_lenz])
    checks["A^2=2H(L^2+1)+kappa^2"] = not (
        runge_lenz_squared
        - h_op.compose(physical_l_squared + identity).scale(2)
        - identity.scale(kappa * kappa)
    ).terms
    checks["L_dot_A=A_dot_L=0"] = (
        not _sum_operators([rotations[i].compose(runge_lenz[i]) for i in range(3)]).terms
        and not _sum_operators([runge_lenz[i].compose(rotations[i]) for i in range(3)]).terms
    )

    return {
        "status": "Passed" if all(checks.values()) else "Failed",
        "input": {"dimension": 3, "kappa": str(kappa), "units": "mu=hbar=1"},
        "generated_module_dimension": generated["quadratic_module_dimension"],
        "generated_kernel_dimension": generated["quadratic_kernel_dimension"],
        "generated_first_order_dimension": generated["first_order_kernel_dimension"],
        "checks": checks,
        "energy_shell_output": {
            "negative_energy_real_form": "so(4)=su(2)+su(2)",
            "equal_spins": "j_+=j_-=j",
            "principal_quantum_number": "n=2j+1=1,2,3,...",
            "energy": "E_n=-kappa^2/(2n^2)",
            "degeneracy": "n^2",
        },
        "not_certified": [
            "existence and completeness of the bound eigenspaces",
            "self-adjoint domains at r=0 and infinity",
            "higher-order or spinorial centralizers",
        ],
    }


if __name__ == "__main__":
    certificate = build_certificate()
    print(json.dumps(certificate, indent=2, sort_keys=True))
    raise SystemExit(0 if certificate["status"] == "Passed" else 1)

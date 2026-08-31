"""Finite-Fock-space checks for N8c's dephased quantum/SSEP bridge."""

from __future__ import annotations

import math


SITES = 4
HOPPING = 0.7
DEPHASING = 1.3
DENSITY = 0.37
TOLERANCE = 1.0e-11
DIMENSION = 1 << SITES


def zero_matrix():
    return [[0j for _ in range(DIMENSION)] for _ in range(DIMENSION)]


def add(left, right, left_scale=1.0, right_scale=1.0):
    return [
        [
            left_scale * left[row][column]
            + right_scale * right[row][column]
            for column in range(DIMENSION)
        ]
        for row in range(DIMENSION)
    ]


def multiply(left, right):
    product = zero_matrix()
    for row in range(DIMENSION):
        for middle in range(DIMENSION):
            coefficient = left[row][middle]
            if coefficient == 0j:
                continue
            for column in range(DIMENSION):
                if right[middle][column] != 0j:
                    product[row][column] += coefficient * right[middle][column]
    return product


def dagger(matrix):
    return [
        [matrix[column][row].conjugate() for column in range(DIMENSION)]
        for row in range(DIMENSION)
    ]


def scale(matrix, coefficient):
    return [[coefficient * entry for entry in row] for row in matrix]


def frobenius_norm(matrix):
    return math.sqrt(
        sum(abs(entry) ** 2 for row in matrix for entry in row)
    )


def annihilation(site):
    operator = zero_matrix()
    lower_mask = (1 << site) - 1
    for state in range(DIMENSION):
        if not state & (1 << site):
            continue
        target = state ^ (1 << site)
        parity = (state & lower_mask).bit_count()
        operator[target][state] = -1.0 if parity % 2 else 1.0
    return operator


ANNIHILATORS = [annihilation(site) for site in range(SITES)]
CREATORS = [dagger(operator) for operator in ANNIHILATORS]
OCCUPATIONS = [
    multiply(CREATORS[site], ANNIHILATORS[site])
    for site in range(SITES)
]


def hopping_hamiltonian():
    hamiltonian = zero_matrix()
    for left in range(SITES):
        right = (left + 1) % SITES
        transfer = multiply(CREATORS[right], ANNIHILATORS[left])
        hamiltonian = add(
            hamiltonian,
            add(transfer, dagger(transfer)),
            right_scale=-HOPPING,
        )
    return hamiltonian


HAMILTONIAN = hopping_hamiltonian()


def commutator(left, right):
    return add(multiply(left, right), multiply(right, left), right_scale=-1.0)


def coherent_generator(matrix):
    return scale(commutator(HAMILTONIAN, matrix), -1j)


def dephasing_generator(matrix):
    result = zero_matrix()
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            distance = (row ^ column).bit_count()
            result[row][column] = (
                -0.5 * DEPHASING * distance * matrix[row][column]
            )
    return result


def adjoint_generator(observable):
    return add(
        scale(commutator(HAMILTONIAN, observable), 1j),
        dephasing_generator(observable),
    )


def diagonal_projection(matrix):
    result = zero_matrix()
    for state in range(DIMENSION):
        result[state][state] = matrix[state][state]
    return result


def inverse_dephasing_on_complement(matrix):
    result = zero_matrix()
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            if row == column or matrix[row][column] == 0j:
                continue
            distance = (row ^ column).bit_count()
            eigenvalue = -0.5 * DEPHASING * distance
            result[row][column] = matrix[row][column] / eigenvalue
    return result


def bond_current(left):
    right = (left + 1) % SITES
    transfer = multiply(CREATORS[right], ANNIHILATORS[left])
    return scale(
        add(transfer, dagger(transfer), right_scale=-1.0),
        1j * HOPPING,
    )


def sum_matrices(matrices):
    total = zero_matrix()
    for matrix in matrices:
        total = add(total, matrix)
    return total


def effective_population_generator():
    generator = [
        [0.0 for _ in range(DIMENSION)] for _ in range(DIMENSION)
    ]
    for state in range(DIMENSION):
        projector = zero_matrix()
        projector[state][state] = 1.0
        first_coherence = coherent_generator(projector)
        eliminated = inverse_dephasing_on_complement(first_coherence)
        effective_state = scale(
            diagonal_projection(coherent_generator(eliminated)), -1.0
        )
        for target in range(DIMENSION):
            generator[target][state] = effective_state[target][target].real
    return generator


def ssep_generator():
    rate = 2.0 * HOPPING * HOPPING / DEPHASING
    generator = [
        [0.0 for _ in range(DIMENSION)] for _ in range(DIMENSION)
    ]
    for state in range(DIMENSION):
        for left in range(SITES):
            right = (left + 1) % SITES
            left_bit = (state >> left) & 1
            right_bit = (state >> right) & 1
            if left_bit == right_bit:
                continue
            target = state ^ (1 << left) ^ (1 << right)
            generator[target][state] += rate
            generator[state][state] -= rate
    return generator


def real_matrix_norm(matrix):
    return math.sqrt(sum(entry * entry for row in matrix for entry in row))


def equilibrium_probabilities():
    return [
        DENSITY ** state.bit_count()
        * (1.0 - DENSITY) ** (SITES - state.bit_count())
        for state in range(DIMENSION)
    ]


def diagonal_expectation(probabilities, observable):
    return sum(
        probabilities[state] * observable[state][state]
        for state in range(DIMENSION)
    )


def main():
    currents = [bond_current(site) for site in range(SITES)]
    total_current = sum_matrices(currents)

    continuity_error = 0.0
    for site, occupation in enumerate(OCCUPATIONS):
        divergence = add(
            currents[(site - 1) % SITES], currents[site], right_scale=-1.0
        )
        difference = add(
            adjoint_generator(occupation), divergence, right_scale=-1.0
        )
        continuity_error = max(continuity_error, frobenius_norm(difference))

    current_commutator_error = frobenius_norm(
        commutator(HAMILTONIAN, total_current)
    )
    current_decay_error = frobenius_norm(
        add(adjoint_generator(total_current), total_current, right_scale=DEPHASING)
    )

    probabilities = equilibrium_probabilities()
    total_number = sum_matrices(OCCUPATIONS)
    number_squared = multiply(total_number, total_number)
    mean_number = diagonal_expectation(probabilities, total_number).real
    variance_number = (
        diagonal_expectation(probabilities, number_squared).real
        - mean_number * mean_number
    ) / SITES
    susceptibility = DENSITY * (1.0 - DENSITY)
    susceptibility_error = abs(variance_number - susceptibility)

    current_squared = multiply(total_current, total_current)
    current_covariance = (
        diagonal_expectation(probabilities, current_squared).real / SITES
    )
    expected_covariance = 2.0 * HOPPING * HOPPING * susceptibility
    covariance_error = abs(current_covariance - expected_covariance)

    effective = effective_population_generator()
    expected = ssep_generator()
    effective_difference = [
        [
            effective[row][column] - expected[row][column]
            for column in range(DIMENSION)
        ]
        for row in range(DIMENSION)
    ]
    effective_error = real_matrix_norm(effective_difference)
    conservation_error = max(
        abs(sum(effective[row][column] for row in range(DIMENSION)))
        for column in range(DIMENSION)
    )
    minimum_rate = min(
        effective[row][column]
        for row in range(DIMENSION)
        for column in range(DIMENSION)
        if row != column
    )

    diffusion_green_kubo = current_covariance / (
        susceptibility * DEPHASING
    )
    diffusion_ssep = 2.0 * HOPPING * HOPPING / DEPHASING

    print(f"sites={SITES} dimension={DIMENSION}")
    print(f"J={HOPPING:.6f} gamma={DEPHASING:.6f} rho={DENSITY:.6f}")
    print(f"continuity_error={continuity_error:.3e}")
    print(f"[H,J_total]_error={current_commutator_error:.3e}")
    print(f"current_decay_error={current_decay_error:.3e}")
    print(f"susceptibility={susceptibility:.12f} error={susceptibility_error:.3e}")
    print(
        f"current_covariance_per_site={current_covariance:.12f} "
        f"error={covariance_error:.3e}"
    )
    print(f"effective_SSEP_error={effective_error:.3e}")
    print(f"probability_conservation_error={conservation_error:.3e}")
    print(f"minimum_off_diagonal_rate={minimum_rate:.12f}")
    print(f"D_Green_Kubo={diffusion_green_kubo:.12f}")
    print(f"D_SSEP={diffusion_ssep:.12f}")

    errors = (
        continuity_error,
        current_commutator_error,
        current_decay_error,
        susceptibility_error,
        covariance_error,
        effective_error,
        conservation_error,
        abs(diffusion_green_kubo - diffusion_ssep),
    )
    if max(errors) >= TOLERANCE:
        raise AssertionError(f"algebra check failed: max error {max(errors):.3e}")
    if minimum_rate < -1.0e-12:
        raise AssertionError("effective generator has a negative jump rate")
    print("all acceptance criteria passed")


if __name__ == "__main__":
    main()

"""Finite-chain TPM charge statistics for N8d."""

from __future__ import annotations

import cmath
import math


SITES = 4
DIMENSION = 1 << SITES
HOPPING = 0.7
DENSITY = 0.5
SLOW_TIME = 0.75
DEPHASINGS = (0.5, 1.0, 2.0, 4.0, 8.0)
FOURIER_POINTS = 5


def zero_matrix():
    return [[0j for _ in range(DIMENSION)] for _ in range(DIMENSION)]


def matrix_add(*terms):
    result = zero_matrix()
    for coefficient, matrix in terms:
        for row in range(DIMENSION):
            for column in range(DIMENSION):
                result[row][column] += coefficient * matrix[row][column]
    return result


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


def dagger(matrix):
    return [
        [matrix[column][row].conjugate() for column in range(DIMENSION)]
        for row in range(DIMENSION)
    ]


def multiply(left, right):
    result = zero_matrix()
    for row in range(DIMENSION):
        for middle in range(DIMENSION):
            coefficient = left[row][middle]
            if coefficient == 0j:
                continue
            for column in range(DIMENSION):
                if right[middle][column] != 0j:
                    result[row][column] += coefficient * right[middle][column]
    return result


ANNIHILATORS = [annihilation(site) for site in range(SITES)]
CREATORS = [dagger(operator) for operator in ANNIHILATORS]


def open_hamiltonian():
    hamiltonian = zero_matrix()
    for left in range(SITES - 1):
        right = left + 1
        transfer = multiply(CREATORS[right], ANNIHILATORS[left])
        reverse = dagger(transfer)
        hamiltonian = matrix_add(
            (1.0, hamiltonian),
            (-HOPPING, transfer),
            (-HOPPING, reverse),
        )
    return hamiltonian


HAMILTONIAN = open_hamiltonian()
HAMILTONIAN_ROWS = [
    [(column, value) for column, value in enumerate(row) if value != 0j]
    for row in HAMILTONIAN
]


def right_charge(state):
    return ((state >> 2) & 1) + ((state >> 3) & 1)


RIGHT_CHARGES = [right_charge(state) for state in range(DIMENSION)]


def equilibrium_probabilities():
    return [
        DENSITY ** state.bit_count()
        * (1.0 - DENSITY) ** (SITES - state.bit_count())
        for state in range(DIMENSION)
    ]


EQUILIBRIUM = equilibrium_probabilities()


def liouvillian(matrix, dephasing):
    result = zero_matrix()
    for row in range(DIMENSION):
        for middle, coefficient in HAMILTONIAN_ROWS[row]:
            for column in range(DIMENSION):
                result[row][column] -= 1j * coefficient * matrix[middle][column]
    for middle in range(DIMENSION):
        for column, coefficient in HAMILTONIAN_ROWS[middle]:
            for row in range(DIMENSION):
                result[row][column] += 1j * matrix[row][middle] * coefficient
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            distance = (row ^ column).bit_count()
            result[row][column] -= (
                0.5 * dephasing * distance * matrix[row][column]
            )
    return result


def rk4_matrix(initial, total_time, dephasing, step_size):
    steps = max(1, math.ceil(total_time / step_size))
    step = total_time / steps
    state = initial
    for _ in range(steps):
        k1 = liouvillian(state, dephasing)
        k2 = liouvillian(matrix_add((1.0, state), (0.5 * step, k1)), dephasing)
        k3 = liouvillian(matrix_add((1.0, state), (0.5 * step, k2)), dephasing)
        k4 = liouvillian(matrix_add((1.0, state), (step, k3)), dephasing)
        state = matrix_add(
            (1.0, state),
            (step / 6.0, k1),
            (step / 3.0, k2),
            (step / 3.0, k3),
            (step / 6.0, k4),
        )
    return state


def quantum_characteristic(angle, dephasing, step_scale=1.0):
    initial = zero_matrix()
    for state, probability in enumerate(EQUILIBRIUM):
        initial[state][state] = probability * cmath.exp(
            -1j * angle * RIGHT_CHARGES[state]
        )
    rate = 2.0 * HOPPING * HOPPING / dephasing
    total_time = SLOW_TIME / rate
    base_step = min(0.01, 0.08 / (SITES * dephasing + 4.0 * HOPPING))
    evolved = rk4_matrix(initial, total_time, dephasing, base_step * step_scale)
    return sum(
        cmath.exp(1j * angle * RIGHT_CHARGES[state])
        * evolved[state][state]
        for state in range(DIMENSION)
    )


def ssep_generator_action(vector):
    result = [0j for _ in range(DIMENSION)]
    for state, weight in enumerate(vector):
        if weight == 0j:
            continue
        for left in range(SITES - 1):
            right = left + 1
            if ((state >> left) & 1) == ((state >> right) & 1):
                continue
            target = state ^ (1 << left) ^ (1 << right)
            result[target] += weight
            result[state] -= weight
    return result


def vector_add(*terms):
    return [
        sum(coefficient * vector[index] for coefficient, vector in terms)
        for index in range(DIMENSION)
    ]


def rk4_vector(initial, total_time, step_size=0.002):
    steps = max(1, math.ceil(total_time / step_size))
    step = total_time / steps
    state = initial
    for _ in range(steps):
        k1 = ssep_generator_action(state)
        k2 = ssep_generator_action(vector_add((1.0, state), (0.5 * step, k1)))
        k3 = ssep_generator_action(vector_add((1.0, state), (0.5 * step, k2)))
        k4 = ssep_generator_action(vector_add((1.0, state), (step, k3)))
        state = vector_add(
            (1.0, state),
            (step / 6.0, k1),
            (step / 3.0, k2),
            (step / 3.0, k3),
            (step / 6.0, k4),
        )
    return state


def ssep_characteristic(angle):
    initial = [
        probability * cmath.exp(-1j * angle * RIGHT_CHARGES[state])
        for state, probability in enumerate(EQUILIBRIUM)
    ]
    evolved = rk4_vector(initial, SLOW_TIME)
    return sum(
        cmath.exp(1j * angle * RIGHT_CHARGES[state]) * evolved[state]
        for state in range(DIMENSION)
    )


def distribution_from_characteristic(characteristic):
    distribution = {}
    maximum_imaginary = 0.0
    for charge in range(-2, 3):
        value = sum(
            characteristic[index]
            * cmath.exp(
                -1j * 2.0 * math.pi * index * charge / FOURIER_POINTS
            )
            for index in range(FOURIER_POINTS)
        ) / FOURIER_POINTS
        maximum_imaginary = max(maximum_imaginary, abs(value.imag))
        distribution[charge] = value.real
    return distribution, maximum_imaginary


def adjoint_symmetric_samples(evaluator):
    samples = [0j for _ in range(FOURIER_POINTS)]
    samples[0] = evaluator(0.0)
    for index in (1, 2):
        angle = 2.0 * math.pi * index / FOURIER_POINTS
        samples[index] = evaluator(angle)
        samples[FOURIER_POINTS - index] = samples[index].conjugate()
    return samples


def quantum_distribution(dephasing, step_scale=1.0):
    characteristic = adjoint_symmetric_samples(
        lambda angle: quantum_characteristic(
            angle, dephasing, step_scale
        )
    )
    return distribution_from_characteristic(characteristic)


def ssep_distribution():
    characteristic = adjoint_symmetric_samples(ssep_characteristic)
    return distribution_from_characteristic(characteristic)


def cumulants(distribution):
    mean = sum(charge * probability for charge, probability in distribution.items())
    centered_2 = sum(
        (charge - mean) ** 2 * probability
        for charge, probability in distribution.items()
    )
    centered_3 = sum(
        (charge - mean) ** 3 * probability
        for charge, probability in distribution.items()
    )
    centered_4 = sum(
        (charge - mean) ** 4 * probability
        for charge, probability in distribution.items()
    )
    return mean, centered_2, centered_3, centered_4 - 3.0 * centered_2**2


def total_variation(left, right):
    return 0.5 * sum(
        abs(left[charge] - right[charge]) for charge in range(-2, 3)
    )


def format_distribution(distribution):
    return " ".join(
        f"P({charge:+d})={distribution[charge]:.9f}"
        for charge in range(-2, 3)
    )


def validate_distribution(distribution, imaginary_leakage):
    normalization = abs(sum(distribution.values()) - 1.0)
    minimum_probability = min(distribution.values())
    mean, _, third, _ = cumulants(distribution)
    if normalization >= 1.0e-9:
        raise AssertionError(f"normalization error {normalization:.3e}")
    if imaginary_leakage >= 1.0e-9:
        raise AssertionError(f"imaginary leakage {imaginary_leakage:.3e}")
    if minimum_probability < -1.0e-9:
        raise AssertionError(f"negative probability {minimum_probability:.3e}")
    if max(abs(mean), abs(third)) >= 1.0e-8:
        raise AssertionError("equilibrium odd cumulant did not vanish")


def main():
    classical, classical_imaginary = ssep_distribution()
    validate_distribution(classical, classical_imaginary)
    classical_cumulants = cumulants(classical)
    print(f"sites={SITES} J={HOPPING} rho={DENSITY} tau={SLOW_TIME}")
    print("SSEP  " + format_distribution(classical))
    print(
        f"SSEP  kappa2={classical_cumulants[1]:.10f} "
        f"kappa4={classical_cumulants[3]:.10f}"
    )

    distances = []
    finest_distribution = None
    for dephasing in DEPHASINGS:
        distribution, imaginary = quantum_distribution(dephasing)
        validate_distribution(distribution, imaginary)
        values = cumulants(distribution)
        distance = total_variation(distribution, classical)
        distances.append(distance)
        print("\n" + f"gamma={dephasing:.1f} " + format_distribution(distribution))
        print(
            f"gamma={dephasing:.1f} kappa2={values[1]:.10f} "
            f"kappa4={values[3]:.10f} TV_to_SSEP={distance:.6e} "
            f"gamma^2*TV={dephasing * dephasing * distance:.6e}"
        )
        if dephasing == DEPHASINGS[-1]:
            finest_distribution, finest_imaginary = quantum_distribution(
                dephasing, step_scale=0.5
            )
            validate_distribution(finest_distribution, finest_imaginary)

    refinement_error = max(
        abs(finest_distribution[charge] - distribution[charge])
        for charge in range(-2, 3)
    )
    print(f"\nlargest-gamma refinement_error={refinement_error:.3e}")
    if refinement_error >= 2.0e-7:
        raise AssertionError("time-step refinement failed")
    if distances[-1] >= distances[0]:
        raise AssertionError("strong dephasing did not improve SSEP recovery")
    print("all acceptance criteria passed")


if __name__ == "__main__":
    main()

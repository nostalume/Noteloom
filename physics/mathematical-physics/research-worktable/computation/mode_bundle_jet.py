"""Exact connection and leakage jets for a transported irreducible carrier."""

from __future__ import annotations

from dataclasses import dataclass, replace

import exact_gaussian_matrix as gaussian
from exact_gaussian_linear import Vector, coordinates, linear_combination, matrix_vector, rank
from represented_star_algebra import StarGenerator
from simple_block_pde import IrreducibleModel


class ModeJetError(ValueError):
    def __init__(self, kind: str, reason: str):
        super().__init__(reason)
        self.kind = kind


@dataclass(frozen=True)
class ModeBundleJet:
    model: IrreducibleModel
    transport_generator: gaussian.ComplexMatrix
    projector_derivative: gaussian.ComplexMatrix
    frame_derivative: tuple[Vector, ...]
    frame_second_derivative: tuple[Vector, ...]
    connection_columns: tuple[Vector, ...]
    second_reduced_columns: tuple[Vector, ...]
    first_leakage_columns: tuple[Vector, ...]
    second_leakage_columns: tuple[Vector, ...]
    exact_decoupling: bool
    checks: dict[str, bool]


@dataclass(frozen=True)
class SectionJetWitness:
    direct_second_derivative: Vector
    reduced_second_derivative: Vector
    leakage: Vector
    synthesis: Vector
    checks: dict[str, bool]


def _subtract(left: Vector, right: Vector) -> Vector:
    return tuple(
        left_entry - right_entry for left_entry, right_entry in zip(left, right, strict=True)
    )


def _add(*values: Vector) -> Vector:
    return tuple(
        sum((value[index] for value in values), gaussian.ZERO) for index in range(len(values[0]))
    )


def _scale(value: Vector, factor: gaussian.Gaussian) -> Vector:
    return tuple(factor * entry for entry in value)


def _decompose(
    projector: gaussian.ComplexMatrix,
    embedding: tuple[Vector, ...],
    derivatives: tuple[Vector, ...],
) -> tuple[tuple[Vector, ...], tuple[Vector, ...]]:
    retained: list[Vector] = []
    leakage: list[Vector] = []
    for derivative in derivatives:
        projected = matrix_vector(projector, derivative)
        coefficients = coordinates(projected, embedding)
        if coefficients is None:
            raise ModeJetError(
                "ConnectionCoordinateResidual",
                "projected frame derivative is outside the retained carrier",
            )
        retained.append(coefficients)
        leakage.append(_subtract(derivative, linear_combination(coefficients, embedding)))
    return tuple(retained), tuple(leakage)


def construct_mode_jet(
    model: IrreducibleModel, transport_generator: gaussian.ComplexMatrix
) -> ModeBundleJet:
    dimension = len(model.selected_projector)
    if len(transport_generator) != dimension or any(
        len(row) != dimension for row in transport_generator
    ):
        raise ModeJetError("TransportDimensionMismatch", "transport dimension differs")
    if gaussian.dagger(transport_generator) != gaussian.scale(
        transport_generator, gaussian.Gaussian(-1)
    ):
        raise ModeJetError(
            "NonSkewTransportGenerator", "transport generator must be skew-Hermitian"
        )

    projector = model.selected_projector
    projector_derivative = gaussian.bracket(transport_generator, projector)
    transport_squared = gaussian.multiply(transport_generator, transport_generator)
    first = tuple(matrix_vector(transport_generator, vector) for vector in model.embedding_columns)
    second = tuple(matrix_vector(transport_squared, vector) for vector in model.embedding_columns)
    connection, first_leakage = _decompose(projector, model.embedding_columns, first)
    second_reduced, second_leakage = _decompose(projector, model.embedding_columns, second)
    zero_vector = tuple(gaussian.ZERO for _ in range(dimension))
    zero_matrix = gaussian.zero(dimension)
    checks = {
        "differentiated_projector_law": projector_derivative
        == gaussian.add(
            gaussian.multiply(projector_derivative, projector),
            gaussian.multiply(projector, projector_derivative),
        ),
        "projector_derivative_hermitian": gaussian.is_hermitian(projector_derivative),
        "first_frame_derivatives_reconstruct": all(
            derivative == _add(linear_combination(coefficients, model.embedding_columns), leak)
            for derivative, coefficients, leak in zip(first, connection, first_leakage, strict=True)
        ),
        "second_frame_derivatives_reconstruct": all(
            derivative == _add(linear_combination(coefficients, model.embedding_columns), leak)
            for derivative, coefficients, leak in zip(
                second, second_reduced, second_leakage, strict=True
            )
        ),
        "leakage_is_off_block": all(
            matrix_vector(projector, leak) == zero_vector
            for leak in (*first_leakage, *second_leakage)
        ),
        "constant_projector_has_zero_derivative": projector_derivative != zero_matrix
        or all(leak == zero_vector for leak in first_leakage),
    }
    if not all(checks.values()):
        failed = next(name for name, passed in checks.items() if not passed)
        raise ModeJetError("ModeJetResidual", f"construction fails at {failed}")
    exact = all(leak == zero_vector for leak in (*first_leakage, *second_leakage))
    return ModeBundleJet(
        model,
        transport_generator,
        projector_derivative,
        first,
        second,
        connection,
        second_reduced,
        first_leakage,
        second_leakage,
        exact,
        checks,
    )


def change_constant_frame(
    model: IrreducibleModel, gauge: gaussian.ComplexMatrix
) -> IrreducibleModel:
    dimension = model.carrier_dimension
    if len(gauge) != dimension or any(len(row) != dimension for row in gauge):
        raise ModeJetError("GaugeDimensionMismatch", "reduced gauge dimension differs")
    gauge_columns = tuple(
        tuple(gauge[row][column] for row in range(dimension)) for column in range(dimension)
    )
    embedding = tuple(
        linear_combination(column, model.embedding_columns) for column in gauge_columns
    )
    if rank(embedding) != dimension:
        raise ModeJetError("SingularGaugeFrame", "reduced gauge must be invertible")
    reduced_generators: list[StarGenerator] = []
    for generator in model.source.generators:
        columns = tuple(
            coordinates(matrix_vector(generator.value, vector), embedding) for vector in embedding
        )
        if any(column is None for column in columns):
            raise ModeJetError("GaugeIntertwinerResidual", "changed frame is not invariant")
        admitted = tuple(column for column in columns if column is not None)
        reduced = tuple(
            tuple(admitted[column][row] for column in range(dimension)) for row in range(dimension)
        )
        reduced_generators.append(StarGenerator(generator.label, reduced))
    return replace(
        model,
        embedding_columns=embedding,
        reduced_generators=tuple(reduced_generators),
    )


def evaluate_section_second_derivative(
    jet: ModeBundleJet,
    amplitude: Vector,
    first_derivative: Vector,
    second_derivative: Vector,
) -> SectionJetWitness:
    reduced_dimension = jet.model.carrier_dimension
    if any(
        len(value) != reduced_dimension
        for value in (amplitude, first_derivative, second_derivative)
    ):
        raise ModeJetError("SectionJetDimensionMismatch", "section-jet dimensions differ")
    direct = _add(
        linear_combination(second_derivative, jet.model.embedding_columns),
        _scale(linear_combination(first_derivative, jet.frame_derivative), gaussian.Gaussian(2)),
        linear_combination(amplitude, jet.frame_second_derivative),
    )
    reduced_coordinates = _add(
        second_derivative,
        _scale(linear_combination(first_derivative, jet.connection_columns), gaussian.Gaussian(2)),
        linear_combination(amplitude, jet.second_reduced_columns),
    )
    reduced = linear_combination(reduced_coordinates, jet.model.embedding_columns)
    leakage = _add(
        _scale(
            linear_combination(first_derivative, jet.first_leakage_columns), gaussian.Gaussian(2)
        ),
        linear_combination(amplitude, jet.second_leakage_columns),
    )
    synthesis = _add(reduced, leakage)
    checks = {"second_product_rule_reconstructs": direct == synthesis}
    if not all(checks.values()):
        raise ModeJetError(
            "SectionJetReconstructionResidual",
            "reduced and leakage terms do not reconstruct the second derivative",
        )
    return SectionJetWitness(direct, reduced, leakage, synthesis, checks)

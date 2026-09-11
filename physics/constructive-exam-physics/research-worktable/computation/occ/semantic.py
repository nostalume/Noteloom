from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional

from sympy import Poly, QQ, Rational, Symbol, simplify, sympify
from sympy.core.expr import Expr

from .pullback import pullback_linear, pullback_quadratic
from .records import Certificate, Matrix, Vector
from .relation import eliminate_polynomial_relations


@dataclass(frozen=True)
class Dimension:
    """Exponent vector for the SI bases mass, length, time, and current."""

    mass: int
    length: int
    time: int
    current: int

    def __add__(self, other: object) -> Dimension:
        if not isinstance(other, Dimension):
            return NotImplemented
        return Dimension(
            self.mass + other.mass,
            self.length + other.length,
            self.time + other.time,
            self.current + other.current,
        )

    def __sub__(self, other: object) -> Dimension:
        if not isinstance(other, Dimension):
            return NotImplemented
        return Dimension(
            self.mass - other.mass,
            self.length - other.length,
            self.time - other.time,
            self.current - other.current,
        )

    def __mul__(self, factor: object) -> Dimension:
        if not isinstance(factor, int) or isinstance(factor, bool):
            return NotImplemented
        return Dimension(
            factor * self.mass,
            factor * self.length,
            factor * self.time,
            factor * self.current,
        )

    __rmul__ = __mul__


@dataclass(frozen=True)
class QuantitySemantics:
    symbol: Symbol
    physical_name: str
    dimension: Dimension
    required_features: frozenset[str] = frozenset()


@dataclass(frozen=True)
class PhysicalRelationPacket:
    area: str
    source: QuantitySemantics
    fields: tuple[QuantitySemantics, ...]
    target: QuantitySemantics
    relations: tuple[Expr, ...]
    map_coefficient_dimension: Dimension
    functional_weight_dimension: Dimension
    regime: tuple[str, ...]
    conventions: tuple[str, ...]


@dataclass(frozen=True)
class ExtractedFunctionalSkeleton:
    functional_kind: str
    field_map: Matrix
    preserved_features: frozenset[str]
    linear_functional: Vector = ()
    quadratic_form: Matrix = ()


@dataclass(frozen=True)
class ReturnLedger:
    area: str
    source_name: str
    field_names: tuple[str, ...]
    target_name: str
    source_dimension: Dimension
    field_dimension: Dimension
    target_dimension: Dimension
    regime: tuple[str, ...]
    conventions: tuple[str, ...]
    preserved_features: frozenset[str]


@dataclass(frozen=True)
class SemanticObstruction:
    code: str
    message: str


@dataclass(frozen=True)
class SemanticCompilationResult:
    status: str
    skeleton: Optional[ExtractedFunctionalSkeleton] = None
    ledger: Optional[ReturnLedger] = None
    target_relation: Optional[Expr] = None
    certificates: tuple[Certificate, ...] = ()
    obstruction: Optional[SemanticObstruction] = None


def _refused(
    code: str,
    message: str,
    *,
    skeleton: Optional[ExtractedFunctionalSkeleton] = None,
    ledger: Optional[ReturnLedger] = None,
) -> SemanticCompilationResult:
    return SemanticCompilationResult(
        status="refused",
        skeleton=skeleton,
        ledger=ledger,
        obstruction=SemanticObstruction(code=code, message=message),
    )


def _fraction(value: object) -> Fraction:
    rational = Rational(value)
    if rational.is_Rational is not True:
        raise ValueError("Extracted coefficients must be exact rational numbers.")
    return Fraction(int(rational.p), int(rational.q))


def _unique_field_expression(
    relations: tuple[Expr, ...],
    field: Symbol,
    source: Symbol,
    target: Symbol,
) -> Optional[Expr]:
    solutions: list[Expr] = []
    for relation in relations:
        if field not in relation.free_symbols or target in relation.free_symbols:
            continue
        polynomial = Poly(relation, field)
        if polynomial.degree() != 1:
            continue
        coefficient = polynomial.coeff_monomial(field)
        remainder = relation - coefficient * field
        expression = simplify(-remainder / coefficient)
        if not expression.free_symbols <= {source}:
            continue
        source_polynomial = Poly(expression, source, domain=QQ)
        if source_polynomial.degree() > 1 or source_polynomial.coeff_monomial(1):
            continue
        if not any(simplify(expression - known) == 0 for known in solutions):
            solutions.append(expression)
    if len(solutions) != 1:
        return None
    return solutions[0]


def _unique_target_expression(
    relations: tuple[Expr, ...],
    target: Symbol,
    fields: tuple[Symbol, ...],
) -> Optional[Expr]:
    solutions: list[Expr] = []
    field_set = set(fields)
    for relation in relations:
        if target not in relation.free_symbols:
            continue
        polynomial = Poly(relation, target)
        if polynomial.degree() != 1:
            continue
        coefficient = polynomial.coeff_monomial(target)
        remainder = relation - coefficient * target
        expression = simplify(-remainder / coefficient)
        if not expression.free_symbols <= field_set:
            continue
        if not any(simplify(expression - known) == 0 for known in solutions):
            solutions.append(expression)
    if len(solutions) != 1:
        return None
    return solutions[0]


def _extract_functional(
    expression: Expr,
    fields: tuple[Symbol, ...],
) -> tuple[str, Vector, Matrix, frozenset[str]]:
    polynomial = Poly(expression, *fields, domain=QQ)
    term_degrees = {sum(monomial) for monomial, _ in polynomial.terms()}
    if term_degrees == {1}:
        weights = tuple(_fraction(polynomial.coeff_monomial(field)) for field in fields)
        return "linear", weights, (), frozenset({"signed", "magnitude"})
    if term_degrees != {2}:
        raise ValueError(
            "The target must be a homogeneous linear or quadratic functional."
        )

    size = len(fields)
    rows = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for row in range(size):
        rows[row][row] = _fraction(polynomial.coeff_monomial(fields[row] ** 2))
        for column in range(row + 1, size):
            coefficient = _fraction(
                polynomial.coeff_monomial(fields[row] * fields[column])
            )
            rows[row][column] = coefficient / 2
            rows[column][row] = coefficient / 2
    return (
        "quadratic",
        (),
        tuple(tuple(row) for row in rows),
        frozenset({"magnitude"}),
    )


def _ledger(
    packet: PhysicalRelationPacket,
    field_dimension: Dimension,
    preserved_features: frozenset[str],
) -> ReturnLedger:
    return ReturnLedger(
        area=packet.area,
        source_name=packet.source.physical_name,
        field_names=tuple(field.physical_name for field in packet.fields),
        target_name=packet.target.physical_name,
        source_dimension=packet.source.dimension,
        field_dimension=field_dimension,
        target_dimension=packet.target.dimension,
        regime=packet.regime,
        conventions=packet.conventions,
        preserved_features=preserved_features,
    )


def compile_single_source_functional(
    packet: PhysicalRelationPacket,
    *,
    max_fields: int = 8,
) -> SemanticCompilationResult:
    """Extract, compute, and return a bounded single-source field functional."""
    if (
        not isinstance(max_fields, int)
        or isinstance(max_fields, bool)
        or max_fields < 1
    ):
        raise ValueError("max_fields must be a positive integer.")
    if not packet.fields:
        return _refused(
            "missing_field", "At least one hidden field quantity is required."
        )
    if len(packet.fields) > max_fields:
        return _refused(
            "field_budget_exceeded",
            "The physical packet exceeds the declared hidden-field budget.",
        )

    quantities = (packet.source,) + packet.fields + (packet.target,)
    if any(not isinstance(quantity.symbol, Symbol) for quantity in quantities):
        raise TypeError("Every physical quantity must use a SymPy Symbol.")
    symbols = tuple(quantity.symbol for quantity in quantities)
    if len(set(symbols)) != len(symbols):
        raise ValueError("Physical source, fields, and target must be distinct.")
    relations = tuple(sympify(relation) for relation in packet.relations)

    source_symbol = packet.source.symbol
    target_symbol = packet.target.symbol
    field_symbols = tuple(field.symbol for field in packet.fields)
    field_expressions = tuple(
        _unique_field_expression(
            relations,
            field,
            source_symbol,
            target_symbol,
        )
        for field in field_symbols
    )
    if any(expression is None for expression in field_expressions):
        return _refused(
            "unsupported_relation_shape",
            "Each hidden field must have one homogeneous linear definition from the source.",
        )

    coefficients = tuple(
        _fraction(
            Poly(expression, source_symbol, domain=QQ).coeff_monomial(source_symbol)
        )
        for expression in field_expressions
        if expression is not None
    )
    field_map = tuple((coefficient,) for coefficient in coefficients)
    target_expression = _unique_target_expression(
        relations,
        target_symbol,
        field_symbols,
    )
    if target_expression is None:
        return _refused(
            "unsupported_relation_shape",
            "The target must have one explicit functional relation on the hidden fields.",
        )
    try:
        kind, linear, quadratic, preserved = _extract_functional(
            target_expression,
            field_symbols,
        )
    except ValueError as error:
        return _refused("unsupported_relation_shape", str(error))

    skeleton = ExtractedFunctionalSkeleton(
        functional_kind=kind,
        field_map=field_map,
        preserved_features=preserved,
        linear_functional=linear,
        quadratic_form=quadratic,
    )
    field_dimension = packet.fields[0].dimension
    ledger = _ledger(packet, field_dimension, preserved)

    if any(field.dimension != field_dimension for field in packet.fields):
        return _refused(
            "dimension_mismatch",
            "All components of the extracted field must have one physical dimension.",
            skeleton=skeleton,
            ledger=ledger,
        )
    expected_field = packet.source.dimension + packet.map_coefficient_dimension
    if field_dimension != expected_field:
        return _refused(
            "dimension_mismatch",
            "The source-to-field map does not recover the declared field dimension.",
            skeleton=skeleton,
            ledger=ledger,
        )
    degree = 1 if kind == "linear" else 2
    expected_target = packet.functional_weight_dimension + degree * field_dimension
    if packet.target.dimension != expected_target:
        return _refused(
            "dimension_mismatch",
            "The extracted functional does not recover the target dimension.",
            skeleton=skeleton,
            ledger=ledger,
        )

    missing_features = packet.target.required_features - preserved
    if missing_features:
        missing = ", ".join(sorted(missing_features))
        return _refused(
            "semantic_feature_lost",
            f"The extracted {kind} skeleton cannot return: {missing}.",
            skeleton=skeleton,
            ledger=ledger,
        )

    if kind == "linear":
        pullback = pullback_linear((field_map,), linear)
        coefficient = pullback.source_covector[0]
    else:
        pullback = pullback_quadratic((field_map,), quadratic)
        coefficient = pullback.source_form[0][0]
    exact_coefficient = Rational(coefficient.numerator, coefficient.denominator)
    target_relation = target_symbol - exact_coefficient * source_symbol**degree

    eliminated = eliminate_polynomial_relations(
        relations,
        eliminate=field_symbols,
        retain=(source_symbol, target_symbol),
        target=target_symbol,
    )
    ideal_passed = eliminated.implies(target_relation)
    lift = {
        field: expression
        for field, expression in zip(field_symbols, field_expressions)
        if expression is not None
    }
    lift[target_symbol] = exact_coefficient * source_symbol**degree
    lift_passed = all(simplify(relation.subs(lift)) == 0 for relation in relations)
    certificates = (
        Certificate(
            name="dimension_return",
            passed=True,
            witness="Map and functional dimensions compose to the physical target.",
        ),
        Certificate(
            name="semantic_features_return",
            passed=True,
            witness="The target requires no feature discarded by the extracted skeleton.",
        ),
        Certificate(
            name="target_relation_is_consequence",
            passed=ideal_passed,
            witness="The returned target relation belongs to the original law ideal.",
        ),
        Certificate(
            name="physical_lift",
            passed=lift_passed,
            witness="Source, reconstructed fields, and target satisfy every original relation.",
        ),
    )
    if not ideal_passed or not lift_passed:
        return _refused(
            "return_certificate_failed",
            "The extracted result could not be lifted through the original relations.",
            skeleton=skeleton,
            ledger=ledger,
        )
    return SemanticCompilationResult(
        status="compiled",
        skeleton=skeleton,
        ledger=ledger,
        target_relation=target_relation,
        certificates=certificates,
    )

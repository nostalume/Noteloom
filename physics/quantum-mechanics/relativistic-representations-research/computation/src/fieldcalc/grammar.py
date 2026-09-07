"""Generate bounded operation grammars from carrier laws and resources."""

from dataclasses import dataclass

from sympy import ImmutableMatrix, Rational, eye, sympify

from .rewrite import Polynomial, Refusal, Rejected, RewriteSystem, Rule


@dataclass(frozen=True)
class CarrierLaw:
    kind: str
    power: int

    def __post_init__(self):
        if self.kind not in {"symmetric", "exterior"}:
            raise ValueError(f"unsupported free-power law: {self.kind}")
        if self.power < 0:
            raise ValueError("power must be nonnegative")


@dataclass(frozen=True)
class ScalarMetricJet:
    order: int
    volume: tuple[object, ...]
    inverse_metric: tuple[ImmutableMatrix, ...]
    densitized_inverse: tuple[ImmutableMatrix, ...]
    provenance: str


@dataclass(frozen=True)
class ScalarMetricVertex:
    order: int
    volume: object
    inverse_metric: ImmutableMatrix
    densitized_inverse: ImmutableMatrix
    value: object
    provenance: str


@dataclass(frozen=True)
class TraceReversal:
    dimension: object
    coefficient: object
    inverse_coefficient: object
    involution_residual: object
    provenance: str


def compile_trace_reversal(dimension) -> TraceReversal:
    """Generate trace reversal and its inverse from T U = dimension I."""
    dimension = sympify(dimension)
    if dimension == 2:
        raise ValueError("trace reversal is singular in dimension two")
    return TraceReversal(
        dimension=dimension,
        coefficient=-Rational(1, 2),
        inverse_coefficient=-1 / (dimension - 2),
        involution_residual=(dimension - 4) / 4,
        provenance="inverse and square residual modulo T U = dimension I",
    )


def compile_scalar_metric_jet(deformation, order: int = 2) -> ScalarMetricJet:
    """Generate the minimal scalar action coefficients for g=eta(I+kappa H)."""
    if order not in {0, 1, 2}:
        raise ValueError("scalar metric jet supports orders 0 through 2")

    deformation = ImmutableMatrix(deformation)
    if deformation.rows != deformation.cols:
        raise ValueError("metric deformation must be a square endomorphism")

    identity = ImmutableMatrix(eye(deformation.rows))
    volume = [1]
    inverse_metric = [identity]
    densitized_inverse = [identity]
    if order >= 1:
        volume.append(deformation.trace() / 2)
        inverse_metric.append(-deformation)
        densitized_inverse.append(volume[1] * identity + inverse_metric[1])
    if order >= 2:
        deformation_squared = deformation * deformation
        volume.append(deformation.trace() ** 2 / 8 - deformation_squared.trace() / 4)
        inverse_metric.append(deformation_squared)
        densitized_inverse.append(
            inverse_metric[2]
            + volume[1] * inverse_metric[1]
            + volume[2] * identity
        )
    return ScalarMetricJet(
        order=order,
        volume=tuple(volume),
        inverse_metric=tuple(ImmutableMatrix(item) for item in inverse_metric),
        densitized_inverse=tuple(
            ImmutableMatrix(item) for item in densitized_inverse
        ),
        provenance="formal determinant, square-root, and inverse residuals",
    )


def compile_scalar_metric_vertex(
    metric,
    incoming,
    outgoing,
    mass_squared,
    deformations,
) -> ScalarMetricVertex:
    """Polarize the metric jet and evaluate its scalar momentum vertex."""
    if len(deformations) not in {1, 2}:
        raise ValueError("vertex requires one or two metric deformations")

    metric = ImmutableMatrix(metric)
    incoming = ImmutableMatrix(incoming)
    outgoing = ImmutableMatrix(outgoing)
    deformations = tuple(ImmutableMatrix(item) for item in deformations)
    dimension = metric.rows
    if metric.rows != metric.cols:
        raise ValueError("metric must be square")
    if incoming.shape != (dimension, 1) or outgoing.shape != (dimension, 1):
        raise ValueError("momenta must be column vectors in the metric space")
    if any(item.shape != metric.shape for item in deformations):
        raise ValueError("metric deformations must act on the momentum space")
    if any(item.T * metric != metric * item for item in deformations):
        raise ValueError("metric deformations must be metric-self-adjoint")

    identity = ImmutableMatrix(eye(dimension))
    if len(deformations) == 1:
        jet = compile_scalar_metric_jet(deformations[0], order=1)
        volume = jet.volume[1]
        inverse_metric = jet.inverse_metric[1]
        densitized_inverse = jet.densitized_inverse[1]
    else:
        left, right = deformations
        inverse_metric = Rational(1, 2) * (left * right + right * left)
        volume = left.trace() * right.trace() / 8 - (left * right).trace() / 4
        densitized_inverse = (
            inverse_metric
            - (left.trace() * right + right.trace() * left) / 4
            + volume * identity
        )

    value = (
        -(incoming.T * metric * densitized_inverse * outgoing)[0]
        + mass_squared * volume
    )
    return ScalarMetricVertex(
        order=len(deformations),
        volume=volume,
        inverse_metric=ImmutableMatrix(inverse_metric),
        densitized_inverse=ImmutableMatrix(densitized_inverse),
        value=value,
        provenance="polarized minimal scalar metric action jet",
    )


def compile_grammar(
    law: CarrierLaw, resources: set[str], budget: int = 3
) -> RewriteSystem | Rejected:
    if law.kind == "symmetric" and "metric" not in resources:
        return Rejected(Refusal("missing metric resource", provenance="symmetric free power"))

    if law.kind == "symmetric":
        rules = (
            Rule(("A", "P"), Polynomial({("P", "A"): 1, ("Q",): 1}), "symmetric derivation law"),
            Rule(("T", "P"), Polynomial({("P", "T"): 1, ("A",): 2}), "metric trace law"),
        )
    else:
        rules = (
            Rule(("A", "P"), Polynomial({("P", "A"): -1, ("Q",): 1}), "exterior derivation law"),
            Rule(("P", "P"), Polynomial(), "exterior nilpotence"),
            Rule(("A", "A"), Polynomial(), "exterior nilpotence"),
        )
    return RewriteSystem(rules, budget=budget, provenance=f"{law.kind} power {law.power}")


def factor_first_order(wave_token: str, budget: int = 3) -> RewriteSystem:
    return RewriteSystem(
        (
            Rule(
                ("G", "G"),
                Polynomial.word(wave_token),
                "polarized first-order factorization",
            ),
        ),
        budget=budget,
        provenance="first-order factorization",
    )

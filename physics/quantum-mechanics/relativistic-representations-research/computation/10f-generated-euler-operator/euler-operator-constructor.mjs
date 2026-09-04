import {
  addPolynomial,
  constructBosonicFieldSystem,
  multiplyRat,
  negateRat,
  polynomial,
  polynomialEqual,
  polynomialText,
  rat,
  scalePolynomial,
  solveMap,
} from '../10c-generative-residual-constructor/residual-constructor.mjs';
import {
  constructBosonicSourceAdapter,
} from '../10e-generated-source-adapter/source-adapter-constructor.mjs';

function coreAdjointDefect(coefficient = rat(1)) {
  return polynomial([
    [['P', 'P', 'T'], coefficient],
    [['U', 'A', 'A'], negateRat(coefficient)],
  ]);
}

function constructBosonicEulerOperator({
  fieldSystemResult,
  maxMetricInsertions = 1,
} = {}) {
  const generated = fieldSystemResult ?? constructBosonicFieldSystem({ maxTraceDepth: 1 });
  if (!generated.ok) return {
    ok: false,
    phase: 'upstream-field-system',
    reason: 'the field-system generator did not return a supported bosonic equation',
    upstream: generated,
  };
  if (!Number.isInteger(maxMetricInsertions) || maxMetricInsertions < 0
      || maxMetricInsertions > 1) return {
    ok: false,
    phase: 'euler-budget',
    reason: 'the bounded double-trace Euler search admits zero or one U T correction',
    maxMetricInsertions,
  };

  const D = generated.fieldSystem.D;
  const paCoefficient = D.get('P A') ?? rat(0);
  const traceCoefficient = D.get('P P T') ?? rat(0);
  const seedResidual = coreAdjointDefect(traceCoefficient);
  const correctionImageCoefficient = negateRat(multiplyRat(rat(2), paCoefficient));
  const correctionWords = maxMetricInsertions === 0 ? [] : [['U', 'T']];
  const solved = solveMap(
    correctionWords,
    () => coreAdjointDefect(correctionImageCoefficient),
    scalePolynomial(rat(-1), seedResidual),
  );
  if (!solved.ok) return {
    ok: false,
    phase: 'euler-self-adjoint-residual',
    capability: 'construct an equation-equivalent formally self-adjoint Euler operator',
    seed: 'D',
    seedResidual: polynomialText(seedResidual),
    maxMetricInsertions,
    ...solved,
  };

  const multiplier = addPolynomial(
    polynomial([[[], rat(1)]]),
    solved.generated,
  );
  const multiplierCoefficient = multiplier.get('U T') ?? rat(0);
  const quotientResidual = addPolynomial(
    seedResidual,
    coreAdjointDefect(multiplyRat(correctionImageCoefficient, multiplierCoefficient)),
  );
  const constraintCoefficient = multiplyRat(multiplierCoefficient, traceCoefficient);
  const constraintResidual = polynomial([
    [['U', 'P', 'P', 'T', 'T'], constraintCoefficient],
    [['U', 'U', 'A', 'A', 'T'], negateRat(constraintCoefficient)],
  ]);

  const sourceAdapter = constructBosonicSourceAdapter({ fieldSystemResult: generated });
  if (!sourceAdapter.ok) {
    throw new Error(`source-adapter comparison failed: ${JSON.stringify(sourceAdapter)}`);
  }
  const certificates = {
    quotientSelfAdjointness: quotientResidual.size === 0,
    identityNormalization: multiplier.get('I')?.n === 1n
      && multiplier.get('I')?.d === 1n,
    independentSourceCoincidence: polynomialEqual(multiplier, sourceAdapter.adapter),
    residualFactorsThroughDoubleTrace: [...constraintResidual.keys()].every((key) =>
      key.startsWith('U U ') || key.endsWith('T T')),
  };
  if (Object.values(certificates).some((value) => !value)) {
    throw new Error(`Euler-constructor certificate failed: ${JSON.stringify(certificates)}`);
  }

  return {
    ok: true,
    capability: 'quadratic Euler equation with the generated physical-source interface',
    budget: { maxMetricInsertions, dimension: 4, fieldTraceDepth: 2 },
    assumptions: [
      'Fischer pairing induced by the Lorentz metric',
      'compact support or a boundary convention removing surface terms',
      'double-traceless symmetric field carrier',
    ],
    upstreamFieldSystem: generated.fieldSystem,
    search: {
      seed: 'D',
      seedResidual: polynomialText(seedResidual),
      correctionBasis: solved.basis,
      correctionCoefficients: solved.coefficients,
      insufficientBudget: constructBosonicEulerOperator({
        fieldSystemResult: generated,
        maxMetricInsertions: 0,
      }),
    },
    multiplier,
    eulerOperator: { leftMultiplier: multiplier, equation: D },
    constraintResidual,
    certificates,
    actionInterface: {
      fieldEquation: 'E phi = J with E = M D',
      functional: 'I[phi;J] = (1/2)<phi,E phi> - <phi,J>',
      variation: 'delta I = <delta phi,E phi-J>',
      gaugeWitness: 'E R = M D R = 0',
      sourceWitness: 'E G_Q M^(-1)J = J when R^dagger J = 0',
    },
  };
}

function serializableEulerOperator(result) {
  if (!result.ok) return result;
  return {
    ...result,
    upstreamFieldSystem: Object.fromEntries(Object.entries(result.upstreamFieldSystem)
      .map(([name, value]) => [name, polynomialText(value)])),
    multiplier: polynomialText(result.multiplier),
    eulerOperator: {
      leftMultiplier: polynomialText(result.eulerOperator.leftMultiplier),
      equation: polynomialText(result.eulerOperator.equation),
    },
    constraintResidual: polynomialText(result.constraintResidual),
  };
}

export {
  constructBosonicEulerOperator,
  coreAdjointDefect,
  serializableEulerOperator,
};

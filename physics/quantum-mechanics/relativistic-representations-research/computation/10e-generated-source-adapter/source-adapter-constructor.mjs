import {
  addPolynomial,
  addRat,
  constructBosonicFieldSystem,
  divideRat,
  isZero,
  multiplyRat,
  negateRat,
  polynomial,
  polynomialEqual,
  polynomialText,
  rat,
  scalePolynomial,
  solveMap,
} from '../10c-generative-residual-constructor/residual-constructor.mjs';

function canonicalAdapterWords(maxMetricInsertions) {
  const words = [[]];
  for (let depth = 1; depth <= maxMetricInsertions; depth += 1) {
    words.push([
      ...Array.from({ length: depth }, () => 'U'),
      ...Array.from({ length: depth }, () => 'T'),
    ]);
  }
  return words;
}

// The capability is equality only after pairing against a traceless parameter.
// A leading U is therefore a pure-trace target and vanishes in this quotient.
function pairedAdjointImage(candidate) {
  const images = [];
  for (const [key, coefficient] of candidate) {
    if (key === 'I') {
      images.push(scalePolynomial(coefficient, polynomial([[['A'], rat(1)]])));
    } else if (key === 'U T') {
      // A U T = U A T + 2 P T; quotienting the first term leaves 2 P T.
      images.push(scalePolynomial(
        multiplyRat(rat(2), coefficient),
        polynomial([[['P', 'T'], rat(1)]]),
      ));
    } else {
      throw new Error(`unsupported source-adapter normal word ${key}`);
    }
  }
  return addPolynomial(...images);
}

function constructBosonicSourceAdapter({
  fieldSystemResult,
  maxMetricInsertions = 1,
} = {}) {
  const generated = fieldSystemResult ?? constructBosonicFieldSystem({ maxTraceDepth: 1 });
  if (!generated.ok) return {
    ok: false,
    phase: 'upstream-field-system',
    reason: 'the bosonic field-system generator did not return a supported object',
    upstream: generated,
  };
  if (maxMetricInsertions > 1) return {
    ok: false,
    phase: 'source-adapter-budget',
    reason: 'the present double-traceless carrier admits only the two Fischer layers I and U T',
    maxMetricInsertions,
  };

  const words = canonicalAdapterWords(maxMetricInsertions);
  const target = generated.fieldSystem.C;
  const solved = solveMap(words, pairedAdjointImage, target);
  if (!solved.ok) return {
    ok: false,
    phase: 'source-adjoint-residual',
    capability: 'convert paired source conservation into the generated Green-source constraint',
    maxMetricInsertions,
    failedCandidate: maxMetricInsertions === 0 ? 'I' : words.map((word) => word.join(' ') || 'I'),
    ...solved,
  };

  const M = solved.generated;
  const traceCoefficient = M.get('U T') ?? rat(0);
  const discardedPairedResidual = polynomial([[['U', 'A', 'T'], traceCoefficient]]);
  const certificates = {
    pairedAdjointIdentity: polynomialEqual(pairedAdjointImage(M), target),
    identityNormalization: M.get('I')?.n === 1n && M.get('I')?.d === 1n,
    selfAdjointNormalWords: [...M.keys()].every((key) => key === 'I' || key === 'U T'),
  };
  if (Object.values(certificates).some((value) => !value)) {
    throw new Error(`source-adapter certificate failed: ${JSON.stringify(certificates)}`);
  }

  return {
    ok: true,
    capability: 'pairing-compatible compact source to generated scalar-Green input',
    budget: { maxMetricInsertions, dimension: 4, fieldTraceDepth: 2 },
    assumptions: [
      'Fischer pairing induced by the Lorentz metric',
      'traceless gauge parameter',
      'double-traceless symmetric field carrier',
    ],
    search: {
      basis: solved.basis,
      coefficients: solved.coefficients,
      insufficientBudget: constructBosonicSourceAdapter({
        fieldSystemResult: generated,
        maxMetricInsertions: 0,
      }),
    },
    upstreamFieldSystem: generated.fieldSystem,
    adapter: M,
    pairedResidual: discardedPairedResidual,
    certificates,
    sourceInterface: {
      input: 'compact J satisfying R^dagger J = 0',
      operation: 'S = M^(-1) J',
      output: 'C S = 0 and D G_Q S = S',
      witness: 'C M^(-1) J = R^dagger J = 0',
    },
  };
}

function inverseSourceAdapter(adapterResult, spin) {
  if (!adapterResult.ok) throw new Error('cannot invert a refused source adapter');
  if (!Number.isInteger(spin) || spin < 1) throw new Error(`invalid integer spin ${spin}`);
  if (spin === 1) return polynomial([[[], rat(1)]]);
  const coefficient = adapterResult.adapter.get('U T') ?? rat(0);
  const eigenvalue = rat(4 * spin);
  const denominator = addRat(rat(1), multiplyRat(eigenvalue, coefficient));
  if (isZero(denominator)) {
    throw new Error(`generated adapter is singular on the trace layer at spin ${spin}`);
  }
  const inverseCoefficient = divideRat(negateRat(coefficient), denominator);
  return polynomial([
    [[], rat(1)],
    [['U', 'T'], inverseCoefficient],
  ]);
}

function serializableSourceAdapter(result, spins = [2, 3, 4, 5, 6]) {
  if (!result.ok) return result;
  return {
    ...result,
    upstreamFieldSystem: Object.fromEntries(Object.entries(result.upstreamFieldSystem)
      .map(([name, value]) => [name, polynomialText(value)])),
    adapter: polynomialText(result.adapter),
    pairedResidual: polynomialText(result.pairedResidual),
    inverses: Object.fromEntries(spins.map((spin) => [
      spin,
      polynomialText(inverseSourceAdapter(result, spin)),
    ])),
  };
}

export {
  canonicalAdapterWords,
  constructBosonicSourceAdapter,
  inverseSourceAdapter,
  pairedAdjointImage,
  serializableSourceAdapter,
};

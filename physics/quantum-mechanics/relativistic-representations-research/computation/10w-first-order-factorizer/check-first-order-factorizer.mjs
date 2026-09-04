import { pathToFileURL } from 'node:url';

import { generateFirstOrderFactorization } from './first-order-factorizer.mjs';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const metric = Object.freeze({
  id: 'eta',
  role: 'metric',
  rank: 2,
  exchangeSign: 1,
  invariant: true,
  nondegenerate: true,
  spacetimeDimension: 4,
});

const capability = Object.freeze({
  equivariant: true,
  momentumOrder: 1,
  linearInMomentum: true,
  completion: {
    kind: 'scalar-quadratic',
    invariant: 'eta',
    coefficient: 1,
  },
});

const chiralCarrier = Object.freeze({
  field: 'complex',
  vectorFactorization: 'S tensor Sbar',
  left: 'S',
  right: 'Sbar',
  leftDimension: 2,
  rightDimension: 2,
});

function request(overrides = {}) {
  return {
    metric,
    capability,
    chiralCarrier,
    moduleRequest: {
      source: 'S direct-sum Sbar',
      target: 'S direct-sum Sbar',
      requireEndomorphism: true,
      parity: 'paired',
      reality: 'complex',
    },
    resourceBudget: { maximumComplexDimension: 4 },
    ...overrides,
  };
}

function run() {
  const answerBearing = generateFirstOrderFactorization({
    ...request(),
    gammaMatrices: [[1, 0], [0, -1]],
  });
  assert(!answerBearing.ok && answerBearing.phase === 'answer-bearing-input',
    'a supplied gamma-matrix answer must be refused');

  const missingMetric = generateFirstOrderFactorization({
    ...request(),
    metric: undefined,
  });
  assert(!missingMetric.ok && missingMetric.phase === 'metric-resource',
    'the factorizer must refuse a missing metric');

  const wrongCompletion = generateFirstOrderFactorization({
    ...request(),
    capability: {
      ...capability,
      completion: { kind: 'arbitrary-endomorphism' },
    },
  });
  assert(!wrongCompletion.ok && wrongCompletion.phase === 'completion-capability',
    'a non-scalar completion must be refused');

  const sameChirality = generateFirstOrderFactorization({
    ...request(),
    moduleRequest: {
      source: 'S',
      target: 'S',
      requireEndomorphism: true,
      parity: 'chiral',
      reality: 'complex',
    },
    resourceBudget: { maximumComplexDimension: 2 },
  });
  assert(!sameChirality.ok && sameChirality.phase === 'chirality-obstruction',
    'a vector symbol cannot act as an endomorphism of one Weyl chirality');

  const unsupportedReality = generateFirstOrderFactorization({
    ...request(),
    moduleRequest: {
      ...request().moduleRequest,
      reality: 'majorana',
    },
  });
  assert(!unsupportedReality.ok && unsupportedReality.phase === 'reality-resource',
    'a requested real structure must not be invented');

  const generated = generateFirstOrderFactorization(request());
  assert(generated.ok, `paired factorization refused: ${JSON.stringify(generated)}`);
  assert(generated.coefficientModule.label === 'Delta',
    'the paired carrier must be retained as Delta');
  assert(generated.coefficientModule.decomposition === 'S direct-sum Sbar',
    'the factorizer must construct the parity-paired chiral carrier');
  assert(generated.action.origin.kind === 'generated-first-order-factorization',
    'the returned coefficient action needs generated provenance');
  assert(generated.action.law === 'metric-polarized-quadratic-action'
      && generated.action.polarizationCoefficient === 2,
  'polarization must be generated from the square completion');
  assert(generated.certificates.square.identity === 'd(p)d(p)=Q(p) I'
      && generated.certificates.polarization.identity
        === 'd(u)d(v)+d(v)d(u)=2 eta^(-1)(u,v) I',
  'the square and polarization witnesses were not retained');
  assert(generated.universalAlgebra.quotient
      === 'T(V*)/<u tensor v+v tensor u-2 eta^(-1)(u,v) 1>',
  'the universal repair must be an output, not a supplied Clifford algebra');

  console.log(JSON.stringify({
    refusals: { answerBearing, missingMetric, wrongCompletion, sameChirality, unsupportedReality },
    generated,
  }, null, 2));
  console.log('first-order factorizer checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

export { capability, chiralCarrier, metric, request };

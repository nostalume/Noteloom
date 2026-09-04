import { pathToFileURL } from 'node:url';

import {
  constructBosonicFieldSystem,
} from '../10c-generative-residual-constructor/residual-constructor.mjs';
import {
  constructCarrierGrammar,
} from '../10h-carrier-to-grammar/carrier-grammar-constructor.mjs';
import {
  selectPresentations,
} from '../10i-capability-presentation-selector/presentation-selector.mjs';
import {
  constructCurvatureCompatibility,
  transformHomogeneous,
  transformVector,
} from './curvature-compatibility-constructor.mjs';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function equalPolynomial(left, right) {
  return left.length === right.length
    && left.every((coefficient, index) => coefficient === right[index]);
}

function isZero(polynomial) {
  return polynomial.every((coefficient) => coefficient === 0);
}

const grammar = constructCarrierGrammar({
  presentation: { functor: 'symmetric-power', coefficientModule: 'scalar' },
  resources: {
    symmetricAlgebra: true,
    metric: { invariant: true, nondegenerate: true, symmetric: true },
  },
});
const potentialSystem = constructBosonicFieldSystem({
  grammarPacket: grammar,
  maxTraceDepth: 1,
});
const curvatureResources = Object.freeze({
  symmetricAlgebra: true,
  chiralBivectorSplit: true,
  alternatingForms: { left: true, right: true },
});

function build(spin, maxDerivativeOrder = spin) {
  return constructCurvatureCompatibility({
    spin,
    maxDerivativeOrder,
    potentialSystem,
    resources: curvatureResources,
  });
}

function repeat(value, count) {
  return Array.from({ length: count }, () => value);
}

function run() {
  assert(grammar.ok && potentialSystem.ok, 'upstream generated potential system failed');

  const missingResources = constructCurvatureCompatibility({
    spin: 2,
    potentialSystem,
    resources: { symmetricAlgebra: true },
  });
  assert(!missingResources.ok && missingResources.phase === 'chiral-resources',
    'missing Hodge/spinor resources must return a typed refusal');

  const invalidBudget = build(2, 1.5);
  assert(!invalidBudget.ok && invalidBudget.phase === 'derivative-budget',
    'a nonintegral derivative budget must return a typed refusal');

  const insufficientOrder = build(3, 2);
  assert(!insufficientOrder.ok && insufficientOrder.phase === 'polynomial-lift'
      && insufficientOrder.requiredDerivativeOrder === 3,
  'degree below spin must fail before a curvature formula is emitted');

  const lambda = [1, 0];
  const mu = [0, 1];
  const barLambda = [1, 0];
  const barMu = [0, 1];
  const momentum = { left: lambda, right: barLambda };
  const plusScreen = { left: lambda, right: barMu };
  const minusScreen = { left: mu, right: barLambda };
  const leftMatrix = [[1, 1], [0, 1]];
  const rightMatrix = [[1, 0], [1, 1]];
  const rows = [];

  for (let spin = 1; spin <= 6; spin += 1) {
    const packet = build(spin);
    assert(packet.ok, `spin-${spin} curvature packet was refused`);
    assert(packet.derivativeOrder === spin
        && packet.multiplicityTrace[spin].multiplicity === 1,
    `spin-${spin} minimal-degree certificate failed`);

    const purePlus = packet.evaluateNullDecomposable(momentum, repeat(plusScreen, spin));
    const pureMinus = packet.evaluateNullDecomposable(momentum, repeat(minusScreen, spin));
    const gauge = packet.evaluateNullDecomposable(
      momentum,
      [momentum, ...repeat(plusScreen, spin - 1)],
    );
    assert(!isZero(purePlus.plus) && isZero(purePlus.minus),
      `spin-${spin} plus screen line did not map to only the plus chiral line`);
    assert(isZero(pureMinus.plus) && !isZero(pureMinus.minus),
      `spin-${spin} minus screen line did not map to only the minus chiral line`);
    assert(isZero(gauge.plus) && isZero(gauge.minus),
      `spin-${spin} gauge image survived the generated curvature map`);

    const transformedMomentum = transformVector(leftMatrix, rightMatrix, momentum);
    const transformedSlots = repeat(plusScreen, spin)
      .map((slot) => transformVector(leftMatrix, rightMatrix, slot));
    const transformedInput = packet.evaluateNullDecomposable(
      transformedMomentum,
      transformedSlots,
    );
    assert(equalPolynomial(
      transformedInput.plus,
      transformHomogeneous(purePlus.plus, leftMatrix),
    ), `spin-${spin} plus covariance check failed`);
    assert(equalPolynomial(
      transformedInput.minus,
      transformHomogeneous(purePlus.minus, rightMatrix),
    ), `spin-${spin} minus covariance check failed`);

    rows.push({
      spin,
      derivativeOrder: packet.derivativeOrder,
      outputDimension: 4 * spin + 2,
      plusLineNonzero: !isZero(purePlus.plus),
      minusLineNonzero: !isZero(pureMinus.minus),
      gaugeKilled: isZero(gauge.plus) && isZero(gauge.minus),
      covariant: true,
    });
  }

  const spinTwoPacket = build(2);
  const bridgeWithoutPacket = selectPresentations({
    physicalFiber: { kind: 'massless-helicity-pair', magnitude: 2 },
    requiredCapabilities: ['physical-shell-potential-curvature-bridge'],
  });
  assert(!bridgeWithoutPacket.ok,
    'N10i must not infer the higher-spin bridge without consuming N10j output');

  const bridgeWithPacket = selectPresentations({
    physicalFiber: { kind: 'massless-helicity-pair', magnitude: 2 },
    requiredCapabilities: [
      'physical-realization',
      'gauge-invariant-curvature-output',
      'physical-shell-potential-curvature-bridge',
    ],
    curvatureCompatibilityPacket: spinTwoPacket,
  });
  assert(bridgeWithPacket.ok
      && bridgeWithPacket.frontier.some((route) => route.id === 'compressed-symmetric-potential'),
  'N10i did not consume the generated spin-two curvature capability');

  const unsupportedInverse = selectPresentations({
    physicalFiber: { kind: 'massless-helicity-pair', magnitude: 2 },
    requiredCapabilities: ['local-polynomial-curvature-inverse'],
    curvatureCompatibilityPacket: spinTwoPacket,
  });
  assert(!unsupportedInverse.ok && unsupportedInverse.phase === 'capability-selection',
    'the generated forward map must not be promoted to a polynomial local inverse');

  console.table(rows);
  console.log(JSON.stringify({
    upstreamProvenance: grammar.provenance,
    insufficientOrder,
    bridgeFrontier: bridgeWithPacket.frontier.map(({ id, cost }) => ({ id, cost })),
    unsupportedInverse,
  }, null, 2));
  console.log('generated curvature-compatibility checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

export { build, curvatureResources, potentialSystem, run };

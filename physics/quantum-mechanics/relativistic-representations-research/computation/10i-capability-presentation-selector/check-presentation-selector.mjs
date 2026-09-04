import { pathToFileURL } from 'node:url';

import { selectPresentations } from './presentation-selector.mjs';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function ids(routes) {
  return routes.map((route) => route.id).sort();
}

function run() {
  const spinTwo = selectPresentations({
    physicalFiber: { kind: 'massless-helicity-pair', magnitude: 2 },
    requiredCapabilities: ['physical-realization'],
  });
  assert(spinTwo.ok, 'spin-two realization selection failed');
  assert(JSON.stringify(ids(spinTwo.frontier)) === JSON.stringify([
    'compressed-symmetric-potential',
    'parity-paired-direct-curvature',
  ]), 'spin two must retain the order/component trade rather than invent a winner');
  assert(spinTwo.dominated.some((route) => route.id === 'completed-symmetric-potential-machine'),
    'the unrequested action/causal completion should be dominated for realization only');

  const spinThree = selectPresentations({
    physicalFiber: { kind: 'massless-helicity-pair', magnitude: 3 },
    requiredCapabilities: ['physical-realization'],
  });
  assert(spinThree.ok && ids(spinThree.frontier)[0] === 'parity-paired-direct-curvature',
    'within the declared axes, the direct spin-three route should dominate realization-only potential routes');

  const causalSpinTwo = selectPresentations({
    physicalFiber: { kind: 'massless-helicity-pair', magnitude: 2 },
    requiredCapabilities: ['quadratic-action', 'admissible-source', 'causal-response'],
  });
  assert(causalSpinTwo.ok
      && ids(causalSpinTwo.frontier)[0] === 'completed-symmetric-potential-machine',
  'the supported action/source/causal request must select the completed potential machine');

  const maxwellBridge = selectPresentations({
    physicalFiber: { kind: 'massless-helicity-pair', magnitude: 1 },
    requiredCapabilities: [
      'physical-realization',
      'gauge-invariant-curvature-output',
      'physical-shell-potential-curvature-bridge',
    ],
  });
  assert(maxwellBridge.ok && maxwellBridge.frontier.length >= 1,
    'the N5 Maxwell potential/curvature bridge should be selectable');

  const missingHigherSpinBridge = selectPresentations({
    physicalFiber: { kind: 'massless-helicity-pair', magnitude: 2 },
    requiredCapabilities: ['physical-shell-potential-curvature-bridge'],
  });
  assert(!missingHigherSpinBridge.ok
      && missingHigherSpinBridge.phase === 'capability-selection',
  'spin-two potential/curvature bridge must refuse because N5 leaves its map open');

  const firstOrderOnly = selectPresentations({
    physicalFiber: { kind: 'massless-helicity-pair', magnitude: 2 },
    resourceBudget: { maxDifferentialOrder: 1 },
  });
  assert(firstOrderOnly.ok
      && ids(firstOrderOnly.frontier)[0] === 'parity-paired-direct-curvature',
  'a first-order budget must exclude the potential routes');

  const incompatibleBudget = selectPresentations({
    physicalFiber: { kind: 'massless-helicity-pair', magnitude: 2 },
    resourceBudget: { maxDifferentialOrder: 1, rawComponentLoad: 24 },
  });
  assert(!incompatibleBudget.ok && incompatibleBudget.phase === 'capability-selection',
    'split order/component budgets should return a typed refusal');

  const scalarScore = selectPresentations({
    physicalFiber: { kind: 'massless-helicity-pair', magnitude: 2 },
    comparisonMode: 'weighted-score',
  });
  assert(!scalarScore.ok && scalarScore.phase === 'comparison-policy',
    'an undeclared scalarization must be refused');

  const halfInteger = selectPresentations({
    physicalFiber: { kind: 'massless-helicity-pair', magnitude: 1.5 },
  });
  assert(!halfInteger.ok && halfInteger.phase === 'physical-target',
    'the bounded integer-helicity bench must not silently generalize to half-integer spin');

  console.log(JSON.stringify({
    spinTwoFrontier: spinTwo.frontier.map(({ id, cost }) => ({ id, cost })),
    spinThreeFrontier: spinThree.frontier.map(({ id, cost }) => ({ id, cost })),
    causalSpinTwoFrontier: ids(causalSpinTwo.frontier),
    maxwellBridgeFrontier: ids(maxwellBridge.frontier),
    missingHigherSpinBridge,
    incompatibleBudget,
    scalarScore,
    halfInteger,
  }, null, 2));
  console.log('capability-relative presentation selector checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

export { run };

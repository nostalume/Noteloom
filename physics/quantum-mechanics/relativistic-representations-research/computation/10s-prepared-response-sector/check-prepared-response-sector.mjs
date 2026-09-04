import { pathToFileURL } from 'node:url';

import {
  compilePreparedSpinTwoResponse,
  constructWeylDoubleDivergencePreparation,
  existingCompactCurrentPreparation,
} from './prepared-response-sector.mjs';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function run() {
  const forbidden = compilePreparedSpinTwoResponse({
    preparations: [existingCompactCurrentPreparation()],
    requestedCapability: 'local-preparation-to-nonzero-screen-response',
    expectedSupport: [2],
  });
  assert(!forbidden.ok && forbidden.phase === 'answer-bearing-input',
    'a supplied support answer must be refused');

  const invalidWeylSeed = constructWeylDoubleDivergencePreparation({
    electricSeed: [[1, 0, 0], [0, 0, 0], [0, 0, 0]],
  });
  assert(!invalidWeylSeed.ok && invalidWeylSeed.phase === 'weyl-seed-algebra',
    'a traceful Weyl seed must be refused');

  const weylPreparation = constructWeylDoubleDivergencePreparation({
    electricSeed: [[1, 0, 0], [0, -1, 0], [0, 0, 0]],
  });
  assert(weylPreparation.ok, `Weyl preparation refused: ${JSON.stringify(weylPreparation)}`);

  const result = compilePreparedSpinTwoResponse({
    preparations: [existingCompactCurrentPreparation(), weylPreparation],
    requestedCapability: 'local-preparation-to-nonzero-screen-response',
  });
  assert(result.ok, `prepared-response construction refused: ${JSON.stringify(result)}`);

  const regression = result.cases.find((entry) =>
    entry.preparation.name === 'N10e-compact-bivector-current');
  const transfer = result.cases.find((entry) =>
    entry.preparation.name === 'compact-Weyl-seed-double-divergence');
  assert(regression.nonnull.activeLayers.map((entry) => entry.label).join(',') === '0,2',
    `N10e regression should discover layers 0 and 2: ${JSON.stringify(regression)}`);
  assert(regression.nullShell.nonzeroPhysicalScreen,
    'N10e regression lost its nonzero screen witness');
  assert(transfer.nonnull.activeLayers.length === 1
      && transfer.nonnull.activeLayers[0].label === 2,
  `Weyl transfer should discover only layer 2: ${JSON.stringify(transfer)}`);
  assert(transfer.nullShell.divergenceError < 1e-8 && transfer.nullShell.traceError < 1e-8,
    'Weyl transfer is not conserved and trace free on shell');
  assert(transfer.nullShell.nonzeroPhysicalScreen,
    'Weyl transfer has no nonzero physical screen');
  assert(transfer.routeComparison.samePotentialAndCurvature,
    'direct and compensated routes do not recover the same transfer response');
  assert(transfer.routeComparison.completeCostVerdict
      === 'same-active-response-work; no computational dominance',
  'the transfer should not claim a carrier-size speedup');
  assert(result.verdict.preparationBridge === 'supported',
    'preparation bridge was not supported');
  assert(result.verdict.computationalGain === 'rejected-against-same-preparation-baseline',
    'whole-route computational verdict changed');

  console.log(JSON.stringify({ forbidden, invalidWeylSeed, result }, null, 2));
  console.log('prepared response-sector checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

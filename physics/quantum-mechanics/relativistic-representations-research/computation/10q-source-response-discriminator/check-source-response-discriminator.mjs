import { pathToFileURL } from 'node:url';

import {
  constructSourceResponseDiscriminator,
} from './source-response-discriminator.mjs';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function stringify(value, space) {
  return JSON.stringify(value, (_, item) => (
    typeof item === 'bigint' ? `${item}` : item
  ), space);
}

function run() {
  const answerBearing = constructSourceResponseDiscriminator({
    dimension: 4,
    spins: [2, 3],
    requestedCapability: 'local-causal-source-response',
    expectedVerdict: 'constrained wins',
  });
  assert(!answerBearing.ok && answerBearing.phase === 'answer-bearing-input',
    'a supplied verdict must be refused');

  const result = constructSourceResponseDiscriminator({
    dimension: 4,
    spins: [2, 3, 4, 5],
    requestedCapability: 'local-causal-source-response',
  });
  assert(result.ok, `source-response construction refused: ${stringify(result)}`);
  assert(result.family === 'projected-carrier-source-response-discriminator',
    `unexpected family ${result.family}`);

  for (const spin of [2, 3, 4, 5]) {
    const row = result.spins[spin];
    assert(row.divergence.surjective,
      `spin ${spin} divergence is not surjective`);
    assert(row.divergence.rightInverse,
      `spin ${spin} right inverse was not constructed`);
    assert(row.sources.constrainedDimension === spin ** 2 + 2,
      `spin ${spin} constrained source dimension is wrong`);
    assert(row.sources.compensatedDimension === spin ** 2 + 2,
      `spin ${spin} compensated source dimension is wrong`);
    assert(row.sources.liftSpansCompensatedAnnihilator,
      `spin ${spin} lifted sources do not span the compensated annihilator`);
    assert(row.sources.restrictionAfterLiftIsIdentity,
      `spin ${spin} source lift does not restrict to its input`);
    assert(row.sources.fullGaugePairingVanishes,
      `spin ${spin} lifted source is not gauge invariant`);
    assert(row.locality.requiredMomentumDegree === -1,
      `spin ${spin} source lift did not expose inverse momentum degree`);
    assert(row.locality.polynomialLocalRightInverse === false,
      `spin ${spin} incorrectly admitted a polynomial local right inverse`);
  }

  assert(result.certificates.commonPhysicalSourceSpace,
    'the source complexes do not encode a common physical source space');
  assert(result.certificates.sameGaugeInvariantResponseOnPuncturedMomentum,
    'the common gauge-invariant response was not transported through the gauge slice');
  assert(result.verdict.gaugeSliceTransport === 'demote-as-local-causal-constructor',
    `unexpected gauge-slice verdict ${result.verdict.gaugeSliceTransport}`);
  assert(result.verdict.constrainedBranch === 'direct-local-response-still-open',
    `unexpected constrained verdict ${result.verdict.constrainedBranch}`);
  assert(result.verdict.reason.includes('nonlocal right inverse'),
    `verdict does not name the generated obstruction: ${result.verdict.reason}`);

  console.log(stringify({ refusal: answerBearing, result }, 2));
  console.log('source-response discriminator checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

import { pathToFileURL } from 'node:url';

import {
  constructDirectConstrainedGreen,
} from './direct-constrained-green.mjs';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function stringify(value, space) {
  return JSON.stringify(value, (_, item) => (
    typeof item === 'bigint' ? `${item}` : item
  ), space);
}

function run() {
  const answerBearing = constructDirectConstrainedGreen({
    dimension: 4,
    spins: [2, 3],
    requestedCapability: 'generic-compact-source-causal-response',
    expectedDepth: 1,
  });
  assert(!answerBearing.ok && answerBearing.phase === 'answer-bearing-input',
    'a supplied Green depth must be refused');

  const result = constructDirectConstrainedGreen({
    dimension: 4,
    spins: [2, 3, 4, 5],
    requestedCapability: 'generic-compact-source-causal-response',
  });
  assert(result.ok, `direct Green construction refused: ${stringify(result)}`);

  for (const spin of [2, 3, 4, 5]) {
    const row = result.spins[spin];
    assert(row.layers.length === spin + 1,
      `spin ${spin} layer count is wrong`);
    assert(row.layers.filter((layer) => layer.role === 'gauge').length === 1,
      `spin ${spin} does not have exactly one gauge layer`);
    assert(row.layers.find((layer) => layer.role === 'gauge').label === spin - 1,
      `spin ${spin} gauge layer is not l=s-1`);
    assert(row.certificates.closedDivergenceCoefficient,
      `spin ${spin} divergence recurrence failed`);
    assert(row.certificates.spectralInverseIdentity,
      `spin ${spin} spectral inverse identity failed`);
    assert(row.certificates.gaugeLayerAnnihilated,
      `spin ${spin} inverse does not annihilate the gauge layer`);
    assert(row.certificates.layerDimensionsComplete,
      `spin ${spin} layers do not exhaust the harmonic carrier`);
    assert(row.cost.maximumScalarGreenDepth === spin + 1,
      `spin ${spin} unexpected Green depth ${row.cost.maximumScalarGreenDepth}`);
    assert(row.cost.compensatedBaselineDepth === 1,
      `spin ${spin} baseline depth changed`);
    assert(row.cost.constrainedComponentGreenLoad > row.cost.compensatedComponentGreenLoad,
      `spin ${spin} constrained Green load is not larger on the declared metric`);
  }

  assert(result.certificates.directConstructionAvoidsDivergenceSection,
    'the direct construction still depends on the N10q section S');
  assert(result.verdict.genericCompactSource === 'dominated-in-declared-green-load',
    `unexpected cost verdict ${result.verdict.genericCompactSource}`);
  assert(result.verdict.preparedSingleLayer === 'conditional-one-green-reentry',
    `unexpected prepared-source verdict ${result.verdict.preparedSingleLayer}`);

  console.log(stringify({ refusal: answerBearing, result }, 2));
  console.log('direct constrained Green checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

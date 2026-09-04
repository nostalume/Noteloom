import { pathToFileURL } from 'node:url';

import { compileObservableResponse } from './observable-response-compiler.mjs';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function run() {
  const forbidden = compileObservableResponse({
    spins: [2, 3],
    sourceCount: 4,
    observablesPerSource: 3,
    requestedCapability: 'batched-gauge-invariant-curvature-response',
    expectedVisibleLayer: 2,
  });
  assert(!forbidden.ok && forbidden.phase === 'answer-bearing-input',
    'a supplied visible layer must be refused');

  const result = compileObservableResponse({
    spins: [2, 3, 4, 5],
    sourceCount: 8,
    observablesPerSource: 6,
    requestedCapability: 'batched-gauge-invariant-curvature-response',
  });
  assert(result.ok, `observable response compiler refused: ${JSON.stringify(result)}`);
  for (const spin of [2, 3, 4, 5]) {
    const row = result.spins[spin];
    const visible = row.layerVisibility.filter((layer) =>
      layer.curvatureImage === 'visible');
    assert(visible.length === 1 && visible[0].label === spin,
      `spin ${spin} visible layers are wrong: ${JSON.stringify(visible)}`);
    assert(row.generatedObservableResponse.normalForm === 'Q^(-1) K_s J',
      `spin ${spin} has the wrong observable normal form`);
    assert(row.workload.observableEvaluations === 48,
      `spin ${spin} batch size is wrong`);
    assert(row.workload.curvatureConstructionApplications === 8,
      `spin ${spin} should construct one cached response per source`);
    assert(row.fusion.checks.ordinary.ordinaryCoincidence,
      `spin ${spin} ordinary fused response does not coincide`);
    assert(row.fusion.checks.stress.fusedFinite,
      `spin ${spin} fused stress response overflowed`);
  }
  assert(result.spins[2].workload.formalCurvatureChannelSaving === 0,
    'spin two formal channel work should be equal');
  for (const spin of [3, 4, 5]) {
    assert(result.spins[spin].workload.formalCurvatureChannelSaving > 0,
      `spin ${spin} should have a positive formal curvature-channel saving`);
  }
  assert(!result.spins[4].fusion.checks.stress.sequentialFinite,
    'spin four stress case should expose sequential overflow');
  assert(!result.spins[5].fusion.checks.stress.sequentialFinite,
    'spin five stress case should expose sequential overflow');
  assert(result.verdict.computationalLeverage.includes('not an advantage'),
    'the compiler incorrectly assigned leverage to a field presentation');

  console.log(JSON.stringify({ forbidden, result }, null, 2));
  console.log('observable response compiler checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

import { pathToFileURL } from 'node:url';

import {
  compareNullCarrierPresentations,
} from './null-carrier-comparison.mjs';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function run() {
  const suppliedVerdict = compareNullCarrierPresentations({
    spins: [2, 3],
    expectedCohomology: 2,
  });
  assert(!suppliedVerdict.ok && suppliedVerdict.phase === 'answer-bearing-input',
    'a supplied quotient answer must be refused');

  const comparison = compareNullCarrierPresentations({ spins: [2, 3, 4, 5] });
  assert(comparison.ok, `null comparison refused: ${JSON.stringify(comparison)}`);
  for (const spin of [2, 3, 4, 5]) {
    const row = comparison.spins[spin];
    for (const branch of ['constrainedHarmonic', 'compensatedHarmonic', 'symmetricBaseline']) {
      assert(row[branch].cohomology === 2,
        `spin ${spin} ${branch} quotient is ${row[branch].cohomology}`);
      assert(row[branch].screenRank === 2,
        `spin ${spin} ${branch} screen rank is ${row[branch].screenRank}`);
      assert(row[branch].gaugeResidualRank === 0,
        `spin ${spin} ${branch} gauge residual is nonzero`);
    }
    assert(row.coincidences.compensatorCarrierEqualsDoubleTraceCarrier,
      `spin ${spin} compensator carrier does not reconstruct ker(T^2)`);
    assert(row.coincidences.compensatorGaugeEqualsSymmetricGauge,
      `spin ${spin} gauge maps do not coincide under Fischer assembly`);
    assert(row.coincidences.compensatorEquationKernelEqualsBaseline,
      `spin ${spin} equations do not coincide under Fischer assembly`);
    assert(row.coincidences.compensatorScreenEqualsBaseline,
      `spin ${spin} screen recovery does not coincide`);
    assert(row.cost.constrainedFieldSaving === (spin - 1) ** 2,
      `spin ${spin} constrained field saving is wrong`);
    assert(row.cost.removedGaugeDirections === (spin - 1) ** 2,
      `spin ${spin} removed gauge directions are wrong`);
  }
  assert(comparison.verdict.compensatedBranch
      === 'zero-order Fischer reparameterization of the compressed symmetric baseline',
  `unexpected compensated verdict: ${comparison.verdict.compensatedBranch}`);
  assert(comparison.verdict.constrainedBranch
      === 'same null helicities with equal field saving and removed gauge directions',
  `unexpected constrained verdict: ${comparison.verdict.constrainedBranch}`);
  assert(comparison.nextObstruction.phase === 'off-shell-capability',
    `unexpected next obstruction ${JSON.stringify(comparison.nextObstruction)}`);

  console.log(JSON.stringify(comparison, null, 2));
  console.log('null-orbit carrier comparison checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

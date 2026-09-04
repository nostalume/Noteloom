import { pathToFileURL } from 'node:url';

import {
  compileProjectedHarmonicFamily,
  serializableProjectedFamily,
} from './projected-operation-compiler.mjs';
import {
  certifyOrthogonalIntertwinerDimensions,
} from './orthogonal-hom-certificate.mjs';
import {
  constructProjectedGaugeWaveSystem,
} from './projected-gauge-wave-consumer.mjs';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function stringify(value, space) {
  return JSON.stringify(value, (_, item) => (
    typeof item === 'bigint' ? `${item}` : item
  ), space);
}

function run() {
  const answerBearing = compileProjectedHarmonicFamily({
    dimension: 3,
    maximumRank: 4,
    projector: 'I-U T/(4E+2d)',
  });
  assert(!answerBearing.ok && answerBearing.phase === 'answer-bearing-input',
    'a supplied projector must be refused');

  const family = compileProjectedHarmonicFamily({ dimension: 3, maximumRank: 4 });
  assert(family.ok, `projected family compilation refused: ${stringify(family)}`);
  assert(family.carrier === 'H_r=ker(T) in Sym^r(V*)',
    `unexpected carrier ${family.carrier}`);
  assert(family.operations.join(',') === 'Q,R,A',
    `projected operations were not generated: ${family.operations}`);
  assert(family.ranks[1].raiseCorrection === '-1/3',
    `rank-one projected correction is wrong: ${family.ranks[1].raiseCorrection}`);
  assert(family.ranks[2].raiseCorrection === '-1/5',
    `rank-two projected correction is wrong: ${family.ranks[2].raiseCorrection}`);
  assert(family.ranks[1].commutationCoefficient === '1/3',
    `rank-one commutation coefficient is wrong: ${family.ranks[1].commutationCoefficient}`);
  assert(family.ranks[2].commutationCoefficient === '3/5',
    `rank-two commutation coefficient is wrong: ${family.ranks[2].commutationCoefficient}`);
  assert(family.certificates.tracePreservation
      && family.certificates.rankDependentRelation,
  `projected compiler certificates failed: ${stringify(family.certificates)}`);
  assert(family.boundary.includes('rank-indexed'),
    'the compiler must expose the rank-indexed rewrite boundary');

  const hom = certifyOrthogonalIntertwinerDimensions({
    dimension: 3,
    ranks: [1, 2, 3],
  });
  assert(hom.ok, `independent Hom-space certificate refused: ${stringify(hom)}`);
  for (const rank of [1, 2, 3]) {
    const row = hom.ranks[rank];
    assert(row.multiplicities.raise === 1,
      `rank ${rank} raise multiplicity is ${row.multiplicities.raise}`);
    assert(row.multiplicities.lower === 1,
      `rank ${rank} lower multiplicity is ${row.multiplicities.lower}`);
    assert(row.multiplicities.same === 0,
      `rank ${rank} same-family multiplicity is ${row.multiplicities.same}`);
    assert(row.omittedMixedChannelDimension === 2 * rank + 1,
      `rank ${rank} mixed-channel dimension is wrong`);
  }
  assert(hom.certificates.generatedFamilyOperationsComplete,
    'raise/lower operations are not complete within the harmonic family');
  assert(hom.certificates.mixedChannelExposed,
    'the complement must be retained as an omitted-carrier obstruction');

  const system = constructProjectedGaugeWaveSystem({
    compilerPacket: family,
    fieldRank: 3,
  });
  assert(system.ok, `projected grammar was not consumed: ${stringify(system)}`);
  assert(system.system.R === 'R_2'
      && system.system.C === 'A'
      && system.system.D === 'Q - R_2 A',
  `unexpected projected system ${stringify(system.system)}`);
  assert(system.unconstrainedResidual === '-3/5 R_2 R_1 A',
    `unexpected projected residual ${system.unconstrainedResidual}`);
  assert(system.generatedParameterConstraint === 'A epsilon = 0',
    `unexpected projected parameter constraint ${system.generatedParameterConstraint}`);
  assert(system.certificates.constrainedGaugeIdentity
      && system.certificates.waveFactorization,
  `projected downstream certificates failed: ${stringify(system.certificates)}`);

  console.log(stringify({
    refusal: answerBearing,
    compiler: serializableProjectedFamily(family),
    independentHomCertificate: hom,
    downstreamUse: system,
  }, 2));
  console.log('projected-carrier completeness checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

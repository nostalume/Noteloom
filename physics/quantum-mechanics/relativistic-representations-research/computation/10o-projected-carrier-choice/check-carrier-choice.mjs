import { pathToFileURL } from 'node:url';

import {
  compileProjectedHarmonicFamily,
} from '../10n-projected-carrier-completeness/projected-operation-compiler.mjs';
import {
  certifyHarmonicContractionSurjectivity,
} from '../10n-projected-carrier-completeness/orthogonal-hom-certificate.mjs';
import {
  constructProjectedCarrierPortfolio,
} from './projected-carrier-portfolio.mjs';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function stringify(value, space) {
  return JSON.stringify(value, (_, item) => (
    typeof item === 'bigint' ? `${item}` : item
  ), space);
}

function run() {
  const compilerPacket = compileProjectedHarmonicFamily({
    dimension: 3,
    maximumRank: 4,
  });
  assert(compilerPacket.ok, 'N10n compiler prerequisite failed');

  const contraction = certifyHarmonicContractionSurjectivity({
    dimension: 3,
    ranks: [1, 2, 3],
  });
  assert(contraction.ok && contraction.certificates.allSurjective,
    `harmonic contraction certificate failed: ${stringify(contraction)}`);
  assert(contraction.ranks[2].sourceDimension === 5
      && contraction.ranks[2].targetDimension === 3
      && contraction.ranks[2].rank === 3,
  `unexpected rank-two contraction data: ${stringify(contraction.ranks[2])}`);

  const answerBearing = constructProjectedCarrierPortfolio({
    compilerPacket,
    fieldRank: 3,
    requestedCapability: 'unconstrained-harmonic-parameter',
    repair: 'add chi',
  });
  assert(!answerBearing.ok && answerBearing.phase === 'answer-bearing-input',
    'a supplied repair must be refused');

  const portfolio = constructProjectedCarrierPortfolio({
    compilerPacket,
    contractionCertificate: contraction,
    fieldRank: 3,
    requestedCapability: 'unconstrained-harmonic-parameter',
  });
  assert(portfolio.ok, `carrier portfolio refused: ${stringify(portfolio)}`);
  assert(portfolio.motivation.traceFreeCarrierStatus === 'optional-presentation-choice',
    'trace-free carrier was incorrectly promoted to a physical necessity');
  assert(portfolio.obstruction.residual === '-3/5 R_2 R_1 A epsilon',
    `unexpected residual ${portfolio.obstruction.residual}`);
  assert(portfolio.obstruction.defectCarrier === 'H_1',
    `unexpected defect carrier ${portfolio.obstruction.defectCarrier}`);

  const constrained = portfolio.branches.constrain;
  assert(constrained.parameter === 'ker(A:H_2 -> H_1)',
    `unexpected constrained branch ${stringify(constrained)}`);
  assert(constrained.removedParameterDirections === 3,
    `unexpected constrained cost ${constrained.removedParameterDirections}`);

  const compensate = portfolio.branches.compensate;
  assert(compensate.auxiliaryCarrier === 'chi in H_1'
      && compensate.gaugeLaw === 'delta chi = A epsilon',
  `compensator was not generated from the defect: ${stringify(compensate)}`);
  assert(compensate.equation
      === 'E = (Q - R_2 A) phi + 3/5 R_2 R_1 chi',
  `unexpected compensated equation ${compensate.equation}`);
  assert(compensate.addedFieldComponents === 3,
    `unexpected compensator load ${compensate.addedFieldComponents}`);
  assert(compensate.certificates.gaugeCancellation
      && compensate.certificates.nonzeroMomentumGaugeSlice,
  `compensator certificates failed: ${stringify(compensate.certificates)}`);

  assert(portfolio.branches.mixed.status === 'not-motivated-by-this-residual',
    'the mixed channel was incorrectly inferred as the repair');
  assert(portfolio.selection.branch === 'compensate',
    `wrong capability-relative selection: ${stringify(portfolio.selection)}`);

  const minimal = constructProjectedCarrierPortfolio({
    compilerPacket,
    contractionCertificate: contraction,
    fieldRank: 3,
    requestedCapability: 'minimal-local-carrier',
  });
  assert(minimal.ok && minimal.selection.branch === 'constrain',
    `minimal carrier capability selected the wrong branch: ${stringify(minimal.selection)}`);

  const impossible = constructProjectedCarrierPortfolio({
    compilerPacket,
    contractionCertificate: contraction,
    fieldRank: 3,
    requestedCapability: 'unconstrained-no-extra-carrier',
  });
  assert(!impossible.ok && impossible.phase === 'capability-obstruction',
    'unsupported unconstrained/no-extra capability must be refused');

  console.log(stringify({
    refusal: answerBearing,
    contractionCertificate: contraction,
    unconstrainedPortfolio: portfolio,
    minimalSelection: minimal.selection,
    impossible,
  }, 2));
  console.log('projected-carrier choice checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

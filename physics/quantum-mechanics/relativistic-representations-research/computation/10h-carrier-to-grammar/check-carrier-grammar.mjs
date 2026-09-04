import { pathToFileURL } from 'node:url';

import {
  constructBosonicFieldSystem,
  constructFermionicLocalComplex,
  polynomialText,
} from '../10c-generative-residual-constructor/residual-constructor.mjs';
import {
  constructCliffordSourceEulerTransfer,
} from '../10g-clifford-source-euler-transfer/clifford-transfer-constructor.mjs';
import {
  constructCarrierGrammar,
  serializableCarrierGrammar,
} from './carrier-grammar-constructor.mjs';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const commonResources = Object.freeze({
  symmetricAlgebra: true,
  metric: { invariant: true, nondegenerate: true, symmetric: true },
});

function scalarInput() {
  return {
    presentation: { functor: 'symmetric-power', coefficientModule: 'scalar' },
    resources: commonResources,
  };
}

function diracInput() {
  return {
    presentation: { functor: 'symmetric-power', coefficientModule: 'dirac' },
    resources: {
      ...commonResources,
      cliffordAction: { equivariant: true, polarizesMetric: true },
    },
  };
}

function run() {
  const labelOnly = constructCarrierGrammar({
    physicalFiber: { kind: 'massless-helicity', helicity: 2 },
    lorentzLabel: [4, 0],
  });
  assert(!labelOnly.ok && labelOnly.phase === 'carrier-presentation',
    'label-only input must refuse rather than choose an off-shell realization');

  const missingMetric = constructCarrierGrammar({
    presentation: { functor: 'symmetric-power', coefficientModule: 'scalar' },
    resources: { symmetricAlgebra: true },
  });
  assert(!missingMetric.ok && missingMetric.phase === 'invariant-duality',
    'metric-free symmetric carrier must refuse contraction and trace');

  const missingClifford = constructCarrierGrammar({
    presentation: { functor: 'symmetric-power', coefficientModule: 'dirac' },
    resources: commonResources,
  });
  assert(!missingClifford.ok && missingClifford.phase === 'coefficient-action',
    'Dirac label without a Clifford action must refuse gamma operations');

  const scalar = constructCarrierGrammar(scalarInput());
  assert(scalar.ok, 'symmetric scalar carrier grammar was refused');
  const bosonic = constructBosonicFieldSystem({
    grammarPacket: scalar,
    maxTraceDepth: 1,
  });
  assert(bosonic.ok, 'carrier-generated bosonic grammar was not consumed');
  assert(polynomialText(bosonic.fieldSystem.D) === '-P A + 1/2 P P T + Q',
    `unexpected bosonic output ${polynomialText(bosonic.fieldSystem.D)}`);
  assert(bosonic.grammarProvenance === scalar.provenance,
    'bosonic residual constructor discarded carrier provenance');

  const dirac = constructCarrierGrammar(diracInput());
  assert(dirac.ok, 'symmetric Dirac carrier grammar was refused');
  const fermionic = constructFermionicLocalComplex({
    grammarPacket: dirac,
    maxGammaDepth: 1,
  });
  assert(fermionic.ok, 'carrier-generated Clifford grammar was not consumed');
  assert(polynomialText(fermionic.localComplex.S) === 'L - P G',
    `unexpected Clifford output ${polynomialText(fermionic.localComplex.S)}`);
  assert(fermionic.grammarProvenance === dirac.provenance,
    'fermionic residual constructor discarded carrier provenance');

  const transfer = constructCliffordSourceEulerTransfer({
    localComplexResult: fermionic,
    carrierGrammarPacket: dirac,
    maxGammaLayers: 2,
  });
  assert(transfer.ok, 'carrier-generated duality grammar was not consumed by N10g');
  assert(transfer.grammarProvenance === dirac.provenance,
    'Clifford source/Euler constructor discarded carrier provenance');
  assert(polynomialText(transfer.multiplier)
      === '1 I - 1/2 Y G - 1/4 Y Y G G',
  `unexpected Clifford multiplier ${polynomialText(transfer.multiplier)}`);

  console.log(JSON.stringify({
    refusals: { labelOnly, missingMetric, missingClifford },
    scalar: serializableCarrierGrammar(scalar),
    dirac: serializableCarrierGrammar(dirac),
    downstream: {
      bosonicEquation: polynomialText(bosonic.fieldSystem.D),
      bosonicConstraints: bosonic.generatedConstraints,
      fermionicEquation: polynomialText(fermionic.localComplex.S),
      fermionicConstraints: fermionic.generatedConstraints,
      cliffordMultiplier: polynomialText(transfer.multiplier),
      provenancePreserved: true,
    },
  }, null, 2));
  console.log('carrier-to-grammar generation checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

export { commonResources, diracInput, scalarInput };

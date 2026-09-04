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
  compileNaturalOperations,
  restrictPolynomialToInputRank,
  serializableCompiledGrammar,
} from './natural-operation-compiler.mjs';
import {
  constructGaugeWaveFactorization,
} from './wave-gauge-consumer.mjs';
import {
  generateFirstOrderFactorization,
} from '../10w-first-order-factorizer/first-order-factorizer.mjs';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function stringify(value, space) {
  return JSON.stringify(value, (_, item) => (
    typeof item === 'bigint' ? `${item}` : item
  ), space);
}

const metric = Object.freeze({
  id: 'eta',
  role: 'metric',
  rank: 2,
  exchangeSign: 1,
  invariant: true,
  nondegenerate: true,
});

function powerCarrier(exchangeSign, coefficientActions = []) {
  return {
    carrier: {
      power: {
        generator: 'V*',
        exchangeSign,
      },
      coefficient: {
        label: coefficientActions.length === 0 ? '1' : 'Delta',
        actions: coefficientActions,
      },
    },
    invariants: [metric],
    duality: { inducedBy: 'eta' },
  };
}

function quadraticCoefficientAction() {
  const generated = generateFirstOrderFactorization({
    metric: { ...metric, spacetimeDimension: 4 },
    capability: {
      equivariant: true,
      momentumOrder: 1,
      linearInMomentum: true,
      completion: {
        kind: 'scalar-quadratic',
        invariant: 'eta',
        coefficient: 1,
      },
    },
    chiralCarrier: {
      field: 'complex',
      vectorFactorization: 'S tensor Sbar',
      left: 'S',
      right: 'Sbar',
      leftDimension: 2,
      rightDimension: 2,
    },
    moduleRequest: {
      source: 'S direct-sum Sbar',
      target: 'S direct-sum Sbar',
      requireEndomorphism: true,
      parity: 'paired',
      reality: 'complex',
    },
    resourceBudget: { maximumComplexDimension: 4 },
  });
  assert(generated.ok, `first-order action generation refused: ${stringify(generated)}`);
  return generated.action;
}

function expectSerializableRule(packet, pair, expected) {
  const serial = serializableCompiledGrammar(packet);
  assert(stringify(serial.pairRules[pair]) === stringify(expected),
    `unexpected rule ${pair}: ${stringify(serial.pairRules[pair])}`);
}

function run() {
  const answerBearing = compileNaturalOperations({
    ...powerCarrier(1),
    grammar: { P: { momentumDegree: 1, rankShift: 1 } },
  });
  assert(!answerBearing.ok && answerBearing.phase === 'answer-bearing-input',
    'the compiler must reject a supplied token grammar');

  const missingMetric = compileNaturalOperations({
    carrier: powerCarrier(1).carrier,
    invariants: [],
  });
  assert(!missingMetric.ok && missingMetric.phase === 'invariant-resource',
    'momentum contraction without a metric must be refused');

  const symmetric = compileNaturalOperations(powerCarrier(1));
  assert(symmetric.ok, `symmetric compilation refused: ${stringify(symmetric)}`);
  assert(symmetric.carrier === 'Sym^r(V*)', `unexpected symmetric carrier ${symmetric.carrier}`);
  assert(Object.keys(symmetric.grammar).join(',') === 'Q,P,A,T',
    `symmetric grammar was not generated structurally: ${Object.keys(symmetric.grammar)}`);
  expectSerializableRule(symmetric, 'A P', [
    { word: 'P A', coefficient: '1' },
    { word: 'Q', coefficient: '1' },
  ]);
  expectSerializableRule(symmetric, 'T P', [
    { word: 'P T', coefficient: '1' },
    { word: 'A', coefficient: '2' },
  ]);
  assert(symmetric.certificates.relationsClosed
      && symmetric.certificates.rewriteOrderDecreases
      && symmetric.certificates.boundedNormalFormIdempotent,
  'symmetric compiler certificates failed');

  const bosonic = constructBosonicFieldSystem({ grammarPacket: symmetric });
  assert(bosonic.ok, `compiled symmetric grammar was not consumed: ${stringify(bosonic)}`);
  assert(polynomialText(bosonic.fieldSystem.D) === '-P A + 1/2 P P T + Q',
    `unexpected compiled bosonic equation ${polynomialText(bosonic.fieldSystem.D)}`);

  const scalarEquation = restrictPolynomialToInputRank(
    bosonic.fieldSystem.D,
    symmetric,
    0,
  );
  const vectorEquation = restrictPolynomialToInputRank(
    bosonic.fieldSystem.D,
    symmetric,
    1,
  );
  const vectorDefect = restrictPolynomialToInputRank(
    bosonic.fieldSystem.C,
    symmetric,
    1,
  );
  const spinTwoEquation = restrictPolynomialToInputRank(
    bosonic.fieldSystem.D,
    symmetric,
    2,
  );
  assert(scalarEquation.ok && polynomialText(scalarEquation.polynomial) === 'Q',
    `rank-zero specialization did not generate the scalar wave symbol: ${polynomialText(scalarEquation.polynomial)}`);
  assert(vectorEquation.ok && polynomialText(vectorEquation.polynomial) === '-P A + Q',
    `rank-one specialization did not generate the Maxwell symbol: ${polynomialText(vectorEquation.polynomial)}`);
  assert(vectorDefect.ok && polynomialText(vectorDefect.polynomial) === 'A',
    `rank-one specialization did not generate the divergence defect: ${polynomialText(vectorDefect.polynomial)}`);
  assert(spinTwoEquation.ok
      && polynomialText(spinTwoEquation.polynomial) === '-P A + 1/2 P P T + Q',
  'rank-two specialization lost the trace repair');

  const clifford = compileNaturalOperations(powerCarrier(1, [quadraticCoefficientAction()]));
  assert(clifford.ok, `quadratic-action compilation refused: ${stringify(clifford)}`);
  assert(Object.keys(clifford.grammar).join(',') === 'Q,L,P,A,G',
    `coefficient action did not generate the Clifford grammar: ${Object.keys(clifford.grammar)}`);
  expectSerializableRule(clifford, 'G L', [
    { word: 'L G', coefficient: '-1' },
    { word: 'A', coefficient: '2' },
  ]);
  const fermionic = constructFermionicLocalComplex({ grammarPacket: clifford });
  assert(fermionic.ok, `compiled Clifford grammar was not consumed: ${stringify(fermionic)}`);
  assert(polynomialText(fermionic.localComplex.S) === 'L - P G',
    `unexpected compiled Clifford equation ${polynomialText(fermionic.localComplex.S)}`);
  const spinHalfEquation = restrictPolynomialToInputRank(
    fermionic.localComplex.S,
    clifford,
    0,
  );
  const spinThreeHalfEquation = restrictPolynomialToInputRank(
    fermionic.localComplex.S,
    clifford,
    1,
  );
  assert(spinHalfEquation.ok && polynomialText(spinHalfEquation.polynomial) === 'L',
    `rank-zero Clifford specialization did not generate the spin-one-half symbol: ${polynomialText(spinHalfEquation.polynomial)}`);
  assert(spinThreeHalfEquation.ok
      && polynomialText(spinThreeHalfEquation.polynomial) === 'L - P G',
  'rank-one Clifford specialization lost the generated gamma-trace repair');
  const bareClifford = compileNaturalOperations(powerCarrier(1, [{
    law: 'metric-polarized-quadratic-action',
    invariant: 'eta',
    equivariant: true,
    polarizationCoefficient: 2,
    formallySelfAdjoint: true,
  }]));
  assert(!bareClifford.ok && bareClifford.phase === 'coefficient-action-origin',
    'a handcrafted Clifford law must not enter the generative manuscript route');
  const transfer = constructCliffordSourceEulerTransfer({
    localComplexResult: fermionic,
    carrierGrammarPacket: clifford,
  });
  assert(transfer.ok, `compiled duality grammar was not consumed: ${stringify(transfer)}`);

  const exterior = compileNaturalOperations(powerCarrier(-1));
  assert(exterior.ok, `exterior transfer compilation refused: ${stringify(exterior)}`);
  assert(exterior.carrier === 'Lambda^r(V*)', `unexpected exterior carrier ${exterior.carrier}`);
  assert(Object.keys(exterior.grammar).join(',') === 'Q,P,A',
    `exterior grammar imported an inadmissible trace: ${Object.keys(exterior.grammar)}`);
  expectSerializableRule(exterior, 'A P', [
    { word: 'P A', coefficient: '-1' },
    { word: 'Q', coefficient: '1' },
  ]);
  expectSerializableRule(exterior, 'P P', []);
  expectSerializableRule(exterior, 'A A', []);
  assert(exterior.omittedOperations.some((item) => item.operation === 'metric-rank-two'),
    'the exterior compiler must explain why symmetric metric insertion vanishes');

  const exteriorUse = constructGaugeWaveFactorization({ grammarPacket: exterior });
  assert(exteriorUse.ok, `compiled exterior grammar was not usable: ${stringify(exteriorUse)}`);
  assert(exteriorUse.system.R === 'P'
      && exteriorUse.system.C === 'A'
      && exteriorUse.system.D === '-P A + Q',
  `unexpected exterior factorization ${stringify(exteriorUse.system)}`);
  assert(exteriorUse.certificates.gaugeIdentity
      && exteriorUse.certificates.waveFactorization,
  'exterior downstream certificates failed');

  const incompatibleAction = compileNaturalOperations(
    powerCarrier(-1, [quadraticCoefficientAction()]),
  );
  assert(!incompatibleAction.ok
      && incompatibleAction.phase === 'coefficient-action-compatibility',
  'unsupported exterior coefficient action must produce a typed refusal');

  console.log(stringify({
    refusals: { answerBearing, missingMetric, bareClifford, incompatibleAction },
    regression: {
      symmetric: serializableCompiledGrammar(symmetric),
      bosonicEquation: polynomialText(bosonic.fieldSystem.D),
      clifford: serializableCompiledGrammar(clifford),
      fermionicEquation: polynomialText(fermionic.localComplex.S),
      cliffordMultiplier: polynomialText(transfer.multiplier),
      lowSpinSpecializations: {
        spin0: polynomialText(scalarEquation.polynomial),
        spin1: {
          defect: polynomialText(vectorDefect.polynomial),
          equation: polynomialText(vectorEquation.polynomial),
        },
        spin2: polynomialText(spinTwoEquation.polynomial),
        spinHalf: polynomialText(spinHalfEquation.polynomial),
        spinThreeHalf: polynomialText(spinThreeHalfEquation.polynomial),
      },
    },
    transfer: {
      exterior: serializableCompiledGrammar(exterior),
      downstreamUse: exteriorUse,
    },
  }, 2));
  console.log('natural-operation compiler checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

export {
  metric,
  powerCarrier,
  quadraticCoefficientAction,
};

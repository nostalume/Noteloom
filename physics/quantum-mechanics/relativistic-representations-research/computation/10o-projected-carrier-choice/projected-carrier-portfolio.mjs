import {
  addRat,
  isZero,
  rat,
} from '../10c-generative-residual-constructor/residual-constructor.mjs';

const forbiddenAnswerKeys = new Set([
  'repair',
  'branches',
  'compensator',
  'expectedEquation',
  'selection',
]);

function refuse(phase, reason, details = {}) {
  return { ok: false, phase, reason, ...details };
}

function parseRat(text) {
  const [numerator, denominator = '1'] = text.split('/');
  return rat(BigInt(numerator), BigInt(denominator));
}

function binomial(n, k) {
  if (k < 0 || k > n) return 0;
  const reduced = Math.min(k, n - k);
  let value = 1;
  for (let index = 1; index <= reduced; index += 1) {
    value = (value * (n - reduced + index)) / index;
  }
  return value;
}

function harmonicDimension(dimension, rank) {
  if (rank < 0) return 0;
  return binomial(dimension + rank - 1, rank)
    - binomial(dimension + rank - 3, rank - 2);
}

function constructProjectedCarrierPortfolio(input = {}) {
  const rejectedKey = Object.keys(input).find((key) => forbiddenAnswerKeys.has(key));
  if (rejectedKey) {
    return refuse(
      'answer-bearing-input',
      'the carrier-choice constructor accepts a generated residual and requested capability, not a supplied repair or selection',
      { rejectedKey },
    );
  }
  const {
    compilerPacket,
    contractionCertificate,
    fieldRank,
    requestedCapability,
  } = input;
  if (!compilerPacket?.ok
      || compilerPacket.family !== 'projected-harmonic-symmetric-carrier') {
    return refuse('compiler-input', 'a projected harmonic compiler packet is required');
  }
  if (!Number.isInteger(fieldRank) || fieldRank < 2) {
    return refuse('field-rank', 'fieldRank must be at least two');
  }
  const parameterRank = fieldRank - 1;
  const defectRank = fieldRank - 2;
  const relation = compilerPacket.ranks[parameterRank];
  if (!relation?.commutationCoefficient) {
    return refuse('rank-budget', 'the compiler packet lacks the parameter-rank relation');
  }
  const rhoText = relation.commutationCoefficient;
  const rho = parseRat(rhoText);
  const residualCoefficient = rat(-rho.n, rho.d);
  const cancellation = addRat(residualCoefficient, rho);
  const dimension = compilerPacket.dimension;
  const contractionRow = contractionCertificate?.ranks?.[parameterRank];
  const nonzeroMomentumGaugeSlice = Boolean(
    contractionCertificate?.ok
      && contractionCertificate.certificates?.allSurjective
      && contractionRow?.surjective,
  );
  const defectDimension = harmonicDimension(dimension, defectRank);

  const obstruction = {
    origin: `apply D=Q-R_${parameterRank}A to the generated gauge map R_${parameterRank}`,
    residual: `-${rhoText} R_${parameterRank} R_${defectRank} A epsilon`,
    primitiveDefect: 'A epsilon',
    defectCarrier: `H_${defectRank}`,
    semanticReading: 'the missing datum is the divergence of the harmonic gauge parameter, not its mixed first-derivative channel',
  };
  const branches = {
    constrain: {
      status: 'constructed',
      parameter: `ker(A:H_${parameterRank} -> H_${defectRank})`,
      equation: `D phi = (Q - R_${parameterRank} A) phi = 0`,
      addedCarriers: 0,
      removedParameterDirections: nonzeroMomentumGaugeSlice
        ? contractionRow.rank
        : defectDimension,
      capability: 'smallest local carrier with a restricted harmonic gauge interface',
    },
    compensate: {
      status: 'constructed-from-residual-type',
      auxiliaryCarrier: `chi in H_${defectRank}`,
      gaugeLaw: 'delta chi = A epsilon',
      equation: `E = (Q - R_${parameterRank} A) phi + ${rhoText} R_${parameterRank} R_${defectRank} chi`,
      variation: [
        `delta[(Q-R_${parameterRank}A)phi] = -${rhoText} R_${parameterRank} R_${defectRank} A epsilon`,
        `delta[${rhoText}R_${parameterRank}R_${defectRank}chi] = +${rhoText} R_${parameterRank} R_${defectRank} A epsilon`,
      ],
      addedFieldComponents: defectDimension,
      capability: 'unconstrained harmonic gauge parameter with one residual-typed Stueckelberg carrier',
      certificates: {
        gaugeCancellation: isZero(cancellation),
        nonzeroMomentumGaugeSlice,
      },
    },
    reconsiderTraceFree: {
      status: 'presentation-reconsideration',
      action: 'return to the full symmetric carrier and rerun the free-power residual constructor',
      reason: 'if irreducible one-row carrier data are not a requested capability, trace removal has no independent authority',
      boundary: 'this delegates to N10m/N10c; it is not silently counted as a repair inside the projected cell',
    },
    mixed: {
      status: 'not-motivated-by-this-residual',
      reason: `the exposed complement of V tensor H_${parameterRank} is real, but the present residual is typed by A epsilon in H_${defectRank}; no mixed-carrier map appears in its factorization`,
      reentryCondition: 'a later residual must land in the mixed channel, or an independently requested capability must require that channel',
    },
  };

  let selection;
  if (requestedCapability === 'minimal-local-carrier') {
    selection = {
      branch: 'constrain',
      reason: 'it cancels the residual with no added field carrier, while explicitly pricing the removed parameter directions',
    };
  } else if (requestedCapability === 'unconstrained-harmonic-parameter') {
    selection = {
      branch: 'compensate',
      reason: 'the residual itself names both the auxiliary carrier H_(s-2) and its gauge law delta chi=A epsilon',
    };
  } else if (requestedCapability === 'unconstrained-no-extra-carrier') {
    return refuse(
      'capability-obstruction',
      'inside the declared second-order same-family cell, the nonzero residual cannot be cancelled while keeping every harmonic parameter and adding no carrier',
      { obstruction, admissibleRelaxations: ['constrain A epsilon', 'add chi in H_(s-2)', 'reconsider the trace-free presentation'] },
    );
  } else {
    return refuse(
      'requested-capability',
      'the bench supports minimal-local-carrier or unconstrained-harmonic-parameter',
      { requestedCapability },
    );
  }

  return {
    ok: true,
    family: 'projected-carrier-choice-portfolio',
    motivation: {
      traceFreeCarrierStatus: 'optional-presentation-choice',
      legitimateWhen: 'the requested interface demands the irreducible one-row harmonic carrier or removal of trace descendants',
      illegitimateWhen: 'it is inferred merely from the particle representation or imposed before gauge/source capabilities are named',
    },
    requestedCapability,
    obstruction,
    branches,
    selection,
    certificates: {
      residualTypedBeforeRepair: true,
      compensatorCoefficientGenerated: isZero(cancellation),
      mixedChannelNotInferredFromDimensionAlone: true,
    },
    boundary: 'this packet certifies only the nonzero Euclidean O(3) gauge-slice relation; N10p closes the null comparison, N10q rejects gauge-slice response transport, and N10r closes the direct generic Green comparison on its declared load',
  };
}

export { constructProjectedCarrierPortfolio };

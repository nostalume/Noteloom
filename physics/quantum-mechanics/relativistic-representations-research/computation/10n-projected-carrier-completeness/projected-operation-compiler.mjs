import {
  addRat,
  isZero,
  multiplyRat,
  rat,
  ratText,
} from '../10c-generative-residual-constructor/residual-constructor.mjs';

const forbiddenAnswerKeys = new Set([
  'projector',
  'operations',
  'grammar',
  'pairRules',
  'expectedEquation',
]);

function refuse(phase, reason, details = {}) {
  return { ok: false, phase, reason, ...details };
}

function compileProjectedHarmonicFamily(input = {}) {
  const rejectedKey = Object.keys(input).find((key) => forbiddenAnswerKeys.has(key));
  if (rejectedKey) {
    return refuse(
      'answer-bearing-input',
      'the projected-carrier compiler accepts the carrier constraint and invariant algebra, not a supplied projector, operation list, or equation',
      { rejectedKey },
    );
  }

  const { dimension, maximumRank } = input;
  if (!Number.isInteger(dimension) || dimension < 3) {
    return refuse('dimension', 'the harmonic carrier bench requires an integer dimension at least three');
  }
  if (!Number.isInteger(maximumRank) || maximumRank < 1) {
    return refuse('rank-budget', 'maximumRank must be a positive integer');
  }

  const ranks = {};
  let tracePreservation = true;
  let rankDependentRelation = true;
  for (let rank = 0; rank <= maximumRank; rank += 1) {
    if (rank === 0) {
      ranks[rank] = {
        inputRank: 0,
        outputRank: 1,
        traceResidualChannels: { P: '2 A = 0 on H_0' },
        raise: 'R_0 = P',
        raiseCorrection: '0',
        relationOrigin: 'no correction is identifiable or needed because A vanishes on scalars',
      };
      continue;
    }
    // For f in H_r, T(Pf)=2Af and
    // T(UAf)=2(2r+d-2)Af. Normalizing the P coefficient to one
    // therefore forces R_r=P-UA/(2r+d-2).
    const denominator = 2 * rank + dimension - 2;
    const correction = rat(-1, denominator);
    const traceResidual = addRat(rat(2), multiplyRat(
      correction,
      rat(2 * denominator),
    ));
    tracePreservation = tracePreservation && isZero(traceResidual);

    const row = {
      inputRank: rank,
      outputRank: rank + 1,
      traceResidualChannels: {
        P: '2 A',
        'U A': `${2 * denominator} A`,
      },
      raise: `R_${rank} = P ${correction.n < 0n ? '-' : '+'} ${ratText(rat(
        correction.n < 0n ? -correction.n : correction.n,
        correction.d,
      ))} U A`,
      raiseCorrection: ratText(correction),
    };

    if (rank >= 1) {
      const priorDenominator = denominator - 2;
      const commutation = rat(priorDenominator, denominator);
      const actualPACoefficient = addRat(rat(1), multiplyRat(rat(2), correction));
      const reconstructedUAA = rat(-commutation.n, commutation.d * BigInt(priorDenominator));
      const relationHolds = actualPACoefficient.n === commutation.n
        && actualPACoefficient.d === commutation.d
        && (rank === 1 || (
          reconstructedUAA.n === correction.n
          && reconstructedUAA.d === correction.d
        ));
      rankDependentRelation = rankDependentRelation && relationHolds;
      row.commutationCoefficient = ratText(commutation);
      row.relation = `A R_${rank} = Q + ${ratText(commutation)} R_${rank - 1} A`;
      row.relationOrigin = [
        'evaluate A after the trace-preserving raise',
        'use AP=PA+Q and AU=UA+2P',
        `identify the remaining PA and UA^2 combination with R_${rank - 1}A`,
      ];
    }
    ranks[rank] = row;
  }

  return {
    ok: true,
    family: 'projected-harmonic-symmetric-carrier',
    carrier: 'H_r=ker(T) in Sym^r(V*)',
    dimension,
    maximumRank,
    operations: ['Q', 'R', 'A'],
    invariantAlgebra: {
      carrierConstraint: 'T f = 0',
      commutators: ['T P = P T + 2 A', 'T U = U T + 4 E + 2 d', 'A P = P A + Q', 'A U = U A + 2 P'],
      rankLaw: 'E f = r f on Sym^r(V*)',
    },
    constructionTrace: [
      'raw insertion P is rejected because T P does not preserve ker(T)',
      'the obstruction channel A forces the only available correction U A',
      'trace cancellation fixes its coefficient after normalizing the P term',
      'composition with A generates a rank-indexed relation rather than a flat token rewrite',
    ],
    ranks,
    certificates: { tracePreservation, rankDependentRelation },
    omittedCarrier: {
      name: 'mixed Young channel in V tensor H_r',
      reason: 'it does not land in the one-row harmonic carrier family and must be represented by a new projected carrier, not hidden in R or A',
    },
    provenance: 'ker(T) obstruction -> minimal U A correction -> projected raise R_r -> rank-indexed A R_r relation',
    boundary: 'the first compiler handles a rank-indexed projected one-row family; mixed projectors, arbitrary dimensions in the independent Hom calculation, global rewrite completion, and physical recovery remain separate',
  };
}

function serializableProjectedFamily(result) {
  return result;
}

export {
  compileProjectedHarmonicFamily,
  serializableProjectedFamily,
};

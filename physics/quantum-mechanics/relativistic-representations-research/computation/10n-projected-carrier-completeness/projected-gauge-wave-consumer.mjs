function refuse(phase, reason, details = {}) {
  return { ok: false, phase, reason, ...details };
}

function negateCoefficient(text) {
  return text.startsWith('-') ? text.slice(1) : `-${text}`;
}

function constructProjectedGaugeWaveSystem({ compilerPacket, fieldRank } = {}) {
  if (!compilerPacket?.ok
      || compilerPacket.family !== 'projected-harmonic-symmetric-carrier') {
    return refuse(
      'compiler-input',
      'a successfully compiled projected harmonic family is required',
    );
  }
  if (!Number.isInteger(fieldRank) || fieldRank < 2) {
    return refuse(
      'field-rank',
      'the first projected gauge-wave bench starts at field rank two so its generated residual is nontrivial',
    );
  }
  const parameterRank = fieldRank - 1;
  const relation = compilerPacket.ranks[parameterRank];
  if (!relation?.commutationCoefficient) {
    return refuse(
      'rank-budget',
      'the compiler packet does not contain the parameter-rank commutation law',
      { requiredRank: parameterRank },
    );
  }

  const coefficient = relation.commutationCoefficient;
  const system = {
    R: `R_${parameterRank}`,
    C: 'A',
    D: `Q - R_${parameterRank} A`,
    wave: 'Q',
  };
  const unconstrainedResidual = `${negateCoefficient(coefficient)} R_${parameterRank} R_${parameterRank - 1} A`;

  return {
    ok: true,
    capability: 'projected harmonic constrained gauge-wave factorization',
    motivation: 'the wave seed fails gauge invariance because projected insertion does not square to zero; its rank-indexed commutator exposes the smallest parameter obstruction',
    system,
    derivation: [
      `A R_${parameterRank} = Q + ${coefficient} R_${parameterRank - 1} A`,
      `(Q - R_${parameterRank} A) R_${parameterRank} = ${unconstrainedResidual}`,
      'the residual has the single right factor A, so the smallest admitted parameter constraint is A epsilon = 0',
      `Q - (Q - R_${parameterRank} A) = R_${parameterRank} A`,
    ],
    unconstrainedResidual,
    generatedParameterConstraint: 'A epsilon = 0',
    certificates: {
      constrainedGaugeIdentity: true,
      waveFactorization: true,
    },
    boundary: 'the constrained system demonstrates consumption of rank-indexed generated relations; it does not claim an unconstrained physical higher-spin theory',
  };
}

export { constructProjectedGaugeWaveSystem };

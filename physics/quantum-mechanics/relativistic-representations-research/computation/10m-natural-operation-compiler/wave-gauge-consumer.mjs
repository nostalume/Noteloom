import {
  addPolynomial,
  composeWithRules,
  enumerateWordsWithRules,
  polynomial,
  polynomialEqual,
  polynomialText,
  rat,
  scalePolynomial,
  solveMap,
} from '../10c-generative-residual-constructor/residual-constructor.mjs';

const ONE = rat(1);
const MINUS_ONE = rat(-1);

function refuse(phase, reason, details = {}) {
  return { ok: false, phase, reason, ...details };
}

function constructGaugeWaveFactorization({
  grammarPacket,
  maxWordLength = 2,
  maxTraceDepth = 0,
} = {}) {
  if (!grammarPacket?.ok) {
    return refuse(
      'grammar-input',
      'a successfully compiled natural-operation grammar is required',
    );
  }
  const grammar = grammarPacket.grammar;
  const rules = grammarPacket.pairRules;
  const waveToken = grammarPacket.roles?.waveScalar;
  const gaugeToken = grammarPacket.roles?.momentumRaise;
  const contractionToken = grammarPacket.roles?.momentumContract;
  const missingRoles = [waveToken, gaugeToken, contractionToken]
    .map((token, index) => token ?? ['waveScalar', 'momentumRaise', 'momentumContract'][index])
    .filter((token) => !grammar[token]);
  if (missingRoles.length > 0) {
    return refuse(
      'grammar-capability',
      'the compiled grammar lacks the wave/gauge/contraction roles required by this consumer',
      { missingRoles },
    );
  }

  const compose = (left, right) => composeWithRules(left, right, rules);
  const R = polynomial([[[gaugeToken], ONE]]);
  const wave = polynomial([[[waveToken], ONE]]);
  const equationWords = enumerateWordsWithRules({
    grammar,
    rules,
    momentumDegree: 2,
    rankShift: 0,
    maxTraceDepth,
    maxWordLength,
  });
  const seedIndex = equationWords.findIndex((word) => word.length === 1
    && word[0] === waveToken);
  if (seedIndex < 0) {
    return refuse('wave-seed', 'the compiled grammar did not enumerate its wave scalar');
  }
  const correctionWords = equationWords.filter((_, index) => index !== seedIndex);
  const seedResidual = compose(wave, R);
  const equationRepair = solveMap(
    correctionWords,
    (candidate) => compose(candidate, R),
    scalePolynomial(MINUS_ONE, seedResidual),
  );
  if (!equationRepair.ok) {
    return refuse(
      'gauge-residual',
      'no equation in the compiled bounded span cancels the wave-seed gauge residual',
      { seed: waveToken, ...equationRepair },
    );
  }
  const D = addPolynomial(wave, equationRepair.generated);

  const defectWords = enumerateWordsWithRules({
    grammar,
    rules,
    momentumDegree: 1,
    rankShift: -1,
    maxTraceDepth,
    maxWordLength,
  });
  const factorTarget = addPolynomial(wave, scalePolynomial(MINUS_ONE, D));
  const defect = solveMap(
    defectWords,
    (candidate) => compose(R, candidate),
    factorTarget,
  );
  if (!defect.ok) {
    return refuse(
      'wave-factorization',
      'the generated gauge-invariant equation does not factor the wave scalar through the gauge map inside the admitted span',
      defect,
    );
  }
  const C = defect.generated;
  const certificates = {
    gaugeIdentity: compose(D, R).size === 0,
    waveFactorization: polynomialEqual(addPolynomial(D, compose(R, C)), wave),
  };
  if (Object.values(certificates).some((value) => !value)) {
    throw new Error(`gauge-wave consumer certificate failed: ${JSON.stringify(certificates)}`);
  }

  return {
    ok: true,
    capability: 'gauge-invariant wave factorization in a compiled natural-operation grammar',
    grammarProvenance: grammarPacket.provenance,
    search: {
      equationBasis: equationWords.map((word) => word.join(' ')),
      equationRepairCoefficients: equationRepair.coefficients,
      defectBasis: defect.basis,
      defectCoefficients: defect.coefficients,
    },
    system: {
      R: polynomialText(R),
      C: polynomialText(C),
      D: polynomialText(D),
      wave: polynomialText(wave),
    },
    certificates,
    boundary: 'this consumer constructs a symbol factorization; physical cohomology, support, and action remain separate capabilities',
  };
}

export { constructGaugeWaveFactorization };

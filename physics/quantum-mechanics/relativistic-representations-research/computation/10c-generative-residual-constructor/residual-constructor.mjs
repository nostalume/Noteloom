const primitiveGrammar = Object.freeze({
  Q: { momentumDegree: 2, rankShift: 0, traceDepth: 0 },
  P: { momentumDegree: 1, rankShift: 1, traceDepth: 0 },
  A: { momentumDegree: 1, rankShift: -1, traceDepth: 0 },
  T: { momentumDegree: 0, rankShift: -2, traceDepth: 1 },
});

const fermionicGrammar = Object.freeze({
  Q: { momentumDegree: 2, rankShift: 0, traceDepth: 0 },
  L: { momentumDegree: 1, rankShift: 0, traceDepth: 0 },
  P: { momentumDegree: 1, rankShift: 1, traceDepth: 0 },
  A: { momentumDegree: 1, rankShift: -1, traceDepth: 0 },
  G: { momentumDegree: 0, rankShift: -1, traceDepth: 1 },
});

function gcd(left, right) {
  let a = left < 0n ? -left : left;
  let b = right < 0n ? -right : right;
  while (b !== 0n) [a, b] = [b, a % b];
  return a;
}

function rat(numerator, denominator = 1n) {
  let n = typeof numerator === 'bigint' ? numerator : BigInt(numerator);
  let d = typeof denominator === 'bigint' ? denominator : BigInt(denominator);
  if (d === 0n) throw new Error('zero rational denominator');
  if (d < 0n) [n, d] = [-n, -d];
  const divisor = gcd(n, d);
  return { n: n / divisor, d: d / divisor };
}

const ZERO = rat(0);
const ONE = rat(1);

const bosonicPairRules = new Map([
  ['A P', [[['P', 'A'], ONE], [['Q'], ONE]]],
  ['T P', [[['P', 'T'], ONE], [['A'], rat(2)]]],
  ['T A', [[['A', 'T'], ONE]]],
]);

function addRat(left, right) {
  return rat(left.n * right.d + right.n * left.d, left.d * right.d);
}

function multiplyRat(left, right) {
  return rat(left.n * right.n, left.d * right.d);
}

function negateRat(value) {
  return rat(-value.n, value.d);
}

function divideRat(left, right) {
  return rat(left.n * right.d, left.d * right.n);
}

function isZero(value) {
  return value.n === 0n;
}

function equalRat(left, right) {
  return left.n === right.n && left.d === right.d;
}

function ratText(value) {
  return value.d === 1n ? `${value.n}` : `${value.n}/${value.d}`;
}

function wordKey(word) {
  return word.length === 0 ? 'I' : word.join(' ');
}

function keyWord(key) {
  return key === 'I' ? [] : key.split(' ');
}

function polynomial(entries = []) {
  const out = new Map();
  for (const [word, coefficient] of entries) addTerm(out, word, coefficient);
  return out;
}

function addTerm(target, word, coefficient) {
  if (isZero(coefficient)) return;
  const key = wordKey(word);
  const value = addRat(target.get(key) ?? ZERO, coefficient);
  if (isZero(value)) target.delete(key);
  else target.set(key, value);
}

function addPolynomial(...polynomials) {
  const out = new Map();
  for (const source of polynomials) {
    for (const [key, coefficient] of source) addTerm(out, keyWord(key), coefficient);
  }
  return out;
}

function scalePolynomial(coefficient, source) {
  const out = new Map();
  for (const [key, value] of source) addTerm(out, keyWord(key), multiplyRat(coefficient, value));
  return out;
}

function rewriteWord(word, coefficient, assumptions, output) {
  for (let index = 0; index + 1 < word.length; index += 1) {
    const left = word[index];
    const right = word[index + 1];

    if (right === 'Q' && left !== 'Q') {
      const moved = [...word];
      [moved[index], moved[index + 1]] = [right, left];
      rewriteWord(moved, coefficient, assumptions, output);
      return;
    }

    if (left === 'A' && right === 'P') {
      const ordered = [...word.slice(0, index), 'P', 'A', ...word.slice(index + 2)];
      const commutator = [...word.slice(0, index), 'Q', ...word.slice(index + 2)];
      rewriteWord(ordered, coefficient, assumptions, output);
      rewriteWord(commutator, coefficient, assumptions, output);
      return;
    }

    if (left === 'T' && right === 'P') {
      const ordered = [...word.slice(0, index), 'P', 'T', ...word.slice(index + 2)];
      const commutator = [...word.slice(0, index), 'A', ...word.slice(index + 2)];
      rewriteWord(ordered, coefficient, assumptions, output);
      rewriteWord(commutator, multiplyRat(rat(2), coefficient), assumptions, output);
      return;
    }

    if (left === 'T' && right === 'A') {
      const moved = [...word];
      [moved[index], moved[index + 1]] = [right, left];
      rewriteWord(moved, coefficient, assumptions, output);
      return;
    }
  }

  if ((assumptions.tracelessInput && word.at(-1) === 'T')
      || (assumptions.annihilator && word.at(-1) === assumptions.annihilator)) return;
  addTerm(output, word, coefficient);
}

function normalize(source, assumptions = {}) {
  const out = new Map();
  for (const [key, coefficient] of source) {
    rewriteWord(keyWord(key), coefficient, assumptions, out);
  }
  return out;
}

const fermionicPairRules = new Map([
  ['G P', [[['P', 'G'], ONE], [['L'], ONE]]],
  ['G L', [[['L', 'G'], rat(-1)], [['A'], rat(2)]]],
  ['G A', [[['A', 'G'], ONE]]],
  ['A P', [[['P', 'A'], ONE], [['Q'], ONE]]],
  ['P L', [[['L', 'P'], ONE]]],
  ['A L', [[['L', 'A'], ONE]]],
  ['L L', [[['Q'], ONE]]],
]);

function rewriteWithRules(word, coefficient, rules, assumptions, output) {
  for (let index = 0; index + 1 < word.length; index += 1) {
    const left = word[index];
    const right = word[index + 1];
    if (right === 'Q' && left !== 'Q') {
      const moved = [...word];
      [moved[index], moved[index + 1]] = [right, left];
      rewriteWithRules(moved, coefficient, rules, assumptions, output);
      return;
    }
    const replacements = rules.get(`${left} ${right}`);
    if (!replacements) continue;
    for (const [replacement, factor] of replacements) {
      rewriteWithRules(
        [...word.slice(0, index), ...replacement, ...word.slice(index + 2)],
        multiplyRat(coefficient, factor),
        rules,
        assumptions,
        output,
      );
    }
    return;
  }
  if (assumptions.annihilator && word.at(-1) === assumptions.annihilator) return;
  addTerm(output, word, coefficient);
}

function normalizeWithRules(source, rules, assumptions = {}) {
  const out = new Map();
  for (const [key, coefficient] of source) {
    rewriteWithRules(keyWord(key), coefficient, rules, assumptions, out);
  }
  return out;
}

function composeWithRules(left, right, rules, assumptions = {}) {
  const raw = new Map();
  for (const [leftKey, leftCoefficient] of left) {
    for (const [rightKey, rightCoefficient] of right) {
      addTerm(raw, [...keyWord(leftKey), ...keyWord(rightKey)],
        multiplyRat(leftCoefficient, rightCoefficient));
    }
  }
  return normalizeWithRules(raw, rules, assumptions);
}

function compose(left, right, assumptions = {}) {
  const raw = new Map();
  for (const [leftKey, leftCoefficient] of left) {
    for (const [rightKey, rightCoefficient] of right) {
      addTerm(raw, [...keyWord(leftKey), ...keyWord(rightKey)],
        multiplyRat(leftCoefficient, rightCoefficient));
    }
  }
  return normalize(raw, assumptions);
}

function polynomialEqual(left, right) {
  const difference = addPolynomial(left, scalePolynomial(rat(-1), right));
  return difference.size === 0;
}

function power(token, exponent) {
  return polynomial([[Array.from({ length: exponent }, () => token), ONE]]);
}

function polynomialText(source) {
  if (source.size === 0) return '0';
  const entries = [...source.entries()].sort(([left], [right]) => left.localeCompare(right));
  return entries.map(([key, coefficient], index) => {
    const negative = coefficient.n < 0n;
    const magnitude = rat(negative ? -coefficient.n : coefficient.n, coefficient.d);
    const factor = equalRat(magnitude, ONE) && key !== 'I' ? '' : `${ratText(magnitude)} `;
    const term = `${factor}${key}`.trim();
    if (index === 0) return negative ? `-${term}` : term;
    return `${negative ? '-' : '+'} ${term}`;
  }).join(' ');
}

function enumerateTypedWords({
  grammar,
  normalizer,
  momentumDegree,
  rankShift,
  maxTraceDepth,
  maxWordLength,
}) {
  const tokens = Object.keys(grammar);
  const found = new Set();

  function visit(word, degree, shift, traceDepth) {
    if (word.length > 0 && degree === momentumDegree && shift === rankShift) {
      const normalized = normalizer(polynomial([[word, ONE]]));
      for (const key of normalized.keys()) found.add(key);
    }
    if (word.length === maxWordLength || degree >= momentumDegree) return;
    for (const token of tokens) {
      const primitive = grammar[token];
      const nextDegree = degree + primitive.momentumDegree;
      const nextTrace = traceDepth + primitive.traceDepth;
      if (nextDegree > momentumDegree || nextTrace > maxTraceDepth) continue;
      visit([...word, token], nextDegree, shift + primitive.rankShift, nextTrace);
    }
  }

  visit([], 0, 0, 0);
  return [...found]
    .map(keyWord)
    .filter((word) => {
      const totals = word.reduce((state, token) => ({
        momentumDegree: state.momentumDegree + grammar[token].momentumDegree,
        rankShift: state.rankShift + grammar[token].rankShift,
        traceDepth: state.traceDepth + grammar[token].traceDepth,
      }), { momentumDegree: 0, rankShift: 0, traceDepth: 0 });
      return totals.momentumDegree === momentumDegree
        && totals.rankShift === rankShift
        && totals.traceDepth <= maxTraceDepth;
    })
    .sort((left, right) => left.length - right.length || wordKey(left).localeCompare(wordKey(right)));
}

function enumerateWords(options) {
  return enumerateTypedWords({
    ...options,
    grammar: primitiveGrammar,
    normalizer: (source) => normalize(source),
  });
}

function enumerateWordsWithRules({ grammar, rules, ...options }) {
  return enumerateTypedWords({
    ...options,
    grammar,
    normalizer: (source) => normalizeWithRules(source, rules),
  });
}

function solveLinear(matrix, target) {
  if (matrix.length === 0) return target.every(isZero) ? [] : null;
  const columns = matrix[0]?.length ?? 0;
  const work = matrix.map((row, index) => [...row, target[index]]);
  const pivots = [];
  let pivotRow = 0;

  for (let column = 0; column < columns && pivotRow < work.length; column += 1) {
    let pivot = pivotRow;
    while (pivot < work.length && isZero(work[pivot][column])) pivot += 1;
    if (pivot === work.length) continue;
    [work[pivotRow], work[pivot]] = [work[pivot], work[pivotRow]];
    const divisor = work[pivotRow][column];
    work[pivotRow] = work[pivotRow].map((value) => divideRat(value, divisor));
    for (let row = 0; row < work.length; row += 1) {
      if (row === pivotRow || isZero(work[row][column])) continue;
      const factor = work[row][column];
      work[row] = work[row].map((value, index) =>
        addRat(value, negateRat(multiplyRat(factor, work[pivotRow][index]))));
    }
    pivots.push(column);
    pivotRow += 1;
  }

  for (const row of work) {
    if (row.slice(0, columns).every(isZero) && !isZero(row[columns])) return null;
  }

  const solution = Array.from({ length: columns }, () => ZERO);
  pivots.forEach((column, row) => { solution[column] = work[row][columns]; });
  return solution;
}

function coefficientSystem(images, target) {
  const channels = [...new Set([
    ...images.flatMap((image) => [...image.keys()]),
    ...target.keys(),
  ])].sort();
  const matrix = channels.map((channel) => images.map((image) => image.get(channel) ?? ZERO));
  const right = channels.map((channel) => target.get(channel) ?? ZERO);
  return { channels, matrix, right };
}

function solveMap(words, imageOf, target) {
  const basis = words.map((word) => polynomial([[word, ONE]]));
  const images = basis.map(imageOf);
  const system = coefficientSystem(images, target);
  const coefficients = solveLinear(system.matrix, system.right);
  if (coefficients === null) {
    return {
      ok: false,
      basis: words.map(wordKey),
      residualChannels: system.channels,
      reason: 'the admitted natural-map span cannot cancel every residual channel',
    };
  }
  const generated = addPolynomial(...basis.map((term, index) =>
    scalePolynomial(coefficients[index], term)));
  return {
    ok: true,
    basis: words.map(wordKey),
    coefficients: coefficients.map(ratText),
    generated,
  };
}

function constructBosonicFieldSystem({
  maxTraceDepth = 1,
  maxFieldConstraintDepth = 2,
  grammarPacket,
} = {}) {
  const activeGrammar = grammarPacket?.grammar ?? primitiveGrammar;
  const activeRules = grammarPacket?.pairRules ?? bosonicPairRules;
  const requiredTokens = ['Q', 'P', 'A', 'T'];
  const missingTokens = requiredTokens.filter((token) => !activeGrammar[token]);
  if (missingTokens.length > 0) return {
    ok: false,
    phase: 'carrier-grammar-input',
    reason: 'the supplied carrier grammar lacks operations required by the bosonic residual capability',
    missingTokens,
  };
  const composeActive = (left, right, assumptions = {}) =>
    composeWithRules(left, right, activeRules, assumptions);
  const normalizeActive = (source, assumptions = {}) =>
    normalizeWithRules(source, activeRules, assumptions);
  const enumerateActive = (options) => enumerateWordsWithRules({
    grammar: activeGrammar,
    rules: activeRules,
    ...options,
  });
  const R = polynomial([[['P'], ONE]]);
  const wave = polynomial([[['Q'], ONE]]);

  const defectWords = enumerateActive({
    momentumDegree: 1,
    rankShift: -1,
    maxTraceDepth,
    maxWordLength: 2,
  });
  const solveDefect = (assumptions) => solveMap(
    defectWords, (candidate) => composeActive(candidate, R, assumptions), wave,
  );
  const unconstrainedDefect = solveDefect({});
  let parameterConstraint = null;
  let parameterAssumptions = {};
  let defect = unconstrainedDefect;
  if (!defect.ok && maxTraceDepth >= 1) {
    parameterConstraint = polynomial([[['T'], ONE]]);
    parameterAssumptions = { annihilator: 'T' };
    defect = solveDefect(parameterAssumptions);
  }
  if (!defect.ok) return {
    ok: false,
    phase: 'defect-map',
    unconstrainedObstruction: unconstrainedDefect,
    ...defect,
  };

  let fieldConstraint = null;
  for (let depth = 1; depth <= maxFieldConstraintDepth; depth += 1) {
    const candidate = power('T', depth);
    if (composeActive(candidate, R, parameterAssumptions).size === 0) {
      fieldConstraint = candidate;
      break;
    }
  }
  if (fieldConstraint === null) return {
    ok: false,
    phase: 'field-carrier',
    reason: 'no admitted trace depth is preserved by the generated gauge map',
    maxFieldConstraintDepth,
  };

  const C = defect.generated;
  const DFromDefect = normalizeActive(addPolynomial(wave,
    scalePolynomial(rat(-1), composeActive(R, C))));

  const equationWords = enumerateActive({
    momentumDegree: 2,
    rankShift: 0,
    maxTraceDepth,
    maxWordLength: 3,
  });
  const seedIndex = equationWords.findIndex((word) => wordKey(word) === 'Q');
  if (seedIndex < 0) throw new Error('the scalar wave seed is absent from the grammar');
  const seed = polynomial([[equationWords[seedIndex], ONE]]);
  const correctionWords = equationWords.filter((_, index) => index !== seedIndex);
  const seedResidual = composeActive(seed, R, parameterAssumptions);
  const direct = solveMap(
    correctionWords,
    (candidate) => composeActive(candidate, R, parameterAssumptions),
    scalePolynomial(rat(-1), seedResidual),
  );
  if (!direct.ok) return {
    ok: false,
    phase: 'equation-residual',
    seed: polynomialText(seed),
    ...direct,
  };
  const DDirect = normalizeActive(addPolynomial(seed, direct.generated));

  const certificates = {
    defectIdentity: polynomialEqual(composeActive(C, R, parameterAssumptions), wave),
    directGaugeIdentity: composeActive(DDirect, R, parameterAssumptions).size === 0,
    factorizedGaugeIdentity: composeActive(DFromDefect, R, parameterAssumptions).size === 0,
    constructionCoincidence: polynomialEqual(DDirect, DFromDefect),
    hyperbolicFactorization: polynomialEqual(
      addPolynomial(DFromDefect, composeActive(R, C)), wave),
  };

  if (Object.values(certificates).some((value) => !value)) {
    throw new Error(`internal construction certificate failed: ${JSON.stringify(certificates)}`);
  }

  return {
    ok: true,
    capability: 'constrained free local realization with scalar-wave completion',
    budget: {
      maxTraceDepth, maxFieldConstraintDepth, maxMomentumDegree: 2, auxiliaryCarriers: 0,
    },
    assumptions: ['symmetric potential carrier', 'no auxiliary carrier'],
    generatedConstraints: {
      parameter: polynomialText(parameterConstraint),
      field: polynomialText(fieldConstraint),
    },
    grammar: activeGrammar,
    grammarProvenance: grammarPacket?.provenance ?? 'legacy built-in symmetric-carrier grammar',
    search: {
      defectBasis: defect.basis,
      defectCoefficients: defect.coefficients,
      unconstrainedDefectObstruction: unconstrainedDefect.ok ? null : unconstrainedDefect,
      equationBasis: ['Q', ...direct.basis],
      equationCoefficients: ['1', ...direct.coefficients],
    },
    fieldSystem: { R, C, D: DFromDefect, wave, parameterConstraint, fieldConstraint },
    certificates,
    responseInterface: {
      input: 'source S satisfying C S = 0',
      operation: 'phi = G_Q S',
      output: 'D phi = S',
      witness: 'D G_Q S = (Q - R C) G_Q S = S - R G_Q C S = S',
    },
  };
}

function constructFermionicLocalComplex({
  maxGammaDepth = 1,
  maxFieldConstraintDepth = 3,
  grammarPacket,
} = {}) {
  const activeGrammar = grammarPacket?.grammar ?? fermionicGrammar;
  const activeRules = grammarPacket?.pairRules ?? fermionicPairRules;
  const requiredTokens = ['Q', 'L', 'P', 'A', 'G'];
  const missingTokens = requiredTokens.filter((token) => !activeGrammar[token]);
  if (missingTokens.length > 0) return {
    ok: false,
    phase: 'carrier-grammar-input',
    reason: 'the supplied carrier grammar lacks operations required by the Clifford residual capability',
    missingTokens,
  };
  const R = polynomial([[['P'], ONE]]);
  const seed = polynomial([[['L'], ONE]]);
  const equationWords = enumerateWordsWithRules({
    grammar: activeGrammar,
    rules: activeRules,
    momentumDegree: 1,
    rankShift: 0,
    maxTraceDepth: maxGammaDepth,
    maxWordLength: 2,
  });
  const correctionWords = equationWords.filter((word) => wordKey(word) !== 'L');
  const solveEquation = (assumptions) => {
    const seedResidual = composeWithRules(seed, R, activeRules, assumptions);
    return solveMap(
      correctionWords,
      (candidate) => composeWithRules(candidate, R, activeRules, assumptions),
      scalePolynomial(rat(-1), seedResidual),
    );
  };
  const unconstrainedEquation = solveEquation({});
  let parameterConstraint = null;
  let parameterAssumptions = {};
  let solved = unconstrainedEquation;
  if (!solved.ok && maxGammaDepth >= 1) {
    parameterConstraint = polynomial([[['G'], ONE]]);
    parameterAssumptions = { annihilator: 'G' };
    solved = solveEquation(parameterAssumptions);
  }
  if (!solved.ok) return {
    ok: false,
    phase: 'fermionic-equation-residual',
    seed: 'L',
    unconstrainedObstruction: unconstrainedEquation,
    ...solved,
  };

  const S = normalizeWithRules(addPolynomial(seed, solved.generated), activeRules);
  let fieldConstraint = null;
  for (let depth = 1; depth <= maxFieldConstraintDepth; depth += 1) {
    const candidate = power('G', depth);
    if (composeWithRules(candidate, R, activeRules, parameterAssumptions).size === 0) {
      fieldConstraint = candidate;
      break;
    }
  }
  if (fieldConstraint === null) return {
    ok: false,
    phase: 'fermionic-field-carrier',
    reason: 'no admitted gamma depth is preserved by the generated gauge map',
    maxFieldConstraintDepth,
  };
  const certificates = {
    gaugeIdentity: composeWithRules(S, R, activeRules, parameterAssumptions).size === 0,
    carrierPreservation: composeWithRules(
      fieldConstraint, R, activeRules, parameterAssumptions,
    ).size === 0,
  };
  if (Object.values(certificates).some((value) => !value)) {
    throw new Error(`fermionic construction certificate failed: ${JSON.stringify(certificates)}`);
  }

  return {
    ok: true,
    capability: 'constrained half-integer local equation complex',
    budget: {
      maxGammaDepth, maxFieldConstraintDepth, maxMomentumDegree: 1, auxiliaryCarriers: 0,
    },
    assumptions: ['symmetric spinor-tensor carrier', 'no auxiliary carrier'],
    generatedConstraints: {
      parameter: polynomialText(parameterConstraint),
      field: polynomialText(fieldConstraint),
    },
    grammar: activeGrammar,
    grammarProvenance: grammarPacket?.provenance ?? 'legacy built-in symmetric spinor-carrier grammar',
    search: {
      equationBasis: ['L', ...solved.basis],
      equationCoefficients: ['1', ...solved.coefficients],
      unconstrainedEquationObstruction: unconstrainedEquation.ok ? null : unconstrainedEquation,
    },
    localComplex: { R, S, parameterConstraint, fieldConstraint },
    certificates,
  };
}

function serializableResult(result) {
  if (!result.ok) return result;
  if (result.localComplex) {
    return {
      ...result,
      localComplex: Object.fromEntries(Object.entries(result.localComplex)
        .map(([name, value]) => [name, polynomialText(value)])),
    };
  }
  return {
    ...result,
    fieldSystem: Object.fromEntries(Object.entries(result.fieldSystem)
      .map(([name, value]) => [name, polynomialText(value)])),
  };
}

export {
  addPolynomial,
  addRat,
  bosonicPairRules,
  compose,
  composeWithRules,
  coefficientSystem,
  constructBosonicFieldSystem,
  constructFermionicLocalComplex,
  divideRat,
  enumerateWords,
  enumerateWordsWithRules,
  fermionicGrammar,
  fermionicPairRules,
  isZero,
  keyWord,
  multiplyRat,
  negateRat,
  normalize,
  normalizeWithRules,
  polynomial,
  polynomialEqual,
  polynomialText,
  primitiveGrammar,
  rat,
  ratText,
  scalePolynomial,
  serializableResult,
  solveLinear,
  solveMap,
};

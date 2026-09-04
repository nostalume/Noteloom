import {
  addPolynomial,
  addRat,
  constructFermionicLocalComplex,
  divideRat,
  isZero,
  multiplyRat,
  polynomial,
  polynomialEqual,
  polynomialText,
  rat,
  scalePolynomial,
  solveMap,
} from '../10c-generative-residual-constructor/residual-constructor.mjs';

const ZERO = rat(0);
const ONE = rat(1);

const defaultCliffordTransferRules = new Map([
  ['P Y', [[['Y', 'P'], ONE]]],
  ['L Y', [[['Y', 'L'], rat(-1)], [['P'], rat(2)]]],
  ['A Y', [[['Y', 'A'], ONE], [['L'], ONE]]],
  ['G P', [[['P', 'G'], ONE], [['L'], ONE]]],
  ['G L', [[['L', 'G'], rat(-1)], [['A'], rat(2)]]],
  ['G A', [[['A', 'G'], ONE]]],
  ['A P', [[['P', 'A'], ONE], [['Q'], ONE]]],
  ['L P', [[['P', 'L'], ONE]]],
  ['A L', [[['L', 'A'], ONE]]],
  ['L L', [[['Q'], ONE]]],
]);

function wordOf(key) {
  return key === 'I' ? [] : key.split(' ');
}

function keyOf(word) {
  return word.length === 0 ? 'I' : word.join(' ');
}

function addWord(target, word, coefficient) {
  if (isZero(coefficient)) return;
  const key = keyOf(word);
  const next = addRat(target.get(key) ?? ZERO, coefficient);
  if (isZero(next)) target.delete(key);
  else target.set(key, next);
}

// Canonical order is Q, Y, P, L, A, G. The rules may now be supplied by the
// carrier-to-grammar constructor; the local default preserves the old API.
function rewriteWord(word, coefficient, output, rules) {
  for (let index = 0; index + 1 < word.length; index += 1) {
    const left = word[index];
    const right = word[index + 1];
    const before = word.slice(0, index);
    const after = word.slice(index + 2);

    if (right === 'Q' && left !== 'Q') {
      rewriteWord([...before, 'Q', left, ...after], coefficient, output, rules);
      return;
    }
    const replacements = rules.get(`${left} ${right}`);
    if (!replacements) continue;
    for (const [replacement, factor] of replacements) {
      rewriteWord(
        [...before, ...replacement, ...after],
        multiplyRat(coefficient, factor),
        output,
        rules,
      );
    }
    return;
  }
  addWord(output, word, coefficient);
}

function normalizeClifford(source, rules = defaultCliffordTransferRules) {
  const output = new Map();
  for (const [key, coefficient] of source) {
    rewriteWord(wordOf(key), coefficient, output, rules);
  }
  return output;
}

function composeClifford(left, right, rules = defaultCliffordTransferRules) {
  const raw = new Map();
  for (const [leftKey, leftCoefficient] of left) {
    for (const [rightKey, rightCoefficient] of right) {
      addWord(raw, [...wordOf(leftKey), ...wordOf(rightKey)],
        multiplyRat(leftCoefficient, rightCoefficient));
    }
  }
  return normalizeClifford(raw, rules);
}

const adjointToken = Object.freeze({ Q: 'Q', P: 'A', A: 'P', L: 'L', G: 'Y', Y: 'G' });

function adjointClifford(source, rules = defaultCliffordTransferRules) {
  const raw = new Map();
  for (const [key, coefficient] of source) {
    const word = wordOf(key).reverse().map((token) => adjointToken[token]);
    if (word.some((token) => token === undefined)) {
      throw new Error(`no adjoint rule for ${key}`);
    }
    addWord(raw, word, coefficient);
  }
  return normalizeClifford(raw, rules);
}

function quotientPolynomial(source, isNullWord) {
  return polynomial([...source.entries()]
    .filter(([key]) => !isNullWord(wordOf(key)))
    .map(([key, coefficient]) => [wordOf(key), coefficient]));
}

function sourcePairingQuotient(source) {
  // A leading Y moves to Gamma on the gamma-traceless gauge parameter.
  return quotientPolynomial(source, (word) => word[0] === 'Y');
}

function fieldPairingQuotient(source) {
  // The two slots of the pairing satisfy Gamma^3=0.
  return quotientPolynomial(source, (word) =>
    (word.length >= 3 && word.slice(0, 3).every((token) => token === 'Y'))
      || (word.length >= 3 && word.slice(-3).every((token) => token === 'G')));
}

function adapterWords(maxGammaLayers) {
  const words = [[]];
  if (maxGammaLayers >= 1) words.push(['Y', 'G']);
  if (maxGammaLayers >= 2) words.push(['Y', 'Y', 'G', 'G']);
  return words;
}

function generateCompletion(S, rules = defaultCliffordTransferRules) {
  const Q = polynomial([[['Q'], ONE]]);
  const residual = normalizeClifford(addPolynomial(Q,
    scalePolynomial(rat(-1), composeClifford(S, S, rules))), rules);
  const stripped = new Map();
  for (const [key, coefficient] of residual) {
    const word = wordOf(key);
    if (word[0] !== 'P') {
      return {
        ok: false,
        phase: 'clifford-wave-completion',
        reason: 'the wave residual does not factor through the generated gauge map P',
        residual: polynomialText(residual),
      };
    }
    addWord(stripped, word.slice(1), coefficient);
  }
  const head = stripped.get('A');
  if (!head || isZero(head)) {
    return {
      ok: false,
      phase: 'clifford-wave-completion',
      reason: 'the factored residual has no contraction head with which to normalize B',
      residual: polynomialText(residual),
    };
  }
  const B = scalePolynomial(divideRat(ONE, head), stripped);
  const completionCoefficient = head;
  const completion = normalizeClifford(addPolynomial(
    composeClifford(S, S, rules),
    scalePolynomial(completionCoefficient,
      composeClifford(polynomial([[['P'], ONE]]), B, rules)),
  ), rules);
  return {
    ok: polynomialEqual(completion, Q),
    residual,
    completionCoefficient,
    B,
    certificate: polynomialEqual(completion, Q),
  };
}

function solveSourceRoute(B, maxGammaLayers, rules = defaultCliffordTransferRules) {
  const A = polynomial([[['A'], ONE]]);
  const words = adapterWords(maxGammaLayers);
  const solved = solveMap(
    words,
    (candidate) => sourcePairingQuotient(composeClifford(A, candidate, rules)),
    sourcePairingQuotient(B),
  );
  if (!solved.ok) return {
    ok: false,
    phase: 'clifford-source-adjoint-residual',
    capability: 'convert constrained source conservation into the generated wave-completion condition',
    maxGammaLayers,
    ...solved,
  };
  const ambientResidual = normalizeClifford(addPolynomial(
    composeClifford(A, solved.generated, rules),
    scalePolynomial(rat(-1), B),
  ), rules);
  return { ok: true, adapter: solved.generated, ambientResidual, solved };
}

function adjointDefect(multiplier, S, rules = defaultCliffordTransferRules) {
  return normalizeClifford(addPolynomial(
    composeClifford(multiplier, S, rules),
    scalePolynomial(rat(-1), composeClifford(adjointClifford(S, rules), multiplier, rules)),
  ), rules);
}

function solveEulerRoute(S, maxGammaLayers, rules = defaultCliffordTransferRules) {
  const identity = polynomial([[[], ONE]]);
  const seedResidual = fieldPairingQuotient(adjointDefect(identity, S, rules));
  const correctionWords = adapterWords(maxGammaLayers).slice(1);
  const solved = solveMap(
    correctionWords,
    (candidate) => fieldPairingQuotient(adjointDefect(candidate, S, rules)),
    scalePolynomial(rat(-1), seedResidual),
  );
  if (!solved.ok) return {
    ok: false,
    phase: 'clifford-euler-adjoint-residual',
    capability: 'construct an equation-equivalent restricted-self-adjoint Clifford Euler operator',
    maxGammaLayers,
    seed: 'S',
    seedResidual: polynomialText(seedResidual),
    ...solved,
  };
  const multiplier = addPolynomial(identity, solved.generated);
  return {
    ok: true,
    multiplier,
    ambientResidual: adjointDefect(multiplier, S, rules),
    solved,
  };
}

function constructCliffordSourceEulerTransfer({
  localComplexResult,
  maxGammaLayers = 2,
  carrierGrammarPacket,
} = {}) {
  const generated = localComplexResult ?? constructFermionicLocalComplex({
    maxGammaDepth: 1,
    maxFieldConstraintDepth: 3,
  });
  if (!generated.ok) return {
    ok: false,
    phase: 'upstream-clifford-complex',
    reason: 'the residual constructor did not return a supported Clifford complex',
    upstream: generated,
  };
  if (!Number.isInteger(maxGammaLayers) || maxGammaLayers < 0 || maxGammaLayers > 2) {
    return {
      ok: false,
      phase: 'clifford-transfer-budget',
      reason: 'the triple-gamma carrier admits the bounded layers I, Y G, and Y^2 G^2',
      maxGammaLayers,
    };
  }
  const activeRules = carrierGrammarPacket?.dualityPairRules
    ?? defaultCliffordTransferRules;
  if (carrierGrammarPacket && (!carrierGrammarPacket.dualityGrammar?.Y
      || !carrierGrammarPacket.dualityGrammar?.G)) return {
    ok: false,
    phase: 'carrier-grammar-input',
    reason: 'the Clifford source/Euler capability requires generated gamma trace and insertion operations',
    missingTokens: ['G', 'Y'].filter((token) => !carrierGrammarPacket.dualityGrammar?.[token]),
  };

  const S = normalizeClifford(generated.localComplex.S, activeRules);
  const completion = generateCompletion(S, activeRules);
  if (!completion.ok) return completion;
  const source = solveSourceRoute(completion.B, maxGammaLayers, activeRules);
  if (!source.ok) return source;
  const euler = solveEulerRoute(S, maxGammaLayers, activeRules);
  if (!euler.ok) return euler;

  const sourceOneLayer = solveSourceRoute(completion.B, 1, activeRules);
  const eulerOneLayer = solveEulerRoute(S, 1, activeRules);
  const bianchiResidual = composeClifford(completion.B, S, activeRules);
  const certificates = {
    waveCompletion: completion.certificate,
    independentMultiplierCoincidence: polynomialEqual(source.adapter, euler.multiplier),
    sourceResidualPairingNull: sourcePairingQuotient(source.ambientResidual).size === 0,
    eulerResidualPairingNull: fieldPairingQuotient(euler.ambientResidual).size === 0,
    oneLayerSourceRefusal: !sourceOneLayer.ok,
    oneLayerEulerRefusal: !eulerOneLayer.ok,
    identityNormalization: source.adapter.get('I')?.n === 1n
      && source.adapter.get('I')?.d === 1n,
  };
  if (Object.values(certificates).some((value) => !value)) {
    throw new Error(`Clifford transfer certificate failed: ${JSON.stringify(certificates)}`);
  }

  return {
    ok: true,
    capability: 'generated Clifford source adapter, Euler operator, and scalar-wave response interface',
    budget: { maxGammaLayers, dimension: 4, fieldGammaDepth: 3, auxiliaryCarriers: 0 },
    assumptions: [
      'complex Dirac-Fischer pairing',
      'gamma-traceless gauge parameter',
      'triple-gamma-traceless symmetric spinor-tensor field',
      'compact support or a boundary convention removing surface terms',
    ],
    upstreamLocalComplex: generated.localComplex,
    grammarProvenance: carrierGrammarPacket?.provenance
      ?? 'legacy built-in Clifford duality grammar',
    completion: {
      B: completion.B,
      coefficient: completion.completionCoefficient,
      residual: completion.residual,
      bianchiResidual,
    },
    search: {
      sourceBasis: source.solved.basis,
      sourceCoefficients: source.solved.coefficients,
      eulerBasis: ['I', ...euler.solved.basis],
      eulerCoefficients: ['1', ...euler.solved.coefficients],
      oneLayerSourceRefusal: sourceOneLayer,
      oneLayerEulerRefusal: eulerOneLayer,
    },
    multiplier: source.adapter,
    sourceResidual: source.ambientResidual,
    eulerResidual: euler.ambientResidual,
    certificates,
    inverseInterface: {
      decomposition: 'psi = h_0 + Y h_1 + Y^2 h_2 with Gamma h_j = 0',
      operation: 'M_n^(-1) psi = h_0 - (1/n)(Y h_1 + Y^2 h_2), n >= 1; M_0^(-1)=I',
      eigenvalues: '1 on H_n and -n on Y H_(n-1) plus Y^2 H_(n-2)',
    },
    responseInterface: {
      input: 'compact J satisfying the constrained adjoint condition R^dagger J = 0',
      operation: 'K=M^(-1)J; psi=S G_Q K',
      output: 'B K=0 and E psi=J for E=M S',
      witness: 'S^2+2PB=Q gives S(S G_QK)=K; multiplying by M gives E psi=J',
    },
    actionInterface: {
      eulerOperator: 'E=M S',
      functional: 'I[psi;J]=(1/2)<psi,E psi>-<psi,J>',
      boundary: 'complex sesquilinear formal action; a real Grassmann action requires extra reality data',
    },
  };
}

function serializableCliffordTransfer(result) {
  if (!result.ok) return result;
  const serializeMap = (value) => polynomialText(value);
  return {
    ...result,
    upstreamLocalComplex: Object.fromEntries(Object.entries(result.upstreamLocalComplex)
      .map(([name, value]) => [name, serializeMap(value)])),
    completion: {
      B: serializeMap(result.completion.B),
      coefficient: `${result.completion.coefficient.n}/${result.completion.coefficient.d}`,
      residual: serializeMap(result.completion.residual),
      bianchiResidual: serializeMap(result.completion.bianchiResidual),
    },
    multiplier: serializeMap(result.multiplier),
    sourceResidual: serializeMap(result.sourceResidual),
    eulerResidual: serializeMap(result.eulerResidual),
  };
}

export {
  adjointClifford,
  composeClifford,
  constructCliffordSourceEulerTransfer,
  defaultCliffordTransferRules,
  fieldPairingQuotient,
  generateCompletion,
  normalizeClifford,
  serializableCliffordTransfer,
  sourcePairingQuotient,
};

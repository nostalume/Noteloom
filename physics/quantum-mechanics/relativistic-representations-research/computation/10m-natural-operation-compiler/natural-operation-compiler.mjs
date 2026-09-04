import {
  normalizeWithRules,
  polynomial,
  polynomialEqual,
  rat,
} from '../10c-generative-residual-constructor/residual-constructor.mjs';

const ONE = rat(1);
const TWO = rat(2);
const MINUS_ONE = rat(-1);

const forbiddenAnswerKeys = new Set([
  'grammar',
  'pairRules',
  'dualityGrammar',
  'dualityPairRules',
  'tokens',
  'expectedEquation',
]);

function refuse(phase, reason, details = {}) {
  return { ok: false, phase, reason, ...details };
}

function containsAnswerBearingInput(input) {
  if (!input || typeof input !== 'object') return null;
  for (const key of Object.keys(input)) {
    if (forbiddenAnswerKeys.has(key)) return key;
  }
  return null;
}

function addRule(rules, trace, left, replacements, origin) {
  rules.set(left.join(' '), replacements);
  trace.push({
    left: left.join(' '),
    right: replacements.map(([word, coefficient]) => ({
      word: word.join(' ') || '0',
      coefficient: coefficient.d === 1n
        ? `${coefficient.n}`
        : `${coefficient.n}/${coefficient.d}`,
    })),
    origin,
  });
}

function relation(...terms) {
  return terms;
}

function validateInput(input) {
  const answerKey = containsAnswerBearingInput(input);
  if (answerKey) {
    return refuse(
      'answer-bearing-input',
      'the natural-operation compiler accepts carrier laws and invariants, not a token grammar or expected result',
      { rejectedKey: answerKey },
    );
  }
  const power = input?.carrier?.power;
  if (!power || !['V', 'V*'].includes(power.generator)
      || ![1, -1].includes(power.exchangeSign)) {
    return refuse(
      'carrier-law',
      'a free power carrier requires generator V or V* and exchangeSign +1 or -1',
      { required: ['carrier.power.generator', 'carrier.power.exchangeSign'] },
    );
  }
  const metric = (input.invariants ?? []).find((item) => item.role === 'metric');
  if (!metric?.invariant || !metric?.nondegenerate || metric.rank !== 2
      || metric.exchangeSign !== 1) {
    return refuse(
      'invariant-resource',
      'a nondegenerate invariant symmetric rank-two metric is required to construct momentum contraction and Q',
      { missingResources: ['invariant nondegenerate symmetric metric'] },
    );
  }
  const actions = input.carrier.coefficient?.actions ?? [];
  for (const action of actions) {
    if (action.law !== 'metric-polarized-quadratic-action'
        || action.invariant !== metric.id
        || !action.equivariant
        || action.polarizationCoefficient !== 2) {
      return refuse(
        'coefficient-action-law',
        'the declared coefficient action does not supply an equivariant metric-polarized quadratic law',
        { action },
      );
    }
    if (action.origin?.kind !== 'generated-first-order-factorization') {
      return refuse(
        'coefficient-action-origin',
        'the generative route accepts a coefficient action returned by FirstOrderFactorizer, not a handcrafted quadratic law',
        { suppliedOrigin: action.origin ?? null },
      );
    }
    if (power.exchangeSign !== 1) {
      return refuse(
        'coefficient-action-compatibility',
        'the present slot-action compiler has derived its contraction/insertion laws only for the symmetric power functor',
        { exchangeSign: power.exchangeSign, actionLaw: action.law },
      );
    }
  }
  if (actions.length > 1) {
    return refuse(
      'coefficient-action-budget',
      'the first compiler bench admits at most one quadratic coefficient action',
      { actionCount: actions.length, maximum: 1 },
    );
  }
  return null;
}

function wordOrder(word, tokenOrder) {
  return word.map((token) => tokenOrder.indexOf(token));
}

function lexicographicallyLess(left, right) {
  for (let index = 0; index < Math.min(left.length, right.length); index += 1) {
    if (left[index] !== right[index]) return left[index] < right[index];
  }
  return left.length < right.length;
}

function rulesDecrease(rules, tokenOrder) {
  for (const [leftText, replacements] of rules) {
    const left = leftText.split(' ');
    const leftOrder = wordOrder(left, tokenOrder);
    for (const [right] of replacements) {
      if (right.length < left.length) continue;
      if (right.length > left.length) return false;
      if (!lexicographicallyLess(wordOrder(right, tokenOrder), leftOrder)) return false;
    }
  }
  return true;
}

function relationsClosed(rules, grammar) {
  const tokens = new Set(Object.keys(grammar));
  for (const [left, replacements] of rules) {
    if (left.split(' ').some((token) => !tokens.has(token))) return false;
    for (const [word] of replacements) {
      if (word.some((token) => !tokens.has(token))) return false;
    }
  }
  return true;
}

function enumerateWords(tokens, maximumLength) {
  const words = [[]];
  for (let length = 1; length <= maximumLength; length += 1) {
    const prior = words.filter((word) => word.length === length - 1);
    for (const word of prior) {
      for (const token of tokens) words.push([...word, token]);
    }
  }
  return words;
}

function boundedNormalFormIdempotent(grammar, rules, maximumLength = 3) {
  for (const word of enumerateWords(Object.keys(grammar), maximumLength)) {
    const source = polynomial([[word, ONE]]);
    const once = normalizeWithRules(source, rules);
    const twice = normalizeWithRules(once, rules);
    if (!polynomialEqual(once, twice)) return false;
  }
  return true;
}

function restrictPolynomialToInputRank(source, grammarPacket, inputRank) {
  if (!grammarPacket?.ok) {
    return refuse(
      'rank-specialization-input',
      'a successfully compiled natural-operation grammar is required',
    );
  }
  if (!Number.isInteger(inputRank) || inputRank < 0) {
    return refuse(
      'rank-specialization-boundary',
      'the input carrier rank must be a nonnegative integer',
      { inputRank },
    );
  }

  const retained = new Map();
  const omittedWords = [];
  for (const [key, coefficient] of source) {
    const word = key === 'I' ? [] : key.split(' ');
    let rank = inputRank;
    let obstruction = null;

    // A word XY denotes X after Y, so its rightmost operation acts first.
    for (let index = word.length - 1; index >= 0; index -= 1) {
      const operation = word[index];
      const descriptor = grammarPacket.dualityGrammar?.[operation]
        ?? grammarPacket.grammar?.[operation];
      if (!descriptor) {
        obstruction = `operation ${operation} is absent from the compiled grammar`;
        break;
      }
      rank += descriptor.rankShift;
      if (rank < 0) {
        obstruction = `${operation} would leave the nonnegative free-power tower`;
        break;
      }
    }

    if (obstruction) omittedWords.push({ word: key, obstruction });
    else retained.set(key, coefficient);
  }

  return {
    ok: true,
    inputRank,
    polynomial: retained,
    omittedWords,
    certificate: 'every retained word has a nonnegative rank after each right-to-left operation',
  };
}

function compileNaturalOperations(input = {}) {
  const invalid = validateInput(input);
  if (invalid) return invalid;

  const power = input.carrier.power;
  const metric = input.invariants.find((item) => item.role === 'metric');
  const actions = input.carrier.coefficient?.actions ?? [];
  const sign = power.exchangeSign;
  const grammar = {
    Q: { momentumDegree: 2, rankShift: 0, traceDepth: 0 },
  };
  const constructions = {
    Q: `evaluate the inverse ${metric.id} pairing on momentum twice`,
  };
  const constructionTrace = [{
    operation: 'Q',
    input: `${metric.id} inverse pairing and momentum p`,
    output: 'the quadratic scalar eta^(-1)(p,p)',
  }];

  if (actions.length === 1) {
    grammar.L = { momentumDegree: 1, rankShift: 0, traceDepth: 0 };
    constructions.L = 'evaluate the metric-polarized coefficient action on momentum';
    constructionTrace.push({
      operation: 'L',
      input: 'coefficient action and momentum p',
      output: 'a degree-one coefficient-module endomorphism',
    });
  }

  grammar.P = { momentumDegree: 1, rankShift: 1, traceDepth: 0 };
  grammar.A = { momentumDegree: 1, rankShift: -1, traceDepth: 0 };
  constructions.P = 'multiply by momentum in the declared free power algebra';
  constructions.A = `apply its universal derivation along p sharp from ${metric.id}`;
  constructionTrace.push(
    {
      operation: 'P',
      input: 'free power functor and momentum p',
      output: 'rank-raising multiplication by p',
    },
    {
      operation: 'A',
      input: `universal derivation and ${metric.id} duality`,
      output: 'rank-lowering contraction by p sharp',
    },
  );

  if (actions.length === 1) {
    grammar.G = { momentumDegree: 0, rankShift: -1, traceDepth: 1 };
    constructions.G = 'contract one power slot through the coefficient action';
    constructionTrace.push({
      operation: 'G',
      input: 'universal slot derivation and the coefficient action',
      output: 'rank-lowering coefficient-action contraction',
    });
  }

  const omittedOperations = [];
  const invariantMatchesPower = metric.exchangeSign === sign;
  // In the coefficient-action cell, G is the admitted trace-like operation.
  // Adding T as well would silently enlarge the old Clifford bench beyond the
  // law supplied by the carrier presentation.
  const rankTwoInvariantAdmitted = invariantMatchesPower && actions.length === 0;
  if (rankTwoInvariantAdmitted) {
    grammar.T = { momentumDegree: 0, rankShift: -2, traceDepth: 1 };
    constructions.T = `double contraction by the inverse ${metric.id}`;
    constructionTrace.push({
      operation: 'T',
      input: `rank-two ${metric.id} invariant and two slot derivations`,
      output: 'rank-two trace contraction',
    });
  } else if (!invariantMatchesPower) {
    omittedOperations.push({
      operation: 'metric-rank-two',
      obstruction: [
        `the power projector has exchange sign ${sign}`,
        `${metric.id} has exchange sign ${metric.exchangeSign}`,
        'their rank-two projection is zero',
      ].join('; '),
    });
  } else {
    omittedOperations.push({
      operation: 'metric-rank-two',
      obstruction: 'the coefficient-action capability cell uses G as its admitted trace; an independent T action was not supplied',
    });
  }

  const pairRules = new Map();
  const relationTrace = [];
  addRule(
    pairRules,
    relationTrace,
    ['A', 'P'],
    relation([['P', 'A'], sign === 1 ? ONE : MINUS_ONE], [['Q'], ONE]),
    'evaluate derivation after multiplication on the same power-carrier input',
  );
  if (sign === -1) {
    addRule(
      pairRules,
      relationTrace,
      ['P', 'P'],
      relation(),
      'alternating multiplication by the same momentum has p wedge p=0',
    );
    addRule(
      pairRules,
      relationTrace,
      ['A', 'A'],
      relation(),
      'alternating contraction by the same metric-dual momentum squares to zero',
    );
  }
  if (rankTwoInvariantAdmitted) {
    addRule(
      pairRules,
      relationTrace,
      ['T', 'P'],
      relation([['P', 'T'], ONE], [['A'], TWO]),
      'the two contractions of the rank-two invariant can each hit the inserted momentum',
    );
    addRule(
      pairRules,
      relationTrace,
      ['T', 'A'],
      relation([['A', 'T'], ONE]),
      'constant metric trace commutes with momentum contraction',
    );
  }

  if (actions.length === 1) {
    addRule(pairRules, relationTrace, ['G', 'P'],
      relation([['P', 'G'], ONE], [['L'], ONE]),
      'the slot contraction either reaches the old input or the inserted momentum');
    addRule(pairRules, relationTrace, ['G', 'L'],
      relation([['L', 'G'], MINUS_ONE], [['A'], TWO]),
      'polarize the quadratic coefficient action and then contract the tensor slot');
    addRule(pairRules, relationTrace, ['G', 'A'],
      relation([['A', 'G'], ONE]),
      'the two contractions act on independent structures');
    addRule(pairRules, relationTrace, ['P', 'L'],
      relation([['L', 'P'], ONE]),
      'power multiplication commutes with coefficient evaluation');
    addRule(pairRules, relationTrace, ['A', 'L'],
      relation([['L', 'A'], ONE]),
      'slot contraction commutes with coefficient evaluation');
    addRule(pairRules, relationTrace, ['L', 'L'],
      relation([['Q'], ONE]),
      'evaluate the quadratic coefficient law twice at the same momentum');
  }

  const dualityGrammar = { ...grammar };
  const adjoints = { Q: 'Q', P: 'A', A: 'P' };
  if (rankTwoInvariantAdmitted) {
    dualityGrammar.U = { momentumDegree: 0, rankShift: 2, traceDepth: -1 };
    adjoints.T = 'U';
    adjoints.U = 'T';
    constructions.U = `multiply by the rank-two invariant ${metric.id}`;
  }
  let dualityPairRules;
  if (actions.length === 1) {
    dualityGrammar.Y = { momentumDegree: 0, rankShift: 1, traceDepth: -1 };
    adjoints.L = 'L';
    adjoints.G = 'Y';
    adjoints.Y = 'G';
    constructions.Y = 'insert one power slot through the coefficient action';
    dualityPairRules = new Map(pairRules);
    // The duality/recovery normal form orders P before L, unlike the local
    // residual normal form. Replace, rather than duplicate, that commuting
    // orientation.
    dualityPairRules.delete('P L');
    const dualTrace = [];
    addRule(dualityPairRules, dualTrace, ['L', 'P'],
      relation([['P', 'L'], ONE]),
      'power multiplication commutes with coefficient evaluation');
    addRule(dualityPairRules, dualTrace, ['P', 'Y'],
      relation([['Y', 'P'], ONE]),
      'power multiplication commutes with coefficient insertion');
    addRule(dualityPairRules, dualTrace, ['L', 'Y'],
      relation([['Y', 'L'], MINUS_ONE], [['P'], TWO]),
      'polarize the coefficient action on momentum and the inserted slot');
    addRule(dualityPairRules, dualTrace, ['A', 'Y'],
      relation([['Y', 'A'], ONE], [['L'], ONE]),
      'momentum contraction can hit the inserted coefficient-action slot');
    relationTrace.push(...dualTrace);
  }

  const localTokenOrder = ['Q', 'L', 'P', 'A', 'G', 'T'];
  const dualTokenOrder = ['Q', 'Y', 'P', 'L', 'A', 'G', 'T', 'U'];
  const localClosed = relationsClosed(pairRules, grammar);
  const dualClosed = !dualityPairRules
    || relationsClosed(dualityPairRules, dualityGrammar);
  const localDecreases = rulesDecrease(pairRules, localTokenOrder);
  const dualDecreases = !dualityPairRules
    || rulesDecrease(dualityPairRules, dualTokenOrder);
  const localIdempotent = boundedNormalFormIdempotent(grammar, pairRules);
  const dualIdempotent = !dualityPairRules
    || boundedNormalFormIdempotent(dualityGrammar, dualityPairRules);
  const certificates = {
    relationsClosed: localClosed && dualClosed,
    rewriteOrderDecreases: localDecreases && dualDecreases,
    boundedNormalFormIdempotent: localIdempotent && dualIdempotent,
    bound: { maximumCheckedWordLength: 3 },
  };
  if (Object.entries(certificates)
    .filter(([name]) => name !== 'bound')
    .some(([, value]) => !value)) {
    return refuse(
      'normal-form-certificate',
      'the compiled relation system failed a closure, termination-order, or bounded idempotence certificate',
      { certificates },
    );
  }

  const powerName = sign === 1 ? 'Sym' : 'Lambda';
  const coefficientLabel = input.carrier.coefficient?.label;
  const carrier = `${powerName}^r(${power.generator})${coefficientLabel && coefficientLabel !== '1'
    ? ` tensor ${coefficientLabel}` : ''}`;
  const provenance = [
    `compiled from the free power law with exchange sign ${sign}`,
    `universal multiplication/derivation on ${power.generator}`,
    `invariant metric ${metric.id}`,
    ...(actions.length === 1 ? ['one metric-polarized quadratic coefficient action'] : []),
  ].join(' -> ');

  return {
    ok: true,
    family: 'compiled-free-power-carrier',
    carrier,
    grammar,
    pairRules,
    dualityGrammar,
    ...(dualityPairRules ? { dualityPairRules } : {}),
    adjoints,
    constructions,
    constructionTrace,
    relationTrace,
    omittedOperations,
    roles: {
      waveScalar: 'Q',
      momentumRaise: 'P',
      momentumContract: 'A',
      ...(grammar.T ? { rankTwoTrace: 'T' } : {}),
      ...(grammar.L ? { coefficientEvaluation: 'L', coefficientTrace: 'G' } : {}),
    },
    certificates,
    provenance,
    presumptions: input,
    boundary: [
      'complete only inside the declared free-power, metric, and optional single-action law cell',
      'carrier selection, arbitrary Schur functors, critical-pair confluence beyond the checked bound, and physical recovery remain separate',
    ].join('; '),
  };
}

function serializableRules(rules) {
  return Object.fromEntries([...rules.entries()].map(([left, replacements]) => [
    left,
    replacements.map(([word, coefficient]) => ({
      word: word.join(' ') || 'I',
      coefficient: coefficient.d === 1n
        ? `${coefficient.n}`
        : `${coefficient.n}/${coefficient.d}`,
    })),
  ]));
}

function serializableCompiledGrammar(result) {
  if (!result.ok) return result;
  return {
    ...result,
    pairRules: serializableRules(result.pairRules),
    ...(result.dualityPairRules
      ? { dualityPairRules: serializableRules(result.dualityPairRules) }
      : {}),
  };
}

export {
  compileNaturalOperations,
  restrictPolynomialToInputRank,
  serializableCompiledGrammar,
  serializableRules,
};

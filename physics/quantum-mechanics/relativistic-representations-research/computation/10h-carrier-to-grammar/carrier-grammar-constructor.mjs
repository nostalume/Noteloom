import {
  rat,
} from '../10c-generative-residual-constructor/residual-constructor.mjs';

const ONE = rat(1);
const TWO = rat(2);
const MINUS_ONE = rat(-1);

function rule(...terms) {
  return terms;
}

function symmetricCoreRules() {
  return new Map([
    // Evaluation after multiplication: i_p m_p=m_p i_p+eta(p,p).
    ['A P', rule([['P', 'A'], ONE], [['Q'], ONE])],
    // The metric contraction can hit either new symmetric slot.
    ['T P', rule([['P', 'T'], ONE], [['A'], TWO])],
    ['T A', rule([['A', 'T'], ONE])],
  ]);
}

function cliffordLocalRules() {
  return new Map([
    // Gamma contraction can hit the inserted momentum slot.
    ['G P', rule([['P', 'G'], ONE], [['L'], ONE])],
    // Clifford polarization turns the anticommutator into 2 A.
    ['G L', rule([['L', 'G'], MINUS_ONE], [['A'], TWO])],
    ['G A', rule([['A', 'G'], ONE])],
    ['A P', rule([['P', 'A'], ONE], [['Q'], ONE])],
    ['P L', rule([['L', 'P'], ONE])],
    ['A L', rule([['L', 'A'], ONE])],
    ['L L', rule([['Q'], ONE])],
  ]);
}

function cliffordDualityRules() {
  return new Map([
    ['P Y', rule([['Y', 'P'], ONE])],
    ['L Y', rule([['Y', 'L'], MINUS_ONE], [['P'], TWO])],
    ['A Y', rule([['Y', 'A'], ONE], [['L'], ONE])],
    ['G P', rule([['P', 'G'], ONE], [['L'], ONE])],
    ['G L', rule([['L', 'G'], MINUS_ONE], [['A'], TWO])],
    ['G A', rule([['A', 'G'], ONE])],
    ['A P', rule([['P', 'A'], ONE], [['Q'], ONE])],
    ['L P', rule([['P', 'L'], ONE])],
    ['A L', rule([['L', 'A'], ONE])],
    ['L L', rule([['Q'], ONE])],
  ]);
}

function refuse(phase, reason, missingResources = []) {
  return { ok: false, phase, reason, missingResources };
}

function validatePresentation(input) {
  const presentation = input?.presentation;
  if (!presentation) {
    return refuse(
      'carrier-presentation',
      'a physical helicity or Lorentz highest-weight label does not choose an off-shell carrier functor',
      ['presentation'],
    );
  }
  if (presentation.functor !== 'symmetric-power') {
    return refuse(
      'carrier-functor',
      'the bounded constructor currently supports only the symmetric-power potential functor',
      ['symmetric-power functor'],
    );
  }
  if (!input.resources?.symmetricAlgebra) {
    return refuse(
      'carrier-functor',
      'symmetric multiplication and derivation are required to construct rank-shifting operations',
      ['symmetricAlgebra'],
    );
  }
  if (!input.resources?.metric?.nondegenerate || !input.resources.metric.symmetric) {
    return refuse(
      'invariant-duality',
      'a nondegenerate invariant symmetric form is required to identify momentum with contraction and construct trace',
      ['nondegenerate symmetric metric'],
    );
  }
  if (!['scalar', 'dirac'].includes(presentation.coefficientModule)) {
    return refuse(
      'coefficient-module',
      'the bounded constructor supports scalar or Dirac coefficient modules',
      ['scalar or dirac coefficientModule'],
    );
  }
  if (presentation.coefficientModule === 'dirac'
      && !input.resources?.cliffordAction?.polarizesMetric) {
    return refuse(
      'coefficient-action',
      'a Dirac label alone does not construct gamma contraction; an equivariant Clifford action polarizing the metric is required',
      ['cliffordAction.polarizesMetric'],
    );
  }
  return null;
}

function constructScalarPacket(input) {
  const grammar = Object.freeze({
    Q: { momentumDegree: 2, rankShift: 0, traceDepth: 0 },
    P: { momentumDegree: 1, rankShift: 1, traceDepth: 0 },
    A: { momentumDegree: 1, rankShift: -1, traceDepth: 0 },
    T: { momentumDegree: 0, rankShift: -2, traceDepth: 1 },
  });
  const dualityGrammar = Object.freeze({
    ...grammar,
    U: { momentumDegree: 0, rankShift: 2, traceDepth: -1 },
  });
  return {
    ok: true,
    family: 'symmetric-tensor',
    carrier: 'Sym^r(V*)',
    provenance: 'generated from Sym(V*) multiplication/derivation and invariant metric duality',
    grammar,
    pairRules: symmetricCoreRules(),
    dualityGrammar,
    adjoints: { Q: 'Q', P: 'A', A: 'P', T: 'U', U: 'T' },
    constructions: {
      P: 'symmetric multiplication m_p',
      A: 'derivation i_(p sharp) constructed by the metric',
      Q: 'eta^(-1)(p,p)',
      T: 'double contraction i_(eta^(-1))',
      U: 'symmetric multiplication m_eta',
    },
    witnesses: [
      'i_(p sharp) m_p - m_p i_(p sharp) = eta^(-1)(p,p)',
      'i_(eta^(-1)) m_p - m_p i_(eta^(-1)) = 2 i_(p sharp)',
      'Fischer duality gives P^dagger=A and T^dagger=U',
    ],
    presumptions: input,
  };
}

function constructDiracPacket(input) {
  const grammar = Object.freeze({
    Q: { momentumDegree: 2, rankShift: 0, traceDepth: 0 },
    L: { momentumDegree: 1, rankShift: 0, traceDepth: 0 },
    P: { momentumDegree: 1, rankShift: 1, traceDepth: 0 },
    A: { momentumDegree: 1, rankShift: -1, traceDepth: 0 },
    G: { momentumDegree: 0, rankShift: -1, traceDepth: 1 },
  });
  const dualityGrammar = Object.freeze({
    ...grammar,
    Y: { momentumDegree: 0, rankShift: 1, traceDepth: -1 },
  });
  return {
    ok: true,
    family: 'symmetric-spinor-tensor',
    carrier: 'Sym^r(V*) tensor Delta',
    provenance: 'generated from Sym(V*) operations, invariant metric, and the equivariant Clifford action on Delta',
    grammar,
    pairRules: cliffordLocalRules(),
    dualityGrammar,
    dualityPairRules: cliffordDualityRules(),
    adjoints: { Q: 'Q', P: 'A', A: 'P', L: 'L', G: 'Y', Y: 'G' },
    constructions: {
      P: 'symmetric multiplication m_p on tensor slots',
      A: 'derivation i_(p sharp) on tensor slots',
      Q: 'eta^(-1)(p,p)',
      L: 'gamma(p) on the Dirac coefficient module',
      G: 'gamma contraction gamma dot partial_u',
      Y: 'gamma insertion gamma(u)',
    },
    witnesses: [
      'G P - P G = L because gamma contraction can hit the inserted p slot',
      'G L + L G = 2 A by Clifford polarization',
      'L^2=Q by evaluating the Clifford identity at (p,p)',
      'Dirac-Fischer duality gives P^dagger=A, G^dagger=Y, and L^dagger=L',
    ],
    presumptions: input,
  };
}

function constructCarrierGrammar(input = {}) {
  const rejected = validatePresentation(input);
  if (rejected) return rejected;
  if (input.presentation.coefficientModule === 'scalar') return constructScalarPacket(input);
  return constructDiracPacket(input);
}

function serializableRules(rules) {
  return Object.fromEntries([...rules.entries()].map(([left, replacements]) => [
    left,
    replacements.map(([word, coefficient]) => ({
      word: word.join(' ') || 'I',
      coefficient: coefficient.d === 1n ? `${coefficient.n}` : `${coefficient.n}/${coefficient.d}`,
    })),
  ]));
}

function serializableCarrierGrammar(result) {
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
  constructCarrierGrammar,
  serializableCarrierGrammar,
  serializableRules,
};

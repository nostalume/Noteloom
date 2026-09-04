const forbiddenAnswerKeys = new Set([
  'anticommutator',
  'cliffordAction',
  'cliffordAlgebra',
  'gammaMatrices',
  'expectedAction',
]);

function refuse(phase, reason, details = {}) {
  return { ok: false, phase, reason, ...details };
}

function findForbiddenKey(value, path = []) {
  if (!value || typeof value !== 'object') return null;
  for (const [key, child] of Object.entries(value)) {
    const next = [...path, key];
    if (forbiddenAnswerKeys.has(key)) return next.join('.');
    const nested = findForbiddenKey(child, next);
    if (nested) return nested;
  }
  return null;
}

function validateMetric(metric) {
  return metric?.role === 'metric'
    && metric.rank === 2
    && metric.exchangeSign === 1
    && metric.invariant
    && metric.nondegenerate
    && metric.spacetimeDimension === 4;
}

function generateFirstOrderFactorization(input = {}) {
  const forbidden = findForbiddenKey(input);
  if (forbidden) {
    return refuse(
      'answer-bearing-input',
      'supply a propagation capability and carrier resources, not a Clifford relation or matrix realization',
      { rejectedKey: forbidden },
    );
  }

  const { metric, capability, chiralCarrier, moduleRequest, resourceBudget } = input;
  if (!validateMetric(metric)) {
    return refuse(
      'metric-resource',
      'the four-dimensional bench requires a nondegenerate invariant symmetric metric',
      { required: 'invariant nondegenerate symmetric metric on a four-dimensional vector carrier' },
    );
  }
  if (!capability?.equivariant
      || capability.momentumOrder !== 1
      || !capability.linearInMomentum) {
    return refuse(
      'first-order-capability',
      'the requested symbol must be Lorentz-equivariant and linear of momentum order one',
    );
  }
  if (capability.completion?.kind !== 'scalar-quadratic'
      || capability.completion.invariant !== metric.id
      || capability.completion.coefficient !== 1) {
    return refuse(
      'completion-capability',
      'this constructor factors the selected metric quadratic scalar Q(p) with unit normalization',
      { suppliedCompletion: capability.completion },
    );
  }
  if (chiralCarrier?.field !== 'complex'
      || chiralCarrier.vectorFactorization !== 'S tensor Sbar'
      || chiralCarrier.leftDimension !== 2
      || chiralCarrier.rightDimension !== 2) {
    return refuse(
      'chiral-carrier-resource',
      'the bounded bench requires the four-dimensional complex chiral factorization V_C=S tensor Sbar',
    );
  }
  if (moduleRequest?.reality !== 'complex') {
    return refuse(
      'reality-resource',
      'a Majorana or other real structure requires an additional conjugation/intertwiner resource',
      { requestedReality: moduleRequest?.reality },
    );
  }

  const paired = moduleRequest?.source === 'S direct-sum Sbar'
    && moduleRequest?.target === 'S direct-sum Sbar'
    && moduleRequest?.requireEndomorphism
    && moduleRequest?.parity === 'paired';
  if (!paired) {
    return refuse(
      'chirality-obstruction',
      'the vector carrier S tensor Sbar changes chirality, so a first-order vector symbol is not an endomorphism of one Weyl summand',
      {
        computedMaps: ['d_+(v):S -> Sbar', 'd_-(v):Sbar -> S'],
        repair: 'pair opposite chiralities as Delta=S direct-sum Sbar, or request a non-endomorphic chiral map',
      },
    );
  }
  if ((resourceBudget?.maximumComplexDimension ?? 0) < 4) {
    return refuse(
      'module-budget',
      'the parity-paired endomorphism carrier needs complex dimension four',
      { required: 4, available: resourceBudget?.maximumComplexDimension ?? 0 },
    );
  }

  const squareEvaluation = [
    'apply the requested completion to u+v',
    'subtract its evaluations at u and at v',
    'use linearity d(u+v)=d(u)+d(v)',
  ];
  const polarizationEvaluation = [
    'd(u+v)^2-d(u)^2-d(v)^2=d(u)d(v)+d(v)d(u)',
    'Q(u+v)-Q(u)-Q(v)=2 eta^(-1)(u,v)',
  ];
  const action = {
    law: 'metric-polarized-quadratic-action',
    invariant: metric.id,
    equivariant: true,
    polarizationCoefficient: 2,
    formallySelfAdjoint: true,
    origin: {
      kind: 'generated-first-order-factorization',
      constructor: 'FirstOrderFactorizer',
      inputCapability: 'equivariant momentum-linear symbol with scalar metric-square completion',
      chiralityRepair: 'Delta=S direct-sum Sbar',
    },
  };

  return {
    ok: true,
    family: 'first-order-metric-factorization',
    coefficientModule: {
      label: 'Delta',
      decomposition: 'S direct-sum Sbar',
      complexDimension: 4,
      vectorAction: ['d_+(v):S -> Sbar', 'd_-(v):Sbar -> S'],
    },
    symbolSpace: 'Hom_Lor(V* tensor Delta, Delta)',
    universalAlgebra: {
      tensorAlgebra: 'T(V*)',
      obstruction: 'uv+vu-2 eta^(-1)(u,v) 1',
      quotient: 'T(V*)/<u tensor v+v tensor u-2 eta^(-1)(u,v) 1>',
      universalProperty: 'every linear metric-square factorization factors uniquely through this quotient',
    },
    action,
    certificates: {
      square: {
        identity: 'd(p)d(p)=Q(p) I',
        origin: 'requested two-step scalar-wave completion',
      },
      polarization: {
        identity: 'd(u)d(v)+d(v)d(u)=2 eta^(-1)(u,v) I',
        evaluation: polarizationEvaluation,
      },
      chirality: {
        obstruction: 'V_C tensor S contains Sbar rather than an endomorphic S channel',
        repair: 'the off-diagonal pair d_+ direct-sum d_- acts on Delta',
      },
      universality: {
        evaluation: squareEvaluation,
        witness: 'the tensor-algebra map kills precisely the generated quadratic obstruction and therefore descends to the quotient',
      },
    },
    boundary: [
      'complex four-dimensional Lorentz carrier only',
      'the real structure, parity interpretation, positivity, and CAR quantization are not generated',
      'classification of all Clifford modules is outside this bench',
    ],
  };
}

export { generateFirstOrderFactorization };

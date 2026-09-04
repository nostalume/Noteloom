const COST_AXES = Object.freeze([
  'maxDifferentialOrder',
  'irreducibleCarrierSlots',
  'gaugeIdentityDepth',
  'physicalRecoveryDepth',
  'sourceActionDepth',
  'observableRecoveryOrder',
  'unexplainedCharacteristicDebt',
  'rawComponentLoad',
]);

const KNOWN_CAPABILITIES = new Set([
  'physical-realization',
  'local-equation',
  'local-potential',
  'gauge-invariant-curvature-output',
  'physical-shell-potential-curvature-bridge',
  'local-polynomial-curvature-inverse',
  'quadratic-action',
  'admissible-source',
  'causal-response',
  'positive-shell-amplitude',
]);

function refuse(phase, reason, details = {}) {
  return { ok: false, phase, reason, ...details };
}

function deriveCost(trace, required) {
  const curvatureRecoveryRequested = required.has('gauge-invariant-curvature-output')
    || required.has('physical-shell-potential-curvature-bridge');
  return {
    maxDifferentialOrder: Math.max(...trace.mapOrders),
    irreducibleCarrierSlots: trace.irreducibleCarrierMultiplicities
      .reduce((sum, multiplicity) => sum + multiplicity, 0),
    gaugeIdentityDepth: trace.gaugeIdentitySteps.length,
    physicalRecoveryDepth: trace.physicalRecoverySteps.length,
    sourceActionDepth: trace.sourceActionSteps.length,
    observableRecoveryOrder: curvatureRecoveryRequested
      ? trace.curvatureRecoveryOrder
      : 0,
    unexplainedCharacteristicDebt: trace.unexplainedCharacteristicStrata.length,
    rawComponentLoad: trace.carrierDimensions.reduce((sum, dimension) => sum + dimension, 0),
  };
}

function hasCurvaturePacket(spin, packet) {
  return packet?.ok
    && packet.family === 'parity-paired-integer-spin-curvature-compatibility'
    && packet.spin === spin
    && packet.certificates?.minimalDegree
    && packet.certificates?.multiplicityAtMinimalDegree === 1;
}

function curvatureCertificate(spin, generatedBridge) {
  return generatedBridge
    ? `N10j: generated degree-${spin} potential/curvature physical-shell map`
    : 'N5 Section 4: Maxwell potential/curvature physical-shell isomorphism';
}

function directCurvatureRoute(spin, required, curvaturePacket) {
  const generatedBridge = hasCurvaturePacket(spin, curvaturePacket);
  const bridgeSupported = spin === 1 || generatedBridge;
  const capabilities = [
    'physical-realization',
    'local-equation',
    'gauge-invariant-curvature-output',
  ];
  if (bridgeSupported) capabilities.push('physical-shell-potential-curvature-bridge');

  const constructionTrace = {
    mapOrders: [1],
    irreducibleCarrierMultiplicities: [2, 2],
    gaugeIdentitySteps: [],
    physicalRecoverySteps: ['identify the nonzero-null kernel with the two chiral helicity lines'],
    sourceActionSteps: [],
    curvatureRecoveryOrder: required.has('physical-shell-potential-curvature-bridge')
      ? spin
      : 0,
    unexplainedCharacteristicStrata: [],
    carrierDimensions: [4 * spin + 2, 8 * spin],
  };
  return {
    id: 'parity-paired-direct-curvature',
    presentation: `Sym^${2 * spin}(S) direct-sum Sym^${2 * spin}(bar S)`,
    capabilities,
    certificates: [
      'N4: first-order chiral symbols and null little-group helicity lines',
      'N5: common physical fiber with the potential route',
      ...(bridgeSupported
        ? [curvatureCertificate(spin, generatedBridge)]
        : []),
    ],
    missingCertificates: bridgeSupported
      ? []
      : ['N10j curvature-compatibility packet for this spin'],
    capabilityObstructions: bridgeSupported
      ? [`local-polynomial-curvature-inverse: momentum homogeneity requires degree -${spin}`]
      : [],
    constructionTrace,
    cost: deriveCost(constructionTrace, required),
    boundary: 'No invariant action, admissible-source adapter, or causal Green completion is certified for this route in the worktable.',
  };
}

function potentialDimensions(spin) {
  return {
    parameter: spin ** 2,
    field: 2 * spin ** 2 + 2,
    compressedEquation: (spin + 1) ** 2,
  };
}

function compressedPotentialRoute(spin, required, curvaturePacket) {
  const dimensions = potentialDimensions(spin);
  const generatedBridge = hasCurvaturePacket(spin, curvaturePacket);
  const bridgeSupported = spin === 1 || generatedBridge;
  const capabilities = [
    'physical-realization',
    'local-equation',
    'local-potential',
  ];
  if (bridgeSupported) {
    capabilities.push(
      'gauge-invariant-curvature-output',
      'physical-shell-potential-curvature-bridge',
    );
  }

  const constructionTrace = {
    mapOrders: [1, 2],
    irreducibleCarrierMultiplicities: spin === 1 ? [1, 1, 1] : [1, 2, 1],
    gaugeIdentitySteps: ['divide the equation kernel by the gradient gauge image'],
    physicalRecoverySteps: [
      'compute the equation kernel',
      'divide by the gradient gauge image',
      'restrict and descend to the trace-free null screen',
    ],
    sourceActionSteps: [],
    curvatureRecoveryOrder: bridgeSupported ? spin : 0,
    unexplainedCharacteristicStrata: [],
    carrierDimensions: [dimensions.parameter, dimensions.field, dimensions.compressedEquation],
  };
  return {
    id: 'compressed-symmetric-potential',
    presentation: `H_${spin - 1} -> ker(T^2) in Sym^${spin}(V*) -> H_${spin}`,
    capabilities,
    certificates: [
      'N10 Section 6.8: minimal upper equation target with unchanged kernel',
      'N4a Section 8: exact null-screen quotient and characteristic audit',
      ...(bridgeSupported
        ? [curvatureCertificate(spin, generatedBridge)]
        : []),
    ],
    missingCertificates: bridgeSupported
      ? ['quadratic action and causal response for the compressed equation target']
      : [
          'quadratic action and causal response for the compressed equation target',
          'N10j curvature-compatibility packet for this spin',
        ],
    capabilityObstructions: bridgeSupported
      ? [`local-polynomial-curvature-inverse: momentum homogeneity requires degree -${spin}`]
      : [],
    constructionTrace,
    cost: deriveCost(constructionTrace, required),
    boundary: 'The smaller equation target is certified for realization, not for the action/source/causal capabilities of N4m.',
  };
}

function completedPotentialRoute(spin, required, curvaturePacket) {
  const dimensions = potentialDimensions(spin);
  const generatedBridge = hasCurvaturePacket(spin, curvaturePacket);
  const bridgeSupported = spin === 1 || generatedBridge;
  const capabilities = [
    'physical-realization',
    'local-equation',
    'local-potential',
    'quadratic-action',
    'admissible-source',
    'causal-response',
    'positive-shell-amplitude',
  ];
  if (bridgeSupported) {
    capabilities.push(
      'gauge-invariant-curvature-output',
      'physical-shell-potential-curvature-bridge',
    );
  }

  const constructionTrace = {
    mapOrders: [1, 2],
    irreducibleCarrierMultiplicities: spin === 1 ? [1, 1, 1] : [1, 2, 2],
    gaugeIdentitySteps: ['divide the equation kernel by the gradient gauge image'],
    physicalRecoverySteps: [
      'compute the equation kernel',
      'divide by the gradient gauge image',
      'restrict and descend to the trace-free null screen',
      'restrict the adapted source to the future shell',
      'complete in the support-faithful positive shell norm',
    ],
    sourceActionSteps: [
      'construct the Fischer pairing adapter',
      'construct the quadratic Euler operator',
      'form the admissible source quotient',
      'apply the scalar retarded or advanced Green operation',
    ],
    curvatureRecoveryOrder: bridgeSupported ? spin : 0,
    unexplainedCharacteristicStrata: [],
    carrierDimensions: [dimensions.parameter, dimensions.field, dimensions.field],
  };
  return {
    id: 'completed-symmetric-potential-machine',
    presentation: `FieldSystem_${spin}=(G,F,R,C,M)`,
    capabilities,
    certificates: [
      'N4m: five-object field machine',
      'N4c/N4f: quadratic Euler operator and causal source/solution quotient',
      'N4g/N4h: positive shell amplitude and support-faithful norm',
      ...(bridgeSupported
        ? [curvatureCertificate(spin, generatedBridge)]
        : []),
    ],
    missingCertificates: bridgeSupported
      ? []
      : ['N10j curvature-compatibility packet for this spin'],
    capabilityObstructions: bridgeSupported
      ? [`local-polynomial-curvature-inverse: momentum homogeneity requires degree -${spin}`]
      : [],
    constructionTrace,
    cost: deriveCost(constructionTrace, required),
    boundary: 'The completion is supported separately for each finite integer spin; countable-spin and interacting completions remain open.',
  };
}

function missingCapabilities(route, required) {
  const supplied = new Set(route.capabilities);
  return [...required].filter((capability) => !supplied.has(capability));
}

function budgetViolations(route, budget) {
  return Object.entries(budget).flatMap(([axis, maximum]) => {
    if (!COST_AXES.includes(axis)) return [];
    return route.cost[axis] > maximum
      ? [{ axis, actual: route.cost[axis], maximum }]
      : [];
  });
}

function dominates(left, right) {
  const noWorse = COST_AXES.every((axis) => left.cost[axis] <= right.cost[axis]);
  const strictlyBetter = COST_AXES.some((axis) => left.cost[axis] < right.cost[axis]);
  return noWorse && strictlyBetter;
}

function selectPresentations(input = {}) {
  const fiber = input.physicalFiber;
  if (fiber?.kind !== 'massless-helicity-pair'
      || !Number.isInteger(fiber.magnitude)
      || fiber.magnitude < 1) {
    return refuse(
      'physical-target',
      'the bounded selector currently accepts one parity-paired positive integer helicity',
      { supportedTarget: { kind: 'massless-helicity-pair', magnitude: 'positive integer' } },
    );
  }
  if (input.comparisonMode && input.comparisonMode !== 'pareto') {
    return refuse(
      'comparison-policy',
      'no scalar ranking is intrinsic; use the capability-relative Pareto order',
      { supportedMode: 'pareto' },
    );
  }

  const requiredList = input.requiredCapabilities ?? ['physical-realization'];
  const unknownCapabilities = requiredList.filter((item) => !KNOWN_CAPABILITIES.has(item));
  if (unknownCapabilities.length > 0) {
    return refuse('capability-contract', 'one or more requested capabilities are not defined', {
      unknownCapabilities,
      knownCapabilities: [...KNOWN_CAPABILITIES],
    });
  }
  const budget = input.resourceBudget ?? {};
  const unknownBudgetAxes = Object.keys(budget).filter((axis) => !COST_AXES.includes(axis));
  const invalidBudgetAxes = Object.entries(budget)
    .filter(([, maximum]) => !Number.isFinite(maximum) || maximum < 0)
    .map(([axis]) => axis);
  if (unknownBudgetAxes.length > 0 || invalidBudgetAxes.length > 0) {
    return refuse('resource-budget', 'the resource budget contains an unknown or invalid axis', {
      unknownBudgetAxes,
      invalidBudgetAxes,
      costAxes: COST_AXES,
    });
  }

  const required = new Set(requiredList);
  const curvaturePacket = input.curvatureCompatibilityPacket;
  const candidates = [
    directCurvatureRoute(fiber.magnitude, required, curvaturePacket),
    compressedPotentialRoute(fiber.magnitude, required, curvaturePacket),
    completedPotentialRoute(fiber.magnitude, required, curvaturePacket),
  ];
  const excluded = [];
  const eligible = [];
  for (const route of candidates) {
    const missing = missingCapabilities(route, required);
    const violations = budgetViolations(route, budget);
    if (missing.length > 0 || violations.length > 0) {
      excluded.push({
        id: route.id,
        missingCapabilities: missing,
        budgetViolations: violations,
        missingCertificates: route.missingCertificates,
        capabilityObstructions: route.capabilityObstructions,
      });
    } else {
      eligible.push(route);
    }
  }

  if (eligible.length === 0) {
    return refuse(
      'capability-selection',
      'no worktable-certified presentation satisfies both the requested output and resource budget',
      {
        physicalFiber: fiber,
        requiredCapabilities: requiredList,
        excluded,
        costAxes: COST_AXES,
      },
    );
  }

  const frontier = eligible.filter((candidate) =>
    !eligible.some((other) => other.id !== candidate.id && dominates(other, candidate)));
  const dominated = eligible
    .filter((candidate) => !frontier.includes(candidate))
    .map((candidate) => ({
      ...candidate,
      dominatedBy: frontier.filter((other) => dominates(other, candidate)).map((other) => other.id),
    }));

  return {
    ok: true,
    scope: 'three already-supported parity-paired integer-helicity routes',
    physicalFiber: fiber,
    requiredCapabilities: requiredList,
    comparisonMode: 'pareto',
    costAxes: COST_AXES,
    frontier,
    dominated,
    excluded,
    boundary: 'Selection is relative to declared capabilities, this cost vector, and worktable certificates; it is not carrier-global minimality.',
  };
}

export {
  COST_AXES,
  KNOWN_CAPABILITIES,
  dominates,
  selectPresentations,
};

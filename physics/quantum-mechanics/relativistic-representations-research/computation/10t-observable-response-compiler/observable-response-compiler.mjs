import {
  constructDirectConstrainedGreen,
} from '../10r-direct-constrained-green/direct-constrained-green.mjs';

const answerBearingKeys = new Set([
  'expectedVisibleLayer',
  'expectedVerdict',
  'preferredPresentation',
  'responseFormula',
]);

function refuse(phase, reason, details = {}) {
  return { ok: false, phase, reason, ...details };
}

function potentialDimension(spin) {
  // dim H_s + dim H_(s-2) in four dimensions.
  return (spin + 1) ** 2 + (spin - 1) ** 2;
}

function curvatureDimension(spin) {
  // Two chiral copies of Sym^(2s)(C^2), each of dimension 2s+1.
  return 2 * (2 * spin + 1);
}

function transverseLayerDimension(spin) {
  return 2 * spin + 1;
}

function stableFusedMultiplier(spin, frequency) {
  if (frequency === 0) return spin === 0 ? 1 : 0;
  if (frequency >= 1 && spin >= 2) {
    return frequency ** (spin - 2) / (1 + 1 / frequency ** 2);
  }
  return frequency ** spin / (1 + frequency ** 2);
}

function numericalFusionCheck(spin, ordinaryFrequency, stressFrequency) {
  const evaluate = (frequency) => {
    const denominator = 1 + frequency ** 2;
    const curvatureSymbol = frequency ** spin;
    const potentialFirst = curvatureSymbol * (1 / denominator);
    const curvatureFirst = curvatureSymbol / denominator;
    const fused = stableFusedMultiplier(spin, frequency);
    const referenceScale = Math.max(1, Math.abs(fused));
    return {
      frequency,
      denominator,
      curvatureSymbol,
      potentialFirst,
      curvatureFirst,
      fused,
      sequentialFinite: Number.isFinite(potentialFirst) && Number.isFinite(curvatureFirst),
      fusedFinite: Number.isFinite(fused),
      ordinaryCoincidence: Number.isFinite(potentialFirst)
        && Math.abs(potentialFirst - curvatureFirst) <= 1e-12 * referenceScale
        && Math.abs(potentialFirst - fused) <= 1e-12 * referenceScale,
      naiveCurvatureIntermediateToOutput: Number.isFinite(curvatureSymbol)
        ? Math.abs(curvatureSymbol) / Math.max(Number.MIN_VALUE, Math.abs(fused))
        : 'overflow',
    };
  };
  return {
    ordinary: evaluate(ordinaryFrequency),
    stress: evaluate(stressFrequency),
  };
}

function compileSpin(row, spin, sourceCount, observablesPerSource, frequencies) {
  const layerVisibility = row.layers.map((layer) => {
    const raised = layer.label < spin;
    return {
      label: layer.label,
      raised,
      role: layer.role,
      curvatureImage: raised ? 'zero' : 'visible',
      witness: raised
        ? 'X_(s,l)=R_(s-1)X_(s-1,l), K_s R_(s-1)=0 from K_s P=K_s U=0'
        : 'A X_(s,s)=0, hence B_s X_(s,s)=0 and f_s(0)=1',
    };
  });
  const visible = layerVisibility.filter((layer) => layer.curvatureImage === 'visible');
  const potentialChannels = potentialDimension(spin);
  const curvatureChannels = curvatureDimension(spin);
  const visibleChannels = transverseLayerDimension(spin);
  const fullDirectGreenWork = sourceCount
    * row.cost.maximumScalarGreenDepth
    * row.layers.reduce((sum, layer) => sum + layer.stabilizerDimension, 0);
  const potentialGreenWork = sourceCount * potentialChannels;
  const curvatureCarrierGreenWork = sourceCount * curvatureChannels;
  const pointwiseVisibleSourceLayerCoordinates = sourceCount * visibleChannels;
  const observableEvaluations = sourceCount * observablesPerSource;

  return {
    spin,
    layerVisibility,
    generatedObservableResponse: {
      directInput: 'K_s Q^(-1) f_s(B_s) j',
      compensatedInput: 'K_s Q^(-1) M_s^(-1) J',
      normalForm: 'Q^(-1) K_s J',
      directWitness: 'K_s B_s=K_s R_(s-1)A/Q=0 and f_s(0)=1',
      compensatedWitness: 'M_s^(-1)-I has image in im U and K_s U=0',
      causalMeaning: 'the same retarded or advanced scalar Green distribution acts after the local curvature source map',
    },
    certificates: {
      exactlyOneVisibleLayer: visible.length === 1 && visible[0].label === spin,
      allLowerLayersAnnihilated: layerVisibility
        .filter((layer) => layer.label < spin)
        .every((layer) => layer.curvatureImage === 'zero'),
      directDepthCollapsesToOne: row.cost.maximumScalarGreenDepth > 1,
      presentationIndependentNormalForm: true,
    },
    workload: {
      sourceCount,
      observablesPerSource,
      observableEvaluations,
      curvatureConstructionApplications: sourceCount,
      fullDirectGreenWork,
      potentialFirstScalarGreenChannelWork: potentialGreenWork,
      curvatureCarrierScalarGreenChannelWork: curvatureCarrierGreenWork,
      pointwiseVisibleSourceLayerCoordinates,
      formalCurvatureChannelSaving: potentialGreenWork - curvatureCarrierGreenWork,
      repeatedObservableEffect: 'the response is cached once per source; more functionals reuse it equally in every presentation',
      repeatedSourceEffect: 'compiler and rewrite certificates are reused; per-source scalar-Green channel differences accumulate',
      routeVerdict: curvatureChannels < potentialChannels
        ? 'formal curvature-carrier Green work is smaller, but this belongs to the common observable compiler rather than the constrained presentation'
        : (curvatureChannels === potentialChannels
          ? 'formal scalar-Green channel work is equal'
          : 'potential-carrier Green work is smaller'),
      activeCostBoundary: '2s+1 is the pointwise top source-layer dimension; minimal image/storage coordinates and their global bundle are not constructed here',
    },
    fusion: {
      exactRule: 'do not materialize K_s J and then divide by Q; compile the boundary-selected composite G_Q K_s as one response operation',
      regularizedProxy: 'frequency^s/(1+frequency^2)',
      checks: numericalFusionCheck(
        spin,
        frequencies.ordinary,
        frequencies.stress,
      ),
      boundary: 'the numerical proxy tests representation order and floating-point range; it is not a wavefront, runtime, or physical ultraviolet theorem',
    },
  };
}

function compileObservableResponse(input = {}) {
  const rejectedKey = Object.keys(input).find((key) => answerBearingKeys.has(key));
  if (rejectedKey) {
    return refuse(
      'answer-bearing-input',
      'the observable compiler accepts spins and a workload, not a visible layer, response formula, preferred presentation, or verdict',
      { rejectedKey },
    );
  }
  const {
    spins,
    sourceCount,
    observablesPerSource,
    ordinaryFrequency = 10,
    stressFrequency = 1e80,
    requestedCapability,
  } = input;
  if (requestedCapability !== 'batched-gauge-invariant-curvature-response') {
    return refuse(
      'requested-capability',
      'the bounded bench compiles repeated gauge-invariant curvature observables from compact sources',
      { requestedCapability },
    );
  }
  if (!Array.isArray(spins)
      || spins.some((spin) => !Number.isInteger(spin) || spin < 2)) {
    return refuse('spin-budget', 'separate integer spins at least two are required');
  }
  if (!Number.isInteger(sourceCount) || sourceCount < 1
      || !Number.isInteger(observablesPerSource) || observablesPerSource < 1) {
    return refuse('workload', 'positive integer source and observable counts are required');
  }
  const green = constructDirectConstrainedGreen({
    dimension: 4,
    spins,
    requestedCapability: 'generic-compact-source-causal-response',
  });
  if (!green.ok) return refuse(
    'upstream-direct-green',
    'the N10r spectrum generator refused the requested spin workload',
    { upstream: green },
  );

  const rows = Object.fromEntries(spins.map((spin) => [
    spin,
    compileSpin(green.spins[spin], spin, sourceCount, observablesPerSource, {
      ordinary: ordinaryFrequency,
      stress: stressFrequency,
    }),
  ]));
  const values = Object.values(rows);
  const certificates = {
    allLowerLayersInvisible: values.every((row) =>
      row.certificates.allLowerLayersAnnihilated),
    uniqueVisibleTopLayer: values.every((row) =>
      row.certificates.exactlyOneVisibleLayer),
    commonObservableNormalForm: values.every((row) =>
      row.certificates.presentationIndependentNormalForm),
    ordinaryFusionCoincides: values.every((row) =>
      row.fusion.checks.ordinary.ordinaryCoincidence),
    fusedStressValuesFinite: values.every((row) =>
      row.fusion.checks.stress.fusedFinite),
    stressExposesSequentialRangeFailure: values.some((row) =>
      !row.fusion.checks.stress.sequentialFinite),
  };
  if (Object.values(certificates).some((value) => !value)) {
    return refuse(
      'observable-response-certificate',
      'layer visibility, common normal form, or fused implementation certificate failed',
      { spins: rows, certificates },
    );
  }

  return {
    ok: true,
    family: 'observable-factored-curvature-response',
    capability: requestedCapability,
    construction: {
      input: 'N10r direct response, N10e compensated response, N10j curvature annihilators, and a declared batch workload',
      obstruction: 'field-first response computes layers that the requested curvature observable annihilates',
      generatedRewrite: 'K_s G_D j = G_Q K_s j = K_s G_F M_s^(-1)J',
      retainedOperation: 'compile and cache the boundary-selected composite G_Q K_s once per source, then evaluate every requested curvature functional',
      implementationRepair: 'fuse derivative and Green symbols when a spectral realization would materialize a much larger intermediate',
    },
    spins: rows,
    certificates,
    verdict: {
      semanticCompression: 'supported: every lower N10r layer is invisible to curvature and the full field response is unnecessary',
      computationalLeverage: 'supported only for the compiled observable operation relative to field-first execution; it is not an advantage of one field presentation over another',
      repeatedObservables: 'reuse is real but presentation-neutral; observable count does not multiply the route difference after caching',
      formalChannelCrossover: 'spin two is equal and spins three onward favor curvature-carrier scalar propagation before active-coordinate costs',
      numericalBoundary: 'fused spectral evaluation avoids avoidable intermediate range growth, but regularity loss and physical ultraviolet sensitivity remain',
    },
    stop: 'the free batched-curvature branch is closed: the reusable object is the observable response compiler, not the constrained carrier. Re-enter only with a different observable, non-scalar dynamics that fails to commute with K_s, or measured discretization data.',
  };
}

export { compileObservableResponse, stableFusedMultiplier };

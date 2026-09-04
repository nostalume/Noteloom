import {
  add,
  basis,
  contractionSymbol,
  identity,
  metric,
  metricInsertionSymbol,
  multiply,
  multiplicationSymbol,
  scale,
  traceSymbol,
} from '../04-local-symbol-extension/check-symmetric-potential.mjs';
import {
  spinTwoCurrentSymbol,
} from '../10e-generated-source-adapter/check-generated-source-adapter.mjs';

const tolerance = 1e-8;
const answerBearingKeys = new Set([
  'expectedLayers',
  'expectedSupport',
  'expectedVerdict',
  'layer',
  'projector',
]);

function refuse(phase, reason, details = {}) {
  return { ok: false, phase, reason, ...details };
}

function quadraticForm(momentum) {
  return momentum.reduce(
    (sum, value, axis) => sum + metric[axis] * value * value,
    0,
  );
}

function maximumAbsolute(matrix) {
  return matrix.reduce((maximum, row) => Math.max(
    maximum,
    ...row.map((value) => Math.abs(value)),
  ), 0);
}

function subtract(left, right) {
  return add(left, scale(-1, right));
}

function harmonicProjector() {
  // On rank two in four dimensions, T U=8 on scalars.
  return add(
    identity(basis(2).length),
    scale(-1 / 8, multiply(metricInsertionSymbol(0), traceSymbol(2))),
  );
}

function projectedRaise(momentum) {
  // R_1=P-U A/(2r+d-2)=P-U A/4.
  return add(
    multiplicationSymbol(1, momentum),
    scale(-1 / 4, multiply(
      metricInsertionSymbol(0),
      contractionSymbol(1, momentum),
    )),
  );
}

function normalizedDivergence(momentum) {
  const q = quadraticForm(momentum);
  if (Math.abs(q) < tolerance) {
    throw new Error('layer discovery requires a non-null momentum representative');
  }
  return scale(
    1 / q,
    multiply(projectedRaise(momentum), contractionSymbol(2, momentum)),
  );
}

function layerSpectrum(spin) {
  return Array.from({ length: spin + 1 }, (_, label) => ({
    label,
    eigenvalue: (spin * (spin + 1) - label * (label + 1)) / (2 * spin),
    dimension: 2 * label + 1,
    role: label === spin - 1 ? 'gauge' : 'physical-source',
  }));
}

function spectralComponent(operator, source, spectrum, selected) {
  let component = source;
  for (const other of spectrum) {
    if (other.label === selected.label) continue;
    component = scale(
      1 / (selected.eigenvalue - other.eigenvalue),
      subtract(multiply(operator, component), scale(other.eigenvalue, component)),
    );
  }
  return component;
}

function discoverLayerSupport(source, momentum) {
  const operator = normalizedDivergence(momentum);
  const spectrum = layerSpectrum(2);
  const scaleOfSource = Math.max(1, maximumAbsolute(source));
  const residuals = {
    trace: maximumAbsolute(multiply(traceSymbol(2), source)),
    divergence: maximumAbsolute(multiply(contractionSymbol(2, momentum), source)),
    normalizedDivergence: maximumAbsolute(multiply(operator, source)),
  };

  // The first path is a calculated short circuit, not a supplied label: A j=0
  // makes B j=R A j/Q=0, and the generated spectrum then identifies its layer.
  if (residuals.divergence < tolerance * scaleOfSource) {
    const zeroLayer = spectrum.find((entry) => Math.abs(entry.eigenvalue) < tolerance);
    return {
      method: 'calculated-divergence-short-circuit',
      active: [zeroLayer],
      components: { [zeroLayer.label]: source },
      residuals,
      operatorApplications: 1,
      reconstructionError: 0,
    };
  }

  const components = Object.fromEntries(spectrum.map((entry) => [
    entry.label,
    spectralComponent(operator, source, spectrum, entry),
  ]));
  const active = spectrum.filter((entry) => (
    maximumAbsolute(components[entry.label]) >= tolerance * scaleOfSource
  ));
  const reconstruction = active.reduce(
    (sum, entry) => add(sum, components[entry.label]),
    scale(0, source),
  );
  return {
    method: 'generated-spectral-projectors',
    active,
    components,
    residuals,
    operatorApplications: spectrum.length * (spectrum.length - 1),
    reconstructionError: maximumAbsolute(subtract(reconstruction, source)),
  };
}

function tensorToPolynomial(tensor) {
  const out = basis(2).map(() => [0]);
  const index = new Map(basis(2).map((powers, position) => [powers.join(','), position]));
  for (let left = 0; left < 4; left += 1) {
    for (let right = 0; right < 4; right += 1) {
      const powers = [0, 0, 0, 0];
      powers[left] += 1;
      powers[right] += 1;
      out[index.get(powers.join(','))][0] += tensor[left][right];
    }
  }
  return out;
}

function constructElectricWeylSeed(electricSeed) {
  if (!Array.isArray(electricSeed)
      || electricSeed.length !== 3
      || electricSeed.some((row) => !Array.isArray(row) || row.length !== 3)) {
    return refuse('weyl-seed-shape', 'the electric Weyl seed must be a 3 by 3 matrix');
  }
  const symmetryError = Math.max(...electricSeed.flatMap((row, i) =>
    row.map((value, j) => Math.abs(value - electricSeed[j][i]))));
  const trace = electricSeed[0][0] + electricSeed[1][1] + electricSeed[2][2];
  if (symmetryError > tolerance || Math.abs(trace) > tolerance) {
    return refuse(
      'weyl-seed-algebra',
      'the electric seed must be symmetric and trace free so its completion is Weyl typed',
      { symmetryError, trace },
    );
  }

  const C = Array.from({ length: 4 }, () => Array.from({ length: 4 }, () =>
    Array.from({ length: 4 }, () => Array(4).fill(0))));
  for (let i = 1; i < 4; i += 1) {
    for (let j = 1; j < 4; j += 1) {
      const value = electricSeed[i - 1][j - 1];
      C[0][i][0][j] = value;
      C[i][0][0][j] = -value;
      C[0][i][j][0] = -value;
      C[i][0][j][0] = value;
    }
  }
  const delta = (left, right) => (left === right ? 1 : 0);
  for (let i = 1; i < 4; i += 1) {
    for (let j = 1; j < 4; j += 1) {
      for (let k = 1; k < 4; k += 1) {
        for (let l = 1; l < 4; l += 1) {
          C[i][j][k][l] =
            delta(i, k) * electricSeed[j - 1][l - 1]
            - delta(i, l) * electricSeed[j - 1][k - 1]
            - delta(j, k) * electricSeed[i - 1][l - 1]
            + delta(j, l) * electricSeed[i - 1][k - 1];
        }
      }
    }
  }
  return {
    ok: true,
    seed: C,
    certificates: {
      symmetricElectricSeed: symmetryError < tolerance,
      traceFreeElectricSeed: Math.abs(trace) < tolerance,
    },
  };
}

function constructWeylDoubleDivergencePreparation({ electricSeed } = {}) {
  const generated = constructElectricWeylSeed(electricSeed);
  if (!generated.ok) return generated;
  return {
    ok: true,
    name: 'compact-Weyl-seed-double-divergence',
    derivativeOrder: 2,
    seedCarrier: 'compact scalar profile times an algebraic Weyl tensor',
    operation: 'J_(mu nu)=partial^alpha partial^beta(C_(mu alpha nu beta) chi)',
    evaluate(momentum) {
      const tensor = Array.from({ length: 4 }, () => Array(4).fill(0));
      for (let mu = 0; mu < 4; mu += 1) {
        for (let nu = 0; nu < 4; nu += 1) {
          for (let alpha = 0; alpha < 4; alpha += 1) {
            for (let beta = 0; beta < 4; beta += 1) {
              tensor[mu][nu] += momentum[alpha] * momentum[beta]
                * generated.seed[mu][alpha][nu][beta];
            }
          }
        }
      }
      return tensorToPolynomial(tensor);
    },
    origin: [
      'antisymmetry in (mu,alpha) makes p^mu J_(mu nu)=0',
      'the Weyl trace identity makes eta^(mu nu) J_(mu nu)=0',
      'no momentum inverse or prescribed response layer is used',
    ],
    certificates: generated.certificates,
  };
}

function existingCompactCurrentPreparation() {
  return {
    ok: true,
    name: 'N10e-compact-bivector-current',
    derivativeOrder: 2,
    seedCarrier: 'compact scalar profile and two fixed bivectors',
    operation: 'difference of two squared bivector-momentum contractions',
    evaluate: spinTwoCurrentSymbol,
    origin: ['bivector antisymmetry makes the current divergence vanish'],
  };
}

function screenContrast(source) {
  const index = new Map(basis(2).map((powers, position) => [powers.join(','), position]));
  const xx = source[index.get('0,2,0,0')][0];
  const yy = source[index.get('0,0,2,0')][0];
  return xx - yy;
}

function analyzePreparation(preparation, nonnullMomentum, nullMomentum) {
  const raw = preparation.evaluate(nonnullMomentum);
  const harmonic = multiply(harmonicProjector(), raw);
  const support = discoverLayerSupport(harmonic, nonnullMomentum);
  const nullSource = preparation.evaluate(nullMomentum);
  const nullDivergence = maximumAbsolute(multiply(
    contractionSymbol(2, nullMomentum),
    nullSource,
  ));
  const nullTrace = maximumAbsolute(multiply(traceSymbol(2), nullSource));
  const contrast = screenContrast(nullSource);
  const gaugeActive = support.active.some((entry) => entry.role === 'gauge');
  const singlePhysicalLayer = support.active.length === 1 && !gaugeActive;
  const sourceAlreadyHarmonic = maximumAbsolute(subtract(raw, harmonic)) < tolerance;
  const baselineAdapterIsIdentity = sourceAlreadyHarmonic
    && support.residuals.divergence < tolerance;
  const activeDimension = support.active.reduce((sum, entry) => sum + entry.dimension, 0);

  return {
    preparation: {
      name: preparation.name,
      derivativeOrder: preparation.derivativeOrder,
      seedCarrier: preparation.seedCarrier,
      operation: preparation.operation,
      origin: preparation.origin,
    },
    nonnull: {
      momentum: nonnullMomentum,
      rawTrace: maximumAbsolute(multiply(traceSymbol(2), raw)),
      rawDivergence: maximumAbsolute(multiply(
        contractionSymbol(2, nonnullMomentum), raw,
      )),
      sourceAlreadyHarmonic,
      supportMethod: support.method,
      activeLayers: support.active.map((entry) => ({
        label: entry.label,
        eigenvalue: entry.eigenvalue,
        dimension: entry.dimension,
        role: entry.role,
      })),
      layerDiscoveryApplications: support.operatorApplications,
      reconstructionError: support.reconstructionError,
      gaugeActive,
    },
    nullShell: {
      momentum: nullMomentum,
      divergenceError: nullDivergence,
      traceError: nullTrace,
      screenContrast: contrast,
      nonzeroPhysicalScreen: Math.abs(contrast) > tolerance,
    },
    routeComparison: {
      singlePhysicalLayer,
      directGreenDepth: singlePhysicalLayer ? 1 : support.active.length,
      compensatedGreenDepth: 1,
      directDeclaredCarrierChannels: 9,
      compensatedDeclaredCarrierChannels: 10,
      observableVisibleChannels: activeDimension,
      baselineAdapterIsIdentity,
      samePotentialAndCurvature: singlePhysicalLayer
        && baselineAdapterIsIdentity
        && support.active[0].eigenvalue === 0,
      completeCostVerdict: singlePhysicalLayer && baselineAdapterIsIdentity
        ? 'same-active-response-work; no computational dominance'
        : 'direct route pays layer discovery/separation; compensated route dominates',
    },
  };
}

function compilePreparedSpinTwoResponse(input = {}) {
  const rejectedKey = Object.keys(input).find((key) => answerBearingKeys.has(key));
  if (rejectedKey) {
    return refuse(
      'answer-bearing-input',
      'the prepared-response compiler accepts preparation maps and a capability, not a layer, projector, expected support, or verdict',
      { rejectedKey },
    );
  }
  const { preparations, requestedCapability } = input;
  if (requestedCapability !== 'local-preparation-to-nonzero-screen-response') {
    return refuse(
      'requested-capability',
      'the bounded bench tests a local spin-two preparation, discovered invariant support, and a nonzero null-screen response',
      { requestedCapability },
    );
  }
  if (!Array.isArray(preparations)
      || preparations.length === 0
      || preparations.some((entry) => !entry?.ok || typeof entry.evaluate !== 'function')) {
    return refuse('preparation-interface', 'one or more successfully constructed preparation maps are required');
  }

  const nonnullMomentum = [2, 1, 0, 0];
  const nullMomentum = [1, 0, 0, 1];
  const cases = preparations.map((preparation) =>
    analyzePreparation(preparation, nonnullMomentum, nullMomentum));
  const transfer = cases.find((entry) =>
    entry.routeComparison.singlePhysicalLayer
    && entry.nullShell.nonzeroPhysicalScreen
    && entry.routeComparison.samePotentialAndCurvature);
  const regression = cases.find((entry) => entry.preparation.name === 'N10e-compact-bivector-current');
  const certificates = {
    noLayerReceivedAsInput: true,
    allSourcesGaugeAdmissible: cases.every((entry) => !entry.nonnull.gaugeActive),
    regressionExposesMixedSupport: regression?.nonnull.activeLayers.length > 1,
    localSingleLayerTransferExists: Boolean(transfer),
    transferRetainsNonzeroScreen: Boolean(transfer?.nullShell.nonzeroPhysicalScreen),
    sameObservableRecovered: Boolean(transfer?.routeComparison.samePotentialAndCurvature),
    completeCostGainRejected: transfer?.routeComparison.completeCostVerdict
      === 'same-active-response-work; no computational dominance',
  };
  if (Object.values(certificates).some((value) => !value)) {
    return refuse(
      'prepared-response-certificate',
      'mixed-support regression, single-layer transfer, screen recovery, or whole-route cost certificate failed',
      { cases, certificates },
    );
  }

  return {
    ok: true,
    family: 'prepared-spin-two-response-sector',
    capability: requestedCapability,
    construction: {
      input: 'a local preparation map into symmetric spin-two currents',
      firstCandidate: 'take its harmonic head and test the generated normalized divergence B=R_1 A/Q',
      obstruction: 'conservation of the full current need not survive harmonic projection when its trace is nonzero',
      retainedSelector: 'calculate A j; short-circuit at B j=0 or generate spectral projectors from the N10r spectrum',
      transferRepair: 'change the preparation seed, not the response answer: double divergence of a Weyl-typed compact seed is conserved and trace free by construction',
      output: 'excited invariant layers, quotient response rule, null-screen witness, and complete-cost verdict',
    },
    cases,
    selectedTransfer: transfer.preparation.name,
    certificates,
    verdict: {
      preparationBridge: 'supported',
      computationalGain: 'rejected-against-same-preparation-baseline',
      reason: 'the Weyl-seed preparation naturally produces one physical layer and a nonzero screen, but the compensated adapter is then already the identity and uses the same one scalar Green operation on the same observable-visible sector',
      retainedTool: 'a preparation-to-layer selector that distinguishes mixed support, accepts a local Weyl-seed transfer, and refuses a false carrier-size speedup',
    },
    stop: 'the local spin-two preparation discriminator is closed; re-enter for a preparation where the constrained route changes active solve work, conditioning, or repeated observable recovery, not merely declared carrier size',
  };
}

export {
  compilePreparedSpinTwoResponse,
  constructWeylDoubleDivergencePreparation,
  discoverLayerSupport,
  existingCompactCurrentPreparation,
};

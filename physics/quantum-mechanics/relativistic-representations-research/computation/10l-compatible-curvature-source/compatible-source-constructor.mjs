function refuse(phase, reason, details = {}) {
  return { ok: false, phase, reason, ...details };
}

function curvatureDimension(spin) {
  return 4 * spin + 2;
}

function directSourceDimension(spin) {
  return 8 * spin;
}

function compatibilityDimension(spin) {
  return 4 * spin - 2;
}

function potentialDimension(spin) {
  return 2 * spin * spin + 2;
}

function minimalLiftTrace(spin, maximumDegree) {
  return Array.from({ length: maximumDegree + 1 }, (_, degree) => ({
    degree,
    multiplicity: degree < spin - 1 ? 0 : (degree === spin - 1 ? 1 : null),
    reason: degree < spin - 1
      ? 'the source and momentum left weights cannot reach spin s-1/2'
      : 'the highest left channel and lowest right channel each occur once',
  }));
}

function validateInput(input) {
  if (!Number.isInteger(input.spin) || input.spin < 1) {
    return refuse('physical-target', 'spin must be a positive integer');
  }
  if (!input.curvaturePacket?.ok || input.curvaturePacket.spin !== input.spin) {
    return refuse(
      'curvature-packet',
      'N10j curvature output for the same spin is required',
      { requestedSpin: input.spin, packetSpin: input.curvaturePacket?.spin ?? null },
    );
  }
  if (!input.sourcedTransportPacket?.ok
      || input.sourcedTransportPacket.spin !== input.spin) {
    return refuse(
      'sourced-transport',
      'N10k sourced transport for the same spin is required',
      {
        requestedSpin: input.spin,
        packetSpin: input.sourcedTransportPacket?.spin ?? null,
      },
    );
  }
  const resources = input.resources ?? {};
  const missingResources = [
    ...(!resources.alternatingSpinorForms ? ['alternatingSpinorForms'] : []),
    ...(!resources.symmetricAlgebra ? ['symmetricAlgebra'] : []),
    ...(!resources.scalarCausalGreen ? ['scalarCausalGreen'] : []),
  ];
  if (missingResources.length > 0) {
    return refuse(
      'direct-complex-resources',
      'the spinor differential complex and causal factorization lack resources',
      { missingResources },
    );
  }
  return null;
}

function normalizeSourceRoute(route, sourceConstraint = true) {
  const output = [...route];
  const trace = [{ rule: 'input', route: [...output] }];
  let changed = true;
  while (changed) {
    changed = false;
    for (let index = 0; index < output.length - 1; index += 1) {
      const pair = `${output[index]} ${output[index + 1]}`;
      if (pair === 'G_E B') {
        output.splice(index, 2, 'B', 'G_Curv');
      } else if (pair === 'L B') {
        output.splice(index, 2, 'K');
      } else if (pair === 'L Y') {
        output.splice(index, 2, sourceConstraint ? 'ZERO' : 'N_C');
      } else {
        continue;
      }
      trace.push({ rule: pair, route: [...output] });
      changed = true;
      break;
    }
  }
  if (output.some((token) => token === 'ZERO')) return { normalForm: ['ZERO'], trace };
  return { normalForm: output, trace };
}

function constructCompatibleCurvatureSource(input = {}) {
  const invalid = validateInput(input);
  if (invalid) return invalid;

  const spin = input.spin;
  const maximumDegree = input.maxLiftDerivativeOrder ?? spin - 1;
  if (!Number.isInteger(maximumDegree) || maximumDegree < 0) {
    return refuse(
      'lift-derivative-budget',
      'maxLiftDerivativeOrder must be a nonnegative integer',
      { maximumDegree },
    );
  }
  const multiplicityTrace = minimalLiftTrace(spin, maximumDegree);
  if (maximumDegree < spin - 1) {
    return refuse(
      'source-lift-degree',
      'the derivative budget cannot reach the direct chiral source carrier',
      {
        spin,
        requiredDerivativeOrder: spin - 1,
        maximumDegree,
        multiplicityTrace,
      },
    );
  }

  const directRoute = ['L', 'G_E', 'B'];
  const transportedRoute = ['K', 'G_Curv'];
  const normalizedDirect = normalizeSourceRoute(directRoute, true);
  const normalizedTransport = normalizeSourceRoute(transportedRoute, true);
  const compatibilityRoute = normalizeSourceRoute(['L', 'Y'], true);

  return {
    ok: true,
    family: 'compatible-direct-chiral-source-complex',
    spin,
    carriers: {
      curvature: {
        type: `Sym^${2 * spin}(S) direct-sum Sym^${2 * spin}(bar S)`,
        dimension: curvatureDimension(spin),
      },
      directSource: {
        type: [
          `Sym^${2 * spin - 1}(S) tensor bar S`,
          `S tensor Sym^${2 * spin - 1}(bar S)`,
        ].join(' direct-sum '),
        dimension: directSourceDimension(spin),
      },
      compatibility: {
        type: `Sym^${Math.max(0, 2 * spin - 2)}(S) direct-sum Sym^${Math.max(0, 2 * spin - 2)}(bar S)`,
        dimension: compatibilityDimension(spin),
      },
    },
    directComplex: {
      sequence: 'Curv_s --Z_s--> E_s^curv --Y_s--> I_s^curv',
      equation: 'Z_s is the N4 first-order zero-rest-mass symbol',
      compatibility: 'Y_s converts the primed source index with momentum and contracts its antisymmetric remainder',
      backOperation: 'B_s symmetrically reinserts the converted source index with normalization 1/(2s)',
      identities: [
        'Y_s Z_s=0',
        'B_s Z_s=Q identity_Curv',
        'Z_s B_s=Q identity_E modulo the compatibility image',
        'Y_s j=0 implies Z_s B_s j=Q j',
      ],
      exactness: 'at non-null momentum, ker Y_s=im Z_s by the symmetric-plus-hook decomposition',
    },
    sourceLift: {
      derivativeOrder: spin - 1,
      multiplicityTrace,
      operation: [
        `L_${spin} applies ${spin - 1} chiral momentum contractions`,
        'to the traceless source layer and leaves one primed index',
      ].join(' '),
      input: 'adapted compact potential source S with C_s S=0',
      output: 'j_s=L_s S in ker Y_s',
      generatedSyzygies: [
        'Y_s L_s=N_s C_s',
        'B_s L_s=K_s',
      ],
      constrainedConsequences: [
        'Y_s L_s S=0',
        'B_s L_s S=K_s S',
        'Z_s K_s S=Q L_s S',
      ],
    },
    greenOperation: {
      retarded: 'G_Z^+ j=B_s G_Q^+ j',
      advanced: 'G_Z^- j=B_s G_Q^- j',
      inputConstraint: 'Y_s j=0',
      certificates: [
        'Z_s G_Z^+/- j=j',
        'G_Z^+/- Z_s phi=phi for compact phi',
        'causal support follows because B_s is differential',
      ],
    },
    sameOutput: {
      directRoute,
      transportedRoute,
      normalizedDirect,
      normalizedTransport,
      equal: normalizedDirect.normalForm.join(' ')
        === normalizedTransport.normalForm.join(' '),
      compatibilityRoute,
    },
    costs: {
      potentialFirstGreenChannels: potentialDimension(spin),
      curvatureTransportGreenChannels: curvatureDimension(spin),
      directCompatibleSourceGreenChannels: directSourceDimension(spin),
      sourceLiftDerivativeOrder: spin - 1,
      backOperationDerivativeOrder: 1,
      verdict: [
        'the independent first-order route propagates more channels than curvature transport;',
        'commuting B_s before G_Q collapses it exactly to the N10k route',
      ].join(' '),
    },
    boundary: {
      supported: [
        'compatible direct-curvature source carrier, retarded/advanced Green operation,',
        'potential-source lift, and same-output equality',
      ].join(' '),
      unsupported: [
        'a new external physical meaning for arbitrary compatible chiral sources,',
        'a cheaper computation, interactions, curved backgrounds, and countable spin',
      ].join(' '),
    },
  };
}

export {
  compatibilityDimension,
  constructCompatibleCurvatureSource,
  curvatureDimension,
  directSourceDimension,
  minimalLiftTrace,
  normalizeSourceRoute,
  potentialDimension,
};

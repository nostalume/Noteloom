function refuse(phase, reason, details = {}) {
  return { ok: false, phase, reason, ...details };
}

function potentialDimension(spin) {
  return 2 * spin * spin + 2;
}

function curvatureDimension(spin) {
  return 4 * spin + 2;
}

function directEquationDimension(spin) {
  return 8 * spin;
}

function classifyChannelLoad(spin) {
  const potentialChannels = potentialDimension(spin);
  const curvatureChannels = curvatureDimension(spin);
  if (curvatureChannels < potentialChannels) return 'curvature-transport-has-fewer-scalar-Green-channels';
  if (curvatureChannels === potentialChannels) return 'equal-scalar-Green-channel-load';
  return 'potential-first-has-fewer-scalar-Green-channels';
}

function validateInput(input) {
  if (!Number.isInteger(input.spin) || input.spin < 1) {
    return refuse('physical-target', 'spin must be a positive integer');
  }
  if (!input.fieldSystemResult?.ok || !input.fieldSystemResult.fieldSystem) {
    return refuse('potential-system', 'a generated symmetric-potential FieldSystem is required');
  }
  if (!input.sourceAdapterResult?.ok || !input.sourceAdapterResult.sourceInterface) {
    return refuse('source-adapter', 'the generated pairing-compatible source adapter is required');
  }
  if (!input.curvaturePacket?.ok || input.curvaturePacket.spin !== input.spin) {
    return refuse(
      'curvature-compatibility',
      'a generated curvature packet for the same spin is required',
      { requestedSpin: input.spin, packetSpin: input.curvaturePacket?.spin ?? null },
    );
  }
  const green = input.greenResources ?? {};
  const missingResources = [
    ...(!green.scalarWaveRetardedAdvanced ? ['scalarWaveRetardedAdvanced'] : []),
    ...(!green.translationInvariantConvolution ? ['translationInvariantConvolution'] : []),
    ...(!green.causalExactSequence ? ['causalExactSequence'] : []),
  ];
  if (missingResources.length > 0) {
    return refuse(
      'green-resources',
      'scalar retarded/advanced convolution and its causal exact sequence are required',
      { missingResources },
    );
  }
  return null;
}

function rewriteRoute(route) {
  const output = [...route];
  const trace = [{ rule: 'input', route: [...output] }];
  let changed = true;
  while (changed) {
    changed = false;
    for (let index = 0; index < output.length - 1; index += 1) {
      const pair = `${output[index]} ${output[index + 1]}`;
      if (pair === 'G_F+ K') {
        output.splice(index, 2, 'K', 'G_C+');
      } else if (pair === 'G_F- K') {
        output.splice(index, 2, 'K', 'G_C-');
      } else if (pair === 'Delta_F K') {
        output.splice(index, 2, 'K', 'Delta_C');
      } else if (pair === 'D K') {
        output.splice(index, 2, 'K', 'Q');
      } else if (pair === 'Q Delta_C') {
        output.splice(index, 2, 'ZERO');
      } else {
        continue;
      }
      trace.push({ rule: pair, route: [...output] });
      changed = true;
      break;
    }
  }
  if (output.includes('ZERO')) return { normalForm: ['ZERO'], trace };
  return { normalForm: output, trace };
}

function constructSourcedCurvatureUse(input = {}) {
  const invalid = validateInput(input);
  if (invalid) return invalid;

  const spin = input.spin;
  if (input.requiredCapability === 'independent-direct-curvature-source-green') {
    return refuse(
      'direct-curvature-source-interface',
      'the first-order chiral equation has no right inverse on arbitrary equation sources',
      {
        spin,
        curvatureCarrierDimension: curvatureDimension(spin),
        directEquationCarrierDimension: directEquationDimension(spin),
        pointwiseSurjectivityDefect: directEquationDimension(spin) - curvatureDimension(spin),
        missingConstruction: 'a compatible source carrier and an identity relating the direct chiral operator to K_s',
      },
    );
  }

  const route = (prescription) => {
    const suffix = prescription === 'retarded' ? '+' : '-';
    const potentialFirst = ['MInv', `G_F${suffix}`, 'K'];
    const curvatureTransportFirst = ['MInv', 'K', `G_C${suffix}`];
    const normalizedPotential = rewriteRoute(potentialFirst);
    const normalizedTransport = rewriteRoute(curvatureTransportFirst);
    return {
      prescription,
      potentialFirst,
      curvatureTransportFirst,
      normalizedPotential,
      normalizedTransport,
      equal: normalizedPotential.normalForm.join(' ') === normalizedTransport.normalForm.join(' '),
    };
  };

  const causalPotentialFirst = ['MInv', 'Delta_F', 'K'];
  const causalTransportFirst = ['MInv', 'K', 'Delta_C'];
  const causalSourceShift = ['D', 'K', 'Delta_C'];
  const normalizedCausalPotential = rewriteRoute(causalPotentialFirst);
  const normalizedCausalTransport = rewriteRoute(causalTransportFirst);
  const normalizedSourceShift = rewriteRoute(causalSourceShift);
  const costs = {
    shared: {
      sourceAdapterOrder: 0,
      curvatureDerivativeOrder: input.curvaturePacket.derivativeOrder,
      scalarGreenApplications: 1,
    },
    potentialFirst: { scalarGreenChannels: potentialDimension(spin) },
    curvatureTransportFirst: { scalarGreenChannels: curvatureDimension(spin) },
    channelVerdict: classifyChannelLoad(spin),
    boundary: [
      'channel count is not runtime: constructing K_s, regularity loss,',
      'conditioning, support representation, and observable recovery remain payable',
    ].join(' '),
  };

  return {
    ok: true,
    family: 'potential-derived-sourced-curvature-transport',
    spin,
    provenance: [
      input.sourceAdapterResult.capability,
      input.curvaturePacket.provenance,
      'translation-invariant scalar causal Green operation',
    ],
    operation: {
      input: 'compact conserved physical current J with R^dagger J=0',
      adapt: 'S=M_s^(-1)J',
      retarded: 'C_J^+=K_s G_(F,s)^+ S=G_(C,s)^+ K_s S',
      advanced: 'C_J^-=K_s G_(F,s)^- S=G_(C,s)^- K_s S',
      causal: '[J] maps to Delta_(C,s) K_s M_s^(-1)J',
      waveEquation: 'Q C_J^+/-=K_s S',
    },
    compareRoutes: route,
    certificates: {
      retardedRouteEquality: route('retarded'),
      advancedRouteEquality: route('advanced'),
      causalRouteEquality: {
        potentialFirst: causalPotentialFirst,
        curvatureTransportFirst: causalTransportFirst,
        normalizedPotential: normalizedCausalPotential,
        normalizedTransport: normalizedCausalTransport,
        equal: normalizedCausalPotential.normalForm.join(' ')
          === normalizedCausalTransport.normalForm.join(' '),
      },
      causalSourceQuotient: {
        shift: 'J -> J+E a implies S -> S+D a',
        route: causalSourceShift,
        normalized: normalizedSourceShift,
        vanishes: normalizedSourceShift.normalForm.length === 1
          && normalizedSourceShift.normalForm[0] === 'ZERO',
        identities: ['K_s D_s=Q K_s', 'Delta_C Q=0'],
      },
      support: 'K_s is differential and preserves compact support; G^+/- then gives retarded/advanced causal support',
      shell: 'N10j makes K_s an isomorphism on the two physical null-screen lines',
    },
    costs,
    directCurvatureCompletion: refuse(
      'direct-curvature-source-interface',
      [
        'the transported scalar-wave response is not an independently generated',
        'Green complex for the first-order chiral equation',
      ].join(' '),
      {
        curvatureCarrierDimension: curvatureDimension(spin),
        directEquationCarrierDimension: directEquationDimension(spin),
        pointwiseSurjectivityDefect: directEquationDimension(spin) - curvatureDimension(spin),
        missingConstruction: [
          'compatible curvature sources plus an off-shell intertwining identity',
          'for the direct chiral operator',
        ].join(' '),
      },
    ),
    boundary: {
      supported: [
        'same sourced curvature output by potential-first and curvature-transport-first',
        'scalar-wave routes, including the causal source quotient',
      ].join(' '),
      unsupported: [
        'independent first-order curvature-source Green theory, total runtime',
        'reduction, interactions, and curved backgrounds',
      ].join(' '),
    },
  };
}

export {
  classifyChannelLoad,
  constructSourcedCurvatureUse,
  curvatureDimension,
  directEquationDimension,
  potentialDimension,
  rewriteRoute,
};

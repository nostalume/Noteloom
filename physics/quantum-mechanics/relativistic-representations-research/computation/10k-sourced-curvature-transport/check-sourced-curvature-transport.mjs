import { pathToFileURL } from 'node:url';

import { constructBosonicFieldSystem } from '../10c-generative-residual-constructor/residual-constructor.mjs';
import { constructBosonicSourceAdapter } from '../10e-generated-source-adapter/source-adapter-constructor.mjs';
import { constructCarrierGrammar } from '../10h-carrier-to-grammar/carrier-grammar-constructor.mjs';
import {
  constructCurvatureCompatibility,
} from '../10j-generated-curvature-compatibility/curvature-compatibility-constructor.mjs';
import {
  constructSourcedCurvatureUse,
  curvatureDimension,
  directEquationDimension,
  potentialDimension,
} from './sourced-curvature-constructor.mjs';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const grammar = constructCarrierGrammar({
  presentation: { functor: 'symmetric-power', coefficientModule: 'scalar' },
  resources: {
    symmetricAlgebra: true,
    metric: { invariant: true, nondegenerate: true, symmetric: true },
  },
});
const fieldSystemResult = constructBosonicFieldSystem({
  grammarPacket: grammar,
  maxTraceDepth: 1,
});
const sourceAdapterResult = constructBosonicSourceAdapter({ fieldSystemResult });
const curvatureResources = Object.freeze({
  symmetricAlgebra: true,
  chiralBivectorSplit: true,
  alternatingForms: { left: true, right: true },
});
const greenResources = Object.freeze({
  scalarWaveRetardedAdvanced: true,
  translationInvariantConvolution: true,
  causalExactSequence: true,
});

function curvaturePacket(spin) {
  return constructCurvatureCompatibility({
    spin,
    potentialSystem: fieldSystemResult,
    resources: curvatureResources,
  });
}

function build(spin, overrides = {}) {
  return constructSourcedCurvatureUse({
    spin,
    fieldSystemResult,
    sourceAdapterResult,
    curvaturePacket: curvaturePacket(spin),
    greenResources,
    ...overrides,
  });
}

function run() {
  assert(grammar.ok && fieldSystemResult.ok && sourceAdapterResult.ok,
    'upstream generated source system failed');

  const missingGreen = build(2, { greenResources: { scalarWaveRetardedAdvanced: true } });
  assert(!missingGreen.ok && missingGreen.phase === 'green-resources',
    'missing commutation/exact-sequence resources must refuse');

  const mismatchedCurvature = build(2, { curvaturePacket: curvaturePacket(3) });
  assert(!mismatchedCurvature.ok && mismatchedCurvature.phase === 'curvature-compatibility',
    'a curvature packet for the wrong spin must refuse');

  const directRefusal = build(2, { requiredCapability: 'independent-direct-curvature-source-green' });
  assert(!directRefusal.ok && directRefusal.pointwiseSurjectivityDefect === 6,
    'arbitrary direct-curvature source Green request must expose the spin-two rank defect');

  const rows = [];
  for (let spin = 1; spin <= 6; spin += 1) {
    const result = build(spin);
    assert(result.ok, `spin-${spin} sourced-curvature construction refused`);
    assert(result.certificates.retardedRouteEquality.equal,
      `spin-${spin} retarded routes did not normalize to one operation`);
    assert(result.certificates.advancedRouteEquality.equal,
      `spin-${spin} advanced routes did not normalize to one operation`);
    assert(result.certificates.causalRouteEquality.equal,
      `spin-${spin} causal routes did not normalize to one operation`);
    assert(result.certificates.causalSourceQuotient.vanishes,
      `spin-${spin} causal output failed to descend through equation-source shifts`);
    assert(result.costs.potentialFirst.scalarGreenChannels === potentialDimension(spin),
      `spin-${spin} potential dimension mismatch`);
    assert(result.costs.curvatureTransportFirst.scalarGreenChannels === curvatureDimension(spin),
      `spin-${spin} curvature dimension mismatch`);
    assert(result.directCurvatureCompletion.pointwiseSurjectivityDefect
      === directEquationDimension(spin) - curvatureDimension(spin),
    `spin-${spin} direct-equation obstruction mismatch`);
    rows.push({
      spin,
      derivativeOrder: result.costs.shared.curvatureDerivativeOrder,
      potentialGreenChannels: result.costs.potentialFirst.scalarGreenChannels,
      curvatureGreenChannels: result.costs.curvatureTransportFirst.scalarGreenChannels,
      channelVerdict: result.costs.channelVerdict,
      directSourceDefect: result.directCurvatureCompletion.pointwiseSurjectivityDefect,
    });
  }

  const spinTwo = build(2);
  assert(spinTwo.costs.channelVerdict === 'equal-scalar-Green-channel-load',
    'the actual spin-two source bench must not claim channel compression');
  const spinThree = build(3);
  assert(spinThree.costs.channelVerdict
    === 'curvature-transport-has-fewer-scalar-Green-channels',
  'spin three should be the first formal channel-load reduction');

  console.table(rows);
  console.log(JSON.stringify({
    spinTwoOperation: spinTwo.operation,
    spinTwoCausalCertificate: spinTwo.certificates.causalSourceQuotient,
    directCurvatureRefusal: directRefusal,
  }, null, 2));
  console.log('generated sourced-curvature transport checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

export { build, greenResources, run };

import { pathToFileURL } from 'node:url';

import { constructBosonicFieldSystem } from '../10c-generative-residual-constructor/residual-constructor.mjs';
import { constructBosonicSourceAdapter } from '../10e-generated-source-adapter/source-adapter-constructor.mjs';
import { constructCarrierGrammar } from '../10h-carrier-to-grammar/carrier-grammar-constructor.mjs';
import { constructCurvatureCompatibility } from '../10j-generated-curvature-compatibility/curvature-compatibility-constructor.mjs';
import { constructSourcedCurvatureUse } from '../10k-sourced-curvature-transport/sourced-curvature-constructor.mjs';
import {
  compatibilityDimension,
  constructCompatibleCurvatureSource,
  curvatureDimension,
  directSourceDimension,
  potentialDimension,
} from './compatible-source-constructor.mjs';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function add(left, right) {
  return left.map((value, index) => value + right[index]);
}

function scale(scalar, polynomial) {
  return polynomial.map((value) => scalar * value);
}

function derivativeX(polynomial) {
  const degree = polynomial.length - 1;
  return polynomial.slice(0, -1).map((coefficient, yPower) =>
    coefficient * (degree - yPower));
}

function derivativeY(polynomial) {
  return polynomial.slice(1).map((coefficient, index) =>
    coefficient * (index + 1));
}

function multiplyX(polynomial) {
  return [...polynomial, 0];
}

function multiplyY(polynomial) {
  return [0, ...polynomial];
}

function maximumError(left, right) {
  return Math.max(...left.map((value, index) => Math.abs(value - right[index])));
}

function applyMatrix(matrix, vector) {
  return [
    add(scale(matrix[0][0], vector[0]), scale(matrix[0][1], vector[1])),
    add(scale(matrix[1][0], vector[0]), scale(matrix[1][1], vector[1])),
  ];
}

function directEquation(polynomial, momentumTranspose) {
  return applyMatrix(momentumTranspose, [derivativeX(polynomial), derivativeY(polynomial)]);
}

function adjugate(matrix) {
  return [[matrix[1][1], -matrix[0][1]], [-matrix[1][0], matrix[0][0]]];
}

function determinant(matrix) {
  return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
}

function compatibility(source, momentumTranspose) {
  const converted = applyMatrix(adjugate(momentumTranspose), source);
  return add(derivativeY(converted[0]), scale(-1, derivativeX(converted[1])));
}

function backOperation(source, momentumTranspose, degree) {
  const converted = applyMatrix(adjugate(momentumTranspose), source);
  return scale(1 / degree, add(multiplyX(converted[0]), multiplyY(converted[1])));
}

const grammar = constructCarrierGrammar({
  presentation: { functor: 'symmetric-power', coefficientModule: 'scalar' },
  resources: {
    symmetricAlgebra: true,
    metric: { invariant: true, nondegenerate: true, symmetric: true },
  },
});
const fieldSystemResult = constructBosonicFieldSystem({ grammarPacket: grammar });
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
const directResources = Object.freeze({
  alternatingSpinorForms: true,
  symmetricAlgebra: true,
  scalarCausalGreen: true,
});

function curvaturePacket(spin) {
  return constructCurvatureCompatibility({
    spin,
    potentialSystem: fieldSystemResult,
    resources: curvatureResources,
  });
}

function transportPacket(spin, packet = curvaturePacket(spin)) {
  return constructSourcedCurvatureUse({
    spin,
    fieldSystemResult,
    sourceAdapterResult,
    curvaturePacket: packet,
    greenResources,
  });
}

function build(spin, overrides = {}) {
  const curvature = curvaturePacket(spin);
  return constructCompatibleCurvatureSource({
    spin,
    curvaturePacket: curvature,
    sourcedTransportPacket: transportPacket(spin, curvature),
    resources: directResources,
    ...overrides,
  });
}

function checkDirectComplex(spin) {
  const degree = 2 * spin;
  const polynomial = Array.from({ length: degree + 1 }, (_, index) =>
    (index + 1) * (index % 2 === 0 ? 1 : -2));
  const momentumTranspose = [[2, 1], [1, 1]];
  const q = determinant(momentumTranspose);
  const source = directEquation(polynomial, momentumTranspose);
  const compatibilityResidual = compatibility(source, momentumTranspose);
  const recoveredCurvature = backOperation(source, momentumTranspose, degree);
  const sourceRecovered = directEquation(recoveredCurvature, momentumTranspose);
  const expectedCurvature = scale(q, polynomial);
  const expectedSource = source.map((component) => scale(q, component));

  assert(Math.max(...compatibilityResidual.map(Math.abs)) < 1e-10,
    `spin-${spin} direct equation did not land in the compatible source kernel`);
  assert(maximumError(recoveredCurvature, expectedCurvature) < 1e-10,
    `spin-${spin} B Z=Q identity failed`);
  assert(Math.max(
    maximumError(sourceRecovered[0], expectedSource[0]),
    maximumError(sourceRecovered[1], expectedSource[1]),
  ) < 1e-10, `spin-${spin} Z B=Q identity failed on a compatible source`);

  const incompatible = [
    Array.from({ length: degree }, (_, index) => index + 1),
    Array(degree).fill(0),
  ];
  const incompatibilityWitness = compatibility(incompatible, momentumTranspose);
  assert(Math.max(...incompatibilityWitness.map(Math.abs)) > 1e-6,
    `spin-${spin} incompatibility witness was not refused by Y`);
  return {
    spin,
    degree,
    compatibilityError: Math.max(...compatibilityResidual.map(Math.abs)),
    curvatureRecoveryError: maximumError(recoveredCurvature, expectedCurvature),
    incompatibleSourceWitness: Math.max(...incompatibilityWitness.map(Math.abs)),
  };
}

function run() {
  assert(grammar.ok && fieldSystemResult.ok && sourceAdapterResult.ok,
    'upstream generated potential/source system failed');

  const missingResources = build(2, { resources: { symmetricAlgebra: true } });
  assert(!missingResources.ok && missingResources.phase === 'direct-complex-resources',
    'missing spinor/Green resources must refuse');

  const insufficientLift = build(3, { maxLiftDerivativeOrder: 1 });
  assert(!insufficientLift.ok && insufficientLift.requiredDerivativeOrder === 2,
    'a source-lift budget below s-1 must refuse');

  const directChecks = [];
  const rows = [];
  for (let spin = 1; spin <= 6; spin += 1) {
    const packet = build(spin);
    assert(packet.ok, `spin-${spin} compatible-source constructor refused`);
    assert(packet.sameOutput.equal,
      `spin-${spin} direct and transported routes did not normalize equally`);
    assert(packet.sameOutput.compatibilityRoute.normalForm[0] === 'ZERO',
      `spin-${spin} lifted source did not normalize into ker Y`);
    assert(packet.sourceLift.derivativeOrder === spin - 1,
      `spin-${spin} source lift has wrong minimal derivative degree`);
    assert(packet.carriers.curvature.dimension === curvatureDimension(spin),
      `spin-${spin} curvature carrier dimension mismatch`);
    assert(packet.carriers.directSource.dimension === directSourceDimension(spin),
      `spin-${spin} direct source carrier dimension mismatch`);
    assert(packet.carriers.compatibility.dimension === compatibilityDimension(spin),
      `spin-${spin} compatibility carrier dimension mismatch`);
    directChecks.push(checkDirectComplex(spin));
    rows.push({
      spin,
      liftOrder: packet.sourceLift.derivativeOrder,
      potentialChannels: potentialDimension(spin),
      curvatureChannels: curvatureDimension(spin),
      directSourceChannels: directSourceDimension(spin),
      compatibilityConditions: compatibilityDimension(spin),
    });
  }

  console.table(rows);
  console.table(directChecks);
  console.log(JSON.stringify({
    insufficientLift,
    spinTwo: build(2),
  }, null, 2));
  console.log('compatible direct-curvature source checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

export {
  backOperation,
  build,
  compatibility,
  directEquation,
  run,
};

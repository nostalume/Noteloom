const tolerance = 1e-11;

function close(actual, expected, scale = 1, label = "value") {
  const error = Math.abs(actual - expected);
  if (error > tolerance * Math.max(1, scale)) {
    throw new Error(`${label}: ${actual} != ${expected}; error=${error}`);
  }
  return error;
}

function norm2(v) {
  return v.reduce((sum, x) => sum + x * x, 0);
}

function scale(a, v) {
  return v.map((x) => a * x);
}

function shellEnergy(mass, momentum) {
  return Math.sqrt(mass * mass + norm2(momentum));
}

function minkowskiSquare(p) {
  return p[0] * p[0] - norm2(p.slice(1));
}

function boostedRestMomentum(mass, rapidity, direction) {
  const spatial = scale(mass * Math.sinh(rapidity), direction);
  return [mass * Math.cosh(rapidity), ...spatial];
}

function fivePointCurvature(mass, direction, step) {
  const energy = (t) => shellEnergy(mass, scale(t, direction));
  return (
    -energy(2 * step)
    + 16 * energy(step)
    - 30 * energy(0)
    + 16 * energy(-step)
    - energy(-2 * step)
  ) / (12 * step * step);
}

const cases = [
  { mass: 2.3, rapidity: 0.7, direction: [1, 0, 0] },
  { mass: 5.1, rapidity: 1.2, direction: [0, 0.6, 0.8] },
  { mass: 0.9, rapidity: 0.35, direction: [2 / 3, -2 / 3, 1 / 3] },
];

let maximumInvariantError = 0;
let maximumShellError = 0;
let maximumRecoveryResidual = 0;
let maximumBoundRatio = 0;

for (const { mass, rapidity, direction } of cases) {
  close(norm2(direction), 1, 1, "unit direction");
  const p = boostedRestMomentum(mass, rapidity, direction);
  const spatial = p.slice(1);
  const expectedEnergy = shellEnergy(mass, spatial);

  maximumInvariantError = Math.max(
    maximumInvariantError,
    close(minkowskiSquare(p), mass * mass, mass * mass, "Minkowski norm"),
  );
  maximumShellError = Math.max(
    maximumShellError,
    close(p[0], expectedEnergy, expectedEnergy, "positive shell energy"),
  );

  const momentum2 = norm2(spatial);
  const kinetic = expectedEnergy - mass;
  const nonrelativistic = momentum2 / (2 * mass);
  const exactCorrection = -(
    momentum2 * momentum2
  ) / (2 * mass * (expectedEnergy + mass) ** 2);
  const residual = kinetic - nonrelativistic - exactCorrection;
  maximumRecoveryResidual = Math.max(
    maximumRecoveryResidual,
    close(residual, 0, Math.abs(kinetic) + 1, "recovery identity"),
  );

  const bound = momentum2 * momentum2 / (8 * mass ** 3);
  const error = Math.abs(kinetic - nonrelativistic);
  if (error > bound * (1 + tolerance)) {
    throw new Error(`quartic bound failed: ${error} > ${bound}`);
  }
  maximumBoundRatio = Math.max(maximumBoundRatio, error / bound);
}

const curvatureMass = 3.7;
const curvatureDirection = [1 / 3, 2 / 3, -2 / 3];
const numericalCurvature = fivePointCurvature(
  curvatureMass,
  curvatureDirection,
  0.02,
);
const exactCurvature = 1 / curvatureMass;
const curvatureError = Math.abs(numericalCurvature - exactCurvature);
if (curvatureError > 2e-9) {
  throw new Error(
    `five-point curvature: ${numericalCurvature} != ${exactCurvature}; error=${curvatureError}`,
  );
}

console.log(JSON.stringify({
  cases: cases.length,
  maximumInvariantError,
  maximumShellError,
  numericalCurvature,
  exactCurvature,
  curvatureError,
  maximumRecoveryResidual,
  maximumBoundRatio,
}, null, 2));

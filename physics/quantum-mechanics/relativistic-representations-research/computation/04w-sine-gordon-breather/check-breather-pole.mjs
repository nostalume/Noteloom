const tolerance = 1e-11;

function close(actual, expected, scale = 1, label = "value") {
  const error = Math.abs(actual - expected);
  if (error > tolerance * Math.max(1, scale)) {
    throw new Error(`${label}: ${actual} != ${expected}; error=${error}`);
  }
  return error;
}

function poleAngle(xi, n) {
  if (!(xi > 0 && xi < 1 && n * xi < 1)) {
    throw new Error(`no physical breather pole for xi=${xi}, n=${n}`);
  }
  return Math.PI * (1 - n * xi);
}

function poleMass(solitonMass, xi, n) {
  return 2 * solitonMass * Math.cos(poleAngle(xi, n) / 2);
}

function spectrumMass(solitonMass, xi, n) {
  return 2 * solitonMass * Math.sin(n * Math.PI * xi / 2);
}

function shellEnergy(mass, momentum) {
  return Math.sqrt(mass * mass + momentum * momentum);
}

function fivePointCurvature(mass, step) {
  const energy = (p) => shellEnergy(mass, p);
  return (
    -energy(2 * step)
    + 16 * energy(step)
    - 30 * energy(0)
    + 16 * energy(-step)
    - energy(-2 * step)
  ) / (12 * step * step);
}

const cases = [
  { solitonMass: 1.7, xi: 0.2 },
  { solitonMass: 2.4, xi: 0.37 },
  { solitonMass: 0.9, xi: 0.75 },
];

let polesChecked = 0;
let maximumPoleMassError = 0;
let minimumFirstBreatherStabilityGap = Infinity;

for (const { solitonMass, xi } of cases) {
  const masses = [];
  for (let n = 1; n * xi < 1; n += 1) {
    const u = poleAngle(xi, n);
    const fromPole = poleMass(solitonMass, xi, n);
    const fromSpectrum = spectrumMass(solitonMass, xi, n);
    const invariantAtPole = 4 * solitonMass ** 2 * Math.cos(u / 2) ** 2;

    maximumPoleMassError = Math.max(
      maximumPoleMassError,
      close(fromPole, fromSpectrum, solitonMass, "pole/spectrum mass"),
      close(invariantAtPole, fromSpectrum ** 2, fromSpectrum ** 2, "pole invariant"),
    );
    if (!(fromPole < 2 * solitonMass)) {
      throw new Error(`breather ${n} is not below constituent threshold`);
    }
    masses.push(fromPole);
    polesChecked += 1;
  }

  for (let i = 1; i < masses.length; i += 1) {
    if (!(masses[i] > masses[i - 1])) {
      throw new Error(`breather masses are not increasing for xi=${xi}`);
    }
  }

  const first = masses[0];
  const stabilityGap = Math.min(2 * solitonMass, 2 * first) - first;
  if (!(stabilityGap > 0)) {
    throw new Error(`first-breather stability gap is not positive for xi=${xi}`);
  }
  minimumFirstBreatherStabilityGap = Math.min(
    minimumFirstBreatherStabilityGap,
    stabilityGap,
  );
}

const benchmarkSolitonMass = 1;
const benchmarkXi = 0.5;
const benchmarkMass = poleMass(benchmarkSolitonMass, benchmarkXi, 1);
close(benchmarkMass, Math.SQRT2, Math.SQRT2, "xi=1/2 mass");
const numericalCurvature = fivePointCurvature(benchmarkMass, 0.005);
const exactCurvature = 1 / benchmarkMass;
const curvatureError = Math.abs(numericalCurvature - exactCurvature);
if (curvatureError > 2e-9) {
  throw new Error(`shell curvature error=${curvatureError}`);
}

const shallowXi = 0.999;
const shallowU = poleAngle(shallowXi, 1);
const shallowMass = poleMass(1, shallowXi, 1);
const binding = 2 - shallowMass;
const kappa = Math.sin(shallowU / 2);
const exactBinding = 2 * kappa ** 2 / (1 + Math.cos(shallowU / 2));
close(binding, exactBinding, binding, "exact shallow binding");
const mechanicalRecoveryRatio = binding / (kappa ** 2);
if (Math.abs(mechanicalRecoveryRatio - 1) > 1e-6) {
  throw new Error(`shallow mechanical recovery ratio=${mechanicalRecoveryRatio}`);
}

console.log(JSON.stringify({
  cases: cases.length,
  polesChecked,
  maximumPoleMassError,
  minimumFirstBreatherStabilityGap,
  benchmark: {
    xi: benchmarkXi,
    solitonMass: benchmarkSolitonMass,
    breatherMass: benchmarkMass,
    binding: 2 - benchmarkMass,
    numericalCurvature,
    exactCurvature,
    curvatureError,
  },
  shallowBinding: {
    xi: shallowXi,
    poleAngle: shallowU,
    binding,
    kappa,
    mechanicalRecoveryRatio,
  },
}, null, 2));

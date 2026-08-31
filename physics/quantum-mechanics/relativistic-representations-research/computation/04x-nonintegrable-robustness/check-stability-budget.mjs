const tolerance = 1e-12;

function close(actual, expected, label, scale = 1) {
  const error = Math.abs(actual - expected);
  if (error > tolerance * Math.max(1, scale)) {
    throw new Error(`${label}: ${actual} != ${expected}; error=${error}`);
  }
  return error;
}

function annihilationResidueCoefficient(frequencyRatio, phase, sign) {
  return Math.cos(phase) - Math.cos(phase - sign * 2 * Math.PI * frequencyRatio);
}

function vacuumValue(frequencyRatio, phase, vacuumIndex) {
  return Math.cos(2 * Math.PI * frequencyRatio * vacuumIndex + phase);
}

function stabilityBudget(xi, solitonBound, breatherBound) {
  const breatherRatio = 2 * Math.sin(Math.PI * xi / 2);
  const thresholdRatio = Math.min(2, 2 * breatherRatio);
  const gapRatio = thresholdRatio - breatherRatio;
  const coefficient = 2 * Math.max(solitonBound, breatherBound) + breatherBound;
  return {
    breatherRatio,
    thresholdRatio,
    gapRatio,
    coefficient,
    safeEtaRadius: gapRatio / coefficient,
  };
}

const xi = 1 / 5;
const betaSquaredOverPi = (8 * xi) / (1 + xi);
const secondHarmonicScalingDimension = betaSquaredOverPi;
const alphaBetaOverPi = 2 * betaSquaredOverPi;
const breatherCount = Array.from({ length: 20 }, (_, index) => index + 1)
  .filter((n) => n * xi < 1 - tolerance).length;

close(betaSquaredOverPi, 4 / 3, "beta^2/pi");
if (!(secondHarmonicScalingDimension < 2)) {
  throw new Error("second harmonic is not relevant at the benchmark");
}
if (!(alphaBetaOverPi < 4)) {
  throw new Error("two-frequency first-order renormalizability bound failed");
}
if (breatherCount !== 4) {
  throw new Error(`expected four breathers, found ${breatherCount}`);
}

const preservingRatio = 2;
const confiningRatio = 1 / 2;
for (const sign of [-1, 1]) {
  close(
    annihilationResidueCoefficient(preservingRatio, 0, sign),
    0,
    "second-harmonic annihilation residue",
  );
  close(
    annihilationResidueCoefficient(confiningRatio, 0, sign),
    2,
    "half-frequency annihilation residue",
  );
}

const oldVacua = [-2, -1, 0, 1, 2];
const preservingVacuumValues = oldVacua.map((q) =>
  vacuumValue(preservingRatio, 0, q));
const confiningVacuumValues = oldVacua.map((q) =>
  vacuumValue(confiningRatio, 0, q));
for (const value of preservingVacuumValues) {
  close(value, 1, "preserved old-vacuum value");
}
for (let index = 0; index < oldVacua.length; index += 1) {
  close(
    confiningVacuumValues[index],
    (-1) ** oldVacua[index],
    "alternating old-vacuum value",
  );
}

// Fixture bounds exercise the theorem. They are not form-factor data.
const fixture = { solitonBound: 1.25, breatherBound: 0.75 };
const budget = stabilityBudget(xi, fixture.solitonBound, fixture.breatherBound);
const eta = 0.99 * budget.safeEtaRadius;
const shifts = [-1, 1];
let minimumAdversarialGap = Infinity;
for (const solitonSign of shifts) {
  for (const breatherSign of shifts) {
    const solitonRatio = 1
      + solitonSign * fixture.solitonBound * Math.abs(eta);
    const breatherRatio = budget.breatherRatio
      + breatherSign * fixture.breatherBound * Math.abs(eta);
    const gap = Math.min(2 * solitonRatio, 2 * breatherRatio) - breatherRatio;
    minimumAdversarialGap = Math.min(minimumAdversarialGap, gap);
    const lowerBound = budget.gapRatio - budget.coefficient * Math.abs(eta);
    if (gap + tolerance < lowerBound) {
      throw new Error(`adversarial gap ${gap} violates lower bound ${lowerBound}`);
    }
  }
}
if (!(minimumAdversarialGap > 0)) {
  throw new Error("fixture stability gap closed inside the safe radius");
}

const initialOverlap = 0.8;
const overlapChangeBound = 0.79;
if (!(Math.abs(initialOverlap) - overlapChangeBound > 0)) {
  throw new Error("overlap continuity fixture does not preserve access");
}

console.log(JSON.stringify({
  benchmark: {
    xi,
    betaSquaredOverPi,
    secondHarmonicScalingDimension,
    alphaBetaOverPi,
    breatherCount,
    firstBreatherMassRatio: budget.breatherRatio,
    unperturbedStabilityGapRatio: budget.gapRatio,
  },
  localityAudit: {
    preservingFrequencyRatio: preservingRatio,
    preservingVacuumValues,
    confiningFrequencyRatio: confiningRatio,
    confiningVacuumValues,
  },
  fixtureOnly: {
    ...fixture,
    stabilityCoefficient: budget.coefficient,
    safeEtaRadius: budget.safeEtaRadius,
    testedEta: eta,
    minimumAdversarialGap,
  },
  accessFixture: {
    initialOverlap,
    overlapChangeBound,
    guaranteedLowerBound: Math.abs(initialOverlap) - overlapChangeBound,
  },
}, null, 2));

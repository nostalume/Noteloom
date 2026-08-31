#!/usr/bin/env node

const tolerance = 1e-12;

function oscillatorFactorization(mass, omega, hbar) {
  const xCoefficient = Math.sqrt((mass * omega) / (2 * hbar));
  const pCoefficient = 1 / Math.sqrt(2 * mass * hbar * omega);

  return {
    mass,
    omega,
    hbar,
    xSquaredResidual:
      hbar * omega * xCoefficient ** 2 - (mass * omega ** 2) / 2,
    pSquaredResidual:
      hbar * omega * pCoefficient ** 2 - 1 / (2 * mass),
    commutatorNormalizationResidual:
      2 * hbar * xCoefficient * pCoefficient - 1,
  };
}

function inverseSquareBrackets({ x, p, mass, coupling }) {
  const hamiltonian = p ** 2 / (2 * mass) + coupling / x ** 2;
  const dilation = (x * p) / 2;
  const conformal = (mass * x ** 2) / 2;

  const dHdx = (-2 * coupling) / x ** 3;
  const dHdp = p / mass;
  const dDdx = p / 2;
  const dDdp = x / 2;
  const dKdx = mass * x;
  const dKdp = 0;

  const poisson = (dFdx, dFdp, dGdx, dGdp) =>
    dFdx * dGdp - dFdp * dGdx;

  return {
    x,
    p,
    mass,
    coupling,
    dilationHamiltonianResidual:
      poisson(dDdx, dDdp, dHdx, dHdp) - hamiltonian,
    dilationConformalResidual:
      poisson(dDdx, dDdp, dKdx, dKdp) + conformal,
    hamiltonianConformalResidual:
      poisson(dHdx, dHdp, dKdx, dKdp) + 2 * dilation,
  };
}

function positiveCubicRoot(lambda) {
  const polynomial = (alpha) => alpha ** 3 - alpha - 6 * lambda;
  let lower = 1;
  let upper = Math.max(2, 1 + 2 * Math.cbrt(6 * lambda));
  while (polynomial(upper) < 0) upper *= 2;

  for (let iteration = 0; iteration < 200; iteration += 1) {
    const midpoint = (lower + upper) / 2;
    if (polynomial(midpoint) > 0) upper = midpoint;
    else lower = midpoint;
  }
  return (lower + upper) / 2;
}

function quarticGaussian(lambda) {
  const alpha = positiveCubicRoot(lambda);
  const energy = alpha / 4 + 1 / (4 * alpha) + (3 * lambda) / (4 * alpha ** 2);
  return {
    lambda,
    optimizedWidth: alpha,
    variationalUpperBound: energy,
    stationarityResidual: alpha ** 3 - alpha - 6 * lambda,
  };
}

const oscillatorResults = [
  oscillatorFactorization(1, 1, 1),
  oscillatorFactorization(2, 3, 0.5),
  oscillatorFactorization(0.7, 4.2, 1.3),
];

const inverseSquareResults = [
  inverseSquareBrackets({ x: 0.7, p: -1.2, mass: 2, coupling: 0.3 }),
  inverseSquareBrackets({ x: 2.3, p: 0.4, mass: 0.8, coupling: -0.1 }),
  inverseSquareBrackets({ x: 1.1, p: 3.2, mass: 1.7, coupling: 2.5 }),
];

const quarticResults = [0.1, 1, 10].map(quarticGaussian);

console.table(oscillatorResults);
console.table(inverseSquareResults);
console.table(quarticResults);

for (const row of [...oscillatorResults, ...inverseSquareResults]) {
  for (const [key, value] of Object.entries(row)) {
    if (key.endsWith("Residual") && Math.abs(value) > tolerance) {
      throw new Error(`${key} failed with residual ${value}`);
    }
  }
}

for (const row of quarticResults) {
  if (Math.abs(row.stationarityResidual) > tolerance) {
    throw new Error(`quartic stationarity failed for lambda=${row.lambda}`);
  }
}

const unitQuartic = quarticResults.find((row) => row.lambda === 1);
if (
  Math.abs(unitQuartic.optimizedWidth - 2) > tolerance ||
  Math.abs(unitQuartic.variationalUpperBound - 0.8125) > tolerance
) {
  throw new Error("lambda=1 quartic Gaussian check failed");
}

console.log("heterogeneous reduction portfolio checks: pass");

#!/usr/bin/env node

const tolerance = 1e-12;

function powerResidual(alpha, coefficient = 1, radius = 1) {
  const value = coefficient * alpha * (alpha + 1) * radius ** (alpha - 1);
  return value;
}

const powerResults = [];
for (let alpha = -4; alpha <= 4; alpha += 1) {
  powerResults.push({
    alpha,
    obstructionAtUnitRadius: powerResidual(alpha),
    conservedVectorCandidate: Math.abs(powerResidual(alpha)) <= tolerance,
    interpretation:
      alpha === -1
        ? "Coulomb potential"
        : alpha === 0
          ? "constant/free potential"
          : "rejected within the declared vector ansatz",
  });
}

function coulombObstruction(radius, kappa = 2) {
  const first = kappa / radius ** 2;
  const second = -2 * kappa / radius ** 3;
  return radius * second + 2 * first;
}

function oscillatorObstruction(radius, mass = 3, omega = 5) {
  const first = mass * omega ** 2 * radius;
  const second = mass * omega ** 2;
  return radius * second + 2 * first;
}

function yukawaObstruction(radius, kappa = 2, scale = 0.7) {
  const exponential = Math.exp(-scale * radius);
  const first = kappa * exponential * (scale / radius + 1 / radius ** 2);
  const second =
    -kappa * exponential *
    (scale ** 2 / radius + 2 * scale / radius ** 2 + 2 / radius ** 3);
  return radius * second + 2 * first;
}

const radii = [0.5, 1, 2, 4];
const modelResults = radii.map((radius) => ({
  radius,
  coulomb: coulombObstruction(radius),
  oscillator: oscillatorObstruction(radius),
  yukawa: yukawaObstruction(radius),
}));

console.table(powerResults);
console.table(modelResults);

for (const row of modelResults) {
  if (Math.abs(row.coulomb) > tolerance) {
    throw new Error(`Coulomb obstruction did not vanish at r=${row.radius}`);
  }
  if (Math.abs(row.oscillator) <= tolerance) {
    throw new Error(`Oscillator unexpectedly passed at r=${row.radius}`);
  }
  if (Math.abs(row.yukawa) <= tolerance) {
    throw new Error(`Yukawa unexpectedly passed at r=${row.radius}`);
  }
}

const nontrivialPowerSolutions = powerResults
  .filter((row) => row.conservedVectorCandidate && row.alpha !== 0)
  .map((row) => row.alpha);

if (nontrivialPowerSolutions.length !== 1 || nontrivialPowerSolutions[0] !== -1) {
  throw new Error("The bounded power-law search did not isolate Coulomb");
}

console.log("bounded Runge-Lenz vector search: pass");

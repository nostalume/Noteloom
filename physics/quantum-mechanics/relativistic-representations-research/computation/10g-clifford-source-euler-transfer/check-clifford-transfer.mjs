import { pathToFileURL } from 'node:url';

import {
  add,
  basis,
  contractionSymbol,
  identity,
  metric,
  multiply,
  multiplicationSymbol,
  nullspace,
  rank,
  scale,
  vertical,
  zeros,
} from '../04-local-symbol-extension/check-symmetric-potential.mjs';
import {
  fieldConstraint,
  gammaInsertion,
  gammaTrace,
  kronecker,
  momentumClifford,
  spinorRealDimension,
  symbols,
} from '../04b-half-integer-potential/check-spinor-potential.mjs';
import {
  constructCliffordSourceEulerTransfer,
  serializableCliffordTransfer,
} from './clifford-transfer-constructor.mjs';

const tolerance = 1e-8;

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function coefficient(source, key) {
  const value = source.get(key);
  return value ? Number(value.n) / Number(value.d) : 0;
}

function transpose(matrix) {
  if (matrix.length === 0) return [];
  return matrix[0].map((_, column) => matrix.map((row) => row[column]));
}

function maximumAbsolute(matrix) {
  return matrix.reduce((maximum, row) =>
    Math.max(maximum, ...row.map((value) => Math.abs(value))), 0);
}

function factorial(value) {
  let out = 1;
  for (let factor = 2; factor <= value; factor += 1) out *= factor;
  return out;
}

function polynomialFischerGram(degree) {
  const out = zeros(basis(degree).length, basis(degree).length);
  basis(degree).forEach((exponents, index) => {
    out[index][index] = exponents.reduce((value, exponent, direction) =>
      value * factorial(exponent) * metric[direction] ** exponent, 1);
  });
  return out;
}

const spinorDiracGram = [1, 1, -1, -1, 1, 1, -1, -1]
  .map((value, row) => Array.from({ length: spinorRealDimension },
    (_, column) => (row === column ? value : 0)));

function qOf(momentum) {
  return momentum.reduce((sum, value, direction) =>
    sum + metric[direction] * value * value, 0);
}

function multiplierMatrix(rankValue, generated) {
  const dimension = basis(rankValue).length * spinorRealDimension;
  if (rankValue === 0) return identity(dimension);
  const Gamma = gammaTrace(rankValue);
  const YGamma = multiply(gammaInsertion(rankValue - 1), Gamma);
  let Y2Gamma2 = zeros(dimension, dimension);
  if (rankValue >= 2) {
    const Gamma2 = multiply(gammaTrace(rankValue - 1), Gamma);
    const Y2 = multiply(gammaInsertion(rankValue - 1), gammaInsertion(rankValue - 2));
    Y2Gamma2 = multiply(Y2, Gamma2);
  }
  return add(
    identity(dimension),
    scale(coefficient(generated.multiplier, 'Y G'), YGamma),
    scale(coefficient(generated.multiplier, 'Y Y G G'), Y2Gamma2),
  );
}

function completionMatrix(rankValue, momentum) {
  const fieldDimension = basis(rankValue).length * spinorRealDimension;
  const parameterDimension = basis(rankValue - 1).length * spinorRealDimension;
  const Gamma = gammaTrace(rankValue);
  const A = kronecker(contractionSymbol(rankValue, momentum),
    identity(spinorRealDimension));
  const slashLower = kronecker(identity(basis(rankValue - 1).length),
    momentumClifford(momentum));
  const LGamma = multiply(slashLower, Gamma);
  let PGamma2 = zeros(parameterDimension, fieldDimension);
  if (rankValue >= 2) {
    const Gamma2 = multiply(gammaTrace(rankValue - 1), Gamma);
    const PLower = kronecker(multiplicationSymbol(rankValue - 2, momentum),
      identity(spinorRealDimension));
    PGamma2 = multiply(PLower, Gamma2);
  }
  return add(A, scale(-0.5, LGamma), scale(-0.5, PGamma2));
}

function checkRank(generated, rankValue, momentum) {
  const q = qOf(momentum);
  const fieldDimension = basis(rankValue).length * spinorRealDimension;
  const parameterDimension = basis(rankValue - 1).length * spinorRealDimension;
  const { P, S } = symbols(rankValue, momentum);
  const B = completionMatrix(rankValue, momentum);
  const M = multiplierMatrix(rankValue, generated);
  const E = multiply(M, S);
  const fieldBasis = nullspace(fieldConstraint(rankValue), fieldDimension);
  const parameterBasis = nullspace(gammaTrace(rankValue - 1), parameterDimension);
  const fieldGram = kronecker(polynomialFischerGram(rankValue), spinorDiracGram);
  const parameterGram = kronecker(polynomialFischerGram(rankValue - 1), spinorDiracGram);

  const gaugeError = maximumAbsolute(multiply(multiply(S, P), parameterBasis));
  const hyperbolicError = maximumAbsolute(multiply(add(
    multiply(S, S),
    scale(2, multiply(P, B)),
    scale(-q, identity(fieldDimension)),
  ), fieldBasis));
  const bianchiError = maximumAbsolute(multiply(multiply(B, S), fieldBasis));
  const sourceAdjointError = maximumAbsolute(multiply(
    transpose(parameterBasis),
    multiply(add(
      multiply(transpose(P), multiply(fieldGram, M)),
      scale(-1, multiply(parameterGram, B)),
    ), fieldBasis),
  ));
  const restrictedEuler = multiply(transpose(fieldBasis),
    multiply(fieldGram, multiply(E, fieldBasis)));
  const selfAdjointError = maximumAbsolute(add(
    restrictedEuler,
    scale(-1, transpose(restrictedEuler)),
  ));
  const restrictedDimension = fieldBasis.length ? fieldBasis[0].length : 0;
  const multiplierRank = rank(multiply(M, fieldBasis));

  for (const [name, value] of Object.entries({
    gaugeError,
    hyperbolicError,
    bianchiError,
    sourceAdjointError,
    selfAdjointError,
  })) {
    assert(value < tolerance, `${name} failed at rank ${rankValue}: ${value}`);
  }
  assert(multiplierRank === restrictedDimension,
    `generated multiplier is singular at rank ${rankValue}`);
  return {
    tensorRank: rankValue,
    helicity: rankValue + 0.5,
    gaugeError,
    hyperbolicError,
    bianchiError,
    sourceAdjointError,
    selfAdjointError,
  };
}

function checkSourcedUse(generated) {
  const rankValue = 2;
  const momentum = [1, 0.2, -0.1, 0.3];
  const q = qOf(momentum);
  const fieldDimension = basis(rankValue).length * spinorRealDimension;
  const parameterDimension = basis(rankValue - 1).length * spinorRealDimension;
  const { P, S } = symbols(rankValue, momentum);
  const B = completionMatrix(rankValue, momentum);
  const M = multiplierMatrix(rankValue, generated);
  const E = multiply(M, S);
  const admissible = nullspace(vertical(fieldConstraint(rankValue), B), fieldDimension);
  assert(admissible.length > 0 && admissible[0].length > 0,
    'no nonzero adapted Clifford source was constructed');
  const K = admissible.map((row) => [row[0]]);
  const J = multiply(M, K);
  const psi = scale(1 / q, multiply(S, K));
  const physicalSourceError = maximumAbsolute(add(multiply(E, psi), scale(-1, J)));
  const adaptedSourceError = maximumAbsolute(multiply(B, K));

  const parameterBasis = nullspace(gammaTrace(rankValue - 1), parameterDimension);
  const fieldGram = kronecker(polynomialFischerGram(rankValue), spinorDiracGram);
  const conservationError = maximumAbsolute(multiply(
    transpose(parameterBasis),
    multiply(transpose(P), multiply(fieldGram, J)),
  ));
  assert(physicalSourceError < tolerance,
    `generated Clifford Euler response did not recover J: ${physicalSourceError}`);
  assert(adaptedSourceError < tolerance,
    `constructed trace-reversed source is not B-admissible: ${adaptedSourceError}`);
  assert(conservationError < tolerance,
    `constructed physical source is not constrained-conserved: ${conservationError}`);
  return { tensorRank: rankValue, momentum, q, physicalSourceError, adaptedSourceError, conservationError };
}

function run() {
  const generated = constructCliffordSourceEulerTransfer({ maxGammaLayers: 2 });
  assert(generated.ok, `supported Clifford transfer was refused at ${generated.phase ?? 'unknown phase'}`);
  console.log(JSON.stringify(serializableCliffordTransfer(generated), null, 2));
  const checks = [1, 2, 3, 4].flatMap((rankValue) => [
    checkRank(generated, rankValue, [1, 0.2, -0.1, 0.3]),
    checkRank(generated, rankValue, [1, 0, 0, 1]),
  ]);
  console.table(checks);
  console.log(JSON.stringify({ sourcedUse: checkSourcedUse(generated) }, null, 2));
  console.log('generated Clifford source/Euler transfer checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

export { checkRank, checkSourcedUse };

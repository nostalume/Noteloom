import { pathToFileURL } from 'node:url';
import {
  add,
  basis,
  contractionSymbol,
  identity,
  metric,
  metricInsertionSymbol,
  multiply,
  multiplicationSymbol,
  nullspace,
  scale,
  traceSymbol,
  zeros,
} from '../04-local-symbol-extension/check-symmetric-potential.mjs';
import { evaluatePolynomial } from '../10c-generative-residual-constructor/check-residual-constructor.mjs';
import {
  constructBosonicSourceAdapter,
  inverseSourceAdapter,
} from '../10e-generated-source-adapter/source-adapter-constructor.mjs';
import { spinTwoCurrentSymbol } from '../10e-generated-source-adapter/check-generated-source-adapter.mjs';
import {
  constructBosonicEulerOperator,
  serializableEulerOperator,
} from './euler-operator-constructor.mjs';

const tolerance = 1e-8;

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function qOf(momentum) {
  return momentum[0] ** 2
    - momentum.slice(1).reduce((sum, value) => sum + value ** 2, 0);
}

function maximumAbsolute(matrix) {
  return matrix.reduce((maximum, row) =>
    Math.max(maximum, ...row.map((value) => Math.abs(value))), 0);
}

function transpose(matrix) {
  if (matrix.length === 0) return [];
  return matrix[0].map((_, column) => matrix.map((row) => row[column]));
}

function factorial(value) {
  let result = 1;
  for (let factor = 2; factor <= value; factor += 1) result *= factor;
  return result;
}

function fischerPairing(degree) {
  const out = zeros(basis(degree).length, basis(degree).length);
  basis(degree).forEach((exponents, index) => {
    out[index][index] = exponents.reduce((value, exponent, slot) =>
      value * factorial(exponent) * metric[slot] ** exponent, 1);
  });
  return out;
}

function polynomialCoefficient(source, key) {
  const value = source.get(key);
  return value ? Number(value.n) / Number(value.d) : 0;
}

function multiplierMatrix(spin, multiplier) {
  const coefficient = polynomialCoefficient(multiplier, 'U T');
  return add(
    identity(basis(spin).length),
    scale(coefficient, multiply(metricInsertionSymbol(spin - 2), traceSymbol(spin))),
  );
}

function adjointEquationMatrix(fieldSystem, spin, momentum) {
  const qCoefficient = polynomialCoefficient(fieldSystem.D, 'Q');
  const paCoefficient = polynomialCoefficient(fieldSystem.D, 'P A');
  const traceCoefficient = polynomialCoefficient(fieldSystem.D, 'P P T');
  const wave = scale(qCoefficient * qOf(momentum), identity(basis(spin).length));
  const pa = multiply(multiplicationSymbol(spin - 1, momentum),
    contractionSymbol(spin, momentum));
  const aa = multiply(contractionSymbol(spin - 1, momentum),
    contractionSymbol(spin, momentum));
  const uaa = multiply(metricInsertionSymbol(spin - 2), aa);
  return add(wave, scale(paCoefficient, pa), scale(traceCoefficient, uaa));
}

function constraintResidualMatrix(spin, momentum, coefficient) {
  if (spin < 4) return zeros(basis(spin).length, basis(spin).length);
  const doubleTrace = multiply(traceSymbol(spin - 2), traceSymbol(spin));
  const pp = multiply(multiplicationSymbol(spin - 3, momentum),
    multiplicationSymbol(spin - 4, momentum));
  const uppTT = multiply(metricInsertionSymbol(spin - 2), multiply(pp, doubleTrace));

  const aaT = multiply(contractionSymbol(spin - 3, momentum),
    multiply(contractionSymbol(spin - 2, momentum), traceSymbol(spin)));
  const uuaaT = multiply(metricInsertionSymbol(spin - 2),
    multiply(metricInsertionSymbol(spin - 4), aaT));
  return scale(coefficient, add(uppTT, scale(-1, uuaaT)));
}

function checkSpin(eulerResult, sourceAdapter, spin, momentum) {
  const fieldSystem = eulerResult.upstreamFieldSystem;
  const D = evaluatePolynomial(fieldSystem.D, spin, momentum).matrix;
  const Ddagger = adjointEquationMatrix(fieldSystem, spin, momentum);
  const M = multiplierMatrix(spin, eulerResult.multiplier);
  const E = multiply(M, D);
  const residual = add(E, scale(-1, multiply(Ddagger, M)));
  const factorCoefficient = polynomialCoefficient(eulerResult.constraintResidual,
    'U P P T T');
  const expected = constraintResidualMatrix(spin, momentum, factorCoefficient);
  const factorError = maximumAbsolute(add(residual, scale(-1, expected)));

  const fieldDimension = basis(spin).length;
  const doubleTrace = multiply(traceSymbol(spin - 2), traceSymbol(spin));
  const fieldBasis = nullspace(doubleTrace, fieldDimension);
  const pairing = fischerPairing(spin);
  const restrictedEuler = multiply(transpose(fieldBasis),
    multiply(pairing, multiply(E, fieldBasis)));
  const selfAdjointError = maximumAbsolute(add(
    restrictedEuler,
    scale(-1, transpose(restrictedEuler)),
  ));

  const parameterDimension = basis(spin - 1).length;
  const parameterBasis = nullspace(traceSymbol(spin - 1), parameterDimension);
  const gauge = multiply(multiplicationSymbol(spin - 1, momentum), parameterBasis);
  const gaugeError = maximumAbsolute(multiply(E, gauge));

  const MInverse = multiplierMatrix(spin, inverseSourceAdapter(sourceAdapter, spin));
  const equivalenceError = maximumAbsolute(multiply(
    add(multiply(MInverse, E), scale(-1, D)),
    fieldBasis,
  ));
  assert(factorError < tolerance, `constraint factorization failed at spin ${spin}: ${factorError}`);
  assert(selfAdjointError < tolerance,
    `restricted Euler operator is not self-adjoint at spin ${spin}: ${selfAdjointError}`);
  assert(gaugeError < tolerance, `Euler gauge identity failed at spin ${spin}: ${gaugeError}`);
  assert(equivalenceError < tolerance,
    `Euler/equation equivalence failed at spin ${spin}: ${equivalenceError}`);
  return { spin, factorError, selfAdjointError, gaugeError, equivalenceError };
}

function checkSourcedEulerUse(eulerResult, sourceAdapter) {
  const spin = 2;
  const momentum = [1, 0.3, 0, 0];
  const q = qOf(momentum);
  const current = spinTwoCurrentSymbol(momentum);
  const M = multiplierMatrix(spin, eulerResult.multiplier);
  const MInverse = multiplierMatrix(spin, inverseSourceAdapter(sourceAdapter, spin));
  const source = multiply(MInverse, current);
  const field = scale(1 / q, source);
  const D = evaluatePolynomial(eulerResult.upstreamFieldSystem.D, spin, momentum).matrix;
  const E = multiply(M, D);
  const greenEquationError = maximumAbsolute(add(multiply(D, field), scale(-1, source)));
  const physicalSourceError = maximumAbsolute(add(multiply(E, field), scale(-1, current)));
  assert(greenEquationError < tolerance,
    `generated scalar response failed to recover the adapted source: ${greenEquationError}`);
  assert(physicalSourceError < tolerance,
    `generated Euler response failed to recover the physical current: ${physicalSourceError}`);
  return { momentum, q, greenEquationError, physicalSourceError };
}

function run() {
  const generated = constructBosonicEulerOperator({ maxMetricInsertions: 1 });
  assert(generated.ok, `supported Euler budget refused: ${JSON.stringify(generated)}`);
  const refused = generated.search.insufficientBudget;
  assert(!refused.ok && refused.phase === 'euler-self-adjoint-residual',
    `identity-only Euler budget should be refused: ${JSON.stringify(refused)}`);
  const sourceAdapter = constructBosonicSourceAdapter({ maxMetricInsertions: 1 });
  assert(sourceAdapter.ok, 'source-adapter regression failed');

  console.log(JSON.stringify(serializableEulerOperator(generated), null, 2));
  const spinChecks = [2, 3, 4, 5, 6].map((spin) =>
    checkSpin(generated, sourceAdapter, spin, [1, 0.2, -0.1, 0.3]));
  console.table(spinChecks);
  const sourcedUse = checkSourcedEulerUse(generated, sourceAdapter);
  console.log(JSON.stringify({ sourcedUse }, null, 2));
  console.log('generated Euler-operator checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

export { adjointEquationMatrix, fischerPairing };

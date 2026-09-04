import { pathToFileURL } from 'node:url';
import {
  add,
  basis,
  contractionSymbol,
  identity,
  multiply,
  multiplicationSymbol,
  nullspace,
  rank,
  scale,
  traceSymbol,
  vertical,
  zeros,
} from '../04-local-symbol-extension/check-symmetric-potential.mjs';
import {
  constructBosonicFieldSystem,
  constructFermionicLocalComplex,
  keyWord,
  serializableResult,
} from './residual-constructor.mjs';
import {
  gammaTrace,
  kronecker,
  momentumClifford,
  spinorRealDimension,
} from '../04b-half-integer-potential/check-spinor-potential.mjs';

const tolerance = 1e-7;

function qOf(momentum) {
  return momentum[0] ** 2 - momentum.slice(1).reduce((sum, value) => sum + value ** 2, 0);
}

function evaluateWord(word, inputDegree, momentum) {
  let degree = inputDegree;
  let matrix = identity(basis(inputDegree).length);
  for (const token of [...word].reverse()) {
    if (token === 'Q') {
      matrix = scale(qOf(momentum), matrix);
    } else if (token === 'P') {
      matrix = multiply(multiplicationSymbol(degree, momentum), matrix);
      degree += 1;
    } else if (token === 'A') {
      matrix = multiply(contractionSymbol(degree, momentum), matrix);
      degree -= 1;
    } else if (token === 'T') {
      matrix = multiply(traceSymbol(degree), matrix);
      degree -= 2;
    } else {
      throw new Error(`unknown semantic primitive ${token}`);
    }
  }
  return { degree, matrix };
}

function evaluatePolynomial(source, inputDegree, momentum) {
  let outputDegree = null;
  let out = null;
  for (const [key, coefficient] of source) {
    const evaluated = evaluateWord(keyWord(key), inputDegree, momentum);
    if (outputDegree === null) {
      outputDegree = evaluated.degree;
      out = zeros(basis(outputDegree).length, basis(inputDegree).length);
    }
    if (evaluated.degree !== outputDegree) throw new Error('polynomial mixes map types');
    const numeric = Number(coefficient.n) / Number(coefficient.d);
    out = add(out, scale(numeric, evaluated.matrix));
  }
  return { degree: outputDegree, matrix: out };
}

function evaluateFermionicWord(word, inputDegree, momentum) {
  let degree = inputDegree;
  let matrix = identity(basis(inputDegree).length * spinorRealDimension);
  for (const token of [...word].reverse()) {
    if (token === 'Q') {
      matrix = scale(qOf(momentum), matrix);
    } else if (token === 'L') {
      matrix = multiply(kronecker(identity(basis(degree).length),
        momentumClifford(momentum)), matrix);
    } else if (token === 'P') {
      matrix = multiply(kronecker(multiplicationSymbol(degree, momentum),
        identity(spinorRealDimension)), matrix);
      degree += 1;
    } else if (token === 'A') {
      matrix = multiply(kronecker(contractionSymbol(degree, momentum),
        identity(spinorRealDimension)), matrix);
      degree -= 1;
    } else if (token === 'G') {
      matrix = multiply(gammaTrace(degree), matrix);
      degree -= 1;
    } else {
      throw new Error(`unknown fermionic primitive ${token}`);
    }
  }
  return { degree, matrix };
}

function evaluateFermionicPolynomial(source, inputDegree, momentum) {
  let outputDegree = null;
  let out = null;
  for (const [key, coefficient] of source) {
    const evaluated = evaluateFermionicWord(keyWord(key), inputDegree, momentum);
    if (outputDegree === null) {
      outputDegree = evaluated.degree;
      out = zeros(basis(outputDegree).length * spinorRealDimension,
        basis(inputDegree).length * spinorRealDimension);
    }
    if (evaluated.degree !== outputDegree) throw new Error('fermionic polynomial mixes map types');
    const numeric = Number(coefficient.n) / Number(coefficient.d);
    out = add(out, scale(numeric, evaluated.matrix));
  }
  return { degree: outputDegree, matrix: out };
}

function maximumAbsolute(matrix) {
  return matrix.reduce((maximum, row) =>
    Math.max(maximum, ...row.map((value) => Math.abs(value))), 0);
}

function checkSpin(fieldSystem, spin, label, momentum) {
  const fieldDimension = basis(spin).length;
  const parameterDimension = basis(spin - 1).length;
  const R = evaluatePolynomial(fieldSystem.R, spin - 1, momentum).matrix;
  const C = evaluatePolynomial(fieldSystem.C, spin, momentum).matrix;
  const D = evaluatePolynomial(fieldSystem.D, spin, momentum).matrix;
  const parameterConstraint = evaluatePolynomial(
    fieldSystem.parameterConstraint, spin - 1, momentum,
  ).matrix;
  const parameterBasis = nullspace(parameterConstraint, parameterDimension);
  const gaugeImage = multiply(R, parameterBasis);
  const residual = multiply(D, gaugeImage);
  if (maximumAbsolute(residual) > tolerance) {
    throw new Error(`generated D R residual at spin ${spin}: ${maximumAbsolute(residual)}`);
  }

  const defectResidual = add(multiply(C, gaugeImage),
    scale(-qOf(momentum), parameterBasis));
  if (maximumAbsolute(defectResidual) > tolerance) {
    throw new Error(`generated C R - Q residual at spin ${spin}`);
  }

  const fieldConstraint = evaluatePolynomial(fieldSystem.fieldConstraint, spin, momentum).matrix;
  const solutionBasis = nullspace(vertical(fieldConstraint, D), fieldDimension);
  const solutionDimension = solutionBasis.length ? solutionBasis[0].length : 0;
  const gaugeRank = rank(gaugeImage);
  return {
    spin,
    label,
    solutionDimension,
    gaugeRank,
    cohomology: solutionDimension - gaugeRank,
  };
}

function checkResponseUse(fieldSystem, spin, momentum) {
  const q = qOf(momentum);
  if (Math.abs(q) <= tolerance) throw new Error('the response probe requires a non-null momentum');
  const fieldDimension = basis(spin).length;
  const C = evaluatePolynomial(fieldSystem.C, spin, momentum).matrix;
  const D = evaluatePolynomial(fieldSystem.D, spin, momentum).matrix;
  const fieldConstraint = evaluatePolynomial(fieldSystem.fieldConstraint, spin, momentum).matrix;
  const admissibleSources = nullspace(vertical(fieldConstraint, C), fieldDimension);
  const sourceRank = admissibleSources.length ? admissibleSources[0].length : 0;
  if (sourceRank === 0) throw new Error(`no admissible response probe at spin ${spin}`);
  const response = scale(1 / q, admissibleSources);
  const recoveryResidual = add(multiply(D, response), scale(-1, admissibleSources));
  const error = maximumAbsolute(recoveryResidual);
  if (error > tolerance) throw new Error(`generated response failed at spin ${spin}: ${error}`);
  return { spin, admissibleSourceRank: sourceRank, recoveryError: error };
}

function checkFermionicRank(localComplex, tensorRank, label, momentum) {
  const parameterDimension = basis(tensorRank - 1).length * spinorRealDimension;
  const fieldDimension = basis(tensorRank).length * spinorRealDimension;
  const R = evaluateFermionicPolynomial(localComplex.R, tensorRank - 1, momentum).matrix;
  const S = evaluateFermionicPolynomial(localComplex.S, tensorRank, momentum).matrix;
  const parameterConstraint = evaluateFermionicPolynomial(
    localComplex.parameterConstraint, tensorRank - 1, momentum,
  ).matrix;
  const parameterBasis = nullspace(parameterConstraint, parameterDimension);
  const gaugeImage = multiply(R, parameterBasis);
  const residual = multiply(S, gaugeImage);
  if (maximumAbsolute(residual) > tolerance) {
    throw new Error(`generated fermionic S R residual at rank ${tensorRank}`);
  }
  const constraint = evaluateFermionicPolynomial(
    localComplex.fieldConstraint, tensorRank, momentum,
  ).matrix;
  const solutionBasis = nullspace(vertical(constraint, S), fieldDimension);
  const solutionDimension = solutionBasis.length ? solutionBasis[0].length : 0;
  const gaugeRank = rank(gaugeImage);
  return {
    tensorRank,
    helicity: tensorRank + 0.5,
    label,
    solutionDimension: solutionDimension / 2,
    gaugeRank: gaugeRank / 2,
    cohomology: (solutionDimension - gaugeRank) / 2,
  };
}

function run() {
  const generated = constructBosonicFieldSystem({ maxTraceDepth: 1 });
  if (!generated.ok) throw new Error(`supported budget refused: ${JSON.stringify(generated)}`);
  console.log(JSON.stringify(serializableResult(generated), null, 2));

  const insufficient = constructBosonicFieldSystem({ maxTraceDepth: 0 });
  if (insufficient.ok || insufficient.phase !== 'defect-map') {
    throw new Error(`trace-free budget should be refused: ${JSON.stringify(insufficient)}`);
  }
  console.log('bounded refusal:', JSON.stringify(insufficient));
  const shallowBosonicCarrier = constructBosonicFieldSystem({ maxFieldConstraintDepth: 1 });
  if (shallowBosonicCarrier.ok || shallowBosonicCarrier.phase !== 'field-carrier') {
    throw new Error(`single-trace field budget should be refused: ${JSON.stringify(shallowBosonicCarrier)}`);
  }
  console.log('bosonic carrier refusal:', JSON.stringify(shallowBosonicCarrier));

  const results = [];
  const momenta = { nonnull: [1, 0, 0, 0], null: [1, 0, 0, 1] };
  for (let spin = 2; spin <= 6; spin += 1) {
    for (const [label, momentum] of Object.entries(momenta)) {
      const result = checkSpin(generated.fieldSystem, spin, label, momentum);
      const expected = label === 'nonnull' ? 0 : 2;
      if (result.cohomology !== expected) {
        throw new Error(`physical regression failed: ${JSON.stringify(result)}`);
      }
      results.push(result);
    }
  }
  console.table(results);

  const responseResults = [];
  for (let spin = 2; spin <= 6; spin += 1) {
    responseResults.push(checkResponseUse(generated.fieldSystem, spin, [1, 0, 0, 0]));
  }
  console.table(responseResults);

  const fermionic = constructFermionicLocalComplex({ maxGammaDepth: 1 });
  if (!fermionic.ok) throw new Error(`Clifford transfer refused: ${JSON.stringify(fermionic)}`);
  console.log(JSON.stringify(serializableResult(fermionic), null, 2));
  const fermionicInsufficient = constructFermionicLocalComplex({ maxGammaDepth: 0 });
  if (fermionicInsufficient.ok
      || fermionicInsufficient.phase !== 'fermionic-equation-residual') {
    throw new Error(`gamma-free budget should be refused: ${JSON.stringify(fermionicInsufficient)}`);
  }
  console.log('Clifford bounded refusal:', JSON.stringify(fermionicInsufficient));
  const shallowFermionicCarrier = constructFermionicLocalComplex({ maxFieldConstraintDepth: 2 });
  if (shallowFermionicCarrier.ok
      || shallowFermionicCarrier.phase !== 'fermionic-field-carrier') {
    throw new Error(`double-gamma field budget should be refused: ${JSON.stringify(shallowFermionicCarrier)}`);
  }
  console.log('Clifford carrier refusal:', JSON.stringify(shallowFermionicCarrier));
  const fermionicResults = [];
  for (let tensorRank = 1; tensorRank <= 4; tensorRank += 1) {
    for (const [label, momentum] of Object.entries(momenta)) {
      const result = checkFermionicRank(fermionic.localComplex, tensorRank, label, momentum);
      const expected = label === 'nonnull' ? 0 : 2;
      if (result.cohomology !== expected) {
        throw new Error(`fermionic transfer regression failed: ${JSON.stringify(result)}`);
      }
      fermionicResults.push(result);
    }
  }
  console.table(fermionicResults);
  console.log('generative residual constructor checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

export { evaluatePolynomial };

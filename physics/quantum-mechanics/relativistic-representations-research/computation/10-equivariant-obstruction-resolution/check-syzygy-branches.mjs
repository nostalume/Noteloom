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
  traceSymbol,
  zeros,
} from '../04-local-symbol-extension/check-symmetric-potential.mjs';

const tolerance = 1e-8;

function factorial(value) {
  let out = 1;
  for (let index = 2; index <= value; index += 1) out *= index;
  return out;
}

function metricInsertionSymbol(degree) {
  const input = basis(degree);
  const output = basis(degree + 2);
  const outputIndex = new Map(output.map((exponent, index) => [exponent.join(','), index]));
  const matrix = zeros(output.length, input.length);
  input.forEach((exponent, column) => {
    for (let index = 0; index < 4; index += 1) {
      const target = [...exponent];
      target[index] += 2;
      matrix[outputIndex.get(target.join(','))][column] += metric[index];
    }
  });
  return matrix;
}

function harmonicProjection(degree) {
  let projection = identity(basis(degree).length);
  for (let power = 1; power <= Math.floor(degree / 2); power += 1) {
    let down = identity(basis(degree).length);
    let currentDegree = degree;
    for (let index = 0; index < power; index += 1) {
      down = multiply(traceSymbol(currentDegree), down);
      currentDegree -= 2;
    }
    let up = identity(basis(currentDegree).length);
    while (currentDegree < degree) {
      up = multiply(metricInsertionSymbol(currentDegree), up);
      currentDegree += 2;
    }
    const coefficient = ((-1) ** power) * factorial(degree - power)
      / ((4 ** power) * factorial(power) * factorial(degree));
    projection = add(projection, scale(coefficient, multiply(up, down)));
  }
  return projection;
}

function inverse(matrix) {
  const size = matrix.length;
  const work = matrix.map((row, index) => [...row, ...identity(size)[index]]);
  for (let column = 0; column < size; column += 1) {
    let pivot = column;
    for (let row = column + 1; row < size; row += 1) {
      if (Math.abs(work[row][column]) > Math.abs(work[pivot][column])) pivot = row;
    }
    if (Math.abs(work[pivot][column]) < tolerance) throw new Error('singular coordinate minor');
    [work[column], work[pivot]] = [work[pivot], work[column]];
    const value = work[column][column];
    for (let index = 0; index < 2 * size; index += 1) work[column][index] /= value;
    for (let row = 0; row < size; row += 1) {
      if (row === column) continue;
      const factor = work[row][column];
      for (let index = 0; index < 2 * size; index += 1) {
        work[row][index] -= factor * work[column][index];
      }
    }
  }
  return work.map((row) => row.slice(size));
}

function coordinatesIn(columnBasis, vectors) {
  const dimension = columnBasis[0]?.length ?? 0;
  if (dimension === 0) return zeros(0, vectors[0]?.length ?? 0);
  const rows = [];
  for (let row = 0; row < columnBasis.length && rows.length < dimension; row += 1) {
    const candidate = [...rows.map((index) => columnBasis[index]), columnBasis[row]];
    if (rank(candidate) > rows.length) rows.push(row);
  }
  if (rows.length !== dimension) throw new Error('basis does not have full column rank');
  const square = rows.map((row) => columnBasis[row]);
  const sampledVectors = rows.map((row) => vectors[row]);
  return multiply(inverse(square), sampledVectors);
}

function harmonicBasis(degree) {
  return nullspace(traceSymbol(degree), basis(degree).length);
}

function blockMatrix(upperLeft, upperRight, lowerLeft, lowerRight) {
  const upperRows = upperLeft.length;
  const lowerRows = lowerLeft.length;
  const leftColumns = upperLeft[0]?.length ?? lowerLeft[0]?.length ?? 0;
  const rightColumns = upperRight[0]?.length ?? lowerRight[0]?.length ?? 0;
  const out = zeros(upperRows + lowerRows, leftColumns + rightColumns);
  for (let row = 0; row < upperRows; row += 1) {
    for (let column = 0; column < leftColumns; column += 1) out[row][column] = upperLeft[row][column];
    for (let column = 0; column < rightColumns; column += 1) out[row][leftColumns + column] = upperRight[row][column];
  }
  for (let row = 0; row < lowerRows; row += 1) {
    for (let column = 0; column < leftColumns; column += 1) out[upperRows + row][column] = lowerLeft[row][column];
    for (let column = 0; column < rightColumns; column += 1) out[upperRows + row][leftColumns + column] = lowerRight[row][column];
  }
  return out;
}

function vertical(upper, lower) {
  return [...upper, ...lower];
}

function invariantBlocks(spin, momentum) {
  const q = momentum.reduce((sum, value, index) => sum + metric[index] * value * value, 0);
  const parameter = harmonicBasis(spin - 1);
  const upper = harmonicBasis(spin);
  const lower = harmonicBasis(spin - 2);
  const upperDimension = upper[0].length;
  const lowerDimension = lower[0].length;
  const parameterDimension = parameter[0].length;
  const upperProjection = harmonicProjection(spin);
  const lowerProjection = harmonicProjection(spin - 2);

  const rPlusAmbient = multiply(upperProjection,
    multiply(multiplicationSymbol(spin - 1, momentum), parameter));
  const rMinusAmbient = multiply(contractionSymbol(spin - 1, momentum), parameter);
  const rPlus = coordinatesIn(upper, rPlusAmbient);
  const rMinus = coordinatesIn(lower, rMinusAmbient);
  const RPlus = vertical(rPlus, zeros(lowerDimension, parameterDimension));
  const RMinus = vertical(zeros(upperDimension, parameterDimension), rMinus);

  const upperIdentity = identity(upperDimension);
  const lowerIdentity = identity(lowerDimension);
  const E00q = blockMatrix(scale(q, upperIdentity), zeros(upperDimension, lowerDimension),
    zeros(lowerDimension, upperDimension), zeros(lowerDimension, lowerDimension));
  const upperPA = multiply(upperProjection,
    multiply(multiplicationSymbol(spin - 1, momentum),
      multiply(contractionSymbol(spin, momentum), upper)));
  const E00a = blockMatrix(coordinatesIn(upper, upperPA), zeros(upperDimension, lowerDimension),
    zeros(lowerDimension, upperDimension), zeros(lowerDimension, lowerDimension));

  const upperP2Lower = multiply(upperProjection,
    multiply(multiplicationSymbol(spin - 1, momentum),
      multiply(multiplicationSymbol(spin - 2, momentum), lower)));
  const E01 = blockMatrix(zeros(upperDimension, upperDimension), coordinatesIn(upper, upperP2Lower),
    zeros(lowerDimension, upperDimension), zeros(lowerDimension, lowerDimension));

  const lowerA2Upper = multiply(contractionSymbol(spin - 1, momentum),
    multiply(contractionSymbol(spin, momentum), upper));
  const E10 = blockMatrix(zeros(upperDimension, upperDimension), zeros(upperDimension, lowerDimension),
    coordinatesIn(lower, lowerA2Upper), zeros(lowerDimension, lowerDimension));
  const E11q = blockMatrix(zeros(upperDimension, upperDimension), zeros(upperDimension, lowerDimension),
    zeros(lowerDimension, upperDimension), scale(q, lowerIdentity));

  let E11a = zeros(upperDimension + lowerDimension, upperDimension + lowerDimension);
  if (spin >= 3) {
    const lowerPA = multiply(lowerProjection,
      multiply(multiplicationSymbol(spin - 3, momentum),
        multiply(contractionSymbol(spin - 2, momentum), lower)));
    E11a = blockMatrix(zeros(upperDimension, upperDimension), zeros(upperDimension, lowerDimension),
      zeros(lowerDimension, upperDimension), coordinatesIn(lower, lowerPA));
  }

  return { RPlus, RMinus, E00q, E00a, E01, E10, E11q, E11a };
}

function linearCombination(terms) {
  return add(...terms.map(([coefficient, matrix]) => scale(coefficient, matrix)));
}

function genericPair(spin, momentum, rho, weights = [1, 1]) {
  const blocks = invariantBlocks(spin, momentum);
  const [upperWeight, lowerWeight] = weights;
  const R = linearCombination([[1, blocks.RPlus], [rho, blocks.RMinus]]);
  const D = linearCombination([
    [-upperWeight, blocks.E00q],
    [upperWeight, blocks.E00a],
    [-upperWeight * (spin - 1) / (spin * rho), blocks.E01],
    [lowerWeight, blocks.E10],
    [-lowerWeight * (2 * spin - 1) / (spin * rho), blocks.E11q],
    [-lowerWeight * (spin - 2) / (spin * rho), blocks.E11a],
  ]);
  return { R, D };
}

function boundaryPair(spin, momentum, branch, coefficients) {
  const blocks = invariantBlocks(spin, momentum);
  if (branch === 'upper') {
    const [cross, lowerQ, lowerA] = coefficients;
    return {
      R: blocks.RPlus,
      D: linearCombination([
        [cross, blocks.E01], [lowerQ, blocks.E11q], [lowerA, blocks.E11a],
      ]),
    };
  }
  if (branch === 'lower') {
    const [upperQ, upperA, cross] = coefficients;
    return {
      R: blocks.RMinus,
      D: linearCombination([
        [upperQ, blocks.E00q], [upperA, blocks.E00a], [cross, blocks.E10],
      ]),
    };
  }
  throw new Error(`unknown boundary branch ${branch}`);
}

function quotientDimension({ R, D }) {
  const kernelDimension = D[0].length - rank(D);
  const gaugeRank = rank(R);
  const residualRank = rank(multiply(D, R));
  if (residualRank !== 0) throw new Error(`D R residual rank ${residualRank}`);
  return { kernelDimension, gaugeRank, cohomology: kernelDimension - gaugeRank };
}

function checkGeneric(spin, rho) {
  const nonnull = quotientDimension(genericPair(spin, [1, 0, 0, 0], rho));
  const nullShell = quotientDimension(genericPair(spin, [1, 0, 0, 1], rho));
  return { spin, rho, nonnull: nonnull.cohomology, null: nullShell.cohomology };
}

function checkEquationBoundary(spin, rho, weights) {
  const nonnull = quotientDimension(genericPair(spin, [1, 0, 0, 0], rho, weights));
  const nullShell = quotientDimension(genericPair(spin, [1, 0, 0, 1], rho, weights));
  return { spin, weights: weights.join(':'), nonnull: nonnull.cohomology,
    null: nullShell.cohomology };
}

function scanBoundary(spin, branch) {
  const values = [-2, -1, 0, 1, 2];
  const width = 3;
  const candidates = [[]];
  for (let index = 0; index < width; index += 1) {
    const previous = [...candidates];
    candidates.length = 0;
    for (const prefix of previous) {
      for (const value of values) candidates.push([...prefix, value]);
    }
  }
  const matches = [];
  for (const coefficients of candidates) {
    if (coefficients.every((value) => value === 0)) continue;
    const nonnull = quotientDimension(boundaryPair(spin, [1, 0, 0, 0], branch, coefficients));
    const nullShell = quotientDimension(boundaryPair(spin, [1, 0, 0, 1], branch, coefficients));
    if (nonnull.cohomology === 0 && nullShell.cohomology === 2) matches.push(coefficients);
  }
  return { spin, branch, candidates: candidates.length - 1, matches: matches.length,
    witness: matches[0] ?? null };
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const results = [];
  for (let spin = 2; spin <= 6; spin += 1) {
    for (const rho of [1 / (2 * spin), 1, -2]) results.push(checkGeneric(spin, rho));
  }
  for (const result of results) {
    if (result.nonnull !== 0 || result.null !== 2) {
      throw new Error(`generic branch failed: ${JSON.stringify(result)}`);
    }
  }
  console.table(results);
  const equationBoundaries = [];
  for (const spin of [2, 3, 4]) {
    equationBoundaries.push(checkEquationBoundary(spin, 1 / (2 * spin), [1, 0]));
    equationBoundaries.push(checkEquationBoundary(spin, 1 / (2 * spin), [0, 1]));
  }
  console.table(equationBoundaries);
  const boundaryResults = [];
  for (const spin of [2, 3, 4]) {
    boundaryResults.push(scanBoundary(spin, 'upper'));
    boundaryResults.push(scanBoundary(spin, 'lower'));
  }
  for (const result of boundaryResults) {
    if (result.matches !== 0) throw new Error(`unexpected boundary witness: ${JSON.stringify(result)}`);
  }
  console.table(boundaryResults);
  console.log('syzygy-branch cohomology checks: pass');
}

export { boundaryPair, genericPair, invariantBlocks, quotientDimension, scanBoundary };

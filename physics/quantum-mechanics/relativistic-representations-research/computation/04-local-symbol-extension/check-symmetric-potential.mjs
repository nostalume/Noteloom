import { pathToFileURL } from 'node:url';

const metric = [1, -1, -1, -1];
const tolerance = 1e-9;

function compositions(total, slots, prefix = []) {
  if (slots === 1) return [[...prefix, total]];
  const out = [];
  for (let value = 0; value <= total; value += 1) {
    out.push(...compositions(total - value, slots - 1, [...prefix, value]));
  }
  return out;
}

const bases = new Map();
function basis(degree) {
  if (degree < 0) return [];
  if (!bases.has(degree)) bases.set(degree, compositions(degree, 4));
  return bases.get(degree);
}

function indexOfBasis(degree) {
  return new Map(basis(degree).map((exponent, index) => [exponent.join(','), index]));
}

function zeros(rows, columns) {
  return Array.from({ length: rows }, () => Array(columns).fill(0));
}

function identity(size) {
  const out = zeros(size, size);
  for (let i = 0; i < size; i += 1) out[i][i] = 1;
  return out;
}

function add(...matrices) {
  const rows = matrices[0].length;
  const columns = rows ? matrices[0][0].length : 0;
  const out = zeros(rows, columns);
  for (const matrix of matrices) {
    for (let row = 0; row < rows; row += 1) {
      for (let column = 0; column < columns; column += 1) {
        out[row][column] += matrix[row][column];
      }
    }
  }
  return out;
}

function scale(factor, matrix) {
  return matrix.map((row) => row.map((value) => factor * value));
}

function multiply(left, right) {
  const rows = left.length;
  const middle = right.length;
  const columns = middle ? right[0].length : 0;
  const out = zeros(rows, columns);
  for (let row = 0; row < rows; row += 1) {
    for (let inner = 0; inner < middle; inner += 1) {
      const coefficient = left[row][inner];
      if (coefficient === 0) continue;
      for (let column = 0; column < columns; column += 1) {
        out[row][column] += coefficient * right[inner][column];
      }
    }
  }
  return out;
}

function vertical(...matrices) {
  return matrices.flatMap((matrix) => matrix);
}

function multiplicationSymbol(degree, momentum) {
  const input = basis(degree);
  const output = basis(degree + 1);
  const outputIndex = indexOfBasis(degree + 1);
  const matrix = zeros(output.length, input.length);
  const flatMomentum = momentum.map((value, index) => metric[index] * value);
  input.forEach((exponent, column) => {
    for (let index = 0; index < 4; index += 1) {
      if (flatMomentum[index] === 0) continue;
      const target = [...exponent];
      target[index] += 1;
      matrix[outputIndex.get(target.join(','))][column] += flatMomentum[index];
    }
  });
  return matrix;
}

function contractionSymbol(degree, momentum) {
  if (degree === 0) return zeros(0, 1);
  const input = basis(degree);
  const output = basis(degree - 1);
  const outputIndex = indexOfBasis(degree - 1);
  const matrix = zeros(output.length, input.length);
  input.forEach((exponent, column) => {
    for (let index = 0; index < 4; index += 1) {
      if (exponent[index] === 0 || momentum[index] === 0) continue;
      const target = [...exponent];
      target[index] -= 1;
      matrix[outputIndex.get(target.join(','))][column] +=
        momentum[index] * exponent[index];
    }
  });
  return matrix;
}

function traceSymbol(degree) {
  if (degree < 2) return zeros(0, basis(degree).length);
  const input = basis(degree);
  const output = basis(degree - 2);
  const outputIndex = indexOfBasis(degree - 2);
  const matrix = zeros(output.length, input.length);
  input.forEach((exponent, column) => {
    for (let index = 0; index < 4; index += 1) {
      if (exponent[index] < 2) continue;
      const target = [...exponent];
      target[index] -= 2;
      matrix[outputIndex.get(target.join(','))][column] +=
        metric[index] * exponent[index] * (exponent[index] - 1);
    }
  });
  return matrix;
}

function rank(matrix) {
  if (matrix.length === 0) return 0;
  const work = matrix.map((row) => [...row]);
  const rows = work.length;
  const columns = work[0].length;
  let pivotRow = 0;
  for (let column = 0; column < columns && pivotRow < rows; column += 1) {
    let pivot = pivotRow;
    for (let row = pivotRow + 1; row < rows; row += 1) {
      if (Math.abs(work[row][column]) > Math.abs(work[pivot][column])) pivot = row;
    }
    if (Math.abs(work[pivot][column]) <= tolerance) continue;
    [work[pivotRow], work[pivot]] = [work[pivot], work[pivotRow]];
    const value = work[pivotRow][column];
    for (let current = column; current < columns; current += 1) {
      work[pivotRow][current] /= value;
    }
    for (let row = 0; row < rows; row += 1) {
      if (row === pivotRow) continue;
      const factor = work[row][column];
      if (Math.abs(factor) <= tolerance) continue;
      for (let current = column; current < columns; current += 1) {
        work[row][current] -= factor * work[pivotRow][current];
      }
    }
    pivotRow += 1;
  }
  return pivotRow;
}

function nullspace(matrix, columns) {
  if (matrix.length === 0) return identity(columns);
  const work = matrix.map((row) => [...row]);
  const pivots = [];
  let pivotRow = 0;
  for (let column = 0; column < columns && pivotRow < work.length; column += 1) {
    let pivot = pivotRow;
    for (let row = pivotRow + 1; row < work.length; row += 1) {
      if (Math.abs(work[row][column]) > Math.abs(work[pivot][column])) pivot = row;
    }
    if (Math.abs(work[pivot][column]) <= tolerance) continue;
    [work[pivotRow], work[pivot]] = [work[pivot], work[pivotRow]];
    const value = work[pivotRow][column];
    for (let current = column; current < columns; current += 1) {
      work[pivotRow][current] /= value;
    }
    for (let row = 0; row < work.length; row += 1) {
      if (row === pivotRow) continue;
      const factor = work[row][column];
      if (Math.abs(factor) <= tolerance) continue;
      for (let current = column; current < columns; current += 1) {
        work[row][current] -= factor * work[pivotRow][current];
      }
    }
    pivots.push(column);
    pivotRow += 1;
  }
  const pivotSet = new Set(pivots);
  const free = Array.from({ length: columns }, (_, index) => index)
    .filter((index) => !pivotSet.has(index));
  const vectors = free.map((freeColumn) => {
    const vector = Array(columns).fill(0);
    vector[freeColumn] = 1;
    pivots.forEach((pivotColumn, row) => {
      vector[pivotColumn] = -work[row][freeColumn];
    });
    return vector;
  });
  return Array.from({ length: columns }, (_, row) => vectors.map((vector) => vector[row]));
}

function screenRestriction(degree) {
  const input = basis(degree);
  const screen = Array.from({ length: degree + 1 }, (_, first) => [first, degree - first]);
  const screenIndex = new Map(screen.map((exponent, index) => [exponent.join(','), index]));
  const matrix = zeros(screen.length, input.length);
  input.forEach((exponent, column) => {
    if (exponent[0] === 0 && exponent[3] === 0) {
      matrix[screenIndex.get([exponent[1], exponent[2]].join(','))][column] = 1;
    }
  });
  return matrix;
}

function symbols(spin, momentum) {
  const q = momentum.reduce((sum, value, index) => sum + metric[index] * value * value, 0);
  const P = multiplicationSymbol(spin - 1, momentum);
  const A = contractionSymbol(spin, momentum);
  const T = traceSymbol(spin);
  const PA = multiply(multiplicationSymbol(spin - 1, momentum), A);
  const P2T = spin >= 2
    ? multiply(multiplicationSymbol(spin - 1, momentum),
      multiply(multiplicationSymbol(spin - 2, momentum), T))
    : zeros(basis(spin).length, basis(spin).length);
  const D = add(scale(q, identity(basis(spin).length)), scale(-1, PA), scale(0.5, P2T));
  return { P, D, T };
}

function check(spin, label, momentum) {
  const fieldDimension = basis(spin).length;
  const { P, D } = symbols(spin, momentum);
  const T = traceSymbol(spin);
  const T2 = spin >= 4 ? multiply(traceSymbol(spin - 2), T) : [];
  const fieldConstraints = vertical(T2, D);
  const solutionBasis = nullspace(fieldConstraints, fieldDimension);
  const solutionDimension = solutionBasis.length ? solutionBasis[0].length : 0;
  const parameterDimension = basis(spin - 1).length;
  const parameterTrace = traceSymbol(spin - 1);
  const parameterBasis = nullspace(parameterTrace, parameterDimension);
  const gaugeImage = multiply(P, parameterBasis);
  const gaugeRank = rank(gaugeImage);
  const cohomology = solutionDimension - gaugeRank;
  let screenRank = null;
  if (label === 'null') screenRank = rank(multiply(screenRestriction(spin), solutionBasis));
  return { spin, label, solutionDimension, gaugeRank, cohomology, screenRank };
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const momenta = {
    null: [1, 0, 0, 1],
    nonnull: [1, 0, 0, 0],
    zero: [0, 0, 0, 0],
  };

  const results = [];
  for (let spin = 1; spin <= 6; spin += 1) {
    for (const [label, momentum] of Object.entries(momenta)) {
      const result = check(spin, label, momentum);
      if (label === 'null' && (result.cohomology !== 2 || result.screenRank !== 2)) {
        throw new Error(`null check failed: ${JSON.stringify(result)}`);
      }
      if (label === 'nonnull' && result.cohomology !== 0) {
        throw new Error(`nonnull check failed: ${JSON.stringify(result)}`);
      }
      results.push(result);
    }
  }

  console.table(results);
  console.log('symmetric-potential fiber checks: pass');
}

export {
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
  tolerance,
  vertical,
  zeros,
};

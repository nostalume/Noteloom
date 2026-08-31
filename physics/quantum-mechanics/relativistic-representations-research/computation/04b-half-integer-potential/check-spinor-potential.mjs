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
  tolerance,
  vertical,
  zeros,
} from '../04-local-symbol-extension/check-symmetric-potential.mjs';

const spinorRealDimension = 8;

function complex(re = 0, im = 0) {
  return { re, im };
}

function realify(matrix) {
  const size = matrix.length;
  const out = zeros(2 * size, 2 * size);
  for (let row = 0; row < size; row += 1) {
    for (let column = 0; column < size; column += 1) {
      const { re, im } = matrix[row][column];
      out[row][column] = re;
      out[row][column + size] = -im;
      out[row + size][column] = im;
      out[row + size][column + size] = re;
    }
  }
  return out;
}

function complexMatrix(entries) {
  return entries.map((row) => row.map((entry) => {
    if (Array.isArray(entry)) return complex(entry[0], entry[1]);
    return complex(entry, 0);
  }));
}

const gamma = [
  complexMatrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, -1, 0],
    [0, 0, 0, -1],
  ]),
  complexMatrix([
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, -1, 0, 0],
    [-1, 0, 0, 0],
  ]),
  complexMatrix([
    [0, 0, 0, [0, -1]],
    [0, 0, [0, 1], 0],
    [0, [0, 1], 0, 0],
    [[0, -1], 0, 0, 0],
  ]),
  complexMatrix([
    [0, 0, 1, 0],
    [0, 0, 0, -1],
    [-1, 0, 0, 0],
    [0, 1, 0, 0],
  ]),
].map(realify);

function kronecker(left, right) {
  if (left.length === 0 || right.length === 0) return [];
  const leftColumns = left[0].length;
  const rightColumns = right[0].length;
  const out = zeros(left.length * right.length, leftColumns * rightColumns);
  for (let leftRow = 0; leftRow < left.length; leftRow += 1) {
    for (let leftColumn = 0; leftColumn < leftColumns; leftColumn += 1) {
      for (let rightRow = 0; rightRow < right.length; rightRow += 1) {
        for (let rightColumn = 0; rightColumn < rightColumns; rightColumn += 1) {
          out[leftRow * right.length + rightRow]
            [leftColumn * rightColumns + rightColumn] =
              left[leftRow][leftColumn] * right[rightRow][rightColumn];
        }
      }
    }
  }
  return out;
}

function gammaTrace(degree) {
  if (degree === 0) return [];
  const terms = [];
  for (let direction = 0; direction < 4; direction += 1) {
    const unit = [0, 0, 0, 0];
    unit[direction] = 1;
    terms.push(kronecker(contractionSymbol(degree, unit), gamma[direction]));
  }
  return add(...terms);
}

function gammaInsertion(degree) {
  if (degree < 0) return [];
  const terms = [];
  for (let direction = 0; direction < 4; direction += 1) {
    const unit = [0, 0, 0, 0];
    unit[direction] = 1;
    terms.push(kronecker(multiplicationSymbol(degree, unit), gamma[direction]));
  }
  return add(...terms);
}

function momentumClifford(momentum) {
  const out = zeros(spinorRealDimension, spinorRealDimension);
  for (let direction = 0; direction < 4; direction += 1) {
    const coefficient = metric[direction] * momentum[direction];
    for (let row = 0; row < spinorRealDimension; row += 1) {
      for (let column = 0; column < spinorRealDimension; column += 1) {
        out[row][column] += coefficient * gamma[direction][row][column];
      }
    }
  }
  return out;
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
  return kronecker(matrix, identity(spinorRealDimension));
}

function fieldConstraint(rankValue) {
  if (rankValue < 3) return [];
  return multiply(gammaTrace(rankValue - 2),
    multiply(gammaTrace(rankValue - 1), gammaTrace(rankValue)));
}

function symbols(rankValue, momentum) {
  const polynomialIdentity = identity(basis(rankValue).length);
  const Slash = kronecker(polynomialIdentity, momentumClifford(momentum));
  const Gamma = gammaTrace(rankValue);
  const P = rankValue > 0
    ? kronecker(multiplicationSymbol(rankValue - 1, momentum), identity(spinorRealDimension))
    : [];
  const S = rankValue > 0 ? add(Slash, scale(-1, multiply(P, Gamma))) : Slash;
  return { P, S };
}

function transpose(matrix) {
  if (matrix.length === 0) return [];
  return Array.from({ length: matrix[0].length }, (_, column) =>
    Array.from({ length: matrix.length }, (_, row) => matrix[row][column]));
}

function maximumAbsoluteEntry(matrix) {
  let maximum = 0;
  for (const row of matrix) {
    for (const entry of row) maximum = Math.max(maximum, Math.abs(entry));
  }
  return maximum;
}

function factorial(value) {
  let out = 1;
  for (let current = 2; current <= value; current += 1) out *= current;
  return out;
}

function polynomialFischerGram(degree) {
  const monomials = basis(degree);
  const out = zeros(monomials.length, monomials.length);
  monomials.forEach((exponent, index) => {
    out[index][index] = exponent.reduce((value, power, direction) =>
      value * factorial(power) * (metric[direction] ** power), 1);
  });
  return out;
}

const spinorDiracGram = [1, 1, -1, -1, 1, 1, -1, -1]
  .map((value, row) => Array.from({ length: spinorRealDimension },
    (_, column) => (row === column ? value : 0)));

function independentColumnBasis(matrix) {
  if (matrix.length === 0) return [];
  const selected = [];
  let current = zeros(matrix.length, 0);
  for (let column = 0; column < matrix[0].length; column += 1) {
    const trial = matrix.map((row, rowIndex) => [
      ...current[rowIndex],
      row[column],
    ]);
    if (rank(trial) > selected.length) {
      selected.push(column);
      current = trial;
    }
  }
  return current;
}

function minimumCholeskyPivot(matrix) {
  const size = matrix.length;
  const lower = zeros(size, size);
  let minimum = Number.POSITIVE_INFINITY;
  for (let row = 0; row < size; row += 1) {
    for (let column = 0; column <= row; column += 1) {
      let value = matrix[row][column];
      for (let inner = 0; inner < column; inner += 1) {
        value -= lower[row][inner] * lower[column][inner];
      }
      if (row === column) {
        if (value <= tolerance) return value;
        lower[row][column] = Math.sqrt(value);
        minimum = Math.min(minimum, value);
      } else {
        lower[row][column] = value / lower[column][column];
      }
    }
  }
  return minimum;
}

function screenFischerGram(degree) {
  return Array.from({ length: degree + 1 }, (_, first) =>
    Array.from({ length: degree + 1 }, (_, second) => (
      first === second ? factorial(first) * factorial(degree - first) : 0
    )));
}

function positiveShellCheck(rankValue) {
  const p = [1, 0, 0, 1];
  const a = [0.5, 0, 0, -0.5];
  const alternativeA = [1, 1, 0, 0];
  const spinorKernel = nullspace(momentumClifford(p), spinorRealDimension);
  const kappa = multiply(spinorDiracGram, momentumClifford(a));
  const alternativeKappa = multiply(spinorDiracGram, momentumClifford(alternativeA));
  const witnessResidual = maximumAbsoluteEntry(multiply(transpose(spinorKernel),
    multiply(add(alternativeKappa, scale(-1, kappa)), spinorKernel)));
  const symmetryResidual = maximumAbsoluteEntry(add(kappa, scale(-1, transpose(kappa))));

  const pastKappa = scale(-1, multiply(spinorDiracGram,
    momentumClifford(a.map((value) => -value))));
  const timeOrientationResidual = maximumAbsoluteEntry(add(
    pastKappa,
    scale(-1, kappa),
  ));

  const fieldRealDimension = basis(rankValue).length * spinorRealDimension;
  const { S } = symbols(rankValue, p);
  const solutionBasis = nullspace(vertical(fieldConstraint(rankValue), S),
    fieldRealDimension);
  const physicalBasis = independentColumnBasis(multiply(
    screenRestriction(rankValue),
    solutionBasis,
  ));
  const physicalDimension = physicalBasis.length ? physicalBasis[0].length : 0;
  const physicalGram = kronecker(screenFischerGram(rankValue), kappa);
  const restrictedGram = multiply(transpose(physicalBasis),
    multiply(physicalGram, physicalBasis));
  const minimumPivot = minimumCholeskyPivot(restrictedGram);

  if (witnessResidual > tolerance || symmetryResidual > tolerance
      || timeOrientationResidual > tolerance) {
    throw new Error(`spinor-shell metric invariance failed at rank ${rankValue}`);
  }
  if (physicalDimension !== 4 || minimumPivot <= tolerance) {
    throw new Error(`physical shell metric is not positive at rank ${rankValue}`);
  }

  return {
    tensorRank: rankValue,
    helicity: rankValue + 0.5,
    physicalComplexDimension: physicalDimension / 2,
    minimumCholeskyPivot: minimumPivot,
    witnessResidual,
  };
}

function completionCheck(rankValue, momentum) {
  const polynomialDimension = basis(rankValue).length;
  const fieldRealDimension = polynomialDimension * spinorRealDimension;
  const q = momentum.reduce((sum, value, direction) =>
    sum + metric[direction] * value * value, 0);
  const { P, S } = symbols(rankValue, momentum);
  const Gamma = gammaTrace(rankValue);
  const T = rankValue >= 2
    ? multiply(gammaTrace(rankValue - 1), Gamma)
    : zeros(0, fieldRealDimension);
  const Y = rankValue >= 1
    ? gammaInsertion(rankValue - 1)
    : zeros(fieldRealDimension, 0);
  const YGamma = rankValue >= 1
    ? multiply(Y, Gamma)
    : zeros(fieldRealDimension, fieldRealDimension);
  const Y2T = rankValue >= 2
    ? multiply(gammaInsertion(rankValue - 1),
      multiply(gammaInsertion(rankValue - 2), T))
    : zeros(fieldRealDimension, fieldRealDimension);
  const M = add(identity(fieldRealDimension), scale(-0.5, YGamma), scale(-0.25, Y2T));
  const fieldBasis = nullspace(fieldConstraint(rankValue), fieldRealDimension);

  const preservationResidual = fieldConstraint(rankValue).length
    ? maximumAbsoluteEntry(multiply(fieldConstraint(rankValue), multiply(M, fieldBasis)))
    : 0;
  const restrictedDimension = fieldBasis.length ? fieldBasis[0].length : 0;
  const restrictedRank = rank(multiply(M, fieldBasis));

  const E = multiply(M, S);
  const gram = kronecker(polynomialFischerGram(rankValue), spinorDiracGram);
  const restrictedGram = multiply(transpose(fieldBasis), multiply(gram, fieldBasis));
  const restrictedGramRank = rank(restrictedGram);
  const restrictedEuler = multiply(transpose(fieldBasis),
    multiply(gram, multiply(E, fieldBasis)));
  const adjointResidual = maximumAbsoluteEntry(add(
    restrictedEuler,
    scale(-1, transpose(restrictedEuler)),
  ));

  let hyperbolicResidual = maximumAbsoluteEntry(add(
    multiply(S, S),
    scale(-q, identity(fieldRealDimension)),
  ));
  let bianchiResidual = 0;
  let gaugeResidual = 0;

  if (rankValue >= 1) {
    const parameterRealDimension = basis(rankValue - 1).length * spinorRealDimension;
    const A = kronecker(contractionSymbol(rankValue, momentum),
      identity(spinorRealDimension));
    const PT = rankValue >= 2
      ? multiply(kronecker(multiplicationSymbol(rankValue - 2, momentum),
        identity(spinorRealDimension)), T)
      : zeros(parameterRealDimension, fieldRealDimension);
    const slashLower = kronecker(identity(basis(rankValue - 1).length),
      momentumClifford(momentum));
    const B = add(A, scale(-0.5, PT), scale(-0.5, multiply(slashLower, Gamma)));
    const parameterBasis = nullspace(gammaTrace(rankValue - 1), parameterRealDimension);

    hyperbolicResidual = maximumAbsoluteEntry(multiply(add(
      multiply(S, S),
      scale(2, multiply(P, B)),
      scale(-q, identity(fieldRealDimension)),
    ), fieldBasis));
    bianchiResidual = maximumAbsoluteEntry(multiply(multiply(B, S), fieldBasis));
    gaugeResidual = maximumAbsoluteEntry(multiply(add(
      multiply(B, P),
      scale(-0.5 * q, identity(parameterRealDimension)),
    ), parameterBasis));
  }

  const residuals = {
    preservationResidual,
    adjointResidual,
    hyperbolicResidual,
    bianchiResidual,
    gaugeResidual,
  };
  for (const [name, value] of Object.entries(residuals)) {
    if (value > tolerance) {
      throw new Error(`${name} failed at rank ${rankValue}: ${value}`);
    }
  }
  if (restrictedRank !== restrictedDimension) {
    throw new Error(`trace reversal is singular at rank ${rankValue}`);
  }
  if (restrictedGramRank !== restrictedDimension) {
    throw new Error(`constrained pairing is degenerate at rank ${rankValue}`);
  }

  return {
    tensorRank: rankValue,
    helicity: rankValue + 0.5,
    fieldDimension: restrictedDimension / 2,
    pairingRank: restrictedGramRank / 2,
    traceReversalRank: restrictedRank / 2,
    maximumResidual: Math.max(...Object.values(residuals)),
  };
}

function check(rankValue, label, momentum) {
  const fieldRealDimension = basis(rankValue).length * spinorRealDimension;
  const { P, S } = symbols(rankValue, momentum);
  const constraints = vertical(fieldConstraint(rankValue), S);
  const solutionBasis = nullspace(constraints, fieldRealDimension);
  const solutionRealDimension = solutionBasis.length ? solutionBasis[0].length : 0;

  let gaugeRealRank = 0;
  if (rankValue > 0) {
    const parameterRealDimension = basis(rankValue - 1).length * spinorRealDimension;
    const parameterBasis = nullspace(gammaTrace(rankValue - 1), parameterRealDimension);
    gaugeRealRank = rank(multiply(P, parameterBasis));
  }

  const cohomology = (solutionRealDimension - gaugeRealRank) / 2;
  const screenRank = label === 'null'
    ? rank(multiply(screenRestriction(rankValue), solutionBasis)) / 2
    : null;
  return {
    tensorRank: rankValue,
    helicity: rankValue + 0.5,
    label,
    solutionDimension: solutionRealDimension / 2,
    gaugeRank: gaugeRealRank / 2,
    cohomology,
    screenRank,
  };
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const momenta = {
    null: [1, 0, 0, 1],
    nonnull: [1, 0, 0, 0],
    zero: [0, 0, 0, 0],
  };

  const results = [];
  for (let tensorRank = 0; tensorRank <= 3; tensorRank += 1) {
    for (const [label, momentum] of Object.entries(momenta)) {
      const result = check(tensorRank, label, momentum);
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
  console.log('half-integer spinor-potential fiber checks: pass');

  const completionResults = [];
  for (let tensorRank = 0; tensorRank <= 3; tensorRank += 1) {
    completionResults.push(completionCheck(tensorRank, momenta.nonnull));
    completionResults.push(completionCheck(tensorRank, momenta.null));
  }
  console.table(completionResults);
  console.log('half-integer adjoint and hyperbolic-completion checks: pass');

  const positiveShellResults = [];
  for (let tensorRank = 0; tensorRank <= 3; tensorRank += 1) {
    positiveShellResults.push(positiveShellCheck(tensorRank));
  }
  console.table(positiveShellResults);
  console.log('half-integer positive spinor-screen metric checks: pass');
}

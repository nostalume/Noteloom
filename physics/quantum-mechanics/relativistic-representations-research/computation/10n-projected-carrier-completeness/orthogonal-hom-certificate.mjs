import {
  addRat,
  divideRat,
  isZero,
  multiplyRat,
  negateRat,
  rat,
  solveLinear,
} from '../10c-generative-residual-constructor/residual-constructor.mjs';

const ZERO = rat(0);
const ONE = rat(1);
const MINUS_ONE = rat(-1);

function monomials(dimension, degree) {
  if (degree < 0) return [];
  const out = [];
  function visit(axis, remaining, prefix) {
    if (axis === dimension - 1) {
      out.push([...prefix, remaining]);
      return;
    }
    for (let value = 0; value <= remaining; value += 1) {
      visit(axis + 1, remaining - value, [...prefix, value]);
    }
  }
  visit(0, degree, []);
  return out;
}

function zeroMatrix(rows, columns) {
  return Array.from({ length: rows }, () => Array.from({ length: columns }, () => ZERO));
}

function rref(matrix, columns) {
  const work = matrix.map((row) => [...row]);
  const pivots = [];
  let pivotRow = 0;
  for (let column = 0; column < columns && pivotRow < work.length; column += 1) {
    let pivot = pivotRow;
    while (pivot < work.length && isZero(work[pivot][column])) pivot += 1;
    if (pivot === work.length) continue;
    [work[pivotRow], work[pivot]] = [work[pivot], work[pivotRow]];
    const divisor = work[pivotRow][column];
    work[pivotRow] = work[pivotRow].map((value) => divideRat(value, divisor));
    for (let row = 0; row < work.length; row += 1) {
      if (row === pivotRow || isZero(work[row][column])) continue;
      const factor = work[row][column];
      work[row] = work[row].map((value, index) => addRat(
        value,
        negateRat(multiplyRat(factor, work[pivotRow][index])),
      ));
    }
    pivots.push(column);
    pivotRow += 1;
  }
  return { work, pivots };
}

function nullspace(matrix, columns) {
  const { work, pivots } = rref(matrix, columns);
  const pivotSet = new Set(pivots);
  const free = Array.from({ length: columns }, (_, index) => index)
    .filter((index) => !pivotSet.has(index));
  return free.map((freeColumn) => {
    const vector = Array.from({ length: columns }, () => ZERO);
    vector[freeColumn] = ONE;
    pivots.forEach((pivotColumn, row) => {
      vector[pivotColumn] = negateRat(work[row][freeColumn]);
    });
    return vector;
  });
}

function matrixRank(matrix, columns) {
  return rref(matrix, columns).pivots.length;
}

function addEntry(matrix, row, column, value) {
  matrix[row][column] = addRat(matrix[row][column], value);
}

function laplacianMatrix(dimension, degree, sourceMonomials) {
  const targets = monomials(dimension, degree - 2);
  const targetIndex = new Map(targets.map((powers, index) => [powers.join(','), index]));
  const matrix = zeroMatrix(targets.length, sourceMonomials.length);
  sourceMonomials.forEach((powers, column) => {
    for (let axis = 0; axis < dimension; axis += 1) {
      if (powers[axis] < 2) continue;
      const target = [...powers];
      target[axis] -= 2;
      addEntry(matrix, targetIndex.get(target.join(',')), column,
        rat(powers[axis] * (powers[axis] - 1)));
    }
  });
  return { matrix, targets };
}

function columnsToMatrix(columns, rowCount) {
  const matrix = zeroMatrix(rowCount, columns.length);
  columns.forEach((column, columnIndex) => {
    column.forEach((value, row) => { matrix[row][columnIndex] = value; });
  });
  return matrix;
}

function harmonicModel(dimension, degree) {
  const fullBasis = monomials(dimension, degree);
  const fullIndex = new Map(fullBasis.map((powers, index) => [powers.join(','), index]));
  const laplacian = laplacianMatrix(dimension, degree, fullBasis).matrix;
  const harmonicColumns = nullspace(laplacian, fullBasis.length);
  return {
    dimension,
    degree,
    fullBasis,
    fullIndex,
    harmonicColumns,
    inclusion: columnsToMatrix(harmonicColumns, fullBasis.length),
    harmonicDimension: harmonicColumns.length,
  };
}

function fullGenerator(model, first, second) {
  const matrix = zeroMatrix(model.fullBasis.length, model.fullBasis.length);
  model.fullBasis.forEach((powers, column) => {
    if (powers[second] > 0) {
      const target = [...powers];
      target[second] -= 1;
      target[first] += 1;
      addEntry(matrix, model.fullIndex.get(target.join(',')), column, rat(powers[second]));
    }
    if (powers[first] > 0) {
      const target = [...powers];
      target[first] -= 1;
      target[second] += 1;
      addEntry(matrix, model.fullIndex.get(target.join(',')), column,
        rat(-powers[first]));
    }
  });
  return matrix;
}

function fullReflection(model) {
  const matrix = zeroMatrix(model.fullBasis.length, model.fullBasis.length);
  model.fullBasis.forEach((powers, index) => {
    matrix[index][index] = powers[0] % 2 === 0 ? ONE : MINUS_ONE;
  });
  return matrix;
}

function multiplyMatrixVector(matrix, vector) {
  return matrix.map((row) => row.reduce(
    (sum, value, index) => addRat(sum, multiplyRat(value, vector[index])),
    ZERO,
  ));
}

function restrictOperator(model, fullOperator) {
  const columns = model.harmonicColumns.map((basisVector) => {
    const image = multiplyMatrixVector(fullOperator, basisVector);
    const coordinates = solveLinear(model.inclusion, image);
    if (!coordinates) throw new Error('invariant operator left the harmonic subspace');
    return coordinates;
  });
  return columnsToMatrix(columns, model.harmonicDimension);
}

function directSumTensorAction(harmonicAction, vectorAction) {
  const harmonicDimension = harmonicAction.length;
  const vectorDimension = vectorAction.length;
  const dimension = harmonicDimension * vectorDimension;
  const matrix = zeroMatrix(dimension, dimension);
  const index = (harmonic, vector) => harmonic * vectorDimension + vector;
  for (let hOut = 0; hOut < harmonicDimension; hOut += 1) {
    for (let hIn = 0; hIn < harmonicDimension; hIn += 1) {
      for (let vector = 0; vector < vectorDimension; vector += 1) {
        addEntry(matrix, index(hOut, vector), index(hIn, vector), harmonicAction[hOut][hIn]);
      }
    }
  }
  for (let vOut = 0; vOut < vectorDimension; vOut += 1) {
    for (let vIn = 0; vIn < vectorDimension; vIn += 1) {
      for (let harmonic = 0; harmonic < harmonicDimension; harmonic += 1) {
        addEntry(matrix, index(harmonic, vOut), index(harmonic, vIn), vectorAction[vOut][vIn]);
      }
    }
  }
  return matrix;
}

function tensorReflection(harmonicReflection, vectorReflection) {
  const harmonicDimension = harmonicReflection.length;
  const vectorDimension = vectorReflection.length;
  const dimension = harmonicDimension * vectorDimension;
  const matrix = zeroMatrix(dimension, dimension);
  const index = (harmonic, vector) => harmonic * vectorDimension + vector;
  for (let hOut = 0; hOut < harmonicDimension; hOut += 1) {
    for (let hIn = 0; hIn < harmonicDimension; hIn += 1) {
      for (let vOut = 0; vOut < vectorDimension; vOut += 1) {
        for (let vIn = 0; vIn < vectorDimension; vIn += 1) {
          const coefficient = multiplyRat(
            harmonicReflection[hOut][hIn],
            vectorReflection[vOut][vIn],
          );
          addEntry(matrix, index(hOut, vOut), index(hIn, vIn), coefficient);
        }
      }
    }
  }
  return matrix;
}

function intertwinerMultiplicity(domainActions, targetActions) {
  const domainDimension = domainActions[0].length;
  const targetDimension = targetActions[0].length;
  const unknowns = domainDimension * targetDimension;
  const unknownIndex = (target, domain) => target * domainDimension + domain;
  const equations = [];
  for (let action = 0; action < domainActions.length; action += 1) {
    const domainMatrix = domainActions[action];
    const targetMatrix = targetActions[action];
    for (let targetOut = 0; targetOut < targetDimension; targetOut += 1) {
      for (let domainIn = 0; domainIn < domainDimension; domainIn += 1) {
        const row = Array.from({ length: unknowns }, () => ZERO);
        for (let targetIn = 0; targetIn < targetDimension; targetIn += 1) {
          const index = unknownIndex(targetIn, domainIn);
          row[index] = addRat(row[index], targetMatrix[targetOut][targetIn]);
        }
        for (let domainOut = 0; domainOut < domainDimension; domainOut += 1) {
          row[unknownIndex(targetOut, domainOut)] = addRat(
            row[unknownIndex(targetOut, domainOut)],
            negateRat(domainMatrix[domainOut][domainIn]),
          );
        }
        if (row.some((value) => !isZero(value))) equations.push(row);
      }
    }
  }
  return unknowns - matrixRank(equations, unknowns);
}

function modelActions(model) {
  const generators = [];
  for (let first = 0; first < model.dimension; first += 1) {
    for (let second = first + 1; second < model.dimension; second += 1) {
      generators.push(restrictOperator(model, fullGenerator(model, first, second)));
    }
  }
  return {
    generators,
    reflection: restrictOperator(model, fullReflection(model)),
  };
}

function certifyOrthogonalIntertwinerDimensions({ dimension, ranks } = {}) {
  if (dimension !== 3) {
    return {
      ok: false,
      phase: 'independent-certificate-dimension',
      reason: 'the present exact independent Hom-space evaluator is intentionally bounded to O(3)',
    };
  }
  if (!Array.isArray(ranks) || ranks.some((rank) => !Number.isInteger(rank) || rank < 1)) {
    return { ok: false, phase: 'rank-budget', reason: 'positive integer ranks are required' };
  }

  const neededDegrees = new Set(ranks.flatMap((rank) => [1, rank - 1, rank, rank + 1]));
  const models = Object.fromEntries([...neededDegrees].map((degree) => [
    degree,
    harmonicModel(dimension, degree),
  ]));
  const actions = Object.fromEntries([...neededDegrees].map((degree) => [
    degree,
    modelActions(models[degree]),
  ]));
  const vectorActions = actions[1];
  const resultRanks = {};
  let generatedFamilyOperationsComplete = true;
  let mixedChannelExposed = true;

  for (const rank of ranks) {
    const source = models[rank];
    const sourceActions = actions[rank];
    const domainGenerators = sourceActions.generators.map((action, index) =>
      directSumTensorAction(action, vectorActions.generators[index]));
    const domainReflection = tensorReflection(
      sourceActions.reflection,
      vectorActions.reflection,
    );
    const domainActions = [...domainGenerators, domainReflection];
    const multiplicities = {};
    for (const [name, targetRank] of [
      ['raise', rank + 1],
      ['same', rank],
      ['lower', rank - 1],
    ]) {
      const target = actions[targetRank];
      multiplicities[name] = intertwinerMultiplicity(
        domainActions,
        [...target.generators, target.reflection],
      );
    }
    const domainDimension = source.harmonicDimension * dimension;
    const representedDimension = models[rank + 1].harmonicDimension
      + models[rank - 1].harmonicDimension;
    const omittedMixedChannelDimension = domainDimension - representedDimension;
    generatedFamilyOperationsComplete = generatedFamilyOperationsComplete
      && multiplicities.raise === 1
      && multiplicities.lower === 1
      && multiplicities.same === 0;
    mixedChannelExposed = mixedChannelExposed && omittedMixedChannelDimension > 0;
    resultRanks[rank] = {
      sourceDimension: source.harmonicDimension,
      domainDimension,
      multiplicities,
      omittedMixedChannelDimension,
    };
  }

  return {
    ok: true,
    group: 'O(3)',
    method: 'exact rational nullspace of Lie-algebra intertwining equations plus one reflection equation',
    ranks: resultRanks,
    certificates: { generatedFamilyOperationsComplete, mixedChannelExposed },
    boundary: 'this is an independent finite-rank completeness certificate, not the construction algorithm and not an arbitrary-dimension character engine',
  };
}

function directionalDerivativeMatrix(source, target, axis = 0) {
  const fullMatrix = zeroMatrix(target.fullBasis.length, source.fullBasis.length);
  source.fullBasis.forEach((powers, column) => {
    if (powers[axis] === 0) return;
    const imagePowers = [...powers];
    imagePowers[axis] -= 1;
    const row = target.fullIndex.get(imagePowers.join(','));
    fullMatrix[row][column] = rat(powers[axis]);
  });
  const columns = source.harmonicColumns.map((basisVector) => {
    const image = multiplyMatrixVector(fullMatrix, basisVector);
    const coordinates = solveLinear(target.inclusion, image);
    if (!coordinates) throw new Error('directional derivative left the harmonic family');
    return coordinates;
  });
  return columnsToMatrix(columns, target.harmonicDimension);
}

function certifyHarmonicContractionSurjectivity({ dimension, ranks } = {}) {
  if (dimension !== 3) {
    return {
      ok: false,
      phase: 'independent-certificate-dimension',
      reason: 'the present exact contraction evaluator is intentionally bounded to O(3)',
    };
  }
  if (!Array.isArray(ranks) || ranks.some((rank) => !Number.isInteger(rank) || rank < 1)) {
    return { ok: false, phase: 'rank-budget', reason: 'positive integer ranks are required' };
  }
  const neededDegrees = new Set(ranks.flatMap((rank) => [rank - 1, rank]));
  const models = Object.fromEntries([...neededDegrees].map((degree) => [
    degree,
    harmonicModel(dimension, degree),
  ]));
  const resultRanks = {};
  let allSurjective = true;
  for (const rank of ranks) {
    const source = models[rank];
    const target = models[rank - 1];
    const contraction = directionalDerivativeMatrix(source, target);
    const rankOfMap = matrixRank(contraction, source.harmonicDimension);
    const surjective = rankOfMap === target.harmonicDimension;
    allSurjective = allSurjective && surjective;
    resultRanks[rank] = {
      sourceDimension: source.harmonicDimension,
      targetDimension: target.harmonicDimension,
      rank: rankOfMap,
      kernelDimension: source.harmonicDimension - rankOfMap,
      surjective,
    };
  }
  return {
    ok: true,
    group: 'O(3)',
    momentumRepresentative: 'p=e_0 with p^2 nonzero',
    method: 'exact rational rank of p dot partial_x restricted to harmonic polynomials',
    ranks: resultRanks,
    certificates: { allSurjective },
    boundary: 'the certificate is non-null and Euclidean; null Lorentz momentum requires a separate orbit calculation',
  };
}

export {
  columnsToMatrix,
  certifyHarmonicContractionSurjectivity,
  certifyOrthogonalIntertwinerDimensions,
  directionalDerivativeMatrix,
  harmonicModel,
  matrixRank,
  nullspace,
  zeroMatrix,
};

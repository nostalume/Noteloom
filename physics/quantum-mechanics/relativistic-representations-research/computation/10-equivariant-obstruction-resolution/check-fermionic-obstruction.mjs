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

function horizontal(left, right) {
  if (left.length !== right.length) throw new Error('horizontal row mismatch');
  return left.map((row, index) => [...row, ...right[index]]);
}

function transpose(matrix) {
  if (matrix.length === 0) return [];
  return Array.from({ length: matrix[0].length }, (_, column) =>
    Array.from({ length: matrix.length }, (_, row) => matrix[row][column]));
}

function slashSymbol(degree, momentum) {
  return kronecker(identity(basis(degree).length), momentumClifford(momentum));
}

function pSymbol(degree, momentum) {
  return kronecker(multiplicationSymbol(degree, momentum), identity(spinorRealDimension));
}

function aSymbol(degree, momentum) {
  return kronecker(contractionSymbol(degree, momentum), identity(spinorRealDimension));
}

function pPower(degree, power, momentum) {
  let out = identity(basis(degree).length * spinorRealDimension);
  let current = degree;
  for (let index = 0; index < power; index += 1) {
    out = multiply(pSymbol(current, momentum), out);
    current += 1;
  }
  return out;
}

function unconstrainedComplex(tensorRank, momentum) {
  if (tensorRank < 2) throw new Error('the fermionic compensator begins at tensor rank 2');
  const parameterDimension = basis(tensorRank - 1).length * spinorRealDimension;
  const fieldDimension = basis(tensorRank).length * spinorRealDimension;
  const xiDimension = basis(tensorRank - 2).length * spinorRealDimension;
  const { P, S } = symbols(tensorRank, momentum);

  const R = vertical(P, gammaTrace(tensorRank - 1));
  const Aeq = horizontal(S, pPower(tensorRank - 2, 2, momentum));

  let Beq = [];
  if (tensorRank >= 3) {
    const targetRows = basis(tensorRank - 3).length * spinorRealDimension;
    const gamma3 = fieldConstraint(tensorRank);
    let pGamma2 = zeros(targetRows, xiDimension);
    if (tensorRank >= 4) {
      const gamma2 = multiply(gammaTrace(tensorRank - 3), gammaTrace(tensorRank - 2));
      pGamma2 = multiply(pSymbol(tensorRank - 4, momentum), gamma2);
    }
    const slashGamma = multiply(slashSymbol(tensorRank - 3, momentum),
      gammaTrace(tensorRank - 2));
    const twoA = scale(2, aSymbol(tensorRank - 2, momentum));
    const xiBlock = add(scale(-1, pGamma2), scale(-1, slashGamma), scale(-1, twoA));
    Beq = horizontal(gamma3, xiBlock);
  }

  const E = vertical(Aeq, Beq);
  if (R[0].length !== parameterDimension) throw new Error('parameter typing failed');
  if (E[0].length !== fieldDimension + xiDimension) throw new Error('field typing failed');
  return { R, E };
}

function quotientDimension({ R, E }) {
  const residual = rank(multiply(E, R));
  if (residual !== 0) throw new Error(`gauge residual rank ${residual}`);
  const kernelDimension = E[0].length - rank(E);
  const gaugeRank = rank(R);
  return {
    kernelDimension: kernelDimension / 2,
    gaugeRank: gaugeRank / 2,
    cohomology: (kernelDimension - gaugeRank) / 2,
  };
}

function gammaLayerEquation(tensorRank, momentum, discardedPower) {
  const fieldRealDimension = basis(tensorRank).length * spinorRealDimension;
  const { P, S } = symbols(tensorRank, momentum);
  const parameterBasis = tensorRank > 0
    ? nullspace(gammaTrace(tensorRank - 1), basis(tensorRank - 1).length * spinorRealDimension)
    : [];
  const R = tensorRank > 0 ? multiply(P, parameterBasis) : zeros(fieldRealDimension, 0);

  let retained = S;
  if (discardedPower > 0 && tensorRank >= discardedPower) {
    let Ypower = identity(basis(tensorRank - discardedPower).length * spinorRealDimension);
    let degree = tensorRank - discardedPower;
    for (let index = 0; index < discardedPower; index += 1) {
      Ypower = multiply(gammaInsertion(degree), Ypower);
      degree += 1;
    }
    const annihilator = nullspace(transpose(Ypower), Ypower.length);
    retained = multiply(transpose(annihilator), S);
  }
  const E = vertical(fieldConstraint(tensorRank), retained);
  const residual = rank(multiply(E, R));
  if (residual !== 0) throw new Error(`projected residual rank ${residual}`);
  const kernelDimension = fieldRealDimension - rank(E);
  const gaugeRank = rank(R);
  return {
    kernelDimension: kernelDimension / 2,
    gaugeRank: gaugeRank / 2,
    cohomology: (kernelDimension - gaugeRank) / 2,
  };
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const momenta = { nonnull: [1, 0, 0, 0], null: [1, 0, 0, 1] };
  const unconstrained = [];
  for (let tensorRank = 2; tensorRank <= 5; tensorRank += 1) {
    for (const [label, momentum] of Object.entries(momenta)) {
      const result = quotientDimension(unconstrainedComplex(tensorRank, momentum));
      const expected = label === 'null' ? 2 : 0;
      if (result.cohomology !== expected) {
        throw new Error(`unconstrained quotient failed: ${JSON.stringify({ tensorRank, label, ...result })}`);
      }
      unconstrained.push({ tensorRank, helicity: tensorRank + 0.5, label, ...result });
    }
  }
  console.table(unconstrained);

  const projected = [];
  for (let tensorRank = 1; tensorRank <= 4; tensorRank += 1) {
    for (const [label, momentum] of Object.entries(momenta)) {
      const expected = label === 'null' ? 2 : 0;
      const head = gammaLayerEquation(tensorRank, momentum, 1);
      projected.push({ tensorRank, retainedLayers: 1, label, ...head });
      if ((tensorRank >= 2 || label === 'null') && head.cohomology === expected) {
        throw new Error(`one-layer obstruction missing: ${JSON.stringify({ tensorRank, label, ...head })}`);
      }

      const firstTwo = gammaLayerEquation(tensorRank, momentum, 2);
      if (firstTwo.cohomology !== expected) {
        throw new Error(`two-layer quotient failed: ${JSON.stringify({ tensorRank, label, ...firstTwo })}`);
      }
      projected.push({ tensorRank, retainedLayers: 2, label, ...firstTwo });
    }
  }
  console.table(projected);
  console.log('fermionic obstruction and compensator checks: pass');
}

export { gammaLayerEquation, quotientDimension, unconstrainedComplex };

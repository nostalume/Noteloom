import { pathToFileURL } from 'node:url';
import {
  add,
  basis,
  contractionSymbol,
  identity,
  metric,
  multiply,
  multiplicationSymbol,
  rank,
  scale,
  traceSymbol,
  zeros,
} from '../04-local-symbol-extension/check-symmetric-potential.mjs';

function vertical(...matrices) {
  return matrices.flatMap((matrix) => matrix);
}

function horizontal(left, right) {
  if (left.length !== right.length) throw new Error('horizontal row mismatch');
  return left.map((row, index) => [...row, ...right[index]]);
}

function qOf(momentum) {
  return momentum.reduce((sum, value, index) => sum + metric[index] * value * value, 0);
}

function pPower(inputDegree, power, momentum) {
  let out = identity(basis(inputDegree).length);
  let degree = inputDegree;
  for (let index = 0; index < power; index += 1) {
    out = multiply(multiplicationSymbol(degree, momentum), out);
    degree += 1;
  }
  return out;
}

function fronsdalSymbol(spin, momentum) {
  const q = qOf(momentum);
  const PA = multiply(multiplicationSymbol(spin - 1, momentum),
    contractionSymbol(spin, momentum));
  const P2T = spin >= 2
    ? multiply(pPower(spin - 2, 2, momentum), traceSymbol(spin))
    : zeros(basis(spin).length, basis(spin).length);
  return add(scale(q, identity(basis(spin).length)), scale(-1, PA), scale(0.5, P2T));
}

function compensatorComplex(spin, momentum) {
  if (spin < 3) throw new Error('the compensator branch begins at spin 3');
  const parameterDimension = basis(spin - 1).length;
  const fieldDimension = basis(spin).length;
  const alphaDimension = basis(spin - 3).length;

  const gaugeField = multiplicationSymbol(spin - 1, momentum);
  const gaugeAlpha = traceSymbol(spin - 1);
  const R = vertical(gaugeField, gaugeAlpha);

  const equationField = fronsdalSymbol(spin, momentum);
  const equationAlpha = scale(-0.5, pPower(spin - 3, 3, momentum));
  const Aeq = horizontal(equationField, equationAlpha);

  let Beq = [];
  if (spin >= 4) {
    const trace2 = multiply(traceSymbol(spin - 2), traceSymbol(spin));
    const divergence = contractionSymbol(spin - 3, momentum);
    const tracedAlpha = spin >= 5
      ? multiply(multiplicationSymbol(spin - 5, momentum), traceSymbol(spin - 3))
      : zeros(basis(spin - 4).length, alphaDimension);
    const constraintAlpha = add(scale(-4, divergence), scale(-1, tracedAlpha));
    Beq = horizontal(trace2, constraintAlpha);
  }
  const E = vertical(Aeq, Beq);
  if (E[0].length !== fieldDimension + alphaDimension) throw new Error('equation typing failed');
  if (R[0].length !== parameterDimension) throw new Error('gauge typing failed');
  return { R, E };
}

function quotientDimension({ R, E }) {
  const residual = rank(multiply(E, R));
  if (residual !== 0) throw new Error(`gauge residual rank ${residual}`);
  const kernelDimension = E[0].length - rank(E);
  const gaugeRank = rank(R);
  return { kernelDimension, gaugeRank, cohomology: kernelDimension - gaugeRank };
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const results = [];
  for (let spin = 3; spin <= 7; spin += 1) {
    for (const [label, momentum] of Object.entries({
      nonnull: [1, 0, 0, 0],
      null: [1, 0, 0, 1],
    })) {
      const result = quotientDimension(compensatorComplex(spin, momentum));
      const expected = label === 'null' ? 2 : 0;
      if (result.cohomology !== expected) {
        throw new Error(`compensator quotient failed: ${JSON.stringify({ spin, label, ...result })}`);
      }
      results.push({ spin, label, ...result });
    }
  }
  console.table(results);
  console.log('unconstrained compensator checks: pass');
}

export { compensatorComplex, quotientDimension };

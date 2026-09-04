import { pathToFileURL } from 'node:url';
import {
  add,
  basis,
  contractionSymbol,
  identity,
  metricInsertionSymbol,
  multiply,
  nullspace,
  scale,
  traceSymbol,
  zeros,
} from '../04-local-symbol-extension/check-symmetric-potential.mjs';
import { evaluatePolynomial } from '../10c-generative-residual-constructor/check-residual-constructor.mjs';
import {
  constructBosonicSourceAdapter,
  inverseSourceAdapter,
  serializableSourceAdapter,
} from './source-adapter-constructor.mjs';
import {
  bump,
  bumpFourier,
} from '../10d-generated-causal-use/check-generated-causal-use.mjs';

const tolerance = 1e-8;

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function maximumAbsolute(matrix) {
  return matrix.reduce((maximum, row) =>
    Math.max(maximum, ...row.map((value) => Math.abs(value))), 0);
}

function adapterCoefficient(adapterPolynomial) {
  const value = adapterPolynomial.get('U T');
  return value ? Number(value.n) / Number(value.d) : 0;
}

function adapterMatrix(spin, adapterPolynomial) {
  const coefficient = adapterCoefficient(adapterPolynomial);
  const traceReinsert = multiply(metricInsertionSymbol(spin - 2), traceSymbol(spin));
  return add(identity(basis(spin).length), scale(coefficient, traceReinsert));
}

function expectedPairedResidual(spin, momentum, coefficient) {
  if (spin < 3) return zeros(basis(spin - 1).length, basis(spin).length);
  return scale(coefficient, multiply(
    metricInsertionSymbol(spin - 3),
    multiply(contractionSymbol(spin - 2, momentum), traceSymbol(spin)),
  ));
}

function checkSpin(adapterResult, spin, momentum) {
  const M = adapterMatrix(spin, adapterResult.adapter);
  const inverse = inverseSourceAdapter(adapterResult, spin);
  const MInverse = adapterMatrix(spin, inverse);
  const fieldDimension = basis(spin).length;
  const doubleTrace = multiply(traceSymbol(spin - 2), traceSymbol(spin));
  const fieldBasis = nullspace(doubleTrace, fieldDimension);
  const inverseError = maximumAbsolute(multiply(
    add(multiply(MInverse, M), scale(-1, identity(fieldDimension))),
    fieldBasis,
  ));

  const generatedC = evaluatePolynomial(
    adapterResult.upstreamFieldSystem.C,
    spin,
    momentum,
  ).matrix;
  const pairedResidual = add(
    multiply(contractionSymbol(spin, momentum), M),
    scale(-1, generatedC),
  );
  const expected = expectedPairedResidual(
    spin,
    momentum,
    adapterCoefficient(adapterResult.adapter),
  );
  const pairedError = maximumAbsolute(add(pairedResidual, scale(-1, expected)));
  assert(inverseError < tolerance, `adapter inverse failed at spin ${spin}: ${inverseError}`);
  assert(pairedError < tolerance, `paired residual failed at spin ${spin}: ${pairedError}`);
  return { spin, inverseError, pairedError };
}

function squareLinear(coefficients) {
  const output = Array(basis(2).length).fill(0);
  const index = new Map(basis(2).map((exponents, position) => [exponents.join(','), position]));
  for (let left = 0; left < 4; left += 1) {
    for (let right = 0; right < 4; right += 1) {
      const exponents = [0, 0, 0, 0];
      exponents[left] += 1;
      exponents[right] += 1;
      output[index.get(exponents.join(','))] += coefficients[left] * coefficients[right];
    }
  }
  return output;
}

function spinTwoCurrentSymbol(momentum) {
  const [energy, px, py] = momentum;
  const xBivectorMomentum = [-px, energy, 0, 0];
  const yBivectorMomentum = [-py, 0, energy, 0];
  const xSquare = squareLinear(xBivectorMomentum);
  const ySquare = squareLinear(yBivectorMomentum);
  return xSquare.map((value, index) => [value - ySquare[index]]);
}

function checkSpinTwoSourceUse(adapterResult) {
  const momentum = [1, 0.3, 0, 0];
  const current = spinTwoCurrentSymbol(momentum);
  const divergence = multiply(contractionSymbol(2, momentum), current);
  const trace = multiply(traceSymbol(2), current);
  const C = evaluatePolynomial(adapterResult.upstreamFieldSystem.C, 2, momentum).matrix;
  const unadaptedResidual = multiply(C, current);
  const inverse = inverseSourceAdapter(adapterResult, 2);
  const adapted = multiply(adapterMatrix(2, inverse), current);
  const adaptedResidual = multiply(C, adapted);
  const recovery = add(
    multiply(adapterMatrix(2, adapterResult.adapter), adapted),
    scale(-1, current),
  );

  assert(maximumAbsolute(divergence) < tolerance, 'constructed spin-two current is not conserved');
  assert(maximumAbsolute(trace) > 1e-3, 'source bench failed to expose a trace channel');
  assert(maximumAbsolute(unadaptedResidual) > 1e-3,
    'unadapted current unexpectedly satisfies the generated Green constraint');
  assert(maximumAbsolute(adaptedResidual) < tolerance,
    'generated inverse adapter failed to produce an admissible Green source');
  assert(maximumAbsolute(recovery) < tolerance,
    'generated adapter did not recover the same physical current');
  return {
    momentum,
    divergenceError: maximumAbsolute(divergence),
    traceWitness: maximumAbsolute(trace),
    unadaptedConstraintResidual: maximumAbsolute(unadaptedResidual),
    adaptedConstraintError: maximumAbsolute(adaptedResidual),
    sourceRecoveryError: maximumAbsolute(recovery),
  };
}

function bumpSecondDerivative(value) {
  if (Math.abs(value) >= 1) return 0;
  const denominator = 1 - value * value;
  return bump(value) * 2 * (3 * value ** 4 - 1) / denominator ** 4;
}

function causalScreenContrast(time, cells, prescription) {
  const step = 2 / cells;
  let sum = 0;
  for (let ix = 0; ix < cells; ix += 1) {
    const x = -1 + (ix + 0.5) * step;
    const bx = bump(x);
    for (let iy = 0; iy < cells; iy += 1) {
      const y = -1 + (iy + 0.5) * step;
      const bxy = bx * bump(y);
      for (let iz = 0; iz < cells; iz += 1) {
        const z = -1 + (iz + 0.5) * step;
        const radius = Math.hypot(x, y, z);
        if (radius === 0) continue;
        const sourceTime = prescription === 'retarded' ? time - radius : time + radius;
        sum += 2 * bxy * bump(z) * bumpSecondDerivative(sourceTime)
          / (4 * Math.PI * radius);
      }
    }
  }
  return sum * step ** 3;
}

function run() {
  const adapter = constructBosonicSourceAdapter({ maxMetricInsertions: 1 });
  assert(adapter.ok, `supported source-adapter budget refused: ${JSON.stringify(adapter)}`);

  const refused = adapter.search.insufficientBudget;
  assert(!refused.ok && refused.phase === 'source-adjoint-residual',
    `identity-only adapter budget should be refused: ${JSON.stringify(refused)}`);

  console.log(JSON.stringify(serializableSourceAdapter(adapter), null, 2));
  const spinChecks = [2, 3, 4, 5, 6].map((spin) =>
    checkSpin(adapter, spin, [1, 0.2, -0.1, 0.3]));
  console.table(spinChecks);

  const sourceUse = checkSpinTwoSourceUse(adapter);
  const observationTime = 2.5;
  const resolutions = [72, 104, 144];
  const retarded = resolutions.map((cells) => ({
    cells,
    value: causalScreenContrast(observationTime, cells, 'retarded'),
  }));
  const advanced = causalScreenContrast(observationTime, 32, 'advanced');
  const finalValue = retarded.at(-1).value;
  const relativeChange = Math.abs(finalValue - retarded.at(-2).value) / Math.abs(finalValue);
  assert(retarded.every(({ value }) => value > 0), 'retarded spin-two screen contrast vanished');
  assert(advanced === 0, `advanced spin-two response should vanish, got ${advanced}`);
  assert(relativeChange < 0.03, `spin-two causal quadrature did not stabilize: ${relativeChange}`);

  const omega = 0.5;
  const chiShell = bumpFourier(omega) ** 2 * bumpFourier(0) ** 2;
  const shellContrast = 2 * omega ** 2 * chiShell;
  assert(shellContrast > 0, 'spin-two shell contrast should be nonzero');

  console.log(JSON.stringify({
    sourceUse,
    causal: {
      observation: [observationTime, 0, 0, 0],
      retarded,
      relativeChange,
      advanced,
    },
    shell: {
      momentum: [omega, 0, 0, omega],
      screenTensor: 'e_x tensor e_x - e_y tensor e_y',
      contrastMagnitude: shellContrast,
    },
  }, null, 2));
  console.log('generated source-adapter and spin-two causal-use checks: pass');
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) run();

export { bumpSecondDerivative, causalScreenContrast, spinTwoCurrentSymbol };

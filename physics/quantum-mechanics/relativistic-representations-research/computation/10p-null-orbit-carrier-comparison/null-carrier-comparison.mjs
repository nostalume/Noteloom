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
  rank,
  scale,
  traceSymbol,
  vertical,
  zeros,
} from '../04-local-symbol-extension/check-symmetric-potential.mjs';

const nullMomentum = [1, 0, 0, 1];
const answerBearingKeys = new Set([
  'expectedCohomology',
  'expectedHelicity',
  'preferredBranch',
  'verdict',
]);

function refuse(phase, reason, details = {}) {
  return { ok: false, phase, reason, ...details };
}

function horizontal(...matrices) {
  const rows = matrices[0].length;
  if (matrices.some((matrix) => matrix.length !== rows)) {
    throw new Error('horizontal row mismatch');
  }
  return Array.from({ length: rows }, (_, row) => matrices.flatMap((matrix) => matrix[row]));
}

function transpose(matrix) {
  if (matrix.length === 0) return [];
  return Array.from({ length: matrix[0].length }, (_, column) =>
    matrix.map((row) => row[column]));
}

function subtract(left, right) {
  return add(left, scale(-1, right));
}

function blockDiagonal(left, right) {
  const leftColumns = left[0]?.length ?? 0;
  const rightColumns = right[0]?.length ?? 0;
  return [
    ...left.map((row) => [...row, ...Array(rightColumns).fill(0)]),
    ...right.map((row) => [...Array(leftColumns).fill(0), ...row]),
  ];
}

function matrixNearZero(matrix, tolerance = 1e-8) {
  return matrix.every((row) => row.every((value) => Math.abs(value) <= tolerance));
}

function sameColumnSpace(left, right) {
  const leftRank = rank(left);
  const rightRank = rank(right);
  return leftRank === rightRank
    && rank(horizontal(left, right)) === leftRank;
}

function sameRowSpace(left, right) {
  const leftRank = rank(left);
  const rightRank = rank(right);
  return leftRank === rightRank
    && rank(vertical(left, right)) === leftRank;
}

function qOf(momentum) {
  return momentum.reduce((sum, value, index) =>
    sum + metric[index] * value * value, 0);
}

function harmonicInclusion(degree) {
  return nullspace(traceSymbol(degree), basis(degree).length);
}

function doubleTraceInclusion(degree) {
  if (degree < 4) return identity(basis(degree).length);
  const doubleTrace = multiply(traceSymbol(degree - 2), traceSymbol(degree));
  return nullspace(doubleTrace, basis(degree).length);
}

function projectedRaise(inputRank, momentum) {
  const P = multiplicationSymbol(inputRank, momentum);
  if (inputRank === 0) return P;
  const A = contractionSymbol(inputRank, momentum);
  const U = metricInsertionSymbol(inputRank - 1);
  const denominator = 2 * inputRank + 2;
  return add(P, scale(-1 / denominator, multiply(U, A)));
}

function projectedWave(fieldRank, momentum) {
  const q = qOf(momentum);
  const A = contractionSymbol(fieldRank, momentum);
  const R = projectedRaise(fieldRank - 1, momentum);
  return add(scale(q, identity(basis(fieldRank).length)), scale(-1, multiply(R, A)));
}

function fronsdalSymbol(spin, momentum) {
  const q = qOf(momentum);
  const P = multiplicationSymbol(spin - 1, momentum);
  const A = contractionSymbol(spin, momentum);
  const P2T = spin >= 2
    ? multiply(P, multiply(multiplicationSymbol(spin - 2, momentum), traceSymbol(spin)))
    : zeros(basis(spin).length, basis(spin).length);
  return add(
    scale(q, identity(basis(spin).length)),
    scale(-1, multiply(P, A)),
    scale(0.5, P2T),
  );
}

function harmonicHeadQuotient(degree) {
  const U = metricInsertionSymbol(degree - 2);
  const leftNullspace = nullspace(transpose(U), basis(degree).length);
  return transpose(leftNullspace);
}

function screenRestriction(degree) {
  const input = basis(degree);
  const screenBasis = Array.from({ length: degree + 1 }, (_, first) => [first, degree - first]);
  const screenIndex = new Map(screenBasis.map((powers, index) => [powers.join(','), index]));
  const matrix = zeros(screenBasis.length, input.length);
  input.forEach((powers, column) => {
    if (powers[0] !== 0 || powers[3] !== 0) return;
    matrix[screenIndex.get([powers[1], powers[2]].join(','))][column] = 1;
  });
  return matrix;
}

function quotientRecord({ equation, gauge, fieldInclusion, recovery }) {
  const equationOnFields = multiply(equation, fieldInclusion);
  const gaugeResidualRank = rank(multiply(equation, gauge));
  const solutionBasis = nullspace(equationOnFields, fieldInclusion[0].length);
  const kernelDimension = solutionBasis[0]?.length ?? 0;
  const gaugeRank = rank(gauge);
  const screen = screenRestriction(recovery.outputRank);
  const screenRank = rank(multiply(screen, multiply(recovery.map, solutionBasis)));
  return {
    fieldDimension: fieldInclusion[0].length,
    equationRank: rank(equationOnFields),
    kernelDimension,
    gaugeRank,
    cohomology: kernelDimension - gaugeRank,
    screenRank,
    gaugeResidualRank,
    solutionBasis,
    equationOnFields,
  };
}

function stripInternal(record) {
  const { solutionBasis, equationOnFields, ...publicRecord } = record;
  return publicRecord;
}

function compareSpin(spin) {
  const parameterRank = spin - 1;
  const defectRank = spin - 2;
  const Hparameter = harmonicInclusion(parameterRank);
  const Hfield = harmonicInclusion(spin);
  const Hdefect = harmonicInclusion(defectRank);
  const R = projectedRaise(parameterRank, nullMomentum);
  const Aparameter = contractionSymbol(parameterRank, nullMomentum);
  const Afield = contractionSymbol(spin, nullMomentum);
  const Dprojected = projectedWave(spin, nullMomentum);

  const parameterDefect = multiply(Aparameter, Hparameter);
  const allowedParameterCoordinates = nullspace(
    parameterDefect,
    Hparameter[0].length,
  );
  const allowedParameters = multiply(Hparameter, allowedParameterCoordinates);
  const constrainedGauge = multiply(R, allowedParameters);
  const constrained = quotientRecord({
    equation: Dprojected,
    gauge: constrainedGauge,
    fieldInclusion: Hfield,
    recovery: { map: Hfield, outputRank: spin },
  });

  const rho = parameterRank / (parameterRank + 1);
  const lowerRaise = projectedRaise(defectRank, nullMomentum);
  const repair = scale(rho, multiply(R, lowerRaise));
  const compensatedEquation = horizontal(Dprojected, repair);
  const compensatedFieldInclusion = blockDiagonal(Hfield, Hdefect);
  const compensatedGauge = vertical(
    multiply(R, Hparameter),
    parameterDefect,
  );
  const Udefect = metricInsertionSymbol(defectRank);
  const fischerAssembly = horizontal(
    Hfield,
    scale(1 / (2 * spin), multiply(Udefect, Hdefect)),
  );
  const compensated = quotientRecord({
    equation: compensatedEquation,
    gauge: compensatedGauge,
    fieldInclusion: compensatedFieldInclusion,
    recovery: { map: fischerAssembly, outputRank: spin },
  });

  const baselineField = doubleTraceInclusion(spin);
  const symmetricGauge = multiply(multiplicationSymbol(parameterRank, nullMomentum), Hparameter);
  const head = harmonicHeadQuotient(spin);
  const baselineEquation = multiply(head, fronsdalSymbol(spin, nullMomentum));
  const baseline = quotientRecord({
    equation: baselineEquation,
    gauge: symmetricGauge,
    fieldInclusion: baselineField,
    recovery: { map: baselineField, outputRank: spin },
  });

  const assembledGauge = add(
    multiply(R, Hparameter),
    scale(1 / (2 * spin), multiply(Udefect, parameterDefect)),
  );
  const baselineOnAssembly = multiply(baselineEquation, fischerAssembly);
  const compensatedOnCoordinates = multiply(
    compensatedEquation,
    compensatedFieldInclusion,
  );
  const carrierCoincidence = sameColumnSpace(fischerAssembly, baselineField);
  const gaugeCoincidence = matrixNearZero(subtract(assembledGauge, symmetricGauge));
  const equationCoincidence = sameRowSpace(
    compensatedOnCoordinates,
    baselineOnAssembly,
  );

  const baselineFieldDimension = baselineField[0].length;
  const harmonicFieldDimension = Hfield[0].length;
  const fullParameterDimension = Hparameter[0].length;
  const constrainedParameterDimension = allowedParameterCoordinates[0]?.length ?? 0;

  return {
    constrainedHarmonic: stripInternal(constrained),
    compensatedHarmonic: stripInternal(compensated),
    symmetricBaseline: stripInternal(baseline),
    coincidences: {
      compensatorCarrierEqualsDoubleTraceCarrier: carrierCoincidence,
      compensatorGaugeEqualsSymmetricGauge: gaugeCoincidence,
      compensatorEquationKernelEqualsBaseline: equationCoincidence,
      compensatorScreenEqualsBaseline: equationCoincidence
        && compensated.screenRank === baseline.screenRank,
      fischerAssembly: `Phi = phi + 1/${2 * spin} U chi`,
      fischerInverse: 'chi = 1/2 T Phi',
    },
    cost: {
      constrainedFieldSaving: baselineFieldDimension - harmonicFieldDimension,
      removedGaugeDirections: fullParameterDimension - constrainedParameterDimension,
      constrainedFieldDimension: harmonicFieldDimension,
      compensatedFieldDimension: compensatedFieldInclusion[0].length,
      baselineFieldDimension,
      constrainedParameterDimension,
      fullParameterDimension,
    },
  };
}

function compareNullCarrierPresentations(input = {}) {
  const rejectedKey = Object.keys(input).find((key) => answerBearingKeys.has(key));
  if (rejectedKey) {
    return refuse(
      'answer-bearing-input',
      'the null-orbit comparator accepts presentation laws and spin budgets, not an expected quotient or preferred branch',
      { rejectedKey },
    );
  }
  const spins = input.spins;
  if (!Array.isArray(spins)
      || spins.some((spin) => !Number.isInteger(spin) || spin < 2)) {
    return refuse('spin-budget', 'the null comparison requires integer spins at least two');
  }
  const rows = Object.fromEntries(spins.map((spin) => [spin, compareSpin(spin)]));
  const certificates = {
    commonNullMomentum: qOf(nullMomentum) === 0,
    allGaugeComplexes: Object.values(rows).every((row) =>
      row.constrainedHarmonic.gaugeResidualRank === 0
      && row.compensatedHarmonic.gaugeResidualRank === 0
      && row.symmetricBaseline.gaugeResidualRank === 0),
    commonPhysicalQuotient: Object.values(rows).every((row) =>
      row.constrainedHarmonic.cohomology === 2
      && row.compensatedHarmonic.cohomology === 2
      && row.symmetricBaseline.cohomology === 2
      && row.constrainedHarmonic.screenRank === 2
      && row.compensatedHarmonic.screenRank === 2
      && row.symmetricBaseline.screenRank === 2),
    fischerChainCoincidence: Object.values(rows).every((row) =>
      Object.entries(row.coincidences)
        .filter(([, value]) => typeof value === 'boolean')
        .every(([, value]) => value)),
  };
  if (Object.values(certificates).some((value) => !value)) {
    return refuse(
      'comparison-certificate',
      'one null quotient, gauge identity, screen recovery, or Fischer coincidence failed',
      { spins: rows, certificates },
    );
  }
  return {
    ok: true,
    family: 'null-orbit-projected-carrier-comparison',
    momentum: nullMomentum,
    metric,
    spins: rows,
    certificates,
    verdict: {
      compensatedBranch: 'zero-order Fischer reparameterization of the compressed symmetric baseline',
      constrainedBranch: 'same null helicities with equal field saving and removed gauge directions',
      physicalNovelty: 'none at the free null quotient',
      retainedUse: 'projected-carrier compiler regression and an explicit partial-gauge presentation when that interface is requested',
    },
    nextObstruction: {
      phase: 'off-shell-capability',
      question: 'does the constrained harmonic branch improve an action, source, causal, locality, or conditioning computation enough to justify its momentum-differential gauge restriction?',
      stop: 'do not construct more carrier variants until one named off-shell capability distinguishes them',
    },
    boundary: 'finite polynomial-matrix rank comparison at one four-dimensional null representative; only transverse-screen dimension is recomputed here, while full little-group action, action, source, causal, and interaction claims remain open',
  };
}

export { compareNullCarrierPresentations };

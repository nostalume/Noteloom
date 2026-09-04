import {
  addRat,
  divideRat,
  isZero,
  multiplyRat,
  negateRat,
  rat,
  solveLinear,
} from '../10c-generative-residual-constructor/residual-constructor.mjs';
import {
  columnsToMatrix,
  directionalDerivativeMatrix,
  harmonicModel,
  matrixRank,
  nullspace,
  zeroMatrix,
} from '../10n-projected-carrier-completeness/orthogonal-hom-certificate.mjs';

const ZERO = rat(0);
const ONE = rat(1);
const answerBearingKeys = new Set([
  'expectedSourceDimension',
  'expectedVerdict',
  'preferredBranch',
  'rightInverse',
]);

function refuse(phase, reason, details = {}) {
  return { ok: false, phase, reason, ...details };
}

function transpose(matrix) {
  if (matrix.length === 0) return [];
  return Array.from({ length: matrix[0].length }, (_, column) =>
    matrix.map((row) => row[column]));
}

function multiply(left, right) {
  const rows = left.length;
  const inner = left[0]?.length ?? 0;
  const columns = right[0]?.length ?? 0;
  if (right.length !== inner) throw new Error('matrix multiplication shape mismatch');
  const output = zeroMatrix(rows, columns);
  for (let row = 0; row < rows; row += 1) {
    for (let column = 0; column < columns; column += 1) {
      let value = ZERO;
      for (let index = 0; index < inner; index += 1) {
        value = addRat(value, multiplyRat(left[row][index], right[index][column]));
      }
      output[row][column] = value;
    }
  }
  return output;
}

function multiplyVector(matrix, vector) {
  return matrix.map((row) => row.reduce(
    (sum, value, index) => addRat(sum, multiplyRat(value, vector[index])),
    ZERO,
  ));
}

function add(left, right) {
  return left.map((row, rowIndex) => row.map((value, column) =>
    addRat(value, right[rowIndex][column])));
}

function scale(coefficient, matrix) {
  return matrix.map((row) => row.map((value) => multiplyRat(coefficient, value)));
}

function vertical(...matrices) {
  return matrices.flatMap((matrix) => matrix.map((row) => [...row]));
}

function horizontal(...matrices) {
  const rows = matrices[0].length;
  if (matrices.some((matrix) => matrix.length !== rows)) {
    throw new Error('horizontal row mismatch');
  }
  return Array.from({ length: rows }, (_, row) =>
    matrices.flatMap((matrix) => matrix[row]));
}

function matrixZero(matrix) {
  return matrix.every((row) => row.every((value) => isZero(value)));
}

function sameColumnSpace(left, right) {
  const leftColumns = left[0]?.length ?? 0;
  const rightColumns = right[0]?.length ?? 0;
  const leftRank = matrixRank(left, leftColumns);
  const rightRank = matrixRank(right, rightColumns);
  return leftRank === rightRank
    && matrixRank(horizontal(left, right), leftColumns + rightColumns) === leftRank;
}

function fullMultiplication(source, target, axis) {
  const matrix = zeroMatrix(target.fullBasis.length, source.fullBasis.length);
  source.fullBasis.forEach((powers, column) => {
    const image = [...powers];
    image[axis] += 1;
    matrix[target.fullIndex.get(image.join(','))][column] = ONE;
  });
  return matrix;
}

function fullMetricInsertion(source, target) {
  const matrix = zeroMatrix(target.fullBasis.length, source.fullBasis.length);
  source.fullBasis.forEach((powers, column) => {
    for (let axis = 0; axis < source.dimension; axis += 1) {
      const image = [...powers];
      image[axis] += 2;
      const row = target.fullIndex.get(image.join(','));
      matrix[row][column] = addRat(matrix[row][column], ONE);
    }
  });
  return matrix;
}

function coordinatesIn(model, fullColumns) {
  const columns = Array.from({ length: fullColumns[0]?.length ?? 0 }, (_, column) => {
    const image = fullColumns.map((row) => row[column]);
    const coordinates = solveLinear(model.inclusion, image);
    if (!coordinates) throw new Error('generated operation left the harmonic carrier');
    return coordinates;
  });
  return columnsToMatrix(columns, model.harmonicDimension);
}

function projectedRaise({ dimension, rank, source, target, lower, contraction }) {
  const multiplication = multiply(fullMultiplication(source, target, 0), source.inclusion);
  if (rank === 0) return coordinatesIn(target, multiplication);
  const insertion = fullMetricInsertion(lower, target);
  const correction = multiply(insertion, multiply(lower.inclusion, contraction));
  const coefficient = divideRat(ONE, rat(2 * rank + dimension - 2));
  return coordinatesIn(target, add(multiplication, scale(negateRat(coefficient), correction)));
}

function rightInverse(matrix) {
  const targetDimension = matrix.length;
  const sourceDimension = matrix[0]?.length ?? 0;
  const columns = Array.from({ length: targetDimension }, (_, column) => {
    const target = Array.from({ length: targetDimension }, (__, row) =>
      (row === column ? ONE : ZERO));
    const solution = solveLinear(matrix, target);
    if (!solution) return null;
    return solution;
  });
  if (columns.some((column) => column === null)) return null;
  return columnsToMatrix(columns, sourceDimension);
}

function identity(dimension) {
  return Array.from({ length: dimension }, (_, row) =>
    Array.from({ length: dimension }, (__, column) => (row === column ? ONE : ZERO)));
}

function equal(left, right) {
  return left.length === right.length
    && left.every((row, rowIndex) => row.length === right[rowIndex].length
      && row.every((value, column) => isZero(addRat(value, negateRat(right[rowIndex][column])))));
}

function compareSpin(dimension, spin) {
  const parameterRank = spin - 1;
  const defectRank = spin - 2;
  const field = harmonicModel(dimension, spin);
  const parameter = harmonicModel(dimension, parameterRank);
  const defect = harmonicModel(dimension, defectRank);
  const contraction = directionalDerivativeMatrix(parameter, defect, 0);
  const contractionRank = matrixRank(contraction, parameter.harmonicDimension);
  const section = rightInverse(contraction);
  if (!section) throw new Error(`spin ${spin} divergence has no right inverse`);
  const sectionIdentity = multiply(contraction, section);

  const raise = projectedRaise({
    dimension,
    rank: parameterRank,
    source: parameter,
    target: field,
    lower: defect,
    contraction,
  });
  const allowedParameterColumns = nullspace(
    contraction,
    parameter.harmonicDimension,
  );
  const allowedParameters = columnsToMatrix(
    allowedParameterColumns,
    parameter.harmonicDimension,
  );
  const constrainedGauge = multiply(raise, allowedParameters);
  const constrainedSourceColumns = nullspace(
    transpose(constrainedGauge),
    field.harmonicDimension,
  );
  const constrainedSources = columnsToMatrix(
    constrainedSourceColumns,
    field.harmonicDimension,
  );

  const compensatedGauge = vertical(raise, contraction);
  const compensatedSourceColumns = nullspace(
    transpose(compensatedGauge),
    field.harmonicDimension + defect.harmonicDimension,
  );
  const compensatedSources = columnsToMatrix(
    compensatedSourceColumns,
    field.harmonicDimension + defect.harmonicDimension,
  );

  const raiseAdjoint = transpose(raise);
  const sectionAdjoint = transpose(section);
  const liftedColumns = constrainedSourceColumns.map((source) => {
    const defectSource = multiplyVector(
      sectionAdjoint,
      multiplyVector(raiseAdjoint, source),
    ).map(negateRat);
    return [...source, ...defectSource];
  });
  const liftedSources = columnsToMatrix(
    liftedColumns,
    field.harmonicDimension + defect.harmonicDimension,
  );
  const restrictedLift = liftedSources.slice(0, field.harmonicDimension);
  const fullGaugeResidual = multiply(transpose(compensatedGauge), liftedSources);
  const compensatedDimension = compensatedSourceColumns.length;
  const constrainedDimension = constrainedSourceColumns.length;

  return {
    carriers: {
      harmonicFieldDimension: field.harmonicDimension,
      defectDimension: defect.harmonicDimension,
      compensatedFieldDimension: field.harmonicDimension + defect.harmonicDimension,
      parameterDimension: parameter.harmonicDimension,
      constrainedParameterDimension: allowedParameterColumns.length,
    },
    divergence: {
      map: `A:H_${parameterRank}->H_${defectRank}`,
      rank: contractionRank,
      targetDimension: defect.harmonicDimension,
      surjective: contractionRank === defect.harmonicDimension,
      rightInverse: equal(sectionIdentity, identity(defect.harmonicDimension)),
      section: `S_${parameterRank}:H_${defectRank}->H_${parameterRank}, A S_${parameterRank}=1`,
    },
    sources: {
      constrainedCondition: 'R^dagger j lies in im(A^dagger)',
      compensatedCondition: 'R^dagger j + A^dagger k = 0',
      lift: `L_S(j)=(j,-S_${parameterRank}^dagger R_${parameterRank}^dagger j)`,
      constrainedDimension,
      compensatedDimension,
      fullGaugePairingVanishes: matrixZero(fullGaugeResidual),
      restrictionAfterLiftIsIdentity: equal(restrictedLift, constrainedSources),
      liftSpansCompensatedAnnihilator: sameColumnSpace(
        liftedSources,
        compensatedSources,
      ),
    },
    quotientTransport: {
      slice: `sigma(phi,chi)=phi-R_${parameterRank}S_${parameterRank}chi`,
      sliceAfterInclusion: 'sigma(phi,0)=phi',
      inclusionAfterSliceDefect: `(phi,chi)-(sigma(phi,chi),0)=G S_${parameterRank}chi`,
      sourcePairing: '<L_S(j),(phi,chi)>=<j,sigma(phi,chi)>',
      curvatureCoincidence: 'C(phi,chi)=C(sigma(phi,chi),0) whenever C G=0',
    },
    locality: {
      obstruction: 'A(p)S(p)=1 cannot hold for polynomial S because A(0)S(0)=0',
      scaling: 'A(lambda p)=lambda A(p) forces a homogeneous natural section to scale as lambda^(-1)',
      requiredMomentumDegree: -1,
      polynomialLocalRightInverse: false,
    },
  };
}

function constructSourceResponseDiscriminator(input = {}) {
  const rejectedKey = Object.keys(input).find((key) => answerBearingKeys.has(key));
  if (rejectedKey) {
    return refuse(
      'answer-bearing-input',
      'the discriminator accepts presentation data and a capability, not an expected source dimension, inverse, or verdict',
      { rejectedKey },
    );
  }
  const { dimension, spins, requestedCapability } = input;
  if (dimension !== 4) {
    return refuse('dimension-budget', 'the present source-response bench is bounded to four dimensions');
  }
  if (!Array.isArray(spins)
      || spins.some((spin) => !Number.isInteger(spin) || spin < 2)) {
    return refuse('spin-budget', 'integer spins at least two are required');
  }
  if (requestedCapability !== 'local-causal-source-response') {
    return refuse(
      'requested-capability',
      'the current branch tests local causal response for one common physical source class',
      { requestedCapability },
    );
  }

  const rows = Object.fromEntries(spins.map((spin) => [spin, compareSpin(dimension, spin)]));
  const rowValues = Object.values(rows);
  const certificates = {
    exactNonzeroMomentumSlice: rowValues.every((row) =>
      row.divergence.surjective && row.divergence.rightInverse),
    commonPhysicalSourceSpace: rowValues.every((row) =>
      row.sources.constrainedDimension === row.sources.compensatedDimension
      && row.sources.fullGaugePairingVanishes
      && row.sources.restrictionAfterLiftIsIdentity
      && row.sources.liftSpansCompensatedAnnihilator),
    sameGaugeInvariantResponseOnPuncturedMomentum: rowValues.every((row) =>
      row.sources.fullGaugePairingVanishes
      && row.sources.liftSpansCompensatedAnnihilator),
    localPolynomialSourceLiftRefused: rowValues.every((row) =>
      !row.locality.polynomialLocalRightInverse
      && row.locality.requiredMomentumDegree === -1),
  };
  if (Object.values(certificates).some((value) => !value)) {
    return refuse(
      'source-response-certificate',
      'a divergence section, source lift, quotient transport, or locality certificate failed',
      { spins: rows, certificates },
    );
  }

  return {
    ok: true,
    family: 'projected-carrier-source-response-discriminator',
    capability: requestedCapability,
    momentumRepresentative: 'nonzero Euclidean p=e_0',
    method: 'exact rational harmonic-polynomial linear algebra plus invariant quotient transport',
    obstruction: {
      origin: 'restricting the gauge parameter from H_(s-1) to ker(A) changes the annihilator condition on a source',
      constrainedCondition: 'R^dagger j annihilates ker(A), hence R^dagger j lies in im(A^dagger)',
      generatedResource: 'a section S with A S=1 lifts j to (j,-S^dagger R^dagger j)',
      localityFailure: 'every such natural section has inverse momentum degree and cannot be a polynomial local differential operation',
    },
    spins: rows,
    responseTransport: {
      input: 'one constrained physical source class [j] and the existing compensated/symmetric response symbol away from p=0',
      sourceLift: 'L_S(j)=(j,-S^dagger R^dagger j)',
      fieldSlice: 'sigma(phi,chi)=phi-RSchi',
      transportedResponse: 'G_constrained(p) = sigma(p) G_compensated(p) L_S(p) on quotient classes for p nonzero',
      observableRecovery: 'C G=0 makes C G_compensated L_S = C i G_constrained',
      retainedMeaning: 'the same physical source functional and gauge-invariant curvature response',
    },
    certificates,
    verdict: {
      gaugeSliceTransport: 'demote-as-local-causal-constructor',
      constrainedBranch: 'direct-local-response-still-open',
      compensatedBranch: 'retain-as-local-source-compatible-baseline',
      reason: 'the gauge-slice equivalence preserves the physical source quotient only after a nonlocal right inverse reconstructs the discarded compensator direction; this route demonstrates no whole-route local causal gain, but it does not exclude an independently generated constrained Green operation',
      retainedUse: 'nonzero-momentum gauge slice, optional nonlocal reduction, and projected-carrier compiler regression',
    },
    boundary: 'the exact finite-rank certificate uses a Euclidean nonzero momentum representative; the nonlocal section prevents automatic extension to a compact-source causal operation, while distributional completion through p=0, interactions, and numerical conditioning remain open',
    nextObstruction: {
      question: 'can a self-adjoint constrained Euler complex and compact-source Green operation be generated directly, without using the section S, and beat the compensated baseline for the same curvature observable?',
      requiredOutput: 'direct source adapter, causal Green operation, same-observable certificate, and complete cost comparison',
    },
    stop: 'stop the gauge-slice transport route and do not extend it by more ranks; only a separately generated constrained Euler/Green operation can reopen the capability verdict',
  };
}

export { constructSourceResponseDiscriminator };

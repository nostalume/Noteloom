const parameters = {
  mechanicalEnergy: -1.0,
  evenEnergy: 1.2,
  oddEnergy: 2.5,
  preparationCoupling: 0.4,
  tangentCoupling: 0.7,
  bareMass: 3.0,
};

const tolerance = 1e-10;
const finiteDifferenceTolerance = 2e-6;

function assertClose(name, actual, expected, tol = tolerance) {
  const error = Math.abs(actual - expected);
  if (error > tol) {
    throw new Error(`${name}: error ${error} exceeds ${tol}`);
  }
  return error;
}

function dot(x, y) {
  return x.reduce((sum, value, index) => sum + value * y[index], 0);
}

function norm(x) {
  return Math.sqrt(dot(x, x));
}

function normalize(x) {
  const size = norm(x);
  return x.map((value) => value / size);
}

function lowestEigenvalue3(matrix) {
  const a = matrix.map((row) => [...row]);
  for (let sweep = 0; sweep < 80; sweep += 1) {
    let p = 0;
    let q = 1;
    let largest = Math.abs(a[p][q]);
    for (let i = 0; i < 3; i += 1) {
      for (let j = i + 1; j < 3; j += 1) {
        if (Math.abs(a[i][j]) > largest) {
          p = i;
          q = j;
          largest = Math.abs(a[i][j]);
        }
      }
    }
    if (largest < 1e-15) break;

    const angle = 0.5 * Math.atan2(2 * a[p][q], a[q][q] - a[p][p]);
    const cosine = Math.cos(angle);
    const sine = Math.sin(angle);
    const app = a[p][p];
    const aqq = a[q][q];
    const apq = a[p][q];

    a[p][p] = cosine * cosine * app - 2 * sine * cosine * apq + sine * sine * aqq;
    a[q][q] = sine * sine * app + 2 * sine * cosine * apq + cosine * cosine * aqq;
    a[p][q] = 0;
    a[q][p] = 0;

    for (let r = 0; r < 3; r += 1) {
      if (r === p || r === q) continue;
      const arp = a[r][p];
      const arq = a[r][q];
      a[r][p] = cosine * arp - sine * arq;
      a[p][r] = a[r][p];
      a[r][q] = sine * arp + cosine * arq;
      a[q][r] = a[r][q];
    }
  }
  return Math.min(a[0][0], a[1][1], a[2][2]);
}

function matrixAt(t) {
  const {
    mechanicalEnergy: h,
    evenEnergy: a,
    oddEnergy: c,
    preparationCoupling: b,
    tangentCoupling: w,
    bareMass: mass,
  } = parameters;
  const kinetic = (t * t) / (2 * mass);
  return [
    [h + kinetic, b, 0],
    [b, a + kinetic, w * t],
    [0, w * t, c + kinetic],
  ];
}

const {
  mechanicalEnergy: h,
  evenEnergy: a,
  oddEnergy: c,
  preparationCoupling: b,
  tangentCoupling: w,
  bareMass: mass,
} = parameters;

const discriminant = Math.sqrt((h - a) ** 2 + 4 * b ** 2);
const energy = (h + a - discriminant) / 2;
const fullState = normalize([b, energy - h, 0]);
const oddResponseDenominator = c - energy;
const directCurvature =
  1 / mass - (2 * w ** 2 * fullState[1] ** 2) / oddResponseDenominator;

const qEven = b / (energy - a);
const recoveredState = normalize([1, qEven, 0]);
const secularResidual = energy - h - b * qEven;
const recoveryError = Math.min(
  norm(recoveredState.map((value, index) => value - fullState[index])),
  norm(recoveredState.map((value, index) => value + fullState[index])),
);

const qOddPrime = (w * qEven) / (energy - c);
const qEvenSecond =
  (qEven / mass + 2 * w * qOddPrime) / (energy - a);
const sigmaSecond = b * qEvenSecond;
const sigmaEnergyDerivative = -(qEven ** 2);
const feshbachCurvature =
  (1 / mass + sigmaSecond) / (1 - sigmaEnergyDerivative);

const step = 1e-3;
const e0 = lowestEigenvalue3(matrixAt(0));
const ePlus = lowestEigenvalue3(matrixAt(step));
const eMinus = lowestEigenvalue3(matrixAt(-step));
const ePlus2 = lowestEigenvalue3(matrixAt(2 * step));
const eMinus2 = lowestEigenvalue3(matrixAt(-2 * step));
const finiteDifferenceCurvature =
  (-ePlus2 + 16 * ePlus - 30 * e0 + 16 * eMinus - eMinus2) /
  (12 * step ** 2);

const checks = {
  originEigenvalue: assertClose("origin eigenvalue", e0, energy),
  secularEquation: assertClose("Feshbach secular equation", secularResidual, 0),
  recoveredState: assertClose("recovered eigenvector", recoveryError, 0),
  routeEquality: assertClose(
    "direct versus Feshbach curvature",
    feshbachCurvature,
    directCurvature,
  ),
  finiteDifference: assertClose(
    "finite difference versus direct curvature",
    finiteDifferenceCurvature,
    directCurvature,
    finiteDifferenceTolerance,
  ),
};

console.log(JSON.stringify({
  parameters,
  energy,
  directCurvature,
  feshbachCurvature,
  finiteDifferenceCurvature,
  checks,
}, null, 2));

import {
  addRat,
  divideRat,
  isZero,
  multiplyRat,
  rat,
  ratText,
  solveLinear,
} from '../10c-generative-residual-constructor/residual-constructor.mjs';

const ZERO = rat(0);
const ONE = rat(1);
const answerBearingKeys = new Set([
  'expectedDepth',
  'expectedLayers',
  'expectedVerdict',
  'inversePolynomial',
]);

function refuse(phase, reason, details = {}) {
  return { ok: false, phase, reason, ...details };
}

function equalRat(left, right) {
  return isZero(addRat(left, rat(-right.n, right.d)));
}

function power(value, exponent) {
  let output = ONE;
  for (let index = 0; index < exponent; index += 1) {
    output = multiplyRat(output, value);
  }
  return output;
}

function evaluatePolynomial(coefficients, value) {
  return coefficients.reduceRight(
    (output, coefficient) => addRat(coefficient, multiplyRat(value, output)),
    ZERO,
  );
}

function recurrenceCoefficient(spin, label) {
  let coefficient = ZERO;
  for (let rank = label; rank < spin; rank += 1) {
    const rho = divideRat(rat(rank), rat(rank + 1));
    coefficient = addRat(ONE, multiplyRat(rho, coefficient));
  }
  return coefficient;
}

function closedCoefficient(spin, label) {
  const numerator = spin * (spin + 1) - label * (label + 1);
  return divideRat(rat(numerator), rat(2 * spin));
}

function interpolateInverse(layers) {
  const degreeBudget = layers.length - 1;
  const vandermonde = layers.map((layer) =>
    Array.from({ length: degreeBudget + 1 }, (_, degree) =>
      power(layer.divergenceCoefficientValue, degree)));
  const targets = layers.map((layer) => (
    layer.role === 'gauge' ? ZERO : divideRat(ONE, layer.eulerEigenvalueValue)
  ));
  const coefficients = solveLinear(vandermonde, targets);
  if (!coefficients) throw new Error('spectral inverse interpolation failed');
  let degree = coefficients.length - 1;
  while (degree > 0 && isZero(coefficients[degree])) degree -= 1;
  return { coefficients: coefficients.slice(0, degree + 1), targets, degree };
}

function polynomialText(coefficients) {
  const terms = [];
  coefficients.forEach((coefficient, degree) => {
    if (isZero(coefficient)) return;
    const scalar = ratText(coefficient);
    if (degree === 0) terms.push(scalar);
    else if (degree === 1) terms.push(`${scalar} B`);
    else terms.push(`${scalar} B^${degree}`);
  });
  return terms.join(' + ').replaceAll('+ -', '- ') || '0';
}

function compareSpin(spin) {
  const layers = Array.from({ length: spin + 1 }, (_, label) => {
    const recurrence = recurrenceCoefficient(spin, label);
    const closed = closedCoefficient(spin, label);
    const eigenvalue = addRat(ONE, rat(-closed.n, closed.d));
    const role = label === spin - 1
      ? 'gauge'
      : (label === spin ? 'transverse-physical' : 'longitudinal-physical-source');
    return {
      label,
      carrier: `X_(${spin},${label})=R_${spin - 1}...R_${label} ker(A:H_${label}->H_${label - 1})`,
      stabilizerDimension: 2 * label + 1,
      divergenceCoefficient: ratText(closed),
      eulerEigenvalue: ratText(eigenvalue),
      role,
      inverseCoefficient: role === 'gauge'
        ? null
        : ratText(divideRat(ONE, eigenvalue)),
      divergenceCoefficientValue: closed,
      recurrenceValue: recurrence,
      eulerEigenvalueValue: eigenvalue,
    };
  });
  const inverse = interpolateInverse(layers);
  const closedDivergenceCoefficient = layers.every((layer) =>
    equalRat(layer.divergenceCoefficientValue, layer.recurrenceValue));
  const spectralInverseIdentity = layers.every((layer, index) => {
    const value = evaluatePolynomial(inverse.coefficients, layer.divergenceCoefficientValue);
    return equalRat(value, inverse.targets[index]);
  });
  const gaugeLayer = layers[spin - 1];
  const gaugeLayerAnnihilated = isZero(
    evaluatePolynomial(inverse.coefficients, gaugeLayer.divergenceCoefficientValue),
  );

  return {
    equation: {
      operator: `D_${spin}=Q-R_${spin - 1}A`,
      adjointOrigin: 'the Fischer pairing makes the harmonic projection of P adjoint to A, hence R^dagger=A and D^dagger=D',
      gaugeParameter: `ker(A:H_${spin - 1}->H_${spin - 2})`,
      gaugeIdentity: `D_${spin} R_${spin - 1} epsilon=0 when A epsilon=0`,
    },
    layers: layers.map((layer) => {
      const {
        divergenceCoefficientValue,
        recurrenceValue,
        eulerEigenvalueValue,
        ...publicLayer
      } = layer;
      return publicLayer;
    }),
    generatedInverse: {
      normalizedOperator: `B_${spin}=R_${spin - 1}A/Q`,
      response: `G_D=(1/Q) f_${spin}(B_${spin}) on the source annihilator`,
      polynomial: polynomialText(inverse.coefficients),
      polynomialDegree: inverse.degree,
      gaugePrescription: `f_${spin}(1)=0`,
      physicalPrescription: `f_${spin}(c_l)=1/(1-c_l) for l!=${spin - 1}`,
    },
    cost: {
      maximumScalarGreenDepth: inverse.degree + 1,
      compensatedBaselineDepth: 1,
      constrainedComponentGreenLoad: (inverse.degree + 1) * (spin + 1) ** 2,
      compensatedComponentGreenLoad: 2 * spin ** 2 + 2,
      genericLayerSeparationRequired: true,
      preparedSingleLayerDepth: 1,
      interpretation: 'each power of B contributes one additional Q inverse; the outer response contributes one more',
    },
    certificates: {
      closedDivergenceCoefficient,
      spectralInverseIdentity,
      gaugeLayerAnnihilated,
      uniqueGaugeLayer: layers.filter((layer) => layer.role === 'gauge').length === 1,
      layerDimensionsComplete: layers.reduce(
        (sum, layer) => sum + layer.stabilizerDimension,
        0,
      ) === (spin + 1) ** 2,
    },
  };
}

function constructDirectConstrainedGreen(input = {}) {
  const rejectedKey = Object.keys(input).find((key) => answerBearingKeys.has(key));
  if (rejectedKey) {
    return refuse(
      'answer-bearing-input',
      'the direct Green constructor accepts the generated harmonic algebra and a capability, not a supplied layer decomposition, inverse, depth, or verdict',
      { rejectedKey },
    );
  }
  const { dimension, spins, requestedCapability } = input;
  if (dimension !== 4) {
    return refuse('dimension-budget', 'the closed layer recurrence is presently derived for four dimensions');
  }
  if (!Array.isArray(spins)
      || spins.some((spin) => !Number.isInteger(spin) || spin < 2)) {
    return refuse('spin-budget', 'integer spins at least two are required');
  }
  if (requestedCapability !== 'generic-compact-source-causal-response') {
    return refuse(
      'requested-capability',
      'the present bench compares a generic compact physical-source response with the compensated scalar-Green baseline',
      { requestedCapability },
    );
  }

  const rows = Object.fromEntries(spins.map((spin) => [spin, compareSpin(spin)]));
  const values = Object.values(rows);
  const certificates = {
    directConstructionAvoidsDivergenceSection: true,
    allLayerRecurrencesClosed: values.every((row) =>
      row.certificates.closedDivergenceCoefficient),
    allSpectralInversesExact: values.every((row) =>
      row.certificates.spectralInverseIdentity
      && row.certificates.gaugeLayerAnnihilated
      && row.certificates.uniqueGaugeLayer
      && row.certificates.layerDimensionsComplete),
    genericRouteExceedsBaselineDepth: values.every((row) =>
      row.cost.maximumScalarGreenDepth > row.cost.compensatedBaselineDepth
      && row.cost.constrainedComponentGreenLoad > row.cost.compensatedComponentGreenLoad),
  };
  if (Object.values(certificates).some((value) => !value)) {
    return refuse(
      'direct-green-certificate',
      'a layer recurrence, quotient inverse, gauge removal, or route-cost certificate failed',
      { spins: rows, certificates },
    );
  }

  return {
    ok: true,
    family: 'direct-constrained-harmonic-green',
    capability: requestedCapability,
    construction: {
      input: 'the projected harmonic operations R,A,Q and the restricted parameter ker A',
      layerGenerator: 'start with v_l in ker A and raise it to X_(s,l)=R_(s-1)...R_l v_l',
      recurrence: 'c_(r+1,l)=1+[r/(r+1)]c_(r,l), c_(l,l)=0',
      closedLaw: 'A X_(s,l)=([s(s+1)-l(l+1)]/(2s)) Q X_(s-1,l)',
      eulerSpectrum: 'D X_(s,l)=([l(l+1)-s(s-1)]/(2s)) Q X_(s,l)',
      inverseGenerator: 'interpolate f_s on the finite invariant spectrum, set the gauge value to zero, and return Q^(-1)f_s(RA/Q)',
    },
    spins: rows,
    causalContract: {
      theoremInput: 'retarded/advanced scalar-wave powers exist on flat Minkowski space and retain the chosen causal support',
      use: 'replace each Q^(-k) in the generated rational symbol by the corresponding boundary-selected scalar-wave power',
      sameObservable: 'causal uniqueness on the physical quotient and the N10q source isomorphism identify the resulting gauge-invariant curvature with the compensated route',
      boundary: 'the executable certifies the invariant spectrum and rational inverse, not distributional kernel construction or wavefront estimates',
    },
    certificates,
    verdict: {
      genericCompactSource: 'dominated-in-declared-green-load',
      preparedSingleLayer: 'conditional-one-green-reentry',
      reason: 'a generic constrained source must be separated into invariant layers; on the declared component-Green metric the generated response has depth s+1 and load (s+1)^3, whereas the compensated source adapter has depth one and load 2s^2+2',
      retainedTool: 'a direct quotient Green generator and an exact refusal of generic whole-route compression',
    },
    stop: 'the generic projected-carrier response comparison is closed; re-enter only for a preparation that supplies one invariant layer, or for a discretization where the generated layer projectors improve conditioning enough to repay their Green depth',
  };
}

export { constructDirectConstrainedGreen };

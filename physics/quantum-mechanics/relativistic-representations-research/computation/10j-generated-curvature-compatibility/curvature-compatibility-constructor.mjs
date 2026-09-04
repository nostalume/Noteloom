function refuse(phase, reason, details = {}) {
  return { ok: false, phase, reason, ...details };
}

function wedge(left, right) {
  return left[0] * right[1] - left[1] * right[0];
}

function polynomialMultiply(left, right) {
  const output = Array(left.length + right.length - 1).fill(0);
  for (let i = 0; i < left.length; i += 1) {
    for (let j = 0; j < right.length; j += 1) output[i + j] += left[i] * right[j];
  }
  return output;
}

function polynomialScale(polynomial, scalar) {
  return polynomial.map((coefficient) => coefficient * scalar);
}

function polynomialPower(polynomial, power) {
  let output = [1];
  for (let i = 0; i < power; i += 1) output = polynomialMultiply(output, polynomial);
  return output;
}

function spinorPolynomial(spinor) {
  return [spinor[0], spinor[1]];
}

function bivectorPlus(momentum, vector) {
  return polynomialScale(
    polynomialMultiply(
      spinorPolynomial(momentum.left),
      spinorPolynomial(vector.left),
    ),
    wedge(momentum.right, vector.right),
  );
}

function bivectorMinus(momentum, vector) {
  return polynomialScale(
    polynomialMultiply(
      spinorPolynomial(momentum.right),
      spinorPolynomial(vector.right),
    ),
    wedge(momentum.left, vector.left),
  );
}

function curvatureOnDecomposable(momentum, fieldSlots) {
  const plus = fieldSlots.reduce(
    (output, vector) => polynomialMultiply(output, bivectorPlus(momentum, vector)),
    [1],
  );
  const minus = fieldSlots.reduce(
    (output, vector) => polynomialMultiply(output, bivectorMinus(momentum, vector)),
    [1],
  );
  return { plus, minus };
}

function transformSpinor(matrix, spinor) {
  return [
    matrix[0][0] * spinor[0] + matrix[0][1] * spinor[1],
    matrix[1][0] * spinor[0] + matrix[1][1] * spinor[1],
  ];
}

function transformVector(leftMatrix, rightMatrix, vector) {
  return {
    left: transformSpinor(leftMatrix, vector.left),
    right: transformSpinor(rightMatrix, vector.right),
  };
}

function transformHomogeneous(polynomial, matrix) {
  const degree = polynomial.length - 1;
  const oldX = [matrix[0][0], matrix[1][0]];
  const oldY = [matrix[0][1], matrix[1][1]];
  let output = Array(degree + 1).fill(0);
  for (let yPower = 0; yPower <= degree; yPower += 1) {
    const monomial = polynomialMultiply(
      polynomialPower(oldX, degree - yPower),
      polynomialPower(oldY, yPower),
    );
    output = output.map((coefficient, index) =>
      coefficient + polynomial[yPower] * monomial[index]);
  }
  return output;
}

function boundedMultiplicityTrace(spin, maximumDegree) {
  const trace = [];
  for (let degree = 0; degree <= maximumDegree; degree += 1) {
    const maximumLeftSpin = (degree + spin) / 2;
    const multiplicity = degree < spin ? 0 : (degree === spin ? 1 : null);
    trace.push({
      degree,
      maximumLeftSpin,
      targetLeftSpin: spin,
      multiplicity,
      reason: degree < spin
        ? 'the source cannot reach left spin s'
        : 'the top traceless momentum and field factors contain the target once',
    });
  }
  return trace;
}

function validateInput(input) {
  if (!Number.isInteger(input.spin) || input.spin < 1) {
    return refuse('physical-target', 'spin must be a positive integer');
  }
  if (!input.potentialSystem?.ok || !input.potentialSystem.fieldSystem) {
    return refuse(
      'potential-presentation',
      'a generated symmetric-potential field system is required',
      { missingResources: ['potentialSystem.fieldSystem'] },
    );
  }
  const resources = input.resources ?? {};
  if (!resources.symmetricAlgebra || !resources.chiralBivectorSplit
      || !resources.alternatingForms?.left || !resources.alternatingForms?.right) {
    return refuse(
      'chiral-resources',
      'symmetric multiplication, both alternating spinor forms, and the chiral bivector split are required',
      {
        missingResources: [
          ...(!resources.symmetricAlgebra ? ['symmetricAlgebra'] : []),
          ...(!resources.chiralBivectorSplit ? ['chiralBivectorSplit'] : []),
          ...(!resources.alternatingForms?.left ? ['alternatingForms.left'] : []),
          ...(!resources.alternatingForms?.right ? ['alternatingForms.right'] : []),
        ],
      },
    );
  }
  return null;
}

function constructCurvatureCompatibility(input = {}) {
  const invalid = validateInput(input);
  if (invalid) return invalid;

  const maximumDegree = input.maxDerivativeOrder ?? input.spin;
  if (!Number.isInteger(maximumDegree) || maximumDegree < 0) {
    return refuse(
      'derivative-budget',
      'maxDerivativeOrder must be a nonnegative integer',
      { maximumDegree },
    );
  }
  const multiplicityTrace = boundedMultiplicityTrace(input.spin, maximumDegree);
  if (maximumDegree < input.spin) {
    return refuse(
      'polynomial-lift',
      'the derivative budget cannot reach the direct chiral carrier',
      {
        spin: input.spin,
        requiredDerivativeOrder: input.spin,
        maximumDegree,
        multiplicityTrace,
      },
    );
  }

  const spin = input.spin;
  const provenance = [
    input.potentialSystem.grammarProvenance ?? 'generated symmetric-potential system',
    'N2b chiral bivector split',
    'minimal-degree Lorentz multiplicity obstruction',
  ].join(' -> ');

  return {
    ok: true,
    family: 'parity-paired-integer-spin-curvature-compatibility',
    spin,
    inputCarrier: `ker(T^2) in Sym^${spin}(V*)`,
    outputCarrier: `Sym^${2 * spin}(S) direct-sum Sym^${2 * spin}(bar S)`,
    derivativeOrder: spin,
    provenance,
    multiplicityTrace,
    operation: {
      plus: `K_${spin}^+(p)(v_1 symmetric-product ... symmetric-product v_${spin}) = symmetric-product_i b_+(p,v_i)`,
      minus: `K_${spin}^-(p)(v_1 symmetric-product ... symmetric-product v_${spin}) = symmetric-product_i b_-(p,v_i)`,
      bivectors: 'b_+ and b_- are the two Hodge-chiral projections of p wedge v',
    },
    certificates: {
      minimalDegree: true,
      multiplicityAtMinimalDegree: 1,
      gaugeAnnihilation: 'K_s(p) P_p epsilon=0 because every polarized term contains b_+(p,p)=b_-(p,p)=0',
      traceInvisibility: 'the lower H_(s-2) trace layer cannot reach chiral weight (s,0) or (0,s) at degree s',
      physicalShellLines: 'at p=lambda tensor bar(lambda), the two screen endpoint lines map nontrivially to lambda^(2s) and bar(lambda)^(2s)',
    },
    evaluateNullDecomposable(momentum, fieldSlots) {
      if (fieldSlots.length !== spin) {
        throw new Error(`expected ${spin} symmetric field slots, received ${fieldSlots.length}`);
      }
      return curvatureOnDecomposable(momentum, fieldSlots);
    },
    boundary: {
      supported: 'local polynomial potential-to-chiral-curvature map and physical-shell quotient isomorphism',
      unsupported: 'no polynomial local inverse, sourced curvature Green complex, or interacting deformation is generated',
    },
  };
}

export {
  bivectorMinus,
  bivectorPlus,
  constructCurvatureCompatibility,
  curvatureOnDecomposable,
  polynomialMultiply,
  transformHomogeneous,
  transformVector,
};

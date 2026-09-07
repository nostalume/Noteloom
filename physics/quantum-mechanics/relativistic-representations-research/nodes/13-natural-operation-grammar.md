# Natural-operation and residual-repair compiler

Status: bounded symmetric, exterior, and Clifford requests generate operations,
repairs, certificates, or typed refusals

## Obstruction

A residual solver is only verification if its tokens and identities already encode
the desired equation. Operations must first be generated from the carrier law and
admitted resources; only then may failure construct a correction.

## Generate the grammar

Input contains no field name or expected equation:

```text
carrier law: symmetric or exterior free power, optional coefficient action
resources: metric, invariant tensors, or Clifford factorization
budget: word length and rank range
```

Functorial multiplication and derivation generate raising/lowering maps. Metric
duality generates trace and insertion only when supplied. Exterior exchange
generates its sign. Evaluating composites on one symmetric tensor constructs

```text
A P-P A=Q+U T-sensitive rank term,
```

with its coefficient obtained from the power law. Exterior power instead gives

```text
A P=-P A+Q,  P^2=A^2=0.
```

For a first-order `G`, polarization of `G(p)^2=Q(p)I` generates the Clifford
relation without a component matrix.

Orient relations by a declared decreasing word order, enumerate only inside the
budget, reduce, and verify

```text
N(N(w))=N(w).
```

Missing resources, nondecreasing rules, unresolved bounded ambiguities, and
insufficient depth produce typed refusals.

## Let the obstruction generate repair

Given candidate maps `R_0,D_0`, compute

```text
r=N(D_0R_0).
```

Generate a typed correction basis `b_i` from the grammar and set

```text
D=D_0+sum_i c_i b_i,
N(DR_0)=r+sum_i c_i N(b_iR_0).
```

Collecting independent normal words gives an exact linear system over `QQ`.
Solving it constructs the coefficients, parameter constraints, or inconsistency.
The same operation handles several meanings of failure:

- complete cancellation returns a generated operator;
- a conditional solution returns its parameter constraint and failed channel;
- a residual absorbable by a new field generates its transformation and coupled
  equation;
- pairing/adjoint failure generates a source adapter or Euler multiplier;
- bounded Clifford words carry fermionic repair through the same interface.

## Retained interface and proof

```text
CompileOperation(carrier_law, resources, request, budget)
 -> grammar + generated maps + constraints + provenance
    + normal-form certificates
 | refusal(reason, residual channels, unresolved words, required resources).
```

The proof is internal to the reusable output:

```text
N(DR)=0,
N(source compatibility residual)=0,
N(Euler adjoint residual)=0.
```

A consumer uses the returned maps without replaying the derivation. Regression
covers scalar, vector, spin two, spin `1/2`, and spin `3/2`, while transfer across
symmetric and Clifford grammars tests that the compiler is not one memorized
formula.

Completeness is relative to the generated finite basis and budget. Arbitrary
invariant-map discovery, mixed symmetry, interaction consistency, and the
carrier-global problem remain open. [Node 15](15-carrier-source-obstructions.md)
tests whether generated presentations and observables actually reduce work.

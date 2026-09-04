# Projected-Carrier Operation Contracts

Status: primary-source boundary for N10n; the sources motivate traceless projectors,
Fischer decomposition, and generalized gradients, while N10n owns its obstruction
derivation and exact finite Hom-space calculation

## `PC-01` — Traceless projection is a genuine representation-theoretic operation

- Source: D. V. Bulgakova, Y. O. Goncharov, and T. Helpin,
  [Construction of the traceless projection of tensors via the Brauer algebra](https://arxiv.org/abs/2212.14496).
- Locator: Introduction and Sections 3--4.
- Contract: for tensor powers equipped with a nondegenerate invariant metric,
  contractions and permutations generate the Brauer centralizer algebra; traceless
  projection can be constructed systematically and can be made compatible with
  projection to a chosen `GL`-irreducible tensor symmetry.
- Research use: supports treating `ker T` and more general trace-free Young
  carriers as constructed projected representations, rather than as a decorative
  field constraint.
- Boundary: N10n does not import the paper's closed projector. It derives the
  rank-one momentum-raising correction from failure to preserve `ker T` and uses
  the source only to delimit the broader mixed-projector horizon.

## `PC-02` — Harmonic tensors are the trace-free Fischer summands

- Source: Roman Lavicka and Dalibor Smid,
  [Fischer decomposition for polynomials on superspace](https://arxiv.org/abs/1508.03426).
- Locator: Introduction, especially the classical-form decomposition and the
  invariant `sl(2)` operators recalled in Section 2.
- Contract: in the ordinary bosonic specialization, homogeneous polynomials split
  into harmonic pieces multiplied by powers of the metric quadratic form; the
  Laplacian, metric multiplication, and Euler degree operator form the invariant
  `sl(2)` algebra underlying this decomposition.
- Research use: justifies the polynomial realization
  `H_r=ker T subset Sym^r(V*)` and the invariant algebra `{T,U,E}` used by N10n.
- Boundary: the source's superspace exceptional regimes are outside this bench.
  N10n works in ordinary dimension at least three and derives all momentum
  relations directly.

## `PC-03` — Projected first-order maps are generalized gradients

- Source: Sergey Stepanov and Irina Tsyganok,
  [Extensions and Applications of Stein-Weiss Operators to Traceless Symmetric Tensor](https://arxiv.org/abs/2512.09605).
- Locator: abstract and the decomposition of the covariant derivative of a
  symmetric trace-free tensor.
- Contract: first-order operators on symmetric trace-free tensors arise by
  projecting the tensor product with a covector into irreducible orthogonal-group
  summands; their adjoint compositions support invariant second-order identities.
- Research use: prevents N10n from claiming novelty for projected gradients as
  objects. Its contribution is the compiler interface: generate the projection
  coefficient from the preservation obstruction, expose the omitted summand, and
  pass the rank-indexed relation to a downstream residual calculation.
- Boundary: the source is Riemannian and geometric. N10n's flat symbol algebra and
  computability verdict are independently constructed.

## Current source verdict

The sources establish that trace-free projectors, harmonic decomposition, and
projected gradients are established tools. They do not provide the answer-bearing
input used by N10n. The node's supported claim is narrower and operational:

```text
carrier constraint T f=0
  -> failure of raw insertion
  -> generated correction and rank-indexed relation
  -> independent finite Hom-space completeness check
  -> downstream residual and typed missing-carrier obstruction.
```

## `PC-04` — Trace constraints belong to a presentation, not automatically to the particle

- Source: D. Francia and A. Sagnotti,
  [Minimal Local Lagrangians for Higher-Spin Geometry](https://arxiv.org/abs/hep-th/0507144).
- Locator: abstract and the local compensator construction.
- Contract: the Fronsdal presentation uses trace restrictions on fields and gauge
  parameters; removing those restrictions requires additional compensator and
  multiplier carriers in a local formulation. Thus constrained and unconstrained
  presentations trade algebraic restrictions against extra fields.
- Research use: prevents N10n from promoting `H_r` to a consequence of the
  particle representation. N10o must state the requested carrier/interface
  capability first, then let the residual choose between a parameter constraint,
  an added compensator, or reconsideration of the projected presentation.
- Boundary: N10o's compensator is generated for its own harmonic projected
  residual and is not identified with the full Fronsdal compensator system.

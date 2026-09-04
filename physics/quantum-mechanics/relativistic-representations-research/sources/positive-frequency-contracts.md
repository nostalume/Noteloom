# Positive-Frequency and One-Particle Contracts

Recorded: 2026-08-29  
Used by: [bosonic free-field machine](../nodes/06-bosonic-free-field-machine.md) and [fermionic free-field machine](../nodes/07-fermionic-free-field-machine.md)

This packet binds only the analytic statements that are not consequences of the
finite-spin polynomial complexes. node 06 and node 07 construct their shell maps, quotient
independence, positivity, and Poincare intertwining internally.

## PF-01 — Fourier form of the wave causal propagator

- **Source:** Christian Baer, [Green-hyperbolic operators on globally hyperbolic
  spacetimes](https://arxiv.org/abs/1310.0738), *Communications in Mathematical
  Physics* 333 (2015), 1585--1615.
- **Input used:** the scalar wave operator on Minkowski spacetime, its unique
  retarded and advanced Green operators, and their causal difference.
- **Output consumed from the source:** existence, uniqueness, causal support, and
  exact-sequence properties of the causal difference.
- **Internal Minkowski computation in node 06:** the retarded and advanced scalar
  multipliers are the two boundary prescriptions for `1/p^2`. Applying
  `1/(x+i0)-1/(x-i0)=-2 pi i delta(x)` separately at `p^0>0` and `p^0<0` gives a
  nonzero convention-dependent multiple of

  ```text
  sign(p^0) delta(p^2).
  ```

  Thus its two connected nonzero shell components are the future and past null
  cones with opposite signs. The source supplies the analytic Green operators;
  the displayed Fourier identity is not attributed to it without computation.
- **Boundary:** the exact scalar coefficient depends on the Fourier convention and
  on whether the causal propagator is defined as advanced minus retarded or the
  reverse. node 06 retains one real nonzero normalization constant instead of hiding
  this choice.

## PF-02 — Positive-energy arbitrary-helicity Hilbert realization

- **Source:** Fernando Lledo, [Massless relativistic wave equations and quantum
  field theory](https://arxiv.org/abs/math-ph/0303031), *Annales Henri Poincare* 5
  (2004), 607--670.
- **Input used:** the positive light cone with invariant measure, a massless
  canonical/Wigner representation, a covariant test-function representation, and
  an intertwining constraint that removes the excess covariant fiber.
- **Output consumed:** for arbitrary discrete helicity, constrained
  test-function embeddings are continuous into a one-particle Hilbert space that
  carries the positive-energy massless Wigner representation. The paper also
  distinguishes the finite covariant test-function fiber from the canonical
  one-particle fiber.
- **Research use:** independent evidence that the route

  ```text
  covariant test function -> constrained future-shell amplitude ->
  one-particle completion
  ```

  is the correct analytic kind of bridge. node 06 does not import Lledo's spinor
  formulas or use them as a proof for the symmetric-potential source quotient.
  node 07 uses the paper's Weyl and arbitrary odd-rank fermionic cases as an external
  check, while constructing its own spinor-screen metric and potential-source map.
- **Boundary:** continuity and density must be checked for the particular source
  map being used. The paper's arbitrary-helicity construction does not by itself
  prove density of node 06's compact, projected-conserved symmetric sources.

## PF-03 — Identification with the induced representation

- **Sources:** Eugene Wigner, [On unitary representations of the inhomogeneous
  Lorentz group](https://doi.org/10.2307/1968551), *Annals of Mathematics* 40
  (1939); G. W. Mackey, [Imprimitivity for Representations of Locally Compact
  Groups I](https://doi.org/10.1073/pnas.35.9.537), *PNAS* 35 (1949), 537--545.
- **Input used:** one positive-energy orbit, its invariant measure, a unitary
  little-group fiber, and the covariant momentum spectral measure.
- **Output consumed:** the completed orbit-section action is the induced
  Poincare representation, and the imprimitivity theorem supplies the converse
  identification under the regularity hypotheses already recorded in N2.
- **Boundary:** these theorems type the target representation. They do not create
  the local field equation, the source quotient, or the dense source map.

## PF-04 — Support-completion theorem

For each fixed finite integer `s>=1`, the completion problem separates into two
claims:

```text
(a) faithfulness:
    W_s[J]=0 implies J=E_s a for one compact smooth a;

(b) density:
    the future-shell restrictions of compact smooth J with R_s^dagger J=0,
    modulo J=E_s a, are dense in
    L2(O_+,dmu_0;Sym_0^s(Q_p tensor C)^*).
```

Claim (a) is discharged in
[bosonic free-field machine](../nodes/06-bosonic-free-field-machine.md). The complete finite-type
compatibility complex converts zero shell cohomology into a spacelike-compact
gauge parameter, because its degree-one support obstruction is

```text
H_sc^1(M;Kill_s)~=H_c^1(R^3;Z_s)=0.
```

The detailed theorem bindings are recorded in the
[support-faithfulness packet](support-faithfulness-contracts.md).

Claim (b) remains open. Two admissible proof routes are:

1. construct compactly supported physical Cauchy data, lift them through the
   gauge constraint, and use density in the finite-energy norm; or
2. show that an `L2` shell section annihilating every admissible compact source
   defines the zero distributional solution, then use node 06's source/solution
   duality.

node 06 proves that pointwise screen exactness alone was insufficient for (a), then
supplies the missing support-preserving lift. Consequently node 06's norm is faithful
on the original real causal quotient. Until (b) is proved, its completion is the
**closed invariant image** inside the N3 Hilbert space, not automatically the
whole induced space.

## PF-05 — Fermionic two-shell typing

- **Source:** Fernando Lledo, PF-02, especially the Weyl construction and its
  extension to odd spinor rank.
- **Output consumed:** half-integer massless covariant test functions embed into
  positive-energy one-particle spaces; fermionic quantization uses CAR data, and
  the particle construction has two canonical one-particle sectors.
- **Internal construction in node 07:** the positive spinor metric is derived from the
  null Clifford homotopy and the time-oriented Dirac current. The source amplitude
  is `res_p(S_n(p)M_n^(-1)J_hat(p))`; future data and conjugated past data are then
  separated algebraically into particle and antiparticle sectors.
- **Boundary:** the source does not prove that every shellwise gauge amplitude for
  node 07's symmetric spinor-tensor potential has one spacelike-compact gauge lift.
  It also does not discharge density for this particular compact-source image.

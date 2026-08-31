# Quantization and One-Particle Recovery Contracts

Recorded: 2026-08-30  
Used by: [N4y quantization--recovery bridge](../nodes/04y-quantization-recovery-bridge.md)
and [N4z fermionic CAR coincidence](../nodes/04z-fermionic-car-coincidence.md)

This packet binds the analytic and operator-algebra statements needed to connect
the already constructed causal source quotients to quantum field algebras and to
recover their one-particle images. N4y constructs the same-source coincidence and
its boundary internally.

## QR-01 — One-particle structure and bosonic Fock realization

- **Source:** Igor Khavkine and Valter Moretti, [Algebraic QFT in Curved
  Spacetime and quasifree Hadamard states: an
  introduction](https://arxiv.org/abs/1412.5945), Proposition 11 and Theorem
  2.1.
- **Inputs consumed:** a real symplectic solution space, a positive real form
  compatible with the symplectic form, and the resulting one-particle structure
  `K:Sol->H`.
- **Output consumed:** the corresponding quasifree GNS representation is the
  symmetric Fock space over `H`; the vacuum is the zero-particle vector; and the
  smeared free field is the sum of annihilation and creation operators applied to
  the one-particle image.
- **Internal use:** N4y substitutes N4g's already constructed faithful map `W_s`
  for `K`, evaluates the field on the vacuum, and projects the resulting vector to
  the positive shell. The source does not prove that N4g's particular compact
  source image is dense in the whole N3 Wigner space.
- **Boundary:** the theorem is stated for the scalar Klein--Gordon field. The
  Fock/one-particle theorem is used abstractly after N4g has independently
  constructed the higher-spin symplectic and positive structures; locality and
  gauge faithfulness remain owned by N4f/N4h.

## QR-02 — CCR/CAR quantization of linear gauge systems

- **Source:** Thomas-Paul Hack and Alexander Schenkel, [Linear bosonic and
  fermionic quantum gauge theories on curved
  spacetimes](https://arxiv.org/abs/1205.3484), Proposition 4.1, Definitions
  4.2--4.4, Proposition 4.9, Definition 4.10, and Section 5.
- **Inputs consumed:** the observable quotient of a linear bosonic gauge theory
  with its causal presymplectic form, or a fermionic observable quotient with a
  positive real inner product.
- **Output consumed:** the bosonic quotient admits a CCR/Weyl quantization; a
  positive-type fermionic quotient admits a self-dual CAR quantization; field
  equations and gauge equivalence are encoded in the observable classes rather
  than imposed after quantization.
- **Internal use:** N4y computes the CCR directly from N4g's inner product and
  constructs the self-dual CAR representation from N4k's positive realification.
  N4z supplies the missing internal equality witness: the source/causal-Green
  form is reduced to N4k's positive two-shell form on the same source pair.
- **Boundary:** positivity is a real restriction for fermionic gauge systems; a
  formally Hermitian field equation alone does not guarantee a physical CAR
  representation. Existence of the abstract algebra does not choose a state,
  vacuum, or interacting dynamics.

## QR-03 — Representation-independent Dirac-field check

- **Source:** Ko Sanders, [The locally covariant Dirac
  field](https://arxiv.org/abs/0911.1304), especially the field-algebra and
  state constructions.
- **Output consumed:** the free Dirac field admits a representation-independent
  locally covariant algebraic construction, with Hilbert representations supplied
  after a state is chosen.
- **Research use:** this is the spin-`1/2` external regression for the fermionic
  branch. It supports the existence of a correct local CAR construction but does
  not by itself prove the normalization equality for N4k's all-rank
  spinor-screen map.

## QR-04 — Interacting particles are recovered asymptotically

- **Source:** Detlev Buchholz and Wojciech Dybalski, [Scattering in relativistic
  quantum field theory: basic concepts, tools, and
  results](https://arxiv.org/abs/math-ph/0509047), Sections 1--3.
- **Inputs consumed:** an interacting local quantum field theory with vacuum,
  positive-energy translations, a stable sharp particle subspace, and admissible
  interpolators satisfying the stated regularity conditions.
- **Output consumed:** the one-particle projection is recovered by time-smeared
  field operators; products with separated velocity supports construct isometric
  incoming and outgoing Fock embeddings.
- **Internal use:** N4y uses this only to type the interacting deformation of the
  free recovery diamond. The detailed stable-shell quotient remains in N4s and
  its existing `FP-01` contract.
- **Boundary:** the asymptotic Fock space need not equal the microscopic field
  Hilbert space, and asymptotic completeness is not automatic. Infraparticles,
  resonances, confinement, and collective response require different outputs.

## Supported boundary

The sources support the following distinction:

```text
linear physical quotient plus compatible positive structure
  -> CCR/CAR algebra and a chosen quasifree/Fock representation;

interacting field algebra plus state and stable shell
  -> extracted one-particle space and conditional asymptotic Fock embeddings.
```

They do not support an ordinal hierarchy in which a field equation is the endpoint
of representation theory or Fock quantization is automatically the fundamental
description of every interacting or collective regime.

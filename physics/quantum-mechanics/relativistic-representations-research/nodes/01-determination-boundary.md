# N1 — Poincare Determination Boundary

State: supported within the scope below  
Manuscript destination: Section 1, problem and determination boundary

## Question

Starting from Poincare symmetry, which data of a free relativistic particle and its
field equation are determined, and which data remain constructive choices?

## Scope and presumptions

The conclusion assumes:

- Minkowski spacetime and the proper orthochronous Poincare group (or its spin
  cover);
- a one-particle complex Hilbert space carrying a strongly continuous projective
  unitary representation;
- irreducibility, positive energy, and a single translation-spectrum orbit;
- either a positive-mass finite-spin sector or a massless finite-helicity sector;
- a free linear solution space when this particle representation is realized by a
  field equation.

Continuous-spin, tachyonic, reducible, interacting, curved-background, and
spontaneously broken sectors are outside the present conclusion. Parity, time
reversal, charge conjugation, and a reality condition are not included in the
proper orthochronous group and must be added separately.

## Bound material

- Manuscript lines 13--47: candidate Poincare and spin-cover conventions;
- manuscript lines 348--424: group-function expansion and the overstrong central
  claim under challenge;
- [Wigner 1939](https://doi.org/10.2307/1968551): unitary irreducible
  representations of the inhomogeneous Lorentz group;
- [Bekaert--Boulanger](https://arxiv.org/abs/hep-th/0611263): induced
  representation/little-group classification and covariant equations;
- [Weinberg 1969](https://doi.org/10.1103/PhysRev.181.1893): free fields in general
  irreducible Lorentz representations;
- [Weinberg 1964, massless fields](https://doi.org/10.1103/PhysRev.134.B882):
  restrictions from the massless little group and the nontrivial status of vector
  potentials;
- [Gitman--Shelepin source packet](../sources/gitman-shelepin-2000.md): different
  Lorentz realizations with the same mass/spin labels.

## Construction

The internal construction is developed in
[N2](02-three-representation-spaces.md), including the theorem contracts and
equations hidden by the compressed account below. Its semantic chain is:

```text
transition-probability symmetry
  -> projective unitary action on state vectors
  -> spin-cover representation
  -> strongly continuous translation representation
  -> joint spectral measure E(dp)
  -> momentum support
  -> Lorentz orbit (single-orbit presumption)
  -> residual standard-frame stabilizer
  -> induced physical representation.
```

The stabilizer of a chosen standard momentum is

```text
G_k = { Lambda | Lambda k = k }
```

and its irreducible unitary action `sigma` is transported over the orbit through
the associated state bundle constructed in `N2`. Thus the physical state
representation is classified by

```text
(momentum orbit O_k, little-group representation sigma),
```

with mass and spin/helicity as familiar labels in the sectors retained here.

This construction acts on physical states. A covariant field instead starts with a
Lorentz carrier `D`, an intertwiner from physical states into field-valued
functions or distributions, and usually equations/constraints or gauge
equivalences. Those objects are additional realization data.

## Supported result

**Determination boundary.** Within the stated scope, Poincare symmetry plus the
spectral and irreducibility assumptions determines the physical one-particle
representation up to equivalence through its orbit and little-group
representation. It does not uniquely determine:

- a finite- or infinite-dimensional Lorentz carrier for a field;
- whether the description uses a potential, curvature, tensor, spinor, auxiliary
  field, or scalar function on the full group;
- a particular local differential operator, its order, or a first-order
  factorization;
- subsidiary constraints, gauge redundancy, parity completion, or a reality
  condition;
- an action, normalization, interaction, coupling rule, or off-shell completion.

A chosen carrier and desired physical representation constrain possible
intertwiners and equations, sometimes strongly. That is a construction problem,
not a consequence of the group classification alone.

## Why the stronger manuscript claim fails

The statement at manuscript line 424 identifies all relativistic wave equations
with invariant eigenvalue problems on scalar functions on the Poincare group. The
sources support that construction as one generating realization, not as the unique
definition of a relativistic equation. In particular:

- Gitman--Shelepin explicitly admit finite-dimensional nonunitary and
  infinite-dimensional unitary Lorentz realizations with the same mass/spin data;
- Weinberg constructs free fields in general Lorentz carriers, so the carrier is a
  realization choice constrained by its relation to particle states;
- massless little groups make covariant potentials and physical helicity states
  non-identical objects, exposing the need for redundancy or a noncovariant
  transformation law in familiar potential descriptions;
- Casimir eigenvalues can label a sector but do not by themselves specify the
  carrier, multiplicity, locality, or gauge quotient.

## Manuscript proposition

The first section may safely use the following thesis:

> Poincare symmetry classifies one-particle state representations by momentum
> orbits and little-group representations. A relativistic field equation is an
> additional covariant construction whose physical solution space must realize the
> selected state representation. Scalar functions on the Poincare group provide
> one candidate generating realization, whose bridge to ordinary fields must be
> constructed and checked.

## Checks

- **Assumption check:** removing positive energy, irreducibility, or the
  single-orbit restriction enlarges the representation class, so the conclusion is
  not stated without them.
- **Massless check:** helicity assumes the translation-like part of the massless
  little group acts trivially; continuous-spin representations are explicitly
  excluded.
- **Discrete-symmetry check:** the proper orthochronous group does not force parity
  pairing or field reality.
- **Realization check:** `GS-09` supplies distinct Lorentz realizations for the same
  mass/spin labels, refuting uniqueness of the field realization.
- **Falsifier:** a theorem deriving a unique carrier and local operator solely from
  the scoped representation datum, without further locality/minimality/field
  assumptions, would revise this boundary. No bound source supplies such a theorem.

## Output and edges

The result exported to `N2` and `N3` is:

```text
input fixed by classification:
  orbit + little-group representation

realization data still to construct:
  field space + carrier + intertwiner + equation/complex + physical quotient
```

The open question passed to `N3` is not “which equation is dictated by symmetry?”
but “which realization maps recover the classified physical representation, with
what locality, multiplicity, and computational cost?”

# Lorentz-Carrier Theorem Contracts

Status: source packet for `N2a/N2b`; sources delimit theorem contracts and do not
replace the node's internal constructions

## `LC-01` — Spin cover and representation scope

- Source: Xavier Bekaert and Nicolas Boulanger, [The unitary representations of
  the Poincare group in any spacetime dimension](https://arxiv.org/html/hep-th/0611263v2),
  Section 1.1.
- Locator: Section 1.1, especially the paragraphs defining the proper
  orthochronous Lorentz group and `Spin(D-1,1)` as its double cover for `D>=4`.
- Contract: in four dimensions, single- and double-valued Lorentz
  representations are treated as genuine representations of the spin cover.
- Boundary: this source does not construct the particular
  `SL(2,C)->SO^+(1,3)` map used by N2b.

## `LC-02` — Concrete spinor covering map

- Source: Jonas Larsson and Karl Larsson, [The Lorentz group and the Kronecker
  product of matrices](https://arxiv.org/abs/2110.15118), Section 3.
- Locator: Section 3.2, equations (33)–(39), for the homomorphism, Lorentz-form
  preservation, and invariant alternating form; conclusion for the two-to-one
  map.
- Imported check: the action induced by `A tensor bar A` covers the restricted
  Lorentz group twice.
- Internal replacement: N2b constructs the action on `Herm(S)`, computes its
  kernel invariantly, and proves compatibility with the chosen spin cover.

## `LC-03` — Particle labels live on stability subgroups

- Source: Bekaert and Boulanger, same notes as `LC-01`.
- Locator: Sections 3.1–3.3; the table in Section 3.3 identifies the massive
  stability subgroup as `SO(D-1)` and the massless subgroup as `ISO(D-2)`.
- Contract: an induced Poincare representation is classified by a momentum orbit
  and a unitary representation of its stability subgroup.
- Internal replacement: N2 constructs the standard-momentum ambiguity; N2a
  constructs the intrinsic null-stabilizer exact sequence and physical fiber; N2b
  only restricts a carrier along that subgroup.

## `LC-04` — Finite helicity and null translations

- Source: Steven Weinberg, [Massless Particles in Higher
  Dimensions](https://arxiv.org/abs/2010.05823), Introduction, equations (1)–(2)
  and the following discussion.
- Corroborating locator: Bekaert–Boulanger Sections 3.3 and 5.3.1, where helicity
  corresponds to trivial action of the massless little group's translations.
- Contract: a finite-helicity field-state matrix element lies in the sector fixed
  by the invariant Abelian subgroup of the null little group.
- Boundary: this does not say that every carrier contains the desired direct
  line. N2b constructs an extremal line; gauge subquotients remain in N3/N4a.

## `LC-05` — Algebraic classification contracts

- Source: Pavel Etingof et al., [Introduction to Representation
  Theory](https://arxiv.org/abs/0901.0827), Section 2.15 for finite-dimensional
  `sl(2)` representations; the tensor-product statement is the standard
  Clebsch–Gordan consequence of this classification.
- Contract A: a three-dimensional complex simple Lie algebra is
  `sl(2,C)`.
- Contract B: finite-dimensional irreducible `sl(2,C)` modules are symmetric
  powers of its fundamental two-dimensional module.
- Contract C: their tensor products obey the multiplicity-one Clebsch–Gordan
  decomposition.
- Research use: these standard theorems certify completeness. N2b independently
  constructs the Hodge ideals, carrier functors, invariant inclusion maps, and
  dimension witness.
- Boundary: these contracts imply neither unitarity of finite Lorentz carriers nor
  locality, field equations, or statements about infinite-dimensional carriers.

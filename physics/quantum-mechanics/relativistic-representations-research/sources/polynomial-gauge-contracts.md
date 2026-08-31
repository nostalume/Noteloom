# Polynomial Gauge-Resolution Contracts

Status: source packet for `N4a/N4b`; the source bounds comparison claims and does not
replace the node's polynomial-lift or fiber computations

## `PG-01` — Module-to-gauge construction

- Source: K. B. Alkalaev, M. Grigoriev, and I. Yu. Tipunin,
  [Massless Poincare modules and gauge invariant equations](https://arxiv.org/abs/0811.3999).
- Locator: Introduction and Section 2, especially the construction of the parent
  system and the ghost-number-zero BRST cohomology.
- Contract: for the class of indecomposable massless Poincare modules treated in
  the paper, the parent/BRST construction produces a local free gauge system whose
  gauge structure is organized by the BRST differential.
- Boundary: this is not a theorem that an arbitrary prescribed `K_k`-complex,
  finite carrier list, or differential-order bound admits a polynomial lift.

## `PG-02` — Reduction is part of equivalence

- Source: the same paper.
- Locator: Section 3, where reduction of the parent formulation recovers the
  Labastida equations; see also the introduction's distinction between parent,
  unfolded, and metric-like forms.
- Contract: eliminating generalized auxiliary or contractible pairs can relate
  different local presentations of the same free module.
- Boundary: adding an arbitrary contractible polynomial pair or applying a field
  redefinition can change differential order, characteristic strata, or locality
  of inverse maps. N4a therefore records these costs rather than treating every
  quasi-isomorphism as equally economical.

## `PG-03` — Physical Wigner content requires an independent check

- Source: the same paper.
- Locator: Section 4 and the momentum-space check described in the introduction.
- Contract: the gauge-inequivalent solutions of the constructed system are checked
  against the irreducible Poincare module induced from the relevant Wigner
  little-group representation.
- Research use: corroborates N4a's insistence that polynomial covariance and a
  gauge identity do not by themselves establish the physical fiber.
- Internal completion: N4a now performs this computation for the symmetric
  bosonic integer-spin complex through an intrinsic screen exact sequence.
- Boundary: PG-03 and the N4a bosonic proof do not cover arbitrary mixed-symmetry
  or half-integer potential complexes; N4b and PG-04 treat the symmetric
  half-integer branch separately.

## `PG-04` — Symmetric half-integer potential data

- Source: J. Fang and C. Fronsdal,
  [Massless fields with half-integral spin](https://doi.org/10.1103/PhysRevD.18.3630),
  _Physical Review D_ 18 (1978), 3630--3633.
- Locator: the four-page paper's definition of the rank-`n` Rarita--Schwinger
  spinor-tensor, its triple spinor-trace constraint, and its gauge transformation
  with spinor-traceless parameter.
- Contract: the constrained symmetric spinor-tensor equation is a local gauge
  formulation intended to transmit the massless half-integer spin sector.
- Internal completion: N4b reconstructs its auxiliary-variable symbol from the
  Clifford action, proves the gauge identity, and computes the little-group
  cohomology and characteristic set.
- Boundary: neither the source contract nor N4b supplies an action comparison,
  massive deformation, mixed-symmetry fermion, or interacting theory.

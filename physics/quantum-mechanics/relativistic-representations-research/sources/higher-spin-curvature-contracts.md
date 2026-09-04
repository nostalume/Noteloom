# Source contracts — higher-spin curvature and gauge compatibility

Consumed by: [carrier/source obstructions](../nodes/15-carrier-source-obstructions.md).

Status: primary-source boundary for node 15; its chiral construction,
physical-shell calculation, compatible source complex, and normalization remain
internal

## HS-CURV-01 — Generalized differential complex

- Source: Xavier Bekaert and Nicolas Boulanger, [Tensor gauge fields in arbitrary
  representations of `GL(D,R)`: duality and Poincare
  lemma](https://arxiv.org/abs/hep-th/0208058).
- Authority: primary mathematical-physics paper proving a generalized Poincare
  lemma for tensor gauge fields through `N`-complexes.
- Exact input used: flat spacetime, polynomial/local tensor gauge transformations,
  and Young-projected generalized differentials.
- Exact output used: higher-spin curvatures belong to a systematic generalized
  differential complex; local exactness requires the theorem's Young-diagram and
  regularity hypotheses.
- Boundary: node 15 does not import the paper's full mixed-symmetry complex or claim
  curved-background exactness. It internally constructs only the symmetric
  four-dimensional chiral output needed by the current spine.

## HS-CURV-02 — Curvature generates local gauge invariants

- Source: Xavier Bekaert and Nicolas Boulanger, [Gauge invariants and Killing
  tensors in higher-spin gauge theories](https://arxiv.org/abs/hep-th/0505068).
- Authority: primary classification of local gauge-invariant functions for free
  completely symmetric tensor gauge fields, on and off shell.
- Exact input used: local functions of a free symmetric gauge potential on flat
  spacetime.
- Exact output used: generalized curvature and its derivatives own the local
  gauge-invariant content under the paper's constrained/unconstrained hypotheses.
- Boundary: this classification validates the capability target; it does not
  construct node 15's minimal-degree chiral map or its selector cost.

## HS-CURV-03 — Derivative order and geometric equations

- Source: Dario Francia and Augusto Sagnotti, [Free geometric equations for higher
  spins](https://arxiv.org/abs/hep-th/0207002).
- Authority: primary construction relating symmetric higher-spin dynamics to the
  de Wit--Freedman generalized curvatures.
- Exact input used: a symmetric spin-`s` gauge potential on flat spacetime.
- Exact output used: the generalized curvature contains `s` derivatives, while
  obtaining unconstrained geometric equations from its traces can introduce
  inverse powers of the wave operator beyond the Maxwell/Einstein cases.
- Boundary: node 15 generates the local forward curvature observable, not those
  nonlocal kinetic equations, an unconstrained action, or an interacting theory.

## HS-CURV-04 — Curvature/Fronsdal differential identity

- Source: Johan Engquist and Olaf Hohm, [Geometry and dynamics of higher-spin
  frame fields](https://arxiv.org/abs/0708.1391).
- Authority: primary derivation of flat and AdS Damour--Deser identities for
  arbitrary symmetric bosonic spin.
- Exact input used: the generalized higher-spin curvature and the corresponding
  Fronsdal tensor on flat spacetime.
- Exact output used: the higher-derivative curvature equation is a projected chain
  of curls of the Fronsdal tensor; in flat space the identity is locally integrable.
- Boundary: node 15 does not import the paper's frame variables, AdS corrections, or
  unconstrained compensator theory. It internally constructs the four-dimensional
  chiral source complex and uses the flat identity only as an independent theorem
  contract for the generated source-lift syzygy.

## Worktable use

These contracts prevent four overclaims:

1. recovering a familiar curvature formula is not presented as novel;
2. the local forward curvature map is not confused with a local inverse or a new
   curvature-based source/Green complex;
3. a four-dimensional chiral construction is not promoted to the full
   mixed-symmetry generalized Poincare lemma.
4. a potential-derived compatible chiral source is not promoted to an arbitrary
   matter coupling or interacting higher-spin current.

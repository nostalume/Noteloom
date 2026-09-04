# Fermionic Action and Green Contracts

Recorded: 2026-08-29  
Used by: [fermionic free-field machine](../nodes/07-fermionic-free-field-machine.md) and [fermionic free-field machine](../nodes/07-fermionic-free-field-machine.md)

## FH-01 — Constrained Fang--Fronsdal action

- **Source:** J. Fang and C. Fronsdal, [Massless fields with half-integral
  spin](https://doi.org/10.1103/PhysRevD.18.3630), *Physical Review D* 18
  (1978), 3630--3633.
- **Input used:** a symmetric rank-`n` spinor-tensor, triple gamma-trace field
  constraint, gamma-traceless rank-`n-1` gauge parameter, and the first-order
  Fang--Fronsdal equation.
- **Output consumed:** this constrained system admits a local gauge-invariant
  quadratic action for each finite half-integer spin.
- **Internal obligation:** node 07 constructs the Dirac--Fischer pairing, proves the
  trace reversal invertible in four dimensions, computes the formal-adjoint
  defect, and derives the source condition. These facts are not imported merely
  from the existence of the historical action.
- **Boundary:** the source does not select a Majorana real form, positivity,
  causal support class, or countable-spin completion.

## FH-02 — Arbitrary-rank Lagrangian comparison

- **Source:** I. L. Buchbinder, V. A. Krykhtin, and A. Pashnev, [BRST approach to
  Lagrangian construction for fermionic massless higher spin
  fields](https://arxiv.org/abs/hep-th/0410215), *Nuclear Physics B* 711 (2005),
  367--391.
- **Output consumed:** an arbitrary finite half-integer-spin BRST Lagrangian
  reduces in four dimensions, after partial gauge fixing and auxiliary-field
  elimination, to the constrained Fang--Fronsdal Lagrangian.
- **Research use:** independent all-rank evidence that the constrained Euler
  representative is not a low-spin accident.
- **Boundary:** the unconstrained BRST carrier has auxiliary fields and reducible
  gauge structure. node 07 does not identify it with the constrained carrier without
  the stated reduction.

## FH-03 — Green-hyperbolic gauge theorem and spin-three-halves check

- **Source:** Thomas-Paul Hack and Alexander Schenkel, [Linear bosonic and
  fermionic quantum gauge theories on curved
  spacetimes](https://arxiv.org/abs/1205.3484), *General Relativity and
  Gravitation* 45 (2013), 877--910.
- **Output consumed:** a formally self-adjoint gauge operator with compatible
  Green-hyperbolic gauge completion produces causal observables and a
  source/solution construction. Their Rarita--Schwinger example uses an invertible
  gamma-trace reversal; after gauge completion its field and parameter operators
  are of Dirac or wave type.
- **Research use:** low-spin and analytic boundary for node 07. node 07's all-rank flat
  identities are derived internally and are not attributed to the spin-`3/2`
  example.
- **Output additionally consumed by node 07:** the source/solution quotient theorem
  follows from Green-hyperbolic gauge compatibility. node 07 reconstructs the needed
  flat all-rank support argument directly from the wave exact sequence rather than
  assuming that its constrained operators fit the abstract theorem automatically.

## FH-04 — Dirac and wave Green operators

- **Sources:** Christian Baer, [Green-hyperbolic operators on globally hyperbolic
  spacetimes](https://arxiv.org/abs/1310.0738), *Communications in Mathematical
  Physics* 333 (2015), 1585--1615; Hack and Schenkel, FH-03, Section 2.
- **Output consumed:** normally hyperbolic operators and Dirac-type operators have
  unique retarded and advanced Green operators with causal support; their causal
  propagators satisfy the standard exact sequence. The wave Green maps extend
  uniquely to past-compact and future-compact sections, which is the support
  operation used in node 07's temporal-cutoff construction.
- **Internal flat-space use:** node 07 needs only the scalar wave Green maps on the
  finite-rank constrained bundles. Its identity

  ```text
  S_n^2+2R_nB_n=q identity
  ```

  then constructs the fermionic sourced response without an explicit propagator
  numerator.
- **Boundary:** this contract does not prove the half-integer gauge quotient by
  itself; node 07 supplies the missing constructions. It also does not prove
  positive-frequency faithfulness or density.

## Supported source boundary

The literature supports the constrained all-rank action family, the general
Green-hyperbolic gauge framework, and the complete spin-`3/2` example. The uniform
four-dimensional identities for `M_n`, `B_n`, and the admissible-source response
are internal results of node 07. node 07 proves causal quotient bijectivity from those
identities and wave support exactness. node 07 separately constructs the positive
particle/antiparticle completion, and node 07 proves its gauge-rank shell-map
faithfulness. node 07 closes causal-Euler/CAR normalization downstream. Density and
countable-spin estimates remain separate claims.

# Finite-Spin Green Contracts

Consumed by: [bosonic free-field machine](../nodes/06-bosonic-free-field-machine.md).

Recorded: 2026-08-29  
Role: independent analytic and spin-two boundaries for node 06; the uniform flat-space
integer-spin construction remains internal to nodes 05 and 06

## FG-01 — Linearized-gravity Green contract

Christopher J. Fewster and David S. Hunt, [Quantization of linearized gravity in
cosmological vacuum spacetimes](https://arxiv.org/abs/1203.0261), *Reviews in
Mathematical Physics* 25 (2013), 1330003,
[DOI](https://doi.org/10.1142/S0129055X13300033).

- **Hypotheses:** linearized Einstein gravity on a globally hyperbolic cosmological
  vacuum background, with trace reversal and de Donder gauge.
- **Output used:** the de Donder equation is normally hyperbolic; it has unique
  retarded and advanced Green operators; gauge transformations intertwine the
  vector and symmetric-tensor wave operators; divergence-free compact test tensors
  generate gauge-invariant observables and causal solution representatives.
- **Independent check:** the flat, zero-cosmological-constant specialization agrees
  with node 06's spin-two completion and source quotient.
- **Boundary:** transverse-traceless gauge has additional global obstructions, and
  phase-space nondegeneracy depends on background topology. node 06 uses de Donder, not
  TT gauge, and stays on Minkowski spacetime.

## FG-02 — Abstract linear gauge contract

Thomas-Paul Hack and Alexander Schenkel, [Linear bosonic and fermionic quantum
gauge theories on curved spacetimes](https://arxiv.org/abs/1205.3484), *General
Relativity and Gravitation* 45 (2013), 877-910,
[DOI](https://doi.org/10.1007/s10714-013-1508-y).

- **Hypotheses:** a formally self-adjoint linear equation operator, a gauge map,
  compatible gauge fixing, and Green-hyperbolicity of the completed operators.
- **Output used:** causal propagators descend from gauge-invariant compact sources
  to solution classes and define a gauge-invariant presymplectic structure.
- **Semantic bridge:** Green compatibility belongs to a typed gauge complex, not to
  an isolated inverse matrix.
- **Boundary:** the theorem does not establish the node 05 trace-constrained identities;
  node 06 must construct those internally for every finite `s`.

## FG-03 — Symmetric integer-spin action contract

C. Fronsdal, [Massless fields with integer
spin](https://doi.org/10.1103/PhysRevD.18.3624), *Physical Review D* 18 (1978),
3624-3629.

- **Hypotheses:** a double-traceless symmetric rank-`s` potential and traceless
  rank-`s-1` gauge parameter on flat spacetime.
- **Output used:** a local gauge-invariant quadratic action and its projected source
  conservation law.
- **Internal construction already supplied:** node 05 constructs `R,C,D` and their
  shell cohomology; node 05 constructs `M`, its inverse, the constrained pairing,
  formal self-adjointness, and the Euler operator `E=M D`.
- **Boundary:** the historical action does not by itself prove causal Green
  compatibility or a countable-spin completion.

## Extraction rule

node 06 may use MG-01's causal exact sequence and FG-01/FG-02 as theorem contracts for
Green-hyperbolic analysis. Every finite-spin carrier identity, source transformation,
quotient map, and shell coincidence must be evaluated inside node 06.

# Structured seed compression before raw tensor enumeration

## Inquiry and frozen contract `C_G1_v1`

G0 constructs an infinitesimal stabilizer as a simultaneous defect kernel, but its
canonical `End(V)` seed and raw tensor codomains grow as `d^2` and `d^r`.  G1 asks
whether structure already present in the supplied tensors can reduce both spaces
*before* elimination, without supplying the expected Lie algebra or its basis.

The frozen input is the existing three-dimensional elasticity bench.  Its metric,
constitutive tensor, observable, tolerance, and resource accounting are unchanged.
No new physical example may alter the constructor during this probe.

Three live routes are compared:

1. **Raw route `R`:** `End(V)` candidates and every ordered tensor component.
2. **Metric seed `M`:** construct candidates from alternating covariant two-forms
   by `omega -> g^{-1} omega`, so metric preservation is satisfied by construction.
3. **Permutation target `P`:** retain one coordinate per declared tensor-symmetry
   orbit: `Sym^2(V*)` for rank two and `Sym^2(Sym^2(V*))` for elasticity.

`M` and `P` begin as alternatives because either might fail independently.  They
may be composed only if each has its own exact completeness witness.

## Constructive laws

For a nondegenerate symmetric metric, the map

```text
Lambda^2(V*) -> End(V),       omega -> A=g^{-1}omega
```

has image exactly the metric defect kernel.  Indeed,

```text
gA=omega  =>  A^T g + gA = omega^T+omega=0,
A^T g+gA=0 => omega=gA is alternating and A=g^{-1}omega.
```

Thus this seed has dimension `d(d-1)/2`, not `d^2`, and its origin is the supplied
metric rather than an algebra label.

For a tensor whose declared permutation group is `Pi`, the infinitesimal tensor
action commutes with every slot permutation in `Pi`.  Therefore a `Pi`-invariant
input has a `Pi`-invariant residual.  Evaluating one canonical multi-index per
`Pi`-orbit is complete: omitted coordinates are equal to retained coordinates,
not silently discarded.  The exact target dimensions are

```text
Sym^2(V*):             d(d+1)/2,
Sym^2(Sym^2(V*)):      m(m+1)/2,  m=d(d+1)/2.
```

The compiler must still certify the remaining kernel, visible quotient, bracket,
and closure.  The raw route remains an independent comparison whenever its budget
admits it.

## Frozen discriminators

- **Semantic equality:** raw and structured final generator matrices span the same
  exact subspace whenever both routes complete.
- **Compression:** for `d=3`, the structured elasticity route has 3 candidates and
  a 21-coordinate constitutive residual, versus 9 candidates and raw metric plus
  elasticity targets of dimensions 9 and 81.
- **Transfer within the frozen input:** the former candidate budget 8 must admit the
  structured route even though it refuses the raw route.
- **Adversarial control:** the axis dyad must still lower the structured kernel from
  three generators to one; a candidate budget below three must remain unresolved.
- **Use:** the same two-projector propagator observable must stay within `1e-12` of
  the independent dense eigensolve.
- **Cost:** compare complete one-time arithmetic proxies and recompute break-even;
  do not claim measured runtime dominance.

The candidate is falsified if it encodes the expected stabilizer basis, loses a raw
kernel direction, treats a nondeclared symmetry as exact, moves enumeration into
an opaque decomposition oracle, or changes the observable contract.

## Executable design

```text
metric_seed(g):
    invert g exactly
    for each i<j:
        omega <- elementary alternating two-form(i,j)
        emit g^{-1} omega
    certify A^T g + g A = 0 for every emitted A

canonical_targets(tensor_signature):
    symmetric-2 -> indices i<=j
    elasticity  -> unordered pairs (i<=j) <= (k<=l)
    otherwise refuse the structured route

compile_route(candidates, tensors, target_policy, budget):
    construct Leibniz residual columns on canonical targets
    compile simultaneous kernel + visible quotient + bracket closure
    return exact witness or typed refusal

compare(raw, structured):
    if both exact: certify equality of generated matrix spans
    if structured exact and raw budget-refused: retain the raw refusal as evidence
    select the least-cost exact route; never convert refusal into no symmetry
```

The implementation slice is bounded to the existing tensor grammar: the generic
seed/compression module stays at or below 300 source lines and the input/use adapter
at or below 550; exact elimination stays owned by the shared defect compiler.
General tensor-symmetry parsing, indefinite metrics, jets, nonlinear symmetries,
and analytic Fourier inversion remain outside `C_G1_v1`.

## Evidence ledger

- `E-G1-01` (deductive witness + exact test): `omega -> g^-1 omega` generates
  three candidates in dimension three and certifies the metric defect identically.
  The same constructor passes for the non-orthonormal exact metric
  `diag(2,3,5)`. Symmetry-orbit targets have dimensions 21 for elasticity and 6
  for a symmetric dyad.
- `E-G1-02` (independent route comparison): whenever both routes are admitted,
  their generated matrix spans are exactly equal. The frozen elasticity kernel
  has dimension three; the axis dyad lowers both routes to the same
  one-dimensional kernel. Closure and the effective bracket pass exactly.
- `E-G1-03` (cost/use/adversarial): the raw route remains at cost proxy 1638,
  while the composed `M+P` route costs `3*21+54=117`. The former candidate budget
  8 now admits the structured result while recording raw refusal; budget 2 still
  returns `CandidateBudgetExceeded`. The observable error remains
  `4.996003610813204e-16`, and proxy break-even moves from 103 to 8 queries.

## Disposition

`M` and `P` are not rival final routes: the probe shows that they remove different
axes of work and compose. `C_G1_v1` is **supported bounded** for positive-definite
metrics and the declared symmetric-two/elasticity tensor signatures. This is exact
semantic and human compression plus conditional arithmetic-proxy leverage; runtime
dominance was not measured.

The remaining weakness is no longer raw tensor size. The adapter still chooses a
metric-first rule and assigns one of two known symmetry tags. Promotion beyond this
domain therefore requires a typed relation planner that derives admissible seed and
codomain functors from signatures and completeness laws, rather than another
physics-kind branch.

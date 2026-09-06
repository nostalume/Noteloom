# Lazy compositional tensor quotients

## Frozen contract `C_G3_v1`

G2 generates routes from relations, but its generic orbit constructor visits all
`d^r` indices and the benchmark materializes both routes. G3 asks whether a compact
quotient expression can generate only retained coordinates and admit resources
before any defect block exists.

Two alternatives remain live on the unchanged elasticity tensors and observable:

1. **Permutation-orbit canonicalization:** exact and generic for a supplied finite
   slot-permutation group, but bounded by `d^r |Pi|` comparison work.
2. **Compositional quotient expression:** build coordinate modules recursively
   from typed operations. The admitted constructor is `SymmetricPower(X,k)` with
   atomic `Slot(V*)`.

The expressions are

```text
metric and dyad:  SymmetricPower(Slot, 2),
elasticity:       SymmetricPower(SymmetricPower(Slot, 2), 2).
```

These are relation data, not physics names or expected Lie-algebra information.

## Semantic computation

If `Coords(X)` is a canonically ordered coordinate basis, define

```text
Coords(SymmetricPower(X,k))
    = combinations_with_replacement(Coords(X), k), flattened.
dim SymmetricPower(X,k) = binomial(dim X + k - 1, k).
```

Thus for `dim V=3`,

```text
dim Sym^2(V*) = binomial(4,2)=6,
dim Sym^2(Sym^2(V*)) = binomial(7,2)=21.
```

Construction emits 6 or 21 coordinates directly. Exact equality with G2's
permutation-orbit representatives is required in an explicit audit, but that audit
cost is not charged to the selected operational route.

A route plan is a symbolic blueprint containing candidate dimension, target
dimensions, quotient expressions, dependencies, and cost bounds. Admission checks
candidate, residual, and bracket bounds before `DefectBlock` materialization.
Operational execution materializes only the cheapest admitted plan. An input flag
may request independent raw-span and permutation-orbit audit; the witness must state
which policy ran.

## Frozen discriminators

- The quotient constructor emits exactly the independent G2 target tuples for the
  six-coordinate dyad and 21-coordinate elasticity modules.
- Operational structured planning work falls from the G2 bound 648 to 21 emitted
  coordinates; selected planning-plus-compiler proxy becomes `21+117=138`.
- Symbolic candidate budget 2 refuses before candidates, targets, or defects are
  materialized. Candidate budget 8 admits only the structured route.
- Without explicit audit, the raw defect route is not materialized. With audit,
  raw/structured stabilizer spans and compositional/orbit coordinate sets agree
  exactly and audit cost remains separately reported.
- Stabilizer dimensions `3` and `1`, exact bracket, wave channels, and observable
  error remain unchanged. The full-route proxy break-even becomes 9 queries;
  stabilization-only break-even 8 remains separately labeled.
- A certified permutation relation lacking a quotient expression returns
  `MissingQuotientConstructor` for the compositional route; it never silently falls
  back to exhaustive orbit construction in operational mode.

The candidate is falsified if it embeds elasticity-specific code, generates raw
indices internally, performs defect work before budget admission, executes an
unselected route without an audit request, or changes the frozen observable.

## Pseudocode and code boundary

```text
coordinates(Slot, d):
    emit (0),...,(d-1)

coordinates(SymmetricPower(child,k), d):
    child_coords <- coordinates(child,d)
    for tuple in combinations_with_replacement(child_coords,k):
        emit flatten(tuple)

plan(relations):
    emit symbolic raw and compositional blueprints
    compute dimensions and cost bounds without tensors defects

admit(plan,budget):
    check candidate_dimension, sum(target_dimensions), bracket_upper_bound
    return admitted or typed unresolved

execute(selected_plan):
    materialize candidates, quotient targets, defects, action, bracket
    compile kernel and closure
    if explicit audit:
        execute raw plan and generic orbit comparison separately
```

The quotient core remains below roughly 120 source lines; planner below roughly
360; adapter below roughly 450. The domain covers recursive symmetric powers of one
covariant slot. Exterior powers, signs, traces, mixed variance, arbitrary Young
functors, spinors, jets, nonlinear symmetry, and analytic integration remain open.

## Evidence ledger

### `E-G3-01` — quotient construction

The recursive constructor emits 6 dyad coordinates and 21 elasticity coordinates
without first constructing 9 or 81 raw tuples. In the explicit independent audit,
those 21 coordinates equal the permutation-orbit representatives exactly. The
audit performs 648 orbit comparisons; operational construction performs 21 emits.

### `E-G3-02` — admission and refusal

Planning stores dimensions and conservative bounds but no candidates, target
arrays, or defect blocks. Candidate budget 8 admits the three-generator structured
route and rejects the nine-generator raw route. Budget 2 rejects both and reports
zero materialized routes. A certified permutation signature with no compositional
quotient returns `MissingQuotientConstructor` rather than running the generic orbit
algorithm silently.

### `E-G3-03` — execution policy and coincidence

The ordinary small-budget fixture reports
`selected-route-only-after-symbolic-admission` and materializes only the structured
route. Explicit audit fixtures report
`selected-plus-explicit-raw-span-audit`, materialize both routes, and recover exact
raw/structured stabilizer-span equality for the isotropic, axial, and
non-orthonormal controls. The quotient-orbit comparison is likewise explicit.

### `E-G3-04` — same observable and complete proxy

The selected compiler proxy remains 117; recursive quotient planning adds 21, so
the complete selected one-time proxy is 138. Against 27 versus 11 per-query work,
the complete-route break-even is 9 queries. The stabilization-only value 8 remains
reported under that narrower label. Projectors, channels, and the observable are
unchanged, including absolute error `4.996003610813204e-16`.

Disposition: **supported bounded** for recursive symmetric powers of one covariant
slot and lazy route execution. The result removes G2's exhaustive orbit scan from
the operational path; it does not generalize to arbitrary Young functors, traces,
mixed variance, spinors, jets, nonlinear symmetry, or analytic integration. A
further elasticity example would exercise the same constructor without testing a
new bridge. The next active probe therefore moves to coupled vector/spinor
carriers and Clifford covariance.

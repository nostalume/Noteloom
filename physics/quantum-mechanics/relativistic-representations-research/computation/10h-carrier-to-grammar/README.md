# N10h computation — carrier-to-grammar packet adapter

Run from the repository root:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/10h-carrier-to-grammar/check-carrier-grammar.mjs
```

The constructor distinguishes two inputs that the earlier research sometimes
blurred:

```text
physical fiber or Lorentz label
  != off-shell carrier presentation with invariant operations.
```

A label-only request is refused. For the bounded symmetric-power presentation, the
node derives the natural operations and rewriting identities from:

- symmetric multiplication and derivation;
- a nondegenerate invariant metric;
- for spinor tensors, an equivariant Clifford action polarizing that metric.

The executable then dispatches one of two handwritten packets, justified by that
derivation, and passes it directly into N10c and N10g. The check requires
them to regenerate the bosonic equation and constraints, the Clifford equation and
constraints, and the Clifford source/Euler multiplier while preserving grammar
provenance. Missing metric and missing Clifford-action inputs return separate
failure records.

This is an exact symbolic adapter and downstream regression. No component tensor
or gamma matrix is used. It does not compute operations or relations from an
arbitrary carrier expression: `symmetric-power` plus `scalar` or `dirac` selects a
stored packet. The construction-origin boundary and next compiler obligation are
recorded in [the audit](../../results/07-construction-origin-audit.md).

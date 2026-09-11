# N2 adaptive-admission training sheet

This sheet teaches a decision boundary, not a rule to use sparse elimination on
every network.

## Three decisions

```text
direct_gate
  The declared and minimum-fill computations do the same elimination work.
  Sparse inspection adds positive setup work and cannot pay inside the model.

conditional_candidate
  Minimum fill removes symbolic updates but adds pivot-selection work.
  Sparse can pay only when its returned positive-weight inequality is satisfied.

refuse
  The reciprocal scalar planner's assumptions or provable scalar pivots fail.
  Do not force the strip; use another valid representation or method.
```

## Decision procedure

```text
1. Check reciprocity: K must be exactly symmetric for this strip.
2. Check that a remaining hidden diagonal pivot is provably nonzero.
3. Compare declared and minimum-fill local update ledgers.
4. Same updates + extra inspection       -> direct_gate.
5. Fewer updates + extra inspection      -> conditional_candidate.
6. Failed reciprocity or scalar pivot     -> refuse.
```

The candidate decision does not mean “sparse is faster.” It means the answer
depends on the relative human costs of selection and symbolic update. Those costs
are not supplied during recognition.

## Worked training examples

- One hidden junction between two terminals: both orders are the same, so choose
  `direct_gate`.
- A reciprocal central junction with two grounded leaf branches: eliminating the
  leaves before the center reduces fill, so choose `conditional_candidate`.
- A directed response matrix with `K != K^T`: choose `refuse` for this reciprocal
  scalar strip even if another solver could handle the system.

Study the sheet until the administrator ends training. It is removed before every
scored phase.

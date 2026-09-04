# N10o computation — projected-carrier choice and residual repair

Run from the repository root:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/10o-projected-carrier-choice/check-carrier-choice.mjs
```

This bench corrects an overreach in N10n: `H_r=ker T` is an optional irreducible
one-row presentation, not a carrier forced by the particle representation.

The constructor receives N10n's rank-indexed relation and a requested capability.
At field rank three, the generated residual is

```text
-(3/5) R_2 R_1 A epsilon in H_3.
```

Its primitive defect is `A epsilon in H_1`. The returned portfolio is therefore:

- constrain `A epsilon=0` and add no carrier;
- introduce `chi in H_1`, generate `delta chi=A epsilon`, and add
  `(3/5)R_2R_1chi` to the equation;
- reconsider the trace-free presentation and return to the full symmetric
  compiler;
- refuse to infer the mixed channel, because it does not occur in this residual.

An exact rational harmonic-polynomial calculation independently verifies that
`A:H_r -> H_(r-1)` is surjective at the nonzero Euclidean `O(3)` representative
for ranks one through three. At rank two, restricting the parameter removes three
directions; the compensator instead adds the same three-component `H_1` carrier.

The selection is capability-relative. `minimal-local-carrier` chooses the
constraint. `unconstrained-harmonic-parameter` chooses the compensator.
`unconstrained-no-extra-carrier` returns a typed obstruction.

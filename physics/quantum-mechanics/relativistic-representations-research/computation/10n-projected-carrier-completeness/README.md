# N10n computation — projected-carrier operation completeness

Run from the repository root:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/10n-projected-carrier-completeness/check-projected-carrier.mjs
```

The packet separates construction from verification.

The constructor receives `H_r=ker(T)`, the invariant metric algebra, dimension,
and a rank budget. It rejects a supplied projector or operation table. Failure of
raw momentum insertion to preserve `ker(T)` generates

```text
R_r=P-[1/(2r+d-2)]UA,
A R_r=Q+[(2r+d-4)/(2r+d-2)]R_(r-1)A.
```

The coefficients are checked symbolically for the requested ranks. A separate
exact rational verifier realizes harmonic polynomials in three variables, constructs
the `so(3)` generator matrices and one reflection, and solves the full intertwiner
equations. For ranks one through three it finds one map to `H_(r+1)`, one to
`H_(r-1)`, and no map to the same untwisted `O(3)` carrier. The unrepresented
dimensions `3,5,7` are retained as the mixed/determinant-twisted channel rather
than counted as generated same-family operations.

A consumer uses the rank-indexed relation at field rank three. Starting with the
wave seed, it constructs

```text
R=R_2,
C=A,
D=Q-R_2A,
D R_2=-(3/5)R_2R_1A.
```

The residual generates the parameter constraint `A epsilon=0`; under that
constraint `DR=0`, while `D+RC=Q` holds without it. This is a downstream-use
certificate, not a claim that the constrained complex is a complete physical
higher-spin theory.

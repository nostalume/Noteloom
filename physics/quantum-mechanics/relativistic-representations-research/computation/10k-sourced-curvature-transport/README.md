# N10k computation — sourced curvature transport

Run from the repository root:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/10k-sourced-curvature-transport/check-sourced-curvature-transport.mjs
```

The constructor consumes the generated potential `FieldSystem`, N10e's source
adapter, N10j's curvature operation for the same spin, and N4f's scalar causal
Green resources. It retains two operations on the same compact physical current:

```text
J -> M^(-1)J -> G_F^+/- M^(-1)J -> K_s G_F^+/- M^(-1)J,
J -> M^(-1)J -> K_s M^(-1)J -> G_C^+/- K_s M^(-1)J.
```

A small typed rewrite calculus computes their equality from constant-coefficient
commutation. It also reduces an equation-source shift through
`K_sD_s=QK_s` and `Delta_C Q=0`, proving that the causal curvature output descends
to the physical source quotient.

For spins one through six the check compares potential and curvature scalar-Green
channel loads and exposes the direct first-order source obstruction. The chiral
equation carrier has larger pointwise dimension than its field carrier, so it
cannot have a right Green inverse on arbitrary equation sources. The artifact does
not convert the transported scalar-wave response into an independent direct
curvature source theory; it returns that missing compatibility complex as a typed
refusal.

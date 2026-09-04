# N10l computation — compatible direct-curvature sources

Run from the repository root:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/10l-compatible-curvature-source/check-compatible-source.mjs
```

The packet consumes N10j's curvature packet and N10k's sourced transport. The node
internally constructs the short direct chiral complex

```text
curvature --Z--> first-order source --Y--> compatibility defect
```

together with the normalized back operation `B`; the executable records their
descriptions rather than emitting general map objects. In a symmetry-adapted homogeneous
spinor-polynomial model, the check verifies `YZ=0`, `BZ=Q`, and `ZB=Q` on
compatible sources for spins one through six. An incompatible source is retained as
a nonzero `Y` witness rather than silently projected.

The node also derives the minimal order-`s-1` lift `L` of an adapted potential
source. Its syzygies imply `YL S=0` and `BL S=K S` when `CS=0`, so

```text
B G_Q L S=G_Q K S.
```

The executable normalizer consumes these two analytically derived syzygies; it
does not claim to rederive them by a hidden tensor-component expansion. Their
construction and theorem boundary are recorded in N10l, Section 4. The executable
part independently checks the direct complex/back identities and the resulting
route, refusal, and cost bookkeeping. It is therefore a verification/use backend,
not yet a general compatible-source generator; see the
[construction-origin audit](../../results/07-construction-origin-audit.md).

This equips the direct first-order equation with retarded/advanced solutions on its
compatible source space, but rejects computational compression: it propagates
`8s` source channels instead of the `4s+2` curvature channels of N10k. Moving `B`
before the scalar Green operation reduces it exactly to N10k's route.

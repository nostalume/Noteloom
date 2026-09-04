# N10r computation — direct constrained Green generator

Run from the repository root:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/10r-direct-constrained-green/check-direct-constrained-green.mjs
```

The packet does not use N10q's divergence section. From the generated projected
operations `R,A,Q` it constructs the invariant layers

```text
X_(s,l)=R_(s-1)...R_l ker A,
```

closes the divergence recurrence, computes the spectrum of
`D_s=Q-R_(s-1)A`, removes its single gauge layer, and interpolates the quotient
inverse

```text
G_D=Q^(-1) f_s(RA/Q).
```

Exact rational checks cover spins two through five. The packet records both the
maximum scalar-Green depth and a declared component-Green load. It does not claim
universal runtime dominance: conditioning, sparsity, parallel execution, and
prepared sources may change implementation cost.

The causal promotion uses a theorem contract for retarded/advanced powers of the
flat scalar wave operator. The executable verifies the invariant rational symbol;
it does not construct distribution kernels or wavefront estimates.


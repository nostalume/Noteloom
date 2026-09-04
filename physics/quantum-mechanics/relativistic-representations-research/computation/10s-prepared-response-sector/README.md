# N10s computation — prepared response-sector discriminator

Run from the repository root:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/10s-prepared-response-sector/check-prepared-response-sector.mjs
```

The packet accepts local spin-two preparation maps, not expected layer labels. It
takes the harmonic head, calculates its normalized divergence
`B=R_1 A/Q`, and either discovers `B j=0` directly or constructs the finite
spectral projectors generated in N10r.

Two cases share the same interface:

- the N10e compact bivector current is the regression; its harmonic head
  generically excites physical layers zero and two;
- a compact Weyl-typed seed is sent through double divergence; antisymmetry and
  trace freedom internally produce a conserved, trace-free current, and the
  selector discovers only layer two without receiving that label.

The Weyl transfer retains a nonzero null-screen contrast and both direct and
compensated routes return the same one-Green response. This is a successful
preparation-to-sector construction but not a computational speedup: on that same
prepared source the compensated adapter is already the identity, so both routes
act on the same observable-visible sector. The packet records this negative
whole-route verdict rather than inferring gain from declared carrier dimensions.

The executable is an exact-small symbolic/numerical regression at fixed non-null
and null momentum representatives. Distributional compact-support completion is
inherited from multiplying the displayed polynomial symbols by a compact scalar
profile; it does not implement a spacetime Green kernel.

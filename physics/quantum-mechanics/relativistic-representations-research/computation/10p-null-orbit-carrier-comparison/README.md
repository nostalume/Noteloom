# N10p computation — null-orbit carrier comparison

Run from the repository root:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/10p-null-orbit-carrier-comparison/check-null-carrier-comparison.mjs
```

The comparator constructs three symbol complexes at the common four-dimensional
null momentum `p=(1,0,0,1)`:

1. the harmonic field `H_s` with parameter restricted by `A epsilon=0`;
2. the harmonic pair `H_s direct-sum H_(s-2)` with N10o's compensator;
3. the compressed symmetric baseline `ker T^2` with `epsilon in ker T`.

It computes kernel, gauge-image, quotient, and transverse-screen ranks for spins
two through five. Every branch has quotient dimension two and screen rank two.

The packet also constructs the zero-order Fischer assembly

```text
Phi=phi+[1/(2s)]U chi,
chi=(1/2)T Phi.
```

It verifies that this map identifies the compensated carrier with `ker T^2`, sends
its gauge map to `delta Phi=P epsilon`, and gives the same equation kernel and
screen recovery as the compressed symmetric baseline.

The constrained branch removes `(s-1)^2` field components and exactly the same
number of null-orbit gauge directions. It is therefore a partial gauge
presentation, not a new physical quotient compression.

The matrix backend uses the existing finite polynomial-symbol evaluator and
floating row reduction with tolerance `1e-9`. The invariant Fischer identities
own the all-spin carrier/gauge interpretation; the finite ranks are regression
evidence, not an exact arbitrary-rank theorem engine.

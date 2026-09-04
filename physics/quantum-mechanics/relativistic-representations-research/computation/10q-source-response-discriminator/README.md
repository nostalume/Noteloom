# N10q computation — source-response discriminator

Run from the repository root:

```powershell
node physics/quantum-mechanics/relativistic-representations-research/computation/10q-source-response-discriminator/check-source-response-discriminator.mjs
```

The packet constructs, rather than assumes, the source-side consequence of the
restricted harmonic gauge parameter. At the exact nonzero Euclidean representative
`p=e_0` in four dimensions it:

1. builds `H_s`, `H_(s-1)`, and `H_(s-2)` as harmonic-polynomial kernels;
2. generates the projected raise `R` from the N10n trace obstruction;
3. constructs `A:H_(s-1)->H_(s-2)` and an exact rational section `S` with
   `A S=1`;
4. derives the constrained and compensated source annihilators;
5. generates the lift `L_S(j)=(j,-S^dagger R^dagger j)`;
6. verifies that restriction after lifting is the identity and that the lifted
   sources span the full compensated annihilator; and
7. returns the locality obstruction: a polynomial symbol `S(p)` cannot satisfy
   `A(p)S(p)=1`, since the left side vanishes at `p=0`.

Spins two through five are checked with exact rational linear algebra. The program
does not construct a global causal distribution for `S`. It proves algebraic
source and gauge-invariant-response equivalence away from zero momentum, then
records the failure of **gauge-slice transport** to provide a local causal
constructor. This does not exclude a separately generated constrained Euler/Green
operation.

The component matrices are verification data only. The promoted construction is
the invariant chain

```text
divergence section S
  -> field slice sigma(phi,chi)=phi-RSchi
  -> dual source lift L_S
  -> quotient-response transport
  -> polynomial-locality refusal.
```

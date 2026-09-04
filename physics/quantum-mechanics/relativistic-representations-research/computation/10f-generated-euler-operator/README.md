# Computation Contract — Generated Bosonic Euler Operator

Parent node: [N10f generated Euler operator](../../nodes/10f-generated-euler-operator.md)

## Semantic question

Does the obstruction to formal self-adjointness independently generate an
equation-equivalent Euler operator, and does its multiplier coincide with N10e's
source adapter without using that adapter as construction input?

N10c supplies

```text
D=Q-PA+cP^2T,  c=1/2.
```

The Lorentz-metric Fischer pairing supplies the primitive adjoints. The expected
trace-reversal coefficient is not an input.

## Residual construction

The normalized seed is `E_0=D`. Its formal-adjoint defect is generated from `D`:

```text
D-D^dagger=c(P^2T-UA^2).
```

An identity-only budget therefore refuses the action capability. With one admitted
zero-order correction `mUT`, the same operator algebra computes

```text
UTD-D^dagger UT
 =2(P^2T-UA^2)+c(UP^2T^2-U^2A^2T).
```

The second pair already factors through the double-trace constraint. Exact rational
elimination of the remaining physical channels returns `m=-1/4`. The constructor
exports the composite Euler operation

```text
E=MD,
M=I-(1/4)UT,
```

and the residual certificate

```text
MD-(MD)^dagger
 =(1/8)(U^2A^2T-UP^2T^2).
```

Only after this independent generation does it compare `M` with N10e's returned
source adapter.

## Run

```text
node check-generated-euler-operator.mjs
```

For spins `2` through `6`, finite natural-map matrices verify:

- exact residual factorization before carrier restriction;
- formal self-adjointness in the Fischer pairing on `ker T^2`;
- the gauge identity `ER=0` on traceless parameters;
- equation equivalence `M^(-1)E=D`;
- independent coincidence with N10e's source multiplier.

The same spin-two current used by N10e is then adapted and passed through the
off-shell scalar response. The returned Euler operation recovers the physical
current through `E phi=J`, rather than stopping at the Green source `D phi=S`.

## Boundary

This is a free quadratic bosonic action constructor inside the same four-dimensional
double-trace grammar. It assumes the Lorentz-metric Fischer pairing and a compact-
support or boundary contract. It does not fix overall normalization, positivity,
boundary charges, quantization, interactions, arbitrary carriers, or the fermionic
Grassmann/reality structure. It adds no single-observable speedup over N4c/N4f.

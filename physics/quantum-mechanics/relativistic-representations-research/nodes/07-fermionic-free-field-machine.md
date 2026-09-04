# Fermionic free-field machine

Status: supported for declared first-order Clifford families

## Obstruction

The bosonic wave symbol does not encode a first-order fermionic propagation law or
antisymmetric quantum algebra. Introducing explicit gamma matrices would choose a
basis before constructing why Clifford multiplication is needed.

## First-order construction

Request an equivariant first-order symbol `S(p)` whose square recovers the scalar
mass shell:

```text
S(p)^2 = Q(p) I.
```

Polarizing this equation constructs the Clifford relation

```text
S(p)S(q)+S(q)S(p)=2 eta(p,q) I.
```

Thus Clifford action is forced by factorization; matrices are optional finite
witnesses. Tensoring this action with symmetric carrier operations yields the
declared spinor-tensor families. Gamma/trace constraints arise when the residual
fails to preserve the requested physical quotient.

## Causal and positive-frequency construction

If `S_- S_+ = Q I`, a scalar causal Green operator generates a first-order one:

```text
G_S = S_- G_Q,
S_+ G_S = S_+ S_- G_Q = Q G_Q = I
```

on admitted sources. The source pairing and quotient must separately satisfy the
fermionic adjoint constraint.

The positive shell produces a one-particle Hilbert space `H_1`. Antisymmetric Fock
completion constructs

```text
Psi(f)=a(Kf)+a^dagger(JKf),
{Psi(f),Psi(g)^*}=<Kf,Kg>I
```

with charge conjugation/real structure `J` supplied where required.

## Output and boundary

Output: abstract Clifford factorizer, fermionic causal quotient, positive shell,
and free CAR field. The construction covers the spin-1/2 regression and bounded
spinor-tensor transfer, including a spin-3/2 constraint witness.

It does not select a real structure, interacting fermionic source, detector CAR
measure, or remove higher-spin consistency obstructions.

- [Equivalence boundary](08-realization-equivalence-boundary.md) tests whether the
  causal quotient and positive shell preserve the physical realization.
- [Equivalence boundary](08-realization-equivalence-boundary.md) prevents CAR
  recovery from being confused with interacting equivalence.

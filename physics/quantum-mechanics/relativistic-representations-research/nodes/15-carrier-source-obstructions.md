# Carrier and source obstruction boundary

Status: supported negative/conditional comparison; no preferred universal carrier

## Question

Can a trace-free projected carrier or curvature-first source reduce the complete
response calculation, rather than merely reduce field components?

## Projected carrier construction

For rank `r` harmonic tensors, the failure of naive multiplication to preserve
trace freedom computes a trace component. Cancelling it generates the projected
raise operation

```text
R_r = P - U A/(2r+d-2).
```

The denominator is forced by applying `T` and solving `T R_r=0`. The operation is
therefore generative once trace-free presentation is requested; trace freedom
itself is not forced by the particle representation.

## Physical discriminator

At the same null momentum, constrained harmonic, compensated harmonic, and full
symmetric complexes have equal quotient dimension and transverse-screen rank for
the tested spins. The assembly

```text
Phi = phi + U chi/(2s)
```

identifies compensated and compressed physical content. The constrained branch
removes as many null gauge directions as field components; no new particle content
or automatic computation reduction follows.

## Source obstruction

Restricted gauge pairing requires

```text
R^dagger j in im A^dagger,
```

while compensation requires `R^dagger j+A^dagger k=0`. A section `S` with `AS=1`
constructs an equivalence of source slices, but its inverse momentum degree proves
that no polynomial-local section exists. Source equivalence is therefore nonlocal.

Direct constrained Green construction avoids that section but produces a rank-
dependent polynomial and deeper solve. On the declared load metric it is more
expensive than the compensated route. A preparation supported in one invariant
layer admits one Green solve, but trace freedom simultaneously makes the competing
adapter trivial; neither presentation dominates.

## Curvature-visible quotient

If curvature `K_s` satisfies `K_s R=0`, then every gauge-raised response layer is
annihilated. Both carrier routes reduce on the named observable to

```text
K_s G J = G_Q K_s J
```

under the commuting-symbol contract. This is a genuine observable compression but
is presentation-neutral.

## Output and boundary

Output: projected operation, source/locality refusal, direct-route cost certificate,
and curvature-visible normal form.

- [Observable compiler](16-observable-measure-compiler.md) retains the useful
  presentation-neutral quotient.

Carrier-global selection remains open:

```text
(physical fiber, capability, locality/resources)
  -> admissible carrier presentations.
```

The current selector can filter supplied candidates; it cannot generate them.

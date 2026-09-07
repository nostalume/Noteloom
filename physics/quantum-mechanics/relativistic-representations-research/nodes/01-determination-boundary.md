# Determination and representation boundary

Status: the kinematic datum and its representation spaces are constructed;
dynamics and a local carrier remain supplied choices

## Obstruction

“The representation” may mean a physical Hilbert space, equivariant functions on
the group, finite coefficients, or spacetime fields. Identifying them hides both
what symmetry determines and the maps that must preserve physical content.

## Construct the physical datum

Let `G=R^(1,3) semidirect L` and `U` be a strongly continuous unitary
representation. Translation composition gives self-adjoint generators:

```text
U(t e_mu)U(s e_mu)=U((t+s)e_mu),
U(t e_mu)=exp(i t P_mu).
```

Because the translations commute, their joint spectral measure `E` constructs

```text
U(a)=integral exp(i<a,p>) dE(p).
```

Lorentz covariance then transports the spectrum:

```text
U(A)U(a)U(A)^(-1)=U(Lambda(A)a)
=> U(A)E(Delta)U(A)^(-1)=E(Lambda(A)Delta).
```

An irreducible positive-energy sector therefore supplies one Lorentz orbit `O`
and one unitary representation `rho:K->U(F)` of the stabilizer of a standard
momentum `k`. This pair, rather than a field equation, is the physical datum.

## Construct the typed realizations

The induced physical space is

```text
H_phys=L^2(O,dmu;F),
(U(a,A)psi)(p)
 =exp(i<a,p>)rho(W(A,p))psi(Lambda(A)^(-1)p).
```

Equivariant group functions `f(g kappa)=rho(kappa)^(-1)f(g)` are optional
packaging. A finite Lorentz module `V` is instead a generally nonunitary
coefficient carrier. A covariant field is a `V`-valued distribution or section;
equations and gauge maps must still select its physical quotient.

Choose transports `B(p)k=p`. An orbitwise map `u(p):F->V` represents the same
state only when

```text
S(A)u(q)=u(p)rho(W(A,p)),
q=Lambda(A)^(-1)p.
```

Indeed, both routes act on the same `v in F` and land in `V`:

```text
S(A)u(q)v=u(p)rho(W(A,p))v.
```

This equality is the semantic certificate. It does not identify `V` with
`H_phys`, nor prove injectivity, locality, completeness, or quotient recovery.

## Retained output and boundary

Output:

```text
(orbit O, stabilizer fiber F, induced action, typed realization obligation).
```

The datum determines mass/sign sector, spin or helicity fiber, and the induced
Poincare action up to unitary equivalence. It constrains possible carriers and
equivariant operations, but does not choose a carrier, gauge redundancy,
differential order, action, interaction, state, detector, boundary condition, or
approximation.

[Spin, helicity, and realization](03-spin-helicity-carriers.md) constructs the
fiber, finite carrier, and actual bridge. Reducible sectors require their full
spectral decomposition; reality, parity, domains, and countable completion remain
open.

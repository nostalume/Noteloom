# Representation spaces and the maps between them

Status: supported type discipline

## Obstruction

“The representation” may mean a physical Hilbert space, functions on the group,
finite coefficients, or spacetime fields. Equating them hides the maps that carry
physical content and makes later quotient claims unverifiable.

## Four constructed spaces

From the determination datum of node 01, fix an orbit `O`, a
standard momentum `k`, its stabilizer `K`, and a unitary fiber representation
`rho:K -> U(F)`.

1. The physical induced space is

   ```text
   H_phys = L^2(O, dmu; F),
   U(a,A)psi evaluated at p
     = exp(i<a,p>) rho(W(A,p)) psi(Lambda(A)^(-1)p).
   ```

2. The group-function space consists of equivariant functions

   ```text
   f(gkappa) = rho(kappa)^(-1) f(g),
   ```

   and is optional packaging of the induced construction, not a field space.

3. A finite coefficient carrier is a finite-dimensional Lorentz module `V`. It is
   generally nonunitary and contains more vectors than the physical fiber.

4. A covariant field is a distribution or section with values in `V`, transformed
   by pullback and the carrier action. Equations and gauge maps select its physical
   quotient.

## The bridge is an intertwiner, not an identification

Choose transports `B(p)` with `B(p)k=p`. An orbitwise map
`u(p):F -> V` must satisfy

```text
S(A) u(q) = u(p) rho(W(A,p)),
q = Lambda(A)^(-1)p.
```

Then `Phi(p)=u(p)psi(p)` is covariant. Injectivity, quotient recovery, locality,
and completeness are separate obligations; no equality of the four spaces is
asserted.

## Semantic computation

Both sides act on the same `v in F` and land in `V`:

```text
S(A) Phi(q)
  = S(A)u(q)psi(q)
  = u(p)rho(W(A,p))psi(q)
  = Phi'(p).
```

Thus the same induced state is represented after the carrier transformation. The
calculation states exactly what is preserved and does not turn `V` into `H_phys`.

## Output and edges

Output: typed spaces plus the required intertwiner equation.

- [Spin, helicity, and carriers](03-spin-helicity-carriers.md) constructs `F` and
  candidate `V`.
- [Realization bridge](04-realization-bridge.md) constructs `u` or a quotient
  complex and tests recovery.

## Boundary

The node supplies no locality theorem and no finite carrier automatically. Density,
reality, parity, countable-spin completion, and domain questions remain explicit.

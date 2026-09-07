# Spin, helicity, carriers, and realization

Status: finite complex four-dimensional sectors have an explicit orbitwise or
cohomological realization; global analytic and countable-spin completion is open

## Obstruction

Transport to a standard momentum is nonunique. Its ambiguity creates the
stabilizer representation, while a finite Lorentz carrier generally contains more
vectors than that physical fiber. The bridge must therefore be constructed, not
assumed.

## Construct the fibers and candidate carriers

For `k_m=(m,0,0,0)`, two transports differ by `B'(p)=B(p)r` with `rk_m=k_m`.
The stabilizer is `SU(2)`, and its finite irreducible unitary fibers are

```text
F_s=Sym^(2s) C^2,  2s in Z_(>=0).
```

Their infinitesimal action is obtained by differentiating the product action:

```text
d rho_s(X)(v_1...v_(2s))
 =sum_j v_1...(Xv_j)...v_(2s).
```

For null `k_0`, the stabilizer is the double cover of `E(2)`. Finite-helicity
sectors make its translation part trivial and retain

```text
rho_h(theta)=exp(i h theta),  2h in Z.
```

Nontrivial translations give continuous spin and lie outside this worktable.

The complex Lorentz algebra has two commuting `sl(2)` actions, so its finite
irreducible carriers are

```text
V_(j_L,j_R)
 =Sym^(2j_L) C^2 tensor Sym^(2j_R) conjugate(C^2).
```

This catalogue does not select a presentation. Restriction to the stabilizer asks
whether `F_s` or `F_h` occurs; locality, multiplicity, real structure, and desired
operations determine whether that occurrence is useful.

## Construct the orbitwise bridge

Choose `B(p)k=p`, put `q=Lambda(A)^(-1)p`, and calculate the two routes to `p`:

```text
B(p)k=p,
A B(q)k=Aq=p.
```

Their relative map fixes `k`:

```text
W(A,p)=B(p)^(-1)AB(q),
W(A,p)k=k.
```

Search at `k` for `u_k:F->V` satisfying

```text
S(r)u_k=u_k rho(r),  r in K,
```

and transport it by `u(p)=S(B(p))u_k`. Then

```text
S(A)u(q)
 =S(AB(q))u_k
 =S(B(p))S(W(A,p))u_k
 =u(p)rho(W(A,p)).
```

The covariance law is thus the output of a computed composite.

## Quotient realization

When a gauge potential cannot contain the physical fiber injectively, construct

```text
G_p --R(p)--> V --D(p)--> E,
D(p)R(p)=0,
H_p=ker D(p)/im R(p).
```

Support requires an explicit bijective stabilizer intertwiner `H_k->F`; covariance
then transports it along the orbit. Massive spin one, massless helicity one, and
abstract-Clifford half-integer carriers are regression witnesses, not imported
motivation.

## Retained output and boundary

Output: physical fiber, candidate finite carriers, and an orbitwise intertwiner or
symbol-complex cohomology carrying the same stabilizer representation.

[The local free-field complex](05-local-symbol-complex.md) adds polynomial
locality, causal propagation, and CCR/CAR completion. The Lorentz split used here
is dimension-specific; mixed symmetry, real/parity structure, source density,
interactions, and countable completion remain open.

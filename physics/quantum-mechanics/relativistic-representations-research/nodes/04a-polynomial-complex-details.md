# N4a — Technical Details for Polynomial Symbol Complexes

Status: fixed-data polynomial-lift criterion and uniform bosonic integer-spin potential family supported on the nonzero null orbit  
Readable main construction: [N4 arbitrary finite spin/helicity](04-local-symbol-extension.md)  
Consumes: [N1](01-determination-boundary.md), [N2](02-three-representation-spaces.md), [N2a spin/helicity](02a-spin-and-helicity.md), [N3](03-realization-bridge.md), [massive spin one](03a-massive-spin-one.md), and [massless helicity one](03b-massless-helicity-one.md)

## Research contract

- **Question:** given an orbit `O`, a standard momentum `k`, and a little-group
  representation `sigma`, how can one construct a finite-order local covariant
  equation whose physical fiber is exactly `sigma`?
- **Presumptions:** a free linear field on Minkowski space, constant coefficients,
  finite-dimensional Lorentz carriers, finite differential order, and one chosen
  positive-energy orbit. Reality, parity, an action principle, and minimality are
  extra requirements unless stated.
- **Required output:** a bounded complex of Lorentz carriers `C^a`, polynomial
  symbols `delta^a(p):C^a->C^(a+1)`, and an exact criterion for when
  `delta^(a+1)(p)delta^a(p)=0`, with

  ```text
  H^0(k) = ker delta^0(k) / im delta^(-1)(k) ~= sigma
  ```

  as a little-group representation, together with a check that no unwanted
  characteristic orbit carries physical cohomology.
- **Failure boundary:** the criterion is finite and decisive only after carriers
  and degree bounds are chosen. Symmetry and `sigma` supply no universal bound on
  those choices and need not select a unique gauge presentation or action.

For a three-term presentation, `delta^(-1)=R` and `delta^0=D`. These symbols are
used so that `K_k` remains reserved for the little group at `k`.

## 1. Construct the standard-momentum complex first

The desired particle data are already concentrated at `k`: the stabilizer

```text
K_k = { r in L_spin | r k = k }
```

acts on the target fiber by `sigma`. A field equation can represent this datum
only if its standard-momentum amplitudes form a complex

```text
G --R_k--> F --D_k--> E,
D_k R_k = 0,
H(k) = ker D_k / im R_k ~= sigma.
```

Here `F` is the amplitude carrier, `im R_k` is the part declared gauge, and
`ker D_k` is the part satisfying the equation. This is not an imported
cohomological decoration: quotienting by `im R_k` is exactly the operation that
makes two amplitudes represent the same physical state.

Because `K_k` must act on the quotient, the two maps must respect its action:

```text
rho_F(r) R_k = R_k rho_G(r),
rho_E(r) D_k = D_k rho_F(r),       r in K_k.
```

The second identity preserves the kernel; the first preserves the gauge image.
Therefore the action `[f] -> [rho_F(r)f]` is defined on `H(k)`. The assertion
`H(k) ~= sigma` must compare this action, not merely dimensions.

Gauge symmetry can itself be reducible. The correct object is then a bounded
complex

```text
... -> C^(-2) --delta^(-2)--> C^(-1) --delta^(-1)--> C^0
    --delta^0--> C^1 -> ... .
```

`H^0` is the physical amplitude. Negative degrees encode gauge parameters and
gauge-for-gauge relations; positive degrees encode equations and their identities.
The three-term complex is the first irreducible case, not the universal shape.

## 2. Transport the complex around the orbit

Assume `G,F,E` carry Lorentz representations `rho_G,rho_F,rho_E` extending their
little-group actions. Choose `B(p)` with `B(p)k=p` and define on the orbit

```text
R_O(p) = rho_F(B(p)) R_k rho_G(B(p))^(-1),
D_O(p) = rho_E(B(p)) D_k rho_F(B(p))^(-1).
```

This definition is independent of the chosen lift. Indeed, another lift is
`B'(p)=B(p)r` for some `r in K_k`, and little-group equivariance gives

```text
rho_F(B') R_k rho_G(B')^(-1)
= rho_F(B) rho_F(r) R_k rho_G(r)^(-1) rho_G(B)^(-1)
= rho_F(B) R_k rho_G(B)^(-1),
```

with the same calculation for `D_O`. Thus the operation constructs an orbit-wide
complex rather than merely comparing two routes informally.

For `A in L_spin` and `q in O`, note that

```text
A B(q) = B(Aq) W(A,q),
W(A,q) = B(Aq)^(-1) A B(q) in K_k.
```

Substitution and little-group equivariance compute

```text
R_O(Aq) = rho_F(A) R_O(q) rho_G(A)^(-1),
D_O(Aq) = rho_E(A) D_O(q) rho_F(A)^(-1).
```

Consequently the transported cohomology at every `p in O` is the transported
copy of `sigma`. This settles covariance on the orbit. It does **not** yet produce
a local spacetime equation.

## 3. Construct every local candidate inside a finite intertwiner space

A constant-coefficient operator of order at most `d` becomes under Fourier
transformation a polynomial symbol of degree at most `d`. After the metric
identifies momentum covectors with `V_C`, construct the candidate space

```text
P_<=d(X,Y)
  = direct-sum_(r=0)^d Hom_L(Sym^r(V_C) tensor X,Y).
```

An element of this space is exactly a Lorentz-equivariant polynomial map
`a(p):X->Y` of degree at most `d`: evaluating its symmetric multilinear part on
`p tensor ... tensor p` produces the symbol, while polarization reconstructs the
multilinear map from the polynomial. Thus no component ansatz is needed.

Evaluation at the standard momentum constructs a linear map

```text
ev_k:P_<=d(X,Y)->Hom_(K_k)(X,Y),
ev_k(a)=a(k).
```

The codomain is correct because Lorentz covariance evaluated at `r k=k` computes

```text
a(k)rho_X(r)=a(rk)rho_X(r)=rho_Y(r)a(k).
```

This exposes the first locality obstruction. A desired little-group map `a_k`
has a degree-`d` polynomial lift only when

```text
[a_k]=0 in coker(ev_k).
```

Orbit transport alone produces a smooth or measurable equivariant map; it does
not force this cokernel class to vanish.

## 4. The fixed-carrier, fixed-order criterion

Fix finite Lorentz carriers `C^a` and degree bounds `d_a`. Construct

```text
Z_d(C)
 ={ delta=(delta^a) |
    delta^a in P_<=d_a(C^a,C^(a+1)),
    delta^(a+1)(p)delta^a(p)=0 for every p }.
```

Composition is itself a semantic computation. If `star` denotes multiplication
of polynomial coefficients followed by composition of carrier maps, then

```text
(delta^(a+1) star delta^a)(p)
  =delta^(a+1)(p)delta^a(p).
```

Hence `Z_d(C)` is the common zero set of finitely many quadratic equations inside
finite Lorentz-intertwiner spaces. It is not shorthand for an infinite search over
coordinate tensors.

Let `c_k=(C^a,d_k^a)` be a chosen `K_k`-equivariant standard-momentum complex with
`H^0(c_k)~=sigma`. Simultaneous evaluation gives

```text
Ev_k:Z_d(C)->{K_k-equivariant complexes on the restricted carriers}.
```

The exact criterion is

```text
c_k has a Lorentz-covariant local realization
with these carriers and degree bounds

iff

Ev_k^(-1)(c_k) is nonempty.
```

For the forward direction, a point of the fiber supplies polynomial symbols,
their complex identities, and the prescribed standard fiber; Fourier substitution
produces finite-order operators. Conversely, any such local constant-coefficient
complex has polynomial Fourier symbols, covariance puts each symbol in the stated
intertwiner space, the operator identities put their tuple in `Z_d(C)`, and
evaluation returns `c_k`. Both directions act on the same carriers, so this is an
inverse construction rather than an analogy.

Individual vanishing cokernel classes are necessary but not sufficient: chosen
lifts can still fail the simultaneous quadratic equations. This second obstruction
is the emptiness of `Ev_k^(-1)(c_k)` inside `Z_d(C)`—the polynomial syzygy
obstruction.

## 5. Characteristic cohomology is a rank computation

Let `A=Sym(V_C^*)` be the momentum polynomial ring. The symbols construct a
complex of free `A`-modules `A tensor C^a`. Evaluation at `p` gives the finite
fiber complex. Because `im delta^(a-1)(p)` lies in `ker delta^a(p)`, direct
dimension counting computes

```text
dim H^a(p)
 =dim C^a-rank delta^(a-1)(p)-rank delta^a(p).
```

If `n_a=dim C^a`, the characteristic set at degree `a` is therefore

```text
Char_a(delta)
 = union_(r=0)^(n_a-1)
   {p | rank delta^(a-1)(p)<=r,
        rank delta^a(p)<=n_a-r-1}.
```

Each rank condition is cut out by minors, so the characteristic set is an
invariant algebraic set computable from determinantal ideals. This avoids solving
the field equations component by component. Covariance makes rank and cohomology
constant along each Lorentz orbit, but different orbits or singular strata may
still occur.

A successful realization requires the desired positive-energy orbit in
`Char_0`, an explicit `K_k`-isomorphism `H^0(k)~=sigma`, and an account of every
other component. Evaluation at `k` alone cannot exclude another mass shell,
zero-momentum cohomology, or a higher-derivative branch.

## 6. The obstruction ledger

For fixed carriers and degree bounds, failure has four distinct meanings:

1. **fiber presentation:** no `K_k`-complex on the restricted carriers has
   `H^0~=sigma`;
2. **polynomial extension:** a required `d_k^a` is outside `im ev_k`;
3. **syzygy compatibility:** individual lifts exist, but no simultaneous lifts
   satisfy `delta^(a+1)delta^a=0`;
4. **characteristic contamination:** a lift exists but has unexplained physical
   cohomology on another orbit or singular stratum.

These tests are finite representation decomposition, finite invariant polynomial
algebra, and determinantal rank calculations. What remains unbounded is the prior
choice of carriers and degree limits. Therefore this node proves a decision
criterion for a proposed presentation, not a universal existence theorem selected
by `sigma` alone.

## 7. The vector equations test every obstruction

The detailed vector constructions are owned by
[N3a](03a-massive-spin-one.md) and [N3b](03b-massless-helicity-one.md). This node
consumes their checked outputs only to test whether the obstruction ledger
distinguishes the two cases:

| Presentation | Fiber input | Chosen local data | Obstruction result | Characteristic result |
| --- | --- | --- | --- | --- |
| massive vector | `V_1~=k^perp_C` at rest | vector carrier, quadratic parity-even symbol, no extra branch | the carrier contains an unwanted scalar; minimality and its removal select `D_m(p)=(m^2-p^2)I+p tensor p_flat` up to scale | physical cohomology occurs only on `p^2=m^2` |
| massless vector potential | `k^perp_C/span(k)~=C_(+1) direct-sum C_(-1)` | `R(p)lambda=p lambda`, quadratic parity-even `D`, polynomial identity `D R=0` | syzygy compatibility selects `D_0(p)=p^2I-p tensor p_flat` up to scale | non-null cohomology vanishes; the null screen survives; `p=0` carries the exceptional full carrier |

Thus both examples pass fiber presentation, polynomial extension, syzygy, and
characteristic tests, but only after extra carrier, degree, parity, and minimality
choices are named. Spin or helicity alone does not select either presentation. A
single massless helicity instead uses N4's chiral curvature carrier.

## 8. A uniform integer-spin gauge identity

The criterion can construct more than isolated named equations. Let a rank-`s`
symmetric Lorentz tensor be represented by a homogeneous polynomial `phi(u)` in
one auxiliary vector `u`. The auxiliary variable packages the symmetric tensor;
it is not an additional spacetime coordinate. Metric contraction constructs

```text
P_p phi(u)=(p.u)phi(u),
A_p phi(u)=d/dt phi(u+t p)|_(t=0),
T phi(u)=metric trace of phi.
```

Evaluating both compositions on the same polynomial gives the invariant operator
relations

```text
[A_p,P_p]=p^2,
[T,P_p]=2A_p,
[T,A_p]=0.
```

For integer `s>=1`, construct the carriers

```text
G_s=ker T in Sym^(s-1)(V_C^*),
F_s=ker T^2 in Sym^s(V_C^*),
```

and the degree-one gauge symbol and degree-two equation symbol

```text
R_s(p)=P_p:G_s->F_s,
D_s(p)=p^2-P_p A_p+(1/2)P_p^2 T:F_s->F_s.
```

The types are part of the construction. The commutators compute

```text
T^2 P_p=P_p T^2+4A_p T,

T^2 D_s(p)
 =(3p^2+3P_p A_p+(1/2)P_p^2T)T^2,
```

so `R_s` sends traceless parameters into double-traceless fields and `D_s`
preserves the field carrier. The decisive composite reduces without expanding a
single tensor component:

```text
D_s(p)P_p
 =p^2P_p-P_p(A_pP_p)+(1/2)P_p^2(TP_p)
 =(1/2)P_p^3T.
```

It vanishes on `G_s`. Therefore

```text
G_s --R_s(p)--> F_s --D_s(p)--> F_s
```

is a Lorentz-equivariant polynomial complex for every finite integer spin. At
`s=1`, the trace restrictions are empty and the formula is exactly the Maxwell
complex above. At `s=2`, it constructs the symmetric metric-potential symbol and
its vector gauge map. No separate index expansion is required as `s` grows.

### 8.1 Null momentum exposes the constraint actually being solved

Construct the first-order contraction

```text
C_p=A_p-(1/2)P_p T:F_s->G_s.
```

Its codomain is not asserted. Acting with `T` and using the commutators computes

```text
T C_p
 =T A_p-(1/2)T P_p T
 =-(1/2)P_p T^2,
```

so `T C_p phi=0` for every `phi in F_s`. The equation symbol is now

```text
D_s(p)=p^2-P_p C_p.
```

At a nonzero null momentum `k`, multiplication by the nonzero linear polynomial
`P_k(u)=k.u` is injective. Therefore

```text
D_s(k)phi=0
iff
P_k C_k phi=0
iff
C_k phi=0.
```

The physical kernel is thus a first-order invariant constraint; no tensor
components need be eliminated.

### 8.2 Restriction constructs the screen amplitude

The equation itself constructs the map to the screen. Restrict `phi` to the
hyperplane `k^perp`, which is exactly `P_k(u)=0`. On that hyperplane `C_k phi=0`
computes

```text
A_k phi|_(k^perp)=0.
```

`A_k` differentiates along `u |-> u+t k`, the radical direction of `k^perp`.
Hence the restricted polynomial is constant on the fibers of
`k^perp->Q_k` and descends uniquely to a homogeneous polynomial

```text
res_k(phi) in Sym^s(Q_k tensor C)^*.
```

The descended polynomial is trace-free. To verify this without making a screen
choice part of the result, choose one null witness `n` with `k.n=1` and let
`B_n` differentiate along `n`. Applying `B_n` to the same equation and then
restricting to `P_k=0` gives

```text
0=B_n(C_k phi)|_(k^perp)
  =A_k B_n phi-(1/2)T phi.
```

Under the splitting witnessed by `n`, the Lorentz trace decomposes as

```text
T=2A_k B_n+T_Q.
```

Substitution computes `T_Q res_k(phi)=0`. The resulting trace-free screen
polynomial is independent of `n`; `n` only verifies the intrinsic quotient trace.

### 8.3 The kernel of screen restriction is exactly gauge

First compute that a gauge amplitude belongs to the equation kernel. At `k^2=0`,

```text
C_k P_k
 =A_k P_k-(1/2)P_k T P_k
 =-(1/2)P_k^2T.
```

Thus `C_k(P_k epsilon)=0` for `epsilon in G_s`, and the previous trace identity
also gives `P_k epsilon in F_s`. Multiplication by `P_k` is injective, so the
left arrow below is injective.

Conversely, suppose `C_k phi=0` and `res_k(phi)=0`. The second condition says that
the polynomial `phi` vanishes on the hyperplane `P_k=0`; polynomial division by
this linear factor constructs a unique `psi` with

```text
phi=P_k psi.
```

Applying the displayed composite to the same `psi` yields

```text
0=C_k phi=-(1/2)P_k^2T psi.
```

The polynomial ring has no zero divisors and `P_k!=0`, hence `T psi=0`.
Therefore `psi in G_s` and `phi=R_s(k)psi` is gauge.

Surjectivity is also constructive. Given a trace-free screen polynomial `f`, choose
one witness `n`, identify the screen with `{k,n}^perp`, and extend `f` to be
constant along the `k` and `n` directions. Its extension `phi_f` satisfies

```text
A_k phi_f=0,
T phi_f=T_Q f=0,
```

so `phi_f in ker C_k` and `res_k(phi_f)=f`. A different witness changes the lift
by an element already proved to be gauge. We have therefore constructed the exact
sequence

```text
0 -> G_s --R_s(k)--> ker D_s(k)
  --res_k--> Sym_0^s(Q_k tensor C)^* -> 0.
```

All maps are `K_k`-equivariant: the stabilizer preserves `k^perp`, its radical,
the quotient metric, polynomial restriction, and trace. Consequently

```text
H^0_s(k)=ker D_s(k)/im R_s(k)
        ~=Sym_0^s(Q_k tensor C)^*
```

as a little-group representation, not merely as a vector space.

### 8.4 The screen representation computes the two helicities

For `s>=1`, the metric and orientation of `Q_k` construct the quarter-turn
`J:Q_k->Q_k`, with `J^2=-1`. Complexification gives its two eigenlines

```text
Q_k tensor C=L_+ direct-sum L_-,
J|_(L_+)=+i,
J|_(L_-)=-i.
```

A screen rotation through `theta` acts on these lines by `exp(+i theta)` and
`exp(-i theta)`. Symmetric power decomposes by the number of factors from each
line. The trace pairs one `L_+` factor with one `L_-` factor: on a mixed summand
`L_+^r L_-^(s-r)` it is nonzero for `0<r<s`, while it kills the two endpoint
lines. Therefore

```text
Sym_0^s(Q_k tensor C)^*
 ~= (L_+^*)^s direct-sum (L_-^*)^s
 ~= C_(+s) direct-sum C_(-s),
```

up to the already declared helicity-sign convention. N2a proves that null
translations act identically on `Q_k`, hence trivially on this functor of `Q_k`.
The exact sequence therefore recovers precisely the parity-paired finite-helicity
fiber `+s direct-sum -s`. A single helicity still requires the chiral curvature
realization from N4 or an additional chiral projection.

### 8.5 Every momentum stratum is now accounted for

Let `p^2!=0` and suppose `D_s(p)phi=0`. The identity
`T C_p=-(1/2)P_pT^2` makes `C_p phi` traceless. The equation itself computes

```text
phi=P_p[(1/p^2)C_p phi].
```

The bracketed polynomial is therefore a valid gauge parameter, so every solution
is gauge. Conversely `D_s(p)R_s(p)=0`, already proved above. Hence

```text
p^2!=0  => H^0_s(p)=0.
```

At nonzero null `p`, the exact sequence gives
`H^0_s(p)~=C_(+s) direct-sum C_(-s)`. At `p=0`, both `R_s(0)` and `D_s(0)` vanish,
so `H^0_s(0)=F_s`. Thus

```text
Char_0(R_s,D_s)={p | p^2=0},
```

On real momentum space this consists of the future-null and past-null orbits plus
an exceptional origin carrying the whole off-shell carrier. The positive-energy
representation selects the future orbit; polynomial locality does not remove its
negative-frequency partner. The particle construction excludes the origin by
`p!=0`, and no other mass shell or higher-derivative branch occurs.

For `s=0`, the separate scalar symbol `D_0(p)=p^2` gives the helicity-zero line on
the same nonzero null orbit. The construction above therefore supplies a local
parity-paired potential equation for every finite bosonic integer helicity.

## 9. Polynomial symbols become spacetime field equations

Fix the Fourier construction

```text
Phi(x) = integral exp(-i p.x) Phi_tilde(p) dp.
```

Acting on the same integrand computes

```text
i partial_mu exp(-i p.x) = p_mu exp(-i p.x).
```

Hence a polynomial identity `D(p)Phi_tilde(p)=0` becomes the local differential
equation

```text
D(i partial)Phi(x)=0,
```

and `Phi_tilde -> Phi_tilde+R(p)epsilon_tilde` becomes
`Phi -> Phi+R(i partial)epsilon`. The semantic invariant is the same plane-wave
amplitude; Fourier transformation changes its representation, not its physical
fiber.

For the two vector symbols this yields, up to an overall Fourier-sign normalization,

```text
partial_mu F^(mu nu)+m^2 A^nu=0             (massive spin 1),
partial_mu F^(mu nu)=0,  A->A+partial alpha (massless helicity +/-1).
```

The first equation has mass-shell kernel `V_1`; the second has null-shell
cohomology `C_(+1) direct-sum C_(-1)`. This is the exact relation between the
spin/helicity construction and the spacetime field equation.

The same substitution promotes the uniform integer-spin complex without an index
expansion:

```text
T^2 Phi=0,
T epsilon=0,
D_s(i partial)Phi=0,
Phi -> Phi+P_(i partial)epsilon.
```

Here `P_(i partial)` is the symmetric gradient, `A_(i partial)` is divergence,
and `T` is trace. The exact screen sequence proves that the gauge-inequivalent
positive-energy plane waves of this local quadratic system carry helicities
`+s direct-sum -s`.

## 10. Construction and evaluation route

For a specified orbit and `sigma`:

1. choose finite Lorentz carriers `C^a` and explicit degree bounds `d_a`;
2. construct a `K_k`-equivariant standard complex with `H^0~=sigma`;
3. compute the evaluation maps from `P_<=d_a(C^a,C^(a+1))`;
4. test polynomial-extension cokernels and the simultaneous syzygy equations;
5. compute the little-group action on `H^0(k)`, not only its dimension;
6. obtain every characteristic stratum from the rank conditions;
7. only then construct the global solution-space intertwiner and physical norm.

The evaluation favors fewer semantic transformations: carrier decompositions or
component expansions are admitted only when they return an intertwiner, a rank
jump, a quotient action, or a counterexample.

## 11. Nonuniqueness and selection criteria

The target cohomology does not determine a unique complex. One may multiply an
equation by an invariant polynomial, add contractible auxiliary pairs, make local
field redefinitions, choose a larger carrier, or introduce higher derivatives
without changing the desired fiber at `k`. Some of these operations add other
characteristic components or obscure observables.

Any uniqueness or economy claim therefore requires named extra criteria, such as:

- minimal polynomial degree;
- no unexplained characteristic component;
- minimal carrier and auxiliary content;
- a reality/parity condition;
- existence of a variational or formally self-adjoint presentation, audited but not
  yet completed in [N4c](04c-action-completion-audit.md);
- preservation of locality under the comparison map.

## Computation decision

The proof above closes by restriction, descent, and polynomial divisibility, so no
large recurrence enters the conceptual node. A separate bounded
[rank check](../computation/04-local-symbol-extension/README.md) constructs the
operators on homogeneous polynomials and verifies spins `1` through `6` at null,
non-null, and zero momentum. It is independent evidence, not the reason the
all-spin exact sequence is accepted.

## Source bindings and open edge

- Bekaert--Boulanger supply the induced-representation and covariant-equation
  comparison used to bound the construction.
- [The polynomial-gauge source packet](../sources/polynomial-gauge-contracts.md)
  binds the Alkalaev--Grigoriev--Tipunin construction: Sections 2--4 respectively
  supply the parent/BRST construction, its Labastida reduction, and the independent
  Wigner-module check. That broader construction is comparison material, not a
  proof that every chosen standard complex lies in `im Ev_k`.

The readable N4 node supplies a gauge-free chiral carrier and local symbol for every
finite spin/helicity. N4a now additionally supplies a parity-paired potential
realization for every finite bosonic integer helicity, with its little-group
cohomology and characteristic strata constructed. The separate
[N4b half-integer node](04b-half-integer-potential.md) now supplies the analogous
symmetric spinor-tensor family. Mixed-symmetry carriers, actions, interactions,
and uniqueness remain separate research branches.

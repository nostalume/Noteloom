# N2a — Constructing Spin and Helicity as Physical Fibers

Status: supported within the massive finite-spin and massless finite-helicity sectors  
Consumes: the momentum orbit, standard momentum, and residual-frame group constructed in [N2](02-three-representation-spaces.md)  
Produces: the exact little-group representation that a covariant field equation must recover
Source contracts: [little-group and spin-cover contracts](../sources/lorentz-carrier-contracts.md)

## Research contract

- **Question:** after momentum has been fixed, what internal datum distinguishes
  particles, and how do the labels `s` and `h` arise from that datum?
- **Presumptions:** a positive-energy irreducible unitary representation of the
  spin-covered Poincare group; either `p^2=m^2>0`, or `p^2=0`, `p!=0`, with a
  finite-dimensional physical polarization fiber.
- **Output:** for the massive orbit, the spin-`s` irreducible representation of
  `SU(2)`; for the null orbit, a helicity character on which null translations act
  trivially.
- **Downstream obligation:** a field equation represents the particle only when
  its plane-wave kernel modulo gauge is isomorphic to this constructed fiber.

Spin and helicity are therefore not names attached to an equation afterward. They
are the input representation that the equation must preserve.

## 1. Why an internal representation remains after momentum is fixed

`N2` constructs a standard momentum `k` on an orbit and a transport `B(p)` with
`B(p)k=p`. If `B_1(p)` and `B_2(p)` reach the same `p`, then

```text
r = B_1(p)^(-1) B_2(p)
```

satisfies `rk=k`. Thus changing the standard frame without changing momentum is
the stabilizer

```text
K_k = { r | rk=k }.
```

An amplitude at `k` must transform under this unavoidable ambiguity. Probability
preservation makes the action unitary, and irreducibility of a single particle
species makes it an irreducible representation `sigma` of `K_k`. The entire
spin/helicity question has therefore been reduced from the noncompact Poincare
group to a representation on one physical momentum fiber.

## 2. Massive momentum constructs rotations

Choose `k=(m,0,0,0)`, `m>0`. If `r k=k`, Lorentz-metric preservation gives, for
every `x in k^perp`,

```text
k.(r x) = (r^(-1)k).x = k.x = 0.
```

Thus `r` preserves the Euclidean space `(k^perp,-eta)`. Conversely, every proper
rotation of `k^perp` extends to a Lorentz transformation by fixing `k`. Hence the
connected stabilizer is `SO(3)`, and in the chosen spin cover it is `SU(2)`.

This construction explains why massive internal states rotate: they are precisely
the residual orientations of the rest frame.

## 3. Finite unitary `SU(2)` fibers construct spin

Differentiate the stabilizer action and choose self-adjoint generators `J_i` with

```text
[J_i,J_j] = i epsilon_(ijk) J_k,
J_+ = J_1+iJ_2,
J_- = J_1-iJ_2.
```

The commutators compute

```text
[J_3,J_+] = J_+,
[J_3,J_-] = -J_-.
```

Because the fiber is finite-dimensional and unitary, `J_3` has a largest
eigenvalue. Call it `s` and choose `v_s` with `J_3 v_s=s v_s`. The first
commutator says `J_+v_s` would have eigenvalue `s+1`; maximality therefore forces
`J_+v_s=0`.

Introduce the invariant operator

```text
J^2 = J_1^2+J_2^2+J_3^2
    = J_-J_+ + J_3(J_3+1).
```

Evaluating it on `v_s` gives `J^2v_s=s(s+1)v_s`. Since `J^2` commutes with every
`J_i`, every nonzero vector

```text
v_m proportional to J_-^(s-m) v_s
```

has the same `J^2` eigenvalue and `J_3` weight `m`. The norm calculation

```text
||J_-v_m||^2
  = <v_m,J_+J_-v_m>
  = (s+m)(s-m+1) ||v_m||^2
```

shows that the chain terminates at `m=-s` and has weights

```text
m = s,s-1,...,-s.
```

Therefore `2s` is a nonnegative integer and the irreducible fiber has dimension
`2s+1`. This constructed irreducible action is what “massive spin `s`” means.

For `s=1`, the fiber has weights `1,0,-1` and is isomorphic to the complexified
rest-space `k^perp_C` with its ordinary rotation action. This—not the existence of
a four-vector field—is the physical input consumed by the massive vector bridge.

## 4. Null momentum constructs an exact stabilizer sequence

Let `k` be nonzero and null. Metric degeneracy is now meaningful rather than a
defect: the radical of `eta` on `k^perp` is exactly `span(k)`. Quotienting that
unobservable null direction constructs the screen space

```text
Q_k=k^perp/span(k),
< [x],[y] >_Q=-eta(x,y).
```

The displayed form is independent of representatives and positive definite.
The spacetime orientation, time orientation, and chosen future ray of `k` induce
an orientation on the quotient, so `Q_k` is an intrinsic oriented Euclidean
two-space.

Work first in the connected Lorentz group and write

```text
K_k^L={r in SO^+(V,eta) | rk=k}.
```

Every `r in K_k^L` preserves `k^perp` and its radical, hence constructs a
rotation of the quotient:

```text
pi_Q:K_k^L->SO(Q_k),
pi_Q(r)[x]=[rx].
```

This is a homomorphism because both sides act by composition on the same class.
It is onto: choose one null `n` with `k.n=1`, represent `Q_k` by the orthogonal
screen `E={k,n}^perp`, extend any rotation of `E` by fixing `k,n`, and then
forget that noncanonical witness.

The kernel must now be constructed. For a class `q=[xi] in Q_k`, define

```text
N_q(v)
 =v+(k.v)xi-[xi.v+(xi^2/2)(k.v)]k.
```

Replacing `xi` by `xi+a k` cancels between the second and third terms, so
`N_q` depends only on `q`. Direct expansion computes

```text
eta(N_q u,N_q v)=eta(u,v),
N_q k=k,
[N_q x]=[x] for x in k^perp.
```

Thus `N_q in ker pi_Q`. Substitution into the same formula also gives

```text
N_q N_r=N_(q+r).
```

Conversely, let `a in ker pi_Q` and choose any `n` with `k.n=1`. Define

```text
nu(a)=[a n-n] in Q_k.
```

If `n'` is another such vector, `n'-n in k^perp`; because `a` acts trivially
on `Q_k`, the two definitions differ only by `span(k)`. Hence `nu(a)` is
choice independent. Metric preservation of `n^2` and `n.x`, followed by
linearity, reconstructs exactly the displayed map `N_(nu(a))`. Therefore
`q |-> N_q` and `nu` are inverse group homomorphisms.

We have constructed the exact sequence

```text
1 -> (Q_k,+) --N--> K_k^L --pi_Q--> SO(Q_k) -> 1.
```

Conjugation is also computed on the same input:

```text
r N_q r^(-1)=N_(pi_Q(r)q).
```

A choice of screen splits the sequence and displays the familiar semidirect
product, but the sequence and its maps do not depend on that choice.

Pull this sequence back to the chosen spin cover. The translation group `Q_k` is
simply connected and lifts uniquely; the quotient becomes the double cover
`Spin(Q_k)` of `SO(Q_k)`. Thus the physical stabilizer has the intrinsic form

```text
1 -> (Q_k,+) -> K_k -> Spin(Q_k) -> 1,
```

with `Spin(Q_k)~=Spin(2)`. This covering statement is the theorem-contract part;
all vector-space and kernel maps were computed above.

## 5. Finite polarization selects the zero translation spectrum

Let `sigma:K_k->U(H_k)` be the irreducible physical action, with `H_k`
finite-dimensional. The normal subgroup `Q_k` is Abelian, so its commuting
unitaries are simultaneously diagonalizable. Their finite joint spectrum is a
finite set `T subset Q_k^*`, and on the `tau` eigenspace

```text
sigma(N_q)=exp(i tau(q)).
```

The conjugation identity from Section 4 makes `T` invariant under every screen
rotation. A nonzero `tau` has a full circular rotation orbit, which is infinite.
Since `T` is finite, it can contain only

```text
T={0}.
```

Therefore the entire translation subgroup acts trivially:

```text
sigma(N_q)=identity.
```

The representation factors through `K_k/Q_k=Spin(2)`. This quotient is Abelian,
so an irreducible unitary representation is one-dimensional. If `theta` denotes
the physical rotation angle, the double cover has period `4pi`, and its
characters are

```text
sigma_h(theta)=exp(i h theta),
h in (1/2)Z.
```

This one-dimensional character is the helicity-`h` physical fiber `C_h`.
Pairing `h` with `-h` requires an additional parity or reality presumption; it
does not follow from the proper connected group.

The discarded alternative is now precise. If the translation spectrum contains
`tau!=0`, rotation generates its circular orbit and the fiber is necessarily
infinite-dimensional: this is the continuous-spin branch, not a defective
finite-helicity calculation.

## 6. Casimirs record, but do not construct, the fiber

Define the Pauli--Lubanski vector

```text
W^mu = (1/2) epsilon^(mu nu rho sigma) P_nu M_(rho sigma).
```

At massive rest momentum, substitution of `P=k=(m,0,0,0)` gives, up to the fixed
epsilon convention,

```text
W^0=0,
bold W=m bold J,
W^2=-m^2 J^2=-m^2 s(s+1).
```

For a null finite-helicity fiber, trivial null translations remove the transverse
components and the remaining rotation character gives

```text
W^mu = h P^mu,
W^2=0.
```

Thus the Casimirs verify the labels already constructed from the stabilizer action.
They do not reveal helicity from `W^2` alone and do not choose a covariant field
carrier or equation.

## 7. Exact output consumed by a field equation

The constructed particle input is

```text
massive:  (O_m^+, sigma_s:SU(2)->U(V_s)),
massless: (O_0^+, sigma_h:K_k->U(C)),  sigma_h(N_q)=1.
```

A covariant carrier `F` generally contains more than this physical fiber. A local
equation and gauge map must remove the excess so that

```text
ker D(k) / im R(k) ~= V_s       (massive),
ker D(k) / im R(k) ~= C_h       (single massless helicity),
```

or a declared direct sum such as `C_(+1) direct-sum C_(-1)`. The isomorphism must
intertwine `K_k`; matching the number of components is not sufficient.

This is the typed edge into the realization and local-symbol nodes. It prevents a
named equation from appearing before the spin/helicity content it is required to
realize.

## Checks and boundary

- The massive ladder calculation constructs all weights and their positive norms.
- The massless spectral-orbit calculation distinguishes finite helicity from the
  continuous-spin branch.
- The vector cases are checks of `s=1` and `h=+/-1`, not definitions of those
  labels.
- Continuous spin, tachyonic orbits, reducible multiplets, parity completion, and
  interacting fields remain outside this node.
- Bekaert--Boulanger, Wigner, and Weinberg provide the classification theorem
  boundary; the stabilizer exact sequence, finite-spectrum obstruction, ladder,
  quotient, and character calculations above supply the internal construction used
  by this project.

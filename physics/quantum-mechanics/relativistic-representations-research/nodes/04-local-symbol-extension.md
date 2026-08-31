# N4 — Local Field Equations for Arbitrary Finite Spin and Helicity

Status: universal free chiral families supported; parity-paired symmetric potential families supported separately in N4a/N4b  
Technical companion: [N4a polynomial-complex details](04a-polynomial-complex-details.md)

For the complete parity-paired integer-spin route from potential equation through
causal response to one-particle amplitude, read the distilled
[N4m field machine](04m-finite-integer-spin-field-machine.md) before its proof
packets.

## Read this node as one construction

**Input from N2a:** a massive spin fiber `V_s` or a massless helicity line `C_h`.  
**Input from N2b:** the tuple
`(F_(m,n),Res_(K_k)F_(m,n),j_sigma)`, including the equivariant
vector–spinor bridge and an explicit fiber inclusion.  
**Input from N3:** a field realizes the particle when its plane-wave kernel modulo
gauge is that fiber as a little-group representation.  
**Output here:** one local covariant equation for every
`s,h in {0,1/2,1,3/2,...}`.

The semantic path is

```text
physical spin/helicity
  -> Lorentz carrier containing that fiber
  -> polynomial-extension obligation from N3
  -> momentum-space symbol selecting it
  -> p_mu becomes i partial_mu
  -> local spacetime equation.
```

This node first constructs a uniform family. Dirac, Proca, Rarita--Schwinger,
Fierz--Pauli, Maxwell potentials, and metric potentials are alternative carrier
choices with extra parity, reality, gauge, or differential-order requirements.
They are not used to define spin or helicity.

## 1. Consume the constructed vector--spinor bridge

[N2b](02b-lorentz-carriers.md) already constructs the objects used here:

```text
Lorentz bivectors
  -> Hodge projectors and commuting chiral ideals
  -> fundamental spinor carrier S
  -> SL(S) double cover acting on Herm(S)
  -> equivariant iota:V->Herm(S)
  -> iota(k)=lambda tensor conjugate(lambda) for future-null k.
```

N4 does not reconstruct this chain or introduce a preferred matrix basis. It
consumes `iota`, the chiral carriers, their massive restriction, and their null
helicity line in order to construct local symbols.

## 2. Build the finite chiral carriers

Symmetric powers now construct the finite chiral carriers:

```text
F_(j_L,j_R)
  = Sym^(2j_L)(S) tensor Sym^(2j_R)(bar S),

j_L,j_R in {0,1/2,1,...}.
```

[N2b](02b-lorentz-carriers.md) constructs these carriers from the invariant Hodge
split and the two commuting chiral actions. In
particular, `F_(s,0)=Sym^(2s)(S)` is no longer an imported label.

At massive rest, the little group is the diagonal `SU(2)`. Its action on
`F_(s,0)` is exactly the spin-`s` symmetric power constructed in `N2a`:

```text
F_(s,0) restricted to SU(2) ~= V_s.
```

Thus `(s,0)` contains one spin and no lower-spin rest-frame summand. It is a
uniform direct carrier for the construction below. No minimality claim is made
until N5/N6 defines and compares a semantic cost.

## 3. Massive spin `s`: one equation for every `s`

Fix `m>0` and any `s in {0,1/2,1,...}`. Choose

```text
Phi_(A_1...A_(2s)) in F_(s,0).
```

The orbit is `p^2=m^2`, so construct the scalar symbol on this carrier

```text
D_(m,s)(p) = (p^2-m^2) identity_(F_(s,0)).
```

It is Lorentz equivariant because `(Ap)^2=p^2` and the identity commutes with the
carrier action:

```text
D_(m,s)(Ap) rho_s(A)
  = (p^2-m^2)rho_s(A)
  = rho_s(A)D_(m,s)(p).
```

Its fibers are computed without components:

```text
p^2 != m^2  => ker D_(m,s)(p)=0,
p^2  = m^2  => ker D_(m,s)(p)=F_(s,0).
```

At `k=(m,0,0,0)`, the second line carries exactly `V_s` under the little group.
N3 therefore turns the positive-energy solutions into the massive spin-`s`
Poincare representation.

With `p_mu <-> i partial_mu`, the spacetime equation is

```text
(Box+m^2) Phi_(A_1...A_(2s)) = 0
```

up to the fixed Fourier-sign convention.

This is a universal local second-order realization. It is complex and chiral; it
does not by itself impose parity, a real structure, a first-order equation, an
action, or a conventional tensor/potential interpretation. Those extra demands
lead to other equations. Therefore the result is existence of a local realization,
not uniqueness of dynamics.

## 4. Massless helicity magnitude `h`: one equation for either sign

### Scalar sector

For `h=0`, choose `F_(0,0)=C` and the null-shell symbol

```text
D_0(p)=p^2,
```

which becomes the massless Klein--Gordon equation.

### Nonzero chiral sector

Fix `h>0`, put `n=2h`, and choose

```text
phi in F_(h,0)=Sym^n(S).
```

The alternating form constructs `x^flat=epsilon(x,-):S->C`. Let
`iota_(x^flat):Sym^n(S)->Sym^(n-1)(S)` be symmetric-algebra contraction and
define the prior natural map

```text
C_n:(S tensor bar S) tensor Sym^n(S)
       -> Sym^(n-1)(S) tensor bar S,

C_n((x tensor bar y) tensor phi)
  =iota_(x^flat)(phi) tensor bar y.
```

The momentum symbol is evaluation of this map:

```text
D_h(p)phi=C_n(iota_C(p) tensor phi).
```

It is linear in `p`, hence local and first order. Since `epsilon`, symmetric
multiplication, and contraction are natural, their common transformation computes

```text
D_h(Ap)rho_h(A)=rho_target(A)D_h(p).
```

This is a commuting naturality square, not an index-pattern assertion.

At nonzero null `k`, N2b supplies

```text
iota_C(k)=lambda tensor bar(lambda),
ell=span(lambda).
```

The covector `lambda^flat=epsilon(lambda,-)` has kernel `ell`. Its contraction
has the exact sequence

```text
0 -> Sym^n(ell)
  -> Sym^n(S)
  --iota_(lambda^flat)--> Sym^(n-1)(S)
  -> 0.
```

To witness exactness, choose any right inverse `u:C->S` of
`lambda^flat`. Then `S=ell direct-sum im(u)`; grading the symmetric algebra by
the number of `im(u)` factors makes contraction surjective and leaves only
`Sym^n(ell)` in its kernel. The witness uses a splitting, but the sequence and
kernel do not depend on that choice. The nonzero factor `bar(lambda)` therefore
gives

```text
ker D_h(k)=Sym^n(ell).
```

This is exactly the direct line and intertwiner constructed by N2b. It carries
helicity `-h` in that convention; the conjugate carrier and equation give `+h`.

If `p^2!=0`, then `det iota_C(p)!=0`, so the induced map
`S^*->bar S` is invertible. If `D_h(p)phi=0`, composing with every covector of
`bar S` makes every contraction of `phi` vanish; hence `phi=0`. Nonzero
solutions occur only on the null cone, and N3 identifies their positive-energy
space with the massless helicity representation.

Fourier transformation gives the zero-rest-mass equation

```text
partial^(A A') phi_(A A_2...A_(2h))=0.
```

It is a gauge-free curvature realization. A potential realization requires a
separate differential complex whose cohomology is this helicity line.

## 5. The complete range from zero through spin two

The same two formulas specialize as follows:

| Label | Massive minimal chiral realization | Massless chiral realization | Familiar alternative carrier |
| --- | --- | --- | --- |
| `0` | scalar Klein--Gordon | scalar Klein--Gordon | none needed |
| `1/2` | `(1/2,0)` spinor with Klein--Gordon | Weyl equation on `phi_A` | parity-paired Dirac field |
| `1` | `(1,0)` symmetric spinor with Klein--Gordon | self-dual Maxwell curvature `phi_(AB)` | Proca or Maxwell vector potential |
| `3/2` | `(3/2,0)` symmetric spinor with Klein--Gordon | chiral curvature `phi_(ABC)` | Rarita--Schwinger potential |
| `2` | `(2,0)` symmetric spinor with Klein--Gordon | chiral Weyl curvature `phi_(ABCD)` | Fierz--Pauli or metric gauge potential |

The second and third columns are the uniform representation-theoretic answer. The
last column adds physical or presentational requirements and must be derived by a
separate carrier resolution. In particular, the massive chiral Klein--Gordon
realization is not being renamed “Dirac,” “Proca,” or “Fierz--Pauli.” It realizes
the same one-particle spin with a different off-shell field system.

## 6. Uniformity over all finite labels

The allowed finite labels form the countable set

```text
(1/2)N_0 = {0,1/2,1,3/2,...}.
```

The carrier functor `n |-> Sym^n(S)` and the natural symbols above are defined
for every `n in N_0`. This is a countable family of independently checked finite
sectors, not a single completed infinite-dimensional field.

A generating series would only repackage these sectors. A genuine completion
requires a topology or norm, degree weights, a mass-growth law, operator domains,
and rules for mixing degrees. Those are new N6 presumptions, so such a series is
not part of this node's field-equation proof.

This family is also not Wigner's continuous-spin representation: every degree is
a separate finite-spin or finite-helicity sector, whereas continuous spin has
nontrivial null-translation data.

## 7. Where potential and gauge equations enter

The universal massless equation uses gauge-invariant chiral curvatures because the
physical helicity is then a literal one-dimensional kernel. Potentials replace
this short route by a complex:

```text
gauge parameter --R(p)--> potential --D(p)--> equation,
physical fiber = ker D(k)/im R(k).
```

N4a constructs this complex uniformly for every bosonic integer `s>=1`. Its
traceless gauge parameters, double-traceless symmetric potentials, and quadratic
symbol have null-fiber cohomology

```text
Sym_0^s(Q_k tensor C)^* ~= C_(+s) direct-sum C_(-s),
```

while all non-null cohomology vanishes. This includes Maxwell at `s=1` and the
metric-like gauge complex at `s=2`. It is a parity-paired potential realization,
not the one-character chiral curvature route constructed in this node.

The construction, exact screen sequence, and characteristic checks are retained
in [N4a](04a-polynomial-complex-details.md). The analogous symmetric
spinor-tensor construction is proved in
[N4b](04b-half-integer-potential.md): tensor rank `n` gives the parity-paired
helicities `+(n+1/2)` and `-(n+1/2)`. General mixed-symmetry potential resolutions
remain open branches, not prerequisites for the universal curvature family.

## 8. Checks, assumptions, and downstream edge

Supported checks:

- massive: the only characteristic shell is `p^2=m^2`, and the rest fiber is
  exactly `V_s`;
- massless: null factorization reduces the kernel to one helicity line, while an
  invertible non-null momentum gives zero kernel;
- locality: the massive symbols are quadratic and the nonzero-helicity massless
  symbols are linear in momentum;
- uniformity: the same carrier functor and natural symbols apply at every finite
  degree.

Assumptions and boundaries:

- four-dimensional Minkowski spacetime and the proper connected spin-covered
  Poincare group;
- free complex fields and positive-energy solution sectors;
- no parity, reality, action, statistics, interaction, or potential formulation is
  inferred unless added explicitly;
- the direct family over all half-integer labels is supported, while a completed
  interacting infinite tower is not.

This node supplies N5 with the complete `0` through `2` chiral table and supplies
N6 with a uniform finite-degree functor, not a completed tower. N4a remains the
technical workspace for polynomial complexes and alternative gauge carriers.

## Source boundary

- Bekaert--Boulanger provide the modern induced-representation and covariant
  equation classification used as an external theorem boundary.
- Bargmann--Wigner provide the foundational arbitrary-spin covariant-wave-equation
  comparison.

The spinor factorization and exact-sequence kernel computation used by this node
are displayed internally rather than delegated to those sources.

# N4c — Variational Completion Audit

Status: bosonic and complex fermionic invariant pairings, trace reversals, formal self-adjointness, and equation equivalence supported; real fermionic form and presymplectic comparison remain developing  
Consumes: [N4a bosonic potentials](04a-polynomial-complex-details.md), [N4b fermionic potentials](04b-half-integer-potential.md), and [action-principle source contracts](../sources/action-principle-contracts.md)  
Produces: a typed criterion for deciding what an action adds and when an action presentation is equivalent to the supported equation complex

## Research contract

- **Question:** what new mathematical and physical structure is added when the
  N4a/N4b symbol complexes are required to arise from a local quadratic action?
- **Presumptions:** flat four-dimensional spacetime; free symmetric fields;
  constant-coefficient locality; the trace-constrained carriers already constructed
  in N4a/N4b; compactly supported variations or boundary conditions eliminating
  surface terms.
- **Material bindings:** N4a/N4b operator algebras; primary contracts `AP-01` and
  `AP-02`; `AP-03/AP-04` only delimit unconstrained and source-coupled comparisons.
- **Output:** an action-completion diagram, constructed bosonic pairing and Euler
  operator, computed Bianchi identities, an equivalence-cost audit, and exact
  remaining proof obligations.
- **Boundary:** the bosonic quadratic action is supported on compactly supported or
  boundary-compatible fields, but this node does not claim positivity, canonical
  normalization, gauge fixing, propagator, quantization, interaction, or a
  completed real/Majorana fermionic action.

## 1. The missing object is a duality, not another helicity equation

N4a/N4b construct a gauge complex at each momentum,

```text
G --R(p)--> F --D(p)--> E,
```

and compute its physical cohomology. An action requires additional arrows. Choose a
nondegenerate invariant pairing that identifies the equation target with the dual
of admissible field variations, then construct an Euler operator `Euler(p)` satisfying

```text
Euler(p)^dagger=Euler(p),
Euler(p)R(p)=0 modulo the parameter constraint.
```

The quadratic functional is then a consequence,

```text
I[Phi]=(1/2) integral <Phi,Euler(i partial)Phi> dx,
```

because evaluation on the same variation gives

```text
d/dt I[Phi+t delta Phi]|_(t=0)
 = integral <delta Phi,Euler(i partial)Phi> dx
```

only after formal self-adjointness and the boundary convention have been proved.
Thus `D Phi=0` and `delta I=0` are not synonymous assertions. The action adds a
duality and an integrability condition on the equation operator.

## 2. The bosonic pairing and formal adjoint are constructed invariantly

### 2.1 The need to vary a field constructs the fiber pairing

Let

```text
P_s=Sym^s(V_C^*)
```

be the homogeneous auxiliary-polynomial carrier used in N4a. The Lorentz metric
identifies every covector slot with a vector slot, so complete contraction of two
rank-`s` tensors constructs the Fischer pairing

```text
<phi,psi>_s=[conj(phi)(partial_u) psi(u)]_(u=0).
```

The displayed polynomial formula is shorthand for contracting all slots with the
metric; it is independent of a basis and Lorentz invariant. On the real carrier it
restricts to the real symmetric bilinear pairing needed by the action. Its
indefinite signature is expected and is not a positivity claim.

Evaluate multiplication and contraction on the same two homogeneous polynomials:

```text
<P phi,psi>=<phi,A psi>,
<U phi,psi>=<phi,T psi>.
```

The first identity removes the inserted factor `p.u` by one derivative; the second
removes `u^2` by two metric contractions. Nondegeneracy on the full symmetric
carrier therefore constructs the fiber adjoints

```text
P^dagger=A,
A^dagger=P,
U^dagger=T,
T^dagger=U.
```

For spacetime fields use

```text
(Phi,Psi)=integral <Phi(x),Psi(x)>_s dx.
```

Compact support, or boundary conditions with zero surface pairing, makes
`p=i partial` formally self-adjoint. Hence the fiber identities above are also the
formal adjoint identities of the constant-coefficient operators. Reality of the
action is obtained by restricting the complex Fourier bookkeeping to the real
field form.

### 2.2 Double-traceless fields have a nondegenerate two-layer decomposition

Construct the degree operator `N=u.partial_u`. Product differentiation on one
arbitrary polynomial gives

```text
A U-U A=2P,
T U-U T=4N+2d.
```

The second identity explains why trace insertion is not a projector. In the
present dimension `d=4`, if `k` is traceless and has degree `s-2`, then

```text
T(U k)=4s k.
```

For `phi in F_s=ker T^2`, construct

```text
k=(1/(4s))T phi,
h=phi-U k.
```

Both `k` and `h` are traceless, and substitution computes

```text
T h=T phi-T(U k)=T phi-4s k=0,
phi=h+U k.
```

The decomposition is unique: tracing `h+U k=0` gives `4s k=0`, hence `k=0`
and then `h=0`.

**Theorem contract (Fischer decomposition).** For a nondegenerate quadratic form
over characteristic zero,

```text
P_s=direct-sum_(j=0)^(floor(s/2)) U^j ker(T|_(P_(s-2j))).
```

Its constructive coefficient is

```text
T(U^j h_r)=2j(2r+d+2j-2)U^(j-1)h_r,
```

for traceless homogeneous `h_r`. The coefficients do not vanish for `d=4` and
nonnegative degrees, so repeated trace subtraction constructs the summands. The
contract supplies only the nondegeneracy of the metric pairing on each traceless
summand; the two layers actually used by `F_s` were constructed explicitly above.

They are orthogonal because

```text
<h,U k'>=<T h,k'>=0,
<U k,U k'>=<k,T(U k')>=4s<k,k'>.
```

The Fischer contract and `4s!=0` therefore make the restricted pairing on

```text
F_s=ker T direct-sum U ker(T|_(P_(s-2)))
```

nondegenerate. Constrained variations can consequently detect an Euler tensor in
`F_s`; no unmentioned ambient projection is needed.

### 2.3 Trace reversal is invertible on the constrained carrier

On `phi=h+U k`, the trace-reversal map from AP-01 evaluates to

```text
M_B phi
 =(identity-(1/4)U T)(h+U k)
 =h+(1-s)U k.
```

For `s>=2` it is therefore an automorphism of `F_s`, with

```text
M_B^(-1)=identity-(1/(4(s-1)))U T.
```

At `s=1`, trace vanishes by degree and `M_B=identity`; the scalar case is separate
and also has `M_B=identity`. At `s=2`, `M_B^2=identity`: trace reversal changes the
sign of the pure-trace layer while fixing the traceless layer.

Thus the trace-reversed equation contains the same vacuum kernel:

```text
E_B phi=0
iff M_B D phi=0
iff D phi=0.
```

This implication uses both the four-dimensional trace decomposition and the
double-trace constraint. It is not an equality inferred from the conventional
name “Einstein tensor.”

### 2.4 The self-adjointness defect factors through the constraint

The adjoints from Section 2.1 compute

```text
D^dagger=p^2-P A+(1/2)U A^2,
M_B^dagger=M_B.
```

Using only

```text
[A,P]=p^2,
[T,P]=2A,
[A,U]=2P,
[T,A]=0,
```

reduce the difference of the two composites on the full polynomial carrier:

```text
M_B D-(M_B D)^dagger
 =(1/8)(U^2 A^2 T-U P^2 T^2).
```

This is stronger than checking selected ranks. For common inputs
`phi,psi in F_s`, evaluation in the constructed pairing gives

```text
<psi,U^2 A^2 T phi>=<T^2 psi,A^2 T phi>=0,
<psi,U P^2 T^2 phi>=0.
```

Therefore

```text
<psi,E_B phi>=<E_B psi,phi>,
E_B=M_B D,
```

on the entire double-traceless carrier for every finite integer `s`. Together with
the nondegenerate restricted pairing, this constructs the real quadratic action

```text
I_B[Phi]=(1/2) integral <Phi,E_B(i partial)Phi> dx
```

and its variation

```text
delta I_B[Phi]=integral <delta Phi,E_B(i partial)Phi> dx.
```

Its Euler equation is equivalent to N4a's `D Phi=0`. Overall normalization,
positivity, boundary charges, gauge fixing, and quantization remain additional
questions.

## 3. Bosonic Bianchi identity is computable invariantly

Use N4a's operators and introduce only the adjoints demanded by the pairing:

```text
U phi(u)=u^2 phi(u),
P^dagger=A,
U^dagger=T.
```

The Fronsdal symbol and its constraint operator are

```text
D=p^2-P A+(1/2)P^2 T,
C=A-(1/2)P T.
```

Using `[A,P]=p^2` and `[T,P]=2A`, evaluate the composite on one arbitrary
double-traceless field:

```text
C D=-(1/4)P^3 T^2.
```

Hence `C D phi=0` on `F_s=ker T^2`. This is the constrained Bianchi identity; it
is stronger semantic information than the already known gauge composite
`D P=(1/2)P^3T`, because it controls the adjoint/source side of the complex.

The source-backed action candidate uses the trace-reversal operator

```text
M_B=I-(1/4)U T,
E_B=M_B D.
```

Its divergence is computed without components:

```text
A E_B
 =C D-(1/4)U A T D
 =U[-(1/4)A T D]              on ker T^2.
```

Therefore `A E_B phi` is a pure trace. For a traceless gauge parameter `epsilon`,

```text
<P epsilon,E_B phi>
 =<epsilon,A E_B phi>
 =<T epsilon,-(1/4)A T D phi>
 =0.
```

Section 2 proves the required formal self-adjointness, so this calculation now
constructs gauge invariance of `I_B`. It also constructs the source condition for a coupling `<Phi,J>`:
the traceless projection of `A J` must vanish, not necessarily `A J` itself.

## 4. Fermionic Bianchi identity has the same semantic shape

Use N4b's

```text
S=Slash-P Gamma,
Gamma^3 psi=0,
Gamma epsilon=0,
```

and define the first-order Bianchi operator

```text
B=A-(1/2)P T-(1/2)Slash Gamma.
```

The five Clifford/operator relations of N4b reduce the full composite to

```text
B S=(1/2)P^2 Gamma^3.
```

Thus `B S psi=0` on the triple-gamma-traceless carrier. This is a direct
calculation: its common input is `psi`, its target is the rank-`n-1`
spinor-tensor carrier, and the obstruction is exactly the declared field
constraint.

Let

```text
Y psi(u)=gamma(u)psi(u),
U=Y^2,
M_F=I-(1/2)Y Gamma-(1/4)U T,
E_F=M_F S.
```

The missing construction is now completed in
[N4i](04i-half-integer-green-construction.md). The Dirac--Fischer pairing gives
`Y^dagger=Gamma` and `P^dagger=A`; its three gamma-layer decomposition proves
`M_F` invertible on `ker Gamma^3`. Normal ordering computes

```text
M_FS-(M_FS)^dagger
 =(1/4)(Y^2P Gamma^3-Y^3A Gamma^2).
```

Both terms vanish between triple-gamma-traceless fields, so `E_F=M_FS` is
formally self-adjoint. Invertibility of `M_F` then proves

```text
E_Fpsi=0 iff Spsi=0.
```

N4i also constructs the constrained-adjoint identity `R^dagger M_F=B`, which
turns the projected source law into the gauge-fixing condition used by its causal
response. A real Grassmann action still requires a declared Majorana or other
reality convention; it is not inferred from the complex formal-adjoint result.

## 5. What the action adds, and what it does not

| Structure | N4a/N4b equation complex | Additional action content |
| --- | --- | --- |
| Physical one-particle fiber | already computed by null-screen cohomology | no new helicity |
| Off-shell equation | polynomial `D` or `S` | Euler representative `E_B=M_B D` or `E_F=M_F S` |
| Duality | unnecessary for the kernel quotient | invariant real/Dirac fiber pairing and spacetime integral |
| Gauge identity | equation-side `D R=0` or `S R=0` | adjoint Noether identity and constrained source law |
| Normalization | equation can be multiplied by a nonzero scalar | action coefficient fixes normalization only after a source/quantization convention |
| Boundary data | absent from the momentum-fiber calculation | integration domain and surface-term convention |
| Observables beyond plane waves | physical quotient only | presymplectic current, charges, propagator after further constructions |

An action therefore strengthens the off-shell presentation but does not follow from
the Poincare representation alone. The trace reversals `M_B,M_F`, pairing, reality,
and boundary choice are extra presumptions.

## 6. Three inequivalent meanings of “same theory”

The audit separates three tests:

1. **Physical-fiber equivalence:** standard-momentum cohomologies are isomorphic as
   little-group modules. N4a/N4b already prove this.
2. **Local Euler equivalence:** a local invertible field/target map intertwines the
   gauge complexes, preserves characteristic strata, and carries one formally
   self-adjoint Euler operator to the other up to a boundary term.
3. **Source-response equivalence:** after coupling admissible currents and gauge
   fixing, the inverse kinetic operators give the same current-current amplitude.

The relations are not a hierarchy without extra maps:

```text
local Euler equivalence
  --plus compatible current map and gauge fixing--> source-response equivalence
  --plus orbit/analytic regularity---------------> physical-fiber equivalence

source-response equivalence
  -----------------------------------------------> same exchanged sector only.
```

No converse is automatic, and identical exchange need not determine unused or
auxiliary off-shell sectors. `AP-04` provides the complementary warning:
vacuum-equivalent nonlocal equations can differ in current exchange because their
Bianchi identities select different source couplings.

## 7. Low-spin semantic checks

- `s=1`: traces vanish by degree, `M_B=I`, and the N4a Maxwell symbol is already
  the Euler operator.
- `s=2`: `M_B` is an involutive trace reversal; Section 2 proves that it changes
  the Ricci-like equation into a self-adjoint linear Einstein-like Euler tensor
  without changing its vacuum kernel.
- `n=0`: `S=Slash` is the Dirac symbol; the complex Dirac pairing and formal
  adjoint are included in N4i, while a real action still requires a declared
  reality convention.
- `n=1`: the trace constraints are automatic, but `M_F` is nontrivial and produces
  the Rarita--Schwinger Euler representative. Thus even the first fermionic gauge
  field shows why equation and variational operators must be distinguished.

The arbitrary-rank bosonic and fermionic formal-adjoint identities are now
supported. Low-rank calculations remain independent checks rather than the proof.

## 8. Audit disposition and next constructions

Supported now:

- the action-completion data absent from representation/cohomology alone;
- the invariant bosonic Fischer pairing and its nondegenerate restriction to
  `ker T^2`;
- invertibility of bosonic trace reversal and equivalence of `E_B phi=0` with
  `D phi=0` in four dimensions;
- formal self-adjointness of `E_B=M_B D` on every finite-rank double-traceless
  bosonic carrier, hence the constrained quadratic action;
- the bosonic identity `C D=-(1/4)P^3T^2`;
- the fermionic identity `B S=(1/2)P^2Gamma^3`;
- the invariant complex Dirac--Fischer pairing on `ker Gamma^3`;
- invertibility of `M_F`, formal self-adjointness of `E_F=M_FS`, and vacuum
  equivalence with N4b's equation;
- the fermionic constrained source identity `R^dagger M_F=B`;
- the projected bosonic Noether/source condition;
- the three-level equivalence criterion and auxiliary cost of removing trace
  constraints.

Still developing:

- select and construct a Majorana or other real fermionic form, including its
  Grassmann and sign conventions;
- derive the presymplectic current and compare its quotient with the N3 physical
  inner product;
- only then compare constrained and compensator formulations at the local Euler
  and source-response levels.

No heavy computation is needed for either adjoint or the two Bianchi identities:
their invariant operator reductions are shorter and stronger than a rank-by-rank
component check. N4i records the bounded fermionic check only as independent
evidence.

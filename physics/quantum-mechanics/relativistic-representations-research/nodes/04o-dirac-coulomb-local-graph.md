# N4o — Dirac--Coulomb Local Graph from the Representation Spine

Status: developing; the inherited massive Dirac carrier, `U(1)` deformation,
curvature obstruction, static Hamiltonian and manifest-rotation reduction are
supported; N4p factors the remaining magnetic multiplicity but shows that the
half-line fiber is still the old gamma subblock and therefore not the sought
computational reduction; gap eigenvalues and projectors remain open  
Consumes: [N2a spin and helicity](02a-spin-and-helicity.md), [N2b Lorentz
carriers](02b-lorentz-carriers.md), [N3 realization bridge](03-realization-bridge.md),
[N4 local symbols](04-local-symbol-extension.md), [N4b Clifford
construction](04b-half-integer-potential.md), [N4c action audit](04c-action-completion-audit.md),
[N4i fermionic adjoint](04i-half-integer-green-construction.md), [N4d computation
interface](04d-computation-interface.md), [N4n reduction audit](04n-algebraic-spectrum-bridge.md),
and [endpoint contracts](../sources/computability-endpoint-contracts.md)  
Worktable binding: the undeveloped Dirac claim in
[`relativistic-representations.typ`](../../relativistic-representations.typ)
lines 1383--1396 is a manuscript candidate, not an input authority  
Produces: one typed local graph from the established representation spine to a
self-adjoint Coulomb gap observable, plus the first non-component reduction edge

## Research contract

- **Question:** how does the existing free representation construction reach a
  well-typed relativistic Coulomb bound-state problem without importing gamma
  matrices, a Hamiltonian, or a radial equation independently?
- **Inherited presumptions:** four-dimensional Minkowski space, the proper
  connected spin cover, the two Weyl carriers, their Clifford action, the massive
  spin-`1/2` rest fiber, and the invariant Dirac pairing.
- **New presumptions:** `m>0`; a chirality-paired first-order off-shell realization
  and, when parity is claimed, a chosen extension beyond the connected spin group;
  a charged Hermitian line with a `U(1)` connection; a future unit time direction;
  an external static point Coulomb field; and the distinguished self-adjoint
  extension in the subcritical regime.
- **Observable:** the discrete spectral measure of the distinguished Hamiltonian
  in `(-m,m)`: eigenvalues together with their spectral projectors. Energies alone
  are a later projection of this object.
- **Boundary:** this node does not yet derive the Sommerfeld levels, construct an
  extra Coulomb symmetry, prove a radial formula, or replace the external field by
  a dynamical photon sector.

## 1. Dependency audit: what the past actually supplies

| Incoming node | Exact object consumed here | What it does not supply |
| --- | --- | --- |
| N2a/N2b | `V_(1/2)`, `S`, `bar S`, the rest group `K_tau~=SU(2)`, and its carrier maps | a massive first-order equation or interaction |
| N3 | the little-group intertwiner criterion for “same particle” | an off-shell field operator |
| N4 | the chiral massive equation `(p^2-m^2)Phi=0` on `S` | parity pairing, a Dirac equation, or a positive Hilbert form |
| N4b | `Delta=S direct-sum bar S` and the natural action `gamma(v)` with the Clifford identity | its massive deformation or Coulomb domain |
| N4c/N4i | the invariant Dirac form `beta` and `gamma(v)` self-adjointness relative to it | positivity before a time direction is chosen |
| N4d | the background-deformation and resolvent obligations | a particular coupling or closed Hamiltonian |
| N4n | witness/recovery/cost contracts for a local reduction graph | a method selector or a Dirac--Coulomb solution |

The manuscript's displayed Dirac equation is therefore downstream material to be
replaced eventually by this construction. It cannot be used to justify the node
that justifies it.

## 2. The old Clifford map constructs the massive Dirac carrier

N4b constructs

```text
Delta=S direct-sum bar S,
gamma(v)gamma(w)+gamma(w)gamma(v)=2 eta(v,w)I_Delta.
```

No matrix representative is needed. The new physical choice is to demand a
chirality-paired first-order operator with mass `m`. Since the scalar identity is
Lorentz invariant, construct

```text
D_m(p)=slash p-mI_Delta,
slash p=gamma(p).
```

Naturality of the old Clifford map evaluates covariance on the same spinor:

```text
D_m(Ap)rho_Delta(A)z
 =rho_Delta(A)(slash p-m)z
 =rho_Delta(A)D_m(p)z.
```

The real scalar mass is a declared choice. Lorentz covariance alone would not
forbid every chirality-dependent or pseudoscalar mass convention; no uniqueness
claim is hidden here.

Apply the opposite first-order factor to the same spinor `z`:

```text
(slash p+m)D_m(p)z
  =(slash p+m)(slash p-m)z
  =(p^2-m^2)z.
```

The last equality is exactly N4b's Clifford identity at `v=w=p`. Thus a Dirac
solution maps to N4's massive Klein--Gordon solution on the parity-paired carrier,
and away from the mass shell the inverse is constructed rather than named:

```text
D_m(p)^(-1)=(slash p+m)/(p^2-m^2).
```

This does not make the two off-shell systems identical. It gives an explicit map
from the new first-order system to the old second-order one and exposes the scalar
denominator inherited by the free propagator.

To verify the physical fiber, let `tau` be a future unit vector and `k=m tau`.
Put

```text
B_tau=gamma(tau),
Pi_tau^plus=(I+B_tau)/2,
Pi_tau^minus=(I-B_tau)/2.
```

Because `B_tau^2=I`, these are complementary idempotents. The two off-diagonal
Clifford maps between `S` and `bar S` are inverse at `tau`, so each eigenspace is
the graph of one of those maps and is isomorphic to the fundamental rest module
`V_(1/2)`. Direct evaluation gives

```text
D_m(k)z=m(B_tau-I)z,

D_m(k)z=0
  iff Pi_tau^minus z=0
  iff z in im Pi_tau^plus~=V_(1/2).
```

At `-k`, the kernel is `im Pi_tau^minus`. N3 now identifies the future-shell
kernel with the same massive spin-`1/2` Poincare representation already realized
by N4's chiral Klein--Gordon field. This is the exact relation to the prior spine:
same on-shell particle, different constructed off-shell operator.

The direct sum alone does not construct discrete parity, because N2b deliberately
uses only the connected spin group. Relative to the chosen `tau`, construct the
spacetime reflection

```text
P_tau(t tau+x)=t tau-x,       x in Sigma,
```

and its spinor-field action, up to one constant phase,

```text
[cal(P)_tau psi](t,x)=B_tau psi(t,-x).
```

For `x` spatial, the Clifford relation computes

```text
B_tau gamma(tau)B_tau=gamma(tau),
B_tau gamma(x)B_tau=-gamma(x).
```

Thus `cal(P)_tau` intertwines `D_m` with the reflected momentum and makes the
chirality pair parity-complete only after this disconnected symmetry has been
chosen. The scalar mass is parity even by construction.

## 3. Local phase comparison constructs the `U(1)` connection

A charged field must be comparable after a spacetime-dependent phase change.
Introduce a Hermitian line `L` and let `psi` be a section of `Delta tensor L`.
For real coupling `e`, require

```text
psi -> psi'=exp(-i e chi)psi.
```

The ordinary derivative of `psi'` contains the unwanted term
`-i e dchi psi`. Introduce a real one-form `A` and construct

```text
nabla^A=d+i e A,
A -> A'=A+dchi.
```

Evaluate both transformed operations on the same field:

```text
nabla^(A') psi'
 =d(exp(-i e chi)psi)+i e(A+dchi)exp(-i e chi)psi
 =exp(-i e chi)nabla^A psi.
```

Thus the connection, rather than the phrase “minimal coupling,” is the operation
that preserves local phase comparison. Put

```text
Pi_A=i nabla^A=i d-eA,
D_(m,A)=slash Pi_A-m.
```

The Coulomb potential is not derived from Poincare or `U(1)` symmetry. It will be
an external choice of the connection.

## 4. Curvature computes the obstruction to the old scalar reduction

The free factorization cannot simply be copied. On constant vector fields the
connection curvature computes

```text
[Pi_(A,mu),Pi_(A,nu)]=-i e F_(mu nu),
F=dA.
```

Split the Clifford product into its symmetric and antisymmetric parts and apply it
to the same section:

```text
(slash Pi_A+m)(slash Pi_A-m)
 =slash Pi_A^2-m^2
 =(Pi_A^2-m^2)I
   -(i e/4)[gamma^mu,gamma^nu]F_(mu nu).
```

The first term is the covariant version of N4's scalar massive symbol. The second
is a spin--curvature endomorphism produced by the failure of covariant momenta to
commute. For a nonzero Coulomb electric field it does not vanish. Therefore

```text
free Dirac -> scalar Klein--Gordon factorization,
background Dirac -> covariant Klein--Gordon plus curvature action.
```

This is the first decisive obstruction discovered by relating the new problem to
the old spine. Reusing the scalar Green compiler from N4d/N4i without this term
would change the dynamics.

## 5. A time direction constructs the Hilbert space and Hamiltonian

The Lorentz-invariant form `beta` inherited from N4i is indefinite. Once the
external static approximation chooses `tau`, construct

```text
h_tau(z,w)=beta(z,B_tau w).
```

Using the `tau`-identification `S~=bar S` from N2b, this is the sum of the two
positive Weyl norms; fix the overall sign of `beta` so `h_tau` is positive. On the
spatial slice `Sigma=tau^perp`, the one-particle Hilbert space is therefore

```text
H_tau=L2(Sigma,Delta;h_tau).
```

Assume the external connection is static and has no spatial component. Multiplying
`D_(m,A)psi=0` by `B_tau` computes the same equation as

```text
i partial_t psi=H_A psi,

H_A=-i B_tau slash nabla_Sigma+m B_tau+e A(tau).
```

Choose the attractive point connection by the explicit physical input

```text
e A(tau)=-nu/r,
r=|x|,
0<=nu<1.
```

This constructs the symmetric minimal operator

```text
H_nu^min
 =-i B_tau slash nabla_Sigma+mB_tau-nu/r
```

on `C_c^infinity(Sigma without {0},Delta)`. The endpoint source contract supplies
an irreducible analytic theorem: in the stated subcritical regime the Coulomb
operator has a unique distinguished self-adjoint realization `H_nu`; its gap
eigenvalues admit a min--max characterization. The domain is semantic input, not
an afterthought. Other self-adjoint extensions in critical regimes may have
different discrete spectra.

The observable is now well typed as a projection-valued function:

```text
O_nu:B |-> E_(H_nu)(B),
B a Borel subset of (-m,m),
```

the projection-valued spectral measure restricted to the gap. Its atoms contain
both each eigenvalue and its projector. Equivalently, an isolated atom is recovered
from the resolvent by

```text
P_E=Res_(z=E)(z-H_nu)^(-1),
```

which consumes the resolvent contract already constructed in N4d/N4n.

## 6. The old rest group gives the first reduction edge

The selected time direction leaves the rest group `K_tau~=SU(2)` from N2a/N2b.
It acts simultaneously on space and the spinor carrier:

```text
[U(R)psi](x)=rho_Delta(R)psi(R^(-1)x).
```

For the same test spinor, covariance of `gamma`, invariance of `r`, and the chain
rule compute

```text
H_nu U(R)psi=U(R)H_nu psi.
```

The minimal domain is rotation-invariant, and uniqueness of the distinguished
extension propagates this commutation to `H_nu`. Compact `SU(2)` decomposition
therefore constructs

```text
H_tau=Hilbert-direct-sum_(j in 1/2+N_0) V_j tensor M_j,

H_nu=Hilbert-direct-sum_j I_(V_j) tensor h_(nu,j).
```

This edge removes the magnetic multiplicity `V_j` without coordinates or a tensor
expansion. It does **not** compute the spectrum: the multiplicity operator
`h_(nu,j)` still contains the radial, parity and domain information. Any further
angular operator or Coulomb symmetry must be constructed on these multiplicity
spaces and must beat direct spectral computation by N4n's whole-route audit.

[N4p](04p-dirac-angular-reduction.md) constructs that angular edge from the same
orbital, spin and total rotation actions. It separates `h_(nu,j)` into
`kappa=plus-or-minus(j+1/2)` half-line blocks and supplies an exact recovery map.
Its negative audit also proves that the residual two-involution fiber is
`Cl_2(C)~=M_2(C)`, hence a gamma subblock up to basis change. This is exact block
diagonalization, not the requested semantic reduction.

## 7. The local reduction graph and supported frontier

```text
N2a/N2b/N4b
  --carrier plus Clifford witness--> D_m

N3/N4
  --rest-fiber and factorization witnesses--> same massive particle plus free inverse

N4c/N4i
  --Dirac pairing plus chosen tau--> H_tau

charged line plus A
  --local phase covariance--> D_(m,A)
  --curvature computation--> obstruction to scalar Green reuse

static tau plus Coulomb input plus domain theorem
  --> distinguished H_nu
  --N4d/N4n resolvent contract--> O_nu

K_tau action
  --commutation witness--> {h_(nu,j)}_j.
```

Every arrow either consumes a named prior result or is computed in this node. N4p
tests and rejects the orthodox radial continuation as the intended computational
principle. The current frontier is:

- retain N4p's magnetic decomposition only as an exact check and fallback;
- before radial separation, seek a constructible relation among `H_nu`, its
  background and its observable algebra that constrains the gap measure;
- reject any candidate whose construction plus observable recovery merely
  reintroduces the same two-dimensional Clifford calculation.

## Checks and failure boundary

Supported checks:

- `D_m` factorizes to the exact massive scalar symbol already owned by N4;
- its rest kernel is the N2a/N2b spin-`1/2` module, so N3 applies;
- the `U(1)` connection covariance is evaluated on the same transformed section;
- curvature is the explicit obstruction to commuting-momentum factorization;
- the Hamiltonian and positive Hilbert form use the same chosen time direction;
- rotation covariance produces a typed isotypic reduction, not an energy claim;
- the distinguished-domain theorem types the gap observable before reduction.

Open or excluded:

- a pre-radial semantic reduction or an obstruction showing why none is cheaper;
- computation of the N4p half-line channel measures and domains only as fallback
  or independent verification;
- any Johnson--Lippmann or supersymmetric Coulomb operator and its domain;
- the exact Sommerfeld spectrum and projector recovery;
- supercritical couplings, finite nuclear size, recoil, radiative corrections,
  many-electron sectors, and dynamical photons.

## Edges

- `N2a/N2b/N3/N4/N4b -> N4o`: the rest module, Lorentz carrier, realization
  criterion, massive scalar shell and Clifford map construct the massive Dirac
  bridge.
- `N4c/N4i -> N4o`: the invariant Dirac pairing combines with the new time
  direction to construct the positive one-particle Hilbert space.
- `N4d/N4n -> N4o`: background, resolvent and reduction-edge contracts type the
  Coulomb observable without choosing its solver.
- `N4o -> N4p`: pass the distinguished central Hamiltonian, time involution,
  rotation multiplicities and gap spectral measure for intrinsic angular
  reduction.
- `N4o/N4p -> pre-radial reduction discovery`: pass `H_nu`, its distinguished
  domain and projector-valued target together with N4p's exact block equivalence
  and proof that the residual Clifford fiber is not a new computational principle.
- `N4o -> N4q`: pass the interacting operator, curvature obstruction, domain, and
  spectral-measure target as the global view's unsolved regression case.
- `N4o -> N4r`: pass the external electrostatic Dirac representative, its source
  and domain obligations, and its gap projector so the field/preparation origin
  and variation stability can be constructed.
- `N4o -> manuscript synthesis`: eventually replace the unsupported equation at
  lines 1383--1396 only after the remaining spectral edge is supported.

# N4p — Angular Block Decomposition and Its Computational Obstruction

Status: supported angular block decomposition, but rejected as the sought semantic
or computational reduction; it removes magnetic multiplicity while relocating the
remaining gamma calculation into a two-dimensional Clifford fiber  
Consumes: [N4o Dirac--Coulomb local graph](04o-dirac-coulomb-local-graph.md),
[N2a massive rest group](02a-spin-and-helicity.md), [N2b spin carrier](02b-lorentz-carriers.md),
[N4b Clifford construction](04b-half-integer-potential.md), and [endpoint source
contracts](../sources/computability-endpoint-contracts.md)  
Produces: an intrinsic angular Dirac operator, its `kappa` spectrum, an exact
central-Hamiltonian commutation witness, a unitary half-line block decomposition,
and a negative audit of its computational gain

## Research contract

- **Question:** does the unresolved rotation multiplicity `M_j` in N4o admit a
  further invariant split that reduces the gap spectral computation without
  importing spinor spherical components?
- **Inherited objects:** the positive Hilbert space `H_tau`, distinguished
  Coulomb Hamiltonian `H_nu`, rest group `K_tau~=SU(2)`, Clifford map `gamma`, time
  involution `B_tau`, and gap spectral measure `O_nu` constructed in N4o.
- **New construction:** orbital and spin infinitesimal rotation actions, their
  Casimirs, the angular operator `A`, the conserved operator `K=B_tau A`, and the
  polar unitary map.
- **Output:** for each nonzero integer `kappa`, one half-line first-order operator
  `h_(nu,kappa)` and an exact direct-sum recovery map for `O_nu`.
- **Boundary:** this node does not compute the spectrum of `h_(nu,kappa)`, prove
  equality of the `+kappa` and `-kappa` spectra, or reduce the residual Clifford
  computation. Calling the last step coordinate-free does not make it a new
  calculational principle.

## 1. The unresolved multiplicity is produced by two rotation actions

N4o constructs the total rotation action on spatial spinors:

```text
[U(R)psi](x)=rho_Delta(R)psi(R^(-1)x).
```

Differentiate its two factors separately. The pullback of the argument constructs
the orbital action `L`; differentiation of `rho_Delta` constructs the intrinsic
spin action `S`. Their sum is the generator of the same `U`:

```text
J=L+S.
```

This is not a decomposition of the relativistic particle representation into two
independent observables. It is a decomposition of one already constructed spatial
rotation action into its action on the base point and on the carrier.

Let `C_L`, `C_S`, and `C_J` be the quadratic `SU(2)` Casimirs of these three
actions. N2a/N2b give two copies of the fundamental spin module inside `Delta`, so

```text
C_S=(3/4)I_Delta.
```

The Clebsch--Gordan decomposition of one orbital module `V_l` with the fundamental
spin module is

```text
V_l tensor V_(1/2)
 ~=V_(l+1/2) direct-sum V_(l-1/2),
```

with the negative-label summand omitted at `l=0`. This is exactly the source of
the unresolved copies of a fixed total module `V_j` in N4o: they come from

```text
l=j-1/2       or       l=j+1/2.
```

## 2. The Casimir difference constructs the angular Dirac operator

The required operator must distinguish those two origins while commuting with
total rotations. Construct it only from the actions above:

```text
A=C_J-C_L-C_S+I.
```

Because `C_J=(L+S)^2`, this is the invariant meaning of the conventional
spin--orbit expression `2 L.S+I`; the dot-product notation is not needed for the
construction.

Evaluate `A` on the same total-spin module `V_j`. For `l=j-1/2`,

```text
A
 =j(j+1)-(j-1/2)(j+1/2)-3/4+1
 =j+1/2.
```

For `l=j+1/2`,

```text
A
 =j(j+1)-(j+1/2)(j+3/2)-3/4+1
 =-(j+1/2).
```

The two branches exhaust the Clebsch--Gordan decomposition. Hence the same
calculation constructs the operator identity

```text
A^2=C_J+1/4.
```

This `A` is the intrinsic Dirac operator of the unit two-sphere, up to the sign
fixed by spatial orientation. Its spectrum is the nonzero integers; the eigenspace
with eigenvalue `a` is the total-spin module

```text
j=|a|-1/2.
```

The sphere-spectrum theorem is used only to identify the Casimir construction
with the geometric angular Dirac operator and to supply completeness. The two
eigenvalue calculations above construct the labels consumed here.

## 3. The time involution pairs the angular branches correctly

N4o constructs `B_tau=gamma(tau)`. Spatial rotations fix `tau`, so `B_tau`
commutes with `L`, `S`, and therefore `A`. Define

```text
K=B_tau A.
```

Then

```text
K^2=A^2=C_J+1/4,
```

and the allowed eigenvalues are

```text
kappa in Z without {0},
j=|kappa|-1/2.
```

Why insert `B_tau` rather than use `A` alone? The massive Hamiltonian couples the
two `B_tau` eigenspaces. A fixed `K` eigenspace pairs

```text
B_tau=+1, A=kappa
```

with

```text
B_tau=-1, A=-kappa.
```

It therefore retains both first-order radial amplitudes while removing the
magnetic module `V_j`. This pairing is constructed from the same time involution
that produced N4o's positive Hilbert form and parity action; it is not an
independent angular convention.

N4o's parity reflection preserves `L` and `S` as axial rotation generators and
commutes with `B_tau`. Hence it commutes with `K` and may be diagonalized on the
finite residual multiplicity of each `kappa` sector. The assignment of a parity
sign depends on the constant phase chosen in N4o, so `sign(kappa)` alone must not
be called an absolute parity observable.

## 4. Polar geometry computes the Hamiltonian commutator

For `x` away from the origin put

```text
r=|x|,
n=x/r,
alpha_r=B_tau gamma(n).
```

The old Clifford relation and `n` spatial compute

```text
alpha_r^2=I,
B_tau alpha_r+alpha_r B_tau=0.
```

The Euclidean spinor Gauss formula on
`Sigma without {0}=R_+ times S^2` gives the remaining angular identity

```text
A alpha_r+alpha_r A=0.
```

This is a theorem contract with exact input and output: the ambient flat Clifford
connection restricted to a unit sphere splits into radial differentiation, its
mean-curvature term, and the intrinsic sphere Dirac operator `A`. It fails in this
form for a nonspherical foliation or a connection with angular gauge curvature.

Now evaluate the candidate conserved operator on the same spinor:

```text
K alpha_r
 =B_tau A alpha_r
 =-B_tau alpha_r A
 =alpha_r B_tau A
 =alpha_r K.
```

Also `[K,B_tau]=0`, and every radial scalar multiplication commutes with `K`.
These are the complete algebraic witnesses needed for `[K,H_nu]=0` after the
polar formula below; no gamma-matrix entries are used.

## 5. The polar unitary map exposes the residual operator

Spatial measure separates as `dx=r^2 dr dOmega`. Therefore

```text
[W psi](r,n)=r psi(rn)
```

is unitary from `L2(Sigma,Delta)` to
`L2(R_+,dr) tensor L2(S^2,Delta)`, because both norms evaluate to

```text
integral_(R_+) integral_(S^2) |r psi(rn)|^2 dOmega dr.
```

The same spinor Gauss formula, with the factor `r` absorbing the mean-curvature
term, computes N4o's kinetic operator as

```text
W[-i B_tau slash nabla_Sigma]W^(-1)
 =-i alpha_r(partial_r-A/r).
```

Substitute `A=B_tau K`. On the `K=kappa` eigenspace,

```text
-i alpha_r(partial_r-A/r)
 =-i alpha_r(partial_r-B_tau kappa/r).
```

Both `B_tau` and `alpha_r` commute with the total rotation action and preserve
the `K=kappa` space. After one equivariant identification of its finite angular
multiplicity, Schur's lemma makes them two constant operations `b` and `a` on a
two-dimensional residual fiber, satisfying

```text
a^2=b^2=I,
ab+ba=0.
```

Thus the actual residual operator is constructed as

```text
h_(nu,kappa)
 =-i a(partial_r-b kappa/r)+m b-nu/r
```

on `L2(R_+,dr;C^2)`, with the radial domain induced from N4o's distinguished
three-dimensional extension. The symbols `a,b` encode two invariant involutions,
but this notation does not remove the old matrix content. Their relations present
the complex Clifford algebra

```text
Cl_2(C)=<a,b | a^2=b^2=I, ab+ba=0> ~= M_2(C).
```

Consequently every irreducible two-dimensional realization of this pair is
unitarily equivalent to a Pauli pair, hence to the corresponding gamma-matrix
subblock. The construction has hidden the entries, not eliminated the object or
its computation.

The source contract confirms that spherically symmetric Dirac--Coulomb operators
reduce to precisely this class of half-line operators and that their closed
realizations depend on the singular endpoint. It does not replace the construction
above or license an arbitrary boundary condition.

## 6. Observable recovery proves equivalence, not computational reduction

The angular and polar maps combine into one unitary transformation `U_ang`. The
Hilbert space and distinguished Hamiltonian become

```text
U_ang H_tau
 ~=Hilbert-direct-sum_(kappa in Z without {0})
     V_(|kappa|-1/2) tensor L2(R_+,dr;C^2),

U_ang H_nu U_ang^(-1)
 =Hilbert-direct-sum_(kappa in Z without {0})
     I_(V_(|kappa|-1/2)) tensor h_(nu,kappa).
```

Functional calculus now recovers the exact N4o observable. For every Borel set
`B subset (-m,m)`,

```text
U_ang E_(H_nu)(B) U_ang^(-1)
 =Hilbert-direct-sum_(kappa in Z without {0})
    I_(V_(|kappa|-1/2)) tensor E_(h_(nu,kappa))(B).
```

Therefore each channel eigenvalue has at least the magnetic degeneracy

```text
dim V_(|kappa|-1/2)=2|kappa|.
```

No equality between the `+kappa` and `-kappa` channel spectra has been used. Such
an equality, if claimed, requires a separately constructed Coulomb-specific
intertwiner.

The edge has one bounded gain:

```text
three-dimensional operator with magnetic duplication
  -> magnetic modules V_j factored out
  -> exact direct-sum recovery of the original spectral measure.
```

It does not quotient a physical degree of freedom in the residual `C^2`, derive an
energy relation, or decrease the Clifford calculation there. Moreover, the polar
map explicitly selects `r=|x|`, `n=x/r`, and the foliation by spheres. It is
rotation-adapted and invariantly expressible, but it is still a coordinate
separation. Exact recovery establishes unitary equivalence; it does not establish
that the whole route is simpler.

## 7. A coordinate-free obstruction explains why the old problem returns

The failure is not caused only by a poor choice of notation. N4o's rotation
representation has the abstract isotypic form

```text
H_tau ~= Hilbert-direct-sum_j V_j tensor M_j,
```

where `V_j` is the irreducible magnetic module and `M_j` is its unresolved
multiplicity space. Let `E_H(B)` be any spectral projector of a self-adjoint
rotation-invariant Hamiltonian. Its block from `V_j tensor M_j` to
`V_k tensor M_k` intertwines the rotation actions. Schur's theorem computes

```text
j != k:  E_H(B)_(k,j)=0,
j = k:   E_H(B)_(j,j)=I_(V_j) tensor e_j(B),
```

for an otherwise unrestricted projector `e_j(B)` on `M_j`. Conversely, any
projector-valued measures `e_j` define a rotation-invariant spectral measure by
the displayed direct sum. Therefore rotation symmetry determines the magnetic
degeneracy and nothing about the spectral measure on `M_j`.

The `kappa` construction only refines `M_j` into invariant blocks. Inside the
residual block, `a,b` generate all of `M_2(C)`. Hence the symmetry commutant still
contains the full two-dimensional Clifford dynamics:

```text
rotation data
  -> I_(V_j) tensor arbitrary multiplicity dynamics,
kappa refinement
  -> I_(V_j) tensor radial Cl_2(C) dynamics.
```

This is the precise obstruction. Manifest group representation can classify and
remove degeneracy, but it cannot determine the Coulomb energy relation. Any
further gain must consume additional dynamical structure, not another basis for
the same rotation representation.

## 8. Failure audit against the intended research philosophy

The previous version called the path below two semantic reductions:

```text
N4o: total rotations remove magnetic multiplicity,
N4p: angular Clifford geometry selects kappa blocks,
result: the conventional singular radial Dirac operator in abstract notation.
```

Only the first arrow certainly lowers computational multiplicity. The second
chooses a symmetry-adapted basis and rewrites the gamma subblock as `a,b`. It is a
valid representation-theoretic decomposition and a useful regression check, but
it repeats the orthodox radial path and fails the stronger goal of semantic and
computational reduction.

The planned continuation into radial endpoint analysis is therefore withdrawn as
the default frontier. The research returns locally to discovery *before* that
coordinate split: seek a relation among the constructed Hamiltonian, observables,
and background geometry that determines or constrains the gap spectral measure.
A candidate relation earns continuation only if its construction and observable
recovery cost less than the radial Clifford problem; otherwise it is another
relocation of the same work.

## Checks and open boundary

Supported checks:

- `A` is constructed from the same orbital, spin and total actions that produced
  N4o's `SU(2)` reduction;
- its two eigenvalues are computed from Casimirs on the two exhaustive
  Clebsch--Gordan branches;
- `K^2=C_J+1/4` recovers `j=|kappa|-1/2` without angular components;
- `K` uses the same `B_tau` as N4o's Hilbert and parity constructions;
- the polar map is unitary by direct norm evaluation;
- the Clifford/Gauss anticommutations compute `[K,H_nu]=0`;
- the half-line blocks have an exact spectral-measure recovery map;
- Schur's theorem on the bounded spectral projectors proves that rotations leave
  the multiplicity spectral measures arbitrary;
- the singular endpoint domain is retained rather than solved formally first.

Negative check:

- `a,b` generate `M_2(C)`, so the residual system is the old gamma subblock up to
  unitary equivalence;
- the polar map uses a radial coordinate and sphere foliation;
- no energy, projector, or shorter residual computation is produced.

Open:

- a pre-radial semantic relation that constrains `E_(H_nu)` without choosing a
  gamma subblock;
- a construction or obstruction theorem for such a relation from the Coulomb
  background and the prior representation objects;
- explicit characterization and computation of radial channels only as a
  fallback or independent check, not as the presumed next theory path;
- finite nuclear size, nonspherical backgrounds and dynamical photons.

## Edges

- `N2a/N2b/N4b/N4o -> N4p`: the rest action, spin carrier, Clifford map, static
  Hilbert space and distinguished Hamiltonian construct `A`, `K`, and the polar
  reduction.
- `N4p -> pre-radial reduction discovery`: pass the exact magnetic decomposition
  together with the obstruction `Cl_2(C)~=M_2(C)` showing why its residual fiber
  is not a new computational principle.
- `N4p -> N4q`: pass the Schur-commutant insufficiency theorem and residual
  Clifford obstruction as the negative regression case for semantic compression.
- `N4p -> N7`: pass the precise strength of the reduction—unitary spectral
  equivalence, not an analytic solution or hidden-symmetry claim.

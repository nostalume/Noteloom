# N4n — Adaptive Observable Reduction Without a Universal Solver

Status: local discovery supported across five contrasting mechanisms; no universal
reducer is claimed; N4o supplies the relativistic Coulomb operator graph while
N4p shows that its intrinsic angular/half-line split is only a block equivalence,
not the sought computational reduction  
Consumes: [N4d computation interface](04d-computation-interface.md),
[computability endpoint audit](../results/05-computability-endpoint-audit.md), and
[algebraic-spectrum contracts](../sources/algebraic-spectrum-contracts.md)  
Produces: an open reduction-graph audit and composition contract; no catalogue
for discovering transformations is claimed

## Research contract

- **Question:** what can remain common when bound and scattering observables admit
  incompatible reduction mechanisms, and why do mechanical bound-state methods
  and field-theoretic scattering methods appear separated?
- **Presumptions:** one closed dynamics with a declared domain; observables act on
  a common invariant core; an asymptotic reference is additional data for
  scattering; fixed-particle mechanics is treated as a selected sector rather than
  a rival fundamental theory.
- **Output:** open-graph edge contracts, contrasting construction witnesses, an
  exact Coulomb probe, and an exact sector-elimination identity connecting
  mechanical and field descriptions.
- **Boundary:** the Coulomb calculation below is nonrelativistic. N4o separately
  constructs the massive parity-paired Dirac carrier, external connection,
  distinguished-domain contract and manifest rotation reduction. N4p constructs
  its exact `kappa`-channel block equivalence but proves that the residual
  `Cl_2(C)` fiber is the old gamma subblock up to basis change. A pre-radial
  semantic reduction, channel spectral computation and a field-theoretic QED
  kernel remain open.

## 1. One candidate edge: manifest symmetry and a bounded hidden-algebra probe

Let `H` be the constructed self-adjoint dynamics. The action or covariance
construction supplies its **manifest** symmetry operators and Noether quantities.
Those are reusable inputs. A hidden integral is not.

On a common invariant core define

```text
ad_H(A)=HA-AH.
```

The full commutant can be named as

```text
C_H=ker ad_H,
```

the algebra of domain-preserving conserved observables. This definition is not an
algorithm. It contains every `f(H)`, and finding it can already require the full
spectrum.

An admissible hidden-symmetry search must first declare a finite budget

```text
B=(tensor type, differential order, coefficient class, locality, domain).
```

It constructs a low-complexity semantic class `A_B`—for example natural
differential or polynomial observables of bounded order with coefficients in a
finite derivative-stable function family—and computes

```text
C_H^B=ker(ad_H restricted to A_B).
```

Increase `B` only when an unexplained degeneracy, transition or geometric structure
justifies the added cost. Stop when the search cost exceeds the residual spectral
computation it was meant to remove. Failure proves only `C_H^B=0`; it does not prove
that `H` has no hidden integral. This keeps the search finite and makes its boundary
explicit. A **degeneracy algebra**
lies in this kernel and acts within one energy; a **spectrum-generating algebra**
may instead have controlled nonzero commutators with `H` and move between energy
sectors. An **asymptotic algebra** acts on incoming/outgoing continuum fibers.
Their observable contracts are different.

If a closed algebra `g` acts on a spectral sector and operator identities give

```text
H=f(C_1,...,C_r)
```

for its Casimirs, then a unitary irreducible label `lambda` computes

```text
E_lambda=f(c_1(lambda),...,c_r(lambda)).
```

This is genuinely algebraic only if all four operations are supplied:

```text
construct conserved generators
  -> verify closure on the declared domain
  -> evaluate the Casimir identities on the same sector
  -> classify the admissible unitary representations.
```

If rotations are the whole computed commutant, their labels determine angular
degeneracy but not energy. The remaining multiplicity operator then owns the
spectral work. It may be radial for a central one-body problem, but it may instead
be a finite matrix, an integral kernel, a graph Hamiltonian or a numerical
variational problem. “Radial” is therefore one residual representation, not the
universal reduction principle.

### Discovery from already computed bound states

When the algebra is unknown but approximate spectral projectors `P_E` are
available, use them as discovery material. For each candidate `A in A_B`, compute

```text
(I-P_E) A P_E
```

to test whether `A` preserves the eigenspace. To search for an energy-moving
generator from `E` to `E'`, compute both composites on `P_E H`:

```text
[H,A]P_E
  =HAP_E-AHP_E,

(E'-E)AP_E.
```

Their coincidence is a finite-sector witness. Projected commutators can then
suggest structure constants. But the discovered algebra becomes supported only
after those operator identities are lifted from the sampled projectors and
verified on a common invariant domain. Numerical degeneracy alone may be accidental
or symmetry-broken outside the sample.

## 2. A bounded search constructs the Coulomb vector

Do not begin by naming the Runge--Lenz operator. Start with a central classical
dynamics

```text
H_V=p^2/(2mu)+V(r),
L=x cross p.
```

Manifest rotations compute `dL/dt=0`. Declare one small hidden-vector budget:
rotational vector type, momentum degree at most two, perpendicular to `L`, and one
undetermined radial coefficient. Its minimal ansatz is

```text
A_g=p cross L+g(r)x.
```

Hamilton's equations construct

```text
dx/dt=p/mu,
dp/dt=-V'(r)x/r,
dL/dt=0.
```

Evaluate `dA_g/dt` on the same phase-space point. The vector triple-product identity
keeps the calculation invariant:

```text
dA_g/dt
  =[rV'(r)+g(r)/mu]p
   +[g'(r)/mu-V'(r)](x dot p)x/r.
```

For generic `x,p`, the two displayed vector directions vary independently.
Conservation within this ansatz therefore computes

```text
g=-mu rV',
g'=mu V'.
```

Differentiate the first equation and substitute the second:

```text
rV''+2V'=0
  iff (r^2V')'=0
  iff V(r)=-kappa/r+V_0,

g(r)=-mu kappa/r.
```

Thus the search constructs the Coulomb potential and its extra vector together;
it did not recover a universal generator from an arbitrary equation. The
[bounded regression](../computation/04n-algebraic-spectrum-bridge/README.md) checks
power laws and rejects oscillator and Yukawa potentials in this vector class. The
oscillator's known tensor integral is a reminder that rejection is ansatz-relative.

For the Coulomb result, symmetric quantization produces the candidate

```text
A=(p cross L-L cross p)/(2mu)-kappa x/r.
```

Evaluating its commutators and quadratic products on a common invariant core gives

```text
[H,L_i]=[H,A_i]=0,
[L_i,L_j]=i hbar epsilon_ijk L_k,
[L_i,A_j]=i hbar epsilon_ijk A_k,
[A_i,A_j]=-(2 i hbar H/mu) epsilon_ijk L_k,

L dot A=A dot L=0,
A^2=kappa^2+(2H/mu)(L^2+hbar^2).
```

These identities validate the quantum lift. They do not supply an algorithm for
finding a higher-order or nonlocal integral outside the declared budget.

The energy sign is now an internal algebraic input, not an imposed difference
between two theories. On an eigenspace with `E<0`, construct

```text
M=sqrt(-mu/(2E)) A,
J_+=(L+M)/2,
J_-=(L-M)/2.
```

Substitution into the commutators computes two commuting `su(2)` algebras. The
orthogonality identity computes equal Casimirs:

```text
J_+^2=J_-^2=hbar^2 j(j+1).
```

Evaluate the quadratic identity on the same energy eigenspace:

```text
L^2+M^2
  =-mu kappa^2/(2E)-hbar^2
  =4 hbar^2 j(j+1).
```

Since a unitary `SU(2)` representation has `2j+1=n` with positive integer `n`,

```text
E_n=-mu kappa^2/(2 hbar^2 n^2).
```

No radial wavefunction was solved. The computation works because the hidden
algebra is compact, the representation is finite-dimensional, and `H` is recovered
from its Casimir. It is an exceptional closure, not a property of central
potentials in general.

The output is exactly the energy set and its algebraic degeneracy. It does not yet
compute a position-space density, a transition matrix element, a perturbative
splitting or a radiative correction. Those require either a constructed
realization and reduced matrix elements or a larger spectrum-generating algebra
with an observable recovery map. “The algebra solves hydrogen” is therefore true
for a named observable, not for every prediction about the atom.

## 3. Scattering is the same algebra with different completion data

On an energy sector `E>0`, instead construct

```text
N=sqrt(mu/(2E)) A.
```

The same commutator now evaluates to

```text
[N_i,N_j]=-i hbar epsilon_ijk L_k,
```

so `(L,N)` closes as noncompact `so(3,1)`. Its unitary representations carry
continuous parameters; admissibility therefore does not quantize `E` as the
compact `so(4)` sector did.

More importantly, a bound state is intrinsic to `H`, while scattering compares
two dynamics. Given a reference `H_0` and declared asymptotic identifications
`J_pm(t)`, construct

```text
Omega_pm=strong-limit_(t->plus-or-minus infinity)
         exp(i t H) J_pm(t) exp(-i t H_0),

S=Omega_+^dagger Omega_-.
```

The limit, not the formal group label, constructs incoming and outgoing states.
For short-range interactions `J_pm(t)` may be the identity; Coulomb is long range
and requires modified asymptotics. When a noncompact dynamical algebra is tied to
the Hamiltonian, `S` can reduce to an intertwiner between its incoming and outgoing
representations. But the asymptotic identification, normalization and analytic
boundary value remain necessary inputs.

Thus the large practical difference is exact:

| Bound sector | Scattering sector |
| --- | --- |
| point spectral subspace of one `H` | comparison of `H` with `H_0` |
| normalizable vectors | generalized continuum fibers or wave packets |
| compact hidden algebra may discretize labels | noncompact algebra has continuous labels |
| eigenvalue and residue | channel intertwiner, phase and flux normalization |
| no time-infinity comparison | existence/completeness of asymptotic limits |

This table states the ordinary point/absolutely-continuous split. Embedded
eigenvalues, thresholds and singular-continuous spectrum are explicit failure
boundaries of the simple dichotomy, not new permission to identify every
non-normalizable solution with a scattering state.

## 4. One resolvent contains both spectral regimes

For `z` off the spectrum construct

```text
R(z)=(z-H)^(-1).
```

On any test vector `f`, the scalar transform

```text
m_f(z)=<f,R(z)f>
```

has two different boundary behaviors. If `E_b` is an isolated eigenvalue,

```text
Res_(z=E_b) R(z)=P_b,
```

which returns its spectral projector. On an absolutely continuous interval, the
boundary discontinuity returns the spectral density:

```text
d mu_f^ac/dE
  =(1/(2 pi i))
    [m_f(E-i0)-m_f(E+i0)].
```

The semantic object is one spectral measure. Atoms are bound states; continuous
density supplies scattering channels. The `S` matrix still requires the relational
comparison with `H_0`; it is not encoded by the list of eigenvalues alone.

## 5. Exact bridge from field theory to mechanical theory

Let the full Hilbert space split into a selected sector and its complement:

```text
I=P+Q,
psi=psi_P+psi_Q.
```

Apply `(E-H)psi=0` first with `Q`:

```text
(E-QHQ)psi_Q=QHP psi_P.
```

Where the declared `Q`-resolvent exists, this computes

```text
psi_Q=(E-QHQ)^(-1)QHP psi_P.
```

Apply the original equation with `P` and substitute that same `psi_Q`:

```text
[E-H_eff(E)]psi_P=0,

H_eff(E)
  =PHP+PHQ(E-QHQ)^(-1)QHP.
```

This Schur complement is the precise bridge. A mechanical Hamiltonian is a
selected-sector representation of the field dynamics, exact while its energy
dependence is retained. Below the first open `Q` threshold, the resolvent can
produce a closed bound-state problem. Across a threshold, its boundary values
acquire a discontinuity; eliminated channels return as scattering, decay and
generally a non-Hermitian effective operator.

The apparent separation between mechanics and field theory is therefore caused by
which sector and analytic boundary are retained:

```text
closed low-energy P sector
  -> approximately autonomous particle mechanics,

open Q channels
  -> multichannel scattering or decay,

variable particle number
  -> field/Fock sectors rather than fixed-particle mechanics.
```

It is not a fundamental separation between bound and scattering physics.

## 6. The same field kernel produces poles and scattering

Let `G_0` be the selected free two-particle propagation and `K` the constructed
interaction kernel. The response equation

```text
T=K+K G_0 T
```

computes, wherever the inverse exists,

```text
T=(I-KG_0)^(-1)K.
```

A bound-state amplitude occurs exactly when the same inverse fails:

```text
(I-KG_0)Gamma=0
  iff Gamma=K G_0 Gamma.
```

Away from a pole, a finite graph expansion may approximate `T`. A new bound-state
pole normally requires the infinite resolvent or an equivalent nonperturbative
eigenproblem; no finite truncation of

```text
K+KG_0K+KG_0KG_0K+...
```

constructs that singularity unless it was already inserted into `K`. This is why
perturbative field theory is operationally successful for many scattering
observables yet poorly organized for binding. Bethe--Salpeter, Hamiltonian,
spectral and lattice methods are alternative computations of the missing inverse,
not separate physics.

## 7. Typical examples reject a common reduction mechanism

The Coulomb probe cannot serve as a framework. Three other ordinary systems expose
different constructive handles.

### 7.1 Quadratic oscillator — normal form before algebra

For

```text
H=p^2/(2mu)+(mu omega^2/2)x^2,
```

the positive quadratic form itself constructs a compatible complex coordinate:

```text
a=sqrt(mu omega/(2hbar))x
  +i p/sqrt(2mu hbar omega).
```

Evaluate the same canonical commutator `xp-px=i hbar`:

```text
[a,a^dagger]=1,
H=hbar omega(a^dagger a+1/2).
```

The ladder algebra is an output of factorizing a quadratic normal form, not a
hidden commutant found by search. For a positive multidimensional quadratic
Hamiltonian, symplectic normal-form construction plays the same role.

### 7.2 Inverse square — algebra exists but does not finish the spectrum

For the classical model

```text
H=p^2/(2mu)+g/x^2,
D=xp/2,
K=mu x^2/2,
```

direct Poisson evaluation gives

```text
{D,H}=H,
{D,K}=-K,
{H,K}=-2D.
```

The conformal closure is immediate. Nevertheless, quantization of the singular
operator requires a self-adjoint domain; extension or renormalization data may
introduce a bound scale not determined by the formal algebra. Here algebra is easy
and observable recovery is hard.

### 7.3 Quartic oscillator — computable without hidden structure

For

```text
H_lambda=(p^2+x^2)/2+lambda x^4,
```

use the normalized Gaussian of width `alpha`. Its semantic output is a trial state,
not a guessed symmetry. Gaussian moments compute the Rayleigh quotient

```text
E_lambda(alpha)
  =alpha/4+1/(4alpha)+3lambda/(4alpha^2).
```

Stationarity gives

```text
alpha^3-alpha-6lambda=0.
```

At `lambda=1`, `alpha=2` and

```text
E_0<=E_1(2)=0.8125.
```

The min--max principle makes this a rigorous upper bound. Richer Ritz spaces trade
finite matrix cost for accuracy. No exact hidden algebra is required for the named
observable to be computable.

### 7.4 Integrable many-body models — an isospectral embedding

When a model-specific Lax pair is constructed,

```text
dL/dt=[M,L],
```

cyclicity of trace evaluates

```text
d tr(L^k)/dt
  =k tr([M,L]L^(k-1))
  =0.
```

This produces commuting-integral candidates through an isospectral matrix flow.
But finding `L`, its `r` matrix or a quantum transfer object is itself fine-tuned
model construction; it is not generated by the Coulomb ansatz or oscillator
factorization.

The [heterogeneous regression](../computation/04n-algebraic-spectrum-bridge/README.md)
checks the oscillator factorization, inverse-square brackets and quartic Gaussian
optimization independently. Their common output is not an algebra:

| System | Productive construction | What remains |
| --- | --- | --- |
| oscillator | quadratic/symplectic normal form | observable matrix elements |
| Coulomb | exceptional conserved vector and Casimir | domains and non-spectral observables |
| inverse square | conformal closure | self-adjoint extension and scale |
| quartic oscillator | variational spectral approximation | lower/error bounds and convergence cost |
| integrable many-body model | Lax/transfer construction | model discovery and solution of spectral equations |

## 8. What survives is an open reduction graph, not a method framework

The examples above only refute a mandatory algebra search. They do **not** form a
complete portfolio and cannot be promoted into a selector for future problems.
Indeed, even the gap question is undecidable on a sufficiently broad class of
local many-body Hamiltonians. This does not obstruct the restricted systems in
this note, but it rules out interpreting this node as a universal spectral
algorithm.

For one specified model `M`, observable `O_M` and tolerance `epsilon`, build a
problem-local **reduction graph**:

```text
M -------------------------------> O_M
|                                  ^
| T                                | recover
v                                  |
M_T ------------ compute --------> y_T
```

Vertices are concrete representations of the same problem or partial computed
objects. An edge `T` is a newly constructed semantic transformation; its type is
not selected from a closed catalogue. The diagram is accepted only when it
commutes exactly or carries a checked estimate

```text
d_O(recover(y_T),O_M)<=epsilon.
```

Thus factorization, algebra, separation, variational methods, Schur reduction,
asymptotics, graphs and numerical approximation are merely known edge examples.
New research may invent an edge with a different type. There is no fixed order,
permission gate or claim that every model admits one of the listed edges.

Each proposed edge records:

```text
input and validity domain,
construction of T,
equality or error witness,
recovery map from T back to O,
whole-route cost,
failure boundary and fallback.
```

Composed edges are admissible only when adjacent domains match and their equality
or error witnesses compose. Their practical gain is measured on the whole route:

```text
Gain(T;O)
  =Cost_direct(O)
   -[Cost_construct(T)+Cost_verify(T)+Cost_recover(O from T)].
```

Retain `T` only if its gain is positive, its error meets the target tolerance, or
its reusable semantic output justifies the extra construction. Otherwise compute
`O_M` directly by a controlled residual method. Candidate edges may be explored in
parallel or abandoned early; failure of one changes no permission state. The
invention of useful edges remains research and is intentionally not specified by
this audit envelope.

This grammar distinguishes four outcomes without prescribing a technique:

- **exactly computable:** the observable and recovery map are finite and verified;
- **certifiably approximable:** an algorithm returns the observable with an error
  or variational bound;
- **structurally reduced:** a smaller residual problem is produced with a proved
  semantic equivalence;
- **not yet computable:** construction, recovery, convergence or error control is
  missing.

This is deliberately not a reduction framework. It is an audit and composition
language for reductions after or while they are invented. Its value is to prevent
a beautiful representation change from being counted as reduction when discovery
or observable recovery merely hides the original computation.

## Edges and open boundary

- `N4d -> N4n`: the resolvent and observable contracts become one spectral object
  with point and continuous regimes.
- `N4c -> N4n`: the action, coupling and domain construct the model whose
  observable-preserving transformations may be explored; no transformation type
  is privileged.
- `N4n -> bound computation`: pass whichever verified construction has positive
  whole-route gain—or the direct residual problem—together with its recovery and
  error contract.
- `N4n -> scattering computation`: pass the continuous representation fibers plus
  the declared asymptotic intertwiner problem.
- `N4n -> field/mechanics comparison`: pass the exact Schur complement and its
  threshold boundary.
- `N4n -> N9a`: pass the qualitative atom/continuum unity for realization by one
  normalized prepared spectral measure.
- `N4n -> N4q`: pass the observable-relative reduction diagram, whole-route cost,
  common resolvent, sector elimination, and rejection of a universal solver for
  global synthesis.

N4o now constructs the parity-paired Dirac--Coulomb operator, its distinguished
domain contract, the curvature obstruction to free scalar factorization, and its
manifest rotation multiplicities. N4p constructs their intrinsic angular split
and exact recovery from half-line `kappa` spectral measures, then rejects it as a
computational reduction because its residual fiber is still `M_2(C)`. Open are a
pre-radial semantic relation, computation of channel measures and projectors as a
fallback, any Coulomb-specific channel
intertwiner, a modified Coulomb wave-operator construction, a checked
field-theoretic QED kernel, and quantitative complexity/error comparisons among
actually constructed transformations.

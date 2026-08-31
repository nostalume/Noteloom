# N4d — Algebraic Computation Interface of an Equivariant Field Complex

Status: algebraic pointwise contraction, massless-vector splitting obstruction, and invariant spin 0, 1, and 2 source-response checks supported here; analytic Maxwell and finite symmetric integer-spin promotions are owned by N4e/N4f  
Consumes: [N3 realization bridge](03-realization-bridge.md), [N3a massive spin one](03a-massive-spin-one.md), [N3b massless helicity one](03b-massless-helicity-one.md), [N4 local symbol extension](04-local-symbol-extension.md), [N4a bosonic potentials](04a-polynomial-complex-details.md), [N4b fermionic potentials](04b-half-integer-potential.md), and [N4c variational-completion audit](04c-action-completion-audit.md)  
Produces: a representation-independent algebraic contraction, compatibility obligations for Green distributions, and low-spin observable checks, with external-background and dynamical-response probes kept conditional

## Research contract

- **Question/capability:** when does a local field complex that realizes the correct
  little-group representation also support a reduced, verifiable computation of a
  spectrum, propagation law, or response?
- **Presumptions:** the free finite-label symbol complex and its physical
  cohomology have already been constructed; all pairings, splittings, domains,
  boundary prescriptions, gauge fixings, interactions, and approximations not
  supplied by those nodes remain additional data.
- **Material bindings:** N3 supplies the physical-fiber/cohomology coincidence;
  N3a/N3b supply the invariant vector symbols and their physical fibers;
  N4/N4a/N4b supply general finite-label symbol families; N4c identifies the
  pairing, adjoint, Noether, boundary, and source data absent from the free
  representation problem.
- **Output:** a checked pointwise contraction identity, exact compatibility
  obligations for promoting an algebraic inverse to Green distributions, typed
  low-spin observable maps, and two branch contracts that test rather than presume
  predictivity.
- **Boundary:** this node does not claim that every equivariant complex is
  Green-hyperbolic, that the low-spin rational inverses possess a common
  distributional extension, that symmetry determines a coupling, or that the
  arbitrary-spin interaction problem is solved.

## 1. Why physical cohomology does not yet compute an observable

At momentum `p`, write the free covariant realization as a finite complex

```text
... -> E^(r-1)_p --d^(r-1)_p--> E^r_p --d^r_p--> E^(r+1)_p -> ...,
```

with

```text
d^r_p d^(r-1)_p=0.
```

At the field degree, N3/N4 identify the quotient

```text
H^r(C_p)=ker d^r_p / im d^(r-1)_p
```

with the intended little-group module on the physical orbit. This answers which
covariant configurations represent the particle. It does not yet answer how a
source is solved, how boundary data propagate, or how a spectral value is
extracted.

The missing capability is to separate three kinds of input at every degree:

1. exact or gauge directions already produced from the preceding degree;
2. representatives of physical cohomology;
3. complementary directions that the equation maps onward.

A Green construction must perform this separation without changing which
cohomology class denotes the physical state.

## 2. Pointwise contraction is constructed from the complex itself

Fix one momentum `p` and abbreviate

```text
B^r=im d^(r-1)_p,
Z^r=ker d^r_p.
```

The complex identity gives `B^r subset Z^r`. Choose complements

```text
Z^r=B^r direct-sum H^r,
E^r_p=B^r direct-sum H^r direct-sum L^r.
```

Here `H^r` is a chosen representative space for the cohomology; it is not an
additional physical sector. The restriction

```text
d^r_p|_(L^r):L^r -> B^(r+1)
```

is an isomorphism. Its kernel is zero because `L^r intersect Z^r=0`. It is
surjective because `d^r_p` vanishes on `Z^r` and
`im d^r_p=B^(r+1)`, so every image already comes from `L^r`.

Construct the degree-minus-one map `h^r_p:E^r_p->E^(r-1)_p` by

```text
h^r_p|_(B^r)=(d^(r-1)_p|_(L^(r-1)))^(-1),
h^r_p|_(H^r direct-sum L^r)=0,
```

and let `Pi^r_p` project onto `H^r` along `B^r direct-sum L^r`. For a common
input

```text
e=b+q+l in B^r direct-sum H^r direct-sum L^r,
```

the two composites evaluate to

```text
d^(r-1)_p h^r_p(e)=b,
h^(r+1)_p d^r_p(e)=l.
```

Consequently,

```text
d_p h_p+h_p d_p=identity-Pi_p.
```

This is the semantic coincidence required of the contraction: the left side
removes exactly the noncohomological directions, while `Pi_p e=q` retains the
same physical cohomology class. If the complex is acyclic at `p`, then `H^r=0`
and the same computation gives

```text
d_p h_p+h_p d_p=identity.
```

Thus pointwise acyclicity implies pointwise contractibility for these
finite-dimensional carrier complexes. The construction also exposes what is not
canonical: the complements, hence `h_p` and `Pi_p`, are choices even though the
cohomology quotient is intrinsic.

## 3. Equivariance is a new obligation, not a consequence of choosing complements

For a Lorentz transformation `g`, the symbol family already obeys

```text
d_(g p) rho(g)=rho(g)d_p.
```

An equivariant contraction would additionally have to satisfy

```text
h_(g p) rho(g)=rho(g)h_p,
Pi_(g p) rho(g)=rho(g)Pi_p.
```

Arbitrary complements need not satisfy these identities. A supported family-level
construction must therefore do one of the following:

- construct invariant complements directly from the carrier decomposition;
- construct them from a nondegenerate invariant pairing and adjoints;
- prove that a local equivariant generalized inverse exists on the required
  momentum stratum;
- or record the obstruction and restrict the claim.

The massive and massless cases already behave differently.

For a massive standard momentum, the little group `K_k~=SU(2)` is compact. Starting
from any positive-definite auxiliary form on a finite carrier, normalized
bi-invariant Haar averaging constructs

```text
<u,v>_K=integral_(K_k) <rho(a)u,rho(a)v>_0 da.
```

For `b in K_k`, right invariance and the substitution `a'=a b` compute

```text
<rho(b)u,rho(b)v>_K
 =integral_(K_k) <rho(a b)u,rho(a b)v>_0 da
 =<u,v>_K.
```

Orthogonal complements of invariant subspaces are therefore invariant. At a fixed
massive momentum, the complements used in Section 2 can be chosen
`K_k`-equivariantly. If two transports to `p` obey `B'(p)=B(p)b`, then

```text
rho(B'(p))L^r=rho(B(p))rho(b)L^r=rho(B(p))L^r.
```

The transported complement is therefore independent of that residual-frame
choice. This does not yet prove a regular off-shell or analytic family, but it
removes the on-shell splitting obstruction.

The massless vector potential supplies a direct counterexample to the same move.
N3b constructs

```text
P_k=k^perp_C,
G_k=span_C(k),
H_A(k)=P_k/G_k,
```

and for a chosen screen representative `x` and null translation `N_q`,

```text
N_q x=x-(xi.x)k.
```

Assume that a `K_k`-invariant complement `E'` existed with
`P_k=G_k direct-sum E'`. Every `x' in E'` has a unique expression `x+a k` for a
screen vector `x`. Invariance would put both `N_q x'` and `x'` in `E'`, so

```text
N_q x'-x'=-(xi.x)k in E' intersect G_k={0}.
```

This would force `xi.x=0` for every screen translation `xi`, hence `x=0`. It
contradicts `E'` representing the nonzero two-dimensional quotient. Therefore the
massless vector potential has no little-group-equivariant physical complement
inside the unquotiented carrier.

This obstruction explains rather than merely tolerates gauge equivalence. A
covariant massless Green construction must act on the quotient, use curvature or
conserved-source data, or introduce a gauge choice whose auxiliary dependence is
proved to disappear from observables. General higher-spin potential complexes
must be checked separately; the vector calculation is evidence, not an automatic
all-spin theorem.

### 3.1 The intrinsic transverse quotient is constructed before it is called physical

Let `k` be a nonzero null momentum. Orthogonality constructs

```text
k^perp={v in V | eta(k,v)=0}.
```

Because `eta(k,k)=0`, the momentum line lies inside this hyperplane. It is exactly
the radical of the restricted metric. One inclusion follows from
`eta(k,k^perp)=0`. Conversely, if `v in k^perp` is orthogonal to every element of
`k^perp`, then

```text
v in (k^perp)^perp=span(k).
```

The degeneracy therefore forces the quotient

```text
Q_k=k^perp/span(k).
```

The rule

```text
eta_Q([v],[w])=eta(v,w)
```

is representative-independent because adding a multiple of `k` changes neither
pairing, and it is nondegenerate because the removed line was the whole radical.
In four-dimensional spacetime `Q_k` has dimension two. This constructed object is
the **intrinsic transverse quotient**; only after the field equation and gauge map
identify it with physical cohomology do we call it the screen.

Choosing another null vector `n` with `eta(k,n)=1` produces a concrete plane

```text
E_(k,n)={k,n}^perp
```

representing `Q_k`, but changing `n` changes that plane. The quotient does not
change, so no auxiliary screen choice belongs to the physical datum.

For the vector potential, the null equation gives `a in k^perp` and the gauge map
gives `a~a+k alpha`. Hence its physical cohomology is precisely `[a] in Q_k`.
The null-translation calculation

```text
N_q a=a-(xi.a)k
```

changes only the representative and therefore acts trivially on `[a]`; the
rotation quotient acts nontrivially and supplies helicity. For a symmetric rank-`s`
potential, the corresponding fiber is not merely `Sym^s(Q_k)^*` but its trace-free
part

```text
Sym_0^s(Q_k tensor C)^* ~= C_(+s) direct-sum C_(-s),
```

as constructed in N4a. Thus “physical screen quotient” abbreviates a completed
semantic route—null transversality, gauge quotient, induced metric, and
little-group action—not a chosen two-dimensional coordinate plane.

This is where N4c enters essentially. If a compatible adjoint `delta=d^dagger`
has been constructed, the candidate Laplacian of the complex is

```text
Delta=d delta+delta d.
```

On a domain where a generalized inverse `Delta^+` exists and commutes with the
complex maps, the candidate

```text
h=delta Delta^+
```

computes

```text
d h+h d
 =(d delta+delta d)Delta^+
 =identity-Pi_(ker Delta).
```

This equation is presently a construction contract, not a completed theorem for
the N4a/N4b families. N4c now supplies the bosonic invariant pairing and formal
adjoint, but a family-level generalized inverse, domain, and kernel/cohomology
comparison remain open; N4i supplies the fermionic pairing, adjoint, and
admissible causal response, and N4j completes its causal quotient theorem.

## 4. A symbol contraction is not yet a spacetime Green operator

The distinction already appears for the scalar denominator `q(p)`. The algebraic
function `1/q(p)` exists only for `q(p)!=0`. A distributional inverse is a
distribution `g` satisfying

```text
q g=1.
```

If `g_1` and `g_2` are two such extensions, direct subtraction computes

```text
q(g_1-g_2)=0.
```

Their difference is a homogeneous solution carried by the characteristic shell.
Retarded, advanced, Feynman, Euclidean, or state-dependent prescriptions therefore
add different causal or state semantics; they are not interchangeable names for
the same rational inverse.

The tempting Fourier prescription

```text
widehat(G f)(p)=h_p widehat(f)(p)
```

is valid only after further analytic questions are answered:

- Does `p |-> h_p` vary rationally, smoothly, or distributionally on the chosen
  stratum?
- What growth permits it to act on the selected test-function or distribution
  space?
- How is it extended across the characteristic set where cohomology appears and
  contraction fails?
- Which advanced, retarded, Feynman, Euclidean, or spectral boundary prescription
  is required by the observable?
- For a gauge complex, on which quotient or gauge-fixed complement is the inverse
  defined, and why is the final observable independent of that choice?

These data construct different analytic Green objects from the same algebraic
symbol. They must not be hidden inside the notation `d^(-1)`.

The representation carried by a pole or characteristic residue must be checked by
an explicit map back to N3's cohomology. A singular denominator alone does not
prove that its residue contains only the desired physical fiber.

### 4.1 General compatibility is a contract with possible obstructions

For a variational gauge system, type the relevant part of the complex as

```text
G --R--> F --K--> F^* --R^dagger--> G^*,
```

with `K R=0` and `R^dagger K=0`. A Green distribution is compatible with this
complex only after the following independent checks succeed:

1. **Inverse modulo gauge.** It solves the sourced equation on the admissible
   source space, possibly only up to `im R`; it is not asserted as an inverse on
   the whole redundant carrier.
2. **Typed inverse and causal identities.** One symbol can produce distinct
   distributional maps. If a gauge completion `P=d delta+delta d` has retarded or
   advanced inverses `G^+/-`, then the degree-lowering maps

   ```text
   h^+/-=delta G^+/-
   ```

   must satisfy the sourced contraction identity

   ```text
   d h^+/-+h^+/- d=identity
   ```

   on their declared source domains. Their causal difference

   ```text
   E=G^+-G^-
   ```

   instead satisfies `P E=E P=0` and maps source classes to homogeneous
   solutions. A shell projector `Pi` may be introduced only when a separate
   spectral splitting constructs it; it is not a universal synonym for `E`.
3. **Covariance of the prescription.** For every symmetry `g` preserved by the
   boundary or state choice,

   ```text
   G(g p)=rho(g)G(p)rho(g)^(-1).
   ```

   A time-oriented prescription may preserve the proper orthochronous Poincare
   group; a fixed Coulomb background preserves only its own time-translation and
   rotation subgroup.
4. **Gauge-choice independence at the observable.** Candidate representatives
   need not be equal. If their difference has the typed gauge form

   ```text
   G'-G=R X+Y R^dagger,
   ```

   then for admissible sources `R^dagger J=R^dagger J'=0`, the same source pair
   computes

   ```text
   <J,(G'-G)J'>
    =<R^dagger J,X J'>+<Y^dagger J,R^dagger J'>
    =0.
   ```

   Whether two actual gauge choices have this form is itself an obligation, not a
   general presumption.
5. **Residue/cohomology coincidence.** The pole or discontinuity must descend to
   the N3/N4 physical quotient and carry its little-group action. Equality of
   denominators is insufficient.
6. **Analytic validity.** Test-function space, operator domain, support, singular
   extension, wavefront behavior, and boundary conditions must be stated for the
   selected observable.

The current graph establishes the retarded/advanced physical admissible-source
response uniformly for every separate finite symmetric massless potential. N4e
promotes the Maxwell branch, N4f the integer-spin family, and N4i/N4j the
half-integer family;
N4g/N4h and N4k/N4l add faithful positive shell images. The
[computability endpoint audit](../results/05-computability-endpoint-audit.md)
further shows that any separately declared scalar fundamental distribution lifts
through the same identities. It does not thereby construct its state or boundary
prescription. Countable-tower, state-selected, background-spectral, and interacting
promotions remain separate research.

## 5. Observable extraction is the semantic output

The computation interface is complete for a chosen problem only when it ends in a
typed observable map. Three common outputs have different contracts:

| Output | Required construction | Semantic check |
| --- | --- | --- |
| free propagation | boundary-selected Green map on the physical quotient | propagated data retain the same cohomology class and causal support |
| bound-state spectrum | a closed background Hamiltonian and its resolvent | pole/residue equals an eigenvalue/spectral projector in the declared domain |
| response/correlator | source map, state, quantization, and renormalized generating object | gauge/Noether identities and observable independence from auxiliary choices |

Coordinates or components may enter after these invariant objects have reduced the
problem to the smallest symmetry sector. They are an execution representation,
not the construction of the theory.

For the exact finite-spin lift and the remaining distance to a spectrum, see the
[computability endpoint audit](../results/05-computability-endpoint-audit.md). Its
result is deliberately physical rather than gauge-fixed: one scalar `g_b` with
`qg_b=1` produces the integer response `g_bM_s^(-1)J` and the half-integer response
`S_ng_bM_n^(-1)J` on admissible sources. No full inverse on a redundant carrier is
claimed.

### First structural check — scalar and vector symbols

The scalar and vector realizations give a nontrivial test without invoking a
spinor or a component basis. Write

```text
q(p)=eta(p,p).
```

For a scalar of mass `m`, the symbol is multiplication by

```text
K_0(p)=m^2-q(p).
```

Away from the mass shell, its inverse is the same invariant scalar

```text
G_0(p)=1/(m^2-q(p)).
```

The inverse fails on the characteristic mass shell; its positive-energy component
is the physical orbit in the present scope. Turning this algebraic pole into a
propagator still requires one of the analytic prescriptions listed in Section 4.

For `q(p)!=0`, construct two endomorphisms of the vector carrier:

```text
L_p(v)=p eta(p,v)/q(p),
T_p=identity-L_p.
```

Direct evaluation on the same vector gives

```text
L_p^2=L_p,
T_p^2=T_p,
L_p T_p=T_p L_p=0,
im L_p=span(p),
im T_p=p^perp.
```

They are not coordinate polarization sums. They are the invariant decomposition
of the carrier into the momentum line and its orthogonal complement.

Using the massive vector symbol constructed in
[N3a](03a-massive-spin-one.md), write

```text
K_1(p)=(m^2-q(p))identity+p eta(p,-)
      =(m^2-q(p))T_p+m^2 L_p.
```

The two invariant summands diagonalize the operator. Therefore

```text
G_1(p)=T_p/(m^2-q(p))+L_p/m^2
```

for `q(p)!=0,m^2`, and multiplication computes

```text
K_1(p)G_1(p)
 =(m^2-q)T_p T_p/(m^2-q)+m^2 L_p L_p/m^2
 =T_p+L_p
 =identity.
```

Recombining the projectors removes the apparent singularity at `q(p)=0`:

```text
G_1(p)=[identity-p eta(p,-)/m^2]/(m^2-q(p)).
```

Thus the inverse extends algebraically to every momentum away from the physical
mass shell; the intermediate `L_p/T_p` split exposed the meaning of the two
sectors without introducing a false characteristic.

Only the transverse term has a mass-shell pole. Up to the scalar orientation used
for the pole variable, its residue projector is `T_p`, whose image at
`q(p)=m^2` is `p^perp`, precisely the massive spin-one fiber verified in N3a.
The longitudinal carrier direction is algebraically eliminated with no pole. This
is the required semantic bridge from the field symbol to the physical spectral
residue.

For the massless vector symbol in
[N3b](03b-massless-helicity-one.md),

```text
K_Max(p)=q(p)T_p.
```

It has no inverse on the full carrier because `L_p` is its gauge kernel. A source
coupling is gauge invariant only if its momentum-space current satisfies

```text
eta(p,j)=0,
```

so `T_p j=j`. For `q(p)!=0`, the equation `K_Max(p)a=j` then determines the gauge
class

```text
[a]=[j/q(p)].
```

An optional gauge-fixing parameter `xi!=0` gives

```text
K_xi(p)=q(p)T_p+(q(p)/xi)L_p,
G_xi(p)=T_p/q(p)+xi L_p/q(p).
```

Their product is the identity, but the physically relevant check uses two
conserved currents:

```text
eta(j,G_xi(p)j')=eta(j,j')/q(p),
```

because `L_p j'=0`. The response is independent of `xi`; gauge fixing constructed
an executable inverse without changing the conserved-source observable.

At the null pole, `j,j' in p^perp`. Replacing either current by a representative
differing by a multiple of `p` leaves `eta(j,j')` unchanged. Hence the residue
pairing descends to

```text
p^perp/span(p)=Q_p,
```

the same physical screen quotient constructed in N3b. At the algebraic level,
this verifies the route

```text
massless vector cohomology
  -> gauge-fixed rational inverse away from the shell
  -> conserved-current response
  -> intrinsic pairing of the pole numerator on the shell
```

without choosing polarization components. It also shows why a propagator itself
is not the observable: `G_xi` depends on an auxiliary choice while its admissible
source pairing does not. Turning this rational identity into a retarded, advanced,
Feynman, or other Green distribution still requires every check in Section 4.1.

### Second structural check — spin two from the completed bosonic action

For rank two, the double-trace constraint is automatic and the gauge parameter has
rank one, so its trace constraint is also automatic. Consume N4a's operators

```text
C=A-(1/2)P T,
D=q-P C,
```

and N4c's now-supported Euler data

```text
M=identity-(1/4)U T,
E=M D,
M^2=identity                 on F_2.
```

The first computation constructs an invariant gauge slice. For any rank-one
parameter `epsilon`, use `[A,P]=q` and `[T,P]=2A` to evaluate

```text
C(P epsilon)
 =A P epsilon-(1/2)P T P epsilon
 =q epsilon-(1/2)P^2 T epsilon
 =q epsilon.
```

When `q(p)!=0`, the choice

```text
epsilon=-(1/q)C phi
```

therefore sends `phi` to the gauge-equivalent representative

```text
phi_g=phi+P epsilon,
C phi_g=C phi-q(C phi)/q=0.
```

N4a already proves that `C phi` is traceless, so the construction stays inside the
admissible gauge-parameter carrier. On this gauge slice,

```text
D phi_g=q phi_g,
E phi_g=q M phi_g.
```

Now let `J` be an admissible rank-two source. Since the rank-one gauge parameter is
unconstrained by trace, gauge invariance of `<phi,J>` requires full conservation:

```text
A J=0.
```

The trace `T J` is scalar. In four dimensions, `[A,U]=2P` and
`T U=U T+4N+8` compute

```text
A(M J)=-(1/2)P T J,
T(M J)=-T J,
C(M J)=0.
```

Thus the candidate sourced solution

```text
phi_J=(1/q)M J
```

already lies in the constructed gauge slice. Evaluating the Euler operator on the
same source gives

```text
E phi_J
 =q M[(1/q)M J]
 =M^2 J
 =J.
```

The corresponding source response is therefore the invariant expression

```text
Response_2(J,J';p)=(1/q(p))<J,M J'>.
```

It is independent of a change `phi_(J')->phi_(J')+P epsilon`, because

```text
<J,P epsilon>=<A J,epsilon>=0.
```

This proves gauge independence at the observable pairing rather than asserting it
for an auxiliary propagator.

At a nonzero null momentum, conservation puts each source slot in `p^perp`, and
the radical `span(p)` disappears from the induced pairing. On the two-dimensional
screen quotient `Q_p=p^perp/span(p)`, the induced trace reversal is

```text
M_Q j=j-(1/2)metric_Q trace_Q(j),
```

which is exactly the projection onto `Sym_0^2(Q_p tensor C)^*`. Consequently the
pole numerator pairs only the trace-free screen class, the same
helicity-`+2 direct-sum -2` fiber constructed in N4a. The semantic route is

```text
spin-two field cohomology
  -> invariant gauge slice
  -> trace-reversed sourced solution
  -> conserved-source response
  -> trace-free screen residue.
```

No tensor-component expansion or polarization sum occurs. The remaining analytic
task is to choose and control a distributional boundary value for `1/q(p)`.

## 6. Interaction begins as a deformation problem

Let `C_0` denote a supported free complex. Coupling it to a background or dynamical
object is extra structure, represented schematically by

```text
d_A=d_0+V_A+higher terms.
```

Before using `d_A`, compute:

1. its covariance under the physical symmetry and any gauge transformation of
   `A`;
2. whether the deformed sequence remains a complex or acquires a curvature
   obstruction;
3. whether the action-side Noether identity survives;
4. whether the free domain and physical quotient deform coherently;
5. which new parameters and approximation assumptions entered.

Symmetry may constrain `V_A`; it does not generally select it uniquely. For higher
spin, failure of one of these computations is meaningful evidence of an
interaction obstruction rather than permission to reuse the free propagator
formally.

### Probe E — prescribed external background

For a static background that admits a Hamiltonian

```text
H_A=H_0+V_A,
R_A(z)=(z-H_A)^(-1),
```

the free and background resolvents inhabit the same operator space. Since

```text
R_0^(-1)=R_A^(-1)+V_A,
```

multiplication on the left by `R_0` and on the right by `R_A` computes

```text
R_A=R_0+R_0 V_A R_A.
```

This algebraic resolvent identity is the precise conditional edge from a chosen
free resolvent to a background spectral problem. It becomes an operator or Green
identity only on a common domain where both resolvents exist. A Coulomb source in
the spin-`1/2` branch is one possible test, but it cannot consume the present
massive chiral Klein--Gordon carrier directly.
[N4o](04o-dirac-coulomb-local-graph.md) now constructs a parity-paired first-order
Dirac carrier from the prior Clifford map, adds its `U(1)` connection and static
Coulomb input, computes the curvature obstruction to scalar factorization, and
binds the distinguished self-adjoint-domain theorem. [N4n](04n-algebraic-spectrum-bridge.md)
then audits its problem-local reduction graph. Factorization, normal form, algebraic
closure, variational bounds, Schur/resolvent maps and direct spectral computation
are independent candidate edges, not a prescribed portfolio. Each constructed
edge must expose an equality or error witness, recover the named observable, and
reduce the whole-route cost. N4n's Coulomb vector and quartic variational bound are
contrasting witnesses; neither is a default for the Dirac problem. Failure of one
edge rejects only that construction and must not block another edge or the direct
residual computation. Residual rotations may produce radial spaces
`L2((0,infinity),dr;C^2)`, but only when that representation lowers the remaining
cost. A bound state is a discrete gap eigenvalue detected by a resolvent pole or
an equivalent checked spectral condition. The Coulomb formula is one terminal
regression, not the universal definition of the interface.

### Probe D — dynamical response

If `A` is dynamical, the branch additionally needs an action, state or vacuum,
measure/quantization rule, regulator, and renormalization conditions. A
renormalized effective object `Gamma[A]`, when constructed, produces its quadratic
response by the typed Hessian

```text
Pi=delta^2 Gamma[A]/(delta A delta A)|_(A=0).
```

A graph expansion is one computation of this derivative. Its propagator lines and
vertices must be traced back to the inverse quadratic operator and the derivatives
of the coupled action. Graph reduction, invariant tensor structure, and Ward or
Noether identities precede any component integral.

Vacuum polarization in a charged spin-`1/2` branch is therefore a probe of this
contract, not an output of free representation theory.

## 7. Philosophy alignment is operational

| Research principle | Obligation in this node |
| --- | --- |
| internal construction | `h_p` is built from exact, cohomology, and complement directions; distributional Green data require a separate construction rather than an unnamed inverse |
| semantic invariance | `Pi_p` retains precisely the physical cohomology passed from N3/N4 |
| computation reduction | quotient and invariant carrier decomposition precede coordinates, partial waves, or graph integrals |
| reflective intuitionism | failure of contraction, covariance, deformation, or analytic continuation exposes a hidden presumption and may reconstruct the theory view |
| construction over formal closure | success requires a spectrum, propagation law, or response with checks, not merely a formally covariant equation |

The practical thesis under test is therefore bounded:

> A symmetry-derived field complex becomes predictively useful only when its
> physical cohomology can be connected, through explicitly added analytic and
> dynamical data, to a reduced observable computation.

This statement neither reduces dynamics to symmetry nor abandons the
representation spine. It locates exactly where new physical input enters.

## 8. Checks, edges, and open boundary

### Supported here

- the fixed-momentum decomposition and contraction identity
  `d h+h d=identity-Pi`;
- invariant complements for finite massive fibers by compact little-group
  averaging, together with the exact massless-vector obstruction to an invariant
  complement inside the potential carrier;
- the distinction among physical cohomology, algebraic contraction, analytic Green
  data, and observable extraction;
- the algebraic resolvent identity conditionally relating free and background
  spectral problems on a common resolvent domain;
- the uniform physical lift of any declared scalar wave fundamental distribution
  to every separate finite symmetric massless integer- and half-integer-spin
  admissible-source response, as recorded in the endpoint audit;
- the scalar, massive-vector, and massless-vector invariant inverse calculations,
  including the massive spin-one pole projector and Maxwell gauge-parameter
  cancellation on conserved sources;
- the rank-two invariant gauge slice, sourced inverse, gauge-independent response,
  and identification of its pole numerator with the trace-free screen fiber;
- the classification of external-background and dynamical-response examples as
  conditional probes rather than universal consequences.

### Required checks beyond the N4e/N4f promotions

- consume [N4i](04i-half-integer-green-construction.md) and
  [N4j](04j-half-integer-causal-quotient.md), which now construct the
  half-integer pairing, formal adjoint, Green response, and causal quotient
  without component matrices; consume
  [N4k](04k-half-integer-positive-frequency.md), which constructs its positive
  particle/antiparticle completion, and
  [N4l](04l-half-integer-support-faithfulness.md), which proves gauge-rank
  faithfulness; N4z discharges CAR normalization, while density remains open;
- consume [N4g](04g-positive-frequency-completion.md), which now adds
  positive-frequency data, proves positivity on the compact-source image, and
  induces the N3 little-group action; then discharge its full-space density
  contract;
- construct a topology, common domain, and uniform estimates before treating the
  separate finite-spin Green family as one countable carrier;
- state the function spaces, domains, singular extension, and boundary prescription
  for every analytic Green claim;
- consume N4o's parity-paired massive Dirac background operator, distinguished
  domain and gap spectral-measure target together with N4p's exact magnetic block
  decomposition and residual-Clifford obstruction; search first for a pre-radial
  semantic relation, and use channel domains or direct residual computation only
  as a fallback when no transformation earns its whole-route cost before claiming
  a hydrogenic gap spectrum;
- for each interaction probe, verify the deformed covariance/Noether identity and
  return an observable with a convergence or validity statement.

### Edges

- `N3/N4 -> N4d`: the exact physical cohomology and its little-group
  identification are the semantic content that `Pi_p` must preserve.
- `N4a/N4b -> N4d`: their polynomial symbol complexes are the finite-spin test
  families; Clifford multiplication remains only the half-integer branch tool.
- `N4c -> N4d`: pairings, adjoints, domains, Noether identities, and admissible
  sources are prerequisites for analytic inversion and response.
- `N4d -> N4e`: the typed inverse/causal distinction and six compatibility
  obligations are executed for the Maxwell complex.
- `N4d -> N4f`: the same obligations are executed for every separate finite
  symmetric integer-spin complex after the spin-two test.
- `N4d -> N4n`: the resolvent and observable contracts feed an adaptive audit of
  heterogeneous reductions for bound poles and continuum scattering data; no
  solver is prescribed.
- `N4d -> N4o`: the background-deformation and resolvent contracts type the
  externally coupled Dirac Hamiltonian and its gap spectral measure.
- `N4d/N4o -> N4p`: the typed central Hamiltonian and spectral measure are block
  diagonalized by angular Clifford geometry; N4p records why this does not reduce
  the residual gamma computation.
- `N4d -> N7`: contraction, analytic, deformation, and observable data distinguish
  physical-fiber, local-Euler, and source-response equivalence.
- `N4d -> Probe E/Probe D`: only a separately constructed free Green object and a
  verified deformation contract may pass forward; neither interaction is inferred
  from symmetry.

### Open boundary

Pointwise contraction does not imply a globally equivariant or analytically useful
family. The countable-spin tower additionally requires a topology, common dense
domain, convergence control, and uniform estimates; a formal direct sum supplies
none of them. Interaction consistency may fail for some finite spins before that
completion question is reached.

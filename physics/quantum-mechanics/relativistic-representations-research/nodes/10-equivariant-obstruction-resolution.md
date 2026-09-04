# N10 — Equivariant Obstruction Resolution as a Local-Field Constructor

Status: developing; the integer and half-integer symmetric-potential families are
regenerated from their gauge/carrier residuals, their minimal equation layers are
classified within declared truncations, and their smallest compensator enlargements
are quotient-equivalent but costlier; the retained bosonic constructor now reaches
a generated physical-source adapter, spin-two causal use, and a quadratic Euler
operator, carrier-derived grammars, and a bounded capability-relative presentation
frontier; the missing integer-spin curvature output is generated at minimal degree,
reaches a causal physical-source consumer, and has a compatible direct-source
complex, while native direct-source physics, carrier-global minimality, and novelty
remain open  
Consumes: [N1 determination boundary](01-determination-boundary.md),
[N2 representation spaces](02-three-representation-spaces.md),
[N2a physical fibers](02a-spin-and-helicity.md),
[N3 orbitwise realization](03-realization-bridge.md),
[N4a polynomial complexes](04a-polynomial-complex-details.md),
[N4b half-integer potentials](04b-half-integer-potential.md), and
[N4m integer-spin field machine](04m-finite-integer-spin-field-machine.md)  
Source comparison: [obstruction-resolution contracts](../sources/obstruction-resolution-contracts.md)  
Produces: a candidate generative spine for the free-field paper, a typed
equivariant symbol-resolution calculus, obstruction-generated integer and
half-integer benchmarks, and exact obligations for a minimality theorem

## Research contract

- **Defect:** the current free-field paper begins with already selected orbit,
  carrier, symbol, complex, and completion machinery. It verifies that these
  objects recover the desired representation, but often does not construct why
  those objects—and not simpler candidates—must appear.
- **Question:** can a particle representation be turned into a local field system
  by repeatedly calculating the obstruction to the cheapest current candidate,
  rather than by guessing a known equation and checking it afterward?
- **Invariant target:** the same massive-spin or massless-helicity little-group
  fiber throughout orbit transport, polynomial extension, gauge quotient, and
  characteristic audit.
- **Capability:** construct a finite local covariant presentation and expose its
  trade among differential order, carrier content, gauge depth, characteristic
  debt, and recovery depth.
- **Internal benchmark:** regenerate the symmetric massless integer-spin potential
  equation from the failure of the scalar wave symbol on a gradient gauge change;
  recover N4a's shell cohomology; state exactly which choice remains unforced.
- **Research horizon:** four-dimensional Minkowski space, constant-coefficient
  free linear systems, finite Lorentz carriers, bounded polynomial degree, and
  separate finite spins. No curved deformation, interaction, infinite tower,
  observable prediction, or manuscript rewrite belongs to this bench.

This node reopens a local discovery region inside the otherwise supported free
baseline. Existing equations remain evidence. They no longer determine the order
of explanation.

## 1. Representation data arise from transport obstructions

The construction should not begin with the phrase “choose a Poincare
representation.” Its kinematic prefix is already available in N2/N2a:

```text
repeatable spacetime motion of states
  -> strongly continuous translations
  -> their joint spectral momentum
  -> Lorentz covariance transports spectral support
  -> an irreducible positive-energy sector lies on one orbit O
  -> transporting one standard momentum k to p is nonunique
  -> the relative transport fixes k
  -> its action on the standard fiber is the little-group representation sigma.
```

The residual-frame object is computed. If `B(p)k=p` and `B'(p)k=p`, then

```text
r(p)=B(p)^(-1)B'(p),
r(p)k=B(p)^(-1)B'(p)k=B(p)^(-1)p=k.
```

Thus `r(p)` lies in `K_k`; `K_k` is not imported vocabulary but the ambiguity of
representing the same momentum by a frame. The physical fiber `V_sigma` stores
how the state changes under precisely this unavoidable ambiguity.

This kinematic construction stops at an orbit bundle. A local field has a
different capability: finitely many spacetime components related by finite-order
differential operators. The mismatch between these two descriptions constructs
the next problem.

## 2. The local-realization problem

Let

```text
A=Sym(M_C^*)
```

be the polynomial algebra on complexified momentum space. A constant-coefficient
local differential operator is represented by an equivariant polynomial symbol.
For finite Lorentz carriers `C^a`, construct free `A`-modules

```text
F^a=A tensor C^a
```

and polynomial differentials

```text
... -> F^(-1) --delta^(-1)--> F^0
    --delta^0--> F^1 -> ...,

delta^(a+1) delta^a=0.                         (2.1)
```

Evaluation at momentum `p` produces a finite carrier complex. Its physical
amplitude is

```text
H^0_p(F)=ker delta^0(p)/im delta^(-1)(p).       (2.2)
```

A realization of `(O,sigma)` must construct a `K_k`-equivariant isomorphism

```text
H^0_k(F) ~= V_sigma                             (2.3)
```

and transport it over `O`. It must also account for every other momentum stratum
where `H^0_p(F)` is nonzero. Equations (2.1)--(2.3) define a **local realization
complex**. Calling it a free resolution of one global algebraic module requires
additional support and coherence hypotheses; this node does not conceal those
hypotheses inside the name “resolution.”

## 3. Construct by residuals, not by completed equations

For fixed carriers and degree bounds, the constructor has five obstruction
operations.

### 3.1 Fiber obstruction

Restrict the candidate carriers to `K_k`. If no complex of restricted carriers
has cohomology `V_sigma`, then the carrier choice cannot express the particle even
before locality is imposed. A missing physical subspace may force a quotient,
auxiliary carrier, parity completion, or a different carrier.

### 3.2 Polynomial-lift obstruction

For carriers `X,Y`, construct the finite space

```text
P_<=d(X,Y)
 =direct-sum_(r=0)^d Hom_L(Sym^r(M_C) tensor X,Y).       (3.1)
```

Evaluation at `k` gives

```text
ev_k:P_<=d(X,Y)->Hom_(K_k)(X,Y).                        (3.2)
```

A required fiber map `a_k` is local at degree `d` only when its cokernel class
vanishes. Orbit transport can construct a smooth map while (3.2) still has no
polynomial preimage.

### 3.3 Complex obstruction

Individually lifted maps need not compose to zero. On a common input compute

```text
R_a(p)=delta^(a+1)(p)delta^a(p).                        (3.3)
```

The nonzero equivariant polynomial `R_a` is the residual that must be removed.
One may change coefficients, add a carrier through which it factors, restrict a
domain, or reject the candidate. The resolution is the record of these forced
repairs. The correction is not unique until a cost or capability is declared.

### 3.4 Characteristic obstruction

After (2.1) holds, compute the ranks of adjacent symbols. The determinantal loci

```text
dim H^a_p
 =dim C^a-rank delta^(a-1)(p)-rank delta^a(p)            (3.4)
```

expose unwanted shells and singular strata. A complex that works at `k` but
creates unexplained cohomology elsewhere has not solved the local realization
problem.

### 3.5 Capability obstruction

A representation-correct complex need not possess an invariant action, Green
response, positive physical norm, or stable deformation. Each stronger capability
adds a new failed equality: formal-adjoint mismatch, noninvertible gauge symbol,
indefinite carrier pairing, or curvature breaking `delta^2=0`. Those are later
extensions of the same obstruction discipline, not automatic consequences of
(2.3).

The resulting tool is therefore

```text
fiber target
  -> finite equivariant candidate space
  -> calculate lift residuals
  -> calculate composition residuals
  -> calculate characteristic residuals
  -> retain the nondominated supported complexes.        (3.5)
```

For fixed carriers and degree bounds every step in (3.5) is finite. The prior
search over all carriers and orders is not finite and is not claimed to be a
universal compiler.

## 4. Representation multiplicities replace component ansatzes

Equation (3.1) is the computational core. Decompose each tensor product into
irreducible Lorentz modules. Schur's lemma then replaces a covariant tensor ansatz
by maps between finite multiplicity spaces. In a multiplicity-free summand, an
operator contributes one scalar coefficient rather than an array of components.

Choose bases `e_i^a` for the relevant invariant-map spaces and write

```text
delta^a(p)=sum_i c_i^a e_i^a(p).                         (4.1)
```

Evaluation constraints are linear equations in `c_i^a`; the complex relations are
finite quadratic equations; characteristic strata are determinantal ideals. The
semantic object remains the equivariant map, while coordinates occur only on its
small multiplicity space.

This supplies a real computational claim only after the invariant-map basis has
been constructed and compared with the component route. N4a establishes the
finite fixed-data criterion; a general efficient decomposition implementation is
still an open computation artifact.

## 5. First obstruction-generated benchmark: symmetric integer spin

Take one massless parity-paired integer spin `s>=2`. Declare the capability:

```text
one rank-s symmetric potential,
one rank-(s-1) symmetric gradient gauge parameter,
at most a quadratic equation symbol,
no auxiliary carrier,
and the physical null-shell fiber +s direct-sum -s.       (5.1)
```

Let `P_p` be symmetric multiplication by `p`, `A_p` contraction with `p`, and
`T` the trace. They obey

```text
[A_p,P_p]=q,
[T,P_p]=2A_p,
q=p^2.                                                   (5.2)
```

The cheapest equation candidate is the scalar wave symbol `q I`. It fails on a
gauge change:

```text
(q I)P_p epsilon=q P_p epsilon !=0.                      (5.3)
```

The failure is not interpreted after the fact; it is the residual that constructs
the correction. Inside the natural-map ansatz with no metric insertion,
normalize the scalar term and write

```text
D_(b,c)=q I+b P_pA_p+c P_p^2T.                           (5.4)
```

Require the parameter to be traceless for this branch: `T epsilon=0`. Evaluate
the candidate on the same gauge input, using (5.2):

```text
D_(b,c)P_p epsilon
 =(1+b)q P_p epsilon+(b+2c)P_p^2A_p epsilon.              (5.5)
```

The two residual operations have different tensor degree patterns for generic
`epsilon`. Gauge invariance forces

```text
1+b=0,
b+2c=0,

b=-1,
c=1/2.                                                   (5.6)
```

Thus the symbol is generated, within the declared ansatz, as

```text
D_s=q I-P_pA_p+(1/2)P_p^2T.                              (5.7)
```

Equivalently, seek a first-order defect map

```text
C_alpha=A_p+alpha P_pT
```

whose action on a gauge change is exactly the scalar wave symbol. The same-input
calculation gives

```text
C_alpha P_p epsilon
 =q epsilon+(1+2alpha)P_pA_p epsilon,                    (5.8)
```

so `alpha=-1/2` and

```text
C_s=A_p-(1/2)P_pT,
D_s=q I-P_pC_s,
C_sP_p=q I,
D_sP_p=0.                                                (5.9)
```

The carrier constraints are also typing operations, not decorative conditions.
For

```text
G_s=ker T,
F_s=ker T^2,
```

the commutators compute

```text
T^2P_p epsilon=0,                  epsilon in G_s,
T C_s phi=-(1/2)P_pT^2phi=0,       phi in F_s.            (5.10)
```

Hence `P_p:G_s->F_s` and `C_s:F_s->G_s` are typed. If the trace restriction on
the parameter is removed, the residual returns explicitly:

```text
D_sP_p epsilon=(1/2)P_p^3T epsilon.                      (5.11)
```

Equation (5.11) constructs the fork: impose the trace constraint, or add
compensator/auxiliary data whose image cancels this residual. The constrained and
unconstrained formulations are therefore different obstruction resolutions with
different costs.

N4a's restriction and polynomial-divisibility computation supplies the recovery
witness

```text
ker D_s(k)/im P_k
 ~=Sym_0^s(Q_k tensor C)^*
 ~=C_(+s) direct-sum C_(-s).                             (5.12)
```

The supported generative chain is now

```text
wave symbol fails on gradient gauge
  -> finite invariant correction ansatz
  -> residual coefficients force (5.7)
  -> residual typing forces the trace branch (5.10)
  -> unresolved trace gives the compensator fork (5.11)
  -> screen cohomology recovers the particle fiber.       (5.13)
```

This is stronger than checking a known Fronsdal symbol. It is not yet a global
minimality theorem: (5.4) excludes invariant terms containing metric insertion
and assumes the carrier shape and derivative budget in (5.1). Computing the full
spaces (3.1) and proving which candidates are dominated is the next mathematical
obligation.

For `s=1`, trace operations leave the available degrees and the same residual
construction reduces to `D_1=qI-P_pA_p`, the Maxwell potential symbol.

## 6. The complete invariant-map count exposes the hidden choice

The first benchmark forces the coefficients only after (5.1) chooses `R=P_p` and
the three-dimensional equation ansatz (5.4). The calculus must now test whether
those are the complete equivariant spaces.

Let `H_r=ker T` in `Sym^r(M_C^*)` be the traceless symmetric carrier. The trace
decomposition gives, as Lorentz modules,

```text
G_s=H_(s-1),
F_s=H_s direct-sum U H_(s-2).                   (6.1)
```

In the chiral notation already constructed by N2b,

```text
M_C=(1/2,1/2),
H_r=(r/2,r/2),
Sym^2(M_C)=(0,0) direct-sum (1,1).              (6.2)
```

### 6.1 First-order gauge maps

For `s>=2`, apply the two independent `SU(2)` Clebsch--Gordan decompositions to

```text
(1/2,1/2) tensor ((s-1)/2,(s-1)/2).             (6.3)
```

The decomposition contains one copy of `(s/2,s/2)=H_s`, one copy of
`((s-2)/2,(s-2)/2)=H_(s-2)`, and two mixed-chirality summands that do not occur
in `F_s`. Therefore

```text
dim Hom_L(M_C tensor G_s,F_s)=2,       s>=2.     (6.4)
```

The two natural directions may be represented by the gradient `P_p` and a
metric-inserted divergence `U A_p`, after restriction to `G_s`. Thus the ordinary
gradient gauge map is one ray in the full invariant space; spin/helicity alone
does not select it. For `s=1`, the second trace channel is absent and the dimension
drops to one.

### 6.2 Quadratic equation maps

Use (6.2) and decompose each source and target trace level in (6.1). For `s>=3`,
the multiplicities are

| Source -> target | multiplicity in `Sym^2(M_C) tensor source` |
| --- | ---: |
| `H_s -> H_s` | 2 |
| `H_s -> H_(s-2)` | 1 |
| `H_(s-2) -> H_s` | 1 |
| `H_(s-2) -> H_(s-2)` | 2 |

Consequently

```text
dim Hom_L(Sym^2(M_C) tensor F_s,F_s)=6,
                                                    s>=3. (6.5)
```

At `s=2`, the lower trace component is scalar. The `(1,1)` part of
`Sym^2(M_C)` does not map that scalar back to itself, so the dimension is five.
At `s=1`, only `H_1` remains and the dimension is two.

The span

```text
{q I, P_pA_p, P_p^2T}                            (6.6)
```

used in (5.4) is therefore only half of the generic six-dimensional equation
space. The missing channels mix or act within the two trace levels through metric
insertion. This conclusion is representation arithmetic, not a component count.

### 6.3 Construct the complete basis without tensor components

The multiplicity count becomes an executable construction once the two trace
levels are split internally. For `phi in F_s`, define

```text
e_1(phi)=(1/(4s))T phi,
pi_1(phi)=U e_1(phi),
pi_0(phi)=phi-pi_1(phi).                         (6.7)
```

The calculation `T(Uh)=4s h` for `h in H_(s-2)` proves

```text
pi_0(F_s)=H_s,
e_1(F_s)=H_(s-2),
phi=pi_0(phi)+U e_1(phi).                        (6.8)
```

Thus (6.7) is not an imported projector formula; it is the inverse of the trace
operation on the second Fischer layer. Let `calH_r` denote the traceless output of
the finite trace-subtraction recursion constructed in N4c. The two gauge basis maps
are

```text
R_+(p)=calH_s P_p : H_(s-1)->H_s,
R_-(p)=U A_p      : H_(s-1)->U H_(s-2).          (6.9)
```

They also expose the ordinary gradient as a selected ratio, because

```text
T(P_p epsilon)=2A_p epsilon

P_p=R_+(p)+(1/(2s))R_-(p)       on H_(s-1).      (6.10)
```

For `s>=3`, a typed basis of the six quadratic maps is

```text
E_00^q = q pi_0,
E_00^a = calH_s P_p A_p pi_0,

E_01   = calH_s P_p^2 e_1,
E_10   = U A_p^2 pi_0,

E_11^q = U q e_1,
E_11^a = U calH_(s-2) P_p A_p e_1.               (6.11)
```

The first index names the target trace level and the second the source trace
level. Their degrees and types are visible from their compositions. The four
diagonal maps are the scalar and `(1,1)` channels on each irreducible layer; the
two off-diagonal maps are the unique channels between adjacent layers. Therefore
the representation count in (6.5) proves that (6.11) spans the whole space, rather
than merely offering six plausible tensor expressions. At `s=2`, `E_11^a=0`; at
`s=1`, only the two upper-layer diagonal maps remain.

Every candidate in the declared carrier/order budget can now be written

```text
R=r_+ R_+ + r_- R_-,
D=sum_(alpha in {00q,00a,01,10,11q,11a}) d_alpha E_alpha.
                                                               (6.12)
```

No spacetime component array is required. The remaining equation `D R=0` is a
finite bilinear system in the two `r` coefficients and the five/six `d`
coefficients. Its exact coefficient table belongs in the separate
[N10 computation packet](../computation/10-equivariant-obstruction-resolution/README.md),
because expanding every composition here would obscure the semantic construction.

### 6.4 The full gauge-identity calculation remains small

The block basis makes `D R=0` calculable without expanding a symmetric tensor. Put

```text
X=calH_s P_p^2 A_p epsilon,
Y_0=q A_p epsilon,
Y_1=calH_(s-2) P_p A_p^2 epsilon.                (6.13)
```

Repeated use of the four operator relations gives

```text
E_00^a R_+ = q R_+ + ((s-1)/s)X,
E_01   R_- = X,

E_10   R_+ = U[((2s-1)/s)Y_0+((s-2)/s)Y_1],
E_11^q R_- = U Y_0,
E_11^a R_- = U Y_1.                              (6.14)
```

All other source/target-mismatched compositions vanish. Independence of the two
upper and two lower cubic channels turns `D R=0` into four scalar equations:

```text
r_+(d_00q+d_00a)=0,
r_+((s-1)/s)d_00a+r_-d_01=0,

r_+((2s-1)/s)d_10+r_-d_11q=0,
r_+((s-2)/s)d_10+r_-d_11a=0.                    (6.15)
```

For a generic gauge ray with `r_+ r_- !=0`, (6.15) leaves two independent equation
directions: one with upper target and one with lower target. Pure upper or pure
lower gauge rays are still more degenerate. Therefore the exact syzygy calculation
already proves a negative selection result:

> Within the complete fixed-carrier, degree-`(1,2)` search space, gauge invariance
> does not select either the ordinary gradient or one unique field equation.

The coefficient derivation and finite-spin regression are retained in the
[N10 computation packet](../computation/10-equivariant-obstruction-resolution/README.md).
The physical tests below use shell cohomology and characteristic cleanliness before
applying capability cost.

### 6.5 Physical recovery selects one generic chain-equivalence class

Normalize `r_+=1` and write `rho=r_-`. The ordinary gradient has
`rho_0=1/(2s)` by (6.10). For any `rho!=0`, construct the zero-order field
automorphism

```text
S_rho=pi_0+(2s rho)pi_1,
S_rho^(-1)=pi_0+(1/(2s rho))pi_1.                 (6.16)
```

Evaluate it on the same traceless parameter:

```text
S_rho P_p epsilon
 =S_rho[R_+(p)epsilon+(1/(2s))R_-(p)epsilon]
 =R_+(p)epsilon+rho R_-(p)epsilon
 =R_rho(p)epsilon.                               (6.17)
```

Let `D_s` be (5.7) and construct

```text
D_rho(p)=D_s(p)S_rho^(-1).                       (6.18)
```

Then the common-input calculation is

```text
D_rho R_rho epsilon
 =D_s S_rho^(-1)S_rho P_p epsilon
 =D_s P_p epsilon
 =0.                                             (6.19)
```

Moreover `S_rho` maps `ker D_s(p)` bijectively onto `ker D_rho(p)` and maps
`im P_p` onto `im R_rho(p)`. It therefore induces

```text
ker D_s(p)/im P_p  ~=  ker D_rho(p)/im R_rho(p)  (6.20)
```

at every momentum. N4a's off-shell exactness and null-screen computation now apply
to every nonzero gauge ratio without another component calculation. The ordinary
gradient is a convenient normalization of this class, not a uniquely selected
ray.

### 6.6 The lower equation direction is semantically redundant

Let `E_s=pi_0 D_s:F_s->H_s` retain only the traceless equation layer. The inclusion
`ker D_s(p) subset ker E_s(p)` is immediate. To compute the converse, take
`phi in ker E_s(p)`. Trace splitting constructs a unique `ell in H_(s-2)` with

```text
D_s(p)phi=U ell.                                  (6.21)
```

The already constructed Bianchi map `C_s=A_p-(1/2)P_pT` obeys `C_sD_s=0`. Apply
it to the same `phi` and use `A_pU=UA_p+2P_p` and `T(Uell)=4s ell`:

```text
0=C_sD_s phi
  =C_s(Uell)
  =U A_p ell-2(s-1)P_p ell.                       (6.22)
```

For `p!=0`, the linear polynomial `P_p` and the nondegenerate quadratic `U` are
coprime. Equation (6.22) makes `U` divide `P_p ell`, hence `U` divides `ell`.
But `ell` is traceless, and the direct Fischer decomposition gives

```text
H_(s-2) intersect U Sym^(s-4)(M_C^*)={0}.
```

Therefore `ell=0`, so `D_s phi=0`. At `p=0`, both symbols vanish and the equality
is immediate. We have constructed the exact kernel equality

```text
ker E_s(p)=ker D_s(p)                 for every p. (6.23)
```

The same statement transfers through `S_rho` to
`E_rho=pi_0D_sS_rho^(-1)`. Hence any solution of (6.15) with a nonzero upper-target
coefficient has the same kernel whether or not its lower-target equation is added.
If the upper coefficient vanishes, the equation lands only in `H_(s-2)` and the
rank bound gives

```text
dim(ker D/im R)
 >=[dim F_s-dim H_(s-2)]-dim G_s
 =(s+1)^2-s^2
 =2s+1.                                          (6.24)
```

It cannot realize a two-helicity fiber. The nondominated realization therefore
uses `E_rho` alone. It removes `(s-1)^2` equation components:

```text
dim F_s=2s^2+2  ->  dim H_s=(s+1)^2.              (6.25)
```

This is a semantic and executable compression for the free realization problem;
it does not yet claim a cheaper observable computation. It also need not preserve
the action capability, because the equation target is no longer the field carrier.
Action completion must remain a separately priced capability.

### 6.7 The two singular gauge rays fail the physical bench

For the pure upper ray `r_-=0`, equations (6.15) force
`d_00q=d_00a=d_10=0`. Every `h in H_s` is therefore in `ker D(p)`, while the gauge
image has dimension at most `dim G_s=s^2`. Already away from the null cone,

```text
dim(ker D/im R_+) >=(s+1)^2-s^2=2s+1.             (6.26)
```

For the pure lower ray `r_+=0`, take a nonzero null `p`. Every
`h in ker(A_p:H_s->H_(s-1))` is killed by all allowed equation blocks: `q=0`,
`P_pA_ph=0`, and `A_p^2h=0`. These classes cannot be gauge because `im R_-` lies
in the lower trace layer. The null factorization
`H_s~=Sym^s(S) tensor Sym^s(Sbar)` makes `A_p` the tensor product of two
surjective contractions, so

```text
dim ker A_p=(s+1)^2-s^2=2s+1.                    (6.27)
```

Both boundary rays therefore carry at least `2s+1` unwanted classes and are
rejected. At `s=1` the lower layer is absent; the one available gauge direction and
the two upper quadratic maps reduce directly to the Maxwell symbol.

### 6.8 Verdict of the fixed-budget classification

Within `G_s=H_(s-1)`, `F_s=ker T^2`, `deg R=1`, and `deg D=2`, physical recovery
does not select one formula. It selects:

```text
one nonzero-ratio chain-equivalence class of gauge maps,
represented conveniently by the ordinary gradient;

one minimal upper-target equation E_s=pi_0D_s,
with the lower equation layer removed as redundant.        (6.28)
```

The finite-rank computation packet checks (6.20), (6.23), and the boundary failure
for spins `2` through `6`. Equations (6.16)--(6.27), rather than that component
regression, establish the all-spin result.

## 7. Complexity is a partial order, not one magic number

Attach to a supported realization a capability-relative cost record

```text
Cost(F)=
  (degree profile,
   irreducible carrier multiplicities,
   gauge/identity depth,
   characteristic debt,
   physical-recovery depth).                             (7.1)
```

- **Degree profile** records the order of each map, not only the final equation.
- **Carrier multiplicities** count representation content and auxiliary pairs;
  raw component dimension may be retained as a secondary execution estimate.
- **Gauge/identity depth** records how many resolution layers must be constructed.
- **Characteristic debt** records unexplained shells or singular cohomology.
- **Recovery depth** counts the semantic operations needed to obtain the requested
  physical fiber, response, or other declared capability.

Compare two realizations only after fixing the same physical target and requested
capabilities. Use componentwise domination; do not collapse (7.1) to a scalar
unless an application supplies weights. A curvature realization, potential
realization, parity completion, action completion, and causal completion may lie
at different nondominated points.

Contractible pairs and invertible field changes are not cost-free. They preserve
cohomology but may increase differential order, carrier content, inverse
nonlocality, or recovery depth. This is why quasi-isomorphism alone cannot select
the simplest field formulation.

## 8. Novelty boundary

The surrounding literature already supplies major parts of the landscape:

| Framework | Established capability | Boundary of the present candidate |
| --- | --- | --- |
| parent/BRST construction | constructs gauge systems from classes of Poincare modules and relates parent, Labastida, and unfolded formulations | N10 must not claim the first module-to-gauge construction |
| generalized auxiliary-field reduction | relates formulations while exposing locality subtleties for infinite auxiliary systems | N10 adds a proposed explicit capability cost, not a new definition of auxiliary-field equivalence |
| BGG detour complexes | generate invariant gauge and dynamical complexes and expose curved higher-spin propagation obstructions | N10 presently concerns flat orbit-fiber recovery and bounded polynomial candidates |
| compatibility complexes/formal PDE theory | constructs universal identities and gauge-invariant observables downstream of a given differential operator | N10 attempts the reverse design problem from a particle fiber to an operator complex |

The candidate contribution is therefore narrower:

```text
little-group target plus declared local resources
  -> finite invariant-map search
  -> explicit residual-driven repairs
  -> characteristic and physical-fiber recovery
  -> capability-relative Pareto comparison.               (8.1)
```

Whether (8.1) is genuinely new as a combined calculus remains a source question.
No novelty claim is supported until it is compared more deeply with algebraic
free resolutions, Spencer cohomology, BRST/BV, BGG, and unfolded constructions.

## 9. Graph relations and manuscript effect

- `N2/N2a -> N10`: pass the orbit, residual-frame construction, and physical
  fiber; N10 changes their narrative role from preliminaries to forced responses.
- `N3 -> N10`: pass the standard-fiber intertwiner/subquotient and the exact
  polynomial-extension defect.
- `N4a/N4b -> N10`: pass finite map spaces, syzygy and characteristic tests, and
  supported bosonic/fermionic regression families.
- `N4m -> N10`: pass the five-object integer-spin machine as the first finished
  output to be regenerated from residuals.
- `N7 -> N10`: pass the proof that verification, causal equivalence, action
  equivalence, and prediction are distinct; N10 reopens only generative origin.
- `N10 -> N10a`: pass the unconstrained trace residual and compressed constrained
  baseline; N10a constructs and prices the compensator resolution.
- `N10 -> N10c`: pass the natural-operator grammar, typed residual obligations,
  and bosonic regression target; N10c retains them as an exact generator rather
  than another terminal proof.
- `N10b -> N10c`: pass the Clifford/Fischer relations as the next transfer input;
  the known fermionic formula remains an external oracle, not generator data.
- `N10c -> N4m`: return generated `(R,C,D)` and the scalar-wave factorization for
  downstream response use.
- `N10c/N4e -> N10d`: specialize the returned family to Maxwell, construct a
  compact admissible source, and test causal response plus physical-shell recovery.
- `N10c/N10d/N4c -> N10e`: expose the Maxwell-hidden source residual, generate its
  pairing adapter and inverse, and consume them in a compact spin-two response.
- `N10c/N10e/N4c -> N10f`: independently generate the Euler multiplier from the
  skew-adjoint equation residual and recover N10e's same physical current.
- `N10c/N10f/N4i -> N10g`: transfer wave completion, source adaptation, and
  restricted Euler generation to the Clifford grammar, using N4i only as a
  regression and inverse-semantics baseline.
- `N2b/N3/N10c/N10g -> N10h`: distinguish physical labels from off-shell carrier
  presentations, derive the symmetric tensor and spinor-tensor grammars from their
  invariant functorial operations, adapt two handwritten packets, and consume them
  through the retained residual/source interfaces.
- `N4/N4a/N4m/N5/N10h -> N10i`: compare only worktable-certified direct-curvature,
  compressed-potential, and completed-potential routes after capability filtering;
  return their Pareto frontier or a typed missing-witness/budget refusal.
- `N2b/N4/N4a/N5/N10c/N10i -> N10j`: turn N10i's missing integer-spin curvature
  certificate into a minimal-degree chiral compatibility generator, then invoke
  N10i's retained selector operation to produce the revised frontier.
- `N4/N4f/N10e/N10j -> N10k`: consume the retained source adapter and curvature
  operation in two equal scalar-causal routes, then expose the source-compatibility
  obstruction of the direct first-order chiral equation.
- `N4/N10e/N10j/N10k -> N10l`: factor that obstruction into the shortest compatible
  source complex, construct its causal Green operation and potential-source lift,
  then compare complete route cost on the same observable.

The Typst manuscript remains frozen. If N10 succeeds, the paper's central theorem
must change from “these equations realize these representations” to an
obstruction-construction and complexity result. If N10 fails, the supported free
paper remains a technical realization theorem and should not claim a new
low-complexity view.

## 10. Supported frontier and next obligations

Supported in this node:

- the representation-to-locality mismatch is typed as a polynomial-complex
  construction problem;
- for fixed carriers and degree bounds, lift, composition, and characteristic
  obstructions are finite computations;
- the symmetric integer-spin potential coefficients are forced by the gauge
  residual inside the declared natural-map ansatz;
- the full invariant-map count proves that the ordinary gradient occupies one of
  two gauge directions and the three-term equation ansatz occupies only three of
  five/six quadratic directions;
- the complete composition table reduces `D R=0` to four scalar equations and
  proves that gauge invariance alone leaves a family of equation symbols;
- all gauge rays with two nonzero trace-level components form one zero-order local
  chain-equivalence class with the ordinary gradient as a representative;
- the two singular gauge rays fail with at least `2s+1` unwanted cohomology classes;
- the traceless projection `E_s=pi_0D_s` has exactly the same kernel as `D_s` and
  removes `(s-1)^2` redundant equation components for realization capability;
- the trace-constrained and compensator routes are separated by the explicit
  residual `(1/2)P_p^3T`;
- N4a supplies the same-fiber recovery witness for the resulting constrained
  complex.
- N10a proves that the smallest unconstrained compensator equation complex recovers
  the same quotient but is more costly for realization-only capability.
- N10b generates the Fang--Fronsdal symbol, gamma-traceless parameter, and
  triple-gamma field carrier from residuals, then proves that exactly the first two
  gamma-Fischer equation layers suffice within that truncation.
- N10b's unconstrained rank-`n-2` compensator complex reduces exactly to the
  constrained quotient and is again costlier for realization-only capability.
- N10c generates the constrained bosonic `(R,C,D,T,T^2)` and fermionic
  `(R,S,Gamma,Gamma^3)` data from their typed primitive grammars and exact residual
  solving, returns resource-budget refusals, and exports the bosonic result to one
  non-null response-symbol consumer.
- N10d consumes that returned object in the Maxwell specialization, constructs a
  compact conserved current from an antisymmetric potential, recovers nonzero
  retarded and physical-shell outputs, and rejects single-instance computational
  gain after a complete shared-cost comparison.
- N10e generates `M=I-(1/4)UT`, its finite-spin inverse and an identity-only
  refusal from the paired residual `R^dagger M-C`; a compact conserved spin-two
  current fails before adaptation, passes afterward, and produces causal plus
  helicity-two outputs.
- N10f independently generates the same multiplier from `D-D^dagger`, factors the
  remaining defect through `T^2`, returns the quadratic Euler operation `E=MD`,
  and recovers N10e's same current through `E phi=J`.
- N10g generates the Clifford completion `B` from `Q-S^2`; source and Euler
  obstructions independently return
  `M=I-(1/2)Y Gamma-(1/4)Y^2Gamma^2`, while both one-layer budgets are refused.
  Its inverse interface and scalar-wave completion recover a nonzero rank-two
  sourced Euler response.
- N10h refuses a physical or Lorentz label without an off-shell presentation;
  from a declared symmetric-power functor plus metric and optional Clifford action,
  it derives the complete local/adjoint grammars, dispatches their two handwritten
  packets, and passes them through N10c/N10g with provenance preserved. General
  executable grammar synthesis remains open under the construction-origin audit.
- N10i turns the unresolved presentation choice into a bounded operation. For the
  parity-paired integer-helicity registry it filters by certified capability and
  budget, derives route costs from semantic construction traces, and returns a
  Pareto frontier. Spin two remains a realization trade; the direct route dominates
  realization-only potential routes from spin three within the declared axes;
  action/source/causal requests select the completed potential machine; and a
  higher-spin potential/curvature request without a generated certificate returns
  a typed refusal.
- N10j consumes that refusal for integer spin. Lorentz weight proves that the
  chiral target first appears at derivative degree `s` with multiplicity one; the
  generated product of chiral bivector maps kills the gradient gauge image and
  maps the two null-screen endpoint lines isomorphically to N4's direct kernels.
  N10i consumes the packet and charges order `s`, while momentum homogeneity
  obstructs a polynomial local inverse.
- N10k consumes N10e's compact physical source and N10j's retained `K_s`. Constant-
  coefficient convolution constructs identical potential-first and curvature-
  transport-first outputs, while `K_sD_s=QK_s` makes the causal output descend to
  the physical source quotient. The direct first-order chiral equation has
  pointwise source-surjectivity defect `4s-2`, so an unrestricted curvature-source
  Green operation is refused rather than inferred.
- N10l turns that defect into the complex `Curv_s -> E_curv_s -> I_curv_s`, exact
  at non-null momentum.
  Its normalized back operation reduces the compatible first-order Green problem
  to one scalar Green distribution, while the unique order-`s-1` lift of N10e's
  adapted source makes the direct and transported outputs identical. The direct
  carrier has `8s` channels, so this closes semantic capability but rejects a
  computational reduction for the potential-derived observable.

Open bridge that can change the spine:

1. determine whether a native preparation or interaction supplies compatible
   chiral sources without first constructing a potential source, or whether the
   first-order complex improves conditioning/locality for one fixed numerical
   observable despite its larger carrier;
2. audit the full null little-group action rather than quotient dimension alone;
3. only then formalize the allowed chain-equivalence/cost theorem and complete the
   neighboring-framework source comparison.

The symmetric-potential cross-family bench is closed by (6.28), N10a, and N10b.
Residual construction survives the Clifford branch but does not force the same
compression: the bosonic equation needs one trace layer, while the fermionic
equation needs two gamma-Fischer layers. Formula regeneration is closed; retained
generation has now survived one cross-family transfer, one Maxwell causal-use
consumer, and one discriminating spin-two source consumer. N10e closes the bosonic
source adapter, N10f closes its free quadratic Euler operation, N10g transfers the
same retained interface to the Clifford grammar with an independent rank-two
consumer, N10h/N10i close grammar generation plus bounded presentation selection,
N10j closes the integer-spin curvature-output bridge, N10k closes its potential-
derived causal-use bench while refusing the unrestricted direct source interface,
and N10l constructs the compatible source complex but finds no route compression.
All reject cheaper single-instance prediction. The re-entry condition is now a
native direct-source preparation, a conditioning/locality gain on a fixed
observable, a full little-group-action failure, or a stronger physical capability—
not another symmetric rank or hand-derived familiar equation.

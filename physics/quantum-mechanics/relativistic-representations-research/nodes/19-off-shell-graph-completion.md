# Off-shell graph completion

Status: the minimal scalar packet and its structural relative Ward closure are
supported; free-edge realization is exported to node 20 and regulated evaluation
remains open

## Capability and spine binding

Node 17 generated a local scalar--scalar--spin-two vertex and proved its
conservation on scalar mass shells. That was enough for tree exchange, but it is
not enough for the proposed one-loop scalar two-point function: the internal
scalar momentum is integrated off shell.

This node asks for the smallest stronger capability:

```text
generated free edge + action-owned scalar coupling
  -> off-shell vertex identity
  -> graph rewrites forced by that identity
  -> gauge-complete order-g^2 graph packet
  -> only then a regulated two-point evaluation.
```

The upstream anchors are node 17's generated current family and spin-two edge,
and node 18's order-`g^2` irreducible return. The retained target is one scalar
two-point kernel together with its declared external-state quotient at fixed
perturbative order. The downstream question is whether algebraic normalization and
graph quotienting remove repeated tensor/integral work rather than merely rename a
textbook graph.

The present horizon stops before loop integration. It must construct the exact
off-shell identity, generate the second contact vertex from one declared action,
identify the identity that closes its graph packet, and define a cost comparison.
Renormalization, a physical pole shift, and higher-loop closure remain outside the
bench.

## The tree relation cannot be imported into a loop

Retain the scalar inverse kernel, momentum transfer, and scalar product as typed
inputs:

```text
E(p)=Q_p-m^2,
q=p'-p,
s=<p,p'>.
```

Do **not** impose `E(p)=E(p')=0`. The cheapest symmetric bilinear from node 17 is

```text
V_0(p',p)=P_p P_(p') 1.
```

Contracting its spin-two port by `q` computes, in the common rank-one target,

```text
A_q V_0
  =<q,p>P_(p')+<q,p'>P_p
  =(s-Q_p)P_(p')+(Q_(p')-s)P_p.
```

The metric repair generated at tree level is still local:

```text
A_q[U(s-m^2)/2]=(s-m^2)(P_(p')-P_p).
```

Subtract it from the obstruction and collect coefficients of the same two
rank-one operations:

```text
A_q J_0(p',p)
  =[Q_(p')-s+s-m^2]P_p
   +[s-Q_p-(s-m^2)]P_(p')
  =E(p')P_p-E(p)P_(p').
```

Here

```text
J_0(p',p)=P_p P_(p')1-U(s-m^2)/2.
```

This equation is not a failed conservation proof. It is the stronger off-shell
output: divergence factors through the scalar inverse kernels. The improvement

```text
I_q=P_q^2-UQ_q
```

still obeys `A_q I_q=0`, so every member `J_xi=J_0+xi I_q` has the same syzygy.
On shell, substitution of `E(p)=E(p')=0` recovers node 17's conservation law. The
on-shell law is therefore a specialization of this identity, not a valid rewrite
for internal loop legs.

## What the identity computes inside a graph

Let `Delta_E(k)` be a scalar internal edge on a domain where its inverse relation
is admitted:

```text
E(k) Delta_E(k)=1.
```

At a cubic vertex joining an external scalar `p` to an internal scalar `k`, put
`q=k-p`. The generated syzygy evaluates to

```text
A_q J_xi(k,p)=E(k)P_p-E(p)P_k.
```

If the external leg is on shell, composition with the adjacent scalar edge gives

```text
Delta_E(k) A_q J_xi(k,p)
  =Delta_E(k)E(k)P_p
  =P_p.
```

Thus a longitudinal contraction does not vanish. It contracts an internal edge
and returns a local contact operation. This is a semantic graph rewrite: the same
external two-point operation is retained, while a vertex--edge composite is
replaced by the contact term calculated from its inverse relation.

This also exposes a defect in the naive loop request. Two cubic vertices generate
the connected one-loop topology with one internal scalar edge and one internal
spin-two edge, but that graph alone is not closed under the calculated rewrite.
Its longitudinal contraction produces a contact descendant not represented by the
cubic-only grammar.

## The obstruction generates an action-jet compiler

The missing input cannot be selected by representation theory. Choose, as the
smallest transfer bench, the minimally coupled scalar action

```text
S[g,phi]
  =1/2 integral [g^(-1)(d phi,d phi)-m^2 phi^2] vol_g.
```

Minimal coupling is supplied dynamics, not a consequence of the spin-two
representation. A curvature improvement such as `xi R phi^2` is a different action
input and generates a different jet.

Let the covariant metric deformation be encoded by the endomorphism

```text
g_kappa=eta circle (I+kappa H),
H=eta^(-1) h,
t=tr H,
u=tr(H^2).
```

Construct the inverse rather than quoting it. Put

```text
R_kappa=I+kappa R_1+kappa^2 R_2.
```

Multiplication on the same endomorphism space gives

```text
(I+kappa H)R_kappa
  =I+kappa(H+R_1)+kappa^2(R_2+H R_1)+O(kappa^3).
```

Cancelling the two residual coefficients forces

```text
R_1=-H,
R_2=H^2.
```

The volume coefficient is generated independently. In the truncated formal
series, `log det=tr log` computes

```text
det(I+kappa H)
  =1+kappa t+kappa^2 (t^2-u)/2+O(kappa^3).
```

Write its square root as `v_kappa=1+kappa v_1+kappa^2 v_2`. Squaring this candidate
and cancelling coefficients in the same scalar series gives

```text
2v_1=t,
v_1^2+2v_2=(t^2-u)/2,

v_1=t/2,
v_2=t^2/8-u/4.
```

No determinant components are expanded. Convolution of `v_kappa` with
`R_kappa` now generates the densitized inverse metric:

```text
D_0=I,
D_1=(t/2)I-H,
D_2=H^2-(t/2)H+(t^2/8-u/4)I.
```

Substitution into the supplied action returns its reusable second jet:

```text
S_0[phi]
  =1/2 integral [(d phi,d phi)-m^2 phi^2] vol_eta,

S_1[H,phi]
  =1/2 integral [(d phi,D_1 d phi)-m^2 v_1 phi^2] vol_eta,

S_2[H,H,phi]
  =1/2 integral [(d phi,D_2 d phi)-m^2 v_2 phi^2] vol_eta.
```

`S_1` owns the cubic vertex and `S_2` owns the quartic contact vertex. The retained
constructor is

```text
ActionJet(action, order=2, resource budget)
  -> (v_0..v_2, R_0..R_2, D_0..D_2,
      S_0..S_2, provenance, refusal).
```

If only an on-shell cubic current is supplied, it must refuse loop compilation.
The executable constructor currently realizes the algebraic metric jet
`(v,R,D)` for any supplied square endomorphism and refuses orders above two. The
field-functional `S_i` remain semantic consumers of those coefficients rather than
a component tensor expansion.

## The second Ward identity is generated with the action jet

The contact vertex must be connected to the cubic graph by computation, not by its
familiar name. Rescale an infinitesimal diffeomorphism by `kappa` and construct its
action on the same inputs:

```text
delta_xi phi=kappa L_xi phi,
delta_xi h=R_0 xi+kappa L_xi h,
R_0 xi=L_xi eta.
```

Naturality of `d`, metric contraction, and the volume density makes the original
action invariant under simultaneous pullback of `(g,phi)`. Substitute

```text
S_kappa=S_0+kappa S_1+kappa^2 S_2+O(kappa^3)
```

and collect coefficients on the common input `(xi,h,phi)`. Order one computes

```text
D_h S_1[R_0 xi]+D_phi S_0[L_xi phi]=0.
```

After Fourier transformation this is the inverse-kernel syzygy already calculated
above. Order two computes the new identity

```text
D_h S_2[R_0 xi]
  +D_h S_1[L_xi h]
  +D_phi S_1[L_xi phi]
  =0.
```

All three terms are functionals of the same `(xi,h,phi)` and have the same
coupling degree. The first term contracts a gauge port of the contact vertex. The
other two are exactly the metric and scalar gauge descendants of the cubic vertex.
Therefore the second action jet supplies the missing topology-changing relation:
the contact graph is not appended by memory; it is forced as the term that cancels
the cubic packet's calculated residual.

This identity is supported at the action-functional level. Its explicit momentum-
space graph normalization remains open and must be generated from the declared
Fourier and vertex conventions before graph-packet closure is claimed.

There is an essential qualification. A bare off-shell scalar two-point kernel is
not itself invariant under the spin-two gauge symmetry: the scalar external state
also transforms. Consequently a valid packet need not have zero **total** Ward
residual off shell. It must have zero internal residual and expose the remainder in
the external inverse-kernel ideal

```text
I_ext=<E(p_left),E(p_right)>.
```

The observable or external-state compiler may then apply the on-shell quotient
`E(p_left)=E(p_right)=0`, or retain the boundary residual when the requested output
is genuinely off shell. This prevents the graph layer from confusing gauge-
dependent intermediate kernels with observables.

## Generate invariant momentum vertices from the jet

The action jet still needs an evaluator that a graph can consume. Give the metric
space `(V,eta)`, oriented scalar momenta `p,p'`, and an `eta`-self-adjoint
deformation `H`. Put

```text
s=<p,p'>,
v_1(H)=tr(H)/2,
D_1(H)=v_1(H)I-H.
```

Replacing each scalar derivative by its oriented momentum insertion generates the
cubic polynomial

```text
C(H;p',p)
  =-<p,D_1(H)p'>+m^2 v_1(H)
  =<p,H p'>-(tr H)(s-m^2)/2.
```

This is not merely compared with node 17's current. Evaluate it on the linear
gauge deformation

```text
R_0(q,xi)=q tensor xi^flat+xi tensor q^flat,
q=p'-p.
```

The two required contractions are

```text
tr R_0(q,xi)=2<q,xi>,

<p,R_0(q,xi)p'>
  =<p,q><xi,p'>+<p,xi><q,p'>.
```

Substitute `<p,q>=s-Q_p`, `<q,p'>=Q_(p')-s`, and
`<q,xi>=<p',xi>-<p,xi>`. Coefficient collection gives

```text
C(R_0(q,xi);p',p)
  =E(p')<p,xi>-E(p)<p',xi>.
```

Thus the momentum evaluator reconstructs the earlier Ward syzygy from the action
jet on the same typed input.

The contact vertex is generated by polarization. For two self-adjoint metric
deformations `H_1,H_2`, define

```text
v_2(H_1,H_2)
  =(tr H_1)(tr H_2)/8-tr(H_1 H_2)/4,

R_2(H_1,H_2)
  =(H_1 H_2+H_2 H_1)/2,

D_2(H_1,H_2)
  =R_2(H_1,H_2)
   -[(tr H_1)H_2+(tr H_2)H_1]/4
   +v_2(H_1,H_2)I.
```

Direct substitution `H_1=H_2=H` recovers the diagonal coefficient generated
above. The graph-facing contact polynomial is therefore

```text
D(H_1,H_2;p',p)
  =-<p,D_2(H_1,H_2)p'>+m^2 v_2(H_1,H_2).
```

The executable evaluator retains `(v_i,R_i,D_i)` with the scalar value and
provenance. It uses a constant number of traces, matrix compositions, and pairings;
it does not materialize a four-index contact tensor. A dense backend spends
`O(dim(V)^3)` on the second composition and stores `O(dim(V)^2)` coefficients.
This is a real local representation reduction from a materialized rank-four array,
but it is not yet a whole-loop advantage because contraction with the internal
spin-two edge may reintroduce equivalent work.

The overall Fourier phase and signature convention remain evaluator inputs. The
present polynomial fixes the oriented algebraic coefficient, not a universal
Feynman-rule sign.

## Generate the normalized 1PI packet instead of naming diagrams

The target must also decide which graphs count. Choose the amputated one-particle-
irreducible scalar two-point kernel, not the full connected correlator. Polarize the
two action coefficients into symmetric vertices `C` and `D`:

```text
S_int
  =kappa/(2! 1!) C(phi,phi,h)
   +kappa^2/(2! 2!) D(phi,phi,h,h)+O(kappa^3).
```

Use Euclidean `exp(-S_int)` only to fix the following bookkeeping signs; another
evaluator must export its phase convention explicitly. At order `kappa^2`, two
cubic vertices carry denominator

```text
2! (2!)^2=8,
```

where the first factor permutes identical vertices and the other factors permute
the scalar ports at each vertex. Assign two labelled external scalar legs to the
four scalar ports. There are `4*3=12` assignments. They divide without drawing a
diagram:

```text
8 assignments: the external legs meet different cubic vertices;
4 assignments: the external legs meet the same cubic vertex.
```

In the first class, the remaining scalar ports form one internal scalar edge and
the spin-two ports form a parallel internal edge. Removing either edge leaves the
two vertices connected, so the graph is 1PI. Its normalized weight is

```text
w_CC=+8/8=+1.
```

In the second class, the two vertices are joined only by the spin-two edge; that
edge is a bridge. The class has weight `+4/8=+1/2` in the connected correlator but
is rejected by the declared 1PI target rather than silently discarded.

For one contact vertex, the two external scalar assignments give `2!` histories;
the two spin-two ports have one self-pairing. Its vertex denominator is
`2! 2!=4`, and the single insertion carries the negative exponential sign:

```text
w_D=-2/4=-1/2.
```

The action and target therefore generate the packet skeleton

```text
Pi_2^1PI=Gamma_CC-(1/2)Gamma_D.
```

This coefficient is also structurally compatible with the second Ward identity:
differentiating the quadratic contact term in one spin-two slot produces a factor
of two, which cancels its graph weight `1/2`. This is a normalization witness, not
yet the momentum-space closure proof; Fourier conventions and the gauge-fixed
field evaluator still own that calculation.

## Compose the packet without choosing a field normalization

The matter jet and free spin-two edge may use different representatives of the
same field normalization. Do not repair that mismatch with a numerical convention.
Let `h'=lambda h`. Expressing the same metric deformation and free quadratic action
in `h'` gives

```text
C'=lambda^(-1) C,
D'=lambda^(-2) D,
G'=lambda^2 G.
```

Evaluate both packet terms on these transformed inputs:

```text
C' G' C'
  =lambda^(-1) C lambda^2 G lambda^(-1) C
  =C G C,

tr_(h')[G' D']
  =tr_h[lambda^2 G lambda^(-2) D]
  =tr_h[G D].
```

The graph compiler should therefore consume the normalization orbit of `(C,D,G)`,
not an isolated propagator numerator. An absolute coupling convention is required
only when recovering a normalized physical amplitude. This quotient removes an
arbitrary representation choice while preserving both packet contributions.

## Structural relative Ward closure

Let two admissible spin-two Green representatives differ by a gauge-exact
homotopy on the free complex:

```text
delta G=R_0 X+X^dagger R_0^dagger.
```

This is a declared Green-complex hypothesis, not a consequence of the scalar
action. Insert it into the two-cubic graph. Adjointness moves each `R_0` onto its
neighboring cubic current, where the generated Ward syzygy applies. After the
internal scalar inverse kernel cancels its edge, the result has the normal form

```text
delta Gamma_CC
  =X_L+X_R
   -Delta_E(k)[E(p_L)Y_L+E(p_R)Y_R].
```

`X_L,X_R` are the two internal edge-collapse descendants; `Y_L,Y_R` retain the
external scalar transformations. They are names for the displayed typed
composites, not uncomputed equality claims.

The order-two action identity computes the contact variation. With the generated
weight `-1/2`, differentiation of either identical spin-two port gives

```text
delta[-Gamma_D/2]=-X_L-X_R.
```

Adding the two graph variations on their common external two-point target gives

```text
delta Pi_2^1PI
  =-Delta_E(k)[E(p_L)Y_L+E(p_R)Y_R]
  in I_ext.
```

Every internal descendant cancels before loop integration. Applying the declared
external on-shell quotient sends the remaining expression to zero. This is the
first supported graph-level composition of the action jet, inverse-kernel syzygy,
contact weight, and free gauge complex.

The workbench now retains this composition as an obstruction-driven `WardLift`, not
only as prose. In the internal basis `(X_L,X_R)`, the two-cubic contribution supplies
the residual column `(1,1)` and the unweighted order-two action jet supplies the
admissible repair column `(2,2)`. Exact residual solving computes

```text
(1,1)+c(2,2)=(0,0)       ->       c=-1/2.
```

The external coefficients `(-Delta_E Y_L,-Delta_E Y_R)` are carried separately on
the declared generators `(E(p_L),E(p_R))`. The returned packet therefore has

```text
weights=(1,-1/2),
internal residual=(0,0),
external residual in I_ext.
```

If the action jet is absent, outside the residual span, or beyond the repair budget,
the same operation returns the surviving internal channels and a refusal. It does
not yet generate graph orbits: the existing port-history certificate supplies the
candidate 1PI contributions. Automating that preceding orbit-to-residual map is the
remaining graph-side half of this bench.

The result is conditional in two precise ways. The chosen Green representatives
must admit the displayed gauge-exact difference, and the regulator/evaluator must
preserve the algebraic cancellation or return its breaking term. The construction
does not prove that an arbitrary off-shell self-energy is gauge independent.

## Free-edge realization

The structural calculation above consumes a gauge-exact Green homotopy. Its
spin-two realization, including the reason this carrier is the active stress
test, the dimension-dependent trace-reversal inverse, and the common
boundary-value algebra, is generated in
[node 20](20-dimension-compatible-green-compiler.md). Node 19 retains only the
graph-packet obligation and the external ideal that node 20 must preserve.

## Graphs must be compiled in Ward-closed packets

An individual graph is no longer the correct normalization unit. The graph layer
must retain all topologies connected by the action-jet identities:

```text
GraphPacket(vertex jet, external ports, coupling/loop budget)
  1. generate typed contraction histories;
  2. retain connected, 1PI, or observable-linked graphs as requested;
  3. quotient histories by typed graph isomorphism and grading;
  4. contract one gauge port symbolically;
  5. rewrite vertex divergences by the supplied Ward syzygies;
  6. cancel adjacent inverse-kernel/propagator pairs;
  7. add the forced contact descendants;
  8. separate internal residuals from the external inverse-kernel ideal;
  9. accept only when internal residuals vanish, returning the external remainder.
```

The returned object is

```text
(canonical graph packet,
 cached algebra normal forms,
 internal Ward-closure certificate,
 external boundary residual,
 unresolved analytic kernels,
 construction-cost record).
```

This connects the compilers mathematically rather than by file format. The algebra
compiler exports the inverse relations and Ward syzygies; the graph compiler turns
them into topology-changing rewrites; the evaluator receives only a closed packet.
Proof is internal to packet construction because zero internal residual and ideal
membership of the boundary residual are returned certificates.

## Computability claim and complete-route bench

The current result is a potential compression mechanism, not yet measured
computational leverage. Compare the same regulated two-point kernel and the same
external-state quotient by

```text
C_base
  = history enumeration
    + tensor reduction per history
    + gauge/contact cancellation after expansion
    + distinct integral evaluations,

C_packet
  = typed orbit generation
    + one cached normal form per orbit
    + Ward closure before realization
    + remaining master-kernel evaluations
    + observable recovery.
```

Record at least:

```text
N_history, N_orbit, N_normal_form, N_master_kernel,
maximum tensor rank, expression size, and recovery depth.
```

At the present skeleton level the measured counts are

```text
N_history=12+2=14,
N_connected_topology=3,
N_1PI_topology=2.
```

The three connected classes are the rainbow, the bridge graph, and the contact
tadpole; the 1PI target removes only the bridge graph. This `14 -> 3 -> 2`
compression does not establish computational leverage. A competent textbook route
uses the action expansion and symmetry factors to begin with the same two 1PI
terms, rather than normalizing fourteen histories independently. The history count
is therefore a generator regression and provenance certificate.

The compiler wins only if the full packet route reduces one of these costs while
recovering the same quotient observable under the same regulator and tolerance.
A shorter invariant formula, cancellation of one toy term, or reuse of a familiar
Ward identity is insufficient.

No momentum cutoff is selected yet. A regulator is admissible only after the
packet identity is constructed and the regulated evaluator is shown to preserve
internal closure and the declared external ideal (or to expose a controlled
breaking term). Integrating a cubic-only graph with an arbitrary cutoff would
produce a number but would not answer the spine's computability question.

## Checks and boundary

Supported now:

- exact coefficient collection gives
  `A_q J_xi=E(p')P_p-E(p)P_(p')` without components;
- on-shell substitution recovers the tree conservation certificate;
- composition with `Delta_E` contracts an off-shell scalar edge and returns a
  contact operation;
- the cubic-only one-loop graph set is therefore not closed under its own Ward
  rewrite;
- exact inverse and square-root residual solves generate `R_0..R_2`, `v_0..v_2`,
  and `D_0..D_2` without a component tensor expansion;
- polarization generates reusable cubic and contact momentum vertices, and the
  cubic evaluator reproduces the inverse-kernel Ward syzygy;
- coefficient extraction from diffeomorphism invariance generates the order-two
  action identity relating the contact vertex to both cubic descendants;
- the graph-level acceptance target is relative closure: zero internal residual
  with an explicit remainder in `I_ext`, not false invariance of an off-shell
  two-point kernel;
- port-history counting and the 1PI filter generate packet weights `+1` for the
  two-cubic rainbow and `-1/2` for the contact tadpole, while retaining the rejected
  bridge graph as an explicit connected-but-not-1PI class;
- the `14 -> 3 -> 2` history/orbit/1PI reduction is classified as regression, not
  leverage, because the fair textbook baseline also evaluates two normalized
  diagrams;
- the normalization orbit makes both the cubic--cubic and contact contractions
  invariant under `h'=lambda h`;
- under the declared gauge-exact Green-homotopy hypothesis, the normalized packet
  has zero internal Ward residual and an explicit remainder in `I_ext`.
- node 20 now generates a dimension-compatible Green family whose gauge variation
  has exactly the homotopy shape consumed here.
- the retained `WardLift` derives the contact weight from internal residual closure,
  propagates the external ideal, and refuses missing, incompatible, or over-budget
  repairs.

Still open:

- consume node 21's two-sector lowering in one subtracted packet and test whether
  subtraction preserves the relative closure;
- compare invariant Ward reduction with the textbook integrand on maximum tensor
  rank, expression size, and number of master kernels;
- choose a compatible regulator and compare complete construction/evaluation cost.

Reject the branch if contact closure requires hard-coded final diagrams, if the
packet does not recover the direct action expansion, or if its complete cost is no
lower on the fixed two-point bench. Re-enter integration only with a propagator and
regulator that realize the structural closure without an uncontrolled breaking
term.

## Materials and edges

- Node 17 supplies `J_xi`, the spin-two edge, and the negative tree-level cost
  comparison.
- Node 18 supplies the irreducible order-`g^2` return shape.
- `symmetry-and-quantum-fields.typ` supplies the matching/orbit and loop-degree
  baseline, but not the off-shell action completion.
- `sources/action-principle-contracts.md` explicitly bounds the current-exchange
  evidence away from an interacting completion.
- Node 20 owns the independent de Donder/Green theorem contracts and constructs the
  exact homotopy required by this packet.

Edges:

```text
13/14 algebra grammar and residual repair
  + 17 generated local vertex and edge
  + 18 observable-return excursion
  -> 19 off-shell Ward syzygy and graph-packet obligation
  -> 20 dimension-compatible Green compiler
  -> 21 semantic integrand lowering
  -> 22/23 threshold boundary and spectral window
  -> 24 external-ideal observable descent
  -> characteristic external completion or refusal.
```

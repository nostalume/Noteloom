#import "../lib.typ": *
#import "@preview/physica:0.9.8": *
#import theorion: *

#show: daily-en.with(
  title: [From Field Presentations to Observable-Visible Spectral Measures],
  abstract: [
    A covariant field equation is an intermediate presentation, not yet a
    prediction.  This paper constructs a reusable route from a supplied physical
    request to the part of a free field channel visible to that request.  Carrier
    laws and invariant resources first generate a bounded algebra of natural
    operations; failed gauge, source, and adjoint identities then generate their
    repair operations.  The same operation compiler generates the scalar rank
    boundary, the symmetric integer-spin branch, and a component-free Clifford
    branch for parity-paired half-integer spin.  For separate positive integer spin
    in flat spacetime, the resulting curvature annihilates every lower potential-response layer, so
    constrained and compensated field presentations compile to the same scalar
    Green--curvature composite.  A preparation and detector then construct a
    positive visible spectral measure from four typed factors: orbit measure,
    observable amplitude, preparation amplitude, and energy.  The same compiler
    transfers from a massless curvature detector to a massive recoil channel,
    and the returned radial coupling measure supplies preparation-dependent bound, open-channel, finite-time, and memory
    transforms.  The supported result is an exact observable quotient and a
    complete leading-return construction, not a symmetry-derived interaction,
    universal spectral solver, finite-coupling resonance theorem, or runtime
    optimum.
  ],
  keywords: (
    "observable quotient",
    "spectral measure",
    "generative construction",
    "higher-spin curvature",
    "Clifford field complex",
    "bound and open channels",
  ),
)

#show: show-theorion

= Prediction, not presentation <sec-request>

A field equation describes admissible fields and their evolution only after its
analytic completion has been chosen.  A physical calculation additionally needs a
preparation and an observable.  We therefore begin from the typed request

$
  (cal(R), H, P_"prep", O),
$

where $cal(R)$ contains the representation and local carrier resources, $H$ is
the supplied dynamics, $P_"prep"$ selects the prepared sector, and $O$ is the supplied
observable.  The representation constrains admissible channels; it does not choose
$H$, $P_"prep"$, or $O$.

If $"Sol"_(H)$ denotes the response selected by the dynamics and boundary data,
the semantic target is the composite

$
  F_(H,P_"prep",O)=O compose "Sol"_(H) compose P_"prep".
$

An invertible field change may rewrite the middle term without changing this
target composite.  It becomes a computation reduction only when the complete route
to the same value is shorter, cheaper, better conditioned, or reusable.  The representation-to-
field construction needed below is supplied by the companion free-field theorem:
every separate finite helicity in the declared positive-energy class has a local
chiral realization, and the parity-paired symmetric integer-spin family has a
potential complex whose physical quotient recovers the same helicity pair.  That
result is an upstream theorem contract, not the thesis repeated here.  Its state
classification begins with the Wigner orbit/little-group contract @wigner1939,
while the familiar symmetric higher-spin and massless-wave constructions provide
historical regression points rather than the generator's input @fronsdal1978
@lledo2004.

The present question is consequently narrower and more operational:

#align(center)[
  _Which field distinctions can change a named prepared observable, and what
  minimal positive object retains all of its supported predictions?_
]

The answer will be a generator rather than another field catalogue:

#align(center)[
  $
    (cal(R), H, P_"prep", O)
    arrow.r
    M_(P,O)
    arrow.r
    "bound/open/memory transforms".
  $
]

Every nontrivial construction below follows the same reading contract:

#figure(
  fletcher.diagram(
    spacing: 2.8em,
    fletcher.node((0,0), [need]),
    fletcher.node((1,0), [candidate]),
    fletcher.node((2,0), [residual]),
    fletcher.node((3,0), [repair]),
    fletcher.node((4,0), [retained operation]),
    fletcher.edge((0,0), (1,0), "-|>"), fletcher.edge((1,0), (2,0), "-|>"),
    fletcher.edge((2,0), (3,0), "-|>"), fletcher.edge((3,0), (4,0), "-|>"),
  ),
  caption: [An obstruction generates each retained operation.],
) <fig-obstruction-chain>

In symbols, the repair is accepted only when
$"test"("candidate"+"repair")="target"$.

An equation is therefore never meant to appear merely as a familiar identity.
Its surrounding paragraph states what is being requested, the displayed lines
evaluate the candidate on the same typed input, and the following paragraph says
which coefficient, map, or refusal the residual forces.

The construction keeps five kinds of object distinct.  This is a trust ledger,
not extra formalism:

#figure(
  table(
    columns: (1.1fr, 1.65fr, 1.8fr),
    inset: 5pt,
    align: left + top,
    table.header([*Kind*], [*Objects in this paper*], [*Admission rule*]),
    [supplied physical data],
      [$H$, $P_"prep"$, $O$, detector coupling and smearing],
      [not attributed to representation theory],
    [generated operations],
      [$P_p, A_p, T, U, Q_p, L_p, G, K_s$],
      [returned by a stated obstruction calculation],
    [theorem contracts],
      [physical helicity quotient, causal scalar Green distribution, Fock realization],
      [hypotheses, output, and failure boundary are stated],
    [conventions],
      [Fourier sign, chiral scale, detector normalization],
      [may change coordinates or coupling units, not the visible observable],
    [open outputs],
      [interacting matter vertex, CAR detector, finite-coupling resonance],
      [excluded until separately constructed],
  ),
  caption: [Type and provenance ledger for the principal objects.],
) <tab-trust-ledger>

Subscripts keep later operator families disjoint: $P_"prep",Q_"prep"$ are
preparation projections; $P_p,A_p$ act on field carriers;
$B_"dep"$ is a Hamiltonian departure map; and $nu_s$ is a radial coupling
measure whose energy pushforwards are written $M_g$ and $M_e$.
Inside equations containing only field-carrier operations, the lighter symbols
$P_p,A_p,T,U,Q$ abbreviate the explicitly typed field operations above;
$R^H$ always denotes the raise projected between harmonic carriers.

= The spin-two obstruction bench <sec-bench>

The first obstruction appears before any spectral integral.  Take one compact
physical source and ask only for what a finite detector can read from its spin-two
curvature.  Two already valid field realizations are available:

- a constrained harmonic field, whose inverse resolves several invariant response
  layers;
- a compensated full symmetric field, whose source adapter and inverse retain a
  trace sector.

Both recover the same helicity pair, but that representation-level fact does not
yet show that they compute the same sourced observable.  Conversely, choosing the
smaller carrier merely by counting components would confuse a presentation choice
with a physical reduction.

The common input and target are therefore fixed before either route is evaluated:

#figure(
  fletcher.diagram(
    spacing: 3em,
    fletcher.node((0,1), [$J$]),
    fletcher.node((1,0), [constrained]), fletcher.node((1,2), [compensated]),
    fletcher.node((2,0), [$K_2 G_D J$]),
    fletcher.node((2,2), [$K_2 G_F M_2^(-1) J$]),
    fletcher.node((3,1), [$G_Q K_2 J$]),
    fletcher.edge((0,1), (1,0), "-|>"), fletcher.edge((0,1), (1,2), "-|>"),
    fletcher.edge((1,0), (2,0), "-|>"), fletcher.edge((1,2), (2,2), "-|>"),
    fletcher.edge((2,0), (3,1), "-|>"), fletcher.edge((2,2), (3,1), "-|>"),
  ),
  caption: [Two presentations are compared only after the same source and causal
  prescription reach the same curvature readout.],
) <fig-presentation-bench>

The bench succeeds exactly when both composites equal $G_Q K_2 J$.

The bench asks three constructive questions.  Which natural maps can be built
without coordinates?  Which corrections are forced when the cheapest maps leave
their carrier or fail gauge invariance?  After those maps are generated, which
parts of each response survive the curvature detector?

The next two sections construct the needed operations rather than assuming them.
Then @sec-quotient evaluates both complete composites
on the same source.  Spin two is used because it is the first case with a genuine
trace repair; the resulting operations remain indexed by arbitrary separate
  nonnegative integer spin.  A compatible Clifford coefficient action opens the
  half-integer branch, but the spin-two bench itself remains bosonic.

= Operations before equations <sec-operations>

The common normal form would be only a fortunate simplification if $K_s$ and the field
operations were imported in finished form.  Their bounded construction begins
from a free-power carrier law rather than from a named equation.

The immediate capability is modest: generate every operation available from one
momentum covector and one invariant pairing inside a declared rank and polynomial-
degree budget.  This is exactly the information a residual solver can inspect.  A
coordinate matrix is unnecessary because the carrier functor already says how a
new covector may be inserted and how an existing slot may be derived.

Let $F_r(V^*)$ be either the symmetric or exterior free power, with exchange sign
$epsilon=+1$ or $-1$.  The momentum $p in V^*$ supplies the only degree-one
covector, while a nondegenerate invariant pairing $eta$ supplies its dual direction.
For the symmetric cell, fix the tensor-to-polynomial map

$
  Phi(u)=frac(1,r!)phi_(mu_1 dots mu_r)
    u^(mu_1) dots u^(mu_r).
$

Multiplication and differentiation now act on the same symmetric tensor without a
hidden factorial convention.  Within this resource cell the rank shifts construct:

- $P_p=p dot u$: momentum multiplication, raising rank;
- $A_p=p dot partial_u$: metric-dual differentiation, lowering rank;
- $T=partial_u^2$ and $U=u^2$: trace and metric insertion;
- $N=u dot partial_u$: symmetric degree; and
- $Q_p=eta^(-1)(p,p)$: scalar quadratic momentum.

Their first nontrivial composite is not postulated as a commutator.  Write $m_alpha$
for insertion of a covector $alpha$ and $i_v$ for derivation along $v$.  The selected
free-power law says what happens when the derivation meets the new factor:

$
  i_v(m_alpha Phi)=alpha(v)Phi+epsilon m_alpha(i_v Phi).
$

The metric constructs $p^sharp$ from the same momentum.  Substituting
$(alpha,v)=(p,p^sharp)$ now evaluates both sides on the same carrier element:

$
  A_p(P_p Phi)
  &=i_(p^sharp)(m_p Phi)\
  &=p(p^sharp)Phi+epsilon m_p(i_(p^sharp) Phi)\
  &=Q_p Phi+epsilon P_p(A_p Phi).
$

so the compiler emits the rewrite

$
  A_p P_p
  arrow.r epsilon P_p A_p+Q_p.
$

For symmetric powers, $T$ contracts two slots with $eta^(-1)$.  After one
insertion, either contraction slot can meet that new factor, so evaluation on the
same $Phi$ gives

$
  T(P_p Phi)
  &=P_p(T Phi)+A_p Phi+A_p Phi\
  &=P_p(T Phi)+2A_p Phi.
$

Metric insertion is $U=u^2$, whereas trace is $T=partial_u^2$.  Their commutator is
forced by applying the product rule before replacing homogeneous degree by $N$:

$
  T(U Phi)
  &=partial_u^2(u^2 Phi)\
  &=(2d+4u dot partial_u)Phi+u^2 partial_u^2 Phi\
  &=(4N+2d)Phi+U(T Phi).
$

Thus $T P_p=P_p T+2A_p$ and $[T,U]=4N+2d$ are rewrite outputs, not
additional primitives.

The Fischer pairing is constructed from polynomial evaluation,

$
  braket(Phi,Psi)_F=[Phi(partial_u)Psi(u)]_(u=0).
$

Moving one multiplication into the evaluation differentiates the other input;
moving metric insertion does the same twice:

$
  braket(P_p Phi,Psi)_F
  &=[Phi(partial_u)(p dot partial_u)Psi(u)]_(u=0)
   =braket(Phi,A_p Psi)_F,\
  braket(U Phi,Psi)_F
  &=[Phi(partial_u)partial_u^2 Psi(u)]_(u=0)
   =braket(Phi,T Psi)_F.
$

This calculation constructs $P_p^dagger=A_p$ and $U^dagger=T$.  For exterior
powers, the same operations evaluate differently because the carrier alternates:

$
  P_p^2 omega="wedge"(p,"wedge"(p,omega))=0,
  quad A_p^2 omega=i_(p^sharp) i_(p^sharp) omega=0,
  quad "Alt"(eta)=0.
$

The last equality refuses symmetric metric insertion into an alternating pair.
Thus changing the carrier law changes the emitted calculus without naming the
expected field equation.

Exterior exchange symmetry must not be confused with Fermi statistics: an
exterior spacetime carrier describes differential-form slots, while fermionic
statistics enters only after CAR quantization.  The half-integer local carrier is
instead

$
  F_n^"F"="Sym"^n(V^*) times.o Delta,
$

The coefficient action is not supplied.  Request instead a Lorentz-equivariant
symbol $d(p)$, linear in momentum, whose two-step propagation is the scalar symbol
$Q_p I$.  Evaluate this request at $u+v$ and subtract its values at $u$ and $v$:

$
  d(u+v)^2-d(u)^2-d(v)^2
    &=d(u)d(v)+d(v)d(u),\
  Q_(u+v)-Q_u-Q_v&=2eta^(-1)(u,v).
$

The two lines have the same endomorphism target, so scalar-wave completion forces
the polarized relation.  Killing precisely this obstruction in the free tensor
algebra constructs

$
  "Cl"(V^*,eta^(-1))
  =T(V^*)/(u times.o v+v times.o u-2eta^(-1)(u,v)I).
$

The remaining existence step is a bounded representation-theorem contract, not an
output of the polynomial compiler.  For the complex spin cover in four dimensions,
take irreducible chiral modules $S,bar(S)$ with
$V_C equiv S times.o bar(S)$.  Their Clebsch--Gordan decomposition gives

$
  "dim Hom"_"Spin"(V_C times.o S,bar(S))&=1,
  &"dim Hom"_"Spin"(V_C times.o S,S)&=0,\
  "dim Hom"_"Spin"(V_C times.o bar(S),S)&=1,
  &"dim Hom"_"Spin"(V_C times.o bar(S),bar(S))&=0.
$

Thus a vector action has one channel in each direction,
$d_+(v):S arrow.r bar(S)$ and $d_-(v):bar(S) arrow.r S$, but no
same-chirality endomorphism channel.  The endomorphism request therefore forces the
parity-paired carrier $Delta=S plus.o bar(S)$ and the off-diagonal action
$d=d_+ plus.o d_-$.  Scalar-wave completion fixes their common scale through the
polarized relation above.  A real structure requires another intertwiner and is
refused if none is supplied.  The factorizer constructs the quotient and normalized
action after this theorem contract; it does not claim to rederive the classification
of complex spin modules.

Momentum evaluation constructs $L_p=d(p)$.  Applying $d$ after one universal slot
derivation constructs the coefficient contraction $G$, while its Fischer adjoint
constructs insertion $Y=G^dagger$.  On a spinor-valued polynomial $psi(u)$, the
product rule evaluates the first relation rather than naming it:

$
  G(P_p psi)
  &=d(partial_u)((p dot u)psi)\
  &=d(p)psi+(p dot u)d(partial_u)psi\
  &=L_p psi+P_p(G psi).
$

For the other two composites, apply polarization and scalar completion to the same
$psi$:

$
  (G L_p+L_p G)psi
  &=[d(partial_u)d(p)+d(p)d(partial_u)]psi
   =2(p dot partial_u)psi=2A_p psi,\
  L_p^2 psi&=d(p)^2 psi=Q_p psi.
$

Thus $G P_p=P_p G+L_p$, $G L_p=-L_p G+2A_p$, and $L_p^2=Q_p$ are
calculated grammar outputs without a component choice.  The first two remember
which tensor slot was consumed; the last is the scalar-wave factorization that a
later residual calculation may use.

The retained operation has the interface

#align(center)[
  #set math.equation(numbering: none)
  $
    "FirstOrderFactorizer"(eta,"completion","chirality")
      &arrow.r ("coefficient action" | "Refusal"),\
    "NaturalOperations"("carrier law","invariants","action","budget")
      &arrow.r ("operations","laws","adjoints","provenance","certificates" | "Refusal").
  $
]

Its completeness is deliberately bounded.  It covers the declared symmetric and
exterior free-power cells and one compatible Clifford coefficient action; arbitrary
projected or mixed-symmetry operation spaces remain outside the theorem.

= Residuals generate the repairs <sec-repairs>

The emitted grammar is consumed by a residual solver.  For the symmetric bosonic
cell, take the cheapest gauge candidate $R=P_p$ and ask for a degree-one defect map
$C$ satisfying $C R=Q$ on its admitted parameter carrier.  The grammar admits

$
  C=a A_p+b P_p T.
$

Evaluate the two basis maps after the same parameter $epsilon$:

$
  A_p P_p epsilon=P_p A_p epsilon+Q epsilon,
  quad
  P_p T P_p epsilon=P_p^2 T epsilon+2P_p A_p epsilon.
$

Therefore

$
  C P_p epsilon
  =a Q epsilon+(a+2b)P_p A_p epsilon+b P_p^2 T epsilon.
$

Matching the independent $Q epsilon$ and $P_p A_p epsilon$ channels forces
$a=1$ and $b=-1/2$.  The remaining channel then forces $T epsilon=0$ inside
the no-auxiliary budget.  Applying the generated gauge map to that carrier computes

$
  T(P_p epsilon)=2A_p epsilon,
  quad
  T^2(P_p epsilon)=2T A_p epsilon=2A_p T epsilon=0.
$

Thus $P_p$ need not preserve $ker T$, but it does preserve $ker T^2$; double
tracelessness is the shallowest field carrier produced by this calculation.  The
equation is returned as the residual complement

$
  C=A_p-frac(1,2)P_p T,
  quad
  D=Q-P_p C=Q-P_p A_p+frac(1,2)P_p^2 T.
$

The gauge identity is now internal to the construction:

$
  D R=(Q-R C)R=Q R-R Q=0.
$

If trace access is removed, the residual equality requires $a=1$ to produce $Q$ and $a=0$ to cancel
$P_p A_p$.  The solver returns this incompatibility as a refusal rather than a
malformed equation.

== The coefficient residual generates the fermionic branch

The Clifford grammar must now generate an equation rather than merely certify a
known Dirac expression.  For $n>=1$, the cheapest rank-preserving first-order
candidate is $L_p$.  It does not annihilate the gauge candidate $P_p epsilon$.
The bounded grammar supplies one correction of the same degree and rank, so write

$
  cal(S)_b=L_p+b P_p G.
$

Use the generated relation $G P_p=P_p G+L_p$ and the commuting actions
$L_p P_p=P_p L_p$.  Applying the candidate to the same parameter gives

$
  cal(S)_b P_p epsilon
  =(1+b)P_p L_p epsilon+b P_p^2 G epsilon.
$

The first independent channel forces $b=-1$; the remaining channel then vanishes
exactly on the generated parameter carrier $G epsilon=0$.  Hence the residual
operation returns

$
  cal(S)=L_p-P_p G,
  quad cal(S) P_p|_(ker G)=0.
$

The field constraint is generated by preservation.  On the same
$epsilon in ker G$, successive contraction evaluates as

$
  G P_p epsilon&=(P_p G+L_p)epsilon=L_p epsilon,\
  G^2 P_p epsilon
    &=G(P_p G+L_p)epsilon
     =(P_p G^2+L_p G+G L_p)epsilon
     =2A_p epsilon,\
  G^3 P_p epsilon
    &=(P_p G^3+L_p G^2+2A_p G)epsilon=0.
$

Thus $ker G^3$, not an imported triple-contraction rule, is the shallowest
admitted field carrier.  The scalar-wave failure of the returned $cal(S)$ also has
to be generated.  Expanding its square and normal-ordering with the same grammar
gives

$
  cal(S)^2
    &=(L_p-P_p G)^2\
    &=Q-P_p L_p G-P_p G L_p+P_p G P_p G\
    &=Q-2P_p A_p+P_p L_p G+P_p^2 G^2,\
  Q-cal(S)^2
    &=2P_p(A_p-frac(1,2)L_p G-frac(1,2)P_p G^2)
     =2P_p cal(B),\
  cal(B)=A_p-frac(1,2)L_p G-frac(1,2)P_p G^2.
$

This identity is reusable: for an adapted source $J_"F" in ker cal(B)$, the scalar Green
operation gives $psi=cal(S) G_Q J_"F"$ and direct substitution yields
$cal(S) psi=J_"F"$.
Source duality is not hidden in that statement.  With $Y=G^dagger$, seek the
smallest normalized rank-preserving correction

$
  M_"F"=I+a Y G+b Y^2 G^2.
$

The adjoint grammar computes $A_p Y=Y A_p+L_p$ and
$A_p Y^2=Y^2 A_p+2P_p$.  Subtracting the completion map $cal(B)$ and separating
terms that already begin with $Y$ gives

$
  A_p M_"F"-cal(B)
  &=(a+frac(1,2))L_p G+(2b+frac(1,2))P_p G^2\
  &quad +a Y A_p G+b Y^2 A_p G^2.
$

Only the last two terms are invisible against a parameter in $ker G$.  Cancellation
of the two visible channels therefore forces

$
  a=-frac(1,2),
  quad b=-frac(1,4),
  quad M_"F"=I-frac(1,2)Y G-frac(1,4)Y^2 G^2.
$

The Euler request independently tests $cal(E)=M cal(S)$.  Since
$cal(S)^dagger=L_p-Y A_p$, the identity multiplier leaves
$cal(S)-cal(S)^dagger=Y A_p-P_p G$.  Put
$delta(X)=X cal(S)-cal(S)^dagger X$.  The grammar evaluates the two repair images:

$
  delta(Y G)
    &=2Y A_p-2P_p G-Y P_p G^2+Y^2 A_p G,\
  delta(Y^2 G^2)
    &=2Y P_p G^2-2Y^2 A_p G-Y^2 P_p G^3+Y^3 A_p G^2.
$

Cancelling the four visible channels again forces $a=-1/2$, $b=-1/4$ and leaves

$
  M_"F"cal(S)-cal(S)^dagger M_"F"
  =frac(1,4)(Y^2 P_p G^3-Y^3 A_p G^2).
$

The two terms vanish in the pairing on the triple-$G$-traceless field carrier, so
the source and Euler constructions coincide without claiming ambient equality.
This is the free fermionic source/response branch.  CAR quantization and an
interacting fermionic departure measure remain downstream operations; exterior
power alone does not supply them.

== Carrier preservation generates the projected raise

The constrained route asks for something different from the double-traceless
system above: a gauge map from the harmonic parameter carrier
$H_(s-1)=ker T$ into the harmonic field carrier $H_s=ker T$.  The cheapest
candidate is again $P_p$.  It fails on an arbitrary $epsilon in H_(s-1)$ because

$
  T(P_p epsilon)=(P_p T+2A_p)epsilon=2A_p epsilon,
$

which need not vanish.  The failure has rank $s-2$.  Inside the generated grammar,
the lowest-degree repair with the same target rank is therefore $U A_p epsilon$.
Write the unknown correction as

$
  R_(s-1) epsilon=P_p epsilon-alpha_s U A_p epsilon.
$

To solve for $alpha_s$, use the carrier identity
$[T,U]=4N+2d$, where $N$ measures symmetric rank and $d=4$.  Since
$A_p epsilon$ has rank $s-2$ and remains harmonic,

$
  T U A_p epsilon
  =(U T+4N+2d)A_p epsilon
  =4s A_p epsilon.
$

Applying $T$ to the candidate on the same parameter now gives

$
  T R_(s-1) epsilon=(2-4s alpha_s)A_p epsilon.
$

Carrier preservation for every harmonic $epsilon$ forces
$alpha_s=1/(2s)$ and constructs

$
  R_(s-1)=P_p-frac(1,2s)U A_p,
  quad
  T R_(s-1)|_(H_(s-1))=0.
$

The trace-free carrier has not been declared physically superior.  The calculation
only constructs the repair required if that presentation is chosen.

== Gauge-invariant readout generates the curvature degree

The observable cannot consume a gauge representative: its output must be unchanged
under $phi mapsto phi+P_p epsilon$.  The representation baseline supplies the
physical chiral target

$
  cal(C)_s="Sym"^(2 s)(S) plus.o "Sym"^(2 s)(bar(S)),
$

whose two null-shell lines carry helicities $+s$ and $-s$.  This is a theorem
contract from the representation paper.  The present construction asks for the
first polynomial map from $H_s$ to $cal(C)_s$ that can descend through gauge.

For a candidate of momentum degree $r$, the top left spin available from
$"Sym"^r(V_C) times.o H_s$ is $(r+s)/2$.  The positive-chiral target has left
spin $s$.  Therefore

$
  r<s
  quad => quad
  frac(r+s,2)<s,
  quad => quad
  "Hom"_"Lorentz"("Sym"^r(V_C) times.o H_s,
    "Sym"^(2 s)(S))=0.
$

No lower-derivative repair exists in the declared carriers.  At $r=s$, the highest
left-spin coupling and the right-spin singlet each occur once:

$
  dim "Hom"_"Lorentz"("Sym"^s(V_C) times.o H_s,"Sym"^(2 s)(S))&=1,\
  dim "Hom"_"Lorentz"("Sym"^s(V_C) times.o H_s,"Sym"^(2 s)(bar(S)))&=1.
$

Construct that first admissible line.  Antisymmetrization sends
$v times.o w$ to $v times.o w-w times.o v$; orientation and the metric split its
bivector target into chiral summands with projections $pi_+$ and $pi_-$.  Define

$
  b_+^0&=pi_+ compose "wedge":V_C times.o V_C arrow.r "Sym"^2(S),\
  b_-^0&=pi_- compose "wedge":V_C times.o V_C arrow.r "Sym"^2(bar(S)).
$

This constructs the line but not its absolute scale: a one-dimensional Hom space
still admits multiplication by a nonzero scalar.  Choose rotation-invariant fiber
norms and normalize the physical null-shell vectors at unit frequency.  That is a
compiler convention; the remaining physical scale is retained in the spin-specific
detector coupling $g_s$, rather than hidden in $K_s$.

On a polarized symmetric field $"sym"(v_1,...,v_s)$, define

$
  K_s^plus(p)("sym"(v_1,...,v_s))
    =product_(i=1)^s b_+^0(p,v_i),
$
$
  K_s^minus(p)("sym"(v_1,...,v_s))
    =product_(i=1)^s b_-^0(p,v_i),
  quad
  K_s=K_s^plus plus.o K_s^minus.
$

Polarized tensors span the carrier, so this defines the operation linearly.  On a
gauge input, one factor is the inserted momentum.  Evaluating the same product gives

$
  b_+^0(p,p)=b_-^0(p,p)=0,
  quad
  K_s(p)P_p epsilon=0.
$

The first equality is now evaluated: $"wedge"(p,p)=p times.o p-p times.o p=0$,
and both chiral projections send zero to zero.

For the trace layer $U H_(s-2)$, the same degree-$s$ input supplies at most
$j_L=(s+s-2)/2=s-1<s$ (and likewise on the right).  Hence its target Hom spaces
vanish and

$
  K_s(p)U chi=0.
$

These are not checks appended to a remembered curvature formula.  The requested
gauge-invariant chiral readout, the lower-degree obstruction, and the first
nonempty map space generated $K_s$ and the two annihilators consumed next.

== Source conservation generates the adapter

The compensated field solver cannot yet consume a physical current directly.
The invariant carrier pairing constructs $P_p^dagger=A_p$ and $U^dagger=T$.
Consequently gauge invariance of the source pairing asks for

$
  braket(R epsilon,J)=braket(epsilon,R^dagger J)=0,
$

whereas the factorized field response accepts an adapted source $J_"ad"$ satisfying
$C J_"ad"=0$.  At spin one the two conditions coincide.  For $s>=2$, the cheapest
identification $J_"ad"=J$ fails because

$
  A_p-C=frac(1,2)P_p T.
$

The adapter must turn the paired physical constraint into the field-source
constraint.  Equivalently, seek a rank-preserving $M$ for which
$A_p M-C$ has image in the trace layer $"im" U$, invisible when paired with a
harmonic gauge parameter.  The identity candidate leaves the residual above.
Its one trace and unchanged rank force the smallest enlarged ansatz

$
  M=I+m U T.
$

The generated operation grammar evaluates the new word before its coefficient is
chosen:

$
  A_p U T=(U A_p+2P_p)T=U A_p T+2P_p T.
$

Substitution into the same residual gives

$
  A_p M-C=(2m+frac(1,2))P_p T+m U A_p T.
$

Only the second term already lands in $"im" U$; cancellation of the first forces

$
  m=-frac(1,4),
  quad
  M=I-frac(1,4)U T.
$

On the double-traceless carrier, write $phi=h+U k$ with $T h=T k=0$.
Since $T U k=4s k$, one has $(U T)^2=4s U T$ on this carrier.  Composing
$M$ with $I+n_s U T$ and cancelling the nonidentity coefficient gives

$
  -frac(1,4)+n_s-s n_s=0,
  quad
  n_s=-frac(1,4(s-1)),
$

and therefore constructs

$
  M_s^(-1)=I-frac(1,4(s-1))U T,
  quad
  "im"(M_s^(-1)-I) subset.eq "im" U.
$

To close the source bridge, write $A_p M-C=U Z$ and set $J=M J_"ad"$.  For every
harmonic parameter $epsilon$, evaluate the same source pairing:

$
  braket(R epsilon,J)
  =braket(P_p epsilon,M J_"ad")
  =braket(epsilon,A_p M J_"ad")
  =braket(epsilon,C J_"ad")+braket(epsilon,U Z J_"ad")
  =braket(epsilon,C J_"ad").
$

The last term vanishes because $U^dagger=T$ and $T epsilon=0$.  Since $C J_"ad"$
lies in the harmonic parameter carrier and its invariant pairing is nondegenerate,
physical-current conservation is equivalent to $C J_"ad"=0$.  Thus a conserved $J$
constructs the admissible field source $J_"ad"=M_s^(-1) J$.  The coefficient, inverse,
and source conversion needed below have now been constructed inside the paper
rather than imported as trace reversal.

== The shared scalar kernel generates curvature transport

Let $gamma_Q$ be the chosen retarded or advanced scalar fundamental distribution.
The factorized potential Green operation and its curvature-carrier counterpart are
the same convolution on different finite fibers:

$
  G_F J_"ad"="Conv"_(gamma_Q)(J_"ad"),
  quad
  G_Q c="Conv"_(gamma_Q)(c).
$

Because the generated $K_s$ has constant coefficients, differentiation commutes
with convolution on the admitted compact source.  Evaluating both routes on the
same $J_"ad"$ therefore gives

$
  K_s G_F J_"ad"
  =K_s "Conv"_(gamma_Q)(J_"ad")
  ="Conv"_(gamma_Q)(K_s J_"ad")
  =G_Q K_s J_"ad".
$

The equality retains the same boundary prescription; it is not a Green operation
for an independently sourced first-order curvature equation.

== Rank boundaries generate the familiar low spins

The compiler is not tested only at the first traceful case.  Its rank bound removes
every word whose rightmost action would leave the nonnegative free-power tower.
This operation, rather than a list of named equations, produces four informative
boundary cases:

#figure(
  table(
    columns: (0.55fr, 1.25fr, 1.8fr, 1.75fr),
    inset: 5pt,
    align: left + top,
    table.header([*Spin*], [*Compiled carrier cell*], [*Generated local operation*], [*Retained readout/response*]),
    [$0$],
      [$"Sym"^0(V^*)$],
      [$D_0=Q$; no negative-rank gauge map],
      [$K_0=I$, so $G_Q J$ is already observable],
    [$1/2$],
      [$"Sym"^0(V^*) times.o Delta$],
      [$S_(1/2)=L_p$, with $L_p^2=Q$],
      [$psi=L_p G_Q J$ solves $L_p psi=J$],
    [$3/2$],
      [$"Sym"^1(V^*) times.o Delta$],
      [$cal(S)_1=L_p-P_p G$; $G epsilon=0$ by rank],
      [$cal(B)_1=A_p-L_p G/2$ adapts the source],
    [$1$],
      [$"Sym"^1(V^*)$],
      [$C_1=A_p$, $D_1=Q-P_p A_p$],
      [$K_1(A)=b_+(p,A) plus.o b_-(p,A)$],
    [$2$],
      [$"Sym"^2(V^*)$],
      [$C_2=A_p-P_p T/2$, $D_2=Q-P_p A_p+P_p^2 T/2$],
      [$K_2$ is the first case using the trace/source repairs],
  ),
  caption: [Low-spin outputs of one rank-aware operation compiler. The familiar
  scalar, spinor, Maxwell, and linearized spin-two names are interpretations of
  the returned operations, not compiler inputs.],
) <tab-low-spin>

For spin zero, $A_p$ and $T$ cannot act on the input carrier, so restricting the
general symmetric residual to rank zero leaves exactly $Q$.  For spin one, $T$
still cannot act, while $A_p$ can; hence the same restriction leaves $Q-P_p A_p$,
and the physical source condition is already $A_p J=0$.  At spin two, trace becomes
available and its uncancelled residual forces the first genuine repair.  The
sequence therefore explains why spin two was a discriminating obstruction bench
without treating it as the definition of the compiler.

The spin-one-half row is a different rank boundary of the Clifford cell.  Because
$G$ would lower tensor rank below zero, the correction $P_p G$ is absent and the
generated equation is simply $L_p$.  From tensor rank one onward the same cell
retains $L_p-P_p G$ and its gamma constraints.  No explicit gamma matrix has entered
either specialization.

The first nontrivial half-integer transfer is spin three halves, not merely the
statement “from rank one onward.”  Its gauge parameter has rank zero, so
$G epsilon=0$.  The compiler laws evaluate the residual without components:

$
  cal(S)_1 P_p epsilon
  &=(L_p-P_p G)P_p epsilon\
  &=P_p L_p epsilon-P_p(P_p G+L_p)epsilon
    =-P_p^2 G epsilon=0.
$

The scalar-completion identity specializes because $G^2$ cannot act twice on a
rank-one tensor:

$
  Q_p-cal(S)_1^2=2P_p cal(B)_1,
  quad
  cal(B)_1=A_p-frac(1,2)L_p G.
$

Thus $J in ker cal(B)_1$ has the generated solution
$Psi=cal(S)_1 G_Q J$.  With the declared antisymmetrization convention, the
textbook Rarita--Schwinger image is a post-composition, not an imported equation:

$
  cal(R)_mu
  =(cal(S)_1 Psi)_mu-frac(1,2)gamma_mu
     gamma^nu(cal(S)_1 Psi)_nu
  =gamma_(mu nu rho) p^nu psi^rho.
$

This is the conventional half-integer regression target @fang-fronsdal1978.

The physical-recovery theorem contract then returns
$ker cal(S)_1(k)/"im" P_k
  equiv C_(+3/2) plus.o C_(-3/2)$ for nonzero future-null $k$.
This is a field regression only: no fermionic visible measure is claimed before a
CAR departure constructor and a physical fermionic detector are supplied.

For orientation, the compact component dictionary is:

#figure(
  table(
    columns: (1.05fr, 1.9fr, 1.7fr),
    inset: 5pt,
    align: left + top,
    table.header([*Generated object*], [*Component image*], [*Textbook role*]),
    [$D_0=Q_p$], [$p^2 phi$], [massless scalar wave],
    [$D_1=Q_p-P_p A_p$],
      [$p^2 A_mu-p_mu(p dot A)$], [Maxwell kinetic operator],
    [$C_2=A_p-P_p T/2$],
      [$p^rho h_(rho mu)-p_mu h^"tr"/2$], [de Donder functional],
    [$D_2=Q_p-P_p A_p+P_p^2 T/2$],
      [$p^2 h_(mu nu)-p_mu p^rho h_(rho nu)-p_nu p^rho h_(rho mu)+p_mu p_nu h^"tr"$],
      [spin-two Fronsdal tensor],
    [$L_p$], [$slash(p)$], [massless Dirac symbol],
    [$cal(S)_1$], [$slash(p)psi_mu-p_mu(gamma dot psi)$],
      [Fang--Fronsdal vector-spinor],
    [$K_1$], [$(pi_+ plus.o pi_-)("wedge"(p,A))$],
      [chiral Maxwell curvature],
    [$K_2$], [chiral projection of the double curl],
      [linearized Weyl curvature],
  ),
  caption: [Regression dictionary. Components translate generated operations; they
  do not generate them.],
) <tab-textbook-dictionary>

For example, the Maxwell row is checked on a common $A$ and scalar $alpha$:

$
  (D_1 A)_mu&=p^2 A_mu-p_mu(p dot A),\
  (D_1(p alpha))_mu&=p^2 p_mu alpha-p_mu p^2 alpha=0,\
  "wedge"(p,A+p alpha)&="wedge"(p,A).
$

= The observable quotient <sec-quotient>

The construction has now changed the primitive computational target.  It no longer
asks which field presentation is intrinsically smallest.  It asks which quotient
is invisible to the supplied observable.

Let $cal(P)$ denote the physical response space and define

$
  phi tilde_O psi
  quad <=> quad
  O(phi)=O(psi).
$

For a linear curvature observable, the null directions include gauge, trace, and
potentially some dynamically generated response layers.  We must compute those
inclusions rather than infer them from physical degree-of-freedom counts.

The constrained inverse is not admitted as an unnamed polynomial.  On the
harmonic carrier define the dimensionless operation

$
  X_s=R^H_(s-1) A_p/Q_p.
$

The invariant-layer theorem contract constructs its eigenvalues
$c_(s,l)=[s(s+1)-l(l+1)]/(2s)$ and identifies $l=s-1$ as the gauge layer.
At the spin-two bench these are

$
  c_(2,0)=frac(3,2),
  quad c_(2,1)=1,
  quad c_(2,2)=0.
$

The inverse and gauge-removal requirements are therefore the three interpolation
conditions

$
  f_2(frac(3,2))=-2,
  quad f_2(1)=0,
  quad f_2(0)=1.
$

Writing $f_2(x)=c_0+c_1 x+c_2 x^2$ turns these values into the finite solve

$
  mat(1,0,0; 1,1,1; 1,frac(3,2),frac(9,4))
  mat(c_0; c_1; c_2)
  =mat(1; 0; -2)
  quad => quad
  mat(c_0; c_1; c_2)=mat(1; 1; -2).
$

Thus $f_2(x)=1+x-2x^2$, and

$
  G_(D,2)=G_Q(I+X_2-2X_2^2).
$

The general nodes do not collide: for $l != l'$, their difference is
$[l'(l'+1)-l(l+1)]/(2s) != 0$; moreover $c_(s,l)=1$ only at the gauge layer
$l=s-1$.  Thus interpolation is defined precisely when that layer is removed.
For general $s$, $f_s(c_(s,s-1))=0$ and
$f_s(c_(s,l))=1/(1-c_(s,l))$ on every non-gauge layer.  Each power of
$X_s$ contains a power of $Q_p^(-1)$; all such powers receive the same retarded
or advanced boundary prescription as $G_Q$.  Existence of those distributional
powers is the causal theorem contract, not hidden algebraic division.

Every response layer below the top transverse one begins with the constructed
raise $R^H_(s-1)$.  Apply $K_s$ to that same map and use the two generated
annihilators:

$
  K_s R^H_(s-1)
  =K_s P_p-frac(1,2s)K_s U A_p
  =0.
$

Thus $K_s X_s=0$.  At spin two, the full polynomial is evaluated rather than
abbreviated:

$
  K_2 f_2(X_2)=K_2+K_2 X_2-2K_2 X_2^2=K_2.
$

Since $K_s$ and the scalar boundary-selected Green operation
$G_Q$ have constant coefficients, their distributional composites commute on the
admissible compact source class.  Evaluating the complete constrained route on one
such source $j$ gives

$
  K_s G_D j
  =G_Q K_s f_s(X_s)j
  =G_Q f_s(0)K_s j
  =G_Q K_s j.
$

For the compensated route, the source-repair theorem contract states that
$M_s^(-1)-I$ lands in $"im" U$.  Hence, on the corresponding representative $J$,

$
  K_s M_s^(-1) J
  =K_s J+K_s(M_s^(-1)-I)J
  =K_s J.
$

The second contract $K_s G_F=G_Q K_s$ then computes

$
  K_s G_F M_s^(-1) J=G_Q K_s J.
$

Both composites now have the same source class, causal boundary condition, and
curvature-distribution codomain.  Their equality constructs, rather than names,
the common quotient response

$
  "ObservableResponse"_s(J)=G_Q K_s J.
$

No projector onto every discarded field layer was needed.  The observable itself
supplied the annihilator that removed them.

#proposition[Presentation-neutral curvature response][
  For the supported flat symmetric integer-spin systems, any constrained or
  compensated source representing the same physical source class has the same
  boundary-selected curvature response $G_Q K_s J$.  The equality is forced by the
  annihilators $K_s P_p=K_s U=0$ and constant-coefficient Green commutation.  It does
  not imply equality of off-shell field representatives, actions, interacting
  deformations, or numerical implementations.
] <prop-curvature-response>

The returned object may be cached once per source and then paired with many
curvature functionals.  Fusion should retain the composite Green--curvature symbol
rather than materialize a high-order numerator before applying the Green
denominator.  This changes intermediate numerical range while preserving the same
distributional boundary prescription; it does not remove the physical high-
frequency order of the observable.

= The visible-measure compiler <sec-measure>

The quotient response is still classical.  To construct a quantum prediction,
introduce a supplied preparation and detector.  For a two-level probe with ground
and excited states, gap $Omega$, localized smearing $f$, detector contraction $e$,
and coupling $g_s$, construct the detector transition
$m_D=ket(0)bra(1)+ket(1)bra(0)$, form the smeared curvature observable
$cal(O)_s(f,e)$ by

$
  cal(O)_s(f,e)=integral_(Sigma) f(x)
    braket(e,K_s Phi_s(x)) d Sigma(x),
$

and declare the interaction

$
  V_s=m_D times.o cal(O)_s(f,e),
  quad
  H_("tot",s)=H_D+H_F+g_s V_s.
$

This Hamiltonian is a supplied detector model, not a consequence of representation
theory.  Its relevant property is that it couples directly to the generated
gauge-invariant curvature channel.

The positive-one-particle/Fock theorem contract is used at one precise boundary:
a positive-frequency one-particle space and its bosonic symmetric Fock functor
return a linear smeared field $C_s=a_s+a_s^dagger$ whose annihilation part kills
the vacuum and whose creation part maps the vacuum to the one-particle space.
It does not construct the interaction, detector, or a dressed state.
The positive/quasifree construction is standard background for this contract
@khavkine-moretti2015; the shell amplitude below remains an internal computation.

Let $P_"prep"$ project onto the two vacuum preparations

$
  "Ran" P_"prep"="span"(ket(0) times.o Omega_F, ket(1) times.o Omega_F),
  quad
  Q_"prep"=1-P_"prep".
$

Put $H_0=H_D+H_F$.  This free Hamiltonian preserves the prepared space, so only the
interaction can leave it.  With $cal(O)_s(f,e)=a_s(f,e)+a_s^dagger(f,e)$, vacuum
annihilation evaluates the first departure operation on both prepared vectors:

$
  B_("dep",s)^(1)=Q_"prep" V_s P_"prep",
$
$
  B_("dep",s)^(1)(ket(0) times.o Omega_F)
    =ket(1) times.o a_s^dagger(f,e)Omega_F,
$
$
  B_("dep",s)^(1)(ket(1) times.o Omega_F)
    =ket(0) times.o a_s^dagger(f,e)Omega_F.
$

Because $Q_"prep" H_0 P_"prep"=0$, the full departure is computed rather than
assigned:

$
  Q_"prep" H_("tot",s) P_"prep"
  =g_s Q_"prep" V_s P_"prep"=g_s B_("dep",s)^(1).
$

Its range is exactly one-particle at the
first nonzero return order.  This sparsity, rather than a Fock cutoff, is why the
complete coefficient through order $g^2$ needs no dressed Fock eigenvector.

== Why the departure spectral measure is forced

The measure is not introduced as a convenient bath description.  It is the common
object required when the prepared space is not invariant.  For an arbitrary
Hamiltonian $H$, define

$
  B_"dep"=Q_"prep" H P_"prep",
  quad
  H_"prep"=P_"prep" H P_"prep",
  quad
  H_"comp"=Q_"prep" H Q_"prep".
$

Assume $H=H^dagger$, so the reverse block is $P_"prep" H Q_"prep"=B_"dep"^dagger$.
To compute the prepared resolvent, solve
$[z-H](psi+chi)=eta$ with $psi in "Ran" P_"prep"$, $chi in "Ran" Q_"prep"$, and
$eta in "Ran" P_"prep"$.  Applying both projectors gives the two blocks

$
  (z-H_"prep")psi-B_"dep"^dagger chi=eta,
  quad
  -B_"dep"psi+(z-H_"comp")chi=0.
$

For $z$ in the complementary resolvent set, the second block gives

$
  (z-H_"comp")chi=B_"dep" psi,
  quad
  chi=(z-H_"comp")^(-1) B_"dep" psi.
$

Substitution into the prepared equation yields

$
  [z-H_"prep"-B_"dep"^dagger(z-H_"comp")^(-1) B_"dep"] psi=eta.
$

Therefore every prepared resolvent query consumes the self-energy

$
  Sigma_"dep"(z)=B_"dep"^dagger(z-H_"comp")^(-1) B_"dep".
$

The independent time construction starts from $i dot(Psi)=H Psi$, with
$Psi=psi+chi$ and $chi(0)=0$.  Projection, integration of the second equation,
and substitution into the first give

$
  i dot(psi)&=H_"prep" psi+B_"dep"^dagger chi,\
  i dot(chi)&=B_"dep" psi+H_"comp" chi,\
  chi(t)&=-i integral_0^t exp(-i(t-tau)H_"comp") B_"dep" psi(tau)d tau,\
  i dot(psi)(t)&=H_"prep" psi(t)
    -i integral_0^t cal(K)_"dep"(t-tau) psi(tau)d tau,
$

where the return kernel is
$cal(K)_"dep"(t)=B_"dep"^dagger exp(-i t H_"comp")B_"dep"$.
Let $E_"comp"$ be the projection-valued spectral
measure of $H_"comp"$.  Applying its functional calculus to these two operations on the
same prepared vector constructs the positive operator-valued measure

$
  M_"dep"(Delta)=B_"dep"^dagger E_"comp"(Delta)B_"dep",
$

whose positivity is computed on every prepared $psi$:

$
  braket(psi,M_"dep"(Delta)psi)
  =braket(B_"dep"psi,E_"comp"(Delta)B_"dep"psi)
  =norm(E_"comp"(Delta)B_"dep"psi)^2 >= 0.
$

with the two coincident transforms

$
  Sigma_"dep"(z)=integral frac(d M_"dep"(E),z-E),
  quad
  cal(K)_"dep"(t)=integral exp(-i t E) d M_"dep"(E).
$

This is why $M_"dep"$, rather than a field representative or a guessed density, is the
semantic object preserved by the later bound and temporal calculations.

For the supported coefficient through order $g^2$, use the free complement
$H_("comp",0)=Q_"prep" H_0 Q_"prep"$ and the already computed $B_("dep",s)^(1)$.  The retained measure is

$
  M_s^(2)(Delta)
  =g_s^2(B_("dep",s)^(1))^dagger E_("comp",0)(Delta)B_("dep",s)^(1).
$

Higher return orders replace this one-particle measure by the spectral data of
larger cyclic Fock sectors; the present construction makes no claim there.

After the finite internal fiber has been reduced, let $r>=0$ parameterize a radial
one-particle channel and let $ket((r,alpha))$ denote its generalized shell vectors.
The following factorization is conditional, not automatic: the declared detector
coupling is separable between its finite-fiber observable and radial preparation.
Under that condition its departure matrix element evaluates as

$
  braket(r,alpha,B_("dep",s)^(1) psi)=a_alpha(r)h(r).
$

Here $a_alpha(r)$ is the observable shell action on the finite physical fiber and
$h(r)$ is the preparation amplitude.  If $q(r)d r$ is the radial Hilbert measure,
spectral resolution on an energy set $Delta$ evaluates

$
  braket(psi,M_s^(2)(Delta),psi)
  =g_s^2 integral 1_Delta(epsilon(r))q(r)
     sum_alpha abs(a_alpha(r))^2 abs(h(r))^2 d r.
$

After the internal finite-fiber norm is constructed, absorb $g_s$ into the prepared
amplitude and write $abs(a(r))^2=sum_alpha abs(a_alpha(r))^2$.  The compiler thus
receives four independently meaningful maps:

$
  q(r) d r,
  quad a(r),
  quad h(r),
  quad epsilon(r).
$

They are respectively the orbit/Hilbert measure, observable shell amplitude,
coupled preparation amplitude, and complementary energy.  The preceding shell
calculation—not a density ansatz—forces the radial measure

$
  d nu_s(r)=q(r)abs(a(r))^2 abs(h(r))^2 d r.
$

Assume $epsilon(0)=E_"th"$ and $epsilon'(r)>0$ on the declared window.  The
spectral measure is the pushforward

$
  M_epsilon(Delta)=integral 1_Delta(epsilon(r)) d nu_s(r)
  =(epsilon_* nu_s)(Delta).
$

Its density is constructed rather than guessed.  Evaluate both descriptions on
the same compactly supported test function $F$ and substitute $E=epsilon(r)$:

$
  integral F(E) d M_epsilon(E)
  =integral F(epsilon(r))q(r)abs(a(r))^2 abs(h(r))^2 d r
$
$
  =integral_(E_"th")^infinity F(E)
    frac(q(r(E))abs(a(r(E)))^2 abs(h(r(E)))^2,
         epsilon'(r(E))) d E.
$

Since both sides are the same positive functional on every such $F$, the pushforward density
is

$
  m(E)=frac(q(r(E))abs(a(r(E)))^2 abs(h(r(E)))^2,
            epsilon'(r(E))).
$

If $epsilon$ turns around, the single-branch density formula omits roots and is false.  The compiler must then
receive or construct monotone branches and sum their positive pushforwards; without
that branch certificate it refuses the scalar density.

== Angular construction for the curvature detector

For a future null momentum $p=omega(1,n)$ in three spatial dimensions,

$
  frac(d^3 p,2abs(p))
  =frac(omega^2 d omega d Omega(n),2omega)
  =frac(omega,2) d omega d Omega(n).
$

For $s>=1$, evaluate the normalized curvature map at unit frequency on unit
helicity vectors and call the results $kappa_(s,+)(n)$ and $kappa_(s,-)(n)$.
The projectors are then constructed, not presumed:

$
  Pi_(s,h)(n)
  =frac(ket(kappa_(s,h)(n))bra(kappa_(s,h)(n)),
          norm(kappa_(s,h)(n))^2),
  quad h in {+,-}.
$

This quotient is invariant under a nonzero rescaling of the shell vector.  The
absolute normalization omitted by the projector remains in $g_s$.
To decide whether direction can be discarded, construct its positive sphere
average before assuming that it is a scalar:

$
  Q_s=integral_(S^2)(Pi_(s,+)(n) plus.o Pi_(s,-)(n)) d Omega(n).
$

Write $Q_s=Q_(s,+) plus.o Q_(s,-)$.  For either chirality, evaluate a rotation on
the same averaged operator:

$
  U_s(R)Q_(s,+) U_s(R)^(-1)
  =integral_(S^2) U_s(R)Pi_(s,+)(n)U_s(R)^(-1) d Omega(n)
$
$
  =integral_(S^2) Pi_(s,+)(R n) d Omega(n)
  =Q_(s,+).
$

The second equality is projector covariance; the third substitutes $n'=R n$ and
uses invariance of sphere measure.  Thus $Q_(s,+)$ lies in the commutant of the
irreducible spin-$s$ rotation module.  The irreducible-commutant theorem contract
returns $Q_(s,+)=lambda_s I$.  It leaves only one coefficient, which the trace of the
same constructed operator computes:

$
  (2s+1)lambda_s=integral_(S^2) "Tr" Pi_(s,+)(n) d Omega(n)=4pi,
  quad
  lambda_s=frac(4pi,2s+1).
$

For $e=e_+ plus.o e_-$, the angular response is consequently

$
  A_(s,e)=frac(4pi,2s+1)
    (norm(e_+)^2+norm(e_-)^2).
$

The scalar boundary is generated separately rather than by duplicating the two
chiral lines at $s=0$.  Its physical fiber is one-dimensional, $K_0=I$, and sphere
averaging the identity gives

$
  A_(0,e)=4pi norm(e)^2.
$

With this rank-zero convention the following visible-measure formula applies to
the scalar and every supported positive integer curvature channel.

The detector tensor is supplied; its integrated response is generated.  Before
abbreviation, the created shell amplitude is the product

$
  beta_(s,h)(omega,n)
  =g_s omega^s hat(f)(omega n)
    braket(e_h,kappa_(s,h)(n)).
$

Its factors are respectively coupling, curvature action, preparation smearing,
and finite-fiber detector contraction.  Since the
curvature has derivative degree $s$, its squared null-shell amplitude contributes
$omega^(2 s)$.  Multiplying the shell factor, angular response, and squared preparation amplitude
$g_s^2 abs(hat(f)(omega))^2$ gives the radial coupling measure

$
  d nu_(s,e)(omega)
  =frac(g_s^2 A_(s,e),2)
    omega^(2 s+1) abs(hat(f)(omega))^2 d omega.
$

The power $2s+1$ is therefore an output: one shell power plus twice the curvature
degree.  If the smearing is anisotropic, its angular weight remains inside the
projector average, which need not be scalar.  The compiler then retains a
direction-dependent positive operator instead of asserting a scalar radial measure.

= One radial measure, two spectra <sec-transforms>

The semantic advantage of $nu_s$ is reuse.  Each requested quantity is a transform
of the same constructed radial coupling measure, not a new fitted bath.  The
energy-coordinate measures are nevertheless preparation dependent.  For the
ground and excited vacuum preparations define

$
  epsilon_g(omega)=Omega+omega,
  quad
  epsilon_e(omega)=omega-Omega,
$

where the excited prepared energy has been shifted to zero.  The scalar spectral
measures are the distinct pushforwards

$
  M_g=(epsilon_g)_*nu_s,
  quad M_e=(epsilon_e)_*nu_s.
$

Equivalently, the unshifted two-preparation operator-valued measure retains both
diagonal energy placements.  The common object is $nu_s$, not a scalar measure in
one shared energy coordinate.
The spectral theorem is used here only as the transform contract for the positive
measure; it does not construct the model-dependent factors entering that measure.

== Bound branch from the projected resolvent

Take the detector ground-vacuum energy as zero.  Its complementary one-particle
energy is $Omega+omega$, so evaluating the self-energy constructed in
@sec-measure at the unperturbed energy gives

$
  Sigma_g(z)=integral_0^infinity
    frac(d nu_s(omega),z-(Omega+omega)),
$
$
  delta E_g=Sigma_g(0)
    =-integral_0^infinity frac(d nu_s(omega),Omega+omega).
$

The prepared resolvent denominator is $D_g(z)=z-Sigma_g(z)$ at this order.  If
$z_*$ is its simple zero, its exact residue within this reduced model and its
order-$g^2$ expansion are

$
  "Res"_(z=z_*) frac(1,D_g(z))
  &=frac(1,1-Sigma_g'(z_*))\
  &=1+Sigma_g'(0)+O(g_s^4),\
  Sigma_g'(0)&=-integral_0^infinity
    frac(d nu_s(omega),(Omega+omega)^2).
$

Thus the complete leading correction is

$
  Z_g=1+Sigma_g'(0)
    =1-integral_0^infinity frac(d nu_s(omega),(Omega+omega)^2).
$

The sign and denominator are therefore outputs of the prepared energy placement;
they were not attached to an arbitrary transform.

== Open branch from the transition amplitude

For the excited vacuum, let $b(omega)$ denote the visible one-particle departure
amplitude, so $abs(b(omega))^2 d omega=d nu_s(omega)$.  The first Duhamel term for a
particle of energy $omega$ is

$
  cal(A)_t(omega)
  =-i b(omega)integral_0^t exp(i(omega-Omega)tau)d tau
$
$
  =-i b(omega)exp(i(omega-Omega)t/2)
     frac(2sin((Omega-omega)t/2),Omega-omega).
$

Taking its norm before integrating over the orthogonal shell states constructs the
finite-time emitted event:

$
  P_"emit"(t)=integral_0^infinity
    frac(4 sin^2((Omega-omega)t/2),(Omega-omega)^2) d nu_s(omega).
$

If $d nu_s(omega)=m_s(omega)d omega$ with $m_s$ continuous at $Omega$, its continuum
boundary coefficient follows from the approximate identity

$
  frac(1,t)frac(4sin^2(x t/2),x^2)
  arrow.r 2pi delta(x)
$

against continuous test densities.  Substituting $x=Omega-omega$ gives

$
  Gamma=2pi m_s(Omega),
  quad
  P_"emit"(t)/t arrow.r Gamma
$

at the coefficient level.  This limit is not an exponential survival theorem
at finite coupling.

== Memory branch from complementary evolution

The time-elimination calculation in @sec-measure already constructed the operator
$B_"dep"^dagger exp(-i t H_"comp")B_"dep"$.  First retain the Fourier transform
of the common radial measure,

$
  hat(nu)_s(t)=integral_0^infinity exp(-i omega t) d nu_s(omega).
$

The preparation-specific return kernels are then computed without ambiguity:

$
  cal(K)_g(t)=exp(-i Omega t)hat(nu)_s(t),
  quad
  cal(K)_e(t)=exp(+i Omega t)hat(nu)_s(t).
$

When $integral omega^n d nu_s(omega)<infinity$, differentiation is admitted and

$
  i^n partial_t^n hat(nu)_s(0)=integral_0^infinity omega^n d nu_s(omega).
$

Thus bounded, open, and temporal questions are
different operations on one radial positive object and its typed pushforwards.  Their physical interpretations
remain different; the construction does not identify a ground pole with an
embedded excited state.

= Regression, transfer, and refusal <sec-transfer>

A generative interface must survive a changed input whose answer is not encoded in
the implementation.

== Massless spin ladder regression

For isotropic Gaussian smearing,
$abs(hat(f)(r))^2=exp(-(r/Lambda)^2)$, the curvature channel supplies

$
  q_s(r)=r/2,
  quad
  abs(a_s(r))^2=A_(s,e) r^(2 s),
  quad
  abs(h_s(r))^2=g_s^2 exp(-(r/Lambda)^2),
  quad
  epsilon_s(r)=r.
$

The pushforward density formula returns

$
  m_s(E)=frac(g_s^2 A_(s,e),2)
    E^(2 s+1) exp(-(E/Lambda)^2).
$

The rank-generated scalar, Maxwell, and spin-two channels are therefore visibly
different outputs of the same operation rather than one gravitational example:

$
  m_0(E)&=frac(g_0^2 A_(0,e),2)E exp(-(E/Lambda)^2),\
  m_1(E)&=frac(g_1^2 A_(1,e),2)E^3 exp(-(E/Lambda)^2),\
  m_2(E)&=frac(g_2^2 A_(2,e),2)E^5 exp(-(E/Lambda)^2).
$

The powers $1,3,5$ are computed from one shell power plus twice the generated
readout degrees $0,1,2$.  Scalar identity readout, Maxwell curvature, and the
spin-two curvature thus test the same compiler across the two rank boundaries
where gauge and trace operations first become admissible.

The honest cross-spin ratio retains the independent coupling normalizations:

$
  frac(m_2(E),m_1(E))
  =frac(g_2^2,g_1^2)frac(A_(2,e),A_(1,e))E^2.
$

Only in the compiler regression convention $g_2=g_1$ with equal detector norm
does this become $3E^2/5$.  That value tests curvature degree and angular
normalization; it is not a physical prediction comparing dimensionally unrelated
matter couplings.  No component polarization basis is used.

== Massive recoil transfer

The transfer case is chosen to challenge the operation, not to add another spin.
Its orbit measure is three-dimensional rather than null-shell, its energy is
massive and nonlinear in radius, and its threshold is not an odd power.  If the
same interface constructs this channel without receiving the answer density, the
portable object is the factor-to-pushforward operation rather than the massless
formula.

Spherical reduction of $d^3 k$ constructs $q(r)=4pi r^2$.  The named scalar
observable acts as the identity on the one-dimensional internal fiber, while the
declared Gaussian preparation and recoil dynamics supply the remaining factors:

$
  q(r)=4pi r^2,
  quad
  abs(a(r))^2=1,
  quad
  abs(h(r))^2=g^2 exp(-(r/Lambda)^2),
$
$
  epsilon(r)=sqrt(r^2+mu^2)+frac(r^2,2M).
$

Its derivative is

$
  epsilon'(r)=r(1/sqrt(r^2+mu^2)+1/M)>0
$

for $r>0$, so the same compiler admits it.  Near threshold,

$
  epsilon(r)=mu+c r^2+O(r^4),
  quad
  c=frac(1,2)(1/mu+1/M).
$

Substitute $r(E)=sqrt((E-mu)/c)+O((E-mu)^(3/2))$ into the pushforward density.  The result is

$
  q(r)abs(h(r))^2=4pi g^2 r^2+O(r^4),
  quad
  epsilon'(r)=2c r+O(r^3).
$

Dividing these constructed factors before replacing $r$ by its threshold inverse
gives

$
  m(mu+y)=frac(2pi g^2,c^(3/2))sqrt(y)+O(y^(3/2)).
$

The unchanged interface has transferred from a massless odd-power threshold to a
massive square-root threshold.  Both returned measures support an off-axis bound
transform and a continuum boundary transform.

== Refusal is part of the output

The scalar compiler refuses three distinct situations rather than hiding them:

- a detector with zero physical contraction is a blind channel;
- anisotropic angular weight returns a positive angular operator, not a scalar
  radial measure;
- a nonmonotone energy map requires a certified branch partition before the
  single-branch density formula can
  be used.

These refusals delimit the theorem and retain the unresolved structure needed by a
future extension.

== Dictionary to resolvents and graphs

The retained spectral operations have familiar names, but the dictionary keeps
their types visible:

#figure(
  table(
    columns: (1.25fr, 2fr),
    inset: 5pt,
    align: left + top,
    table.header([*Constructed object*], [*Standard role*]),
    [$B_"dep"=Q_"prep" H P_"prep"$], [prepared-sector coupling or form factor],
    [$Sigma_"dep"(z)$], [Feshbach--Schur self-energy],
    [$M_"dep"$], [coupling-weighted operator-valued spectral measure],
    [$nu_s(d omega)$], [radial coupling/form-factor measure],
    [$Gamma=2pi (d nu_s/d omega)(Omega)$],
      [leading golden-rule continuum coefficient],
  ),
  caption: [Spectral dictionary with preparation and energy types retained.],
) <tab-spectral-dictionary>

At order $g_s^2$, $Sigma_"dep"$ is also the operator form of the one-return
graph integral: depart once, propagate once in the free complementary sector, and
return once.  This paper has constructed exactly that graph content.  It has not
constructed Wick or CAR signs, graph symmetry factors, renormalization, overlapping
subdivergences, or higher-return resummation; those require a separate graph
compiler and cannot be inferred from the present resolvent notation.

= Complete-route verdict <sec-cost>

The construction separates several kinds of reduction that should not be
conflated.

#figure(
  table(
    columns: (1.25fr, 1.8fr, 1.75fr),
    inset: 5pt,
    align: left + top,
    table.header([*Reduction*], [*Supported gain*], [*Unpaid obligation*]),
    [semantic quotient],
      [removes gauge, trace, lower layers, and invisible channels],
      [exact only for the declared observable],
    [leading return],
      [vacuum departure occupies one-particle space],
      [later returns enter multiparticle sectors],
    [isotropy],
      [reduces the finite fiber to a radial measure],
      [anisotropy retains an angular operator],
    [transform reuse],
      [one cached measure supplies several transforms],
      [each transform retains cost and error],
    [channel count],
      [dense curvature propagation is smaller for $s>=3$],
      [runtime and conditioning remain unmeasured],
  ),
  caption: [What the complete route removes and what it leaves unresolved.],
) <tab-cost>

The reusable interface is

#align(center)[
  #set math.equation(numbering: none)
  $
    "CompileVisibleMeasure"(q,a,h,epsilon,W)
      &arrow.r (nu,epsilon_*nu,"transforms",\
      &quad "certificates" | "Refusal").
  $
]

It passes four different obligations: regression on the massless curvature
channel, transfer to the massive nonlinear recoil channel, use in bound and open
quantities, and refusal for an unpartitioned nonmonotone dispersion.  These tests
make it a retained tool rather than a proof that is discarded after recovering a
known equation.

= Supported theorem and frontier <sec-frontier>

#theorem[Observable-visible measure construction][
  Fix either the supported flat free scalar channel or a supported positive-integer-spin curvature channel and a supplied
  preparation and linear detector observable.  If the observable factors through
  the generated curvature, its response is independent of the constrained or
  compensated field presentation and is given by $G_Q K_s J$.  If the surviving
  one-particle channel has a finite reduced internal fiber, positive radial factor
  maps $(q,a,h)$, and a strictly monotone energy map $epsilon$, then the factor
  product constructs a positive radial coupling measure and each declared energy
  map constructs its spectral pushforward.  Their Stieltjes, continuum-
  boundary, finite-time, and Fourier transforms give the complete supported
  leading-return bound, open-channel, and memory quantities.  The same construction
  applies to the massless curvature and massive recoil inputs above.  Anisotropy or
  nonmonotonicity returns the corresponding retained operator or branch obligation
  rather than an unjustified scalar measure.
] <thm-visible-measure>

The strongest statement of the theorem is not that representation theory solves a
Hamiltonian. Rather, representation and locality construct admissible physical
channels and the annihilators used by the observable quotient. Dynamics, preparation, and
measurement then determine which positive spectral object is relevant.  The
  radial coupling measure, together with the preparation energy map, is the semantic invariant across the several supported queries; the field
equation is construction substrate.

The current research horizon stops here.  The following require new obstructions
and cannot be added as stronger adjectives:

- finite-coupling control of the dressed cyclic Fock sector;
- a physically derived matter interaction rather than the effective detector;
- a fermionic CAR departure-measure and graph compiler consuming the free
  Clifford branch constructed above;
- anisotropic operator-valued measures or automatically constructed energy
  branches;
- noncommuting, curved, or interacting dynamics where $K_s G_Q=G_Q K_s$ fails;
- incoming asymptotic channels and a normalized scattering matrix;
- measured runtime or conditioning improvement for a declared discretization;
- a publication-novelty claim established by focused literature comparison.

The #link("poincare-to-free-fields.pdf")[baseline representation paper] retains the
detailed construction of physical fibers and free local complexes.  The
#link("field-equations-to-computable-observables.md")[Markdown exploration
companion] retains the failed universal-solver search, mechanics/field comparison,
collective branches, and finite-coupling probes.  They are not discarded; they are
kept outside this deduction so the reusable generator remains visible.

#bibliography("poincare-to-free-fields.bib")

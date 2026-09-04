#import "../lib.typ": *
#import "@preview/physica:0.9.8": *
#import theorion: *

#show: daily-en.with(
  title: [From Poincare Representations to Local Free Fields],
  abstract: [
    Poincare symmetry classifies a one-particle state representation, under
    positive energy and irreducibility assumptions, by a momentum orbit and a
    representation of the stabilizer of one standard momentum. It does not select
    a unique covariant carrier or field equation. This paper constructs the
    missing realization bridge: from a massive-spin or massless-helicity fiber to
    a covariant Lorentz carrier, then to an equivariant local symbol or
    differential complex whose physical kernel/quotient recovers that fiber. The
    local construction is uniform for every separate finite integer or
    half-integer spin. For the parity-paired massless symmetric potential families,
    its causal and positive-frequency completion yields a source-generated free
    CCR or CAR field and recovers the same physical shell vector by one field
    application to the vacuum. Parity choices, real fermion forms, interactions,
    full induced-space density, and a completed countable-spin tower require
    additional input and are not consequences of the classification theorem.
  ],
  keywords: (
    "Poincare representations",
    "free fields",
    "finite spin",
    "helicity",
    "gauge complexes",
  ),
)

#show: show-theorion

= Problem and determination boundary <sec-problem>

The paper answers a realization question rather than an eigenvalue-classification
question:

#align(center)[
  _Given a physical Poincare representation, which covariant local construction
  has precisely that representation as its physical solution space?_
]

Fix four-dimensional Minkowski spacetime and the proper orthochronous Poincare
group, using its spin cover when necessary. The physical input is a strongly
continuous, positive-energy, irreducible one-particle representation whose
translation spectrum lies on one positive-mass orbit or one future null orbit. In
the massless case we retain finite helicity and exclude continuous-spin sectors.
This is the Wigner classification contract in the declared spectral regime
@wigner1939.

The spectral and irreducibility assumptions reduce the physical classification to

$
  (cal(O)_k, sigma),
$

where $cal(O)_k$ is the momentum orbit through a chosen standard momentum $k$ and
$sigma$ is an irreducible unitary representation of the subgroup that fixes $k$.
This pair specifies the on-shell state content. A field realization additionally
requires a Lorentz carrier, an intertwining map, an equation or differential
complex, a physical kernel or quotient, and analytic completion data.

#proposition[Determination boundary][
  Poincare symmetry determines the scoped one-particle
  representation up to equivalence. It does not uniquely determine a carrier,
  differential order, potential or curvature description, gauge redundancy,
  parity completion, reality condition, action, interaction, or observable.
] <prop-determination-boundary>

Consequently, covariance of an equation is only the first check. The decisive
check is semantic recovery: the standard-momentum solution fiber, after quotienting
gauge directions when present, must carry the original stabilizer representation;
the transported global solution space must then intertwine the original Poincare
action.

The argument is organized by the objects it constructs:

#align(center)[
  $
    (cal(O)_k, sigma)
    arrow.r
    V_sigma
    arrow.r
    F
    arrow.r
    (R(p), D(p))
    arrow.r
    (ker D(k)) / (im R(k))
    arrow.r
    cal(H)_(cal(O), sigma).
  $
]

@sec-particle-data through @sec-realization construct the physical fiber, carrier, and global realization map.
@sec-local-complexes constructs finite-spin local equations and complexes. @sec-causal-completion adds
causal, positive-frequency, and free quantum completion. @sec-low-spin checks familiar
low-spin descriptions against the general construction. @sec-equivalence-outlook identifies
which stronger equivalences and interacting claims require new presumptions.

= Physical representation data <sec-particle-data>

The construction uses three spaces with different jobs. The physical particle
space is unitary and on shell. A covariant field has values in one fixed Lorentz
carrier and is generally off shell before equations and quotients are imposed.
Scalar functions on the full Poincare group may package carrier components, but
they are not automatically either of the first two spaces. We first construct the
physical space that every later field must recover.

== Translations construct momentum

Let $V$ be real translation space with Minkowski form $eta$, and let $L_("spin")$
be the connected spin cover of the proper orthochronous Lorentz group. The affine
composition law, evaluated on the same event, is

$
  (a,A)(b,B)=(a+Lambda(A)b,A B).
$

We therefore work with $G=V times.r L_("spin")$. Preservation of transition
probabilities first supplies a projective unitary action on state rays. The
standard lifting theorem, under strong continuity, replaces it by an ordinary
unitary representation $U$ of the spin-covered group. This is a theorem contract:
the spin cover removes the projective rotation ambiguity; it does not choose a
field carrier @bargmann1954.

Restrict $U$ to a translation line $t e_mu$. Strong continuity and the group law
give a unique self-adjoint generator $P_mu$ through Stone's theorem @stone1932,

$
  U(t e_mu)=exp(i t P_mu),
  quad
  P_mu psi=1/i lim_(t arrow.r 0)
    (U(t e_mu)psi-psi)/t,
$

where the second expression defines the generator domain. The exponential is not
a formal expansion: it is spectral calculus. Because translations commute, their
spectral projections commute, and the joint spectral theorem @reed-simon1980
constructs one
projection-valued measure $E$ on $V^*$ such that

$
  U(a)=integral_(V^*) exp(i p dot a) dif E(p)
      =exp(i a^mu P_mu),
  quad
  P_mu=integral_(V^*) p_mu dif E(p).
$

Thus a momentum is a joint spectral value of translations. The Lorentz action on
momenta is forced by preservation of the translation pairing:

$
  (A dot p)(a):=p(Lambda(A)^(-1)a),
  quad
  (A dot p)(Lambda(A)a)=p(a).
$

Conjugating one translation by $U(A)$ and applying spectral uniqueness to the same
operator gives

$
  U(A) E(Delta) U(A)^(-1)=E(A dot Delta).
$

Hence the spectral support is Lorentz invariant. The one-particle hypothesis adds
the nontrivial restriction that the support lies on one orbit

$
  cal(O)_k={A dot k mid A in L_("spin")}.
$

For $k=(m,0,0,0)$, $m>0$, Lorentz invariance gives

$
  cal(O)_m^+={p mid p^2=m^2, p^0>0}.
$

The reverse inclusion is constructive: for any $p$ in the displayed set, the boost
with velocity $bold(v)=bold(p)/p^0$ sends $k$ to $p$. The mass shell is therefore
the orbit of the rest momentum; it has not been introduced as a field equation.
For $m=0$, the corresponding orbit is the future null cone with its vertex removed.

Restricting invariant four-volume to either positive shell constructs

$
  dif mu_m(p)
    =dif^4 p delta(p^2-m^2) theta(p^0)
    =dif^3 bold(p)/(2 E_bold(p)),
  quad
  E_bold(p)=sqrt(m^2+abs(bold(p))^2).
$

The factor $1/(2E_bold(p))$ is the Jacobian obtained by integrating the positive
root of the delta distribution. Existence is explicit; uniqueness up to scale is
the invariant-measure theorem contract for these transitive orbits.

== Residual frames construct the internal fiber

Choose a measurable transport $B(p)$ satisfying $B(p) dot k=p$. This choice cannot
be unique. If $B_1(p)$ and $B_2(p)$ reach the same momentum, direct evaluation gives

$
  [B_1(p)^(-1) B_2(p)] dot k
    =B_1(p)^(-1) dot p
    =k.
$

The ambiguity itself therefore constructs the subgroup

$
  K_k={r in L_("spin") mid r dot k=k}.
$

We call $K_k$ the stabilizer or little group only after this calculation. An
internal amplitude at $k$ must transform under this unavoidable residual change of
frame. Let $sigma:K_k arrow.r U(V_sigma)$ be its irreducible unitary action.

The fibers at all momenta are constructed without fixing $B$. Identify pairs by

$
  (A r,v) tilde (A,sigma(r)v),
  quad r in K_k,
$

and define

$
  cal(E)_sigma=(L_("spin") times V_sigma)/tilde
    arrow.r cal(O)_k,
  quad
  [A,v] mapsto A dot k.
$

This is well defined because $(A r) dot k=A dot k$. A standard transport merely
expresses a bundle section as $[B(p),psi(p)]$. If
$B'(p)=B(p)r(p)$, equality of the same bundle element computes

$
  psi'(p)=sigma(r(p))^(-1)psi(p).
$

The coordinate changes; the state does not.

== The induced state representation

To transport a state under $A$, fix the output momentum $p$ and construct the
required input $q=A^(-1) dot p$. Both $A B(q)$ and $B(p)$ carry $k$ to $p$:

$
  [A B(q)] dot k=A dot q=p,
  quad B(p) dot k=p.
$

Their relative transformation is therefore

$
  w(A,p)=B(p)^(-1) A B(A^(-1) dot p).
$

It belongs to $K_k$ by the same-input computation

$
  w(A,p) dot k
    =B(p)^(-1) dot [A dot (B(q) dot k)]
    =B(p)^(-1) dot p
    =k.
$

For $q=A_1^(-1) dot p$, cancellation of the middle transport proves the cocycle
identity

$
  w(A_1,p) w(A_2,q)
    =B(p)^(-1) A_1 A_2 B((A_1 A_2)^(-1) dot p)
    =w(A_1 A_2,p).
$

The square-integrable sections of $cal(E)_sigma$ form

$
  cal(H)_(cal(O),sigma)
    =L^2(cal(O)_k,dif mu_cal(O);V_sigma).
$

The three already constructed operations—translation character, momentum
pullback, and residual-frame conversion—then define

$
  [U_("ind")(a,A)psi](p)
    =exp(i p dot a)
      sigma(w(A,p))
      psi(A^(-1) dot p).
$

Evaluation on one $psi$ proves the group law. If $q=A_1^(-1) dot p$, then
$q dot b=p dot Lambda(A_1)b$ and the cocycle identity above give

$
  U_("ind")(a,A_1) U_("ind")(b,A_2)
    =U_("ind")(a+Lambda(A_1)b,A_1 A_2).
$

Unitarity is equally explicit: the phase has unit modulus, $sigma$ is unitary, and
the invariant measure permits $q=A^(-1) dot p$,

$
  norm(U_("ind")(a,A)psi)^2
    =integral_cal(O) norm(psi(A^(-1) dot p))^2 dif mu_cal(O)(p)
    =norm(psi)^2.
$

Conversely, the imprimitivity theorem @mackey1949 identifies the original one-orbit
representation, together with its covariant spectral measure, with this induced
representation. Its exact hypotheses—unitarity, covariance of $E$, transitive
support, and the stated regularity—are part of the theorem contract.

== Massive spin and massless helicity

For massive $k=(m,0,0,0)$, every stabilizer element fixes the time axis and acts
orthogonally on the Euclidean rest space $k^perp$. Conversely, any proper rotation
of $k^perp$ extends by fixing $k$. Thus the stabilizer is $"SO"(3)$ and its inverse
image in the spin cover is $"SU"(2)$.

Let $J_i$ be the self-adjoint infinitesimal generators of an irreducible finite
fiber, with $J_+ = J_1+i J_2$ and $J_- = J_1-i J_2$. If $s$ is the largest
$J_3$ eigenvalue, then $J_+v_s=0$. The invariant operator satisfies

$
  J^2=J_-J_+ + J_3(J_3+1),
  quad
  J^2 v_s=s(s+1)v_s.
$

For a weight vector $v_m$, positivity computes

$
  norm(J_-v_m)^2
    =(s+m)(s-m+1) norm(v_m)^2.
$

The chain therefore terminates with weights $s,s-1,dots,-s$; hence
$2s in bb(N)_0$, and the physical fiber $V_s$ has dimension $2s+1$. This
residual rest-frame action, rather than a tensor rank, is the meaning of massive
spin.

For nonzero null $k$, the metric on $k^perp$ has radical $"span"(k)$. Removing the
direction that has zero pairing with the entire transverse space constructs the
oriented Euclidean screen

$
  Q_k=k^perp/"span"(k),
  quad
  innerproduct(overline(x),overline(y))_Q=-eta(x,y).
$

Every Lorentz stabilizer element acts on this quotient. To construct the kernel of
that action, choose a representative $xi in k^perp$ of $q=[xi] in Q_k$ and define

$
  N_q(v)
    =v+(k dot v)xi
      -[xi dot v+(xi^2/2)(k dot v)]k.
$

Replacing $xi$ by $xi+a k$ leaves this map unchanged. Direct substitution gives

$
  eta(N_q u,N_q v)=eta(u,v),
  quad N_q k=k,
  quad [N_q x]=[x],
  quad N_q N_r=N_(q+r).
$

Conversely, if a stabilizer element acts trivially on $Q_k$, choose any $n$ with
$k dot n=1$ and assign it $[a n-n]$. Changing $n$ changes this vector only by
$"span"(k)$, and metric preservation reconstructs $a=N_[a n-n]$. Hence the kernel
has been computed, giving the exact sequence

$
  1 arrow.r (Q_k,+) arrow.r^(N) K_k
    arrow.r "Spin"(Q_k) arrow.r 1.
$

The normal group $(Q_k,+)$ is Abelian. In a finite-dimensional unitary fiber its
joint character spectrum is finite, but conjugation by screen rotations rotates
that spectrum. Every nonzero character has an infinite circular orbit. Therefore
only the zero character remains, $sigma(N_q)=1$, and the physical representation
factors through $"Spin"(2)$. Its irreducible characters are

$
  sigma_h(theta)=exp(i h theta),
  quad h in 1/2 bb(Z).
$

The resulting one-dimensional fiber $bb(C)_h$ is helicity $h$. A nonzero
translation character produces the excluded infinite-dimensional continuous-spin
branch. Pairing $h$ with $-h$ requires parity or a reality condition and is not
implied by the connected Poincare group.

#remark[Section output][
  The particle datum supplied downstream is
  $(cal(O)_m^+,V_s)$ for massive spin or $(cal(O)_0^+,bb(C)_h)$ for massless
  helicity, together with the induced unitary action constructed above. A field
  represents this particle only if its standard-momentum physical fiber is
  isomorphic as a $K_k$ representation—not merely equal in dimension.
]

= Covariant Lorentz carriers <sec-lorentz-carriers>

A finite Lorentz carrier is introduced because a local field must compare values at
different spacetime points in one fixed component space. It is not itself the
unitary particle fiber: finite nontrivial Lorentz carriers are nonunitary and often
contain several rest spins. We construct both their two labels and the maps that
select the @sec-particle-data fiber.

== Lorentz motions split invariantly

An infinitesimal metric-preserving motion is an endomorphism $X$ satisfying

$
  eta(X u,v)+eta(u,X v)=0.
$

The metric turns a bivector into exactly such a motion,

$
  M(u and v)x=eta(v,x)u-eta(u,x)v.
$

Substitution verifies the metric identity. Nondegeneracy and equal dimension make
$M:"Λ"^2 V arrow.r frak("so")(V,eta)$ an isomorphism, while

$
  A M(alpha) A^(-1)=M(("Λ"^2 A)alpha)
$

shows that both sides describe the same transformed motion.

Metric and orientation construct the Hodge operator by

$
  beta and star alpha=innerproduct(beta,alpha)_eta "vol".
$

On bivectors in signature $(1,3)$, $star^2=-1$. After complexification, its two
spectral projectors are

$
  P_+=(1-i star)/2,
  quad P_-=(1+i star)/2.
$

Computing from $star^2=-1$ gives

$
  P_+^2=P_+,
  quad P_-^2=P_-,
  quad P_+P_-=0,
  quad P_++P_-=1.
$

Every proper oriented Lorentz transformation preserves the defining metric and
volume form, so $star ("Λ"^2 A)=("Λ"^2 A) star$. The two images are therefore
ideals. Since they are complementary, their bracket lies in their zero
intersection:

$
  frak("so")(V,eta)_bb(C)=frak(g)_+ plus.o frak(g)_-,
  quad [frak(g)_+,frak(g)_-]=0.
$

The classification theorem for three-dimensional complex simple Lie algebras
identifies each ideal with $frak("sl")(2,bb(C))$. The calculation above—not a list of
rotation and boost components—explains why there are two commuting chiral actions.
This Hodge splitting is special to four dimensions because only there does $star$
map bivectors to bivectors.

== The spin cover constructs the vector carrier

Let $S$ be a complex two-space equipped with a nonzero alternating form $epsilon$.
The transformations preserving $epsilon$ form $"SL"(S)$. Its conjugate action on the
real space $"Herm"(S)$ of Hermitian elements of $S times.o bar(S)$ is

$
  lambda(A)P=(A times.o bar(A))P.
$

The form $epsilon times.o bar(epsilon)$ constructs the real quadratic form
$q(P)=det(P)$, and preservation of $epsilon$ gives
$q(lambda(A)P)=q(P)$. If $lambda(A)$ fixes every Hermitian element, it fixes every
rank-one ray; hence $A=c 1$, and $det A=1$ yields $c=plus.minus 1$. Dimension,
connectedness, and injectivity of the derivative then give the double cover

$
  lambda:"SL"(S) arrow.r "SO"^+("Herm"(S),q),
  quad ker lambda={plus.minus 1}.
$

Choose an orientation- and time-orientation-preserving isometry
$iota:V arrow.r "Herm"(S)$. Uniqueness of the connected spin cover supplies
$c:L_("spin") arrow.r "SL"(S)$ with the commuting witness

$
  iota(Lambda(g)v)=lambda(c(g))iota(v).
$

Both sides are the same transformed spacetime vector. The choice of $iota$ is a
spin-frame convention; changing it conjugates the construction but does not alter
the carrier multiplicities or physical fibers.

== Finite carriers and massive restriction

Functorial symmetric powers now construct the finite complex carriers

$
  F_(m,n)="Sym"^m(S) times.o "Sym"^n(bar(S)),
  quad (j_L,j_R)=(m/2,n/2),
  quad m,n in bb(N)_0.
$

Their representation law follows from functoriality; no generator expansion is
needed. The finite highest-weight theorem is used only as a contract stating that
every finite-dimensional irreducible complex Lorentz carrier is of this form
@fulton-harris1991.

At massive rest, the positive Hermitian vector $iota(k)$ identifies $bar(S)$ with
$S$ equivariantly under $K_k tilde.equiv "SU"(2)$. Calling the resulting fundamental
module $W$ gives

$
  Res_(K_k) F_(m,n)
    ="Sym"^m(W) times.o "Sym"^n(W).
$

Let $Omega=epsilon^(-1) in "Λ"^2 W$. The symmetric-algebra coproduct has a
bidegree component

$
  Delta_(a,b):"Sym"^(a+b)(W)
    arrow.r "Sym"^a(W) times.o "Sym"^b(W).
$

It distributes one symmetric tensor between the two carrier factors. Multiplying
the output by $Omega^r$ then constructs, for $0<=r<=min(m,n)$,

$
  I_r:"Sym"^(m+n-2r)(W)
      arrow.r "Sym"^m(W) times.o "Sym"^n(W),
  \
  I_r(f)=Omega^r dot Delta_(m-r,n-r)(f).
$

The map is nonzero and $"SU"(2)$ equivariant because $Omega$, coproduct, and
symmetric multiplication are equivariant. The Clebsch--Gordan theorem contract
@fulton-harris1991, checked by

$
  sum_(r=0)^min(m,n) [m+n-2r+1]=(m+1)(n+1),
$

then yields the multiplicity-free restriction

$
  Res_(K_k)F_(m,n)
    tilde.equiv
    "Sym"^(m+n)(W) plus.o "Sym"^(m+n-2)(W)
      plus.o dots plus.o "Sym"^abs(m-n)(W).
$

Thus the massive spins present are

$
  s=abs(m-n)/2, abs(m-n)/2+1,dots,(m+n)/2,
$

and the actual map passed downstream is
$j_s^(m,n)=I_r:V_s arrow.r F_(m,n)$. In the chiral carrier $F_(2s,0)$ this
map is the identity and no lower rest spin occurs.

== Null restriction and the direct helicity line

For future-null $k$, positivity and $det(iota(k))=0$ construct a rank-one element

$
  iota(k)=lambda_0 times.o bar(lambda_0),
$

and hence a line $ell="span"(lambda_0) subset S$. The null stabilizer preserves this
line. Its translation-like normal subgroup acts identically both on $ell$ and on
$S/ell$; through the commuting vector--spinor witness above, it is the same
subgroup $(Q_k,+)$ constructed in @sec-particle-data.

It therefore fixes the extremal line

$
  L_(m,n)="Sym"^m(ell) times.o "Sym"^n(bar(ell))
    subset F_(m,n).
$

If the residual screen rotation by $theta$ acts on $ell$ as
$z=exp(-i theta/2)$, its action on this line is

$
  z^m bar(z)^n=exp(i(n-m)theta/2).
$

Consequently line inclusion constructs a little-group intertwiner

$
  j_h^(m,n):bb(C)_h arrow.r F_(m,n),
  quad h=(n-m)/2.
$

This is a direct single-helicity realization. Potential descriptions need not
contain the physical helicity as a literal subspace; their fiber is instead a
kernel modulo a gauge image, constructed in @sec-realization.

#remark[Section output][
  For each directly occurring massive spin or massless
  helicity, the construction exports
  $(F_(m,n),Res_(K_k)F_(m,n),j_sigma)$ with an explicit $K_k$ intertwiner.
  Occurrence inside a carrier does not yet provide a local equation, a positive
  norm on the whole carrier, or a gauge resolution.
]

= The realization theorem <sec-realization>

The particle fiber $V_sigma$ and a Lorentz carrier $F$ live in different
representation spaces. The carrier describes the particle only when an explicit
map preserves the residual-frame action and remains well defined over the entire
momentum orbit.

== Ordinary orbitwise realization <sec-orbitwise-realization>

Let $rho:L_("spin") arrow.r "GL"(F)$ be a carrier action. Suppose @sec-lorentz-carriers has
constructed an injective map $j:V_sigma arrow.r F$ satisfying

$
  j sigma(r)=rho(r)j,
  quad r in K_k.
$

On the associated-bundle representative $[A,v]$, define

$
  cal(J)_j[A,v]=(A dot k,rho(A)j(v)).
$

The quotient also represents this input as $[A r,v]=[A,sigma(r)v]$. Evaluating
$cal(J)_j$ on both representatives gives

$
  cal(J)_j[A r,v]
    =(A dot k,rho(A)rho(r)j(v))
    =(A dot k,rho(A)j sigma(r)v)
    =cal(J)_j[A,sigma(r)v].
$

This equality is the well-definedness witness. Conversely, an equivariant map over
the orbit is fixed by its value above $k$, and that value must satisfy the same
stabilizer identity. Ordinary orbitwise realizations are therefore classified by

$
  "Hom"_(K_k)(V_sigma,"Res"_(K_k)F).
$

Using the standard transport only for coordinates, the resulting field amplitude
is

$
  [cal(W)_j psi](p)=rho(B(p))j psi(p).
$

If $B'(p)=B(p)r(p)$, the same state has
$psi'(p)=sigma(r(p))^(-1)psi(p)$, and the two field expressions coincide:

$
  rho(B'(p))j psi'(p)
    =rho(B(p))rho(r(p))j sigma(r(p))^(-1)psi(p)
    =rho(B(p))j psi(p).
$

To verify covariance, put $q=A^(-1) dot p$ and use the already constructed
$w(A,p)=B(p)^(-1)A B(q)$. Evaluation on the same wavefunction gives

$
  rho(A)[cal(W)_j psi](q)
    =rho(B(p))rho(w(A,p))j psi(q)
    =rho(B(p))j sigma(w(A,p))psi(q).
$

The right-hand side is $cal(W)_j$ applied to the Lorentz part of the induced state
action. Translations multiply both sides by the same phase $exp(i p dot a)$.
Therefore

$
  cal(W)_j U_("ind")(g)=T_rho(g)cal(W)_j.
$

The physical inner product is transported through $cal(W)_j$; it is not presumed
to be a momentum-independent positive form on the nonunitary finite carrier.

== Gauge realization as physical cohomology

A potential may contain no invariant copy of $V_sigma$ before redundant directions
are removed. At the standard momentum, construct a $K_k$-equivariant complex

$
  G arrow.r^(R_k) F arrow.r^(D_k) E,
  quad D_k R_k=0.
$

The first identity puts $im R_k$ inside $ker D_k$, so the stabilizer acts on the
physical quotient

$
  H_k=(ker D_k)/(im R_k).
$

The potential describes the desired particle precisely when an explicit
intertwining isomorphism $bar(j):V_sigma tilde.equiv H_k$ has been constructed.

Assume $G,F,E$ are restrictions of Lorentz carriers with actions
$rho_G,rho_F,rho_E$. Transport the maps to $p$ by

$
  R_p=rho_F(B(p))R_k rho_G(B(p))^(-1),
  quad
  D_p=rho_E(B(p))D_k rho_F(B(p))^(-1).
$

If $B'(p)=B(p)r$, equivariance computes on the same input

$
  rho_F(B r)R_k rho_G(B r)^(-1)
    =rho_F(B)[rho_F(r)R_k rho_G(r)^(-1)]rho_G(B)^(-1)
    =R_p,
$

and the identical calculation applies to $D_p$. Thus the maps and their quotient
do not depend on the chosen standard transport. Their complex relation is also
preserved by direct composition:

$
  D_p R_p
    =rho_E(B(p))[D_k R_k]rho_G(B(p))^(-1)
    =0.
$

Transporting $bar(j)$ by the associated-bundle construction of
@sec-orbitwise-realization then
gives

$
  cal(H)_(cal(O),sigma)
    tilde.equiv
    "positive-energy sections of" (ker D_p)/(im R_p),
$

before analytic completion. An ordinary carrier is the special case with no gauge
image. Added auxiliary fields are harmless only when their added complex is exact.

== Locality and analytic completion are additional obligations

The orbitwise construction is algebraic and on shell. A finite-order spacetime
equation exists only if the transported maps extend away from the orbit as
Lorentz-equivariant polynomial symbols

$
  R(p):G arrow.r F,
  quad D(p):F arrow.r E,
  quad D(p)R(p)=0.
$

At $p=k$, their cohomology must still be $V_sigma$, and their characteristic set
must be stated. A rational or merely measurable extension may realize the same
orbit representation without defining a local differential operator. Carrier
occurrence alone therefore does not imply locality.

An equivalence of completed physical spaces further requires the invariant orbit
measure, measurable bundle data, closed kernels and gauge images or an explicitly
declared distributional quotient, and a positive quotient pairing. On a dense
domain the required norm witness is

$
  innerproduct(cal(W)psi,cal(W)chi)_("field")
    =innerproduct(psi,chi)_("ind").
$

The later causal construction supplies this pairing for the finite families it
treats. @sec-realization does not infer it from the algebraic intertwiner.

== Group functions are downstream packaging

For a cyclic covector $lambda in F^*$, a covariant field may be encoded by

$
  [cal(C)_(rho,lambda)Phi](x,B)
    =lambda(rho(B^(-1))Phi(x)).
$

Cyclicity makes this coefficient map injective: if all frame readings vanish, all
covectors in the orbit span annihilate $Phi$, hence $Phi=0$. Evaluating the left
Poincare action on the same field gives

$
  L_g cal(C)_(rho,lambda)Phi
    =cal(C)_(rho,lambda)T_rho(g)Phi.
$

This map points from a field to scalar coefficient functions. For a nontrivial
finite Lorentz carrier, those coefficients do not lie in the regular Hilbert space
$L^2(G)$: otherwise its Haar inner product would pull back to a forbidden
positive-definite Lorentz-invariant norm on $F$. The group-function representation
uses existence and uniqueness of Haar measure as a theorem contract @folland2016.
It is optional algebraic packaging, not an intermediate physical Hilbert
space and not a computational reduction unless a later observable has a cheaper
verified route through it.

#theorem[Orbitwise realization][
  A physical induced representation is realized
  by an ordinary carrier exactly through a stabilizer intertwiner
  $V_sigma arrow.r F$, or by a gauge carrier through a stabilizer-cohomology
  isomorphism $V_sigma tilde.equiv ker D_k/im R_k$. Associated-bundle transport
  constructs the global Poincare intertwiner. Polynomial locality, analytic
  completion, parity, reality, and an action are separate obligations.
] <thm-orbitwise-realization>

= Universal local finite-spin complexes <sec-local-complexes>

@sec-realization constructed an equivariant field bundle only on a momentum orbit. A
finite-order constant-coefficient equation requires more: its momentum symbol must
extend polynomially away from that orbit. We first state this locality obligation,
then construct two uniform solutions. The direct chiral family realizes one
massive spin or one massless helicity with the shortest symbol. The potential
families realize parity-paired massless helicities as gauge cohomology.

#remark[Construction contract][
  *Input:* the physical standard fiber and its explicit carrier intertwiner from
  @sec-realization. *Invariant:* the same little-group module must survive every
  extension and quotient. *Route:* test polynomial extendability; construct the
  direct chiral symbols; construct the bosonic and fermionic potential complexes;
  compute their cohomology on null, non-null, and zero-momentum strata. *Output:*
  a finite-family local realization theorem with its exceptional strata exposed.
  Action, causal inversion, positivity, and quantization remain obligations for
  @sec-causal-completion.
] <contract-local-complexes>

== Locality is a polynomial-extension problem

Let $X,Y$ be finite Lorentz carriers and let $V_bb(C)^*$ be complexified momentum
space. A Lorentz-equivariant polynomial symbol $a(p):X arrow.r Y$ of degree at
most $d$ is equivalently an element of the finite intertwiner space

$
  cal(P)_(<=d)(X,Y)
    ="Hom"_L(X,Y)
      plus.o "Hom"_L(V_bb(C) times.o X,Y)
      plus.o dots
      plus.o "Hom"_L("Sym"^d(V_bb(C)) times.o X,Y).
$

Evaluation at the standard momentum constructs

$
  "ev"_k:cal(P)_(<=d)(X,Y)
    arrow.r "Hom"_(K_k)(X,Y),
  quad "ev"_k(a)=a(k).
$

The codomain is forced by covariance: for $r in K_k$,

$
  a(k)rho_X(r)=a(r dot k)rho_X(r)=rho_Y(r)a(k).
$

Thus a desired fiber map has a degree-$d$ local extension only when it belongs to
$im "ev"_k$. For a bounded complex, the individual lifts must additionally obey
the polynomial identities $delta^(a+1)(p)delta^a(p)=0$ on every momentum. This is
the simultaneous syzygy obstruction. Orbitwise transport alone guarantees neither
condition.

Once a candidate complex is constructed, its characteristic cohomology is a rank
calculation. If $delta^(a-1)(p)$ enters $C^a$ and $delta^a(p)$ leaves it, then

$
  dim H^a(p)
    =dim C^a-rank(delta^(a-1)(p))-rank(delta^a(p)).
$

The minors of the two symbols therefore locate every momentum stratum on which
physical cohomology can appear. This test prevents an equation that works at $k$
from silently adding another mass shell or an unexplained zero-momentum sector.

The criterion is decisive only after carriers and degree bounds have been chosen.
Symmetry supplies no universal choice or uniqueness theorem for those data. The
families below establish existence by constructing their symbols explicitly.

== Direct chiral realization of every finite label

=== Massive spin

Fix $m>0$ and $s in 1/2 bb(N)_0$. @sec-lorentz-carriers constructed the chiral carrier

$
  F_s^("ch")="Sym"^(2s)(S),
$

whose restriction to the massive stabilizer is exactly $V_s$, with no lower rest
spin. The orbit equation itself constructs the quadratic scalar symbol

$
  D_(m,s)(p)=(p^2-m^2)1_(F_s^("ch")).
$

It is Lorentz equivariant because $p^2$ is invariant and the identity commutes with
the carrier action. Its fiber is computed without components:

$
  p^2!=m^2 => ker D_(m,s)(p)=0,
  quad
  p^2=m^2 => ker D_(m,s)(p)=F_s^("ch").
$

At rest the second kernel is precisely the spin-$s$ module already constructed.
@sec-realization therefore transports its positive-energy solutions into
$cal(H)_(cal(O)_m^+,s)$. With the Fourier convention
$Phi(x)=integral exp(-i p dot x) Phi_tilde(p) dif p$, the same plane wave satisfies
$i partial_mu exp(-i p dot x)=p_mu exp(-i p dot x)$, so the symbol becomes

$
  (square+m^2)Phi=0,
$

up to the declared metric convention. This is a local second-order complex chiral
realization. It is not a Dirac, Proca, or Fierz--Pauli presentation and supplies no
parity, reality, first-order factorization, or action by itself.

=== Massless helicity

For helicity zero, take the scalar carrier and symbol $D_0(p)=p^2$. For $h>0$, put
$n=2h$ and use $F_h="Sym"^n(S)$. The alternating form on $S$ turns
$x in S$ into the covector $x^flat$ defined by
$x^flat(y)=epsilon(x,y)$. Contraction by this covector gives

$
  iota_(x^flat):"Sym"^n(S) arrow.r "Sym"^(n-1)(S).
$

Define the natural map on a decomposable vector--spinor input by

$
  cal(C)_n((x times.o bar(y)) times.o phi)
    =iota_(x^flat)(phi) times.o bar(y).
$

@sec-lorentz-carriers constructed the complexified vector bridge
$iota_(bb(C)):V_bb(C) arrow.r S times.o bar(S)$. Evaluating $cal(C)_n$ on the
momentum factor therefore constructs the first-order symbol

$
  D_h(p)phi
    =cal(C)_n(iota_(bb(C))(p) times.o phi).
$

Every operation in this composite is natural, so
$D_h(A dot p)rho_h(A)=rho_("target")(A)D_h(p)$; polynomial degree one gives a
local first-order equation.

For nonzero null $k$, @sec-lorentz-carriers constructed
$iota_(bb(C))(k)=lambda times.o bar(lambda)$ and
$ell="span"(lambda)$. The covector $lambda^flat$ has kernel $ell$. Choose one
right inverse of $lambda^flat$ only to witness the symmetric-algebra exact sequence

$
  0 arrow.r "Sym"^n(ell)
    arrow.r "Sym"^n(S)
    arrow.r^(iota_(lambda^flat)) "Sym"^(n-1)(S)
    arrow.r 0.
$

Grading by the number of factors in the chosen complementary line proves
surjectivity and leaves exactly $"Sym"^n(ell)$ in the kernel. The sequence itself
is independent of that witness. Because $bar(lambda)$ is nonzero,

$
  ker D_h(k)="Sym"^n(ell).
$

This is the extremal line constructed in @sec-lorentz-carriers and carries one helicity, $-h$
in the chosen convention. Complex conjugation gives the opposite chirality and
helicity. If $p^2!=0$, the vector--spinor map defined by $p$ is invertible; then all
spinor contractions of a vector in $ker D_h(p)$ vanish, forcing that vector to
zero. The only nonzero characteristic orbit is therefore the null cone, apart from
its separately accounted origin.

Fourier substitution yields the familiar index form only after the invariant map
has been constructed:

$
  partial^(A A') phi_(A A_2 dots A_(2h))=0.
$

This is a gauge-free curvature realization. A potential requires a longer complex
because its physical helicity is not a literal carrier subspace before quotienting.

== Symmetric bosonic potential complex

A symmetric rank-$s$ tensor is equivalently a homogeneous polynomial $phi(u)$ of
degree $s$ in one auxiliary vector. This loses no tensor information and exposes
four invariant operations:

$
  P_p phi=(p dot u)phi,
  quad A_p phi=derivative_(t) phi(u+t p)|_(t=0), \
  T="trace",
  quad
  U="metric insertion".
$

Acting on the same polynomial verifies the commutators

$
  [A_p,P_p]=p^2,
  quad [T,P_p]=2A_p,
  quad [A_p,U]=2P_p.
$

For integer $s>=1$, construct the constrained carriers

$
  G_s=ker T subset "Sym"^(s-1)(V_bb(C)^*),
  quad
  F_s=ker T^2 subset "Sym"^s(V_bb(C)^*).
$

Define the gauge map and its compatible divergence by

$
  R_s(p)=P_p,
  quad
  C_s(p)=A_p-(1/2)P_p T.
$

For the same traceless parameter $epsilon$, the commutators compute

$
  C_s(p)R_s(p)epsilon
    =A_p P_p epsilon-(1/2)P_p T P_p epsilon
    =p^2 epsilon.
$

The equation is therefore the defect of the scalar wave symbol along the gauge
direction,

$
  D_s(p)=p^2 1_(F_s)-R_s(p) C_s(p)
    =p^2-P_p A_p+(1/2)P_p^2 T.
$

The common-input identity just proved gives

$
  D_s(p) R_s(p)
    =p^2 R_s-R_s C_s R_s
    =0.
$

The same commutator algebra verifies that $R_s$ maps $G_s$ into $F_s$ and $D_s$
preserves $F_s$. Thus

$
  G_s arrow.r^(R_s(p)) F_s arrow.r^(D_s(p)) F_s
$

is a Lorentz-equivariant polynomial complex of degrees one and two for every
finite integer $s$.

=== The null screen computes its physical cohomology

Let $k$ be nonzero and null. Because multiplication by the nonzero polynomial
$P_k(u)=k dot u$ is injective,

$
  D_s(k)phi=-P_k C_s(k)phi=0
  quad <=> quad
  C_s(k)phi=0.
$

Restrict $phi$ to the hyperplane $k^perp$, where $P_k=0$. The constraint says that
this restriction is constant along the radical $"span"(k)$, so it descends to a
homogeneous polynomial on the screen $Q_k$. Choose one null complement $n$ only
to verify the trace. Applying $A_n$ to the same constraint and using
$T=2A_k A_n+T_Q$ shows that the descended polynomial is screen-traceless. This
constructs the intrinsic map

$
  "res"_k:ker D_s(k)
    arrow.r "Sym"_0^s(Q_k times.o bb(C))^*.
$

Its kernel is exactly gauge. If $"res"_k(phi)=0$, polynomial divisibility by the
linear equation $P_k=0$ constructs a unique $psi$ with $phi=P_k psi$. Acting with
$C_s(k)$ on the same $psi$ gives

$
  0=C_s(k)phi=-(1/2)P_k^2 T psi.
$

The polynomial ring has no zero divisors, so $T psi=0$ and
$phi=R_s(k)psi$. Conversely, every gauge amplitude has the factor $P_k$ and
restricts to zero. Extending any trace-free screen polynomial constantly along a
chosen null pair gives a solution; changing that lift changes it only by the gauge
kernel already computed. Hence the sequence

$
  0 arrow.r G_s arrow.r^(R_s(k)) ker D_s(k)
    arrow.r^("res"_k) "Sym"_0^s(Q_k times.o bb(C))^*
    arrow.r 0
$

is exact and $K_k$ equivariant.

The screen metric and orientation split $Q_k times.o bb(C)$ into two rotation lines
$L_+ plus.o L_-$. Trace contracts one $L_+$ with one $L_-$, so its kernel on the
$s$th symmetric power consists only of the two endpoint lines. Therefore

$
  ker D_s(k)/im R_s(k)
    tilde.equiv
    "Sym"_0^s(Q_k times.o bb(C))^*
    tilde.equiv bb(C)_(+s) plus.o bb(C)_(-s).
$

For $p^2!=0$, $T C_s(p)=0$ on $F_s$, and the field equation itself reconstructs

$
  phi=R_s(p)[(1/p^2) C_s(p)phi].
$

Every non-null solution is consequently gauge. At $p=0$ both symbols vanish and
the full constrained carrier remains. The real characteristic set is exactly the
null cone: future and past orbits plus this exceptional origin. Positive energy
selects the future orbit. At $s=1$ the complex is Maxwell; at $s=2$ it is the
symmetric metric-potential complex, but neither special case carries the proof.

== Symmetric half-integer potential complex

The spinor construction uses the same polynomial carrier and replaces trace by an
internally constructed Clifford contraction. @sec-lorentz-carriers gives
$V_bb(C) tilde.equiv S times.o bar(S)$. On
$Delta=S plus.o bar(S)$, put the two vector--spinor maps in opposite chiral blocks
and call the result $gamma(v)$. Polarizing the determinant form computes

$
  gamma(v)gamma(w)+gamma(w)gamma(v)
    =2eta(v,w)1_Delta.
$

Gamma matrices are coordinate representatives of this map and are not used here.

For a degree-$n$ $Delta$-valued polynomial $psi(u)$, construct

$
  "Slash"_p=gamma(p),
  quad
  Gamma=gamma dot partial_u,
$

along with the already defined $P_p,A_p,T$. Evaluation on the same polynomial
first gives the two quadratic relations

$
  "Slash"_p^2=p^2,
  quad [A_p,P_p]=p^2.
$

The contraction map is compatible with multiplication and Clifford action by

$
  [Gamma,P_p]="Slash"_p,
  quad Gamma^2=T,
$

$
  Gamma "Slash"_p+"Slash"_p Gamma=2A_p.
$

For $n>=1$, define

$
  G_n=ker Gamma
    subset "Sym"^(n-1)(V_bb(C)^*) times.o Delta,
  quad
  F_n=ker Gamma^3
    subset "Sym"^n(V_bb(C)^*) times.o Delta,
$

and the degree-one symbols

$
  R_n(p)=P_p,
  quad
  S_n(p)="Slash"_p-P_p Gamma.
$

If $Gamma epsilon=0$, repeated use of
$Gamma P_p=P_p Gamma+"Slash"_p$ gives $Gamma^3(P_p epsilon)=0$, so $R_n$ has the
stated target. The equation-gauge composite reduces to

$
  S_n(p) R_n(p)epsilon=-P_p^2 Gamma epsilon=0.
$

For $n=0$, take $F_0=Delta$, omit the gauge carrier, and use the ordinary symbol
$S_0(p)="Slash"_p$.

=== The spinor screen computes helicity

Fix nonzero null $k$. From $S_n(k)psi=0$, applying $"Slash"_k$ and then $Gamma$
on the same field gives

$
  "Slash"_k Gamma psi=0,
  quad
  2A_k psi=P_k Gamma^2 psi.
$

On $k^perp$, the second identity makes the restriction constant along
$"span"(k)$; the equation itself puts its spinor value in

$
  W_k=ker("Slash"_k:Delta arrow.r Delta).
$

Differentiating once along a null complement constructs the remaining intrinsic
screen constraint $Gamma_Q r=0$. Thus restriction gives

$
  "res"_k:ker S_n(k) arrow.r cal(S)_n(Q_k,W_k),
$

where

$
  cal(S)_n(Q_k,W_k)
    ={r in "Sym"^n(Q_k times.o bb(C))^* times.o W_k
      mid Gamma_Q r=0}.
$

As in the bosonic case, zero restriction means divisibility:
$psi=P_k epsilon$. Applying the already computed composite yields

$
  0=S_n(k)psi=-P_k^2 Gamma epsilon,
$

so $epsilon in G_n$. A constant extension of screen data proves surjectivity, and
different null complements change the extension only by this gauge kernel. Hence

$
  0 arrow.r G_n arrow.r^(R_n(k)) ker S_n(k)
    arrow.r^("res"_k) cal(S)_n(Q_k,W_k) arrow.r 0
$

is an exact $K_k$ sequence.

To evaluate its last term, choose the two isotropic rotation lines
$Q_k times.o bb(C)=L_+ plus.o L_-$. The null Clifford relation constructs two
one-dimensional spinor lines $W_+,W_- subset W_k$ of weights $+1/2$ and $-1/2$.
Writing a degree-$n$ screen spinor as

$
  r=f_+(z_+,z_-)w_+ + f_-(z_+,z_-)w_-,
$

the invariant equation $Gamma_Q r=0$ evaluates to

$
  partial_(z_-)f_+=0,
  quad partial_(z_+)f_-=0.
$

Homogeneity then leaves

$
  r=alpha_+ z_+^n w_+ + alpha_- z_-^n w_-,
$

whose weights are $+(n+1/2)$ and $-(n+1/2)$. Consequently

$
  ker S_n(k)/im R_n(k)
    tilde.equiv
    bb(C)_(+(n+1/2)) plus.o bb(C)_(-(n+1/2)).
$

For $p^2!=0$, a solution constructs the gamma-traceless parameter

$
  epsilon=(1/p^2)"Slash"_p Gamma psi.
$

The triple-gamma constraint and the displayed operator algebra compute
$Gamma epsilon=0$ and $psi=P_p epsilon$. Thus non-null cohomology vanishes. At the
origin both symbols vanish, leaving the constrained carrier. The characteristic
set and positive-energy selection are therefore the same null strata as in the
bosonic family.

== What has and has not been constructed

For every separate finite label, @tab-local-families summarizes the checked route.

#figure(
  table(
    columns: (1.1fr, 1.2fr, 1.4fr, 1.5fr),
    inset: 5pt,
    align: left + top,
    table.header(
      [*Input*], [*Carrier*], [*Symbol/complex*], [*Physical fiber*],
    ),
    [massive $s$], [chiral $"Sym"^(2s)(S)$],
      [$p^2-m^2$], [$V_s$],
    [massless $h$], [chiral $"Sym"^(2h)(S)$],
      [first-order contraction], [$bb(C)_(-h)$; conjugate gives $+h$],
    [integer $s>=1$], [double-traceless symmetric potential],
      [$G_s arrow.r F_s arrow.r F_s$], [$bb(C)_(+s) plus.o bb(C)_(-s)$],
    [half-integer $n+1/2$], [triple-gamma-traceless spinor potential],
      [$G_n arrow.r F_n arrow.r "target"$],
      [$bb(C)_(+(n+1/2)) plus.o bb(C)_(-(n+1/2))$],
  ),
  caption: [Constructed finite-spin local realization families.],
) <tab-local-families>

These are finite-family existence theorems, not a completed infinite-spin field.
The potential complexes add parity pairing, redundant variables, and trace
constraints; they are not more fundamental than the direct curvature route.

Nor is a polynomial equation automatically an Euler equation or a propagator. An
action additionally requires an invariant nondegenerate pairing and a formally
self-adjoint representative. Causal computation additionally requires a hyperbolic
completion, source constraint, support theorem, and positive physical pairing.
Those constructions begin in @sec-causal-completion. Reality conditions, massive conventional
potentials, mixed-symmetry fields, interactions, and countable-spin completion
remain outside the present theorem.

#theorem[Finite-spin local realization][
  On four-dimensional Minkowski space,
  every separate finite massive spin and massless helicity has a local complex
  chiral realization. Every separate finite massless integer or half-integer
  helicity magnitude also has a parity-paired symmetric potential complex whose
  nonzero-null standard fiber, modulo gauge, is exactly the corresponding pair of
  little-group characters. Non-null cohomology vanishes; the origin is an explicit
  exceptional stratum. None of these realizations is selected uniquely by
  Poincare symmetry.
] <thm-finite-local-realization>

= Causal and quantum completion <sec-causal-completion>

A polynomial complex identifies its plane waves but does not select an inverse, a
causal boundary condition, a positive-frequency space, or a quantum state. This
section constructs those additional objects for the parity-paired massless
symmetric potential families of @sec-local-complexes. The same compact source class will be
followed through every step; changing its representation must not change its
physical shell amplitude.

The direct massive chiral systems remain valid local one-particle realizations, and
their scalar Klein--Gordon symbols have ordinary causal Green maps. The stronger
source-quotient, statistics, and recovery theorem below is claimed only for the
bosonic and fermionic massless potential complexes for which the pairing, gauge,
support, and positivity constructions have been established.

#remark[Construction contract][
  *Input:* one parity-paired potential complex and one compact admissible source
  from @sec-local-complexes. *Invariant:* the source must determine the identical
  physical shell vector after every representation change. *Route:* construct the
  dual pairing and Euler operator; reduce causal response to scalar Green maps;
  identify source and solution quotients; restrict to the future shell and complete
  its positive norm; then apply CCR or CAR functoriality. *Output:* a faithful
  source-generated one-particle and free-quantum realization. Density in the full
  abstract induced space, interactions, and observable prediction remain outside
  this contract.
] <contract-causal-completion>

== A field equation becomes an Euler equation only after duality

An action requires a nondegenerate invariant pairing on fields and a formally
self-adjoint representative of the equation. These data are not consequences of
the physical kernel alone.

=== Bosonic trace reversal

Complete Lorentz contraction constructs the Fischer pairing on symmetric tensors.
On the auxiliary-polynomial operations of @sec-local-complexes it gives

$
  P_p^dagger=A_p,
  quad U^dagger=T.
$

Compact support makes $p=i partial$ formally self-adjoint after spacetime
integration. On the double-traceless carrier $F_s$, define

$
  M_s=1-(1/4)U T,
  quad
  E_s=M_s D_s.
$

For $s>=2$, the trace decomposition $phi=h+U k$ with $T h=T k=0$ gives

$
  M_s h=h,
  quad M_s(U k)=(1-s)U k,
$

and therefore the executable inverse

$
  M_s^(-1)=1-[1/(4(s-1))]U T.
$

For $s=1$, traces vanish and $M_1=1$. Normal ordering with the three commutators
from @sec-local-complexes makes the self-adjointness defect factor through $T^2$; hence

$
  innerproduct(phi,E_s psi)=innerproduct(E_s phi,psi),
  quad phi,psi in F_s.
$

Because $M_s$ is invertible, $E_s phi=0$ and $D_s phi=0$ have the same vacuum
solutions. The constrained adjoint is obtained on one gauge parameter and field:

$
  innerproduct(R_s epsilon,M_s phi)
    =innerproduct(epsilon,C_s phi),
  quad
  R_s^dagger M_s=C_s.
$

Thus a compact source $J$ couples gauge-invariantly precisely when
$R_s^dagger J=0$. For the trace-reversed source $K=M_s^(-1)J$, the same identity
turns admissibility into $C_s K=0$.

=== Fermionic trace reversal

The invariant Dirac form on $Delta$ and complete Lorentz contraction construct the
Dirac--Fischer pairing. Its natural adjoints are

$
  P_p^dagger=A_p,
  quad Y^dagger=Gamma,
  quad "Slash"_p^dagger="Slash"_p,
$

where $Y$ multiplies by $gamma(u)$. Every triple-gamma-traceless rank-$n$ field has
the constructed three-layer decomposition

$
  psi=h_0+Y h_1+Y^2 h_2,
  quad Gamma h_j=0.
$

Define

$
  M_n=1-(1/2)Y Gamma-(1/4)Y^2 Gamma^2,
  quad
  E_n=M_n S_n.
$

Evaluation on those same layers gives

$
  M_n h_0=h_0,
  quad M_n(Y h_1)=-n Y h_1,
  quad M_n(Y^2h_2)=-n Y^2h_2.
$

Hence $M_0=1$ and $M_n$ is invertible for every $n>=1$ without a component
matrix. Normal ordering makes the adjoint defect vanish between fields in
$ker Gamma^3$, so $E_n$ is formally self-adjoint and has the same vacuum kernel
as $S_n$.

The operator that both detects gauge and completes the wave equation is

$
  B_n=A_p-(1/2)P_p Gamma^2-(1/2)"Slash"_p Gamma.
$

The Clifford algebra of @sec-local-complexes computes

$
  B_n S_n=0,
  quad
  B_n R_n=(1/2)p^2 1_(G_n),
  quad
  R_n^dagger M_n=B_n.
$

Thus $R_n^dagger J=0$ becomes $B_n M_n^(-1)J=0$. A real Grassmann or Majorana
action would require an additional real-form convention; the complex
formal-adjoint construction does not select one.

== Hyperbolic completion constructs causal response

The bosonic identities already have the homotopy form

$
  C_s R_s=p^2 1_(G_s),
  quad
  D_s+R_s C_s=p^2 1_(F_s).
$

The fermionic equation is first order, so one composition is required:

$
  S_n^2+2R_n B_n=p^2 1_(F_n).
$

These identities reduce both constrained systems to scalar wave operators on
finite-rank bundles. For $tau in {+,-}$, the Green-hyperbolicity theorem
supplies unique maps $G_(F,s)^tau$, $G_(G,s)^tau$, and $g_n^tau$ with
retarded support for $tau=+$ and advanced support for $tau=-$. Naturality and
uniqueness make them commute with the constant-coefficient complex maps
@baer2015 @hack-schenkel2013.

For an admissible bosonic source, set $K=M_s^(-1)J$ and define

$
  phi_J^tau=G_(F,s)^tau K,
  quad tau in {+,-}.
$

Since $C_s K=0$, commutation gives $C_s phi_J^tau=0$, and evaluation by the
original Euler operator yields

$
  E_s phi_J^tau
    =M_s(p^2-R_s C_s)G_(F,s)^tau K
    =J.
$

For a fermionic source put $K=M_n^(-1)J$ and

$
  psi_J^tau=S_n g_n^tau K,
  quad tau in {+,-}.
$

The source condition $B_n K=0$ and the hyperbolic identity compute

$
  S_n psi_J^tau
    =(p^2-2R_n B_n)g_n^tau K
    =K,
  quad
  E_n psi_J^tau=J.
$

Thus neither response inverts the gauge-degenerate field symbol directly. Each
uses the scalar wave Green operator after the source constraint has removed the
gauge defect.

== The causal source quotient equals the solution quotient

Subtract retarded and advanced maps:

$
  Delta_(F,s)=G_(F,s)^+-G_(F,s)^-,
  quad
  Delta_n=g_n^+-g_n^-.
$

The difference solves the homogeneous wave equation and sends a compact source to
a spacelike-compact solution. For bosons define

$
  cal(O)_s^bb(R)
    ={J in F_(s,c)^bb(R) mid R_s^dagger J=0}
       /E_s F_(s,c)^bb(R),
$

$
  cal(S)_s^bb(R)
    ={phi in F_(s,"sc")^bb(R) mid E_s phi=0}
       /R_s G_(s,"sc")^bb(R).
$

The causal map is

$
  cal(I)_s[J]
    =[Delta_(F,s)M_s^(-1)J].
$

If $J$ changes by $E_s a$, then

$
  Delta_(F,s)M_s^(-1)E_s a
    =Delta_(F,s)(p^2-R_s C_s)a
    =-R_s Delta_(G,s)C_s a,
$

which is gauge. Hence $cal(I)_s$ is a map of quotient classes.

Its inverse is a construction, not a dimension argument. Write $H_(F,s)=p^2$ and
$H_(G,s)=p^2$ for the wave operators on fields and parameters. Given
$E_s phi=0$, solve

$
  H_(G,s) epsilon=-C_s phi,
  quad
  phi'=phi+R_s epsilon.
$

Then $C_s phi'=0$ and $H_(F,s)phi'=0$. Wave exactness constructs compact $a,b$
with

$
  Delta_(F,s)a=phi',
  quad
  C_s a=H_(G,s)b.
$

The corrected compact datum $a'=a-R_s b$ obeys $C_s a'=0$ and
$[Delta_(F,s)a']=[phi]$. Thus $J=M_s a'$ is admissible and
$cal(I)_s[J]=[phi]$.

For injectivity, suppose $Delta_(F,s)S=R_s chi$ with compact $S$, $C_s S=0$, and
spacelike-compact $chi$. Applying $C_s$ and then wave exactness constructs compact
$b,a$ such that

$
  chi=Delta_(G,s)b,
  quad
  S-R_s b=H_(F,s)a.
$

Applying $C_s$ to the second equality gives
$H_(G,s)(b+C_s a)=0$. Compact wave uniqueness forces $b=-C_s a$, whence

$
  S=(H_(F,s)-R_s C_s)a=D_s a,
  quad
  J=M_s S=E_s a.
$

The source class is therefore zero. Combining the two constructed directions gives

$
  cal(O)_s^bb(R) tilde.equiv cal(S)_s^bb(R)
$

for every separate finite integer $s>=1$.

For fermions use the complex source quotient

$
  cal(O)_n^bb(C)
    ={J in F_(n,c) mid R_n^dagger J=0}/E_n F_(n,c)
$

and the spacelike-compact solution quotient by $R_n G_(n,"sc")$. Trace reversal
turns a source class into

$
  [K] in {K in F_(n,c) mid B_n K=0}/S_n F_(n,c).
$

The causal bridge is

$
  cal(I)_n[J]=[S_n Delta_n M_n^(-1)J].
$

Its inverse is explicitly support preserving. For a solution $psi$, choose a
temporal cutoff $chi$ and form

$
  a_+=chi psi,
  quad
  a_-=-(1-chi)psi,
  quad
  K=S_n a_+=S_n a_-=[S_n,chi]psi.
$

The datum $K$ is compact and $B_n K=0$. The cutoff fields need not satisfy the
subsidiary condition, so repair each support sign with

$
  epsilon_tau=-2g_(G,n)^tau B_n a_tau,
  quad
  a'_tau=a_tau+R_n epsilon_tau,
  quad tau in {+,-}.
$

Now $B_n a'_tau=0$ and $S_n a'_tau=K$. Wave uniqueness and the hyperbolic
identity yield

$
  S_n Delta_n K
    =a'_+-a'_-
    =psi+R_n(epsilon_+-epsilon_-).
$

Thus $J=M_n K$ maps back to $[psi]$. Conversely, if
$S_n Delta_n K=R_n epsilon$, applying $B_n$ gives $p^2 epsilon=0$. Two wave
exactness steps construct compact $b,c$ with

$
  epsilon=Delta_n b,
  quad
  S_n K-R_n b=p^2c.
$

Applying $B_n$ makes compact wave uniqueness give $b=-2B_n c$; substitution and
$S_n^2+2R_n B_n=p^2$ give $K=S_n c$. Hence $J=E_n c$ and the original source
class is zero. Therefore

$
  cal(O)_n^bb(C)
    tilde.equiv
    {psi in F_(n,"sc") mid S_n psi=0}/R_n G_(n,"sc")
$

for every finite $n>=0$.

== The physical shell constructs a positive one-particle space

The causal propagators contain both energy signs. A particle Hilbert space needs a
positive-energy orbit and a positive metric only after gauge quotienting.

=== Bosonic future-shell map

For $p in cal(O)_+={p mid p^2=0,p^0>0}$, define on the same source class

$
  W_s[J](p)
    ="res"_p(M_s^(-1)J_hat(p))
    in "Sym"_0^s(Q_p times.o bb(C))^*.
$

Admissibility places the trace-reversed datum in $ker D_s(p)$. If the source
changes by $E_s a$, then on shell $M_s^(-1)E_s a=-R_s C_s a$, and screen restriction
kills the gauge image. Thus $W_s$ is defined on $cal(O)_s^bb(R)$.

The Euclidean screen metric and the invariant measure
$dif mu_0=dif^3 bold(p)/(2abs(bold(p)))$ construct

$
  z_s([J],[K])
    =integral_(cal(O)_+)
      h_(s,p)(W_s[J](p),W_s[K](p)) dif mu_0(p).
$

For real sources, the future amplitude determines the past amplitude by Fourier
conjugation. If $W_s[J]=0$, the complete finite-type compatibility operator for
$R_s$ vanishes on the causal solution. The only obstruction to assembling local
gauge parameters with spacelike-compact support is

$
  H_("sc")^1(M;"Kill"_s)
    tilde.equiv H_c^1(bb(R)^3;Z_s)=0.
$

Therefore the solution is globally gauge, and injectivity of $cal(I)_s$ gives
$[J]=0$. The form $z_s$ is a genuine positive norm on the source quotient, not a
seminorm requiring another spectral quotient.

Its complex completion is the source-generated one-particle space

$
  cal(H)_("src",s)
    =overline(W_s(cal(O)_s^bb(R)))
    subset.eq
    L^2(cal(O)_+,dif mu_0;
      bb(C)_(+s) plus.o bb(C)_(-s)).
$

Screen transport gives exactly the induced Poincare action of @sec-particle-data, so this
is a closed invariant subrepresentation of the abstract helicity-pair space.
Density in that entire abstract space is not claimed.

The causal form and positive form are compatible. Future multiplication by $+i$
and conjugate past multiplication by $-i$ construct a complex structure $J_s$;
the opposite signs of the causal distribution on the two shells then give, after
one overall real action normalization,

$
  omega_s(x,y)=2 "Im" z_s(x,y),
  quad
  mu_s(x,y)=omega_s(x,J_s y)=2 "Re" z_s(x,y).
$

=== Fermionic particle and antiparticle map

For a fermionic source set $K_J=M_n^(-1)J$ and first construct an actual on-shell
field amplitude

$
  X_J(p)=S_n(p)K_J_hat(p).
$

The hyperbolic identity and $B_n K_J=0$ give $S_n(p)X_J(p)=0$ on the null cone, so
screen restriction defines $w_n[J](p) in cal(S)_n(Q_p,W_p)$.

The positive spinor metric is not the indefinite Dirac pairing. For nonzero null
$p$, choose a null witness $a_p$ with $p dot a_p=1$ and the same time orientation,
and define on $W_p=ker gamma(p)$

$
  kappa_p(w,v)
    ="sign"(p^0) beta(w,gamma(a_p)v).
$

If $a'_p-a_p=q in p^perp$, the null Clifford homotopy and
$gamma(p)w=gamma(p)v=0$ make the difference vanish. Writing
$t_p="sign"(p^0)(p+a_p)/sqrt(2)$ identifies $kappa_p$ with a positive observer
spinor metric. Tensoring it with the Euclidean screen metric gives a positive
metric $h_(n,p)$ on the gamma-traceless physical fiber.

A complex source has independent future and past data, so both must be retained.
For $p in cal(O)_+$ define

$
  w_n^+[J](p)=w_n[J](p),
  quad
  w_n^-[J](p)=overline(w_n[J](-p)).
$

The paired map $W_n^("pair")=(w_n^+,w_n^-)$ is real linear. Both components have
positive translation spectrum because conjugation reverses the past-shell phase.
At each future-shell momentum, construct the two branch pairings

$
  h_(n,p)^+([J],[K])=h_(n,p)(w_n^+[J],w_n^+[K]), \
  h_(n,p)^-([J],[K])=overline(h_(n,-p))(w_n^-[J],w_n^-[K]).
$

Their direct-sum integral is the positive form

$
  z_n^("pair")([J],[K])
   =integral_(cal(O)_+) [h_(n,p)^+([J],[K])+h_(n,p)^-([J],[K])] dif mu_0(p).
$

If both amplitudes vanish, the finite-type compatibility complex for the
gamma-traceless gauge operator has obstruction

$
  H_("sc")^1(M;"KillSpin"_n)
    tilde.equiv H_c^1(bb(R)^3;Z_n)=0.
$

It constructs one spacelike-compact gauge parameter, and the causal quotient
isomorphism then gives $[J]=0$. Thus the paired form is faithful for every finite
$n$, including the ungauged $n=0$ case.

The completion

$
  cal(H)_("src",n)
    =overline("span"_bb(C) W_n^("pair")(cal(O)_n^bb(C)))
$

is a positive-energy particle/antiparticle subrepresentation. Each component has
helicities $+(n+1/2)$ and $-(n+1/2)$. No Majorana or charge-conjugation
identification between them has been imposed, and full induced-space density
remains open.

The local Euler form is not a second unrelated fermionic structure. On the null
shell, choose the canonical gamma-traceless screen lift $tilde(r)_K$ of the physical
amplitude. Exactness gives
$X_K-tilde(r)_K=R_n epsilon$; pairing with the same admissible source kills this
gauge term. Since $M_n tilde(r)_K=tilde(r)_K$, trace reversal also disappears. One
application of

$
  gamma(p)gamma(a_p)r_K=2r_K
$

then converts the remaining Dirac pairing into $h_(n,p)$. The energy sign of the
causal distribution cancels the sign in $kappa_p$. After one allowed overall real
normalization of the quadratic action,

$
  q_n(x,y)=z_n^("pair")(x,y),
  quad
  tau_n(x,y)=2 "Re" z_n^("pair")(x,y).
$

This is a same-source equality of the local causal and positive CAR forms.

== Fock multiplicity recovers the same one-particle vector

For a complex Hilbert space $cal(H)$, construct

$
  Gamma_+(cal(H))=limits(plus.o)_(r>=0) "Sym"^r cal(H),
  quad
  Gamma_-(cal(H))=limits(plus.o)_(r>=0) "Alt"^r cal(H).
$

The zero-fold tensor power supplies the vacuum
$Omega=(1,0,0,dots)$. The canonical one-particle injection and projection satisfy

$
  iota_1(u)=(0,u,0,dots),
  quad
  P_1 iota_1=1_cal(H).
$

For $epsilon_("stat") in {+,-}$, functoriality of symmetric or antisymmetric powers also
computes

$
  Gamma_(epsilon_("stat"))[U_1(g)] iota_1(u)=iota_1(U_1(g)u),
$

so the original particle representation remains a canonical summand.

For the bosonic source-generated space, let $a^dagger,a$ satisfy the CCR and
define on the same real source class

$
  Phi_s(x)=a(W_s x)+a^dagger(W_s x).
$

Then

$
  [Phi_s(x),Phi_s(y)]
    =2i "Im" innerproduct(W_s x,W_s y)
    =i omega_s(x,y).
$

Causal support makes this commutator vanish for causally disjoint sources. Acting
on the vacuum removes the annihilation term:

$
  Phi_s(x)Omega=iota_1(W_s x),
  quad
  P_1 Phi_s(x)Omega=iota_1(W_s x).
$

Thus quantization returns exactly the shell vector that entered it.

For fermions, realify the paired source image and define

$
  b_n(x)=a(W_n^("pair")x)+a^dagger(W_n^("pair")x)
$

on $Gamma_-(cal(H)_("src",n))$. The normalized causal equality gives

$
  {b_n(x),b_n(y)}
    =2 "Re" innerproduct(W_n^("pair")x,W_n^("pair")y)
    =tau_n(x,y)1.
$

It vanishes for causally disjoint supports, proving graded locality. The same
vacuum calculation gives

$
  P_1 b_n(x)Omega=iota_1(W_n^("pair")x).
$

Faithfulness on both branches makes the recovery null spaces coincide:

$
  x=0
  <=> W x=0
  <=> "field"(x)Omega=0
  <=> P_1"field"(x)Omega=0.
$

#theorem[Causal and free-quantum recovery][
  For every separate finite symmetric
  massless integer or half-integer potential complex constructed in @sec-local-complexes,
  compact admissible sources modulo Euler sources are isomorphic to
  spacelike-compact solutions modulo gauge. Their faithful physical shell maps
  construct positive source-generated one-particle Hilbert spaces carrying the
  induced Poincare representations. Symmetric or antisymmetric Fock construction
  adds multiplicity, while one field application to the vacuum recovers the
  identical shell vector. Density in the entire abstract induced Hilbert space,
  optional real fermion forms, countable-spin completion, and interactions are not
  included.
] <thm-causal-quantum-recovery>

= Low-spin recovery and comparison <sec-low-spin>

Spins $0,1/2,1,3/2,2$ now test the universal construction; they do not define it.
The invariant under every comparison is the physical standard-momentum fiber.
The strength of the relation between two field presentations must be computed
separately.

== “Same particle” has a precise but limited meaning <sec-low-spin-equivalence>

For a symbol complex at a standard momentum $k$, write

$
  cal(P)_(D,R)(k)=ker D(k)/im R(k),
$

with $im R(k)=0$ when there is no gauge map. Suppose a carrier map
$L_k:F arrow.r F'$ satisfies

$
  L_k(ker D(k)) subset.eq ker D'(k),
  quad
  L_k(im R(k)) subset.eq im R'(k).
$

Evaluating both inclusions on the same solution and gauge representatives
constructs the quotient map

$
  bar(L)_k:cal(P)_(D,R)(k) arrow.r cal(P)_(D',R')(k),
  quad
  bar(L)_k[phi]=[L_k phi].
$

If $bar(L)_k$ is a $K_k$-equivariant isomorphism, @sec-realization transports it over the
momentum orbit and the two systems carry the same induced one-particle
representation.

A comparison can be made even when no direct carrier map is known. If the two
physical fibers have already been constructed through

$
  j:cal(P)_(D,R)(k) tilde.equiv V_sigma,
  quad
  j':cal(P)_(D',R')(k) tilde.equiv V_sigma,
$

then the common-fiber composite

$
  bar(L)_k=(j')^(-1)j
$

is an orbitwise representation equivalence. It depends on the choices in $j,j'$
and need not extend to a polynomial local map. Consequently the paper distinguishes
three increasingly weak outcomes:

$
  "same symbol"
  arrow.r
  \
  "local map of physical complexes"
  arrow.r
  \
  "orbitwise representation equivalence".
$

Neither arrow reverses without an additional construction. None by itself proves
equality of actions or persistence after coupling.

== Spin zero is the direct scalar evaluation

The scalar carrier has no redundant direction. The massive and massless symbols
are

$
  D_m(p)=p^2-m^2,
  quad
  D_0(p)=p^2.
$

On the selected shell their kernels are $bb(C)$; away from it the kernels vanish.
The stabilizer acts trivially on this one-dimensional carrier, so @sec-realization gives
massive spin zero or massless helicity zero directly. No quotient, polarization,
or component equation is required. A real scalar condition and a particular
quadratic action remain choices beyond this complex one-particle realization.

== Spin one half separates chirality, parity pairing, and differential order

=== Massless: the paired Clifford kernel is two Weyl kernels

The vector--spinor bridge of @sec-local-complexes constructs the Clifford action on
$Delta=S plus.o bar(S)$. Denote its off-diagonal natural maps by

$
  c_p:S arrow.r bar(S),
  quad
  bar(c)_p:bar(S) arrow.r S.
$

On the same pair $xi plus.o bar(eta)$, the definition of $gamma(p)$ evaluates as

$
  gamma(p)(xi plus.o bar(eta))
    =bar(c)_p bar(eta) plus.o c_p xi.
$

Therefore

$
  ker gamma(k)=ker c_k plus.o ker bar(c)_k.
$

The two summands are precisely the chiral null lines constructed in @sec-local-complexes,
with helicities $-1/2$ and $+1/2$. The half-integer potential machine at $n=0$
has $S_0(k)=gamma(k)$ and no gauge carrier, so its physical fiber is exactly the
direct sum of the two Weyl fibers. Selecting one Weyl equation, keeping the pair,
or imposing a reality relation are distinct additional decisions.

=== Massive: Dirac factorization adds an off-shell choice

The shortest massive baseline is the scalar shell symbol

$
  D_(m,1/2)^"ch"(p)=(p^2-m^2)1_S.
$

To obtain a first-order parity-paired presentation, choose $Delta$ and construct

$
  D_m^"Dir"(p)=gamma(p)-m.
$

The Clifford identity evaluates the opposite factor on the same $z in Delta$:

$
  (gamma(p)+m)D_m^"Dir"(p)z=(p^2-m^2)z.
$

This is a factorization witness, not an assertion that the two off-shell systems
are identical. For $k=m tau$, put

$
  B_tau=gamma(tau),
  quad
  Pi_tau^+=(1+B_tau)/2.
$

Since $B_tau^2=1$,

$
  D_m^"Dir"(k)z=0
  quad <=> quad
  z=Pi_tau^+z,
  quad
  im Pi_tau^+ tilde.equiv V_(1/2).
$

The chiral rest carrier is the same $V_(1/2)$. Their common-fiber composite from
@sec-low-spin-equivalence therefore proves equality of the positive-energy one-particle
representations. The chirality pair, first-order factorization, scalar mass
coupling, Dirac pairing, and any disconnected parity action are extra structure.

== Spin one exhibits both comparison strengths

=== Massive: chiral and Proca are orbitwise equivalent

The direct baseline is $(p^2-m^2)1_("Sym"^2(S))$. Choosing instead the Lorentz
vector carrier and requiring a parity-even quadratic symbol with no extra
longitudinal characteristic constructs

$
  K_"Proca"(p)A=(m^2-p^2)A+p(p dot A).
$

Contracting the same vector with $p$ gives

$
  p dot K_"Proca"(p)A=m^2(p dot A).
$

Thus an on-shell solution is transverse. At $k=(m,0,0,0)$,

$
  ker K_"Proca"(k)=k^perp tilde.equiv V_1.
$

The chiral carrier also restricts to $V_1$, with no lower rest spin. The
common-fiber composite proves orbitwise one-particle equivalence, but no local
invertible field redefinition between the chiral and Proca equations has been
constructed. The vector carrier, transversality constraint, minimal quadratic
order, parity-even ansatz, and exclusion of another longitudinal shell are the
extra Proca presumptions.

=== Massless: curvature constructs a local physical-shell isomorphism

At $s=1$, the bosonic potential complex evaluates to

$
  R(p)alpha=p alpha,
  quad
  K_"Max"(p)A=i_p(p and A)=p^2A-p(p dot A).
$

The curvature operation kills gauge on the same scalar:

$
  p and R(p)alpha=p and p alpha=0.
$

It therefore descends to

$
  bar(d)_p:ker K_"Max"(p)/im R(p) arrow.r "Alt"^2 V_bb(C),
  quad
  bar(d)_p[A]=p and A.
$

For nonzero null $p$, it is injective because $p and A=0$ makes $A$ proportional
to $p$. It is onto the closed and coclosed curvature fiber by an explicit inverse.
Given $F$ with $p and F=0$ and $i_p F=0$, choose $n$ with $n dot p=1$; contraction
computes

$
  0=i_n(p and F)=F-p and (i_n F),
  quad
  F=p and (i_n F).
$

Hence

$
  ker K_"Max"(p)/im R(p)
  tilde.equiv
  {F mid p and F=0, i_p F=0}.
$

This is stronger than a common-fiber comparison: $A mapsto p and A$ is a
polynomial local map on physical shell data. Hodge duality then separates the two
curvature helicities. Gauge redundancy belongs to the potential presentation;
choosing one duality sector, pairing both helicities, imposing reality, or extending
the statement through nontrivial topology requires further input.

== Spins three halves and two expose the present local-map boundary

At $n=1$, the fermionic potential complex is the massless vector--spinor branch.
Its screen restriction computes

$
  ker S_1(k)/im R_1(k)
    tilde.equiv cal(H)_1(Q_k,W_k)
    tilde.equiv bb(C)_(+3/2) plus.o bb(C)_(-3/2).
$

The two direct chiral curvature equations on $"Sym"^3(S)$ and its conjugate have
the same two character lines. Composing their already-constructed character maps
with the inverse screen map gives the orbitwise equivalence of @sec-low-spin-equivalence.
This vector--spinor specialization may be called the massless symmetric
Rarita--Schwinger or Fang--Fronsdal branch, but the comparison proves neither a
massive Rarita--Schwinger system nor an off-shell local equivalence to the chiral
curvature.

At $s=2$, the bosonic potential complex similarly gives

$
  ker D_2(k)/im R_2(k)
    tilde.equiv "Sym"_0^2(Q_k times.o bb(C))^*
    tilde.equiv bb(C)_(+2) plus.o bb(C)_(-2).
$

The two direct chiral spin-two curvature equations carry those same character
lines. Their common-fiber composite again proves orbitwise representation
equivalence. The symmetric metric potential, trace reversal, gauge quotient, and
parity pairing are additional structures. A local curvature/potential
quasi-isomorphism has not been constructed here, and a conventional massive
Fierz--Pauli comparison is outside the supported branch.

== Bounded verdict

The comparison strengths and their unpaid presumptions are collected in
@tab-low-spin-verdict.

#figure(
  table(
    columns: (0.45fr, 1.35fr, 1.25fr, 1.55fr),
    inset: 5pt,
    align: left + top,
    table.header(
      [*Spin*], [*Evaluated presentations*], [*Strongest supported relation*],
      [*Additional input or boundary*],
    ),
    [$0$], [scalar shell], [direct identity], [reality and action],
    [$1/2$], [Weyl, paired massless Dirac, massive Dirac],
      [massless block identity; massive orbitwise equivalence],
      [chirality pairing, first order, mass coupling, parity],
    [$1$], [chiral curvature, Maxwell, massive chiral, Proca],
      [Maxwell local shell isomorphism; Proca orbitwise equivalence],
      [gauge, duality/reality, vector carrier, minimality],
    [$3/2$], [chiral curvature and massless vector--spinor potential],
      [orbitwise equivalence], [local curvature map and massive comparison open],
    [$2$], [chiral curvature and massless metric potential],
      [orbitwise equivalence], [local curvature map and Fierz--Pauli comparison open],
  ),
  caption: [Supported relations among the bounded low-spin presentations.],
) <tab-low-spin-verdict>

The bounded cases reproduce the universal physical fibers and reveal which
presumptions purchase a familiar equation. They do not select one preferred
presentation. The old component gamma/sigma chains and recursive chirality
elimination are therefore not promoted: without an independently checked quotient
map they add algebraic length but no stronger equivalence. This is the @sec-low-spin
stop condition.

= Equivalence boundary and outlook <sec-equivalence-outlook>

@sec-low-spin showed that two fields can recover the same particle at different
mathematical strengths. This final section makes those strengths explicit, tests
one attempted passage to interaction, and states where the present construction
must stop.

The broader continuation is retained rather than discarded. The companion
#link("field-equations-to-computable-observables.md")[*From Field Equations to
Computable Observables*] follows the research graph from failed universal spectral
reductions through field/particle extraction, collective closure, and the
field-derived coupling measure. It is separate because it consumes additional
Hamiltonians, preparations, observables, and scale assumptions; it is continuous
with this paper because its first input is the free field realization constructed
here.

== Equivalence is indexed by the structure preserved <sec-equivalence-levels>

Let $cal(C)$ and $cal(C)'$ be two free symbol complexes on the same declared
momentum orbit. Their comparison can ask for the witnesses in
@tab-equivalence-ladder.

#figure(
  table(
    columns: (1.15fr, 1.9fr, 1.8fr),
    inset: 5pt,
    align: left + top,
    table.header(
      [*Claim*], [*Required witness*], [*Not supplied by that witness*],
    ),
    [label coincidence], [same orbit and little-group label],
      [carrier, equation, or gauge complex],
    [physical-fiber equivalence],
      [$K_k$-isomorphism $bar(L)_k:H(cal(C)_k) tilde.equiv H(cal(C)'_k)$],
      [polynomial local field map],
    [one-particle equivalence],
      [unitary Poincare intertwiner $U_1$],
      [off-shell or source-response equivalence],
    [local-complex equivalence],
      [polynomial chain maps with inverse chain homotopies],
      [support, action, or state preservation],
    [causal-response equivalence],
      [commuting source/solution square for the causal maps],
      [equality of quadratic actions],
    [action equivalence],
      [pairing-preserving field/source map, up to boundary and null sectors],
      [survival after deformation],
    [free-quantum equivalence],
      [isometric symplectic or CAR map and its Fock lift],
      [interacting equivalence or equal observables],
    [deformation equivalence],
      [the preceding maps for the deformed complexes and domains],
      [computational compression],
    [predictive equivalence],
      [same-input observable equality or controlled error],
      [a cheaper route to that observable],
  ),
  caption: [Equivalence claims indexed by their required witness.],
) <tab-equivalence-ladder>

The implications used in this paper are computed rather than inferred from the
names. A polynomial chain equivalence induces an isomorphism on the quotient
fibers. @sec-realization then transports a $K_k$-isomorphism over the orbit to obtain a
Poincare intertwiner. If that intertwiner is unitary, symmetric or antisymmetric
functoriality constructs

$
  Gamma_(epsilon_("stat"))(U_1)iota_1(u)=iota_1(U_1u),
  quad epsilon_("stat") in {+,-}.
$

Thus the same one-particle vector is preserved inside the corresponding Fock
space. The reverse implications do not hold automatically. @sec-low-spin already
exhibits orbitwise equivalences for which no polynomial local inverse has been
constructed.

Causal comparison adds support-sensitive data. If $Delta_cal(C)$ and
$Delta_(cal(C)')$ are the two causal source maps, source and solution maps must
make the same-source square commute:

$
  L_"sol"(Delta_cal(C)[J])
    =[Delta_(cal(C)') L_"src"(J)].
$

An orbitwise map alone has neither a compact-source domain nor a causal support
statement, so it cannot prove this equation.

Action comparison adds the duality that defines a source. For an invertible field
map $L$, the required equalities have the form

$
  cal(A)'[L phi]=cal(A)[phi]+"boundary",
  quad
  J'=L^(-dagger)J,
  quad
  innerproduct(J',L phi)=innerproduct(J,phi).
$

Equal vacuum kernels without these identities need not have equal sourced
response.

== The strongest theorem constructed here

The first five sections establish, for every separate finite label,

$
  (cal(O)_k,sigma)
  arrow.r V_sigma
  arrow.r F
  arrow.r (R,D)
  arrow.r H(cal(C)_k)
  tilde.equiv V_sigma
  arrow.r cal(H)_(cal(O),sigma).
$

The direct chiral route supplies this construction for every finite massive spin
and massless helicity. The parity-paired massless symmetric potential routes first
continue to a source-generated one-particle space:

$
  "physical cohomology"
  arrow.r
  "causal source/solution quotient"
  arrow.r
  cal(H)_"src".
$

For $epsilon_("stat") in {+,-}$, the statistics choice then constructs

$
  cal(H)_"src" arrow.r Gamma_(epsilon_("stat"))(cal(H)_"src").
$

Every arrow in that continuation was evaluated on one compact admissible source.
In particular, @sec-causal-completion obtained

$
  P_1 "field"(x)Omega=iota_1(W x).
$

The right side is exactly the positive-shell vector used to define the
one-particle completion. This is stronger than matching spin labels: the causal
quotient, positive norm, quantum statistics, and vacuum recovery share the same
input and null space.

#theorem[Finite free-field realization and recovery][
  On four-dimensional
  Minkowski spacetime, every separate finite massive spin or massless finite
  helicity representation in the declared positive-energy class admits a local
  complex chiral realization whose physical standard-momentum fiber recovers the
  original little-group representation. Every separate parity-paired massless
  symmetric integer or half-integer potential family constructed here additionally
  admits a causal source/solution quotient, a faithful source-generated positive
  one-particle completion, and free CCR or CAR quantization whose one-field vacuum
  excitation is the identical physical shell vector. These constructions are
  existence and recovery results; they assert neither uniqueness of presentation
  nor the stronger equivalences in @sec-equivalence-levels.
] <thm-free-field-recovery>

== Curvature obstructs automatic survival after coupling

The massive Dirac example gives a same-input test of deformation. For commuting
free momentum, @sec-low-spin computed

$
  (gamma(p)+m)(gamma(p)-m)=(p^2-m^2)1_Delta.
$

Now choose a $U(1)$ connection and replace $p_mu$ by the covariant momentum
$Pi_(A,mu)=i partial_mu-e A_mu$. Acting on the same section gives

$
  [Pi_(A,mu),Pi_(A,nu)]=-i e F_(mu nu).
$

Splitting the Clifford product into symmetric and antisymmetric parts therefore
computes

$
  (gamma(Pi_A)+m)(gamma(Pi_A)-m)
   =(Pi_A^2-m^2)1_Delta
     -(i e/4)[gamma^mu,gamma^nu]F_(mu nu).
$

The last term is a spin--curvature endomorphism. It vanishes for the free flat
connection but not for a general electromagnetic background. Hence the free
Dirac-to-scalar factorization does not deform into a scalar covariant-wave
factorization. The failure is produced by curvature, not by a poor coordinate
choice.

The same test governs any interacting continuation. One must reconstruct the
deformed complex identities, action and Noether identity, operator domains, causal
maps, state, and observable. Agreement at zero coupling supplies initial data for
that problem; it is not its solution.

== A field equation is an intermediate object, not a prediction <sec-equation-intermediate>

Let $cal(I)$ be admissible input data, let
$"Sol"_cal(C):cal(I) arrow.r cal(P)$ be a chosen physical response, and let
$O:cal(P) arrow.r cal(Z)$ be a named observable. The prediction is the composite

$
  F_(cal(C),O)=O circle "Sol"_cal(C):cal(I) arrow.r cal(Z).
$

This equation shows why covariance or even a free Fock representation is not an
endpoint. Boundary conditions, a domain, a state and preparation, and an observable
must be constructed before $F_(cal(C),O)$ exists.

An invertible presentation change $T:cal(P) arrow.r cal(P)'$ preserves the
prediction only after both response and observable are transported:

$
  "Sol"_cal(C)'=T circle "Sol"_cal(C),
  quad
  O'=O circle T^(-1).
$

Evaluation on the same $i in cal(I)$ gives the semantic coincidence

$
  O'("Sol"_cal(C)'(i))=O("Sol"_cal(C)(i)).
$

This equality proves invariant meaning, but not cheaper computation. A genuine
observable compression must construct a smaller route whose recovery equals this
same composite and whose complete construction, solution, and recovery cost is
lower or controlled. That question is model and observable dependent.

The present free-field construction does achieve two bounded reductions. First,
physical quotienting removes gauge directions that every declared observable must
identify. Second, the massless symmetric potential identities reduce all separate
finite ranks to scalar wave Green maps plus finite carrier operations. Neither
result is a universal solver for interacting spectra, bound states, scattering, or
many-body dynamics.

== Stop and re-entry conditions

The paper stops because its internal benchmark has been met: it constructs local
finite-spin realizations, verifies their physical fibers, and, on the supported
potential branches, recovers the same one-particle vector after causal completion
and free quantization. Additional detail cannot strengthen that theorem without
changing the claim class.

The open branches have precise re-entry conditions:

- Full equality with the abstract induced Hilbert spaces requires a density theorem
  for the compact-source shell images.
- A countable-spin object requires a chosen topology, label weights, a common dense
  operator domain, and Green estimates uniform in spin.
- Conventional massive higher-spin comparisons require explicit local chain maps
  and standard-fiber checks, not matching component counts.
- Curved or interacting fields require a deformed complex or action, domains,
  causal construction, state, preparation, and observable.
- A claim of computational gain requires a fixed model, input class, observable,
  accuracy, and same-observable whole-route cost comparison.

Poincare symmetry therefore supplies the invariant particle datum and constrains
its covariant realizations. Mathematics then constructs particular equations,
quotients, causal responses, and quantum fields from additional choices. The
distinction is productive: it tells us exactly what has been predicted, which
presumptions paid for it, and where a new theory or computation must begin.

#bibliography("poincare-to-free-fields.bib")

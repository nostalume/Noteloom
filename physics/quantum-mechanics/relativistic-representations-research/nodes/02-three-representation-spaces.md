# N2 — Constructing the Three Representation Spaces

State: supported construction within the `N1` free-particle scope  
Consumes: the determination boundary of `N1`  
Manuscript destination: Section 2

Gap audit: [02-semantic-gap-audit.md](../results/02-semantic-gap-audit.md)

## Capability

Construct, rather than import, the mathematical objects needed to pass from
inertial symmetry to:

1. physical one-particle states;
2. local covariant fields;
3. scalar generating functions on the space of reference frames.

The construction begins with what an observer can change or measure. Terms such as
orbit, little group, invariant measure, and carrier are introduced only when a
specific obstruction creates them.

Every bridge below is marked by its logical role:

- **presumption:** physical or analytic input not derived here;
- **definition:** a name assigned to an object already constructed;
- **theorem contract:** a standard theorem whose exact hypotheses and output are
  stated, so it is not used as a hidden slogan;
- **deduction:** an equation derived from preceding objects.

The primary research spine is Sections 1--4:

```text
symmetry -> momentum orbit -> residual-frame group -> physical state space
         -> optional finite Lorentz carrier -> covariant field space.
```

Section 5 is an optional branch asking whether reference-frame coordinates provide
either a new Hilbert realization or only coefficient packaging. Section 6 returns
that branch to the primary field bridge. A reader concerned only with local field
equations may move from Section 4 directly to the constructed relation near the
end.

## Development contract

- **Incoming datum:** `N1` supplies a strongly continuous one-particle symmetry
  action, positive energy, irreducibility, and concentration on one momentum
  orbit. It does not supply a field carrier or equation.
- **Question:** which representation spaces are forced by the distinct
  capabilities “describe physical states,” “write local covariant equations,” and
  “replace components by frame coordinates”?
- **Semantic invariant:** an active change of inertial frame must describe the
  same event, momentum, state, or field section in new coordinates. Every equality
  below is evaluated on that common object.
- **Output:** typed spaces, actions, norms, and exact bridges passed to `N3`; no
  claim that the spaces are automatically equivalent.
- **Failure boundary:** massless gauge realization, equation construction, and the
  physical meaning of right translations remain downstream questions.

## Starting physical structure

Let `V` be real four-dimensional translation space and let `eta` be a
nondegenerate bilinear form of signature `(1,3)`. Assume:

- events form an affine four-dimensional spacetime with Minkowski interval;
- inertial observers are related by transformations preserving that interval and
  the chosen space/time orientation;
- quantum states are complex amplitudes and changing inertial observer preserves
  transition probabilities;
- the present problem concerns one free particle, so spacetime translations are
  exact symmetries.

**Presumption (affine inertial spacetime).** An inertial transformation acts by

```text
x |-> Lambda x + a,  a in V.
```

Applying first `(b,M)` and then `(a,Lambda)` to the same event `x` computes

```text
Lambda(Mx+b)+a
  = (Lambda M)x + (a+Lambda b),

(a,Lambda)(b,M) = (a+Lambda b, Lambda M).
```

The inverse is fixed by requiring both products to return `(0,1)`:

```text
(a,Lambda)^(-1) = (-Lambda^(-1)a,Lambda^(-1)),

(a,Lambda)(-Lambda^(-1)a,Lambda^(-1)) = (0,1).
```

The affine form is not derived merely from the word “inertial”; it is part of the
starting spacetime structure. Interval preservation then requires
`Lambda^T eta Lambda=eta`. The connected transformations preserving orientations
form `L_0=SO^+(1,3)`.

**Definition.** The transformations with the derived composition law form the
connected Poincare group `G_0=V semidirect L_0`.

Quantum states are rays: multiplying a state vector by a phase does not change its
physical state. A spacetime symmetry therefore first acts on rays, not necessarily
on chosen vectors.

**Theorem contract (ray symmetry).** A bijection of Hilbert-space rays preserving
all transition probabilities is implemented by either a unitary or an antiunitary
operator, unique up to phase. A transformation connected continuously to the
identity cannot switch between these two types. Choosing unitary implementers
therefore produces a strongly continuous projective action:

```text
U(g_1)U(g_2) = omega(g_1,g_2) U(g_1g_2),
|omega|=1.
```

The phase `omega` is not observable on rays but obstructs treating `U` as an
ordinary representation.

**Theorem contract (lifting the projective action).** A strongly continuous
projective unitary representation is an ordinary unitary representation of the
central extension defined by its multiplier. For the connected 3+1-dimensional
Poincare symmetry in the present scope, after the translation cocycle is shown
trivial in Section 1, this extension is represented by passing to the universal
spin cover. In particular, rotations are lifted to

```text
L_spin = Spin^+(1,3) ~= SL(2,C),
Lambda: L_spin -> L_0,
```

allowing a `2pi` rotation to act as `-1` on a state vector while leaving its ray
unchanged. From this point

```text
G = V semidirect_Lambda L_spin
```

and `U` is an ordinary strongly continuous unitary representation of `G`.

Momentum is a covector because it evaluates a translation. For `p in V^*`, write
`p.a := p(a)`. The Lorentz action on momenta is constructed as the dual action

```text
(A dot p)(a) := p(Lambda(A)^(-1)a).
```

It is the unique action preserving the pairing:

```text
(A dot p).(Lambda(A)a) = p.a.
```

The metric `eta` may identify `V^*` with `V`, after which `A dot p` has the usual
four-vector notation `Lambda(A)p`. Until that identification is needed, `dot`
keeps the domains visible.

This construction repairs manuscript line 85: the first translation cannot vanish
from a composition of affine transformations.

## 1. Translations construct momentum

Restrict `U` to translations. A projective translation action could in principle
produce a central Lie-algebra term

```text
[P_mu,P_nu] = i Z_(mu nu) identity.
```

Differentiating Lorentz covariance would make `Z` a fixed antisymmetric Lorentz
two-form. Its components `Z_(0i)` form a spatial vector under rotations, while
`epsilon_(ijk)Z_(jk)/2` form another. A tensor fixed by every spatial rotation
would give two rotation-fixed vectors, and the only such vectors are zero. Hence
`Z=0`. Because `V` is simply connected, the projective translation multiplier
with zero infinitesimal cocycle is a coboundary; a phase choice therefore makes the
translation representation ordinary:

```text
U(a)U(b) = U(a+b).
```

The missing bridge to generators is spectral, not a formal Taylor expansion.

**Theorem contract (one-parameter generator).** If `t |-> U(t e_mu)` is a strongly
continuous unitary one-parameter group, then there is a unique self-adjoint
operator `P_mu` with

```text
U(t e_mu) = exp(i t P_mu).
```

Here the exponential is defined by the spectral calculus of `P_mu`. Conversely,
every self-adjoint `P_mu` defines such a strongly continuous unitary group. Its
domain can also be recovered directly from the strong derivative

```text
P_mu psi = (1/i) lim_(t->0) [U(t e_mu)psi-psi]/t
```

on exactly those vectors for which the limit exists.

The semantic content can be seen before the full theorem. On a one-dimensional
spectral component, unitarity makes `U(t)` a phase `c(t)`. The group law and
continuity require

```text
c(t+s)=c(t)c(s),
|c(t)|=1
  => c(t)=exp(i t p)
```

for one real number `p`. The spectral theorem assembles a general Hilbert space as
a continuous orthogonal superposition of these phase characters; the real label
`p` becomes the spectrum of the self-adjoint generator. Stone's theorem supplies
the rigorous domain statement when the generator is unbounded.

Because the four translation subgroups commute, their spectral projections commute
strongly. The joint spectral theorem therefore supplies one projection-valued
measure `E(dp)` on momentum space such that

```text
U(a) = integral exp(i p.a) E(dp)
     = exp(i a^mu P_mu),

P_mu = integral p_mu E(dp).
```

Equivalently, every continuous one-dimensional unitary character of the whole
translation group has the form `a |-> exp(i p.a)` for one covector `p`; `E(dp)`
assembles these characters with their Hilbert-space multiplicities.

This is the rigorous meaning of

```text
U(a) = exp(i a^mu P_mu).
```

**Definition.** A point `p` in the support of the joint spectral measure is a
possible momentum. Thus momentum is the spectral value created by translation
symmetry, not an extra representation coordinate.

Changing inertial frame conjugates translations:

```text
U(A) U(a) U(A)^(-1) = U(Lambda(A)a).
```

This conjugation transports a momentum spectral subspace rather than changing its
physical content. To calculate the transport, let `F_A(Delta)` denote
`U(A)E(Delta)U(A)^(-1)`. Then

```text
integral exp(i p.a) F_A(dp)
  = U(A)U(a)U(A)^(-1)
  = U(Lambda(A)a)
  = integral exp(i p.(Lambda(A)a)) E(dp)
  = integral exp(i (A^(-1) dot p).a) E(dp)
  = integral exp(i q.a) E(d(A dot q)).
```

Both sides are spectral representations of the same translation operator for
every `a`. Uniqueness of the joint spectral measure therefore gives

```text
U(A) E(Delta) U(A)^(-1) = E(A dot Delta)
```

for every measurable momentum set `Delta`. Hence the spectral support is invariant
under frame changes: if `p` can occur, so can `A dot p`.

An invariant spectrum could still be a union of several invariant pieces. The
restriction to one particle species therefore uses the **single-orbit presumption
from N1**: the spectral measure is concentrated on the orbit of one momentum `k`,

```text
O_k = { A dot k | A in L_spin }.
```

**Definition.** This set is the momentum orbit because it consists precisely of the momenta
reachable by changing inertial frame. The Minkowski square is unchanged along it.
For a positive-energy massive particle, choosing `k=(m,0,0,0)` gives

```text
O_m^+ = { p | p^2=m^2, p^0>0 }.
```

The orbit is contained in this set because the norm and time orientation are
preserved. Conversely, for any `p` in the displayed set, define

```text
v = spatial(p)/p^0,
gamma = 1/sqrt(1-|v|^2) = p^0/m.
```

The boost with velocity `v` sends `(m,0,0,0)` to
`(gamma m,gamma m v)=p`. Thus both inclusions are computed, and the mass shell is
the orbit of a rest momentum rather than an unrelated wave equation inserted
later.

## 2. Ambiguity of the standard frame constructs the little group

The map `A |-> A dot k` is onto `O_k` by construction. To compare internal
states at different `p`, choose one preimage `B(p)`:

```text
B(p) dot k = p.
```

Such a choice is called a section of this map. A measurable section is sufficient
for the Hilbert-space construction; a global smooth section is not presumed. The
choice is not unique. If both `B_1(p)` and `B_2(p)` send `k` to `p`, then

```text
B_1(p)^(-1) B_2(p) dot k
  = B_1(p)^(-1) dot p
  = k.
```

The ambiguity is therefore exactly the set

```text
K_k = { R in L_spin | R dot k=k }.
```

**Definition.** We call it the little group of `k`; it has not been added externally. It is the
unavoidable residual change of frame left after momentum has been standardized.

Any internal state attached to `k` must specify how this ambiguity acts. Let
`V_sigma` be that internal state space and `sigma(R)` its probability-preserving
action. If `sigma` split into invariant pieces, the alleged particle type would
split as well, so a single particle species is represented by an irreducible
`sigma`.

The fibers over different momenta can now be constructed without choosing `B(p)`.
Start from pairs `(A,v)` with `A in L_spin` and `v in V_sigma`, and identify

```text
(A R, v) ~ (A, sigma(R)v),  R in K_k.
```

The projection is constant on each equivalence class because

```text
(A R) dot k = A dot (R dot k) = A dot k.
```

Thus `A` and `AR` reach the same momentum while `R` changes only the internal
rest-frame basis. The quotient

```text
E_sigma = (L_spin times V_sigma)/~  -> O_k,
[A,v] |-> A dot k
```

is the internal state bundle over the momentum orbit. Choosing `B(p)` merely writes
a section of this bundle as `[B(p),psi(p)]`. If another choice is
`B'(p)=B(p)r(p)` with `r(p) in K_k`, equality of the same bundle element computes

```text
[B'(p),psi'(p)] = [B(p),psi(p)]
  iff sigma(r(p))psi'(p)=psi(p)
  iff psi'(p)=sigma(r(p))^(-1)psi(p).
```

The section choice therefore changes fiber coordinates, not the physical state.

For `k=(m,0,0,0)`, the equation `R dot k=k` fixes the time axis. Preservation of
`eta` then preserves its orthogonal complement `k^perp`, where `-eta` is Euclidean.
The restriction of `Lambda(R)` to `k^perp` is therefore a spatial rotation, and
every spatial rotation extends by fixing `k`. Hence the stabilizer in `L_0` is
`SO(3)` and its preimage in `L_spin` is `Spin(3)~=SU(2)`; its irreducible unitary
actions produce the spin label. For a null `k`, the stabilizer is
different. We do not import its structure here: the massless bridge will construct
it directly from `R dot k=k` and show which part acts physically and which part becomes
gauge redundancy. The finite-helicity scope remains an assumption until that
construction is complete.

## 3. Probability conservation constructs the orbit measure and state space

A physical wavefunction assigns an internal amplitude to every allowed momentum:

```text
p |-> psi(p) in V_sigma.
```

Its total probability must not change when the momentum variables are changed by
`p |-> A dot p`. Therefore the integration rule must satisfy

```text
dmu_O(A dot p) = dmu_O(p).
```

For the retained positive-energy mass shells this rule can be constructed directly.
Start from four-volume `d4p`. Since `det Lambda(A)=1`, changing variables gives
`d4(A dot p)=d4p`. Both `p^2-m^2` and `p^0>0` are also invariant under the
connected group, so restricting four-volume gives, for `m>=0`,

```text
dmu_m(p) = d4p delta(p^2-m^2) theta(p^0),
```

To derive the spatial form, factor

```text
delta((p^0)^2-E_p^2)
 = [delta(p^0-E_p)+delta(p^0+E_p)]/(2E_p).
```

The factor `theta(p^0)` removes the negative root. Performing the `p^0` integral
therefore gives

```text
dmu_m(p) = d3p / (2 E_p),
E_p = sqrt(m^2 + |p|^2),
```

up to an overall normalization. The factor `1/(2E_p)` is not a convention inserted
by hand; it is the Jacobian of restricting invariant four-volume to the positive
mass shell. For `m=0`, take `E_p=|p|` and remove the zero momentum, which is a
different orbit and a measure-zero point for this measure.

**Theorem contract (uniqueness of orbit measure).** On each transitive massive or
nonzero massless orbit in the present scope, a nonzero invariant Radon measure is
unique up to scale. The explicit delta-function construction establishes existence;
the theorem is used only to say that another invariant probability integration rule
has the same measure class and normalization freedom.

**Definition.** The physical state space is the square-integrable section space

```text
H_(O,sigma) = L2(O_k,dmu_O;V_sigma),
```

with norm

```text
||psi||^2 = integral_O <psi(p),psi(p)>_sigma dmu_O(p).
```

This notation uses the chosen section `B(p)` to trivialize the bundle `E_sigma`.
Intrinsically, `H_(O,sigma)` consists of square-integrable sections of `E_sigma`;
changing `B(p)` changes coordinates in each fiber but not the section itself.

Let `A in L_spin`, fix the output momentum `p`, and construct its input momentum

```text
q = A^(-1) dot p.
```

The selected transport `B(q)` reaches `q`. Applying `A` after it reaches `p`:

```text
[A B(q)] dot k
  = A dot [B(q) dot k]
  = A dot q
  = A dot (A^(-1) dot p)
  = p.
```

The selected `B(p)` also reaches `p`. Their relative transformation is therefore
constructed as

```text
W(A,p) = B(p)^(-1) A B(q).
```

It fixes the standard momentum by direct evaluation:

```text
W(A,p) dot k
  = B(p)^(-1) dot [A dot (B(q) dot k)]
  = B(p)^(-1) dot p
  = k.
```

Hence `W(A,p) in K_k`. This calculation, rather than the phrase “two ways,”
constructs the residual transformation called the Wigner rotation.

Its composition law is also a calculation. Put `q=A_1^(-1) dot p`. Then

```text
W(A_1,p) W(A_2,q)
 = [B(p)^(-1) A_1 B(q)]
   [B(q)^(-1) A_2 B(A_2^(-1) dot q)]
 = B(p)^(-1) A_1 A_2 B((A_1 A_2)^(-1) dot p)
 = W(A_1 A_2,p).
```

The cancellation of `B(q)B(q)^(-1)` is the equality witness; the common semantic
endpoint is still `p`.

These constructed operations define the induced state action

```text
[U_ind(a,A)psi](p)
  = exp(i p.a) sigma(W(A,p)) psi(A^(-1) dot p).
```

The three factors now have separate origins: the translation character evaluates
`a` at the output momentum, the pullback retrieves the amplitude at the input
momentum, and `sigma(W)` converts its internal standard frame to the one selected
at `p`. Nothing in this space is yet a Lorentz tensor field or a local differential
equation.

To verify the representation law, take `g_1=(a,A_1)`, `g_2=(b,A_2)`, and again
`q=A_1^(-1) dot p`. Evaluation on the same `psi` gives

```text
[U_ind(g_1)U_ind(g_2)psi](p)
 = exp(i p.a)
   exp(i q.b)
   sigma(W(A_1,p)W(A_2,q))
   psi((A_1 A_2)^(-1) dot p)

 = exp(i p.(a+Lambda(A_1)b))
   sigma(W(A_1 A_2,p))
   psi((A_1 A_2)^(-1) dot p)

 = [U_ind(a+Lambda(A_1)b,A_1 A_2)psi](p).
```

The second equality uses exactly the two witnesses already constructed:

```text
q.b = (A_1^(-1) dot p).b = p.(Lambda(A_1)b),
W(A_1,p)W(A_2,q) = W(A_1 A_2,p).
```

Unitarity is verified independently rather than inferred from the word “induced”:

```text
||U_ind(a,A)psi||^2
 = integral_O ||sigma(W(A,p))psi(A^(-1) dot p)||^2 dmu_O(p)
 = integral_O ||psi(A^(-1) dot p)||^2 dmu_O(p)
 = integral_O ||psi(q)||^2 dmu_O(q)
 = ||psi||^2.
```

Here the phase has modulus one, `sigma` is unitary, and the final substitution uses
the already constructed invariant orbit measure.

Finally, the choice of standard transports is not physical. If
`B'(p)=B(p)r(p)`, direct substitution gives

```text
W'(A,p) = r(p)^(-1) W(A,p) r(A^(-1) dot p),
psi'(p) = sigma(r(p))^(-1)psi(p).
```

Inserting both identities into the primed action cancels the two `r` factors and
returns the same bundle section. Thus changing `B` conjugates fiber coordinates
but does not change the induced representation up to unitary equivalence.

**Theorem boundary (imprimitivity).** The calculation above constructs
`U_ind` from `(O_k,sigma)`. Conversely, a unitary representation `U` equipped with
the covariant projection-valued measure `E` constructed in Section 1, transitive
support `O_k`, and the stated regularity is unitarily equivalent to one induced
from a unitary representation of `K_k`. This exact input/output is the part of the
imprimitivity theorem used to identify the original one-particle `U` with an
`U_ind`; it is not another algebraic consequence of the displayed formulas.

## 4. The demand for a local equation constructs a covariant field

The state `psi(p)` is already physical but lives only on the mass shell and carries
momentum-dependent internal frames. A local equation instead needs values at
spacetime points that can be differentiated and compared in one fixed component
space. This extra capability introduces a finite-dimensional vector space `V_D`
and a representation `D: L_spin -> GL(V_D)`. The choice of `D` is realization
data; it was not determined by the particle classification.

A field is a function

```text
Psi: x |-> Psi(x) in V_D.
```

For `g=(a,A)`, the old event that maps to `x` is the unique solution of

```text
x = Lambda(A)y+a,
y = Lambda(A)^(-1)(x-a).
```

Evaluating the old field at this event and then expressing its value in the new
component frame constructs

```text
[T_D(a,A)Psi](x)
  = D(A) Psi(Lambda(A)^(-1)(x-a)).
```

We call `V_D` the Lorentz carrier because `D(A)` carries these component
transformations.

The inverse argument is required by the representation law. Applying `(b,B)` and
then `(a,A)` gives

```text
T_D(a,A)T_D(b,B)Psi(x)
 = D(AB) Psi(Lambda(AB)^(-1)(x-a-Lambda(A)b))
 = T_D((a,A)(b,B))Psi(x).
```

Thus this is a derived group action once `D(AB)=D(A)D(B)` is chosen; changing the
inverse or translation signs arbitrarily would break the group law.

For Fourier transformation and differential operators, a controlled starting
domain is the space of smooth rapidly decreasing fields. Plane waves and on-shell
solutions are not rapidly decreasing, so the actual solution space is allowed to
contain distributions. Denote these spaces by

```text
Gamma_D  = S(V,V_D),
Gamma_D' = S'(V,V_D).
```

This analytic choice is a tool, not a physical axiom, and can be refined later.

The carrier is deliberately larger than the physical state fiber.

**Deduction (finite carrier nonunitarity).** Suppose a nontrivial
finite-dimensional `D` preserved a positive-definite inner product. Its
differential would be a Lie-algebra map

```text
dD: sl(2,C)_real -> u(V_D).
```

The kernel is an ideal. Simplicity of `sl(2,C)_real` makes `dD` injective unless it
is zero; zero would make `D` trivial because `L_spin` is connected. On the compact
algebra `u(V_D)`, `-Tr(XY)` is a positive-definite invariant form. Pulling it back
along an injective `dD` would give `sl(2,C)_real` a positive-definite adjoint-
invariant form, which is equivalent to compactness. This contradicts the boost
subgroups of `sl(2,C)_real`. Therefore a nontrivial finite carrier is nonunitary.

`Gamma_D'` consequently includes off-shell and unphysical components; an equation,
constraints, or a gauge quotient must construct the physical unitary representation
inside it. This is the task passed to `N3/N4`.

## 5. Optional branch: treating the reference frame as a coordinate

The manuscript seeks to replace a discrete component index by continuous spin or
orientation coordinates. A spacetime origin and a spin-lifted oriented inertial
frame are specified by a pair `(x,B)` with `B in L_spin`. Fix one reference spin
frame. There is then a unique element `(x,B) in G` sending the reference origin and
frame to that pair. Conversely, acting with an element of `G` produces one such
pair. Freeness and transitivity therefore identify the configuration space with
`G` itself.
Therefore a scalar description of an oriented object naturally has the form

```text
f: (x,B) |-> complex number.
```

Changing the laboratory frame by `g` sends the group coordinate to `g^(-1)q`;
changing the body-fixed frame by `h` sends it to `qh`. Hence the two actions are
constructed as

```text
[L_g f](q) = f(g^(-1)q),
[R_h f](q) = f(qh).
```

The representation and commutation laws are verified on the same function:

```text
[L_(g_1)L_(g_2)f](q)
  = f(g_2^(-1)g_1^(-1)q)
  = [L_(g_1g_2)f](q),

[R_(h_1)R_(h_2)f](q)
  = f(qh_1h_2)
  = [R_(h_1h_2)f](q),

[L_g R_h f](q)
  = f(g^(-1)qh)
  = [R_h L_g f](q).
```

The left action changes the observer; the right action changes the oriented
object/frame recorded relative to that observer.

This produces two different function spaces because two different capabilities may
be requested.

### 5a. If the function itself is a quantum amplitude on all frames

Its norm should be unchanged by left and right frame changes. We therefore require
an integration rule `dg` satisfying

```text
integral |f(g^(-1)q)|^2 dq = integral |f(q)|^2 dq,
integral |f(qh)|^2 dq      = integral |f(q)|^2 dq.
```

**Theorem contract (group measure).** Every locally compact group has a nonzero
left-invariant measure, unique up to scale. Right translation may rescale it by a
modular factor; left and right measures coincide precisely for a unimodular group.

For the connected Lorentz group, the modular factor is one. Its action on
spacetime also has `det Lambda=1`. Consequently the semidirect product is
unimodular, and the Poincare measure factors as

```text
dg = d4x dB.
```

The invariance can be checked directly. Left multiplication maps

```text
(x,B) |-> (a+Lambda(A)x, AB),
```

whose spacetime Jacobian is `det Lambda(A)=1`; right multiplication maps

```text
(x,B) |-> (x+Lambda(B)b, BA),
```

whose full Jacobian is block triangular with unit spacetime block. Left/right
invariance of `dB` completes both checks.

Completing finite-norm functions constructs the unitary regular space

```text
F_reg = L2(G,dg).
```

The measure computations now verify the requested norm invariance:

```text
||L_g f||^2
  = integral_G |f(g^(-1)q)|^2 dq
  = integral_G |f(r)|^2 dr,

||R_h f||^2
  = integral_G |f(qh)|^2 dq
  = integral_G |f(r)|^2 dr.
```

Thus Haar measure is not background vocabulary: it is the integration rule forced
by asking left/right changes of frame to preserve total probability.

### 5b. If orientation only packages finitely many field components

Now begin with the covariant carrier `D` already constructed above. Asking for one
scalar reading of a vector `v in V_D` requires a linear functional
`lambda in V_D^*`. Reading the same field in every body-fixed frame constructs

```text
[C_(D,lambda)Psi](x,B)
  = lambda(D(B^(-1))Psi(x)).
```

This formula is pointwise on `Gamma_D`. For `Gamma_D'`, fix `B` and apply the
finite-dimensional covector `lambda compose D(B^(-1))` to the distributional
value; equivalently, pair the result with a spacetime test function. Thus the same
linear map extends to distributions without pretending that every distribution has
a point value.

As `B` varies, the same geometric field is inspected from every oriented frame. If
the linear span of

```text
{ lambda compose D(B^(-1)) | B in L_spin }
```

is all of `V_D^*`, call `lambda` cyclic. If
`C_(D,lambda)Psi(x,B)=0` for every `B`, then each covector in this span annihilates
`Psi(x)`. Cyclicity therefore computes

```text
C_(D,lambda)Psi = 0
  => ell(Psi(x))=0 for every ell in V_D^*
  => Psi(x)=0 for every x.
```

Thus `C_(D,lambda)` is injective. For an irreducible finite-dimensional complex
carrier, any nonzero `lambda` is cyclic: the span of its orbit is nonzero and is
preserved by the dual action, so irreducibility makes it all of `V_D^*`.

Reconstruction is finite but not canonical. Choose `dim V_D` group elements `B_i`
such that `lambda compose D(B_i^(-1))` form a basis of `V_D^*`; the readings
`f(x,B_i)` are then the coordinates of `Psi(x)` in the dual frame. Polynomial spin
coordinates implement the same inverse by coefficient extraction.

This function is not being introduced as a probability amplitude over all Lorentz
frames. Restriction to one boost subgroup reveals exponential-polynomial behavior,
but that subgroup has Haar measure zero and therefore does **not** alone prove
failure of square integrability. The needed incompatibility has a shorter semantic
proof.

At a fixed spacetime point, write the Lorentz coefficient of `v in V_D` as

```text
c_v(B) := lambda(D(B^(-1))v).
```

Let `W` be the set of `v` for which `c_v` is in `L2(L_spin,dB)`. Left translation
preserves `L2`, and direct substitution gives

```text
[L_A c_v](B)
 = c_v(A^(-1)B)
 = lambda(D(B^(-1)A)v)
 = c_(D(A)v)(B).
```

Therefore `W` is a `D`-invariant subspace. For irreducible `D`, either `W=0` or
`W=V_D`. Suppose `W=V_D`. Injectivity of the cyclic coefficient map would then pull
the Haar inner product back to a positive-definite inner product on `V_D`:

```text
<v,w>_c := <c_v,c_w>_(L2).
```

The displayed intertwining identity and unitarity of `L_A` compute

```text
<D(A)v,D(A)w>_c
 = <L_A c_v,L_A c_w>_(L2)
 = <c_v,c_w>_(L2)
 = <v,w>_c.
```

This would make the nontrivial finite-dimensional Lorentz carrier `D` unitary for
a positive-definite norm, contradicting the noncompact-carrier result in Section 4.
Hence `W=0`: no nonzero vector in an irreducible finite carrier produces an `L2`
Lorentz coefficient. Finite-dimensional `sl(2,C)` carriers are completely
reducible; applying the same argument to each nontrivial summand, while observing
that a trivial summand gives a nonzero constant on an infinite-volume group, gives
the same boundary for a general finite carrier. The finite generating sector

```text
F_(D,lambda) = image C_(D,lambda)
```

is an algebraic coefficient realization, not an invariant subspace of `F_reg` with
the same Hilbert norm. Gitman--Shelepin state the stronger coordinate fact for their
polynomial sectors after Eq. (106): the corresponding Haar integral diverges.

This resolves the ambiguity in “functions on the Poincare group”: the unitary
regular space and the finite polynomial generating space are constructed for
different purposes and cannot be silently identified.

## 6. The coefficient map is forced to intertwine

For `g=(a,A)`, the group inverse and product give

```text
g^(-1)(x,B)
  = (Lambda(A)^(-1)(x-a), A^(-1)B).
```

Applying the left action and then the coefficient definition to the same field
computes

```text
[L_(a,A) C_(D,lambda)Psi](x,B)
 = lambda(D((A^(-1)B)^(-1))
          Psi(Lambda(A)^(-1)(x-a)))
 = lambda(D(B^(-1))D(A)
          Psi(Lambda(A)^(-1)(x-a)))
 = [C_(D,lambda) T_D(a,A)Psi](x,B).
```

Therefore `C_(D,lambda)` preserves the left Poincare action. Under a pure right
Lorentz transformation `C`,

```text
[R_C C_(D,lambda)Psi](x,B)
 = lambda(D((BC)^(-1))Psi(x))
 = [lambda compose D(C^(-1))](D(B^(-1))Psi(x))
 = C_(D,D^vee(C)lambda)Psi(x,B),

D^vee(C)lambda = lambda compose D(C^(-1)).
```

The right action changes which body-frame component is read. Closing a selected
copy under right rotations therefore produces multiplicity in the realization. It
does not automatically produce a new physical spin: physical spin was constructed
earlier from the stabilizer of momentum, not from the right Lorentz index.

For a right translation `(b,1)`, multiplication computes

```text
(x,B)(b,1) = (x+Lambda(B)b,B),

[R_(b,1)C_(D,lambda)Psi](x,B)
 = lambda(D(B^(-1))Psi(x+Lambda(B)b)).
```

The spacetime argument now depends on the orientation `B`; right translations are
therefore not component rotations and require a separate physical interpretation.

## Constructed relation among the spaces

The construction yields

```text
translation symmetry
  -> momentum spectrum
  -> momentum orbit O_k
  -> residual frame ambiguity K_k
  -> physical Hilbert space H_(O,sigma)

locality choice + Lorentz carrier D
  -> covariant field space Gamma_D'
  -> equation/constraint/gauge quotient still required

orientation as coordinate
  -> scalar functions on G
  -> either F_reg for an invariant group-space norm
  -> or F_(D,lambda) for finite component packaging
```

The bridge passed to `N3` is therefore

```text
H_(O,sigma) --W_D--> Sol(K_D)/Gauge  inside Gamma_D'

Gamma_D' --C_(D,lambda)--> F_(D,lambda).
```

`W_D` must construct the physical particle inside the carrier. `C_(D,lambda)` only
changes how the carrier components are encoded. A direct embedding of the physical
state space into `L2(G)` is neither needed nor presumed.

## Presumptions exposed by the construction

| Presumption | Why it entered | What changes if removed |
| --- | --- | --- |
| exact translations | construct simultaneous momentum labels | momentum orbit is no longer the starting classifier |
| positive-energy single orbit | isolate one particle sector | reducible/multi-orbit states appear |
| irreducible little-group action | prevent the particle type from splitting | multiple species or degeneracy remain |
| locality in spacetime | motivates `Psi(x)` and differential equations | nonlocal/on-shell descriptions may avoid a carrier equation |
| finite Lorentz carrier | obtain finitely many conventional components | infinite-component or direct group realizations remain possible |
| orientation coordinate | replace component indices by frame dependence | ordinary covariant fields are already sufficient |
| invariant norm on all of `G` | construct `F_reg` | algebraic coefficient functions need not be square-integrable |

## Checks against the worktable and sources

- The dual-action convention is checked by
  `(A dot p).(Lambda(A)a)=p.a`; every later phase identity uses this same pairing.
- Stabilizer membership, the Wigner cocycle, the full semidirect-product
  representation law, norm preservation, and standard-section independence are
  each evaluated explicitly rather than inferred from route comparison.
- The separation `F_(D,lambda) != F_reg` is checked without treating a boost
  subgroup as positive Haar measure: an `L2` coefficient would construct a
  forbidden positive-definite invariant norm on the finite Lorentz carrier.
- The semidirect product construction exposes the missing translation in manuscript
  line 85.
- Manuscript lines 348--381 are recovered as the coordinate expansion of
  `C_(D,lambda)`, but only after its carrier and purpose are known.
- [Bekaert--Boulanger](https://arxiv.org/abs/hep-th/0611263) independently verifies
  the orbit/stabilizer construction of physical representations.
- [Stone](https://doi.org/10.2307/1968538),
  [Bargmann](https://doi.org/10.2307/1969831), and
  [Mackey](https://doi.org/10.1073/pnas.35.9.537) are the primary checks for the
  generator, ray-representation, and imprimitivity theorem contracts respectively.
- [Gitman--Shelepin 2009](../sources/gitman-shelepin-2009.md) independently verifies
  the left/right group action, coefficient expansion, and the separation between
  `L2(G)` and finite nonunitary polynomial sectors.

The sources validate the constructed objects; they are not used as substitutes for
constructing them.

## Downstream result and open boundary

- The residual-frame group is consumed by
  [N2a](02a-spin-and-helicity.md), which constructs massive spin and massless
  helicity before either is compared with a field equation.
- The massless helicity-one `W_D`, null stabilizer, and gauge quotient are now
  constructed in the
  [massless realization bridge](03b-massless-helicity-one.md).
- Decide whether the right-type closure carries physical information beyond a
  redundant component-reading frame.
- Determine whether a group-function operator can reduce work across a family of
  carriers, rather than merely repackage one already chosen carrier.

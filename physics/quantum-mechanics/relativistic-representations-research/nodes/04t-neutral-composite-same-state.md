# N4t — Neutral Composite Same-State Test

Status: dressed-atom fiber band and Rayleigh asymptotic channel supported under
explicit model contracts; prepared spectral-weight equality computed internally;
relativistic particle and vacuum-interpolator lifts remain open  
Consumes: [N4r field/mechanics projection](04r-field-mechanics-stability.md),
[N4s field/particle extraction](04s-field-particle-extraction.md), and
[neutral-composite source contracts](../sources/neutral-composite-fiber-contracts.md)  
Produces: one same-state diagram joining prepared mechanical spectral weight, the full
field spectral band, and the zero-photon dressed-atom scattering channel, plus
the exact boundary between a nonrelativistic quasiparticle and a Wigner particle

## Node contract

- **Question/capability:** in one neutral composite model, do prepared mechanical
  spectral weight,
  recovery, full-field spectral selection, and asymptotic particle extraction
  refer to the same state?
- **Presumptions:** NC-01 or NC-02 constructs a self-adjoint translation-
  invariant Hamiltonian and its total-momentum fibers. The rank-one calculation
  uses NC-02's simple dressed ground state `psi_P` on a measurable momentum
  region `B`; NC-01 alone supplies existence and may require the finite-rank
  version in Section 6. A chosen bare mechanical preparation has nonzero overlap
  with the target fiber. The stronger scattering statements use NC-02's
  additional infrared-cutoff, small-coupling, energy, and velocity hypotheses.
- **Output:** an invariant band isometry `W`, its decomposable spectral projector
  `P_das`, a normalized preparation whose spectral projection equals `Wf`, and
  an asymptotic wave-operator identity selecting that same vector.
- **Boundary:** this node does not construct a Lorentz representation, create an
  atom from the vacuum with a local field, evaluate `E_g(P)`, or prove the
  nonzero-overlap assumption.

## 1. Construct the model from the physical split

Take one electron and one dynamical nucleus. Their positions construct center-of-
mass and relative variables

```text
X=(m_e x_e+m_n x_n)/M,
x=x_e-x_n,
M=m_e+m_n,
mu=m_e m_n/M.
```

The meaning of this transformation is not “choose useful coordinates.” `X`
records the action of spatial translations on the whole composite; `x` is
unchanged by that action and therefore records its internal mechanics. Couple
this pair to a radiation Fock space. In the simplified NC-02 model the Hamiltonian
has the semantic form

```text
H_g=P_X^2/(2M)+H_at+H_f+g Phi(G_(X,x)),
H_at=p_x^2/(2mu)+V(x).
```

The interaction translates the matter and field together. Hence the conserved
generator is not `P_X` but

```text
Pi=P_X+P_f,
[H_g,Pi]=0.
```

The joint spectral theorem, not a component ansatz, then constructs

```text
mathcal_H=direct-integral_(R^3) mathcal_H_P dP,
H_g=direct-integral_(R^3) H_g(P) dP,

H_g(P)=(P-P_f)^2/(2M)+H_at+H_f+g Phi(F_x).
```

The same structure holds for the Pauli--Fierz model of NC-01 with its transverse
vector potential. `H_at` is the uncoupled internal mechanics. `H_g(P)` is the
full field dynamics at fixed total momentum. They must not be identified.

## 2. The dressed atom is a band of field states

On a momentum region `B`, use NC-02's simple-eigenvalue contract (or impose the
same simplicity hypothesis on another model):

```text
H_g(P) psi_P=E_g(P) psi_P,
||psi_P||=1,
P_b(P)=|psi_P><psi_P|.
```

Choose the phase measurably. Construct

```text
W:L^2(B,dP)->H,
(Wf)(P)=f(P)psi_P.
```

The direct-integral norm computes

```text
||Wf||^2
 =integral_B |f(P)|^2 ||psi_P||^2 dP
 =||f||^2.
```

Thus `W` is an isometry. Its range is the dressed-atom band

```text
H_das=Ran W,
P_das=WW^dagger=direct-integral_B P_b(P)dP.
```

Apply the full operators to the same vector:

```text
H_g Wf=W(E_g f),
Pi Wf=W(P f).
```

This constructs a stable translation-covariant dispersive object. No center-of-
mass trajectory or internal wavefunction expansion is required. It also shows
what is still absent: translations determine the graph `(E_g(P),P)`, but without
boosts they do not make it a Poincare orbit.

## 3. Mechanical preparation detects the same band

Let `phi_0` be a normalized bound state of `H_at`, and inject the bare
mechanical preparation into each field fiber by

```text
J_P phi=phi tensor Omega_f.
```

Define its overlap with the exact dressed atom by

```text
c(P)=<psi_P,J_P phi_0>.
```

The condition `c(P)!=0` is a physical access condition: the preparation can
actually excite the dressed state. It is not implied merely by the existence of
`psi_P`.

The prepared resolvent is

```text
G_P(z)=J_P^dagger(z-H_g(P))^(-1)J_P.
```

The spectral theorem first gives a statement that remains valid when the
eigenvalue lies at a continuum threshold:

```text
s-lim_(epsilon down to 0)
  i epsilon G_P(E_g(P)+i epsilon)
 =J_P^dagger P_b(P)J_P.
```

Indeed the scalar multiplier `i epsilon/(E_g(P)+i epsilon-lambda)` tends to one
at `lambda=E_g(P)`, to zero elsewhere, and is uniformly bounded. Thus the strong
limit selects exactly the prepared spectral atom. If the eigenvalue is isolated,
the same statement can be written as a meromorphic residue:

```text
<phi_0,G_P(z)phi_0>
 =|c(P)|^2/(z-E_g(P))+regular,

Res_(z=E_g(P)) G_P(z)
 =J_P^dagger P_b(P)J_P.
```

The prepared spectral atom—and the residue when isolation permits that
language—contains the exact branch energy and prepared weight. It is not the
full dressed state. Recover that state without choosing components by
normalizing the full spectral projection:

```text
r_P=P_b(P)J_P phi_0/c(P)=psi_P.
```

Here the inner-product convention fixes the harmless conjugation/phase choice;
equivalently define `r_P` as the unique phase-normalized vector on the ray
`P_b(P)J_P phi_0`. The equation is directly verifiable because

```text
P_b(P)J_P phi_0
 =psi_P <psi_P,J_P phi_0>
 =c(P)psi_P.
```

At a massless threshold, `E_g(P)-Q_PH_g(P)Q_P` need not be invertible. Therefore
N4r's pointwise Schur recovery `K_P(E_g(P))` cannot be inserted by notation. If a
massive-photon/gapped regulator makes that inverse exist, the Feshbach theorem
gives the same ray:

```text
K_P(E_g(P)) J_P^dagger psi_P=psi_P.
```

Without that gap, the spectral projection or a threshold Feshbach theorem owns
the recovery. This is a correction to the previous proposed computation, not a
technical footnote.

## 4. Global spectral selection gives the same state

For a wave packet `f` supported where `c(P)!=0`, construct the normalized bare
preparation

```text
(Cf)(P)=f(P) J_P phi_0/c(P).
```

It need only be defined where `1/c` is bounded enough for `Cf` to lie in the
Hilbert space. Fiberwise computation gives

```text
(P_das Cf)(P)
 =f(P)P_b(P)J_P phi_0/c(P)
 =f(P)psi_P
 =(Wf)(P).
```

Hence

```text
P_das Cf=Wf.
```

This is the exact mechanics/field same-state identity. The left side says “start
from an internally bound mechanical preparation and retain only its exact
dressed field band.” The right side says “construct the full dressed-atom wave
packet.” Both operations return the same vector, not merely the same energy.

`P_das` is the joint spectral projection of `(H_g,Pi)` onto the measurable graph
`{(E_g(P),P):P in B}` when that graph is a separated measurable spectral
component. At a threshold, it is more safely treated as the decomposable
eigenprojection above; calling it an isolated shell would overstate the theorem.

## 5. The asymptotic channel retains the same atom

NC-02 constructs asymptotic photon operators and a wave operator

```text
Omega_+:
H_das tensor F_as -> H.
```

For a dressed atom and `n` free photons it gives

```text
Omega_+(Wf tensor a^*(h_1)...a^*(h_n)Omega)
 =a_+^*(h_1)...a_+^*(h_n)Wf.
```

Set `n=0`. The definition computes

```text
Omega_+(Wf tensor Omega)=Wf.
```

Combining this with the previous section yields the promised same-state diagram:

```text
mechanical preparation Cf
  -- full spectral band projection P_das --> Wf
  <-- prepared spectral atom plus normalized recovery -- G_P(z)
  <-- zero-photon asymptotic channel -------- Omega_+(Wf tensor Omega).
```

With asymptotic photons, the same `Wf` remains the atomic factor while the
created `a_+^*(h)` factors record radiation escaping from it. Under NC-02's
stronger hypotheses, asymptotic completeness says that every state below the
restricted ionization/velocity threshold is assembled from this dressed-atom
band and asymptotically free photons.

This is stronger than a formal pole analogy: one spectral vector has been shown
to serve as prepared bound composite, exact field eigenstate, and asymptotic
atom. It is weaker than N4s's relativistic claim for two exact reasons.

## 6. What generalizes, and what does not

The reusable construction is

```text
conserved translations
 -> direct-integral fibers H(P)
 -> finite-rank stable eigenbundle P_b(P)
 -> band isometry W and projector P_b
 -> prepared spectral-weight/access test
 -> model-appropriate wave operator.
```

Rank one is not essential. For a finite internal multiplicity, replace `psi_P`
by a measurable fiber `V_P`, `P_b(P)` by its finite-rank projection, and `c(P)`
by the preparation map

```text
C(P)=P_b(P)J_P:M_P->V_P.
```

The exact access condition is then surjectivity of `C(P)` on the desired
particle fiber; a measurable right inverse replaces division by the scalar
`c(P)`. This is the common finite-spin extension of the same-state calculation.

What does **not** transfer automatically:

- `E_g(P)` is an arbitrary nonrelativistic dispersion, not
  `sqrt(M_b^2+|P|^2)`;
- the model has no Lorentz boosts, so no Wigner spin or helicity is extracted;
- it works in a fixed one-atom matter sector, so there is no vacuum-to-atom local
  interpolator `B` and no literal test of N4s's `E(Sigma)B Omega` quotient;
- NC-02's asymptotic completeness uses scalar photons and a positive infrared
  interaction cutoff;
- NC-01's more physical neutral Pauli--Fierz ground-state theorem does not by
  itself supply the same scattering theorem.

Therefore the node validates the **architecture** of the field/mechanics/particle
bridge and falsifies the claim that translation fibers alone complete the
relativistic particle construction.

## 7. Computability verdict and next dependent question

The semantic compression is real:

- the composite state is represented by a finite-rank eigenbundle rather than a
  full field history;
- all three descriptions meet at the projector `P_b(P)`;
- the observable branch is `E_g(P)` and its prepared weight is the spectral atom
  `J_P^dagger P_b(P)J_P`, also a residue when the eigenvalue is isolated;
- escaping radiation is handled by asymptotic photon data, not by following all
  field configurations in time.

The dependent comparison is now carried out in
[N4u](04u-effective-mass-route-audit.md). It chooses the effective mass

```text
1/M_eff=(1/3) Delta_P E_g(P)|_(P=0):

direct fiber spectral computation
versus
prepared-resolvent/self-energy differentiation.
```

N4u finds that exact self-energy notation alone relocates the complementary
inverse. Genuine reduction first appears at weak coupling, where the order-`g^2`
field problem becomes one atomic-resolvent momentum integral. That result does
not yet evaluate `P_b(P)` or `c(P)` beyond the selected observable.
Separately, the relativistic continuation must construct a local neutral
interpolator and prove that its Poincare-shell projection is the covariant
counterpart of this band. [N4v](04v-relativistic-mass-shell.md) now constructs
the conditional shell kinematics and exact mass coincidence, but it does not
make this nonrelativistic model Lorentz covariant or supply the missing
interpolator.

## Edges

- `N4r -> N4t`: pass the prepared resolvent, spectral weight, and gapped recovery
  map, with the threshold-invertibility obligation kept explicit.
- `N4s -> N4t`: pass the same-state target and the distinction between spectral
  stability and asymptotic extraction.
- `NC-01 -> N4t`: pass the neutral Pauli--Fierz fiber and ground-state theorem.
- `NC-02 -> N4t`: pass the simple dressed band, wave operator, and restricted
  Rayleigh completeness theorem.
- `N4t -> N4s`: return a successful nonrelativistic same-state test together
  with the two missing relativistic arrows: vacuum interpolation and Poincare
  covariance.
- `N4t -> N4u`: pass `E_g(P)`, `P_b(P)`, the prepared spectral atom, and the
  two-route effective-mass cost question.
- `N4t -> N4v`: pass the translation-covariant band and the absence of boosts as
  the regression case in which rest energy and curvature mass remain independent.

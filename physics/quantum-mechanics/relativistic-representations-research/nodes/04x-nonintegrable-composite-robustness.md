# N4x — What Survives When the Breather Loses Integrability?

Status: channel-preserving and channel-destroying deformations constructed;
first-order mass tangent and finite stability certificate supported conditionally
on certified reference form factors and remainder bounds; numerical tangent,
all-orders continuum construction, and large-coupling continuation remain open  
Consumes: [N4s field/particle extraction](04s-field-particle-extraction.md),
[N4v relativistic shell closure](04v-relativistic-mass-shell.md),
[N4w sine-Gordon breather regression](04w-sine-gordon-breather-rest-pole.md),
[nonintegrable source contracts](../sources/nonintegrable-composite-contracts.md),
and [stability regression](../computation/04x-nonintegrable-robustness/README.md)  
Produces: one explicit nonintegrable deformation in which the N4w constituent
channel survives, a one-form-factor rest-mass tangent, a finite stability and
field-access certificate, the exact shell that survives independently of
factorization, and one counter-deformation that forces a new confined-particle
basis

## Node contract

- **Question/capability:** which parts of N4w describe a relativistic stable
  composite, and which parts describe only an integrable solution method?
- **Presumptions:** NI-01--06 and N4w's exact sine-Gordon reference data; small
  renormalized deformation parameter; Poincare-invariant continuum theory in the
  regime being discussed; certified mass/remainder bounds before a stability
  claim is promoted.
- **Construction:** deform the same reference theory in two ways. The second
  harmonic preserves the old soliton sector but destroys factorization. The
  half-frequency harmonic preserves Poincare and reflection symmetry while
  destroying the old single-soliton sector.
- **Semantic computation:** evaluate both perturbations on the old vacua and in
  the soliton semilocality residue; reduce the surviving particle's first mass
  tangent to crossed diagonal form factors; propagate certified mass bounds to a
  threshold-gap bound; apply N4v only after that gap remains positive.
- **Output boundary:** no numerical deformation radius is claimed until the
  diagonal form factors and remainders have been evaluated in one normalization.
  No exact sine-Gordon mass formula is carried to nonzero deformation.

## 1. The audit needs two deformations, not one analogy

N4w uses one exact chain:

```text
factorized soliton S-matrix
  -> physical-strip pole
  -> exact breather mass and fusion residue
  -> local form-factor access
  -> stable Poincare shell.
```

One small perturbation can show that a result continues, but cannot identify why.
Use a survival/failure pair with the same reference model:

| Deformation | Poincare | `phi -> -phi` | old single soliton | integrability |
| --- | --- | --- | --- | --- |
| `Psi_2=cos(2 beta phi)` | preserved | preserved | survives the locality/vacuum test | generically broken |
| `Psi_(1/2)=cos(beta phi/2)` | preserved | preserved | confined | broken |

The common spacetime and reflection symmetries cannot explain the different
outcomes. The discriminating datum is locality relative to the constituent
sector, equivalently the vacuum energy encountered across one old soliton.

## 2. Construct a controlled channel-preserving benchmark

Take the canonical sine-Gordon reference action from N4w and add

```text
S_lambda=S_SG+lambda integral d^2x Psi_2(x),
Psi_2(x)=cos(2 beta phi(x)).
```

The added term is a Lorentz scalar and is even under `phi -> -phi`. It therefore
preserves Poincare covariance and the charge-conjugation action that exchanges
soliton and antisoliton.

Choose

```text
xi=1/5,
beta^2=8 pi xi/(1+xi)=4 pi/3.
```

This coupling is selected by a typed ultraviolet and infrared check, not because
it makes a familiar formula short. In canonical normalization the total scaling
dimension of `cos(alpha phi)` is

```text
x_alpha=alpha^2/(4 pi).
```

Substituting `alpha=2 beta` and the constructed `beta^2` gives

```text
x_(2 beta)=beta^2/pi=4/3<2.
```

The perturbation is relevant. NI-03's strict two-frequency condition evaluates
on the same parameters as

```text
alpha beta=2 beta^2=8 pi/3<4 pi.
```

Thus no extra periodic interaction is required by that first-order
renormalizability test. Since `alpha != beta` and both couplings are nonzero,
NI-03 identifies this as a generic nonintegrable two-frequency model.

At `xi=1/5`, N4w gives `n xi<1` for `n=1,2,3,4` and

```text
r:=m_1/M_s=2 sin(pi/10)=(sqrt(5)-1)/2.
```

The equality to the radical is a scalar trigonometric evaluation; the
[regression](../computation/04x-nonintegrable-robustness/README.md) checks the
numerical value without using it as a premise. The first breather is the lightest
reference particle, so its first multiparticle threshold is

```text
T_0=min(2M_s,2m_1)=2m_1,
d_0=T_0-m_1=m_1=r M_s>0.
```

This relatively large initial gap makes the benchmark suitable for a robustness
test. It does not predetermine the sign of its mass shift.

## 3. The vacuum and semilocality computations preserve the constituent channel

An old sine-Gordon vacuum has

```text
phi_q=2 pi q/beta,  q in Z.
```

Evaluate the new interaction on that same input:

```text
Psi_2(phi_q)
 =cos(2 beta (2 pi q/beta))
 =cos(4 pi q)
 =1.
```

Every old vacuum receives the same perturbing potential value. The combined
potential still has the old period `2 pi/beta`; a configuration crossing one old
soliton does not leave behind a region with energy density proportional to its
length.

NI-02 provides an independent momentum-space witness. For
`Psi=cos(alpha phi+delta)`, define the annihilation-residue coefficient

```text
C_+/-=cos(delta)-cos(delta -/+ 2 pi alpha/beta).
```

For `alpha/beta=2` and `delta=0`, direct substitution on both signs gives

```text
C_+/-=1-cos(+/-4 pi)=0.
```

The soliton semilocality phase is one, so the crossed diagonal form factor has no
confining annihilation pole. The two witnesses have the same content:

```text
same perturbing energy on adjacent old vacua
  <=> no linear string energy across one soliton
  <=> zero semilocal annihilation residue.
```

This establishes that the *obstruction* responsible for confinement is absent.
It does not by itself establish an all-orders soliton pole; that existence remains
part of the small-deformation spectral contract below.

## 4. One crossed form factor constructs each first mass tangent

Let `x=4/3` be the scaling dimension of `Psi_2`, fix the unperturbed physical
soliton mass `M_s`, and define the dimensionless perturbation

```text
eta=lambda/M_s^(2-x).
```

For a reference particle `a`, NI-01 constructs the first correction from the
connected crossed diagonal value

```text
m_a(eta)^2
 =m_a(0)^2+2 lambda F_(a anti-a)^Psi_2(i pi)+O(lambda^2).
```

Define dimensionless reference data

```text
f_s=F_(s anti-s)^Psi_2(i pi)/M_s^x,
f_1=F_(11)^Psi_2(i pi)/M_s^x.
```

Both are scalars: Poincare covariance has already removed momentum dependence,
crossing places the external particle on the same rest-shell question, and the
charge-conjugation-even perturbation gives equal soliton and antisoliton shifts.
Taking the positive square root around `eta=0` computes

```text
M_s(eta)/M_s=1+eta f_s+O(eta^2),
m_1(eta)/M_s=r+eta f_1/r+O(eta^2).
```

The square-root witness is

```text
(1+eta f_s)^2=1+2 eta f_s+O(eta^2),
(r+eta f_1/r)^2=r^2+2 eta f_1+O(eta^2).
```

NI-04 constructs `f_s` and `f_1` from exact reference-theory exponential form
factors. Their integral evaluation and analytic continuation are substantial
computation and remain bound to the N4x computation branch. The conceptual node
promotes only the reduction:

```text
generic nonintegrable rest-spectrum tangent
  -> two crossed diagonal scalar form factors,
not
  -> an exact deformed mass formula.
```

## 5. Certified mass bounds produce a finite stability radius

A formal first derivative does not prove that a pole remains stable. Suppose a
form-factor/finite-volume computation certifies, for `|eta|<=eta_*`,

```text
|M_s(eta)/M_s-1| <= C_s |eta|,
|m_1(eta)/M_s-r| <= C_1 |eta|.
```

These constants include the first tangent and its controlled remainder; they are
not merely `|f_s|` and `|f_1/r|` unless the remainder has separately been bounded.

The lowest neutral threshold at the deformed coupling is

```text
T(eta)=min(2M_s(eta),2m_1(eta)).
```

Apply the two input bounds to each argument of the minimum:

```text
T(eta)/M_s
 >=min(2-2C_s|eta|,2r-2C_1|eta|)
 >=min(2,2r)-2 max(C_s,C_1)|eta|.
```

The second inequality can be checked branch by branch: whichever undeformed
argument realizes the minimum loses at most the larger declared error. The
upper mass bound is

```text
m_1(eta)/M_s<=r+C_1|eta|.
```

Subtracting quantities with the same energy target gives the stability
certificate

```text
d(eta)/M_s
 :=[T(eta)-m_1(eta)]/M_s
 >=d_0/M_s-[2 max(C_s,C_1)+C_1]|eta|.
```

Therefore

```text
|eta|<min(eta_*, (d_0/M_s)/(2 max(C_s,C_1)+C_1))
```

guarantees `d(eta)>0`. At the benchmark, `d_0/M_s=r`. This bound remains valid
even if the identity of the lowest threshold changes. The regression tests it
against every sign choice of adversarial mass shifts at the declared bounds.

The certificate is computable but not yet numerical physics: its predictive
radius awaits certified `C_s,C_1,eta_*`. This is the precise current frontier.

## 6. Stability, not factorization, carries the pole and shell

Assume the certificate in Section 5 and a continuum construction in which the
soliton channel and local fields exist. The stable `B_1(eta)` spectral atom then
has a simple one-particle pole. Near that pole, the full, generally inelastic
soliton--antisoliton amplitude has the local form

```text
A_(s anti-s -> s anti-s)(s;eta)
 =Gamma_out(eta) Gamma_in(eta)
    /(s-m_1(eta)^2+i0)
  +terms regular at the pole.
```

This equation is a general isolated-state residue contract. It does not say that
the rest of the amplitude factorizes. The input channel and output channel meet
the same spectral projector; inserting that rank-one projector between the two
channel maps constructs `Gamma_in` and `Gamma_out`. Unitarity relates them after
normalizations are fixed.

Because the deformed action remains Poincare invariant, N4v acts on the resulting
sharp orbit and computes

```text
E_1(P;eta)=sqrt(m_1(eta)^2+P^2),
partial_P^2 E_1(0;eta)=1/m_1(eta).
```

The same mass appears because both expressions evaluate the invariant
`p_mu p^mu=m_1(eta)^2` on the positive orbit. No factorized S-matrix is used in
this step. Thus the exact shell *shape* is robust; its rest mass and existence
remain dynamical.

What is lost at nonzero `eta` is equally explicit:

- two-body amplitudes no longer determine all multiparticle amplitudes;
- particle-production channels and additional cuts are allowed;
- the N4w trigonometric mass formula no longer evaluates the deformed mass;
- the deformed fusion residue is not generated from an elastic bootstrap;
- higher mass corrections require regulated spectral sums, disconnected terms,
  any scheme-required ultraviolet subtractions, and NI-05's finite-volume
  computation.

## 7. Local field access survives under one checkable inequality

Let `A` be the odd local exponential combination used in N4w and define its
deformed one-particle overlap

```text
Z_A(eta)=<B_1(eta),A Omega_eta>.
```

N4w supplies `Z_A(0)!=0`. If a continuum or finite-volume computation proves

```text
|Z_A(eta)-Z_A(0)|<|Z_A(0)|,
```

the reverse triangle inequality on the same complex amplitude gives

```text
|Z_A(eta)|
 >=|Z_A(0)|-|Z_A(eta)-Z_A(0)|
 >0.
```

N4s can then quotient all interpolators with zero shell overlap and recover the
same deformed particle space. Reflection symmetry makes the odd sector readable,
but symmetry alone does not prove the strict inequality; the overlap computation
does.

## 8. A symmetry-preserving counter-perturbation destroys the old channel

Now instead add

```text
tilde Psi=cos(beta phi/2),
tilde S=S_SG+tilde lambda integral d^2x tilde Psi.
```

This is again a Poincare scalar and even under `phi -> -phi`. Evaluate it on the
same old vacua:

```text
tilde Psi(phi_q)=cos(pi q)=(-1)^q.
```

Adjacent old vacua no longer have equal energy. A soliton--antisoliton pair
separated by length `L` encloses the other vacuum value, so its excess energy has
a term proportional to `|tilde lambda| L`. The original separated soliton states
are not asymptotic states.

The NI-02 residue computes the same obstruction with
`alpha/beta=1/2`, `delta=0`:

```text
tilde C_+/-=1-cos(+/- pi)=2!=0.
```

The first-order single-soliton mass formula diverges because it is being applied
to a state that the deformed theory does not contain. This is a semantic failure,
not a need for more terms in the same particle expansion. NI-06 constructs the
replacement question:

```text
old separated soliton pair
  -> linearly confined pair
  -> new neutral meson spectrum.
```

Breather-like neutral states may continue or mix into those mesons, but N4w's
single-soliton fusion map is no longer their valid constituent realization.

## 9. Whole-route computability audit

The comparison separates three strengths of result:

| Query | Smallest supported input | Output | Cost boundary |
| --- | --- | --- | --- |
| exact integrable rest mass | one physical-strip pole angle and `M_s` | exact `m_1` | constructing the exact factorized theory is model-specific |
| first nonintegrable tangent | two connected diagonal reference form factors | `dM_s/deta`, `dm_1/deta` at zero | integral continuation and normalization still need execution |
| certified survival interval | form-factor tangents plus uniform remainder bounds | positive threshold gap and nonzero access | finite-volume/continuum extrapolation supplies the bounds |
| finite deformation | regulated Hamiltonian or Euclidean field calculation | mass, residue, thresholds, widths | no bootstrap compression; spectral sums and renormalization grow |
| confining deformation | string tension and new two-body/field kernel | meson spectrum | the particle basis itself has changed |

The robust compression is local in coupling and observable:

```text
all deformed momentum fibers
  -> one rest-mass tangent plus one stability certificate
  -> exact Poincare shell.
```

It does not turn a generic interacting field theory into an integrable one. The
form factor is a compressed exact-reference matrix element, while the stability
bound names the additional evidence needed to keep that compression honest.

## 10. Verdict and supported frontier

Supported:

- `cos(2 beta phi)` at `xi=1/5` is a relevant, Poincare- and reflection-
  preserving, generically nonintegrable deformation satisfying NI-03's stated
  first-order two-frequency conditions;
- evaluating the perturbation on old vacua and in the semilocal residue removes
  the confinement obstruction and preserves the meaning of the old constituent
  channel locally in coupling;
- the first soliton and breather mass tangents reduce to two crossed diagonal
  scalar form factors of the exact reference theory;
- certified mass bounds imply an explicit positive stability radius without
  assuming which threshold remains lowest;
- a stable deformed pole retains a general channel residue and an exact Poincare
  dispersion even though factorization and the exact sine-Gordon mass formula
  are gone;
- `cos(beta phi/2)` is a falsifier: it preserves the same manifest spacetime and
  reflection symmetries but confines the old soliton and requires a meson basis.

Open:

- evaluate `f_s` and `f_1` in one consistent normalization;
- produce `C_s,C_1,eta_*` from finite volume plus continuum and truncation-error
  control;
- compute the deformed residue and local overlap rather than assuming their
  continuity;
- determine the first inelastic process and its order in `eta`;
- construct the complete local continuum model and compare the whole route with
  direct truncated-space or lattice spectral computation;
- test which contract transfers to a nonintegrable `3+1`-dimensional composite.

The next smallest predictive node is therefore **not another general pole
discussion**. It is the isolated NI-04 computation of `f_s,f_1` at `xi=1/5`,
followed by a finite-volume remainder estimate. Those outputs would turn the
present symbolic radius into the first numerical nonintegrable composite
prediction on this route.

## Edges

- `N4s -> N4x`: pass the nonzero local-shell access test and the rule that a
  resonance or confined meson is not a defective stable-particle quotient.
- `N4v -> N4x`: pass exact propagation from any certified sharp rest mass to its
  Poincare shell and curvature.
- `N4w -> N4x`: pass the exact reference mass, stability gap, soliton fusion
  channel, and local exponential-field form factors.
- `NI-01/NI-04 -> N4x`: pass the first mass-tangent reduction and the exact
  reference form-factor representation.
- `NI-02/NI-03 -> N4x`: pass the locality, vacuum, relevance,
  renormalizability, and nonintegrability tests.
- `NI-05/C4x -> N4x`: pass the higher-order computation contract and finite
  stability-bound regression.
- `NI-06 -> N4x`: pass the confined-meson replacement for the failed constituent
  channel.
- `N4x -> N7/manuscript synthesis`: pass the distinction between robust
  Poincare/spectral particle structure and integrability-specific exact
  computation.
- `N4x -> nonintegrable mass computation`: pass the exact scalar inputs,
  normalization obligations, and remainder certificate that must be evaluated.
- `N4x -> N9b`: pass the nonintegrable form-factor/remainder boundary so the
  integrable spectral-sum route is not generalized without evidence.

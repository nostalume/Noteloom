# N4w — Sine-Gordon Breather as a Relativistic Composite Regression

Status: model selection, pole-to-mass construction, first-breather stability,
field-access bridge, and shell propagation supported within the exact factorized
S-matrix/form-factor contracts; absolute scale requires one renormalized mass
input, and a complete local-net construction with bound states remains open  
Consumes: [N4r field/mechanics projection](04r-field-mechanics-stability.md),
[N4s field/particle extraction](04s-field-particle-extraction.md),
[N4v relativistic mass-shell closure](04v-relativistic-mass-shell.md),
[sine-Gordon source contracts](../sources/sine-gordon-breather-contracts.md),
and [pole regression](../computation/04w-sine-gordon-breather/README.md)  
Produces: one selected relativistic neutral-composite test, its exact renormalized
mass ratio, a pole/fusion/local-field same-particle bridge, a stability gap, and
the precise locality and three-dimensional fidelity boundaries

## Node contract

- **Question/capability:** can one interacting relativistic model compute a
  neutral composite rest pole and connect it to both a field-created particle
  shell and its constituent scattering channel?
- **Presumptions:** the attractive quantum sine-Gordon factorized S-matrix,
  particle spectrum, and local exponential-field form factors satisfy SG-01--03.
  The physical soliton mass `M_s` is a renormalization input. The full local-QFT
  completion is not inferred from the bootstrap data.
- **Representation choice:** rapidity is the intrinsic coordinate on a positive
  mass orbit in `1+1` dimensions. Complex rapidity is used only to locate an
  analytic scattering pole; it is not interpreted as an observable constituent
  momentum.
- **Output:** the first-breather mass `m_1`, its binding below the
  soliton--antisoliton threshold, its exact Poincare dispersion and curvature,
  and the normalized coincidence of the scattering-fusion and local-field
  particle maps.
- **Boundary:** this is an integrable `1+1`-dimensional regression. It does not
  solve relativistic hydrogen, derive the exact S-matrix from a generic action,
  or close the currently open operator-domain and strict-locality problems for
  bound-state wedge fields.

## 1. Select a model by the obligations, not by familiarity

The requested test must simultaneously expose:

```text
a relativistic interacting field dynamics,
a neutral bound object,
a computable rest pole,
a sharp stable one-particle shell,
a field operator with nonzero access,
and a route back to constituent mechanics or scattering.
```

Four nearby candidates behave differently:

| Candidate | Rest-pole computation | Field/particle bridge | Verdict for first test |
| --- | --- | --- | --- |
| relativistic QED hydrogen | no controlled exact pole or sharp-shell construction at the required level | physically correct target, but local neutral-atom interpolation and infrared stability are unresolved | retain as fidelity target |
| ladder Bethe--Salpeter scalar atom | numerically executable after truncation | the truncation need not preserve the exact field spectral state or crossing/unitarity | useful approximate computation, not an exact regression |
| [massless Schwinger model](https://doi.org/10.1103/PhysRev.128.2425) | exact gauge-generated massive mode | strong field-to-particle reconstruction, but no nontrivial two-body bound-state pole or scattering test | retain as a mass-generation control |
| sine-Gordon / massive-Thirring neutral sector | exact bound-state pole and mass ratios | soliton--antisoliton fusion and local form factors reach the same neutral breather shell | selected |

The selection does not claim that lower dimension is more realistic. It minimizes
the unsupported arrows in the specific N4r/N4s/N4v diagram. The model is
nontrivial where our question is nontrivial: binding, field access, relativistic
shell covariance, and scattering are all present.

## 2. Construct the physical input and its renormalized parameters

Use the sine-Gordon action convention

```text
S[phi]=integral d^2x
  [ (1/2) partial_mu phi partial^mu phi
    +(mu/beta^2)(cos(beta phi)-1) ].
```

The displayed action names the local interaction but does not by itself define
the quantum theory: normal ordering, the meaning of `mu`, and the ultraviolet
completion are convention dependent. Replace the bare dimensional coefficient
by one physical renormalization condition:

```text
M_s = measured or otherwise fixed soliton pole mass.
```

The remaining dimensionless coupling is encoded by

```text
xi=beta^2/(8 pi-beta^2).
```

The attractive regime `0<beta^2<4 pi` is exactly `0<xi<1`. SG-04 supplies an
exact mass--coupling theorem if a specific ultraviolet normalization of `mu` is
needed. This node instead uses `M_s` as the scale, because a dimensionful theory
cannot predict an absolute number before one scale is fixed. Its nontrivial
renormalized predictions are dimensionless mass ratios and scattering data.

Coleman's correspondence identifies the sine-Gordon neutral sector with the
massive-Thirring neutral sector and the soliton with the Thirring fermion, under
the stated coupling and operator-normalization contract. Therefore the neutral
breather can be read in two compatible ways:

```text
sine-Gordon:       neutral excitation of the interacting scalar field,
massive Thirring:  fermion--antifermion bound state.
```

The correspondence supplies interpretation and an independent presentation. It
does not replace the pole computation below.

## 3. A physical-strip pole constructs the composite rest mass

A soliton of mass `M_s` on the positive orbit is parametrized by rapidity:

```text
p(theta)=M_s(cosh theta,sinh theta).
```

For two real rapidities, Lorentz invariance makes their difference
`theta=theta_1-theta_2` the scattering variable. In the center-of-momentum frame
put `theta_1=theta/2` and `theta_2=-theta/2`. The total invariant is computed on
the same two-particle input:

```text
s(theta)
 =[p(theta/2)+p(-theta/2)]^2
 =4 M_s^2 cosh^2(theta/2).
```

SG-01 gives simple soliton--antisoliton poles in the physical strip at

```text
theta=i u_n,
u_n=pi(1-n xi),
n xi<1.
```

Continue the already constructed invariant to that pole:

```text
m_n^2=s(i u_n)
     =4 M_s^2 cos^2(u_n/2).
```

Because `0<u_n<pi`, the positive rest energy is

```text
m_n=2 M_s cos(u_n/2)
   =2 M_s sin(n pi xi/2).
```

The second equality evaluates the substitution
`u_n=pi(1-n xi)` inside the same scalar invariant. This is the rest-pole
computation: the analytic pole supplies `u_n`, relativistic two-body kinematics
maps it to one real invariant mass, and the positive-energy choice selects the
physical root. No relative-coordinate wavefunction or Bethe--Salpeter component
expansion occurs.

For the first breather,

```text
m_1/M_s=2 sin(pi xi/2),
Delta_bind=2M_s-m_1>0.
```

The absolute mass is fixed once the physical input `M_s` is fixed. At the
one-breather benchmark `xi=1/2`,

```text
u_1=pi/2,
m_1=sqrt(2) M_s,
Delta_bind=(2-sqrt(2))M_s.
```

This is a renormalized prediction, not a bare-coupling perturbation series.

## 4. The pole residue constructs the fusion map

A pole location alone can be a kinematic singularity. The bound-state contract
also requires a simple pole with the physical residue sign. In the charge-neutral
channel, write its factorized neighborhood as

```text
S_(s anti-s)(theta)
 =i Gamma_n^dagger Gamma_n/(theta-i u_n)+regular.
```

Here `Gamma_n` is not imported as a Clebsch--Gordan coefficient. The residue is a
positive rank-one form on the selected multiplicity-one channel; factorizing that
form constructs `Gamma_n` up to a phase. Its domain is the analytically continued
soliton--antisoliton channel and its codomain is the one-breather fiber.

Evaluating the total momentum at the pole gives

```text
p(theta_0+i u_n/2)+p(theta_0-i u_n/2)
 =m_n(cosh theta_0,sinh theta_0).
```

Thus `Gamma_n` intertwines translations: the two constituent labels and the
breather label have exactly the same real total momentum. Factorized scattering
then uses the bootstrap residue to define every amplitude involving `B_n` from
amplitudes involving its soliton and antisoliton constituents. The composite is
therefore a reusable asymptotic species, not merely a pole name.

This is the model's replacement for a coordinate-space mechanical wavefunction:

```text
two-particle asymptotic channel
  -> analytic continuation to a physical pole
  -> residue/fusion quotient
  -> one neutral particle fiber.
```

It is closer to N4r's prepared-sector semantics than to an external potential:
only the channel response that returns through the bound pole is retained. An
explicit equality with N4r's Schur kernel would require a Hamiltonian realization
and remains outside the S-matrix contract.

## 5. The first breather is a sharp stable particle in the bootstrap spectrum

For `0<xi<1`,

```text
0<m_1<2M_s.
```

The first inequality uses positivity of the sine on `(0,pi/2)`; the second uses
that it is strictly less than one there. Therefore `B_1` lies below its
soliton--antisoliton constituent threshold.

Every higher allowed breather has `n xi<1`, so its sine argument remains in
`(0,pi/2)` and

```text
m_n>m_1  for n>1.
```

A neutral decay into topologically charged particles needs at least one soliton
and one antisoliton, with threshold `2M_s`. A neutral multiparticle breather state
has threshold at least `2m_1`. Hence the distance from `m_1` to the first
kinematically allowed neutral continuum is

```text
delta_stab=min(2M_s,2m_1)-m_1>0.
```

Energy, momentum, and topological charge conservation therefore leave no decay
channel for `B_1` within the SG-01 spectrum. Its pole stays on the real mass shell
and supplies a sharp stable particle species. This is a spectrum-relative proof:
an omitted lighter neutral species would falsify it.

## 6. A local field and scattering fusion select the same particle

Let `Sigma_1` be the positive shell of mass `m_1`. N4s constructs the field
particle map

```text
T_(Sigma_1)(A)=E(Sigma_1)A Omega.
```

SG-03 supplies local exponential fields and their form factors. Smear an odd
combination `A_a` with a compact test function and choose its parameter so that
the one-breather form factor is nonzero:

```text
F_a^(1)(theta)
 =<B_1(theta),A_a Omega> !=0.
```

Consequently

```text
T_(Sigma_1)(A_a)!=0.
```

The residue construction in Section 4 gives a second nonzero intertwiner into
the same mass-`m_1`, neutral, scalar particle fiber. The connected massive little
group in `1+1` dimensions is trivial, and SG-01 supplies one `B_1` species, so
the selected sector has multiplicity one. Normalize both constructions as maps
from the rapidity wave-packet space onto that sector. Composing one inverse with
the other gives an endomorphism commuting with the irreducible Poincare action;
it is a scalar. Fix the phase of `Gamma_1` by the form-factor residue. The two
maps then select the same normalized one-particle state.

This constructs the N4s coincidence in the bootstrap model:

```text
local field A_a Omega -- shell projection --> B_1 wave packet
                                               ^
soliton--antisoliton channel -- pole residue --|
```

The equality is not inferred from calling both outputs “a breather.” It is earned
by their common shell, quantum numbers, multiplicity-one target, and normalized
intertwining maps.

## 7. N4v propagates the computed pole over the whole shell

Once `m_1` has been constructed and stability has supplied a sharp orbit, N4v
applies without another dynamical solve:

```text
E_1(P)=sqrt(m_1^2+P^2),
M_curvature=m_1.
```

At `xi=1/2`, this becomes

```text
E_1(P)=sqrt(2M_s^2+P^2),
partial_P^2 E_1(0)=1/(sqrt(2)M_s).
```

The whole route has only three semantic transformations:

```text
physical-strip pole
  -> invariant rest mass
  -> stable field-accessible shell
  -> exact momentum dependence.
```

Integrability performs genuine compression here: infinitely many graph and
multi-particle consistency conditions are encoded by factorization, crossing,
unitarity, and the bootstrap. This does not make integrability a universal
method. Constructing or proving the exact S-matrix is the model-specific hard
step that replaces the generic spectral inverse.

## 8. The weak-binding limit recovers relative mechanics

Put `u=u_1` and define the imaginary relative-momentum scale at the pole by

```text
kappa=M_s sin(u/2).
```

The exact binding below the two-soliton threshold is

```text
Delta_bind
 =2M_s[1-cos(u/2)]
 =2 kappa^2/[M_s(1+cos(u/2))].
```

Both expressions evaluate the same pole; the second follows by multiplying
`1-cos(u/2)` by `(1+cos(u/2))/(1+cos(u/2))`. As `u` tends to zero,
`cos(u/2)` tends to one, so

```text
Delta_bind/(kappa^2/M_s)
 =2/[1+cos(u/2)] ->1.
```

The reduced mass of two equal solitons is `M_s/2`, and their nonrelativistic
binding scale is `kappa^2/(2(M_s/2))=kappa^2/M_s`. The exact pole construction
therefore recovers the mechanical shallow-bound-state relation without solving a
relative-coordinate equation. Away from weak binding, the exact trigonometric
relation replaces that approximation.

## 9. Computability verdict and locality boundary

The [finite regression](../computation/04w-sine-gordon-breather/README.md)
evaluates the pole-to-mass identity for several couplings, checks the first-
breather stability gap, verifies the `xi=1/2` benchmark and shell curvature, and
tests the weak-binding recovery ratio.

Supported within the factorized-scattering/form-factor model:

- sine-Gordon/massive-Thirring is the smallest current worktable candidate that
  closes rest pole, constituent channel, local-field access, and Poincare shell;
- the exact mass ratio is constructed directly from the physical-strip pole;
- the pole residue constructs a translation-compatible fusion map;
- `B_1` is separated from every allowed neutral continuum and is stable;
- a nonzero local form factor and the fusion residue reach the same
  multiplicity-one particle sector;
- N4v turns the one rest mass into the full dispersion and curvature;
- the shallow-pole limit recovers ordinary two-body binding with an exact
  coincidence witness.

Not supported as a full constructive local QFT theorem:

- derivation of the exact factorized S-matrix from the renormalized action alone;
- strong locality, self-adjointness, and nontrivial double-cone algebras for the
  bound-state wedge-field construction in the full sine-Gordon model;
- a literal equality between the S-matrix pole kernel and N4r's Hamiltonian Schur
  complement;
- transfer of integrability or the mass formula to `3+1`-dimensional QED;
- an absolute mass without fixing one physical scale such as `M_s`.

The next useful branch is now sharply split. A **foundational branch** constructs
the local-net/spectral projector behind the bootstrap breather. The first
**robustness branch** is now [N4x](04x-nonintegrable-composite-robustness.md): it
carries the pole/fusion/access contract—not the sine-Gordon mass formula—into a
specific nonintegrable second-harmonic deformation, constructs the first mass
tangent and a threshold-gap certificate, and uses a half-frequency deformation
to falsify the old constituent channel. A later fidelity branch can transfer the
surviving contract to a relativistic Bethe--Salpeter or lattice calculation.

## Edges

- `N4r -> N4w`: pass the prepared-sector meaning and the demand that a reduced
  pole retain a recovery map to the full field state.
- `N4s -> N4w`: pass the field-created shell quotient, local-access test,
  asymptotic particle criterion, and distinction between a real pole and a
  resonance.
- `N4v -> N4w`: pass the rest-pole-to-shell propagation and curvature identity.
- `SG-01/SG-02 -> N4w`: pass the exact soliton S-matrix pole spectrum and the
  massive-Thirring neutral-composite interpretation.
- `SG-03 -> N4w`: pass nonzero local exponential-field form factors.
- `SG-04/SG-05 -> N4w`: pass the optional ultraviolet mass-scale map and the
  rigorous locality/domain boundary.
- `C4w -> N4w`: pass the finite pole, stability, curvature, and weak-binding
  regression.
- `N4w -> local integrable-QFT completion`: pass the exact shell, fusion residue,
  form-factor access map, and the missing strong-locality obligations.
- `N4w -> N4x`: pass the portable pole/fusion/access/stability contract while
  leaving the sine-Gordon mass formula behind.
- `N4w -> N7/manuscript synthesis`: pass the first evaluated relativistic
  field/mechanics/particle model and its exact computability boundary.
- `N4w -> N9b`: pass stable asymptotic particles and local form factors as a
  physical spectral-sum route to a coupling-visible measure.

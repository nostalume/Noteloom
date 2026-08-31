# Audit — Does the Representation Spine Reach Computable Observables?

Status: supported audit of the current worktable; free causal propagation and a nonrelativistic algebraic Coulomb-spectrum witness are reached; the relativistic Coulomb half-line path is exact block equivalence but failed computational reduction; N4r constructs the field/mechanics projected resolvent, N4s constructs the general spectral field/particle relation, N4t verifies their same-state architecture, N4u reduces the first weak-coupling effective-mass correction to an atomic-resolvent integral while rejecting a generic exact self-energy cost advantage, N4v proves that one sharp stable massive Poincare orbit compresses all momentum dependence to one dynamically computed rest mass, N4w evaluates that diagram for a sine-Gordon neutral breather, and N4x proves which particle structures survive a controlled nonintegrable deformation while isolating the numerical form-factor/remainder frontier  
Inputs: N1--N4x, especially [N4d computation interface](../nodes/04d-computation-interface.md), [N4m integer-spin field machine](../nodes/04m-finite-integer-spin-field-machine.md), [N4i half-integer response](../nodes/04i-half-integer-green-construction.md), [N4l half-integer faithfulness](../nodes/04l-half-integer-support-faithfulness.md), [N4n adaptive observable-reduction audit](../nodes/04n-algebraic-spectrum-bridge.md), [N4o Dirac--Coulomb local graph](../nodes/04o-dirac-coulomb-local-graph.md), [N4p angular block obstruction](../nodes/04p-dirac-angular-reduction.md), [N4q semantic computability](../nodes/04q-semantic-computability.md), [N4r field/mechanics stability](../nodes/04r-field-mechanics-stability.md), [N4s field/particle extraction](../nodes/04s-field-particle-extraction.md), [N4t neutral-composite same-state test](../nodes/04t-neutral-composite-same-state.md), [N4u effective-mass route audit](../nodes/04u-effective-mass-route-audit.md), [N4v relativistic mass-shell closure](../nodes/04v-relativistic-mass-shell.md), [N4w sine-Gordon breather test](../nodes/04w-sine-gordon-breather-rest-pole.md), [N4x nonintegrable robustness](../nodes/04x-nonintegrable-composite-robustness.md), and [endpoint source contracts](../sources/computability-endpoint-contracts.md)

## Audit question and verdict

The goal is not merely to classify representations or write covariant equations.
It is to reduce the semantic and computational path to observables such as a
propagator or a bound-state spectrum.

The current verdict is mixed but precise:

```text
representation classification                 supported
  -> local free field complex                 supported
  -> admissible source and gauge quotient     supported
  -> retarded/advanced free response          supported
  -> faithful positive one-particle image     supported at each finite spin
  -> state-selected free propagator           structurally reduced, prescription open
  -> observable-reduction audit               five mechanisms; no universal reducer
  -> relativistic Coulomb operator graph      carrier/domain/observable typed
  -> intrinsic angular decomposition          exact blocks; residual gamma problem unchanged
  -> semantic-computability synthesis         observable compression distinguished from reformulation
  -> field/mechanics projection               exact response and state recovery under declared hypotheses
  -> observable-stable variation              contour projector bound; self-energy not yet evaluated
  -> field/particle extraction                spectral quotient/covariance; asymptotic theorem contracted
  -> neutral composite same-state test        spectral/preparation/asymptotic identity supported
  -> effective-mass route audit               exact routes equal; leading atomic-resolvent reduction supported
  -> relativistic bound-state spectrum        eigenvalues and projectors not yet computed
  -> interacting graph observable             not yet constructed.
```

Thus the spine has a strong **front-end reduction** and one algebraic backend
prototype, not a complete observable engine. It removes redundant carrier and
gauge work before the analytic computation and shows when a Casimir can eliminate
the residual spectral equation. It cannot replace the background, domain, state,
coupling, asymptotic comparison, or field kernel that define other observables.

## 1. What the path has genuinely reduced

| Capability | Current result | Computational reduction | Remaining cost |
| --- | --- | --- | --- |
| physical degrees of freedom | little-group fiber equals field cohomology | no polarization enumeration | orbit integration only |
| free equation | uniform invariant symbols for every finite label | no rank-by-rank component derivation | finite trace/gamma algebra |
| causal propagator | one scalar wave Green map generates every finite symmetric massless-potential response | no tensor propagator inversion | scalar distribution and support |
| positive states | screen metric and support faithfulness | no indefinite-carrier diagonalization | density in full induced space |
| background spectrum | open reduction graph plus exact Schur complement | N4o constructs the relativistic carrier, connection and domain target; N4p exposes the half-line `Cl_2(C)` residue; N4r constructs a pre-radial projected-resolvent and projector-variation relation | evaluated self-energy/kernel bound, spectrum and projector kernels |
| dynamical response | prepared field projection and action/graph contracts | N4r localizes recoil, radiative, pair, and photon sectors in one recoverable energy-dependent self-energy | field Hamiltonian realization, regulator, renormalization, kernel evaluation, error and cost control |
| particle content | field-created translation-shell quotient plus asymptotic contracts | N4s removes interpolator redundancy; N4t identifies one dressed neutral composite simultaneously by prepared spectral weight, full band projection, and zero-photon asymptotic channel; N4u reduces its leading curvature correction to an atomic resolvent integral; N4v proves that a sharp single Poincare orbit identifies rest and curvature mass and fixes the full dispersion; N4w computes an exact neutral-breather mass ratio and joins pole fusion to local-field access; N4x breaks integrability, reduces the first mass tangent to crossed diagonal form factors, certifies stability from explicit remainder bounds, and shows by confinement when the constituent basis must be replaced | numerical N4x tangent/remainder bounds, complete local-net realization, nonintegrable `3+1` composite mass/weight, charged particle weights, cutoff removal, and realistic completeness |

This is useful reduction: tensor or spinor rank no longer enlarges the analytic
denominator of the free response. But reduction of free kinematics is not yet
reduction of a background spectral or interacting problem.

## 2. A single scalar distribution generates the free physical propagators

Let `g_b` be a scalar distribution with a declared boundary prescription `b` and

```text
q g_b=1.
```

Retarded and advanced choices are already constructed. A Feynman choice is
conditional on separately selecting and validating its boundary value/state.

### 2.1 Integer spin

For an admissible source `J`, N4f constructs

```text
K=M_s^(-1)J,
C_sK=0,
E_s=M_sD_s,
D_s=qI-R_sC_s.
```

Define the boundary-selected response

```text
Phi_b[J]=g_b K.
```

All constant-coefficient operators commute with `g_b`. Evaluate the same field:

```text
C_sPhi_b[J]=g_b C_sK=0,

D_sPhi_b[J]
 =(qI-R_sC_s)g_bK
 =K,

E_sPhi_b[J]=M_sK=J.
```

Therefore every scalar wave fundamental distribution lifts to the physical
admissible-source response for every separate finite symmetric massless
integer-spin potential.

### 2.2 Half-integer spin

For the half-integer source use N4i's data

```text
K=M_n^(-1)J,
B_nK=0,
E_n=M_nS_n,
S_n^2+2R_nB_n=qI.
```

The first-order response is

```text
Psi_b[J]=S_ng_bK.
```

The Bianchi and wave identities compute

```text
B_nPsi_b[J]=B_nS_ng_bK=0,

E_nPsi_b[J]
 =M_nS_n^2g_bK
 =M_n(qI-2R_nB_n)g_bK
 =M_nK
 =J.
```

The only fermionic numerator is the already meaningful field operator `S_n`.
No gamma-matrix inverse or rank-dependent polarization sum appears.

### 2.3 Exact boundary of this result

This is an admissible-source propagator, which is the object entering physical
source pairings. It is not a full inverse on the redundant carrier. A gauge-fixed
off-shell kernel may contain additional gauge terms, and an interacting Feynman
propagator requires a state and renormalized action.

Computationally, however, the free massless symmetric-potential families have
reached the desired form:

```text
construct one scalar distribution
  -> apply one finite algebraic trace reversal
  -> optionally apply one first-order fermionic symbol.
```

The transformation depth is independent of spin.

## 3. The relativistic operator now exists, but its spectrum is not yet an output

The present arbitrary-spin massive construction uses a minimal chiral carrier with
a Klein--Gordon equation. It realizes the correct massive representation, but it
is not the parity-paired first-order Dirac electron used in a Coulomb background.
Representation equivalence does not preserve off-shell coupling or spectral
domains automatically.

A hydrogenic calculation therefore needed new physical inputs. N4o now separates
and constructs them as follows:

```text
prior Weyl/Clifford carrier plus parity-paired first-order choice
  -> massive Dirac carrier and positive time-selected Hilbert space
  -> chosen U(1) coupling and static source approximation
  -> distinguished self-adjoint Hamiltonian H_nu
  -> manifest SU(2) multiplicity reduction                 supported
  -> intrinsic kappa blocks                                 exact equivalence only
  -> residual Clifford computation                          not reduced
  -> channel spectral computation                           open
  -> discrete gap spectrum and projectors                   open.
```

The decisive relation to the old spine is also computed. The free massive Dirac
operator factorizes to N4's scalar massive symbol, but after `U(1)` deformation
its square contains the spin--curvature term
`-(i e/4)[gamma^mu,gamma^nu]F_(mu nu)`. Thus the scalar Green compiler cannot be
reused unchanged in a Coulomb field.

The Dirac Hamiltonian is neither a bounded operator nor bounded above or below.
“Bound-state spectrum” means its discrete eigenvalues in the mass gap `(-m,m)`.
The self-adjoint realization is semantic data: different Coulomb extensions can
have different spectra, so solving the formal differential equation first is not
enough.

## 4. No universal reducer survives the cross-example audit

The earlier radial-first proposal was too orthodox. Replacing it by “compute the
generating algebra first,” even inside a fixed budget, still privileged one search
language. The corrected audit is owned by
[N4n](../nodes/04n-algebraic-spectrum-bridge.md):

```text
named observable and tolerance
  -> open, problem-local graph of invented transformations
  -> equality/error witness and observable-recovery map
  -> whole-route cost and failure boundary
  -> retain it or compute the residual directly.
```

This is not a framework that discovers the transformations. It is a common
language for verifying and composing them. No closed list of examples can become
a universal selector; on broad local many-body Hamiltonian classes, even deciding
whether a spectral gap exists is undecidable. The current Dirac--Coulomb target is
much narrower, so this is a boundary on the claim—not an excuse to avoid its
computation.

For the nonrelativistic Coulomb Hamiltonian, angular momentum and the Runge--Lenz
operator close as compact `so(4)` on negative-energy sectors. Their Casimir identity
and finite-dimensional unitary labels compute

```text
E_n=-mu kappa^2/(2 hbar^2 n^2)
```

without a radial wavefunction. On positive-energy sectors, the same commutator
changes sign and closes as noncompact `so(3,1)`. Continuous representation labels
do not quantize the energy; scattering additionally requires a reference dynamics,
incoming/outgoing asymptotic maps, and flux normalization. In the exceptional
Coulomb case the `S` matrix can also be reduced algebraically to an intertwiner,
but the long-range asymptotic prescription remains physical input.

For a generic central potential the bounded vector probe need not find a hidden
closure. This rejects only its declared ansatz. Manifest rotations still remove
angular degeneracy but leave a multiplicity operator; a radial channel is one
possible execution of that residue. It is not the conceptual origin of the
spectrum and need not be the residual representation in many-body or field
problems.

The oscillator instead constructs ladder operators from a quadratic/symplectic
normal form. The inverse-square model has an easy conformal closure but still needs
self-adjoint extension data. The quartic oscillator yields a rigorous Gaussian
variational upper bound without hidden algebra. Integrable many-body models may use
a Lax or transfer object whose construction is itself model-specific. These are
counterexamples to a fixed algebra specification, not additional mandatory stages.

One resolvent still unifies the spectral outputs: isolated poles/projectors are
bound states, while continuous boundary discontinuities give spectral densities.
The scattering matrix is more relational because it compares this continuum with
a separately constructed asymptotic reference.

## 5. Audit against the research philosophy

| Criterion | Free propagator path | Bound-state path | Verdict |
| --- | --- | --- | --- |
| internal construction | field/gauge operators and source maps are constructed | Dirac carrier, external connection, positive static Hilbert space and domain target constructed | supported through operator typing |
| semantic computation | every free response identity has a same-input witness | free factorization, `U(1)` covariance, curvature obstruction, angular recovery, projected field response, full-state recovery, and contour stability are explicit; no relativistic energy is produced | structural bridge supported, predictive evaluation partial |
| reduced transformation depth | one scalar Green map plus finite algebra | the polar transform relocates the gamma subblock; N4r avoids it for prepared projectors but has not yet shown that evaluating the self-energy is cheaper | exact relation supported, computational gain unproved |
| component economy | components occur only in bounded regression checks | matrix entries are suppressed, but the abstract involutions generate `M_2(C)` and therefore retain the same component content | notation improved, computation not reduced |
| predictive output | causal propagation and positive one-particle image | nonrelativistic Coulomb energies computed; relativistic energies/projectors absent | incomplete |
| generality | every separate finite symmetric massless integer- and half-integer-spin potential | no common reducer; the witness/recovery/cost contract is portable but every useful edge remains problem-specific | honest but locally incomplete |

The path is therefore not a failed formalism. It has successfully compiled
symmetry data into minimal free physical operators. But the original goal of
prediction is reached only after an **observable backend** is added.

## 6. Exact follow-on research nodes

These are semantic nodes, not engineering stages or permission gates:

1. **Boundary-selected free response.** Choose the scalar Feynman distribution,
   state its wavefront/test-function domain, apply the formulas in Section 2, and
   verify the physical residue and source-pairing independence.
2. **Adaptive observable-reduction audit.** N4n now contrasts quadratic normal form,
   finite Runge--Lenz search, conformal/domain analysis, variational bounds and
   Lax constructions; retains the common resolvent and exact sector Schur
   complement; and rejects both a universal solver and a closed method selector.
   Its output is only an open-graph edge contract for witness, recovery, cost,
   error and composition.
3. **Massive Dirac background system.** N4o constructs why the parity-paired
   first-order carrier and `U(1)` coupling are additional to the massive chiral
   Klein--Gordon realization, declares the Hilbert space and distinguished-domain
   contract, computes the curvature obstruction, and performs the manifest
   rotation reduction. N4p then constructs the conventional invariant split from
   the old rotation Casimirs and Clifford normal, but its `Cl_2(C)~=M_2(C)` audit
   shows that this is the old radial gamma calculation up to basis change.
4. **Field/mechanics projection and stable variation.** N4r constructs the exact
   relation: preparation pulls the full field resolvent back to a common
   mechanical space; Gauss' law constructs its electrostatic part; Feshbach
   elimination supplies the energy-dependent field self-energy and full-state
   recovery; a contour estimate bounds prepared projector variation. The next
   computation must evaluate that bound in one UV-controlled heavy-source model
   and compare its cost with direct recomputation.
5. **Field/particle extraction.** N4s reverses N3: project field-created states
   onto a sharp translation-spectrum component, quotient zero shell overlap, and
   complete. The resulting Poincare representation is the particle. Stable
   composite shells enter the same construction; Haag--Ruelle limits add the
   scattering interpretation. N4r's rest pole must first become a covariant
   total-momentum branch. Resonances and infraparticles have different output
   types rather than defective Wigner spaces.
6. **Neutral composite same-state test.** N4t constructs total-momentum fibers
   for one atom--radiation model and proves that the prepared spectral atom, full
   dressed-band projector, and zero-photon Rayleigh channel select the same
   vector. At a massless threshold, it replaces N4r's unjustified pointwise
   Schur inverse by spectral-projection recovery. It also records why this is not
   yet a relativistic particle: the model has neither boosts nor a local
   vacuum-to-atom interpolator.
7. **Effective-mass route audit.** N4u differentiates that same dressed branch.
   The direct route needs one full reduced-resolvent response; exact Feshbach
   differentiation needs a scalar root and reusable complementary tangent
   solves. Their equality is proved by exact isospectrality and checked by a
   finite regression. Self-energy notation alone gives no generic cost gain, but
   the order-`g^2` scalar-model correction contracts to one positive atomic-
   resolvent momentum integral and predicts mass enhancement.
8. **Relativistic mass-shell closure.** N4v starts from an interacting sharp
   spectral component rather than a free dispersion. Covariance transports the
   same rest state over one massive orbit; the shell invariant then constructs
   `E(P)=sqrt(M_b^2+|P|^2)` and proves orbit, rest, and curvature masses equal.
   Rationalization recovers the nonrelativistic kinetic energy with an exact
   quartic error bound. This removes repeated momentum-fiber solves after `M_b`
   is known, but it neither proves the shell exists nor computes `M_b`.
9. **Evaluated relativistic composite.** N4w selects the sine-Gordon first
   breather / massive-Thirring neutral bound state after rejecting QED hydrogen
   and ladder Bethe--Salpeter truncation as the first exact regression. Analytic
   continuation of the two-soliton invariant to the physical-strip pole computes
   `m_1/M_s=2 sin(pi xi/2)`; the residue supplies fusion, a local form factor
   supplies field access, a positive threshold gap supplies stability, and N4v
   supplies the shell. The exact result belongs to the integrable bootstrap
   model; strong locality and transfer beyond integrability remain open.
10. **Nonintegrable robustness and falsifier.** N4x deforms that same model by
   `cos(2 beta phi)` at `xi=1/5`. Vacuum and semilocality computations preserve
   the old soliton channel while generic factorization is lost. Two crossed
   diagonal form factors give the first mass tangents; uniform mass/remainder
   bounds give an explicit positive threshold-gap radius; N4v retains the exact
   shell shape. The paired `cos(beta phi/2)` deformation has a nonzero
   annihilation residue and confines the old soliton, proving that a new meson
   basis—not more terms in the old pole expansion—is required. Numerical form
   factors and continuum bounds remain open.
11. **Dynamical graph response.** Construct action, state, regulator,
   renormalization conditions, and graph reductions before evaluating scattering
   or vacuum polarization.

The pre-radial semantic relation now exists in N4r, while N4p's half-line operator
remains an exact fallback and regression target. The frontier has moved from
“find a relation” to “realize and evaluate it”: construct one admissible field
Hamiltonian and heavy-source preparation, bound the source and self-energy
variation on an isolated contour, and decide whether the prepared projector is
cheaper to certify than to recompute. Below eliminated-sector thresholds this is
a closed mechanical bound query. When a threshold opens, ordinary inverses and
self-adjoint projectors give way to continuum boundary values, widths, and
scattering observables; that change is a physical boundary, not a coordinate
effect. N4s adds the final semantic distinction: even a computed bound pole is not
yet a particle until field-created states project nontrivially onto a stable
covariant shell and the required asymptotic limit exists. N4t validates the
same-state architecture below that boundary. N4u completes its first
cost-sensitive test: exact elimination generally relocates the inverse, whereas
the controlled weak-coupling sector reduction genuinely shortens the route. A
physical nonrelativistic number now requires a specified atomic potential, form
factor, cutoffs, and an error-controlled evaluation of the resulting spectral
integral. N4v adds a different compression: after dynamics constructs one sharp
stable relativistic rest pole, Poincare covariance fixes its entire dispersion
and identifies its curvature mass without new fiber solves. The next unresolved
cost is therefore concentrated where it belongs—computing, renormalizing, and
proving stability of that rest pole in one interacting relativistic model.
N4w now supplies that number and stability check in one deliberately restricted
integrable model: after fixing the physical soliton scale, the first-breather
mass ratio, binding, fusion channel, and shell are exact. This is the first place
where the relativistic field/mechanics/particle route reaches an evaluated bound
composite. The remaining gap is no longer hidden numerical algebra; it is whether
the bootstrap/form-factor objects arise from a complete local net and which
compression survives when factorization and `1+1`-dimensional integrability are
removed. N4x answers the structural half of that question. A local second
harmonic preserves the constituent sector; the first nonintegrable mass tangent
uses one crossed scalar form factor per species; a certified error budget keeps
the pole below threshold; and Poincare symmetry still fixes all momentum
dependence. Elastic factorization, the exact trigonometric mass formula, and
two-body determination of multiparticle scattering do not survive. The
half-frequency counterexample also shows that preserving Poincare and charge
conjugation is insufficient: semilocality can confine the old constituents and
force a new meson computation. The next frontier is quantitative rather than
verbal—evaluate the two second-harmonic form factors and finite-volume remainder
bounds at `xi=1/5`.

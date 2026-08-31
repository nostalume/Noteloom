# N4s — Field-to-Particle Extraction Beyond Free Realization

Status: spectral quotient and covariance supported internally; stable-particle,
asymptotic-scattering, and infraparticle steps bounded by explicit theorem
contracts; N4t now tests one interacting neutral composite band but not its
relativistic vacuum-sector particle quotient; N4v constructs the conditional
mass-shell closure once that quotient is a sharp single massive orbit; N4w
evaluates the pole/fusion/form-factor diagram in an integrable bootstrap model  
Consumes: [N3 free field realization](03-realization-bridge.md), [N4g bosonic
positive shell](04g-positive-frequency-completion.md), [N4k fermionic positive
shell](04k-half-integer-positive-frequency.md), [N4r field/mechanics
projection](04r-field-mechanics-stability.md), and [field/particle source
contracts](../sources/field-particle-extraction-contracts.md)  
Produces: a field-to-particle spectral quotient, its relation to N3's reverse
particle-to-field construction, a common treatment of elementary and composite
stable particles, and explicit resonance/infraparticle boundaries

## Node contract

- **Question/capability:** given a local field dynamics, what operation constructs
  its particle content, and when does that content agree with the Wigner
  representations from N2/N3?
- **Presumptions:** a physical Hilbert space, translation spectrum, vacuum, and
  admissible interpolating operators have been constructed. Locality, positivity,
  charge-sector access, and asymptotic regularity are stated separately rather
  than inferred from a formal field equation.
- **Output:** an invariant particle quotient from field excitations; exact
  covariance; the condition for Haag--Ruelle scattering; the lift of an N4r
  mechanical bound pole to a relativistic composite particle; and distinct output
  types for stable particles, resonances, and infraparticles.
- **Boundary:** the construction does not find spectral shells automatically,
  prove asymptotic completeness, or make correlator/pole computation cheap.

## 1. Why N3 is only one direction of the relation

N3 begins with a Wigner particle representation and asks whether a covariant
field carrier or field complex realizes it:

```text
particle fiber V_sigma
  -> field subspace or cohomology over a chosen orbit.
```

That direction is adequate for free equations because the orbit and particle
label are already known. In an interacting field theory they are outputs, not
inputs. A local field symbol may overlap several masses, a composite operator may
create a stable particle, and a charged excitation may have no sharp Wigner mass.
The reverse question must therefore start from the field theory's actual
translation spectrum:

```text
field dynamics and vacuum
  -> spectral particle candidates
  -> stability/asymptotic test
  -> Wigner particle, resonance, or generalized particle weight.
```

These directions are not automatically inverse. They coincide only after the
field-generated particle quotient is complete in the chosen shell and its
Poincare representation matches N3's constructed orbit representation.

## 2. Translations construct the spectral question

Let a field theory provide:

```text
H             physical Hilbert space,
Omega         invariant vacuum,
U(a,Lambda)   positive-energy Poincare action,
E(Delta)      joint spectral measure of the translation generators,
C             admissible interpolating operators.
```

`C` is not automatically the observable algebra. Neutral excitations may be
created by bounded local observables. Charged sectors require a field algebra or
appropriately localized intertwiners connecting the vacuum sector to the charged
sector. This access choice is part of the particle claim.

For `A in C`, the state `A Omega` carries the spectral measure

```text
mu_A(Delta)=||E(Delta)A Omega||^2.
```

This equation is a computation: apply the projection `E(Delta)` to the same
field-created state and evaluate its Hilbert norm. It asks how much of that state
has energy-momentum in `Delta`; it does not interpret the carrier index of `A` as
a particle label.

Let `Sigma` be a Poincare-invariant sharp spectral component, for example a
positive mass hyperboloid. Construct

```text
T_Sigma:C -> E(Sigma)H,
T_Sigma(A)=E(Sigma)A Omega.
```

Different interpolating operators can create exactly the same particle state,
and many create no state on this shell. Remove only that irrelevant distinction:

```text
N_Sigma=ker T_Sigma,

<[A],[B]>_Sigma
 =<E(Sigma)A Omega,E(Sigma)B Omega>_H.
```

If `A` is changed by `K in N_Sigma`, then

```text
E(Sigma)(A+K)Omega
 =E(Sigma)A Omega+T_Sigma(K)
 =E(Sigma)A Omega,
```

so the form and the particle state are unchanged. Quotient and complete:

```text
P_Sigma=completion(C/N_Sigma).
```

`T_Sigma` extends to an isometry

```text
Tbar_Sigma:P_Sigma
  -> closure(E(Sigma)C Omega) subseteq E(Sigma)H.
```

This is the general field-to-particle compression. It retains only the response
of field operations on the named spectral component. Equality with the entire
shell space is the separate cyclicity/density statement

```text
closure(E(Sigma)C Omega)=E(Sigma)H.
```

## 3. Covariance turns the shell quotient into a particle representation

For `g=(a,Lambda)`, define the transformed interpolator

```text
g.A=U(g)A U(g)^(-1).
```

Vacuum invariance and covariance of the translation spectral measure give

```text
T_Sigma(g.A)
 =E(Sigma)U(g)A Omega
 =U(g)E(Lambda^(-1)Sigma)A Omega.
```

The chosen `Sigma` is Poincare invariant, so `Lambda^(-1)Sigma=Sigma`. Hence

```text
T_Sigma(g.A)=U(g)T_Sigma(A).
```

This computation proves that `N_Sigma` is invariant and that `P_Sigma` carries
the restriction of the physical Poincare action. Decompose that restriction into
irreducible orbit representations. N2/N2a then names their mass, spin, or
helicity; N3 determines which local carrier/cohomology realizes each fiber.

Particle labels are therefore extracted from `U` on the spectral quotient, not
from the tensor or spinor indices of the interpolating field.

## 4. Free-field source maps are the computable regression case

N4g and N4k start from classical causal source quotients and evaluate their
Fourier data on a known free shell. Their maps have the same quotient shape:

```text
source class
  -> positive-shell amplitude
  -> quotient by zero shell amplitude
  -> positive one-particle completion.
```

N4h and N4l prove faithfulness, so their source quotients already have no extra
spectral null classes. Their covariance calculation identifies the resulting
closed images with subrepresentations of N3's Wigner Hilbert spaces.

N4g and N4k alone stop at this structural regression. Downstream
[N4y](04y-quantization-recovery-bridge.md) now constructs the symmetric or
antisymmetric multiplicity space and evaluates the field generator on the vacuum.
For the bosonic branch it proves on the same source class that the resulting
one-particle vector is exactly N4g's shell amplitude and hence the free instance
of `T_Sigma`. For the fermionic branch the occupation-space recovery is exact,
but equality between N4i/N4j's local causal Euler form and N4k's positive CAR real
form remains open. Thus “second quantization” closes one free recovery loop; it
does not remove the interacting spectral extraction problem of this node.

## 5. Stability constructs scattering particles

A nonzero spectral quotient is not sufficient for a scattering interpretation.
Assume `Sigma_m` is a sharp massive shell, its states have nonzero interpolating
overlap, and FP-01 or FP-02's stability/regularity hypothesis holds. For a
wavepacket `f` supported on the shell, the Haag--Ruelle time smear `A_t(f)` is
constructed so that the off-shell spectrum oscillates away while the target
dispersion remains stationary. The theorem contract gives the strong limit

```text
lim_(t -> plus-or-minus infinity) A_t(f)Omega
 =E(Sigma_m)A(f)Omega
 =T_(Sigma_m)(A(f)).
```

The right side is exactly the particle state already constructed by the spectral
quotient. Thus the asymptotic theorem does not invent a second particle; it proves
that the spectral state can be isolated by late-time field operations.

For wavepackets with separated velocities, the theorem contract also constructs

```text
Omega^(in/out):Fock_stat(P_(Sigma_m)) -> H^(in/out) subseteq H
```

from limits of products of the same time-smeared operators. These maps are
isometric and Poincare-intertwining. Here `stat` is not decorative: FP-01's
displayed theorem supports the bosonic local case. Fermionic or more general
charged sectors require the corresponding graded/localized scattering theorem;
the spectral quotient itself did not choose statistics. When the incoming and
outgoing ranges coincide, the scattering operator is

```text
S=Omega^(out,dagger) Omega^in.
```

The Poincare representation on `H` does not determine `S`: two theories can have
the same particle representations but different actions of local fields and
therefore different incoming/outgoing embeddings.

## 6. Elementary and composite particles use the same extraction

Nothing in `T_Sigma(A)=E(Sigma)A Omega` asks whether `A` is called elementary.
Suppose a composite interpolator `B` is built from local fields and

```text
E(Sigma_b)B Omega !=0
```

for a stable sharp shell `Sigma_b`. Then the same quotient constructs its
one-particle Hilbert space. If the stability theorem applies, that bound composite
enters the asymptotic Fock space as one particle species. Conversely, an
“elementary” field with zero projection on every stable shell creates no
asymptotic particle of its own.

This removes an unnecessary ontology:

```text
one particle type may be created by many fields,
one field may overlap many particle types and continua,
composite and elementary interpolators may create the same particle state.
```

The invariant object is the stable spectral subrepresentation and its observable
couplings, not the polynomial appearance of the interpolator.

## 7. N4r is one momentum fiber of the composite-particle question

N4r constructs a prepared mechanical resolvent from a field Hamiltonian and
recovers its dressed state. A static external source, however, breaks total
translation invariance. Its gap eigenvalue is a mechanical bound level, not yet a
relativistic particle mass.

Restore a dynamical source and decompose the full field theory by conserved total
momentum, assuming the spectral theorem gives the required measurable fiber
decomposition in the stated model:

```text
H = direct-integral H(P) dmu(P),
mathbb H = direct-integral mathbb H(P) dmu(P).
```

In each fiber, N4r's construction can produce a prepared resolvent `G_P(z)`. If
an isolated or regular pole persists as a branch `E_b(P)` and the recovered
states are measurable and normalizable, it constructs

```text
Sigma_b={(E_b(P),P)}.
```

If the full dynamics is Poincare covariant and this branch is one massive orbit,
then evaluating the invariant on the same branch gives

```text
E_b(P)^2-|P|^2=M_b^2.
```

At `P=0`, the exact full-field branch satisfies `E_b(0)=M_b` when the vacuum
energy is normalized to zero. N4o/N4r's external Dirac eigenvalue
`epsilon_b(0)`, however, omits the dynamical source rest energy and some field
corrections. A controlled field/mechanics limit must compute

```text
M_b=E_ref+epsilon_b(0)+controlled correction,
```

with `E_ref` carrying the declared heavy-source and renormalization reference.
Thus a hydrogenic Dirac level is one contribution to the composite rest mass, not
the mass by notation. Let `P_b(P)` be the recovered exact fiber eigenprojection.
The shell projection and its prepared residue are

```text
E(Sigma_b)=direct-integral P_b(P) dmu(P),
Pi_b^M(P)=J_P^dagger P_b(P)J_P,
```

while N4r's recovery map reconstructs the eliminated field dressing in each
momentum fiber. Therefore

```text
mechanical bound pole
  + dynamical source
  + covariant momentum branch
  + stability/asymptotic limit
  -> composite particle.
```

Every arrow is necessary. A Coulomb energy formula alone does not construct the
particle representation.

## 8. Failure of a sharp shell changes the output type

The field-to-particle relation has several regimes:

| Spectral/asymptotic situation | Constructed output | What is not justified |
| --- | --- | --- |
| isolated sharp shell | Wigner one-particle quotient; ordinary Haag--Ruelle scattering | asymptotic completeness |
| sharp shell embedded near massless continuum plus regularity | stable Wigner particle and scattering states | regularity from symmetry alone |
| stable composite shell | bound object as another particle species | elementary/composite ontology |
| no real shell, only a continued complex pole | resonance energy/width candidate | normalizable one-particle Hilbert subspace |
| Gauss-law charged infrared sector | particle weight and inclusive asymptotic content | sharp-mass Lorentz-covariant Wigner state or ordinary `S` matrix |
| no asymptotic spectral/detector contribution | no particle of that field excitation | identifying field carrier with a confined particle |

For the infraparticle row, FP-03 constructs temporal detector limits `sigma` on a
localizing operator ideal `L`. The same semantic pattern reappears:

```text
<L_1,L_2>_sigma=sigma(L_1^*L_2)
  -> quotient zero norm
  -> complete
  -> decompose into improper sharp-momentum components.
```

The output is not a normalizable sharp-mass shell, so N3's ordinary Wigner-space
bridge cannot be imposed. This is a reconstruction of the particle concept forced
by the long-range field, not a component correction to a free electron equation.

## 9. Computability and the supported frontier

The construction reduces the prediction target from “solve the field history” to
specific spectral or asymptotic data:

- `mu_A(Delta)` for particle spectral weight;
- `E(Sigma)A Omega` for the stable one-particle amplitude;
- pole location and residue for a bound branch;
- `Omega^(in/out)` or LSZ on-shell limits for scattering;
- detector weights/inclusive measures when a Wigner particle fails.

This is semantic compression only when those objects can be computed or bounded
without reconstructing the entire field state. A compact spectral formula or LSZ
notation may still hide a hard correlator, analytic continuation, renormalization,
or large-time limit.

Supported:

- the field-created spectral quotient, its null identification, completion, and
  Poincare covariance are computed internally;
- N3 and N4s are identified as opposite, conditionally inverse directions;
- elementary and composite stable particles are unified by the same spectral
  operation;
- N4r's mechanical pole is placed correctly as one momentum-fiber input, not
  prematurely called a particle;
- scattering and infraparticle constructions have explicit theorem contracts.

Open:

- density of the finite-rank fermionic compact-source image in the full induced
  space; N4z closes the local causal-Euler/CAR equality, and N4y closes the free
  bosonic source/field/shell bridge;
- graded/localized scattering contracts for fermionic and non-observable charged
  sectors;
- one interacting model in which `mu_A`, a stable shell, and its interpolating
  quotient are reconstructed from a complete local net rather than assumed
  through factorized-scattering/form-factor contracts;
- the covariant heavy-source lift of N4r's atomic pole;
- resonance analytic continuation and a certified pole/width computation;
- charged-sector particle weights for the intended relativistic QED model;
- countable particle inventory, superselection reconstruction, and asymptotic
  completeness.

That smallest model test is now [N4t](04t-neutral-composite-same-state.md). In a
translation-invariant atom--radiation model it proves that prepared mechanical
spectral weight, the decomposable dressed-atom spectral projection, and the
zero-photon Rayleigh channel select the same vector. The test also finds two
honest gaps: the model has no Lorentz boosts, and its fixed one-atom sector has no
local vacuum-to-atom interpolator. It therefore validates the same-state
architecture without pretending to compute `E(Sigma_b)B Omega` in relativistic
QED.

## Edges

- `N3 -> N4s`: pass the orbitwise particle-to-field intertwiner and its density
  boundary for comparison with the reverse spectral quotient.
- `N4g/N4h/N4k/N4l -> N4s`: pass the faithful free positive-shell source maps as
  regression cases and their still-open quantization/density boundaries.
- `N4r -> N4s`: pass the prepared pole, projected residue, full-state recovery,
  and the missing total-momentum/covariance obligations.
- `FP-01/FP-02 -> N4s`: pass stable-shell asymptotic convergence and Moller-map
  theorem contracts.
- `FP-03/FP-04 -> N4s`: pass the infraparticle alternative and completeness
  boundary.
- `N4s -> field/mechanics/particle computation`: pass the same-state coincidence
  diagram among fiber pole recovery, full spectral projection, and asymptotic
  particle extraction.
- `N4s -> N4t`: specialize the diagram to one neutral translation-invariant
  atom--radiation model and return the exact relativistic boundary.
- `N4s -> N4v`: pass the sharp field-created spectral quotient, its Poincare
  covariance, access and stability requirements, and the resonance/infraparticle
  alternatives.
- `N4s -> N9`: pass the invariant sharp shell and asymptotic intertwiner as the
  exact particle/scattering descent cases.
- `N4s -> N9a`: pass the sharp-atom/continuum distinction and scattering boundary
  so both regimes can be evaluated from one coupling measure.
- `N4s -> N4w`: pass the nonzero local-field shell projection, real-pole
  stability, and same-particle coincidence obligations for an evaluated model.
- `N4s -> N4y`: pass the interacting spectral quotient and asymptotic Moller-map
  contracts; N4y compares their extraction order with the exact free
  quantization/recovery loop.
- `N4s -> N7/manuscript synthesis`: pass the distinction among field carrier,
  stable particle quotient, scattering species, resonance, and particle weight.

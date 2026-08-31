# N4r — Field/Mechanics Projection and Observable-Stable Variation

Status: exact projected-resolvent, reconstruction, Gauss-law, and bounded-variation
identities supported under the declared operator hypotheses; the renormalized QED
realization and controlled heavy-source limit remain open  
Consumes: [N4o Dirac--Coulomb local graph](04o-dirac-coulomb-local-graph.md),
[N4q semantic computability](04q-semantic-computability.md), and
[field/mechanics variation source contracts](../sources/field-mechanics-variation-contracts.md)  
Produces: a common mechanical observable extracted from a field dynamics, an exact
field-state recovery map, a physically generated family of electrostatic
representatives, and a contour criterion for observable stability

## Node contract

- **Question/capability:** when is a mechanical Hamiltonian a controlled
  observable-sector representative of a field dynamics, and which bound-state
  information survives admissible variations of the source and eliminated field
  sectors?
- **Presumptions:** a self-adjoint field Hamiltonian has already been constructed
  in a stated regulated or renormalized model; a preparation selects a mechanical
  sector; the comparison window avoids the eliminated-sector spectrum; and the
  compared models have an explicit identification of their mechanical sectors.
- **Representation choices:** an orthogonal projection represents the preparation,
  and a time slice represents the bound-state query. Neither choice is claimed to
  follow from Poincare symmetry alone.
- **Output:** exact formulas for projected response and state recovery; construction
  of the instantaneous electrostatic term from the `U(1)` constraint; a stable-
  observable pseudometric and projector bound; and a precise list of what must be
  proved before N4o's external Coulomb operator is recovered from field theory.
- **Boundary:** no arbitrary Hamiltonian is made tractable. The self-energy may
  retain the full field complexity, and singular source limits or open channels
  require stronger analysis than the bounded calculation here.

## 1. Construct mechanics from a preparation, not by deleting fields

Let `Theta` be a restricted family of field models. For each `theta in Theta`, the
field theory supplies a Hilbert space `H_theta` and self-adjoint dynamics
`mathbb H_theta`. To ask for an atomic bound observable, prepare:

- one light charged-fermion sector;
- a heavy charged source in a specified internal state;
- no resolved transverse radiation in the chosen energy window.

Represent that preparation by a common mechanical Hilbert space `M` and an
isometry

```text
J_theta:M -> H_theta.
```

Then

```text
P_theta=J_theta J_theta^dagger,
Q_theta=I-P_theta
```

are constructed rather than guessed. `P_theta` means “information retained by
this preparation and observable”; it does not mean that the omitted field states
do not exist. The maps `J_theta` also solve a comparison problem: projected
objects from different field Hilbert spaces are pulled back to the same `M`.

The first mechanical observable is therefore not a wavefunction but the prepared
resolvent

```text
G_theta(z)
 =J_theta^dagger(z-mathbb H_theta)^(-1)J_theta:M -> M.
```

For prepared vectors `f,g in M`, its matrix element is exactly the field response

```text
<f,G_theta(z)g>_M
 =<J_theta f,(z-mathbb H_theta)^(-1)J_theta g>_(H_theta).
```

The equality follows directly from the definition of the Hilbert adjoint. Thus
the same prepared excitation and detection are evaluated on both sides; this is
the semantic coincidence that makes `G_theta` a mechanical observable of the
field theory.

## 2. Eliminate the complementary field sector on the same input

Fix `theta` and abbreviate `J,P,Q,mathbb H`. Construct

```text
h=J^dagger mathbb H J:M -> M,

Sigma(z)
 =J^dagger mathbb H Q
   (z-Q mathbb H Q)^(-1)
   Q mathbb H J:M -> M,

F(z)=z-h-Sigma(z).
```

These expressions require `z-Q mathbb H Q` to be invertible on `QH` and the
displayed composites to respect the domains. FM-01 owns the unbounded-operator
theorem contract.

To compute the identity internally, solve

```text
(z-mathbb H)(Ju+v)=Jf,
u in M, v in QH.
```

Applying `Q` gives

```text
(z-Q mathbb H Q)v=Q mathbb H J u,

v=(z-Q mathbb H Q)^(-1)Q mathbb H J u.
```

Apply `J^dagger` to the same equation and substitute this constructed `v`:

```text
[z-h-Sigma(z)]u=f.
```

Consequently

```text
G_theta(z)=F_theta(z)^(-1).
```

This is not merely isospectral notation. Define the recovery map

```text
K_theta(z)u
 =J_theta u
  +Q_theta(z-Q_theta mathbb H_theta Q_theta)^(-1)
   Q_theta mathbb H_theta J_theta u.
```

The `Q` computation above makes the `Q` component of
`(z-mathbb H_theta)K_theta(z)u` vanish. Its `P` component is
`J_theta F_theta(z)u`. Hence

```text
F_theta(E)u=0
  => mathbb H_theta K_theta(E)u=E K_theta(E)u.
```

The field state is recovered from the mechanical state, including its virtual or
eliminated-sector dressing. Mechanics is therefore the exact prepared-sector
presentation `F_theta(E)u=0`, not simply `P mathbb H P`.

## 3. Construct the electrostatic mechanical representative from the field constraint

The static Coulomb term in N4o should not enter as an unrelated potential. On the
spatial slice selected by the preparation, the `U(1)` Gauss constraint is

```text
div E=rho_tot.
```

The Euclidean metric constructs the orthogonal split

```text
E=E_T-grad phi,
div E_T=0.
```

Substitution into Gauss' law computes

```text
(-Delta)phi=rho_tot,
phi=C rho_tot,
C=(-Delta)^(-1)
```

with decay at spatial infinity fixing the inverse. Orthogonality removes the
transverse/longitudinal cross term. Integration by parts on the decaying solution
evaluates the longitudinal energy on the same `rho_tot`:

```text
(1/2)||grad phi||^2
 =(1/2)<rho_tot,C rho_tot>.
```

Write `rho_tot=rho_e+rho_N`. Bilinearity produces the cross interaction

```text
<rho_e,C rho_N>.
```

For a one-electron sector this is multiplication by the source potential
`q_e C rho_N`. Opposite charge signs make it attractive. After subtracting the
prepared source rest energy, this constructs the electrostatic part

```text
h_(rho_N)
 =-i B_tau slash nabla_Sigma+mB_tau+q_e C rho_N,
```

of the finite-source version of N4o's external Hamiltonian. The exact projected
block can also contain source-local contact data or other interactions acting
entirely inside `P`; retain them as `delta h_theta^P`:

```text
h_theta=h_(rho_N)+delta h_theta^P.
```

If the source measure converges to a point charge and the distinguished domains
converge in an appropriate resolvent sense, `q_e C rho_N` tends to `-nu/r`. The
potential formula is computed here; the singular operator-limit statement and
the control of `delta h_theta^P` remain explicit obligations.

The remaining dynamical transverse photons, source recoil/excitation, pair
sectors, and radiative dressing are not discarded. Relative to the chosen `P`,
they occur in

```text
Sigma_theta(z)
 =J_theta^dagger mathbb H_theta Q_theta
  (z-Q_theta mathbb H_theta Q_theta)^(-1)
  Q_theta mathbb H_theta J_theta.
```

The field/mechanics relation is therefore

```text
field dynamics plus preparation
  -> F_theta(z)=z-h_(rho_N)-delta h_theta^P-Sigma_theta(z)
  -> prepared poles, weights, and response.
```

The ordinary external-field equation is the approximation
`delta h_theta^P=0=Sigma_theta(z)` together with frozen source data. It is not the
exact content of field theory.

## 4. The admissible family is generated by physical variations

A model parameter `theta` records only variations that can be prepared or
resolved in the target regime:

```text
theta=(rho_N, source state and mass, direct P-sector coupling data,
       field-sector model, energy window, mechanical injection J_theta).
```

For the present node, admissibility means:

1. `rho_N` has the declared total charge and produces a distinguished
   electrostatic Dirac operator in the chosen domain class;
2. `mathbb H_theta` is self-adjoint in a stated regulated or renormalized field
   model;
3. `J_theta` implements the same preparation semantics on the common `M`;
4. a contour `Gamma` around the target bound cluster lies in the resolvent of the
   eliminated `Q_theta` block;
5. the effective-kernel differences below are bounded on `Gamma`, or a stronger
   form/resolvent theorem is supplied.

This is a restricted physical family, not “all Hamiltonians.” Varying the nuclear
charge distribution probes finite-size stability; varying the source mass probes
recoil; varying `Sigma` probes radiative and eliminated-sector effects. Changing
field content, charge, preparation semantics, or crossing a threshold leaves the
current family and must be typed as a different comparison.

## 5. Observable stability is computed before any coordinate spectrum

Put

```text
L_theta(z)=h_(rho_N)+delta h_theta^P+Sigma_theta(z),
G_theta(z)=[z-L_theta(z)]^(-1).
```

For two admissible models, the two effective operators act on the same `M`.
Compute the inverse identity there:

```text
G_theta(z)-G_eta(z)
 =G_theta(z)[L_theta(z)-L_eta(z)]G_eta(z).
```

Indeed, with `F_theta=z-L_theta` and `F_eta=z-L_eta`, the right side is

```text
G_theta(F_eta-F_theta)G_eta
 =G_theta F_eta G_eta-G_theta F_theta G_eta
 =G_theta-G_eta.
```

Both sides therefore compare the same prepared response, not two unrelated
operator presentations.

Therefore

```text
||G_theta(z)-G_eta(z)||
 <=||G_theta(z)||
   ||L_theta(z)-L_eta(z)||
   ||G_eta(z)||.
```

No gamma subblock, polar coordinate, or component propagator appears. The middle
factor separates the two physical causes of change:

```text
L_theta-L_eta
 =q_e C(rho_(N,theta)-rho_(N,eta))
  +(delta h_theta^P-delta h_eta^P)
  +(Sigma_theta-Sigma_eta).
```

Let `Gamma` be a positively oriented contour isolating a bound-state cluster of
the full field Hamiltonian while remaining inside the Feshbach window. Its
prepared spectral weight is constructed by

```text
Pi_theta^M
 =J_theta^dagger E_(mathbb H_theta)(inside Gamma)J_theta
 =(1/(2 pi i)) integral_Gamma G_theta(z) dz.
```

Integrating the same-input resolvent bound gives

```text
||Pi_theta^M-Pi_eta^M||
 <=length(Gamma)/(2 pi)
   sup_(z in Gamma)
   ||G_theta(z)||
   ||L_theta(z)-L_eta(z)||
   ||G_eta(z)||.
```

This is the first supported stable prediction: if the right side is small, every
prepared transition amplitude through that bound cluster changes by at most the
same amount. It protects the whole degenerate projector rather than an arbitrary
eigenvector basis.

Define the observable pseudometric

```text
d_Gamma(theta,eta)=||Pi_theta^M-Pi_eta^M||.
```

Exact equality `d_Gamma=0` is an equivalence relation; quotienting by it produces
the observable classes. The tolerance statement `d_Gamma<=epsilon` is **not** an
equivalence relation because it need not be transitive; it defines a resolution
neighbourhood or an `epsilon`-cover. This prevents experimental tolerance from
being hidden inside false quotient language.

## 6. What this compresses, and what it only relocates

The construction produces semantic compression when the requested observable is
`Pi_theta^M` or a matrix element of `G_theta` and the effective difference can be
bounded without constructing the full field state. It combines several sources
of computational gain:

- **quotient:** field states indistinguishable by prepared response have zero
  `d_Gamma` distance;
- **locality/scale:** short-distance source structure enters a small set of
  effective data when an EFT error bound is available;
- **sparsity:** only `P-Q` couplings that return to the prepared sector enter
  `Sigma`;
- **recursion:** the `Q` resolvent may itself admit further sector projections;
- **conditioning:** a contour separated from both the target pole and `Q`
  thresholds controls the norm factors.

It is only reformulation when evaluating `Sigma_theta(z)` requires the same full
inverse and no bound, recursion, or reusable kernel is obtained. It becomes an
epicycle-like correction program when an increasing list of source- and energy-
specific terms is added without a stable effective-data class. A threshold,
nonanalytic pole merger, pair-production boundary, or loss of a common
preparation map is instead evidence that this mechanical ontology has reached its
failure boundary.

## 7. Supported frontier and next computation

Supported in this node:

- mechanics is constructed as a prepared field observable on a common space;
- the exact Schur equation and full-state recovery are computed on one input;
- Gauss' law constructs the instantaneous finite-source Coulomb term;
- radiative, recoil, and open field sectors are localized in one typed
  energy-dependent self-energy;
- bounded effective-kernel variation gives an explicit projected-resolvent and
  bound-cluster stability estimate;
- exact quotient and finite-resolution neighbourhood are correctly distinguished.

Still open:

- construction of a common cutoff-independent relativistic QED Hamiltonian in
  the required charged sectors;
- a controlled operator limit from the heavy finite source to N4o's point
  Dirac--Coulomb Hamiltonian;
- an evaluated bound on `Sigma_theta-Sigma_eta` for an atomic pole;
- continuation across a `Q` threshold, where widths and scattering boundary
  values replace an isolated self-adjoint projector;
- a whole-route cost comparison against direct spectral or field computation.

The smallest honest computation node is therefore not an exact Coulomb spectrum.
It is:

```text
choose one UV-controlled heavy-source field model and one isolated contour
 -> bound q_e C(delta rho_N) and delta Sigma(z) on that contour
 -> certify the change of the prepared bound-cluster projector
 -> compare this cost with direct recomputation.
```

That calculation will decide whether the field/mechanics bridge supplies actual
computational gain or only an exact re-expression.

## Edges

- `N4o -> N4r`: pass the distinguished external electrostatic Dirac operator,
  domain obligation, and gap spectral measure.
- `N4q -> N4r`: pass the same-observable compression contract, projected-resolvent
  target, and whole-route rejection test.
- `FM-01/FM-02 -> N4r`: pass exact sector recovery and the field Green-object to
  energy-dependent mechanical-equation contract.
- `FM-03/FM-04 -> N4r`: pass heavy-source effective data and the general-charge
  distinguished-domain boundary.
- `N4r -> field/mechanics stability computation`: pass `L_theta`, `G_theta`,
  `Pi_theta^M`, the contour estimate, and the exact residual obligations.
- `N4r -> N7/manuscript synthesis`: pass the distinction among an external
  mechanical presentation, a prepared field observable, and a controlled
  effective theory only after one quantitative stability computation succeeds.
- `N4r -> N4s`: pass the prepared pole, fiber recovery map, and source/self-energy
  stability obligations; N4s adds total-momentum covariance and the asymptotic
  criterion required before calling the bound level a composite particle.
- `N4r -> N4t`: pass the prepared fiber resolvent and recovery identity; N4t
  replaces pointwise recovery by the spectral atom at a massless threshold
  and checks both against one dressed-atom band.
- `N4r -> N9`: pass the noninvariant prepared projection, exact self-energy, and
  dressing recovery as the memory-bearing mechanics case.
- `N4r -> N9a`: pass the departure map, complementary spectral measure, pole
  equation, and dressing recovery for one explicit threshold evaluation.
- `N4r -> N4u`: pass the scalar Schur equation, complementary recovery vector,
  and same-observable cost criterion for effective-mass differentiation.
- `N4r -> N4v`: pass the prepared rest-pole equation and the requirement that its
  recovered field state become a sharp stable Poincare spectral component.
- `N4r -> N4w`: pass the prepared-channel and recovery semantics; N4w tests their
  on-shell pole/fusion analogue while retaining the missing Hamiltonian-Schur
  equality as an explicit boundary.

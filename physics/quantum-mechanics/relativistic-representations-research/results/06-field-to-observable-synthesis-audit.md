# Field-to-Observable Synthesis Audit

Status: audit amended by N9e's scalar provenance and N9f's predictive-window test; the Typst manuscript is unchanged  
Worktable: `physics/quantum-mechanics/relativistic-representations.typ`  
Audited path: N1--N4/N4m/N4i--N4z, N4q/N4r/N4y, and N9--N9f

## Audit question

Does the current graph support one readable deduction of the form

```text
group representation
  -> local field equation
  -> quantum field Hamiltonian
  -> preparation and departure measure
  -> bound and open-channel predictions?
```

## Verdict

The original audit found **two strong modules and one unconstructed interface**.
N9e now closes that interface for one regulated scalar model, but not as a
universal consequence of representation theory:

```text
Module F: exact free realization

representation datum
  -> covariant carrier and local complex
  -> causal source quotient / positive shell
  -> one-particle Hilbert representation
  -> free CCR/CAR Fock recovery

       N9e scalar bridge: declared profile + mobile two-level system
         -> self-adjoint H_full -> exact total-momentum fiber

Module O: observable compression for a supplied dynamics

derived scalar fiber plus declared preparation J
  -> departure B and coupling-visible measure
  -> memory / self-energy / detector transforms
  -> bound and open order-g^2 coefficients.
```

The portable global claim is therefore:

> Symmetry and local field realization construct admissible free state content;
> after an interacting dynamics and preparation are supplied separately, an
> observable-selected spectral measure can compress several bound and open
> predictions.

The stronger claim is unsupported:

> The group-derived field equation itself determines the interacting Hamiltonian
> or the N9c/N9d coupling measure.

This distinction still controls manuscript synthesis. N9c/N9d/N9e/N9f now form a
valid same-model benchmark for observable compression, but they are not the
universal predictive endpoint of the relativistic-representation derivation: the
profile, two-level system, coupling, and nonrelativistic matter dynamics remain
additional inputs.

## 1. Bridge coverage

| Bridge | Exact object passed | Status | Audit consequence |
| --- | --- | --- | --- |
| representation -> physical fiber | massive spin or massless helicity little-group representation | supported by N1--N2b | safe main argument |
| physical fiber -> local realization | covariant carrier, symbol/complex, physical kernel or quotient | supported by N3--N4; finite-spin boundaries explicit | safe main argument |
| local realization -> free one-particle Hilbert space | positive shell map from the causal source quotient | supported on the compact-source image; full induced-space density remains open | state the image boundary |
| one-particle space -> free quantum field | symmetric/antisymmetric Fock functor and vacuum recovery | exact in N4y/N4z | safe free quantization result |
| free field -> interacting dynamics | scalar shell amplitude, declared spatial profile, self-adjoint full Hamiltonian, exact momentum fiber, and free limit | supported by N9e for one massive regulated scalar/two-level model | scalar interface closed; universal interaction selection open |
| supplied dynamics -> prepared response | preparation isometry, projection, Feshbach response, and dressing recovery | exact abstractly in N4r under operator contracts | safe theorem, not a model derivation |
| retained information -> dynamics | invariant-kernel or exact-memory criterion | exact for bounded linear evolution in N9; unbounded use is contracted | safe abstract discriminator |
| supplied `H,J` -> coupling-visible measure | `M_B=B^dagger E_Q B` on the cyclic sector | exact abstractly in N9b | construction cost can remain full-Fock |
| regulated scalar field -> computable measure | radial free one-boson pushforward | complete order-`g^2` coefficient in N9c | genuine model-local compression |
| continuum boundary -> operational event | finite-time emitted-boson projection and survival/memory identities | N9d coefficient plus N9f exact Duhamel remainder | finite short-time window certified; `t=80` remainder vacuous |
| leading measure -> finite-coupling prediction | same exact ground energy and emitted-boson event | N9f combined-parity/Feshbach and finite-sector Duhamel bounds | ground and short-time open prediction supported; long-time rate not certified |
| boundary/event -> resonance or scattering | complex pole or incoming/outgoing wave operators | deliberately absent | do not synthesize as lifetime or `S` matrix |

## 2. The recorded defect and its bounded resolution

N4y ends with a free one-particle representation `H_1`, its Fock space, vacuum,
and smeared free field. N4r begins by presuming that a self-adjoint interacting
Hamiltonian has already been constructed. N9 begins with a supplied evolution
`T_t` or generator `L`. Before N9e, N9c/N9d then postulated a massive scalar
Nelson/spin--boson Hamiltonian with nonrelativistic recoil, Gaussian coupling,
and a two-level internal space.

Before N9e, no composite performed

```text
(free carrier/complex, source quotient, Fock field)
  -> choose an interaction constrained by locality/symmetry/gauge
  -> construct a self-adjoint H_g and state Omega_g
  -> construct preparation J
  -> recover H_free and the N4y one-particle injection as g -> 0.
```

N9e resolves the model-local part by computing

```text
massive Klein--Gordon positive shell H_1
  -> Phi_0(h)Omega=iota_1(h)
  -> f_hat=sqrt(2 omega)h
  -> H_full with [H_full,P_X+P_f]=0
  -> H_g(p) under exact fiber conjugation
  -> B=QH_gJ
  -> N9d's M_(B,2).
```

The Gaussian in N9d is thereby identified as a shell amplitude, not a Gaussian
spatial source. Its corresponding profile is Schwartz and noncompact. N4q's
determination boundary remains intact: symmetry does not choose that profile,
`M`, `Delta`, `g`, or the internal flip. N9e constructs the bare-vacuum
preparation required for the complete order-`g^2` coefficient. N9f subsequently
constructs the zero-momentum interacting ground vector and a finite-coupling
remainder, but only a bounded short-time remainder for the open preparation.

### Smallest bridge bench: discharged

N9e implements the smallest discriminating scalar bench:

```text
N4 scalar Klein--Gordon realization
  -> N4y positive shell and bosonic Fock field
  -> smeared field Phi(h) constructed from that shell
  -> a declared two-level/mobile preparation coupled by sigma_x Phi(h)
  -> self-adjointness and free-limit contract
  -> N9d detector event from the resulting H_g.
```

This establishes **scalar-field provenance** for N9d. It does not establish a
universal interaction for every spin, nor a fully relativistic composite-particle
model. Those are different, larger claims.

## 3. Semantic-preservation audit

The route preserves different objects on different segments; claiming one object
survives end to end would be false.

| Segment | Semantic invariant actually preserved |
| --- | --- |
| N2--N4 | the specified little-group representation on the physical fiber |
| N4g/N4k--N4y | the same compact-source shell amplitude and one-particle vector |
| N4q--N9 | the same named observable evaluated before and after a proposed reduction |
| N4r--N9b | the same prepared return response under projection, memory, and resolvent transforms |
| N9c | the same leading one-boson field measure under radial, energy, Fourier, Stieltjes, and moment representations |
| N9d | the same finite-time emitted-boson event under detector norm, memory curvature, and boundary-rate limits |
| N9e | the same shell vector through spatial smearing, Fock injection, translation reduction, vacuum departure, and N9d's free-complement measure |
| N9f | the same exact ground energy and detector event before and after the leading-measure approximation |

N9e now records the change of invariant at the interface. The free scalar shell
vector becomes the created field factor of N9d's prepared two-level state; the
two-level label remains an additional tensor factor rather than being falsely
identified with the scalar particle. The global composition is still modular:
free field output, declared dynamics input, then observable semantics.

## 4. Constructivism and readability

### What is now readable

- N2/N3 construct representation spaces and maps before using them.
- N4m and the half-integer branch reduce repeated low-spin calculations to
  reusable complexes and source/shell maps.
- N4y computes free quantization and one-particle recovery on the same source.
- N9 derives descent, memory, and self-energy from explicit block operations.
- N9c derives its density from `H_g,P,B`, rather than prescribing a bath density.
- N9d defines an actual detector projection before calculating emission.
- N9e distinguishes the spatial profile from its shell amplitude and computes
  the total-momentum fiber before identifying it with N9d's Hamiltonian.
- N9f constructs the conserved combined parity before estimating, then compares
  exact and leading observables through explicit remainder identities.

### What obstructs synthesis

1. **The current Typst order contradicts the supported argument.** It begins with
   coordinate identities, has empty headings, and postpones the actual thesis to
   line 424. The architecture already recommends the reverse order.
2. **The line-424 thesis is too strong.** “Relativistic wave equations are nothing
   but eigenvalue problems ... and ... follow rigidly” conflicts with N1 and N4q:
   representation data do not fix carriers, interactions, domains, or dynamics.
3. **Several global diagrams repeat with slightly different vocabulary.** N4q,
   N4y, N9, N9b, N9c, and N9d should not all become consecutive manuscript
   sections. One synthesis diagram should own the vocabulary; model nodes should
   become one benchmark.
4. **Notation is overloaded.** `P` denotes total momentum, a preparation
   projection, and visually evokes the Poincare group; `W` denotes both
   realization and access maps. A synthesis should use

   ```text
   bold p             total momentum,
   J                  preparation isometry,
   Pi=JJ^dagger       prepared projection,
   Q=1-Pi             complement,
   B=QHJ              departure from the preparation space,
   M_B=B^dagger E_(QHQ)B.
   ```

5. **“Same measure” currently names three related levels.** Keep separate:

   ```text
   M_B^(g)       exact interacting operator-valued measure,
   nu_2          leading free one-boson base measure,
   M_(B,2)       shifted/operator-valued pushforwards used by N9d.
   ```

6. **Exactness levels need visual labels.** Use only:

   ```text
   exact structural identity,
   exact theorem under named contracts,
   complete perturbative coefficient,
   numerical regression,
   open quantitative remainder.
   ```

## 5. Computability audit

### Genuine reductions

- N4m reuses one scalar Green denominator and quotients gauge-null directions.
- N9b removes the coupling-invisible reducing complement exactly.
- N9c combines that quotient with boson-number order, rotations, and an injective
  radial dispersion, reducing a Fock return coefficient to one quadrature.
- N9d applies target kernels directly to that measure and never reconstructs the
  dressed state merely to obtain the detector probability.
- N9f certifies the ground route through one scalar Feshbach transform and the
  short-time detector route through three finite Fock-sector norm actions.

The supported short computational route is

```text
(H_g,J) -> B -> nu_2 -> one target transform -> observable coefficient.
```

Each arrow preserves a named object and has low transformation depth.

### Work only relocated or still absent

- selecting the interaction profile and internal matter system from additional
  physical input rather than symmetry;
- evaluating the exact finite-`g` cyclic spectral measure;
- controlling the long-time `t=80` event through phase-sensitive estimates rather
  than the vacuous time-polynomial norm bound;
- removing the boson mass and Gaussian cutoff;
- constructing a physical atomic form factor;
- obtaining a resonance lifetime or normalized scattering amplitude.

The N9c/N9d quadrature coincidences test implementation and transform identities.
They are not certified error bounds for perturbation theory. In particular,
`Gamma t<0.25` monitors secular loss but does not bound the omitted Dyson terms.
N9f supplies separate analytic Feshbach/Duhamel bounds and shows directly that
the latter becomes vacuous at the same `t=80` point.

## 6. Presumption debt

| Presumption/resource | What it buys | Why it is nonportable |
| --- | --- | --- |
| four-dimensional Minkowski free theory | Wigner fibers and local finite-spin complexes | no curved background or interaction |
| chosen positive frequency and Fock state | exact free CCR/CAR recovery | not selected by a general equation/background |
| self-adjoint scalar Hamiltonian | spectral theorem, Feshbach map, unitary evolution | N9e constructs it from declared regular inputs, not from symmetry |
| massive scalar boson | gap and regular threshold | avoids infrared/infraparticle behavior |
| Gaussian radial form factor | ultraviolet finiteness and one-dimensional reduction | not a derived physical coupling |
| rotations and injective dispersion | scalar density and mass recovery | fails for anisotropic/noninjective channels |
| two internal levels | simultaneous bound/open preparations | not derived from the relativistic carrier spine |
| small coupling/order `g^2` | one-boson first return | no finite-coupling lifetime or dressed measure |
| one-boson detector | explicit finite-time event | not a multichannel or inclusive scattering observable |

These resources make N9c/N9d/N9e/N9f an effective internal bench. They must appear before
the numerical values, not after them as caveats.

## 7. Safe manuscript synthesis

The current Typst paper should remain a **free representation-to-field paper**.
The safe endpoint is:

```text
representation datum
  -> local field realization
  -> physical source/shell quotient
  -> free quantization and recovery
  -> boundary: an equation is not yet an interacting prediction.
```

N4q/N9 can contribute one short concluding interface explaining what additional
objects a prediction needs. N9e now derives N9c/N9d's scalar Hamiltonian from the
free scalar field plus declared model inputs, but the nonrelativistic body and
profile are not consequences of the relativistic representation construction.
The three nodes therefore belong in a companion research note or a clearly
labeled model benchmark rather than as an uninterrupted universal theorem.

### Minimal future manuscript tasks

1. Replace the line-424 rigid-determination thesis with N1's determination
   boundary.
2. Follow the existing manuscript architecture rather than dimension-first source
   order.
3. Add one notation/exactness legend shared by the free and global discussions.
4. End the free paper with the typed interaction interface, not the N9d numbers.
5. Synthesize N9c--N9f separately around one diagram and one table if a companion
   observable-compression note is desired.

No manuscript edit is authorized or performed by this audit.

## 8. Global frontier after the audit

### Supported spine

- finite-spin/helicity free realization and compact-source free quantization;
- observable-relative compression and exact memory/self-energy semantics for a
  supplied dynamics;
- field-derived one-boson measure and operational bound/open coefficient regression
  in one regulated scalar two-level model;
- exact scalar profile/Fock/full-Hamiltonian/fiber provenance for that benchmark,
  with interaction selection and relativistic matter explicitly excluded;
- finite-coupling ground and short-time detector certificates, with the long-time
  boundary-rate prediction explicitly uncontrolled.

### Bounded bridge verdict and next stop

The scalar interaction-provenance interface is constructed and N9f has tested its
predictive leverage. The ground and short-time event are controlled; the long-time
rate is not. The branch stops here: higher perturbative order, kinetic scaling,
resonance, scattering, a physical atom, a massless field, or a
relativistic/higher-spin interaction each changes the output or model and must be
justified by a new manuscript need.

### Parked branches and re-entry conditions

- **long-time phase-sensitive remainder:** re-enter for a numerical lifetime claim;
- **resonance:** re-enter for an exponential finite-coupling decay law;
- **scattering:** re-enter for a normalized incoming/outgoing amplitude;
- **physical atom/transverse field:** re-enter for comparison with spectroscopy;
- **massless field:** re-enter for infrared or infraparticle conclusions;
- **higher spin interaction:** re-enter only after one scalar provenance bridge
  shows which construction must generalize;
- **adaptive moments/Euclidean inversion:** re-enter for a named resolution target,
  not generic improvement.

## Audit checks

- The free manuscript architecture and current Typst order were compared directly.
- Every claimed cross-node edge was checked for the exact object it passes.
- Exact identities, theorem-contract uses, perturbative coefficients, and numerical
  regressions were separated.
- The N9c and N9d computations remain independently executable and passing.
- N9e's source--shell and same-measure regression passes independently.
- N9f's ground and finite-time certificate regression passes independently.
- No claim depends on treating a continuum boundary as an `S` matrix or a secular
  coefficient as an exponential law.

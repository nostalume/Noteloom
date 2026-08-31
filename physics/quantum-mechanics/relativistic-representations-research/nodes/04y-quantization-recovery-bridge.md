# N4y — Quantization and One-Particle Recovery Inside the Global View

Status: free bosonic and fermionic quantization/recovery loops supported; the
fermionic causal-Euler/CAR equality is closed downstream by N4z; interacting
branches retain model-dependent theorem contracts, while N8 supplies the first
leading collective-response reduction  
Consumes: [N4g bosonic positive shell](04g-positive-frequency-completion.md),
[N4h bosonic faithfulness](04h-support-faithfulness.md), [N4k fermionic positive
shell](04k-half-integer-positive-frequency.md), [N4l fermionic
faithfulness](04l-half-integer-support-faithfulness.md), [N4s field/particle
extraction](04s-field-particle-extraction.md), [N4r field/mechanics
projection](04r-field-mechanics-stability.md), and [quantization--recovery source
contracts](../sources/quantization-recovery-contracts.md)  
Produces: an exact free same-source recovery diamond, a precise statement of what
field quantization adds, and a common placement of bounded, scattering, and
collective outputs after—not inside—the field equation

## Node contract

- **Question/capability:** after representation data have been realized by a
  local equation, what additional constructions turn the equation into a quantum
  theory, and when does that theory recover the same one-particle representation
  or a mechanical effective sector?
- **Presumptions:** one separate finite-spin free system from N4g or N4k; its
  faithful positive-shell map; a chosen Poincare-invariant positive-frequency
  structure; the standard symmetric or antisymmetric Fock functor; and, for the
  interacting branch, N4s's vacuum/spectrum/stability assumptions.
- **Representation choices:** positive frequency selects a state and
  one-particle structure. It is not determined by the differential equation on a
  general background. Fock representation is exact for the selected free system
  and an asymptotic construction for suitable interacting particles, not a
  universal interacting state space.
- **Output:** one commuting free recovery diagram; exact CCR and vacuum-to-shell
  equality on the bosonic branch; exact fermionic one-particle recovery with its
  causal/CAR coincidence completed in N4z; and a typed global diagram separating
  equation, quantization, response, and observable reduction.
- **Boundary:** no claim is made that every field theory has particles, every
  particle sector is Fock-complete, every collective mode is a particle, or a
  compact field equation makes its spectral and scattering observables cheap.

## 1. Why the equation cannot be the endpoint

N1--N4 begin with representation data and construct a local field presentation:

```text
mass/spin or helicity representation
  -> covariant carrier and physical fiber
  -> local symbol or gauge complex
  -> equation whose physical kernel realizes that fiber.
```

This solves a realization problem. It does not yet construct probabilities,
vacuum correlations, particle number, a bound-state observable, or scattering.
Those require further objects:

```text
equation/gauge complex
  -> action or causal pairing
  -> observable quotient
  -> quantum algebra
  -> state and Hilbert representation
  -> response or spectral object
  -> observable-specific reduction.
```

Each arrow changes the question. The equation determines admissible histories or
solutions after its domain and background are fixed. The causal pairing determines
which linear observables fail to commute. Quantization constructs their algebra.
A state constructs expectation values and a Hilbert representation. Only then can
a spectral, bounded, scattering, or collective query be posed.

## 2. Construct the multiplicity space without coordinates

For a complex Hilbert space `H`, define

```text
Gamma_+(H)=direct-sum_(r>=0) Sym^r H,
Gamma_-(H)=direct-sum_(r>=0) Alt^r H.
```

The zero-fold tensor power is `C`. It supplies the vacuum

```text
Omega=(1,0,0,...).
```

The canonical one-particle injection and projection are

```text
iota_1(u)=(0,u,0,...),
P_1(z_0,z_1,z_2,...)=iota_1(z_1).
```

Thus

```text
P_1 iota_1=identity_H.
```

This equality is the basic recovery witness. The Fock functor adds all finite
symmetrized or antisymmetrized multiplicities while retaining `H` as a canonical
summand. It does not quantize the differential equation a second time; it changes
the allowed multiplicity of the already constructed one-particle object.

If `U_1(g)` is the N3/N4g/N4k one-particle Poincare action, define on the `r`-fold
sector

```text
Gamma_+/-[U_1(g)]|_(H^(tensor_+/- r))=U_1(g)^(tensor_+/- r).
```

Apply the two sides to the same `u in H`:

```text
Gamma_+/-[U_1(g)] iota_1(u)
 =iota_1(U_1(g)u).
```

Hence `iota_1` is an intertwiner. The particle representation derived before the
field equation is not lost when variable multiplicity is introduced.

## 3. The bosonic source, quantum field, and shell amplitude coincide

Fix one integer spin `s`. N4g/N4h supply:

```text
O_s^R                         faithful real causal source quotient,
W_s:O_s^R -> H_(src,s)        future-shell one-particle map,
omega_s(u,v)=2 Im <W_su,W_sv> causal symplectic form.
```

Construct the symmetric Fock space

```text
F_s=Gamma_+(H_(src,s)).
```

Let `a^dagger(u)` be creation and `a(u)` annihilation, normalized by

```text
[a(u),a^dagger(v)]=<u,v> identity,
a(u)Omega=0.
```

For the same real source class `x in O_s^R`, define the smeared field

```text
Phi_s(x)=a(W_sx)+a^dagger(W_sx).
```

The commutator is computed on two source classes `x,y`:

```text
[Phi_s(x),Phi_s(y)]
 =<W_sx,W_sy>-<W_sy,W_sx>
 =2i Im <W_sx,W_sy>
 =i omega_s(x,y).
```

Thus the quantum commutator is exactly the causal pairing already produced by
the field equation and action; no polarization or component propagator is added.
If the source supports are causally disjoint, N4f's causal support makes
`omega_s(x,y)=0`, so the same computation gives locality.

Now evaluate the field on the vacuum:

```text
Phi_s(x)Omega
 =a(W_sx)Omega+a^dagger(W_sx)Omega
 =iota_1(W_sx).
```

Project the same vector to the one-particle sector:

```text
P_1 Phi_s(x)Omega
 =P_1 iota_1(W_sx)
 =iota_1(W_sx).
```

Every `W_sx` has positive-shell translation spectrum. If `E_F(Sigma_s)` is the
Fock translation projection onto that shell, then on this already one-particle
vector

```text
E_F(Sigma_s)Phi_s(x)Omega=iota_1(W_sx).
```

This is N4s's free spectral extractor evaluated on the same source class. N4h's
faithfulness gives the null coincidence

```text
W_sx=0
  iff Phi_s(x)Omega=0
  iff E_F(Sigma_s)Phi_s(x)Omega=0
  iff x=0 in O_s^R.
```

The free bosonic recovery diamond therefore commutes exactly. Its range is
`H_(src,s)`. Equality with all of N3's induced Wigner space still requires N4g's
open compact-source density theorem.

## 4. Fermionic multiplicity recovery and the downstream local equality

Fix `n>=0`. N4k/N4l construct a faithful real-linear map

```text
W_n^pair:O_n^C -> H_(src,n)
                  =H_n^part direct-sum H_n^anti.
```

Construct

```text
F_n=Gamma_-(H_(src,n)).
```

For `u` in the real span of the paired image, put

```text
b(u)=a(u)+a^dagger(u).
```

The CAR is computed without a spinor component basis:

```text
{b(u),b(v)}
 =<u,v>+<v,u>
 =2 Re <u,v>.
```

On the vacuum,

```text
b(W_n^pair x)Omega=iota_1(W_n^pair x),
P_1 b(W_n^pair x)Omega=iota_1(W_n^pair x).
```

N4l's faithfulness therefore gives

```text
b(W_n^pair x)Omega=0 iff x=0 in O_n^C.
```

The particle/antiparticle one-particle space is recovered exactly after the
antisymmetric multiplicity construction.

The remaining local claim is proved downstream in
[N4z](04z-fermionic-car-coincidence.md). It computes on the same source classes

```text
tau_Euler(x,y)=2 Re <W_n^pair x,W_n^pair y>
```

with the correct conjugation and normalization conventions. Its witness first
annihilates the gauge part of a canonical screen lift, removes trace reversal on
the gamma-traceless representative, and then uses one null Clifford homotopy.
The causal propagator's energy sign cancels the screen metric's energy sign.
After the one allowed overall action normalization, N4z obtains

```text
tau_Euler(x,y)=2 Re <W_n^pair x,W_n^pair y>,

causally disjoint supports
  -> tau_Euler(x,y)=0
  -> graded locality.
```

Thus the local Euler observable, positive particle/antiparticle space,
antisymmetric multiplicity, and one-particle recovery are one construction.
Density in the whole induced representation and optional Majorana real forms
remain separate.

## 5. The free diamond deforms into extraction, not a global interacting Fock identity

For a free theory the previous construction starts with a known `H_(src)` and
builds `Gamma_+/-H_(src)`. N4s reverses the direction in an interacting theory:

```text
quantum field algebra, state Omega, and translations
  -> sharp stable spectral quotient H_Sigma
  -> asymptotic multiplicity space Gamma_stat(H_Sigma)
  -> Moller maps Omega^(in/out):Gamma_stat(H_Sigma)->H_field.
```

The Moller maps are conditional on the stability and regularity contracts in
N4s/FP-01. They are not an identification of the microscopic interacting Hilbert
space with one Fock space. Apply a one-particle vector `u in H_Sigma` to the same
asymptotic map:

```text
Omega^(in/out)iota_1(u)=u.
```

Here equality means the stable spectral state already contained in `H_field`;
the asymptotic construction adds separated multiparticle configurations around
it. Surjectivity is the separate asymptotic-completeness question.

Thus the free and interacting directions have different epistemic order:

```text
free:         known particle space -> multiplicity field representation;
interacting:  field dynamics -> extract stable particle space -> asymptotic multiplicity.
```

This explains why “second quantization” is useful terminology for the free
multiplicity functor but an incomplete ontology for interacting QFT.

## 6. Bounded, scattering, and collective dynamics are different queries

After an algebra, state, and dynamics are constructed, one response object can
support several incompatible observable reductions:

| Query | Constructed selector | Output | Existing owner |
| --- | --- | --- | --- |
| prepared bounded dynamics | injection `J`, projected resolvent, isolated contour | bound-cluster projector and effective mechanical kernel | N4r |
| stable particle | sharp translation shell and field-created quotient | Wigner one-particle space | N4s |
| scattering | asymptotic time limits or resolvent boundary values | incoming/outgoing embeddings and `S` matrix | N4s/N4n |
| resonance | continued pole with no real spectral projector | position and width with continuation boundary | open in N4s |
| collective response | conserved density, equilibrium state, and hydrodynamic scaling | diffusion pole and density-response kernel | N8 |

The selectors are not interchangeable. An isolated eigenvalue is intrinsic to one
Hamiltonian and preparation. Scattering compares full and asymptotic dynamics.
A collective mode may be a pole or concentration of a many-body response without
being a microscopic particle or a sharp vacuum Wigner shell.

N8 implements the minimal collective contract from a named conserved density,
state `omega`, and response function

```text
chi_ij(z,k),
```

and constructs the diffusion kernel only after conservation-law closure and a
controlled derivative expansion. Both microscopic and reduced routes compute
the response of the same density to the same chemical-potential source. The
microscopic computation of conductivity and a model-specific remainder bound
remain open rather than being hidden inside the effective equation.

## 7. Reconstructed global view

The project now has a larger spine than field-equation derivation:

```text
representation and symmetry
  -> classify admissible state content and covariance;

field realization and equation
  -> present that content locally, with gauge and off-shell choices;

action, algebra, state, and dynamics
  -> construct quantum observables, correlations, and response;

observable selector
  -> choose bounded, particle, scattering, resonance, or collective information;

verified reduction
  -> compute that information through a semantic quotient, exact factorization,
     asymptotic limit, approximation, or model-local algorithm.
```

This view neither ranks mechanics below fields nor promotes an additional
quantization ordinal. Mechanics is the compressed prepared sector constructed by
N4r. A particle is the stable spectral quotient constructed by N4s. A Fock space
organizes multiplicity when its one-particle input or asymptotic output exists.
Collective variables become new primitives only when their response construction
and recovery map beat or extend the microscopic description.

The field equation remains essential because it constructs locality, admissible
sources, gauge equivalence, and causal propagation. It is intermediate because
none of those facts selects a state, an observable, or a computational reduction.

## 8. Computability verdict and open boundary

The supported free bosonic route has low semantic depth:

```text
source class
  -> shell amplitude W_sx
  -> one creation operation
  -> the identical one-particle vector.
```

No component expansion and no repeated solution of the equation occurs. The Fock
construction is reusable because all multiplicity sectors are functorial in one
Hilbert space and one representation.

What it does not reduce:

- construction of an interacting vacuum or correlator;
- discovery of a stable shell, bound pole, resonance, or collective variable;
- evaluation of Moller maps or proof of asymptotic completeness;
- N4r's eliminated-sector self-energy;
- numerical spectra or graph integrals in a generic interacting theory.

The former smallest unresolved computation inside this node was the all-rank
fermionic equality

```text
local causal Euler form = CAR real form of W_n^pair;
```

N4z closes it. N8 independently constructs the first collective mode and its
microscopic response-recovery map in a regime where neither a prepared bound
state nor a vacuum Wigner shell is the right output. Its remaining frontier is
microscopic transport evaluation and certified hydrodynamic error, not another
quantization step.

## Verification ledger

| Obligation | Same-input witness | Boundary |
| --- | --- | --- |
| retain the one-particle representation | `P_1 iota_1=identity` and `Gamma(U_1)iota_1=iota_1U_1` | selected `H_(src)` only |
| bosonic CCR | direct commutator equals `i omega_s` | N4g's normalization and N4h faithfulness |
| bosonic spectral recovery | `Phi_s(x)Omega=iota_1(W_sx)` | compact-source image; N3 density open |
| fermionic multiplicity recovery | `P_1 b(W_n^pair x)Omega=iota_1(W_n^pair x)` | positive realification of N4k's image |
| fermionic local CAR field | `tau_Euler=2 Re <W_n^pair .,W_n^pair .>` | closed downstream by N4z; full induced-space density open |
| interacting Fock relation | `Omega^(in/out)iota_1(u)=u` | stable-shell scattering theorem contract |
| collective reduction | same density response recovered from `chi,sigma` and the diffusion kernel | leading derivative order in N8; microscopic coefficients/remainder open |

## Edges

- `N4g/N4h -> N4y`: pass the faithful bosonic shell map, positive inner product,
  and causal symplectic form; N4y returns the exact CCR/vacuum/shell coincidence.
- `N4k/N4l -> N4y`: pass the faithful particle/antiparticle shell map; N4y returns
  exact antisymmetric multiplicity recovery and isolates the equality closed by
  N4z.
- `N4s -> N4y`: pass the interacting spectral quotient and asymptotic theorem
  contracts; N4y distinguishes extraction from a microscopic Fock identity.
- `N4r -> N4y`: pass mechanics as a prepared projected response, placing bounded
  dynamics beside rather than before field quantization.
- `N4y -> N7/manuscript synthesis`: pass the distinction among representation,
  equation, algebra/state, spectral extraction, and computational equivalence.
- `N4y -> N4z`: pass the exact two forms and normalization coincidence to be
  evaluated on common compact source classes; N4z closes the equality.
- `N4y -> N8`: pass the observable/response/recovery contract without assuming
  that a collective mode is a Wigner particle; N8 constructs diffusion from a
  microscopic conserved density.

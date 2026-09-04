# Nonintegrable Composite Robustness Source Contracts

These contracts support
[field--mechanics boundary](../nodes/09-field-mechanics-reduction-boundary.md). They distinguish a
controlled deformation of the node 09 breather from the exact factorization that
made node 09 solvable.

## NI-01 — Form factors reduce the first nonintegrable mass shift to one scalar

- **Source:** G. Delfino, G. Mussardo, and P. Simonetti,
  [Non-integrable Quantum Field Theories as Perturbations of Certain Integrable
  Models](https://arxiv.org/abs/hep-th/9603011).
- **Hypotheses consumed:** a massive solvable relativistic reference theory,
  known asymptotic particles and form factors, a scalar perturbing field
  `Psi`, a small coupling, and the paper's asymptotic-state normalization.
- **Output consumed:** to first order,

  ```text
  delta m_a^2 = 2 lambda F_(a anti-a)^Psi(i pi),
  ```

  together with first-order vacuum-energy and scattering corrections. The
  paper also identifies elastic factorization and absence of production as
  special consequences of integrability rather than generic relativistic
  kinematics.
- **Research use:** node 09 turns the exact node 09 rest mass into a one-form-factor
  tangent and keeps the normalization, remainder, and isolation hypotheses
  visible.
- **Boundary:** this is a perturbative expansion, not an all-orders persistence
  theorem. At higher order, disconnected pieces, intermediate spectral sums,
  inelastic thresholds, and any ultraviolet subtractions required by the chosen
  operator scheme enter.

## NI-02 — Locality relative to the soliton decides survival or confinement

- **Source:** G. Delfino and G. Mussardo,
  [Non-integrable aspects of the multi-frequency Sine-Gordon
  model](https://arxiv.org/abs/hep-th/9709028).
- **Hypotheses consumed:** sine-Gordon deformed by
  `lambda cos(alpha phi + delta)`, with the reference vacuum and adiabatic
  convention fixed.
- **Output consumed:** the perturbation has soliton semilocality index
  `alpha/beta`; its soliton--antisoliton form factor obeys

  ```text
  -i Res_(theta=+/- i pi) F_(s anti-s)^Psi(theta)
    =[cos(delta)-cos(delta -/+ 2 pi alpha/beta)] <exp(i alpha phi)>.
  ```

  A nonzero annihilation residue gives a divergent first-order soliton mass
  correction and diagnoses confinement. For rational `alpha/beta=m/n`, the
  combined potential has period `2 pi n/beta`; generically only packets of `n`
  old solitons remain topological asymptotic excitations.
- **Research use:** `alpha/beta=2` makes the residue vanish and preserves each
  old vacuum value, whereas `alpha/beta=1/2`, `delta=0` gives a nonzero residue
  and confines the single-soliton channel.
- **Boundary:** a vanishing residue removes this confinement obstruction but
  does not prove all-orders particle stability. A nonzero residue invalidates
  the old constituent channel; it does not say that no neutral mesons exist.

## NI-03 — The chosen second harmonic is a genuine relevant nonintegrable model

- **Source:** Z. Bajnok, L. Palla, G. Takacs, and F. Wagner,
  [Nonperturbative study of the two-frequency Sine-Gordon
  model](https://arxiv.org/abs/hep-th/0008066).
- **Hypotheses consumed:** two nonzero cosine interactions with unequal
  frequencies, treated as perturbations of the compact free boson.
- **Output consumed:** generic unequal-frequency two-cosine models are
  nonintegrable; each frequency must satisfy `alpha^2<=8 pi` for relevance in
  canonical normalization, and `alpha beta<=4 pi` avoids generation of extra
  first-order periodic counterterms in the strict two-frequency description.
  The paper also supplies finite-volume truncated-space checks of form-factor
  perturbation theory in the rational-frequency model.
- **Research use:** at node 09's benchmark `xi=1/5`, `beta^2=4 pi/3` and
  `alpha=2 beta`, so `alpha^2=16 pi/3<8 pi` and
  `alpha beta=8 pi/3<4 pi`. The perturbation is relevant, strictly
  two-frequency at this order, and not another integrable sine-Gordon coupling.
- **Boundary:** the inequalities type the ultraviolet perturbation; they do not
  provide its infrared convergence radius or a continuum error bound.

## NI-04 — The required tangent is an exact reference-theory form factor

- **Source:** Sergei Lukyanov,
  [Form-factors of exponential fields in the sine-Gordon
  model](https://arxiv.org/abs/hep-th/9703190).
- **Hypotheses consumed:** the attractive sine-Gordon bootstrap, the paper's
  exponential-field normalization, and analytic continuation/crossing
  conventions.
- **Output consumed:** integral representations for soliton and breather form
  factors of `exp(i a phi)`, including one- and two-`B_1` matrix elements and
  their fusion construction.
- **Research use:** the diagonal connected values for
  `Psi=cos(2 beta phi)` are computable scalar inputs to NI-01; an odd
  exponential combination continues to test local access to `B_1`.
- **Boundary:** node 09 has reduced the nonintegrable tangent to these values but has
  not yet implemented their analytic continuation, vacuum normalization, and
  numerical quadrature. The finite regression therefore treats certified form-
  factor bounds as inputs rather than inventing a number.

## NI-05 — Beyond first order requires a separate finite-volume computation

- **Source:** Gabor Takacs,
  [Form factor perturbation theory from finite
  volume](https://arxiv.org/abs/0907.2109).
- **Hypotheses consumed:** a finite-volume regularization of the integrable
  reference basis and controlled treatment of disconnected matrix elements.
- **Output consumed:** a systematic finite-volume formulation of higher-order
  form-factor perturbation theory, tested on double sine-Gordon vacuum energy
  and breather mass corrections and compared with truncated conformal-space
  calculations.
- **Research use:** node 09 places second and higher orders in a computation node;
  they are not hidden behind `O(lambda^2)` as if the exact bootstrap survived.
- **Boundary:** the published double-sine-Gordon evaluation uses its own
  frequency and normalization choices. It supplies a method contract, not the
  missing numerical coefficient for node 09's second-harmonic benchmark.

## NI-06 — The counter-perturbation produces a new meson problem

- **Source:** Sergei B. Rutkevich,
  [Soliton confinement in the double sine-Gordon
  model](https://arxiv.org/abs/2311.07303).
- **Hypotheses consumed:** a weak `cos(beta phi/2)` deformation of sine-Gordon
  in `1+1` dimensions.
- **Output consumed:** the deformation linearly confines sine-Gordon solitons;
  neutral soliton pairs form mesons, with controlled weak-confinement mass
  expansions in several parameter regions.
- **Research use:** this confirms that failure of node 09's single-soliton fusion
  channel is a semantic reconstruction of the particle basis, not disappearance
  of all composite prediction.
- **Boundary:** the meson expansions answer a different spectral question from
  continuation of the old `B_1` pole and must be represented by a new node if
  pursued.

## Supported boundary

Together these contracts support

```text
local second harmonic
  -> nonintegrable but unconfined old soliton channel
  -> one exact-reference form factor per first mass tangent
  -> conditional positive stability budget
  -> Poincare-fixed deformed shell;

half-frequency perturbation
  -> nonzero semilocal annihilation residue
  -> old single-soliton channel invalid
  -> confined-meson reconstruction required.
```

They do not yet support an all-orders continuum construction, a numerical value
for the second-harmonic mass tangent, or transfer to `3+1` dimensions.

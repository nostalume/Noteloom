# Sine-Gordon Breather Source Contracts

These contracts support
[field--mechanics boundary](../nodes/09-field-mechanics-reduction-boundary.md). They separate exact
factorized-scattering inputs, field-access inputs, ultraviolet scale matching,
and the still-open constructive-locality boundary.

## SG-00 — The exact mass-generation control does not test binding

- **Source:** Julian Schwinger, [Gauge Invariance and Mass.
  II](https://doi.org/10.1103/PhysRev.128.2425).
- **Output consumed:** an exactly solvable `1+1`-dimensional gauge model can
  generate a nonzero particle mass without a conventional symmetry-breaking
  mass term.
- **Research use:** node 09 retains the massless Schwinger model as a semantic-
  reconstruction control but does not select it for the present test, because
  the target requires a nontrivial constituent-channel bound pole and scattering
  fusion.
- **Boundary:** this comparison does not deny the Schwinger model's composite
  interpretations; it says only that its exactly reduced free massive mode does
  not exercise the pole/fusion route selected here.

## SG-01 — The exact soliton S-matrix contains neutral bound-state poles

- **Source:** A. B. Zamolodchikov and Al. B. Zamolodchikov, [Factorized
  S-matrices in two dimensions as the exact solutions of certain relativistic
  quantum field theory models](https://doi.org/10.1016/0003-4916(79)90391-9),
  especially Section 4.
- **Hypotheses consumed:** the attractive quantum sine-Gordon model, survival of
  the integrable conservation laws, factorization, unitarity, crossing, and the
  minimal exact soliton S-matrix.
- **Output consumed:** soliton and antisoliton asymptotic particles of mass `M_s`;
  physical-strip poles associated with neutral breathers; exact masses

  ```text
  m_n=2M_s sin(n pi xi/2),  n xi<1;
  ```

  residue fusion rules defining amplitudes with breathers; and odd charge parity
  of `B_1`.
- **Research use:** node 09 reconstructs the mass formula from the pole rapidity and
  total invariant instead of importing the displayed spectrum as an unexplained
  result.
- **Boundary:** the S-matrix solution assumes the factorized-scattering framework;
  it is not a constructive proof of the local quantum field theory from the bare
  action.

## SG-02 — The neutral breather has a fermion--antifermion interpretation

- **Source:** Sidney Coleman, [Quantum sine-Gordon equation as the massive
  Thirring model](https://doi.org/10.1103/PhysRevD.11.2088).
- **Hypotheses consumed:** Coleman's field and coupling normalizations and the
  restriction to the neutral/zero-charge sector.
- **Output consumed:** the sine-Gordon soliton is identified with the massive-
  Thirring fermion, while the neutral sine-Gordon sector corresponds to the
  neutral Thirring sector.
- **Research use:** node 09 interprets a breather pole as a fermion--antifermion bound
  state without making constituent appearance the definition of the particle.
- **Boundary:** modern global-form and operator-algebra refinements of bosonization
  are not reconstructed here; the correspondence is not used as the proof of the
  breather pole or local-field access.

## SG-03 — Local exponential fields have computable particle form factors

- **Source:** Sergei Lukyanov, [Form-factors of exponential fields in the
  sine-Gordon model](https://arxiv.org/abs/hep-th/9703190).
- **Hypotheses consumed:** the sine-Gordon bootstrap spectrum, form-factor axioms,
  and the paper's normalization of local exponential fields.
- **Output consumed:** explicit integral representations for matrix elements of
  local exponential fields between the vacuum and asymptotic particle states.
- **Research use:** node 09 selects an odd local combination with nonzero `B_1`
  one-particle form factor, which supplies node 09's nonzero field-access map.
- **Boundary:** form-factor solutions provide local-operator matrix elements
  within the bootstrap framework; they do not alone prove existence of the full
  Haag--Kastler net.

## SG-04 — One ultraviolet normalization fixes the physical mass scale

- **Source:** Al. B. Zamolodchikov, [Mass scale in the sine-Gordon model and its
  reductions](https://doi.org/10.1142/S0217751X9500053X).
- **Hypotheses consumed:** the paper's perturbed-conformal-field-theory
  normalization of the cosine operator and its dimensional coupling.
- **Output consumed:** an exact relation between that ultraviolet coupling and
  the asymptotic soliton mass, plus the vacuum energy.
- **Research use:** this contract can replace node 09's physical input `M_s` when the
  ultraviolet normalization is fixed exactly. node 09 keeps `M_s` as its primary
  renormalization condition so convention-dependent constants do not enter the
  pole-to-mass construction.
- **Boundary:** the formula must not be transferred across action, normal-ordering,
  or cutoff conventions without an explicit parameter map.

## SG-05 — Bound-state poles complicate constructive locality

- **Source:** Daniela Cadamuro and Yoh Tanimoto, [Wedge-local fields in integrable
  models with bound states](https://arxiv.org/abs/1502.01313).
- **Hypotheses consumed:** scalar factorizing S-matrices with physical-strip poles
  and the operator-algebraic wedge-local construction.
- **Output consumed:** a bound-state operator can cancel pole residues and produce
  weakly commuting wedge-field candidates on a dense domain.
- **Research use:** node 09 uses this as evidence that fusion-pole data participate in
  field construction, not only in spectral naming.
- **Boundary:** self-adjointness, strong commutativity, nontrivial local
  intersections, and extension to the matrix-valued sine-Gordon S-matrix remain
  open in the cited construction. node 09 therefore does not label its bootstrap
  field-access result a complete constructive local-net theorem.

## Supported boundary

Together the contracts support

```text
exact soliton--antisoliton pole
  -> neutral breather mass and fusion channel
  -> nonzero local-field one-particle form factor
  -> stable relativistic particle within the bootstrap model.
```

They do not yet support

```text
renormalized local action
  -> complete Haag--Kastler/Wightman model
  -> independently reconstructed exact S-matrix
```

for the full sine-Gordon bound-state spectrum.

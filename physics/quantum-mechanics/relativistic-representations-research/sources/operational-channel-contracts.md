# Operational Bound/Open Channel Source Contracts

These contracts support
[visible spectral measure](../nodes/11-visible-spectral-measure.md). node 11 constructs its
finite-time event and all equalities internally; the sources delimit transfer to
physical spontaneous emission, resonances, and scattering.

## OC-01 — A two-level system coupled to a scalar field is a field model

- **Source:** Jana Reker, [Existence of Resonances for the Spin-Boson-Model with
  Critical Coupling Function](https://arxiv.org/abs/1805.02263).
- **Hypotheses consumed:** a two-level system, second-quantized scalar radiation
  field, off-diagonal linear coupling, ultraviolet control, and small coupling.
- **Output consumed:** this is a genuine field Hamiltonian with a ground-state and
  resonance problem; a resonance requires complex deformation, multiscale
  estimates, and a Feshbach--Schur construction rather than merely assigning an
  imaginary part to a second-order boundary value.
- **Research use:** node 11 chooses a simpler massive Gaussian, recoiling variant and
  stops at its complete order-`g^2` finite-time event. The source marks what would
  be required to promote that event to a finite-coupling resonance theorem.
- **Boundary:** node 11 neither imports the paper's critical infrared coupling nor its
  resonance existence result.

## OC-02 — Finite-time emission is distinct from an assumed exponential law

- **Source:** V. Debierre, T. Durt, A. Nicolet, and F. Zolla, [Spontaneous light
  emission by atomic Hydrogen: Fermi's golden rule without
  cheating](https://arxiv.org/abs/1502.06404).
- **Hypotheses consumed:** an initially excited atomic state, vacuum radiation,
  first-order transition amplitudes, a declared atom--field coupling function,
  and explicit finite-time survival evaluation.
- **Output consumed:** finite-time emitted-field probability can be calculated
  before imposing a golden-rule or exponential approximation; cutoff and exact
  coupling choices are part of the prediction.
- **Research use:** node 11 derives the corresponding scalar-field event from its own
  Dyson coefficient and checks its boundary-rate limit without importing the
  hydrogen dipole formula.
- **Boundary:** the source's numerical accuracy statement is specific to hydrogen
  and is not transferred to node 11.

## OC-03 — A scattering matrix requires asymptotic channel constructions

- **Source:** Miguel Ballesteros, Dirk-André Deckert, and Felix Hänle, [Relation
  between the Resonance and the Scattering Matrix in the massless Spin-Boson
  Model](https://arxiv.org/abs/1801.04843).
- **Hypotheses consumed:** a two-level system coupled to a second-quantized scalar
  field, ultraviolet cutoff, controlled infrared behavior, asymptotic creation
  operators, and scattering-state constructions.
- **Output consumed:** relating resonance data to an actual scattering kernel is
  an additional theorem with incoming/outgoing states and normalization; a
  self-energy boundary alone is not that kernel.
- **Research use:** node 11 calls its detected one-boson probability an operational
  open-channel observable but refuses to rename it an `S`-matrix element.
- **Boundary:** node 11 is massive, fixed-order, and finite-time. It does not consume
  the paper's massless scattering theorem.

## Supported boundary

The sources support the model class and the distinction among finite-time
transition probability, resonance, and scattering. node 11's operator-valued measure,
probability-conservation witness, memory identity, and regression are internally
constructed. Exponential decay at kinetic times, complex poles, and an `S` matrix
remain separate re-entry problems.

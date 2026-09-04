# Field/Mechanics Variation Source Contracts

These contracts support [field--mechanics boundary](../nodes/09-field-mechanics-reduction-boundary.md). They
separate exact sector algebra, field-theoretic realization, and the heavy-source
approximation. None of the sources by itself derives a cutoff-independent QED
Hamiltonian or makes its atomic spectrum easy.

## FM-01 — Exact sector elimination and recovery

- **Sources:** M. Griesemer and D. Hasler, [On the Smooth Feshbach--Schur
  Map](https://arxiv.org/abs/0704.3244); Genevieve Dusson, Israel Sigal, and
  Benjamin Stamm, [The Feshbach--Schur map and perturbation
  theory](https://arxiv.org/abs/2105.02058), Theorem 1.2 and equations
  (1.10)--(1.16).
- **Hypotheses consumed:** complementary projections `P,Q`; a closed operator;
  invertibility of the `Q`-block at the spectral parameter; boundedness/domain
  compatibility of the Schur expression.
- **Output consumed:** the Feshbach operator is isospectral in the declared
  window, and the full eigenvector is reconstructed from its `P` component.
  The later paper also gives explicit discrete-spectrum perturbation bounds
  under relative-form and gap hypotheses.
- **Research use:** node 09 derives the elementary projected-resolvent and recovery
  identities on one typed vector, then uses this theorem contract only for the
  unbounded-operator hypotheses and quantitative perturbation boundary.
- **Boundary:** the eliminated resolvent may be as hard as the original problem.
  At a `Q`-sector threshold an ordinary inverse must be replaced by controlled
  boundary values or a resonance construction.

## FM-02 — A field Green object can produce an equal-time mechanical equation

- **Source:** Edit Matyus, David Ferenc, Peter Jeszenszki, and Adam Margocsy,
  [The Bethe--Salpeter QED wave equation for bound-state computations of atoms
  and molecules](https://arxiv.org/abs/2211.02389), Sections II.4--II.5 and III.
- **Output consumed:** an exact equal-time form can be obtained from the
  space-time Bethe--Salpeter equation; its mechanical equation is nonlinear in
  the energy through a residual kernel. Retaining the instantaneous positive-
  energy part produces a no-pair Dirac--Coulomb(--Breit) reference, while the
  relative-energy, transverse, retardation, pair, and crossed-photon content
  remains in an energy-dependent correction.
- **Research use:** this validates the *shape* of node 09's field/mechanics bridge:
  an instantaneous mechanical representative plus an energy-dependent field
  self-energy, both observed through the same projected Green object.
- **Boundary:** this review does not supply a nonperturbative error bound for the
  one-electron Dirac--Coulomb limit used in node 09. Kernel truncation, gauge
  consistency, renormalization, and numerical recovery remain separate work.

## FM-03 — A compact charged source contributes effective data, not a universal

point boundary condition

- **Source:** C. P. Burgess, Peter Hayman, Markus Rummel, and Laszlo Zalavari,
  [Point-Particle Effective Field Theory III: Relativistic Fermions and the
  Dirac Equation](https://arxiv.org/abs/1706.01063), Sections 2--4, especially
  equations (10), (24)--(30), and the bound-state discussion.
- **Output consumed:** a sufficiently heavy compact source admits a first-
  quantized effective description; Gauss flux fixes its long-range Coulomb
  field, while finite size and other short-distance physics enter running
  near-source couplings/boundary data. The standard point-source condition is a
  limit, not an input valid for every source.
- **Research use:** node 09 treats charge distribution, heavy-source preparation,
  and short-distance data as coordinates of the admissible model family rather
  than hiding them inside one `-nu/r` formula.
- **Boundary:** the paper computes within a spherical short-distance expansion
  and uses radial solutions for applications. node 09 consumes only the source-to-
  effective-data contract; it does not import the component calculation as its
  reduction principle.

## FM-04 — General charge distributions require a domain theorem

- **Source:** Maria J. Esteban, Mathieu Lewin, and Eric Sere,
  [Dirac--Coulomb operators with general charge distribution. I. Distinguished
  extension and min--max formulas](https://arxiv.org/abs/2003.04004).
- **Output consumed:** for the source's stated class of positive charge measures
  and coupling bounds, the electrostatic Dirac operator has a distinguished
  self-adjoint realization and its gap eigenvalues admit min--max
  characterizations.
- **Research use:** this is the domain/stability theorem contract for the
  finite-source mechanical representatives in node 09.
- **Boundary:** norm-resolvent continuity for every singular source variation is
  not inferred. node 09's explicit contour estimate is supported first for bounded
  effective-kernel variation; singular point limits need a separate form- or
  resolvent-convergence theorem.

## Supported boundary

The contracts support an exact algebraic projection once a field Hamiltonian and
admissible sector are supplied, and they support physically motivated
instantaneous/heavy-source mechanical representatives. They do **not** yet
construct a common cutoff-independent relativistic QED Hamiltonian, prove the
heavy-source limit in operator topology, or bound the full radiative correction
to a Dirac--Coulomb gap projector. Those are explicit downstream obligations.

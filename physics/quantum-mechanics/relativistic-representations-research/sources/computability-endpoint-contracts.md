# Propagator and Bound-State Computability Contracts

Recorded: 2026-08-29  
Used by: [computability endpoint audit](../results/05-computability-endpoint-audit.md)
and [N4o Dirac--Coulomb local graph](../nodes/04o-dirac-coulomb-local-graph.md)

## CE-01 — Boundary-selected free Green objects

- **Sources:** Christian Baer, [Green-hyperbolic operators on globally hyperbolic
  spacetimes](https://arxiv.org/abs/1310.0738), *Communications in Mathematical
  Physics* 333 (2015), 1585--1615; the finite-spin Green contracts already bound
  to N4e/N4f/N4i.
- **Output consumed:** normally hyperbolic operators have unique retarded and
  advanced Green maps with causal support and exact sequences.
- **Internal extension:** once any scalar distribution `g_b` satisfying
  `q g_b=1` and a declared prescription `b` has been constructed, the invariant
  finite-spin identities lift it to an admissible-source response. This includes
  retarded/advanced maps and conditionally includes a Feynman boundary value.
- **Boundary:** existence of the causal maps does not select a Feynman state,
  Euclidean continuation, or renormalized interacting propagator.

## CE-02 — Self-adjoint Dirac--Coulomb operator and gap eigenvalues

- **Sources:** Jean Dolbeault, Maria J. Esteban, and Eric Sere,
  [Distinguished self-adjoint extension and eigenvalues of operators with gaps.
  Application to Dirac--Coulomb operators](https://arxiv.org/abs/2206.11679);
  Maria J. Esteban, Mathieu Lewin, and Eric Sere,
  [Dirac--Coulomb operators with general charge distribution. I. Distinguished
  extension and min--max formulas](https://arxiv.org/abs/2003.04004).
- **Output consumed:** a Dirac--Coulomb-type symmetric operator requires a
  distinguished self-adjoint extension; under the stated hypotheses its
  eigenvalues in the spectral gap admit a min--max characterization. For a charge
  distribution with no atom of weight greater than or equal to one, the second
  source constructs the unique distinguished extension.
- **Research use:** N4o takes `0<=nu<1`, types the target as the projection-valued
  gap spectral measure of one declared closed operator, and uses the min--max
  theorem only as a candidate computational edge. The theorem does not construct
  N4o's carrier, connection or rotation reduction.
- **Boundary:** the theorem does not derive the Coulomb coupling from Poincare
  symmetry and does not construct the conserved algebra or whatever residual
  spectral computation remains after algebraic extraction.

## CE-03 — Exact Coulomb spectrum as a terminal check

- **Source:** Matteo Gallone and Alessandro Michelangeli, [Discrete spectra for
  critical Dirac--Coulomb Hamiltonians](https://arxiv.org/abs/1710.11389).
- **Output consumed:** self-adjoint realization matters to the discrete spectrum;
  the distinguished realization recovers the Sommerfeld formula, while other
  extensions can have different discrete spectra.
- **Research use:** the exact Coulomb levels are a terminal check for an
  algebra/Schur/residual spectral algorithm, not permission to skip its operator
  domain.
- **Boundary:** the closed formula is special to the Coulomb potential and should
  not be presented as the universal meaning of a bound-state computation.

## CE-04 — Angular Dirac spectrum and half-line reduction

- **Sources:** Jan Derezinski and Blazej Ruba, [Holomorphic family of
  Dirac--Coulomb Hamiltonians in arbitrary
  dimension](https://arxiv.org/abs/2107.03785); A. A. Abrikosov Jr., [Dirac
  operator on the Riemann sphere](https://arxiv.org/abs/hep-th/0212134).
- **Output consumed:** spherically symmetric Dirac--Coulomb operators separate
  into closed half-line Dirac operators related to the sphere Dirac eigenproblem;
  the unit-sphere Dirac spectrum is the nonzero integers, with total spin
  `j=|kappa|-1/2`.
- **Research use:** N4p constructs the angular operator from the inherited orbital,
  spin and total Casimirs, evaluates both eigenvalue branches internally, and uses
  these sources only for the spinor Gauss/polar theorem, completeness, and the
  closed-realization boundary. Its later audit classifies the result as exact block
  equivalence rather than a new computational reduction.
- **Boundary:** neither source makes the angular reduction an energy computation.
  The singular half-line domain and spectral measure must still be constructed or
  evaluated in each channel.

## Supported boundary

The sources support causal scalar Green maps and the operator-theoretic typing of
Dirac--Coulomb gap eigenvalues. The invariant lift to every separate finite
symmetric massless potential is internal to the research graph. N4o now constructs
the separate massive Dirac carrier, external connection, curvature obstruction,
static Hilbert space and manifest-rotation reduction internally. N4p further
constructs the angular Dirac split and exact half-line spectral-measure recovery,
then exposes its residual `M_2(C)` fiber and radial-coordinate dependence. The
sources type the distinguished extension, polar theorem and terminal spectrum
check. N4r now contains an exact pre-radial
field/mechanics projected-resolvent relation, field-state recovery, and a bounded
variation estimate for prepared gap projectors; its renormalized field
realization, singular heavy-source limit, evaluated self-energy, computed channel
measures, positive-cost spectral computation, and dynamical field-theoretic
prediction remain open.

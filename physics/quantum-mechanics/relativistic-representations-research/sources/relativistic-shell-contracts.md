# Relativistic Mass-Shell Source Contracts

These contracts support [N4v](../nodes/04v-relativistic-mass-shell.md). They
bound the two irreducible external steps: classification of a massive Poincare
orbit and the conditions under which a sharp interacting spectral component is
a scattering particle. N4v constructs the shell equation, Hessian, mass
coincidence, and nonrelativistic recovery internally.

## RS-01 — A positive massive Poincare orbit is generated from a rest momentum

- **Source:** Xavier Bekaert and Nicolas Boulanger, [The unitary
  representations of the Poincare group in any spacetime
  dimension](https://arxiv.org/abs/hep-th/0611263), especially the induced-
  representation and massive-orbit discussion.
- **Hypotheses consumed:** a strongly continuous positive-energy unitary
  representation of the Poincare group; restriction to one irreducible massive
  orbit with nonnegative mass squared.
- **Output consumed:** the translation spectrum of a massive irreducible sector
  is the Lorentz orbit of a timelike standard momentum; its residual group
  supplies the spin fiber.
- **Research use:** N2 already constructs the orbit and stabilizer internally.
  N4v reuses only this classification boundary when identifying an interacting
  stable spectral component with one such orbit.
- **Boundary:** representation classification does not prove that a given
  interacting field theory contains the orbit or determine the mass value.

## RS-02 — A sharp massive spectral component needs dynamical stability

- **Sources:** Detlev Buchholz and Wojciech Dybalski, [Scattering in
  relativistic quantum field theory: basic concepts, tools, and
  results](https://arxiv.org/abs/math-ph/0509047), Sections 1--3; Wojciech
  Dybalski, [Haag--Ruelle scattering theory in presence of massless
  particles](https://arxiv.org/abs/hep-th/0412226), Theorem 1.1.
- **Hypotheses consumed:** local relativistic field dynamics, positive energy,
  invariant vacuum, a sharp massive one-particle spectral subspace, nonzero
  interpolating overlap, and the stated mass-gap or Herbst-type regularity
  conditions.
- **Output consumed:** the sharp subspace supports covariant asymptotic
  one-particle states; under the stronger regularity theorem, a neutral massive
  particle may remain a sharp scattering species in the presence of massless
  excitations.
- **Research use:** N4v treats sharpness, access, and stability as inputs before
  applying orbit kinematics to a composite rest pole.
- **Boundary:** neither theorem locates the composite pole, proves the required
  regularity in relativistic QED, determines its mass, or proves asymptotic
  completeness.

## Supported boundary

The sources license a conditional bridge:

```text
sharp stable interacting spectral component
  + one massive Poincare orbit
  -> relativistic one-particle shell.
```

They do not license the converse claim that a mechanically computed bound level
automatically produces a relativistic particle. N4r's rest pole, N4s's field
access and stability, and N4v's orbit closure are separate obligations.

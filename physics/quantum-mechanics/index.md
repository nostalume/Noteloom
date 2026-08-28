# Quantum Mechanics

Quantum mechanics is a framework for assigning amplitudes to alternatives and
probabilities to measurement outcomes. Its unfamiliarity is concentrated in a
small set of structural rules: states form rays in a complex Hilbert space,
observables are represented by self-adjoint operators, isolated systems evolve
unitarily, and composite systems use tensor products.

This note assumes classical mechanics, waves, complex linear algebra, and basic
differential equations. It covers nonrelativistic quantum mechanics; quantum
field theory is outside its scope.

## States and amplitudes

A pure state is represented by a normalized vector \(|\psi\rangle\) in a
Hilbert space \(\mathcal H\):

\[
\langle\psi|\psi\rangle=1.
\]

Vectors that differ only by an overall nonzero phase represent the same physical
state. If \(\{|a_n\rangle\}\) is an orthonormal basis, then

\[
|\psi\rangle=\sum_n c_n|a_n\rangle,
\qquad
\sum_n|c_n|^2=1.
\]

The coefficients are amplitudes, not ordinary probabilities. Interference
occurs because amplitudes add before their squared magnitudes are taken.

## Observables and measurement

An observable \(A\) is represented by a self-adjoint operator \(\hat A\). In a
discrete nondegenerate example,

\[
\hat A|a_n\rangle=a_n|a_n\rangle.
\]

Measuring \(A\) in state \(|\psi\rangle\) returns \(a_n\) with probability

\[
P(a_n)=|\langle a_n|\psi\rangle|^2.
\]

The expectation value

\[
\langle A\rangle=\langle\psi|\hat A|\psi\rangle
\]

is an ensemble average, not generally the result of one trial. Degeneracy and
continuous spectra require projectors or spectral measures, but the same rule
survives: probabilities are squared norms of projected amplitudes.

## Time evolution

For an isolated system, the state obeys the Schrödinger equation

\[
i\hbar\frac{d}{dt}|\psi(t)\rangle=\hat H(t)|\psi(t)\rangle.
\]

A self-adjoint Hamiltonian generates unitary evolution, which preserves inner
products and therefore total probability. If \(\hat H\) is time independent,

\[
|\psi(t)\rangle=e^{-i\hat Ht/\hbar}|\psi(0)\rangle.
\]

An energy eigenstate gains only a phase. A superposition of different energies
develops relative phases, and those relative phases drive observable dynamics.

## Position representation

For one particle on a line, the abstract state is represented by
\(\psi(x,t)=\langle x|\psi(t)\rangle\). With

\[
\hat H=-\frac{\hbar^2}{2m}\frac{d^2}{dx^2}+V(x,t),
\]

the Schrödinger equation becomes

\[
i\hbar\frac{\partial\psi}{\partial t}
=-\frac{\hbar^2}{2m}\frac{\partial^2\psi}{\partial x^2}
+V\psi.
\]

The density \(|\psi|^2\) and current

\[
j=\frac{\hbar}{m}\operatorname{Im}
\left(\psi^*\frac{\partial\psi}{\partial x}\right)
\]

satisfy a continuity equation. Normalization is therefore preserved when the
Hamiltonian and boundary conditions make the probability flux well defined.

## Stationary states organize bound problems

For time-independent \(V\), separate variables with
\(\psi(x,t)=\phi(x)e^{-iEt/\hbar}\). The spatial function satisfies

\[
\hat H\phi=E\phi.
\]

This is a boundary-value and spectral problem. Normalizability and boundary
conditions select the allowed states; discreteness is a consequence of the
operator and domain, not a universal assumption that every observable has a
discrete spectrum.

The infinite well, harmonic oscillator, and finite barriers are useful because
each isolates a different idea: boundary quantization, ladder structure, and
tunneling. They should be studied as models of the framework rather than as a
list of special solutions.

## Commutators and uncertainty

For two operators,

\[
[\hat A,\hat B]=\hat A\hat B-\hat B\hat A.
\]

In the position representation,

\[
[\hat x,\hat p]=i\hbar,
\qquad
\hat p=-i\hbar\frac{d}{dx}.
\]

The Robertson relation

\[
\Delta A\,\Delta B
\geq\frac12\left|\langle[\hat A,\hat B]\rangle\right|
\]

describes the statistical spread of two observables in one state. It is not, by
itself, a claim about disturbance caused by a particular measuring instrument.

## Spin and composite systems

Spin shows that a quantum degree of freedom need not arise from a particle moving
through ordinary space. A spin-\(1/2\) state lives in \(\mathbb C^2\), and its
components depend on the chosen measurement axis.

For systems with Hilbert spaces \(\mathcal H_A\) and \(\mathcal H_B\), the joint
space is

\[
\mathcal H_{AB}=\mathcal H_A\otimes\mathcal H_B.
\]

Not every vector in this space factors into one state for \(A\) and one for
\(B\). The nonfactorizable states are entangled; their correlations cannot be
encoded by assigning an independent pure state to each subsystem.

## Approximation is part of the theory's use

Exactly solvable Hamiltonians are rare. The main controlled tools are
time-independent perturbation theory, time-dependent perturbation theory, and
the variational method. Every approximation should state its small parameter or
trial space and should be checked against normalization, symmetry, dimensions,
and a solvable limit.

The print companion [notes.typ](notes.typ) develops operators, spin, standard
one-dimensional models, and perturbation theory.

## Advanced manuscripts

- [Symmetry and quantum fields](symmetry-and-quantum-fields.typ) develops group
  actions, moment maps, Lie and Clifford representations, angular momentum,
  path integrals, and field-theory structures.
- [Relativistic representations](relativistic-representations.typ) studies
  Poincare and Lorentz representations and their associated wave equations.

## References and next steps

- Barton Zwiebach, [MIT 8.04 Quantum Physics I lecture notes](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/pages/lecture-notes/).
- David Tong, [Quantum Mechanics](https://www.damtp.cam.ac.uk/user/tong/qm/qmhtml/S1.html) and [the formalism of quantum mechanics](https://www.damtp.cam.ac.uk/user/tong/qm/qmhtml/S3.html).

The next coherent extension is density operators and open systems, followed by
angular momentum addition and scattering. The advanced manuscripts should be
edited against stable special-relativity and representation-theory foundations
without discarding their existing derivations.

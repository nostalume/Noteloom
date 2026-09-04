# Determination boundary

Status: supported kinematic boundary; dynamics remains supplied

## Question

What can a unitary Poincare representation determine before a field equation,
action, Hamiltonian, state, preparation, or observable is supplied?

## Construction

Let `G = R^(1,3) semidirect L` and let `U` be a strongly continuous unitary
representation. Translation covariance gives commuting self-adjoint generators
`P_mu` through the one-parameter groups

```text
U(t e_mu) U(s e_mu) = U((t+s)e_mu),
U(t e_mu) = exp(i t P_mu).
```

Because translations commute, their joint spectral measure `E` constructs

```text
U(a) = integral exp(i <a,p>) dE(p).
```

Lorentz covariance transports the spectrum:

```text
U(A) U(a) U(A)^(-1) = U(Lambda(A)a)
=> U(A) E(Delta) U(A)^(-1) = E(Lambda(A)Delta).
```

An irreducible positive-energy sector therefore selects one Lorentz orbit and one
unitary stabilizer representation. That pair is the physical representation datum.

## Determined and supplied objects

The datum determines orbit, mass/sign sector, spin or helicity fiber, and induced
Poincare action up to unitary equivalence. It constrains admissible finite carriers
and equivariant local operators.

It does not determine a carrier presentation, gauge redundancy, differential
order, action normalization, interaction, quantum state, detector, boundary
condition, or approximation. These require explicit additional inputs.

## Output and edges

Output: `(orbit, little-group fiber, induced unitary action)`.

- [Representation spaces](02-representation-spaces.md) separates this output from
  coefficient and field realizations.
- [Spin, helicity, and carriers](03-spin-helicity-carriers.md) constructs the two
  stabilizer types and possible finite carriers.

## Checks and boundary

The spectral covariance equation is the decisive equality witness. The boundary
fails for reducible sectors unless the spectral decomposition is retained, and it
does not infer dynamics from symmetry alone.

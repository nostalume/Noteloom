# Variable spin-texture PDE: a mode-bundle transfer

## Purpose

This is the first variable-coefficient transfer candidate of the PDE machine.  It asks
whether a spatially varying two-level spinor Hamiltonian can be reduced without
choosing spin components at every point.  The target observable is leakage from
one local spin band over a finite time.

This model tests variable internal spin direction.  It is not yet the full
slowly varying orbital Landau problem; the obstruction to making that
identification is recorded in Section 8.

## 1. Input and admission condition

On a Euclidean region (or a compact flat manifold without boundary), take

```text
H_epsilon = -epsilon^2 Delta I - mu B(x).sigma,        mu>0,          (1)
```

on the spinor core `C_c^infinity(X,C^2)`.  Assume `B` is `C^2` and

```text
|B(x)| >= B_0 > 0.                                                    (2)
```

Define `n=B/|B|`.  The two eigenvalues of the internal operator are
`E_s=-s mu|B|`, `s=+1,-1`, and their gap is at least `2 mu B_0`.
Therefore the PDE itself constructs the rank-one projectors

```text
P_s(x) = (I+s n(x).sigma)/2.                                         (3)
```

No Euler angles, local spinors, or predetermined rotation group decomposition is
needed to obtain (3).

## 2. Exact local projection calculus

The mode line bundle is `E_s=Ran(P_s)`.  Its intrinsic connection, curvature,
and transition arrow are

```text
nabla^s = P_s d,
F_s     = P_s(dP_s wedge dP_s)P_s,
K_s     = P_(-s)dP_s P_s.                                            (4)
```

`K_s` is the variable replacement for a fixed spin raising/lowering operator: it
maps a derivative of the `s` mode into the opposite mode.  Since

```text
dP_s = (s/2) dn.sigma,                                                (5)
```

its magnitude is controlled directly by the rate at which the physical field
direction turns.

If a local normalized eigenspinor `u_s` is introduced only for presentation,
`nabla^s` becomes a Berry `U(1)` connection.  On overlaps, phases of `u_s`
change, while all projector expressions in (4) remain invariant.  If `n` has
nonzero degree over a closed surface, the eigenline may be nontrivial and no
single global eigenspinor exists; (3)--(4) still do.

## 3. Projected PDE without spin components

For a section of `E_s`, direct projection of the kinetic operator gives

```text
P_s H_epsilon P_s
 = epsilon^2 (nabla^s)^*nabla^s
   - s mu|B| + epsilon^2 Phi_s,                                      (6)
```

where the geometric potential is

```text
Phi_s P_s
 = sum_j P_s(partial_j P_s)(partial_j P_s)P_s
 = (1/4)|nabla n|^2 P_s.                                             (7)
```

Thus the first reduced PDE is not obtained by replacing `sigma.B` by one
eigenvalue.  It also retains the induced connection and the positive
Born--Huang/geometric potential forced by the moving subspace.

Equations (3), (6), and (7) are the human-size representation: one unit vector
field generates the projectors, connection, curvature, potential, and both
channels.

## 4. Exact off-diagonal residual

The internal potential commutes with `P_s`.  Product differentiation therefore
gives the exact defect

```text
[H_epsilon,P_s] psi
 = -epsilon^2[(Delta P_s)psi
              +2 sum_j (partial_j P_s)(partial_j psi)].              (8)
```

This is the first mode-conversion operator; it vanishes precisely for constant
field direction.  On a momentum-limited sector satisfying

```text
||epsilon nabla psi|| <= K ||psi||,                                  (9)
```

(5) and (8) yield, with the gradient norm understood as the corresponding
row-operator norm,

```text
||[H_epsilon,P_s]psi||
 <= [epsilon K ||nabla n||_infinity
     +(epsilon^2/2)||Delta n||_infinity] ||psi||.                    (10)
```

The two dimensionless failure scales are therefore

```text
eta_gap  ~ epsilon K ||nabla n||/(mu B_0),
eta_bend ~ epsilon^2 ||Delta n||/(mu B_0).                           (11)
```

Slow variation has operational meaning only when these are small relative to the
gap.  Equation (10), not the phrase “adiabatic,” is the computational certificate.

## 5. Observable recovery

Let the preparation lie in `Ran(P_s)` and remain in the sector (9).  Comparing
the full propagator with its block-diagonal part by Duhamel gives the finite-time
leakage contract

```text
||(I-P_s) exp(-itH_epsilon) P_s psi||
 <= |t| [epsilon K ||nabla n||_infinity
          +(epsilon^2/2)||Delta n||_infinity] ||psi||,               (12)
```

provided the energy-localized commutator and domain invariance needed for the
unbounded operator comparison hold.  Equation (12) names the same observable on
both sides: probability amplitude outside the prepared mode.  It is a first-
projector estimate, not an all-orders adiabatic theorem.

A superadiabatic projector from the
[mode-bundle calculus](../nodes/adiabatic-mode-bundle-calculus.md) can reduce the
residual order when additional smoothness and symbol hypotheses are certified.

## 6. What became of the group and ladder?

At each point, the Pauli relations provide the local two-dimensional Clifford
module, and `P_+ + P_-=I` decomposes it.  But a varying `n(x)` destroys a single
global generator `sigma_3` commuting with the PDE.  The surviving objects are

```text
diagonal connection:  P_s dP_s,
up/down transition:   P_(-s)dP_s P_s and its adjoint,
curvature/holonomy:   P_s(dP_s wedge dP_s)P_s.                        (13)
```

Their coefficients vary over the base, so their natural closure is a bundle of
operator arrows (a connection algebra/algebroid), not a finite Lie algebra with
constant structure constants.  When `n` is constant, (13) vanishes and the fixed
spin decomposition of the uniform bench is recovered.  Ordinary fixed-generator
closure is therefore a special constant-projector limit of the broader bilateral
machine.

## 7. Transfer verdict

Passed at the differential-construction level:

- the PDE coefficients construct their own spin projectors and mode bundle;
- the reduced operator retains connection and geometric potential without a
  component expansion;
- the failure of exact decomposition is an explicit differential operator;
- a momentum-window bound converts that residual into a conditional finite-time
  leakage certificate;
- nontrivial topology is represented without inventing a global eigenbasis.

Not yet passed:

- invariance of the stated momentum sector under the comparison dynamics, or an
  alternative energy-localized theorem closing the analytic contract in (12);
- an all-orders superadiabatic construction on this bench;
- long-time control beyond the scale allowed by (12);
- boundaries, zeros of `B`, non-self-adjoint terms, or band crossings;
- a same-observable cost comparison with a numerical spinor propagation.

If `B=0` somewhere, the gap closes and the correct result is
`CrossingObstruction`, or a coupled two-mode PDE.  The machine must not continue
with (6) as a scalar band equation.

## 8. Why this is not yet the variable orbital Landau problem

For a three-dimensional Pauli operator with orbital magnetic curvature, the
uniform transverse Landau levels have guiding-center degeneracy, while the free
longitudinal kinetic energy makes their full spectral ranges overlap.  Hence an
ordinary global spectral projection of the complete Hamiltonian does not isolate
one Landau channel.  A local phase-space band may still be isolated at fixed slow
variables and longitudinal momentum, but then the construction requires magnetic
Weyl/space-adiabatic calculus and a careful fast--slow split.

With a varying field direction, the transverse planes also fail to form one
fixed product foliation.  Field-line curvature and derivatives of the local
Landau projectors become additional transition terms.  These are substantive
geometric data, not coordinate nuisances.

The next orbital-field transfer must therefore specify an energy/phase-space
window, retain guiding-center multiplicity, construct the magnetic projector
symbol, and bound its commutator with the full Pauli operator.  Importing the
scalar two-level calculation above as if it solved those obligations would be a
category error.

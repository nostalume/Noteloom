# Coulomb PDE to hidden `so(4)`: a full-route inverse benchmark

## 1. Question, invariant, and horizon

This bench asks whether the inverse machine can start without a hidden group and
construct enough representation structure to compute the same physical output as
separation of variables.

```text
Input:  H = p^2/(2 mu)-kappa/r on L^2(R^3),  p=-i hbar grad,
        kappa>0, negative-energy bound sector, standard Coulomb realization.
Output: all bound energies E_n and their degeneracies.
Invariant: the spectral projector multiplicity at each E_n.
Baseline: spherical separation plus a parameterized radial quantization.
```

Wavefunction reconstruction, scattering, relativistic corrections, external
fields, and classification of arbitrary potentials are outside the horizon.

## 2. What is and is not supplied

Supplied: Euclidean metric, canonical symplectic/commutator structure, the scalar
potential `V(r)=-kappa/r`, rotation covariance visible in the coefficients, and
the physical domain theorem contract.

Not supplied: `SO(4)`, the Runge--Lenz operator, spherical coordinates, hydrogenic
special functions, or energy/degeneracy formulas.

The metric-generated candidate construction is complete for scalar,
time-reversal-even symbols of momentum degree at most two in the declared radial
coefficient algebra. It does not prove that the displayed operators are the full
unbounded differential centralizer of `H`, nor does it cover spin or higher order.

## 3. Canonical seed: rotations

The principal symbol

```text
h(x,p)=p^2/(2 mu)+V(r),       r=|x|                         (1)
```

is rotation invariant.  The moment map therefore constructs

```text
L=x cross p,                 {h,L_i}=0.                    (2)
```

This is a canonical seed, not an ansatz.  It gives `so(3)` but only explains the
`2 ell+1` magnetic multiplicity; it does not yet explain degeneracy across
different `ell` or compute the energy.

## 4. Complete-module selection and its human compression

The six Euclidean Killing fields `P_i,R_i` generate 21 symmetric products. Exact
tensor reduction discovers the one relation `sum_i P_i symmetric-product R_i=0`,
so the metric supplies a 20-dimensional rank-two Killing module before `V` is
read. The compatibility map

```text
K -> d(K dV)                                               (3a)
```

then selects a ten-dimensional Coulomb kernel: `H`, the six symmetric products
of rotations, and three additional vector components. The lower-order equation
`dW=K dV` reconstructs their `-kappa x_i/r` terms. On the control
`V=-kappa/r+r^2`, the same module returns only the seven visible directions
`H+Sym^2<R_i>`.

The following invariant argument is the human compression of why the three new
kernel directions exist; it is no longer the candidate generator. Write the
generated rotation-covariant, time-reversal-even vector as

To test for the smallest new object that can mix angular sectors, select one
rotation-covariant, time-reversal-even vector of momentum degree two.  Modulo the
existing scalar invariants, its minimal intrinsic form is

```text
a = (p cross L)/mu-F(r) r_hat.                            (3)
```

Hamilton's equations give, with `p_perp=p-p_r r_hat`,

```text
d/dt [(p cross L)/mu] = [r V'(r)/mu] p_perp,
d/dt [F(r) r_hat]     = [F'(r)p_r/mu] r_hat
                         +[F(r)/(mu r)]p_perp.             (4)
```

The two invariant directions must vanish separately:

```text
F'(r)=0,                 r V'(r)-F(r)/r=0.                (5)
```

Thus this module lifts precisely when

```text
(r^2 V'(r))'=0,
V(r)=-kappa/r+constant,  F=kappa.                         (6)
```

For the supplied Coulomb coefficient, (6) constructs rather than presupposes the
classical Runge--Lenz symbol

```text
a=(p cross L)/mu-kappa r_hat.                             (7)
```

For a generic central potential the first obstruction is the nonzero scalar
`(r^2V')'`.  This is a short refusal certificate inside the declared covariance
module.

## 5. Quantum lift and its honest boundary

Hermitian lifting of (7) gives

```text
A = (p cross L-L cross p)/(2 mu)-kappa r_hat.             (8)
```

On the common invariant core of smooth functions supported away from the Coulomb
singularity, canonical commutator reduction yields

```text
[H,L_i]=0,                  [H,A_i]=0,
[L_i,L_j]=i hbar eps_ijk L_k,
[L_i,A_j]=i hbar eps_ijk A_k,
[A_i,A_j]=-(2 i hbar/mu) H eps_ijk L_k,                  (9)
L dot A=A dot L=0,
A^2=kappa^2+(2H/mu)(L^2+hbar^2).                        (10)
```

The `hbar^2` in (10) is a genuine lower-order quantum correction. In units
`mu=hbar=1`, [`coulomb_e3_closure.py`](../computation/coulomb_e3_closure.py)
consumes the complete generated kernel and verifies (9)--(10) by exact
differential-operator composition for positive rational `kappa`. The classical
Poisson relations are independently replayed by
[`coulomb_symbolic.py`](../computation/coulomb_symbolic.py); that script is not
misreported as a quantum proof. Essential self-adjointness, preservation of the
chosen realization, and bound-state completeness remain analytic inputs.

## 6. Energy-shell closure constructs the algebra

Restrict (9) to a negative-energy eigenspace `H=E<0` and define

```text
M=sqrt(mu/(-2E)) A,          J_+=(L+M)/2,
                              J_-=(L-M)/2.               (11)
```

Direct substitution, rather than a group name, gives

```text
[J_+i,J_+j]=i hbar eps_ijk J_+k,
[J_-i,J_-j]=i hbar eps_ijk J_-k,
[J_+i,J_-j]=0.                                           (12)
```

Hence the represented Lie algebra on this shell is
`su(2) direct-sum su(2)`, with effective compact group locally `SO(4)` (or its
spin cover before the kernel is fixed).  Notice the energy dependence: the compact
real form is a sectorwise output.  The positive-energy sector has a different real
form and is not silently included.

## 7. Casimir arithmetic produces spectrum and degeneracy

Orthogonality in (10) implies `J_+^2=J_-^2`; write the two spins as the same `j`.
The second identity in (10) gives

```text
L^2+M^2 = -mu kappa^2/(2E)-hbar^2
          = 4 hbar^2 j(j+1).                            (13)
```

Therefore

```text
-mu kappa^2/(2E)=hbar^2(2j+1)^2.
```

With `n=2j+1=1,2,...`, the machine returns

```text
E_n = -mu kappa^2/(2 hbar^2 n^2),
mult(E_n)=(2j+1)^2=n^2.                                 (14)
```

No radial differential equation, termination of a hypergeometric series, or sum
over `ell=0,...,n-1` is used in (13)--(14).  The representation decomposition
computes exactly the requested energy and total degeneracy, not the coordinate
eigenfunctions.

## 8. Bilateral round trip

The inverse half is

```text
Coulomb coefficients
 -> metric Killing algebra and 21-to-20 module quotient
 -> compatibility kernel <H,Sym^2(L),A>
 -> reconstructed lower terms and exact Hermitian lift
 -> energy-shell su(2)+su(2)
 -> equal-spin irreducible
 -> E_n and n^2.                                         (15)
```

The forward half starts with the represented algebra, selects the enveloping
relations (9)--(10), realizes `L,A` by (8), and recovers the same `H` on the common
core.  The round trip determines the effective represented algebra and Coulomb
scale; it does not distinguish global covers from the differential action alone.

## 9. Whole-route complexity audit

The two valid routes are compared only for bound energies and degeneracies:

| Stage | Spherical/radial baseline | Centralizer/representation route | Verdict |
| --- | --- | --- | --- |
| discover | choose rotation-adapted coordinates and separated labels | quotient the metric-generated `21` presentations to `20`; compute one compatibility kernel | complete in the declared order-two class |
| construct/lift | derive angular and radial operators | rank `20 -> 10`; solve `dW=K dV`; exact divergence lift | finite exact construction |
| close/decompose | organize the `ell,m` sectors and their admissible ranges | six generators, relations (9), two `su(2)` labels | family-level compression |
| solve | solve a parameterized radial ODE, impose special-function termination, and assemble allowed labels | one Casimir calculation (13) | radial analytic solve eliminated for the named output |
| recover | sum `ell` multiplicities for total degeneracy | one irrep dimension `(2j+1)^2` | eliminated |
| analytic/certify | radial boundary conditions, normalizability, completeness | domain, existence, completeness of negative-energy eigenspaces | relocated, not eliminated |
| human depth | coordinates, radial ODE, special-function termination, label sum | one module quotient, one kernel, one closure, one Casimir | compressed |

The algebraic route dominates for repeated spectral/degeneracy queries once the
six-generator presentation is constructed.  It does **not** dominate a request
for explicit position-space wavefunctions, local asymptotics, or scattering
phases; those require analytic reconstruction absent from this bench.

## 10. Status and falsification

Status: `supported complete-module full-route algebraic regression; analytic
completeness imported`.

The [three-dimensional module contract](../e3-quadratic-centralizer.md) records
the exact `21 -> 20 -> 10` construction and its `20 -> 7` radial-perturbation
falsifier. The [two-dimensional transfer](coulomb-e2-complete.md) remains the
lower-dimensional closure comparison rather than evidence substituted for this
bench.

The benchmark fails if any of the following occurs:

- the coefficient-derived obstruction does not force (6);
- the lifted operator fails any relation in (9)--(10) on the declared core;
- the Casimir calculation does not reproduce both energy and degeneracy;
- the route is advertised as a full PDE solution rather than the named spectral
  output;
- `SO(4)` is inserted before the operator closure constructs it.

Primary theorem contracts and historical group analyses are catalogued in the
[source map](../sources.md).  They also show why this bench is stronger than a
Legendre regression: the hidden generators mix the angular sectors that ordinary
spatial rotations leave separate.

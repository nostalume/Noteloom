# Complete-module Coulomb transfer on `E^2`

## 1. Question and supplied data

Can the inverse workflow rediscover the hidden Coulomb algebra without selecting a
Runge--Lenz vector module?

```text
H=-1/2 Delta-kappa/r,       kappa>0,       mu=hbar=1.      (1)
```

Supplied: the Euclidean metric, the scalar coefficient (1), the punctured smooth
core, and the request for all first-order and scalar even second-order commutants.

Not supplied: rotations, Runge--Lenz operators, a Lie group, separation
coordinates, spectrum, or degeneracy.

## 2. Full-module construction

The [radial extension](../radial-centralizer-extension.md) applies the complete
three-dimensional Killing-vector module and complete six-dimensional rank-two
Killing-tensor module.  Exact compatibility kernels give

```text
dim ker[X -> X(V)] = 1,
dim ker[K -> d(K dV)] = 4.                               (2)
```

The first kernel generates the rotation vector field

```text
J_0=x partial_y-y partial_x.                              (3)
```

After distinguishing the Hamiltonian, the quadratic kernel contains `L^2` and two
independent tensors.  Solving `dW=K dV` constructs their lower terms

```text
W_x=-kappa x/r,        W_y=-kappa y/r.                   (4)
```

The divergence lift therefore produces `A_x,A_y` without a named ansatz.  In the
tool's real differential convention,

```text
A_x=y partial_xy-x partial_yy+(1/2)partial_x-kappa x/r,
A_y=x partial_xy-y partial_xx+(1/2)partial_y-kappa y/r.  (5)
```

Every generator in (2) is selected by coefficient-derived rank, and every lifted
commutator with `H` vanishes by exact operator composition.

## 3. Closure constructs the group type

The closure certificate consumes (3)--(5), rather than recreating them, and checks

```text
[J_0,A_x]=-A_y,
[J_0,A_y]= A_x,
[A_x,A_y]=-2H J_0.                                       (6)
```

On an energy shell `H=E<0`, define the physical Hermitian angular momentum
`L=-iJ_0` and `M_i=A_i/sqrt(-2E)`.  Equation (6) then becomes the Hermitian
`so(3)` commutator algebra.  The group type is therefore a late energy-sector
output; it was not used to generate the candidates.

## 4. Quantum Casimir and spectrum

Exact differential composition also gives the dimension-specific quantum identity

```text
A_x^2+A_y^2=2H(L^2+1/4)+kappa^2 I.                       (7)
```

On an irreducible negative-energy sector, evaluate both sides on the same carrier:

```text
j(j+1)=L^2+M_x^2+M_y^2
      =-1/4-kappa^2/(2E).                                (8)
```

Consequently the scalar single-valued sectors `j=0,1,2,...` have

```text
E_j=-kappa^2/[2(j+1/2)^2],
deg(E_j)=2j+1.                                           (9)
```

As in the three-dimensional bench, (9) gives the allowed algebraic spectrum and
multiplicity.  Existence and completeness of every bound sector remain an analytic
theorem contract.

## 5. Perturbation discriminates hidden from visible symmetry

Run the unchanged generator on

```text
V=-kappa/r+r^2.                                          (10)
```

Rotation survives, but the quadratic kernel drops from dimension `4` to `2`:

```text
ker B_V=<H,L^2>.                                         (11)
```

Thus rotational symmetry alone does not manufacture Runge--Lenz operators.  The
two hidden directions occur only when the Coulomb coefficient makes the
compatibility rank drop.  This negative control is the decisive evidence that the
machine is reading the PDE rather than replaying a group template.

## 6. Computability audit

The human-retained calculation is

```text
metric -> 3+6 canonical modules -> two kernels -> closure -> one Casimir.          (12)
```

The component rows and Leibniz expansions remain in the replayable certificates.
Compared with the earlier Coulomb derivation, the successful vector type is no
longer supplied, so Step B changes from guided construction to relative-complete
generation.  The special resources are flat dimension two, order two, and the
radial--Laurent coefficient domain.

Status: `supported relative-complete E2 Coulomb regression and group closure`.

The next consequential transfer is dimension three.  There the metric-generated
rank-two module must be constructed with its algebraic redundancy, and the same
kernel must return all three Runge--Lenz components before the existing `so(4)`
spectrum bench can be upgraded.

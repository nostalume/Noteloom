# Noncentral oscillator: exact cross-probe route selection

## 1. Question and common observable

This bench tests whether two valid PDE-first constructions can be compared as
actual reductions rather than as unrelated algebraic descriptions.

```text
Input: H=-Delta/2+(1/2)x^T Kx on Schwartz(R^3),
       K positive with expanded rational coefficients.
Observable: full discrete spectrum and heat trace.
Candidates: normal-mode factorization and complete quadratic centralizer.
Required output: equal ReductionWitness objects plus a route-selection verdict.
```

The input matrix is

```text
K = [[41/25,-12/25,0],
     [-12/25,34/25,0],
     [0,0,3]].                                           (1)
```

No axes, group, factors, eigenvalues, or commuting operators are supplied.

## 2. Factor constructor

Exact characteristic-polynomial reduction gives the distinct positive eigenvalues
`1,2,3`. Instead of enumerating eigenvector components, construct the primitive
projectors by polynomial functional calculus:

```text
P_i=product_(j != i) (K-lambda_j I)/(lambda_i-lambda_j). (2)
```

For (1), this gives

```text
P_1=[[ 9/25, 12/25,0],     P_2=[[16/25,-12/25,0],
     [12/25, 16/25,0],          [-12/25, 9/25,0],
     [0,0,0]],                   [0,0,0]],

P_3=[[0,0,0],[0,0,0],[0,0,1]].                          (3)
```

Exact multiplication verifies `P_iP_j=delta_ij P_i`, `sum P_i=I`, and
`KP_i=lambda_iP_i`. Canonical rational unit vectors spanning their images are

```text
v_1=(3/5,4/5,0),  v_2=(4/5,-3/5,0),  v_3=(0,0,1).       (4)
```

With `z_i=v_i dot x` and `omega_i=sqrt(lambda_i)`, the factor probe constructs

```text
a_i^-=partial_(z_i)+omega_i z_i,
a_i^+=-partial_(z_i)+omega_i z_i,
H_i=(1/2)a_i^+a_i^-+omega_i/2.                           (5)
```

The universal one-mode composition yields the oscillator relations and
`H=sum_i H_i`.

## 3. Independent centralizer constructor

The second route does not start by diagonalizing `K`. The Euclidean metric first
generates 21 rank-two presentations, quotients their intrinsic relation to a
20-dimensional module, and applies `K_tensor -> d(K_tensor dV)`. The exact output
is

```text
first-order kernel = 0,       quadratic kernel: 20 -> 3. (6)
```

Thus no continuous configuration-space group seeds the reduction. From the
returned three-dimensional commutative tensor algebra, the machine selects the
first admitted simple-spectrum element

```text
T=[[-7/24,1/2,0],[1/2,0,0],[0,0,0]],                    (7)
```

whose rational eigenvalues are `-2/3,0,3/8`. Polynomial functional calculus on
`T`, followed only by ordering through `trace(P_iK)`, independently reconstructs
the three projectors in (3). Exact linear solving verifies that each primitive
projector belongs to the generated centralizer kernel.

The corresponding differential operators

```text
Q_i=-1/2 partial^T P_i partial + W_i,
dW_i=P_i dV                                                (8)
```

are generated rather than supplied. Full differential-operator composition checks
`[Q_i,Q_j]=0` and `sum_i Q_i=H`.

## 4. Coincidence witness

Let `S` have columns (4), and `A=S^T`. Both routes return the same data:

```text
AS=SA=I,
A K S=diag(1,2,3),
z=A x,                 x=S z,
(U f)(z)=f(Sz),         (U^-1 g)(x)=g(Ax).               (9)
```

Consequently their reduced dynamics, oscillator representations, and observables
coincide—not merely their final eigenvalue lists. The executable checks equality
of the projectors, `A`, `S`, reduced stiffness, factor relations, operator sum,
operator commutators, and observable payload.

Both routes therefore recover

```text
omega=(1,sqrt(2),sqrt(3)),
E_(n1,n2,n3)=sum_i (n_i+1/2)omega_i,
Tr exp(-tH)=product_i exp(-t omega_i/2)/(1-exp(-t omega_i)). (10)
```

The unitary action of the orthogonal coordinate transform on `L^2`, preservation
of Schwartz space, and completeness of the one-dimensional oscillator basis are
analytic theorem contracts rather than conclusions of the finite certificate.

## 5. Route decision

For the named spectrum and heat trace, both routes have identical work after the
three projectors exist. The centralizer route strictly adds:

1. generation of 21 Killing-tensor presentations;
2. quotienting to 20 independent tensors;
3. a 20-column compatibility kernel;
4. splitting a generated commutant element.

The factor route is therefore selected for this model and observable. This is a
positive result for the decision engine, not a failure of representation theory:
the machine declines a more elaborate algebraic route when direct factorization
constructs the same representation and observable more cheaply.

The centralizer remains useful when the requested capability includes complete
classification of scalar even order-two commuting operators, comparison across
potentials, or detection of symmetry enhancement. Route choice is observable-
relative, not a universal ranking of methods.

## 6. Status and boundary

Status: `supported exact cross-probe selection; analytic completeness imported`.

The executable is
[`oscillator_cross_probe.py`](../computation/oscillator_cross_probe.py), consuming
the exact [rotated input](../computation/examples/rotated-anisotropic-e3.json).
Persistent tests cover projector equality, witness and representation coincidence,
observable recovery, CLI behavior, and refusal of the degenerate isotropic case.

The implementation is bounded to homogeneous positive quadratic potentials in
three dimensions whose stiffness and chosen commutant splitter have rational,
simple spectra and rationally normalized axes. Repeated eigenvalues, affine terms,
indefinite directions, general algebraic eigenvectors, higher-order resonances, and
domain changes require distinct extensions. No general claim that factorization
dominates centralizers is made.

# Observable-cyclic selection for a coupled quadratic PDE

## Purpose and spine binding

This bench tests whether the decision engine can choose between two valid exact
reductions for the same observable. It consumes the group-free quadratic
factorization, but does not ask again for the full spectrum.

- **Input class:** `H_L=-Delta+x^T L^2 x` with real symmetric `L>0`, retained as
  a positive factor or efficient action oracle rather than expanded away.
- **Preparation:** one PDE-constructed ladder excitation in a supplied direction
  `u`.
- **Observable:** its normalized survival amplitude.
- **Competing routes:** full normal-mode/commutant decomposition and the minimal
  observable-cyclic carrier.
- **Internal benchmark:** construct both routes, prove that they return the same
  amplitude, and select by the discovered cyclic degree `r` rather than by a
  hard-coded group or eigenbasis.

The special resource is quadratic closure. The transferable result is the
selection rule and reduction witness, not the oscillator's solvability.

## 1. The PDE constructs a finite coefficient dynamics

Define, for `u in R^n`, the first-order arrows

```text
a_u^- = u^T(nabla+Lx),
a_u^+ = u^T(-nabla+Lx).                                             (1)
```

Their common kernel contains the normalizable Gaussian

```text
psi_0(x) = c exp[-x^T Lx/2],       E_0=tr(L).                        (2)
```

The products in (1) compute the supplied PDE and their polarization computes the
arrow algebra:

```text
H_L = sum_j a_(e_j)^+ a_(e_j)^-+tr(L),
[a_u^-,a_v^+] = 2 u^T L v,
[H_L,a_u^+] = 2 a_(Lu)^+.                                          (3)
```

No eigenbasis of `L` was used. Let

```text
W:R^n -> L^2(R^n),          Wu=a_u^+ psi_0.                          (4)
```

Since `a_u^- psi_0=0`, the commutator in (3) gives the physical inner product on
the coefficient carrier:

```text
<Wu,Wv>
 = <psi_0,a_u^-a_v^+psi_0>
 = 2 u^T L v.                                                       (5)
```

Applying the last relation in (3) to the same input produces the intertwiner

```text
H_L Wu
 = a_u^+H_L psi_0+[H_L,a_u^+]psi_0
 = W[(E_0 I+2L)u].                                                  (6)
```

Thus the infinite-dimensional PDE has an exact `n`-dimensional one-excitation
reduction with coefficient metric `<u,v>_L=u^T L v` and reduced Hamiltonian

```text
T=E_0 I+2L.                                                         (7)
```

Equations (5)--(6) are the analysis/synthesis certificate: `W` is an isometry up
to the fixed factor `sqrt(2)`, and both operator residuals vanish on `Ran(W)`.

## 2. Same observable for both routes

For nonzero `u`, ask only for

```text
C_u(t) = <Wu,exp(-itH_L)Wu>/<Wu,Wu>.                                (8)
```

Equation (6) transports the propagator to the coefficient carrier. Evaluating
both numerator and denominator with (5) gives the basis-free formula

```text
C_u(t)
 = exp[-it tr(L)]
   [u^T L exp(-2itL)u]/[u^T L u].                                  (9)
```

This is the common target against which the two candidates are compared.

## 3. Candidate A: full normal-mode/commutant route

The full route diagonalizes

```text
L=O diag(omega_1,...,omega_n) O^T,
c=O^T u.                                                            (10)
```

Substitution into (9) produces

```text
C_u(t)
 = exp[-it sum_j omega_j]
   [sum_j omega_j |c_j|^2 exp(-2it omega_j)]
   /[sum_j omega_j |c_j|^2].                                       (11)
```

This candidate constructs every independent ladder, number operator, frequency,
and degeneracy relation. It is the right output when the complete spectrum or
many unrelated preparations will be reused. For the single observable (8), every
mode with `c_j=0` is constructed and then discarded.

## 4. Candidate B: observable-cyclic route

Instead construct the relative Krylov carrier

```text
K_u = span{u,Lu,L^2u,...},
r   = dim(K_u).                                                      (12)
```

Because `L` is self-adjoint for `<.,.>_L`, this carrier is invariant under `L`
and has an `L`-orthonormal Lanczos basis `Q_r`. Exact termination is detected by
the first exactly or certifiably zero next-vector norm, not by a floating-point
threshold. Define

```text
J_r = Q_r^(*L) (2L) Q_r,                                            (13)
```

where `Q_r^(*L)` is the adjoint for the coefficient metric. With the first basis
vector `q_0=u/sqrt(u^TLu)`, invariance gives

```text
(2L)Q_r=Q_r J_r,
u^T L f(2L)u/(u^TLu)=e_1^T f(J_r)e_1                               (14)
```

for every polynomial `f`; the finite spectral theorem extends (14) to the
exponential. Hence the second candidate returns

```text
C_u(t)=exp[-it tr(L)] e_1^T exp(-itJ_r)e_1.                         (15)
```

Equations (11) and (15) coincide because both were evaluated from the same
functional-calculus expression (9). The cyclic route has not approximated the
invisible modes: it has proved that they do not occur in this observable.

The retained human object is one three-term recurrence of length `r`. Classical
special polynomials may name that recurrence in particular families, but they are
outputs of the cyclic measure rather than the machine's input catalogue.

## 5. Decision and whole-route cost

The ground-state factorization (1)--(7) is shared cost. After it, the two route
profiles are:

| Cost item | Full normal modes | Exact cyclic carrier |
| --- | --- | --- |
| discovery | diagonalize or recognize a global commuting algebra | apply `L` until the Krylov rank stops growing |
| dense arithmetic | `O(n^3)` eigensystem | `O(r n^2+r^2n)` orthogonalized iteration |
| sparse/operator arithmetic | depends on global eigensolver | `O(r nnz(L)+r^2n)` |
| retained carrier | all `n` one-excitation modes | exactly `r` observable-visible directions |
| recovery | weighted sum over all visible normal modes | one entry of `exp(-itJ_r)` |
| human data | complete frequency/eigenvector family | one recurrence and one initial vector |

Therefore the decision engine returns

```text
if r << n and only C_u or functions u^T L f(L)u are requested:
    Select(ObservableCyclicReduction)

if r=n and no reusable recurrence or sparsity improves execution:
    EquivalentCost or Select(FullModesForReuse)

if many preparations or the complete spectrum are requested:
    Select(FullModeReduction), unless a block-cyclic reuse plan is cheaper.
```

This is a conditional computational-leverage result. It counts discovery,
construction, and recovery, and it refuses to infer savings merely from the
tridiagonal shape of `J_r`. If the PDE supplies only the expanded potential matrix
`K=L^2`, construction of its positive square root belongs to shared cost and may
erase the advantage. Finite-precision Lanczos before exact termination is a
different approximate branch and requires loss-of-orthogonality and quadrature
error certificates.

## 6. Scalable semantic check: hypercube-coupled oscillators

Let `A_d` be the adjacency operator of the `d`-dimensional hypercube and take

```text
L=aI+bA_d,          a>d|b|,          b!=0,          n=2^d,           (16)
```

with `u` the indicator of one vertex. Positivity in (16) follows from the
hypercube eigenvalue interval `[-d,d]`. The span of vectors constant on each
distance shell from `u` is preserved by `A_d`. Counting neighbors between adjacent
shells gives an irreducible recurrence with nonzero neighboring coefficients, so
the cyclic carrier reaches all and only these `d+1` directions. Thus

```text
r=d+1=1+log_2(n).                                                    (17)
```

The independent commuting-flip construction writes

```text
A_d=X_1+...+X_d,       X_j^2=I,       [X_i,X_j]=0.
```

It evaluates the vertex return function as

```text
<u,exp(-isA_d)u>=cos(s)^d.                                          (18)
```

Applying `(i/2)d/dt` to the coefficient exponential in (9), with `s=2bt`,
computes the same survival amplitude:

```text
C_u(t)
 = exp[-it(2^d a+2a)]
   [cos(2bt)^d
    -i(db/a) sin(2bt) cos(2bt)^(d-1)].                              (19)
```

Equation (19) is a semantic coincidence witness between the commutant and cyclic
routes, not an appeal to a table of hypercube polynomials. If the commuting-flip
factorization is supplied or cheaply recognized, both routes are `O(d)` semantic
constructions and the engine should retain them as equivalent witnesses. If only
sparse action and the preparation are available, the cyclic route reaches (17)
without first reconstructing the global tensor-product group.

As a separate sign check, the binomial spectral sum and (19) were evaluated in
double precision for `d=1,...,8`, `a=3`, `b=0.2`, and `t=0.37`; the maximum
absolute residual was `2.55e-14`. The binomial and derivative calculations above,
not this finite sample, are the exact witness.

## 7. Status and boundary

Passed:

- both candidates instantiate exact reduction witnesses on the same prepared
  sector;
- equations (9), (11), and (15) recover exactly the same observable;
- the discovered relative degree `r` supplies an observable-dependent selector;
- the hypercube family shows exponential carrier compression without enumerating
  vertices, modes, or polynomial components.

Boundaries:

- the quadratic factorization and invariant one-excitation sector are special;
- a cheap retained factor/action for `L` is part of the leverage condition;
- computing or applying `L` may itself dominate the route for an opaque dense
  coefficient matrix;
- `r=n` supplies no cyclic dimension reduction;
- higher-excitation and nonlinear observables generate larger symmetric-power
  carriers and require a new cost comparison;
- approximate early termination is not certified by this bench. The
  [finite exact cyclic backend](../computation/README.md) can certify its basic
  Duhamel boundary bound, but no nonquadratic PDE transfer has yet consumed it.

The portable global result is: **construct only the cyclic representation seen by
the preparation and observable, then enlarge to a group decomposition only when
reuse or closure repays its discovery cost.**

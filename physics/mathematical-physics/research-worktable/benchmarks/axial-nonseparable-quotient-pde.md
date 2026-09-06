# Axial nonseparable PDE: a 3D-to-2D orbit reduction

## 1. Spine binding

- **Upstream:** the boundary stabilizer and fixed-accuracy disk nodes construct
  `SO(2)` and show a 2D-to-1D gain.
- **Bridge question:** does the same mechanism reduce a PDE to lower-dimensional
  PDEs when ordinary separation does not finish the problem?
- **Invariant target:** one manufactured continuum solution in cylindrical
  weighted `L^2`, together with exact equality of the two discrete routes.
- **Baseline:** a full sparse 3D finite-volume solve.
- **Reduced route:** discover the connected stabilizer, extract source character
  support, solve the resulting 2D quotient PDEs, and synthesize the same field.
- **Horizon:** scalar elliptic operator on an annular cylinder, finite source
  support, periodic angular grid, and sparse direct solution. The rotation axis
  and curved/non-product boundaries remain outside this node.

Source [48](../sources.md) supplies only the sparse linear-solver substrate. The
joint stabilizer, sector PDE, manufactured forcing, intertwining witness, and cost
comparison are constructed internally.

## 2. The PDE and its constructed group

On

```text
M={(r,theta,z):1<r<2, theta in S^1, 0<z<1},                    (1)
```

with Dirichlet conditions at `r=1,2` and `z=0,1`, consider

```text
L=-r^(-1) d_r(r a d_r)-d_z(b d_z)-c r^(-2) d_theta^2+V,       (2)

a=1+(r-1)z/5,   b=1+(r-1)z/7,
c=1+(r-1)z/9,   V=1+(r-1)z/11.                               (3)
```

The inverse step starts from the six affine Euclidean Killing generators. The
radial walls remove `T_x,T_y`; the end caps and coefficient dependence remove
`T_z`; the axis/end caps remove `J_x,J_y`. Only

```text
J_z=-y d_x+x d_y                                               (4)
```

annihilates all coefficients and preserves every boundary trace. Its connected
action is `SO(2)`. A control with a `cos(theta)` coefficient returns
`NoExactOrbitReduction` because the interior residual of (4) is nonzero.

This is bounded discovery relative to the affine Euclidean ansatz, not a universal
symmetry classifier.

## 3. Why the reduced object remains a PDE

The generic orbits are circles, so

```text
dim M=3,   dim orbit=1,   dim(M/SO(2))=2.                       (5)
```

The quotient variables are `(r,z)`. Character analysis
`u_m(r,z)e^(im theta)` gives the parameterized operator

```text
L_m=-r^(-1)d_r(r a d_r)-d_z(b d_z)+c m^2/r^2+V.               (6)
```

Every mixed coefficient derivative `d_r d_z a`, `d_r d_z b`, `d_r d_z c`, and
`d_r d_z V` is nonzero. Hence (6) is not an additive radial-plus-axial operator in
the cylindrical product presentation. Orbit reduction has stopped at a coupled
2D PDE; it has not smuggled in an ODE or special-function solution. This is not a
proof against every possible nonlinear coordinate transformation.

## 4. Source-visible sector selection

Choose the exact continuum solution

```text
u_* = sin(pi(r-1)) sin(pi z)
      [1+(3/10)cos(theta)+(1/5)sin(2 theta)],                  (7)
```

and construct `f=L u_*` analytically. Its representation support is

```text
(m,real type)={(0,cos),(1,cos),(2,sin)}.                       (8)
```

Since `L` is equivariant, the solution of `Lu=f` has the same support. Thus three
real quotient fields are solved; no spectral or special-polynomial catalogue is
enumerated. This is a source-specific certificate. It does not truncate a full
resolvent, which sees arbitrary sectors.

A second admissible input changes all four couplings, makes one diffusion coupling
negative while retaining ellipticity, and replaces (8) by sine weight `1` and
cosine weight `3`. The same constructor passes at eight quotient cells with
continuum error `1.295e-2`, selects weights `{1,3}`, and reconstructs the full
discrete solution within `5.2e-16`. Thus neither the coefficients nor active
characters are hard-coded to the regression output.

## 5. Discrete equality witness

Use a cell-centered finite-volume matrix `A_Q` on the `(r,z)` quotient and a
periodic second-difference matrix `L_theta` on 24 angular nodes. The full matrix is

```text
A_full=A_Q tensor I + diag(c/r^2) tensor L_theta.              (9)
```

The discrete characters diagonalize `L_theta` with

```text
mu_m=4 sin^2(m h_theta/2)/h_theta^2.                           (10)
```

Therefore the exact discrete sector matrix is

```text
A_m=A_Q+mu_m diag(c/r^2).                                     (11)
```

Equations (9)--(11), rather than agreement with the manufactured answer, construct
the intertwiner. At the accepted resolution the executable measures

```text
analysis residual                         5.6e-16,
synthesis/full-equation residual          2.6e-15,
full versus reconstructed relative L2     6.3e-16.             (12)
```

So the two numerical routes are the same discrete PDE under character analysis and
synthesis.

## 6. Fixed-accuracy complexity result

The continuum observable is weighted relative `L^2` error against (7), with target
`1/50`. Both routes fail at six quotient cells per direction with error `2.178e-2`
and pass at eight cells with error `1.220e-2`.

| accepted-resolution quantity | full 3D route | three quotient PDEs |
| --- | ---: | ---: |
| solved unknowns | 1,536 | 192 |
| assembled nonzeros | 9,984 | 864 |
| relative continuum `L^2` error | `1.220e-2` | `1.220e-2` |
| algebraic/discrete residual | `3.7e-15` | below `2.6e-15` after synthesis |

The solved-carrier ratio is exactly

```text
3 N_r N_z / (24 N_r N_z)=1/8.                                (13)
```

The nonzero ratio is `864/9984=0.0865`. Failed refinements, stabilizer discovery,
assembly, all three solves, synthesis, and continuum-error evaluation remain in
the machine-readable cost record. One-run timings are retained as observations
only because sparse-direct fill and hardware dominate their portability.

If the complete field is requested, synthesis still costs
`Theta(N_r N_z N_theta)`; the reduction primarily removes solve work and storage.
For a sector-local observable, full-field synthesis can be omitted.

## 7. What this changes—and what it does not

The supported principle is now stronger than radial reduction:

```text
group orbits remove one variable;
the quotient variables remain coupled;
one parameterized 2D PDE template replaces a 3D component system;
source representation support selects the finite solve set.                  (14)
```

This supports both computer and human computability. A human retains (6), the
three labels (8), and one synthesis formula—not 24 angular component equations or
a catalogue of separated functions.

Still unpaid: an axis-containing domain with singular orbit strata; a curved or
non-product boundary; vector/spinor multiplicity bundles; high-accuracy and
iterative/preconditioned baselines; arbitrary source tails; and group discovery
beyond the declared Killing ansatz. The next strongest test is therefore a warped
axial boundary including the rotation axis, where isotropy generates sector-
dependent regularity conditions.

## 8. Reproducibility

```powershell
uv run physics\mathematical-physics\research-worktable\computation\axial_quotient_pde.py `
  physics\mathematical-physics\research-worktable\computation\examples\axial-nonseparable-manufactured.json `
  --summary

uv run --directory physics\mathematical-physics\research-worktable\computation `
  --with numpy==2.3.3 --with scipy==1.16.1 `
  python -m unittest check_axial_quotient_pde.py -v
```

The coefficient-dependent control and changed-coupling/changed-character transfer
are available through the same public constructor. The JSON output retains
discovery residuals, orbit dimensions,
sector origin, refinement attempts, analysis/synthesis residuals, continuum error,
cost components, human compression, and explicit non-certifications.

# Warped axial boundary and singular-orbit reduction

## 1. Spine binding

The annular axial benchmark proved `3D PDE -> 2D PDE family` but deliberately
removed the rotation axis and used a product boundary. This node asks whether the
same constructor survives both missing features: a fixed-point orbit and a warped
wall. The invariant target is one manufactured continuum solution in cylindrical
weighted `L^2`; the two routes must also be exactly intertwined after
discretization.

The bounded domain is

```text
Omega={0<=r<R(z), 0<z<1},       R(z)=1+z(1-z)/2,                (1)
```

with Dirichlet data on the outer wall and end caps. The baseline is a full
three-dimensional sparse finite-volume solve on the same warped cylindrical mask.

## 2. Boundary-compatible group and orbit strata

The joint coefficient/domain/trace stabilizer retains only

```text
J_z=-y partial_x+x partial_y,       G=SO(2).                    (2)
```

For `r>0`, the orbits are circles and the quotient is two-dimensional. At `r=0`,
the entire group fixes the point. Thus the axis becomes a singular boundary
stratum of `Omega/SO(2)`, even though it is not a physical boundary of `Omega`.

If `u_m` has character `exp(i m alpha)`, isotropy gives

```text
u_m(0,z)=exp(i m alpha)u_m(0,z) for every alpha.                (3)
```

Consequently `u_m(0,z)=0` for `m!=0`. Smooth Cartesian extension strengthens this
to the human rule

```text
u_0: partial_r u_0(0,z)=0,
u_m: u_m(r,z)=O(r^|m|),      m!=0.                              (4)
```

The executable derives (4) from the isotropy label. A control applying uniform
Neumann data to all weights returns `AxisRegularityObstruction`; it does not solve
an incorrectly reduced PDE.

## 3. Coupled sector PDE and manufactured solution

Use the smooth axial operator

```text
L=-r^(-1)partial_r(r a partial_r)-partial_z(b partial_z)
  -c r^(-2)partial_theta^2+V,                                  (5)

a=1+r^2 z(1-z)/5,   b=1+r^2 z(1-z)/7,
c=1+r^2 z(1-z)/9,   V=1+r^2 z(1-z)/11.                        (6)
```

Character analysis again yields coupled 2D operators `L_m`; it does not produce
ODEs. The manufactured modes are

```text
u_m=r^m [R(z)^2-r^2]z(1-z),      m=0,1,2,                     (7)
```

with amplitudes `1`, `(1/3)cos(theta)`, and `(1/5)sin(2theta)`.
They satisfy the physical boundary and the generated axis orders by construction.
The forcing `f=L u` is differentiated analytically, so continuum error does not
depend on a special-function oracle.

## 4. Discrete intertwining and cost

Cell-centered radial flux has zero area at the axis. The angular discrete
Laplacian supplies the character value
`mu_m=4 sin^2(m h_theta/2)/h_theta^2`, so the full masked matrix and sector
matrices obey the same Kronecker/character intertwiner as in the annular case.

At target relative error `1/50`, both routes fail at resolutions 8 and 12 and pass
at 16:

| accepted-resolution quantity | full warped 3D route | three stratified 2D sectors |
| --- | ---: | ---: |
| active quotient cells | 246 | 246 |
| solved unknowns | 5,904 | 738 |
| assembled nonzeros | 39,792 | 3,498 |
| continuum relative `L^2` error | `9.622e-3` | `9.622e-3` |
| full/reconstructed difference | — | `9.54e-16` |
| analysis residual | — | `7.69e-16` |
| synthesis residual | — | `6.11e-14` |

The solved-carrier ratio remains `3/24=1/8`; the nonzero ratio is `0.0879`.
Construction of the warped mask and axis rule, failed refinements, assembly,
solution, and full-field synthesis are charged. Wall times are observations only;
SciPy supplies the sparse direct solve, not the reduction semantics.

## 5. Meaning and next boundary

This closes the first stratified boundary descent for scalar fields:

```text
physical boundary + fixed-point isotropy
 -> quotient boundary strata
 -> representation-dependent regularity
 -> valid sector domains
 -> exact synthesis of the full discrete PDE.                            (8)
```

The result is more than a coordinate singularity convention: the axis condition
is forced by the isotropy representation. That same mechanism predicts a richer
finite fiber for tensors and spinors, where rotations act on internal indices and
the admissible total weight combines orbital and fiber weights.

Still unpaid: boundary-fitted high-order geometry, arbitrary warp grammars,
axis-sensitive error estimates, iterative/preconditioned scaling, spin/Clifford
fibers, and nonlinear sector fusion. The next globally discriminating branch is
therefore bundle-valued isotropy reduction—not another scalar axial example.

## 6. Reproducibility

```powershell
uv run physics\mathematical-physics\PDE-group-research\computation\warped_axis_quotient_pde.py `
  physics\mathematical-physics\PDE-group-research\computation\examples\warped-axis-manufactured.json `
  --summary

uv run --directory physics\mathematical-physics\PDE-group-research\computation `
  --with numpy==2.3.3 --with scipy==1.16.1 `
  python -m unittest check_warped_axis_quotient_pde.py -v
```

The wrong-axis-policy input exercises the refusal path through the same public
constructor.

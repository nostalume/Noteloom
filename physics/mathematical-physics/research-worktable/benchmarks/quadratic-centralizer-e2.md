# Complete quadratic-centralizer transfer on the Euclidean plane

## 1. Bridge question and invariant

The Coulomb regression still selected a rotation-vector module by hand.  This
bench asks whether a PDE can instead generate a **complete** bounded candidate
space and let its coefficients select the hidden operators.

```text
Input: H=-1/2(∂_x^2+∂_y^2)+V(x,y),  V in Q[x,y].
Capability: all scalar, time-reversal-even commuting operators of order <=2.
Invariant: the same joint spectral problem for H and every generated Q.
Baseline: a generic coefficient ansatz for Q followed by determining equations.
```

The [quadratic generator](../quadratic-centralizer-generator.md) replaces the
baseline with the canonical six-dimensional Killing-tensor module and one exact
kernel calculation.

## 2. Transfer input hides its coordinates

The executable receives only the expanded polynomial

```text
V = 3x^4-4x^3y+18x^2y^2-4xy^3+3y^4+3x+3y.             (1)
```

No rotation, separating variables, group, or expected integral is supplied.  The
input happens to admit the compressed expression

```text
V=F(u)+G(v),  u=x+y, v=x-y,
F(u)=u^4+3u,  G(v)=2v^4,                                (2)
```

but (2) is retained only as an independent recovery check after generation.

## 3. Generated kernel

For each basis vector of the complete tensor module (3) in the parent calculus,
the tool constructs `d(K dV)`.  Exact rational row reduction returns

```text
dim ker(B_V)=2,
dim(ker(B_V)/<g>)=1.                                    (3)
```

The first generator is the metric and reconstructs `H`.  The nontrivial kernel
representative is generated as

```text
K^xx=K^yy=0,       K^xy=1,                              (4)
W=-(x^4+y^4)+12x^3y-6x^2y^2+12xy^3+3x+3y.              (5)
```

Using (2) only after the calculation identifies `W=F(u)-G(v)`.  Divergence
quantization returns

```text
Q=-∂_x∂_y+F(u)-G(v),        [H,Q]=0.                    (6)
```

The commutator in (6) is not sampled numerically: differential operators are
composed with the full Leibniz rule and every polynomial coefficient cancels
exactly.

## 4. The generated operator constructs separation

Apply the invertible linear coordinate map `(x,y)->(u,v)` to the two already
constructed operators.  Since

```text
∂_x=∂_u+∂_v,        ∂_y=∂_u-∂_v,                       (7)
```

both combinations land on the same scalar carrier and evaluate to

```text
(H+Q)/2 = -∂_u^2+F(u),
(H-Q)/2 = -∂_v^2+G(v).                                  (8)
```

Thus the hidden operator generates the coordinates and the tensor-sum
decomposition; coordinates did not generate the operator.  Joint spectral labels
`(r,s)` give

```text
E_(r,s)=epsilon_r[F]+epsilon_s[G],
Q_(r,s)=epsilon_r[F]-epsilon_s[G].                       (9)
```

No claim is made that either one-dimensional quartic spectrum has a closed form.
The construction produces an exact computational reduction: a two-dimensional
spectral problem is replaced by two reusable one-dimensional problems and pairwise
arithmetic.  Since this bench does not execute those one-dimensional solvers, a
use-level runtime or accuracy advantage remains open.

## 5. Whole-route cost

For an `N x N` tensor discretization, the unreduced carrier has dimension `N^2`.
The generated decomposition stores and solves two one-dimensional operators of
dimension `N`, then forms requested sums (9).  Dense asymptotic comparisons are
only indicative—structure-aware numerical baselines may also exploit tensor
form—but the exact semantic reduction is independent of discretization.

Human depth changes from generic coefficient PDEs plus guessed coordinates to

```text
metric Killing algebra -> six tensor seeds -> one kernel -> one eigenframe.      (10)
```

The construction cost is paid once for the potential; subsequent spectral,
propagator, or resolvent queries reuse the two one-dimensional factors.

## 6. Negative transfer and relative nonexistence

Run the identical generator on

```text
V_generic=x^4+xy+y^3+2x.                                (11)
```

It returns

```text
dim ker(B_V)=1,
ker(B_V)=<metric>,
status=MetricOnly.                                      (12)
```

Because the six-dimensional Killing module is complete, (12) rules out every
additional nonconstant scalar even quadratic integral, modulo the affine span of
`H` and the identity, in the admitted class.  It does not
rule out higher-order, odd, non-polynomial, matrix-valued, or nonlocal symmetries.

## 7. Reproducibility and status

Inputs:

- [`rotated-quartic.json`](../computation/examples/rotated-quartic.json)
- [`generic-polynomial.json`](../computation/examples/generic-polynomial.json)

Runner:

```powershell
python physics\mathematical-physics\research-worktable\computation\quadratic_centralizer.py `
  physics\mathematical-physics\research-worktable\computation\examples\rotated-quartic.json `
  --summary
```

Status: `supported relative-complete quadratic transfer on Q[x,y]`.

As a limiting regression, kernel dimensions grow from `2` for an anisotropic
quadratic potential to `4` in its isotropic limit and `6` in the free limit.  The
enhancement is detected as a rank drop of `B_V`; no symmetry group name is used to
trigger it.

The result upgrades Step B only inside its declared class.  The
[radial rejoin](coulomb-e2-complete.md) now rediscovers the Coulomb Runge--Lenz
integrals from the full six-dimensional module, not a selected vector ansatz.  The
next open rejoin is the complete rank-two construction in dimension three.

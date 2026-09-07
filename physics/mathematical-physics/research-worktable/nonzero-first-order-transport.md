# Nonzero first-order transport

## Frozen contract `C_G6_v1`

### Why this probe matters

G5 proved that a generated coupled action can descend through curvature,
first-order, zeroth-order, and common-core layers, but every successful first-order
coefficient was zero. That leaves two live explanations: the defect compiler is a
reusable operator construction, or its apparent success is confined to a vanishing
layer. G6 changes only that layer while keeping the schema, relation constructor,
generic defect laws, domain contract, and Pauli factorization fixed.

The admitted operator remains

```text
H = g^(ij) Pi_i Pi_j + sum_i C_i Pi_i - b Sigma_F,
[Pi_i,Pi_j] = i F_ij I.                                (1)
```

No fixture supplies a curvature axis, drift scalar, generator, grading, completed
square, or energy polynomial.

### PDE-to-algebra selection

In oriented Euclidean dimension three, construct

```text
f = (F_23,F_31,F_12),       b = sqrt(f dot f),
e = f/b.                                                 (2)
```

For scalar coefficients `C_i=c_i I`, the fiber commutator in the existing G5
first-order residual vanishes, leaving

```text
R_C,i(A,B) = -sum_j A_(j,i)c_j I.                       (3)
```

Thus the generic compiler, not the observable consumer, intersects the curvature
stabilizer with the stabilizer of `c`. If `c=mu e`, the rotation about `e` survives.
A transverse `c` kills it. No axial rule is added to the compiler.

Only after a nonzero action survives does the optional Pauli consumer extract each
`c_i` by the exact scalar-identity equality, compute

```text
mu = (c dot f)/b,       delta_i = c_i - mu f_i/b,        (4)
```

and require every `delta_i` to vanish. Matrix-valued coefficients are outside this
consumer even when they preserve the generic operator action.

### Algebra-to-PDE recovery

With parallel momentum `Pi_parallel=e^i Pi_i`, equation (4) gives

```text
sum_i C_i Pi_i = mu Pi_parallel I.                      (5)
```

The transverse Pauli offsets remain exactly those of G5. For either curvature
grading sector and its orbital offset `epsilon`, longitudinal Fourier analysis
constructs

```text
E(k) = k^2 + mu k + epsilon
     = (k + mu/2)^2 + epsilon - mu^2/4.                 (6)
```

The machine returns both polynomial coefficients and the completed-square
constant. This is an exact symbolic recovery; it does not enumerate coordinate
eigenfunctions. The old transverse-channel list remains unchanged, so the G5
bilateral comparison retains its original target.

## Frozen discriminators

1. With `F_12=3` and `C_3=2I`, curvature must reduce `3 -> 1`, the first-order
   block must retain that action, and the consumer must derive `e=(0,0,1)` and
   `mu=2`.
2. The returned polynomial must be `k^2+2k+epsilon`, with momentum shift `1` and
   completed-square constant `epsilon-1`.
3. Rotating the data to `F_23=3` and `C_1=2I` must derive `e=(1,0,0)` and return
   identical polynomial channels without a preferred coordinate axis.
4. With `F_12=3` and `C_1=2I`, curvature may first leave one action, but the
   unchanged first-order defect must reduce it to zero and report
   `first-order-covariance`.
5. At the frozen G6 boundary, an axial matrix coefficient `C_3=2 gamma_3` may
   preserve the operator action, but scalar observable recovery must refuse while
   retaining the exact generic candidate as partial evidence.

The claim is falsified if the compiler learns an axial special case, the fixture
contains `e` or `mu`, rotation changes the dispersion, the transverse coefficient
is ignored, or observable refusal erases the successful generic construction.

## Evidence ledger

The G6 closure gate runs 146 unit tests and 20 computational checks. Ruff lint and
format checks pass, all 68 JSON fixtures parse, Python compilation succeeds, and
241 local Markdown links resolve. These repository checks certify reproducibility;
the inferential content remains bounded by the discriminators below.

### `E-G6-01` — nonzero aligned regression

The positive fixture returns relation dimensions `13 -> 4 -> 3`, followed by

```text
curvature-covariance:    3 -> 1, rank drop 2,
first-order-covariance:  1 -> 1, rank drop 0,
zeroth-order-covariance: 1 -> 1, rank drop 0.
```

Equations (2)--(4) return `e=(0,0,1)` and `mu=2`. Through orbital level one, the
four exact energy polynomials have constants `0,6,6,12`; equation (6) returns
completed-square constants `-1,5,5,11`. Direct rational substitution verifies the
polynomial/completed-square identity.

### `E-G6-02` — rotated transfer

The rotated fixture changes the only nonzero curvature plane from `12` to `23`,
rotates the scalar coefficient from component `3` to `1`, and changes the Pauli
zeroth-order matrix accordingly. The same operations derive `e=(1,0,0)`, retain
the same rank path, and return exactly the same transport data and channel
polynomials.

### `E-G6-03` — two distinct refusals

The transverse scalar coefficient is not silently projected onto `e`: the generic
first-order defect kills the final action and reports `NoEffectiveOperatorSymmetry`
at `first-order-covariance`. In contrast, the axial matrix coefficient preserves a
one-dimensional operator action but returns `UnsupportedChannelLowerOrder` at
`observable-recovery`. Its exact generic candidate remains in the obstructed
envelope with `use=null` and no advertised analysis/synthesis maps.

## Cost and disposition

G6 does not enlarge the generic plan: it still has three input actions, nineteen
residual coordinates, and bracket bound 63. The scalar consumer checks `d` matrices
against the identity, performs one `d`-term contraction and one exact reconstruction,
then emits `2(r+1)` structured channel records. At the tested `d=3`, fiber size
two, and `r=1`, this adds twelve matrix-entry comparisons, two length-three vector
passes, and four records. It performs no eigenfunction expansion or eigensolve.

Disposition: **supported bounded** for nonzero constant scalar transport parallel
to a rational-norm curvature axis in the Euclidean rank-three Pauli common-core
contract. This is transfer of the unchanged operator compiler and exact downstream
use, not a runtime advantage or a general matrix-valued spectral theorem.

Variable coefficients, non-Euclidean metrics, irrational exact norms,
matrix-valued transport, boundary domains, global integration, and self-adjoint
completion remain outside `C_G6_v1`. The matrix-valued refusal identifies the next
consequential bridge: construct an observable-relative finite coefficient algebra
and its projectors rather than adding another Pauli component rule. That bridge is
now implemented separately under [`C_G7_v1`](matrix-valued-transport-algebra.md);
this page retains the G6 closure contract and evidence counts.

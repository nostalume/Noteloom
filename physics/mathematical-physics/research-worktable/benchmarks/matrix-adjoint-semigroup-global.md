# Global analytic promotion of the generated adjoint symbol

## Spine binding and bounded horizon

The [symbol-covariance constructor](matrix-symbol-covariance-casimir.md) produces
an exact second-order action on `Sym(sl_n^*)`, but no Hilbert space, positive real
form, self-adjoint domain, normalized measure, or global group. Formal polynomial
closure therefore cannot yet support heat evolution.

F7 asks for the smallest analytic promotion that changes this capability:

```text
generated complex coefficient algebra and eigenvalue
  + involution and positivity data
  + global carrier and domain contract
  -> one closed adjoint coefficient heat-semigroup block
  -> one heat matrix element and the prior exchange amplitude.           (1)
```

The horizon remains `n=2,3` and one adjoint coefficient copy. The full heat trace
and full Peter--Weyl spectrum are not targets.

## The involution constructs the compact real form

The new physical datum is conjugate transpose `X -> X^*`. Intersect its skew fixed
space with the generated traceless algebra:

```text
k={X in sl_n(C): X^*=-X}.                               (2)
```

On (2), the supplied normalization constructs

```text
<X,Y>=-2 tr(XY).
```

For `X!=0`, skew-adjointness gives the decisive positivity computation

```text
<X,X>=-2tr(X^2)=2tr(X^*X)>0.                            (3)
```

Thus the complex algebra alone did not select compactness; the involution did.
Exponentiating (2) inside the determinant-one matrices produces the connected
star-unitary group

```text
K_sc={U: U^*U=I, det U=1}=SU(n).                        (4)
```

Connected integration and compactness in (4) are explicit finite-dimensional Lie
theorem contracts. The executable constructor retains them as contracts rather
than claiming to prove them by matrix sampling.

## The observable determines the effective global group

The center of (4) is

```text
Z_n={zeta I: zeta^n=1}.                                 (5)
```

For the retained coefficient function `q_Y(g)=Ad_(g^-1)Y`, evaluate a central
translate:

```text
q_Y(zg)
 =Ad_((zg)^-1)Y
 =Ad_(g^-1)Ad_(z^-1)Y
 =Ad_(g^-1)Y
 =q_Y(g).                                               (6)
```

Hence every retained state, tensor amplitude, and heat matrix element factors
through

```text
K_eff=SU(n)/Z_n=PSU(n).                                 (7)
```

Normalized Haar probability on `SU(n)` pushes forward to normalized Haar
probability on (7). Equations (6)--(7) therefore prove equality of analysis,
synthesis, and observable on the simply connected group and the adjoint quotient.
The PDE cannot distinguish these global groups using only the chosen adjoint
observable; this is a computed inverse ambiguity, not missing metadata.

## Domain and semigroup theorem contract

On

```text
H=L^2(PSU(n),sl_n(C)),
Dom(Delta)=H^2(PSU(n),sl_n(C)),
C=C^infinity(PSU(n),sl_n(C)),                           (8)
```

use normalized Haar probability and the positive bi-invariant Laplacian. Compact
ellipticity supplies the imported contract that this realization is self-adjoint,
that `C` is a core, and that `exp(-t Delta)` is a contraction semigroup.

F6 already generated, rather than supplied,

```text
Delta q_Y=n q_Y.                                       (9)
```

Functional calculus now turns the algebraic result into analytic evolution:

```text
exp(-t Delta)q_Y
 =sum_(r>=0) (-t)^r Delta^r q_Y/r!
 =sum_(r>=0) (-nt)^r q_Y/r!
 =exp(-nt)q_Y.                                        (10)
```

For `O_Z(q_W)=tr(ZW)`, equations (9)--(10) give the common observable

```text
O_Z(exp(-t Delta)q_Y)=exp(-nt)tr(ZY).                  (11)
```

The power-series display is a calculation on the eigenvector; the self-adjoint
spectral theorem is what promotes it to the closed semigroup in (8).

## Regression, transfer, and refusal

For rank three, choose `tr(ZY)=1` and `t=1/2`. The constructor returns

```text
exp(-3/2)=0.22313016014842982...                        (12)
```

and retains the F6 exchange result `(5,1)` with odd/even parts `(2,3)`. Rank two
uses `t=1/3` and returns

```text
exp(-2/3)=0.513417119032592...                          (13)
```

together with the one-channel exchange result `(4,-4)`.

Two negative fixtures leave the local F6 witness intact:

- transpose without complex conjugation does not supply the admitted compact
  positive real form and returns `RealFormPositivityObstruction`;
- an `L^2`-only operator declaration lacks the `H^2` Laplacian domain and returns
  `DomainContractObstruction`.

Local algebraic correctness is therefore neither erased nor silently upgraded by
global analytic failure.

## Computability and boundary

For the named observable, promotion adds one involution check, one positivity
identity, one center quotient, one imported compact elliptic theorem contract, one
scalar exponential, and one trace pairing. It performs no new spectral solve and
enumerates no representation sectors. This is analytical and human computation on
the visible block, not a full heat-kernel algorithm.

The result does not recover representations on which the center acts nontrivially,
the full heat trace, noncompact real forms, or arbitrary coefficient algebras. The
next generality test must replace the hardwired inner derivations of full traceless
matrix algebras by a bounded stabilizer/derivation constructor for a supplied
natural-operation tensor.

## Theorem contracts and provenance

The worktable constructs (2)--(7), the observable quotient, and the composition
(9)--(11). It imports compact-group Haar, elliptic self-adjointness, and spectral
functional-calculus facts. Sources 10 and 53 in the [source map](../sources.md)
anchor the compact invariant-operator and normalization contracts.

## Artifacts

- Promotion router: `../computation/matrix_adjoint_global_router.py`
- Rank-three input: `../computation/examples/matrix-adjoint-semigroup-sl3.json`
- Rank-two transfer: `../computation/examples/matrix-adjoint-semigroup-sl2.json`
- Real-form refusal: `../computation/examples/matrix-adjoint-semigroup-wrong-real-form.json`
- Domain refusal: `../computation/examples/matrix-adjoint-semigroup-wrong-domain.json`
- Public tests: `../computation/test_reduction_workbench.py`

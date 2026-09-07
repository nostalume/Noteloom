# PDE-first matrix Lie-algebra reconstruction

## Question

The forward adjoint PDE bench starts from `SU(n)`. This inverse bench removes that
label. Its input is a small family of exact traceless matrix-valued coefficient
seeds, their common second-order action on a declared smooth coefficient span, the
two PDE couplings, and the exchange-paired observable. It asks for the effective
infinitesimal algebra and reduced maps—not for a unique global group.

The bounded executable horizon is matrix size two or three over the rationals. It
does not accept a root system, weight list, structure constants, Casimir value, or
expected reduced output.

## Minimal closure constructor

Let the supplied seeds be `B_1,...,B_s`. Build

```text
L_0=span_Q{B_1,...,B_s},
L_(k+1)=L_k+span_Q{[X,Y]: X,Y in a basis of L_k}.       (1)
```

Exact row reduction admits a new bracket only when it increases rank. The process
stops when a full pass adds no direction or the declared dimension budget is
exceeded. This is a generative closure, not an enumeration of unknown structure
constants.

For the rank-three fixture, four simple off-diagonal seeds produce

```text
dim L_k: 4 -> 8 -> stable.                              (2)
```

Every seed and bracket is traceless. Since the resulting space has dimension
`3^2-1`, it equals the entire traceless matrix space. The program additionally
checks

```text
[L,L]=L,                 dim Z(L)=0,
rank(tr(B_i B_j))=8.                                  (3)
```

Thus the effective complex represented algebra is `sl_3(C)`. This recognition is
particularly cheap because the matrix realization makes the ambient traceless
space available; it is not a general Lie-algebra classifier.

## Recovering the representation and multiplicity maps

Once `L=sl_n(C)` is constructed, its coefficient fiber is its adjoint module under

```text
ad_A X=[A,X].                                          (4)
```

The associative matrix product generates the same two natural maps as the forward
bench:

```text
F(X,Y)=[X,Y],
D(X,Y)=XY+YX-(2/n)tr(XY)I.                             (5)
```

Their equivariance is certified without component tables. The identity

```text
[A,XY]=[A,X]Y+X[A,Y]                                  (6)
```

proves naturality of `F`; (6) plus cyclicity of trace proves naturality of `D`.
For `n=2`, polarized Cayley--Hamilton makes `D` identically zero. For `n=3`, the
constructed closure contains a pair for which `D` is nonzero. The bounded
adjoint-tensor theorem contract then identifies two channels in rank three and
one in rank two.

## Meeting the forward PDE witness

The PDE input declares that its smooth coefficient span is a common eigenmodule
of the positive second-order part:

```text
Delta q=lambda q.                                      (7)
```

This is coefficient-jet data extracted upstream from the PDE; it is not supplied
as a group Casimir. For the rank-three fixture `lambda=3`, so the visible action is

```text
R_X(Y)=4[a[X,Y]+b{X,Y}_0].                             (8)
```

With the same preparation, probe, and couplings as the forward bench, the inverse
route returns

```text
ordered=5, exchange-reversed=1,
odd=2,     even=3.                                     (9)
```

The test compares (9) directly with the independently routed
`su-adjoint-pde/v1` result. The rank-two transfer infers `sl_2(C)`, obtains factor
three from (7), returns `(4,-4)`, and retains only the bracket channel.

## Refusal and ambiguity

Two rank-three seeds `E_12,E_23` close only to the three-dimensional strictly
upper-triangular algebra. The constructor returns `IncompleteCoefficientAlgebra`;
it does not rename this proper subalgebra `sl_3` or invent missing directions.

Even successful recovery gives only an effective complex infinitesimal algebra.
It does not determine:

- a compact versus noncompact real form;
- a simply connected group versus a central quotient;
- a kernel of the global action;
- completeness of coefficient fields beyond the supplied eigenmodule.

Accordingly the public result says `global_group: unresolved`. This is a feature
of the bilateral semantics: PDE-to-group recovery is an equivalence class with
explicit ambiguity, never a forced inverse function.

## Computability verdict

The rank-three input contains four seed matrices. Closure tests 34 pair brackets
across two passes and stores no structure-constant table. The retained human
description is

```text
four seeds -> commutator closure -> full traceless space
           -> ad + (bracket, traceless Jordan)
           -> one scalar differential action -> one trace observable.           (10)
```

This is exact internal and human compression for the bounded matrix grammar. It
does not itself discover (7) or the covariance-generating vector fields. The
[symbol-covariance continuation](matrix-symbol-covariance-casimir.md) repairs that
dependency for an invariant matrix-symbol grammar, while arbitrary coordinate
coefficient jets remain outside both constructors.

## Artifacts

- Router: `../computation/matrix_pde_inverse_router.py`
- Rank-three fixture: `../computation/examples/matrix-pde-inverse-sl3.json`
- Rank-two transfer: `../computation/examples/matrix-pde-inverse-sl2.json`
- Nonspanning refusal: `../computation/examples/matrix-pde-inverse-incomplete.json`
- Public tests: `../computation/test_reduction_workbench.py`

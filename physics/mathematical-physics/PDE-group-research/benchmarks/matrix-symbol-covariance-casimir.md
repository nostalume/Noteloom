# Matrix-symbol covariance and generated second-order action

## Obstruction repaired

The PDE-first matrix closure recovered `sl_n(C)` and its natural bracket/Jordan
maps, but it still received the scalar relation `Delta q=n q` as input. Supplying
that eigenvalue concealed the differential part of the bilateral bridge.

A literal array of coordinate jets would repair this by reintroducing the
component expansion the worktable is meant to avoid. The invariant replacement is
the smallest symbol-fiber datum from which those jets can be generated:

```text
exact matrix coefficient seeds,
a quadratic pairing belonging to the principal symbol,
the polynomial core Sym(L^*),
the natural tensor dynamics and observable.             (1)
```

No group, Lie-algebra name, covariance generator, Casimir label, coefficient
eigenvalue, root, weight, or expected amplitude is supplied.

## From coefficients to first-order covariance arrows

Exact commutator closure first constructs the coefficient algebra `L`. As in the
preceding inverse bench, four rank-three seeds close `4 -> 8` and therefore fill
the traceless matrix space. For every generated `A in L`, construct—not guess—the
linear vector field on `L`

```text
X_A f(x)=d f_x([A,x]),        f in Sym(L^*).             (2)
```

Associativity of matrix multiplication gives the Jacobi identity, and hence

```text
[X_A,X_B]=X_[A,B].                                      (3)
```

The executable certificate represents (2) in the generated basis and checks all
`dim(L)^2` residuals in (3) exactly. This finite component check audits the
constructor; it is not the derivation and is not retained as a structure-constant
table.

## The principal pairing decides whether the arrows are symmetries

Let the supplied covariant principal pairing be

```text
g(A,B)=2 tr(AB).                                        (4)
```

For each constructed inner derivation `ad_A`, cyclicity of trace computes

```text
g([A,X],Y)+g(X,[A,Y])
 =2 tr(AXY-XAY+XAY-XYA)
 =0.                                                    (5)
```

Thus the matrix equation

```text
ad_A^T g+g ad_A=0                                      (6)
```

has zero residual in every generated direction. Equation (6) is the covariance
test for the quadratic symbol; the coefficient algebra alone would not make an
arbitrary PDE metric invariant.

The refusal fixture replaces (4) by the identity matrix in the generated,
nonorthogonal closure basis. Its first residual (6) is nonzero, so the constructor
returns `PrincipalSymbolCovarianceObstruction`. It does not manufacture a symmetry
from the coefficient commutator alone.

## Generating the second-order operator

Let `B_i` be the generated basis and `g^(ij)` the exact inverse of (4). On the
polynomial core, construct the pairing-dual square

```text
Delta_g=sum_(i,j) g^(ij) X_(B_i) X_(B_j).              (7)
```

This is a basis-independent second-order differential operator because (6) makes
the inverse pairing invariant. For a linear coefficient

```text
ell_Y(x)=g(Y,x),                                        (8)
```

equation (2) sends its label by the dual adjoint action. Applying (7) twice and
contracting with the inverse pairing gives an endomorphism `C` of `L`:

```text
X_A ell_Y(x)
 =g(Y,[A,x])
 =-g([A,Y],x)
 =-ell_{[A,Y]}(x),

Delta_g ell_Y
 =sum_(i,j) g^(ij) ell_[B_j,[B_i,Y]]
 =ell_(C Y).                                            (9)
```

The machine constructs `C` and tests whether it is scalar rather than assuming a
Casimir eigenvalue:

```text
C=3 I_L  for the rank-three input,
C=2 I_L  for the rank-two transfer.                    (10)
```

Consequently

```text
Delta_g ell_Y=n ell_Y,       n=3 or 2.                 (11)
```

The normalization in (4) is essential. Rescaling the principal pairing rescales
(7) and therefore changes (9); it is physical differential data, not a group
convention added after the calculation.

## Bilateral coincidence and use

The generated scalar action now supplies the input previously imported by the
matrix-PDE inverse. Composing it with the internally constructed natural maps gives

```text
R_X(Y)=(1+n)[a[X,Y]+b{X,Y}_0].                         (12)
```

For the unchanged rank-three preparation and couplings, (11) returns

```text
(ordered, reversed)=(5,1),      (odd, even)=(2,3).     (13)
```

The rank-two transfer derives eigenvalue two, returns `(4,-4)`, and removes the
Jordan channel. Thus the coefficient-to-covariance-to-second-order route and the
group-first adjoint PDE meet at the same reduced observable without sharing a
supplied eigenvalue.

## What this does and does not establish

This is an exact differential construction on the algebraic core `Sym(L^*)`. Its
human object is four seeds, the commutator, one trace pairing, and one pairing-dual
square. It avoids named-group search, coordinate charts, root/weight enumeration,
and a stored structure-constant tensor.

It is not yet analytical completion. The polynomial core is not supplied with a
positive Hilbert norm, self-adjoint closure, compact real form, Haar measure, or
global group action. Nor is the constructor a stabilizer solver for arbitrary
polynomial PDE tensors: it handles the pairing-dual-square grammar generated by a
matrix symbol fiber. These debts must remain separate.

## Artifacts

- Constructor: `../computation/matrix_pde_inverse_router.py`
- Rank-three input: `../computation/examples/matrix-symbol-covariance-sl3.json`
- Rank-two transfer: `../computation/examples/matrix-symbol-covariance-sl2.json`
- Broken-pairing refusal: `../computation/examples/matrix-symbol-covariance-broken-pairing.json`
- Public tests: `../computation/test_reduction_workbench.py`

# Simple-block PDE reduction

## Frozen contract `C_G10_v1`

G9 constructs an isotypic block `H_r ~= V_r tensor M_r` with dimensions `d,m`,
but still acts on the full `q=dm` carrier. G10 must construct one copy of `V_r`,
reduce a second-order differential symbol, and reconstruct the same observable.
Neither a tensor basis nor an irreducible label may enter the input.

## Primitive commutant slice

The commutant acts as `I_V tensor End(M)`. Therefore a primitive projector of the
commutant has rank `d`, its range is invariant under `A`, and that range realizes
one irreducible carrier.

G10 scans only a declared number of Hermitian commutant elements constructed by
G9. For each candidate `S`, it calls G8 on `(P_r,P_r S P_r)`. It accepts only an
exact rational splitting into `m` projectors under `P_r`, each of rank `d`:

```text
Q_a Q_b=delta_ab Q_a,    sum_a Q_a=P_r,    rank(Q_a)=d.        (1)
```

This is a bounded scan of a constructed invariant space, not a search over group
elements, algebra words, block layouts, or arbitrary coefficient tuples. If no
admitted element splits rationally, it returns `MultiplicitySplitterUnavailable`.

From one `Q_a`, the machine retains `d` independent columns as an exact embedding

```text
B : Q(i)^d -> Q(i)^q,       image(B)=image(Q_a).                (2)
```

For every coefficient `C` in the represented algebra it solves, rather than
assumes, the intertwining equation

```text
C B = B C_red.                                                 (3)
```

The solution `C_red` is the constructed irreducible action. Failure of (3) is a
typed carrier-invariance obstruction.

## Second-order PDE use

The downstream object is the constant-coefficient differential symbol

```text
K(k)=k^2 K_2+k K_1+K_0,                                      (4)
```

covering a one-dimensional matrix second-order equation or one covector ray of a
multidimensional symbol. For Hermitian `K_j` in `A`, (3) constructs

```text
K(k)B=B K_red(k),
det K(k) = det K_red(k)^m.                                    (5)
```

The implementation computes both determinants over `Q(i)` and accepts only exact
agreement. A Hermitian coefficient outside the bicommutant returns
`CoefficientOutsideRepresentedAlgebra`; otherwise a multiplicity operator could
act differently on other copies and invalidate (5).

## Evidence

For `M_2` acting twice, the first admitted commutant candidate splits the rank-four
carrier into two rank-two projectors. Exact projector columns construct `B`; both
`sigma_x tensor I_2` and `sigma_z tensor I_2` satisfy (3). With `K_2=I`, `K_1=X`,
`K_0=Z`, and `k=2`, the reduced determinant is `11` and the full determinant is
`121=11^2`.

A rational orthogonal conjugation changes the embedding but preserves full and
reduced determinants at `k=3`. Zero splitter budget returns
`MultiplicitySplitterUnavailable`. A noncentral commutant coefficient returns
`CoefficientOutsideRepresentedAlgebra` before determinant comparison.

The closure gate runs 169 unit tests and 20 computational checks. Ruff passes over
74 Python files, compilation succeeds, all 69 JSON fixtures parse, and 256 local
Markdown links resolve.

## Complete-route cost

The ledger reports a scalar-work proxy, not runtime. For carrier dimension `q`,
reduced dimension `d`, and tested splitter count `t`, it uses

```text
construction = G9 commutator-system entries + t q^4 + q d^2,
baseline/query = q^3,
reduced/query = d^3,
recovery/query = max(1, bit_length(m)).                        (6)
```

The bench has `3344` construction units and per-query `64` versus `8+2`, giving
proxy break-even at 62 evaluations. It supports amortized leverage for this proxy,
not single-solve dominance or a hardware-runtime claim. Exact bit growth, domain
solution, and Fourier integration remain outside (6).

## Disposition and next obstruction

Disposition: **supported bounded** for one full finite Gaussian-rational isotypic
block when a constructed commutant element exposes rational primitive projectors
within budget. G10 upgrades multiplicity from an integer to an executable
irreducible action and exact second-order-symbol reconstruction.

If `P_r=P_r(x)` varies, derivatives produce `(partial P_r)` coupling and (5) no
longer yields independent PDE sectors. [G11](variable-projector-differential-jet.md)
now constructs the induced connection and exact first/second leakage jet. A
quantitative adiabatic error still requires gap, norm, time, and domain data.

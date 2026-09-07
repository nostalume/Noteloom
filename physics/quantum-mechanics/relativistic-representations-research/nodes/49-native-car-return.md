# Native CAR return compiler

Status: selective factorization and native CAR reachability expose and retain a
compact rank-30 algebra; post-hoc Wick evaluation is correct but computationally
rejected

Consumes: [node 47's graded functional port](47-graded-return-functional-port.md),
node 41's CAR interaction, and the
local-before-bath factorization of the Anderson model.

Produces: native graded directions, reduced free/interaction actions, source
coordinates, exact normal-product certificates, and the thermal-state obstruction
consumed by [node 53](53-native-thermal-boundary.md).

## Obstruction: late factor recovery preserves early matrix expansion

The scalar port asks only for insertions

```text
O_j={q_j,d^dagger},                                      (49.1)
```

but an opaque `64 x 64` matrix hides which local and bath operations a contraction
evaluator can share. Regrouping indices constructs

```text
H=H_bath tensor H_local,
O_j=sum_(alpha=1)^r L_(j,alpha) tensor B_(j,alpha).      (49.2)
```

The rank is that of the induced map `End(H_local)^* -> End(H_bath)`, so it is
invariant under separate local/bath coordinate changes.

For each bath factor, calculate charge from

```text
N_b=sum_i c_i^dagger c_i,
[N_b,B]=qB.                                              (49.3)
```

Then generate only normal words

```text
C_(I,J)=prod_(i in I)c_i^dagger prod_(j in J)c_j,
|I|-|J|=q,                                               (49.4)
```

and solve inside that sector. This exposes a determinant-consumable language
without enumerating the full bath operator basis.

## Why the post-hoc Wick route still fails

With interaction events appended to an endpoint word, the free thermal CAR state
generates the contraction recursively:

```text
W(A_1,...,A_(2k))
 =sum_(j=2)^(2k)(-1)^j <A_1A_j>_0
   W(A_2,...,omit A_j,...,A_(2k)),                       (49.5)
```

equivalently as a Pfaffian. This is a reusable constructor, but applying it after
the matrix-valued graded module fans every endpoint word across every ordered
interaction cell. Correctness does not remove that earlier expansion.

## Construct the algebra natively

Retain an operator directly as

```text
O=sum_(a,b,I,J)o_(abIJ) C_(I,J) tensor E_ab.             (49.6)
```

Products are generated from the three CAR rewrites

```text
c_i c_j^dagger=delta_(ij)-c_j^dagger c_i,
c_i c_j=-c_jc_i,
c_i^dagger c_j^dagger=-c_j^dagger c_i^dagger,           (49.7)
```

plus `E_ab E_cd=delta_(bc)E_ad`. Each exchange lowers inversion number and each
contraction lowers word length, proving termination. For diagonal `H_0`, every
label has the computable free gap

```text
[C_(I,J) tensor E_ab,H_0]
 =(E_b-E_a+sum_(j in J)epsilon_j-sum_(i in I)epsilon_i)
   C_(I,J) tensor E_ab.                                 (49.8)
```

Normal ordering also constructs the trace metric:

```text
Tr_b C_(I,J)=delta_(IJ)2^(m-|I|),
Tr_d(E_ab^dagger E_cd)=delta_(ac)delta_(bd).             (49.9)
```

Thus free spectral closure, interaction commutators, and independence are all
computed before any full-Hilbert matrix is formed.

## Evidence ladder

- `E49-selective-factor-v1`: the 30 carriers require 109 local--bath factors, while
  their observable insertions require 77 rather than the dense local bound 480.
  Maximum rank falls from seven to three; reconstruction and Green recovery hold
  within `8.17e-16` and `5.56e-16`.
- `E50-car-consumability-v1`: the 77 bath factors contain 182 stable occurrences
  drawn from 66 charge-homogeneous words, rather than 19,712 dense per-factor
  coefficients. Reconstruction and Green recovery hold within `4.56e-15` and
  `3.94e-15`.
- `E51-word-native-v1`: the endpoint-extended Wick operation is correct, but it
  generates 74,446 Wick evaluations, 988,270 Pfaffian updates, and about 24.0
  million operations. Its `32.06 s` local run loses to the `1.04 s` raw path and
  `0.041 s` endpoint routes; adjacent-order error is also unusably loose.
- `E52-native-CAR-reachability-v1`: applying (49.6)--(49.9) during generation gives

```text
filtration rank                 (2,6,12,22,30)
support by exact valuation      (2,20,26,146,100)
retained native coefficients                  294
ambient matrix slots                       122,880
counted native / matrix work       128,000 / 7,794,688.  (49.10)
```

The native closure residual is zero; independent matrix recovery residuals are
`3.14e-16` and `1.65e-16`. Its small-bench Python runtime (`0.122 s`) remains slower
than optimized dense NumPy (`0.051 s`).

## Disposition and edge

Selective factorization and charge-adapted words are supported semantic exposure.
The Wick constructor is retained as a general CAR operation, but the post-hoc
functional route and its self-certificate are rejected. Native reachability is the
surviving generative tool: it stores 294 coefficients and callable reduced actions,
with about 61-fold structural work reduction on the frozen model. Runtime leverage,
cross-model transfer, continuum baths, and asymptotic advantage remain unresolved.

The next required object is not another Pfaffian cache. It is a thermal functional
acting on this native module. Node 53 tests whether stationarity, right-action
closure, or a trace-behavioral quotient can construct it economically.

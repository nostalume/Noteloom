# Correlation-functional return

Status: finite Hermitian returns admit an internally constructed scalar functional
and endpoint perturbative recurrence; dense state metrics and fixed-rank moment
expansion fail as general reduction routes on the frozen Anderson bench

Consumes: node 39's Pauli--Fierz return, node 41's Anderson response, node 13's
operation grammar, and `V_response-1`.

Produces: the coefficient-valued correlation functional and normalized resolvent
target consumed by the graded return compiler.

## Capability and obstruction

Both field and impurity problems can be written as a visible return

```text
M(z)=B^dagger(z-K)^(-1)B,                               (43.1)
```

but notation alone does not construct `K`, the prepared functional, or a cheaper
query. In the Anderson energy basis one may set

```text
K_A(m,n)=E_n-E_m,
B_A(m,n)=sqrt((w_m+w_n)/Z) d_mn,                        (43.2)
```

which recovers the Green function exactly but first computes the full eigensystem.
This is a verification representation, not the desired native constructor.

## From cyclic vectors to a state functional

For a Hermitian `K`, source-generated projection constructs

```text
Q_r=orth span{B,KB,...,K^(r-1)B},
T_r=Q_r^dagger K Q_r,
C_r=Q_r^dagger B.                                      (43.3)
```

Because `K^aB=Q_rT_r^aC_r` for `a<r`, the first `2r` moments satisfy

```text
B^dagger K^j B=C_r^dagger T_r^j C_r.                   (43.4)
```

This construction transfers to the two frozen domains, but Anderson coordinates
still import (43.2). Let `rho=exp(-beta H)/Z` and

```text
L(A)=AH-HA,
<A,B>_rho=Tr[A^dagger(rho B+B rho)].                    (43.5)
```

Positivity follows by splitting (43.5) into the squared norms of
`rho^(1/2)A` and `A rho^(1/2)`. Since `[rho,H]=0`, trace cyclicity gives

```text
<A,L(B)>_rho=<L(A),B>_rho.                              (43.6)
```

Hence `(z-L)X=d` and `G(z)=<d,X>_rho` generate the same response without
transition labels. Yet the observable uses this metric only through

```text
mu_k=<d,L^k(d)>_rho.                                    (43.7)
```

The density matrix can therefore be replaced by the restricted functional. With
`W=exp(-beta H)` define

```text
D_d=W d+d W,
Omega_d(A)=Tr(D_d^dagger A)/Tr(D_d^dagger d).           (43.8)
```

CAR computes `Tr(D_d^dagger d)=Tr(W)`, so (43.8) is normalized internally. The
moments (43.7) generate a Hankel pairing and, when its rank is stable, a Jacobi
return. This reduces state information but inherits a loose off-axis residual
bound.

## Endpoint perturbative construction

For the actual order-four target, write

```text
H(lambda)=H_0+lambda V,
W(lambda)=sum_(s=0)^4 lambda^s W_s,
L(lambda)=L_0+lambda L_1.                               (43.9)
```

Coefficient matching in `partial_t W=-H(lambda)W` constructs the state once:

```text
partial_t W_0=-H_0W_0,                 W_0(0)=1,
partial_t W_s=-H_0W_s-VW_(s-1),        W_s(0)=0.        (43.10)
```

Set `Z_s=Tr(W_s)` and `D_s=W_s d+d W_s`. The resolvent coefficients are generated
without imaginary-time quadrature:

```text
(z-L_0)X_0=d,
(z-L_0)X_s=L_1X_(s-1).                                  (43.11)
```

Their common scalar target and normalization are

```text
Q_s(z)=sum_(a+b=s) Tr[D_a^dagger X_b(z)],
G_s(z)=[Q_s(z)-sum_(a=1)^s Z_aG_(s-a)(z)]/Z_0.          (43.12)
```

Replacing `X_b` by the generated nested-commutator coefficients also yields the
large-`z` moment series. Thus the moment and resolvent routes consume the same
functional rather than two fitted models.

## Evidence and bounded disposition

The fixed domain is finite-dimensional, Hermitian, equilibrium, scalar, and
off-axis. It excludes continuum limits, zero-temperature singular states,
nonnormal/Keldysh generators, and real-axis certification without a gap.

- `E43-cyclic-transfer-v1`: the unchanged cyclic operation preserves the first
  `2r` moments. Pauli--Fierz rank is 12 at depth four; Anderson rank is 10 at depth
  ten. The latter needs 221 queries to amortize its full transition adapter, and
  its generic error bounds overestimate observed errors by factors about 411--554.
- `E44-native-metric-v1`: (43.5)--(43.6) recover the transition-space response to
  `9.79e-16`, but dense metric setup costs `12,005,864` operations versus `524,288`
  for the cached spectral adapter. Complete-route leverage is rejected.
- `E45-functional-moment-v1`: 21 scalar correlations reproduce the state-metric
  moments within `2e-11`; setup falls to `1,072,104`, with conditional break-even
  after 135 certified queries. The useful accuracy certificate remains unresolved.
- `E46-perturbative-correlation-v1`: one `320 x 320` endpoint action replaces 25
  time-sampled actions and recovers all five Green coefficients within `5.63e-17`.
  At `z=40i`, moment and resolvent series agree within `4.01e-18`.

The zeroth-order depth-six Hankel singular values are

```text
(3,3,2.56e-16,9.06e-17,0,0),                            (43.13)
```

so fixed-rank Jacobi expansion at `lambda=0` would invert four nonexistent
directions. The retained result is therefore the endpoint functional
(43.10)--(43.12), not the dense metric or a regularized moment inverse.

## Edge and boundary

The functional is exact/error-bounded on the frozen bench and gives real
state-construction leverage over time quadrature. It does not yet give a reusable
multi-frequency module: every query still applies five full operator resolvents,
and rank changes with coupling order. Node 47 consumes precisely this valuation
obstruction. Re-entry into the dense metric or transition route requires a new
consumer that changes their complete-cost verdict.

# Native thermal-functional boundary

Status: the native rank-30 dynamical algebra remains valid, but exact thermal
closure and both packet- and final-query behavioral quotients are rejected on the
frozen Anderson route

Consumes: [node 49's native graded algebra](49-native-car-return.md) and
[node 47's normalized Green target](47-graded-return-functional-port.md).

Produces: the state/dynamics separation, exact trace-behavioral construction,
rank/resource boundary, and stopped-branch disposition `V_native-thermal-1`.

## State dynamics is not commutator dynamics

Stationarity `Phi([O,H])=0` does not determine `Phi(O)`. Let

```text
R_r(t)=[lambda^r]exp[-t(H_0+lambda V)].                 (53.1)
```

Differentiation and cyclicity construct

```text
d/dt Tr[R_r(t)X]
 =-Tr[R_r(t)XH_0]-Tr[R_(r-1)(t)XV].                    (53.2)
```

The required observable actions are therefore right multiplications

```text
D_0(X)=XH_0,      D_1(X)=XV,                            (53.3)
```

not the commutators that close the rank-30 real-frequency algebra.

For the partition and its 30 endpoint restrictions, seed

```text
X_0=1,
X_j=q_jd_up^dagger+d_up^dagger q_j.                    (53.4)
```

Direct closure would construct

```text
T_0=cyclic_(D_0){X_0,...,X_30},
T_(r+1)=cyclic_(D_0)D_1T_r.                             (53.5)
```

Right multiplication by `V` escapes the dynamical module with residual
`0.5527707983925674`, so importing that module would assume the missing state.

## Generate the trace-behavioral realization

Direct dual closure preserves distinctions before the common preparation is used.
Reverse the construction around the identity state:

```text
P_0=cyclic_(right H_0){1},
P_(r+1)=cyclic_(right H_0){pV:p in P_r}.                (53.6)
```

In native bases `p_(r,a)`, generate action matrices `A_0,A_1` and output rows

```text
(C_r)_(j,a)=Tr[p_(r,a)X_j].                             (53.7)
```

The continuation space and its invisible kernel are

```text
K=span{C_r A_(i_1)...A_(i_k)},
N=K^perp.                                               (53.8)
```

For an orthonormal row basis `Q` of `K`, quotient actions are forced by

```text
Q A_i=Abar_i Q,      Abar_i=Q A_i Q^dagger.             (53.9)
```

This is generative: the reduced evolution

```text
y(beta)=exp[-beta(Abar_0+Abar_1)]Q[1]                   (53.10)
```

returns every grade/output coefficient through the compressed rows.

## Compose the final Green consumer

The 31-output packet may still preserve too much. Node 49's algebra generates

```text
(z-J_0)y_0=b,
(z-J_0)y_r=J_1y_(r-1).                                  (53.11)
```

Before quotienting, construct the actual numerator rows

```text
n_s(z)=sum_(a+b=s)sum_(j=1)^30 y_(b,j)(z)C_(a,j),
Q_s(z)=n_s(z)x(beta),                                   (53.12)
```

and normalize with

```text
Z_s=C_(s,0)x(beta),
G_s(z)=[Q_s(z)-sum_(a=1)^s Z_aG_(s-a)(z)]/Z_0.          (53.13)
```

The final-query continuation space is generated from only the five partition rows
and five `n_s(z)` rows. A smaller seed rank is useful only if it remains invariant
under `A_0,A_1`; otherwise it precomputes one answer rather than retaining thermal
evolution.

## Evidence and calculation boundary

The horizon is the two-impurity-mode, four-bath-mode model, `beta=2`, coupling
grade four, the first Matsubara query, and 100 million declared work units.

- `E53-native-dual-closure-v1`: (53.5) reaches grade-zero rank 136 and incomplete
  grade-one rank 76 before refusing at `101,866,899` work units with 16,889 retained
  coefficients. Eventual full-algebra saturation is not claimed.
- `E54-trace-Hankel-v1`: the identity construction refuses during grade three at
  `100,838,570`. A relaxed diagnostic completes with

```text
prefix rank                   (10,16,26,32,36)
behavioral rank               (10,16,26,32,36)
total prefix / quotient rank               120 / 120
retained native coefficients                  18,283
declared work                            407,361,547
packet recovery error                  8.26 * 10^(-11). (53.14)
```

- `E55-final-Green-faithfulness-v1`: the ten rows from (53.12)--(53.13) have seed
  rank four, but backward continuation has rank 120. Hence `dim N=0`. All five
  normalized coefficients are recovered within `2e-8`.

## Disposition and stop

- The state/dynamics distinction and the constructions (53.2)--(53.13) are exact
  within the admitted finite algebra.
- The rank-30 native commutator compiler remains a valid reusable dynamical tool.
- Reuse of that module as a Gibbs functional is rejected by measured right-action
  escape.
- Packet-relative and final-query exact invariant quotients are rejected because
  their continuation rank equals the full reachable rank 120.
- Native thermal complete-route leverage is rejected by the 407.4-million-work
  diagnostic; faster kernels would not alter the semantic-rank verdict.

This branch is stopped. Re-entry requires a changed semantic contract: a certified
finite time/temperature or accuracy window, a different observable algebra, or a
new generated state primitive capable of changing semantic rank or complete-route
cost. Optimizing the same exact rank-120 realization is not re-entry.

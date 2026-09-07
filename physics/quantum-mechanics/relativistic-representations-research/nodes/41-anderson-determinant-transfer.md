# Anderson-impurity determinant transfer

Status: post-freeze transfer bench completed for `C_response-v1`; bounded semantic
transfer and contraction compression are supported, while complete-route leverage
is rejected on the frozen order-four observable

Consumes: node 40's frozen observable-relative interaction calculus and node 05's
CAR/exterior recurrence. Source boundaries are `IRT-03` and `IRT-04` in
`../sources/interaction-return-transfer-contracts.md`.

Produces: a condensed-matter adapter, a CAR-generated determinant quotient of bath
graphs, and an independent full-Hilbert coefficient target for one impurity Green
function.

## Why this transfer is discriminating

Node 39 still resembles the field/Hamiltonian seeds from which `C_response-v1` was
constructed. The Anderson model changes four structural features at once:

- fermionic rather than bosonic internal statistics;
- an equilibrium state functional rather than one prepared vector;
- a retained interacting local sector rather than a quadratic return; and
- a bath-contraction determinant rather than explicit graph histories.

If the core contract survives these changes through adapter data alone, it has a
bounded cross-domain transfer. If a new repair or meaning of the observable class
is required, the candidate must split or be rejected.

## Freeze the finite model and observable

Order fermionic modes only for serialization as

```text
(d_up,d_down,c_(1,up),c_(1,down),c_(2,up),c_(2,down)).    (41.1)
```

The semantic input is the CAR, not Jordan--Wigner matrices. Let

```text
H(lambda)=H_imp+H_bath+lambda H_hyb,
H_imp=-sum_sigma n_(d,sigma)+2 n_(d,up)n_(d,down),
H_bath=sum_sigma[-3/4 n_(1,sigma)+3/4 n_(2,sigma)],
H_hyb=(1/3)sum_(k=1)^2 sum_sigma
       [c_(k,sigma)^dagger d_sigma+d_sigma^dagger c_(k,sigma)]. (41.2)
```

Thus `epsilon_d=-1`, `U=2`, the bath is particle--hole symmetric, and `lambda`
grades hybridization order. Fix inverse temperature `beta=2` and the first
fermionic Matsubara frequency `omega_0=pi/beta=pi/2`. The requested observable is

```text
G_up(i omega_0;lambda)
 =-integral_0^beta exp(i omega_0 tau)
   Tr[rho_lambda T d_up(tau)d_up^dagger] d tau,
rho_lambda=exp(-beta H(lambda))/Z(lambda).                 (41.3)
```

The finite Hilbert space has dimension `2^6=64`; exact diagonalization is feasible
but remains the comparison route, not the proposed compiler.

## Generate Fock signs from the CAR

For an occupation word `n=(n_1,...,n_6)`, applying the annihilator of mode `j`
crosses the occupied odd modes preceding it. Hence

```text
a_j|n>=0                                      if n_j=0,
a_j|n>=(-1)^(sum_(l<j)n_l)|n-e_j>             if n_j=1.  (41.4)
```

Creation has the same prefix sign and the opposite occupancy condition. Applying
the two orders to one word computes

```text
(a_i a_j^dagger+a_j^dagger a_i)|n>=delta_(ij)|n>.         (41.5)
```

Equation (41.5) is the serialization certificate. Reordering (41.1) conjugates all
operators and cannot change (41.3). A sign table supplied independently of (41.4)
is not admitted.

## Eliminate only the quadratic bath

For one spin, the free bath equation at complex frequency `z` is

```text
(z-epsilon_k)c_k=V_k d.
```

Solving and substituting at the impurity port gives

```text
c_k=V_k d/(z-epsilon_k),
Delta(z)=sum_k |V_k|^2/(z-epsilon_k)
        =(1/9)[1/(z+3/4)+1/(z-3/4)].                      (41.6)
```

The local interaction `2 n_(d,up)n_(d,down)` is not absorbed into `Delta` or called
a self-energy. Bath elimination produces an interacting impurity action with free
kernel `z+1-Delta(z)` and the unchanged local `U` operation. Thus (41.6) removes
bath degrees of freedom without pretending to solve the impurity.

## Let CAR antisymmetry compress the bath graphs

At hybridization order `2k`, fix impurity annihilation times
`tau_1,...,tau_k` and creation times `tau'_1,...,tau'_k`. Let `C_k` be the bath
expectation after all bath modes have been eliminated. Moving the first odd
annihilator to each possible partner computes

```text
C_k=sum_(j=1)^k (-1)^(j-1)
      Delta(tau_1-tau'_j)
      C_(k-1)(omit tau_1, omit tau'_j),
C_0=1.                                                   (41.7)
```

Construct the matrix `D_(ij)=Delta(tau_i-tau'_j)`. Laplace expansion along its
first row obeys exactly (41.7), so induction generates

```text
C_k=det D.                                                (41.8)
```

This is the algebra compiler's retained quotient: `k!` signed bath-contraction
graphs become one determinant computed in `O(k^3)` arithmetic after its `k^2`
entries are built. It is not an imported diagram rule. The local impurity trace,
time integrations, perturbative convergence, and possible sign cancellations
remain irreducible costs.

Expanding (41.8) recovers every bath pairing and its CAR sign. Therefore the graph
route is diagnostic and reversible at the prequotient level, while the determinant
is the direct realization consumed by the observable.

## Generate the local-trace boundary from the grading

Do not import a hybridization-expansion sign table. The fixed local-before-bath
mode order constructs the graded factorization

```text
d_sigma=d_sigma^loc tensor 1,
c_(k,sigma)=P_d tensor c_(k,sigma)^bath,
P_d=(-1)^(n_(d,up)+n_(d,down)).                           (41.9a)
```

Consequently each even interaction term factorizes without an undetermined sign:

```text
c_(k,sigma)^dagger d_sigma
  =(P_d d_sigma)^loc tensor c_(k,sigma)^dagger,
d_sigma^dagger c_(k,sigma)
  =(d_sigma^dagger P_d)^loc tensor c_(k,sigma).            (41.9b)
```

At order `r`, Dyson expansion over the ordered simplex
`beta>t_1>...>t_r>0` therefore computes the unnormalized Green numerator as

```text
Q_r=-(-1)^r integral d tau exp(i omega_0 tau)
       integral_(t_1>...>t_r) sum_(e_1,...,e_r)
       Tr_d[e^(-beta H_loc) T(d_up(tau) F_(e_1)(t_1)...
                              F_(e_r)(t_r)d_up^dagger)]
       Tr_b[e^(-beta H_b) B_(e_1)(t_1)...B_(e_r)(t_r)].    (41.9c)
```

Here `F_e` and `B_e` are exactly the two factors in (41.9b). Removing the external
operators constructs `Z_r`. No `1/r!` remains because the integration domain is
already ordered.

For ordered bath events, construct the antisymmetric contraction matrix `K` from
the two nonzero CAR pairings

```text
<B_sigma(t_i) B_sigma^dagger(t_j)>
  =sum_k |V_k|^2 exp[-epsilon_k(t_i-t_j)](1-f_k),
<B_sigma^dagger(t_i) B_sigma(t_j)>
  =sum_k |V_k|^2 exp[ epsilon_k(t_i-t_j)]f_k,              (41.9d)
```

where `i<j`, `t_i>t_j`, and `f_k=(exp(beta epsilon_k)+1)^(-1)`. CAR recurrence
gives `Pf(K)`. Number conservation makes the annihilation--annihilation and
creation--creation blocks zero. If `pi` groups annihilators before creators, direct
Pfaffian permutation gives

```text
Pf(K)=sgn(pi)(-1)^(k(k-1)/2) det K_(ann,cre).              (41.9e)
```

Thus both the determinant and its configuration sign originate in (41.2) and the
grading, rather than an external diagram convention. The implementation integrates
each fixed ordering chamber separately. It maps a unit cube to the simplex by
`t_1=beta x_1`, `t_2=t_1 x_2`, ..., and includes the generated Jacobian; the
external time occupies each of the `r+1` possible chambers. This avoids integrating
across a hidden time-ordering discontinuity.

## Construct an independent coefficient target

The graph-free comparator must not use (41.7). Write

```text
exp[-tH(lambda)]=sum_(r>=0) lambda^r E_r(t).               (41.9)
```

Differentiating (41.9) and matching coefficients constructs

```text
partial_t E_0=-H_0 E_0,                 E_0(0)=I,
partial_t E_r=-H_0 E_r-H_hyb E_(r-1),   E_r(0)=0.          (41.10)
```

One block-lower-triangular exponential with `-H_0` on the diagonal and `-H_hyb`
on the first subdiagonal returns all `E_0,...,E_4`; it never chooses a bath
pairing. For `0<tau<beta`, construct numerator coefficients

```text
N_r(tau)=sum_(a+b=r)
 Tr[E_a(beta-tau)d_up E_b(tau)d_up^dagger],
Z_r=Tr E_r(beta).                                        (41.11)
```

Let

```text
Q_r=-integral_0^beta exp(i omega_0 tau)N_r(tau)d tau.
```

Series division, rather than an assumed normalization, generates the Green
coefficients:

```text
sum_(a+b=r) Z_a G_b=Q_r,
G_r=(Q_r-sum_(a=1)^r Z_a G_(r-a))/Z_0.                    (41.12)
```

Bath-parity conjugation sends `lambda` to `-lambda` while leaving (41.3)
unchanged, so `G_1=G_3=0` is an additional target, not a discarded result.

The decisive common-target certificate is

```text
G_r^(determinant)=G_r^(block),       r=0,2,4,              (41.13)
```

within a declared quadrature and matrix-exponential error. Full diagonalization at
several real `lambda` values supplies a secondary reconstruction check against
`G_0+lambda^2G_2+lambda^4G_4` and its observed remainder; it cannot replace
(41.13).

## Evidence contract and refusal cases

Execution must return:

1. CAR and mode-reordering certificates for (41.4)--(41.5);
2. the generated hybridization function (41.6);
3. determinant/expanded-pairing equality through `k=2` and the general recurrence
   certificate (41.7)--(41.8);
4. block-target coefficients and odd-order zeros from (41.9)--(41.12);
5. equality (41.13) with separate integration and linear-algebra errors; and
6. complete graph, determinant, block-target, and observable-recovery costs.

The adapter refuses a non-CAR mode action, non-Hermitian Hamiltonian parameters,
zero partition function, unsupported complex-time boundary, unresolved numerical
error, or resource exhaustion. A nondiagonal interacting bath is outside `v1`; it
cannot be hidden inside a fitted `Delta`.

Failure of (41.13) with valid independent implementations rejects cross-domain
transfer. Equality supports the common semantics only for this finite equilibrium
impurity. The factorial-to-cubic statement supports contraction-layer leverage;
whole-observable leverage requires the complete cost receipt and may be rejected.

## Horizon and stop rule

The horizon is the frozen two-site bath, one interacting impurity orbital,
`beta=2`, one Matsubara Green function, and hybridization orders through four. It
excludes continuum-bath extrapolation, analytic continuation, Kondo-scale accuracy,
DMFT self-consistency, real-time contours, lattice thermodynamic limits, and phase
transitions.

Stop after the six receipts and refusals are classified. Additional bath sites,
temperatures, frequencies, or impurity observables cannot promote
`C_response-v1`; they require a later disposition and a named re-entry purpose.

## Execution and local disposition receipt

The public implementations are `fieldcalc.impurity` for the finite system and
`fieldcalc.impurity_expansion` for the isolated heavy determinant calculation;
their behavioral certificate is `tests/test_anderson_transfer.py`. The frozen
request constructs 64 Fock states and a block recurrence of dimension 320. With
12-point Gauss--Legendre integration it uses 25 sparse exponential actions and
returns

```text
max CAR residual = 0
Delta(i)          = -0.14222222222222222 i
G_0               = -0.453018350450290 i
G_1               = 0
G_2               = -0.005103533972002 i
G_3               = 0
G_4               =  0.004336966189266 i.                (41.14)
```

The graph-free truncated series differs from the independent Lehmann value by
`1.23e-10`, `1.40e-9`, and `2.99e-8` at `lambda=0.08`, `0.12`, and `0.20`,
respectively. Direct Lehmann values at `lambda` and `-lambda` agree exactly at
reported precision. These receipts support (41.4)--(41.6) and (41.9)--(41.12).

For a generic grade-three kernel, the CAR recurrence and determinant agree while
the receipt records six explicit pairing histories and nine kernel entries. The
action-factored route (41.9a)--(41.9e), evaluated with order-four simplex
quadrature, independently returns

```text
coefficient   |G_r^det-G_r^block|
G_0            3.28e-6
G_2            1.48e-5
G_4            6.51e-6.                                  (41.15)
```

The determinant route visits 5,588 simplex points and evaluates 194,368 retained
determinant cells representing 258,880 spin-admissible pairing histories. On the
same run environment it takes 18.72 seconds, while the 320-dimensional block route
with 25 sparse exponential actions takes 0.294 seconds. The wall times are
comparative single-run evidence; the cell/history counts are reproducible
structural costs.

The persistent test uses order-three quadrature as a compact sign/target
certificate (`47,016` determinant cells and maximum coefficient discrepancy below
`9e-4`). Equation (41.15) is the separately executed order-four evidence packet;
it is not imposed on every canonical test run.

Evidence `E41-det-transfer-v1` therefore has the following bounded disposition:

- **correctness, exact/error-bounded:** (41.9a)--(41.9e) generate the local and bath
  factors, and (41.13) holds through order four within (41.15);
- **transfer, reproduced:** unchanged `C_response-v1` fields admit the finite
  equilibrium impurity through adapter data, so this is one cross-domain transfer;
- **semantic compression, exact:** the determinant quotients the factorial bath
  pairing histories and can expand back to them;
- **complete-route leverage, comparative rejection:** at the frozen order and
  accuracy, time-simplex construction overwhelms contraction savings and is much
  slower than the block comparator; and
- **unresolved:** higher order, continuum baths, stochastic sampling, real time,
  thermodynamic limits, and any claim that determinant asymptotics eventually
  outweigh integration cost.

This closes node 41. More impurity parameters cannot change its disposition. Its
bounded consequence is incorporated in
[`V_response-1`](../results/observable-interaction-v1-disposition.md); the later
same-action and coherent-information benches are closed there as separate evidence.

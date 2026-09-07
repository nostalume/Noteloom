# Open-line quotient and analytic subset transfer

Status: scalar and fermionic open trees admit exact subset compression; nodes 29
and 30 consume them in characteristic amplitudes and finite detector measures,
while infrared completion and loops remain open

## Obstruction

The four-point regression has only three histories. With `N` labelled photons,
ordered singleton currents and pair contacts proliferate. A useful compiler must
evaluate their sum without constructing each ordered history, while retaining an
exact recovery map and Ward endpoint law.

## Generate the histories from action arity

The scalar-QED jet permits blocks

```text
{i}   one current insertion,
{i,j} one polarized contact insertion.          (27.1)
```

Consequently the ordered-history count is constructed by

```text
H_0=H_1=1,
H_N=NH_(N-1)+binom(N,2)H_(N-2),

m_(N,r)=N!/[2^r r!(N-2r)!],
h_(N,r)=m_(N,r)(N-r)!,
H_N=sum_r h_(N,r).                              (27.2)
```

The worldline Schwinger inverse

```text
K^(-1)=integral_0^infinity dT exp(-TK)
```

places all photon positions in one proper-time cube. Gaussian contraction turns
its multilinear coefficient into

```text
W_S(J,K)=[product_(i in S)z_i]
 exp(sum_i z_iJ_i+sum_(i<j)z_iz_jK_(ij)).       (27.3)
```

Choosing any `i in R` constructs the matching recurrence

```text
W_empty=1,
W_R=J_iW_(R-{i})
 +sum_(j in R-{i})K_(ij)W_(R-{i,j}).            (27.4)
```

It has involution-number complexity

```text
M_0=M_1=1,
M_N=M_(N-1)+(N-1)M_(N-2),
```

and recovers every ordered history by multiplying a matching with its `(N-r)!`
chamber multiplicity. For example,

```text
W_{1,2}=J_1J_2+K_12,
W_{1,2,3}=J_1J_2J_3+K_12J_3+K_13J_2+K_23J_1.
```

Replacing `epsilon_i` by `k_i` makes the current insertion a total derivative, so
the physical quotient becomes a worldline endpoint law before graph recovery.

## Integrate chambers into subset states

For an ordered block history `B_1,...,B_r`, define accumulated momenta and
Euclidean denominators

```text
q_0=p,
q_a=p+sum_(b<=a)sum_(i in B_b)k_i,
D_a=m^2+<q_a,q_a>.
```

Changing ordered positions to positive segment lengths `s_a` gives the exact
factorization

```text
integral_chamber dT d^r tau exp[-sum_(a=0)^rD_as_a]
 =product_(a=0)^r integral_0^infinity ds_a exp(-D_as_a)
 =product_(a=0)^rD_a^(-1).                     (27.5)
```

The action-generated transition and contact are

```text
G(q)=[m^2+<q,q>]^(-1),
V_i(q)=<2q+k_i,epsilon_i>,
C_(ij)=-2<epsilon_i,epsilon_j>.                 (27.6)
```

Their Ward laws follow from kinetic differences:

```text
V_i(q)|_(epsilon_i=k_i)=D(q+k_i)-D(q),

V_j(q+k_i)-V_j(q)=2<k_i,epsilon_j>
                 =-C_(ij)|_(epsilon_i=k_i).     (27.7)
```

For subset `S`, let `q_S=p+sum_(i in S)k_i`, `G_S=G(q_S)`. Shared accumulated
states then obey

```text
A_empty=G_empty,

A_S=G_S[
 sum_(i in S)V_i(q_(S-{i}))A_(S-{i})
 +sum_({i,j} subset S)C_(ij)A_(S-{i,j})].       (27.8)
```

Induction on `|S|` proves that `A_S` is the sum of all ordered singleton/pair
histories on `S`. At two photons, explicit telescoping gives the endpoint identity

```text
W_1A_{1,2}(p)=A_2(p)-A_2(p+k_1).                (27.9)
```

## Exact use and cost certificate

For the retained generic rational `N=4` Euclidean fixture:

```text
24 four-current histories
+36 one-contact histories
+ 6 two-contact histories
=66,

A_{1,2,3,4}^subset-A_{1,2,3,4}^histories=0.    (27.10)
```

The subset evaluator uses 16 states and

```text
E_N=N2^(N-1)+binom(N,2)2^(N-2)
```

transitions: `E_4=56`. Independent history evaluation repeats 216 event
applications. At `N=10`, 9,496 matching monomials recover 64,751,400 ordered
histories. These are exact construction counts, not asymptotic integration claims.

## Preserve order while merging fermion histories

Fermion vertices cannot enter the commutative matching kernel: changing their
order changes the Clifford product. Yet every history that has consumed the same
label subset `S` reaches the same momentum `q_S`. With node 05's exterior normal
form `N`, let the transition that appends label `i` last be

```text
T_(i|R)=N(C(epsilon_i))                         if R=empty,
T_(i|R)=N(C(epsilon_i)S(q_R))                  otherwise,

F_empty=1,  F_S=sum_(i in S) T_(i|S-{i}) star F_(S-{i}). (27.11)
```

This recurrence is forced by a disjoint partition, not commutation. Every ordering
of `S` has one last label `i`; deleting it leaves exactly one ordering counted by
`F_(S-{i})`, and left multiplication restores the original order. Hence

```text
F_S=sum_(pi in Perm(S))
 T_(pi_n|S-{pi_n}) star ... star T_(pi_1|empty). (27.12)
```

The graph layer therefore falls from `N N!` ordered steps to `N 2^(N-1)` subset
transitions. The algebra layer does not re-expand those states into matrices: in
dimension `d`, each state has at most `2^d` blade coefficients, with actual cost
set by the surviving sparse coefficient products.

Contracting label `a` uses the generated kinetic difference
`C(k_a)=K(q+k_a)-K(q)`. In adjacent insertion positions the factors `SK=KS=1`
cancel pairwise; retaining the two unmatched endpoints computes

```text
W_aF_S(p)
 =N(K(q_S)S(q_(S-{a}))) star F_(S-{a})(p)
  -F_(S-{a})(p+k_a) star N(S(p+k_a)K(p)).       (27.13)
```

Thus external shell projectors kill the same Ward image without enumerating its
positions. All four contractions have zero endpoint-identity residual in the
retained rational `d=3` fixture.

For four photons, `16` subset states and `32` transitions recover all `24`
orderings. Shared factor construction included, the grade route uses `1025`
products versus `2490`; one fresh isolated run took `0.0158 s` versus `0.0288 s`.
The subset/direct product counts for `N=1,...,5` are respectively
`(2,2), (37,37), (263,351), (1025,2490), (3317,18292)`. The crossover is real but
bounded: grade storage grows as `2^d`, subset states as `2^N`, and the check is an
exact Euclidean algebra fixture rather than a physical multiphoton event.

## Retained interface and boundary

```text
CompileOpenLine(action jet, labelled insertions, kinematics, budget)
 -> matching kernel + subset evaluator + history recovery
    + endpoint Ward certificate + operation counts
 | refusal(zero denominator, unsupported arity, or budget).

CompileFermionLine(kinetic factor, labelled vertices, frame, budget)
 -> exterior-valued subset states + ordered-history recovery
    + endpoint Ward certificate + complete product counts
 | refusal(characteristic denominator, frame, label, or budget).
```

The node demonstrates open-tree leverage: a complicated graph sum becomes a
dynamic program on physical accumulated subsets, and the exterior state preserves
fermionic order while merging histories. [Node 29](29-characteristic-scalar-amplitude.md)
constructs the characteristic scalar amplitude; [node 30](30-prepared-matter-event.md)
consumes the scalar/fermion outputs in detector measures without losing the bounded
cost gain. The exact evidence boundary is recorded in
`../results/open-tree-compiler-v1-disposition.md`. Inclusive soft cancellation and
loops remain outside this node.

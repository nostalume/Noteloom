# Open-line worldline quotient

Status: the scalar-line insertion family admits a supported matching-kernel
quotient and bounded evaluator; node 28 closes its generic Euclidean open-tree
integration boundary with exact subset transfer

## Capability and spine binding

Node 26 gives scalar QED a generated local interaction jet: a photon may meet a
scalar line singly through the current or in a pair through the contact operation.
Its four-point regression contains only three histories, so it cannot tell whether
physical transfer provides computational leverage when the number of insertions
grows.

- **Upstream anchor:** node 26's generated singleton/contact operations and node
  25's interpretation of internal propagation as transfer homotopy.
- **Bridge question:** can all ordered insertions on one scalar line be generated
  and evaluated without constructing each graph history?
- **Invariant target:** the tree-level scalar propagator dressed by `N` labelled
  photons, with the same on-shell Ward quotient and the same off-shell endpoint
  boundary.
- **Downstream effect:** determine whether the algebra compiler can hand a smaller
  semantic object to the graph/integral compiler.
- **Special resources:** scalar QED, one open scalar line, tree order, and the
  Gaussian free worldline measure.
- **Rejoin edge:** an exact matching recurrence, a history-recovery map, and a
  complete-cost boundary for the next analytic bench.

The horizon ends at integrand construction and exact combinatorial recovery. It
does not claim generic evaluation of the remaining proper-time integral, include
loops, or extend the result to fermions.

## Construct the graph family from the action arities

Let `S={1,...,N}` label the photon requests. Equation (26.4) permits only two local
events on the charged line:

```text
{i}       one current insertion carrying photon i;
{i,j}     one polarized contact insertion carrying photons i and j.    (27.1)
```

A graph history is therefore not introduced by drawing named diagrams. It is an
ordered partition of `S` into blocks of size one or two. If the first event is a
singleton, there are `N` choices and `H_(N-1)` continuations. If it is a pair,
there are `binom(N,2)` choices and `H_(N-2)` continuations. Evaluation on the same
label set constructs

```text
H_0=H_1=1,
H_N=N H_(N-1)+binom(N,2) H_(N-2).                 (27.2)
```

For a history with `r` contact pairs, first choose an unordered partial matching,
then order its `N-r` resulting events:

```text
m_(N,r)=N!/[2^r r! (N-2r)!],
h_(N,r)=m_(N,r)(N-r)!,
H_N=sum_(0<=r<=floor(N/2)) h_(N,r).               (27.3)
```

The factors have direct semantics: `2^r r!` forgets orientations and ordering of
the pairs, while `(N-r)!` restores propagation order. No symmetry factor is added
afterward.

The executable compiler gives:

| `N` | matching monomials `M_N` | ordered histories `H_N` | subset-state bound |
| ---: | ---: | ---: | ---: |
| 2 | 2 | 3 | 4 |
| 3 | 4 | 12 | 8 |
| 4 | 10 | 66 | 16 |
| 6 | 76 | 3,690 | 64 |
| 8 | 764 | 385,560 | 256 |
| 10 | 9,496 | 64,751,400 | 1,024 |
| 12 | 140,152 | 15,949,256,400 | 4,096 |

Thus the obstruction is calculated: repeated homotopy transfer preserves a tiny
local grammar but materializes an explosive number of its ordered histories.

## Construct one moduli object instead of ordering it first

Let the inverse scalar kinetic operator be represented, on a Euclidean positive
domain, by its proper-time identity

```text
K^(-1)=integral_(0)^infinity dT exp(-T K),
K integral_(0)^infinity dT exp(-T K)
  =[-exp(-T K)]_(0)^infinity=I.                  (27.4)
```

This computation constructs `T` as propagation length rather than importing it as
a diagram parameter. For a plane-wave photon `(k_i,epsilon_i)`, variation of the
connection along a path `x(tau)` supplies the insertion

```text
V_i=integral_0^T d tau_i
      epsilon_i dot x_dot(tau_i) exp(i k_i dot x(tau_i)).         (27.5)
```

Introduce a scalar tag `z_i` only to extract one copy of each labelled request:

```text
V_i=[z_i] integral_0^T d tau_i
      exp(i k_i dot x(tau_i)+z_i epsilon_i dot x_dot(tau_i)).     (27.6)
```

After the free path is separated from its endpoints, its measure is Gaussian.
The Gaussian cumulant identity is the theorem contract consumed here: connected
cumulants above degree two vanish. Consequently all dependence on the tags has the
constructed form

```text
W_S(J,K)
 =[product_(i in S) z_i]
   exp(sum_i z_i J_i+sum_(i<j) z_i z_j K_(ij)).                  (27.7)
```

`J_i` is the one-insertion contraction with the endpoint path and the other photon
momenta. `K_(ij)` is the two-insertion velocity contraction. To construct them,
take every external momentum incoming, so `p+p'+sum_i k_i=0`, and separate the
tag-independent exponent returned by Gaussian completion:

```text
E_0(tau)
 =-2 sum_i (p dot k_i) tau_i
  +sum_(i,j) [|tau_i-tau_j|/2-(tau_i+tau_j)/2]
               (k_i dot k_j),

J_i(tau)
 =2i epsilon_i dot p
  -i sum_j [sign(tau_i-tau_j)-1](epsilon_i dot k_j),

K_(ij)(tau)
 =2 delta(tau_i-tau_j)(epsilon_i dot epsilon_j),   i<j.          (27.8)
```

The factor two in `K_(ij)` combines the ordered `(i,j)` and `(j,i)` entries of the
Gaussian double sum. These expressions use only invariant momentum/polarization
pairings. In particular the pair kernel is supported exactly on coincidence and
therefore carries the local contact event rather than an unlabelled correction.
The full integrand is `exp(E_0) W_S(J,K)`.

The full domain is the single labelled cube `[0,T]^N`. Ordering is now geometry
inside that domain, not a prior graph-enumeration choice.

## Generate the multilinear coefficient by obstruction-free recursion

Fix the smallest label `i` in a nonempty subset `R`. A multilinear term can contain
`z_i` in exactly one of two ways:

```text
z_i J_i,
z_i z_j K_(ij) for one j in R-{i}.                               (27.9)
```

These cases are disjoint and exhaustive because the Gaussian exponent has tag
degree at most two. Removing the tags already consumed constructs the recurrence

```text
W_empty=1,
W_R=J_i W_(R-{i})
    +sum_(j in R-{i}) K_(ij) W_(R-{i,j}).                       (27.10)
```

This is the retained operation `evaluate_matching_kernel`. It accepts one-body
weights, a symmetric pair kernel, and a state budget. Memoizing by the remaining
label subset gives an upper bound of `2^N` states and `O(N 2^N)` arithmetic, after
`O(N^2)` pair-kernel construction. It refuses before evaluation when that declared
state bound exceeds the supplied budget.

Counting rather than evaluating (27.10) sets every weight to one and gives

```text
M_0=M_1=1,
M_N=M_(N-1)+(N-1)M_(N-2),                       (27.11)
```

the number of partial matchings. The first nontrivial outputs are calculated as

```text
W_{1,2}=J_1 J_2+K_12,                            (27.12)

W_{1,2,3}=J_1 J_2 J_3
          +K_12 J_3+K_13 J_2+K_23 J_1.           (27.13)
```

These are generated from the recurrence; neither the Compton answer nor a graph
list appears in the input.

## Recover every ordered history

Take a monomial of (27.7) containing `r` pair kernels. It defines a partial
matching with `N-r` propagation events. Its proper-time stratum has `(N-r)!` open
ordering chambers. Therefore the number of graph histories recovered from every
master monomial is

```text
sum_r m_(N,r)(N-r)!=H_N,                          (27.14)
```

which coincides term by term with the independently constructed action count
(27.3).

For `N=2`, `J_1 J_2` has the two chambers `tau_1<tau_2` and `tau_2<tau_1`; `K_12`
has the coincidence/contact stratum. It recovers exactly node 26's two exchanges
and one contact. For `N=3`, the all-single monomial has `3!=6` chambers, while each
of three pair monomials has `2!=2`, giving

```text
6+3(2)=12=H_3.                                   (27.15)
```

Thus the master kernel is not merely concise notation. It quotients propagation
ordering during construction and supplies an explicit recovery map when a graphwise
answer is requested.

## Preserve the physical quotient before graph recovery

Replace one polarization by its photon momentum in the same vertex operation:

```text
V_i[k_i,k_i]
 =integral_0^T d tau_i k_i dot x_dot exp(i k_i dot x)
 =(1/i)[exp(i k_i dot x(T))-exp(i k_i dot x(0))].                (27.16)
```

The Ward operation has become an endpoint map before any ordering chamber is
created. For an amputated on-shell scalar amplitude the endpoint terms vanish;
for an untruncated off-shell propagator they remain and record its endpoint charge.
This is the same physical/off-shell boundary found in nodes 25--26, now applied to
the whole insertion family at once.

A coincidence-supported pair kernel must be retained as a stratum, not sampled as
an ordinary measure-zero point in the cube. Dropping it would lose the contact
operation and break the recovery equality. The quotient object is therefore a
stratified integral kernel, not a smooth `N`-cube integrand.

## Compiler interface and algebra--graph bridge

The reusable handoff is now concrete:

```text
local U(1) obstruction
  -> algebra compiler generates event arities {singleton,pair}
     and the Ward endpoint law
  -> compile_open_line_quotient(N)
     generates matching strata and recovery multiplicities
  -> evaluate_matching_kernel(J,K,budget)
     folds their weights without ordered-history enumeration
  -> analytic evaluator integrates the stratified proper-time object
  -> optional chamber expansion recovers individual textbook graphs.           (27.17)
```

The algebra compiler supplies allowed operations and identities; the graph compiler
composes them; neither is discarded after verifying the amplitude. This is the
first retained bridge in the spine whose output changes construction complexity.

## Complete-route verdict

Supported gain:

- ordered integrand assembly falls from `H_N` graph histories to one stratified
  master object;
- its multilinear coefficient can be evaluated within `O(N 2^N)` arithmetic and
  `2^N` declared subset states instead of materializing `M_N` symbolic monomials;
- the Ward quotient is applied once as an endpoint operation before graph recovery;
  and
- the `N=2` and `N=3` recovery computations prove that contact and ordering data
  were compressed rather than deleted.

Unsupported gain:

- the remaining proper-time integral has dimension `N` and non-smooth/contact
  strata;
- exact analytic evaluation may force a chamber decomposition and recreate much of
  the ordering cost;
- naive continuous Monte Carlo misses coincidence-supported terms, while a
  stratified sampler still needs variance and error analysis; and
- no runtime or accuracy comparison for one physical observable has yet been run.

The result is therefore **combinatorial leverage in construction**, not a claim of
polynomial-time multiphoton amplitudes or complete predictive leverage.

## Supported frontier and next bench

Supported:

- the scalar-QED action arities generate ordered singleton/pair histories;
- Gaussian contraction quotients those histories into a partial-matching kernel;
- the matching recurrence is an executable reusable evaluator with a resource
  refusal;
- every ordered graph history is recovered by the stratum chamber count; and
- the global Ward operation agrees with the physical/off-shell boundary of the
  earlier spine.

Open:

- causal continuation and characteristic singularities outside the Euclidean
  denominator domain;
- a physical on-shell observable and its recovery cost;
- loop sewing and renormalization; and
- the fermionic Grassmann/Pfaffian extension.

Node 28 completes the declared `N=4` discriminating bench: it integrates each
proper-time chamber into a propagator chain, folds the chains over 16 photon-subset
states, and recovers the same exact dressed propagator as all 66 ordered histories.
This branch now stops at the scalar open-tree boundary.

## Materials and edges

- Node 25 supplies physical transfer and the off-shell endpoint interpretation.
- Node 26 supplies the generated scalar-QED event arities and `N=2` regression.
- `fieldcalc.worldline` owns the matching quotient and bounded evaluator.
- `computation/tests/test_worldline_quotient.py` owns recurrence, recovery-count,
  transfer, and refusal certificates.
- Node 28 consumes the quotient in an exact analytic use-level calculation.
- [Off-shell resolution and graph-geometry contracts](../sources/off-shell-resolution-contracts.md)
  bound the homotopy-transfer and worldline theorem inputs.

```text
25 transfer semantics + 26 U(1) action jet
  -> 27 open-line matching quotient
  -> 28 analytic subset transfer
  -> fermionic spin-transport discriminator.
```

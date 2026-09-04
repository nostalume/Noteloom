# N10t — Observable-Factored Response Compiler

Status: supported for separate integer spins two through five; the curvature
observable annihilates every lower N10r response layer, both constrained and
compensated routes compile to one boundary-selected operation `G_Q K_s`, and a
batched/fused execution contract is retained; the resulting leverage belongs to
observable factoring rather than either field presentation

Consumes: [N10r direct constrained Green generator](10r-direct-constrained-green.md),
[N10s preparation-selected sector](10s-prepared-response-sector.md),
[N10j generated curvature](10j-generated-curvature-compatibility.md), and
[N10k sourced curvature transport](10k-sourced-curvature-transport.md)

Computation: [observable response compiler](../computation/10t-observable-response-compiler/README.md)

Produces: an observable-visible layer theorem, a presentation-independent causal
response normal form, a reusable batch compiler, formal work comparisons, a fused
spectral implementation rule, and explicit scope/refusal boundaries

## Research contract

- **Upstream anchor:** N10s constructs a physical one-layer preparation but finds
  no advantage over the same prepared compensated route. It leaves open whether a
  repeated observable workload, rather than a carrier, exposes reusable work.
- **Bridge question:** which N10r response layers can change the gauge-invariant
  curvature, and can the observable be computed without constructing the complete
  field response for every source and query?
- **Invariant target:** the same boundary-selected curvature distribution and the
  same family of linear curvature functionals for both presentations.
- **Special resources:** flat constant-coefficient scalar Green operations,
  N10j's generated `K_s`, finite integer spin, and a batch of compact sources and
  curvature observables.
- **Internal benchmark:** derive visibility for every generated layer; normalize
  both response routes on the same source class; compile an `8`-source,
  `6`-observable workload for spins `2--5`; distinguish formal channel counts from
  active cost; and test a fused regularized spectral realization.
- **Horizon:** free flat scalar-wave dynamics and curvature-factorizing linear
  observables. A direct first-order curvature source theory, interactions, curved
  backgrounds, and measured runtime are outside this node.

## 1. Field-first inversion computes invisible layers

N10r constructs

```text
G_D=Q^(-1)f_s(B_s),
B_s=R_(s-1)A/Q,                                       (1.1)
```

on the harmonic carrier layers

```text
X_(s,l)=R_(s-1)X_(s-1,l),  l<s,
X_(s,s)=ker A.                                        (1.2)
```

The requested output is not the field representative. It is N10j's curvature
`K_s`. That operation was generated with two annihilators:

```text
K_s P=0,
K_s U=0.                                              (1.3)
```

The first is gauge annihilation; the second says that the chiral target ignores
the metric trace layer. N10n's projected raise is

```text
R_(s-1)=P-[1/(2s)]U A.                                (1.4)
```

Apply `K_s` to (1.4) on the same parameter:

```text
K_s R_(s-1)
 =K_sP-[1/(2s)]K_sUA
 =0.                                                   (1.5)
```

Every `l<s` layer in (1.2) begins with this raise. Therefore

```text
K_s X_(s,l)=0,  l<s.                                  (1.6)
```

For the remaining layer, `A X_(s,s)=0`, so

```text
B_s X_(s,s)=0,
f_s(0)=1.                                              (1.7)
```

Equations (1.5)--(1.7) construct the observable-visible quotient: exactly the top
transverse layer can change the curvature. This is stronger than observing a
two-dimensional shell rank, and it does not require constructing any layer
projector on the source.

## 2. The observable generates its own response normal form

Let `j` be an admissible constrained source. Constant-coefficient `K_s` commutes
with the boundary-selected scalar Green operation. From (1.1), calculate

```text
K_s G_D j
 =G_Q K_s f_s(B_s)j
 =G_Q f_s(0)K_sj
 =G_Q K_sj.                                            (2.1)
```

The second equality uses `K_sB_s=K_sR_(s-1)A/Q=0`; it is not a post-hoc deletion
of unwanted components.

Now take the corresponding full symmetric current `J`. N10e's inverse source
adapter has the form

```text
M_s^(-1)=I+U T times a spin-dependent scalar.          (2.2)
```

Using the second annihilator in (1.3), compute

```text
K_s M_s^(-1)J=K_sJ.                                   (2.3)
```

N10k's causal commutation then gives

```text
K_s G_F M_s^(-1)J
 =G_Q K_sM_s^(-1)J
 =G_Q K_sJ.                                            (2.4)
```

The constrained and compensated composites in (2.1) and (2.4) have the same
physical source class, boundary condition, and curvature target. Their common
normal form is the retained operation

```text
ObservableResponse_s(J)=G_Q K_sJ.                     (2.5)
```

Thus the complicated inverse is removed because the observable annihilates its
extra work, not because one field equation has been declared preferable.

## 3. Batch construction exposes what repetition can and cannot save

Let `J_i`, `i=1,...,N`, be compact sources and let the requested observables factor
through curvature:

```text
O_(i,a)=L_a(ObservableResponse_s(J_i)),
a=1,...,m.                                             (3.1)
```

The compiler constructs (2.5) once per source and caches it. The complete batch is

```text
for each J_i:
  C_i=G_Q K_sJ_i;
  return L_1(C_i),...,L_m(C_i).                        (3.2)
```

Consequently the curvature construction and Green work scale with `N`, while the
final functional evaluations scale with `Nm`. Increasing `m` does not create a
presentation advantage: both presentations cache the same `C_i`. Increasing `N`
does amortize the one-time compiler certificates and repeats whatever per-source
channel difference the chosen implementation actually has.

For the declared dense-carrier accounting,

```text
dim potential carrier =2s^2+2,
dim curvature carrier =4s+2,
dim top transverse layer=2s+1.                         (3.3)
```

On the executable workload `N=8`, `m=6`:

| spin | full N10r field work | potential Green channels | curvature Green channels | formal saving |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 216 | 80 | 80 | 0 |
| 3 | 512 | 160 | 112 | 48 |
| 4 | 1000 | 272 | 144 | 128 |
| 5 | 1728 | 416 | 176 | 240 |

“Full N10r work” multiplies its carrier-wide Green depth by harmonic carrier size
and source count. It is a rejected field-first route for this observable. The
curvature count improves the formal dense scalar propagation from spin three, as
N10k anticipated. It is not yet a runtime theorem. In particular, `2s+1` is a
pointwise dimension of the top source layer, not a proof of minimal curvature-image
storage and not a constructed global coordinate bundle. A baseline implementation
may consume the same compiler and receive the same reduction.

## 4. Fusion repairs an avoidable numerical obstruction

The algebraic rewrite `K_sG_Q=G_QK_s` does not imply that both sequential
implementations are equally stable. In a spectral realization, a naive
curvature-first route materializes an order-`s` multiplier before the order-two
Green denominator acts. The intermediate may be larger than the result by roughly
the denominator scale.

The compiler therefore retains the composite, rather than the commuting prose:

```text
FusedResponse_s(k)=boundary_multiplier(k) K_s(k).      (4.1)
```

For a regularized scalar proxy, one coefficient is

```text
k^s/(1+k^2).                                           (4.2)
```

At ordinary frequency `k=10`, field-first, curvature-first, and fused evaluations
coincide for spins `2--5`. At the floating-point stress value `k=10^80`, explicitly
forming `k^s` overflows for spins four and five, whereas evaluating the same ratio
as

```text
k^(s-2)/(1+k^(-2))                                    (4.3)
```

remains finite. This is a representation-order and numerical-range certificate,
not a claim that fusion removes the physical `k^(s-2)` regularity loss. It also does
not replace the distributional boundary prescription by an ordinary pointwise
division at `Q=0`.

## 5. Retained tool and global verdict

The generated interface is

```text
CompileCurvatureResponse(
  generated field response,
  generated curvature operation,
  boundary condition,
  compact sources,
  curvature functionals,
  implementation capability)
 -> observable-visible quotient,
    common response operation G_Q K_s,
    cached batch evaluator,
    fused implementation rule,
    equality/cost/stability certificates,
    refusal boundary.                                  (5.1)
```

Its global meaning is:

- **semantic compression is supported:** lower response layers are irrelevant to
  the named observable and the full field need not be solved;
- **computational leverage is bounded but real:** the compiled operation removes
  field-first Green depth and supports stable fusion; formal curvature-channel
  savings begin at spin three;
- **carrier preference is rejected:** every presentation compiles to (2.5), so the
  gain belongs to preparation/dynamics/observable factoring;
- **repeated observables are neutral after caching:** they reuse the result but do
  not distinguish presentations;
- **runtime and ultraviolet claims remain open:** they require an actual
  discretization, data layout, accuracy target, and measured conditioning.

The free batched-curvature branch now reaches its internal stop. Re-enter only for
an observable that does not factor through `K_s`, dynamics that no longer commutes
with it, or a concrete discretization whose measured costs can strengthen or reject
the formal channel comparison.

## Edges

- `N10r -> N10t`: pass the generated layer spectrum and full quotient inverse whose
  observable-visible part is compiled.
- `N10j/N10k -> N10t`: pass `K_s`, its annihilators, causal commutation, and the
  formal curvature-channel comparison.
- `N10s -> N10t`: pass the same-preparation cost refusal and the requirement that
  reuse be evaluated rather than presumed.
- `N10t -> global generative spine`: return the observable response compiler as the
  reusable object; close carrier-based free-curvature gain and expose noncommuting
  dynamics or measured discretization as the next meaningful re-entry.

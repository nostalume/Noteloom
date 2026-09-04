# N10i — Capability-Relative Presentation Selector

Status: supported bounded selector for three existing parity-paired integer-helicity
routes; N10j now supplies the generated higher-spin curvature-output packet, while
half-integer selection, curvature-first causal completion, and carrier-global
enumeration remain open
Consumes: [N4 direct chiral symbols](04-local-symbol-extension.md),
[N4a symmetric potential complex](04a-polynomial-complex-details.md),
[N4m completed integer-spin field machine](04m-finite-integer-spin-field-machine.md),
[N5 low-spin comparison](05-low-spin-comparison.md),
[N10 cost partial order](10-equivariant-obstruction-resolution.md), and
[N10h carrier-to-grammar boundary](10h-carrier-to-grammar.md)
Later revision: [N10j curvature compatibility](10j-generated-curvature-compatibility.md)
invokes this retained selector with its generated packet and owns the augmented
frontier
Computation: [bounded presentation selector](../computation/10i-capability-presentation-selector/README.md)
Produces: a hard capability filter, a resource-budget filter, a Pareto frontier,
and typed refusals when the worktable has no required comparison witness  
Construction-origin correction: [audit](../results/07-construction-origin-audit.md) —
the selection operation is generated, while the three candidate routes and their
construction traces are handwritten registry inputs

## Research contract

- **Obstruction:** N10h can derive and packetize an operator grammar only after a
  presentation is chosen, while a helicity fiber admits several presentations. Choosing one by
  familiarity would return the original hidden presumption.
- **Input:** one parity-paired massless integer-helicity fiber, a list of required
  outputs, and optional upper bounds on declared resource axes.
- **Invariant target:** every surviving route must recover the same
  `C_(+s) direct-sum C_(-s)` little-group fiber and every requested stronger
  output using witnesses already present in the worktable.
- **Construction:** exclude uncertified or over-budget routes first; compare the
  remaining complete routes componentwise; retain every nondominated route.
- **Internal benchmark:** distinguish realization-only, curvature-output,
  action/source/causal, and incompatible-budget requests at spins one through
  three without a scalar score.
- **Boundary:** the registry contains only the direct curvature, compressed
  symmetric-potential, and completed symmetric-potential routes. It neither
  enumerates new carriers nor proves global minimality.

## 1. Selection begins with an output, not with a carrier

For the same helicity pair, the present worktable supports three different
routes:

```text
direct chiral pair
  -> first-order curvature equation
  -> physical helicity kernel,

symmetric potential
  -> quadratic gauge complex
  -> quotient and screen restriction
  -> the same helicity pair,

completed symmetric potential
  -> pairing adapter and Euler operator
  -> admissible sources and causal response
  -> positive shell amplitude.
```

These arrows do not have the same codomain. A route that realizes the particle is
not thereby capable of coupling a conventional source, and a route with an action
is unnecessarily expensive when only physical cohomology is requested. The
selector therefore evaluates

```text
(physical fiber, required capabilities, resource budget, certificates)
  -> eligible routes
  -> Pareto frontier or refusal.                         (1.1)
```

Capabilities are hard predicates. Cost never compensates for a missing theorem.
This is the first correction to an ordinary optimization problem.

## 2. The route registry is constructed from existing witnesses

Fix `s>=1` and target `C_(+s) direct-sum C_(-s)`.

### 2.1 Parity-paired direct curvature

N4 constructs the two chiral carriers

```text
F_curv=Sym^(2s)(S) direct-sum Sym^(2s)(bar S)           (2.1)
```

and a first-order equation on each summand. Its nonzero-null kernel is the desired
pair of helicity lines. This route certifies a local equation and a gauge-invariant
curvature amplitude. It does **not** currently certify a quadratic action,
admissible-source adapter, or causal Green response in this worktable.

### 2.2 Compressed symmetric potential

N10 constructs the realization-only complex

```text
H_(s-1) --R_s--> ker T^2 subset Sym^s(V*)
          --pi_0 D_s--> H_s.                            (2.2)
```

N4a proves that its nonzero-null cohomology is the same helicity pair, and N10
proves that `pi_0D_s` has the same kernel as the uncompressed equation. The route
certifies a local potential and a gauge quotient. The compressed equation target
has no independently certified action or causal completion.

### 2.3 Completed symmetric potential

N4m retains the full equation target and constructs

```text
FieldSystem_s=(G_s,F_s,R_s,C_s,M_s),                    (2.3)
```

from which N4c/N4f/N4g/N4h supply the quadratic Euler operator, admissible-source
conversion, retarded/advanced response, and positive shell amplitude. This route
has more capability than (2.2), not a universally better presentation.

The original registry received a physical-shell potential/curvature isomorphism
only for `s=1` from N5:

```text
[A] |-> p wedge A,
F |-> [i_n F],       n dot p=1.                         (2.4)
```

For `s=3/2` and `s=2`, N5 initially proved only common-fiber equivalence and
explicitly left the local curvature map open. The selector therefore refused the
spin-two bridge rather than filling it by analogy with Maxwell. N10j now consumes
that refusal and returns a spin-indexed capability packet. When—and only when—the
packet's spin, minimal-degree, and multiplicity certificates match the request, the
registry adds the integer-spin curvature-output and physical-shell bridge
capabilities. The half-integer refusal is unchanged.

## 3. Cost is a partial order on complete routes

For one fixed request, attach the vector

```text
Cost = (
  maximum differential order,
  irreducible carrier slots,
  gauge/identity depth,
  physical recovery depth,
  source/action construction depth,
  observable recovery order,
  unexplained characteristic debt,
  raw component load).                                 (3.1)
```

The first seven entries record semantic construction; the final entry is a
secondary execution estimate. A route `A` dominates `B` exactly when every entry
of `Cost(A)` is no larger and at least one is smaller. No weights are supplied by
representation theory, so a request for a weighted score is refused.

The executable selector does not receive these depths as unexplained numbers. Each
route carries a construction trace: differential orders of its maps, multiplicity
of each invariant carrier layer, gauge/identity operations, physical recovery
operations, source/action operations, observable-recovery order, and any
unexplained characteristic strata. Equation (3.1) is computed by taking the
maximum order, summing multiplicities, and counting the corresponding semantic
operations. The trace is returned with the route so every cost entry can be
audited.

The raw loads are not guessed from components. Representation dimensions give

```text
direct pair:
  dim F_curv=4s+2,
  dim E_curv=8s,
  load=12s+2;

compressed potential:
  dim G_s=s^2,
  dim F_s=2s^2+2,
  dim H_s=(s+1)^2,
  load=4s^2+2s+3;

completed potential:
  load=dim G_s+2 dim F_s=5s^2+4.                        (3.2)
```

Here the direct equation target follows from
`Sym^(2s-1)(S) tensor bar S` and its conjugate. The potential dimensions follow
from the trace-level decompositions already used in N10. Thus the numerical axis
is derived from invariant carriers even though it estimates component storage.

Characteristic debt is zero for these registered realization routes because N4
and N4a account for their non-null and null strata; zero means “explained,” not
“no exceptional origin.” Missing action or recovery certificates are capability
failures and are never encoded as a finite cost.

## 4. The selector is a finite constructive operation

Let `R` be the bounded route registry and `C_req` the requested capability set.
The first filter constructs

```text
R_cap={r in R | C_req subset Capabilities(r)}.           (4.1)
```

For each budget entry `Cost_i<=b_i`, the second filter constructs

```text
R_budget={r in R_cap | Cost_i(r)<=b_i for every named i}. (4.2)
```

Finally return

```text
Frontier={r in R_budget |
          no r' in R_budget componentwise dominates r}. (4.3)
```

Equations (4.1)--(4.3) are directly executable comparisons on finite records. If
the final set is empty, the refusal lists separately:

- missing requested capabilities;
- missing worktable certificates;
- resource axes and exact overruns.

This makes failure useful: it identifies whether the next research node needs a
new mathematical map or merely a larger declared budget.

## 5. Bounded results

### 5.1 Realization-only spin two remains plural

For `s=2`, the decisive costs are

| Route | order | invariant slots | gauge depth | recovery depth | raw load |
| --- | ---: | ---: | ---: | ---: | ---: |
| direct curvature | 1 | 4 | 0 | 1 | 26 |
| compressed potential | 2 | 4 | 1 | 3 | 23 |

The direct route has lower order and no quotient; the compressed potential has
smaller raw carrier load. Neither dominates. The completed potential is dominated
because its extra action/source construction was not requested.

### 5.2 The realization-only crossing occurs after spin two

From (3.2), the direct load is smaller than the compressed-potential load when

```text
12s+2 < 4s^2+2s+3
iff 4s^2-10s+1>0.                                    (5.1)
```

For positive integer `s`, this first holds at `s=3`. At that point the direct
route is also no worse on every other declared realization axis, so it dominates
the two registered potential routes. This is a bounded presentation result, not a
theorem against unregistered carriers or a claim about source computation.

### 5.3 Stronger capability changes eligibility

For `s=2`, requiring

```text
quadratic action + admissible source + causal response   (5.2)
```

excludes both the direct and compressed routes. The completed potential machine
is the only certified survivor. This is why carrier selection must occur after
the output is named.

For `s=1`, requiring a gauge-invariant curvature output and the physical-shell
potential/curvature bridge retains the Maxwell routes by (2.4). At `s=2`, the same
request without an N10j packet still returns the original missing-witness refusal.
Passing N10j's generated degree-two packet admits both direct and compressed
potential routes and charges curvature recovery order `2` to the same-output
comparison. A request for a polynomial local inverse still refuses: N10j's
momentum-scaling calculation requires inverse degree `-s`.

Finally, at `s=2` the simultaneous budget

```text
maximum order <=1,
raw component load <=24                                (5.3)
```

has no solution: curvature violates the load bound (`26`), while both potentials
violate the order bound (`2`). The selector reports the split obstruction rather
than silently relaxing one constraint.

## 6. What this changes and what it does not

The representation-to-field spine is now executable through one further arrow:

```text
  physical helicity fiber
  -> capability and budget declaration
  -> certified presentation frontier or refusal       [N10i]
  -> carrier-derived, packetized grammar                [N10h]
  -> obstruction-generated equation/source machinery  [N10c--N10g]. (6.1)
```

The apparent order reversal between N10h and N10i is operational, not circular:
N10h first exposed the missing presentation input; N10i now supplies a selector
for that input, and a selected supported potential can re-enter N10h. A direct
curvature selection stops before N10h because the current grammar adapter is
bounded to two symmetric-potential families.

The selector does not yet compare half-integer direct and potential routes, because
their common-fiber statement lacks a local recovery map and a matched cost packet.
It also does not decide whether the direct curvature family can acquire action and
causal capabilities at lower total cost. Those are mathematical obligations, not
missing `if` branches.

N10j closes the integer-spin forward compatibility operation as a retained
generator. The next discriminating use is consequently downstream: apply its
returned `K_s` to N4m's sourced causal response, recover a gauge-invariant
curvature observable, and compare the complete route with a curvature-first causal
construction—or expose why the latter cannot be built with local source and Green
resources. Merely adding more budget weights or another rank check would not
change the spine.

## Edges

- `N4/N4a/N4m -> N10i`: pass the three certified routes and their carrier,
  equation, quotient, action, source, and causal capabilities.
- `N5 -> N10i`: pass the Maxwell physical-shell bridge and the explicit absence
  of a higher-spin local bridge.
- `N10 -> N10i`: pass the capability-relative cost vector and componentwise
  domination rule.
- `N10h -> N10i`: pass the label-only refusal and the need to choose an off-shell
  presentation before grammar generation.
- `N10i -> N10h/N10c--N10g`: a selected symmetric potential re-enters the retained
  grammar/residual toolchain; a direct curvature choice records a separate grammar
  obligation.
- `N10i -> N10j`: pass the typed higher-spin recovery refusal and retained selector
  operation. N10j generates the spin-indexed forward map, invokes the selector with
  that packet, and owns the revised frontier; no reverse graph edge is introduced.

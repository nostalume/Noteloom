# Off-shell resolution and physical transfer

Status: the semantic role of off-shell propagation is supported at the free-complex
and tree-transfer level; loop-level compression and tropical evaluation remain open

## Capability and spine binding

Nodes 19--24 treated an off-shell Green packet as the object to be completed and
then tested against an observable quotient. That route generated exact Ward and
external-ideal obstructions, but replacing the Green kernel by a reduced resolvent
would only move its inverse. This node asks the prior question:

```text
What operation does off-shell space perform before any integral is evaluated?
```

- **Upstream anchor:** node 05's local free complex, node 17's graph compositor,
  node 19's internal Ward closure, and node 24's failure of the bulk homotopy on a
  characteristic external channel.
- **Bridge question:** can off-shell propagation be reconstructed as a homotopy
  that transfers local interaction to physical cohomology, so graph and tropical
  methods act only after the unphysical resolution has been quotiented?
- **Invariant target:** the same on-shell amplitude or detector effect produced by
  the original local action.
- **Downstream effect:** replace graphs as primitive objects by generated transfer
  composites, identify where tropical geometry can lower their evaluation cost,
  or reject the route as another reformulation.
- **Special resources:** a contraction of the free complex on generic internal
  momentum strata, a supplied local interaction, and a finite coupling/loop budget.
- **Rejoin edge:** a typed physical-transfer compiler or a measured refusal showing
  that its construction costs no less than the existing packet route.

The research horizon includes the first nontrivial tree transfer and one loop-level
graph-moduli probe. It does not claim an all-order construction, convergence of the
perturbation series, or a general solution of Feynman integration.

## Construct virtuality as a composition defect

Let `K(p):V_p->E_p` be the free kinetic symbol and let physical external data obey

```text
K(k_i) u_i=0.                                      (25.1)
```

At a local vertex, a subset `S` of external inputs carries the summed momentum

```text
p_S=sum_(i in S) k_i.                              (25.2)
```

Let `u_S` be the output obtained by applying the supplied local vertex to those
same inputs. Equation (25.1) imposes no free equation on this partial output.
Direct evaluation produces the partial-composition defect

```text
omega_S=K(p_S) u_S.                                (25.3)
```

For a scalar, `K(p)=p^2-m^2`; even when every `k_i^2=m_i^2`, cross terms in
`p_S^2` make `K(p_S)` generically nonzero. On a complement where `K(p_S)` is
invertible, the Green operation `h(p_S)` is forced by the repair equation

```text
K(p_S) h(p_S) omega_S=omega_S.                     (25.4)
```

Thus an internal off-shell edge is not an additional physical state. It carries
the failure of a partial local composition to solve the free equation. When
`K(p_S)=0`, this complement disappears, `h(p_S)` develops a pole, and the residue
must factor through the newly physical intermediate channel. Virtuality is the
equation-of-motion defect of partial composition; a pole is the locus where that
defect becomes physical propagation.

## Construct the resolution rather than import a propagator

Assemble node 05's maps into the graded free complex `C_free` with differential
`d`. Its physical carrier is the relevant cohomology

```text
H=ker(d)/im(d).                                    (25.5)
```

Choose an inclusion `i:H->C_free`, projection `pi:C_free->H`, and a degree-minus-
one operation `h` only on the contractible internal complement. A valid contraction
must compute

```text
pi i=I_H,
d h+h d=I_C-i pi.                                 (25.6)
```

Evaluating the second identity on the same `c in C_free` gives

```text
c=i pi(c)+d h(c)+h d(c).                          (25.7)
```

The three terms have distinct semantics: physical cohomology, an exact/gauge or
equation descendant, and a chosen witness contracting the remaining defect. This
is the mathematical work performed by off-shell space. It is a nonminimal local
resolution in which the interaction can compose before the equation and gauge
quotients are taken.

Equation (25.6) also explains node 24's boundary failure. On a characteristic
momentum the physical cohomology is nonzero, so `I_C-i pi` is not the identity and
the internal contraction cannot be extended as `K^(-1)` through that channel.
Node 20's `Q^(-1)` refusal at `Q=0` is therefore structural, not a missing
prescription. External states must enter through `i` and physical observables
through `pi`; the bulk homotopy belongs only on contractible internal edges.

## Generate a graph as homotopy transfer

Let a supplied local interaction be encoded by the nonlinear operation

```text
F(a)=sum_(r>=2) ell_r(a,...,a)/r!,
d a+F(a)=0.                                       (25.8)
```

For physical seed `x in H`, seek an interacting lift `a[x] in C_free` with
`pi a=x` and the homotopy condition `h a=0`. Evaluate (25.7) on this same `a` and
substitute its equation:

```text
a
 =i pi(a)+d h(a)+h d(a)
 =i x-h F(a).                                     (25.9)
```

Equation (25.9) is the generated recursion. Starting with `a_0=i x`, iteration
constructs every correction:

```text
a_(n+1)=i x-h F(a_n).                             (25.10)
```

Projecting the original equation and using `pi d=0` leaves the physical equation

```text
F_H(x)=pi F(a[x])=0.                              (25.11)
```

Its homogeneous coefficients are the transferred physical interactions. For a
binary interaction only, the first correction is

```text
a[x]=i x-(1/2)h ell_2(i x,i x)+O(x^3).
```

Polarizing the cubic term of `F_H` generates the unnormalized tree composite

```text
T_3(x_1,x_2,x_3)
 =-sum_cyclic pi ell_2(i x_1,h ell_2(i x_2,i x_3)),             (25.12)
```

with the exact symmetry and Koszul coefficients inherited from the supplied
`ell_2` convention and polarization. No channel graph was an input. Every symbol
in (25.9)--(25.12) has now been constructed:

```text
external leg  -> i,
local vertex  -> ell_2,
internal edge -> h,
physical readout -> pi.
```

A tree graph is therefore syntax for one composite contributing to a transferred
physical operation. It is not the primitive physical process. The higher
homotopy identities and independence of admissible contraction choices are used
here as theorem contracts; the cited minimal-model results establish them under
their stated BV or differential-graded hypotheses. The node does not pretend that
the finite calculation (25.9) proves the full theorem.

This reclassifies the existing compiler boundary:

```text
node 05 algebra compiler
  -> constructs (C_free,d,H);

nodes 19--20 Green/Ward machinery
  -> proposes and certifies the internal contraction h;

graph compiler
  -> generates the composites defining ell_n^H;

observable compiler
  -> consumes ell_n^H, not a bare off-shell packet.             (25.13)
```

At tree level, the minimal physical products may admit recursion or a direct
boundary characterization. At loop level, homotopy transfer is indexed by general
Feynman graphs rather than trees, so semantic quotienting alone does not establish
computational leverage.

## Connect the transferred graphs to metric-graph geometry

After the physical/gauge contraction has been performed, attach an analytic kernel
to each remaining internal homotopy. In a Euclidean region where `Re K_e>0`, the
Schwinger identity computes

```text
1/K_e=integral_0^infinity exp(-alpha_e K_e) d alpha_e.          (25.14)
```

For a transferred graph `Gamma`, the positive parameters `alpha_e` form a metric-
graph cell

```text
M_Gamma=R_(>0)^(E(Gamma))/Aut(Gamma).             (25.15)
```

Ordinary graph polynomials and their kinematic data live on this cell. Tropical
methods replace polynomial competition by its polyhedral dominant regions, making
sector geometry and global sampling computable without enumerating every local
coordinate chart independently. Worldline methods similarly combine families of
edge insertions into a master moduli integral.

The order of operations is forced by semantics:

```text
local BV/free resolution
  -> homotopy transfer and gauge quotient
  -> physical decorated graph classes
  -> Schwinger/metric-graph cells
  -> tropical, worldline, or direct evaluator.                  (25.16)
```

Applying tropical dominance before the physical quotient is unsafe for the present
goal: gauge and gravity numerators can cancel between graph representatives, while
a dominant-monomial or positive sampling model need not preserve those signed
cancellations. This is a research inference and an explicit falsifier, not a theorem
imported from the tropical sources.

## Candidate generative interface

The obstruction above proposes the retained tool

```text
PhysicalTransfer(
  free complex and physical projection,
  supplied local interaction,
  admissible contraction grammar,
  coupling/loop/resource budget,
  observable target)

  -> transferred physical operations,
     canonical decorated graph classes,
     factorization boundaries,
     metric-graph cells,
     contraction/Ward certificates,
     anomaly or characteristic refusals,
     complete construction-cost record.                        (25.17)
```

The expected answer is not an input. The compiler evaluates `F(i x)` and its
nonphysical component `(I_C-i pi)F(i x)`. It may use a candidate `h` only when
(25.6) contracts that component on the declared internal domain. Characteristic
external data are projected rather than inverted.
At quantum order it must return any surviving BV/anomaly residual instead of
silently treating the tree contraction as a loop theorem.

Three different evaluation backends are now comparable on the same transferred
object:

- minimal-model or factorization recursion for physical composition;
- positive geometry when residues and boundaries determine a canonical form; and
- tropical/worldline evaluation on the remaining graph-moduli integral.

Loop-tree duality is a fourth evaluator that replaces loop-energy integration by
regularized forward limits, but its UV subtraction and prescription remain part of
the complete cost.

## Discriminating probes and stop conditions

The next probes are related by consumed outputs, not permission order:

```text
scalar--spin-one regression [completed in node 26]
  -> generate the two exchange transfers and local action jet
  -> recover both Ward quotients
  -> reject four-point computational leverage;

scalar--spin-one multiphoton probe [completed in node 27]
  -> quotient transfer trees into one matching kernel
  -> support combinatorial construction leverage
  -> leave stratified proper-time evaluation open;

scalar--spin-two transfer
  -> reuse the interface with node 20's contraction
  -> expose characteristic and gauge failures without a component propagator;

first quantum cell
  -> form quotient decorated one-loop classes
  -> compare direct, worldline, and tropical evaluation of the same observable.
```

Record for each route

```text
N_raw_history, N_physical_graph_class, N_integral_cell,
maximum intermediate expression size, transformation depth,
sampling variance/runtime, observable recovery cost, and failure residual.
```

The branch supports computational leverage only if it lowers the complete route
for the same observable and tolerance. Stop with a semantic result but reject the
compiler claim if it merely regenerates the textbook graph list, if constructing
`h` costs the original inverse, or if tropical evaluation improves a proxy while
recovery of the physical numerator restores the lost cost. A scalar-only success
does not support transfer to gauge or spin-two interactions.

## Supported frontier and open boundary

Supported now:

- virtuality is constructed as the kinetic defect of partial composition;
- an internal propagator is typed as a contraction witness on the nonphysical
  complement, not as a physical state;
- local interaction transfers to physical cohomology through graph-indexed
  composites such as (25.12);
- node 24's characteristic failure is reclassified as misuse of an internal
  contraction on an external cohomology channel; and
- tropical geometry belongs after physical transfer, where it can address graph-
  moduli enumeration and integration rather than gauge semantics.

Open:

- generate a contraction from node 05's full finite-spin complexes without
  importing a gauge-fixed propagator;
- prove or refuse the loop-level quantum/BV transfer required by the active model;
- determine whether physical quotienting before tropicalization reduces signed
  graph complexity in scalar--spin-one and scalar--spin-two examples;
- determine whether node 28's exact scalar open-line leverage survives fermionic
  spin transport, physical observable recovery, or loop sewing; and
- find whether positive geometry supplies a direct boundary generator for any
  admissible non-scalar sector rather than only a comparison formalism.

## Materials and edges

- [Off-shell resolution and graph-geometry contracts](../sources/off-shell-resolution-contracts.md)
  delimit the theorem inputs and computational claims.
- Node 05 supplies the local complex and physical cohomology.
- Nodes 17 and 19 supply the existing graph grammar and Ward-closed packet.
- Node 26 supplies the completed scalar--spin-one regression and its negative
  four-point cost verdict.
- Node 27 supplies the scalar-line matching quotient and its unresolved analytic
  cost boundary; node 28 closes that boundary for the generic Euclidean open tree.
- Node 20 supplies the off-characteristic Green contraction and its singular
  boundary.
- Node 24 supplies the external-ideal failure reinterpreted here.

```text
05 local complex + 17 graph grammar + 19/20 internal homotopy
  -> 25 off-shell resolution and physical transfer
  -> physical graph quotient
  -> tropical/worldline/positive-geometric probe
  -> same observable and complete-route verdict.
```

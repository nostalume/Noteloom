# Observable-return calculus across mechanics and fields

Status: exact linear projection calculus supported under its domain hypotheses;
it is a scope envelope, while node 17 owns the active spin-two exchange bench

## Obstruction and capability

The algebra-to-graph bridge is not mathematically unified merely because two
programs exchange a data object. The algebra compiler by itself constructs local
operations but not their repeated dynamical composition. A graph compiler by itself
can enumerate shapes while forgetting which compositions are physical, which
relations identify them, and which observable they serve.

The common capability is therefore:

> Given an algebra of physical operations, a supplied dynamical generator, a
> retained preparation/observable, and a resource budget, construct the
> irreducible excursions that leave the retained sector and return to it; then
> evaluate those excursions in the mechanical, quantum, field, or collective
> realization actually supplied.

This does not identify mechanics with field theory. It identifies one mathematical
operation that both consume.

## Common datum constructed from an observable request

Let `X` be the state or observable module used by the chosen realization. Supply:

```text
A = typed algebra of admissible operations and relations,
L = dynamical generator on X,
P = idempotent retaining the requested preparation/observable sector,
O = final readout on P X,
Q = 1-P.
```

The algebra can be Poisson, associative, star, or `Z_2`-graded. The generator can
act on states or on observables. These choices are typed; a Hamiltonian acting on
state vectors is not silently identified with its commutator or Poisson derivation.

Projecting `L` constructs four maps rather than importing a self-energy:

```text
L_P = P L P: P X -> P X,
L_Q = Q L Q: Q X -> Q X,
B   = Q L P: P X -> Q X,
C   = P L Q: Q X -> P X.
```

`B` is departure, `C` is return, and `L_Q` evolves an unresolved excursion. Only
for an orthogonal projection and a self-adjoint Hamiltonian is `C=B^dagger`.

## Resolvent construction on the same input

For `eta in P X`, solve

```text
(z-L)(u+v)=eta,  u in P X,  v in Q X.
```

Applying `P` and `Q` computes

```text
(z-L_P)u-Cv=eta,
-Bu+(z-L_Q)v=0.
```

When `R_Q(z)=(z-L_Q)^(-1)` exists on the required domain, the second equality gives

```text
v=R_Q(z) B u.
```

Substitution into the first equality, on that same `u`, gives

```text
[z-L_P-Sigma_P(z)]u=eta,
Sigma_P(z)=C R_Q(z) B,
P(z-L)^(-1)P=[z-L_P-Sigma_P(z)]^(-1)P.
```

`Sigma_P` is the **irreducible observable return**: it leaves `P X`, evolves
entirely in `Q X`, and returns once. The equality is exact but not automatically
cheap because `R_Q` may retain the original difficulty.

## Time construction and the same return

For `dot(x)=Lx`, write `x=u+v`. Projection gives

```text
dot(u)=L_P u+C v,
dot(v)=B u+L_Q v.
```

Variation of constants evaluates the second equation:

```text
v(t)=exp(t L_Q)v(0)
     +integral_0^t exp((t-s)L_Q)B u(s) d s.
```

Substituting this constructed `v(t)` produces

```text
dot(u)(t)=L_P u(t)+C exp(t L_Q)v(0)
  +integral_0^t K_P(t-s)u(s) d s,
K_P(t)=C exp(t L_Q)B.
```

The Laplace transform of `K_P` is `Sigma_P` wherever both constructions are
defined. Resolvent correction and memory are therefore two evaluations of the same
departure--unresolved-evolution--return composite, not an analogy between separate
formulas.

For the Hamiltonian convention `i dot(x)=H x`, repeat the projection with
`L=H`. If `H` is self-adjoint and `P` is orthogonal, then `C=B^dagger`; spectral
resolution of `H_Q=QHQ` constructs the positive measure

```text
M_B(Delta)=B^dagger E_(H_Q)(Delta)B,
Sigma_P(z)=integral (z-lambda)^(-1) dM_B(lambda),
K_P(t)=B^dagger exp(-i t H_Q)B
      =integral exp(-i t lambda) dM_B(lambda).
```

The earlier semigroup formula is recovered by taking its generator to be `-iH`.
A general Liouvillian or nonorthogonal coarse-graining need not yield a positive
measure; the return kernel survives, positivity may not. The convention is part of
the evaluator rather than a suppressed factor.

## How perturbative graphs are generated

Suppose the retained and unresolved sectors are invariant under a reference
generator `L_0`, and supply an interaction `V`:

```text
L=L_0+g V,
Q L_0 P=P L_0 Q=0.
```

Then direct projection computes

```text
B=g B_1,  B_1=Q V P,
C=g C_1,  C_1=P V Q,
L_Q=L_(Q,0)+g W,  W=Q V Q.
```

Put `R_0(z)=(z-L_(Q,0))^(-1)`. In a convergent Neumann domain, or as a declared
formal series,

```text
R_Q(z)
  =[z-L_(Q,0)-gW]^(-1)
  =sum_(n>=0) g^n (R_0(z)W)^n R_0(z).
```

Consequently the irreducible return is generated as

```text
Sigma_P(z)
  =sum_(n>=0) g^(n+2)
     C_1 (R_0(z)W)^n R_0(z) B_1.
```

Every coefficient is an ordered excursion graph:

```text
P -> B_1 -> Q -> R_0 -> (W -> R_0)^n -> C_1 -> P.
```

This formula constructs the connection between the paper's order-`g` departure
and its order-`g^2` self-energy. It also exposes what higher order means before any
Feynman diagram is drawn.

When `V` is a polynomial field operation and the reference field state is
quasifree, evaluation of each ordered operator word generates Wick contraction
histories. Quotienting those histories by the typed symmetry action produces the
colored Feynman graphs of node 17. Thus a QFT graph is a **refinement of an
observable-return excursion** by field ports, pairings, parity, and spacetime or
momentum kernels. The graph compiler is not appended after the algebra compiler;
it is the free compositional completion of the operations that the algebra compiler
has typed and reduced.

## Mathematical compiler factorization

The retained construction has three mathematical layers:

```text
Alg(A)
  = colors, generators, grading, relations, normal forms;

Diag(Alg(A))
  = tensor/composition/contraction diagrams generated from Alg(A),
    quotiented by graph isomorphism and the certified relations;

Ev_R: Diag(Alg(A)) -> End(X_R)
  = evaluation in a declared realization R.
```

The algebra compiler constructs `Alg(A)`. The graph compiler constructs bounded
morphisms in `Diag(Alg(A))`. The mechanical, quantum, or field backend supplies
`Ev_R`. Correctness requires

```text
Ev_R(Normalize(D))=Ev_R(D)
```

on every admitted diagram `D`. This equality is the semantic-coincidence
certificate connecting algebraic reduction to graph evaluation.

## Realizations, common structure, and real differences

| Regime | Algebra and generator | Retained sector | Generated diagrams | Extra obligation |
| --- | --- | --- | --- | --- |
| classical mechanics | Poisson algebra, `L_H f={f,H}` | selected functions or coarse variables | time-ordered words/rooted response trees | control of nonlinear flow and projection error |
| quantum mechanics | operator/star algebra; `H` on states or `-i[H,-]` on observables | bound, prepared, or measurement sector | transition paths and irreducible returns | spectral domains, normalization, continuum boundaries |
| quantum field theory | graded field algebra with CCR/CAR and local vertices | prepared cyclic/Fock sector and detector | port-refined Wick/Feynman graphs | distributions, regularization, renormalization, asymptotic states |
| collective dynamics | microscopic observable algebra and Liouvillian | slow/conserved observables | memory diagrams and effective-kernel expansions | scale separation, decay of memory, noise/fluctuation data |

The common object is `C f(L_Q) B` relative to `(L,P,O)`, together with its
perturbative diagram expansion. Classical response trees are not declared to have
fermion loops; field graphs are not reduced to particle trajectories. They are
different admissible sublanguages and evaluators of the same typed composition
calculus.

This also clarifies the field--particle relation. A mechanical Hamiltonian can be a
selected sector/effective representative of a field generator when a recovery map
and error are supplied. The return calculus compares their responses on the same
`P` and `O`; it does not assert that first and second quantization are identical.

## What is and is not unified

The calculus unifies:

- exact projection, departure, memory, and self-energy constructions;
- perturbative composition and coupling-order bookkeeping;
- early use of symmetry, gauge quotients, conserved quantities, and observable
  annihilators;
- reuse of one irreducible return in bound-resolvent, finite-time, and continuum
  evaluations when their analytic hypotheses hold;
- a common whole-route cost audit and refusal language.

It does not unify or automatically solve:

- the discovery of a useful `P`, interaction, hidden algebra, or collective
  variable;
- classical Poisson, quantum commutator, and graded field relations into one
  interchangeable algebra;
- radial bound spectra, Feynman integrals, renormalization, long-time kinetics, or
  scattering-state construction;
- nonperturbative phenomena invisible to the selected reference and expansion;
- positivity outside the self-adjoint orthogonal-projection setting.

The framework is therefore a generative response calculus, not a universal theory
of dynamics.

## Research horizon and active consumer

This node records the common mathematical envelope; it does not authorize a broad
cross-regime implementation. The oscillator-network comparison, classical rooted
trees, mixed Gaussian signs, and Yukawa graphs are parked because each could become
an independent formalism exercise before the previous field-equation algebra has
changed a calculation.

The sole active consumer is node 17's spin-two exchange bench. Its first probe
constructs a conserved traceful source and proves that the generated source adapter
changes the internal edge. Its local transfer then uses scalar on-shell dynamics to
generate a conserved vertex family and a graph quotient to produce three labelled
tree orbits. The return calculus supplies only the two-vertex excursion shape; the
field compiler supplies the edge normal form, the matter input supplies its
improvement parameter, and the graph layer supplies the inequivalent compositions.

The generated tree kernel has now been evaluated at fixed kinematics and matches
the component-propagator route after its declared pairing normalization. Its full
construction is not cheaper at one channel, so this establishes connection but not
computational leverage. Re-enter only with a bounded multi-history request whose
orbit quotient or repeated algebra can change total work. Stop with a formal-
unification verdict if that request merely renames standard Feynman expansion.

## Materials, edges, and boundary

- Nodes 09 and 11 supply the projected resolvent and positive visible-measure
  constructions.
- Node 10 and `sources/observable-dynamics-contracts.md` supply the exact-memory
  boundary and warn that orthogonal dynamics may retain full cost.
- Nodes 13 and 14 supply typed algebra generation and residual repair.
- `sources/field-mechanics-variation-contracts.md` bounds the field-to-mechanical
  effective reduction.

Edges:

```text
09 projected response + 10 collective memory + 11 visible measure
  + 13/14 generated algebra
  -> 18 observable-return calculus
  -> 17 field-port graph refinement
  -> 16/12 observable transform and certified window.
```

The open boundary is a checked evaluation functor for each admitted regime and a
complete-route comparison showing whether quotienting before evaluation is cheaper
than the corresponding direct or textbook construction.

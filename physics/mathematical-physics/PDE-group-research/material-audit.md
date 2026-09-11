# Original source-note audit

## Scope and revision boundary

This is a located audit of the original mathematical-physics source notes, not a
verdict on the present PDE-group worktable or its implemented capabilities. The
findings and line locators below refer to these Git objects:

| Source owner | Git blob | Last-modifying commit |
| --- | --- | --- |
| `physics/mathematical-physics/functional-and-spectral-methods.typ` | `dfa70950e10c8d66c947e1783c7ef01a614b8e40` | `bce47ffaf3cbc0f635eae381420fc5c38ef0c642` |
| `physics/mathematical-physics/differential-geometry.typ` | `2def606481470ce4c18468cd9cfcfdc8db203ab7` | `bce47ffaf3cbc0f635eae381420fc5c38ef0c642` |
| `physics/mathematical-physics/category-and-homology.typ` | `ee98449f2468d750119225a1df81a9d053dcfe9e` | `bce47ffaf3cbc0f635eae381420fc5c38ef0c642` |
| `physics/mathematical-physics/homology.typ` | `3053476761beca3a5854faf2a820e0a61586a447` | `bce47ffaf3cbc0f635eae381420fc5c38ef0c642` |
| `physics/mathematical-physics/homology.pdf` | `55879a14d8f33f778a97b141f5431df1cf11ddf9` | `8980ab9d8d216e3c6ca0a9853b3c7b78aca27e58` |

The PDF is only a rendered projection of `homology.typ`, not independent
evidence. Later worktable constructions are owned by the research graph and nodes;
they do not retroactively change this source-note audit.

## Verdict on the audited notes

At those revisions, the notes contain most raw ingredients for the forward
direction: unbounded operators, spectral resolution, separation of variables,
classical special functions, vector fields, Lie brackets, naturality, and
kernels/quotients. They do not yet define the object preserved between
representation decomposition and differential-equation decomposition. Several
analytic claims also need repair before they can certify a machine output.

This audit leaves the source notes untouched. It states what may be consumed from
those pinned revisions and which claims require independent repair or theorem
contracts.

## `functional-and-spectral-methods.typ`

### Reusable material

- Lines 347–359 identify operator domains, closed graphs, adjoints, and the need to
  distinguish symmetric from self-adjoint operators.  This is the correct analytic
  region for the machine's domain certificate.
- Lines 361–387 aim at functional calculus, spectral measures, multiplication
  models, resolvents, and Green functions.  These are the right recovery objects,
  especially once attached to a cyclic vector or observable.
- Lines 390–486 connect translation representations, the generator `∂x`, Fourier
  decomposition, resolvents, Laplace transforms, and semigroups.  This is already a
  small forward representation-to-operator example.
- Lines 488–763 develop separation of variables and hypergeometric-type equations.
  Line 763 contains a decisive insight: the associated Legendre factor indexed by
  `m` is not the complete orthogonal decomposition until the azimuthal factor is
  restored.  The first benchmark makes this observation structural.
- Lines 829–914 identify gauge/conjugation and shift relations such as
  `ψ⁻¹Dψ = D + λ`, including Euler operators and generalized eigenfunction chains.
  These are seeds of the inverse factorization analyzer.
- Lines 1064–1098 derive Bessel recurrences from a generating function and shift
  operators.  These are reusable intertwiners, but not yet a recovered group.

### Claims requiring repair before reuse

- Line 359 concludes self-adjointness from symmetry/closure.  A densely defined
  symmetric operator is closable, but its closure need not be self-adjoint;
  essential self-adjointness or compatible deficiency data are additional
  obligations.
- Lines 361–378 blend continuous functional calculus, a cyclic spectral model, and
  projection-valued measures without stating the hypotheses or the role of the
  chosen vector.  These should become theorem contracts for a self-adjoint (or
  bounded normal) operator, with cyclic and non-cyclic cases separated.
- Line 452 treats broad Dirichlet/Neumann/Robin-looking conditions as though they
  automatically define a self-adjoint derivative operator.  The boundary form and
  maximal domain must be computed for the particular differential expression;
  conditions appropriate to first- and second-order operators differ.
- Line 787 says an integral operator is compact in general.  Compactness depends on
  kernel, spaces, and domain; a Volterra operator on a bounded interval is a useful
  benchmark, not a universal rule.
- Line 810 infers unrestricted Neumann expansion from zero spectrum.  Convergence
  needs an operator topology and a norm/spectral-radius condition; quasinilpotence
  alone does not justify every displayed manipulation without a bounded setting.
- Several Rodrigues/Legendre/Bessel calculations change symbols or signs between
  steps.  They are valuable derivation probes but need exact residual checks before
  promotion.

### Missing bridge

The note often moves from `Dψ=λψ` to a basis or recurrence, but it does not record:

```text
which group/algebra acts;
which representation space carries the action;
which enveloping-algebra element realizes D;
which domain and boundary data make the realization analytic;
which preparation/observable is preserved by the decomposition;
whether the recurrence closes to a Lie algebra or only intertwines a family.
```

Those fields are now mandatory in `BridgePackage`.

## `differential-geometry.typ`

### Reusable material

- Lines 33–128 construct vector fields, directional derivatives, and a commutator.
  This supplies the local differential language for infinitesimal actions.
- Lines 200 onward construct differential forms and exterior differentiation.
  The homogeneous-bundle node now consumes this as the local definition of the
  graded arrow `d`; adjoints, Hodge theory, induced representations, and the
  Casimir realization remain theorem contracts outside the local note.

### Missing bridge

The note does not yet construct a Lie-group action, fundamental vector fields,
homogeneous space `G/K`, invariant measure, Laplace–Beltrami operator, or Casimir
realization.  Consequently the phrase “Lie derivative” near line 120 should not be
used as a representation certificate.  The worktable's homogeneous-bundle
calculus supplies the missing representation object without silently attributing
it to the original note.

## `category-and-homology.typ`

### Reusable material

- Lines 15–279 develop morphisms, functors, naturality, and a Yoneda-style view of
  objects through their relations.  This supports the central idea that the two
  routes are compared by explicit maps rather than by matching names.
- Lines 286–508 develop kernels, cokernels, exactness, and derived-functor
  motivation.  These may later encode compatibility and obstruction spaces.

### Boundary

This is currently language, not a machine.  No functor between a category of
representation packages and a category of analytic differential problems is yet
constructed, and the inverse is not an ordinary inverse functor.  Line 244 should
say **natural isomorphism** when all components of a natural transformation are
isomorphisms.

## `homology.typ` and `homology.pdf`

The Typst note is a cleaner compact treatment of presheaves, Yoneda, abelian
categories, and chain complexes.  The PDF appears to be its rendered artifact and
is not independent evidence.  Its kernel/image and chain-complex language is now
consumed by the representation-wise de Rham complex in the homogeneous-bundle
node.  Derived-functor and sheaf machinery remains parked until a concrete
deformation, localization, or obstruction calculation consumes it.

## Bibliographies

Both local `.bib` files currently contain the same placeholder entry unrelated to
the mathematical content.  They provide no evidence for the present research
question.  The authoritative starting sources are tracked separately in
[sources.md](sources.md) until the manuscript chooses a citation format.

## Immediate reconstruction

The existing chapter order suggests a progression from spaces to operators to
special functions.  The research machine should instead organize those components
around a semantic invariant:

```text
(representation, chosen dynamics, analytic realization, preparation, observable)
  -> symmetry-resolved sector
  -> reduced operator and solution transform
  -> recovery of the same observable.
```

In the reverse direction, failed bracket closure, missing boundary invariance, or
non-unique global integration is information returned by the constructor, not a
gap to cover with another special-function derivation.

# Research-Spine Audit: Readability, Construction, Computation, Simplicity

Status: current audit of `N1` through `N4c`; supersedes the earlier repair log  
Scope: the research worktable, not the unchanged Typst manuscript

## Audit question

Does the present route from Poincare symmetry to field equations remain readable,
internally constructed, verifiable as semantic computation, and simpler than the
component-heavy route it replaces?

The four criteria are distinct:

| Criterion | Passing evidence | Failure signal |
| --- | --- | --- |
| Readability | each object is introduced by the need that constructs it; notation has one local meaning; incoming and outgoing edges are visible | long branch changes, unexplained symbols, name collisions, or repeated proofs whose ownership is unclear |
| Constructivism | capability/obstruction -> typed object -> operation -> witness -> consequence | a named theorem, group, quotient, or matrix property performs an unexposed logical step |
| Computability | every deduction can be evaluated on a common input; heavy work has a reproducible witness | equation asserted from analogy, prospective “method” inside a supported node, or numerical output treated as proof |
| Simplicity | few semantic transformations, one owner for each proof, components used only as bounded checks | duplicated bridges, relabeling work as abstraction, or extra files/notation without a new result |

Line count is not itself a defect, but it exposes where a reader must retain too
many active objects. N2 remains the largest node at about 980 lines; N3c was
reduced from 350 to about 130 lines and N4a from 746 to about 650.

## Node-level disposition

| Region | Readability | Constructivism | Computability | Simplicity | Disposition |
| --- | --- | --- | --- | --- | --- |
| `N1` | strong | adequate for a determination boundary | adequate; counterexamples and scope checks are explicit | strong | retain |
| `N2` | adequate after route clarification | strong overall; theorem contracts are typed | strong locally | dense but one conceptual three-space comparison | route map now marks Sections 1--4 as primary and group functions as optional |
| `N2a/N2b` | strong | strong; stabilizers, Hodge split, spin cover, and restriction maps arise from obstructions | strong invariant witnesses with bounded basis checks | strong | retain as the model style |
| `N3` | strong | strong associated-bundle and quotient construction | adequate; analytic completion is honestly bounded | strong by itself | retain as sole owner of the universal bridge |
| `N3c` | strong as a bounded companion | consumes rather than repeats N3 | owns analytic/computation obligations only | strong | resolved |
| `N3a/N3b` | adequate to strong | strong low-spin constructions | adequate invariant checks | justified as concrete falsifiers of the universal bridge | retain; make them sole owners of vector derivations |
| `N4` | strong | strong; natural maps and exact contraction replace components | strong all-rank deduction | strong | retain as the readable main theorem |
| `N4a` | adequate after ownership reduction | strong fixed-data criterion and bosonic screen proof | strong; independent rank check remains secondary | vector proofs now consumed through a compact result table | resolved |
| `N4b` | strong | screen Clifford maps and kernel lines now constructed internally | all-rank algebra plus finite-rank executable check | `Slash_p` is distinct from little group `K_k` | resolved |
| `N4c` | strong as an audit | Bianchi identities supported; adjoint/action claims correctly developing | invariant reductions are short | Euler operators use `E_B,E_F` | continue the variational bridge |

## High-impact findings

### `RA-01` — `K_k` has two incompatible types

Throughout `N2/N3/N4a`, `K_k` is the little group fixing momentum `k`. Earlier
N4b reused `K` for Clifford contraction and N4c reused it for an Euler operator.
These objects have different domains and semantic jobs; the collision made correct
equations hard to type by inspection.

Resolution: `K_k` is reserved for the little group; N4b uses `Slash_p`, and N4c
uses `Euler(p)`, `E_B`, and `E_F`.

### `RA-02` — N3 and N3c duplicate the universal bridge

Both files construct the associated bundle, the standard-fiber intertwiner, boost
independence, the global Poincare map, and the gauge subquotient. This is not an
independent check: it is nearly the same semantic route written twice.

Resolution: N3 remains the proof owner. N3c now contains only analytic completion,
computability, and route-cost obligations. Git history preserves its earlier form.

### `RA-03` — N4a repeats the low-spin witnesses

N4a Section 7 rederives the massive vector and Maxwell-potential symbols already
constructed in N3a/N3b. Their role in N4a is to test the four obstruction classes,
but repeating the derivations hides that role.

Resolution: the repeated algebra is replaced by a compact obstruction-result
table. N3a/N3b own the computations; N4a consumes their outcomes.

### `RA-04` — N2 changes semantic branch too many times without a return map

N2 constructs momentum, orbit, stabilizer, measure, physical Hilbert space,
covariant fields, regular group functions, and coefficient group functions. Each
step is locally motivated, but a reader must traverse the entire group-function
branch before recovering the primary particle-to-field edge near the end.

Resolution: one file remains because the three-space distinction is one conceptual
question. A route map now marks Sections 1--4 as primary, Section 5 as optional,
and the return to the field bridge explicitly. Further shortening is not justified
without removing a distinct construction.

### `RA-05` — the screen Clifford kernel is not yet internally constructed

N4b constructs the intrinsic target

```text
H_n(Q_k,W_k)=ker Gamma_Q,
```

but then says that the two-dimensional Clifford relations make one isotropic
screen gamma map annihilate `w_+` and the other annihilate `w_-`. This is the
decisive step producing helicities `+-(n+1/2)`, yet the kernel lines and their
weights are not evaluated from the previously constructed Clifford module on a
common input.

Resolution: N4b now constructs the oriented isotropic screen lines, proves the two
restricted Clifford maps are nonzero rank-one nilpotents with distinct kernels,
identifies their rotation weights, and evaluates `Gamma_Q r=0` on a common
polynomial. No matrix is used in the derivation.

### `RA-06` — executable checks are reproducible but numerically weaker than their inputs

The N4a/N4b scripts use integer or half-integer matrices but floating-point Gaussian
elimination at tolerance `1e-9`. This is acceptable as independent low-rank
evidence because invariant all-rank proofs own the claims. It is not ideal as a
future regression oracle: rank decisions could become tolerance-sensitive as
degree grows, and the README files do not record a Node runtime version.

Disposition: do not expand the current checks. When they are next modified, use
exact rational elimination or restrict the declared rank range, and record the
runtime version. No computation rewrite is required for the supported theorems.

### `RA-07` — the manuscript remains a separate readability debt

The nodes now contain a clearer argument than
`physics/quantum-mechanics/relativistic-representations.typ`, but the manuscript has
deliberately not been rewritten. Research-node readability does not imply reader
readability of the final note.

Disposition: do not synthesize yet. The action bridge and the N4b screen gap should
close first; afterward the manuscript should consume only supported node outputs,
not reproduce the research graph or its audit history.

## Supported philosophical result

The spine has genuinely reduced computation:

- little-group quotients replace polarization component elimination;
- Hodge and spinor functors replace repeated Lorentz-generator tables;
- exact sequences replace monomial kernel counts;
- polynomial divisibility replaces gauge-component solving;
- Bianchi operator identities replace rank-by-rank action variations.

This is semantic reduction rather than hidden expansion. The identified
duplication, notation collision, and screen-Clifford gap are resolved. Remaining
boundaries are the variational adjoint construction, optional exact-regression
hardening, analytic completion, and eventual manuscript synthesis.

## Available next node

The next scientific frontier is the N4c variational bridge, but its first
bounded output should be narrower than “prove the action”:

```text
input:
  constrained bosonic and fermionic carriers,
  Lorentz/Dirac real structures,
  spacetime compact-support boundary convention;

construct:
  invariant fiber pairings,
  P^dagger=A, U^dagger=T, Y^dagger=Gamma,
  formally adjoint Euler candidates E_B,E_F;

output:
  exact adjoint algebra and the obstruction, if any, to self-adjointness.
```

The trace-reversal coefficients should then be solved from this algebra together
with the constrained Noether identity, rather than imported from the named
Fronsdal actions.

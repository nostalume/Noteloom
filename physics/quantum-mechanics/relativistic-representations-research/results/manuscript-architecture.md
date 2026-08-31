# Manuscript Architecture for Relativistic Field Equations

Status: migration complete; manuscript Sections 1--8 composed and verified from baseline `R1`  
Worktable: `physics/quantum-mechanics/relativistic-representations.typ`  
Manufactured manuscript: `physics/quantum-mechanics/poincare-to-free-fields.typ`  
Research graph: [../plan.md](../plan.md)
Migration contract: [manuscript-migration-plan.md](manuscript-migration-plan.md)
Global continuation audit:
[field-to-observable synthesis](06-field-to-observable-synthesis-audit.md)

## Editorial principle

The research graph and the paper serve different purposes. The graph preserves
open alternatives, source packets, computations, challenges, and unsupported
claims. The paper should expose one checked semantic path:

```text
physical representation datum
  -> covariant realization
  -> equivariant equation or differential complex
  -> physical kernel/quotient
  -> recovery of the target little-group representation.
```

The fields-on-the-Poincare-group construction is retained as a proposed realization
bridge, not used silently as the definition of a particle or as a substitute for
the physical-fiber check.

## Proposed main paper

### 1. Problem and determination boundary

**Question.** What can Poincare symmetry determine about a free field equation, and
what further assumptions are required?

**Content.** State the target input `(mass, spin)` or `(helicity)`, distinguish
states, covariant fields, and scalar functions on the group, and list the extra
choices: carrier, locality, differential order, parity/reality, subsidiary
conditions, and gauge equivalence.

**Output.** A precise thesis weaker than the present line-424 claim: symmetry
classifies the physical representation, while a field equation constructs a chosen
covariant realization of it.

**Research binding.** [N1](../nodes/01-determination-boundary.md); current
manuscript lines 13--47 and 422--424 must be corrected or replaced, not copied.

### 2. Three representation spaces

**Question.** Which objects are being related?

Define and type:

1. the unitary induced Poincare representation `H_(m,s)` or `H_(0,h)`;
2. either the unitary regular space on the Poincare group or a finite nonunitary
   coefficient sector—these must not be conflated;
3. sections of a covariant Lorentz carrier `E_(j_1,j_2)` over Minkowski space.

Give the orbit/little-group classification only to the extent consumed later. Give
the abstract group law, action, and differentiation law once. Do not derive all
coordinate generators here.

**Output.** Typed physical, group-function, and covariant-field spaces with named
actions and analytic structures, so later maps have well-defined domains and
codomains.

**Research binding.** [N2](../nodes/02-three-representation-spaces.md); current
lines 13--345 contain raw material, but the product at line 85 and convention chain
at lines 18, 201--264 must be independently checked before synthesis.

### 3. Spin and helicity as physical fibers

**Question.** What internal representation remains after momentum is fixed?

Construct the stabilizer as the ambiguity of a standard momentum frame. For a
massive rest momentum, construct its `SU(2)` action and the highest-weight ladder
`m=s,...,-s`. For null momentum, construct the screen quotient and exact sequence
`1->Q_k->K_k->Spin(Q_k)->1`, including the representative-independent maps
`N_q`. Use the finite joint translation spectrum and its rotation invariance to
force the zero orbit, then obtain `exp(i h theta)`. Casimir values enter afterward
as checks of these representations, not as their definitions.

**Output.** The exact physical fibers `V_s` and `C_h` that every later
kernel/quotient must reproduce as a little-group representation.

**Research binding.** [N2a](../nodes/02a-spin-and-helicity.md).

### 4. Lorentz carriers from invariant motion splitting

**Question.** Why do covariant carriers have two labels `(j_L,j_R)`, and which
massive spin or massless helicity can each carrier contain?

Identify infinitesimal Lorentz motions with bivectors. Construct the Hodge map from
metric and orientation, compute its complementary complex projectors, and use
Lorentz naturality to prove that their images are commuting ideals. The familiar
`J_i+/-iK_i` combinations appear only afterward as a bounded convention check.

Construct `SL(S)->SO^+(Herm(S),det)`, compute its kernel, and exhibit the
commuting equation identifying it with the chosen spin cover of the original
vector space. Construct `F_(m,n)` by symmetric-power functors. At massive rest,
use coproduct and invariant contraction maps to build the actual spin inclusions;
at null momentum, construct the spinor line, unipotent radical, and direct helicity
character. State the four-dimensional and direct-line boundaries explicitly.

**Output.** The tuple
`(F_(m,n),Res_(K_k)F_(m,n),j_sigma)` for each directly occurring physical fiber,
including the excess massive spin content a later equation must remove.

**Research binding.** [N2b](../nodes/02b-lorentz-carriers.md).

### 5. The realization bridge

**Question.** When and how do the three spaces describe the same free particle?

Present one typed diagram:

```text
H_(O,sigma) --W--> Sol(D)/Gauge inside Gamma(E)
                              |
                              | C_(rho,lambda)
                              v
                    F_(rho,lambda)/C(Gauge)
```

Construct `W` universally from either a little-group intertwiner
`V_sigma->E|_(K_k)` or an isomorphism from `V_sigma` to a little-group
kernel/quotient. The coefficient map points from fields to scalar group functions;
it is optional packaging, not a required intermediate representation. For each
arrow state covariance, kernel, image, multiplicity, locality, inner-product
behavior, and noncanonical choices. The expansion
`f(x,z) = sum_i phi_i(z) psi_i(x)` appears here only after the function space and
basis/completeness statement have been supplied.

**Output.** The universal orbitwise realization theorem and its exact boundary:
local finite-order realization still requires a polynomial extension. The
group-function route earns a role only if it factors or reduces this construction.

**Research binding.** [N3](../nodes/03-realization-bridge.md); the orbitwise bridge
is supported. Current manuscript lines 348--381 provide only the downstream
coefficient construction and must not be presented as the physical realization
itself. Analytic and economy details remain in
[N3c](../nodes/03c-realization-details.md).

### 6. Universal local equations

**Question.** Can every finite massive spin and massless helicity be given a local
equation before choosing a conventional potential or parity-complete carrier?

Construct the two uniform chiral families:

Consume the vector--spinor bridge from Section 4: `Herm(S)` is the constructed
four-vector carrier, `det` is its Lorentz quadratic form, and null momentum is a
rank-one Hermitian form. Do not repeat that derivation here.

```text
massive spin s:
  F_(s,0)=Sym^(2s)(S),
  D_(m,s)(p)=(p^2-m^2)I;

massless helicity h>0:
  F_(h,0)=Sym^(2h)(S),
  [D_h(p)phi]^(A')_(A_2...)=p^(A A')phi_(A A_2...).
```

Derive the massive rest fiber. For the massless kernel, use the exact contraction
sequence
`0->Sym^n(ell)->Sym^n(S)->Sym^(n-1)(S)->0` rather than a monomial expansion.
Treat the opposite chirality as the opposite helicity. Show explicitly how
`p_mu` becomes `i partial_mu`. State that these are free complex chiral
realizations; parity, reality, actions, and potentials are additional requirements.

**Output.** Local equations for every `s,h in (1/2)N_0`, including one table for
`0,1/2,1,3/2,2` and a uniform finite-degree construction. A completed tower is
not an N4 result.

**Research binding.** [N4](../nodes/04-local-symbol-extension.md). Technical orbit
transport, polynomial complexes, and characteristic checks belong to
[N4a](../nodes/04a-polynomial-complex-details.md). N4a now supplies an exact
fixed-carrier/fixed-order lift criterion and a uniform symmetric integer-spin gauge
complex. Its intrinsic screen exact sequence proves the parity-paired helicity
fiber and its characteristic analysis excludes non-null physical cohomology. This
may now enter the manuscript as a separate bosonic potential theorem, without
being confused with the shorter one-helicity curvature construction.

[N4b](../nodes/04b-half-integer-potential.md) supplies the parallel Clifford
construction. Its gamma-traceless parameter, triple-gamma-traceless field,
spinor-screen exact sequence, and characteristic calculation give every
parity-paired half-integer helicity. Present it beside the bosonic theorem through
their common restriction/divisibility structure, not as a separate component
catalogue.

[N4c](../nodes/04c-action-completion-audit.md) prevents the manuscript from
silently identifying a wave equation with an Euler equation. Section 6 now
constructs the invariant pairings and trace reversals, proves the formal-adjoint
identities, and follows the resulting admissible source through causal and
positive-frequency completion. The resulting theorem remains bounded to the
parity-paired massless potential families and their source-generated Hilbert
subspaces.

### 7. Alternative carriers from spin zero through two

This section is now composed as a recovery-strength audit rather than an equation
catalogue. It compares the universal chiral baseline with familiar extra
requirements:

- `0`: scalar mass-shell equation;
- `1/2`: chiral massive realization versus parity-paired Dirac, and massless Weyl;
- `1`: chiral bivector versus Proca, and curvature versus Maxwell potential;
- `3/2`: chiral carrier versus Rarita--Schwinger spinor-vector;
- `2`: chiral carrier versus Fierz--Pauli or metric gauge potential.

Each example has the same five-line contract: carrier, symbol/complex,
kernel/quotient, little-group representation, and assumptions/failure boundary.
The massless `3/2` physical quotient is now supplied uniformly by N4b. N4c has
identified the action comparison and proved its Bianchi input; formal-adjoint,
reality, and massive comparisons remain obligations.
One short component calculation may independently verify each structural result;
the full expansion does not enter the argument.

**Output.** One quotient-map contract distinguishes exact block coincidence, a
local map of physical complexes, and common-fiber orbitwise equivalence. The
massless Weyl/Dirac and Maxwell potential/curvature comparisons reach the first two
levels respectively; several higher comparisons reach only the third. Extra
parity, reality, gauge, action, and locality presumptions remain visible.

**Research binding.** [N5](../nodes/05-low-spin-comparison.md), with `N3a/N3b/N4o`
as supported special branches. Old lines 1190--1499 provide candidate Dirac and
Proca calculations but contain the line-1298 label defect and an unproved component
elimination at lines 1366--1381.

### 8. Equivalence boundary and conclusion

This section is now composed. It distinguishes label, physical-fiber,
one-particle, local-complex, causal-response, action, free-quantum, deformation,
and predictive equivalence by the witness each preserves. It states the strongest
finite free-field theorem supported by Sections 1--7, then computes the curvature
term that obstructs carrying the free Dirac factorization through general `U(1)`
covariantization. Finally it constructs prediction as a typed
input--response--observable composite and names the exact stop and re-entry
conditions.

**Output.** A precise scope statement, a coupling obstruction, and a stopping
theorem rather than a universal slogan.

**Research binding.** `N4q`, `N5`, and
[N7](../nodes/07-equivalence-boundary.md). The countable-tower and
group-function economy question remains a separate `N6` horizon because no
topology, common operator domain, or uniform estimates presently support its
promotion into this finite-spin paper.

## Material outside the main deduction

| Existing material | Destination | Semantic result returned to the paper |
| --- | --- | --- |
| Repeated coordinate derivation of left/right generators, lines 92--345 | Appendix A or a bounded `N2` check | verified generator convention and commuting actions |
| Full spinor-polynomial bases beginning near line 348 | Appendix B / representation backend | carrier labels, multiplicities, and coefficient map |
| 1+1 and 2+1 development, lines 426--1091 | separate comparative note unless a later node proves it essential | dimension-specific exceptions and limits |
| Sigma/gamma contraction chains, lines 1190--1499 | Appendix C / executable checks | compact intertwiner, rank, kernel, or projector identity |
| Recursive chirality elimination, lines 1351--1381 | isolated symbolic computation | equivalence conditions and any introduced/lost solutions |
| Sources, contradictions, rejected routes, raw outputs | tracked research worktable | cited supported claims, never research bookkeeping |

Moving material out of the main deduction is not deletion. It must return a compact
invariant result that a main-text proposition or example actually consumes.

## Claim ladder

The manuscript should not advance to a stronger rung without proving the previous
one:

1. the equations/actions are covariant;
2. the symbol or complex has the stated kernel and gauge image;
3. the standard-momentum quotient carries the intended little-group action;
4. the global solution space realizes the target Poincare representation;
5. two realizations are related by an explicit map with stated locality/unitarity;
6. any claim of minimality or universality survives comparison with alternatives.

Rungs 1--4 are supported for the free complex chiral family at every finite
spin/helicity: N4 computes the symbols and fibers, while N3 supplies the global
Poincare intertwiner. Proca and Maxwell independently support alternative vector
branches. Rungs 5--6 remain open for most conventional carriers and for the
completed countable tower. The old dimension-only check remains excluded because
representation equivalence requires the little-group action, not just matching
dimensions.

## Synthesis rule

The paper may be rearranged incrementally without waiting for the whole graph, but
only supported outputs become assertions. Open results enter as questions,
conjectures, or omitted sections. The first safe manuscript operation is therefore
not a wholesale rewrite: it is to create this section skeleton, use the supported
`N1` boundary, type the three spaces in `N2`, and develop the bridge in `N3` while
retaining the old derivation as source material in Git history.

## Global-continuation boundary

The field-to-observable audit confirms that this architecture should remain a
free representation-to-field paper. N4q/N9 may supply a short concluding interface
showing why action, quantum algebra, state, interaction, preparation, and observable
are additional inputs. N9e now constructs N9c/N9d's nonrelativistic scalar
spin--boson Hamiltonian from the free scalar shell/Fock objects, a declared
spatial profile, and exact total-momentum reduction. It therefore closes scalar
provenance and the free limit. The benchmark must still remain separate because
the profile, two-level body, and coupling are not derived from the relativistic
carrier construction, and the matter dynamics is not Poincare covariant. N9f
adds a controlled ground and short-time prediction to that companion benchmark;
its failure to certify the long-time rate is a boundary to state, not a reason to
merge the benchmark into the free paper.

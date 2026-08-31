# N7 — Equivalence Boundary and Free-Field Stop Theorem

Status: supported synthesis for the scoped finite-spin free paper  
Consumes: [N3 realization bridge](03-realization-bridge.md),
[N4d computation interface](04d-computation-interface.md),
[N4q semantic computability](04q-semantic-computability.md),
[N4y free quantization recovery](04y-quantization-recovery-bridge.md),
[N4z fermionic CAR coincidence](04z-fermionic-car-coincidence.md), and
[N5 low-spin comparison](05-low-spin-comparison.md)  
Produces: the equivalence hierarchy, coupling obstruction, paper-level theorem
boundary, and bounded continuation interface for manuscript Section 8

## Research contract

- **Question/capability:** exactly what kind of sameness has the
  representation-to-free-field construction proved, and which stronger claims
  require new data?
- **Upstream anchor:** N3 identifies physical orbit representations; N5 shows that
  familiar low-spin presentations reach different equivalence strengths; N4q
  distinguishes presentation from response and prediction; N4y/N4z prove the
  scoped free Fock recovery.
- **Invariant target:** at the paper's main level, the same positive-energy
  one-particle representation and, for the parity-paired massless potential
  families, the same source-generated shell vector before and after free
  quantization.
- **Internal benchmark:** define each equivalence rung by a typed map/equality,
  prove the forward implication used by the paper, exhibit one obstruction to an
  unsupported reverse or deformation step, and state the stopping theorem.
- **Boundary:** no countable-spin topology, full induced-space density theorem,
  curved-background complex, interacting higher-spin system, bound/scattering
  calculation, or observable-compression result is promoted into this paper.

## 1. The hierarchy is a hierarchy of witnesses

For two free presentations `C=(G->F->T)` and `C'=(G'->F'->T')` on the same
momentum orbit, distinguish:

1. **label coincidence:** the same mass and spin/helicity labels;
2. **physical-fiber equivalence:** a little-group isomorphism
   `bar L_k:H(C_k)~=H(C'_k)`;
3. **one-particle equivalence:** a unitary Poincare intertwiner
   `U_1:H_C~=H_C'`;
4. **local-complex equivalence:** polynomial chain maps `L,M` whose composites are
   chain-homotopic to the identities on the declared complex;
5. **causal-response equivalence:** source and solution maps satisfying
   `L_sol Delta_C=Delta_C' L_src` modulo gauge with the declared supports;
6. **action equivalence:** a field/source map taking one quadratic action to the
   other up to a boundary term and invertible auxiliary/null sectors;
7. **free-quantum equivalence:** an isometric symplectic or CAR map whose Fock lift
   intertwines the field algebra and chosen vacuum/state;
8. **deformation equivalence:** a family of the preceding maps for the deformed
   complexes/actions, not only at zero coupling;
9. **predictive equivalence:** for the same admissible input, preparation, and
   observable, the two response composites agree or have a controlled error.

The implications actually used are constructive:

```text
local chain equivalence
 -> induced physical-fiber isomorphism,

physical-fiber isomorphism plus orbit transport
 -> one-particle intertwiner,

one-particle isometry plus symmetric/antisymmetric functor
 -> free Fock intertwiner.
```

For the second implication, N3 constructs the orbitwise map. For the third, if
`U_1:H->H'` is unitary, functoriality gives

```text
Gamma_+/- (U_1) iota_1(u)=iota_1(U_1u).
```

The reverse implications fail without new witnesses. N5 gives the local evidence:
several presentations share the physical fiber while no polynomial local inverse
has been constructed.

## 2. Causal, action, and quantum equivalence add distinct data

A physical-fiber map lives on shell. A causal comparison additionally needs maps
on compact source classes and spacelike-compact solution classes. If `Delta_C` and
`Delta_C'` are the causal maps, the same-source square is

```text
L_sol(Delta_C[J])=[Delta_C' L_src(J)].
```

This equality includes support and gauge representatives; an orbitwise map alone
does not define it.

An action comparison must preserve the duality that defines sources. For a linear
field map `L`, the required witness has the form

```text
S_C'[L phi]=S_C[phi]+boundary,
J'=L^(-dagger)J,
<J',L phi>=<J,phi>.
```

Without this relation, equal vacuum kernels do not imply equal source response.

For free quantization, N4y/N4z start from the faithful shell forms and apply the
symmetric or antisymmetric Fock functor. On the same source class `x`,

```text
P_1 field(x) Omega=iota_1(Wx).
```

This is the paper's strongest recovery equality. It depends on the source quotient,
positive shell metric, and vacuum; it is not obtained from Casimir labels alone.

## 3. Curvature obstructs automatic survival after coupling

The free massive Dirac factorization is

```text
(slash p+m)(slash p-m)=(p^2-m^2)I.
```

Replace commuting momenta by covariant momenta
`Pi_(A,mu)=i partial_mu-eA_mu`. Their same-section commutator is

```text
[Pi_(A,mu),Pi_(A,nu)]=-i e F_(mu nu).
```

Splitting the Clifford product into symmetric and antisymmetric parts computes

```text
(slash Pi_A+m)(slash Pi_A-m)
 =(Pi_A^2-m^2)I
  -(i e/4)[gamma^mu,gamma^nu]F_(mu nu).
```

The spin--curvature term vanishes in the free flat connection but not for a general
background. Therefore a free factorization or field equivalence does not supply a
deformed equivalence. The deformation must reconstruct its chain/Noether identities,
domains, causal maps, state, and observables.

## 4. Prediction is downstream of the paper

Let `I` be admissible data, `Sol_C:I->P` a selected physical response, and
`O:P->Z` an observable. The prediction is

```text
F_(C,O)=O circle Sol_C.
```

For a presentation isomorphism `T:P->P'`, define

```text
Sol_C'=T circle Sol_C,
O'=O circle T^(-1).
```

Evaluation on the same `i in I` gives

```text
O'(Sol_C'(i))=O(Sol_C(i)).
```

This proves semantic invariance, not computational reduction. A genuine
compression additionally requires a smaller route
`r circle C_red circle q=O circle Sol_C` with a whole-route cost or error witness.
Those model- and observable-dependent constructions belong to N4q and its
descendants, not to the free representation paper.

## 5. Scoped stopping theorem

The supported paper-level route is

```text
(momentum orbit, little-group representation)
 -> physical fiber
 -> chosen Lorentz carrier
 -> local symbol/complex
 -> physical kernel/cohomology
 -> induced one-particle representation.
```

For every separate finite label, the direct chiral branch reaches the last object.
For every separate finite parity-paired massless symmetric potential family, the
supported route continues:

```text
physical cohomology
 -> compact-source/spacelike-compact-solution quotient
 -> faithful source-generated positive shell completion
 -> CCR/CAR Fock space
 -> identical one-particle vector after one field acts on the vacuum.
```

This closes the paper's thesis. Further work cannot strengthen that thesis without
changing the claim class or adding new presumptions.

## 6. Re-entry conditions

- **Full induced-space density:** re-enter when a support/Paley--Wiener theorem
  proves the compact-source image dense in the entire abstract induced space.
- **Countable spin:** re-enter only after choosing a topology, common dense domain,
  label weights, and Green estimates uniform in spin.
- **Conventional massive higher-spin carriers:** re-enter after explicit local
  chain maps and physical-fiber checks exist.
- **Curved or interacting fields:** re-enter after the deformed complex/action,
  domains, causal construction, state, and observable are specified.
- **Computability/prediction:** re-enter for a fixed model, input, observable,
  accuracy, and whole-route comparison; symmetry alone is not the solver.

## Edges

- `N5/N4q -> N7`: comparison strength and observable semantics construct the
  hierarchy.
- `N4o -> N7`: the covariant-curvature term is the deformation obstruction.
- `N4y/N4z -> N7`: one-field vacuum recovery fixes the paper's strongest theorem.
- `N7 -> manuscript Section 8`: promote only the hierarchy, obstruction, stop
  theorem, and re-entry conditions.

# Research nodes

This directory owns the semantic constructions of the bilateral PDE/group
program. It is flat because filenames already identify the operation; the groups
below are reading views, not additional hierarchy. Each node must return a typed
construction, witness or obstruction, validity boundary, and named consumer.

The live spine and frontier are in the [research graph](../research-graph.md).
Executable evidence is indexed by [benchmarks](../benchmarks/README.md) and run
through the [computation workbench](../computation/README.md).

## Bilateral and reduction calculi

| Node | Capability | Disposition |
| --- | --- | --- |
| [operator-algebra inverse](operator-algebra-inverse.md) | infer factors, ladders, closure type, and obstructions from an operator | supported, grammar-bounded |
| [representation calculus](representation-calculus.md) | realize actions as matrix coefficients and spectral channels | supported contract |
| [operator decomposition](operator-decomposition-calculus.md) | construct selection graphs and reduced maps | supported contract |
| [PDE decomposition](pde-decomposition-calculus.md) | route quotient, complex, spectral, or microlocal reductions | supported, route-bounded |
| [orbit-space reduction](orbit-space-reduction-calculus.md) | descend PDEs, domains, and isotropy strata | supported |
| [homogeneous-bundle calculus](homogeneous-bundle-calculus.md) | construct finite multiplicity complexes for bundle-valued fields | supported contract |
| [adiabatic mode bundles](adiabatic-mode-bundle-calculus.md) | construct effective connections and leakage residuals | conditional |
| [observable-cyclic calculus](observable-cyclic-calculus.md) | retain the preparation/observable-visible carrier | supported bounded |
| [polynomial-algebra bridge](polynomial-algebra-bridge.md) | distinguish Lie closure, polynomial closure, and positivity debt | supported boundary |
| [decision engine](decomposition-decision-engine.md) | compare valid routes for one observable and accuracy | supported |

## Candidate construction

| Node | Capability | Disposition |
| --- | --- | --- |
| [filtered centralizers](filtered-centralizer-calculus.md) | lift symbol centralizers to commuting differential operators | supported bounded |
| [quadratic centralizer generator](quadratic-centralizer-generator.md) | generate complete rank-two quadratic candidates | supported bounded |
| [radial centralizer extension](radial-centralizer-extension.md) | extend the Euclidean radial construction | supporting backend |
| [`E^3` quadratic centralizer](e3-quadratic-centralizer.md) | certify the complete three-dimensional module | supporting backend |
| [seed--defect construction](defect-kernel-construction.md) | compute exact defect kernels, ineffective quotients, and closure | supported bounded |
| [structured seed compression](structured-seed-compression.md) | derive natural candidates before elimination | supported bounded |
| [typed relation planner](typed-relation-planner.md) | select relation constructors from certified capabilities | supported bounded |
| [lazy tensor quotients](lazy-compositional-tensor-quotients.md) | emit quotient coordinates without raw orbit scans | supported bounded |

## Finite represented-algebra realization

| Node | Capability | Disposition |
| --- | --- | --- |
| [coupled-carrier covariance](coupled-carrier-covariance.md) | construct linked base/fiber actions from metric and link defects | supported bounded |
| [full-operator covariance lift](full-operator-covariance-lift.md) | test curvature and lower-order terms on a generated action | supported bounded |
| [nonzero first-order transport](nonzero-first-order-transport.md) | recover curvature-aligned scalar transport | supported bounded |
| [matrix-valued transport](matrix-valued-transport-algebra.md) | construct two-sector coefficient projectors and polynomials | supported bounded |
| [finite semisimple coefficient algebra](finite-semisimple-coefficient-algebra.md) | construct joint idempotents and multiplicities | supported bounded |
| [finite represented star algebra](finite-represented-star-algebra.md) | recover center, isotypic blocks, and double-centralizer multiplicity | supported bounded |
| [simple-block PDE reduction](simple-block-pde-reduction.md) | realize a primitive carrier and reconstruct its PDE observable | supported, amortized |

## Variable-block observable propagation

| Node | Capability | Disposition |
| --- | --- | --- |
| [variable-projector jet](variable-projector-differential-jet.md) | construct connection, second-order potential, and leakage | supported bounded |
| [gap-aware leakage](gap-aware-leakage-bound.md) | promote one channel to an exact transition and controlled bound | supported bounded |
| [full finite-window propagation](full-block-finite-window-propagation.md) | propagate the coherent off-block map | supported bounded |
| [coefficient-derived projector jet](coefficient-derived-projector-jet.md) | differentiate isolated coefficient blocks without eigenvector matching | supported bounded |
| [projector-native propagation](projector-native-propagation.md) | lower frame and projector routes to common invariant arrows | supported bounded |
| [complete-route leverage](complete-route-leverage.md) | compare exact and sampled routes for the same observable | mixed bounded |
| [prepared observable active subspace](prepared-observable-active-subspace.md) | construct the minimal preparation-reachable carrier and pull back the effect | mixed; wins after reuse |

## Ownership rule

A node is the sole owner of its construction law and boundary. Benchmark packets
own concrete evidence; `research-graph.md` owns only the current dependency view
and disposition. Add a new node only when a new semantic object or bridge cannot
be represented by an existing owner. New examples belong under `benchmarks/`
unless they change a contract, capability verdict, or failure boundary.

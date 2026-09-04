# Realization and equivalence boundary

Status: supported classification; textbook recovery is regression evidence

## Obstruction

Two routes may have the same spin/helicity count while differing in locality,
sources, causal response, quantum algebra, deformation, or computational cost.
“Equivalent” is therefore meaningless without an observed level.

## Equivalence ladder

| Level | Required witness |
| --- | --- |
| physical fiber | unitary little-group intertwiner |
| local realization | chain map inducing fiber-cohomology isomorphism |
| source/response | source-quotient maps commuting with Green response |
| free quantum field | unitary map preserving CCR/CAR and vacuum state |
| interacting theory | map preserving supplied dynamics and observables |
| computation | same observable within error plus complete-route cost |

A higher row implies none of the lower implementation details, and a lower row
does not imply a higher one.

## Low-spin regression

At a standard null momentum, both Maxwell potential cohomology and chiral curvature
recover helicities `+1/-1`; their field carriers and source interfaces differ. At
massive momentum, the spin-one transverse carrier has three physical directions.
These calculations check signs, dimensions, and quotient meaning. They do not
generate the general construction.

For projected and unprojected higher-spin carriers, equality of quotient dimension
and screen rank establishes physical-fiber equivalence only. A local source map may
still require inverse momentum, and a direct Green route may be more expensive.

## Output and edges

Output: the exact witness required before one route may replace another.

- [Carrier/source obstruction](15-carrier-source-obstructions.md) applies the
  source and cost rows.
- [Observable compiler](16-observable-measure-compiler.md) applies the same-output
  computational row.

## Boundary

No equivalence is claimed outside the named domain, source class, state, dynamics,
observable, or error regime. Familiar equations remain useful regression targets,
not the research endpoint.

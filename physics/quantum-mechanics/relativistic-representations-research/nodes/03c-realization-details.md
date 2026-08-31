# N3c — Analytic and Economy Obligations for the Realization Bridge

Status: developing technical companion; it does not repeat the orbitwise bridge proved in [N3](03-realization-bridge.md)  
Consumes: N3's ordinary/gauge realization theorem and the typed spaces constructed in [N2](02-three-representation-spaces.md)  
Produces: analytic-completion and computational-economy tests for candidate realizations

## Research contract

- **Question:** after N3 constructs an algebraic orbitwise realization, what
  remains before claiming equivalence of completed solution spaces or a
  computational advantage?
- **Presumptions:** one fixed orbit, invariant orbit measure, finite Lorentz
  carriers, and N3's bundle/cohomology map.
- **Output:** bounded analytic, locality, norm, and route-cost obligations.
- **Boundary:** this node owns no second proof of the associated-bundle or
  little-group bridge and constructs no polynomial field symbol.

## 1. Supported input from N3

N3 supplies the only bridge consumed here:

```text
physical fiber V_sigma
  --little-group intertwiner or cohomology isomorphism-->
field fiber H_k
  --associated-bundle transport-->
orbitwise field realization.
```

Finite coefficient functions on the Poincare group are optional packaging
downstream of the field. N3c begins after these results; it does not reconstruct
them.

## 2. Analytic completion obligation

An algebraic bundle isomorphism becomes an equivalence of physical spaces only
after constructing:

1. the invariant measure `d mu_O` on the momentum orbit;
2. measurable standard boosts, or an intrinsic measurable bundle;
3. a dense common domain for the Poincare action and field constraints;
4. closed equation kernels and gauge images, or a declared distributional
   quotient when closed range fails;
5. a positive pairing on the quotient and its completion.

For a candidate bridge `W`, the required common-input computation is

```text
<W psi,W chi>_physical-field=<psi,chi>_induced
```

on a dense domain, together with its null space and completion. A
momentum-independent positive form on the finite Lorentz carrier is neither
required nor generally available. N2 supplies the orbit-measure contract and N3
the algebraic map; closed-range, domain, and completion claims remain open here.

## 3. Bounded computation questions

Machine or component work is justified only when it returns one of these outputs.

### C3.1 Coefficient-map equivariance

For a selected finite coefficient sector, verify

```text
C_(rho,lambda) dT_rho(X)=dL(X) C_(rho,lambda)
```

on generators of the connected Lie algebra. Output an exact identity or the
convention and generator that fail. This checks optional packaging, not N3's
physical bridge.

### C3.2 Multiplicity and information loss

Compute `Hom_(K_k)(V_sigma,Res F)` or the relevant isotypic multiplicity before a
coordinate matrix. For coefficient extraction, compute its kernel and image.
Output whether the sector contains zero, one, or several target copies and whether
reconstruction loses information.

### C3.3 Alternative gauge fiber

For a complex not already treated in N4a/N4b, compute

```text
H_field(k)=ker D(k)/im R(k)
```

and its little-group action. The result must be an explicit intertwiner with
`V_sigma`, not equality of dimensions.

### C3.4 Pairing and locality

Pull a proposed pairing through `W` and report its radical, signature, invariance,
and quotient. In momentum space, classify bridges and equation symbols as
polynomial, rational, or nonlocal; record degree, poles, and exceptional momenta.

## 4. Computational-economy criterion

Compare direct covariant and group-function routes on the same state input and
requested observable:

| Measure | Required account |
| --- | --- |
| semantic transformations | every change among state, carrier, coefficient, equation, and observable representations |
| decomposition burden | irreducible blocks constructed and later discarded |
| symbolic growth | carrier dimension, multiplicity, and degree as spin grows |
| locality cost | inverse operators, poles, exceptional momenta, and differential order |
| verification cost | intertwiner, quotient, characteristic, and norm identities |
| recovery cost | operations needed to recover a physical observable |
| reusable output | intertwiners, projectors, or complexes useful beyond one carrier |

Replacing an index by a continuous frame coordinate is not a reduction when
coefficient extraction and reconstruction add transformations without removing a
physical computation.

## 5. Existing low-spin evidence

[N3a](03a-massive-spin-one.md) and [N3b](03b-massless-helicity-one.md) test the
ordinary embedding and gauge-subquotient cases. Both find no fixed-spin/helicity
economy from group-function coefficient packaging. Their structural orbit,
quotient, and locality arguments require no duplicate matrix packet here.

## Output and open boundary

Promote only analytic domain/completion results, exact multiplicities,
kernel/image data, quotient representations, locality classes, and whole-route
cost comparisons. Raw matrices remain in a computation packet when required.

Open are the Hilbert/distribution completion of general gauge cohomology,
positivity after variational pairing, and evidence that a group-function route
reduces work for a family rather than repackages one carrier.

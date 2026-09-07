# Bilateral executable Pauli bridge

## Question

Can the same public constructor travel in both directions for a bundle-valued
PDE—representation data to a differential reduction, and a matrix differential
operator back to an effective represented algebra—without a supplied group name,
gauge choice, or component eigenfunctions?

The bounded test is the constant-curvature Pauli operator on oriented Euclidean
three-space.  It preserves the spin-resolved transverse energy channels through a
requested orbital level.  This is deliberately a channel observable: global
magnetic degeneracy would additionally require topology and volume data.

## Independent inputs

The schema `pauli-landau-bilateral/v1` carries two descriptions of one proposed
problem.  They are consumed by independent probes.

The representation-first probe receives only:

```text
oriented Euclidean dimension 3,
an irreducible complex Clifford fiber of dimension 2,
constant rank-two curvature with magnitude b and charge sign s,
a commuting translation along ker(F).
```

The PDE-first probe receives only:

```text
the scalar Euclidean principal symbol on a rank-two spinor fiber,
[Pi_1,Pi_2] = i kappa I,
the 2 by 2 matrix zeroth-order term M,
a commuting longitudinal momentum and a named common core.
```

No input contains a vector potential, eigenbasis, ladder, projector, spectral
formula, group name, or route name.  Exact matrix entries are used only as the
finite fiber presentation of the PDE; all subsequent operations are invariant
products, traces, adjoints, and projectors.

## Forward construction

Set `kappa=s b`.  From the Clifford relations and curvature,

```text
Q = gamma_1 Pi_1 + gamma_2 Pi_2 + gamma_3 Pi_3,
Q^2 = Pi^2-kappa gamma_3.
```

The curvature-aligned grading is `Sigma=s gamma_3`, so

```text
Q^2 = Pi_parallel^2+2b(N+1/2)I-b Sigma,
P_+ = (I+Sigma)/2,             P_-=(I-Sigma)/2,
a = (Pi_1+i s Pi_2)/sqrt(2b), [a,a^*]=I.
```

This constructs the second-order PDE and its analysis/synthesis grammar from the
represented Clifford algebra.  The fixed fiber is never expanded into two scalar
differential equations.

## Inverse construction

The PDE does not initially supply `Sigma` or a group.  The inverse probe computes

```text
b=|kappa|,        s=sign(kappa),        Sigma=-M/b.       (1)
```

For a Pauli factorization, (1) must satisfy the invariant finite-fiber tests

```text
Sigma^*=Sigma,       tr(Sigma)=0,       Sigma^2=I.        (2)
```

It then sets `gamma_3=s Sigma`, constructs an anticommuting unit Clifford seed
`gamma_1`, and orients `gamma_2=i gamma_1 gamma_3`.  Exact multiplication verifies

```text
{gamma_i,gamma_j}=2 delta_ij I,
gamma_1 gamma_2=i gamma_3,
-kappa gamma_3=M.                                      (3)
```

Equations (2)--(3) recover a Clifford factorization groupoid, not a unique spin
frame.  Curvature independently generates the same `a,a^*`, and hence the same
graded Clifford--Heisenberg algebra with longitudinal translation.

## Common reduction witness

Fourier analysis along `ker(F)`, Fock analysis of `N`, and the two spin projectors
give

```text
E_(k,n,+)=k^2+2bn,
E_(k,n,-)=k^2+2b(n+1).                                 (4)
```

The implementation compares the independently constructed `b`, charge
orientation, matrix spin term, grading, projectors, and rule (4).  Equality is
tested under unitary spin-frame and gauge conjugacy.  Analysis is longitudinal
Fourier plus spin/Fock projection; synthesis is the inverse transform and channel
sum.

For `b=3`, levels `n=0,1,2` have offsets

```text
aligned:       0, 6, 12,
antialigned:   6, 12, 18.
```

Changing `s` from `+1` to `-1` leaves (4) invariant but changes the aligned
projector from `diag(1,0)` to `diag(0,1)`.  This transfer check prevents a
hard-coded choice of spin component.

## Refusal

If `M=0` while `kappa=3`, normalization gives `Sigma=0`, so `Sigma^2!=I`.  The
PDE-first probe returns `SpinCurvatureResidual`; the representation-first probe
remains applicable and retains its candidate.  The final bilateral decision is
obstructed because one valid direction cannot certify a round trip.

This is stronger information than merely failing to diagonalize: it identifies
the lower-order matrix term that prevents the scalar principal symbol from
lifting to the requested Clifford square.

## Computability and complexity

The human construction uses four generative relations, one grading, two
projectors, and the single rule (4).  The exact implementation performs a fixed
number of `2 by 2` rational/Gaussian matrix operations and `O(r)` evaluations to
print channels through level `r`.  It performs zero coordinate eigenfunction
expansions.  This is semantic compression, not an asymptotic solver for arbitrary
fields.

The gain is largest when many channel values or spin-resolved observables reuse
the same factorization.  It does not pay the omitted global costs: proof of the
full direct-integral transform, degeneracy measure, boundary domains, or
variable-curvature mode coupling.

## Reproduction

From the repository root:

```powershell
python physics/mathematical-physics/PDE-group-research/computation/reduction_workbench.py `
  discover `
  physics/mathematical-physics/PDE-group-research/computation/examples/pauli-landau-positive.json `
  --summary
```

The positive- and negative-charge fixtures return `exact` with
`exact_bilateral_cross_probe`.  The inconsistent fixture returns exit code `2`
and the first inverse residual `SpinCurvatureResidual`.  Unit tests check both
transfers and the independent refusal.

## Capability boundary and next edge

This closes the first bounded executable bundle bridge.  It proves that the
common witness can retain a matrix fiber, its isotropy/projectors, an odd factor,
and a graded algebra.  It does **not** prove that every matrix PDE admits a
Clifford factor or that the inverse determines a global group.

That edge is now realized on `T^2 x R` by the
[global analytic Pauli benchmark](pauli-global-analytic.md): integral charged flux
constructs the magnetic-translation multiplicity, while nonintegral flux or the
wrong bundle domain refuses promotion without invalidating this local bridge.
That next edge is now passed by the [`SU(3)` outer-multiplicity bench](tensor-operator-su3.md):
natural intertwiners change an exchange-paired transition decision. The remaining
PDE-level edge is to realize those multiplicity maps on an analytic differential
carrier; more constant-field spin examples would not change the current verdict.

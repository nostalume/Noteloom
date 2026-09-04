# Bosonic free-field machine

Status: supported on declared compact-source images

## Capability

Turn a bosonic local complex into causal classical solutions, a positive-frequency
one-particle space, and a free quantum field without treating the field equation as
the predictive endpoint.

## Causal quotient

Given formally self-adjoint Euler operator `D` and gauge map `R`, admit compact
sources satisfying the adjoint constraint `R^dagger j=0`, modulo sources that pair
trivially with gauge-invariant solutions. A gauge-fixed Green operator `G` must
satisfy, on the admitted quotient,

```text
D G j = j mod im R,
G D f = f mod im R.
```

If two representatives differ by `R epsilon`, every admitted source gives the same
pairing because

```text
<j,R epsilon> = <R^dagger j,epsilon> = 0.
```

The causal propagator `E=G_ret-G_adv` maps the source quotient into the solution
quotient and constructs the symplectic form from the same pairing.

## Positive shell and CCR

Positive-energy spectral restriction gives a map `K` from compact-source classes
to the one-particle Hilbert space. The free field is then constructed by

```text
Phi(j)=a(Kj)+a^dagger(Kj),
[Phi(j),Phi(k)] = i sigma(j,k) I.
```

The second equality is computed from the CCR and the definition of `sigma`; it is
not a second determination by the group.

## Finite-spin transfer

Maxwell is the regression case. Symmetric higher-spin potentials reuse the same
source/Green/shell interface only when their gauge residual and source compatibility
are generated. Curvature-first and potential-first routes are compared on the same
observable in [carrier/source obstructions](15-carrier-source-obstructions.md).

## Output and boundary

Output: causal source quotient, symplectic solution image, positive-shell map, and
free CCR representation. Density of the compact-source image, interacting dynamics,
state selection beyond the vacuum, and generic higher-spin sources remain open.

- [Field--mechanics boundary](09-field-mechanics-reduction-boundary.md) asks what
  happens after dynamics is supplied.
- [Equivalence boundary](08-realization-equivalence-boundary.md) tests whether the
  causal and positive-frequency completions preserve the physical realization.
- [Visible measure](11-visible-spectral-measure.md) adds preparation/observable.

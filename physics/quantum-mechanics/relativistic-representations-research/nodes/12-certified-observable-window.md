# Certified observable window

Status: supported for ground and bounded short-time scalar observables

## Obstruction

A leading visible measure can reproduce a coefficient while failing at finite
coupling or long time. The approximation needs a remainder tied to the same
observable.

## Ground-state route

For a gapped prepared level, the Feshbach equation has the form

```text
E_g = E_0 + g^2 Sigma(E_g,g).
```

If the reduced resolvent remains bounded in a declared neighborhood, subtract the
leading value and use the resolvent identity:

```text
E_g-E_0-g^2 Sigma(E_0,0)
 = g^2[Sigma(E_g,g)-Sigma(E_0,0)].
```

A Lipschitz/resolvent bound on the bracket yields an explicit higher-order
remainder. The visible measure supplies `Sigma(E_0,0)`; the operator bound supplies
the certification.

## Open-channel route

Duhamel expansion of the same prepared state gives

```text
Q exp(-itH_g)J
 = -i g integral_0^t exp(-i(t-s)QH_0Q) B_1 exp(-isE_0) ds + R_2(t,g).
```

Squaring the leading vector constructs the finite-time emitted event from the
Fourier transform of `M_B`. A norm estimate on `R_2` defines the admitted window in
`g` and `t`; outside it the calculation returns “uncertified,” not a decay rate.

## Approximation semantics

Every result carries:

- exact model and preparation;
- expansion order and small parameter;
- target observable;
- tolerance/remainder bound;
- time/energy window;
- failure condition.

Tightening a numerical quadrature tolerance cannot repair an analytically vacuous
remainder.

## Output and edges

Output: certified bound coefficient and short-time open event derived from the same
field-generated measure, plus a refusal beyond the supported window.

- [Observable compiler](16-observable-measure-compiler.md) returns values and error
  evidence.

## Boundary

The benchmark does not establish long-time exponential decay, exact resonance,
finite-coupling scattering, or arbitrary kinetic reconstruction. Those require new
dynamics and error contracts, not more terms in the same unchecked expansion.

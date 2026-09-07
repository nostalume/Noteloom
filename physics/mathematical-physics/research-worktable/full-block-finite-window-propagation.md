# Full-block finite-window propagation

## Frozen contract `C_G13_v1`

G12 bounds one prepared leakage column. That loses interference: two nonzero
columns can cancel on a coherent preparation. G13 therefore constructs the whole
carrier arrow before any propagation or norm estimate.

Let `B:C^d -> C^q` be the G10 synthesis and `P` its Hermitian projector. The
constructor solves exact coordinates for every `P e_i`, producing analysis `A`
and checking

```text
A B=I_d,                 B A=P.                                     (1)
```

No orthonormal-frame assumption is made.

## Frame-invariant off-block operator

At each admitted momentum `k`, assemble every G11 column:

```text
V(k)=epsilon(2 k K+L),   T(k)=V(k) A.                               (2)
```

The exact structural checks are

```text
P T=0,                   T P=T.                                     (3)
```

Under a constant reduced-frame change `B_new=B G`, one has
`V_new=V G` and `A_new=G^-1 A`; hence `T_new=T`. This is the invariant object
missing from a list of columnwise bounds.

## Full and reduced routes

For a supplied positive gap `Delta`, define on the original carrier

```text
Q=I-P,
H_0=(Delta/2)(Q-P),
W=T+T^dagger,
H=H_0+W.                                                            (4)
```

`H_0` is the reduced baseline and has exactly zero `Q`-transition probability
from a retained preparation. The machine verifies (3), Hermiticity of `W,H`, and
`Q H_0 P=0` over `Q(i)`. It then evaluates `exp(-itH)` blockwise with SciPy and
returns unitarity and imaginary-expectation residuals instead of calling the
floating result exact.

The common observable is

```text
p_Q(t)=<exp(-itH) psi, Q exp(-itH) psi>/<psi,psi>.                   (5)
```

## Preparation-specific bounds

Finite-dimensional singular-value decomposition of the exact arrow `T` splits
(4) into independent two-level singular channels. Applying the G12 inequalities
inside that theorem contract gives, for each momentum block,

```text
p_Q(t) <= t^2 ||T psi||^2/||psi||^2,
p_Q(t) <= 4 ||T psi||^2/(Delta^2 ||psi||^2).                        (6)
```

For a finite direct sum, G13 sums the exact numerators and preparation norms before
division. It also reports `||T||_F^2` only as an operator-norm upper bound; it is
not substituted for the preparation quadratic form or labeled an equality.

## Evidence

The repeated-Pauli carrier is transported so both retained frame vectors leak into
the same complement direction. Thus `T` has rank one at both rational momenta.
For momenta `(1/2,1)`, gaps `(2,3)`, `epsilon=1/5`, `t=1`, and coherent preparation
`(1,1)` in both blocks, the constructor returns

```text
||T||_F^2 by block:       (2/25, 8/25),
time bound:               1/5,
gap bound / final bound:  1/9,
full transition:          0.0897128463663037,
reduced transition:       0.
```

The largest propagator unitarity residual is `2.93e-16`. For preparation `(1,-1)`,
the full map constructs `T psi=0` in both blocks, so the exact bound is zero and
the numerical observable agrees within the declared `1e-11` tolerance. Swapping
the reduced frame and preparation coordinates preserves `T`, the bound, and the
carrier observable. A constant G11 jet recovers zero; a closing gap and malformed
window lengths refuse distinctly.

## Cost, disposition, and boundary

For `n` momentum points, carrier size `q`, and retained size `d`, analysis requires
`q` exact coordinate solves. Coupling construction builds `n q^2` carrier entries;
blockwise dense propagation costs `O(n q^3)` time and `O(n q^2)` retained output.
Observable recovery is `O(n q^2)`. These are complete G13 costs after the upstream
G11 construction, not a runtime advantage over every baseline.

Disposition: **supported bounded** for a finite direct sum of Gaussian-rational
carrier blocks, positive supplied gaps, exact retained preparations, and the
complement-transition observable. G13 replaces channel enumeration by one
frame-invariant operator and detects coherent bright/dark structure.

[G14](coefficient-derived-projector-jet.md) now derives the projector jet and gap
from an isolated exact Hermitian coefficient cluster. G13 still does not consume a
general non-rigid projector jet directly, certify the transcendental matrix
exponential, cover a continuous spectral window, transport operator domains, or
treat crossings and nonlinear feedback.

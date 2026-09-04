# Collective-response boundary

Status: supported finite mechanisms; arbitrary nonequilibrium closure open

## Obstruction

A microscopic field or particle representation does not by itself select an
autonomous collective variable. A collective law is supported only when projection
and scale separation close the evolution of a named observable.

## Closure construction

Let `X_t` be microscopic dynamics and `Y=pi(X)` a proposed collective variable.
Closure requires a semigroup `S_t` with

```text
E[f(pi(X_t)) | pi(X_0)=y] = (S_t f)(y)
```

in the declared limit or exactly. Failure of this equality measures unresolved
memory; it is not repaired by renaming `Y` a hydrodynamic mode.

For a conserved density with local current, diffusive scaling seeks

```text
partial_t rho = div(D(rho) grad rho).
```

Current fluctuations require more than the mean law. A large-deviation generating
function or tilted generator constructs the exponential cost and exposes which
mobility/noise data are additional.

## Retained benches

- Classical SSEP supplies an exact finite generator and a diffusive/current
  large-deviation regression.
- Dephased quantum hopping reduces diagonal populations to SSEP only after the
  dephasing/scale limit is computed.
- A two-time charge statistic tests whether the same projected observable is
  retained rather than replacing it with a different classical question.

These are three aspects of one closure obstruction, not a chain of general theory.

## Semantic check

For the quantum-to-classical bench, eliminate coherences only when their resolvent
is controlled. Substitution into the population equation produces the effective
exchange generator plus a declared remainder. The comparison is made on the same
charge observable and time scaling.

## Output and edges

Output: an exact/controlled collective generator, fluctuation object, or explicit
memory refusal. The result is a separate dynamical regime under the global spine,
not a “third quantization.”

- [Certified window](12-certified-observable-window.md) supplies error semantics.

## Boundary

Finite SSEP and dephasing witnesses do not prove arbitrary interacting quantum
hydrodynamics, nonlinear closure, or long-time large deviations.

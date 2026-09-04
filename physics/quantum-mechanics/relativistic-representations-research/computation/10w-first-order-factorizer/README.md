# N10w first-order factorizer computation

This executable bench constructs the coefficient action required by the
half-integer natural-operation grammar.  Its input is a capability request, not a
Clifford relation or a matrix realization:

```text
equivariant momentum-linear d(p)
  + d(p)^2=Q(p)I
  + four-dimensional complex chiral carrier data
  + endomorphism/parity/reality budget
  -> chirality obstruction or paired carrier
  -> polarized quadratic law
  -> universal Clifford quotient and action certificate.
```

Run:

```powershell
node check-first-order-factorizer.mjs
```

The regression rejects supplied gamma matrices, a missing metric, a non-scalar
completion, a same-chirality endomorphism request, and an unsupported real
structure.  The successful case returns the action packet consumed by N10m.

The bench is intentionally bounded to complex four-dimensional Lorentz carriers.
It does not classify Clifford modules, invent a reality structure, establish
positivity, or construct CAR quantization.

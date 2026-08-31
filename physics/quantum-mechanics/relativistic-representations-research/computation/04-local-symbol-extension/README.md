# Check — Symmetric Potential Fiber Ranks

Semantic question: does the uniform symmetric complex in `N4a` have only gauge
cohomology away from the null cone and a two-dimensional screen quotient at a
nonzero null momentum for low finite spins?

The executable check represents symmetric tensors by homogeneous auxiliary-vector
polynomials. It constructs the invariant operators `P_p`, `A_p`, and `T`, then
computes:

- `ker(T^2) intersect ker(D_s(p))`;
- the rank of `P_p` on `ker(T)`;
- their quotient dimension;
- at null momentum, the rank of restriction to one screen witness.

Run:

```text
node check-symmetric-potential.mjs
```

The script uses exact integer/half-integer matrix entries and numerical Gaussian
elimination with tolerance `1e-9`. It is an independent finite-rank check, not the
proof: N4a's restriction/divisibility argument establishes all spins invariantly.

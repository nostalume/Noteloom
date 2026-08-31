# Check — Half-Integer Spinor-Tensor Fiber Ranks

Semantic question: does the spinor-tensor complex constructed in `N4b` have two
complex physical polarizations on a nonzero null momentum and no non-null
cohomology at low ranks?

The script imports the homogeneous-polynomial and linear-algebra operations used by
the bosonic check, adds a real form of the four-dimensional complex Dirac matrices,
and constructs `P_p`, `Gamma`, `Slash_p`, and `S_n(p)` directly. It also constructs
N4i's `Y`, `M_n`, and `B_n` to check the adjoint and hyperbolic completion, then
checks N4k's positive spinor-screen metric.

Run:

```text
node check-spinor-potential.mjs
```

It checks tensor ranks `n=0,1,2,3`, corresponding to helicity magnitudes
`1/2,3/2,5/2,7/2`, at null, non-null, and zero momentum. Complex dimensions are
obtained by halving ranks in the realification. Tolerance is `1e-9`.

At null and non-null sample momenta it additionally checks:

```text
M_n(F_n) subseteq F_n,
the Dirac--Fischer pairing is nondegenerate on F_n,
rank(M_n|_(F_n))=dim F_n,
E_n=M_nS_n is self-adjoint in the Dirac--Fischer Gram form,
B_nS_n=0 on F_n,
B_nR_n=(1/2)q on G_n,
S_n^2+2R_nB_n=qI on F_n,
kappa_p is independent of the auxiliary null witness on ker Slash_p,
the time-orientation correction agrees on future and past shells,
the induced metric on the two-complex-dimensional physical screen image is positive.
```

This is an independent finite-rank check. N4b's Clifford/restriction argument and
N4i/N4k's invariant operator reductions are the all-rank proofs.

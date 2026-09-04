# Support-Faithfulness Contracts

Recorded: 2026-08-29  
Used by: [bosonic free-field machine](../nodes/06-bosonic-free-field-machine.md) and [fermionic free-field machine](../nodes/07-fermionic-free-field-machine.md)

## SF-01 — Complete compatibility complex from a finite-type equation

- **Source:** Igor Khavkine, [Compatibility complexes of overdetermined PDEs of
  finite type, with applications to the Killing
  equation](https://arxiv.org/abs/1805.03751), *Classical and Quantum Gravity* 36
  (2019), 185012.
- **Hypotheses consumed:** a regular linear differential operator of finite type;
  locally constant ranks in its prolongation; smooth finite-rank bundles.
- **Output consumed:** an algorithm constructs a universal first compatibility
  operator and extends it to a full compatibility complex. Locally, its first
  kernel is the image of the original operator. The construction proceeds by
  finite prolongation, conversion to a connection-type system, and homological
  transfer back to the original bundles.
- **Application check in node 06:** on flat spacetime,
  `R_s=Sym partial:ker T->ker T^2` has constant coefficients and finite type. A
  rank-`s-1` Killing tensor is fixed by a finite jet and has no unrestricted
  derivatives beyond the finite prolongation order. Trace restriction is a
  constant invariant subbundle, so it does not spoil regularity.
- **Boundary:** the source treats the general method and the ordinary Killing
  operator in detail. node 06 applies the stated finite-type theorem contract to the
  traceless higher-rank Killing operator; it does not attribute an explicit
  minimal higher-spin formula to the paper.

## SF-02 — Local exactness, Killing sheaf, and causal supports

- **Sources:** Igor Khavkine, [The Calabi complex and Killing sheaf
  cohomology](https://arxiv.org/abs/1409.7212), *Journal of Geometry and Physics*
  113 (2017), 131--169; Igor Khavkine, [Cohomology with causally restricted
  supports](https://arxiv.org/abs/1404.1932), *Annales Henri Poincare* 17 (2016),
  3577--3603.
- **Output consumed:** a locally exact compatibility complex is a fine resolution
  of its solution sheaf; for the Killing operator on constant-curvature
  backgrounds this is the Calabi complex and the solution sheaf is locally
  constant. Causally restricted cohomology is computed from the corresponding
  ordinary/compact support cohomology, with the de Rham and Calabi complexes as
  explicit applications.
- **Internal extension used by node 06:** the finite prolongation in SF-01 turns the
  flat traceless Killing-tensor system into parallel sections of a finite-rank flat
  bundle. Its twisted de Rham resolution uses the same support homotopy as the
  constant-coefficient de Rham case. Therefore

  ```text
  H_sc^r(M;Kill_s) ~= H_c^r(Sigma;Z_s)
  ```

  for `M=R x Sigma`, where `Z_s` is the finite-dimensional space of prolonged
  traceless Killing data. This displayed higher-rank specialization is an internal
  consequence of the flat local-system construction, not a theorem quoted
  verbatim from the Calabi example.
- **Boundary:** curved backgrounds can make the prolonged connection nonflat and
  the Killing sheaf nonconstant. Nontrivial Cauchy-surface topology can also leave
  support cohomology.

## SF-03 — Maxwell spacelike-compact check

- **Source:** Marco Benini, [Optimal space of linear classical observables for
  Maxwell `k`-forms via spacelike and timelike compact de Rham
  cohomologies](https://arxiv.org/abs/1401.7563), 2014.
- **Output consumed:** for a globally hyperbolic spacetime with Cauchy surface
  `Sigma`, spacelike-compact de Rham cohomology is isomorphic to compactly
  supported de Rham cohomology of `Sigma`. In particular, on Minkowski spacetime
  `H_sc^1 ~= H_c^1(R^3)=0`.
- **Research use:** independent `s=1` check of the general local-system argument.

## SF-04 — Higher-spin curvature boundary

- **Sources:** Michel Dubois-Violette and Marc Henneaux, [Generalized cohomology
  for irreducible tensor fields of mixed Young symmetry
  type](https://arxiv.org/abs/math/9907135), *Letters in Mathematical Physics* 49
  (1999), 245--252; Bernard de Wit and Daniel Z. Freedman, [Systematics of
  higher-spin gauge fields](https://doi.org/10.1103/PhysRevD.21.358), *Physical
  Review D* 21 (1980), 358.
- **Output consumed:** generalized higher-spin curvatures and generalized
  Poincare lemmas provide the local unconstrained symmetric-gradient model.
- **Boundary:** node 06's gauge parameter is traceless. The ordinary de Wit--Freedman
  curvature is gauge invariant for the larger unconstrained gradient image, so it
  is not automatically a complete compatibility operator for the smaller
  constrained image. node 06 uses SF-01's complete compatibility construction and
  treats the traditional curvature only as a low-cost comparison.

## SF-05 — Gamma-traceless spinor-tensor specialization

- **Theorem contracts used:** SF-01 and SF-02.
- **Internal input:** on flat spacetime, the unconstrained symmetric-gradient
  equation with spinor coefficients is a finite direct sum of finite-type Killing
  tensor equations. Gamma contraction is constant, Lorentz equivariant, and
  commutes with flat prolongation.
- **Output constructed in node 07:** restricting every prolonged bundle to the
  gamma-traceless constant-rank subbundle preserves finite type and produces a
  flat finite-rank prolonged local system `Z_n`. Its degree-one
  spacelike-compact obstruction is `H_c^1(R^3;Z_n)=0`.
- **Boundary:** neither primary source states this arbitrary-rank fermionic
  specialization verbatim. The sources provide the finite-type compatibility and
  support-cohomology machinery; node 07 owns the restriction and its application.

## Supported conclusion

On four-dimensional Minkowski spacetime, the degree-one spacelike-compact
cohomology vanishes for the complete compatibility complexes of both

```text
R_s:ker T in Sym^(s-1) -> ker T^2 in Sym^s

and

R_n:ker Gamma in Sym^(n-1) tensor Delta
    -> ker Gamma^3 in Sym^n tensor Delta.
```

These are the exact support theorems used in node 06 and node 07. Density of compact source
amplitudes in the full induced Hilbert spaces is not part of these contracts.

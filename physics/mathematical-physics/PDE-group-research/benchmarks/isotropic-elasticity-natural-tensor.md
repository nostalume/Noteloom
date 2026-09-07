# Held-out natural-tensor transfer: isotropic elasticity

## Frozen contract before execution

- **Target:** `C_G0_v1` transfer and use dimensions.
- **Input:** a three-dimensional exact vector carrier `V`, a positive Euclidean
  metric `g`, an isotropic elasticity tensor

  ```text
  C_ijkl = lambda g_ij g_kl
           + mu(g_ik g_jl+g_il g_jk),
  ```

  positive rational Lamé parameters, a nonzero rational covector `k`, preparation
  `u`, probe `z`, and a time parameter. No group/algebra name, stabilizer basis,
  longitudinal/transverse projectors, multiplicities, or wave speeds are supplied.
- **Seed:** the canonical candidate module `End(V)` with commutator and its
  Leibniz action on covariant tensors.
- **Construction:** compile metric and constitutive-tensor preservation defects;
  certify the effective Lie algebra; construct the Fourier-symbol action
  `A(k)` from `C`; generate its longitudinal and transverse projectors from `g`
  and `k`; recover one plane-wave propagator matrix element.
- **Baseline:** form and diagonalize the full `3 x 3` symbol independently for each
  wave-vector direction, retaining its component eigenvectors.
- **Transfer discriminator:** the unchanged compiler must derive a three-dimensional
  stabilizer and closed bracket without using the full-matrix inner-derivation
  theorem from F6/F7.
- **Use discriminator:** the same symbol must reduce to one longitudinal and one
  transverse scalar channel, and analysis/synthesis must recover the named matrix
  element exactly or with the declared scalar-function accuracy.
- **Adversarial control:** a supplied anisotropy tensor must lower the kernel for a
  predicted tensor residual; an insufficient bracket/tensor budget must return an
  unresolved result.
- **Falsifier:** any expected group, projector, eigenvalue, or preferred kernel
  basis must be added to the input or to a case-named compiler rule.
- **Boundary:** homogeneous constant-coefficient linear elasticity on the Fourier
  core. Boundaries, variable media, nonlinear strain, analytic Fourier inversion,
  and continuum discretization cost are outside this transfer.
- **Promotion:** transfer may be supported after the unchanged tensor compiler and
  refusal pass. Use requires same-observable recovery. Leverage requires complete
  repeated-query cost including tensor stabilization and projector construction.

This file freezes the bench before its calculation. A failed result restricts or
rejects `C_G0_v1`; it may not silently amend the compiler and remain transfer
evidence for the same version.

## Execution result

The frozen positive input used `g=I`, `lambda=mu=1`, and
`k=(1,2,2)`. The constructor began with the canonical nine-dimensional
`End(V)` seed. Metric preservation lowered it by six dimensions; elasticity-tensor
preservation caused no further rank loss, as predicted because the isotropic
constitutive tensor is generated from the metric. Exact bracket certification
returned a closed three-dimensional effective algebra and no invisible ideal.

The compiler supplied the basis; no preferred skew matrices or rotation label was
input. The induced bracket table was constructed from the endomorphism commutator.
Adding the frozen axis dyad lowered the same kernel by two more dimensions to one.
Reducing the candidate budget from nine to eight returned
`CandidateBudgetExceeded`, not a false no-symmetry verdict.

For the use witness, contraction of the constitutive tensor with `k` constructed

```text
A(k) = 9 I + 2 k tensor k.
```

The metric and nonzero covector generated, without eigensolver output,

```text
P_L = (k tensor k)/9,       P_T=I-P_L,
A(k)P_T=9P_T,              A(k)P_L=27P_L.             (1)
```

All projector, orthogonality, synthesis, and intertwining identities in (1) were
checked exactly over the rationals. The two-channel cosine propagator and an
independent dense symmetric eigensolve gave respectively

```text
-0.39417615338896717
-0.39417615338896667
```

for the frozen probe/preparation, an absolute difference
`4.996003610813204e-16` below `1e-12`.

## Whole-route disposition

The declared arithmetic proxy counts `1638` one-time stabilization operations,
including `828` bracket-law/closure checks. Per wave vector it compares a dense
`3^3=27` eigensolve proxy with `3^2+2=11` projector/scalar operations. Its formal
break-even is therefore 103 queries.

This supports:

- **transfer:** unchanged finite defect compilation beyond the F6/F7
  full-matrix-inner-derivation origin;
- **use:** controlled same-observable recovery from two generated channels;
- **human compression:** one tensor signature, one simultaneous kernel, and two
  projectors replace direction-by-direction component eigenvectors;
- **conditional repeated-query leverage:** only under the stated dense arithmetic
  proxy and after its break-even count.

It does not support measured runtime dominance. More importantly, `End(V)` still
has dimension `d^2` and the rank-four residual target has dimension `d^4` before
tensor symmetries are compressed. Thus the transfer passes `C_G0_v1` while exposing
the next obstruction: natural seed construction is canonical but not yet scalable.

## Evidence packet and disposition

```text
id: E-G0-04
target: C_G0_v1 transfer, use, and leverage dimensions
kind: held-out transfer + adversarial control + controlled use/cost comparison
result: transfer supported; use supported at tolerance 1e-12; leverage conditional
        after 103-query proxy break-even; runtime dominance unresolved
independence: held out after C_G0_v1 and its regression compiler were frozen
boundary: dimension-three constant-coefficient Fourier core; full End(V) seed;
          no boundary, variable coefficients, Fourier inversion, or nonlinear strain
re-entry: a structured seed compiler must reduce d^2/d^4 candidate-residual growth
```

## G1 structured-compression continuation

The G0 contract and result above remain frozen. G1 reran the same input through two
prior structural operations: the exact metric-kernel isomorphism
`Lambda^2(V*) -> ker(delta_g)` and tensor-permutation orbit coordinates. In three
dimensions this changed the complete stabilization route as follows:

| Quantity | G0 raw route | G1 structured route |
| --- | ---: | ---: |
| candidate dimension | 9 | 3 |
| metric target dimension | 9 | satisfied by seed |
| elasticity target dimension | 81 | 21 |
| bracket checks | 828 | 54 |
| one-time proxy | 1638 | 117 |
| repeated-query break-even | 103 | 8 |

The raw and structured final generator matrices span exactly the same rational
subspace. The axis control also agrees exactly and lowers the structured kernel
`3 -> 1`, using a six-coordinate dyad residual. A diagonal non-orthonormal metric
passes the same span comparison. Candidate budget 8 now succeeds through the
structured route while retaining the raw route's typed refusal; budget 2 refuses
both.

The plane-wave projectors, eigenvalues, baseline observable, reduced observable,
and `4.996003610813204e-16` error are unchanged. Thus `E-G1-01`--`E-G1-03` support
structured semantic compression and conditional proxy leverage within the frozen
tensor grammar. They do not establish measured runtime dominance, arbitrary tensor
symmetry parsing, indefinite-metric support, or cross-family transfer.

## G2 relation-planning continuation

G2 leaves the physical input and both executed routes unchanged, but replaces the
adapter-selected structured path by a relation plan:

```text
metric-kernel
  -> permutation-orbits(isotropic constitutive tensor)
  -> simultaneous-defect-kernel
  -> visible-quotient
  -> bracket-closure.
```

The planner sees one certified nondegenerate symmetric bilinear form and three
rank-four permutation generators; it contains no elasticity, axis, rotation, or
stabilizer rule. Anonymous tensors with the same typed relations generate the same
21-coordinate plan. Missing, duplicated, or uncertified relations reject the
structured plan while preserving the raw route.

This exposes a cost previously outside the stabilization proxy. Generic orbit
canonicalization scans 81 indices under an eight-element permutation group, an
upper-bound 648 checks. Adding that to the 117 compiler proxy gives 765 and a
48-query break-even; the comparable raw planning-plus-compiler upper proxy is
1872. These are transparent arithmetic surrogates, not runtime measurements. G2
therefore supports relation-driven and human construction, but restricts broad
computational leverage until quotient coordinates can be emitted without a raw
orbit scan.

## G3 lazy-quotient continuation

G3 leaves the physical input and compiler unchanged but replaces generic orbit
canonicalization in the selected route by the recursive expression
`Sym^2(Sym^2(V*))`. It emits the 21 elasticity coordinates directly, admits the
route symbolically, and materializes no unselected route unless the fixture asks
for audit. In audit mode those coordinates equal the independent G2 orbit set and
the final stabilizer span equals the raw route exactly.

The selected planning-plus-compiler proxy is `21+117=138`, giving a nine-query
break-even against the same 27-versus-11 per-query comparison. The observable
error remains `4.996003610813204e-16`. This closes the operational-enumeration
obstruction for nested symmetric powers only; it does not establish arbitrary
tensor functors or coupled spinor representations.

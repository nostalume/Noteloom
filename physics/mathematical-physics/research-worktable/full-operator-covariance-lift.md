# Full-operator covariance lift

## Frozen contract `C_G5_v1`

### Capability and obstruction

G4 constructs a joint infinitesimal action `(A,B)` on a real metric carrier `V`
and Hermitian fiber `S` from the link `gamma:V -> End(S)`. Its output preserves
the principal Clifford symbol, but this does not imply preservation of a realized
differential operator. The missing operation is an ordered descent through the
remaining coefficient and domain data without replacing the generated action by
a named spin group or preferred rotation basis.

The bounded input is a covariant-momentum normal form

```text
H = g^(ij) Pi_i Pi_j + sum_i C_i Pi_i + M,
[Pi_i,Pi_j] = i F_ij I,                                (1)
```

where `g` and `gamma` satisfy the G4 contract, `F` is a constant real two-form,
and `C_i,M` are constant Hermitian Gaussian-rational matrices. The public
`coupled-operator-covariance/v1` schema returns the operator action without an
observable; the optional admitted use stage is the oriented Euclidean rank-three
Pauli operator. Both use the boundaryless gauge-covariant Schwartz core. The
schema supplies no group name, infinitesimal generator, grading, projector,
curvature axis, gauge potential, or channel rule.

### Ordered defect construction

Let `h_4` be the effective quotient algebra returned by G4. For each generated
pair `(A,B)` in `h_4`, form the residuals

```text
R_F(A,B)   = A^T F + F A,
R_C,i(A,B) = [B,C_i] - sum_j A_(j,i) C_j,
R_M(A,B)   = [B,M].                                    (2)
```

All three maps are linear on `h_4`. The common defect compiler therefore computes

```text
h_H = ker R_F intersect ker R_C intersect ker R_M       (3)
```

and certifies bracket closure using the quotient bracket already constructed by
G4. Equation (3), rather than a supplied stabilizer, determines the surviving
full-operator action. Its rank ledger retains the first layer at which a candidate
is lost. A zero-dimensional result is a meaningful `NoEffectiveOperatorSymmetry`
obstruction, not permission to invent a smaller named group.

The finite defect computation certifies equality of differential expressions in
the covariant-momentum grammar. Domain promotion is a separate theorem contract.
For `Schwartz(R^3,C^2)`, linear base actions and constant fiber actions preserve
the common core; a constant-curvature stabilizer has a gauge-covariant lift. The
returned witness is explicitly common-core covariance, not a proof of a unique
self-adjoint completion. Any other boundary/domain description is refused in
`C_G5_v1` rather than silently transported.

### Observable recovery without an imported grading

For a nonzero two-form in oriented Euclidean dimension three, construct its axial
covector and norm

```text
f = (F_23,F_31,F_12),        b = sqrt(f dot f).          (4)
```

The Clifford link then constructs the curvature grading

```text
Sigma_F = (-i/b) sum_(i<j) F_ij gamma_i gamma_j.         (5)
```

No eigensolver or preferred spin component enters (5). The use stage checks

```text
Sigma_F^* = Sigma_F,       Sigma_F^2 = I,
M = -b Sigma_F,            P_+/- = (I +/- Sigma_F)/2.   (6)
```

For the zero first-order matrices admitted by the present Pauli normal form,
curvature supplies the oscillator relation and the projectors give

```text
E_(k,n,+) = k^2 + 2bn,
E_(k,n,-) = k^2 + 2b(n+1).                              (7)
```

The analysis map is parallel Fourier analysis followed by `P_+/-` and oscillator
number analysis; synthesis is the spin/Fock sum and inverse parallel Fourier
transform. The executable comparison tests (7) and `P_+` against the independently
implemented bilateral Pauli route, so shared output is not obtained by sharing its
grading or channel code.

### Frozen discriminators

1. The rank-three G4 relation stage must construct `13 -> 4 -> 3`, including the
   ineffective fiber phase quotient.
2. Curvature must reduce the generated three-dimensional action to one dimension;
   zero first- and Pauli zeroth-order terms must cause no further rank drop.
3. All retained generators must close after the ordered intersection.
4. A request without an observable must retain the full-operator action and return
   no Pauli channels or projectors.
5. Positive-curvature projectors and channels must equal the independent bilateral
   Pauli result through the requested level.
6. Curvature reversal must preserve the energy rule while exchanging the aligned
   projector, without a preferred spin component in the input.
7. A transverse zeroth-order term must kill the curvature-stabilizing action at
   `zeroth-order-covariance`.
8. An unmatched half-space domain must return `DomainContractMismatch` rather than
   inheriting the boundaryless analysis/synthesis maps.

The candidate is falsified if it imports a rotation/spin generator, reconstructs
only the principal symbol, merges domain admission with formal covariance, shares
the independent Pauli implementation, or compares a different observable.

## Retained computation

```text
parse typed relation, coefficient, domain, observable, and budget data
relation <- G4(metric, gamma)
admit operator defect dimensions before materialization
lifted <- compile_defects(relation.effective_pairs, R_F, R_C, R_M)
refuse if lifted is empty or not closed
grading <- CliffordContract(F, gamma)
certify factorization and projectors
recover channels and compare with the independent bilateral regression
```

The implementation separates five semantic owners:

- `coupled_relation_input.py`: shared relation admission without router coupling;
- `coupled_operator_input.py`: typed admission and domain theorem matching;
- `full_operator_covariance.py`: reusable ordered coefficient defects;
- `pauli_operator_channels.py`: curvature grading and observable recovery;
- `coupled_operator_router.py`: thin public orchestration and witness assembly.

The G5 owners contain 178, 171, 113, and 263 lines against respective caps of 190,
220, 150, and 300; the focused public test contains 91 lines against a cap of 140.
The 101-line shared relation admission owner remains below its 130-line cap. The
operator plan has three candidate actions, nineteen residual coordinates, and a
conservative bracket bound of sixty-three. It materializes no coordinate
differential expression and performs no eigenfunction enumeration.

## Evidence ledger

The fresh worktable gate runs 142 unit tests and 20 computational checks. Ruff lint
and format checks pass, all 64 JSON fixtures parse, Python compilation succeeds,
and 236 local Markdown links resolve. These counts are repository observations,
not mathematical evidence beyond the discriminators below.

### `E-G5-01` — positive-curvature full lift

The unchanged G4 constructor returns relation dimensions `13 -> 4 -> 3`. On the
full coefficient package with `F_12=3`, the ordered ledger is

```text
curvature-covariance:   3 -> 1, residual rank 2,
first-order-covariance: 1 -> 1, residual rank 0,
zeroth-order-covariance:1 -> 1, residual rank 0.
```

The surviving action is closed. Equation (5) constructs `Sigma_F=diag(1,-1)`, all
seven factorization/projector checks pass, and (7) returns offsets
`0,6,6,12,12,18` through level two. The projector and full channel list exactly
equal the independent `pauli-landau-bilateral/v1` result.

The same schema without an observable returns this closed one-dimensional action
with `use=null`, no channels, and no projector. Thus Pauli recovery consumes the
operator result but does not define the generic covariance operation.

### `E-G5-02` — charge-orientation transfer

Changing `F_12` from `3` to `-3` and changing `M` according to (6) leaves every
energy offset unchanged. Equation (5) instead constructs
`P_+=diag(0,1)`, exactly matching the independent negative-charge bilateral route.
The same parser, defects, and use operations are retained.

### `E-G5-03` — lower-order and domain refusals

With positive curvature but `M=-3 gamma_1`, curvature first leaves one candidate
and the zeroth-order commutator then reduces its kernel to zero. The public result
is `NoEffectiveOperatorSymmetry` with first residual
`zeroth-order-covariance`. Replacing the declared Schwartz contract by a Dirichlet
half-space returns `DomainContractMismatch`; no boundaryless channel maps are
promoted.

## Disposition and boundary

Disposition: **supported bounded** for the generic covariance operation on the
tested exact constant-coefficient rank-three coupled package, and for its optional
Pauli observable in covariant-momentum normal form on the matched boundaryless
Schwartz common core. The evidence supports the relation-defect IR as a reusable
middle language across natural tensors, coupled symbols, and one full spinor
operator; it does not yet establish transfer of G5 itself beyond that coefficient
package.

It does not establish nonzero first-order transport, arbitrary Laplace-type
operators, variable coefficients, boundary domains, global spin integration,
self-adjoint completeness, or a universal PDE-to-group inverse. In particular,
the first-order block is operational but the successful fixtures set `C_i=0`.
The next discriminating bridge is therefore a nonzero symmetry-compatible
first-order coefficient with a changed but exactly recoverable observable—not
another constant-field parameter instance.

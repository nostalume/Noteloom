# Matrix-valued transport algebra

## Frozen contract `C_G7_v1`

### Bridge under test

G6 separated two questions that must not be conflated: the generated action may
preserve the full differential operator even when the observable consumer cannot
reduce a matrix-valued longitudinal coefficient. G7 resolves that consumer gap by
constructing a small coefficient algebra. It does not add a spin-component rule
to the generic defect compiler.

On the admitted Pauli common core, curvature and the Clifford link have already
constructed a Hermitian involution `Sigma_F`. The surviving first-order package
must first reconstruct a single axial coefficient

```text
C_i = e_i C_parallel,        e = (*F)/|*F|.                  (1)
```

The new algebra owner admits exact Hermitian `C_parallel` only when

```text
Sigma_F^2 = I,     [Sigma_F,C_parallel] = 0,                (2)
C_parallel P_s = lambda_s P_s,
P_+ = (I+Sigma_F)/2,     P_- = (I-Sigma_F)/2.               (3)
```

Equation (3) is checked as a matrix identity. A commuting coefficient that is not
scalar on either grading sector is refused rather than diagonalized inside that
sector.

### Constructed object

The two-sector star-algebra is represented by the basis and relation

```text
A = span_Q{I,Sigma_F},          Sigma_F^2=I,
C_parallel = alpha I + beta Sigma_F,                       (4)
alpha=(lambda_+ + lambda_-)/2,
beta =(lambda_+ - lambda_-)/2.                              (5)
```

The roots are recovered from invariant restricted traces, not supplied
eigenvectors:

```text
lambda_s = tr(P_s C_parallel)/tr(P_s).                      (6)
```

For distinct roots, the monic minimal polynomial and primitive idempotents are

```text
m_C(x)=(x-lambda_+)(x-lambda_-),
Q_+=(C_parallel-lambda_- I)/(lambda_+-lambda_-),
Q_-=I-Q_+.                                                  (7)
```

The machine verifies `m_C(C_parallel)=0` and `(Q_+,Q_-)=(P_+,P_-)`. Equal roots
collapse the coefficient's minimal polynomial to degree one while the grading
algebra remains available; this is exactly the G6 case and keeps the old scalar
witness shape.

### Algebra-to-PDE synthesis

For transverse offset `epsilon_(n,s)` and longitudinal Fourier momentum `k`, the
matrix polynomial is synthesized sectorwise as

```text
H_n(k) = sum_s [k^2 + lambda_s k + epsilon_(n,s)] P_s.      (8)
```

Thus recovery emits `2(r+1)` scalar channel polynomials through requested orbital
level `r`, together with the projectors that synthesize the matrix operator. This
is a finite algebraic decomposition, not an eigenfunction expansion.

## Frozen discriminators

1. For `F_12=3` and `C_3=2 gamma_3`, construct coordinates `(alpha,beta)=(0,2)`,
   roots `(2,-2)`, and minimal polynomial `x^2-4`.
2. Projectors derived from `C_parallel` must equal those independently derived
   from curvature grading.
3. The four level-zero/one energies must be `k^2+2k`, `k^2-2k+6`,
   `k^2+2k+6`, and `k^2-2k+12`.
4. Rotation to `F_23=3`, `C_1=2 gamma_1` must preserve the abstract algebra and
   energy list while rotating the concrete projectors.
5. `C_parallel=2I` must collapse to minimal polynomial `x-2` and preserve G6's
   scalar transport contract.
6. A Hermitian coefficient not commuting with `Sigma_F` must return
   `NoncommutingCoefficientAlgebra`; it may not choose a preferred eigenbasis.

The claim is falsified if roots or eigenvectors enter the input, the generic
full-operator compiler changes, rotation changes the spectrum, the minimal
polynomial residual is omitted, or a noncommuting coefficient is silently split.

## Evidence ledger

The G7 closure gate runs 150 unit tests and 20 computational checks. Ruff lint and
format checks pass across 65 Python files, all 69 JSON fixtures parse, Python
compilation succeeds, and 246 local Markdown links resolve.

### `E-G7-01` — former refusal becomes exact

The unchanged generic operator stage follows `13 -> 4 -> 3` in relation space and
`3 -> 1 -> 1 -> 1` through curvature, first-order, and zeroth-order defects. The
old G6 matrix fixture now constructs (4)--(7). All algebra residuals vanish, and
equation (8) produces the required sector-dependent longitudinal polynomials.

### `E-G7-02` — rotated transfer

The rotated fixture supplies only rotated curvature, link-coupled coefficients,
and zeroth order. It derives `e=(1,0,0)`, has the same roots and minimal polynomial,
and returns the same energy records. Its serialized projectors differ, confirming
that comparison occurs through the abstract algebra rather than fixed matrix
entries.

### `E-G7-03` — regression and refusal

Direct algebra tests certify distinct-root projector recovery, equal-root scalar
collapse, and noncommutation refusal. Existing zero-transport, scalar-transport,
transverse-defect, broken-zeroth-order, and domain-refusal tests remain part of the
canonical suite. The public CLI also admits the matrix fixture as an exact
`coupled-full-operator-kernel` result.

## Complexity and human leverage

G7 does not enlarge the candidate action or the nineteen-coordinate ordered
defect plan. After symmetry survival, axial reconstruction costs one length-`d`
matrix contraction and `d` exact matrix comparisons. For fiber dimension `q`, the
algebra stage uses two projector constructions, a constant number of dense `q x q`
products, two traces, and a degree-at-most-two polynomial check: `O(d q^2+q^3)`
arithmetic with `O(q^2)` storage. Channel emission remains `O(r)`.

The human object is four relations—(1), (2), (4), and (7)—plus the channel
synthesis (8). It replaces a component eigensystem for every coordinate
orientation and orbital level. This is a semantic compression claim, not a
measured runtime advantage.

## Disposition and boundary

Disposition: **supported bounded** for exact constant Hermitian longitudinal
coefficients in the two-sector algebra of a constructed Hermitian involution, on
the existing Euclidean rank-three Pauli common-core contract.

The reusable constructor is not intrinsically Pauli-specific, but its present
completeness is: two nonzero grading sectors, rational restricted traces, scalar
action on each sector, and coefficients in the Gaussian-rational field. Its
implementation now delegates primitive-sector construction to the
[finite split algebra](finite-semisimple-coefficient-algebra.md), which separately
supports more than two rationally split commuting sectors and reports unresolved
carrier multiplicity. This page retains the stricter G7 observable contract.
Noncommutative coefficients, irreducible field extensions, variable connections,
path ordering, domains, self-adjoint completion, and nonlinear closure remain open.

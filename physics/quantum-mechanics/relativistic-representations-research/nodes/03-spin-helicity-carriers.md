# Spin, helicity, and finite Lorentz carriers

Status: supported in four-dimensional complex finite-spin sectors

## Obstruction

The orbit alone does not specify internal states. Transport to a standard momentum
is nonunique; the ambiguity constructs the stabilizer action that must be realized.

## Massive construction

For `k_m=(m,0,0,0)`, transports differing by `B'(p)=B(p)r` obey `rk_m=k_m`.
The stabilizer is the rotation double cover `SU(2)`. Its irreducible finite unitary
fibers are `F_s = Sym^(2s) C^2`, with `2s` a nonnegative integer.

The generators arise from differentiating the group action, not from importing
matrices:

```text
d rho_s(X)(v_1 ... v_(2s))
  = sum_j v_1 ... (X v_j) ... v_(2s).
```

This construction covers integer and half-integer spin uniformly.

## Massless construction

For a null `k_0`, the stabilizer is the double cover of `E(2)`. Finite-helicity
particle sectors require its translation part to act trivially; the remaining
circle character is

```text
rho_h(theta)=exp(i h theta),  2h in Z.
```

Nontrivial translation action would instead describe continuous-spin sectors,
outside the present worktable.

## Lorentz carriers

The complexified Lorentz algebra splits as two commuting `sl(2)` actions. Finite
irreducible carriers are constructed as

```text
V_(j_L,j_R) = Sym^(2j_L) C^2 tensor Sym^(2j_R) conjugate(C^2).
```

This is a carrier catalogue, not a selection rule. Restricting `V_(j_L,j_R)` to a
massive or massless stabilizer determines whether the requested `F_s` or `F_h`
occurs. Multiplicity, locality, real structure, and desired operations decide
whether the occurrence is useful.

Representative families:

| physical label | economical carrier request | additional structure |
| --- | --- | --- |
| spin 0 | `(0,0)` | scalar wave symbol |
| spin/helicity 1/2 | `(1/2,0)` or `(0,1/2)` | first-order factorization |
| spin/helicity 1 | chiral `(1,0)`/`(0,1)` or vector potential | curvature or gauge complex |
| spin/helicity 3/2 | vector-spinor or symmetric spinor-tensor | gamma/trace constraint |
| spin/helicity 2 | chiral curvature or symmetric potential | differential gauge invariant |

## Output and edges

Output: the physical fiber `F`, admissible finite carrier candidates, and the
restriction/multiplicity question.

- [Realization bridge](04-realization-bridge.md) constructs orbitwise maps.
- [Natural-operation grammar](13-natural-operation-grammar.md) generates operations
  only after a carrier law and resource budget are supplied.

## Boundary

The Lorentz split is special to four dimensions. Mixed-symmetry, real/parity,
continuous-spin, and countable direct-sum completion are not generated here.

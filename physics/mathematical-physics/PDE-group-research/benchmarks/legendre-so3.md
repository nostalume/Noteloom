# Regression benchmark: `SO(3)` and the associated-Legendre family

## Bridge binding

- **Upstream anchor:** the local separation-of-variables and associated-Legendre
  material in `../../functional-and-spectral-methods.typ`, especially its
  observation at line 763 that the fixed-`m` ODE is not the whole orthogonal basis.
- **Bridge question:** what extra structure turns the separated ODE family into an
  `SO(3)` representation decomposition, and which part can be reconstructed in the
  reverse direction?
- **Invariant target:** the joint eigenspace of angular momentum operators in
  `H = L²(S²,dΩ)` and the coefficient observable
  `O_lm(f)=⟨Y_l^m,f⟩`.
- **Special resources:** compactness, a homogeneous space, invariant measure,
  discrete spectrum, separability, and regular singular endpoints.
- **Downstream effect:** decides whether the machine's common package is
  sufficient and whether its inverse reports missing data honestly.

## Analytic problem

Let

```text
M = S²,
H = L²(S², sin(theta) dtheta dphi),
C = C-infinity(S²),
D = -Delta_S²,
B = smoothness at the poles and 2pi-periodicity in phi.
```

The benchmark observable is `O_lm`, not merely the scalar eigenvalue.  Exact
normalization may follow the DLMF convention, but the same convention must be used
in both routes.

## Forward route: representation to differential equation

### Constructed inputs

`SO(3)` acts on `S²`; the induced unitary action on `H` is

```text
(pi(g)f)(x) = f(g^-1 x).
```

On the smooth core, choose the convention

```text
L_z = -i partial_phi,
L_+ = exp(+i phi)(+partial_theta + i cot(theta) partial_phi),
L_- = exp(-i phi)(-partial_theta + i cot(theta) partial_phi).
```

### Algebra certificate

On a generic `f in C`, explicitly expand only far enough to check

```text
[L_z,L_+]f = +L_+ f,
[L_z,L_-]f = -L_- f,
[L_+,L_-]f = 2 L_z f.
```

Construct the Casimir

```text
L² = L_z² + (L_+L_- + L_-L_+)/2
   = -[1/sin(theta) partial_theta(sin(theta) partial_theta)
       + 1/sin(theta)² partial_phi²]
   = -Delta_S²
```

on `C`.  The second equality is an operator equality on the same test function,
not a match of final formulas.

### Decomposition

The joint equations

```text
L² Y_l^m = l(l+1) Y_l^m,
L_z Y_l^m = m Y_l^m
```

with global regularity give `l in N_0` and `m=-l,...,l`.  With

```text
Y_l^m(theta,phi) = N_lm exp(i m phi) P_l^m(cos(theta)),
x = cos(theta),
```

the polar factor satisfies

```text
(1-x²)y'' - 2x y'
  + [l(l+1) - m²/(1-x²)]y = 0.
```

The forward output must retain the complete joint label `(l,m)`, invariant measure,
normalization, and ladder action; the ODE alone is a lossy projection of this
package.

## Reverse route: differential equation to representation candidate

### Input variants

The inverse is tested with successively richer inputs:

1. one scalar associated-Legendre equation with fixed numerical `(l,m)`;
2. the operator family parameterized by `m` and spectral parameter `lambda`;
3. that family plus endpoint regularity and weight `1` on `x in (-1,1)`;
4. the family embedded by `x=cos(theta)` and augmented with a periodic variable
   `phi`.

### Required output

- Variant 1 must return `Underdetermined`: a single equation does not expose the
  `m`-ladder, global topology, invariant measure on `S²`, or the distinction among
  covering groups.
- Variants 2–3 may return formal intertwiners between `m`-sectors, but must not yet
  claim a global `SO(3)` action.
- Variant 4 may construct `L_z,L_+,L_-`, their bracket closure, and the Casimir
  identity.  Integration yields at best a candidate effective action; the data may
  distinguish `SO(3)` from `SU(2)` only after the allowed spectrum and global
  single-valuedness are included.

### Intertwining witness

For every accepted ladder operator, calculate on a common core that

```text
L_+ : E_lm -> E_l,m+1,
L_- : E_lm -> E_l,m-1,
```

where `E_lm` is the joint eigenspace.  This requires both

```text
L² L_± f = L_± L² f,
L_z L_± f = L_±(L_z ± 1)f,
```

plus preservation of the global domain.  A recurrence relation for `P_l^m` without
the azimuthal factor is only a formal intertwiner certificate.

## Round-trip law

Let `A` be harmonic analysis and `S` synthesis.  On the declared dense test class,

```text
A(f) = {<Y_l^m,f>}_{l,m},
S(A(f)) = sum_l sum_m <Y_l^m,f> Y_l^m.
```

The benchmark passes when:

1. forward construction produces the stated differential family without
   hard-coding its final coefficients;
2. inverse construction on variant 4 returns a candidate whose differential
   realization is intertwined with the forward one;
3. `O_lm(S(A(f))) = O_lm(f)` exactly for every benchmark test function;
4. variants 1–3 return the specified missing-data records;
5. all equalities name the common core and all global claims name the closure and
   boundary conditions used.

## Machine-checkable test set

Use exact symbolic arithmetic on the finite span

```text
{Y_l^m : 0 <= l <= 3, -l <= m <= l}.
```

This finite set checks bracket, Casimir, ladder termination, eigenvalues,
orthogonality, and round-trip coefficients.  It does not prove general
completeness; the full Peter–Weyl/spherical-harmonic statement enters as a theorem
contract with exact hypotheses.

## Stop and re-entry

Stop after the certificate bundle passes.  Higher `l`, more recurrence identities,
or additional closed forms do not change the bridge.  Re-enter only if a transfer
case exposes a missing type, equivalence, domain condition, or ambiguity class.

# Global analytic promotion of the Pauli bridge

## Spine binding and horizon

- **Upstream:** the [bilateral Pauli router](bilateral-pauli-router.md) constructs
  the local Clifford--Heisenberg channel algebra but leaves its measure,
  degeneracy, topology, and self-adjoint realization unpaid.
- **Bridge question:** what minimum global data promote that local algebra to an
  actual Hilbert-space decomposition?
- **Invariant target:** the Pauli heat trace per unit length along the field.
- **Horizon:** constant curvature on `T^2 x R`, no boundary, one Hermitian line
  bundle, a rank-two spin fiber, and one positive heat time.
- **Success:** construct the direct-integral carrier and measure, global Landau
  multiplicity, self-adjoint domain contract, heat observable, and topology/domain
  refusals through the public router.

The torus is not another convenient coordinate separation. It is the smallest
compact transverse geometry on which the local curvature algebra confronts a
global topological admission condition and yields finite degeneracy.

## 1. The local algebra does not determine a global carrier

The local bridge supplies

```text
[Pi_1,Pi_2]=i s b I,
H=Pi_parallel^2+2b(N+1/2)I-b Sigma,
Sigma^2=I.
```

These relations exist on a local trivialization for any `b>0`. On a flat torus of
area `A`, however, a charged constant-curvature connection lives on a Hermitian
line bundle only if

```text
c_1 = (1/(2 pi)) integral_(T^2) qF = s b A/(2 pi) in Z.   (1)
```

Thus topology is not a degeneracy correction added after solving the PDE. It is
the admission test for the global Hilbert space itself. The executable schema asks
for `A/(2*pi)` and computes (1); it does not ask the user to provide `c_1` or the
degeneracy.

For the positive fixture,

```text
b=3,       A/(2*pi)=2/3,       s=+1
```

so `c_1=2`. Charge reversal gives the conjugate bundle with `c_1=-2`.

## 2. Topology constructs representation multiplicity

Let `d=|c_1|`. The transverse magnetic translations at the `1/d` lattice steps
generate the finite Heisenberg central extension

```text
T_1^d=T_2^d=I,
T_1 T_2=exp(2 pi i/c_1) T_2 T_1.                       (2)
```

Its irreducible Landau multiplicity carrier has dimension `d`. The group is now a
late output of the PDE, curvature, and topology:

```text
local curvature commutator
  -> integral cocycle c_1
  -> finite Heisenberg extension
  -> d-dimensional multiplicity space.
```

This answers a part of the bilateral question that the local factorization could
not answer. Energies use the oscillator representation; degeneracy uses the
global projective translation representation. Neither alone is the complete
spectral decomposition.

## 3. The unitary decomposition and its measure

The admitted Hilbert carrier is

```text
Hcal = L2(T^2,L^(c_1)) tensor L2(R) tensor C^2.          (3)
```

On smooth bundle sections and compactly supported smooth longitudinal functions,
the torus Bochner operator and free longitudinal Laplacian act on distinct tensor
factors. Their self-adjoint strongly commuting tensor realization is the declared
domain contract.

Use the unnormalized forward Fourier convention

```text
f_hat(k)=integral_R exp(-ikz) f(z) dz,
f(z)=integral_R exp(ikz) f_hat(k) dk/(2*pi).             (4)
```

Torus Landau projectors followed by (4) construct

```text
Hcal ~= integral_R^oplus direct-sum_(n>=0)
  [(C^d tensor S_+) + (C^d tensor S_-)] dk/(2*pi),      (5)

H_red(k,n,+)=k^2+2bn,
H_red(k,n,-)=k^2+2b(n+1).                               (6)
```

The measure `dk/(2*pi)` is part of the witness, not notation omitted after the
formal direct-integral sign. Analysis uses orthogonal Landau/spin projectors and
Fourier--Plancherel; synthesis sums those sectors and applies Fourier inversion.

## 4. Downstream analytic observable

The full heat operator is not trace class because the longitudinal line has
infinite volume. The invariant observable is therefore the trace per unit
longitudinal length. Equations (5)--(6) give

```text
Theta(t)/Length
 = d integral_R dk/(2*pi) exp(-t k^2)
     sum_(n>=0) [exp(-2btn)+exp(-2bt(n+1))]

 = d /(2 sqrt(pi t)) * (1+exp(-2bt))/(1-exp(-2bt))

 = d coth(bt)/(2 sqrt(pi t)).                           (7)
```

No transverse eigenfunction or gauge component appears in (7). For the fixture
`d=2`, `b=3`, and `t=1/2`, the tool returns

```text
Theta(t)/Length = 2*coth(3t)/(2*sqrt(pi*t))
                = 0.8814959953686372...
```

As an independent finite computation, levels `0` through `4` give
`0.8814957257169668`; evaluating the exact positive geometric tail gives
`2.6965167049633283e-7`. An exact-rational certificate—eight positive Taylor
terms for `exp(2bt)`, `pi>3`, and an integer-square-root lower bound—places it
below `2.814e-7`, hence below the requested `1e-6`. This audit checks the
observable evaluation, while the theorem contracts establish completeness.

## 5. Refusal separates local and global validity

Two refusal fixtures preserve the already valid local bridge.

1. If `A/(2*pi)=1/2` with `b=3`, then `c_1=3/2`. The constructor returns
   `FluxQuantizationObstruction`: no global torus line bundle realizes that local
   constant curvature.
2. If the transverse domain is declared as ordinary periodic scalar functions,
   the nonzero Chern class cannot be represented by that trivial carrier. The
   constructor returns `DomainContractObstruction` rather than silently choosing
   quasiperiodic component conditions.
3. If the requested finite audit tolerance is smaller than the exact positive
   tail at the declared level budget, the result is `unresolved` with
   `HeatTailBudgetExceeded`; the exact symbolic formula is not misreported as a
   completed finite numerical certificate.

Both local probes remain applicable and their candidates remain in the result.
Only `global-analytic-promotion` fails. This proves that local group/algebra
discovery and global representation realization are different semantic steps.

## 6. Computability verdict

For the named heat observable, the promoted route uses:

```text
one exact flux-integrality test,
one generated multiplicity d=|c_1|,
three generative spectral/translation relations,
one O(1) closed-form evaluation,
2(r+1) channel terms for an optional finite error audit,
zero coordinate eigenfunctions.
```

This is both human and internal computational compression: a topological integer
and a geometric series replace gauge-patched eigenfunction enumeration. It is not
yet a measured runtime victory over a specified three-dimensional discretization;
the tool says so explicitly.

## 7. Theorem contracts and provenance

The worktable constructs the composition and observable. It imports three
irreducible analytic facts:

- the constant-curvature torus Bochner operator is self-adjoint on its natural
  bundle realization, its lowest space has dimension `|c_1|`, and the ladder gives
  its Landau levels;
- the magnetic translations act unitarily through the finite Heisenberg extension;
- Fourier--Plancherel and the spectral theorem promote the orthogonal tensor
  factors to (5).

Sources 49--51 in the [source map](../sources.md) bind these claims. They do not
construct the present bilateral composition or heat observable.

## 8. Reproduction and stop rule

```powershell
python physics/mathematical-physics/PDE-group-research/computation/reduction_workbench.py `
  discover `
  physics/mathematical-physics/PDE-group-research/computation/examples/pauli-landau-global-positive.json `
  --summary
```

Positive and negative fixtures return `local_bilateral_then_global_exact` and
Landau multiplicity `2`. Nonintegral-flux and wrong-domain fixtures retain the two
local candidates but refuse global promotion.

The analytic-completion bridge is now supported for this bounded observable and
geometry. More torus shapes, gauges, or heat times would not change the spine.
Re-enter this branch only for a boundary, variable curvature, noncompact
transverse geometry, or an observable that requires explicit projector kernels.

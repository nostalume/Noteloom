# Continuum completion of finite departures

Status: `V_radial-1` supports the Gaussian continuum completion and common error
law; cross-family transfer, tight certification, and cost leverage remain open

Consumes: node 11's regulated neutral scalar model, node 34's finite
action-generated departure, and the return dispositions.

Produces: a controlled atomic approximation to the field-derived radial measure,
with one error law shared by its bound and finite-time open transforms.

## Obstruction: point sampling loses the shell measure

Node 11's one-boson departure is the multiplication vector

```text
b(r)=sqrt(4pi) r g f(r) in L^2(R_+,dr),
E(r)=sqrt(r^2+mu^2)+r^2/(2M),                  (35.1)
```

so its visible measure in the radial variable is

```text
dM(r)=|b(r)|^2dr=4pi r^2 g^2|f(r)|^2dr.        (35.2)
```

Replacing the continuum by modes with coefficients `g f(r_j)` does not converge
to (35.2): it omits both cell width and radial shell multiplicity. This is a
semantic mismatch before any quadrature error is considered.

For a partition `I_j=[r_j,r_(j+1)]`, the finite action must instead preserve the
departure norm on each cell. Construct

```text
m_j=integral_(I_j)|b(r)|^2dr,
c_j=sqrt(m_j).                                  (35.3)
```

Applying node 34's unchanged creation action with coefficient `c_j` gives
`B_N=(c_0,...,c_(N-1))^T`, hence

```text
B_N^dagger B_N=sum_j m_j=M([0,R]).             (35.4)
```

The shell normalization is now exact on the truncated interval. It is generated
from the continuum action density, not fitted to a target transform.

## Separate spectral approximation from departure generation

Use the midpoint representative

```text
epsilon_j=E((r_j+r_(j+1))/2)                   (35.5)
```

only after (35.3). This produces the atomic visible measure

```text
M_N=sum_j m_j delta_(epsilon_j).                (35.6)
```

It is a controlled spectral collocation, not the exact compression of the
multiplication operator `E(r)`. For any bounded Lipschitz transform `F`, define

```text
V_N=sum_j m_j max_(r in I_j)|E(r)-epsilon_j|,
T_R=M([R,infinity)).                            (35.7)
```

Adding and subtracting `F(epsilon_j)` within each cell computes

```text
|integral F(E(r))dM(r)-sum_j m_jF(epsilon_j)|
 <=Lip(F)V_N+||F||_infinity T_R.                (35.8)
```

Because `E` is increasing, the maximum in (35.7) is attained at a cell endpoint;
no component expansion or unknown optimizer is hidden in the bound.

## Generate both transform certificates

For a real bound parameter `z<E(0)=mu`, take

```text
F_z(E)=1/(z-E),
||F_z||<=1/(mu-z),   Lip(F_z)<=1/(mu-z)^2.      (35.9)
```

The atomic bound-return error is therefore

```text
epsilon_res<=V_N/(mu-z)^2+T_R/(mu-z).          (35.10)
```

For the finite-time emitted-channel kernel, construct it before using its closed
trigonometric form:

```text
A_t(delta)=integral_0^t exp(-is delta)ds,
K_t(delta)=|A_t(delta)|^2.                      (35.11)
```

Directly estimating the integral and its derivative gives

```text
|A_t|<=t, |A_t'|<=t^2/2,
|K_t'|<=2|A_t'||A_t|<=t^3, ||K_t||<=t^2.       (35.12)
```

With `delta=E-level_gap`, the same atomic departure has

```text
epsilon_open<=t^3 V_N+t^2 T_R.                 (35.13)
```

Thus bound and open convergence are not two fitted quadratures; they are two
declared transforms of the same cell masses and the same variation/tail witness.

## Gaussian model closes the tail calculation

Node 11 supplies `f(r)=exp[-r^2/(2Lambda^2)]`. Integrating (35.2) gives

```text
M(R,infinity)
 =g^2 pi^(3/2)Lambda^3 erfc(R/Lambda)
  +2pi g^2 Lambda^2 R exp[-R^2/Lambda^2].       (35.14)
```

Differences of (35.14) generate every `m_j`; no numerical integration is needed
to define the finite action coefficients. The continuum quadrature remains only an
independent comparison witness.

## Frozen candidate `C_radial-v1`

```text
CompileRadialDeparture(ScalarModel, radial cutoff R, cell count N, budget)
 -> action-generated finite B_N + cell masses/energies
    + exact truncated mass + V_N + Gaussian tail
    + bound/open atomic transforms and error bounds
 | refusal(nonfinite/nonpositive R, noninteger/nonpositive N, zero coupling,
           failed finite departure, or budget).
```

Independent dimensions are shell normalization, unchanged finite-action reuse,
mass convergence, bound-transform containment, open-transform containment,
refusals, and complete cost. The contract is restricted to node 11's Gaussian
neutral scalar family; parameter variation is robustness, not cross-family transfer.

The post-freeze bench uses node 11's existing `M=2`, `mu=1`, `Lambda=1`, `g=0.2`,
gap `1.4`, cutoff `R=5`, and `N=16,32,64`. It supports convergence only if the
finite departure mass equals the analytic cell mass, both continuum errors lie
inside (35.10)/(35.13), and the bounds decrease with refinement. A second parameter
fixture tests normalization robustness; invalid cutoff, coupling, and budget must
be refused without altering the compiler.

The fair baseline is direct quadrature of the same one-dimensional measure. Both
routes are structure-aware and `O(N)` at fixed accuracy; no leverage claim is
admitted without measured accuracy-versus-work evidence.

## Execute the frozen bench

For the declared node 11 fixture, the full mass is
`0.222733119873268...`. At `R=5`, the generated finite departure has mass
`0.222733119855474...` and analytic tail `1.77945e-11`; their sum recovers the full
mass to floating precision. The finite and continuum objects carry the same
measure identifier.

At bound parameter `z=0` and open time `t=1/2`, the continuum transforms are

```text
R(0)=-0.128671982921050,
O(1/2)=0.0548934769218276.                      (35.15)
```

The post-freeze atomic results are

| cells | bound error | bound certificate | open error | open certificate |
| ---: | ---: | ---: | ---: | ---: |
| 16 | `1.36272e-4` | `4.62264e-2` | `1.84076e-5` | `5.77830e-3` |
| 32 | `3.44829e-5` | `2.25787e-2` | `4.60276e-6` | `2.82234e-3` |
| 64 | `8.64688e-6` | `1.11497e-2` | `1.15074e-6` | `1.39372e-3` |

Every actual error lies inside (35.10) or (35.13), and both certificates decrease
under refinement. A second Gaussian parameter fixture preserves (35.4); invalid
cutoff, cell count, coupling, and budget are refused.

The actual errors fall approximately quadratically, while the Lipschitz witness
falls only linearly and overestimates them by hundreds. This does not invalidate
containment, but it prevents the present certificate from supporting an efficient
accuracy selector. The executable evidence is `computation/tests/test_measures.py`;
the disposition is in `../results/return-compiler-dispositions.md`.

## Horizon and stop rule

The horizon is the regulated monotone Gaussian radial model and bounded transforms
in (35.9)--(35.13). It excludes a removed ultraviolet regulator, threshold/on-cut
resolvents, long-time limits, resonance continuation, multichannel coherence,
gauge fields, and asymptotic scattering. The convergence, robustness, and refusal
dimensions are classified, so this branch stops. Re-enter only if a moment-based
cell construction can sharpen the certificate or a new form-factor family can
test transfer without changing the finite action semantics.

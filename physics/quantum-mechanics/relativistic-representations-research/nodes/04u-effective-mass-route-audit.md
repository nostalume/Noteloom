# N4u — Effective-Mass Evaluation Bridge and Cost Audit

Status: exact direct-response and scalar self-energy curvature formulas supported
in the gapped fiber; their same-branch equality and a finite regression are
verified; the leading weak-coupling atom formula is reduced to an internal
resolvent integral but not numerically evaluated; N4v now constructs the
conditional relativistic identification of this curvature with rest mass  
Consumes: [N4r field/mechanics projection](04r-field-mechanics-stability.md),
[N4t neutral composite same-state test](04t-neutral-composite-same-state.md),
[effective-mass source contracts](../sources/effective-mass-route-contracts.md),
and [finite route regression](../computation/04u-effective-mass/README.md)  
Produces: one observable with two exact evaluation routes, their semantic
coincidence witness, a leading one-photon reduction, and a whole-route cost
verdict

## Node contract

- **Question/capability:** does N4r's prepared self-energy make the dressed
  composite's effective mass cheaper to compute than differentiating the full
  fiber eigenbranch?
- **Presumptions:** `H(P)` is a twice differentiable self-adjoint fiber family
  with common domain near `P=0`; the chosen ground branch is simple and isolated
  in the modified/no-soft sector; inversion makes its first derivative vanish;
  and ordinary Feshbach inversion is used only inside that gap. Scalar mass
  additionally requires rotation covariance.
- **Material bindings:** N4t supplies the same dressed branch and preparation;
  EM-01 supplies the gapped atom--radiation fiber; EM-02 supplies an independent
  Pauli--Fierz response theorem; EM-03 controls the weak-coupling expansion.
- **Output:** exact full-space and prepared-sector Hessians, a finite regression,
  the order-`g^2` atomic-resolvent formula, and the conditions under which either
  route reduces total work.
- **Boundary:** no numerical hydrogen mass shift or cutoff removal is claimed.

## 1. Construct the observable from the dressed band

N4t constructs a translation-covariant dressed band

```text
H(P) psi_P=E(P) psi_P.
```

The energy itself answers the cost of preparing momentum `P`. Its first
derivative is the band velocity. The next variation therefore measures how much
additional momentum changes that velocity. Construct the inverse effective-mass
tensor by

```text
(M_eff^(-1))_(ij)=partial_(P_i) partial_(P_j) E(P)|_(P=0).
```

This definition uses only the same spectral branch; it does not import a
classical mass parameter after dressing. If rotations act covariantly on the
fiber family, the Hessian commutes with every spatial rotation. The only such
real symmetric bilinear form is a scalar multiple of the Euclidean metric, so

```text
M_eff^(-1)=(1/3) Delta_P E(0).
```

Without rotation covariance, retain the tensor. Isotropy is a simplifying
physical hypothesis, not a consequence of translation invariance.

To minimize notation, fix one unit direction `n` and set

```text
H(t)=H(t n),
E(t)=E(t n),
V=H'(0),
W=H''(0).
```

Then `E''(0)=<n,M_eff^(-1)n>`. An isotropic model needs only this one directional
calculation; the tensor can otherwise be reconstructed by polarization.

## 2. Direct route: differentiate the same eigenstate equation

Let `psi=psi_0` be normalized and let

```text
P_psi=|psi><psi|,
Q_psi=I-P_psi,
R_perp=Q_psi(H(0)-E(0))^(-1)Q_psi.
```

The gap constructs this inverse on the orthogonal complement. Choose the local
phase of `psi_t` so that `<psi,psi'(0)>=0`. Differentiate the normalized
eigenstate equation on the same branch:

```text
H(t)psi_t=E(t)psi_t.
```

At `t=0`, inversion symmetry gives `E'(0)=0`. Subtracting the differentiated
right side computes

```text
(H(0)-E(0))psi'(0)=-V psi.
```

Both sides lie in `Q_psi H`: the phase condition puts `psi'` there, while
Hellmann--Feynman gives `<psi,V psi>=E'(0)=0`. Apply the constructed inverse:

```text
psi'(0)=-R_perp V psi.
```

Differentiate `E'(t)=<psi_t,H'(t)psi_t>` and substitute this same response:

```text
E''(0)
 =<psi,W psi>+2 Re<psi'(0),V psi>
 =<psi,W psi>-2 Re<V psi,R_perp V psi>.
```

This is the direct response route. It requires one ground eigenpair and one
linear solve on its full orthogonal complement; it does not require eigenvalues
at several nearby momenta.

For EM-01's composite fiber,

```text
H(P)=(P-P_f)^2/(2M)+H_at+H_f+g Phi(F_x),
```

so the operation `d/dt` itself constructs

```text
V=-(n dot P_f)/M,
W=1/M.
```

The curvature becomes

```text
E''(0)
 =1/M-(2/M^2)
   <(n dot P_f)psi,R_perp(n dot P_f)psi>.
```

The second term is nonnegative because `H(0)-E(0)` is positive on the
complement. Hence `E''(0)<=1/M`; where the dressed branch remains strictly
convex, a nonzero response gives `M_eff>=M`. This is a semantic result: field
momentum stored in the dressing reduces the response of band velocity to total
momentum.

## 3. Prepared route: differentiate the scalar self-energy

Choose N4t's normalized bare preparation

```text
chi=phi_0 tensor Omega,
P_0=|chi><chi|,
Q_0=I-P_0.
```

For the gapped modified/no-soft fiber, construct

```text
h(t)=<chi,H(t)chi>,
b(t)=Q_0 H(t)chi,
H_Q(t)=Q_0 H(t)Q_0,
A(t,z)=z-H_Q(t).
```

Solve one complementary equation

```text
A(t,z)v(t,z)=b(t).
```

Then N4r's exact Schur computation is the scalar equation

```text
f(t,z)=z-h(t)-Sigma(t,z),
Sigma(t,z)=<b(t),v(t,z)>.
```

The Feshbach theorem gives the same eigenbranch through

```text
f(t,E(t))=0,
psi_t proportional to chi+v(t,E(t)).
```

This branch equality, not similarity of notation, is the bridge to the direct
route.

At fixed `z`, differentiate the *linear solve*, rather than expanding the inverse:

```text
A v=b,

A v_t=b_t+(H_Q)_t v,

A v_tt=b_tt+(H_Q)_tt v+2(H_Q)_t v_t.
```

Each equation has the same operator `A`. Thus one factorization or preconditioner
can be reused. The required self-energy derivative is computed from these
solutions:

```text
Sigma_tt
 =Re[<b_tt,v>+2<b_t,v_t>+<b,v_tt>].
```

Energy differentiation is even simpler. Since `b` is independent of `z`,

```text
Sigma_z
 =<b,-A^(-2)b>
 =-||v||^2.
```

The denominator appearing in implicit differentiation is therefore

```text
1-Sigma_z=1+||v||^2=||chi+v||^2.
```

It is not an arbitrary wavefunction-renormalization symbol: it is exactly the
norm of N4r's recovered state. Differentiate `f(t,E(t))=0` twice. Inversion
symmetry makes `E'(0)=0`, so the mixed terms vanish and the same directional
curvature is

```text
E''(0)
 =[h_tt+Sigma_tt]/[1-Sigma_z]
 =[h_tt+Sigma_tt]/[1+||v||^2],
```

with all quantities evaluated at `(t,z)=(0,E(0))`.

For EM-01's bare vacuum preparation, `b_t(0)=0` and `h_tt=1/M`. The prepared
route therefore needs the root solve for `E(0)` and, after reusing its
complementary solve, two tangent solves for `v_t` and `v_tt`.

## 4. The two formulas have an explicit common target

Define `E_D(t)` as the unique simple eigenvalue continued from `E(0)` by the
full spectral theorem. Define `E_F(t)` as the unique root of `f(t,z)=0` in the
same Feshbach window. Exact isospectrality and uniqueness compute

```text
E_D(t)=E_F(t)=E(t)
```

on one neighborhood of zero. Apply the same operation `d^2/dt^2` to this
function identity:

```text
<psi,W psi>-2 Re<V psi,R_perp V psi>

  =E''(0)

  =[h_tt+Sigma_tt]/[1-Sigma_z].
```

This is the semantic-coincidence witness. Both expressions answer the change of
velocity on the same dressed band; neither is allowed to substitute a different
state, cutoff, or preparation.

The [finite regression](../computation/04u-effective-mass/README.md) evaluates
both sides on one parity-symmetric block family. It also differentiates the
lowest eigenvalue independently by a five-point stencil. The direct and
Feshbach curvatures agree to `5.6e-17`; the finite-difference check agrees to
`6.8e-10`.

## 5. Leading weak-coupling reduction removes the Fock-space eigenproblem

The exact formulas still hide a large inverse. In the gapped scalar model, a
controlled small-`g` expansion supplies one stronger reduction. At `g=0`, let
`phi_0` be the internal atomic ground state with energy `e_0`. Acting once with
the linear field coupling on `phi_0 tensor Omega` creates exactly one photon.
Absorb the field normalization into the atomic vector

```text
c(k)=one-photon creation amplitude at momentum k applied to phi_0.
```

The free one-photon complementary operator at total momentum `P` is

```text
H_1(P;k)=(P-k)^2/(2M)+H_at+|k|.
```

At `(P,z)=(0,e_0)`, construct the positive atomic operator

```text
D_k=H_at-e_0+|k|+|k|^2/(2M).
```

The infrared cutoff makes `D_k` uniformly invertible on the coupled one-photon
support. Since `e_0-H_1(0;k)=-D_k`, the order-`g^2` self-energy is

```text
Sigma^(2)(P,z)
 =g^2 integral dk
   <c(k),[z-H_1(P;k)]^(-1)c(k)>.
```

No photon-number expansion beyond this sector contributes at this order. To
differentiate without components, put `R_k=-D_k^(-1)` and apply the inverse
derivative to the same atomic vector:

```text
partial_t^2 [z-H_1(t n;k)]^(-1)|_0

 =M^(-1) R_k^2
  +2 M^(-2)(n dot k)^2 R_k^3.
```

The first term appears again in `1-Sigma_z`. Substitute both into the exact
prepared formula. Their `M^(-1)R_k^2` contributions cancel on the same input,
leaving

```text
E''(0)
 =1/M
  -(2g^2/M^2) integral dk (n dot k)^2
     <c(k),D_k^(-3)c(k)>
  +O(g^4).
```

Field parity sends `g` to `-g`, so the isolated branch is even and the next term
is `O(g^4)`. In the rotationally covariant case, average the directional
quadratic form:

```text
1/M_eff
 =1/M
  -(2g^2/(3M^2)) integral dk |k|^2
     <c(k),D_k^(-3)c(k)>
  +O(g^4).
```

Every integrand is nonnegative. The formula therefore predicts mass enhancement
at weak coupling and explains it through an atomic resolvent moment, without
solving the dressed Fock-space eigenstate. This is genuine perturbative
compression in its declared regime, not evidence that perturbation is universally
preferable.

The remaining computation is now sharply localized: evaluate or bound this
integral for a specified `V`, form factor, cutoff, and unit convention. The
atomic resolvent `D_k^(-3)` may still be difficult, but its input is an internal
atomic spectral measure rather than the full field Hilbert space.

## 6. Whole-route cost verdict

| Route | Required large operations | Conditioning | Reuse | Verdict |
| --- | --- | --- | --- | --- |
| nearby-momentum finite difference | three or five full ground-energy solves | solver error is amplified by `delta P^(-2)` | weak | regression only |
| full response Hessian | one full ground eigenpair plus one reduced full-space solve per independent direction | controlled by the dressed spectral gap | ground state and reduced preconditioner | preferred when the full eigenpair is already available |
| exact scalar self-energy | scalar root iterations, each with a `Q` solve, then two tangent `Q` solves per direction | controlled by distance to `sigma(H_Q)` and by `1-Sigma_z` | same `A` factorization/preconditioner | cheaper only if `Q` has reusable structure or the scalar observable avoids a full eigenvector |
| order-`g^2` one-photon reduction | atomic resolvent evaluations under one momentum integral | controlled by infrared support and atomic thresholds | strong across form factors and directions | genuine weak-coupling compression |

The exact Feshbach route is therefore **not generically cheaper**. A one-
dimensional output does not imply a one-dimensional computation; its self-energy
contains the eliminated inverse. Its value is architectural until one of three
extra structures exists:

1. `Q` decomposes recursively into cheap sectors;
2. sparsity/locality gives reusable linear solves;
3. a controlled scale expansion restricts the required sectors, as at order
   `g^2` above.

This answers N4t's cost question. The leading perturbative reduction succeeds;
the exact self-energy notation alone does not.

## 7. Supported frontier and next questions

Supported:

- effective mass is constructed as curvature of the same dressed branch;
- direct differentiation reduces it to one reduced-resolvent response;
- Feshbach differentiation reduces it to a scalar root and reusable tangent
  solves, with its denominator identified as recovered-state normalization;
- exact isospectrality proves both curvatures coincide;
- the finite regression checks the formulas independently;
- at order `g^2`, the field computation compresses to one atomic-resolvent
  momentum integral and predicts mass enhancement.

Open:

- numerical evaluation for a specified hydrogenic potential and form factor;
- uniform control as the infrared modification is removed;
- comparison with the transverse Pauli--Fierz composite rather than the scalar
  Rayleigh model;
- an interacting relativistic model whose sharp stable shell satisfies N4v's
  conditions and whose rest mass can be computed;
- experimental matching and renormalization of the bare mass/cutoff parameters.

The computational continuation fixes `V` and `c(k)` and evaluates the atomic
spectral integral with an error bound. The conceptual continuation is now
constructed in [N4v](04v-relativistic-mass-shell.md): on a sharp single Poincare
orbit, rest energy and curvature mass coincide, whereas N4u's nonrelativistic
band permits them to vary independently. What remains is dynamical realization,
not another kinematic differentiation.

## Edges

- `N4r -> N4u`: pass the exact scalar Schur equation and full-state recovery.
- `N4t -> N4u`: pass the dressed branch, bare preparation, and effective-mass
  target.
- `EM-01/EM-02/EM-03 -> N4u`: pass the gapped composite fiber, independent
  response formula, and analytic-expansion contract.
- `C4u -> N4u`: pass the finite same-branch equality and recovery regression.
- `N4u -> atomic-resolvent evaluation`: pass `D_k`, `c(k)`, the order-`g^2`
  integral, cutoff data, and required error bound.
- `N4u -> relativistic composite lift`: pass the distinction between rest energy
  and curvature mass; N4v constructs their conditional Poincare-shell
  coincidence, while the interacting realization remains open.
- `N4u -> N4v`: pass curvature mass, the same-branch requirement, and the cost
  distinction between eliminating momentum dependence and relocating an inverse.
- `N4u -> N9b`: pass the fixed-momentum atom--field channel structure and reduced
  atomic-resolvent integral as one candidate construction of a coupling measure.

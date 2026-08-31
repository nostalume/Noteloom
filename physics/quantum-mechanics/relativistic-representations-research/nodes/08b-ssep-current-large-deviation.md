# N8b — Equilibrium SSEP Current Large Deviations

Status: exact scaled current generating function bound by microscopic and MFT
theorem contracts; equilibrium reduction, cumulants, Legendre rate, and numerical
evaluation constructed  
Consumes: [N8a exact SSEP collective regression](08a-ssep-exact-collective-regression.md)
and [SSEP response and fluctuation contracts](../sources/ssep-response-contracts.md)  
Produces: one solved nonlinear rare-current prediction and an explicit boundary
between hydrodynamic closure, fluctuation theory, and integrable computation

## Research contract

- **Question:** does N8a's trajectory action compute a non-Gaussian observable,
  and what extra structure makes that computation possible?
- **Presumptions:** one-dimensional SSEP on the infinite lattice with unit
  symmetric bond rate; annealed Bernoulli equilibrium of density `0<rho<1`;
  signed integrated current across the bond `(0,1)`; and the large-time theorem
  contract SR-02/SR-03.
- **Output:** the scaled cumulant-generating function `mu_rho`, its second and
  fourth cumulants, the Legendre rate function `Phi_rho`, its Gaussian center and
  cubic tail, and a reproducible scalar numerical evaluation.
- **Boundary:** the exact closed form comes from SSEP integrability. Diffusive
  hydrodynamics fixes the typical law and quadratic fluctuation scale but does
  not, by itself, construct the full non-Gaussian function.

## 1. The observable is constructed from conservation

N8a used a finite periodic lattice to certify its response error. N8b retains
the same local exchange rule, rate normalization, equilibrium measure, and bond
current but changes the global geometry to the infinite line before taking
`T->infinity`. This change is required by SR-02/SR-03. A fixed finite ring has a
different long-time current problem, so no finite-ring asymptotic is smuggled
through this edge.

Let `J_(x,x+1)(T)` be the number of right exchanges through `(x,x+1)` minus the
number of left exchanges during `[0,T]`. Define

```text
Q_T=J_(0,1)(T).
```

This sign is operational: each particle crossing the origin to the right adds
one and each crossing to the left subtracts one. Summing the microscopic
continuity equation over the right half-line gives the same observable as a
change of stored charge,

```text
Q_T=sum_(x>=1) [eta_x(T)-eta_x(0)],
```

whenever the difference is interpreted through a finite cutoff and then the
cutoff is removed. Thus the current is not an external label; it is the boundary
term of the same conserved density used in N8a.

Diffusion communicates with sites over distance `O(sqrt(T))`. Only that many
occupation differences can contribute coherently to the half-line identity, so
the rare-current scale suggested by conservation and diffusion is

```text
Q_T=O(sqrt(T)).
```

The exact theorem below confirms this scale. It is larger than the typical
fluctuation: because `Var(Q_T)=O(sqrt(T))`, a typical `Q_T` is only `O(T^(1/4))`.
The rate function therefore describes genuinely rare currents, not the central
fluctuation window.

## 2. Exponential tilting asks one verifiable probability question

For real `lambda`, define

```text
Z_T(lambda)=E_rho[exp(lambda Q_T)],

mu_rho(lambda)
  =lim_(T->infinity) T^(-1/2) log Z_T(lambda).
```

Multiplication by `exp(lambda Q_T)` changes the weight of the same trajectories:
positive `lambda` favors positive current and negative `lambda` favors negative
current. Differentiation retains the observable semantics,

```text
partial_lambda log Z_T(lambda)
  =E_(rho,lambda)[Q_T],
```

where the right side is expectation under the normalized tilted trajectory
measure. At `lambda=0`, successive derivatives are the cumulants of the original
current. The tilt is therefore a computable change of measure, not a new kind of
quantization.

It also has a direct generator realization. Write `eta^x` for exchange across
`(x,x+1)`. Away from the observed bond, keep N8a's generator. On `(0,1)`, weight
each off-diagonal transition by its measured current increment:

```text
(L_lambda f)(eta)
  =sum_(x!=0) [f(eta^x)-f(eta)]

   +eta_0(1-eta_1)[exp(lambda)f(eta^0)-f(eta)]

   +eta_1(1-eta_0)[exp(-lambda)f(eta^0)-f(eta)].
```

The Feynman--Kac identity on finite cutoffs is

```text
E_eta[exp(lambda Q_T)f(eta(T))]
  =(exp(T L_lambda)f)(eta).
```

Setting `f=1` and averaging the same expression over Bernoulli initial data
produces `Z_T(lambda)`. Thus the exact theorem in the next section evaluates a
specific deformation of the microscopic dynamics; it does not introduce its
generating function externally. For `lambda!=0`, `L_lambda 1` need not vanish,
so this tilted operator is deliberately not another probability-conserving
Markov generator.

## 3. The exact theorem compresses the path problem to one scalar

SR-03 supplies the annealed step-density theorem

```text
mu_(rho_a,rho_b)(lambda)=F(omega),

F(omega)
  =(1/sqrt(pi)) sum_(n>=1)
       (-1)^(n+1) omega^n/n^(3/2),

omega
  =rho_a(exp(lambda)-1)
   +rho_b(exp(-lambda)-1)
   +rho_a rho_b(exp(lambda)-1)(exp(-lambda)-1).
```

Now impose the equilibrium input `rho_a=rho_b=rho` and compute, rather than
merely quote, the reduction. Since

```text
(exp(lambda)-1)+(exp(-lambda)-1)
  =2(cosh(lambda)-1),

(exp(lambda)-1)(exp(-lambda)-1)
  =-2(cosh(lambda)-1),
```

the theorem's scalar becomes

```text
chi=rho(1-rho),

omega_rho(lambda)=2chi[cosh(lambda)-1],

mu_rho(lambda)=F(omega_rho(lambda)).
```

For real `lambda`, `omega_rho(lambda)>=0`. An equivalent integral, useful beyond
the power-series disk, is

```text
F(omega)
  =(1/pi) integral_(-infinity)^infinity
     log[1+omega exp(-k^2)] dk.
```

The nonlinear trajectory optimization has become the composition of two scalar
maps. This is the computational gain. SR-03 obtains it microscopically by an
integrable determinant/Bethe construction; SR-02 obtains the same function from
the nonlinear MFT boundary problem by an integrable transformation. Neither
derivation follows from conservation and diffusion alone.

## 4. Symmetry and cumulants are deductions from the same function

Because `omega_rho(-lambda)=omega_rho(lambda)`,

```text
mu_rho(-lambda)=mu_rho(lambda).
```

This is the equilibrium left-right symmetry of the current written as an exact
generating-function identity. Every odd scaled cumulant vanishes.

To extract the first nonlinear information, expand only the two scalar maps:

```text
omega_rho(lambda)
  =chi lambda^2+(chi/12)lambda^4+O(lambda^6),

F(omega)
  =(1/sqrt(pi))[omega-omega^2/2^(3/2)+O(omega^3)].
```

Composition on the same `lambda` gives

```text
mu_rho(lambda)
  =(1/sqrt(pi)){
      chi lambda^2
      +[chi/12-chi^2/2^(3/2)]lambda^4
      +O(lambda^6)
    }.
```

Hence the scaled cumulants are

```text
lim_(T->infinity) <Q_T^2>_c/sqrt(T)
  =mu_rho''(0)
  =2chi/sqrt(pi),

lim_(T->infinity) <Q_T^4>_c/sqrt(T)
  =mu_rho''''(0)
  =[2chi-6sqrt(2)chi^2]/sqrt(pi).
```

The second cumulant is the fluctuation consequence of N8a's susceptibility and
mobility. The nonzero fourth cumulant proves that the rare-current law contains
information absent from linear response.

## 5. The rate function is a one-dimensional dual computation

Use the nonnegative rate convention

```text
P_rho(Q_T/sqrt(T) approximately q)
  =exp[-sqrt(T) Phi_rho(q)+o(sqrt(T))].
```

Convex duality of the same tilted observable gives

```text
Phi_rho(q)
  =sup_(lambda in R) [lambda q-mu_rho(lambda)].
```

For `q>=0`, the optimizer is the nonnegative solution of

```text
q=mu_rho'(lambda)
  =2chi sinh(lambda) F'(omega_rho(lambda)),

F'(omega)
  =(1/pi) integral_(-infinity)^infinity
     exp(-k^2)/[1+omega exp(-k^2)] dk.
```

Evenness then gives `Phi_rho(-q)=Phi_rho(q)`. The numerical work is only a
positive scalar integral plus a monotone scalar root solve; no density/current
field discretization is needed after the exact reduction.

Near the typical current, `mu_rho=(kappa_2/2)lambda^2+O(lambda^4)` with
`kappa_2=2chi/sqrt(pi)`. Performing the quadratic dual explicitly yields

```text
Phi_rho(q)
  =sqrt(pi) q^2/(4chi)+O(q^4).
```

SR-03 also gives the far positive-current asymptotic. Converted from its
log-probability convention to the nonnegative convention used here and reflected
by equilibrium symmetry,

```text
Phi_rho(q)
  =pi^2 |q|^3/12-|q|log[chi]+o(|q|)
  as |q|->infinity.
```

Thus one computed object connects a Gaussian center to a cubic rare-event tail.
The cubic tail cannot be inferred by extrapolating the linear-response pole.

## 6. Microscopic and macroscopic routes meet on the same event

The MFT fields in N8a obey

```text
partial_t r+partial_x j=0,

I[r,j]
  =(1/2) integral dt dx
       [j+partial_x r]^2/[2r(1-r)].
```

On the same right-half-line observable, continuity gives

```text
Q_T=integral_0^infinity [r(x,T)-r(x,0)] dx.
```

Tilting by `lambda Q_T` adds precisely this endpoint functional to the path
optimization. In the Hamiltonian formulation it supplies a step terminal datum
for the conjugate field. SR-02 solves that nonlinear boundary-value problem and
returns the same `F(omega)` as the microscopic theorem SR-03.

The equality being checked is therefore

```text
microscopic current through the origin
  =half-line density change
  =MFT endpoint current,

microscopic scaled log moment
  =optimized MFT scaled log moment.
```

It is not a comparison between two merely analogous currents. Both routes receive
the same density, initial law, sign convention, tilt, and observation time.

## 7. What is general and what is special

The construction separates four layers:

```text
conservation
  -> defines the current and its half-line identity;

diffusive constitutive law + mobility
  -> defines the MFT path cost and Gaussian center;

large-deviation duality
  -> converts a scaled log moment into a rate function;

SSEP integrability
  -> evaluates the nonlinear path optimization as F(omega).
```

The first three layers transfer, with changed coefficients and hypotheses, to
many diffusive systems. The fourth is the model-specific compression. Calling
the final answer “hydrodynamic” without this distinction would hide the actual
computational burden.

This also refines the project's global view. A field equation or mean evolution
is an intermediate presentation. Prediction depends on the named observable and
may require a different quotient of histories. Here the useful quotient is not
the mean density alone but the exponential weight of one conserved flux. Exact
integrability then turns an infinite-dimensional optimal-history problem into a
scalar transform. Semantic quotienting chooses the correct object; integrable
structure makes that object cheap to evaluate.

## 8. Computation and verification ledger

The isolated computation is documented in
[computation/08b-ssep-current](../computation/08b-ssep-current/README.md).

| Obligation | Same-input witness | Verdict |
| --- | --- | --- |
| current semantics | microscopic continuity summed on the half-line | exact |
| equilibrium reduction | direct substitution `rho_a=rho_b=rho` into SR-03's `omega` | exact |
| left-right symmetry | `omega_rho(-lambda)=omega_rho(lambda)` | exact |
| second/fourth cumulants | derivatives of the same reduced `mu_rho` | exact |
| rate construction | scalar Legendre transform of `mu_rho` | exact under SR-03 |
| numerical evaluation | integral/series agreement, monotonicity, and stationarity residual | reproducibly checked |
| microscopic/MFT equality | SR-02 and SR-03 evaluate the same tilted current | supported by theorem contracts |
| Gaussian center | local dual of the computed second cumulant | exact |
| cubic tail | SR-03 asymptotic with sign convention converted | supported by theorem contract |
| generic diffusive solvability | no analogue of `F(omega)` constructed | open; explicitly rejected |

## 9. Frontier

N8b completes the promised nontrivial rare-current computation. It shows both a
success and a limitation:

```text
N8a linear response
  -> typical relaxation and variance coefficient;

N8b current large deviation
  -> full non-Gaussian flux cost;

exact scalar evaluation
  -> requires special integrable structure.
```

[N8c dephased quantum chain and SSEP recovery](08c-dephased-quantum-ssep.md)
performs the next discriminating comparison. It computes the quantum diffusion
coefficient, constructs the monitored occupation quotient, and recovers SSEP in
the strong-monitoring slow limit. Its negative result is equally important:
finite-dephasing full current statistics do not follow from the unconditional
Lindblad state alone.

## Edges

- `N8a -> N8b`: pass the local exchange/current convention, `D=1`,
  `sigma_MFT=2rho(1-rho)`, equilibrium initial cost, and trajectory action.
  Replace the finite ring by SR-02/SR-03's infinite-line geometry before taking
  the large-time limit.
- `N8b -> N8c`: pass one named-current hierarchy—mean
  response, variance, fourth cumulant, and rate function—and require the quantum
  model to state which levels it can actually recover.
- `N8b -> N7/manuscript synthesis`: pass the distinction among conservation,
  hydrodynamic fluctuation structure, convex duality, and integrable evaluation.

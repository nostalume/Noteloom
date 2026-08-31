# N8a — Exact SSEP Collective Response and Hydrodynamic Recovery

Status: exact finite-lattice mean-density dynamics, equilibrium susceptibility,
linear conductivity, Fourier response, and a quantitative lattice-to-diffusion
recovery bound supported; equilibrium density large deviations constructed and
the dynamical MFT continuation bound by theorem contract  
Consumes: [N8 collective diffusion response](08-collective-diffusion-response.md)
and [SSEP response contracts](../sources/ssep-response-contracts.md)  
Produces: the first evaluated microscopic collective reduction, including
`chi`, conductivity, `D`, a same-response equality, a continuum error, and a
static large-deviation bridge

## Research contract

- **Question:** can one interacting microscopic model compute every datum left
  symbolic in N8 and recover the hydrodynamic response with an explicit error?
- **Presumptions:** a one-dimensional periodic lattice; continuous-time symmetric
  nearest-neighbor exchange at unit bond rate; grand-canonical Bernoulli
  equilibrium with density `0<rho<1`; weak site chemical-potential source; and
  linear response. Diffusive hydrodynamic and trajectory-large-deviation claims
  additionally consume SR-01/SR-02.
- **Output:**

  ```text
  chi(rho)=rho(1-rho),
  sigma_cond(rho)=rho(1-rho),
  D=sigma_cond/chi=1,

  R_latt(omega,k)
    =chi lambda(k)/(lambda(k)-i omega),
  lambda(k)=4 sin^2(k/2),
  ```

  together with its exact comparison to N8's continuum response.
- **Boundary:** SSEP is a stochastic interacting-particle model, not a unitary
  quantum theory. It proves that the collective construction can be fully
  executable; it does not settle quantum transport, momentum-coupled fluids,
  anomalous diffusion, or generic many-body coefficient computation.

## 1. Candidate audit: why this microscopic model comes first

| Candidate | Closure and coefficients | Additional burden | Verdict |
| --- | --- | --- | --- |
| independent random walkers | exact | no interaction or exclusion | too weak |
| SSEP | exact mean closure, algebraic coefficients, rigorous hydrodynamic/LDP contracts | stochastic rather than unitary | selected benchmark |
| dephased quantum hopping chain | diffusion is accessible | Lindblad choice and coherent-mode elimination | next quantum comparator |
| Hamiltonian XXZ-type chain | physically stronger | ballistic channels, integrability, and hard diffusion extraction | premature first test |

SSEP is selected because it closes the whole requested computation without
pretending that symmetry alone fixes transport. Its limitation—stochastic rather
than quantum dynamics—is explicit and becomes the discriminating question for the
next model.

This does not detach N8a from the previous field/algebra spine. The common typed
construction is

```text
observable algebra + stationary state + dynamics generator + source
  -> response of the named observable.
```

Quantum dynamics differentiates an observable by a Hamiltonian commutator (or a
quantum dynamical generator); SSEP differentiates it by a Markov generator. N8a
changes that one input while retaining the conserved density, source, response,
and recovery target. It therefore tests the collective selector and its
computability, not the earlier CAR/CCR quantization theorem. A later quantum node
must construct the bridge between these dynamics rather than treating SSEP as a
quantum derivation.

## 2. Exclusion constructs the microscopic state space and dynamics

Let the periodic lattice be

```text
Lambda_N=Z/NZ.
```

A configuration is a function

```text
eta:Lambda_N->{0,1},
```

where `eta_x=1` means that site `x` is occupied. For the bond `(x,x+1)`, let
`eta^(x,x+1)` exchange the two occupations. The Markov generator acts on an
observable `f` by

```text
(L_N f)(eta)
 =sum_(x in Lambda_N) [f(eta^(x,x+1))-f(eta)].
```

This definition already enforces exclusion: if the two occupations agree, the
exchange changes nothing. The total number

```text
Q(eta)=sum_x eta_x
```

is conserved because every generator term only permutes two entries.

The rightward instantaneous current through bond `(x,x+1)` is

```text
j_(x,x+1)(eta)=eta_x-eta_(x+1).
```

Apply the generator to the same local density observable `eta_x`:

```text
L_N eta_x
 =(eta_(x-1)-eta_x)+(eta_(x+1)-eta_x)
 =j_(x-1,x)-j_(x,x+1).
```

This is the microscopic continuity equation. The current was not guessed from a
continuum analogy; it is the bond contribution whose discrete divergence equals
the generator action on the conserved observable.

## 3. The mean density closes exactly

Let

```text
rho_x(t)=E[eta_x(t)].
```

The Markov evolution identity `dE[f]/dt=E[L_Nf]`, evaluated on the same
`f=eta_x`, gives

```text
d rho_x/dt
 =rho_(x-1)+rho_(x+1)-2rho_x
 =Delta_d rho_x.
```

No factorization of a two-point function was used. Exclusion interactions cancel
inside the gradient current, so the one-point observable is an invariant closed
sector of the generator.

This is the first strong compression:

```text
2^N-state probability evolution
  -> N-dimensional exact mean-density evolution.
```

It is observable-relative. Higher correlations and rare trajectories are not
determined by the mean equation.

## 4. Equilibrium constructs susceptibility without a Kubo sum

For `0<rho<1`, define the Bernoulli product measure

```text
nu_rho(eta)
 =product_x rho^(eta_x)(1-rho)^(1-eta_x).
```

An exchange preserves `sum_x eta_x`, so it preserves the weight of every
configuration. Forward and reverse exchange rates are equal; therefore
`nu_rho` is reversible.

Use the dimensionless chemical potential

```text
mu=log[rho/(1-rho)].
```

Solving this same equation for density gives

```text
rho=e^mu/(1+e^mu).
```

Differentiate the constructed equilibrium state:

```text
chi(rho)=d rho/d mu=rho(1-rho).
```

The same number is the one-site fluctuation:

```text
Var_(nu_rho)(eta_x)
 =E[eta_x^2]-E[eta_x]^2
 =rho-rho^2
 =rho(1-rho)
 =chi(rho),
```

because `eta_x^2=eta_x`. Static response and equilibrium variance coincide on
the same microscopic occupation variable.

## 5. A weak chemical-potential field computes conductivity

Let `h_x` be a weak external chemical-potential source. Across `(x,x+1)`, set

```text
E_x=h_(x+1)-h_x.
```

Choose locally detailed-balanced exchange rates

```text
10 -> 01: exp(E_x/2),
01 -> 10: exp(-E_x/2).
```

Their ratio is `exp(E_x)`, which equals the ratio of the source-weighted
equilibrium probabilities after and before a particle moves right. Thus the
source coupling is constructed from equilibrium semantics rather than inserted
as an arbitrary drift.

The rightward current observable becomes

```text
j_x^h
 =eta_x(1-eta_(x+1))exp(E_x/2)
  -eta_(x+1)(1-eta_x)exp(-E_x/2).
```

Linearize its expectation about uniform `nu_rho`. The zero-field part is exactly
`rho_x-rho_(x+1)`. In the coefficient of `E_x`, evaluate both occupation events
on the same product equilibrium:

```text
(1/2)E[eta_x(1-eta_(x+1))
       +eta_(x+1)(1-eta_x)]
 =(1/2)[rho(1-rho)+rho(1-rho)]
 =rho(1-rho).
```

Hence

```text
E[j_x^h]
 =-(delta rho_(x+1)-delta rho_x)
   +chi(rho)(h_(x+1)-h_x)
   +O(delta^2,h^2,delta h).
```

The coefficient multiplying the thermodynamic field is N8's conductivity:

```text
sigma_cond(rho)=chi(rho)=rho(1-rho).
```

Therefore the Einstein ratio is computed, not assumed:

```text
D=sigma_cond/chi=1.
```

## 6. The exact lattice response and the N8 response share one source

Take the discrete divergence of the previous current. To linear order,

```text
partial_t delta rho
 =Delta_d delta rho-chi Delta_d h.
```

For the Fourier mode `exp(-i omega t+ikx)`, the positive lattice relaxation
symbol is

```text
lambda(k)=2-2cos k=4sin^2(k/2),
-Delta_d -> lambda(k).
```

Apply both operators to the same mode:

```text
(-i omega+lambda(k))delta rho(omega,k)
 =chi lambda(k)h(omega,k).
```

Thus the exact finite-lattice linear response is

```text
R_latt(omega,k)
 =delta rho/h
 =chi lambda(k)/(lambda(k)-i omega).
```

N8's hydrodynamic route, on the same source and density observable with `D=1`,
gives

```text
R_hyd(omega,k)=chi k^2/(k^2-i omega).
```

The only difference is now the explicit lattice-versus-continuum Laplacian
symbol. No microscopic coefficient remains hidden.

## 7. The continuum error is an algebraic identity plus one symbol bound

For `|k|<=pi`, the trigonometric remainder gives

```text
0<=k^2-lambda(k)<=k^4/12.
```

Evaluate the two response maps on the same `(omega,k)` and subtract before
estimating:

```text
R_latt-R_hyd
 =chi [lambda/(lambda-iomega)-k^2/(k^2-iomega)]
 =chi iomega(k^2-lambda)
       /[(lambda-iomega)(k^2-iomega)].
```

For real `omega` and `(omega,k)!=(0,0)`, this yields the explicit bound

```text
|R_latt-R_hyd|
 <=chi |omega| k^4
     /[12 |lambda-iomega| |k^2-iomega|].
```

Under diffusive scaling

```text
k=epsilon q,
omega=epsilon^2 Omega,
```

with fixed nonzero hydrodynamic datum `(Omega,q)`, the right side is `O(epsilon^2)`.
The response reduction is therefore quantitatively second-order in lattice
spacing for this mode.

The time-domain comparison is equally direct. Since `lambda(k)<=k^2`, the mean
value theorem gives

```text
|exp[-lambda(k)t]-exp[-k^2t]|
 <=t[k^2-lambda(k)]exp[-lambda(k)t]
 <=t k^4 exp[-lambda(k)t]/12.
```

With `t=T/epsilon^2` and `k=epsilon q`, the semigroup error is again
`O(epsilon^2)` at fixed macroscopic time.

## 8. Ordered limits and conservation survive exactly

For `omega!=0`, set `k=0`:

```text
R_latt(omega,0)=0.
```

The total particle number cannot respond dynamically inside the closed ring.

For `k!=0`, take the static limit:

```text
R_latt(0,k)=chi.
```

Then taking `k->0` recovers the equilibrium susceptibility. Reversing the limits
gives zero. Thus N8's noncommuting limits are already exact on the lattice; they
are not artifacts of the continuum approximation.

## 9. Static large deviations reconstruct the same susceptibility

In a block of `M` equilibrium sites, let

```text
r_M=(1/M)sum_(x=1)^M eta_x.
```

For `r=m/M`, product equilibrium gives the binomial probability

```text
P(r_M=r)
 =binomial(M,m)rho^m(1-rho)^(M-m).
```

Applying Stirling's formula to this same probability constructs

```text
P(r_M approximately r)
 =exp[-M I_rho(r)+o(M)],

I_rho(r)
 =r log(r/rho)
  +(1-r)log[(1-r)/(1-rho)].
```

The typical density and fluctuation curvature follow by differentiation:

```text
I_rho'(rho)=0,
I_rho''(rho)=1/[rho(1-rho)]=chi(rho)^(-1).
```

Therefore three constructions on the same occupation variable coincide:

```text
static response chi
 =equilibrium variance per site
 =inverse curvature of the density rate function.
```

This is the first precise bridge from N8's response view to the preferred large-
deviation view of statistical mechanics.

## 10. Dynamic fluctuations add one convention-sensitive mobility

The full density/current trajectory is not determined by its mean. SR-01/SR-02
supply the diffusive-scaling theorem contract

```text
partial_t r+partial_x j=0,

I_[0,T](r,j)
 =(1/2)integral_0^T dt integral dx
   [j+partial_x r]^2/sigma_MFT(r),

sigma_MFT(r)=2r(1-r).
```

In the equivalent denominator convention,

```text
I_[0,T](r,j)
 =integral dt dx [j+partial_x r]^2/[4r(1-r)].
```

The factor two does not contradict Section 5:

```text
sigma_MFT=2 sigma_cond=2chi D.
```

`sigma_cond` multiplies an applied thermodynamic field in the mean current;
`sigma_MFT` is the current-noise covariance convention used in the trajectory
action.

Set the action integrand to zero on the same path:

```text
j=-partial_x r
  -> partial_t r=partial_x^2 r.
```

The deterministic diffusion equation is exactly the zero-cost trajectory of the
large-deviation theory. Large deviation is therefore not an appended correction
to diffusion: it reconstructs diffusion as its typical path and adds the costs of
atypical currents.

N8a does not solve the nonlinear variational problem for a specified rare event.
That is now a well-typed downstream computation rather than an undefined appeal
to fluctuations.

## 11. Computability and reconstruction verdict

The entire mean-response route has low semantic depth:

```text
exchange generator
  -> exact conserved-density sector
  -> one lattice Fourier symbol
  -> exact response;

Bernoulli equilibrium
  -> one derivative / variance
  -> chi and sigma_cond;

lattice symbol
  -> one remainder inequality
  -> certified hydrodynamic response.
```

No diagonalization of the `2^N` Markov generator, eigenstate sum, perturbative
diagram, or simulation is needed. The gain comes from a gradient current and an
observable-invariant sector—not merely from renaming microscopic variables.

The large-deviation reconstruction changes the primitive prediction from one
mean history to a probability cost over density/current histories. It recovers
the old successful diffusion equation as its zero-cost path and predicts rare
current statistics unavailable from the mean equation alone. Its nonlinear
variational problems can still be hard; the reconstruction does not promise a
universal solver.

## 12. Verification ledger and frontier

| Obligation | Same-input witness | Verdict |
| --- | --- | --- |
| microscopic conservation | `L_N eta_x=j_(x-1,x)-j_(x,x+1)` | exact |
| mean closure | expectation of the same generator identity | exact |
| susceptibility | `d rho/dmu=Var(eta_x)` | exact |
| conductivity | derivative of the detailed-balanced bond current at `E=0` | exact linear response |
| Einstein relation | `sigma_cond/chi=1` | exact |
| response recovery | replace only `lambda(k)` by `k^2` on the same source | explicit `O(epsilon^2)` bound |
| conservation/static limits | evaluate the exact lattice response in both orders | exact |
| static large deviation | binomial probability plus Stirling | supported |
| dynamic large deviation | SR-01/SR-02 scaling theorem contract | supported under contract; N8b evaluates one event |
| unitary quantum transport | no unitary dynamics in SSEP | open; next comparator |

Available downstream nodes:

- [N8b equilibrium current large deviations](08b-ssep-current-large-deviation.md)
  constructs the tilted current, exact scaled cumulants, and Legendre rate from
  this node's action and compares it with the microscopic theorem;
- construct a locally dephased quantum hopping chain and test which exact SSEP
  edges survive coherent dynamics and adiabatic elimination;
- replace one conserved density by a coupled density matrix to test finite-density
  charge/energy/momentum mixing.

## Edges

- `N8 -> N8a`: pass the named-density response and coefficient/remainder
  obligations; N8a evaluates them in one microscopic model.
- `N8a -> N8b`: pass `D=1`,
  `sigma_MFT=2rho(1-rho)`, the equilibrium rate function, and the path action.
- `N8a -> quantum diffusion comparator`: pass the exact gradient-model benchmark
  and require any quantum reduction to recover the same response/coefficient
  objects with its approximation cost included.
- `N8a -> N7/manuscript synthesis`: pass the first complete collective
  microscopic-to-response-to-fluctuation reconstruction and its stochastic
  boundary.

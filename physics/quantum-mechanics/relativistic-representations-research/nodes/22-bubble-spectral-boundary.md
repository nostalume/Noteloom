# Spectral threshold response and pole obstruction

Status: one subtracted bubble generates its continuum and finite-resolution
response; an isolated Fock pole at the touching threshold is rejected

## Obstruction

Node 20 leaves one nonlocal massive--massless bubble. The same analytic object was
expected to supply a dressed pole and an open channel, but those endpoints need
not coexist when the continuum touches the nominal shell.

## Construct the common boundary

For `mu=m^2>0`, subtract at a real `P_0<mu` before assigning a finite value:

```text
B(P;P_0)
 =-integral_0^1 dy log[(mu-yP-i0)/(mu-yP_0)].   (22.1)
```

Below threshold define

```text
b(P)=1+(mu-P)/P log(1-P/mu),  b(0)=0.
```

Differentiating both the parameter integral and `b` gives

```text
-1/P-mu/P^2 log(1-P/mu),
```

so the common initial value and derivative construct

```text
B(P;P_0)=b(P)-b(P_0).                           (22.2)
```

For `s>mu`, the logarithm crosses its cut on `y in (mu/s,1)`. Its discontinuity
therefore generates

```text
rho_B(s)=1-mu/s,

B(P;P_0)=(P-P_0)integral_mu^infinity
 rho_B(s)/[(s-P-i0)(s-P_0)]ds.                 (22.3)
```

At `d=4`, the packet coefficient `C_4(P)=2mu(2P-mu)` gives

```text
rho_Sigma(s)=2mu(2s-mu)(1-mu/s),  s>=mu,
rho_Sigma(mu)=0,
lim_(s->mu+)rho_Sigma(s)/(s-mu)=2mu.            (22.4)
```

## Let the pole obstruction change the observable

The free shell and lightest scalar-plus-massless-spin-two threshold coincide:

```text
P_shell=P_threshold=mu.
```

The same primitive calculates

```text
lim_(P->mu-)b'(P)=+infinity,
C_4(mu)=2mu^2!=0.                               (22.5)
```

Hence `Z^(-1)=1-Sigma'(P_pole)` is not admitted at `P_pole=mu` in this one-loop
Fock representation. A local counterterm cannot cancel the nonanalytic logarithmic
derivative. This rejects an isolated residue, not all dressed or inclusive
particle constructions.

A detector with finite excess-mass resolution instead generates the spectral
effect

```text
D_Delta=E_Q([mu,mu+Delta]),  Delta>0,
D_Delta D_Lambda=D_min(Delta,Lambda).           (22.6)
```

For preparation `eta` and departure `B`,

```text
<Beta,D_Delta Beta>
 =<eta,M_B([mu,mu+Delta])eta>,  Beta=B eta.     (22.7)
```

Thus detector response and visible-measure mass are the same composite without an
intermediate pole.

## Construct the minimal visible realization

On an admitted band `[mu,mu+Lambda]`, define

```text
J(Lambda)=integral_mu^(mu+Lambda)rho(s)ds,
H_Lambda=L^2([mu,mu+Lambda],ds),
psi_Lambda(s)=1_band(s)sqrt(rho(s)/J(Lambda)).
```

Then `||psi_Lambda||=1` and

```text
F(Delta|Lambda)
 =<psi_Lambda,D_Delta psi_Lambda>
 =J(Delta)/J(Lambda).                           (22.8)
```

For the generated density, putting `x=s-mu` yields

```text
rho_Sigma(mu+x)=2mu[2x-mu+mu^2/(mu+x)],

J_mu(Delta)
 =2mu[Delta^2-mu Delta+mu^2 log(1+Delta/mu)].   (22.9)
```

Differentiation returns `rho_Sigma(mu+Delta)`. Positivity makes `J_mu` monotone;
an overall positive action/cut normalization cancels from

```text
F_mu(Delta|Lambda)=J_mu(Delta)/J_mu(Lambda).
```

Only after this exact construction does expansion expose

```text
J_mu(Delta)=mu Delta^2+(2/3)Delta^3+O(Delta^4/mu),
F_mu(Delta|Lambda)
 =(Delta/Lambda)^2[1+O((Delta+Lambda)/mu)].      (22.10)
```

## Retained interface and boundary

```text
CompileThresholdResponse(mu,P_0,Delta,Lambda,normalization)
 -> subtracted boundary + density + nested effects
    + cell mass + conditional response + pole diagnostic
 | refusal(mu<=0, P_0>=mu, or invalid window).
```

Certificates compare (22.2) with (22.3), differentiate (22.9), check nesting and
normalization cancellation, and enforce the pole refusal. The finite-resolution
law is presently a gauge-fixed spectral diagnostic: [node 24](24-external-ideal-observable-descent.md)
shows that it does not yet descend through the packet’s external Ward quotient.
Absolute normalization, coherent/inclusive completion, and all-orders infrared
behavior remain open.

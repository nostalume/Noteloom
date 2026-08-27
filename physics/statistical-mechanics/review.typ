#import "../lib.typ": *
#import "@preview/physica:0.9.8": *

#show: mine.with(
  title: "Statistical Mechanics Review",
)

#let vf(content) = $upright(bold(content))$

= Ideal Gas

Given general parameters, we have general exchange system or grand canonical system:

$
  H(bold(p),bold(q)) = 1/(2m) sum_i^(d N) p_i^2
  = sum_i^(d N) u_i^2 quad u_i = sqrt(2 m E) p_i
$

$
  D(E, V, N) &= integral 1/(N! (2pi planck)^d) d^(N d) q d^(N d) p delta(1/(2m) sum_i^(d N) p^2_i - E) \
  &= V^N/N! (sqrt(2 m E)/planck)^(N d) 1/E integral d^M u delta(sum_i^M u_i^2 - 1) quad (M = N d)\/(delta(E x) = E^(-1) delta(x)) \
$

Where we integral on a solid ball with unit radius, thus the radial part integral must be unit. Also, the delta function will be reduced to $delta(sum_i u_i^2 - 1) = delta(bold(u)^2-1) = 1/2 (delta(bold(u) + 1) + delta(bold(u)-1))$ with ball integral $d^M u = bold(u)^(M-1) d bold(u) d italic(Omega)_M$.

$
  D(E,V,N) = V^N/(N!) (sqrt(2m)/planck)^(N d) E^(1/2 N d - 1) 1/2 italic(Omega)_(N d)
$

$
  italic(Omega)_M = (2pi^(M/2))/(Gamma(M/2))
$

$
  Z(beta,V,N) & = 1/(N!) integral dd(x_i^d, p_i^d)/(2 pi planck)^d e^(- beta bold(p)^2_i \/ 2m) \
              & = V^N/N! (integral_(-infinity)^infinity dd(p)/(2pi planck) e^(- beta bold(p)^2 \/ 2m))^(N d) \
              & = V^N/N! (2 pi planck)^(- N d) ((2 pi m)/beta)^(N d \/ 2) \
              & = V^N/N! (m/(2 pi beta planck^2))^(N d \/ 2)
$

$
  Z(beta,V,N) = 1/N! (V/lambda_beta^d)^N, quad lambda_beta = ((2 pi beta planck^2)/(m))^(1/2)
$

$
  italic(Xi)(beta, V, mu) = sum_(N=0)^(infinity) e^(beta mu N) Z(beta, V, N) = sum_(N=1)^(infinity) 1/N! ((V e^(beta mu))/(lambda_beta^d))^N = exp((V e^(beta mu))/lambda_beta^d) \
$

$
  Omega = - p V = - beta^(-1) ln italic(Xi) = -beta^(-1) V e^(beta mu) lambda_beta^(- d) = - beta^(-1) V e^(beta mu) (m/(2pi beta planck^2))^(d\/2)
$

$
  p = beta^(-1) e^(beta mu) lambda_beta^(-d) = beta^(-1) e^(beta mu) (m/(2pi beta planck^2))^(d\/2)
$

$
  n = N/V = - 1/V pdv(Omega, mu) = e^(beta mu) lambda_beta^(-d)
$

$
  mu = beta^(-1) ln (N lambda^d)/V
$

$
  p V = beta^(-1) e^(beta mu) lambda_beta^(-d) V = N/beta = N k_B T
$

$
  expval(H) = - pdv(ln italic(Xi), beta) + mu N = - (V mu e^(beta mu))/(lambda_beta^d) + mu N + V e^(beta mu) d/(lambda_beta^(d+1)) dot 1/2 lambda_beta^(-1) beta^(-1/2) beta^(-1/2) = (N d)/2 beta^(-1)
$

$
  expval(H) - S T - mu expval(N) & = Omega \
               S & = (expval(H) - mu expval(N) - Omega)/T \
               S & = k beta^(-1) ( beta pdv(Omega, beta) - mu pdv(Omega, mu) - Omega) \
               S & = k (beta pdv(ln Xi, beta) - mu beta^(-1) pdv(Xi, mu) - ln Xi)
$

$
  S = - pdv(Omega,T) = - pdv(Omega,beta) dv(beta,T) = 1/(k_B T^2) pdv(Omega,beta) = k_B beta pdv(Omega,beta)
$

Set $k_B = 1$ as Gibbs entropy:

$
  S &= V/(lambda_B^d)e^(beta mu) ((d+2)/2 - mu beta) \
  &= ln Xi + beta expval(H) - beta mu expval(N)
$

The state relation can also be computed:

$
  F = - beta^(-1) ln Z = beta^(-1) [N (ln V - d ln lambda_beta) - ln N!]
$

$
  - p = - pdv(F, V) & = - beta^(-1) N/V \
                p V & = N k_B T
$

$
  pdv(ln lambda_beta, beta) = 1/2 beta^(-1)
$

$
  expval(H) = - pdv(ln Z, beta) = (N d)/2 beta^(-1) = (N d)/2 k_B T
$

$
  expval(H^2) - expval(H)^2 = "Var"(H) = - pdv(expval(H), beta) = (N d)/2 beta^(-2)
$

$
  ("Var"(H))^(1/2)/(expval(H)) = (2/(d N))^(1/2) ->(N -> infinity) = 0
$

$
  beta expval(H) - S = ln Z
$

$
  S = - pdv(F,T) = - pdv(F,beta) dv(beta,T) = 1/(k_B T^2) pdv(F,beta) = k_B beta pdv(F,beta)
$

Set $k_B = 1$ as Gibbs entropy:

$
  S = beta expval(H) - ln Z & = (N d)/2 + (N (ln V - d ln lambda_B) - ln N!) \
  &= N (ln V/(lambda_B^d) + d/2 - ln N!)\
  &approx N (ln V/(lambda_B^d) + (d+2)/2 - ln N)
$

The notorious _Maxwell Velocity Distriution_ can also be established by given empirical vector of momentum.

$
  L (bold(p)) = lim_(n->infinity) 1/n sum_(i=1)^n delta(p_i - p) \
$

$
  expval(L(bold(p))) & = (integral d^d p_1 delta(p_1 - p) e^(- beta p_1^2\/2m))/(integral d^d p_1 e^(- beta p_1^2\/2m)) \
                     & =(beta/(2 pi m))^(d/2) e^(- beta p^2\/2m)
$

Typically, transform the variables to $d^3 p -> p^2 d p d italic(Omega) = 4 pi p^2 d p$.

$
  H_u = 1/2 k u^2 => zeta(beta) := integral_(-infinity)^infinity e^(- beta k u^2 \/2) = ((2pi)/(k beta))^(1/2)
$

$
  expval(H)_u = - pdv(ln zeta(beta), beta) = 1/2 beta^(-1) = 1/2 k_B T
$

$
  h = bold(p)^2/(2m) + p_theta^2/(2 I) + p^2_phi.alt/(2 I sin^2 theta) - mu_0 bold(E) dot hat(bold(n))
$

Assume $bold(E) = E hat(z)$, $u_d (theta) = - mu_0 E cos theta$.

$
  d m = (d^3 p d^3 q)/(2 pi planck)^3 dd(theta, p_theta, phi.alt, phi.alt)/(2 pi planck)^2
$

$
  Z_1 (beta, V) &= V/(lambda_beta^3) integral_0^(2 pi) d phi.alt integral_0^pi d theta integral_(-infinity)^(infinity) (d p_theta)/(2 pi planck) integral_(-infinity)^infinity (d p_phi.alt)/(2 pi planck) exp(- beta/(2I) (p_theta^2 + p_phi.alt^2 \/ sin^2 theta) - beta u_d (theta)) \
  &= V/(lambda_beta^3) I/(beta planck^2) integral_0^pi d theta sin theta exp(- beta mu_0 E cos theta) = (dots) (sinh (beta mu_0 E))/(beta mu_0 E)
$

$
  Z_n = (Z_1)^n/n!
$

$
  phi(beta) = lim_(n -> infinity) 1/n ln Z_n = ln Z_1 - ln n
$

$
  F = - beta^(-1) phi(beta) = - beta^(-1) (ln Z_1 - ln n)
$

$
  expval(h) = - pdv(ln Z_1, beta) = 3/2 beta^(-1) + beta^(-1) + mu_0 E coth (beta mu_0 E) + beta^(-1) = 7/2 beta^(-1) + mu_0 E coth (beta mu_0 E)
$

$
  expval(bold(d)) = mu_0 expval(hat(bold(n))) = - pdv(F, E) hat(z) = [mu_0 coth (beta mu_0 E) - 1/(beta E)] hat(z)
$

Suppose without electric field $bold(E)$:

$
  Z_1 (beta, V) = (dots) I/(beta planck^2) integral_0^pi d theta sin theta = (dots) (2 I)/(beta planck^2)
$

$
  expval(h) = 5/2 beta^(-1)
$

$
  "Var"(h) = pdv(ln Z_1, beta, 2) = - pdv(expval(h), beta) = 5/2 beta^(-2)
$

$
  ("Var"(H)^(1/2))/(expval(H)) = (5/(d N))^(1/2) ->^(N -> infinity) 0
$

= Spins in External Magnetic Field

Use hat to denote the Hamiltonian else is the magnetic field tensity.

$
  sigma("up") = 1, sigma("down") = -1 \
  hat(H) = - mu_0 H sum_(i=1)^N sigma_i \
$

We should transverse all states of $sigma$ for each $i$:

$
  Z = sum_(sigma_1) ... sum_(sigma_N) e^(- beta hat(H)) = sum_(sigma_1) e^(beta mu_0 H sigma_1) ... sum_(sigma_N) e^(beta mu_0 H sigma_N) = product_i^N sum_sigma_i (...) = 2 cosh^N (beta mu_0 H)
$

$
  F(T,H,N) = - beta^(-1) log Z = - N beta^(-1) log (2 cosh (beta mu_0 H)) \
$

$
  M = - (partial F)/(partial H) = N mu_0 tanh beta mu_0 H \
  E = (partial (beta F))/(partial beta) = - N mu_0 H tanh (beta mu_0 H) \
  E = - M H ~ hat(H) = - mu_0 H sum_(i=1)^N sigma_i
$

= Noninteracting Quantum Systems

In a quantum system, we have energy levels $epsilon_1, epsilon_2, dots$ and each level has a degeneracy $g_j$ (the number of available quantum states at that energy).

- Macrostates: $n_i in {n_1,n_2,dots}$, where $n_i$ is the density of particles at energy level $i$.
- Occupancy ($nu_j$): In the thermodynamic limit, we define the mean number of particles per state: $nu_j = n_j/g_j$.

Bosons is a *stars and bars* problem:

$
  Omega_(B E,j) = (n_j + g_j - 1)!/(n_j ! (g_j - 1)!)
$

$
  s_(B E) (v_j) = (v_j + 1) ln (v_j + 1) - v_j ln v_j
$

Fermions is a *slots* problem:

$
  Omega_(F D,j) = (g_j !)/(n_j ! (g_j - n_j)!)
$

$
  s_(F D)(v_j) = - (v_j ln v_j + (1-v_j) ln (1-v_j))
$

$
  S = sum_(i) g_j s (v_j)
$

Constraints:

- $sum g_j v_j = N$
- $sum g_j v_j epsilon_j = H$

$
  cal(L)_j [v_j] = s(v_j) - alpha v_j - beta epsilon_j v_j
$

$
  pdv(s, v_j) - (alpha + beta epsilon_j) = 0
$

$
  pdv(s_(B E), v_j) = ln (v_j + 1)/(v_j) = alpha + beta epsilon_j => v_j = 1/(e^(alpha + beta epsilon_j) - 1)
$

$
  pdv(s_(F D), v_j) = ln (1- v_j)/(v_j) = alpha + beta epsilon_j => v_j = 1/(e^(alpha + beta epsilon_j) + 1)
$

$
  n(epsilon_j) = n_j = g_j/(e^(alpha + beta epsilon_j) minus.plus 1)
$

$
  Z_(B E, i) = sum_(n=0)^(infinity) e^(- beta n (epsilon_i - mu)) = 1/(1 - epsilon^(- beta(epsilon_i - mu)))
$

$
  Z_(F D,i) = sum_(n=0)^1 e^(- beta n (epsilon_i - mu)) = 1 + e^(- beta (epsilon_i - mu))
$

$
  italic(Xi)_(B E\/F D) = product_i Z_(B E\/F D,i)
$

The single particle density of states per unit volume $g(epsilon)$:

$
  g (epsilon) = 1/V sum_i delta (epsilon - epsilon_i)
$

Spin degeneracy is $g_s$

$
  g(epsilon) = g_s integral (d^d p)/(2pi planck)^d delta (epsilon - epsilon(bold(p))) = g_s italic(Omega)_d p^(d-1)/(2 pi planck)^d (dv(epsilon, p))^(-1)
$

$
  epsilon(bold(p)) = C p^alpha => p = (epsilon/C)^(1/alpha)
$

$
  dv(p, epsilon) = 1/alpha epsilon^(1/alpha - 1) C^(- 1/alpha)
$

$
  g(epsilon) &= g_s italic(Omega)_d (epsilon/C)^((d-1) \/ alpha) 1/(2pi planck^d) 1/alpha epsilon^(1\/alpha - 1) C^(-1\/alpha) \
  &= (g_s italic(Omega)_d)/(2 pi planck)^d 1/alpha epsilon^(d/alpha - 1) C^(- d/alpha) Theta(epsilon)
$

Where $Theta(epsilon) = cases(0 "if" epsilon < 0, 1 "if" epsilon > 0) thin$ , is a step function.

$
  epsilon(bold(p)) = bold(p)^2/(2m) => C = 1/(2m), alpha = 2
$

$
  g(epsilon) = (g_s Omega_d)/(2 pi planck)^d 1/2 2m^(d/2) epsilon^(d/2 - 1) Theta(epsilon)
$

$
  v (epsilon)(beta,mu) = 1/(e^(beta(epsilon - mu)) minus.plus 1)
$

$
  N (beta,V,mu) = V integral_(-infinity)^(infinity) d epsilon thin g (epsilon) v (epsilon) = V integral^(infinity)_(-infinity) d epsilon thin n(epsilon)
$

$
  expval(n) = N/V
$

In boson case, suppose $beta ~ T^(-1)$ is *fixed*, we have both constraint:

- $n(epsilon) > 0 => epsilon > mu$, therefore there exist a minimum of $epsilon$, $epsilon_0 >= mu$.
- $expval(n) = integral (dots) d epsilon$ must exactly match.

Then:

- $expval(n)$ monotonically increase in $mu$.
- its maximum possible value is $epsilon_0$.
- the maximum integration $expval(n)_c$ is the critical density.

Now:

- If $expval(n) <= expval(n)_c (T)$: there's a unique $mu < epsilon_0$ solving integration.
- If $expval(n) >= expval(n)_c (T)$: no solution exists, any possible $mu$ can't make the integral reaching $expval(n) >= expval(n)_c (T)$.

That's, the *continuum assumption* of energy density failed. Where the freedom *freeze* at low enough temperature in which energy is the base energy $epsilon_0$.

$
  expval(n)(beta) &= 1/V (g_s (epsilon_0))/(e^(beta(epsilon_0 - mu)) - 1) + integral_0^infinity d epsilon' thin g(epsilon' + epsilon_0)/(e^(beta epsilon') - 1), quad epsilon' = epsilon - epsilon_0 \
  &= n(epsilon_0) + integral_(epsilon_0)^infinity n(epsilon) = n(epsilon_0) + expval(n)_c (beta)
$

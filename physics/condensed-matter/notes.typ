#import "../lib.typ": *
#import physica: *
#import fletcher: diagram, edge, node

#show: mine.with(
  title: "Condensed Matter Notes",
  eq-numbering: "(1.1)",
  eq-chapterwise: true,
)

= Lattice vibrations

$
  bold(r)_(n alpha) (t) = bold(R)_(n alpha)^((0)) + bold(u)_(n alpha) (t)
$

$abs(bold(u)) << a$ where $a$ is lattice constant.

$
  L = T - U = 1/2 sum_(n alpha) M_alpha (abs(bold(u))_(n alpha)^2 - U({ bold(u) }) )
$

$
  U = U_0 + 1/2 sum_(n, alpha, i; m, beta, j) lr(pdv(U, u_(n alpha, i), u_(m beta, j))bar)_0 u_(n alpha, i) u_(m beta, j)
$

Where $i, j in {1, 2, ..., d}$ is the index of the spatial dimension.

$
  Phi_(n alpha, i; m beta, j) equiv lr(pdv(U, u_(n alpha, i), u_(m beta, j))bar)_0
$

$
  M_alpha dot.double(u) = - sum_(m,beta,j) Phi_(n alpha, i; m beta, j) u_(m beta, j)
$

= Coherent states

== Bosonic coherent states

We begin by defining the displacement operator that generates the coherent state from the vacuum:
$
  D(hat(phi.alt)) equiv exp(sum_beta phi.alt_beta hat(a)_beta^dagger)
$

Our goal is to show that this state satisfies the eigenvalue equation $hat(a)_alpha ket(phi.alt) = phi.alt_alpha ket(phi.alt)$.

To proceed, we need a useful identity for commutators involving exponentials. When two operators $hat(A)$ and $hat(B)$ have a commutator $[hat(A), hat(B)] = c$ that is simply a c-number (a complex number rather than an operator), we can establish that:
$
  [hat(A), e^(hat(B))] = [hat(A), hat(B)] e^(hat(B))
$
This follows from expanding the exponential as $e^(hat(B)) = sum_(n=0)^infinity hat(B)^n \/ n!$ and using the property $[hat(A), hat(B)^n] = n[hat(A), hat(B)]hat(B)^(n-1)$, which holds when the commutator is a c-number.

Now we apply this identity to our specific case. Taking $hat(A) = hat(a)_alpha$ and $hat(B) = sum_beta phi.alt_beta hat(a)_beta^dagger$, we first compute their commutator:
$
  [hat(a)_alpha, sum_beta phi.alt_beta hat(a)_beta^dagger] = sum_beta phi.alt_beta [hat(a)_alpha, hat(a)_beta^dagger] = sum_beta phi.alt_beta delta_(alpha beta) = phi.alt_alpha
$

$
  braket(phi.alt, phi.alt') = braket(0, exp(sum_alpha phi.alt_alpha^* hat(a)_alpha), phi.alt') = exp(sum_alpha phi.alt_alpha^* phi.alt_alpha) braket(0, phi.alt) = exp(phi.alt^* dot phi.alt)
$

$
  hat(alpha)^dagger ket(phi.alt) &= hat(alpha)^dagger exp(sum_alpha phi.alt_alpha hat(a)_alpha^dagger) ket(0) = pdv(, phi.alt_alpha) exp(sum_alpha phi.alt_alpha hat(a)_alpha^dagger) ket(0) = pdv(, phi.alt_alpha) ket(phi.alt)
$

$
  [hat(a)_alpha^dagger, ketbra(phi.alt, phi.alt)] = (pdv(, phi.alt_alpha) - phi.alt_alpha^*) ketbra(phi.alt, phi.alt)
$

The standard Gaussian measure on the complex plane:

$
  d^2 phi.alt = d (Re phi.alt) (Im phi.alt) => integral e^(- abs(phi.alt)^2) d^2 phi.alt = pi
$

Sometimes, we prefer to use $d phi.alt d phi.alt^* = 2 i d^2 phi.alt$:

$
  d mu(phi.alt) = product_alpha (dd(phi.alt_alpha, phi.alt^*_alpha))/(2pi i) exp(- sum_alpha abs(phi.alt_alpha)^2)
$

$
  integral d mu (phi.alt) [a^dagger_alpha, ketbra(phi.alt, phi.alt)] = integral d mu (phi.alt) (pdv(, phi.alt_alpha) - phi.alt_alpha^*) ketbra(phi.alt, phi.alt)
$

Use integral by parts:

$
  pdv(, phi.alt_alpha) exp(- sum_(alpha) abs(phi.alt_alpha)^2) = - phi.alt^*_alpha exp(- sum_(alpha) abs(phi.alt_alpha)^2)
$

So everything cancelled. Since the measure commutes with every $a_alpha, a_alpha^dagger$. By full Fock space irreducibility, Schur's lemma tells us that the measure must be proportional to the identity $O = c bold(1)$.

$
  & hat(a)_alpha ket(phi.alt) = phi.alt_alpha ket(phi.alt) = pdv(, phi.alt^*) ket(phi.alt) \
  & bra(phi.alt) hat(a)_alpha^dagger = bra(phi.alt) phi.alt_alpha^*
$

$
  ket(psi) = integral d mu(phi.alt) psi(phi.alt^*) ket(phi.alt)
$

$
  hat(a)_alpha -> pdv(, phi.alt^*), quad hat(a)^dagger_alpha -> phi.alt^*_alpha
$

It's clear that the unitary transformation:

$
  braket(phi.alt', psi) = integral d mu(phi.alt) braket(phi.alt', phi.alt) braket(phi.alt, psi) = integral d mu(phi.alt) exp(phi.alt' dot phi.alt) psi(phi.alt)
$

$
  braket(phi.alt', hat(A)(hat(a)^dagger,hat(a)), phi.alt) = A(phi.alt^*,phi.alt) braket(phi.alt', phi.alt) = A(phi.alt^*,phi.alt) e^(phi.alt' dot phi.alt)
$

== Grassmann variables

Let $xi,xi^*$ be independent Grassmann variables.
$
  [xi,xi^*]_+ = 0, quad xi^2 = 0, quad (xi^*)^2 = 0
$

$
  e^(xi) = sum_(i>=0) 1/i! xi^i = 1 + xi => f(xi) = f_0 + f_1 xi
$

Because the translation invariance, the total integral at boundary is zero:

$
   integral d xi f(xi + eta) & = integral d xi f(xi) \
  a I_1 + b I_xi + b eta I_1 & = a I_1 + b I_xi => I_1 = 0
$

$
  I_xi = B => "choose" B = 1
$

$
  pdv(, xi) (xi^* xi) = pdv(, xi) (-xi xi^*) = - xi^*
$

$
  integral d xi^* d xi e^(- xi^* xi) f^*(xi) g(xi^*) &= integral d xi^* d xi (1 - xi^* xi) (f^*_0 + f^*_1 xi) (g_0 + g_1 xi^*) \
  &= f_0^* g_0 + f_1^* g_1
$

It's worth noting:

$
  xi_alpha ket(0) = xi_alpha (1-xi_alpha) ket(0) = xi_alpha (1-xi_alpha hat(a)^dagger_alpha) ket(0)
$

$
  ket(xi) = exp(- sum_alpha xi_alpha hat(a)^dagger_alpha) ket(0) = product_alpha (1-xi_alpha hat(a)^dagger_alpha) ket(0)
$

$
  hat(a)_alpha ket(xi) ~ hat(a)_alpha - hat(a)_alpha xi_alpha hat(a)^dagger_alpha ket(0) = xi_alpha ket(0) = xi_alpha (1-xi_alpha hat(a)^dagger_alpha) ket(0) => hat(a)_alpha ket(xi) = xi_alpha ket(xi)
$


= Finite-temperature field theory

== Thermal evolution

For general bracket:

$
  [hat(a)_alpha,hat(a)^dagger_beta]_minus.plus = delta_(alpha beta)
$

$
  hat(rho) = exp(-beta (hat(H) - mu hat(N))) \/ Z
$

$
  expval(hat(O)(t)) = tr [hat(rho) thin hat(O)(t)] & = tr [hat(rho) e^(-i hat(H) t) hat(O) e^(i hat(H) t)] \
                                                   & = tr [e^(i hat(H) t) hat(rho) e^(-i hat(H) t) hat(O)] \
                                                   & = tr [hat(rho) hat(O)] = expval(hat(O)(0))
$

For $hat(H)$ independent of time. The last step is due to $hat(rho)$ commutes with $e^(i hat(H) t)$.

$
  G^((n))(alpha_i t_i, alpha'_i t'_i) = (-i)^n expval(hat(T)[product^n_(i = 1) a^((H))_alpha_i (t_i) product^1_(i=n) a^(dagger (H))_alpha'_i (t'_i)])
$

- $a_alpha^((H))(t)$ is annihilation operator in Heisenberg picture.
- $expval(dots)$ is ensemble or ground state average.
- $hat(T)(dots)$ is time ordering operator: $hat(T) [product_i hat(O) (t_i)] = product_i hat(O) (t_(rho(i)))$ where $rho(i)$ is any possible time permutation that make it ascending or descending based on the context and goal.

$
  G(alpha t;alpha' t) = -i expval(hat(T)[hat(a)_alpha_1 (t) hat(a)^dagger_alpha'_1 (t')])
$

$
  hat(a)^((H))_alpha (t) = e^(i H t) hat(a)_alpha e^(-i H t)
$

$
  expval(hat(a)^((H))_alpha (t) hat(a)_alpha^(dagger (H)) (t')) &= sum_n rho_n braket(n, hat(a)_alpha^((H))(t) hat(a)_alpha^(dagger (H)) (t'), n) \
  &= sum_n rho_n braket(n, e^(i H t) hat(a)_alpha e^(-i H(t-t')) hat(a)^dagger_alpha e^(-i H t), n) \
$

Suppose: $ket(psi_n (t)) = e^(- i H t) ket(n)$:

$
  "LHS" = sum_n rho_n braket(psi_n (t), hat(a)_alpha e^(-i H(t-t')) hat(a)^dagger_alpha, psi_n (t'))
$

Assuming simple Hamiltonian: $hat(K)_0 = sum_alpha (epsilon_alpha - mu) hat(a)^dagger_alpha hat(a)_alpha$

$
  [hat(a)_alpha, hat(a)^dagger_beta hat(a)_beta] = delta_(alpha beta) hat(a)_beta => [hat(a)_alpha, hat(K)_0] = (epsilon_alpha - mu_0) hat(a)_alpha
$

For Heisenberg picture:

$
  i planck pdv(, t) hat(a)_alpha (t) = [hat(a)_alpha (t), hat(K)_0] = (epsilon_alpha - mu) hat(a)_alpha (t) => hat(a)_alpha (t) = e^(-i (epsilon_alpha - mu)(t-t_0) \/planck) hat(a)_alpha (t_0)
$

$
  i planck pdv(, t) G_0 (alpha t; alpha' t') = - i i planck pdv(, t) [theta(t-t') expval(hat(a)_alpha (t) hat(a)^dagger_alpha (t')) + eta theta(t'-t) expval(hat(a)^dagger_alpha (t) hat(a)_alpha (t))]
$

For $t = t'$: $pdv(, t) theta(t-t') = delta(t-t')$, for $t!=t'$, focus on operator $i planck pdv(, t) hat(a)_alpha (t) = (epsilon_alpha - mu) hat(a)_alpha (t)$:

$
  "LHS" &= - i delta(t-t') expval([hat(a)_alpha (t) hat(a)^dagger_alpha (t') ]) + (epsilon_alpha - mu) G_0 (alpha t;alpha' t') \
  &= planck delta_(alpha alpha') delta(t-t') + (epsilon_alpha - mu) G_0 (alpha t; alpha' t')
$

For fixed $alpha', t'$, we treat it as a first-order linear differential equation on $t$. If we fix the diagonal property in $alpha,alpha'$ due to $delta_(alpha,alpha')$:

$
  i planck pdv(, t) G_alpha (t,t') & = planck delta(t-t') + (epsilon_alpha - mu) G_alpha (t,t') \
                    G_alpha (t,t') & = C exp(- i (epsilon_alpha - mu) (t-t') \/ planck)
$

Where discontinuity condition:

$
  i planck (G_alpha (t-t' = 0^+) - G_alpha (t-t'=0^-)) = planck => G_alpha (0^+) - G_alpha (0^-) = - i
$

$
  G_alpha (tau = t - t') = A_(plus.minus) exp(- i (epsilon_alpha - mu) (t-t') \/ planck)
$

For $tau > 0$ or $tau < 0$.

$
  lim_(t -> t^+) G_0 (alpha t;alpha' t') = - i expval(hat(a)_alpha (t') hat(a)^dagger_alpha' (t'))
$

Due to $hat(K)_0 prop hat(a)^dagger_alpha hat(a)_alpha$ is diagonal, therefore each $alpha,alpha'$ belongs to different modes that:

$
  expval(hat(a)_alpha hat(a)^dagger_alpha') = expval(hat(a)_alpha) expval(hat(a)^dagger_alpha') = 0 quad alpha != alpha'
$

$
  "LHS" = - i expval(hat(a)_alpha (t') hat(a)^dagger_alpha (t')) = 1 + eta n_alpha, quad n_alpha = expval(hat(a)^dagger_alpha hat(a)_alpha)
$

Generally:

$
  lim_(t -> t^+) G_0(alpha t;alpha' t') = - i delta_(alpha alpha') (1 + eta n_alpha), quad lim_(t -> t^-) G_0(alpha t;alpha' t') = - i delta_(alpha alpha') eta n_alpha
$

$
  G_alpha (0^+) = A_+ = -i (1 + eta n_alpha), quad G_alpha (0^-) = A_- = -i eta n_alpha
$

$
  G_0 (alpha t; alpha' t') = - i delta_(alpha alpha') exp(-i (epsilon_alpha - mu) (t - t')) [theta(t - t') (1 + eta n_alpha) + theta(t' - t) eta n_alpha]
$

$
  tilde(G)_0 (alpha;alpha') (omega) &= integral_(-infinity)^infinity d t thin G_0 (alpha t;alpha' t') e^(-i omega (t-t')) \
$

Evaluate in separation:

$
  tilde(G)_0 (omega) = - i [(1+eta n_alpha) integral_0^infinity d tau e^(i omega tau) e^(-i (epsilon_alpha - mu) tau) + eta n_alpha integral^0_(-infinity) d tau e^(i omega tau) e^(-i (epsilon_alpha - mu) tau)]
$

Here we translate $d t -> d (t - t') = d tau$ where $t - t' > 0$ or $t - t' < 0$ for each part.

$
  tilde(G)_0 (omega) &= - i [(1+eta n_alpha) i/(omega - omega_alpha + i 0^+) + eta n_alpha (-i)/(omega - omega_alpha - i 0^+)] \
  &= (1 + eta n_alpha)/(omega - omega_alpha + i 0^+) - (eta n_alpha)/(omega - omega_alpha - i 0^-)
$

$
  tilde(G)_0 (alpha;alpha') (omega) = delta_(alpha alpha') e^(i omega 0^+) [(1 + eta n_alpha)/(omega - (epsilon_alpha - mu) + i 0^+) - (eta n_alpha)/(omega - (epsilon_alpha - mu) - i 0^-)]
$

We can define the dual of time and temperature: $t <-> - i tau$, $tau in [0,planck beta) = [0,planck \/ k T)$

$
  G^((n))(alpha_i tau_i, alpha'_i tau'_i) = - expval(hat(T)[product^n_(i = 1) hat(a)^((H))_alpha_i (tau_i) product^1_(i=n) hat(a)^(dagger (H))_alpha'_i (tau'_i)])
$

$
  hat(a)_alpha^((H))(tau) = e^(hat(H) tau) hat(a)_alpha e^(-hat(H) tau)
$

To elucidate the periodicity, we omit any unnecessary symbol:

$
  G(tau) = - expval(hat(T) [hat(a)(tau) hat(a)^dagger (0)])
$

$
  G(tau) = cases(- expval(hat(a)(tau) hat(a)^dagger (0)) quad tau > 0, - eta expval(hat(a)^dagger (0) hat(a)(tau)) quad tau < 0)
$

$
  G(beta^-) &= - expval(hat(a)(beta) hat(a)^dagger (0)) = - tr[e^(-beta hat(H)) e^(beta H) hat(a) e^(- beta H) hat(a)^dagger] \
  &= - tr[hat(a) e^(- beta hat(H)) hat(a)^dagger] = - tr [e^(-beta hat(H)) hat(a)^dagger hat(a)] \
  &= eta thin G(0^-)
$

The $n$-point Green's functions is same as below to take $[product_i A_i]$ as $[A_j X]$ by cyclic property of trace.

Assume the system is time-translation invariant, so the Green's function depends only on the difference $tau - tau'$.

$
  G(tau) := G(alpha,alpha';tau) := G(alpha tau; alpha' 0)
$

Where $alpha,alpha'$ could be omitted in cases we don't pay attention.

$
  G(tau + planck beta) = eta thin G(tau)
$

Suggests the discrete Fourier transformation, or Fourier series.

$
  G(tau) = 1/(planck beta) sum_(-infinity)^infinity e^(- i omega_n tau) G(omega_n)
$
$
  e^(-i omega_n (tau + planck beta)) &equiv eta thin e^(-i omega_n tau) \
  e^(-i omega_n planck beta) &= eta 1 \
  omega_n &= cases((2n pi)/(planck beta) quad &eta = 1, ((2n+1)pi)/(planck beta) quad &eta = -1)
$

$
  integral_0^(planck beta) d tau thin e^(i (omega_n - omega_m) tau) := planck beta delta_(n m)
$

$
  G(omega_n) = integral_0^(planck beta) d tau thin e^(i omega_n tau) G(tau)
$

Restoring original notation:

$
  G(alpha tau; alpha' tau') = 1/(planck beta) sum_n e^(-i omega_n (tau - tau')) G(alpha;alpha') (omega_n)
$

$
  G(alpha;alpha') (omega_n) = integral_0^(planck beta) d tau thin e^(i omega_n (tau - tau')) G(alpha tau;alpha tau')
$

For non-interacting system, the answer is simple that change all $(t-t') <-> -i (tau - tau')$:

$
  G_0 (alpha tau, alpha' tau') = - delta_(alpha alpha') exp(-(epsilon_alpha - mu)(tau - tau') \/ planck) [theta(tau-tau')(1+ eta n_alpha) + eta theta(tau'-tau)n_alpha]
$

Suppose $tau - tau' <-> tau$:

$
                                       G_0 (0^-) & = G_0 (beta^-) \
                                     eta n_alpha & = eta e^(-beta(epsilon_alpha - mu)) (1 + eta n_alpha) \
  n_alpha (eta - e^(-beta (epsilon_alpha - mu))) & = eta e^(-beta(epsilon_alpha - mu)) \
                                         n_alpha & = 1/(e^(beta (epsilon_alpha - mu)) - eta)
$

$
  G_0 (alpha,alpha')(omega_n) = delta_(alpha alpha') e^(i omega 0^+) (1/(i omega_n - (epsilon_alpha - mu)\/planck))
$

== Continuum field operators

Kinetic energy:

$
  hat(T) = integral dd(r, 3) thin hat(psi)^dagger (bold(r)) (- planck^2/(2m) nabla^2_(bold(r))) hat(psi) (bold(r)) \
$

Where $hat(psi)(bold(r))$ is the field operator satisfying the equal time relation:

$
  [hat(psi)(bold(r)),hat(psi)^dagger (bold(r)')]_(minus.plus) = delta(bold(r) - bold(r)')
$

The thermal expectation value is:

$
  expval(hat(T)) &= integral dd(r, 3) expval(hat(psi)^dagger (bold(r))(-planck^2/(2m)) nabla^2_(bold(r)) hat(psi)(bold(r))) \
  &= integral dd(r, 3) lr(expval(hat(psi)^dagger (bold(r'))(-planck^2/(2m)) nabla^2_(bold(r)) hat(psi)(bold(r)))bar)_(bold(r)' = bold(r)) \
  &= integral dd(r, 3) (-planck^2/(2m)) nabla^2_(bold(r)) lr(expval(hat(psi)^dagger (bold(r')) hat(psi)(bold(r)))bar)_(bold(r)' = bold(r))
$

Immediately, we inspect:#footnote[The $T$ is time operator now:]

$
  G(bold(r) t;bold(r') t') = - i expval(hat(T)[hat(psi)^((H))(bold(r),t) hat(psi)^(dagger (H)) (bold(r)', t')]) \
  i eta thin G(bold(r) t;bold(r') t^+) = expval(hat(psi)^((H))(bold(r),t) hat(psi)^(dagger (H)) (bold(r)', t^+))
$

So:

$
  expval(hat(T)) = integral dd(r, 3) (- planck^2/(2m)) nabla^2_(bold(r)) [i eta thin lr(G(bold(r)t;bold(r') t^+)] bar)_(bold(r') = bold(r))
$

Assume the system is translation invariant in space and time, so one can take: $bold(R) = bold(r) - bold(r')$, $tau = t - t'$

$
  G(bold(R),tau) := G(bold(r) t; bold(r') t')
$

$
  tilde(G)(bold(k),omega) = integral dd(R, 3) dd(tau) e^(- i bold(k) dot bold(R) + i omega tau) G(bold(R), tau)
$

$
  nabla^2_(bold(R)) G(0,0^-) &= integral (dd(k, 3) dd(omega))/((2pi)^4) (i bold(k))^2 e^(-i omega 0^-) lr(tilde(G)(bold(k),omega)bar)_(bold(R) = 0) = - integral (dd(k, 3) dd(omega))/((2pi)^4) k^2 e^(i omega 0^+) tilde(G)(bold(k),omega)
$

$
  expval(hat(T)) &= i eta cal(V) (- (planck^2)/(2m)) (-integral (dd(k, 3) dd(omega))/((2pi)^4) k^2 e^(i omega 0^+) tilde(G)(bold(k),omega)) \
  &= i eta cal(V) integral (dd(k, 3) dd(omega))/((2pi)^4) e^(i omega 0^+) (planck k)^2/(2 m) tilde(G)(bold(k),omega)
$

Interaction energy:

It's simpler to deduce from:

$
  hat(psi)^dagger (bold(r),t) i planck pdv(, t) hat(psi)(bold(r),t) = &hat(psi)^dagger (bold(r),t) [hat(psi)(bold(r),t),hat(T) + hat(V)] \
  hat(psi)^dagger (bold(r),t) i planck pdv(hat(psi)(bold(r),t), t) = &hat(psi)^dagger (bold(r),t) (-planck^2/(2m) nabla^2 - mu) hat(psi)(bold(r),t) \ &+ integral dd(r, 3) hat(psi)^dagger (bold(r),t) hat(psi)^dagger (bold(r'),t) v(bold(r) - bold(r)') hat(psi) (bold(r'),t) hat(psi) (bold(r),t)
$

$
  expval(hat(V)) &= (i eta)/2 integral dd(r, 3) lr([(i planck pdv(, t) + planck^2/(2m) nabla^2_(bold(r)) + mu) G(bold(r) t;bold(r)' t')]bar)_(bold(r) = bold(r'), t' = t^+) \
  &= (i eta)/2 cal(V) integral (dd(k, 3) dd(omega))/((2pi)^4) e^(i omega 0^+) (planck omega - (planck k)^2/(2 m) + mu) tilde(G)(bold(k),omega)
$

== Linear response

Linear Responses:

$
  delta hat(H) = - e integral dd(bold(r)) hat(rho) (bold(r)) phi.alt(bold(r))
$

Where $phi.alt(bold(r))$ is external electric potential and $hat(rho) (bold(r)) = hat(psi)^dagger (bold(r)) hat(psi) (bold(r))$ is the density operator.

$
  hat(j) (bold(r)) = (i e planck)/(2 m) [hat(psi)^dagger (bold(r)) (nabla hat(psi)(bold(r))) - (nabla hat(psi)^dagger (bold(r))) hat(psi) (bold(r))]
$

We only approximate in linear order, a merit is the total response is the summation of all field responses.

Consider a time-dependent infinitesimally small external field:

$
  hat(H)_phi.alt (t) = hat(H) + hat(O) phi.alt (t)
$

Where $phi.alt$ is the external field and $hat(O)$ is the observable.

$
  i planck pdv(, t) hat(U) (t,t_i) & = hat(H)_phi.alt (t) hat(U)(t,t_i) \
                    hat(U) (t,t_i) & = hat(T) [exp(-i/planck integral_(t_i)^t hat(H)_phi.alt (t) dd(t))]
$

$
  i planck pdv(, t) hat(U) (t,t_i) &= (hat(H) + hat(O) phi.alt(t)) hat(U)(t,t_i), quad hat(U)(t_i,t_i) = bold(1) \
  i planck pdv(, t) delta hat(U) (t,t_i) &= hat(H) delta hat(U)(t,t_i) + hat(O) phi.alt(t) U_0 (t,t_i) + O(delta^2 U) \
  hat(U)_0 (t_i, t) i planck pdv(, t) delta hat(U) (t,t_i) + i planck pdv(, t) (U_0 (t_i,t)) delta hat(U) (t,t_i) &= U_0 (t_i,t) hat(O) phi.alt(t) U_0 (t,t_i) + O(delta^2 U) \
  i planck pdv(, t) (U_0 (t_i,t) delta hat(U)(t,t_i)) &= U_0 (t_i,t) hat(O) phi.alt(t) U_0 (t,t_i) + O(delta^2 U) \
  delta hat(U) (t,t_i) &= - i/planck hat(U)_0 (t,t_i) integral_(t_i)^t dd(t_1) hat(U)_0 (t_i,t_1) hat(O) phi.alt(t_1) hat(U)_0 (t_1,t_i) \
  delta hat(U) (t,t_i) &= - i/planck integral_(t_i)^t dd(t_1) hat(U)_0 (t,t_1) hat(O) phi.alt(t_1) hat(U)_0 (t_1,t_i) \
$

Suppose $hat(U) approx hat(U)_0 + delta hat(U)$
where $hat(U)_0$ is unperturbed evolution operator without $hat(O) phi.alt(t)$, and *ignores* the second order.

$
  delta ket(psi(t)) &= delta hat(U)(t,t_i) ket(psi(t_i)) = integral_(t_i)^t dd(t_1) dv(hat(U)(t,t_i), phi.alt(t_1), d: delta) phi.alt(t_1) ket(psi(t_i)) \
$

$
  lr(dv(hat(U)(t,t_i), phi.alt(t_1), d: delta)bar)_(phi.alt -> 0) &= - i/planck hat(U)_0 (t,t_1) hat(O) hat(U)_0 (t_1,t_i), quad t_i < t_1 < t \
  &= -i/planck e^(-i hat(H) (t-t_i) \/ planck) (e^(i hat(H) (t_1 - t_i) \/ planck) hat(O) e^(-i hat(H) (t_1 - t_i) \/ planck)) \
  &= -i/planck e^(-i hat(H) (t - t_i)) hat(O)^((H)) (t_1) \
  &= -i/planck U_0 (t,t_i) hat(O)^((H)) (t_1)
$

$
  "LHS" = - i/planck integral_(t_i)^t dd(t_1)U_0 (t,t_i) hat(O)^((H)) (t_1) phi.alt(t_1) ket(psi(t_i))
$

The expectation value of an observable $hat(R)$ other than $hat(O)$:

$
  delta hat(R)(t) &= delta sum_n rho_n braket(psi_n (t), hat(R), psi_(n) (t)) \
  &= sum_n rho_n (braket(delta psi_n (t), hat(R), psi_(n) (t)) + braket(psi_n (t), hat(R), delta psi_(n) (t))) \
$

Evaluate the first term:

$
  braket(delta psi_n (t), hat(R), psi_(n) (t)) &= i/planck integral_(t_i)^t dd(t_1) phi.alt(t_1) braket(psi_n (t_i), hat(O)^((H)) (t_1)U_0 (t_i,t) hat(R), psi_n (t)) \
  &= i/planck integral_(t_i)^t dd(t_1) phi.alt(t_1) braket(psi_n (t_i), hat(O)^((H))(t_1) U_0 (t_i,t) hat(R) U_0(t,t_i), psi_n (t_i)) \
  &= i/planck integral_(t_i)^t dd(t_1) phi.alt(t_1) braket(psi_n (t_i), hat(O)^((H))(t_1) hat(R)^((H)) (t), psi_n (t_i))
$

Therefore, suppose $t_i -> -infinity$ where we can compute the evolution by initial distribution:

$
  "LHS" = -i/planck integral_(-infinity)^(infinity) dd(t_1) theta(t-t_1) expval([hat(R)^((H))(t),hat(O)^((H))(t_1)]) phi.alt(t_1)
$

$
  D^r (hat(R);hat(O))(t;t') = dv(hat(R)(t), phi.alt(t')) = - i/planck theta(t-t') expval([hat(R)^((H))(t),hat(O)^((H))(t')])
$

Scattering experiments:

$
  i planck pdv(, t) ket(psi(t)) = (hat(H)_0 + hat(V)) ket(psi(t)) \
$

We define interaction picture state as:

$
  ket(psi_I (t)) := e^(i hat(H)_0 t \/ planck) ket(psi (t)) \
$

$
  i planck pdv(, t) ket(psi_I (t)) &= (-hat(H)_0 e^(i hat(H)_0 t \/ planck) + e^(i hat(H)_0 t \/ planck) (hat(H)_0 + hat(V))) ket(psi(t)) \
  i planck pdv(, t) ket(psi_I (t)) &= e^(i hat(H)_0 t \/ planck) hat(V) e^(- i hat(H)_0 t \/ planck) ket(psi_I (t)) \
  i planck pdv(, t) ket(psi_I (t)) &= hat(V)_I (t) ket(psi_I (t))
$

Start at $t = 0$ with $ket(psi(0)) = ket(psi_i)$. For a weak perturbation, we iterate to first order (Born approximation):

$
  ket(psi_I (t)) approx ket(psi_i) - i/planck integral_0^t dd(t') hat(V)_I (t') ket(psi_i)
$

The amplitude of finding the system in a different state $psi_f$ at time $t$ is:

$
  c^((1))_(f i) (t) &= braket(psi_f, psi_i (t)) = - i/planck integral_0^t dd(t') braket(psi_f, hat(V)_I (t'), psi_i) \
  &= - i/planck integral_0^t dd(t') braket(psi_f, e^(i hat(H)_0 t \/ planck) hat(V) e^(- i hat(H)_0 t \/ planck), psi_i) \
  &= - i/planck integral_0^t dd(t') e^(i (E_f - E_i) \/ planck) braket(psi_f, hat(V), psi_i)
$

We determine the transition matrix from probed system $ket(alpha)$ to $ket(beta)$ and wave vector from $bold(k)$ to $bold(k)+bold(q)$. Consider an external particle apply such effect on a many body system by scattering.

We prepare the initial state where:

- The many body system with eigenstate $ket(alpha)$ of $hat(H)_("sys")$.
- The external particle is in a plane wave state $ket(bold(k))$ with wave vector $bold(k)$.

The initial state is:

$
  ket(psi_i) = ket(bold(k)) times.o ket(alpha) equiv ket(bold(k) \, alpha)
$

The final state is:

$
  ket(psi_f) = ket(bold(k) + bold(q)) times.o ket(beta) equiv ket(bold(k) + bold(q) \, beta)
$

$
  hat(V) &= integral dd(r, 3) thin hat(psi)^dagger (bold(r))_("ext") hat(V)_("ext") hat(psi)_"ext" (bold(r)) = integral dd(r, 3) thin hat(psi)^dagger (bold(r))_("ext") v(r-r_i) hat(psi)_"ext" (bold(r)) \
$

$
  braket(psi_f, hat(V), psi_i) = bra(bold(k) + bold(q) \, beta) integral dd(r, 3) thin hat(psi)^dagger (bold(r))_("ext") v(r-r_i) hat(psi)_"ext" (bold(r)) ket(bold(k) \, alpha) \
$

Because:

$
  hat(psi)_"ext" (bold(r)) ket(bold(k)) = hat(psi)_"ext" (bold(r)) ket(bold(r)) braket(bold(r), bold(k)) 1/(V^(1/2)) e^(i bold(k) dot bold(r)) ket(0)_("ext")
$

$
  braket(psi_f, hat(V), psi_i) = T_(alpha beta) (bold(q)) = integral dd(r, 3) bra(beta) (e^(-i (bold(k) + bold(q)) dot bold(r)) sum_i v(bold(r) - bold(r)_i) e^(i bold(k) dot bold(r))) ket(alpha)
$

$
  integral dd(r, 3) e^(-i bold(q) dot bold(r)) v(bold(r) - bold(r)_i) = e^(-i bold(q) dot bold(r)_i) integral dd(R, 3) thin v(bold(R)) = e^(-i bold(q) dot bold(r)_i) tilde(v)(bold(q))
$

$
  T_(alpha beta) (bold(q)) = tilde(v)(bold(q)) braket(beta, sum_i e^(-i bold(q) dot bold(r)_i), alpha) = tilde(v)(bold(q)) braket(beta, hat(rho)(bold(q)), alpha)
$

Where density matrix is $hat(rho)(bold(q)) = sum_i e^(-i bold(q) dot hat(bold(r))_i)$.

$
  c^((1))_(alpha beta) (t) &= - i/planck T_(alpha beta) (bold(q)) integral_0^t dd(t') e^(i omega_(alpha beta)), quad omega_(alpha beta) = -(E_alpha - E_beta)/planck \
  &= - 1/planck T_(alpha beta) (bold(q)) (e^(i omega_(alpha beta) t) - 1)/(omega_(alpha beta))
$

$
  P_(alpha beta) (bold(q), t) = abs(c^((1))_(alpha beta) (t))^2 = abs(T_(alpha beta) (bold(q)))^2/(planck^2) (4 sin^2 (omega_(alpha beta) t \/ 2))/(omega_(alpha beta)^2)
$

We are interested in transitions to any final state $beta$ of the many-body system, with the external particle's momentum transfer fixed to $bold(q)$. The total probability for scattering with momentum transfer $q$ and energy transfer $planck omega = E_beta - E_alpha$ is obtained by summing over all $beta$. In a macroscopic system, the final states form a continuum; we introduce the density of states $rho(E_beta)$ at energy $E_beta$. Then the total probability (for a given initial state $ket(alpha)$) is:

$
  P_alpha (bold(q),t) = integral dd(E_beta) rho(E_beta) P_(alpha beta) (bold(q),t)
$

For large $t$, the function becomes sharply peaked around $E_alpha = E_beta$:

$
  (4 sin^2 (omega_(alpha beta) t \/ 2))/(omega_(alpha beta)^2) approx 2pi planck t delta (E_beta - E_alpha)
$

$
  P_alpha (bold(q),t) approx sum_beta (2pi t)/(planck) lr(rho(E_alpha) abs(T_(alpha beta)(bold(q)))^2 bar)_(E_beta -> E_alpha)
$

$
  Gamma_alpha (bold(q)) = dv(P_alpha (bold(q),t), t) = sum_beta (2pi)/(planck) lr(rho(E_alpha) abs(T_(alpha beta)(bold(q)))^2 bar)_(E_beta -> E_alpha)
$

In practise, the $E_beta$ may differ $E_alpha$ by a energy transfer $planck omega$ we are interested in.

$
              f (E_beta - E_alpha) & = planck integral d omega f(planck omega) delta (E_beta - E_alpha - planck omega) \
  dv(, omega) f (E_beta - E_alpha) & = planck f(planck omega) delta (E_beta - E_alpha - planck omega)
$

$
  sigma_alpha(bold(q), omega) = dv(, omega) Gamma_alpha (bold(q)) (omega) = 2pi sum_beta rho(E_alpha) delta(E_beta - E_alpha - planck omega) abs(T_(alpha beta) (bold(q)))^2
$

$
  delta(E_beta - E_alpha - planck omega) = 1/(2pi planck) integral_(-infinity)^infinity dd(t) e^(i (E_beta - E_alpha - planck omega) t \/ planck)
$

$
  sum_beta e^(i (E_beta - E_alpha) t \/ planck) braket(alpha, hat(rho)^dagger (bold(q)), beta) braket(beta, hat(rho) (bold(q)), alpha) &= braket(alpha, e^(i hat(H) t \/ planck) hat(rho)^dagger (bold(q)) e^(- i hat(H) t \/ planck) hat(rho) (bold(q)), alpha) \
  &= braket(alpha, hat(rho)^dagger (bold(q)) (t) hat(rho), alpha)
$

$
  sigma_alpha (bold(q), omega) prop abs(tilde(v)(bold(q)))^2 rho(E_alpha) integral dd(t) braket(alpha, hat(rho)^dagger (bold(q)) (t) hat(rho), alpha)
$

== Real-time Green functions

$
  G(r t;r' t') = - i expval(hat(T)[hat(psi)(r,t) hat(psi)^dagger (r',t')])
$

We omit irrelevant indices, coordinates and focus on Green's function:

$
  G &= - i expval(hat(T) [psi psi^dagger]) = - i [theta(t-t') expval(psi psi^dagger) + eta theta(t'-t) expval(psi^dagger psi)] \
  &= theta(t-t') (-i expval(psi psi^dagger)) + theta(t'-t) (-i eta expval(psi^dagger psi)) \
  &= theta(t-t') G^> + theta(t'-t) G^<
$

Another way to decompose is by identity:

$
  theta(t-t') + theta(t'-t) = bold(1)
$

$
  G & = - i [theta(t-t') expval(psi psi^dagger) + eta theta(t'-t) expval(psi^dagger psi)] \
    & = -i [theta(t-t') expval(psi psi^dagger) + eta (1-theta(t-t')) expval(psi^dagger psi)] \
    & = -i [theta(t-t') expval([psi, psi^dagger]) + eta expval(psi^dagger psi)] \
    & = G^r + G^<
$

$
  G & = - i [theta(t-t') expval(psi psi^dagger) + eta theta(t'-t) expval(psi^dagger psi)] \
    & = - i [(1- theta(t'-t))expval(psi psi^dagger) + eta theta(t'-t) expval(psi^dagger psi)] \
    & = -i [expval(psi psi^dagger) - theta(t'-t) expval([psi,psi^dagger])] \
    & = G^> + G^a
$

$
  G^r + G^< = G^> + G^a => G^r - G^a = G^> - G^<
$

We assume $expval(O)^* = expval(O^dagger)$, which is true for thermal state or ground states with Hermitian Hamiltonian.

$
  [A,B]^dagger = [B^dagger,A^dagger] => [psi(bold(r), t),psi^dagger (bold(r'),t')]^dagger = [psi (bold(r'),t'),psi^dagger (bold(r),t)]
$

$
  (G^r)^* (r t;r' t') & = (-i theta(t-t') expval([psi, psi^dagger]))^* = i theta(t-t') expval([psi,psi^dagger]^dagger) \
                      & = i theta(t-t') expval([psi (bold(r'),t'),psi^dagger (bold(r),t)]) \
                      & =^(t <-> t') G^a (r' t';r t)
$

Reversely:

$
  (G^a)^* (r t;r' t') = G^r (r' t'; r t)
$

Assume translation invariance in space and time that $t -> t - t'$, $r -> r - r'$:

$
  G^r (bold(k),omega) = - i integral_(-infinity)^infinity dd(r, 3) integral_(-infinity)^infinity dd(t) e^(-i bold(k) dot bold(r) + i omega t) thin G^r (bold(r) t;bold(r)' t') \
$

Then, indeed:

$
  A(bold(k),omega) &= i (G^(r) (bold(k),omega) - G^a (bold(k),omega)) = i (G^(r) (bold(k),omega) - (G^r)^*(bold(k),omega)) \
  &= i dot 2 i Im G^(r) (bold(k),omega) = - 2 Im G^r (bold(k), omega) \
$

It's same that: $A(bold(k), omega) = i (G^> - G^<)$ too.

$
  integral_(-infinity)^infinity dd(omega)/(2pi) A(bold(k),omega) &= integral_(-infinity)^infinity dd(omega)/(2pi) integral^infinity_(-infinity) dd(t) thin e^(i omega t) (dots) \
  &= integral_(-infinity)^infinity delta(t) thin G(t,bold(k)) = G(0,bold(k)) \
$

Notice that when $t <-> t - t' = 0$, where the system at initial state has the canonical commutation relation, therefore:

$
  expval([psi,psi^dagger]) = 1 => G(0,bold(k)) = 1
$

Then the spectrum identity is obvious:

$
  integral_(-infinity)^infinity dd(omega)/(2pi) A(bold(k),omega) = 1
$

The spectrum in momentum space is more clear:

$
  A(bold(k),omega) = integral_(-infinity)^infinity dd(t) e^(i omega t) expval([hat(a)_k (t), hat(a)^dagger_k])
$

We can check by non-interacting system:

$
  hat(a)_k (t) = e^(-i (epsilon - mu) t) hat(a)_k => [hat(a)_k (t), hat(a)_k^dagger] = e^(-i (epsilon_k - mu) t) \
$

$
  A(bold(k),omega) = integral_(-infinity)^infinity dd(t) e^(i omega t) e^(i (epsilon-mu) t) = 2pi delta(omega - (epsilon_k - mu))
$

== Spectral representation

$
  G^< (bold(k),t) = - i eta sum_(m,n) e^(-beta K_n) abs(braket(m, hat(a)_k, n))^2 e^(i (K_m - K_n) t \/ planck) \
$

$
  G^< (bold(k), omega) = integral dd(t) e^(i omega t) G^< (bold(k), t) = - i eta sum_(n,m) e^(-beta K_n) 2pi delta(omega - (K_n - K_m) \/ planck) abs(braket(m, hat(a)_k, n))^2
$

Similarly:

$
  G^> (bold(k),t) = -i sum_(n,m) e^(-beta K_n) abs(braket(m, hat(a)_k, n))^2 e^(i (K_n - K_m) t \/ planck) \
$

To build the connection between $G^>$ and $G^<$, we relabel $n <-> m$ for consistency:

$
  G^> (bold(k),omega) = -i sum_(n,m) e^(- beta K_m) 2pi delta(omega - (K_n - K_m)\/planck) abs(braket(m, hat(a)_k, n))^2
$

$
  G^< (bold(k),omega) = eta e^(-beta (K_n - K_m)) G^> (bold(k),omega) = eta e^(- beta planck omega) G^> (bold(k),omega)
$

$
  G^> (bold(k),omega) = eta e^(beta planck omega) G^< (bold(k),omega)
$

$
  A(bold(k),omega) = i [G^> (bold(k),omega) - G^< (bold(k),omega)] = i (G^> (bold(k),omega) ( eta e^(beta planck omega) - 1) \
$

$
  G^< (bold(k),omega) = - i eta A/(e^(beta planck omega) - eta) => G^< = -i eta n_eta (omega) A (bold(k), omega)
$

$
  G^> (bold(k), omega) = -i eta e^(beta planck omega) dot n_eta (omega) A(bold(k), omega) = - i (1 + eta n_eta) A(bold(k), omega)
$

$
  & G^> (bold(k),t) = -i integral dd(omega_1) e^(-i omega_1 t) [1 + eta n_eta (omega_1)] A(bold(k),omega) \
  & G^< (bold(k),t) = -i eta integral dd(omega_1) e^(-i omega_1 t) n_eta (omega_1) A(bold(k),omega)
$

The expression by $A(bold(k),omega)$ can also be applied to $G^r$ and $G^a$:

$
  & G^r (bold(k),t) = theta (t) (G^> (bold(k),t) - G^< (bold(k),t)) \
  & G^a (bold(k), t) = - theta(-t) (G^> (bold(k),t) - G^< (bold(k),t))
$

Because:

$
  A(bold(k),omega) = i [G^> (bold(k),omega) - G^< (bold(k),omega)]
$

$
  G^r (bold(k),omega) &= integral dd(t) e^(i omega t) theta(t) (-i) integral dd(omega_1)/(2pi) e^(-i omega_1 t) A = -i integral dd(omega_1)/(2pi) A(bold(k),omega_1) integral_0^infinity e^(i (omega-omega_1) t) \
  &= -i dot i integral dd(omega_1)/(2pi) A(bold(k), omega_1)/(omega - omega_1 + i 0^+) = integral dd(omega_1)/(2pi) A(bold(k), omega_1)/(omega - omega_1 + i 0^+)
$

$
  G^a (bold(k),omega) = -(-i) integral dd(omega_1)/(2pi) A(bold(k), omega_1) integral^0_(-infinity) dd(t) e^(i (omega - omega_1) t) = integral dd(omega_1)/(2pi) (A(bold(k),omega_1))/(omega - omega_1 - i 0^+)
$

$
  G (bold(k),t) &= theta(t) G^> (bold(k),t) + theta(-t) G^< (bold(k),t) = integral dd(t) e^(i omega t) [theta(t) G^> (bold(k),omega) + theta(-t) G^< (bold(k),omega)] \
  &= integral dd(omega_1)/(2pi) A [(1+eta n_eta (omega))/(omega-omega_1 + i 0^+) - (eta n_eta (omega))/(omega - omega_1 - i 0^+)]
$

A useful identity can be applied to separate real and imaginary part:

$
  1/(x plus.minus i 0^+) = cal(P)(1/x) minus.plus i pi delta(x)
$

$
  G^r (bold(k),omega) = integral dd(omega_1)/(2pi) A[cal(P)(1/(omega-omega_1) - i pi delta(omega-omega_1))] = cal(P)(integral dd(omega_1)/(2pi) (A (bold(k),omega))/(omega-omega_1)) - i/2 A(bold(k),omega) \
$

$
  Re G^r = cal(P)(integral dd(omega_1)/(2pi) (A (bold(k),omega))/(omega-omega_1)), quad Im G^r = -1/2 A
$

$
  Re G^a = Re G^r = cal(P)(integral dd(omega_1)/(2pi) (A (bold(k),omega))/(omega-omega_1)), quad Im G^a = 1/2 A
$

$
  G &= integral dd(omega_1)/(2pi) A{1+eta n_eta [cal(P)(1/(omega - omega_1)) - i pi delta(omega-omega_1)] + ...} \
  &= cal(P)(integral dd(omega_1)/(2pi) (A (bold(k),omega))/(omega-omega_1)) - i pi integral dd(omega_1)/(2pi) A thin delta(omega-omega_1) (1 + eta n_eta + eta n_eta) \
$

$
  Im G = -1/2 (1+2 eta n_eta (omega)) A(bold(k),omega)
$

Interestingly, the particle density distribution can be further reduced:

$
  1 + 2 eta n_eta (omega) = 1 + (2 eta)/(e^(beta planck omega) - eta) = (e^(beta planck omega) + eta)/(e^(beta planck omega) - eta) = (e^(beta planck omega \/2) + eta e^(-beta planck omega \/ 2))/(e^(beta planck omega \/2) - eta e^(-beta planck omega \/ 2)) = (tanh ((beta planck omega)/2))^(-eta)
$

$
  Im G = -1/2 tanh^(-eta) ((beta planck omega)/2) A(bold(k),omega)
$

Generally, one can use analytic continuation to acquire all Green's functions:

$
  & G(bold(k),z) = integral_(-infinity)^infinity dd(omega)/(2pi) (A(bold(k),omega))/(z - omega) \
$

$
  G^r (bold(k), omega) = lim_(epsilon -> 0^+) G(k,omega - i eta) = integral_(-infinity)^infinity dd(omega_1)/(2pi) (A(bold(k),omega))/(omega - omega_1 - i epsilon)
$

Indeed:

$
  G^a (bold(k),omega) = lim_(epsilon -> 0^+) G(k,omega - i epsilon)
$

$
  G(bold(k), tau = omega_n) = integral_(-infinity)^infinity dd(omega_1)/(2pi) (A(bold(k),omega_1))/(i omega_n - omega_1)
$

== Nonequilibrium evolution

$
  hat(U) (t,t') = hat(T) exp(-i/planck integral_(t')^t hat(H) (tau) dd(tau)) \
$

With convention $hat(U) (t,t') = hat(U)^dagger (t',t)$.

$
  G^> (r t;r' t') &= -i expval(hat(psi)^((H))(r,t) hat(psi)^(dagger (H)) (r',t')) \
  &= -i tr[e^(-beta hat(H)(t_i)) hat(U)(t_i,t) hat(psi)(r) hat(U)(t,t') hat(psi)^dagger (r') hat(U)(t',t_i)] \
$

Where $t_i$ is the initial time. Now we rewrite the thermal factor as a evolution along the imaginary axis:

$
  e^(-beta hat(H)(t_i)) = hat(U)(t_i - i planck beta, t_i)
$

$
  G^> (r t;r' t') &= -i tr[hat(U)(t_i - i planck beta, t_i) hat(U)(t_i,t) hat(psi)(r) hat(U)(t,t') hat(psi)^dagger (r') hat(U)(t',t_i)] \
$

We can formalize the specific contour that from $t_i^+ -> t'^+ -> t^- -> t_i^- -> t_i^- - i planck beta$ that from above real axis to below real axis and down to imaginary axis, we assign the above, below and down to imaginary one each as $C^+, C^-, C^beta$.

= Path integrals

== Time slicing

$
  hat(U) (t_f,t_i) = e^(-i/planck hat(H) (t_f - t_i))
$

$
  e^(hat(A) + hat(B)) = lim_(M->infinity) (e^(hat(A)\/M) e^(hat(B)\/M))^M
$

$
  e^(- i/planck hat(H) (t_f - t_i)) = lim_(M->infinity) (e^(-i/planck hat(T) epsilon) e^(-i/planck hat(V) epsilon))^M
$

Where $epsilon = (t_f - t_i) \/ M$.

$
  U (x_f,t_f;x_i,t_i) = lim_(M->infinity) braket(x_f, (e^(-i/planck hat(T) epsilon) e^(-i/planck hat(V) epsilon))^M, x_i)
$

$
  U = lim_(M->infinity) integral product_(k=1)^(M-1) dd(x_k) braket(x_f, e^(-i/planck hat(T) epsilon) e^(-i/planck hat(V) epsilon), x_(M-1)) dots.c
$

$
  braket(x_n, e^(-i/planck hat(T) epsilon) e^(-i/planck hat(V) epsilon), x_(n-1)) = integral dd(p_n)/(2pi planck) e^(i/planck p_n (x_n - x_(n-1))) e^(-i/planck p_n^2/(2m) epsilon) e^(-i/planck V(x_(n-1)) epsilon)
$

$
  U = lim_(M->infinity) integral & product_(k=1)^(M-1) dd(x_k) product_(k=1)^M dd(p_k)/(2pi planck) \
                                 & exp(i/planck sum_(k=1)^M (p_k (x_k - x_(k-1))) - epsilon H(p_k,x_(k-1)))
$

$
  x_k, thin k in bb(N) => x(k), thin k in bb(N) =>^(k -> infinity) x(t), thin t in bb(R)
$

$
  d mu (x) = product_(k=1)^(M-1) dd(x_k) =>^(M->infinity) dd(x(t), d: upright(D))
$

$
  U(x_f, t_f; x_i,t_i) = integral^(x(t_f) = x_f)_(x(t_i) = t_i) dd(x(t), d: upright(D)) integral_(-infinity)^infinity dd(p(t), d: upright(D)) exp(i/planck dd(t) L(p,x) (t))
$

$
  L(x,dot(x)) (t) = p(t) dot(x)(t) - H(p(t),x(t))
$

$
  S[x(t)] = integral_(x_i)^(x_f) L(x,dot(x)) (t)
$

If the kinematic energy is the simple form $p^2 \/ 2m$, we can integrate it and therefore:

$
  dd(x(t), d: upright(D)) = lim_(M -> infinity) (m/(2pi i planck epsilon))^(M/2) product^(M-1)_(k=1) (dd(x_k))/(sqrt("scale"))
$

For $t_1 > t_2$, we start with Heisenberg picture operators:

$
  hat(O)^((H)) (t) = e^(i/planck hat(H) (t - t_i)) hat(O) e^(-i/planck hat(H) (t - t_i))
$

The time ordered product is:

$
  hat(T) (hat(O)^((H)) (t_1) hat(O)^((H)) (t_2)) = hat(O)^((H)) (t_1) hat(O)^((H)) (t_2) quad t_1 > t_2
$

$
  braket(x_f, T [hat(O)^((H)) (t_1) , hat(O)^((H)) (t_2)], x_i) = integral dd(x(t), d: upright(D)) O(x(t_1)) O(x(t_2)) e^(i/planck S[x(t)])
$

$
  Z = tr e^(- beta hat(H)) = integral_(x (tau_i) = x_0)^(x (tau_f) = x_0) braket(x, e^(-beta hat(H)), x)
$

Using the same time-slicing idea, with $epsilon = planck beta \/ M$, $tau_f - tau_i = planck beta$.

$
  U(x_f,tau_f;x_i, tau_i) = braket(x_f, e^(-1/planck (tau_f - tau_i) hat(H)), x_i), quad tau = i t
$

Replace with $t = -i tau$:

$
  Z = integral_(x(planck beta) = x(0)) dd(x(tau), d: upright(D)) exp(- 1/planck S_E [x(tau)])
$

$
  S_E [x(tau)] & = i evaluated(S (x (-i tau)))_(x(planck beta) = x(0)) \
               & = i/planck integral_(x(planck beta) = x(0)) - i dd(tau) (m/2 dv(x, (-i tau), 2) + V(x)) \
               & = 1/planck integral_(x(planck beta) = x(0)) dd(tau) (m/2 dv(x, tau, 2) + V(x))
$

For time-slicing $k$, we can build upon the classical interpretation:

$
  H ({x_k}) = 1/(planck beta) sum_(k=1)^M [m/2 (x_k-x_(k-1))^2/(epsilon^2) + V(x_(k-1))] epsilon
$

Is generally a harmonic string where potential is split equally among these beads.

$
  Z = 1/(N!) sum_sigma eta^(abs(sigma)) integral product_(i=1)^N dd(x_i (tau), d: upright(D)) delta(x_i (planck beta) - x_(sigma(i)) (0)) e^(- S_E \/ planck)
$

For all permutation $sigma$, where $eta = plus 1$ for bosons and $minus 1$ for fermions.

=== Free Particle

$
  Z_"free" = integral_(x(planck beta) = x(0)) dd(x, upright: D) exp(-m/(2 planck) integral_0^(planck beta) dd(tau) dot(x)^2)
$

Because $x(tau)$ satisfy boundary condition as a fourier modes:

$
  x(tau) = sum_(n=-infinity)^infinity x_n e^(i omega_n tau), quad omega_n = (2pi n)/(planck beta), quad x_(-n) = x^*_n
$


$
  integral_0^(planck beta) dd(tau) dot(x)^2 &= sum_(n=-infinity)^infinity sum_(n' = -infinity)^infinity integral_0^(planck beta) dd(tau) thin i omega_n x_n i omega_(n') x_(n') e^(i (omega_n - omega_(n')) tau) \
  &= sum_(n=-infinity)^infinity sum_(n' = -infinity) planck beta delta_(n n') x_n x_n' omega_n omega_(n') \
  &= planck beta sum_(n=-infinity)^infinity abs(x_n)^2
$

The mesasure $dd(x, d: upright(D))$ is proportional to $product_n dd(x_n) dd(x_(-n))$ with appropriate normalization.

$
  Z_"free" = product_(n>=0) integral dd(x_n) dd(x_(-n)) exp(-m/(2 planck) planck beta omega_n^2 (abs(x_n)^2 + abs(x_(-n))))
$

$
  integral dd(x_n) exp(-m/(2 planck) planck beta omega_n^2 abs(x_n)^2) = (2pi/(m beta omega_n^2))^(1/2)
$

For zero eigenvlue $x(tau) = "const"$:

$
  x(tau) = x_0 + x' (tau) => Z [x_0] = integral_(-infinity)^infinity dd(x_0) = V
$

Then

$
  1/ planck planck beta omega_n^2 = (2pi n)^2/(planck^2 beta)
$

$
  Z_"free" = V product_(n=1)^infinity ((planck^2 beta)/(2pi m n^2))
$

Define the spectral zeta function $zeta_(Pi) (s)$ associated with the iegenvalues $lambda_n$:

$
  product_(n=1)^infinity lambda_n = exp(sum_(n=1)^infinity ln lambda_n)
$

$
  sum_(n=1)^infinity lambda_n^(-s) ln lambda_n = evaluated((- sum_(n=1)^infinity lambda_n^(-s)))_(s=0) = - zeta'_(Pi) (s = 0)
$

$
  zeta_(Pi) (s) = sum_(n=1)^infinity lambda_n^(-s)
$

So it equal to:

$
  Z_"free" = V exp(-zeta((planck^2 beta)/(2 pi m n^2)') (s=0))
$

Generally, for $zeta (s) = sum_(n>=1) 1/n^s$:

$
  zeta (0) = - 1/2
$

$
  zeta' (0) = 1/2 ln (2 pi)
$

Which we will not prove here.

Suppose $lambda_n = c n^(-s)$:

$
  zeta'_(Pi) (0) = -1/2 ln (c) + ln (2pi)
$

$
  - zeta'_(Pi) (0) = 1/2 ln (c) - ln (2pi) = ln ((m/(2pi planck^2 beta)^(1/2)), quad c = (2pi m)/(planck^2 beta)
$

$
  Z_"free" = V (m/(2pi planck^2 beta))^(1/2)
$

This is exactly the well-known result for a free particle in 1-dimension for a volume $V$

=== Vector Potential

For particle in vector potential, the action, which is Lagrange of particle in vector potential is:

$
  S [bold(x)] = integral_(x_i)^(x_f) dd(t) [L(x,dot(x)) - e bold(A)(bold(x)) dot dot(bold(x))]
$

For certain Lagrange of the particle without vector potential.

The Euclidean action is the variable transformation:

$
  S_E [bold(x)] = integral_0^(planck beta) dd(tau) [L(x,dot(x)) + i e bold(A) (bold(x)) dot dot(bold(x))]
$

We focus on the latter term:

$
  integral_0^(planck beta) dd(tau) i e bold(A) (bold(x)) dot dot(bold(x)) = i e integral_(x_i)^(x_f) dd(bold(x)) dot bold(A)
$

Which is the line integral of vector potential along the path. If path closed:

$
  "LHS" = i e integral_S dd(bold(S)) dot (nabla times A) = i e integral_S dd(bold(S)) dot B = i e Phi_S
$

Is the magnetic flux through the area swept by the particle.

However, it's heuristic to derive from Hamitonian:

$
  U(t_f,t_i) = integral dd(bold(p), bold(x), d: upright(D)) exp[i/planck integral_(t_i)^(t_f) dd(t) (bold(p) dot dot(bold(r)) - H(bold(p),bold(r))]
$

The term in exponent involving $bold(p)$ is:

$
  - 1/(2m planck) (bold(p)^2 - 2 bold(p) dot (e bold(A)(bold(r)) + m dot(bold(r)) + e^2 bold(A)^2(bold(r)))
$

To integrate over $bold(p)$, we complete the square:

$
  bold(p)^2 - 2 bold(p) dot (e bold(A) + m dot(bold(r)) = (p-(q bold(A) + m dot(bold(r))))^2 - (q bold(A) + m dot(bold(r)))^2
$

$
  i/(2m planck) [(q bold(A) + m dot(bold(r)))^2 - e^2 bold(A)^2] = i/planck [1/2 m dot(bold(r))^2 + q dot(bold(r)) dot bold(A)(bold(r))]
$

$
  L = 1/2 m dot(bold(r))^2 + q dot(bold(r)) dot bold(A)(bold(r))
$

== Gross-Pitaevskii Equation

For bosons with a contact interaction $bold(V)(r,r') = g delta(r - r')$:

$
  hat(H) = integral dd(r) hat(psi)^dagger (r) [- (planck^2 nabla^2)/(2m) + V_("ext")(r)] hat(psi)(r) + 1/2 integral dd(r, r') hat(psi)^dagger (r) hat(psi)^dagger (r') V(r,r') hat(psi)(r') hat(psi) (r)
$

$
  hat(H) = integral dd(r) [hat(psi)^dagger (r) [- (planck^2 nabla^2)/(2m) + V_("ext")(r)] hat(psi)(r) + g/2 hat(psi)^dagger(r) hat(psi)^dagger(r) hat(psi)(r) hat(psi)(r)]
$

$
  S & = integral dd(t) i planck psi^* partial_t psi - hat(H)(psi^*,psi) \
$

$
  pdv(S, psi^*, d: delta) = i planck partial_t psi - (- (planck^2 nabla^2)/(2m) + V_("ext")(r)) psi - g abs(psi)^2 psi = 0
$

Rearranging gives the *GP Equation*:

$
  i planck pdv(psi, t) = (- (planck^2 nabla^2)/(2m) + V_("ext")(r) + g abs(psi)^2) psi(bold(r), t)
$

== Matsubara sums

Evaluate $I = 1\/(planck beta) sum_(omega_n) e^(i omega epsilon) \/ (i omega_n - x)$

Consider function $f(z) = e^(epsilon z)/(z - x) n_(eta) (z)$ where $n_eta (z) = 1/(e^(planck beta z - eta)$.

The function $n_eta (z)$ has poles at the Matsubara frequencies $z = i omega_n$:

- Bosons ($eta = 1$): $omega_n = (2 n pi)/(planck beta)$.
- Fermions ($eta = -1$): $omega_n = ((2n + 1) pi)/(planck beta)$.

The residues of $n_eta (z)$ at each $i omega_n$ is $1/(planck beta)$.

Integrate $f(z)$ over a large circle $C$ at infinity. For $0 < epsilon < planck beta$, the factor $e^(epsilon z)$ and $n_eta (z)$ ensure that the integral vanishes as the radius $R -> infinity$.

$
  integral.cont_C (dd(z))/(2pi i) f(z) = sum Res(i omega_n) + Res(x) = 0
$

- At $z = i omega_n$, the residue is $e^(i omega_n epsilon)/(i omega_n x) dot 1/(planck beta)$.
- At $z = x$: The residue is $e^(epsilon x)/(e^(planck beta x) - eta)$.

$
  1/(planck beta) sum_(omega_n) e^(i omega_n epsilon)/(i omega_n - x) = - e^(epsilon x)/(e^(planck beta x) - eta)
$

== Coherent-state path integral

Recall that for coherent states $ket(psi)$, the identity operator is expressed as:

$
  hat(1) = integral dd(psi^*, psi)/(N) e^(-psi^* psi) ketbra(psi)
$

When we time-slice the evolution operator:

$
  braket(psi_k, e^(-i/planck hat(H)(hat(a)^dagger,hat(a)) epsilon), psi_(k-1)) approx braket(psi_k, (1-i/planck hat(H)(hat(a)^dagger,hat(a))epsilon), psi_(k-1))
$

$
  braket(psi_k, hat(H)(hat(a)^dagger,hat(a)), psi_(k-1)) = hat(H)(psi^*_k, psi_(k-1)) braket(psi_k, psi_(k-1))
$

Using the overlap formula for coherent states, $braket(psi_k, psi_(k-1)) = e^(psi^*_k psi_(k-1))$, we get:

$
  "LHS" approx exp(psi^*_k psi_(k-1) - i/planck epsilon H(psi^*_k, psi_(k-1)))
$

Generally, the action looks like this:

$
  i/planck S[psi,psi^*] ({k}) = sum_(k=1)^M [psi^*_k psi_(k-1) - psi_k^* psi_k - (i epsilon)/planck H(psi^*_k, psi_(k-1))]
$

Where $- psi_k^* psi_k$ comes from the integral factor.

$
  psi_k^* psi_(k-1) - psi_k^* psi_k = - psi_k^* (psi_k - psi_(k-1))
$

$
  S[psi,psi^*] = integral_(t_i)^(t_f) dd(t) [i planck psi^*(t) dot(psi)(t) - H(psi^*(t), psi(t))]
$

$
  U(psi^*_f, t_f; psi_i, t_i) = e^(psi^*_f psi_f) integral dd(psi^*, psi, d: upright(D)) exp(i/planck S[psi^*,psi])
$

== Thermal traces and boundary conditions

$
  tr(hat(O)) = integral dd(psi^*, psi)/(N) e^(-psi^* psi) braket(eta psi, hat(O), psi)
$

Where $eta = 1$ for bosons and $eta = -1$ for fermions. Where the boundary condition can be evaluated as $psi(planck beta) = eta psi(0)$.

Based on previous deduction:

$
  braket(psi_k, e^(- epsilon/planck hat(K)), psi_(k-1)) approx e^(psi^*_k psi_(k-1)) e^(-epsilon/planck K(psi_k^*,psi_(k-1))
$

$
  Z = lim_(M->infinity) integral product_(k=1)^M &dd(psi_k^*, psi_k)/(N) \ &exp(sum_(k=1)^M [psi_k^* psi_(k-1) - psi^*_k psi_k - epsilon/planck hat(K) (psi^*_k, psi_(k-1))])
$

$
  S_E [psi^*,psi] = integral_0^(beta planck) dd(tau) psi^* (tau) planck partial_tau psi (tau) + H(psi^*,psi) - mu psi^* (tau) psi (tau)
$ <action_psi>

Which the $mu psi^* psi$ is the mass term or chemical potential from $Z = exp^(-beta (hat(H) - mu hat(N))$

For a non-interacting system, the Hamiltonian is quadratic: $hat(K)_0 = sum_alpha (epsilon_alpha - mu) hat(a)^dagger_alpha hat(a)_alpha$. THe functional integral decouples for each mode $alpha$.

For a single mode alpha, the discrete action in <action_psi> is a quadratic form $psi^dagger S psi$. Evaluate the matrix form:

- Diagonal: $psi^*_k psi_k$
- Off-diagonal: $psi^*_k psi_(k-1)$ and the $H$ term where $a = 1 - epsilon/planck (epsilon_alpha - mu)$.
- Corner: $psi_0 = eta psi_M$, the first slice $psi^*_1 psi_0$ actually becomes $psi^*_1 (eta psi_M)$.

$
  Z_0 &= lim_(M -> infinity) product_alpha integral product_(k=1)^M dd(psi^(alpha *)_k, psi^alpha_k)/N \ &quad quad exp(- sum_(k=1)^M psi_k^(alpha *) [(psi^alpha_k - psi^alpha_(k-1))] + epsilon(epsilon_alpha - mu) psi^(alpha)_(k-1)) \
  &= lim_(M->infinity) product_alpha integral product_(k=1)^M dd(psi^(alpha *)_k, psi^alpha_k)/N exp(- psi^(alpha dagger) S^((alpha)) psi^(alpha)) \
  &= lim_(M->infinity) product_alpha [det(S)^((alpha))]^(-eta)
$

Where $epsilon = beta/M$.

$
  a = 1-(beta (epsilon_alpha - mu))/M, quad S^((alpha)) = mat(1, 0, dots.c, -eta a; -a, 1, dots.c, 0; 0, -a, dots.down, 0; 0, 0, dots.c, 1), quad psi^(alpha) = vec(psi_1^alpha, dots.v, psi^alpha_M)
$

One can deduce the determinant by row reduction.

$
  det S^((alpha)) = 1 - eta a^M = 1 - eta lim_(M->infinity) (1- (beta Delta)/M)^M = 1 - eta e^(-beta Delta^alpha), quad Delta^alpha = epsilon_alpha - mu
$

$
  Z_0 = product_alpha (1 - eta exp(- beta(epsilon_alpha - mu))^(- eta)
$

From previous derivation of each single particle mode $alpha$:

$
  Z_(0, alpha) = [det S^((alpha))]^(-eta)
$

$
  Z_0 = exp(sum_alpha ln [det S^((alpha))]^(-eta)) = exp(-eta sum_alpha ln det S^((alpha)))
$

We now use the fundamental identity for any square matrix $M$:

$
  det M = exp(tr ln M)
$

$
  Z_0 = exp(- eta sum_alpha tr ln S^((alpha)))
$

We apply Lagrange transformation to the action.

$
  Z[J^*,J] = integral dd(psi^*, psi, d: upright(D)) exp(- S[psi^*,psi]/planck + sum_i (J_i^* psi_i + psi_i^* J_i))
$

In the discrete case:

$
  - sum_(j k) psi^*_j S_(j k) psi_k + sum_i (J_i^* psi_i + psi_i^* J_i)
$

This is the trick makes the Gaussian integral solvable. We shift the variables of $psi$ and $psi^*$ to elminate the linear source terms.

$
  phi.alt = psi - S^(-1) J, quad phi.alt^* = psi^* - J^* S^(-1)
$

$
  psi^* S psi - J^* psi - psi^* J = phi.alt^* S phi.alt + J^* S^(-1) J
$

$
  Z[J^*,J] = Z_0 exp(J^* S^(-1) J)
$

Note that $Z_0 = [det S]^(-eta)$ as derivd previously.

$
  G_(q r) = - expval(psi_q psi^*_r) = -1/Z_0 integral dd(psi^*, psi, d: upright(D)) psi_q psi^*_r exp(- 1/planck S_E)
$

Using the property of exponentials, we can replace the variables $psi$ and $psi^*$ with the deriatives with respect to their sources:

$
  psi_q -> pdv(, J_q^*), quad psi_r^* -> pdv(, J_r)
$

$
  G_(q r) = - eta/Z_0 pdv(, J_q^*, J_r) [Z_0 exp(sum_(j k) J_j^* (S^(-1))_(j k) J_k)]_(J = J^* = 0) = - (S^(-1))_(q r)
$

When we differentiate $J_j^* (S^(-1))_(j k) J_k$ with respect to $J_q^*$, $J_r$, only the term where $j=q$ and $k=r$ survivies. Then we requires to find the elements of $S^(-1)$ that $S dot G = - I$.

$
  sum_j S_(k j) G_(j r) = - delta_(k r)
$

$
  G_(1 r) - eta a G_(M r) = - delta_(1 r), quad k = 1
$

$
  G_(k r) - a G_(k-1) r = - delta_(k r), quad k > 1
$

Away from the source at $k=r$, the equation is simply $G_(k r) = a G_(k-1 r)$.

In general for $k >= r$:

$
  G_(r+1,r) = a G_(r r) => G_(r + 2,r) = a^2 G_(r r) => G_(k r) = a^(k - r) G_(r r)
$

For $k < r$:

$
  G_(1 r) = eta a G_(M r) = eta a (a^(M - r) G_(r r)) = eta a^(M - r + 1) G_(r r)
$

$
  G_(k r) = a^(k-1) G_(1 r) = a^(k-1) (eta a^(M - r + 1) G_(r r)) = eta a^(M - r + k) G_(r r)
$

To anchor these formulas, we evaluate diagonal term:

$
                        G_(r r) - a G_(r - 1 r) & = - 1 \
  G_(r r) - a (eta a^(M - r + (r - 1)) G_(r r)) & = - 1 \
                      G_(r r) - eta a^M G_(r r) & = - 1 \
                            G_(r r) (1-eta a^M) & = - 1 \
                                        G_(r r) & = -1/(1- eta a^M)
$

When $M -> infinity$, $a^M -> exp(-beta Delta)$, and $a^(k - r) -> exp(- (tau_q - tau_r) Delta \/ planck)$.

Recall the density distribution:

$
  n_alpha = 1/(e^(beta Delta) - eta), quad 1 + eta n_alpha = 1/(1-eta e^(-beta Delta)) = G_(r r)
$

For $tau_q > tau_r thin (k > r)$:

$
  G_(q r) = a^(k - r) G_(r r) = e^(-Delta (tau_q - tau_r) \/ planck) (1 + eta n_alpha)
$

For $tau_q < tau_r thin (k < r)$:

$
  G_(q r) = eta a^(M - (r - k)) G_(r r) & = eta e^(- beta Delta) e^(- Delta (tau_q - tau_r) \/ planck) (1 + eta n_alpha) \
                                        & = - e^(- Delta (tau_q - tau_r) \/ planck) (eta n_alpha)
$

$
  G_0 (tau_q, tau_r) = - e^(- Delta (tau_q - tau_r) \/ planck) [theta(tau_q - tau_r) (1+eta n_alpha) + eta theta(tau_r - tau_q) n_alpha]
$

We already now that $G_(0)^((alpha)) = - [S^((alpha))]^(-1)$ that:

$
  Z_0 = exp (-eta sum_alpha tr ln(-[G_0^((alpha))]^(-1)))
$

I we look at its structure in discrete time-slice representation, it looks exactly like the matrix $S$ but the scalar $a$ replaced by the operator $hat(a) = 1 - beta(hat(h)_0 - mu) \/ M$, where $hat(h)_0$ is the single particle Hamiltonian.

Since the grand potential is $Omega = - k_B T ln Z$, the formula gives:

$
  Omega_0 = eta k_B T tr ln (- hat(G)_0^(-1))
$

= Perturbative expansion

Suppose $S = S_0 + S_V$.

$
  Z = integral dd(psi^*, psi, d: upright(D)) exp(-(S_0 + S_V)/planck)
$

$
  Z = Z_0 dot Z/Z_0
$

By definition, the ratio on the right is the expectation alue of the operator $e^(- S_V \/ planck)$ with respect to the non-interacting weight $e^(-S_0 \/ planck)$.

$
  Z = Z_0 expval(exp^(-S_V \/ planck))_0
$

However, it's not applicable to directly solve it, we expand the exponential function:

$
  expval(exp(-S_V \/ planck)) = expval(sum_(n=0)^infinity 1/(n!) (-S_V/planck)^n)_0
$

$
  Z/Z_0 = sum_(n=0)^infinity (-1/planck)^n 1/(n!) expval(S_V^n)_0
$

It's directly that for a set of complex variables:

$
  (integral dd(upright(z)^*, upright(z)) (z_i z_j^*) e^(- upright(z)^* S upright(z)))/(integral dd(upright(z)^*, upright(z)) e^(- upright(z)^* S upright(z))) = (S^(-1))_(i j)
$

$
  Z[J^*,J] = integral dd(psi^*, psi, d: upright(D)) exp(- S[psi^*,psi]/planck + sum_i (J_i^* psi_i + psi_i^* J_i)) = Z_0 expval(J^* S^(-1) J)
$

$
  expval(psi_i psi_j^*) = 1/Z_0 evaluated(pdv(Z, J_i^*, J_j))_(J=0) = pdv(, J_i^*, J_i) exp(sum_(a b) J^*_a (S^(-1))_(a b) J_b)
$

$
  expval(product_(i=1)^n psi_i product_(j=n)^1 psi_j^*)_0 = sum_sigma eta^(abs(sigma)) product_(i=1)^n (-G_0 (i,sigma(i))
$

For connection of element $i$ and $sigma(i)$. Which is the product generated by all permutation $sigma$.

- Contraction, i.e. a Green's function for non-interactive system, is repsented by a propagator line: #diagram($edge("r", "-|>-")$)
- Interaction element, is represented by a vertex, usually, the four body is two incoming and two outgoing lines: #text(5pt)[#diagram($edge("rd", "-<|-") & & & edge("ld", "-|>-") \ & edge("--<|--") \ edge("ru", "-<|-") & & & edge("lu", "-|>-")$)]

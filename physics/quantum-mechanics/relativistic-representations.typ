#import "../lib.typ": *
#import "@preview/physica:0.9.8": *

#show: daily-en.with(
  title: "Rep of Poincare",
)

#let lie(body) = $frak(body)$
#let vf(body) = $bold(upright(body))$
#let tb(body) = $tilde(bold(body))$

=

$
  x'^(nu) = tensor(Lambda, nu, -mu) x^mu + a^nu
$

$bold(x) = (x^mu, mu = 0,dots,D)$ in $d = D+1$-dimensional Minkovski space. $dd(s^2) = eta_(mu nu) dd(x^mu, x^nu)$, $eta_(mu nu) = "diag"(1,underbrace(-1\,dots\,-1, n))$. The matrix $Lambda$ define rotations of $O(d,1)$ group.

Consider Euclidean space is fine. $dd(s^2) = eta_(mu nu) dd(x^mu, x^nu)$ where $eta_(mu nu) = "diag"(1,dots,1)$.

$
  x''^(nu) = tensor(Lambda_1, nu, -mu) x'^mu + a_1^nu = tensor(Lambda_1, nu, -mu) tensor(Lambda_2, mu, -xi) x^xi + tensor(Lambda_1, nu, -mu) a_2^mu + a_1^nu
$

$
  (Lambda_1, bold(a)_1) dot (Lambda_2, bold(a)_2) = (Lambda_1 Lambda_2, bold(a_1) + Lambda_1 bold(a)_2)
$

$
  g^(-1) = (Lambda^(-1),- Lambda^(-1) a)
$

$
  I O (d,1) = T(d) times.r O(d,1)
$

The one-to-one correspondence between vector $x in bb(R)^(d,1)$ and $2 times 2$ Hermitian matrices. It's a isomorphism in lie algebra such that:

$
  & lie("so")(2,1;bb(C)) tilde.equiv lie("so")(3,bb(C)) tilde.equiv lie("sl")(2;bb(C)) tilde.equiv lie("sp")(2;bb(C)) \
  & lie("so")(3,1;bb(C)) tilde.equiv lie("so")(4;bb(C)) tilde.equiv lie("sl")(2;bb(C)) plus.o lie("sl")(2;bb(C)) \
  & lie("so")(5,1;bb(C)) tilde.equiv lie("so")(6;bb(C)) tilde.equiv lie("sl")(4;bb(C))
$

$
  lie("so")(4)_(bb(R)) tilde.equiv lie("su")(2) plus.o lie("su")(2)
$

As real vector space.

$
  bold(x) <-> X, quad X = x^mu sigma_mu
$

$
  sigma_mu sigma^nu = tensor(delta, nu, -mu) + tensor(epsilon, -mu, nu, xi) sigma_xi
$

$
  "Tr"(x^mu sigma_mu sigma^nu) = "Tr"(x^mu (tensor(delta, nu, -mu) + tensor(epsilon, -mu, nu, xi) sigma_xi)) = 2 x^mu
$

$
  x^mu = 1/2 "Tr"(X sigma^mu)
$

Then $X$ should follow the same obligation of $x^mu$, transforming as below:

$
  X' = U X U^dagger + A, quad sigma_nu tensor(Lambda, nu, -mu) = U sigma_mu U^(dagger), A = a^mu sigma_mu
$

We fix the arbitrariness of matrix $U$ due to surjection in constraint of $U$ indicating non-one-to-one correspondence of $Lambda$ and $U$.

$
  det U = 1
$

$
  I s p (d,1) = T(d) times.r S p i n (d,1)
$

$
  (U_1, A_1) dot (U_2, A_2) = (U_1 U_2, U_1 A_2 U_1^dagger)
$

$
  g^(-1) = (U^(-1), - U^(-1) A U^(-1)^dagger)
$

Suppose $alpha(g)$ is the action of $alpha(g): f -> f'$ and $beta(g)$ is the action of $beta(g): g_0 -> g'_0$. Such action representation would be reduced to a notation as $g dot (-)$. Where left is $g_L dot (-)$ and right is $g_R dot (-)$ for simplicity.

$
  g_L dot f(g_0) = f'(g_0) = f(g_L dot g_0)
$

$
  g_R dot f(g_0) = f'(g_0) = f(g_R dot g_0)
$

Clearly:

$
  g_1 dot (g_2 dot f(g_0)) = g_2 dot f(g_1 dot g_0) = f(g_2 dot (g_1 dot g_0))
$

Is contravariant.

So the action should be canonically:

$
  beta(g_2) compose beta(g_1) = beta(g_1 g_2), quad beta(e) = "Id"
$

a anti-homomorphism. We left with two choices:

$
  beta(g)_L dot g_0 = g^(-1) g_0, quad beta(g)_R dot g_0 = g_0 g
$

$
  g_L dot f(g_0) = f(g^(-1) g_0), quad g_R dot f(g_0) = f(g_0 g)
$

Suppose $G = tilde(L)(3,1)$:

$
  g_0 <=> (bold(x),bold(z),tb(z)) := (bold(x),vf(z)) <=> (X,Z) , quad X = x^mu sigma_mu, Z in S L (2; bb(C))
$

$
  g <=> (bold(a), Lambda) <=> (A,U), quad g^(-1) <=> (-Lambda^(-1) bold(a), Lambda^(-1)) <=> (- U^(-1) A U^(-1)^dagger, U^(-1))
$

Where $Z$ is spin coordinates:

$
  Z = (bold(z), tilde(bold(z))) = mat(z_1, tilde(z)_1; z_2, tilde(z)_2) \
  z'_alpha = tensor(U, -alpha, beta) z_beta, quad tilde(z)_alpha = tensor(U, -alpha, beta) tilde(z)_beta, quad z_1 tilde(z)_2 - tilde(z)_1 z_2 = 1
$

$
  det Z' = det U det Z = det Z
$

We fix the determinant as $det Z = 1$ as $Z in S L (2; bb(C))$

$
  g'_0 = g g_0 &tilde.eq (X',Z') = (A, U) dot (X,Z) = (U X U^dagger + A, U Z) \
  &tilde.eq (bold(x)', bold(z)', tb(z)') = (bold(a),Lambda) dot (bold(x),bold(z),tb(z)) =(Lambda bold(x) + bold(a), U bold(z)', U tb(z)') quad Lambda <-> U\
$

$
  g'_0 = g_0 g^(-1) &tilde.eq (X,Z) dot (-U^(-1) A U^(-1)^dagger, U^(-1)) = (Z (-U^(-1) A U^(-1)^dagger) Z^dagger + X, Z U^(-1)) \
  &= (X - (Z U^(-1)) A (Z U^(-1))^dagger, Z U^(-1)) \
$

If we consider $S L (2;bb(C))$, $U^dagger != U^(-1)$ where $z, z^*$ is the independent variables leading to a complexification where we consider $x + i y = z$ behaves differently. However, use $(z,z^*)$ is a better choice which shares the same behaviors.

One can plugin $(-)dot (A,U)$ for simplicity:

$
  (X,Z) dot (A,U) = (X + Z A Z^dagger, Z U)
$

However, because $Lambda -> U$ is many to one. There's no canonical right action by representation of coordinates. So we can define a correspondence by certain choice #footnote[The choice is arbitrary for exactness only if possible. Or we say we define a *filter* for choice.].

Define a map $L (Lambda) = U$ for such choices.

$
  g'_0 = g_0 g^(-1) &tilde.eq (bold(x),bold(z),tb(z)) dot (bold(a),Lambda) = (bold(x) + Z bold(a) , L(Lambda) bold(z), L(Lambda) tb(z)) quad Lambda <-> L(Lambda) = U
$

==

$
           T(a): & bold(x) -> bold(x) + bold(a) \
  Lambda(omega): & bold(x) -> Lambda bold(x) \
$

$
  hat(X) = lr(dv(g(t), t) bar)_(t=0), quad g(0) = e
$

$
  tensor(Lambda, mu, -rho) tensor(eta, -mu, -nu) tensor(Lambda, nu, -sigma) = tensor(eta, -rho, -sigma)
$

$
  tensor(Lambda, mu, -nu) = tensor(delta, mu, -nu) + tensor(omega, mu, -nu) => tensor(eta, -mu, -nu) tensor(omega, mu, -rho) + tensor(eta, -mu, -nu) tensor(omega, nu, -sigma) = 0 => tensor(omega, -nu, -rho) + tensor(omega, -mu, -sigma) = 0
$

Therefore, $T(a)$ and $Lambda(theta)$ as operator upon algebraic object of representation would be:

$
  T(a) = 1 + i a^mu hat(p)_mu + O(a^2), quad Lambda(theta) = 1 + i omega^(mu nu) hat(J)_(mu nu) + O(omega^2)
$

$
  tensor(omega, mu, nu) = - tensor(omega, nu, mu) => J_(mu nu) = - J_(mu nu) => tensor(J, mu, nu) prop tensor(gamma, mu) and tensor(gamma, nu)
$

Where second identity from the swapping and relabelling of indices. Then $J^(mu nu)$ as operator should be inducing a anti-symmetric algebra.

Indeed:

$
  delta V^rho = tensor(omega, rho, -sigma) V^sigma = tensor(eta, rho, alpha) tensor(omega, -alpha, -sigma) V^sigma &= tensor(eta, rho, alpha) 1/2 (tensor(omega, -alpha, -sigma) V^sigma - tensor(omega, -sigma, -alpha) V^sigma) \
  &= 1/2 (omega_(alpha sigma) eta^(rho alpha) V^sigma - omega_(sigma alpha) eta^(rho alpha) V^sigma)) \
  &= 1/2 omega_(alpha sigma) (eta^(rho alpha) V^sigma - eta^(rho sigma) V^alpha) quad "swap second term": sigma <-> alpha \
  &= 1/2 omega_(alpha sigma) [J^(alpha sigma), V^rho]
$

Where the last identity from the evaluation of $Lambda(theta)$ on vector should be same as the variation of transformation of vector. If we want a *quantum style*, as previous shown, we add $i$, the imaginary unit.

$
  [J^(mu nu), V^rho] = i (eta^(rho nu) V^mu - eta^(mu rho) V^nu)
$

$
  [J^(mu nu), p^rho] = i (eta^(rho nu) p^mu - eta^(mu rho) p^nu)
$

The final term can be evaluated:

$
  J^(mu nu) := gamma^mu and gamma^nu
$

By normalization of factor.

Consider the extension of anti-symmetric algebra should factor out a unique homomorphism from tensor algebra such that:
$
  gamma^mu times.o gamma^nu = 1/2 (gamma^mu times.o gamma^nu + gamma^nu times.o gamma^mu) + 1/2 (gamma^mu times.o gamma^nu - gamma^nu times.o gamma^mu) => eta^(mu nu) + gamma^mu and gamma^nu
$

Where $eta^(mu nu)$ of symmetric part is the bilinear-form endowed as Minkovski metric which can be achieved by normalization. Or better, the commutator must be closed as a linear form of $eta$, therefore it must be proportional to the metric.

Usually, we notate $gamma^mu times.o gamma^nu = gamma^mu gamma^nu$ for simplicity just like other tensor.

$
  gamma^mu gamma^nu and gamma^rho &= gamma^mu (gamma^nu and gamma^rho) + (gamma^mu and gamma^rho) gamma^nu \ &= gamma^mu gamma^nu gamma^rho - gamma^mu eta^(nu rho) + gamma^mu gamma^rho gamma^nu - gamma^(mu rho) gamma^nu \
  &= 2 gamma^mu eta^(nu rho) - gamma^mu eta^(nu rho) - eta^(mu rho) gamma^nu quad [gamma^nu gamma^rho]_+ = 2 eta^(nu rho) \
  &= gamma^mu eta^(nu rho) - gamma^(nu) eta^(mu rho)
$

If one evaluate bracket identity:

$
  [A B,C] = A [B,C]_+ - [A,C]_+ B
$

By homomorphism in tensor, we evaluate in bracket.

$
  J^(mu nu) and gamma^rho = gamma^mu gamma^nu and gamma^rho = [gamma^mu gamma^nu, gamma^rho] = gamma^mu eta^(nu rho) - gamma^nu eta^(mu rho)
$

$
  [J^(mu nu), J^(rho sigma)] &= gamma^mu gamma^nu and gamma^rho gamma^sigma quad "due to" eta^(mu nu) and gamma^rho = 0 \
  &= (gamma^mu gamma^nu and gamma^rho) gamma^sigma + gamma^rho (gamma^mu gamma^nu and gamma^sigma) \
  &= gamma^mu gamma^sigma eta^(nu rho) - gamma^nu gamma^sigma eta^(mu rho) + gamma^rho gamma^mu eta^(nu sigma) - gamma^rho gamma^nu eta^(mu sigma) \
  &= J^(mu sigma) eta^(nu rho) - J^(v sigma) eta^(mu rho) + J^(rho mu) eta^(nu sigma) - J^(rho nu) eta^(mu sigma) "expanding" gamma^mu gamma^nu "then" eta^(mu nu) eta^(sigma rho) "cancelled"
$

// One can also compute in matrix contraction such that $tensor((J^(mu nu)),-alpha,-beta) = tensor(delta,mu,-alpha) tensor(delta,nu,-beta) - tensor(delta,mu,-beta) tensor(delta, nu,-alpha)$ for matrix $(alpha,beta)$, Therefore $J^(mu nu) J^(rho sigma) = J^(mu sigma) eta^(nu eta) - J^(nu sigma) eta^(mu rho)$.
//
In order to deduce the generator in representation:

$
  hat(xi) dot f(g_0) = lr(dv(, t) f (e^(- t hat(xi)) dot g_0)|)_(t=0)
$

Where $e^(- t xi)$ is the lift to certain $g in G$ by parametrization of $t$.

$
  T(a)_L (t) dot g_0 = T(a)^(-1)(t) (bold(x),vf(z)) = (bold(x) - bold(t) bold(a), vf(z))
$

$
  lr(dv(, t) f (T(a)_L (t) dot g_0)|)_(t=0) = lr(dv(, t) f(bold(x) - bold(t) bold(a),vf(z))bar)_(t=0) = - a^mu pdv(f, x^mu) = a^mu hat(p)_mu (f(bold(x),vf(z)))
$

$
  hat(p)_L_mu = - i pdv(, x^mu)
$

In quantum style.

Rotation is already evaluated by $delta V^rho = tensor(omega, rho, -mu) V^mu$.

$
  dv(, t) f(Lambda(omega)_L (theta) dot g_0) &= lr(dv(, t) (f (x^rho - theta thin omega^(mu nu) (tensor(eta, rho, -nu) x_mu - tensor(eta, rho, -mu) x_nu ), vf(z)))bar)_(theta = 0) \
  &= - omega^(mu nu) (tensor(eta, rho, -nu) x_mu - tensor(eta, rho, -mu) x_nu) pdv(f, x^rho) \
  &= - omega^(mu nu) (pdv(f, x^nu) x_mu - pdv(f, x^mu) x_nu)
$

$
  L_L_(mu nu) = i(pdv(, x^mu) x_nu - pdv(, x^nu) x_mu)
$

Generally, it's easier to calculate by:

$
  delta f = delta x^mu pdv(f, x^mu)
$

For any coordinates.

The generator for spin basis follows the same routine:

$
  U(omega) = exp (-i/2 omega^(mu nu) Sigma_(mu nu)) in S L (2;bb(C))
$

Where $Sigma_(mu nu) <-> J_(mu nu)$ is the matrix representation of generator that generates element $U$. It's instructive to mention that $mu,nu$ is not matrix element but indices of *generators*.

$
  Sigma_(mu nu) := tensor((Sigma_(mu nu)), alpha, -beta)
$

$
  z_alpha -> z_alpha - 1/2 omega^(mu nu) tensor((Sigma_(mu nu)), alpha, -beta) z_alpha pdv(f, z^alpha)
$

$
  S_L_(mu nu) = 1/2 tensor((Sigma_(mu nu)), alpha, -beta) z_alpha pdv(, z^alpha)
$

Where $S_(mu nu)$ is the group action on $f$ induced by matrix representation $Sigma_(mu nu)$ action on $z_alpha$. It's tough to evaluate the concrete form of $Sigma_(mu nu)$.

As for right action, by the action evaluation in matrix representation:

$
  (X,Z) dot (A,U) = (X + Z A Z^dagger, Z U)
$

$
  hat(p)_R_(mu) = tensor((L^(-1) (Lambda)), -mu, nu) hat(p)_L_nu, quad hat(J)_R_(mu nu) = hat(S)^R_(mu nu)
$

By inspection.

In following section, we *omit* left action due to the canonical coordinates representation.

#quote(
  attribution: [FIELDS ON THE POINCARE ́ GROUP: Arbitrary Spin Description and Relativistic Wave Equations],
  block: true,
)[
  In the framework of theory of the scalar functions on the Poincar ́e group a standard spin description in terms of multicomponent functions arises under the separation of space and spin variables.

  Since $vf(z)$ is invariant under translations, one may decomposed $dots$
]

$
  f(bold(x),vf(z)) = phi^i (vf(z)) psi_i (bold(x))
$

Where $phi^i (vf(z))$ forms a *basis* in the representation space of Lorentz group. The basis can be transformed as:

$
  phi^i (vf(z)') = phi^j (vf(z)') dot tensor(U, -j, i)
$

By apply group action in matrix multiplication.

To reduce notation, It's simpler to omit indices in summation.

$
  f'(bold(x)',vf(z)') = phi(vf(z)') psi'(bold(x)') = (phi(vf(z)) dot U) psi'(bold(x)') = phi(vf(z)) psi'(bold(x)')
$

$
  psi'(bold(x)') = U^(-1) dot psi(bold(x)) = U^(-1) psi(g_L dot bold(x)')
$

It suggests that:

$
  g_L dot psi(bold(x)) = U^(-1) dot psi(g_L dot bold(x)) = U^(-1) dot psi(Lambda^(-1) (bold(x) - bold(a)))
$

// $
// 	[sigma_mu, sigma_nu]_+ = 2 delta_(mu nu) \
// 	(sigma_mu)^T = - sigma_mu
// $

// $
// 	sigma_mu = - sigma_nu^(-1) sigma_mu sigma_nu = - sigma_nu sigma_mu sigma_nu quad mu != nu \
// $
//
$
  & overline(sigma)_mu = (sigma_0, -sigma_i) \
  & overline(x)_mu = (x_0, - x_mu) \
  & overline(X) = x^mu overline(sigma)_mu
$

Is the space reflection or parity transformation $P$. Reversely, $-overline((dot))$ indicates time reversal.

$
  & (X, Z) ->^P (overline(X), (Z^dagger)^(-1)) \
  & (X, Z) ->^T (-overline(X), (Z^dagger)^(-1)) \
  & (X, Z) ->^(P T) (- X, Z) \
  & (X, Z) ->^C (X^*, Z^*) \
$

$
  f(bold(x),vf(z)) ->^P f(overline(bold(x)),(vf(z)^dagger)^(-1))
$

$
  f(bold(x),vf(z)) ->^T f(- overline(bold(x)),(vf(z)^dagger)^(-1))
$

$
  f(bold(x),vf(z)) ->^C f^* (bold(x),vf(z))
$

Is charge conjugation by $i -> -i$.

=

Relativistic wave equations are nothing but eigenvalue problems for invariant operators acting on functions on the Poincaré group, and the successes and failures of all known higher-spin equations follow rigidly from the structure of Lorentz and Poincaré representations.

== Dimensions 1+1

$
  I s o (d=1,1) = T(2) times.r S O (1,1)
$

$
  f(bold(x),vf(z)) = f((x_1,x_2),theta)
$

$
  & hat(p)^2 = - partial_mu partial^mu \
  & hat(S) = - i partial_theta
$

$
  & hat(p)^2 f(x,theta) = m^2 f(x,theta) \
  & hat(S) f(x,theta) = lambda f(x,theta) \
$

$
  f(x,theta) = psi(x) e^(plus.minus i lambda theta)
$

In rest frame, it's easy to write down:

$
  f_"rest" (x,theta) = e^(plus.minus i m x^0) (e^(i lambda theta) plus.minus e^(- i lambda theta))
$

But the general problem is still unsolved that how to construct a invariant under improper Poincaré group#footnote[where the representation space must be invariant under $P: cal(H) -> cal(H)$.] with definite solution.

$
  hat(p)_mu hat(Gamma)^mu f(x, theta) = kappa f(x,theta)
$

$
  hat(Gamma)^mu := hat(Gamma)^mu (theta, pdv(, theta))
$

The group can be extended from $S O(1,1)$ to $S O (2,1) ~ S U (1,1)$ where $s = abs(lambda)$ is invariant under parity offering a potential solution. It's worth to note that any element $g in S O (1,1)$ is a rotation of *time-space* plane. To formalize the correspondence, one may fix the *space* plane rotation element as $hat(Gamma)^0$, consequently, $hat(S) in S O(1,1) subset S O (2,1)$ is identified as $hat(Gamma)^(1\/2)$.

$
  [hat(Gamma)^i, hat(Gamma)^j] = epsilon^(i j k) hat(Gamma)_k , quad hat(Gamma)^i hat(Gamma)_i = s(s+1), quad eta = "diag"(1,-1,-1)
$

We still apply quantum style where the commutator generate $i$ the imaginary unit.

$
  [hat(Gamma)^i, hat(Gamma)^j] = i epsilon^(i j k)hat(Gamma)_k
$

$
  hat(Gamma)^i = A^i (theta) + B^i (theta) partial_theta \
$

$
  [hat(S), f(theta)] = - i f'(theta), quad [hat(S),partial_theta] = 0
$

$
  [hat(S) = hat(Gamma)^2, hat(Gamma)^i] = - i (A'^i (theta) + B'^i (theta) partial_theta) = i epsilon^(i j) hat(Gamma)_j, quad i,j in {0,1}
$

$
   A'_i & = - tensor(epsilon)^j_i A_j \
  A''_i & = epsilon_i^j epsilon^i_j A_i = A_i quad i <-> j \
    A_i & = C_(1 i) cosh theta + C_(2 i) sinh theta \
    B_i & = D_(1 i) cosh theta + D_(2 i) sinh theta \
$

$
  [f(theta), g(theta) partial_theta] = - f'(theta) g(theta) \
  [f(theta) partial_theta, g(theta) partial_theta] = (f(theta) g'(theta) - g f'(theta)) partial_theta
$

$
  [hat(Gamma)^0, hat(Gamma)^1] & = i hat(Gamma)^2 = i hat(S) = partial_theta \
                               & = [A^0 + B^0 partial_theta, A^1 + B^1 partial_theta] \
                               & = (B^0 A'^1 - B^1 A'^0) + (B^0 B'^1 - B^1 B'^0) partial_theta \
                               & = partial_theta
$

$
  B^0 A'^1 - B^1 A'^0 & = 0 \
              B^0/B^1 & = A'^0/A'^1 \
$

$
  B^0 B'^1 - B^1 B'^0 = 1 \
$

It's clear that one can fix $B_0 = - sinh theta$, then $B_1 = -cosh theta$. Therefore $A_0 = cosh theta$, $B_0 = sinh theta$ invariant up to constant.

$
  hat(Gamma)^0 = C cosh theta - sinh theta pdv(, theta), quad hat(Gamma)^1 = C sinh theta - cosh theta pdv(, theta), quad hat(Gamma)^2 = hat(S) = - i pdv(, theta)
$

$
  hat(Gamma)^mu hat(Gamma)_mu = C^2 (cosh^2 theta - sinh^2 theta) + C (- sinh^2 theta + cosh theta^2) = C^2 + C = s(s+1) => C = s
$

In rest frame: $f(x,theta) = phi(theta) psi(x)$, $hat(p) psi(x) = plus.minus m$.

$
  hat(Gamma)^0 phi(theta) = (s cosh theta - sinh theta pdv(, theta)) phi(theta) &= plus.minus kappa/m phi(theta)\
  sinh theta pdv(, theta) phi(theta) &= (- (plus.minus kappa/m) + s cosh theta) phi(theta) \
  ln phi(theta) &= integral (- (plus.minus kappa/m)/(sinh theta) + s coth theta) d theta \
  ln phi(theta) &= - (plus.minus kappa/m) ln (tanh theta/2) + s ln (sinh theta) \
  phi(theta) &= C (sinh theta)^s (tanh theta/2)^(minus.plus kappa\/m)
$

Indeed, $kappa = plus.minus m s$.

$
  f_"rest" (x,theta) = C_1 e^(i m x_0) (cosh theta/2)^(2s) + C_2 e^(-i m x_0) (sinh theta/2)^(2s)
$

For a *fixed* axial spin system.

$
  (cosh theta/2)^(2 s) = sum_(lambda = -s)^s a_lambda e^(lambda theta) \
  (sinh theta/2)^(2 s) = sum_(lambda = -s)^s b_lambda e^(lambda theta)
$

Forming a spin basis containing $2s+1$ components. So one can expand in basis to yield a matrix action on space part:

$
  hat(p)^mu hat(Gamma)_mu (psi^i (x) phi_i (theta)) &= hat(p)^mu psi^i (x) hat(Gamma)_mu phi_i (theta) \
  &= hat(p)^mu psi^i (x) tensor((hat(Gamma)_mu), -i, j) phi_j (theta) = m psi^i (x) s phi_i (theta) \
  &= (1/s hat(p)^mu tensor((hat(Gamma)_mu), -i, j) -m) psi^i (x) = 0
$

For $s = 1\/2$, the function $f(x,theta) = sum_(lambda=-1/2)^(1/2) psi_(1/2,lambda) e^(lambda theta)$ as vector $Psi(x) = (psi_(1/2,1/2) (x), psi_(1/2,-1/2)(x))$.

$
  & hat(Gamma)^0 e^(theta/2) = 1/2 (cosh theta - sinh theta) e^(theta/2) = 1/2 e^(-theta) e^(theta/2) = 1/2 e^(-theta/2) \
  & hat(Gamma)^0 e^(-theta/2) = 1/2 (cosh theta + sinh theta) e^(-theta/2) = 1/2 e^(theta) e^(-theta/2) = 1/2 e^(theta/2)
$

$
  hat(Gamma)^0 vec(e^(theta/2), e^(-theta/2)) = vec(1/2 e^(-theta/2), 1/2 e^(theta/2)) \
  (hat(Gamma)^0) = mat(0, 1/2; 1/2, 0), quad 1/s (hat(Gamma)^0) = 2(hat(Gamma)^0) = sigma_1\
$

$
  & hat(Gamma)^1 e^(theta/2) = 1/2 (sinh theta - cosh theta) e^(theta/2) = - 1/2 e^(-theta/2) \
  & hat(Gamma)^1 e^(-theta/2) = 1/2 (sinh theta + cosh theta) e^(-theta/2) = 1/2 e^(theta/2)
$

$
  hat(Gamma)^1 vec(e^(theta/2), e^(-theta/2)) = vec(-1/2 e^(-theta/2), 1/2 e^(theta/2)) \
  (hat(Gamma)^1) = mat(0, -1/2; 1/2, 0), quad 1/s (hat(Gamma)^1) = 2(hat(Gamma)^1) = -i sigma_2 \
$

$
  & hat(Gamma)^2 e^(theta/2) = - i/2 e^(theta/2) \
  & hat(Gamma)^1 e^(-theta/2) = i/2 e^(-theta/2) \
$

$
  hat(Gamma)^2 vec(e^(theta/2), e^(-theta/2)) = vec(-i/2 e^(theta/2), i/2 e^(-theta/2)) \
  (hat(Gamma)^2) = mat(-i/2, 0; 0, i/2), quad 1/s (hat(Gamma)^2) = 2 (hat(Gamma)^2) = i sigma_3
$

For $s=1$, the function $f(x,theta) = sum_(lambda=-1)^1 psi_(1,lambda) e^(lambda theta)$ as vector $Psi(x) = (psi_(1,1) (x),psi_(1,0) (x),psi_(1,-1) (x))$.

$
  & hat(Gamma)^0 e^(theta) = (cosh theta - sinh theta)e^(theta) = 1 \
  & hat(Gamma)^0 e^(0 dot theta) = cos theta = 1/2(e^(theta) + e^(-theta)) \
  & hat(Gamma)^0 e^(-theta) = (cosh theta + sinh theta) e^(-theta) = 1 \
$

$
  hat(Gamma)^0 vec(e^(theta), 1, e^(-theta)) = vec(1, 1/2 (e^(theta) + e^(-theta)), 1) \
  (hat(Gamma)^0) = mat(0, 1, 0; 1/2, 0, 1/2; 0, 1, 0)
$

$
  & hat(Gamma)^1 e^(theta) = (sinh theta - cosh theta) e^(theta) = -1 \
  & hat(Gamma)^1 e^(0 dot theta) = sinh theta = 1/2(e^(theta) - e^(-theta)) \
  & hat(Gamma)^1 e^(-theta) = (sinh theta + cosh theta) e^(-theta) = 1 \
$

$
  hat(Gamma)^1 vec(e^(theta), 1, e^(-theta)) = vec(-1, 1/2 (e^(theta) - e^(-theta)), 1) \
  (hat(Gamma)^1) = mat(0, -1, 0; 1/2, 0, -1/2; 0, 1, 0)
$

$
  & hat(Gamma)^2 e^(theta) = - i e^(theta) \
  & hat(Gamma)^2 0 = 0 \
  & hat(Gamma)^2 e^(-theta) = i e^(theta) \
$

$
  hat(Gamma)^2 vec(e^(theta), 1, e^(-theta)) = vec(-i e^(theta), 0, i e^(theta)) \
  (hat(Gamma)^2) = -i mat(1, 0, 0; 0, 0, 0; 0, 0, -1)
$

Investigate the matrix, one can summarize by basis transformation $A_0 = psi_(1,-1) - psi_(1,1)$, $A_1 = psi_(1,-1) + psi_(1,1)$.

$
  & 1/2 (p_0 A_1 - p_1 A_0) = m psi_(1,0) \
  & p_0 psi_(1,0) - p_1 psi_(1,0) = m psi_(1,1) \
  & p_0 psi_(1,0) + p_1 psi_(1,0) = m psi_(1,-1) \
$

By variable transformation simplifying above equations:

$
  A_1 := 2 A_1, A_0 := 2 A_0, psi_(1,0) := i F_(1 0) = -i F_(01) \
$

$
  p_0 A_1 - p_1 A_0 & = - i m F_(0 1) \
      i p_0 F_(1 0) & = m A_1 \
      i p_1 F_(0 1) & = m A_0 \
$

$
  partial_mu A_nu - partial_nu A_mu = m F_(mu nu), quad partial^nu F_(mu nu) = m A_mu
$

One allows to apply massless case.

$
  hat(p)_mu hat(Gamma)^mu f = m s_i f, quad s_i = s, s-1,dots,-s
$

$
  p^2 = m^2 s_i^2 = m_i, quad m_i = m abs(s_i)
$

We see that if $s=1/2$, there's only one possible mass spectrum; if $s=1$, by $partial^nu F_(mu nu) = 0$, and by gauge symmetry $A_mu -> A_mu + partial_mu alpha$, the two constraints restrict the field $F_(mu nu) = "const"$. Therefore the only choice is mass one and massless one have no propagation which is unphysical. So $s= 1/2,1$ is reasonable with only *single* mass spectrum. The condition breaks when $s > 1$ that describles many particles with *different masses*, in which $hat(p)^2 (-) = m^2 (-)$ is needed to project out the one physical with mass $m$ and spin $s$.

== Dimensions 1+2

$
  I s o (d=2,1) = T(3) times.r S O (2,1)
$

It's reasonable to use Hodge dual. Any anti-symmetric tensor $A^(mu nu) = - A^(nu mu)$ has 3-components, same as vector. Then we can define its _dual_:

$
  & A^rho := 1/2 epsilon^(rho mu nu) A_(mu nu) \
  & A_(mu nu) = epsilon_(rho mu nu) A^(rho) \
$

Where $1/2$ is the factor due to $epsilon^(rho mu nu) epsilon_(sigma mu nu) = -2 tensor(delta, rho, -sigma)$.

$
  epsilon^(mu_1 dots mu_d) epsilon_(nu_1 dots nu_d) = (-1)^eta det (tensor(delta, mu_i, -nu_j)), quad eta "is metric signature" \
  epsilon^(alpha_1 dots alpha_k mu_(k+1) dots mu_d) epsilon_(beta_1 dots beta_k mu_(k+1) dots mu_d) = (-1)^(eta) (d-k)! tensor(delta, [alpha_1 dots, alpha_k], - beta_1 dots beta_k)
$

Where we have $(d-k)!$ contraction factor contribution.

$
  J^rho = 1/2 epsilon^(rho mu nu) J_(mu nu) = 1/2 epsilon^(rho mu nu)(L_(mu nu) + S_(mu nu)) := L^rho + S^rho
$

$
  [p^sigma, J^(rho)] = 1/2 epsilon^(mu nu rho) [p^sigma, J_(mu nu)] = i/2 epsilon^(mu nu rho) (tensor(eta, sigma, -mu) p_nu - tensor(eta, sigma, -nu) p_mu) = -i epsilon^(mu sigma rho) p_mu
$

$
  epsilon^(alpha mu nu) tensor(epsilon, -beta rho mu) = tensor(delta, alpha, -beta) tensor(delta, nu, -rho) - tensor(delta, alpha, -rho) tensor(delta, nu, -beta)
$

$
  epsilon^(alpha mu nu) epsilon^(beta rho sigma) eta_(mu rho) J_(nu sigma) = epsilon^(alpha mu nu) tensor(epsilon, beta, -mu, sigma) J_(nu sigma) = - J^(beta alpha) = J^(alpha beta)
$

Which is duality indication, because it's only a indices transposition.

$
  [J^alpha, J^beta] = 1/4 epsilon^(alpha mu nu) epsilon^(beta rho sigma) [J_(mu nu), J_(rho sigma)] = - i epsilon^(alpha beta gamma) J_gamma
$

$
  [hat(p)_mu, hat(p)_nu] = 0, quad [hat(p)_mu, hat(J)_nu] = - i epsilon_(mu nu eta) hat(p)^eta, quad [J^mu, J^nu] = - i epsilon^(mu nu eta) J_eta
$

=== $S U (1,1)$ and $S U (2)$

In $S O(3)$, the double cover $S U(2)$ restrict its coordinates:

$
  mat(delta, -beta; -gamma, alpha) = U^(-1) = U^(dagger) = mat(alpha^*, gamma^*; beta^*, delta^*) => delta = alpha^*, beta = -gamma^* \
  abs(alpha)^2 + abs(beta)^2 = 1
$

$
  S U (2) in.rev Z = mat(z_1, tilde(z)_1; z_2, tilde(z)_2), quad z_1 =tilde(z)^*_2, z_2 = -tilde(z)^*_1
$

$
  U(epsilon) = I - i epsilon T + O(epsilon^2)
$

$
  T = i lr(dv(U(epsilon), epsilon)bar)_(epsilon = 0)
$

$
  U^dagger (epsilon) U (epsilon) & = I \
    I + i epsilon (T^dagger - T) & = I \
                        T^dagger & = T
$

$
      det (U(epsilon)) & = 1 \
  1 - i epsilon tr (T) & = 1 \
                 tr(T) & = 0
$

$
  T = mat(alpha, beta; beta^*, -alpha), quad alpha in bb(R), beta in bb(C)
$

We recover $sigma_a$ the _Pauli Matrix_. $T$ can be decomposed as $T = sum_a T_a = sum_a sigma_a$:

$
  T_a = sigma_a, quad sigma_0 = mat(0, 1; 1, 0), thick sigma_1 = mat(0, -i; i, 0), thick sigma_2 = mat(1, 0; 0, -1)
$

There exist a anti-symmetric invariant tensor acts as metric.

$
  B (U z, U w) = B (z,w) => (U z)^alpha B_(alpha beta) (U w)^beta = z^mu B_(mu nu) w^nu => U^T B U
$

$
     U^T (epsilon) B U(epsilon) & = I \
  (sigma_mu)^T B + B (sigma_mu) & = I
$

$
                                            sigma_1^T B + B sigma_1 & = 0 \
  mat(0, 1; 1, 0) mat(a, b; c, d) + mat(a, b; c, d) mat(0, 1; 1, 0) & = 0 \
                                                  => c = -b, quad a & = -d
$

$
                                              sigma_3^T B + B sigma_3 & = 0 \
  mat(1, 0; 0, -1) mat(a, b; c, d) + mat(a, b; c, d) mat(1, 0; 0, -1) & = 0 \
                                                     => a = 0, quad d & = 0
$

A normalized metric is:

$
  B = mat(0, 1; -1, 0)
$

The _Euler-angle_ decomposition of matrix follows by $z y z$ coordinates transformation:

$
  U (psi,theta,phi.alt) = e^(-i psi/2 sigma_3) e^(-i theta/2 sigma_2) e^(-i phi.alt/2 sigma_3)
$

$
  e^(-i phi.alt/2 sigma_3) = exp(- i phi.alt/2 mat(1, 0; 0, -1)) = mat(e^(- i phi.alt/2), 0; 0, e^(i phi.alt/2)) \
$

$
  e^(-i theta/2 sigma_2) = exp(- i theta/2 mat(0, -i; i, 0)) = mat(cos theta/2, -sin theta/2; sin theta/2, cos theta/2)
$

$
  e^(-i psi/2 sigma_3) = mat(e^(-i psi/2), 0; 0, e^(i psi/2))
$

In $S O (2,1)$, the double cover $S U (1,1)$ restrict its coordinates:

$
  mat(delta, -beta; -gamma, alpha) mat(-1, 0; 0, 1) = U^(-1) eta = eta U^(dagger) = mat(-1, 0; 0, 1) mat(alpha^*, gamma^*; beta^*, delta^*) => delta = alpha^*, beta = gamma^* \
  abs(alpha)^2 - abs(beta)^2 = 1
$

$
  S U (1,1) in.rev Z = mat(z_1, tilde(z)_1; z_2, tilde(z)_2), quad z_1 =tilde(z)^*_2, z_2 = tilde(z)^*_1
$


$
  U(epsilon) = I - i epsilon K + O(epsilon^2)
$

$
  U^dagger (epsilon) eta U (epsilon) & = eta \
                        K^dagger eta & = eta K \
                            K^dagger & = eta K eta^(-1) = eta K eta \
$

$
       det(U(epsilon)) & = 1 \
  1 = i epsilon tr (K) & = 1 \
                 tr(K) & = 0 \
$

By inspection of $eta$, the minus signature.

$
  K^dagger eta = mat(-1, 0; 0, 1) mat(alpha^*, gamma^*; beta^*, -alpha^*) = mat(alpha, beta; gamma, -alpha) mat(-1, 0; 0, 1) = K eta
$

$
  K = mat(alpha, beta; -beta^*, -alpha), quad alpha in bb(R), beta in bb(C)
$

$K = sum_a k_a$ as:

$
  k_0 = sigma_3 = mat(1, 0; 0, -1), quad k_1 = i sigma_1 = mat(0, i; i, 0), quad k_2 = i sigma_2 = mat(0, -1; 1, 0)
$

The metric is same, as $k_mu$ is only different in coefficients

$
  B = mat(0, 1; -1, 0)
$

Where the _Euler-angle_ decomposition by $z y z$ coordinates transformation:

$
  U(psi,theta,phi.alt) = e^(-i psi/2 k_0) e^(-i theta k_1) e^(-i phi.alt k_0)
$

We only show the different part:

$
  e^(-i theta/2 k_1) = e^(theta/2 sigma_1) = exp(theta/2 mat(0, 1; 1, 0)) = mat(cosh theta/2, sinh theta/2; sinh theta/2, cosh theta/2)
$

Which is unbounded.

The representation:

$
  U dot f(v) = f(U^(-1) v), quad v = vec(v_1, v_2)
$

$
  U^(-1) = mat(u^*_1, - u_2; -u^*_2, u_1), quad abs(u_1)^2 - abs(u_2)^2 = 1
$

Now we use $(u_mu)^i_j$ represent the generated elements of $U$, which corresponds to $k_a$ or $sigma_a$.

$
  delta f = delta v^i pdv(f, v_i) = sum_mu (u_mu)^i_j v^j pdv(f, v_i)
$

The ladder operator is various due to basis selection, generally, we choose below basis no matter our previous basis is:

$
  u^0 = 1/2 mat(1, 0; 0, -1), quad u^+ = mat(0, 1; 0, 0), quad u^- = mat(0, 0; 1, 0)
$

$
  hat(J)^0 = - 1/2 (v_1 pdv(, v_1) - v_2 pdv(, v_2)), quad hat(J)_+ = v_2 pdv(, v_1), quad hat(J)_- = v_1 pdv(, v_2)
$

$
  [hat(J)^mu, hat(J)^nu] = - i epsilon^(mu nu eta) hat(J)_eta, quad [hat(J)_+, hat(J)_-] = 2 hat(J)^0, quad [hat(J)^0,hat(J)_(plus.minus)] = plus.minus hat(J)_(plus.minus)
$

$
  hat(J)^2 = hat(J)_mu hat(J)^mu = hat(J)_0^2 + 1/2 (hat(J)_+ hat(J)_- + hat(J)_- hat(J)_+) = hat(J)^0 (hat(J)^0 +1) + hat(J)_- hat(J)_+
$

We see that for any representation $hat(J)^0 ket(n) = n ket(n)$, then for the highest weight, one deduce that $hat(J)^2 ket(n) = n(n+1) ket(n)$, which is commutative to any other operator. The whole system is decomposed by its highest weight, which called $j$, that $hat(J)^2 = j (j+1)$ if $j$ is specified.

The general eigenvector of $v pdv(, v)$ is $v^n$ for arbitrary $n$. Then let's take the form $f(n_1,n_2)(v) = v_1^(n_1) v_2^(n_2)$:

$
  hat(J)^0 f(n_1,n_2) = m = (n_2 - n_1)/2
$

$
  hat(J)^2 f(n_1,n_2) = j(j+1), quad j & = (n_2 - n_1)/2 (n_2 - n_1 + 2)/2 + (n_2 + 1)n_1 \
                                       & = (n_2 + n_1)/2 (n_2 + n_1 + 2)/2, quad j = (n_1 + n_2)/2
$

Therefore by variable transformation:

$
  n_1 = j - m, quad n_2 = j + m, quad f(n_1,n_2) := f(j,m)
$

===

Now:

$
  S U (1,1) in.rev Z = mat(z_1, tilde(z)_1; z_2, tilde(z)_2) = mat(z_1, z^*_2; z_2, z^*_1) = (bold(z),tb(z)), quad z_1 =tilde(z)^*_2, z_2 = tilde(z)^*_1
$

Where the minus sign comes from the contraction with metric $eta$.

$
  hat(S)^mu = 1/2 (- bold(z) k^mu partial_(bold(z)) + tb(z) k^mu partial_(tb(z))) quad bold(z) = vec(z_1, z_2)^T, partial_bold(z) = vec(pdv(, z_1), pdv(, z_2)), k^mu = (k_0,k_1,k_2)
$

$
  hat(p)^2 f(bold(x),vf(z)) = m^2 f(bold(x),vf(z)) \
  hat(p)_mu hat(S)^mu f(bold(x),vf(z)) = kappa f(bold(x),vf(z)) \
  hat(S)_mu hat(S)^Mu f(bold(x),vf(z)) = S(S+1) f(x,vf(z))
$

$
  & (hat(p)^2 - m^2) psi(bold(x)) = 0 \
  & (hat(p)_mu hat(S)^mu - m_s m) psi(bold(x)) = 0
$

$
  f(bold(x),vf(z)) = sum_i phi_i (vf(z)) psi^i (bold(x)) = phi (vf(z)) psi(bold(x))
$

$
  hat(S)^mu f(bold(x),vf(z)) & = sum_i (hat(S)^mu)_i^j phi_j (vf(z)) psi^i (bold(x)) \
                             & = sum_j [(hat(S)^mu)_i^j psi^i (bold(x))] phi_j (vf(z))
$

It's shown that $phi (vf(z))$ can be represented by $phi(bold(z))$ only because $bold(z)$ and $tb(z)$ is similar.

$
  hat(S)^mu = -1/2 bold(z) k^mu partial_bold(z), quad bold(z) = vec(z_1, z_2)^T, thick partial_bold(z) = vec(pdv(, z_1), pdv(, z_2))
$

$
  phi(S, m_s)(bold(z)) = N(S,m_s) z_1^(S-m_s) z_2^(S+m_s)
$

$
  phi(S, n)(bold(z)) = sum_(n=0)^(2 S) N(S,n) z_1^(2 S - n) z_2^n, quad S + m_s = n, thick S-m_s = 2 S - n
$

Where expands in $2 S + 1$ components equipped with $psi_(n - S)(x) = psi_(m_s) (x)$.

Consider $S = 1\/2$, then $m_s in {1\/2,-1\/2}$.

$
  f(bold(x),bold(z)) = psi_(1/2) (x) z_2 - psi_(-1/2) (x) z_1, quad hat(S)^2 f = 3/4 f
$

Which the action of $S^mu$ is the multiplication of matrix $k^mu$.

$
  hat(S) psi(bold(x)) = 1/2 k^mu psi(x)
$

$
  [k^mu, k^nu]_+ = 2 eta^(mu nu), quad [k^mu, k^nu] = - 2 i epsilon^(mu nu eta) k_eta
$

Is the $2 times 2$-matrices in $2+1$ dimensions.

Consider $S = 1$, then $m_s in {1,0,-1}$.

$
  f(bold(x),bold(z)) = psi_1 (x) z_2^2 + psi_0 (x) z_1 z_2 + psi_(-1) (x) z_1^2
$

Where $psi (x) = (psi_1 (x), psi_0 (x), psi_(-1) (x))^T$.

Calculate by apply $hat(S)^mu = -1/2 bold(z) k^mu partial_(bold(z))$ in basis $(z_1^2, z_1 z_2, z_2^2)$:

$
  hat(S)^0 = -mat(1, 0, 0; 0, 0, 0; 0, 0, -1), quad hat(S)^1 = -i mat(0, 1, 0; 1/2, 0, 1/2; 0, 1, 0), quad hat(S)^2 = -1 mat(0, -1, 0; 1/2, 0, -1/2; 0, 1, 0)
$

$
  & p_0 psi_(1,-1) + p_1 psi_(1,0) - p_2 psi_(1,0) = m_s m psi_(1,-1) \
  & 1/2 (p_1 (i psi_(1,-1) + i psi_(1,1)) + p_2 (psi_(1,-1) - psi_(1,1))) = m_s m psi_(1,0) \
  & -p_0 psi_(1,1) + p_1 psi_(1,0) + p_2 psi_(1,0) = m_s m psi_(1,1) \
$

$
  cal(F)_1 := i (psi_(1,-1) + psi_(1,1)), quad cal(F)_2 := psi_(1,-1) - psi_(1,1), quad cal(F)_0 = 2 psi_(1,0)
$

Compare or transform the variables, we found:

$
  epsilon^(mu nu eta) partial_nu cal(F)_eta - m_s m cal(F)^mu = 0
$

A transversality condition follows by apply $partial_mu$ on the equation above:

$
  partial_mu cal(F)^mu = 0
$

$
  cal(F)^mu = epsilon^(mu nu eta) partial_nu A_eta = 1/2 epsilon^(mu nu eta) F_eta, quad epsilon^(mu nu eta) cal(F)_eta = F^(mu nu)
$

$
               partial_nu F^(mu nu) - 1/2 m_s m epsilon^(mu alpha beta) F_(alpha beta) & = 0 \
               partial_nu F^(nu mu) + 1/2 m_s m epsilon^(mu alpha beta) F_(alpha beta) & = 0 \
  (partial_nu F^(nu mu) + 1/2 m_s m epsilon^(mu alpha beta) F_(alpha beta)) delta A_mu & = 0 \
$

$
  partial_nu F^(nu mu) delta A_mu = - F^(nu mu) partial_nu delta A_mu = -1/2 F^(mu nu) (partial_mu delta A_nu - partial_nu delta A_mu) = 1/2 F^(mu nu) delta F_(mu nu)
$

It's the Lagrange action in topologically massive gauge theory with the _Chern-Simons_ term.

$
  cal(L)_(C S) = -1/4 F^(mu nu) F_(mu nu) + 1/2 m_s m epsilon^(mu alpha beta) A_mu F_(alpha beta)
$

Otherwise transform the columns by metric.

$
  B vec(z_1, z_2) = mat(0, 1; -1, 0) vec(z_1, z_2) = vec(z_2, -z_1)
$

$
  overline(f)(bold(x),vf(z)) = B dot f^dagger (bold(x),vf(z)) &= sum_n phi^dagger (S,n) (B vf(z)) psi^dagger_n (bold(x)) \
  &= sum_n overline(phi)(S,n) (vf(z)) psi^dagger_n (bold(x)) \
  &= sum_n' phi(S, n') (vf(z)) overline(psi)_n' (bold(x)) \
  &= sum_n' phi(S, n') (vf(z)) (psi^dagger_n (Gamma)^n_n') (bold(x))
$

$
  overline(phi)(S,n)(bold(z)) = sum_(n=0)^(2 S) N(S,n) (-z_1)^(n) z_2^(2S-n), quad S + m_s = n, thick S-m_s = 2 S - n
$

If we fix $hat(S)$ as matrix act on $psi(x)$ in decomposition

$
  psi^dagger (bold(x)) (hat(S)^(dagger mu) arrow.l(hat(p)) - m_s m) = 0
$

$
  overline(psi)' (bold(x)) = overline(psi) (dot g), quad overline(psi) (bold(x)) = psi^dagger (bold(x)) Gamma
$

$
  overline(psi)'(bold(x)) psi'(bold(x)) & = (psi^dagger (bold(x)) Gamma) dot g) (g dot psi(bold(x))) \
                          Gamma (dot g) & = (dot g)^dagger Gamma \
$

$
  S^(dagger mu) & = Gamma S^mu Gamma
$

$
  psi^dagger (bold(x)) (hat(S)^(dagger mu) arrow.l(hat(p))_mu + m_s m) & = 0 \
                              overline(psi) (bold(x)) (hat(S) + m_s m) & = 0 \
$

$
  j^mu = overline(psi) hat(S)^mu psi, quad partial_mu j^mu = 0
$

$
  (hat(p)_mu hat(S)^mu + m_s m) (hat(p)_nu hat(S)^nu - m_s m) psi(bold(x)) = (1/2 hat(p)_mu hat(p)_nu [hat(S)^mu,hat(S)^nu]_+ - m_s^2 m^2) psi(bold(x)) = 0
$

In representation $S=1\/2$, we have $m_s = plus.minus 1\/2$, $S^mu = k^mu$ and $[hat(S)^mu, hat(S)^nu]_+ = eta^(mu nu)\/2$, the equation reduce into _Klein-Gordon_ equation.

== Dimension 1+3

=== $S L (2)$

$
  U = mat(a, b; c, d) in S L(2, bb(C)), quad det(U) = a d - b c = 1,a,b,d in bb(C)
$

$
  U(epsilon) = I - i epsilon X + O(epsilon^2)
$

$
      det(U(epsilon)) & = 1 \
  1 - i epsilon "Tr"(X) & = 1 \
                "Tr"(X) & = 0 => X = mat(a, b; c, -a) quad a,b,c in bb(C) \
$

It's shown that one can decompose the generator into:

$
  beta = (b + c)/2 + i (b - c)/(2 i), quad beta^* = (b+c)/2 - i(b - c)/(2 i)
$

We found that it's natural that:

$
  X = mat(a, beta; beta^*, -a), quad a,beta in bb(C)
$

Is the *complex* linear combination of _Pauli Matrix_.

$
  X = bold(c) dot bold(sigma), quad bold(c) = (c_1,c_2,c_3) in bb(C)
$

$
  X = sum_(k=1)^3 (i/2 theta^k sigma_k + 1/2 eta^k sigma_k)
$

Where $theta_k$ is the rotation and $eta_k$ is the boost, corresponding to generator: $hat(S)_(mu nu) => hat(S)_k = 1/2 epsilon_(i j k) hat(S)^(i j), hat(B)_k = hat(S)_(0 k)$ identified with rotation and boost. It's the decomposition isomorphism that $lie("sl")(2;bb(C)) tilde.equiv lie("su")(2) plus.o lie("su")(2)$ as real vector spaces.

We immediately see that $[i sigma_i, sigma_j] = - epsilon_(i j k) sigma^k$, therefore the commutation between two basis will fall into the boost one.

$
  X = x^mu sigma_mu, quad X' = U(epsilon) X U(epsilon)^dagger
$

$
  x'^rho sigma_rho &= (I + i/2 omega_(mu nu) Sigma^(mu nu)) (x^lambda sigma_lambda) (I - i/2 omega_(mu nu) Sigma^(mu nu)) \
  omega_(rho lambda) sigma^rho &= i/2 omega_(mu nu) (Sigma^(mu nu) sigma_lambda - sigma_lambda Sigma^(dagger mu nu)) quad x'^rho = x^rho + omega^(rho lambda) x_lambda \
$

$
  omega_(rho lambda) = omega_(mu nu) (tensor(delta, mu, -rho) tensor(eta, nu, -lambda) - tensor(delta, nu, -rho) tensor(eta, mu, -lambda))
$

Follow $eta_(mu nu)$ Lorentz metric such that $overline(sigma) = (sigma_0,-sigma_i)$#footnote[one may suggest that $sigma^lambda eta_(lambda rho) = sigma_rho$ as transformation, but in such case, $sigma^lambda sigma_rho + sigma^rho sigma_lambda$ is ill defined in tensor contraction, so does $Sigma^(mu nu)$]:

$
  sigma_lambda overline(sigma)_(kappa) + sigma_(kappa) overline(sigma)_lambda = 2 tensor(eta, -kappa lambda) I
$

$
  -i (tensor(delta, mu, -rho) tensor(eta, nu, -lambda) - tensor(delta, nu, -rho) tensor(eta, mu, -lambda)) sigma^rho overline(sigma)^lambda &= Sigma^(mu nu) sigma_lambda overline(sigma)^lambda - sigma_lambda Sigma^(dagger mu nu) overline(sigma)^lambda \
  -i (sigma^mu overline(sigma)^nu - sigma^nu overline(sigma)^mu) &= 2 Sigma^(mu nu) (sigma_lambda overline(sigma)^lambda) \
  Sigma^(mu nu) &= -i/4 (sigma^mu overline(sigma)^nu - sigma^nu overline(sigma)^mu)
$

$
  -i overline(sigma)^lambda (tensor(delta, mu, -rho) tensor(eta, nu, -lambda) - tensor(delta, nu, -rho) tensor(eta, mu, -lambda)) sigma^rho &= overline(sigma)^lambda Sigma^(mu nu) sigma_lambda - overline(sigma)^lambda sigma_lambda Sigma^(dagger mu nu) \
  i (overline(sigma)^mu sigma^nu - overline(sigma)^nu sigma^mu) &= 2 Sigma^(mu nu) ( overline(sigma)^lambda sigma_lambda) \
  Sigma^(mu nu) &= i/4 (overline(sigma)^mu sigma^nu - overline(sigma)^nu sigma^mu) \
$

Suppose right hand equal to $-2 Sigma^(dagger mu nu) (overline(sigma)^lambda sigma_lambda)$:

$
  Sigma^(dagger mu nu) = -i/4 (overline(sigma)^mu sigma^nu - overline(sigma)^nu sigma^mu)
$

$
  sigma^(mu nu) = overline(sigma)^mu sigma^nu - overline(sigma)^nu sigma^mu, quad overline(sigma)^(mu nu) = overline(sigma)^mu sigma^nu - overline(sigma)^nu sigma^mu
$

Better one is from:

$
  1/2 (theta^k i sigma_k + eta^k sigma_k) &= 1/2 (omega_(i j) epsilon^(i j k) i sigma_k + omega^(0 k) sigma_k) \
  &= 1/4 (omega^(i j) (sigma_i overline(sigma)_j - sigma_j overline(sigma)_i) + omega^(0 k) (sigma_k overline(sigma)_0 - sigma_0 overline(sigma)_k)) \
  &= 1/4 omega^(mu nu) (sigma_mu overline(sigma)_nu - sigma_nu overline(sigma)_mu) \
$

$
  (sigma_mu overline(sigma)_nu - sigma_nu overline(sigma)_mu) sigma_rho &= sigma_mu eta_(nu rho) - sigma_mu (overline(sigma_rho) sigma_nu) + (mu <-> nu) \
  &= sigma_mu eta_(nu rho) + sigma_nu eta_(mu rho)
$

From general view, $hat(Sigma)^(mu nu)$ is a generated element of Clifford algebra as $Sigma^(mu nu) = gamma^mu and gamma^nu$. By tensor homomorphism identification, one has:

$
  hat(Sigma)^(mu nu) = -i/4 [gamma^mu,gamma^nu], quad [gamma^mu, gamma^nu]_+ = 2 eta^(mu nu)
$

When we acts on the conjugation $bold(z)^*$ by $Sigma^(dagger mu nu)$, $(bold(z),bold(z)^*)$ can be expressed as:

$
  cal(S)^(mu nu) = mat(sigma^(mu nu), 0; 0, overline(sigma)^(mu nu)), quad cal(S)^(mu nu) = [gamma^mu, gamma^nu]
$

Immediately, in such basis, the $gamma^mu$ is clear that must be off-diagonal due to $cal(S)^(mu nu)$ is a commutator:

$
  gamma^mu = mat(0, sigma^mu; overline(sigma)^mu, 0), quad gamma^mu gamma^nu = mat(sigma^mu overline(sigma)^nu, 0; 0, overline(sigma)^mu sigma^nu)
$

Is what we expected. We can apply the same routine for $(tb(z),tb(z)^*)$ yielding the same results.

The Clifford algebra suggests that such tensor construction can be achieved gradually:

$
  gamma^5 = gamma_0 gamma_1 gamma_2 gamma_3, quad (gamma^5)^2 = (-1)^(3 + 2 + 1) (-1)^3 = -1
$

Commonly, one could choose $gamma^5 := i gamma_0 gamma_1 gamma_2 gamma_3$ to make $(gamma^5)^2 = 1$. It's shown that such tensor behaves like a volume of space, constructed by anti-commutation relation, then the Hodge dual can reduced to:

$
  underline(gamma)^mu = i gamma^(mu) gamma^5
$

$
  [gamma^5, gamma^mu]_+ = 0, quad [gamma^5, cal(S)^(mu nu)] = 0
$

It indicates that $gamma^5$ should be a diagonal matrix:

$
  mat(lambda_1, 0; 0, lambda_2) mat(0, sigma^mu; overline(sigma)^mu, 0) + mat(0, sigma^mu; overline(sigma)^mu, 0) mat(lambda_1, 0; 0, lambda_2) = 0 => lambda_1 = -lambda_2
$

By $(gamma^5)^2 = 1$:

$
  gamma^5 = mat(1, 0; 0, -1)
$

Suppose $(u)^i_j$ is the generator:

$
  delta f = (u)^i_j z^j pdv(f, z_i)
$

$
  &hat(S)_k = 1/2 (bold(z) sigma_k partial_bold(z) - z^* sigma_k^* partial_(bold(z)^*)) + (bold(z) <-> tb(z)) \
  &hat(B)_k = i/2 (bold(z) sigma_k partial_bold(z) + z^* sigma_k^* partial_(bold(z)^*)) + (bold(z) <-> tb(z)), quad bold(z) = vec(z_1, z_2), partial_bold(z) = vec(pdv(, z_1), pdv(, z_2))^T \
$

$
  [hat(S)_i, hat(B)_j] = i epsilon_(i j k) hat(B)^k
$

Is same as before.

Generally, a function must coupled with $(z,z^*)$ together in transformation due to $U^dagger != U^(-1)$, where the choices $(bold(z), tb(z)^*)$ represents _Driac $z$-spinor_ or $(bold(z), bold(z)^*)$ represents _Majorana $z$-spinor_. Which both coordinates behave same.

$
  &hat(S)^(mu nu) = 1/2 (bold(z) sigma^(mu nu) partial_(bold(z)) + bold(z)^* sigma^(mu nu) partial_(bold(z)^*)) + (bold(z) <-> tb(z)) \
  &hat(Gamma)^mu = 1/2 (bold(z)^* overline(sigma)^mu partial_bold(z) + bold(z) sigma^mu partial_(bold(z)^*)) + (bold(z) <-> tb(z))
$

Currently, we omit the differentiation of two columns $(bold(z),tb(z))$ and focus on conjugation only. In decomposition, one should decompose into algebraic structure isomorphic to 2-summand of $lie("su")(2)$.

$
  hat(M)_k = 1/2 (hat(S)_k - i hat(B)_k) = bold(z) sigma_k partial_(bold(z)), quad hat(M)^*_k = -1/2 (hat(S)_k + i hat(B)_k) = bold(z)^* sigma^*_k partial_(bold(z)^*) \
$

$
  hat(M)^+ = z_1 pdv(, z_2), quad hat(M)^- = z^2 pdv(, z_1) \
  hat(M)^(* +) = z^*_1 pdv(, z^*_2), quad hat(M)^(* -) = z^*_2 pdv(, z^*_1) \
$

Such that 2-summand is commutative together. Any previous investigation can be applied:

$
  hat(M)^2 = j_1 (j_1 + 1), quad hat(M)^(* 2) = j_2 (j_2 + 1) \
$

$
  hat(M)^2 + hat(M)^(* 2) & = 1/2 (hat(S)^2 - hat(B)^2) \
$

Though $[hat(S)^i,hat(B)^j] = i epsilon^(i j k) hat(B)_k$, it shown that $[hat(S)^i, hat(B)^i] = 0 = hat(S)^i hat(B)_i - hat(B)^i hat(S)_i$ in permutation.

$
  hat(M)^2 - hat(M)^(* 2) = i hat(S)^i hat(B)_i \
$

In finite-dimensional representation, we follow the same procedure that the basis is a linear combination of:

$
  (z_1)^a (z_2)^b (z^*_1)^c (z^*_2)^d, quad a,b,c,d in bb(N)
$

It's obvious that:

$
  j_1 = (a + b)/2, quad j_2 = (c+d)/2, quad m_1 = (a-b)/2, quad m_2 = (a - b)/2
$

$
  f(j_1,m_1;j_2,m_2)(bold(x),bold(z),bold(z)^*) = sum_(j_1 + j_2 = S) sum_(m_1,m_2) psi (j_1,m_1;j_2,m_2)(bold(x)) phi (j_1,m_1;j_2,m_2)(bold(z),bold(z)^*)
$

$
  phi (j_1,m_1;j_2;m_2) (bold(z),bold(z)^*) = N(j_1,m_1;j_2,m_2)^(1/2) z_1^(j_1 + m_1) z_2^(j_1 - m_1) z^(* j_2 + m_2) z^(* j_2 - m_2)
$

$
  & hat(p)^2 f(bold(x),vf(z)) = m^2 f(bold(x),vf(z)) \
  & hat(p)_mu hat(Gamma)^mu f(bold(x),vf(z)) = kappa f(bold(x),vf(z)) \
$

In rest frame:

$
  &hat(p)_0^2 f(bold(x),vf(z)) = m^2 f(bold(x),vf(z)) \
  &hat(p)_0 hat(Gamma)^0 f(bold(x),vf(z)) = kappa f(bold(x),vf(z)), quad hat(Gamma)^0 = 1/2 (bold(z)^* sigma^0 partial_bold(z) + bold(z) sigma^0 partial_bold(z))
$

According to first equation, $p_0 = plus.minus m$. To solve the second one, we need to solve in eigenvectors where:

$
  bold(u) := bold(z) + bold(z)^*, quad bold(v) := bold(z) - bold(z)^* \
$

$
  hat(Gamma)^0 = 1/2 ((bold(u) - bold(v))/2 sigma^0 partial_(bold(u) + bold(v)) + dots) = 1/2 (bold(u) partial_bold(u) - bold(v) partial_(bold(v)))
$

The eigenvector in *homogeneous* polynomial: $bold(u)^(n_1) bold(v)^(n_2)$, the eigenvalue is $(n_1 - n_2)\/2 = tilde(S)$. Indeed, ${bold(u), bold(v)}$ forms a space where $T_(n_1) times.o T_(n_2) = plus.big.o_(n = abs(n_1 - n_2))^(n_1 + n_2) T_(n)$ in routine of angular momentum. If we choose $n_1\/2 = S, abs(tilde(S)) = m_s = S$ for all possible value $s$. Thus for unique mass $m$ and spin $m_s$, there are $2 m_s + 1$ independent positive-frequency solutions and $2 m_s + 1$ negative-frequency solutions.

$
  f(s,m)(bold(x),vf(z)) = sum_(m = -s)^s N(s,m) e^(i m x^0) u_1^(s+m) u_2^(s-m) + N'(s,m) e^(-i m x^0) v_1^(s+m) v_2^(s-m)
$

$
  hat(S)_3 f(bold(x),vf(z)) = (m_1 + m_2) f(bold(x),vf(z)) = m f(bold(x),vf(z)), quad hat(S)_3 = 1/2 (bold(z) sigma_3 partial_bold(z) - bold(z)^* sigma_3^* partial_(bold(z)^*))
$

Suppose the spin $s$ is fix, one can decompose each $(j_1,j_2)$ by its _Chirality_ $lambda$:

$
  f(s)(bold(x),vf(z)) = sum_(lambda = -s)^s f(s;lambda) (bold(x),vf(z)), quad s = j_1 + j_2, thick lambda = j_1 - j_2
$

No
w we represent as basis $f(j_1,j_2)$:

$
  hat(p)^mu hat(Gamma)_mu f = m s f, quad hat(Gamma)^mu = 1/2 (bold(z)^* overline(sigma)^mu partial_bold(z) + bold(z) sigma^mu partial_(bold(z)^*))
$

Identify:

$
  R^mu = 1/2 bold(z)^* overline(sigma)^mu partial_bold(z), quad L^mu = 1/2 bold(z) sigma^mu partial_(bold(z)^*)
$

Where $L^mu f (j_1,j_2) -> f(j_1 + 1/2, j_2 - 1/2), R^mu f(j_1,j_2) -> f(j_1 - 1/2, j_2 + 1/2)$ in basis transformation.

$
  hat(p)^mu mat(0, L^mu, 0, dots, 0; R^mu, 0, L^mu, dots, 0; 0, R^mu, 0, dots.down, dots.v; dots.v, dots.v, dots.down, 0, L^mu; 0, 0, dots, R^mu, 0) vec(f(s,0), f(s-1/2,1/2), f(s-1,1), dots.v, f(0,s)) = m s vec(f(s,0), f(s-1/2,1/2), f(s-1,1), dots.v, f(0,s))
$

Is the chirality matrix. A lucky news is that the first and last row have only one neighbor, then one can substitute the first and last into second into third and so on, until every components are expressed in terms of one central field. A example of $s=1$, the chain has three components: $f(1,0), f(1\/2,1\/2), f(0,1)$. Focus on $f(1\/2,1\/2)$ solely:

$
  & hat(bold(p)) dot hat(bold(L)) f(1/2,1/2) = m f(1,0) \
  & hat(bold(p)) dot hat(bold(R)) f(1,0) + hat(bold(p)) dot hat(bold(L)) f(0,1) = m f(1/2,1/2) \
  & hat(bold(p)) dot hat(bold(R)) f(1/2,1/2) = m f(0,1) \
$

Substitute first and third into the second row equation:

$
  (hat(bold(p)) dot hat(bold(R)) thin hat(bold(p)) dot hat(bold(L)) + hat(bold(p)) dot hat(bold(L)) thin hat(bold(p)) dot hat(bold(R))) f(1/2,1/2) &= m^2 f(1/2,1/2) \
  [hat(bold(p)) dot hat(bold(R)),thin hat(bold(p)) dot hat(bold(L))]_+ f(1/2,1/2) &= m^2 f(1/2,1/2) \
$

For higher spin, you can substitute to get order $1 + floor.l s floor.r$ wave equation.

Consider $s= j_1 + j_2 = 1\/2$:

$
  f(s=1/2)(bold(x),vf(z)) = psi^(1/2,0) bold(z) + psi^(0,1/2) bold(z^*) = psi vec(bold(z), bold(z)^*)
$

As basis $(bold(z),bold(z)^*)$. By generator $gamma$ of representation $hat(Gamma)$, we can apply directly that:

$
  (hat(p)_mu hat(Gamma)^mu - 1/2 m) f(s=1/2) & = 0 \
                (hat(p)_mu gamma^mu - m) psi & = 0
$

Is the wave equation called _Dirac equation_.

// To acquire complex conjugation corresponds to charge conjugation state, we should expand in metric:

// $
//   f^* (s=1/2) (bold(x),vf(z)) = - bold(z) psi^(1/2,0) + bold(z)^* psi^(0,1/2)
// $
//
//
$
  f(s=1) (bold(x),vf(z)) = psi^(1,0)_(alpha beta) z^alpha z^beta + psi^(1/2,1/2)_(alpha beta) z^(alpha) z^(* beta) + psi^(0,1)_(alpha beta) z^(* alpha) z^(* beta)
$

Expand our equation:

$
  &1/2 hat(p)_mu (sigma^mu)_(alpha gamma) tensor(psi^(1/2,1/2), gamma, -beta) = m psi^(1,0)_(alpha beta), quad 1/2 hat(p)_mu (overline(sigma)^mu)_(gamma alpha) tensor(psi^(1/2,1/2), gamma, -beta) = m psi^(0,1) \
  &1/2 hat(p)_mu ((sigma^mu)_(alpha gamma) tensor(psi^(0,1), gamma, -beta) + (overline(sigma)^mu)_(gamma alpha) tensor(psi^(1,0), gamma, -beta)) = m psi^(1/2,1/2)_(alpha beta)
$

To separate indices of $z^alpha$ and $z^(* alpha)$, we choose $alpha$ and $dot(alpha)$ for each.

$
  1/2 hat(p)_mu mat(0, sigma^mu,0;overline(sigma)^mu, 0,sigma^mu;0,overline(sigma)^mu,0) vec(psi^(1,0),psi^(1/2,1/2),psi^(0,1)) = m vec(psi^(1,0),psi^(1/2,1/2),psi^(0,1))
$

$
  (sigma_rho)_(alpha dot(beta)) epsilon^(alpha gamma) epsilon^(dot(beta) dot(delta)) = (overline(sigma)_rho)^(gamma dot(delta)) \
$

$
  (sigma_rho)_(alpha dot(beta)) (overline(sigma)^delta)^(alpha dot(beta)) = -2 tensor(delta, -rho, delta)
$

By swapping $(z,z^*)$.

$
  tensor(sigma^mu, -alpha dot(alpha)) tensor(overline(sigma), nu dot(alpha) beta) + tensor(sigma, nu, -alpha dot(alpha)) tensor(overline(sigma), mu dot(alpha) beta) = 2 eta^(mu nu) tensor(delta, -alpha, beta) \
  tensor(sigma^mu, -beta dot(alpha)) tensor(overline(sigma)^nu, dot(alpha) gamma) = eta^(mu nu) tensor(delta, -beta, gamma) + tensor((sigma^(mu nu)), -beta, gamma) \
$

$
  psi_alpha epsilon^(alpha dot(gamma)) = psi^(dot(gamma)) \
$

Since $psi^(1,0)_(alpha beta) = psi^(1,0)_(beta alpha)$ and $psi^(0,1)_(alpha beta) = psi^(0,1)_(beta alpha)$ due to homogeneous polynomial:

$
  "Tr"(psi^(1,0 \/ 0,1)) = epsilon^(gamma alpha) epsilon^(delta beta) psi^(1,0 \/ 0,1)_(alpha beta) psi^(1,0 \/ 0,1)_(gamma delta) = epsilon^(1 2) psi^(1,0\/0,1)_(1 2) + (1 <-> 2) = 0
$

$
  &1/2 hat(p)_mu (sigma^mu)^(dot(alpha) gamma) tensor(psi^(1/2,1/2), -gamma, dot(beta)) = m psi^(0,1 dot(alpha) dot(beta)) \
  &1/2 hat(p)_mu (overline(sigma)^mu)_(dot(gamma) alpha) tensor(psi^(1/2 1/2), -beta, dot(gamma)) = m psi^(1,0)_(alpha beta)
$

Apply $sigma_(mu nu)$ into $psi^(1,0)$ or $psi^(0,1)$:

$
  (sigma_(mu nu))_(alpha beta) (1/2 hat(p)_rho tensor((sigma^rho), alpha, -dot(gamma)) tensor(psi^(1/2,1/2), dot(gamma), beta)) &= 1/2 hat(p)_rho (tensor(eta, rho, -nu) tensor((sigma_mu), -alpha dot(gamma)) - tensor(eta, rho, -mu) tensor((sigma_nu), -alpha dot(gamma))) tensor(psi^(1/2,1/2), dot(gamma), beta) \
  &= 1/2 (hat(p)_nu (dots) + hat(p)_mu (dots)) tensor(psi^(1/2,1/2), dot(gamma), beta)
$

Indeed, apply for $hat(p)_mu (dots) psi^(1,0) = m psi^(1/2,1/2)$ too in $overline(sigma)$. Interesting, and tough that:

$
  F_(mu nu) := (sigma_(mu nu))_(alpha beta) tensor(psi^(0,1), alpha beta) + (psi^(0,1) <-> psi^(1,0), sigma<->overline(sigma)), quad A_mu := tensor((sigma_mu), -alpha dot(beta)) tensor(psi^(1/2,1/2), alpha, dot(beta)) = (overline(sigma)_mu)_(alpha dot(beta)) tensor(psi^(1/2,1/2), alpha dot(beta))
$

$
  m F_(mu nu) = partial_mu A_nu - partial_nu A_mu
$

$
  tensor(sigma^mu, alpha, - dot(alpha)) tensor(overline(sigma)^nu, dot(alpha) gamma) tensor(psi^(1,0), -gamma alpha) = (eta^(mu nu) tensor(delta, alpha, gamma) + tensor((sigma^(mu nu)), alpha, gamma))tensor(psi^(1,0), -gamma alpha) \
$

Apply for $psi^(1,0)$ and $psi^(0,1)$ in contraction, where the $"Tr"(psi^(1,0)) = 0$ and we get:

$
  m A^mu = m tensor((sigma^mu), alpha, -dot(alpha)) tensor(psi^(1/2,1/2), dot(alpha), -alpha) = partial_nu F^(mu nu)
$

$
  partial^mu (m A_mu) = partial^mu partial^nu F_(mu nu) = 0 => partial^mu A_mu = 0
$

$
  m^2 A_mu = m partial^nu F_(mu nu) = partial^nu partial_mu A_nu - partial^nu partial_nu A_mu => (hat(p)^2 + m^2) A_mu = 0 \
$

$
  A_mu = "Tr"(overline(sigma)_mu psi^(1/2,1/2)), quad F_(mu nu) = "Tr"(sigma_(mu nu) psi^(1,0) + overline(sigma)_(mu nu) psi^(0,1))
$

$
  m psi^(1,0) = 1/2 hat(p)_mu overline(sigma)^mu psi^(1/2,1/2), quad m psi^(0,1) = 1/2 hat(p)_mu sigma^mu psi^(1/2,1/2) \
  m psi^(1/2,1/2) = hat(p)_mu (overline(sigma)^mu psi^(0,1) + sigma^mu psi^(1,0)) \
$

$
                                           (hat(p)_mu R^mu) f(j_1,j_2) & = m f(j_1 -1/2,j_2 + 1/2) \
  ((2j_1) !)/((2j_2) !)(hat(p)_mu R^(mu))^(2abs(j_1 - j_2)) f(j_1,j_2) & = m^(2abs(j_1-j_2)) f(j_2,j_1)
$

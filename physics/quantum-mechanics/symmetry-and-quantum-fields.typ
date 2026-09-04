#import "../lib.typ": *
#import "@preview/physica:0.9.8": *
#import "@preview/fletcher:0.5.8" as fletcher: diagram, edge, node

#show: daily-en.with(
  title: "Review of Quantum",
)

#let lie(body) = $frak(body)$
#let vf(body) = $bold(upright(body))$

=

==

$g in G$, given a action of group on a general space $M$ equipped with function on it as $F(M)$. Thus we can apply $g$ on $M$ and lift upon $F(M)$ as well, i.e. $phi(g) dot x$ for $x in M$ and $rho(g) dot f$ for $f in F(M)$ as a $G$-equivariant map.

#figure(
  diagram(
    $x edge(f, ->) edge("d", phi(g), ->) & f(x) edge("d", rho(g), ->)\
    phi(g) dot x edge(f, ->) & rho(g) dot f(x) \/ f(phi(g) dot x)$,
  ),
  caption: "Commutative diagram of group action on space and mapped space",
)

Is commutative, i.e.

$
  rho(g) dot (rho(h) dot f) (x) = rho(h) dot f (phi(g) dot x) = f (phi(h) dot (phi(g) dot x)) = f( phi(h) compose phi(g) dot x)
$

Is a anti-homomorphism, i.e. Such representation should be only with $g$ element, thus a canonical choice is $g^(-1)$ where below is given as a reduced notation:

$
  g dot f(x) = f (g^(-1) dot x) \
$

$V = W plus.o W' -> v = w + w'$, where the projection $q(v) = w$. Define $overline(q): v -> 1/(abs(G)) sum_(g in G) rho(g) q(rho(g^(-1))v)$ which we drop $rho$ representation notation.

$
  overline(q)(w) = 1/(abs(G)) sum_(g in G) g q(g^(-1) w) = 1/(abs(G)) sum_(g in G) g (g^(-1) w) = w \
$

$
  h overline(q)(v) = 1/(abs(G)) sum_(g in G) h g q(g^(-1) h^(-1) h v) = 1/(abs(G)) sum_(g' in G) g' q(g'^(-1) h v) = overline(q)(h v) \
$

If $v in "Ker"(overline(q)), h in G$ then $h overline(q)(v) = 0 = overline(q)(h v)$ that $h v in "Ker"(overline(q))$ that we decompose by a $G$-invariant morphism based on solely vector space projection $q$.

// TODO!
How can we define a $G$-invariant operation on $V$? We should *always* remember that $g$ act transitively on $G$ itself that if $g G = G$. Then if we can put all elements of $G$ on the operation, then it should be $G$-invariant. By the way, we can define the module of $G$-invariance which is $R G = sum_(g_i in G) r_i g_i quad r_i in R, g_i in G$. The way is to average the operation by group action for all elements. Thus one has:

$
  h f(v_1, dots.c, v_n) & = 1/(abs(G)) sum_(g in G) h g f(g^(-1) h^(-1) h v_1, dots.c, g^(-1) h^(-1) h v_n) \
                        & = 1/(abs(G)) sum_(g' in G) g' f(g'^(-1) h v_1, dots.c, g'^(-1) h v_n) = f(h v_1, dots.c, h v_n) \
$

$
  f(h v_1, dots.c, h v_n) &= 1/(abs(G)) sum_(g in G) g f(g^(-1) h v_1,dots.c, g^(-1) h v_n) \ &= 1/(abs(G)) sum_(h^(-1) g in G) h^(-1) g f((h^(-1) g)^(-1) v_1, dots.c,(h^(-1) g)^(-1) v_n) = f(v_1,dots.c,v_n)\
$

$
  innerproduct(v, u) = innerproduct(u, v)^* \
  innerproduct(u, alpha v + beta w) = alpha innerproduct(u, v) + beta innerproduct(u, w) \
  norm(u)^2 = innerproduct(u, u)
$

$
  innerproduct(rho(g) x, rho(g) y) = innerproduct(x, y) \
$

If there's a invariant space that $rho(g) (V_1) subset.eq V_1$, with the decomposition $V_2 = V_1^(perp)$ that $V_2 = {v in V | (v,x) = 0 thick forall x in V_1}$.

$
  innerproduct(rho(g) x, y) = innerproduct(rho(g)^(-1) rho(g) x, rho(g)^(-1) y) = innerproduct(x, rho(g)^(-1) y) quad forall y in V_1
$

Thus if $x in V_2$, the inner product should be *zero*. Reversely, we deduce that $rho(g) x in V_2$ because $y in V_1$ by first term. Therefore the representation can be decomposed if we seek a *sole* invariant space and repeat the procedure.

Thus given a inner product, which is also a bilinear-function, we can construct $G$-invariant form like above.

$
  innerproduct(x, y) := sum_(h in G) innerproduct(rho(h)x, rho(h)y)
$

Which is _unitary_ as above already proved. Same as integral form one has:

$
  innerproduct(x, y) := integral_G d mu(h) innerproduct(rho(h)x, rho(h)y)
$

Yields the same results. However, we can conclude the canonical $G$-invariance form for _finite_ and _compact_ group due to the convergence given by the integral only for compactness.

Given linear morphism for irreducible space, $phi_1: V -> W$ and $phi_2: V->W$, one could inspect that due to $ker (phi) = {0} "or" V$ due to *irreducible* property, one can acquire no smaller subspace. Thus, $phi = 0 "or" "isomorphism"$, by uniqueness, $phi_1 = lambda phi_2$.

Now given a space transformation:
$
  phi(rho(g)) = A^(-1) rho(g) A = rho' (g)
$

By above suggestion on irreducible representation, one should have $A = 0$, or better, the irreducible representation should be isomorphism, thus $A = lambda I$. However, for clarification, you should prefer $bb(C)$ field that to fully decompose space rather the root problem would occur.

$
  (v_1,v_2) -> v_1 times.o v_2 equiv v_1^i e_1^i times.o v_2^j e_2^j = v_1^i thin v_2^i thin e_1^i times.o e_2^j
$

$
  (rho_1 times.o rho_2) (g) (v_1 times.o v_2) = rho_1 (g) (v_1) times.o rho_2 (g) (v_2)
$

$
  chi_rho (g) = "Tr" (rho (g)) \
$

$
  chi_rho'(g) = "Tr" (rho'(g)) = "Tr" (A^(-1) rho(g) A) = "Tr" (A^(-1) A rho(g)) = "Tr" (rho(g)) = chi_rho (g)
$

$
  chi_(rho_1 plus.o rho_2) (g) = "Tr" (rho_1 plus.o rho_2 (g)) = "Tr"(rho_1 (g)) + "Tr"(rho_2 (g)) = chi_(rho_1) (g) + chi_(rho_2) (g)
$

$
  chi_(rho_1 times.o rho_2) (g) = "Tr" (rho_1 times.o rho_2 (g)) &= "Tr"(rho_1 (g)) times.o "Tr"(rho_2 (g)) \ &= chi_(rho_1) (g) times.o chi_(rho_2)(g) = chi_(rho_1) (g) chi_(rho_2) (g) times.o 1 tilde.equiv chi_(rho_1) (g) chi_(rho_2) (g)
$

$
  chi_rho (e) = "Tr" (rho (e)) = "Tr" (I_V) = dim (V)
$

$
  M^(i k)_(j l) = integral_G d mu (g) thin rho_1(g)^i_j rho_2(g^(-1))^k_l
$

$
  rho_1 (h)^i_a rho_1 (g)^a_j = rho_1 (h g)^i_j
$

$
  rho_1 (h)^i_a M^(a k)_(j l) & = integral_G d mu (g) rho_1 (h)^i_a rho_1 (g)^a_j rho_2(g^(-1))^k_l \
                              & = integral_G d mu (h g) rho_1 (h g)^i_j rho_2 (g^(-1))^k_l quad h g -> g' \
                              & = integral_G d mu (g') rho_1 (g')^i_j rho_2 (g'^(-1) h)^k_l \
                              & = M^(i k)_(j b) rho_2(h)^b_k
$

By Schur's lemma, one acquire a one for all relation that either isomorphism, or nothing for $M$ as a transformation matrix. Thus, fix $j, k$ as $M^(j l)_(i k) = cal(M)_i^l$.

$
  M^(j l)_(i k) = alpha^j_k delta_i^l \
$

However, one can change the summation for matrix by apply direction as:

$
  rho_1(h)^a_j rho_1 (g)^i_a = rho_1 (g h)^i_j
$

Giving us:

$
  M^(j l)_(i k) = beta^l_i delta^j_k = alpha^j_k delta^l_i \
$

Thus it's actually a decomposition as $C delta^j_k delta^l_i$ for the same irreducible representation or else nothing. We then find it's actually a trace summation:

$
  integral_G d mu (g) rho (g)^i_j rho (g^(-1))^j_i = integral_G d mu (g) "Tr" (I_V) = n integral_G d mu (g) = sum_(i, j) M^(i j)_(j i) = C n^2
$

If we can normalize the integral:

$
  integral_G d mu (g) = 1 -> C = 1/n = 1/(dim (V))
$

$
  integral_G d mu (g) rho (g)^i_i rho (g^(-1))^j_j = integral_G d mu (g) chi_rho (g) chi_rho (g^(-1)) = sum_(i j) M^(i j)_(i j) = C n^2 = n
$

Thus, one has:

$
  1/n integral_G d mu (g) chi_rho_1 (g) chi_rho_2 (g^(-1)) = 1_id delta_(rho_1,rho_2)
$

==

$
  vf(F)(q,p) = vec(F_q (q,p), F_p (q,p)) = vec(partial_q F(q,p), partial_p F (q,p))\
$

$
  d H = H_q d q + H_p d p = - dv(p, t) d q + dv(q, t) d p \
$

$
  dv(, t) = dv(q, t) partial_q + dv(p, t) partial_p = H_p partial_q - H_q partial_p := {dot,H} := X_H
$

That's, Hamiltonian defines the evolution of the system.
$
  dv(F(q,p), t) = X_H F(q,p) = {F(q,p),H} \
$

$
  X_H (p thin d q) = dot(p) d q + p d dot(q) & = dot(p) d q - dot(q) d p + d (p dot(q)) \
                                             & = - H_q d q + H_p d p + d (p dot(q)) = d (-H + p dot(q)) := d L(q, dot(q))
$

$
  {F,H} = X_H F = - X_F H \
$

Where the $X_F = pdv(F, p) partial_q - pdv(F, q) partial_p$.

Generally, one scalar function defined upon sympletic manifold can induce a vector field on it, with a general area preservation:

$
  omega = d q and d p \
  iota_(X_F) (omega) = iota_(pdv(F, q) partial_p - pdv(F, p) partial_q) (d q and d p) = pdv(F, q) d q + pdv(F, p) d p = d F \
$

$
  iota_(X_H) iota_(X_F) (omega) = iota_(X_H) (d F) = X_H F = {F,H} = dv(F, t)
$

We thus induce a symmetric bilinear form:

$
  omega(X_F, X_G) = iota_(X_F) iota_(X_G) (omega) = iota_(X_F) (d G) = X_F G = {G,F} = - {F,G} \
$

One can lift the Hamiltonian in exponential flow by dynamics of $X_H$.

$
  dv(, t) F(exp(t X_H)) bar_(t=0) = {F(p,q), H(p,q)}
$

One thus can define lie group dynamics too just like above:

$
  L in #lie[g] -> X_L \
  X_L F(p,q) = dv(, t) F(e^(t L) dot (p,q)) \
$

However, due to the representation of any group should be a anti-homomorphism, we have:

$
  L dot F(p,q) = dv(, t) F(e^(-t L) dot (p,q)) = - X_L F(p,q)\
$

Now we can try translation group $T = bb(R)^3$ first:

$
  a dot (q,p) = (q + a, p) quad a in T <-> e^(-t lambda) in T thick lambda in #lie[t]\
$
Here we *abuse* of notation because the lie algebra of translation induced by lie group is trivial.
$
  a dot F(p,q) = dv(, t) F(e^(- t lambda) dot (p,q)) bar_(t=0) = dv(, t) F(q-t a,p) bar_(t=0) = -a pdv(, q) F = - X_a F
$

$
  X_a = a pdv(, q) \
$

We know that $iota_(X_F) (omega)$ is a closed form that it corresponds to a certain function $F$ up to a constant, we can induce the scalar function of action by the lie group.

$
  X_a (omega) = a p -> mu_a (p) = mu_a (p,q)
$

We thus recover the momentum operator which configures the momentum for each translation element $a$. Such closed form check lift a function defined in the manifold which shared the same role as Hamiltonian, if $H$ is $G$-invariant, then $mu_a$ is a conserved quantity, as the Hamiltonian version of Noether's theorem.

$
  iota_(X_H) (d mu_L) = {mu_L,H} = dv(mu_L, t) = - {H,mu_L} = -iota_(X_L) (d H) = - X_L H = 0 \
$

==

$
  [phi.alt(X), phi.alt(Y)] = phi.alt([X,Y]) = phi.alt(X) phi.alt(Y) - (-1)^(sigma(X) sigma(Y)) phi.alt(Y) phi.alt(X) \
$

$
  Omega (J v_1, J v_2) = Omega(v_1, v_2) -> J in "Sp"(2n, bb(R))
$

$
  A^T A = I -> A in "O"(n, bb(R)) \
  A^T Omega A = Omega -> A in "Sp"(2n, bb(R)) \
  A^T Omega A = A^T A Omega -> A^T (Omega A - A Omega) = 0 -> Omega A = A Omega \
  Omega(A v, A w) = g(A Omega v, A w) = g(Omega A v, A w) = Omega(v, w) \
  A in "O"(n, bb(R)) inter "Sp"(2n, bb(R)) = "U"(n) \
$

$
  z_j = 1/sqrt(2) (q_j + i p_j), quad overline(z_j) = 1/sqrt(2) (q_j - i p_j) \
$

$
  L_1 = Q_2 P_3 - Q_3 P_2, quad L_2 = Q_3 P_1 - Q_1 P_3, quad L_3 = Q_1 P_2 - Q_2 P_1 \
  Gamma(L_1) = a_3^(dagger) a_2 - a_2^(dagger) a_3, quad Gamma(L_2) = a_1^(dagger) a_3 - a_3^(dagger) a_1, quad Gamma(L_3) = a_2^(dagger) a_1 - a_1^(dagger) a_2 \
$

$
  & F(theta) = c_0 + c_1 theta + c_2 theta^2 + dots.c + c_n theta^n = c_0 + c_1 theta \
  & pdv(F, theta) = c_1 \
  & F(theta_1,dots.c,theta_n) = F_A + theta_j F_B quad exists F_A, F_B in and.big (bb(R)^n) \
  & pdv(F G, theta_j) = pdv(F, theta_j) G + (-1)^(sigma(F)) F pdv(G, theta_j) quad sigma(F) #[is the degree of] F \
$

Given a translation invariance property of integral:

$
  integral f(theta + eta) d theta = integral f(theta) d theta \
$

$
  integral (theta + eta) d theta = integral theta d theta + eta integral d theta = integral theta d theta -> integral d theta = 0\
$

Given with normalization convention:

$
  integral theta d theta = 1 -> integral c_0 + c_1 theta d theta = c_1 -> integral f(theta) d theta = dv(f, theta)\
$

Thus for multi-variables calculus, one should be careful on applying order of partial derivative:

$
  integral f(theta_1,dots.c,theta_n) d theta_n dots.c d theta_1 = pdv(, theta_1) dots.c pdv(, theta_n) f\
$
Where swap of order of partial derivative will induce a minus sign.

$
  [theta_j, theta_k]_+ = plus.minus delta_(j k) \
  dv(, t) theta_j (t) = [theta_j (t),H]_+
$

Given $H$:

$
  B = mat(0, B_(12), B_(13), dots.c, B_(1n); -B_(12), 0, B_(23), dots.c, B_(2n); -B_(13), -B_(23), 0, dots.c, B_(3n); dots.c; -B_(1n), -B_(2n), -B_(3n), dots.c, 0) \
  H = 1/2 sum_(j,k=1)^n B_(j k) theta_j theta_k \
$

$
  dv(, t) theta_j (t) = [theta_j (t),H]_+ = -[H,theta_j (t)]_+ = sum_(k=1)^n B_(j k) theta_k (t) \
$
The minus sign of commutator is due to $B_(j k) = - B_(k j)$. Which is highly similar to the bosonic case in evolution.

$
  Omega^+(J v_1, J v_2) = Omega^+ (v_1, v_2) -> J in "SO"(2n, bb(R))
$

$
  U_A = sum_(j k) a^(dagger)_j A_(j k) a_k \
  [U_A, a_j]_(plus.minus) = plus.minus sum_k A_(j k) a_k = plus.minus A bold(a)\
  [U_A, a^(dagger)_j]_(plus.minus) = sum_k a^(dagger)_k A_(k j) = A^T bold(a)^(dagger)\
$

$
  v times.o w = 1/2 (v times.o w - u times.o v) + 1/2 (v times.o w + w times.o v) = v and w + g(v,w)
$

Thus given a basis omit tensor notation, for example:

$
  e_i e_j = e_i and e_j quad (i != j)
$

Or physics notation:

$
  bold(v) = (v_1,dots.c,v_n) in bb(R)^n -> gamma(bold(v)) = cancel(bold(v)) = v_1 gamma_1 + dots.c + v_n gamma_n \
$

$
  v' = v - 2 (g(v,w))/(g(w,w)) w = cancel(v) - (cancel(v) cancel(w) - cancel(w) cancel(v))/(g(w,w)) cancel(w) \ = - (cancel(w) cancel(v) cancel(w))/(g(w,w))
$

$
  2 A B = [A,B]_plus + [A,B]_minus \
  2 B A = [A,B]_plus - [A,B]_minus \
$

Thus we can always decompose a product term into symmetric and antisymmetric parts.

$
  A B C = 1/2 A [B,C]_plus + 1/2 A [B,C]_minus = 1/2 [A,B]_plus C - 1/2 [A,C]_plus B + 1/2 [A,B]_minus C - 1/2 [A,C]_minus B \
$

$
  [A B, C]_minus = A B C - C A B & = A (1/2 [B,C]_plus + 1/2 [B,C]_minus) - (1/2 [A,C]_plus - 1/2 [A,C]_minus) B \
                                 & = 1/2 (A [B,C]_plus - [A,C]_plus B) + 1/2 (A [B,C]_minus + [A,C]_minus B) \
$

$
  [A B, C]_plus = A B C + C A B & = A (1/2 [B,C]_plus + 1/2 [B,C]_minus) + (1/2 [A,C]_plus - 1/2 [A,C]_minus) B \
                                & = 1/2 (A [B,C]_plus - [A,C]_minus B) + 1/2 (A [B,C]_minus + [A,C]_plus B) \
$

Equal below:

$
  [A B, C]_minus = A [B,C]_minus + [A,C]_minus B = A [B,C]_plus - [A,C]_plus B \
$

$
  [A B, C]_plus = A [B,C]_plus + [A,C]_minus B = A [B,C]_minus - [A,C]_plus B \
$


$
  [A B, C D]_minus & = A [B, C D]_minus + [A, C D]_minus B \
                   & = A ( [B,C]_plus D - C[B,D]_plus) + ([A,C]_plus D - C[A,D]_plus) B \
                   & = A [B,C]_plus D - A C [B,D]_plus + [A,C]_plus D B - C [A,D]_plus B \
$

For Clifford algebra, symmetric part is given by metric, anti-symmetric part is given by wedge product.
$
  & tensor(M, -mu, -nu) = gamma_mu and gamma_nu \
  & tensor(M, -mu, -nu) = gamma_mu gamma_nu - tensor(g, -mu, -nu) \
$

$
 tensor(M,-mu,-nu) = [gamma_mu,gamma_nu]_-
$

$
  tensor(M, -mu, -nu) and gamma_rho = gamma_mu gamma_nu and gamma_rho = gamma_mu g_(nu rho) - gamma_nu g_(mu rho)
$

By $[A B,C]_- = dots$.

$
  tensor(M, -mu, -nu) and tensor(M, -rho, -sigma) = gamma_mu gamma_nu and gamma_rho gamma_sigma = gamma_mu gamma_sigma g_(v rho) - gamma_mu gamma_rho g_(nu sigma) + gamma_nu gamma_rho g_(mu sigma) - gamma_nu gamma_sigma g_(mu rho)
$
Is same as above, however, I didn't found this is useful : (.

==

$
  L/[L,L] #[is abelian that] forall a,b in L, [a,b] = 0
$

Thus given a central series:

$
  [L^n, L^n] = L^(n+1) -> L^n/[L^n,L^n] = L^n/L^(n+1)
$
Factor through, for all possible elements, otherwise $[L, L] = L$ is irreducible. Thus induce a maximal nilpotent ideal of $L$ which is the maximal solvable ideal of $L$, else it must be a *semi-simple* structure without additional smaller space. Where nilpotent is a structure that can be shared with a basis with commutative eigenvectors, that's $X Y v = Y X v + [X, Y]v = lambda(X) Y v + lambda ([X,Y]) v$ where $[X,Y]$ in some smaller space by deduction of nilpotent ideal.

Given a basis ${X_1,dots.c,X_n}$ with structure constants for a semi-simple lie algebra:

$
  [X_i ,X_j] = sum_k tensor(c, -i, -j, +k) X_k \
$

Given the commutation relation, one has:
$
  tensor(c, -i, -j, +k) = - tensor(c, -j, -i, +k) \
  tensor(c, -i, -j, +k) + tensor(c, -j, -k, +i) + tensor(c, -k, -i, +j) = 0 \
$

Moreover, we can define the representation based on the structure constants:

$
  & (T_i)_j^k = (D_(X_i))_j^k = tensor(c, -i, -j, +k) \
  & D_(X_i): #lie[g] -> "ad"(#lie[g])
$

$
  D_(X_i) X_j = [X_i, X_j] = sum_k tensor(c, -i, -j, +k) X_k \
$

$
  [D_(X_i), D_(X_j)] = D_([X_i, X_j]) \
  [D_(X_i), D_(X_j)] X_k = D_([X_i, X_j]) X_k \
  [X_i [X_j X_k]] - [X_j [X_i X_k]] = [[X_i, X_j] X_k] \
$

Which adjoin representation with *homomorphism consistency* should restrict all lie algebras to contain Jacobi identity.

$
  D_(X_i) D_(X_j) X_l = D_(X_i) tensor(c, k, -j, -l) X_k = tensor(c, -i, -k, m) tensor(c, -j, -l, k) X_m \
  (D_(X_i) D_(X_j))^m_l = tensor(c, -i, -k, m) tensor(c, -j, -l, k) \
  "Tr"(D_(X_i) D_(X_j)) = (D_(X_i) D_(X_j))^m_m = tensor(c, -i, -k, m) tensor(c, -j, -m, k) = tensor(g, -i, -j) = tensor(c, -j, -m, k) tensor(c, -i, -k, m) = tensor(g, -j, -i) \
$

Where:

$
  tensor(g, -i, -j) tensor(g, j, l) = tensor(c, -i, -k, m) tensor(c, -j, -m, k) tensor(c, j, n, -f) tensor(c, l, f, -n) = tensor(c, -i, -k, m) tensor(c, l, f, -n) tensor(delta, -m, n) tensor(delta, k, -f) = tensor(delta, -i, l)
$

// $
//   [D_(X_i), D_(X_j)]_(k l) = sum_m (tensor(c, -i, -j, +m) tensor(c, -m, -k, +l) - tensor(c, -j, -i, +m) tensor(c, -m, -k, +l)) = sum_m tensor(c, -i, -j, +m) tensor(c, -m, -k, +l) \
// $
//
$
  innerproduct(v, w) = v^i (D_(X_i))_k^l v^j (D_(X_j))_l^k = v^i v^j g_(i j)
$

Cyclic property:

$
  0 = "Tr" ([A,B C]) & = "Tr" (B[A,C]) + "Tr" ([A,B]C) \
$

$
  "Tr" ([A,B]C) & = "Tr" ((A B - B A) C) \
              & = "Tr" (A B C) - "Tr" (B A C) \
              & = "Tr" (A B C) - "Tr" (A C B) = "Tr" (A [B,C]) \
$

$
  0 = "Tr" ([rho(X_i) rho(X_j), rho(X_k)]) & = "Tr" (rho(X_i)[rho(X_j),rho(X_k)]) + "Tr" ([rho(X_i),rho(X_k)]rho(X_j)) \
                                         & = "Tr" (rho(X_i) f_(j k)^d rho(X_d)) + "Tr" (f_(i k)^d rho(X_d) rho(X_j)) \
                                         & = f_(j k)^d g_(i d) + f_(i k)^d g_(d j) \
                                         & = f_(j k i) + f_(i k j)
$

Given with $f_(j k i) = - f_(k j i)$, one has $f_(j k i) = - f_(k j i) = f_(i j k) = - f_(j i k)$. It's totally anti-symmetric tensor.

Fix indices as $f_(i j)^k = (cal(f)_i)^k_j$:
$
  cal(f)_j g^(\(rho\)) + (cal(f)_i g^(\(rho\)))^T & = 0 \
            g^(-1)^(\(rho\)) cal(f)_j g^(\(rho\)) & = - cal(f)_i^T quad "by" g = g^T \
                             cal(f)_j g^(\(rho\)) & = g^(\(rho\)) g^(-1)^(\(rho\)) cal(f)_j g^(\(rho\)) \
            cal(f)_j g^(\(rho\)) g^(-1)^(\(rho\)) & = g^(\(rho\)) g^(-1)^(\(rho\)) cal(f)_j \
$

Thus by Schur's lemma, for _simple_ lie algebra, it should be up to constant for the representation of the metric form compared with the canonical metric form.

However, it doesn't mean that *semi-simple* structure contains no ideal. We try to diagonalize as much as possible even we can't achieve for all like solvable case. That's $#lie[t] subset #lie[g]$ which all elements are commutative. We call such maximal commutative subalgebra as *Cartan subalgebra*, which can be diagonalized simultaneously. Thus if one choose a vector space it acts on, we can decompose the space into eigen-space for all:

$
  V = plus.o.big_(lambda(#lie[t])) V_lambda quad V_lambda = {v in V | forall H in #lie[t], H v = lambda(H) v} \
$

Given a adjoin representation or homomorphism as $X_i -> D_(X_i)$, we can then apply the Cartan subalgebra to decompose the lie algebra itself:

$
  #lie[g] = plus.o.big_(alpha(#lie[t])) #lie[g] _alpha quad #lie[g] _alpha = {X in #lie[g] | forall H in #lie[t], [H,X] = D_(H) (X) = alpha(H) X} \
$
Which is called *root space decomposition*, where $alpha in #lie[t]^*$ is the eigenvalue on $#lie[t]$.

We often see the ladder operator in physics that a state shared by all other raising and lowering operators, which is the eigenvector of Cartan subalgebra.

$
  bold(H) = (H_1,dots.c,H_r) \
  [H_i, H_j] = 0 quad forall i,j = 1,dots.c,r -> [rho(H_i),rho(H_j)] = 0 quad "for finite representation"
$

Due to mutually commutation, each $H_i$ can share the same eigenstate with weights $bold(m)$.
$
  rho(H_i) ket(bold(m)) = m_i ket(bold(m)) quad bold(m) = (m_1,dots.c,m_r)
$

Plus, given by the adjoint representation, the same routine is applied for remained decomposition.
$
  D_H_i (E_(bold(alpha))) = [H_i, E_(bold(alpha))] = bold(alpha)(H_i) E_bold(alpha) = alpha_i E_(bold(alpha)) quad bold(alpha) = (alpha_1,dots.c,alpha_r)
$

#[
  #let balpha = $bold(alpha)$
  #let bbeta = $bold(beta)$
  $
    D_H_i ([E_balpha,E_bbeta]) = [H_i, [E_balpha,E_bbeta]] &= [[H_i,E_balpha],E_bbeta] + [E_balpha,[H_i,E_bbeta]] \
    &= (alpha_i + beta_i) [E_balpha,E_bbeta] ~ H_i E_(balpha + bbeta) <-> [#lie[g] _alpha,#lie[g] _beta] subset.eq #lie[g] _(alpha+beta)\
  $
]

Just like you already have seen in generator of $lie(s u)(2)$ that $[xi_3, xi^(plus.minus)] = plus.minus xi^plus.minus$.

We know if the ladder operator act too many times in finite representation, it will reach zero, that's $D_(X)$ is nilpotent for $X in #lie[g] _(alpha), alpha != 0$, or we simply call it nilpotent that $#lie[g] _(beta+ n alpha) = 0$.

For clarity, $#lie[g] _0$ means $[#lie[t],#lie[g] _0] = 0 dot #lie[g] _0 = 0$ thus $#lie[t] subset #lie[g] _0$, however, due to maximality of Cartan subalgebra, we have $#lie[g] _0 = #lie[t]$.

$
  [#lie[g] _alpha,#lie[g] _(-alpha)] subset.eq #lie[g] _0 = #lie[t] \
$

Given a unitary representation, with the observable eigenvalue should be _real_, thus, we restrict $bold(m), bold(alpha)$ to real value, or $bold(H)^dagger = bold(H)$.

$
  [H_i, E_bold(alpha)]^dagger = (alpha_i E_bold(alpha))^dagger -> [E_bold(alpha)^dagger, H_i] = alpha_i^* E_bold(alpha)^dagger = - [H_i, E_bold(alpha)^dagger] -> E_bold(alpha)^dagger in lie(g)_(-alpha)
$

Which is justify the existence of $lie(g)_(-alpha)$

$
  [E_bold(alpha), E_(-bold(alpha))] = sum_i^r b^i H_i \
$

Restrict to $lie(t)$, we acquire its metric as $"Tr" (H_i H_j) = g_(i j)$.

$
  sum_j g_(i j) b^j = "Tr" (H_i [E_bold(alpha), E_(-bold(alpha))]) = "Tr" ([H_i, E_bold(alpha)] E_(-bold(alpha))) = alpha_i "Tr" (E_bold(alpha),E_(-bold(alpha)))
$

If we normalize that $"Tr" (E_bold(alpha),E_(-bold(alpha))) = 1$.

$
  sum_j g_(i j) b^j = alpha_i -> b^j = sum_i g^(i j) alpha_i
$

We thus could define $H_bold(alpha) := [E_bold(alpha), E_(-bold(alpha))] = sum_j b_j H_j$.

$
  [H_bold(alpha),E_bold(beta)] = sum_j b_j [H_j, E_bold(beta)] = (bold(b) dot bold(beta)) E_bold(beta) -> [H_bold(alpha), E_bold(plus.minus alpha)] = plus.minus (bold(b) dot bold(alpha)) E_(plus.minus bold(alpha))\
$

However:
$
  bold(b) dot bold(alpha) = sum_(i j) alpha_i alpha_j g^(i j) = innerproduct(alpha, alpha)
$

And we actually acquire a more ease representation as $H_bold(alpha)$.

===
#[
  #let bm = $bold(m)$
  #let balpha = $bold(alpha)$
  #let bbeta = $bold(beta)$
  #let rhoket(body) = $ket(#[$rho; body$])$
  $
    rho(H_i) rho(E_bold(alpha)) ket(#[$rho; bm$]) = ([rho(H_i),rho(E_bold(alpha))] + rho(E_bold(alpha)) rho(H_i)) ket(#[$rho;bm$]) = (bold(alpha)_i + m_i) E_(bold(alpha)) ket(#[$rho;bm$])
  $

  $
    rho(E_balpha) rhoket(bm) = N_alpha (bm) rhoket(bm + balpha)
  $

  $
       & [rho(E_balpha),rho(E_(-balpha))] = rho (H_balpha) \
    -> & N_alpha (bm - balpha) N_(-alpha) (bm) - N_(-alpha) (bm + balpha) N_(alpha) (bm) = (balpha,bm)
  $

  $
    E_balpha rhoket(bm + p balpha) = 0 quad E_(-balpha) rhoket(bm - q balpha) = 0
  $

  $
    N_alpha (bm + (k - 1) balpha) N_(-alpha)(bm + k balpha) - N_(-alpha) (bm + (k+1) balpha) N_alpha (bm + k balpha) = innerproduct(balpha, bm + k balpha)
  $

  $
    sum_(k = -q)^p &N_alpha (bm + (k - 1) balpha) N_(-alpha)(bm + k balpha) \ &- N_(-alpha) (bm + (k+1) balpha) N_alpha (bm + k balpha) = sum_(k=-q)^p innerproduct(balpha, bm + k balpha)
  $

  Then, for second term, change the summation from $k -> k - 1$, we cancel each term except the first and last.

  $
    & N_alpha (bm - (q + 1) balpha) N_(-alpha)(bm - q balpha) \
    & - N_(-alpha) (bm + (p + 1) balpha) N_alpha (bm + p balpha) = sum_(k=-q)^p innerproduct(balpha, bm + k balpha)
  $

  However, due to the finite order restriction, the left terms all vanish.
  $
    (p+q+1) innerproduct(balpha, bm) + (1/2 p(p+1) - 1/2 q(q+1)) innerproduct(balpha, balpha) & = 0 \
                                      2 innerproduct(balpha, bm)/innerproduct(balpha, balpha) & = q-p
  $

  So what's the procedure to investigate the roots of a lie algebra? First, given a canonical matrix representation, one should find the Cartan subalgebra, how? We seek the maximal independent _diagonal_ matrix set. Then seek the relation of $bold(H)$ and remaining elements, you may not pretty lucky to find direct scalar relation rather mixed terms. Then, you should make a combination like $v = a^i M_i$, and try to build by $[H_i, a^j M_j] = lambda_i a^j M_j$ exactly. Given each coefficient with normalization, you may find a set of $delta_(i,j) + delta_(i+1,j) +dots.c$ for possible slots. Summarize, it can be evaluated for $bold(alpha) (H_i)$ for $i$ index of this vector, it indicates to extract the $i$ set to form a basis combination by $delta_(i j) + delta_(i+1,j) ~ e_j$ etc, which is the root.

  === $A_n = lie(s l)(n+1)$

  #let bue = $bold(upright(e))$

  Given $bue_i$ for $i = 1,dots.c,n+1$ in $bb(R)^(n+1)$ parametrize the lie algebra $lie(s l)(n+1)$. Thus the matrix is represented by $(M_(i j))_(alpha beta) = delta_(i alpha) delta_(j beta)$ which Kronecker index connects the matrix slot and generator index.

  It's more natural to just seek a matrix summation to yield results, rather a direct index summation is false. Looking at the $j k$ summation yielding:

  $
    M_(i,j) M_(k,l) = delta_(j,k) M_(i,l)
  $

  $
    [M_(i,j), M_(k,l)] = delta_(j,k) M_(i,l) - delta_(i,l) M_(j,k)
  $

  Given $"Tr" (lie(s l)(n+1)) = 0$, we should take the maximal diagonal and traceless basis set, then we choose:

  $
               H_i & = M_(i,i) - M_(i+1, i+1) \
    [H_i, M_(k,l)] & = delta_(i,k) M_(i,l) - delta_(i+1,k) M_(i+1,l) + delta_(i,l) M_(k, i) - delta_(i+1,l) M_(k,i+1) \
                   & = (delta_(i,k) - delta_(i,l) - delta_(i+1,k) + delta_(i+1,l)) M_(k,l)
  $

  Now, be clever to extract the basis of $i$ index to form simple root set.
  $
    bold(alpha) = bue_(k) - bue_(l) quad E_bold(alpha) = M_(k,l) \
  $

  $
    [H_i, E_(balpha)] & = balpha(H_i) E_(balpha) \
    bold(alpha) (H_i) & = (delta_(i,k) - delta_(i,l)) - (delta_(i+1,k) - delta_(i+1,l))
  $

  Where we choose root as $alpha_i = bue_i - bue_(i+1) quad i = 1,dots.c,n$ to expand into more clarified basis set.
  $
    bue_k - bue_l = sum_k^(l-1) (bue_i - bue_(i+1))
  $

  $
    innerproduct(alpha_i, alpha_j) = cases(2 &"if" i = j, -1 &"if" abs(i-j) = 1, 0 &"if" abs(i-j) >= -2)
  $

  We only care about the normalization relation upon the inner product, which build the relation between each basis. How to express this clearly? One named _Dynkin_, creates the diagram as follows:

  #let dynkin_node(pos) = node(pos, radius: 4pt, stroke: 0.5pt)
  #align(center)[
    #figure(
      diagram({
        let nodes = range(6).map(i => {
          if i == 4 {
            return node((i * 0.5, 0))[$dots.c$]
          }
          dynkin_node((i * 0.5, 0))
        })

        let syms = range(6).map(i => {
          if i == 4 {
            return
          }
          if i == 5 {
            return node((i * 0.5, 0.3))[$balpha_n$]
          }
          node((i * 0.5, 0.3))[$balpha_#(i + 1)$]
        })

        (..nodes,).intersperse(edge("-"))
        (..syms,)
      }),
      caption: [Dynkin diagram of $A_n = lie(s l)(n+1)$],
    )
  ]

  Where the solid line connects node indicates $-1/2 = cos pi/3$ by normalization of simple roots in $i,j$ where $abs(i-j)=1$. Thus, given a relation between nodes, we connects nodes by single or multiple solid lines to indicates different normalization angles. We could also express in matrix form by $C_(i j) = innerproduct(alpha_i, alpha_j)$ called _Cartan_ matrix which is too sparse in expression compared to Dynkin diagram.

  === $D_n = lie(s o)(2n)$

  As for algebra $lie(s o)(2n)$, the antisymmetric matrix should be denoted as $M_(i j) = - M_(j i) = - M_(i j)^T$ for $i, j = 1,dots.c,2n$.

  $
    (M_(i j))_(alpha beta) = delta_(a,alpha)delta_(b,beta) - delta_(a,beta) delta_(b,alpha) \
  $

  We should notie that one should transpose the index to sum again in second term, thus given $(i,j) (k,l)$, we should merge $j,k$ first and then $i,k$.

  $
    [M_(i,j),M_(k,l)] = delta_(j,k) M_(i,l) - delta_(i,k) M_(j,l) + delta_(l,i) M_(k,j) - delta_(k,i) M_(l,j) \
  $

  We define the Cartan subalgebra as, for maximal $n$ ranks for $lie(s o)(2n)$:

  $
    H_i = M_(2i-1,2i) quad i = 1,2,dots.c,n
  $

  Which is *not* diagonalizable actually, that it must mix four elements by previous calculation. If one need to diagonalize such basis, we should take in $bb(C)$ with $i$ factor appended. Rank $n$ is the consequence derived from maximally $n$ independent rotation.

  We aren't lucky enough to extract the scalar for a single basis, rather those are scalars distributing around different ones. Thus, we choose a vector format to calculate by choose a various $j,k = 1,2,dots.c,n$ basis:

  $
    bold(M) = a M_(2j-1,2k-1) + b M_(2j,2k-1) + c M_(2j-1,2k) + d M_(2j,2k) \
    [H_i,bold(M)] = a (delta_(2i,2j-1) M_(2i-1,2k-1) - delta_(2i-1,2j-1) M_(2i,2k-1) + delta_(2k-1,2i-1) M_(2i,2j-1) - delta_(2k-1,2i) M_(2i-1,2j-1)) + dots.c \
  $

  We suddenly found that $2i != 2j-1$ ever and ever because one is odd and one is even! We immediately reduce the index into $2i-1,2j-1$ or $2k-1,2i-1$. Then, we note that $delta_(i,j) M_(2i,2k-1) = M_(2j,2k-1)$, $delta_(k,i) M_(2i,2j-1) = - M_(2j-1,2k)$.

  Thus we choose:
  $
    & balpha = eta bue_j + eta' bue_k quad j!= k quad eta, eta' = 1,-1 \
    & E_balpha = 1/2 (M_(2j-1,2k-1) + eta M_(2j,2k-1) + eta' M_(2j-1,2k) - eta eta' M_(2j,2k)) \
    & balpha(H_i) = eta delta_(i,j) + eta' delta_(i,k) \
    & [H_i, E_balpha] = (eta delta_(i,j) + eta' delta_(i,k)) E_balpha
  $

  By counting numbers of generators, we found that they are $2n(n-1)$ for $j,k$ root generators.

  $
    & alpha_i = bue_i - bue_(i+1) quad i = 1,dots.c,n-1 \
    & alpha_n = bue_(n-1) + bue_n \
  $

  Actually, choose arbitrary sign is acceptable, but such is preferable.

  $
    innerproduct(alpha_i, alpha_j) = cases(2 &"if" i = j, -1 &"if" abs(i-j)=1, 0 &"if" abs(i-j) = 0, 0 &"if" i = n-1 thick j=n)
  $

  We draw the _Dynkin_ diagram as below:
  #figure(
    diagram(
      {
        let nodes = range(4).map(i => {
          if i == 2 {
            return node((i * 0.5, 0))[$dots.c$]
          }
          dynkin_node((i * 0.5, 0))
        })

        let syms = range(4).map(i => {
          if i == 2 {
            return
          }
          if i == 3 {
            return node((i * 0.5, 0.3))[$balpha_(n-2)$]
          }
          node((i * 0.5, 0.3))[$balpha_#(i + 1)$]
        })

        (..nodes,).intersperse(edge("-"))
        (..syms,)
      },
      dynkin_node((4 * 0.5, 0.5)),
      node((4 * 0.5, 0.8))[$balpha_(n)$],
      dynkin_node((4 * 0.5, -0.5)),
      node((4 * 0.5, -0.2))[$balpha_(n-1)$],
      edge((3 * 0.5, 0), (4 * 0.5, 0.5)),
      edge((3 * 0.5, 0), (4 * 0.5, -0.5)),
    ),
    caption: [Dynkin diagram of $D_n = lie(s o)(2n)$],
  )

  #figure(
    diagram(
      {
        let nodes = range(4).map(i => {
          if i == 2 {
            return node((i * 0.5, 0))[$dots.c$]
          }
          dynkin_node((i * 0.5, 0))
        })

        let syms = range(4).map(i => {
          if i == 2 {
            return
          }
          if i == 3 {
            return node((i * 0.5, 0.3))[$balpha_(n-1)$]
          }
          node((i * 0.5, 0.3))[$balpha_#(i + 1)$]
        })

        (..nodes,).intersperse(edge("-"))
        (..syms,)
      },
      dynkin_node((4 * 0.5, 0)),
      node((4 * 0.5, 0.3), $balpha_n$),
      edge((3 * 0.5, 0), (4 * 0.5, 0), "="),
    ),
    caption: [Dynkin diagram of $B_n = lie(s o)(2n+1)$],
  )

  === Coincidence

  $
    & lie(s o)(3;bb(C)) = lie(s l)(2;bb(C)) = lie(s p)(2;bb(C)) \
    & lie(s o)(4;bb(C)) = lie(s l)(2;bb(C)) plus.o lie(s l)(2;bb(C)) \
    & lie(s o)(5;bb(C)) = lie(s p)(4;bb(C)) \
    & lie(s o)(6;bb(C)) = lie(s l)(4;bb(C)) \
  $
]

===

$#lie[su(2)] = {X in #lie[gl] (2,bb(C)) | overline(X)^t + X = 0, "Tr"(X) = 0}$ and $#lie[so(3)]$ are all real lie algebras of dimension 3.

(a) The basis:

$
  xi_1 = 1/2mat(0, i; i, 0), quad xi_2 = 1/2mat(0, -1; 1, 0), quad xi_3 = 1/2mat(i, 0; 0, -i)
$

With $[xi_k, xi_l] = epsilon_(k l m) xi_m$.

$
  xi^2 = xi_1^2 + xi_2^2 + xi_3^2 \
$
$
  [xi^2, xi_k] = 0
$

We construct a commute element which the maximal diagonalized state is #ket($b,m$).

$
  xi^2 #ket($b,m$) = b #ket($b,m$) \
  xi_3 #ket($b,m$) = m #ket($b,m$) \
$

$
  xi^+ = xi_1 + i xi_2, quad xi^- = xi_1 - i xi_2 \
$
$
  [xi_3, xi^+] = xi^+, quad [xi_3, xi^-] = - xi^- \
$
$
  [xi^+, xi^-] = 2 xi_3 \
$

$
  xi_3 xi^(plus.minus) #ket($b,m$) = [xi_3, xi^(plus.minus)] #ket($b,m$) + xi^(plus.minus) xi_3 #ket($b,m$) = (m plus.minus 1) xi^(plus.minus) #ket($b,m$) \
$

Thus we conclude that $xi^(plus.minus) #ket($b,m$) = C #ket($b,m plus.minus 1$), quad C in bb(C)$, and $xi_3 #ket($b,m plus.minus 1$) = (m plus.minus 1) #ket($b,m plus.minus 1$)$.

We call such operators ladder operators or raising and lowering operators.

$
  xi^+ #ket($b,j$) = 0 quad exists j in thick?
$

$
  xi^minus xi^+ = (xi_1 - i xi_2)(xi_1 + i xi_2) = xi_1^2 + xi_2^2 + i[xi_1, xi_2] = xi^2 - xi_3^2 + xi_3 \
$

$
  0 = xi^- xi^+ #ket($b,j$) = (b - j^2 + j) #ket($b,j$) -> b = j(j+1)\
$

Same for $xi^+ xi^-$, one has $b - j'^2 + j' = 0$

$
  b = j'(j' - 1) = - j' (-j' + 1) \
  -> j' = -j \
$
We conclude that for $m$ can be $-j, -j+1, dots.c, j-1, j$, thus $2j in bb(N)$ is a integer for finite dimension.

$
  & j = 0, quad m = 0, quad j(j+1) = 0 \
  & j = 1/2, quad m = 1/2, -1/2, quad j(j+1) = 3/4 \
  & j = 1, quad m = 1,0,-1, quad j(j+1) = 2 \
  & dots.c
$

From the definition of $xi^+ = xi^-^dagger$ by its expansion, we have such normalization factor:

$
  #braket($b,m$, $xi^+^dagger xi^+$, $b,m$) & = #braket($b,m$, $xi^- xi^+$, $b,m$) \
                                            & = #braket($b,m$, $xi^2 - xi^2_3 - xi_3$, $b,m$) \
                                            & = b - m^2 -m = j(j+1) -m^2 -m = C^2 \
$

$
  C = sqrt(j(j+1) - m(m+1)) \
$

Same, one has for $xi^-$ that $tilde(C) = sqrt(j(j+1) - m(m-1))$.

===

Take the transformation $S O (3)$ as $G L (3;bb(R))$ matrix representation act naturally on $bb(R)^3$ equipped with function valued on it as a scalar form.
$
  l_1 (f)(bold(x)) = f (l^(-1)_1 x) & = d/(d t) f(exp(
                                          t mat(
                                            0, 0, 0;
                                            0, 0, 1;
                                            0, -1, 0;
                                          )
                                        ) vec(x_1, x_2, x_3))|_(t=0) \
                                    & = dv(, t) f(mat(
                                          1, 0, 0;
                                          0, cos t, sin t;
                                          0, -sin t, cos t;
                                        ) vec(x_1, x_2, x_3))|_(t=0) \
                                    & = dv(, t) f(vec(
                                          x_1,
                                          x_2 cos t + x_3 sin t,
                                          - x_2 sin t + x_3 cos t,
                                        )) \
                                    & = (pdv(f, x_1),pdv(f, x_2),pdv(f, x_3)) dot vec(0, x_3, -x_2) \
                                    & = x_3 pdv(f, x_2) - x_2 pdv(f, x_3)
$

If we have $x_1 = r sin theta cos phi.alt, x_2 = r sin theta sin phi.alt, x_3 = r cos theta$, we can construct the transformation upon $theta,phi.alt$ too.

$
  pdv(, x_i) = pdv(r_i, x_i) pdv(, r_i) \
$

In differential geometry as a basis vector transformation, or familiar Jacobi.

$
  & l_1 = x_3 pdv(, x_2) - x_2 pdv(, x_3) = sin phi.alt pdv(, theta) + cot theta cos phi.alt pdv(, phi.alt) \
  & l_2 = - cos phi.alt pdv(, theta) + cot theta sin phi.alt pdv(, phi.alt) \
  & l_3 = - pdv(, phi.alt)
$

$
  & l^+ = e^(- i phi.alt) (-i pdv(, theta) + cot theta pdv(, phi.alt)) \
  & l^- = e^(i phi.alt) (i pdv(, theta) + cot theta pdv(, phi.alt))
$

Given the representation $F(theta,phi.alt)(m)$ with the weight $m$ chosen by $l_3$, with the highest weight denoted as $l$:

$
  l_3 F(theta,phi.alt)(m) = - pdv(, phi.alt) F(theta,phi.alt)(m) = m F(theta,phi.alt)(m)
$

Thus we have $F(theta,phi.alt) ~ e^(m phi.alt) G (theta)$, however, we have such restriction $phi.alt + 2 pi ~ phi.alt$, thus we must have $m -> i m$ to match such period.

We can immediately decompose the representation scalar function by raising operator for the highest weight:
$
  (pdv(, theta) - l cot theta) G (theta)(l) & = 0 \
                             ln G(theta)(l) & = l ln sin theta \
            G(theta)(l) = C_(l) sin^l theta
$

Where the constant is, for the representation of $2 l + 1$ dimension in $l$ weight. Apply lowering operator would giving us:

$
  F(theta,phi.alt)(m) &= C_m (l^-)^(l-m) F(theta,phi.alt)(l) \
  &= C_m (e^(-i phi.alt) (i pdv(, theta) + cot theta pdv(, phi.alt)))^(l-m) e^(-i l phi.alt) sin^l theta \
$

However, one usually encompass the whole $2l+1$ representation for arbitrary $l$ as:

$
  Y_l^m (theta,phi.alt) = C_(l m) (dots.c) thick "as representation for" 2l+1 "dimension with weight" m
$

Casimir operator with commutative property acting on will give us the eigenvalue.
$
  l^2 = l_1^2 + l_2^2 + l_3^2 \
$

$
  l^2 Y_l^m (theta, phi.alt) = l(l+1) Y_l^m (theta, phi.alt)
$

$
  l^2 &= l^-l^+ + i l_3 + l_3^2 \
  &= e^(i phi.alt)(i pdv(, theta) + cot theta pdv(, phi.alt)) e^(-i phi.alt)(-i pdv(, theta) + cot theta pdv(, phi.alt)) - i pdv(, phi.alt) + pdv(, phi.alt, 2) \
  &= pdv(, theta, 2) + i pdv(, theta)(cot theta pdv(, phi.alt)) + e^(i phi.alt) cot theta pdv(, phi.alt) (e^(- i phi.alt) (-i pdv(, theta))) + e^(i phi.alt) cot theta pdv(, phi.alt) (e^(-i phi.alt) cot theta pdv(, phi.alt)) + (dots.c) \
$

Evaluate that:

$
  i pdv(, theta)(cot theta pdv(, phi.alt)) = i/(sin^2 theta) pdv(, phi.alt) + i cot theta pdv(, theta, phi.alt) \
  e^(i phi.alt) cot theta pdv(, phi.alt) (e^(- i phi.alt) (-i pdv(, theta))) = - cot theta pdv(, theta) - i cot theta pdv(, theta, phi.alt) \
  e^(i phi.alt) cot theta pdv(, phi.alt) (e^(-i phi.alt) cot theta pdv(, phi.alt)) = -i cot^2 theta pdv(, phi.alt) + cot^2 theta pdv(, phi.alt, 2)
$

The first term evaluate as:

$
  "First term" &= pdv(, theta, 2) - cot theta pdv(, theta) + i(1/(sin^2 theta) pdv(, phi.alt) - cot^2 theta pdv(, phi.alt)) + cot^2 theta pdv(, phi.alt, 2)\
  &= pdv(, theta, 2) - cot theta pdv(, theta) + i pdv(, phi.alt) + cot^2 theta pdv(, phi.alt, 2)
$

$
  "LHS" &= pdv(, theta, 2) - cot theta pdv(, theta) + cot^2 theta pdv(, phi.alt, 2) + pdv(, phi.alt, 2) \
  &= 1/(sin theta) (pdv(, theta) (pdv(, theta)) sin theta + pdv(, theta) (sin theta) pdv(, theta) ) + 1/(sin^2 theta) pdv(, phi.alt, 2) \
  &= 1/(sin theta) pdv(, theta) (sin theta pdv(, theta)) + 1/(sin^2 theta) pdv(, phi.alt, 2) = Delta_(Omega)
$

Which is the *Spherical Laplacian*#footnote[Actually, calculate by $l_1^2 + l_2^2 + l_3^2$ is more simpler, or use some notation reduction would be easier in burden.].

This, actually can be formalize in such insight, that Laplacian as:
$
  pdv(, x_1, 2) + pdv(, x_2, 2) + pdv(, x_3, 2) = Delta_Omega \
$

Is rotation invariant given by $[Delta_Omega, l_i] = 0$. Which is same as Casimir operator by its *uniqueness* up to constant. Thus we decompose $L^2 (S^2)$ into basis equipped with $Y^m_l (theta,phi.alt)$.

===

Given $S O (2)$, it contains one generator which rotates the plane:

$
  l = mat(0, 1; -1, 0) ~ l = x_1 pdv(, x_2) - x_2 pdv(, x_1) = - pdv(, phi.alt)
$

It's simple that only one element share the eigenvalue solely.
$
  l ket(m) = m ket(m) ~ ket(m) = F(phi.alt)(m) = e^(- i m phi.alt)
$
With period condition induced.

$S O (2) times.r bb(R)^+ = E(2)$

$
  mat(R(theta), bold(t); 0^T, 1) = mat(cos theta, sin theta, x; sin theta, cos theta, y; 0, 0, 1)
$

$#lie[e] (2)$
$
  l -> mat(0, -1, 0; 1, 0, 0; 0, 0, 0) quad p_x -> mat(0, 0, 1; 0, 0, 0; 0, 0, 0) quad p_y -> mat(0, 0, 0; 0, 0, 1; 0, 0, 0)
$

$
  [l,p_x] = p_y quad [l,p_y] = - p_x quad [p_x,p_y] = 0
$

$
  & l -> x_1 pdv(, x_2) - x_2 pdv(, x_1) = - pdv(, phi.alt) \
  & p_x -> pdv(, x) \
  & p_y -> pdv(, y) \
$

Given a Cartan subalgebra, we choose $l$, because the Cartan subalgebra must be a semi-simple decomposition thus we shouldn't take a nilpotent ideal which would *vanish in commutation*.

$
  p^(plus.minus) := p_x plus.minus i p_y = pdv(, x) plus.minus i pdv(, y) = e^(plus.minus i phi.alt) (pdv(, r) plus.minus i/r pdv(, phi.alt)) \
$

$
  [l,p^(plus.minus)] = plus.minus p^(plus.minus) quad [p^+,p^-] = 0
$

Casimir

$
          p^+ p^- - p^+ p^- & = 0 \
  [l,p^+] p^- + p^+ [l,p^-] & = 0 \
                [l,p^+ p^-] & = 0 \
         [l, p_x^2 + p_y^2] & = 0 \
                   [l, p^2] & = 0
$

Thus, it's the Casimir operator, why there's no $l^2$? Because there's no element can generate $l$ to absorb in. Thus we clarify such operator should be unique up to scalar, which is $Delta_perp$ in representation.

$
  p^+ p^- & = e^(i phi.alt) (pdv(, r) + i/r pdv(, phi.alt)) (e^(- i phi.alt))(pdv(, r) - i/r pdv(, phi.alt)) \
$

$
    & e^(i phi.alt)(pdv(, r) + i/r pdv(, phi.alt)) (e^(- i phi.alt) B) \
  = & pdv(, r) B + 1/r B + i/r pdv(, phi.alt) B
$

$
  p^+ p^- &= pdv(, r, 2) - i/r pdv(, r, phi.alt) + i/r^2 pdv(, phi.alt) + 1/r pdv(, r) - i/r^2 pdv(, phi.alt) + i/r pdv(, phi.alt, r) + 1/r^2 pdv(, phi.alt, 2) \
  &= pdv(, r, 2) + 1/r pdv(, r) + 1/r^2 pdv(, phi.alt, 2)
$

We inspect that the commutation relation differs from the case in semi-simple algebra like $S U (2)$, which we can't generate the angular part from the translation. If you review the proof of weight boundedness of $S U(2)$ representation that Casimir operator build the connection with maximal and minimal weight, however, we can't reach the results in this one, indicating _unboundedness_ of the weight.

$
  p^(plus.minus) F(r,phi.alt,z)(m,k_z) = e^(plus.minus i phi.alt)(pdv(, r) plus.minus i/r pdv(, phi.alt)) F(r,phi.alt,z)
$

$
  Delta_perp = pdv(, x, 2) + pdv(, y, 2) = pdv(, r, 2) + 1/r pdv(, r) + 1/r^2 pdv(, phi.alt, 2) = p^2 \
$

Given by weight $m$, we extract terms like $e^(i m phi.alt)$:

$
                   (Delta_perp + partial_z^2) F(r,phi.alt,z)(m,k_z) & = lambda F(r,phi.alt,z)(m,k_z) \
                               Delta_perp (e^(i m phi.alt) R(r)(m)) & = (lambda - k_z^2) (e^(i m phi.alt) R(r)(m)) \
  (pdv(, r, 2) + 1/r pdv(, r) - m^2/r^2 + (k_z^2 - lambda)) R(r)(m) & = 0
$

Which is called _Bessel Equation_, the solution is called _Bessel Function_ $J_m (r)$ with $m$ as weight notation. Notice that $k_z^2 - lambda$ is a isolated scalar generated from $z$ translation which could be reduced, we denote as $r -> sqrt(k_z^2 - lambda) r := k r$.

$
  G (r,phi.alt)(m) = e^(i m phi.alt) R(r)(m) = J_m (k r) e^(i m phi.alt) \
  p^+ (G(r,phi.alt)(m)) = G(r,phi.alt)(m+1) \
$

$
  J_(m+1) (r) = m/x J_m (r) - J'_m (r)
$

However, we have no choice like $S U(2)$ to denote the minimal or maximal basis function and iterates for else. Thus, we can only acquire a iteration relation like above. You may expect the different solution or _differential seed_ will inherit the same iteration property like above.

$
  [l,p^(plus.minus)] = plus.minus p^(plus.minus) \
  e^(t l) p^(plus.minus) e^(- t l) = e^(t D_l) (p^(plus.minus)) = sum_n^infinity t^(n)/n! (plus.minus 1)^n p^(plus.minus) = e^(plus.minus t) p^(plus.minus) \
$

We then set $t -> i phi.alt$ for period restriction.

$
  U(phi.alt) := e^(i phi.alt l) \
  U(phi.alt) ket(m) = e^(i phi.alt l) ket(m) = e^(i m phi.alt) ket(m)
$

We thus immediately decompose it to the $m$-weight space, recall the representation decomposition, one has $chi(g) = e^(i m phi.alt)$:

$
  1/(2 pi) integral_0^(2 pi) e^(-i m phi.alt) e^(i m phi.alt) d phi.alt = 1_m \
  1/(2 pi) integral_0^(2 pi) e^(- i m phi.alt) U(phi.alt) ket(m) d phi.alt = 1_id \
  1/(2 pi) integral_0^(2 pi) e^(- i m phi.alt) U(phi.alt) d phi.alt = Pi_m \
$

$
  "Tr" (U(phi.alt)) = braket(m, U(phi.alt), m) = sum_(m in bb(z)) e^(i m phi.alt) = 2 pi sum_(m in bb(z)) delta(phi.alt - 2pi n) = sum_m Pi_m = 1_id \
$

$
  sum_m Pi_m (e^(i k r cos phi.alt)) = sum_(m in bb(z)) J_m (k r) e^(i m phi.alt)
$

==

$
  S[*]: cal(F) -> bb(R); cal(F) = { bold(q)(t): t in [t_0,t_1] subset bb(R) -> bb(R)^M }
$

With differential set if applicable:

$
  cal(F)_epsilon = {delta bold(q)(t); abs(delta bold(q)(t)) < epsilon; abs(delta bold(dot(q))(t)) < epsilon; forall t in [t_0,t_1] subset bb(R)}
$

$
  delta S(bold(q),bold(dot(q))) = 0 -> delta bold(q)(t_0) = delta bold(q)(t_1) = 0
$

Given by a certain basis product form:
$
  ket(x) "or" ket(x + delta)? -> "continuous basis" \
  braket(x, psi) = braket(x, x') braket(x', psi)
$

Thus $phi$ should be a continuous basis expansion for the representation of coordinates:
$
  integral d mu thin phi(x|x') <-> braket(x, x') \
  integral d mu thin phi(x|x') phi(x'|x_0) <-> braket(x, x') braket(x', x_0) = braket(x, x_0) <-> delta(x'|x_0)
$

$
  phi(x|x_0) = phi(x|x_(N-1)) phi(x_(N-1)|x_(N-2)) dots.c phi(x_1|x_0) \
  phi(x|x_0) = lim_(N->infinity) product^(infinity) T(phi(x_epsilon))
$

Denotes $M(V;bb(C))$ as set of non-degenerate complex-valued symmetric bilinear forms on $V$ with non-negative definite real part, with dense set $M^circle.small (V;bb(C))$. Now fix a translation invariant volume form $d x$ on $V$, thus we can define the determinant $det(B) thick B in M^circle.small (V;bb(C))$.

Let $cal(S)(V)$ be the _Schwartz space_ of $V$ where the smooth functions on $V$ whose all derivatives are rapidly decaying at $infinity$ faster than any power of $abs(x)$, equipped with the dual space $cal(S)^*(V)$ in natural inclusions $cal(S)(V) subset L^2(V) subset cal(S)'(V)$.

$
  cal(F): cal(S)(V) -> cal(S)(V^*) \
  cal(F)[g](p) = (2pi)^(-d/2) integral_V g(x) e^(-i innerproduct(p, x)) d x
$

Isometry is given by $cal(F)^2[g](x) = g(-x)$. By duality, such operator could be extended to $cal(S)^*(V) -> cal(S)^*(V^*)$ for tempered distribution. The function $exp(-1/2 B(x,x))$ for matrix $B in M^circle.small (V)$ belongs to $cal(S)^*(V)$ if $Re B >= 0$ by its decaying behavoir.

For dimension 1, where a diagonalizable $B$:
$
  cal(F)(exp(-1/2 B(x,x))) &= (2pi)^(-1/2) integral_(-infinity)^(infinity) exp(-i p x - 1/2 a x^2) d x \
  &= (2 pi)^(-1/2) exp(-1/2 a^(-1) p^2) integral_(-infinity)^(infinity) exp(-1/2 a(x+i a^(-1)p)^2) d x \
  &= (2 pi)^(-1/2) exp(-1/2 a^(-1) p^2) integral_(bb(R) + i a^(-1)p) exp(-1/2 a(x+i a^(-1)p)^2) d x \
  &= a^(-1/2) exp(-1/2 a^(-1) p^2)
$

We therefore could extend such matrix to diagonalizable by dense property that for arbitrary countable dimensions where a general results is given by:

$
  cal(F)(exp(-1/2 B(x,x))) = (det B)^(-1/2) exp(-1/2 B^(-1) (p,p))
$

That the $det(B)^(-1/2) = product_i lambda_i$ by eigenvalues which is trivial in dimension 1.

$
  I[g;B] (hbar) & = 1/hbar^(1/2) integral_V g(x) e^(-1/(2 hbar) B(x,x)) d x quad hbar >= 0 \
                & = integral_V g(hbar^(1/2) x) e^(-1/2 B(x,x)) d x quad x -> x/(hbar^(1/2))
$

$
  I[g;B] (0) = integral_V (dots.c) d x thick g(0) = (2pi)^(d/2) (det B)^(-1/2) g(0)
$

$
  I[g;B] (planck) & = innerproduct(g(planck^(1/2)x), exp(-1/2 B(x,x))) \
                  & = planck^(-d/2) (det B)^(-1/2) innerproduct(cal(F)[g](planck^(-1/2)p), exp(-1/2 B^(-1)(p,p))) \
                  & = (det B)^(-1/2) innerproduct(cal(F)[g](p), exp(- planck/2 B^(-1)(p,p))) \
$

Where $planck -> 0 ~> exp(-planck/2 B^(-1)(p,p)) = 1$.

If $l in V^*$ and $g in cal(S)(V)$, then:

$
  I[l g;B] (planck) & = innerproduct(l(planck^(1/2) x) g(planck^(1/2)x), exp(-1/2 B(x,x))) \
                    & = planck^(1/2) innerproduct(g(planck^(1/2)x), l(x) exp(-1/2 B(x,x))) \
                    & = - planck^(1/2) innerproduct(g(planck^(1/2)x), partial_(B^(-1) l) exp(-1/2 B(x,x))) \
                    & = planck^(1/2) innerproduct(partial_(B^(-1) l) g(planck^(1/2)x), exp(-1/2 B(x,x))) \
                    & = planck innerproduct((partial_(B^(-1)l) g) (planck^(1/2) x), exp(-1/2 B(x,x))) \
                    & = planck I [partial_(B^(-1) l) g;B] (planck)
$

$
  dv(, planck) (g(planck^(1/2) x)) = 1/2 planck^(-1/2) (x^* dot partial_(planck^(1/2) x) g)(planck^(1/2) x) = 1/2 planck^(-1/2) planck^(-1/2) (x^* dot partial_x g)(planck^(1/2) x) = 1/2 planck^(-1) (x^* dot partial_x g)(planck^(1/2) x)
$

Where $x^*$ is the covector compared to vector $x$. Compose two results we get a Laplacian operator:

$
  I' [g;B] (planck) = 1/2 planck^(-1) I [x^* dot partial_x g] (planck) = 1/2 planck^(-1) planck I [partial_(B^(-1) x^*) dot partial_x g)] (planck) = I [1/2 Delta_B g;B] (planck)
$

By deduction, we can apply as much as possible that:

$
  I^(\(n\))[g;B](planck) = I[(1/2 Delta_B)^n;B](planck)
$

If moreover $g$ vanishes at the origin to order $2n+1$, then for every differential operator of order $<= 2n$ annihilates $g$ at $0$, hence:

$
  I_g (0) = I'_g (0) = dots.c = I_g^(\(n\))(0) = 0
$

Assume $f$ attains a global minimum at a unique point $c in [a,b]$, s.t. $a<c<b$ and $f''(c)>0$. To acquire more information, we could expand the function as:

$
  f(x) = f(c) + 1/2 f''(c) (x-c)^2 + dots.c \
$

Or even better to take a variable transformation with equality by rescale and shift:

$
  c -> 0 quad f(c) = 0 ~> f(x) = M/2 x^2 \
$

If given a compact support that ${c} in U$ where divide the function as $g = g_1 + g_2 quad g_1 subset U, g_2 subset [a,b]\\U$. Hence the integral of second term will rapidly decaying if we choose a enough huge neighborhood support around $c$. We left with the first term as:

$
  I[g](planck) = integral_(-infinity)^(infinity) g(planck^(1/2) y) e^(-M/2 y^2) d y
$

$
  planck^(1/2) I [g;f] = integral_a^b g(x) e^(- f(x)/planck) d x = planck^(1/2) e^(-f(c)/planck) I[tilde(g);B = (dot)^2]
$

It actually show a general strategy to expand the integral by:

$
  c = 0 quad f(x) = 1/2 p(x)^2 \
  p'(0) = sqrt(f''(0)) > 0 \
$

$
  integral_(-infinity)^(infinity) g(x) e^(-p(x)^2/(2 planck)) d x ~ planck^(1/2) integral_(-infinity)^(infinity) tilde(g)(planck^(1/2) y) e^(-y^2/2) d y
$

$
  & p(x)/(planck^(1/2)) = y \
  & d x = d p^(-1)(planck^(1/2) y) = (p^(-1))' (planck^(1/2) y) planck^(1/2) d y \
$
$
                    p(p^(-1)(x)) & = x \
  p'(p^(-1)(x)) dot (p^(-1))'(x) & = 1 \
                    (p^(-1))'(x) & = 1/(p'(p^(-1)(x))) \
$
$
  tilde(g)(y) := g(p^(-1)(y)) thin (p^(-1))' (y) = g(p^(-1)(y))/(p'(p^(-1)(y)))
$

We could expand $tilde(g)$ by Taylor polynomials to acquire a series of summation.

Notice that any odd order polynomials expansion will vanish due to the whole space integral. Thus we can freely expand in $O(planck^n)$ order as:

$
  planck^(1/2) I[g;f] = planck^(1/2) e^(- f(c)/planck) I[tilde(g);B] = (2pi planck)^(1/2) e^(-f(c)/planck) sum_(n>=0) a_n planck^n
$

The Gaussian integral can be expanded as $integral_(-infinity)^(infinity) y^(2m) e^(-y^2/2) d y = (2pi)^(1/2) (2m-1)!!$, So we can exploit the constant that $tilde(g)(y) = sum_(n>=0)^(infinity) b_n y^n -> a_n = b_(2n) (2m-1)!!$.

$
  integral_a^b g(x) e^((i f(x))/planck) d x = planck^(1/2) e^((i f(c))/planck) e^((plus.minus pi i)/4) I[g](planck)
$

$
  I(planck) = sum_(n>=0) a_n planck^n &= sum_(n>=0) a_n planck^n/n! n! \
  &= sum_(n>=0) a_n planck^n/n! integral_0^infinity u^n e^(- u) d u \
  &= integral_0^infinity g(planck u) e^(-u) d u quad g(planck) = sum_(n>=0) a_n (planck^n)/n! \
  &= integral_(-infinity)^(infinity) abs(v) g (planck v^2) e^(-v^2) d v quad u -> v^2 \
  &= planck^(-1/2) integral_(-infinity)^(infinity) tilde(g) (planck^(1/2) v) e^(-v^2) d v quad tilde(g)(v) = abs(v) g(v^2) \
$

$
  Gamma(s+1) & = integral_0^infinity t^s e^(-t) d t quad s > 0 \
             & = s^(s+1) integral_0^infinity x^s e^(-s x) d x quad t -> s x \
             & = s^(s+1) integral_0^infinity e^(-s (x - ln x)) d x quad hbar -> 1/s, f(x) -> x-ln x, g(x) -> 1 \
             & = s^(s+1/2) e^(-s) (2pi)^(1/2) sum_(n>=0) a_n (1/s)^n quad f(c) = f(1) = 1
$

$
  p(x) = sqrt(2 (x-ln x)) & = sqrt(2(x - (x - x^2/2 +x^3/3 + dots.c))) \
                          & = x sqrt(1 - (2x)/3 + x^2/2 + dots.c) = x - x^2/3 + (7x^3)/36 + dots.c
$

$
  p^(-1) (x) = x + x^2/3 + x^3/36 + dots.c \
  (p^(-1))' (x) = 1 + (2x)/3 + (x^2)/12 + dots.c \
$

$
  tilde(g)(y) = p'^(-1) (y) -> a_0 = 1, a_1 = 1/12 (2-1)!! = 1/12 \
$

Multidimensional steepest descent formula:
$
  planck^(d/2) I^D [g;f] = integral_D g(x) e^(-f(x)/planck) d x = planck^(d/2) e^(-f(c)/planck) I[g;B]
$

$
  T -> Pi(T) \
  abs(Pi_k) = ((2k)!)/(2^k k!) = ((2k)!)/((2k)!!) = (2k-1)!!
$

$
  expval(l_1 dots.c l_N) := planck^(d/2) e^(S(c)/planck) integral_D l_1(x) dots.c l_N (x) e^(-S(x)/planck) d x \
$

$
  S(x) = B(x,x)/2 + tilde(S)(x) = B(x,x)/2 - sum_(i>=0) g_i (B_i (x,dots.c,x))/i!
$

$
  Z = I[1;S(x)] = planck^(d/2) integral_V e^(-S(x)/planck) d x
$

$
  vf(n) = (n_0,n_1,n_2,dots.c) \
  F_(Gamma) = product_i g_i^n_i dot tilde(F)_Gamma \
$

$
  x -> y = planck^(-1/2)x \
  B_i (x,dots.c,x) -> planck^(i/2) B_i (x,dots.c,x) \
$

$
  Z = sum_(vf(n)) Z_(vf(n)) \
  Z_(vf(n)) = integral_V e^(- B(y,y)/2) product_i g_i^n_i/((i!)^(n_i) n_i !) (planck^(i/2-1) B_i (y,dots.c,y))^(n_i) d y
$

Contract each vertex.

$
  -chi(Gamma) = E(Gamma) - V(Gamma) = 1/2 sum_(i>=0) n_i i - sum_(i>=0) n_i = sum_(i>=0) n_i (i/2 - 1)
$

$
  Z_n = (2pi)^(d/2) (det B)^(-1/2) product_i g_i^n_i/((i!)^(n_i) n_i !) sum_(sigma in product(T_vf(n))) tilde(F)(sigma)
$

+ permutation of "flowers" of given valency: $S_(n_i)$
+ permutation of the $i$th edges inside each $i$-valent "flower": $S^(n_i)_i$

$
       bb(G)_vf(n) & = product_i (S_(n_i) times.l S_i^(n_i)) \
  abs(bb(G)_vf(n)) & = product_i (n_i !)(i!)^(n_i)
$

The group $bb(G)_vf(n)$ acts on the set $Pi(T_vf(n))$, which the stabilizer of a given matching is $"Aut"(Gamma)$.

$
  N_Gamma = (product_i (n_i !)(i!)^(n_i))/(abs("Aut"(Gamma))) \
$

$
  sum_(sigma in Pi(T_vf(n))) tilde(F)(sigma) = sum_Gamma (product_i (n_i !)(i!)^(n_i))/(abs("Aut"(Gamma))) F_Gamma = sum_Gamma N_Gamma tilde(F)_Gamma
$

$
  chi(Gamma) & = beta_0(Gamma) - beta_1(Gamma) = V - E \
$
$
  Z = sum_(vf(n)) Z_vf(n) = (2pi)^(d/2) (det B)^(-1/2) sum_(vf(n)) product_i (g_i planck^(i/2 - 1))^(n_i) sum_(Gamma in G(vf(n))) tilde(F)_Gamma/(abs("Aut"(Gamma))) \
$

We know that such exponential can be expanded as infinite sum of expectation of products.

$
  expval(e^l) := sum_(n>=0) 1/n! expval(l^n) = planck^(d/2) integral_V e^(l(x)-S(x)/planck) d x
$

We immediately inspect that the infinite sum of $Z_vf(n)$ is exact the same as the exponential expansion of $Z$, a specific case for $B_1(dot) = l(dot)$ as the external vertices plus a arbitrary action of $S(x)/planck$ to induce the Feynman amplitude for $F_Gamma (l_1,dots.c,l_N) thick Gamma in G(vf(n))$.

Given below diagram, one have two external vertices and a loop, also with a 3-valent flower and 4-valent flower too.

#let dig_node(pos) = node(pos, radius: 2pt, stroke: 0.5pt)
#figure(
  diagram(
    spacing: 4em,
    dig_node((0, 0)),
    dig_node((1, 0)),
    edge((0, 0), (1, 0)),
    edge((1, 0), (2, 0), bend: 90deg),
    edge((2, 0), (1, 0), bend: 90deg),
    dig_node((3, 0)),
    dig_node((4, 0)),
    dig_node((5, 0)),
    edge((3, 0), (4, 0)),
    edge((3, 0), (4, 0), bend: 90deg),
    edge((4, 0), (3, 0), bend: 90deg),
    edge((4, 0), (5, 0)),
  ),
  caption: [A graph with separated components.],
)

$
  & B_3 = sum_i b^1_i times.o b^2_i times.o b^3_i \
  & B_4 = sum_j c^1_j times.o c^2_j times.o c^3_j times.o c^4_j \
$

In expansion of $B_3$ and $B_4$ exponential will generate the 3-valent and 4-valent flowers, plus two external vertices $l_1,l_2$, all which will be contracted by the edges $B_2$.

$
  F_Gamma (l_1,l_2) = sum_i B^(-1)(l_1,b_i^1) B^(-1) (b_i^2,b_i^3) sum_(i j) B^(-1) (b_i^1,c^1_j) B^(-1) (b_i^2,c^2_j) B^(-1) (b_i^3,c^3_j) B^(-1) (c^4_j,l_2)
$

Suppose the coefficients $g_i = 1$, we acquire the general expression for expectation as sum of all possible graphs:

$
  expval(l_1 dots.c l_N) = sum_(Gamma in G(N)) planck^(-chi(Gamma))/(abs("Aut"(Gamma))) tilde(F)_Gamma (l_1,dots.c,l_N)
$

Where we reduce the product of $product_i (g_i hbar^(i/2-1))$ in $hbar^(-chi(Gamma))$ by the Euler characteristic.

Now, suppose in $1$-dimension, given a examples as simple as possible that $B(y,y) = y^2$, $B_i = z^i$, $g_i = g$, $hbar = 1$:

$
  Z = (2pi)^(-1/2) integral_(-infinity)^(infinity) exp(- y^2/2 + g sum_(i>=0) (z x)^i/i!) d y = (2pi)^(-1/2) integral_(-infinity)^(infinity) exp(- y^2/2 + g e^(z x)) d y \
$

It actually contains infinite many vertices with arbitrary *valency*, we expand the second term $g e^(z x)$:

$
  Z = (2pi)^(-1/2) integral_(-infinity)^(infinity) exp(- y^2/2) sum_(n>=0) (g e^(z y))^n/n! d y = (2pi)^(-1/2) sum_(n>=0) g^n/n! integral_(-infinity)^(infinity) exp(-y^2/2 + n z y) d y \
$

We can explain that $z(dot)$ pair a vertex, thus $n$ vertices will contribute $n$ factors of $z$ as $z(dot) + z(dot) + dots.c$:

$
  integral exp(-y^2/2 + n z y) d y = exp((n^2 z^2)/2) integral exp(-1/2(y-n z^2)) d y = (2pi)^(1/2) exp((n^2 z^2)/2)
$

$
  Z = sum_(n>=0) g^n/n! exp((n^2 z^2)/2) = sum_(n>=0) g^n/n! sum_(k>=0) (n^2 z^2/2)^k/k! = sum_(n,k>=0) (g^n n^(2k))/(2^k k! n!) z^(2k) = sum_(n>=0) g^n sum_(Gamma in G(n)) tilde(F)_Gamma/(abs("Aut"(Gamma)))
$

Given a number of vertices $n$ with contribution $z y$ to each $B^(-1) (z y,z y) = z^2 B^(-1) (y,y) = z^2$. Thus a general graph with $k$ edges contribute $F_Gamma = z^(2 k) times (B^(-1))^k = z^(2k)$. It can also be evaluated by expanding $exp(n z y)$ then integrating. Therefore, we can identify the $abs("Aut"(Gamma))$ too:

$
  sum_(Gamma in G(n)) (dots.c) = sum_k sum_(Gamma in G(n;k)) 1/(abs("Aut"(Gamma))) = n^(2k)/(2^k k! n!)
$

To scrutinize our answer in combinatorics, we pick out two vertices from $n$ vertices with $n^2$ choice with order. For list of $k$ edges, we have $n^2 dot n^2 dot dots.c = n^(2 k)$ choices. To cancel out the order, we first remove orientation of edges which contribute $2 dot 2 dot 2dots.c = 2^k$ choices. Then we reomove the permutation of edges #footnote[It should also be considered as the contraction order from $1$ to $k$, so if we pick out $(a_1,b_1), (a_2,b_2)$, it's also reasonable to pick out $(a_2,b_2),(a_1,b_1)$ which remove the contribution of edges order.] which contribute $k!$ choices. We still treats the vertices as labelled, so remove the permutation of vertices which contribute $n!$ choices.

Try to decompose the graph to connected components, we denote $Gamma = union.sq.big_(j=1)^r Gamma_j^(k_j)$ with $vf(k)$ as tuple of number of copies of each connected components.

$
  F_(Gamma_1 union.sq Gamma_2) = F_(Gamma_1) times F_(Gamma_2) \
  chi(Gamma_1 union.sq Gamma_2) = chi(Gamma_1) + chi(Gamma_2) \
  abs("Aut"(Gamma_1^k_1 union.sq Gamma_2^k_2 dots.c union.sq Gamma_r^(k_r))) = product_(j=1)^r abs("Aut"(Gamma_j))^(k_j) k_j !
$

Here $k_j!$ of the third equality comes from the permutation of identical connected components.

Given a connected graph set $G_c (*)$, $Gamma = union.sq.big_(gamma in G_c (*)) gamma^(k_gamma)$ where the index is same as the graph itself for simplicity.

$
  w(Gamma) := (F_Gamma)/(abs("Aut"(Gamma))) product_i (g_i hbar^(i/2-1))^(n_i)\
$

$
  tilde(F)_Gamma/(abs("Aut"(Gamma))) = product_(gamma in G_c (*)) (tilde(F)_gamma/(abs("Aut"(gamma))))^(k_gamma) 1/(k_gamma !) \
$

We decompose the second product $product_i (dots.c)$ too, therefore we reduce the terms as:

$
  w(Gamma) = product_(gamma in G_c (*)) w(gamma)^(k_gamma)/(k_gamma !) \
$

$
  Z = (2pi)^(d/2) (det B)^(-1/2) sum_(vf(n)) sum_(Gamma in G(n)) w(Gamma) = Z_0 sum_(Gamma in G(*)) w(Gamma) quad Z_0 = (2pi)^(d/2) (det B)^(-1/2)\
$

Where we just reduce our previous expansion of $Z$ in a more concise expression.

$
  Z/Z_0 = sum_(Gamma in G(*)) w(Gamma) = sum_(k_gamma) product_(gamma in G_c (*)) w(gamma)^(k_gamma)/(k_gamma !) = exp(sum_(gamma in G_c (*)) w(gamma)) \
$

For any summation of arbitrary graphs in $G(*)$, we can decompose it to connected components with reordering $vf(n) -> vf(k) ~ sum_vf(n) product_i -> sum_(vf(k)) product_gamma$ by counting the flowers into counting the connected components.

$
  ln Z/Z_0 = sum_(gamma in G_c (*)) w(gamma) = sum_(gamma in G_c (*)) tilde(F)_gamma/(abs("Aut"(gamma))) product_i (g_i hbar^(i/2-1))^(n_i (gamma)) = sum_(vf(n)) product_i (g_i hbar^(i/2-1)) sum_(gamma in G_c (vf(n))) tilde(F)_gamma/(abs("Aut"(gamma)))
$

A spanning-tree $T subset Gamma$ contains all $V$ vertices and without any cycles, thus a spanning-tree on $V$ vertices contains exactly $V-1$ edges. Thus the extra edges will contribute exact the same number of loops.

$
  beta_1(Gamma) = 1 - chi(Gamma) = E -V + 1 \
$
$
  beta_0(Gamma) & = 1 "for connected graph" \
  beta_1(Gamma) & = E - V + 1
$

It suggests $planck^(-chi(gamma))$ will contribute in different order of $O(planck)$. For *tree*, $beta_1 = 0$, thus a connected graph contribute $-chi(gamma) = -(V-E) = - (beta_0 - beta_1) = - 1 ~ O(planck^(-1))$ order. For *1-loop* graph, $beta_1 = 1$, thus contribute $O(planck)$ order, and so forth. Given a set of classes of graphs with *$j$* loops:

$
  planck^(j-1) (ln Z/Z_0)_j := sum_vf(n) product_i g_i^(n_i (gamma)) planck^(j-1) sum_(gamma in G_c (vf(n))) tilde(F)_gamma/(abs("Aut"(gamma)))
$

$
  ln Z/Z_0 = sum_(j>=0) (ln Z/Z_0)_j planck^(j-1)
$

$
  Z := planck^(-d/2) integral_V e^(-S(x)/planck) d x = e^(- S(x_0)/planck) I [1;B = B_2] = e^(- S(x_0)/planck) (det B)^(1/2) det(S''(x_0))^(-1/2) sum_(i>=0) a_i planck^i \
$

By steepest descent formula in the neighborhood of critical point $x_0$ where $S'(x_0) = 0$.

$
  log Z/Z_0 = - S(x_0)/hbar + 1/2 log det(B)/det(S''(x_0)) + log (sum_(i>=0) a_i hbar^i) \
$

Often, the first term is called _classical approximation_ by physicists, the second term is called _1-loop approximation_ etc.

$
  S'(x) &= 0 \
  (1/2 B(x,x) - sum_(i>=3) g_i B_i (x,dots.c,x)/i!)' = B(x, dot) - sum_(i>=3) g_i (B_i (x,dots.c,x,dot))/(i-1)! &= 0 \
  sum_(i>=3) g_i B^(-1) (B_i (x,dots.c,x,dot))/((i-1)!) := beta(x) &= x quad B^(-1): V^* -> V\
$

In the sense of power series norm, $beta$ is a contraction mapping in a neighborhood of $0$.

$
  x_0 = lim_(n->infinity) beta^(n)(x) \
$

- Each application of $beta$ produces a new *vertex* with $i-1$ incoming arguments and one outgoing edge.
- $B^(-1)$ contracts the open leg (argument of the slot $B(x,dots.c,-)$) with the upper vertex.

$
  x^(2) = beta(x^(1)) = sum_i g_i B^(-1) (B_i (x^(1),dots.c,x^(1)))/((i-1)!) \
$

$
  x_0 = sum_(vf(n)) product_i (g_i hbar^(i/2-1))^(n_i) sum_(Gamma in G^(0)(vf(n))) tilde(F)_T/(abs("Aut"(T)))
$

Where the graph $Gamma$ is a _tree_ with one external vertex. Take the convergence results $x_0$ back to the action $S(x) -> S(x_0)$. To explain this, $B(x_0,x_0)/2$ corresponds to gluing two trees with both single external vertices; $1/i! B_i (x_0,dots.c,x_0)$ corresponds to gluing $i$ trees with external vertices together into a $i$-valent flower. We can think of the first term as counting tree $E$ times (once per edge), and rest of terms as counting each tree $V$ times (once per vertex), therefore $-S(x_0) = V - E = 1$ (per tree). So the tree summation contribution is $-S(x_0)$.

$
  S(x) := x^2/2 - g h(x) quad h(x) = sum_(n>=0) c_n x^n "with" c_1 != 0 quad g "is constant"
$

$
                               S'(x) & = 0 \
                                 x_0 & = g h' (x_0) \
                       x_0/(h'(x_0)) & = g \
  (x_0/(h'(x_0)))^(-1) x_0/(h'(x_0)) & = (x_0/h'(x_0))^(-1) (g) \
                                 x_0 & = f (g) quad (x_0/(h'(x_0)))^(-1) = f \
$

$
  -S(x_0) = F(g) = - f(g)^2/2 + g h (f(g))
$

$
  F'(g) = - f(g) f'(g) + h(f(g)) + g h'(f(g)) f'(g)
$

But $x_0 = g h'(x_0) -> f(g) = g h'(f(g)) -> h'(f(g)) = f(g)/g$, first and third terms cancel each other.

$
  F'(g) = h (f(g)) -> -S(x_0) = integral_0^g h(f(a)) d a
$

Consider $B_i = 1, g_i = g$ with $S(x) = x^2/2 - g e^x$, expanding $e^x$ will give the all flowers or external edges for us to compute the number of trees.

$
  sum_(n>=0) g^n sum_(gamma in G^(0)_c (n)) 1/(abs("Aut"(gamma))) = - S(x_0)
$

$
  S'(x) = 0 -> x = g e^x -> x_0 = f(g) = (x/e^x)^(-1) (g)
$

$
  f(x)/e^(f(x)) = x -> e^(f(x)) = f(x)/x
$

$
  -S(x_0) = integral_0^g h(f(a)) d a -> integral e^(f(a)) d a -> integral f(a)/a d a
$

Now we need to evaluate the coefficients of Taylor series of $f(x)$ to acquire the count of summation of automorphism class of graphs.

$
  f(g) = sum_(n>=1) a_n g^n \
  a_n = 1/(2pi i) integral.cont f(g)/(g^(n+1)) d g ->^(g -> f^(-1)(x)) 1/(2pi i) integral.cont x/(x e^(-x))^(n+1) d (x e^(-x)) = 1/(2pi i) integral.cont e^(n x) (1-x)/(x^n) d x
$

We take residue in a simpler way, expand $e^(n x) = sum_(i>=0) (n x)^i/i!$, we immediately see the residue equal to $n^i/i! x^(i - k) quad i - k = -1$. Therefore $k = n "or" n-1$, we get:

$
  a_n = n^(n-1)/(n-1)! - n^(n-2)/(n-2)! = n^(n-2)/(n-1)!
$

$
  -S(x_0) = integral_0^a f(a)/a d a = sum_(n>=1) n^(n-2)/(n-1)! integral_0^g a^(n-1) d a = sum_(n>=1) n^(n-2)/n! g^n
$

$
  -S(x_0) = sum_(n>=1) n^(n-2)/n! g^n & = sum_(n>=0) g^n sum_(gamma in G_c^(0) (n)) 1/(abs("Aut"(gamma))) \
                           n^(n-2)/n! & = sum_(gamma in G_c^(0) (n)) 1/(abs("Aut"(gamma)))
$

We conclude that the number of labelled tree of $n$ vertices is $n^(n-2)$ as $n!/abs("Aut"(gamma))$ non-isomorphic labellings, The theorem is called _Cayley_ theorem.

Consider now $B_i = 1, g_i = g$ with $S(x) = x^2/2 - g(x + x^3/6)$ which is the set of graphs composed by 1-valent and 3-valent flowers. However, we can directly calculate the fixed point by solving algebraically.

$
  S'(x) = 0 -> x = g (1 + x^2/2) \
  x_0 = (1 - (1-2g^2)^(1/2))/2 \
$

$
  - S(x_0) & = integral_0^g (1-(1-2a^2)^(1/2))/a + (1-(1-2a^2)^(1/2))^3/(6a^3) d a \
           & = integral_0^g 1/(6a^3) (6a^2 - 6a^2(1-2a^2)^(1/2) + 1 + 3 (1-2a^2) - 3 (1-2a^2)^(1/2) - (1-2a^2)^(3/2)) d a \
           & = integral_0^g 1/(6a^3) (4-(6a^2+3+1-2a^2) (1-2a^2)^(1/2)) d a \
           & = 2/3 integral_0^g 1/a^3 (1-(1+a^2)(1-2a^2)^(1/2)) d a quad "integrate by part" d v = 1/a^3 \
           & = 2/3 lr((-1/(2a^2))|)^g_0 - 2/3 lr((1+a^2)(1-2a^2)^(1/2) (-1/(2a^2)) |)_0^g \
           & #h(3em) - 2/3 integral_0^g -1/(2a^2) (2a (1-2a^2)^(1/2) + (1+a^2) dot 1/2 (1-2a^2)^(-1/2) dot (-4a)) d a \
$

We focus on third term in:

$
  d u & = 2 a (1-2a^2)^(1/2) - 2a (1+a^2)(1-2a^2)^(-1/2) \
      & = (2 a (1-2a^2) - 2 a (1+a^2))/(1-2a^2)^(1/2) \
      & = (6a^3)/(1-2a^2)^(1/2)
$

$
  "third term" = integral_0^g (2a)/(1-2a^2)^(1/2) d a = integral_0^g 1/(1-2a^2)^(1/2) d a^2 = -lr((1-2a^2)^(1/2)|)_0^g
$

Combine two terms together:

$
  I & = 1/(3a^2) ((1+a^2)(1-2a^2)^(1/2) - 1 - 3a^2(1-2a^2)^(1/2)) \
    & = 1/(3a^2) ((1-2a^2)(1-2a^2)^(1/2) - 1) \
    & = 1/(3a^2) ((1-2a^2)^(3/2) - 1)
$

$
  lr(I|)^g_0 & = 1/(3g^2)((1-2g^2)^(3/2) - 1) - lim_(a -> 0) 1/(3a^2) (-3a^2) quad "L'Hôpital's Rule" \
             & = 1/(3g^2)((1-2g^2)^(3/2) - 1) + 1
$

$
  -S(x_0) &= 1/(3g^2)((1-2g^2)^(3/2) - 1) + 1 \
  &= 1/(3g^2) sum_(n=0)^(infinity) 1/((n+1)!) 3/2 dot 1/2 dot dots.c dot (3-2n)/2 (-2)^(n+1) g^(2(n+1)) + 1/(3g^2) - 1/(3g^2) + 1 thick "by shift 1 index"\
  &= sum_(n=1)^(infinity) 1/((n+1)!) 1/2 dot dots.c dot (2n - 3)/2 (-1)^(n) (-2)^(n) g^(2n) - 1 + 1 thick "by extract first term" \
  &= sum_(n=1)^(infinity) (1 dot 3 dot dots.c dot (2n-3))/((n+1)!) g^(2n)
$

Now we see each coefficients corresponds to counts of tree with $m = 2n$ vertices, if we multiply $2n$ then corresponds to the one with vertices labelled.

Feynman calculus can be used to count not only oriented but also oriented graphs. Suppose we want to count not labelled oriented trees, how to represent this? Given two labelled point $x,y$ rather $x^2$, the bilinear form is thus $x y$. Identify $x$ as the source of the edge and $y$ as the sink of the edge, we extend all flowers same as before but summation for both: $b e^x + a e^y$. Combine together: $S(x,y) = x y - b e^x - a e^y$. The critical point is the zeros of partial derivative in such 2-dimension manifold.

$
  pdv(S(x,y), x) = y - b e^x = 0 -> b e^x = y \
  pdv(S(x,y), y) = x - a e^y = 0 -> a e^y = x \
$

Such transcendental function can't be solved directly, we expand each coefficients:

$
  & x = a (sum_(i>=0) y^i/i!) = a + sum_(p>=1, q>=1) c_(p,q) a^p b^q \
  & y = b (sum_(i>=0) x^i/i!) = b + sum_(p>=1,q>=1) d_(p,q) a^p b^q
$

Evaluate the coefficient of each order by Cauchy's theorem:

$
  c_(p,q) = 1/(2pi i)^2 integral.cont integral.cont x a^(-(p+1)) b^(-(q+1)) d a and d b
$

$
  d a = e^(-y) (d x - x d y) quad d b = e^(-x) (d y - y d x) \
  d a and d b = e^(-x-y) (d x - x d y) and (d y - y d x) = e^(-x-y) (1 - x y) d x and d y
$

$
  a^(-(p+1)) = x^(-(p+1)) e^((p+1) y), b^(-(q+1)) = y^(-(q+1)) e^((q+1)x)
$

$
  c_(p,q) &= 1/(2pi i)^2 integral.cont integral.cont x x^(-(p+1)) e^((p+1) y) y^(-(q+1)) e^((q+1)x) e^(-x-y) (1-x y) d x and d y \
  &= 1/(2pi i)^2 integral.cont integral.cont (1-x y) x^(-p) y^(-(q+1)) e^(q x + p y) d x and d y \
$

We evaluate $x^(-k) y^(-l) e^(q x + p y)$ to tackle general case:

$
  x^(-k) y^(-l) sum_(i,j>=0) (q x)^i/i! (p y)^j/j! -> i - k = -1, j - l = -1 -> I = q^(k-1)/((k-1)!) p^(l-1)/((l-1)!)
$

$
  c_(p,q) = q^(p-1)/((p-1)!) p^(q)/(q!) - q^(p-2)/((p-2)!) p^(q-1)/((q-1)!) & = (q^(p-1) p^(q) - (p-1) q^(p-2) q p^(q-1))/((p-1)! q!) \ &= ((p - (p-1)) q^(p-1) p^(q-1))/((p-1)! q!) \
  &= (q^(p-1) p^(q-1))/((p-1)! q!)
$

Similarly, $d_(p,q)$ is solved by same strategy while $x <-> y$, thus $p <-> q$, is $(q^(p-1) p^(q-1))/((q-1)!p!)$. Use integral trick to compute $S(x_0,y_0)$, but before on the hand, we decompose:

$
  pdv(S(x_0,y_0), a) = - e^(y_0) = - x_0/a, quad pdv(S(x_0,y_0), a) = - e^(x_0) = - y_0/b
$

Thus we can evaluate the integral of the curve by the total derivative of the action:

$
  - S(x_0,y_0)(a,b) & = integral^(a,b)_(a,0) integral^(a,0)_(0,0) x_0/u d u + y_0/v d v \
                    & = integral_(0,0)^(a,0) (x_0 (u,0))/u d u + integral_(a,0)^(a,b) (y_0 (a,v))/v d v \
                    & = a + integral_0^b (1 + sum_(p>=1, q>=1) d_(p,q) a^p v^(q-1)) d v \
                    & = a + b + sum_(p>=1,q>=1) (q^(p-1) p^(q-1))/(q! p!) a^p b^q
$

Now we see that the number of trees with $p$ sources and $q$ sinks is $(q^(p-1) p^(q-1))/(q! p!)$ labelled for source and sink one, or $q^(p-1) p^(q-1) (p+q)!/(q! p!)$ unlabelled for which is source or sink, or $p^(q-1) p^(q-1)$ if the vertices *in* source and sink are also labelled.

Can we extend the vertex to arbitrary finite labelled choices or colored? For example, the previous case has two color choices for each vertex, then the choice for different color can be considered as source and sink. Therefore we have a tuple of vertex color as $(x_1,dots.c,x_n)$ and their connection edges by $1/2 vf(x)^T B vf(x)$ bilinear form while the previous case is $B = mat(0, 1; 1, 0)$. Different flowers for each color can be constructed by $sum_j^m a_j e^(x_j)$, reaching the final actions:

$
  S(vf(x)) = 1/2 sum_(i j) B_(i j) x_i x_j - sum_j^m a_j e^(x_j)
$

Differentiate to get fixed points tuple:

$
  pdv(S, x_i) = 0 -> sum_j B_(i j) x_j = a_i e^(x_i)
$

Define $X_i := sum_j B_(i j) x_j$ as the co-vector, the critical equations are:

$
  X_i = a_i e^(x_i) -> a_i = X_i e^(-x_i), quad x_i := sum_i (B^(-1))_(i j) X_j
$

We already know the final form of the action on critical points is restricted by:

$
  & pdv(S(vf(x_0))(vf(a)), a_i) = e^(x_i) = X_i/a_i \
  & - S(vf(x)_0) = sum_i integral_0^(a_i) (X_i (a_1,dots.c,a_i= u,0,dots.c))/u d u
$

So the only problem is to solve the coefficients of expansion of each critical points.

$
  X_i = a_i + sum_(p_j >= 1) c_(vf(p),i) product_j^m a_j^p_j
$

Where the coefficient $c_(vf(p),i)$ indicates the power counts tuple $p_j$ for each $a_j^(p_j)$ while the $i$ indicates the $X_i$ co-vector.

Induce that any $X_i (a_1,..,u,0,dots.c) = a_i$ because all product term vanishes, thus we only need to know the coefficient and integrate to get the result: $c_(vf(p),i)/p_i$.

$
  c (vf(p),i) &= 1/(2pi i)^m integral.cont X_i (product_k a_k^(-p_k-1)) d vf(a) \
  &= 1/(2pi i)^m integral.cont X_i (product_k (X_k e^(-x_k))^(-p_k - 1)) d (X_1 e^(-x_1)) and dots.c and d (X_m e^(-x_m))
$

We first calculate the single term, transforming all into $X_i$:

$
  pdv(X_i e^(-x_i), X_j) = e^(-x_i) delta_(i j) - X_i e^(-x_i) B^(-1)_(i j) = e^(-x_i) (delta_(i j) - B^(-1)_(i j) X_i)
$

Thus the Jacobian matrix $J_(i j) = e^(-x_i) (delta_(i j) - B^(-1)_(i j) X_i)$. We can inspect in matrix form:

$
  J = Lambda(e^(-x_1), dots.c, e^(-x_m)) dot (I - Lambda (X_1,dots.c,X_m) B^(-1)) quad Lambda(dots.c) "is diagonal matrix"
$

$
  det (J) = product_(i = 1)^m e^(-x_i) det(I - Lambda(X_1, dots.c, X_m) B^(-1)) = e^(- sum_(i=1)^m x_i) det(I - Lambda(X_1, dots.c, X_m) B^(-1))
$

Generally, we should evaluate the concrete form of $det (lambda I - A)$ for certain matrix $A$. To calculate the determinant, recall the linearity of determinant for row and column:

$
  det (lambda I - A) &= det (lambda_1 - a^((1)),dots.c,lambda_n - a^((n))) quad a^((i)) "is column" (i) \
  &= det (lambda_1,dots.c,lambda_n) + sum_({1,dots.c,n} supset T, abs(T) = 1) det (lambda_1,dots.c,lambda_(n-1),-a^((n))) + dots.c
$

The dumb expansion could be summarized in more terse form, scrutinize that we can pick arbitrary columns $a^((i))$ from the tuple, which *count* as a subset $T subset {1,dots.c,n}$. For example, we pick two columns ${1,2} in {1,2,3}$ for a 3-dimension matrix resulting $det (-a^((1)),-a^((2)),lambda_3)= lambda_3 det (a^((1)),a^((2)),1) := lambda_3 D_({1,2}) (A)$ where we use $D$ to represent the residual or _minor_ determinant of the matrix $A$. Thus the determinant is the summation of all subsets:

$
  det (lambda I - A) = sum_(T subset {1,dots.c,n}) (-1)^(abs(T)) D_T (A) product_(r in {1,dots.c,n}\\T) lambda_r
$

You can see the product of $lambda_r$ comes from the remained index subtracted from $T$.

$
  det (J) &= e^(- sum_(i=1)^m x_i) sum_(T subset {1,dots.c,m}) (-1)^abs(T) D_T (Lambda (X_1,dots.c,X_m) B^(-1)) \
  &= (dots.c) product_(r in T) X_r D_T (B^(-1)) = (dots.c) product_(i=1)^m X_i product_(r in {1,dots.c,n} \\ T) X_r^(-1) D_T (B^(-1))
$

Where the final term is just reverse the product in set $T$ to the product of whole dividing the product *not in* the $T$.

$
  c(vf(p),i) &= 1/(2pi i)^m integral.cont sum_(T subset {1,dots.c,m}) (-1)^(abs(T)) D_T (B^(-1)) X_i product_(r in {1,dots.c,n}\\T) X_r^(-1) \ &quad quad times product_(k=1)^m X_k^(- p_k - 1) product_(h=1)^m X_h exp(sum_(k=1)^m (p_k + 1) x_k - sum_(h=1)^m x_i)) d vf(X)
$

We see a lot of dumb index repeated count, reduce them:

$
  c(vf(p),i) &= 1/(2pi i)^m integral.cont sum_(T subset {1,dots.c,m}) (-1)^abs(T) D_T (B^(-1)) X_i product_(r in {1,dots.c,n}\\T) X_r^(-1) \ &quad quad times product_(k=1)^m X_k^(-p_k) exp(sum_(k,l)^m p_k B^(-1)_(k,l) X_l) d vf(X)
$

The residue power counting is same as before, to simplify notation, identify $T^c = {1,dots.c,n}\\T$. Focus on the certain dumb index $l$:

$
  &n_l - p_l - delta(l in T^c) + delta(i=l) = - 1 \
  &n_l = p_l + delta(l in T^c) - delta(i=l) - 1 -> product_l^m (sum_k^m p_k B^(-1)_(k,l))^(p_l + delta(l in T^c) - delta(i = l) - 1)/((p_l + delta(l in T^c) - delta(i=l) - 1)!)
$

The delta notation impede us reduce further, we reformat the first delta $delta (l in T^c) = 1 - delta (l in T)$, second, we see that $delta (i = l)$ can be decomposed into $delta (i in T^c = l) + delta (i in T = l)$, but it only effect $X_i$, so extract out $i$ index: $p_i - delta(i in T) - delta(i in T) - delta(i in T^c) = p_i - 1 - delta (i in T)$. Focus the $i$ index term, we balance the power:

$
  (sum_k^m p_k B_(k,i)^(-1))^(p_l - delta(i in T) - 1)/(p_i - delta(i in T) - 1)! = (p_i - delta(i in T))/(sum_k^m p_k B^(-1)_(k,i)) (sum_k^m p_k B^(-1)_(k,i))^(p_l - delta(i in T))/((p_i - delta(i in T))!)
$

To thunk the $i$ index term into a whole product. Now we combine all into:

$
  c(vf(p),i) = sum_(T subset {1,dots.c,m}) (-1)^abs(T) D_T (B^(-1)) (p_i - delta (i in T))/(sum_k^m p_k B_(k,l)^(-1)) product_l^m (sum_k^m p_k B^(-1)_(k,l))^(p_l - delta(l in T))/((p_l - delta(l in T))!)
$

$
  product_l^m (dots.c) = product_(l in T)^m ((sum_k^m p_k B^(-1)_(k,l))^(p_l))/(p_l !) product_(l in.not T)^m ((sum_k^m p_k B^(-1)_(k,l))^(p_l - 1))/((p_l - 1)!) = product_l^m C^(p_l)_l/(p_l !) product_(l in.not T)^m (p_l/C_l) \ C_(k,l) = p_k B^(-1)_(k,l) quad C_l = sum_k^m p_k B^(-1)_(k,l)
$

Where we extract by $product_(l in.not T)^m C_l^(p_l-1)/(p_l - 1)! = product_(l in.not T)^m C_l^(p_l)/(p_l !) p_l/(C_l)$.

$
  c(vf(p),i) = product_i^m C^(p_l)_l/(p_l !) sum_(T subset {1,dots.c,m}) (-1)^(abs(T)) (p_i - 1 + delta(i in T^c))/C_i D_T (B^(-1)) product^m_(l in.not T) (p_l/C_l)
$

Here the key, we decompose by $(p_i - 1) + delta(i in T^c)$ into two parts:

$
  det M & := det (C_i delta_(i l) - p_i B_(i l)^(-1)) = product_k^m C_k det (delta_(i l) - p_i/C_i B^(-1)_(i l)) \
        & = product_k^m C_k sum_(T subset {1,..,m}) (-1)^abs(T) D_T (B^(-1)) product^m_(l in.not T) (p_l/C_l)
$

Where each column or row summation is zero, thus, we can find a vector that $C_i$ as columns with $C_i - sum_l C_(i l) = 0$ which is the linear dependence.

$
  det M := det (C_i delta_(i l) - C_(i l)) := 0
$

$
  "term 1" = (p_i - 1)/C_i det (delta_(i l) - p_i/C_i B^(-1)_(i l)) = (p_i - 1) 1/C_i product_k^m 1/C_k det M = 0
$

$
  sum_(T subset {1,dots.c,m}) delta (i in T^c) = sum_(T subset {1,dots.c,m}\\i) -> det D_({1,dots.c,m} \\ i) (M) := (det M)_((i))
$

Where we can see due to the delta notation, the summation must be restricted to index without $i$. Thus the determinant should be ignore the whole $j$ column and row, which is the minor determinant without $j$ index.

$
  "term 2" = 1/C_i det(delta_(i l) - p_i/C_i B^(-1)_(i l))_((i)) = 1/C_i product_(k != i)^m 1/C_k (det M)_((i)) = product_k^m 1/C_k (det M)_((i))
$

$
  c(vf(p),i) = product_l^m C_l^(p_l - 1)/(p_l !) (det M)_((i))
$

Is the final answer, notice the $p_l - 1$ power counts rather $p_l$ due to the factor division from $product_k^m 1/C_k$. It can also be formatted as:

$
  det M &:= product_k^m 1/p_k det (C_i p_l delta_(i,l) - C_(i,l) p_l) := product_k^m 1/p_k det L \ &quad -> N_Gamma (vf(p)) := c(vf(p),i)/p_i = product_k^m 1/(p_k) product_l^m C^(p_l - 1)_l/(p_l !) (det (L) )_(i)
$

Be careful! The *left* $1/p_i$ pair with $product_(k != i)^m 1/p_k$ to forming the whole product. The theorem generalize into a weighted version of _Kirchnoff's matrix tree theorem_, a highly non-trivial extension of _Cayley's theorem_, where we have $p_i$ numbers of vertex $a_i$ of $Gamma$. Suppose only $a_1$ type of vertex, one has $C_l = sum_k^m p_k B_(k,l)^(-1) = p_1$. Because such special case, the $(det (L))_(i)$ is a zero matrix which is defined as $1$. Thus, $N_Gamma (p_1) = p^(p - 2)/p!$, which is exactly the answer of _Cayley's theorem_. We then apply it to the case containing vertices type $a_1$ and $a_2$ or source and sinks:

$
  B = mat(0, 1; 1, 0) -> B^(-1) = mat(0, 1; 1, 0) \
  vf(p) = (p,q)
$

$
  C_l = sum_(k = 1)^2 p_k B_(k,l)^(-1) = (q,p) \
  det(L) = C_i p_l delta_(i,l) - C_(i,l) p_l = mat(p q, -p q; - p q, p q) -> (det(L))_(i) = p q\
$

$
  N_Gamma ((p,q)) = 1/(p q) (p^(q-1) q^(p-1))/(p! q!) dot p q = (p^(q-1) q^(p-1))/(p! q!)
$

Which is same as the results of previous calculation.

$
  cal(A): "set of combinatorial objects or simply objects" \
  omega(vf(s))(a): cal(A) -> bb(N): a -> "counts of" vf(s)-"subojects in" a
$

$
  [cal(A):omega(vf(s))](x) := cases(
    sum_(a in cal(A)) x^(omega(vf(s))(a)) quad "labelled",
    sum_(a in cal(A)) x^(omega(vf(s))(a))/(omega(vf(s))(a)!) quad "unlabelled"
  )
$

We can say that we represent any potential $a$ by $[cal(A):omega(vf(s))](x)$.

For representation of set $cal(U) := {emptyset,{1},{1,2},dots.c}$ of unlabelled combinatorial objects, one get:

$
  [cal(U):omega(vf(s))](x) = sum_(k>=0) x^k/k! = e^x
$

$
  & [cal(A) union cal(B): omega(vf(s))] = [cal(A):omega(vf(s))] + [cal(B):omega(vf(s))] \
  & [cal(A) \\ cal(B): omega(vf(s))] = [cal(A):omega(vf(s))] - [cal(B):omega(vf(s))] \
  & [cal(A) times cal(B): omega(vf(s)) plus.o omega(vf(r))] = [cal(A) : omega(vf(s))] dot [cal(B) : omega(vf(s))] \
  & [cal(A) compose cal(B):omega(vf(s))](y) = ([cal(A):omega(vf(s))] compose [cal(B):omega(r)])(y) \
  & [partial_(vf(s)) cal(A):omega(vf(s))](x) = dv(, x) [cal(A):omega(vf(s))](x) \
$

Where deletion operator will remove all single $vf(s)-$object for possible $a in cal(A)$. Therefore, we can also distinguish the object for all possible ways.

$
  [vf(s) partial_(vf(s)) cal(A):omega(vf(s))](x) = x dv(, x) [cal(A):omega(vf(s))](x)
$

Thus a multi-variate series can represent multiple type of objects.

$
  [cal(A):omega(vf(s_1)) times.o omega(vf(s_2))](x,y) = sum_(a in cal(A)) x^(omega(vf(s_1)) y^(omega(vf(s_2)))
$

$
  G(y) := [cal(G):times.big.o_(k>=1) omega(vf(v)_k) times.o omega(vf(e))](y;lambda_k,u)
$

One can construct a tree by sum its all possible ways: $cal(T) = union.big {"possible way to recover trees"}$. We should investigate the ways by distinguishing method. First, for any $k-$valent flower $lambda_k$ or closed $1-$valent $y$ vertex, we can attach it by deleting each closed vertex $y$ of $k$ trees and attach the flowers to connect $k$ trees or just amend attaching closed $1-$valent vertex for our deleted $1-$valent vertex. However, edge is more special, to attach a edge to recover a tree, we need to delete each vertex and its edge already in two trees and attach one new.#footnote[Or better, we remove each vertex of tree and one edge of *either* tree, then connect them together. The result is same: $1/(2 u) pdv(T, y)^2$] To summarize above operations, we should notice that edge operations are smaller one count than the vertex operations because a tree always has $V - E = 1$. The attaching ways of vertex are always one plus than the attaching ways of edge, yielding the below results.

$
  cal(T) tilde.eq union.big_(k>=1) vf(v)_k partial_(vf(v)_k) cal(T) \\ vf(e) dot cal(U)_2 compose (vf(e)^(-1) partial_(vf(v_1))cal(T))
$

$
  y pdv(T, y) + sum_(k>=3) lambda_k/k! (pdv(T, y))^k - u/2 (1/u pdv(T, y))^2 = T
$

$
  y = u^(-1) (pdv(, x) x^2/2) compose_y (y) = u^(-1) (pdv(, x) x^2/2) compose_y (pdv(, y) (u y^2)/2)
$

$vf(e)^(-1) partial_vf(v)_1 <-> u^(-1) pdv(, y)$.

$
  - u^(-1) (pdv(, x) x^2/2) compose pdv(, y) T + (sum_(k>=3) lambda_k x^k/k!) compose pdv(, y) T
$

$
  y pdv(T, y, 2) + pdv(T, y) + pdv(, pdv(T, y)) (sum_(k>=3) lambda_k/k! (pdv(T, y))^k - 1/(2u) (pdv(T, y))^2) pdv(T, y, 2) &= pdv(T, y) \
  pdv(T, y, 2)(y + pdv(, pdv(T, y))(dots.c)) &= 0 \
  pdv(, pdv(T, y)) (1/(2u) (pdv(T, y))^2 - sum_(k>=3) 1/k! (pdv(T, y))^k) &= y \
$

$
  y = pdv(, x) (x^2/(2u) - sum_(k>=3) x^k/k!) compose_(x:y) (pdv(T, y))
$

We recover the vertex expression by tree in a astonishing way. Therefore establishes a bijection between $T$ and $F = x^2/(2 u) - sum_(k>=3) x^k/k!$.

$
  L[T](x = pdv(T, y)) = y pdv(T, y) - T = x^2/(2u) - sum_(k>=3) x^k/k! = F(x)
$

$
  L^2[T](x = pdv(T, y)) & = L[F](z = pdv(F, x)) \
                        & = x pdv(F, x) - F \
                        & = (z^2/(2 u^(-1)) - sum_(k>=3) z^k/k!) compose_(z:x) (pdv(F, x)) quad (pdv(F, x) = y) \
                        & = (dots.c) compose_(z:x) (y) = T(z)
$

Imply a original tree. It suggests that if we consider a general graph as a tree of 1-irreducible components or 2-connected components, taking Legendre transformation yielding a set of 1-irreducible components. It's especially useful that we could investigate irreducible components only.

==

A supervector space $V$ over $bb(R)$ or any $bb(k)$ field of characteristic $0$ is just a $bb(Z)_2$-graded vector space:

$
  "gr"_(I)(V) = plus.o.big_(I) V^I
$

$
  "fil"(V) = 0 subset F^1 (V) subset F^2 (V) subset ... subset F^k (V) = V
$

$
  "agr"(V) = plus.o.big_I F^(i+1)(V)\/F_i (V) != V
$

$
  V = V_0 plus.o V_1 = bb(k)^n plus.o bb(k)^m := bb(k)^(n|m) quad eta: V_(0\/1) -> 0\/1
$

A tensor algebra is:

$
  T(V) = plus.o.big_(n=0)^(infinity) T^(i) (V) = plus.o.big_(n=0)^(infinity) underbrace(V times.o V dots.c times.o V, n) = plus.o.big_(n=0)^infinity V^(times.o n)
$

$
  S(V) = T(V)\/(v times.o w - w times.o v) -> T(V) \/ (v times.o w - (-1)^(eta(w) eta(v)) w times.o v) \
  eta: underbrace(xi_(i_1) times.o xi_(i_2) dots.c times.o xi_(i_n), n) = n mod 2
$

$
  Lambda(V) = T(V)\/(v times.o w + w times.o v) -> T(V) \/ (v times.o w + (-1)^(eta(w) eta(v)) w times.o v)
$

$
  S(V_0) <->^(Pi) Lambda (V_1), quad S(V_1) <->^(Pi) Lambda(V_0)
$

$
  &S(V) tilde.equiv S(V_0) times.o Lambda(V_1) tilde.equiv plus.o.big S^i (V_0) times.o plus.o.big Lambda^i (V_1): v times.o w = (-1)^(eta(v)eta(w)) w times.o v \
  &Lambda(V) tilde.equiv Lambda(V_0) times.o S(V_1) tilde.equiv plus.o.big Lambda^i (V_0) times.o plus.o.big S^i (V_1): v and w = -(-1)^(eta(v)eta(w)) w and v \
$

$
  cal(O)(V) = bb(k)[x_1,...,x_n;xi_1,...,xi_m] = S(V_0^*) times.o Lambda(V_1^*) "in linear coordinates"\
  x_i x_j = x_j x_i, thick x_i xi_j = xi_j x_i, thick xi_i xi_j = - xi_j xi_i
$

$C^(infinity)(V_1)$ have no topology defined upon due to $xi^2 = 0$. Thus there's no smoothness. But we can still define the polynomial algebra with a correspondence by $f(xi_1,dots.c,xi_n)= sum_(k>=0) f^(\(k\))/(k!) xi_(k_1) xi_(k_2) dots.c xi_(k_n)$, explicitly, one define $e^(xi) = sum_(k>=0) xi^k/k! = 1 + xi$.

$
  C_s^(infinity)(V_1) "doesn't exist!" ->
  C_s^infinity := C^(infinity)(V_0) times.o Lambda (V_1^*)
$

$
  (M, C_(s)^infinity (M)) supset (U := U_0 times V_1, C_s^infinity (U_0) := C^infinity (U_0) times.o Lambda(V_1^*)) \
  F: M (x_1,dots.c,x_n;xi_1,dots.c xi_m) -> N(y_1,...,y_p;zeta_1,...,zeta_q) \
$

$
  y_i = f_i (x_1,dots,x_n) + f_i^(j_1,j_2) (x_1,dots,x_n) xi_(j_1) xi_(j_2) + dots "with"
  eta(y_i) = 0 \
  zeta_i = g^(j_1)_i (x_1,dots, x,_n) xi_(j_1) + g^(j_1,j_2,j_3)_i (x_1,dots,x_n) xi_(j_1) xi_(j_2) xi_(j_3) + dots "with" eta(zeta_i) = 1 \
$

Therefore for any scalar function defined upon manifold, one has such pullback:

$
  F^*: C^(infinity)_s (M) -> C^(infinity)_s (N) \
  F^(*)(f)(x_1,dots,x_n;xi_1,dots,xi_m) = f compose F (y_1,dots,y_p;zeta_1,dots,zeta_q)
$

$
  F: M = bb(R)^(1|2) -> N = bb(R)^(1|2) = (x_1,xi_1,xi_2) -> (x + xi_1xi_2,xi_1,xi_2) \
  F^* (f(x_1)) = f(x_1+xi_1 xi_2) = f(x) + f'(x) xi_1 xi_2
$

$
  R := R_0 plus.o R_1 quad R_i R_j subset.eq R_(i + j mod 2)\
  x y = (-1)^(eta(x)eta(y)) y x
$

$
  T: V -> V "is even if" T(V_i) subset.eq V_i quad "is odd if" T(V_i) subset.eq V_(i+1 mod 2)
$

$
  & T "is even if" eta(T) = 1 \
  & T "is odd if" eta(T) = -1 \
$

$
  [A,B] := A B - (-1)^(eta(A) eta(B)) B A
$

Thus if $T -> "Mat"_(n|m)(R)(e_1,dots,e_n;f_1,dots,f_m)$ with basis $e_i$ of $V_0$ and $f_i$ of $V_1$, we immediately see that:

$
  G L_(n|m) (R) tilde.equiv "Mat"_(n|m)(R) = mat(A_00, A_01; A_10, A_11)
$

Where $A_00$ is $n$ by $n$, $A_11$ is $m$ by $m$ is _even_ mapping to the same space while $A_(10\/01)$ is $m times n$ or $n times m$ is _odd_ mapping to another space changing the parity.

$
  "sTr": "Mat"_(n|m)(R) -> R \
  "sTr"(mat(A_00, A_01; A_10, A_11)) -> "Tr"(A_00) + epsilon thin "Tr"(A_11)
$

$
  A = mat(0, X; 0, 0), quad B = mat(0, 0; Y, 0) \
  A B = mat(X Y, 0; 0, 0), quad B A = mat(0, 0; 0, Y X) \
$

$
  & "sTr"(A B) = "Tr" (X Y) + epsilon dot 0 = "Tr" (X Y) \
  & "sTr"(B A) = epsilon "Tr" (Y X)
$

// $
//   "sTr"([A,B]) &= "sTr"(A B - (-1)^(eta(A)eta(B)) B A) \
//   &= "sTr"(A B + B A) \
//   &= "Tr"(X Y) + epsilon "Tr"(Y X) = 0\
// $

$
  "sTr"(A B) = "sTr"(B A) -> "Tr"(X Y) = epsilon "Tr"(Y X)
$

$
  "Tr"(Y X) & = sum_(i,j)^(m,n) Y_(j i) X_(i j) = - sum_(i,j)^(m,n) X_(i j) Y_(j i) = - "Tr" (X Y) \
          & -> "Tr" (X Y) = epsilon (-"Tr"(X Y)) \
          & -> epsilon = -1
$

$
  "sTr"(A) := "Tr"(A_00) - "Tr"(A_11)
$

For block-diagonal matrix $A = A_00 times.o A_11$:

$
  "sDet"(e^A) = e^("sTr"(A)) = e^("Tr"(A_00) - "Tr"(A_11)) = "Det"(A_00)/"Det"(A_11)
$

Generally, apply Gauss elimination in block-level. To achieve this, we have to suppose the block is invertible.

$
  mat(A_00, A_01; A_10, A_11) & = mat(I, 0; A_10 A_00^(-1), I) mat(A_00, A_01; 0, A_11 - A_10 A_00^(-1) A_01) \
                              & = (dots) mat(A_00, 0; 0, A_11 - A_10 A_00^(-1) A_01) mat(I, A_00^(-1) A_01; 0, I) \
$

$
  mat(A_00, A_01; A_10, A_11) & = mat(I, A_(01) A_11^(-1); 0, I) mat(A_00 - A_01 A_11^(-1) A_10, 0; A_10, A_11) \
                              & = (dots) mat(A_00 - A_01 A_11^(-1) A_10, 0; 0, A_11) mat(I, 0; A_11^(-1)A_10, I)
$

$
  & "sDet"(mat(I, A_10; A_10, I)) = exp("sTr"(dots)) = exp(0) = 1 \
  & "sDet"(A B) = "sDet"(A) "sDet"(B) \
$

$
  "sDet"(A) = ("Det"(A_00 - A_01 A_11^(-1) A_10))/("Det"(A_11)) "or" ("Det"(A_00))/("Det"(A_11 - A_10 A_00^(-1) A_01))
$

$
  & n = 1, m = 0; x' = lambda x: integral f(x') d x' = integral f(lambda x) abs(lambda) d x \
  & n = 0, m = 1; xi' = mu xi: integral f(xi') d xi' = integral f(mu xi) abs(mu)^(-1) d xi
$

$
  T_h: x -> x + h => T_h (I) = I "by translation invariance"\
  integral f(vf(x),vf(xi)) d x^I d xi^I = integral f(vf(x) + vf(lambda), vf(xi) + vf(mu)) d x^I d xi^I \
$

Differentiate in coordinates zero, we immediately found that any partial derivatives in any directions is zero:

$
  integral partial_(x_i\/xi_i) f(vf(x),vf(xi)) d x^I d xi^I = 0
$

$
  integral partial_xi xi thin d xi = integral d xi = 0
$

$
  integral xi thin d xi = "constant" =>^("normalization") integral xi thin d xi = 1
$

$
  B(xi,xi) = sum_(i,j) b_(i j) xi_i xi_j \
$

It's easy to see that $b_(i j) = - b_(j i)$ to make sense, otherwise it must be zero due to anti-commutation of odd variables.

$
  B(xi,xi) = sum_(i,j) b_(i j) xi_i xi_j = - sum_(i,j) b_(i j) xi_j xi_i = sum_(i,j) b_(j i) xi_j xi_i = B(xi,xi)
$

$
  e^(1/2 B(xi,xi)) = sum_(k>=0) 1/(2^k k!) (B(xi,xi))^k \
$

We must have even numbers of odd variables due to unmatched integral for certain odd variable $xi$ contributing zero. For each $k-$degree term, the only nonzero contribution must be indices distinction due to $xi^2 = 0$. Thus:

$
  (B(xi,xi))^k = (2 sum_(i<j) b_(i j) xi_i xi_j)^k &= 2^k sum_(sigma in Pi_k) b_(sigma(i_1)(j_1)) dots.c b_(sigma(i_k)(j_k)) xi_(sigma(i_1)) xi_(sigma(j_1)) dots.c xi_(sigma(i_k)) xi_(sigma(j_k)) \
  &= 2^k k! sum_(sigma in Pi_k) product_(m) b_(sigma(i_m)(j_m)) xi_(i_1) xi_(j_1) dots.c xi_(i_k) xi_(j_k) \
  &= 2^k k! sum_(sigma in Pi_k) product_m b_(sigma(i_m)sigma(j_m)) eta(sigma) xi_1 xi_2 dots.c xi_(2m) \
$

$
  integral e^(1/2 B(xi,xi)) d xi &= integral sum_(sigma in Pi_k) product_m b_(sigma(i_m) sigma(j_m)) eta(sigma) xi_1 dots.c xi_(2m) thick d xi_(2m) dots.c d xi_1 \
  &= sum_(sigma in Pi_k) eta(sigma) product_(m) b_(sigma(i) sigma(j))
$

Where the pairing sign is depended on the order. We can see by swapping times, one swap corresponds to one minus sign. Quicker, we can see if each pairing number crossing each other. ${{1,4},{2,5},{3,6}}$, we see by ${1,4}$ across else two terms, and ${2,5}$ cross ${3,6}$, thus $(-1)^3 = -1$, is minus sign. Thus the maximal minus sign must be $m - 1 + m - 2 + dots = (m(m-1))/2$ times.

$
  Z (s_1,dots,s_n) = integral e^(-1/2 B(xi,xi) + sum_(i=1)^n s_i lambda_i (xi)) d xi \
$

$
  lr(pdv(, s_n) dots pdv(, s_1) Z(vf(s))bar)_(s=0) = integral e^(1/2 B(xi,xi)) product_i^n lambda_i (xi) d xi
$

$
  eta := sum_(i=1)^n s_i lambda_i => xi' := xi - B^(-1) eta in V => -1/2 B(xi,xi) + eta (xi) = -1/2 B(xi',xi') + 1/2 B^(-1) (eta,eta)
$

Where $B^(-1) eta = B^(-1) (eta, dot)$ with $B (B^(-1) eta, dot) = (B B^(-1) eta, dot) = (eta, dot) = eta(dot)$.

$
  B^(-1)(eta,eta) = sum_(i,j) s_i s_j B^(-1) (lambda_i, lambda_j) => sum_(sigma in Pi_m) s_(i_1) s_(j_1) dots s_(i_m) s_(j_m) product_(r=1)^m B^(-1) (lambda_(i_r), lambda_(j_r))
$

$
  S(v) = 1/2 B(v,v) - sum_(r >= 3) (B_r (v,dots,v))/r!
$

$
  B_r (v,dots,v) = sum_(s=0)^r vec(r, s) B_(s,r-s) (v_1,dots,v_1,v_0,dots,v_0)
$

$
  I[S](planck) = ((2pi planck)^(dim V_0)/(det B_0))^(1/2) (planck^(-(dim V_1)) "sDet"(-B_1))^(1/2) sum_(Gamma) planck^(eta(Gamma))/(abs("Aut"(Gamma))) bb(F)_Gamma (l_1,dots,l_m;lambda_1,dots,lambda_n)
$

$
  dot(f) = [f,H]_(plus.minus)
$

$
  [a,b]_(plus.minus) = i innerproduct(a,b) \
$
$
  &a b - b a = i innerproduct(a,b) "for Weyl" \
  &a b + b a = i innerproduct(a,b) "for Clifford" \
$

$

$

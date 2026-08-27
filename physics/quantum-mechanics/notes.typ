#import "../lib.typ": *
#import "@preview/physica:0.9.8": *

#show: mine.with(
  title: "Review of Quantum",
)

= Operator

For Hermitian:

$
	expval(A) = braket(psi,A psi) = braket(A psi, psi) = braket(psi,A psi)^* = expval(A)^*
$

Reversely, if $forall psi$ s.t. $braket(psi,A psi)$ is real:

$
	psi = psi_1 + psi_2 \
	braket(psi, A psi) = braket(psi_1,A psi_1) + braket(psi_1,A psi_2) + braket(psi_2,A psi_1) + braket(psi_2,A psi_2) = braket(A psi,psi) = dots
$

$
	braket(psi_1,A psi_2) + braket(psi_2, A psi_1) &= braket(A psi_2,psi_1) + braket(A psi_1, psi_2) \
	braket(psi_1,A psi_2) - braket(A psi_1,psi_2) &= (dots) 
$

The composition is arbitrary because:

$
	psi = psi_1 + psi' +  psi_2 - psi' = psi'_1 + psi'_2
$

Therefore the only choice is: $braket(psi_1,A psi_2) = braket(psi_2, A psi_1)$

$
	i planck dv(A,t) = [A,H]
$

$
	- planck^2 dv(A,t,2) = [[A,H],H]
$

$
	i planck dv(,t) braket(psi,e^(- i/planck H t) A e^(i/planck H t), psi) = braket(psi(t),[A,H],psi(t))
$

$
	- planck^2 (,t,2) braket(psi,e^(- i/planck H t) A e^(i/planck H t), psi) &= braket(psi(t),[[A,H],H],psi(t)) \
	dv(,t,2) expval(A) = braket([[A,H],H])
$

$
	E_n &= braket(psi_n (t),H,psi_n (t)) \
	dv(E_n,lambda) &= dv(,lambda) braket(psi_n,e^(- i H t) H e^(i H t), psi_n) \
	dv(E_n,lambda) &= braket(psi_n, dv(H,lambda),psi_n)
$

So one often say:

$
	dv(A,t) = dv(A_H,t) = -i/planck [A,H]
$

$
	braket(n,dv(A,t),n') = -i/planck braket(n,[A,H],n') = - i/planck (E_n' - E_n) braket(n,A,n')
$

$
	[[A,H],A] = [A,H] A - A [A,H] \
$

$
	braket(n,[A,H] A - A [A,H],n') &= sum_k (E_n - E_k) braket(n,A,k) braket(k,A,n') - (n <-> n') \
$

If $n = n'$:

$
	"LHS" = 2 sum_k (E_n - E_k) F_(n k)^2
$

Suppose $A = hat(x)$ for $H = p^2/(2m) + V(bold(r))$:

$
	[[x, H],x] = i planck [p/m, x] = -planck^2/m
$

$
	sum_k (E_n - E_k) x^2_(n k)  &= -planck^2/(2m) \
	sum_k (E_k - E_n) x^2_(k n)  &= planck^2/(2m) \
$

= Spin

$
	a dot b := 1/2 (a b + b a) = 1/2 [a,b]_+\
	a and b := 1/2 (a b - b a) = 1/2 [a,b]_-
$

$
	e_i dot e_j = delta_(i j) = 1/2(e_i e_j + e_j e_i) = 1/2 [e_i,e_j]_+\
$

$
	e_i and e_j = 1/2 (e_i e_j - e_j e_i) = e_i e_j "if" i != j
$

$
	I = e_1 e_2 e_3, quad I^2 = e_1 e_2 e_3 e_1 e_2 e_3 = (-1)^(n(n-1)\/2) = -1
$

$
	[sigma_i, sigma_j]_- = 2 i epsilon_(i j k) sigma_k, quad [sigma_i,sigma_j]_+ = 2 delta_(i j)
$

$
	sigma_i sigma_j = delta_(i j) + i epsilon_(i j k) sigma_k
$

$
	bold(v) = ket(arrow.t) "or" ket(arrow.b) => lambda = plus.minus 1/2 planck ~ plus.minus 1
$

$
	sigma_z = mat(1,0;0,-1), [sigma_z, sigma_(i != z)]_+ = 0 => sigma_z (sigma_(i!=z) v) = - lambda_v (sigma_(i!=z) v) => lambda_(sigma_(i!=z) v) = -lambda_v = minus.plus 1
$

$
	sigma_(i!=z): V_1 plus.o V_(-1) -> V_1 plus.o V_(-1) => V_1 -> V_(-1), V_(-1) -> V_1
$

$
	sigma_(i!=z) = mat(0,a;a^(dagger),0), sigma^2_(i!=z) = 1 => sigma_(i!=z) = mat(0,a;a^(-1),0)
$

$
	sigma_x = mat(0,1;1,0), quad sigma_y = mat(0,i;-i,0)
$

$
	(bold(a) dot bold(sigma)) (bold(b) dot bold(sigma)) = a_i b_j sigma_i sigma_j = bold(a) dot bold(b) + i bold(sigma) dot (bold(a) times bold(b))
$

$
	(bold(a) dot bold(sigma)) bold(sigma) = a_i sigma_i sigma_j = bold(a) + i epsilon_(i j k) a_i sigma_k = bold(a) - i epsilon_(j i k) a_i sigma_k = bold(a) - i (bold(a) times bold(sigma))
$

$
	sigma^2 = (sum_i sigma_i)^2 = 3 + sum_(i,j) [sigma_i, sigma_j]_+ = 3
$

$
	s_i = planck/2 sigma_i
$

$
	S^2 = (bold(s)^1 + bold(s)^2)^2 = 2 dot 3/4 planck^2 + 1/2 planck^2 (bold(sigma)^1 dot bold(sigma)^2) ~ 3/2 + 1/2 (bold(sigma)^1 dot bold(sigma)^2)
$

$
	&chi_(00) = 1/(sqrt(2)) ket(arrow.t)_1 ket(arrow.b)_2 - ket(arrow.b)_1 ket(arrow.t)_2 \
	&chi_(10) = 1/(sqrt(2)) ket(arrow.t)_1 ket(arrow.b)_2 + ket(arrow.b)_1 ket(arrow.t)_2 \
	&chi_(11) = ket(arrow.t) ket(arrow.b) \
	&chi_(1 -1) = ket(arrow.b) ket(arrow.b)
$

$
	P_(lambda_k) = product_(j!=k) (A-lambda_j I)/(lambda_k - lambda_j)
$

$
	&P_(s = 0) = (S^2 - 2)/(0 - 2) = 1/2 (2 - S^2) = 1/4 (I - bold(sigma)^1 bold(sigma)^2) \
	&P_(s = 1) = (S^2 - 0)/(2 - 0) = 1/2 (S^2) = 1/4 (3 I + bold(sigma)^1 bold(sigma)^2) \
$

$
	P_(s=0) + P_(s=1) = I
$

$
	(P_(s=0) - P_(s=1)) v = P_(1 2) v = - lambda_(v) v
$

== Zeeman Effect

A electron with angular momentum $bold(L)$:

$
	mu_L = - e/(2m_e) bold(L) = - g_l bold(L)
$

Suppose $bold(B) = B hat(z)$:

$
	H_L = - mu_L dot bold(B) = (e B)/(2m_e) L_z
$

A electron intrinsic spin $bold(S)$:

$
	mu_S = - g_s bold(S) approx - e/(m_e) bold(S) 
$

Usually, we have a *approximation* relation:

$
	2 g_l = g_s
$

$
	H_S = - mu_S dot bold(B) approx - (e B)/(m_e) S_z 
$

$
	H_B approx g_l B (L_z + 2 S_z), quad H = H_0 + xi(bold(r)) bold(L) dot bold(S) + H_B
$

Or generally:

$
	H_B = g_l B_z (L_z + alpha S_z)
$

Since $bold(B)$ is weak, we perturbs by $H_B = H'$ and solve in $ket(n j s j m_j)$ eigenstate.

Now beside $n,l$ state, we use composite state $j = l + s$ rather their own, with the $m_j$ as axial momentum.

$
	bold(J) = bold(L) + bold(S) \
$

Focus only on $ket(j m_j)$:

$
	Delta E = g_l braket(j m_j, L_z + alpha S_z, j m_j)
$

$
	mu_"eff" = g_j bold(J), quad mu_"eff" dot bold(B) = g_j J_z \
	Delta E = g_j braket(j m_j, J_z ,j m_j)
$

Because we are in $ket(j m_j)$ basis, therefore any vector must *project* into $J$ subspace.

$
	expval(bold(L) + alpha bold(S)) = expval((bold(L) + alpha bold(S)) dot bold(J))/(expval(bold(J)^2)) expval(bold(J))
$

$
	mu_"eff" = g_l expval((bold(L) + alpha bold(S)) dot bold(J))/(expval(bold(J)^2)) bold(J) = g_j bold(J)
$

$
	(bold(L) + alpha bold(S))(bold(L) + bold(S)) = bold(L)^2 + (alpha + 1) bold(L) dot bold(S) + alpha bold(S)^2
$

$
	bold(L) dot bold(S) = 1/2 (bold(J)^2 - bold(L)^2 - bold(S)^2)
$

$
	(bold(L) + alpha bold(S))(bold(L) + bold(S)) =  ((1+alpha) bold(J)^2 + (1-alpha)bold(L)^2 + (alpha - 1)bold(S)^2)/2
$

$
	g_j  = g_l expval((bold(L) + alpha bold(S)) dot bold(J))/(expval(bold(J)^2)) = g_l ((1+alpha)j(j+1) + (1-alpha)(l(l+1) - s(s-1)))/(2 j(j+1))
$

$
	Delta E = g_j planck m_j quad m_j in {-j,-j+1,dots,j}
$

Where we gets $2j+1$ split state.

If there's no $xi(bold(r)) bold(L) dot bold(S)$, we have no need to apply perturbation calculation and use eigenstate $ket(n l m_l m_s)$:

$
	Delta E = g_l B (m_l + alpha m_s)
$

Totally $(2 l + 1) dot 2$ states.

== Problem

$
	H = A bold(s)^1 dot bold(s)^2 = A/2(S^2 - 3/2), quad v(0) = ket(arrow.t)_1 ket(arrow.b)_2 = (chi_(00) + chi_(10))(0)
$

$
	s = 1 => E_1 = A/4, quad s = 0 => E_0 = -3/4 A
$

$
	v(t) = e^(- i H t) v(0) = e^(- i E_0 t) chi_(0 0) + e^(- i E_1 t) chi_(10)
$


= Typical Model

== Delta Potential

$
	- planck^2/(2m) pdv(psi,x,2) = (E - gamma delta(x)) psi(x)
$

Consider the boundary condition at $x = 0$:

$
	- planck^2/(2m) (psi'(0^+) - psi'(0^-)) &= - gamma psi(0) \
	psi'(0^+) - psi'(0^-) &= (2 m gamma)/(planck^2) psi (0)
$

Unit normalization $planck = 1$.

$
	psi''(x) + k^2 psi(x) = 0, quad k = (2 m E)^(1/2)
$

$
	psi(x) = cases(e^(i k x) + R e^(-i k x) quad &x<0, S e^(i k x) quad &x>0) \
$

$
	psi(0^+) &= psi(0^-) \
	1 + R &= S
$

$
	psi'(0^+) - psi'(0^-) &= 2 m gamma psi (0) \
	S - (1 - R) &= - i (2 m gamma)/k psi(0) = -i (2 m gamma)/k S \
$

$
	2 = S(2 + i (2 m gamma)/k), quad (m gamma)/k = alpha
$

$
	S = 1/(1 + i alpha), quad R = (- i alpha)/(1 + i alpha)
$

$
	S^* S + R^* R = 2 S S^* - S - S^* + 1 &= 1 \
	2 &= 1/S + 1/S^*
$

Indeed, $S$ satisfy the condition.

Reversely, $- gamma <-> gamma$ with ansatz:

$
	psi(x) = cases(A e^(k x) quad x < 0,A e^(- k x) quad x > 0)
$

$
	- 2 k A &= - (2 m gamma) A \
	k &= m gamma
$

$
	E = - (m alpha^2)/(2 planck^2)
$

== Harmonic Oscillator

$
  H = p^2/(2 m) + 1/2 m omega^2 x^2 => H = hat(p)^2/(2m) + 1/2 m omega^2 hat(x)^2
$

$
  H = 1/2 p^2 + 1/2 x^2 = 1/2^(1/2) (p - i x) 1/2^(1/2)(p + i x) + 1/2
$

$
  a^(dagger) = 1/2^(1/2) (p-i x), quad a = 1/2^(1/2) (p+i x), quad hat(N) = a^(dagger) a, quad hat(H) = hat(N) + 1/2
$

$
	x = (a-a^(dagger))/(i 2^(1/2)), quad p = (a + a^dagger)/2^(1/2)
$

$
	hat(H) ket(alpha) = hat(N) + 1/2 ket(alpha) = (n + 1/2) ket(alpha), quad alpha = n
$

$
	[hat(N),a^dagger] = a^dagger, quad [hat(N),a] = - a
$

$
	[hat(N), a^dagger] ket(n) = - n a^dagger ket(n) + hat(N) a^dagger ket(n) = a^(dagger) ket(n) \
	[hat(N), a] ket(n) = - n a ket(n) + hat(N) a ket(n) = - a ket(n)
$

$
	hat(N) a^(dagger) ket(n) = (n+1) a^(dagger) ket(n), quad hat(N) a ket(n) =(n-1) a ket(n)
$

$
	braket(n,hat(N),n) = braket(n, a^dagger a,n) = n = c^2, quad c = n^(1/2)
$

$
	braket(n,hat(N),n) = n^(1/2) braket(n, a^dagger, n-1) = n
$

$
	a^dagger ket(n) = (n+1)^(1/2) ket(n+1), quad a ket(n) = n^(1/2) ket(n-1)
$

$
	ket(n) = 1/(n!)^(1/2) (a^dagger)^n ket(0)
$

$
	x ket(n) = i/2^(1/2) a^dagger - a ket(n) = i/2^(1/2) [(n+1)^(1/2) ket(n+1) - n^(1/2) ket(n-1)] \
	p ket(n) = 1/2^(1/2) a^dagger + a ket(n) = 1/2^(1/2) [(n+1)^(1/2) ket(n+1) + n^(1/2) ket(n-1)] \
$

$
	[m omega^2 x^2] = [planck omega], [x] = ([planck]/[m omega])^(1/2) \
	[p^2/m] = [planck omega], [p] = ([m omega] [planck]])^(1/2) \
$

= Perturbation

$
	H = H_0 + lambda H', quad ket(n) = sum_(i=0) lambda^i ket(n^i), quad E_n = sum_(i=0) lambda^i E^i_n
$

$
	H ket(n) &= E_n ket(n) \
	H_0 + lambda H' sum_(i=0) lambda^i ket(n^i) &= sum_(j=0) lambda^j E_n^j sum_(k=0) lambda^k ket(n^k) \
	H_0 ket(n^0) + sum_(i=1) lambda^(i) (H_0 ket(n^i) + H' ket(n^(i-1))) &= E_n^0 ket(n^0) + sum_(i=1) sum_(j+k = i) E_n^j ket(n^k) \
$

$
	&lambda^0: quad H_0 ket(n^0) = E_n^0 ket(n^0) \
	&lambda^1: quad H_0 ket(n^1) + H' ket(n^0) = E^0_n ket(n^1) + E^1_n ket(n^0) \
	&lambda^2: quad H_0 ket(n^2) + H' ket(n^1) = E^0_n ket(n^2) + E^1_n ket(n^1) + E^2_n ket(n^0)
$

By orthogonality:

$
	ket(n^i) = sum_(m!=n^0) c_m^i ket(m^0) => braket(n^i,n^0) = 0
$

$
	lambda^1: quad braket(n^0,H_0,n^1) + braket(n^0,H',n^0) &= E_n^1 \
	E_n^1 &= braket(n_0,H',n_0) \
$

$
	lambda^1: quad braket(k^0,H_0,n^1) + braket(k^0,H',n^0) &= E_n^0 braket(k^0,n^1) + E^1_n braket(k^0,n^0) \
	E_k^0 c_k^1 + braket(k^0,H',n^0) &= E_n^0 c_k^1 \
	c_k^1 &= braket(k^0,H',n^0)/(E_n^0 - E_k^0)
$

$
	lambda^2: quad braket(n^0,H_0,n^2) + braket(n^0,H',n^1) &= E_n^2 \
	sum_(k^0 != n^0) (braket(n^0,H',k^0) braket(k^0,H',n^0))/(E^0_n - E^0_k) &= E_n^2
$

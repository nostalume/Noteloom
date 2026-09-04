#import "../lib.typ": *


#show: daily-en.with(
  title: "Review of Electromagnetics",
  eq-numbering: "(1.1)",
  eq-chapterwise: true,
)

#let up(x) = { $upright(#x)$ }
#let hup(x) = { $hat(upright(#x))$ }
#let four_p = $A^mu (t, #up("x"))$

= Static Field

== Correction

The usual problem derived from the static field solving. Usually, there are two parts, first, we already know the distribution of charge or current, second, we only know some of underneath boundary condition in vacuum or isotopic media.

It's more constructive to first expand potential:

$
  phi.alt(x) = 1 / (4 pi epsilon_0) 1 / r integral d^3 x' rho(x') / (|x - x'|)
$

In spherical coordinates, we have $x dot x' = |x||x'| cos theta$, and if $x$ is far way from source:
$
  1 / (|x-x'|) = 1 / x sum_(l=0)^infinity (x' / x)^l P_l (hat(x) dot hat(x)' = cos theta) quad x >> x'
$

We have below for first few $P_l$:
$
  P_1(cos theta) = 1, quad P_2(cos theta) = cos theta, quad P_3(cos theta) = 1 / 2(3 cos^2 theta - 1)
$
Indeed, if we plugin in, we acquire the monopole, dipole, and quadruple. A good message is the $P_3$ is indeed the $Q_(i j)$.

We see that $integral d x'^3 rho(x') x'_i x'_j = Q_(i j)$ and so on...

But however, a clever hindsight is the traceless in summation of matrix, but traceless of $x$ is traceless of $x'$ of symmetry, so we turn the $x' -> x$ in trace resulting $1 / 3 D_(i j) = integral d x'^3 x'_i x'_j - 1 / 3 |x'|^2 delta_(i j)$, $(3 x_i x_j - |x|^2 delta_(i j)) -> 3 x_i x_j$

Then:
$
  D_(i j) = integral d x'^3 3 x'_i x'_j - |x'|^2 delta_(i j)
$

To ease our burden.

Now we back to the one order, we know:
$
  d_i = up(d) = integral d x'^3 rho(x') x'_i
$

We take such term as a correction of native electric field as $P$ for all residue terms.

$
  phi.alt(t, x) &= 1 / (4 pi epsilon_0) integral d x'^3 P(x') (x - x') / (|x - x'|^3) \
  &= - 1 / (4 pi epsilon_0) integral d^3 x' nabla_x' P(x') / (|x-x'|) + 1 / (4 pi epsilon_0) integral d^2 s' dot P(x') / (|x - x'|)
$

So beside the surface charge $up(n) dot P(x)$, we has bounded charge as $- nabla P(x)$, comes from the one order correction.

That's dipole must be naturally neutral. So based on Gauss, we know:
$
  - integral_V d^3 x nabla dot P(x) = - integral_(partial V) d^2 s hat(up(n))_s dot P(x)
$

Which added the surface charge as zero. What does this mean? It means the charge distributes on surface only, and inner cancels.

So we have a surface integration:
$
  nabla dot (epsilon_0 E + P) = nabla dot D = q_("free") \
  - nabla dot P = q_("bol")
$

== Energy

Energy is bit troublesome, The energy we deduce in discrete level is actually interaction energy and we then add $1 / 2$ in summation. However, we then call it the self energy of such assembly. Is that so? In electrostatics, every charges must be *fixed*, so we counts them up as:

$
  1 / (4 pi epsilon_0) d^3 x d^3 x' (rho_1(x) rho_2(x')) / (|x - x'|)
$

Then self energy, must be $rho_1(x) rho_1(x')$, there's a over-counting by symmetry of the same charge distribution by $x <-> x' quad rho(x) <-> rho(x')$ for the same position permutation, we add $1 / 2$. But how, is that only interaction energy in discrete level? Indeed, there's no self energy in classical level as a diverge. That's a ultraviolent diverge, which cause the quantum field regularization. However, classical level won't tackle this, which is only a ideal model and we only cares about grand independent system.

We try to formulate the principle of freely moving charge in metal, to solve many problems. Premiere, we know fixed charge distribution means lowest level energy in potential variation.

$
  U = 1 / 2 integral epsilon_0 |E|^2 d^3 x > 0 \
  delta U = 1 / 2 integral epsilon_0 delta abs(E)^2 d^3 x ~ E delta E ~ E rho delta x
$
For variation of $delta x$ in source, for example, metal. That's, $E = 0$ indeed, because source should have charge. However, we know $E = 0 -> rho = 0$, they are same in Gauss view. So a metal must not have charge inside volume and only in boundary because $delta x$ now isn't possible of variation on boundary. So $V = V_0$, is fixed but unknown.

Thus we only know such boundary condition, for example, a surface warps inner hallow of a conductor and surface itself is in the conductor, we has $integral E d S = q_("inner") + q_("ind") = 0$. So, $q_("ind") = - q_("inner")$ as the integral of $integral - nabla phi.alt dot hat(up(n)) d S = 0$ is the boundary condition.

Another condition is to use a batter to give the boundary potential a specific value. Notice, previous is unknown but fixed value, this one is a *specific* value. So, it states that $phi.alt|_(S) = V_0$.

All above is given as two end point problem, but sometimes, you only know one, because other is at origin or infinity, which should be a bounded value.
$
  phi.alt|_S = V_0 \ "or" \ integral nabla phi.alt hat(up(n)) dot d S = Q_0 \
$
$
  phi.alt|_(S -> infinity\/0) = "bounded value"
$

Gives us a full condition, sometimes, it could be a two solution connection, which must be equal on value and differential value.

$
  phi.alt_1|_S = phi.alt_2|_S \
  "or" \
  nabla phi.alt_1 dot hat(up(n)) = nabla phi.alt_2 dot hat(up(n))
$

Which are also two conditions indeed.

What about uniqueness, or we say *injection*, $T(v_1) = T(v_2) -> T(v_1 - v_2) = 0$? We use inner product with $<v_1 , A v_2>$.

$
  integral d^3 x phi_1 nabla^2 phi_2 &= integral d S phi_1 nabla phi_2 - integral d^3 x nabla phi_1 nabla phi_2\
  &= integral d^3 x phi_2 nabla^2 phi_1 + integral d S phi_1 nabla phi_2 - phi_2 nabla phi_1 \
$

For the operator $T(v) = 0$ and zero boundary condition would giving us a solely $integral d^3 x nabla v nabla v = 0$.

Where the positive definiteness, giving us $nabla v = 0 -> v = "constant"$. Thus the operator is injection up to constant.

A sight is, to take $A v_2 = delta_(i j)$, where $<v_1, A v_2> = sum_i <v_(1,i), A v_(2,i)> = sum_j v_(1,j) = v_1$. Such thing called green function:

Take equation (1.14):
$
  phi(x) = integral^3 d^3 G(x,x') f + integral d S phi nabla G - G nabla phi_2
$

For continuous space, it means $G$ almost everywhere zero. Which restrict to the volume inside boundary. It's also reasonable that there's multiple $sum_i delta(x - x_i)$ outside such volume. Because there are not in the solution volume inside.

Then we restrict boundary condition, if $phi|_S = 0$, then we take $G|_S = 0$. But, due to Gauss, $integral d S nabla G = integral d V nabla^2 G = 1$. Thus we can not take the other Neumann condition as $nabla G = 0$ also, but $nabla G = 1 / A$ for integration surface. Such constant helping us add a average surface integral $<phi>|_S$, which can be ignored.

We know operator is independent the coordinates, so we try spherical, the key is, rather strongly on gradient field, depends only $|r|$ rather $bold(r)$, because if not, there must be a curl. The metric must be something like $d r^2 + r^(n-1) d Omega^2$, where $f(Omega)$ is the component related to angle.

$
  nabla^2 &= 1 / (r^(n-1) f(Omega))(partial) / (partial r) (r^(n-1) f(Omega))(partial) / (partial r) \
  &= (partial^2) / (partial r^2) + (n-1) / r (partial) / (partial r) \
  &= (partial^2) / (partial r^2) / ((partial) / (partial r)) + (n-1) / r \
  &= (partial) / (partial r)(ln (partial / (partial r))) + (n-1) / r
$
We choose the integration constant as the $1 / A$ to fully cancel.
$
  phi(r) = cases(
    -1 / (2pi) ln r quad n=2,
    (1) / (n(n-2)alpha(n) r^(n-2)) quad n=3,
  )
$

$alpha(n)$ is the unit ball volume, and then $n alpha(n)$ is surface area.

Phew! That's mean every 3 dimension, the solution of green function must be like this, but may multiples of it as mentioned above $sum_i delta(x - x_i)$. However, to mimic the correction boundary condition, it's almost impossible to list many many of them.

That's the reason why images method comes in, we know that in spherical coordinates, we can expand the $phi(r)$ as sum of $P_l r^l$, which is indeed the same logic here.

So to solve a problem, we use images method to acquire a specific green function of a specific problem and then solve it by above, or else, choose specific series sum in specific problem(boundary condition), which, must be $nabla^2 phi = 0$ for almost all space, even green function is the solution because $nabla^2 phi = -q / epsilon_0 delta(...) -> phi = - q / epsilon_0 G$.

But usually, images methods can not acquire a solution for Neumann conditions, which is hard to derive the differential on surface. Thus, we suggest, rather directly the series solution, which directly, is the suggested green function as solution.

=== problem

List few you would better know.

Basic cylinder($j = 0$, no Bessel) :
$
  f(r, theta) = sum_(n=0)^infinity r^n (a_n cos n theta + b_n sin n theta)
$

Basic ball($phi.alt = 0$ invariant):
$
  f(r, theta) = sum_(n=0)^infinity (r^n P_l (cos theta) + r^(-(n+1)) P_l (cos theta))
$

Several procedure:

$
  nabla^2 phi = - q / epsilon_0 delta(r - r_0) \
  -> phi = -q / (4 pi epsilon_0) 1 / (|r - r_0|) \
$
or, even, dipole problem, which is a really, really close positive and negative charge yielding a differential on $delta$(Or you can directly use the before $P$ potential too):
$
  d = r_+ - r_- \
  R = (r_+ + r_-) / 2 \
  delta(r - r_+) = delta(r-(R_0 + d / 2))\
  delta(r - r_-) = delta(r-(R_0 - d / 2))\
  f(r)delta(r-r_0) -> f(r_0)delta(r-r_0)
$
$
  delta(r-R_0 - d / 2) &approx delta(r-R_0) - d / 2 nabla_(r-R_0) delta(r-R_0) \
  rho(r) &= q (-d / 2 - d / 2)(nabla_(r-R_0)(r -R_0))\
  rho(r) &= -q d nabla delta(r-R_0) = - p nabla delta(r-R_0)
$
Therefore:
$
  <G,nabla delta> = -<nabla G,delta> \
  nabla^2 phi = - (-p) / epsilon_0 delta'(r-r_0) \
  -> phi = - (-p) / (4 pi epsilon_0) (-(d ) / (d r)) (1 / (|r-r_0|)) \
  phi = 1 / (4 pi epsilon_0) p dot (r-r_0) / (|r-r_0|^3)
$
Coincide with previous $P$ potential.

- Suppose permittivity $epsilon_1$ ball, with a dipole $p_0$ inside the origin of ball. Then, outside is filled with permittivity $epsilon_2$, derive the potential.

For inside ball:
$
  nabla^2 phi = - p nabla delta(r) \
  -> G_0 = 1 / (4 pi epsilon_0) p dot (r) / (|r|^3) \
  phi = G_0 + G_i = G_0 + F(r, theta) = G \
  nabla^2 F(r,theta) = 0 \
  F(r,theta) = ("spherical series") \
  F(r,theta)|_(r->0) = "bounded constant" \
$

For outside hollow ball:
$
  nabla^2 phi = 0 \
  -> phi = F(r,theta) = G \
  F(r,theta) = ("spherical series") \
  F(r,theta)|_(r->infinity) = "bounded constant"
$

Now, we derive vacuum solution to match the boundary condition! For inside and outside, equal on surface in value and differential value.
$
  phi_1|_(r=a) = phi_2|_(r=a) \
  epsilon_1 (partial phi) / (partial r)|_(r=a) = epsilon_2 (partial phi) / (partial r)|_(r=a)
$

Actually if no addition term to correct it, we should see:
$
  a_l r^l P_l = b_l r^(-(l+1)) P_l \
  a_l (l r^(l-1)) P_l = b_l (-(l+1) r^(-(l+2))) P_l \
  -> a_l = b_l = 0
$
Thus, we can see many terms is zero unless there's a additional correction due to dipole or monopole etc...

Another you may be encounter is permittivity ball with given charge density $rho_f$.

Which is also the radial solution:
$
  nabla^2 phi = - rho_f / epsilon_0 \
  1 / r^2 (partial) / (partial r)(r^2 (partial) / (partial r)phi) = - rho_f / epsilon_0 \
  r^2 (partial) / (partial r) phi = - (rho_f r^3) / (3epsilon_0) \
  E = (partial / partial r) phi = - (rho_f r) / (3 epsilon_0) \
  phi = - (rho_f r^2) / (6 epsilon_0) + c_0
$
We discard the possible $1 / r$ order in integral.

So we minus that, we can acquire the vacuum solution too.

Another common situation is the outer charge effect the boundary condition, for example, still the ball.

In outer region:
$
  nabla^2 phi_1 = -q / epsilon_0 delta(x- a e_x) \
  phi_1 = q / epsilon_0 1 / (|r - a e_x|) + F(r,theta) \
  F(r,theta)|_(r-> infinity) = "bounded constant" \
$
In inner hollow region:
$
  nabla^2 phi_2 = 0 \
$

In boundary:
$
  phi_1|_(r=R_1) = phi_2|_(r=R_2) = phi_0 \
  "or" \
  integral - epsilon_1 (partial phi_1) / (partial r)|_(r=R_1) - epsilon_2 (partial phi_2) / (partial r)|_(r=R_2) = q_("ball")
$
Now, for $R_1 < a$:
$
  1/(|r-a e_x|) =  sum_0^infinity (r^l)/(a^(l+1)) P_l (cos theta) 
$

For potential constant condition:
$
  phi_2(R_2) = V_0 \
  -> phi_2(r) = V_0
$
Indeed, Faraday cave.
$
  phi_1(R_1) = V_0 \
  q_0/(4pi epsilon_0) sum_0^infinity (R^l/(a^(l+1))) P_l (cos theta) + sum_0^infinity D_l R_1^(-(l+1)) P_l (cos theta) = V_0 \
  l=0: quad q_0/(4pi epsilon_0 a) + D_0 R_1^(-1) =V_0 \
  l>0: quad (q_0 R_1^l)/(4pi epsilon_0 a^(l+1)) + D_l R_1^(-(l+1)) = 0 \
  D_l = - q_0/(4pi epsilon_0) (R_1^(2l+1))/(a^(l+1))
$

Which actually is the image charge:
$
  (R_1^(2l+1)/(a^(l+1))) = ((R^2)/(a))^l (R/a) \
  - q_0(R/a) sum_0^infinity ((R^2)/(a))^l r^(-(l+1)) P_l (cos theta) = -q_0(R/a) 1/(|r - (R^2)/a e_x|)
$

Or, charge condition:
$
  integral d S - epsilon_0 (partial phi_2)/(partial r)|_(r = R_2) = 0 = q_("in") \
  integral d S (- epsilon_0) (partial phi_1)/(partial r)|_(r=R_1) = q_("out") = q_("free") \
$
Plugin in:
$
  integral P_l (cos theta) sin theta d theta = 0 quad l > 0 \
  integral P_l (x) d x = integral P_l dot (1 = P_0) d x = 0
$

Thus, for two terms:
$
  integral d S l R_2^(l-1)/a^(l+1) P_l (cos theta) = 0 quad l >= 0 \
  integral d S (l+1) D_l R_2^(-(l+2)) P_l (cos theta) = 4 pi epsilon_0 D_0 = q_("free")\
  D_0 = R_2 (V_? - q_0/(4pi epsilon_0)) \
  V_? = phi_2 = q_0/(4pi epsilon_0 a) + q_("free")/(4pi epsilon R_2)
$

Yielding the results.

== Duality in Magnetics

We thus has the coincide:

$
  nabla times (B - mu_0 M) = mu_0 j \
  nabla times (1/mu_0 B -M) = j \
  nabla times H = j
$

In expansion, we see the first term is zero:
$
  integral d^3 x' j_i (x') &= integral d^3 x'j_j (x') partial_j (x'_i) \
  &= - integral d^3 x' x'_i partial_j j_j (x') \
  &= 0
$

Current isn't a fully correspondence of charge, because charge is native while current isn't. To maintain the current we need a battery, that's the reason why mechanical potential isn't equal to field potential. 

Usually, we only consider the second term which is already a 2-tensor:
$
  integral d^3 j_i (x) x_j &= integral d^3 x (partial_k x_i) j_k (x) x_j \
  &= - integral d^3 x x_i partial_k (j_k (x) x_j) \
  &= - (...) j_k (x) partial_k x_j \
  &= - (...) x_i j_j (x) \
  &-> j_i (x) x_j = 1/2 (j_i (x) x_j - j_j (x) x_i) \
  &= -1/2 epsilon_(i j k) (x times j)_k \
  &= - epsilon_(i j k) m_k
$

Thus we has: $epsilon_(i j k) x'_j m_k = x' times m $.

$
  A = mu_0/(4 pi) (m times x)/(r^3)
$

Then, introduce energy is just correction order by accumulating $x_i partial_i$ on $phi.alt_("ext")$:

$
  U = q phi -> - p dot E -> - 1/6 Q_(i j) partial_i E_j -> ... \
$

Now, interaction is a bit of interesting that $|x-x'| = |r-(x-y)|$ for $x$ in first charge distribution and $x' = r+y$ in another.

So it's just $1/r (x_i - y_i) partial_i$#footnote[The $partial_i$ is for $r$ which is the variable of $U$ and $x-y$ is integration variable only.] correction order on each other:

$
  U_("interaction") = (q_1 q_2)/(r) -> 1/r^3(q_2 d_1 dot r - q_1 d_2 dot r) \ -> 1/6 D_(i j)(r)(q_1 Q_2_(i j)(y) + q_2 Q_1_(i j) (x) - (d_(1 i) d_(2 j) + d_(2 i) d_(1 j) ))
$

Suppose a variation of $q$ on energy $U$, this gives the effect of potential on $q$.
$
  delta U &= phi delta q + q delta phi \
  &= phi delta q - F delta x
$
To acquire mechanical forces for fixed charges.

However, if we give a variation of $phi$ instead:
$
  delta hat(U) = - q delta phi - F delta x = delta U - delta(q phi) = -1/2 q phi
$
Which is the force for fixed potential.

That's the reason why mechanical potential of current and magnetic field is negative of field potential. Because we maintains a fixed potential for current: $U = 1/2 j A$.

Suppose a variation of $j$, this gives the effect of potential on $j$.

$
  delta U &= A delta j + j delta A \
  &= A delta j + j_i partial_j A_i delta x_j \
  &= A delta j + j_i 1/2 (partial_j A_i - (i <-> j)) delta x_j \
  &= A delta j + j_i epsilon_(k j i) B_k delta x_j\
  &= A delta j + epsilon_(j i k) j_i B_k delta x_j\
  &= A delta j + F_j delta x_j \ 
$
$
  (- ( -((partial U)/(partial x_j))_(j))) = F_j
$

We can see the force indeed, isn't negative here.

$
  delta hat(U) &= - j delta A + F delta x = delta U - delta(j A) \
$

Is the potential with fixed external potential.

The main idea is about coils, sometimes, we should take care that for a small range on cross section of a coil, we have $n d l = N$ is the total coil density. For example, on a hemisphere, we can round on it. Then the cross section is semi-circle, that's: $n d l = n R d theta -> n R integral d theta = n R pi/2 = N -> n = (2N)/(R pi)$. So it should be take care in this problem.

Another usual problem is to derive magnetic field, which is based on current or given boundary condition, but the latter is less common, because like previous we said, we should maintain a current based on potential, thus, the static magnetic field is always beyond the response like free charge on conductor.

The common model is just like electric field on surface, which is 2 dim -> 3 dim, which is plane and sphere, the corresponding model is 1 dim -> 2 dim, which is line and circle.

Suppose a line in $e_z$ direction:
$
  nabla^2 A = - mu_0 J e_z \
$

A common misunderstanding is to expand it like $nabla^2(A^i) e_i$. Which is wrong! The key is that it's not *tensor invariant*!

Now we apply this:
$
  e'_i = A e_i \
  v^i e_i = v'^j A^i_j A^(j -1)_i e'_j  = v'^j e'_j \
$

For a Cartesian coordinates, we have the original expanding:
$
  nabla^2(A^i) e_i &= nabla^2 (A'^j R^i_j) R^(j -1)_i e'_j \ 
  &= nabla^2 A'^j e'_j + (2 nabla A'^j nabla R^i_j R^(j -1)_i) e'_j + (nabla^2(R^i_j) A'^j R^(j -1)_i) e'_j 
$

Thus, the transformation suggests that:
$
  nabla^2(A^i e_i) &= nabla^2(A^i)e_i + 2 nabla (A^i) dot nabla (e_i) + A^i nabla^2(e_i) \
$

// Where $nabla(R^j_i) e'_j = Gamma^k_i e_k $, I abuse notation here, but forgive this now, we can't hold it any more because two differential must be another possible: $nabla (Gamma^k_i) e_k + Gamma^k_i Gamma^l_k e_l$ which is more complicated, should be the curvature term.

// So we should select $k = i$, thus, $nabla_i (R^j_i) e'_j = Gamma^i_i e_i$, thus second term is $2 nabla_i (A^i) Gamma^i_i e_i$, then same for third term: $nabla(Gamma_i^i)e_i + Gamma^k_i Gamma^i_k e_i$.
// 
We introduce below the calculation, which you may familiar if you know connection and Christoffel symbol:
$theta^i (e_j) = delta^i_j$, and $tau^i = d theta^i + omega^i_j and theta^j = 0$, with $omega^i_j = - omega^j_i$.

Whith $theta^i$ the one-form basis. And the matrix $omega^i_j$ the matrix styled connection.

$
  d r^2 + r^2 d theta^2 + d z^2 = d s^2 \
  theta^1 = d r, theta^2 = r d theta, theta^3 = d z \
$

$
  d (d r) = 0 \
  d (r d theta) = d r and d theta = - omega_r^theta and d r \
  d (d z) = 0 \
$

$
  0 = - omega_i^r and d x^i \
  d r and d theta = - omega^theta_i and d x^i \
  0 = - omega_i^z and d x^i
$

So only $omega^theta_r = 1 d theta$. Then $nabla_X e_j = omega^i_j e_i$.


$omega^theta_r (X) e_theta = nabla_X e_r, omega_theta^r (X) e_r = nabla_X e_theta$, Where $X = (partial)/(partial r) + 1/r (partial)/(partial theta) + (partial)/(partial z)$. You may acquainted with it that $omega^i_j (e_k) = Gamma^i_(j k)$.

$
  nabla_X e_r =  1/r e_theta \
  nabla_X e_theta = -1/r e_r \
  nabla_X^2 e_r =  -1/r^2 e_theta \
  nabla_X^2 e_theta = -1/r^2 e_r \
$
Then for $A_r$ in cylindrical coordinates:
$
  (nabla^2 A)_r = nabla^2 (A_r) - 2/r^2 (partial A_theta)/(partial theta) - (A_r)/r^2
$

Is the answer.

For spherical coordinates:

$
  d r^2 + r^2 d theta^2 + r^2 sin^2 theta d phi.alt^2 \
  d(d r) = 0 = d r and d r \
  d(r d theta) = d r and d theta = - omega_r^theta and d r \
$
$
  d(r sin theta d phi.alt) &= sin theta d r and d phi.alt + r cos theta d theta and d phi.alt \
  &= - omega^phi.alt_r and d r - omega^phi.alt_theta and (r d theta) \
$
$
  nabla_X e_r = omega_r^theta (X) e_theta + omega_r^phi.alt (X) e_phi.alt = 1/r e_theta + 1/r e_phi.alt \
  nabla_X e_theta = omega_theta^r (X) e_r + omega_theta^phi.alt (X) e_phi.alt = -1/r e_r + (cot theta)/r e_phi.alt \
  nabla_X e_phi.alt = omega_phi.alt^r (X) e_r + omega^theta_phi.alt (X) e_theta = - 1/r e_r - (cot theta)/r e_theta
$

Then you can calculate the vector Laplacian in spherical coordinates too.#footnote[You can use Euler-Lagrange equation to deduce Christoffel symbol too, but it can't gives you the relation between basis.]

So generally, we can't deduce it easily for specific coordinates. Even previous is actually very fast compared to directly calculate the identity: $nabla^2 A = nabla(nabla dot A) - nabla times (nabla times A)$.

It's reasonable to follow previous experience, we know $(r, theta + theta', z + z') equiv (r, theta, z)$, the invariance telling us that $A = A_z (r)$ indeed, that's, no *transformation* of $z$ in the process, so we apply it directly.

// $
//   nabla (R^x_r + R^y_r ) = 1/r (partial)/(partial theta)(cos theta + sin theta) \
//   nabla^2 (R^x_r + R^y_r) = 1/r (partial)/(partial theta)(1/r (partial)/(partial theta)) (cos theta + sin theta) \
//   -> nabla^2 A_r e_r + A_r/r^2 e_r
// $
// 
// Suppose $h_1 h_2 h_3 = sqrt(g) = kappa$
// $
//   nabla^2 (bold(A))_k = h^(-1)_k partial_k (kappa^(-1) partial_m (A_m kappa h_m^(-1))) - \ h_k kappa^(-1) epsilon_(k i j) partial_i (h_j (h_j kappa^(-1)epsilon_(j m l) partial_m (h_l A_l)))
// $

// For first term:
// $
//   h_k^(-1) partial_k (h_m^(-1) partial_m A_m + A_m kappa^(-1) partial_m (kappa h_m^(-1))) \
// $

// Second term:
// $
//   h_k kappa^(-1) epsilon_(k i j) epsilon_(j m l) partial_i (h_j^2 kappa^(-1) partial_m (h_l A_l)) \
//   // = h_k kappa^(-1) delta_(k m) delta_(i l) - delta_(k l) delta_(i m) (...) \
//   h_k kappa^(-1) epsilon_(k i j) epsilon_(j m l) (2 partial_i (h_j) kappa^(-1) partial_m (h_l A_l) + h_j^2 partial_i (kappa^(-1) partial_m (h_l A_l)) \
// $

$
  1/r (partial )/(partial r)(r (partial A_z)/(partial r)) = -mu_0 J 
$

$
  A_r = - (mu_0 J r^2)/4
$

The related boundary condition is also:
$
	e_r times 1/mu_1 nabla times A_1 = e_r times 1/mu_2 nabla times A_2
$

The final situation is related to response of bounded current. A magnetic conductor will be magnetized in magnetic field.

Suppose there's no free current, we has $nabla times H = 0$. Then $H = nabla phi$ for a unknown scalar potential.

$
  nabla dot B = nabla dot (mu_0 (H + M)) = 0 \
  nabla^2 phi = - nabla dot M = rho_("bound") \
$
Which is *magnetic charge*, we know the current is $nabla times M$.

Then, in linear model, we know $nabla dot M prop nabla dot B = 0$. That's, always zero. So in such classical problem, we always solve the vacuum situation, with such boundary condition:

$
  mu_1 (partial phi_1)/(partial r) = mu_2 (partial phi_2)/(partial r)
$

Some problem may denote specific relationship between $M$ and $B$ to classify a non zero $nabla dot M = rho_("bound")$.

And, some problem is the combination of two of them, that rotating free charge ball.

If $omega = omega e_z$:
$
  J_f (bold(r)) = rho_f (bold(r)) (omega times bold(r)) prop e_phi.alt
$
But it's zero in almost everywhere except on the ball, the serious solution to solve $A$ is still tiring, but the current formed vector potential must be porpotional to $e_phi.alt$, with invariance on $phi.alt$.

However, due to previous exposition, it's hard to solve this.
$
  nabla^2 A_phi.alt (r, theta) = 0 \
$

The only hope is to derive directly by source:
$
  A(bold(r)) &= integral d^3 x' (J(bold(r)))/(|r-r'|) \
  &= (mu_0 rho_f omega)/(4pi) integral_0^R integral_0^pi integral_0^(2pi) (r' sin theta')/(|r - r'|) hat(phi.alt') r'^2 sin d phi.alt' d theta' d r'
$

Then, for $A(bold(r)) = A hat(phi.alt)$, take inner product gives:
$
  hat(phi.alt)' dot hat(phi.alt) = cos(phi.alt - phi.alt') 
$

The problem first comes from the integration on $cos(phi.alt-phi.alt')/(|r-r'|)$, which the angle between $r$ and $r'$ is a unknown summation as $gamma$, we therefor expand it as unit vector product $cos gamma$:
$
  cos gamma = sin theta sin theta' cos(phi.alt - phi.alt') + cos theta cos theta' \
  P_l (cos gamma) = P_l (sin theta sin theta' cos(phi.alt - phi.alt') + cos theta cos theta') = sum Y^*(theta', phi.alt') Y(theta, phi.alt)
$

Why the end is the sum of harmonic spherical series? First, it's must be the expansion sum of basis $Y(theta, phi.alt)$, second, $P_l$ is a delta function valued on $cos gamma$, so it must be a valued expansion as $e^i e_j = delta^i_j$.

We denote only the factor difference($(2l+1)/(4pi)$ should be cancel out in integration of both side):
$
  Y (theta, phi.alt) prop sqrt((l-m)!/(l+m)!) P_l^m (cos theta) e^(i m phi.alt) \ 
  Y^*(theta',phi.alt') Y(theta, phi.alt) = sum_(m=-l)^(m=l) (l-m)!/(l+m)! P_l^m (cos theta') P^m_l (cos theta) e^i(m (phi.alt - phi.alt'))
$

Above omit the $0$ term is for clarity, we know from $-m $ to $m$, $0$ is only single term but others sum to $2$ terms.

$
  integral_0^(2pi) cos(phi.alt -phi.alt') sum_l 1/r_> ((r_<)/(r_>))^l (sum_(m<= plus.minus l) (l-m)!/(l+m)! P_l^m (cos theta') P^m_l (cos theta) e^i(m (phi.alt - phi.alt')) \
$
We observe that only same $m$ would filter out. That's $m=1$, $P^1_l$ only. But then looks at $sin^2 theta$, it's clear that it should be proportional to $sin^2 theta d theta ~ sin theta d cos theta ~ sqrt(1-cos^2 theta') d cos theta ~ sqrt(1 - x^2)$, higher terms disappear for $l > 1$ where $P^1_1 = sin theta$ already.

Ok, we only left $l=m=1$, $phi.alt$ integration is $pi$:
$
  theta "terms" = pi (r_<)/(r_>)^2 sin theta sin theta'  \
  integral_0^pi sin^2 theta' sin theta d (- cos theta') \
  = integral_(-1)^(1) (1-u^2)d u = 4/3 \
$
For radius part, we divide into two case, inner ball and outer ball.

Then for inner part, we should cleverly change $r_< <-> r_> ~ r <-> r'$ in integration:
$
  integral_0^R r'^3 r_</r^2_> &= integral_0^r r'^4/r^2 d r' + integral_r^R r'^3 r/r'^2 \
  &= r^3/5 + r(R^2/2 - r^2/2) \
  &= r R^2/2 - 3r^3/10 \
$

Outer part:
$
  integral_0^R r'^3 r_</r^2_> = 1/r^2 integral_0^R r'^4 d r' = R^5/(5r^2)
$

Combine coefficient: $mu_0 rho_f omega / 3 sin theta$ to yield the results.

You won't gonna do it again, sad story.

= Tensor

We know the energy, like so:
$
  u = 1/2 epsilon_0 E^2 + 1/2 1/mu_0 B^2 \
  S = 1/mu_0 E times B ~ E J  quad "energy flow" \
  P = epsilon_0 E times B ~ q/L^2 (F L^3)/(q V) =  (F L)/V ~ M V \
  F = rho (E + v times B)
$

$
  (partial u)/(partial t) + nabla dot S = E dot J
$

Stress tensor is much harder to derive. Which is like:
$
  E_i E_j - 1/2 delta_(i j) E^2 + (E <-> B)
$
With:
$
  partial_i T_(i j ) = (partial P_i)/(partial t) + F_i
$

$
  E = - nabla phi.alt - (partial)/(partial t) A \
  B = nabla times B \
  (phi.alt , bold(A)) -> (phi.alt + (partial theta)/(partial t), bold(A) - nabla theta) quad "invariant" -> "lorentz"...
$

Here it can be more intuitive...

= Radiation

$
  A^mu (t,upright(x)) = mu_0 / (4pi)integral d^3 x' (j^mu (t-(|upright(x)-upright(x')|) / c,upright(x'))) / (|upright(x)-upright(x')|)
$

$upright(x) = r hup(n)$ and $|x'| < d$

For $r -> infinity$, then $|x-x'| -> |x| = r >> |x'| < d$.

$
  #four_p = mu_0 / (4 pi) 1 / r integral d^3 x' j^mu ((t-r / c+ (hat(up(n)) dot up(x)') / c) , up(x')) + O(1 / r^2)
$

We are only interested in part of $O(1 / r)$ for radiation.

#let iomegac = $i omega / c$
#let nxs = $hup(n) dot up(x')$
#let e_p = $e^(-i omega dot hup(n) dot up(x)'\/c)$
#let partialt = $(partial) / (partial t)$
$
  partial_i #e_p = - i omega / c (partial_i n_j) x'_j #e_p
$
$
  partial_i n_j &= partial_i (x_j / r) = delta_(i j) / r - x_j / r^2 partial_i r \
  &= 1 / r (delta_(i j) - (x_i x_j) / r^2) = 1 / r (delta_(i j) - n_i n_j)
$
We found that the plus $1 / r$ contribution could be neglected.

We only need:
$
  partial_i e^(iomegac r) = iomegac partial_i (r) e^(iomegac r) = iomegac n_i e^(iomegac r)
$

Thus:
$
  up(E) &= - (nabla phi.alt + partialt up(A))\
  &= 1 / (4pi epsilon_0)1 / r integral d^3 x' integral (d omega) / (2 pi) i omega / c^2e^(-i omega [t -(r / c) + (hup(n) dot up(x)') / c])(up(j)(omega,up(x')) - c hup(n) rho(omega, up(x')))\
$

Or:
$
  up(E) &= 1/(4 pi epsilon_0 r) integral d^3 x' 1/c partial_t rho((t - r/c + ...),x') n_i - 1/c^2 partial_t j_i ((...),x') \
  &= 1/(4pi epsilon_0 c^2 r) partial_t integral d^3 x' c rho(...) n_i - j_i (...) \
$

$
  c rho = n_i j_i \
  (j^i n_i) n_i - j_i -> (n dot j) n - j = j_(perp) \
$

$
  up(E) = -1/(4 pi epsilon_0 c^2 r) partial_t integral d^3 x' j_(perp) (...)
$

Notice that we can do fourier transform on $e^(- i omega nxs / c)$
$
  up(E)(t,up(x)) = 1 / (4 pi epsilon_0 c^2) 1 / r integral (d omega) / (2pi) e^(-i omega (t-r / c)) i omega [up(j)(omega, omega hup(n) / c) - c hup(n) rho(omega, omega hup(n) / c)]
$

We know in continuity that:
$
  omega rho(omega, up(k)) - up(k) dot up(j)(omega,up(k)) = 0 \
  k = omega hup(n) / c \
  c rho(omega, omega hup(n) / c) = up(n) dot up(j)(omega,omega hup(n) / c)
$
$
  up(E)(t,up(x)) = (...)integral (d omega) / (2pi) (...) i omega [up(j)(omega, omega hup(n) / c) - hup(n) (hup(n) dot up(j)(omega, omega hup(n) / c))]
$
We write last term as: $up(j)_(perp)(...) = - hup(n) times (hup(n) times up(j)(...))$.

Notice that $i omega e^(- i omega t) = - partial_t e^(-i omega t)$
$
  up(E)(t,up(x)) &= -(...)1 / r partial_t integral (d omega) / (2pi) e^(-i omega (t - r / c)) integral d^3 x' d t' e^(i omega t' - i omega nxs / c) up(j)_perp (t',up(x')) \
  &= - (...)1 / r partial_t integral d^3 x' d t up(j)_perp(t', up(x')) delta(t' - (t- r / c + nxs / c)) \
  &= - (...)1 / r partial_t integral d^3 x' up(j)_perp (t- r / c + nxs / c , up(x'))
$

We know $up(B)(t,up(x)) = nabla times up(A)$, So it just as:
$
  c up(B) / mu_0 = epsilon_0 c^2 hup(n) times up(E) \
  c up(B) = hup(n) times up(E)
$

$
  up(S) &= 1 / (mu_0 c) E^2 hup(n) \
  &= epsilon_0 c E^2 hup(n) \
  &= epsilon_0 c 1 / (4pi epsilon_0 c^2 r)^2(...)
$
$
  (d cal(E)) / (d t d Omega) &= epsilon_0 c (1 / (4pi epsilon_0 c^2))|partial_t integral d^3 x' up(j)_perp (t- r / c + nxs / c, up(x'))|^2 \
$

We can also transform to frequency domain, based on previous electric field in frequency domain:
$
  (d cal(E)) / (d t d Omega) &= (...) omega^2|up(j)_perp (omega, omega hup(n) / c)|^2 \
$
And we can transform back to explicit source term:
$
  |hup(n) times (hup(n) times up(v))| = |hup(n) times up(v)|
$

By continuity equation that $c rho ~ hup(n) dot up(j)$
$
  |up(j)_perp (...)|^2 &= |hup(n) times up(j)(...)|^2 =|up(j) - hup(n) c rho(...)|^2 \
  &= |up(j)|^2 - 2 c rho(...) (hup(n) dot up(j)) + c^2 rho^2(...) \
  &= |up(j)|^2 - c^2|rho(...)|^2 \
$

== Low-Frequency Limit

In $#e_p$, we see that $|x'| < d$, if we want to expand this term, we should restrict that $(omega' d) / c << 1$. Which go quickly to zero for large $omega'$.

Thus for a source with typical frequency: $omega_s ~ v / d$, we know that $v << c$. or $lambda_s = c / omega_s >> d$.

$
  up(E)(t,up(x)) &= -(...)1 / r partial_t integral (d omega) / (2pi) e^(-i omega (t - r / c)) integral d^3 x' d t' e^(i omega t' - i omega nxs / c) up(j)_perp (t',up(x')) \
$

Suppose we only localize the source with $delta(t' - (t - r / c))$, turn $-i omega ~ partial_t$. Expand the term $#e_p$:
$
  partial_t sum_k integral d^3 x' 1/(n!) (partial_t hup(n) dot up(x') / c)^k up(j)_perp (t-r / c, up(x')) \
  partial_t sum_k (hup(n) dot )^k  (partial_t)^k integral d^3 x' 1/(n!) up((x' / c))^k up(j)_perp (t-r / c, up(x')) \
$
Thus we expand those terms like $n_i \/ x_i$, $n_i n_j \/ x_i x_j$, $n_i n_j n_k \/ x_i x_j x_k$ and so on...

$
  up(j)_perp (t-r / c, up(x')) &= up(j)(t - r / c, up(x')) - hup(n) (hup(n) dot up(j)(t - r / c, up(x'))) \
  &= up(j)(t - r / c, up(x')) - hup(n) c rho(t-r / c, up(x')) \
$

Notice a addtional $partial_t$ in front of resulting $partial_t^(k+1)$

A useful check is that $up(j) ~ v q; 1 / c^2 partial_t up(j) ~ (omega_s q v) / c^2 ~ q / d (v / c)^2$ is already second order, and $c partial_t rho$, one order, is zero because whole integral is a constant. Thus start from $1 / c^3 c partial_t^2 rho x'_i ~ 1 / c^2 dot.double(d) ~ (omega_s^2 q d) / c^2 ~ q / d v^2 / c^2$ again second order.

That's means all radiation terms start from $(v / c)^2$ order and disappers in $v -> 0$ for static limit.

We check the second order which is the first term:

$
  integral d^3 x' up(j)(t,up(x')) &= integral d^3 x' j_k (t,up(x')) partial_k x^i
  &= - integral d^3 x' x_i partial_k j_k (t,up(x')) \
  &= partial_t integral d^3 x' rho(t, up(x')) x_i \
  &= dot(d)_i (t)
$

Thus:
$
  up(E)(t,up(x)) = - (1) / (4 pi epsilon_0 c^2) 1 / r (dot.double(up(d))(t - r / c) - hup(n) (hup(n) dot dot.double(up(d))(t - r / c))) \
$

Then, for third order:
$
  partial^3_t integral d x'^3 rho(...) x'_i x'_j = dot.triple(Q)_(i j)
$
Where $nabla dot j = - partial_t rho$
$
  partial^2_t integral d^3 x' j_i x_j &= partial^2_t - integral d^3 x x_i partial_k (x_j j_k) \ &= partial^2_t (- integral d^3 x x_i j_j  + partial_t integral d^3 x' rho x_i x_j) \
$

We split into symmetric and antisymmetric part corresponding to:
$
  (...) n_j = n_j (1/2 dot.triple(Q)_(i j) - epsilon_(i j k) dot.double(m)_k) \
$

If we choose $Q_(i j)n_j = Q_i $, just to get with:

$
  1/(4pi epsilon_0 c^3 r^2) (1/2dot.triple(Q)_(perp)) "or" (...) 1/6 dot.triple(D)
$

== Problem

It's easy to calculate approximation four-potential by removing the additional $partial_t$, and the corresponding $perp$.

For example, $dot.double(d)_perp = hat(n) times (hat(n) times dot.double(d))$ for $E$, then it's useful to notice that:
$
  B = 1/c hat(n) times E &= 1/c hat(n) times - (dot.double(d) - hat(n) (hat(n) dot dot.double(d))) \
  &= 1/c dot.double(d) times hat(n) 
$

So usual problem is to calculate corresponding order of $p \/ d$ and even higher order $D$ to acquire $E\/B$ and $S$ energy flow.

Some problem will also makes you calculate $p$ first and then gives it a small vibration to yielding a radiation.

- Suppose a $p_0$ with a small vibration, calculate the radiation and energy flow.

$
  p(t,x) = e_z p_0 e^(i omega t) quad dot.double(p) = - omega^2 p = -omega^2 p_0 e^(i omega t)e_z  \
$

For magnetic field, it's second order, so must has $1/c^2$, but we also know it should be $1/c E$, which is $1/c^3$ indeed, second, we should be careful that the time is $t-r/c$ rather $t$ solely.
$
  B = -1/(4 pi epsilon_0 c^3 r) omega^2 e^(i omega (t - r/c)) p_0 e_z times e_r
$

$
  e_r = sin theta cos phi.alt e_x + sin theta sin phi.alt e_y + cos theta e_z \
  e_phi.alt =1/(sin theta)(sin theta (- sin phi.alt) e_x + sin theta cos phi.alt e_y) \
  e_z times e_r = sin theta e_phi.alt
$
#footnote[Use cylindrical is simpler, but the results is different, which is not $sin theta$ here.]

$
  B = (...) sin theta e_phi.alt \
  E = c B times e_r = (...) sin theta e_theta \
$

Then, the energy flow is:
$
  chevron.l S chevron.r  &= 1/2 (epsilon_0 E times B) \
  &= (omega^4 p_0^2)/(32 pi^2 epsilon_0 c^5 r^2) sin^2 theta e_r
$

You can integrate this to yielding total radiation power.

Then, the basic starting point, how to calculate $p$ is somehow need to be pondered.

For example, a circling electron:
$
  p = e r_0 (cos omega t e_x + sin omega t e_y) \ 
  p = e r_0 (e_x - i e_y) e^(i omega t) \
  dot.double(p) = - omega^2 e r_0 (e_x - i e_y) \
$

Or else, you may encounter $m$ as magnetic dipole:
$
  m = 1/2 integral d l x times j \
$

However, based on previous we know:
$
  integral d^3 x j_i (t,x) = - integral d^3 x x_i partial_k j_k (t, x) = partial_t integral d^3 x rho(t, x) x_i = dot(d)_i (t)
$

So, we can derive it as(the summation is for many dipoles, rather coordinates):
$
  m &= 1/2 sum_alpha x_alpha times dot(d)_alpha \
  d_alpha &= plus.minus p_0 e^(i omega t) e_x \
  x_alpha &= plus.minus a/2 e_z \
  m &= 1/2 (a/2 e_z times d_1 - a/2 e_z times d_2) \
  m &= a/2 e_z times d = a/2 e_y i omega p_0 e^(i omega t)
$

For quadruple, you should calculate as tensor, and then apply:
$
  Q_(i j) n_j = Q_(i j) e_i e_j dot e_r \ 
  n_j = e_r \
  e_r = sin theta cos phi.alt e_x + sin theta sin phi.alt e_y + cos theta e_z \
$

To yield correct results.

The final comments is, for static current or charge, it won't radiates, at least, it should has acceleration! Also, just like static multipole expansion, if the distribution of charge is symmetric, it won't contribute to the final answer:
$
  p_1 + p_2 = (p_0 - p_0) e^(i omega t) = 0
$

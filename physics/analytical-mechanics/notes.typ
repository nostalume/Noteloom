#import "../lib.typ": *

#show: mine.with(
  title: "Review of Classical Mechanics",
  eq-numbering: "(1.1)",
  eq-chapterwise: true,
)

#let inpro(l: none, r: none) = {
  let l = if l == none {
    h(0.5em)
  } else {
    l
  }

  let r = if r == none {
    h(0.5em)
  } else {
    r
  }

  $chevron.l #l , #r chevron.r$
}

= Coordinates

Classical mechanics is for a given coordinates $(q_1,...,q_n)$, and a single parameter $t$, given a insertion with $(q_1 (t),...,q_n (t))$ for $phi.alt: [0,1] -> M$ to describe mass points.

We introduce few usual coordinates:
$
  (x,y,z) \
  (x = r cos theta, y = r sin theta, z = z) \
  (r = r sin theta cos phi, y = r sin theta sin phi, z = r cos theta)
$

Then we can describe a unit vector field on such coordinates transformation.
$
  (partial ) / (partial r_i) = (partial x_j (r_1,...,r_n) := partial f(x_j)) / (partial r_i)(partial) / (partial x_j)
$

We take inner product in standard metric of $x,y,z$, Euclidean metric, to acquire a metric of given field. For example, in spherical coordinates:

$
  g_(i j) = inpro(l: partial_i, r: partial_j) \
  g_(i j)d x^i d x^j = d r^2 + r^2 d theta^2 + r^2 sin theta^2 d phi^2
$

Then given a distance action variation, we seek minimal:
$
  delta S = delta integral d t g_(i j) d x^i d x^j \
  dot.double(r) - r dot(theta)^2 - r sin theta^2 dot(phi)^2 = 0 \
  (d r^2 dot(theta)^2) / (d t) - r^2 sin theta cos theta dot(phi)^2 = 0 \
  (d r^2 sin theta^2 dot(phi)) / (d t) = 0
$

Take $sin theta = 1$, we give the plane motion too.

We can also understand it as a parametrization by $t$ for each direction that:
$
  v^i partial_i = (partial x_i) / (partial t) partial_i \
$

Normalize to:
$
  v^i e_i = v^r e_r + v^theta e_theta + v^phi e_phi \
  (D (v^i e_i)) / (d t) = ...
$
We differentiate by decompose it as Euclidean vector field first, and then summarize.

Natural coordinates must be given in a explicit coordinates to identify, for example, if we given a distance like $d = R theta = R t$, it can be a direct path or circle too.

Given a unit vector, decompose to field along $v$ and perpendicular, is actually a insertion of single parameter $phi.alt: [0,1] -> bb(R)^3$
$
  v^i e_i = v tau = (partial s) / (partial t) tau
$
Where $tau$ is parallel with $v$.
$
  inpro(l: tau, r: tau) = 1 \
  inpro(l: (D tau) / (d t), r: tau) + (tau <-> (D tau) / (d t)) = 0
$
Given a unit vector $n = (D tau) / (d t) (1) / (|(D tau) / (d t)|$.

Actually, there's a parametrization difference on $s$ or $t$, indeed we can let $s$ be time itself, but currently we choose:

$
  (D tau) / (d s) (d s) / (d t) = kappa v n \
  a_n = v (kappa) v = v^2 kappa \
  kappa = 1 / rho \
$

We take cross product:
$
  v tau times (tau dot.double(v) + v^2 kappa n) = v^3 kappa b
$
So $kappa = 1 / rho = |upright(v) times upright(a)|$.

== Variable Mass

Suppose a rope or chain falling from a hole in a frictionless, smooth horizontal table, let $y$ be the lower end respect to the table top of falling chain.

Such problem can be formulated by a additional metric called inertia metric carrying along coordinates. $inpro(l: dot(q), r: dot(q))_M(q)$.

Where $dot(q)$ is unrelated to $q$.
$
  inpro(l: dot(q), r: dot(q))_M(q) =1 / 2 integral rho(q) dot(q)^2 d q \
  = 1 / 2 dot(q)^2 integral rho(q) d q \
  U(q) = integral U_rho (q) d q \
$

For rocket, we has a general force upon $Q = (d m) / (d t) u = - (d M)/(d t) u$ which is momentum flux, causing the energy non-conservative, which can be considered as convection. Therefore, for environment, we has no $M dot(u)$ for its acceleration, and due to inelastic collision:

$
  - (d M)/(d t) u + p = p' = p + (d p)/(d t) \
  (d p)/(d t) = Q \
  (d p)/(d t) = - (partial H)/(partial q) + Q
$

The chain above is $M = rho y$, thus giving us $T = 1 / 2 (rho y) dot(y)^2$:

$
  L = 1 / 2 rho y dot(y)^2 - integral rho g y d y = (...) - rho g y^2 / 2 \
  rho(dot(y)^2 + y dot.double(y)) - (1 / 2 rho dot(y)^2 + rho g y) = 0 \
  y dot.double(y) + 1 / 2 dot(y)^2 - g y = 0 \
  dot.double(y) = 0 -> dot(y)^2 = 2 g y \
$
Is the equation of motion in stable case.

If it falls on ground, we has $f = rho s g + rho (d y) / (d t) (v) = rho s g + rho v^2$ where $s$ is the part already fallen on ground.

= Rotation

Suppose a variation of speed on $"SO"(3)$,resulting a additional $v' <- v + omega times r$ for coordinates $x,y,z$.

$
  (v + omega times r)^2 = v^2 + 2 v dot (omega times r) + (omega times r)^2 \
  delta S -> dot(v) + (dot(omega) times r) + (omega times v) - (- (omega times v) - omega times (omega times r)) \
  = dot(v) + (dot(omega) times r) + 2(omega times v) + omega times (omega times r) = dot(v)'
$

$
  dot(v) tilde -2 (omega times v)
$
Monsoon, due to season transformation:

In summer, continent are heated by sun and ocean warms slowly so is relatively cool, then pressure gradient is from ocean to continent, which is the trade wind, which in southern hemisphere, will be deflected by Coriolis force to the right. Forming the southwest monsoon.

In winter, everything reverse, that continent is cooler relatively and ocean is warmer. Then forming the northeast monsoon.

- The Intertropical Convergence Zone: near the equator, air heats up, creating low pressure.

- High Pressure Zone of Subtropical Belt: located near the latitude of 30 Degrees North and south, high-altitude air deposition sinking, forming a high pressure.

- Low Pressure Zone of Subpolar Belt: located near 60 degrees north and south latitude, the prevailing westerly and polar easterly encounter, air rise, forming a low pressure.

- High Pressure Zone of Polar: located near the north and south poles, the air sinks due to cold, forming high pressure.

== Rotation on Earth

Now we exploit effect of centrifugal acceleration:
$
  g_("eff") = g - omega times ( omega times r)
$

In earth surface, we has $r approx R$. We exploit that:
$
  |omega times (omega times r)| = | omega (omega dot r) - omega^2 r| = |-omega^2_(perp) r| = omega^2 r sin theta
$

$
  g^(parallel)_("eff") = g - omega^2 R sin^2 theta \
  g^(perp)_("eff") = omega^2 R sin theta cos theta \
  alpha approx tan alpha = (g^(parallel)_("eff")) / (g^(perp)_("eff")) = ...
$
Which is small that $theta = 45 degree -> alpha = 0.0088degree$.

Thus for Coriolis force:
$
  a' = g_("eff") - 2 omega times v' \
  upright(omega) = omega cos lambda upright(j') + omega sin lambda upright(k') \
  g_("eff") = - g upright(k') \
  2 upright(omega) times upright(v') = 2((omega dot(z) cos lambda - omega dot(y) sin lambda) upright(i') + (omega dot(x) sin lambda) upright(j') - (omega dot(x) cos lambda)upright(k')) \
$
Suppose the zero order of $omega$:
$
  dot.double(y) = - 2 omega dot(x) sin lambda approx 0 \
  dot.double(z) = - g + 2 omega dot(x) cos lambda approx -g \
  dot.double(x) = - 2 omega(dot(z) cos lambda - dot(y) sin lambda) approx -2 omega dot(z) cos lambda \
  x = 1 / 3 omega g t^3 cos lambda
$
Is the free fall effect($z = h, dot(z) = 0$), point to the east in right hand direction from angular velocity.

Otherwise a initial speed with $dot(z) = v_0$ giving us:
$
  x = 1 / 3 omega g t^3 cos lambda - omega v_0 t^2 cos lambda \
  v = (2 v_0) / g \
  x = (8 / 3 - 4)(...) = -4 / 3 omega v_0^3 / g^2
$
Which is negative, due to the velocity surrounding in earth can't catch velocity in its corresponding altitude. Indeed, we see if we throw a ball, fall down to ground, it has no deflection because up and down cancelled out.

Another thing is about weather system. For a fluid of gas, equation can be formulated as:
$
  rho upright(a) = - nabla P - rho(2 omega times upright(v) - omega times (omega times r)) \
$

Assuming balance of $upright(a) approx 0$:
$
  plus.minus v^2 / r = 1 / rho nabla P - 2 v omega sin lambda
$
The key is the high pressure in outward or low pressure inward.
$
  v = plus.minus ( - r omega sin lambda + sqrt((r omega sin lambda)^2 plus.minus (r / rho) nabla P) ) \
$
So if it's minus, is a high pressure system and weak pressure gradient.

Another final useful problem is, a dancer can draws her arms to change inertia and cause a different angular frequency. But what's the force cause this?

In comoving system of dancer, we have:
$
  m dot(v) = m dot(omega) r = - 2 m omega times dot(r) \
  dot(omega) = - 2 omega dot(r) / r \
  dot(p_theta) = (d) / (d t)(m r^2 dot(omega)) = m r^2 dot(dot(omega)) + 2 m r dot(r) dot(omega) \
$
Plugin in:
$
  dot(p_theta) = 0
$
That's constant indeed in rotation system. But its energy increases due to the change of inertia to against the centrifugal force:
$
  E_("rot") = (p_theta)^2 / (2 I)
$

== Gyro

Suppose a gyro affected by gravitation.

$
  tau_s = (d sin phi.alt hat(r) + d cos phi.alt hat(k)) times (m g - hat(k)) = m g d sin phi.alt hat(theta)
$

We know the self rotation is:
$
  omega_s = - omega_s sin phi.alt hat(r) - omega_s cos phi.alt hat(k) \
  L_("cm") = I_"cm" omega_s \
$

Now, the rotation of angular momentum of mass center is:
$
  (d L_("cm"))/(d t) = - I_"cm" omega_s sin phi.alt (d hat(r))/(d t) = (...) omega_z hat(theta) = tau_s
$

Equal both side yield:
$
  omega_z = - (m g d)/(I_("cm") omega_s)
$

So when the self angular velocity is very high, the precession is actually slower.

== Instant Center

We often comes, in rigid body we need to decompose the solely rotation effect:
$
  v_s = v_0 + omega times (r_s - r_0) \
$

If $v_s = 0$:

$
  v_0 = omega times (r_0 - r_s) \
$

That's we only need to know where $r_s$ is to acquire it, it's often useful in 2-dim because two lines intersect one points, which, given two velocity of two points in rigid body, from equation we know it must be perpendicular to the $r_0 - r_s$, and $omega$ must be in $e_z$ direction, thus, $r_0 - r_s$ must be in the plane and perpendicular to both velocity.

For example, a rolling disk, assume a comoving coordinates with disk center:

$
  v_"bottom" = v_0 hat(x) + (-v_0) hat(x') = v_0 hat(x) - v_0 hat(x') = 0
$

So it's the instant point here.

It's also common to solve the instant center trajectory, and expressing both in fixed coordinates and comoving coordinates in rigid body.

$
  x_"bottom" = omega R t hat(x) - R hat(y)\
  x_"bottom" = 0 hat(x)' - R hat(y)
$

Sometimes, it's rather a geometry problem to solve this, because using parameter function may be redundant here.

== Problem Sheet

A common falsification is to differentiate $v$ in rotation coordinates in answer.

For a rotating wheel at peek and bottom:
$
  v = 2 v_0 hat(i) -> v_0 hat(i) + v_0 hat(i') \
  (d v) / (d t) = 2 v_0 omega hat(j) = 2 v_0^2 / r hat(j) quad (#text[Wrong!]) \
  a = omega times (omega times O P) = - omega hat(k) times (- omega hat(k) times (r cos theta hat(i) + r sin theta hat(j))) \
  ~ - (v_0^2 / r) hat(j)
$

At bottom:
$
  v = 0 -> v = v_0 hat(i) - v_0 hat(i') \
  (d v) / (d t) = ??? \
$
Which is wrong if we take derivative against already "valued" vector, you see the second term is where original deduction of acceleration comes in to derive centrifugal force, rather a "valued" zero in the results. Because we usually set $O'$ coincide with $O$ in every instant time to ease our burden.

- A cone with height $h$ and point angle $2 alpha$, no-slipping scroll on a surface, calculate the acceleration of the peak of underside.

In the base of underside, is the instant center.
$
  omega_1 h cos^(-1) alpha + omega_2 h tan alpha = 0 \
  omega_1 = - omega_2 sin alpha \
  omega_1 = omega_1 upright(k) \
  omega_2 = -omega_1 sin^(-1) alpha (cos alpha upright(i') + sin alpha upright(k)) \
  omega = omega_1 + omega_2 = - omega_1 cot alpha upright(i')
$
In the peak of underside:
$
  v &= (omega_1 + omega_2) times r_A = - omega_1 cot alpha upright(i') times (h cos alpha^(-1)(cos 2 alpha upright(i') + sin 2 alpha upright(k'))) \
  &= omega_1 sin^(-1) alpha h sin 2alpha upright(j') \
  &= omega_1 h 2 cos alpha upright(j') \
$
Now, $r_A$ is $r_A_(O'')$:
$
  a &= (d omega) / (d t) times r_A + omega times (omega times r_A) \
$
Here the handling is to separate:
$
  d(omega_1 + omega_2) / (d t) ~ d(omega_1_O + omega_2_O') / (d t) \
  = ((d) / (d t))_O (omega_2_O') + omega_1 times omega_2 = omega_1 times omega_2
$
$
  a &= (omega_1 times omega_2) times r_A + omega times (omega times r_A)
$

So the key is to separate coordinates for each:
$
  ((d) / (d t))_O omega_(O'') &= ((d) / (d t))_O' omega_(O'') + omega_1 times omega_O'' \
  &= ((d) / (d t))_(O'') omega_(O'') + omega_2 times omega_O'' + omega_1 times omega_(O'')
$
Usually we set $O = O'$ in instant time to ease burden.

- Estimating the relationship between Gyro rotation and precession.

$
  tau = r times F = (d sin phi hat(r) + d cos phi hat(k)) times (m g - hat(k)) = m g d sin phi hat(theta) \
$

For a large, and nearly constant $omega_s$ as self-spin.
$
  L_("spin") = - I_("cm")(omega_s sin phi hat(r) + omega_s cos phi hat(k)) \
  (d) / (d t) L_("spin") = - I_("cm") omega_s sin phi omega_z hat(theta) \
  (d) / (d t)(theta) = omega_z \
$

$
  m g d sin phi hat(theta) = - I_("cm") omega_s sin phi omega_z hat(theta) \
  omega_z = - (d m g) / (I_"cm" omega_s)
$
When we see that gyro nearly topple over, it process faster with greater leaning angle.


= Lagrange and Hamilton

== Hamilton Jacobi

$
  delta S = integral d t (delta p_i dot(q)_i + p_i delta dot(q)_i - (partial H) / (partial p_i) delta p_i - (partial H) / (partial q_i) delta q_i) \
$
Read that:
$
  dot(q_i) = (partial H) / (partial p_i) quad dot(p_i) = -(partial H) / (partial q_i)
$

Suppose action called $W(q,t) = S[q,dot(q),tau]|^t = integral^t d tau L(q,dot(q),tau)$

First way is to quote $delta Q$.
$
  d q = delta q + dot(q) delta t\
  delta Q = delta W = p delta q + L delta t \
  delta W = p d q + (L - p dot(q)) delta t \
$
or:
$
  integral^t delta L d tau + L delta t \
  integral^t ((partial L) / (partial q) - (d) / (d tau)(partial L) / (partial dot(q))) delta q d tau + [(partial L) / (partial dot(q))delta q]^t
$
Note we are in the actual path, thus integral term is zero.
$
  delta W = p delta q + L delta t
$
same results.

Plugin back as $delta -> d$ for variation on the variable itself for actual path giving us:
$
  (d W) / (d t) = (partial W) / (partial q_i) dot(q)_i - (partial W) / (partial t) = L \
  (partial W) / (partial t) = -H \
  (partial W) / (partial q_i) = p_i
$

Now $W(q,t) = W(q(t),t)$ after integral of upper bound. So we doesn't differentiate respect to $tau$, rather to $t$ itself at end point.

Insert into Hamiltonian:
$
  cal(H) = (partial W) / (partial t) + H(q, (partial W) / (partial q_i), t) = 0 \
  (partial cal(H)) / (partial Q) = dot(P) = 0 \
  (partial cal(H)) / (partial P) = -dot(Q) = 0\
$
The last two equation is due to that $cal(H) = 0$.

#let ptl = $partial$
So:
$
  {q_i,p_i}_(Q_i,P_i) := (partial q_i) / (partial Q_i)(partial p_i) / (partial P_i) - (partial q_i) / (partial P_i)(partial p_i) / (partial Q_i) := 1
$
The last is due to independence of coordinates.

Thus we choose $W(q_i (Q,P),t;P_i,Q_i)$ with constant $P_i$ and $Q_i$.
$
  &(partial q_i) / (partial Q_i)((partial^2 W) / (partial P_i partial q_i) + (partial^2 W) / (partial q^2)(partial q) / (partial P_i)) - (partial q_i) / (partial P_i)((partial^2 W) / (partial q_i partial Q_i) + (partial^2 W) / (partial q^2)(partial q) / (partial Q_i)) \ &= (partial q_i) / (partial Q_i)(partial) / (partial q_i)(partial W) / (partial P_i) - (partial q_i) / (partial P_i)(partial) / (partial q_i)(partial W) / (partial Q_i) := 1
$

A selection tells us that $(ptl W) / (ptl P_i) = 1 / 2Q_i$ and $(ptl W) / (ptl Q_i) = -1 / 2 P_i$. Much like $cal(H)$ with factor $1 / 2$. However, It's fuzzy for solving original equation because they are all constants. But how do we know which is the new constant momentum or position? Actually, we select constant in separation, indeed, they are must be $Q_i (q_i, p_i, t)$ etc.

Suppose constant energy $E = H = -(ptl W) / (partial t)$.
$
  (partial W) / (partial E) = 1 / 2 Q_i \
  (partial W) / (partial Q_i) = -1 / 2 E \
$
Thus we immediately know that $Q_i = 2t$.

However, it would be tiring to select $P_i$ or $Q_i$. Rather we only know one each constants by separation in solving. For example, we know a group constant $alpha$, in a bunch of functions $W_i (q,P?,Q?) = f(q,alpha)$. We can simply use the first or second based on what we know without bothering the other, which are symmetric.

Thus we can simply choose $(ptl W) / (ptl P_i) = Q_i$ or $(ptl W) / (ptl Q_i) = -P_i$. While discarding dependency on the other.

This gives us that $(partial W) / (partial P_i) = Q_i$.

Suppose we can separate for $q_i$:
$
  W(q_i,t;P_i) = sum_i W_i (q_i;P) + W_t (t;P) \
$

If there's energy conservation:
$
  (ptl W) / (ptl t) = (ptl W_t) / (ptl t) = -E \
$
We simply set $W_t = -E t$ because extra constants can be omitted.
$
  W(q_i,t;P_i) = sum_i W_i (q_i;P) - E t \
  E = H(q, (ptl W) / (ptl q_i),t)
$
Is the separation. We exploit that separation is to choose $W_i (q_i;P)$ with solely $q_i$.

Take a further step, if there's only explicit $p_i$ in $H$, we know that separation can factor solely constant related to $p_i = P_i = (ptl W) / (ptl q_i)$. Thus take $W_i (q_i;P_i) = P_i q_i = p_i q_i$ is constant.

== Poisson Bracket

$
  {f g, h} = f {g, h} + {f , h} g \
$
$
  D_[a,b](c) = D_a D_b (c) - D_b D_a (c) \
  {{f,g}, h} = {f, {g, h}} - {g, {f, h}} \
  {{f,g}, h} + {{g,h},f} + {{h,f},g} = 0 
$

Suppose angular momentum:

$
  {L_1,L_2} &= {r_2 p_3 - r_3 p_2, r_3 p_1 - r_1 p_3} \
  &= {r_2 p_3, r_3 p_1} + {r_3 p_2, r_1 p_3} \
  &= {r_2, r_3}p_3 p_1 + r_3{r_2, p_1}p_1 + ... \
  &+ r_1{r_3, p_3}p_2 + ... \
  &= -r_2 p_1 + r_1 p_2 = L_3
$
It's useful to check that:
$
  {L_i, L_j} &= {epsilon_(i l m) r_l p_m, epsilon_(j k n) r_k p_n} \
  &= r_k {r_l, p_n}p_m + r_l {p_m, r_k}p_n + ... \
  &= -epsilon_(i l m) epsilon_(j k n) r_k p_m delta_(l n) + epsilon_(i l m) epsilon_(j k n) r_l p_n delta_(m k) \
  &= - (delta_(i j) delta_(m k) - delta_(i k) delta_(j m)) r_k p_m + ... \
  &= - (r_m p_m  - r_i p_j) + (r_l p_l - r_j p_i) \
  &= r_i p_j - r_j p_i = epsilon_(i j k) L_k
$
Which is the pesudo-vector.

== Problem Sheet

- A bowl with a rod leaning on the edge, with one side out of bowl, the length inside is $c$, prove its whole length.

Take $O$ as the center of bowl with a down $y$ axis.
$
  m g delta y_c = 0 \
  y_c = (2 r cos theta - l / 2) cos theta \
  2 r cos theta = c \
$

$
  delta y_c = (-2 r sin^2 theta + (2r cos theta - l / 2) cos theta) delta theta = 0 \
  l = 2(-2r sin^2 theta + 2r cos^2 theta) / (cos theta) \
  l = 4 r (c^2 / 4r^2 - (1 - c^2 / 4r^2)) / (c / 2r) = 4(c^2-2r^2) / c
$

- Two same even and smooth ball tied on the fixed point $O$ with two rope, and hold on a same weight ball on two of them, seek relation of $alpha$ as middle down axis with rope and $beta$ as the center connection of the held ball and another ball with the down axis.

$
  m g sum_i^3 delta y_i = 0 \
  y_1 = y_2 = l cos alpha, y_3 = l cos alpha - 2r cos beta \
  2 r sin beta = l sin alpha \
  2 r cos beta delta beta = l cos alpha delta alpha \
$

$
  (-3 l sin alpha delta alpha + 2 r sin beta delta beta) = 0 \
  -3 delta alpha + delta beta = 0 \
$

$
  (-3 l sin alpha + l tan beta cos alpha) delta alpha = 0 \
  tan beta = 3 tan alpha
$

Notice $-3 delta alpha + delta beta = 0 != 3 alpha = beta$. Because there relation is $delta alpha = F(alpha,beta) delta beta$ rather a single variable relation. We can only say that $F(alpha,beta) = (l cos alpha)/(2 r cos beta) = 3$ in equilibrium rather a integral for arbitrary displacement.

It's more like implicit function, for example:
$
  x^2 + y^2 = R^2 \
  d y = - x/y d x \
$
$
  #text[if we know $d y = 3 d x$] \
  - x/y = 3 \
  - x = 3 y != y = 3 x != d y = 3 d x\
$

The usual problem about solving a system by langrange is mainly geometric, the mainly restriction is about fixed length and no-slip rotation:

$
  Delta x^2 + Delta y^2 = l \
  Delta x = l cos theta \ 
  Delta y = l sin theta
$

$
  R theta = v
$

Above should be also used with basic translation and rotation addition property throughout different frame:

$
  v = v_1 + v_2 + ... \
  omega = omega_1 + omega_2 + ...\
$

- Suppose a cleavage and a block on it, the ground and surface on the cleavage is smooth.

Many problems need you to decompose throughout various frame. Like above, we decompose to the fixed frame on cleavage and the comoving frame with block, which is parallel with the slope.

Suppose $r_1$ is cleavage position, $r_2$ is the block:
$
  r_1 = x_1 hat(x)_1 \
  r_2 = r_1 + x_2 hat(x)_2 \
$

$
  dot(r)_1 = dot(x_1) hat(x)_1 \
  dot(r)_2 = dot(x_1) hat(x)_1 + dot(x)_2 hat(x)_2 \
  hat(x)_1 dot hat(x)_2 = cos theta \
  hat(y)_1 dot hat(x)_2 = sin theta
$

$
  T_1 = 1/2 M dot(x)_1^2 \
  T_2 = 1/2 m (dot(x)_1^2 + 2 dot(x)_1 dot(x)_2 cos theta + dot(x)^2_2 ) \
  U = m g (r_2 dot y)= m g x_2 sin theta \
$

Now we turn to rotation:
- Suppose a circle rotated around a point in the circle, a mass point smoothly rotates on the circle.

Decomposition is first, the fixed point rotation frame, and then the circle center rotation frame.

$
  r = r_1 + r_2 = rho_1 hat(rho)_1 + rho_2 hat(rho)_2 \
  dot(r) = rho_1 dot(theta)_1 hat(theta)_1 + rho_2 (dot(theta)_1 + dot(theta)_2) hat(theta)_2 \
  rho_1 = rho_2 = R \
$

It should be noticed that, the $(d r_2)/(d t)$ is a composition of angular velocity, equal to $(omega_1 + omega_2) times hat(r)_2 = (dot(theta)_1 + dot(theta)_2) hat(k) times hat(r)_2 = (...) hat(theta)_2$. The angle of $theta_1$ and $theta_2$ is because $(d hat(r)_2)/(d t) = ((d hat(r)_2)/(d t))_(O_2) + dot(theta)_1 hat(k) times hat(r)_2 $. Thus, $cos theta_2$ is the angle difference of fixed rotation and comoving rotation frame.

$
  hat(theta)_2 dot hat(theta)_1 = (hat(k) times hat(r)_2) dot hat(theta)_1 = - (hat(k) times hat(theta)_1) dot hat(r)_2 = hat(r)_1 dot hat(r)_2 = cos theta_2\
  hat(theta)_1 dot hat(theta)_2 = cos theta_2 \
$

$
  T = 1/2 m R^2(dot(theta)_1^2 + (dot(theta)_1 + dot(theta)_2)^2 + 2 cos theta_2 dot(theta)_1 (dot(theta)_1 + dot(theta)_2))
$

There're also the angular velocity relation due to self-rotation and revolution, we often denote former as $I_("cm") omega_2^2$ and latter as $I_"re" omega_1^2$.

- Suppose a small smooth rolling placed on the top of a big smooth rolling, when the small rolling tends to fall, there are non-slip rotation between them.

Suppose small rolling with $theta$, $r$ and big rolling with $phi.alt$, $R$, based on the non-slip, the revolution speed and rotation speed is same.
$
  r phi.alt = (R + r) theta
$

The common confusion is to identify the arc length on the big rolling, which is wrong. Because the identification should be the small rolling mass center velocity, from non-slip rotation, it has $v = r dot(phi.alt)$, we also know revolution, which means it has $(R+r) dot(theta)$ is same. This is due to that the contacted point, the bottom of the rolling is actually with speed $0 = v_c - dot(phi.alt) r$ with the basic knowledge of no-slip rotation and within the fixed frame of big rolling, $v_c = (R+r) dot(theta)$, which yield the answer here.

We then identify rotation on each different coordinates, the principle to do this is to identify each rotation inertia with its corresponding angular velocity in its coordinates.

$
  L &= (r_"cm" + r_0) times m (v_"cm" + v_0) \
    &= r_"cm" times m v_"cm" + r_0 times m v_0 \
    &= L_("orbit") + L_("spin") 
$

Indeed, for inertia, the former is actualy:
$
  L_"orbit" = (m r^2_"cm") omega_"O" -> T_"orbit" = 1/2 (m r_"cm"^2) omega^2_O \
  L_"spin" = I_"cm" omega_O_"cm" -> T_"spin" = 1/2 I_"cm" omega^2_O_"cm"
$
Where the confusion is $I_"cm"$ is the mass inertia in center matter frame and $r_"cm"$ is the position of center mass.

$
  T = 1/2 (I_1 dot(theta)^2 + m (R+r)^2 dot(theta)^2 + I_(2 "cm") dot(phi.alt)^2)
$

Where the second term is $T_"orbit"$ which is rotation of whole in fixed rotation frame with angular velocity $theta$, and $T_"spin"$ is the comoving rotation frame with angular velocity $phi.alt$.

The another information about rolling is the disk or ball's other point related to center mass. Which as a additional angular velocity.

Rolling disk or a ball with fixed plane movement on the ground, would give its center:
$
  x_c, y_c = R
$

For any other point on the disk, would be:

$
  x = x_c + x, y = y_c + y \
  r = x_c hat(x) + y_c hat(y) + r_O' hat(r)_O' \
  dot(r) = dot(x)_c hat(x) + r_O' dot(theta) hat(theta)_O' \
  hat(theta)_O' dot hat(x) = cos theta
$

Where the final equation is based on the rotation of center as before. Note that this is one point on the rolling disk, but beside this addtional mass point, there are also the whole disk rotation inertia.

$
  T_"disk" = 1/2 M dot(x)_c^2 + 1/2 I_"cm" dot(theta)^2 \
  R dot(theta) = dot(x)_c
$

After this, if there's another rigid body embedded in the disk, we has also:
$
  T_"rigid" = 1/2 M' dot(x)^2 + 1/2 I'_"cm" dot(theta)^2
$

Suppose a stick with length $2 a sin alpha$ which $alpha$ is a constant. Then the length related to disk center is $rho = a cos alpha$.

$
  T_"rigid" = 1/2 m (dot(x)_c^2 + a^2 cos^2 alpha dot(theta)^2 + 2 dot(x)_c a cos alpha dot(theta)  cos theta) + 1/2 I'_"cm" dot(theta)^2 \
  I'_"cm" = 1/12 m 4 a^2 sin^2 alpha  = 1/3 m a^2 sin^2 alpha
$

$
  U = m g rho hat(rho) dot hat(y) = m g a cos alpha cos theta
$

Which can be apply to any rigid body embedded problem, even half disk is also too, decompose into rotation and translation to derive answer.

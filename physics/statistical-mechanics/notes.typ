#import "../lib.typ": *
#import "@preview/physica:0.9.8": *

#show: mine.with(
  title: "Statistical Mechanics",
)

#let vf(content) = $upright(bold(content))$

= Classical

$
  d U = d Q + d W \
$

$
  eta(Q_i, Q_f) = W/Q_i = (Q_i - Q_f)/Q_i = 1 - Q_f/Q_i
$

$
  W(T_i,Q_i;T_f,Q_f) -> W(T_i,Q_i;T_f,Q'_f)
$

$
  W(T_1,Q_1;T_2,Q_2) W(T_2,Q_2;T_3,Q_3) = W(T_1,Q_1;T_3,Q_3)
$

$
  W^(-1) (T_i,Q_i;T_f,Q_f) = W(T_f,Q_f;T_i,Q_i)
$

$
  W^(-1) (T_i,Q_i;T_f,Q_f) W(T_i,Q_i;T_f,Q'_f) = W(T_f, Q_f; T_f, Q'_f)
$

However, if $Q'_f < Q_f$, one create a machine that produces more work from a single source, thus it's impossible a machine could be more stronger than reversible one. Thus, it's better to say that $forall eta, eta <= eta^R$.

If the substance of system works in a certain environment temperature, which is independent of other condition due to heat $Q$ is. Thus measure heat transfer between them is indeed measure the temperature of them.

$
  Q_2/Q_1 = phi(T_1, T_2) -> Q_2/Q_1 = phi(T_3, T_2)/phi(T_3, T_1) -> Q_2/Q_1 = phi(T_2)/phi(T_1) -> Q_2/Q_1 = T_2/T_1
$

Due to arbitrary $T_3$ must be cancelled in function, which we reduce in more tense expression that $T_2\/T_1$ rather $phi(T_2)\/phi(T_1)$. The reverse machine is uniquely determined by $Q_i, T_i, T_f$, one could say $Q_2\/Q_1 = T_2\/T_1$, if not, $Q_2\/Q_1 > T_2\/T_1$. Make it a algebraic variables by denoting $Q > 0$ absorbing, $Q < 0$ exerting. $Q_2\/Q_1 > T_2 \/T_1 -> Q_2\/T_2 + Q_2\/T_1 <= 0$.

$
  integral.cont (d Q)/T <= 0
$

You may say that if $(d Q)/T = S$ for a exact differential. We can say that a reverse machine correspond to such $S$ which $d S >= (d Q)/T$ because a normal machine must with cycle or a part of integral, smaller than reversible one.

$
  & d U = pdv(U, S)_V d S + pdv(U, V)_S d V = T d S - P d V \
  & d H = pdv(H, S)_P d S + pdv(H, P)_S d P = T d S + V d P \
  & d F = pdv(F, T)_V d T + pdv(H, V)_T d V = - S d T - P d V \
  & d G = pdv(G, T)_P d T + pdv(G, P)_T d P = - S d T + V d P
$

A general characteristic function may be the Legendre transformation of arbitrary general work and position.

$
  f = L(U; X_1,...,X_n)
$

Given parameter in $(T,V)$:

$
  d U = T d S - P d V & = T (pdv(S, T)_V d T + pdv(S, V)_T d V) - P d V \
                      & = T pdv(S, T)_V d T + (T pdv(S, V)_T - P) d V \
                      & = T pdv(P, V)_T d T + (T pdv(P, T)_V - P) d V
$

Given parameter in $(T,P)$

$
  d H = T d S + V d P & = T (pdv(S, T)_V d T + pdv(S, P)_T d P) + V d P \
                      & = T pdv(S, T)_V d T + (T pdv(S, P)_T + V) d P \
                      & = T pdv(P, V)_T d T + (-T pdv(V, T)_P + V) d P
$

$
  & (d Q)_V = d (U - W)_V = (d U + P d V)_V = (d U)_V \
  & (d Q)_P = d (U - W)_P = (d U + P d V)_P = (d H)_P
$

$
  & C_V = pdv(Q, T)_V = pdv(U, T)_V = T pdv(S, T)_V \
  & C_P = pdv(Q, T)_P = pdv(H, T)_P = T pdv(S, T)_P \
$

$
  C_P - C_V & = pdv(U + P V, T)_P - pdv(U, T)_V
              quad (pdv(U, T)_P = pdv(U, T)_V + pdv(U, V)_T pdv(V, T)_P) \
            & = (P - pdv(U, V)_T) pdv(V, T)_P quad (pdv(U, V)_T = pdv(U, V)_S + pdv(U, S)_V pdv(S, V)_T) \
            & = - pdv(U, S)_V pdv(S, V)_T pdv(V, T)_P \
            & = T pdv(P, T)_V pdv(V, T)_P
$

Thus we recover everything in integral:

$
  & d U = C_V d T + (T pdv(P, T)_V - P) d V \
  & d S = C_V/T d T + pdv(P, T)_V d V \
$

$
  & d H = C_P d T + (-T pdv(V, T)_P + V) d P \
  & d S = C_P/T d T - pdv(V, T)_P d P
$

Use the expression in $T pdv(S, T)_((dot))$ would be easier.

Denote $C_P/C_V = gamma$, which is a measurement of per unit work compensated by temperature increasing in heat bath. As for ideal gas, it's same as $dv(P V, T) = n R$.

A example of $C_V > 0$ and $pdv(P, V)_T < 0$ to deduce $C_P > 0$ and $pdv(P, V)_S < 0$.
$
  C_P = T pdv(S, T)_P = T (pdv(S, T)_V + pdv(S, V)_T pdv(V, T)_P) = C_V + T pdv(P, T)_V pdv(V, T)_P = C_V - T pdv(P, V)_T pdv(T, V)^(-1)_P pdv(V, T)_P
$

Thus $C_P = C_V + "positive" -> C_P > 0$.

$
  pdv(P, V)_S & = pdv(P, V)_T + pdv(P, T)_V pdv(T, V)_S \
              & = pdv(P, V)_T - pdv(P, V)_T pdv(T, S)_V pdv(V, S)^(-1)_T \
              & = pdv(P, V)_T - T/(C_V) pdv(P, V)_T pdv(P, T)_V
$

We see that $pdv(P, V)_S = pdv(P, V)_T - "positive" -> pdv(P, V)_S < 0$.

$
  C_V (gamma - 1) = T pdv(P, T)_V pdv(V, T)_P = T (n R)/V (n R)/P = n R \
  C_V = (n R)/(gamma - 1), thick C_P = (gamma n R)/(gamma - 1)
$

$
  f(lambda x_1,...,lambda x_n) = lambda^n f(x_1,...,x_n)
$

$
  f(x_1,...,x_n) = sum_i^n x_i (partial f(x_1,...,x_n))/(partial x_i)
$

$
  U (lambda S,lambda V,lambda N) = lambda U(S,V,N) \
$

$
  U(S,V,N_i) = T S - P V + sum_i^l mu_i N_i
$

It can be generalized to arbitrary variables.

$
      H & = T S + sum_i^l mu_i N_i \
      F & = - P V + sum_i^l mu_i N_i \
      G & = sum_i^l mu_i N_i \
  Omega & = F - sum_i^l mu_i N_i = - P V \
      J & = 0 \
$

Thus:

$
  S d T - V d P + sum_i^l N_i d mu_i = 0
$

Sometimes we will rely on the extensible property of a certain variable to divide every other extension variables to acquire the intension property.

For example:

$
  d mu = - S_m d T + V_m d P
$

We know that $S (V,T) = integral C_V/T d T + pdv(P, T)_V d V$, therefore, fixed the $V$ variable, we integrate $T$ variable:

$
  & integral_(T_0)^T integral_(T_0)^(T') (C_(P,m) (T'',P_0))/T'' d T'' d T' quad (T_0 <= T'' <= T' <= T -> T' in [T'',T]) \
  & = integral_(T_0)^T (integral_(T_'')^T d T') (...) d T'' \
  & = integral_(T_0)^T (T - T'') (...) d T''
$

Which is what we need, if you want, a arbitrary constant could be added because we can never measure a *absolute* potential indeed. For ideal gas, you may expect:

$
   d mu & = -(integral_(T_0)^T C_(P,m)/T'' d T'') d T + (R T)/P d P \
  -> mu & = R T (phi + ln P) quad (R T phi = -integral S_m d T)
$

If we emphasize for multiple components, the special case in ideal gas and independence between components will induce that:

$
  P_i prop N_i -> P_i = x_i P = N_i/N P
$

$
  mu_i = R T (phi_i + ln x_i P)
$

Denote different phase for single component as $(dot)^(alpha\/beta\/gamma...)$, we can divide two phase as two system in contact, therefore share the same intensive attributes:

$
  d S^alpha = d U^alpha 1/T^alpha + d V^alpha P^alpha/T^alpha - d n^alpha mu^alpha/T^alpha
$

$
  d S = d S^alpha + d S^beta = 0 \
$

However, the whole system is closed thus $d (dot)^alpha + d (dot)^beta = 0$ for each correlated attributes. We conclude that they share the same temperature, pressure and chemical potential in reversible phase transition:

$
  T^alpha = T^beta = T, P^alpha = P^beta = P, mu^alpha = mu^beta = mu
$

// $
//   d G = d (G^alpha + G^beta) &= - S d T + V d P + mu (d n^alpha + d n^beta) \
//   &= - S d T + V d P
// $

// It should be clear that the total Gibbs energy won't be zero variation due to the if we follow the curve of phase transition, rather in the fixed temperature and pressure of two phase in contact.

Suppose the extensive Gibbs-Duhem theorem:

$
                      d mu^alpha & = d mu^beta \
  -S^alpha_m d T + V^alpha_m d P & = -S^beta_m d T + V^beta_m d P \
                     (d P)/(d T) & = (S_m^alpha - S_m^beta)/(V^alpha_m - V^beta_m) = L/(T Delta V_m)
$

Which is called Clausius-Clapeyron relation. It's also can be seen that, the total entropy will move along the curve of phase transition:

$
              d S & = lr((partial S)/(partial V_m)|)_T d V_m + lr((partial S)/(partial T)|)_(V_m) d T \
              d S & = lr((partial S)/(partial V_m)|)_T d V_m quad "Fixed temperature" \
              d S & = lr((partial P)/(partial T)|)_(V_m) d V_m quad "Maxwell relation" \
  L/(T Delta V_m) & = (d P)/(d T) quad Delta V = d V_m = V^beta_m - V^alpha_m \
$

In the case where two parameter move in phase transition curve $(P,T)$.

$
  dv(L(P,T), T) = dv(, T) (S^beta - S^alpha)T &= 1/T dv(, T)(S^beta - S^alpha) + (S^beta - S^alpha)\
  &= T (pdv(S^beta, T)_P + pdv(S^beta, P)_T dv(P, T) + (beta <-> alpha)) + L/T \
  &= C^beta_P - C^alpha_P + (pdv(V^beta, T)_P - pdv(V^alpha, T)_P) L/(Delta V)
$

$
  d G & = V d P - S d T \
      & = V d P = 0 \
$

$
  integral_i^f V d P = (P V)|^f_i - integral_i^f P d V = 0
$

$
                  d S = d (S_1 + S_2 + S_A) & = 0 \
  (4 pi r^2 (p_1 - p_2) + 8 pi r sigma) d r & = 0 \
                    p_1 - p_2 + (2 sigma)/r & = 0 \
                          p_1 + (2 sigma)/r & = p_2 -> Delta p = (2 sigma)/r
$

$
        mu_g (p_r, T) & = mu_l (p_("in"),T) \
  mu_g (p_infinity,T) & = mu_l (p_infinity,T) \
           Delta mu_g & = Delta mu_l
$

$
  mu_g (p_r, T) = integral_(p_infinity)^(p_r) V_(m,g) d p + mu_g (p_infinity,T) = integral_(p_infinity)^(p_r) (R T)/p d p + ... = R T ln (p_r/p_infinity) + mu_g (p_infinity,T) \
$

$
  Delta p = p_r - p_infinity approx p_("in") - p_(infinity)
$

$
  mu_l (p_("in"), T) = integral_(p_infinity)^(p_"in") V_(m,l) d p approx V_(m,l) Delta p
$

$
  R T ln (p_r/p_infinity) & = (2 sigma)/r V_(m,l) \
           p_r/p_infinity & = exp((2 sigma V_(m,l))/(R T r))
$

$((partial mu)/(partial p))_T = V_m > 0$, thus increase pressure will increase chemical potential, while in phase transition equilibrium needs to maintain the equality, $mu_l > mu_g$, thus $mu_l -> mu_g$ (or _saturated vapor pressure_) indicates the vaporize itself, so maintains the mechanical equilibrium will break the chemical potential equilibrium. If the temperature keeps cool down while the condensation nucleus is few thus the expected phase transition doesn't happen, we expect $mu_g arrow.b$ or $p > p_"vapor" = p_infinity$, which is the expect inequality, plus, if it's also smaller than the $p_r$, we still can't maintain mechanical equilibrium thus droplet nucleus tends to vaporize. Until the point where the enough huge liquid bubble emergent to meet such mechanical equilibrium, therefore growing and whole gas is liquefied. In real life, due to dust or polarized molecules, the $r_c$ is great enough and $p_r$ is smaller enough nearly equal to $p_infinity$, when we reach the liquefaction point, the gas is immediately liquefied.

For Vanderwaals gas, the deflection in lower volume is the key of phase transition. But such deflection only exist in lower temperature too, denoted as $T_c$ the critical temperature. So, for $T < T_c$, we can describe the phase transition of the gas, the problem is how can deflection expressing the coexistence of liquid and gas?

$
  T_l = T_g \
  P_l = P_g \
  mu_l (T,P) = mu_g (T,P)
$

Thus the specified $P$ must be special that satisfying certain condition that the phase transition occurs.

$
  d mu = - S_m d T + V_m d P = V_m d P quad "fixed temperature" \
  d (mu_l - mu_g) = integral.cont_(V_g -> V_l) V_m d P = 0
$

The deflection of $P-V$ graph shows that for a given temperature, we can integrate along the curve while the difference must be *zero* where the start and end point have the same pressure. We transform the variable to solve reversely:

$
  integral_(V_g)^(V_l) V_m (P) d P &= lr(P V_m)|_(V_g)^(V_l) - integral_(V_g)^(V_l) P(V_m) d V_m quad (P(V_g) = P(V_l) = P_"eq")\
  &= integral_(V_g)^(V_l) (P(V_m) - P_"eq") d V_m = 0
$

Where we can deduce $P_"eq"$ by integration following the graph.

For ideal gas/liquid, one have:

$
  d mu_i (T,P) = - S_m d T + V_m d P -> mu_i (T,P) = g_i (T,P) + R T ln P_i quad (P_i = x_i P)
$

We absorb the scalar into $g_i$ as:

$
  mu_i = g_i (T,P) + R T ln x_i
$

Thus we see that if $x_i = 1$, single component will have $mu = g_i (T,P)$. One therefore reduce that the difference of $G(T,P) = n_i mu_i$:

$
  & Delta G = sum_i^n R T n_i ln x_i \
  & Delta V = sum_i pdv(Delta G, P)_(n_i,T, P) = 0 \
  & Delta S = - sum_i pdv(Delta G, T)_(n_i,P) = -sum_i^n R n_i ln x_i \
  & Delta H = Delta G + T Delta S = 0 \
  & Delta U = Delta H - P Delta V = 0
$

We see that due to thermo equilibrium and pressure equilibrium, only Gibbs energy changes. Suppose the solvent can be evaporated solely, thus in chemical potential equilibrium.

$
  g' = g + R T ln (1-x)
$

Where $x$ is the partition ratio of solute, $g'$ is the chemical potential of solvent in gas. Differentiate that:
$
            pdv(g', P)_T d P + pdv(g', T)_P d T & = pdv(g, P)_T d P + pdv(g, T)_P d T - (R T)/(1-x) d x + R ln(1-x) d T \
                              V_g d P - S_g d T & = V_l d P - S_l d T - (R T)/(1-x) d x + R ln (1-x) d T \
  (V_g - V_l) d P - (S_g - S_l + R ln(1-x)) d T & = -(R T)/(1-x) d x \
$

$
  S_g - S_l + R ln (1-x) = ((g' + T S_g) - (g + T S_l))/T = (H_g - H_l)/T
$

Suppose $d T = 0$ or fixed temperature:

$
  pdv(P, x)_(T) & = (R T)/(V_g - V_l) 1/(1-x) \
                & = P/(1-x) quad (V_g >> V_l "with ideal gas model") \
                & -> p_x = p_0 (1-x) quad (x = 0 -> p_x = p_0)
$

Suppose $d P = 0$ or fixed pressure:

$
  (H_g - H_l)/T d T & = (R T)/(1-x) d x \
        pdv(T, x)_P & = (R T^2)/(L(1-x)) quad (H_g - H_l = L) \
$

If $x << 1$, or dilute solution:

$
  Delta T = (R T^2)/L x
$

However, we could achieve this by semi-permable membrane. Like sugar solution while only water can cross the membrane, we can create a pressure difference while maintaining the chemical potential equilibrium. Thus $p_x - p_0$ is the difference between sugar solution and pure water.

$
  g' = g(T,P) = g(T,P_0) + R T ln(1-x) \
  V_(l,m) (p-p_0) = R T ln (1-x) approx -R T x \
  p - p_0 = (R T)/V_(l,m) x = (R T)/V_(l,m) n_2/(n_1 + n_2) approx (R T)/V_(l,m) n_2/n_1 = (n_2 R T)/V_l
$

Notice, previous is in same pressure which can be identified as saturated vapor pressure; while this is in different pressure proportional to the amount of sugar substance.










= Priori

== Probability

Probability is a fundamental information lost measure. Suppose we know the dynamics of a process, and its initial condition, we can deduce the deterministic results.

So, probability must be a measure upon some potential state set to reflect the state in *frequency* or *understanding* to such system. We say $P: Omega -> cal(B)$ with element measure as $P(d mu)$ for $d mu in Omega$, or discrete $P(omega)$ for $omega in Omega$. Thus, we can take the summon on such element due to disjointness that $P(union_i omega_i) = P(A)$ where $omega_i in A$.

$
  P(A inter B|Omega) = P(B|Omega) dot P(A|B)
$

$
  P( A inter B )/(P(B)) = P(A|B)
$

Indicates that the conditional probability $A|B$ of a given presumed condition $B$. Suppose one has $P(A inter B = emptyset) = 0$, one has $P(A|B) = 0$. If $A subset.eq B -> A inter B = A$, we has a simpler expression $P(A)\/P(B)$, which is akin to a subset from whole. Another special case is $P(A|B) = P(A)$ where the condition is indifferent to $A$, where one has $P(A inter B) = P(A)P(B)$.

$
  P(A inter B) = P(A|B) dot P(B) = P(B|A) dot P(A) \
$

Then given that $Omega = union_i A_i$ for disjoint partition, we has:

$
  P(A inter Omega = A) = P(A|Omega) dot P(Omega) = sum_i P(A|B_i) P(B_i)
$

Given a projection or random variable $X: Omega -> cal(B)$ where $cal(B)$ is measurable set, which, you may want it's also a metric and separable space, however, the crucial thing is one commonly investigate the state set by such function, suppose we have $t -> f(t)$ in classical mechanics, we inspect that $f(t + T) = f(t)$, then we retroactively conclude that in such system, time is in period. The same thing happens upon the state space. We redistribute the state space through a coarse measure of it to acquire a dynamics quality. Such thing can be restated in statistical mechanics that we have many micro states of particles and a projection or macro state to *reflect* the system.

$
  integral_Omega P(d mu) = 1_(cal(B))
$

Sometimes given a already measurable state space, we will notate also:

$
  P(d mu) & equiv p(mu) d mu equiv d P(mu) \
$
$
  integral_Omega P(d mu) equiv integral_Omega p(mu) thin d mu \
$

Thus we can extend probability from state set to random variable as indicators:

$
  P(X in cal(B)) = integral_{mu in Omega | X(mu) in cal(B)} P(d mu) \
  bb(E)(X) = expval(X) = integral_Omega X(mu) P(d mu)
$

Thus if one has no additional investigation upon such state space, each state is indifferent and thus, *equal* in respective view of evaluation. Such *priori* probability is called uniform distribution, which is the basic results comes from indifference of elements of a set. How? A uneven distribution would reflect the underneath state dynamics by given intersections or *section* in local view. Then for even case, each $P(inter^(infinity)_i A_i) -> P(omega)$ must be equal for any set convergence, resulting the same local view.

$
  P({union.big_I omega_i}) = sum_I P({omega_i}) = integral_Omega P(d omega) = 1_(cal(B)) \
$

$
  P({omega}) = 1/abs(Omega) #[or] P({omega}) = delta_mu ({omega}) = 1_{omega = mu}
$

That's the uniform distribution where every element is measured in constant.

A strong suggestion of such *priori* equal probability is information, which is the most unknown condition for observer. If you read few axioms about information and entropy origin, you will find that it's a delicate suitable restriction to deduce the results form. For example, strong additivity:

$
  & H(X,Y)_P = H(X)_P + H(Y|X)_P \
  & H(X,Y)_P = H(X)_P + H(Y)_P quad "if" X,Y "independent" -> H(Y|X) = H(Y)
$

For a given probability distribution. Given above maximal condition upon uniform distribution, we has below:

$
  H(X)_P = - integral_X p(mu) log p(mu) thin d mu = - integral_X (log dv(P, mu)) P(d mu) \
$

Suppose $I = P(d mu)$ is a uniform distribution, one has:

$
  H(X)_I = sum_i 1/abs(Omega) log abs(Omega) = 1/abs(Omega) log abs(Omega) dot abs(Omega) = log abs(Omega) \
$

Often, one call $-log p(mu) = - log (dv(P, mu))$ the information $I(X)_P$. It is suitable for any restriction based on human imaginary, for example, you should acquire more information if the probability is low because you need to update your knowledge based on Bayesian!

$
  H(X, Y)_P & = - integral_(X,Y) d mu p(x,y) log p(x,y) \
            & = - integral_(X,Y) d mu p(x,y) log p(x) p(y|x) \
            & = - integral_(X) d mu p(x) log p(x) - integral_(X,Y) p(x,y) log p(y|x)
$

$
  H(Y|X) & = integral_X d mu p(x) H(Y|X = x) \
         & = - integral_(X,Y) d mu p(x) p(y|x) log p(y|x) \
$

Where $H(X) = bb(E)(I(X))$, thus fix a element $x$, one has $H(Y|X=x) = bb(E)(I(Y|X=x))$. Then we integrate or sum on the state subset $X$.

Denote $p: bb(N) -> bb(R)$ that evaluate the probability on $bb(N)$ with each $p(i) = p_i$ for $i in bb(N)$, so does for $X_i^a$.

$
  S(p_i; lambda_a) = - sum_i p_i log p_i + sum_a lambda_a (sum_i X^a_i p_i - X^a) \
$

With $lambda_a$ the Lagrange multiplier, $sum_i X^a_i = X^a$ the summation constraint. We has such extreme point:

$
  & (partial S)/(partial p_i) = - log p_i - 1 + sum_a lambda_a X^a_i = 0 \
  & (partial S)/(partial lambda_a) = sum_i X^a_i p_i - X^a = 0 \
$

With distribution:

$
  p_i = exp(sum_a lambda_a X^a_i - 1) = 1/Z exp(sum_a lambda_a X^a_i)
$

One can extend by the generalized Lebesgue integral to a variation calculus on distribution. We have observables by abusing notation:

$
  X^a = integral_Omega X^a (mu) thin p(mu) thin d mu
$

Suppose $X^0 (mu) equiv X^0 equiv 1$, the constraint of normalization of probability measure.

$
  S[p;lambda_a] = - integral p log p thin d mu + sum_a lambda_a (integral X^a p thin d mu - X^a)
$

$
  & 0 = pdv(S [p;lambda_a], p, d: delta) = integral (- log p - 1 + sum_a lambda_a X^a) d mu \
  & 0 = pdv(S [p;lambda_a], lambda_a, d: delta) = integral X^a p thin d mu - X^a
$

Therefore, for a usual observation of observables in $bb(R)$:

$
  integral p(x) thin d x = 1, quad integral x thin p(x) thin d x = expval(x), quad integral x^2 thin p(x) thin d x = expval(x^2) \
$

$
  P(x) & = C e^(lambda_1 x + lambda_2 x^2) \
  & = C exp(lambda_1^2/(4 lambda_2)) exp(-lambda_2 (x + lambda_1/(2 lambda_2))^2) quad C exp(lambda_1^2/(4 lambda_1)) = A\
$

Contrive deducing coefficients $lambda_1$ and $lambda_2$ by the constraints:

$
  x => x + lambda_1/(2 lambda_2) = y \
$
$
  integral^infinity_(-infinity) P(x) d x = A sqrt(pi/lambda_2) = 1 \
$
$
  A integral^infinity_(-infinity) (y - lambda_1/(2lambda_2)) e^(-lambda_2 y^2) d y = - A lambda_1/(2 lambda_2) sqrt(pi/lambda_2) = expval(x) \
$

$
  A integral^infinity_(-infinity) (y - lambda_1/(2 lambda_2))^2 e^(-lambda_2 y^2) d y = 1/(2lambda_2) + lambda_1^2/(4 lambda_2^2) = expval(x^2) \
$

$
  lambda_1/lambda_2 = - 2 expval(x) = -2 mu\
  1/(2 lambda_2) = expval(x^2) - expval(x)^2 = sigma\
$

$
  P(x) = A exp((x-mu)^2/(2 sigma^2)) \
$

Is the final answer, which is a Gaussian distribution with mean $mu$ and variance $sigma^2$.

The maximal entropy is the consequence of uniform distribution can be deduced by Lagrange multiplier with sole constraint $sum_i p_i = 1$.
$
  S_n = 1/n sum_i^N X_i >= x
$

For a non-negative random variable s.t. $X: Omega -> bb(R)^+$:
$
  bb(E)(X) = integral_Omega X P(d mu) >= integral_({mu in Omega|X(mu) >= a}) X P(d mu) >= a integral_({mu in Omega|X(mu) >= a}) P(d mu) = a P(X>=a)
$

$
  bb(E)(X) >= a P(X>=a)
$

$
  P(1/n sum_i^N X_i >= x) & = P(exp(lambda sum_i^n X_i) >= exp(lambda n x)) \
                          & <= exp(-lambda n x) bb(E)(exp(lambda sum_i^N X_i)) \
                          & = exp(-n (lambda x - Lambda(lambda) )) quad Lambda = ln bb(E)(exp(lambda sum_i^N X_i))
$

$
  I(x) = lambda x - Lambda(lambda)
$

Consider a random variable $S_n (bold(omega))$ where $bold(omega) = (omega_1,dots,omega_n)$ for n-random variables. Denoting $p(omega)$ the probability density of $omega$.

$
  p(S_n = s) = integral_{omega in Omega|S_n (omega) = s} p(omega) thin d omega = integral_Omega delta(S_n (omega)-s) p(omega) thin d omega = expval(delta(S_n (omega)-s))
$

$
  delta(s) &= 1/(2 pi) integral e^(i zeta s) d zeta = 1/(2pi i) integral_(- i infinity + a)^(i infinity + a) e^(zeta s) d zeta
$

$
  p(S_n = s) = 1/(2pi i) integral_(- i infinity + a)^(i infinity + a) d zeta integral_Omega d omega thin p(omega) e^(zeta (S_n (omega) - s)) = 1/(2pi i) integral_(- i infinity + a)^(i infinity + a) d zeta thin e^(- zeta s) integral_Omega d omega thin thin p(omega) thin e^(zeta S_n (omega))
$

$
  zeta -> n zeta \
  Lambda(zeta) = lim_(n->infinity) 1/n ln expval(e^(n zeta S_n))
$

Choosing a contour so that it goes through the saddle point $zeta^*$ of $zeta s - Lambda(zeta)$, therefore we consider the most significant contribution from the saddle point as exponential contribution.

$
  p(S_n = s) asymp integral^(zeta^* + i infinity)_(zeta^* - i infinity) d zeta thin e^(- n (zeta s - Lambda(zeta))) asymp e^(-n (zeta^* s - Lambda(zeta^*)))
$

A large-$n$ limit will filter all other contribution and leave the supremum in place.

$
  lim_(n->infinity) - 1/n ln p (S_n = s) = sup_(k in bb(R)) {k s - Lambda(k)} ~ zeta^* s - Lambda (zeta^*)
$

A hindsight proof is to construct a Radon-Nikodym derivative or simply, variable transformation.

$
  & P_zeta (d omega) asymp e^(n (zeta S_n (omega) - Lambda(zeta))) P (d omega) \
  & (P_zeta (d omega))/(P (d omega)) asymp e^(n (zeta S_n (omega) - Lambda(zeta)))
$

$
  P (S_n in d s) = integral_({omega in Omega|S_n (omega) in d s)) P (d omega) &= integral_({omega in Omega|S_n (omega) in d s}) P(d omega)/(P_zeta (d omega)) P_zeta (d omega) \
  &asymp integral_({omega in Omega|S_n (omega) in d s}) e^(-n (zeta S_n (omega) - Lambda (zeta))) P_zeta (d omega) \
$

As for $S_n in d s <=> S_n subset.eq B(s,delta)$.

To find the concentration point, or saddle point, it can be evaluated by differentiation if could:

$
  dv(, zeta) (zeta s - Lambda (zeta)) = s - Lambda'(zeta) = s - lim_(n->infinity) expval(S_n e^(n zeta S_n))/expval(e^(n zeta S_n))
$

Actually $s_(zeta^*) = Lambda'(zeta^*)$ is the concentration point such that the expectation of $S_n$ in $P_zeta$ probability measure:

$
  lim_(n->infinity) expval(S_n)_zeta &= lim_(n -> infinity) integral_(Omega) S_n (omega) P_zeta (d omega) \
  &= lim_(n -> infinity) 1/(expval(e^(n zeta S_n))) integral_Omega S_n (omega) e^(n zeta S_n (omega)) P(d omega) \
  &= lim_(n -> infinity) expval(S_n e^(n zeta S_n))/expval(e^(n zeta S_n)) \
  &= Lambda'(zeta) \
$

One can say that if:

$
  s = s_(zeta^*) => lim_(n -> infinity) integral_(Omega) S_n (omega) P_zeta (d omega) = lim_(n -> infinity) integral_({omega in Omega|S_(omega) in d s_(zeta^*)}) S_n (omega) P_zeta (d omega) = Lambda'(zeta)\
$
$ lim_(n->infinity) P_zeta (S_n (omega) subset.eq B(s_(zeta^*), delta)) = 1 $.

$
  P (S_n in d s) asymp e^(-n(zeta s - Lambda (zeta)))integral_({omega in Omega|S_n (omega) in d s}) P_zeta (d omega)
$

If we choose the concentration point $s_(zeta^*) = s = Lambda'(zeta)$, it implies:

$
  P (S_n in d s) asymp e^(-n (zeta s - Lambda(zeta)))
$

Thus such rate function $I(s) = zeta s - Lambda(zeta)$ should exist at least in a boundary condition. Even though the actual function may not exist. Then such minimum if exist, must be $I(s) = sup{zeta s - Lambda(zeta)}$ with a specified lambda, if we are lucky, it should be the convergence too. It suggests that one can directly formulate the definition as:

$
  lim_(n -> infinity) 1/n ln P(S_n in d s) asymp I (s)
$

Generally, one could apply to for various function $f(s)$, which is the general Laplacian transformation on function $f(s)$ as $Lambda(f)$.

$
  Lambda(f) = lim_(n->infinity) 1/(a_n) bb(E)(e^(a_n f(S_n))) = sup_s (f(s) - I(s))
$

The application of the _Gärtner-Ellis_ Theorem to a sample mean:

$
  S_n = 1/n sum_(i=1)^n X_i
$

of independent and identically distributed random variables yields a classical results of probability theory known as _Cramér's theorem_.

$
  Lambda(k) = lim_(n->infinity) 1/n ln expval(e^(k sum_(i=1)^n X_i)) = lim_(n->infinity) 1/n ln product_(i=1)^n expval(e^(k X_i)) = lim_(n->infinity) ln expval(e^(k X))
$

where $X$ is any of the summands $X_i$.

We can apply it to $n$-Gaussian *IID* random variables.

$
  expval(e^(k X)) & = integral_(-infinity)^(infinity) e^(k x) dot 1/(sqrt(2pi sigma^2)) e^(- (x-mu)^2/(2 sigma^2)) d x \
$

$
  -1/(2 sigma^2) (x^2 - 2(mu + k sigma^2) x + mu^2) = -1/(2 sigma^2) [(x - (mu + k sigma^2))^2 - (mu + k sigma^2) + mu^2] \
  -1/(2 sigma^2) ((mu + k sigma^2)^2 - mu^2) = k mu + 1/2 k^2 sigma^2
$

$
  Lambda (k) = ln expval(e^(k X)) = mu k + 1/2 sigma^2 k^2
$

Which the supremum is the unique maximum point satisfying $Lambda'(k) = s$.

$
  Lambda'(k) = mu + sigma^2 k = s => k = (s - mu)/sigma^2
$

$
  I(s) = sup_k (k s - Lambda(k)) = sup_k (k (s - mu) - 1/2 sigma^2 k^2) = (s-mu)^2/(2 sigma^2)\
$

$
  P(S_n in d s) = P(1/n sum_(i=1)^n X_i in d s) asymp e^(- I (s))
$

A other example is the investigation of exponential distribution $p(X = x) = 1/mu e^(- x/mu) thick x > 0, mu > 0$.

$
  expval(e^(k X)) = integral_(0)^(infinity) e^(k x) dot 1/mu e^(- x/mu) thin d x = 1/(1 - mu k) quad k < 1/mu
$

$
  Lambda (k) = ln expval(e^(k X)) = - ln (1-mu k)
$

$
  Lambda'(k) =mu/(1-mu k) = s => k = 1/mu - 1/s
$

$
  I(s) = sup_k {k s - Lambda (k)} = s/mu - 1 - ln s/mu quad s > 0
$

$
  P(S_n in d s) = P(1/n sum_(i=1)^n X_i in d s) asymp e^(- I(s)) = s/mu e^(1-s/mu)
$

== Properties of Large Deviation

We know that $Lambda (k)$ is the generating function of random variables.

$
  Lambda'(0) = lim_(n -> infinity) lr((expval(S_n e^(n k S_n)))/(expval(e^(n k S_n))) bar)_(k=0) = lim_(n->infinity) expval(S_n)
$

$
  Lambda''(0) = lim_(n->infinity) n lr((expval(S_n^2 e^(n k S_n)) - expval(S_n e^(n k S_n))^2)/expval(e^(n k S_n))^2|)_(k=0) = lim_(n -> infinity) n (expval(S_n^2) - expval(S_n)^2) = lim_(n -> infinity) n "Var"(S_n)
$

Which reduce to $Lambda''(0) = "Var"(X)$ for IID sample means.

To investigate in functional space, we need to construct a norm. Generally, a norm must satisfy triangle inequality or convex condition. To achieve this, apply to $ln(dot)$ which is convex. We also know that one can consider a function by it's double dual. Therefore we should build a connection between inner product and norm.

$
  log (lambda a + (1-lambda) b) >= lambda log a + (1-lambda) log b
$

Therefore, one can replace by:

$
  lambda => p, 1 - lambda => q, a => x^(1/p), b => y^(1/q) \
  log (p x^(1/p) + q y^(1/q)) >= p log x^(1/p) + q log y^(1/q) = log x y
$

Exponentiate both to get:

$
  p x^(1/p) + q y^(1/q) & >= x y \
      1/p x^p + 1/q y^q & >= x y (p => 1/p, q => 1/q)
$

Choose $norm(f)_p = norm(g)_q = 1$, yields _Holder inequality_:

$
  integral d mu thin abs(f dot g) <= norm(f)^p/p + norm(g)^q/q = 1 = norm(f)_p norm(g)_q quad (1/p + 1/q = 1)
$

And take the inequality in probability measure space:

$
      expval(X Y) & <= expval(X^p)^(1/p) expval(Y^q)^(1/q) \
  log expval(X Y) & <= 1/p log expval(X^p) + 1/q log expval(Y^q)
$

Therefore choose $X = e^(n alpha k_1 S_n)$ and $Y = e^(n (1-alpha) k_2 S_n)$ where $alpha in [0,1]$.

$
  log expval(e^(n (alpha k_1 + (1-alpha) k_2)S_n)) <= alpha log expval(e^(n k_1 S_n)) + (1-alpha) log expval(e^(n k_2 S_n)) \
  Lambda (alpha k_1 + (1-alpha) k_2) <= alpha Lambda (k_1) + (1-alpha) Lambda (k_2)
$

Which proves the convexity of $Lambda$.

Due to Legendre duality of rate function and generating function, one has:

$
  Lambda (k) = lim_(n->infinity) 1/n expval(e^(n k S_n)) = sup_s {k s - I(s)}
$

Replacing the product of $k S_n$ by a arbitrary continuous function $f$ of $S_n$, a general results is:

$
  Lambda (f) = lim_(n->infinity) 1/n expval(e^(n f(S_n))) = sup_s {f(s) - I(s)}
$

Better, $Lambda (0) = sup_s {-I(s)} = -inf_s {I(s)} = lim_(n->infinity) 1/n expval(1) = 0$, deducing that $I(s) > 0$, the positivity of rate function.

The duality can be expressed by below table that the unique point of $Lambda'(k) = s$ if it's differentiable:

$
  I'(s) = k quad Lambda'(k) = s \
  I''(s) = (d k)/(d s) quad Lambda''(k) = (d s)/(d k) \
  I''(s) = 1/(Lambda''(k)) > 0 quad Lambda''(k) = 1/(I''(s)) > 0
$

Since $Lambda (k)$ is convex with no linear parts $Lambda''(k) = n "Var"(S_n) > 0$. So rate function must be convex too. In the case of IID sample means, in particular, $I''(s = mu) = 1/(Lambda''(0)) = 1/(sigma^2)$.

However, above properties won't exist if we have no analyticity of function. Suppose a mix of discrete and continuous variables by Binomial and normalized Gaussian variable which has $mu = 0, sigma = 1$:

$
  & P(Y=-1) = P(Y=1) = 1/2 \
  & S_n = 1/n sum_(i=1)^n X_i + Y \
  & P(S_n in d s|Y= plus.minus 1) asymp e^(-n I_(plus.minus)(s)) \
  & I_(plus.minus) = (s plus.minus 1)^2/2 \
$

By condition probability $P(X) = sum_i P(X|Y_i)$:

$
  P(S_n in d s) asymp (1/2 e^(-n I_plus (s)) + 1/2 e^(-n I_minus (s))) \
$
$
  I(s) = min(I_(minus)(s), I_(plus) (s)) = cases(
    I_(minus) (s) quad s > 0,
    I_(plus) (s) quad s < 0
  )
$

Which is a symmetric function has minimums $-1,1$, breaking the general convexity due to non-differentiable in zero point.

If $I(s)$ has a unique global minimum that $I'(s^*) = k = 0$, then: $s^* = Lambda'(0) = lim_(n->infinity) expval(S_n)$.

$
  I (s^*) = k (s^*) s^* - Lambda (k(s^*)) = 0 dot s^* - 0 = 0
$

The global minimum indicates a unique concentration on typical value $s^*$ is the expression of _Law of Large Numbers_.

It implies that one can expand it in quadratic terms: $I(s) approx 1/2 I''(s^*)(s - s^*)^2$:

$
  P(S_n in d s) approx e^(- n/2 I''(s^*)(s-s^*)^2) quad (I''(s^*) = 1/(Lambda''(0)) = 1/sigma^2)
$

Called _Central Limit Theorem_. Suggests a Gaussian approximation in which around $s^*$ of the order $O(n^(1/2))$. So Large deviation theory is a generalization of Central Limit Theorem which has no quadratic Tylor expansion around its minimum.

Now we apply the routine to Binary sample:

$
  P(X_i = -1) = P(X_i = 1) = 1/2 \
  Lambda(k) = ln expval(e^(k X_i)) = ln 1/2(e^k + e^(-k)) = ln cosh k\
$

$
  s = Lambda'(k) = dv(ln cosh k, k) = tanh k \
  s = (e^k - e^(-k))/(e^k + e^(-k)) => k = 1/2 ln((1+s)/(1-s))\
$
$
  1 - tanh^2 k = 1/(cosh^2 k) => cosh k = 1/(sqrt(1- tanh^2 k)) \
$
$
  I(s) & = sup_k {k s - Lambda(k)} \
       & = s 1/2 ln((1+s)/(1-s)) - ln (1/(sqrt(1- s^2))) \
       & = 1/2((1+s)ln(1+s) + (1-s)ln(1-s)) quad s in [-1,1]
$

The minimum and zero of $I(s)$ is $s = 0$.

Large deviation can be formulated for random vectors too. A single random variable is extended to a vector valued form: $L_n (bold(X)), bold(X) = (X_1,dots,X_n)$, then one say the probability of the random vector is same as the observation value expressed as $P(L_n = l)$ for $L_n (bold(X)) = (L_(n,1) (X_1),dots,L_(n,m) (X_m))$. A usual empirical vector $L_n (bold(X))$ is the empirical frequencies:

$
  L_(n) [bold(X)](j) = 1/n sum_(i=1)^n delta(X_i, j)
$

It's actually said that $L_(n,j)$ is the counting of empirical samples that $X = j$.

$
  sum_(j in Omega) L_(n) [bold(X)](j) = sum_(j in Omega) 1/n sum_(i=1)^n delta(X_i, j) = 1/n sum_(i=1)^n sum_(j in Omega) delta(X_i, j) = 1/n sum_(i=1)^n 1 = 1
$

It seems easy to generalize the discrete samples into a continuous samples by replacing the space. The continuous extension of the empirical vector is the _empirical density_.

$
  L_(n) [bold(X)](x) = 1/n sum_(i=1)^n delta(X_i, x)
$

$
  integral_Omega L_(n) [bold(X)](x) d x = 1/n sum_(i=1)^n integral_Omega delta(X_i, x) d x = 1/n sum_(i=1)^n 1 = 1
$

Or better by measure:

$
  L_n [bold(X)](A) = 1/n sum_(i=1)^n delta_(X_i) (A) quad delta_(X_i)(A) = 1 "iff" X_i in A
$

$
  integral_Omega L_n [bold(X)](d x) = 1/n sum_(i=1)^n delta_(X_i) (Omega) = 1/n sum_(i=1)^n 1 = 1
$

The scalar parameter $k$ is replaced by a function $k: Omega -> cal(B)$. For discrete case, it's a vector form $bold(k) = (k_1,dots,k_m) thick forall m in Omega$; for continuous case, it's a usual function to adjust density in space for each $X_i = x in Omega$.

$
  bold(k) dot L_n = integral_Omega k(x) dot 1/n sum_(i=1)^n delta_(X_i) (d x) &= 1/n sum_(i=1)^n integral_(Omega) k(x) dot delta_(X_i) (d x) \
  &= 1/n sum_(i=1)^n k (X_i)
$

The scaled cumulant generating function can be calculated:

$
  Lambda (bold(k)) = lim_(n->infinity) 1/n ln expval(e^(n bold(k) dot L_n))
$

For discrete and continuous case:

$
  Lambda (bold(k)) = ln expval(e^(bold(k) dot L_n)) = ln sum_(j in Omega) P(X_i = j) e^(k_j) = ln sum_(j in Omega) rho_j e^(k_j) = ln expval(e^(k (X)))
$

$
  Lambda (bold(k)) = ln integral_Omega e^(k (x)) dot p(x) thin d x = ln expval(e^(k (X)))
$

$
  dv(Lambda(bold(k)), k(x), d: delta) = (p(x) e^(k (x)))/(expval(e^(k(X)))) = s (x) => k(x) = ln (s(x) expval(e^(k (X)))/p(x)) = ln s(x)/p(x) + Lambda(bold(k))
$

One immediately see that $integral_Omega s(x) d x = expval(e^(k (X)))/expval(e^(k (X))) = 1$ is the probability measure in $expval(dot)_(e^(k (X))$.

$
  I(s) = sup_(k) (bold(k) dot bold(s) - Lambda (bold(k))) = sum_(j in Omega) s(j) ln s(j)/p(j)
$

$
  I(s) = sup_(k) (bold(k) dot bold(s) - Lambda (bold(k))) = integral_(Omega) s(x) ln s(x)/p(x) d x
$

It's suggested that for a empirical density, one can investigate the probability distribution that matches such empirical density:

$
  P(L_n [bold(X)](x) in delta s) asymp e^(- I (bold(s)))
$

Which is the cost of our observation on the underneath real probability density $p(mu)$, called *relative entropy*. After enough observation, we conclude that the observation data should converge to the real underneath probability density. If the support of $s(mu)$ is larger than $p(mu)$, the functional will explode, and indicating that the thing never gonna happen as a zero probability.

The relative entropy is our establishment on _general maximal entropy principle_, which is the typical point or equilibrium point around behavior deeply related to maximal entropy.

$
  A_n (bold(omega)) = - 1/n ln p_n (bold(omega))
$

$
  Lambda (k) = lim_(n-> infinity) 1/n ln expval(e^(-k ln p_n)) &= lim_(n->infinity) 1/n ln (integral_(Omega) p_n^(-k)(omega) P_n (d omega)) \
  &= 1/n ln (integral_Omega p_n^(1-k) d omega) \
$

$
  Lambda'(k) = 1/n ln expval(p_n^(1-k))' = 1/n (p_n^(1-k) ln p_n)/expval(p_n^(1-k)) = s
$

$
  p_n^(1-k)/expval(p_n^(1-k)) ln p_n^(1-k)/expval(p_n^(1-k)) = p_n^(1-k)/expval(p_n^(1-k)) ((1-k) ln p_n - ln expval(p_n^(1-k))) = (1-k) s - Lambda (k)
$

Therefore let $p_n^(1-k)/expval(p_n^(1-k)) = q_k$

$
  I(s) = sup_(k) (k s - Lambda (k)) = H(q_k bar.double p)
$

If $X = sum_(i=1)^n X_i => p_n (bold(omega)) = p_n (X_1 = x_1, X_2 = x_2, dots, X_n = x_n) = product_(i=1)^n p$, one has:

$
  "LHS" = ln (integral_Omega p^(1-k) d omega) \
  A_n (bold(omega)) = - 1/n ln product_(i=1)^n p(omega) = ln p(omega) quad X_i = omega
$

Astonishingly suggests the "surprise" of one observe the probability in given sequence ${X_i = x_i}$.

$
  expval(A_n) & = integral_(Omega) A_n P_n (d omega) \
              & = -1/n integral_Omega p_n (omega) ln p_n (omega) d omega = 1/n H(p_n)
$

For IID:

$
  expval(A_n) = expval(A) = 1/n H(p_n) = H(p)
$

Such specific selection gives:

$
  Lambda' (0) = expval(A_n) = 1/n H(p_n)
$

If the limit of $A_n$ exists.

$
  S_n = 1/n sum_(i=1)^n f(omega_i)
$

In empirical vector:

$
  S_n = integral_Omega f(x) L_n [bold(X)] (x) d x = f dot L_n = 1/n sum_(i=1)^n f(omega_i)
$

$
  P(B_n in d b) = integral_(a: h(a) = b) P(A_n in d a) = integral_(a:h(a) = b) e^(-k I(a)) d a asymp exp (-k inf_(a:h(a) = b) I_A (a)) d a
$

Where, apply the same strategy that $P (B_n in d b)$ should be evaluated in saddle point of distribution in $P(A_n in d a)$, which is the $inf_(a:h(a)=b) I_A (a)$.

It evaluates that given a observation of data of $f$, what's the probability distribution in real?

$
  P(L_n in d mu,f dot L_n (mu) in d s) => I_1 (s) = inf_(mu: f dot L_n (mu) = s) I_2 (mu)
$

Where $P (f dot L_n (mu) in d s) => I_1 (s)$ and $P(L_n in d mu) => I_2 (mu)$.

Reversely, one gets the conditional probability:

$
  P(L_n in d mu|f dot L_n in d s) = P(L_n in d mu,f dot L_n in d s)/P(f dot L_n in d s) = I_2 (mu) - I_1 (s) = I^s (s) "if" h(mu) = s
$

To see the global minima, notice that $I_1 (s) <= I_2 (mu) thick forall mu: L_n (mu) = s$. By above choice, one gets $inf_(mu) I^s (mu) = I_2 (mu) - I_1 (s) = 0$.

Previously, we deduce Binary sample in equal probability case, we now choose an arbitrary one:

$
  P(X = 1) = p, P(X=-1) = q \
  s(X = 1) = p', s(X=-1) = q' "where" s "is arbitrary binary distribution with" q' >= q \
$

$
  I(s) = H(s bar.double P) = q' ln q'/q + p' ln p'/p = q' ln q'/q + (1-q') ln (1-q')/(1-q)
$

Suppose we want to shift from the distribution $s$ to expectation value of distribution $s$ for rate function evaluation.

$
  expval(X)_s = 1-2q' = s => q' = (1-expval(X)_s)/2
$

Due to notation abusing, the expectation value, which we denote as $expval(X)_s = s'$ for alleviation.

$
  I(s') = H(s bar.double p)(s') & = (1-s')/2 ln (1-s')/2q + (1+s')/2 ln (1+s')/(2(1-q)) \
                                & = 1/2 ((1+s')ln (1+s')/(2p) + (1-s')ln (1+s')/(2(1-q)))
$

Which is same as previous example as $I(s') = I(s)$ if $p = q = 1/2$.

= Hamiltonian

Given a phase space with coordinates $mu = (bold(q),bold(p))$ where $bold(q) = (q^1,...,q^(N))$ and $bold(p) = (p^1,...,p^(N))$. Given a volume in such phase space, denotes the initial condition as $cal(R)(0) = { mu(0) | mu(0) in cal(R)_0 } ->^("time evolution") cal(R)(t) = { mu(t) | mu(0) in cal(R) }$. For a instance time $t -> t + epsilon$, we has:

$
  d mu_(t+ epsilon) &= det((partial mu_(t+epsilon))/(partial mu_(t))) d mu_t \
  &= det(delta_(i j) + epsilon (partial dot(mu)_(t i))/(partial mu_(t j)) + O(t^2)) d mu_t \
  &= (1 + epsilon "Tr"((partial dot(mu)_(t))/(partial mu_(t)))_i + O(t^2)) d mu_t quad (log det M = "Tr" log M) \
$

We haven't introduce the dynamic equation yet, if it satisfy the canonical form:

$
  "Tr"(...) = ((partial dot(q)_(t i))/(partial q_(t i)) + ( q -> p)) = ((partial)/(partial q_(t i)) (partial H)/(partial p_(t i)) - (partial)/(partial p_(t i)) (partial H)/(partial q_(t i))) = 0
$

Which is just a reframe of the basic Hamiltonian equation, because we just integrate phase point solely.

That's, given a distribution $rho(mu, t)$:
$
  rho (mu, t) = rho (bold(p), bold(q), t) \
  (d rho)/(d t) = (partial rho)/(partial t) + {rho, H} = 0 \
$

Above called _Liouville's equation_.

A famous theorem is _Poincaré recurrence theorem_, which states that for a system with finite energy, the system will return to a state arbitrarily close to the initial state after a sufficiently long time. This is a consequence of the conservation of phase space volume and the deterministic nature of Hamiltonian dynamics.

Given a distribution $delta (E - H(bold(q),bold(p)))$, one has the possible phase space volume as the total volume $Tau$ the initial condition can transverse, for example $p^2/(2m) + 1/2 m omega^2 x^2 = H(x,p) = E$. Then we can apply a continuous transformation to the phase space volume, due to *finite energy/volume*, the union space. We clarify such transformation as $g_tau$ with given $tau$ as time parameter or any parameter you want, then we has:

$
  Tau = union.big_(k=0)^(infinity) g_tau^k cal(R)_0 quad cal(R)_0 "is initial condition phase volume" \
$

Thus we must have intersection of possible transverse like $k$ to $k + l$ finitely, otherwise $Tau$ would be infinite due to infinite disjoint sets.

$
  g^k_tau cal(R)_0 inter g^(k +l)_tau cal(R)_0 != emptyset ->^(g "is reversible") cal(R)_0 inter g^l_tau cal(R)_0 != emptyset \
$
Which prove the theorem. It said that for a non-dissipative or closed(*invertible + volume preservation*), *finite* system, the system will emerge recurrence. However, this theorem is not collide with macro equilibrium.

== Kac Ring Model


#figure(
  image("assets/sm-flipper.png", width: 80%),
  caption: [Left: A configuration of the Kac ring with $N = 16$ sites and $F = 4$ flippers. The flippers, which live on the links, are represented by blue dots. Right: The ring system after one time step. Evolution proceeds by clockwise rotation. Spins passing through flippers are flipped."],
)

Above picture shows a simple model, $N$ sites is a instance with spin up and down, then we also have $F$ flippers on the link between sites, which can flip spin instance. The evolution is just rotate the ring clockwise one step and the spin instance would be flipped if it pass through the flipper. Thus, it's deterministic and invertible with finite state. It must has *recurrence*. #footnote[You may wonder why we can apply recurrence to a system without canonical Hamiltonian equation. The reason is that the theorem is not about Hamiltonian system, but about the finite state system with invertible and state volume preservation.]

Now suppose $s(0) = (s_i (0))$ is the initial state, we has a general probability relation:

$
  s_i (+) = 1, s_i (-) = -1 \
  sum_i s_i (+) (n+1) = (N - F)/N sum_i s_i (+) (n) + F/N sum_i s_i (-) (n)\
$

$
  N^+ + N^- = N \
  p^+ (n+1) = (1 - eta) p^+ (n) + eta (1 - p^+ (n)) quad eta = F/N \
  p^+ (n+1) = (1-2 eta) p^+ (n) + eta \
$

Thus one should have:

$
  p^+(n) = a + b (1-2eta)^n \
  p^+(0) = a + b \
  p^+(infinity) = 1/2 = a \
  p^+(n) = 1/2 + (p^+(0) - 1/2) (1-2eta)^n \
$

#figure(
  image("assets/sm-kac-test.png", width: 80%),
  caption: [Three simulations of the Kac ring model with $N = 2500$ sites and three different concentrations of flippers. The red line shows the magnetization as a function of time, starting from an initial configuration in which 100% of the spins are up. The blue line shows the prediction of the Stosszahlansatz, which yields an exponentially decaying magnetization with time constant $tau$.],
)


It's astonishing that given a priori uniform distribution, one can acquire a probability evolution, without any confliction with deterministic evolution, which we cast off information for a specific ring and presume a potential microstates in priori uniform distribution.

Now we construct the microscopic state:
$
  bold(X)(t) = (s_1(t), s_2(t), ... ,s_N (t)| m_1(t), m_2(t),... m_F (t)) quad (s_(i+1)(t) = m_i s_i (t))
$

For each micro state, one can generate by permutation choices of flippers, which is $vec(N, F)$, however we know many of them is same for unknown observer, such process called *coarse-graining* or *projection*, which is often the averaging over irrelevant degrees of freedom, losing micro information increasing macro entropy.

Now the macro state is evident that:
$
  Delta (t) = sum_i s_i (t) quad (s_i (+) = 1, s_i (-) = -1) \
$

With such projection:

$
  Delta(t) = sum_bold(m) P(bold(m)) Delta(t|bold(m))
$
For each general ensemble of flipper distribution, which is priori a uniform distribution(a.k.a closed system), one can decompose as:

$
  Delta(t) & = sum_(bold(m)) 1/vec(N, F) Delta(t|bold(m)) \
           & = sum_(bold(m)) 1/vec(N, F) sum_i s_i^+ (t|bold(m))
$

$
  sum_i s_i^+(t|bold(m)) = sum_i (product_(k=0)^(t-1) m_(i - k) s_i (0)) = product_(k=0)^(t-1) m_(i - k) Delta(0)
$
The key is the uniform distribution that:

$
  chevron.l product_(k=0)^(t-1) m_(i-k) chevron.r = product_(k=0)^(t-1) chevron.l m_(i-k) chevron.r = product_(k=0)^(t-1) (-P(m_i = -1) + P(m_i = +1)) = product_(k=0)^(t-1) (1-2 eta) = (1-2 eta)^t
$

Thus, the distribution of $bold(m)$ is actually unimportant, which is cancel out.

$
  Delta(t) = (1-2 eta)^t Delta(0)
$

$
  & Delta^(+) (t) + Delta^(-) (t) = Delta (t) \
  & Delta^(+) (t) - Delta^(-) (t) = N
$

$
  & Delta^+(t) = 1/2(N + Delta(t)) = 1/2 sum_i (1 + s_i (t)) \
  & Delta^+(t) = 1/2 (N + (1-2 eta)^t Delta(0))
$

Which is indeed the original solution. That's more rigorous process demonstrate how we establish the distribution in blurring information, in which we lose initial condition and presume flippers counts only. Following from the probability investigation, we can therefore recover the *true* probability distribution based on the test, because there's no guarantee a uniform distribution for potential flippers distribution.

If we consider the all micro state entropy, it should be fixed that transverse all *priori* uniform distribution. rather, if we consider an *ensemble* of rings in macro state, one has:

$
  H_("micro")("up/down") = ln Omega = ln 2^N = N ln 2 quad "fixed"
$

$
  H("flippers") & = ln (vec(N, M)) = ln ((N!)/(M!(N-M)!)) \
                & ~ N ln N - N - M ln M + M - (N-M) ln (N-M) + (N-M) \
                & ~ - N (M/N ln M/N - (1-M/N) ln (N-M)/N ) \
                & ~ - N (eta ln eta + (1-eta) ln (1-eta)) quad "fixed"
$

$
  H_("macro")("up/down")(t) = - N (p ln p + (1-p)ln(1-p)) quad p(t) = (Delta^+(t))/N
$

It has the maximum in $p = 1/2$ as the convergence results, showing the entropy increasing dynamics based on macro state, reaching the micro state entropy.

Now we can summarize to answer the problem of _Hamilton Dynamics_, why micro determinism will emerge macro uncertainty? It's plausible to say information is a key, first, it's objective but relative, like speed, it's a coarse-graining process to shed underneath initial condition, we have no idea about the concrete position and momentum but a *priori* potential distribution of them, from which, the observation tells us, in a enough time, one should approach the real distribution.

= Ergodicity

A stronger statement is _ergodicity_, it means given all possible phase volume $Tau$, the distribution of phase point in a longer enough time would transverse all possible phase point in $Tau$, in $t -> infinity$:

$
  chevron.l rho(mu) chevron.r_t & = lim_(T -> infinity) (1/T) integral_0^(T) d mu rho (mu t) \
                            & = integral d mu rho(mu) delta(E - H(mu)) \/ integral d mu delta(E - H(mu)) \
                            & = chevron.l rho(mu) chevron.r_E
$

Usually, denoted as the hyper-surface as:

$
  D(E) = integral d mu delta(E - H(mu)) = integral_(S_E) d Sigma_E
$

The integral inspection doesn't ensure the stability of the distribution, clearly, we can have a distribution with oscillation in time and with a suitable boundary condition, which make cause equality, but the oscillation property of the distribution won't disappear in time.

$
  f(q,p) = sum_(m,n) hat(f)_(m,n) e^(i m q + i n p) \
  expval(f(q,p))_t = hat(f)_(0,0) = expval(f(q,p))_E \
$

= Fundamental

First, we explore the specific case for mean energy $h_n$ respect to priori distribution $P_n (d Omega)$ defined in $Omega_n$ for $n$-particles.

$
  P(h_n in d u) = integral_({h_n (omega) in d u|omega in Omega_n}) P(d omega) \
$

For uniform priori measure, a closed system, is $P(d omega) = d omega\/abs(Omega_n)$.

$
  Omega (h_n in d u) = integral_({h_n (omega) in d u|omega in Omega_n}) d omega
$

of microstates $omega$ such that $h_n (omega) in d u$. Now rate function is clear.

$
  & I (u) = lim_(n->infinity) -1/n ln P(h_n in d u) = ln abs(Omega_n) - I_0(u) \
  & I_0 (u) = lim_(n->infinity) 1/n ln Omega_n (h_n in d u)
$

is the _microcanonical entropy_ or _entropy density_. The constant is irrelevant which can be absorbed into rate function.

// That's, given the energy bound as $delta(E-H(mu))$, one has a energy shell that contains the possible states. In a uniform prior measure we can reduce the constant and use the latter $I'(u)$, which called $s(u)$ in classical expression.

$
  &Lambda(k) = lim_(n->infinity) 1/n ln expval(e^(n beta h_n)) = -Lambda_0(-k) - ln abs(Omega_n) \
  &Lambda_0 (beta) = lim_(n->infinity) -1/n ln integral_(Omega_n) e^(-n beta h_n (omega)) d omega = lim_(n->infinity) - 1/n integral_(Omega_n) e^(- beta H (omega)) d omega
$

Actually, we immediately inspect that $Lambda_0 (-k)$ is the canonical free energy function. By Legendre duality, one can recover each other for closed system and heat-bath system. Now we rename the these function to a familiar notation in statistical mechanics: $I_0 => s_0, Lambda_0 => phi$.

We have above _Legendre-Fenchel Transformation_ which is the saddle point transformation of _Laplace Transformation_.

$
  & phi(beta) = inf_u (beta u - s(u)) \
  & s(u) = inf_beta (beta u - phi(beta)) \
$

Due to the common notation about negative sign, from $sup -> inf$ is evident. If the whole is differentiable, it should be convex and contains global minimum, else, it contains multiple, or *phase transformation* in such non-differentiable configuration.

Now the problem is how to turn each particles microstates into a macrostates of such system. We consider the case where $H_n (omega) = sum_i h_n (omega) = U$ or $h_n (omega) = u$.

Suppose now, given a macro state, the constrained probability measure is given by:

$
  P^(u) (d omega) = P (d omega bar h_n in d u) = cases(P(d omega)/P(h_n in d u) "if" h_n (omega) in d u, 0 "otherwise")
$

$
  integral_Omega P^(u) (d omega) = 1/(P(h_n in d u)) integral_({omega in Omega|h_n(omega) in d u}) P(d omega) = 1
$

Given a macrostate $M_n in d m$, the probability of one observe it is the conditional probability by:

$
  P^u (M_n in d m) = P(M_n in d m|h_n in d u) = (P(h_n in d u, M_n in d m))/(P(h_n in d u))
$

Large deviation tells us, we should expect the most probable value of $M_n$ by locating the global minima of the corresponding rate function.

$
  P (M_n in d m) = integral_({omega in Omega|M_n (omega) in d m}) P(d omega) asymp e^(- n I_m (m)) d m
$

$
  P(h_n in d u) asymp e^(-n I_h (u)) d u
$

The evaluated space is different for macrostate and microstate, first choice is to take a variable transformation such that:

$
  lim_(n -> infinity) h_n (omega) - h_n (M_n (omega)) -> 0
$

Uniformly as $n -> infinity$ just in case of mathematical rigorousness, called _energy representation function_. Or worse, a joint probability as:

$
  P (h_n in d u, M_n (omega) in d m) asymp e^(n I (u,m)) d u d m
$

At least in theory deduction.

$
  P^u (M_n in d m) asymp e^(-n (I (u,m) - I_h (u))) d m
$

Now everything is clear that the rate function must be the one as section deduction consequence shown. Which should be the global minima that:

$
  cal(S) = {m in Omega_m|I (u,m) - I_h (u) = 0}
$

By previous investigation on large deviation of joint probability.

Such macrostates is the _equilibrium states_. The corresponding macrostates probability distribution must be the one minimize above. We will see how the necessity arise in derivation of _Jayne's Maximum Entropy Principle_.

$
  L_n (epsilon) = 1/n sum_(i=1)^n delta(epsilon - epsilon_i)
$

Where the macrostate is the *observation* of probability distribution $L_n in mu$ where $mu$ is arbitrary probability distribution.#footnote[So it's clear that macrostate can also be a distribution we observed.]

$
  h_n = 1/n sum_(i=1)^n epsilon_i = integral_(Omega) epsilon dot L_n (epsilon) d epsilon
$

By _Sanov's Theorem_, the large deviation of $L_n$ are ruled by the relative entropy $I(mu)$, where the priori distribution is uniform distribution. But we will deduce for arbitrary distribution.

$
  I (mu) = integral_(Omega_epsilon) mu (epsilon) ln mu(epsilon)/rho(epsilon) d epsilon
$

If $rho (epsilon) = abs(Omega)^(-1)$:

$
  I (mu) & = integral_(Omega_epsilon) mu (epsilon) (ln mu(epsilon) + ln abs(Omega)) d epsilon \
         & = - s (mu) + ln abs(Omega)
$

Where $s (mu) = - integral_(Omega_epsilon) mu(epsilon) ln mu(epsilon) d epsilon$ is the _Boltzmann-Gibbs-Shannon entropy_. By contraction theorem, $I_h (u) = inf_(mu: h_n (mu) = u) I (mu)$

By definition, the _microcanonical entropy_ is $s(u)$:

$
  s (u) = sup_(mu: h_n (mu) = u) {- I (mu)} = sup_(mu: h_n (mu) = u) {s (mu)} - ln abs(Omega)
$

The way to maximize is done by Lagrange multiplier.

$
  cal(L)[mu] = - integral_(Omega_epsilon) mu ln mu/rho d epsilon + lambda_1 (integral_(Omega_epsilon) mu d epsilon - 1) + lambda_2 (integral_(Omega_epsilon) epsilon mu thin d epsilon - u)
$

$
  ln mu(epsilon)/rho(epsilon) & = lambda_1 - 1 + lambda_2 epsilon \
                  mu(epsilon) & prop rho(epsilon) e^(- beta epsilon)
$

$
  h_n (L_n in d mu) = integral_(Omega_epsilon) epsilon mu thin d epsilon = u
$

Is the constraint. Statistical Mechanics tells us $beta = lambda_2 = 1/(k T)$ where $k$ is Boltzmann constant can be solved reversely by constraint. One recover partition function with internal energy relation:

$
  mu (epsilon) = e^(- beta epsilon)/(Z (beta)), quad Z(beta) = integral_(Omega_epsilon) e^(- beta epsilon) d epsilon
$

$
  - dv(ln Z(beta), beta) = - (Z'(beta))/Z(beta) = 1/Z(beta) integral_(Omega_epsilon) epsilon e^(-beta epsilon) d epsilon = integral_(Omega_epsilon) epsilon mu thin d epsilon = u
$

For example, suppose a system with ${epsilon_1, epsilon_2}$ as two-state energy system, with the given constraint $h_n (L_n in d mu) = integral_(Omega_epsilon) epsilon mu d epsilon = u$.

$
  s (mu) = - (mu_1 ln mu_1 + mu_2 ln mu_2), quad mu_1 + mu_2 = 1
$

By probability distribution $mu := (mu_1, mu_2) := delta (epsilon_1, mu_1) + delta(epsilon_2, mu_2)$ for each state.

$
  h(mu) = mu_1 epsilon_1 + mu_2 epsilon_2 = u \
$

$
  mu_1^* = (u - epsilon_2)/(epsilon_1 - epsilon_2), quad
  mu_2^* = (epsilon_1 - u)/(epsilon_1 - epsilon_2)
$

$
  s(u) = s(mu^*) = - ((u - epsilon_2)/(epsilon_1 - epsilon_2) ln (u-epsilon_2)/(epsilon_1 -epsilon_2) + (mu_1^* <-> mu_2^*))
$

Finally, $beta = dv(s(u), u)$:

$
  beta = 1/(epsilon_1 - epsilon_2) ln (epsilon_1 - u)/(u - epsilon_2) \
  e^(beta (epsilon_1 - epsilon_2)) = (mu_2^*)/mu^*_1 = e^(-beta epsilon_2)/(e^(- beta epsilon_1))
$

$
  Z(beta) = e^(- beta epsilon_1) + e^(- beta epsilon_2)
$

From fixed energy we deduce the temperature as microcanonical ensemble.

// $
//   Z(beta) = cal(L)[D(epsilon)] = integral_(Omega_epsilon) e^(-beta H_n (omega)) D(epsilon) thin d epsilon,quad D(epsilon) = integral_Omega delta(epsilon - H(omega)) P(d omega)
// $


Same procedure in proof of large deviation can be applied to deduce with fixed temperature:

$
  P_beta (d omega) = e^(- beta n h_n (omega))/(Z_n (beta)) P(d omega),quad Z_n (beta) = integral e^(- beta n h_n (omega)) P (d omega)
$

Since

$
  P(M_n in d m) asymp e^(- n s(m))
$

Then:

$
  P_beta (M_n in d m) = integral_({omega in Omega|M_n (omega) in d m})P_beta (d omega) asymp e^(- n I_beta (m))
$

$
  I_beta (m) = beta h_n (m) - s (m) - phi(beta), quad phi(beta) = lim_(n->infinity) 1/n Z_n (beta)
$

Or in joint probability $P(h_n in d u, M_n in d m)$ with macro-entropy $s(u,m)$:

$
  I_beta (m) = inf_(u) {beta u - s(u,m)} - phi(beta)
$

With the set:

$
  cal(S) = {m in Omega_m|I_beta (m) = 0}
$


Therefore one recover the definition too:

$
  phi(beta) = inf_m {beta h_n (m) - s(m)}
$

Or in joint probability:

$
  phi(beta) = inf_m inf_u {beta u - s(u,m)}
$

The partition function in macrostate:

$
  Z_n (beta) asymp integral_(Omega_m) e^(-n beta h_n (m)) P(M_n in d m) asymp integral_(Omega_m) e^(-n (beta h_n (m) - s(m))) d m asymp e^(-n inf_m {beta h_n (m) - s(m)})
$

The same two-state energy system can be applied too:

$
  h(mu) = mu_1 epsilon_1 + mu_2 epsilon_2 \
  s(mu) = - (mu_1 ln mu_1 + mu_2 ln mu_2) \
$

$
  mu_1 + mu_2 = 1
$

With the minimization of $phi(beta)$:

$
  phi(beta) = beta h(mu) + s (mu)
$

$
  pdv(f, mu_1) = 0 => ln (mu_1/(1-mu_1)) = - beta (epsilon_1 - epsilon_2)
$

$
  (mu_2^*)/mu_1^* = e^(- beta epsilon_2)/(e^(- beta epsilon_1))
$

From given temperature to energy.

Several useful equations can be derived with the most expected distribution $mu^*$:

$
  - integral_(Omega_m) mu^* ln mu^* thin d m = beta u + ln Z(beta) = s(mu) = beta (- f + u)
$

$
  - beta^(-1) ln Z(beta) = f
$

$
  s(u) = s(mu^*) = ln Z(beta) - beta dv(ln Z(beta), beta)
$

For general force $k_i$ with general displacement $l_i$ in macrostates:

$
  k_i = pdv(f, l_i) = - beta^(-1) pdv(ln Z(beta), l_i)
$

Fluctuations has already been induced in the investigation of $e^(k X)$ where double differentiation is variance.

$
  - pdv(u, beta) = pdv(ln Z, beta, 2) = expval(H^2) - expval(H)^2
$

$
  pdv(k_i, l_i) = pdv(f, l_i, 2) = beta^(-2) pdv(ln Z(beta), l_i, 2) = expval(k_i^2) - expval(k_i)^2
$

Generally, any family of observables can be incorporated by imposing restriction such as $hat(q) =expval(q)$ that permutes with Hamiltonian. For an arbitrary countable collection of macrostates, the same formalism applies: $sum_i lambda_i q_i$ like energy, magnetization, particles number and related quantities. In statistical mechanics, physicist typically adopt an modified Hamiltonian by $sum_i lambda_i q_i => beta (h_i + sum_i q_i lambda_i \/beta)$ as _Grand Canonical Ensemble_ shown. In which the conjugated pair #footnote[$mu_f$, $n$ where $k$ is adopted by above notation of general force and displacement.] $mu_f <-> n$  where $mu_f$ is fugacity and $n$ is particle number or particle density, the probability distribution $mu^* = exp(- n beta (h - mu_f))$.

$
  italic(Xi)_n (beta,mu) = integral_Omega_m e^(- n beta(h_n - mu_f)) d m = integral_(Omega_m) e^(-n beta mu_f) e^(- n beta h_n) d m 
$

If $d m = d m' d n$, and $n in {0,1,dots}$:

$
  italic(Xi)_n (beta,mu) = sum_(n=0)^infinity e^(beta mu n) Z_n (beta)
$

Just for simplicity in cell division for such case.

#quote(attribution: [The large deviation approach to statistical mechanics -- Hugo Touchette], block: true)[
  ... The class of macrostates for which large deviation principles can be derived in the canonical ensemble is exactly the
  same as in the microcanonical ensemble, since the rate functions of these two ensembles are built from the same energy. representation function and macrostate entropies.
]

#import "../lib.typ": *
#import "@preview/physica:0.9.8": *

#let abstract-en = [In this work, we present a unified and pedagogical introduction to several fundamental numerical methods for solving partial differential equations arising in computational physics. We begin by reviewing the finite difference method and providing a general framework for analyzing the stability and convergence of schemes for parabolic equations. Both classical von Neumann (Fourier) analysis and the energy/entropy method are discussed, highlighting their respective roles in understanding numerical stability.

  We then introduce pseudo-spectral methods and develop the associated Gaussian quadrature and orthogonal polynomial machinery through a streamlined and conceptually transparent derivation, improving upon traditional proofs. Finally, we demonstrate how the time-independent Schrödinger equation can be discretized naturally within the pseudo-spectral framework, yielding accurate and efficient numerical approximations.

  Our exposition aims to bridge foundational theory with computational practice, offering a coherent route from basic discretization techniques to modern spectral approaches.]

#let abstract-zh = [
  本工作对计算物理中若干常用的偏微分方程数值方法进行了系统而简明的介绍。首先回顾有限差分法，并对抛物型方程的离散格式给出一般性的稳定性与收敛性分析，讨论了经典的 von Neumann（傅里叶）分析方法以及能量法与熵估计在稳定性研究中的作用。

  随后，引入伪谱方法（pseudo-spectral methods），并以一种比传统推导更为简洁清晰的方式构建高斯求积与正交多项式所依赖的基本理论。最后，展示如何在伪谱框架下将定态薛定谔方程离散化，从而获得高精度且高效率的数值近似。

  本文旨在在基础离散方法与现代谱方法之间建立逻辑连贯的桥梁，为计算物理中的数值求解提供理论与实践相结合的完整思路。
]

#let intro-en = [
  The numerical solution of partial differential equations (PDEs) plays a central role in computational physics, where accurate and efficient discretization schemes are essential for modeling diffusion, wave propagation, quantum systems, and a variety of multiscale phenomena. Although a wide range of numerical techniques has been developed, a coherent understanding of their stability, convergence, and underlying mathematical structure remains fundamental for both theoretical analysis and practical computation.

  This work is organized with the goal of building a conceptual path from classical discretization techniques to modern spectral methods. We begin with the finite difference method, whose simplicity makes it an ideal setting for introducing stability and convergence theory. For parabolic equations, we discuss two complementary tools: the von Neumann Fourier analysis, which provides a frequency-space perspective on amplification factors, and the energy/entropy method, which yields robust stability estimates even when Fourier analysis is not directly applicable.

  Moving beyond local discretization, we introduce pseudo-spectral methods, where global basis functions lead to high-order—or even spectral—accuracy. To support this framework, we provide a streamlined derivation of Gaussian quadrature and orthogonal polynomials, emphasizing the structural properties that make spectral methods both powerful and elegant. As a concrete application, we formulate the time-independent Schrödinger equation within the pseudo-spectral setting and examine its resulting discrete eigenvalue problem.

  Through this progression, the paper seeks to offer an integrated view of numerical PDE methods, illustrating how classical ideas naturally evolve into spectral techniques that are central to modern computational physics.
]

#let intro-zh = [
  偏微分方程的数值求解在计算物理中占据核心地位。无论是扩散过程、波动传播，还是量子体系的能谱计算，稳定且高效的离散化方法都是构建可靠模型的关键。尽管近年来各类数值方法不断发展，但要深入理解其稳定性、收敛性及背后的数学结构，仍需从基本框架出发建立系统的认识。

  本文旨在构建一条从经典离散方法通向现代谱方法的逻辑路线。我们首先从有限差分法开始，其结构直观，适合作为介绍稳定性与收敛性理论的起点。针对抛物型方程，我们分别讨论 von Neumann（傅里叶）分析与能量法 / 熵估计两种互补的工具：前者从频率角度刻画放大因子，后者则在更普适的框架下提供稳定性控制。

  在此基础上，我们进一步引入伪谱方法。相较局部离散方式，伪谱方法使用全局基函数，可获得高阶甚至谱精度。为构建该方法所需的数学基础，我们给出高斯求积与正交多项式的简化推导，强调其结构特性如何自然地支持谱方法的高效性与优雅性。作为具体示例，我们将定态薛定谔方程置于伪谱框架下，并讨论其所得到的离散特征值问题。

  通过上述内容的衔接，本文希望呈现数值 PDE 方法的整体图景，展示从传统离散思想到现代谱方法的自然演进过程，为计算物理的实际计算提供理论与方法上的统一视角。
]

#let end-en = [
  In this work, we have presented a coherent introduction to several core numerical methods used in computational physics, emphasizing the stability, convergence, and structural properties underlying their effectiveness. Beginning with finite difference schemes, we examined general stability theory for parabolic equations through both Fourier (von Neumann) analysis and the energy/entropy method, highlighting the complementary insights offered by these approaches.

  We then turned to pseudo-spectral methods and provided a streamlined development of the Gaussian quadrature and orthogonal polynomial framework that supports them. This derivation not only simplifies classical proofs but also clarifies the mathematical mechanisms responsible for the high-order accuracy characteristic of spectral techniques. As an application, we demonstrated how the time-independent Schrödinger equation can be discretized within the pseudo-spectral setting, resulting in an efficient and accurate numerical representation.

  Taken together, these elements form a continuous progression from local, low-order discretizations to global, high-accuracy spectral methods. We hope that the exposition offered here serves as a useful reference for readers seeking both conceptual understanding and practical tools for solving PDEs in computational physics.
]

#let end-zh = [
  本文系统地介绍了计算物理中若干核心的偏微分方程数值方法，并重点讨论了它们在稳定性、收敛性及数学结构方面的关键特征。首先，我们从有限差分法出发，利用傅里叶（von Neumann）分析以及能量法 / 熵估计，对抛物型方程的离散格式进行了全面的稳定性探讨，展示了两种方法在理论上的互补性。

  随后，我们引入伪谱方法，并以更为简洁的方式推导了其所依赖的高斯求积与正交多项式的基础理论。这种推导不仅简化了传统证明，也更清晰地呈现了谱方法能够实现高阶精度的数学机制。通过将定态薛定谔方程置于伪谱框架下，我们展示了其离散化方法的有效性与高精度特点。

  总体而言，本文构建了一条从局部低阶离散方法到全局高精度谱方法的连续路线。希望本文的呈现能够为读者在计算物理中求解偏微分方程提供兼具概念深度与实际应用价值的参考。
]

#let keywords-en = (
  "Finite Difference Method",
  "Stability and Convergence",
  "Pseudo-spectral Methods",
  "Gaussian Quadrature",
  "Computational Physics",
)

#let keywords-zh = (
  "有限差分法",
  "稳定性与收敛性",
  "伪谱方法",
  "高斯求积",
  "计算物理",
)

#show: mine.with(
  template: "daily-en",
  title: (en: "Exploring Finite Difference and Pseudo-Spectral Methods",zh: "有限差分法与伪谱法探索"),
  abstract: abstract-en,
  keywords: keywords-en,
)

#let vf(content) = $upright(bold(content))$

= 引言

#intro-en

= Finite Difference Methods

The fundamental role of _Schrödinger's equation_ is no doubt, which is considered as a heat equation by certain variables transformation.

$
  i planck pdv(, t) psi = hat(H) psi \
$

Generally, it's demonstrated as below form.

$
  u_t = u_(x x) + V(x) u
$

To discretize the equation, suppose $x_j = j Delta x = j h_x$, $t_j = j Delta t = j h_t$ as finite elements. While to distinguish the discretized form:

$
  u(x,t) -> u[i](t) -> u[i,j]
$

A second order differentiation thus is represented:

$
  u_(x x) = (u[i+1] - 2 u[i] - u[i-1])/h_x^2 = 1/h^2 D_(x,+) D_(x,-) u[i]
$

$
  u_t = 1/h^2 D_(x,+) D_(x,-) u[i] + V[i] u[i] = H u[i]
$

We introduce few common methods in general:@chern_solving_nodate[p~26]

- Forward Euler method:

$
  u[i,j] - u[i,j-1] = h_t H u[i,j-1]
$

- Backward Euler method:

$
  u[i,j] - u[i,j-1] = h_t H u[i,j]
$

- 2nd order Runge-Kutta (RK2):

$
  & u[i,j+1] - u[i,j-1] = h_t H u[i,j+1/2] \
  & u[i,j+1/2] = u[i,j] + h_t/2 H u[i,j]
$

The error comes from two sources, the first is the local truncation error due to finite differentiation, the second is the deduction error due to iterations@chern_solving_nodate[p~27]:

$
  u_t = D_(t,+) u(x_i,t_j) + (u_t - D_(t,+) u(x_i,t_j)) = D_(t,+) u(x_i,t_j) + tau_t [i,j] \
$
$
  u_(x x) & = D_(x,+) D_(x,-) u(x_i,t_j) + (u_(x x) - D_(x,+) D_(x,-) u(x_i,t_j)) \
          & = D_(x,+) D_(x,-) u(x_i, t_j) + tau_(x x) [i,j] \
$
$
  tau [i,j] = tau_(x x) [i,j] + tau_t [i,j] = O(h_t) + O(h_x^2)
$

However, it only involves the difference error or local truncation error. We should adjust the deduction error:

$
  e[i,j] = u(x_i,t_j) - u[i,j] \
$

$
  u(x_i,t_(j+1)) - u(x_i,t_j) = & h_t/h_x^2 (u(x_(i+1),t_j) - 2u(x_i, t_j) + u(x_(i-1),t_j)) \
                                & + h_t tau [i,j]
$

Subtract the exact differentiation terms by the real deduction terms, resulting error terms:

$
  e[i,j+1] - e[i,j] = h_t/h_x^2 (e[i+1,j] - 2e[i,j] + e[i-1,j]) + h_t tau[i,j]
$

Absorbs all terms about $e[i,j]$ as $G$, a linear operator to be investigated.

$
  e[i,j+1] = G e[i,j] + h_t tau[i,j]
$

Expanding all possible deductions:

$
  norm(e[i,j+1]) & = norm(G e[i,j]) + h_t norm(tau[i,j]) \
                 & <= norm(G^2 e[i,j-1]) + h_t (norm(G tau[i,j-1]) + norm(tau[i,j])) \
                 & <= norm(G^(j+1) e[i,0]) + h_t sum_(m=0)^j (norm(G^m tau [i,j-m]))
$

Suppose the matrix $G$ satisfies _stability_ condition or _bounded_ in _any_ order:

$
  norm(G^n u[j]) <= C norm(u[j])
$

For some scalar $C$ independent of $n$.

$
  norm(e[i,j+1]) <= C_1 norm(e[i,0]) + C_2 max_m abs(tau[i,j-m])
$

For possible scalar $C_1$ and $C_2$. It implies that we only need to restriction certain condition on $tau$. If the local truncation error is _consistent_:

$
  max_m norm(tau [i,j-m]) = O(h_x^2) + O(h_t)
$

And the initial deduction error satisfies:
$
  norm(e [i,0]) = O(h^2)
$

In such, the global true error:

$
  norm(e[i,j]) = O(h_x^2) + O(h_t)
$

To systematically exemplify this, one commonly say that error is _convergent_ if:

$
  norm(e[i,j]) -> 0 "if" h_(\(dot\)) -> 0
$

Thus indeed, if operator $G$ is locally _stable_ for our estimated region and truncation error is _consistent_:

$
  #[_stability_ + _consistency_] => #[_convergence_]
$

== von Neumann Analysis

Given $u[i]$ as a discretization of a function, or vector-form with each elements ${u[i]}_(j in bb(Z))$. One can define the norm:

$
  norm(u[i])_(L^2) = sum_(i in bb(Z)) abs(u[i])^2
$

A usual way to analyze the stability is to use Fourier analysis@chern_solving_nodate[p~28]. To avoid confusion of $i$ as imaginary unit and as indices, we use $j$ as indices:

$
  hat(u)(omega) = 1/(2 pi) sum_(j in bb(Z)) u[j]|_j e^(- i omega j), omega in [-pi, pi]
$

Notice $hat(u)[omega + 2pi] = hat(u)(omega)$ due to integer indices.

- The shift operator is transformed to a multiplier function:

$
  T_1 u[j] = u[j+1] => hat(T_1 u)(omega) = e^(i omega) hat(u)(omega)
$

It's shown that the differentiation becomes:

$
  D_+ u[j] = 1/h_x (T_1 u[j] - u[j]) => hat(D_+) hat(u)(omega) = 1/h_x (e^(i omega) - 1) hat(u)(omega)
$

- The Parseval equality:

$
  norm(hat(u)(omega))^2 &= integral_(-pi)^(pi) 1/((2pi)^2) sum_(j in bb(Z)) u^*[j] e^(-i omega j) sum_(k in bb(Z)) u[k] e^(-i omega k) d omega\
  &= 1/(2pi) sum_(j in bb(Z)) u^*[j] u[j] = 1/(2 pi) norm(u[j])^2
$

To reduce notation, we omit $2pi$ factor. Therefore the linear operator $G$ can be expressed as:

$
  u[k,j+1] = G u[k,j] = sum_(m = -l)^n a_m u[k+m,j]
$

$
  (hat(u)[k,j+1]) = hat(G) (hat(u)[k,j]) = sum_(m = -l)^n a_k e^(i m omega) (hat(u)[k,j])
$

By Parseval equality, we only need to care about the operator in transformed domain:

$
  norm(u[k,j+1])^2 & = norm(hat(u)[k,j+1])^2 \
                   & = integral_(-pi)^pi abs(hat(G)(omega))^2 abs(hat(u)[k,j])^2(omega) d omega \
                   & <= max_(omega) abs(hat(G)(omega))^2 norm(u[k,j])
$

Thus a sufficient condition for stability of a operator $G$ must be:

$
  norm(hat(G))_(infinity) < 1
$

Suppose a backward Euler method for heat equation without potential:

$
  1/h_t (u[k,j+1] - u[k,j]) = 1/h_x^2 (u[k+1,j+1] - 2 u[k,j+1] + u[k-1,j+1]) \
$

$
  alpha := h_t/h_x^2
$

Every differential operator reduce to a linear combination:

$
             u[k,j+1] - alpha (u[k+1,j+1] - 2 u[k,j+1] + u[k-1,j+1])) & = u[k,j] \
  hat(u)[k,j+1] - alpha (e^(i omega) - 2 + e^(-i omega))hat(u)[k,j+1] & = hat(u)[k,j] \
                            hat(u)[k,j+1](1 + 4 alpha sin^2(omega/2)) & = hat(u)[k,j]
$

It's demonstrated that backward Euler method have no sufficient condition for stability, but it doesn't mean it has no *such condition*.

$
  hat(G)_(B E)(omega) = 1/(1 + 4 alpha sin^2(omega/2))
$

Thus backward operator has no conditional stability. Readily, one can prove that for forward operator:

$
  hat(G)_(F E)(omega) = 1 - 4alpha sin^2 (omega/2) <= 1 => h_t/h_x^2 <= 1/2 \
$

== Energy/Entropy method

We notice that the action of $G$ is a convex combination of $u[k-1,j],u[k,j],u[k+1,j]$, provided:

$
  0 < h_t/h_x^2 <= 1/2
$

$
  min { u[k-1,j], u[k,j], u[k+1,j]} <= u[k,j+1] <= max {...}
$

Which leads to:

$
  & min_k u[k,j+1] >= min_k u[k,j] \
  & max_k u[k,j+1] <= max_k u[k,j] \
$

$
  max_k abs(u[k,j+1]) <= max_k u[k,j]
$

For this reason, $G$ is stable in $norm(dot)_infinity.$ Given any convex combination of $u[k,j]$, with convex function $eta(dot)$, we can extend:

$
  eta(u[k,j+1]) <= alpha eta(u[k-1,j]) + beta eta(u[k,j]) + gamma eta(u[k+1,j]) \ alpha + beta + gamma = 1
$

Summing over $k$, we deduce:

$
  sum_k eta(u[k,j+1]) <= sum_k eta(u[k,j])
$

The convex function is called _entropy_ in this setting. The above inequality means the _entropy_ decreasing in time. Various convex functions can apply:

- $eta (u) = u^2 => norm(u[k,j+1])^2_2 <= norm(u[k,j])^2_2$
- $eta (u) = u^p, 1<=p<=infinity$ results:

$
  norm(u[k,j+1])^2_p <= norm(u[k,j])^2_p
$

Is the general $L^p$ stability indicating $norm(G)_p <= 1$.

= PesudoSpectral Methods

To integrate a function, it's impossible to continuously achieve such while we have to discretize all data set. This force one to
interpolate a certain data set as ${(x_i,f(x_i)}_(i=1)^N$. To decompose problems, one can regard data set as a combination of delta functions.

$
  {(x_i,f(x_i))} => {(x_i, f(x) delta(x - x_i))} => f(x){(x_i, delta(x - x_i))}
$

It allows us to analyze the function which must be a basis combination sharing the same property with delta function.

$
  delta(x - x_i) ~> l_i (x) "s.t." l_i (x_j) = delta_(i j)
$

A function therefore can be approximated:

$
  f(x) approx sum_(i=1)^N f(x_i) l_i (x) \
  l_i (x_j) = delta_(i j)
$

As for the integral of a function, it also must be the integral of each basis.

$
  I[f] := integral_a^b f(x) d x approx integral_a^b p(x) d x = integral sum_(i=0)^N f(x_i) l_i (x) d x = sum_(i=0)^N w_i f(x_i) \
  w_i = integral_a^b l_i (x) d x
$

We call $w_i$ as weight of basis. Suppose one want to interpolate a certain function by $n$-degree polynomials as basis, then the basis itself must be exactly match our interpolation.

$
  integral_a^b sum_(i=0)^n a_i x^i d x = sum_(i=0)^n a_i (b^(i+1) - a^(i+1))/((i+1)!)
$

Interpolating itself suggests that weights must be a linear combination of the integral of itself.

$
  I_n [sum_(i=0)^n a_i x^i] = sum_(j=0)^n w_j (sum_(i=0)^n a_i x_j^i) = sum_(j=0)^n (w_j x_j^i) sum_(i=0)^n a_i
$

$
  sum_(j=0)^n w_j x^i_j = (b^(i+1) - a^(i+1))/((i+1)!) quad forall i in {1,...,n}
$

As a results, one should solve such _Vandermonde_ matrix.

$
  vf(V)^T vf(w) = vf(b), thick b_i = integral_a^b x^i d x
$

In essence, a weight must be a linear combination of $x^i$.

$
  w_i = integral_a^b l_i (x) d x =>^("polynomial") w_i = sum_(j=0)^n a_(i j) integral_a^b x^j d x
$

$
  vf(w) = vf(A) vf(b)
$

If $vf(A) = vf(V)^(-1)^T$, one finds the same weights produced by interpolating polynomial exactly. However, polynomials in evenly spaced grid isn't well-behaved in many conditions. Recall that Runge's function $f(x) = 1/(1+x^2)$ in uniformly spaced points interpolation fails to uniformly converge to itself in the defect of boundary divergence. A expedience is _Clenshaw-Curtis_ quadrature:

$
  x_j = cos ((j pi)/n) in [-pi,pi], quad j= 0,...,n
$

Such spaced points distributes tensely on the boundaries while sparely on the middle. Nonetheless, such interpolation is not satisfied which leading to _Gaussian Quadrature_.

== Gaussian Quadrature

A approximation of function is a linear combination of basis functions.

$
  & f_n (x) = sum_(j=1)^n f(x_j) l_j (x) \
  & f (x) = sum_(j>=1) f (x_j) l_j (x)
$

A insight is that we have maximally $2n$ unknown variables containing $n$ grid $x_j$ and $n$ weights $w_j$. Hence we can approximate a $2n$ polynomial *exactly*.

$
  I_n [f] = integral_I f(x) d x = sum_(j=0)^n f(x_j) integral_I l_j (x) d x = sum_(j=0)^n f(x_j) w_j
$

To adapt general space, we introduce a weight function for various possible basis.

$
  I_n [f] = integral_a^b f(x) w(x) d x = sum_(j=0)^n f(x_j) integral_a^b l_j (x) w (x) d x = sum_(j=0)^n f(x_j) w_j
$

$
  w_j := integral_a^b l_j (x) w(x) d x
$

First, we adapt basis itself, which shows the common property of basis.

$
  I_n [l_j] = integral_a^b l_j (x) w (x) & = sum_(k=0)^n l_j (x_k) integral_a^b l_k (x) w(x) d x \
                                         & => l_k (x_j) = delta_(k j)
$

A intriguing phenomena is that we plugin two basis into the integration, where $j,k < n => j+k < 2n$ must be exactly integrated:

$
  I_n [l_j l_k] = integral_a^b l_j (x) l_k (x) w(x) d x & = sum_(l=0)^n l_j (x_l) l_k (x_l) integral_a^b l_l (x) w(x) d x \
                  integral_a^b l_j (x) l_k (x) w(x) d x & = sum_(l=0)^n l_j (x_l) l_k (x_l) w_l = delta_(j k) w_j
$

It follows that basis is _orthogonal_ to each other. Consequently, a basis must be a linear combination of _orthogonal polynomials_. One plugin the orthogonal polynomials in with suitable degree less than $n$.

$
  I_n [p_(n-1) p_(m-1)] = integral_I p_(n-1) p_(m-1) w d x = sum_(l=0)^n p_(n-1) (x_l) p_(m-1) (x_l) w_j = delta_(n m)
$

Now, here the crucial point. The orthogonal polynomials can be necessarily expanded into a delta function which is also a *linear combination* of itself.

$
  p_(m-1) (x) = sum_(k=1)^n p_(k-1) (x) delta_(k n) &= sum_(k=1)^n p_(k-1) (x) sum_(l=1)^n p_(k-1) (x_l) p_(m-1) (x_l) w_l \
  &= sum_(l=1)^n p_(m-1)(x_l) sum_(k=1)^n p_(k-1) (x) p_(k-1) (x_l) w_l \
  &= sum_(l=1)^n p_(m-1) (x_l) I_l (x)
$

Consequently, a basis is represented below:

$
  l_i (x) = w_i sum_(k=1)^n p_(k-1) (x) p_(k-1) (x_i)
$

Although we still don't know the property of $x_j$ and $w_j$. It pushes us to evaluate orthogonal polynomials. A essential property is orthogonal polynomial must be orthogonal to any polynomials with degree smaller than itself.

$
  innerproduct(x p_n (x), p_k (x)) = innerproduct(p_n (x), x p_k (x)) = 0 => k + 1 < n
$

It means, $x p_n (x)$ should be a linear combination of only $n+1, n, n-1$-degree.

$
  & x p_n (x) = A_n p_(n+1) + B_n p_n + C_(n) p_(n-1) \
  & x p_(n+1) (x) = A_(n+1) p_(n+2) + B_(n+1) p_(n+1) + C_(n+1) p_(n)
$

It can be verified that $C_(n+1) = A_n$:

$
  C_(n+1) = innerproduct(x p_(n+1), p_n) = innerproduct(p_(n+1), x p_n) = A_n
$

$
  & x p_n (x) = C_(n+1) p_(n+1) + B_n p_n + C_n p_(n-1) \
$

For basis $l_(n+1)$, the terms $sum_n p_n (x) p_n (x_i)$ is the key, motivating us to collects terms resemble to it.

$
  & x p_n (x) p_n (y) = C_(n+1) p_(n+1) (x) p_(n) (y) + B_n p_n (x) p_n (y) + C_n p_(n-1) (x) p_n (y) \
  & y p_n (x) p_n (y) = C_(n+1) p_(n) (x) p_(n+1) (y) + B_n p_n (x) p_n (y) + C_n p_(n) (x) p_(n-1) (y)
$

Subtract above two terms:

$
  (x-y) p_n (x) p_n (y) = & C_(n+1) (p_(n+1) (x) p_(n) (y) - p_n (x) p_(n+1) (y) ) \
                          & - C_n (p_n (x) p_(n-1) (y) - p_(n-1) (x) p_n (y))
$

We define $K_n (x,y)$ to simplify the notation:

$
  & K_n (x,y) = p_(n+1) (x) p_n (y) - p_(n) (x) p_(n+1) (y) \
  & K_(-1) (x,y) = 0 - 0 = 0
$

Summation of terms yields another expression of basis:

$
  sum_(i=0)^n (x-y) p_i (x) p_i (y) & = sum_(i=0)^n (C_(n+1) K_n - C_n K_(n-1)) \
                                    & = sum_(i=0)^n C_(n+1) K_n - sum_(i=0)^(n-1) C_(n+1) K_n - K_(-1) \
                                    & = C_(n+1) K_n
$

$
  sum_(i=0)^n p_i (x) p_i (y) = (C_(n+1) K_n)/(x-y)
$

To acquire the meaning of $x_j$, we use the fresh expression:

$
  delta_(j k) = l_k (x_j) & = w_j sum_(i=0)^(n-1) p_i (x_j) p_i (x_k) \
                          & = w_j C_(n+1) (K_(n-1) (x_j, x_k))/(x_j-x_k) \
                          & = w_j C_(n+1) (p_(n) (x_j) p_(n-1) (x_k) - p_(n-1) (x_j) p_n (x_k) )/(x_j-x_k)
$

To force zero if $j!=k$, we must have:

$
        p_n (x_j) p_(n-1) (x_k) & = p_(n-1) (x_j) p_n (x_k) \
  (p_(n) (x_j))/(p_(n-1) (x_j)) & = (p_n (x_k))/(p_(n-1) (x_k)) =^? 0
$

Indeed, it's impossible unless we choose $x_j$, $x_k$ both the roots of $p_n$ or $p_(n-1)$ orthogonal polynomials. To investigate the roots coincidence, we treating $x_k$ as constant while manipulating $x_j$ as variables:

$
  lim_(x_j -> x_k) "LHS" & = (dv(, x_j) (p_(n) (x_j) p_(n-1) (x_k) - p_(n-1) (x_j) p_n (x_k) ))/(dv(, x_j) (x_j - x_k)) \
                         & = p'_n (x_j) p_(n-1) (x_j) - p'_(n-1) (x_j) p_n (x_j) = 1/(w_j C_(n+1))
$

For choice of roots, we follow the sign matter, choosing $x_j = x_k$ is the roots of $p_n$ orthogonal polynomial. Derives the final expression of weight:

$
  w_j = 1/(C_(n+1) p'_n (x_j) p_(n-1) (x_j))
$

$
  l_k (x) = w_j C_(n+1) (p_n (x) p_(n-1) (x_k))/(x - x_k)
$

A immediate consequence is any $x_j$ will be the zeros of $p_n (x)$ for a certain basis set ${l_i}_(i=1)^n$. Take the weight into the basis expression:

$
  l_k (x_k) = (p_n (x) p_(n-1)(x_k))/(p'_n (x_k) p_(n-1) (x_k) (x-x_k)) = (p_n (x))/(p'_n (x_k) (x-x_k))
$

We recover $l_k$ as the Lagrange basis in polynomial $p_n$, by removing the $x_k$ zero. It shown that, given any orthogonal polynomials set, one only needs to compute the set of zeros and differentiations of polynomials at zeros which is pretty easy for nowadays computer.

Another choice of basis comes from _Shannon_ and _Whittaker_@lo_pseudospectral_nodate[p~13]. We only needs two property to define the basis by zeros and orthogonality. It suggests that the orthogonality can be derived from Fourier analysis.

$
  sinc (x) = (sin (pi x))/(pi x)
$

The integral form of the $sinc$ function is depicted by characteristic function:

$
  sinc (x) = 1/(2pi) integral_(-pi)^pi e^(- i omega x) d x = hat(chi)_[-pi,pi]
$

$
  chi_[a,b] (omega) = cases(1 quad "if" -pi <= omega <= pi, 0 quad "otherwise")
$

It shown that orthogonality inherits from characteristic function by $chi_[-pi + n pi, pi+ n pi] dot chi_[-pi + m pi, pi + m pi] = 0$:

$
  integral_(-infinity)^(infinity) sinc(x - m) sinc(x - n) d x = 1/(2pi) integral_(-pi)^(pi) e^(i (n - m) omega) d omega = delta_(n m)
$

So the only left part is zeros property, which must be $x = j, j in bb(Z)$.

$
  l_j (x) = sinc((x-x_j)/h) quad x_j = x_0 + j delta x = x_0 + j h_x
$

$
  l_j (x_i) = cases(
    1 quad "if" x_i = x_j,
    sin (pi (i - j)) = 0 quad "if" x_i != x_j
  )
$

$
  integral_(-infinity)^(infinity) l_i (x) l_j (x) d x = h delta_(i j)
$

In which, we constructs the basis entirely.

== Application as Spectral Decomposition

Based on previous achievements, we can finally turn into the construction of _pesudospectral_ methods. The key is not to find the spectral basis of certain linear operator, but to approximate the answer by predefined basis in Gaussian quadrature.

$
  1/(sqrt(w_i)) integral_I sqrt(w(x)) l_i (x) sqrt(w(x)) l_j (x) d x = delta_(i j) \
$

Define the basis function as:

$
  sqrt((w (x))/(w_i)) l_i (x) = phi.alt_i (x)
$

For the same reason, we omit $w_i$ for simplicity.

Any function defined on the same domain of basis, can be decomposed by basis function with the merits of integration approximation:

$
  psi(x) = sqrt(w(x)) sum_(j>=1) psi(x_j) l_j (x) = sum_(j>=1) psi (x_j) phi.alt_j (x)
$

$
  integral_Omega psi(x)^* psi(x) d x = sum_(j>=1) psi^* (x_j) psi(x_j) integral_Omega phi.alt^*(x) phi.alt (x) d x = sum_(j>=1) psi^2 (x_j)
$

Based on the approximation of basis, the error should be $O(2n)$ order in integration.

A differential equation is usually a form of:

$
  L psi(x) = g(x)
$

Take the product of basis function and integrates in the space:

$
                                  integral_Omega phi.alt_j (x) L psi(x) d x & = integral_Omega phi.alt_j (x) g(x) d x \
  sum_(i>=1) psi(x_j) integral_Omega phi.alt_j (x) L thin phi.alt_i (x) d x & = integral_Omega phi.alt_j (x) g(x) d x \
$

One define the discretization of the equation, simplify the integration problem into a matrix problem.

$
  vf(L) = integral_Omega phi.alt_j L thin phi.alt_i d x, thick vf(g) = integral_Omega phi.alt_j thin g thin d x, thin vf(c) = psi(x_j)
$

The eigenvalue problem follows the same routine:

$
  L psi^m (x) = lambda_m psi^m (x) => vf(L) vf(c)_m = lambda_m vf(c)_m
$

We present the reduction of Schrödinger's equation:

$
  hat(H) psi = - planck^2/(2 mu) pdv(, x, 2) psi + V psi = E psi
$

Next, we can use bracket symbol to formulate the basis that every integration is a summation of basis:

$
  braket(i, n) = sqrt(w_i) l_n (x_i) \
$
$
  ket(i) = ket(n) braket(n, i) = sum_(n>=1) sqrt(w_i) l_n (x_i) ket(n)
$

The orthogonality property is illustrated below:

$
  & braket(j, i) = braket(j, n) braket(n, i) = sum_(n>=1) sqrt(w_i w_j) l_n (x_i) l_n (x_j) = delta_(i j) \
  & braket(n, m) = braket(n, i) braket(i, m) = sum_(i>=1) w_i l_n (x_i) l_m (x_i) = delta_(m n)
$

Potential is a diagonal matrix:

$
  hat(V) ket(j) = V (x_j) ket(j) \
  V_(m n) = braket(i, hat(V), j) = V (x_i) delta_(i j)
$

$
  hat(K) = planck^2/(2 mu) hat(D)^dagger hat(D) \
$

While kinetic is more complex involving the differential of basis@lo_pseudospectral_nodate[p~94]:

$
  K_(i j) = planck^2/(2 mu) braket(i, hat(D)^dagger hat(D), j) = planck^2/(2 mu) braket(i, hat(D)^dagger, k) braket(k, hat(D), j) = planck^2/(2 mu) sum_(k>=1) D_(k i) D_(k j)
$

$
  D_(k i) = braket(k, hat(D), n) braket(n, i) = sqrt(w_k w_i) sum_(n>=1) l'_n (x_k) l_n (x_i)
$

The Hamiltonian is:

$
  H_(i j) = planck^2/(2 mu) sum_(k>=1) D_(k i) D_(k j) + V (x_i) delta_(i j) \
$

= 结论

#end-en

#bibliography("references.bib", title: "参考文献")

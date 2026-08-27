#import "../lib.typ": *
#import "@preview/physica:0.9.8": *
#import "@preview/lovelace:0.3.0": *

#show: mine.with(
  template: "daily-en",
  title: "Computational Physics",
)

= Error

Suppose approximation $Z^*$ for $Z$, define the function _significant figures_ by:

$
  #pseudocode-list[
    + Input: $Z^*$: Number, $Z$: Number
    + aid_bit := if significant_digits($abs(Z-Z^*)$) < 5: 0 else: $-1$
    + return digits($Z^*$) + aid_bit
  ]
$

Suppose $Z = pi = 3.14159dots$, $Z^* = 3.141$:

$
  #pseudocode-list[
    + aid_bit := eval(if significant_digits($0.00059$) < 5: 0 else: $-1$) = -1
    + return eval(digits($3.141$) - 1) = 3
  ]
$

Which is same as $Z^* = 3.14$.

If $Z^* = 3.142$, aid_bit := $0$, therefore return $4$ as results.

= Linear Algebra

== Direct Method

$
  A x = b
$

For $A in bb(R)^(n times n), b in bb(R)^n$. If one transform the system into a equivalent upper-triangular form:

$
  U x = c
$

Where $U$ in upper-triangular, then solve by *back substitution*. Now we represent $A[i,:]$ for rows and $A[:,j]$ for columns. Given combined matrix system:

$
  [A,b] => [U,c]
$

For each $k$ rows, we eliminate each rows below $k$ or $i in {k+1,dots,n}$ row.

$
  U[i,:] & <- A[i,:] - A[i,k]/A[k,k] A[k,:] \
    b[i] & <- b[i] - A[i,k]/A[k,k] b[k]
$

Forward Elimination:
$
  #pseudocode-list[
    + Input: $A$: Matrix$(n,n)$, $b$: Vector($n$)
    + $U := A$
    + $c := b$
    + for $k$ in $[1 dots n-1]$:
      + for $i$ in $[k+1 dots n]$:
        + $m := A[i,k]\/A[k,k]$
        + $U[i,:] <- A[i,:] - m dot A[k,:]$
        + $c[i] <- b[i] - m dot c[k]$

    + return ($U,c$)
  ]
$

Back substitution:
$
  #pseudocode-list[
    + Input: $U$: upper-triangular Matrix($n,n$), $c$: Vector($n$)
    + $x := c$
    + for $i$ in $[n dots 1]$:
      + $x[i] <- (c[i] - U[i,i+1:n] dot x[i+1:n])\/U[i,i]$

    + return $x$
  ]
$

Such operation can be decomposed to:

$
  E_1 dots.c E_m A & = U \
                 A & = (E_1 dots.c E_m)^(-1) U \
                 A & = L U
$

$
  A[i,:] & = sum_(k=1)^i L[i,k] dot U[k,:] \
$

$
  #pseudocode-list[
    + Input: $T in bb(R)^(n times n)$, $c in bb(R)^n$
      + $L := "zeros"(n,n)$
      + $U := A$
      + $c := b$
      + for $k$ in $[1 dots n-1]$:
        + for $i$ in $[k+1 dots n]$:
          + $m := A[i,k]\/A[k,k]$
          + $L[i,k] <- m$
          + $U[i,:] <- A[i,:] - m dot A[k,:]$
          + $c[i] <- b[i] - m dot c[k]$

      + return ($U,c$)
  ]
$

== Iteration Method

Jacobi iteration method:

$
  b[i] = A[i,:] x[:] & = A[i,:i-1] x[:i-1] + A[i,i] x[i] + A[i,i+1:] x[i+1:] \
$

$
  x[i] = b[i]/A[i,i] - (A[i,:!=i] dot x[:!=i])/A[i,i]
$

$
  x^(\(k+1\))[i] = b[i]/A[i,i] - (A[i,:!=i] dot x^(\(k\))[:!=i])/A[i,i]
$

Given matrix $A$ decomposed into $D,L,U$:

$
  L = mat(0, dots, 0; -a_(21), dots, 0; dots.v, dots.down, dots.v; a_(n 1), dots, 0), quad U = mat(0, -a_(12), dots, -a_(1 n); 0, 0, dots, - a_(2 n); dots.v, dots.v, dots.down, dots.v; 0, 0, dots, 0), quad D = mat(a_11, 0, dots, 0; 0, a_22, dots, 0; dots.v, dots.v, dots.down, dots.v; 0, 0, dots, a_(n n))
$

$
  (D - L - U) dot x & = b \
                D x & = (L+U) x + b \
                  x & = D^(-1) (L + U) x + D^(-1) b \
            x^((k)) & = D^(-1) (L+U) x^((k-1)) + D^(-1) b \
$

We see that if $x^((k+1))[i]$ already known, directly plugin into next $x^((k+1))[k]$ where $k > i$ is totally acceptable and improves the convergence of the algorithm.

$
  x^((k+1))[i] = 1/A[i,i] (b[i] - A[i,:i-1] dot x^((k+1))[:i-1] - A[i,i+1:] dot x^((k))[i+1:])
$

$
  (D - L) x^((k)) & = U x^((k-1)) + b \
          x^((k)) & = (D-L)^(-1) (U x^((k-1)) + b)
$

Generally, all above iteration methods can be expressed as:

$
                      x^((k)) & = T x^((k-1)) + c \
                      x^((k)) & = T^(k) x^((0)) + sum_(i=0)^(k-1) T^i c \
  lim_(k -> infinity) x^((k)) & = lim_(k->infinity) T^(k) x^((0)) + sum_(i=0)^(k-1) T^i c \
$

$
  sigma(T) = {lambda in bb(C): T-lambda I "is not invertible"}
$

$
  sigma(T) subset.eq {lambda in bb(C): abs(lambda) <= norm(T)}
$

Indeed due to:

$
  (T - lambda I)^(-1) = -1/lambda sum_(i=0)^infinity (T/lambda)^n
$

must converge absolutely when $norm(T\/lambda) = norm(T)\/abs(lambda) < 1$, therefore exists. So $abs(lambda) <= norm(T)$ is a necessity for spectrum.

$
  rho(T) = sup{abs(lambda): lambda in sigma(T)}
$

We know that $lim_(k->infinity) T^k$ won't diverge only if $norm(T) < 1$. It's deduced that $lim_(k->infinity) norm(T)^k -> 0 => lim_(k->infinity) T^k -> 0$. We immediately found that:

$
  lim_(k->infinity) x^((k)) = (1-T)^(-1) c
$

If the limit vector exists, following below bound error estimation:

$
  x - x^((k)) & = (T x + c) - (T x^((k-1)) + c) \
              & = T^(k) (x - x^((0))) \
$

$
  norm(x-x^((k))) <= norm(T^k) norm(x-x^((0)))
$

$
  #pseudocode-list[
    + Input: $T in bb(R)^(n times n)$, $c in bb(R)^n$
    + requires: $rho(T) < 1$
    + $x := x_0$
    + $"tol" := "MAX"$
    + while $"tol" > "tol"_0$:
      + $"prev" <- x$
      + $x <- T x + c$
      + $"tol" <- norm(x - "prev")$
    + return $x$
  ]
$

== Problem

=== LU Algorithm

$
  A: mat(2,2,3;4,7,7;-2,4,5), b = vec(3,1,-7) \
$

$
  A = mat(2,2,3;4,7,7;-2,4,5) -> mat(1,0,0;2,1,0;-1,0,1) mat(2,2,3;0,3,1;0,6,8) -> mat(1,0,0;2,1,0;-1,2,1) mat(2,2,3;0,3,1;0,0,6) = L U \
  b = vec(3,1,-7) -> vec(3,-5,-4) -> vec(3,-5,6) 
$ 
  
$ 
  mat(2,2,3;0,3,1;0,0,6) vec(3,-5,6) -> 
  mat(2,2,3;0,3,1;0,0,1) vec(3,-5,1) &-> \
  mat(2,2,3;0,1,0;0,0,1) vec(3,(-5 - 1)\/3=-2,1) &-> 
  mat(1,0,0;0,1,0;0,0,1) vec((3-3+4)\/2=2,-2,1)
$

$
  x = vec(2,-2,1)
$

=== Jacobi Algorithm

$
  A= mat(1,5,-3;5,-2,1;2,1,-5), b = vec(2,4,-11) \
$

Switch pivot:

$
  A' = mat(5,-2,1;1,5,-3;2,1,-5), b' = vec(4,2,-11)
$

$
  &x_1^((k)) = 1/5 (4 + 2 x_2^((k-1)) - x_3^((k))) \
  &x_2^((k)) = 1/5 (2 - x_1^((k-1)) + 3x_3^((k))) \
  &x_1^((k)) = 1/5 (11 + 2 x_1^((k-1)) + x_2^((k))) \
$

= Roots Finding

Bisection finding is based on the function property that $f(a) dot f(b) < 0$ due to intermediate value theorem. To avoid oscillation problem for multiple zeros, we should focus on the interval contains only *single* zero to avoid confusion problem.

Assume $f(x)$ is continuous by default.

$
  #pseudocode-list[
    + Input: $f(x)$: $C^0$, $[a,b] subset bb(R)$
    + requires: $f(a) dot f(b) < 0$, $f([a,b])$ contains *single* root.
    + $"tol" := "MAX"$
    + while $"tol" > "tol"_0$
      + $"mid" = (a+b)\/2$
      + if $f(c) = 0$: return $c$
      + else if $f(a) dot f(c) < 0$: $b <- c$
      + else: $a <- c$
      + $"tol" <- abs(f(c))$
    + return $c$
  ]
$

To estimate the error:

$
  E_n = abs(x - c_n) < L_n & = abs(b_n - a_n) \
$

Suppose $b_n = (a_(n-1) + b_(n-1))\/2$ without losing generality.

$
  L_n = 1/2 abs(b_(n-1) - a_(n-1)) = 1/2 L_(n-1) = (1/2)^(n+1) L_0
$

$
  E_n <= L_0/2^(n+1), E_(n+1) <= L_0/(2^(n+2)) => E_(n+1) <= 1/2 E_n
$

Suppose the toleration is $epsilon$, we want $abs(x-c_n) < epsilon$

$
  abs(x-c_n) < L_n & < epsilon \
   (1/2)^(n+1) L_0 & < epsilon \
                 n & > log_2 (L_0/epsilon) - 1
$

The convergence speed can be estimated by:

$
  abs(E_(n+1)) <= C abs(E_n)^k => k "is convergence ratio"
$

It suggests that bisection is linear convergence comparing to above deduction.

Newton-Raphson method uses tangent lines to approximate roots, starting from an initial guess.

$
  y = f(x) approx f(x_0) + f'(x_0) (x-x_0)
$

$
  0 & = f(x_0) + f'(x_0) (x - x_0) \
  x & = x_0 - f(x_0)/(f'(x_0))
$

Now $x => x_(n+1), x_0 => x_n$:

$
  x_(n+1) = x_n - f(x_n)/(f'(x_n))
$

It suggests that if the tangent line is far from the expected zero, the linearization may not work and cause oscillation or divergence problem.

Impose the *sufficient close* condition for interval $[a,b]$ s.t.:

- $f'(x) != 0$ for $x in [a,b]$
- $f''(x) approx c$ or $f$ is approximately quadratic.
- No other roots for confusion problem.

$
  #pseudocode-list[
    + Input: $f(x)$: $C^1$, $x_0 in bb(R)$
    + requires: $x_0 in [a,b]$ is sufficient close to single zero of $f(x)$
    + $x := x_0$
    + $f' := f'$ (given by manual calculation or symbol calculation)
    + $"tol" := "MAX"$
    + while $"tol" > "tol"_0$
      + $x <- x - f(x)\/f'(x)$
      + $"tol" <- abs(f(x))$
    + return $x$
  ]
$

To estimate the error, we expand one more terms:

$
  0 = f(alpha) & = f(x_n) + f'(x_n) (alpha - x_n) + 1/2 f''(xi_n) (alpha - x_n)^2 \
               & = f(x_n)/(f'(x_n)) - x_n + alpha + 1/2 (f''(xi_n))/(f'(x_n))(alpha-x_n)^2 \
$

$
  x_(n+1) - alpha & = 1/2 (f''(xi_n))/(f'(x_n)) (alpha - x_n)^2 \
          E_(n+1) & = 1/2 (f''(xi_n))/(f'(x_n)) E_n^2
$

If a root has multiplicity $m > 1$, or $f(alpha) = f'(alpha) = dots.c = f^((m-1)) (alpha) = 0, f^((m)) (alpha) != 0$.

Generally, for $abs(E_(n+1)) = C abs(E_n)^(p)$, with a tolerance $epsilon$, one has:

$
  abs(E_(n)) = C abs(E_(n-1))^p = C dot C^p abs(E_(n-2))^(p^2) = dots.c
$

$
  sum_(i=1)^n p^i = (p^n - 1)/(p - 1)
$

If $p = 1$, then:

$
  lim_(p->1) (p^n-1)/(p-1) -> n
$

$
  abs(E_n) = C^((p^n - 1)/(p-1)) abs(E_0)^(p^n) & < epsilon \
         (p^n - 1)/(p-1) ln C + p^n ln abs(E_0) & < epsilon \
                            p^n (ln C abs(E_0)) & lt.tilde ln epsilon \
$

Since $C abs(E_0) < 1$ for most case:

$
  n & gt.tilde log_p (ln 1/epsilon)/(ln (1/(C abs(E_0))))
$

If $p=1$, choose $log_(p->1)(x) = 1(x)$.

Now $C < 1$ is necessary for convergence:

$
  C^n < epsilon/abs(E_0) \
  n > log_(1\/C) (abs(E_0)/epsilon)
$

= Function Approximation

== Fitting

We want to find a polynomials that minimize the square error:

$
  (integral_a^b (f(x) - P_* (x))^2 d x)^(1/2) & = min_(p in cal(P)_n) (integral_a^b (f(x) - p (x))^2 d x)^(1/2) \
                              norm(f - P_*)_2 & = min_(p in cal(P)_n) norm(f - p)_2
$

Suppose polynomials of form $p = c_0 + c_1 x$:

$
  E(c_0,c_1) & := norm(f(x) - (c_0 + c_1 x))_2 \
             & = integral_a^b (f(x) - c_0 - c_1 x)^2 d x \
             & = integral_a^b f(x)^2 d x - 2 c_0 integral_a^b f(x) d x \
             & quad quad quad -2c_1 integral_a^b x f(x) d x + c_0^2 (b-a) + c_0 c_1 (b^2 -a^2) + 1/3c_1^2 (b^3 - a^3)
$

$
  pdv(E, c_0) = pdv(E, c_1) = 0 \
$

$
  & pdv(E, c_0) = - 2 integral_a^b f(x) d x + 2 c_0 (b-a) + c_1 (b^2 - a^2) \
  & pdv(E, c_1) = -2 integral_a^b x f(x) d x + c_0 (b^2 - a^2) + c_1 2/3 (b^3 - a^3)
$

Setting basis with $c_0, c_1$ forming a $A x = b$ problem:

$
  mat(2(b-a), b^2 - a^2; b^2-a^2, 2/3 (b^3-a^3)) vec(c_0, c_1) = vec(2 integral_a^b f(x) d x, 2integral_a^b x f(x) d x)
$

A better function fitting is to use basis function:

$
  braket(f, psi_i) = c_j braket(psi_j, psi_i)
$

Which given any innerproduct of $braket(psi_j, psi_i)$, we can deduce the coefficients.

The more practical case is for data fitting:

$
  E(c_0,c_1) = sum_(i=1)^n (y_i - (c_0 + c_1 x_i))^2 \
$

$
  pdv(E, c_0) = - 2 sum_(i=1)^n (y_i - (c_0 + c_1 x_i)) \
  pdv(E, c_1) = - 2 sum_(i=1)^n x_i (y_i - (c_0 + c_1 x_i)) \
$

$
  c_0 n + c_1 sum_(i=1)^n x_i = sum_(i=1)^n y_i \
  c_0 sum_(i=1)^n x_i + c_1 sum_(i=1)^n x_i^2 = sum_(i=1)^n x_i y_i
$

A coincidence is therefore to solve such overdetermined $A x = b$ problem. To find the minimal of overdetermined equations, we use it too:

$
  E(x_i) = norm(A x - b)^2 = (A x - b)^T (A x - b) \
$

We pose such matrix and vector differential:

- If $f: bb(R)^n -> bb(R)^m$, then $nabla f$ is a $m times n$ matrix based on the basis mapping.
- Then: $f: bb(R)^n -> bb(R)$ is a $n times 1$ columns vector.

$
  pdv(a^T x, x) = (pdv(a_1 x_1 + dots, x_1), dots.c, pdv(a_n x_n + dots, x_n)) = x
$

$
  pdv(x^T A x, x) = (pdv(a_(11) x_1 x_1 + a_(12) x_1 x_2 + dots, x_1), dots) = (A + A^T) x
$

$
  pdv(E, x) = 2 (A x - b)^T A => pdv(E, x)^T = 2 A^T (A x - b) \
$

$
  A^T A x = A^T b
$

$
  A = mat(1, x_1; dots.v, dots.v; 1, x_n), quad c = vec(c_0, c_1), quad y = vec(y_1, dots.v, y_n)
$

$
  A^T A = mat(n, sum_(i=1)^n x_i; sum_(i=1)^n x_i, sum_(i=1)^n x_i^2)
$

Which yields same results:

$
  mat(n, sum_(i=1)^n x_i; sum_(i=1)^n x_i, sum_(i=1)^n x_i^2)
  vec(c_0, c_1) =
  vec(sum_(i=1)^n y_i, sum_(i=1)^n x_i y_i)
$

The solution is easy to compute that:

$
  (A^T A)^(-1) = 1/(n sum_i x_i^2 - (sum_i x_i)^2) mat(sum_i x_i^2, -sum_i x_i; -sum_i x_i, n)
$

== Interpolation

If we pose, not overdetermined, but exactly determine it by $p = sum_(i=1)^n c_i x^i$. Then it's a polynomials interpolation. Due to Runge's phenomena, use basis ${x^i}$ seems not a wise choice.

We conclude the properties of interpolation function:

$
  s(x_i) = y_i \
$

=== Newton Basis

Suppose $p_n (x) = p_(n-1)(x) + c_n q_n (x)$ for additional polynomials. Based on the properties, $p_n (x_(i < n)) = y_(i < n) = p_(i < n) (x_(i < n))$, which indicates $c_n q_n (x_(i<n)) = 0$. Pick the non-trivial case, $q_n (x_(i<n)) = 0$. Then, $q_n prop product_(i=1)^(n-1) (x - x_i)$.

$ p_n (x_n) = p_(n-1) (x_n) + c_n q_n (x_n) = y_n => c_n = (y_n - p_(n-1)(x_n))/(q_n (x_n)) $,

Without losing generality, impose $p_n = product_(i=1)^(n-1) (x-x_i)$, such interpolation function can be solved by forward substitution.

$
  mat(1, dots, dots, 0; 1, (x_1 - x_0), dots, 0; 1, (x_2 - x_0), dots, 0; dots.v, dots.v, dots.down, 0; 1, (x_n -x_0), dots, product_(i=0)^(n-1)(x_n - x_i)) vec(c_0, dots.v, dots.v, c_n) = vec(f(x_0), dots.v, dots.v, f(x_n))
$

$
  p_n (x) = sum_(j=0)^n c_j q_j (x)
$

=== Lagrange Basis

Such interpolating matrix can be diagonal by forcing $s_i (x_j) = delta_(i j)$ for each node basis $s_i$. Such node is immediate if zeros constraint is imposed.

$
  l_j (x) = product_(i!=j)^n (x - x_i)
$

However, $s_i (x_i) = 1$ suggests that:

$
  l_j (x) = product_(i!=j)^n (x-x_i)/(x_j - x_k)
$

$
  p_n (x) = sum_(k=0)^n y_k l_k (x)
$

=== Error

For any point $hat(x) in.not {x_i}$, the error $E(hat(x)) = f(hat(x)) - p(hat(x))$ is the explicit error. By interpolation, we can add a polynomial $w(x)$ s.t. $w(x_i) = 0$ to avoid any additional error beside $hat(x)$, then select a carefully toned $lambda$, $f(hat(x)) - (p(hat(x)) + lambda w(hat(x))) = 0$ should be possible.


Select $w(x) = product_(i=1)^n (x-x_i)$ is acceptable. Forcing $phi.alt(hat(x)) = f(hat(x)) - (p(hat(x)) + lambda w(hat(x))) = 0$.

$
  lambda = (f(hat(x)) - p (hat(x)))/(w(hat(x)))
$

Expanding $f(hat(x)) = sum_(i=0)^n f^((i))(x_0) (hat(x) - x_0)^i$, but wait, which local point?

$
  phi.alt(x) = f(x) - p(x) + lambda w(x) "contains" n+1 "zeros" \ => phi.alt^((n))(x) = f^((n))(x) - (p^((n)) (x) + lambda w^((n)) (x)) = f^((n)) (x) - lambda (n)! "contains" 1 "zero" \
$

Due to _Mean Value Theorem_.

$
  phi.alt^((n)) (xi) = 0 = f^((n)) (xi) - lambda (n)!
$

Finally:

$
  E = lambda w(x) = (f^((n))(xi))/n! product_(i=1)^n (hat(x) - x_i)
$

==== Problem

Give a fit curve for a actual $x^2$ function by Newton's interpolation and Lagrange's interpolation:
$
  (x_i,f_i) = {(1,1),(2,4),(4,16)}
$

$
  f_1 (x) = f(x_0) + f[x_0,x_1](x-x_0) = 1 + (4-1)/(2-1) (x-1) = 1 + 3(x-1) = 3 x - 2
$

$
  f_2 (x) &= f_1 (x) + (y_2-f_1(x_2))/((x_2 - x_0)(x_2 - x_1)) (x - x_0)(x-x_1) \
  &= f_1 (x) + (16 - 10)/(3 dot 2) (x - 1) (x-2) \
  &= f_1 (x) + (x-1) (x-2) \
  &= 3 x - 2 + x^2 - 3 x + 2 = x^2
$

Is what we expected.

$
  &l_(0,2) = ((x-2)(x-4))/((1-2)(1-4))  = 1/3 (x-2)(x-4) \
  &l_(1,2) = ((x-1)(x-4))/((2-1)(2-4)) = -1/2 (x-1)(x-4) \
  &l_(2,2) = ((x-1)(x-2))/((4-1)(4-2)) = 1/6 (x-1)(x-2) \
$

$
  f(x) &= l_(0,2) + 4 l_(1,2) + 16 l_(2,2) \
  &= 1/3 (x^2-6x+8) -2(x^2 - 5 x + 4) + 8/3(x^2 - 3 x + 2) \
  &= x^2 + (-2 + 19 -8) x + (8/3 - 8 + 16/3) = x^2
$

Is what we expected.

Now we estimate error:

$
  abs(E(x)) = (f^((3)))/(3!)(x(x-1)(x-2))
$

=== Splines

Another choice is to abandon the whole function in $[a,b]$, rather build a function by each data section $[x_i, x_(i+1)]$ using low-degree polynomials. The most often choice is _Cubic Splines_ with set $s_j (x)$ where $j in {1,dots,n}$ for ${x_i}$ where $i in {0,dots,n}$.

- $s_j (x_j) = f(x_j) quad j = 1,dots,n$
- $s_j (x_(j-1)) = f(x_(j-1)) quad j = 1,dots,n$
- $s'_j (x_j) = s'_(j+1) (x_j) quad j = 1,dots,n-1$
- $s''_j (x_j) = s''_(j+1) (x_j) quad j = 1,dots,n-1$

All sets of cubic polynomials contains totally $4 dot n$ unknowns. The requirements only contains: $n + n + (n-1) + (n-1) = 4n-2$ constraints. So canonical ways to define for left two constraints are:

- $S''(x_0) = S''(x_n) = 0$
- Specify concrete value: $S(x_0)$ and $S(x_n)$
- $S'''(x_1)$ and $S'''(x_(n-1))$ must be continuous

$
  [x_0]f := f(x_0)
$

$
  [x_0,dots,x_k]f := ([x_1,dots,x_k]f - [x_0,dots,x_(k-1)]f)/(x_k - x_0)
$

$
  underbrace([x_0,dots,x_0], k)f := lim_(h->0) (overbrace([x_0,dots,x_0], k-1)f - overbrace([x_0,dots,x_0], k-1)f)/(h)
$

Notice that given $k$ points, one *uniquely* determine a $k-1$-degree polynomials. No matter the choice of Lagrange or Newton's one. So the definition by dividing a polynomials can get its leading coefficient. It's applicable to achieve so by inspecting in Newtons form that only the one with highest-degree $product_(i=0)^(k-1) (x - x_i)$ can survive. Then we reveal another definition that it's the _leading coefficient of the $k-1$-degree interpolation polynomial_ for $k$-divided difference. Choose Lagrange's basis:

$
  p(x) = sum_(i=0)^k f(x_i) l_i (x) quad l_i (x) = product_(j!=i)^k (x-x_j)/(x_i - x_j)
$

Notice that $product_(j=0,j!=i)^k (x-x_j)$ is $k$-degree, so for $k+1$-divided difference:

$
  [x_0,dots,x_k]f = sum_(i=0)^k f(x_i)/(product_(j!=i) (x_i-x_j))
$

Explicitly evaluate Newton's basis, the leading coefficient must be $omega_k (x) = c_(k) product_(i=0)^(k) (x - x_i)$. So $c_(k) = [x_0,dots,x_k]f$. Plus, it's known that $p_(n+1) (x) = p_n (x) + omega_(n+1) (x)$, so by deduction, each coefficient must also be $c_i = [x_0,dots,x_i]f$. The formal expression is:

$
  p_k (x) = sum_(i=0)^k c_i omega_i (x) = sum_(i=0)^k [x_0,dots,x_i] f dot omega_i (x)
$

$
                 f(x) & = sum_(i=0)^k [x_0,dots,x_i]f dot omega_i (x) \
            f(x) g(x) & = sum_(i=0)^k [x_0,dots,x_i]f dot omega_i (x) g(x) \
  [x_0,dots,x_k](f g) & = sum_(i=0)^k [x_0,dots,x_i] f dot [x_0,dots,x_k] (omega_i g)
$

Due to $omega_i = product_(l=0)^(i) (x-x_l)$, The leading coefficient of $omega_i g$ can be shift from $[x_0,dots,x_k]$ to $[x_i,dots,x_k]$.

$
  [x_0,dots,x_k](f g) & = sum_(i=0)^k [x_0,dots,x_i] f dot [x_i,dots,x_k] g
$

We back to our construction of $S(x)$ by another view:

$
  S(x) = cases(p^1 (x) quad x in [t_0,t_1], p^2 (x) quad x in [t_1,t_2], quad dots.v, p^n (x) quad x in [t_(n-1),t_n])
$

Where $S(x)$ is the spline polynomials equipped with $d$-degree piecewise polynomials. The insightful view is to represent the function in _truncation polynomial_.

$
  p^i (x) - p^(i-1) (x) = c_n (x - t_(i))^d
$

The smooth constraint for each polynomials must be very specific with a difference in $d$-degree differential at the endpoint $t_i$. But such difference only exist if $x > t_i$. Then we restrict a _truncation_ by $f_+ (x-c)$ where $x -c > 0$. For $c_n (x-t_i)^d$, it's $x - t_i > 0$.

Therefore any spline function can be represented by a function set: ${c_i (x-t_i)^d}, thick i in {0,dots,k}$.

$
  S(x) = sum_(i=0)^d c_i (x-t_i)_+^i
$

Now $S(x)$ should satisfy support constraint that $S(x)$ must be zero when $x > t_i, thick forall t_i.$

$
  S(x > {t_i}) = sum_(i=0)^d c_i (x-t_i)^i = 0 => sum_(i=0)^k c_i t_i^r = 0 quad "for" r = 0,dots,d
$

Since $f(t) = t^r$ is *already* a interpolation polynomial itself:

$
  [t_0,dots,t_(d)] t^r = sum_(i=0)^(d) 1/(product_(k!=i)(t_i - t_k)) t_i^r = a sum_(i=0)^(d) c_i t_i^r = 0 \
  [t_0,dots,t_(d)] (x-t)^r = a sum_(i=0)^(d) c_i (x - t_i)^r = 0
$

Where $a$ is unknown arbitrary constant. Due to leading coefficient for $r < d + 1$ is zero. Comparing both equation yields:

$
  S(x) = sum_(i=0)^(d) c_i (x-t_i)_+^d = a [t_0,dots,t_(d+1)] (x-t)_+^d
$

The new function, in general restriction to $d$-degree with smoothness and support property, called _B-spline_ basis $B_(i,d) = a [t_i,dots,t_(i+d+1)] (x-t)_+^d$.

The rest problem is to choose a suitable constant for normalization. Suppose $0$-degree:

$
  B_(i,0) = a [t_0, t_1] dot 1_+ = a 1_(x > t_0)/(t_0 - t_1) + a 1_(x > t_1)/(t_1 - t_0) = a(1_(x>t_0) - 1_(x>t_1))/(t_1 - t_0)
$

It's simple to see $1_(x>t_0) - 1_(x>t_1) = 1_([t_0,t_1])$. So a normalization choice is $a = (t_1 - t_0)$. Generally, $a = t_(i+d+1) - t_i$ by induction of divided difference.

Every spline function can be expressed as:

$
  S(x) = sum_(i=0)^n c_i B_(i,3) (x)
$

So $n+d-1$ basis functions is necessary because each basis can only be derived from $i -> i+d+1$.

$
  S(x_j) = sum_(i=0)^n c_i B_(i,3) (x_j) = y_j
$

Each node ${t_i}$ must be covered by any possible support. It shows that if we only cover by $B_(d,i)$ is not enough. To extend the support as slide window for each node such that $B_(d,i-d)$ to $B_(d,i)$ by:

$
  {underbrace(t_0 \, t_0 \, dots,d),t_1,t_2,dots,underbrace(t_n\,t_n\,dots,d)}
$.

$
  B_(i,d) (x) &= (t_(i+d+1) - t_i) [t_i,dots,t_(i+d+1)](x-t)_+^(d-1) (x-t)_+ \
  &= (dots) sum_(j=i)^(i+d+1) [t_i,dots,t_j](x-t)_+^(d-1) [t_j,dots,t_(i+d+1)](x-t)_+ \
  &= (dots) [t_i,dots,t_(i+d+1)](x-t)_+^(d-1) (x - t_(i+ d+1)) + [t_i,dots,t_(i+ d)] (x-t)^(d-1) \
  &= (dots) (x-t_(i+d+1)) ([t_i,dots,t_(i+d)] (x-t)_+^(d-1) - [t_(i+1),dots,t_(i+d+1)](x-t)_+^(d-1))/(t_(i+d+1) - t_i) + (dots) \
  &= (x-t)/(t_(i+d) - t_i) B_(i,d-1) (x) + (t_(i+d+1) - x)/(t_(i+d+1) - t_(i+1)) B_(i+1,d) (x)
$

=== Problem

I will introduce a way simpler for manual work.

Interpolates below data points by quadratic spline:

$
  (x_i,y_i) = {(0,0),(1,1),(2,1),(3,0)} "for" [0,1], [1,2], [2,3]
$

$
  S_i = a_i + b_i x + c_i x^2, quad [x_i,x_(i+1)] "for" 9 "unknowns"
$

However, I will introduce a simpler way to achieve this that, the step polynomial must only occur in $2$-degree due to $C^1$ condition. Therefore whole problem can be reduce to solve:

$
  S(x) = a + b x + c x^2 + alpha_1 (x-1)_+^2 + alpha_2 (x-2)_+^2
$

Only $5$ unknowns!

Interpolation condition:

$
  &S(0) = a = 0 \ 
  &S(1) = a + b + c = b+c = 1 \ 
  &S(2) = a+2b+4c+alpha_1 = 2b+4c+alpha_1 = 1\
  &S(3) = a+3b+9c+4alpha_1 + alpha_2 = 3b+9c+4alpha_1+alpha_2=0
$

We only need to impose one extra condition for boundary condition, due to property of step polynomial, the necessity is only for *left* boundary.
$
  S''(x) = 0 "for" x < 1 => S''(x) = 2 c+2alpha_1 H(x-1) + 2alpha_2 H(x-2) = 0 => c=0
$

From boundary condition:
$
  &(1): b = 1 \
  &(2): alpha_1 = -1 \
  &(3): alpha_2 = 1 \
$

$
  S(x) = cases(
    x quad &x in [0,1],
    x - (x-1)^2 = - x^2 + 3x - 1 quad &x in [1,2],
    x - (x-1)^2 +(x-2)^2 = 3 - x quad &x in [2,3],
  )
$

== Differential

Approximate $f(x)$ by interpolation polynomial $p(x)$ to replace differential by $p'(x)$.

$
  l_(1,0) = (x-x_1)/(x_0 - x_1), quad l_(1,1) (x) = (x-x_0)/(x_1 - x_0) \
$

$
  p_1 (x) = f(x_0) (x-x_1)/(x_0 - x_1) + f(x_1) (x-x_0)/(x_1 - x_0)
$

$
  p'_1 (x) = (f(x_1) - f(x_0))/(x_1 - x_0) = (f(x_0 + h) - f(x_0))/h approx f'(x)
$

$
  f(x) - p_1 (x) &= (f''(xi(x)))/(2!) (x-x_0) (x - x_1) \
  f'(x) - p_1 (x) &= (2x - x_0 - x_1) (f''(xi(x)))/2! + (x-x_0)(x-x_1)((f''(xi(x)))/2!)'
$

When $x = x_0$, the second term vanishes and left:

$
  f'(x_0) - p_1 (x_0) = -h/2 (f''(xi))
$

In general:

$
  f(x) approx p_n (x) = sum_(i=0)^n f(x_i) l_(n,i) (x), quad l_(n,i) (x) = product_(j!=i)^n (x-x_j)/(x_i - x_j) 
$

$
  f'(x) approx p'_n (x) = sum_(i=0)^n f(x_i) l'_(n,i) (x)
$

$
  E(f) = f'(x_j) - p'_n (x_j) = (f^((n+1))(xi))/((n+1)!) product_(k!=j)^n (x_j - x_k)
$

Called $(n+1)$-point formula to approximate $f'(x_j)$.

=== Problem

Using three points ${x_0, x_0 + h, x_0 + 2h}$ derive $3$-point forward difference formula for $x_0$ and determine the order of error.

Evaluate $f'(0)$ for $f(x) = e^x$.

$
  &f(x_0) = f_0 \
  &f(x_0 + h) = f_0 + h f'_0 + h^2/2 f''_0 + h^3/6 f'''_0 + O(h^4) \
  &f(x_0 + 2h) = f_0 + 2h f'_0 + (2h)^2/2 f''_0 + (2h)^3/6 f'''_0 + O(h^4) \ 
$

$
  f'(x_0) approx A f(x_0) + B f(x_0 + h) + C f(x_0 + 2h)
$

$
  &(A + B + C) f_0 = 0 \
  &h(B + 2 C) f'_0 = f'_0 \
  &h^2 (B/2 + 2 C) f''_0 = 0 \
$

Can fully determine the equation, now we normalize that $A_i = A_i\/h$ due to division $h$ coefficient.

$
  &B/2 + 2C = 0 => B = -4C \
  &B + 2 C = 1 => C = -1/2, B = 2 \
  &A + B + C = 0 => A = -3/2 \
$

$
  f'(x_0) = (-3 f(x_0) + 4 f(x_0 + h) - f(x_0 + 2h))/(2 h) + O(h^2)
$

Suppose $h = 0.1$ for $f(x) = e^x$:

$
  f(0) = 1, quad f(0.1) = e^(0.1), quad f(0.2) = e^(0.2)
$

$
  f'(0) = (-3 + 4 e^(0.1) - e^(0.2))/(0.2)
$

== Integration

$
  integral f(x) d x approx integral p_n (x) d x = sum_(i=0)^n integral f(x_i) l_(n,i) (x) d x = sum_(i=0)^n f(x_i) integral l_(n,i) (x) d x 
$

$
  integral f(x) d x = sum_(i=0)^n f(x_i) w_i, quad w_i = integral l_(n,i) (x) d x
$

$
  E(f) = 1/((n+1)!) integral f^((n+1)) (xi(x)) product_(i=0)^n (x-x_i) d x
$

$
  p_1 (x) = f(x_0) (x-x_1)/(x_0 - x_1) + f(x_1) (x-x_0)/(x_1 - x_0)
$

$
  integral^(x_1)_(x_0) (x - x_1)/(x_0 - x_1) d x = lr((x-x_1)^2/(2 (x_0 - x_1)) bar)^(x_1)_(x_0) = - (x_0 - x_1)/2 \
  integral^(x_1)_(x_0) (x - x_0)/(x_1 - x_0) d x = (x_1 <-> x_0) = (x_1 - x_0)/2
$

$
  E_1(f) &= (f''(xi))/2 integral_a^b (x-a)(x-b) d x \
  &= (f''(xi))/2 + lr(x^3/3 - (a+b)x^2/2 + a b x|)^b_a \
$

Take $b = h, a=0$ for simplicity.

$
  integral_0^h x (x-h) d x = lr(x^3/3 - h x^2/2|)^h_0 = - h^3/6 
$

$
  integral f(x) d x =  (x_1-x_0)/2 (f(x_0) + f(x_1)) - (x_1 - x_0)^3/12 f''(xi) = h/2 (dots) - h^3/12 f''(xi)
$

Called _Trapezoidal Rule_.

$
  integral f(x) d x approx h/3 (f(x_0) + 4 f(x_1) + f(x_2)) - h^5/(90) f^((4)) (xi)
$

Or $E = -f^((4)) (xi) (b-a)^5\/2880 $.

Called _Simpson's Rule_.

The degree of precision of a quadrature formula is the largest positive integer $n$ such that the formula is exact for $x^k$, for each $k = 0, 1, dots, n$.

Directly apply $n$-degree integral is not a wise choice for large intervals, because it can be considered as the local expansion of function. High-degree formulas would require more complicated coefficients which is hard to be derived too. Each points can be packed into piecewise function integral approximation called _composite integral_.

$
  integral_a^b f(x) d x &= h/2 (f(a) + f(x_1)) + h/2 (f(x_1) + f(x_2)) + dots \ 
  &= h/2 (f(a) + 2 sum_(i=1)^(n-1) f(x_j) + f(b)) - (b-a)/12 h^2 f''(xi)
$

$
  E(f) = sum_(i=0)^(n-1) - h^3/12 f'''(xi_i) = -h^3/12 sum_(i=0)^(n-1) f'''(xi_i) = -h^3/12 m 1/m (dots) = -(b-a)h^2/12 f'''(xi) \
  1/m sum_(i=0)^(n-1) f''(xi_i) = f'''(xi_i), quad "due to IVP"
$

$
  integral_a^b f(x) d x &= h/3 (f(a) + 4 f(x_1) + f(x_2) + dots) \
  &= h/3 (f(a) +  4 sum_(i=1)^(n/2) f(x_(2 j - 1)) + 2 sum_(i=1)^((n\/2)-1) f(x_(2 j)) + f(b)) - (b-a)/(180) h^4 f^((4)) (xi)
$

$
  E (f) = - sum_(i=0)^(m\/2-1) h^5/90 f^((4)) (xi_i) = - h^5/90 sum_(i=0)^(m\/2-1) f^((4)) (xi_i) = - h^5m/180 2/m (dots) = - (b-a)/180 h^4 f^((4))(xi)
$

Where $h = x_i - x_(i-1)$.

=== Problem

Approximate:

$
  I = integral_0^1 e^x d x
$

Where $abs(E) < 10^(-6)$ by composite Simpson's rule.

$
  E = -h^5/(90) f^((4))(xi)
$

Split $[0,1]$ into $N$ *even* intervals where based on the section counts for each single integration:

$
  h = 1/N, quad M = N/2 => abs(E) <= M dot h^5/90 max(abs(f^((4))(x)))
$

$
  abs(E) <= 1/(2h) dot h^5/90 max(abs(f^((4))(x))) = e/180 h^4 <10^(-6)
$

$
  h^4 < 180/e times 10^(-6) => h < 0.09, thick N > 11.1
$

Choose $N=12$:

$
  integral_a^b e^x d x = sum_(i=1)^N h/3 (f(x_i) + 4 f(x_(i+1)) + f(x_(i+2)))
$

By calculation.
#import "@preview/theorion:0.3.3": *
#import "../lib.typ": *

#show: daily-en.with(title: [Differential Geometry])

#show: show-theorion

#set heading(numbering: "1.1")
#set par(
  first-line-indent: (
    amount: 1em,
    all: true,
  ),
)

#let cdot = $circle.small$
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

= Vector Fields on manifold

== Manifold is enough

#definition[
  A *Riemannian metric* on a manifold $M$ is the assignment to each point p in $M$ of a inner product $#inpro()_p$ on a tangent space $T_p M$.
  A *Riemannian manifold* is a manifold equipped with such metric.
]

Define a Riemannian metric on a piece of $M$ is always possible due to locally assemble to $bb(R)^n$. If we want to define globally, we need to tackle overlap. For example a point $p$, overlapped by multiple $U_alpha$, will cause a multiple intersection by multiple functions such that $sum_alpha f_alpha (p) #inpro(l: "-", r: "-")$. That's indicating, we may want, first the sum is finite for convergence and smooth; second the $sum_alpha f_alpha (p) = 1$ for equal weight. Rather strictly, we don't want boundary point be devil for us, for example infinite open intersection may be accumulated in a limit point even every inner points converges, also we want the boundary be smoothly going to zero. We thus define *supp($f$)* be the closure of $f$ whih $f(p) != 0$.

Then for a collection of atlas, or open set ${S_alpha}$, is locally finite if every point has a neighborhood $U_p$ in each $S_alpha$ only intersects only finitely many of the subset $S_alpha$.

A partition of unity is subordinate to ${U_alpha}$:

#set enum(numbering: "(i)")

+ supp$rho_alpha subset U_alpha$ for all $alpha$
+ the collections ${"supp" rho_alpha}$ is locally finite.
+ $sum_alpha rho_alpha (p) = 1$

Notice that we don't define $"supp"(rho_alpha) subset.eq U_alpha$ due the boundary limit point undefined behavoir. We only define metric on open set.

Rather a theorem lengthy tells us that existence of partition is in masonry. So every manifold can have a Riemannian metric to become a Riemannian manifold.

== Directional Derivative

We could parametrize a arc be unit of parameter.

For example a $c(t)$, define $t = t(s)$, we get $gamma(s) = c(t(s))$. Further, we define $||c'(t)|| = (d s) / (d t)$ which means $s$ is just length unit.

$
  ||gamma'(s)|| = ||c'(t(s))|||t'(s)| = (d s) / (d t) |(d t) / (d s)| = 1 \
  "length" = integral_a^t ||gamma'(s)|| d s = t - a
$

Choose $a = 0$, we get unit parametrization. Which means we can always use $[0,l]$ as the parameter.

We can then seek a directional derivative on $bb(R)^(n)$:

Suppose a small directional parameter $x^i = p^i + t a^i$

$
  D_(X_p) f &= (d ) / (d t)|_(t=0)f(p+t a) \
  &= sum (partial f) / (partial x^i)|_p (d x) / (d t)|_0 = (sum a^i (partial) / (partial x^i))f = X_p f \
$

In shorthand, we know it measure derivative of the components on each direction.

$
  D_(X_p) Y = sum (X_p b^i) (partial) / (partial x^i)|_p
$

Indeed match it. Notice that it differ from $X Y$ as composite derivative not only components but also partial derivative.

Thus former is a map from $cal(X)(bb(R)^n) -> cal(X)(bb(R)^n)$.

== Shape and Curvature

Suppose a _hypersurface_ $M$ in $bb(R)^(n+1)$ as a submanifold with codimension 1. Assume there is a smooth unit normal vector $N$ on $M$. We choose a directional derivative $D_(\(-\))$ in $bb(R)^(n+1)$ to encompass this submanifold.

$
  0 = X_p inpro(l: N, r: N) = 2inpro(l: D_(X_p)N, r: N)
$

This indeed gives us a hindsight on how a manifold curves. We know any tangent vector upon $M$ would be perpendicular to $N$. That's:

$
  &quad inpro(l: Y, r: N) = 0 \
  &-> X inpro(l: Y, r: N) = inpro(l: D_(X)Y, r: N) + inpro(l: Y, r: D_(X)N) = 0 \
  &-> inpro(l: D_(X)Y, r: N) = -inpro(l: Y, r: D_X N)
$

Know we seek a difference to measure the possible form:
$
  &quad inpro(l: D_(X)Y, r: N) - inpro(l: D_Y X, r: N) \
  &= inpro(l: D_X Y - D_Y X, r: N) \
  &= quad ?
$

We can calculate based on $bb(R)^(n+1)$ directional derivative.
$
  D_X Y - D_Y X &= a^i partial_i (b^j) partial_j - b^i partial_i (a^j) partial_j \
  &= a^i partial_i (b^j partial_j) - b^i partial_i (a^j partial^j) = X Y - Y X \
  &= [X, Y]
$

We denote final as commutator. We see in $bb(R)^(n+1)$, directional derivative commutator indeed a lie derivative.

It's still zero as $D_(X) Y$ is also a vector field on $M$, perpendicular to $N$.

$
  inpro(l: D_X Y - D_Y X, r: N) = inpro(l: [X,Y], r: N) = 0
$

Indeed, this indicates a symmetry. Which indicates a form much like metric.

Gives a $inpro(l: D_X Y, r: N) = inpro(l: Y, r: - D_X N)$, we define it as $inpro(l: L(X), r: Y) = inpro(l: X, r: L(Y))$.

It's useful to see for a curve $c(t)$ with vector field along it as $V$, we measure the component of the curvature of curve as difference along $V$(a.k.a $(d V) / (d t)$) that how much is along $N$:

$
  inpro(l: c''(t), r: N_(c(t))) &= inpro(l: (d V(t)) / (d t), r: N_(c(t))) \
  &= inpro(l: V(t), r: D_(c'(t))N_(c(t))) \
  &= inpro(l: L(c'(t)), r: V(t)) \
  &= inpro(l: L(V(t)), r: V(t))
$

Which indeed the normal curvature.

Now we seek by a unit vector $X$ with $inpro(l: L(X), r: X)$.

$
  inpro(l: L(X_p), r: X_p) &= X_p^T L G X_p = X_p^T A X_p \
$

Where $G$ is metric. Notice that given symmetry of $L$, we know $L G = G L$.

Given a lagrange multiplier with constraint $inpro(l: X_p, r: X_p) = 1$, we seek $X_p^T A X_p - lambda X_p^T G X_p$.

Thus we know:
$
  "grad"(...) &= 0 \
  A X_p &= lambda G X_p \
  L X_p &= lambda X_p
$

Indeed, that means $X_p$ is eigenvector, and $lambda$ are eigenvalues. Which point out in the most curved direction. We call them principal curvatures.

How can we seek a form? Usually we need parametrization by given $(r_1,...,r_n)$ substitute $(x_1(r_1,...,r_n),...,x_(n+1)(...))$. Given a partial derivative $(partial) / (partial r^j) = a_j^i (partial) / (partial x^i)$ relation by evaluate partial derivative on substitution, s.t.:

$
  f: M -> bb(R)^(n+1)\
  f_*: T(M) -> T(bb(R)^(n+1)) \
  f_*((partial) / (partial r^i)) = (partial x^j (r_1,...,r_n)) / (partial r^i)(partial) / (partial x^j)
$

Where we see $f(x^j) = x^j (r_1,...,r_n)$.

We denote each basis as $e_1,...,e_n$. Then we can get a metric based on inner product. We may hope to normalize it(But we can rather not if we focus on $det$). Finally we can get a normal vector by generalized cross product.

$
  N = mat(
    n_1, ..., n_(n+1);
    e_1;
    dots.v;
    e_n
  )
$

Where each $e_i$ has $n+1$ components, thus omit arbitrary column we can form a $det$ to give each $n_i$.

All in all, we take derivative on each to get a suitable solution for $L$.

We call $L(-)$ as second form as metric is first form. If we know what conponent are, as $L^i_j$, we may determines how curve a surface it's. However:

#set quote(block: true)
#quote(attribution: [Loring W. Tu Differential Geometry])[
  Some of the central problems in differential geometry originate in everyday life. Consider the problem in cartography of representing the surface of the earth on a flat piece of paper. A good map should show accurately distances between any two points. Experience suggests that this is not possible on a large scale. We are all familiar with the Mercator projection which vastly distorts countries near the north and south poles. On a small scale there are fairly good maps, but are they merely approximations or can there be truly accurate maps in a mathematical sense? In other words, is there a distance-preserving bijection from an open subset of the sphere to some open subset of the plane? Such a map is an isometry.
]

Thus if a map from $F: (N, inpro()) -> (M,inpro()')$, is a diffeomorphism, we also hope it's metric preserving:
$
  inpro(l: u, r: v)' = inpro(l: F_*(u), r: F_*(v))
$
Which we call it *isometry*. Thus if we want to measure how curve it's, we hope for any at least isometry map, there's a invariant retain its characteristic. We can see isometry as isometric embeddings(You can't stretch the surface but twist it smoothly) of the same manifold, for example, plane and cylinder. Thus if it's a isometry invariant, it should be *priori* and independent to various embeddings

= Differential Form

Suppose a bundle map, there's correspondence that:

$
  {"bundle maps" phi: E->F} <-> { cal(F)-"linear maps" alpha: Gamma (E) -> Gamma (F)},
$

Then given a $M -> T(M)$ and $M -> (M,C^infinity (M))$, we know that the fiber is $cal(X)(M)$ and $C^infinity(M)$ it give us a section map from $cal(X)(M) -> C^infinity (M)$ by:

$
  omega_p (X_p) = omega(X)(p)
$
Is the 1-form. Similarly, define n-form is just for multiple $product M$ repeatedly.

We can define wedge product without too much algebraic knowledge, for a $k$-form $alpha$ and a $l$-form $beta$, we define a shuffle as it permutes all possible cases.

$
  (alpha and beta) = sum_(sigma) "sign"(sigma) alpha(v_(sigma(1)), ..., v_(sigma(k))) beta(v_sigma(k+1), ..., v_sigma(l+k)).
$

A _exterior derivative_ is defined by $0$-form recursively.

Suppose $f$ is 0-form, Which must be nowhere injection into $C^infinity (M)$, is a arbitrary function, given a parameter $t$:

$
  f_*(X_p)(t) = X_p (t compose f) = X_p f \
  a (d ) / (d t)|_(f(p)) <-> a
$

Thus we say a correspondence by identification of $T_(f(p))bb(R)$ with $bb(R)$.

If we write down explicit coordinates:
$
  (d x^i)(partial) / (partial x^j) = (partial ) / (partial x^j)(x^i) = delta^i_j \
  (d f)_p (X_p) = X_p f \
  d f = sum (partial f) / (partial x^i) d x^i \
  (d f)_p (X_p) = (partial f) / (partial x^i) b^j delta^i_j = a
$

Indeed, we process on this recursively, the key is to notice that for 0-form $a$,$a and d x^i = a d x^i$. This is because 0-form takes no input and we omit this. Then it's clear that it form a algebra by such linearity and multiplication as $and$(0-form isn't special here without $and$!).

by a notation $I$ as index set:

$
  d omega &= sum d (a_I and d x^I) = d a_I and d x^I + (-1)^I a_I and d d x^I \
  &= d a_I and d x^I \
$
Indeed if we permutes:

$
  d (d x^I a_I ) &= (-1)^I d x^I and d a_I \
  &= (-1)^I (-1)^(I dot 1) d a_I and d x^I \
  &= d a_I and d x^I
$

It's instructive to derive a 1-form $omega = f d g$ explicitly:

$
  d omega(X, Y) &= d f(X) and d g(Y) = d f (X) d g (Y) - d g(X) d f(Y) = (X f)Y g - (Y f) X g \
  &= X (f Y g) -  f (X Y g) - (Y(f X g) - f(Y X g)) \
  &= X (f d g (Y)) - Y(f d g (X)) + f (X Y - Y X)g \
  &= X omega (Y) - Y omega (X) + omega([X,Y])
$

That's, if we gives a affine connection for a frame for $E$ over $U$ neighborhood. We can get that the connection must also be a linear combination of $e_i$.

$
  nabla_X e_j = sum omega^i_j (X) e_i
$

Where $omega$ is 1-form. This indeed give us:
$
  nabla_X Y = nabla_X(h^j e_j) = (X h^j)e_j + h^j omega^i_j (X) e_i = (X h^j + h^j omega^i_j (X)) e_i
$

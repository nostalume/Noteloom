#import "../lib.typ": *

#show: mine.with(
  title: "Math Physics",
)

#let hyperreal = $attach(bb(R), tl: *)$
#let tlstar(content) = $attach(content, tl: *)$

= Number System

The evolution of cognition of mathematics stem from *natural number*. What's the natural number? It describe a infinite process starts from a base. The base is *empty*. The negation of everything denoted as $nothing$. From a primitive view, the higher process includes the lower process which suggests that $? -> S(?)$ is a inclusion morphism. Such view is *ordinal* view. A child will imagine things in ordinal view, 3 apples is 1 apples more on 2 apples, etc. That's, inclusion process, a ordered structure. Such inclusion indicates that $?$ as a ordinal is a subset of its successor.

We can safely process $emptyset$ in mind, as a subset of a larger set. $S(emptyset) = {emptyset}$. The successor must be a larger set contains both empty and successor of empty, a well-inclusion process suggests ${emptyset, {emptyset}} = S({emptyset})$. Arabs number system spread as our todays number system. However we immediately found that such inclusion process itself is a number system. $S(*) -> S(S(*))$, it said, object is nothing but its relation, and base isn't such important, because select any number as base is reasonable. Such process generally and widely used in mathematics.

$S(b) = b + 1$ is not a equation but a interpretation which we translate function notation to Arabs number notation. But that's much more than this. First, we have no $+$, second, $1$ is a instance, but we haven't expanded such structure that $1$ is special to any others as such notation.

From $0$ to $1$, We has such equivalence that $(+ 1) -> S(*)$. Because a larger set of a set is a inclusion of elements of the set and the set itself, and the empty set as *nothing*, we acquire 1 as a instance. However, from morphism view, we see $0 = emptyset ~ id_(0\/emptyset)$, and $1 ~ S(id_0(*)) = S dot id_0 = S(*)$. Emphasis again, the instance is nothing but its relations, natural number as instance is actually the intepretation of infinite process.

That's, $(+1) ~ S(*)$. Arabians already knows addition which is multiple inclusion process. That's $S -> S dot S -> S dot S dot S(*) -> ...$ We thus immediately acquire addition as infinite process of such inclusion process itself.

So $(+n) ~ overbrace(S dot S..., n "times")$ gives us the operation. The commutativity is trivial because we apply the same induction process as $S$, there's no permutation at all. It's useful to use our infinite process again, it giving us multiplication as multiple inclusion of $(+n) -> (+n)(+n)(*) -> ...$. Usually, Arabians use $a n$ to denote $a$ times addtition of $n$. But it implicate a vagueness in addition and multiplication process priority. So in such number system, we should use bracket or restrict a multiplication priority:

$
  n x + b != n(x + b)
$

Where we fix $x$ as applied element. The distribution property is a corollary of commutativity of $+$.

$
  n (a + b) & = overbrace((a+b)+(a+b)+..., n "times") = overbrace(a+b+a+b+..., n "times") \
            & = overbrace(a+a+..., n "times") + overbrace(b+b+..., n "times") = n a + n b
$

We remove bracket is because there's no operation priority for $+$ as a repeated operation, we can place $+$ to anywhere with a element beside of it.

Now, we have a simpler way to deduce commutativity.

$
  n a (*) = n (overbrace(1 + 1 + ..., a "times")) (*) = overbrace(n+n+..., a "times") (*) = a n (*)
$

Finally, the relation of multiplication and successor:

$
  S(n)(*) = (n+1)(*) = n(*) + (*)
$

We apply induction process again to deduce power, $(* n) -> (* n)(* n) -> ... ~ n^(x)$ for $x$ times induction. We has the distribution, commutativity, and relation to addition(lower second order) in power too, with its multiplication as element:

$
  (a b)^x = overbrace((a b)(a b)..., x "times") = a^x b^x \
  (n^x)^y = (overbrace(n..., x "times"))^y = overbrace(n^y..., x "times") = (n^y)^x \
  (n)^(x + y) = overbrace(n..., x + y "times") = overbrace(n..., x "times") overbrace(n..., y "times") = n^x n^y
$

You see that the operation commutativity and distribution is based on the lower order but not all order. You can apply it to addition too.

Now, what if we deduce again? $(n)^n -> ((n)^n)^n -> (((n)^n)^n)^n -> ... ~ overbrace(n^n^n^..., x "times") = a arrow.t arrow.t b$ where we has a thing much like power. Such induction process called *Hyperoperation*.

We need to acquire a inverse operation of such system. This is, the extension of number system. Suppose addition first, $a + x = b$. If such reverse operation is always defined, we should has $x = (a+)^(-1) (b)$ to give a pleasant result. The partial order indicates a violation if $a > b$. Where there shouldn't exist a number in successor logic. But if it's defined, the new number is coming out as a extension of original number system. We test that:

$
  x = (a +)^(-1) (0) = (a +)^(-1)(id_0) = (a +)^(-1) \
  (a +)^(-1) (a +) x = x \
  (a +)^(-1) (a +) = 0 \
$

If it's applicable, and indeed so, called negative number corresponding to positive number. $bb(N) -> bb(Z)$ as the answer. But what's there order? It should be a reverse successor that, if original is greater, this should be smaller to retains the correct order. That's, $S^(-1) (a) < a$, $S^(-1)(0) < 0$. Now, there's no lower bound.

We try multiplication too, $a x = b$ is also in such corner. Define $x = (a *)^(-1) b$ reveals a huger number system. The reverse operation should has the same property as the original to maintain consistency. Test that:

$
  (a *)^(-1) (b) + (a *)^(-1)(c) = (a*)^(-1)(b + c) \
$
$
  (a *)^(-1) b + (c *)^(-1) d & = (a *)^(-1)(c *) (c *)^(-1) b + .... \
                              & = (a *)^(-1)(c *)^(-1)(b c + a d)
$

Such extension is $bb(Z) -> bb(Q)$, integer to rational number. It shows that given a rational number the order is determined by $b c - a d$. Where $0 < (n *)^(-1) 1 < 1$ is a results.

We summarize current cardinality where $abs(bb(Q)) = abs(bb(Z) times bb(Z)^*)$ Where we remove $0$, but reasonably, there could be a ${plus.minus infinity}$ as a additional number, but it will break the order. We can check any infinity has same order. But negative infinity is lower than any number, positive infinity is higher than any number, forming a circle order.
#footnote[It's undefined and rather prohibited as we usually learned, but limit haven't been "created" now.]

Now we proceed on power, or exponential. Because it's not commutative now. Such astonishing consequence derived from the canonical morphism that $n -> S^n$. $S^m S^n ~ S^n S^m$. But such distribution failed in exponential for $S$ that $S(n) m != S(m n)$ as we already shown in multiplication non-commutativity with successor.

Such problem immediately cause a infinite sequence which we call *polynomial*.

$
  sum_(bb(Q)) a_sigma x^sigma = 0
$
Where we use $sigma$ as a general notation of infinite iteration on all possible number of $bb(Q)$. We can, thus deduce that the new number system must be $product_abs(bb(Q)) bb(Q)$. However, $bb(Q)$ as a product, can be drawn as a grid and iterate in anyway to fill it. Which states that $f(n) -> bb(Q)$ is injective and surjective, for example $m/n <-> 2^m 3^n in bb(N)$. Thus $product_abs(bb(Q)) bb(Q) = product_abs(bb(N)) bb(Q)$. Which is a infinite sequence. How we express such system? The structure should inherit from $bb(Q)$, we can define it element-wise that each element endure the regulation of order of $bb(Q)$. But it doe not induce a native order like its base number system. That's, we need to induce a morphism into a order set or canonical number system to construct closeness.

Such infinite sequence can be expressed in many ways. galois extension states such extension as a vector space s.t. $Q[sqrt(2), sqrt(3), i, pi ...]$ #footnote[It should be clarified that the extension of all finite polynomial is called algebraic number $bb(A)$, which is a subfield of $bb(C)$. If you consider a infinite polynomial, for example $sin(x) = sum_i a_i x^i$, we can get $pi$ from $sin(x) = 0$, absolutely not in $bb(A)$.], or well known 10 digit expression s.t. $(...,0,1,2,3,...) <-> ...0.123...$ etc. The new number system is larger than we expected, as $abs(bb(N))^abs(bb(N))$, higher than $|bb(N)|$.



We apply induction of finite sequence with element of $bb(Q)$, the new number system must be a infinite sequence with a *nearness* no matter how we express it. Such process we call it *limit*. $lim_(n -> infinity)$ express the higher cardinality level as $lim_(n->infinity) (...,q_n) -> r$. Or, you can express it in anyway you want, for example, notorious $0.9999... = 1$ is the same logic here, also $lim_(n->infinity) q_n = r$ for rational $q_n$. The latter is *Cauchy Sequence* common in analysis. All above follows a order in $bb(Q)$ to construct $bb(R)$.

A additional structure should be established. A usual procedure to reach a real number by infinitesimal is that, $lim_(n->infinity) (r - q_n) = 0$, where $r - q_n < epsilon$, $forall epsilon$ $exists n > N in bb(N)$. This is a standard analysis that $epsilon$ is a residual number exist in Real which can be arbitrary small. Presume for most of elements in sequence they are *same*. The two real numbers should be infinitesimally close, construct a equality. Such sequence procedure with a *nearness*, notates as $tlstar(bb(Q)) tilde.equiv bb(R)$ could be a intermediate procedure during extension. We can apply it to every that $bb(N)^abs(bb(N))$ to construct $tlstar(bb(N))$ etc, with same cardinality as $bb(R)$.
#footnote[
  Such construction is called *hyper*, which is a nonstandard extension. The tedious comes from a order field embedding and the equivalence proposition of $bb(R)$ and $hyperreal$
]

In order to create such *nearness*(or convergence), suggest a filter on infinite elements in canonical order#footnote[Indeed if we use digit expression, we should compare the higher digit first. The filter on sequence should be restricted to the canonical order to avoid prohibited expression of sequence.], against finite, the case for $tlstar(bb(R))$ as a intermediate number system could be constructed. Ultra filter said that we can select collections of subsets of $bb(N)$, where its infinite, so it contains $bb(N)$, but also a consistent selection for intersections or superset other than finite sets. Thus every sequence could be compared through a equivalence class of such filter ensured by axiom choice although the conrete form is unknown.
#footnote[
  Even sequence like $(1,2,3,1,2,3,...)$ is not a canonical number in $bb(R)$, it could be assigned a determined order in $hyperreal$. Notably, we only compare the number in $bb(R)$, that's why it's not standard.
]

Thus for positive sequence that smaller than any number of $bb(R)^(>0)$, gives a infinitesimal(hypersmall) class $[epsilon]$, for positive sequence that greater than any number of $bb(R)^(>0)$, gives a infinite(hyperlarge) class $[infinity]$.

Now, we try to formalize continuity as a attempt. $forall delta in hyperreal, delta ~ [epsilon]: tlstar(f)(c+delta) - f(c) ~ [epsilon]$, where $c$ is a standard number in $bb(R)$.
#footnote[It should be clear that if in continuous process both number could be non-standard, it's called uniform continuity, for example, $1/N, 1/(N+1) ~ [epsilon]$ for $1/x$ is $N+1 approx.not N$ is not uniform continuous.]
Also the monotone boundary sequence has limit as $exists N ~ [infinity] in tlstar(bb(N))$
#footnote[Where we give the same sequence procedure on $bb(N)$, in which $[infinity] ~ [1,2,3,...]$ could be a instance of such equivalence class.]
, $forall n in N$ $s_N >= s_n$ is a element of upper bound, we also know it's a element of sequence, which suggest it's a least upper bound element, as $s_N = lim_(n->infinity) s_n$ in standard analysis.

The final problem here is that the number system can be inductively constructed higher than $bb(R)$ by operation completion? Currently, I don't know such operation as extension can be proceed further. But the cardinality, suggest a map from $bb(R)$ to $bb(R)$, which is $abs(bb(R))^(abs(bb(R)))$. That's where function(s) comes in.

= Function Space

In function, we can consider each real number in source as the ordinal of sequence $bb(N)$, and each element in the sequence as domain. Thus natively, we inherit the property of every operation in number like addition, multiplication, exponential etc. $(f + g)(x), f(x)g(x), f(x)^g(x) ...$. A structure has a basic additional *completion*(Or induction process completion if you want) is called *vector space*#footnote[I choose such because a mathematical structure must stem from canonical number system, multiplication could be derived as a induction of addition therefore construct a endomorphism as $v+v+v... ~ n v$, $n in bb(Z)$ and contrive a extension if we could.]. It's usual, even it's not trivial to define a ultra filter to measure how close between functions.

But wait here, such system seems, if acquire a total order by ultra filter, losing too much as we already seen in $bb(R)$. Where function space becomes a monotone space by a specific ultra filter. But if a ultra filter restrict too much, a less strict design should be considered. First we could define limit as usual.

The introduction of Lebesgue integral is highly resemble to filter#footnote[Rather ultra filter because for example, $[0,0.5]$ is a set where itself or its complement either is measurable, which doesn't satisfy *in or not* property of ultra filter.] where we need a basic order topology which usually contains all interval of $bb(R)$ which called Borel $sigma$-algebra. Where is closed under countable unions and intersections. We can consider it as a application of filter language. The measure, is actually full of tendency to create a consistent additive morphisms into $bb(R)^(>=0)$ where built upon characteristic function.

$
  chi_E = cases(
    1 quad x in E,
    0 quad x in bb(R) \/ E
  )
$

Where $f(x)$ is a fine addition of $chi_E$. But if we consider it as a sequence that such integration is actually natural and the limit $f(x) - f_N (x)$ $N tilde.eq [infinity] in tlstar(bb(N))$ can be reached if, the filter exclude all countable set which has smaller cardinality than $bb(R)$, constructing *almost all* property.
#footnote[The basic consequence is that the integral of $xi_bb(Q)$ is $0$.]

However, it there's no order, we should has a weaker order logic. We try to induce a morphism $d(*,*) -> S$ for a order set $S$(Or any given canonical number system).

The history of topology is based on selection of set. A finer selection means a huger control on element. Given a ordered set, we can always construct a open set which has ${x in X|a<x<b}$ stem from canonical order of number system. For a finite set, which has a cardinality equal to a subset of $bb(N)$, can be equipped with a order in $bb(N)$ as a topology space, it can be finer that for every element discretely separated, define every open set also as closed set as ${x}$.

Given a morphism $d(*,*): X times X -> S$ where $S$ a order set, it must has property to reflect the order of $S$. $X$ has no necessity to deduce a *total order* where every element can be smaller or greater, that's, we will encounter a violation if $d(a,c) < 0, d(b,c) > 0$ but $d(a, b) < 0$. But we indeed has $d(x,x) = d(x,x) + d(x,x)$ as a identity element of such addition structure, $d(x,x) = 0$. The continuity given by distance $d(x,B(x,epsilon))= d(B(x,epsilon),x) -> (x,y) = d(y,x)$ for the open ball defined as ${y in X | d(x,y)\/ d(y,x) < epsilon}$. Finally, suppose we want to find a distance in minimal lower bound by a selection of element $d(x,y_m)$, with a limit, $d(y_m,y_n) > d(x,y_m) + d(x,y_n) tilde.eq [epsilon]$ cause a violation. Thus $d(y_m,y_n) <= (...)$ forms a triangle inequality.

Thus, $bb(Q)^abs(bb(N))$ can also be a vector space equipped with $d(*,*)$. But is this necessary, the answer is no. It's at least indicates a Hausdorff topology. A weaker property is acceptable but the order induced by canonical number system is indeed Hausdorff, so we will take all this as a canonical way.

The distance morphism could retains vector structure in domain. First, it should be translation invariant which $d(x,y) tilde.eq d(x+alpha, y+alpha)$ independent of reference base. Second, it must retain scalar as linearity, $f(a x) = a f(x) -> d(a x, a y) = a d(x,y)$. Thus, we has $d(x,y) = d(x-y,0) tilde.eq norm(x-y)$.

The highly non trivial property of inequality ensure the limit existence. Which is another name of convexity. Suppose a homotopy $F(lambda)$ $lambda in [0,1]$:

$
  f(lambda x + (1-lambda)y) <= lambda f(x) + (1-lambda) f(y)
$

Where we recover back to triangle inequality if $lambda = 1/2$.

Now we are already into the language of function space. The basic analysis tells that $(*)^p$ is convex if $p >= 1$. With a pointwise inequality:

$
  abs(lambda f(t) + (1- lambda)g(t))^p <= lambda abs(f(t))^p + (1-lambda) abs(g(t))^p
$

Now, we apply integral which is addition of sequence or the given limit of characteristic function.

$
  integral abs(lambda f(t)+ (1-lambda) g(t))^p d mu <= lambda integral abs(f(t))^p d mu + (1-lambda) integral abs(g(t))^p d mu
$

Now a selection of $lambda$ is the trick to solve here. Suppose for $norm(x + y) <= norm(x) + norm(y)$:
$
  norm((x+y)/(norm(x)+norm(y))) <= 1
$
Thus take $lambda = norm(x)/(norm(x)+norm(y))$, $u = x/(norm(x))$ and $v=x/(norm(y))$, it becomes:

$
  norm(lambda u + (1-lambda)v) <= 1
$

then take equivalence selection on above integration, it suggests that the norm should be $(integral |f(t)|^p d mu)^(1/p)$. Then the inequality in integral called *Minkowski inequality* in $L_p$, where $L_p$ is the integrable sequence space with the given norm.

So, what about $p in [infinity]$? We could take a insight from basic analysis that $c^p tilde [epsilon]$ if $c in (0,1)$. Thus $norm(u/sup(abs(u)))_infinity = 1$ Where all element are suppressed only if the supreme is retained. That's, $norm(f)_infinity = inf_(mu(A)=0) sup_(t in Omega \\ A) abs(f)$ excluding all measure $0$.

The completeness is a verification of efficiency of approximation. That's, the near point as $d(a,b) < epsilon$ for $epsilon in bb(R)^(>0)$ and $a$ or $b$ is standard(Not the infinitesimal here!), is a same set as $a approx b$ or $a = b + [epsilon]$, For all nonstandard number here. Which states that the metric is effective reflective of point nearness.

The completeness criterion could be transferred from Cauchy in sequence into Cauchy in series. Suppose a absolute convergent $w_n = sum_(i=1)^n s_i$ that $norm(w_n - w_m) = norm(sum_m^n s_i) <= sum_m^n norm(s_i)$ where $n,m ~ [infinity]$, then $sum_m^n norm(s_i) ~ [epsilon]$, that's smaller than any $bb(R)^(>0)$, the completeness shows its converges. Reversely, a absolute convergent series converges, can be formulated as positive sequence
$w_n = sum_i^n (x_(i+1) - x_i)$. Which states that every sequence converges too. But what if the sequence contains negative? Where we separate here all $x_k = x_k^+ - x_k^-$ where positive part and negative is indeed converges $0 <= x_k^+ <= abs(x_k)$ suggests whole sequence converges, otherwise either part didn't converge cause a contradiction.

The same logic applied to $L_p$ here, that, every bounded or absolute convergent series of positive functions as:

$
  norm(sum_k^n f_k)_p <= sum_k^n norm(f_k)_p <= M
$

A limit of infinity is bounded too. Where the tails must also be converges to zero too. And apply a decomposition on positive and negative yielding a general results.

Such complete norm space called *Banach Space*.

= Functional Space

Now we try to proceed further, that with cardinality as $bb(R)^abs(bb(R))^abs(bb(R))$ as a functional space, evaluated each as a map from function to $bb(R)$(Or $bb(C)$). With a linearity based on base number system.

For $|T(f_n - f)| ~ [epsilon]$, for $n ~ [infinity]$, That's, $C[epsilon] ~ [epsilon]$ for any standard real number $C$. So the functional is bounded if:

$
  abs(T(f)) <= C norm(f)
$

Proceed further that if $norm(f) = 1$, we acquire:

$
  abs(T(f)) <= C
$
Which only depended on the bounded constant, which should be: $sup_(norm(f) = 1)(abs(T(f))) = C$, we also establish another definition that:

$
  norm(T) = sup(T(f)/(norm(f))) = sup_(norm(f)=1)(T(f)) \
  |T(f)| <= norm(T)norm(f)
$

Where we just change name from $C$ to $norm(T)$.

We know that, based on our fundamental spirit, a mathematical object can be represented as the relation upon that. Now we see that the *bounded* functional#footnote[If not it's not continuous and no limit at all.] can be formulated as the relation upon its working space. Where we call it *Dual Space* upon certain Banach space $X$, equipped with the $norm(*)_("op")$ functional norms, is a Banach space by the applied element on $X$ itself.

The problem is, is this always a natural corresponding relation between $X$ and its dual space $X^*$? We can formulates $X$ as double dual or dual of dual as $X^(**)$. That's if $x^(**)(theta) = y^(**)(theta)$ for all $theta in X^*$, then $x=y$. However, we should notice that we haven't prove this, it say that $()^(**): X -> X^(**)$ is injective by $x^(**) = y^(**) -> x = y$ if above is valid.

In finite dimension, it's always workable by finite selection extension, however, we can apply Zorn lemma(ensured by axiom choice) for infinite case. Suppose we already has a corresponding $f$ on given element or a subspace like $w$, then we want to do the same on $x = w + alpha z$ or $x in Z := W + "span"(z)$.

$
  g(w+alpha z) = f(w) + alpha c quad c in bb(R)
$

Which should be *bounded*. But how? We can select suitable $c$ to nudge over possible restriction where $g(w+alpha z) <= k norm(w+alpha z) -> c <= 1/(alpha) (k norm(w + alpha z) - f(w))$.

Indeed $alpha$ can be negative or positive so we turn around for all positive here and indeed smaller than the bound.
$
  (-1/alpha_1)(norm(v - alpha_1 z) + f(v)) <= c <= (v <-> w, alpha_1 <-> - alpha_2) quad forall v,w in W
$
We make a mess with algebra to yield:
$
  f(alpha_1 v + alpha_2 w) <= k norm(alpha_2 v + alpha_1 w) <= k (norm(alpha_1 v - alpha_1 alpha_2 z) + (v<-> w, alpha_1 <-> - alpha_2)) \
$
Which is reasonable. That's, we can always extend the *bounded* functional element to the maximal element as the union of them. Such theorem called *Hahn-Banach* theorem.

If there's a $f(x) != f(y)$ in a subspace, then it can be extended the whole space which yield the contradiction.

Such selection gives another topology, even the convergence of norm fails, the convergence of $theta(x_k)$,$forall theta in X^*$ is possible. We can thus extend it into the normed space where $x_k$ is bounded and $theta(x_k)$,$forall theta in A$. for the dense set $A in X^*$. It shows that the object of $X$ can converges in *element* that each sequence element will converge into the desired object, but the whole sum in norm is not. That's, *pointwise*, in Lebesgue integral sense(delta function if you like) for $L_p$, or pointwise convergence sense for $C(K)$ where $K$ is a compact topology space. The topology is indeed weaker than norm topology, called *Weak Topology*, with $tau_w subset.eq tau_s$ compared to *Strong(norm) Topology*, where the open set or reversely, closed set cardinality indeed lesser. But we can prove that they are the same in certain condition, that if we say $f(x_k) = g T(x_k)$ for $g in Y^*$, $T in "Hom"(X,Y)$, the key is $T$, from geometric level, if such sum or norm is restrict to compact space, where finite cover is enough, there restriction should be same. Indeed, for a compact space, we can always has a convergence sub-sequence, if not, we can extend the ball union infinitely where the finite cover doesn't work. Thus if $T$ is *compact*(Not only bound, but the domain is compact), we has the convergence limit as $T(x_k) -> T(x)$.

Then we apply inductively again on $x^(**)(f_k)$, where the canonical injection say that $f_k (x)$ converges, such dual of weak topology as *Weak\* Topology*. So what's matter? Suppose we separate $product_(x in X) {-norm(x), norm(x)} = {f: X -> bb(R) | abs(f(x)) <= norm(x) forall x in X} ~ {norm(f) <= 1}$ as the bounded set of each sequence element. Then a ball, defines a set can be modulo the unsatisfied element not in $X^*$. Such product topology identify each $f$ to the evaluation $(f(x))_(x in X)$, is a product of compact(bounded) interval in $bb(R)$. Thus such embed of ball of $X^*$ into the product space assign $f_k -> f ~ (f_k (x_n)) -> f(x_n)$ as the support of $f$. Which is compact. #footnote[We use the Tychonoff theorem where the product of compact space is compact. You can expand the detail that the $f_k$ bounded for certain $x_n$ must also has $f_k (x_n) <-> f_l (x_n)$ for a bounded sequence thus convergent(in $bb(R)$) with $k,l tilde.eq [infinity] in bb(N)^*$. Thus $f_k <-> f_l$.]
It said that $B_(X^*)$ is weak\* compact in the sense of evaluation on $X$. Where we can take $x^(**) (f) = f(x)$ embedding the $x in X$ into $f$ where $f in B_(X^*)$ $norm(f) <=1$ to redefine $x$ as $sup_f abs(f(x)) = norm(x)_X$ in $B_(X^*)$. Which called *universal* embedding as $X -> C(B_(X^*))$

We reverse the theorem that for the dual space and ball $B_(X^(**))$ in weak topology, identify the double dual with dual, if $X^(**) tilde.equiv X$, then the dual theorem exist and vice versa. We call it *reflexive* under canonical embedding.

A non-trivial application is to consider a concave inequality:
$
  ln(lambda a + (1-lambda) b) & >= lambda ln a + (1-lambda) ln b \
$

Choose $lambda = p$, $1-lambda = q$.
$
  ln(p a + q b) >= ln a^p + ln b^q = ln a^p b^q
$
Choose $a = x^(1/p)$,$b = y^(1/q)$:
$
  ln(p x^(1/p) + q y^(1/q)) & >= ln x y \
                 e^(ln ...) & >= e^(ln ...) \
      p x^(1/p) + q y^(1/q) & >= x y
$
Such inequality is called *Young's inequality*.

Take function evaluation pointwisely on $x,y$, we should take $1/p ~ p$ and $1/q ~ q$, rescaling $norm(f)_p = norm(g)_q = 1$ for simplicity.

$
  abs(f(t)g(t)) <= abs(f(t))^p/p + abs(g(t))^q/q \
  integral abs(f g) d mu = norm(f g)_1 <= 1/p + 1/q = 1 = norm(f)_p norm(g)_q
$
Called *Holder's inequality*. Rescaling on a different factor which is $s>=r$ that for bounded measure $mu(Omega)$:
#footnote[You may seek a counter example that $1/x$ on $L_2 subset.not L_1$, That, $L_2$ is bounded integral, isn't the case in $L_1$.]

$
  norm(f)^r_r & <= norm(abs(f)^r)_(s/r) norm(1)_(q) quad 1/q + 1/(s/r) = 1 \
              & = norm(f)_s mu(Omega)
$
It means $L_r subset.eq L_s$ for $1 <= r <= s <= [infinity]$.

// Same thing can also be achieved that $p/p = p(1-1/q) = p - p/q$ and $(p-1) = p/q$ for $norm(f)^(p(1-1/q))_p = norm(f)_p$,$norm(abs(f^(p-1)))_q = norm(f)_p^(p/q)$:
// $
// 	abs(f+g)^p <= abs(f+g)^(p-1)(abs(f)+abs(g)) \
// $

// $
// 	norm(f) = norm(f)_p^p (norm(abs(f^(p-1)))_q)^(-1)
// $
// By *Holder's inequality*.
// $
// 	norm(f+g)^p &<= norm(abs(f+g)^(p-1))_q (norm(f)_p + norm(g)_q) \
// 	&<= norm(f+g)_p^(p/q) (...)
// $

// $
// 	norm(f+g)_p <= norm(f)_p + norm(g)_p
// $
// Called *Minkowski inequality*. Above inequality indeed need a horrible attention.

The greatness comes from a minimal insight that:
$
  f(x) = f(x_mu(A) e_mu(A)) = x_mu(A) f(e_mu(A)) \
$
Define:
$
  f(e_mu(A)) := y_(mu(A))
$
Do I abuse notation? I hope not #footnote[It's called *Radon-Nikodym Theorem* where the all $f(1_A)$ is new mesure can be represented as $integral g d mu$ for a measurable function $g$ which is proved by arrange function of $mu + nu$.], even I don't suppose separable or countable basis but use the sequence view as before. Then for all $y_mu(A)$, there exist a $x$ s.t. Holder inequality is a equality, namely, choose $x := |y_mu(A)|^(q-1) e_mu(A)$ where $1/p + 1/q = 1$.

$
  abs(f(x)) = abs(x_mu(A) y_mu(A)) = abs(y^q_mu(A)) &<= norm(x_mu(A))_p norm(y_mu(A))_q \
  &= abs(y^(q/p p)_mu(A))^(1/p) abs(y_(mu(A))^q)^(1/q) = abs(y^q_mu(A)) = abs(f(x))
$
With $abs(f(x)) <= norm(f) norm(x)_p$, so $norm(y_mu(A))_q <= norm(f) <= norm(y_mu(A))_q$. Giving us the results.
#footnote[Note we choose a specific $x$ for arbitrary $y$ to acquire the supreme as equality. Not reversely!]

That's, $L_p^*$ can be represented as a weight function $y$ in integral form of $L_q$ where $1/p + 1/q = 1$. So we see that indeed, $L_p^(**) = L_p$ where in weak topology sense that converges element-wise. Generally, for a compact topology space $K$, the dual $C(K)^*$ is:
$
  f(x) := integral f d mu \
  norm(f) = abs(mu)(K)
$

Where $abs(mu)(K)$ is the total variation on the measured space, actually you are may acquainte like $integral d abs(mu) = integral abs(f) d x$ for some function but we shouldn't constraint ourselves at such concrete form. However, in $p=1$,$L_1^* = L_infinity$ by a bounded function as a compact space support, doesn't yield the same results on $L_infinity^*$ where the bounded restriction is lessen on the supreme support, that's we only need finite additive rather $sigma$-additive or countable additive, that bounded finite additive measure space is the $L_infinity^*$.

A notice should be mentioned that in descrete space, the inclusion is reverse that, for $1 <= r <= s <= [infinity]$, suppose that $norm(x)_r = 1$:
$
  x_n^r < 1 \
  x_n^s <= x_n^r \
  norm(x)_s <= 1 = norm(x)_r \
$
Is a reverse inclusion compared to $bb(R)$ cardinality integral space.

For the special case where $X tilde.equiv X^*$ as its compact support, that $1/p + 1/p = 1$, $p = 2$ give us a symmetry space that the product representation of $f$ is in itself. Such product symmetry representation called *Inner Product*. That $X = X^*$ space called *Hilbert Space* denoted as $H$, where the famous *Cauchy-Schwartz inequality* is the special case of Holder inequality. With a elegant projection property that the minimal product form:
$
  D(t) := norm(v + t y)^2 = norm(v)^2 + 2 t (v,y) + t^2 norm(y)^2
$
Where $t=0$ is the projection for minimal distance, we can always decompose the space into a subspace and its orthogonal complement as $H = M plus.o M^(perp)$.

We summarize above. Throughout the whole context, you won't see physics but it's appearance. The truth is, the sole appearance. Evaluate the number system is the quantification of the metric which represents the world, for example, time-space. A function is a state of the system which represents a evaluation of background for potential world. Therefore functional is the evaluation of the state, and operator is a transformation of the state, thus the system.

= ?

The cardinality start from $bb(R) arrow.t arrow.t 4$. However, the space is restricted to a symmetry in inner product evaluation. That's, $"Hom"(X -> X)$ for linear operator. Thus, given a base number system, we can construct the algebra indeed with addition, multiplication and norm inequality.

We denote the operator domain as $D(T)$ for source space $E$, where the graph $(x,T x) in Gamma(T)$ for morphism system $(T, D(T))$, is a closed space if, given a canonical norm by $norm(x)_E +norm(T x)_F$ has limit. We know that bounded space will faithfully inject the whole space $E$ without lossing information, $norm(T)_F <= M$. Thus the *closed* graph suggests a bounded operator if $D(T) = E$. A operator can be extended to a closed space if the uniqueness is ensured by original operator that $u <-> T u$ is unique, a.k.a injection, for example $u_n -> 0 ~> T u_n -> 0$ by linearity. That's, $overline(Gamma(T)) ~ Gamma(overline(T))$ as the smallest close extension indeed.

Actually a simple operator is not closable, for example $T(phi) = phi(0)$ where $phi(0) = 1$ is reasonable even $phi_n = phi(n x) -> norm(phi_n) = n^(-d/2)norm(phi) -> 0$ for $L_2(bb(R)^d)$ space, you may guess it's a delta-like function.

We restrict ourselves to Hilbert space where the inner product representation is a canonical form. That $((*)w,v): "Hom"(X -> X) -> bb(R)$ $forall w,v in H$ is a injection, it's true that $(A w,v) = 0$ for all $v,w$ and its coefficients which indeed zero. That, due to the domain problem, unbounded operator on inner product should consider two condition, first, if the inner product is same for all $v,w in D(T)$, then we call it *Symmetric*, indicates that $D(T) in D(T^*)$ for $T$ can take any role of $T^*$ can do. If there $D(T) = D(T^*)$, we call it *Self-Adjoint* plus the symmetric condition.

The uniqueness comes from the test elements on whole $H$. Where, if $D(T)$ is dense in $H$, the $T^*$ has a unique corresponding element by the uniqueness of Hilbert space.

Such pair $J:(x,y) -> (-y, x)$ that $(T x, v) <-> (x, T^* v)$ is a $(x, T x) -> (- T x, x) -> (v T x) - (T^*(v) x) = 0 = (-T x, x) dot (v, T^*(v))$. Where we can say that $gamma(T^*) = J(Gamma(T))^(perp)$. Thus, $Gamma(T^*)^(perp) = (...)^(perp)^(perp) = overline(J(Gamma(T)))$, indicates $T^*$ is closed. You can achieve the same by calling convergence on $(T x, v_n) = (x, T^* v_n)$. If $D(T^*)$ is dense, the $T^(**)$ is well defined, $J dot J = - I$,$Gamma(T^(**)) = ("twice") = overline(Gamma(T))$ suggests $overline(T) = T^(**)$, which means $T$ is closable. /* Reversely, if $T$ is closable, and indeed dense, then graph closure is the graph of closure, suggests, the $(...)^(perp)$ is also dense: $J J(overline(Gamma(T))) = J(Gamma(T^*)^(perp)) = J(Gamma(T^*))^(perp)$ is 0, thus $$ */

$(x, T^* v) = (T x, v) = (T^(**) x, v)$ for all $x in D(T^(**))$ suggests that $T subset T^(**)$. For dense $T$, $overline(T)^* = (T^(**))^* = (T^*)^(**) = overline(T^*) = T^*$. The symmetric $T$ suggests that $T subset T^*$ is also dense too. Then $T subset overline(T) subset overline(T)^* = T^*$. We know this means $T$ is closable, so extend $T$ into $T^(**)$ giving us equality, $T$ is self-adjoint by its symmetric property.

Suppose a morphism $l: cal(B)(bb(C),bb(C)) -> bb(C)$ from a measurable function $bb(C) -> bb(C)$ to $bb(C)$. We apply it: $l(f) = (f(T)v,v)$. The key is $(norm(f(T))^2v,v) = 0 -> norm(f(T)) = 0 -> f(T) = 0$. That's, the kernel of $l$. Due to injectivity of norm, we decompose it to $phi_T: C(bb(C)) -> "End"(H)$ with $f -> f(T)$ for linearity operator between $H$. The kernel $f(T) = 0$ must be well defined. Suppose a point valued function $f$ that $T - lambda_{x}$ that $f(T)|_({x}) = 0$ must be well defined, thus for all possible, may not countable $lambda_mu$ for certain measure $mu$ must be defined upon it to depict the whole kernel, for example the product form like $product_mu (T-lambda_mu)$. Now we said that such $lambda$ called *spectrum* of $T$. We can immediately inspect that there must countable or isolated points set and a continuous part as $mu_s + mu_c$ if you want. Thus we see $f(T) = 0 <=> f|_(sigma(T)) = 0$ giving us $cal(B)\/(f|_sigma(T) = 0) -> cal(B)(sigma(T))$ where $phi_T (f) = 0$ if $f|_(sigma(T)) = 0$.

Measure given on $(f(T)v,v) = integral_bb(R) f(x) d mu (x)$ for non vanishing function $f$ on spectrum with $mu(x) = mu_(T,v)(x)$ upon specific $T$ and $v$. The transformation giving by $U: L_2(sigma(T),mu) -> H$ is isometry which retains the norm. So that's the light comes from:
$
  T(U(f))(v) = T(f(T))(v) = (x f)(T)(v) = U(x f) v
$
$S = U^(-1) T U = x(*)$, is a  multiplication operator on $L_2(sigma(T),mu_v)$. It should be clarified that we don't construct somehow isomorphism, such map between them is not injective, Therefore the $x$ corresponds to a unknown measurable function $g$ in original space.
#footnote[Such technique corresponding to descrete space is also related to polynomial, that defines a $bb(F)[x]$-module with multiplication as endomorphism $x dot v = A v$ which has a non-zero kernel. Then $bb(F)^n [x]$ should construct a homomorphism $bb(F)^n [x] -> V$ to deduce the diagonal or rational form.]

We formalize a new measure on the inner product where the orthogonal projection $mu_v (A) = (Pi_A (v),v) in bb(R)$ induce the $Pi_A$ as the idempotent measure as $Pi_(T,bb(R)) = Pi_(T,[-r,r]) = I$ $Pi^2 = Pi = P$ as the project operator, thus $(T(v),v) = (integral_bb(R) f d Pi(v),v) = integral_bb(R) f(lambda) d mu_v (lambda)$ should be uniquely determined by $f$. We decompose $f = sum_i alpha_i chi_A$ for specific $A_i in bb(R)$. Such measure is finite that $norm(integral f(lambda) d mu_v(lambda)(v)) <= norm(f)_infinity norm(v)$. Thus $norm(integral f(lambda) d mu_v) <= norm(f(lambda))_infinity$. The identity operator is $I = integral_bb(R) d mu_v (lambda)$. You may say bad luck that we can't deduce $f(lambda)$ ever and ever! But the trick is to change variable:
#footnote[It suggests that first is to quote $T$ can be transformed into the multiplicative function $g$, then we use projection measure to transform onto $lambda$ variable by $chi_g$. But I guess jumping to the projection measure is a fine idea.]

$
  integral_bb(R) f(lambda) d mu_v (lambda) & = integral_bb(R) lambda d nu_v (lambda) \
                                 f(lambda) & = lambda'
$

If there's a $h in H$ that $(h, integral_bb(R) f(lambda)d Pi(lambda)(h)) <= norm(f(T)h)norm(h) = 0 -> f(T)h = 0$. That's, decompose the whole space except $"ker"(T)$ into its orthogonal projection. In practise, that's where $L v = lambda v$ comes from.

All above is just a rephrase of $T = lambda_mu v_mu times.o w_mu$ for certain measure. Thus we has $(T - lambda)^(-1) ~ 1/(lambda - lambda_mu) w_mu times.o v_mu$, thus $1/(2pi i)integral.cont_C (...) = w_mu times.o v_mu$, take product on arbitrary function inducing $(x_mu, w_mu) times.o (v_mu,y_mu) = delta(x-y)$ called *Green Function* or *Resolvent* of $T$ as $G(x,y,lambda)$. Usually we take $lambda=0 -> G(x,y)$, where $T G = w_mu times.o v_mu$, thus, $G(x,x') = 1/lambda_mu (x_mu, w_mu) times.o (v_mu,x'_mu)$.

We has the below form for spectrum where the $sigma(T)$ is the set of all $lambda$ support that $T-lambda$ is not injective on $D(T)$ where the support $x$ losing information. Suppose $v in "Ker"(T-lambda_0)$:
$
  0 = ((T-lambda_0) v,w) = (v, T^*-overline(lambda_0) w) = (v, (T - overline(lambda_0))w) \
$
If $lambda_0 = overline(lambda_0)$, a real number, for all $w in D(T)$, then $T-lambda_0 = 0$ yields a contradiction. Thus, $lambda_0$ must be a complex number and $v=0$. Thus, the spectrum is real subset. #footnote[It's not a proof, seriously you need to prove $T+i$ for its kernel and image that $(T v,v) = (v, T v) = plus.minus i norm(v)^2 -> v = 0$, thus $i$ shouldn't be in the spectrum. The same for $-i$. And therefore the $"Ker"(T - i) = "Im"(T-i)^(perp) = 0$ for arbitrary complex number that not a real.])

It's rather tiring to prove the unbounded case which I would rather quote the support of the space if could. You will find that we choose $T-i$ as a cheat, because it's not in the spectrum thus it's injective and dense for bijection, therefore it's continuous and then bounded. We apply again to prove that.

= Royal Road

A partial derivative operator:
$
  i partial_x: D(i partial_x) = {f in H | f in C^1} -> H \
$
If we apply inner product on $H$:
$
  integral f i partial_x g d mu = integral i partial_x f g d mu \
$
Wait, are we missing something? We force a vanishing upon the boundary condition. Suppose for $H(bb(R))$, for a compact support that such $f,g$ always vanishing on the boundary is called distributional derivative. If the derivative is in the $H$, such space called *Sobolev Space* $H^1 (bb(R))$ with a finite condition on $norm(partial_x f)$. We can define a higher order derivative for higher order Sobolev space $H^k (bb(R))$.

Dual of Sobolev space $H^(-k)(bb(R))$, can be represented as a sum of $L_2$ functions actings on derivatives of test functions as $sum_alpha integral f_alpha D^alpha u$ with $f_alpha in L_2$ upon $u$. For example, the delta function is in $H^(-k)$ but not in the $H^k$ space, where $H^(-k) supset L_2 supset H^k$.

It should be noted that $delta(x)$ upon $1_mu$ is $1_mu.$

Given a spectrum of $i partial_x$:
$
  i partial_x f = lambda f \
  f(x) = e^(i lambda x) quad lambda in bb(R) \
$
Represent the diagonal transformation. For any function $f$ in $H^1$ can be densely inserted into $L_2$ space. We thus decompose a function into its spectrum by:
$
  (f, e^(i lambda x)) = integral f(x) e^(-i lambda x) d mu(x) = cal(F)(f(x))(lambda)
$

Now we can say that $e^(i lambda x)$ is the general eigenfunction of operator $i partial_x$, with the orthogonal relation:
$
  integral e^(i lambda x) e^(-i lambda' x) d mu(x) = e^(i(lambda - lambda')x)/(i(lambda - lambda'))|^(+infinity)_(-infinity) = 2 pi delta(lambda - lambda')
$
By contour integral. Or $delta(x) = integral (delta(x),e^(i lambda x)) e^(i lambda x) d mu(lambda) = integral e^(i lambda x) d mu(lambda)$

With the summation of spectrum:
$
  f(x) = 1/(2pi) integral (f, e^(i lambda x)) e^(i lambda x) d mu(lambda)
$
As the so called inverse Fourier transform.

Now we impose the operator on $H[a,b]$ with periodic boundary condition that $f(a) = f(b)$, thus is self-adjoint for $i partial_x$:
$
  i partial_x f & = lambda f \
           f(a) & = f(b) \
$
$
  e^(i lambda a) & = e^(i lambda b) \
          lambda & = (2 pi n)/(b-a) = (2 pi n)/(L) \
            f(x) & = e^(x (2 pi i n)/L) \
$
With a orthogonal relation:
$
  integral e^(i lambda x) e^(-i lambda' x) d mu(x) = (...)|^b_a = L delta(lambda - lambda') \
$

Take the decomposition of $f$:
$
  (f, e^(i lambda x)) = integral f(x) e^(-i lambda x) d mu(x) = cal(F)(f(lambda)) quad lambda in (2 pi n)/(L) \
$
With the summation:
$
  f(x) = 1/L integral (f, e^(i lambda x)) e^(i lambda x) d mu(lambda) \
$
Usually the terms $L$ or $2 pi$ will be placed on one side like inverse Fourier transform or evenly placed as $1/sqrt(*)$.
#footnote[You can choose many conditions as long as it forms a self-adjoint operator. Usually, they are Dirichlet or periodic boundary condition, or Neumann boundary condition that $partial_x f(a) = partial_x f(b)$, or Robin boundary condition that $alpha_1 f(a) + alpha_2 partial_x f(a) = beta_1 f(b) + beta_2 partial_x f(b)$ for some constants $alpha_i,beta_i$ where the operator is self-adjoint. The key is to ensure the operator is self-adjoint, then the spectrum is real and the eigenfunction is orthogonal.]

Actually, because $i partial_x <-> partial_x$, the $partial_x$ all spectrum should be $"Im"(bb(C))$. Thus $(A - lambda I)^(-1)$ is well defined as $G(lambda)$,$lambda in bb(R)$:

$
  (lambda - partial_x') G(lambda)(x,x') = delta(x - x') \
  G(lambda)(x,x') = e^(-lambda (x-x')) Theta(x-x')
$
Where $T u = f$ gives:
$
  u(x) & = integral u T(x') G(x,x') d mu(x') \
       & = integral ((lambda + partial_x') u G d mu(x') + u G|^?_? \
       & = integral f G d mu + u G|^?_? \
       & = integral f e^(- lambda (x-x')) d mu(x') + (u e^(- lambda (x-x'))|^?_? \
$
Given a function where $x > x'$, or we change variable to $x - x' = t$, which called *Resolvent* of $partial_x$. Even through the operator is not equal to its dual. If you choose $t in L_1[0, infinity]$ that the boundary term only left with $-u(0)$. Now given a arbitrary $lambda$ as $R(partial_x)(lambda)$:
$
  u(x) = integral_(-infinity)^x f(x') e^(-lambda (x-x')) d mu(x') = integral_0^(+infinity) f(x + t) e^(-lambda t) d t \
$
$
  R(partial_x)(lambda) = integral_0^(+infinity) f(t) e^(-lambda t) d t = u(0)(lambda)
$
Is the boundary term, which is *Laplace Transform*. Evaluate further that $f(x+t) = D(t)(f(x)) = e^(t partial_x)(f(x))$. Generally, $partial_x$ is the generator of the translation operator. Where $D(t) = e^(t partial_x)$ is the continuous semi-group of the generator. We know that the contour of green function would be:
$
  1/(2pi i) integral.cont_C (lambda I - T)^(-1) d mu(lambda) = I
$
For possible measure, thus we has below:
$
  1/(2pi i)integral.cont_C e^(t lambda) (lambda I - T)^(-1) d mu(lambda) = e^(t T) = D(t)
$
Where given $partial_x$ we has:
$
  1/(2pi i)integral.cont_C e^(t partial_lambda) (lambda I - partial_x)^(-1)(f(x)) d mu(lambda) = D(t)(f(x)) = f(x+t)
$
Choose $x = 0$ gives us *Inverse Laplace Transform*. The projection isn't orthogonal but still span completely.

= Special is Bad
$
  (L_1(r_i,...,r_n) + L_2(r_i,...,r_n'))psi = 0
$
If there's a separation indicates:
$
  L_1({r_i})psi = - L_2({r_i'})psi \
  L_1({r_i})psi = lambda psi \
  psi({r_i,r_i'}) = C({r_i'})psi({r_i}) \
$
Where $r_i,r_i'$ are distinct, and $psi$ is a eigenfunction of the operator $L_2$, then it must give us a eigenfunction on $L_1$ which is a smaller decomposition. We may repeat again and again until the set of coordinates are exhausted and sole as $L(r_i)psi = lambda psi$ for a specific $r_i$ where the coordinates are independent. It should be considered that $psi$ must be automatically a general composition of all eigenfunctions.

For example:
$
  (partial psi)/(partial t) = kappa(1/r^2 (partial)/(partial r)(r^2 (partial psi)/(partial r)) + 1/(r^2 sin(theta)) (partial)/(partial theta)(sin theta (partial psi)/(partial theta)) + 1/(r^2 sin^2 theta) (partial)/(partial phi)(partial psi)/(partial phi))
$
In order to derive $r$ single coordinate, we already see that we already separate $t$, so it's a first constant. Second, we multiply $r^2$ and we inspect that all terms are separated from $r$, so we acquire:
$
  (partial)/(partial r)(r^2(partial psi)/(partial r)) + (lambda_1/(kappa)r^2 + lambda_3+lambda_4)psi = 0
$
As for $theta$, we multiply $r^2$ and separate all unrelated terms, we leave only $theta$ and $phi$. Then, multiply $sin^2(theta)$ to yield a independent operator on $theta$:

$
  sin theta (partial)/(partial theta)(sin theta (partial psi)/(partial theta)) + ((lambda_1/(kappa)+lambda_2) sin^2 theta + lambda_4))psi = 0
$
Where we should know that the equality will reduce the number of known, so we choose $f(lambda_1,lambda_2,lambda_3,lambda_4) = lambda_1/kappa + lambda_2 + lambda_3 + lambda_4 = 0$, or other way you want to reduce the number of knowns.

$
  (partial^2 psi)/(partial phi^2) + (lambda_1/kappa + lambda_2 + lambda_3)psi = 0 \
  (...) - lambda_4 psi = 0
$

Suppose ODE:

$
  sigma(z) y'' + tau(z) y' + lambda y = 0 \
  sigma(z) y''' + (tau(z) + sigma'(z)) y'' + (lambda + tau'(z)) y' = 0 \
$
Take $y' = v$
$
  lambda v = lambda y' = - (tau(z) v'' + (tau(z) + sigma'(z))v' + tau'(z)v) \
  lambda y = - (sigma(z) v'' + tau(z) v) = integral v d z \
$
That said:
$
  L y = lambda y \
  (L' y = L' y') + L y' = lambda y' \
  (L^((n)) + L^((n-1))) y^((n-1)) = lambda y^((n-1)) \
$
Where $y'$ is also the original solution derivative. We thus take a recursion on it with a form $v_n = y^((n))$.

Then we write as self-adjoint form by a suitable function $rho(z)$:
$
        (sigma rho y')' + lambda rho y & = 0 \
  (sigma rho_n v'_n)' + mu_n rho_n v_n & = 0 \
$
With:
$
       sigma y'' + & tau y' + lambda y = 0 \
    (sigma rho)' = & tau rho \
  (sigma rho_n)' = & tau_n rho_n \
$

After such transformation, the orthogonal property rely on the new ODE rather the old:

$
  L = (sigma y'' + tau y') \
  integral y_1 rho L (y_2) d mu = integral y_1 lambda_2 rho y_2 d mu = integral rho L (y_1) y_2 d mu = integral rho lambda_1 y_1 y_2 d mu = 0
$

That's, we has a additional weight function $rho$ compared to original $L v = lambda v$ spectrum orthogonality.

The recursion can be taken:
$
       tau_n (z) & = tau(z) + n sigma' (z) \
  (sigma rho_n)' & = tau_n rho_n = (tau + n sigma') rho_n = ((sigma rho)'/rho + n sigma') rho_n \
$
$
  sigma' rho_n + sigma rho'_n & = sigma' rho_n + (n sigma' + rho'/rho) rho_n \
                 rho'_n/rho_n & = rho'/rho + (n sigma')/sigma \
                     ln rho_n & = ln rho + n ln sigma \
                        rho_n & = rho sigma^n \
$
$
  mu_n = lambda + n tau' + n(n-1)/2 sigma'' \
$
The recursion said that:
$
  (sigma rho_n v'_n)' = (rho sigma^(n+1) v_(n+1))' = (rho_(n+1) v_(n+1))' = - mu_n rho_n v_n \
$
$
  rho_n v_n = - 1/mu_n (rho_(n+1) v_(n+1))' => (product_n^m 1/mu_n) (rho_m v_m)^((m - n))
$
If $y(z)$ is a polynomial of degree $n$, or simply with a finite recursion that $v_n = "const"$, we has:
$
  v_n = y^((n)) = "const" \
  rho y = (product^n_0 1/mu_n) (sigma^n rho)^((n)) = C_n (sigma^n rho)^((n))
$
$
  mu_n = 0 -> lambda = - n tau' - n(n-1)/2 sigma'' \
$

Such form called *Rodrigue polynomial* in recursion.

We has the tool to solve the *Legendre* polynomial:
$
  (1-x^2)d/(d x) P(x) - 2 x d/(d x) P(x) + lambda P(x) & = 0 \
                  d/(d x) ((1-x^2) P(x)) + lambda P(x) & = 0 \
$
$
  sigma & = 1 \
    rho & = (1-x^2)
$
$
  P_n = C_n (d/(d x))^(n) (1-x^2)^n \
  lambda = - n tau' - n(n-1)/2 tau' = n(n+1)
$

For general second order ODE, we want to first transform it into *Rodrigue* form by parameter transformation.
$
  u'' + gamma/sigma u' + theta/sigma u = 0 \
$
We can take a parameter transformation which is also a second order ODE.
$
  u = phi.alt y \
  y'' + (2 phi.alt'/phi.alt + gamma/sigma)u' + (phi.alt''/phi.alt + phi.alt'/phi.alt gamma/sigma + theta/sigma) u = 0
$

We then want to encompass the denominator of $sigma$ into $phi.alt'/phi.alt$.
$
                  phi.alt'/phi.alt & = pi/sigma \
  2 phi.alt'/phi.alt + gamma/sigma & = tilde(gamma)/sigma \
                                pi & = 1/2(tilde(gamma) - gamma)
$

Thus one has:
$
  phi.alt''/phi.alt = (phi.alt'/phi.alt)' + (phi.alt'/phi.alt)^2 = (pi/sigma)' + (pi/sigma)^2
$

In order to absorb the denominator of the third term, which is of $sigma^2$ in denominator, we have to transform $theta/sigma ~> theta/sigma^2$ for original $theta$ for ease.

We has the final form:
$
  tilde(gamma) = gamma + 2 pi \
  tilde(theta) = theta + pi^2 + pi(gamma-sigma') + pi' sigma
$
$
  y'' + (tilde(gamma)/sigma)y' + (tilde(theta)/sigma)y = 0
$

In order to transform into Rodrigue form, one has $tilde(theta) = lambda sigma$. To determine this, we need to determine the new variable function $pi$ first.

Do some algebra into the quadratic form:
$
  pi^2 + (gamma - sigma') pi + theta - (lambda - pi')sigma = 0
$

If we assume $lambda - pi'$ is known:
$
  pi = (sigma' - gamma)/2 plus.minus sqrt(((sigma'-gamma)/2)^2 - theta + (lambda - pi')sigma)
$
Current consequence is the final answer, a highly non-trivial equation hard to solve.

However, for a polynomial form, or any arbitrary polynomial expansion:
$
  deg(pi) < max(deg(theta), deg(sigma))/2 \
  deg(pi') = deg(pi) - 1 \
$
We must has a square term is also a polynomial too. Thus its discriminant is also zero.

Thus we get:
$
  & Delta((sigma' - gamma)/2 - theta + (lambda - pi') sigma) = 0 \
  & tilde(gamma) = gamma + 2 pi \
  & tilde(theta) = theta + pi^2 + pi(gamma-sigma') + pi' sigma \
  & lambda = tilde(theta)/sigma \
  & phi.alt'/phi.alt = (ln (phi.alt))' = pi/sigma
$
Is the final answer.

We will use above technique to solve $Theta = psi(theta)$ part. First, we will transform it into a finite polynomial form, or you should notice that $sin^2 theta = 1 - cos^2 theta$ is a general polynomial relation:

$
  sin theta (d)/(d theta) = sin theta ((d cos theta)/(d theta))(d)/(d cos theta) = - sin theta^2 (d)/(d theta) \
$

$
  (d)/(d x)[(1-x^2) (d Theta)/(d x)] + (mu + m/(1-x^2))Theta = 0 \
$
We choose below constant representation:
$
  mu & = lambda_1/kappa + lambda_2 \
   m & = lambda_4
$

We can inspect that $sigma = 1-x^2, gamma = -2x, theta = mu(1-x^2) +m$. We can derive $pi$:

$
  pi = (sigma' - gamma)/2 plus.minus sqrt(((sigma'-gamma)/2)^2 - theta + (lambda - pi')sigma)
$
$
  (sigma' - gamma)/2 & = 1/2 (-2x + 2x) = 0 \
        lambda - pi' & = k \
$
$
  Delta & = k(1-x^2) - m - mu(1-x^2) = 0 \
        & = (mu - k)x^2 - m + k - mu
$
We inspect that we has non-trivial solution by taking $lambda - pi' = k = "const"$ that:
$
  pi = cases(
    plus.minus sqrt(m) quad k = mu,
    plus.minus sqrt(m)x quad k = mu + m
  ) \
  pi' = lambda - k = lambda - mu - m = plus.minus sqrt(m) \ lambda = mu + sqrt(m)(sqrt(m) plus.minus 1)
$
Which is consisten answer.

$
  phi.alt'/phi.alt = (ln (phi.alt))' = pi/sigma
$

$
  tilde(gamma) & = gamma + 2 pi = -2x plus.minus 2 sqrt(m) x = 2(plus.minus sqrt(m)-1)x \
$
$
  ln(phi.alt)' & = plus.minus sqrt(m)x/(1-x^2) \
       phi.alt & = (1-x^2)^(plus.minus sqrt(m)/2) \
$

In order to take Rodrigue form, we need to take a self-adjoint form first, with new parameter $rho$:
$
                             (sigma rho)' & = tilde(gamma) rho \
                  sigma' rho + sigma rho' & = tilde(gamma) rho \
  (sigma' - tilde(gamma))rho + sigma rho' & = 0 \
$
$
  (-2x - 2(sqrt(m) - 1)x) rho + (1-x^2) rho' & = 0 \
                                (1-x^2) rho' & = 2 plus.minus sqrt(m)x rho \
                                         rho & = C_m (1-x^2)^(plus.minus sqrt(m))
$
Thus we has:
$
  (rho sigma y')' + lambda rho y = 0 \
$
$
    rho & = (1-x^2)^(plus.minus sqrt(m)) \
  sigma & = (1-x^2) \
$
Choose $sqrt(m) ~ m$ to ease burden:
$
  y_n = C_(n m)/((1-x^2)^(m)) ((d)/(d x))^n ((1-x^2)^(n+ m))
$

$
  Theta = phi.alt y = C_(l m) (1-x^2)^(-m/2) (d/(d x))^(l-m)(1-x^2)^(l) quad l = (n+m) \
  lambda = mu + m(m plus.minus 1)
$
Is the final answer.

We can inspect that for a self-adjoint form ODE, we has $sigma' = gamma$. Thus we only has:

$
  pi & = sqrt((lambda - pi') sigma - theta) = sqrt(k sigma - theta) \
$

We then try to develop the operator induction form on $Phi = psi(phi)$. For a operator $D psi = lambda psi$ we gain a spectrum. However it's actually a reduced form of component of general $f(D)psi = f(lambda)psi$. Such function set, can reduce to $D psi = lambda psi$. Thus for $partial psi = lambda psi$, one has $psi = e^(lambda x)$. In angular part, we has $phi ~ (0,2pi)$ with periodic form $psi(phi + 2pi) = psi(phi)$ forming a skew-symmetric operator, where all spectrum is imaginary and integer form.

$
  D^2 psi & = partial^2 psi = lambda^2 psi \
   lambda & = i lambda' quad lambda' in bb(Z) \
      psi & = e^(i lambda x) \
$

It should be clarified that $Theta = P_(l m)$ is only orthogonal in $l$ rather in $m$, unless we encompass the $Phi$ part too. It's because the coefficient dependence of $m$ which is external to the ODE rather as the spectrum. Generally $nabla^2 v = lambda v$ will construct the whole basis, and indeed, $nabla^2 v = 0$ only construct a part of it, which the radial part forms no orthogonal basis.

Thus we reduce any form into algebraic equation for certain operator $D$. Especially many coefficients derivatives polynomial form $f(partial_x)$ must has a general form $e^(lambda x)$ where there may not exist a self-adjoint form, thus resolvent must intervene with $R(D)(f)(lambda)$ for certain special function with special solution, it's a generalization of linear algebra that one has rank and null for vector expansion, we call it *Fredholm theory*. Now we gonna develop a derivative operator form:

$
        p y' + y & = q \
  p(partial+1) y & = q \
               y & = 1/(p partial + 1) q \
$
If we expand it as:
$
  y ~ sum_(n=0)^(infinity) (-1)^n (p partial)^n q
$

For spectrum:
$
  p partial v & = lambda v \
      (d v)/v & = lambda/(p) d x \
            v & = C exp(integral lambda/p d x)
$
Is unbounded for many function set $p$. Actually we know $p partial$ is a unbounded operator as we developed before, choose $p = 1$:
$
  norm(partial e^(i lambda x)) ~ lambda^2 norm(e^(i lambda x)) = lambda^2 -> infinity
$
Thus generally, we can only acquire a part of solution upon $p partial$ operator with $norm(lambda) <= 1$ for above series expansion. However, integral operator is compact:

$
  integral^x p v d x & = lambda v \
                 p v & = lambda v' \
                   v & = C exp (integral^x p/lambda d x) \
$

We inspect that given a finite boundary initial condition e.g. $v(c) = C$, we has:

$
  integral^x_c p v d x & = lambda v \
                  v(c) & = integral^c_c p v d x = 0 = C exp(integral^c_c p/lambda d x) = C \
$
Giving that $v = 0$ for general $lambda$, thus we only has $lambda = 0$ in $L_1[c, infinity]$, indicating a inverse always exist, where we restrict the function all into the domain of integral operator where the function should be bounded after integral.

Thus for many initial condition ODE, we has a better behavoir on integral operator rather differential operator, we denote as $1/partial = partial^(-1)$:

$
  y' + p y = q \
  y + (partial^(-1) p) y + C = partial^(-1) q \
  y = 1/(1+ partial^(-1)p) (C + partial^(-1) q)
$
Because it has a zero spectrum, we can always expand without worrying.
$
  y = sum_(n=0)^(infinity) (-1)^n (partial^(-1)p)^n (C + partial^(-1) q) \
$

// For second order, one has:
// $
//   y'' + p y' + q y = f \
// $
// Take integral:
// $
//   y' + p y + partial^(-1)(p' y) + partial^(-1)(q y) + C &= partial^(-1) f \
//   y + partial^(-1)(p y) + partial^(-2)(p' y) + partial^(-2)(q y) + C_2 + C_1 x &= partial^(-2) f \
//   (1 + (partial^(-1)p) + partial^(-2) (p' + q')) y &= partial^(-2)f + C_2 + C_1 x \
// $
// We has:
// $
//   y = (1 + (partial^(-1)p) + partial^(-2) (p' + q'))^(-1)(partial^(-2)f + C_2 + C_1 x))
// $
// Certainly not a pleasant procedure. We only denote a shift property for general case on $D psi = lambda psi$

$
           D (psi u) & = psi (D + lambda) u \
  psi^(-1) D (psi u) & = (D + lambda) u \
$
Or, if there exist a inverse:
$
  u & = psi^(-1) D^(-1)(psi (D+lambda) u) \
$
$
  psi^(-1) D^(-1) (psi (*)) ~ (D+lambda)^(-1) \
  psi^(-1) D^(-n) (psi (*)) ~ (D+lambda)^(-n) \
$
/* For example:
$
  cal(F)(e^(i a x) f) = T_a (cal(F) f) \
  e^(i a x)(f) = cal(F)^(-1) T_a cal(F) (f) \
$ */
Thus, one has #footnote[You should notice that we only has $U A = Sigma U$ but we don't have $U A U^(-1) = Sigma$ to transform back without losing information, for example, partial will remove constant related information.]:
$
  p partial (e^(integral lambda/p d x)u) = e^(integral lambda/p d x)(p partial + lambda)u
$
Which solve as:
$
                                               y' + p y & = q \
                                    (1/p partial + 1) y & = q/p \
  e^(- integral p d x) 1/p partial e^(integral p d x) u & = q/p \
                                                      u & = e^(- integral p d x)(integral q e^(integral p d x) + C)
$

Now, if $lambda_1/kappa = 0$, we can acquire a Euler differential equation:

$
  (r^2 R'(r))' + mu R(r) = 0 \
$
It's hard to observe it's actually a polynomial form of a single operator.
$
  (x partial)^2 = x (partial x partial) = x (partial + x partial^2) = x^2 partial^2 + x partial \
$
Where we can thus formulate the spectrum:
$
  x partial v & = lambda v \
      (ln v)' & = lambda / x \
            v & = x^(lambda) \
$
Then we take the solution set:
$
  lambda (r^2 r^(lambda - 1))' + mu r^lambda = 0 \
  lambda (lambda - 1) r^lambda + mu r^(lambda) = 0 \
  mu = -lambda (lambda - 1)
$
We should observe that $mu$ is a integer form in $Theta$ part, thus $lambda$ is integer.

We could also formulate the folded part $(D - lambda)^n y = 0$:
$
  (D - lambda)^n (psi y) = psi D^n y = 0\
$
Thus we can inductively deduce the form:
$
  D^n y = 0
  D y_n = y_(n+1) ~> 0
$
As for case $partial$, we has:
$
  y = sum_0^(n-1) c_i x^i \
  psi y = e^(lambda x) y
$
Or in $x partial$, we has:
$
  x partial y & = 0 \
            y & = c = c x^0 \
$
$
  x partial y & = c \
            y & = ln x \
$
$
  x(partial y) & = ln x \
     partial y & = ln x (ln x)' \
             y & = 1/2 ln^2 x \
      ~> psi y & = x^(lambda) sum_0^(n-1) c_i ln^i x
$

We evaluate Rodrigue further:

$
  Phi(z, t) = sum_(n=0)^(infinity) y_n/(n!) t^n \
  y_n = 1/rho (d/(d z))^n (sigma^n rho) = 1/rho n!/(2 pi i) integral_C (sigma^n (s) rho (s))/(s - z)^(n+1) d s
$

$
  Phi(z, t) = 1/(2 pi i rho) integral_C rho(s)/(s - z) [sum_(n=0)^(infinity) ((sigma(s)t)/(s - z))^n] d s \
$
We interchange summation and interaction because if $Phi(z, t)$ is not convergent, there's no need to evaluate a concrete form indeed. We apply geometric series too:

$
  sum_(n=0)^(infinity)((sigma(s)t)/(s - z))^n = 1/(1- (sigma(s)t)/(s-z)) = (s-z)/(s-z- sigma(s) t) \
$
$
  Phi(z, t) = 1/(2pi i rho) integral_C rho(s)/(s - z - sigma(s) t) d s
$
Where we can evaluate on single pole of $s-z-sigma(s)t$ which must be $(s-xi)f'(s) = (s-xi)(1-sigma'(s)t)$:
$
  C_(-1) = rho(s)/(1 - sigma'(s)t) \
  Phi(z, t) = rho(s)/rho(z) 1/(1-sigma'(s)t)bar_(s=xi(z, t))
$

For Legendre polynomial, we can check that:
$
            sigma(s) & = 1-s^2 \
  s - z - sigma(s) t & = s - z - (1-s^2) t = 0 \
$

$
  t s^2 + s - z - t = 0 \
  s = (-1 + sqrt(1+4t(t+z)))/(2 t) \
$

$
  Phi(z, t) = 1/(1+2s t)|_(s=xi(z, t)) = 1/(sqrt(1+4 t z + 4t^2)) = sum_(n=0)^(infinity) (P_n (z))/n! t^n \
  P_n = (d/(d z))^n (1-z^2)^n
$
Normalize to determine the coefficients:
$
                                 t & -> t/2 \
                (P_n (z))/(2^n n!) & -> P_n (z) \
  sum_(n=0)^(infinity) P_n (z) t^n & = 1/sqrt(1+ 2 t z + t^2)
$

For $z = cos theta in (-1,1)$, $abs(t) < 1$ is the convergence condition, if we want to expand a distance:

$
  1/(abs(r_1 - r_2)) = 1/(sqrt(r_1^2 + r_2^2 - 2 r_1 r_2 cos theta))
$
You can take out the denominator to normalize it as you want $r_1/r_2$ or $r_2/r_1$ as long as $r_1 < r_2$ or $r_1 > r_2$.

We know back to the general part, where addition time part will give the freedom of radial part as:

$
  r^2 ((partial)/(partial r))^2 psi + 2r (partial)/(partial r)psi + (k r^2 + alpha) psi = 0
$

$
  z^2 u'' + z u' + (z^2 - v^2) u = 0 \
$
$
  & sigma = z \
  & gamma = 1 \
  & theta = z^2 - v^2 \
$

$
  & pi = sqrt(k sigma - theta) = sqrt(k z - z^2 + v^2) \
  & Delta = k^2 + 4 v^2 = 0 -> k = plus.minus 2 i v \
  & pi = plus.minus (i z + v) \
$

$
  (ln (phi.alt))' & = plus.minus(i z + v)/(z) = plus.minus(i + v/z) \
          phi.alt & = z^(plus.minus v)e^(plus.minus i z) \
$
$
  tilde(gamma) & = 2pi + gamma = plus.minus 2(i z + v) + 1 \
        lambda & = k + pi' = plus.minus 2 i v + plus.minus i = plus.minus i (2 v + 1) \
$

$
                              (sigma rho)' & = tau rho \
  (sigma' - tilde(gamma)) rho + sigma rho' & = 0 \
       minus.plus 2(i z + v) rho + z rho ' & = 0 \
                               (ln (rho))' & = plus.minus 2(i + v/z) \
                                       rho & = z^(plus.minus 2 v) e^(plus.minus 2 i z) \
$

$
                lambda + n tilde(gamma)' + 1/2 n(n-1) sigma'' & = 0 \
  lambda plus.minus n 2i = plus.minus i(2v+1) plus.minus n 2i & = 0 \
                                                            n & = - v - 1/2 \
$

$
  y_n (z) = C_n/(rho) (d/(d z))^n (rho sigma^n) \
  u_v (z) = phi.alt y_n (z) = C_n z^(minus.plus v) e^(minus.plus i z) (d/(d z))^(-v -1/2) (z^(plus.minus 2 v -v -1/2) e^(plus.minus 2 i z))
$

Which can't be expressed in common polynomial due to the fractional differentiation, that's why many text book omit this. However, if, for $v -> v + 1/2$, we has a primitive expression for Those Bessel basis, like:

$
  u_(-1/2) (z) = C_(-1/2) z^(-1/2) e^(plus.minus i z)
$

We know:
$
  v(r,phi) & = u_n (r) e^(i n phi) \
   u_n (r) & = 1/(2 pi) integral_(-pi)^(pi) v(r,phi) e^(- i n phi) d phi
$

For simplest solution $v(r,phi) = e^(i k r sin phi)$:
$
  u_n (r) = 1/(2 pi) integral_(-pi)^(pi) e^(i r sin phi - i n phi) d phi \
$

Must be Bessel equation of order $n$, we denote such term directly as normalization called $J_n (r)$.

Then we can extend it into analytic contour, from $[-pi,pi]$ to $[pi,pi - i infinity)]$, $[-pi - i infinity, -pi]$, we omit the infinity term because it decays to zero.
$
  u_v (z) = 1/(2 pi) integral_C e^(i z sin phi - i v phi) d phi = 0 \
$

Thus, we choose $[pi,pi-i infinity]$ contour as $H^(1)_v$, same for another as $H^(2)_(v)$. A inspection of shift $pi$ will yielding the relation of $v <-> -v$ for the $[pi, pi-i infinity]$.

$
  1/(2 pi) integral_(L + pi) e^(-i z sin phi' + i v (phi' + pi)) d phi' = H_v (z) e^(i v pi) = H_(-v) (z)
$
Where the shift of $pi$ doesn't effect the imaginary integral, and negative sign is cancelled after parametrization $phi -> - phi$.

$
  J_v (z) + H_v^(1)(z) + H_v^(2)(z) = 0 \
  J_v = - (H_v^(1) + H_v^(2)) \
$
However, sometimes one said that $1/pi (...) = H^(1)$ with negative factor as:
$
  J_v = 1/2 (H_v^(1) + H_v^(2)) \
  e^(i z sin phi) = sum_(-infinity)^(infinity) J_n (z) e^(i n phi)
$

Sometimes, because we take real value on $J_v$, we has same, imaginary part as:

$
  Y_v = 1/(2 i) (H_v^1 - H_v^2) \
$

For cylindrical coordinates, indeed you will find we construct $J_n$ for specific $n$ in Laplace $nabla^2 v = 0$ just as spherical case, unless we choose $nabla^2 v = lambda v$ will construct the whole $J_n$ basis, which is plane wave.

Generating function is suitable to deduce induction relation, but it's not useful in contemporary practise, however, Bessel equation has a shift property worth mention.

$
  (partial G(z,phi))/(partial z) & = i sin phi G(z,phi) = sum_(-infinity)^(infinity) J'_n (z) e^(i n phi) \
                       i sin phi & = (e^(i phi) - e^(-i phi))/2 \
                        J'_n (z) & = 1/2 (J_(n-1) (z) - J_(n+1) (z)) \
$

$
  (partial G(z,phi))/(partial phi) & = i z cos phi G(z,phi) = sum_(-infinity)^(infinity) i n J_n (z) e^(i n phi) \
                         i cos phi & = i ((e^(i phi) + e^(-i phi))/2) \
                       n/z J_n (z) & = 1/2 (J_(n-1) (z) + J_(n+1) (z))
$

If you are astute enough to inspect the shift property already seen in $x partial$:
$
  x partial (x^n y) = x^n (n + x partial) y \
$
We sum the two equation above:
$
  1/z z^(1-n) partial (z^n J_n (z)) = J_(n-1) (z) \
  1/z partial(z^n J_n (z)) = z^(n-1) J_(n-1) (z) \
$
Same, we can acquire for $-n$:
$
  - 1/z partial(z^(-n) J_n (z)) = z^(-(n+1)) J_(n+1) (z)
$

Which is a pleasant deduction form, then for half integer part, it can be written as:

$
  H^(1,2)_(n-1/2) (z) & = C_n z^(-1/2 + n) (-1/z d/(d z))^n e^(plus.minus i z) \
        J_(n-1/2) (z) & = (...) cos z \
        Y_(n-1/2) (z) & = (...) sin z \
$

#import "../lib.typ": *
#import fletcher: diagram, node, edge
#import theorion: *

#show: daily-en.with(
  title: "Homology",
  eq-numbering: "(1.1)",
  eq-chapterwise: true,
)

#show: show-theorion

= Presheaves

== Yoneda embedding

#definition[][
  Let $A$ be a category. A _presheaf_ on $A$ is a functor
  $X: A^(op) -> "Set"$. For an object $a$ of $A$, write $X_a = X(a)$ for
  the fibre of $X$ at $a$.

  A morphism $u: a -> b$ induces the restriction map

  $
    u^* = X(u): X_b -> X_a.
  $

  A morphism of presheaves $f: X -> Y$ is a natural transformation. Its
  component maps $f_a: X_a -> Y_a$ make the following square commute for
  every $u: a -> b$:

  $
    #diagram[$
      X_a edge("->", f_a) & Y_a \
      X_b edge("->", f_b) edge("u", "->", u^*) & Y_b edge("u", "->", u^*)
    $]
  $

  Equivalently, $f_a u^* = u^* f_b$. Presheaves on $A$ and their natural
  transformations form the category $hat(A)$.
]

#definition[][
	Yoneda embedding
	$
		h: A -> hat(A), quad h_a = hom_A (-,a)
	$
]

#theorem[][
  For any presheaf $X$ on $A$, there is a natural bijection

  $
    hom_(hat(A)) (h_a, X) ->^~ X_a \
    (h_a ->^u X) |-> u_a (1_a).
  $

  For each morphism $u: c -> a$ and section $s in X_a$, define
  $f_c(u) = u^*(s)$. These maps are the components of a natural
  transformation $f: h_a -> X$.
]


= Abelian categories

== Additive and Abelian structure

#theorem[][
	Let $cal(A)$ be a category. We say that $A$ is additive if:
	- $forall A,B in cal(A)$, _$hom(A,B)$_ has the structure of an Abelian group, in such a way the composition is additive.
	- Therefore, particular the set _$hom(A,b)$_ is not empty as it contains the $0$ element. Which is terminal and initial for $cal(A)$ unique up to isomorphism.
	A consequence of this is that the identity $id_0$ is the only element of _$hom_(cal(A)) (0,0)$_.
	- In $cal(A)$, there exists binary products and coproducts.
]

Fix two objects $A,B in cal(A)$, consider projection and inclusion maps $p_((-))$, $i_((-))$. Then $(id_A,0)$ and $(id_B,0)$

#theorem[][
	Let $f: A -> B$ be a morphism in an	additive category. The _kernel_ of $f$, denoted as _$ker f$_ is the equalizer of $f$ and $0$. So does _$"coker" f$_ as coequalizer of $f$ and $0$.
]

#proposition[][
	Let $cal(A)$ be an additive category, $f: A->B$ a morphism. Let $F: cal(A) -> #[_Ab_]$ be a functor defined by:
	_$
		F(X) = ker (hom(X,A) -> hom(X,B))
	$_
]

Let $K = ker f$, fitting in universal diagram:

$
	#diagram[$
		K edge("->",k) & A edge("->",f) & B
	$]
$
Then for $X in cal(A)$, the composition of homomoprhism:

$
	#diagram[$
		hom(X,K) edge("->",k compose -) & hom(X,A) edge("->",f compose -) & hom(X,B)
	$]
$

Is indeed $0$. Which means $hom(X,K)$ is the kernel or $F tilde.equiv h_K$ .

#definition[][
	Let $cal(A)$ be an additive category. We say that $cal(A)$ is an _Abelian category_ if $cal(A)$ admits kernels and cokernels that identify the isomorphism on image and coimage.
]

$
	#diagram[$
		K edge("->",k) & A edge("->",f_1) & I edge("->", f_2) & B edge("->", l) & L
	$]
$

$
	#diagram[$
		0 edge("->") & ker f_k edge("->") & A_k edge("->") & im f_k edge("->") & 0
	$]
$

$
	#diagram[$
		0 edge("->") & A edge("->",i_A) & A plus.o B edge("->",p_B) & B edge("->") & 0
	$]
$

#proposition[][
	Let $cal(A)$ be an Abelian category, $X in cal(A)$, The functors $h_X$ and $h^X$ (with target _Ab_) are both left exact.
]

#proof[
	$
		#diagram[$
			0 edge("->") & A edge("->",f) & B edge("->",g) & C edge("->") & 0
		$]
	$

	Be any short exact sequence. So every morphism $h : X -> B$ such that $g compose h = 0$ factors through $A$. Therefore:
	$
		#text(9pt)[#diagram[$
			0 edge("->") & hom(X,A) edge("->") & hom(X,B) edge("->") & hom(X,C) edge("->") & 0
		$]]
	$
]

== Subobjects

Given two objects $u: U -> A$ and $v: V -> A$ of $A$, if there's a morphism $f:U -> V$ such that $u = v compose f$, then $u$ is factored through $v$ and $u$ is monomorphism indicates $f$ is monomorphism too. so $U$ is a subobject of $V$. We will abuse notation and write $U subset V$.

#lemma[][
	$
		#diagram[$
			U edge("->",f) & V edge("->", g) & U edge("->", u) & A
		$]
	$

	Let $A$ be an object of an Abelian category. Then $U,V$ as subobjects that $f: U -> V$ and $g: V -> U$ are such that $u = v compose f$ and $v = u compose g$, then above chain is enough shows that $u = v compose f = u compose g compose f$. $g compose f$ is also monomorphism, shows isomorphism.
]

Intersection $(inter)$ as pullback, for subbojects $u: U -> A$ and $v: V -> A$:

$
	#diagram[$
		U inter V edge("->", p_2) edge("d","->",p_1) & V edge("d","->",v) \
		U edge("->",u) & A
	$]
$

If $K -> U inter V$ is such that $K -> A$ is zero, then $K -> U -> A$ is zero. Since $u$ is mono, $K -> U$ must be zero. By the same logic for $V$, the universal property of the pullback forces the unique map $K -> U inter V$ is zero. Thus $U inter V -> A$ is a monomorphism.

Sum $(+)$ as a coimage, the sum $U + V$ is the image of the coproduct map by factor $U plus.o V ->^e I ->^m A$. Where $e$ is epi and $m$ is a mono. We define $U + V ：= I$ is the smallest suboject of $A$ through which both $u$ and $v$ factor.

A morphism $f: A -> B$ determines functors $f_*: "Sub" (A) -> "Sub" (B)$ and $f^*: "Sub" (B) -> "Sub" (A)$ given by direct and inverse image respectively.

$
	f_* (U) subset.eq V <=> U subset.eq f^* (V)
$

For a subobject $V ->^j B$, $f^(-1) (V)$ is the pullback of $j$ along $f$. Because $V -> B$ is monomorphim, $f^(-1) (V) -> A$ is a monomorphism. Then $U -> A$ factors through $f^(-1) (V)$, then $f (U)$ must factor through $V$. Reversely, $U ->^i A$, $f(U)$ is the image of composition $f compose i$.

Assume $f$ is mono, then for any suboject $i: U -> A$ the composition $f compose i$ is mono too.

$
	#diagram[$
		P edge("->") edge("d","->",j) & U edge("d","->", f compose i) \
		A edge("->",f) & B
	$]
$

The pullback $f^(-1) (f compose i) (U)$ retain the monomorphism and the whole diagram commutative.

$
	#diagram[$
		A edge("->",a) edge("d","->",alpha) & B edge("->",b) edge("d","->",beta) & C edge("->",c) edge("d","->",gamma) & D edge("d","->",delta) \
		A' edge("->",a') & B' edge("->",b') & C' edge("->",c') & D'
	$]
$

= Chain complexes and homology

Let $cal(A)$ be an Abelian category.

#definition[][
	The category of complexes _$"Kom"(cal(A))$_ has for objects doubly infinite complexes of objects in $cal(A)$:
	$
		#diagram[$
			dots edge("->") & A_(n-1) edge("->") & A_n edge("->") & A_(n+1) edge("->") & dots
		$]
	$
]

$
	H_n (A_circle.filled.small) := (ker A_n -> A_(n+1))/(im A_(n-1) -> A_(n))
$

If $H_n (A_circle.filled.small) = 0$ for all $n$, we say that $A_circle.filled.small$ is acyclic.

It's common to denote $B_n = im (A_(n-1) -> A_n)$ for boundary and $Z_n = ker(A_n -> A_(n+1))$ for cycle. Then $B_n$ is a subobject of $Z_n$ and $H_n (A_circle.small.filled) = Z_n \/ B_n$.

$
	#diagram[$
		0 edge("->") & A edge("->") & B edge("->") & C edge("->") & 0
	$]
$

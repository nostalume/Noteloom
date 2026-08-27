#import "../lib.typ": *
// utils functions
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

// Mine infos
#let abstract = {
  "本论文旨在深入探讨李群理论在分析力学中的应用,尤其关注其在对称性和不变量分析中的核心作用.论文首先介绍了流形和李群的基本概念及其在物理学中描述构型空间与对称变换的必要性.在此基础上,我们详细分析了伽利略群的结构及其李代数,并结合拉格朗日分析力学和诺特定理,证明了伽利略不变性所导致的动量,能量等守恒量的存在,以及非相对论动能形式的内在联系.随后,论文进一步阐述了Euler-Poincaré定理,该定理通过将动力学方程从传统的构型空间约化到李代数空间,极大地简化了处理具有李群对称性的系统.最后,我们将Euler-Poincaré应用于旋转群的框架下,成功推导并分析了刚体转动的欧拉运动方程.从而展示了李群与流形理论在揭示复杂动力学系统深层对称性和简化方程方面的强大能力."
}

#let keywords = ("李群", "伽利略群", "李代数", "诺特定理", "拉格朗日力学")

#show: mine.with(
  template: "am-zh",
  lang: "zh",
  title: "基于李群的伽利略不变性与刚体转动动力学研究",
  abstract: abstract,
  keywords: keywords,
)

#set super(typographic: false)

= 导言

我们已经了解Euler-Lagrange等式的形式等价于对于Lagrange作用量泛函的静态变分,即对于如下结构,由Hamilton原理给出$delta S = 0$:
$
  S[q] := integral L(q(t),dot(q)(t)) d t
$
实际上,由于变分的任意性,我们了解到运动轨迹的变化随任意坐标的变化而变化却不影响最终的动力学结果.这也意味着,对于任意作用量的变分是不随坐标的变换而改变的,即Hamilton原理包含了*坐标不变性*@holm_geometric_nodate[p~26],Lagrange作用量是比坐标的表示形式更为基础的代数对象.

给予初始的演化参数$q_i (0), dot(q)_i (0)$,动力学的演化告诉我们坐标依照特定的约束轨迹行进,因而$bb(R)^3$空间下,即使我们没有流形的知识,直觉告诉我们,其约束的空间则是一个在其空间下的平面或者说子空间,质点的运动轨迹是一个可以用一定约束坐标描述的曲线.

基础的坐标变换知识告诉我们,任意的曲线轨迹所在的邻域下所在的空间存在的函数$f(x_1,...,x_n)$具有其各个方向的变化@tu_differential_2017[p~22],等价于:
$
  x^i & = p^i + t a^i \
$
$
  D f & = lim_(t->0)(f(p+t a) - f(p)) / t \
      & = d / (d t)|_(t=0)f(p+t a) \
      & = sum (partial f) / (partial x^i)|_p (d x^i) / (d t)|_(t=0) = sum (partial f) / (partial x^i)|_p a^i \
$

我们知道任意坐标的变化的参数$a^i$是任意的,函数$f$也是任意的,但是求导的形式却是确定的.我们尝试抽象结构,邻域的所在的空间结构不会变化,只要我们既定坐标,我们都存在$(partial) / (partial x^i)$,不仅如此,它的形式仅随我们对此邻域的坐标表述变化而变化,而不随邻域的变化而变化.我们可以将其抽象为$bb(R)^n$下的线性空间,称其为关于点$p$的$T_p (M)$切空间. 若线性空间成立,则必然存在对应的对偶空间即类似于$v_j ((partial) / (partial x^i)) = delta_(i j)$的结构存在.幸运的是,我们已经知道了,即$d x^i^* : d x^i^*((partial) / (partial x^i)) = (partial) / (partial x^i)(d x^i) = 1$. 于此,我们可以定义内积,即对于任意既定的基向量$bold(x) = sum x^i e_i$存在:
$
  inpro(l: e_i, r: e_j) = a_(i j) \
  inpro(l: bold(x), r: bold(y)) = sum_(i j) a_(i j)x^i y^j = sum_(i j)a_(i j) v^i (x)v^j (y) \
$
$
  inpro(l: -, r: -) = sum_(i j) a_(i j) v^i (-) v^j (-)
$
其中$v^i$是对应坐标的对偶映射.如此我们定义了关于该流形每一点上存在的切向量空间,取流形$M$的点$p$,既然定义切空间为$T_p (M)$,其对偶空间便是$T_p^* (M)$.

这时候流形上的Lagrange作用量自然而然也就定义了,其坐标即流形邻域下的坐标@holm_geometric_nodate[p~36].

$
  delta S[q] = lim_(s -> 0) (S[q+delta q]-S[q]) / s = d / (d s)|_(s=0)S[q+delta q] := inpro(l: (delta S) / (delta q), r: delta q)
$
对于我们熟知的正交坐标而言,或者说对于已经正交化的坐标而言,只有对角线也即$a_(i i)$分量.

只要邻域本身同构于$bb(R)^n$,我们永远可以建立局部的坐标系,构建线性空间.我们称这种空间为*流形*.但比起任意的此种空间,在伽利略的年代,我们都知道我们所存在的空间具有速度变换的动力学不变性,这意味着我们的空间存在着对称性,实现各种各样的变换但我们对空间的感知并不会改变.如何从流形的视角理解这一点? 考虑一变换$phi.alt: M -> M$,其中$M$为流形,即使我们目前不了解任何内部信息,我们也知道,这种对称性意味着空间的变换不会损失任何信息,也就是同构. 同时我们知道,同构变换的信息存储于空间中,因为我们没有施加任何超出流形的代数对象.现在我们期望从伽利略的视角出发构建这种特殊的流形及其变换.

在考虑连续的流形之前,离散的视角是值得考虑的.从离散的视角出发,如果我们对一集合$G$的元素进行同构变换,且变换的映射就是离散元素本身,那么我们可以了解到:
$
  g: G -> G \
  g(h) = g h in G quad forall h in G
$
得到了这一集合的代数结构.我们还能再获取什么呢?首先,$g$既是变换也是元素,它具有双重的功能.其次,如果施加多个变换,那么根据映射的结合律,元素本身的作用必然也保持结合律.最后,如果是同构,我们必然存在逆映射$g^(-1)$作用,即$g^(-1)(g) = g^(-1) g = id_G$.其中$id_G$是单位映射,不改变任何信息,因此作为群的元素我们成为单位元. 这样的代数结构我们称为群.

同样,流形的每一点必然附加了同构的映射信息,那么如何表示它呢?注意到邻域本身同构于$bb(R)^n$,则元素必然具有类似于$g: bb(R)^n times bb(R)^n -> bb(R)^n$的同构变换.我们知道这种变换就是*矩阵*,可以拓展到任意线性空间,等价于$g: V -> V$的变换作用.同时,它必然也具有群的代数结构,这种既是流形也是群的代数结构成为*李群*.探究伽利略原理,无非是对具有伽利略变换的群的探究.

= 李群

既然要研究伽利略变换相关的李群,我们首先探究李群本身. 从如上对李群的分析可以看出,李群所具有的元素使得它的表示比一般的流形反而更为具体.我们仍然考虑一运动轨迹$gamma(t) in G$,由于群的作用,我们知道$gamma(s) in G, gamma(t) in G -> gamma(s)gamma(t) = gamma(s+t)$建立了一保持群的映射关系,而保持代数结构的映射被成为*同态*.假如群的结构保存,则单位元必然也保存:$gamma(s-s) = gamma(0) = id_gamma(-) = gamma(s)gamma(-s) = gamma(s)gamma(s)^(-1)$.

$gamma(-): bb(R) -> G$.注意到这一映射并非同构的,因为普遍的群并不具有$g_1 g_2 = g_2 g_1$的交换关系,但因为我们的映射是从一实数的加法群映射到李群,所以是交换的.

普遍的,我们遵从流形的定义对其求导,对时间的求导即对坐标分量的链式求导,但在这里并不需要.
$
  (d ) / (d s)(gamma(s+t)) = (d ) / (d s)(gamma(s) gamma(t)) \
  dot(gamma)(s+t) = dot(gamma)(s)gamma(t) \
$
同时,取$s=0$:
$
  dot(gamma)(t) = dot(gamma)(0)gamma(t) \
$
我们知道$gamma(0)=X$是该流形上的切向量,这定义了一阶常微分方程:
$
  dot(gamma(t)) = X gamma(t) \
  gamma(t) = e^(X t) = sum_i (1) / (n !)(X t)^i
$
在此我们定义矩阵的指数即其级数表达.

我们取旋转群进行验证,我们已经知道对二维平面的旋转无非是一正交矩阵,而它实际上完全的描述了这个流形.我们使用$(d ) / (d t)e^(t X)|_(t=0)$来验证:
$
  (d) / (d t)
  mat(
    cos t, sin t;
    - sin t, cos t
  )|_(t=0) =
  mat(
    0, 1;
    -1, 0;
  )
$

耐心的读者可以尝试反向验证此关系.

$X$是该流形的切向量,意味着该流形的切向量空间$T_(id)(G)$蕴含着流形上的信息. 根据如上定义,$X e^(t X) = e^(t X) X$,这是连乘的交换性，其次,$e^(t X) e^(- t X) = id$.这是$gamma$同态的定义.

值得注意的是一类特殊的群内变换保持了代数结构即同态:
$
  "AD"_g: x -> g x g^(-1) = x' \
$
即它将所有操作元素平移了一元素$g$.这种变换称为*共轭*.
$
  x(h) -> x'(g h) = g x g^(-1) g h = g (x h)
$
平移元素并不改变群本身,这本身就是群的定义的一部分:
$
  "AD"_g (x_1)"AD"_g (x_2) & = g x_1 g^(-1) g x_2 g^(-1) \
                           & = g x_1 x_2 g^(-1) = "AD"_g (x_1 x_2)
$
即同态同构.当然,对于李群亦是如此.同样,我们可以定义关于李群的$"AD"_g$.更重要的是处于其上的切向量:
$
  e^(t g X g^(-1)) = sum_i (1) / (n !)(g X g^(-1))^i t^i \
  (g X g^(-1))^i = g X g^(-1) g X g^(-1) ... = g X^i g^(-1) \
$
则不仅共轭变换对群的元素有效,对群上切向量也有效.则定义:
$
  "Ad"(g)(X) = g X g^(-1) \
$
假若$g = e^(t Y)$, 更近一步我们可以定义群上切向量的关系:
$
  (d ) / (d t)(e^(t Y)X e^(- t Y))|_(t=0) & = e^(t Y)Y X e^(- t Y) - e^(t Y)X Y e^(-t Y)|_(t=0) \
                                          & = Y X - X Y
$
根据如上的分析,它仍然是切向量,即切向量至切向量的映射. 这一发现预示着我们能否如群一样定义其元素的映射关系,答案是肯定的.
$
  [-,-]\/"ad"_(\(-\)) (-): ? -> ? \
  [X,Y] = X Y - Y X = "ad"_(X) (Y) \
  [X + Y, Z] = [X, Z] + [Y, Z] \
$
通常我们称其为交换子.那么既然元素的连乘是不能得到其切向量的元素,仅是交换子操作可以得到,那么我们可以依据矩阵的线性加法和交换子定义其为*李代数*.即包含加法与作为交换子的"乘法".

最后我们考虑一类李代数即旋转群,旋转群的定义可直接从矩阵中方便获得,即$det(A) = 1$且$A^(T)A = 1$.实际上这两个约束无非表明该矩阵的基向量是正交且归一的.其中$A = e^(t X)^T = sum_i (...)^T = e^(t X^T)$.
$
  e^(t X)e^(t X)^T = 1 \
$
求导并取$t=0$时刻的切向量:
$
  e^(t X) X e^(t X^T) + e^(t X) X^T e^(t X^T) = 0 \
  X + X^T = 0 \
  X = -X^T
$
此类矩阵被成为反对称矩阵.

我们称三维的旋转群为$S O (3)$,其李代数为$frak(s o)(3)$.根据基本的定义,即作为$bb(R)^n$的线性变换$R v$,其李代数依然如此是一线性变换:
$
  mat(
    0, omega_3, -omega_2;
    - omega_3, 0, omega_1;
    omega_2, -omega_1, 0;
  )
  mat(
    x_1;
    x_2;
    x_3
  )
  -> hat(omega) times bold(x)
$
注意左边的运算即为右边的叉乘运算,其中$hat(omega) = (omega_1,omega_2,omega_3)$. 这种一一对应的关系使我们可以定义一同构映射，其中的代数运算关系仍然被保持,所以是同态$frak(s o)(3) -> (R^3, times)$定义了叉乘本身.

我们可以将此种映射理解为叉乘的一种定义,同时我们知道叉乘仅能在$bb(R)^3$获得定义,这是因为三维的反对称矩阵具有$n(n-1) / 2 |_(n=3) = 3$个变量的原因,在此之外我们无法定义叉乘.

= 伽利略群

伽利略通过其思想实验确定了基本的相对性原则,即我们无法区分一恒定速度差异下参考系的动力学的演化,同时,这一思想实验同样确定了,动力学的演化与时间,方向,参考位置无关.我们需要更进一步区分这几点,我们能够观察到的动力学参量是位置与速度,实际上这一点隐含了其所处的时间和参考方向,其由我们所处的参考系决定.如果这些参量形成了群,其必然包含相关的信息即元素本身,而这些参量的变化必然是元素的叠加,我们继续伽利略的思想实验来分析各个元素的相互关系.

对于动力学演化的观察,不依赖我们从何时计时与位置选取,无论从多远的地方还是何时计时,其演化相同.这表明伽利略群具有时空平移的作用.我们所处的三维空间,不论选择任意的坐标轴都不影响动力学演化,这表明旋转作用.最终是伽利略原则对恒定速度的观察,即速度叠加不影响动力学演化,这表明的是伽利略提升(Galilean boost)作用.

我们抽象这些作用形式,即代表旋转空间$S O(3)$的矩阵$O$;时空平移的矢量$(bold(r),t)$;以及恒定速度$bold(v)$.我们的物理直观告诉我们,时空平移的变换并不由顺序决定,即加法的交换性$(bold(r) + bold(r)_1 + bold(r)_2, t + t_1 + t_2) = g_(r_1,t_1) g_(r_2,t_2) (g_(r,t)) = g_(r_2,t_2)g_(r_1,t_1)(g_(r,t))$;提升操作仍为加法,但不仅是速度的叠加,我们的空间也因为速度的叠加而平移了:$(id_r, id_t, v')(r,t,v) = (r+ v't, t, v' + v)$;而旋转的操作显然并非交换,当我们操作李群$S O(3)$时矩阵的乘法并非交换 @holm_part_2011[p~14].

我们再来看看更有趣的组合,当我们先旋转再平移空间时:$r ->^O O r ->^(r_1) O r + a$. 此时的空间平移是在旋转的参考系下描述的;而反之则:$r ->^(r_1) r+r_1 ->^O O(r + r_1)$.同样,速度也是如此,它也会被旋转.这意味着各个操作之间并非独立,也即可交换的.现在我们确定一下影响顺序,旋转操作改变提升和平移,而提升操作仅改变平移,平移操作独立.粗浅的描述类似于$O > v > (r,t)$.

既然如此我们优先考虑时空平移的作用. 时空平移的作用,无非是$bold(r) + b$的叠加操作.既然其是李群,必然能表达为矩阵形式:
$
  bold(r) + bold(b) = I bold(r) + bold(b) 1 = g_b mat(bold(r); 1) \
$
如何分析矩阵的分量? 我们进行拆分:
$
  mat(
    A = I, ?;
    ?, ?
  )
  mat(
    bold(r);
    1
  ) =
  mat(
    bold(r) + bold(b);
    1
  )
$
实际上这无非是右上对角的混合作用改变了其独立性,使得操作混合:
$
  g_b = mat(
    I, bold(b);
    0, 1
  )
$
同样的,我们以相同操作分析提升:
$
  mat(
    bold(r) + bold(b) + v t;
    t + t_0;
  ) =
  mat(
    I bold(r) + bold(b) 1 + v t;
    1 t + t_0 1
  ) =
  g_(b,v,t_0) mat(
    bold(r);
    t;
    1
  )
$
之前的分析告诉我们$1$的作用是最后额外的哑分量带来的线性叠加.
$
  mat(
    I, ?, ?;
    ?, ?, ?;
    0, 0, 1;
  ) mat(
    bold(r);
    t;
    1
  )
$

而根据如上的比较,我们得出:
$
  g_(b,v,t_0) = mat(
    I, v, bold(b);
    0, 1, t_0;
    0, 0, 1
  )
$
对角线保持了原分量,而右上分量是与哑分量或者和$t$所带来的混合作用.

这提醒我们,这是否是一种普遍的构造形式,我们知道取一组独立元素$(g_1,h_1) -> (g g_1, h h_1)$互不干扰组成了独立的群. 而不一样的是$(g_1, h_1) -> (g alpha_(h)(g_1), h h_1)$, 假设一同态映射$alpha_(\(-\))(-): H times G -> G$ 通过作用改变了左边元素的操作,此时左边元素的结构不再独立.我们称这种操作为*半直积*.显然这种操作并不对称,左边的元素被右边所影响,这就是我们在如上处理时,并未改变$(r,t) <-> (t, r)$的顺序,否则矩阵的形式会倒转.我们定义该操作为$G times.r_(alpha) H$.而如上的分析就是矩阵表示中半直积的定义表示.注意其逆元应当是$g alpha_h (g_1) = id_g$,$h h_1 = id_h$.因为$h = h_1^(-1)$,则$g = alpha_(h^(-1))(g_1^(-1)) = alpha_(h')^(-1)(g_1)$. $(g',h')(g,h)(alpha_(h')^(-1)(g'),h'^(-1)) = (g' alpha_h'(g), h'h)(alpha_(h')^(-1)(g'),h'^(-1)) = (g'alpha_h' (g) alpha_(h'h)(alpha_h'^(-1)(g')),h'h h'^(-1)) = (g' alpha_h' (g) alpha_(h' h h'^(-1)) (g'^(-1)), h' h h'^(-1))$. 取$h = id_h$可以看出$G$在共轭下仍是其内部元素,即$(G,id_h)$.但是我们会发现$g = id_g$是$H$在共轭下出现了$G$的相关元素,这意味着$H$对$G$的作用改变了其自身的独立性.


现在我们仅剩旋转群,那么根据其作用的权重,旋转作用改变提升和平移.实际上我们已经得到了其结果,那就是将$I <-> O$得到最终的伽利略群的表达.值得注意的是,寻常的仿射变换$A x + b$无非是$V times.r G L(n, bb(R))$,即一线性空间作为平移与一线性变换群的半直积.这也是如上推导的结果.

我们定义三维的伽利略群为$G a l(3)$.根据如上分析得到:$G a l(3) tilde.equiv (bb(R)^4times.r bb(R)^3) times.r S O(3)$.半直积操作不具备结合律,所以我们必须指定嵌套的顺序,即对应的同态映射.

可以看出简单的分析实际上包含丰富的数学结构.我们终于可以尝试对群的切空间进行处理了.

首先,我们仍然考虑单位元处的切空间,单位元意味着其作用不变,显然在矩阵中为单位矩阵.同时,任意的元素$g(s)|_(s=0) = id_g$,每个分量由$t$参量描述.那么切空间$T_(id)(G(3))$必然是:

$
  dot(g)(s)|_(s=0) = X g(s)|_(s=0) -> X = g^(-1)(s)dot(g)(s)|_(s=0)
$

我们首先知道,想要弥合多个半直积的影响,则群的逆需要各个分量一步步相反操作@holm_geometric_nodate[p~18]:
$
  g^(-1) = mat(
    [O^(-1) = O^T], - O^T v, - O^T (r - v t);
    0, 1, -t;
    0, 0, 1
  )
$
然后进行计算,注意$g(s)$在参量$s=0$时必然回归单位元即单位矩阵.
$
  Xi = mat(
    omega, v', r';
    0, 0, t';
    0, 0, 0
  )
$
其中使用$(...)'$表明对其的微分.值得注意的是这些微分是对参量$s$而非时间的微分,它们只能表明无限小的生成元而非动力学项.

现在我们来计算$"Ad"_tilde(g) (Xi)$:
$
  "Ad"_tilde(g) (Xi) =
  mat(
    "Ad"_tilde(O) omega; -"Ad"_tilde(O)(omega) tilde(v)+ tilde(O) v'; -"Ad"_(tilde(O))(omega)(tilde(r)-tilde(v)tilde(t)) - tilde(O)v' tilde(t) + tilde(O)r' + tilde(v)t';
    0, 0, t';
    0, 0, 0
  )
$
鉴于第一行过长采取了竖直的排列.我们可以看见,这一共轭实际上给出了在另一参考系下对该切空间,或者说无限小生成元的观测结果.我们可以看到第二项中类似科氏力的无限小速度位移.以及第三项中$hat(omega) times r$带来的无限小空间位移. 但是这并非完全的粒子运动的描述,它仅是对于该空间具有的运动性质的变换的描述.

同理我们可以计算$"ad"_(Xi_1) Xi_2$:
$
  [Xi_1,Xi_2] = mat(
    [omega_1,omega_2]; omega_1 v'_2 - omega_2 v'_1; omega_1 r'_2 - omega_2 r'_1 + v'_1 t'_2 - v'_2 t'_1;
    0, 0, 0;
    0, 0, 0,
  )
$
它描述了两运动形式的微分差距, 值得注意的是第一项

$
  [omega_1, omega_2]v & = hat(omega)_1 times (hat(omega)_2 times v) - hat(omega)_2 times (hat(omega)_1 times v) \
                      & = hat(omega)_2(hat(omega)_1 dot v) - v (hat(omega)_2 dot hat(omega)_1) \
                      & -(hat(omega)_1 (hat(omega)_2 dot v) - v(hat(omega)_2 dot hat(omega)_1)) \
                      & = (hat(omega)_1 times hat(omega)_2) times v
$

它实际上正是不同次序的转动形成的微分差距.同样,我们可以看到提升的差距,即$v'_1 t'_2 - v'_2 t'_1$,假设相同的时间增量则该项消失.


= 群,流形,作用量

我们知道,群的作用不论如何是不会影响作用量的最终效果的,只是对于我目前的我们来说,如何影响和效果是未知的.如何抽象化群对某一对象的作用呢?这一点的关键在于群本身是对自己的作用,那么对于离散群来说,群对自己的作用等价于对自己集合的作用,这是等价的.同样,李群对于自己的作用等价于对自己所在流形的作用.假如所作用的集合或者流形并非自己,它的作用必然存在一定的缺失,或者重复.可以抽象化这种重复吗?这种不变量就应该等效于作用量的群作用不变性.

我们可以定义简单的左作用或者右作用,例如对于群$G$与流形$M$,$Phi: G times M -> M$.这一作用本身必然如同对于自己的作用一样,保存了群的结构,也即同态.那么结合律,单位元必然也存在.无需累赘.

$
  Phi(id, x) = x quad x in M \
  Phi(g thin Phi(h, x)) = Phi(g h, x)
$

所以我们简化为$g dot x$.方便描述.

例如$S O(2) times bb(R)^2 -> bb(R)^2$:
$
  mat(
    cos theta, -sin theta;
    sin theta, cos theta;
  )
  mat(
    x;
    y;
  ) -> mat(
    x cos theta - y sin theta;
    x sin theta + y cos theta;
  )
$
可以观察到除去$vec(0, 0)$以外,其他的点必然被旋转地映射到另一点.那么我们挖去这一点所对应的空间,即$bb(R)^2 \/ vec(0, 0)$,构成了我们期望的无信息损失的旋转作用. 假设我们更近一步,考虑其模为$1$的向量.那么我们直接还原至$vec(cos alpha, sin alpha)$,构成了旋转群的映射空间.这直接等价于$S O(2)$对自己的映射,也即群自身.那么$S^1 tilde.equiv {||v|| =1 | v in bb(R)^2 } tilde.equiv S O (2)$.

我们现在需要知道Lagrange作用量所处的流形空间是什么,不过我们往往先从局部入手.对于一点邻域形成的局部坐标系$(q_1, ..., q_n)$构成了对流形$Q$的局部描述.但是我们还差一点,因为我们还需要知道$(dot(q)_1,...,dot(q)_n)$来完整的描述Lagrange作用量.这意味着它所处的流形空间并非单纯的流形,而是由其上所处的切空间共同构建而成 @tu_differential_2017[p~51]:
$
  T Q = { (q, dot(q)) | q in Q, dot(q) in T_p Q}
$
构成了切丛.

其中对于任意流形映射来说$f: Q -> Q'$:
$
  f_*(q, dot(q)) = (f(q), f_(*,p)(dot(q)))
$
如何理解这一映射结构? 我们考虑一群作用来尝试:
$
  #let dq = $bold(dot(q))$
  dq = dot(q)^i (partial ) / (partial q^i) -> T_q (g dot q) = T_q (tilde(q)) = (partial tilde(q)^j) / (partial q^i) -> tilde(dot(q)) = dot(q)^i (partial tilde(q)^j) / (partial q^i) (partial) / (partial tilde(q)^j)
$
即:
$
  g_(*,q) dot dot(q) = dot(q)^i (partial tilde(q)^j) / (partial q^i)
$
可以看出这无非是求导的雅可比变换.既然是链式法则,那么多个元素作用的结合律实际上仍是满足的.

现在我们考虑一无穷小元素的作用,注意,是群的无穷小作用.此时我们用参量$s$表达对其的微分,同样的,矩阵变换的结果是相同的,我们使用$D(...)$来表明非分量的形式:
$
  X dot q = (d) / (d t)|_(t=0) e^(t X) dot q \
  X_(*,q) dot dot(q) = D(X dot q) dot bold(dot(q))
$

同样的,我们还存在对于对偶空间的变换,如果我们的度量是良定义的,首先我们的变换对于左右两边必然等价,且对于对偶空间的作用必然应当抵消对于空间的作用,使其不变.这必然给出了一余切丛的定义,其切空间无非转换成余切空间.

我们取$g_(...)^*$表明余切空间的作用.
$
  inpro(l: alpha', r: g_(*,q) v) = inpro(l: alpha, r: v) \
  inpro(l: g'^*_(*,?) alpha, r: g_(*,q) v) = inpro(l: alpha, r: g'_(*,?) g_(*,q) v) \
  g'_(*,?) = g^(-1)_(*,g dot q) \
  g'^*_(*, g dot q) = g^(*,-1)_(*,g dot q)
$
值得注意的是,该点必然抵消已经被$g$作用的点,而非$q$本身.值得注意的是,具体的形式下我们注意到:
$
  ((partial tilde(q)^j)/(partial q^i))^(-1) = (partial q^i)/(partial tilde(q)^j) = (...)^T
$

同样,因为作用群本身所在的逆也转换成$e^(-t X)$,携带一负号.所以无限小提升的结果仅仅只是原无限小元素的:
$
  X_(*,g dot q) dot dot(q) = - D(X dot q)^T dot bold(dot(q))
$

现在让我们尝试对Lagrange进行变分.此时变分的操作不再是任意的,而是由一参数$s$在李群上的轨迹形成的微小变分组成:
#let tit = $tilde(t)$
#let tiq = $tilde(q)$
$
  {t, q} -> {tilde(t)(t,q,s), tilde(q)(t,q,s)} \
$
$
  tau(t, q) = (d)/(d s)|_(s=0)tilde(t)(t,q,s) \
  xi^alpha (t,q) = (d)/(d s)|_(s=0) tilde(q)^alpha (t,q,s)
$
这给出了如下的微小展开:
$
  tit = t + s tau(t, q) quad tiq^alpha = q^alpha + s xi^alpha (t,q)
$

$
  (d tiq^alpha)/(d tit) = d(q^alpha + s xi^alpha)/(d t) (d t)/(d (t + s tau)) = dot(q)^alpha + s (xi^alpha - dot(q)^alpha dot(tau))
$
忽略$O(s^2)$以展开至一阶,对生成元的时间微分实际上是对其变量的全微分.

所以,此时我们标记$q$的全变分为$D q = delta q + dot(q) delta t$,在下面的计算中我们不带入具体对象,而仅是全变分.

#let Ldt = $(partial L)/(partial t)$
#let qdt = $dot(q)^alpha$
#let Ldq = $(partial L)/(partial q^alpha)$
#let Ldqdt = $(partial L)/(partial qdt)$
#let Ldqqdt = $(partial^2 L)/(partial qdt partial dot(q)^beta)$
$
  S'[q',t'] & = integral L(tilde(q),tilde(dot(q))) d tit \
            & = integral L(q,dot(q)) + Ldq D q + Ldqdt (D qdt - delta dot(t)qdt) ((1+delta dot(t))d t) \
$
展开全变分$D dot(q) = delta dot(q) + (d)/(d t)(dot(q) delta t)$并保留一阶变分:
$
  &= integral L(q,dot(q))+ L delta dot(t) + Ldq(delta q^alpha + dot(q)^alpha delta t) + Ldqdt(delta dot(q)^alpha + dot.double(q)^alpha delta t) d t \
  &= integral L(q,dot(q)) + L delta dot(t) + (d)/(d t)(L)delta t + (d)/(d t)(Ldqdt delta q^alpha) d t
$
其中最后一项我们利用的Euler-Lagrange等式.
$
  delta S = integral (d)/(d t)(Ldqdt delta q^alpha+L delta t) d t
$
那么根据变分的Hamilton原理,其内部应当恒为零.这说明,假设具体的Lagrange已经既定,且该变分形式下Lagrange的形式不变.则:
$
  F = Ldqdt delta q^alpha + L delta t
$
为一守恒量,往往称其为*守恒荷*.
假设某一种变分形式中:$D q = 0 -> delta q = - dot(q)delta t$:
$
  F = - Ldqdt dot(q) + L = - H
$
这正是能量的定义,即Hamilton量.当Lagrange作用量的时间变分守恒,则能量作为守恒量.也即时间对称性推导出能量守恒.

现在我们带入原来的变分形式:
$
  delta q = D q - dot(q) delta t = xi - dot(q) tau \
  F = Ldqdt(xi^alpha- dot(q)^alpha tau) + L tau
$
我们在参量$s$的轨迹上作用伽利略群于Lagrange所在的流形.
$
  g(q,dot(q),t) \ -> (O(s)q + t v_0(s) + q_0(s), O(s)dot(q) + v_0(s),t + t_0(s))
$
读者也可以尝试使用矩阵作用,结果相同.
$
  tau = (d t)/(d s)|_(s=0) = t'_0 \
$
$
  xi = (d q)/(d s)|_(s=0) = q'_0 + v'_0t + hat(omega) times q \
$
$
  dot(xi)-dot(q)dot(tau) = (d dot(q))/(d s)|_(s=0) = v'_0 + hat(omega) times dot(q)
$
我们取$(d(...)(s))/(d s)|_(s=0) = (...)'$.

原则上来说,这些作用混合了旋转,平移,提升.我们可以先仅仅关注平移的性质.结合物理的分析我们将得出动能的表达式.

首先,因为作用量在微分平移下不变,粒子的运动作用量必然不包含$q$.且从任意时间观察该运动作用量必然不会变化,则时间变分$delta S|_(delta t) = 0$.这意味着能量守恒,但因为之前我们已经得到过答案,这里我们仅对平移变分.最终$L = K(dot(q))$.

$
  delta q^alpha = q'_0\
  P = Ldqdt q'_0\
$
以及能量:
$
  E = Ldqdt dot(q)^alpha - L \
$
我们先对能量进行时间微分,注意$L=K$仅是关于$dot(q)$的函数:
$
  0 & = Ldqqdt dot(q)^alpha^2 + Ldqdt dot.double(q)^alpha - Ldqdt dot.double(q)^alpha \
    & = Ldqqdt dot(q)^alpha dot.double(q)^beta
$
首先$L$作为标量且二阶导良定义的函数并不会恒为0.$dot(q)^alpha$同样作为切空间分量并不会恒为0.则$dot.double(q)^alpha = 0$.

我们考察$P$,同样的道理可以得到$p_alpha = Ldqdt$是一常矢量.但若二阶导不为零,则必然只能是动量分量的组合:
$
  (d p_alpha)/(d dot(q)^beta) = c_(alpha beta) -> p_alpha = c_(alpha beta) dot(q)^beta
$
$
  Ldqdt & = c_(alpha beta) dot(q)^beta \
      L & = c_(alpha beta) dot(q)^alpha dot(q)^beta
$
这便是动能的表达.我们可以看出这无非是内积的形式.这似乎意味着特定的度规,对应着特定的动能表达.因此它也被称为惯量度规.

另一问题是实际上该形式定义在一般的直角坐标系下的,假若我们转换坐标,那么这也必然产生一非单位度规.最后$dot.double(q) = 0$必然包含该非单位度规.这会给出在特定坐标下的测地线方程.

我们本可以希望这里具有质量的表达,但是我们并没有质量的生成形式,而且从一开始就不存在质量的生成元.这是一个更为奇怪的问题,因为质量从直观上看仅仅只是粒子的性质而非时空的不变性.但现在,它不得不决定我们的度规.

这一问题实际上来源于伽利略群中不封闭的问题,我们展开群的元素$e^(t X)$,其中假设每个单一参数具有对应的切空间分量,则位移$bold(a)$对应的参数为$e^(bold(a) dot bold(s))$.其中$bold(s)$生成了位移,往往称其为位移的生成元,即动量.我们已经从刚才的动量守恒中看到了这一点.

对于提升生成元$x_i - v_i t$,和平移生成元$p_i$,我们采用泊松括号对单一粒子说明这一点:
$
  [x_i - v_i t, p_j] = [x_i, p_j] - t[v_i,p_j] = delta_(i j)
$
其中第二项交换为0.第一项为对应的生成元.我们看到原伽利略群中单纯的交换是不能满足这一特殊的对易关系.它说明伽利略群并不封闭,这是我们缺失的部分.但这一关系实际上需要在Hamilton的代数结构中才能看到.而庞加莱群作为伽利略群的完备并没有这个问题,实际上它将会得到时间平移生成元也即能量的对应部分.这便是质量的关键.

也即质量的部分是无法单纯从群的对称性中完全获得,反而,它在其中仅作为任意规定的度规存在.假设我们想获得进一步的分析则必须引入质量的具体形式.但是我们可以弥补这一点@holm_part_2011[p~45]:
$
  p^alpha = c_(alpha beta) dot(q)^beta = (d)/(d t)(c_(alpha beta)q^beta) \
$
$
  p^alpha t = c_(alpha beta) q^beta
$
假设度规为对角的,或者说对多个粒子的独立描述.
$
  p^alpha t = C q^alpha
$
它描写了该方向上对应的"惯性",而根据各向同性,对单个粒子各个分量的惯性描述相同,我们称其为质量.这一形式由提升不变性获得,它意味着质心守恒.

若粒子轨迹直接由群在时间参量生成,即$q(t) = g(t)q(0)$.
$
  dot(q)(t) = dot(g)(t) q(0) = dot(g) g^(-1)(t) q(t) := cal(L)_(xi_R) q(t)
$
这意味着$tau = 1$,$delta q = 0$.它直接生成坐标构型的动力学演化形式.

其形式是右乘不变的,对任意元素$h$:
$
  dot(g)h(g h)^(-1) = dot(g)h h^(-1) g^(-1) = dot(g) g^(-1)
$
我们称$xi_R = dot(g)g^(-1)(t)$为右不变的速度矢量(right-invariant velocity vector).

假如群的作用反应的是群自身的性质,那么我们应该可以天然的定义群作为流形的拉格朗日量,即群对自身的作用下的不变量.它必然是左或者右乘不变的:
$
  delta integral L(g(t),dot(g)(t)) = 0 \
  g^(-1) delta integral L(g(t),dot(g)(t)) = 0 \
  delta integral L(id_G,g^(-1)dot(g)(t)) = 0
$

这正是$xi_(R\/L)$的来源.它将任意一点的切空间元素即速度拉回至单位元.

方便起见,我们仅考虑左乘不变,忽略下标.我们可以尝试对任意的Lagrange量进行变分.获得其动力学方程,不过因为不变元素的方便表达,我们可以变换坐标让$L(g,dot(g)) -> L(g, g^(-1)dot(g)) = L(g,xi)$.也即$L(g, xi) -> L(g, g xi)$.这称为左平凡坐标(left-trivalized coordinates).

对其元素的变分无非是对矩阵的变分@holm_geometric_nodate[p~224]:
$
  delta xi = delta (g^(-1)dot(g)) = -g^(-1)(delta g)g^(-1)dot(g) + g^(-1)delta dot(g) \
$
这一表达的复杂性来源于变分和时间的混合,它必然是在衡量变分和时间微分的差距.这一原因促使我们尝试倒转顺序:
$
  dot(eta) = (d )/(d t)(g^(-1)delta g) = - g^(-1) dot(g)g^(-1)delta g + g^(-1)delta dot(g) \
$
$
  delta xi - dot(eta) = -g^(-1)(delta g)g^(-1)dot(g) + g^(-1)dot(g)g^(-1)delta g = xi eta - eta xi = [xi, eta]
$
即:
$
  delta xi = dot(xi) + [xi,eta] = dot(xi) + "ad"_(xi)(eta)
$
同样的,因为其元素表达,$delta g = g eta$便是直接定义.
#let Ldg = $(delta L)/(delta g)$
#let Ldxi = $(delta L)/(delta xi)$
$
  & quad integral inpro(l: Ldg, r: delta g) + inpro(l: Ldxi, r: delta xi) d t \
  & = integral inpro(l: Ldg, r: g eta) + inpro(l: Ldxi, r: dot(eta)+"ad"_(xi)eta) \
  & = integral inpro(l: Ldg, r: g_(*,e)eta) + inpro(l: Ldxi, r: dot(eta)) + inpro(l: Ldxi, r: "ad"_(xi)eta) \
  & = integral inpro(l: g^*_(*,e) (Ldg), r: eta) + inpro(l: -(d)/(d t)(Ldxi)+"ad"^*_xi (Ldxi), r: eta) d t
$
即:
$
  (d)/(d t)(Ldxi) = -"ad"^*_(xi) (Ldxi) + g^*_(*,e)(Ldg) \
  dot(g) = xi g
$
称之为Euler-Poincaré约化定理@holm_part_2011[p~226],那么$g = id_G$.第二项消失,这便是寻常的Euler-Poincaré等式.

那么剩下的问题是对偶空间的$"ad"$到底是如何定义的,但实际上原先的分析已经给出了答案,因为群对自己的作用无非是群对流形作用的一个特例,假如$[eta,xi] = "ad"_xi eta$,那么对偶的形式应当类似于$-[eta,xi^T]$,也即原先的$-D(X dot q)^T dot X'~ - D(X)^T dot X' ~ -[X',X^T]$.

我们会注意到因为元素的映射即为矩阵连乘,所以微分形式等于连乘本身,这便是矩阵表达下直接与坐标变换的呼应.

$
  g dot (h, dot(h)) & = (g h, g_(*,h)(dot(h))) \
                    & = (g h, (d)/(d t)(g h(t))|_(t=0)) = (g h, g dot(h))
$

我们来验证一下:
$
  inpro(l: mu, r: [xi,eta]) & = inpro(l: mu, r: xi eta) - inpro(l: mu, r: eta xi) \
                            & = inpro(l: xi^T mu, r: xi) -inpro(l: mu eta^T, r: xi) \
                            & = -inpro(l: [mu,xi^T], r: eta)
$
那么万事俱备,我们将这些构造直接运用至$S O(3)$,它应当给出旋转的动力学演化.

我们对旋转群的切空间已经很熟悉,其元素无非是$omega = O^(-1)dot(O)(t)$.即无限小的旋转元素,但现在是对时间演化的直接描述,也即角速度.其性质是$omega^T = -omega$.

右作用和左作用的角速度的关联是什么呢?
$
  dot(x)(t) = dot(O)(t)x(0) \
  dot(x)(t) = dot(O)(t)O^(-1)x(t) \
$
反之:
$
  O^(-1)dot(x)(t) = O^(-1)dot(O)(t)O^(-1)O x(0) \
  dot(X)(t) = O^(-1)dot(O)(t)x(0)
$
注意,体坐标系的坐标不变而空间坐标系的坐标变化.所以前者是空间坐标系角速度,而后者则是体坐标系角速度.

$
  (d)/(d t)(delta L)/(delta omega) - [(delta L)/(delta omega),omega^T] & = 0 \
    (d)/(d t)(delta L)/(delta omega) + [(delta L)/(delta omega),omega] & = 0 \
$
因为$S O(3)$的切空间等价于一三维欧氏空间附带叉乘的代数结构.我们尝试转化成此表达.其中其内积结构为任意一对称矩阵$inpro(l: hat(omega), r: hat(omega))_II = hat(omega)^T II hat(omega)$.我们知道内积的结构定义了其上元素的自由运动,其良定义蕴含了元素作用不变性这一点:
$
  (delta L)/(delta omega) -> (delta L)/(delta hat(omega)) = II hat(omega)
$
$
  (d)/(d t)(delta L)/(delta omega) + [(delta L)/(delta omega),omega] & = 0 \
             II dot(hat(omega)) + II hat(omega) times hat(omega) = 0
$
这便是Euler运动方程.因为质量的定义必然不包含在群的作用内,我们考虑旋转群对流形的作用,即流形本身具有一度规,其定义为:
$
  m = integral_B rho(x) d^3 x
$
这意味着在一邻域内$"supp"(rho) subset U$定义了类似于$rho(x)|_(x in U) inpro(l: -, r: -)$形式的度规@tu_differential_2017[p~6],因为这实际上是对流形邻域划分(partition)所形成的全局度规.

则$omega times q$的速度生成下所携带的动能形式具有如下表达:
$
  K & = (1)/(2) integral_B rho(x)||omega bold(x)||^2 d^3x \
    & = (1)/(2) integral_B rho(x)||[x] hat(omega)||^2 d^3x \
    & = (1)/(2) integral_B rho(x) ||hat(omega)^T [x]^T [x] hat(omega)|| d^3x \
    & = (1)/(2) hat(omega)^T (integral_B rho(x) [x]^T [x] d^3 x)hat(omega)
$
其中我们使用了:$omega bold(x) = hat(omega) times x = - x times hat(omega) = - [x]hat(omega)$.为了不模糊积分和矢量,暂且使用此区分.

$
  [x]^T [x]v & = - [x][x]v = - bold(x) times (bold(x) times v) \
             & = v(bold(x) dot bold(x)) - bold(x)(bold(x) dot v) \
             & = ||bold(x)||v - bold(x)(bold(x)^T v) \
             & = (||bold(x)|| - bold(x)bold(x)^T)v \
$
这正是$II$作为惯量度规的定义.我们能否定义含时的惯量度规即空间坐标系的惯量度规?这意味着该度规随参数不断变化,这并非一良定义的度规.实际上在经典力学里我们就可以理解这一点,那就是转动惯量在定义时必然选取一刚体的体坐标系进行分解,才能获得其分解项.同样的,关于转动的角动量也只在此时才能与转动惯量存在稳定关系.

假若存在依赖于位置相关或者说并非左乘不变的作用量形式,意味着运动的形式不再自由而是受到限制.例如一转动相关的势能$V(O)$.

$g eta = g_(*,e) dot eta$.即为其左作用.则同样的原因如前文所述它的对偶无非是$g^* eta = g^*_(*,e) dot eta = g^T eta$:
$
  inpro(l: mu, r: g eta) = inpro(l: g^T mu, r: eta)
$
所以:
$
  g^T ((delta L)/(delta g)) = TT
$
那么最终的结果便是:
$
  II dot(hat(omega)) + II hat(omega) times hat(omega) = TT
$
这便是具有约束的Euler运动方程.

= 总结

本论文全面探讨了李群与流形理论在分析力学中的应用,并成功地展示了其在处理具有连续对称性的物理系统时的优越性.通过首先引入流形和李群的基本概念,为后续的动力学分析奠定了坚实的数学基础.对伽利略群的深入分析,结合拉格朗日量和诺特定理,不仅验证了动量和能量守恒的普适性,也揭示了非相对论动能形式与伽利略不变性之间的紧密联系,特别是质量作为中心扩充在动能度规中扮演的角色.最后论文详细阐述了Euler-Poincaré定理的推导及其在动力学演化中的重要意义.该定理使得我们能够将复杂的构型空间动力学转化为李代数上更为简洁的运动方程.


#bibliography("galilean-symmetry.bib", title: "参考文献")

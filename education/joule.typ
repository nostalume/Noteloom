#import "@preview/touying:0.6.1" as touying: *
#import themes.university: *

#set text(font: (
  (name: "Microsoft Sans Serif", covers: "latin-in-cjk"),
  "Microsoft YaHei",
))

#show: university-theme.with(
  aspect-ratio: "16-9",
  // config-common(handout: true),
  config-info(
    title: [焦耳定律],
    subtitle: [微观*透视*下的电热],
    author: [nostalume],
    date: datetime.today(),
    institution: [],
    logo: emoji.leaf,
  ),
  config-page(margin: (top: 2.4em)),
)

#title-slide()

= 冲突

== 生活

#grid(
  columns: 2,
  image("assets/estove.png"),
  [
    #set text(1.2em)
    电流为什么会产生热量？\ \
    定量分析的公式？
  ],
)

== 微观

在无外电场时，最外层的自由电子做无规则热运动，宏观上并不产生定向电流，而产生定向电流意味着：

$
  J = n e v, quad I = J S
$

\

我们假设存在一外电场驱动金属，阳离子同自由电子间被各个方向的作用力*均匀*地吸引着，因而外电场几乎无法直接促使阳离子位移，这种现象是微观的电磁屏蔽。通过自由电子紧密结合的链接方式被称为*金属键*。

= 矛盾

== 电子的定向运动

#[
  #set text(1.2em)
  假如电子在某一方向上做定向移动，我们可知：
  $
    F = E e \
    #pause
    v prop F/m t -> infinity?
  $
  #pause
  我们发现电子的速率将会趋于无穷，那么电流不是*无穷大*吗？
]

== 晶格碰撞

#[
  #set text(1.2em)
  答案是*碰撞*(能量转移）! \ \
  自由电子在同金属阳离子所形成的势场间运动，但是金属阳离子并非真正牢固不动，而是发生振动，同电子间碰撞产生能量交换。 \ \

  *电子加速 -> 撞上晶格 -> 速度归零 -> 再次加速...*
]

== 分析

#grid(
  columns: 2,
  column-gutter: 12pt,
  image("assets/scatter.png"),
  [
    - 电子同阳离子发生碰撞；
    - 电子同电子发生碰撞；
    - 电子同杂质发生碰撞;
    #pause
    \ 
    #set text(1.2em)
    电子的运动受到阻碍！产生*电阻*！
    其中绝大部分热量贡献来自于阳离子振动的传递！
  ],
)

= 数学处理

== 碰撞与平均漂移速度

我们设定$tau$为电子碰撞的*平均*时间间隔, 则碰撞下

$
  m Delta v_d = e E dot tau \
$

#pause

由此电流和电阻为：

$
  J = n e overline(v)_d = (n e^2 tau)/m E = sigma E
$

#pause

$
  P_V = n (e E v_d) = J E
$

#pause

$
  P_V = J^2/sigma = J^2 rho
$

== 电阻率与几何

#align(center)[
  我们由此得到了*电阻*的表达式：
  $
    V = E L = rho J L\
    I = J A \
    R = V/I = rho (L/A) \
  $
  
  #pause
  
  由此宏观的焦耳定律表达式为*单位体积的功率*乘以*体积*：

  $
    P = P_V dot V = ((I/A)^2 R A/L) dot A L = I^2 R
  $
]

= 回顾

== 焦耳定律的适用范围

#[
  #set text(1.2em)
  #set align(center)
  
  实际上对于相当多的电器，焦耳定律并不能用于计算总功率。
  焦耳定律仅仅处理了*热能*的来源。而许多电器将能量转化为了*其他形式*。 
  
  \ \

  例如电灯中电子跃迁释放光子，这部分能量转移*并非*由焦耳定律决定！
]

= 感谢！

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
    title: [楞次定律],
    subtitle: [电磁转换分析],
    author: [nostalume],
    date: datetime.today(),
    institution: [],
    logo: emoji.leaf,
  ),
  config-page(margin: (top: 2.4em)),
)

#title-slide()

= 冲突

== 回顾

*电磁感应定律回顾：*

$
  E = - N (Delta Phi)/(Delta t)
$

#[
  #set text(1.2em)
  #align(center)[电动势的大小与磁通量的变化率呈正比 \
    但公式中的负号意味着什么？它具有什么物理意义？]
]

== 方向的困惑

#grid(
  columns: 2,
  image("assets/magnetic.png"),
  align(center)[
    #set text(1.3em);
    假设一联通电路，其中与一螺线管相连接用以放大电磁感应效应. \ \ 我们如何检验磁铁作用呢？
  ],
)

#align(center)[#set text(1.5em);
  在磁感应强度变化的过程中，产生的电流方向一样吗？它遵循什么*规律*？
]

= 实验与规律

== 寻找统一解释

#image("assets/lenz.png")

我们能否找到一统一的表示方法来解释该现象？

= 定律

== 楞次定律

#[
  #set text(1.2em)
  *感应电流具有这样的方向，即感应电流的磁场总要阻碍引起感应电流的磁通量的变化*
]

#[
  #set par(leading: 3em)
  #pause
  - 阻碍 $!=$ 阻止：是*延缓*变化而不是使其*停止*。 \
  - 变化是针对原磁通量的变化。 \
  #set text(1.5em)
  #pause
  现在我们能否分析原磁通量变化的作用效果？
]

== 分析

#[
  - 判方向: 明确原磁场$B_i$的方向及磁通量$Phi$的增减。

  - 定*阻碍*: 根据*增反减同*确定感应电流的磁场$B_c$方向。

  - $Phi$增加 $->$ $B_i$与$B_c$方向相反

  - $Phi$减少 $->$ $B_i$与$B_c$方向相同 \ \

  - 用安培定则： 根据$B_c$的方向，用右手螺旋定则判定感应电流$I_c$的方向。
]

== 实质

#[

  #grid(
    columns: 2,
    image("assets/magnetic_fallen.png"),
    [
			#text(1.5em)[*能量的转换告诉我们阻碍运动必然使得这部分能量转移*]
       \
			- 如果没有*阻碍*，磁铁会加速下落，动能无限增加，而场并无相互作用。 \ \
			- 正是因为有*阻碍*，我们需要克服安培力做功，这部分机械能就转化成了电路中的*电能*。
		],
  )
]


= 感谢！

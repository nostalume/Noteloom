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
    title: [机械效率],
    subtitle: [省力还是省功？],
    author: [nostalume],
    date: datetime.today(),
    institution: [],
    logo: emoji.leaf,
  ),
  config-page(margin: (top: 2.4em)),
)

#title-slide()

= 冲突

== 情景

- 我们往往在现实中遭遇或遇见搬运重物的情况

#[
  #set text(1.2em)
  #align(center)[
    - 扛着重物从楼梯搬运
    - 使用滑轮器械搬运
  ]
  #set text(1.5em)
  #align(center)[*你会如何选择？* \ #pause \ *省力！* ]
]

== 代价

#[
  #set text(1.5em)
  #align(center)[
    省力，真的*省事*吗？\
    \
    仔细思考，我们的器械具有摩擦和重量...\
    *省事*的力学对应是什么？\
    \
    #pause
    *省功！*
  ]
]

= 功

== 概念

#[
  #set text(1.2em)
  #set par(leading: 3em)

  - *总功*：在运动过程中所需要的全部功。
  - *有用功*：为达目的而不得不做的功。
  - *额外功*：在达成目的以外仍产生的功。
]

我们在搬运重物的时候，直觉*分解*了哪些功？\
有用功和额外功的定义是*自然*的吗?

== 思想实验

*现实中存在完美机械使得*$W_e = 0$?

#pause

#[
  #set text(1.5em)
  *不可能！*
]

- 自重：机械的自重在运动中必须克服。
- 内摩擦： 材料在相互运动中迁移存在的形变/振动耗散。
- 外摩擦： 材料在运动中受到空气阻力，或液体的粘滞阻力。

#[
  #set text(1.5em)
  *热力学第二定律*!
]

== 机械效率

#[
  #set text(1.5em)
  *如何衡量机械的优劣?*
]

#pause

我们希望有用功占比更大，额外功的占比更小... \ \
但是一台器械在不同过程中存在的功的大小是不同的 \
如何得到普遍的不变量呢？

#pause

$
  eta = (W_u/W) times 100%
$

*有用功*占总功的比重越大，比值便越大，而这一数值不与任何具体的有用功的大小相关！

= 感谢！

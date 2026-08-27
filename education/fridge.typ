#import "@preview/touying:0.6.1": *
#import themes.university: *

#set text(font: (
  (name: "Microsoft Sans Serif", covers: "latin-in-cjk"),
  "Microsoft YaHei",
))

#show: university-theme.with(
  aspect-ratio: "16-9",
  footer-a: self => [冰箱工作原理],
  config-common(handout: true),
  config-info(
    title: [电冰箱工作原理揭秘],
    subtitle: [热量转运的现代应用],
    author: [nostalume],
    date: datetime.today(),
    institution: [],
    logo: emoji.leaf,
  ),
  config-page(margin: (top: 2.4em)),
)

#title-slide()

= 原理

== 热学

- 物体在相变时会从周围吸收或释放热量

#[
  #set text(1.5em)
  #align(center)[*我们该如何利用这一点？*]
]

假若我们通过外界手段使:

#[
  #set text(1.2em)
  #align(center)[
    - 液体蒸发为气体吸收热量
    - 气体冷凝为液体释放热量
  ]
]

我们便实现了热量的转移。

== 热学

#[
  #set text(1.5em)
  #align(center)[
    *依据热力学原理,我们不可能在封闭系统下不受外界影响降低其温度！* \
    \
    所以该怎么达到这一点呢？\
    \
    *压缩式制冷循环！*
  ]
]

= 构造

== 循环

#grid(
  columns: 2,
  gutter: 1em,
  image("assets/fridge.png"),
  [
    #set par(leading: 3em)
    - *压缩机:* 压缩气体升温 \
    - *冷凝器:* 冷凝释放热量
    - *毛细管/膨胀阀:* 降压气体降温
    - *蒸发器:* 气体蒸发吸收热量
  ],
)

== 揭秘

#grid(
  columns: 2,
  gutter: 0.2em,
  image("assets/refrigerant.png"),
  [
    *关键在于合适的热物质！*
    - 沸点：通过*合理*的压力使其可以液化
    - 汽化潜热： 物质在相变时必须具有*高效*的热量变化
    - 临界温度： 液体能够因压力相变的极限温度，需显著高于环境温度，否则在日常高温下难以凝结为液体
  ],
)


== 历史演变

*早期*：使用氨(NH₃)、二氧化硫(SO₂)等。这些物质毒性大、易燃易爆，但制冷效果好。

\

*黄金时代*：1930s，发明了氟利昂/氯氟烃（CFCs，如R12）。它们无毒、不燃、化学性质极其稳定，完美解决了安全问题。

\

*发现问题*：1970s，科学家发现CFCs是破坏地球臭氧层的元凶。因此，《蒙特利尔议定书》规定全面淘汰它们。

== 历史演变

*第二代制冷剂*：氢氟烃（HFCs) 分类替代了氟利昂，其优点是对臭氧层无破坏，但却会捕获热量，导致全球变暖。

\

*第三代制冷剂*： 碳氢化合物（HCs) 分类即可以保护臭氧层，也不会导致全球变暖，但缺点是可燃。所以制造和维修过程	必须严格规范，防止泄露。

#set text(1.5em)
#align(center)[*感谢！*]


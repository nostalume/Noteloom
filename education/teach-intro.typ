#import "@preview/touying:0.6.1": *
#import themes.university: *

#set text(font: (
  (name: "Microsoft Sans Serif", covers: "latin-in-cjk"),
  "Microsoft YaHei",
))

#show: university-theme.with(
  aspect-ratio: "16-9",
  footer-a: self => [大气压强],
  config-common(handout: true),
  config-info(
    title: [看不见的"大力士"],
    subtitle: [探索大气压强的奥秘],
    author: [nostalume],
    date: datetime.today(),
    institution: [],
    logo: emoji.leaf,
  ),
  config-page(margin: (top: 2.4em)),
)

#title-slide()

= 引入

== 现象

#[
#set text(1.5em)
#align(center)[*你能拉开它们吗？*]
]

#grid(
	columns: 2,
	gutter: 0.8em,
	image("assets/suction_cup.png"),
	[
		#set text(1.5em)
		邀请力气大的同学 \ 尝试拉开！\

		到底是什么力量 \ 阻碍了它们？\
	]
)

== 现象

#grid(
	columns: 2,
	gutter: 0.8em,
	image("assets/reversed_cup.png"),
	[
		#set text(1.5em)
		是胶水吗？❌ \ 
		是纸板吗？ ❌ \
		是水的粘性吗？ ❌ \
		是手有魔力吗？❌ \
		那到底是什么？ ➡️
	]
)

基于受力分析，我们必须承认一种力阻碍了其运动！

== 揭秘

// #[
// ]

#grid(
	columns: 2,
	gutter:0.8em,
	image("assets/pressure.png"),
	[
		#[
			#set text(1.2em)
			#align(center)[*神秘的大力士 --- 大气压强*]
		]
		大气对处在其中的物体产生的压强， \
		称作*大气压强*, 而我们就生活在这\
		“海洋”的底部！\
		\
		- 大气压强稳定吗？\

		- 假如稳定，我们该如何测量？ \

		- 它如何改变我们的生活？
	]
)

= 开启探索之旅！


/* ============================================================================
 *  Typst 课程笔记模板 · 笔记模板1
 *  模板：inelegant-note 0.9.1（https://typst.app/universe/package/inelegant-note）
 *  样式源自：《机械设计.typ》学习笔记（字体、五色盒、注记盒、三线表等沿用）
 *
 *  编译（在文件所在目录执行）：
 *      typst compile 笔记模板1.typ 笔记.pdf
 *  实时预览：
 *      typst watch 笔记模板1.typ
 *  依赖：Typst ≥ 0.13；首次编译会自动下载 inelegant-note 及其依赖包。
 *  字体：正文 思源宋体（Source Han Serif SC）；标题 思源黑体（Source Han Sans SC，
 *        缺失时自动回退 Noto Sans SC / SimHei / SimSun）。
 *
 *  ── 使用说明 ──────────────────────────────────────────────────────────
 *  1. 复制本文件到你的笔记工作目录并改名（如 机械设计.typ）；
 *  2. 全文搜索并替换所有【】标记：封面信息、格言、前言、章节目录与正文；
 *  3. 图片请放在同目录 Figure/ 子文件夹中（或修改 image 路径）；
 *  4. 每章开头保留 counter 重置代码，可使图片/表格编号按章重新计数；
 *  5. 每章结尾可选「本章重点」框（见正文示例末尾）。
 *  ============================================================================ */

#import "@preview/inelegant-note:0.9.1": *

// ----------------------------------------------------------------------------
//  字体：标题优先思源黑体，正文优先思源宋体，缺失时逐级回退。
// ----------------------------------------------------------------------------
#let my-sans = (
  (name: "Noto Sans SC", covers: "latin-in-cjk"),
  "Source Han Sans SC",
  "Noto Sans SC",
  "SimHei",
)
#let my-serif = (
  (name: "Source Han Serif SC", covers: "latin-in-cjk"),
  "Source Han Serif SC",
  "SimSun",
)

// ----------------------------------------------------------------------------
//  封面：替换【】内容；不需要日期时注释掉 date 一行即可。
// ----------------------------------------------------------------------------
#{
  show text: set text(font: my-sans)
  cover-environment(
    title: [【课程名称】],
    subtitle: "【课程英文名 / 副标题 · 学习笔记】",
    author: "【姓名】",
    date: datetime(year: 2026, month: 10, day: 15),
    cover-image: none,
  )
}

#show: overall

// 章、节标题字体适配
#show heading: set text(font: my-sans)

// ----------------------------------------------------------------------------
//  盒子样式：五色内容盒（定义 / 定理 / 例 / 特征 / 公式），标题统一 my-sans。
//  正文写作时直接调用：
//      #definition-showy(title: "…")[ … ]
//      #theorem-showy(title: "…")[ … ]
//      #example-showy(title: "…")[ … ]
//      #feature-showy(title: "…")[ … ]
//      #formula-showy(title: "…")[ $ … $ ]
// ----------------------------------------------------------------------------
#let md-head = (size: 10.5pt, font: my-sans, weight: "regular", fill: black)
#let md-body = (size: 10.5pt, font: my-serif, weight: "regular", fill: black)

#let md-frame(identifier, name, color) = make-frame(
  identifier, name, inherited-levels: 1,
  render: my-fancy-box.with(
    border-color: color, title-color: color,
    body-color: color.lighten(95%), end-symbol: none,
    head-text: md-head, body-text: md-body,
  ),
)

#let (_, _, definition-showy, show-md-definition) = md-frame("md-definition", [定义], rgb("f19790"))
#let (_, _, theorem-showy, show-md-theorem) = md-frame("md-theorem", [定理], rgb("619ac3"))
#let (_, _, example-showy, show-md-example) = md-frame("md-example", [例], rgb("bec936"))
#let (_, _, feature-showy, show-md-feature) = md-frame("md-feature", [特征], rgb("63bbd0"))
#let (_, _, formula-showy, show-md-formula) = md-frame("md-formula", [公式], rgb("fba414"))

#let md-shows(body) = {
  show: show-md-definition
  show: show-md-theorem
  show: show-md-example
  show: show-md-feature
  show: show-md-formula
  body
}
#show: md-shows

// 注记盒：note（蓝）/ key（深蓝）/ warn（红）/ remark（灰引用条）
//   #note-box[ … ]        #key-box(title: "重点")[ … ]
//   #warn-box(title: "注意")[ … ]   #remark-box[ … ]
#let md-note-box(md-title, fill, icon, body) = my-notebox-rainbow(
  head-text: (size: .95em, weight: "regular", font: my-sans),
  body-text: (size: .95em, weight: "regular", font: my-serif, fill: black),
  fill: fill, title: md-title, icon-name: icon, body,
)
#let note-box(title: "注", body) = md-note-box(title, rgb("#0969da"), "info", body)
#let key-box(title: "重点", body) = md-note-box(title, rgb("#123a7d"), "bookmark", body)
#let warn-box(title: "注意", body) = md-note-box(title, rgb("#d1242f"), "alert", body)
#let remark-box(body) = my-quotebox-rainbow(
  body-text: (size: .95em, weight: "regular", font: my-serif, fill: black),
  body,
)

// 三线表（表头上下粗线、表头下细线）：
//   #figure(
//     md-table((3cm, 5cm, 4cm), ([表头A], [表头B], [表头C]), [a1], [b1], [c1], …),
//     caption: [表题],
//   )<fig-标签>
#let md-table(columns, head, ..rows) = table(
  columns: columns,
  stroke: none,
  inset: (x: 6pt, y: 5pt),
  table.hline(stroke: 0.08em),
  table.header(..head),
  table.hline(stroke: 0.05em),
  ..rows.pos(),
  table.hline(stroke: 0.08em),
)

// ----------------------------------------------------------------------------
//  前辅文：格言页、前言、目录（替换【】内容即可）
// ----------------------------------------------------------------------------
#front-matter[
  #align(center + horizon)[
    #text(font: "KaiTi", size: 17pt)[【格言，如：知者创物，巧者述之守之，世谓之工。】]
  ]

  = 前言

  本笔记整理自【教材 / 课程名称】（【作者 / 出版社】）。目前收录【已整理章节】，后续将陆续补入【待整理章节】。

  整理原则如下：

  - 概念、定义与计算公式一律沿用教材原文的表述与写法，仅作版式重排与环境归类，不改写、不删减；
  - 存疑或待补之处以醒目的标注框标出，不作臆改。

  #my-outline()
]

// ----------------------------------------------------------------------------
//  正文
// ----------------------------------------------------------------------------
#show: main-matter

// ============================================================================
//  第一章 示例（复制本章结构并替换【】内容即可开始写作）
// ============================================================================

= 【第一章 章节标题】

// 每章开头重置图片/表格编号，使编号按章重新计数
#counter(figure.where(kind: image)).update(0)
#counter(figure.where(kind: table)).update(0)

== 【1.1 小节标题】

正文直接书写，行内公式如 $F = m a$，独立公式如：

$ L_h = frac(10^6, 60 n) dot (frac(C, f_P (X F_r + Y F_a)))^epsilon $

#definition-showy(title: "定义名称")[
  *定义*（_英文术语_）：这里写定义内容。
]

#theorem-showy(title: "定理名称")[
  定理 / 强度条件等结论写在这里，可含公式：

  $ sigma = frac(M, W) <= [sigma] $
]

#formula-showy(title: "公式名称")[
  只放公式的盒子：

  $ p = "链号" times 25.4/16 $
]

#feature-showy(title: "特征名称")[
  特征 / 特点 / 分类要点写在这里，如“特点一；特点二；特点三”。
]

#example-showy(title: "例")[
  例题与解答过程写在这里。
]

#note-box[
  补充说明（蓝色“注”盒）。
]

#key-box(title: "重点")[
  重点内容（深蓝“重点”盒），可自定义标题。
]

#warn-box(title: "注意")[
  易错提醒（红色“注意”盒）。
]

#remark-box[
  引用 / 备注（灰色引用条）。
]

#figure(
  md-table(
    (3cm, 5cm, 4cm),
    ([列标题A], [列标题B], [列标题C]),
    [单元格], [单元格], [单元格],
    [单元格], [单元格], [单元格],
  ),
  caption: [三线表示例],
)<fig-表示例>

// 图片用法示例：把图片放入同目录 Figure/ 后取消注释。
// #figure(
//   image("Figure/示例图.png", width: 80%),
//   caption: [图片说明],
// )<fig-图示例>

正文可用 @fig-表示例 交叉引用上面的图/表。

#heading(level: 2, numbering: none, outlined: true)[本章重点]

+ 重点一；
+ 重点二；
+ 重点三。

// ---- 模板结束：复制以下结构继续写下一章 ----

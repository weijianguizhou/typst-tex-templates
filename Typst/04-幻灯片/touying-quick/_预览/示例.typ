// 仅用于生成预览；模板入口仍是 ../template/main.typ（空白起步）。
#import "@preview/touying-quick:0.5.0": *

#show: touying-quick.with(
  title: "基于 Typst 的学术汇报",
  subtitle: "从写作到幻灯片的统一工作流",
  heading-idx: true,
  bgimg: bgsky,
  theme: "blue",
  info: default-info,
  styles: default-styles,
  names: default-names,
  lang: "zh",
)

= 研究背景

== 为什么选择 Typst

- 纯文本源文件，版本管理友好
- 编译速度快，公式与排版原生支持
- 模板即代码，样式可以复用

== 一个最小示例

$ integral_0^1 x^2 dif x = 1/3 $

#table(
  columns: 3,
  [方法], [优点], [局限],
  [Word], [上手快], [公式排版弱],
  [LaTeX], [排版强], [编译链复杂],
  [Typst], [兼顾两者], [生态仍在成长],
)

= 方法与结果

== 工作流

+ 用 Typst 写论文
+ 同一套公式与图表复用到幻灯片
+ 一键导出 PDF

== 结论

- 模板把版式与内容分离
- 中文支持良好
- 适合组会、答辩与课程汇报

#show: appendix

== 备用页

这里放 Q&A 可能用到的补充材料。

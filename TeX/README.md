# TeX / LaTeX 模板

> 本目录只放 **LaTeX / TeX** 模板；Typst 模板在 [`../Typst/`](../Typst/README.md)。
> 中文模板统一用 **XeLaTeX** 编译，含目录/参考文献的通常要编译两遍。推荐 `latexmk -xelatex 主文件.tex`。

## 目录

| 类别 | 入口 | 说明 |
|---|---|---|
| PPT演示 | [`NJUST南理工-Beamer模板/NJUST-slides.tex`](<PPT演示/NJUST南理工-Beamer模板/NJUST-slides.tex>) | 南理工紫极简 Beamer，校徽、中文定理、三线表，16:9 |
| PPT演示 | [`钱学森学院beamer/QXC-slides.tex`](<PPT演示/钱学森学院beamer/QXC-slides.tex>) | 钱院洋红 Beamer，院徽组合标识，结构与 NJUST 版一致 |
| PPT演示 | [`minimalist-pku-beamer-2026-main/main.tex`](<PPT演示/minimalist-pku-beamer-2026-main/minimalist-pku-beamer-2026-main/main.tex>) | PKU 极简 Beamer 原版，NJUST/QXC 两版的版式来源 |
| 学术论文与报告 | [`学术论文模板.tex`](学术论文与报告/学术论文模板.tex) | 摘要、数学、图表、引用、附录的完整论文骨架 |
| 简历CV | [`简历模板.tex`](简历CV/简历模板.tex) | 单页紧凑简历：教育、项目、获奖、技能 |
| 公文与书信 | [`公文模板.tex`](公文与书信/公文模板.tex) | 正式公文排版 |
| 公文与书信 | [`书信模板.tex`](公文与书信/书信模板.tex) | 中文书信 / 邮件，附编译好的 PDF |
| 演讲稿 | [`演讲稿模板.tex`](演讲稿/演讲稿模板.tex) | 学术演讲、答辩讲稿；同目录有 Markdown 快速版 |
| 课程笔记 | [`课程笔记模板.tex`](课程笔记/课程笔记模板.tex) | 「李思风」极简学术笔记，12 款封面，方正宋体、定理盒 |
| 课程笔记 | [`笔记整理模板（分栏&多主题框）/cn-mynotes.tex`](<课程笔记/笔记整理模板（分栏&多主题框）/cn-mynotes.tex>) | `textbook.cls` 教材/长篇讲义，分栏、多主题框、参考文献 |

## 快速开始

1. 把整个模板子目录复制到新项目，保留同目录的图片、`.bib`、`.sty`/`.cls`；
2. 替换正文中的 `【】` 占位内容；
3. 用 VS Code + LaTeX Workshop 或 TeXstudio，编译器选 **XeLaTeX**；
4. 有目录/引用时编译两遍，或直接：

```powershell
latexmk -xelatex 主文件.tex
```

## 字体与依赖

- 中文：`ctex` + `xeCJK`；Windows 一般用 SimSun/SimHei，macOS 用 Songti SC，其他环境回退 Fandol；
- 数学：`amsmath`；图表：`graphicx` + `booktabs`；
- 参考文献：`natbib` + `.bib`（部分模板用 `biblatex`，以主文件为准）。

## 迁移说明

原 `模板/` 根目录下的 LaTeX 分类已整体移入本目录，文件内容未改；原顶层 Typst 笔记模板已移到 [`../Typst/03-课程笔记/我的课程笔记-inelegant-note/`](../Typst/03-课程笔记/我的课程笔记-inelegant-note/)。

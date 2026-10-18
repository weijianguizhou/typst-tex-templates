# 模板库

> 两套排版体系，物理分开、互不混杂：
>
> - **TeX/**：LaTeX / XeLaTeX 模板（原有模板全部迁入此目录）
> - **Typst/**：Typst 模板（80 个来自 Typst Universe 的精选模板 + 1 个本库自用笔记模板）

## 先选类型

| 你要做 | 推荐去处 | 编译方式 |
|---|---|---|
| 中文毕业论文 / 课程论文 | [`Typst/02-学位论文/`](Typst/02-学位论文/README.md) 或 [`TeX/学术论文与报告/`](TeX/学术论文与报告/学术论文模板.tex) | `typst compile` / `xelatex` |
| 英文期刊、会议投稿 | [`Typst/01-学术论文/`](Typst/01-学术论文/README.md) | `typst compile` |
| 课程笔记、讲义 | [`Typst/03-课程笔记/`](Typst/03-课程笔记/README.md) 或 [`TeX/课程笔记/`](TeX/课程笔记/README.md) | 两者均可 |
| 组会 / 答辩幻灯片 | [`Typst/04-幻灯片/`](Typst/04-幻灯片/README.md) 或 [`TeX/PPT演示/`](TeX/PPT演示/) | `typst compile` / `xelatex` |
| 简历 | [`Typst/05-简历CV/`](Typst/05-简历CV/README.md) 或 [`TeX/简历CV/`](TeX/简历CV/简历模板.tex) | 两者均可 |
| 学术海报 | [`Typst/06-海报/`](Typst/06-海报/README.md) | `typst compile` |
| 书稿 / 长讲义 | [`Typst/07-书籍与长文/`](Typst/07-书籍与长文/README.md) | `typst compile` |
| 公文、书信、邮件 | [`Typst/08-公文与书信/`](Typst/08-公文与书信/README.md) 或 [`TeX/公文与书信/`](TeX/公文与书信/) | 两者均可 |
| 试卷、作业、实验报告 | [`Typst/09-试卷作业与报告/`](Typst/09-试卷作业与报告/README.md) | `typst compile` |

## Typst：81 个本地模板 + 855 个全量目录

- 总入口：[`Typst/README.md`](Typst/README.md)
- 全量目录：[`Typst/Typst-Universe-全量目录.md`](Typst/Typst-Universe-全量目录.md)（855 个带模板的包，含版本、说明、仓库、是否已下载）
- 可筛选版本：[`Typst/Typst-Universe-全量目录.csv`](Typst/Typst-Universe-全量目录.csv)
- 中文模板专项：[`Typst/中文模板索引.md`](Typst/中文模板索引.md)
- 制作环境：Typst 0.15.1 / Windows，80 个上游模板已全部实测编译出 PDF。

| 分类 | 数量 | 代表模板 |
|---|---:|---|
| [学术论文](Typst/01-学术论文/README.md) | 12 | IEEE、ACM、LNCS、Elsevier、Springer Nature、CVPR、NeurIPS、ICML、ACL、arXiv、中文论文 |
| [学位论文](Typst/02-学位论文/README.md) | 14 | 南大、上交、南科大、哈工大、清华、北大、东南、华师大、厦大、中山、电子科大、河海、吉大、北航 |
| [课程笔记](Typst/03-课程笔记/README.md) | 13 | inelegant-note、chengsi、zhaji、simple-handout、ilm、minimal-note、dvdtyp + 自用模板 |
| [幻灯片](Typst/04-幻灯片/README.md) | 10 | Touying 快速起步、Aqua、Metropolyst、上交/中山/清华/山东大学主题、极简演示 |
| [简历 CV](Typst/05-简历CV/README.md) | 10 | modern-cv、brilliant-cv、ATS 友好、学术 CV、中文单页简历 |
| [海报](Typst/06-海报/README.md) | 6 | peace-of-posters、placard、pollux、pasquino 等 |
| [书籍与长文](Typst/07-书籍与长文/README.md) | 4 | bookly、orange-book、min-book、latexy-book |
| [公文与书信](Typst/08-公文与书信/README.md) | 4 | GB/T 9704 公文、DIN 5008 信函、letterloom、学术信函 |
| [试卷作业与报告](Typst/09-试卷作业与报告/README.md) | 8 | 考试卷、作业题、实验报告、国赛数学建模 |

**快速开始：**

```powershell
cd 模板/Typst/01-学术论文/charged-ieee
typst compile --root . template/main.typ 我的论文.pdf
```

每个模板目录都有 `模板信息.md`（中文说明 / 版本 / 许可 / 入口）和 `README.md`（上游原文），并带 `_预览/预览.pdf` 与 `预览.png`。首次编译会自动下载 `@preview/...` 依赖。

## TeX：原有 6 类 40 个 `.tex`

- 总入口：[`TeX/README.md`](TeX/README.md)
- [PPT演示](TeX/PPT演示/)：南理工 Beamer、钱学森学院 Beamer、PKU 极简 Beamer
- [学术论文与报告](TeX/学术论文与报告/学术论文模板.tex)：论文骨架（摘要 / 数学 / 图表 / 引用 / 附录）
- [简历CV](TeX/简历CV/简历模板.tex)：单页紧凑简历
- [公文与书信](TeX/公文与书信/)：正式公文 + 中文书信
- [演讲稿](TeX/演讲稿/演讲稿模板.tex)：LaTeX 讲稿 + Markdown 快速版
- [课程笔记](TeX/课程笔记/README.md)：李思风极简笔记 + `textbook.cls` 分栏笔记

```powershell
cd 模板/TeX/学术论文与报告
latexmk -xelatex 学术论文模板.tex
```

## 目录约定

```text
模板/
├── README.md                 # 本页：TeX / Typst 总入口
├── TeX/                      # 只放 LaTeX / TeX
│   ├── README.md
│   ├── PPT演示/
│   ├── 学术论文与报告/
│   ├── 简历CV/
│   ├── 公文与书信/
│   ├── 演讲稿/
│   └── 课程笔记/
├── Typst/                    # 只放 Typst
│   ├── README.md
│   ├── 01-学术论文/ … 09-试卷作业与报告/
│   ├── Typst-Universe-全量目录.md/.csv
│   └── 中文模板索引.md
└── _data/                    # 上游索引快照、精选清单、构建脚本
```

## 来源、版本与许可

- Typst 模板均来自 [Typst Universe](https://typst.app/universe/) 的 `packages/preview` 归档；每个目录保留上游 `README.md`、`LICENSE`（若有）和 `typst.toml`，版本见 `模板信息.md`。
- 上游未附 `LICENSE` 文件的包，许可字段取自 Typst Universe 索引（MIT / GPL-3.0 等），再分发前请回上游仓库确认。
- TeX 模板为原有模板与公开版本（PKU 极简 Beamer 等），版权与署名见各目录 `README.md`。
- 全量索引快照：`_data/typst-universe-index.json`；精选清单：`_data/curated.json`。

## 维护

```powershell
python 模板/_data/build_typst.py       # 重新抓取 Typst Universe 索引 + 补齐下载
python 模板/_data/compile_previews.py  # 编译并生成首页预览
python 模板/_data/fix_notes.py         # 修正编译说明、补缺失许可、写本地修正注记
python 模板/_data/make_indexes.py      # 重建分类页、中文索引、README
```

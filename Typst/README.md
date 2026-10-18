# Typst 模板

> 本目录只放 **Typst** 模板；LaTeX / TeX 模板在 [`../TeX/`](../TeX/README.md)。
> 已本地化 **81 个**模板：**80 个**精选自 [Typst Universe](https://typst.app/universe/) 的开放包，另加 **1 个**本库自用课程笔记模板；并附 **855 个**全量模板目录。
> 制作环境：Typst 0.15.1 / Windows；80 个上游模板均已实测编译出 PDF，预览见各分类页。

## 分类

| 分类 | 数量 | 内容 |
|---|---|---|
| [`01-学术论文`](./01-学术论文/README.md) | 12 | 期刊/会议论文，含 IEEE、ACM、LNCS、Elsevier、Springer Nature、CVPR、NeurIPS、ICML、ACL、arXiv 与中文论文排版。 |
| [`02-学位论文`](./02-学位论文/README.md) | 14 | 中国高校学位论文模板为主，覆盖南大、上交、南科大、哈工大、清华、北大、东南、华师大、厦大、中山、电子科大、河海、吉大、北航。 |
| [`03-课程笔记`](./03-课程笔记/README.md) | 13 | 课程笔记、讲义、数学笔记与知识整理，含中文排版与 Elegant Book 风格。 |
| [`04-幻灯片`](./04-幻灯片/README.md) | 10 | Touying / Polylux / 极简演示文稿，含上交、中山、清华、山东大学等中文主题。 |
| [`05-简历CV`](./05-简历CV/README.md) | 10 | 学术简历、ATS 友好简历、单页中文简历与多语言简历。 |
| [`06-海报`](./06-海报/README.md) | 6 | 会议 poster、A0/A1 学术海报与模块化网格布局。 |
| [`07-书籍与长文`](./07-书籍与长文/README.md) | 4 | 书稿、讲义成书、经典 LaTeX 书籍样式的 Typst 复刻。 |
| [`08-公文与书信`](./08-公文与书信/README.md) | 4 | GB/T 9704 中文公文、DIN 5008 商务信函、学术推荐信/求职信。 |
| [`09-试卷作业与报告`](./09-试卷作业与报告/README.md) | 8 | 考试卷、作业题、实验报告、数学建模与课程设计报告。 |

## 先看这里

- **全量目录（855 个）**：[`Typst-Universe-全量目录.md`](./Typst-Universe-全量目录.md) ｜ [`CSV`](./Typst-Universe-全量目录.csv) — 含包名、版本、说明、仓库、本地是否已下载。
- **中文模板索引**：[`中文模板索引.md`](./中文模板索引.md) — 从全量目录中筛出说明含中文的模板。
- **来源与版本**：[`_data/typst-universe-index.json`](../_data/typst-universe-index.json)（上游索引快照）与 [`_data/curated.json`](../_data/curated.json)（本库精选清单）。

## 快速开始

```powershell
cd 模板/Typst/01-学术论文/charged-ieee
typst compile --root . template/main.typ 我的论文.pdf
```

每个模板目录里：

- `模板信息.md`：中文说明、版本、许可、入口与编译命令；
- `README.md`：上游原始说明；
- `template/`：直接改这里的示例；
- `_预览/预览.pdf` / `预览.png`：本库编译出的首页预览；
- `lib.typ` 等：模板实现，一般不用改。

首次编译会从 Typst Universe 自动下载 `@preview/...` 依赖。中文模板若缺思源宋体/黑体，会回退到系统字体，建议安装 Noto Sans/Serif CJK SC。

## 选型建议

- 课程论文/期刊投稿：优先 `charged-ieee`（IEEE）、`faithful-acmart`（ACM）、`fine-lncs`（Springer LNCS）、`elsevier-replica`、`stellar-springer-nature`。
- 中文毕业论文：先看自己学校；没有就改 `02-学位论文` 里结构最接近的一版，字体和封面最容易替换。
- 课程笔记：`inelegant-note`、`chengsi`、`zhaji`、`simple-handout`；想要彩色卡片风格看 `dvdtyp`、`minimal-note`。
- 组会/答辩幻灯片：`touying-quick` 起步；中文主题看 `touying-simpl-sjtu`、`shuimu-touying`、`sdu-touying-simpl`。
- 简历：中文优先 `golixp-resume-zh-cn`、`habaneraa-one-page-resume-zh`；英文/学术优先 `modern-cv`、`brilliant-cv`、`modern-acad-cv`。
- 数学建模：`cumcm-muban`（国赛）与 `mcm-scaffold`（美赛，仅在全量目录中）。

## 许可

各模板许可见其目录下 `LICENSE` 与 `模板信息.md` 的「许可」字段。上游未附 LICENSE 文件的包，已在 `模板信息.md` 标注索引中的 SPDX 许可；商用/再分发前请回到上游仓库确认。

## 维护

重建/更新命令（需 Python 3 与 typst）：

```powershell
python 模板/_data/build_typst.py
python 模板/_data/compile_previews.py
python 模板/_data/fix_notes.py
python 模板/_data/make_indexes.py
```

`build_typst.py` 会重新抓取上游索引；`compile_previews.py` 只补缺失的预览；`fix_notes.py` 重写编译说明并补许可；`make_indexes.py` 重建分类页、中文索引与本页。

想从全量目录里再加一个模板：把包名加进 `_data/curated.json` 对应分类的 `items`，再依次跑 `build_typst.py`、`compile_previews.py`、`fix_notes.py`、`make_indexes.py`。

> 本地模板合计约 70 MB。
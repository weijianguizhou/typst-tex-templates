import json
import re
from pathlib import Path

BASE = Path(r"D:\studynotes\模板")
TYp = BASE / "Typst"
DATA = BASE / "_data"
CURATED = DATA / "curated.json"
INDEX = DATA / "typst-universe-index.json"
STATUS = DATA / "compile-status.json"

CAT_LABEL = {
    "thesis": "学位论文", "paper": "学术论文", "presentation": "幻灯片", "cv": "简历",
    "poster": "海报", "book": "书籍", "office": "公文信函", "report": "报告",
    "flyer": "传单", "layout": "版式", "utility": "工具", "components": "组件",
    "model": "模型", "fun": "趣味", "text": "文本", "visualization": "可视化",
    "integration": "集成", "scripting": "脚本", "languages": "语言", "other": "其他",
}


def vk(v):
    return tuple(int(x) for x in re.findall(r"\d+", v))


def main():
    raw = json.loads(INDEX.read_text(encoding="utf-8"))
    latest = {}
    for x in raw:
        if not x.get("template"):
            continue
        n = x["name"]
        if n not in latest or vk(x["version"]) > vk(latest[n]["version"]):
            latest[n] = x
    curated = json.loads(CURATED.read_text(encoding="utf-8"))
    status = {}
    if STATUS.exists():
        for x in json.loads(STATUS.read_text(encoding="utf-8")):
            status[x["name"]] = x
    selected = {n for c in curated["categories"] for n in c["items"]}

    category_rows = []
    for cat in curated["categories"]:
        rows = []
        previews = []
        for name in cat["items"]:
            meta = latest[name]
            folder = TYp / cat["dir"] / name
            st = status.get(name, {})
            state = st.get("status", "pending")
            mark = {"ok": "✓", "ok-existing": "✓", "ok-no-png": "△", "compile-error": "✗", "missing-folder": "✗", "missing-entry": "✗", "timeout": "✗"}.get(state, "…")
            desc = (meta.get("description") or "").strip()
            desc = re.sub(r"\s+", " ", desc).replace("|", "\\|")
            if len(desc) > 110:
                desc = desc[:107] + "…"
            entry = f"{meta['template']['path']}/{meta['template']['entrypoint']}"
            entry_link = f"[`{entry}`](<./{name}/{entry}>)"
            rows.append(f"| [`{name}`](./{name}/) | {meta['version']} | {desc} | {entry_link} | {mark} |")
            png = folder / "_预览" / "预览.png"
            if png.exists() and len(previews) < 8:
                previews.append(f'<a href="./{name}/_预览/预览.pdf"><img src="./{name}/_预览/预览.png" width="260" alt="{name}"></a>')
        if cat["dir"].startswith("03"):
            custom = "我的课程笔记-inelegant-note"
            rows.append(f"| [`{custom}`](./{custom}/) | 自用 | 本库自用的中文课程笔记模板（inelegant-note 五色盒、注记盒、三线表） | [`笔记模板1.typ`](<./{custom}/笔记模板1.typ>) | ✓ |")
            png = TYp / cat["dir"] / custom / "_预览" / "预览.png"
            if png.exists():
                previews.insert(0, f'<a href="./{custom}/_预览/预览.pdf"><img src="./{custom}/_预览/预览.png" width="260" alt="{custom}"></a>')
        cat_md = [f"# {cat['dir']}", "", f"> {cat['note']}", "", "| 模板 | 版本 | 简介 | 入口 | 编译 |", "|---|---|---|---|---|"]
        cat_md += rows
        if previews:
            cat_md += ["", "## 预览", "", '<div style="display:flex;flex-wrap:wrap;gap:12px">', "", *previews, "", "</div>"]
        if cat["dir"].startswith("04"):
            cat_md += ["", "> `touying-quick` 上游是空白起步模板；预览由 `_预览/示例.typ` 填充演示内容后生成。"]
        if cat["dir"].startswith("08"):
            cat_md += ["", "> `gbt9704-gongwen` 上游是空白起步模板；预览由 `_预览/示例.typ` 生成，内容为虚构的公文示例。"]
        cat_md += ["", "> 编译状态为制作时在 Typst 0.15.1、Windows 中抽检的结果；缺少字体会产生 warning，不一定影响出 PDF。", ""]
        (TYp / cat["dir"] / "README.md").write_text("\n".join(cat_md), encoding="utf-8")
        category_rows.append((cat, len(rows), mark))

    # 自定义模板行（03 类）
    custom = TYp / "03-课程笔记" / "我的课程笔记-inelegant-note"
    total_bytes = sum(p.stat().st_size for p in TYp.rglob("*") if p.is_file())
    # 顶层 README
    lines = [
        "# Typst 模板",
        "",
        "> 本目录只放 **Typst** 模板；LaTeX / TeX 模板在 [`../TeX/`](../TeX/README.md)。",
        "> 已本地化 **81 个**模板：**80 个**精选自 [Typst Universe](https://typst.app/universe/) 的开放包，另加 **1 个**本库自用课程笔记模板；并附 **855 个**全量模板目录。",
        "> 制作环境：Typst 0.15.1 / Windows；80 个上游模板均已实测编译出 PDF，预览见各分类页。",
        "",
        "## 分类",
        "",
        "| 分类 | 数量 | 内容 |",
        "|---|---|---|",
    ]
    for cat, n, _ in category_rows:
        total = n
        lines.append(f"| [`{cat['dir']}`](./{cat['dir']}/README.md) | {total} | {cat['note']} |")
    lines += [
        "",
        "## 先看这里",
        "",
        "- **全量目录（855 个）**：[`Typst-Universe-全量目录.md`](./Typst-Universe-全量目录.md) ｜ [`CSV`](./Typst-Universe-全量目录.csv) — 含包名、版本、说明、仓库、本地是否已下载。",
        "- **中文模板索引**：[`中文模板索引.md`](./中文模板索引.md) — 从全量目录中筛出说明含中文的模板。",
        "- **来源与版本**：[`_data/typst-universe-index.json`](../_data/typst-universe-index.json)（上游索引快照）与 [`_data/curated.json`](../_data/curated.json)（本库精选清单）。",
        "",
        "## 快速开始",
        "",
        "```powershell",
        "cd 模板/Typst/01-学术论文/charged-ieee",
        "typst compile --root . template/main.typ 我的论文.pdf",
        "```",
        "",
        "每个模板目录里：",
        "",
        "- `模板信息.md`：中文说明、版本、许可、入口与编译命令；",
        "- `README.md`：上游原始说明；",
        "- `template/`：直接改这里的示例；",
        "- `_预览/预览.pdf` / `预览.png`：本库编译出的首页预览；",
        "- `lib.typ` 等：模板实现，一般不用改。",
        "",
        "首次编译会从 Typst Universe 自动下载 `@preview/...` 依赖。中文模板若缺思源宋体/黑体，会回退到系统字体，建议安装 Noto Sans/Serif CJK SC。",
        "",
        "## 选型建议",
        "",
        "- 课程论文/期刊投稿：优先 `charged-ieee`（IEEE）、`faithful-acmart`（ACM）、`fine-lncs`（Springer LNCS）、`elsevier-replica`、`stellar-springer-nature`。",
        "- 中文毕业论文：先看自己学校；没有就改 `02-学位论文` 里结构最接近的一版，字体和封面最容易替换。",
        "- 课程笔记：`inelegant-note`、`chengsi`、`zhaji`、`simple-handout`；想要彩色卡片风格看 `dvdtyp`、`minimal-note`。",
        "- 组会/答辩幻灯片：`touying-quick` 起步；中文主题看 `touying-simpl-sjtu`、`shuimu-touying`、`sdu-touying-simpl`。",
        "- 简历：中文优先 `golixp-resume-zh-cn`、`habaneraa-one-page-resume-zh`；英文/学术优先 `modern-cv`、`brilliant-cv`、`modern-acad-cv`。",
        "- 数学建模：`cumcm-muban`（国赛）与 `mcm-scaffold`（美赛，仅在全量目录中）。",
        "",
        "## 许可",
        "",
        "各模板许可见其目录下 `LICENSE` 与 `模板信息.md` 的「许可」字段。上游未附 LICENSE 文件的包，已在 `模板信息.md` 标注索引中的 SPDX 许可；商用/再分发前请回到上游仓库确认。",
        "",
        "## 维护",
        "",
        "重建/更新命令（需 Python 3 与 typst）：",
        "",
        "```powershell",
        "python 模板/_data/build_typst.py",
        "python 模板/_data/compile_previews.py",
        "python 模板/_data/fix_notes.py",
        "python 模板/_data/make_indexes.py",
        "```",
        "",
        "`build_typst.py` 会重新抓取上游索引；`compile_previews.py` 只补缺失的预览；`fix_notes.py` 重写编译说明并补许可；`make_indexes.py` 重建分类页、中文索引与本页。",
        "",
        "想从全量目录里再加一个模板：把包名加进 `_data/curated.json` 对应分类的 `items`，再依次跑 `build_typst.py`、`compile_previews.py`、`fix_notes.py`、`make_indexes.py`。",
        "",
        f"> 本地模板合计约 {total_bytes / 1024 / 1024:.0f} MB。",
    ]
    (TYp / "README.md").write_text("\n".join(lines), encoding="utf-8")

    # 中文索引：全量 855 个中筛出简介含中文的包
    name_to_cat = {n: cat["dir"] for cat in curated["categories"] for n in cat["items"]}
    zh = []
    for meta in latest.values():
        desc = meta.get("description") or ""
        if not re.search(r"[\u4e00-\u9fff]", desc):
            continue
        if not (re.search(r"这|个|为|与|论文|模板|简历|笔记|中文|汉字|书法|公文|试卷|竞赛|课程|学位|毕业|排版|字体|公式|实验|讲义", desc) or re.search(r"Chinese|China|CJK", desc, re.I)):
            continue
        name = meta["name"]
        if name in name_to_cat:
            cdir = name_to_cat[name]
        else:
            cats = meta.get("categories") or []
            primary = next((c for c in ["thesis", "paper", "presentation", "cv", "poster", "book", "office", "report", "flyer"] if c in cats), cats[0] if cats else "other")
            cdir = CAT_LABEL.get(primary, primary)
        zh.append((cdir, name, meta, desc))
    zh.sort(key=lambda x: (x[0], x[1]))
    zlines = ["# 中文 Typst 模板索引", "", f"> 从 855 个 Typst Universe 模板中筛出简介含中文的包，共 {len(zh)} 个。★ 表示已下载到本库。", "", "| 分类 | 包 | 版本 | 说明 | 本地 |", "|---|---|---|---|---|"]
    for cdir, name, meta, desc in zh:
        desc = re.sub(r"\s+", " ", desc).replace("|", "\\|")
        if len(desc) > 110:
            desc = desc[:107] + "…"
        local = f"[★](./{cdir}/{name}/)" if name in selected else ""
        zlines.append(f"| {cdir} | `{name}` | {meta['version']} | {desc} | {local} |")
    zlines += ["", "> 表中“分类”对已下载模板用本库目录名，其余用上游主类别。", ""]
    (TYp / "中文模板索引.md").write_text("\n".join(zlines), encoding="utf-8")

    # 全量目录的英文类别名换成中文/英文对照
    catalog_path = TYp / "Typst-Universe-全量目录.md"
    catalog = catalog_path.read_text(encoding="utf-8")
    for en, cn in CAT_LABEL.items():
        catalog = catalog.replace(f"## {en}（", f"## {cn} / {en}（")
    catalog_path.write_text(catalog, encoding="utf-8")
    print("indexes written", len(category_rows), "categories,", len(zh), "Chinese templates")


if __name__ == "__main__":
    main()

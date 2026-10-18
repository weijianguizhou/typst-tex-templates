import csv
import json
import os
import re
import shutil
import tarfile
import tempfile
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

BASE = Path(r"D:\studynotes\模板")
DATA = BASE / "_data"
TYp = BASE / "Typst"
INDEX = DATA / "typst-universe-index.json"
CURATED = DATA / "curated.json"
UA = {"User-Agent": "Mozilla/5.0 (template-library-builder)"}


def version_key(v):
    return tuple(int(x) for x in re.findall(r"\d+", v))


def load_index():
    raw = json.loads(INDEX.read_text(encoding="utf-8"))
    latest = {}
    for item in raw:
        if not item.get("template"):
            continue
        name = item["name"]
        if name not in latest or version_key(item["version"]) > version_key(latest[name]["version"]):
            latest[name] = item
    return raw, latest


def download(url, dest):
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=90) as resp, open(dest, "wb") as fh:
                shutil.copyfileobj(resp, fh)
            return
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise last


def safe_extract(archive, target):
    with tarfile.open(archive, "r:gz") as tf:
        if hasattr(tarfile, "data_filter"):
            tf.extractall(target, filter="data")
        else:
            for member in tf.getmembers():
                member_path = (target / member.name).resolve()
                if not str(member_path).startswith(str(target.resolve())):
                    raise RuntimeError(f"unsafe path in archive: {member.name}")
            tf.extractall(target)


def display_name(meta):
    return meta["name"]


def chinese_note(meta, category):
    desc = (meta.get("description") or "").strip()
    text = desc if desc else "（上游未提供简介）"
    return f"""# {meta['name']}

> {text}

## 基本信息

| 项目 | 内容 |
|---|---|
| 分类 | {category} |
| Typst 包版本 | `{meta['version']}` |
| 作者 | {', '.join(meta.get('authors') or ['未知'])} |
| 许可 | {meta.get('license') or '未标注'} |
| 上游仓库 | {meta.get('repository') or '见 Typst Universe 页面'} |
| Universe | https://typst.app/universe/package/{meta['name']} |
| 入口文件 | `{meta['template']['path']}/{meta['template']['entrypoint']}` |

## 编译

在本目录执行：

```powershell
typst compile --root . "{meta['template']['path']}/{meta['template']['entrypoint']}" "_预览/预览.pdf"
```

首次编译会从 Typst Universe 下载 `@preview/{meta['name']}:{meta['version']}` 及其依赖。
若缺少字体，可先运行 `typst fonts` 查看本机字体，或在命令后加 `--font-path <字体目录>`。

## 目录说明

- `{meta['template']['path']}/`：上游模板示例，直接改这里的内容。
- `lib.typ` / 其他根目录文件：模板实现，通常不需要改。
- `_预览/`：本库生成的首页预览（若有）。
- `README.md`、`LICENSE`：上游说明与许可证，使用前请阅读。
"""


def main():
    raw, latest = load_index()
    curated = json.loads(CURATED.read_text(encoding="utf-8"))
    TYp.mkdir(parents=True, exist_ok=True)
    status = []
    total_bytes = 0
    for cat in curated["categories"]:
        cat_dir = TYp / cat["dir"]
        cat_dir.mkdir(parents=True, exist_ok=True)
        for name in cat["items"]:
            meta = latest.get(name)
            if not meta:
                status.append({"name": name, "category": cat["label"], "status": "missing-in-index"})
                print(f"[MISSING] {name}")
                continue
            folder = cat_dir / name
            info = folder / "模板信息.md"
            if info.exists() and (folder / meta["template"]["path"]).is_dir():
                status.append({"name": name, "category": cat["label"], "version": meta["version"], "status": "existing", "path": str(folder)})
                print(f"[SKIP] {name}")
                continue
            url = f"https://packages.typst.org/preview/{name}-{meta['version']}.tar.gz"
            print(f"[GET ] {name} {meta['version']}")
            with tempfile.TemporaryDirectory() as td:
                archive = Path(td) / f"{name}.tar.gz"
                try:
                    download(url, archive)
                    staging = Path(td) / "pkg"
                    staging.mkdir()
                    safe_extract(archive, staging)
                    entry = staging / meta["template"]["path"] / meta["template"]["entrypoint"]
                    if not entry.is_file():
                        raise RuntimeError(f"entrypoint not found: {entry.relative_to(staging)}")
                    if folder.exists():
                        shutil.rmtree(folder)
                    shutil.copytree(staging, folder)
                    (folder / "模板信息.md").write_text(chinese_note(meta, cat["label"]), encoding="utf-8")
                    size = sum(p.stat().st_size for p in folder.rglob("*") if p.is_file())
                    total_bytes += size
                    status.append({"name": name, "category": cat["label"], "version": meta["version"], "status": "ok", "bytes": size, "path": str(folder)})
                except Exception as exc:  # noqa: BLE001
                    status.append({"name": name, "category": cat["label"], "version": meta["version"], "status": "error", "error": str(exc)})
                    print(f"[FAIL] {name}: {exc}")
            time.sleep(0.15)
    (DATA / "download-status.json").write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = sum(1 for x in status if x["status"] in ("ok", "existing"))
    print(f"done: ok={ok} total={len(status)} bytes={total_bytes/1024/1024:.1f} MB")

    # 全量目录：855 个模板
    by_cat = defaultdict(list)
    priority = ["thesis", "paper", "presentation", "cv", "poster", "book", "office", "report", "flyer"]
    selected = {name for cat in curated["categories"] for name in cat["items"]}
    for meta in latest.values():
        cats = meta.get("categories") or []
        primary = next((c for c in priority if c in cats), cats[0] if cats else "other")
        by_cat[primary].append(meta)
    order = priority + sorted(set(by_cat) - set(priority))
    lines = [
        "# Typst Universe 全量模板目录",
        "",
        f"> 数据源：[Typst Universe 包索引](https://packages.typst.org/preview/index.json)，抓取时间 {time.strftime('%Y-%m-%d')}。",
        f"> 共 **{len(latest)}** 个带模板的包（同一包的多个版本只保留最新版）。带 ★ 的已下载到本库。",
        "",
        "分类按上游 `categories` 的主类别归并；一个模板可能同时属于多个类别。",
        "",
    ]
    for cat in order:
        items = sorted(by_cat.get(cat, []), key=lambda x: x["name"].lower())
        if not items:
            continue
        lines += [f"## {cat}（{len(items)}）", "", "| 包名 | 版本 | 说明 | 本地 | 来源 |", "|---|---|---|---|---|"]
        for meta in items:
            desc = re.sub(r"\s+", " ", meta.get("description") or "").replace("|", "\\|")
            if len(desc) > 100:
                desc = desc[:97] + "…"
            local = ""
            if meta["name"] in selected:
                rel = next((p for p in (TYp.rglob(meta["name"])) if p.is_dir()), None)
                local = "★" if rel else ""
            repo = meta.get("repository") or ""
            src = f"[Universe](https://typst.app/universe/package/{meta['name']})"
            if repo:
                src += f" / [Repo]({repo})"
            lines.append(f"| `{meta['name']}` | {meta['version']} | {desc} | {local} | {src} |")
        lines.append("")
    (TYp / "Typst-Universe-全量目录.md").write_text("\n".join(lines), encoding="utf-8")

    with open(TYp / "Typst-Universe-全量目录.csv", "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(["包名", "版本", "主分类", "全部类别", "说明", "作者", "许可", "仓库", "Universe", "本地已下载"])
        for meta in sorted(latest.values(), key=lambda x: x["name"].lower()):
            cats = meta.get("categories") or []
            primary = next((c for c in priority if c in cats), cats[0] if cats else "other")
            writer.writerow([
                meta["name"], meta["version"], primary, ",".join(cats),
                meta.get("description") or "", "; ".join(meta.get("authors") or []),
                meta.get("license") or "", meta.get("repository") or "",
                f"https://typst.app/universe/package/{meta['name']}",
                "是" if meta["name"] in selected else "否",
            ])
    (DATA / "typst-template-names.json").write_text(json.dumps(sorted(selected), ensure_ascii=False, indent=2), encoding="utf-8")
    print("catalog written")


if __name__ == "__main__":
    main()

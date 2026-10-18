import json
import re
import tomllib
from pathlib import Path

BASE = Path(r"D:\studynotes\模板")
TYp = BASE / "Typst"
DATA = BASE / "_data"
CURATED = DATA / "curated.json"
INDEX = DATA / "typst-universe-index.json"

PATCH_NOTES = {
    "lucky-icml": "上游 0.7.0 在 Typst 0.15 下有两处兼容问题：`main.typ` 改为导入本地 `../icml.typ`（不再走 `@preview`），并把 `icml2024.typ` 中的 `\"字符串\" + type(...)` 改为 `str(type(...))`。功能不变。",
    "cumcm-muban": "上游示例公式把 `diff` 当作变量，Typst 0.15 会报 `unknown variable: diff`；已把三处微分符号改为 `d`，其余内容未动。",
    "uo-tsinghua-thesis": "上游使用 `planck.reduce`，Typst 0.15 已移除该修饰符；已替换为约化普朗克常数符号 `ℏ`，其余内容未动。",
}

PREVIEW_NOTES = {
    "touying-quick": "上游入口是空白起步模板；本库的 `_预览/预览.pdf` 由 `_预览/示例.typ` 填充演示内容后生成，方便看实际效果。",
    "gbt9704-gongwen": "上游入口是空白起步模板；本库的 `_预览/预览.pdf` 由 `_预览/示例.typ` 生成，内容为虚构的公文示例。",
}

LICENSE_TEXT = {
    "arkheion": "MIT",
    "modern-sustech-thesis": "MIT",
    "modern-uestc-thesis": "MIT",
    "uo-tsinghua-thesis": "GPL-3.0",
    "inelegant-note": "MIT",
    "obelisk": "MIT",
    "touying-aqua": "MIT",
}


def main():
    latest = {}
    for x in json.loads(INDEX.read_text(encoding="utf-8")):
        if not x.get("template"):
            continue
        n = x["name"]
        if n not in latest or tuple(map(int, re.findall(r"\d+", x["version"]))) > tuple(map(int, re.findall(r"\d+", latest[n]["version"]))):
            latest[n] = x
    curated = json.loads(CURATED.read_text(encoding="utf-8"))
    for cat in curated["categories"]:
        for name in cat["items"]:
            folder = TYp / cat["dir"] / name
            if not folder.is_dir():
                continue
            toml = tomllib.loads((folder / "typst.toml").read_text(encoding="utf-8"))
            tpath = toml["template"]["path"]
            entry = toml["template"]["entrypoint"]
            up = "../" * len(Path(tpath).parts)
            info = (folder / "模板信息.md").read_text(encoding="utf-8")
            help_block = f"""## 编译

推荐在模板目录内编译（模板里的 `/xxx` 绝对引用会以 `{tpath}/` 为根）：

```powershell
cd "{tpath}"
typst compile "{entry}" "{up}_预览/预览.pdf"
```

若报找不到 `/lib.typ` 等包根文件，改从包根目录编译：

```powershell
typst compile --root . "{tpath}/{entry}" "_预览/预览.pdf"
```

首次编译会从 Typst Universe 下载 `@preview/{name}:{latest[name]['version']}` 及其依赖。
若缺少字体，可先运行 `typst fonts` 查看本机字体，或在命令后加 `--font-path <字体目录>`。
"""
            if name in {"lucky-icml"}:
                help_block = f"""## 编译

本模板已改为引用包根目录的本地实现，必须从包根目录编译：

```powershell
typst compile --root . "{tpath}/{entry}" "_预览/预览.pdf"
```

首次编译会下载 `@preview/lemmify` 等依赖。若缺少字体，可在命令后加 `--font-path <字体目录>`。
"""
            info = re.sub(r"## 编译\n.*?(?=\n## 目录说明)", help_block, info, flags=re.S)
            if name in PATCH_NOTES and "## 本地修正" not in info:
                info = info.replace("## 目录说明", f"## 本地修正\n\n{PATCH_NOTES[name]}\n\n## 目录说明")
            if name in PREVIEW_NOTES and "## 预览说明" not in info:
                info = info.replace("## 目录说明", f"## 预览说明\n\n{PREVIEW_NOTES[name]}\n\n## 目录说明")
            (folder / "模板信息.md").write_text(info, encoding="utf-8")

            readme = folder / "README.md"
            if readme.exists():
                text = readme.read_text(encoding="utf-8", errors="replace")
                marker = "> 本目录由模板库整理"
                if marker not in text:
                    text = f"> 本目录由模板库整理；版本、许可与编译方式见 [模板信息.md](./模板信息.md)。\n\n" + text
                    readme.write_text(text, encoding="utf-8")

            if name in LICENSE_TEXT and not (folder / "LICENSE").exists() and not (folder / "LICENSE.txt").exists():
                repo = latest[name].get("repository") or f"https://typst.app/universe/package/{name}"
                (folder / "LICENSE").write_text(
                    f"SPDX-License-Identifier: {LICENSE_TEXT[name]}\n\n"
                    f"上游包：{name} {latest[name]['version']}\n"
                    f"来源：{repo}\n\n"
                    "Typst Universe 归档未附 LICENSE 文件；许可标识取自上游索引。\n"
                    "完整许可证文本请到上面的仓库或 Universe 页面查看。\n",
                    encoding="utf-8",
                )
    print("notes/license refresh done")


if __name__ == "__main__":
    main()

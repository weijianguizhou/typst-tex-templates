import json
import subprocess
import time
import tomllib
from pathlib import Path

BASE = Path(r"D:\studynotes\模板")
TYp = BASE / "Typst"
DATA = BASE / "_data"
CURATED = DATA / "curated.json"


def main():
    curated = json.loads(CURATED.read_text(encoding="utf-8"))
    results = []
    for cat in curated["categories"]:
        for name in cat["items"]:
            folder = TYp / cat["dir"] / name
            toml = tomllib.loads((folder / "typst.toml").read_text(encoding="utf-8"))
            tpath = toml["template"]["path"]
            entry = toml["template"]["entrypoint"]
            up = "../" * len(Path(tpath).parts)
            a = subprocess.run(
                ["typst", "compile", "--root", ".", entry, f"{up}_预览/_cmdtest.pdf"],
                cwd=folder / tpath, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180,
            )
            b = subprocess.run(
                ["typst", "compile", "--root", ".", f"{tpath}/{entry}", "_预览/_cmdtest.pdf"],
                cwd=folder, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180,
            )
            results.append({"name": name, "category": cat["dir"], "in_template": a.returncode == 0, "from_root": b.returncode == 0})
            print(f"{name}\tA={a.returncode == 0}\tB={b.returncode == 0}", flush=True)
            time.sleep(0.05)
    (DATA / "compile-modes.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    only_b = [x["name"] for x in results if x["from_root"] and not x["in_template"]]
    both = [x["name"] for x in results if x["from_root"] and x["in_template"]]
    neither = [x["name"] for x in results if not x["from_root"] and not x["in_template"]]
    print(f"\nboth={len(both)} only_root={len(only_b)} neither={len(neither)}")
    print("only_root:", ", ".join(only_b))
    print("neither:", ", ".join(neither))


if __name__ == "__main__":
    main()

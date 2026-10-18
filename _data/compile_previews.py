import json
import re
import subprocess
import time
from pathlib import Path

BASE = Path(r"D:\studynotes\模板")
TYp = BASE / "Typst"
DATA = BASE / "_data"
INDEX = DATA / "typst-universe-index.json"
CURATED = DATA / "curated.json"
FONT_PATH = None
TYPST = "typst"


def version_key(v):
    return tuple(int(x) for x in re.findall(r"\d+", v))


def main():
    raw = json.loads(INDEX.read_text(encoding="utf-8"))
    latest = {}
    for item in raw:
        if not item.get("template"):
            continue
        n = item["name"]
        if n not in latest or version_key(item["version"]) > version_key(latest[n]["version"]):
            latest[n] = item
    curated = json.loads(CURATED.read_text(encoding="utf-8"))
    status = []
    for cat in curated["categories"]:
        for name in cat["items"]:
            meta = latest.get(name)
            folder = TYp / cat["dir"] / name
            if not meta or not folder.is_dir():
                status.append({"name": name, "category": cat["label"], "status": "missing-folder"})
                continue
            entry = Path(meta["template"]["path"]) / meta["template"]["entrypoint"]
            if not (folder / entry).is_file():
                status.append({"name": name, "category": cat["label"], "status": "missing-entry", "entry": str(entry)})
                print(f"[NOENTRY] {name} {entry}")
                continue
            preview = folder / "_预览"
            preview.mkdir(exist_ok=True)
            pdf = preview / "预览.pdf"
            png = preview / "预览.png"
            if pdf.exists() and pdf.stat().st_size > 1000 and png.exists() and png.stat().st_size > 1000:
                status.append({"name": name, "category": cat["label"], "status": "ok-existing", "entry": str(entry), "seconds": 0, "warnings": 0})
                print(f"[KEEP] {name}", flush=True)
                continue
            font_args = ["--font-path", FONT_PATH] if FONT_PATH else []
            cmd = [TYPST, "compile", "--root", ".", *font_args, str(entry), str(Path("_预览") / "预览.pdf")]
            t0 = time.time()
            try:
                proc = subprocess.run(cmd, cwd=folder, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
                elapsed = round(time.time() - t0, 1)
                out = (proc.stdout or "") + (proc.stderr or "")
                if proc.returncode != 0 or not pdf.exists():
                    status.append({"name": name, "category": cat["label"], "status": "compile-error", "entry": str(entry), "seconds": elapsed, "log": out[-2500:]})
                    print(f"[FAIL] {name}: {out.strip().splitlines()[-1] if out.strip() else 'unknown'}")
                    continue
                cmd2 = [TYPST, "compile", "--root", ".", *font_args, str(entry), str(Path("_预览") / "预览.png"), "--format", "png", "--pages", "1", "--ppi", "96"]
                proc2 = subprocess.run(cmd2, cwd=folder, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
                warn = len(re.findall(r"^warning:", out, flags=re.M))
                status.append({
                    "name": name,
                    "category": cat["label"],
                    "status": "ok" if proc2.returncode == 0 and png.exists() else "ok-no-png",
                    "entry": str(entry),
                    "seconds": elapsed,
                    "warnings": warn,
                    "pdf_bytes": pdf.stat().st_size,
                })
                print(f"[OK  ] {name} {elapsed}s warn={warn}", flush=True)
            except subprocess.TimeoutExpired:
                status.append({"name": name, "category": cat["label"], "status": "timeout", "entry": str(entry)})
                print(f"[TIME] {name}")
    (DATA / "compile-status.json").write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = sum(1 for x in status if x["status"].startswith("ok"))
    fail = [x["name"] for x in status if not x["status"].startswith("ok")]
    print(f"\ncompiled ok={ok}/{len(status)}")
    if fail:
        print("failed:", ", ".join(fail))


if __name__ == "__main__":
    main()

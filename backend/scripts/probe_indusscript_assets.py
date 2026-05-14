"""Download bundled indusscript.in assets and probe all AssetManifest paths."""
from __future__ import annotations
import json
import urllib.request
from pathlib import Path

REPO = Path(__file__).parents[2]
PROBE = REPO / "glossa-corpus" / "indus" / "sources" / "rmrl" / "raw" / "indusscript-probe"
PROBE.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
BASE = "https://indusscript.in"

def fetch(url: str) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read(), r.headers.get("content-type", "")

def try_asset(path: str, save_name: str) -> None:
    url = f"{BASE}/{path}"
    try:
        data, ctype = fetch(url)
        # Check if we got the SPA shell (index.html) instead of real content
        is_html = data[:100].strip().startswith(b"<!") or b"<html" in data[:500].lower()
        if is_html and len(data) < 10000 and "pdf" in path.lower():
            print(f"  REDIRECT-TO-SPA: {path} ({ctype}) — got HTML shell")
            return
        (PROBE / save_name).write_bytes(data)
        print(f"  OK: {save_name} ({len(data):,} bytes, {ctype})")
    except Exception as exc:
        print(f"  FAIL: {path} -> {exc}")

print("=== Probing bundled asset paths ===")

# High-value specific assets
priority = [
    ("assets/assets/im77intro.pdf", "im77intro.pdf"),
    ("assets/lang/en.json", "lang_en.json"),
    ("assets/lang/ta.json", "lang_ta.json"),
    ("version.json", "version.json"),
    ("flutter_service_worker.js", "flutter_service_worker.js"),
]
for path, name in priority:
    try_asset(path, name)

# Read AssetManifest to find ALL bundled assets
am = PROBE / "AssetManifest.json"
if am.exists():
    assets = json.loads(am.read_text(encoding="utf-8"))
    print(f"\n=== All {len(assets)} bundled asset paths ===")
    for path in sorted(assets.keys()):
        print(f"  {path}")

    # Try to download any asset that looks like data/PDF/JSON
    print("\n=== Attempting data/document asset downloads ===")
    for path in sorted(assets.keys()):
        if any(path.lower().endswith(ext) for ext in [".json", ".pdf", ".csv", ".txt", ".tsv"]):
            save_name = path.replace("/", "_").replace("assets_assets_", "")
            try_asset(path, save_name)

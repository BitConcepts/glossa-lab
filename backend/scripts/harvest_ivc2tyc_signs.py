#!/usr/bin/env python3
"""Harvest Indus sign images from the ivc2tyc GitHub dataset.

Source: https://github.com/oohalakkadi/ivc2tyc (MIT licence)
        datasets/indus/{N}.jpg  — 715 individual sign images numbered by
        Fuls/ICIT sign numbers.

Mapping strategy
----------------
* M001-M417  (Mahadevan range) : look up fuls_id in sign_crosswalk.json.
* M420+      (Fuls extension)  : the numeric suffix IS the ICIT number.
* P-prefix   (Parpola IDs)     : numeric suffix compared against ivc2tyc.

Output
------
* static/signs/{sign_id}.png          — normalised 128px black-on-white
* static/signs/originals/{sign_id}.png — original (possibly larger)
* static/signs/originals/ivc2tyc_cache/{N}.jpg — raw download cache
  (kept permanently so future re-runs never re-download)
* static/signs/manifest.json          — updated provenance tracking
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

# ── Paths ────────────────────────────────────────────────────────────────────
_SCRIPT_DIR   = Path(__file__).resolve().parent
_BACKEND_DIR  = _SCRIPT_DIR.parent
_STATIC_SIGNS = _BACKEND_DIR / "static" / "signs"
_ORIGINALS    = _STATIC_SIGNS / "originals"
_IVC2TYC_CACHE = _ORIGINALS / "ivc2tyc_cache"   # permanent raw download cache
_MANIFEST_PATH = _STATIC_SIGNS / "manifest.json"
_CROSSWALK_PATH = (
    _BACKEND_DIR.parent / "glossa-corpus" / "indus" / "canonical" / "sign_crosswalk.json"
)
_ANCHORS_PATH   = _BACKEND_DIR / "reports" / "INDUS_FINAL_ANCHORS.json"

SIGN_SIZE   = 128
SOURCE_KEY  = "ivc2tyc"
DELAY_SECS  = 0.25   # polite delay between GitHub downloads

_UA = "GlossaLab-SignHarvester/1.0 (+https://github.com/BitConcepts/glossa-lab)"
_RAW_BASE = "https://raw.githubusercontent.com/oohalakkadi/ivc2tyc/main/datasets/indus"


# ── Helpers ──────────────────────────────────────────────────────────────────

def _now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def load_manifest() -> dict:
    if _MANIFEST_PATH.exists():
        try:
            return json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_manifest(m: dict) -> None:
    _MANIFEST_PATH.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")


def normalize(img_arr: np.ndarray) -> np.ndarray:
    """Convert any colour/grey image to 128×128 pure black-on-white."""
    if img_arr.ndim == 3 and img_arr.shape[2] == 4:
        pil = Image.fromarray(img_arr, "RGBA")
        bg  = Image.new("RGBA", pil.size, (255, 255, 255, 255))
        bg.paste(pil, mask=pil.split()[3])
        gray = np.array(bg.convert("L"))
    elif img_arr.ndim == 3:
        gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    else:
        gray = img_arr.copy()

    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if binary.mean() < 128:
        binary = cv2.bitwise_not(binary)

    rows = np.any(binary < 200, axis=1)
    cols = np.any(binary < 200, axis=0)
    if rows.any() and cols.any():
        r0, r1 = np.where(rows)[0][[0, -1]]
        c0, c1 = np.where(cols)[0][[0, -1]]
        pad = max(6, int(0.12 * max(r1 - r0, c1 - c0, 1)))
        r0 = max(0, r0 - pad);  r1 = min(binary.shape[0] - 1, r1 + pad)
        c0 = max(0, c0 - pad);  c1 = min(binary.shape[1] - 1, c1 + pad)
        content = binary[r0:r1 + 1, c0:c1 + 1]
    else:
        content = binary

    h, w = content.shape
    sz = max(h, w, 1)
    sq = np.full((sz, sz), 255, dtype=np.uint8)
    sq[(sz - h) // 2:(sz - h) // 2 + h, (sz - w) // 2:(sz - w) // 2 + w] = content
    out = cv2.resize(sq, (SIGN_SIZE, SIGN_SIZE), interpolation=cv2.INTER_AREA)
    _, out = cv2.threshold(out, 127, 255, cv2.THRESH_BINARY)
    return out


def save_sign(sign_id: str, proc: np.ndarray, orig: np.ndarray,
              manifest: dict) -> None:
    _STATIC_SIGNS.mkdir(parents=True, exist_ok=True)
    _ORIGINALS.mkdir(parents=True, exist_ok=True)

    proc_path = _STATIC_SIGNS / f"{sign_id}.png"
    Image.fromarray(proc).convert("L").save(str(proc_path), optimize=True)

    orig_path = _ORIGINALS / f"{sign_id}.png"
    orig_gray = orig if orig.ndim == 2 else cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    Image.fromarray(orig_gray).convert("L").save(str(orig_path), optimize=True)

    manifest[sign_id] = {
        "status": "ok",
        "source": SOURCE_KEY,
        "processed_path": str(proc_path.relative_to(_BACKEND_DIR)),
        "original_path":  str(orig_path.relative_to(_BACKEND_DIR)),
        "timestamp": _now(),
    }


# ── GitHub availability list ──────────────────────────────────────────────────

def fetch_available_numbers(cache_path: Path) -> set[int]:
    """Return set of ICIT numbers available in the ivc2tyc repo.

    Caches the list to *cache_path* so repeated runs don't hammer the API.
    """
    if cache_path.exists():
        try:
            data = json.loads(cache_path.read_text(encoding="utf-8"))
            nums = set(data.get("available", []))
            fetched = data.get("fetched_at", "")
            print(f"  [cache] {len(nums)} numbers from {fetched}")
            return nums
        except Exception:
            pass

    print("  Querying GitHub API for ivc2tyc file list…")
    api_url = "https://api.github.com/repos/oohalakkadi/ivc2tyc/git/trees/main?recursive=1"
    req = urllib.request.Request(
        api_url,
        headers={"Accept": "application/vnd.github.v3+json", "User-Agent": _UA},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        tree = json.loads(r.read()).get("tree", [])

    nums: set[int] = set()
    for item in tree:
        p = item.get("path", "")
        if p.startswith("datasets/indus/") and p.endswith(".jpg"):
            try:
                nums.add(int(p[len("datasets/indus/"):-len(".jpg")]))
            except ValueError:
                pass

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        json.dumps({"available": sorted(nums), "fetched_at": _now()}, indent=2),
        encoding="utf-8",
    )
    print(f"  Found {len(nums)} signs ({min(nums)}–{max(nums)})")
    return nums


# ── Number → sign_id mapping ─────────────────────────────────────────────────

def build_mapping(available: set[int]) -> dict[str, int]:
    """Return {sign_id: icit_number} for all signs we can fetch."""
    # 1. Fuls crosswalk (M001-M417 range with explicit fuls_id)
    fuls_map: dict[str, int] = {}
    if _CROSSWALK_PATH.exists():
        try:
            cw = json.loads(_CROSSWALK_PATH.read_text(encoding="utf-8"))
            for sid, info in cw.get("crosswalk", {}).items():
                fid = info.get("fuls_id")
                if fid:
                    try:
                        fuls_map[sid] = int(str(fid))
                    except (ValueError, TypeError):
                        pass
        except Exception:
            pass

    # 2. Extended anchor signs (M420+, P-prefix, etc.)
    #    For M-prefix where number ≥ 1: number suffix = ICIT number.
    #    For P-prefix: numeric suffix compared against available.
    all_sign_ids: set[str] = set()
    # From crosswalk
    if _CROSSWALK_PATH.exists():
        try:
            cw = json.loads(_CROSSWALK_PATH.read_text(encoding="utf-8"))
            all_sign_ids |= set(cw.get("crosswalk", {}).keys())
        except Exception:
            pass
    # From anchors
    if _ANCHORS_PATH.exists():
        try:
            data = json.loads(_ANCHORS_PATH.read_text(encoding="utf-8"))
            all_sign_ids |= set(data.get("anchors", {}).keys())
        except Exception:
            pass
    # From manifest
    manifest = load_manifest()
    all_sign_ids |= set(manifest.keys())

    mapping: dict[str, int] = {}
    for sid in all_sign_ids:
        # Explicit fuls crosswalk mapping (highest confidence)
        if sid in fuls_map and fuls_map[sid] in available:
            mapping[sid] = fuls_map[sid]
            continue
        # M-prefix: number suffix
        if sid.startswith("M"):
            try:
                n = int(sid[1:])
                if n in available:
                    mapping[sid] = n
            except ValueError:
                pass
        # P-prefix: number suffix
        elif sid.startswith("P"):
            try:
                n = int(sid[1:])
                if n in available:
                    mapping[sid] = n
            except ValueError:
                pass

    return mapping


# ── Download one sign ─────────────────────────────────────────────────────────

def download_or_cache(icit_n: int) -> np.ndarray | None:
    """Return BGR image array for ICIT sign number *icit_n*.

    Downloads once and caches permanently in ivc2tyc_cache/.
    """
    _IVC2TYC_CACHE.mkdir(parents=True, exist_ok=True)
    cache_file = _IVC2TYC_CACHE / f"{icit_n}.jpg"

    if cache_file.exists() and cache_file.stat().st_size > 0:
        img = cv2.imread(str(cache_file))
        if img is not None:
            return img

    url = f"{_RAW_BASE}/{icit_n}.jpg"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = r.read()
        cache_file.write_bytes(raw)
        arr = np.frombuffer(raw, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return img
    except Exception as exc:
        print(f"    FAIL {icit_n}: {exc}")
        return None


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    import argparse
    p = argparse.ArgumentParser(description="Harvest ivc2tyc Indus sign images")
    p.add_argument("--force",     action="store_true", help="Re-download even if already sourced from ivc2tyc")
    p.add_argument("--all",       action="store_true", help="Process ALL sign IDs, not just fallbacks")
    p.add_argument("--sign",      metavar="ID",        help="Process one sign (e.g. M700)")
    p.add_argument("--no-cache",  action="store_true", help="Force re-query GitHub API (ignore local file list cache)")
    p.add_argument("--dry-run",   action="store_true", help="Show plan without downloading")
    args = p.parse_args()

    print("\n═══════════════════════════════════════════════")
    print("  ivc2tyc Sign Harvest  (MIT licence)")
    print("═══════════════════════════════════════════════\n")

    # Step 1: Get available ICIT numbers
    list_cache = _IVC2TYC_CACHE / "_file_list.json"
    if args.no_cache and list_cache.exists():
        list_cache.unlink()
    print("Step 1: Loading ivc2tyc file list")
    available = fetch_available_numbers(list_cache)

    # Step 2: Build mappings
    print("\nStep 2: Building sign_id → ICIT number mapping")
    mapping = build_mapping(available)
    print(f"  {len(mapping)} sign IDs mappable")

    # Step 3: Filter to what needs downloading
    manifest = load_manifest()
    if args.sign:
        targets = {args.sign: mapping[args.sign]} if args.sign in mapping else {}
        if not targets:
            print(f"  ERROR: {args.sign} not in mapping")
            sys.exit(1)
    elif args.all:
        targets = mapping
    else:
        # Only process signs still on fallback_icon (or missing)
        targets = {
            sid: n for sid, n in mapping.items()
            if (args.force or
                manifest.get(sid, {}).get("source") in ("fallback_icon", "", None) or
                sid not in manifest)
        }

    print(f"\nStep 3: {len(targets)} signs to download/process")
    if args.dry_run:
        for sid, n in sorted(targets.items())[:30]:
            print(f"  {sid} ← ICIT #{n}")
        if len(targets) > 30:
            print(f"  … and {len(targets) - 30} more")
        print("\n[dry-run] No files written.")
        return

    # Step 4: Download, normalise, save
    print("\nStep 4: Downloading and normalising…\n")
    saved = 0
    failed = 0
    skipped = 0

    for i, (sign_id, icit_n) in enumerate(sorted(targets.items())):
        # Skip if already ivc2tyc-sourced and not forcing
        if not args.force and manifest.get(sign_id, {}).get("source") == SOURCE_KEY:
            skipped += 1
            continue

        img = download_or_cache(icit_n)
        if img is None:
            failed += 1
            continue

        try:
            proc = normalize(img)
            # Validate: not blank, not solid black
            black_ratio = float(np.sum(proc < 128)) / proc.size
            if not (0.005 <= black_ratio <= 0.60):
                print(f"  SKIP {sign_id} (ICIT #{icit_n}): bad density {black_ratio:.3f}")
                skipped += 1
                continue
            save_sign(sign_id, proc, img, manifest)
            saved += 1
            print(f"  ✓ {sign_id} ← ICIT #{icit_n} (density={black_ratio:.3f})")
        except Exception as exc:
            print(f"  FAIL {sign_id}: {exc}")
            failed += 1

        if saved % 25 == 0 and saved > 0:
            save_manifest(manifest)
            print(f"    [checkpoint] {saved} saved so far…")

        if img is not None:          # was a real download, not cache hit
            cache_file = _IVC2TYC_CACHE / f"{icit_n}.jpg"
            if not cache_file.exists() or cache_file.stat().st_size == 0:
                time.sleep(DELAY_SECS)

    save_manifest(manifest)

    print(f"""
═══════════════════════════════════════════════
  Complete
  Saved:   {saved}
  Failed:  {failed}
  Skipped: {skipped}
  Total:   {saved + failed + skipped}

  Cache:   {_IVC2TYC_CACHE}
  Manifest updated.
═══════════════════════════════════════════════
""")


if __name__ == "__main__":
    main()

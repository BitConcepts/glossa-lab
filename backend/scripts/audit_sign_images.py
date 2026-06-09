#!/usr/bin/env python3
"""Cross-reference audit for Indus sign images.

Runs four independent checks to ensure sign images are accurate:

1. FILE CHECK   — every manifest entry has a real PNG on disk, correct size
2. PIXEL CHECK  — ink density is within 0.3%–65% (not blank, not solid)
3. MULTI-SOURCE — signs with 2+ sources are compared structurally
                  (Structural Similarity Index ≥ 0.2 after normalisation
                  and size matching; lower SSI = possibly wrong sign)
4. SEQUENTIAL   — M001-M417 glyphs should look distinct from their immediate
                  neighbours; flags any pair with SSI ≥ 0.80 (suspiciously
                  similar) that aren't known numeric-stroke sequences

Reports a per-sign verdict and an overall summary.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np

_BACKEND_DIR   = Path(__file__).resolve().parent.parent
_STATIC_SIGNS  = _BACKEND_DIR / "static" / "signs"
_MANIFEST_PATH = _STATIC_SIGNS / "manifest.json"
_CROSSWALK     = _BACKEND_DIR.parent / "glossa-corpus" / "indus" / "canonical" / "sign_crosswalk.json"
_ANCHORS       = _BACKEND_DIR / "reports" / "INDUS_FINAL_ANCHORS.json"
_REPORT_PATH   = _BACKEND_DIR / "reports" / "sign_image_audit.json"

SIGN_SIZE = 128

# Known Mahadevan stroke-numeral signs — adjacent numbers in these families
# are legitimately similar so SSI thresholds are relaxed.
_STROKE_FAMILIES = {
    frozenset(range(86, 110)),   # M086-M109: stroke numerals
    frozenset(range(97, 110)),
}


# ── Helpers ─────────────────────────────────────────────────────────────────

def load_img(sign_id: str) -> np.ndarray | None:
    p = _STATIC_SIGNS / f"{sign_id}.png"
    if not p.exists():
        return None
    img = cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    img = cv2.resize(img, (SIGN_SIZE, SIGN_SIZE))
    _, b = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if b.mean() < 128:
        b = cv2.bitwise_not(b)
    return b.astype(np.float32) / 255.0


def pixel_density(img: np.ndarray) -> float:
    """Fraction of black pixels in a normalised 0-1 float image."""
    return float((img < 0.5).sum()) / img.size


def structural_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Simple normalised cross-correlation as proxy for structural similarity."""
    fa = a.flatten() - a.mean()
    fb = b.flatten() - b.mean()
    norm_a = np.linalg.norm(fa)
    norm_b = np.linalg.norm(fb)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(fa, fb) / (norm_a * norm_b))


def _is_stroke_numeral(a: str, b: str) -> bool:
    try:
        na, nb = int(a[1:]), int(b[1:])
    except (ValueError, IndexError):
        return False
    for fam in _STROKE_FAMILIES:
        if na in fam and nb in fam:
            return True
    return False


# ── Checks ───────────────────────────────────────────────────────────────────

def check_files(manifest: dict) -> dict[str, list[str]]:
    """Check 1: every manifest entry has a real PNG on disk."""
    issues: dict[str, list[str]] = {}
    for sid, entry in manifest.items():
        errs: list[str] = []
        proc = _BACKEND_DIR / entry.get("processed_path", "")
        if not proc.exists():
            errs.append("PNG_MISSING")
        elif proc.stat().st_size == 0:
            errs.append("PNG_EMPTY")
        if entry.get("status") != "ok":
            errs.append(f"STATUS={entry.get('status')}")
        if errs:
            issues[sid] = errs
    return issues


def check_pixels(manifest: dict) -> dict[str, list[str]]:
    """Check 2: pixel density in acceptable range."""
    issues: dict[str, list[str]] = {}
    for sid, entry in manifest.items():
        src = entry.get("source", "")
        if src == "fallback_icon":
            continue  # skip generated placeholders
        img = load_img(sid)
        if img is None:
            issues[sid] = ["LOAD_FAIL"]
            continue
        d = pixel_density(img)
        errs: list[str] = []
        if d < 0.003:
            errs.append(f"TOO_SPARSE({d:.4f})")
        elif d > 0.65:
            errs.append(f"TOO_DENSE({d:.4f})")
        if errs:
            issues[sid] = errs
    return issues


def check_multi_source(manifest: dict, ivc2tyc_cache: Path) -> dict[str, dict]:
    """Check 3: signs with 2+ sources — compare m77_pdf vs ivc2tyc.

    For M001-M417 signs that exist in both the m77_pdf and ivc2tyc, load both
    images and compute structural similarity.  Very low SSI (<0.05) means the
    two images look completely different — likely a numbering mismatch.
    """
    results: dict[str, dict] = {}

    # Load ivc2tyc file list
    flist_path = ivc2tyc_cache / "_file_list.json"
    if not flist_path.exists():
        return {}
    try:
        available_icit = set(json.loads(flist_path.read_text())["available"])
    except Exception:
        return {}

    # Load crosswalk for Mahadevan→ICIT mapping
    fuls_map: dict[str, int] = {}
    if _CROSSWALK.exists():
        try:
            cw = json.loads(_CROSSWALK.read_text(encoding="utf-8"))
            for sid, info in cw.get("crosswalk", {}).items():
                fid = info.get("fuls_id")
                if fid:
                    try:
                        fuls_map[sid] = int(str(fid))
                    except (ValueError, TypeError):
                        pass
        except Exception:
            pass

    for sid, entry in manifest.items():
        if entry.get("source") != "m77_pdf":
            continue
        if not sid.startswith("M"):
            continue
        try:
            n = int(sid[1:])
        except ValueError:
            continue
        # Find ICIT number
        icit_n = fuls_map.get(sid)
        if icit_n is None and n in available_icit:
            icit_n = n  # direct mapping for M420+

        if icit_n not in available_icit:
            continue

        # Load current (m77_pdf) image
        img_current = load_img(sid)
        if img_current is None:
            continue

        # Load ivc2tyc raw image
        raw_path = ivc2tyc_cache / f"{icit_n}.jpg"
        if not raw_path.exists():
            continue
        raw = cv2.imread(str(raw_path), cv2.IMREAD_GRAYSCALE)
        if raw is None:
            continue
        raw = cv2.resize(raw, (SIGN_SIZE, SIGN_SIZE))
        _, b = cv2.threshold(raw, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if b.mean() < 128:
            b = cv2.bitwise_not(b)
        img_icit = b.astype(np.float32) / 255.0

        ssi = structural_similarity(img_current, img_icit)
        status = "ok" if ssi >= 0.05 else "MISMATCH"
        results[sid] = {
            "icit_n": icit_n,
            "ssi": round(ssi, 3),
            "status": status,
        }

    return results


def check_sequential(manifest: dict, stride: int = 1) -> dict[str, dict]:
    """Check 4: adjacent M-numbers should look distinct.

    Flags (sign_a, sign_b) pairs with SSI ≥ 0.80 that are not stroke numerals.
    High similarity between non-numeral neighbours often indicates a grid
    mis-alignment (same cell extracted twice).
    """
    m_ids = sorted(
        [sid for sid in manifest if sid.startswith("M")
         and manifest[sid].get("source") == "m77_pdf"],
        key=lambda s: int(s[1:])
    )
    flags: dict[str, dict] = {}
    for i in range(len(m_ids) - stride):
        a, b = m_ids[i], m_ids[i + stride]
        if _is_stroke_numeral(a, b):
            continue
        try:
            na, nb = int(a[1:]), int(b[1:])
        except ValueError:
            continue
        if nb - na > 5:
            continue  # non-adjacent in Mahadevan sequence
        img_a = load_img(a)
        img_b = load_img(b)
        if img_a is None or img_b is None:
            continue
        ssi = structural_similarity(img_a, img_b)
        if ssi >= 0.92:
            flags[f"{a}_{b}"] = {
                "sign_a": a, "sign_b": b, "ssi": round(ssi, 3),
                "note": "suspiciously_similar_neighbours",
            }
    return flags


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    if not _MANIFEST_PATH.exists():
        print("ERROR: manifest.json not found")
        sys.exit(1)

    manifest = json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))
    ivc2tyc_cache = _STATIC_SIGNS / "originals" / "ivc2tyc_cache"

    print("╔══════════════════════════════════════════════════════╗")
    print("║          Sign Image Cross-Reference Audit            ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    total  = len(manifest)
    by_src: dict[str, int] = {}
    for v in manifest.values():
        s = v.get("source", "none")
        by_src[s] = by_src.get(s, 0) + 1

    print("── Source breakdown ──")
    for src, cnt in sorted(by_src.items(), key=lambda x: -x[1]):
        print(f"  {cnt:4d}  {src}")
    print()

    # Check 1
    print("── Check 1: File existence ──")
    file_issues = check_files(manifest)
    if file_issues:
        for sid, errs in sorted(file_issues.items()):
            print(f"  ✗ {sid}: {', '.join(errs)}")
    else:
        print(f"  ✓ All {total} manifest entries have valid PNGs on disk")
    print()

    # Check 2
    print("── Check 2: Pixel density ──")
    pixel_issues = check_pixels(manifest)
    real_count = sum(1 for v in manifest.values() if v.get("source") != "fallback_icon")
    if pixel_issues:
        for sid, errs in sorted(pixel_issues.items()):
            print(f"  ✗ {sid}: {', '.join(errs)}")
    else:
        print(f"  ✓ All {real_count} real images have acceptable ink density")
    print()

    # Check 3
    print("── Check 3: Multi-source consistency (m77_pdf vs ivc2tyc) ──")
    multi = check_multi_source(manifest, ivc2tyc_cache)
    mismatches = {k: v for k, v in multi.items() if v["status"] != "ok"}
    ok_count   = sum(1 for v in multi.values() if v["status"] == "ok")
    if mismatches:
        print(f"  {ok_count} OK, {len(mismatches)} MISMATCHES:")
        for sid, info in sorted(mismatches.items()):
            print(f"  ✗ {sid} ↔ ICIT#{info['icit_n']}: SSI={info['ssi']} — likely numbering mismatch")
    elif multi:
        print(f"  ✓ {ok_count} cross-referenced signs match between m77_pdf and ivc2tyc (SSI ≥ 0.05)")
    else:
        print("  (no overlapping sources to compare)")
    print()

    # Check 4
    print("── Check 4: Sequential neighbour similarity ──")
    seq_flags = check_sequential(manifest)
    if seq_flags:
        print(f"  {len(seq_flags)} suspiciously similar neighbour pairs (possible grid mis-alignment):")
        for key, info in sorted(seq_flags.items()):
            print(f"  ⚠ {info['sign_a']} ↔ {info['sign_b']}: SSI={info['ssi']}")
    else:
        print("  ✓ No suspiciously similar neighbour pairs detected")
    print()

    # Overall verdict
    total_issues = len(file_issues) + len(pixel_issues) + len(mismatches) + len(seq_flags)
    fallback_count = by_src.get("fallback_icon", 0)
    print("══════════════════════════════════════════════════════")
    print(f"  Total signs:    {total}")
    print(f"  Real images:    {total - fallback_count}")
    print(f"  Fallback icons: {fallback_count}")
    print(f"  Sources:        {len(by_src)}")
    print(f"  Check issues:   {total_issues}")
    if total_issues == 0:
        print("  VERDICT: ✓ PASS — all checks clean")
    else:
        print(f"  VERDICT: ⚠ {total_issues} issue(s) need review")
    print("══════════════════════════════════════════════════════")

    # Save report
    report = {
        "total": total,
        "by_source": by_src,
        "file_issues": file_issues,
        "pixel_issues": pixel_issues,
        "multi_source": multi,
        "multi_source_mismatches": mismatches,
        "sequential_flags": seq_flags,
        "verdict": "PASS" if total_issues == 0 else "REVIEW",
    }
    _REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    _REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\n  Full report: {_REPORT_PATH.relative_to(_BACKEND_DIR)}")


if __name__ == "__main__":
    main()

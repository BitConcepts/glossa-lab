"""Mahadevan 1977 — Glyph labeling and template building.

For each textnum in the Firestore dump that also has glyph crops:
  1. Load the known sign sequence (from Firestore texts[] field)
  2. Load the extracted glyph crops (from glyph_segment.py)
  3. Align glyphs with signs by position
  4. Save each glyph as a labeled template: templates/{sign_id}/sample_{n}.png
  5. Build canonical templates (median image per sign class)

The alignment is position-based:
  - If glyph count == sign count: direct 1:1 mapping
  - If glyph count > sign count: over-segmented, skip or use midpoints
  - If glyph count < sign count: under-segmented, use what we have

Output:
  ocr_results/glyph_templates/{sign_id}/sample_{n}.png  — labeled samples
  ocr_results/glyph_templates/{sign_id}/canonical.png   — median template
  ocr_results/glyph_templates/label_report.json         — alignment stats

Usage:
    shell.cmd python backend/scripts/glyph_label.py
"""
from __future__ import annotations
import json, sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import numpy as np
import cv2

REPO = Path(__file__).parents[2]
FIRESTORE = (REPO / "glossa-corpus/indus/sources/rmrl/raw/indusscript-probe"
             / "firestore_indusarrays_full.json")
CROPS_DIR = REPO / "glossa-corpus/indus/ocr_results/glyph_crops"
TMPL_DIR  = REPO / "glossa-corpus/indus/ocr_results/glyph_templates"
TMPL_DIR.mkdir(parents=True, exist_ok=True)

GLYPH_SIZE = 64  # must match glyph_segment.py


def load_firestore_signs() -> dict[int, list[str]]:
    """Load best sign sequence per textnum (group all docs, pick longest)."""
    import re as _re
    from collections import defaultdict
    data = json.loads(FIRESTORE.read_text(encoding="utf-8"))
    by_tn: dict[int, list[list[str]]] = defaultdict(list)
    for doc in data.get("documents", []):
        tn = doc.get("textnum")
        if tn is None:
            continue
        texts = doc.get("texts") or []
        signs = [_re.sub(r'[<>:"/\\|?*]', '_', str(s).strip()).lstrip("0") or "0"
                 for s in texts if str(s).strip()]
        if signs:
            by_tn[int(tn)].append(signs)
    result = {}
    for tn, seqs in by_tn.items():
        result[tn] = max(seqs, key=len)
    return result


def load_glyph_crops(textnum: int) -> list[np.ndarray]:
    """Load sorted glyph crops for a textnum."""
    d = CROPS_DIR / str(textnum)
    if not d.exists():
        return []
    files = sorted(d.glob("glyph_*.png"))
    glyphs = []
    for f in files:
        img = cv2.imread(str(f))
        if img is not None:
            glyphs.append(img)
    return glyphs


def align_and_label(signs: list[str], glyphs: list[np.ndarray]
                     ) -> list[tuple[str, np.ndarray]] | None:
    """
    Align sign IDs with glyph crops.
    Returns list of (sign_id, glyph_img) or None if alignment is unreliable.
    """
    n_signs = len(signs)
    n_glyphs = len(glyphs)

    if n_signs == 0 or n_glyphs == 0:
        return None

    # Exact match
    if n_signs == n_glyphs:
        return list(zip(signs, glyphs))

    # Over-segmented: more glyphs than signs
    # Some signs (like "|||" strokes) split into multiple crops
    # Strategy: evenly distribute glyphs to signs (each sign gets ceil(n_glyphs/n_signs) crops)
    # Use the FIRST glyph of each sign's allocation
    if n_glyphs > n_signs:
        ratio = n_glyphs / n_signs
        pairs = []
        for i, sign in enumerate(signs):
            glyph_idx = min(int(i * ratio), n_glyphs - 1)
            pairs.append((sign, glyphs[glyph_idx]))
        return pairs

    # Under-segmented: fewer glyphs than signs
    # Skip this text for labeling (unreliable alignment)
    return None


def build_canonical(samples: list[np.ndarray]) -> np.ndarray:
    """Build canonical template as the sharpest sample (most dark pixels after threshold).
    Avoids the ghost-image problem of median averaging with misaligned samples.
    """
    if not samples:
        return np.ones((GLYPH_SIZE, GLYPH_SIZE, 3), dtype=np.uint8) * 255
    best_img = samples[0]
    best_score = 0
    for s in samples:
        gray = cv2.cvtColor(s, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
        # Score = dark pixel fraction (more ink = cleaner sign)
        dark_frac = np.sum(binary == 0) / binary.size
        if dark_frac > best_score:
            best_score = dark_frac
            best_img = s
    return best_img


def main():
    print("=== M77 Glyph Labeling & Template Building ===")

    # Load data
    signs_db = load_firestore_signs()
    print(f"Firestore texts: {len(signs_db)}")

    # Find textnums with both crops and sign data
    crop_textnums = set(
        int(d.name) for d in CROPS_DIR.iterdir()
        if d.is_dir() and d.name.isdigit() and (d / "glyph_00.png").exists()
    )
    common = set(signs_db.keys()) & crop_textnums
    print(f"Texts with both crops and Firestore data: {len(common)}")

    # Build labeled set
    templates: dict[str, list[np.ndarray]] = defaultdict(list)
    stats = {
        "exact_match": 0,
        "over_segmented": 0,
        "under_segmented": 0,
        "skipped": 0,
        "total_labeled_pairs": 0,
    }

    for tn in sorted(common):
        signs = signs_db[tn]
        glyphs = load_glyph_crops(tn)
        if not glyphs:
            stats["skipped"] += 1
            continue

        pairs = align_and_label(signs, glyphs)
        if pairs is None:
            stats["under_segmented"] += 1
            continue

        n_s, n_g = len(signs), len(glyphs)
        if n_s == n_g:
            stats["exact_match"] += 1
        else:
            # Skip over-segmented texts for template building
            # Only exact matches give reliable alignment
            stats["over_segmented"] += 1
            continue

        for sign_id, glyph in pairs:
            # Normalize sign ID for use as directory name.
            # Signs like "*342" (prefixed variants) use underscore instead.
            import re as _re
            sign_key = _re.sub(r'[<>:"/\\|?*]', '_', sign_id.strip()).lstrip("0") or "0"
            templates[sign_key].append(glyph)
            stats["total_labeled_pairs"] += 1

    print(f"\nAlignment stats:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"  Unique sign classes: {len(templates)}")

    # Save templates
    sample_counts = {}
    for sign_id, samples in templates.items():
        d = TMPL_DIR / sign_id
        d.mkdir(exist_ok=True)
        # Save up to 20 samples per sign
        for i, s in enumerate(samples[:20]):
            cv2.imwrite(str(d / f"sample_{i:03d}.png"), s)
        # Build canonical
        canonical = build_canonical(samples)
        cv2.imwrite(str(d / "canonical.png"), canonical)
        sample_counts[sign_id] = len(samples)

    # Report
    sign_counts_sorted = sorted(sample_counts.items(), key=lambda x: -x[1])
    print(f"\nTop 20 sign classes by sample count:")
    for sid, cnt in sign_counts_sorted[:20]:
        print(f"  Sign {sid:>4}: {cnt} samples")

    low_coverage = [(s, c) for s, c in sign_counts_sorted if c < 3]
    print(f"\nSigns with <3 samples: {len(low_coverage)}")

    report = {
        "_citation": {"primary_sources": ["I.8", "A.1"]},
        "generated_at": datetime.utcnow().isoformat(),
        "stats": stats,
        "sign_classes": len(templates),
        "sign_sample_counts": dict(sign_counts_sorted),
        "low_coverage_signs": [s for s, _ in low_coverage],
    }
    (TMPL_DIR / "label_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(f"\nTemplates saved: {TMPL_DIR}")
    print(f"Report: {TMPL_DIR / 'label_report.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

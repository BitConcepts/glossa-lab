#!/usr/bin/env python3
"""Extract individual sign glyph images from Mahadevan 1977 Appendix I pages.

Processes page scans from data/page_previews/mah_p793.png through mah_p804.png
(Appendix I: List of Sign Variants, pages 785-796 of the book).

Strategy:
  1. Split each page into left and right table halves
  2. Detect horizontal ruled lines that separate sign entries
  3. For each row, find the sign number (left-margin text) and the
     primary variant drawing (first large blob)
  4. Normalize each extracted glyph to 128x128 black-on-white PNG
  5. Save to static/signs/M{NNN}.png and update manifest.json

Usage::
    python backend/scripts/extract_mahadevan_sign_glyphs.py
    python backend/scripts/extract_mahadevan_sign_glyphs.py --dry-run
    python backend/scripts/extract_mahadevan_sign_glyphs.py --page 793
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

# ── Paths ────────────────────────────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
_BACKEND_DIR = _SCRIPT_DIR.parent
_DATA_DIR = _BACKEND_DIR / "data"
_PAGE_DIR = _DATA_DIR / "page_previews"
_STATIC_SIGNS = _BACKEND_DIR / "static" / "signs"
_ORIGINALS_DIR = _STATIC_SIGNS / "originals"
_MANIFEST_PATH = _STATIC_SIGNS / "manifest.json"

# Appendix I pages: IIIF indices 793-804 contain sign variant drawings
APPENDIX_I_PAGES = list(range(793, 805))

# Output sign image size
SIGN_SIZE = 128

# ── Known sign sequence per page (from visual inspection) ────────────────
# Each entry: (page_index, column, [sign_numbers])
# column: 'L' = left half, 'R' = right half
# These are Mahadevan sign numbers (not M-prefixed).
# Extracted by reading the SIGN No. column from each page scan.
PAGE_SIGN_MAP: dict[int, dict[str, list[int]]] = {
    793: {
        "L": [1, 8, 9, 12, 14, 15, 17, 19, 28],
        "R": [29, 32, 35, 38, 40, 48, 49, 50, 51, 53, 54],
    },
    794: {
        "L": [55, 56, 57, 60, 67, 68, 69, 70, 72, 73, 74, 76],
        "R": [78, 81, 84, 86, 87, 89, 90, 91, 94, 96, 98, 102, 103],
    },
    795: {
        "L": [104, 106, 109, 111, 112, 119, 120, 121, 123, 124, 125, 128, 132],
        "R": [136, 137, 141, 142, 143, 146, 149, 150, 155, 158, 159, 162, 167],
    },
    796: {
        "L": [171, 176, 177, 179, 181, 182, 183, 185, 186, 188, 189, 193],
        "R": [195, 199, 200, 211, 216, 217, 218, 220, 221, 222, 224, 225, 226],
    },
    797: {
        "L": [227, 228, 230, 231, 232, 233, 236, 237, 238, 240, 241, 243, 244],
        "R": [246, 248, 249, 251, 253, 254, 258, 260, 261, 262, 263, 267, 268],
    },
    798: {
        "L": [269, 270, 271, 272, 273, 275, 276, 278, 279, 280, 281, 283],
        "R": [284, 285, 289, 291, 293, 295, 296, 298, 300, 301, 303, 304],
    },
    799: {
        "L": [306, 307, 308, 309, 310, 311, 312, 313, 314, 316, 317, 319, 320],
        "R": [321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333],
    },
    800: {
        "L": [336, 337, 338, 340, 341, 342, 343, 345, 347],
        "R": [348, 358, 359, 365, 367, 371, 373, 374, 375, 379, 381, 384],
    },
    801: {
        "L": [385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395],
        "R": [396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406],
    },
    802: {
        "L": [407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417],
        "R": [],  # second half is empty or continuation
    },
}


def _load_manifest() -> dict:
    if _MANIFEST_PATH.exists():
        try:
            return json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def _save_manifest(manifest: dict) -> None:
    _MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def normalize_glyph(crop: np.ndarray) -> np.ndarray:
    """Normalize a cropped glyph to SIGN_SIZE x SIGN_SIZE black-on-white."""
    # To grayscale
    if crop.ndim == 3:
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    else:
        gray = crop.copy()

    # Otsu threshold
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Ensure black-on-white
    if binary.mean() < 128:
        binary = cv2.bitwise_not(binary)

    # Auto-crop to content bounding box
    rows = np.any(binary < 200, axis=1)
    cols = np.any(binary < 200, axis=0)
    if rows.any() and cols.any():
        r0, r1 = np.where(rows)[0][[0, -1]]
        c0, c1 = np.where(cols)[0][[0, -1]]
        pad = max(6, int(0.12 * max(r1 - r0, c1 - c0, 1)))
        r0 = max(0, r0 - pad)
        r1 = min(binary.shape[0] - 1, r1 + pad)
        c0 = max(0, c0 - pad)
        c1 = min(binary.shape[1] - 1, c1 + pad)
        content = binary[r0 : r1 + 1, c0 : c1 + 1]
    else:
        content = binary

    # Pad to square
    h, w = content.shape
    sz = max(h, w, 1)
    square = np.full((sz, sz), 255, dtype=np.uint8)
    yo = (sz - h) // 2
    xo = (sz - w) // 2
    square[yo : yo + h, xo : xo + w] = content

    # Resize to SIGN_SIZE
    out = cv2.resize(square, (SIGN_SIZE, SIGN_SIZE), interpolation=cv2.INTER_AREA)
    _, out = cv2.threshold(out, 127, 255, cv2.THRESH_BINARY)
    return out


def detect_hlines(binary: np.ndarray, min_width_frac: float = 0.3) -> list[int]:
    """Detect horizontal ruled lines in a binary image. Returns y-coords."""
    h, w = binary.shape
    min_w = int(w * min_width_frac)

    # Morphological horizontal line detection
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (min_w, 1))
    detected = cv2.morphologyEx(255 - binary, cv2.MORPH_OPEN, kernel)

    # Find y-coordinates of detected lines
    row_sums = detected.sum(axis=1)
    threshold = w * 128  # at least half the width should be line
    line_ys = np.where(row_sums > threshold)[0]

    if len(line_ys) == 0:
        return []

    # Cluster nearby y-values (within 5px)
    clusters = []
    cluster = [line_ys[0]]
    for y in line_ys[1:]:
        if y - cluster[-1] <= 5:
            cluster.append(y)
        else:
            clusters.append(int(np.mean(cluster)))
            cluster = [y]
    clusters.append(int(np.mean(cluster)))

    return clusters


def _find_best_glyph(cell: np.ndarray, min_area: int = 60) -> np.ndarray | None:
    """Find the largest ink blob in a cell and return it as a cropped image."""
    inv = 255 - cell
    n_labels, labels, stats, _ = cv2.connectedComponentsWithStats(inv, connectivity=8)

    max_area = cell.size * 0.7
    candidates = []
    for lbl in range(1, n_labels):
        area = stats[lbl, cv2.CC_STAT_AREA]
        bw = stats[lbl, cv2.CC_STAT_WIDTH]
        bh = stats[lbl, cv2.CC_STAT_HEIGHT]
        if area < min_area or area > max_area:
            continue
        if bw < 6 or bh < 6:
            continue
        candidates.append((area, lbl))

    if not candidates:
        return None

    candidates.sort(key=lambda x: -x[0])
    best = candidates[0][1]
    bx = stats[best, cv2.CC_STAT_LEFT]
    by = stats[best, cv2.CC_STAT_TOP]
    bw = stats[best, cv2.CC_STAT_WIDTH]
    bh = stats[best, cv2.CC_STAT_HEIGHT]
    pad = max(3, int(0.08 * max(bw, bh)))
    cx0 = max(0, bx - pad)
    cy0 = max(0, by - pad)
    cx1 = min(cell.shape[1], bx + bw + pad)
    cy1 = min(cell.shape[0], by + bh + pad)
    crop = cell[cy0:cy1, cx0:cx1]
    return crop if crop.size > 0 else None


def extract_signs_from_page(
    page_idx: int,
    dry_run: bool = False,
) -> list[tuple[str, np.ndarray]]:
    """Extract sign glyphs from one Appendix I page.

    Uses a uniform cell grid: divides each column into N equal-height cells
    where N = number of expected signs. Then extracts the primary glyph from
    each cell using connected-component analysis.
    """
    page_path = _PAGE_DIR / f"mah_p{page_idx:03d}.png"
    if not page_path.exists():
        print(f"  SKIP: {page_path.name} not found")
        return []

    if page_idx not in PAGE_SIGN_MAP:
        print(f"  SKIP: no sign map for page {page_idx}")
        return []

    sign_map = PAGE_SIGN_MAP[page_idx]
    img = cv2.imread(str(page_path))
    if img is None:
        print(f"  FAIL: cannot read {page_path.name}")
        return []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    h, w = binary.shape
    mid_x = w // 2

    # Table area: skip header (~7% from top) and footer (~5% from bottom)
    table_y0 = int(h * 0.07)
    table_y1 = int(h * 0.93)
    table_h = table_y1 - table_y0

    results: list[tuple[str, np.ndarray]] = []

    for col_key, sign_nums in sign_map.items():
        if not sign_nums:
            continue
        n_signs = len(sign_nums)

        # Column x-bounds; skip left ~12% of each column (sign number labels)
        if col_key == "L":
            col_x0 = int(w * 0.06)   # skip "SIGN No." label area
            col_x1 = mid_x - 5
        else:
            col_x0 = mid_x + int(w * 0.06)
            col_x1 = w - 5

        # Divide the table area into n_signs equal-height cells
        cell_h = table_h // n_signs

        for i, sign_num in enumerate(sign_nums):
            sign_id = f"M{sign_num:03d}"

            # Cell boundaries
            cy0 = table_y0 + i * cell_h
            cy1 = cy0 + cell_h
            cell = binary[cy0:cy1, col_x0:col_x1]

            if cell.size == 0:
                continue

            # Find the primary glyph in this cell
            crop = _find_best_glyph(cell)
            if crop is None:
                print(f"    {sign_id}: no glyph found")
                continue

            normalized = normalize_glyph(crop)
            results.append((sign_id, normalized))

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract Mahadevan sign glyphs from Appendix I pages"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Count signs without saving"
    )
    parser.add_argument(
        "--page", type=int, help="Process a single page index (e.g. 793)"
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing sign images"
    )
    args = parser.parse_args()

    print("Mahadevan 1977 Appendix I — Sign Glyph Extraction\n")

    _STATIC_SIGNS.mkdir(parents=True, exist_ok=True)
    _ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)

    pages = [args.page] if args.page else APPENDIX_I_PAGES
    manifest = _load_manifest()

    total_extracted = 0
    total_saved = 0
    total_skipped = 0

    for page_idx in pages:
        if page_idx not in PAGE_SIGN_MAP:
            continue
        print(f"\n  Page {page_idx} (mah_p{page_idx:03d}.png):")
        results = extract_signs_from_page(page_idx, dry_run=args.dry_run)

        for sign_id, normalized in results:
            total_extracted += 1

            if not args.force and not args.dry_run:
                existing = manifest.get(sign_id, {})
                # Don't overwrite wikimedia or manual uploads
                if existing.get("source") in ("wikimedia", "manual_upload"):
                    total_skipped += 1
                    continue

            if args.dry_run:
                print(f"    {sign_id}: would extract ({normalized.shape})")
                continue

            # Save processed image
            out_path = _STATIC_SIGNS / f"{sign_id}.png"
            Image.fromarray(normalized).convert("L").save(
                str(out_path), optimize=True
            )

            # Save original crop
            orig_path = _ORIGINALS_DIR / f"{sign_id}.png"
            Image.fromarray(normalized).convert("L").save(
                str(orig_path), optimize=True
            )

            # Update manifest
            manifest[sign_id] = {
                "status": "ok",
                "source": f"mahadevan_appendix_i:mah_p{page_idx:03d}",
                "processed_path": f"static\\signs\\{sign_id}.png",
                "original_path": f"static\\signs\\originals\\{sign_id}.png",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            total_saved += 1
            print(f"    {sign_id}: ✓ saved")

        # Save manifest periodically
        if not args.dry_run and total_saved > 0:
            _save_manifest(manifest)

    print(f"\n{'=' * 50}")
    print(f"  Extracted: {total_extracted} signs")
    print(f"  Saved:     {total_saved} new images")
    print(f"  Skipped:   {total_skipped} (existing wikimedia/manual)")
    print(f"  Manifest:  {_MANIFEST_PATH}")

    if not args.dry_run and total_saved > 0:
        _save_manifest(manifest)
        print(f"\n  ✓ Manifest updated with {total_saved} mahadevan_appendix_i entries")


if __name__ == "__main__":
    main()

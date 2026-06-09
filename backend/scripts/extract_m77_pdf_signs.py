#!/usr/bin/env python3
"""Extract specific Indus sign images from the Mahadevan 1977 Sign List PDF.

The PDF (data/page_previews/sukii_m77_sign_list.pdf) contains 4 pages with
all 417 signs in a 10-column grid:
  Page 1 (index 0): signs 1-110   (11 rows × 10 cols)
  Page 2 (index 1): signs 111-219 (11 rows × 10 cols, last row short)
  Page 3 (index 2): signs 220-329 (11 rows × 10 cols, last row short)
  Page 4 (index 3): signs 330-417 (9 rows × 10 cols, last row short)

Usage:
    python scripts/extract_m77_pdf_signs.py
    python scripts/extract_m77_pdf_signs.py --sign M349
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import cv2
import fitz  # PyMuPDF
import numpy as np
from PIL import Image

_SCRIPT_DIR   = Path(__file__).resolve().parent
_BACKEND_DIR  = _SCRIPT_DIR.parent
_PDF_PATH     = _BACKEND_DIR / "data" / "page_previews" / "sukii_m77_sign_list.pdf"
_STATIC_SIGNS = _BACKEND_DIR / "static" / "signs"
_ORIGINALS    = _STATIC_SIGNS / "originals"
_MANIFEST_PATH = _STATIC_SIGNS / "manifest.json"

SIGN_SIZE  = 128
SOURCE_KEY = "m77_pdf"

# Render DPI — higher = sharper crops
RENDER_DPI = 300


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
    _MANIFEST_PATH.write_text(json.dumps(m, indent=2, ensure_ascii=False),
                              encoding="utf-8")


# Actual first sign number on each page (from the PDF scan):
# Page 1: 1-110   (110 signs, 11 rows × 10 cols)
# Page 2: 111-219 (109 signs — last row only 9 wide)
# Page 3: 220-329 (110 signs)
# Page 4: 330-417 (88 signs)
_PAGE_STARTS = [1, 111, 220, 330, 418]  # 418 is a sentinel
# Number of sign rows per page
_PAGE_ROWS   = [11, 11, 11, 9]
# Bottom margin of the sign table (fraction of page height).
# Pages 1-3 fill almost to the bottom; page 4 has a NOTES section
# at ~77-83%, so signs end at ~74%.
_PAGE_BOT    = [0.92, 0.92, 0.92, 0.74]


def sign_to_page_cell(sign_num: int) -> tuple[int, int, int] | None:
    """Return (page_index, row, col) for a given Mahadevan sign number."""
    if not 1 <= sign_num <= 417:
        return None
    for i in range(len(_PAGE_STARTS) - 1):
        if _PAGE_STARTS[i] <= sign_num < _PAGE_STARTS[i + 1]:
            pos = sign_num - _PAGE_STARTS[i]
            row = pos // 10
            col = pos % 10
            return i, row, col
    return None


def normalize(img_arr: np.ndarray) -> np.ndarray:
    """128×128 pure black-on-white from any colour image."""
    if img_arr.ndim == 3:
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
        pad = max(4, int(0.10 * max(r1 - r0, c1 - c0, 1)))
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


def render_page(doc: fitz.Document, page_idx: int) -> np.ndarray:
    """Render a PDF page to a numpy BGR array at RENDER_DPI."""
    page = doc[page_idx]
    mat  = fitz.Matrix(RENDER_DPI / 72, RENDER_DPI / 72)
    pix  = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)
    img  = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)
    return img  # grayscale


def _detect_col_centers(page_img: np.ndarray, n_rows: int = 9,
                        t_bot: float = 0.92) -> list[int] | None:
    """Auto-detect column x-centers from ink clusters in the first complete row.

    Tries rows 0-4 in order and returns the first that yields exactly 10
    clusters.  Returns None only if all rows fail (fallback: uniform spacing).
    """
    h, w = page_img.shape
    t_top = 0.09
    cell_h = (t_bot - t_top) * h / n_rows

    # Try to get actual row starts for more accurate column detection
    row_key = (id(page_img), n_rows, t_bot, "rows")
    row_starts = _ROW_STARTS.get(row_key)

    for row_idx in range(min(5, n_rows)):
        if row_starts and len(row_starts) == n_rows:
            cy0 = row_starts[row_idx]
            next_start = row_starts[row_idx + 1] if row_idx + 1 < n_rows else int(t_bot * h)
            row_h_local = next_start - cy0
        else:
            cy0 = int(t_top * h + row_idx * cell_h)
            row_h_local = int(cell_h)
        cy1 = cy0 + int(row_h_local * 0.55)
        strip = page_img[cy0:cy1, :]
        _, b = cv2.threshold(strip, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if b.mean() < 128:
            b = cv2.bitwise_not(b)
        col_ink = (b < 128).sum(axis=0)
        min_ink = (cy1 - cy0) * 0.012
        ink_x = np.where(col_ink > min_ink)[0]
        if len(ink_x) < 5:
            continue
        breaks = np.where(np.diff(ink_x) > 35)[0]
        groups = np.split(ink_x, breaks + 1)
        groups = [g for g in groups if len(g) > 4]
        if len(groups) == 10:
            return [int((g[0] + g[-1]) // 2) for g in groups]

    return None  # all rows failed; caller will use uniform-spacing fallback


# Page-level column-center cache to avoid re-detecting every call
_COL_CENTERS: dict[tuple, list[int]] = {}
# Page-level row-start cache
_ROW_STARTS: dict[tuple, list[int]] = {}


def _detect_row_starts(page_img: np.ndarray, n_rows: int,
                       t_bot: float = 0.92) -> list[int] | None:
    """Auto-detect the y-start of each sign row from horizontal ink bands.

    Returns a list of *n_rows* y-start pixel positions, or None if the
    number of detected bands doesn't match *n_rows*.
    """
    h, w = page_img.shape
    # Work below the title header (top ~7% of page)
    search_top = int(0.07 * h)
    search_bot = int(t_bot * h)
    strip = page_img[search_top:search_bot, :]

    _, b = cv2.threshold(strip, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if b.mean() < 128:
        b = cv2.bitwise_not(b)

    row_ink = (b < 128).sum(axis=1)
    min_ink  = w * 0.003
    ink_y    = np.where(row_ink > min_ink)[0]
    if len(ink_y) < 5:
        return None

    breaks = np.where(np.diff(ink_y) > 15)[0]
    groups = np.split(ink_y, breaks + 1)
    # Sign rows span ~130-170 px; title and page-number bands are <50 px
    groups = [g for g in groups if len(g) > 50]

    if len(groups) != n_rows:
        return None

    # Return the y-start of each band (adjusted back to full-page coordinates)
    return [int(g[0]) + search_top for g in groups]


def extract_sign_from_page(page_img: np.ndarray, row: int, col: int,
                           n_rows: int = 11,
                           t_bot: float = 0.92) -> np.ndarray | None:
    """Crop one sign cell from a rendered page image.

    First attempts to auto-detect the 10 column x-centers from row-0 ink
    clusters (which handles uneven margins accurately), then falls back to
    uniform spacing if detection fails.
    """
    h, w = page_img.shape[:2]

    # ── Row y-bounds: use auto-detected ink-band starts if available ─────
    row_cache_key = (id(page_img), n_rows, t_bot, "rows")
    if row_cache_key not in _ROW_STARTS:
        _ROW_STARTS[row_cache_key] = _detect_row_starts(page_img, n_rows, t_bot)

    row_starts = _ROW_STARTS.get(row_cache_key)
    if row_starts and len(row_starts) == n_rows:
        cy0 = row_starts[row]
        # Row height = distance to the next row's start (or page bottom for last row)
        if row + 1 < n_rows:
            row_h = row_starts[row + 1] - cy0
        else:
            row_h = int(t_bot * h) - cy0
    else:
        # Fallback: uniform spacing
        t_top  = 0.09
        cell_h = (t_bot - t_top) * h / n_rows
        cy0    = int(t_top * h + row * cell_h)
        row_h  = int(cell_h)

    # label_frac: fraction of ROW HEIGHT to drop from the bottom.
    # Each ink band = sign glyph (~50%) + number label (~35%) + gap (~15%).
    # Keeping only the top 50% of the ink band isolates the glyph cleanly.
    label_frac = 0.50
    cy1 = cy0 + int(row_h * (1 - label_frac))

    # ── Column x-bounds: try auto-detection first ─────────────────────────
    cache_key = (id(page_img), n_rows, t_bot)
    if cache_key not in _COL_CENTERS:
        _COL_CENTERS[cache_key] = _detect_col_centers(page_img, n_rows, t_bot)

    centers = _COL_CENTERS.get(cache_key)
    if centers and len(centers) == 10:
        # Use detected center ± (half-neighbour-gap) with a small inward
        # trim (6 px each side at 300 dpi ≈ 0.5 mm) to prevent adjacent-
        # sign strokes from bleeding while not clipping wide glyphs.
        cx_center = centers[col]
        if col > 0:
            half = (cx_center - centers[col - 1]) // 2
        elif col < 9:
            half = (centers[col + 1] - cx_center) // 2
        else:
            half = 130
        cx0 = max(0, cx_center - half + 6)
        cx1 = min(w, cx_center + half - 6)
    else:
        # Fallback: uniform spacing with ~3% inward crop per side
        t_left, t_right = 0.03, 0.97
        cell_w = (t_right - t_left) * w / 10
        inset = int(cell_w * 0.04)
        cx0 = int(t_left * w + col * cell_w) + inset
        cx1 = min(int(cx0 + cell_w) - inset * 2, w)

    cell = page_img[cy0:cy1, cx0:cx1]
    return cell if cell.size > 0 else None


def save_sign(sign_id: str, proc: np.ndarray, orig: np.ndarray,
              manifest: dict) -> None:
    _STATIC_SIGNS.mkdir(parents=True, exist_ok=True)
    _ORIGINALS.mkdir(parents=True, exist_ok=True)
    proc_path = _STATIC_SIGNS / f"{sign_id}.png"
    Image.fromarray(proc).convert("L").save(str(proc_path), optimize=True)
    orig_path = _ORIGINALS / f"{sign_id}.png"
    Image.fromarray(orig).convert("L").save(str(orig_path), optimize=True)
    manifest[sign_id] = {
        "status": "ok",
        "source": SOURCE_KEY,
        "processed_path": str(proc_path.relative_to(_BACKEND_DIR)),
        "original_path": str(orig_path.relative_to(_BACKEND_DIR)),
        "timestamp": _now(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sign",  metavar="ID",
                        help="Process one sign (e.g. M349)")
    parser.add_argument("--force", action="store_true",
                        help="Re-extract even if already done")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not _PDF_PATH.exists():
        print(f"ERROR: PDF not found at {_PDF_PATH}")
        sys.exit(1)

    manifest = load_manifest()
    doc = fitz.open(str(_PDF_PATH))
    n_pages = len(doc)
    print(f"PDF: {n_pages} pages")

    # Which signs to process
    if args.sign:
        sid = args.sign
        try:
            n = int(sid.lstrip("M"))
        except ValueError:
            print(f"ERROR: invalid sign ID {sid}")
            sys.exit(1)
        targets = [(sid, n)]
    else:
        # All fallback signs that are in M001-M417 range
        targets = []
        for sid, entry in manifest.items():
            if entry.get("source") not in ("fallback_icon", "", None):
                if not args.force:
                    continue
            if not sid.startswith("M"):
                continue
            try:
                n = int(sid[1:])
            except ValueError:
                continue
            if 1 <= n <= 417:
                targets.append((sid, n))

    if not targets:
        print("Nothing to do.")
        return

    print(f"\nTargets: {len(targets)} signs")
    if args.dry_run:
        for sid, n in sorted(targets):
            loc = sign_to_page_cell(n)
            print(f"  {sid} (#{n}): page={loc[0]+1}, row={loc[1]}, col={loc[2]}"
                  if loc else f"  {sid}: OUT OF RANGE")
        return

    # Cache rendered pages to avoid re-rendering
    page_cache: dict[int, np.ndarray] = {}
    saved = 0
    failed = 0
    skipped = 0

    for sid, n in sorted(targets):
        loc = sign_to_page_cell(n)
        if not loc:
            skipped += 1
            continue
        page_idx, row, col = loc

        if page_idx >= n_pages:
            print(f"  SKIP {sid}: page {page_idx+1} out of range")
            skipped += 1
            continue

        if page_idx not in page_cache:
            print(f"  Rendering page {page_idx + 1}…")
            page_cache[page_idx] = render_page(doc, page_idx)

        page_img = page_cache[page_idx]

        n_rows = _PAGE_ROWS[page_idx]
        t_bot  = _PAGE_BOT[page_idx]
        cell = extract_sign_from_page(page_img, row, col, n_rows=n_rows, t_bot=t_bot)
        if cell is None or cell.size == 0:
            print(f"  FAIL {sid}: empty cell")
            failed += 1
            continue

        try:
            proc = normalize(cell)
            black = float(np.sum(proc < 128)) / proc.size
            if not (0.003 <= black <= 0.70):
                print(f"  SKIP {sid} (#{n}): bad density {black:.4f}")
                skipped += 1
                continue
            save_sign(sid, proc, cell, manifest)
            saved += 1
            print(f"  ✓ {sid} (#{n}) p{page_idx+1}[r{row}c{col}] density={black:.3f}")
        except Exception as exc:
            print(f"  FAIL {sid}: {exc}")
            failed += 1

        if saved % 20 == 0 and saved > 0:
            save_manifest(manifest)

    save_manifest(manifest)
    print(f"\nDone: saved={saved} failed={failed} skipped={skipped}")


if __name__ == "__main__":
    main()

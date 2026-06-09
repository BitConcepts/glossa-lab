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
# Number of rows per page (used for cell-height calculation)
_PAGE_ROWS   = [11, 11, 11, 9]


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


def _detect_col_centers(page_img: np.ndarray, n_rows: int = 9) -> list[int] | None:
    """Auto-detect column x-centers from ink clusters in the first data row.

    Returns a list of 10 x-pixel centers, one per column, or None if detection
    fails.
    """
    h, w = page_img.shape
    t_top, t_bot = 0.09, 0.92
    cell_h = (t_bot - t_top) * h / n_rows
    # Use row 0 (most complete) to detect column positions
    cy0 = int(t_top * h)
    cy1 = cy0 + int(cell_h * 0.65)
    strip = page_img[cy0:cy1, :]
    _, b = cv2.threshold(strip, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if b.mean() < 128:
        b = cv2.bitwise_not(b)
    col_ink = (b < 128).sum(axis=0)
    min_ink = (cy1 - cy0) * 0.015
    ink_x = np.where(col_ink > min_ink)[0]
    if len(ink_x) < 5:
        return None
    breaks = np.where(np.diff(ink_x) > 40)[0]
    groups = np.split(ink_x, breaks + 1)
    groups = [g for g in groups if len(g) > 5]  # filter noise
    if len(groups) != 10:
        # Fallback: not exactly 10 clusters — use uniform spacing
        return None
    return [int((g[0] + g[-1]) // 2) for g in groups]


# Page-level column-center cache to avoid re-detecting every call
_COL_CENTERS: dict[tuple, list[int]] = {}


def extract_sign_from_page(page_img: np.ndarray, row: int, col: int,
                           n_rows: int = 11) -> np.ndarray | None:
    """Crop one sign cell from a rendered page image.

    First attempts to auto-detect the 10 column x-centers from row-0 ink
    clusters (which handles uneven margins accurately), then falls back to
    uniform spacing if detection fails.
    """
    h, w = page_img.shape[:2]
    t_top = 0.09
    t_bot = 0.92
    table_h = (t_bot - t_top) * h
    cell_h  = table_h / n_rows
    label_frac = 0.32

    # ── Row y-bounds ─────────────────────────────────────────────────────────
    cy0 = int(t_top * h + row * cell_h)
    cy1 = cy0 + int(cell_h * (1 - label_frac))

    # ── Column x-bounds: try auto-detection first ─────────────────────────
    cache_key = (id(page_img), n_rows)
    if cache_key not in _COL_CENTERS:
        _COL_CENTERS[cache_key] = _detect_col_centers(page_img, n_rows)

    centers = _COL_CENTERS.get(cache_key)
    if centers and len(centers) == 10:
        # Use detected center; crop ±half_cell around it
        cx_center = centers[col]
        # Estimate half-width from neighbour spacing
        if col > 0:
            half = (cx_center - centers[col - 1]) // 2
        elif col < 9:
            half = (centers[col + 1] - cx_center) // 2
        else:
            half = 130
        cx0 = max(0, cx_center - half - 10)
        cx1 = min(w, cx_center + half + 10)
    else:
        # Fallback: uniform spacing
        t_left, t_right = 0.03, 0.97
        cell_w = (t_right - t_left) * w / 10
        cx0 = int(t_left * w + col * cell_w)
        cx1 = min(int(cx0 + cell_w), w)

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
        cell = extract_sign_from_page(page_img, row, col, n_rows=n_rows)
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

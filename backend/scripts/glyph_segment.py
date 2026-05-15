"""Mahadevan 1977 — Glyph segmentation.

Strategy: anchor-based row extraction.
  1. Run Tesseract with bounding box output on the left column
  2. Find bounding boxes of 4-digit IM77 textnums (1000–9999)
  3. Each textnum bbox gives the y-center of that row
  4. Extract the sign column to the right at that y-position
  5. Segment individual glyphs within the row using column projection

Output:
  ocr_results/glyph_crops/{textnum}/row.png        — full row image
  ocr_results/glyph_crops/{textnum}/glyph_{N}.png  — individual glyph (64x64)
  ocr_results/glyph_crops/segment_report.json       — all bboxes and crops

Usage:
    shell.cmd python backend/scripts/glyph_segment.py --test    (5 pages)
    shell.cmd python backend/scripts/glyph_segment.py --all     (all TEXTS pages)
    shell.cmd python backend/scripts/glyph_segment.py --page 0101
"""
from __future__ import annotations
import argparse, json, os, sys
from datetime import datetime
from pathlib import Path
import numpy as np
import cv2

REPO = Path(__file__).parents[2]
M77  = REPO / "glossa-corpus/indus/sources/internet-archive/raw/2026-05-14/images/mahadevan1977"
IDX  = REPO / "glossa-corpus/indus/ocr_results/m77_page_index.json"
OUT  = REPO / "glossa-corpus/indus/ocr_results/glyph_crops"
OUT.mkdir(parents=True, exist_ok=True)

# Page geometry (calibrated from probe + visual inspection)
# M77 page structure at 1800px:
#   0-15%:   text number column (4-digit: 3227)
#   15-42%:  catalog number column (6-digit: 219709 or sub-code: 0001)
#   42-100%: sign drawing area
SIGN_COL_X  = 0.42   # sign column starts at 42% (past catalog numbers)
NUM_COL_END = 0.28   # OCR column for textnum detection (first 28%)
BODY_Y_TOP  = 0.12   # skip header
BODY_Y_BOT  = 0.95   # skip page number
GLYPH_SIZE  = 64     # pixels for normalized glyph output
ROW_PAD     = 4      # px padding around row (tight — avoid capturing sub-entries)
GLYPH_PAD   = 3      # px padding around each glyph


def setup_tesseract():
    import pytesseract, os
    tess = Path.home() / "scoop/apps/tesseract/current/tesseract.exe"
    tessdata = Path.home() / "scoop/apps/tesseract/current/tessdata"
    if tess.exists():
        pytesseract.pytesseract.tesseract_cmd = str(tess)
        os.environ["TESSDATA_PREFIX"] = str(tessdata)
    return pytesseract


def preprocess(img_gray: np.ndarray) -> np.ndarray:
    """Binarize with a fixed threshold suited to M77's cream background."""
    # Cream background ~220-240, text ~30-80 — threshold at 160 works well
    _, binary = cv2.threshold(img_gray, 160, 255, cv2.THRESH_BINARY)
    return binary


def find_textnum_rows(img_path: Path, pytesseract) -> list[dict]:
    """
    Use Tesseract to find bounding boxes of 4-digit textnums in left column.
    Returns list of {textnum, x, y, w, h, cx, cy}.
    """
    import re
    img_bgr = cv2.imread(str(img_path))
    if img_bgr is None:
        return []
    H, W = img_bgr.shape[:2]
    # Crop left column only (faster OCR)
    x_end = int(W * NUM_COL_END)
    y_start = int(H * BODY_Y_TOP)
    y_end   = int(H * BODY_Y_BOT)
    left_col = img_bgr[y_start:y_end, :x_end]
    # 2x upscale for better OCR
    left_up = cv2.resize(left_col, (x_end * 2, (y_end - y_start) * 2))
    # Get word bounding boxes
    try:
        data = pytesseract.image_to_data(
            left_up, config="--psm 6 --oem 3",
            output_type=pytesseract.Output.DICT
        )
    except Exception:
        return []
    rows = []
    for i, text in enumerate(data["text"]):
        text = (text or "").strip()
        if not re.match(r'^[1-9][0-9]{3}$', text):
            continue
        conf = int(data["conf"][i])
        if conf < 30:
            continue
        # Bounding box in upscaled coords — convert back to original
        bx = data["left"][i] // 2
        by = data["top"][i] // 2 + y_start
        bw = data["width"][i] // 2
        bh = data["height"][i] // 2
        rows.append({
            "textnum": int(text),
            "x": bx, "y": by, "w": bw, "h": bh,
            "cx": bx + bw // 2,
            "cy": by + bh // 2,
            "conf": conf,
        })
    # Deduplicate by textnum (keep highest conf)
    best: dict[int, dict] = {}
    for r in rows:
        tn = r["textnum"]
        if tn not in best or r["conf"] > best[tn]["conf"]:
            best[tn] = r
    return sorted(best.values(), key=lambda r: r["cy"])


def segment_row_glyphs(img_bgr: np.ndarray, row_y_center: int,
                        row_height: int) -> list[np.ndarray]:
    """Extract individual glyph images from the sign column of a row."""
    H, W = img_bgr.shape[:2]
    sign_x = int(W * SIGN_COL_X)
    # Row bounds
    half = row_height // 2 + ROW_PAD
    y0 = max(0, row_y_center - half)
    y1 = min(H, row_y_center + half)
    # Extract sign area
    row_img = img_bgr[y0:y1, sign_x:]
    row_gray = cv2.cvtColor(row_img, cv2.COLOR_BGR2GRAY)
    binary = preprocess(row_gray)
    # Column projection to find glyph boundaries
    # Invert: dark pixels = 0 in binary (text is black on white after threshold)
    # In our binary: text = 0, background = 255
    col_profile = np.sum(binary == 0, axis=0)  # dark pixel count per column
    # Find glyph column runs
    in_glyph = False
    glyph_cols = []
    start = 0
    for ci, v in enumerate(col_profile):
        if v > 0 and not in_glyph:
            start = ci
            in_glyph = True
        elif v == 0 and in_glyph:
            if ci - start >= 3:  # min glyph width
                glyph_cols.append((start, ci))
            in_glyph = False
    if in_glyph and len(col_profile) - start >= 3:
        glyph_cols.append((start, len(col_profile)))
    # Merge adjacent segments separated by tiny gaps (ligatures)
    merged = []
    for gc in glyph_cols:
        if merged and gc[0] - merged[-1][1] <= 4:
            merged[-1] = (merged[-1][0], gc[1])
        else:
            merged.append(list(gc))
    glyph_cols = [tuple(m) for m in merged]
    # Crop each glyph
    glyphs = []
    for c0, c1 in glyph_cols:
        x0 = max(0, c0 - GLYPH_PAD)
        x1 = min(row_img.shape[1], c1 + GLYPH_PAD)
        glyph = row_img[:, x0:x1]
        if glyph.size > 0 and glyph.shape[1] >= 5:
            glyph_sq = cv2.resize(glyph, (GLYPH_SIZE, GLYPH_SIZE))
            glyphs.append(glyph_sq)
    return glyphs


def process_page(img_path: Path, pytesseract) -> dict:
    """Extract glyph crops for all textnums on a page."""
    img_bgr = cv2.imread(str(img_path))
    if img_bgr is None:
        return {"file": img_path.name, "status": "load_error"}
    H, W = img_bgr.shape[:2]
    # Find textnum row anchors
    rows = find_textnum_rows(img_path, pytesseract)
    if not rows:
        return {"file": img_path.name, "status": "no_textnums", "rows": 0}
    # Estimate typical row height from sorted y-positions
    if len(rows) > 1:
        gaps = [rows[i+1]["cy"] - rows[i]["cy"] for i in range(len(rows)-1)]
        typical_height = int(np.percentile(gaps, 30)) if gaps else 60
    else:
        typical_height = 60
    typical_height = max(40, min(120, typical_height))
    page_result = {
        "file": img_path.name,
        "status": "ok",
        "rows": len(rows),
        "textnums": [],
    }
    for row in rows:
        tn = row["textnum"]
        glyphs = segment_row_glyphs(img_bgr, row["cy"], typical_height)
        if not glyphs:
            continue
        # Save glyphs
        glyph_dir = OUT / str(tn)
        glyph_dir.mkdir(exist_ok=True)
        # Save full row
        sign_x = int(W * SIGN_COL_X)
        half = typical_height // 2 + ROW_PAD
        y0 = max(0, row["cy"] - half)
        y1 = min(H, row["cy"] + half)
        row_img = img_bgr[y0:y1, sign_x:]
        cv2.imwrite(str(glyph_dir / "row.png"), row_img)
        # Save individual glyphs
        for gi, glyph in enumerate(glyphs):
            cv2.imwrite(str(glyph_dir / f"glyph_{gi:02d}.png"), glyph)
        page_result["textnums"].append({
            "textnum": tn, "glyphs": len(glyphs),
            "y": row["cy"], "conf": row["conf"],
        })
    return page_result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Process 5 TEXTS pages")
    parser.add_argument("--all", action="store_true", help="All TEXTS pages")
    parser.add_argument("--page", type=str, default=None, help="Process one page fragment")
    args = parser.parse_args()

    pytesseract = setup_tesseract()

    # Load page index
    index_data = json.loads(IDX.read_text())
    texts_pages = [p["file"] for p in index_data["pages"] if p["type"] == "TEXTS"]
    print(f"=== M77 Glyph Segmentation ===")
    print(f"TEXTS pages: {len(texts_pages)}")

    # Select pages
    if args.page:
        candidates = [f for f in sorted(M77.glob("*.jpg")) if args.page in f.name]
        to_process = candidates[:1]
    elif args.test:
        to_process = [M77 / f for f in texts_pages[:5]]
    elif args.all:
        to_process = [M77 / f for f in texts_pages]
    else:
        print("Use --test, --all, or --page FRAGMENT")
        return 0

    print(f"Processing: {len(to_process)} pages")
    all_results = []
    total_textnums = 0

    for i, pg in enumerate(to_process):
        if not pg.exists():
            continue
        print(f"  [{i+1:3d}/{len(to_process)}] {pg.name}...", end=" ", flush=True)
        result = process_page(pg, pytesseract)
        all_results.append(result)
        n = len(result.get("textnums", []))
        total_textnums += n
        glyphs_total = sum(r["glyphs"] for r in result.get("textnums", []))
        print(f"{n} textnums, {glyphs_total} glyphs")

    print(f"\n=== Done ===")
    print(f"  Pages: {len(all_results)}")
    print(f"  Textnums with crops: {total_textnums}")
    print(f"  Glyph dirs: {OUT}")

    report = {
        "_citation": {"primary_sources": ["I.8", "A.1"]},
        "generated_at": datetime.utcnow().isoformat(),
        "pages_processed": len(all_results),
        "total_textnums": total_textnums,
        "results": all_results,
    }
    (OUT / "segment_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  Report: {OUT / 'segment_report.json'}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

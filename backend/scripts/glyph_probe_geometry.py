"""Probe M77 page geometry to understand row and glyph structure.

Uses OpenCV to:
1. Find horizontal row boundaries using projection profile
2. Identify the text-number column vs glyph column boundary
3. Within one row, find vertical glyph boundaries
4. Save annotated image + geometry report

Must be run BEFORE building the full pipeline.
Run on page 0101 (confirmed TEXTS/MOHENJODARO, book page 91).

Usage: shell.cmd python backend/scripts/glyph_probe_geometry.py
"""
import json, os, sys
from pathlib import Path
import numpy as np
import cv2
from PIL import Image

REPO = Path(__file__).parents[2]
M77 = REPO / "glossa-corpus/indus/sources/internet-archive/raw/2026-05-14/images/mahadevan1977"
OUT = REPO / "glossa-corpus/indus/ocr_results/geometry_probe"
OUT.mkdir(parents=True, exist_ok=True)

def load_page(name_fragment: str):
    imgs = [f for f in sorted(M77.glob("*.jpg")) if name_fragment in f.name]
    if not imgs:
        raise FileNotFoundError(f"No image matching {name_fragment}")
    return imgs[0]

def projection_profile(binary_img, axis=0):
    """Sum of dark pixels along axis (0=rows, 1=cols)."""
    return np.sum(binary_img == 0, axis=axis)

def find_runs(profile, threshold, min_gap=5, min_segment=10):
    """Find contiguous segments above threshold in projection profile."""
    above = profile > threshold
    segments = []
    in_seg = False
    start = 0
    for i, v in enumerate(above):
        if v and not in_seg:
            start = i
            in_seg = True
        elif not v and in_seg:
            if i - start >= min_segment:
                segments.append((start, i))
            in_seg = False
    if in_seg and len(above) - start >= min_segment:
        segments.append((start, len(above)))
    # Merge segments separated by small gaps
    merged = []
    for seg in segments:
        if merged and seg[0] - merged[-1][1] < min_gap:
            merged[-1] = (merged[-1][0], seg[1])
        else:
            merged.append(list(seg))
    return [tuple(s) for s in merged]

def main():
    print("=== M77 Page Geometry Probe ===")

    # Load page 0101 (confirmed MOHENJODARO TEXTS)
    page_path = load_page("0101")
    print(f"Page: {page_path.name}")

    # Load as numpy via OpenCV
    img_bgr = cv2.imread(str(page_path))
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    h, w = img_gray.shape
    print(f"Size: {w}x{h}")

    # Binary threshold (Otsu's)
    _, binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # --- 1. Find rows using horizontal projection ---
    # Skip top 12% (header) and bottom 5% (page number)
    body_start = int(h * 0.12)
    body_end   = int(h * 0.95)
    body = binary[body_start:body_end, :]

    h_profile = projection_profile(body, axis=1)  # sum across columns per row

    # Rows have dark pixels; gaps between rows are white
    row_segments = find_runs(h_profile, threshold=3, min_gap=3, min_segment=15)
    print(f"\nRows found: {len(row_segments)}")
    for i, (r0, r1) in enumerate(row_segments[:5]):
        print(f"  Row {i}: y={r0+body_start}–{r1+body_start} ({r1-r0}px tall)")

    # --- 2. Find column split: left numbers vs right glyphs ---
    # The sign area starts after the text/catalog numbers (~28% from left based on OCR)
    # Probe the vertical profile in the sign area
    sign_x_start = int(w * 0.28)
    right_col = body[:, sign_x_start:]
    v_profile_right = projection_profile(right_col, axis=0)  # sum per column in sign area

    print(f"\nSign area: x={sign_x_start}–{w} ({w - sign_x_start}px wide)")

    # --- 3. Within one row, find individual glyphs ---
    # Use row 3 (likely to have actual signs)
    if len(row_segments) >= 4:
        test_row = row_segments[3]
        r0, r1 = test_row[0] + body_start, test_row[1] + body_start
        row_img = binary[r0:r1, sign_x_start:]
        row_h, row_w = row_img.shape

        # Vertical projection within this row
        v_profile = projection_profile(row_img, axis=0)
        glyph_segs = find_runs(v_profile, threshold=1, min_gap=2, min_segment=5)
        print(f"\nTest row (y={r0}–{r1}, {r1-r0}px tall):")
        print(f"  Glyphs found: {len(glyph_segs)}")
        for i, (c0, c1) in enumerate(glyph_segs[:15]):
            print(f"    Glyph {i}: x={c0}–{c1} ({c1-c0}px wide)")

        # Save row image for inspection
        row_img_color = img_bgr[r0:r1, sign_x_start:]
        cv2.imwrite(str(OUT / "test_row.png"), row_img_color)

        # Save individual glyph crops
        glyph_dir = OUT / "test_glyphs"
        glyph_dir.mkdir(exist_ok=True)
        for i, (c0, c1) in enumerate(glyph_segs[:20]):
            # Add padding
            pad = 5
            x0 = max(0, c0 - pad)
            x1 = min(row_w, c1 + pad)
            glyph = row_img_color[:, x0:x1]
            # Normalize to standard size
            if glyph.size > 0:
                glyph_resized = cv2.resize(glyph, (64, 64))
                cv2.imwrite(str(glyph_dir / f"glyph_{i:02d}.png"), glyph_resized)

        print(f"  Saved: {OUT / 'test_row.png'}")
        print(f"  Glyphs saved to: {glyph_dir}")

    # --- 4. Annotated full page ---
    annotated = img_bgr.copy()
    # Draw row boundaries
    for r0, r1 in row_segments:
        y0, y1 = r0 + body_start, r1 + body_start
        cv2.rectangle(annotated, (0, y0), (w, y1), (0, 255, 0), 1)
    # Draw sign column boundary
    cv2.line(annotated, (sign_x_start, 0), (sign_x_start, h), (0, 0, 255), 2)
    # Scale down for saving
    scale = 0.4
    small = cv2.resize(annotated, (int(w*scale), int(h*scale)))
    cv2.imwrite(str(OUT / "annotated_page.png"), small)
    print(f"\nAnnotated page: {OUT / 'annotated_page.png'}")

    # --- 5. Geometry report ---
    report = {
        "page": page_path.name,
        "size": {"w": w, "h": h},
        "body_region": {"y_start": body_start, "y_end": body_end},
        "sign_column_x_start": sign_x_start,
        "rows_found": len(row_segments),
        "row_height_avg": int(np.mean([r1-r0 for r0,r1 in row_segments])) if row_segments else 0,
        "row_height_min": min(r1-r0 for r0,r1 in row_segments) if row_segments else 0,
        "row_height_max": max(r1-r0 for r0,r1 in row_segments) if row_segments else 0,
        "sample_rows": [(r0+body_start, r1+body_start) for r0,r1 in row_segments[:10]],
    }
    (OUT / "geometry_report.json").write_text(json.dumps(report, indent=2))
    print(f"Geometry report: {OUT / 'geometry_report.json'}")
    print(f"\nRow height avg: {report['row_height_avg']}px, range: {report['row_height_min']}–{report['row_height_max']}px")
    print("\nNext: inspect annotated_page.png and test_glyphs/ to verify segmentation quality")
    return 0

if __name__ == "__main__":
    sys.exit(main())

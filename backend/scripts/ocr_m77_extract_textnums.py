"""Mahadevan 1977 — Text number extractor.

Extracts 4-digit IM77 text numbers from the left column of
TEXTS and CONCORDANCE pages using Tesseract OCR.

Page structure (observed from images):
  TEXTS page:       [textnum] [6-digit catalog] [sign drawings...]
  CONCORDANCE page: [textnum] [sub-code 00/10/20] [sign drawings...]

The left ~25% of the page width contains only numbers — ideal for
digit-mode OCR (high accuracy, no risk of glyph misidentification).

Validation: valid textnums are 4-digit integers, first digit 1-9.
Pattern: NNN[0-9] where N in 1-9. Range observed: 1001-9905.

Usage:
    shell.cmd python backend/scripts/ocr_m77_extract_textnums.py --test
    shell.cmd python backend/scripts/ocr_m77_extract_textnums.py --pages-file page_index.json
    shell.cmd python backend/scripts/ocr_m77_extract_textnums.py --all

Output:
    ocr/textnums_raw.json    — per-page extraction results
    ocr/textnums_all.txt     — flat deduplicated sorted list
    ocr/textnums_missing.json — diff vs our known 2,906 texts
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parents[2]
IA_RAW = REPO / "glossa-corpus/indus/sources/internet-archive/raw"
M77_DIR = sorted(IA_RAW.iterdir())[-1] / "images" / "mahadevan1977"
OCR_DIR = sorted(IA_RAW.iterdir())[-1] / "ocr"
OCR_DIR.mkdir(parents=True, exist_ok=True)

# Known textnums from our Firestore dump
KNOWN_TEXTNUMS_PATH = (REPO / "glossa-corpus/indus/sources/rmrl/raw/indusscript-probe"
                       / "firestore_indusarrays_full.json")

# Tesseract config for digit-heavy left column
# PSM 6 = single uniform block; digits config for high precision
TESS_DIGITS_CONFIG = "--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789 "
TESS_NUM_CONFIG = "--psm 6 --oem 3"


def setup_tesseract():
    import pytesseract, os
    tess_path = Path.home() / "scoop" / "apps" / "tesseract" / "current" / "tesseract.exe"
    tessdata = Path.home() / "scoop" / "apps" / "tesseract" / "current" / "tessdata"
    if tess_path.exists():
        pytesseract.pytesseract.tesseract_cmd = str(tess_path)
        os.environ["TESSDATA_PREFIX"] = str(tessdata)
    return pytesseract


def extract_textnums_from_page(img_path: Path, pytesseract, pil_Image,
                                cv2=None) -> list[int]:
    """Extract all valid 4-digit text numbers from the left column of a page."""
    img = pil_Image.open(img_path)
    w, h = img.size

    # Crop left 28% — text numbers + catalog codes, no sign drawings
    # Skip top 12% (header) and bottom 5% (page number)
    left_col = img.crop((0, int(h * 0.12), int(w * 0.28), int(h * 0.95)))

    # Upscale for better OCR accuracy (Tesseract works best at 300+ DPI equivalent)
    scale = 2
    try:
        resample = pil_Image.LANCZOS
    except AttributeError:
        resample = pil_Image.Resampling.LANCZOS
    left_col = left_col.resize(
        (left_col.width * scale, left_col.height * scale),
        resample
    )

    # OCR with number-friendly config
    raw = pytesseract.image_to_string(left_col, config=TESS_NUM_CONFIG)

    # Extract all 4-digit numbers that look like valid IM77 textnums
    # Valid: 1000-9999 range, first digit 1-9
    candidates = re.findall(r'\b([1-9][0-9]{3})\b', raw)
    textnums = sorted(set(int(t) for t in candidates))

    # Filter out obvious false positives (catalog numbers are 6-digit, sub-codes are 2-digit)
    # Sub-codes: 00, 01, 02, 10, 20 — 2-digit, won't match 4-digit pattern
    # Catalog codes: 6-digit — won't match either
    # Page numbers at bottom (e.g. "91", "191") — 2-3 digit, won't match
    return textnums


def load_known_textnums() -> set[int]:
    """Load the 2,906 textnums we already have from Firestore."""
    if not KNOWN_TEXTNUMS_PATH.exists():
        print(f"WARNING: Known textnums file not found: {KNOWN_TEXTNUMS_PATH}")
        return set()
    data = json.loads(KNOWN_TEXTNUMS_PATH.read_text(encoding="utf-8"))
    docs = data.get("documents", [])
    textnums = set()
    for doc in docs:
        tn = doc.get("textnum")
        if tn is not None:
            textnums.add(int(tn))
    print(f"  Known textnums from Firestore: {len(textnums)}")
    return textnums


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true",
                        help="Test on 5 known TEXTS pages only")
    parser.add_argument("--all", action="store_true",
                        help="Process all pages")
    parser.add_argument("--pages-file", type=str, default=None,
                        help="Path to page_index.json from classifier")
    parser.add_argument("--type", choices=["TEXTS", "CONCORDANCE", "both"],
                        default="TEXTS", help="Which page types to process")
    args = parser.parse_args()

    try:
        pytesseract = setup_tesseract()
        from PIL import Image as pil_Image
    except ImportError as e:
        print(f"ERROR: {e}")
        return 1

    images = sorted(M77_DIR.glob("*.jpg"))
    if not images:
        print(f"ERROR: No images found at {M77_DIR}")
        return 1

    print(f"=== Mahadevan 1977 — Text Number Extractor ===")
    print(f"Images available: {len(images)}")

    # Load page index if available
    page_index = {}
    index_path = OCR_DIR / "page_index.json"
    if index_path.exists():
        index_data = json.loads(index_path.read_text())
        page_index = {p["file"]: p["type"] for p in index_data.get("pages", [])}
        print(f"Page index loaded: {len(page_index)} classified pages")

    # Select pages to process
    if args.test:
        # Use 5 pages from the known texts section (around page 0101 which we saw)
        # Based on our visual inspection: pages 0070-0350 appear to be texts/concordance
        test_indices = [83, 84, 85, 101, 102]  # 0-indexed
        to_process = [images[i] for i in test_indices if i < len(images)]
        print(f"TEST MODE: processing {len(to_process)} pages")
    elif args.all:
        if page_index:
            target_types = {"TEXTS", "CONCORDANCE"} if args.type == "both" else {args.type}
            to_process = [img for img in images
                          if page_index.get(img.name, "UNKNOWN") in target_types]
            print(f"Processing {len(to_process)} {args.type} pages from index")
        else:
            to_process = images
            print(f"Processing all {len(to_process)} pages (no index — classifying on the fly)")
    else:
        print("Use --test for a quick test, or --all to process everything")
        print("Run ocr_m77_classify.py first to build the page index")
        return 0

    print()
    all_textnums: set[int] = set()
    per_page_results = []

    for i, img_path in enumerate(to_process):
        print(f"  [{i+1:3d}/{len(to_process)}] {img_path.name}...", end=" ", flush=True)
        textnums = extract_textnums_from_page(img_path, pytesseract, pil_Image)
        all_textnums.update(textnums)
        print(f"{len(textnums)} textnums: {textnums[:5]}{'...' if len(textnums) > 5 else ''}")
        per_page_results.append({
            "file": img_path.name,
            "page_type": page_index.get(img_path.name, "UNKNOWN"),
            "textnums": textnums,
            "count": len(textnums),
        })

    print()
    print(f"=== Results ===")
    print(f"  Pages processed: {len(to_process)}")
    print(f"  Unique textnums found: {len(all_textnums)}")
    if all_textnums:
        print(f"  Range: {min(all_textnums)} – {max(all_textnums)}")

    # Compare with known
    known = load_known_textnums()
    if known:
        new_found = all_textnums - known
        print(f"  NEW textnums not in Firestore: {len(new_found)}")
        if new_found:
            print(f"  Sample new: {sorted(new_found)[:10]}")

    # Save outputs
    raw_out = OCR_DIR / "textnums_raw.json"
    existing_raw = {}
    if raw_out.exists():
        try:
            existing_raw = {p["file"]: p for p in json.loads(raw_out.read_text())["pages"]}
        except Exception:
            pass
    for p in per_page_results:
        existing_raw[p["file"]] = p

    raw_out.write_text(json.dumps({
        "_citation": {"primary_sources": ["I.8", "A.1"]},
        "extracted_at": datetime.utcnow().isoformat(),
        "pages": sorted(existing_raw.values(), key=lambda x: x["file"]),
    }, indent=2), encoding="utf-8")

    # All textnums (accumulate across runs)
    cumulative_all: set[int] = set()
    all_out = OCR_DIR / "textnums_all.txt"
    if all_out.exists():
        cumulative_all = set(int(x) for x in all_out.read_text().splitlines() if x.strip().isdigit())
    cumulative_all.update(all_textnums)
    all_out.write_text("\n".join(str(t) for t in sorted(cumulative_all)), encoding="utf-8")

    # Missing textnums
    if known:
        missing_from_firestore = cumulative_all - known
        (OCR_DIR / "textnums_missing.json").write_text(json.dumps({
            "_citation": {"primary_sources": ["I.8", "A.1"]},
            "generated_at": datetime.utcnow().isoformat(),
            "known_count": len(known),
            "ocr_found_count": len(cumulative_all),
            "new_not_in_firestore": sorted(missing_from_firestore),
            "note": ("These textnums appear in Mahadevan 1977 but not in indusscript.in Firestore. "
                     "They represent the gap between what RMRL digitized and the full IM77 concordance."),
        }, indent=2), encoding="utf-8")
        print(f"\n  Missing textnums saved: {OCR_DIR / 'textnums_missing.json'}")

    print(f"\nSaved:")
    print(f"  {raw_out}")
    print(f"  {all_out} ({len(cumulative_all)} total textnums)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

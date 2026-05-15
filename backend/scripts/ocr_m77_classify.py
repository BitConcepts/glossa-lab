"""Mahadevan 1977 — Page classifier.

Classifies each page image into one of:
  TEXTS       — site-name header + text numbers + sign sequences (what we want)
  CONCORDANCE — "CONCORDANCE" header + sign occurrences by position
  PLATE       — photographic plate / blank / front matter
  UNKNOWN     — could not classify

Uses OCR on a narrow top strip (~15% of page height) to detect page type
from the header text. This is fast because it only OCRs a small region.

Usage:
    shell.cmd python backend/scripts/ocr_m77_classify.py [--sample N]
    shell.cmd python backend/scripts/ocr_m77_classify.py --all

Output: glossa-corpus/indus/sources/internet-archive/raw/*/ocr/page_index.json
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
M77_DIR = sorted(IA_RAW.iterdir())[-1] / "images" / "mahadevan1977"  # most recent date
OCR_DIR = sorted(IA_RAW.iterdir())[-1] / "ocr"
OCR_DIR.mkdir(parents=True, exist_ok=True)

# Site headers that appear on TEXTS pages
SITE_HEADERS = {
    "MOHENJODARO", "MOHENJO-DARO", "MOHENJO DARO",
    "HARAPPA", "CHANHU-DARO", "CHANHU DARO", "CHANHUDARO",
    "LOTHAL", "KALIBANGAN", "KALlBANGAN",
    "SUTKAGEN-DOR", "SUTKAGENDOR",
    "NAUSHARO", "SIBRI", "MEHRGARH",
    "DHOLAVIRA", "RAKHIGARHI",
    "JHUKAR", "AMRI", "BALAKOT",
}


def setup_tesseract():
    import pytesseract, os
    tess_path = Path.home() / "scoop" / "apps" / "tesseract" / "current" / "tesseract.exe"
    tessdata = Path.home() / "scoop" / "apps" / "tesseract" / "current" / "tessdata"
    if tess_path.exists():
        pytesseract.pytesseract.tesseract_cmd = str(tess_path)
        os.environ["TESSDATA_PREFIX"] = str(tessdata)
    return pytesseract


def classify_page(img_path: Path, pytesseract, pil_Image) -> dict:
    """Classify a single page image."""
    try:
        img = pil_Image.open(img_path)
        w, h = img.size

        # Crop top 15% — this is where the header lives
        header_crop = img.crop((0, 0, w, int(h * 0.15)))

        # OCR the header strip — fast, just text detection
        header_text = pytesseract.image_to_string(
            header_crop,
            config="--psm 6 --oem 3"
        ).strip().upper()

        # Classify based on header content
        page_type = "UNKNOWN"
        header_found = ""

        if "CONCORDANCE" in header_text:
            page_type = "CONCORDANCE"
            header_found = "CONCORDANCE"
        else:
            for site in SITE_HEADERS:
                if site in header_text:
                    page_type = "TEXTS"
                    header_found = site
                    break

        if page_type == "UNKNOWN":
            # Check if page is mostly blank (very little text)
            full_text = pytesseract.image_to_string(img, config="--psm 6 --oem 3")
            word_count = len(full_text.split())
            if word_count < 5:
                page_type = "PLATE_OR_BLANK"
            else:
                page_type = "OTHER"  # front matter, appendix, etc.

        return {
            "file": img_path.name,
            "type": page_type,
            "header": header_found,
            "header_raw": header_text[:100],
        }

    except Exception as exc:
        return {"file": img_path.name, "type": "ERROR", "error": str(exc)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=int, default=20,
                        help="Number of evenly-spaced pages to classify (default: 20)")
    parser.add_argument("--all", action="store_true",
                        help="Classify all pages (slow — ~842 pages)")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=None)
    args = parser.parse_args()

    try:
        pytesseract = setup_tesseract()
        from PIL import Image as pil_Image
    except ImportError as e:
        print(f"ERROR: {e}. Run: shell.cmd python -m pip install pytesseract Pillow opencv-python")
        return 1

    images = sorted(M77_DIR.glob("*.jpg"))
    if not images:
        print(f"ERROR: No images found at {M77_DIR}")
        return 1

    print(f"=== Mahadevan 1977 Page Classifier ===")
    print(f"Total images: {len(images)}")
    print(f"Tesseract: {pytesseract.pytesseract.tesseract_cmd}")
    print()

    if args.all:
        to_classify = images[args.start:args.end]
    else:
        # Evenly spaced sample
        step = max(1, len(images) // args.sample)
        to_classify = images[::step][:args.sample]

    print(f"Classifying {len(to_classify)} pages...")
    print()

    results = []
    counts = {"TEXTS": 0, "CONCORDANCE": 0, "PLATE_OR_BLANK": 0, "OTHER": 0, "ERROR": 0, "UNKNOWN": 0}

    for i, img_path in enumerate(to_classify):
        result = classify_page(img_path, pytesseract, pil_Image)
        results.append(result)
        counts[result["type"]] = counts.get(result["type"], 0) + 1
        print(f"  [{i+1:3d}/{len(to_classify)}] {img_path.name}: {result['type']}"
              + (f" ({result['header']})" if result.get('header') else ""))

    print()
    print("=== Summary ===")
    for ptype, count in sorted(counts.items(), key=lambda x: -x[1]):
        if count > 0:
            print(f"  {ptype}: {count}")

    # Save index
    out = OCR_DIR / "page_index.json"
    existing = {}
    if out.exists():
        try:
            existing = {r["file"]: r for r in json.loads(out.read_text())["pages"]}
        except Exception:
            pass
    for r in results:
        existing[r["file"]] = r

    out.write_text(json.dumps({
        "_citation": {"primary_sources": ["I.8", "A.1"],
                      "derivation": "Page classification of Mahadevan 1977 IA scan."},
        "classified_at": datetime.utcnow().isoformat(),
        "total_images": len(images),
        "summary": counts,
        "pages": sorted(existing.values(), key=lambda x: x["file"]),
    }, indent=2), encoding="utf-8")
    print(f"\nIndex saved: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

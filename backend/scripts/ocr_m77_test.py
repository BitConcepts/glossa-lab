"""Quick test of the Tesseract OCR pipeline on one M77 page.
Run this to verify the setup before running the full pipeline.

Usage: shell.cmd python backend/scripts/ocr_m77_test.py
"""
from pathlib import Path
import sys

REPO = Path(__file__).parents[2]
M77_DIR = (REPO / "glossa-corpus/indus/sources/internet-archive/raw/2026-05-14/images/mahadevan1977")

def main():
    print("=== OCR Pipeline Test ===")

    # 1. Check Tesseract
    import pytesseract
    from PIL import Image

    import os
    tess = Path.home() / "scoop/apps/tesseract/current/tesseract.exe"
    tessdata = Path.home() / "scoop/apps/tesseract/current/tessdata"
    if tess.exists():
        pytesseract.pytesseract.tesseract_cmd = str(tess)
        os.environ["TESSDATA_PREFIX"] = str(tessdata)
        print(f"Tesseract: {tess} [OK]")
        print(f"TESSDATA:  {tessdata} [{'OK' if tessdata.exists() else 'MISSING'}]")
    else:
        print(f"WARNING: Tesseract not found at {tess}, using PATH")

    # 2. Check LANCZOS (Pillow version compatibility)
    try:
        resample = Image.LANCZOS
    except AttributeError:
        resample = Image.Resampling.LANCZOS
    print(f"PIL LANCZOS: {resample} [OK]")

    # 3. Find images
    images = sorted(M77_DIR.glob("*.jpg"))
    print(f"M77 images: {len(images)}")
    if not images:
        print("ERROR: No images found")
        return 1

    # 4. Test on page 0101 (we visually confirmed this is a TEXTS page)
    test_page = None
    for img in images:
        if "0101" in img.name:
            test_page = img
            break
    if test_page is None:
        test_page = images[100] if len(images) > 100 else images[0]
    print(f"Test image: {test_page.name}")

    # 5. Open and inspect
    img = Image.open(test_page)
    w, h = img.size
    print(f"Image size: {w}x{h}")

    # 6. OCR the header strip
    print("\n--- Header OCR (top 15%) ---")
    header = img.crop((0, 0, w, int(h * 0.15)))
    header_text = pytesseract.image_to_string(header, config="--psm 6 --oem 3")
    print(repr(header_text[:200]))

    # 7. OCR the left column (text numbers)
    print("\n--- Left column OCR (numbers, 12%-95% height, left 28% width) ---")
    left = img.crop((0, int(h * 0.12), int(w * 0.28), int(h * 0.95)))
    left_2x = left.resize((left.width * 2, left.height * 2), resample)
    left_text = pytesseract.image_to_string(left_2x, config="--psm 6 --oem 3")
    print(repr(left_text[:500]))

    # 8. Extract 4-digit textnums
    import re
    candidates = re.findall(r'\b([1-9][0-9]{3})\b', left_text)
    textnums = sorted(set(int(t) for t in candidates))
    print(f"\n--- Extracted textnums ({len(textnums)}) ---")
    print(textnums)

    # 9. Validate against known M77 range
    valid = [t for t in textnums if 1001 <= t <= 9999]
    print(f"Valid range (1001-9999): {valid}")

    print("\n=== Test complete ===")
    if textnums:
        print("SUCCESS: OCR extracted text numbers from the page")
    else:
        print("WARNING: No text numbers extracted — check OCR output above")
    return 0


if __name__ == "__main__":
    sys.exit(main())

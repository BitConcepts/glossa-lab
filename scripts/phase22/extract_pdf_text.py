"""Phase-22: extract searchable text from each contact-zone PDF.

For each PDF in corpora/downloads/contact_zone/publications/, run
PyMuPDF text extraction. If the PDF is image-only (text < 200 chars
on first 5 pages), flag it for OCR. Save output as <name>.txt next
to the PDF.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parents[2]
PUB_DIR = ROOT / "corpora" / "downloads" / "contact_zone" / "publications"
OUT_INDEX = PUB_DIR / "_text_extraction_index.json"


def main() -> int:
    if not PUB_DIR.exists():
        print(f"ERROR: publication dir not found: {PUB_DIR}", file=sys.stderr)
        return 1

    pdfs = sorted(PUB_DIR.glob("*.pdf"))
    print(f"Found {len(pdfs)} PDFs in {PUB_DIR}")
    index: list[dict] = []

    for pdf in pdfs:
        out_txt = pdf.with_suffix(".txt")
        try:
            doc = fitz.open(str(pdf))
            n_pages = doc.page_count
            chunks: list[str] = []
            for i in range(n_pages):
                try:
                    chunks.append(doc.load_page(i).get_text("text"))
                except Exception as exc:  # noqa: BLE001
                    chunks.append(f"[error on page {i}: {exc}]")
            text = "\n".join(chunks)
            doc.close()
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL  {pdf.name}: {exc}")
            index.append({
                "pdf": pdf.name, "pages": 0, "chars": 0,
                "image_only": True, "error": str(exc),
            })
            continue
        out_txt.write_text(text, encoding="utf-8")
        # First-pass image-only detection: check first 5 pages
        first_5 = "\n".join(chunks[:5])
        image_only = len(first_5.strip()) < 200
        kw_meluh = sum(text.lower().count(k) for k in
                       ["meluh", "meluḫḫa", "magan", "magán", "dilmun"])
        print(f"  {pdf.name:55s}  pages={n_pages:4d}  chars={len(text):8d}  "
              f"meluh+={kw_meluh:4d}  image_only={image_only}")
        index.append({
            "pdf": pdf.name, "pages": n_pages, "chars": len(text),
            "image_only": image_only,
            "meluhha_keyword_hits": kw_meluh,
            "txt_path": out_txt.name,
        })

    OUT_INDEX.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"\nIndex: {OUT_INDEX}")
    n_image_only = sum(1 for i in index if i.get("image_only"))
    print(f"Image-only (require OCR): {n_image_only}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

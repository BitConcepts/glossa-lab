#!/usr/bin/env python3
"""Phase-124 driver step 0: render CISI scan PDFs to page PNGs (cache).

    python3 scripts/phase124_cisi/render_pages.py --pdf <scan.pdf> \
        --out /tmp/cisi_pages/v1 --dpi 140

The renders are a disposable cache (default /tmp); the source scans are
in-copyright research copies and renders must never be committed.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dpi", type=int, default=140)
    a = ap.parse_args()
    import fitz  # PyMuPDF

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(a.pdf)
    for i, page in enumerate(doc, start=1):
        target = out / f"p{i:03d}.png"
        if target.exists():
            continue
        page.get_pixmap(dpi=a.dpi, colorspace=fitz.csGRAY).save(target)
    print(f"rendered {doc.page_count} pages at {a.dpi} dpi -> {out}")


if __name__ == "__main__":
    main()

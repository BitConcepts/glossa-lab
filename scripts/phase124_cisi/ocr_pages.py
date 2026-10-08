#!/usr/bin/env python3
"""Phase-124 driver step 1: per-page OCR of rendered CISI pages.

Run with the OCR venv (RapidOCR + OpenCV):
    ~/workspace/venvs/ocr/bin/python scripts/phase124_cisi/ocr_pages.py \
        --pages-dir /tmp/cisi_pages/v1 --out <local-store>/ocr/v1 \
        --workers 2

Reads page PNGs named pNNN.png, writes one checkpoint JSON per page
(lines with text, score and box). Checkpointed: existing outputs are
skipped, so a killed run resumes where it stopped. The outputs are
derived from in-copyright research scans and belong ONLY in the
gitignored local store (corpora/downloads/cisi_image_layer/).
"""
from __future__ import annotations

import argparse
import json
from multiprocessing import Pool
from pathlib import Path

_ENGINE = None


def _init():
    # One engine per worker process. Creating RapidOCR() per page costs
    # ~20 s of model loading per page and dominates the whole run.
    global _ENGINE
    from rapidocr_onnxruntime import RapidOCR

    _ENGINE = RapidOCR()


def _work(args):
    png, out = args
    if out.exists():
        return f"skip {png.name}"
    try:
        result, _ = _ENGINE(str(png))
    except Exception as exc:  # noqa: BLE001 — one bad render must not kill the pool
        return f"ERROR {png.name}: {exc}"
    lines = []
    for box, text, score in result or []:
        xs = [p[0] for p in box]
        ys = [p[1] for p in box]
        lines.append({
            "text": text, "score": round(float(score), 4),
            "x": round(min(xs), 1), "y": round(min(ys), 1),
            "w": round(max(xs) - min(xs), 1), "h": round(max(ys) - min(ys), 1),
        })
    out.write_text(json.dumps({"page_png": png.name, "lines": lines}))
    return f"done {png.name}: {len(lines)} lines"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    pages = sorted(Path(a.pages_dir).glob("p*.png"))
    outdir = Path(a.out)
    outdir.mkdir(parents=True, exist_ok=True)
    jobs = [(p, outdir / (p.stem + ".json")) for p in pages]
    with Pool(a.workers, initializer=_init) as pool:
        for msg in pool.imap_unordered(_work, jobs):
            print(msg, flush=True)


if __name__ == "__main__":
    main()

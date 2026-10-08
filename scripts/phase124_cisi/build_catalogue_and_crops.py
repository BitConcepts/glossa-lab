#!/usr/bin/env python3
"""Phase-124 driver steps 2-3: catalogue assembly + sign-crop sample.

Step 2 (catalogue): reads the per-page OCR checkpoints, parses headers
and captions with glossa_lab.cisi_image_layer, detects photo boxes on
the 140-dpi renders (texture segmentation), associates captions to
photos, and writes the catalogue CSV + a coverage summary JSON into the
local store. The bundled djvu.txt ID sequence is used only to
corroborate that an ID occurs somewhere in the volume (it has no page
breaks, so it cannot corroborate pages).

Step 3 (crops): for pages listed in --crop-pages (vol:pdfpage,...),
re-renders at 200 dpi, segments sign regions in each associated seal
photo (side A/a), and writes crop PNGs + a crop manifest CSV into the
local store. Crops are region proposals; no sign identity is asserted.

ALL outputs are derived from in-copyright research scans: local store
only, never committed.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab.cisi_image_layer import (
    COLUMNS,
    Header,
    OcrLine,
    PageRecord,
    associate_captions,
    build_page_rows,
    find_photo_boxes,
    find_photo_for_caption,
    parse_caption,
    parse_header,
    segment_sign_regions,
)

RENDER_DPI = 140
CROP_DPI = 200


def djvu_id_set(djvu_txt: Path) -> set[str]:
    text = djvu_txt.read_text(errors="replace")
    return {f"{p}-{int(n)}" for p, n in
            re.findall(r"\b([A-Z][A-Za-z]{0,2})-(\d{1,4})\b", text)}


def load_page(ocr_json: Path):
    data = json.loads(ocr_json.read_text())
    return [OcrLine(**{k: ln[k] for k in ("text", "score", "x", "y", "w", "h")})
            for ln in data["lines"]]


def assemble(volume: int, ocr_dir: Path, pages_dir: Path,
             djvu_ids: set[str], out_csv: Path) -> dict:
    import numpy as np
    from PIL import Image

    rows: list[dict] = []
    pages_with_rows = 0
    pages_seen = 0
    dropped = 0
    for ocr_json in sorted(ocr_dir.glob("p*.json")):
        pdf_page = int(ocr_json.stem[1:])
        pages_seen += 1
        lines = load_page(ocr_json)
        png = pages_dir / f"p{pdf_page:03d}.png"
        if not png.exists():
            continue
        with Image.open(png) as im:
            _w, h = im.size
            gray = np.asarray(im.convert("L"))
        top = [ln.text for ln in lines if ln.y < 0.085 * h]
        header: Header = parse_header(top)
        caps = []
        for ln in lines:
            cap = parse_caption(ln.text)
            if cap is not None:
                caps.append((cap, ln))
        # Primary locator: caption-anchored photo search (robust to
        # staggered dense plates). Fallback: grid segmentation +
        # association for any caption the anchored search missed.
        assoc = []
        missed = []
        for cap, ln in caps:
            box = find_photo_for_caption(gray, ln.cx, ln.y)
            if box is None:
                missed.append((cap, ln))
            else:
                assoc.append((box, cap, ln))
        photos = []
        if missed:
            photos = find_photo_boxes(gray)
            assoc.extend(associate_captions(photos, missed, h))
        rec = PageRecord(volume=volume, pdf_page=pdf_page, header=header)
        page_rows = build_page_rows(rec, photos, assoc, djvu_ids=djvu_ids)
        # The back-of-book sign index lists bare object IDs in running
        # text; those lines parse as captions but are not plate
        # captions. Keep a row only if it has an associated photograph
        # or sits on a plate page (header carries a site/object type).
        plate_page = bool(header.object_type or header.site)
        kept = [r for r in page_rows if r["photo_box_xywh"] or plate_page]
        dropped += len(page_rows) - len(kept)
        if kept:
            pages_with_rows += 1
        rows.extend(kept)

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=COLUMNS)
        wr.writeheader()
        wr.writerows(rows)
    low = sum(1 for r in rows if r["confidence"] == "low")
    return {
        "volume": volume, "pages_seen": pages_seen,
        "pages_with_rows": pages_with_rows, "rows": len(rows),
        "non_plate_caption_lines_dropped": dropped,
        "distinct_cisi_ids": len({r["cisi_id"] for r in rows}),
        "low_confidence_rows": low,
        "rows_with_photo": sum(1 for r in rows if r["photo_box_xywh"]),
        "sites": sorted({r["site"] for r in rows if r["site"]}),
    }


def make_crops(crop_pages: list[tuple[int, int, Path]], rows_by_page: dict,
               store: Path) -> list[dict]:
    """Crop sign regions for associated photos on the given pages.

    Pages must be pre-rendered at CROP_DPI into
    ``<store>/page_cache_200/v<vol>/pNNN.png`` (render_pages.py, run
    under the system Python that has PyMuPDF; this driver runs in the
    glossa venv, which does not).
    """
    import numpy as np
    from PIL import Image

    crops_dir = store / "crops"
    crops_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    for volume, pdf_page, _pdf_path in crop_pages:
        png = (store / "page_cache_200" / f"v{volume}"
               / f"p{pdf_page:03d}.png")
        page_img = Image.open(png).convert("L")
        scale = CROP_DPI / RENDER_DPI
        for row in rows_by_page.get((volume, pdf_page), []):
            if not row["photo_box_xywh"] or row["side"] not in ("A", "a"):
                continue
            x, y, w, h = (int(float(v) * scale)
                          for v in row["photo_box_xywh"].split(";"))
            if h > 1.5 * w:
                # Degenerate (merged) photo box from the grid fallback:
                # cropping from it would produce junk. Skip and say so.
                manifest.append({
                    "crop_file": "", "volume": volume,
                    "cisi_id": row["cisi_id"], "side": row["side"],
                    "printed_page": row["printed_page"],
                    "pdf_page": pdf_page,
                    "photo_box_xywh_200dpi": f"{x};{y};{w};{h}",
                    "crop_box_xywh_in_photo": "",
                    "crop_index_on_photo": 0,
                })
                continue
            photo = page_img.crop((x, y, x + w, y + h))
            regions = segment_sign_regions(np.asarray(photo))
            for j, (rx, ry, rw, rh) in enumerate(regions, start=1):
                key = row["photo_key"].replace(" ", "_")
                name = (f"v{volume}_{key}"
                        f"_p{row['printed_page']}_s{j:02d}.png")
                photo.crop((rx, ry, rx + rw, ry + rh)).save(crops_dir / name)
                manifest.append({
                    "crop_file": name, "volume": volume,
                    "cisi_id": row["cisi_id"], "side": row["side"],
                    "printed_page": row["printed_page"],
                    "pdf_page": pdf_page,
                    "photo_box_xywh_200dpi": f"{x};{y};{w};{h}",
                    "crop_box_xywh_in_photo": f"{rx};{ry};{rw};{rh}",
                    "crop_index_on_photo": j,
                })
    with (store / "crops" / "crop_manifest.csv").open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=[
            "crop_file", "volume", "cisi_id", "side", "printed_page",
            "pdf_page", "photo_box_xywh_200dpi", "crop_box_xywh_in_photo",
            "crop_index_on_photo"])
        wr.writeheader()
        wr.writerows(manifest)
    return manifest


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True,
                    help="gitignored local store (cisi_image_layer/)")
    ap.add_argument("--pages-root", required=True,
                    help="render cache root with v1/ and v2/ subdirs")
    ap.add_argument("--src-root", required=True,
                    help="research downloads root with cisi-{1,2}-ia-scan/")
    ap.add_argument("--crop-pages", default="",
                    help="comma list vol:pdfpage, e.g. 1:66,1:91,2:66")
    ap.add_argument("--hand-verified-pages", default="",
                    help="comma list vol:pdfpage whose rows were "
                         "hand-verified against rendered pages; their "
                         "extraction_basis gains +hand_verified")
    a = ap.parse_args()
    hand_verified = set()
    for item in filter(None, a.hand_verified_pages.split(",")):
        v_s, p_s = item.split(":")
        hand_verified.add((int(v_s), int(p_s)))
    store = Path(a.store)
    summaries = []
    all_rows: dict[tuple[int, int], list[dict]] = {}
    for vol in (1, 2):
        src = Path(a.src_root) / f"cisi-{vol}-ia-scan"
        ids = djvu_id_set(src / f"CorpusVol{vol}_djvu.txt")
        out_csv = store / "catalogue" / f"cisi_vol{vol}_catalogue.csv"
        summaries.append(assemble(
            vol, store / "ocr" / f"v{vol}", Path(a.pages_root) / f"v{vol}",
            ids, out_csv))
        with out_csv.open() as fh:
            for r in csv.DictReader(fh):
                all_rows.setdefault((vol, int(r["pdf_page"])), []).append(r)
        if any(v == vol for v, _ in hand_verified):
            with out_csv.open() as fh:
                vol_rows = list(csv.DictReader(fh))
            for r in vol_rows:
                if (vol, int(r["pdf_page"])) in hand_verified:
                    r["extraction_basis"] += "+hand_verified"
            with out_csv.open("w", newline="") as fh:
                wr = csv.DictWriter(fh, fieldnames=COLUMNS)
                wr.writeheader()
                wr.writerows(vol_rows)
    (store / "catalogue" / "coverage_summary.json").write_text(
        json.dumps(summaries, indent=2))
    print(json.dumps(summaries, indent=2))

    if a.crop_pages:
        jobs = []
        for item in a.crop_pages.split(","):
            vol_s, page_s = item.split(":")
            vol, page = int(vol_s), int(page_s)
            pdf = (Path(a.src_root) / f"cisi-{vol}-ia-scan"
                   / f"CorpusVol{vol}.pdf")
            jobs.append((vol, page, pdf))
        manifest = make_crops(jobs, all_rows, store)
        print(f"crops: {len(manifest)} -> {store / 'crops'}")


if __name__ == "__main__":
    main()

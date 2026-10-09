#!/usr/bin/env python3
"""Phase-129 driver: CISI cropper v2 benchmark + gated expansion.

Benchmark mode (frozen protocol, reports/phase129_cisi_cropper_v2_
protocol.md): replays the Phase-124 worked sample — the 32 CISI
ID+side groups / 34 photo boxes recorded in the local store's
``crops/verification.csv``, cut from the 200-dpi page renders — runs
v1 first and asserts its boxes reproduce the frozen manifest exactly
(input sanity, not a re-grade), then runs v2 twice and asserts the
two runs are identical (determinism), writing v2 crops + a v2 crop
manifest into the local store under ``crops_v2/``.

Expansion mode: runs v2 over every catalogue row with side A/a and a
non-degenerate photo box, cut from the 140-dpi page cache, excluding
the benchmark photos. The caller must only invoke it when the
frozen win definition was met; the script records the operator's
gate attestation string in the local expansion manifest. A fixed
seed (129) spot-check sample of 30 crop filenames is printed for
manual grading context.

ALL outputs are derived from in-copyright research scans: local
store only, never committed.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from glossa_lab.cisi_cropper_v2 import segment_sign_regions_v2
from glossa_lab.cisi_image_layer import segment_sign_regions as segment_v1

FIELDS = ["crop_file", "volume", "cisi_id", "side", "printed_page",
          "pdf_page", "photo_box_xywh_200dpi", "crop_box_xywh_in_photo",
          "crop_index_on_photo"]


def _photos_from_verification(store: Path):
    rows = [r for r in csv.DictReader(
        (store / "crops" / "verification.csv").open())
        if r["crop_file"]]
    photos: dict[str, tuple[dict, list[dict]]] = {}
    for r in rows:
        stem = r["crop_file"].rsplit("_s", 1)[0]
        photos.setdefault(stem, (r, []))[1].append(r)
    return photos


def run_benchmark(store: Path) -> dict:
    import numpy as np
    from PIL import Image

    photos = _photos_from_verification(store)
    out_dir = store / "crops_v2"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    v1_repro_ok = True
    for stem, (r0, crops) in sorted(photos.items()):
        vol, page = int(r0["volume"]), int(r0["pdf_page"])
        page_im = Image.open(
            store / "page_cache_200" / f"v{vol}" / f"p{page:03d}.png"
        ).convert("L")
        x, y, w, h = (int(v) for v in
                      r0["photo_box_xywh_200dpi"].split(";"))
        photo_im = page_im.crop((x, y, x + w, y + h))
        photo = np.asarray(photo_im)
        frozen = [tuple(int(v) for v in
                        c["crop_box_xywh_in_photo"].split(";"))
                  for c in crops]
        if segment_v1(photo) != frozen:
            v1_repro_ok = False
            print(f"V1 REPRODUCTION MISMATCH: {stem}", file=sys.stderr)
        boxes = segment_sign_regions_v2(photo)
        if segment_sign_regions_v2(photo.copy()) != boxes:
            raise AssertionError(f"v2 non-deterministic on {stem}")
        for j, (rx, ry, rw, rh) in enumerate(boxes, start=1):
            name = f"cv2_{stem}_s{j:02d}.png"
            photo_im.crop((rx, ry, rx + rw, ry + rh)).save(out_dir / name)
            manifest.append({
                "crop_file": name, "volume": vol,
                "cisi_id": r0["cisi_id"], "side": r0["side"],
                "printed_page": r0["printed_page"], "pdf_page": page,
                "photo_box_xywh_200dpi": r0["photo_box_xywh_200dpi"],
                "crop_box_xywh_in_photo": f"{rx};{ry};{rw};{rh}",
                "crop_index_on_photo": j,
            })
    with (out_dir / "crop_manifest_v2.csv").open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=FIELDS)
        wr.writeheader()
        wr.writerows(manifest)
    return {"mode": "benchmark", "photos": len(photos),
            "v1_reproduction_exact": v1_repro_ok,
            "v2_crops": len(manifest)}


def run_expansion(store: Path, gate_attestation: str) -> dict:
    import numpy as np
    from PIL import Image

    benchmark = _photos_from_verification(store)
    bench_keys = {(int(r0["volume"]), int(r0["pdf_page"]),
                   r0["photo_box_xywh_200dpi"])
                  for r0, _ in benchmark.values()}
    out_dir = store / "crops_v2_expansion"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    skipped_no_render = 0
    photos_done = 0
    for vol in (1, 2):
        cat = store / "catalogue" / f"cisi_vol{vol}_catalogue.csv"
        page_cache: dict[int, object] = {}
        for row in csv.DictReader(cat.open()):
            if row["side"] not in ("A", "a") or not row["photo_box_xywh"]:
                continue
            x, y, w, h = (int(float(v)) for v in
                          row["photo_box_xywh"].split(";"))
            if h > 1.5 * w:
                continue
            page = int(row["pdf_page"])
            # Benchmark boxes are 200-dpi; catalogue boxes are
            # 140-dpi. The same photo at 140 dpi scales by 0.7.
            # The v1 driver scaled 140-dpi boxes to 200 dpi with
            # int() truncation; match that exactly or the benchmark
            # photos are not recognised and get re-cropped.
            scaled = ";".join(str(int(v * 200 / 140))
                              for v in (x, y, w, h))
            if (vol, page, scaled) in bench_keys:
                continue
            if page not in page_cache:
                png = store / "page_cache" / f"v{vol}" / f"p{page:03d}.png"
                if not png.exists():
                    page_cache[page] = None
                else:
                    page_cache[page] = Image.open(png).convert("L")
            page_im = page_cache[page]
            if page_im is None:
                skipped_no_render += 1
                continue
            photo_im = page_im.crop((x, y, x + w, y + h))
            boxes = segment_sign_regions_v2(np.asarray(photo_im))
            photos_done += 1
            key = row["photo_key"].replace(" ", "_")
            for j, (rx, ry, rw, rh) in enumerate(boxes, start=1):
                # The same ID+side+printed page can occur on two
                # distinct photos (re-photographed exemplars in the
                # catalogue); the pdf page + box origin keep every
                # expansion filename unique.
                name = (f"cv2x_v{vol}_{key}_p{row['printed_page']}"
                        f"_pdf{page}_{x}_{y}_s{j:02d}.png")
                photo_im.crop((rx, ry, rx + rw, ry + rh)).save(
                    out_dir / name)
                manifest.append({
                    "crop_file": name, "volume": vol,
                    "cisi_id": row["cisi_id"], "side": row["side"],
                    "printed_page": row["printed_page"],
                    "pdf_page": page,
                    "photo_box_xywh_200dpi": scaled,
                    "crop_box_xywh_in_photo": f"{rx};{ry};{rw};{rh}",
                    "crop_index_on_photo": j,
                })
    names = [m["crop_file"] for m in manifest]
    assert len(names) == len(set(names)), "duplicate expansion filenames"
    with (out_dir / "expansion_manifest.csv").open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=FIELDS)
        wr.writeheader()
        wr.writerows(manifest)
    (out_dir / "expansion_summary.json").write_text(json.dumps({
        "gate_attestation": gate_attestation,
        "photos_processed": photos_done,
        "skipped_no_render": skipped_no_render,
        "crops": len(manifest),
        "distinct_cisi_ids": len({m["cisi_id"] for m in manifest}),
    }, indent=2))
    rng = random.Random(129)
    spot = rng.sample([m["crop_file"] for m in manifest],
                      min(30, len(manifest)))
    (out_dir / "spotcheck_seed129.txt").write_text("\n".join(spot))
    return {"mode": "expansion", "photos_processed": photos_done,
            "skipped_no_render": skipped_no_render,
            "crops": len(manifest),
            "distinct_cisi_ids":
                len({m["cisi_id"] for m in manifest}),
            "spotcheck": spot}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True,
                    help="gitignored local store (cisi_image_layer/)")
    ap.add_argument("--mode", choices=("benchmark", "expansion"),
                    required=True)
    ap.add_argument("--gate-attestation", default="",
                    help="expansion only: operator attestation that "
                         "the frozen win definition was met")
    a = ap.parse_args()
    store = Path(a.store)
    if a.mode == "benchmark":
        print(json.dumps(run_benchmark(store), indent=2))
    else:
        if not a.gate_attestation:
            raise SystemExit("expansion requires --gate-attestation")
        print(json.dumps(run_expansion(store, a.gate_attestation),
                         indent=2))


if __name__ == "__main__":
    main()

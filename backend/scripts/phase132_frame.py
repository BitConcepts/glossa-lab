"""Phase-132 (spec 023, FROZEN) Stage P pilot — deterministic frame draw.

Implements the frozen pilot frame rule exactly as tasked:

- Universe: distinct objects keyed (volume, cisi_id) from the two CISI
  catalogue CSVs in the local image-layer store.
- Exclusions: objects whose (first photo row's) site is empty or
  'Addenda' (spec 023 section 3.3 / 3.1 — pilot strata require a
  printed site), and objects whose first photo row's object_type is
  'Graffiti' (the pilot spans seals and tablets per section 3.1).
- Canonical key: cisi:v{volume}:{cisi_id}.
- Mayig overlap set: the CISI objects corresponding to
  data/corpus_layers/mayig_cisi_layer_v1.json via its Phase-122
  mapping. The layer file keys each inscription by its printed CISI
  object ID (cisi_object_id); an inscription resolves to the unique
  catalogue object carrying that printed ID. Entries that resolve to
  zero catalogue objects, or ambiguously to more than one volume,
  are counted and reported — never guessed.
- Strata quotas: Mohenjo-Daro 25 (mayig sub-quota 10), Harappa 15
  (mayig sub-quota 0), Lothal+Kalibangan 10 (drawn Lothal 6 then
  Kalibangan 4; mayig sub-quota 0). FRAME QUOTA CORRECTION
  (Phase-132): the mayig layer is Mohenjo-Daro-only in the
  catalogue resolution — all 179 mayig-overlap objects resolve to
  Mohenjo-Daro (176) or site-uncaptured (3), with 0 at Harappa,
  Lothal, Kalibangan, or any other site — so the original
  Harappa / Lothal+Kalibangan mayig sub-quotas were unfillable and
  only 5 mayig objects were drawn. Spec 023 section 3.1 designs
  ~10 mayig-overlap objects into the pilot frame and site spread
  across strata is NOT required for the overlap subset, so the
  full mayig sub-quota of 10 is placed on Mohenjo-Daro.
- Within a stratum: first draw the mayig sub-quota from the stratum's
  mayig-overlap objects, then fill the remaining quota from
  non-overlap objects. Each sublist is sorted by (pdf_page of the
  object's earliest photo row, cisi_id) and drawn every-k-th:
  k = max(1, floor(len(sublist)/needed)), start index =
  20261009 % k, indices start, start+k, ... until the quota is met.
  If the stepped pass is exhausted before the quota is met, drawing
  continues from the start of the list skipping already-drawn
  objects; when this fallback fires it is recorded. A sub-quota
  larger than the available overlap pool draws the whole pool and
  the balance of the stratum quota is filled from non-overlap
  objects (the shortfall is recorded in the summary).
- Gold sample: random.Random(20261009).sample(frame, 10) after the
  draw.

Outputs: frame.json in the local store pilot workspace and a copy at
data/keyed_transcription/phase132_pilot_frame.json in the repo.

Deterministic: no wall-clock, no ambient randomness beyond the
seeded gold draw, no dict-order dependence in the draw itself.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
from pathlib import Path

SEED = 20261009

DEFAULT_STORE = Path.home() / "workspace" / "glossa-lab" / "corpora" / \
    "downloads" / "cisi_image_layer"
REPO_ROOT = Path(__file__).resolve().parents[2]
LAYER_PATH = REPO_ROOT / "data" / "corpus_layers" / "mayig_cisi_layer_v1.json"
REPO_FRAME_OUT = REPO_ROOT / "data" / "keyed_transcription" / \
    "phase132_pilot_frame.json"

MAYIG_CORRECTION_REASON = (
    "Frame quota correction (Phase-132): the mayig layer is "
    "Mohenjo-Daro-only in the catalogue resolution — all 179 "
    "mayig-overlap objects resolve to Mohenjo-Daro (176) or "
    "site-uncaptured (3), with 0 elsewhere (0 Harappa, 0 Lothal, "
    "0 Kalibangan). The original Harappa / Lothal+Kalibangan "
    "mayig sub-quotas were therefore unfillable and only 5 mayig "
    "objects were drawn. Spec 023 section 3.1 designs ~10 "
    "mayig-overlap objects into the pilot frame and site spread "
    "across strata is not required for the overlap subset, so the "
    "mayig sub-quota is Mohenjo-Daro 10, Harappa 0, "
    "Lothal+Kalibangan 0."
)

RULE_TEXT = (
    "Universe: distinct (volume, cisi_id) objects from "
    "catalogue/cisi_vol{1,2}_catalogue.csv. Excluded: first-photo-row "
    "site empty or 'Addenda'; first-photo-row object_type 'Graffiti'. "
    "Canonical key cisi:v{volume}:{cisi_id}. Mayig overlap: printed "
    "CISI object IDs from data/corpus_layers/mayig_cisi_layer_v1.json "
    "(Phase-122 mapping) resolved to the unique catalogue object with "
    "that printed ID; unresolvable or ambiguous entries counted, "
    "never guessed. " + MAYIG_CORRECTION_REASON + " Strata: "
    "Mohenjo-Daro 25 (mayig sub-quota 10), "
    "Harappa 15 (mayig sub-quota 0), Lothal+Kalibangan 10 = Lothal 6 "
    "then Kalibangan 4 (mayig sub-quota 0). "
    "Within a stratum the mayig sub-quota is drawn first "
    "from the stratum's overlap objects, then the quota is filled "
    "from non-overlap objects. Sublists are sorted by (pdf_page of "
    "the object's earliest photo row, cisi_id) — volume breaks exact "
    "ties only — and drawn every-k-th with k = max(1, floor(len/"
    "needed)), start = 20261009 % k, indices start, start+k, ...; "
    "if exhausted, drawing continues from the start of the list "
    "skipping already-drawn objects (fallback recorded when it "
    "fires). A sub-quota above the available overlap pool draws the "
    "whole pool and the shortfall is filled from non-overlap objects "
    "(recorded). Gold: random.Random(20261009).sample(frame, 10) "
    "after the draw."
)

# Ordered strata specification: (stratum name, [(site, quota), ...],
# mayig sub-quota shared across the site draws in order).
STRATA = [
    ("Mohenjo-Daro", [("Mohenjo-Daro", 25)], 10),
    ("Harappa", [("Harappa", 15)], 0),
    ("Lothal+Kalibangan", [("Lothal", 6), ("Kalibangan", 4)], 0),
]

EXCLUDED_SITES = ("", "Addenda")
EXCLUDED_TYPE = "Graffiti"


def parse_box(raw: str):
    """Parse a 'x;y;w;h' photo_box_xywh cell to [x, y, w, h] or None."""
    raw = (raw or "").strip()
    if not raw:
        return None
    parts = raw.split(";")
    if len(parts) != 4:
        return None
    try:
        return [int(p) for p in parts]
    except ValueError:
        return None


def load_catalogue(store: Path) -> dict:
    """Distinct objects keyed (volume, cisi_id), rows in file order."""
    objects: dict = {}
    for volume in (1, 2):
        path = store / "catalogue" / f"cisi_vol{volume}_catalogue.csv"
        with open(path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                key = (volume, row["cisi_id"])
                objects.setdefault(key, []).append(row)
    out = {}
    for (volume, cisi_id), rows in objects.items():
        first = rows[0]
        photo_rows = []
        for r in rows:
            try:
                pdf_page = int(r["pdf_page"])
            except (TypeError, ValueError):
                pdf_page = None
            photo_rows.append({
                "photo_key": r["photo_key"],
                "side": r["side"],
                "bis": r["bis"],
                "pdf_page": pdf_page,
                "printed_page": r["printed_page"],
                "photo_box_xywh": parse_box(r["photo_box_xywh"]),
            })
        pages = [p["pdf_page"] for p in photo_rows if p["pdf_page"] is not None]
        out[(volume, cisi_id)] = {
            "volume": volume,
            "cisi_id": cisi_id,
            "canonical_key": f"cisi:v{volume}:{cisi_id}",
            "site": first["site"],
            "object_type": first["object_type"],
            "earliest_pdf_page": min(pages) if pages else None,
            "photos": photo_rows,
        }
    return out


def is_eligible(obj: dict) -> bool:
    return obj["site"] not in EXCLUDED_SITES and \
        obj["object_type"] != EXCLUDED_TYPE


def resolve_mayig_overlap(layer_path: Path, objects: dict):
    """Resolve each layer inscription to a catalogue object.

    Returns (overlap set of (volume, cisi_id), report dict). The layer
    file carries the printed CISI object ID per inscription
    (cisi_object_id, the Phase-122 mapping's key); resolution is to
    the unique catalogue object with that printed ID across both
    volumes.
    """
    layer = json.loads(Path(layer_path).read_text(encoding="utf-8"))
    by_printed_id: dict = {}
    for key in objects:
        by_printed_id.setdefault(key[1], []).append(key)
    overlap = set()
    unresolved = []
    ambiguous = []
    n_inscriptions = 0
    for insc in layer["inscriptions"]:
        n_inscriptions += 1
        printed_id = insc["cisi_object_id"]
        candidates = by_printed_id.get(printed_id, [])
        if len(candidates) == 1:
            overlap.add(candidates[0])
        elif len(candidates) == 0:
            unresolved.append(printed_id)
        else:
            ambiguous.append(printed_id)
    report = {
        "n_layer_inscriptions": n_inscriptions,
        "n_resolved_objects": len(overlap),
        "n_unresolved": len(unresolved),
        "unresolved_printed_ids": sorted(unresolved),
        "n_ambiguous": len(ambiguous),
        "ambiguous_printed_ids": sorted(ambiguous),
    }
    return overlap, report


def sort_key(obj: dict):
    page = obj["earliest_pdf_page"]
    return (page if page is not None else 1 << 30, obj["cisi_id"],
            obj["volume"])


def every_kth(sublist: list, needed: int):
    """Every-k-th draw per the frozen rule.

    Returns (drawn list, info dict). sublist must already be sorted.
    """
    info = {"pool_size": len(sublist), "needed": needed, "k": None,
            "start_index": None, "fallback_fired": False}
    if needed <= 0 or not sublist:
        return [], info
    take = min(needed, len(sublist))
    k = max(1, math.floor(len(sublist) / needed))
    start = SEED % k
    info["k"] = k
    info["start_index"] = start
    drawn = []
    seen = set()
    idx = start
    while len(drawn) < take and idx < len(sublist):
        drawn.append(sublist[idx])
        seen.add(sublist[idx]["canonical_key"])
        idx += k
    if len(drawn) < take:
        info["fallback_fired"] = True
        for obj in sublist:
            if len(drawn) >= take:
                break
            if obj["canonical_key"] not in seen:
                drawn.append(obj)
                seen.add(obj["canonical_key"])
    return drawn, info


def draw_frame(objects: dict, overlap: set):
    """Run the stratified draw. Returns (frame list, summary dict)."""
    eligible = {k: o for k, o in objects.items() if is_eligible(o)}
    frame = []
    drawn_keys = set()
    per_stratum = []
    for stratum_name, site_quotas, sub_quota in STRATA:
        remaining_sub = sub_quota
        stratum_drawn = []
        site_reports = []
        for site, quota in site_quotas:
            pool = [o for o in eligible.values() if o["site"] == site
                    and o["canonical_key"] not in drawn_keys]
            overlap_pool = sorted(
                [o for o in pool if (o["volume"], o["cisi_id"]) in overlap],
                key=sort_key)
            non_overlap_pool = sorted(
                [o for o in pool
                 if (o["volume"], o["cisi_id"]) not in overlap],
                key=sort_key)
            mayig_drawn, mayig_info = every_kth(overlap_pool, remaining_sub)
            remaining_sub -= len(mayig_drawn)
            fill_needed = quota - len(mayig_drawn)
            fill_drawn, fill_info = every_kth(non_overlap_pool, fill_needed)
            site_drawn = mayig_drawn + fill_drawn
            for o in site_drawn:
                drawn_keys.add(o["canonical_key"])
            stratum_drawn.extend(site_drawn)
            site_reports.append({
                "site": site,
                "quota": quota,
                "drawn": len(site_drawn),
                "mayig_drawn": len(mayig_drawn),
                "mayig_draw": mayig_info,
                "fill_draw": fill_info,
            })
        frame.extend(stratum_drawn)
        per_stratum.append({
            "stratum": stratum_name,
            "quota": sum(q for _, q in site_quotas),
            "mayig_sub_quota": sub_quota,
            "mayig_drawn": sum(s["mayig_drawn"] for s in site_reports),
            "drawn": len(stratum_drawn),
            "sites": site_reports,
        })
    return frame, eligible, per_stratum


def build_frame(store: Path, layer_path: Path) -> dict:
    objects = load_catalogue(store)
    overlap, overlap_report = resolve_mayig_overlap(layer_path, objects)
    frame_objs, eligible, per_stratum = draw_frame(objects, overlap)

    frame_keys = [o["canonical_key"] for o in frame_objs]
    gold_keys = [o["canonical_key"] for o in
                 random.Random(SEED).sample(frame_objs, 10)]
    gold_set = set(gold_keys)

    frame = []
    for o in frame_objs:
        frame.append({
            "canonical_key": o["canonical_key"],
            "volume": o["volume"],
            "cisi_id": o["cisi_id"],
            "site": o["site"],
            "object_type": o["object_type"],
            "mayig_overlap": (o["volume"], o["cisi_id"]) in overlap,
            "gold": o["canonical_key"] in gold_set,
            "photos": o["photos"],
        })

    type_counts: dict = {}
    for o in frame_objs:
        type_counts[o["object_type"]] = \
            type_counts.get(o["object_type"], 0) + 1

    summary = {
        "rule": RULE_TEXT,
        "mayig_quota_correction": MAYIG_CORRECTION_REASON,
        "seed": SEED,
        "n_frame": len(frame),
        "n_universe_objects": len(objects),
        "n_eligible_objects": len(eligible),
        "per_stratum": per_stratum,
        "site_counts": {s["stratum"]: s["drawn"] for s in per_stratum},
        "type_counts": type_counts,
        "mayig_overlap_count": sum(1 for o in frame if o["mayig_overlap"]),
        "mayig_resolution": overlap_report,
        "gold_keys": gold_keys,
    }
    return {"frame_summary": summary, "frame": frame}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--store", type=Path, default=DEFAULT_STORE,
                    help="local CISI image-layer store root")
    ap.add_argument("--layer", type=Path, default=LAYER_PATH,
                    help="mayig CISI layer JSON (Phase-122 mapping)")
    ap.add_argument("--out-store", type=Path, default=None,
                    help="store frame.json output (default: "
                         "<store>/phase132_pilot/frame.json)")
    ap.add_argument("--out-repo", type=Path, default=REPO_FRAME_OUT,
                    help="repo copy of the frame JSON")
    args = ap.parse_args(argv)

    doc = build_frame(args.store, args.layer)
    payload = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"

    out_store = args.out_store or \
        (args.store / "phase132_pilot" / "frame.json")
    out_store.parent.mkdir(parents=True, exist_ok=True)
    out_store.write_text(payload, encoding="utf-8")
    args.out_repo.parent.mkdir(parents=True, exist_ok=True)
    args.out_repo.write_text(payload, encoding="utf-8")

    s = doc["frame_summary"]
    print(json.dumps({
        "n_frame": s["n_frame"],
        "site_counts": s["site_counts"],
        "type_counts": s["type_counts"],
        "mayig_overlap_count": s["mayig_overlap_count"],
        "gold_keys": s["gold_keys"],
        "mayig_resolution": s["mayig_resolution"],
        "wrote": [str(out_store), str(args.out_repo)],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

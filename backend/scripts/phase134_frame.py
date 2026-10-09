"""Phase-134 (spec 024, Stage 1) — deterministic pilot frame draw.

Implements the frame rule frozen in
specs/024-evidence-integration/stage1-freeze.md §2:

- population: catalogue objects (volume-scoped keys) with >=1 photo
  row carrying a parseable photo_box_xywh and object_type in
  {Seals, Tablets, Graffiti}; site grouped Mohenjo-Daro / Harappa /
  Other;
- allocation: proportional to the 9 cell populations by largest
  remainder, minimum 2 per non-empty cell, total exactly 100;
- selection: within a cell, order by
  sha256("phase134-20261009|" + canonical_key) ascending, take quota;
- gold subset: drawn frame in the same hash order, indices
  0, 5, 10, ..., 95 (20 objects);
- reserves: the next candidates per cell, in hash order, for the
  frozen pre-coding replacement rule.

Reads the Phase-124 catalogue CSVs from the gitignored local store
(main checkout, the Phase-133 convention). Writes
data/evidence_integration/phase134_pilot_frame.json.
"""

import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MAIN_CHECKOUT = Path.home() / "workspace" / "glossa-lab"
STORE = MAIN_CHECKOUT / "corpora" / "downloads" / "cisi_image_layer"
OUT = REPO_ROOT / "data" / "evidence_integration" / \
    "phase134_pilot_frame.json"

SEED = "phase134-20261009"
SAMPLE_SIZE = 100
TYPES = ("Seals", "Tablets", "Graffiti")


def site_group(site: str) -> str:
    return site if site in ("Mohenjo-Daro", "Harappa") else "Other"


def hash_key(canonical_key: str) -> str:
    return hashlib.sha256(
        f"{SEED}|{canonical_key}".encode()).hexdigest()


def parse_box(raw: str):
    try:
        parts = [int(p) for p in raw.strip().split(";")]
        return parts if len(parts) == 4 else None
    except (ValueError, AttributeError):
        return None


def load_population():
    objects = {}
    for vol in (1, 2):
        path = STORE / "catalogue" / f"cisi_vol{vol}_catalogue.csv"
        with open(path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                key = f"cisi:v{vol}:{row['cisi_id']}"
                obj = objects.setdefault(key, {
                    "canonical_key": key, "volume": vol,
                    "cisi_id": row["cisi_id"], "site": row["site"],
                    "object_type": row["object_type"],
                    "photos": [], "motif_chapters": set()})
                if parse_box(row["photo_box_xywh"]) is not None:
                    obj["photos"].append({
                        "photo_key": row["photo_key"],
                        "side": row["side"],
                        "pdf_page": int(row["pdf_page"])
                        if row["pdf_page"].isdigit() else None,
                        "photo_box_xywh":
                            parse_box(row["photo_box_xywh"])})
                if row["motif_chapter"].strip():
                    obj["motif_chapters"].add(
                        row["motif_chapter"].strip())
    return objects


def chapter_family(obj) -> str:
    chaps = obj["motif_chapters"]
    if not chaps:
        return "NONE"
    lowered = {c.lower().replace(" ", "") for c in chaps}
    if any(c.startswith(("unicorn", "unicorm", "unicom", "unicon",
                         "uricorn", "unico")) for c in lowered):
        return "UNICORN"
    return "NONMAPPABLE"


def allocate(cells: dict, total: int) -> dict:
    """Largest-remainder proportional allocation, min 2/cell."""
    pop_total = sum(cells.values())
    quotas = {c: max(2, int(total * n / pop_total))
              for c, n in cells.items()}
    # exact shares for remainder ordering
    exact = {c: total * n / pop_total for c, n in cells.items()}
    while sum(quotas.values()) > total:
        # remove from the cell whose quota most exceeds its exact
        # share (never below its minimum of 2 or its population)
        c = max(quotas, key=lambda k: (quotas[k] - exact[k],
                                       quotas[k]))
        quotas[c] -= 1
    while sum(quotas.values()) < total:
        c = max(exact, key=lambda k: (exact[k] - quotas[k]))
        quotas[c] += 1
    return quotas


def main() -> int:
    objects = load_population()
    eligible = {k: o for k, o in objects.items()
                if o["photos"] and o["object_type"] in TYPES}
    excluded = len(objects) - len(eligible)

    cells = defaultdict(list)
    for key, obj in eligible.items():
        cells[(site_group(obj["site"]), obj["object_type"])].append(key)
    cell_pops = {c: len(v) for c, v in cells.items()}
    quotas = allocate(cell_pops, SAMPLE_SIZE)

    frame, reserves = [], {}
    for cell, keys in cells.items():
        ordered = sorted(keys, key=hash_key)
        quota = quotas[cell]
        take, rest = ordered[:quota], ordered[quota:]
        reserves[f"{cell[0]}|{cell[1]}"] = rest[:10]
        for key in take:
            obj = eligible[key]
            frame.append({
                "canonical_key": key, "volume": obj["volume"],
                "cisi_id": obj["cisi_id"],
                "site_group": cell[0], "site": obj["site"],
                "object_type": obj["object_type"],
                "n_photos": len(obj["photos"]),
                "motif_chapter_family": chapter_family(obj),
                "photos": obj["photos"]})
    frame.sort(key=lambda o: hash_key(o["canonical_key"]))
    gold = [frame[i]["canonical_key"]
            for i in range(0, len(frame), 5)][:20]
    gold_set = set(gold)
    for obj in frame:
        obj["gold"] = obj["canonical_key"] in gold_set

    doc = {
        "phase": 134, "spec": "024", "stage": 1,
        "seed": SEED,
        "rule": "stage1-freeze.md §2 (largest-remainder proportional "
                "allocation over site-group x object-type cells, "
                "min 2/cell; sha256 hash order within cell; gold = "
                "every 5th of the hash-ordered frame)",
        "population": {
            "catalogue_objects": len(objects),
            "eligible": len(eligible), "excluded": excluded,
            "cell_populations":
                {f"{c[0]}|{c[1]}": n for c, n in
                 sorted(cell_pops.items())},
            "cell_quotas":
                {f"{c[0]}|{c[1]}": n for c, n in
                 sorted(quotas.items())}},
        "frame_size": len(frame), "gold_size": len(gold),
        "gold_keys": gold,
        "reserves": reserves,
        "replacements": [],
        "frame": frame,
        "ai_disclosure": "All coding roles in this pilot are "
                         "executed by AI agents (Muse Spark, via "
                         "Muse) in blinded role-isolated instances, "
                         "at the direction of Tristen Pierson "
                         "(constitution §VI; spec 024 §4.4).",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "eligible": len(eligible), "excluded": excluded,
        "frame": len(frame), "gold": len(gold),
        "quotas": doc["population"]["cell_quotas"],
        "frame_motif_families":
            Counter(o["motif_chapter_family"] for o in frame)},
        indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

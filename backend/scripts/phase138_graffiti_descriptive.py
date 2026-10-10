#!/usr/bin/env python3
"""Phase-138 (spec 024, Stage 2(d), FROZEN) — graffiti descriptive protocol.

Implements specs/024-evidence-integration/stage2d-freeze.md §2 exactly:
a DESCRIPTIVE protocol only. No test, no p-value, no inference; this
arm is not a member of the Stage 2 family. Counts, proportions,
medians and interquartile ranges — nothing else.

Population (freeze §1): all Phase-124 catalogue rows (CISI Vols. 1–2)
whose ``object_type`` is exactly ``Graffiti``. Distinct objects are
volume-scoped: canonical key ``cisi:v{volume}:{cisi_id}``.

Outputs (freeze §2):
1. rows and distinct objects by volume;
2. distinct objects by catalogue ``site`` (Class O), including the
   no-site count, all sites shown (pooled and by volume);
3. photo-rows-per-object distribution, by volume and pooled;
4. ``side`` and ``bis`` value counts as printed;
5. ``motif_chapter`` (Class C, CISI editors' chapter organization):
   filled rows / rate and distinct values with counts AS PRINTED —
   spelling variants and heading strings recorded, never cleaned;
6. ``caption_ocr_score`` and ``scale_pct``: median + IQR with
   present-counts (extraction-quality descriptors of the catalogue);
7. context table (descriptive only): the same site distribution and
   rows-per-object distribution for ``Seals`` and ``Tablets`` rows —
   a description of catalogue composition, explicitly NOT a
   repertoire comparison and licensing no inference;
8. the qualitative Kodumanal paragraph restating
   reports/phase133_stage0_report.md §6.1 (in the main checkout's
   committed reports; also summarised in the freeze §2.8).

Inputs live in the gitignored local store of the main checkout
(never committed). Every number is recomputed from the files at run
time. Deterministic: no randomness, no wall-clock in the outputs,
stable ordering everywhere (count-descending, then value-ascending,
for value-count tables; numeric-ascending for distributions).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MAIN_CHECKOUT = Path.home() / "workspace" / "glossa-lab"

DEFAULT_OUT = REPO_ROOT / "reports" / "phase138_results.json"

AI_DISCLOSURE = (
    "This execution was produced by an AI agent (Muse Spark, "
    "via Muse) at the direction of Tristen Pierson, per "
    "constitution §VI."
)

MANDATORY_STATEMENTS = [
    (
        "The Tamil Nadu graffiti corpus (tngraffiti.in) is not in "
        "hand — 0 records (access requested 2026-10-08; no reply on "
        "record). No number in this arm describes it."
    ),
    (
        "Dating-gap caveat: the Tamil Nadu graffiti material is "
        "separated from the Indus material by ≥ 1,000 years on the "
        "published rebuttal of the continuity claims (the "
        "Harappa.com critique of Rajan & Sivanantham). Any "
        "resemblance ever noted across that gap is formal "
        "resemblance across a millennium-plus separation — nothing "
        "more. This caveat attaches to every comparative statement "
        "in this arm."
    ),
    (
        "A permitted output of this arm is \"resemblance described\"; "
        "a prohibited output is any continuity, descent, or survival "
        "claim (spec 024 §5.5)."
    ),
]

NO_OVERLAP_STATISTIC_REASON = (
    "No overlap statistic against the seal-text sign repertoire is "
    "computed: no machine-readable sign-form repertoire of the "
    "catalogue graffiti objects exists in hand (the catalogue "
    "records photographs and captions, not transcriptions; "
    "Phase-132 closed the program's attempt to manufacture "
    "transcriptions from plates)."
)

KODUMANAL_PARAGRAPH = (
    "The Kodumanal volume is a trench-organized excavation report "
    "whose Graffiti Marks section describes marks by ware and by "
    "vessel position (shoulder near the rim), and as pre-firing vs "
    "surface marks (Phase-133 Stage 0 report §6.1). Its printed "
    "tallies are quoted as prose only, with their internal "
    "inconsistency stated: the section states \"Out of 175 graffiti "
    "marks 75 in Black and Red ware, 70 Red ware, 70 Russet Coated "
    "ware and 10 Black ware were noticed\" — subtotals summing to "
    "225 against a stated 175 — and separately that \"41 Brahmi "
    "sherds were observed and 99 Graffiti marks were collected\". "
    "No tally from the volume is used as a count anywhere in this "
    "arm."
)


def catalogue_dir() -> Path:
    """Locate the gitignored Phase-124 catalogue store."""
    candidates = [
        REPO_ROOT / "corpora" / "downloads" / "cisi_image_layer"
        / "catalogue",
        MAIN_CHECKOUT / "corpora" / "downloads" / "cisi_image_layer"
        / "catalogue",
    ]
    for cand in candidates:
        if (cand / "cisi_vol1_catalogue.csv").exists():
            return cand
    return candidates[0]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def median_iqr(values: list[float]) -> dict:
    """Median and IQR (inclusive quartiles) for a non-empty list."""
    if not values:
        return {"present_count": 0, "median": None, "q1": None,
                "q3": None, "iqr": None}
    ordered = sorted(values)
    median = statistics.median(ordered)
    if len(ordered) == 1:
        q1 = q3 = ordered[0]
    else:
        q1, _median_dup, q3 = statistics.quantiles(
            ordered, n=4, method="inclusive")
    return {"present_count": len(ordered), "median": median,
            "q1": q1, "q3": q3, "iqr": q3 - q1}


def _value_counts(values) -> list[dict]:
    counts = Counter(values)
    return [{"value": value, "count": count}
            for value, count in sorted(
                counts.items(), key=lambda kv: (-kv[1], kv[0]))]


def _object_key(row: dict) -> tuple[str, str]:
    """Volume-scoped object identity: cisi:v{volume}:{cisi_id}."""
    return (row["volume"], row["cisi_id"])


def _rows_per_object(rows: list[dict]) -> dict:
    per_object = Counter(_object_key(row) for row in rows)
    dist = Counter(per_object.values())
    return {str(k): dist[k] for k in sorted(dist)}


def _distinct_by_site(rows: list[dict]) -> dict:
    """Distinct volume-scoped objects per catalogue site, as printed.

    An object's site is taken from its rows; an object appearing
    under more than one site value would be counted once under each
    (none occurs in the population as run). The empty-string site
    is the no-site count.
    """
    object_sites: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in rows:
        object_sites[_object_key(row)].add(row["site"])
    counts: Counter = Counter()
    for sites in object_sites.values():
        for site in sites:
            counts[site] += 1
    entries = [{"site": site, "distinct_objects": counts[site]}
               for site in sorted(counts, key=lambda s: (-counts[s], s))]
    return {
        "distinct_objects_by_site": entries,
        "no_site_count": counts.get("", 0),
    }


def describe_subset(rows: list[dict]) -> dict:
    """The §2.2–2.3 descriptives for one object_type subset."""
    return {
        "rows": len(rows),
        "distinct_objects": len({_object_key(r) for r in rows}),
        **_distinct_by_site(rows),
        "rows_per_object_distribution": _rows_per_object(rows),
    }


def describe_graffiti(rows: list[dict]) -> dict:
    out = describe_subset(rows)
    out["side_value_counts"] = _value_counts(r["side"] for r in rows)
    out["bis_value_counts"] = _value_counts(r["bis"] for r in rows)
    filled = [r for r in rows if r["motif_chapter"].strip() != ""]
    out["motif_chapter"] = {
        "field_class": "Class C (CISI editors' chapter organization)",
        "total_rows": len(rows),
        "filled_rows": len(filled),
        "filled_rate": (len(filled) / len(rows)) if rows else 0.0,
        "distinct_values": _value_counts(
            r["motif_chapter"] for r in filled),
    }
    out["numeric_descriptors"] = {}
    for field in ("caption_ocr_score", "scale_pct"):
        values = []
        for row in rows:
            raw = (row[field] or "").strip()
            if raw:
                values.append(float(raw))
        out["numeric_descriptors"][field] = median_iqr(values)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--catalogue-dir", type=Path, default=None)
    args = parser.parse_args()

    cat_dir = args.catalogue_dir or catalogue_dir()
    inputs = []
    all_rows: dict[int, list[dict]] = {}
    for volume in (1, 2):
        path = cat_dir / f"cisi_vol{volume}_catalogue.csv"
        if not path.exists():
            print(f"input missing: {path}", file=sys.stderr)
            return 1
        with path.open(newline="", encoding="utf-8") as fh:
            all_rows[volume] = list(csv.DictReader(fh))
        inputs.append({
            "volume": volume,
            "path": str(path),
            "sha256": sha256_file(path),
        })

    by_volume: dict[str, dict] = {}
    pooled_graffiti: list[dict] = []
    context: dict[str, dict] = {}
    for volume in (1, 2):
        rows = all_rows[volume]
        graffiti = [r for r in rows if r["object_type"] == "Graffiti"]
        pooled_graffiti.extend(graffiti)
        by_volume[str(volume)] = describe_graffiti(graffiti)
    pooled = describe_graffiti(pooled_graffiti)

    for object_type in ("Seals", "Tablets"):
        per_volume = {}
        pooled_rows: list[dict] = []
        for volume in (1, 2):
            subset = [r for r in all_rows[volume]
                      if r["object_type"] == object_type]
            pooled_rows.extend(subset)
            per_volume[str(volume)] = describe_subset(subset)
        entry = describe_subset(pooled_rows)
        entry["by_volume"] = per_volume
        context[object_type] = entry

    results = {
        "phase": "Phase-138",
        "spec": "024 §5.5 (arm (d), Stage 2(d))",
        "freeze": "specs/024-evidence-integration/stage2d-freeze.md",
        "family_role": "none (descriptive only)",
        "descriptive_only": True,
        "ai_disclosure": AI_DISCLOSURE,
        "inputs": inputs,
        "population": {
            "definition": (
                "Phase-124 catalogue rows (CISI Vols. 1–2) with "
                "object_type exactly 'Graffiti'; distinct objects "
                "are volume-scoped (canonical key "
                "cisi:v{volume}:{cisi_id})."
            ),
            "rows_total": pooled["rows"],
            "distinct_objects_total": pooled["distinct_objects"],
            "by_volume": {
                vol: {"rows": d["rows"],
                      "distinct_objects": d["distinct_objects"]}
                for vol, d in by_volume.items()
            },
        },
        "graffiti": {"pooled": pooled, "by_volume": by_volume},
        "context_table": {
            "label": (
                "Catalogue-composition description only: the "
                "graffiti subset's catalogue shape read against the "
                "corpus it sits in. This is not a comparison of "
                "repertoires and licenses no inference. Graffiti "
                "rows are never pooled with seal or tablet rows in "
                "any joint repertoire."
            ),
            "by_object_type": context,
        },
        "kodumanal_qualitative": KODUMANAL_PARAGRAPH,
        "mandatory_statements": MANDATORY_STATEMENTS,
        "no_overlap_statistic_reason": NO_OVERLAP_STATISTIC_REASON,
        "quartile_method": (
            "statistics.quantiles(n=4, method='inclusive'); median "
            "via statistics.median."
        ),
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(f"wrote {args.out}: rows={pooled['rows']} "
          f"objects={pooled['distinct_objects']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

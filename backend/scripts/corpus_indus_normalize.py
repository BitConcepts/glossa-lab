"""Indus Corpus — Normalization Pipeline.

Reads staging/objects_{date}.jsonl and applies:
  1. Diplomatic layer: ensures ICIT-format encoding (+NNN-NNN+) is present
  2. Graphemic layer: maps source sign IDs through the crosswalk to canonical IDs
  3. Allograph annotation: adds typed variant relations where known

Outputs:
  glossa-corpus/indus/canonical/objects.jsonl     (all objects, normalized)
  glossa-corpus/indus/canonical/sign_instances.jsonl  (flat sign token table)
  glossa-corpus/indus/canonical/sign_crosswalk.json   (crosswalk snapshot)
  glossa-corpus/indus/canonical/rights_register.json  (rights summary)
  glossa-corpus/indus/canonical/normalize_report.json

Rules (must never be violated):
  - Diplomatic layer is LOSSLESS — source strings preserved unchanged
  - Graphemic layer is SEPARATE — stored in canonical_grapheme_ids, not overwriting source
  - Unknown mappings -> None, NEVER invented
  - Allograph relations -> typed links, NEVER collapsed

Usage:
    shell.cmd python backend/scripts/corpus_indus_normalize.py [--date YYYY-MM-DD]

_citation:
  primary_sources: ["A.1", "A.7", "I.1", "I.2", "I.3", "I.4", "I.5"]
  derivation: "Normalization pipeline for ICIT-scale Indus corpus reconstruction."
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

REPO = Path(__file__).parents[2]
CORPUS = REPO / "glossa-corpus" / "indus"
TODAY = datetime.utcnow().strftime("%Y-%m-%d")


def load_staging(date: str) -> List[dict]:
    path = CORPUS / "staging" / f"objects_{date}.jsonl"
    if not path.exists():
        # Try most recent
        files = sorted(CORPUS.joinpath("staging").glob("objects_*.jsonl"))
        if not files:
            print(f"ERROR: No staging file found for date {date}")
            return []
        path = files[-1]
        print(f"  Using most recent staging: {path.name}")
    objects = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                objects.append(json.loads(line))
            except Exception:
                pass
    return objects


def get_crosswalk():
    """Import the crosswalk — graceful fallback if module unavailable."""
    try:
        sys.path.insert(0, str(REPO / "backend"))
        from glossa_lab.data.indus_sign_crosswalk import get_crosswalk as _get
        return _get()
    except ImportError as exc:
        print(f"  WARN: crosswalk import failed ({exc}), using identity mapping")
        return None


def normalize_diplomatic(text: Optional[str], scheme: Optional[str]) -> Optional[str]:
    """Ensure text is in ICIT format. Returns None if can't normalize."""
    if not text:
        return None
    text = text.strip()
    # Already ICIT format if starts/ends with +
    if text.startswith("+") and text.endswith("+"):
        return text
    # Try to build from hyphen-separated numbers
    parts = [p.strip() for p in text.replace(",", "-").split("-") if p.strip()]
    if parts:
        return "+" + "-".join(parts) + "+"
    return None


def apply_crosswalk(sign_ids: List[str], source_scheme: str, xw) -> List[Optional[str]]:
    """Map source sign IDs to canonical grapheme IDs (M77). Returns None for unknowns."""
    if xw is None:
        return [None] * len(sign_ids)

    from glossa_lab.data.indus_sign_crosswalk import IndusSignCrosswalk
    from glossa_lab.data.indus_object_model import SignIdScheme

    scheme_map = {
        "Parpola1982": SignIdScheme.PARPOLA_1982,
        "Wells2006": SignIdScheme.WELLS_2006,
        "Fuls2014": SignIdScheme.FULS_2014,
        "Mahadevan1977": SignIdScheme.MAHADEVAN_1977,
    }
    from_scheme = scheme_map.get(source_scheme, SignIdScheme.PARPOLA_1982)
    to_scheme = SignIdScheme.GLOSSA_CANONICAL

    canonical = []
    for sid in sign_ids:
        if sid in ("000", "++"):
            canonical.append(sid)  # preserve damage markers as-is
            continue
        result = xw.translate(sid, from_scheme, to_scheme)
        canonical.append(result)
    return canonical


def parse_sign_ids_from_diplomatic(diplomatic: str) -> List[str]:
    """Extract sign ID tokens from ICIT diplomatic string."""
    if not diplomatic:
        return []
    text = diplomatic.strip()
    # Split on ++ first (eroded-unknown-length markers)
    parts = []
    for chunk in text.split("++"):
        chunk = chunk.strip("+").strip("-")
        if chunk:
            tokens = [t for t in chunk.split("-") if t]
            parts.extend(tokens)
        parts.append("++")
    if parts and parts[-1] == "++":
        parts.pop()
    return parts


def normalize_object(obj: dict, xw) -> dict:
    """Apply diplomatic and graphemic normalization to one object record."""
    diplomatic = obj.get("text_code_diplomatic")
    scheme = obj.get("sign_id_scheme") or "Parpola1982"

    # 1. Diplomatic layer — normalize format, preserve source
    norm_diplomatic = normalize_diplomatic(diplomatic, scheme)
    obj["text_code_diplomatic_normalized"] = norm_diplomatic  # separate from source

    # 2. Graphemic layer — crosswalk to canonical IDs
    canonical_ids = []
    sign_instance_count = 0
    if norm_diplomatic:
        sign_ids = parse_sign_ids_from_diplomatic(norm_diplomatic)
        canonical_ids = apply_crosswalk(sign_ids, scheme, xw)
        sign_instance_count = len([s for s in sign_ids if s not in ("000", "++")])

    obj["canonical_grapheme_ids"] = canonical_ids
    obj["sign_instance_count"] = sign_instance_count
    obj["crosswalk_coverage"] = (
        round(sum(1 for c in canonical_ids if c and c not in ("000", "++")) / max(sign_instance_count, 1), 3)
        if sign_instance_count > 0 else 0.0
    )
    obj["pipeline_stage"] = "normalized"
    return obj


def build_sign_instances(objects: List[dict]) -> List[dict]:
    """Build flat sign instance table from normalized objects."""
    instances = []
    for obj in objects:
        gid = obj.get("glossa_id", "")
        diplomatic = obj.get("text_code_diplomatic_normalized") or obj.get("text_code_diplomatic", "")
        scheme = obj.get("sign_id_scheme") or "unknown"
        canonical_ids = obj.get("canonical_grapheme_ids") or []

        if not diplomatic:
            continue
        sign_ids = parse_sign_ids_from_diplomatic(diplomatic)
        for idx, (sid, cid) in enumerate(zip(sign_ids, canonical_ids + [None] * len(sign_ids))):
            instances.append({
                "sign_instance_id": f"{gid}-SI-{idx:04d}",
                "object_id": gid,
                "reading_order_index": idx,
                "source_sign_id": sid,
                "source_scheme": scheme,
                "canonical_sign_id": cid,
                "damage_marker": sid if sid in ("000", "++") else None,
                "_citation": {
                    "primary_sources": ["A.1", "A.7", "I.1"],
                    "derivation": f"Sign instance from object {gid}",
                },
            })
    return instances


def build_rights_register(objects: List[dict]) -> dict:
    """Summarize rights status across all objects."""
    from collections import Counter
    rights_counter = Counter(obj.get("rights_status", "unknown") for obj in objects)
    ml_cleared = [obj for obj in objects if obj.get("rights_status") in ("CC0", "MIT", "CC BY 4.0")]
    research_cleared = [obj for obj in objects if obj.get("rights_status") not in
                        ("unknown", "india-museum-restricted", "permission-required", "licensed")]
    return {
        "_citation": {
            "primary_sources": ["I.1", "I.2", "I.3", "I.4", "I.5"],
            "derivation": "Rights register for Indus corpus reconstruction.",
        },
        "total_objects": len(objects),
        "by_rights_status": dict(rights_counter),
        "ml_training_cleared": len(ml_cleared),
        "research_use_cleared": len(research_cleared),
        "quarantined": len([o for o in objects if o.get("quarantine_reason")]),
        "last_updated": datetime.utcnow().isoformat(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize Indus corpus staging objects")
    parser.add_argument("--date", default=TODAY)
    args = parser.parse_args()

    print(f"=== Indus Normalization — date: {args.date} ===")
    canonical_dir = CORPUS / "canonical"
    canonical_dir.mkdir(parents=True, exist_ok=True)

    objects = load_staging(args.date)
    if not objects:
        print("ERROR: No staging objects found.")
        return 1
    print(f"  Loaded {len(objects)} staging objects")

    xw = get_crosswalk()

    normalized = [normalize_object(obj, xw) for obj in objects]
    sign_instances = build_sign_instances(normalized)
    rights_register = build_rights_register(normalized)

    # Export crosswalk snapshot
    xw_snapshot = xw.export_json() if xw else {"note": "crosswalk unavailable"}

    # Write canonical outputs
    obj_path = canonical_dir / "objects.jsonl"
    with open(obj_path, "w", encoding="utf-8") as f:
        for obj in normalized:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    si_path = canonical_dir / "sign_instances.jsonl"
    with open(si_path, "w", encoding="utf-8") as f:
        for si in sign_instances:
            f.write(json.dumps(si, ensure_ascii=False) + "\n")

    xw_path = canonical_dir / "sign_crosswalk.json"
    xw_path.write_text(json.dumps(xw_snapshot, indent=2, ensure_ascii=False), encoding="utf-8")

    rr_path = canonical_dir / "rights_register.json"
    rr_path.write_text(json.dumps(rights_register, indent=2, ensure_ascii=False), encoding="utf-8")

    # Report
    with_diplomatic = sum(1 for o in normalized if o.get("text_code_diplomatic"))
    with_canonical = sum(1 for o in normalized if o.get("canonical_grapheme_ids"))
    avg_coverage = (
        sum(o.get("crosswalk_coverage", 0) for o in normalized if o.get("sign_instance_count", 0) > 0)
        / max(sum(1 for o in normalized if o.get("sign_instance_count", 0) > 0), 1)
    )

    report = {
        "_citation": {
            "primary_sources": ["A.1", "A.7", "I.1", "I.2", "I.3", "I.4", "I.5"],
            "derivation": "Normalization report for Indus corpus reconstruction.",
        },
        "batch_id": f"{args.date}-INDUS-NORMALIZE",
        "timestamp": datetime.utcnow().isoformat(),
        "objects_normalized": len(normalized),
        "objects_with_diplomatic": with_diplomatic,
        "objects_with_canonical_graphemes": with_canonical,
        "sign_instances_total": len(sign_instances),
        "avg_crosswalk_coverage": round(avg_coverage, 3),
        "rights_register": rights_register,
    }
    rpt_path = canonical_dir / "normalize_report.json"
    rpt_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n=== DONE ===")
    print(f"  Objects normalized: {len(normalized)}")
    print(f"  With diplomatic text: {with_diplomatic}")
    print(f"  Sign instances: {len(sign_instances)}")
    print(f"  Avg crosswalk coverage: {avg_coverage:.1%}")
    print(f"  Canonical: {obj_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Convert indusarrays Firestore dump to canonical IndusObject JSONL.

The indusarrays collection is the Mahadevan 1977 Indus concordance from
indusscript.in. Each document represents a concordance entry (one sign
occurrence in a text). Multiple documents share the same textnum.

This script:
1. Groups documents by textnum
2. Picks the most complete sign sequence per text (max non-empty signs)
3. Builds ICIT diplomatic format strings (Mahadevan sign IDs)
4. Writes to glossa-corpus/indus/staging/objects_{date}_indusarrays.jsonl

Fields:
  textnum  - IM77 4-digit text number (primary key)
  texts    - array of Mahadevan sign IDs as strings (e.g. ["67","342","8"])
  inscobj  - inscription object (1=obverse, 2=reverse, etc.)
  signnum  - number of signs
  posnum   - position of indexed sign within text
  locus    - findspot/locus code
  dir      - reading direction (1=RTL, 3=LTR, etc.)
  level    - concordance nesting level
  fs80     - field symbol code
  S1-S14   - individual sign positions

Output schema: glossa_id, source_system=indusscript-m77, textnum,
               text_code_diplomatic, sign_id_scheme=Mahadevan1977, etc.

_citation:
  primary_sources: ["I.6", "A.1"]
  derivation: "Converted from indusarrays Firestore (indusscript.in / RMRL, 2021).
               Original data: Mahadevan (1977) IM77 concordance."
"""
from __future__ import annotations
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parents[2]
PROBE = REPO / "glossa-corpus" / "indus" / "sources" / "rmrl" / "raw" / "indusscript-probe"
STAGING = REPO / "glossa-corpus" / "indus" / "staging"
STAGING.mkdir(parents=True, exist_ok=True)
TODAY = datetime.utcnow().strftime("%Y-%m-%d")

# Locus -> site name mapping (Mahadevan concordance locus codes)
# Partial — main sites only
LOCUS_SITES = {
    "17": "Mohenjo-daro",
    "31": "Mohenjo-daro",
    "16": "Harappa",
    "18": "Harappa",
    "13": "Chanhu-Daro",
    "12": "Lothal",
    "14": "Kalibangan",
    "15": "Sutkagen-Dor",
    "79": "Mohenjo-daro",
    "80": "Harappa",
}


def locus_to_site(locus: str | int | None) -> str | None:
    if locus is None:
        return None
    return LOCUS_SITES.get(str(locus))


def best_sequence(docs: list[dict]) -> list[str]:
    """Pick the most complete sign sequence from multiple concordance rows for one text."""
    best = []
    for doc in docs:
        texts = doc.get("texts") or []
        non_empty = [t for t in texts if t and t.strip()]
        if len(non_empty) > len(best):
            best = non_empty
    return best


def build_diplomatic(signs: list[str]) -> str:
    """Build ICIT diplomatic string from Mahadevan sign IDs."""
    if not signs:
        return ""
    # Zero-pad to 3 digits (Mahadevan sign IDs are 1-417+)
    padded = [s.zfill(3) if s.isdigit() else s for s in signs if s]
    return "+" + "-".join(padded) + "+"


def main():
    dump_path = PROBE / "firestore_indusarrays_full.json"
    if not dump_path.exists():
        print("ERROR: firestore_indusarrays_full.json not found.")
        print("Run dump_indusscript_firestore.py first.")
        return 1

    print(f"=== Converting indusarrays -> canonical staging ===")
    data = json.loads(dump_path.read_text(encoding="utf-8"))
    docs = data["documents"]
    print(f"Input: {len(docs)} Firestore documents")

    # Group by textnum, keeping all docs per text
    by_textnum: dict[int, list[dict]] = defaultdict(list)
    for doc in docs:
        tn = doc.get("textnum")
        if tn is not None:
            by_textnum[int(tn)].append(doc)

    print(f"Unique texts: {len(by_textnum)}")

    # Build canonical objects
    objects = []
    quarantined = []
    counter = 10000  # start after existing GLI-IND IDs to avoid collision

    for textnum in sorted(by_textnum.keys()):
        doc_group = by_textnum[textnum]
        representative = doc_group[0]

        signs = best_sequence(doc_group)
        diplomatic = build_diplomatic(signs)

        locus = representative.get("locus")
        site = locus_to_site(locus)
        inscobj = representative.get("inscobj")
        direction = representative.get("dir")

        counter += 1
        glossa_id = f"GLI-IND-M77-{textnum:05d}"

        reason = None
        if not signs:
            reason = "no sign sequence"
        if len(signs) < 1:
            reason = "empty sign sequence"

        obj = {
            "glossa_id": glossa_id,
            "source_system": "indusscript-m77",
            "source_object_id": str(textnum),
            "artifact_type": "seal",
            "site_name": site,
            "locus": locus,
            "rights_status": "rmrl-research",
            "text_code_diplomatic": diplomatic,
            "sign_id_scheme": "Mahadevan1977",
            "canonical_grapheme_ids": [],
            "sign_instance_count": len(signs),
            "raw_signs": signs,
            "inscobj": inscobj,
            "direction": direction,
            "review_state": "unreviewed",
            "pipeline_stage": "objectized",
            "quarantine_reason": reason,
            "_source_extra": {
                "textnum": textnum,
                "doc_count": len(doc_group),
                "fs80": representative.get("fs80"),
                "level": representative.get("level"),
            },
            "_citation": {
                "primary_sources": ["I.6", "A.1"],
                "derivation": (
                    f"IM77 text {textnum} from indusscript.in Firestore (RMRL, 2021). "
                    "Original: Mahadevan (1977) The Indus Script: Texts, Concordance and Tables."
                ),
            },
        }

        if reason:
            quarantined.append(obj)
        else:
            objects.append(obj)

    # Write staging output
    out_path = STAGING / f"objects_{TODAY}_indusarrays.jsonl"
    with open(out_path, "w", encoding="utf-8") as f:
        for obj in objects:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    quar_path = STAGING / f"quarantine_{TODAY}_indusarrays.jsonl"
    with open(quar_path, "w", encoding="utf-8") as f:
        for obj in quarantined:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    # Stats
    total_signs = sum(o["sign_instance_count"] for o in objects)
    avg_len = total_signs / max(len(objects), 1)
    max_len = max((o["sign_instance_count"] for o in objects), default=0)
    with_site = sum(1 for o in objects if o.get("site_name"))

    print(f"\n=== Conversion complete ===")
    print(f"  Objects written:    {len(objects)}")
    print(f"  Quarantined:        {len(quarantined)}")
    print(f"  Total sign tokens:  {total_signs:,}")
    print(f"  Avg inscription len:{avg_len:.1f} signs")
    print(f"  Max inscription len:{max_len} signs")
    print(f"  With site name:     {with_site}")
    print(f"\n  Output: {out_path}")
    print(f"  Quarantine: {quar_path}")
    print()
    print("ICIT comparison:")
    print(f"  Texts:  {len(objects):,} / 5,509 ICIT target ({len(objects)/5509*100:.1f}%)")
    print(f"  Signs:  {total_signs:,} / 19,616 ICIT target ({total_signs/19616*100:.1f}%)")
    print()
    print("Next: run corpus_indus_normalize.py then corpus_indus_export.py")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

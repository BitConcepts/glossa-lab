#!/usr/bin/env python3
"""Spec 093 Stage 2 — T201 grounding counts.

Counts, from the pinned files, the populations and field
distributions the Stage 2 channel definition (T201) and
freeze (T202) name: the sequence population, the
sequence-and-site population, and the Stage 1 join's
population, with each registered culture-side field's
presence, variance, and class counts on each. Presence
counting only, in the Stage 1 census's method and under
its empty convention: no statistic relating a
culture-side value to a sequence property is computed.

Usage: python3 stage2_counts.py <repo-root>
Prints one JSON document on stdout. Deterministic: the
same inputs produce the same document byte-for-byte.
"""
import collections
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
SENTINELS = {"", "None", "-", "--"}


def is_empty(v):
    if v is None:
        return True
    if isinstance(v, (list, dict)):
        return len(v) == 0
    if isinstance(v, str):
        return v.strip() in SENTINELS
    return False


def present(rec, field):
    return field in rec and not is_empty(rec[field])


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


out = {}
snap_path = ROOT / "glossa-corpus/indus/exports/indus_research.jsonl"
snap = load_jsonl(snap_path)
out["snapshot"] = {"path": "glossa-corpus/indus/exports/indus_research.jsonl",
                   "sha256": sha256(snap_path), "rows": len(snap)}

seq_pop = [r for r in snap if present(r, "canonical_grapheme_ids")]
out["sequence_population"] = {
    "n": len(seq_pop),
    "by_source": dict(collections.Counter(r["source_system"] for r in seq_pop)),
}
SP = {}
for f in ["site_name", "artifact_type", "current_holding", "material",
          "accession_number", "sign_id_scheme", "rights_status",
          "crosswalk_coverage"]:
    rs = [r for r in seq_pop if present(r, f)]
    SP[f] = {"present": len(rs),
             "distinct": len({str(r[f]) for r in rs}),
             "top": dict(collections.Counter(str(r[f]) for r in rs).most_common(12))}
out["sequence_population_fields"] = SP

# Population A: sequence + site
popA = [r for r in seq_pop if present(r, "site_name")]
out["population_A_seq_site"] = {
    "n": len(popA),
    "by_source": dict(collections.Counter(r["source_system"] for r in popA)),
    "site_counts": dict(collections.Counter(r["site_name"] for r in popA).most_common()),
    "scheme_counts": dict(collections.Counter(str(r.get("sign_id_scheme")) for r in popA)),
    "rights_counts": dict(collections.Counter(str(r.get("rights_status")) for r in popA)),
    "crosswalk_counts": dict(collections.Counter(str(r.get("crosswalk_coverage")) for r in popA)),
    "artifact_type_counts": dict(collections.Counter(str(r.get("artifact_type")) for r in popA)),
}

# Join pairs / Population B
pairs_path = ROOT / "specs/093-material-context-channel/records/t103-join-pairs-v1.jsonl"
pairs = load_jsonl(pairs_path)
out["join_pairs"] = {"path": "specs/093-material-context-channel/records/t103-join-pairs-v1.jsonl",
                     "sha256": sha256(pairs_path), "n": len(pairs),
                     "keys": sorted(pairs[0].keys())}
by_id = {r["glossa_id"]: r for r in snap}
text_ids = [p["text_id"] for p in pairs]
out["population_B_joined"] = {
    "n_pairs": len(pairs),
    "text_records_found": sum(1 for t in text_ids if t in by_id),
    "text_records_with_graphemes": sum(
        1 for t in text_ids if t in by_id and present(by_id[t], "canonical_grapheme_ids")),
    "material_raw_counts": dict(collections.Counter(p["material_raw"] for p in pairs).most_common()),
    "material_raw_present": sum(1 for p in pairs if not is_empty(p["material_raw"])),
    "type_counts": dict(collections.Counter(p["type"] for p in pairs).most_common()),
    "area_section_counts": dict(collections.Counter(p["area_section"] for p in pairs).most_common()),
    "area_section_present": sum(1 for p in pairs if not is_empty(p["area_section"])),
    "excavation_idno_distinct": len({p["excavation_idno"] for p in pairs
                                     if not is_empty(p["excavation_idno"])}),
    "period_counts": dict(collections.Counter(p["period"] for p in pairs).most_common()),
    "site_counts": dict(collections.Counter(p["site"] for p in pairs).most_common()),
    "snapshot_side": {
        "source": dict(collections.Counter(by_id[t]["source_system"] for t in text_ids if t in by_id)),
        "artifact_type": dict(collections.Counter(str(by_id[t].get("artifact_type")) for t in text_ids if t in by_id)),
        "site_name_present": sum(1 for t in text_ids if t in by_id and present(by_id[t], "site_name")),
        "holding_present": sum(1 for t in text_ids if t in by_id and present(by_id[t], "current_holding")),
        "material_present": sum(1 for t in text_ids if t in by_id and present(by_id[t], "material")),
    },
}

# Copresence over the whole snapshot (forcing counts for
# fields with no sequence-bearing population)
def both(a, b):
    return sum(1 for r in snap if a(r) and b(r))


has_seq = lambda r: present(r, "canonical_grapheme_ids")  # noqa: E731
out["copresence_with_sequence"] = {
    "site_name": both(has_seq, lambda r: present(r, "site_name")),
    "material": both(has_seq, lambda r: present(r, "material")),
    "current_holding": both(has_seq, lambda r: present(r, "current_holding")),
    "artifact_type": both(has_seq, lambda r: present(r, "artifact_type")),
    "accession_number": both(has_seq, lambda r: present(r, "accession_number")),
}
out["seq_no_site_by_source"] = dict(collections.Counter(
    r["source_system"] for r in seq_pop if not present(r, "site_name")))
print(json.dumps(out, indent=1, sort_keys=True))

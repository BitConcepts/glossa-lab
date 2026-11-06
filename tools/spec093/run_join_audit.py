#!/usr/bin/env python3
"""Spec 093 Stage 1 — T103 join audit.

Executes the frozen design in
specs/093-material-context-channel/records/t103-join-freeze-v1.md
exactly: key families K1 (cross-population exact keys) and K2
(CISI catalogue concordance), the §4 pair-correctness
criterion, the §6 complete-enumeration audit and 0.90 floor.

Usage:
  python3 run_join_audit.py <repo-root>            summary only
  python3 run_join_audit.py <repo-root> <out.json> <pairs.jsonl>

The full audit JSON carries every produced pair's adjudication;
the pairs file carries the accepted families' pairs only (the
join output). No input file is modified.
"""
import collections
import csv
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

PINS = {
    "snapshot": ("glossa-corpus/indus/exports/indus_research.jsonl",
                 "08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3"
                 "d84db5dc44505e"),
    "canonical": ("glossa-corpus/indus/canonical/objects.jsonl",
                  "e24f42a95ee4cc1fdb16c789c3edfb937993ed7c82223d6daa9"
                  "6d66895174ae5"),
    "csv": ("backend/glossa_lab/data/yajnadevam_inscriptions.csv",
            "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02"
            "c43428f58d98"),
}
FLOOR = 0.90
MUSEUM_SYSTEMS = {"PennMuseum", "MetOpenAccess",
                  "ClevelandArtOpenAccess", "MuseumsOfIndia"}
TEXT_SYSTEMS = {"indusscript-m77", "mayig-cisi"}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic_write(path, text):
    fd, tmp = tempfile.mkstemp(dir=str(Path(path).parent),
                               suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def normalize_object(source_object_id):
    if re.search(r"\d[AB]$", source_object_id):
        return source_object_id[:-1]
    return source_object_id


def run_audit(root):
    root = Path(root)
    for name, (rel, pin) in PINS.items():
        got = sha256(root / rel)
        if got != pin:
            print(f"PIN MISMATCH {name}: {got}")
            sys.exit(1)
    canon = [json.loads(l) for l in
             (root / PINS["canonical"][0]).read_text(
                 encoding="utf-8").splitlines() if l.strip()]
    csv_rows = list(csv.DictReader(
        (root / PINS["csv"][0]).open(encoding="utf-8")))
    museum = [r for r in canon if r["source_system"] in MUSEUM_SYSTEMS]
    text = [r for r in canon if r["source_system"] in TEXT_SYSTEMS]

    # ---------------- K1: cross-population exact keys
    k1 = {"accession_number": {"produced": 0,
                               "note": "accession_number is present "
                                       "only on the museum side; it "
                                       "produces no pairs"}}
    by_soi_text = {}
    for r in text:
        if r.get("source_object_id"):
            by_soi_text.setdefault(r["source_object_id"], []).append(r)
    k1_pairs = []
    for r in museum:
        soi = r.get("source_object_id")
        if soi and soi in by_soi_text:
            for t in by_soi_text[soi]:
                k1_pairs.append((r, t))
    k1_adj = []
    for m, t in k1_pairs:
        site_eq = bool(m.get("site_name")) and \
            m.get("site_name") == t.get("site_name")
        prov = ((m.get("_source_extra") or {}).get("provenience")
                or "")
        prov_names = bool(t.get("site_name")) and \
            t["site_name"].lower() in prov.lower()
        second_id = (
            (m.get("accession_number") and
             m.get("accession_number") == t.get("accession_number"))
            or (m.get("image_master_uri") and
                m.get("image_master_uri") == t.get("image_master_uri")))
        corroborated = bool(site_eq or prov_names or second_id)
        k1_adj.append({
            "key": m["source_object_id"],
            "museum_id": m["glossa_id"],
            "text_id": t["glossa_id"],
            "museum_system": m["source_system"],
            "text_system": t["source_system"],
            "corroboration": {"site_equal": site_eq,
                              "provenience_names_site": prov_names,
                              "second_identifier": bool(second_id)},
            "correct": corroborated,
        })
    k1_correct = sum(1 for p in k1_adj if p["correct"])
    k1_precision = (k1_correct / len(k1_adj)) if k1_adj else 0.0
    k1["source_object_id"] = {
        "produced": len(k1_adj), "correct": k1_correct,
        "precision": k1_precision,
        "verdict": "ACCEPTED" if k1_precision >= FLOOR else "REJECTED",
        "pairs": k1_adj}

    # ---------------- K2: CISI catalogue concordance
    csv_by_key = {}
    for row in csv_rows:
        c = (row.get("cisi") or "").strip()
        if c:
            csv_by_key.setdefault(c, []).append(row)
    cisi_records = [r for r in text if r["source_system"] == "mayig-cisi"]
    obj_to_records = collections.defaultdict(list)
    for r in cisi_records:
        obj_to_records[normalize_object(r["source_object_id"])].append(r)
    k2_adj = []
    unmatched_records = []
    for r in cisi_records:
        obj = normalize_object(r["source_object_id"])
        rows = csv_by_key.get(obj, [])
        if not rows:
            unmatched_records.append(r["glossa_id"])
            continue
        for row in rows:
            checks = {
                "catalogue_equal": True,
                "one_to_one": len(rows) == 1 and
                              len(obj_to_records[obj]) == 1,
                "site_prefix_consistent": row["site"] == "Mohenjo-daro",
                "type_consistent": row["type"].startswith("SEAL") and
                                   r["artifact_type"] == "seal",
            }
            k2_adj.append({
                "cisi_object": obj, "text_id": r["glossa_id"],
                "checks": checks,
                "correct": all(checks.values()),
                "_row": row})
    k2_correct = sum(1 for p in k2_adj if p["correct"])
    k2_precision = (k2_correct / len(k2_adj)) if k2_adj else 0.0
    k2_verdict = "ACCEPTED" if k2_precision >= FLOOR else "REJECTED"

    # diagnostics over the correct pairs (content agreement)
    diag_pairs = [p for p in k2_adj if p["correct"]]
    field_agree = 0
    token_agree = 0
    artifacts = 0
    nonnumeric_count_fields = []
    delta_dist = collections.Counter()
    content_disagreements = []
    by_id = {r["glossa_id"]: r for r in cisi_records}

    def parse_count(v):
        try:
            return int(v)
        except (TypeError, ValueError):
            return None

    def token_count(s):
        # Both files write a sequence as '+'-wrapped dash-joined
        # codes, e.g. '+001-368-861+': tokens split on '-'.
        s = (s or "").strip().strip("+")
        return len(s.split("-")) if s else 0

    for p in diag_pairs:
        r = by_id[p["text_id"]]
        row = p["_row"]
        csv_field = parse_count(row["text length"])
        csv_tokens = token_count(row["text"])
        mayig_field = r["sign_instance_count"]
        mayig_tokens = token_count(r["text_code_diplomatic"])
        if csv_field is None:
            nonnumeric_count_fields.append({
                "cisi_object": p["cisi_object"], "text_id": p["text_id"],
                "csv_text_length_raw": row["text length"]})
        if csv_field is not None and csv_field == mayig_field:
            field_agree += 1
        if csv_tokens == mayig_tokens:
            token_agree += 1
        delta_dist[csv_tokens - mayig_tokens] += 1
        if (csv_field is not None and csv_field != csv_tokens) or \
                mayig_field != mayig_tokens:
            artifacts += 1
        if csv_tokens != mayig_tokens:
            content_disagreements.append({
                "cisi_object": p["cisi_object"], "text_id": p["text_id"],
                "csv_tokens": csv_tokens, "mayig_tokens": mayig_tokens,
                "delta": csv_tokens - mayig_tokens,
                "csv_count_field": csv_field,
                "mayig_count_field": mayig_field})

    pairs_out = []
    if k2_verdict == "ACCEPTED":
        for p in diag_pairs:
            row = p["_row"]
            pairs_out.append({
                "text_id": p["text_id"], "cisi_object": p["cisi_object"],
                "material_raw": row["material"], "site": row["site"],
                "period": row["period"], "type": row["type"],
                "area_section": row["area-section"],
                "excavation_idno": row["excavation-idno"],
                "horizontal_mm": row["horizontal(mm)"],
                "vertical_mm": row["vertical(mm)"],
                "thickness_mm": row["thickness(mm)"]})
    pairs_out.sort(key=lambda d: d["cisi_object"])

    audit = {
        "audit": "t103-join-audit",
        "freeze": "t103-join-freeze-v1",
        "floor": FLOOR,
        "input_pins": {k: v[1] for k, v in PINS.items()},
        "K1": k1,
        "K2": {"produced": len(k2_adj), "correct": k2_correct,
               "precision": k2_precision, "verdict": k2_verdict,
               "unmatched_text_records": unmatched_records,
               "pairs": [{k: v for k, v in p.items() if k != "_row"}
                         for p in k2_adj],
               "diagnostics": {
                   "count_field_agreement": field_agree,
                   "token_count_agreement": token_agree,
                   "pairs_compared": len(diag_pairs),
                   "count_field_artifacts": artifacts,
                   "nonnumeric_csv_count_fields": nonnumeric_count_fields,
                   "token_delta_distribution": {
                       str(k): v for k, v in
                       sorted(delta_dist.items())},
                   "content_disagreements": content_disagreements}},
        "join_output": {"accepted_families": (
            ["K2"] if k2_verdict == "ACCEPTED" else []) +
            (["K1"] if k1_precision >= FLOOR else []),
            "pairs": len(pairs_out)},
    }
    return audit, pairs_out


def main():
    audit, pairs_out = run_audit(Path(sys.argv[1]))
    k1 = audit["K1"]["source_object_id"]
    k2 = audit["K2"]
    diag = k2["diagnostics"]
    print(f"K1 source_object_id: produced {k1['produced']}, correct "
          f"{k1['correct']}, precision {k1['precision']:.3f} -> "
          f"{k1['verdict']}")
    print(f"K2: produced {k2['produced']}, correct {k2['correct']}, "
          f"precision {k2['precision']:.3f} -> {k2['verdict']}; "
          f"unmatched text records: "
          f"{len(k2['unmatched_text_records'])}")
    print(f"diagnostics over {diag['pairs_compared']} correct pairs: "
          f"count-field agreement {diag['count_field_agreement']}, "
          f"token-count agreement {diag['token_count_agreement']}, "
          f"count-field artifacts {diag['count_field_artifacts']}")
    print("token delta distribution:",
          diag["token_delta_distribution"])
    print(f"join output: {len(pairs_out)} pairs")
    if len(sys.argv) > 3:
        atomic_write(sys.argv[2],
                     json.dumps(audit, indent=1, sort_keys=True))
        atomic_write(sys.argv[3], "".join(
            json.dumps(p, sort_keys=True) + "\n" for p in pairs_out))
        print("wrote audit JSON + pairs JSONL")


if __name__ == "__main__":
    main()

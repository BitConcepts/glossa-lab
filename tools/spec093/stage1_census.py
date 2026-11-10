#!/usr/bin/env python3
"""Spec 093 Stage 1 — T101 census computation.

Computes the completed culture-side census over the named
sources (plus the sources the 2026-11-05 grounding inventory
missed, which this census adds) from the pinned files in the
repository. Presence counting only: no statistic relating a
culture-side value to a sequence property is computed.

Usage: python3 stage1_census.py <repo-root>
Prints one JSON document on stdout. Deterministic: the same
inputs produce the same document except the `computed_at`
line, which is informational and no count depends on it.

Empty convention (uniform, stated in the census record): a
value is EMPTY iff it is None, an empty list/dict, or a
string whose stripped form is one of '', 'None', '-', '--'.
Presence counts use this convention; sentinel occurrences in
the snapshot's own fields are also reported raw so the
convention's effect is visible.
"""
import ast
import collections
import csv
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


def field_census(records, fields):
    return {f: sum(1 for r in records if present(r, f)) for f in fields}


def distinct(records, field):
    return sorted({str(r[field]) for r in records if present(r, field)})


out = {}

# ---------------------------------------------------------------- snapshot
snap_path = ROOT / "glossa-corpus/indus/exports/indus_research.jsonl"
snap = load_jsonl(snap_path)
FIELDS16 = ["glossa_id", "source_system", "rights_status", "artifact_type",
            "site_name", "current_holding", "material",
            "text_code_diplomatic", "text_code_diplomatic_normalized",
            "sign_id_scheme", "canonical_grapheme_ids",
            "sign_instance_count", "crosswalk_coverage", "image_master_uri",
            "accession_number", "_citation"]
S = {}
S["sha256"] = sha256(snap_path)
S["rows"] = len(snap)
S["fields"] = FIELDS16
_key_union = sorted({k for r in snap for k in r.keys()})
S["key_union"] = _key_union
S["key_count_per_record"] = dict(collections.Counter(
    len(r.keys()) for r in snap))
S["keys_beyond_the_16"] = [k for k in _key_union if k not in FIELDS16]
S["field_presence"] = field_census(snap, FIELDS16)
S["value_types"] = {f: sorted({type(r[f]).__name__ for r in snap})
                    for f in FIELDS16}
by_src = collections.defaultdict(list)
for r in snap:
    by_src[r["source_system"]].append(r)
S["rows_by_source"] = {k: len(v) for k, v in sorted(by_src.items())}
S["presence_by_source"] = {
    src: field_census(rs, FIELDS16) for src, rs in sorted(by_src.items())}


def seq(r):
    return present(r, "text_code_diplomatic")


SIDE = {"sequence": lambda r: seq(r),
        "site": lambda r: present(r, "site_name"),
        "material": lambda r: present(r, "material"),
        "holding": lambda r: present(r, "current_holding"),
        "accession": lambda r: present(r, "accession_number"),
        "image": lambda r: present(r, "image_master_uri")}
S["copresence"] = {}
keys = list(SIDE)
for i, a in enumerate(keys):
    for b in keys[i + 1:]:
        S["copresence"][f"{a}&{b}"] = sum(
            1 for r in snap if SIDE[a](r) and SIDE[b](r))
S["site_distribution_all"] = dict(
    collections.Counter(r["site_name"] for r in snap
                        if present(r, "site_name")).most_common())
S["site_distribution_sequence_population"] = dict(
    collections.Counter(r["site_name"] for r in snap
                        if seq(r) and present(r, "site_name")).most_common())
S["site_distribution_by_source"] = {
    src: dict(collections.Counter(r["site_name"] for r in rs
                                  if present(r, "site_name")).most_common())
    for src, rs in sorted(by_src.items())}
S["distinct_counts"] = {
    "site_name": len(distinct(snap, "site_name")),
    "current_holding": len(distinct(snap, "current_holding")),
    "material": len(distinct(snap, "material")),
    "accession_number": len(distinct(snap, "accession_number")),
}
S["holdings"] = distinct(snap, "current_holding")
S["artifact_type_by_source"] = {
    src: dict(collections.Counter(r["artifact_type"] for r in rs))
    for src, rs in sorted(by_src.items())}
S["rights_by_source"] = {
    src: dict(collections.Counter(r["rights_status"] for r in rs))
    for src, rs in sorted(by_src.items())}
S["scheme_counts"] = dict(collections.Counter(
    r["sign_id_scheme"] for r in snap if present(r, "sign_id_scheme")))
# sequence bookkeeping anomalies (counting facts about the record system)
anom = {"seq_records": 0, "count_zero": [], "count_vs_graphemes_mismatch": 0,
        "count_vs_code_tokens_mismatch": 0}


def code_tokens(s):
    return [t for t in str(s).strip("+").split("-") if t not in ("", "+")]


for r in snap:
    if not seq(r):
        continue
    anom["seq_records"] += 1
    if r["sign_instance_count"] == 0:
        anom["count_zero"].append(r["glossa_id"])
    if r["sign_instance_count"] != len(r["canonical_grapheme_ids"]):
        anom["count_vs_graphemes_mismatch"] += 1
    if r["sign_instance_count"] != len(code_tokens(r["text_code_diplomatic"])):
        anom["count_vs_code_tokens_mismatch"] += 1
anom["records_with_000_token"] = sum(
    1 for r in snap if seq(r) and "000" in code_tokens(r["text_code_diplomatic"]))
anom["mismatch_and_000"] = sum(
    1 for r in snap if seq(r)
    and r["sign_instance_count"] != len(code_tokens(r["text_code_diplomatic"]))
    and "000" in code_tokens(r["text_code_diplomatic"]))
S["sequence_bookkeeping"] = anom
S["crosswalk_coverage_1_by_source"] = {
    src: sum(1 for r in rs if r["crosswalk_coverage"] == 1.0)
    for src, rs in sorted(by_src.items())}
out["snapshot"] = S

# ---------------------------------------------------------------- canonical
can_path = ROOT / "glossa-corpus/indus/canonical/objects.jsonl"
can = load_jsonl(can_path)
C = {}
C["sha256"] = sha256(can_path)
C["rows"] = len(can)
CAN_FIELDS = sorted(can[0].keys())
C["fields"] = CAN_FIELDS
cby = collections.defaultdict(list)
for r in can:
    cby[r["source_system"]].append(r)
C["rows_by_source"] = {k: len(v) for k, v in sorted(cby.items())}
EXTRA = ["dimensions_mm", "source_object_id", "_source_extra",
         "pipeline_stage", "review_state", "quarantine_reason"]
C["extra_field_presence_by_source"] = {
    src: field_census(rs, EXTRA) for src, rs in sorted(cby.items())}
C["culture_field_presence_by_source"] = {
    src: field_census(rs, ["site_name", "material", "current_holding",
                           "accession_number", "text_code_diplomatic",
                           "image_master_uri"])
    for src, rs in sorted(cby.items())}
snap_ids = {r["glossa_id"] for r in snap}
can_ids = {r["glossa_id"] for r in can}
C["snapshot_ids_subset_of_canonical"] = snap_ids <= can_ids
C["canonical_ids_not_in_snapshot"] = len(can_ids - snap_ids)
C["not_in_snapshot_by_source"] = dict(collections.Counter(
    r["source_system"] for r in can if r["glossa_id"] not in snap_ids))
# _source_extra key census per source
extra_keys = {}
for src, rs in sorted(cby.items()):
    kc = collections.Counter()
    for r in rs:
        e = r.get("_source_extra")
        if isinstance(e, dict):
            kc.update(e.keys())
    extra_keys[src] = dict(kc)
C["source_extra_key_census"] = extra_keys


def extra_of(r):
    e = r.get("_source_extra")
    return e if isinstance(e, dict) else {}


penn = cby["PennMuseum"]
prov = [extra_of(r).get("provenience") for r in penn]
prov = [p for p in prov if not is_empty(p)]
C["penn_provenience"] = {
    "present": len(prov), "distinct": len(set(prov)),
    "top": dict(collections.Counter(prov).most_common(10)),
    "present_and_site_name": sum(
        1 for r in penn if not is_empty(extra_of(r).get("provenience"))
        and present(r, "site_name")),
}
C["penn_culture_present"] = sum(
    1 for r in penn if not is_empty(extra_of(r).get("culture")))
met = cby["MetOpenAccess"]
C["met_culture_top"] = dict(collections.Counter(
    extra_of(r).get("culture") for r in met).most_common(6))
C["dimensions_present_by_source"] = {
    src: sum(1 for r in rs if present(r, "dimensions_mm"))
    for src, rs in sorted(cby.items())}
rep = json.load(open(ROOT / "glossa-corpus/indus/exports/export_report.json"))
C["export_report"] = {
    "canonical_objects": rep.get("canonical_objects"),
    "research_export": rep.get("research_export"),
    "open_export": rep.get("open_export"),
}
out["canonical"] = C

# ---------------------------------------------------------------- open export
op = load_jsonl(ROOT / "glossa-corpus/indus/exports/indus_open.jsonl")
O = {"rows": len(op), "fields": sorted(op[0].keys()),
     "ids_subset_of_snapshot": {r["glossa_id"] for r in op} <= snap_ids,
     "field_presence": field_census(op, sorted(op[0].keys()))}
out["open_export"] = O

# ---------------------------------------------------------------- icit format
icf = json.load(open(ROOT / "glossa-corpus/indus/exports/indus_icit_format.json"))
I = {"type": type(icf).__name__}
if isinstance(icf, dict):
    I["top_keys"] = sorted(icf.keys())
    for k, v in icf.items():
        if isinstance(v, list):
            I[f"len_{k}"] = len(v)
            if v and isinstance(v[0], dict):
                I[f"item_keys_{k}"] = sorted(v[0].keys())
elif isinstance(icf, list):
    I["rows"] = len(icf)
    if icf and isinstance(icf[0], dict):
        I["item_keys"] = sorted(icf[0].keys())
out["icit_format_export"] = I

# ---------------------------------------------------------------- flat files
F = {}
for name, rel in [("m77", "reports/mahadevan_corpus_flat.txt"),
                  ("icit", "reports/icit_corpus_flat.txt")]:
    p = ROOT / rel
    lines = [l for l in open(p, encoding="utf-8").read().splitlines()
             if l.strip()]
    toks = [l.split() for l in lines]
    F[name] = {"sha256": sha256(p), "lines": len(lines),
               "tokens": sum(len(t) for t in toks),
               "distinct_codes": len({t for l in toks for t in l}),
               "max_code": max(int(t) for l in toks for t in l)}
out["flat_files"] = F

# ---------------------------------------------------------------- CISI corpus
cc = json.load(open(ROOT / "backend/glossa_lab/data/indus_cisi_corpus.json"))
ins = cc["inscriptions"]
CI = {"sha256": sha256(ROOT / "backend/glossa_lab/data/indus_cisi_corpus.json"),
      "inscriptions": len(ins),
      "fields": sorted(ins[0].keys()),
      "field_presence": field_census(ins, sorted(ins[0].keys())),
      "site_values": dict(collections.Counter(str(i.get("site"))
                                              for i in ins)),
      "header": {k: cc.get(k) for k in
                 ["n_inscriptions", "n_sign_tokens", "n_distinct_signs",
                  "sign_numbering"]}}
out["cisi_corpus"] = CI
fs = json.load(open(ROOT / "backend/glossa_lab/data/cisi_findspots.json"))
FS = {"sha256": sha256(ROOT / "backend/glossa_lab/data/cisi_findspots.json"),
      "top_keys": sorted(fs.keys())}
for k in ["site_prefix_to_findspot", "core_indus_prefixes",
          "mesopotamia_dilmun_external_prefixes_in_other_volumes"]:
    if isinstance(fs.get(k), dict):
        FS[k + "_entries"] = len(fs[k])
        FS[k + "_entry_fields"] = sorted(
            next(iter(fs[k].values())).keys()) if fs[k] else []
out["cisi_findspots"] = FS

# ---------------------------------------------------------------- yajnadevam csv
csv_path = ROOT / "backend/glossa_lab/data/yajnadevam_inscriptions.csv"
with open(csv_path, encoding="utf-8") as f:
    yrows = list(csv.DictReader(f))
Y = {"sha256": sha256(csv_path), "rows": len(yrows),
     "fields": list(yrows[0].keys()),
     "field_presence": field_census(yrows, list(yrows[0].keys()))}
Y["distinct_sites"] = len(distinct(yrows, "site"))
Y["site_top"] = dict(collections.Counter(
    r["site"] for r in yrows if present(r, "site")).most_common(8))
Y["distinct_materials"] = len(distinct(yrows, "material"))
Y["material_top"] = dict(collections.Counter(
    r["material"] for r in yrows if present(r, "material")).most_common(10))
cvals = [r["cisi"] for r in yrows if present(r, "cisi")]
Y["cisi_present"] = len(cvals)
Y["cisi_distinct"] = len(set(cvals))
Y["cisi_m_prefix_rows"] = sum(1 for c in cvals if c.startswith("M-"))
Y["period_top"] = dict(collections.Counter(
    r["period"] for r in yrows if present(r, "period")).most_common(8))
Y["type_top"] = dict(collections.Counter(
    r["type"] for r in yrows if present(r, "type")).most_common(8))
out["yajnadevam_csv"] = Y

# ---------------------------------------------------------------- contact zone
Z = {}
zdir = ROOT / "glossa-corpus/indus/sources/contact-zone-rebuilt-2026-10-25"
seals = json.load(open(zdir / "seals_at_mesopotamia.json"))["seals"]
Z["seals"] = {"rows": len(seals), "fields": sorted(seals[0].keys()),
              "field_presence": field_census(seals, sorted(seals[0].keys()))}
mel = json.load(open(zdir / "meluhha_tablets.json"))
hits = mel["tablets"]
Z["meluhha"] = {"rows": len(hits), "fields": sorted(hits[0].keys()),
                "field_presence": field_census(hits, sorted(hits[0].keys())),
                "header_n_hits": mel.get("n_hits")}
lau = json.load(open(zdir / "laursen_2010_table1.json"))
lrows = lau["rows"]
Z["laursen"] = {"rows": len(lrows), "fields": sorted(lrows[0].keys()),
                "field_presence": field_census(lrows, sorted(lrows[0].keys())),
                "n_inscribed_with_indus_text": lau.get(
                    "n_inscribed_with_indus_text"),
                "n_rows_expected": lau.get("n_rows_expected")}
out["contact_zone"] = Z

# ---------------------------------------------------------------- catalogue seeder
src = (ROOT / "backend/glossa_lab/corpus_catalogue_seeder.py").read_text(
    encoding="utf-8")
tree = ast.parse(src)
catalogue = None
for node in ast.walk(tree):
    if isinstance(node, ast.AnnAssign) and isinstance(
            node.target, ast.Name) and node.target.id == "CATALOGUE":
        catalogue = ast.literal_eval(node.value)
    if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "CATALOGUE"
            for t in node.targets):
        catalogue = ast.literal_eval(node.value)
CAT = {"entries": len(catalogue),
       "fields": sorted(catalogue[0].keys()),
       "field_presence": field_census(catalogue, sorted(catalogue[0].keys()))}
out["corpus_catalogue"] = CAT

# ---------------------------------------------------------------- batches
B = {}
bdir = ROOT / "glossa-corpus/indus/sources"
for p in sorted(bdir.glob("batch_*.json")) + [bdir / "master_acquisition_2026-05-14.json"]:
    if not p.exists():
        continue
    d = json.load(open(p, encoding="utf-8"))
    entry = {"wrapper_keys": sorted(d.keys()) if isinstance(d, dict) else None}
    res = d.get("results") if isinstance(d, dict) else None
    if isinstance(res, dict):
        entry["results_form"] = "summary dict (acquisition manifest)"
        entry["results_keys"] = sorted(res.keys())
        entry["results_scalars"] = {
            k: v for k, v in res.items()
            if isinstance(v, (int, float, bool, str)) and len(str(v)) < 80}
    elif isinstance(res, list):
        entry["results_form"] = "record list"
        entry["results"] = len(res)
    B[p.name] = entry
out["acquisition_batches"] = B

section = sys.argv[2] if len(sys.argv) > 2 else None
if section:
    print(json.dumps(out[section], indent=1, sort_keys=True))
else:
    print(json.dumps(out, indent=1, sort_keys=True))

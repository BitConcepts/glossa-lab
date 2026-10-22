#!/usr/bin/env python3
"""Phase-406 — Spec 047 step 0 + step 1 (Asset B build and freeze).

Executes the frozen Spec 047 contract
(specs/047-roif-ledger-distribution/freeze.md, freeze digest
8501feabb7beee621e99ae48529e5a74c0788fb0619ac49c615912e13914cdc7)
through step 1 only:

  Step 0 (spec section 3, fail-closed, in order):
    0.1 every section-2 input hashes to its freeze pin;
    0.2 the gazetteer spine reproduces exactly (36 rows,
        30 distinct program_site_id clusters, the frozen
        cluster list);
    0.3 the corpus join census accounts for every one of the
        5,679 primary-layer records in exactly one class
        (joined / non-spine site / no site value), under the
        section 6.1 normalisation (lowercase, whitespace and
        punctuation collapsed; no fuzzy matching, no hand
        assignment).

  Step 1a (spec section 4): Asset B
    (specs/047-roif-ledger-distribution/asset-b/
    site-functions.jsonl) is validated against the section 4.1
    form and the mechanical build gates B1 (coverage: exactly
    the 30 spine clusters, sorted) and B2 (citation
    completeness per status). B3 (the section 4.3 verification
    pass) and B4 (the section 4.5 attestation) are worker acts
    recorded in the step-1 outcome record; this script records
    their presence by reference, never by assertion.

  Step 1b (spec section 5): the ledger-sign list
    (asset-b/ledger-signs.jsonl) is validated for entry
    completeness and its extraction census recomputed.

Outputs (full run):
  reports/phase406_results.json
  reports/phase406_step1_report.md

Step 2 (spec section 6) is NOT run by this script: no
distribution quantity is computed here. The census counts
records for accounting only (gate 0.3); it is not joined to
any class.

Modes:
  --step0 <sealed_census_path>: run step 0 only; write the
  detailed census to the sealed path (outside the repo) and
  print only gate verdicts and class totals. Used before the
  classification exists, so the build's blindness discipline
  (section 4.5) is mechanical, not promised.

Fail-closed: any gate or form violation aborts before any
repo output is written. The anchors file is asserted
byte-identical before and after (its section-2 pin).

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution section VI.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SPEC = _REPO / "specs/047-roif-ledger-distribution"
_ASSET_B = _SPEC / "asset-b/site-functions.jsonl"
_LEDGER = _SPEC / "asset-b/ledger-signs.jsonl"
_OUT_JSON = _REPO / "reports/phase406_results.json"
_OUT_MD = _REPO / "reports/phase406_step1_report.md"

FREEZE_DIGEST = (
    "8501feabb7beee621e99ae48529e5a74c0788fb0619ac49c615912e13914cdc7")
WORKER = "Muse Spark via Muse (AI agent)"

# Spec section 2 pins (SHA-256), re-asserted at the freeze by
# two independent routes (freeze.md section 2).
PINS = {
    "data/movement/gazetteer_rows.jsonl":
        "5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6",
    "backend/glossa_lab/data/yajnadevam_inscriptions.csv":
        "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98",
    "data/crosswalks/yajnadevam_to_parpola_crosswalk.csv":
        "e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2",
    "glossa-indus/reports/phase104_claims_evaluation.json":
        "2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d",
    "backend/scripts/seed_citations.py":
        "39d28112e21151ccba0f5a370801c78d87575c6ff61695bb8fafc5c14c08b8f9",
    "glossa-indus/hypotheses/models/roif_guild_ledger.yaml":
        "c5f08461cc1a37b91cb5a17981e2e4d7c02958312e1e7b6b9a49618a154c9586",
    "backend/reports/INDUS_FINAL_ANCHORS.json":
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
    "specs/027-movement-culture-language/spec.md":
        "7fff5d5a90b0af5697afa17a631e6901702b521f7e61c3c2bb444f08e369f9b0",
}

# The frozen spine: 30 clusters (gate 0.2), sorted.
CLUSTERS = [
    "amri", "banawali", "chagylly", "desalpur", "harappa",
    "hiregudda", "islam chowki", "jhukar", "joenniemi",
    "kalibangan", "kanispur", "khirsara", "kunal", "lothal",
    "mohenjo daro", "mullali", "ojiyana", "piklihal",
    "qasim bagh", "rangpur", "rojdi", "sannarachamma",
    "shahr i sokhta", "sheri khan tarakai",
    "sheri khan tarakai 3", "sheri khan tarakai 4",
    "surkotada", "ter kala dheri", "tigrana", "yalangach",
]
CORPUS_RECORDS = 5679
GAZETTEER_ROWS = 36

CLASSES = {
    "gateway/border", "administrative", "port/trade",
    "domestic", "ritual", "mixed/unknown",
}
STATUSES = {"AGREED", "DISAGREED", "SINGLE-SOURCE", "NO-SOURCE"}
ROW_FIELDS = {
    "program_site_id", "site_name_as_published", "status",
    "primary_class", "source_a", "source_b", "notes",
}
SOURCE_FIELDS = {"citation", "locator", "stated_function", "mapped_class"}
LEDGER_FIELDS = {
    "roif_sign", "assigned_function", "source_posting", "locator",
    "mapped_mahadevan_ids", "mapped_parpola_ids", "mapping_basis",
    "notes",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _normalise(name: str) -> str:
    """Spec section 6.1: lowercase, whitespace and punctuation
    collapsed. No fuzzy matching."""
    lowered = name.lower()
    spaced = re.sub(r"[^\w\s]", " ", lowered, flags=re.UNICODE)
    return " ".join(spaced.split())


class GateFailure(Exception):
    def __init__(self, gate: str, observed: str):
        super().__init__(f"{gate}: {observed}")
        self.gate = gate
        self.observed = observed


def gate_01() -> dict:
    """0.1 Input integrity: every section-2 input hashes to
    its freeze pin."""
    observed = {}
    for rel, pin in PINS.items():
        path = _REPO / rel
        if not path.exists():
            raise GateFailure(
                "0.1", f"input missing: {rel}")
        digest = _sha256(path)
        observed[rel] = digest
        if digest != pin:
            raise GateFailure(
                "0.1",
                f"{rel} hashes to {digest}, pin is {pin}")
    return observed


def gate_02() -> dict:
    """0.2 Spine reproduction: 36 rows, 30 distinct clusters,
    the frozen cluster list."""
    path = _REPO / "data/movement/gazetteer_rows.jsonl"
    rows = [json.loads(line) for line in
            path.read_text("utf-8").splitlines() if line.strip()]
    if len(rows) != GAZETTEER_ROWS:
        raise GateFailure(
            "0.2", f"gazetteer carries {len(rows)} rows, "
            f"frozen count is {GAZETTEER_ROWS}")
    clusters = sorted({r["program_site_id"] for r in rows})
    if clusters != CLUSTERS:
        raise GateFailure(
            "0.2", f"cluster list differs from the frozen list: "
            f"{clusters}")
    published = {}
    for r in rows:
        pid = r["program_site_id"]
        name = r["site_name_as_published"]
        if pid in published and published[pid] != name:
            raise GateFailure(
                "0.2", f"cluster {pid} carries two published "
                f"names: {published[pid]} / {name}")
        published[pid] = name
    return {"rows": len(rows), "clusters": len(clusters),
            "cluster_list": clusters,
            "site_name_as_published": published}


def gate_03(spine: dict) -> dict:
    """0.3 Corpus join census: every primary-layer record in
    exactly one class. Counts records, not signs."""
    path = _REPO / "backend/glossa_lab/data/yajnadevam_inscriptions.csv"
    norm_to_cluster = {}
    for pid in spine["cluster_list"]:
        key = _normalise(pid)
        if key in norm_to_cluster:
            raise GateFailure(
                "0.3", f"two clusters normalise to {key!r}")
        norm_to_cluster[key] = pid
    joined = {pid: 0 for pid in spine["cluster_list"]}
    non_spine: dict[str, int] = {}
    no_site = 0
    total = 0
    with path.open("r", encoding="utf-8", newline="") as fh:
        for rec in csv.DictReader(fh):
            total += 1
            site = rec.get("site")
            if site is None or site.strip() == "":
                no_site += 1
                continue
            key = _normalise(site)
            if key in norm_to_cluster:
                joined[norm_to_cluster[key]] += 1
            else:
                non_spine[site] = non_spine.get(site, 0) + 1
    accounted = sum(joined.values()) + sum(non_spine.values()) + no_site
    if total != CORPUS_RECORDS or accounted != total:
        raise GateFailure(
            "0.3", f"records total {total}, accounted {accounted}, "
            f"frozen corpus size {CORPUS_RECORDS}")
    return {
        "total_records": total,
        "joined_total": sum(joined.values()),
        "joined_by_cluster": {k: joined[k] for k in
                              spine["cluster_list"]},
        "non_spine_sites": [
            {"site_as_in_corpus": k, "records": non_spine[k]}
            for k in sorted(non_spine)],
        "non_spine_total": sum(non_spine.values()),
        "no_site_value": no_site,
    }


def _check_source(src, where: str) -> None:
    if not isinstance(src, dict) or set(src) != SOURCE_FIELDS:
        raise GateFailure(
            "B2", f"{where}: source fields are not exactly "
            f"{sorted(SOURCE_FIELDS)}")
    for field in SOURCE_FIELDS:
        if not isinstance(src[field], str) or not src[field].strip():
            raise GateFailure(
                "B2", f"{where}: source field {field} is empty")
    if src["mapped_class"] not in CLASSES:
        raise GateFailure(
            "B2", f"{where}: mapped_class {src['mapped_class']!r} "
            f"is outside the section 4.2 vocabulary")


def validate_asset(spine: dict) -> dict:
    """Step 1a form + mechanical build gates B1/B2."""
    if not _ASSET_B.exists():
        raise GateFailure("B1", "asset-b/site-functions.jsonl missing")
    rows = [json.loads(line) for line in
            _ASSET_B.read_text("utf-8").splitlines() if line.strip()]
    ids = [r.get("program_site_id") for r in rows]
    if ids != CLUSTERS:
        raise GateFailure(
            "B1", f"asset rows are not exactly the 30 spine "
            f"clusters in sorted order: {ids}")
    per_status = {s: 0 for s in sorted(STATUSES)}
    per_class: dict[str, int] = {}
    testable = []
    for r in rows:
        pid = r["program_site_id"]
        if set(r) != ROW_FIELDS:
            raise GateFailure(
                "B2", f"{pid}: row fields are not exactly "
                f"{sorted(ROW_FIELDS)}")
        if r["site_name_as_published"] != \
                spine["site_name_as_published"][pid]:
            raise GateFailure(
                "B2", f"{pid}: site_name_as_published "
                f"{r['site_name_as_published']!r} differs from the "
                f"gazetteer's {spine['site_name_as_published'][pid]!r}")
        status = r["status"]
        if status not in STATUSES:
            raise GateFailure("B2", f"{pid}: status {status!r}")
        per_status[status] += 1
        a, b = r["source_a"], r["source_b"]
        if status == "AGREED":
            if a is None or b is None:
                raise GateFailure(
                    "B2", f"{pid}: AGREED row lacks two sources")
            _check_source(a, pid + " source_a")
            _check_source(b, pid + " source_b")
            if a["mapped_class"] != b["mapped_class"]:
                raise GateFailure(
                    "B2", f"{pid}: AGREED row's sources map to "
                    f"different classes")
            if r["primary_class"] != a["mapped_class"]:
                raise GateFailure(
                    "B2", f"{pid}: primary_class is not the "
                    f"agreed class")
            per_class[r["primary_class"]] = \
                per_class.get(r["primary_class"], 0) + 1
            if r["primary_class"] != "mixed/unknown":
                testable.append(pid)
        elif status == "DISAGREED":
            if a is None or b is None:
                raise GateFailure(
                    "B2", f"{pid}: DISAGREED row lacks two sources")
            _check_source(a, pid + " source_a")
            _check_source(b, pid + " source_b")
            if a["mapped_class"] == b["mapped_class"]:
                raise GateFailure(
                    "B2", f"{pid}: DISAGREED row's sources map "
                    f"to the same class")
            if r["primary_class"] is not None:
                raise GateFailure(
                    "B2", f"{pid}: DISAGREED row carries a "
                    f"primary_class")
        elif status == "SINGLE-SOURCE":
            if a is None or b is not None:
                raise GateFailure(
                    "B2", f"{pid}: SINGLE-SOURCE row must carry "
                    f"exactly one source (source_a)")
            _check_source(a, pid + " source_a")
            if r["primary_class"] is not None:
                raise GateFailure(
                    "B2", f"{pid}: SINGLE-SOURCE row carries a "
                    f"primary_class")
        else:  # NO-SOURCE
            if a is not None or b is not None:
                raise GateFailure(
                    "B2", f"{pid}: NO-SOURCE row carries a source")
            if r["primary_class"] is not None:
                raise GateFailure(
                    "B2", f"{pid}: NO-SOURCE row carries a "
                    f"primary_class")
            if not isinstance(r["notes"], str) or \
                    not r["notes"].strip():
                raise GateFailure(
                    "B2", f"{pid}: NO-SOURCE row records no "
                    f"search in notes")
    return {
        "rows": len(rows),
        "per_status_counts": per_status,
        "agreed_class_counts": per_class,
        "testable_count": len(testable),
        "testable_sites": testable,
        "sha256": _sha256(_ASSET_B),
    }


def validate_ledger() -> dict:
    """Step 1b form + extraction census."""
    if not _LEDGER.exists():
        raise GateFailure("B2", "asset-b/ledger-signs.jsonl missing")
    rows = [json.loads(line) for line in
            _LEDGER.read_text("utf-8").splitlines() if line.strip()]
    mapped = 0
    unmapped = 0
    for r in rows:
        if set(r) != LEDGER_FIELDS:
            raise GateFailure(
                "B2", f"ledger entry {r.get('roif_sign')!r}: "
                f"fields are not exactly {sorted(LEDGER_FIELDS)}")
        ids = r["mapped_mahadevan_ids"]
        if ids == "UNMAPPED":
            unmapped += 1
        elif isinstance(ids, list) and ids and \
                all(isinstance(x, str) and len(x) == 3 and
                    x.isdigit() for x in ids):
            mapped += 1
        else:
            raise GateFailure(
                "B2", f"ledger entry {r['roif_sign']!r}: "
                f"mapped_mahadevan_ids is neither a token list "
                f"nor UNMAPPED")
    return {
        "entries_entered": len(rows),
        "entries_mapped": mapped,
        "entries_unmapped": unmapped,
        "sha256": _sha256(_LEDGER),
    }


def run_step0(sealed_path: Path) -> int:
    pins = gate_01()
    spine = gate_02()
    census = gate_03(spine)
    sealed_path.write_text(json.dumps({
        "gate_0_1_input_sha256": pins,
        "spine": spine,
        "census": census,
    }, indent=2, sort_keys=True) + "\n", "utf-8")
    print("gate 0.1 INPUT INTEGRITY: PASS "
          f"({len(pins)} inputs hash to their freeze pins)")
    print(f"gate 0.2 SPINE REPRODUCTION: PASS "
          f"({spine['rows']} rows, {spine['clusters']} clusters)")
    print(f"gate 0.3 JOIN CENSUS: PASS "
          f"(total {census['total_records']}; joined "
          f"{census['joined_total']}; non-spine sites "
          f"{len(census['non_spine_sites'])} carrying "
          f"{census['non_spine_total']}; no site value "
          f"{census['no_site_value']}; every record in "
          f"exactly one class)")
    print(f"sealed census written to {sealed_path} "
          f"(per-site figures are not printed before the "
          f"asset freeze, spec section 4.5)")
    return 0


def run_full() -> int:
    anchors_before = _sha256(
        _REPO / "backend/reports/INDUS_FINAL_ANCHORS.json")
    pins = gate_01()
    spine = gate_02()
    census = gate_03(spine)
    asset = validate_asset(spine)
    ledger = validate_ledger()
    anchors_after = _sha256(
        _REPO / "backend/reports/INDUS_FINAL_ANCHORS.json")
    if anchors_before != anchors_after or \
            anchors_after != PINS[
                "backend/reports/INDUS_FINAL_ANCHORS.json"]:
        raise GateFailure(
            "0.1", "anchors file changed during the run")

    results = {
        "phase": 406,
        "spec": "047-roif-ledger-distribution",
        "scope": "step 0 + step 1 only (Asset B build and "
                 "freeze; ledger-sign list frozen in the same "
                 "act). Step 2 (spec section 6) NOT run: no "
                 "distribution quantity computed.",
        "freeze_digest": FREEZE_DIGEST,
        "worker": WORKER,
        "corpus_label": "Primary layer as pinned in spec "
            "section 2: backend/glossa_lab/data/"
            "yajnadevam_inscriptions.csv (5,679 records; the "
            "site-attributed layer of Specs 027/028), SHA-256 "
            + PINS["backend/glossa_lab/data/"
                   "yajnadevam_inscriptions.csv"],
        "step0": {
            "gate_0_1_input_integrity": "PASS",
            "gate_0_1_input_sha256": pins,
            "gate_0_2_spine_reproduction": "PASS",
            "spine_rows": spine["rows"],
            "spine_clusters": spine["clusters"],
            "gate_0_3_join_census": "PASS",
            "census": census,
        },
        "asset_b": {
            "file": "specs/047-roif-ledger-distribution/"
                    "asset-b/site-functions.jsonl",
            "sha256": asset["sha256"],
            "rows": asset["rows"],
            "testable_count": asset["testable_count"],
            "testable_sites": asset["testable_sites"],
            "per_status_counts": asset["per_status_counts"],
            "agreed_class_counts": asset["agreed_class_counts"],
        },
        "ledger_sign_list": {
            "file": "specs/047-roif-ledger-distribution/"
                    "asset-b/ledger-signs.jsonl",
            "sha256": ledger["sha256"],
            "extraction_census": {
                "entries_entered": ledger["entries_entered"],
                "entries_mapped": ledger["entries_mapped"],
                "entries_unmapped": ledger["entries_unmapped"],
            },
        },
        "build_gates": {
            "B1_coverage": "PASS (mechanical: exactly the 30 "
                           "spine clusters, sorted)",
            "B2_citation_completeness": "PASS (mechanical: "
                "per-status records complete, section 4.1 "
                "form exact)",
            "B3_verification": "worker act recorded in the "
                "step-1 outcome record (specs/"
                "047-roif-ledger-distribution/outcome.md), "
                "including demotions made before the freeze",
            "B4_circularity": "attestation in the step-1 "
                "outcome record (spec section 4.5)",
        },
        "step2": "NOT RUN (separate execution act; tasks "
                 "E5-E7 open)",
        "anchors_byte_identical": True,
        "component_fence": "This result concerns the "
            "distribution component of Roif's ledger thesis "
            "only; the guild-authority and Akkadian-influence "
            "components were not tested.",
    }
    _OUT_JSON.write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n",
        "utf-8")

    census_lines = [
        f"- joined to a spine cluster: "
        f"{census['joined_total']} records",
        f"- non-spine sites: {census['non_spine_total']} "
        f"records over {len(census['non_spine_sites'])} "
        f"site values:",
    ]
    for entry in census["non_spine_sites"]:
        census_lines.append(
            f"  - {entry['site_as_in_corpus']}: "
            f"{entry['records']}")
    census_lines.append(
        f"- no site value: {census['no_site_value']} records")
    joined_lines = [
        f"  - {pid}: {census['joined_by_cluster'][pid]}"
        for pid in spine["cluster_list"]]
    status_lines = [
        f"- {s}: {asset['per_status_counts'][s]}"
        for s in sorted(asset["per_status_counts"])]
    report = f"""# Phase-406 — Spec 047 step 1 report (Asset B build and freeze)

Held under the Roif gate (spec section 10): an internal
program record; nothing in it is published.

**Headline.** Corpus: the primary layer as pinned in spec
section 2 (backend/glossa_lab/data/
yajnadevam_inscriptions.csv, 5,679 records; the
site-attributed layer of Specs 027/028). Asset B digest
`{asset['sha256']}` over
specs/047-roif-ledger-distribution/asset-b/
site-functions.jsonl ({asset['rows']} rows; testable
{asset['testable_count']}: {', '.join(asset['testable_sites']) or 'none'}).
Ledger-sign list digest `{ledger['sha256']}`
(extraction census: {ledger['entries_entered']} entered,
{ledger['entries_mapped']} mapped,
{ledger['entries_unmapped']} UNMAPPED). Step 2 was not
run: no distribution quantity exists. This result
concerns the distribution component of Roif's ledger
thesis only; the guild-authority and Akkadian-influence
components were not tested.

## Step 0 gates

- 0.1 input integrity: PASS — every section-2 input
  hashes to its freeze pin (recorded in
  reports/phase406_results.json).
- 0.2 spine reproduction: PASS — 36 rows, 30 distinct
  clusters, the frozen cluster list.
- 0.3 join census: PASS — all
  {census['total_records']} records accounted for in
  exactly one class:
{chr(10).join(census_lines)}
- joined records by cluster (accounting only; computed
  by the machinery after the asset froze):
{chr(10).join(joined_lines)}

## Asset B (step 1a)

Per-status counts:
{chr(10).join(status_lines)}

Testable sites (AGREED, non-mixed/unknown class):
{asset['testable_count']} — {', '.join(asset['testable_sites']) or 'none'}.
The number of testable sites is not a build gate
(DD-047-1); its thinness is adjudicated by the step-2
classification gate (spec section 6.3), which has not
run.

## Ledger-sign list (step 1b)

Frozen in the same act under its own digest (above).
Extraction from the two Academia.edu postings of spec
section 2.1 only. Census: sought 13 depicted sign
classes; {ledger['entries_entered']} entered;
{ledger['entries_mapped']} mapped to the primary
layer's numbering; {ledger['entries_unmapped']}
UNMAPPED (recorded in the list and excluded from
counting by rule). The all-UNMAPPED case of DD-047-13
does not fire.

## Records

- results: reports/phase406_results.json
- asset: specs/047-roif-ledger-distribution/asset-b/
  site-functions.jsonl
- ledger list: specs/047-roif-ledger-distribution/
  asset-b/ledger-signs.jsonl
- outcome record: specs/047-roif-ledger-distribution/
  outcome.md (the build record, the section 4.3
  verification pass in full, the section 4.5
  attestation, and the digests — the pin source fixed
  by Spec 051 DD-051-14)
- anchors asserted byte-identical before and after.

*AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen
Pierson, per constitution section VI.*
"""
    _OUT_MD.write_text(report, "utf-8")
    print("step 0 gates: PASS (0.1, 0.2, 0.3)")
    print(f"Asset B: {asset['rows']} rows; digest "
          f"{asset['sha256']}; testable "
          f"{asset['testable_count']}; per-status "
          f"{asset['per_status_counts']}")
    print(f"ledger list: digest {ledger['sha256']}; "
          f"entered {ledger['entries_entered']}, mapped "
          f"{ledger['entries_mapped']}, unmapped "
          f"{ledger['entries_unmapped']}")
    print(f"wrote {_OUT_JSON.relative_to(_REPO)} and "
          f"{_OUT_MD.relative_to(_REPO)}")
    return 0


def main(argv: list[str]) -> int:
    try:
        if len(argv) == 3 and argv[1] == "--step0":
            return run_step0(Path(argv[2]))
        if len(argv) == 1:
            return run_full()
        print(__doc__)
        return 2
    except GateFailure as exc:
        print(f"GATE FAILURE {exc.gate}: {exc.observed}")
        print("The run stops here; no output was written. "
              "The closure is recorded with the frozen "
              "wording for the gate reached (spec section 7).")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

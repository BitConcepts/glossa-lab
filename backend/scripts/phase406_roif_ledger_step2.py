#!/usr/bin/env python3
"""Phase-406 — Spec 047 step 2 (the distribution test, E5–E6).

Executes step 2 of the frozen Spec 047 contract
(specs/047-roif-ledger-distribution/freeze.md, freeze digest
8501feabb7beee621e99ae48529e5a74c0788fb0619ac49c615912e13914cdc7)
against Asset B as frozen at step 1 (step-1 outcome record,
specs/047-roif-ledger-distribution/outcome.md):

  Asset B  specs/047-roif-ledger-distribution/asset-b/
           site-functions.jsonl
           SHA-256 a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85
           (30 rows; AGREED 3, DISAGREED 1, SINGLE-SOURCE 10,
           NO-SOURCE 16; testable 2)
  Ledger   specs/047-roif-ledger-distribution/asset-b/
           ledger-signs.jsonl
           SHA-256 dfa48f50907a3374b45d6270f0ffbed8a2492c5d33c186da36950140b233292b
           (8 entered, 3 mapped, 5 UNMAPPED)

Order of the act (fail-closed):

  Step 0 re-run (spec section 3): 0.1 every section-2 input
  hashes to its freeze pin; 0.2 the gazetteer spine
  reproduces exactly (36 rows, 30 clusters); 0.3 the corpus
  join census accounts for every one of the 5,679
  primary-layer records in exactly one class, under the
  section 6.1 normalisation. A failure stops the run as
  INVALID before any step-2 act.

  Asset pin re-assertion: Asset B and the ledger-sign list
  hash to the digests recorded in the step-1 outcome record.
  A mismatch stops the run as INVALID (spec section 4.6:
  dependents re-assert the digest; the asset is never
  quietly edited and re-digested).

  E5 — the classification gate (spec section 6.3), checked
  before any distribution quantity exists: the test does
  not run if fewer than 12 sites are testable, or if either
  the pooled ADMIN-TRADE-GATEWAY class or the domestic /
  ritual contrast class is empty in the test population
  (spec section 6.1: testable sites carrying at least one
  joined inscription; testable sites with none are listed
  NO-CORPUS-COVERAGE). A fired gate ends the execution as
  INCONCLUSIVE — the classification is the finding — with
  the section 7 pre-written wording, the exclusions
  republished in full (spec section 6.4), and no
  distribution quantity computed.

  E6 — the primary measures and sensitivities (spec
  sections 6.2, 6.4), carried below in the frozen form
  (shares ratios R and R_ledger; the 9,999-shuffle
  permutation test at the freeze-recorded seed 20261021;
  the mechanical section 6.3 partition; each-source-alone
  and five-largest recomputations). They run only if the
  classification gate does not fire.

Outputs (full run):
  reports/phase406_step2_results.json
  reports/phase406_step2_report.md

The claim append of task E7 (the dated, component-scoped
entry on the claim's record) is prescribed in the results
under "claim_append" and performed by the executor, never
by this script, so re-running the script never appends
twice (the Spec 056 form). The anchors file is asserted
byte-identical before and after (its section-2 pin). All
products are held under the Roif gate (spec section 10).

AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution section VI.
"""
from __future__ import annotations

import csv
import hashlib
import json
import random
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SPEC = _REPO / "specs/047-roif-ledger-distribution"
_ASSET_B = _SPEC / "asset-b/site-functions.jsonl"
_LEDGER = _SPEC / "asset-b/ledger-signs.jsonl"
_OUT_JSON = _REPO / "reports/phase406_step2_results.json"
_OUT_MD = _REPO / "reports/phase406_step2_report.md"

FREEZE_DIGEST = (
    "8501feabb7beee621e99ae48529e5a74c0788fb0619ac49c615912e13914cdc7")
WORKER = "Muse Spark via Muse (AI agent)"
EXECUTION_DATE = "2026-10-21"
CLAIM_ID = ("indus_valley_script_deciphered_from_myth_"
            "65ff0a26_manual_001")
ASSET_B_SHA256 = (
    "a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85")
LEDGER_SHA256 = (
    "dfa48f50907a3374b45d6270f0ffbed8a2492c5d33c186da36950140b233292b")
TESTABLE_FLOOR = 12
PERMUTATION_SHUFFLES = 9999
PERMUTATION_SEED = 20261021

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
POOLED = {"gateway/border", "administrative", "port/trade"}
CONTRAST = {"domestic", "ritual"}

COMPONENT_FENCE = (
    "This result concerns the distribution component of "
    "Roif's ledger thesis only; the guild-authority and "
    "Akkadian-influence components were not tested.")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _normalise(name: str) -> str:
    """Spec section 6.1: lowercase, whitespace and punctuation
    collapsed. No fuzzy matching."""
    lowered = name.lower()
    spaced = re.sub(r"[^\w\s]", " ", lowered, flags=re.UNICODE)
    return " ".join(spaced.split())


def _grouping(cls: str | None) -> str | None:
    if cls in POOLED:
        return "ADMIN-TRADE-GATEWAY"
    if cls in CONTRAST:
        return "CONTRAST (domestic/ritual)"
    return None


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
            raise GateFailure("0.1", f"input missing: {rel}")
        digest = _sha256(path)
        observed[rel] = digest
        if digest != pin:
            raise GateFailure(
                "0.1", f"{rel} hashes to {digest}, pin is {pin}")
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
            "asset-form", f"{where}: source fields are not "
            f"exactly {sorted(SOURCE_FIELDS)}")
    for field in SOURCE_FIELDS:
        if not isinstance(src[field], str) or not src[field].strip():
            raise GateFailure(
                "asset-form", f"{where}: source field {field} "
                f"is empty")
    if src["mapped_class"] not in CLASSES:
        raise GateFailure(
            "asset-form", f"{where}: mapped_class "
            f"{src['mapped_class']!r} is outside the section "
            f"4.2 vocabulary")


def validate_asset(spine: dict) -> dict:
    """Asset B: digest pin first, then the section 4.1 form
    and the section 4.3/4.4 status mechanics, re-derived
    from the committed bytes (the step-1 mechanical gates
    B1/B2 in their step-2 re-assertion form)."""
    if not _ASSET_B.exists():
        raise GateFailure("asset-pin", "asset-b/site-functions.jsonl missing")
    digest = _sha256(_ASSET_B)
    if digest != ASSET_B_SHA256:
        raise GateFailure(
            "asset-pin", f"Asset B hashes to {digest}; the "
            f"step-1 outcome record pins {ASSET_B_SHA256}. "
            f"Under section 4.6 the run stops as INVALID; "
            f"the asset is never re-digested at run time.")
    rows = [json.loads(line) for line in
            _ASSET_B.read_text("utf-8").splitlines() if line.strip()]
    ids = [r.get("program_site_id") for r in rows]
    if ids != CLUSTERS:
        raise GateFailure(
            "asset-form", f"asset rows are not exactly the 30 "
            f"spine clusters in sorted order: {ids}")
    per_status = {s: 0 for s in sorted(STATUSES)}
    per_class: dict[str, int] = {}
    testable = []
    by_status: dict[str, list[str]] = {s: [] for s in STATUSES}
    agreed_mixed = []
    for r in rows:
        pid = r["program_site_id"]
        if set(r) != ROW_FIELDS:
            raise GateFailure(
                "asset-form", f"{pid}: row fields are not "
                f"exactly {sorted(ROW_FIELDS)}")
        if r["site_name_as_published"] != \
                spine["site_name_as_published"][pid]:
            raise GateFailure(
                "asset-form", f"{pid}: site_name_as_published "
                f"differs from the gazetteer's")
        status = r["status"]
        if status not in STATUSES:
            raise GateFailure("asset-form", f"{pid}: status {status!r}")
        per_status[status] += 1
        by_status[status].append(pid)
        a, b = r["source_a"], r["source_b"]
        if status == "AGREED":
            if a is None or b is None:
                raise GateFailure(
                    "asset-form", f"{pid}: AGREED row lacks two sources")
            _check_source(a, pid + " source_a")
            _check_source(b, pid + " source_b")
            if a["mapped_class"] != b["mapped_class"]:
                raise GateFailure(
                    "asset-form", f"{pid}: AGREED row's sources "
                    f"map to different classes")
            if r["primary_class"] != a["mapped_class"]:
                raise GateFailure(
                    "asset-form", f"{pid}: primary_class is not "
                    f"the agreed class")
            per_class[r["primary_class"]] = \
                per_class.get(r["primary_class"], 0) + 1
            if r["primary_class"] != "mixed/unknown":
                testable.append({
                    "program_site_id": pid,
                    "primary_class": r["primary_class"],
                    "grouping": _grouping(r["primary_class"]),
                })
            else:
                agreed_mixed.append(pid)
        elif status == "DISAGREED":
            if a is None or b is None:
                raise GateFailure(
                    "asset-form", f"{pid}: DISAGREED row lacks "
                    f"two sources")
            _check_source(a, pid + " source_a")
            _check_source(b, pid + " source_b")
            if a["mapped_class"] == b["mapped_class"]:
                raise GateFailure(
                    "asset-form", f"{pid}: DISAGREED row's "
                    f"sources map to the same class")
            if r["primary_class"] is not None:
                raise GateFailure(
                    "asset-form", f"{pid}: DISAGREED row "
                    f"carries a primary_class")
        elif status == "SINGLE-SOURCE":
            if a is None or b is not None:
                raise GateFailure(
                    "asset-form", f"{pid}: SINGLE-SOURCE row "
                    f"must carry exactly one source (source_a)")
            _check_source(a, pid + " source_a")
            if r["primary_class"] is not None:
                raise GateFailure(
                    "asset-form", f"{pid}: SINGLE-SOURCE row "
                    f"carries a primary_class")
        else:  # NO-SOURCE
            if a is not None or b is not None:
                raise GateFailure(
                    "asset-form", f"{pid}: NO-SOURCE row "
                    f"carries a source")
            if r["primary_class"] is not None:
                raise GateFailure(
                    "asset-form", f"{pid}: NO-SOURCE row "
                    f"carries a primary_class")
            if not isinstance(r["notes"], str) or \
                    not r["notes"].strip():
                raise GateFailure(
                    "asset-form", f"{pid}: NO-SOURCE row "
                    f"records no search in notes")
    return {
        "rows": rows,
        "sha256": digest,
        "row_count": len(rows),
        "per_status_counts": per_status,
        "agreed_class_counts": per_class,
        "testable_count": len(testable),
        "testable_sites": testable,
        "by_status": by_status,
        "agreed_mixed_unknown": agreed_mixed,
    }


def validate_ledger() -> dict:
    """Ledger-sign list: digest pin, entry form, extraction
    census, and the mapped-token sets measure (b) would use."""
    if not _LEDGER.exists():
        raise GateFailure("ledger-pin", "asset-b/ledger-signs.jsonl missing")
    digest = _sha256(_LEDGER)
    if digest != LEDGER_SHA256:
        raise GateFailure(
            "ledger-pin", f"ledger-sign list hashes to "
            f"{digest}; the step-1 outcome record pins "
            f"{LEDGER_SHA256}")
    rows = [json.loads(line) for line in
            _LEDGER.read_text("utf-8").splitlines() if line.strip()]
    mapped = []
    unmapped = []
    for r in rows:
        if set(r) != LEDGER_FIELDS:
            raise GateFailure(
                "ledger-form", f"ledger entry {r.get('roif_sign')!r}: "
                f"fields are not exactly {sorted(LEDGER_FIELDS)}")
        ids = r["mapped_mahadevan_ids"]
        if ids == "UNMAPPED":
            unmapped.append(r["roif_sign"])
        elif isinstance(ids, list) and ids and \
                all(isinstance(x, str) and len(x) == 3 and
                    x.isdigit() for x in ids):
            mapped.append({
                "roif_sign": r["roif_sign"],
                "assigned_function": r["assigned_function"],
                "mapped_mahadevan_ids": ids,
            })
        else:
            raise GateFailure(
                "ledger-form", f"ledger entry {r['roif_sign']!r}: "
                f"mapped_mahadevan_ids is neither a token list "
                f"nor UNMAPPED")
    return {
        "sha256": digest,
        "entries_entered": len(rows),
        "entries_mapped": len(mapped),
        "entries_unmapped": len(unmapped),
        "mapped_entries": mapped,
        "unmapped_signs": unmapped,
    }


# ── E6 machinery (spec sections 6.2/6.4), in the frozen form.
# ── None of it runs when the classification gate fires.

def _ledger_occurrences(population_ids: set, token_to_sign: dict):
    """Per-site ledger-sign occurrence counts over the primary
    layer's `text` token sequences, for the given sites."""
    path = _REPO / "backend/glossa_lab/data/yajnadevam_inscriptions.csv"
    per_site: dict[str, int] = {pid: 0 for pid in population_ids}
    per_sign: dict[str, dict[str, int]] = {}
    norm_to_cluster = {_normalise(c): c for c in CLUSTERS}
    with path.open("r", encoding="utf-8", newline="") as fh:
        for rec in csv.DictReader(fh):
            site = rec.get("site")
            if site is None:
                continue
            pid = norm_to_cluster.get(_normalise(site))
            if pid is None or pid not in population_ids:
                continue
            text = (rec.get("text") or "").strip().strip("+")
            for tok in text.split("-"):
                tok = tok.strip()
                sign = token_to_sign.get(tok)
                if sign is not None:
                    per_site[pid] += 1
                    per_sign.setdefault(sign, {}).setdefault(pid, 0)
                    per_sign[sign][pid] += 1
    return per_site, per_sign


def _ratio(pooled_sum: float, total_sum: float,
           pooled_sites: int, total_sites: int):
    if total_sum == 0 or total_sites == 0:
        return None
    return (pooled_sum / total_sum) / (pooled_sites / total_sites)


def compute_primary(population: list, ledger: dict) -> dict:
    """Sections 6.2/6.3/6.4, mechanically. `population` entries
    carry program_site_id, grouping, joined_records."""
    ids = [p["program_site_id"] for p in population]
    counts = {p["program_site_id"]: p["joined_records"]
              for p in population}
    pooled_ids = [p["program_site_id"] for p in population
                  if p["grouping"] == "ADMIN-TRADE-GATEWAY"]
    total_inscr = sum(counts.values())
    r_obs = _ratio(sum(counts[i] for i in pooled_ids), total_inscr,
                   len(pooled_ids), len(ids))
    # Ledger occurrences.
    token_to_sign = {}
    for entry in ledger["mapped_entries"]:
        for tok in entry["mapped_mahadevan_ids"]:
            token_to_sign[tok] = entry["roif_sign"]
    occ, per_sign = _ledger_occurrences(set(ids), token_to_sign)
    total_occ = sum(occ.values())
    r_led = None
    if ledger["entries_mapped"] > 0:
        r_led = _ratio(sum(occ[i] for i in pooled_ids), total_occ,
                       len(pooled_ids), len(ids))
    # Permutation test: labels shuffled across sites, 9,999
    # shuffles, seed fixed at the freeze (DD-047-10).
    labels = [p["grouping"] for p in population]
    rng = random.Random(PERMUTATION_SEED)
    ge = 0
    for _ in range(PERMUTATION_SHUFFLES):
        shuffled = labels[:]
        rng.shuffle(shuffled)
        sp = sum(counts[pid] for pid, lab in zip(ids, shuffled)
                 if lab == "ADMIN-TRADE-GATEWAY")
        r_shuf = _ratio(sp, total_inscr, len(pooled_ids), len(ids))
        if r_shuf is not None and r_obs is not None and \
                r_shuf >= r_obs:
            ge += 1
    p_val = ge / PERMUTATION_SHUFFLES
    # The mechanical partition (spec section 6.3).
    if ledger["entries_mapped"] == 0:
        # DD-047-13: the ledger clause is vacated for this run.
        if r_obs is not None and r_obs >= 1.5 and p_val < 0.05:
            verdict = "SUPPORTED"
        elif r_obs is not None and (r_obs <= 1.0 or p_val >= 0.05):
            verdict = "NOT SUPPORTED"
        else:
            verdict = "INCONCLUSIVE"
    else:
        if r_obs is not None and r_obs >= 1.5 and p_val < 0.05 \
                and r_led is not None and r_led > 1.0:
            verdict = "SUPPORTED"
        elif (r_obs is not None and r_obs <= 1.0) or \
                (p_val >= 0.05 and r_obs is not None and r_obs > 1.0):
            verdict = "NOT SUPPORTED"
        else:
            verdict = "INCONCLUSIVE"
    per_sign_report = []
    for entry in ledger["mapped_entries"]:
        sign = entry["roif_sign"]
        by_site = per_sign.get(sign, {})
        per_sign_report.append({
            "roif_sign": sign,
            "occurrences_total": sum(by_site.values()),
            "occurrences_pooled": sum(
                by_site.get(i, 0) for i in pooled_ids),
            "occurrences_by_site": by_site,
        })
    return {
        "R": r_obs,
        "permutation": {
            "shuffles": PERMUTATION_SHUFFLES,
            "seed": PERMUTATION_SEED,
            "shuffles_at_or_above_R": ge,
            "p_value": p_val,
        },
        "R_ledger": r_led,
        "per_sign_ledger_counts": per_sign_report,
        "verdict_by_partition": verdict,
    }


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

    # Section 6.1 test population: testable sites carrying at
    # least one joined inscription. Testable sites with none
    # are NO-CORPUS-COVERAGE and enter neither share.
    population = []
    no_coverage = []
    for t in asset["testable_sites"]:
        joined = census["joined_by_cluster"][t["program_site_id"]]
        entry = {**t, "joined_records": joined}
        if joined >= 1:
            population.append(entry)
        else:
            no_coverage.append(t["program_site_id"])
    pooled_pop = [p for p in population
                  if p["grouping"] == "ADMIN-TRADE-GATEWAY"]
    contrast_pop = [p for p in population
                    if p["grouping"] == "CONTRAST (domestic/ritual)"]

    # E5 — the classification gate (spec section 6.3), before
    # any distribution quantity exists.
    floor_pass = asset["testable_count"] >= TESTABLE_FLOOR
    gate_fires = (not floor_pass) or not pooled_pop or not contrast_pop

    exclusions = {
        "DISAGREED": asset["by_status"]["DISAGREED"],
        "SINGLE-SOURCE": asset["by_status"]["SINGLE-SOURCE"],
        "NO-SOURCE": asset["by_status"]["NO-SOURCE"],
        "AGREED_mixed_unknown": asset["agreed_mixed_unknown"],
        "NO-CORPUS-COVERAGE": no_coverage,
    }

    status_counts_text = (
        f"AGREED {asset['per_status_counts']['AGREED']} "
        f"(of which 1, shahr i sokhta, agreed at mixed/unknown "
        f"and excluded by section 4.2), DISAGREED "
        f"{asset['per_status_counts']['DISAGREED']}, "
        f"SINGLE-SOURCE {asset['per_status_counts']['SINGLE-SOURCE']}, "
        f"NO-SOURCE {asset['per_status_counts']['NO-SOURCE']}")
    wording = (
        "The distribution test did not run: "
        f"{asset['testable_count']} of the gazetteer's 30 sites "
        "survived the two-source agreement rule as testable "
        "(floor 12), and one side of the comparison is empty "
        "in the test population (the pooled "
        "ADMIN-TRADE-GATEWAY side carries both testable "
        "sites; the domestic/ritual contrast side carries "
        "none). The finding of this execution is the "
        "classification itself (Asset B, digest "
        f"{ASSET_B_SHA256}): {status_counts_text}, with the "
        "disagreed and unclassifiable sites named in full. "
        "No distribution quantity was computed. The claim "
        "stands UNTESTED for its distribution component, "
        "now with the reason measured rather than asserted.")

    results = {
        "phase": 406,
        "spec": "047-roif-ledger-distribution",
        "scope": "step 2 only (tasks E5-E7): step 0 re-run, "
                 "Asset B pin re-assertion against the step-1 "
                 "outcome record, the section 6.3 "
                 "classification gate (E5), and — only if the "
                 "gate does not fire — the section 6.2 "
                 "primaries and section 6.4 sensitivities "
                 "(E6). Step 1 (Asset B build and freeze; the "
                 "ledger-sign list) is the step-1 act, "
                 "recorded in reports/phase406_results.json.",
        "freeze_digest": FREEZE_DIGEST,
        "worker": WORKER,
        "execution_date": EXECUTION_DATE,
        "claim_under_test": CLAIM_ID,
        "outcome": "INCONCLUSIVE" if gate_fires else None,
        "outcome_kind": ("classification gate (spec section "
                          "6.3)" if gate_fires else None),
        "headline": ("INCONCLUSIVE (classification)"
                     if gate_fires else None),
        "stop_gate": "6.3 classification gate" if gate_fires else None,
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
            "sha256_pin_step1_record": ASSET_B_SHA256,
            "pin_match": asset["sha256"] == ASSET_B_SHA256,
            "rows": asset["row_count"],
            "testable_count": asset["testable_count"],
            "testable_sites": asset["testable_sites"],
            "per_status_counts": asset["per_status_counts"],
            "agreed_class_counts": asset["agreed_class_counts"],
        },
        "ledger_sign_list": {
            "file": "specs/047-roif-ledger-distribution/"
                    "asset-b/ledger-signs.jsonl",
            "sha256": ledger["sha256"],
            "sha256_pin_step1_record": LEDGER_SHA256,
            "pin_match": ledger["sha256"] == LEDGER_SHA256,
            "extraction_census": {
                "entries_entered": ledger["entries_entered"],
                "entries_mapped": ledger["entries_mapped"],
                "entries_unmapped": ledger["entries_unmapped"],
            },
            "all_unmapped_case_dd_047_13_fires":
                ledger["entries_mapped"] == 0,
        },
        "classification_gate": {
            "rule": "spec section 6.3: the test does not run "
                    "if fewer than 12 sites are testable, or "
                    "if either the pooled class or the "
                    "contrast class is empty in the test "
                    "population",
            "testable_floor": TESTABLE_FLOOR,
            "testable_count": asset["testable_count"],
            "testable_floor_pass": floor_pass,
            "test_population": population,
            "pooled_sites_in_test_population": len(pooled_pop),
            "contrast_sites_in_test_population": len(contrast_pop),
            "pooled_nonempty": bool(pooled_pop),
            "contrast_nonempty": bool(contrast_pop),
            "gate_fires": gate_fires,
        },
        "distribution_quantities": None,
        "permutation": None,
        "sensitivities": {
            "each_source_alone": None,
            "five_largest_sites": None,
            "not_run_reason": (
                "the classification gate fired at E5; the "
                "section 6.4 recomputations presuppose a "
                "primary test that did not run" if gate_fires
                else None),
            "exclusions_restated": exclusions,
        },
        "wording": wording if gate_fires else None,
        "claim_append": {
            "key": "spec047_step2",
            "claim_id": CLAIM_ID,
            "spec": "047",
            "phase": "Phase-406",
            "date": EXECUTION_DATE,
            "kind": "step-2 outcome (classification gate)",
            "outcome": ("INCONCLUSIVE (classification gate, "
                        "spec section 6.3)" if gate_fires else None),
            "wording": wording if gate_fires else None,
            "record": "specs/047-roif-ledger-distribution/outcome.md",
            "results": "reports/phase406_step2_results.json",
            "posture": (
                "The append itself is an executor act on the "
                "claim's record (task E7), performed by the "
                "executor with the results digest added at "
                "the act — removing the appended entry "
                "reproduces the pre-act file byte-identically "
                "— and it is prescribed here, not performed "
                "by this script, so re-running the script "
                "never appends twice. The claim's status and "
                "stage are unchanged: the claim stands "
                "UNTESTED for its distribution component."),
        },
        "anchors_byte_identical": True,
        "component_fence": COMPONENT_FENCE,
    }

    if not gate_fires:
        primary = compute_primary(population, ledger)
        results["distribution_quantities"] = primary
        results["permutation"] = primary["permutation"]
        results["outcome"] = primary["verdict_by_partition"]
        results["outcome_kind"] = "measures (spec section 6.3)"
        results["headline"] = primary["verdict_by_partition"]
        results["stop_gate"] = None

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
    status_lines = [
        f"- {s}: {asset['per_status_counts'][s]}"
        for s in sorted(asset["per_status_counts"])]
    testable_lines = [
        f"  - {t['program_site_id']}: {t['primary_class']} "
        f"({t['grouping']})"
        for t in asset["testable_sites"]]
    excl_lines = []
    for name in ("DISAGREED", "SINGLE-SOURCE", "NO-SOURCE",
                 "AGREED_mixed_unknown", "NO-CORPUS-COVERAGE"):
        vals = exclusions[name]
        excl_lines.append(
            f"- {name}: {len(vals)} — "
            f"{', '.join(vals) if vals else 'none'}")
    report = f"""# Phase-406 — Spec 047 step 2 report (the distribution test)

Held under the Roif gate (spec section 10): an internal
program record; nothing in it is published.

**Headline.** Corpus: the primary layer as pinned in spec
section 2 (backend/glossa_lab/data/
yajnadevam_inscriptions.csv, 5,679 records; the
site-attributed layer of Specs 027/028). Asset B digest
`{asset['sha256']}` over
specs/047-roif-ledger-distribution/asset-b/
site-functions.jsonl ({asset['row_count']} rows; testable
{asset['testable_count']}). Ledger-sign list digest
`{ledger['sha256']}` (extraction census:
{ledger['entries_entered']} entered,
{ledger['entries_mapped']} mapped,
{ledger['entries_unmapped']} UNMAPPED). Headline outcome:
**INCONCLUSIVE (classification)** — the section 6.3
classification gate fired at E5, the distribution test
did not run, and no distribution quantity was computed
(no R, no permutation p-value, no R_ledger exists).
{COMPONENT_FENCE}

## The section 7 wording (INCONCLUSIVE, classification)

"{wording}"

## Step 0 gates (re-run at step 2)

- 0.1 input integrity: PASS — every section-2 input
  hashes to its freeze pin (recorded in
  reports/phase406_step2_results.json).
- 0.2 spine reproduction: PASS — 36 rows, 30 distinct
  clusters, the frozen cluster list.
- 0.3 join census: PASS — all
  {census['total_records']} records accounted for in
  exactly one class (identical to the step-1 census):
{chr(10).join(census_lines)}

## Asset B pin re-assertion

Asset B hashes to the digest recorded in the step-1
outcome record (`{ASSET_B_SHA256}`), and the ledger-sign
list to its step-1 digest (`{LEDGER_SHA256}`). The
asset's section 4.1 form and status mechanics were
re-validated from the committed bytes. Per-status
counts:
{chr(10).join(status_lines)}

Testable sites (AGREED, non-mixed/unknown class):
{asset['testable_count']} —
{chr(10).join(testable_lines) if testable_lines else '  - none'}

## The classification gate (E5, spec section 6.3)

- Testable sites: {asset['testable_count']} — the frozen
  floor is {TESTABLE_FLOOR}. The floor does not pass.
- Test population (section 6.1): the testable sites
  carrying at least one joined inscription —
  harappa (2,717 joined records, administrative, pooled)
  and lothal (208 joined records, port/trade, pooled).
- Pooled ADMIN-TRADE-GATEWAY side in the test
  population: {len(pooled_pop)} sites. Contrast
  (domestic/ritual) side: {len(contrast_pop)} sites —
  empty.
- The gate fires on both of its clauses. The test does
  not run; E6 (the primaries and sensitivities) was not
  run. The each-source-alone and five-largest
  recomputations of section 6.4 presuppose a primary
  test and are recorded not run; the section 6.4
  exclusions are restated in full below.

## Exclusions restated (spec section 6.4)

{chr(10).join(excl_lines)}

## Records

- results: reports/phase406_step2_results.json
- step-1 record: reports/phase406_results.json;
  reports/phase406_step1_report.md
- asset: specs/047-roif-ledger-distribution/asset-b/
  site-functions.jsonl
- ledger list: specs/047-roif-ledger-distribution/
  asset-b/ledger-signs.jsonl
- outcome record: specs/047-roif-ledger-distribution/
  outcome.md (step-2 append)
- anchors asserted byte-identical before and after.

*AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution section VI.*
"""
    if gate_fires:
        _OUT_MD.write_text(report, "utf-8")
    print("step 0 gates: PASS (0.1, 0.2, 0.3)")
    print(f"Asset B pin: {'MATCH' if asset['sha256'] == ASSET_B_SHA256 else 'MISMATCH'} "
          f"({asset['sha256']}); rows {asset['row_count']}; "
          f"testable {asset['testable_count']}; per-status "
          f"{asset['per_status_counts']}")
    print(f"ledger list pin: {'MATCH' if ledger['sha256'] == LEDGER_SHA256 else 'MISMATCH'}; "
          f"entered {ledger['entries_entered']}, mapped "
          f"{ledger['entries_mapped']}, unmapped "
          f"{ledger['entries_unmapped']}")
    if gate_fires:
        print(f"classification gate FIRES: testable "
              f"{asset['testable_count']} < floor {TESTABLE_FLOOR}; "
              f"pooled sites in test population {len(pooled_pop)}; "
              f"contrast sites {len(contrast_pop)}")
        print("OUTCOME: INCONCLUSIVE (classification) — no "
              "distribution quantity computed")
    else:
        print(f"classification gate does not fire; primary "
              f"verdict by partition: "
              f"{results['distribution_quantities']['verdict_by_partition']}")
        print("NOTE: the report renderer of this script "
              "covers the classification-gate form; a "
              "measures outcome requires its own report act.")
    print(f"wrote {_OUT_JSON.relative_to(_REPO)}"
          + (f" and {_OUT_MD.relative_to(_REPO)}"
             if gate_fires else ""))
    return 0


def main(argv: list[str]) -> int:
    try:
        if len(argv) == 1:
            return run_full()
        print(__doc__)
        return 2
    except GateFailure as exc:
        print(f"GATE FAILURE {exc.gate}: {exc.observed}")
        print("The run stops here; no output was written. "
              "A section-2 / asset-pin failure is recorded "
              "with the frozen INVALID wording (spec "
              "section 7).")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

"""Phase-399 (Spec 035) — PRED-2026-010: step 0 of the
frozen scoring contract, run in the frozen order.

Freeze: specs/035-pred-2026-010-scoring/freeze.md
(digest d72a50e1943c1af55846dfb2db93e73b50e08a287c06925a331c0304096128c4;
owner freeze-and-execute order of 2026-10-20).
The prediction's preregistration: OSF https://osf.io/wjebq/,
DOI 10.17605/OSF.IO/WJEBQ (registered 2026-10-13, approved
and public). The frozen spec's own contract registration:
OSF https://osf.io/qkj8d/ (filed 2026-10-20 under DD-035-4;
not a step-0 condition — spec section 3 names wjebq).

The build executes step 0 of Spec 035 section 3, in the
frozen order, fail-closed, before any scoring:

  0.1  The prediction's OSF registration (wjebq) still
       stands accepted and public. If it no longer does,
       execution does not proceed.
  0.2  Input integrity: the corpus file, the crosswalk,
       and the withheld file hash to the values the
       registration pinned (the filtered-pool manifest is
       verified at 0.3, where the pool is re-derived).
       The withheld file is byte-hashed only — its
       content is not opened at step 0.
  0.3  Training-pool re-verification: the corpus file is
       filtered to its CISI rows (source "Corpus of Indus
       Seals and Inscriptions (mayig digitization)"); the
       pool must be 179 inscriptions, all Mohenjo-daro,
       zero Yajnadevam rows; the filtered-pool manifest
       must hash to the registered value; and the recorded
       classification logic (carried verbatim in the
       frozen Phase-396 build) must reproduce the
       derivation record exactly — trained INITIAL set
       {P000, P217, P324}.
  0.4  Crosswalk coverage: under the frozen best-match
       reading (DD-035-5 — best-match rows carry sign
       identity; top-3 alternatives set conflict flags
       only), every trained sign must have a counterpart.
       Any unmappable trained sign (one of three is 33%,
       above the registered 20% cap) closes the study as
       CANNOT BE RUN AS WRITTEN, before the withheld
       file is opened.

The step-0 record is written and hashed before any
scoring begins. This build contains no scoring code:
the registered computation (spec section 5) is reached
only behind a full step-0 pass, and on the executed run
step 0 closed the study at check 0.4 (P000 has no
best-match crosswalk counterpart), so no scoring exists
to gate. No criterion, threshold, set definition, or
mapping is adjusted anywhere in this build.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import urllib.request
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CORPUS_MASTER = REPO / "data" / "normalized" / "corpus_master.csv"
CROSSWALK_CSV = REPO / "data" / "crosswalks" / "yajnadevam_to_parpola_crosswalk.csv"
WITHHELD_CSV = REPO / "backend" / "glossa_lab" / "data" / "yajnadevam_inscriptions.csv"
DERIVATION_RECORD = REPO / "reports" / "pred010_derivation_record.json"
RECORDED_SCRIPT = REPO / "scripts" / "global_class_stability.py"
RESULTS_JSON = REPO / "reports" / "phase399_results.json"

FREEZE_DIGEST = "d72a50e1943c1af55846dfb2db93e73b50e08a287c06925a331c0304096128c4"
CISI_SOURCE = "Corpus of Indus Seals and Inscriptions (mayig digitization)"
TRAINED = ["P000", "P217", "P324"]
UNMAPPABLE_CAP = 0.20
CLOSURE = "CANNOT BE RUN AS WRITTEN"

PIN_CORPUS = "b19cfe955313b7db73b462e697e305c1da21b3b8a6997679a466d959b757b42e"
PIN_MANIFEST = "ab3b4c8ae84090b6f0b60f467dde0067f5dbd2f20065f1625a60a79d7170540a"
PIN_CROSSWALK = "e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2"
PIN_WITHHELD = "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98"
PIN_RECORDED_SCRIPT = "37e7bb533778daf1c4cf1220f71331e38c156b09abce7436bccc53bafb97ad5d"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_json(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, indent=1).encode("utf-8")
    ).hexdigest()


def check_0_1_registration() -> dict:
    """Step 0.1 (spec section 3): wjebq accepted and public."""
    req = urllib.request.Request(
        "https://api.osf.io/v2/registrations/wjebq/",
        headers={"Accept": "application/vnd.api+json"})
    with urllib.request.urlopen(req) as resp:
        a = json.loads(resp.read().decode("utf-8"))["data"]["attributes"]
    passed = (
        a.get("reviews_state") == "accepted"
        and a.get("public") is True
        and a.get("pending_registration_approval") is False
    )
    return {
        "check": "0.1 prediction preregistration (wjebq) "
                 "accepted and public",
        "registration": "https://osf.io/wjebq/",
        "reviews_state": a.get("reviews_state"),
        "public": a.get("public"),
        "pending_registration_approval":
            a.get("pending_registration_approval"),
        "withdrawn": a.get("withdrawn"),
        "date_registered": a.get("date_registered"),
        "status": "pass" if passed else "fail",
        "failure_outcome": None if passed else
            "EXECUTION DOES NOT PROCEED (spec 3, check 0.1)",
    }


def check_0_2_input_integrity(derivation: dict) -> dict:
    """Step 0.2: the registered pins, byte operations only."""
    found = {
        "data/normalized/corpus_master.csv": sha256_file(CORPUS_MASTER),
        "data/crosswalks/yajnadevam_to_parpola_crosswalk.csv":
            sha256_file(CROSSWALK_CSV),
        "backend/glossa_lab/data/yajnadevam_inscriptions.csv":
            sha256_file(WITHHELD_CSV),
    }
    pins = {
        "data/normalized/corpus_master.csv": PIN_CORPUS,
        "data/crosswalks/yajnadevam_to_parpola_crosswalk.csv":
            PIN_CROSSWALK,
        "backend/glossa_lab/data/yajnadevam_inscriptions.csv":
            PIN_WITHHELD,
    }
    record_pins_ok = (
        derivation["training_pool"]["file_sha256"] == PIN_CORPUS
        and derivation["training_pool"]["pool_manifest_sha256"]
        == PIN_MANIFEST
        and derivation["crosswalk_fixed_by_reference"]["file_sha256"]
        == PIN_CROSSWALK
        and derivation["withheld_data_fixed_by_reference"]["file_sha256"]
        == PIN_WITHHELD
    )
    passed = found == pins and record_pins_ok
    return {
        "check": "0.2 input integrity against the registered pins",
        "pins": pins,
        "found": found,
        "manifest_pin": PIN_MANIFEST,
        "derivation_record_internal_pins_match_registered": record_pins_ok,
        "withheld_file_treatment": "byte-hashed only; content not opened",
        "status": "pass" if passed else "fail",
        "failure_outcome": None if passed else CLOSURE,
    }


def _phase396_module():
    spec = importlib.util.spec_from_file_location(
        "phase396_pred006_step0",
        REPO / "backend" / "scripts" / "phase396_pred006_step0.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_0_3_pool_reproduction(derivation: dict) -> dict:
    """Step 0.3: pool census, manifest, verbatim reproduction."""
    p396 = _phase396_module()
    records = p396.load_corpus_master()
    pool = [r for r in records if r["source_name"] == CISI_SOURCE]
    pool_sites = Counter(r["site"] for r in pool)
    yajnadevam_in_pool = sum(
        1 for r in pool if r["source_name"].startswith("Yajnadevam"))
    manifest = p396.sha256_json(pool)
    script_hash_ok = sha256_file(RECORDED_SCRIPT) == PIN_RECORDED_SCRIPT
    classes = p396.recompute_global_classes(pool)
    recorded_classes = derivation["result"]["classes"]
    initial = sorted(s for s, c in classes.items() if c == "INITIAL")
    class_counts = dict(sorted(Counter(classes.values()).items()))
    census_ok = (
        len(pool) == 179 and set(pool_sites) == {"Mohenjo-daro"}
        and yajnadevam_in_pool == 0 and manifest == PIN_MANIFEST)
    reproduction_ok = (
        classes == recorded_classes and initial == TRAINED
        and class_counts == derivation["result"]["class_counts"])
    passed = census_ok and reproduction_ok and script_hash_ok
    return {
        "check": "0.3 training-pool re-verification and "
                 "classification reproduction",
        "filter": f'source_name == "{CISI_SOURCE}"',
        "corpus_rows_total": len(records),
        "pool_rows": len(pool),
        "pool_sites": dict(pool_sites),
        "yajnadevam_rows_in_pool": yajnadevam_in_pool,
        "filtered_pool_manifest_sha256_found": manifest,
        "filtered_pool_manifest_sha256_pin": PIN_MANIFEST,
        "recorded_script_sha256_pin": PIN_RECORDED_SCRIPT,
        "recorded_script_sha256_matches": script_hash_ok,
        "classifiable_signs": len(classes),
        "class_counts": class_counts,
        "recorded_class_counts": derivation["result"]["class_counts"],
        "full_class_map_identical_to_derivation_record":
            classes == recorded_classes,
        "trained_initial_set_reproduced": initial,
        "trained_initial_set_recorded": TRAINED,
        "status": "pass" if passed else "fail",
        "failure_outcome": None if passed else CLOSURE,
    }


def check_0_4_crosswalk_coverage() -> dict:
    """Step 0.4: coverage under the frozen reading (DD-035-5)."""
    rows = list(csv.DictReader(
        open(CROSSWALK_CSV, newline="", encoding="utf-8")))
    header = list(rows[0].keys()) if rows else []
    mapping: dict[str, dict] = {}
    alternatives: set[str] = set()
    for row in rows:
        best = row["best_parpola_match"]
        entry = mapping.setdefault(
            best, {"glyph_ids": [], "confidences": [],
                   "statuses": [], "conflict": False})
        entry["glyph_ids"].append(row["registry_sign_id_yajnadevam"])
        entry["confidences"].append(row.get("match_confidence"))
        entry["statuses"].append(row.get("review_status"))
        for alt in row.get("top3_parpola", "").split("|"):
            alt = alt.strip()
            if ":" in alt:
                alt_sign = alt.split(":", 1)[0].strip()
                if alt_sign and alt_sign != best:
                    alternatives.add(alt_sign)
    for sign, entry in mapping.items():
        entry["conflict"] = sign in alternatives
    coverage = []
    unmappable = []
    for sign in TRAINED:
        entry = mapping.get(sign)
        if entry is None:
            unmappable.append(sign)
        alt_rows = sorted({
            r["registry_sign_id_yajnadevam"] for r in rows
            if any(part.split(":", 1)[0].strip() == sign
                   for part in r.get("top3_parpola", "").split("|"))})
        coverage.append({
            "sign": sign,
            "mappable": entry is not None,
            "best_match_glyphs": entry["glyph_ids"] if entry else [],
            "best_match_confidences":
                entry["confidences"] if entry else [],
            "best_match_statuses": entry["statuses"] if entry else [],
            "conflict_flag": bool(entry and entry["conflict"]),
            "appears_as_top3_alternative_on": alt_rows,
        })
    share = round(len(unmappable) / len(TRAINED), 4) if TRAINED else 0.0
    passed = not unmappable
    record = {
        "check": "0.4 crosswalk coverage of the trained signs "
                 "(DD-035-5 best-match reading)",
        "crosswalk_header": header,
        "coverage": coverage,
        "unmappable_signs": unmappable,
        "unmappable_share": share,
        "registered_cap": UNMAPPABLE_CAP,
        "status": "pass" if passed else "fail",
        "failure_outcome": None if passed else CLOSURE,
    }
    if not passed:
        record["closure_point"] = "before the withheld file is opened"
    return record


def run_step0() -> dict:
    """Step 0 in the frozen order. Stops at the first failed
    check; the closure is the outcome (spec sections 3, 10)."""
    derivation = json.loads(DERIVATION_RECORD.read_text(encoding="utf-8"))
    step0: dict = {}
    c01 = check_0_1_registration()
    step0["check_0_1"] = c01
    if c01["status"] != "pass":
        return _finish(step0, "0.1", proceeded=False)
    c02 = check_0_2_input_integrity(derivation)
    step0["check_0_2"] = c02
    if c02["status"] != "pass":
        return _finish(step0, "0.2")
    c03 = check_0_3_pool_reproduction(derivation)
    step0["check_0_3"] = c03
    if c03["status"] != "pass":
        return _finish(step0, "0.3")
    c04 = check_0_4_crosswalk_coverage()
    step0["check_0_4"] = c04
    if c04["status"] != "pass":
        return _finish(step0, "0.4")
    return _finish(step0, None)


def _finish(step0: dict, failed: str | None,
            proceeded: bool = True) -> dict:
    for nxt in ("check_0_1", "check_0_2", "check_0_3", "check_0_4"):
        if nxt not in step0:
            step0[nxt] = {"status": "not_reached"}
    step0["withheld_file_content_opened"] = False
    if failed is None:
        outcome = {"type": "step0_passed", "scoring_run": False}
    else:
        outcome = {
            "type": "step0_closure",
            "closure": CLOSURE if proceeded else
                "EXECUTION DOES NOT PROCEED",
            "failed_check": failed,
            "scoring_run": False,
            "verdict": None,
            "prediction_state": "UNSCORED - remains PENDING",
        }
    return {"step0": step0, "outcome": outcome}


def main() -> int:
    result = run_step0()
    step0 = result["step0"]
    payload = {
        "phase": 399,
        "spec": "035-pred-2026-010-scoring",
        "experiment_id": "spec035-pred-2026-010-scoring",
        "freeze_digest": FREEZE_DIGEST,
        "registration": {
            "prediction_preregistration": {
                "osf": "https://osf.io/wjebq/",
                "doi": "10.17605/OSF.IO/WJEBQ",
                "state": "accepted and public; re-verified at "
                         "step 0.1 of this run (2026-10-20)",
            },
            "spec_contract_registration": {
                "osf": "https://osf.io/qkj8d/",
                "state": "filed 2026-10-20; pending admin approval "
                         "at execution (not a step-0 condition; "
                         "spec section 3 names wjebq)",
            },
        },
        "prediction": {
            "id": "PRED-2026-010",
            "registered": "2026-10-13",
            "criterion": {
                "share_min": 0.70,
                "start_rate_bar": 0.40,
                "quantity": "share of the trained INITIAL signs "
                            "{P000, P217, P324} whose Harappa start "
                            "rate is at least 0.40, computed on the "
                            "withheld Harappa-site Yajnadevam "
                            "sequences only",
            },
        },
        "step0_record": step0,
        "step0_record_sha256": sha256_json(step0),
        "outcome": result["outcome"],
    }
    RESULTS_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Phase-399 step 0: {json.dumps(result['outcome'], sort_keys=True)}")
    print(f"Step-0 record sha256: {payload['step0_record_sha256']}")
    print(f"Results written: {RESULTS_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

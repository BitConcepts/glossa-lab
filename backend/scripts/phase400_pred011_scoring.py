"""Phase-400 (Spec 036) — PRED-2026-011: step 0 of the
frozen scoring contract, in the frozen order, then —
only behind a full step-0 pass — the registered
scoring (spec section 5).

Freeze: specs/036-pred-2026-011-scoring/freeze.md
(digest bbd5c4fd5abdb69bd79dfc1115a13e7debf56a7ec38d00ab8e2c8ff6132e946;
owner do-all order of 2026-10-20: "do all of spec 036
now"). The prediction's preregistration: OSF
https://osf.io/t6whq/, DOI 10.17605/OSF.IO/T6WHQ
(registered 2026-10-20, approved and public). The
frozen spec's own contract registration: OSF
https://osf.io/gjen4/ (filed 2026-10-20
under DD-036-4; not a step-0 condition — spec
section 3 names t6whq).

The build executes step 0 of Spec 036 section 3, in
the frozen order, fail-closed, before any scoring:

  0.1  The prediction's OSF registration (t6whq) still
       stands accepted and public. If it no longer
       does, execution does not proceed.
  0.2  Input integrity: the corpus file, the
       crosswalk, and the withheld file hash to the
       values the registration pinned (the
       filtered-pool manifest is verified at 0.3,
       where the pool is re-derived). The withheld
       file is byte-hashed only — its content is not
       opened at step 0.
  0.3  Training-pool re-verification and screen
       reproduction: the corpus file is filtered to
       its CISI rows (source "Corpus of Indus Seals
       and Inscriptions (mayig digitization)"); the
       pool must be 179 inscriptions, all
       Mohenjo-daro, zero Yajnadevam rows; the
       filtered-pool manifest must hash to the
       registered value; the recorded classification
       logic (carried verbatim in the frozen
       Phase-396 build) must reproduce the derivation
       record exactly — unscreened INITIAL set
       {P000, P217, P324}; and the registered
       mappability screen, re-applied to the pinned
       crosswalk, must return the trained set
       {P217, P324} exactly, with P000's exclusion
       reproduced as a screen outcome.
  0.4  Crosswalk coverage: under the frozen
       best-match reading (DD-036-5 — best-match rows
       carry sign identity; top-3 alternatives set
       conflict flags only), every trained sign must
       have a counterpart. Any unmappable trained
       sign (one of two is 50%, above the registered
       20% cap) closes the study as CANNOT BE RUN AS
       WRITTEN, before the withheld file is opened.

The step-0 record is written and hashed before any
scoring begins. Only behind a full step-0 pass does
step 1 run the registered computation (spec section
5): the frozen Phase-396 build's scoring function,
unchanged, over the withheld file's Harappa
sequences — each trained sign's start rate is the
share of its Harappa occurrences, counted through
its best-match counterpart glyphs, in which it
stands in initial position. Harappa sequences are
tokenised from the pinned file's text field by the
programme's parser for this dataset (the Phase-284
build's parse_lipi, carried in substance): the text
is split on '-', bracket markers are stripped, and
only 3-digit sign codes are kept — the parser
excludes the '000' eroded-sign placeholder — in
recorded order; each kept code is carried into the
crosswalk's glyph namespace as 'Y' + the code
zero-padded to four digits. Within those sequences
the frozen scoring function keeps every token's
position: a token with no crosswalk mapping stands
as an unmappable placeholder, so initial position
is position in the sequence as recorded. No
criterion, threshold, set definition, or mapping
is adjusted anywhere in this build.
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
DERIVATION_RECORD = (
    REPO / "docs" / "research" / "pred-2026-011-registration"
    / "derivation-record.json"
)
RECORDED_SCRIPT = REPO / "scripts" / "global_class_stability.py"
RESULTS_JSON = REPO / "reports" / "phase400_results.json"

FREEZE_DIGEST = "bbd5c4fd5abdb69bd79dfc1115a13e7debf56a7ec38d00ab8e2c8ff6132e946"
SPEC_REG_ID = "gjen4"
CISI_SOURCE = "Corpus of Indus Seals and Inscriptions (mayig digitization)"
TRAINED = ["P217", "P324"]
UNSCREENED = ["P000", "P217", "P324"]
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


def _phase396_module():
    spec = importlib.util.spec_from_file_location(
        "phase396_pred006_step0",
        REPO / "backend" / "scripts" / "phase396_pred006_step0.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _pred011_module():
    spec = importlib.util.spec_from_file_location(
        "pred011_register_derivation",
        REPO / "backend" / "scripts" / "pred011_register_derivation.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_0_1_registration() -> dict:
    """Step 0.1 (spec section 3): t6whq accepted and public."""
    req = urllib.request.Request(
        "https://api.osf.io/v2/registrations/t6whq/",
        headers={"Accept": "application/vnd.api+json"})
    with urllib.request.urlopen(req) as resp:
        a = json.loads(resp.read().decode("utf-8"))["data"]["attributes"]
    passed = (
        a.get("reviews_state") == "accepted"
        and a.get("public") is True
        and a.get("pending_registration_approval") is False
    )
    return {
        "check": "0.1 prediction preregistration (t6whq) "
                 "accepted and public",
        "registration": "https://osf.io/t6whq/",
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


def check_0_3_pool_and_screen(derivation: dict) -> dict:
    """Step 0.3: pool census, manifest, verbatim reproduction,
    and the registered screen re-applied."""
    p396 = _phase396_module()
    records = p396.load_corpus_master()
    pool = [r for r in records if r["source_name"] == CISI_SOURCE]
    pool_sites = Counter(r["site"] for r in pool)
    yajnadevam_in_pool = sum(
        1 for r in pool if r["source_name"].startswith("Yajnadevam"))
    manifest = p396.sha256_json(pool)
    script_hash_ok = sha256_file(RECORDED_SCRIPT) == PIN_RECORDED_SCRIPT
    classes = p396.recompute_global_classes(pool)
    recorded = derivation["underlying_classification"]
    recorded_classes = recorded["classes"]
    initial = sorted(s for s, c in classes.items() if c == "INITIAL")
    class_counts = dict(sorted(Counter(classes.values()).items()))
    census_ok = (
        len(pool) == 179 and set(pool_sites) == {"Mohenjo-daro"}
        and yajnadevam_in_pool == 0 and manifest == PIN_MANIFEST)
    reproduction_ok = (
        classes == recorded_classes and initial == UNSCREENED
        and class_counts == recorded["class_counts"])
    # The registered screen, re-applied by the derivation
    # build's own screen function to the pinned crosswalk.
    p011 = _pred011_module()
    with open(CROSSWALK_CSV, newline="", encoding="utf-8") as handle:
        crosswalk_rows = list(csv.DictReader(handle))
    screen = p011._screen(UNSCREENED, crosswalk_rows)
    recorded_screen = derivation["mappability_screen"]
    screened = screen["trained_initial_set"]
    excluded = screen["excluded_signs"]
    recorded_excluded = recorded_screen["excluded_signs"]
    excluded_glyphs = sorted(
        a["yajnadevam_glyph"]
        for e in excluded for a in e["top3_only_appearances"])
    recorded_excluded_glyphs = sorted(
        a["yajnadevam_glyph"]
        for e in recorded_excluded for a in e["top3_only_appearances"])
    screen_ok = (
        screened == recorded_screen["trained_initial_set"] == TRAINED
        and [e["sign"] for e in excluded]
        == [e["sign"] for e in recorded_excluded] == ["P000"]
        and excluded_glyphs == recorded_excluded_glyphs)
    counterparts_ok = all(
        screen["counterparts_by_underlying_initial_sign"].get(sign)
        == recorded_screen[
            "counterparts_by_underlying_initial_sign"].get(sign)
        for sign in UNSCREENED)
    passed = census_ok and reproduction_ok and script_hash_ok \
        and screen_ok and counterparts_ok
    return {
        "check": "0.3 training-pool re-verification, classification "
                 "reproduction, and screen reproduction",
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
        "recorded_class_counts": recorded["class_counts"],
        "full_class_map_identical_to_derivation_record":
            classes == recorded_classes,
        "unscreened_initial_set_reproduced": initial,
        "unscreened_initial_set_recorded": UNSCREENED,
        "screen_reapplied": {
            "rule": recorded_screen["rule"],
            "screened_trained_set": screened,
            "screened_trained_set_recorded":
                recorded_screen["trained_initial_set"],
            "excluded_signs": [e["sign"] for e in excluded],
            "excluded_top3_only_glyphs": excluded_glyphs,
            "counterparts_identical_to_derivation_record":
                counterparts_ok,
        },
        "status": "pass" if passed else "fail",
        "failure_outcome": None if passed else CLOSURE,
    }


def check_0_4_crosswalk_coverage() -> dict:
    """Step 0.4: coverage under the frozen reading (DD-036-5)."""
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
                 "(DD-036-5 best-match reading)",
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


def tokenise_yajnadevam_text(text: str) -> list[str]:
    """The programme's parser for this dataset (the
    Phase-284 build's parse_lipi, carried in substance):
    split the recorded text on '-', strip bracket
    markers, keep only 3-digit sign codes — the parser
    excludes the '000' eroded-sign placeholder — in
    recorded order; carry each kept code into the
    crosswalk's glyph namespace ('Y' + zero-padded
    four digits)."""
    text = (text or "").strip().strip("+")
    if not text:
        return []
    signs = []
    for part in text.split("-"):
        s = part.strip().rstrip("[").lstrip("]")
        if s and s != "000" and not s.startswith("[") \
                and not s.startswith("/"):
            if s.isdigit() and len(s) == 3:
                signs.append("Y" + s.zfill(4))
    return signs


def run_scoring() -> dict:
    """Step 1 (spec section 5): the registered computation,
    run only behind a full step-0 pass. The scoring
    function is the frozen Phase-396 build's, unchanged;
    the crosswalk is fixed by that build's own function."""
    p396 = _phase396_module()
    crosswalk = p396.fix_crosswalk()
    with open(WITHHELD_CSV, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    harappa_rows = [r for r in rows if r.get("site") == "Harappa"]
    sequences = []
    rows_without_tokens = 0
    for row in harappa_rows:
        seq = tokenise_yajnadevam_text(row.get("text") or "")
        if seq:
            sequences.append(seq)
        else:
            rows_without_tokens += 1
    scoring = p396.score_registered_test(TRAINED, crosswalk, sequences)
    lengths = sorted(len(s) for s in sequences)
    median = lengths[len(lengths) // 2] if lengths else 0
    return {
        "withheld_rows_total": len(rows),
        "harappa_rows": len(harappa_rows),
        "harappa_sequences_tokenised": len(sequences),
        "harappa_rows_without_tokens": rows_without_tokens,
        "total_tokens_in_harappa_sequences":
            sum(len(s) for s in sequences),
        "sequence_length_composition": {
            "median_length": median,
            "single_sign_sequences":
                sum(1 for s in sequences if len(s) == 1),
            "length_counts": dict(sorted(
                Counter(len(s) for s in sequences).items())),
        },
        "tokenisation": (
            "the Phase-284 build's parse_lipi carried in "
            "substance (split on '-'; bracket markers "
            "stripped; only 3-digit sign codes kept, the "
            "'000' eroded-sign placeholder excluded by "
            "that parser; recorded order; codes carried "
            "as 'Y' + zero-padded four digits)"),
        "computation": (
            "backend/scripts/phase396_pred006_step0.py "
            "score_registered_test + fix_crosswalk, "
            "imported unchanged from the frozen "
            "Phase-396 build"),
        **scoring,
    }


def run_step0() -> dict:
    """Step 0 in the frozen order. Stops at the first failed
    check; the closure is the outcome (spec sections 3, 10).
    Behind a full pass, step 1 scores (spec section 5)."""
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
    c03 = check_0_3_pool_and_screen(derivation)
    step0["check_0_3"] = c03
    if c03["status"] != "pass":
        return _finish(step0, "0.3")
    c04 = check_0_4_crosswalk_coverage()
    step0["check_0_4"] = c04
    if c04["status"] != "pass":
        return _finish(step0, "0.4")
    result = _finish(step0, None)
    scoring = run_scoring()
    result["scoring"] = scoring
    result["step0"]["withheld_file_content_opened"] = True
    result["step0"]["withheld_content_opened_after"] = (
        "all four step-0 checks passed (spec section 3)")
    result["outcome"] = {
        "type": "verdict",
        "verdict": scoring["verdict"],
        "share": scoring["share"],
        "signs_meeting_bar": scoring["signs_meeting_bar"],
        "trained_set_size": scoring["trained_set_size"],
        "scoring_run": True,
        "prediction_state": scoring["verdict"],
    }
    return result


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
        "phase": 400,
        "spec": "036-pred-2026-011-scoring",
        "experiment_id": "spec036-pred-2026-011-scoring",
        "freeze_digest": FREEZE_DIGEST,
        "registration": {
            "prediction_preregistration": {
                "osf": "https://osf.io/t6whq/",
                "doi": "10.17605/OSF.IO/T6WHQ",
                "state": "accepted and public; re-verified at "
                         "step 0.1 of this run (2026-10-20)",
            },
            "spec_contract_registration": {
                "osf": f"https://osf.io/{SPEC_REG_ID}/",
                "state": "filed 2026-10-20 under DD-036-4 "
                         "(not a step-0 condition; spec "
                         "section 3 names t6whq)",
            },
        },
        "prediction": {
            "id": "PRED-2026-011",
            "registered": "2026-10-20",
            "criterion": {
                "share_min": 0.70,
                "start_rate_bar": 0.40,
                "quantity": "share of the trained INITIAL signs "
                            "{P217, P324} whose Harappa start "
                            "rate is at least 0.40, computed on "
                            "the withheld Harappa-site "
                            "Yajnadevam sequences only",
            },
        },
        "step0_record": step0,
        "step0_record_sha256": sha256_json(step0),
        "outcome": result["outcome"],
    }
    if "scoring" in result:
        payload["scoring_record"] = result["scoring"]
        payload["scoring_record_sha256"] = sha256_json(result["scoring"])
    RESULTS_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Phase-400: {json.dumps(result['outcome'], sort_keys=True)}")
    print(f"Step-0 record sha256: {payload['step0_record_sha256']}")
    if "scoring_record_sha256" in payload:
        print(f"Scoring record sha256: {payload['scoring_record_sha256']}")
    print(f"Results written: {RESULTS_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

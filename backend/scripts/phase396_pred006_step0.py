"""Phase-396 (Spec 032) — PRED-2026-006: the Harappa
breakdown, computed exactly as registered.

Freeze: specs/032-pred-2026-006-harappa-breakdown/freeze.md
(digest 34cd6230471c746878ab80110c4a07c3f3daeecef6c05bf222521b39054490ab;
design D-30 of the 2026-10-13 experiment-design portfolio,
carried into the freeze without deviation).
Registered before execution: OSF https://osf.io/3htn8/,
DOI 10.17605/OSF.IO/3HTN8 (approved and public 2026-10-13).
Execution ordered by the owner 2026-10-13 ("Do ALL that
remains now", and the Spec 032 execution order of the same
day).

The build executes the frozen shape of Spec 032 section 10:

  E2  Step 0 — provenance checks (spec section 3), run in
      the frozen order, before any counting. The step-0
      record is written and hashed before any counting
      begins. A step-0 failure closes the study under
      section 3 and the closure is the outcome:
        3.1  The trained INITIAL set is reconstructed from
             the recorded global_class_stability lineage
             (scripts/global_class_stability.py;
             outputs/analysis/global_class_stability.json;
             reports/global_class_stability_report.md) and
             frozen as a list. Failure to reproduce the
             exact set closes the study as CANNOT BE RUN
             AS WRITTEN (F032-C04).
        3.2  The withholding is verified: the INITIAL
             assignments came from CISI Mohenjo-daro, and
             the Harappa Yajnadevam sequences played no
             part in training them (F032-C05). Failure
             closes the study as CANNOT BE RUN AS WRITTEN.
        3.3  Sign identity is fixed through the existing
             crosswalks under data/crosswalks/ before
             counting (F032-C06); unmappable trained signs
             are counted and reported, and coverage above
             20 percent leads the verdict's first sentence
             (F032-C07) — a reporting rule, not a closure.
  E3  Scoring — the registered computation only (spec
      section 5): for each frozen trained INITIAL sign, its
      Harappa start rate on the withheld Yajnadevam Harappa
      sequences; the share at or above 0.40; the verdict
      under section 6 (CONFIRMED at a share of at least
      70 percent, NOT CONFIRMED below; no other band).
      E3 runs only if step 0 passes in full.

No criterion, threshold, set definition, or mapping is
adjusted anywhere in this build (DD-30-1..DD-30-3).
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CORPUS_MASTER = REPO / "data" / "normalized" / "corpus_master.csv"
STABILITY_JSON = REPO / "outputs" / "analysis" / "global_class_stability.json"
YAJNADEVAM_CSV = REPO / "backend" / "glossa_lab" / "data" / "yajnadevam_inscriptions.csv"
CROSSWALK_CSV = REPO / "data" / "crosswalks" / "yajnadevam_to_parpola_crosswalk.csv"
RESULTS_JSON = REPO / "reports" / "phase396_results.json"

FREEZE_DIGEST = "34cd6230471c746878ab80110c4a07c3f3daeecef6c05bf222521b39054490ab"
SHARE_MIN = 0.70
START_RATE_BAR = 0.40
UNMAPPABLE_REPORT_THRESHOLD = 0.20
CLOSURE = "CANNOT BE RUN AS WRITTEN"

# The recorded lineage's own constants and rule, carried
# verbatim from scripts/global_class_stability.py (the
# recorded run of 2026-04-22T18:16:22Z). They are the
# training's definitions; nothing here re-decides them.
MIN_FREQ_GLOBAL = 10


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_json(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, indent=1).encode("utf-8")
    ).hexdigest()


def _positional_profile(records: list[dict]) -> dict[str, dict]:
    """The recorded script's positional_profile, verbatim."""
    freq: Counter = Counter()
    sf: Counter = Counter()
    ef: Counter = Counter()
    intf: Counter = Counter()
    for r in records:
        seq = r["sign_sequence_raw"].split()
        for i, s in enumerate(seq):
            if not s.startswith("P"):
                continue
            freq[s] += 1
            if i == 0:
                sf[s] += 1
            elif i == len(seq) - 1:
                ef[s] += 1
            else:
                intf[s] += 1
    return {
        s: {
            "freq": f,
            "sr": round(sf[s] / f, 4),
            "er": round(ef[s] / f, 4),
            "ir": round(intf[s] / f, 4),
        }
        for s, f in freq.items()
    }


def _classify(p: dict) -> str:
    """The recorded script's classify, verbatim."""
    f = p["freq"]
    if f < MIN_FREQ_GLOBAL:
        return "INSUFFICIENT_DATA"
    if p["er"] >= 0.55:
        return "TERMINAL"
    if p["sr"] >= 0.55:
        return "INITIAL"
    if p["ir"] >= 0.70:
        return "MEDIAL"
    if p["sr"] >= 0.30 and p["er"] >= 0.30 and p["ir"] < 0.30:
        return "BIMODAL"
    return "MIXED"


def recompute_global_classes(records: list[dict]) -> dict[str, str]:
    """Recompute the recorded global classification from the
    recorded training corpus. Returns the classifiable map
    (INSUFFICIENT_DATA excluded, as the recorded JSON's
    global_classes holds only classifiable signs)."""
    profile = _positional_profile(records)
    classes = {s: _classify(p) for s, p in profile.items()}
    return {s: c for s, c in classes.items() if c != "INSUFFICIENT_DATA"}


def load_corpus_master() -> list[dict]:
    with open(CORPUS_MASTER, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_3_1_trained_set(records: list[dict], recorded: dict) -> dict:
    """Step 0.1 (spec 3.1 / F032-C03, C04): the exact trained
    INITIAL set, reconstructed from the recorded lineage.

    Passes iff the classification recomputed from the
    recorded training corpus reproduces the recorded
    output's classifiable map exactly; the trained INITIAL
    set is then the recorded map's INITIAL signs, frozen.
    """
    recomputed = recompute_global_classes(records)
    recorded_classes = recorded["global_classes"]
    matches = recomputed == recorded_classes
    initial = sorted(s for s, c in recorded_classes.items() if c == "INITIAL")
    return {
        "check": "3.1 trained INITIAL set reconstruction",
        "status": "pass" if matches else "fail",
        "recorded_output": "outputs/analysis/global_class_stability.json",
        "recorded_generated": recorded.get("generated"),
        "recomputed_classifiable_signs": len(recomputed),
        "recorded_classifiable_signs": len(recorded_classes),
        "maps_identical": matches,
        "trained_initial_set": initial if matches else None,
        "trained_initial_set_size": len(initial) if matches else None,
        "failure_outcome": None if matches else CLOSURE,
    }


def check_3_2_withholding(records: list[dict], trained_initial: list[str]) -> dict:
    """Step 0.2 (spec 3.2 / F032-C05): the withholding was
    real for this purpose.

    The frozen fact has two parts: the INITIAL assignments
    came from CISI Mohenjo-daro, and the Harappa Yajnadevam
    sequences played no part in training them. Both are
    tested against the recorded training corpus itself:
    the corpus the recorded lineage classified on.
    """
    by_source: Counter = Counter()
    cisi_sites: Counter = Counter()
    yajnadevam_rows = 0
    yajnadevam_harappa_rows: list[dict] = []
    for r in records:
        by_source[r["source_name"]] += 1
        if r["source_name"].startswith("Yajnadevam"):
            yajnadevam_rows += 1
            if r["site"] == "Harappa":
                yajnadevam_harappa_rows.append(r)
        else:
            cisi_sites[r["site"]] += 1
    occurrences = {}
    for sign in trained_initial:
        occurrences[sign] = sum(
            r["sign_sequence_raw"].split().count(sign)
            for r in yajnadevam_harappa_rows
        )
    total_occurrences = sum(occurrences.values())
    signs_present = sum(1 for v in occurrences.values() if v > 0)
    training_was_cisi_mohenjo_only = (
        yajnadevam_rows == 0 and set(cisi_sites) == {"Mohenjo-daro"}
    )
    harappa_yajnadevam_played_no_part = total_occurrences == 0
    passed = training_was_cisi_mohenjo_only and harappa_yajnadevam_played_no_part
    return {
        "check": "3.2 withholding verification",
        "status": "pass" if passed else "fail",
        "training_corpus": "data/normalized/corpus_master.csv",
        "training_corpus_rows": len(records),
        "rows_by_source": dict(by_source),
        "cisi_rows_sites": dict(cisi_sites),
        "yajnadevam_rows_in_training_corpus": yajnadevam_rows,
        "yajnadevam_harappa_rows_in_training_corpus": len(yajnadevam_harappa_rows),
        "trained_sign_occurrences_inside_yajnadevam_harappa": occurrences,
        "trained_signs_present_inside_yajnadevam_harappa": signs_present,
        "total_trained_sign_occurrences_inside_yajnadevam_harappa": total_occurrences,
        "fact_part_1_assignments_from_cisi_mohenjo_daro_only": (
            training_was_cisi_mohenjo_only
        ),
        "fact_part_2_harappa_yajnadevam_played_no_part": (
            harappa_yajnadevam_played_no_part
        ),
        "failure_outcome": None if passed else CLOSURE,
    }


def fix_crosswalk() -> dict[str, dict]:
    """Step 0.3 (spec 3.3 / F032-C06): the sign-identity
    mapping, fixed from the existing crosswalk file before
    counting. Returns {parpola_sign: {glyph_ids, conflict}}.

    A trained sign is conflict-flagged (spec section 8)
    when any glyph whose best match is a different sign
    lists it among its top-3 alternatives.
    """
    mapping: dict[str, dict] = {}
    alternatives: set[str] = set()
    rows = list(csv.DictReader(open(CROSSWALK_CSV, newline="", encoding="utf-8")))
    for row in rows:
        best = row["best_parpola_match"]
        entry = mapping.setdefault(best, {"glyph_ids": [], "conflict": False})
        entry["glyph_ids"].append(row["registry_sign_id_yajnadevam"])
        for alt in row.get("top3_parpola", "").split("|"):
            alt = alt.strip()
            if ":" in alt:
                alt_sign = alt.split(":", 1)[0].strip()
                if alt_sign and alt_sign != best:
                    alternatives.add(alt_sign)
    for sign, entry in mapping.items():
        entry["conflict"] = sign in alternatives
    return mapping


def score_registered_test(
    trained_initial: list[str],
    crosswalk: dict[str, dict],
    harappa_sequences: list[list[str]],
) -> dict:
    """The registered computation (spec section 5), nothing
    added. Runs only behind a full step-0 pass.

    harappa_sequences are the withheld Harappa sequences
    tokenised to Yajnadevam glyph ids. Tokens with no
    crosswalk mapping keep their position as unmappable
    placeholders (the corpus's own Yunmapped convention),
    so initial position is position in the sequence as
    recorded. A trained sign with no crosswalk counterpart
    is UNMAPPABLE: counted in the denominator, never in
    the numerator. A trained sign with no Harappa
    occurrence has no start rate at or above the bar:
    counted in the denominator, never in the numerator.
    """
    glyph_to_parpola = {}
    for parpola, entry in crosswalk.items():
        for glyph in entry["glyph_ids"]:
            glyph_to_parpola[glyph] = parpola
    occurrences: Counter = Counter()
    initial_occurrences: Counter = Counter()
    for seq in harappa_sequences:
        mapped = [glyph_to_parpola.get(tok) for tok in seq]
        for i, sign in enumerate(mapped):
            if sign is None or sign not in trained_initial:
                continue
            occurrences[sign] += 1
            if i == 0:
                initial_occurrences[sign] += 1
    table = []
    n_meeting = 0
    n_unmappable = 0
    for sign in trained_initial:
        entry = crosswalk.get(sign)
        unmappable = entry is None
        if unmappable:
            n_unmappable += 1
        occ = occurrences.get(sign, 0)
        init = initial_occurrences.get(sign, 0)
        start_rate = round(init / occ, 4) if occ else None
        meets = start_rate is not None and start_rate >= START_RATE_BAR
        if meets:
            n_meeting += 1
        table.append({
            "sign": sign,
            "unmappable": unmappable,
            "crosswalk_conflict": bool(entry and entry["conflict"]),
            "harappa_occurrences": occ,
            "initial_occurrences": init,
            "start_rate": start_rate,
            "meets_bar": meets,
        })
    share = round(n_meeting / len(trained_initial), 4) if trained_initial else 0.0
    unmappable_share = (
        round(n_unmappable / len(trained_initial), 4) if trained_initial else 0.0
    )
    return {
        "per_sign_table": table,
        "signs_meeting_bar": n_meeting,
        "trained_set_size": len(trained_initial),
        "unmappable_signs": n_unmappable,
        "unmappable_share": unmappable_share,
        "unmappable_coverage_leads_verdict": (
            unmappable_share > UNMAPPABLE_REPORT_THRESHOLD
        ),
        "share": share,
        "verdict": "CONFIRMED" if share >= SHARE_MIN else "NOT CONFIRMED",
    }


def run_step0() -> dict:
    """Step 0 in the frozen order. Stops at the first failed
    check; the closure is the outcome (spec sections 3, 10).
    The registered scoring is never reached on a closure.
    """
    records = load_corpus_master()
    recorded = json.loads(STABILITY_JSON.read_text(encoding="utf-8"))
    c31 = check_3_1_trained_set(records, recorded)
    step0: dict = {"check_3_1": c31}
    if c31["status"] != "pass":
        step0["check_3_2"] = {"status": "not_reached"}
        step0["check_3_3"] = {"status": "not_reached"}
        return {
            "step0": step0,
            "outcome": {
                "type": "step0_closure",
                "closure": CLOSURE,
                "failed_check": "3.1",
                "scoring_run": False,
            },
        }
    trained = c31["trained_initial_set"]
    c32 = check_3_2_withholding(records, trained)
    step0["check_3_2"] = c32
    if c32["status"] != "pass":
        step0["check_3_3"] = {"status": "not_reached"}
        return {
            "step0": step0,
            "trained_initial_set": trained,
            "outcome": {
                "type": "step0_closure",
                "closure": CLOSURE,
                "failed_check": "3.2",
                "scoring_run": False,
            },
        }
    # Step 0 passed in full: fix the crosswalk (3.3), then
    # E3 would score the withheld set. (Not reached on the
    # recorded lineage; see outcome.md.)
    crosswalk = fix_crosswalk()
    unmappable = [s for s in trained if s not in crosswalk]
    step0["check_3_3"] = {
        "check": "3.3 sign identity fixed before counting",
        "status": "pass",
        "crosswalk": "data/crosswalks/yajnadevam_to_parpola_crosswalk.csv",
        "unmappable_signs": unmappable,
        "unmappable_share": round(len(unmappable) / len(trained), 4),
    }
    return {
        "step0": step0,
        "trained_initial_set": trained,
        "outcome": {"type": "step0_passed", "scoring_run": False},
    }


def main() -> int:
    result = run_step0()
    step0_record = {
        "step0": result["step0"],
        "trained_initial_set": result.get("trained_initial_set"),
        "inputs": {
            "training_corpus_sha256": sha256_file(CORPUS_MASTER),
            "recorded_stability_output_sha256": sha256_file(STABILITY_JSON),
            "crosswalk_sha256": sha256_file(CROSSWALK_CSV),
            "withheld_file_sha256": sha256_file(YAJNADEVAM_CSV),
        },
    }
    payload = {
        "phase": 396,
        "spec": "032-pred-2026-006-harappa-breakdown",
        "experiment_id": "spec032-pred-2026-006-harappa-breakdown",
        "freeze_digest": FREEZE_DIGEST,
        "registration": {
            "osf": "https://osf.io/3htn8/",
            "doi": "10.17605/OSF.IO/3HTN8",
            "state": "approved and public before execution (2026-10-13)",
        },
        "prediction": {
            "id": "PRED-2026-006",
            "registered": "2026-04-22",
            "criterion": {
                "share_min": SHARE_MIN,
                "start_rate_bar": START_RATE_BAR,
                "quantity": (
                    "share of the frozen trained INITIAL signs whose "
                    "Harappa start rate is at least 0.40, computed on "
                    "the withheld Harappa-site Yajnadevam sequences only"
                ),
            },
        },
        "step0_record": step0_record,
        "step0_record_sha256": sha256_json(step0_record),
        "outcome": result["outcome"],
    }
    RESULTS_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"
    )
    outcome = result["outcome"]
    print(f"Phase-396 step 0: {json.dumps(outcome, sort_keys=True)}")
    print(f"Step-0 record sha256: {payload['step0_record_sha256']}")
    print(f"Results written: {RESULTS_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

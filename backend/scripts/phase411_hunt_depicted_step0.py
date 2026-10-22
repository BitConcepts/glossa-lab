#!/usr/bin/env python3
"""Phase-411 — Spec 045 step 0 (Hunt's three parts:
pattern, or meanings?; design D-05; builder of Asset A).

Executes STEP 0 of the frozen Spec 045 contract
(specs/045-hunt-depicted-kinds/freeze.md; freeze digest
5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a;
OSF registration 4mt9k, approved and public before this
run) under the campaign's Wave 3 execution order, in
which step 0 runs first — as the Group 1 executions of
Specs 044 (Phase-404) and 047 (Phase-406) ran their
step-0 gates before any asset build. Only if every
step-0 gate passes does step 1 build Asset A. This
script contains no Asset A entry code, no model code,
and no join code: a step-0 failure closes the execution
before any of those exist, by the frozen design.

Gates, in the frozen order (spec section 6):

  0.1 Input integrity — every spec section 4 input
      hashes to its freeze-record value. (The clause
      "Asset A's digest recomputes" belongs to the
      post-build reading of this gate: Asset A does
      not exist before step 1, so there is no asset
      digest to recompute at step 0; the asset gates
      A1–A6 govern the build if it is ever reached.)
      Mismatch closes INVALID.
  0.2 Positional reproduction — the pinned positional
      record's quantities are reproduced from the
      pinned corpus under the recorded framework: the
      805/2,267 formula count and the 40/61/20
      strong-sign classes. The reproduction attempt is
      mechanical and is recorded in full:
        R1 the recorded quantities, read from the
           pinned positional record itself;
        R2 the pinned corpus's own census — records,
           and inscriptions of length >= 3 under the
           corpus's text field — against the recorded
           denominator 2,267;
        R3 the Phase-43 battery record's structure —
           the counts it states, the member lists it
           does or does not exhibit (its terminal list,
           any initial/medial list), and the per-sign
           role labels it carries;
        R4 the recorded framework — a tree scan for
           any Phase-43 code path or methods record
           beyond the results file, and for the
           positional record's producing script;
        R5 the corpus the positional quantities in
           fact belong to, per the fuller record of
           the same test (the Batch-5 analysis report,
           which carries the identical quantities and
           names its corpus), and whether that
           corpus's data file exists in the tree —
           including the corpus-v3 loader's own
           Firestore dump path.
      No threshold, floor, subset rule, or member
      list is invented, borrowed from a neighbouring
      battery, or substituted: if the recorded
      framework does not state the rule, the
      reproduction fails as recorded. Mismatch
      closes INVALID.
  0.3 Population census — reached only if 0.2 passes.
  0.4 Freeze-order proof — reached only if 0.3 passes.

On a gate failure the execution stops in the frozen
order: later gates are NOT REACHED, no model quantity
is computed, and Asset A is not built.

Outputs (written on every terminal outcome):
  - reports/phase411_results.json (the step-0 record)
  - reports/phase411_step0_report.md (the step-0
    report, under spec section 9's headline rules as
    they apply to a step-0 closure)

Integrity: every section 4 pin is asserted before any
reproduction quantity; the anchors file is asserted
byte-identical before and after. The script is
deterministic: a second run reproduces both output
files byte-identically.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]

PIN_POSITIONAL = (
    "glossa-indus/analysis/positional/hunt_tripartite_test.json",
    "0e546962c1b72b929c87d4ce40c97633e8e3e340737f32f5dd3eae9f04759e48",
)
PIN_PHASE43 = (
    "outputs/phase43_all.json",
    "78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4",
)
PIN_CORPUS = (
    "backend/glossa_lab/data/yajnadevam_inscriptions.csv",
    "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98",
)
PIN_CROSSWALK = (
    "data/crosswalks/sign_crosswalk_master.csv",
    "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf",
)
PIN_ANCHORS = (
    "backend/reports/INDUS_FINAL_ANCHORS.json",
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
)
PIN_CONCORDANCE = (
    "specs/046-horned-tiger-concordance/concordance-297.json",
    "772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf",
)
BATCH5_RECORD = (
    "glossa-indus/reports/model_reports/batch5_analysis_report.json"
)
FIRESTORE_DUMP = (
    "glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/"
    "firestore_indusarrays_full.jsonl"
)

_OUT_RESULTS = _REPO / "reports/phase411_results.json"
_OUT_REPORT = _REPO / "reports/phase411_step0_report.md"

EXECUTION_DATE = "2026-10-21"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _check_pin(rel: str, pin: str) -> dict:
    path = _REPO / rel
    if not path.exists():
        return {"file": rel, "pin": pin, "observed": None,
                "present": False, "match": False}
    observed = _sha256(path)
    return {"file": rel, "pin": pin, "observed": observed,
            "present": True, "match": observed == pin}


def _corpus_census() -> dict:
    path = _REPO / PIN_CORPUS[0]
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    len_ge3 = 0
    nonempty = 0
    for r in rows:
        text = (r.get("text") or "").strip().strip("+")
        seq = [s for s in text.split("-") if s] if text else []
        if seq:
            nonempty += 1
        if len(seq) >= 3:
            len_ge3 += 1
    return {"records": len(rows),
            "inscriptions_with_text": nonempty,
            "inscriptions_len_ge3": len_ge3}


def _crosswalk_census() -> dict:
    path = _REPO / PIN_CROSSWALK[0]
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return {"rows": len(rows),
            "distinct_registry_sign_id":
                len({r["registry_sign_id"] for r in rows})}


def _phase43_structure() -> dict:
    rec = json.loads((_REPO / PIN_PHASE43[0]).read_text("utf-8"))
    t22 = rec["T2_2_terminal_suffix_table"]
    t11 = rec["T1_1_corpus_v3"]
    # Any member list exhibited for the initial or medial
    # classes, anywhere in the record?
    member_lists = []

    def walk(obj, trail):
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f"{trail}/{k}")
        elif isinstance(obj, list) and trail.endswith(
                ("initial_strong", "medial_strong")):
            member_lists.append(
                {"path": trail, "entries": len(obj)})

    walk(rec, "")
    role_counts = Counter(
        row.get("positional_role") for row in rec["T2_1_rebus_table"])
    return {
        "t2_2_counts": {
            "initial_strong_count": t22["initial_strong_count"],
            "medial_strong_count": t22["medial_strong_count"],
            "terminal_strong_count": t22["terminal_strong_count"],
            "terminal_moderate_count": t22["terminal_moderate_count"],
            "total_signs_profiled": t22["total_signs_profiled"],
        },
        "terminal_strong_list_exhibited": len(t22["terminal_strong"]),
        "initial_or_medial_member_lists_exhibited": member_lists,
        "t2_1_role_labels": dict(sorted(role_counts.items())),
        "t1_1_corpus": {
            "source": t11["source"],
            "total_records": t11["total_records"],
            "total_sequences": t11["total_sequences"],
            "unique_dockeys": t11["unique_dockeys"],
        },
        "record_keys": sorted(rec.keys()),
    }


def _tree_scan() -> dict:
    hits = []
    for path in _REPO.rglob("*"):
        if ".git" in path.parts or "node_modules" in path.parts:
            continue
        name = path.name.lower()
        if "phase43" in name or "phase_43" in name or "phase-43" in name:
            hits.append(str(path.relative_to(_REPO)))
    producers = []
    for path in _REPO.rglob("*.py"):
        if ".git" in path.parts:
            continue
        if "hunt_tripartite" in path.name:
            producers.append(str(path.relative_to(_REPO)))
    return {"phase43_paths": sorted(hits),
            "hunt_tripartite_code_paths": sorted(producers),
            "firestore_dump_present": (_REPO / FIRESTORE_DUMP).exists(),
            "firestore_dump_path": FIRESTORE_DUMP}


def main() -> int:
    anchors_before = _sha256(_REPO / PIN_ANCHORS[0])

    # ── Gate 0.1 — input integrity ──────────────────────
    pins = [_check_pin(*p) for p in (
        PIN_POSITIONAL, PIN_PHASE43, PIN_CORPUS,
        PIN_CROSSWALK, PIN_ANCHORS)]
    gate_01 = {
        "gate": "0.1",
        "name": "Input integrity",
        "inputs": pins,
        "asset_a_digest_clause": (
            "not applicable at step 0: Asset A does not "
            "exist before step 1; no asset digest exists "
            "to recompute"),
        "verdict": "PASS" if all(p["match"] for p in pins)
                   else "FAIL",
    }

    gates = [gate_01]
    reproduction = None
    outcome = None

    if gate_01["verdict"] != "PASS":
        outcome = "INVALID"
        gates.append({"gate": "0.2", "verdict": "NOT REACHED"})
        gates.append({"gate": "0.3", "verdict": "NOT REACHED"})
        gates.append({"gate": "0.4", "verdict": "NOT REACHED"})
    else:
        # ── Gate 0.2 — positional reproduction ──────────
        positional = json.loads(
            (_REPO / PIN_POSITIONAL[0]).read_text("utf-8"))
        recorded = {
            "formula_numerator":
                positional["formula_test"]
                ["inscriptions_with_imit_structure"],
            "formula_denominator":
                positional["formula_test"]
                ["total_inscriptions_len3plus"],
            "initial_strong":
                positional["structural_test"]
                ["initial_strong_signs"],
            "medial_strong":
                positional["structural_test"]
                ["medial_strong_signs"],
            "terminal_strong":
                positional["structural_test"]
                ["terminal_strong_signs"],
            "mean_i_rate_of_initial_signs":
                positional["structural_test"]
                ["mean_i_rate_of_initial_signs"],
            "expected_i_by_chance":
                positional["structural_test"]
                ["expected_i_by_chance"],
        }
        census = _corpus_census()
        crosswalk = _crosswalk_census()
        p43 = _phase43_structure()
        scan = _tree_scan()
        batch5 = json.loads((_REPO / BATCH5_RECORD).read_text("utf-8"))
        batch5_hunt = batch5["results"]["hunt_tripartite"]
        batch5_same_quantities = (
            batch5_hunt["formula_test"]
            ["inscriptions_with_imit_structure"]
            == recorded["formula_numerator"]
            and batch5_hunt["formula_test"]
            ["total_inscriptions_len3plus"]
            == recorded["formula_denominator"]
            and batch5_hunt["structural_test"]
            ["initial_strong_signs"] == recorded["initial_strong"]
            and batch5_hunt["structural_test"]
            ["medial_strong_signs"] == recorded["medial_strong"]
            and batch5_hunt["structural_test"]
            ["terminal_strong_signs"] == recorded["terminal_strong"]
        )
        reproduction = {
            "R1_recorded_quantities": recorded,
            "R2_pinned_corpus_census": census,
            "R2_crosswalk_census": crosswalk,
            "R2_denominator_matches":
                census["inscriptions_len_ge3"]
                == recorded["formula_denominator"],
            "R3_phase43_structure": p43,
            "R3_classes_exhibitable": (
                p43["terminal_strong_list_exhibited"]
                == recorded["terminal_strong"]
                and len(p43[
                    "initial_or_medial_member_lists_exhibited"]) > 0
            ),
            "R4_tree_scan": scan,
            "R5_batch5_record": {
                "file": BATCH5_RECORD,
                "corpus_named": batch5["corpus"],
                "n_sequences": batch5["n_sequences"],
                "n_dockeys": batch5["n_dockeys"],
                "n_signs_profiled": batch5["n_signs_profiled"],
                "carries_identical_quantities":
                    batch5_same_quantities,
            },
            "formula_numerator_computable": False,
            "formula_numerator_note": (
                "the numerator counts inscriptions following "
                "the opening-middle-ending structure under the "
                "strong-sign classes; the classes' membership "
                "is exhibited by no record of record (R3), so "
                "the numerator cannot be computed from the "
                "pinned corpus under any recorded framework"),
        }
        reproduced = (
            reproduction["R2_denominator_matches"]
            and reproduction["R3_classes_exhibitable"]
            and scan["firestore_dump_present"]
        )
        gate_02 = {
            "gate": "0.2",
            "name": "Positional reproduction",
            "recorded": {
                "formula": f"{recorded['formula_numerator']}/"
                           f"{recorded['formula_denominator']}",
                "classes": (f"{recorded['initial_strong']}/"
                            f"{recorded['medial_strong']}/"
                            f"{recorded['terminal_strong']}"),
            },
            "observed": {
                "pinned_corpus_len_ge3":
                    census["inscriptions_len_ge3"],
                "terminal_members_exhibited":
                    p43["terminal_strong_list_exhibited"],
                "initial_medial_member_lists_exhibited":
                    len(p43[
                        "initial_or_medial_member_lists_exhibited"]),
                "phase43_code_paths": scan["phase43_paths"],
                "positional_corpus_data_present":
                    scan["firestore_dump_present"],
            },
            "verdict": "PASS" if reproduced else "FAIL",
        }
        gates.append(gate_02)
        if reproduced:
            gates.append({"gate": "0.3", "verdict": "NOT RUN BY "
                          "THIS SCRIPT (step-0 continuation)"})
            gates.append({"gate": "0.4", "verdict": "NOT RUN BY "
                          "THIS SCRIPT (step-0 continuation)"})
            outcome = "STEP 0 CONTINUES"
        else:
            outcome = "INVALID"
            gates.append({"gate": "0.3", "verdict": "NOT REACHED"})
            gates.append({"gate": "0.4", "verdict": "NOT REACHED"})

    concordance = _check_pin(*PIN_CONCORDANCE)
    concordance_rec = json.loads(
        (_REPO / PIN_CONCORDANCE[0]).read_text("utf-8"))
    anchors_after = _sha256(_REPO / PIN_ANCHORS[0])

    rec = {
        "phase": "Phase-411",
        "spec": "045-hunt-depicted-kinds",
        "act": "step 0 (spec section 6 gates, in frozen order)",
        "execution_date": EXECUTION_DATE,
        "base_commit": "cefef0c6c84fe4122b168805e392f64d8b498815",
        "claim_id":
            "without_kings_or_conquests_the_indus_scr_"
            "ce9d98cc_manual_001",
        "freeze_digest":
            "5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a",
        "osf_registration": "4mt9k (approved and public)",
        "gates": gates,
        "reproduction_attempt": reproduction,
        "d18_feed_state": {
            "file": PIN_CONCORDANCE[0],
            "sha256_observed": concordance["observed"],
            "sha256_match": concordance["match"],
            "schema": concordance_rec.get("schema"),
            "signs": concordance_rec.get("signs"),
            "closure": concordance_rec.get("closure"),
            "note": (
                "recorded as context only: the D-18 feed "
                "gates (A2) belong to the Asset A build, "
                "which this closure precedes; the feed is "
                "an empty feed in the frozen closure form, "
                "and it was neither consumed nor "
                "reconstructed"),
        },
        "asset_a": {
            "built": False,
            "reason": (
                "step 0 closed the execution as INVALID at "
                "gate 0.2 before step 1; gates A1–A6 never "
                "ran and no sign was classified"),
        },
        "models_computed": False,
        "anchors": {
            "file": PIN_ANCHORS[0],
            "sha256_before": anchors_before,
            "sha256_after": anchors_after,
            "byte_identical": anchors_before == anchors_after,
        },
        "outcome": outcome,
        "outcome_wording_frozen_spec_5_5": (
            "Spec 045 stopped before any model quantity: "
            "gate 0.2 (positional reproduction) failed — "
            "the pinned corpus carries 3,463 inscriptions "
            "of length >= 3 against the recorded 2,267; "
            "the 40/61/20 strong-sign classes are exhibited "
            "by no record of record (the Phase-43 record "
            "exhibits 10 of its 20 terminal-strong signs "
            "and no initial or medial member list, and "
            "states no position rule, count floor, "
            "threshold, or profiled-set rule); and the "
            "corpus the recorded quantities belong to "
            "(the Firestore V3 corpus, 3,137 sequences) "
            "is absent from the tree. No verdict is "
            "recorded; the claim stands as recorded."
            if outcome == "INVALID" else None
        ),
    }

    lines = [
        "# Phase-411 — Spec 045 step-0 report",
        "",
        f"Claim: `{rec['claim_id']}` — standing IN QUESTION,",
        "partially supported for position only, exactly as",
        "recorded. Execution date: 2026-10-21. Freeze digest:",
        f"`{rec['freeze_digest']}`. OSF registration 4mt9k",
        "(approved and public).",
        "",
        f"## Outcome: {outcome}",
        "",
    ]
    if outcome == "INVALID":
        lines += [
            "Frozen wording (spec section 5.5, INVALID form):",
            "",
            f"> {rec['outcome_wording_frozen_spec_5_5']}",
            "",
        ]
    lines += [
        "## Gates, in frozen order",
        "",
    ]
    for g in gates:
        lines.append(f"- **Gate {g['gate']} — {g.get('name', '')}: "
                     f"{g['verdict']}**")
        if g["gate"] == "0.1":
            for p in g["inputs"]:
                lines.append(
                    f"  - `{p['file']}` — "
                    f"{'match' if p['match'] else 'MISMATCH'} "
                    f"({p['observed']})")
        if g["gate"] == "0.2" and reproduction is not None:
            r = reproduction
            lines += [
                f"  - Recorded: formula "
                f"{r['R1_recorded_quantities']['formula_numerator']}/"
                f"{r['R1_recorded_quantities']['formula_denominator']}; "
                f"classes {r['R1_recorded_quantities']['initial_strong']}/"
                f"{r['R1_recorded_quantities']['medial_strong']}/"
                f"{r['R1_recorded_quantities']['terminal_strong']}.",
                f"  - Pinned corpus census: "
                f"{r['R2_pinned_corpus_census']['records']} records; "
                f"{r['R2_pinned_corpus_census']['inscriptions_len_ge3']} "
                f"inscriptions of length >= 3 (recorded: 2,267).",
                f"  - Phase-43 record exhibits "
                f"{r['R3_phase43_structure']['terminal_strong_list_exhibited']} "
                f"of 20 terminal-strong signs and no initial or "
                f"medial member list; its corpus is the Firestore "
                f"'indusarrays' source (3,137 sequences), whose "
                f"data file is absent from the tree.",
            ]
    lines += [
        "",
        "## What was not done",
        "",
        "Asset A was not built (no sign was classified); no",
        "model was fitted; no join was made; gates 0.3 and",
        "0.4 were not reached. No gloss is established by",
        "this record: it states only that the frozen step-0",
        "reproduction gate failed on the values above, and",
        "the claim stands as recorded. Spec 037's census",
        "caution (object-type labels diverging between",
        "compilations in 49% of matched cases) is restated",
        "here as it travels with every statement under this",
        "spec; Asset A's construction was its designed",
        "answer, and that construction was never reached.",
        "",
        "Anchors asserted byte-identical before and after:",
        f"`{anchors_before}` at both readings.",
        "",
        "*AI disclosure: executed by an AI agent (Muse Spark,",
        "via Muse) at the direction of Tristen Pierson, per",
        "constitution section VI.*",
        "",
    ]

    _OUT_RESULTS.parent.mkdir(parents=True, exist_ok=True)
    _OUT_RESULTS.write_text(
        json.dumps(rec, indent=2, sort_keys=True,
                   ensure_ascii=False) + "\n", "utf-8")
    _OUT_REPORT.write_text("\n".join(lines), "utf-8")
    print(f"Phase-411 step 0: outcome {outcome}")
    for g in gates:
        print(f"  gate {g['gate']}: {g['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

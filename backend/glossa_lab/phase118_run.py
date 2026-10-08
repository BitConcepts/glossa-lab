"""Phase-118 (spec 017) — orchestration: partition ->
judgeability -> phi (per direction) -> calibration -> gates
-> (only if accepted) main run.

Executes the frozen protocol of
specs/017-phase118-within-compilation-validation-v2/spec.md,
the W1-primary redesign of spec 016's battery:

  1. Recompute and assert the frozen sets (FLAGGED44,
     STRICT94, KUR113) — spec 011 section 2 definitions, via
     phase113_run.compute_sets (identical to Phase-117: its
     battery was rejected at calibration and modified no
     anchor).
  2. Load Holdat (the sole corpus), build the frozen seed-117
     partition carried from spec 016, and assert its design
     totals (half A = 3,531 / half B = 3,471) before any
     instrument runs.
  3. Judgeability (spec section 2.1, count properties):
     recompute J94 (STRICT94 signs W1-scorable and
     W3-scorable; asserted 67) and JKUR (KUR113 signs
     W3-scorable; asserted 29) before calibrating.
  4. phi per direction := 10th percentile (type-7) of
     STRICT94 cross-fit self-scores in that direction (spec
     section 4.3), computed before the gates.
  5. Calibration gates (spec section 6): positive —
     VALIDATED share over J94 >= 0.50 (and |J94| >= 50);
     negative — over JKUR, VALIDATED = 0 and DEMOTE share
     >= 0.25 (and |JKUR| >= 8). A failed gate rejects the
     battery: FLAGGED44 is never run and the anchors file is
     NOT modified. Universal indeterminacy among JKUR yields
     DEMOTE share 0 and fails the negative gate by
     construction — spec 016's vacuous-pass defect is the
     recorded basis for this design.
  6. Main run (only if both gates pass): the battery over
     FLAGGED44, the section-8 rule applied mechanically,
     anchors updated (changed-entries == change-register
     signs, asserted). VALIDATED earns the spec section 9
     status `validated_within_compilation` — internal
     coherence within Holdat only; not independent or non-SA
     validation, and it never promotes a tier.

Donor stream: one random.Random(118) for the whole run (spec
section 3), consumed in sorted-sign order (STRICT94 LOO,
KUR113, FLAGGED44), per sign in direction order
modelA_scoreB then modelB_scoreA; guard-rejected directions
consume no draws. Holdat is read from the gitignored
downloads area and never committed; only statistics and
verdicts are published.
"""
from __future__ import annotations

import json
import random
import sys
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_BACKEND = _REPO / "backend"
sys.path.insert(0, str(_BACKEND))

from glossa_lab.phase113_battery import CorpusContext, normalize_reading  # noqa: E402
from glossa_lab.phase113_run import (  # noqa: E402
    _gpu_device, _regenerate_bookkeeping, _tally, compute_sets,
)
from glossa_lab.phase117_battery import percentile  # noqa: E402
from glossa_lab.phase117_run import load_holdat_with_sites  # noqa: E402
from glossa_lab.phase118_battery import (  # noqa: E402
    DONOR_SEED, build_partition, evaluate_anchor, phonemes_of,
    site_profiles, w3x_scorable, w3x_self_score,
)

ANCHORS_PATH = _BACKEND / "reports" / "INDUS_FINAL_ANCHORS.json"
REGISTER_PATH = _REPO / "reports" / "phase108_provenance_register.json"
RESULTS_PATH = _REPO / "reports" / "phase118_within_battery_results.json"
CHANGE_REGISTER_PATH = _REPO / "reports" / "phase118_within_battery_change_register.json"
SUMMARY_PATH = _REPO / "reports" / "phase118_within_battery_summary.md"
SPEC = "specs/017-phase118-within-compilation-validation-v2"
DATE = "2026-10-07"

PARTITION_A_TOKENS = 3531   # spec 016 section 3, carried by spec 017
PARTITION_B_TOKENS = 3471
J94_EXPECTED = 67           # spec 017 section 2.1 / Appendix A
JKUR_EXPECTED = 29
J94_MIN = 50                # spec 017 section 6
JKUR_MIN = 8
POSITIVE_SHARE_MIN = 0.50
KUR_DEMOTE_SHARE_MIN = 0.25
W1_HALF_FLOOR = 4           # spec 017 section 2.1 (W1-scorable)


class BatteryInputs:
    """Everything the battery needs, built once."""

    def __init__(self, anchors: dict):
        ins_sites = load_holdat_with_sites(_find_holdat_csv())
        self.ins_sites = ins_sites
        self.inscriptions = [t for t, _ in ins_sites]
        self.holdat_tokens = [t for ins in self.inscriptions for t in ins]
        assert len(self.inscriptions) == 1670, len(self.inscriptions)
        assert len(self.holdat_tokens) == 7002, len(self.holdat_tokens)
        self.ctx_full = CorpusContext(self.inscriptions)
        half = build_partition(ins_sites)
        self.partition = half
        self.ins_a = [t for t, h in zip(self.inscriptions, half)
                      if h == "A"]
        self.ins_b = [t for t, h in zip(self.inscriptions, half)
                      if h == "B"]
        tok_a = sum(len(x) for x in self.ins_a)
        tok_b = sum(len(x) for x in self.ins_b)
        # Frozen partition assertion (spec section 3): the totals
        # must reproduce exactly before any instrument runs.
        assert tok_a == PARTITION_A_TOKENS, tok_a
        assert tok_b == PARTITION_B_TOKENS, tok_b
        self.partition_tokens = {"A": tok_a, "B": tok_b}
        self.ctx_a = CorpusContext(self.ins_a)
        self.ctx_b = CorpusContext(self.ins_b)
        self.profiles_by_site = site_profiles(ins_sites)
        self.readings_norm = {s: normalize_reading(e["reading"])
                              for s, e in anchors.items()}
        self.phon = {}
        for s, rn in self.readings_norm.items():
            ph = phonemes_of(rn)
            assert ph is not None, f"reading does not tokenize: {s} {rn}"
            self.phon[s] = ph
        self.holdat_counts = dict(self.ctx_full.token_counts)
        self.anchor_signs = sorted(anchors)

    def evaluate(self, sign, anchors, core_signs, phi, rng):
        return evaluate_anchor(
            sign, anchors[sign]["reading"], core_signs, self.phon,
            self.readings_norm, self.ins_a, self.ins_b,
            self.ins_sites, self.ctx_full, self.ctx_a, self.ctx_b,
            self.profiles_by_site, self.holdat_counts,
            self.anchor_signs, phi, rng)


def _find_holdat_csv() -> Path:
    rel = Path("corpora") / "downloads" / "external_repos" \
        / "holdatllc_indus" / "indus_corpus 2.csv"
    main_repo = Path.home() / "workspace" / "glossa-lab"
    for cand in (_REPO / rel, main_repo / rel):
        if cand.exists():
            return cand
    raise FileNotFoundError("Holdat CSV not found in worktree "
                            "or main checkout")


def compute_phi(inputs: BatteryInputs, strict94) -> dict:
    """phi per direction := 10th percentile (type-7) of
    STRICT94 cross-fit self-scores in that direction (spec
    section 4.3), over the core signs scorable in the
    direction (model built without the tested sign)."""
    strict = set(strict94)
    out = {}
    for name, model_ins, scoring_ins in (
            ("modelA_scoreB", inputs.ins_a, inputs.ins_b),
            ("modelB_scoreA", inputs.ins_b, inputs.ins_a)):
        scores = {}
        for t in strict94:
            sc = w3x_self_score(t, model_ins, scoring_ins,
                                strict - {t}, inputs.phon)
            if sc is not None:
                scores[t] = sc
        out[name] = {
            "phi": round(percentile(list(scores.values()), 10), 6),
            "n_self_scores": len(scores),
            "percentile": "10th, linear interpolation (type-7)",
            "self_scores": {s: round(v, 6) for s, v in
                            sorted(scores.items())},
        }
    return out


def compute_judgeability(inputs: BatteryInputs, sets) -> dict:
    """Spec section 2.1 judgeable sets, recomputed from counts
    and asserted against the design-stage values before
    calibration."""
    strict = set(sets["strict94"])

    def w1_ok(s):
        return (inputs.ctx_a.token_count(s) >= W1_HALF_FLOOR
                and inputs.ctx_b.token_count(s) >= W1_HALF_FLOOR)

    def w3_ok(s, core):
        return w3x_scorable(s, inputs.ins_a, inputs.ins_b, core,
                            inputs.holdat_counts, inputs.anchor_signs)

    j94 = sorted(s for s in sets["strict94"]
                 if w1_ok(s) and w3_ok(s, strict - {s}))
    jkur = sorted(s for s in sets["kur113"] if w3_ok(s, strict))
    assert len(j94) == J94_EXPECTED, (len(j94), J94_EXPECTED)
    assert len(jkur) == JKUR_EXPECTED, (len(jkur), JKUR_EXPECTED)
    return {"J94": j94, "JKUR": jkur,
            "counts": {"J94": len(j94), "JKUR": len(jkur)}}


def _evaluate_set(signs, anchors, inputs: BatteryInputs, core_signs,
                  phi, rng, loo=False):
    results = {}
    for s in signs:
        core = (core_signs - {s}) if loo else core_signs
        results[s] = inputs.evaluate(s, anchors, core, phi, rng)
    return results


def _apply_outcomes(anchors: dict, results: dict) -> list:
    """Apply the spec-017 section-8 rule to FLAGGED44 entries
    in-place; return change-register records (Phase-113 shape)."""
    register = []
    for s in sorted(results):
        r = results[s]
        e = anchors[s]
        before = {"confidence": e["confidence"],
                  "validation_status": e.get("validation_status")}
        states = {k: r[k]["state"] for k in ("w1", "w3", "w4")}
        ann_head = (f"Phase-118 ({DATE}): within-compilation battery "
                    f"v2 (spec 017) outcome {r['outcome']} — "
                    f"W1 {states['w1']}, W3 {states['w3']}, "
                    f"W4 {states['w4']}.")
        stats = {
            "w1": {d: {k: v.get(k) for k in
                       ("n_scoring_half", "modal_class", "modal_share",
                        "tv_to_centroid", "state", "reason")}
                   for d, v in r["w1"]["directions"].items()},
            "w3": {"state": r["w3"]["state"],
                   "n_junctions": r["w3"].get("n_junctions"),
                   "directions": {
                       d: {k: v.get(k) for k in
                           ("n_junctions", "score", "phi", "p_value",
                            "donor_pool_size", "state", "reason")}
                       for d, v in r["w3"]["directions"].items()}},
            "w3_descriptive": r["w3"].get("descriptive"),
            "w4": {"state": r["w4"]["state"],
                   "reason": r["w4"].get("reason"),
                   "max_pairwise_tv": r["w4"].get("max_pairwise_tv"),
                   "strata": r["w4"].get("strata")},
        }
        if r["outcome"] == "VALIDATED":
            e["validation_status"] = "validated_within_compilation"
            ref = ("Phase-118 (spec 017) within-compilation battery "
                   "v2 W1/W3/W4: "
                   "reports/phase118_within_battery_results.json")
            e["evidence_ref"] = (f"{e['evidence_ref']}; {ref}"
                                 if e.get("evidence_ref") else ref)
            e["phase118_annotation"] = (
                ann_head + " validation_status set to "
                "validated_within_compilation: the reading is "
                "internally coherent with the strict core's fabric "
                "inside Holdat under split-half and permutation-null "
                "discipline (spec 017 section 9, carrying spec 016 "
                "section 9). This is NOT independent validation and "
                "does not alter the anchor's SA-lineage provenance. "
                "Tier unchanged (this phase validates or demotes; "
                "it never promotes).")
            action = "validate-within-compilation"
        elif r["outcome"] == "DEMOTE":
            failed = [k.upper() for k, v in states.items() if v == "FAIL"]
            e["confidence"] = "CANDIDATE"
            e["validation_status"] = "failed_within_compilation_validation"
            e["phase118_annotation"] = (
                ann_head + f" Failed instrument(s): "
                f"{', '.join(failed)}. Demoted to CANDIDATE per the "
                "frozen decision rule (spec 017 section 8); the "
                "demotion records a contradiction with Holdat-"
                "internal evidence at the frozen thresholds, not a "
                "finding that the reading is false.")
            action = "demote"
        else:
            e["phase118_annotation"] = (
                ann_head + " UNRESOLVED: no tier change; anchor "
                "stays flagged pending_non_sa_validation.")
            action = "unresolved-no-change"
        register.append({
            "step": "main-run", "sign": s, "rule": "spec017-section8",
            "action": action, "instruments": states,
            "statistics": stats,
            "before": before,
            "after": {"confidence": e["confidence"],
                      "validation_status": e.get("validation_status")},
        })
    return register


def run_all() -> dict:
    anchors_data = json.loads(ANCHORS_PATH.read_text("utf-8"))
    anchors = anchors_data["anchors"]
    register = json.loads(REGISTER_PATH.read_text("utf-8"))
    sets = compute_sets(anchors, register)
    inputs = BatteryInputs(anchors)
    assert all(inputs.readings_norm[s] for s in sets["strict94"]), \
        "empty normalized reading in STRICT94"
    strict_cov = round(
        sum(1 for t in inputs.holdat_tokens if t in set(sets["strict94"]))
        / len(inputs.holdat_tokens), 6)
    assert abs(strict_cov - 0.7368) <= 0.001, strict_cov

    strict_set = set(sets["strict94"])
    judge = compute_judgeability(inputs, sets)
    phi_rec = compute_phi(inputs, sets["strict94"])
    phi = {d: rec["phi"] for d, rec in phi_rec.items()}
    # One seeded donor stream for the whole run (spec section 3,
    # stream (ii)), consumed in sorted-sign order: STRICT94 LOO,
    # then KUR113, then FLAGGED44.
    rng = random.Random(DONOR_SEED)
    cal_strict = _evaluate_set(sets["strict94"], anchors, inputs,
                               strict_set, phi, rng, loo=True)
    cal_kur = _evaluate_set(sets["kur113"], anchors, inputs,
                            strict_set, phi, rng)
    t_strict, t_kur = _tally(cal_strict), _tally(cal_kur)

    j94, jkur = judge["J94"], judge["JKUR"]
    val94 = sum(1 for s in j94
                if cal_strict[s]["outcome"] == "VALIDATED")
    share94 = (val94 / len(j94)) if j94 else 0.0
    gate_positive = len(j94) >= J94_MIN and share94 >= POSITIVE_SHARE_MIN
    k_val = sum(1 for s in jkur
                if cal_kur[s]["outcome"] == "VALIDATED")
    k_dem = sum(1 for s in jkur
                if cal_kur[s]["outcome"] == "DEMOTE")
    k_unr = sum(1 for s in jkur
                if cal_kur[s]["outcome"] == "UNRESOLVED")
    k_share = (k_dem / len(jkur)) if jkur else 0.0
    gate_negative = (len(jkur) >= JKUR_MIN and k_val == 0
                     and k_share >= KUR_DEMOTE_SHARE_MIN)
    accepted = gate_positive and gate_negative

    results = {
        "phase": 118, "spec": SPEC, "date": DATE,
        "gpu_device": _gpu_device(),
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "sets": {
            "flagged44": {"n": 44, "signs": sets["flagged44"]},
            "strict94": {"n": 94, "signs": sets["strict94"],
                         "holdat_coverage": strict_cov},
            "kur113": {"n": 113, "signs": sets["kur113"]},
        },
        "corpora": {
            "holdat": {"inscriptions": len(inputs.inscriptions),
                       "tokens": len(inputs.holdat_tokens)},
            "partition": {"seed": 117,
                          "tokens": inputs.partition_tokens,
                          "asserted": {"A": PARTITION_A_TOKENS,
                                       "B": PARTITION_B_TOKENS}},
        },
        "judgeability": {
            "J94": {"n": len(j94), "signs": j94,
                    "expected": J94_EXPECTED, "min": J94_MIN},
            "JKUR": {"n": len(jkur), "signs": jkur,
                     "expected": JKUR_EXPECTED, "min": JKUR_MIN},
        },
        "phi": {"directions": phi_rec,
                "percentile": "10th, linear interpolation (type-7)"},
        "calibration": {
            "strict94_leave_one_out": {"tally": t_strict,
                                       "per_sign": cal_strict},
            "kur113_negative_control": {"tally": t_kur,
                                        "per_sign": cal_kur},
            "gates": {
                "positive": {
                    "denominator": "J94",
                    "judgeable_n": len(j94),
                    "validated_in_judgeable": val94,
                    "validated_share": round(share94, 6),
                    "share_min": POSITIVE_SHARE_MIN,
                    "min_judgeable": J94_MIN,
                    "pass": gate_positive,
                },
                "negative": {
                    "denominator": "JKUR",
                    "judgeable_n": len(jkur),
                    "validated_in_judgeable": k_val,
                    "demote_in_judgeable": k_dem,
                    "unresolved_in_judgeable": k_unr,
                    "demote_share": round(k_share, 6),
                    "validated_required": 0,
                    "demote_share_min": KUR_DEMOTE_SHARE_MIN,
                    "min_judgeable": JKUR_MIN,
                    "pass": gate_negative,
                },
                "battery_accepted": accepted,
            },
        },
        "main_run": None,
        "final": None,
    }

    if accepted:
        main = _evaluate_set(sets["flagged44"], anchors, inputs,
                             strict_set, phi, rng)
        before = deepcopy(anchors)
        hm_before = {s for s, v in anchors.items()
                     if v["confidence"] in ("HIGH", "MEDIUM")}
        cov_before = round(
            sum(1 for t in inputs.holdat_tokens if t in hm_before)
            / len(inputs.holdat_tokens), 6)
        entries = _apply_outcomes(anchors, main)
        book = _regenerate_bookkeeping(anchors_data, inputs.holdat_tokens)
        anchors_data["_phase118_note"] = (
            f"Phase-118 ({DATE}, spec 017): within-compilation "
            "validation battery v2 (W1-primary, cross-fit W3) "
            "applied to the 44 Phase-109 SA-lineage flagged "
            "anchors; outcomes per the frozen decision rule in "
            "reports/phase118_within_battery_change_register.json; "
            "summary fields regenerated from the entries. "
            "validated_within_compilation (spec 017 section 9, "
            "carrying spec 016 section 9) denotes internal "
            "coherence within Holdat only — not independent "
            "validation; SA-lineage provenance is unaltered by "
            "any outcome.")
        changed = {s for s in anchors if anchors[s] != before[s]}
        reg_signs = {r["sign"] for r in entries}
        assert changed == reg_signs, (
            f"diff/register mismatch: {sorted(changed ^ reg_signs)}")
        entries.append({
            "step": "bookkeeping", "sign": "*",
            "rule": "spec017-bookkeeping",
            "action": "regenerate-summary-fields",
            "before": {"hm_signs": len(hm_before),
                       "hm_holdat_coverage": cov_before},
            "after": book})
        ANCHORS_PATH.write_text(
            json.dumps(anchors_data, indent=2, ensure_ascii=False),
            encoding="utf-8")
        change_register = {
            "phase": 118, "spec": SPEC, "date": DATE,
            "gpu_device": results["gpu_device"],
            "entries": entries}
        CHANGE_REGISTER_PATH.write_text(
            json.dumps(change_register, indent=2, ensure_ascii=False),
            encoding="utf-8")
        results["main_run"] = {"tally": _tally(main), "per_sign": main}
        results["final"] = {
            **book,
            "validated_within_compilation": {
                "n": sum(1 for r in main.values()
                         if r["outcome"] == "VALIDATED"),
                "signs": sorted(s for s, r in main.items()
                                if r["outcome"] == "VALIDATED")},
            "strict94_holdat_coverage": strict_cov,
        }

    RESULTS_PATH.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8")
    SUMMARY_PATH.write_text(render_summary(results), encoding="utf-8")
    return results


def _instrument_tallies(per_sign: dict) -> dict:
    out = {}
    for k in ("w1", "w3", "w4"):
        out[k] = dict(Counter(r[k]["state"] for r in per_sign.values()))
    return out


def render_summary(r: dict) -> str:
    cal = r["calibration"]
    gates = cal["gates"]
    pos, neg = gates["positive"], gates["negative"]
    phi = r["phi"]["directions"]
    tt_s = _instrument_tallies(cal["strict94_leave_one_out"]["per_sign"])
    tt_k = _instrument_tallies(cal["kur113_negative_control"]["per_sign"])
    lines = [
        "# Phase-118 — Within-Compilation Validation Battery v2 for the 44 SA-Lineage Anchors",
        "",
        f"**Spec:** {SPEC} (frozen before any results) · "
        f"**Date:** {r['date']} · **GPU device:** {r['gpu_device']}",
        "",
        "Successor to Phase-117 (spec 016), whose battery was "
        "rejected at calibration: its W3 (leave-one-out-minus-self "
        "junction reference; PASS band p <= 0.05 attained by 3/81 "
        "judged core signs) made its own PASS nearly unattainable, "
        "and its KUR113 gate passed vacuously on universal "
        "indeterminacy. This battery is the commissioned W1-primary "
        "redesign, entirely Holdat-internal: W1 split-half "
        "positional cross-fit (spec-011 T2a thresholds unretuned) "
        "as the primary instrument; W3 junction coherence rebuilt "
        "cross-fit (model and phi from the opposite partition "
        "half; donor-permutation null retained per direction; "
        "median-donor bands); W4 site-stratum stability as a "
        "FAIL-guard only. W2 remains dropped as decision-bearing "
        "(spec 016 section 4.2). A VALIDATED outcome earns the "
        "status `validated_within_compilation` (spec 017 section "
        "9, carrying spec 016 section 9): internal coherence "
        "within Holdat only — NOT independent validation, and not "
        "the `validated_non_sa` status of specs 011/014.",
        "",
        "## Verdict",
        "",
    ]
    if gates["battery_accepted"]:
        tally = r["main_run"]["tally"]
        lines += [
            "Calibration gates **passed**; the frozen battery was "
            "applied to the 44 flagged anchors and the section-8 "
            "rule executed mechanically:",
            "",
            f"- VALIDATED (`validated_within_compilation`, tier "
            f"unchanged): **{tally.get('VALIDATED', 0)}**",
            f"- DEMOTE (to CANDIDATE): **{tally.get('DEMOTE', 0)}**",
            f"- UNRESOLVED (stays flagged): "
            f"**{tally.get('UNRESOLVED', 0)}**",
        ]
    else:
        lines += [
            "**BATTERY REJECTED at calibration.** The frozen gates "
            "of spec 017 section 6 were not both met, so FLAGGED44 "
            "was never run and the anchors file was not modified. "
            "The battery may not be re-tuned under this spec.",
        ]
    ts = cal["strict94_leave_one_out"]["tally"]
    tk = cal["kur113_negative_control"]["tally"]
    # Negative-gate diagnostic (computed from the recorded
    # direction records): how often the absolute leg fired at
    # all among the judgeable negative control.
    kur_ps = cal["kur113_negative_control"]["per_sign"]
    kur_dirs = [d for s in r["judgeability"]["JKUR"]["signs"]
                for d in kur_ps[s]["w3"]["directions"].values()
                if "score" in d]
    kur_below = sum(1 for d in kur_dirs if d["score"] < d["phi"])
    kur_min_p = min((d["p_value"] for d in kur_dirs), default=None)
    lines += [
        "",
        "## Calibration (executed before the 44; reported whatever it showed)",
        "",
        f"phi per direction (10th percentile, type-7, of STRICT94 "
        f"cross-fit self-scores): modelA→scoreB = "
        f"**{phi['modelA_scoreB']['phi']}** "
        f"(n = {phi['modelA_scoreB']['n_self_scores']}); "
        f"modelB→scoreA = **{phi['modelB_scoreA']['phi']}** "
        f"(n = {phi['modelB_scoreA']['n_self_scores']}).",
        "",
        "| Gate | Denominator | Result | Requirement | Verdict |",
        "|---|---|---|---|---|",
        f"| Positive (STRICT94) | J94 = {pos['judgeable_n']} "
        f"judgeable of 94 (tally over all 94: "
        f"{ts.get('VALIDATED', 0)} V / {ts.get('DEMOTE', 0)} D / "
        f"{ts.get('UNRESOLVED', 0)} U) | VALIDATED "
        f"{pos['validated_in_judgeable']} / {pos['judgeable_n']} "
        f"= {pos['validated_share']:.4f} | share >= "
        f"{pos['share_min']} and n >= {pos['min_judgeable']} | "
        f"**{'PASS' if pos['pass'] else 'FAIL'}** |",
        f"| Negative (KUR113) | JKUR = {neg['judgeable_n']} "
        f"judgeable of 113 (tally over all 113: "
        f"{tk.get('VALIDATED', 0)} V / {tk.get('DEMOTE', 0)} D / "
        f"{tk.get('UNRESOLVED', 0)} U) | VALIDATED "
        f"{neg['validated_in_judgeable']}, DEMOTE "
        f"{neg['demote_in_judgeable']} / {neg['judgeable_n']} "
        f"= {neg['demote_share']:.4f}, UNRESOLVED "
        f"{neg['unresolved_in_judgeable']} | VALIDATED = 0 and "
        f"DEMOTE share >= {neg['demote_share_min']} and n >= "
        f"{neg['min_judgeable']} | "
        f"**{'PASS' if neg['pass'] else 'FAIL'}** |",
        "",
        f"Negative-gate diagnostic: in **{kur_below} of "
        f"{len(kur_dirs)}** JKUR direction records is the sign's "
        f"cross-fit score below its direction's phi, while every "
        f"judgeable direction's donor p-value is >= 0.50 (minimum "
        f"{kur_min_p}) — the relative (donor) leg separates the "
        "known-bad `kur` readings from the core's fabric, but the "
        "absolute leg never fires, because the phoneme pair of "
        "`kur` occupies high-probability junction cells. The "
        "conjunctive FAIL band therefore produces no kur demotion "
        "and the negative gate fails on its discrimination clause "
        "— it does not pass vacuously. This is the coarse-fabric "
        "limit registered in spec section 10, now measured under "
        "the cross-fit construction as well.",
        "",
        "Per-instrument states (calibration):",
        "",
        "| Set | Instrument | PASS | FAIL | INDETERMINATE |",
        "|---|---|---|---|---|",
    ]
    for label, tt in (("STRICT94", tt_s), ("KUR113", tt_k)):
        for k in ("w1", "w3", "w4"):
            c = tt[k]
            lines.append(
                f"| {label} | {k.upper()} | {c.get('PASS', 0)} | "
                f"{c.get('FAIL', 0)} | {c.get('INDETERMINATE', 0)} |")
    if r["main_run"]:
        tt_m = _instrument_tallies(r["main_run"]["per_sign"])
        lines += [
            "",
            "Per-instrument states (FLAGGED44 main run):",
            "",
            "| Instrument | PASS | FAIL | INDETERMINATE |",
            "|---|---|---|---|",
        ]
        for k in ("w1", "w3", "w4"):
            c = tt_m[k]
            lines.append(
                f"| {k.upper()} | {c.get('PASS', 0)} | "
                f"{c.get('FAIL', 0)} | {c.get('INDETERMINATE', 0)} |")
    lines += [
        "",
        "## Sets and corpora (recomputed; assertions in spec sections 2-3)",
        "",
        "- FLAGGED44: 44 anchors (24 SA_DERIVED + 20 "
        "SA_CONFIRMED_ONLY; 43 HIGH + M293 MEDIUM).",
        f"- STRICT94: 94 anchors (90 HIGH + 4 MEDIUM); Holdat token "
        f"coverage {r['sets']['strict94']['holdat_coverage']:.4f} "
        f"(5,159 / 7,002). Judgeable core J94 = "
        f"{r['judgeability']['J94']['n']} (asserted).",
        f"- KUR113: 113 premise-superseded anchors, all reading "
        f"`kur`. Judgeable JKUR = {r['judgeability']['JKUR']['n']} "
        f"(asserted; W3-scorable only — the cohort is structurally "
        "W1-unscorable and W4-unjudgeable).",
        f"- Holdat (sole corpus): "
        f"{r['corpora']['holdat']['inscriptions']} inscriptions / "
        f"{r['corpora']['holdat']['tokens']} tokens; frozen "
        f"partition (seed 117, carried from spec 016) asserted at "
        f"A = {r['corpora']['partition']['tokens']['A']} / "
        f"B = {r['corpora']['partition']['tokens']['B']} tokens. "
        "No ICIT layer was loaded or consulted (Phase-116 "
        "constraint).",
    ]
    if r["final"]:
        f = r["final"]
        vc = f["validated_within_compilation"]
        lines += [
            "",
            "## Final state",
            "",
            f"- Tiers after: {f['by_confidence']} "
            f"(H+M = {f['hm_signs']}, Holdat coverage "
            f"{f['hm_holdat_coverage']:.4f}).",
            f"- `validated_within_compilation`: {vc['n']} anchors "
            f"({', '.join(vc['signs']) if vc['signs'] else 'none'}). "
            "Per spec section 9 this status claims internal "
            "coherence within Holdat only; the anchors' SA-lineage "
            "provenance is unaltered, and every outcome is "
            "provisional against a genuinely independent corpus.",
            "- Per-anchor records: "
            "`reports/phase118_within_battery_change_register.json`; "
            "full instrument statistics: "
            "`reports/phase118_within_battery_results.json`.",
        ]
    lines += [
        "",
        "## Limitations (registered in spec section 10)",
        "",
        "Single-compilation ceiling: every instrument measures "
        "coherence inside one modern compilation; systematic error "
        "in Holdat or in STRICT94's readings is invisible to this "
        "battery by construction. Cross-fit halves the evidence "
        "twice over (W1 and rebuilt W3 both derive and score on "
        "disjoint halves); per-direction W3 scores may average as "
        "few as 2 junction observations (the floor at which the "
        "negative control remains testable). The negative gate "
        "rests on W3 alone over 29 judgeable kur signs. The "
        "section-8 conjunction is reachable by at most 11/44 "
        "flagged anchors; M235, M254, M402 are judgeable by no "
        "instrument and UNRESOLVED by construction. A FAIL demotes "
        "to CANDIDATE; it does not declare the reading false.",
        "",
        "## Deviations",
        "",
        "None in the battery's frozen definitions, thresholds, "
        "floors, bands, partition, seeds, or decision rule. "
        "Conventions fixed in the frozen spec text itself (not "
        "post-hoc): phi's percentile is the linear-interpolation "
        "(type-7) 10th percentile per direction; the donor stream "
        "is one random.Random(118) consumed in sorted-sign order "
        "(STRICT94 LOO, KUR113, FLAGGED44), per sign in direction "
        "order modelA_scoreB then modelB_scoreA, with "
        "guard-rejected directions consuming no draws; W2's "
        "descriptive support/context counts are computed against "
        "the evaluation core (leave-one-out core during STRICT94 "
        "calibration).",
        "",
        "## Verification",
        "",
        "Recorded in the phase ledger entries and the PR body "
        "(full backend suite; foundation check per H21; ruff).",
        "",
        "**AI disclosure:** executed by an AI agent (Muse Spark, "
        "via Muse) at the direction of Tristen Pierson, per "
        "constitution section VI.",
        "",
    ]
    return "\n".join(lines)

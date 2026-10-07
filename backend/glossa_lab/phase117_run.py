"""Phase-117 (spec 016) — orchestration: partition -> phi ->
calibration -> gate -> (only if accepted) main run.

Executes the frozen protocol of
specs/016-phase117-within-compilation-validation/spec.md:

  1. Recompute and assert the frozen sets (FLAGGED44, STRICT94,
     KUR113) — spec 011 section 2 definitions, reused from
     phase113_run.compute_sets.
  2. Load Holdat (the sole corpus; loader machinery of
     sa_validation.load_holdat_corpus, replicated with the
     per-inscription site the partition and W4 need), build the
     frozen seed-117 partition, and assert its design totals
     (half A = 3,531 tokens / half B = 3,471) before any
     instrument runs.
  3. phi := 10th percentile of STRICT94 leave-one-out W3
     self-scores (spec section 4.3), computed before the gates.
  4. Calibration (spec section 6): STRICT94 leave-one-out must
     VALIDATE >= 47/94; KUR113 VALIDATED <= 5/113. A failed
     gate rejects the battery — FLAGGED44 is never run and the
     anchors file is NOT modified.
  5. Main run (only if calibration passes): the battery over
     FLAGGED44, the section-8 decision rule applied
     mechanically, anchors file updated (changed-entries ==
     change-register signs, asserted — the Phase-113 pattern).
     VALIDATED earns the spec section 9 status
     `validated_within_compilation` — internal coherence
     within Holdat only; it is not, and must not be reported
     as, independent or non-SA validation.

Holdat is read from the gitignored downloads area and never
committed; only statistics and verdicts are published.
"""
from __future__ import annotations

import csv
import json
import random
import sys
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_BACKEND = _REPO / "backend"
_MAIN_REPO = Path.home() / "workspace" / "glossa-lab"
sys.path.insert(0, str(_BACKEND))

from glossa_lab.phase113_battery import CorpusContext, normalize_reading  # noqa: E402
from glossa_lab.phase113_run import (  # noqa: E402
    _gpu_device, _regenerate_bookkeeping, _tally, compute_sets,
)
from glossa_lab.phase117_battery import (  # noqa: E402
    SEED, build_partition, evaluate_anchor, percentile,
    phonemes_of, site_profiles, w3_self_score,
)

ANCHORS_PATH = _BACKEND / "reports" / "INDUS_FINAL_ANCHORS.json"
REGISTER_PATH = _REPO / "reports" / "phase108_provenance_register.json"
RESULTS_PATH = _REPO / "reports" / "phase117_within_battery_results.json"
CHANGE_REGISTER_PATH = _REPO / "reports" / "phase117_within_battery_change_register.json"
SUMMARY_PATH = _REPO / "reports" / "phase117_within_battery_summary.md"
SPEC = "specs/016-phase117-within-compilation-validation"
DATE = "2026-10-07"

STRICT_VALIDATED_MIN = 47   # of 94  (spec 016 section 6)
KUR_VALIDATED_MAX = 5       # of 113 (spec 016 section 6)
PARTITION_A_TOKENS = 3531   # spec 016 section 3 / Appendix A.2
PARTITION_B_TOKENS = 3471


def _find_holdat_csv() -> Path:
    rel = Path("corpora") / "downloads" / "external_repos" \
        / "holdatllc_indus" / "indus_corpus 2.csv"
    for cand in (_REPO / rel, _MAIN_REPO / rel):
        if cand.exists():
            return cand
    raise FileNotFoundError("Holdat CSV not found in worktree "
                            "or main checkout")


def load_holdat_with_sites(csv_path: Path):
    """Replica of sa_validation.load_holdat_corpus grouping
    (loader logic only; no SA code is executed), additionally
    carrying the per-inscription site from the CSV `site` field
    (constant within a cisi_number group). Returns a list of
    (tokens, site) in loader (first-appearance) order."""
    seals: dict[str, list] = {}
    sites: dict[str, str] = {}
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = (row.get("cisi_number") or "").strip()
            p = int(row.get("position") or 0)
            if c not in seals:
                seals[c] = []
                sites[c] = (row.get("site") or "").strip()
            while len(seals[c]) <= p:
                seals[c].append("")
            seals[c][p] = s
    return [([t for t in v if t], sites[c])
            for c, v in seals.items() if any(v)]


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
        ins_a = [t for t, h in zip(self.inscriptions, half) if h == "A"]
        ins_b = [t for t, h in zip(self.inscriptions, half) if h == "B"]
        tok_a = sum(len(x) for x in ins_a)
        tok_b = sum(len(x) for x in ins_b)
        # Frozen partition assertion (spec section 3): the totals
        # must reproduce exactly before any instrument runs.
        assert tok_a == PARTITION_A_TOKENS, tok_a
        assert tok_b == PARTITION_B_TOKENS, tok_b
        self.partition_tokens = {"A": tok_a, "B": tok_b}
        self.ctx_a = CorpusContext(ins_a)
        self.ctx_b = CorpusContext(ins_b)
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
            self.readings_norm, self.inscriptions, self.ins_sites,
            self.ctx_full, self.ctx_a, self.ctx_b,
            self.profiles_by_site, self.holdat_counts,
            self.anchor_signs, phi, rng)


def compute_phi(inputs: BatteryInputs, strict94) -> dict:
    """phi := 10th percentile of STRICT94 leave-one-out W3
    self-scores (spec section 4.3), over the strict signs whose
    self-score is defined (junction floor met)."""
    strict = set(strict94)
    scores = {}
    for s in strict94:
        sc = w3_self_score(s, inputs.inscriptions, strict - {s},
                           inputs.phon)
        if sc is not None:
            scores[s] = sc
    phi = percentile(list(scores.values()), 10)
    return {"phi": round(phi, 6), "n_self_scores": len(scores),
            "percentile": "10th, linear interpolation (type-7)",
            "self_scores": {s: round(v, 6) for s, v in
                            sorted(scores.items())}}


def _evaluate_set(signs, anchors, inputs: BatteryInputs, core_signs,
                  phi, rng, loo=False):
    results = {}
    for s in signs:
        core = (core_signs - {s}) if loo else core_signs
        results[s] = inputs.evaluate(s, anchors, core, phi, rng)
    return results


def _apply_outcomes(anchors: dict, results: dict) -> list:
    """Apply the spec-016 section-8 rule to FLAGGED44 entries
    in-place; return change-register records (Phase-113 shape)."""
    register = []
    for s in sorted(results):
        r = results[s]
        e = anchors[s]
        before = {"confidence": e["confidence"],
                  "validation_status": e.get("validation_status")}
        states = {k: r[k]["state"] for k in ("w1", "w3", "w4")}
        ann_head = (f"Phase-117 ({DATE}): within-compilation battery "
                    f"(spec 016) outcome {r['outcome']} — "
                    f"W1 {states['w1']}, W3 {states['w3']}, "
                    f"W4 {states['w4']}.")
        stats = {
            "w1": {d: {k: v.get(k) for k in
                       ("n_scoring_half", "modal_class", "modal_share",
                        "tv_to_centroid", "state", "reason")}
                   for d, v in r["w1"]["directions"].items()},
            "w3": {k: r["w3"].get(k) for k in
                   ("n_junctions", "score", "phi", "p_value",
                    "donor_pool_size", "state", "reason")},
            "w3_descriptive": r["w3"].get("descriptive"),
            "w4": {"state": r["w4"]["state"],
                   "reason": r["w4"].get("reason"),
                   "max_pairwise_tv": r["w4"].get("max_pairwise_tv"),
                   "strata": r["w4"].get("strata")},
        }
        if r["outcome"] == "VALIDATED":
            e["validation_status"] = "validated_within_compilation"
            ref = ("Phase-117 (spec 016) within-compilation battery "
                   "W1/W3/W4: "
                   "reports/phase117_within_battery_results.json")
            e["evidence_ref"] = (f"{e['evidence_ref']}; {ref}"
                                 if e.get("evidence_ref") else ref)
            e["phase117_annotation"] = (
                ann_head + " validation_status set to "
                "validated_within_compilation: the reading is "
                "internally coherent with the strict core's fabric "
                "inside Holdat under split-half and permutation-null "
                "discipline (spec 016 section 9). This is NOT "
                "independent validation and does not alter the "
                "anchor's SA-lineage provenance. Tier unchanged "
                "(this phase validates or demotes; it never "
                "promotes).")
            action = "validate-within-compilation"
        elif r["outcome"] == "DEMOTE":
            failed = [k.upper() for k, v in states.items() if v == "FAIL"]
            e["confidence"] = "CANDIDATE"
            e["validation_status"] = "failed_within_compilation_validation"
            e["phase117_annotation"] = (
                ann_head + f" Failed instrument(s): "
                f"{', '.join(failed)}. Demoted to CANDIDATE per the "
                "frozen decision rule (spec 016 section 8); the "
                "demotion records a contradiction with Holdat-"
                "internal evidence at the frozen thresholds, not a "
                "finding that the reading is false.")
            action = "demote"
        else:
            e["phase117_annotation"] = (
                ann_head + " UNRESOLVED: no tier change; anchor "
                "stays flagged pending_non_sa_validation.")
            action = "unresolved-no-change"
        register.append({
            "step": "main-run", "sign": s, "rule": "spec016-section8",
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
    phi_rec = compute_phi(inputs, sets["strict94"])
    phi = phi_rec["phi"]
    # One seeded donor stream for the whole run (spec section 3,
    # stream (ii)), consumed in sorted-sign order: STRICT94 LOO,
    # then KUR113, then FLAGGED44.
    rng = random.Random(SEED)
    cal_strict = _evaluate_set(sets["strict94"], anchors, inputs,
                               strict_set, phi, rng, loo=True)
    cal_kur = _evaluate_set(sets["kur113"], anchors, inputs,
                            strict_set, phi, rng)
    t_strict, t_kur = _tally(cal_strict), _tally(cal_kur)
    gate_strict = t_strict.get("VALIDATED", 0) >= STRICT_VALIDATED_MIN
    gate_kur = t_kur.get("VALIDATED", 0) <= KUR_VALIDATED_MAX
    accepted = gate_strict and gate_kur

    results = {
        "phase": 117, "spec": SPEC, "date": DATE,
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
            "partition": {"seed": SEED,
                          "tokens": inputs.partition_tokens,
                          "asserted": {"A": PARTITION_A_TOKENS,
                                       "B": PARTITION_B_TOKENS}},
        },
        "phi": phi_rec,
        "calibration": {
            "strict94_leave_one_out": {"tally": t_strict,
                                       "per_sign": cal_strict},
            "kur113_negative_control": {"tally": t_kur,
                                        "per_sign": cal_kur},
            "gates": {
                "strict_validated_min": STRICT_VALIDATED_MIN,
                "strict_gate_pass": gate_strict,
                "kur_validated_max": KUR_VALIDATED_MAX,
                "kur_gate_pass": gate_kur,
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
        anchors_data["_phase117_note"] = (
            f"Phase-117 ({DATE}, spec 016): within-compilation "
            "validation battery applied to the 44 Phase-109 "
            "SA-lineage flagged anchors; outcomes per the frozen "
            "decision rule in "
            "reports/phase117_within_battery_change_register.json; "
            "summary fields regenerated from the entries. "
            "validated_within_compilation (spec section 9) denotes "
            "internal coherence within Holdat only — not "
            "independent validation; SA-lineage provenance is "
            "unaltered by any outcome.")
        changed = {s for s in anchors if anchors[s] != before[s]}
        reg_signs = {r["sign"] for r in entries}
        assert changed == reg_signs, (
            f"diff/register mismatch: {sorted(changed ^ reg_signs)}")
        entries.append({
            "step": "bookkeeping", "sign": "*",
            "rule": "spec016-bookkeeping",
            "action": "regenerate-summary-fields",
            "before": {"hm_signs": len(hm_before),
                       "hm_holdat_coverage": cov_before},
            "after": book})
        ANCHORS_PATH.write_text(
            json.dumps(anchors_data, indent=2, ensure_ascii=False),
            encoding="utf-8")
        change_register = {
            "phase": 117, "spec": SPEC, "date": DATE,
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
    tt_s = _instrument_tallies(cal["strict94_leave_one_out"]["per_sign"])
    tt_k = _instrument_tallies(cal["kur113_negative_control"]["per_sign"])
    lines = [
        "# Phase-117 — Within-Compilation Validation Battery for the 44 SA-Lineage Anchors",
        "",
        f"**Spec:** {SPEC} (frozen before any results) · "
        f"**Date:** {r['date']} · **GPU device:** {r['gpu_device']}",
        "",
        "Phase-116 (spec 015) returned R-NONE — no conjunctive "
        "cross-corpus positional gate on the Holdat/ICIT pair — "
        "and licensed validation within a single compilation. "
        "This battery is entirely Holdat-internal: W1 split-half "
        "positional cross-fit (spec-011 T2a thresholds unretuned), "
        "W3 junction coherence against a seeded donor-permutation "
        "null, W4 site-stratum stability. W2 (spec-011 T3) was "
        "dropped as a decision-bearing instrument at design "
        "(spec section 4.2); its statistics are recorded "
        "descriptively in the W3 records. A VALIDATED outcome "
        "earns the status `validated_within_compilation` (spec "
        "section 9): internal coherence within Holdat only — "
        "NOT independent validation, and not the "
        "`validated_non_sa` status of specs 011/014.",
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
            "of spec 016 section 6 were not both met, so FLAGGED44 "
            "was never run and the anchors file was not modified. "
            "The battery may not be re-tuned under this spec.",
        ]
    ts = cal["strict94_leave_one_out"]["tally"]
    tk = cal["kur113_negative_control"]["tally"]
    lines += [
        "",
        "## Calibration (executed before the 44; reported whatever it showed)",
        "",
        "| Set | n | VALIDATED | DEMOTE | UNRESOLVED | Gate |",
        "|---|---|---|---|---|---|",
        f"| STRICT94 (positive, leave-one-out) | 94 | "
        f"{ts.get('VALIDATED', 0)} | {ts.get('DEMOTE', 0)} | "
        f"{ts.get('UNRESOLVED', 0)} | >= 47 required: "
        f"**{'PASS' if gates['strict_gate_pass'] else 'FAIL'}** |",
        f"| KUR113 (negative control) | 113 | "
        f"{tk.get('VALIDATED', 0)} | {tk.get('DEMOTE', 0)} | "
        f"{tk.get('UNRESOLVED', 0)} | <= 5 required: "
        f"**{'PASS' if gates['kur_gate_pass'] else 'FAIL'}** |",
        "",
        f"phi (10th percentile of STRICT94 leave-one-out W3 "
        f"self-scores, n = {r['phi']['n_self_scores']}): "
        f"**{r['phi']['phi']}**.",
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
        "## Sets and corpora (recomputed; assertions in spec section 2-3)",
        "",
        "- FLAGGED44: 44 anchors (24 SA_DERIVED + 20 "
        "SA_CONFIRMED_ONLY; 43 HIGH + M293 MEDIUM).",
        f"- STRICT94: 94 anchors (90 HIGH + 4 MEDIUM); Holdat token "
        f"coverage {r['sets']['strict94']['holdat_coverage']:.4f} "
        f"(5,159 / 7,002).",
        "- KUR113: 113 premise-superseded anchors, all reading `kur`.",
        f"- Holdat (sole corpus): "
        f"{r['corpora']['holdat']['inscriptions']} inscriptions / "
        f"{r['corpora']['holdat']['tokens']} tokens; frozen "
        f"partition (seed 117) asserted at "
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
            "`reports/phase117_within_battery_change_register.json`; "
            "full instrument statistics: "
            "`reports/phase117_within_battery_results.json`.",
        ]
    lines += [
        "",
        "## Limitations (registered in spec section 10)",
        "",
        "Single-compilation ceiling: every instrument measures "
        "coherence inside one modern compilation; systematic "
        "error in Holdat or in STRICT94's readings is invisible "
        "to this battery by construction. W3 concentration: "
        "27/44 flagged anchors are judgeable by W3 alone. W1 "
        "fully judges 13/44. The negative gate is asymmetric "
        "(KUR113 is largely unjudgeable: W1 cannot PASS below 8 "
        "tokens and W4 cannot PASS below two 4-token sites, so "
        "the kur cohort structurally cannot validate; the gate "
        "verifies non-validation of the judgeable minority and "
        "the binding gate is the positive one). A FAIL demotes "
        "to CANDIDATE; it does not declare the reading false.",
        "",
        "## Deviations",
        "",
        "None in the battery's frozen definitions, thresholds, "
        "floors, bands, partition, seeds, or decision rule. "
        "Implementation conventions fixed where the spec is "
        "silent, recorded here per spec section 12: phi's "
        "percentile is the linear-interpolation (type-7) 10th "
        "percentile; W3's donor stream is one random.Random(117) "
        "consumed in sorted-sign order (STRICT94 LOO, KUR113, "
        "FLAGGED44); W2's descriptive support/context counts are "
        "computed against the evaluation core (leave-one-out core "
        "during STRICT94 calibration).",
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

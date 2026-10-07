"""Phase-115 (spec 014) — orchestration: calibration -> gate -> run.

Executes the frozen protocol of
specs/014-phase115-nonsa44-validation-v2/spec.md:

  1. Recompute and assert the frozen sets (FLAGGED44, STRICT94,
     KUR113) — definitions identical to spec 011, reused from
     phase113_run.compute_sets.
  2. Load the v2 ICIT converted layer (spec 014 section 2) and
     assert its build statistics against layer_build_meta_v2.json
     (4,531 inscriptions / 13,492 mapped tokens, frozen in spec).
  3. Calibration: battery v2 over STRICT94 (leave-one-out) and
     KUR113. Gates identical to spec 011: strict VALIDATED >=
     57/94; kur VALIDATED <= 5/113. A failed gate rejects the
     battery — the anchors file is NOT modified and FLAGGED44 is
     never run.
  4. Main run (only if calibration passes): battery v2 over
     FLAGGED44, the section-6 decision rule applied mechanically,
     anchors file updated (changed-entries == change-register
     signs, asserted — the Phase-113 pattern).

Local restricted corpora (Holdat CSV, ICIT layers) are read from
the gitignored downloads area and never committed; only
statistics and verdicts are published.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_BACKEND = _REPO / "backend"
_MAIN_REPO = Path.home() / "workspace" / "glossa-lab"
sys.path.insert(0, str(_BACKEND))

from glossa_lab.phase113_battery import (  # noqa: E402
    CoreGrammar, CorpusContext, normalize_reading,
)
from glossa_lab.phase113_run import (  # noqa: E402
    _gpu_device, _load_module_by_path, _regenerate_bookkeeping,
    _tally, compute_sets, load_holdat_inscriptions,
    load_icit_inscriptions,
)
from glossa_lab.phase115_battery import evaluate_anchor_v2  # noqa: E402

ANCHORS_PATH = _BACKEND / "reports" / "INDUS_FINAL_ANCHORS.json"
REGISTER_PATH = _REPO / "reports" / "phase108_provenance_register.json"
RESULTS_PATH = _REPO / "reports" / "phase115_nonsa44v2_results.json"
CHANGE_REGISTER_PATH = _REPO / "reports" / "phase115_nonsa44v2_change_register.json"
SUMMARY_PATH = _REPO / "reports" / "phase115_nonsa44v2_summary.md"
SPEC = "specs/014-phase115-nonsa44-validation-v2"
DATE = "2026-10-07"
SENTINEL = "UNK"

STRICT_VALIDATED_MIN = 57   # of 94  (spec 014 section 5: >= 60%)
KUR_VALIDATED_MAX = 5       # of 113 (spec 014 section 5)


def _find_downloads() -> Path:
    for cand in (_REPO / "corpora" / "downloads",
                 _MAIN_REPO / "corpora" / "downloads"):
        if (cand / "icit_fieldcady" / "icit_converted_v2.json").exists():
            return cand
    raise FileNotFoundError("corpora/downloads with v2 layer not found "
                            "in worktree or main checkout")


def _evaluate_set(signs, anchors, core_signs, readings_norm,
                  holdat, icit, is_valid_initial, ratio, loo=False):
    results = {}
    for s in signs:
        core = (core_signs - {s}) if loo else core_signs
        grammar = CoreGrammar(core, readings_norm, holdat)
        results[s] = evaluate_anchor_v2(
            s, anchors[s]["reading"], grammar, readings_norm,
            holdat, icit, is_valid_initial, ratio)
    return results


def _apply_outcomes(anchors: dict, results: dict) -> list:
    """Apply the spec-014 section-6 rule to FLAGGED44 entries
    in-place; return change-register records (Phase-113 shape)."""
    register = []
    for s in sorted(results):
        r = results[s]
        e = anchors[s]
        before = {"confidence": e["confidence"],
                  "validation_status": e.get("validation_status")}
        states = {k: r[k]["state"] for k in ("t1", "t2", "t3")}
        ann_head = (f"Phase-115 ({DATE}): non-SA battery v2 (spec 014) "
                    f"outcome {r['outcome']} — T1 {states['t1']}, "
                    f"T2 {states['t2']}, T3 {states['t3']}.")
        if r["outcome"] == "VALIDATED_NON_SA":
            e["validation_status"] = "validated_non_sa"
            ref = ("Phase-115 (spec 014) non-SA battery v2 T1+T2+T3: "
                   "reports/phase115_nonsa44v2_results.json")
            e["evidence_ref"] = (f"{e['evidence_ref']}; {ref}"
                                 if e.get("evidence_ref") else ref)
            e["phase115_annotation"] = (
                ann_head + " validation_status set to "
                "validated_non_sa with an H26 evidence reference. "
                "Tier unchanged (this phase validates or demotes; "
                "it never promotes).")
            action = "validate"
        elif r["outcome"] == "DEMOTE":
            failed = [k.upper() for k, v in states.items() if v == "FAIL"]
            e["confidence"] = "CANDIDATE"
            e["validation_status"] = "failed_non_sa_validation"
            e["phase115_annotation"] = (
                ann_head + f" Failed test(s): {', '.join(failed)}. "
                "Demoted to CANDIDATE per the frozen decision rule.")
            action = "demote"
        else:
            e["phase115_annotation"] = (
                ann_head + " No tier change; anchor stays flagged "
                "pending_non_sa_validation.")
            action = "unresolved-no-change"
        register.append({
            "step": "main-run", "sign": s, "rule": "spec014-section6",
            "action": action,
            "tests": states,
            "statistics": {
                "t1": {k: r["t1"].get(k) for k in
                       ("n_icit_tokens", "opportunity", "floor",
                        "modal_holdat", "modal_icit", "tv")},
                "t2": {k: r["t2"].get(k) for k in
                       ("n_holdat_tokens", "modal_class", "modal_share")},
                "t2a_tv": r["t2"].get("t2a", {}).get("tv_to_centroid"),
                "t3": {k: r["t3"].get(k) for k in
                       ("support", "n_contexts", "legal_fraction")}},
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
    downloads = _find_downloads()
    build_meta = json.loads(
        (downloads / "layer_build_meta_v2.json").read_text("utf-8"))
    layer_stats = build_meta["icit_v2"]
    holdat_ins = load_holdat_inscriptions(
        downloads / "external_repos" / "holdatllc_indus"
        / "indus_corpus 2.csv")
    icit_ins = load_icit_inscriptions(
        downloads / "icit_fieldcady" / "icit_converted_v2.json")
    holdat = CorpusContext(holdat_ins)
    icit = CorpusContext(icit_ins)
    # Frozen layer assertions (spec 014 section 2): the built layer
    # must be the layer the spec froze.
    sentinel_tokens = sum(1 for ins in icit_ins for t in ins
                          if t == SENTINEL)
    mapped_tokens = icit.n_tokens - sentinel_tokens
    assert icit.n_inscriptions == layer_stats["kept_inscriptions"], \
        (icit.n_inscriptions, layer_stats["kept_inscriptions"])
    assert mapped_tokens == layer_stats["kept_mapped_tokens"], \
        (mapped_tokens, layer_stats["kept_mapped_tokens"])
    assert layer_stats["kept_inscriptions"] == 4531, layer_stats
    assert layer_stats["kept_mapped_tokens"] == 13492, layer_stats
    ratio = mapped_tokens / holdat.n_tokens
    holdat_tokens = [t for ins in holdat_ins for t in ins]
    readings_norm = {s: normalize_reading(e["reading"])
                     for s, e in anchors.items()}
    assert all(readings_norm[s] for s in sets["strict94"]), \
        "empty normalized reading in STRICT94"
    p58 = _load_module_by_path(
        "phase58_phonological_gap",
        _BACKEND / "scripts" / "phase58_phonological_gap.py")
    is_valid_initial = p58.is_valid_dravidian_initial

    strict_cov = round(
        sum(1 for t in holdat_tokens if t in set(sets["strict94"]))
        / len(holdat_tokens), 6)
    assert abs(strict_cov - 0.7368) <= 0.001, strict_cov

    strict_set = set(sets["strict94"])
    cal_strict = _evaluate_set(sets["strict94"], anchors, strict_set,
                               readings_norm, holdat, icit,
                               is_valid_initial, ratio, loo=True)
    cal_kur = _evaluate_set(sets["kur113"], anchors, strict_set,
                            readings_norm, holdat, icit,
                            is_valid_initial, ratio)
    t_strict, t_kur = _tally(cal_strict), _tally(cal_kur)
    gate_strict = t_strict.get("VALIDATED_NON_SA", 0) >= STRICT_VALIDATED_MIN
    gate_kur = t_kur.get("VALIDATED_NON_SA", 0) <= KUR_VALIDATED_MAX
    accepted = gate_strict and gate_kur

    results = {
        "phase": 115, "spec": SPEC, "date": DATE,
        "gpu_device": _gpu_device(),
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "sets": {
            "flagged44": {"n": 44, "signs": sets["flagged44"]},
            "strict94": {"n": 94, "signs": sets["strict94"],
                         "holdat_coverage": strict_cov},
            "kur113": {"n": 113, "signs": sets["kur113"]},
        },
        "corpora": {
            "holdat": {"inscriptions": holdat.n_inscriptions,
                       "tokens": holdat.n_tokens},
            "icit_converted_v1_phase107": build_meta.get("icit_v1_phase107"),
            "icit_converted_v2": {
                **layer_stats,
                "sentinel_tokens_observed": sentinel_tokens,
                "sampling_ratio_r": round(ratio, 6)},
        },
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
        main = _evaluate_set(sets["flagged44"], anchors, strict_set,
                             readings_norm, holdat, icit,
                             is_valid_initial, ratio)
        before = deepcopy(anchors)
        hm_before = {s for s, v in anchors.items()
                     if v["confidence"] in ("HIGH", "MEDIUM")}
        cov_before = round(
            sum(1 for t in holdat_tokens if t in hm_before)
            / len(holdat_tokens), 6)
        entries = _apply_outcomes(anchors, main)
        book = _regenerate_bookkeeping(anchors_data, holdat_tokens)
        anchors_data["_phase115_note"] = (
            f"Phase-115 ({DATE}, spec 014): non-SA validation battery "
            "v2 applied to the 44 Phase-109 SA-lineage flagged "
            "anchors; outcomes per the frozen decision rule in "
            "reports/phase115_nonsa44v2_change_register.json; summary "
            "fields regenerated from the entries.")
        changed = {s for s in anchors if anchors[s] != before[s]}
        reg_signs = {r["sign"] for r in entries}
        assert changed == reg_signs, (
            f"diff/register mismatch: {sorted(changed ^ reg_signs)}")
        entries.append({
            "step": "bookkeeping", "sign": "*",
            "rule": "spec014-bookkeeping",
            "action": "regenerate-summary-fields",
            "before": {"hm_signs": len(hm_before),
                       "hm_holdat_coverage": cov_before},
            "after": book})
        ANCHORS_PATH.write_text(
            json.dumps(anchors_data, indent=2, ensure_ascii=False),
            encoding="utf-8")
        change_register = {
            "phase": 115, "spec": SPEC, "date": DATE,
            "gpu_device": results["gpu_device"],
            "entries": entries}
        CHANGE_REGISTER_PATH.write_text(
            json.dumps(change_register, indent=2, ensure_ascii=False),
            encoding="utf-8")
        validated_core = strict_set | {
            s for s, r in main.items()
            if r["outcome"] == "VALIDATED_NON_SA"
            and anchors[s]["confidence"] in ("HIGH", "MEDIUM")}
        results["main_run"] = {"tally": _tally(main), "per_sign": main}
        results["final"] = {
            **book,
            "validated_core_after": {
                "n_signs": len(validated_core),
                "holdat_coverage": round(
                    sum(1 for t in holdat_tokens if t in validated_core)
                    / len(holdat_tokens), 6)},
        }

    RESULTS_PATH.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8")
    SUMMARY_PATH.write_text(render_summary(results), encoding="utf-8")
    return results


def _test_tallies(per_sign: dict) -> dict:
    out = {}
    for tk in ("t1", "t2", "t3"):
        out[tk] = dict(Counter(r[tk]["state"] for r in per_sign.values()))
    return out


def render_summary(r: dict) -> str:
    cal = r["calibration"]
    gates = cal["gates"]
    v2 = r["corpora"]["icit_converted_v2"]
    tt_s = _test_tallies(cal["strict94_leave_one_out"]["per_sign"])
    tt_k = _test_tallies(cal["kur113_negative_control"]["per_sign"])
    lines = [
        "# Phase-115 — Non-SA Validation Battery v2 for the 44 SA-Lineage Anchors",
        "",
        f"**Spec:** {SPEC} (frozen before any results) · "
        f"**Date:** {r['date']} · **GPU device:** {r['gpu_device']}",
        "",
        "## What changed vs Phase-113 (spec 014 sections 1-2, 4)",
        "",
        "Phase-113's battery was rejected at calibration (STRICT94 "
        "validated 3/94) because T1 starved on the Phase-107 ICIT "
        "layer. Diagnosis: a leading-zero key mismatch cost 4,014 "
        "source tokens and the all-or-nothing inscription rule "
        "discarded the rest. Battery v2 rebuilds the layer and "
        "scales T1's attestation floor to each sign's measured "
        "opportunity; T2/T3, the gates, and the decision rule are "
        "spec 011 unchanged.",
        "",
        f"- v2 layer: {v2['kept_inscriptions']} inscriptions / "
        f"{v2['kept_mapped_tokens']} mapped tokens "
        f"(+ {v2['kept_sentinel_tokens']} sentinel positions); "
        f"token-map coverage excl. placeholders "
        f"{v2['token_map_coverage_excl_placeholders']:.4f} "
        "(v1: 0.693); sampling ratio r = "
        f"{v2['sampling_ratio_r']}.",
        "",
        "## Verdict",
        "",
    ]
    if gates["battery_accepted"]:
        tally = r["main_run"]["tally"]
        lines += [
            "Calibration gates **passed**; the frozen battery v2 "
            "was applied to the 44 flagged anchors and the "
            "section-6 rule executed mechanically:",
            "",
            f"- VALIDATED_NON_SA: **{tally.get('VALIDATED_NON_SA', 0)}**",
            f"- DEMOTE (to CANDIDATE): **{tally.get('DEMOTE', 0)}**",
            f"- UNRESOLVED (stays flagged): **{tally.get('UNRESOLVED', 0)}**",
        ]
    else:
        lines += [
            "**BATTERY REJECTED at calibration.** The frozen gates "
            "of spec 014 section 5 were not both met, so FLAGGED44 "
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
        f"{ts.get('VALIDATED_NON_SA', 0)} | {ts.get('DEMOTE', 0)} | "
        f"{ts.get('UNRESOLVED', 0)} | >= 57 required: "
        f"**{'PASS' if gates['strict_gate_pass'] else 'FAIL'}** |",
        f"| KUR113 (negative control) | 113 | "
        f"{tk.get('VALIDATED_NON_SA', 0)} | {tk.get('DEMOTE', 0)} | "
        f"{tk.get('UNRESOLVED', 0)} | <= 5 required: "
        f"**{'PASS' if gates['kur_gate_pass'] else 'FAIL'}** |",
        "",
        "Per-test states (calibration):",
        "",
        "| Set | Test | PASS | FAIL | NOT_ATTESTED | INDETERMINATE |",
        "|---|---|---|---|---|---|",
    ]
    for label, tt in (("STRICT94", tt_s), ("KUR113", tt_k)):
        for tk_name in ("t1", "t2", "t3"):
            c = tt[tk_name]
            lines.append(
                f"| {label} | {tk_name.upper()} | {c.get('PASS', 0)} | "
                f"{c.get('FAIL', 0)} | {c.get('NOT_ATTESTED', 0)} | "
                f"{c.get('INDETERMINATE', 0)} |")
    lines += [
        "",
        "## Sets and corpora (recomputed; assertions in spec section 3)",
        "",
        "- FLAGGED44: 44 anchors (24 SA_DERIVED + 20 "
        "SA_CONFIRMED_ONLY; 43 HIGH + M293 MEDIUM).",
        f"- STRICT94: 94 anchors (90 HIGH + 4 MEDIUM); Holdat token "
        f"coverage {r['sets']['strict94']['holdat_coverage']:.4f} "
        f"(5,159 / 7,002).",
        "- KUR113: 113 premise-superseded anchors, all reading `kur`.",
        f"- Holdat: {r['corpora']['holdat']['inscriptions']} "
        f"inscriptions / {r['corpora']['holdat']['tokens']} tokens. "
        f"ICIT v2 layer: {v2['kept_inscriptions']} inscriptions / "
        f"{v2['kept_mapped_tokens']} mapped tokens (local "
        "restricted data; statistics only).",
    ]
    if r["final"]:
        f = r["final"]
        vc = f["validated_core_after"]
        lines += [
            "",
            "## Final state",
            "",
            f"- Tiers after: {f['by_confidence']} "
            f"(H+M = {f['hm_signs']}, Holdat coverage "
            f"{f['hm_holdat_coverage']:.4f}).",
            f"- Validated core after (STRICT94 + newly validated "
            f"H+M): {vc['n_signs']} signs, Holdat coverage "
            f"{vc['holdat_coverage']:.4f}.",
            "- Per-anchor records: "
            "`reports/phase115_nonsa44v2_change_register.json`; full "
            "test statistics: `reports/phase115_nonsa44v2_results.json`.",
        ]
    lines += [
        "",
        "## Limitations (registered in spec section 8)",
        "",
        "A PASS certifies distributional and compositional "
        "survival under independent non-SA tests; it does not prove "
        "the phonetic value. A FAIL demotes to CANDIDATE; it does "
        "not declare the reading false. Holdat and the ICIT layer "
        "are independent compilations of the same published "
        "catalogues, not independent archaeology; sentinel "
        "positions preserve positional geometry but the v2 layer "
        "measures a broader inscription population than v1.",
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


if __name__ == "__main__":
    out = run_all()
    print({"battery_accepted":
           out["calibration"]["gates"]["battery_accepted"],
           "main_tally": (out["main_run"] or {}).get("tally")})

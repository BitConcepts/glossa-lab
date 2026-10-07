"""Phase-113 (spec 011) — orchestration: calibration -> gate -> run.

Executes the frozen protocol of
specs/011-phase113-nonsa44-validation/spec.md:

  1. Recompute and assert the frozen sets (FLAGGED44, STRICT94,
     KUR113) from the anchors file + Phase-108 provenance register.
  2. Calibration: the unchanged battery over STRICT94
     (leave-one-out) and KUR113. Gates: strict VALIDATED >= 57/94;
     kur VALIDATED <= 5/113. A failed gate rejects the battery —
     the anchors file is NOT modified and FLAGGED44 is never run.
  3. Main run (only if calibration passes): battery over
     FLAGGED44, the section-5 decision rule applied mechanically,
     anchors file updated with the Phase-109/110 bookkeeping
     pattern (summary fields regenerated from the entries;
     changed-entries == change-register signs, asserted).

Local restricted corpora (Holdat CSV, ICIT converted layer) are
read from the gitignored downloads area (this worktree's copy if
present, else the main checkout's). They are never committed;
only statistics and verdicts are published.
"""
from __future__ import annotations

import importlib.util
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
    CoreGrammar, CorpusContext, evaluate_anchor, normalize_reading,
)

ANCHORS_PATH = _BACKEND / "reports" / "INDUS_FINAL_ANCHORS.json"
REGISTER_PATH = _REPO / "reports" / "phase108_provenance_register.json"
RESULTS_PATH = _REPO / "reports" / "phase113_nonsa44_results.json"
CHANGE_REGISTER_PATH = _REPO / "reports" / "phase113_nonsa44_change_register.json"
SUMMARY_PATH = _REPO / "reports" / "phase113_nonsa44_summary.md"
SPEC = "specs/011-phase113-nonsa44-validation"
DATE = "2026-10-07"

STRICT_VALIDATED_MIN = 57   # of 94  (spec 011 section 4: >= 60%)
KUR_VALIDATED_MAX = 5       # of 113 (spec 011 section 4)


def _gpu_device() -> str:
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:  # noqa: BLE001
        return "cpu (torch absent)"


def _load_module_by_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _find_downloads() -> Path:
    for cand in (_REPO / "corpora" / "downloads",
                 _MAIN_REPO / "corpora" / "downloads"):
        if (cand / "icit_fieldcady" / "icit_converted.json").exists():
            return cand
    raise FileNotFoundError("corpora/downloads not found in worktree "
                            "or main checkout")


def load_holdat_inscriptions(csv_path: Path):
    """Exact replica of sa_validation.load_holdat_corpus grouping
    (loader logic only; no SA code is executed): rows grouped by
    cisi_number at their position index, empties dropped."""
    import csv
    seals: dict[str, list] = {}
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = (row.get("cisi_number") or "").strip()
            p = int(row.get("position") or 0)
            if c not in seals:
                seals[c] = []
            while len(seals[c]) <= p:
                seals[c].append("")
            seals[c][p] = s
    return [[s for s in v if s] for v in seals.values() if any(v)]


def load_icit_inscriptions(path: Path):
    data = json.loads(path.read_text("utf-8"))
    return [list(x) for x in data["inscriptions"] if x]


def compute_sets(anchors: dict, register: dict) -> dict:
    records = register["records"]
    flagged = sorted(s for s, e in anchors.items()
                     if e.get("validation_status")
                     == "pending_non_sa_validation")
    strict = sorted(
        s for s, r in records.items()
        if r["category"] not in ("SA_DERIVED", "SA_CONFIRMED_ONLY")
        and not r["sa_in_chain"]
        and anchors[s]["confidence"] in ("HIGH", "MEDIUM"))
    kur = sorted(s for s, e in anchors.items()
                 if e.get("validation_status") == "premise_superseded")
    # Frozen assertions (spec 011 section 2)
    assert len(flagged) == 44, f"FLAGGED44 size {len(flagged)}"
    assert len(strict) == 94, f"STRICT94 size {len(strict)}"
    assert len(kur) == 113, f"KUR113 size {len(kur)}"
    assert not set(flagged) & set(strict), "flagged/strict overlap"
    assert all(anchors[s]["reading"] == "kur" for s in kur)
    assert Counter(anchors[s]["confidence"] for s in flagged) == \
        Counter({"HIGH": 43, "MEDIUM": 1})
    return {"flagged44": flagged, "strict94": strict, "kur113": kur}


def _evaluate_set(signs, anchors, core_signs, readings_norm,
                  holdat, icit, is_valid_initial, loo=False):
    results = {}
    for s in signs:
        core = (core_signs - {s}) if loo else core_signs
        grammar = CoreGrammar(core, readings_norm, holdat)
        results[s] = evaluate_anchor(
            s, anchors[s]["reading"], grammar, readings_norm,
            holdat, icit, is_valid_initial)
    return results


def _tally(results: dict) -> dict:
    return dict(Counter(r["outcome"] for r in results.values()))


def _apply_outcomes(anchors: dict, results: dict) -> list:
    """Apply the section-5 rule to FLAGGED44 entries in-place;
    return change-register records (Phase-110 entry shape)."""
    register = []
    for s in sorted(results):
        r = results[s]
        e = anchors[s]
        before = {"confidence": e["confidence"],
                  "validation_status": e.get("validation_status")}
        states = {k: r[k]["state"] for k in ("t1", "t2", "t3")}
        ann_head = (f"Phase-113 ({DATE}): non-SA battery (spec 011) "
                    f"outcome {r['outcome']} — T1 {states['t1']}, "
                    f"T2 {states['t2']}, T3 {states['t3']}.")
        if r["outcome"] == "VALIDATED_NON_SA":
            e["validation_status"] = "validated_non_sa"
            ref = ("Phase-113 (spec 011) non-SA battery T1+T2+T3: "
                   "reports/phase113_nonsa44_results.json")
            e["evidence_ref"] = (f"{e['evidence_ref']}; {ref}"
                                 if e.get("evidence_ref") else ref)
            e["phase113_annotation"] = (
                ann_head + " validation_status set to "
                "validated_non_sa with an H26 evidence reference. "
                "Tier unchanged (this phase validates or demotes; "
                "it never promotes).")
            action = "validate"
        elif r["outcome"] == "DEMOTE":
            failed = [k.upper() for k, v in states.items() if v == "FAIL"]
            e["confidence"] = "CANDIDATE"
            e["validation_status"] = "failed_non_sa_validation"
            e["phase113_annotation"] = (
                ann_head + f" Failed test(s): {', '.join(failed)}. "
                "Demoted to CANDIDATE per the frozen decision rule.")
            action = "demote"
        else:
            e["phase113_annotation"] = (
                ann_head + " No tier change; anchor stays flagged "
                "pending_non_sa_validation.")
            action = "unresolved-no-change"
        register.append({
            "step": "main-run", "sign": s, "rule": "spec011-section5",
            "action": action,
            "tests": states,
            "statistics": {
                "t1": {k: r["t1"].get(k) for k in
                       ("n_icit_tokens", "modal_holdat", "modal_icit", "tv")},
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


def _regenerate_bookkeeping(data: dict, holdat_tokens: list) -> dict:
    """Phase-109/110 bookkeeping regeneration + H+M coverage."""
    anchors = data["anchors"]
    counts = Counter(v.get("confidence") for v in anchors.values())
    data["total"] = len(anchors)
    data["total_all_entries"] = len(anchors)
    data["by_confidence"] = {k: counts.get(k, 0) for k in
                             ("HIGH", "MEDIUM", "LOW", "CANDIDATE")}
    data["n_high"] = counts.get("HIGH", 0)
    data["n_medium"] = counts.get("MEDIUM", 0)
    data["n_low"] = counts.get("LOW", 0)
    data["n_candidate"] = counts.get("CANDIDATE", 0)
    md = data.setdefault("metadata", {})
    md["total_count"] = len(anchors)
    md["high_count"] = counts.get("HIGH", 0)
    md["medium_count"] = counts.get("MEDIUM", 0)
    md["low_count"] = counts.get("LOW", 0)
    md["candidate_count"] = counts.get("CANDIDATE", 0)
    md["hm_confirmed_count"] = counts.get("HIGH", 0) + counts.get("MEDIUM", 0)
    hm = {s for s, v in anchors.items()
          if v.get("confidence") in ("HIGH", "MEDIUM")}
    n_cov = sum(1 for t in holdat_tokens if t in hm)
    data["corpus_token_coverage"] = round(n_cov / len(holdat_tokens), 6)
    return {"by_confidence": data["by_confidence"],
            "hm_signs": len(hm), "hm_holdat_coverage": data["corpus_token_coverage"]}


def run_all() -> dict:
    anchors_data = json.loads(ANCHORS_PATH.read_text("utf-8"))
    anchors = anchors_data["anchors"]
    register = json.loads(REGISTER_PATH.read_text("utf-8"))
    sets = compute_sets(anchors, register)
    downloads = _find_downloads()
    holdat_ins = load_holdat_inscriptions(
        downloads / "external_repos" / "holdatllc_indus"
        / "indus_corpus 2.csv")
    icit_ins = load_icit_inscriptions(
        downloads / "icit_fieldcady" / "icit_converted.json")
    holdat = CorpusContext(holdat_ins)
    icit = CorpusContext(icit_ins)
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
                               is_valid_initial, loo=True)
    cal_kur = _evaluate_set(sets["kur113"], anchors, strict_set,
                            readings_norm, holdat, icit,
                            is_valid_initial)
    t_strict, t_kur = _tally(cal_strict), _tally(cal_kur)
    gate_strict = t_strict.get("VALIDATED_NON_SA", 0) >= STRICT_VALIDATED_MIN
    gate_kur = t_kur.get("VALIDATED_NON_SA", 0) <= KUR_VALIDATED_MAX
    accepted = gate_strict and gate_kur

    results = {
        "phase": 113, "spec": SPEC, "date": DATE,
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
            "icit_converted": {"inscriptions": icit.n_inscriptions,
                               "tokens": icit.n_tokens},
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
                             is_valid_initial)
        before = deepcopy(anchors)
        hm_before = {s for s, v in anchors.items()
                     if v["confidence"] in ("HIGH", "MEDIUM")}
        cov_before = round(
            sum(1 for t in holdat_tokens if t in hm_before)
            / len(holdat_tokens), 6)
        entries = _apply_outcomes(anchors, main)
        book = _regenerate_bookkeeping(anchors_data, holdat_tokens)
        anchors_data["_phase113_note"] = (
            f"Phase-113 ({DATE}, spec 011): non-SA validation battery "
            "applied to the 44 Phase-109 SA-lineage flagged anchors; "
            "outcomes per the frozen decision rule in "
            "reports/phase113_nonsa44_change_register.json; summary "
            "fields regenerated from the entries.")
        changed = {s for s in anchors if anchors[s] != before[s]}
        reg_signs = {r["sign"] for r in entries}
        assert changed == reg_signs, (
            f"diff/register mismatch: {sorted(changed ^ reg_signs)}")
        entries.append({
            "step": "bookkeeping", "sign": "*",
            "rule": "spec011-bookkeeping",
            "action": "regenerate-summary-fields",
            "before": {"hm_signs": len(hm_before),
                       "hm_holdat_coverage": cov_before},
            "after": book})
        ANCHORS_PATH.write_text(
            json.dumps(anchors_data, indent=2, ensure_ascii=False),
            encoding="utf-8")
        change_register = {
            "phase": 113, "spec": SPEC, "date": DATE,
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


def render_summary(r: dict) -> str:
    cal = r["calibration"]
    gates = cal["gates"]
    lines = [
        "# Phase-113 — Non-SA Validation Battery for the 44 SA-Lineage Anchors",
        "",
        f"**Spec:** {SPEC} (frozen before any results) · "
        f"**Date:** {r['date']} · **GPU device:** {r['gpu_device']}",
        "",
        "## Verdict",
        "",
    ]
    if gates["battery_accepted"]:
        tally = r["main_run"]["tally"]
        lines += [
            "Calibration gates **passed**; the frozen battery was "
            "applied to the 44 flagged anchors and the section-5 "
            "rule executed mechanically:",
            "",
            f"- VALIDATED_NON_SA: **{tally.get('VALIDATED_NON_SA', 0)}**",
            f"- DEMOTE (to CANDIDATE): **{tally.get('DEMOTE', 0)}**",
            f"- UNRESOLVED (stays flagged): **{tally.get('UNRESOLVED', 0)}**",
        ]
    else:
        lines += [
            "**BATTERY REJECTED at calibration.** The frozen gates "
            "of spec 011 section 4 were not both met, so FLAGGED44 "
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
        "## Sets and corpora (recomputed; assertions in spec section 2)",
        "",
        f"- FLAGGED44: 44 anchors (24 SA_DERIVED + 20 "
        f"SA_CONFIRMED_ONLY; 43 HIGH + M293 MEDIUM).",
        f"- STRICT94: 94 anchors (90 HIGH + 4 MEDIUM); Holdat token "
        f"coverage {r['sets']['strict94']['holdat_coverage']:.4f} "
        f"(5,159 / 7,002).",
        f"- KUR113: 113 premise-superseded anchors, all reading `kur`.",
        f"- Holdat: {r['corpora']['holdat']['inscriptions']} "
        f"inscriptions / {r['corpora']['holdat']['tokens']} tokens. "
        f"ICIT converted layer: "
        f"{r['corpora']['icit_converted']['inscriptions']} "
        f"inscriptions / {r['corpora']['icit_converted']['tokens']} "
        f"tokens (local restricted data; statistics only).",
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
            "`reports/phase113_nonsa44_change_register.json`; full "
            "test statistics: `reports/phase113_nonsa44_results.json`.",
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
        "catalogues, not independent archaeology; T1 NOT_ATTESTED "
        "partly measures ICIT conversion coverage.",
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

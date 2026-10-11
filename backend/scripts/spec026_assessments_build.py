"""Spec 026 S5 — build historical-assessments.{json,md} from the
impact register plus the assessment overlay authored in this
script. Originals are never modified; assessments are new
records linked to the register rows. Strict: every register
row gets exactly one assessment row; bespoke overlays must
reference real register IDs.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO / "specs" / "026-rcph-framework-transfer"
REGISTER = SPEC_DIR / "impact-register.json"
OUT_JSON = SPEC_DIR / "historical-assessments.json"
OUT_MD = SPEC_DIR / "historical-assessments.md"

# item_id -> (framework_status, status_changed, assessment)
BESPOKE: dict[str, tuple[str, bool, str]] = {
    "PHASE-132": ("CONTRADICTED", True,
        "Phase-383 rescoring: exact-sequence agreement recomputed "
        "exactly (0.20) with bootstrap CI [0.10, 0.32] against the "
        "frozen 0.80 floor. The stop-rule outcome maps to "
        "CONTRADICTED for the bounded claim that this AI coding "
        "basis at this protocol can produce a publishable keyed "
        "transcription layer. What the old run establishes: the "
        "basis failed decisively (not sampling noise). It does "
        "not establish anything about human-coder feasibility."),
    "PHASE-134": ("INCONCLUSIVE", True,
        "Phase-383 rescoring: agreement 0.84 / kappa 0.7885 "
        "recomputed exactly; CIs agreement [0.77, 0.91], kappa "
        "[0.689, 0.878]. The middle-band outcome maps to "
        "INCONCLUSIVE. The 'missed the proceed gate by one "
        "object' framing cannot be excluded on sampling grounds "
        "(the CI reaches 0.85) — and the gate-spanning CI is "
        "itself the finding: a 100-object pilot cannot resolve a "
        "0.01 margin. Origin-group audit: one coder origin group "
        "(single AI model family); agreement is intra-origin "
        "consistency, not independent corroboration."),
    "PHASE-135": ("INCONCLUSIVE", True,
        "Phase-383 rescoring: agreement 0.78 / kappa 0.7129 "
        "recomputed exactly; agreement CI [0.70, 0.86]. Middle "
        "band -> INCONCLUSIVE. Same origin-group narrowing as "
        "Phase-134 (one origin group). The replication pilot "
        "reproduced the first pilot's band under a second icon "
        "set — a consistency fact about the protocol, not a "
        "confirmation."),
    "PHASE-137": ("F2 CONTRADICTED (bounded, at declared margin); "
                  "F3 SUPPORTED (margin-adjudicated)", True,
        "Phase-384: chi2/V verified from the recorded tables and "
        "rebuilt populations (tables asserted equal). F2: the "
        "original NOT SUPPORTED (composition-controlled "
        "permutation p = 0.7354) is untouched; the margin "
        "completion adds that the marginal effect's "
        "bias-corrected basic CI [0.0589, 0.0778] sits below "
        "the declared 0.10 floor — the bounded marginal claim "
        "is CONTRADICTED at the declared margin. F3: SUPPORTED "
        "stands, now margin-adjudicated (basic CI [0.1823, "
        "0.2104]). The v1 interval procedure was INVALID "
        "(failed its independence control) and is not used. "
        "Original confounder confessions unchanged."),
    "PHASE-140": ("SUPPORTED under control (margin-adjudicated; "
                  "chronology NOT controlled)", True,
        "Phase-385: population and observed chi2 verified "
        "exactly; stratified basic bootstrap CI [0.1838, "
        "0.2102] lies entirely above the declared 0.10 floor — "
        "G1 SUPPORTED under control stands at the declared "
        "margin. Chronology remains NOT controlled (rider "
        "travels with the claim). The recorded permutation "
        "result (0/9,999) was not recomputed and is unaltered."),
    "SPEC-023": ("status refined by Phase-383 (see PHASE-132)", True,
        "The Stage P pilot's framework status is the Phase-383 "
        "assessment of Phase-132: CONTRADICTED for the bounded "
        "AI-basis claim. Stage T remains unexecuted behind its "
        "own gate; nothing here changes that."),
    "SPEC-024": ("family status refined by Phases 383/384 "
                 "(see PHASE-134/135/137)", True,
        "Motif arm: INCONCLUSIVE x2 (unchanged outcome, new "
        "intervals + origin-group narrowing). Stage 2 family: "
        "F2 bounded claim CONTRADICTED at the declared margin; "
        "F3 SUPPORTED margin-adjudicated; F1/F4/F5 mappings "
        "unchanged from the register (NULL / descriptive). The "
        "motif arm remains CLOSED; reopening requires an owner "
        "decision plus human expert coders."),
    "SPEC-025": ("G1 SUPPORTED under control, margin-adjudicated "
                 "(chronology NOT controlled)", True,
        "Phase-385 supplies the interval G1 lacked; the verdict "
        "stands at the declared margin. The published record "
        "(Zenodo v4.9.0, DOI 10.5281/zenodo.23288406) is not "
        "altered by this program; any republication decision is "
        "the owner's, informed by this assessment."),
    "PHASE-111": ("INVALID", True,
        "The run's own label stands in its file. Framework "
        "status: INVALID — a control-validity failure means the "
        "run establishes nothing about its bounded claim, in "
        "either direction. What it does establish: the "
        "instrument/control defect it documented."),
    "PHASE-112": ("INVALID", True,
        "As Phase-111: own label stands; evidentiary status "
        "INVALID (control validity failed)."),
    "PHASE-113": ("INVALID", True,
        "Own label (INVALID RUN — control validity failed at "
        "round 1) stands; evidentiary status INVALID. The "
        "second study filed under this phase number inherits "
        "the same reading for its instrument claims."),
    "PHASE-114": ("INVALID", True,
        "No standalone report exists; the execution artifacts "
        "filed under Phase-113 outputs carry the INVALID "
        "reading of that run. Nothing about the bounded claims "
        "is established."),
    "PHASE-115": ("INCONCLUSIVE (battery rejected at calibration)", True,
        "'BATTERY REJECTED at calibration' means the instrument "
        "never earned the right to test the claim: the frozen "
        "gates were not met, so no claim verdict exists. "
        "Framework status INCONCLUSIVE — the run establishes "
        "calibration facts about the battery, not a contradiction "
        "of the underlying hypothesis."),
    "PHASE-117": ("INCONCLUSIVE (battery rejected at calibration)", True,
        "As Phase-115: calibration rejection -> INCONCLUSIVE; "
        "the typicality claim was not tested by this battery."),
    "PHASE-118": ("INCONCLUSIVE (battery rejected at calibration)", True,
        "As Phase-115: calibration rejection -> INCONCLUSIVE."),
    "PHASE-116": ("bounded harmonization claims CONTRADICTED; "
                  "diagnostic findings stand", True,
        "Replayed exactly by Phase-386 (REPRODUCED). The study's "
        "own recommendation (R-NONE: no harmonization "
        "transformation is justified; cross-corpus positional "
        "validation on this pair is not viable under any tested "
        "convention alignment) maps the bounded harmonization "
        "claims to CONTRADICTED. Arm-level UNRESOLVED labels "
        "stand as recorded for the sub-questions they name."),
    "PHASE-125": ("CONTRADICTED (bounded agreement claim)", True,
        "Replayed exactly by Phase-386 (median TV 0.636931; "
        "null p = 0.824; 16 judgeable signs). The historical "
        "FAIL — DISAGREEMENT label stands in its file; under "
        "the frozen §6.3 falsifier the bounded claim (Holdat "
        "and ICIT positional profiles agree beyond the null) "
        "is CONTRADICTED. Phase-127's noise band (median TV "
        "0.0826) is what makes this a contradiction rather than "
        "an absence of signal: observed disagreement is ~8x the "
        "noise floor."),
    "PHASE-127": ("diagnostic CONFIRMED stands; supplies the "
                  "discriminating noise band for Phase-125", True,
        "Replayed exactly by Phase-386 (all compared quantities "
        "REPRODUCED, incl. bootstrap CI [0.548638, 0.722042] and "
        "0/999 replicates >= observed). The 'FINAL' wording in "
        "the original label is read as final for the bounded "
        "cross-compilation question it tested — not for broader "
        "cross-corpus questions on other compilation pairs."),
    "SPEC-017": ("INVALID (mirrors Phases 111/112)", True,
        "Spec-level status follows its phase runs: INVALID; the "
        "spec's bounded claims were not tested by a valid "
        "instrument."),
    "SPEC-015": ("mirrors Phase-116 (REPRODUCED; bounded claims "
                 "CONTRADICTED)", True,
        "See PHASE-116. The spec's diagnostic findings stand as "
        "recorded."),
    "SPEC-019": ("mirrors Phase-125 (REPRODUCED; CONTRADICTED "
                 "bounded)", True,
        "See PHASE-125. PRED-2026-001's readiness adjudication "
        "is unaffected: PENDING, no scoring permitted or "
        "performed."),
    "SPEC-021": ("readiness NO-GO stands (REPRODUCED)", False,
        "Replay chain verified by Phase-386 via Phase-131's "
        "inputs of record. The adjudication's framework reading "
        "is unchanged: the qualifying-corpus readiness claim "
        "was not established; PRED items remain PENDING."),
    "SPEC-022": ("published negative stands (REPRODUCED via "
                 "Phase-131)", False,
        "The attribution result (6.1% credited / 93.9% residual "
        "unexplained) replayed exactly. No status change."),
}

SA_COHORT = ("evidentiary status superseded (H26 quarantine)",
             True,
             "SA-era item. Under H26 (SA method falsified as "
             "sufficiency evidence at Phase-107 and quarantined), "
             "this item establishes at most its bounded "
             "computational/descriptive content. It is not "
             "evidence for any reading, language identification, "
             "or decipherment claim, and no rerun may rehabilitate "
             "it as promotion evidence. Its historical label "
             "stands in its file.")


def main() -> int:
    doc = json.loads(REGISTER.read_text("utf-8"))
    rows = doc["register"]
    out_rows = []
    for r in rows:
        item = r["item_id"]
        if item in BESPOKE:
            status, changed, text = BESPOKE[item]
        elif r["classification"] == "NOT-RERUNNABLE":
            status = "NOT-RERUNNABLE — evidentiary ceiling: no claim-level weight"
            changed = True
            text = (
                "The register records this item as NOT-RERUNNABLE: "
                "no artifact exists in any scoped location (the "
                "record survives only in outputs/ and grouped "
                "summaries) and the original experiment definition "
                "is not recoverable. Evidentiary ceiling, as the "
                "register promised: the preserved record "
                "establishes only that work under this phase "
                "number was reported; it carries no evidentiary "
                "weight for or against any claim. The surrounding "
                "cohort is SA-era, so any SA-basis content it may "
                "have had is governed by the H26 quarantine "
                "(see the SA cohort assessment). Preserve + label; "
                "do not cite as evidence."
            )
        elif (
            r["classification"] in ("REINTERPRET-ONLY", "NOT-RERUNNABLE")
            and ("H26" in r["rationale"] or "SA " in r["rationale"]
                 or "SA-era" in r["rationale"] or "SA-line" in r["rationale"]
                 or "SA-derived" in r["rationale"])
        ):
            status, changed, text = SA_COHORT
            if r["classification"] == "NOT-RERUNNABLE":
                text += (" Source artifacts are preserved as-is; "
                         "the item is not rerunnable.")
        else:
            status = f"unchanged (register class: {r['classification']})"
            changed = False
            text = ("No superseding assessment: the framework "
                    "reading of this item matches its historical "
                    "record under its register classification.")
        out_rows.append({
            "item_id": item,
            "kind": r["kind"],
            "classification": r["classification"],
            "historical_label": r["historical_label"],
            "framework_status": status,
            "status_changed": changed,
            "assessment": text,
            "rerun_spec": r["rerun_spec"],
        })
    missing = set(BESPOKE) - {r["item_id"] for r in rows}
    if missing:
        raise SystemExit(f"overlay references unknown items: {missing}")
    changed = [r for r in out_rows if r["status_changed"]]
    payload = {
        "spec": "026",
        "artifact": "historical-assessments",
        "register_items": len(out_rows),
        "status_changed_items": len(changed),
        "changed_item_ids": [r["item_id"] for r in changed],
        "rows": out_rows,
        "ai_disclosure": (
            "Produced by an AI agent (Muse Spark, via Muse "
            "Code) at the direction of Tristen Pierson, per "
            "constitution sec.VI."
        ),
    }
    OUT_JSON.write_text(json.dumps(payload, indent=1), "utf-8")

    lines = [
        "# Spec 026 — Historical Assessments",
        "",
        "Original result files and ledger entries are NEVER "
        "rewritten. This file records, per register item, the "
        "framework status that supersedes the historical label's "
        "evidentiary reading where they differ — and says exactly "
        "what the old run does and does not establish. Machine-"
        "readable twin: `historical-assessments.json` (all "
        f"{len(out_rows)} register items; {len(changed)} with "
        "changed status).",
        "",
        "## Items whose evidentiary status CHANGED",
        "",
    ]
    for r in changed:
        lines += [
            f"### {r['item_id']} — {r['framework_status']}",
            "",
            f"Historical label (of record): {r['historical_label']}",
            "",
            r["assessment"],
            "",
        ]
    lines += [
        "## All other register items",
        "",
        "No superseding assessment: framework reading matches "
        "the historical record under the register classification "
        "(see the JSON twin for the per-item rows, and "
        "`impact-register.md` for classifications and rationales).",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), "utf-8")
    print(f"rows={len(out_rows)} changed={len(changed)}")
    print("changed ids:", ", ".join(r["item_id"] for r in changed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

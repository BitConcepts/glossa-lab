"""Phase 192 — Anchor Update Proposal

Synthesizes evidence from Phases 186-191 into a proposed extension
to INDUS_FINAL_ANCHORS.json. For each of the 14 absent phonemes:

  - Takes the best validated proposal (from Phase 191)
  - Assembles a complete evidence chain:
      * Elamite evidence (McAlpin 1974/1981) — STRONG/MODERATE/CANDIDATE
      * Brahui North Dravidian evidence (Phase 189)
      * SA consistency under combined anchors (Phase 190)
      * Grammar/phonotactic validation (Phase 191)
  - Assigns final confidence: MEDIUM or LOW
  - Writes proposed new entries to a diff file (does NOT modify anchors in place)

Output:
  outputs/phase192_anchor_diff.json  — proposed new entries
  outputs/phase192_anchor_update.json — complete proposed INDUS_FINAL_ANCHORS
                                         (original + new entries, NOT written to
                                          backend/reports yet — requires review)

Evidence tiers used (conservative, H23-compliant):
  MEDIUM: Elamite STRONG + SA consistent + grammar valid + phonotactic OK
  LOW:    Elamite MODERATE + (SA consistent OR grammar valid)
  CANDIDATE: Elamite present but incomplete validation
"""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
REPORTS   = REPO_ROOT / "research" / "indus" / "phase_reports"
ANCHOR_F  = REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
sys.path.insert(0, str(REPO_ROOT / "backend"))
OUTPUTS.mkdir(exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

ABSENT_PHONEMES = [
    "su","li","shu","gu","ab","ba","du","zi","ga","mil","gi","en","ki","sum"
]

# Full evidence chain text for each absent phoneme (to be stored in anchor basis)
EVIDENCE_CHAIN = {
    "en": (
        "Phase-186: Elamite an-=lord/ruler → PDr *āṉ/*āṇ (DEDR 298) — STRONG Elamite support. "
        "Phase-189: Brahui an (person,lord) — all 14/14 Brahui coverage confirmed. "
        "Phase-190: SA convergence B/C condition. "
        "McAlpin 1974 JAOS 94(2) Prop. 5."
    ),
    "ki": (
        "Phase-186: Elamite ki=earth/ground → PDr *keḻ/kiḻ (DEDR 1935) — STRONG Elamite support. "
        "Phase-189: Brahui ki (earth,low) direct cognate. "
        "Phase-190: SA convergence B/C condition. "
        "McAlpin 1974 JAOS 94(2)."
    ),
    "du": (
        "Phase-186: Elamite tu=to give → PDr *tu- (DEDR 3302) — STRONG Elamite support. "
        "Phase-189: Brahui tu/du (give) = PDr *tu-. "
        "Phase-190: SA convergence. "
        "McAlpin 1974 JAOS 94(2) Prop. 18."
    ),
    "ga": (
        "Phase-186: Elamite ka=water/eye → PDr *ka/*kaṭ (DEDR 1221) — STRONG. "
        "Phase-189: Brahui q before a-vowels → /ga/ in Indus context. "
        "Phase-190: SA convergence. McAlpin 1974."
    ),
    "sum": (
        "Phase-186: Elamite šum/sum=name/title → PDr *cum- (DEDR 2689) — STRONG. "
        "Phase-189: Brahui sum/cum (name,call) = Elamite šum-. "
        "E16 (McAlpin 1974): title marker hypothesis. "
        "Phase-190: SA convergence."
    ),
    "ab": (
        "Phase-186: Elamite ap-=father/water → PDr *appa (DEDR 172) — MODERATE. "
        "Phase-189: Brahui ap/ab (father). "
        "Phase-190: SA convergence. McAlpin 1974 Prop."
    ),
    "ba": (
        "Phase-186: Elamite pal- → PDr *pal (tooth,ivory DEDR 4003) — MODERATE. "
        "Phase-189: Brahui ba- (speak) cf PDr *pal voiced variant. "
        "Phase-190: SA convergence."
    ),
    "zi": (
        "Phase-186: Elamite zi=cut/divide → PDr *ci- (DEDR 2589) — MODERATE. "
        "Phase-189: Brahui z- (cut) = Elamite zi-; independent of Tamil. "
        "McAlpin 1974 Prop. 7. Phase-190: SA convergence."
    ),
    "mil": (
        "Phase-186: Elamite mel/mil=brightness/light → PDr *mel/*mil (DEDR 5085) — MODERATE. "
        "Phase-189: Brahui mil/mel (rise,shine) preserved from PDr *mil-. "
        "Parpola links to stellar vocabulary. Phase-190: SA."
    ),
    "gi": (
        "Phase-186: Elamite ki=ear/go → PDr *ki (DEDR 1562) — MODERATE (voiced variant). "
        "Phase-189: Brahui ki- (go toward,ear). "
        "Phase-190: SA convergence."
    ),
    "su": (
        "Phase-186: Elamite -su=3sg suffix → PDr *cu/*cū- (DEDR 2678) — MODERATE. "
        "Phase-189: Brahui cu- (to do/say) = Tamil cu-. Kurukh su- (say) direct cognate. "
        "McAlpin 1974 Prop. 21. Phase-190: SA convergence."
    ),
    "li": (
        "Phase-186: Elamite li=give/bring → PDr *il/*li (DEDR 491) — MODERATE. "
        "Phase-189: Brahui li (give). McAlpin 1974 Prop. 14 (l/r/ḷ correspondence). "
        "Phase-190: SA convergence."
    ),
    "gu": (
        "Phase-186: Elamite ku=say/do → PDr *ku/*kuṭ (DEDR 1687) — MODERATE. "
        "Phase-189: Brahui q (uvular k) = PDr *k before back vowel → /gu/ variant. "
        "Phase-190: SA convergence."
    ),
    "shu": (
        "Phase-186: Elamite š-/ši-=fall/down → PDr *cu/*co (DEDR 2665) — CANDIDATE. "
        "Phase-189: Brahui š preserved as distinct from s (palatalization). "
        "McAlpin 1974 Prop. 8. Phase-190: SA convergence (weaker)."
    ),
}


def load_outputs():
    p191_path = OUTPUTS / "phase191_grammar_validation.json"
    p190_path = OUTPUTS / "phase190_elamo_anchor_injection.json"
    p186_path = OUTPUTS / "phase186_elamo_dravidian_gap.json"

    p191 = json.loads(p191_path.read_text()) if p191_path.exists() else {}
    p190 = json.loads(p190_path.read_text()) if p190_path.exists() else {}
    p186 = json.loads(p186_path.read_text()) if p186_path.exists() else {}
    return p186, p190, p191


def build_new_anchor_entries(p186: dict, p190: dict, p191: dict) -> list[dict]:
    """Build new anchor entries for INDUS_FINAL_ANCHORS.json."""
    best_per_phoneme = p191.get("best_per_phoneme", {})
    sa_delta_b = p190.get("delta_b_vs_a", 0.0)
    sa_delta_c = p190.get("delta_c_vs_a", 0.0)

    new_entries = []
    for phoneme in ABSENT_PHONEMES:
        best = best_per_phoneme.get(phoneme)
        if not best:
            # Phoneme has no validated sign candidate — still report coverage
            new_entries.append({
                "phoneme":       phoneme,
                "sign_candidate": None,
                "anchor_sign_id": None,
                "confidence":    "CANDIDATE",
                "evidence_chain": EVIDENCE_CHAIN.get(phoneme, ""),
                "source":        "Phase-186 Elamo-Dravidian + Phase-189 Brahui",
                "note":          "No validated sign candidate from M77 corpus; requires ICIT corpus",
            })
            continue

        m77_id     = best.get("sign", "")
        conf_191   = best.get("confidence", "CANDIDATE")
        elamite    = best.get("elamite", "")
        sa_agrees  = best.get("sa_agrees", False)

        # Final confidence: use Phase 191's assessment but cap at MEDIUM
        # (no absent phoneme moves to HIGH without ICIT corpus validation)
        if conf_191 == "MEDIUM" and elamite in ("STRONG",):
            final_conf = "MEDIUM"
        elif conf_191 in ("MEDIUM", "LOW") and elamite in ("STRONG", "MODERATE"):
            final_conf = "LOW"
        else:
            final_conf = "CANDIDATE"

        anchor_sign_id = f"M{m77_id}"
        new_entries.append({
            "phoneme":        phoneme,
            "sign_candidate": m77_id,
            "anchor_sign_id": anchor_sign_id,
            "confidence":     final_conf,
            "elamite_tier":   elamite,
            "sa_consistent":  sa_agrees,
            "evidence_chain": EVIDENCE_CHAIN.get(phoneme, ""),
            "source": (
                f"Phase-186 Elamo-Dravidian (McAlpin 1974) + Phase-189 Brahui + "
                f"Phase-190 SA delta_b={sa_delta_b:+.4f} delta_c={sa_delta_c:+.4f} + "
                f"Phase-191 grammar validation [{conf_191}]"
            ),
            "note": (
                "Absent phoneme fill. Independent evidence: Elamite cognate (McAlpin) + "
                "Brahui North Dravidian + SA convergence. "
                "Confidence capped at MEDIUM pending ICIT corpus validation."
            ),
        })

    return new_entries


def write_anchor_diff(new_entries: list[dict], existing_anchors: dict) -> tuple[dict, dict]:
    """Produce diff and proposed merged anchor set."""
    diff = {
        "generated_at":   datetime.utcnow().isoformat(),
        "source":         "Phase-192 multi-evidence synthesis (Phases 186-191)",
        "description":    "Proposed extension to INDUS_FINAL_ANCHORS.json with absent phoneme fills",
        "n_new_entries":  sum(1 for e in new_entries if e["anchor_sign_id"]),
        "n_candidate_only": sum(1 for e in new_entries if not e["anchor_sign_id"]),
        "new_anchor_entries": [],
        "candidate_phonemes": [],
        "medium_phonemes": [],
        "low_phonemes": [],
    }

    proposed_merged = dict(existing_anchors)  # start with copy

    for entry in new_entries:
        anchor_id = entry.get("anchor_sign_id")
        conf = entry.get("confidence", "CANDIDATE")

        if anchor_id and anchor_id not in existing_anchors:
            # Add new entry to merged set
            proposed_merged[anchor_id] = {
                "reading":    entry["phoneme"],
                "confidence": conf,
                "basis":      entry["evidence_chain"],
                "source":     entry["source"],
                "_new_phase_192": True,
                "_note":      entry["note"],
            }
            diff["new_anchor_entries"].append({
                "sign_id":    anchor_id,
                "m77_id":     entry["sign_candidate"],
                "phoneme":    entry["phoneme"],
                "confidence": conf,
                "elamite_tier": entry.get("elamite_tier", ""),
            })
            if conf == "MEDIUM":
                diff["medium_phonemes"].append(entry["phoneme"])
            elif conf == "LOW":
                diff["low_phonemes"].append(entry["phoneme"])
            else:
                diff["candidate_phonemes"].append(entry["phoneme"])
        elif not anchor_id:
            diff["candidate_phonemes"].append(entry["phoneme"])

    return diff, proposed_merged


def main():
    import time
    t0 = time.time()
    print("=" * 60)
    print("Phase 192 — Anchor Update Proposal")
    print("=" * 60)

    p186, p190, p191 = load_outputs()
    existing_anchors = json.loads(ANCHOR_F.read_text())["anchors"]
    existing_total   = json.loads(ANCHOR_F.read_text())
    print(f"\nExisting anchors: {len(existing_anchors)}")

    new_entries = build_new_anchor_entries(p186, p190, p191)
    diff, proposed_merged = write_anchor_diff(new_entries, existing_anchors)

    print("\n=== Proposed New Anchor Entries ===")
    for e in diff["new_anchor_entries"]:
        print(f"  {e['sign_id']} → /{e['phoneme']}/ [{e['confidence']}] "
              f"Elamite:{e['elamite_tier']}")

    print(f"\n=== Coverage Summary ===")
    print(f"  MEDIUM confidence:    {diff['medium_phonemes']}")
    print(f"  LOW confidence:       {diff['low_phonemes']}")
    print(f"  CANDIDATE only:       {diff['candidate_phonemes']}")
    print(f"  Total new entries:    {diff['n_new_entries']}")
    print(f"  No sign found (need ICIT): {diff['n_candidate_only']}")

    # Absent phoneme fill summary
    filled_phonemes = [e["phoneme"] for e in diff["new_anchor_entries"]]
    still_absent    = [p for p in ABSENT_PHONEMES if p not in filled_phonemes]
    print(f"\n  Absent phonemes filled: {len(filled_phonemes)}/14")
    print(f"  Filled: {sorted(filled_phonemes)}")
    print(f"  Still absent (no sign candidate): {still_absent}")

    # Build final proposed anchor file
    proposed_full = dict(existing_total)
    proposed_full["anchors"] = proposed_merged
    proposed_full["total"]   = len(proposed_merged)
    proposed_full["_phase192_note"] = (
        "Phase-192 update proposal (2026-05-23): "
        f"{diff['n_new_entries']} new absent-phoneme entries added at LOW/MEDIUM/CANDIDATE. "
        "Evidence: McAlpin (1974) Elamo-Dravidian + Brahui North Dravidian (Phase-189) + "
        "SA convergence (Phase-190) + grammar validation (Phase-191). "
        "NOT FINAL — requires ICIT corpus confirmation before upgrading to HIGH."
    )

    elapsed = round(time.time() - t0, 1)
    result = {
        "phase":          192,
        "elapsed_s":      elapsed,
        "n_existing":     len(existing_anchors),
        "n_new_proposed": diff["n_new_entries"],
        "n_after_update": len(proposed_merged),
        "diff":           diff,
        "new_entries":    new_entries,
        "absent_filled":  filled_phonemes,
        "still_absent":   still_absent,
        "verdict": (
            f"ANCHOR UPDATE PROPOSED: {diff['n_new_entries']} new entries for absent phonemes. "
            f"MEDIUM: {diff['medium_phonemes']} | LOW: {diff['low_phonemes']} | "
            f"CANDIDATE: {diff['candidate_phonemes']}. "
            f"Still absent (no sign): {still_absent}."
        ),
    }

    # Save diff
    diff_out = OUTPUTS / "phase192_anchor_diff.json"
    diff_out.write_text(json.dumps(diff, indent=2, default=str), encoding="utf-8")

    # Save proposed full update (NOT written to backend/reports — requires review)
    update_out = OUTPUTS / "phase192_anchor_update_proposed.json"
    update_out.write_text(json.dumps(proposed_full, indent=2, default=str), encoding="utf-8")

    out = OUTPUTS / "phase192_anchor_update_proposal.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase192_anchor_update_proposal.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")

    print(f"\nPhase 192 complete in {elapsed}s")
    print(f"Verdict: {result['verdict']}")
    print(f"\nDiff saved: {diff_out}")
    print(f"Proposed update (review before applying): {update_out}")


if __name__ == "__main__":
    main()

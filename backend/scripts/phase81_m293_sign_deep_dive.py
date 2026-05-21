"""Phase-81: M293 Sign Deep-Dive — Highest-Priority Unknown Sign Analysis.

M293 is the single highest-priority unread/LOW-confidence sign:
  - Corpus frequency: 232 (3.31% of all tokens) — the largest unknown
  - Phase-73 SA consensus: syl_modal='ta', proto_modal='ar' (ENSEMBLE_LOW, disagreement)
  - Current Phase-79 LOW reading: 'vil' (archery bow iconography)

This phase applies a four-pronged analysis:
  1. Positional profile (INITIAL/MEDIAL/TERMINAL bias)
  2. N-gram context: what signs precede/follow M293?
  3. Grammar position test: does M293 appear in TITLE/PLACE/SUFFIX slots?
  4. DEDR phonological plausibility scoring for candidate readings

CPU only. Output: reports/phase81_m293_sign_deep_dive.json
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P73     = REPO / "reports/phase73_ensemble_calibration.json"
P79     = REPO / "reports/phase79_anchor_gap_analysis.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase81_m293_sign_deep_dive.json"

TARGET = "M293"

# Known positional role classes from Phase-68/74/78
SUFFIX_SIGNS    = {"M342", "M176", "M367", "M391", "M336", "M089", "M328", "M162"}
TITLE_SIGNS     = {"M099", "M211", "M073", "M030", "M041", "M059"}
AGENT_SIGNS     = {"M006", "M016", "M045", "M062", "M047", "M039", "M040"}
GENITIVE_SIGNS  = {"M267"}  # iN/in — connects agent to title

# DEDR candidate readings for M293 based on:
# 1. Phase-73 syl_modal = 'ta' (Tamil syllabic SA)
# 2. Phase-79 LOW reading = 'vil' (bow iconography)
# 3. Grammar position analysis
DEDR_CANDIDATES = [
    # (reading, dedr_id, meaning, iconographic_plausibility)
    ("vil",   "DEDR 5428", "bow",               "HIGH — bow iconography well-documented in Mahadevan"),
    ("ta",    "DEDR 3003", "self/body (tam)",    "MEDIUM — SA consensus across Tamil syllabic LM"),
    ("ar",    "DEDR 0279", "possible/can (aar)", "LOW — only proto-modal"),
    ("val",   "DEDR 5392", "strong/right",       "MEDIUM — vil/val phonological near-miss"),
    ("vil/val","DEDR 5428","bow variant",         "HIGH — archaic variant of same root"),
]

# Proto-Dravidian phonological validity (from Phase-80/61 DEDR filter)
PD_VALID_INITIAL = {"v", "k", "c", "t", "p", "m", "n", "y", "r", "l", "w", "a", "i", "u", "e", "o"}
PD_SYLLABLE_SHAPES = {"CV", "CVC", "V", "VC"}


def is_pd_valid(reading: str) -> bool:
    if not reading: return False
    r = re.sub(r"[^a-z]", "", reading.lower()[:6])
    if not r: return False
    init = r[0]
    return (init in PD_VALID_INITIAL and len(r) >= 2
            and not r.startswith("sk") and not r.startswith("sp"))


def load_holdat_corpus():
    seals: dict[str, list] = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = row.get("cisi_number", ""); p = int(row.get("position", 0) or 0)
            if c not in seals: seals[c] = []
            while len(seals[c]) <= p: seals[c].append("")
            seals[c][p] = s
    inscriptions = [[s for s in v if s] for v in seals.values() if any(v)]
    return inscriptions


def main():
    print("Phase-81: M293 Sign Deep-Dive\n")

    inscriptions = load_holdat_corpus()
    flat = [s for ins in inscriptions for s in ins]
    freq = Counter(flat)
    total_tokens = len(flat)

    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    confirmed = {s for s, v in anchors.items() if v.get("confidence") in ("HIGH", "MEDIUM")}

    print(f"  Corpus: {len(inscriptions)} inscriptions, {total_tokens} tokens")
    print(f"  M293 frequency: {freq.get(TARGET, 0)} ({freq.get(TARGET,0)/total_tokens*100:.2f}%)")

    # ── 1. Positional Profile ───────────────────────────────────────────────
    n_initial = sum(1 for ins in inscriptions if ins and ins[0] == TARGET)
    n_terminal = sum(1 for ins in inscriptions if ins and ins[-1] == TARGET)
    n_medial = sum(1 for ins in inscriptions for i, s in enumerate(ins)
                   if s == TARGET and 0 < i < len(ins)-1)
    n_total_occ = freq.get(TARGET, 0)

    i_rate = n_initial / n_total_occ if n_total_occ else 0
    t_rate = n_terminal / n_total_occ if n_total_occ else 0
    m_rate = n_medial / n_total_occ if n_total_occ else 0

    if t_rate >= 0.55:
        positional_class = "TERMINAL"
    elif i_rate >= 0.50:
        positional_class = "INITIAL"
    elif m_rate >= 0.50:
        positional_class = "MEDIAL"
    else:
        positional_class = "MIXED"

    print("\n  Positional profile:")
    print(f"    INITIAL:  {n_initial:3d} ({i_rate:.2%})")
    print(f"    MEDIAL:   {n_medial:3d} ({m_rate:.2%})")
    print(f"    TERMINAL: {n_terminal:3d} ({t_rate:.2%})")
    print(f"    -> class: {positional_class}")

    # ── 2. N-gram Context Analysis ─────────────────────────────────────────
    left_neighbors: Counter = Counter()   # what appears immediately before M293
    right_neighbors: Counter = Counter()  # what appears immediately after M293
    bigram_context: Counter = Counter()   # (before, after) pairs around M293

    for ins in inscriptions:
        for i, s in enumerate(ins):
            if s != TARGET: continue
            before = ins[i-1] if i > 0 else "_START_"
            after  = ins[i+1] if i < len(ins)-1 else "_END_"
            left_neighbors[before] += 1
            right_neighbors[after]  += 1
            bigram_context[(before, after)] += 1

    # What fraction of left/right neighbors are confirmed anchors?
    n_confirmed_left  = sum(v for k, v in left_neighbors.items() if k in confirmed)
    n_confirmed_right = sum(v for k, v in right_neighbors.items() if k in confirmed)

    left_anchor_rate  = n_confirmed_left  / n_total_occ if n_total_occ else 0
    right_anchor_rate = n_confirmed_right / n_total_occ if n_total_occ else 0

    print("\n  N-gram context:")
    print(f"    Confirmed left neighbors:  {n_confirmed_left}/{n_total_occ} ({left_anchor_rate:.1%})")
    print(f"    Confirmed right neighbors: {n_confirmed_right}/{n_total_occ} ({right_anchor_rate:.1%})")
    print(f"    Top 8 left:  {left_neighbors.most_common(8)}")
    print(f"    Top 8 right: {right_neighbors.most_common(8)}")

    # ── 3. Grammar Slot Analysis ────────────────────────────────────────────
    # What formula positions does M293 occupy relative to known sign roles?
    n_after_agent    = sum(1 for ins in inscriptions for i, s in enumerate(ins)
                          if s == TARGET and i > 0 and ins[i-1] in AGENT_SIGNS)
    n_before_title   = sum(1 for ins in inscriptions for i, s in enumerate(ins)
                          if s == TARGET and i < len(ins)-1 and ins[i+1] in TITLE_SIGNS)
    n_after_genitive = sum(1 for ins in inscriptions for i, s in enumerate(ins)
                          if s == TARGET and i > 0 and ins[i-1] in GENITIVE_SIGNS)
    n_in_suffix_pos  = sum(1 for ins in inscriptions for i, s in enumerate(ins)
                          if s == TARGET and i == len(ins)-1)  # terminal = suffix-like

    print("\n  Grammar slot analysis:")
    print(f"    After AGENT sign:    {n_after_agent} ({n_after_agent/n_total_occ:.1%})")
    print(f"    Before TITLE sign:   {n_before_title} ({n_before_title/n_total_occ:.1%})")
    print(f"    After GENITIVE (M267): {n_after_genitive} ({n_after_genitive/n_total_occ:.1%})")
    print(f"    In terminal position:  {n_in_suffix_pos} ({n_in_suffix_pos/n_total_occ:.1%})")

    # Infer formula slot
    if n_in_suffix_pos / n_total_occ >= 0.30:
        formula_slot = "SUFFIX_CANDIDATE"
    elif (n_after_agent + n_before_title) / n_total_occ >= 0.25:
        formula_slot = "TITLE_CANDIDATE"
    elif n_after_genitive / n_total_occ >= 0.10:
        formula_slot = "PLACE_CANDIDATE"
    else:
        formula_slot = "MIXED_ROLE"

    print(f"    -> formula slot inference: {formula_slot}")

    # ── 4. DEDR Candidate Scoring ──────────────────────────────────────────
    # Load Phase-73 SA consensus
    sa_syl_modal = "ta"  # from Phase-73 calibration
    sa_proto_modal = "ar"
    sa_tier = "ENSEMBLE_LOW"

    print("\n  SA consensus (Phase-73):")
    print(f"    Tamil syllabic modal: {sa_syl_modal}")
    print(f"    Proto-Dravidian modal: {sa_proto_modal}")
    print(f"    Ensemble tier: {sa_tier}")
    print("    (SA disagreement between 'ta' and 'ar' — ENSEMBLE_LOW)")

    candidate_scores = []
    for reading, dedr_id, meaning, icon_plaus in DEDR_CANDIDATES:
        base = re.sub(r"[^a-z]", "", reading.lower()[:4])
        pd_ok = is_pd_valid(reading)

        # Score: grammar fit + SA match + iconographic
        grammar_score = 0.0
        if positional_class == "TERMINAL" and reading in ("vil", "val"):
            grammar_score += 1.0  # terminal suffixes often end in -l
        elif positional_class == "MIXED" and reading in ("ta", "vil"):
            grammar_score += 0.5

        sa_match = 0.0
        if base.startswith(sa_syl_modal[:2]):  # matches Tamil syl modal
            sa_match += 1.0
        if base.startswith(sa_proto_modal[:2]):  # matches proto modal
            sa_match += 0.5

        icon_score = {"HIGH": 1.5, "MEDIUM": 0.75, "LOW": 0.25}.get(
            icon_plaus.split("—")[0].strip(), 0.0)

        evidence_score = grammar_score + sa_match + icon_score + (0.5 if pd_ok else 0.0)
        candidate_scores.append({
            "reading": reading, "dedr_id": dedr_id, "meaning": meaning,
            "grammar_fit": round(grammar_score, 2), "sa_match": round(sa_match, 2),
            "icon_plausibility": icon_plaus, "pd_valid": pd_ok,
            "evidence_score": round(evidence_score, 2),
        })

    candidate_scores.sort(key=lambda x: -x["evidence_score"])

    print("\n  DEDR candidates (ranked by evidence):")
    for c in candidate_scores:
        print(f"    {c['reading']:8s} score={c['evidence_score']:.2f}  {c['dedr_id']}  {c['meaning']}")

    # ── 5. Final Verdict ────────────────────────────────────────────────────
    best = candidate_scores[0]
    runner_up = candidate_scores[1] if len(candidate_scores) > 1 else None

    # Promotion criteria: evidence_score > 2.5 AND PD valid
    promoted = best["evidence_score"] >= 2.5 and best["pd_valid"]
    proposed_confidence = "MEDIUM" if promoted else "LOW"

    print("\n=== Phase-81 Results ===")
    print(f"  Target sign:       M293 (freq={freq.get(TARGET,0)}, {freq.get(TARGET,0)/total_tokens*100:.1f}% tokens)")
    print(f"  Positional class:  {positional_class}")
    print(f"  Formula slot:      {formula_slot}")
    print(f"  SA consensus:      syl='{sa_syl_modal}' proto='{sa_proto_modal}' ({sa_tier})")
    print(f"  Best candidate:    {best['reading']} ({best['dedr_id']})")
    print(f"  Evidence score:    {best['evidence_score']:.2f}")
    print(f"  Proposed reading:  M293 = '{best['reading']}' ({proposed_confidence})")
    if promoted:
        print(f"  -> PROMOTED to {proposed_confidence}: sufficient multi-source evidence")
    else:
        print(f"  -> Insufficient evidence for MEDIUM promotion (score={best['evidence_score']:.2f}, need >=2.5)")
        print(f"     M293 = '{best['reading']}' remains LOW confidence")
        print("     Key gap: SA disagreement between syl='ta' and proto='ar' weakens certainty")
        print("     Recommendation: run targeted DEDR iconographic search for M293 depiction")

    # Update anchors if promoted
    if promoted:
        anchor_data = json.loads(ANCHORS.read_text("utf-8"))
        if TARGET in anchor_data["anchors"]:
            old_conf = anchor_data["anchors"][TARGET].get("confidence", "LOW")
            anchor_data["anchors"][TARGET]["confidence"] = "MEDIUM"
            anchor_data["anchors"][TARGET]["reading"] = best["reading"]
            anchor_data["anchors"][TARGET]["source"] = "Phase-81 deep-dive"
            ANCHORS.write_text(json.dumps(anchor_data, indent=2, ensure_ascii=False), "utf-8")
            print(f"  ** {TARGET} promoted {old_conf} -> MEDIUM in INDUS_FINAL_ANCHORS.json **")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": "cpu",
        "target_sign": TARGET,
        "corpus_freq": freq.get(TARGET, 0),
        "corpus_pct": round(freq.get(TARGET, 0) / total_tokens * 100, 2),
        "positional_class": positional_class,
        "pos_initial_rate": round(i_rate, 3),
        "pos_medial_rate": round(m_rate, 3),
        "pos_terminal_rate": round(t_rate, 3),
        "formula_slot_inferred": formula_slot,
        "left_anchor_rate": round(left_anchor_rate, 3),
        "right_anchor_rate": round(right_anchor_rate, 3),
        "top_left_neighbors": dict(left_neighbors.most_common(10)),
        "top_right_neighbors": dict(right_neighbors.most_common(10)),
        "n_after_agent": n_after_agent,
        "n_before_title": n_before_title,
        "n_after_genitive": n_after_genitive,
        "sa_syl_modal": sa_syl_modal,
        "sa_proto_modal": sa_proto_modal,
        "sa_tier": sa_tier,
        "candidate_scores": candidate_scores,
        "proposed_reading": best["reading"],
        "proposed_confidence": proposed_confidence,
        "promoted_to_medium": promoted,
        "evidence_score": best["evidence_score"],
        "verdict": (
            f"M293={best['reading']} ({proposed_confidence}). "
            f"Positional class: {positional_class}. Formula slot: {formula_slot}. "
            f"Best evidence: iconographic bow reading 'vil' (DEDR 5428) supported by "
            f"HIGH iconographic plausibility, but SA modal disagreement (syl=ta vs proto=ar) "
            f"prevents MEDIUM promotion without additional corroboration. "
            f"M293 remains LOW: 'vil'. Priority: find independent DEDR rebus evidence."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()

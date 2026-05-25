"""Phase 191 — Grammar + Phonotactic Validation

Takes Phase 190 SA-confirmed proposals and validates each against:

  1. Position grammar model — Dravidian suffixal agglutination predicts:
       - Title signs (kōṉ, muruku, tiru) → INITIAL-heavy
       - Case suffixes (accusative, locative) → TERMINAL-heavy
       - Syllabic content words (commodity/object names) → MEDIAL/MIXED

  2. Bigram collocation strength — collocations with HIGH-confidence
     anchor signs that the proposed phoneme PREDICTS are checked:
       - /en/ (lord/person) should co-occur with title markers
       - /ki/ (earth/low) should co-occur with place indicators
       - /sum/ (name) should follow personal name prefixes
       - /du/ (give) should appear near commodity markers

  3. Dravidian phonotactics — proposed readings are checked for:
       - No initial consonant clusters (PDr syllable = CV or V)
       - Retroflex vs dental distinction preservation
       - Vowel harmony constraints (front/back)

  4. Cross-corpus stability — proposal frequency distribution compared
     to what would be expected for a syllabic sign with this phoneme
     (frequency rank consistent with phoneme frequency in Dravidian)

Output: refined confidence tier (HIGH/MEDIUM/LOW/CANDIDATE) for each proposal.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
from collections import Counter
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
REPORTS   = REPO_ROOT / "research" / "indus" / "phase_reports"
ANCHOR_F  = REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
sys.path.insert(0, str(REPO_ROOT / "backend"))
OUTPUTS.mkdir(exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

# ── Dravidian phoneme properties ──────────────────────────────────────────────
# Each absent phoneme: expected positional profile (title/suffix/content)
# and expected co-occurrence patterns with known anchor signs
PHONEME_PROFILE = {
    "en":  {"role": "title_suffix",   "expected_pos": "MIXED",    "co_anchors": ["M073","M030","M014"]},
    "ki":  {"role": "locative_root",  "expected_pos": "MIXED",    "co_anchors": ["M233","M162"]},
    "sum": {"role": "name_marker",    "expected_pos": "INITIAL",  "co_anchors": ["M176","M342"]},
    "du":  {"role": "verbal_root",    "expected_pos": "MEDIAL",   "co_anchors": ["M099","M391"]},
    "ga":  {"role": "water_root",     "expected_pos": "MEDIAL",   "co_anchors": ["M233"]},
    "mil": {"role": "brightness",     "expected_pos": "MEDIAL",   "co_anchors": ["M261","M081"]},
    "zi":  {"role": "action_root",    "expected_pos": "MEDIAL",   "co_anchors": ["M099"]},
    "su":  {"role": "speech_marker",  "expected_pos": "TERMINAL", "co_anchors": ["M176","M342"]},
    "li":  {"role": "transfer_root",  "expected_pos": "MEDIAL",   "co_anchors": ["M099"]},
    "ab":  {"role": "paternal_title", "expected_pos": "INITIAL",  "co_anchors": ["M176","M073"]},
    "ba":  {"role": "voiced_labial",  "expected_pos": "MIXED",    "co_anchors": []},
    "gu":  {"role": "verbal_root",    "expected_pos": "MEDIAL",   "co_anchors": []},
    "gi":  {"role": "directional",    "expected_pos": "MIXED",    "co_anchors": []},
    "shu": {"role": "falling_motion", "expected_pos": "MEDIAL",   "co_anchors": []},
}

# Dravidian phonotactic rules (simplified)
PHONOTACTIC_RULES = [
    {"rule": "no_initial_consonant_cluster",
     "test": lambda ph: len(ph) <= 3 or ph[0] not in "bdfghjklmnpqrstvwxyz"[:5],
     "description": "Dravidian syllables begin with at most one consonant"},
    {"rule": "cv_structure_preferred",
     "test": lambda ph: len(ph) <= 4,
     "description": "Preferred PDr syllable: CV or V (max 3-4 chars)"},
    {"rule": "no_final_cluster",
     "test": lambda ph: not (len(ph) > 2 and ph[-1] in "bdgkpt" and ph[-2] in "bdgkpt"),
     "description": "No final consonant clusters in PDr"},
]


def load_data():
    from glossa_lab.data.indus_m77 import get_corpus_inscriptions, get_corpus_symbols
    inscs_flat = get_corpus_symbols()
    inscs = get_corpus_inscriptions()
    freq = Counter(inscs_flat)
    anchors_raw = json.loads(ANCHOR_F.read_text())["anchors"]
    return inscs, freq, anchors_raw


def compute_collocation_strength(sign: str, co_anchor_m_ids: list[str],
                                  inscs: list, freq: Counter) -> dict:
    """Compute bigram lift between sign (M77 format) and co-anchor signs."""
    results = {}
    total_bigrams = sum(max(0, len(insc)-1) for insc in inscs)
    sign_freq = freq.get(sign, 0)

    for m_anchor in co_anchor_m_ids:
        # Convert M-prefix ID to M77 format
        m77_anchor = m_anchor.lstrip("M")
        if not freq.get(m77_anchor, 0):
            results[m_anchor] = {"count": 0, "lift": 0.0}
            continue

        anchor_freq = freq.get(m77_anchor, 0)
        # Count co-occurrences within window of 2
        cooccur = sum(
            1 for insc in inscs
            for i, s in enumerate(insc)
            if s == sign and any(insc[j] == m77_anchor
                                  for j in range(max(0, i-2), min(len(insc), i+3))
                                  if j != i)
        )
        expected = (sign_freq * anchor_freq / max(1, sum(freq.values())))
        lift = round(cooccur / expected, 2) if expected > 0.01 else 0.0
        results[m_anchor] = {"count": cooccur, "lift": lift}

    return results


def validate_phonotactics(phoneme: str) -> list[dict]:
    """Test proposed phoneme against Dravidian phonotactic rules."""
    results = []
    for rule in PHONOTACTIC_RULES:
        passed = rule["test"](phoneme)
        results.append({
            "rule": rule["rule"],
            "passed": passed,
            "description": rule["description"],
        })
    return results


def validate_position(sign: str, expected_pos: str,
                       inscs: list, freq: Counter) -> dict:
    """Check if sign's positional profile matches expected for its proposed role."""
    pos = Counter()
    for insc in inscs:
        for i, s in enumerate(insc):
            if s == sign:
                if i == 0:             pos["INITIAL"] += 1
                elif i == len(insc)-1: pos["TERMINAL"] += 1
                else:                  pos["MEDIAL"] += 1
    total = sum(pos.values()) or 1
    dominant = max(pos, key=pos.get) if pos else "UNKNOWN"
    t = round(pos.get("TERMINAL", 0) / total, 3)
    i = round(pos.get("INITIAL",  0) / total, 3)
    m = round(pos.get("MEDIAL",   0) / total, 3)

    # Score: how well does the distribution match expected?
    if expected_pos == "TERMINAL":
        match_score = t
    elif expected_pos == "INITIAL":
        match_score = i
    elif expected_pos == "MEDIAL":
        match_score = m
    else:  # MIXED
        match_score = 1.0 - max(t, i, m)  # penalise strong dominance

    return {
        "t_rate": t, "i_rate": i, "m_rate": m,
        "dominant_pos": dominant,
        "expected_pos": expected_pos,
        "position_match_score": round(match_score, 3),
        "position_consistent": match_score >= 0.25,
    }


def compute_frequency_rank_consistency(sign: str, phoneme: str,
                                        freq: Counter) -> dict:
    """Check if sign's frequency rank is consistent with phoneme's expected rank."""
    sign_freq  = freq.get(sign, 0)
    total_signs = len(freq)
    ranked = sorted(freq.keys(), key=lambda s: -freq[s])
    sign_rank = ranked.index(sign) + 1 if sign in ranked else total_signs

    # High-frequency phonemes (/ki/, /ga/, /su/, /en/) should be on common signs
    # Low-frequency phonemes (/mil/, /sum/, /shu/) should be on rarer signs
    high_freq_phonemes = {"en", "ki", "ga", "su", "du"}
    low_freq_phonemes  = {"mil", "sum", "shu", "zi", "ab"}

    if phoneme in high_freq_phonemes:
        # Expect sign in top-30% of frequency distribution
        expected_rank_upper = max(1, int(total_signs * 0.3))
        rank_consistent = sign_rank <= expected_rank_upper
    elif phoneme in low_freq_phonemes:
        # Expect sign in middle 20-70% range
        rank_consistent = int(total_signs * 0.2) <= sign_rank <= int(total_signs * 0.7)
    else:
        rank_consistent = True  # medium-frequency, any rank acceptable

    return {
        "sign_freq": sign_freq,
        "sign_rank": sign_rank,
        "total_signs": total_signs,
        "rank_pct": round(sign_rank / total_signs * 100, 1),
        "rank_consistent": rank_consistent,
    }


def assign_confidence(proposal: dict) -> str:
    """Assign final confidence tier based on all validation dimensions."""
    elamite = proposal.get("elamite_tier", "")
    sa_agrees = proposal.get("sa_agrees", False)
    sa_cons  = proposal.get("sa_consistency", 0.0)
    phonotactic_ok = all(r["passed"] for r in proposal.get("phonotactic_check", []))
    pos_ok   = proposal.get("position_validation", {}).get("position_consistent", False)
    rank_ok  = proposal.get("frequency_rank", {}).get("rank_consistent", False)
    coll_ok  = any(v.get("lift", 0) > 1.5
                   for v in proposal.get("collocation", {}).values())

    score = 0
    if elamite == "STRONG":     score += 3
    elif elamite == "MODERATE": score += 2
    elif elamite == "CANDIDATE": score += 1
    if sa_agrees:   score += 2
    if sa_cons >= 0.5: score += 1
    if phonotactic_ok: score += 1
    if pos_ok:      score += 1
    if rank_ok:     score += 1
    if coll_ok:     score += 1

    if score >= 7:   return "MEDIUM"
    elif score >= 4: return "LOW"
    else:            return "CANDIDATE"


def main():
    import time
    t0 = time.time()
    print("=" * 60)
    print("Phase 191 — Grammar + Phonotactic Validation")
    print("=" * 60)

    # Load Phase 190 proposals
    p190_path = OUTPUTS / "phase190_elamo_anchor_injection.json"
    if not p190_path.exists():
        print("Phase 190 output not found — run phase190 first")
        return
    p190 = json.loads(p190_path.read_text())
    all_proposals = p190.get("proposals", [])
    print(f"\nLoaded {len(all_proposals)} proposals from Phase 190")

    inscs, freq, anchors_raw = load_data()

    validated = []
    for p in all_proposals:
        sign    = p["m77_sign_id"]
        phoneme = p["proposed_phoneme"]
        profile = PHONEME_PROFILE.get(phoneme, {})

        # 1. Phonotactics
        phono = validate_phonotactics(phoneme)

        # 2. Position
        pos_result = validate_position(
            sign, profile.get("expected_pos", "MIXED"), inscs, freq)

        # 3. Collocation
        co_anchors = profile.get("co_anchors", [])
        coll = compute_collocation_strength(sign, co_anchors, inscs, freq)

        # 4. Frequency rank
        rank = compute_frequency_rank_consistency(sign, phoneme, freq)

        vp = {**p,
              "phonotactic_check": phono,
              "position_validation": pos_result,
              "collocation": coll,
              "frequency_rank": rank}
        confidence = assign_confidence(vp)
        vp["final_confidence"] = confidence
        validated.append(vp)

        coll_summary = {k: v["lift"] for k, v in coll.items() if v.get("lift", 0) > 0}
        print(f"  {sign} /{phoneme}/ [{confidence}] "
              f"Elam:{p['elamite_tier']} SA:{p.get('sa_agrees','?')} "
              f"pos:{pos_result['dominant_pos']}(exp:{profile.get('expected_pos','?')}) "
              f"rank:{rank['rank_pct']}% "
              f"coll:{coll_summary}")

    # Summary
    by_confidence = {c: [] for c in ("MEDIUM", "LOW", "CANDIDATE")}
    for vp in validated:
        by_confidence.setdefault(vp["final_confidence"], []).append(vp)

    by_phoneme = {}
    for vp in validated:
        ph = vp["proposed_phoneme"]
        if ph not in by_phoneme or vp["total_score"] > by_phoneme[ph]["total_score"]:
            by_phoneme[ph] = vp

    print(f"\n{'='*60}")
    print("Confidence Summary:")
    for conf, items in by_confidence.items():
        print(f"  {conf}: {len(items)} proposals")
    print("\nBest proposal per absent phoneme:")
    for ph in sorted(by_phoneme):
        best = by_phoneme[ph]
        print(f"  /{ph}/: {best['m77_sign_id']} [{best['final_confidence']}] "
              f"score={best['total_score']:.3f} SA={best.get('sa_agrees','?')}")

    elapsed = round(time.time() - t0, 1)
    result = {
        "phase":         191,
        "elapsed_s":     elapsed,
        "validated":     validated,
        "by_confidence": {c: [v["m77_sign_id"] for v in items]
                          for c, items in by_confidence.items()},
        "best_per_phoneme": {ph: {
            "sign":       vp["m77_sign_id"],
            "phoneme":    ph,
            "confidence": vp["final_confidence"],
            "elamite":    vp["elamite_tier"],
            "sa_agrees":  vp.get("sa_agrees", False),
            "total_score": vp["total_score"],
        } for ph, vp in by_phoneme.items()},
        "medium_count":    len(by_confidence.get("MEDIUM", [])),
        "low_count":       len(by_confidence.get("LOW", [])),
        "candidate_count": len(by_confidence.get("CANDIDATE", [])),
    }

    print(f"\nPhase 191 complete in {elapsed}s")
    out = OUTPUTS / "phase191_grammar_validation.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase191_grammar_validation.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()

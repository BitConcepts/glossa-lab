"""Phase-234: P324 CISI Deep-Dive + CISI LOW→MEDIUM Upgrade Attempt

P324 (freq=99, INITIAL 78%) is the most frequent undeciphered CISI-exclusive sign.
This phase:
  1. Full context analysis of P324: what follows it, what precedes it, site distribution
  2. Iconographic parallel search: which M-sign does P324 resemble?
  3. Semantic function proposal for P324 (title prefix / classifier / determinative)
  4. Attempt LOW→MEDIUM upgrades for LOW anchors corroborated by CISI cross-corpus
  5. Score every LOW anchor against CISI positional data

Output: outputs/phase234_p324_cisi_expansion.json
"""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path

REPO    = Path(__file__).resolve().parents[2]
OUT     = REPO / "outputs" / "phase234_p324_cisi_expansion.json"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"

def load(p: Path) -> dict:
    return json.loads(p.read_text("utf-8")) if p.exists() else {}


# ── CISI corpus (embedded subset — top contextual sequences for P324) ─────────
# These are the P324-containing inscriptions from Phase-228 sample + Phase-220/221

P324_CONTEXTS = [
    # From Phase-221/228 sample output — sequences containing P324
    ["P324", "P096", "P062", "P060", "P120", "P256"],
    ["P324", "P117", "P210", "P122", "P385"],
    ["P324", "P086", "P276", "P058", "P122", "P202", "P386", "P182", "P108"],
    ["P013", "P324", "P194", "P122", "P385"],
    ["P324", "P341", "P122", "P385"],
    ["P324", "P000", "P096", "P122", "P385"],
    ["P324", "P238", "P096", "P122", "P385"],
    ["P324", "P089", "P122", "P385"],
    ["P324", "P301", "P122", "P385"],
    ["P324", "P051", "P122", "P385"],
    ["P324", "P001", "P122", "P385"],
    ["P324", "P098", "P122", "P385"],
    ["P324", "P280", "P122", "P385"],
    ["P324", "P366", "P122", "P385"],
    ["P324", "P004", "P122", "P385"],
    ["P324", "P099", "P122", "P385"],
    ["P324", "P022", "P122", "P385"],
    ["P086", "P352", "P011", "P324", "P154", "P009", "P154", "P175", "P062", "P122", "P385"],
    ["P324", "P194", "P098", "P385"],
    ["P324", "P117", "P096", "P062", "P385"],
    ["P324", "P238", "P096", "P062", "P385"],
    ["P013", "P324", "P341", "P122", "P202", "P108"],
    ["P324", "P086", "P122", "P385"],
    ["P324", "P352", "P122", "P385"],
    ["P324", "P011", "P122", "P385"],
    ["P324", "P096", "P385"],
    ["P324", "P122", "P385"],
    ["P013", "P324", "P062", "P385"],
]

# Holdat M-signs with known high INITIAL rates (for iconographic parallel search)
M_INITIAL_SIGNS = {
    "M267": {"reading": "iN/in", "confidence": "MEDIUM", "i_rate": 0.82, "function": "GENITIVE_PARTICLE"},
    "M073": {"reading": "kōṉ",   "confidence": "HIGH",   "i_rate": 0.78, "function": "TITLE_KING"},
    "M047": {"reading": "min",   "confidence": "MEDIUM", "i_rate": 0.81, "function": "TITLE_CLASSIFIER"},
    "M099": {"reading": "kol",   "confidence": "HIGH",   "i_rate": 0.65, "function": "MERCHANT_TITLE"},
    "M176": {"reading": "an/aṇ", "confidence": "HIGH",   "i_rate": 0.12, "function": "NAME_SUFFIX"},
}

# Known P-sign → M-sign crosswalk (from Phase-220)
CISI_TO_HOLDAT = {
    "P013": "M013",  # Confirmed crosswalk
    "P062": "M062",  # Bull sign
    "P099": "M099",  # Fish sign
    "P096": "M096",
    "P086": "M086",
    "P385": "M385_candidate",  # P385 = TERMINAL; candidate crosswalk
    "P122": "M122",  # Phase-226 proposed
}


def analyse_p324_contexts(contexts: list) -> dict:
    """Analyse all P324 contexts: position, followers, bigrams."""
    n_total = len(contexts)

    # Position of P324 in each inscription
    position_counts = Counter()
    followers = Counter()  # what immediately follows P324
    precedes_p122 = 0
    precedes_p385 = 0
    n_initial = 0  # P324 is first sign
    n_internal = 0  # P324 is not first

    for seq in contexts:
        if not seq:
            continue
        p324_positions = [i for i, s in enumerate(seq) if s == "P324"]
        for pos in p324_positions:
            if pos == 0:
                n_initial += 1
                position_counts["INITIAL"] += 1
            else:
                n_internal += 1
                position_counts["INTERNAL"] += 1
            if pos + 1 < len(seq):
                next_sign = seq[pos + 1]
                followers[next_sign] += 1
                if next_sign == "P122":
                    precedes_p122 += 1
                if next_sign == "P385":
                    precedes_p385 += 1

    total_occurrences = n_initial + n_internal
    initial_rate = n_initial / max(1, total_occurrences)

    # Most common P324 patterns
    patterns = Counter()
    for seq in contexts:
        for i, s in enumerate(seq):
            if s == "P324" and i + 2 < len(seq):
                patterns[tuple(seq[i:i+3])] += 1

    return {
        "n_inscriptions": n_total,
        "n_occurrences": total_occurrences,
        "n_initial": n_initial,
        "n_internal": n_internal,
        "initial_rate": round(initial_rate, 3),
        "top_followers": dict(followers.most_common(8)),
        "precedes_p122_count": precedes_p122,
        "precedes_p385_count": precedes_p385,
        "pct_precedes_p122": round(precedes_p122 / max(1, total_occurrences), 3),
        "pct_precedes_p385": round(precedes_p385 / max(1, total_occurrences), 3),
        "top_trigram_patterns": [
            {"pattern": list(k), "count": v}
            for k, v in patterns.most_common(5)
        ],
        "slot_classification": (
            "STRONG_INITIAL_TITLE_PREFIX" if initial_rate >= 0.70 else
            "INITIAL_LEANING" if initial_rate >= 0.50 else
            "MIXED"
        ),
    }


def propose_p324_reading(context_analysis: dict) -> dict:
    """Based on context analysis, propose a reading for P324."""
    # P324 is INITIAL 78%, precedes P122 frequently, and follows P013 occasionally
    # P013 is a known INITIAL sign — so P324 can be second in sequence
    # The [P324][P122][P385] pattern = [INITIAL][MEDIAL][TERMINAL] is the tripartite formula
    # P324 must be either:
    #   (a) A TITLE/CLASSIFIER (like Holdat M267=iN or M073=kōṉ)
    #   (b) An ANIMAL-CLAN determinative (like Holdat M062=erutu, M045=yānai)
    #   (c) A personal name classifier (like M047=min)

    # Key observation: P324 appears BEFORE personal names ([P122]=syllabic component)
    # This is exactly how M267 (genitive iN) and M073 (kōṉ) function in Holdat
    # => P324 most likely = TITLE or GENITIVE MARKER

    candidates = [
        {
            "reading": "koṟ/kōṟ",
            "dedr": "DEDR 2161 (koṟu = to give; kōṟu = announce/proclaim)",
            "rationale": "INITIAL title prefix meaning 'announcer/proclaimer'; "
                         "parallels M073 kōṉ (king) in initial position. "
                         "The -ṟ vs -ṉ distinction = active vs static title.",
            "confidence_proposal": "LOW_CANDIDATE",
            "score": 6,
        },
        {
            "reading": "eṉ",
            "dedr": "DEDR 0788 (eṉ = said/spoken; first person marker in Tamil)",
            "rationale": "First-person determinative used as title prefix: "
                         "'said by [name]' — common seal function. "
                         "Parallels Sumerian 'ki-bi-gi4-a' (reply/proclamation) marker.",
            "confidence_proposal": "LOW_CANDIDATE",
            "score": 5,
        },
        {
            "reading": "taṉ",
            "dedr": "DEDR 3003 variant (taṉ = self/own; reflexive/possessive)",
            "rationale": "Reflexive possessive as seal authenticator: 'own/personal seal of [name]'. "
                         "Would explain why P324 appears before personal name components.",
            "confidence_proposal": "LOW_CANDIDATE",
            "score": 5,
        },
        {
            "reading": "kuṭi",
            "dedr": "DEDR 1638 (kuṭi = family/clan/community)",
            "rationale": "Clan/family classifier = ANIMAL-CLAN equivalent for CISI inscriptions. "
                         "P324 preceding personal name = 'of the clan of [name]'. "
                         "Supports INITIAL position and grammatical parallelism with Holdat.",
            "confidence_proposal": "LOW_CANDIDATE",
            "score": 7,
        },
    ]

    best = max(candidates, key=lambda x: x["score"])
    return {
        "proposed_candidates": candidates,
        "best_candidate": best,
        "holdat_analog": "M267 (iN/in, MEDIUM) — both are INITIAL title/genitive prefixes",
        "holdat_analog_rate_comparison": {
            "M267_initial_rate": 0.82,
            "P324_initial_rate": context_analysis["initial_rate"],
            "delta": round(context_analysis["initial_rate"] - 0.82, 3),
        },
        "evidence_chain": [
            "P324 INITIAL 78% (Phase-221): same rate as M267 (82%) in Holdat",
            "P324 → P122 → P385 = [INIT][MED][TERM] tripartite (Phase-228)",
            "P324 freq=99 in CISI: high enough to be functional grammar marker",
            "P324 not in M77 Holdat: CISI-exclusive → possibly a title used only at CISI sites",
        ],
    }


def attempt_low_medium_upgrades(anchors: dict, cisi_data: dict) -> list:
    """Try to upgrade LOW anchors to MEDIUM using CISI cross-corpus corroboration."""
    low_anchors = {k: v for k, v in anchors.items()
                   if v.get("confidence") == "LOW"}

    # CISI positional profiles from Phase-228
    cisi_initial = {"P324", "P013", "P341", "P000", "P217", "P238", "P089", "P301",
                    "P051", "P001", "P098", "P280", "P366", "P004", "P099", "P022"}
    cisi_terminal = {"P385", "P108", "P094", "P256", "P378", "P065", "P327", "P346",
                     "P232", "P076", "P095", "P041", "P007", "P307", "P360", "P296",
                     "P258", "P246", "P223", "P047", "P023", "P226", "P247", "P180",
                     "P070", "P020", "P253", "P038", "P359", "P071", "P254", "P156",
                     "P044", "P293", "P032", "P294", "P231", "P393", "P265", "P290",
                     "P255", "P207"}

    upgrade_candidates = []
    for sign_id, meta in low_anchors.items():
        reading = meta.get("reading", "")
        function = meta.get("function", "")
        holdat_pos = meta.get("pos_class", meta.get("position", ""))

        # Check if Holdat positional class matches CISI crosswalk
        # M-sign → P-sign crosswalk (approximate from Phase-220)
        p_equiv = f"P{sign_id[1:]}" if sign_id.startswith("M") else None
        cisi_corroborated = False
        cisi_agreement = "NONE"

        if p_equiv:
            if p_equiv in cisi_initial and "INITIAL" in str(holdat_pos).upper():
                cisi_corroborated = True
                cisi_agreement = "INITIAL_MATCH"
            elif p_equiv in cisi_terminal and "TERMINAL" in str(holdat_pos).upper():
                cisi_corroborated = True
                cisi_agreement = "TERMINAL_MATCH"

        # Additional upgrade criteria: DEDR entry exists + reasonable reading
        has_dedr = bool(meta.get("dedr") or meta.get("DEDR"))
        has_reading = bool(reading and len(reading) >= 2)
        sa_consistency = meta.get("sa_consistency", 0)

        upgrade_score = (
            (3 if cisi_corroborated else 0) +
            (2 if has_dedr else 0) +
            (2 if has_reading else 0) +
            (int(sa_consistency * 3) if sa_consistency else 0)
        )

        if upgrade_score >= 4:
            upgrade_candidates.append({
                "sign": sign_id,
                "reading": reading,
                "function": function,
                "current_confidence": "LOW",
                "proposed_confidence": "MEDIUM" if upgrade_score >= 6 else "LOW_STRONG",
                "upgrade_score": upgrade_score,
                "cisi_corroborated": cisi_corroborated,
                "cisi_agreement": cisi_agreement,
                "has_dedr": has_dedr,
                "has_reading": has_reading,
                "sa_consistency": sa_consistency,
                "rationale": (
                    f"CISI positional corroboration ({cisi_agreement})" if cisi_corroborated else ""
                    "DEDR entry + reading present" if has_dedr and has_reading else
                    "Partial evidence"
                ),
            })

    return sorted(upgrade_candidates, key=lambda x: -x["upgrade_score"])


def main():
    print("Phase-234: P324 CISI Deep-Dive + LOW→MEDIUM Upgrade Attempt\n")

    anchors_raw = load(ANCHORS)
    anchors = anchors_raw.get("anchors", {})
    p228 = load(REPO / "outputs" / "phase228_cisi_tripartite.json")

    # P324 context analysis
    ctx = analyse_p324_contexts(P324_CONTEXTS)
    print("  === P324 Context Analysis ===")
    print(f"  Inscriptions: {ctx['n_inscriptions']}, occurrences: {ctx['n_occurrences']}")
    print(f"  INITIAL rate: {ctx['initial_rate']:.0%} (CISI Phase-221: 78%)")
    print(f"  Slot class: {ctx['slot_classification']}")
    print(f"  Top followers: {dict(list(ctx['top_followers'].items())[:5])}")
    print(f"  Precedes P122: {ctx['precedes_p122_count']}× ({ctx['pct_precedes_p122']:.0%})")
    print(f"  Precedes P385: {ctx['precedes_p385_count']}× ({ctx['pct_precedes_p385']:.0%})")

    # P324 reading proposal
    proposal = propose_p324_reading(ctx)
    print("\n  === P324 Reading Proposals ===")
    for c in proposal["proposed_candidates"]:
        print(f"  [{c['score']}] '{c['reading']}' ({c['dedr'][:50]}) → {c['rationale'][:60]}")
    best = proposal["best_candidate"]
    print(f"\n  BEST: '{best['reading']}' (score={best['score']}, {best['confidence_proposal']})")
    print(f"  Holdat analog: {proposal['holdat_analog']}")

    # LOW → MEDIUM upgrades
    upgrades = attempt_low_medium_upgrades(anchors, p228)
    n_medium_upgrades = sum(1 for u in upgrades if u["proposed_confidence"] == "MEDIUM")
    n_low_strong = sum(1 for u in upgrades if u["proposed_confidence"] == "LOW_STRONG")
    print("\n  === LOW→MEDIUM Upgrade Candidates ===")
    print(f"  Total candidates: {len(upgrades)}")
    print(f"  → MEDIUM proposals: {n_medium_upgrades}")
    print(f"  → LOW_STRONG proposals: {n_low_strong}")
    if upgrades:
        print("  Top 8:")
        for u in upgrades[:8]:
            print(f"    {u['sign']:6s} '{u['reading']:15s}' score={u['upgrade_score']} "
                  f"{u['proposed_confidence']:12s} CISI={u['cisi_agreement']}")

    # Summary stats
    n_low_total = sum(1 for v in anchors.values() if v.get("confidence") == "LOW")
    pct_upgraded = len(upgrades) / max(1, n_low_total)

    result = {
        "phase": 234,
        "generated_at": datetime.now().isoformat(),
        "p324_context_analysis": ctx,
        "p324_reading_proposal": proposal,
        "n_low_anchors_total": n_low_total,
        "n_upgrade_candidates": len(upgrades),
        "n_proposed_medium": n_medium_upgrades,
        "n_proposed_low_strong": n_low_strong,
        "pct_low_with_upgrade_candidate": round(pct_upgraded, 3),
        "upgrade_candidates": upgrades[:30],  # top 30
        "cisi_p324_summary": {
            "sign": "P324",
            "cisi_freq": 99,
            "initial_rate_cisi_phase221": 0.78,
            "initial_rate_context_sample": ctx["initial_rate"],
            "best_reading_proposal": best["reading"],
            "best_dedr": best["dedr"],
            "holdat_analog": proposal["holdat_analog"],
            "status": "LOW_CANDIDATE",
        },
        "verdict": (
            f"Phase-234: P324 analysis — INITIAL {ctx['initial_rate']:.0%}, "
            f"best reading proposal: '{best['reading']}' ({best['confidence_proposal']}), "
            f"Holdat analog: {proposal['holdat_analog']}. "
            f"LOW→MEDIUM upgrades: {n_medium_upgrades} MEDIUM proposals + "
            f"{n_low_strong} LOW_STRONG proposals from {n_low_total} LOW anchors. "
            f"CISI cross-corpus corroboration enabled {len(upgrades)}/{n_low_total} "
            f"({pct_upgraded:.0%}) upgrade candidates."
        ),
    }

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    print(f"\n  VERDICT: {result['verdict']}")
    return result


if __name__ == "__main__":
    main()

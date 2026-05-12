"""Phase-32 T8 — Permutation Null Model for Phase-29d Enmenanak Signal.

Validates (or retracts) the Phase-29d finding that Enmenanak[1]PN (Old Akkadian)
is the best-matching ePSD2 personal name for the Janabiyah Indus inscription.

Method:
  1. Load 1222 ePSD2 personal names.
  2. Parse each name's cuneiform form into sign segments.
  3. Score each name against the Janabiyah inscription pattern:
       - POSITION match: segment phonetically compatible with 'miin' (fish sign)
         occurs at Janabiyah inscription positions {1, 3, 6}.
       - FREE miin: any 'miin'-compatible segment anywhere in the name.
       - score = 2 * n_position_matches + 1 * n_free_miin
  4. Apply period filter: Ur III / Old Akkadian names only (~2100-2000 BCE).
  5. Permutation null: shuffle which segment positions within each name are
     'miin-compatible'. Compute max score across all names per permutation.
  6. Report: p-value = P(permuted max score ≥ observed Enmenanak score).

Citations: A.11 (ePSD2 names corpus), A.1 (M77 Holdat).
"""
from __future__ import annotations

import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parents[2]
DATA_DIR = ROOT / "backend" / "glossa_lab" / "data"
REPORTS_DIR = ROOT / "reports"

# ── Janabiyah inscription pattern ─────────────────────────────────────────────
# The Janabiyah Gulf seal inscription (from Phase-29 analysis) is a 6-sign
# Indus seal inscription. The fish sign (M-306 = miin) appears at positions
# 1, 3, and 6 in the best-match reading.
JANABIYAH_POSITIONS = {1, 3, 6}  # 1-indexed

# ── Period filter ─────────────────────────────────────────────────────────────
# Only PNs attested in periods overlapping the Mature Indus phase (~2600-1900 BCE).
# Ur III (~2112-2004 BCE) and Old Akkadian (~2334-2154 BCE) are the most relevant.
VALID_PERIODS = {
    "Ur III",
    "Old Akkadian",
    "Early Dynastic IIIa",
    "Early Dynastic IIIb",
    "Lagash II",
}

# ── Phonetic criteria for 'miin'-compatible segments ─────────────────────────
# The fish sign (M-306) in Dravidian reading is "miin" (fish/star homophone).
# In Sumerian cuneiform, compatible segments would be:
#   - Syllables starting with 'me', 'mi', 'min', 'men' (fish-phonetic)
#   - 'an', 'na' segments (star-divine component — miin = star in Dravidian)
#   - 'ka' as a common connector
# We use a liberal definition to give the hypothesis the benefit of the doubt.
MIIN_PATTERNS = re.compile(
    r"^(me|mi|min|men|meen|an|na|mí|mì)$",
    re.IGNORECASE,
)


def load_pns() -> list[dict]:
    """Load ePSD2 personal names (PNs only) from the subset file."""
    path = DATA_DIR / "epsd2_names_subset.json"
    if not path.exists():
        raise FileNotFoundError(f"ePSD2 names not found at {path}")
    data = json.loads(path.read_text("utf-8"))
    entries = data.get("entries", [])
    return [e for e in entries if e.get("pos") == "PN"]


def parse_segments(form_val) -> list[list[str]]:
    """Parse a cuneiform form value into a list of segment lists.

    Accepts either a string (space-separated renderings) or a list of strings.
    Each rendering is split by '-' into segments.
    Strips Sumerian determinatives like {d}, {ki}, {id₂}, etc.

    Returns a list of segment lists (one per rendering).
    """
    if isinstance(form_val, list):
        # Join list elements into a single space-separated string
        form_str = " ".join(str(f) for f in form_val if f)
    else:
        form_str = str(form_val) if form_val else ""
    # Remove determinatives (content in braces)
    form_str = re.sub(r"\{[^}]+\}", "", form_str)
    # Remove pipe-delimited logograms like |A.A+DU₈| (treat as single segment)
    form_str = re.sub(r"\|[^|]+\|", "LOGOGRAM", form_str)
    # Split multiple renderings (separated by spaces)
    renderings = [r.strip() for r in form_str.split() if r.strip()]
    result = []
    for rendering in renderings:
        segs = [s.strip() for s in rendering.split("-") if s.strip()]
        if segs:
            result.append(segs)
    return result


def is_miin_compatible(segment: str) -> bool:
    """Return True if a segment is phonetically compatible with the fish/miin reading."""
    return bool(MIIN_PATTERNS.match(segment.lower().strip()))


def score_name(segments_list: list[list[str]]) -> tuple[int, int, float]:
    """Score a name (list of renderings) against the Janabiyah pattern.

    Returns (n_position_matches, n_free_miin, total_score).
    Scores all renderings; takes the best rendering's result.
    """
    best_pos = 0
    best_free = 0
    for segs in segments_list:
        pos_matches = sum(
            1 for i, s in enumerate(segs, 1)
            if i in JANABIYAH_POSITIONS and is_miin_compatible(s)
        )
        free_miin = sum(1 for s in segs if is_miin_compatible(s))
        if 2 * pos_matches + free_miin > 2 * best_pos + best_free:
            best_pos = pos_matches
            best_free = free_miin
    total = 2 * best_pos + best_free
    return best_pos, best_free, total


def period_overlap(periods_val) -> bool:
    """Return True if any listed period overlaps with the Indus contact window."""
    if not periods_val:
        return False
    # Normalise: accept list or space-separated string
    if isinstance(periods_val, list):
        periods_flat = " ".join(str(p) for p in periods_val)
    else:
        periods_flat = str(periods_val)
    # Check each valid period as a substring match
    for vp in VALID_PERIODS:
        if vp.lower() in periods_flat.lower():
            return True
    return False


def main() -> None:
    print("Phase-32 T8 — Permutation Null Model (Enmenanak / Janabiyah)", flush=True)
    print("=" * 65, flush=True)

    pns = load_pns()
    print(f"Loaded {len(pns)} personal names from ePSD2.", flush=True)

    # Parse each PN into segment lists
    parsed: list[tuple[str, list[list[str]], str]] = []
    for pn in pns:
        headword = pn.get("headword", "?")
        forms_raw = pn.get("forms", "")
        periods = pn.get("periods", "")
        segs = parse_segments(forms_raw)
        if segs:
            parsed.append((headword, segs, periods))

    print(f"Parsed forms for {len(parsed)} PNs.", flush=True)

    # Score all PNs
    scores: list[tuple[str, int, int, float, str]] = []
    for headword, segs, periods in parsed:
        pos, free, total = score_name(segs)
        scores.append((headword, pos, free, total, periods))

    # Sort by total score
    scores.sort(key=lambda x: x[3], reverse=True)

    # Observed top results
    print("\nObserved top 10 matches (all periods):", flush=True)
    for hw, pos, free, total, per in scores[:10]:
        print(f"  {hw:<40s}  pos={pos}  free={free}  score={total:.1f}  [{per[:40]}]",
              flush=True)

    observed_max = scores[0][3] if scores else 0.0

    # Period-filtered results
    period_scores = [(hw, pos, free, total, per) for hw, pos, free, total, per in scores
                     if period_overlap(per)]
    period_scores.sort(key=lambda x: x[3], reverse=True)

    print(f"\nPeriod-filtered (Ur III / Old Akkadian etc.): {len(period_scores)} names", flush=True)
    for hw, pos, free, total, per in period_scores[:5]:
        print(f"  {hw:<40s}  pos={pos}  free={free}  score={total:.1f}  [{per[:40]}]",
              flush=True)

    period_max = period_scores[0][3] if period_scores else 0.0

    # ── Permutation null ────────────────────────────────────────────────────────
    # For each permutation: for each name, randomly shuffle its segments,
    # then re-score. This destroys the positional bias while preserving
    # name length and number of potential miin segments.
    N_PERMUTATIONS = 1000
    rng = random.Random(42)

    print(f"\nRunning {N_PERMUTATIONS} permutations (shuffling segment positions)...", flush=True)

    perm_max_scores = []
    perm_period_max_scores = []

    for _ in range(N_PERMUTATIONS):
        perm_max = 0.0
        perm_per_max = 0.0
        for hw, segs_list, per in parsed:
            # For each rendering: shuffle segment order within the name
            shuffled_segs = []
            for segs in segs_list:
                sh = list(segs)
                rng.shuffle(sh)
                shuffled_segs.append(sh)
            _, _, total = score_name(shuffled_segs)
            if total > perm_max:
                perm_max = total
            if period_overlap(per) and total > perm_per_max:
                perm_per_max = total
        perm_max_scores.append(perm_max)
        perm_period_max_scores.append(perm_per_max)

    # p-values
    p_all = sum(1 for s in perm_max_scores if s >= observed_max) / N_PERMUTATIONS
    p_per = sum(1 for s in perm_period_max_scores if s >= period_max) / N_PERMUTATIONS

    print(f"\nObserved max score (all):    {observed_max:.1f}  →  p={p_all:.4f} ({p_all:.2%})",
          flush=True)
    print(f"Observed max score (period): {period_max:.1f}  →  p={p_per:.4f} ({p_per:.2%})",
          flush=True)

    # Verdict
    if p_all <= 0.05:
        verdict_all = "SIGNIFICANT — max score not explained by random positional alignment"
    elif p_all <= 0.10:
        verdict_all = "MARGINAL — suggestive but not significant at p<0.05"
    else:
        verdict_all = "NOT SIGNIFICANT — max score consistent with random chance"

    if p_per <= 0.05:
        verdict_per = "SIGNIFICANT after period filter"
    elif p_per <= 0.10:
        verdict_per = "MARGINAL after period filter"
    else:
        verdict_per = "NOT SIGNIFICANT after period filter"

    print(f"\nAll-period verdict:    {verdict_all}", flush=True)
    print(f"Period-filtered verdict: {verdict_per}", flush=True)

    # Score distribution summary
    score_dist = Counter(round(s[3]) for s in scores)
    print("\nScore distribution (all names):", flush=True)
    for s in sorted(score_dist, reverse=True)[:8]:
        print(f"  score={s}: {score_dist[s]} names", flush=True)
    print(f"  score=0: {sum(c for s, c in score_dist.items() if s == 0)} names", flush=True)

    # Save report
    report = {
        "phase": "Phase-32 T8",
        "test": "Permutation Null Model — Enmenanak / Janabiyah Inscription",
        "observed": {
            "n_pns_total": len(scores),
            "n_pns_period_filtered": len(period_scores),
            "top_match": scores[0][0] if scores else "?",
            "top_score_all": observed_max,
            "top_score_period_filtered": period_max,
            "top5_all": [
                {"headword": hw, "pos_match": pm, "free_miin": fm, "score": sc,
                 "periods": per[:60]}
                for hw, pm, fm, sc, per in scores[:5]
            ],
            "top5_period": [
                {"headword": hw, "pos_match": pm, "free_miin": fm, "score": sc,
                 "periods": per[:60]}
                for hw, pm, fm, sc, per in period_scores[:5]
            ],
        },
        "permutation_null": {
            "n_permutations": N_PERMUTATIONS,
            "method": "Segment-position shuffle within each name; preserves name length and miin-compatible segment count",
            "p_value_all_periods": round(p_all, 4),
            "p_value_period_filtered": round(p_per, 4),
            "mean_perm_max_all": round(sum(perm_max_scores) / len(perm_max_scores), 3),
            "mean_perm_max_period": round(sum(perm_period_max_scores) / len(perm_period_max_scores), 3),
        },
        "verdict_all_periods": verdict_all,
        "verdict_period_filtered": verdict_per,
        "period_filter": sorted(VALID_PERIODS),
        "janabiyah_positions": sorted(JANABIYAH_POSITIONS),
        "scoring_formula": "score = 2 * n_position_matches + 1 * n_free_miin",
        "miin_criterion": "segment matches pattern: me|mi|min|men|meen|an|na",
        "citations": ["A.11", "A.1"],
        "interpretation": (
            "The permutation test checks whether Enmenanak's top-scoring status "
            "could be explained by random positional alignment alone. "
            "A low p-value (< 0.05) supports the Phase-29d finding; "
            "a high p-value indicates the result is consistent with chance. "
            "Note: the scoring function is a simplified reconstruction of Phase-29d; "
            "results may differ from the original analysis. "
            "Period filter (Ur III / Old Akkadian) isolates the historically plausible window."
        ),
    }

    out_path = REPORTS_DIR / "phase32_t8_permutation_null.json"
    out_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(f"\nSaved report to {out_path}", flush=True)


if __name__ == "__main__":
    main()

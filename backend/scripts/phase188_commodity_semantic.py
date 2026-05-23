"""Phase 188 — Commodity Semantic Layer

Multiple 2021-2026 papers converge on the hypothesis that Indus inscriptions
are commodity/trade/tax labels. This script builds a Tamil DEDR-anchored
trade vocabulary and tests whether expected rebus sequences appear in the
corpus at above-chance frequency.

Steps:
  1. Build a commodity vocabulary from DEDR (metals, gems, crops, livestock,
     crafts, weights, measures) — these are the likely inscription subjects
  2. For each commodity word, compute the expected rebus sequence using
     current HIGH/MEDIUM anchor phoneme assignments
  3. Count occurrences of those sequences in the M77 corpus
  4. Compute lift (observed / expected) for each commodity sequence
  5. Report: which commodity vocabulary is corpus-attested above chance?

This is the semantic-layer complement to our positional/statistical anchors.
"""
from __future__ import annotations
import json, math
from pathlib import Path
from collections import Counter

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
REPORTS   = REPO_ROOT / "research" / "indus" / "phase_reports"
ANCHOR_F  = REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
OUTPUTS.mkdir(exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

# ── Tamil DEDR commodity vocabulary ──────────────────────────────────────────
# Each entry: {word, dedr_id, meaning, category, syllables}
# Syllables = phoneme breakdown (each element = one Indus sign slot)
# Source: DEDR (Burrow & Emeneau 1984), Parpola 1994, Tamil Lexicon
COMMODITY_VOCABULARY = [
    # === Metals & Precious materials ===
    {"word": "pon",    "dedr": "4494", "meaning": "gold",
     "category": "metal", "syllables": ["po", "n"]},
    {"word": "vēnkalam","dedr": "5529","meaning": "copper, bronze",
     "category": "metal", "syllables": ["vēn", "ka", "la"]},
    {"word": "irum-pu","dedr": "503",  "meaning": "iron",
     "category": "metal", "syllables": ["iru", "m", "pu"]},
    {"word": "velli",  "dedr": "5530", "meaning": "silver",
     "category": "metal", "syllables": ["vel", "li"]},
    # === Gemstones ===
    {"word": "maṇi",   "dedr": "4647", "meaning": "gem, bead, jewel",
     "category": "gem", "syllables": ["ma", "ṇi"]},
    {"word": "kaṉ",    "dedr": "1335", "meaning": "gem, eye, gold",
     "category": "gem", "syllables": ["ka", "ṉ"]},
    {"word": "paḷiṅku","dedr": "3963", "meaning": "crystal, quartz",
     "category": "gem", "syllables": ["pa", "ḷiṅ", "ku"]},
    # === Agricultural commodities ===
    {"word": "eḷ",     "dedr": "783",  "meaning": "sesame",
     "category": "crop", "syllables": ["eḷ"]},
    {"word": "parutti","dedr": "3982", "meaning": "cotton",
     "category": "crop", "syllables": ["pa", "ru", "ti"]},
    {"word": "nel",    "dedr": "3713", "meaning": "paddy, rice in husk",
     "category": "crop", "syllables": ["nel"]},
    {"word": "varaku", "dedr": "5267", "meaning": "millet (Paspalum)",
     "category": "crop", "syllables": ["va", "ra", "ku"]},
    # === Livestock ===
    {"word": "māṭu",   "dedr": "4798", "meaning": "cattle, cow",
     "category": "livestock", "syllables": ["mā", "ṭu"]},
    {"word": "āṭu",    "dedr": "329",  "meaning": "goat",
     "category": "livestock", "syllables": ["ā", "ṭu"]},
    {"word": "erumai", "dedr": "796",  "meaning": "buffalo (water buffalo)",
     "category": "livestock", "syllables": ["e", "ru", "mai"]},
    {"word": "min",    "dedr": "4897", "meaning": "fish (rebus: star, shine)",
     "category": "commodity_marker", "syllables": ["min"]},
    # === Craft & trade ===
    {"word": "kol",    "dedr": "2172", "meaning": "iron-working, forge",
     "category": "craft", "syllables": ["kol"]},
    {"word": "kaḷaṅ",  "dedr": "1452", "meaning": "grain measure (dry measure)",
     "category": "measure", "syllables": ["ka", "ḷaṅ"]},
    {"word": "tūkku",  "dedr": "3361", "meaning": "weight, balance",
     "category": "measure", "syllables": ["tū", "kku"]},
    # === Luxury goods ===
    {"word": "toḷ",    "dedr": "3562", "meaning": "hide, leather, skin",
     "category": "luxury", "syllables": ["toḷ"]},
    {"word": "pal",    "dedr": "4003", "meaning": "tooth, ivory",
     "category": "luxury", "syllables": ["pal"]},
    {"word": "kari",   "dedr": "1298", "meaning": "elephant (used for ivory ref)",
     "category": "luxury", "syllables": ["ka", "ri"]},
    # === Administrative / title vocabulary ===
    {"word": "kōṉ",    "dedr": "2220", "meaning": "king, ruler",
     "category": "title", "syllables": ["kōṉ"]},
    {"word": "tiru",   "dedr": "3264", "meaning": "auspicious, holy, wealth",
     "category": "title", "syllables": ["ti", "ru"]},
    {"word": "ūr",     "dedr": "720",  "meaning": "town, settlement",
     "category": "admin", "syllables": ["ūr"]},
    {"word": "il",     "dedr": "491",  "meaning": "house, home",
     "category": "admin", "syllables": ["il"]},
]

# ── Phoneme → sign mapping (from current HIGH/MEDIUM anchors) ─────────────────
# Built at runtime from INDUS_FINAL_ANCHORS.json
# Format: {phoneme_prefix: [sign_id, ...]}


def build_phoneme_to_sign(anchors: dict) -> dict[str, list[str]]:
    """Build reverse map: phoneme_root → [sign_ids]."""
    ph_to_sign: dict[str, list[str]] = {}
    for sign_id, rec in anchors.items():
        if not isinstance(rec, dict):
            continue
        conf = rec.get("confidence", "")
        if conf not in ("HIGH", "MEDIUM"):
            continue
        reading = rec.get("reading", "")
        # Split multi-reading (e.g. "ay/ā" → ["ay", "ā"])
        for r in reading.split("/"):
            r = r.strip().lower().split("(")[0].strip()
            if r and len(r) >= 1:
                ph_to_sign.setdefault(r, []).append(sign_id)
                # Also index by first 2 chars for fuzzy match
                if len(r) >= 2:
                    ph_to_sign.setdefault(r[:2], []).append(sign_id)
    return ph_to_sign


def syllable_to_signs(syllable: str, ph_map: dict[str, list[str]]) -> list[str]:
    """Find which signs could represent a given syllable."""
    s = syllable.lower().strip()
    candidates = []
    # Exact match
    candidates.extend(ph_map.get(s, []))
    # Prefix match (2 chars)
    if len(s) >= 2:
        candidates.extend(ph_map.get(s[:2], []))
    # Remove duplicates, keep order
    seen = set()
    out = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out[:3]  # top 3 candidates per syllable


def count_sequence(inscs: list, sign_seq: list[str]) -> int:
    """Count exact n-gram occurrences of sign_seq in inscriptions."""
    n = len(sign_seq)
    if n == 0:
        return 0
    count = 0
    for insc in inscs:
        for i in range(len(insc) - n + 1):
            if insc[i:i+n] == sign_seq:
                count += 1
    return count


def expected_count(sign_seq: list[str], freq: Counter, total_tokens: int) -> float:
    """Expected count under independence assumption."""
    n = len(sign_seq)
    if n == 0 or total_tokens == 0:
        return 0.0
    prob = 1.0
    for s in sign_seq:
        prob *= freq.get(s, 0) / total_tokens
    # Expected in total_tokens - n positions
    return prob * max(1, total_tokens - n)


def main():
    import sys, time
    t0 = time.time()
    print("=" * 60)
    print("Phase 188 — Commodity Semantic Layer")
    print("=" * 60)

    sys.path.insert(0, str(REPO_ROOT / "backend"))
    from glossa_lab.data.indus_m77 import get_corpus_inscriptions, get_corpus_symbols

    inscs = get_corpus_inscriptions()
    syms  = get_corpus_symbols()
    freq  = Counter(syms)
    total_tokens = len(syms)
    anchors = json.loads(ANCHOR_F.read_text())["anchors"]
    ph_map  = build_phoneme_to_sign(anchors)

    print(f"\nLoaded {len(anchors)} anchors, {len(freq)} distinct signs, "
          f"{len(inscs)} inscriptions, {total_tokens} tokens")
    print(f"Phoneme-to-sign mappings: {len(ph_map)} entries")

    # Test each commodity word
    print("\n=== Commodity Rebus Sequence Analysis ===")
    commodity_results = []
    for entry in COMMODITY_VOCABULARY:
        word      = entry["word"]
        syllables = entry["syllables"]
        category  = entry["category"]
        meaning   = entry["meaning"]

        # Build candidate sign sequences from syllables
        sign_options = [syllable_to_signs(syl, ph_map) for syl in syllables]
        # Use top-1 sign per syllable if available
        top_seq = [opts[0] if opts else None for opts in sign_options]

        if None in top_seq:
            # Some syllables have no sign mapping — record as unmapped
            commodity_results.append({
                "word": word, "dedr": entry["dedr"], "meaning": meaning,
                "category": category, "syllables": syllables,
                "sign_sequence": top_seq,
                "corpus_count": 0, "expected": 0.0, "lift": 0.0,
                "status": "UNMAPPED_SYLLABLE",
                "all_sign_options": sign_options,
            })
            continue

        # Count this sequence in corpus
        observed = count_sequence(inscs, top_seq)
        expected = expected_count(top_seq, freq, total_tokens)
        lift = round(observed / expected, 2) if expected > 0.001 else 0.0

        status = (
            "STRONG_MATCH" if lift > 3.0 and observed >= 3 else
            "MODERATE_MATCH" if lift > 1.5 and observed >= 2 else
            "PRESENT" if observed > 0 else
            "ABSENT"
        )

        commodity_results.append({
            "word": word, "dedr": entry["dedr"], "meaning": meaning,
            "category": category, "syllables": syllables,
            "sign_sequence": top_seq,
            "corpus_count": observed,
            "expected": round(expected, 4),
            "lift": lift,
            "status": status,
            "all_sign_options": sign_options,
        })

        marker = "✓✓" if status == "STRONG_MATCH" else ("✓" if "MATCH" in status else ("·" if observed else "✗"))
        print(f"  {marker} {word:12s} ({category:12s}): seq={top_seq} "
              f"n={observed} lift={lift:.2f} [{status}]")

    # Summary
    strong_matches   = [r for r in commodity_results if r["status"] == "STRONG_MATCH"]
    moderate_matches = [r for r in commodity_results if r["status"] == "MODERATE_MATCH"]
    absent           = [r for r in commodity_results if r["status"] == "ABSENT"]
    unmapped         = [r for r in commodity_results if r["status"] == "UNMAPPED_SYLLABLE"]

    print(f"\n{'='*60}")
    print(f"STRONG matches (lift>3, n≥3):    {len(strong_matches)}")
    print(f"MODERATE matches (lift>1.5, n≥2): {len(moderate_matches)}")
    print(f"Absent from corpus:               {len(absent)}")
    print(f"Unmapped syllables:               {len(unmapped)}")
    print(f"\nTop semantic categories present:")
    cat_counts = Counter(r["category"] for r in commodity_results
                         if r["status"] in ("STRONG_MATCH", "MODERATE_MATCH", "PRESENT"))
    for cat, n in cat_counts.most_common():
        print(f"  {cat}: {n}")

    elapsed = round(time.time() - t0, 1)
    result = {
        "phase": 188,
        "elapsed_s": elapsed,
        "n_vocabulary_items": len(COMMODITY_VOCABULARY),
        "strong_matches": len(strong_matches),
        "moderate_matches": len(moderate_matches),
        "absent": len(absent),
        "unmapped_syllables": len(unmapped),
        "commodity_results": commodity_results,
        "strong_detail": strong_matches,
        "moderate_detail": moderate_matches,
        "verdict": (
            f"COMMODITY VOCABULARY CORPUS-ATTESTED: "
            f"{len(strong_matches)} STRONG + {len(moderate_matches)} MODERATE matches"
            if (len(strong_matches) + len(moderate_matches)) > 3
            else "LIMITED COMMODITY ATTESTATION — M77 corpus too small; ICIT needed"
        ),
    }

    print(f"\nPhase 188 complete in {elapsed}s")
    print(f"Verdict: {result['verdict']}")

    out = OUTPUTS / "phase188_commodity_semantic.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase188_commodity_semantic.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()

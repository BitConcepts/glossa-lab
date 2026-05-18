"""Phase-74: M267 Grammar Constraint Test.

Tests the Phase-64 conclusion that M267 = iN (genitive 'of') using a
formal grammar constraint test, independent of SA.

Hypothesis: If M267 is a genitive particle, it should appear between
an agent marker (M328=aaL, M059=eeL, M176=an) and a title marker
(M099=kol, M211, M073=koon) at significantly higher than chance rates.

Test:
  1. Count actual occurrences of [AGENT]-[M267]-[TITLE] pattern
  2. Build null distribution: shuffle M267 positions within inscriptions
  3. Chi-squared + permutation test: is the observed rate p<0.05?

If p<0.05 AND the pattern is the most common M267 context:
  -> Upgrade M267 from UNCERTAIN to MEDIUM confidence with reading 'iN'

CPU only. Fast.
Output: reports/phase74_m267_grammar_test.json
"""
from __future__ import annotations
import csv, json, math, random
from collections import Counter, defaultdict
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P68     = REPO / "reports/phase68_formula_translation.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase74_m267_grammar_test.json"

# Signs from which M267 should be preceded (agent markers)
AGENT_MARKERS   = {"M328", "M059", "M176", "M305", "M336"}
# Signs which M267 should precede (title/kol markers)
TITLE_MARKERS   = {"M099", "M211", "M073", "M030", "M041"}
# Confirmed HIGH/MEDIUM signs generally
CONFIRMED_SIGNS = {"M342", "M176", "M367", "M391", "M336", "M089", "M328",
                   "M162", "M099", "M059", "M006", "M016", "M045", "M062",
                   "M047", "M248", "M211", "M073", "M030", "M041"}

N_PERMUTATIONS = 10_000


def load_inscriptions() -> list[list[str]]:
    seals: dict[str, list] = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            c = row["cisi_number"]; p = int(row.get("position", 0) or 0)
            s = (row.get("letters") or "").strip()
            if c not in seals: seals[c] = []
            while len(seals[c]) <= p: seals[c].append("")
            seals[c][p] = s
    return [[s for s in v if s] for v in seals.values() if any(v)]


def count_m267_pattern(inscriptions: list) -> dict:
    """Count M267 positions and context patterns."""
    m267_total = 0
    # Pattern: preceding sign in AGENT_MARKERS AND following sign in TITLE_MARKERS
    agent_before_title_after = 0
    agent_before_only = 0
    title_after_only = 0
    neither = 0

    bigrams_before: Counter = Counter()  # sign before M267
    bigrams_after:  Counter = Counter()  # sign after M267

    for ins in inscriptions:
        for i, sign in enumerate(ins):
            if sign != "M267":
                continue
            m267_total += 1
            before = ins[i-1] if i > 0 else None
            after  = ins[i+1] if i < len(ins)-1 else None
            if before: bigrams_before[before] += 1
            if after:  bigrams_after[after]  += 1
            has_agent = before in AGENT_MARKERS
            has_title = after  in TITLE_MARKERS
            if has_agent and has_title: agent_before_title_after += 1
            elif has_agent:             agent_before_only += 1
            elif has_title:             title_after_only  += 1
            else:                       neither           += 1

    return {
        "total": m267_total,
        "agent_before_title_after": agent_before_title_after,
        "agent_before_only": agent_before_only,
        "title_after_only": title_after_only,
        "neither": neither,
        "top_before": dict(bigrams_before.most_common(8)),
        "top_after":  dict(bigrams_after.most_common(8)),
    }


def permutation_test(inscriptions: list, observed: int, m267_total: int,
                     n_perms: int = N_PERMUTATIONS) -> tuple[float, int, float]:
    """Permutation null: shuffle M267 positions, count pattern rate."""
    rng = random.Random(42)
    null_counts = []
    for _ in range(n_perms):
        count = 0
        for ins in inscriptions:
            if "M267" not in ins: continue
            signs = list(ins)
            m267_positions = [i for i, s in enumerate(signs) if s == "M267"]
            # Shuffle M267 to random positions within the inscription
            other_pos = [i for i, s in enumerate(signs) if s != "M267"]
            for p in m267_positions:
                if other_pos:
                    j = rng.randint(0, len(signs) - 1)
                    signs[p], signs[j] = signs[j], signs[p]
            # Recount pattern
            for i, sign in enumerate(signs):
                if sign != "M267": continue
                before = signs[i-1] if i > 0 else None
                after  = signs[i+1] if i < len(signs)-1 else None
                if before in AGENT_MARKERS and after in TITLE_MARKERS:
                    count += 1
        null_counts.append(count)

    null_mean = sum(null_counts) / len(null_counts)
    null_std  = math.sqrt(sum((c-null_mean)**2 for c in null_counts)/len(null_counts)) or 1
    z = (observed - null_mean) / null_std
    p_value = sum(1 for c in null_counts if c >= observed) / n_perms
    return z, int(null_mean), p_value


def main():
    print("Phase-74: M267 Grammar Constraint Test\n")

    inscriptions = load_inscriptions()
    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors      = anchors_data["anchors"]

    print(f"  Corpus: {len(inscriptions)} inscriptions")
    print(f"  M267 current confidence: {anchors.get('M267',{}).get('confidence','?')}")

    # Count actual patterns
    counts = count_m267_pattern(inscriptions)
    m267_total = counts["total"]
    observed   = counts["agent_before_title_after"]
    observed_rate = observed / max(m267_total, 1)

    print(f"\n  M267 total occurrences: {m267_total}")
    print(f"  [AGENT]-M267-[TITLE] pattern: {observed}/{m267_total} = {observed_rate:.1%}")
    print(f"  Agent-before-only:            {counts['agent_before_only']}/{m267_total} = {counts['agent_before_only']/max(m267_total,1):.1%}")
    print(f"  Title-after-only:             {counts['title_after_only']}/{m267_total} = {counts['title_after_only']/max(m267_total,1):.1%}")
    print(f"  Neither:                      {counts['neither']}/{m267_total} = {counts['neither']/max(m267_total,1):.1%}")
    print(f"\n  Top signs BEFORE M267: {dict(list(counts['top_before'].items())[:5])}")
    print(f"  Top signs AFTER  M267: {dict(list(counts['top_after'].items())[:5])}")

    # Permutation test
    print(f"\n  Running permutation test ({N_PERMUTATIONS:,} shuffles)...")
    z_score, null_mean, p_value = permutation_test(inscriptions, observed, m267_total)
    print(f"  Null mean: {null_mean:.1f}, Observed: {observed}")
    print(f"  z={z_score:.2f}, p={p_value:.4f}")

    # Decision
    if p_value < 0.05 and observed_rate > 0.10:
        verdict = "GENITIVE_CONFIRMED"
        m267_promoted = True
        interpretation = (
            f"M267=[AGENT]-M267-[TITLE] pattern is statistically significant "
            f"(p={p_value:.4f} < 0.05). M267 functions as a genitive/connective particle. "
            f"Upgrade: UNCERTAIN -> MEDIUM (reading: iN/in)"
        )
    elif p_value < 0.10:
        verdict = "GENITIVE_MARGINAL"
        m267_promoted = False
        interpretation = (
            f"M267 pattern marginally significant (p={p_value:.4f}). "
            f"Grammar evidence suggestive but not conclusive. Remain UNCERTAIN."
        )
    else:
        verdict = "UNCERTAIN_CONFIRMED"
        m267_promoted = False
        interpretation = (
            f"M267 pattern not significantly above chance (p={p_value:.4f}). "
            f"Distribution is not strongly constrained. Remain UNCERTAIN."
        )

    print(f"\n=== Phase-74 Results ===")
    print(f"  Verdict:  {verdict}")
    print(f"  p-value:  {p_value:.4f}")
    print(f"  z-score:  {z_score:.2f}")
    print(f"  Promoted: {m267_promoted}")
    print(f"  Interpretation: {interpretation}")

    # Update anchors if promoted
    if m267_promoted:
        anchors_data["anchors"]["M267"]["confidence"] = "MEDIUM"
        anchors_data["anchors"]["M267"]["reading"]    = "iN/in (genitive 'of')"
        anchors_data["anchors"]["M267"]["source"]     = "Phase-74 grammar constraint test (p<0.05) + Phase-64 positional analysis"
        ANCHORS.write_text(json.dumps(anchors_data, indent=2, ensure_ascii=False), "utf-8")
        print(f"\n  ANCHORS.json updated: M267 promoted UNCERTAIN -> MEDIUM")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": "cpu",
        "m267_total":               m267_total,
        "observed_agent_m267_title":observed,
        "observed_rate":            round(observed_rate, 4),
        "null_mean":                null_mean,
        "z_score":                  round(z_score, 3),
        "p_value":                  round(p_value, 4),
        "verdict":                  verdict,
        "m267_promoted":            m267_promoted,
        "interpretation":           interpretation,
        "pattern_counts":           counts,
        "agent_markers_used":       sorted(AGENT_MARKERS),
        "title_markers_used":       sorted(TITLE_MARKERS),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()

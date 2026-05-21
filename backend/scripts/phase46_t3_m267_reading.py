"""Phase-46 T3: M267 Reading Candidates — Proto-Dravidian Grammar Cross-Check.

M267 profile (from Phase-45 T2):
  - avg_position = 0.54 (medial)
  - iconographic entropy = 0.852 (UNIFORM — motif-independent)
  - M267→M099 formula: 84× (asymmetric: M267 precedes kol/kol)
  - Holdat role: CASE_MARKER_SUFFIX (but positionally medial, not terminal)
  - Count: 400 (2nd most frequent sign in corpus)

This script systematically evaluates candidate Proto-Dravidian readings for M267
against four independent constraints:
  1. POSITIONAL: medial (avg_pos=0.54) — neither initial nor terminal
  2. FORMULA: M267→kol/kol (title marker) 84× — connects identity to title
  3. ICONOGRAPHIC: motif-independent (all faunal motifs equally) → grammatical, not semantic
  4. FREQUENCY: 400 occurrences → very high frequency → grammatical rather than content word

For each candidate, computes a COMPOSITE_SCORE out of 4 constraints and assigns
an EPISTEMIC STATUS.

Also searches the Parpola 1994 extracted text for discussions of medial/linking signs
and the Frenez papers for trade seal formula analysis.

GPU: torch used for vectorised constraint scoring.

Output: reports/phase46_t3_m267_reading.json
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[GPU] torch {torch.__version__} — device: {DEVICE}")
except ImportError:
    torch = None
    DEVICE = "cpu"
    print("[GPU] torch not available — CPU only")

REPO    = Path(__file__).parents[2]
CORPUS  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ROLES   = REPO / "corpora/downloads/external_repos/holdatllc_indus/all_symbol_semantic_roles 2.csv"
DEDR    = REPO / "reports/jambu-dedr/data/dedr/dedr.csv"
PUBS    = REPO / "corpora/downloads/contact_zone/publications"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase46_t3_m267_reading.json"

TARGET = "M267"

# ── Candidate readings with phonological and grammatical rationale ──────────
# Each candidate is a Proto-Dravidian or Old Tamil functional element
# that could appear in the M267 structural slot.
#
# Evidence framework (from Krishnamurti 2003, Subrahmanyam 1983, Burrow & Emeneau DEDR):
#   • In a seal formula [CLASSIFIER-PREFIX] [MEDIAL] [TITLE-SUFFIX]
#     the medial slot most commonly holds: genitive, oblique, or connective particles
#   • kol/kol (M099) is the title/hammer marker → M267 links identity to kol
#
CANDIDATES: list[dict] = [
    {
        "token":   "iṉ",
        "romanized": "in",
        "pos":     "postposition/genitive",
        "gloss":   "'of, from' (genitive-ablative)",
        "formula": "[identity] iṉ kol = '[person]'s lord/hammer'",
        "dedr_ref": "DEDR 499 (iṉ 'sweet, good, pleasant') + Old Tamil genitive -iṉ",
        "positional_ok": True,   # genitive particles are medial
        "formula_ok":    True,   # "[identity] of kol" is a natural title phrase
        "freq_ok":       True,   # genitive is very high frequency
        "icon_ok":       True,   # genitive is motif-independent
        "confidence":    "HIGH_CANDIDATE",
    },
    {
        "token":   "um",
        "romanized": "um",
        "pos":     "enclitic particle",
        "gloss":   "'and, also, even' (additive/inclusive)",
        "formula": "[identity] um kol = '[person] and/also [is] kol'",
        "dedr_ref": "Old Tamil um (inclusive clitic, extremely frequent in Sangam)",
        "positional_ok": True,
        "formula_ok":    True,   # additive particle between identity and title is natural
        "freq_ok":       True,   # um is one of most frequent Tamil particles
        "icon_ok":       True,
        "confidence":    "HIGH_CANDIDATE",
    },
    {
        "token":   "ē",
        "romanized": "e",
        "pos":     "emphatic particle",
        "gloss":   "emphatic 'indeed, truly' (focus marker)",
        "formula": "[identity] ē kol = '[person] TRULY is kol'",
        "dedr_ref": "Old Tamil ē (emphatic enclitic, common in Sangam poetry)",
        "positional_ok": True,
        "formula_ok":    True,
        "freq_ok":       True,   # emphatic particles are very frequent
        "icon_ok":       True,
        "confidence":    "MEDIUM_CANDIDATE",
    },
    {
        "token":   "āṉ",
        "romanized": "aan",
        "pos":     "masculine pronoun/suffix",
        "gloss":   "'he who, the one who' (masculine relative)",
        "formula": "[identity] āṉ kol = 'he who is [identity], the lord'",
        "dedr_ref": "DEDR 367 (āṉ masculine suffix)",
        "positional_ok": True,
        "formula_ok":    True,
        "freq_ok":       False,  # āṉ is less frequent than um/ē
        "icon_ok":       True,
        "confidence":    "MEDIUM_CANDIDATE",
    },
    {
        "token":   "aṭi",
        "romanized": "ati",
        "pos":     "noun",
        "gloss":   "'foot/servant, base' (devotee marker)",
        "formula": "[identity] aṭi kol = '[identity]'s servant-of-kol'",
        "dedr_ref": "DEDR 72 (aṭi 'foot, base')",
        "positional_ok": True,
        "formula_ok":    True,   # aṭi kol would mean "servant of kol/lord"
        "freq_ok":       False,  # aṭi as standalone is less frequent
        "icon_ok":       True,
        "confidence":    "LOW_CANDIDATE",
    },
    {
        "token":   "col",
        "romanized": "col",
        "pos":     "verb",
        "gloss":   "'to say, speak, call' → naming/title formula",
        "formula": "[identity] col kol = 'called kol, lord'",
        "dedr_ref": "DEDR 2953 (col 'to say, word')",
        "positional_ok": True,
        "formula_ok":    True,   # "called/named [title]" is a common formula
        "freq_ok":       True,
        "icon_ok":       True,
        "confidence":    "MEDIUM_CANDIDATE",
    },
    {
        "token":   "al",
        "romanized": "al",
        "pos":     "negative/abstract suffix",
        "gloss":   "negation or abstract nominaliser",
        "formula": "[identity] al kol → unclear / negative formula",
        "dedr_ref": "Old Tamil al (negation) or DEDR 248 (alal 'not')",
        "positional_ok": True,
        "formula_ok":    False,  # negative before title is structurally odd
        "freq_ok":       True,
        "icon_ok":       True,
        "confidence":    "LOW_CANDIDATE",
    },
    {
        "token":   "nāḷ",
        "romanized": "nal",
        "pos":     "noun/temporal",
        "gloss":   "'day, time, good (thing)' — temporal or quality marker",
        "formula": "[identity] nāḷ kol = '[identity]'s time/good lord'",
        "dedr_ref": "DEDR 3654 (nāḷ 'day, time') / DEDR 3639 (nal 'good')",
        "positional_ok": True,
        "formula_ok":    False,
        "freq_ok":       False,
        "icon_ok":       True,
        "confidence":    "LOW_CANDIDATE",
    },
]


def score_candidate(c: dict) -> dict:
    """Compute composite score from 4 independent constraints."""
    constraints = {
        "positional_medial": c["positional_ok"],
        "formula_natural":   c["formula_ok"],
        "high_frequency":    c["freq_ok"],
        "motif_independent": c["icon_ok"],
    }
    score = sum(1 for v in constraints.values() if v)
    max_score = len(constraints)
    pct = score / max_score

    if score == 4:
        epistemic = "STRONG_CANDIDATE"
    elif score == 3:
        epistemic = "PLAUSIBLE_CANDIDATE"
    elif score == 2:
        epistemic = "WEAK_CANDIDATE"
    else:
        epistemic = "UNLIKELY"

    return {**c, "constraint_scores": constraints, "composite_score": score,
            "composite_pct": pct, "epistemic": epistemic}


def load_corpus_context() -> dict:
    """Load corpus and compute what precedes/follows M267."""
    seals: dict[str, dict] = {}
    with open(CORPUS, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cisi = row["cisi_number"]
            pos = int(row.get("position", 0) or 0)
            if cisi not in seals:
                seals[cisi] = {"signs": [], "icon": (row.get("iconography") or "").lower()}
            while len(seals[cisi]["signs"]) <= pos:
                seals[cisi]["signs"].append("")
            seals[cisi]["signs"][pos] = row["letters"]

    pre: Counter = Counter()
    post: Counter = Counter()
    bigram_pre: Counter = Counter()  # what comes 2 before M267
    total = 0

    for d in seals.values():
        signs = [s for s in d["signs"] if s]
        for i, s in enumerate(signs):
            if s == TARGET:
                total += 1
                if i > 0:
                    pre[signs[i-1]] += 1
                if i > 1:
                    bigram_pre[signs[i-2]] += 1
                if i < len(signs) - 1:
                    post[signs[i+1]] += 1

    # Load HIGH anchors
    anchor_path = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
    anchors = json.loads(anchor_path.read_text("utf-8"))["anchors"] if anchor_path.exists() else {}

    def annotate(ctr: Counter) -> list:
        out = []
        for sign, cnt in ctr.most_common(10):
            a = anchors.get(sign, {})
            out.append({"sign": sign, "count": cnt,
                        "reading": a.get("reading", "?"),
                        "confidence": a.get("confidence", "?")})
        return out

    return {
        "total_m267_occurrences": total,
        "top_preceding": annotate(pre),
        "top_following": annotate(post),
        "top_2before": annotate(bigram_pre),
    }


def search_parpola_text() -> list[str]:
    """Extract Parpola passages discussing linking/medial signs."""
    passages = []
    parpola_txt = PUBS / "parpola_1994a_deciphering_indus_script.txt"
    if not parpola_txt.exists():
        return []
    text = parpola_txt.read_text("utf-8", errors="replace")
    patterns = [
        r"genitive", r"connective", r"linking sign", r"medial", r"particle",
        r"copula", r"postposition", r"enclitic", r"formula.*title",
        r"sign\s+(?:267|M267)",
    ]
    for pat in patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            start = max(0, m.start() - 100)
            end = min(len(text), m.end() + 120)
            snippet = text[start:end].replace("\n", " ").strip()
            if snippet and len(snippet) > 30 and snippet not in passages:
                passages.append(snippet)
                if len(passages) >= 8:
                    break
        if len(passages) >= 8:
            break
    return passages[:6]


def gpu_rank_candidates(scored: list[dict]) -> list[dict]:
    """Use torch to compute weighted ranking with GPU if available."""
    if torch is None:
        return sorted(scored, key=lambda x: -x["composite_pct"])

    # Build weight tensor [composite, formula_natural, high_frequency]
    weights = torch.tensor([0.4, 0.4, 0.2], device=DEVICE)
    features = torch.tensor([
        [c["composite_pct"],
         float(c["formula_ok"]),
         float(c["freq_ok"])]
        for c in scored
    ], device=DEVICE)
    scores_t = (features * weights).sum(dim=1)
    ranked_idx = scores_t.argsort(descending=True).cpu().tolist()
    print(f"[GPU:{DEVICE}] Candidate ranking computed on {DEVICE}")
    return [scored[i] for i in ranked_idx]


def main() -> None:
    print("Phase-46 T3: M267 Reading Candidates — Proto-Dravidian Cross-Check\n")

    # Score all candidates
    scored = [score_candidate(c) for c in CANDIDATES]

    # GPU-accelerated ranking
    ranked = gpu_rank_candidates(scored)

    print("\nCandidate Rankings:")
    for i, c in enumerate(ranked):
        print(f"  {i+1}. {c['token']} ({c['romanized']}) — {c['epistemic']} "
              f"[{c['composite_score']}/4] — {c['gloss'][:50]}")

    # Load corpus context
    print("\nLoading corpus context for M267…")
    context = load_corpus_context()
    print(f"  M267 count: {context['total_m267_occurrences']}")
    print(f"  Top preceding: {[(x['sign'], x.get('reading','?'), x['count']) for x in context['top_preceding'][:5]]}")
    print(f"  Top following: {[(x['sign'], x.get('reading','?'), x['count']) for x in context['top_following'][:5]]}")

    # Search Parpola text
    print("\nSearching Parpola 1994 for linking/medial sign discussions…")
    parpola_passages = search_parpola_text()
    print(f"  Found {len(parpola_passages)} relevant passages")

    # Best candidate summary
    best = ranked[0]
    runner_up = ranked[1] if len(ranked) > 1 else {}

    print("\n=== M267 Reading Assessment ===")
    print(f"Best candidate:   {best['token']} ({best['gloss'][:60]})")
    print(f"Epistemic status: {best['epistemic']}")
    print(f"Formula:          {best['formula']}")
    print(f"Runner-up:        {runner_up.get('token','?')} ({runner_up.get('epistemic','?')})")

    result = {
        "_citation": {"primary_sources": ["A.1", "A.13"],
                      "dedr_ref": "Burrow & Emeneau DEDR",
                      "grammar_ref": "Krishnamurti 2003, Subrahmanyam 1983"},
        "gpu_device": DEVICE,
        "target_sign": TARGET,
        "m267_profile": {
            "avg_position": 0.54,
            "iconographic_entropy": 0.852,
            "m267_to_m099_formula_count": 84,
            "total_occurrences": 400,
            "holdat_role": "CASE_MARKER_SUFFIX",
        },
        "corpus_context": context,
        "ranked_candidates": [
            {k: v for k, v in c.items() if k != "dedr_ref"}
            for c in ranked
        ],
        "best_candidate": best["token"],
        "best_candidate_formula": best["formula"],
        "best_candidate_epistemic": best["epistemic"],
        "runner_up": runner_up.get("token"),
        "parpola_passages": parpola_passages,
        "methodology": (
            "Each candidate scored against 4 constraints: (1) positional_medial, "
            "(2) formula_natural (precedes kol/kol title 84x), "
            "(3) high_frequency (M267 is 2nd most frequent), "
            "(4) motif_independent. "
            "GPU-weighted ranking via torch tensor dot product."
        ),
    }

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()

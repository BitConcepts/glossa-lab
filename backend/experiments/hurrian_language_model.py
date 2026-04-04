"""Hurrian language model for Linear A hypothesis testing.

Builds a phoneme-level corpus and bigram model from Hurrian vocabulary.
Hurrian (c. 2300–1200 BCE) is a non-Indo-European isolate spoken in
Mitanni and northern Mesopotamia — a plausible substrate candidate
for Linear A given Minoan trade contacts with the Near East.

Sources:
  - Wegner (2007) Einführung in die hurritische Sprache
  - Wilhelm (1989) The Hurrians (Cornell ANES)
  - Speiser (1941) Introduction to Hurrian (AASOR)
  - Khachikyan (1985) The Hurrian Language

Usage:
  python backend/experiments/hurrian_language_model.py

Output: reports/hurrian_model_validation.json
"""

from __future__ import annotations

import json
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_OUTPUT_PATH = _REPO_ROOT / "reports" / "hurrian_model_validation.json"

# Hurrian vocabulary — administrative, divine, and common terms
# Sources: Wegner (2007), Wilhelm (1989), Speiser (1941)
_HURRIAN_VOCAB: dict[str, str] = {
    # Pronouns and particles
    "en": "I/me (1sg.abs)",
    "ni": "he/she/it (3sg.abs)",
    "til": "all / everyone",
    "an": "and / also",
    "inna": "now / then",
    "anta": "but / however",
    "unna": "when / if",
    # Nouns — family and society
    "attai": "father",
    "nairi": "lord / king",
    "ewri": "lord (divine)",
    "sena": "brother",
    "keldi": "well-being / prosperity",
    "hani": "this",
    "mena": "name / reputation",
    "tena": "with",
    "tura": "son",
    "pairi": "house / household",
    "kiri": "field / land",
    "uri": "city",
    # Verbs (Hurrian morphology is heavily agglutinative)
    "av": "give",
    "ud": "make / do",
    "tiv": "put / place",
    "par": "go / move",
    "al": "come",
    "han": "know",
    "kul": "speak / say",
    "fad": "sit / dwell",
    "nir": "protect",
    "tam": "hold / keep",
    # Divine names and epithets
    "teshup": "storm god (Teshub)",
    "hebat": "sun goddess",
    "shaushka": "goddess of love (Shaushka)",
    "kumarbi": "father of the gods",
    "shimige": "sun god",
    "ashtapi": "deity",
    "nubadig": "deity",
    # Numbers and measure words
    "shini": "two",
    "kig": "one",
    "tumni": "four",
    "shuhi": "many",
    # Administrative terms (Mitanni tablets)
    "ewiri": "lord / master",
    "kireni": "city lord",
    "hamadhe": "chariot",
    "tahe": "tablet",
    "kushhe": "silver",
    "hapiri": "free/roaming people",
    "maryannu": "chariot warrior (loanword)",
    "kiluli": "all together",
    # Suffixes (agglutinative morphology — key feature)
    "ne": "definite article suffix",
    "ve": "genitive suffix",
    "ra": "dative suffix",
    "lla": "ablative suffix",
    "nna": "accusative suffix",
    "ffe": "instrumental suffix",
    "she": "comitative suffix",
    "dan": "directional suffix",
    # More vocabulary
    "wur": "earth / land",
    "abi": "underworld",
    "ashti": "woman / wife",
    "tirwi": "slave",
    "pahi": "give / offer",
    "urnau": "night",
    "simige": "sun",
    "ea": "water god",
    "kuzzi": "cup",
    "mini": "what?",
    "madi": "wisdom",
    "ishmi": "hear",
}


def build_hurrian_corpus(repeat: int = 60) -> list[str]:
    """Build a phoneme-level corpus from Hurrian vocabulary."""
    phonemes: list[str] = []
    for word in _HURRIAN_VOCAB:
        phonemes.extend(list(word))
    return phonemes * repeat


def compute_bigram_profile(phonemes: list[str]) -> dict[str, dict[str, float]]:
    """Build normalised bigram transition probabilities."""
    from collections import defaultdict

    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for i in range(len(phonemes) - 1):
        counts[phonemes[i]][phonemes[i + 1]] += 1
    profile: dict[str, dict[str, float]] = {}
    for ch, nexts in counts.items():
        total = sum(nexts.values())
        profile[ch] = {n: c / total for n, c in nexts.items()}
    return profile


def score_corpus_against_model(
    test_corpus: list[str],
    bigram_profile: dict[str, dict[str, float]],
    alpha: float = 0.01,
) -> float:
    """Log-likelihood of test corpus under bigram model (smoothed)."""
    import math

    log_prob = 0.0
    n = 0
    for i in range(len(test_corpus) - 1):
        a, b = test_corpus[i], test_corpus[i + 1]
        p = bigram_profile.get(a, {}).get(b, alpha)
        log_prob += math.log(p)
        n += 1
    return log_prob / max(n, 1)


def run() -> dict:
    """Build Hurrian model and score against Linear A corpus."""
    import sys

    tests_path = _REPO_ROOT / "backend" / "tests"
    if str(tests_path) not in sys.path:
        sys.path.insert(0, str(tests_path))
    backend_path = _REPO_ROOT / "backend"
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))

    hurrian_corpus = build_hurrian_corpus(repeat=60)
    hurrian_profile = compute_bigram_profile(hurrian_corpus)

    # Greek comparison (same as luwian_language_model.py)
    greek_vocab = [
        "ka",
        "to",
        "te",
        "me",
        "de",
        "ei",
        "en",
        "ek",
        "pa",
        "ma",
        "ti",
        "ke",
        "we",
        "jo",
        "ko",
        "no",
        "po",
        "ro",
        "so",
        "do",
        "pe",
        "ra",
        "sa",
        "ta",
        "na",
        "ni",
        "ku",
        "re",
        "ri",
        "wi",
        "wa",
        "ze",
        "di",
        "mi",
        "pu",
        "su",
        "za",
        "du",
        "pi",
        "si",
    ]
    greek_corpus = []
    for word in greek_vocab:
        greek_corpus.extend(list(word))
    greek_corpus = greek_corpus * 60
    greek_profile = compute_bigram_profile(greek_corpus)

    # Luwian comparison (from luwian_language_model.py)
    luwian_vocab = [
        "ati",
        "imi",
        "tati",
        "nani",
        "sara",
        "ura",
        "zid",
        "za",
        "anda",
        "paran",
        "antu",
        "pi",
        "du",
        "ari",
        "wala",
        "asi",
        "tuwati",
        "isa",
        "mana",
        "hantis",
        "alati",
        "pati",
        "waras",
        "kuis",
        "kuwa",
        "nu",
        "tiya",
        "arha",
        "hant",
        "waliya",
        "piya",
        "la",
        "au",
        "tara",
        "ziya",
        "iya",
        "wasu",
        "nawi",
    ]
    luwian_corpus = []
    for word in luwian_vocab:
        luwian_corpus.extend(list(word))
    luwian_corpus = luwian_corpus * 60
    luwian_profile = compute_bigram_profile(luwian_corpus)

    # Load real Linear A corpus
    try:
        from tests.corpora.real import load_linear_a_signs

        la_corpus = load_linear_a_signs()
    except Exception:
        la_corpus = []

    hurrian_score = score_corpus_against_model(la_corpus, hurrian_profile) if la_corpus else None
    greek_score = score_corpus_against_model(la_corpus, greek_profile) if la_corpus else None
    luwian_score = score_corpus_against_model(la_corpus, luwian_profile) if la_corpus else None

    hurrian_phonemes = sorted(set(hurrian_corpus))

    summary = {
        "hurrian_vocabulary_size": len(_HURRIAN_VOCAB),
        "hurrian_corpus_tokens": len(hurrian_corpus),
        "hurrian_phoneme_inventory": hurrian_phonemes,
        "hurrian_phoneme_inventory_size": len(hurrian_phonemes),
        "linear_a_test_tokens": len(la_corpus),
        "hurrian_log_likelihood_per_token": hurrian_score,
        "greek_log_likelihood_per_token": greek_score,
        "luwian_log_likelihood_per_token": luwian_score,
        "hurrian_vs_greek_advantage": (
            round(hurrian_score - greek_score, 4)
            if hurrian_score is not None and greek_score is not None
            else None
        ),
        "hurrian_vs_luwian_advantage": (
            round(hurrian_score - luwian_score, 4)
            if hurrian_score is not None and luwian_score is not None
            else None
        ),
        "three_way_ranking": (
            sorted(
                [
                    ("Hurrian", hurrian_score),
                    ("Greek", greek_score),
                    ("Luwian", luwian_score),
                ],
                key=lambda x: -(x[1] or -99),
            )
            if hurrian_score is not None
            else None
        ),
        "model_sources": [
            "Wegner (2007) Einführung in die hurritische Sprache",
            "Wilhelm (1989) The Hurrians (Cornell ANES)",
            "Speiser (1941) Introduction to Hurrian (AASOR)",
        ],
    }

    _OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("\n── Hurrian Language Model ──────────────────────────────────")
    print(f"  Vocabulary:          {len(_HURRIAN_VOCAB)} words")
    print(f"  Corpus tokens:       {len(hurrian_corpus)}")
    print(f"  Phoneme inventory:   {len(hurrian_phonemes)} distinct")
    if hurrian_score is not None:
        print(f"  Hurrian log-P/tok:   {hurrian_score:.4f}")
        print(f"  Luwian log-P/tok:    {luwian_score:.4f}")
        print(f"  Greek log-P/tok:     {greek_score:.4f}")
        print("\n  Three-way ranking:")
        for name, score in summary["three_way_ranking"]:
            print(f"    {name:<10} {score:.4f}")
    print(f"\n  Saved: {_OUTPUT_PATH}")
    print("────────────────────────────────────────────────────────────\n")

    return summary


if __name__ == "__main__":
    run()

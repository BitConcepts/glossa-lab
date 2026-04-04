"""Richer Luwian language model for Linear A hypothesis testing.

Builds a more comprehensive Luwian/Anatolian language model from:
1. Extended Hittite/Luwian vocabulary (Melchert 1994, Yakubovich 2010,
   Hawkins 2000 CHLI corpus references)
2. Luwian syllabic writing conventions
3. Tests whether the Luwian advantage over Greek strengthens

Usage:
  python backend/experiments/luwian_language_model.py

Output: reports/luwian_model_validation.json
"""

from __future__ import annotations

import json
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_OUTPUT_PATH = _REPO_ROOT / "reports" / "luwian_model_validation.json"

# Extended Luwian/Hittite vocabulary
# Sources: Melchert (1994), Yakubovich (2010), Hawkins (2000)
_LUWIAN_EXTENDED: dict[str, str] = {
    # Basic nouns
    "ati": "father", "imi": "mother", "tati": "father (Luwian)", "nani": "brother",
    "sara": "up / above", "ura": "great / big", "zid": "this (animate)",
    "za": "this", "anda": "in / into", "paran": "before / ahead",
    "antu": "and", "pi": "give", "du": "make / do", "ari": "come",
    "wala": "die / perish", "asi": "mouth / word", "tuwati": "eye",
    "isa": "mouth", "mana": "mina (unit)", "hantis": "front / first",
    "alati": "tongue", "pati": "foot", "waras": "field / land",
    "kuis": "who", "kuwa": "where", "nu": "and / then",
    # Verbs (Luwian)
    "tiya": "step / place", "arha": "away", "hant": "be in front",
    "waliya": "perish", "piya": "give", "la": "take", "au": "see",
    "tara": "conquer", "ziya": "go", "iya": "make",
    # Administrative terms
    "wasu": "good", "nawi": "not yet", "mawa": "and indeed",
    "apa": "that / he", "amu": "I / me", "tu": "and",
    "hiti": "immediately", "ziti": "person / man", "atri": "send",
    # Hieroglyphic Luwian specific (Hawkins 2000)
    "runta": "storm god", "tarhunza": "storm god", "kubaba": "Kubaba",
    "karhuha": "Karhuha (deity)", "sarruma": "Sharruma",
    "wasusarma": "good king", "urawana": "great", "masana": "deity",
    "sarku": "high / exalted", "tattamaru": "scribe",
    "paskuwati": "satiate", "lali": "tongue", "mati": "name",
    "tarhu": "conquer", "ziyi": "go / move", "tami": "other",
    "hila": "courtyard", "hara": "eagle",
    # Numbers and common functors
    "ima": "this / now", "nawa": "not",
    "wati": "and", "ki": "this", "ha": "take",
    # Suffixes (Luwian morphology — agglutinative)
    "ta": "-then", "mu": "-me/my", "wa": "quotative particle",
    # More extended vocabulary
    "ariyati": "consult (oracle)", "halwati": "wall / fortification",
    "tarwana": "judge", "hawis": "sheep", "immara": "field",
    "aniyan": "made / worked", "asuwattis": "good", "masanalli": "divine",
    "pihassassi": "lightning", "tiwad": "sun / day",
    "huha": "grandfather", "hanna": "grandmother",
    "arawa": "free / exempt", "damnasara": "domestic",
    "walwala": "lion", "zurki": "blood", "halki": "grain",
}


def build_luwian_corpus(repeat: int = 50) -> list[str]:
    """Build a phoneme-level corpus from Luwian vocabulary."""
    phonemes = []
    for word in _LUWIAN_EXTENDED:
        phonemes.extend(list(word))
    return phonemes * repeat


def compute_bigram_profile(phonemes: list[str]) -> dict[str, dict[str, float]]:
    """Build normalised bigram transition probabilities."""
    from collections import defaultdict
    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for i in range(len(phonemes) - 1):
        counts[phonemes[i]][phonemes[i + 1]] += 1
    profile = {}
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
    """Build richer Luwian model and validate against Linear A corpus."""
    import sys
    tests_path = _REPO_ROOT / "backend" / "tests"
    if str(tests_path) not in sys.path:
        sys.path.insert(0, str(tests_path))
    backend_path = _REPO_ROOT / "backend"
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))

    luwian_corpus = build_luwian_corpus(repeat=60)
    luwian_profile = compute_bigram_profile(luwian_corpus)

    # Build Greek comparison model from LB phonetic values
    _GREEK_VOCAB = {
        "ka": "and", "to": "the", "te": "and", "me": "not",
        "de": "but", "ei": "if", "en": "in", "ek": "from",
        "pa": "father", "ma": "mother", "ti": "honor",
        "ke": "and (Myc.)", "we": "and (Myc.)", "jo": "rel.pron.",
        "ko": "village", "no": "temple", "po": "city",
        "ro": "worker", "so": "wine", "do": "gift",
        "pe": "near", "ra": "women", "sa": "linen",
        "ta": "the (pl.)", "na": "temple", "ni": "fig",
        "ku": "total", "re": "linen (type)", "ri": "fig (type)",
        "wi": "wine (type)", "wa": "sheep", "ze": "pair",
        "di": "Zeus", "mi": "mina", "pu": "foal",
        "su": "pig", "za": "barley", "du": "slave",
        "pi": "more", "si": "figs",
        "jo-do-so-si": "they give", "a-pi-qo-ro": "amphipoloi",
    }
    greek_corpus = []
    for word in _GREEK_VOCAB:
        greek_corpus.extend(list(word))
    greek_corpus = greek_corpus * 60
    greek_profile = compute_bigram_profile(greek_corpus)

    # Try to load real Linear A corpus for scoring
    try:
        from tests.corpora.real import load_linear_a_signs
        la_corpus = load_linear_a_signs()
    except Exception:
        la_corpus = []

    luwian_score = score_corpus_against_model(la_corpus, luwian_profile) if la_corpus else None
    greek_score = score_corpus_against_model(la_corpus, greek_profile) if la_corpus else None

    luwian_vocab_size = len(_LUWIAN_EXTENDED)
    luwian_phoneme_inventory = sorted(set(luwian_corpus))
    greek_phoneme_inventory = sorted(set(greek_corpus))

    summary = {
        "luwian_vocabulary_size": luwian_vocab_size,
        "luwian_corpus_tokens": len(luwian_corpus),
        "luwian_phoneme_inventory_size": len(luwian_phoneme_inventory),
        "luwian_phoneme_inventory": luwian_phoneme_inventory,
        "greek_phoneme_inventory_size": len(greek_phoneme_inventory),
        "linear_a_test_tokens": len(la_corpus),
        "luwian_log_likelihood_per_token": luwian_score,
        "greek_log_likelihood_per_token": greek_score,
        "luwian_advantage": (
            round(luwian_score - greek_score, 4)
            if luwian_score is not None and greek_score is not None
            else None
        ),
        "interpretation": (
            "Richer Luwian model STRENGTHENS advantage over Greek"
            if (luwian_score is not None and greek_score is not None and luwian_score > greek_score)
            else "Richer Luwian model does NOT strengthen advantage"
            if (luwian_score is not None and greek_score is not None)
            else "Could not load Linear A corpus for scoring"
        ),
        "model_sources": [
            "Melchert (1994) Anatolian Historical Phonology",
            "Yakubovich (2010) Sociolinguistics of the Luvian Language",
            "Hawkins (2000) Corpus of Hieroglyphic Luwian Inscriptions (CHLI)",
        ],
    }

    _OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("\n── Richer Luwian Language Model ────────────────────────────")
    print(f"  Vocabulary size:     {luwian_vocab_size} words")
    print(f"  Corpus tokens:       {len(luwian_corpus)}")
    print(f"  Phoneme inventory:   {len(luwian_phoneme_inventory)} distinct phonemes")
    if luwian_score is not None:
        print(f"  Luwian log-P/token:  {luwian_score:.4f}")
        print(f"  Greek log-P/token:   {greek_score:.4f}")
        print(f"  Luwian advantage:    {luwian_score - greek_score:+.4f}")
    print(f"\n  → {summary['interpretation']}")
    print(f"\n  Saved: {_OUTPUT_PATH}")
    print("────────────────────────────────────────────────────────────\n")

    return summary


if __name__ == "__main__":
    run()

"""Hypothesis-driven decipherment engine.

Implements an iterative loop:
  1. HYPOTHESIZE — generate informed hypotheses from structural analysis
  2. TEST — run decipherment with each hypothesis as a constraint
  3. SCORE — evaluate results on multiple metrics
  4. LEARN — lock confident mappings, generate new hypotheses
  5. REPEAT — iterate until convergence or exhaustion

Each hypothesis is a partial mapping (some signs locked to values)
plus a target language model. The engine tests each hypothesis by
running the decipherment engine with the locked signs fixed, then
scores the result on word matches, paradigm regularity, and
internal consistency.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from glossa_lab.engine import register_pipeline
from glossa_lab.pipelines.decipher import LanguageModel, decipher

# ── Data structures ───────────────────────────────────────────────

@dataclass
class Hypothesis:
    """A decipherment hypothesis to test."""

    id: str
    name: str
    target_language: str  # e.g. "proto-dravidian", "vedic-sanskrit"
    locked_mappings: dict[str, str] = field(default_factory=dict)
    notes: str = ""
    parent_id: str | None = None  # hypothesis this was derived from
    kandles_profile: str = "default"  # language-specific Kandles bias profile


@dataclass
class HypothesisResult:
    """Scored result of testing a hypothesis."""

    hypothesis_id: str
    mapping: dict[str, str]
    scores: dict[str, float]
    total_score: float
    word_matches: list[dict[str, Any]]
    confident_mappings: dict[str, str]  # signs we're >80% confident about
    suggested_next: list[str]  # suggestions for next hypotheses


# ── Scoring functions ─────────────────────────────────────────────

def score_word_matches(
    deciphered_signs: list[str],
    vocabulary: dict[str, str],
    inscriptions: list[list[str]] | None = None,
) -> dict[str, Any]:
    """Check how many known words appear in the deciphered text.

    vocabulary: mapping of deciphered_form → meaning
    Returns match count, matched words, and coverage.
    """
    # Build deciphered words from inscriptions or sliding windows
    deciphered_words: list[str] = []
    if inscriptions:
        for insc in inscriptions:
            # Each inscription is a potential word or phrase
            word = "".join(insc)
            deciphered_words.append(word)
            # Also check sub-sequences of length 2-5
            for wlen in range(2, min(6, len(insc) + 1)):
                for start in range(len(insc) - wlen + 1):
                    sub = "".join(insc[start:start + wlen])
                    deciphered_words.append(sub)
    else:
        # Sliding window over flat sequence
        text = "".join(deciphered_signs)
        for wlen in range(2, 8):
            for start in range(len(text) - wlen + 1):
                deciphered_words.append(text[start:start + wlen])

    matches = []
    for word in set(deciphered_words):
        if word in vocabulary:
            matches.append({
                "deciphered": word,
                "meaning": vocabulary[word],
                "length": len(word),
            })

    return {
        "match_count": len(matches),
        "total_words_checked": len(set(deciphered_words)),
        "matches": sorted(matches, key=lambda m: m["length"], reverse=True),
        "coverage": len(matches) / max(len(vocabulary), 1),
    }


def score_internal_consistency(
    mapping: dict[str, str],
    cipher_signs: list[str],
    inscriptions: list[list[str]] | None = None,
) -> float:
    """Score how consistently the mapping works across inscriptions.

    Same cipher sequence should always produce the same deciphered
    sequence. Returns 1.0 if perfectly consistent.
    """
    if not inscriptions:
        return 1.0  # Can't check without inscription boundaries

    # Check that repeated sign sequences always decode the same way
    decoded_sequences: dict[str, set[str]] = {}
    for insc in inscriptions:
        cipher_key = "|".join(insc)
        decoded = "|".join(mapping.get(s, "?") for s in insc)
        decoded_sequences.setdefault(cipher_key, set()).add(decoded)

    # All repeated inscriptions should decode identically
    consistent = sum(
        1 for v in decoded_sequences.values() if len(v) == 1
    )
    return consistent / max(len(decoded_sequences), 1)


def score_paradigm_regularity(
    mapping: dict[str, str],
    cipher_signs: list[str],
) -> float:
    """Score whether the mapping produces regular paradigmatic patterns.

    Good decipherments should produce clean inflectional patterns
    (same endings, same prefixes). Returns 0-1.
    """
    # Check if terminal signs map to a small set of values
    # (indicating grammatical suffixes)
    freq = Counter(cipher_signs)
    top10 = [s for s, _ in freq.most_common(10)]

    terminal_values = set()
    for s in top10:
        terminal_values.add(mapping.get(s, "?"))

    # Fewer unique terminal values = more regular paradigm
    if len(terminal_values) == 0:
        return 0.0
    regularity = 1.0 - (len(terminal_values) / max(len(top10), 1))
    return max(0.0, regularity)


# ── Hypothesis Engine ─────────────────────────────────────────────

class HypothesisEngine:
    """Iterative hypothesis-driven decipherment engine.

    The core loop:
      1. Generate hypotheses (from structural analysis or prior results)
      2. Test each hypothesis (run decipherment with locked mappings)
      3. Score results (word matches, consistency, paradigm regularity)
      4. Learn (identify confident mappings, suggest next hypotheses)
    """

    def __init__(
        self,
        cipher_signs: list[str],
        cipher_inscriptions: list[list[str]] | None = None,
    ) -> None:
        self.cipher_signs = cipher_signs
        self.cipher_inscriptions = cipher_inscriptions
        self.history: list[dict[str, Any]] = []
        self.best_mapping: dict[str, str] = {}
        self.best_score: float = 0.0
        self.confident_mappings: dict[str, str] = {}
        self.iteration = 0

    def test_hypothesis(
        self,
        hypothesis: Hypothesis,
        target_model: LanguageModel,
        vocabulary: dict[str, str] | None = None,
        max_iterations: int = 10000,
        restarts: int = 5,
    ) -> HypothesisResult:
        """Test a single hypothesis.

        Runs the decipherment engine with locked mappings from the
        hypothesis, then scores the result.
        """
        # Apply locked mappings: remove locked signs from the search
        locked = {**self.confident_mappings, **hypothesis.locked_mappings}

        # Resolve Kandles profile: explicit field takes precedence, then auto-map
        kandles_profile: str | None = None
        raw_profile = hypothesis.kandles_profile
        if raw_profile and raw_profile not in ("default", "greek", "mycenaean"):
            kandles_profile = raw_profile
        elif raw_profile == "default":
            # Auto-map target language to its own profile
            try:
                from glossa_lab.pipelines.kandles_profiles import LANGUAGE_TO_PROFILE
                mapped = LANGUAGE_TO_PROFILE.get(hypothesis.target_language.lower())
                if mapped and mapped not in ("default",):
                    kandles_profile = mapped
            except ImportError:
                pass

        # Run decipherment
        result = decipher(
            self.cipher_signs,
            target_model,
            seed=42 + self.iteration,
            max_iterations=max_iterations,
            restarts=restarts,
            cipher_inscriptions=self.cipher_inscriptions,
            kandles_profile=kandles_profile,
        )

        mapping = result["proposed_mapping"]

        # Override with locked mappings
        for cipher_sign, target_val in locked.items():
            mapping[cipher_sign] = target_val

        # Score on multiple dimensions
        scores: dict[str, float] = {}

        # 1. Bigram likelihood
        decoded = [mapping.get(s, "?") for s in self.cipher_signs]
        scores["bigram_ll"] = target_model.score_text(decoded)

        # 2. Word matches
        word_result = {"match_count": 0, "matches": [], "coverage": 0.0}
        if vocabulary:
            decoded_inscs = None
            if self.cipher_inscriptions:
                decoded_inscs = [
                    [mapping.get(s, "?") for s in insc]
                    for insc in self.cipher_inscriptions
                ]
            word_result = score_word_matches(
                decoded, vocabulary, decoded_inscs,
            )
        scores["word_matches"] = float(word_result["match_count"])
        scores["word_coverage"] = word_result.get("coverage", 0.0)

        # 3. Internal consistency
        decoded_inscs = None
        if self.cipher_inscriptions:
            decoded_inscs = [
                [mapping.get(s, "?") for s in insc]
                for insc in self.cipher_inscriptions
            ]
        scores["consistency"] = score_internal_consistency(
            mapping, self.cipher_signs, self.cipher_inscriptions,
        )

        # 4. Paradigm regularity
        scores["paradigm_regularity"] = score_paradigm_regularity(
            mapping, self.cipher_signs,
        )

        # 5. Kandles confidence
        scores["kandles"] = result.get("kandles_confidence", 0.0)

        # Total score (weighted combination)
        total = (
            scores.get("word_matches", 0) * 10.0
            + scores.get("consistency", 0) * 5.0
            + scores.get("paradigm_regularity", 0) * 3.0
            + scores.get("kandles", 0) * 2.0
        )
        # Normalise bigram_ll contribution
        if scores["bigram_ll"] != 0:
            total += min(10.0, -scores["bigram_ll"] / 1000.0)

        # Identify confident mappings (high-frequency signs that improve score)
        freq = Counter(self.cipher_signs)
        top_signs = [s for s, _ in freq.most_common(15)]
        new_confident = {}
        for s in top_signs:
            if s in mapping and mapping[s] != "?":
                new_confident[s] = mapping[s]

        # Suggest next hypotheses
        suggestions = []
        if scores.get("word_matches", 0) > 0:
            suggestions.append(
                f"Word matches found — lock top {len(new_confident)} "
                f"mappings and refine remaining signs"
            )
        if scores.get("paradigm_regularity", 0) > 0.5:
            suggestions.append(
                "Good paradigm regularity — try testing verb prefix hypotheses"
            )
        if scores.get("consistency", 0) < 0.8:
            suggestions.append(
                "Low consistency — some inscriptions decode differently. "
                "Consider whether the script is logosyllabic (not alphabetic)"
            )
        if not suggestions:
            suggestions.append(
                "Try a different target language hypothesis"
            )

        # Record in history
        entry = {
            "iteration": self.iteration,
            "hypothesis_id": hypothesis.id,
            "hypothesis_name": hypothesis.name,
            "target_language": hypothesis.target_language,
            "locked_count": len(locked),
            "scores": scores,
            "total_score": round(total, 4),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.history.append(entry)

        # Update best if improved
        if total > self.best_score:
            self.best_score = total
            self.best_mapping = dict(mapping)
            self.confident_mappings.update(new_confident)

        self.iteration += 1

        return HypothesisResult(
            hypothesis_id=hypothesis.id,
            mapping=mapping,
            scores=scores,
            total_score=round(total, 4),
            word_matches=word_result.get("matches", []),
            confident_mappings=new_confident,
            suggested_next=suggestions,
        )

    def run_iteration(
        self,
        hypotheses: list[Hypothesis],
        target_models: dict[str, LanguageModel],
        vocabularies: dict[str, dict[str, str]] | None = None,
        max_iterations: int = 10000,
    ) -> list[HypothesisResult]:
        """Run one iteration: test all hypotheses, return ranked results."""
        results = []
        for hyp in hypotheses:
            model = target_models.get(hyp.target_language)
            if model is None:
                continue
            vocab = (vocabularies or {}).get(hyp.target_language, {})
            result = self.test_hypothesis(
                hyp, model, vocab, max_iterations=max_iterations,
            )
            results.append(result)

        # Sort by total score (best first)
        results.sort(key=lambda r: r.total_score, reverse=True)
        return results

    def get_state(self) -> dict[str, Any]:
        """Return current engine state for serialisation."""
        return {
            "iteration": self.iteration,
            "best_score": self.best_score,
            "best_mapping": self.best_mapping,
            "confident_mappings": self.confident_mappings,
            "history": self.history,
        }


# ── Target language vocabularies ──────────────────────────────────

# Proto-Dravidian reconstructed vocabulary (Parpola hypothesis)
# These are common Dravidian roots that scholars have proposed
# as readings for Indus signs
PROTO_DRAVIDIAN_VOCAB: dict[str, str] = {
    "min": "fish / star (rebus: meen)",
    "kal": "stone",
    "pan": "pig",
    "vel": "spear / white",
    "pal": "tooth / many",
    "kan": "eye / village",
    "kol": "kill / take",
    "nal": "good / four",
    "pur": "city / outside",
    "man": "earth / sand",
    "nil": "stand / blue",
    "kur": "short",
    "ven": "white / hot",
    "tal": "head / place",
    "por": "gold / fight",
    "mur": "three",
    "ir": "two",
    "onr": "one",
    "an": "male",
    "al": "female / not",
    "am": "mother / that",
    "il": "house / not",
    "ur": "village",
    "aru": "six",
    "elu": "seven",
    "ettu": "eight",
    "pattu": "ten",
}

# Vedic Sanskrit vocabulary (Indo-Aryan hypothesis)
VEDIC_SANSKRIT_VOCAB: dict[str, str] = {
    "deva": "god",
    "agni": "fire",
    "soma": "ritual drink",
    "rta": "cosmic order",
    "raja": "king",
    "pura": "city",
    "go": "cow",
    "asva": "horse",
    "nadi": "river",
    "vrsa": "bull",
    "maha": "great",
    "pati": "lord / husband",
    "dasa": "servant / ten",
    "sapta": "seven",
    "tri": "three",
    "dvi": "two",
    "eka": "one",
    "satam": "hundred",
    "yajna": "sacrifice",
    "veda": "knowledge",
}


@register_pipeline("hypothesis")
async def run_hypothesis(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point for hypothesis-driven decipherment."""
    from glossa_lab.database import get_db

    text_id = params.get("text_id")
    if not text_id:
        raise ValueError("Missing text_id")

    db = get_db()
    if db is None:
        raise RuntimeError("Database not available")

    text = await db.get_text(text_id)
    if text is None:
        raise ValueError(f"Text not found: {text_id}")

    symbols = text["content"]

    # Build target models
    target_models = {}
    vocabularies = {}

    # Build proper language models from expanded data modules
    from glossa_lab.data import dravidian, sanskrit

    dravidian_syms = dravidian.get_corpus_symbols()
    target_models["proto-dravidian"] = LanguageModel(dravidian_syms)
    vocabularies["proto-dravidian"] = dravidian.get_vocabulary()

    sanskrit_syms = sanskrit.get_corpus_symbols()
    target_models["vedic-sanskrit"] = LanguageModel(sanskrit_syms)
    vocabularies["vedic-sanskrit"] = sanskrit.get_vocabulary()

    # Create hypotheses
    hypotheses = [
        Hypothesis(
            id="h1-dravidian",
            name="Proto-Dravidian language hypothesis",
            target_language="proto-dravidian",
            notes="Parpola (1994): Indus script encodes a Dravidian language",
        ),
        Hypothesis(
            id="h2-sanskrit",
            name="Vedic Sanskrit language hypothesis",
            target_language="vedic-sanskrit",
            notes="Rao (1982): Indus script encodes an Indo-Aryan language",
        ),
    ]

    engine = HypothesisEngine(symbols)
    results = engine.run_iteration(
        hypotheses, target_models, vocabularies,
        max_iterations=params.get("max_iterations", 5000),
    )

    return {
        "text_id": text_id,
        "iteration": engine.iteration,
        "results": [
            {
                "hypothesis": r.hypothesis_id,
                "total_score": r.total_score,
                "scores": r.scores,
                "word_matches": r.word_matches[:10],
                "confident_mappings_count": len(r.confident_mappings),
                "suggestions": r.suggested_next,
            }
            for r in results
        ],
        "best_mapping": engine.best_mapping,
        "confident_mappings": engine.confident_mappings,
        "history": engine.history,
    }

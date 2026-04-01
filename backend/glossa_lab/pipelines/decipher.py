"""Substitution cipher decipherment engine.

Cracks a substitution cipher by matching the statistical fingerprint
of the ciphered text against a known target language model.

Approach (3-stage):
  1. SEED: Frequency-rank mapping — most frequent cipher sign →
     most frequent target phoneme, etc.
  2. REFINE: Bigram correlation — swap pairs in the mapping to
     maximise bigram log-likelihood against the target model.
  3. VALIDATE: Score the final mapping and report accuracy.

This implements the core insight behind historical decipherments:
if you know (or hypothesise) the language family, you can match
the statistical fingerprint of the unknown script against the
known language to propose sound values.

The Kandles system (Merkur patent) assists by providing a cross-
language phonetic similarity check: if the proposed decipherment
produces Kandles color patterns similar to the target language,
confidence increases.
"""

from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from typing import Any

from glossa_lab.engine import register_pipeline

# ── Language model ────────────────────────────────────────────────────

class LanguageModel:
    """Unigram + bigram + trigram language model with positional stats."""

    def __init__(
        self,
        symbols: list[str],
        inscriptions: list[list[str]] | None = None,
    ) -> None:
        self.symbols = symbols
        total = len(symbols)
        self.alphabet = sorted(set(symbols))
        self.size = len(self.alphabet)

        # Unigram frequencies (normalised)
        counts = Counter(symbols)
        self.unigram_freq: dict[str, float] = {
            s: c / total for s, c in counts.items()
        }
        self.ranked = [s for s, _ in counts.most_common()]

        # Bigram frequencies
        bigram_counts: Counter[tuple[str, str]] = Counter()
        for i in range(len(symbols) - 1):
            bigram_counts[(symbols[i], symbols[i + 1])] += 1
        bigram_total = sum(bigram_counts.values()) or 1
        self.bigram_freq: dict[tuple[str, str], float] = {
            bg: c / bigram_total for bg, c in bigram_counts.items()
        }

        # Trigram frequencies
        trigram_counts: Counter[tuple[str, str, str]] = Counter()
        for i in range(len(symbols) - 2):
            trigram_counts[(symbols[i], symbols[i + 1], symbols[i + 2])] += 1
        trigram_total = sum(trigram_counts.values()) or 1
        self.trigram_freq: dict[tuple[str, str, str], float] = {
            tg: c / trigram_total for tg, c in trigram_counts.items()
        }

        # Positional profiles (if inscriptions provided)
        self.positional: dict[str, dict[str, float]] = {}
        if inscriptions:
            pos_counts: dict[str, dict[str, int]] = defaultdict(
                lambda: {"initial": 0, "medial": 0, "terminal": 0}
            )
            for insc in inscriptions:
                if len(insc) >= 2:
                    pos_counts[insc[0]]["initial"] += 1
                    pos_counts[insc[-1]]["terminal"] += 1
                    for s in insc[1:-1]:
                        pos_counts[s]["medial"] += 1
            for sign, pc in pos_counts.items():
                t = sum(pc.values()) or 1
                self.positional[sign] = {
                    k: v / t for k, v in pc.items()
                }

    def score_text(self, text: list[str]) -> float:
        """Combined bigram + trigram log-likelihood.

        Trigrams are only used when the corpus is large enough
        for meaningful trigram statistics (>1000 symbols).
        """
        smoothing = 1e-8
        ll = 0.0
        # Bigram component (always used)
        for i in range(len(text) - 1):
            p = self.bigram_freq.get((text[i], text[i + 1]), smoothing)
            ll += math.log(p)
        # Trigram component (only if corpus is large enough)
        if len(self.symbols) >= 1000 and len(text) > 2:
            tri_ll = 0.0
            for i in range(len(text) - 2):
                p = self.trigram_freq.get(
                    (text[i], text[i + 1], text[i + 2]), smoothing,
                )
                tri_ll += math.log(p)
            # Light blend: 90% bigram + 10% trigram
            ll = 0.9 * ll + 0.1 * tri_ll
        return ll


# ── Decipherment engine ──────────────────────────────────────────

def decipher(
    cipher_signs: list[str],
    target_model: LanguageModel,
    seed: int = 42,
    max_iterations: int = 5000,
    restarts: int = 3,
    cipher_inscriptions: list[list[str]] | None = None,
) -> dict[str, Any]:
    """Crack a substitution cipher.

    Args:
        cipher_signs: the encrypted symbol sequence.
        target_model: language model of the target (known) language.
        seed: random seed for hill climbing.
        max_iterations: max swaps per restart.
        restarts: number of random restarts.
        cipher_inscriptions: optional inscription-level structure for
            positional constraint scoring.

    Returns:
        dict with proposed_mapping, deciphered_text, score, and stats.
    """
    rng = random.Random(seed)

    cipher_alphabet = sorted(set(cipher_signs))
    target_alphabet = target_model.ranked[: len(cipher_alphabet)]

    while len(target_alphabet) < len(cipher_alphabet):
        target_alphabet.append(f"?{len(target_alphabet)}")

    # Build cipher positional profiles (if inscriptions provided)
    cipher_positional: dict[str, dict[str, float]] = {}
    if cipher_inscriptions:
        pos_counts: dict[str, dict[str, int]] = defaultdict(
            lambda: {"initial": 0, "medial": 0, "terminal": 0}
        )
        for insc in cipher_inscriptions:
            if len(insc) >= 2:
                pos_counts[insc[0]]["initial"] += 1
                pos_counts[insc[-1]]["terminal"] += 1
                for s in insc[1:-1]:
                    pos_counts[s]["medial"] += 1
        for sign, pc in pos_counts.items():
            t = sum(pc.values()) or 1
            cipher_positional[sign] = {k: v / t for k, v in pc.items()}

    # Stage 1: SEED — frequency-rank mapping
    cipher_counts = Counter(cipher_signs)
    cipher_ranked = [s for s, _ in cipher_counts.most_common()]

    best_mapping: dict[str, str] = {}
    best_score = float("-inf")

    for restart in range(restarts):
        if restart == 0:
            mapping = dict(zip(cipher_ranked, target_alphabet))
        else:
            shuffled = list(target_alphabet)
            rng.shuffle(shuffled)
            mapping = dict(zip(cipher_ranked, shuffled))

        # Stage 2: REFINE — hill climbing with combined scoring
        current_score = _score_mapping(
            cipher_signs, mapping, target_model,
            cipher_positional,
        )

        no_improve = 0
        for _iteration in range(max_iterations):
            i = rng.randint(0, len(cipher_ranked) - 1)
            j = rng.randint(0, len(cipher_ranked) - 1)
            if i == j:
                continue

            a, b = cipher_ranked[i], cipher_ranked[j]
            mapping[a], mapping[b] = mapping[b], mapping[a]

            new_score = _score_mapping(
                cipher_signs, mapping, target_model,
                cipher_positional,
            )

            if new_score > current_score:
                current_score = new_score
                no_improve = 0
            else:
                mapping[a], mapping[b] = mapping[b], mapping[a]
                no_improve += 1

            if no_improve > 500:
                break

        if current_score > best_score:
            best_score = current_score
            best_mapping = dict(mapping)

    # Stage 3: VALIDATE — apply mapping + Kandles confidence
    deciphered = [best_mapping.get(s, "?") for s in cipher_signs]

    # Kandles validation (Merkur patent)
    kandles_confidence = _kandles_validate(deciphered, target_model.symbols)

    return {
        "proposed_mapping": best_mapping,
        "deciphered_text": deciphered,
        "score": round(best_score, 4),
        "kandles_confidence": kandles_confidence,
        "cipher_alphabet_size": len(cipher_alphabet),
        "target_alphabet_size": target_model.size,
    }


def _score_mapping(
    cipher_signs: list[str],
    mapping: dict[str, str],
    target_model: LanguageModel,
    cipher_positional: dict[str, dict[str, float]] | None = None,
) -> float:
    """Score a mapping by trigram log-likelihood + positional match."""
    decoded = [mapping.get(s, "?") for s in cipher_signs]
    ll = target_model.score_text(decoded)

    # Positional bonus: reward mappings where positional profiles match
    if cipher_positional and target_model.positional:
        pos_score = 0.0
        for cipher_sign, cipher_pos in cipher_positional.items():
            target_sign = mapping.get(cipher_sign)
            if target_sign and target_sign in target_model.positional:
                target_pos = target_model.positional[target_sign]
                # Cosine-like dot product of positional vectors
                for pos_key in ("initial", "medial", "terminal"):
                    pos_score += (
                        cipher_pos.get(pos_key, 0)
                        * target_pos.get(pos_key, 0)
                    )
        # Very light positional bonus (avoid destabilizing hill climbing)
        ll += pos_score * abs(ll) * 0.005

    return ll


def _kandles_validate(
    deciphered: list[str], target_symbols: list[str],
) -> float:
    """Kandles cross-validation: compare phonetic color distributions.

    Uses the Merkur patent Kandles system to compare the phonetic
    fingerprint of the deciphered text against the target text.
    Returns a confidence score in [0, 1].
    """
    try:
        from glossa_lab.pipelines.kandles import compare_grids, generate_grid
        grid_dec = generate_grid(deciphered[:200])
        grid_tgt = generate_grid(target_symbols[:200])
        result = compare_grids(grid_dec, grid_tgt)
        return result["similarity"]
    except Exception:
        return 0.0


# ── Auto-dispatch: CPSC if available, hill climbing fallback ──────

def _cpsc_available() -> bool:
    """Check if the CPSC module is installed."""
    try:
        from glossa_lab.cpsc import CPSC_AVAILABLE
        return CPSC_AVAILABLE
    except ImportError:
        return False


def decipher_auto(
    cipher_signs: list[str],
    target_model: LanguageModel,
    seed: int = 42,
    max_iterations: int = 10000,
    restarts: int = 5,
    cipher_inscriptions: list[list[str]] | None = None,
    engine: str = "auto",
) -> dict[str, Any]:
    """Decipher with automatic engine selection.

    engine:
      "auto" — use CPSC if available, hill climbing otherwise
      "cpsc" — force CPSC (raises if not available)
      "hillclimb" — force hill climbing
    """
    use_cpsc = False
    if engine == "auto":
        use_cpsc = _cpsc_available()
    elif engine == "cpsc":
        if not _cpsc_available():
            raise RuntimeError(
                "CPSC module not available. "
                "Install glossa_lab.cpsc or use engine='hillclimb'."
            )
        use_cpsc = True

    if use_cpsc:
        from glossa_lab.cpsc.projection import cpsc_project
        return cpsc_project(
            cipher_signs, target_model,
            seed=seed, max_epochs=max_iterations, restarts=restarts,
        )

    # Fallback: hill climbing
    return decipher(
        cipher_signs, target_model,
        seed=seed, max_iterations=max_iterations, restarts=restarts,
        cipher_inscriptions=cipher_inscriptions,
    )


def score_accuracy(
    proposed: dict[str, str],
    answer_key: dict[str, str],
) -> dict[str, Any]:
    """Score a proposed mapping against the answer key.

    answer_key: cipher_sign → true_phoneme
    proposed: cipher_sign → proposed_phoneme
    """
    correct = 0
    total = 0
    details = []
    for sign, true_val in answer_key.items():
        proposed_val = proposed.get(sign, "?")
        match = proposed_val == true_val
        if match:
            correct += 1
        total += 1
        details.append({
            "sign": sign, "true": true_val,
            "proposed": proposed_val, "correct": match,
        })

    return {
        "correct": correct,
        "total": total,
        "accuracy": round(correct / total, 3) if total > 0 else 0,
        "details": details,
    }


@register_pipeline("decipher")
async def run_decipher(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point.

    Params:
        text_id: cipher text corpus
        target_text_id: target language corpus (for building model)
        max_iterations: hill climbing iterations (default 5000)
        restarts: number of random restarts (default 3)
    """
    from glossa_lab.database import get_db

    text_id = params.get("text_id")
    target_text_id = params.get("target_text_id")
    if not text_id or not target_text_id:
        raise ValueError("Requires text_id and target_text_id")

    db = get_db()
    if db is None:
        raise RuntimeError("Database not available")

    cipher_text = await db.get_text(text_id)
    target_text = await db.get_text(target_text_id)
    if cipher_text is None or target_text is None:
        raise ValueError("Text not found")

    target_model = LanguageModel(target_text["content"])
    result = decipher(
        cipher_text["content"],
        target_model,
        max_iterations=params.get("max_iterations", 5000),
        restarts=params.get("restarts", 3),
    )
    result["cipher_text_id"] = text_id
    result["target_text_id"] = target_text_id
    return result

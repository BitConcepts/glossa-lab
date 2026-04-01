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
from collections import Counter
from typing import Any

from glossa_lab.engine import register_pipeline

# ── Language model ────────────────────────────────────────────────

class LanguageModel:
    """Simple unigram + bigram language model from a corpus."""

    def __init__(self, symbols: list[str]) -> None:
        self.symbols = symbols
        total = len(symbols)
        self.alphabet = sorted(set(symbols))
        self.size = len(self.alphabet)

        # Unigram frequencies (normalised)
        counts = Counter(symbols)
        self.unigram_freq: dict[str, float] = {
            s: c / total for s, c in counts.items()
        }
        # Rank order (most frequent first)
        self.ranked = [s for s, _ in counts.most_common()]

        # Bigram frequencies
        bigram_counts: Counter[tuple[str, str]] = Counter()
        for i in range(len(symbols) - 1):
            bigram_counts[(symbols[i], symbols[i + 1])] += 1
        bigram_total = sum(bigram_counts.values()) or 1
        self.bigram_freq: dict[tuple[str, str], float] = {
            bg: c / bigram_total for bg, c in bigram_counts.items()
        }

    def bigram_log_likelihood(self, text: list[str]) -> float:
        """Compute bigram log-likelihood of a text under this model."""
        ll = 0.0
        smoothing = 1e-8
        for i in range(len(text) - 1):
            bg = (text[i], text[i + 1])
            p = self.bigram_freq.get(bg, smoothing)
            ll += math.log(p)
        return ll


# ── Decipherment engine ──────────────────────────────────────────

def decipher(
    cipher_signs: list[str],
    target_model: LanguageModel,
    seed: int = 42,
    max_iterations: int = 5000,
    restarts: int = 3,
) -> dict[str, Any]:
    """Crack a substitution cipher.

    Args:
        cipher_signs: the encrypted symbol sequence.
        target_model: language model of the target (known) language.
        seed: random seed for hill climbing.
        max_iterations: max swaps per restart.
        restarts: number of random restarts.

    Returns:
        dict with proposed_mapping, deciphered_text, score, and stats.
    """
    rng = random.Random(seed)

    cipher_alphabet = sorted(set(cipher_signs))
    target_alphabet = target_model.ranked[: len(cipher_alphabet)]

    # Pad if target has fewer symbols
    while len(target_alphabet) < len(cipher_alphabet):
        target_alphabet.append(f"?{len(target_alphabet)}")

    # Stage 1: SEED — frequency-rank mapping
    cipher_counts = Counter(cipher_signs)
    cipher_ranked = [s for s, _ in cipher_counts.most_common()]

    best_mapping: dict[str, str] = {}
    best_score = float("-inf")

    for restart in range(restarts):
        # Initial mapping: frequency-rank alignment
        if restart == 0:
            mapping = dict(zip(cipher_ranked, target_alphabet))
        else:
            # Random permutation for diversity
            shuffled = list(target_alphabet)
            rng.shuffle(shuffled)
            mapping = dict(zip(cipher_ranked, shuffled))

        # Stage 2: REFINE — hill climbing with bigram scoring
        current_score = _score_mapping(
            cipher_signs, mapping, target_model,
        )

        no_improve = 0
        for iteration in range(max_iterations):
            # Pick two random cipher signs and swap their mappings
            i = rng.randint(0, len(cipher_ranked) - 1)
            j = rng.randint(0, len(cipher_ranked) - 1)
            if i == j:
                continue

            a, b = cipher_ranked[i], cipher_ranked[j]
            mapping[a], mapping[b] = mapping[b], mapping[a]

            new_score = _score_mapping(
                cipher_signs, mapping, target_model,
            )

            if new_score > current_score:
                current_score = new_score
                no_improve = 0
            else:
                # Revert swap
                mapping[a], mapping[b] = mapping[b], mapping[a]
                no_improve += 1

            if no_improve > 500:
                break

        if current_score > best_score:
            best_score = current_score
            best_mapping = dict(mapping)

    # Stage 3: VALIDATE — apply best mapping
    deciphered = [best_mapping.get(s, "?") for s in cipher_signs]

    return {
        "proposed_mapping": best_mapping,
        "deciphered_text": deciphered,
        "score": round(best_score, 4),
        "cipher_alphabet_size": len(cipher_alphabet),
        "target_alphabet_size": target_model.size,
    }


def _score_mapping(
    cipher_signs: list[str],
    mapping: dict[str, str],
    target_model: LanguageModel,
) -> float:
    """Score a mapping by bigram log-likelihood under the target model."""
    decoded = [mapping.get(s, "?") for s in cipher_signs]
    return target_model.bigram_log_likelihood(decoded)


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

"""Corpus utilities shared across the Glossa Lab pipeline.

Key exports
-----------
normalise_sequences(words, reading_direction)
    Reverses each word in *words* when reading_direction is 'rtl'.
    All other experiments and the decipher pipeline should call this
    as their first step when dealing with a corpus that may be RTL.

run_ashraf_detection(words)
    Implements the Ashraf & Sinha (2018 PLoS ONE) handedness test.
    Computes the entropy at word position-0 (leftmost in file) and
    position-(-1) (rightmost in file).  The more constrained
    (lower-entropy) end is the word-END in any natural language.
    Returns a dict with H_pos0, H_posN1, gini values, inferred
    direction ('ltr' | 'rtl' | 'unknown'), and an interpretation string.

Reference
---------
Ashraf, M. & Sinha, P. (2018).  Handedness of language: Directional
symmetry breaking of sign usage in words.  PLOS ONE, 13(1), e0196609.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Any

# ── Internal helpers ────────────────────────────────────────────────────────


def _entropy(counts: dict[Any, int]) -> float:
    """Shannon entropy H in bits of a frequency distribution."""
    total = sum(counts.values()) or 1
    return -sum((c / total) * math.log2(c / total) for c in counts.values() if c > 0)


def _gini(counts: dict[Any, int]) -> float:
    """Gini coefficient of inequality for a frequency distribution.

    0 = perfectly equal; 1 = maximally concentrated.
    """
    vals = sorted(counts.values())
    n = len(vals)
    if n == 0:
        return 0.0
    total = sum(vals)
    if total == 0:
        return 0.0
    cumsum = 0.0
    g = 0.0
    for i, v in enumerate(vals, 1):
        cumsum += v
        g += (2 * i - n - 1) * v
    return g / (n * total)


# ── Public API ───────────────────────────────────────────────────────────────


def normalise_sequences(
    words: list[list[str]],
    reading_direction: str,
) -> list[list[str]]:
    """Return *words* normalised to left-to-right phonological order.

    Args:
        words:             List of words, each word being a list of sign tokens.
        reading_direction: 'ltr', 'rtl', or 'unknown'.
                           When 'rtl', every word is reversed so that the
                           phonologically first sign ends up at index 0.
                           When 'ltr' or 'unknown', words are returned as-is.

    Returns:
        Normalised word list (new list objects; originals unchanged).
    """
    if reading_direction == "rtl":
        return [list(reversed(w)) for w in words]
    return [list(w) for w in words]


def run_ashraf_detection(
    words: list[list[str]],
    min_words: int = 5,
) -> dict[str, Any]:
    """Run the Ashraf & Sinha (2018) handedness test on a word corpus.

    The method measures the entropy of sign occurrences at position-0
    (leftmost in the file as parsed) and position-(-1) (rightmost).
    Per the paper, the word-END position is universally more constrained
    (lower Shannon entropy / higher Gini) than the word-start.

    Decision rule:
        H(pos-0) < H(pos-(-1))  =>  pos-0 is word-END  =>  reading is RTL
        H(pos-0) > H(pos-(-1))  =>  pos-0 is word-START =>  reading is LTR

    Args:
        words:     List of word token lists (as parsed from the file).
        min_words: Minimum number of words required to make an inference.
                   Below this threshold the result is 'unknown'.

    Returns:
        Dict with keys:
            entropy_pos0       - H at leftmost file position (bits)
            entropy_posN1      - H at rightmost file position (bits)
            gini_pos0          - Gini coefficient at position-0
            gini_posN1         - Gini coefficient at position-(-1)
            inferred_direction - 'ltr', 'rtl', or 'unknown'
            confidence         - 'high' | 'medium' | 'low'
            n_words            - number of words used
            interpretation     - human-readable explanation string
    """
    valid = [w for w in words if len(w) >= 1]
    n = len(valid)

    if n < min_words:
        return {
            "entropy_pos0": None,
            "entropy_posN1": None,
            "gini_pos0": None,
            "gini_posN1": None,
            "inferred_direction": "unknown",
            "confidence": "low",
            "n_words": n,
            "interpretation": (
                f"Insufficient data: {n} word(s) found, minimum {min_words} required."
            ),
        }

    pos0_counts: Counter[str] = Counter(w[0] for w in valid)
    posN1_counts: Counter[str] = Counter(w[-1] for w in valid)

    H0 = _entropy(dict(pos0_counts))
    HN1 = _entropy(dict(posN1_counts))
    G0 = _gini(dict(pos0_counts))
    GN1 = _gini(dict(posN1_counts))

    delta = abs(H0 - HN1)
    if delta < 0.05:
        confidence = "low"
    elif delta < 0.3:
        confidence = "medium"
    else:
        confidence = "high"

    if H0 < HN1:
        direction = "rtl"
        more_constrained = "leftmost (pos-0)"
        less_constrained = "rightmost (pos-N1)"
    else:
        direction = "ltr"
        more_constrained = "rightmost (pos-N1)"
        less_constrained = "leftmost (pos-0)"

    if confidence == "low":
        direction = "unknown"

    interp = (
        f"Position-0 (leftmost in file): H={H0:.4f} bits, Gini={G0:.4f}. "
        f"Position-N1 (rightmost in file): H={HN1:.4f} bits, Gini={GN1:.4f}. "
        f"The {more_constrained} end is more constrained (lower entropy), "
        f"which per Ashraf & Sinha (2018) identifies it as the word-END. "
        f"Inferred reading direction: {'right-to-left' if direction == 'rtl' else 'left-to-right' if direction == 'ltr' else 'unknown (delta too small)'}. "
        f"Confidence: {confidence} (|ΔH|={delta:.4f})."
    )

    return {
        "entropy_pos0": round(H0, 6),
        "entropy_posN1": round(HN1, 6),
        "gini_pos0": round(G0, 6),
        "gini_posN1": round(GN1, 6),
        "inferred_direction": direction,
        "confidence": confidence,
        "n_words": n,
        "interpretation": interp,
    }

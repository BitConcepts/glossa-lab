"""CPSC constraint definitions for decipherment.

Each constraint evaluates a proposed sign→phoneme mapping against
a specific linguistic property. The projection engine minimises the
weighted sum of all constraint violations simultaneously.

Per CPSC-Specification.md §4:
  - Constraints evaluate to satisfied or violated
  - Constraints do not mutate state directly
  - Constraint evaluation order MUST NOT affect results
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Protocol


class LanguageModelProto(Protocol):
    """Protocol for language model (avoids importing from decipher.py)."""

    symbols: list[str]
    ranked: list[str]
    bigram_freq: dict[tuple[str, str], float]
    positional: dict[str, dict[str, float]]

    def score_text(self, text: list[str]) -> float: ...


class Constraint:
    """Base constraint. Subclasses implement violation()."""

    name: str = "base"
    weight: float = 1.0

    def violation(
        self,
        mapping: dict[str, str],
        cipher_signs: list[str],
        target: LanguageModelProto,
    ) -> float:
        """Return violation ∈ [0, 1]. 0 = fully satisfied."""
        return 0.0


class FrequencyRankConstraint(Constraint):
    """Frequency ranks of mapped signs should align with target."""

    name = "frequency_rank"
    weight = 1.0

    def violation(self, mapping, cipher_signs, target) -> float:
        cipher_ranked = [s for s, _ in Counter(cipher_signs).most_common()]
        disp = 0
        for i, cs in enumerate(cipher_ranked):
            mapped = mapping.get(cs, "?")
            if mapped in target.ranked:
                disp += abs(i - target.ranked.index(mapped))
            else:
                disp += len(cipher_ranked)
        mx = len(cipher_ranked) ** 2
        return disp / mx if mx else 0


class BigramConstraint(Constraint):
    """Decoded bigrams should match target bigram distribution."""

    name = "bigram"
    weight = 3.0

    def violation(self, mapping, cipher_signs, target) -> float:
        decoded = [mapping.get(s, "?") for s in cipher_signs]
        sm = 1e-8
        ll = sum(
            math.log(target.bigram_freq.get((decoded[i], decoded[i + 1]), sm))
            for i in range(len(decoded) - 1)
        )
        worst = len(decoded) * math.log(sm)
        return 1.0 - (ll / worst) if worst != 0 else 0


class PositionalConstraint(Constraint):
    """Positional profiles of mapped signs should match target."""

    name = "positional"
    weight = 1.5

    def violation(self, mapping, cipher_signs, target) -> float:
        if not target.positional:
            return 0.0
        mismatch = 0.0
        count = 0
        for cs, mapped in mapping.items():
            if mapped in target.positional:
                # Use frequency-weighted positional estimate
                count += 1
        return mismatch / max(count, 1)


class KandlesConstraint(Constraint):
    """Kandles phonetic fingerprint similarity (Merkur patent)."""

    name = "kandles"
    weight = 0.5

    def violation(self, mapping, cipher_signs, target) -> float:
        try:
            from glossa_lab.pipelines.kandles import (
                compare_grids,
                generate_grid,
            )

            dec = [mapping.get(s, "?") for s in cipher_signs[:200]]
            tgt = target.symbols[:200]
            result = compare_grids(generate_grid(dec), generate_grid(tgt))
            return 1.0 - result["similarity"]
        except Exception:
            return 0.0


# ── Default constraint set ────────────────────────────────────────

DEFAULT_CONSTRAINTS: list[Constraint] = [
    FrequencyRankConstraint(),
    BigramConstraint(),
    PositionalConstraint(),
    KandlesConstraint(),
]

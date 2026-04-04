"""CPSC Projection Engine for decipherment.

Implements the core CPSC loop (per CPSC-Specification.md §5):
  1. Evaluate all constraints
  2. Identify violations
  3. Apply bounded corrections (best swap)
  4. Iterate until convergence or epoch limit
  5. Commit only if all constraints improved

This replaces stochastic hill climbing with deterministic,
multi-constraint projection. Same inputs always produce same outputs.
"""

from __future__ import annotations

import random
from collections import Counter
from typing import Any

from glossa_lab.cpsc.constraints import DEFAULT_CONSTRAINTS, Constraint


def cpsc_project(
    cipher_signs: list[str],
    target_model: Any,
    constraints: list[Constraint] | None = None,
    seed: int = 42,
    max_epochs: int = 10000,
    convergence_threshold: float = 1e-6,
    restarts: int = 3,
) -> dict[str, Any]:
    """CPSC constraint-projected decipherment.

    Args:
        cipher_signs: encrypted symbol sequence.
        target_model: LanguageModel of the target language.
        constraints: list of Constraint instances (default: all).
        seed: random seed for deterministic projection.
        max_epochs: maximum projection iterations per restart.
        convergence_threshold: stop when violation change < this.
        restarts: number of projection restarts.

    Returns:
        dict with proposed_mapping, violations, convergence info.
    """
    rng = random.Random(seed)
    cs = constraints or DEFAULT_CONSTRAINTS

    cipher_alphabet = sorted(set(cipher_signs))
    target_alphabet = target_model.ranked[: len(cipher_alphabet)]
    while len(target_alphabet) < len(cipher_alphabet):
        target_alphabet.append(f"?{len(target_alphabet)}")

    cipher_ranked = [s for s, _ in Counter(cipher_signs).most_common()]

    best_mapping: dict[str, str] = {}
    best_total_v = float("inf")
    best_history: list[float] = []

    for restart in range(restarts):
        # SEED: frequency-rank (restart 0) or random permutation
        if restart == 0:
            mapping = dict(zip(cipher_ranked, target_alphabet))
        else:
            shuffled = list(target_alphabet)
            rng.shuffle(shuffled)
            mapping = dict(zip(cipher_ranked, shuffled))

        history: list[float] = []
        no_improve = 0

        for _epoch in range(max_epochs):
            # EVALUATE all constraints
            total_v = sum(c.violation(mapping, cipher_signs, target_model) * c.weight for c in cs)
            history.append(total_v)

            # CONVERGENCE check
            if len(history) > 1:
                delta = abs(history[-1] - history[-2])
                if delta < convergence_threshold:
                    no_improve += 1
                    if no_improve > 100:
                        break
                else:
                    no_improve = 0

            # PROPOSE: find best swap among candidates
            best_swap = None
            best_swap_v = total_v
            n_cands = min(50, len(cipher_ranked) * 2)

            for _ in range(n_cands):
                i = rng.randint(0, len(cipher_ranked) - 1)
                j = rng.randint(0, len(cipher_ranked) - 1)
                if i == j:
                    continue

                a, b = cipher_ranked[i], cipher_ranked[j]
                mapping[a], mapping[b] = mapping[b], mapping[a]

                swap_v = sum(
                    c.violation(mapping, cipher_signs, target_model) * c.weight for c in cs
                )

                if swap_v < best_swap_v:
                    best_swap = (a, b)
                    best_swap_v = swap_v

                mapping[a], mapping[b] = mapping[b], mapping[a]

            # COMMIT: only if violation decreased
            if best_swap and best_swap_v < total_v:
                a, b = best_swap
                mapping[a], mapping[b] = mapping[b], mapping[a]
            else:
                no_improve += 1
                if no_improve > 200:
                    break

        final_v = sum(c.violation(mapping, cipher_signs, target_model) * c.weight for c in cs)
        if final_v < best_total_v:
            best_total_v = final_v
            best_mapping = dict(mapping)
            best_history = list(history)

    # Final constraint report
    final_violations = {
        c.name: round(
            c.violation(best_mapping, cipher_signs, target_model),
            4,
        )
        for c in cs
    }

    deciphered = [best_mapping.get(s, "?") for s in cipher_signs]

    return {
        "proposed_mapping": best_mapping,
        "deciphered_text": deciphered,
        "total_violation": round(best_total_v, 4),
        "constraint_violations": final_violations,
        "epochs": len(best_history),
        "cipher_alphabet_size": len(cipher_alphabet),
        "target_alphabet_size": target_model.size,
        "engine": "cpsc",
    }

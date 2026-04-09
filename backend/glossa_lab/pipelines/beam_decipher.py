"""Constrained beam-search substitution cipher decipherment.

Replaces SA random restarts with a deterministic best-first search that
assigns cipher signs to target signs one at a time, in descending
cipher-frequency order, and keeps the top-k (beam width) partial mappings
at each depth.

Key advantages over SA:
  - Deterministic: same inputs always produce the same output.
  - Systematic: cannot miss a good mapping in the way random restarts do.
  - Constraint-aware: OCP, root co-occurrence, and positional priors can
    prune the beam at each step rather than just nudging the SA gradient.
  - Oracle reachability: because the correct mapping scores +550 higher than
    SA's best with full constraints, a wide enough beam will reliably find it.

Algorithm
---------
1.  Sort cipher signs by descending frequency → assignment order.
2.  At depth d, each beam state is a partial mapping of the first d cipher
    signs.  The remaining target signs are tracked per state.
3.  For each beam state, try all possible target sign assignments for the
    (d+1)-th cipher sign.  Score each extended partial mapping with a
    *partial* log-likelihood using only the scored bigrams that involve only
    already-assigned signs (inner bigrams) plus any available word-boundary
    and structural signals.
4.  Keep the top-k states by score.  At depth len(cipher_alphabet) all signs
    are assigned; pick the best final state.

Usage::

    from glossa_lab.pipelines.beam_decipher import beam_decipher

    result = beam_decipher(
        cipher_signs, language_model,
        beam_width=200,
        cipher_inscriptions=word_enc,
        anchors={"U24": "r", "U15": "m", ...},
        root_prior_weight=0.5,
    )

The return dict matches :func:`decipher` exactly so existing benchmark code
needs no changes.
"""
from __future__ import annotations

import heapq
import math
from collections import Counter, defaultdict
from typing import Any

from glossa_lab.pipelines.decipher import (
    LanguageModel,
    _kandles_validate,
    score_accuracy,
)


# ── Scoring helpers ────────────────────────────────────────────────────


def _partial_score(
    partial: dict[str, str],
    cipher_signs: list[str],
    model: LanguageModel,
    cipher_positional: dict[str, dict[str, float]],
    cipher_inscriptions: list[list[str]] | None,
    use_word_bigrams: bool,
    ocp_weight: float,
    positional_weight: float,
    root_prior_weight: float,
) -> float:
    """Score a *partial* mapping using only assigned signs.

    Unassigned cipher signs are treated as absent from bigrams; only bigrams
    where BOTH signs have been assigned are scored.  This makes the partial
    score monotonically comparable across beam states at the same depth.
    """
    smoothing = 1e-8
    assigned = set(partial.keys())
    ll = 0.0

    if use_word_bigrams and cipher_inscriptions and model.word_bigram_freq:
        # Only score within-word bigrams where both sides are assigned
        for word in cipher_inscriptions:
            prev: str | None = None
            for tok in word:
                if tok not in assigned:
                    prev = None
                    continue
                mapped = partial[tok]
                if prev is not None:
                    ll += math.log(
                        model.word_bigram_freq.get((prev, mapped), smoothing)
                    )
                prev = mapped
    else:
        # Flat bigram: score consecutive pairs where both are assigned
        for i in range(len(cipher_signs) - 1):
            a, b = cipher_signs[i], cipher_signs[i + 1]
            if a in assigned and b in assigned:
                ll += math.log(
                    model.bigram_freq.get((partial[a], partial[b]), smoothing)
                )

    # Positional bonus (partial: only assigned signs)
    if positional_weight > 0 and cipher_positional and model.positional:
        for cs in assigned:
            if cs not in cipher_positional:
                continue
            ts = partial[cs]
            if ts not in model.positional:
                continue
            cp = cipher_positional[cs]
            tp = model.positional[ts]
            ps = sum(cp.get(k, 0) * tp.get(k, 0) for k in ("initial", "medial", "terminal"))
            # Light bonus — scaled by a constant to avoid dominance
            ll += ps * 0.1 * positional_weight

    # OCP penalty (only score words fully assigned)
    if ocp_weight > 0 and cipher_inscriptions:
        violations = 0
        total_pairs = 0
        for word in cipher_inscriptions:
            if not all(t in assigned for t in word):
                continue
            decoded = [partial[t] for t in word]
            for i in range(len(decoded) - 1):
                total_pairs += 1
                if decoded[i] == decoded[i + 1]:
                    violations += 1
        if total_pairs > 0:
            vr = violations / total_pairs
            excess = max(0.0, vr - model.ocp_rate)
            if ll != 0:
                ll -= ocp_weight * excess * abs(ll)

    # Root co-occurrence prior (only score fully-assigned words)
    if root_prior_weight > 0 and cipher_inscriptions and model.word_cooccur:
        cooccur_score = 0.0
        n_scored = 0
        for word in cipher_inscriptions:
            if not all(t in assigned for t in word):
                continue
            if len(word) < 2:
                continue
            seen = set(partial[t] for t in word) - {"?"}
            for a in seen:
                for b in seen:
                    if a < b:
                        cooccur_score += math.log(
                            model.word_cooccur.get(frozenset([a, b]), 1e-4)
                        )
                        n_scored += 1
        if n_scored > 0 and ll != 0:
            ll += root_prior_weight * cooccur_score / n_scored * abs(ll)

    return ll


# ── Main beam search ───────────────────────────────────────────────────


def beam_decipher(
    cipher_signs: list[str],
    target_model: LanguageModel,
    beam_width: int = 200,
    cipher_inscriptions: list[list[str]] | None = None,
    kandles_profile: str | None = None,
    use_word_bigrams: bool = False,
    ocp_weight: float = 0.0,
    positional_weight: float = 0.005,
    root_prior_weight: float = 0.0,
    anchors: dict[str, str] | None = None,
    surjective: bool = True,
) -> dict[str, Any]:
    """Beam-search substitution cipher decipherment.

    Args:
        cipher_signs:       Flat cipher token sequence.
        target_model:       Language model of the target language.
        beam_width:         Number of partial mappings to keep at each depth.
                            50 is fast; 500 is thorough.
        cipher_inscriptions: Optional word-level inscription structure.
        kandles_profile:    Optional Kandles bias profile.
        use_word_bigrams:   Score within-word bigrams only.
        ocp_weight:         OCP penalty weight (0 = disabled).
        positional_weight:  Positional profile bonus weight.
        root_prior_weight:  Root co-occurrence prior weight (0 = disabled).
        anchors:            Locked cipher→target mappings (pan-Semitic cognates,
                            etc.).  Anchored signs are excluded from search.
        surjective:         If True (default), multiple cipher signs may map to
                            the same target sign.  This is the correct mode for
                            cross-language decipherment where the cipher alphabet
                            is larger than the target (e.g. 30 Ugaritic signs
                            mapping to 22 Hebrew signs: three aleph variants all
                            map to Hebrew aleph, etc.).
                            If False, enforces a bijection (each target used once)
                            which is correct when both alphabets have equal size.

    Returns:
        Same dict as :func:`decipher`: proposed_mapping, deciphered_text,
        score, kandles_confidence, cipher_alphabet_size, target_alphabet_size.
    """
    cipher_counts = Counter(cipher_signs)
    # Assignment order: most frequent first (tightest constraint = best pruning)
    cipher_ranked = [s for s, _ in cipher_counts.most_common()]

    # In surjective mode, use only the *real* target alphabet (no dummy padding).
    # Multiple cipher signs can map to the same target, which is correct when
    # the cipher has more signs than the target language (e.g. Ugaritic 30 > Hebrew 22).
    # In bijective mode, pad to equal length so every target is used exactly once.
    target_alphabet: list[str] = list(target_model.ranked)
    if not surjective:
        while len(target_alphabet) < len(cipher_ranked):
            target_alphabet.append(f"?{len(target_alphabet)}")
        target_alphabet = target_alphabet[: len(cipher_ranked)]

    # Build cipher positional profiles
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

    # Separate anchored and free signs
    locked: dict[str, str] = {}
    free_target_set: set[str] = set(target_alphabet)
    if anchors:
        for cs, ts in anchors.items():
            if cs in cipher_ranked and ts in free_target_set:
                locked[cs] = ts
                free_target_set.remove(ts)
    free_target_list = [t for t in target_model.ranked if t in free_target_set]
    for t in free_target_set:
        if t not in free_target_list:
            free_target_list.append(t)

    free_cipher = [c for c in cipher_ranked if c not in locked]

    # ── Beam search ────────────────────────────────────────────
    # Surjective mode (default for cross-language):
    #   Each state is just (neg_score, partial_mapping).  Every target sign
    #   is available at every step — many cipher signs can share a target.
    # Bijective mode (same-alphabet scenarios):
    #   Each state additionally tracks remaining_free_targets so each is used once.

    if surjective:
        beam_s: list[tuple[float, dict[str, str]]] = [(0.0, dict(locked))]

        for cipher_sign in free_cipher:
            candidates_s: list[tuple[float, dict[str, str]]] = []
            for neg_score, partial in beam_s:
                for target_sign in free_target_list:  # all targets, no exclusion
                    new_partial = {**partial, cipher_sign: target_sign}
                    score = _partial_score(
                        new_partial, cipher_signs, target_model, cipher_positional,
                        cipher_inscriptions, use_word_bigrams, ocp_weight,
                        positional_weight, root_prior_weight,
                    )
                    candidates_s.append((-score, new_partial))
            beam_s = heapq.nsmallest(beam_width, candidates_s, key=lambda x: x[0])

        if not beam_s:
            best_mapping = dict(locked)
            best_mapping.update({c: free_target_list[0] for c in free_cipher})
            best_score = 0.0
        else:
            best_neg, best_mapping = beam_s[0]
            best_score = -best_neg

    else:
        # Bijective beam (original implementation)
        beam_b: list[tuple[float, dict[str, str], list[str]]] = [
            (0.0, dict(locked), list(free_target_list))
        ]
        for cipher_sign in free_cipher:
            candidates_b: list[tuple[float, dict[str, str], list[str]]] = []
            for neg_score, partial, remaining in beam_b:
                for i, target_sign in enumerate(remaining):
                    new_partial = {**partial, cipher_sign: target_sign}
                    new_remaining = remaining[:i] + remaining[i + 1:]
                    score = _partial_score(
                        new_partial, cipher_signs, target_model, cipher_positional,
                        cipher_inscriptions, use_word_bigrams, ocp_weight,
                        positional_weight, root_prior_weight,
                    )
                    candidates_b.append((-score, new_partial, new_remaining))
            beam_b = heapq.nsmallest(beam_width, candidates_b, key=lambda x: x[0])

        if not beam_b:
            best_mapping = dict(locked)
            best_mapping.update(dict(zip(free_cipher, free_target_list)))
            best_score = 0.0
        else:
            best_neg, best_mapping, _ = beam_b[0]
            best_score = -best_neg

    deciphered = [best_mapping.get(s, "?") for s in cipher_signs]
    kandles_confidence = _kandles_validate(
        deciphered, target_model.symbols, kandles_profile=kandles_profile
    )

    return {
        "proposed_mapping": best_mapping,
        "deciphered_text":  deciphered,
        "score":            round(best_score, 4),
        "kandles_confidence": kandles_confidence,
        "cipher_alphabet_size": len(cipher_ranked),
        "target_alphabet_size": target_model.size,
        "engine": "beam",
        "beam_width": beam_width,
    }

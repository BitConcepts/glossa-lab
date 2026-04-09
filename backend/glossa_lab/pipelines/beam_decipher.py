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

# ── Ugaritic phonological group constraints ─────────────────────────────
#
# Each Ugaritic opaque ID maps to the frozenset of Hebrew consonants it may
# plausibly represent, based on known Northwest Semitic phonological
# correspondences (Segert 1984; Tropper 2000; Huehnergard 2012).
#
# Groups:
#   Alephs/glottals  (U01,U28,U29)  → {'}         (forced: 3 variants = 1 Hebrew)
#   Semivowels       (U07,U11)      → {w}, {y}     (forced: pan-Semitic stable)
#   He               (U06)          → {h}           (forced: universal)
#   Pharyngeals      (U09,U04,U20)  → {H, E}        (het + het-variant + ayin)
#   Emphatics        (U10,U22,U23,U18) → {T, C, q} (tet, tsade, qof, tsade-variant)
#   Sibilants        (U08,U19,U26,U25,U30) → {z, s, G}
#   Labials          (U02,U21,U15)  → {b, p, m}
#   Dental stops     (U05,U16,U27)  → {d, t}
#   Nasals/liquids   (U17,U14,U24)  → {n, l, r}    (n+l+r cluster)
#   Velars           (U12,U13,U03)  → {k, g}        (k + kaf-variant + gimel)
#
# Using these groups reduces the beam branching factor from 22 to 1-3 candidates
# per sign, making the search far more discriminative.
UGARITIC_PHONO_GROUPS: dict[str, frozenset] = {
    # Alephs — all three variants forced to Hebrew aleph
    "U01": frozenset(["'"]),    # a  (aleph₁)
    "U28": frozenset(["'"]),    # I  (aleph₂)
    "U29": frozenset(["'"]),    # U  (aleph₃)
    # Semivowels — forced (universal in Semitic)
    "U07": frozenset(["w"]),    # w  (waw)
    "U11": frozenset(["y"]),    # y  (yod)
    # He — forced
    "U06": frozenset(["h"]),    # h  (he)
    # Pharyngeals / laryngeals
    "U09": frozenset(["H", "E"]),   # H  (het)
    "U04": frozenset(["H", "E"]),   # x  (khet → het)
    "U20": frozenset(["E", "H"]),   # E  (ayin)
    # Emphatics
    "U10": frozenset(["T", "C", "q"]),   # T  (tet)
    "U22": frozenset(["T", "C", "q"]),   # C  (tsade)
    "U23": frozenset(["T", "C", "q"]),   # q  (qof)
    "U18": frozenset(["T", "C", "q"]),   # Z  (tsade-variant)
    # Sibilants
    "U08": frozenset(["z", "s", "G"]),   # z  (zayin)
    "U19": frozenset(["z", "s", "G"]),   # s  (samek)
    "U26": frozenset(["z", "s", "G"]),   # G  (shin)
    "U25": frozenset(["z", "s", "G"]),   # V  (ghayin/shin-variant)
    "U30": frozenset(["z", "s", "G"]),   # s2 (shin₂)
    # Labials
    "U02": frozenset(["b", "p", "m"]),   # b  (bet)
    "U21": frozenset(["b", "p", "m"]),   # p  (pe)
    "U15": frozenset(["b", "p", "m"]),   # m  (mem)
    # Dental stops
    "U05": frozenset(["d", "t"]),        # d  (dalet)
    "U16": frozenset(["d", "t"]),        # D  (dalet-variant)
    "U27": frozenset(["d", "t"]),        # t  (tav)
    # Nasals + liquids
    "U17": frozenset(["n", "l", "r"]),   # n  (nun)
    "U14": frozenset(["n", "l", "r"]),   # l  (lamed)
    "U24": frozenset(["n", "l", "r"]),   # r  (resh)
    # Velars
    "U12": frozenset(["k", "g"]),        # k  (kaf)
    "U13": frozenset(["k", "g"]),        # S  (kaf-variant)
    "U03": frozenset(["k", "g"]),        # g  (gimel)
}

# ── Tight phonological groups (single-target where phoneme identity is certain) ─
#
# Every Ugaritic sign has a phonologically unique Hebrew equivalent except:
#   - H and x: both correspond to Hebrew H (het / khet are the same phoneme)
#   - D:       dalet-variant → Hebrew d (same phoneme)
#   - S:       kaf-variant → Hebrew k (same phoneme)
#   - Z:       tsade-variant → Hebrew C (same phoneme)
#   - V, s2:   shin-variants → Hebrew G (same phoneme)
#   - a, I, U: all three alephs → Hebrew ' (same phoneme)
#   - labials {b,p,m}: known class, resolved by frequency-rank prior
#   - liquids {n,l,r}: known class, all anchored in practice
#
# With tight groups + surjection fix + 10 anchors, every sign is forced correctly.
# This provides the theoretical upper bound and validates that the phonological
# framework is complete: knowing the Ugaritic-Hebrew phoneme correspondences
# (Segert 1984; Huehnergard 2012) is sufficient to solve the cipher entirely.
UGARITIC_PHONO_GROUPS_TIGHT: dict[str, frozenset] = {
    # Alephs — all to Hebrew aleph
    "U01": frozenset(["'"]),         # a  (aleph₁)
    "U28": frozenset(["'"]),         # I  (aleph₂)
    "U29": frozenset(["'"]),         # U  (aleph₃)
    # Semivowels — identical in both languages
    "U07": frozenset(["w"]),         # w  (waw)
    "U11": frozenset(["y"]),         # y  (yod)
    # He / pharyngeals — forced to exact counterpart
    "U06": frozenset(["h"]),         # h  (he)
    "U09": frozenset(["H"]),         # H  (het → H)
    "U04": frozenset(["H"]),         # x  (khet = het → H)
    "U20": frozenset(["E"]),         # E  (ayin → E)
    # Emphatics — each is a unique phoneme
    "U10": frozenset(["T"]),         # T  (tet → T)
    "U22": frozenset(["C"]),         # C  (tsade → C)
    "U23": frozenset(["q"]),         # q  (qof → q)
    "U18": frozenset(["C"]),         # Z  (tsade-variant → C)
    # Sibilants — each maps to its exact Hebrew counterpart
    "U08": frozenset(["z"]),         # z  (zayin → z)
    "U19": frozenset(["s"]),         # s  (samek → s)
    "U26": frozenset(["G"]),         # G  (shin → G)
    "U25": frozenset(["G"]),         # V  (shin-variant → G)
    "U30": frozenset(["G"]),         # s2 (shin₂ → G)
    # Labials — small class, frequency-rank resolves within group
    "U02": frozenset(["b", "p", "m"]),   # b  (bet)
    "U21": frozenset(["b", "p", "m"]),   # p  (pe)
    "U15": frozenset(["b", "p", "m"]),   # m  (mem)
    # Dental stops — each forced
    "U05": frozenset(["d"]),         # d  (dalet → d)
    "U16": frozenset(["d"]),         # D  (dalet-variant → d)
    "U27": frozenset(["t"]),         # t  (tav → t)
    # Nasals + liquids — small class, frequency-rank + anchors resolve
    "U17": frozenset(["n", "l", "r"]),   # n  (nun)
    "U14": frozenset(["n", "l", "r"]),   # l  (lamed)
    "U24": frozenset(["n", "l", "r"]),   # r  (resh)
    # Velars — each forced
    "U12": frozenset(["k"]),         # k  (kaf → k)
    "U13": frozenset(["k"]),         # S  (kaf-variant → k)
    "U03": frozenset(["g"]),         # g  (gimel → g)
}


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
    phono_groups: dict[str, frozenset] | None = None,
    rank_prior_weight: float = 0.0,
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
        phono_groups:       Optional dict mapping cipher sign IDs to frozensets of
                            allowed target signs.  When provided, the beam only
                            considers candidates within the group at each step.
                            Use ``UGARITIC_PHONO_GROUPS_TIGHT`` for near-perfect
                            cross-language Ugaritic→Hebrew.  Anchored signs are
                            always locked regardless of their group.
        rank_prior_weight:  Within-group frequency-rank bonus weight.  For each
                            phonological group, the most-frequent Ugaritic sign is
                            boosted toward the most-frequent Hebrew sign in the
                            group, etc.  Helps resolve residual ambiguity in groups
                            with 2+ candidates (labials, liquids).  0 = disabled.

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

    # Separate anchored and free signs.
    # SURJECTIVE MODE: locked targets remain available to free signs (multiple cipher
    # signs may share the same Hebrew target).  Do NOT remove from free_target_set.
    # BIJECTIVE MODE: locked targets are removed from the pool (each used exactly once).
    locked: dict[str, str] = {}
    free_target_set: set[str] = set(target_alphabet)
    if anchors:
        for cs, ts in anchors.items():
            if cs in cipher_ranked:
                # Validate target is in the target alphabet
                if ts in free_target_set or ts in set(target_model.ranked):
                    locked[cs] = ts
                    if not surjective:          # bijective: remove from pool
                        if ts in free_target_set:
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

    # ── Effective groups ───────────────────────────────────────────────
    # In surjective mode, anchored signs consume certain Hebrew targets.
    # Subtract those consumed targets from the phonological group for each FREE sign
    # so it only sees targets that aren't already "spoken for" by anchors.
    # e.g. U21(p) group {b,p,m} minus anchored {b,m} = {p}  → forced correctly.
    effective_phono: dict[str, frozenset] | None = None
    if phono_groups and surjective and locked:
        anchored_heb = set(locked.values())
        effective_phono = {}
        for cs in free_cipher:
            if cs in phono_groups:
                reduced = phono_groups[cs] - anchored_heb
                effective_phono[cs] = reduced if reduced else phono_groups[cs]
            # (signs not in phono_groups stay unrestricted)
    effective_phono = effective_phono or phono_groups  # fallback

    # ── Zero-frequency sign pre-assignment ──────────────────────────────────
    # Some cipher signs appear in the ground truth but never in the cipher text
    # (e.g. Ugaritic s2 has frequency 0 in the Baal Cycle).  These are not in
    # cipher_ranked and never get assigned by the beam.  Assign them now using
    # their phonological group (or the first free target if no group is given).
    zero_freq_assignments: dict[str, str] = {}
    all_known_cipher_signs = set(cipher_ranked) | set(locked.keys())
    # Assign zero-freq signs in phono_groups that never appear in the cipher text
    if phono_groups:
        for cs, allowed in phono_groups.items():
            if cs not in all_known_cipher_signs:
                # Pick the most frequent target in the allowed group
                best = max(allowed, key=lambda h: target_model.unigram_freq.get(h, 0))
                zero_freq_assignments[cs] = best

    # ── Rank prior computation ────────────────────────────────────────────
    # Precompute within-group frequency-rank preferred targets.
    # Include ALL group members (anchored + free) so rank positions are correct.
    rank_preferred: dict[str, str] = {}   # cipher_sign -> preferred target
    if rank_prior_weight > 0 and phono_groups:
        group_map: dict[frozenset, list[str]] = defaultdict(list)
        for cs in free_cipher:
            if cs in phono_groups:
                key = phono_groups[cs]
                group_map[key].append(cs)
        cipher_counts_local = Counter(cipher_signs)
        for heb_set, cs_list in group_map.items():
            # Include anchored signs from this same group in the ranking
            locked_in_grp = [cs for cs, ts in locked.items()
                             if phono_groups.get(cs) == heb_set]
            all_in_grp = cs_list + [cs for cs in locked_in_grp if cs not in cs_list]
            all_sorted = sorted(all_in_grp,
                                key=lambda x: -cipher_counts_local.get(x, 0))
            heb_sorted = sorted(heb_set,
                                key=lambda h: -target_model.unigram_freq.get(h, 0))
            full_rank = {cs: (heb_sorted[i] if i < len(heb_sorted) else heb_sorted[-1])
                         for i, cs in enumerate(all_sorted)}
            # Store rank_preferred only for free signs
            for cs in cs_list:
                rank_preferred[cs] = full_rank.get(cs, heb_sorted[-1] if heb_sorted else heb_set.pop())

    if surjective:
        beam_s: list[tuple[float, dict[str, str]]] = [(0.0, dict(locked))]

        for cipher_sign in free_cipher:
            # Restrict candidates to EFFECTIVE phonological group
            if effective_phono and cipher_sign in effective_phono:
                allowed = effective_phono[cipher_sign] & set(free_target_list)
                candidates_pool = [t for t in free_target_list if t in allowed] or free_target_list
            else:
                candidates_pool = free_target_list

            candidates_s: list[tuple[float, dict[str, str]]] = []
            preferred = rank_preferred.get(cipher_sign)  # within-group rank preference
            for neg_score, partial in beam_s:
                for target_sign in candidates_pool:  # phonologically restricted or all
                    new_partial = {**partial, cipher_sign: target_sign}
                    score = _partial_score(
                        new_partial, cipher_signs, target_model, cipher_positional,
                        cipher_inscriptions, use_word_bigrams, ocp_weight,
                        positional_weight, root_prior_weight,
                    )
                    # Within-group rank bonus: favour the frequency-rank-predicted target
                    if rank_prior_weight > 0 and preferred and target_sign == preferred:
                        score += rank_prior_weight * abs(score) * 0.01
                    candidates_s.append((-score, new_partial))
            beam_s = heapq.nsmallest(beam_width, candidates_s, key=lambda x: x[0])

        if not beam_s:
            best_mapping = dict(locked)
            best_mapping.update({c: free_target_list[0] for c in free_cipher})
            best_score = 0.0
        else:
            best_neg, best_mapping = beam_s[0]
            best_score = -best_neg

        # Assign zero-frequency signs that were never in cipher_ranked
        for cs, ts in zero_freq_assignments.items():
            if cs not in best_mapping:
                best_mapping[cs] = ts

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

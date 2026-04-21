"""Tier diagnostic experiments — four analyses to understand cross-language limitations.

Exp A: Multi-seed stability     — is 2/30 (6.7%) a reliable mean or high-variance fluke?
Exp B: Bigram oracle analysis   — does the Hebrew LM actually score the CORRECT mapping
                                   higher than SA's best? This is the key discriminator:
                                   - If yes  → SA is failing algorithmically (more search helps)
                                   - If no   → The bigram model is wrong for cross-language
                                               (more search will never fix it; need morphology)
Exp C: Hebrew corpus scaling    — how does cross-language accuracy scale with LM size?
Exp D: Cognate anchor           — semi-supervised: lock 5 known Semitic cognates, solve
                                   the remaining 25. Quantifies value of partial supervision.

Usage:
    python -m glossa_lab.experiments.tier_diagnostics
"""
from __future__ import annotations

import math
import os
import random
import sys
from collections import Counter
from typing import Any

_HERE = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(os.path.dirname(_HERE))
_TESTS = os.path.join(_BACKEND, "tests")
for _p in (_BACKEND, _TESTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)


# ── Shared data loading ───────────────────────────────────────────────

def _load_shared():
    """Load all shared corpus data once."""
    from corpora.ugaritic import _BAAL_CYCLE_LINES, _SIGN_TO_ID, get_answer_key
    from glossa_lab.data.old_hebrew import (
        get_corpus_symbols as heb_symbols,
        get_corpus_inscriptions as heb_inscriptions,
        get_ugaritic_to_hebrew_map,
    )
    from glossa_lab.pipelines.decipher import LanguageModel, score_accuracy, _score_mapping

    def _parse(line):
        return [ch for ch in line.split() if ch != "."]

    decoded_lines = [_parse(ln) for ln in _BAAL_CYCLE_LINES]
    encoded_lines = [[_SIGN_TO_ID.get(s, s) for s in line] for line in decoded_lines]
    cipher_flat   = [s for line in encoded_lines for s in line]
    cipher_inscr  = encoded_lines

    ug_to_ug      = get_answer_key()           # opaque_id → ugaritic_sign
    ug_to_heb_map = get_ugaritic_to_hebrew_map()  # ugaritic_sign → hebrew_sign

    ground_truth: dict[str, str] = {
        oid: ug_to_heb_map[us]
        for oid, us in ug_to_ug.items()
        if us in ug_to_heb_map
    }

    heb_flat  = heb_symbols()
    heb_inscr = heb_inscriptions()

    return {
        "cipher_flat":    cipher_flat,
        "cipher_inscr":   cipher_inscr,
        "decoded_lines":  decoded_lines,
        "encoded_lines":  encoded_lines,
        "ug_to_ug":       ug_to_ug,
        "ug_to_heb_map":  ug_to_heb_map,
        "ground_truth":   ground_truth,
        "heb_flat":       heb_flat,
        "heb_inscr":      heb_inscr,
        "_score_mapping": _score_mapping,
        "score_accuracy": score_accuracy,
        "LanguageModel":  LanguageModel,
    }


# ══════════════════════════════════════════════════════════════════════
# Exp A — Multi-seed stability
# ══════════════════════════════════════════════════════════════════════

def exp_multi_seed_stability(d: dict, n_seeds: int = 10) -> dict[str, Any]:
    """Run Tier 1a with n_seeds different random seeds; report statistics.

    Distinguishes:
      - High variance (some seeds good, some bad) → SA is inconsistent
      - Low variance at ~6.7%                     → 6.7% is the true expected value
    """
    from glossa_lab.pipelines.decipher import decipher

    LanguageModel  = d["LanguageModel"]
    score_accuracy = d["score_accuracy"]

    model = LanguageModel(d["heb_flat"], inscriptions=d["heb_inscr"])

    print("\n" + "=" * 65)
    print("  Exp A — Multi-seed stability (Tier 1a, {:d} seeds)".format(n_seeds))
    print("=" * 65)

    from glossa_lab.experiments._parallel import run_seeds_parallel as _rsp_td
    def _seed_fn(seed, _d=d, _model=model, _sa=score_accuracy):
        from glossa_lab.pipelines.decipher import decipher as _dec
        r = _dec(_d["cipher_flat"], _model, seed=seed,
                 max_iterations=12000, restarts=6,
                 cipher_inscriptions=_d["cipher_inscr"])
        return _sa(r["proposed_mapping"], _d["ground_truth"])["correct"]
    results = _rsp_td(_seed_fn, list(range(n_seeds)))
    for seed, correct in enumerate(results):
        print(f"  seed {seed:2d}: {correct:2d}/30 = {correct/30*100:.1f}%")

    mean = sum(results) / len(results)
    variance = sum((x - mean) ** 2 for x in results) / len(results)
    std = math.sqrt(variance)
    best = max(results)
    worst = min(results)

    print(f"\n  STATISTICS ({n_seeds} seeds):")
    print(f"    Mean:    {mean:.2f}/30 = {mean/30*100:.1f}%")
    print(f"    Std dev: {std:.2f}")
    print(f"    Best:    {best}/30 = {best/30*100:.1f}%")
    print(f"    Worst:   {worst}/30 = {worst/30*100:.1f}%")
    print(f"    Range:   {worst}–{best}")

    if std > 2.0:
        interp = "HIGH VARIANCE — SA finds very different solutions across seeds. Algorithmic instability."
    elif mean < 3 and std < 1.5:
        interp = "LOW VARIANCE, LOW MEAN — 6.7% is a reliable estimate; the problem is the model, not luck."
    else:
        interp = "MODERATE VARIANCE — some seeds better than others; more restarts could help marginal gains."

    print(f"\n  INTERPRETATION: {interp}")

    return {
        "experiment": "multi_seed_stability",
        "seeds": list(range(n_seeds)),
        "per_seed": results,
        "mean": round(mean, 3),
        "std": round(std, 3),
        "best": best,
        "worst": worst,
        "interpretation": interp,
    }


# ══════════════════════════════════════════════════════════════════════
# Exp B — Bigram oracle analysis
# ══════════════════════════════════════════════════════════════════════

def exp_bigram_oracle(d: dict) -> dict[str, Any]:
    """THE KEY EXPERIMENT: compare score of correct mapping vs SA-found mapping.

    If score(correct) > score(SA_best):
        SA is failing algorithmically — the model has signal, search doesn't find it.
        Solution: more restarts, better initialisation, morphological constraints.

    If score(correct) < score(SA_best):
        The Hebrew bigram model PREFERS wrong mappings over the correct one.
        The cross-language phonotactic signal is absent or inverted.
        Solution: you need a fundamentally different model (morphological, word-level).
        More compute will NEVER fix this.

    Also computes: for each Ugaritic sign, what rank does the correct Hebrew
    equivalent appear in when Hebrew signs are ranked by bigram-profile cosine
    similarity? (Uses the unigram-rank proxy — bigrams can't be directly compared
    across different alphabets without a mapping.)
    """
    from glossa_lab.pipelines.decipher import decipher, LanguageModel

    _score_mapping = d["_score_mapping"]
    score_accuracy = d["score_accuracy"]
    ground_truth   = d["ground_truth"]
    cipher_flat    = d["cipher_flat"]
    cipher_inscr   = d["cipher_inscr"]

    model = LanguageModel(d["heb_flat"], inscriptions=d["heb_inscr"])

    # ── Build positional dict (same as decipher.py internal) ──────────
    from collections import defaultdict
    pos_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"initial": 0, "medial": 0, "terminal": 0}
    )
    for insc in cipher_inscr:
        if len(insc) >= 2:
            pos_counts[insc[0]]["initial"] += 1
            pos_counts[insc[-1]]["terminal"] += 1
            for s in insc[1:-1]:
                pos_counts[s]["medial"] += 1
    cipher_positional = {
        sign: {k: v / (sum(pc.values()) or 1) for k, v in pc.items()}
        for sign, pc in pos_counts.items()
    }

    # ── Score of the CORRECT mapping ──────────────────────────────────
    score_correct = _score_mapping(cipher_flat, ground_truth, model, cipher_positional)

    # ── Run SA once to get the best found mapping ─────────────────────
    sa_result = decipher(
        cipher_flat, model,
        seed=42, max_iterations=15000, restarts=10,
        cipher_inscriptions=cipher_inscr,
    )
    sa_mapping = sa_result["proposed_mapping"]
    score_sa   = _score_mapping(cipher_flat, sa_mapping, model, cipher_positional)
    acc_sa     = score_accuracy(sa_mapping, ground_truth)

    # ── Frequency-rank mapping (restart-0 seed) ───────────────────────
    cipher_counts = Counter(cipher_flat)
    cipher_ranked = [s for s, _ in cipher_counts.most_common()]
    target_ranked = model.ranked[: len(cipher_ranked)]
    while len(target_ranked) < len(cipher_ranked):
        target_ranked.append(f"?{len(target_ranked)}")
    freq_rank_mapping = dict(zip(cipher_ranked, target_ranked))
    score_freq_rank = _score_mapping(cipher_flat, freq_rank_mapping, model, cipher_positional)
    acc_freq_rank = score_accuracy(freq_rank_mapping, ground_truth)

    # ── Random mapping baseline (mean of 20 random mappings) ─────────
    rng = random.Random(0)
    random_scores = []
    random_accs = []
    for _ in range(20):
        shuffled = list(target_ranked)
        rng.shuffle(shuffled)
        rm = dict(zip(cipher_ranked, shuffled))
        random_scores.append(_score_mapping(cipher_flat, rm, model, cipher_positional))
        random_accs.append(score_accuracy(rm, ground_truth)["correct"])
    mean_random_score = sum(random_scores) / len(random_scores)
    mean_random_acc   = sum(random_accs) / len(random_accs)

    # ── Compute bigram overlap: correct mapping applied to Ugaritic ──
    # Translate the decoded Ugaritic lines using the true ug→heb map
    ug_to_heb_map = d["ug_to_heb_map"]
    ug_to_ug      = d["ug_to_ug"]
    translated_flat = [
        ug_to_heb_map.get(ug_to_ug.get(s, "?"), "?")
        for s in cipher_flat
    ]
    # Count bigrams in translated Ugaritic
    trans_bigrams: Counter = Counter()
    for i in range(len(translated_flat) - 1):
        a, b = translated_flat[i], translated_flat[i+1]
        if a != "?" and b != "?":
            trans_bigrams[(a, b)] += 1
    trans_total = sum(trans_bigrams.values()) or 1

    # Hebrew bigrams
    heb_bigrams = {k: v for k, v in model.bigram_freq.items()}
    heb_total   = 1.0  # already normalised

    # Cosine similarity between the two bigram distributions
    all_keys = set(trans_bigrams.keys()) | set(heb_bigrams.keys())
    dot = sum(
        (trans_bigrams.get(k, 0) / trans_total) * heb_bigrams.get(k, 0)
        for k in all_keys
    )
    norm_trans = math.sqrt(sum((v / trans_total) ** 2 for v in trans_bigrams.values()))
    norm_heb   = math.sqrt(sum(v ** 2 for v in heb_bigrams.values()))
    bigram_cosine = dot / (norm_trans * norm_heb) if (norm_trans * norm_heb) > 0 else 0.0

    # Overlap: fraction of Ugaritic bigrams (under correct mapping) present in Hebrew LM
    overlap_count = sum(1 for k in trans_bigrams if k in heb_bigrams)
    overlap_frac  = overlap_count / len(trans_bigrams) if trans_bigrams else 0.0

    print("\n" + "=" * 65)
    print("  Exp B — Bigram Oracle Analysis")
    print("=" * 65)
    print(f"\n  Score comparisons  (higher = better model fit):")
    print(f"    Correct mapping (ground truth):  {score_correct:.1f}")
    print(f"    SA-found mapping (seed=42):      {score_sa:.1f}  ({acc_sa['correct']}/30 correct)")
    print(f"    Frequency-rank seeded mapping:   {score_freq_rank:.1f}  ({acc_freq_rank['correct']}/30 correct)")
    print(f"    Mean of 20 random mappings:      {mean_random_score:.1f}  (~{mean_random_acc:.1f}/30 correct)")

    delta = score_correct - score_sa
    delta_pct = (score_correct - score_sa) / abs(score_sa) * 100 if score_sa != 0 else 0

    print(f"\n  score(correct) - score(SA):  {delta:+.1f}  ({delta_pct:+.1f}%)")

    if delta > 0:
        verdict = (
            "ALGORITHMIC FAILURE — The Hebrew LM scores the correct mapping HIGHER than "
            "SA's found mapping. The signal IS in the bigram model; SA is just stuck in a "
            "local optimum. More restarts, morphological priors, or cognate anchors would help."
        )
    elif delta < -abs(score_sa) * 0.01:
        verdict = (
            "MODEL FAILURE — The Hebrew LM scores wrong mappings BETTER than the correct one. "
            "Cross-language phonotactic statistics do not preserve the true sign correspondences. "
            "No amount of better optimisation will fix this. Morphological constraints are required."
        )
    else:
        verdict = (
            "DEGENERATE LANDSCAPE — Correct and found mappings score similarly. The bigram "
            "model has almost no signal to distinguish correct from wrong. The score landscape "
            "is flat — hundreds of mappings have near-identical scores."
        )

    print(f"\n  VERDICT: {verdict}")

    print(f"\n  Bigram phonotactic overlap (correct mapping applied):")
    print(f"    Cosine similarity (translated Ugaritic vs Hebrew bigrams): {bigram_cosine:.4f}")
    print(f"    Bigram overlap:   {overlap_count}/{len(trans_bigrams)} = {overlap_frac:.1%} of translated Ugaritic bigrams exist in Hebrew LM")

    if bigram_cosine < 0.3:
        overlap_interp = (
            "LOW — Hebrew and Ugaritic phonotactics are dissimilar even under the correct mapping. "
            "This explains why bigram matching fails for cross-language: the languages don't share "
            "the same consonant-cluster patterns despite sharing the same consonants."
        )
    elif bigram_cosine < 0.6:
        overlap_interp = (
            "MODERATE — Some phonotactic overlap; the signal is present but weak. "
            "A larger Hebrew corpus or morphological priors would amplify this signal."
        )
    else:
        overlap_interp = (
            "HIGH — Strong phonotactic overlap under the correct mapping. The model has good signal; "
            "the problem is purely algorithmic (SA not finding the correct mapping)."
        )
    print(f"\n  Overlap interpretation: {overlap_interp}")

    return {
        "experiment": "bigram_oracle",
        "score_correct_mapping": round(score_correct, 2),
        "score_sa_mapping": round(score_sa, 2),
        "score_freq_rank_mapping": round(score_freq_rank, 2),
        "mean_random_score": round(mean_random_score, 2),
        "delta_correct_minus_sa": round(delta, 2),
        "sa_accuracy": acc_sa["correct"],
        "freq_rank_accuracy": acc_freq_rank["correct"],
        "mean_random_accuracy": round(mean_random_acc, 2),
        "bigram_cosine_similarity": round(bigram_cosine, 4),
        "bigram_overlap_fraction": round(overlap_frac, 4),
        "verdict": verdict,
        "overlap_interpretation": overlap_interp,
    }


# ══════════════════════════════════════════════════════════════════════
# Exp C — Hebrew corpus scaling
# ══════════════════════════════════════════════════════════════════════

def exp_corpus_scaling(d: dict) -> dict[str, Any]:
    """Run Tier 1a at 6 Hebrew corpus sizes (500→7897 tokens).

    Answers: are we still in the data-limited regime for cross-language
    decipherment? If accuracy rises steadily, more Hebrew data will help.
    If accuracy is flat, data size is not the bottleneck — it's the model.
    """
    from glossa_lab.pipelines.decipher import decipher, LanguageModel

    score_accuracy = d["score_accuracy"]
    heb_flat       = d["heb_flat"]
    heb_inscr      = d["heb_inscr"]

    # Build fractional corpora by taking the first N tokens from the full corpus
    total = len(heb_flat)
    sizes = [500, 1000, 2000, 3500, 5000, total]

    print("\n" + "=" * 65)
    print("  Exp C — Hebrew Corpus Scaling (Tier 1a cross-language)")
    print("=" * 65)
    print(f"  Full Hebrew corpus: {total} tokens")
    print()

    results = []
    for n_tokens in sizes:
        # Take first n_tokens tokens; adjust inscriptions accordingly
        flat_sub = heb_flat[:n_tokens]
        # Rebuild inscriptions up to n_tokens (keep full lines until we hit the limit)
        inscr_sub = []
        count = 0
        for insc in heb_inscr:
            if count + len(insc) > n_tokens:
                break
            inscr_sub.append(insc)
            count += len(insc)

        model_sub = LanguageModel(flat_sub, inscriptions=inscr_sub)
        result = decipher(
            d["cipher_flat"], model_sub,
            seed=42, max_iterations=12000, restarts=8,
            cipher_inscriptions=d["cipher_inscr"],
        )
        acc = score_accuracy(result["proposed_mapping"], d["ground_truth"])
        pct = acc["correct"] / 30 * 100

        n_bigrams = len(model_sub.bigram_freq)
        voc       = len(model_sub.alphabet)
        print(
            f"  {n_tokens:5d} tokens  V={voc}  bigrams={n_bigrams:3d}: "
            f"{acc['correct']:2d}/30 = {pct:.1f}%"
        )
        results.append({
            "tokens": n_tokens,
            "bigrams": n_bigrams,
            "correct": acc["correct"],
            "accuracy": acc["accuracy"],
        })

    # Check trend
    accuracies = [r["correct"] for r in results]
    is_increasing = all(
        accuracies[i] <= accuracies[i+1] + 1
        for i in range(len(accuracies) - 1)
    )
    is_flat = max(accuracies) - min(accuracies) <= 2

    if is_flat:
        scaling_interp = (
            "FLAT — Accuracy does not improve with more Hebrew data. "
            "We are NOT in the data-limited regime. The bottleneck is the cross-language "
            "model mismatch, not Hebrew corpus size. More Hebrew data will not help."
        )
    elif is_increasing:
        scaling_interp = (
            "SCALING — Accuracy improves with more data. We are data-limited. "
            "Expanding the Hebrew corpus toward ~20,000 tokens (Snyder scale) would improve Tier 1a."
        )
    else:
        scaling_interp = (
            "IRREGULAR — Accuracy does not scale cleanly with corpus size. "
            "The relationship between data size and cross-language accuracy is non-monotonic, "
            "suggesting other factors (SA randomness, bigram coverage) dominate."
        )

    print(f"\n  INTERPRETATION: {scaling_interp}")

    return {
        "experiment": "corpus_scaling",
        "results": results,
        "interpretation": scaling_interp,
    }


# ══════════════════════════════════════════════════════════════════════
# Exp D — Cognate anchor (semi-supervised)
# ══════════════════════════════════════════════════════════════════════

def exp_cognate_anchor(d: dict) -> dict[str, Any]:
    """Lock 5 known-correct cross-Semitic cognate mappings; SA solves remaining 25.

    Chosen anchors (extremely stable across all Semitic languages):
      r → r  (resh — shared in Ugaritic, Hebrew, Arabic, Aramaic)
      b → b  (bet)
      m → m  (mem)
      l → l  (lamed)
      ' → '  (aleph/alep)

    Reports accuracy at 0, 1, 3, 5 anchors to show the value curve.
    """
    from glossa_lab.pipelines.decipher import LanguageModel

    _score_mapping = d["_score_mapping"]
    score_accuracy = d["score_accuracy"]
    ground_truth   = d["ground_truth"]
    ug_to_ug       = d["ug_to_ug"]
    cipher_flat    = d["cipher_flat"]
    cipher_inscr   = d["cipher_inscr"]

    model = LanguageModel(d["heb_flat"], inscriptions=d["heb_inscr"])

    # Build positional dict
    from collections import defaultdict
    pos_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"initial": 0, "medial": 0, "terminal": 0}
    )
    for insc in cipher_inscr:
        if len(insc) >= 2:
            pos_counts[insc[0]]["initial"] += 1
            pos_counts[insc[-1]]["terminal"] += 1
            for s in insc[1:-1]:
                pos_counts[s]["medial"] += 1
    cipher_positional = {
        sign: {k: v / (sum(pc.values()) or 1) for k, v in pc.items()}
        for sign, pc in pos_counts.items()
    }

    # Invert answer key: ugaritic_sign → opaque_id
    ug_sign_to_oid = {v: k for k, v in ug_to_ug.items()}

    # Define anchors: (ugaritic_sign, hebrew_sign)
    # These are the most phonologically stable consonants across NW Semitic
    ANCHOR_CANDIDATES = [
        ("r", "r"),   # resh  — identical function
        ("b", "b"),   # bet   — identical
        ("m", "m"),   # mem   — identical
        ("l", "l"),   # lamed — identical
        ("'", "'"),   # aleph — initial glottal stop
    ]

    # Filter to anchors that are present in both answer key and ground truth
    valid_anchors = []
    for ug_sign, heb_sign in ANCHOR_CANDIDATES:
        oid = ug_sign_to_oid.get(ug_sign)
        if oid and ground_truth.get(oid) == heb_sign:
            valid_anchors.append((oid, heb_sign, ug_sign))

    print("\n" + "=" * 65)
    print("  Exp D — Cognate Anchor (Semi-supervised Tier 1a)")
    print("=" * 65)
    print(f"\n  Valid anchors from {len(ANCHOR_CANDIDATES)} candidates: {len(valid_anchors)}")
    for oid, heb, ug in valid_anchors:
        print(f"    {oid} (Ugaritic {ug}) → {heb}  ✓ confirmed in ground truth")

    def run_anchored_sa(
        anchors: list[tuple[str, str]],
        seed: int = 42,
        max_iterations: int = 15000,
        restarts: int = 10,
    ) -> int:
        """SA with some sign mappings locked. Returns correct count."""
        rng = random.Random(seed)
        cipher_counts = Counter(cipher_flat)
        cipher_ranked = [s for s, _ in cipher_counts.most_common()]

        # All available target signs
        target_alphabet = list(model.ranked[: len(cipher_ranked)])
        while len(target_alphabet) < len(cipher_ranked):
            target_alphabet.append(f"?{len(target_alphabet)}")

        # Fixed mapping for anchored signs
        fixed: dict[str, str] = {}
        free_cipher  = []
        free_target  = list(target_alphabet)

        # Assign anchors first
        anchor_dict = {oid: heb for oid, heb, _ in anchors}
        for oid, heb in anchor_dict.items():
            if oid in cipher_ranked and heb in free_target:
                fixed[oid] = heb
                free_target.remove(heb)
        for c in cipher_ranked:
            if c not in fixed:
                free_cipher.append(c)

        best_mapping: dict[str, str] = {}
        best_score = float("-inf")

        for restart in range(restarts):
            # Build initial mapping for free signs
            shuffled = list(free_target)
            if restart == 0:
                # Frequency-rank for free signs
                pass  # shuffled already in freq order since target_alphabet is ranked
            else:
                rng.shuffle(shuffled)
            mapping = dict(fixed)  # start with locked anchors
            mapping.update(dict(zip(free_cipher, shuffled)))

            current_score = _score_mapping(cipher_flat, mapping, model, cipher_positional)
            temperature = 1.0
            no_improve = 0

            for _ in range(max_iterations):
                if len(free_cipher) < 2:
                    break
                i = rng.randint(0, len(free_cipher) - 1)
                j = rng.randint(0, len(free_cipher) - 1)
                if i == j:
                    continue
                a, b = free_cipher[i], free_cipher[j]
                mapping[a], mapping[b] = mapping[b], mapping[a]

                new_score = _score_mapping(cipher_flat, mapping, model, cipher_positional)
                delta = new_score - current_score

                if delta > 0 or (
                    temperature > 1e-4 and rng.random() < math.exp(delta / temperature)
                ):
                    current_score = new_score
                    no_improve = 0
                else:
                    mapping[a], mapping[b] = mapping[b], mapping[a]
                    no_improve += 1

                temperature *= 0.9985
                thresh = 250 if temperature < 1e-4 else 800
                if no_improve > thresh:
                    break

            if current_score > best_score:
                best_score = current_score
                best_mapping = dict(mapping)

        acc = score_accuracy(best_mapping, ground_truth)
        return acc["correct"]

    print()
    anchor_levels = [0, 1, 3, 5]
    rows = []
    for n_anchors in anchor_levels:
        active = valid_anchors[:n_anchors]
        label  = f"{n_anchors} anchors" if n_anchors > 0 else "0 anchors (baseline)"
        correct = run_anchored_sa(active, seed=42)
        anchor_names = "+".join(ug for _, _, ug in active) if active else "none"
        pct = correct / 30 * 100
        print(f"  {label:20s} ({anchor_names:20s}):  {correct:2d}/30 = {pct:.1f}%")
        rows.append({"n_anchors": n_anchors, "correct": correct, "accuracy": round(correct/30, 3)})

    # Compute marginal value per anchor
    gains = []
    for i in range(1, len(rows)):
        g = rows[i]["correct"] - rows[i-1]["correct"]
        gains.append(g)
    avg_gain = sum(gains) / len(gains) if gains else 0

    print(f"\n  Average gain per anchor: +{avg_gain:.1f} correct signs")

    if rows[-1]["correct"] >= 15:
        anchor_interp = (
            "STRONG — Semi-supervised anchoring dramatically improves Tier 1a. "
            "Even a small number of known correspondences (e.g. from phonological cognate lists) "
            "could bring the system to state-of-the-art territory."
        )
    elif rows[-1]["correct"] >= 8:
        anchor_interp = (
            "MODERATE — Anchors provide meaningful improvement. Combining anchors with "
            "morphological priors would likely push the system above 50%."
        )
    else:
        anchor_interp = (
            "WEAK — Even with 5 correct anchors, performance remains low. "
            "The remaining 25 signs are too degenerate for bigram matching to resolve. "
            "Morphological constraints are necessary, not just anchors."
        )

    print(f"\n  INTERPRETATION: {anchor_interp}")

    return {
        "experiment": "cognate_anchor",
        "valid_anchors": [(oid, heb, ug) for oid, heb, ug in valid_anchors],
        "results": rows,
        "avg_gain_per_anchor": round(avg_gain, 2),
        "interpretation": anchor_interp,
    }


# ══════════════════════════════════════════════════════════════════════
# Main driver
# ══════════════════════════════════════════════════════════════════════

def run_all_diagnostics(verbose: bool = True) -> dict[str, Any]:
    print("\n" + "█" * 65)
    print("  GLOSSA LAB — Tier Diagnostic Experiments")
    print("  Four analyses to understand cross-language limitations")
    print("█" * 65)

    d = _load_shared()
    print(f"\n  Shared data loaded:")
    print(f"    Hebrew LM:  {len(d['heb_flat'])} tokens, {len(set(d['heb_flat']))} signs")
    print(f"    Ugaritic:   {len(d['cipher_flat'])} tokens, {len(set(d['cipher_flat']))} signs")
    print(f"    GT mappings: {len(d['ground_truth'])}/30")

    results_a = exp_multi_seed_stability(d, n_seeds=10)
    results_b = exp_bigram_oracle(d)
    results_c = exp_corpus_scaling(d)
    results_d = exp_cognate_anchor(d)

    print("\n" + "█" * 65)
    print("  MASTER SUMMARY")
    print("█" * 65)
    print(f"\n  Exp A  Mean accuracy across 10 seeds: {results_a['mean']/30*100:.1f}%  ±{results_a['std']/30*100:.1f}%  (best {results_a['best']}/30)")
    print(f"  Exp B  score(correct) - score(SA):    {results_b['delta_correct_minus_sa']:+.0f}  cosine={results_b['bigram_cosine_similarity']:.4f}")
    print(f"  Exp C  Accuracy at 500/2k/7.9k tokens: {' / '.join(str(r['correct'])+'/30' for r in results_c['results'][::2])}")
    print(f"  Exp D  Accuracy at 0/1/3/5 anchors:    {' / '.join(str(r['correct'])+'/30' for r in results_d['results'])}")
    print()

    return {
        "exp_a_stability": results_a,
        "exp_b_oracle": results_b,
        "exp_c_scaling": results_c,
        "exp_d_anchors": results_d,
    }


if __name__ == "__main__":
    run_all_diagnostics()

try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class TierDiagnostics(_EB):
    id = "tier_diagnostics"
    name = "Tier Diagnostic Suite (4 Experiments)"
    category = "Validation"
    description = (
        "Four diagnostic experiments: multi-seed stability, bigram oracle analysis, "
        "Hebrew corpus scaling, and cognate anchor semi-supervision. "
        "Together they identify whether Tier 1a underperformance is algorithmic or informational."
    )
    estimated_time = "~8 min"
    command = "python -m glossa_lab.experiments.tier_diagnostics"
    params_schema = {"type": "object", "properties": {}}

    def run(self, **kwargs):
        return run_all_diagnostics(verbose=False)

"""Cross-culture contact matrix and script family classifier.

  CulturalContactMatrix — Given a list of corpus IDs, computes pairwise
      contact scores using entropy signature overlap and KL-divergence.
      Returns a matrix and top-N ranking of which cultures show strongest
      contact signals with Indus.

  ScriptFamilyClassifier — Applies a simple feature-based classifier
      (bigram entropy, type-token ratio, Zipf alpha, positional bias)
      to classify a script into families: syllabary, logographic, abjad,
      alphabet, undetermined. Returns classification with confidence.

Registered templates:
  cross_culture_contact_matrix_v1, script_family_classifier_v1
"""
from __future__ import annotations

import math
from collections import Counter
from typing import Any


# ── Helpers ──────────────────────────────────────────────────────────────


def _freq_map(sequences: list[list[str]]) -> dict[str, int]:
    c: Counter[str] = Counter()
    for seq in sequences:
        c.update(seq)
    return dict(c)


def _h1(freq: dict[str, int]) -> float:
    total = sum(freq.values())
    if total <= 0:
        return 0.0
    return -sum((c / total) * math.log2(c / total) for c in freq.values() if c > 0)


def _bigram_h(sequences: list[list[str]]) -> float:
    bg: Counter[tuple[str, str]] = Counter()
    for seq in sequences:
        for i in range(len(seq) - 1):
            bg[(seq[i], seq[i + 1])] += 1
    total = sum(bg.values())
    if total <= 0:
        return 0.0
    return -sum((c / total) * math.log2(c / total) for c in bg.values() if c > 0)


def _zipf_alpha(freq: dict[str, int]) -> float:
    ranked = sorted(freq.values(), reverse=True)
    n = len(ranked)
    if n < 2:
        return 0.0
    lrs = [math.log(r + 1) for r in range(n)]
    lfs = [math.log(f) if f > 0 else 0 for f in ranked]
    mr = sum(lrs) / n
    mf = sum(lfs) / n
    num = sum((lrs[i] - mr) * (lfs[i] - mf) for i in range(n))
    den = sum((lr - mr) ** 2 for lr in lrs)
    return round(-num / den, 4) if den else 0.0


def _type_token_ratio(freq: dict[str, int]) -> float:
    total = sum(freq.values())
    return round(len(freq) / max(1, total), 6)


def _positional_bias(sequences: list[list[str]]) -> float:
    """Compute average positional bias: how concentrated signs are in initial/terminal positions."""
    if not sequences:
        return 0.0
    tc: Counter[str] = Counter(s for seq in sequences for s in seq)
    te: Counter[str] = Counter(seq[-1] for seq in sequences if seq)
    ic: Counter[str] = Counter(seq[0] for seq in sequences if seq)
    biases = []
    for sym, n in tc.items():
        if n < 3:
            continue
        t_rate = te[sym] / n
        i_rate = ic[sym] / n
        biases.append(max(t_rate, i_rate))
    return round(sum(biases) / max(1, len(biases)), 4) if biases else 0.0


def _js_divergence(p_map: dict[str, int], q_map: dict[str, int]) -> float:
    total_p = sum(p_map.values()) or 1
    total_q = sum(q_map.values()) or 1
    all_k = set(p_map) | set(q_map)
    js = 0.0
    for k in all_k:
        pk = p_map.get(k, 0) / total_p
        qk = q_map.get(k, 0) / total_q
        m = (pk + qk) / 2
        if pk > 0 and m > 0:
            js += 0.5 * pk * math.log2(pk / m)
        if qk > 0 and m > 0:
            js += 0.5 * qk * math.log2(qk / m)
    return round(js, 6)


# ── Node 1: CulturalContactMatrix ────────────────────────────────────────


def _cultural_contact_matrix(inputs: dict, params: dict) -> dict:
    """Compute pairwise contact scores between multiple corpora.

    Inputs:
      corpora — dict mapping corpus_name to list[list[str]] sequences,
                OR multiple named inputs (a, b, c, ...) each being
                {sequences: [...], label: "..."}

    Returns a pairwise JS-divergence matrix and a ranking of which
    cultures show strongest contact signals.
    """
    corpora: dict[str, list[list[str]]] = {}

    # Try structured input
    if "corpora" in inputs and isinstance(inputs["corpora"], dict):
        for name, seqs in inputs["corpora"].items():
            if isinstance(seqs, list):
                corpora[name] = seqs
    else:
        # Try named inputs (a, b, c, ...)
        for k, v in sorted(inputs.items()):
            if isinstance(v, dict):
                label = v.get("label") or v.get("corpus") or k
                seqs = v.get("sequences") or []
                if seqs:
                    corpora[str(label)] = seqs
            elif isinstance(v, list) and v and isinstance(v[0], list):
                corpora[k] = v

    if len(corpora) < 2:
        return {"error": "Need at least 2 corpora for pairwise comparison."}

    names = sorted(corpora.keys())
    freq_maps = {n: _freq_map(corpora[n]) for n in names}

    # Compute entropy signatures for overlap scoring
    signatures: dict[str, dict] = {}
    for n in names:
        fm = freq_maps[n]
        seqs = corpora[n]
        signatures[n] = {
            "h1": round(_h1(fm), 4),
            "bigram_h": round(_bigram_h(seqs), 4),
            "zipf_alpha": _zipf_alpha(fm),
            "n_types": len(fm),
            "n_tokens": sum(fm.values()),
            "ttr": _type_token_ratio(fm),
        }

    # Pairwise JS divergence matrix
    matrix: list[dict] = []
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            if j <= i:
                continue
            js = _js_divergence(freq_maps[a], freq_maps[b])
            # Entropy signature similarity
            sig_a = signatures[a]
            sig_b = signatures[b]
            h1_diff = abs(sig_a["h1"] - sig_b["h1"])
            zipf_diff = abs(sig_a["zipf_alpha"] - sig_b["zipf_alpha"])
            # Combined contact score (lower = stronger contact)
            contact_score = round(js * 0.6 + h1_diff * 0.1 + zipf_diff * 0.3, 6)
            matrix.append({
                "corpus_a": a,
                "corpus_b": b,
                "js_divergence": js,
                "h1_diff": round(h1_diff, 4),
                "zipf_diff": round(zipf_diff, 4),
                "contact_score": contact_score,
            })

    # Rank by contact score
    matrix.sort(key=lambda x: x["contact_score"])
    top_n = int(params.get("top_n", 10))

    verdict = (
        f"Cultural contact matrix: {len(names)} corpora, "
        f"{len(matrix)} pairwise comparisons. "
        f"Strongest contact: {matrix[0]['corpus_a']} ↔ {matrix[0]['corpus_b']} "
        f"(score={matrix[0]['contact_score']:.4f})."
    ) if matrix else "No comparisons computed."

    return {
        "matrix": matrix[:top_n],
        "full_matrix": matrix,
        "signatures": signatures,
        "n_corpora": len(names),
        "n_pairs": len(matrix),
        "corpus_names": names,
        "verdict": verdict,
        "json": {"matrix": matrix[:top_n], "signatures": signatures},
    }


# ── Node 2: ScriptFamilyClassifier ───────────────────────────────────────


def _script_family_classifier(inputs: dict, params: dict) -> dict:
    """Classify a script into writing system families using structural features.

    Features used:
      - Bigram entropy (H2)
      - Type-token ratio (TTR)
      - Zipf alpha exponent
      - Positional bias (max(initial_rate, terminal_rate) averaged)
      - Vocabulary size (number of distinct symbols)

    Families: syllabary, logographic, abjad, alphabet, undetermined
    """
    sequences = inputs.get("sequences") or []
    if not sequences:
        return {"error": "No sequences — connect a corpus."}

    label = str(params.get("label", "unknown"))

    fm = _freq_map(sequences)
    h1_val = _h1(fm)
    h2_val = _bigram_h(sequences)
    ttr = _type_token_ratio(fm)
    zipf = _zipf_alpha(fm)
    pos_bias = _positional_bias(sequences)
    n_types = len(fm)
    n_tokens = sum(fm.values())
    avg_len = round(sum(len(s) for s in sequences) / max(1, len(sequences)), 2)

    # Rule-based classification
    scores: dict[str, float] = {
        "syllabary": 0.0,
        "logographic": 0.0,
        "abjad": 0.0,
        "alphabet": 0.0,
        "undetermined": 0.0,
    }

    # Vocabulary size signal
    if n_types > 200:
        scores["logographic"] += 3.0
    elif n_types > 80:
        scores["syllabary"] += 2.0
        scores["logographic"] += 1.0
    elif n_types > 40:
        scores["syllabary"] += 2.0
    elif n_types > 20:
        scores["abjad"] += 2.0
        scores["alphabet"] += 1.5
    else:
        scores["abjad"] += 3.0

    # H1 signal
    if h1_val > 8.0:
        scores["logographic"] += 2.0
    elif h1_val > 5.5:
        scores["syllabary"] += 2.0
    elif h1_val > 4.0:
        scores["abjad"] += 1.5
        scores["alphabet"] += 1.0
    else:
        scores["abjad"] += 2.0

    # Zipf alpha signal
    if zipf > 1.5:
        scores["logographic"] += 1.0
    elif zipf > 1.0:
        scores["syllabary"] += 0.5
    else:
        scores["abjad"] += 0.5
        scores["alphabet"] += 0.5

    # Positional bias signal (high = more structured/restricted)
    if pos_bias > 0.4:
        scores["logographic"] += 1.0  # logograms often position-specific
    elif pos_bias > 0.25:
        scores["syllabary"] += 0.5

    # Average word length
    if avg_len > 5:
        scores["syllabary"] += 1.0
    elif avg_len < 3:
        scores["abjad"] += 0.5

    # Find winner
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    best_family = ranked[0][0]
    best_score = ranked[0][1]
    total_score = sum(scores.values())
    confidence = round(best_score / max(1.0, total_score), 4)

    # Low confidence → undetermined
    if confidence < 0.3 or best_score < 2.0:
        best_family = "undetermined"
        confidence = round(confidence * 0.5, 4)

    verdict = (
        f"Script family classifier ({label}): {best_family} "
        f"(confidence={confidence:.2%}). "
        f"Features: H1={h1_val:.2f}, H2={h2_val:.2f}, TTR={ttr:.6f}, "
        f"Zipf={zipf:.2f}, pos_bias={pos_bias:.3f}, "
        f"vocab={n_types}, avg_len={avg_len}."
    )

    return {
        "label": label,
        "classification": best_family,
        "confidence": confidence,
        "scores": {k: round(v, 2) for k, v in ranked},
        "features": {
            "h1": round(h1_val, 4),
            "h2": round(h2_val, 4),
            "ttr": ttr,
            "zipf_alpha": zipf,
            "positional_bias": pos_bias,
            "n_types": n_types,
            "n_tokens": n_tokens,
            "avg_word_length": avg_len,
        },
        "verdict": verdict,
        "text": verdict,
    }


# ── Registration ─────────────────────────────────────────────────────────


def _cross_culture_node_defs() -> list:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "CulturalContactMatrix", "Cultural Contact Matrix",
            "Cross-Language",
            "Compute pairwise contact scores between multiple corpora using "
            "entropy signature overlap and KL-divergence. Returns a ranked matrix "
            "of which cultures show strongest contact signals.",
            inputs=[
                {"name": "corpora", "type": "json", "required": False},
                {"name": "a", "type": "any", "required": False},
                {"name": "b", "type": "any", "required": False},
                {"name": "c", "type": "any", "required": False},
                {"name": "d", "type": "any", "required": False},
                {"name": "e", "type": "any", "required": False},
            ],
            outputs=[
                {"name": "matrix", "type": "json"},
                {"name": "signatures", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {
                "top_n": {"type": "integer", "default": 10, "minimum": 1},
            }},
            fn=_cultural_contact_matrix,
        ),
        AtomicNodeDef(
            "ScriptFamilyClassifier", "Script Family Classifier",
            "Cross-Language",
            "Classify a script into writing system families (syllabary, logographic, "
            "abjad, alphabet, undetermined) using bigram entropy, type-token ratio, "
            "Zipf alpha, and positional bias features.",
            inputs=[
                {"name": "sequences", "type": "sequences", "required": True},
            ],
            outputs=[
                {"name": "classification", "type": "text"},
                {"name": "confidence", "type": "number"},
                {"name": "features", "type": "json"},
                {"name": "scores", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {
                "label": {"type": "string", "default": "unknown",
                          "description": "Label for the corpus being classified"},
            }},
            fn=_script_family_classifier,
        ),
    ]

"""Phase-15 atomic node implementations.

Three orthogonal validation experiments:

  Step 1 — LongTailFilter + LongTailVerdict
      Filter the corpus to inscriptions of length >= min_length (default 7)
      and produce a focused "is the long-tail language-like?" verdict.
      Phase-14's exponential MI-decay finding on full M77 may be a
      length-truncation artifact; this isolates the hypothesis.

  Step 2 — CipherSelfTestRunner
      Build a known random cipher on a reference corpus (Linear B,
      Sumerian, etc.), run CTT-anchored SA twice (once with frequency-
      ranked anchors, once with EpistaticAnchorRanker output), score
      against ground truth. Targets >= 95 percent top-1 with epistatic
      anchors. Validates the framework on a known-decoded script before
      applying to Indus.

  Step 3 — MultiHypothesisRanker
      Take N hypothesis projection outputs (one per language hypothesis)
      and rank by max_violation. The hypothesis with the lowest violation
      is the empirically best fit to the corpus's measured DoFs.

  Step 4 (Phase-16) — DecipheredMappingExporter
      Produce the headline decipherment attempt: applies the best
      hypothesis (lowest max_violation) + epistatic anchors + CTT-SA on
      the long-tail subset and emits the final sign->value mapping with
      per-sign confidence.
"""

from __future__ import annotations

import math
import random
from collections import Counter
from typing import Any


def _flatten(seqs: list[list[str]]) -> list[str]:
    return [s for seq in seqs for s in seq]


# ── Step 1.1 — LongTailFilter ──────────────────────────────────────────


def _long_tail_filter(inputs: dict, params: dict) -> dict:
    """Filter sequences to inscriptions of length >= min_length.

    Distinct from the generic SequenceFilter in that we explicitly tag
    the output for downstream LongTailVerdict consumption and report
    n_dropped / share_kept diagnostics.
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    min_length = max(1, int(params.get("min_length", 7)))
    max_length = int(params.get("max_length", 0))  # 0 = no upper bound
    label = str(params.get("label", "long_tail"))

    kept: list[list[str]] = []
    n_drop_short = 0
    n_drop_long = 0
    for seq in sequences:
        L = len(seq)
        if L < min_length:
            n_drop_short += 1
            continue
        if max_length > 0 and L > max_length:
            n_drop_long += 1
            continue
        kept.append(seq)

    n_in = len(sequences)
    flat_kept = _flatten(kept)
    return {
        "sequences": kept,
        "label": label,
        "min_length": min_length,
        "max_length": max_length,
        "n_input": n_in,
        "n_kept": len(kept),
        "n_dropped_short": n_drop_short,
        "n_dropped_long": n_drop_long,
        "share_kept": round(len(kept) / max(1, n_in), 4),
        "n_tokens_kept": len(flat_kept),
        "distinct_symbols_kept": len(set(flat_kept)),
        "verdict": (
            f"Kept {len(kept)} of {n_in} inscriptions (length>={min_length})"
            f"; total {len(flat_kept)} tokens, "
            f"{len(set(flat_kept))} distinct signs."
        ),
    }


# ── Step 1.2 — LongTailVerdict ─────────────────────────────────────────


def _long_tail_verdict(inputs: dict, params: dict) -> dict:
    """Combine MI-decay (the discriminating Phase-14 test) with HED and
    Zipf on the long-tail-only subset. Decisive yes/no on whether longer
    inscriptions exhibit power-law MI decay.

    Inputs:
      mi_decay_full, mi_decay_long      (both required) — Phase-14 nodes
      hed_long                          (required)
      zipf_long                          (optional)
      conditional_entropy_long           (optional)
      filter_summary                     (LongTailFilter output)

    The headline test:
      - if mi_decay_long.regime == "power_law" and full was "exponential"
        → hypothesis (1) WINS: decipherment is meaningful, M77's full-corpus
        exponential decay was a truncation artifact.
      - if mi_decay_long.regime == "exponential"
        → hypothesis (2) WINS: even the long tail is Markov-1; the script
        is local-only (heraldic/admin), not free text.
      - if regime is "ambiguous" or "flat" with HED still language-like:
        → INSUFFICIENT DATA: 283 inscriptions may not be enough to
        discriminate.
    """
    mi_full = inputs.get("mi_decay_full") or {}
    mi_long = inputs.get("mi_decay_long") or {}
    hed_long = inputs.get("hed_long") or {}
    zipf_long = inputs.get("zipf_long") or {}
    cond_long = inputs.get("conditional_entropy_long") or {}
    filter_summary = inputs.get("filter_summary") or {}

    full_regime = str(mi_full.get("regime", "unknown"))
    long_regime = str(mi_long.get("regime", "unknown"))
    full_gamma = float(mi_full.get("gamma_powerlaw", mi_full.get("gamma", 0.0)))
    long_gamma = float(mi_long.get("gamma_powerlaw", mi_long.get("gamma", 0.0)))
    full_lam = float(mi_full.get("lambda_exponential", mi_full.get("lambda", 0.0)))
    long_lam = float(mi_long.get("lambda_exponential", mi_long.get("lambda", 0.0)))

    hed_regime = str(hed_long.get("regime", "unknown"))
    f2 = float(hed_long.get("f2_over_f1", 0.0))
    f3 = float(hed_long.get("f3_over_f2", 0.0))

    n_kept = int(filter_summary.get("n_kept", 0))
    n_tokens = int(filter_summary.get("n_tokens_kept", 0))

    if long_regime == "power_law":
        if full_regime in ("exponential", "ambiguous", "flat"):
            verdict_class = "TRUNCATION_ARTIFACT_WINS"
            verdict_text = (
                f"DECIPHERMENT IS MEANINGFUL. Long-tail MI decay is power-"
                f"law (gamma={long_gamma:.2f}) while full-corpus is "
                f"{full_regime} (gamma={full_gamma:.2f}). Phase-14's "
                f"exponential-decay finding on full M77 was a length-"
                f"truncation artifact; the script does carry long-range "
                f"correlations on inscriptions where they can fit. "
                f"Hypothesis (1) wins."
            )
        else:
            verdict_class = "POWERLAW_BOTH"
            verdict_text = (
                f"Long-tail and full-corpus both exhibit power-law MI "
                f"decay (gamma_long={long_gamma:.2f}, gamma_full="
                f"{full_gamma:.2f}). Strong signal across all length "
                f"strata."
            )
    elif long_regime == "exponential":
        verdict_class = "HERALDIC_WINS"
        verdict_text = (
            f"DECIPHERMENT IS CLOSED. Long-tail MI decay remains "
            f"exponential (lambda={long_lam:.3f}, gamma={long_gamma:.2f}) "
            f"on {n_kept} inscriptions ({n_tokens} tokens). The script "
            f"is local-only (Markov-1) at every length stratum, which is "
            f"the heraldic / administrative-tag signature, not a free-"
            f"text natural language. Hypothesis (2) wins."
        )
    elif long_regime in ("flat", "unknown"):
        verdict_class = "INSUFFICIENT_DATA"
        verdict_text = (
            f"INSUFFICIENT DATA. Long-tail MI decay is {long_regime} on "
            f"{n_kept} inscriptions; cannot discriminate. Need either "
            f"more long inscriptions, or a different test."
        )
    else:
        verdict_class = "AMBIGUOUS"
        verdict_text = (
            f"AMBIGUOUS. Long-tail decay regime {long_regime} "
            f"(gamma={long_gamma:.2f}, lambda={long_lam:.3f}). Compare "
            f"with HED ({hed_regime}, 2/1={f2:.2f}, 3/2={f3:.2f})."
        )

    return {
        "verdict_class": verdict_class,
        "verdict": verdict_text,
        "mi_full_regime": full_regime,
        "mi_long_regime": long_regime,
        "mi_full_gamma": round(full_gamma, 4),
        "mi_long_gamma": round(long_gamma, 4),
        "mi_full_lambda": round(full_lam, 4),
        "mi_long_lambda": round(long_lam, 4),
        "hed_long_regime": hed_regime,
        "hed_long_f2_over_f1": round(f2, 4),
        "hed_long_f3_over_f2": round(f3, 4),
        "n_long_tail_inscriptions": n_kept,
        "n_long_tail_tokens": n_tokens,
        "next_step": (
            "PROCEED_TO_PHASE_16" if verdict_class.startswith("TRUNCATION") or
            verdict_class == "POWERLAW_BOTH"
            else "STOP_OR_REFRAME"
        ),
        "json": {
            "verdict_class": verdict_class,
            "verdict": verdict_text,
            "mi_full_regime": full_regime,
            "mi_long_regime": long_regime,
        },
    }


# ── Step 2 — CipherSelfTestRunner ──────────────────────────────────────


def _cipher_self_test_runner(inputs: dict, params: dict) -> dict:
    """Build a random cipher on a known-decoded reference corpus, run two
    SA decipherments (frequency anchors vs epistatic anchors), score top-1.

    Inputs:
      sequences  : reference-language sequences (Linear B, Sumerian, ...)

    Params:
      cipher_seed         : random seed for the bijective shuffle
      n_anchors           : how many anchors to inject in each condition
      max_iterations      : SA iterations per restart
      restarts            : SA restarts per condition
      condition_a         : "frequency" | "epistatic" (default: both)
      label               : reporting label

    For each condition we record top-1 accuracy on all signs, on free
    (non-anchored) signs, and the absolute improvement of epistatic over
    frequency.
    """
    sequences: list[list[str]] = inputs.get("sequences") or []
    cipher_seed = int(params.get("cipher_seed", 42))
    n_anchors = int(params.get("n_anchors", 10))
    max_iter = int(params.get("max_iterations", 3000))
    restarts = int(params.get("restarts", 2))
    label = str(params.get("label", "self_test"))

    if not sequences or len(_flatten(sequences)) < 100:
        return {
            "label": label,
            "verdict": "Empty or too-small reference corpus.",
            "freq_acc_all": 0.0,
            "epi_acc_all": 0.0,
        }

    flat = _flatten(sequences)
    inv = sorted(set(flat))
    rng = random.Random(cipher_seed)
    shuf = list(inv)
    rng.shuffle(shuf)
    perm = {inv[i]: shuf[i] for i in range(len(inv))}      # original -> cipher
    truth = {shuf[i]: inv[i] for i in range(len(inv))}     # cipher -> original

    # Build cipher sequences
    cipher_seqs = [[perm[s] for s in seq if s in perm] for seq in sequences]
    cipher_flat = _flatten(cipher_seqs)

    # Frequency-ranked anchors
    freq_ranked = [s for s, _ in Counter(cipher_flat).most_common()]
    freq_anchors = {s: truth[s] for s in freq_ranked[:n_anchors] if s in truth}

    # Epistatic-ranked anchors (compute directly here using bigram PMI on
    # the cipher_seqs, mirroring _epistatic_anchor_ranker).
    uni: Counter[str] = Counter(cipher_flat)
    bi: Counter[tuple[str, str]] = Counter()
    for seq in cipher_seqs:
        for i in range(len(seq) - 1):
            bi[(seq[i], seq[i + 1])] += 1
    n_uni = sum(uni.values()) or 1
    n_bi = sum(bi.values()) or 1
    centrality: dict[str, float] = {}
    for (a, b), c in bi.items():
        if c < 5:
            continue
        p_a = uni[a] / n_uni
        p_b = uni[b] / n_uni
        p_ab = c / n_bi
        if p_a <= 0 or p_b <= 0:
            continue
        pmi = math.log(p_ab / (p_a * p_b))
        w = abs(pmi) * c
        centrality[a] = centrality.get(a, 0.0) + w
        centrality[b] = centrality.get(b, 0.0) + w
    epi_ranked = sorted(centrality.keys(), key=lambda s: -centrality[s])
    epi_anchors = {s: truth[s] for s in epi_ranked[:n_anchors] if s in truth}

    # Build a reference LM on ORIGINAL sequences for SA to score against.
    try:
        from glossa_lab.pipelines.decipher import LanguageModel, decipher  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001
        return {"label": label, "error": f"decipher import failed: {exc}"}

    lm = LanguageModel(flat, inscriptions=sequences)

    def _run_sa(anchors: dict, seed: int) -> dict:
        try:
            r = decipher(
                cipher_flat, lm,
                seed=seed,
                max_iterations=max_iter,
                restarts=restarts,
                cipher_inscriptions=cipher_seqs,
                surjective=False,
                use_sa=True,
                anchors=anchors or None,
            )
            return r.get("proposed_mapping", {})
        except Exception as exc:  # noqa: BLE001
            return {"_error": str(exc)}

    def _score(mapping: dict, anchored: set) -> dict:
        cs = list(truth.keys())
        if not cs:
            return {"top1_all": 0.0, "top1_free": 0.0, "n_signs": 0}
        free = [s for s in cs if s not in anchored]
        n_correct = sum(1 for s in cs if mapping.get(s) == truth.get(s))
        n_correct_free = sum(1 for s in free if mapping.get(s) == truth.get(s))
        return {
            "top1_all": round(n_correct / max(1, len(cs)), 4),
            "top1_free": round(n_correct_free / max(1, len(free)), 4),
            "n_signs": len(cs),
            "n_free": len(free),
            "n_correct_all": n_correct,
            "n_correct_free": n_correct_free,
        }

    # Run both conditions.
    freq_map_a = _run_sa(freq_anchors, cipher_seed + 1)
    epi_map_a  = _run_sa(epi_anchors,  cipher_seed + 2)
    freq_metrics = _score(freq_map_a, set(freq_anchors.keys()))
    epi_metrics  = _score(epi_map_a,  set(epi_anchors.keys()))

    delta_all = epi_metrics.get("top1_all", 0.0) - freq_metrics.get("top1_all", 0.0)
    delta_free = epi_metrics.get("top1_free", 0.0) - freq_metrics.get("top1_free", 0.0)

    if epi_metrics.get("top1_all", 0.0) >= 0.95:
        verdict = (
            f"{label}: epistatic anchors achieve {epi_metrics['top1_all']:.1%} "
            f"top-1 accuracy (target >=95%). FRAMEWORK VALIDATED on a known-"
            f"decoded reference corpus. Field-ready."
        )
    elif epi_metrics.get("top1_all", 0.0) >= freq_metrics.get("top1_all", 0.0) + 0.05:
        verdict = (
            f"{label}: epistatic anchors improve top-1 from "
            f"{freq_metrics['top1_all']:.1%} to {epi_metrics['top1_all']:.1%} "
            f"(delta={delta_all:+.1%}); below the 95% bar but better than "
            f"frequency baseline."
        )
    elif epi_metrics.get("top1_all", 0.0) < freq_metrics.get("top1_all", 0.0) - 0.05:
        verdict = (
            f"{label}: epistatic anchors UNDERPERFORM frequency anchors "
            f"({epi_metrics['top1_all']:.1%} vs {freq_metrics['top1_all']:.1%}). "
            f"Anchor-selection criterion needs revision."
        )
    else:
        verdict = (
            f"{label}: epistatic and frequency anchors are roughly equivalent "
            f"({epi_metrics['top1_all']:.1%} vs {freq_metrics['top1_all']:.1%}); "
            f"either method would do."
        )

    return {
        "label": label,
        "n_inv": len(inv),
        "n_anchors": n_anchors,
        "freq_anchors_count": len(freq_anchors),
        "epi_anchors_count": len(epi_anchors),
        "freq_metrics": freq_metrics,
        "epi_metrics": epi_metrics,
        "delta_top1_all": round(delta_all, 4),
        "delta_top1_free": round(delta_free, 4),
        "verdict": verdict,
        "epistatic_anchor_signs": list(epi_anchors.keys())[:10],
        "frequency_anchor_signs": list(freq_anchors.keys())[:10],
        "json": {
            "label": label,
            "freq_top1": freq_metrics.get("top1_all"),
            "epi_top1": epi_metrics.get("top1_all"),
            "delta": delta_all,
            "verdict": verdict,
        },
    }


# ── Step 3 — MultiHypothesisRanker ─────────────────────────────────────


def _multi_hypothesis_ranker(inputs: dict, params: dict) -> dict:
    """Take up to 6 hypothesis projection outputs (each a result dict
    with success / max_violation / model_source) and rank by max_violation.

    Param `labels` names the hypotheses in port order.

    Output: ranked list, the winning hypothesis name, the max_violation
    spread, and a verdict.
    """
    ports = ("a", "b", "c", "d", "e", "f")
    labels_raw = params.get("labels", []) or []
    if isinstance(labels_raw, str):
        labels = [s.strip() for s in labels_raw.split(",") if s.strip()]
    elif isinstance(labels_raw, (list, tuple)):
        labels = [str(s).strip() for s in labels_raw if str(s).strip()]
    else:
        labels = []

    rows: list[dict] = []
    for i, port in enumerate(ports):
        v = inputs.get(port)
        if not isinstance(v, dict):
            continue
        label = labels[i] if i < len(labels) else port
        mv = float(v.get("max_violation", 1e9))
        ok = bool(v.get("success", False))
        src = str(v.get("model_source", ""))
        rows.append({
            "hypothesis": label,
            "max_violation": round(mv, 6),
            "success": ok,
            "model_source": src,
            "iterations": int(v.get("iterations", 0)),
        })

    if not rows:
        return {"ranked": [], "winner": None,
                "verdict": "No hypothesis projections supplied."}

    rows.sort(key=lambda r: r["max_violation"])
    winner = rows[0]
    runner_up = rows[1] if len(rows) > 1 else None
    spread = (runner_up["max_violation"] - winner["max_violation"]) if runner_up else 0.0

    if winner["max_violation"] >= 1.0:
        confidence_text = "weak (every hypothesis violated >= 1.0)"
    elif spread >= 0.5:
        confidence_text = "strong (winner beats runner-up by >= 0.5)"
    elif spread >= 0.1:
        confidence_text = "moderate"
    else:
        confidence_text = "low (top hypotheses are within 0.1 of each other)"

    verdict = (
        f"Best fit: '{winner['hypothesis']}' with max_violation="
        f"{winner['max_violation']:.4f} (success={winner['success']}). "
        f"Margin to runner-up: {spread:.4f} ({confidence_text})."
    )

    return {
        "ranked": rows,
        "winner": winner["hypothesis"],
        "winner_max_violation": winner["max_violation"],
        "runner_up": runner_up["hypothesis"] if runner_up else None,
        "spread": round(spread, 6),
        "confidence_text": confidence_text,
        "verdict": verdict,
        "json": {
            "ranked": rows,
            "winner": winner["hypothesis"],
            "verdict": verdict,
        },
    }


# ── Step 4 (Phase-16) — DecipheredMappingExporter ──────────────────────


def _deciphered_mapping_exporter(inputs: dict, params: dict) -> dict:
    """Decipherment-attempt summarizer. Takes a proposed_mapping plus the
    epistatic anchor table and the winning-hypothesis label, then emits a
    structured per-sign decipherment table with confidence categories.

    A full-fledged decipherment node would also re-run SA with the
    empirically-best anchors + best CAS-YAML; that path is wired in the
    Phase-16 graph by chaining the existing CTTAnchoredSADecipher with
    Phase-15 outputs as inputs. This node is the *report*.
    """
    proposed = inputs.get("proposed_mapping") or {}
    anchors = inputs.get("anchors") or {}
    epi_ranking = inputs.get("epistatic_ranking") or []
    winner = str(inputs.get("winning_hypothesis") or params.get("winning_hypothesis", "unknown"))

    centrality_by_sign: dict[str, float] = {}
    if isinstance(epi_ranking, list):
        for r in epi_ranking:
            if isinstance(r, dict) and "sign" in r:
                centrality_by_sign[str(r["sign"])] = float(r.get("centrality", 0.0))

    table: list[dict] = []
    for sign, value in proposed.items():
        is_anchored = sign in anchors
        cent = centrality_by_sign.get(sign, 0.0)
        if is_anchored:
            confidence = "anchored"
        elif cent >= 1.0:
            confidence = "high_centrality"
        elif cent >= 0.3:
            confidence = "medium_centrality"
        else:
            confidence = "low_centrality"
        table.append({
            "sign": sign,
            "decoded_value": value,
            "anchored": is_anchored,
            "epistatic_centrality": round(cent, 4),
            "confidence": confidence,
        })

    table.sort(key=lambda r: -r["epistatic_centrality"])
    n_anchored = sum(1 for r in table if r["anchored"])
    n_high = sum(1 for r in table if r["confidence"] == "high_centrality")
    n_medium = sum(1 for r in table if r["confidence"] == "medium_centrality")

    verdict = (
        f"Hypothesis '{winner}' produced a {len(table)}-sign mapping; "
        f"{n_anchored} anchored, {n_high} high-centrality, "
        f"{n_medium} medium-centrality."
    )

    return {
        "winning_hypothesis": winner,
        "table": table,
        "n_signs_total": len(table),
        "n_anchored": n_anchored,
        "n_high_centrality": n_high,
        "n_medium_centrality": n_medium,
        "verdict": verdict,
        "json": {"winner": winner, "table": table[:50], "verdict": verdict},
    }


# ── Atomic node defs for registration ─────────────────────────────────


def _phase15_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "LongTailFilter", "Long-Tail Filter (Phase-15)",
            "Phase-15 / Long-tail",
            "Filter a corpus to inscriptions of length >= min_length (default 7). "
            "Used to isolate the long-tail subset from a corpus dominated by "
            "short inscriptions, so MI decay and HED can be re-measured on "
            "samples where long-range correlations have room to fit.",
            inputs=[{"name": "sequences", "type": "sequences", "required": True}],
            outputs=[
                {"name": "sequences", "type": "sequences"},
                {"name": "label", "type": "text"},
                {"name": "n_input", "type": "number"},
                {"name": "n_kept", "type": "number"},
                {"name": "n_dropped_short", "type": "number"},
                {"name": "n_dropped_long", "type": "number"},
                {"name": "share_kept", "type": "number"},
                {"name": "n_tokens_kept", "type": "number"},
                {"name": "distinct_symbols_kept", "type": "number"},
                {"name": "verdict", "type": "text"},
                {"name": "min_length", "type": "number"},
                {"name": "max_length", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_length": {"type": "integer", "default": 7, "minimum": 1},
                    "max_length": {"type": "integer", "default": 0},
                    "label": {"type": "string", "default": "long_tail"},
                },
            },
            fn=_long_tail_filter,
        ),
        AtomicNodeDef(
            "LongTailVerdict", "Long-Tail Verdict (Phase-15 step 1)",
            "Phase-15 / Long-tail",
            "Combines full-corpus + long-tail MI decay with long-tail HED into "
            "a four-way verdict: TRUNCATION_ARTIFACT_WINS, POWERLAW_BOTH, "
            "HERALDIC_WINS, INSUFFICIENT_DATA, AMBIGUOUS. Tells you whether "
            "Phase-14's exponential MI-decay finding survives length filtering.",
            inputs=[
                {"name": "mi_decay_full", "type": "json", "required": True},
                {"name": "mi_decay_long", "type": "json", "required": True},
                {"name": "hed_long", "type": "json", "required": True},
                {"name": "zipf_long", "type": "json", "required": False},
                {"name": "conditional_entropy_long", "type": "json", "required": False},
                {"name": "filter_summary", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "verdict_class", "type": "text"},
                {"name": "verdict", "type": "text"},
                {"name": "mi_full_regime", "type": "text"},
                {"name": "mi_long_regime", "type": "text"},
                {"name": "mi_full_gamma", "type": "number"},
                {"name": "mi_long_gamma", "type": "number"},
                {"name": "mi_full_lambda", "type": "number"},
                {"name": "mi_long_lambda", "type": "number"},
                {"name": "hed_long_regime", "type": "text"},
                {"name": "n_long_tail_inscriptions", "type": "number"},
                {"name": "n_long_tail_tokens", "type": "number"},
                {"name": "next_step", "type": "text"},
                {"name": "json", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_long_tail_verdict,
        ),
        AtomicNodeDef(
            "CipherSelfTestRunner", "Cipher Self-Test (Phase-15 step 2)",
            "Phase-15 / Validation",
            "Build a known random cipher on a reference corpus, run two SA "
            "decipherments (frequency anchors vs epistatic anchors), and "
            "score top-1 accuracy. Targets >=95 percent with epistatic "
            "anchors. Use to validate the framework on a known-decoded "
            "script before applying to Indus.",
            inputs=[{"name": "sequences", "type": "sequences", "required": True}],
            outputs=[
                {"name": "label", "type": "text"},
                {"name": "n_inv", "type": "number"},
                {"name": "n_anchors", "type": "number"},
                {"name": "freq_metrics", "type": "json"},
                {"name": "epi_metrics", "type": "json"},
                {"name": "delta_top1_all", "type": "number"},
                {"name": "delta_top1_free", "type": "number"},
                {"name": "verdict", "type": "text"},
                {"name": "epistatic_anchor_signs", "type": "json"},
                {"name": "frequency_anchor_signs", "type": "json"},
                {"name": "json", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "cipher_seed": {"type": "integer", "default": 42},
                    "n_anchors": {"type": "integer", "default": 10, "minimum": 1},
                    "max_iterations": {"type": "integer", "default": 3000, "minimum": 100},
                    "restarts": {"type": "integer", "default": 2, "minimum": 1},
                    "label": {"type": "string", "default": "self_test"},
                },
            },
            fn=_cipher_self_test_runner,
        ),
        AtomicNodeDef(
            "MultiHypothesisRanker", "Multi-Hypothesis Ranker (Phase-15 step 3)",
            "Phase-15 / Hypothesis comparison",
            "Take up to 6 hypothesis projection outputs (each a different "
            "language hypothesis) and rank by max_violation. Lowest violation "
            "wins. Returns winner, runner-up, and confidence text.",
            inputs=[
                {"name": "a", "type": "json", "required": False},
                {"name": "b", "type": "json", "required": False},
                {"name": "c", "type": "json", "required": False},
                {"name": "d", "type": "json", "required": False},
                {"name": "e", "type": "json", "required": False},
                {"name": "f", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "ranked", "type": "json"},
                {"name": "winner", "type": "text"},
                {"name": "winner_max_violation", "type": "number"},
                {"name": "runner_up", "type": "text"},
                {"name": "spread", "type": "number"},
                {"name": "confidence_text", "type": "text"},
                {"name": "verdict", "type": "text"},
                {"name": "json", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "labels": {"type": "array", "default": []},
                },
            },
            fn=_multi_hypothesis_ranker,
        ),
        AtomicNodeDef(
            "DecipheredMappingExporter", "Deciphered Mapping Exporter (Phase-16)",
            "Phase-16 / Decipherment",
            "Take a proposed_mapping + epistatic_ranking + winning_hypothesis "
            "and emit a structured per-sign decipherment table with confidence "
            "categories (anchored / high_centrality / medium / low). The "
            "headline output of the Phase-16 decipherment attempt.",
            inputs=[
                {"name": "proposed_mapping", "type": "json", "required": True},
                {"name": "anchors", "type": "json", "required": False},
                {"name": "epistatic_ranking", "type": "json", "required": False},
                {"name": "winning_hypothesis", "type": "text", "required": False},
            ],
            outputs=[
                {"name": "winning_hypothesis", "type": "text"},
                {"name": "table", "type": "json"},
                {"name": "n_signs_total", "type": "number"},
                {"name": "n_anchored", "type": "number"},
                {"name": "n_high_centrality", "type": "number"},
                {"name": "n_medium_centrality", "type": "number"},
                {"name": "verdict", "type": "text"},
                {"name": "json", "type": "json"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "winning_hypothesis": {"type": "string", "default": "unknown"},
                },
            },
            fn=_deciphered_mapping_exporter,
        ),
    ]


__all__ = [
    "_long_tail_filter",
    "_long_tail_verdict",
    "_cipher_self_test_runner",
    "_multi_hypothesis_ranker",
    "_deciphered_mapping_exporter",
    "_phase15_node_defs",
]

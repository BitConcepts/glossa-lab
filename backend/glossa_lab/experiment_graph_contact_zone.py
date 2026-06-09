"""Contact-zone analysis experiment templates.

Provides three atomic nodes for quantifying inter-corpus contact signals:

  ContactZoneKLDivergence  — KL/JS divergence between two corpus symbol
                            distributions, top-N overlapping symbols, and
                            a contact-zone verdict.
  ContactZoneSynthesis     — Synthesises outputs from multiple KL comparisons
                            into a ranked summary of language-family contact.
  ContactZoneABComparison  — Runs two corpora A and B against Indus and
                            reports which has the stronger contact signal.

Registered templates:
  contact_zone_kl_v1, contact_zone_synthesis_v1, contact_zone_ab_v1
"""
from __future__ import annotations

import math
from collections import Counter
from typing import Any


# ── Helpers ──────────────────────────────────────────────────────────────


def _freq_map_from_sequences(sequences: list[list[str]]) -> dict[str, int]:
    c: Counter[str] = Counter()
    for seq in sequences:
        c.update(seq)
    return dict(c)


def _kl_js(p_map: dict[str, int], q_map: dict[str, int], top_n: int = 20) -> dict[str, Any]:
    """Compute KL(P||Q) and JS divergence, plus top-N overlapping symbols."""
    total_p = sum(p_map.values()) or 1
    total_q = sum(q_map.values()) or 1
    all_keys = set(p_map) | set(q_map)

    kl = 0.0
    js = 0.0
    overlap_scores: list[tuple[str, float]] = []

    for k in all_keys:
        pk = p_map.get(k, 0) / total_p
        qk = q_map.get(k, 0) / total_q
        if pk > 0 and qk > 0:
            kl += pk * math.log2(pk / qk)
            # Score overlap by harmonic mean of the two probabilities
            overlap_scores.append((k, 2 * pk * qk / (pk + qk)))
        m = (pk + qk) / 2
        if pk > 0 and m > 0:
            js += 0.5 * pk * math.log2(pk / m)
        if qk > 0 and m > 0:
            js += 0.5 * qk * math.log2(qk / m)

    overlap_scores.sort(key=lambda x: -x[1])
    top_overlap = [{"symbol": s, "score": round(sc, 6)} for s, sc in overlap_scores[:top_n]]
    n_shared = sum(1 for k in all_keys if k in p_map and k in q_map)

    return {
        "kl_divergence": round(kl, 6),
        "js_divergence": round(js, 6),
        "n_symbols_p": len(p_map),
        "n_symbols_q": len(q_map),
        "n_shared": n_shared,
        "overlap_ratio": round(n_shared / max(1, len(all_keys)), 4),
        "top_overlap": top_overlap,
    }


# ── Node 1: ContactZoneKLDivergence ──────────────────────────────────────


def _contact_zone_kl_divergence(inputs: dict, params: dict) -> dict:
    """Compute KL divergence between two corpus token sequences.

    Inputs:
      sequences_a — list[list[str]] (corpus A, e.g. Indus)
      sequences_b — list[list[str]] (corpus B, e.g. Sumerian)
      OR freq_map_a / freq_map_b — pre-computed frequency maps

    Returns divergence score, top-N overlapping symbols, and a
    contact-zone verdict based on JS divergence thresholds.
    """
    seq_a = inputs.get("sequences_a") or inputs.get("sequences") or []
    seq_b = inputs.get("sequences_b") or []
    fm_a = inputs.get("freq_map_a") or inputs.get("freq_map") or (
        _freq_map_from_sequences(seq_a) if seq_a else {}
    )
    fm_b = inputs.get("freq_map_b") or (
        _freq_map_from_sequences(seq_b) if seq_b else {}
    )

    label_a = str(params.get("label_a", "corpus_a"))
    label_b = str(params.get("label_b", "corpus_b"))
    top_n = int(params.get("top_n", 20))

    if not fm_a or not fm_b:
        return {"error": "Need two corpora: connect sequences_a + sequences_b or freq_map_a + freq_map_b."}

    result = _kl_js(fm_a, fm_b, top_n=top_n)

    # Verdict based on JS divergence
    js = result["js_divergence"]
    if js < 0.3:
        verdict = "STRONG_CONTACT"
        verdict_text = (
            f"Strong contact signal between {label_a} and {label_b}: "
            f"JS divergence {js:.4f} < 0.3 with {result['n_shared']} shared symbols."
        )
    elif js < 0.6:
        verdict = "MODERATE_CONTACT"
        verdict_text = (
            f"Moderate contact signal between {label_a} and {label_b}: "
            f"JS divergence {js:.4f}. {result['n_shared']} shared symbols."
        )
    else:
        verdict = "WEAK_CONTACT"
        verdict_text = (
            f"Weak/no contact signal between {label_a} and {label_b}: "
            f"JS divergence {js:.4f} >= 0.6."
        )

    return {
        **result,
        "label_a": label_a,
        "label_b": label_b,
        "verdict": verdict,
        "verdict_text": verdict_text,
        "number": round(js, 6),
    }


# ── Node 2: ContactZoneSynthesis ─────────────────────────────────────────


def _contact_zone_synthesis(inputs: dict, params: dict) -> dict:
    """Synthesise outputs from multiple KL comparisons.

    Takes a list of KL divergence results (wired from multiple
    ContactZoneKLDivergence nodes via Merger) and ranks which
    language families show the highest contact signal with the
    target corpus.
    """
    # Collect all upstream KL results.  They may arrive as individual
    # keys (a, b, c, …) from a Merger or as a list under "comparisons".
    comparisons: list[dict] = []
    if "comparisons" in inputs and isinstance(inputs["comparisons"], list):
        comparisons = inputs["comparisons"]
    else:
        for _k, v in sorted(inputs.items()):
            if isinstance(v, dict) and "js_divergence" in v:
                comparisons.append(v)

    if not comparisons:
        return {"error": "No KL comparison results — connect ContactZoneKLDivergence outputs."}

    # Rank by JS divergence (lower = stronger contact)
    ranked = sorted(comparisons, key=lambda c: c.get("js_divergence", 999))
    top_n = int(params.get("top_n", 10))

    summary = []
    for i, c in enumerate(ranked[:top_n]):
        summary.append({
            "rank": i + 1,
            "label_a": c.get("label_a", "?"),
            "label_b": c.get("label_b", "?"),
            "js_divergence": c.get("js_divergence"),
            "kl_divergence": c.get("kl_divergence"),
            "n_shared": c.get("n_shared"),
            "overlap_ratio": c.get("overlap_ratio"),
            "verdict": c.get("verdict"),
        })

    strongest = ranked[0] if ranked else {}
    verdict_text = (
        f"Contact synthesis: {len(comparisons)} comparisons ranked. "
        f"Strongest contact: {strongest.get('label_b', '?')} "
        f"(JS={strongest.get('js_divergence', '?'):.4f}, "
        f"{strongest.get('n_shared', 0)} shared symbols)."
    ) if strongest else "No comparisons available."

    return {
        "ranked_summary": summary,
        "n_comparisons": len(comparisons),
        "strongest_contact": strongest.get("label_b", ""),
        "strongest_js": strongest.get("js_divergence"),
        "verdict": verdict_text,
        "json": {"ranked_summary": summary},
    }


# ── Node 3: ContactZoneABComparison ──────────────────────────────────────


def _contact_zone_ab_comparison(inputs: dict, params: dict) -> dict:
    """Compare two corpora A and B against Indus, return which has stronger contact signal.

    Inputs:
      sequences_indus — Indus corpus sequences
      sequences_a     — corpus A sequences (e.g. Dravidian)
      sequences_b     — corpus B sequences (e.g. Sumerian)

    Returns which corpus shows stronger contact with Indus.
    """
    seq_indus = inputs.get("sequences_indus") or inputs.get("sequences") or []
    seq_a = inputs.get("sequences_a") or []
    seq_b = inputs.get("sequences_b") or []

    label_a = str(params.get("label_a", "corpus_a"))
    label_b = str(params.get("label_b", "corpus_b"))
    top_n = int(params.get("top_n", 15))

    if not seq_indus:
        return {"error": "No Indus sequences — connect CorpusReader or BuiltinCorpus."}
    if not seq_a and not seq_b:
        return {"error": "Need at least one comparison corpus (sequences_a or sequences_b)."}

    fm_indus = _freq_map_from_sequences(seq_indus)

    result_a = _kl_js(fm_indus, _freq_map_from_sequences(seq_a), top_n) if seq_a else None
    result_b = _kl_js(fm_indus, _freq_map_from_sequences(seq_b), top_n) if seq_b else None

    js_a = result_a["js_divergence"] if result_a else 999.0
    js_b = result_b["js_divergence"] if result_b else 999.0

    if js_a < js_b:
        winner = label_a
        confidence = round(1.0 - js_a / max(js_b, 0.001), 4)
    elif js_b < js_a:
        winner = label_b
        confidence = round(1.0 - js_b / max(js_a, 0.001), 4)
    else:
        winner = "tie"
        confidence = 0.0

    verdict_text = (
        f"A/B contact comparison: {label_a} JS={js_a:.4f} vs {label_b} JS={js_b:.4f}. "
        f"Winner: {winner} (confidence={confidence:.2%})."
    )

    return {
        "winner": winner,
        "confidence": confidence,
        "label_a": label_a,
        "label_b": label_b,
        "js_a": js_a,
        "js_b": js_b,
        "result_a": result_a,
        "result_b": result_b,
        "verdict": verdict_text,
    }


# ── Registration ─────────────────────────────────────────────────────────


def _contact_zone_node_defs() -> list:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "ContactZoneKLDivergence", "Contact Zone KL Divergence",
            "Contact Zone",
            "Compute KL and JS divergence between two corpus symbol distributions. "
            "Returns divergence score, top-N overlapping symbols, and contact verdict.",
            inputs=[
                {"name": "sequences_a", "type": "sequences", "required": False},
                {"name": "sequences_b", "type": "sequences", "required": False},
                {"name": "freq_map_a", "type": "freq_map", "required": False},
                {"name": "freq_map_b", "type": "freq_map", "required": False},
            ],
            outputs=[
                {"name": "kl_divergence", "type": "number"},
                {"name": "js_divergence", "type": "number"},
                {"name": "top_overlap", "type": "json"},
                {"name": "verdict", "type": "text"},
                {"name": "number", "type": "number"},
            ],
            params_schema={"type": "object", "properties": {
                "label_a": {"type": "string", "default": "corpus_a"},
                "label_b": {"type": "string", "default": "corpus_b"},
                "top_n": {"type": "integer", "default": 20, "minimum": 1},
            }},
            fn=_contact_zone_kl_divergence,
        ),
        AtomicNodeDef(
            "ContactZoneSynthesis", "Contact Zone Synthesis",
            "Contact Zone",
            "Synthesise multiple KL divergence comparisons into a ranked summary "
            "of which language families show highest contact signal with the target corpus.",
            inputs=[
                {"name": "comparisons", "type": "json", "required": False},
                {"name": "a", "type": "any", "required": False},
                {"name": "b", "type": "any", "required": False},
                {"name": "c", "type": "any", "required": False},
                {"name": "d", "type": "any", "required": False},
            ],
            outputs=[
                {"name": "ranked_summary", "type": "json"},
                {"name": "strongest_contact", "type": "text"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {
                "top_n": {"type": "integer", "default": 10, "minimum": 1},
            }},
            fn=_contact_zone_synthesis,
        ),
        AtomicNodeDef(
            "ContactZoneABComparison", "Contact Zone A/B Comparison",
            "Contact Zone",
            "Compare two corpora A and B against Indus to determine which shows "
            "stronger contact signal. Returns winner, confidence, and per-corpus divergence.",
            inputs=[
                {"name": "sequences_indus", "type": "sequences", "required": True},
                {"name": "sequences_a", "type": "sequences", "required": False},
                {"name": "sequences_b", "type": "sequences", "required": False},
            ],
            outputs=[
                {"name": "winner", "type": "text"},
                {"name": "confidence", "type": "number"},
                {"name": "verdict", "type": "text"},
                {"name": "result_a", "type": "json"},
                {"name": "result_b", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {
                "label_a": {"type": "string", "default": "corpus_a"},
                "label_b": {"type": "string", "default": "corpus_b"},
                "top_n": {"type": "integer", "default": 15, "minimum": 1},
            }},
            fn=_contact_zone_ab_comparison,
        ),
    ]

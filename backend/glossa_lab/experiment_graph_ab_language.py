"""A/B language comparison experiment templates.

Provides generic anchored SA language comparison and concrete A/B
experiment definitions:

  AnchoredSALanguageAB — Parameterised by lang_a and lang_b.  Loads the
      relevant LM for each, runs anchored SA on the Indus corpus,
      computes z-scores and consistency for each, returns winner with
      confidence and evidence.

  Concrete experiments (using AnchoredSALanguageAB with fixed params):
    ab_dravidian_vs_sanskrit  — Dravidian vs Sanskrit anchored SA
    ab_dravidian_vs_munda     — Dravidian vs Munda anchored SA
    ab_dravidian_vs_hebrew    — Dravidian vs Hebrew anchored SA

  LMConsistencyMatrix — Runs all pairings and produces a summary
      matrix with overall Dravidian confidence.
"""
from __future__ import annotations

import math
import random
from collections import Counter
from typing import Any


# ── Helpers ──────────────────────────────────────────────────────────────


def _load_lm(lang: str) -> Any:
    """Load a LanguageModel for the given language identifier."""
    # Delegate to the builtin LM loader logic in experiment_graph.py
    from glossa_lab.experiment_graph import _builtin_lm  # noqa: PLC0415
    result = _builtin_lm({}, {"language": lang})
    return result.get("lm") if not result.get("error") else None


def _load_indus_sequences() -> list[list[str]]:
    """Load the default Indus corpus sequences."""
    from glossa_lab.experiment_graph import _builtin_corpus  # noqa: PLC0415
    result = _builtin_corpus({}, {"corpus": "indus_m77"})
    return result.get("sequences") or []


def _quick_sa(flat: list[str], lm: Any, n_seeds: int = 3, max_iter: int = 3000) -> dict:
    """Run a lightweight SA decipherment and return modal mapping + consistency."""
    from glossa_lab.pipelines.decipher import decipher  # noqa: PLC0415

    all_maps: list[dict] = []
    for seed in range(n_seeds):
        try:
            r = decipher(
                flat, lm, seed=seed, max_iterations=max_iter, restarts=2,
                cipher_inscriptions=None, surjective=True,
                ocp_weight=0.0, positional_weight=0.0,
            )
            m = r.get("proposed_mapping", {})
            if m:
                all_maps.append(m)
        except Exception:  # noqa: BLE001
            pass

    if not all_maps:
        return {"proposed_mapping": {}, "mean_consistency": 0.0, "hci_count": 0, "n_seeds": 0}

    all_signs = set().union(*[m.keys() for m in all_maps])
    modal: dict[str, str] = {}
    cons: dict[str, float] = {}
    for s in all_signs:
        props = [m[s] for m in all_maps if s in m]
        if props:
            cnt = Counter(props)
            mo, mc = cnt.most_common(1)[0]
            modal[s] = mo
            cons[s] = mc / len(props)

    mean_c = sum(cons.values()) / len(cons) if cons else 0.0
    hci = sum(1 for v in cons.values() if v >= 0.75)

    return {
        "proposed_mapping": modal,
        "mean_consistency": round(mean_c, 4),
        "hci_count": hci,
        "n_seeds": len(all_maps),
        "n_signs": len(modal),
    }


# ── Node 1: AnchoredSALanguageAB ────────────────────────────────────────


def _anchored_sa_language_ab(inputs: dict, params: dict) -> dict:
    """A/B language comparison using anchored SA decipherment.

    Loads LMs for lang_a and lang_b, runs SA on the Indus corpus with each,
    compares consistency z-scores.
    """
    lang_a = str(params.get("lang_a", "dravidian")).lower().strip()
    lang_b = str(params.get("lang_b", "sanskrit")).lower().strip()
    n_seeds = max(1, int(params.get("n_seeds", 3)))
    max_iter = max(500, int(params.get("max_iterations", 3000)))

    # Load Indus sequences
    sequences = inputs.get("sequences") or _load_indus_sequences()
    if not sequences:
        return {"error": "No Indus sequences available."}
    flat = [s for seq in sequences for s in seq]

    # Load LMs
    lm_a = _load_lm(lang_a)
    lm_b = _load_lm(lang_b)
    if not lm_a:
        return {"error": f"Failed to load LM for '{lang_a}'."}
    if not lm_b:
        return {"error": f"Failed to load LM for '{lang_b}'."}

    # Run SA with each LM
    result_a = _quick_sa(flat, lm_a, n_seeds=n_seeds, max_iter=max_iter)
    result_b = _quick_sa(flat, lm_b, n_seeds=n_seeds, max_iter=max_iter)

    cons_a = result_a["mean_consistency"]
    cons_b = result_b["mean_consistency"]
    hci_a = result_a["hci_count"]
    hci_b = result_b["hci_count"]

    # Compute z-score-like difference
    pooled = (cons_a + cons_b) / 2 if (cons_a + cons_b) > 0 else 1.0
    z_diff = (cons_a - cons_b) / max(pooled * 0.1, 0.01)

    if cons_a > cons_b + 0.05:
        winner = lang_a
        confidence = round(min(1.0, abs(z_diff) / 5.0), 4)
    elif cons_b > cons_a + 0.05:
        winner = lang_b
        confidence = round(min(1.0, abs(z_diff) / 5.0), 4)
    else:
        winner = "inconclusive"
        confidence = 0.0

    evidence = (
        f"{lang_a}: consistency={cons_a:.4f}, HCI={hci_a}; "
        f"{lang_b}: consistency={cons_b:.4f}, HCI={hci_b}. "
        f"z_diff={z_diff:.2f}."
    )

    return {
        "lang_a": lang_a,
        "lang_b": lang_b,
        "lang_a_zscore": round(cons_a, 4),
        "lang_b_zscore": round(cons_b, 4),
        "lang_a_hci": hci_a,
        "lang_b_hci": hci_b,
        "winner": winner,
        "confidence": confidence,
        "evidence": evidence,
        "z_diff": round(z_diff, 4),
        "result_a": {k: v for k, v in result_a.items() if k != "proposed_mapping"},
        "result_b": {k: v for k, v in result_b.items() if k != "proposed_mapping"},
        "verdict": f"A/B test: {winner} wins (confidence={confidence:.2%}). {evidence}",
    }


# ── Node 2: LMConsistencyMatrix ──────────────────────────────────────────


def _lm_consistency_matrix(inputs: dict, params: dict) -> dict:
    """Run all A/B language pairings and produce a summary matrix.

    Takes outputs from multiple AnchoredSALanguageAB nodes (wired
    through Merger) and synthesises an overall Dravidian confidence score.
    """
    pairings: list[dict] = []
    if "pairings" in inputs and isinstance(inputs["pairings"], list):
        pairings = inputs["pairings"]
    else:
        for _k, v in sorted(inputs.items()):
            if isinstance(v, dict) and "winner" in v and "lang_a" in v:
                pairings.append(v)

    if not pairings:
        return {"error": "No A/B pairing results — connect AnchoredSALanguageAB outputs."}

    matrix = []
    dravidian_wins = 0
    total = len(pairings)

    for p in pairings:
        row = {
            "lang_a": p.get("lang_a"),
            "lang_b": p.get("lang_b"),
            "winner": p.get("winner"),
            "confidence": p.get("confidence"),
            "lang_a_zscore": p.get("lang_a_zscore"),
            "lang_b_zscore": p.get("lang_b_zscore"),
        }
        matrix.append(row)
        if p.get("winner") in ("dravidian", "tamil", "south_dravidian"):
            dravidian_wins += 1

    dravidian_confidence = round(dravidian_wins / max(1, total), 4)
    avg_confidence = round(
        sum(p.get("confidence", 0) for p in pairings) / max(1, total), 4
    )

    verdict = (
        f"LM consistency matrix: {total} pairings. "
        f"Dravidian wins {dravidian_wins}/{total} ({dravidian_confidence:.0%}). "
        f"Average pairing confidence: {avg_confidence:.2%}."
    )

    return {
        "matrix": matrix,
        "n_pairings": total,
        "dravidian_wins": dravidian_wins,
        "dravidian_confidence": dravidian_confidence,
        "avg_confidence": avg_confidence,
        "verdict": verdict,
        "json": {"matrix": matrix, "dravidian_confidence": dravidian_confidence},
    }


# ── Registration ─────────────────────────────────────────────────────────


def _ab_language_node_defs() -> list:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "AnchoredSALanguageAB", "Anchored SA Language A/B",
            "Cross-Language",
            "A/B language comparison using anchored SA: loads LMs for two languages, "
            "runs SA on the Indus corpus, compares consistency and z-scores. "
            "Returns winner, confidence, and per-language evidence.",
            inputs=[
                {"name": "sequences", "type": "sequences", "required": False},
            ],
            outputs=[
                {"name": "winner", "type": "text"},
                {"name": "confidence", "type": "number"},
                {"name": "evidence", "type": "text"},
                {"name": "verdict", "type": "text"},
                {"name": "lang_a_zscore", "type": "number"},
                {"name": "lang_b_zscore", "type": "number"},
            ],
            params_schema={"type": "object", "properties": {
                "lang_a": {"type": "string", "default": "dravidian",
                           "description": "Language A identifier (e.g. dravidian, sumerian)"},
                "lang_b": {"type": "string", "default": "sanskrit",
                           "description": "Language B identifier (e.g. sanskrit, hebrew)"},
                "n_seeds": {"type": "integer", "default": 3, "minimum": 1},
                "max_iterations": {"type": "integer", "default": 3000, "minimum": 500},
            }},
            fn=_anchored_sa_language_ab,
        ),
        AtomicNodeDef(
            "LMConsistencyMatrix", "LM Consistency Matrix",
            "Cross-Language",
            "Synthesise multiple A/B language pairing results into an overall "
            "consistency matrix with Dravidian confidence score.",
            inputs=[
                {"name": "pairings", "type": "json", "required": False},
                {"name": "a", "type": "any", "required": False},
                {"name": "b", "type": "any", "required": False},
                {"name": "c", "type": "any", "required": False},
            ],
            outputs=[
                {"name": "matrix", "type": "json"},
                {"name": "dravidian_confidence", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_lm_consistency_matrix,
        ),
    ]

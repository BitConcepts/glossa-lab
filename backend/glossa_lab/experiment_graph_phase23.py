"""Phase-23 atomic-node implementations.

Phase-23 builds on the Phase-22 contact-zone corpus to attempt the
first quantitative bilingual analysis. Three sub-experiments:

  Experiment 23a — Seal sign audit
      RefinedSealLoader -> SealSignAuditor -> JSONExport.
      Reports the inscription_length distribution across the 13
      Indus seals catalogued at Mesopotamia, the confidence-tier
      breakdown, and the per-seal sign-source citations.

  Experiment 23b — Refined Meluhhan-name extraction
      RefinedSealLoader -> RefinedMeluhhanPersonsExtractor -> JSONExport.
      Strict Sumerian-PN heuristic (lu2-/lu-/dumu- prefix OR
      -me-luh-ha-ki suffix) with a 100+ entry Akkadian particle /
      Sumerian function-word stoplist. Replaces Phase-22b which
      surfaced mostly noise.

  Experiment 23c — Bilingual readout test
      RefinedSealLoader -> EnhancedNameMatcher -> BilingualReadoutTest -> JSONExport.
      Runs a permutation test on the name-to-seal pairings: for each
      candidate name, score the best length-compatible seal; permute
      the name labels N times and recompute the score; the p-value is
      the fraction of permutations whose best score equals or exceeds
      the observed score. The falsifiable readout test the strategy
      review demanded.

  Phase23Verdict aggregates the three into a single contact-zone
  decipherment-progress verdict.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

# ── Helpers ───────────────────────────────────────────────────────────


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:  # noqa: BLE001
        return default


# ── Loaders ───────────────────────────────────────────────────────────


def _refined_seal_loader(inputs: dict, params: dict) -> dict:
    """Load Phase-23 augmented seals + refined persons."""
    try:
        from glossa_lab.data.mesopotamian_contact import (  # noqa: PLC0415
            get_indus_seals_at_mesopotamia,
            get_meluhhan_persons_strict,
            get_seal_sign_metadata,
            get_seals_with_inscription,
        )
    except Exception as exc:  # noqa: BLE001
        return {"error": f"data module not available: {exc}"}

    all_seals = get_indus_seals_at_mesopotamia()
    inscribed_seals = get_seals_with_inscription()
    sign_metadata = get_seal_sign_metadata()
    strict_persons = get_meluhhan_persons_strict()

    return {
        "all_seals": all_seals,
        "inscribed_seals": inscribed_seals,
        "n_seals_total": len(all_seals),
        "n_seals_inscribed": len(inscribed_seals),
        "sign_metadata": sign_metadata,
        "strict_persons": strict_persons,
        "n_strict_persons": len(strict_persons),
    }


# ── Reporters ─────────────────────────────────────────────────────────


def _seal_sign_auditor(inputs: dict, params: dict) -> dict:
    """Distribution of inscription_length and confidence tiers.

    Spec 087 S3 PR-F: delegates to the generic RecordGroupSummary;
    the per-record safe-int length / falsy-defaulted confidence, the
    key-sorted length counter and the verdict text are spec data.
    """
    from glossa_lab.generic_primitives import record_group_summary_execute

    merged = dict(params)
    merged["summary_spec"] = {
        "records_key": "all_seals",
        "record_fields": [
            {"name": "n", "from": "inscription_length", "safe_int": True},
            {"name": "conf", "from": "signs_confidence",
             "missing": "falsy_default", "default": "unknown"},
        ],
        "blocks": [
            {"kind": "count", "out": "n_seals"},
            {"kind": "sum", "out": "total_indus_signs", "computed": "n"},
            {"kind": "counter", "out": "by_confidence", "computed": "conf",
             "order": "most_common"},
            {"kind": "counter", "out": "by_length", "computed": "n",
             "order": "sorted"},
            {"kind": "rows", "out": "rows", "fields": [
                {"out": "catalogue_id", "from": "catalogue_id"},
                {"out": "find_country", "from": "find_country"},
                {"out": "inscription_length", "computed": "n"},
                {"out": "signs_confidence", "computed": "conf"},
                {"out": "signs_source", "from": "signs_source"},
            ]},
            {"kind": "derived_rows", "out": "inscribed_rows", "from": "rows",
             "where": {"field": "inscription_length", "op": ">", "value": 0}},
            {"kind": "count_of", "out": "n_inscribed", "from": "inscribed_rows"},
            {"kind": "input_field", "out": "method",
             "input_key": "sign_metadata", "field": "method", "default": ""},
            {"kind": "verdict", "out": "verdict",
             "template": (
                 "Phase-23 seal-sign audit: {n_seals} seals; "
                 "{n_inscribed} carry Indus signs ({total_indus_signs} "
                 "total). Confidence tiers: {by_confidence}.")},
        ],
    }
    return record_group_summary_execute(inputs, merged)


def _refined_persons_extractor(inputs: dict, params: dict) -> dict:
    """Aggregate the strict Phase-23 PN extractor output.

    Spec 087 S3 (family F6): the mechanism is the generic
    PersonsAggregator engine (glossa_lab.generic_primitives); this
    node is its Phase-23 parameterisation — the strict_persons
    port, provenience + source-pattern + distinct-tablet
    collection, example lines untruncated, the by-pattern
    distribution over all rows, and known-name confirmation taken
    from the upstream rows' is_known flag (the known set moved
    upstream), all carried as spec data.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        persons_aggregator_execute,
    )

    merged = dict(params)
    merged["persons_spec"] = {
        "input_key": "strict_persons",
        "collect_proveniences": True,
        "collect_patterns": True,
        "distinct_tablets": True,
        "known": {"mode": "upstream_flag"},
        "by_pattern": True,
        "extra_count_key": "n_total",
        "n_key": "n_unique",
        "verdict_template": (
            "Refined Meluhhan-PN extractor (Phase-23): "
            "{n_rows} unique name candidates (freq>={min_freq}); "
            "{n_confirmed} historically-confirmed; "
            "by-pattern distribution {by_pattern}."
        ),
    }
    return persons_aggregator_execute(inputs, merged)


# ── Enhanced matcher ──────────────────────────────────────────────────


def _enhanced_name_matcher(inputs: dict, params: dict) -> dict:
    """Score name <-> seal pairings using inscription_length.

    Phase-23 difference vs Phase-22c: now operates on the
    *strict* persons output (low-noise) and the *augmented* seals
    (inscription_length > 0 for 10/13 seals).

    Spec 087 S3 (family F5): the mechanism is the generic
    LengthMatchScorer engine (glossa_lab.generic_primitives) in its
    all_pairs mode; this node is its Phase-23 parameterisation. The
    segment counter and the tolerance length score are shared with
    the rest of the family inside the engine.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        length_match_scorer_execute,
    )

    merged = dict(params)
    merged["matcher_spec"] = {
        "assignment": "all_pairs",
        "score_spec": {"kind": "tolerance"},
        "min_name_freq_default": 2,
        "verdict_template": (
            "Enhanced matcher (Phase-23): {n_pairings} length-compatible "
            "pairings between {n_seals} inscribed seals and "
            "{n_candidates} strict-PN candidates (freq>={min_name_freq}, "
            "tol={tolerance})."
        ),
        "insufficient_template": (
            "Enhanced matcher: insufficient inputs "
            "(candidates={n_candidates}, inscribed_seals={n_seals})."
        ),
    }
    return length_match_scorer_execute(inputs, merged)


# ── Bilingual readout test (permutation) ──────────────────────────────


def _bilingual_readout_test(inputs: dict, params: dict) -> dict:
    """Permutation p-value on the observed name<->seal length match.

    Test statistic
    ---------------
    For each candidate name, take the *best* length_score against all
    inscribed seals; sum across names. This is the "observed" score.

    Null distribution
    -----------------
    For each of N permutations, randomly permute the inscription_length
    values across the seals (preserving the multiset of lengths) and
    recompute the same statistic. The p-value is the fraction of
    permutations whose statistic equals or exceeds the observed value.

    Why this is the right test
    --------------------------
    The strategy review asked for a falsifiable bilingual moment. A
    significant p-value here means: the *specific* mapping of name
    lengths to seal lengths in our data is unlikely under a null where
    seals carry random Indus-sign counts. That's a length-only signal,
    not a phonetic one — Phase-24 will need the actual sign IDs to
    upgrade the test to a phonetic one.

    Spec 087 S3 (family F5): the mechanism is the generic
    LengthMatchPermutationTest engine (glossa_lab.generic_primitives)
    in its best_match statistic mode; this node is its Phase-23
    parameterisation (permutation floor 100, seed 42).
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        length_match_permutation_test_execute,
    )

    merged = dict(params)
    merged.setdefault("seed", 42)
    merged["test_spec"] = {
        "statistic": "best_match",
        "n_permutations_default": 1000,
        "min_name_freq_default": 2,
        "insufficient_verdict": "INSUFFICIENT_DATA: cannot run readout test",
        "interpretation": (
            "Length-only test: a significant p means the observed "
            "name-length-to-seal-length distribution is unlikely under "
            "shuffled-length null. Phase-24 needs sign IDs (not just "
            "lengths) to upgrade to a phonetic readout."
        ),
    }
    return length_match_permutation_test_execute(inputs, merged)


# ── Verdict aggregator ────────────────────────────────────────────────


def _phase23_verdict(inputs: dict, params: dict) -> dict:
    n_seals = _safe_int(inputs.get("n_inscribed"))
    total_signs = _safe_int(inputs.get("total_indus_signs"))
    n_persons = _safe_int(inputs.get("n_unique"))
    n_confirmed = len(inputs.get("confirmed_hits") or [])
    n_pairings = _safe_int(inputs.get("n_pairings"))
    p_value = inputs.get("p_value")
    readout_verdict = inputs.get("readout_verdict") or ""

    summary = (
        f"Phase-23 contact-zone decipherment progress: "
        f"{n_seals} inscribed seals ({total_signs} signs), "
        f"{n_persons} strict-PN candidates "
        f"({n_confirmed} historically-confirmed), "
        f"{n_pairings} length-compatible pairings; "
        f"readout p={p_value} ({readout_verdict})."
    )

    next_steps: list[str] = []
    if total_signs > 0 and any("?" in str(p_value) for _ in [0]) is False:
        # Always include sign-ID upgrade as priority 1
        pass
    next_steps.append(
        "Phase-24 priority 1: upgrade indus_signs[] from '?' "
        "placeholders to actual Parpola/Mahadevan IDs (CISI Vol 3, "
        "Frenez 2018 plate IV, Ascalone 2008). Required for any "
        "phonetic readout."
    )
    if n_confirmed == 0:
        next_steps.append(
            "Phase-24 priority 2: extend the strict-PN regex to "
            "match additional historically-attested Meluhhan PN "
            "patterns (Ur-suen-me-luh-ha, Sheshkalla-me-luh-ha, "
            "Ur-Lamma-Meluhha)."
        )
    next_steps.append(
        "Phase-24 priority 3: phonetic readout test \u2014 once sign "
        "IDs land, score name<->seal pairings under a candidate "
        "Indus-to-Sumerian phoneme map and re-run the permutation "
        "test on that signal."
    )

    return {
        "summary": summary,
        "n_seals": n_seals,
        "total_signs": total_signs,
        "n_persons": n_persons,
        "n_confirmed_persons": n_confirmed,
        "n_pairings": n_pairings,
        "readout_p_value": p_value,
        "readout_verdict": readout_verdict,
        "next_steps": next_steps,
        "verdict": (
            "READOUT_SIGNIFICANT" if isinstance(p_value, (int, float))
            and p_value < 0.05 else
            "INSUFFICIENT_OR_NOT_SIGNIFICANT"
        ),
    }


# ── Atomic node defs for registration ─────────────────────────────────


def _phase23_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "RefinedSealLoader", "Refined Seal + Persons Loader (Phase-23)",
            "Phase-23 / Sources",
            "Load the Phase-23 augmented Indus-seals-at-Mesopotamia "
            "inventory (with inscription_length + indus_signs[]) and "
            "the strict Meluhhan-PN extraction (lu2-/dumu- prefix or "
            "-me-luh-ha-ki suffix; Akkadian particle stoplist).",
            inputs=[],
            outputs=[
                {"name": "all_seals", "type": "json"},
                {"name": "inscribed_seals", "type": "json"},
                {"name": "n_seals_total", "type": "number"},
                {"name": "n_seals_inscribed", "type": "number"},
                {"name": "sign_metadata", "type": "json"},
                {"name": "strict_persons", "type": "json"},
                {"name": "n_strict_persons", "type": "number"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_refined_seal_loader,
        ),
        AtomicNodeDef(
            "SealSignAuditor", "Seal Sign Auditor (Phase-23)",
            "Phase-23 / Reporters",
            "Audit inscription_length distribution + signs_confidence "
            "tiers across the Indus-seals-at-Mesopotamia inventory.",
            inputs=[
                {"name": "all_seals", "type": "json", "required": True},
                {"name": "sign_metadata", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "n_seals", "type": "number"},
                {"name": "n_inscribed", "type": "number"},
                {"name": "total_indus_signs", "type": "number"},
                {"name": "by_confidence", "type": "json"},
                {"name": "by_length", "type": "json"},
                {"name": "rows", "type": "json"},
                {"name": "inscribed_rows", "type": "json"},
                {"name": "method", "type": "text"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_seal_sign_auditor,
        ),
        AtomicNodeDef(
            "RefinedMeluhhanPersonsExtractor",
            "Refined Meluhhan Persons Extractor (Phase-23)",
            "Phase-23 / Reporters",
            "Aggregate the strict Phase-23 PN extractor: rejects "
            "Akkadian particles via stoplist; accepts only lu2-/lu-/"
            "dumu- prefixed or -me-luh-ha-ki suffixed candidates plus "
            "the historically-attested Meluhhan-name set (Lu-sun-zi-"
            "da, Shu-ilishu).",
            inputs=[
                {"name": "strict_persons", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_unique", "type": "number"},
                {"name": "rows_top50", "type": "json"},
                {"name": "rows_all", "type": "json"},
                {"name": "n_total", "type": "number"},
                {"name": "confirmed_hits", "type": "json"},
                {"name": "by_pattern", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_freq": {"type": "integer", "default": 1, "minimum": 1},
                },
            },
            fn=_refined_persons_extractor,
        ),
        AtomicNodeDef(
            "EnhancedNameMatcher", "Enhanced Name Matcher (Phase-23)",
            "Phase-23 / Decipherment",
            "Score name<->seal pairings using inscription_length on "
            "10 inscribed Mesopotamia-found Indus seals against the "
            "strict-PN candidate list. Sets up the test statistic for "
            "BilingualReadoutTest.",
            inputs=[
                {"name": "rows_all", "type": "json", "required": True},
                {"name": "inscribed_seals", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_candidates", "type": "number"},
                {"name": "n_seals", "type": "number"},
                {"name": "pairings", "type": "json"},
                {"name": "pairings_top50", "type": "json"},
                {"name": "n_pairings", "type": "number"},
                {"name": "best_per_name", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_name_freq": {"type": "integer", "default": 2, "minimum": 1},
                    "tolerance": {"type": "integer", "default": 2, "minimum": 0,
                                  "description": "Max |n_signs - name_n_segments| for non-zero score."},
                },
            },
            fn=_enhanced_name_matcher,
        ),
        AtomicNodeDef(
            "BilingualReadoutTest", "Bilingual Readout Test (Phase-23)",
            "Phase-23 / Decipherment",
            "Permutation test on the observed name<->seal length match. "
            "Statistic: sum of best-length-scores across candidate "
            "names. Null: shuffled inscription_length assignment. The "
            "first falsifiable bilingual contact-zone test.",
            inputs=[
                {"name": "rows_all", "type": "json", "required": True},
                {"name": "inscribed_seals", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "verdict", "type": "text"},
                {"name": "p_value", "type": "number"},
                {"name": "observed", "type": "number"},
                {"name": "null_mean", "type": "number"},
                {"name": "null_sd", "type": "number"},
                {"name": "z_score", "type": "number"},
                {"name": "n_permutations", "type": "number"},
                {"name": "n_candidates", "type": "number"},
                {"name": "n_seals", "type": "number"},
                {"name": "interpretation", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "n_permutations": {"type": "integer", "default": 1000,
                                        "minimum": 100},
                    "min_name_freq": {"type": "integer", "default": 2, "minimum": 1},
                    "tolerance": {"type": "integer", "default": 2, "minimum": 0},
                    "seed": {"type": "integer", "default": 42},
                },
            },
            fn=_bilingual_readout_test,
        ),
        AtomicNodeDef(
            "Phase23Verdict", "Phase-23 Verdict Aggregator",
            "Phase-23 / Reporters",
            "Aggregate the Phase-23 sub-experiment outputs (sign "
            "audit, refined persons, enhanced matcher, readout test) "
            "into a single contact-zone decipherment-progress verdict "
            "+ Phase-24 priority list.",
            inputs=[
                {"name": "n_inscribed", "type": "number", "required": False},
                {"name": "total_indus_signs", "type": "number", "required": False},
                {"name": "n_unique", "type": "number", "required": False},
                {"name": "confirmed_hits", "type": "json", "required": False},
                {"name": "n_pairings", "type": "number", "required": False},
                {"name": "p_value", "type": "number", "required": False},
                {"name": "readout_verdict", "type": "text", "required": False},
            ],
            outputs=[
                {"name": "summary", "type": "text"},
                {"name": "n_seals", "type": "number"},
                {"name": "total_signs", "type": "number"},
                {"name": "n_persons", "type": "number"},
                {"name": "n_confirmed_persons", "type": "number"},
                {"name": "n_pairings", "type": "number"},
                {"name": "readout_p_value", "type": "number"},
                {"name": "readout_verdict", "type": "text"},
                {"name": "next_steps", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase23_verdict,
        ),
    ]


__all__ = [
    "_refined_seal_loader",
    "_seal_sign_auditor",
    "_refined_persons_extractor",
    "_enhanced_name_matcher",
    "_bilingual_readout_test",
    "_phase23_verdict",
    "_phase23_node_defs",
]

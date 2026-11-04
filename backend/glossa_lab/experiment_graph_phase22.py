"""Phase-22 atomic-node implementations.

Phase-22 introduces the *contact-zone anchor* corpus identified in
the Phase-21 forward analysis as the single biggest gap toward an
actual Indus decipherment. The pipeline is:

  Experiment 22a — CDLI Meluhha-mention audit
      ContactCorpusLoader -> MeluhhaCorpusReporter -> JSONExport.
      Reports the 1,462 cuneiform tablets that mention Meluhha /
      Magan / Dilmun / Guabba, broken down by period, provenience,
      and matched-keyword distribution.

  Experiment 22b — Meluhhan named-person extraction
      ContactCorpusLoader -> MeluhhanPersonsExtractor -> JSONExport.
      Heuristically pulls personal-name candidates from tablet lines
      that include "me-luh-ha". Surfaces names like "Lu-sun-zi-da"
      (the canonical "Man of the just buffalo cow" Indus-name
      candidate) for downstream name-matching.

  Experiment 22c — Indus-seal-at-Mesopotamia inventory
      IndusSealsAtMesopotamiaLoader -> ContactZoneSummary -> JSONExport.
      Reports the 13 hand-encoded Indus / Indus-related seals found
      in Mesopotamia, Iran and the Persian Gulf. Ties each artefact
      to its citing source so the Phase-23 work can prioritise
      bilingual / contact anchors.

  Experiment 22d — Meluhhan name <-> Indus-seal matcher (prototype)
      Combines persons + seals + Phase-21d numerical-class table to
      score candidate name <-> seal pairings by length and structural
      compatibility. First step toward a real bilingual anchor.

  Phase22Verdict aggregates the four into a single contact-zone
  inventory verdict.
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


# Spec 087 S3 (family F1): the generic DatasetRecordLoader spec for
# this node — the mesopotamian_contact getters, the two tablet
# filters, and the output assembly are data here, not code.
_CONTACT_DATASET_SPEC: dict[str, Any] = {
    "module": "glossa_lab.data.mesopotamian_contact",
    "getters": {
        "tablets_raw": {"name": "get_meluhha_tablets"},
        "keyword_counts": {"name": "get_meluhha_keyword_counts"},
        "period_counts": {"name": "get_meluhha_period_counts"},
        "provenience_counts": {"name": "get_meluhha_provenience_counts"},
        "seals": {"name": "get_indus_seals_at_mesopotamia"},
        "persons": {"name": "get_meluhhan_persons"},
    },
    "filters": [
        {
            "from": "tablets_raw",
            "as": "tablets",
            "rules": [
                {"kind": "substring_ci", "field": "period", "param": "period_filter"},
                {
                    "kind": "any_substring_ci",
                    "field": "matched_keywords",
                    "param": "keyword_filter",
                },
            ],
        }
    ],
    "outputs": [
        {"op": "value", "key": "tablets", "of": "tablets"},
        {"op": "len", "key": "n_tablets", "of": "tablets"},
        {"op": "value", "key": "keyword_counts", "of": "keyword_counts"},
        {"op": "value", "key": "period_counts", "of": "period_counts"},
        {"op": "value", "key": "provenience_counts", "of": "provenience_counts"},
        {"op": "value", "key": "seals_at_mesopotamia", "of": "seals"},
        {"op": "len", "key": "n_seals_at_mesopotamia", "of": "seals"},
        {"op": "value", "key": "persons", "of": "persons"},
        {"op": "len", "key": "n_persons", "of": "persons"},
    ],
}


def _contact_corpus_loader(inputs: dict, params: dict) -> dict:
    """Load the CDLI Meluhha-mention tablet corpus and the
    Indus-seals-at-Mesopotamia inventory.

    Spec 087 S3 (family F1): delegates to the generic
    DatasetRecordLoader engine with _CONTACT_DATASET_SPEC.
    """
    from glossa_lab.generic_loaders import dataset_record_loader_execute  # noqa: PLC0415

    merged = dict(params)
    merged["dataset_spec"] = _CONTACT_DATASET_SPEC
    return dataset_record_loader_execute(inputs, merged)


# ── Reporters ─────────────────────────────────────────────────────────


def _meluhha_corpus_reporter(inputs: dict, params: dict) -> dict:
    """Compact report on the loaded Meluhha-mention corpus.

    Spec 087 S3 PR-F: delegates to the generic RecordGroupSummary;
    the section specs (top-5 periods / top-10 provenience as data,
    most-mentioned projection) and the verdict text are spec data.
    """
    from glossa_lab.generic_primitives import record_group_summary_execute

    merged = dict(params)
    merged["summary_spec"] = {
        "records_key": "tablets",
        "blocks": [
            {"kind": "count", "out": "n_tablets"},
            {"kind": "input_len", "out": "n_keywords",
             "input_key": "keyword_counts"},
            {"kind": "input_echo", "out": "keyword_counts",
             "input_key": "keyword_counts", "default": {}},
            {"kind": "dict_top", "out": "top_5_periods",
             "input_key": "period_counts", "n": 5},
            {"kind": "dict_top", "out": "top_10_provenience",
             "input_key": "provenience_counts", "n": 10},
            {"kind": "records_top", "out": "most_mentioned_top10",
             "input_key": "tablets", "sort_field": "match_count", "n": 10,
             "fields": [
                 {"out": "p_number", "from": "p_number"},
                 {"out": "designation", "from": "designation"},
                 {"out": "period", "from": "period"},
                 {"out": "provenience", "from": "provenience"},
                 {"out": "match_count", "from": "match_count",
                  "safe_int": True},
                 {"out": "matched_keywords", "from": "matched_keywords"},
             ]},
            {"kind": "verdict", "out": "verdict",
             "template": (
                 "CDLI Meluhha audit: {n_tablets} tablets across "
                 "{n_input_period_counts} periods. Dominant period: "
                 "{top_5_periods_first_key} ({top_5_periods_first_value} "
                 "tablets). Dominant provenience: "
                 "{top_10_provenience_first_key} "
                 "({top_10_provenience_first_value} tablets).")},
        ],
    }
    return record_group_summary_execute(inputs, merged)


def _meluhhan_persons_extractor(inputs: dict, params: dict) -> dict:
    """Surface high-confidence Meluhhan name candidates.

    Spec 087 S3 (family F6): the mechanism is the generic
    PersonsAggregator engine (glossa_lab.generic_primitives); this
    node is its Phase-22 parameterisation — the persons port,
    provenience + distinct-tablet collection, example lines
    untruncated, and confirmation against the known historical
    Meluhhan names below, carried as a data param.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        persons_aggregator_execute,
    )

    merged = dict(params)
    merged["persons_spec"] = {
        "input_key": "persons",
        "collect_proveniences": True,
        "distinct_tablets": True,
        # The known historical Meluhhan names, highlighted in the
        # output (Lu-sun-zi-da, Shu-ilishu, …).
        "known": {
            "mode": "set",
            "names": [
                "lu-sun-zi-da", "lu2-sun-zi-da", "shu-ilishu",
                "shu-ilisu", "su-ilisu",
            ],
        },
        "rows_all": False,
        "extra_count_key": "all_rows_count",
        "n_key": "n_unique_candidates",
        "verdict_template": (
            "Meluhhan-person extractor: {n_rows} unique name "
            "candidates (freq >= {min_freq}); {n_confirmed} match "
            "historically-known Meluhhan-named persons "
            "(Lu-sun-zi-da, Shu-ilishu)."
        ),
    }
    return persons_aggregator_execute(inputs, merged)


def _indus_seals_at_mesopotamia_summary(inputs: dict, params: dict) -> dict:
    """Compact report on hand-encoded Indus seals found in
    Mesopotamia / Iran / Persian Gulf.

    Spec 087 S3 PR-F: delegates to the generic RecordGroupSummary;
    the three group counters ('(unknown)' defaults), the row
    projection and the verdict text are spec data.
    """
    from glossa_lab.generic_primitives import record_group_summary_execute

    merged = dict(params)
    merged["summary_spec"] = {
        "records_key": "seals_at_mesopotamia",
        "blocks": [
            {"kind": "count", "out": "n_seals"},
            {"kind": "counter", "out": "by_country", "field": "find_country",
             "default": "(unknown)", "order": "most_common"},
            {"kind": "counter", "out": "by_type", "field": "type",
             "default": "(unknown)", "order": "most_common"},
            {"kind": "counter", "out": "by_period", "field": "find_period",
             "default": "(unknown)", "order": "most_common"},
            {"kind": "rows", "out": "rows", "fields": [
                {"out": "catalogue_id", "from": "catalogue_id"},
                {"out": "type", "from": "type"},
                {"out": "find_country", "from": "find_country"},
                {"out": "find_spot", "from": "find_spot"},
                {"out": "find_period", "from": "find_period"},
                {"out": "current_collection", "from": "current_collection"},
                {"out": "inscription_reading", "from": "inscription_reading"},
                {"out": "source", "from": "source"},
            ]},
            {"kind": "verdict", "out": "verdict",
             "template": (
                 "Indus-seals-at-Mesopotamia inventory: {n_seals} seals "
                 "({len_by_country} countries, {len_by_type} types). "
                 "Dominant context: {dom_by_country}.")},
        ],
    }
    return record_group_summary_execute(inputs, merged)


# ── Name matcher (prototype) ──────────────────────────────────────────


def _meluhha_name_matcher(inputs: dict, params: dict) -> dict:
    """Score candidate Indus-seal-inscription <-> Meluhhan-name pairs.

    This is a *prototype* scorer. For a real bilingual anchor we'd
    need:
      - actual Indus-sign sequences for the Mesopotamia-found seals
        (currently most of our seals_at_mesopotamia entries have empty
        indus_signs lists pending CISI Vol 3 ingestion),
      - phonetic candidate values for those signs,
      - alignment against the Akkadian-rendered names.

    For now we score by:
      - sign count == hyphen count of the candidate name
      - presence of known Meluhhan-name regex matches
      - period overlap

    Spec 087 S3 (family F5): the mechanism is the generic
    LengthMatchScorer engine (glossa_lab.generic_primitives) in its
    aggregate_pairs mode; this node is its Phase-22 parameterisation.
    The node's divergent length falloff — 1 - |Δ|/5.0 with no
    tolerance, where the rest of the family uses the tolerance
    falloff — is carried as the named score spec
    "linear_falloff_divisor_5", pinned by the PR-C fixture: the
    conversion does not silently change it.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        length_match_scorer_execute,
    )

    merged = dict(params)
    merged["matcher_spec"] = {
        "assignment": "aggregate_pairs",
        "score_spec": {
            "kind": "linear",
            "divisor": 5.0,
            "name": "linear_falloff_divisor_5",
        },
        "min_name_freq_default": 2,
        "verdict_template": (
            "Name-matcher: {n_pairings} length-compatible pairings between "
            "{n_seals_with_signs} sign-bearing seals and "
            "{n_candidates} name candidates."
        ),
        "no_signs_template": (
            "PROTOTYPE STATUS: name-matcher cannot score yet because no "
            "Mesopotamia-found Indus seals have ingested sign sequences. "
            "Phase-23 must populate indus_signs[] from CISI Vol 3 / "
            "Frenez 2018 catalogue tables. "
            "Available: {n_candidates} name candidates "
            "(freq>={min_name_freq}); {n_seals_total} seals (none with signs)."
        ),
    }
    return length_match_scorer_execute(inputs, merged)


# ── Verdict aggregator ────────────────────────────────────────────────


def _phase22_verdict(inputs: dict, params: dict) -> dict:
    """Aggregate Phase-22 sub-experiment outputs into a single
    contact-zone inventory verdict.

    Accepts scalar inputs wired directly from upstream nodes:
      - n_tablets (from MeluhhaCorpusReporter.n_tablets)
      - n_persons (from MeluhhanPersonsExtractor.n_unique_candidates)
      - confirmed_hits (from MeluhhanPersonsExtractor.confirmed_hits)
      - n_seals (from IndusSealsAtMesopotamiaSummary.n_seals)
      - n_pairings (from MeluhhaNameMatcher.n_pairings)
    """
    n_tablets = _safe_int(inputs.get("n_tablets"))
    n_persons = _safe_int(inputs.get("n_persons"))
    confirmed_persons = inputs.get("confirmed_hits") or []
    if not isinstance(confirmed_persons, list):
        confirmed_persons = []
    n_seals = _safe_int(inputs.get("n_seals"))
    n_pairings = _safe_int(inputs.get("n_pairings"))

    summary = (
        f"Phase-22 contact-zone inventory: "
        f"{n_tablets} CDLI tablets, "
        f"{n_persons} Meluhhan-name candidates "
        f"({len(confirmed_persons)} historically-confirmed), "
        f"{n_seals} Indus seals at Mesopotamia, "
        f"{n_pairings} prototype seal-name pairings."
    )

    next_steps = []
    if n_pairings == 0:
        next_steps.append(
            "Phase-23 priority 1: populate indus_signs[] for the 13 "
            "Mesopotamia-found seals from CISI Vol 3 + Frenez 2018."
        )
    if not confirmed_persons:
        next_steps.append(
            "Phase-23 priority 2: tighten the Meluhhan-name regex to "
            "explicitly capture '-me-luh-ha-ki' suffix patterns and "
            "match the Lu-sun-zi-da / Shu-ilishu canonical names."
        )
    next_steps.append(
        "Phase-23 priority 3: define the falsifiable readout test "
        "(per the strategy review): a named Meluhhan attested in CDLI "
        "whose Indus-seal counterpart can be uniquely identified."
    )

    return {
        "summary": summary,
        "n_tablets": n_tablets,
        "n_persons": n_persons,
        "n_confirmed_persons": len(confirmed_persons),
        "n_seals": n_seals,
        "n_pairings": n_pairings,
        "next_steps": next_steps,
        "verdict": (
            "OBSERVED" if n_tablets > 100 and n_seals > 0 else "INSUFFICIENT_DATA"
        ),
    }


# ── Atomic node defs for registration ─────────────────────────────────


def _phase22_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "ContactCorpusLoader", "Contact Corpus Loader (Phase-22)",
            "Phase-22 / Sources",
            "Load the CDLI Meluhha-mention tablet corpus + the "
            "hand-encoded Indus-seals-at-Mesopotamia inventory + "
            "heuristically-extracted Meluhhan-person name candidates.",
            inputs=[],
            outputs=[
                {"name": "tablets", "type": "json"},
                {"name": "n_tablets", "type": "number"},
                {"name": "keyword_counts", "type": "json"},
                {"name": "period_counts", "type": "json"},
                {"name": "provenience_counts", "type": "json"},
                {"name": "seals_at_mesopotamia", "type": "json"},
                {"name": "n_seals_at_mesopotamia", "type": "number"},
                {"name": "persons", "type": "json"},
                {"name": "n_persons", "type": "number"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "period_filter": {"type": "string", "default": "",
                                       "description": "Substring filter on tablet period (e.g. 'Ur III')."},
                    "keyword_filter": {"type": "string", "default": "",
                                        "description": "Substring filter on matched keywords (e.g. 'me-luh')."},
                },
            },
            fn=_contact_corpus_loader,
        ),
        AtomicNodeDef(
            "MeluhhaCorpusReporter", "Meluhha Corpus Reporter (Phase-22)",
            "Phase-22 / Reporters",
            "Compact CDLI Meluhha-mention audit: keyword distribution, "
            "top periods + proveniences, top-10 most-mentioned tablets.",
            inputs=[
                {"name": "tablets", "type": "json", "required": True},
                {"name": "keyword_counts", "type": "json", "required": False},
                {"name": "period_counts", "type": "json", "required": False},
                {"name": "provenience_counts", "type": "json", "required": False},
            ],
            outputs=[
                {"name": "n_tablets", "type": "number"},
                {"name": "n_keywords", "type": "number"},
                {"name": "keyword_counts", "type": "json"},
                {"name": "top_5_periods", "type": "json"},
                {"name": "top_10_provenience", "type": "json"},
                {"name": "most_mentioned_top10", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_meluhha_corpus_reporter,
        ),
        AtomicNodeDef(
            "MeluhhanPersonsExtractor", "Meluhhan Persons Extractor (Phase-22)",
            "Phase-22 / Reporters",
            "Surface high-confidence Meluhhan personal-name candidates "
            "from CDLI tablet lines that include 'me-luh-ha'. Aggregates "
            "across tablets, ranks by occurrence count, and flags any "
            "match against historically-known Meluhhan names (Lu-sun-zi-da, "
            "Shu-ilishu).",
            inputs=[
                {"name": "persons", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_unique_candidates", "type": "number"},
                {"name": "rows_top50", "type": "json"},
                {"name": "all_rows_count", "type": "number"},
                {"name": "confirmed_hits", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_freq": {"type": "integer", "default": 1, "minimum": 1,
                                  "description": "Minimum occurrence count for a candidate name."},
                },
            },
            fn=_meluhhan_persons_extractor,
        ),
        AtomicNodeDef(
            "IndusSealsAtMesopotamiaSummary", "Indus Seals @ Mesopotamia Summary (Phase-22)",
            "Phase-22 / Reporters",
            "Compact summary of Indus / Indus-related seals found in "
            "Mesopotamia, Iran, and the Persian Gulf, broken down by "
            "find country, seal type, and period.",
            inputs=[
                {"name": "seals_at_mesopotamia", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_seals", "type": "number"},
                {"name": "by_country", "type": "json"},
                {"name": "by_type", "type": "json"},
                {"name": "by_period", "type": "json"},
                {"name": "rows", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_indus_seals_at_mesopotamia_summary,
        ),
        AtomicNodeDef(
            "MeluhhaNameMatcher", "Meluhha Name Matcher (Phase-22, prototype)",
            "Phase-22 / Decipherment",
            "Score candidate Indus-seal-inscription <-> Meluhhan-name "
            "pairings by length and structural compatibility. Prototype: "
            "needs indus_signs[] populated on the seal corpus to produce "
            "real candidates. Currently surfaces the gap as a verdict.",
            inputs=[
                {"name": "persons", "type": "json", "required": True},
                {"name": "seals_at_mesopotamia", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_candidates", "type": "number"},
                {"name": "n_seals_with_signs", "type": "number"},
                {"name": "n_seals_total", "type": "number"},
                {"name": "pairings_top50", "type": "json"},
                {"name": "n_pairings", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_name_freq": {"type": "integer", "default": 2, "minimum": 1},
                },
            },
            fn=_meluhha_name_matcher,
        ),
        AtomicNodeDef(
            "Phase22Verdict", "Phase-22 Verdict Aggregator",
            "Phase-22 / Reporters",
            "Aggregate the Phase-22 sub-experiment outputs (Meluhha "
            "audit, persons extractor, seals summary, name matcher) "
            "into a single contact-zone inventory verdict + Phase-23 "
            "priority list.",
            inputs=[
                {"name": "n_tablets", "type": "number", "required": False},
                {"name": "n_persons", "type": "number", "required": False},
                {"name": "confirmed_hits", "type": "json", "required": False},
                {"name": "n_seals", "type": "number", "required": False},
                {"name": "n_pairings", "type": "number", "required": False},
            ],
            outputs=[
                {"name": "summary", "type": "text"},
                {"name": "n_tablets", "type": "number"},
                {"name": "n_persons", "type": "number"},
                {"name": "n_confirmed_persons", "type": "number"},
                {"name": "n_seals", "type": "number"},
                {"name": "n_pairings", "type": "number"},
                {"name": "next_steps", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase22_verdict,
        ),
    ]


__all__ = [
    "_contact_corpus_loader",
    "_meluhha_corpus_reporter",
    "_meluhhan_persons_extractor",
    "_indus_seals_at_mesopotamia_summary",
    "_meluhha_name_matcher",
    "_phase22_verdict",
    "_phase22_node_defs",
]

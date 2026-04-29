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

import math
from collections import Counter
from typing import Any


# ── Helpers ───────────────────────────────────────────────────────────


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:  # noqa: BLE001
        return default


# ── Loaders ───────────────────────────────────────────────────────────


def _contact_corpus_loader(inputs: dict, params: dict) -> dict:
    """Load the CDLI Meluhha-mention tablet corpus and the
    Indus-seals-at-Mesopotamia inventory."""
    try:
        from glossa_lab.data.mesopotamian_contact import (  # noqa: PLC0415
            get_meluhha_tablets, get_meluhha_keyword_counts,
            get_meluhha_period_counts, get_meluhha_provenience_counts,
            get_indus_seals_at_mesopotamia, get_meluhhan_persons,
        )
    except Exception as exc:  # noqa: BLE001
        return {"error": f"data module not available: {exc}"}

    tablets = get_meluhha_tablets()
    keyword_counts = get_meluhha_keyword_counts()
    period_counts = get_meluhha_period_counts()
    provenience_counts = get_meluhha_provenience_counts()
    seals = get_indus_seals_at_mesopotamia()
    persons = get_meluhhan_persons()

    # Optional filter by keyword and period
    period_filter = (params.get("period_filter") or "").strip().lower()
    keyword_filter = (params.get("keyword_filter") or "").strip().lower()
    if period_filter:
        tablets = [t for t in tablets if period_filter in (t.get("period", "")).lower()]
    if keyword_filter:
        tablets = [
            t for t in tablets
            if any(keyword_filter in k.lower() for k in (t.get("matched_keywords") or []))
        ]

    return {
        "tablets": tablets,
        "n_tablets": len(tablets),
        "keyword_counts": keyword_counts,
        "period_counts": period_counts,
        "provenience_counts": provenience_counts,
        "seals_at_mesopotamia": seals,
        "n_seals_at_mesopotamia": len(seals),
        "persons": persons,
        "n_persons": len(persons),
    }


# ── Reporters ─────────────────────────────────────────────────────────


def _meluhha_corpus_reporter(inputs: dict, params: dict) -> dict:
    """Compact report on the loaded Meluhha-mention corpus."""
    tablets = inputs.get("tablets") or []
    keyword_counts = inputs.get("keyword_counts") or {}
    period_counts = inputs.get("period_counts") or {}
    provenience_counts = inputs.get("provenience_counts") or {}

    # Most-mentioned tablet by match_count
    if tablets:
        most_mentioned = sorted(
            tablets, key=lambda t: -_safe_int(t.get("match_count")),
        )[:10]
    else:
        most_mentioned = []

    top_5_periods = sorted(
        period_counts.items(), key=lambda kv: -kv[1],
    )[:5]
    top_10_provenience = sorted(
        provenience_counts.items(), key=lambda kv: -kv[1],
    )[:10]

    verdict = (
        f"CDLI Meluhha audit: {len(tablets)} tablets across "
        f"{len(period_counts)} periods. "
        f"Dominant period: {top_5_periods[0][0] if top_5_periods else '(none)'} "
        f"({top_5_periods[0][1] if top_5_periods else 0} tablets). "
        f"Dominant provenience: "
        f"{top_10_provenience[0][0] if top_10_provenience else '(none)'} "
        f"({top_10_provenience[0][1] if top_10_provenience else 0} tablets)."
    )

    return {
        "n_tablets": len(tablets),
        "n_keywords": len(keyword_counts),
        "keyword_counts": keyword_counts,
        "top_5_periods": top_5_periods,
        "top_10_provenience": top_10_provenience,
        "most_mentioned_top10": [
            {
                "p_number": t.get("p_number"),
                "designation": t.get("designation"),
                "period": t.get("period"),
                "provenience": t.get("provenience"),
                "match_count": _safe_int(t.get("match_count")),
                "matched_keywords": t.get("matched_keywords"),
            }
            for t in most_mentioned
        ],
        "verdict": verdict,
    }


def _meluhhan_persons_extractor(inputs: dict, params: dict) -> dict:
    """Surface high-confidence Meluhhan name candidates."""
    persons = inputs.get("persons") or []
    min_freq = _safe_int(params.get("min_freq", 1), 1)

    name_counts: Counter[str] = Counter()
    name_periods: dict[str, set[str]] = {}
    name_proveniences: dict[str, set[str]] = {}
    name_lines: dict[str, list[str]] = {}
    for p in persons:
        name = p.get("candidate_name", "")
        if not name:
            continue
        name_counts[name] += 1
        name_periods.setdefault(name, set()).add(p.get("period", "") or "")
        name_proveniences.setdefault(name, set()).add(p.get("provenience", "") or "")
        name_lines.setdefault(name, []).append(p.get("line", ""))

    rows: list[dict] = []
    for name, count in name_counts.most_common():
        if count < min_freq:
            continue
        rows.append({
            "candidate_name": name,
            "occurrences": count,
            "n_distinct_tablets": len({p["p_number"] for p in persons
                                          if p.get("candidate_name") == name}),
            "periods": sorted(name_periods.get(name, set())),
            "proveniences": sorted(name_proveniences.get(name, set())),
            "example_line": name_lines[name][0] if name_lines.get(name) else "",
        })

    # Highlight known historical Meluhhan names
    known_names = {"lu-sun-zi-da", "lu2-sun-zi-da", "shu-ilishu", "shu-ilisu",
                    "su-ilisu"}
    confirmed_hits = [r for r in rows if r["candidate_name"].lower() in known_names]

    verdict = (
        f"Meluhhan-person extractor: {len(rows)} unique name candidates "
        f"(freq >= {min_freq}); {len(confirmed_hits)} match historically-known "
        "Meluhhan-named persons (Lu-sun-zi-da, Shu-ilishu)."
    )

    return {
        "n_unique_candidates": len(rows),
        "rows_top50": rows[:50],
        "all_rows_count": len(rows),
        "confirmed_hits": confirmed_hits,
        "verdict": verdict,
    }


def _indus_seals_at_mesopotamia_summary(inputs: dict, params: dict) -> dict:
    """Compact report on hand-encoded Indus seals found in
    Mesopotamia / Iran / Persian Gulf."""
    seals = inputs.get("seals_at_mesopotamia") or []
    by_country: Counter[str] = Counter()
    by_type: Counter[str] = Counter()
    by_period: Counter[str] = Counter()
    for s in seals:
        by_country[s.get("find_country", "(unknown)")] += 1
        by_type[s.get("type", "(unknown)")] += 1
        by_period[s.get("find_period", "(unknown)")] += 1
    rows = []
    for s in seals:
        rows.append({
            "catalogue_id": s.get("catalogue_id"),
            "type": s.get("type"),
            "find_country": s.get("find_country"),
            "find_spot": s.get("find_spot"),
            "find_period": s.get("find_period"),
            "current_collection": s.get("current_collection"),
            "inscription_reading": s.get("inscription_reading"),
            "source": s.get("source"),
        })
    return {
        "n_seals": len(seals),
        "by_country": dict(by_country.most_common()),
        "by_type": dict(by_type.most_common()),
        "by_period": dict(by_period.most_common()),
        "rows": rows,
        "verdict": (
            f"Indus-seals-at-Mesopotamia inventory: {len(seals)} seals "
            f"({len(by_country)} countries, {len(by_type)} types). "
            f"Dominant context: {by_country.most_common(1)[0] if by_country else '(none)'}."
        ),
    }


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
    """
    persons = inputs.get("persons") or []
    seals = inputs.get("seals_at_mesopotamia") or []
    min_name_freq = _safe_int(params.get("min_name_freq", 2), 2)

    # Aggregate names
    name_counts: Counter[str] = Counter(
        p.get("candidate_name", "") for p in persons
    )
    candidates = [(n, c) for n, c in name_counts.most_common()
                  if c >= min_name_freq and n]
    seal_with_signs = [s for s in seals
                        if s.get("indus_signs")
                        and isinstance(s["indus_signs"], list)
                        and len(s["indus_signs"]) > 0]

    pairings: list[dict] = []
    if not seal_with_signs:
        verdict = (
            "PROTOTYPE STATUS: name-matcher cannot score yet because no "
            "Mesopotamia-found Indus seals have ingested sign sequences. "
            "Phase-23 must populate indus_signs[] from CISI Vol 3 / "
            "Frenez 2018 catalogue tables. "
            f"Available: {len(candidates)} name candidates "
            f"(freq>={min_name_freq}); {len(seals)} seals (none with signs)."
        )
    else:
        for seal in seal_with_signs:
            n_signs = len(seal["indus_signs"])
            for name, count in candidates:
                # Akkadian/Sumerian name segments are hyphenated; count + 1
                name_n_segments = name.count("-") + 1
                # Score: 1.0 when length match exact; falls off linearly
                length_score = max(0.0, 1.0 - abs(n_signs - name_n_segments) / 5.0)
                if length_score == 0:
                    continue
                pairings.append({
                    "seal_id": seal.get("catalogue_id"),
                    "seal_n_signs": n_signs,
                    "candidate_name": name,
                    "name_n_segments": name_n_segments,
                    "name_occurrences": count,
                    "length_score": round(length_score, 3),
                })
        pairings.sort(key=lambda r: -r["length_score"])
        verdict = (
            f"Name-matcher: {len(pairings)} length-compatible pairings between "
            f"{len(seal_with_signs)} sign-bearing seals and "
            f"{len(candidates)} name candidates."
        )

    return {
        "n_candidates": len(candidates),
        "n_seals_with_signs": len(seal_with_signs),
        "n_seals_total": len(seals),
        "pairings_top50": pairings[:50],
        "n_pairings": len(pairings),
        "verdict": verdict,
    }


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

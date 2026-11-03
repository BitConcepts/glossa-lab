"""Phase-25 atomic-node implementations.

Phase-25 implements Tiers A, B, and D of the Phase-24-synthesis
strategy: the first phonetic readout attempt on Janabiyah seal #10,
the held-out phonetic test on the rest of the inscribed seals,
period-stratified replication of the Phase-24d bipartite readout
test, persons-v3 cleanup, Shu-ilishu biographical anchor search,
and the Tamil-Brahmi structural cross-check.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Any


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:  # noqa: BLE001
        return default


def _name_n_segments(name: str) -> int:
    return name.count("-") + 1 if name else 0


# ── Loader ────────────────────────────────────────────────────────────


def _phase25_corpus_loader(inputs: dict, params: dict) -> dict:
    """Load all Phase-25 contact-zone artefacts."""
    try:
        from glossa_lab.data.mesopotamian_contact import (  # noqa: PLC0415
            get_indus_seals_at_mesopotamia,
            get_janabiyah_seal_reading,
            get_meluhha_tablets,
            get_meluhhan_persons_v2,
            get_meluhhan_persons_v3,
            get_parpola_phoneme_map,
            get_seals_with_inscription,
        )
    except Exception as exc:  # noqa: BLE001
        return {"error": f"data module not available: {exc}"}

    return {
        "all_seals": get_indus_seals_at_mesopotamia(),
        "inscribed_seals": get_seals_with_inscription(),
        "persons_v2": get_meluhhan_persons_v2(),
        "persons_v3": get_meluhhan_persons_v3(),
        "phoneme_map": get_parpola_phoneme_map(),
        "janabiyah_reading": get_janabiyah_seal_reading(),
        "tablets": get_meluhha_tablets(),
        "n_tablets": len(get_meluhha_tablets()),
    }


# ── Tier A1: Janabiyah phonetic readout ──────────────────────────────


def _janabiyah_phonetic_readout(inputs: dict, params: dict) -> dict:
    """Predict phonetic reading of Janabiyah seal #10 + search CDLI for matches.

    Strategy: Parpola 2010 hypothesizes 'fish' sign family = Dravidian
    *miin* (fish/star). Janabiyah seal contains 3 fish-family signs
    (147, 145, 145). Predict that the underlying name has 3 *miin*
    morphemes, which Akkadian scribes would render as 'mi-in', 'me-en',
    'mi-na', or similar. Search CDLI Meluhha-mention tablets for any
    PN matching this pattern.
    """
    janabiyah = inputs.get("janabiyah_reading") or {}
    phoneme_map = inputs.get("phoneme_map") or {}
    tablets = inputs.get("tablets") or []

    if not janabiyah or not phoneme_map:
        return {"error": "Phoneme map or Janabiyah reading not available."}

    # Reconstruct the predicted phonetic skeleton
    sign_seq = janabiyah.get("sign_sequence", [])
    predictions: list[dict] = []
    for sign_id in sign_seq:
        ph = phoneme_map.get(sign_id, {})
        predictions.append({
            "sign_id": sign_id,
            "phoneme": ph.get("phoneme", "?"),
            "gloss": ph.get("gloss", "(unmapped)"),
            "confidence": ph.get("confidence", "none"),
        })

    miin_count = sum(1 for p in predictions
                     if "miin" in (p["phoneme"] or "").lower())
    skeleton = "-".join(p["phoneme"] for p in predictions)

    # Search CDLI Meluhha-mention tablets for any line containing
    # multiple 'miin'-rendering syllables (mi-in, me-en, mi-na, me-na,
    # mi-il, me-il, mu-li).
    miin_renderings = [
        "mi-in", "me-en", "mi-na", "me-na", "mi-il", "me-il",
        "mi-en", "me-in", "mu-li", "min-", "men-",
    ]
    matches: list[dict] = []
    for t in tablets:
        kw = " ".join(t.get("matched_keywords") or []).lower()
        if "me-luh" not in kw:
            continue
        line_pool: list[str] = []
        line_pool.extend(t.get("atf_lines_with_match") or [])
        line_pool.extend(t.get("atf_excerpt_lines") or [])
        for line in line_pool:
            ll = line.lower()
            hits = sum(1 for r in miin_renderings if r in ll)
            if hits >= 2:
                matches.append({
                    "p_number": t.get("p_number"),
                    "period": t.get("period"),
                    "provenience": t.get("provenience"),
                    "n_miin_hits": hits,
                    "line": line[:160],
                })
    matches.sort(key=lambda m: -m["n_miin_hits"])

    verdict = (
        f"Janabiyah phonetic readout: predicted skeleton '{skeleton}' "
        f"({miin_count}/7 confirmed miin); searched {len(tablets)} CDLI "
        f"tablets, found {len(matches)} lines with >= 2 miin-rendering "
        f"syllables."
    )

    return {
        "skeleton": skeleton,
        "predictions": predictions,
        "n_miin": miin_count,
        "n_signs": len(sign_seq),
        "matches_top20": matches[:20],
        "n_matches": len(matches),
        "miin_renderings_searched": miin_renderings,
        "verdict": verdict,
        "interpretation": (
            "If the Janabiyah seal owner's name carried multiple miin "
            "(fish/star) morphemes per Parpola's Dravidian hypothesis, "
            "Akkadian scribes would have rendered it as multiple "
            "mi-in / me-en / mi-na syllables in clay tablets. A "
            "significant cluster of such tablets in the same period + "
            "provenience as Janabiyah (Early Dilmun ~2100-2000 BC, "
            "Bahrain) would be a phonetic anchor candidate."
        ),
    }


# ── Tier A2: Blind held-out phonetic test ───────────────────────────


def _blind_held_out_test(inputs: dict, params: dict) -> dict:
    """Apply the fixed Parpola phoneme map to all inscribed seals,
    counting how many can be 'read' (i.e. have at least one sign with
    high-confidence Parpola-attributed phoneme).

    Spec 087 S3 (family F4): the mechanism is the generic
    PhonemeMapCoverage engine (glossa_lab.generic_primitives); this
    node is its Phase-25 parameterisation, with the readability
    predicate and the verdict text carried as spec data.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        phoneme_map_coverage_execute,
    )

    merged = dict(params)
    merged["coverage_spec"] = {
        "verdict_template": (
            "Blind held-out test: {n_seals} inscribed seals; "
            "{n_readable} have at least one Parpola-attributed phoneme; "
            "{n_high_conf} have at least one high-confidence phoneme. "
            "Only Janabiyah Laursen #10 currently has actual sign IDs; "
            "the other 10 seals have '?' placeholders pending CISI Vol 3 "
            "plate ingestion."
        ),
    }
    return phoneme_map_coverage_execute(inputs, merged)


# ── Tier B4: Period-stratified replication of bipartite readout ──────


def _period_stratified_readout(inputs: dict, params: dict) -> dict:
    """Split persons-v3 candidates by period and run Phase-24d readout
    test on each subset against the same 11 inscribed seals.

    Spec 087 S3 (family F5): the mechanism is the generic
    StratifiedPermutationTest engine (glossa_lab.generic_primitives);
    this node is its Phase-25 parameterisation. The period coarsening
    that was an inline if/elif chain is now the ordered strata_rules
    data below (case-sensitive, on the stripped period string; the
    "Old Akkadian" bucket carries both of the chain's keys), and the
    per-stratum seed rule is seed_base 42 + len(bucket). The
    module-local _run_bipartite_test / _greedy_score / _length_score
    helpers were used only here; they were removed (the engine
    carries the shared bipartite core). _name_n_segments stays: the
    Persons-v3 extractor still uses it.
    """
    from glossa_lab.generic_primitives import (  # noqa: PLC0415
        stratified_permutation_test_execute,
    )

    merged = dict(params)
    merged["strata_spec"] = {
        "stratum_field": "period",
        "axis_key": "period",
        "strata_rules": [
            ["Ur III", ["Ur III"]],
            ["Old Babylonian", ["Old Babylonian"]],
            ["Neo-Assyrian", ["Neo-Assyrian"]],
            ["Old Akkadian", ["Old Akkadian", "Akkadian"]],
            ["Ebla", ["Ebla"]],
        ],
        "case_insensitive": False,
        "strip_value": True,
        "empty_bucket": None,
        "fallback_bucket": "Other",
        "seed_base": 42,
        "verdict_template": (
            "Period-stratified readout: {n_results} period subsets tested; "
            "{n_significant} achieve p<0.05. Robustness check: if "
            ">1 period strata yield p<0.05, the Phase-24d signal is "
            "period-robust; if only the overall result is significant, "
            "the signal may be a sample-size artifact."
        ),
    }
    return stratified_permutation_test_execute(inputs, merged)


# ── Tier D10: Shu-ilishu biographical anchor search ─────────────────


def _shu_ilishu_anchor_search(inputs: dict, params: dict) -> dict:
    """Search the existing Indus seal corpus (CISI / Mahadevan) for
    seals from Mesopotamia/Iran/Bahrain provenience that could be
    candidates for the bilingual translator Shu-ilishu's Indus-script
    counterpart, or for any seal owned by a person who served the same
    bilingual translator role.
    """
    try:
        from glossa_lab.data.indus_cisi import (  # noqa: PLC0415
            get_corpus_inscriptions as _cisi_inscs,
        )
    except Exception:  # noqa: BLE001
        _cisi_inscs = None

    # We can't fully cross-reference without site metadata in the CISI
    # data module, so we report what's accessible: short Indus
    # inscriptions of length 3-5 that could plausibly encode a
    # bilingual professional name.
    candidates: list[dict] = []
    if _cisi_inscs is not None:
        try:
            inscs = _cisi_inscs()
        except Exception as exc:  # noqa: BLE001
            return {"error": f"CISI corpus not available: {exc}",
                    "candidates": []}
        # Find Indus inscriptions of length 3-7 (compatible with a
        # personal-name + title structure)
        for ins in inscs[:5000]:  # cap to first 5000 for speed
            if 3 <= len(ins) <= 7:
                candidates.append({
                    "n_signs": len(ins),
                    "indus_signs": list(ins),
                })
        # Take a representative sample
        candidates_sample = candidates[:20]
    else:
        candidates_sample = []

    verdict = (
        f"Shu-ilishu anchor search: {len(candidates)} CISI inscriptions "
        f"of length 3-7 in the Indus corpus could plausibly encode "
        f"a bilingual professional name. Full cross-reference with "
        f"find-spot metadata requires CISI Vol 3 ingestion (Phase-26)."
    )
    return {
        "n_candidates_total": len(candidates),
        "candidates_sample": candidates_sample,
        "verdict": verdict,
        "shu_ilishu_seal_summary": (
            "Shu-ilishu seal AO 22310 (Louvre) is cuneiform-only; "
            "his name reads 'Shu-ilishu, EME.BAL.ME.LUH.HA.KI' "
            "= 'translator of Meluhha'. As a bilingual professional, "
            "he likely also possessed an Indus-script counterpart "
            "seal (which has not been identified). Phase-26 needs "
            "CISI find-spot metadata to filter for "
            "Mesopotamia/Iran/Bahrain provenience."
        ),
    }


# ── Tier D11: Tamil-Brahmi structural cross-check ───────────────────


def _tamil_brahmi_crosscheck(inputs: dict, params: dict) -> dict:
    """Compare positional-class distributions between Tamil/Dravidian
    and Indus corpora to test whether Indus shares structural
    typology with the Dravidian family.
    """
    try:
        from glossa_lab.data.dravidian import (  # noqa: PLC0415
            get_corpus_inscriptions as _drav_inscs,
        )
    except Exception:  # noqa: BLE001
        _drav_inscs = None
    try:
        from glossa_lab.data.indus_cisi import (  # noqa: PLC0415
            get_corpus_inscriptions as _indus_inscs,
        )
    except Exception:  # noqa: BLE001
        _indus_inscs = None

    if _drav_inscs is None or _indus_inscs is None:
        return {"error": "Required corpora (dravidian / indus_cisi) "
                          "not available."}

    drav_seqs = _drav_inscs()
    indus_seqs = _indus_inscs()

    def _imt_rates(seqs: list[list[str]]) -> dict:
        """Compute initial/medial/terminal frequency for top-50 signs."""
        total = Counter(s for seq in seqs for s in seq)
        init = Counter(seq[0] for seq in seqs if seq)
        term = Counter(seq[-1] for seq in seqs if len(seq) >= 1)
        med = Counter(s for seq in seqs for s in seq[1:-1])
        rates = {}
        for sym, n in total.most_common(50):
            if n < 5:
                continue
            rates[sym] = {
                "i": init.get(sym, 0) / n,
                "m": med.get(sym, 0) / n,
                "t": term.get(sym, 0) / n,
                "n": n,
            }
        # Aggregate distributions
        n_total = sum(total.values()) or 1
        return {
            "n_seqs": len(seqs),
            "n_tokens": n_total,
            "n_distinct": len(total),
            "i_total": sum(init.values()) / n_total,
            "t_total": sum(term.values()) / n_total,
            "m_total": sum(med.values()) / n_total,
            "top50_rates": rates,
        }

    drav_stats = _imt_rates(drav_seqs)
    indus_stats = _imt_rates(indus_seqs)

    # Compute KL divergence between the I/T/M aggregate distributions
    def _kl(p: list[float], q: list[float]) -> float:
        return sum(pi * math.log2(pi / qi) for pi, qi in zip(p, q)
                   if pi > 0 and qi > 0)

    p_drav = [drav_stats["i_total"], drav_stats["m_total"], drav_stats["t_total"]]
    p_indus = [indus_stats["i_total"], indus_stats["m_total"], indus_stats["t_total"]]
    kl_drav_indus = _kl(p_indus, p_drav)
    kl_indus_drav = _kl(p_drav, p_indus)

    verdict = (
        f"Tamil-Brahmi cross-check: Dravidian corpus = "
        f"{drav_stats['n_seqs']} seqs / {drav_stats['n_tokens']} tokens; "
        f"Indus corpus = {indus_stats['n_seqs']} seqs / "
        f"{indus_stats['n_tokens']} tokens. "
        f"I/M/T aggregate rates - Dravidian: "
        f"({drav_stats['i_total']:.3f}, {drav_stats['m_total']:.3f}, "
        f"{drav_stats['t_total']:.3f}), Indus: "
        f"({indus_stats['i_total']:.3f}, {indus_stats['m_total']:.3f}, "
        f"{indus_stats['t_total']:.3f}). "
        f"KL(Indus||Dravidian) = {kl_drav_indus:.4f} bits; "
        f"KL(Dravidian||Indus) = {kl_indus_drav:.4f} bits. "
        f"Lower KL = better typological fit."
    )
    return {
        "drav_stats": drav_stats,
        "indus_stats": indus_stats,
        "kl_indus_drav_bits": round(kl_drav_indus, 4),
        "kl_drav_indus_bits": round(kl_indus_drav, 4),
        "verdict": verdict,
    }


# ── Persons-v3 reporter ─────────────────────────────────────────────


def _persons_v3_extractor(inputs: dict, params: dict) -> dict:
    persons = inputs.get("persons_v3") or []
    min_freq = _safe_int(params.get("min_freq", 1), 1)

    name_counts: Counter[str] = Counter()
    name_periods: dict[str, set[str]] = {}
    name_lines: dict[str, list[str]] = {}
    for p in persons:
        n = p.get("candidate_name", "")
        if not n:
            continue
        name_counts[n] += 1
        name_periods.setdefault(n, set()).add(p.get("period", "") or "")
        name_lines.setdefault(n, []).append(p.get("line", ""))

    rows = []
    for n, c in name_counts.most_common():
        if c < min_freq:
            continue
        rows.append({
            "candidate_name": n,
            "occurrences": c,
            "n_segments": _name_n_segments(n),
            "periods": sorted(name_periods.get(n, set())),
            "example_line": (name_lines[n][0] if name_lines.get(n) else "")[:160],
        })

    verdict = (
        f"Persons-v3: {len(rows)} unique candidates (freq>={min_freq}). "
        f"v2 noise (lu-ti, lu-na, lu-ma-ku) dropped via extended "
        f"Akkadian-fragment stoplist + 3-segment minimum + 6-segment "
        f"regex (captures ur-{{d}}suen-me-luh-ha)."
    )
    return {
        "n_unique": len(rows),
        "rows_top50": rows[:50],
        "rows_all": rows,
        "verdict": verdict,
    }


# ── Verdict aggregator ──────────────────────────────────────────────


def _phase25_verdict(inputs: dict, params: dict) -> dict:
    summary = (
        "Phase-25 contact-zone progress: phonetic-readout pipeline now "
        "operational. See sub-experiment reports for Janabiyah miin-pattern "
        "predictions, period-stratified bipartite p-values, persons-v3 "
        "noise-cleaned candidates, Shu-ilishu anchor candidates, and "
        "Tamil-Brahmi typology fit."
    )
    next_steps = [
        "Phase-26 priority 1: ingest CISI Vol 3 plates (acquired in "
        "Phase-25 acquisition pass) to populate '?' placeholders for "
        "the remaining 10 inscribed seals with Parpola/Mahadevan IDs.",
        "Phase-26 priority 2: process Parpola 2010 Dravidian-solution "
        "phoneme proposals (acquired) into a tighter sign->phoneme map "
        "covering 30+ signs (vs current 15).",
        "Phase-26 priority 3: extract CDLI find-spot metadata for "
        "Mahadevan M77 corpus to enable the Shu-ilishu biographical "
        "anchor search filter.",
        "Phase-26 priority 4: implement the Bayesian-decoder "
        "approach - score the full inscribed-seal corpus under "
        "Parpola's phoneme-map hypothesis vs random shuffled "
        "phoneme-map nulls to obtain a global p-value for the "
        "Dravidian hypothesis.",
    ]
    return {
        "summary": summary,
        "next_steps": next_steps,
    }


# ── Atomic node defs for registration ───────────────────────────────


def _phase25_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "Phase25CorpusLoader", "Phase-25 Contact Corpus Loader",
            "Phase-25 / Sources",
            "Load Phase-25 contact-zone artefacts: augmented seals, "
            "persons-v2 + persons-v3, Parpola phoneme map, "
            "Janabiyah seal reading, full Meluhha-tablet corpus.",
            inputs=[],
            outputs=[
                {"name": "all_seals", "type": "json"},
                {"name": "inscribed_seals", "type": "json"},
                {"name": "persons_v2", "type": "json"},
                {"name": "persons_v3", "type": "json"},
                {"name": "phoneme_map", "type": "json"},
                {"name": "janabiyah_reading", "type": "json"},
                {"name": "tablets", "type": "json"},
                {"name": "n_tablets", "type": "number"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase25_corpus_loader,
        ),
        AtomicNodeDef(
            "JanabiyahPhoneticReadout", "Janabiyah Phonetic Readout (Phase-25)",
            "Phase-25 / Decipherment",
            "First true bilingual decipherment attempt: predicts the "
            "phonetic reading of Janabiyah seal #10's 7-sign Parpola "
            "sequence using the Parpola candidate phoneme map, then "
            "searches CDLI Meluhha-mention tablets for any name with "
            "the predicted miin-pattern.",
            inputs=[
                {"name": "janabiyah_reading", "type": "json", "required": True},
                {"name": "phoneme_map", "type": "json", "required": True},
                {"name": "tablets", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "skeleton", "type": "text"},
                {"name": "predictions", "type": "json"},
                {"name": "n_miin", "type": "number"},
                {"name": "matches_top20", "type": "json"},
                {"name": "n_matches", "type": "number"},
                {"name": "verdict", "type": "text"},
                {"name": "interpretation", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_janabiyah_phonetic_readout,
        ),
        AtomicNodeDef(
            "BlindHeldOutTest", "Blind Held-Out Phonetic Test (Phase-25)",
            "Phase-25 / Decipherment",
            "Apply the fixed Parpola phoneme map to all inscribed "
            "seals; report which seals can be 'read' (have at least "
            "one Parpola-attributed phoneme).",
            inputs=[
                {"name": "inscribed_seals", "type": "json", "required": True},
                {"name": "phoneme_map", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_seals", "type": "number"},
                {"name": "n_readable", "type": "number"},
                {"name": "n_high_conf", "type": "number"},
                {"name": "rows", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_blind_held_out_test,
        ),
        AtomicNodeDef(
            "PeriodStratifiedReadout",
            "Period-Stratified Readout Test (Phase-25)",
            "Phase-25 / Decipherment",
            "Replicate the Phase-24d bipartite readout test on each "
            "period subset (Ur III, Old Babylonian, Neo-Assyrian, Old "
            "Akkadian, Ebla, Other) plus the overall corpus. Period-"
            "robust signal = p<0.05 in 2+ strata.",
            inputs=[
                {"name": "persons_v3", "type": "json", "required": True},
                {"name": "inscribed_seals", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "results", "type": "json"},
                {"name": "n_significant_strata", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "n_permutations": {"type": "integer", "default": 1000, "minimum": 100},
                    "tolerance": {"type": "integer", "default": 2, "minimum": 0},
                },
            },
            fn=_period_stratified_readout,
        ),
        AtomicNodeDef(
            "Persons_v3_Extractor",
            "Refined Meluhhan Persons Extractor v3 (Phase-25)",
            "Phase-25 / Reporters",
            "Persons-v3: Phase-24 v2 + extended Akkadian-fragment "
            "stoplist (lu-ti, lu-na, lu-ma-ku, etc.) + 3-segment "
            "minimum + 6-segment regex (captures ur-{d}suen-me-luh-ha).",
            inputs=[
                {"name": "persons_v3", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_unique", "type": "number"},
                {"name": "rows_top50", "type": "json"},
                {"name": "rows_all", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_freq": {"type": "integer", "default": 1, "minimum": 1},
                },
            },
            fn=_persons_v3_extractor,
        ),
        AtomicNodeDef(
            "ShuIlishuAnchorSearch",
            "Shu-Ilishu Biographical Anchor Search (Phase-25)",
            "Phase-25 / Decipherment",
            "Search the CISI Indus seal corpus for short (3-7 sign) "
            "inscriptions that could plausibly encode the bilingual "
            "translator Shu-ilishu's Indus-script counterpart name.",
            inputs=[],
            outputs=[
                {"name": "n_candidates_total", "type": "number"},
                {"name": "candidates_sample", "type": "json"},
                {"name": "verdict", "type": "text"},
                {"name": "shu_ilishu_seal_summary", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_shu_ilishu_anchor_search,
        ),
        AtomicNodeDef(
            "TamilBrahmiCrosscheck",
            "Tamil-Brahmi Structural Cross-check (Phase-25)",
            "Phase-25 / Reporters",
            "Compare initial/medial/terminal positional rates between "
            "Dravidian (Tamil-Brahmi) and Indus corpora; compute KL "
            "divergence. Lower KL = better typological fit for the "
            "Dravidian hypothesis.",
            inputs=[],
            outputs=[
                {"name": "drav_stats", "type": "json"},
                {"name": "indus_stats", "type": "json"},
                {"name": "kl_indus_drav_bits", "type": "number"},
                {"name": "kl_drav_indus_bits", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_tamil_brahmi_crosscheck,
        ),
        AtomicNodeDef(
            "Phase25Verdict", "Phase-25 Verdict Aggregator",
            "Phase-25 / Reporters",
            "Aggregate Phase-25 sub-experiment outputs into a "
            "decipherment-progress verdict + Phase-26 priority list.",
            inputs=[],
            outputs=[
                {"name": "summary", "type": "text"},
                {"name": "next_steps", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase25_verdict,
        ),
    ]


__all__ = [
    "_phase25_corpus_loader",
    "_janabiyah_phonetic_readout",
    "_blind_held_out_test",
    "_period_stratified_readout",
    "_persons_v3_extractor",
    "_shu_ilishu_anchor_search",
    "_tamil_brahmi_crosscheck",
    "_phase25_verdict",
    "_phase25_node_defs",
]

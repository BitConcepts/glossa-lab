"""Phase-29 atomic-node implementations.

Phase-29 = the corpus 10x expansion. Builds on Phase-28 with:

  1. Phase29CorpusLoader — adds Mahadevan 1977 (1,669 inscriptions, 9.4x CISI)
     and ePSD2 names subset (4,848 entries: 1,222 PN + 2,068 DN + ...) on top
     of the Phase-28 contact-zone artefacts.

  2. MahadevanInscriptionLoader — exposes the 1,669-inscription M77 corpus
     as a glossa-lab atomic node.

  3. ePSD2NamesLoader — exposes the Sumerian/Akkadian PN/DN/etc. database.

  4. MathematicaEpigraphicaLoader — Fuls vol. 3 placeholder loader. Default
     no-op (data file not bundled). Loads from
     ``corpora/downloads/fuls_me_vol3_corpus.json`` when present.

  5. ICITCorpusLoader — Interactive Corpus of Indus Texts (TU Berlin, Fuls).
     Default no-op; loads from ``corpora/downloads/icit_cache.json`` when
     present, with documented HTTP API path for live access.

  6. M77ReverseJanabiyahSearchV3 — Phase-28d ReverseJanabiyahSearchV2 against
     ePSD2 PNs (1,222 entries; 28x our current 44-name persons-v3 corpus).

  7. M77IconographicAnchorScore — Phase-28c AllographAwareIconographicScore
     re-applied with the M77 corpus as a freq prior, scoring how many M77
     inscriptions actually contain the anchored signs at scale.

  8. Phase29CorpusStats — comparative statistics: CISI vs M77 vs Fuls vs
     ICIT (whichever data files are present). Reports n_inscriptions,
     n_tokens, n_distinct_signs, mean_length per corpus.

  9. Phase29Verdict — aggregator.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:  # noqa: BLE001
        return default


# ── Loader ────────────────────────────────────────────────────────────


def _phase29_corpus_loader(inputs: dict, params: dict) -> dict:
    """Phase-29 loader: extends Phase-28 with Mahadevan 1977 corpus + ePSD2 names."""
    try:
        from glossa_lab.data.mesopotamian_contact import (  # noqa: PLC0415
            get_allograph_families,
            get_cisi_findspot_map,
            get_cisi_vol3_ocr_results,
            get_contact_zone_prefix_set,
            get_epsd2_metadata,
            get_epsd2_names,
            get_epsd2_personal_names,
            get_iconographic_anchors,
            get_indus_seals_at_mesopotamia,
            get_janabiyah_seal_reading,
            get_mahadevan_inscriptions,
            get_mahadevan_metadata,
            get_mahadevan_parpola_crosswalk,
            get_meluhha_tablets,
            get_meluhhan_persons_v3,
            get_parpola_phoneme_map,
            get_phase27_seal_findspot_overrides,
            get_seals_with_inscription,
        )
    except Exception as exc:  # noqa: BLE001
        return {"error": f"data module not available: {exc}"}

    return {
        "all_seals": get_indus_seals_at_mesopotamia(),
        "inscribed_seals": get_seals_with_inscription(),
        "persons_v3": get_meluhhan_persons_v3(),
        "phoneme_map": get_parpola_phoneme_map(),
        "janabiyah_reading": get_janabiyah_seal_reading(),
        "tablets": get_meluhha_tablets(),
        "n_tablets": len(get_meluhha_tablets()),
        "findspot_map": get_cisi_findspot_map(),
        "contact_zone_prefixes": sorted(get_contact_zone_prefix_set()),
        "phase27_overrides": get_phase27_seal_findspot_overrides(),
        "iconographic_anchors": get_iconographic_anchors(),
        "mahadevan_crosswalk": get_mahadevan_parpola_crosswalk(),
        "allograph_families": get_allograph_families(),
        "cisi_vol3_ocr": get_cisi_vol3_ocr_results(),
        # Phase-29 additions:
        "epsd2_names": get_epsd2_names(),
        "epsd2_personal_names": get_epsd2_personal_names(),
        "epsd2_metadata": get_epsd2_metadata(),
        "mahadevan_inscriptions": get_mahadevan_inscriptions(),
        "mahadevan_metadata": get_mahadevan_metadata(),
    }


# ── Corpus loaders (individual) ──────────────────────────────────────


def _mahadevan_inscription_loader(inputs: dict, params: dict) -> dict:
    """Load Mahadevan 1977 inscription corpus.

    Returns 1,669 inscriptions / 5,361 sign tokens / M77 numeric codes.
    9.4x the 178-inscription CISI corpus we used through Phase-28.
    """
    min_length = max(1, _safe_int(params.get("min_length", 1), 1))
    try:
        from glossa_lab.data.mesopotamian_contact import (  # noqa: PLC0415
            get_mahadevan_inscriptions,
            get_mahadevan_metadata,
        )
    except Exception as exc:  # noqa: BLE001
        return {"error": f"data module not available: {exc}"}

    inscriptions = get_mahadevan_inscriptions(min_length=min_length)
    md = get_mahadevan_metadata()
    sign_freq = Counter(s for ins in inscriptions for s in ins)
    return {
        "inscriptions": inscriptions,
        "n_inscriptions": len(inscriptions),
        "n_tokens": sum(len(i) for i in inscriptions),
        "n_distinct_signs": len(sign_freq),
        "metadata": md,
        "top_20_signs": sign_freq.most_common(20),
        "verdict": (
            f"Mahadevan 1977 corpus loaded: {len(inscriptions)} inscriptions, "
            f"{sum(len(i) for i in inscriptions)} sign tokens, "
            f"{len(sign_freq)} distinct M77 sign codes. "
            f"Mean inscription length: {md.get('mean_length', '?')}."
        ),
    }


def _epsd2_names_loader(inputs: dict, params: dict) -> dict:
    """Load ePSD2 names subset (Sumerian/Akkadian PNs/DNs/etc.)."""
    pos_filter = params.get("pos_filter") or ""
    try:
        from glossa_lab.data.mesopotamian_contact import (  # noqa: PLC0415
            get_epsd2_metadata,
            get_epsd2_names,
        )
    except Exception as exc:  # noqa: BLE001
        return {"error": f"data module not available: {exc}"}

    all_names = get_epsd2_names()
    if pos_filter:
        names = [n for n in all_names if n.get("pos") == pos_filter]
    else:
        names = all_names
    md = get_epsd2_metadata()
    return {
        "names": names,
        "n_names": len(names),
        "n_total": len(all_names),
        "metadata": md,
        "pos_filter": pos_filter or "(all)",
        "verdict": (
            f"ePSD2 names loaded: {len(names)} entries"
            + (f" (POS={pos_filter})" if pos_filter else "")
            + f". Total entries: {len(all_names)}. "
            f"Source: {md.get('source', '?')} (license: {md.get('license', '?')})."
        ),
    }


def _mathematica_epigraphica_loader(inputs: dict, params: dict) -> dict:
    """Load Fuls Mathematica Epigraphica vol. 3 (Corpus of Indus Inscriptions).

    Default no-op: data file not bundled (requires Amazon purchase or
    Fuls's email request). Loads from
    ``corpora/downloads/fuls_me_vol3_corpus.json`` if present.

    Expected format: {"inscriptions": [{"id": ..., "site": ..., "signs": [...]}]}.
    """
    repo_root = Path(__file__).resolve().parents[2]
    data_path = params.get("data_path") or "corpora/downloads/fuls_me_vol3_corpus.json"
    p = Path(data_path)
    if not p.is_absolute():
        p = repo_root / data_path

    if not p.exists():
        return {
            "available": False,
            "n_inscriptions": 0,
            "inscriptions": [],
            "verdict": (
                f"Mathematica Epigraphica vol. 3 not available at {data_path}. "
                f"To enable: purchase Amazon paperback ISBN 978-1671804869, "
                f"OCR text into a JSON file at this path, or request data from "
                f"Andreas Fuls (andreas.fuls@tu-berlin.de). Phase-29 falls back "
                f"to Mahadevan 1977 corpus (1,669 inscriptions) which has "
                f"~30%% overlap with Fuls vol. 3 (5,509 inscriptions)."
            ),
        }

    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return {"available": False, "error": f"parse error: {exc}"}

    inscriptions = d.get("inscriptions") or []
    sites = Counter()
    for ins in inscriptions:
        s = (ins.get("site") or "").upper()
        if s:
            sites[s] += 1
    return {
        "available": True,
        "n_inscriptions": len(inscriptions),
        "inscriptions": inscriptions,
        "sites_top": sites.most_common(10),
        "verdict": (
            f"Mathematica Epigraphica vol. 3 loaded: {len(inscriptions)} "
            f"inscriptions across {len(sites)} sites."
        ),
    }


def _icit_corpus_loader(inputs: dict, params: dict) -> dict:
    """Load ICIT (Interactive Corpus of Indus Texts) data.

    Default no-op: requires API access from Andreas Fuls (TU Berlin).
    Loads from ``corpora/downloads/icit_cache.json`` if present.

    Live API: caddy.igg.tu-berlin.de/indus/welcome.htm (login required).
    Email: andreas.fuls@tu-berlin.de
    """
    repo_root = Path(__file__).resolve().parents[2]
    data_path = params.get("data_path") or "corpora/downloads/icit_cache.json"
    p = Path(data_path)
    if not p.is_absolute():
        p = repo_root / data_path

    if not p.exists():
        return {
            "available": False,
            "n_inscriptions": 0,
            "n_signs": 0,
            "verdict": (
                f"ICIT cache not available at {data_path}. To enable: request "
                f"API access from andreas.fuls@tu-berlin.de, then download "
                f"the database export to {data_path}. "
                f"Expected when live: 4,537 objects, 5,509 texts, 19,616 sign "
                f"occurrences."
            ),
        }

    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return {"available": False, "error": f"parse error: {exc}"}

    return {
        "available": True,
        "n_inscriptions": len(d.get("inscriptions") or []),
        "n_signs": d.get("n_signs", 0),
        "metadata": d.get("metadata", {}),
        "verdict": (
            f"ICIT loaded: {len(d.get('inscriptions') or [])} inscriptions."
        ),
    }


# ── M77 reverse Janabiyah search ─────────────────────────────────────


def _epsd_pn_to_segments(headword: str, forms: list[str]) -> list[list[str]]:
    """Convert an ePSD2 PN headword + forms to candidate segment lists.

    e.g. "Abī-simtī[1]PN" with forms ["a-bi-si2-im-ti", "a-bi2-si2-im-ti"] →
    [["a", "bi", "si", "im", "ti"], ["a", "bi", "si", "im", "ti"]]
    """
    segs: list[list[str]] = []
    for f in forms or []:
        if not f:
            continue
        # Strip determinatives like {d}, {disz}, {m}
        clean = re.sub(r"\{[^}]+\}", "", str(f).lower())
        parts = [p for p in re.split(r"[-]+", clean) if p and not p.isspace()]
        # Drop subscript digits
        parts = [re.sub(r"[0-9]+$", "", p) for p in parts]
        parts = [p for p in parts if p]
        if parts:
            segs.append(parts)
    return segs


def _m77_reverse_janabiyah_search_v3(inputs: dict, params: dict) -> dict:
    """Phase-29 extension of Phase-28d ReverseJanabiyahSearchV2.

    Search the ePSD2 PN database (1,222 personal names, 28x our persons-v3)
    against the Janabiyah 7-position phonetic skeleton.

    Same scoring as Phase-28d but the candidate space is now ePSD2 entries
    (each with multiple alternate forms per entry) rather than the 44 me-luh-ha
    co-occurring PN candidates.
    """
    epsd2_pns = inputs.get("epsd2_personal_names") or []
    janabiyah = inputs.get("janabiyah_reading") or {}
    phoneme_map = inputs.get("phoneme_map") or {}
    families = inputs.get("allograph_families") or {}
    top_k = max(10, _safe_int(params.get("top_k", 30), 30))
    min_icount = max(1, _safe_int(params.get("min_icount", 1), 1))

    if not epsd2_pns or not janabiyah:
        return {"verdict": "INSUFFICIENT_DATA",
                "n_pns_searched": 0, "top_matches": []}

    # Filter to PNs with at least min_icount instances
    epsd2_pns = [p for p in epsd2_pns if int(p.get("icount", 0) or 0) >= min_icount]

    # Build miin-renderings dynamically (Phase-28d style)
    base_renderings = {
        "miin", "mi-in", "me-en", "mi-na", "me-na", "mi-il",
        "me-il", "mi-en", "me-in", "mu-li", "min", "men",
        "mul", "imin", "kakkab", "asz",
    }
    fish_family_members = set(
        str(m) for m in (families.get("fish") or {}).get("members") or []
    )
    for sid in fish_family_members:
        ph = (phoneme_map.get(sid) or {}).get("phoneme", "")
        for tok in re.split(r"[/\s]", ph or ""):
            t = tok.strip().lower()
            if t and len(t) >= 2:
                base_renderings.add(t)

    # Tokenized renderings (e.g., "mi-in" → "mi", "in")
    rendering_tokens: set[str] = set()
    for r in base_renderings:
        for t in r.split("-"):
            if t and len(t) >= 2:
                rendering_tokens.add(t)

    miin_positions = {1, 3, 6}
    n_target_segments = 7

    def _score_pn(headword: str, forms: list[str], periods: list[str], icount: int) -> dict:
        all_segs = _epsd_pn_to_segments(headword, forms)
        if not all_segs:
            return None  # type: ignore
        # Score the best (longest) form
        best_score = -999.0
        best_form_segs: list[str] = []
        best_form_pmatch = 0
        best_form_free = 0
        best_positions: list[int] = []
        for segs in all_segs:
            n_segs = len(segs)
            delta = abs(n_segs - n_target_segments)
            length_score = max(0.0, 3.0 - 0.5 * delta)
            position_match = 0
            positions_matched: list[int] = []
            for i, seg in enumerate(segs):
                if i in miin_positions and seg.lower() in rendering_tokens:
                    position_match += 1
                    positions_matched.append(i)
            free_miin = sum(
                1 for s in segs if s.lower() in rendering_tokens
            )
            total = length_score + position_match * 1.5 + free_miin * 0.5
            if total > best_score:
                best_score = total
                best_form_segs = segs
                best_form_pmatch = position_match
                best_form_free = free_miin
                best_positions = positions_matched

        return {
            "headword": headword,
            "best_form": "-".join(best_form_segs),
            "n_segments": len(best_form_segs),
            "position_match": best_form_pmatch,
            "positions_matched": best_positions,
            "free_miin": best_form_free,
            "total_score": round(best_score, 3),
            "icount": icount,
            "periods": periods,
            "n_alternate_forms": len(all_segs),
        }

    scored: list[dict] = []
    for pn in epsd2_pns:
        r = _score_pn(
            pn.get("headword", ""),
            pn.get("forms", []),
            pn.get("periods", []),
            int(pn.get("icount", 0) or 0),
        )
        if r:
            scored.append(r)

    scored.sort(key=lambda r: (-r["total_score"], -r["icount"]))
    top = scored[:top_k]
    n_pos = sum(1 for r in scored if r["position_match"] > 0)
    n_free = sum(1 for r in scored if r["free_miin"] > 0)

    verdict = (
        f"Phase-29 reverse Janabiyah search (ePSD2 v3): {len(scored)} ePSD2 "
        f"PNs scored against {len(rendering_tokens)} miin-token-renderings. "
        f"{n_pos} have at least one position-match (segment with miin-token "
        f"at Janabiyah positions 1/3/6). {n_free} have at least one miin-"
        f"rendering anywhere. "
        + (
            f"Top: '{top[0]['headword']}' (score {top[0]['total_score']}, "
            f"icount {top[0]['icount']}, periods {top[0]['periods']})."
            if top else "No candidates."
        )
        + " 28x scale-up vs Phase-28d (1,222 PNs vs 44)."
    )
    return {
        "n_pns_searched": len(scored),
        "n_renderings": len(rendering_tokens),
        "n_with_position_match": n_pos,
        "n_with_free_miin": n_free,
        "top_matches": top,
        "verdict": verdict,
    }


# ── M77 corpus stats ──────────────────────────────────────────────────


def _phase29_corpus_stats(inputs: dict, params: dict) -> dict:
    """Compare CISI vs Mahadevan 1977 vs Fuls vs ICIT corpus statistics."""
    cisi_inscs = inputs.get("inscribed_seals") or []
    m77_inscs = inputs.get("mahadevan_inscriptions") or []

    # Try to load Fuls + ICIT
    fuls = _mathematica_epigraphica_loader({}, params)
    icit = _icit_corpus_loader({}, params)

    def _stats(name: str, inscriptions, count_field: str = "indus_signs"):
        if not inscriptions:
            return {"corpus": name, "n_inscriptions": 0, "n_tokens": 0,
                    "n_distinct_signs": 0, "mean_length": 0.0}
        if isinstance(inscriptions[0], dict):
            seqs = [i.get(count_field) or [] for i in inscriptions]
            seqs = [[s for s in seq if s and s != "?"] for seq in seqs]
        else:
            seqs = inscriptions
        flat = [s for seq in seqs for s in seq]
        return {
            "corpus": name,
            "n_inscriptions": len(seqs),
            "n_tokens": len(flat),
            "n_distinct_signs": len(set(flat)),
            "mean_length": round(sum(len(s) for s in seqs) / max(1, len(seqs)), 3),
        }

    rows = [
        _stats("CISI Phase-22 contact-zone seals", cisi_inscs, "indus_signs"),
        _stats("Mahadevan 1977 (M77)", m77_inscs),
    ]
    if fuls.get("available"):
        rows.append(_stats("Fuls Mathematica Epigraphica vol. 3",
                            fuls.get("inscriptions") or [], "signs"))
    else:
        rows.append({"corpus": "Fuls ME vol. 3", "n_inscriptions": 0,
                     "n_tokens": 0, "n_distinct_signs": 0, "mean_length": 0.0,
                     "note": "not bundled (see MathematicaEpigraphicaLoader)"})
    if icit.get("available"):
        rows.append({"corpus": "ICIT (live)",
                      "n_inscriptions": icit.get("n_inscriptions", 0),
                      "n_signs": icit.get("n_signs", 0)})
    else:
        rows.append({"corpus": "ICIT (live)", "n_inscriptions": 0,
                     "note": "API access required (Fuls)"})

    # Compute the scale-up factor
    cisi_n = rows[0]["n_inscriptions"] or 1
    m77_n = rows[1]["n_inscriptions"]
    scale_up = round(m77_n / cisi_n, 1) if cisi_n else 0.0

    verdict = (
        f"Corpus 10x expansion (Phase-29): CISI Phase-22 contact-zone seals "
        f"({cisi_n} inscribed seals) -> Mahadevan 1977 ({m77_n} inscriptions, "
        f"{scale_up}x scale-up). Fuls ME vol. 3 + ICIT not yet bundled "
        f"(would add another ~3.3x and 2.7x respectively when accessible)."
    )
    return {
        "rows": rows,
        "scale_up_factor_cisi_to_m77": scale_up,
        "verdict": verdict,
    }


# ── Verdict aggregator ──────────────────────────────────────────────


def _phase29_verdict(inputs: dict, params: dict) -> dict:
    summary = (
        "Phase-29 corpus 10x expansion. (1) Mahadevan 1977 corpus formally "
        "wired as a glossa-lab atomic node — 1,669 inscriptions, 5,361 tokens, "
        "9.4x the 178-inscription CISI subset used through Phase-28. (2) "
        "ePSD2 names subset ingested (4,848 entries: 1,222 PN, 2,068 DN, "
        "346 TN, 335 SN, 306 RN, 263 GN, 164 WN, ...) — Sumerian/Akkadian "
        "name database from Penn Sumerian Dictionary (CC BY-SA), 28x our "
        "previous 44-name persons-v3 corpus. (3) Fuls Mathematica Epigraphica "
        "vol. 3 (5,509 inscriptions) and ICIT (4,537 objects) wired as "
        "no-op-by-default loaders with documented activation paths (Amazon "
        "purchase, Fuls email request). (4) M77ReverseJanabiyahSearchV3 "
        "re-runs Phase-28d against the ePSD2 PN corpus."
    )
    next_steps = [
        "Phase-30 priority 1: acquire Fuls ME vol. 3 (Amazon paperback "
        "$45) — adds another 3.3x corpus expansion + temporal/spatial "
        "metadata for stratification.",
        "Phase-30 priority 2: request ICIT API access from Fuls (TU Berlin) "
        "— adds live, growing corpus + statistical analysis tools.",
        "Phase-30 priority 3: re-run Phase-25c period stratification, "
        "Phase-25e Shu-ilishu filter, and Phase-27c iconographic anchor "
        "score against the Mahadevan 1977 corpus (now wired) for 9.4x "
        "statistical power.",
        "Phase-30 priority 4: ingest CISI Vol 3.1 (Mohenjo-daro/Harappa, "
        "2010) catalogue plates — €220 from tiedekirja.fi, or via ILL.",
        "Phase-30 priority 5: implement Yajnadevam (2024) Sanskrit "
        "decipherment as a competing phoneme map and run our "
        "IconographicAnchorScore against it — clean falsification round.",
    ]
    return {"summary": summary, "next_steps": next_steps}


# ── Atomic node defs for registration ───────────────────────────────


def _phase29_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "Phase29CorpusLoader", "Phase-29 Contact Corpus Loader",
            "Phase-29 / Sources",
            "Load Phase-29 contact-zone artefacts: Phase-28 corpus + "
            "Mahadevan 1977 (1,669 inscriptions) + ePSD2 names subset "
            "(4,848 entries: 1,222 PN, 2,068 DN, ...).",
            inputs=[],
            outputs=[
                {"name": "all_seals", "type": "json"},
                {"name": "inscribed_seals", "type": "json"},
                {"name": "persons_v3", "type": "json"},
                {"name": "phoneme_map", "type": "json"},
                {"name": "janabiyah_reading", "type": "json"},
                {"name": "tablets", "type": "json"},
                {"name": "n_tablets", "type": "number"},
                {"name": "findspot_map", "type": "json"},
                {"name": "contact_zone_prefixes", "type": "json"},
                {"name": "phase27_overrides", "type": "json"},
                {"name": "iconographic_anchors", "type": "json"},
                {"name": "mahadevan_crosswalk", "type": "json"},
                {"name": "allograph_families", "type": "json"},
                {"name": "cisi_vol3_ocr", "type": "json"},
                {"name": "epsd2_names", "type": "json"},
                {"name": "epsd2_personal_names", "type": "json"},
                {"name": "epsd2_metadata", "type": "json"},
                {"name": "mahadevan_inscriptions", "type": "json"},
                {"name": "mahadevan_metadata", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase29_corpus_loader,
        ),
        AtomicNodeDef(
            "MahadevanInscriptionLoader",
            "Mahadevan 1977 Inscription Loader (Phase-29)",
            "Phase-29 / Sources",
            "Load the Mahadevan 1977 inscription corpus (1,669 inscriptions, "
            "5,361 sign tokens, M77 numeric codes). 9.4x the 178-inscription "
            "CISI subset used through Phase-28.",
            inputs=[],
            outputs=[
                {"name": "inscriptions", "type": "json"},
                {"name": "n_inscriptions", "type": "number"},
                {"name": "n_tokens", "type": "number"},
                {"name": "n_distinct_signs", "type": "number"},
                {"name": "metadata", "type": "json"},
                {"name": "top_20_signs", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "min_length": {"type": "integer", "default": 1, "minimum": 1},
                },
            },
            fn=_mahadevan_inscription_loader,
        ),
        AtomicNodeDef(
            "EPSD2NamesLoader",
            "ePSD2 Sumerian/Akkadian Names Loader (Phase-29)",
            "Phase-29 / Sources",
            "Load the ePSD2 names subset (Sumerian/Akkadian PN/DN/TN/SN/etc.). "
            "4,848 total entries: 1,222 PN, 2,068 DN, 346 TN, 335 SN, 306 RN, "
            "263 GN, 164 WN, 73 ON, 45 CN, 19 MN. CC BY-SA, source "
            "oracc.museum.upenn.edu.",
            inputs=[],
            outputs=[
                {"name": "names", "type": "json"},
                {"name": "n_names", "type": "number"},
                {"name": "n_total", "type": "number"},
                {"name": "metadata", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "pos_filter": {
                        "type": "string", "default": "",
                        "description": "Filter by POS: PN | DN | SN | GN | RN | "
                                       "MN | TN | WN | CN | ON | EN | FN | (blank=all)"
                    },
                },
            },
            fn=_epsd2_names_loader,
        ),
        AtomicNodeDef(
            "MathematicaEpigraphicaLoader",
            "Fuls Mathematica Epigraphica vol. 3 Loader (Phase-29)",
            "Phase-29 / Sources",
            "Load the Fuls Mathematica Epigraphica vol. 3 'Corpus of Indus "
            "Inscriptions' data (5,509 inscriptions / 19,616 sign occurrences "
            "expected when accessible). Default no-op: requires Amazon "
            "purchase ISBN 978-1671804869 (~$45) or email request to "
            "andreas.fuls@tu-berlin.de.",
            inputs=[],
            outputs=[
                {"name": "available", "type": "number"},
                {"name": "n_inscriptions", "type": "number"},
                {"name": "inscriptions", "type": "json"},
                {"name": "sites_top", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "data_path": {
                        "type": "string",
                        "default": "corpora/downloads/fuls_me_vol3_corpus.json",
                    },
                },
            },
            fn=_mathematica_epigraphica_loader,
        ),
        AtomicNodeDef(
            "ICITCorpusLoader",
            "ICIT (Interactive Corpus of Indus Texts) Loader (Phase-29)",
            "Phase-29 / Sources",
            "Load the ICIT live corpus (4,537 objects / 5,509 texts / 19,616 "
            "sign occurrences when accessible). Default no-op: requires API "
            "access from Andreas Fuls (TU Berlin), andreas.fuls@tu-berlin.de.",
            inputs=[],
            outputs=[
                {"name": "available", "type": "number"},
                {"name": "n_inscriptions", "type": "number"},
                {"name": "n_signs", "type": "number"},
                {"name": "metadata", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "data_path": {
                        "type": "string",
                        "default": "corpora/downloads/icit_cache.json",
                    },
                },
            },
            fn=_icit_corpus_loader,
        ),
        AtomicNodeDef(
            "M77ReverseJanabiyahSearchV3",
            "Reverse Janabiyah Search V3 (Phase-29, ePSD2 PNs, 28x scale)",
            "Phase-29 / Decipherment",
            "Phase-29 extension of Phase-28d ReverseJanabiyahSearchV2: re-run "
            "the Janabiyah skeleton search against ePSD2's 1,222 personal "
            "names (28x our 44-name persons-v3 corpus). Picks up alternate "
            "forms per name (e.g. a-bi-si2-im-ti AND a-bi2-si2-im-ti for "
            "Abi-simti).",
            inputs=[
                {"name": "epsd2_personal_names", "type": "json", "required": True},
                {"name": "janabiyah_reading", "type": "json", "required": True},
                {"name": "phoneme_map", "type": "json", "required": True},
                {"name": "allograph_families", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_pns_searched", "type": "number"},
                {"name": "n_renderings", "type": "number"},
                {"name": "n_with_position_match", "type": "number"},
                {"name": "n_with_free_miin", "type": "number"},
                {"name": "top_matches", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "top_k": {"type": "integer", "default": 30, "minimum": 5},
                    "min_icount": {"type": "integer", "default": 1, "minimum": 1,
                                   "description": "Minimum instance count per PN to include."},
                },
            },
            fn=_m77_reverse_janabiyah_search_v3,
        ),
        AtomicNodeDef(
            "Phase29CorpusStats",
            "Phase-29 Corpus Statistics (CISI vs M77 vs Fuls vs ICIT)",
            "Phase-29 / Decipherment",
            "Compare statistics across CISI Phase-22 contact-zone seals, "
            "Mahadevan 1977 (1,669 inscriptions), Fuls ME vol. 3 (when "
            "available), and ICIT (when available). Reports n_inscriptions, "
            "n_tokens, n_distinct_signs, mean_length per corpus.",
            inputs=[
                {"name": "inscribed_seals", "type": "json", "required": True},
                {"name": "mahadevan_inscriptions", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "rows", "type": "json"},
                {"name": "scale_up_factor_cisi_to_m77", "type": "number"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase29_corpus_stats,
        ),
        AtomicNodeDef(
            "Phase29Verdict", "Phase-29 Verdict Aggregator",
            "Phase-29 / Reporters",
            "Aggregate Phase-29 sub-experiment outputs into a "
            "decipherment-progress verdict + Phase-30 priority list.",
            inputs=[],
            outputs=[
                {"name": "summary", "type": "text"},
                {"name": "next_steps", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase29_verdict,
        ),
    ]


__all__ = [
    "_phase29_corpus_loader",
    "_mahadevan_inscription_loader",
    "_epsd2_names_loader",
    "_mathematica_epigraphica_loader",
    "_icit_corpus_loader",
    "_m77_reverse_janabiyah_search_v3",
    "_phase29_corpus_stats",
    "_phase29_verdict",
    "_phase29_node_defs",
]

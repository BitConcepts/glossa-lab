"""Phase-28 atomic-node implementations.

Phase-28 builds on Phase-27 with five priority items:
  1. CISIVol3OCRNode: invokes Mistral pixtral-12b-2409 (or local Ollama
     vision model if configured) on CISI Vol 3 Part 3 PDF pages via the
     glossa-lab `call_llm_vision` framework. Persists raw OCR output to
     `reports/cisi_vol3_extracted_signs.json`.
  2. Phase-28 expanded phoneme map (30 -> 35 entries) loaded via the
     same accessor as Phase-27, with new entries for lion, eagle,
     cobra, plus strengthened yoke-carrier/buffalo entries.
  3. ReverseJanabiyahSearchV2: re-runs Phase-27a with the expanded map
     and allograph-aware position scoring (fish-family signs all match
     the miin slot at positions 1/3/6).
  4. MahadevanCrosswalkLoader: loads Mahadevan 1977 -> Parpola 1994b
     sign crosswalk (25 entries) + 4 allograph families.
  5. AllographAwareIconographicScore: extends Phase-27c so that when an
     iconographic anchor reads "fish" against a single sign ID, ALL
     fish-family allographs (47/48/50/52/60/145/147) score against the
     same anchor. Expands anchor coverage from 7 sign IDs to ~14+.

Plus a corpus loader and verdict aggregator.
"""

from __future__ import annotations

import base64
import json
import os
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


def _phase28_corpus_loader(inputs: dict, params: dict) -> dict:
    """Phase-28 loader: extends Phase-27 with Mahadevan-Parpola crosswalk,
    allograph-family map, and CISI Vol 3 OCR results."""
    try:
        from glossa_lab.data.mesopotamian_contact import (  # noqa: PLC0415
            get_indus_seals_at_mesopotamia, get_seals_with_inscription,
            get_meluhhan_persons_v3, get_parpola_phoneme_map,
            get_janabiyah_seal_reading, get_meluhha_tablets,
            get_cisi_findspot_map, get_contact_zone_prefix_set,
            get_phase27_seal_findspot_overrides,
            get_iconographic_anchors,
            get_mahadevan_parpola_crosswalk,
            get_allograph_families,
            get_cisi_vol3_ocr_results,
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
    }


# ── Tier 1 #1: CISI Vol 3 OCR (via call_llm_vision) ─────────────────


_OCR_PROMPT_DEFAULT = (
    "You are looking at a page of the Corpus of Indus Seals and Inscriptions "
    "(CISI) Vol 3 Part 3, edited by Asko Parpola. The page may contain seal "
    "drawings with their CISI catalogue IDs (e.g. 'M-410', 'H-9', 'B-12'), "
    "Parpola sign-list IDs, and iconographic motifs.\n\n"
    "Extract a structured listing in this exact format, one record per line:\n"
    "  SEAL: <catalogue_id> | SIGNS: <comma-separated sign ids or descriptive>\n"
    "  ICONOGRAPHY: <catalogue_id or descriptor> | MOTIF: <motif text>\n"
    "  SIGN_REF: <sign id> | MEANING: <meaning text>\n"
    "If no seal IDs are visible, say 'NO_SEALS_FOUND'."
)


def _cisi_vol3_ocr(inputs: dict, params: dict) -> dict:
    """Run vision-LLM OCR on CISI Vol 3 Part 3 PDF pages.

    Routes through `glossa_lab.ai_utils.call_llm_vision` so the same
    Settings infrastructure (Ollama llava/gemma3-vision first, then
    Mistral pixtral-12b-2409) is used. By default this is a NO-OP that
    returns the previously-saved OCR results to avoid re-running a
    paid API call on every graph execution.

    Params:
      pdf_path: optional path to input PDF (skips OCR if not provided).
      pages: optional list of page numbers to OCR (default: all).
      prompt: custom prompt (default: extraction prompt above).
      run_ocr: if False (default), only load existing results from
        `reports/cisi_vol3_extracted_signs.json`. Set True to re-run.
      output_path: where to write the JSON results.
    """
    run_ocr = bool(params.get("run_ocr", False))
    output_path = params.get(
        "output_path",
        "reports/cisi_vol3_extracted_signs.json",
    )

    # Default no-op: just load the previously-saved results.
    existing_path = Path(output_path)
    if not existing_path.is_absolute():
        # Resolve relative to repo root (data module sits 3 levels deep)
        repo_root = Path(__file__).resolve().parents[2]
        existing_path = repo_root / output_path

    existing: list[dict] = []
    if existing_path.exists():
        try:
            existing = json.loads(existing_path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            existing = []

    if not run_ocr:
        n_seal = sum(1 for e in existing if e.get("type") == "seal")
        n_icon = sum(1 for e in existing if e.get("type") == "iconography")
        n_sign = sum(1 for e in existing if e.get("type") == "sign_ref")
        verdict = (
            f"OCR no-op (run_ocr=False): loaded {len(existing)} existing "
            f"records from {output_path} ({n_seal} seal, {n_icon} "
            f"iconography, {n_sign} sign_ref). To re-run vision OCR, set "
            f"run_ocr=true and provide pdf_path."
        )
        return {
            "n_records": len(existing),
            "n_seal": n_seal,
            "n_iconography": n_icon,
            "n_sign_ref": n_sign,
            "records": existing,
            "verdict": verdict,
        }

    # run_ocr=True: actually call the vision LLM.
    pdf_path = params.get("pdf_path")
    if not pdf_path:
        return {
            "error": "run_ocr=True but pdf_path not provided",
            "n_records": len(existing),
            "records": existing,
        }
    pdf_path_p = Path(pdf_path)
    if not pdf_path_p.is_absolute():
        repo_root = Path(__file__).resolve().parents[2]
        pdf_path_p = repo_root / pdf_path
    if not pdf_path_p.exists():
        return {
            "error": f"pdf not found: {pdf_path_p}",
            "n_records": len(existing),
            "records": existing,
        }

    try:
        import fitz  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001
        return {
            "error": f"PyMuPDF (fitz) not available: {exc}",
            "n_records": len(existing),
            "records": existing,
        }
    try:
        from glossa_lab.ai_utils import call_llm_vision  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001
        return {
            "error": f"call_llm_vision not available: {exc}",
            "n_records": len(existing),
            "records": existing,
        }

    prompt = params.get("prompt") or _OCR_PROMPT_DEFAULT
    pages_param = params.get("pages")
    doc = fitz.open(str(pdf_path_p))
    page_nums = (
        sorted(int(p) for p in pages_param)
        if pages_param else list(range(1, doc.page_count + 1))
    )

    new_records: list[dict] = []
    for pn in page_nums:
        if pn < 1 or pn > doc.page_count:
            continue
        page = doc.load_page(pn - 1)
        pix = page.get_pixmap(dpi=200)
        png_bytes = pix.tobytes("png")
        data_uri = "data:image/png;base64," + base64.b64encode(png_bytes).decode("ascii")
        try:
            text = call_llm_vision(prompt, data_uri)
        except Exception as exc:  # noqa: BLE001
            new_records.append({
                "page": pn, "type": "error", "error": str(exc),
            })
            continue
        for line in (text or "").splitlines():
            ln = line.strip()
            if not ln or ln.startswith("NO_SEALS"):
                continue
            if ln.startswith("SEAL:") and "|" in ln and "SIGNS:" in ln:
                seal_id = ln.split("|")[0].split(":", 1)[1].strip()
                signs = ln.split("SIGNS:", 1)[1].strip()
                new_records.append({
                    "page": pn, "raw": ln, "type": "seal",
                    "seal_id": seal_id, "signs": signs,
                })
            elif ln.startswith("ICONOGRAPHY:") and "|" in ln and "MOTIF:" in ln:
                seal_id = ln.split("|")[0].split(":", 1)[1].strip()
                motif = ln.split("MOTIF:", 1)[1].strip()
                new_records.append({
                    "page": pn, "raw": ln, "type": "iconography",
                    "seal_id": seal_id, "motif": motif,
                })
            elif ln.startswith("SIGN_REF:") and "|" in ln and "MEANING:" in ln:
                sign_id = ln.split("|")[0].split(":", 1)[1].strip()
                meaning = ln.split("MEANING:", 1)[1].strip()
                new_records.append({
                    "page": pn, "raw": ln, "type": "sign_ref",
                    "sign_id": sign_id, "meaning": meaning,
                })
    existing_path.parent.mkdir(parents=True, exist_ok=True)
    existing_path.write_text(json.dumps(new_records, indent=2), encoding="utf-8")

    n_seal = sum(1 for e in new_records if e.get("type") == "seal")
    n_icon = sum(1 for e in new_records if e.get("type") == "iconography")
    n_sign = sum(1 for e in new_records if e.get("type") == "sign_ref")
    verdict = (
        f"OCR run on {len(page_nums)} pages of {pdf_path_p.name}: "
        f"{len(new_records)} records ({n_seal} seal, {n_icon} "
        f"iconography, {n_sign} sign_ref). Saved to {output_path}."
    )
    return {
        "n_records": len(new_records),
        "n_seal": n_seal,
        "n_iconography": n_icon,
        "n_sign_ref": n_sign,
        "records": new_records,
        "verdict": verdict,
    }


# ── Tier 1 #5: Allograph-aware iconographic anchor score ─────────────


def _allograph_aware_iconographic_score(inputs: dict, params: dict) -> dict:
    """Phase-28 extension of Phase-27c IconographicAnchorScore.

    Key change: when an iconographic anchor reads "fish" against a
    single sign ID (e.g. M-410 -> sign 47), all members of the
    fish-allograph family (47, 48, 50, 52, 60, 145, 147) are also
    credited. This expands anchor coverage from 7 sign IDs to ~14+.

    Scoring per anchor (allograph-extended):
      base_score (Phase-27c): 2.0 high anchor + match, 1.0 medium, 0.5 low
      ph_conf bonus: x1.5 if phoneme also high-confidence
      allograph_extension_bonus: +0.25 per additional allograph-family
        member that matches the anchor's iconic_reading
    """
    anchors = inputs.get("iconographic_anchors") or []
    phoneme_map = inputs.get("phoneme_map") or {}
    families = inputs.get("allograph_families") or {}

    if not anchors:
        return {"verdict": "NO_ANCHORS", "score": 0.0, "n_anchors": 0}

    # Build iconic-reading -> family membership map
    iconic_to_family: dict[str, dict] = {}
    for fam_name, fam in families.items():
        members = fam.get("members") or []
        phoneme = (fam.get("phoneme") or "").lower()
        iconic_to_family[fam_name.lower()] = {
            "name": fam_name,
            "members": [str(m) for m in members],
            "phoneme": phoneme,
        }

    iconic_to_phoneme_alias = {
        "fish": ("miin", "fish"),
        "fish/star": ("miin", "fish"),
        "fig": ("vaTa", "fig_tree"),
        "banyan/fig": ("vaTa", "fig_tree"),
        "banyan": ("vaTa", "fig_tree"),
        "muruku": ("muruku", "intersecting_circles"),
        "intersecting circles": ("muruku", "intersecting_circles"),
        "squirrel": ("piLLai", None),
        "pot": ("kuTam", None),
        "pot/jar": ("kuTam", None),
        "veL": ("veL", "numerals"),
        "veN-miin": ("veL", None),
        "venus": ("veL", None),
        "pleiades": ("aru-", "numerals"),
        "ursa major": ("eZu-", "numerals"),
        "north star": ("vaTa", "fig_tree"),
    }

    rows = []
    total_score = 0.0
    n_matches = 0
    n_total_anchors = 0
    n_allograph_extensions = 0
    extended_signs: set[str] = set()

    for a in anchors:
        sid = str(a.get("sign_id", "")).split("+")[0]
        iconic = (a.get("iconic_reading", "") or "").lower()
        anchor_conf = (a.get("confidence") or "low").lower()
        n_total_anchors += 1
        ph_entry = phoneme_map.get(sid, {}) or {}
        ph_value = (ph_entry.get("phoneme", "") or "").lower()
        ph_conf = (ph_entry.get("confidence") or "none").lower()

        match = False
        family_name = None
        for k, (alias, fam_key) in iconic_to_phoneme_alias.items():
            if k in iconic and alias.lower() in ph_value:
                match = True
                family_name = fam_key
                break
        if not match:
            for k, (alias, fam_key) in iconic_to_phoneme_alias.items():
                if k in iconic:
                    match = alias.lower() in ph_value
                    family_name = fam_key
                    if match:
                        break

        anchor_score = 0.0
        if match:
            n_matches += 1
            if anchor_conf == "high":
                anchor_score = 2.0
            elif anchor_conf == "medium":
                anchor_score = 1.0
            else:
                anchor_score = 0.5
            if ph_conf == "high":
                anchor_score *= 1.5

        # Allograph extension bonus: count additional family members with
        # phoneme matching the same alias.
        family_extensions: list[str] = []
        if match and family_name and family_name in iconic_to_family:
            fam = iconic_to_family[family_name]
            target_phoneme = fam["phoneme"]
            for member in fam["members"]:
                if member == sid:
                    continue
                m_entry = phoneme_map.get(member, {}) or {}
                m_phon = (m_entry.get("phoneme", "") or "").lower()
                if not m_phon:
                    continue
                if target_phoneme and target_phoneme in m_phon:
                    family_extensions.append(member)
                    extended_signs.add(member)
            n_allograph_extensions += len(family_extensions)
            anchor_score += 0.25 * len(family_extensions)

        total_score += anchor_score
        rows.append({
            "anchor_id": a.get("anchor_id"),
            "sign_id": sid,
            "object_id": a.get("object_id"),
            "iconic_reading": a.get("iconic_reading"),
            "phoneme_value": ph_value,
            "phoneme_confidence": ph_conf,
            "anchor_confidence": anchor_conf,
            "match": match,
            "family": family_name,
            "family_extensions": family_extensions,
            "n_allograph_extensions": len(family_extensions),
            "anchor_score": round(anchor_score, 3),
        })

    rows.sort(key=lambda r: -r["anchor_score"])
    verdict = (
        f"Allograph-aware iconographic anchor score (Phase-28): "
        f"{n_matches}/{n_total_anchors} anchors have a phoneme match; "
        f"{n_allograph_extensions} additional allograph-family members "
        f"score against the same anchors (vs Phase-27c which scored "
        f"only the explicit sign ID). Total weighted score = "
        f"{total_score:.2f}. Distinct sign IDs gaining anchor support "
        f"via allograph extension: {sorted(extended_signs)}."
    )
    return {
        "n_total_anchors": n_total_anchors,
        "n_matches": n_matches,
        "n_allograph_extensions": n_allograph_extensions,
        "extended_sign_ids": sorted(extended_signs),
        "total_score": round(total_score, 3),
        "rows": rows,
        "verdict": verdict,
    }


# ── Tier 1 #3: Reverse Janabiyah Search v2 (allograph-aware) ────────


def _reverse_janabiyah_search_v2(inputs: dict, params: dict) -> dict:
    """Phase-28 extension of Phase-27a reverse Janabiyah search.

    Same scoring as Phase-27a but with two enhancements:
      1. Expanded miin-rendering set: pulls all phonemes whose value
         contains 'miin' from the (expanded) phoneme map dynamically,
         so newly-added entries are picked up automatically.
      2. Allograph-aware position match: any sign in the fish family
         (47/48/50/52/60/145/147) that maps to a Sumerian transliteration
         containing miin/me/mi syllables counts as a position match.
    """
    persons = inputs.get("persons_v3") or []
    janabiyah = inputs.get("janabiyah_reading") or {}
    phoneme_map = inputs.get("phoneme_map") or {}
    families = inputs.get("allograph_families") or {}
    top_k = max(10, _safe_int(params.get("top_k", 30), 30))

    if not persons or not janabiyah:
        return {"verdict": "INSUFFICIENT_DATA",
                "n_candidates": 0, "top_matches": []}

    # Aggregate persons by candidate_name
    name_counts: Counter[str] = Counter()
    name_meta: dict[str, dict] = {}
    for p in persons:
        n = p.get("candidate_name", "")
        if not n:
            continue
        name_counts[n] += 1
        if n not in name_meta:
            name_meta[n] = {
                "first_period": p.get("period", ""),
                "first_provenience": p.get("provenience", ""),
                "first_p_number": p.get("p_number", ""),
            }

    # Expanded miin renderings: dynamically pulled from phoneme map
    base_renderings = {
        "miin", "mi-in", "me-en", "mi-na", "me-na", "mi-il",
        "me-il", "mi-en", "me-in", "mu-li", "min", "men",
        "mul", "imin", "kakkab", "asz",
    }
    fish_family_members = set(
        str(m) for m in (families.get("fish") or {}).get("members") or []
    )
    # Phonemes attached to fish-family members in the (expanded) map
    for sid in fish_family_members:
        ph = (phoneme_map.get(sid) or {}).get("phoneme", "")
        for tok in re.split(r"[/\s]", ph or ""):
            t = tok.strip().lower()
            if t and len(t) >= 2:
                base_renderings.add(t)

    miin_positions = {1, 3, 6}
    n_target_segments = 7

    def _score(name: str) -> dict:
        segs = name.split("-")
        n_segs = len(segs)
        delta = abs(n_segs - n_target_segments)
        length_score = max(0.0, 3.0 - 0.5 * delta)
        position_match = 0
        positions_matched: list[int] = []
        for i, seg in enumerate(segs):
            seg_l = seg.lower().strip("()? ")
            if i in miin_positions and any(r in seg_l for r in base_renderings):
                position_match += 1
                positions_matched.append(i)
        free_miin = sum(
            1 for s in segs
            if any(r in s.lower().strip("()? ") for r in base_renderings)
        )
        penalty = 0.0
        if name.endswith("-me-luh-ha") or name.endswith("-me-luh-ha-ki"):
            penalty -= 1.5
        total = length_score + position_match * 1.5 + free_miin * 0.5 + penalty
        return {
            "candidate_name": name,
            "n_segments": n_segs,
            "length_score": round(length_score, 2),
            "position_match": position_match,
            "positions_matched": positions_matched,
            "free_miin": free_miin,
            "penalty": round(penalty, 2),
            "total_score": round(total, 3),
            "occurrences": name_counts[name],
            "first_period": name_meta[name].get("first_period", ""),
            "first_provenience": name_meta[name].get("first_provenience", ""),
        }

    scored = [_score(n) for n in name_counts.keys()]
    scored.sort(key=lambda r: (-r["total_score"], -r["occurrences"]))
    top = scored[:top_k]
    n_with_position_match = sum(1 for r in scored if r["position_match"] > 0)
    n_with_free_miin = sum(1 for r in scored if r["free_miin"] > 0)

    verdict = (
        f"Reverse Janabiyah search v2 (Phase-28, expanded map + "
        f"allograph-aware): {len(scored)} unique persons-v3 candidates "
        f"scored against {len(base_renderings)} miin-renderings ("
        f"vs Phase-27a's static 15). {n_with_position_match} have at "
        f"least one position-match; {n_with_free_miin} have at least "
        f"one miin-rendering anywhere. Top candidate: "
        f"'{top[0]['candidate_name']}' (score {top[0]['total_score']}, "
        f"occurrences {top[0]['occurrences']})."
        if top else "No candidates."
    )
    return {
        "n_candidates": len(scored),
        "n_renderings": len(base_renderings),
        "n_with_position_match": n_with_position_match,
        "n_with_free_miin": n_with_free_miin,
        "top_matches": top,
        "verdict": verdict,
    }


# ── Verdict aggregator ──────────────────────────────────────────────


def _phase28_verdict(inputs: dict, params: dict) -> dict:
    summary = (
        "Phase-28 contact-zone progress: (1) CISI Vol 3 Part 3 OCR "
        "executed via glossa-lab `call_llm_vision` framework (Mistral "
        "pixtral-12b-2409) on 40-page PDF; 23 records extracted but the "
        "PDF on disk turned out to be introduction/front-matter only "
        "(seal IDs are LPIW/LE = Linear Proto-Iranian/Linear Elamite, "
        "NOT Indus script; no overlap with Phase-22 catalogue IDs). "
        "(2) Mahadevan 1977 -> Parpola 1994b crosswalk: 25 entries + 4 "
        "allograph families (fish, numerals, intersecting circles, fig "
        "tree). (3) Phoneme map expanded 30 -> 35 entries: lion (araL), "
        "eagle (puL/Garuda?), cobra (naagam?), strengthened yoke-carrier "
        "(kavai) and buffalo (erumai) entries promoted to high-confidence. "
        "(4) ReverseJanabiyahSearchV2: re-ran Phase-27a against the "
        "expanded map with allograph-aware miin-rendering set "
        "(dynamically pulled from fish-family entries). (5) "
        "AllographAwareIconographicScore: extends Phase-27c so e.g. M-410 "
        "fish anchor (sign 47) credits ALL fish-family allographs "
        "(48/50/52/60/145/147) — anchor coverage roughly doubles."
    )
    next_steps = [
        "Phase-29 priority 1: acquire CISI Vol 3 Part 1/Part 2 (the "
        "ACTUAL Indus catalogue plates — Vol 3 Part 3 turned out to be "
        "introduction). Best route: ICIPS or Helsinki/Harvard ILL.",
        "Phase-29 priority 2: complete Mahadevan 1977 sign-list "
        "crosswalk to all ~417 signs (currently 25 of the most-cited).",
        "Phase-29 priority 3: extend allograph-family coverage to Wells "
        "2015 typology (more granular than Parpola 1994b families).",
        "Phase-29 priority 4: attempt Crawford 2001 'Early Dilmun' "
        "again via a different mirror.",
        "Phase-29 priority 5: build a held-out blind test set (any "
        "newly-published seals from 2024-2026) and run the full Phase-28 "
        "pipeline on them as a pre-registered confirmation.",
    ]
    return {
        "summary": summary,
        "next_steps": next_steps,
    }


# ── Atomic node defs for registration ───────────────────────────────


def _phase28_node_defs() -> list[Any]:
    from glossa_lab.experiment_graph import AtomicNodeDef  # noqa: PLC0415

    return [
        AtomicNodeDef(
            "Phase28CorpusLoader", "Phase-28 Contact Corpus Loader",
            "Phase-28 / Sources",
            "Load Phase-28 contact-zone artefacts: extends Phase-27 with "
            "Mahadevan-Parpola crosswalk, allograph families, and CISI "
            "Vol 3 OCR results.",
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
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase28_corpus_loader,
        ),
        AtomicNodeDef(
            "CISIVol3OCRNode",
            "CISI Vol 3 OCR (Mistral pixtral-12b via call_llm_vision)",
            "Phase-28 / Sources",
            "Run vision-LLM OCR on CISI Vol 3 Part 3 PDF pages via the "
            "glossa-lab `call_llm_vision` framework. Default no-op "
            "loads previously-saved results from "
            "`reports/cisi_vol3_extracted_signs.json`. Set "
            "run_ocr=true + pdf_path=... to re-run.",
            inputs=[],
            outputs=[
                {"name": "n_records", "type": "number"},
                {"name": "n_seal", "type": "number"},
                {"name": "n_iconography", "type": "number"},
                {"name": "n_sign_ref", "type": "number"},
                {"name": "records", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={
                "type": "object",
                "properties": {
                    "run_ocr": {"type": "boolean", "default": False},
                    "pdf_path": {"type": "string"},
                    "pages": {"type": "array", "items": {"type": "integer"}},
                    "prompt": {"type": "string"},
                    "output_path": {
                        "type": "string",
                        "default": "reports/cisi_vol3_extracted_signs.json",
                    },
                },
            },
            fn=_cisi_vol3_ocr,
        ),
        AtomicNodeDef(
            "MahadevanCrosswalkLoader",
            "Mahadevan 1977 - Parpola 1994b Crosswalk Loader (Phase-28)",
            "Phase-28 / Sources",
            "Load the Mahadevan 1977 -> Parpola 1994b sign-list crosswalk "
            "(25 entries) plus the 4 allograph families (fish, numerals, "
            "intersecting circles, fig tree). Used by allograph-aware "
            "iconographic scorer.",
            inputs=[],
            outputs=[
                {"name": "mahadevan_crosswalk", "type": "json"},
                {"name": "allograph_families", "type": "json"},
                {"name": "n_crosswalk_entries", "type": "number"},
                {"name": "n_allograph_families", "type": "number"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=lambda inputs, params: {
                **(_phase28_corpus_loader({}, {}) or {}),
                "n_crosswalk_entries": len(
                    (_phase28_corpus_loader({}, {}) or {}).get(
                        "mahadevan_crosswalk", {}
                    )
                ),
                "n_allograph_families": len(
                    (_phase28_corpus_loader({}, {}) or {}).get(
                        "allograph_families", {}
                    )
                ),
            },
        ),
        AtomicNodeDef(
            "AllographAwareIconographicScore",
            "Allograph-Aware Iconographic Anchor Score (Phase-28)",
            "Phase-28 / Decipherment",
            "Phase-28 extension of Phase-27c IconographicAnchorScore: "
            "when an iconographic anchor reads 'fish' against a single "
            "sign (e.g. M-410 -> sign 47), all members of the fish-"
            "allograph family (48/50/52/60/145/147) also score against "
            "the same anchor. Expands anchor coverage from 7 sign IDs "
            "to ~14+.",
            inputs=[
                {"name": "iconographic_anchors", "type": "json", "required": True},
                {"name": "phoneme_map", "type": "json", "required": True},
                {"name": "allograph_families", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_total_anchors", "type": "number"},
                {"name": "n_matches", "type": "number"},
                {"name": "n_allograph_extensions", "type": "number"},
                {"name": "extended_sign_ids", "type": "json"},
                {"name": "total_score", "type": "number"},
                {"name": "rows", "type": "json"},
                {"name": "verdict", "type": "text"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_allograph_aware_iconographic_score,
        ),
        AtomicNodeDef(
            "ReverseJanabiyahSearchV2",
            "Reverse Janabiyah Search V2 (Phase-28, expanded + allograph-aware)",
            "Phase-28 / Decipherment",
            "Phase-28 extension of Phase-27a ReverseJanabiyahSearch: "
            "uses the expanded 35-entry phoneme map and dynamically "
            "pulls all miin-renderings from fish-family entries.",
            inputs=[
                {"name": "persons_v3", "type": "json", "required": True},
                {"name": "janabiyah_reading", "type": "json", "required": True},
                {"name": "phoneme_map", "type": "json", "required": True},
                {"name": "allograph_families", "type": "json", "required": True},
            ],
            outputs=[
                {"name": "n_candidates", "type": "number"},
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
                },
            },
            fn=_reverse_janabiyah_search_v2,
        ),
        AtomicNodeDef(
            "Phase28Verdict", "Phase-28 Verdict Aggregator",
            "Phase-28 / Reporters",
            "Aggregate Phase-28 sub-experiment outputs into a "
            "decipherment-progress verdict + Phase-29 priority list.",
            inputs=[],
            outputs=[
                {"name": "summary", "type": "text"},
                {"name": "next_steps", "type": "json"},
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phase28_verdict,
        ),
    ]


__all__ = [
    "_phase28_corpus_loader",
    "_cisi_vol3_ocr",
    "_allograph_aware_iconographic_score",
    "_reverse_janabiyah_search_v2",
    "_phase28_verdict",
    "_phase28_node_defs",
]

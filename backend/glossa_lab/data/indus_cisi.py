"""Indus Script CISI corpus loader — real multi-sign inscription sequences.

Source: mayig/indus-valley-script-corpus (GitHub, MIT License, 2024-2025).
        A digitization of the Corpus of Indus Seals and Inscriptions (CISI)
        by Parpola et al. (1987-2010) in JSON format.
        https://github.com/mayig/indus-valley-script-corpus

Stats (as of April 2026 download):
  - 179 inscription sides (all Mohenjo-daro, site prefix 'M')
  - 1,003 sign tokens
  - 182 distinct signs (Parpola numbering: P001–P450)
  - Mean inscription length: 5.6 signs (range 1–13)
  - 99% multi-sign inscriptions (178/179 have >= 2 signs)

Sign IDs: Parpola (1982) allograph numbers, e.g. 'P324', 'P122', 'P086'.
These differ from the Mahadevan M77 numbering used in the ICIT synthetic corpus.

Key difference from BuiltinCorpus('indus'):
  - ICIT corpus: 4,513 single-sign sequences (no inscription structure)
  - CISI corpus: 179 real multi-sign sequences with full inscription structure

The CISI corpus enables:
  - Meaningful positional profiling (I/M/T rates per sign)
  - Bigram and trigram analysis
  - Contact zone analysis (when H/L/DK sites added in future repo updates)
  - Anchor convergence benchmarks with realistic inscription length distribution

Attribution:
  Corpus digitization by mcskware (MIT License).
  Original physical corpus: Parpola, A. et al. (1987–2010) Corpus of Indus
  Seals and Inscriptions, Vols. 1–3. Suomalainen Tiedeakatemia, Helsinki.
"""

from __future__ import annotations

import json
from pathlib import Path

# ── Corpus file location ──────────────────────────────────────────────────────
# data/indus_cisi_corpus.json is downloaded by scripts/download_indus_cisi.py
# and lives in glossa-lab/data/ (same directory as rigveda_clean.json).

_CORPUS_FILE_CANDIDATES = [
    Path(__file__).resolve().parents[3] / "data" / "indus_cisi_corpus.json",
    Path(__file__).resolve().parents[2] / "data" / "indus_cisi_corpus.json",
]

_CORPUS_CACHE: list[dict] | None = None


def _load_corpus() -> list[dict]:
    """Load the CISI JSON corpus from disk. Cached after first call.

    Handles two formats:
      - Legacy (original mayig): top-level list of {id, graphemes: [{id}]}
      - Phase-44 rebuild: top-level dict with {inscriptions: [{id, signs: [...]}]}
    """
    global _CORPUS_CACHE  # noqa: PLW0603
    if _CORPUS_CACHE is not None:
        return _CORPUS_CACHE

    # Also check the path inside glossa_lab/data/ (where Phase 44 wrote it)
    extra_candidates = [
        Path(__file__).resolve().parent / "indus_cisi_corpus.json",
    ]
    for p in _CORPUS_FILE_CANDIDATES + extra_candidates:
        if p.exists():
            raw = json.loads(p.read_text("utf-8"))
            # Phase-44 format: dict with 'inscriptions' key
            if isinstance(raw, dict) and "inscriptions" in raw:
                inscs = raw["inscriptions"]
                # Normalise to legacy format: add 'graphemes' from 'signs'
                normalised: list[dict] = []
                for rec in inscs:
                    if not isinstance(rec, dict):
                        continue
                    signs_raw = rec.get("signs") or rec.get("graphemes") or []
                    if signs_raw and isinstance(signs_raw[0], str):
                        # signs is a flat list of strings like ["P121", "P202"]
                        graphemes = [{"id": s} for s in signs_raw if s]
                    else:
                        # already in legacy {"id": ...} form
                        graphemes = signs_raw
                    normalised.append({**rec, "graphemes": graphemes})
                _CORPUS_CACHE = normalised
            else:
                # Legacy format: already a list of dicts with 'graphemes'
                _CORPUS_CACHE = raw if isinstance(raw, list) else []
            return _CORPUS_CACHE

    raise FileNotFoundError(
        "indus_cisi_corpus.json not found. "
        "Run backend/scripts/download_indus_cisi.py to download it."
    )


# ── Public API ────────────────────────────────────────────────────────────────


def get_corpus_inscriptions(
    site: str | None = None,
    min_length: int = 2,
) -> list[list[str]]:
    """Return multi-sign inscription sequences from the CISI corpus.

    Each element is one inscription side, represented as a list of Parpola
    sign IDs. Only inscriptions with >= min_length signs are included.

    Args:
        site:        Optional site prefix filter: 'M' (Mohenjo-daro),
                     'H' (Harappa), 'L' (Lothal), 'DK' (Dholavira).
                     None = all sites.
        min_length:  Minimum number of signs per inscription (default 2).

    Returns:
        List of sequences, e.g. [['P121','P202','P385','P073','P108'], ...]
    """
    corpus = _load_corpus()
    seqs = []
    for insc in corpus:
        if site is not None:
            insc_site = insc.get("id", "").split("-")[0]
            if insc_site != site:
                continue
        graphemes = insc.get("graphemes") or []
        signs = [g["id"] for g in graphemes if g.get("id")]
        if len(signs) >= min_length:
            seqs.append(signs)
    return seqs


def get_corpus_symbols(site: str | None = None) -> list[str]:
    """Return a flat list of sign tokens from all CISI inscriptions.

    Suitable for building a unigram/bigram LanguageModel.

    Args:
        site: Optional site filter (see get_corpus_inscriptions).
    """
    seqs = get_corpus_inscriptions(site=site, min_length=1)
    return [sign for seq in seqs for sign in seq]


def get_inscriptions_by_site() -> dict[str, list[list[str]]]:
    """Return inscription sequences grouped by site prefix.

    Returns:
        Dict mapping site code to list of sign sequences.
        e.g. {'M': [...], 'H': [...], 'L': [...], 'DK': [...]}
    """
    corpus = _load_corpus()
    result: dict[str, list[list[str]]] = {}
    for insc in corpus:
        site_code = insc.get("id", "?").split("-")[0]
        graphemes = insc.get("graphemes") or []
        signs = [g["id"] for g in graphemes if g.get("id")]
        if len(signs) >= 2:
            result.setdefault(site_code, []).append(signs)
    return result


# ── Phase-27: catalogue_id-aware accessors ────────────────────────────────────
#
# Phase-26e revealed that the existing get_corpus_inscriptions() drops the
# catalogue_id (e.g. 'M-001'), preventing provenience-based filtering. The
# accessors below preserve the catalogue_id so downstream nodes can filter
# by site prefix.


def get_corpus_inscriptions_with_ids(
    site: str | None = None,
    min_length: int = 2,
) -> list[dict]:
    """Return inscription sequences as ``[{catalogue_id, signs}]`` (Phase-27).

    Same filter semantics as :func:`get_corpus_inscriptions` but each
    element is a dict ``{'catalogue_id': str, 'signs': list[str]}``.
    Enables provenience-aware filtering by CISI site prefix.
    """
    corpus = _load_corpus()
    out: list[dict] = []
    for insc in corpus:
        cid = insc.get("id", "") or ""
        if site is not None and cid.split("-")[0] != site:
            continue
        graphemes = insc.get("graphemes") or []
        signs = [g["id"] for g in graphemes if g.get("id")]
        if len(signs) >= min_length:
            out.append({"catalogue_id": cid, "signs": signs})
    return out


def get_inscriptions_filtered_by_prefix(
    prefixes: set[str] | list[str] | tuple[str, ...],
    min_length: int = 2,
    max_length: int | None = None,
) -> list[dict]:
    """Return inscriptions whose catalogue_id starts with any of the given
    site prefixes (Phase-27).

    Used to filter the Shu-ilishu candidate list to contact-zone seals.
    """
    if not prefixes:
        return []
    pset = {p for p in prefixes if p}
    out: list[dict] = []
    for entry in get_corpus_inscriptions_with_ids(min_length=min_length):
        cid = entry["catalogue_id"]
        # Try the longest prefix first (4-, 3-, 2-, 1-letter) so 'Gks5' beats 'G'
        for L in (4, 3, 2, 1):
            if cid[:L] in pset:
                if max_length is not None and len(entry["signs"]) > max_length:
                    break
                out.append(entry)
                break
    return out


def get_corpus_metadata() -> dict:
    """Return summary statistics for the loaded CISI corpus."""
    corpus = _load_corpus()
    all_signs = [g["id"] for insc in corpus for g in (insc.get("graphemes") or [])]
    from collections import Counter  # noqa: PLC0415
    sign_freq = Counter(all_signs)
    lengths = [len(insc.get("graphemes") or []) for insc in corpus]
    sites = Counter(insc.get("id", "?").split("-")[0] for insc in corpus)
    return {
        "n_inscriptions": len(corpus),
        "n_tokens": len(all_signs),
        "n_distinct_signs": len(sign_freq),
        "mean_length": round(sum(lengths) / max(len(lengths), 1), 2),
        "max_length": max(lengths, default=0),
        "sites": dict(sites),
        "top_10_signs": sign_freq.most_common(10),
        "sign_numbering": "Parpola (1982)",
        "source": "mayig/indus-valley-script-corpus (MIT, GitHub)",
    }

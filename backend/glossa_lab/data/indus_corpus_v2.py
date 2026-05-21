"""Indus Script Corpus v2 — Real multi-source inscription loader.

Loads from glossa-corpus/indus/exports/indus_research.jsonl (the
rights-cleared research export built by corpus_indus_export.py).

Drop-in replacement for indus_public_corpus.py (synthetic prototype).
Exposes the same interface as all other Glossa Lab corpus modules:
    load_corpus() -> list[list[int]]

Falls back gracefully:
  1. Real corpus from exports/indus_research.jsonl (preferred)
  2. CISI subset from indus_cisi.py (179 real Mohenjo-daro inscriptions)
  3. Synthetic prototype from indus_public_corpus.py (last resort)

Status tracking:
  - call corpus_status() to see what tier is active and coverage %
  - call load_corpus(as_objects=True) for rich dict records instead of int lists

Sign ID mapping:
  - Parpola (P-number) source IDs are converted to integer Mahadevan IDs
    where a crosswalk entry exists; unmapped signs use P-number as fallback int
  - Fuls/Wells 3-digit IDs are preserved as-is (already ints)

_citation:
  primary_sources: ["A.1", "A.7", "I.1", "I.2", "I.3", "I.4", "I.5"]
  derivation: "Data loader for ICIT-scale Indus corpus reconstruction.
               Loads from glossa-corpus/indus/exports/indus_research.jsonl.
               Falls back to indus_cisi.py (CISI subset) or indus_public_corpus.py
               (synthetic prototype) if the real corpus is not yet built."
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List, Optional, Union

_REPO = Path(__file__).parents[3]
_EXPORT_PATH = _REPO / "glossa-corpus" / "indus" / "exports" / "indus_research.jsonl"
_ICIT_PATH = _REPO / "glossa-corpus" / "indus" / "exports" / "indus_icit_format.json"

_CACHE: Optional[list] = None
_TIER: Optional[str] = None


# ── Sign ID parsing ───────────────────────────────────────────────────────────

def _parse_diplomatic_to_ints(diplomatic: str, scheme: Optional[str] = None) -> List[int]:
    """
    Parse ICIT diplomatic string to list of integer sign IDs.

    Rules:
      - Strip outer + markers
      - Split on hyphens
      - Skip damage markers (000, ++)
      - Convert Parpola/Wells/Fuls 3-digit IDs to int
      - Return empty list on failure
    """
    if not diplomatic:
        return []
    text = diplomatic.strip()
    # Remove ++ (eroded unknown length) and normalize
    text = re.sub(r'\+\+', '-', text)
    # Remove outer + markers
    text = text.strip("+")
    parts = [p.strip() for p in text.split("-") if p.strip()]
    ids = []
    for p in parts:
        if p == "000" or p == "":
            continue  # skip eroded signs
        if p.startswith("*"):
            continue  # FIX Phase-43: skip RMRL *NNN supplementary signs (not in Holdat)
        try:
            # FIX: zero-pad to 3 digits to match M77 Holdat format
            # "67" -> "067", "342" -> "342", "8" -> "008"
            ids.append(str(int(p)).zfill(3))
        except ValueError:
            continue
    return ids


def _load_from_jsonl(path: Path) -> list:
    """Load JSONL export into list of dicts."""
    objects = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                objects.append(json.loads(line))
            except Exception:
                pass
    return objects


def _extract_sequences(objects: list) -> List[List[int]]:
    """Extract integer sign sequences from object records."""
    sequences = []
    for obj in objects:
        # Prefer canonical grapheme IDs (already normalized)
        canonical = obj.get("canonical_grapheme_ids") or []
        if canonical:
            ids = []
            for cid in canonical:
                if cid and cid not in ("000", "+"):
                    if isinstance(cid, str) and str(cid).startswith("*"):
                        continue  # FIX Phase-43: skip RMRL *NNN supplementary signs
                    try:
                        # FIX: normalize to 3-digit zero-padded string (M77 format)
                        # "M047" -> "047", "67" -> "067", 342 -> "342"
                        if isinstance(cid, str) and cid.startswith("M"):
                            ids.append(str(int(cid[1:])).zfill(3))
                        elif isinstance(cid, int):
                            ids.append(str(cid).zfill(3))
                        else:
                            ids.append(str(int(str(cid))).zfill(3))
                    except (ValueError, TypeError):
                        pass
            if ids:
                sequences.append(ids)
                continue

        # Fallback: parse diplomatic text
        diplomatic = (
            obj.get("text_code_diplomatic_normalized")
            or obj.get("text_code_diplomatic")
            or obj.get("icit_text")
        )
        scheme = obj.get("sign_id_scheme")
        if diplomatic:
            ids = _parse_diplomatic_to_ints(diplomatic, scheme)
            if ids:
                sequences.append(ids)

    return sequences


# ── Public API ────────────────────────────────────────────────────────────────

def load_corpus(
    as_objects: bool = False,
    min_length: int = 2,
) -> Union[List[List[int]], list]:
    """
    Load the Indus inscription corpus.

    Args:
        as_objects: If True, return raw dict records instead of int lists.
        min_length: Minimum inscription length (in signs) to include.

    Returns:
        List of sign-ID lists (integers), or list of dicts if as_objects=True.

    Tier priority:
        1. Real corpus (glossa-corpus/indus/exports/indus_research.jsonl)
        2. CISI subset (indus_cisi.py) — 179 Mohenjo-daro inscriptions
        3. Synthetic prototype (indus_public_corpus.py)
    """
    global _CACHE, _TIER

    if _CACHE is not None and not as_objects:
        return _CACHE

    # Tier 1: Real corpus export
    if _EXPORT_PATH.exists():
        objects = _load_from_jsonl(_EXPORT_PATH)
        if objects:
            _TIER = f"real-corpus (n={len(objects)} objects from indus_research.jsonl)"
            if as_objects:
                return objects
            sequences = _extract_sequences(objects)
            sequences = [s for s in sequences if len(s) >= min_length]
            _CACHE = sequences
            return sequences

    # Tier 2: CISI subset
    try:
        from glossa_lab.data.indus_cisi import load_corpus as _cisi_load
        seqs = _cisi_load()
        if seqs:
            _TIER = f"cisi-subset (n={len(seqs)} Mohenjo-daro inscriptions)"
            if as_objects:
                return []  # no dict objects in CISI loader
            _CACHE = [s for s in seqs if len(s) >= min_length]
            return _CACHE
    except ImportError:
        pass

    # Tier 3: Synthetic prototype (last resort)
    try:
        from glossa_lab.data.indus_public_corpus import load_corpus as _synth_load
        seqs = _synth_load()
        _TIER = f"synthetic-prototype (n={len(seqs)} generated sequences)"
        if as_objects:
            return []
        _CACHE = [s for s in seqs if len(s) >= min_length]
        return _CACHE
    except ImportError:
        pass

    _TIER = "empty (no corpus data available)"
    return []


def corpus_status() -> dict:
    """Return current corpus tier and coverage statistics."""
    global _TIER

    # Trigger load if not yet loaded
    seqs = load_corpus()
    total_tokens = sum(len(s) for s in seqs)

    icit_sequences = 0
    if _ICIT_PATH.exists():
        try:
            icit_data = json.loads(_ICIT_PATH.read_text(encoding="utf-8"))
            icit_sequences = icit_data.get("total_sequences", 0)
        except Exception:
            pass

    return {
        "tier": _TIER or "unknown",
        "sequences_loaded": len(seqs),
        "total_sign_tokens": total_tokens,
        "icit_target_texts": 5509,
        "icit_target_occurrences": 19616,
        "coverage_texts_pct": round(icit_sequences / 5509 * 100, 1),
        "coverage_tokens_pct": round(total_tokens / 19616 * 100, 1),
        "export_path": str(_EXPORT_PATH),
        "export_exists": _EXPORT_PATH.exists(),
        "_citation": {
            "primary_sources": ["A.1", "A.7", "I.1", "I.2", "I.3", "I.4", "I.5"],
            "derivation": "Corpus status from indus_corpus_v2.py loader.",
        },
    }


# ── Convenience: sign frequency ───────────────────────────────────────────────

def sign_frequencies() -> dict:
    """Return sign ID -> count mapping across all loaded sequences."""
    from collections import Counter
    seqs = load_corpus()
    freq: Counter = Counter()
    for seq in seqs:
        freq.update(seq)
    return dict(freq.most_common())


if __name__ == "__main__":
    status = corpus_status()
    print("=== Indus Corpus v2 Status ===")
    for k, v in status.items():
        if not k.startswith("_"):
            print(f"  {k}: {v}")

    seqs = load_corpus()
    if seqs:
        lengths = [len(s) for s in seqs]
        print(f"\n  Mean inscription length: {sum(lengths)/len(lengths):.1f} signs")
        print(f"  Min: {min(lengths)}  Max: {max(lengths)}")
        print("\n  Sample (first 3):")
        for s in seqs[:3]:
            print(f"    {s}")

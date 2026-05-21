"""Indus Script Corpus — Firestore Direct Reconstruction (Supplementary).

NOTE ON VERSIONING:
  This module loads from the indusscript.in Firestore 'indusarrays' dump.
  It is NOT the user's primary V1 corpus. The primary V1 corpus is:
    backend/glossa_lab/data/indus_corpus_v2.py -> glossa-corpus/indus/exports/indus_research.jsonl
  This Firestore source is supplementary and tracked by acquisition date only.
  See glossa-indus/CORPUS_VERSIONS.md for the versioning policy.

Loads from the indusscript.in Firestore 'indusarrays' dump acquired
2026-05-14.  Each Firestore record = one inscription-side/line entry.
The 'dockey' field maps to Mahadevan (1977) concordance entry numbers.
Signs are stored in the 'texts' array in Mahadevan M77 numbering.

Corpus statistics (Phase-43 analysis):
  - 3,916 Firestore records
  - 2,906 unique dockeys (inscription references)
  - 2,483 dockeys with ZERO *NNN contamination  (85%)
  -   423 dockeys with some *NNN signs (filtered out per sign)
  -  12,868 numeric (Mahadevan) sign instances
  -     504 *NNN (RMRL supplementary) sign instances  (3.8% of non-empty)

*NNN signs are RMRL additions to the Mahadevan catalog and have no
counterpart in the M77 Holdat corpus.  They are filtered at load time.

_citation:
  primary_sources: ["I.6"]
  derivation: "Firestore dump of indusscript.in 'indusarrays' collection.
               Acquired 2026-05-14 with user permission via Firebase REST API.
               Signs converted to integer Mahadevan IDs (filter *NNN)."
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

_REPO = Path(__file__).parents[3]
_FIRESTORE_JSONL = (
    _REPO
    / "glossa-corpus"
    / "indus"
    / "sources"
    / "rmrl"
    / "raw"
    / "indusscript-probe"
    / "firestore_indusarrays_full.jsonl"
)

_S_FIELDS = [f"S{i}" for i in range(1, 15)]  # S1..S14

_CACHE: Optional[List[List[int]]] = None
_CACHE_SEQS_BY_DOCKEY: Optional[Dict[int, List[List[int]]]] = None


def _is_valid_sign(v: str) -> bool:
    """Return True if v is a numeric Mahadevan sign ID (not *NNN, not empty, not '0')."""
    if not v:
        return False
    v = str(v).strip()
    if not v or v == "0":
        return False
    if v.startswith("*"):
        return False  # RMRL supplementary sign — not in Holdat catalog
    try:
        int(v)
        return True
    except ValueError:
        return False


def _load_records() -> list:
    """Load all Firestore records from JSONL."""
    if not _FIRESTORE_JSONL.exists():
        return []
    records = []
    for line in _FIRESTORE_JSONL.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                records.append(json.loads(line))
            except Exception:
                pass
    return records


def _reconstruct_sequences(
    records: list,
) -> Dict[int, List[List[int]]]:
    """
    Reconstruct sign sequences from Firestore records.

    Groups records by dockey.  For each dockey, each unique sideline
    produces one inscription sequence from the 'texts' array.

    Returns: dict mapping dockey (int) -> list of sign-ID sequences (int lists).
    """
    by_key: dict = defaultdict(dict)  # dockey -> {sideline -> texts_list}
    for r in records:
        raw_dockey = r.get("dockey")
        if raw_dockey is None:
            continue
        try:
            dockey = int(str(raw_dockey))
        except (ValueError, TypeError):
            continue

        sideline = str(r.get("sideline", "0"))
        texts = r.get("texts") or []

        # Build clean sign sequence from 'texts' array (most complete)
        clean = [int(v) for v in texts if _is_valid_sign(str(v))]

        # Fallback: reconstruct from S1..S14 if texts is missing/shorter
        if len(clean) < 2:
            clean = [int(r[sf]) for sf in _S_FIELDS
                     if _is_valid_sign(str(r.get(sf, "")))]

        if len(clean) >= 2:
            # Keep longest sequence for this (dockey, sideline) pair
            key = (dockey, sideline)
            if key not in by_key or len(clean) > len(by_key[key]):
                by_key[key] = clean

    # Organise into dict dockey -> list_of_sequences
    result: Dict[int, List[List[int]]] = defaultdict(list)
    for (dockey, _sideline), signs in by_key.items():
        result[dockey].append(signs)
    return dict(result)


def load_corpus(min_length: int = 2) -> List[List[int]]:
    """
    Return all clean inscription sequences as lists of integer Mahadevan sign IDs.

    Args:
        min_length: Minimum inscription length (in signs) to include.
    """
    global _CACHE
    if _CACHE is not None:
        return [s for s in _CACHE if len(s) >= min_length]

    records = _load_records()
    seqs_by_dockey = _reconstruct_sequences(records)
    _CACHE = [seq for seqs in seqs_by_dockey.values() for seq in seqs]
    return [s for s in _CACHE if len(s) >= min_length]


def load_corpus_by_dockey(min_length: int = 2) -> Dict[int, List[List[int]]]:
    """
    Return sequences keyed by dockey (Mahadevan concordance entry number).
    Useful for cross-validation with Holdat.
    """
    global _CACHE_SEQS_BY_DOCKEY
    if _CACHE_SEQS_BY_DOCKEY is not None:
        return {
            dk: [s for s in seqs if len(s) >= min_length]
            for dk, seqs in _CACHE_SEQS_BY_DOCKEY.items()
        }
    records = _load_records()
    _CACHE_SEQS_BY_DOCKEY = _reconstruct_sequences(records)
    return {
        dk: [s for s in seqs if len(s) >= min_length]
        for dk, seqs in _CACHE_SEQS_BY_DOCKEY.items()
    }


def corpus_stats() -> dict:
    """Return summary statistics for the V3 corpus."""
    records = _load_records()
    seqs_by_dockey = _reconstruct_sequences(records)
    all_seqs = [seq for seqs in seqs_by_dockey.values() for seq in seqs]

    # *NNN analysis from raw records
    numeric = star = empty = 0
    for r in records:
        for sf in _S_FIELDS:
            v = str(r.get(sf, ""))
            if not v or v == "0":
                empty += 1
            elif v.startswith("*"):
                star += 1
            else:
                try:
                    int(v)
                    numeric += 1
                except ValueError:
                    empty += 1

    all_signs = [s for seq in all_seqs for s in seq]
    from collections import Counter
    top_signs = Counter(all_signs).most_common(20)

    return {
        "source": "indusscript.in Firestore 'indusarrays' (2026-05-14)",
        "total_records": len(records),
        "unique_dockeys": len(seqs_by_dockey),
        "total_sequences": len(all_seqs),
        "total_sign_instances": len(all_signs),
        "mean_inscription_length": round(
            sum(len(s) for s in all_seqs) / max(len(all_seqs), 1), 2
        ),
        "sign_types": {
            "numeric_mahadevan": numeric,
            "star_nnn_filtered": star,
            "star_nnn_fraction_pct": round(star / max(numeric + star, 1) * 100, 1),
        },
        "top_20_signs_by_frequency": top_signs,
        "dockey_range": [
            min(seqs_by_dockey.keys()),
            max(seqs_by_dockey.keys()),
        ],
        "_citation": {"primary_sources": ["I.6"], "phase": "Phase-43-T1"},
    }


if __name__ == "__main__":
    stats = corpus_stats()
    print(json.dumps(stats, indent=2, default=str))
    seqs = load_corpus()
    print(f"\nLoaded {len(seqs)} sequences (min_length=2)")
    print("Sample sequences:")
    for s in seqs[:5]:
        print(f"  {s}")

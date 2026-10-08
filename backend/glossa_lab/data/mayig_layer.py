"""mayig CISI corpus layer v1 loader (Phase-122).

The mayig corpus (mayig/indus-valley-script-corpus, MIT,
commit ad2f1e218a34b8c33c57de0d6cb8d99272765bbb) integrated as a
first-class corpus layer alongside the existing converted
layers (Holdat, ICIT converted v2 / keyed). Built by
``backend/scripts/phase122_build_crosswalk_mayig.py``; the
layer file is committed (mayig is MIT-licensed — see the layer
metadata for the full provenance record) at
``data/corpus_layers/mayig_cisi_layer_v1.json``.

Inscriptions are keyed by CISI object ID (e.g. "M-1"); each
record is one artefact side (side_id e.g. "M-1A") with its
Parpola (P-number) token sequence in the source's own order
and the per-token mayig feature vectors.

Lineage note: an independent transcription lineage vs the held
Holdat / Mahadevan IC77 / ICIT extractions, over a substantially
overlapping artefact population — deduplicate by CISI artefact
ID before any independence claim.
"""
from __future__ import annotations

import json
from pathlib import Path

_PATH = (Path(__file__).resolve().parents[3] / "data" / "corpus_layers"
         / "mayig_cisi_layer_v1.json")
_CACHE: dict | None = None


def _load() -> dict:
    global _CACHE  # noqa: PLW0603
    if _CACHE is None:
        if not _PATH.exists():
            raise FileNotFoundError(
                f"mayig layer not found at {_PATH}; run "
                "backend/scripts/phase122_build_crosswalk_mayig.py")
        _CACHE = json.loads(_PATH.read_text(encoding="utf-8"))
    return _CACHE


def layer_metadata() -> dict:
    """Provenance + build metadata for the layer."""
    return dict(_load()["source"])


def load_inscriptions() -> list[dict]:
    """All inscription-side records, keyed by CISI object ID."""
    return list(_load()["inscriptions"])


def get_by_object(cisi_object_id: str) -> list[dict]:
    """All sides of one CISI object (e.g. 'M-1' -> [M-1A, ...])."""
    return [r for r in _load()["inscriptions"]
            if r["cisi_object_id"] == cisi_object_id]


def object_ids() -> list[str]:
    return sorted({r["cisi_object_id"] for r in _load()["inscriptions"]})


def sequences(min_length: int = 1) -> list[list[str]]:
    """Token sequences (Parpola P-numbers, source order)."""
    return [list(r["tokens"]) for r in _load()["inscriptions"]
            if r["token_count"] >= min_length]

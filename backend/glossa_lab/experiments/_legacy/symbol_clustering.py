"""Symbol Clustering by Positional Profile.

Groups symbols in a corpus by similarity of their positional behaviour
(T/I/M-rate profiles) using L1 distance. Symbols that appear in the
same structural positions cluster together.

This is a general-purpose method usable on any symbol corpus — unknown
scripts, ciphers, genetic sequences, or any tokenised system.

Optionally accepts a reference_profiles dict to match symbols against
known reference archetypes (e.g. M77 sign classes for Indus research,
or custom classes defined by the researcher).

Parameters
----------
corpus_id : str
    Corpus to cluster.
min_count : int
    Minimum occurrences to include a symbol (default 10).
reference_profiles : dict[str, list[float]], optional
    {label: [t_rate, i_rate, m_rate]} — if provided, each symbol is
    matched to the nearest reference class. Otherwise, unsupervised
    clustering is performed by partitioning the profile space.
"""
from __future__ import annotations

from collections import Counter
from typing import Any

from glossa_lab.experiment_base import ExperimentBase


class SymbolClustering(ExperimentBase):
    id = "symbol_clustering"
    name = "Symbol Clustering"
    category = "Analysis"
    description = (
        "Groups symbols by the similarity of their positional profiles "
        "(initial / medial / terminal rates) using L1 distance. "
        "Works on any corpus \u2014 upload any symbol sequence data and discover "
        "structural symbol classes automatically. "
        "Optionally supply reference_profiles to match against known archetypes."
    )
    estimated_time = "~5 seconds"
    results_file = "symbol_clustering.json"
    command = ""
    params_schema = {
        "type": "object",
        "properties": {
            "corpus_id": {
                "type": "string",
                "title": "Corpus ID",
                "description": "ID of the corpus to cluster (from the Corpora tab). Leave blank to use default Indus corpus.",
            },
            "min_count": {
                "type": "integer",
                "title": "Min Count",
                "default": 10,
                "minimum": 1,
                "description": "Minimum occurrences to include a symbol in clustering.",
            },
        },
    }

    def run(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        corpus_id: str | None = kwargs.get("corpus_id")
        min_count: int = int(kwargs.get("min_count", 10))
        ref: dict[str, list[float]] = kwargs.get("reference_profiles") or {}

        sequences = self._load_corpus(corpus_id)
        if not sequences:
            return {"error": "No corpus found. Pass corpus_id or upload a corpus."}

        total_c    = Counter(s for seq in sequences for s in seq)
        terminal_c = Counter(seq[-1] for seq in sequences if len(seq) > 1)
        initial_c  = Counter(seq[0]  for seq in sequences if len(seq) > 1)
        medial_c   = Counter(s for seq in sequences for s in seq[1:-1])

        # Compute profiles for all qualifying symbols
        sym_profiles: dict[str, tuple[float, float, float]] = {}
        for symbol, n in total_c.items():
            if n < min_count:
                continue
            sym_profiles[symbol] = (
                terminal_c[symbol] / n,
                initial_c[symbol] / n,
                medial_c[symbol] / n,
            )

        def l1(a: tuple, b: tuple) -> float:
            return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

        if ref:
            # Supervised: assign each symbol to the nearest reference class
            ref_tuples = {label: (v[0], v[1], v[2]) for label, v in ref.items()}
            clusters: dict[str, list[dict]] = {label: [] for label in ref_tuples}
            for sym, prof in sym_profiles.items():
                best = min(ref_tuples, key=lambda lbl: l1(prof, ref_tuples[lbl]))
                dist = round(l1(prof, ref_tuples[best]), 4)
                n = total_c[sym]
                clusters[best].append({
                    "symbol": sym, "count": n,
                    "t": round(prof[0], 4), "i": round(prof[1], 4), "m": round(prof[2], 4),
                    "dist_to_ref": dist,
                })
            # Sort each cluster by distance to reference
            for lbl in clusters:
                clusters[lbl].sort(key=lambda d: d["dist_to_ref"])

            return {
                "mode": "supervised",
                "corpus_id": corpus_id,
                "reference_labels": list(ref.keys()),
                "total_sequences": len(sequences),
                "symbols_clustered": len(sym_profiles),
                "clusters": {
                    lbl: {"count": len(members), "members": members}
                    for lbl, members in clusters.items()
                },
            }

        else:
            # Unsupervised: partition by dominant position class
            buckets: dict[str, list[dict]] = {
                "TERMINAL": [], "INITIAL": [], "MEDIAL": [], "MIXED": [],
            }
            for sym, (t, i, m) in sym_profiles.items():
                if t >= 0.60:
                    cls = "TERMINAL"
                elif i >= 0.50:
                    cls = "INITIAL"
                elif m >= 0.65:
                    cls = "MEDIAL"
                else:
                    cls = "MIXED"
                n = total_c[sym]
                buckets[cls].append({
                    "symbol": sym, "count": n,
                    "t": round(t, 4), "i": round(i, 4), "m": round(m, 4),
                })
            for cls in buckets:
                buckets[cls].sort(key=lambda d: -d["count"])
            return {
                "mode": "unsupervised",
                "corpus_id": corpus_id,
                "total_sequences": len(sequences),
                "symbols_clustered": len(sym_profiles),
                "clusters": {
                    cls: {"count": len(members), "members": members}
                    for cls, members in buckets.items()
                },
            }

    def _load_corpus(self, corpus_id: str | None) -> list[list[str]]:
        from glossa_lab.database import get_db  # noqa: PLC0415
        db = get_db()
        if db and corpus_id:
            import asyncio  # noqa: PLC0415
            try:
                loop = asyncio.get_event_loop()
                text = loop.run_until_complete(db.get_text(corpus_id))
                if text and text.get("content"):
                    raw = text["content"]
                    if raw and isinstance(raw[0], list):
                        return raw
                    if raw and isinstance(raw[0], str):
                        return [raw]
            except Exception:  # noqa: BLE001
                pass
        import json  # noqa: PLC0415
        from pathlib import Path  # noqa: PLC0415
        reports = Path(__file__).resolve().parent.parent.parent.parent / "reports"
        icit = reports / "icit_extracted_corpus.json"
        if icit.exists():
            data = json.loads(icit.read_text("utf-8"))
            return [i["sequence"] for i in data["inscriptions"] if i.get("sequence")]
        return []

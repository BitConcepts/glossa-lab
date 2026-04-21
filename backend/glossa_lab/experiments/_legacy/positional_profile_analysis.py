"""Positional Profile Analysis.

For any corpus of symbol sequences, computes how frequently each symbol
appears in INITIAL (first), MEDIAL (middle), or TERMINAL (last) position.

This is a general statistical method applicable to any unknown script,
language, or symbol system stored in the Glossa Lab corpus database.

Parameters
----------
corpus_id : str
    ID of the corpus to analyse (from the Corpora tab).
min_count : int, optional
    Minimum occurrences to include a symbol (default 5).
top_n : int, optional
    Return the top N symbols by frequency (default 100).
"""
from __future__ import annotations

from collections import Counter
from typing import Any

from glossa_lab.experiment_base import ExperimentBase


class PositionalProfileAnalysis(ExperimentBase):
    id = "positional_profile_analysis"
    name = "Positional Profile Analysis"
    category = "Analysis"
    description = (
        "Computes initial / medial / terminal position rates for every symbol "
        "in a corpus. Works on any symbol system \u2014 unknown scripts, languages, "
        "DNA sequences, or any tokenised corpus. "
        "Symbols with high T-rate cluster at sequence endings (suffix candidates). "
        "High I-rate symbols are sequence openers (determinatives / prefixes). "
        "High M-rate symbols are interior elements (phonetic medials)."
    )
    estimated_time = "\u223c3 seconds"
    results_file = "positional_profile_analysis.json"
    command = ""  # invoked via experiment runner
    params_schema = {
        "type": "object",
        "properties": {
            "corpus_id": {
                "type": "string",
                "title": "Corpus ID",
                "description": "ID of the corpus to analyse (from the Corpora tab). Leave blank to use default Indus corpus.",
            },
            "min_count": {
                "type": "integer",
                "title": "Min Count",
                "default": 5,
                "minimum": 1,
                "description": "Minimum occurrences for a symbol to be included.",
            },
            "top_n": {
                "type": "integer",
                "title": "Top N Symbols",
                "default": 100,
                "minimum": 1,
                "description": "Maximum number of symbols to return, sorted by frequency.",
            },
        },
    }

    def run(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        corpus_id: str | None = kwargs.get("corpus_id")
        min_count: int = int(kwargs.get("min_count", 5))
        top_n: int = int(kwargs.get("top_n", 100))

        sequences = self._load_corpus(corpus_id)
        if not sequences:
            return {"error": "No corpus found. Pass corpus_id or upload a corpus."}

        total_c    = Counter(s for seq in sequences for s in seq)
        terminal_c = Counter(seq[-1] for seq in sequences if len(seq) > 1)
        initial_c  = Counter(seq[0]  for seq in sequences if len(seq) > 1)
        medial_c   = Counter(s for seq in sequences for s in seq[1:-1])

        profiles = []
        for symbol, n in total_c.most_common(top_n * 3):  # over-fetch then filter
            if n < min_count:
                continue
            t = terminal_c[symbol] / n
            i = initial_c[symbol] / n
            m = medial_c[symbol] / n

            if t >= 0.60:
                pos_class = "TERMINAL"
            elif i >= 0.50:
                pos_class = "INITIAL"
            elif m >= 0.65:
                pos_class = "MEDIAL"
            else:
                pos_class = "MIXED"

            profiles.append({
                "symbol": symbol, "count": n,
                "t_rate": round(t, 4),
                "i_rate": round(i, 4),
                "m_rate": round(m, 4),
                "pos_class": pos_class,
            })
            if len(profiles) >= top_n:
                break

        return {
            "corpus_id": corpus_id,
            "total_sequences": len(sequences),
            "total_tokens": sum(total_c.values()),
            "distinct_symbols": len(total_c),
            "symbols_analysed": len(profiles),
            "profiles": profiles,
            "class_summary": {
                "TERMINAL": sum(1 for p in profiles if p["pos_class"] == "TERMINAL"),
                "INITIAL":  sum(1 for p in profiles if p["pos_class"] == "INITIAL"),
                "MEDIAL":   sum(1 for p in profiles if p["pos_class"] == "MEDIAL"),
                "MIXED":    sum(1 for p in profiles if p["pos_class"] == "MIXED"),
            },
        }

    # ── Corpus loading ─────────────────────────────────────────────────────────

    def _load_corpus(self, corpus_id: str | None) -> list[list[str]]:
        """Load symbol sequences from the database corpus or from a known report.

        Returns a list of sequences, where each sequence is a list of strings.
        """
        from glossa_lab.database import get_db  # noqa: PLC0415

        db = get_db()
        if db and corpus_id:
            import asyncio  # noqa: PLC0415
            try:
                loop = asyncio.get_event_loop()
                text = loop.run_until_complete(db.get_text(corpus_id))
                if text and text.get("content"):
                    raw = text["content"]
                    # Support both flat list and list-of-lists
                    if raw and isinstance(raw[0], list):
                        return raw  # already list of sequences
                    if raw and isinstance(raw[0], str):
                        return [raw]  # single sequence
            except Exception:  # noqa: BLE001
                pass

        # Fallback: try to load the ICIT corpus if it exists (for Indus research)
        import json  # noqa: PLC0415
        from pathlib import Path  # noqa: PLC0415
        reports = Path(__file__).resolve().parent.parent.parent.parent / "reports"
        icit = reports / "icit_extracted_corpus.json"
        if icit.exists():
            data = json.loads(icit.read_text("utf-8"))
            return [i["sequence"] for i in data["inscriptions"] if i.get("sequence")]

        return []

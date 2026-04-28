"""Indus Script M77 corpus loader — full Mahadevan 1977 concordance.

Source: Iravatham Mahadevan, *The Indus Script: Texts, Concordance and Tables*,
        Memoirs of the Archaeological Survey of India No. 77 (1977).
        OCR + sign-rank-correlation glyph mapping produced
        `reports/mahadevan_corpus_flat.txt` (1669 inscriptions / 5361 tokens).

Format of mahadevan_corpus_flat.txt: one inscription per line, signs
space-separated as 3-digit M77 codes (e.g. ``"047 820 461 256"``).

Stats (April 2026):
  - 1669 inscriptions
  - 5361 sign tokens
  - Mean inscription length: ~3.2 signs (range 1–14)
  - Sign IDs use Mahadevan M77 numbering (3-digit zero-padded, e.g. "047").

Difference from CISI (data.indus_cisi):
  - CISI:    179 multi-sign inscriptions, Mohenjo-daro only, Parpola P-codes.
  - M77:     1669 inscriptions across all major sites, M77 numeric codes.
  - Use M77 for role-classifier statistics and corpus-scale PMI.
  - Use CISI for cross-checking specific Parpola allograph readings.

Public API:
  - get_corpus_inscriptions(min_length=1) -> list[list[str]]
  - get_corpus_symbols() -> list[str]
  - get_corpus_metadata() -> dict
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

# Resolve repo root (../../../ from this file: backend/glossa_lab/data/indus_m77.py).
_REPO_ROOT = Path(__file__).resolve().parents[3]

_CORPUS_FILE_CANDIDATES = [
    _REPO_ROOT / "reports" / "mahadevan_corpus_flat.txt",
    _REPO_ROOT / "data" / "mahadevan_corpus_flat.txt",
    _REPO_ROOT / "data_raw" / "mahadevan_1977" / "mahadevan_corpus_flat.txt",
]

_CORPUS_CACHE: list[list[str]] | None = None


def _load_corpus_text() -> str:
    for p in _CORPUS_FILE_CANDIDATES:
        if p.exists():
            return p.read_text(encoding="utf-8", errors="ignore")
    raise FileNotFoundError(
        "mahadevan_corpus_flat.txt not found. Expected at one of: "
        + " | ".join(str(p) for p in _CORPUS_FILE_CANDIDATES)
    )


def _parse_corpus() -> list[list[str]]:
    """Parse the flat M77 text into a list of sign sequences.

    Each non-empty line is one inscription. Tokens are whitespace-separated.
    Empty lines and comment-style headers are skipped.
    """
    global _CORPUS_CACHE  # noqa: PLW0603
    if _CORPUS_CACHE is not None:
        return _CORPUS_CACHE
    text = _load_corpus_text()
    seqs: list[list[str]] = []
    for line in text.splitlines():
        toks = [t for t in line.strip().split() if t and t.isdigit()]
        if toks:
            seqs.append(toks)
    _CORPUS_CACHE = seqs
    return seqs


def get_corpus_inscriptions(min_length: int = 1) -> list[list[str]]:
    """Return M77 inscription sequences as lists of M77 sign codes."""
    seqs = _parse_corpus()
    if min_length <= 1:
        return list(seqs)
    return [s for s in seqs if len(s) >= min_length]


def get_corpus_symbols() -> list[str]:
    """Return a flat list of M77 sign tokens."""
    return [s for seq in _parse_corpus() for s in seq]


def get_corpus_metadata() -> dict:
    seqs = _parse_corpus()
    flat = [s for seq in seqs for s in seq]
    freq = Counter(flat)
    lengths = [len(s) for s in seqs]
    return {
        "n_inscriptions": len(seqs),
        "n_tokens": len(flat),
        "n_distinct_signs": len(freq),
        "mean_length": round(sum(lengths) / max(1, len(lengths)), 3),
        "max_length": max(lengths, default=0),
        "top_10_signs": freq.most_common(10),
        "sign_numbering": "Mahadevan M77 (1977)",
        "source": "Mahadevan 1977 OCR + rank-corr (reports/mahadevan_corpus_flat.txt)",
    }

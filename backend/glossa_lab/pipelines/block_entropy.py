"""Block entropy analysis pipeline.

Implements the block entropy method from:
  Rao et al. (2009) — "Entropic Evidence for Linguistic Structure in the
  Indus Script", Science 324:1165.

Computes H_N = −Σ p_i^(N) ln(p_i^(N)) for block sizes N=1..max_n.
Normalizes by ln(L) where L is the alphabet size so that sequences with
different alphabet sizes are comparable.

Supports pluggable entropy estimators:
  "mle"          — plain maximum-likelihood (default, matches original paper)
  "miller_madow" — MLE + (K-1)/(2N) additive correction
  "chao_shen"    — coverage-adjusted estimator (best for small corpora)

See glossa_lab.pipelines.nsb_entropy for details.
"""

from __future__ import annotations

import math
from typing import Any

from glossa_lab.database import get_db
from glossa_lab.engine import register_pipeline
from glossa_lab.pipelines.nsb_entropy import estimate_entropy


def compute_block_entropy(
    symbols: list[str],
    n: int,
    estimator: str = "mle",
) -> float:
    """Compute block entropy H_N for a symbol sequence.

    H_N = −Σ p_i log(p_i)  where p_i = count(ngram_i) / total_ngrams.
    Uses natural logarithm (nats).

    Args:
        symbols: flat list of symbols.
        n: block size.
        estimator: entropy estimator — 'mle', 'miller_madow', or 'chao_shen'.
    """
    return estimate_entropy(symbols, n=n, estimator=estimator)


def compute_block_entropies(
    symbols: list[str],
    max_n: int = 6,
    estimator: str = "mle",
) -> dict[str, Any]:
    """Compute block entropies for N=1..max_n.

    Returns dict with alphabet_size, symbol_count, estimator, and
    block_entropies list. Each entry has n, raw (nats), and normalized
    (H_N / ln(L)).

    Args:
        symbols: flat list of symbols.
        max_n: maximum block size.
        estimator: entropy estimator — 'mle', 'miller_madow', or 'chao_shen'.
    """
    alphabet = sorted(set(symbols))
    L = len(alphabet)
    ln_L = math.log(L) if L > 1 else 1.0

    entries = []
    for n in range(1, max_n + 1):
        raw = compute_block_entropy(symbols, n, estimator=estimator)
        normalized = raw / ln_L if ln_L > 0 else 0.0
        entries.append({
            "n": n,
            "raw_nats": round(raw, 6),
            "normalized": round(normalized, 6),
        })

    return {
        "alphabet_size": L,
        "symbol_count": len(symbols),
        "estimator": estimator,
        "block_entropies": entries,
    }


@register_pipeline("block_entropy")
async def run_block_entropy(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point. Params: {text_id: str, max_n: int (default 6)}."""
    text_id = params.get("text_id")
    if not text_id:
        raise ValueError("Missing required param: text_id")

    max_n = params.get("max_n", 6)
    estimator = params.get("estimator", "mle")

    db = get_db()
    if db is None:
        raise RuntimeError("Database not available")

    text = await db.get_text(text_id)
    if text is None:
        raise ValueError(f"Text not found: {text_id}")

    symbols = text["content"]
    if not isinstance(symbols, list):
        raise ValueError("Text content must be a list of symbols")

    result = compute_block_entropies(symbols, max_n=max_n, estimator=estimator)
    result["text_id"] = text_id
    result["text_name"] = text["name"]
    result["corpus_type"] = text["corpus_type"]
    return result

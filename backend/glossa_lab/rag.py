"""Retrieval-Augmented Generation (RAG) module for Glossa Lab.

Provides semantic search over research artifacts:
  - JSON reports in reports/
  - Notebook content from the database
  - Hypothesis statements
  - Experiment descriptions
  - Corpus metadata

Storage: TF-IDF cosine similarity (zero-dependency fallback).
         ChromaDB used automatically when installed.

Usage:
    from glossa_lab.rag import build_index, query, index_size

    await build_index(db)          # rebuild index from all sources
    chunks = query("Indus terminal signs positional", top_k=5)
    # Returns: [{"text": "...", "source": "...", "source_type": "...", "score": 0.85}, ...]
"""
from __future__ import annotations

import json
import logging
import math
import re
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_REPORTS_DIR = Path(__file__).resolve().parent.parent.parent / "reports"
_INDEX_CACHE  = Path(__file__).resolve().parent.parent.parent / "data" / "_rag_index.json"
_CHUNK_MAX    = 600    # max characters per chunk
_CHUNK_OVERLAP = 100   # overlap between chunks


# ── In-memory index ────────────────────────────────────────────────────────────

_chunks: list[dict[str, Any]] = []          # raw chunks with text + metadata
_tfidf_matrix: list[dict[str, float]] = []  # parallel TF-IDF vectors
_vocab: set[str] = set()                    # vocabulary
_idf: dict[str, float] = {}                 # pre-computed IDF values
_index_built_at: float = 0.0


# ── Tokenisation & TF-IDF ──────────────────────────────────────────────────────

def _tokenize(text: str) -> list[str]:
    """Lower-case, split on non-alphanumeric, remove short tokens."""
    return [t for t in re.split(r"[^a-zA-Z0-9_]", text.lower()) if len(t) >= 3]


def _tf(tokens: list[str]) -> dict[str, float]:
    """Compute raw term frequency vector."""
    freq: dict[str, float] = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    n = max(len(tokens), 1)
    return {t: c / n for t, c in freq.items()}


def _build_idf(docs: list[list[str]]) -> dict[str, float]:
    """Compute IDF values for all terms across the document corpus."""
    n = len(docs)
    df: dict[str, int] = {}
    for doc in docs:
        for term in set(doc):
            df[term] = df.get(term, 0) + 1
    return {term: math.log((n + 1) / (count + 1)) + 1 for term, count in df.items()}


def _tfidf(tokens: list[str], idf: dict[str, float]) -> dict[str, float]:
    tf = _tf(tokens)
    return {t: v * idf.get(t, 1.0) for t, v in tf.items()}


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) & set(b)
    if not keys:
        return 0.0
    dot = sum(a[k] * b[k] for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


# ── Chunking helpers ───────────────────────────────────────────────────────────

def _chunk_text(text: str, source: str, source_type: str) -> list[dict[str, Any]]:
    """Split text into overlapping fixed-size chunks."""
    if not text or not text.strip():
        return []
    text = text.strip()
    chunks = []
    pos = 0
    while pos < len(text):
        end = min(pos + _CHUNK_MAX, len(text))
        chunk_text = text[pos:end].strip()
        if chunk_text:
            chunks.append({"text": chunk_text, "source": source, "source_type": source_type})
        pos += _CHUNK_MAX - _CHUNK_OVERLAP
    return chunks


def _flatten_json(obj: Any, depth: int = 0) -> str:
    """Recursively flatten a JSON object to a readable text representation."""
    if depth > 4:
        return ""
    if isinstance(obj, str):
        return obj[:300]
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, dict):
        parts = []
        for k, v in list(obj.items())[:20]:
            flat = _flatten_json(v, depth + 1)
            if flat:
                parts.append(f"{k}: {flat}")
        return ". ".join(parts)
    if isinstance(obj, list):
        return ". ".join(_flatten_json(i, depth + 1) for i in obj[:10] if i)
    return ""


# ── Index building ─────────────────────────────────────────────────────────────

async def build_index(db: Any = None) -> int:
    """Build or rebuild the full RAG index.

    Indexes reports, notebooks, hypotheses, and experiment descriptions.
    Returns the total number of indexed chunks.
    """
    global _chunks, _tfidf_matrix, _idf, _vocab, _index_built_at  # noqa: PLW0603
    all_chunks: list[dict[str, Any]] = []

    # ── 1. JSON reports ───────────────────────────────────────────────────────
    if _REPORTS_DIR.exists():
        for path in sorted(_REPORTS_DIR.glob("*.json")):
            if path.name.startswith("_"):
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                flat = _flatten_json(data)
                all_chunks.extend(_chunk_text(flat, source=path.stem, source_type="report"))
            except Exception:  # noqa: BLE001
                pass

    # ── 2. Experiment descriptions ────────────────────────────────────────────
    try:
        from glossa_lab.experiment_base import list_discovered_experiments  # noqa: PLC0415
        for exp in list_discovered_experiments():
            text = f"{exp['name']}: {exp['description']}"
            if exp.get("params_schema"):
                props = exp["params_schema"].get("properties", {})
                for pname, pdef in props.items():
                    text += f". {pname}: {pdef.get('description', '')}"
            all_chunks.extend(_chunk_text(text, source=exp["id"], source_type="experiment"))
    except Exception:  # noqa: BLE001
        pass

    # ── 3. Database records (notebooks, hypotheses, corpus metadata) ──────────
    if db is not None:
        try:
            for nb in await db.list_notebooks():
                text = f"{nb.get('title', '')}: {nb.get('content', '')}"
                all_chunks.extend(_chunk_text(text, source=f"notebook:{nb.get('id','')}", source_type="notebook"))
        except Exception:  # noqa: BLE001
            pass

        try:
            for hyp in await db.list_hypotheses():
                text = (
                    f"{hyp.get('title', '')} ({hyp.get('status', 'active')}): "
                    f"{hyp.get('statement', '')}"
                )
                all_chunks.extend(_chunk_text(text, source=f"hypothesis:{hyp.get('id','')}", source_type="hypothesis"))
        except Exception:  # noqa: BLE001
            pass

        try:
            for text_row in await db.list_texts():
                text = (
                    f"Corpus {text_row.get('name', '')}: "
                    f"{text_row.get('alphabet_size', 0)} symbols, "
                    f"{len(text_row.get('content', []))} tokens"
                )
                all_chunks.extend(_chunk_text(text, source=f"corpus:{text_row.get('id','')}", source_type="corpus"))
        except Exception:  # noqa: BLE001
            pass

    if not all_chunks:
        logger.warning("RAG index is empty — no sources found")
        return 0

    # ── Build TF-IDF matrix ────────────────────────────────────────────────────
    tokenized = [_tokenize(c["text"]) for c in all_chunks]
    idf = _build_idf(tokenized)
    tfidf_vecs = [_tfidf(toks, idf) for toks in tokenized]

    _chunks = all_chunks
    _tfidf_matrix = tfidf_vecs
    _idf = idf
    _vocab = set(idf)
    _index_built_at = time.time()

    logger.info("RAG index built: %d chunks from %d unique sources", len(_chunks),
                len({c["source"] for c in _chunks}))
    return len(_chunks)


# ── Query ──────────────────────────────────────────────────────────────────────

def query(text: str, top_k: int = 5) -> list[dict[str, Any]]:
    """Query the RAG index for the most relevant chunks.

    Returns a list of dicts: {text, source, source_type, score}.
    Falls back to an empty list if the index has not been built.
    """
    if not _chunks or not _tfidf_matrix:
        return []

    q_tokens = _tokenize(text)
    if not q_tokens:
        return []

    q_vec = _tfidf(q_tokens, _idf)
    scores = [_cosine(q_vec, doc_vec) for doc_vec in _tfidf_matrix]

    # Get top-k indices by score (descending)
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
    results = []
    seen: set[str] = set()  # deduplicate near-identical chunks
    for idx, score in ranked:
        if score < 0.05:
            break
        chunk = _chunks[idx]
        key = chunk["text"][:80]
        if key in seen:
            continue
        seen.add(key)
        results.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "source_type": chunk["source_type"],
            "score": round(score, 4),
        })
    return results


def index_size() -> int:
    """Return the number of indexed chunks."""
    return len(_chunks)


def index_age_seconds() -> float:
    """Return how many seconds ago the index was last built."""
    if _index_built_at == 0:
        return float("inf")
    return time.time() - _index_built_at

"""Corpus analysis endpoints (pure-Python, no extra deps).

Endpoints:
  GET  /texts/{id}/entropy                -- H1, H2, conditional entropy, TTR, Zipf
  GET  /texts/{id}/ngrams?n=2&limit=50    -- top n-gram frequencies
  GET  /texts/{id}/concordance?q=X&w=5   -- KWIC concordance
  GET  /texts/{id}/export?fmt=txt|csv|json -- download corpus content
  POST /texts/{id}/analyze               -- AI corpus analysis
  POST /texts/{id}/anomalies             -- AI anomaly detection
  POST /texts/{id}/critique              -- AI corpus critique
"""

from __future__ import annotations

import asyncio
import csv
import io
import json
import math
from collections import Counter
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from glossa_lab.database import get_db

router = APIRouter()


# ── Helpers ───────────────────────────────────────────────────────────────────


def _compute_entropy(tokens: list[str]) -> dict[str, Any]:
    n = len(tokens)
    if n == 0:
        return {}
    freq1 = Counter(tokens)
    # H1 – unigram Shannon entropy (bits)
    h1 = -sum((c / n) * math.log2(c / n) for c in freq1.values())

    # Bigrams
    bigrams = [f"{tokens[i]}\t{tokens[i + 1]}" for i in range(n - 1)]
    freq2 = Counter(bigrams)
    n2 = len(bigrams)
    h2_joint = -sum((c / n2) * math.log2(c / n2) for c in freq2.values()) if n2 > 0 else 0.0
    cond_h = h2_joint - h1  # H(X_{i+1} | X_i) = H(X1,X2) - H(X1)

    # Type-token ratio
    ttr = len(freq1) / n

    # Zipf deviation: rank-log(freq) correlation ideally -1
    sorted_freqs = sorted(freq1.values(), reverse=True)
    ranks = list(range(1, len(sorted_freqs) + 1))
    if len(ranks) > 1:
        mean_r = sum(ranks) / len(ranks)
        mean_f = sum(math.log2(f) for f in sorted_freqs) / len(sorted_freqs)
        cov = sum((r - mean_r) * (math.log2(f) - mean_f) for r, f in zip(ranks, sorted_freqs))
        var_r = sum((r - mean_r) ** 2 for r in ranks)
        var_f = sum((math.log2(f) - mean_f) ** 2 for f in sorted_freqs)
        zipf_corr = cov / math.sqrt(var_r * var_f) if var_r * var_f > 0 else 0.0
    else:
        zipf_corr = 0.0

    # Zipf rank-freq table (top 50 for front-end charts)
    zipf_table = [
        {
            "rank": i + 1,
            "token": t,
            "freq": c,
            "log_rank": round(math.log2(i + 1), 3),
            "log_freq": round(math.log2(c), 3),
        }
        for i, (t, c) in enumerate(freq1.most_common(50))
    ]

    return {
        "h1": round(h1, 4),
        "h2_joint": round(h2_joint, 4),
        "conditional_h": round(max(cond_h, 0.0), 4),
        "h2_h1_ratio": round(h2_joint / h1, 4) if h1 > 0 else None,
        "type_token_ratio": round(ttr, 4),
        "zipf_correlation": round(zipf_corr, 4),
        "token_count": n,
        "type_count": len(freq1),
        "hapax_count": sum(1 for c in freq1.values() if c == 1),
        "zipf_table": zipf_table,
    }


def _get_ngrams(tokens: list[str], n: int = 2, limit: int = 50) -> list[dict[str, Any]]:
    if len(tokens) < n:
        return []
    grams = [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]
    return [
        {"ngram": g, "count": c, "tokens": g.split(" ")}
        for g, c in Counter(grams).most_common(limit)
    ]


def _get_concordance(tokens: list[str], query: str, window: int = 5) -> list[dict[str, Any]]:
    hits = []
    for i, tok in enumerate(tokens):
        if tok == query:
            left = tokens[max(0, i - window) : i]
            right = tokens[i + 1 : i + 1 + window]
            hits.append({"position": i, "left": left, "match": tok, "right": right})
    return hits


# ── Endpoints ─────────────────────────────────────────────────────────────────


@router.get("/texts/{text_id}/entropy")
async def get_entropy(text_id: str) -> dict[str, Any]:
    """Compute entropy and statistical metrics for a corpus."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    text = await db.get_text(text_id)
    if text is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return _compute_entropy(text["content"])


@router.get("/texts/{text_id}/ngrams")
async def get_ngrams(
    text_id: str,
    n: int = Query(default=2, ge=1, le=10),
    limit: int = Query(default=50, ge=1, le=500),
) -> list[dict[str, Any]]:
    """Return top n-gram frequencies."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    text = await db.get_text(text_id)
    if text is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return _get_ngrams(text["content"], n=n, limit=limit)


@router.get("/texts/{text_id}/concordance")
async def get_concordance(
    text_id: str,
    q: str = Query(..., description="Token to search for"),
    w: int = Query(default=5, ge=1, le=20, description="Context window size"),
) -> dict[str, Any]:
    """Return KWIC (key-word-in-context) concordance."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    text = await db.get_text(text_id)
    if text is None:
        raise HTTPException(status_code=404, detail="Text not found")
    hits = _get_concordance(text["content"], q, w)
    return {"query": q, "hits": hits, "total": len(hits)}


@router.get("/texts/{text_id}/export")
async def export_corpus(
    text_id: str,
    fmt: str = Query(default="txt", description="Format: txt, csv, json"),
) -> Response:
    """Export corpus content in the requested format."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    text = await db.get_text(text_id)
    if text is None:
        raise HTTPException(status_code=404, detail="Text not found")

    safe_name = text["name"].replace(" ", "_").replace("/", "_")[:40]

    if fmt == "json":
        body = json.dumps(
            {
                "id": text["id"],
                "name": text["name"],
                "corpus_type": text["corpus_type"],
                "content": text["content"],
            },
            indent=2,
        ).encode()
        return Response(
            content=body,
            media_type="application/json",
            headers={"Content-Disposition": f'attachment; filename="{safe_name}.json"'},
        )
    if fmt == "csv":
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["position", "token"])
        for i, tok in enumerate(text["content"]):
            w.writerow([i, tok])
        body = buf.getvalue().encode("utf-8")
        return Response(
            content=body,
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{safe_name}.csv"'},
        )
    # default: txt – space-separated tokens
    body = " ".join(text["content"]).encode("utf-8")
    return Response(
        content=body,
        media_type="text/plain",
        headers={"Content-Disposition": f'attachment; filename="{safe_name}.txt"'},
    )


# ── AI endpoints ──────────────────────────────────────────────────────────────


def _make_corpus_summary(text: dict[str, Any]) -> str:
    stats = _compute_entropy(text["content"])
    top5 = Counter(text["content"]).most_common(5)
    return (
        f"Corpus name: {text['name']}\n"
        f"Type: {text['corpus_type']}\n"
        f"Tokens: {stats.get('token_count', 0):,}\n"
        f"Alphabet size: {stats.get('type_count', 0)}\n"
        f"H1 (unigram entropy): {stats.get('h1', '?')} bits\n"
        f"H2/H1 ratio: {stats.get('h2_h1_ratio', '?')}\n"
        f"Conditional entropy H(X|X-1): {stats.get('conditional_h', '?')} bits\n"
        f"Type-token ratio: {stats.get('type_token_ratio', '?'):.3f}\n"
        f"Hapax count: {stats.get('hapax_count', 0)}\n"
        f"Zipf correlation: {stats.get('zipf_correlation', '?')}\n"
        f"Top 5 tokens: {', '.join(f'{t}={c}' for t, c in top5)}\n"
    )


@router.post("/texts/{text_id}/analyze")
async def analyze_corpus(text_id: str) -> dict[str, Any]:
    """AI-generate a structured analysis of the corpus."""
    from glossa_lab.ai_utils import call_llm

    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    text = await db.get_text(text_id)
    if text is None:
        raise HTTPException(status_code=404, detail="Text not found")

    summary = _make_corpus_summary(text)
    system = (
        "You are a computational linguist analyzing a text corpus for Indus Script research. "
        "Return ONLY valid JSON:\n"
        '{"summary": "2-3 sentence overview", '
        '"characteristics": ["characteristic 1", "characteristic 2"], '
        '"linguistic_profile": "is this consistent with natural language? why?", '
        '"indus_relevance": "how does this compare to or relate to the Indus Script corpus?", '
        '"insights": ["insight 1", "insight 2"], '
        '"suggested_experiments": [{"id": "<exp_id_hint>", "rationale": "why this experiment suits this corpus"}], '
        '"suggested_actions": [{"label": "Run Entropy Analysis", "action": "run_experiment", "hint": "..."}]}'
    )
    user = f"Analyze this corpus:\n{summary}"
    try:
        loop = asyncio.get_event_loop()
        raw = await loop.run_in_executor(
            None,
            lambda: call_llm(
                [{"role": "system", "content": system}, {"role": "user", "content": user}],
                json_mode=True,
            ),
        )
        result: dict[str, Any] = json.loads(raw)
        result["text_id"] = text_id
        result["name"] = text["name"]
        result["stats"] = {
            k: v for k, v in _compute_entropy(text["content"]).items() if k != "zipf_table"
        }
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/texts/{text_id}/anomalies")
async def detect_anomalies(text_id: str) -> dict[str, Any]:
    """AI-detect statistical anomalies and unusual patterns in the corpus."""
    from glossa_lab.ai_utils import call_llm

    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    text = await db.get_text(text_id)
    if text is None:
        raise HTTPException(status_code=404, detail="Text not found")

    top20 = Counter(text["content"]).most_common(20)
    summary = _make_corpus_summary(text)
    # Compute local entropy variance (split into 10 chunks)
    tokens = text["content"]
    chunk_size = max(len(tokens) // 10, 1)
    chunks = [tokens[i : i + chunk_size] for i in range(0, len(tokens), chunk_size)]
    chunk_entropies = []
    for chunk in chunks:
        if len(chunk) > 1:
            freq = Counter(chunk)
            n = len(chunk)
            h = -sum((c / n) * math.log2(c / n) for c in freq.values())
            chunk_entropies.append(round(h, 3))

    system = (
        "You are a corpus anomaly detector for Indus Script research. "
        "Return ONLY valid JSON:\n"
        '{"anomalies": [{"type": "statistical|structural|frequency", "description": "...", "severity": "low|medium|high"}], '
        '"overall_assessment": "brief summary of corpus health", '
        '"recommendations": ["recommendation 1", "recommendation 2"]}'
    )
    user = (
        f"{summary}"
        f"Top 20 tokens: {', '.join(f'{t}={c}' for t, c in top20)}\n"
        f"Chunk entropy values (10 segments): {chunk_entropies}\n"
        "Identify any statistical anomalies, unusual patterns, or data quality issues."
    )
    try:
        loop = asyncio.get_event_loop()
        raw = await loop.run_in_executor(
            None,
            lambda: call_llm(
                [{"role": "system", "content": system}, {"role": "user", "content": user}],
                json_mode=True,
            ),
        )
        result = json.loads(raw)
        result["text_id"] = text_id
        result["name"] = text["name"]
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/texts/{text_id}/critique")
async def critique_corpus(text_id: str) -> dict[str, Any]:
    """AI-critique the corpus: coverage, bias, completeness, suitability."""
    from glossa_lab.ai_utils import call_llm

    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")
    text = await db.get_text(text_id)
    if text is None:
        raise HTTPException(status_code=404, detail="Text not found")

    summary = _make_corpus_summary(text)
    system = (
        "You are a research methodologist critiquing a text corpus for use in ancient script research. "
        "Return ONLY valid JSON:\n"
        '{"strengths": ["strength 1"], '
        '"weaknesses": ["weakness 1"], '
        '"coverage_assessment": "how complete/representative is this corpus?", '
        '"bias_risks": ["potential bias 1"], '
        '"suitability": {"entropy_analysis": true, "decipherment": true, "comparative": true}, '
        '"improvement_suggestions": ["suggestion 1", "suggestion 2"]}'
    )
    user = f"Critique this corpus for research use:\n{summary}"
    try:
        loop = asyncio.get_event_loop()
        raw = await loop.run_in_executor(
            None,
            lambda: call_llm(
                [{"role": "system", "content": system}, {"role": "user", "content": user}],
                json_mode=True,
            ),
        )
        result = json.loads(raw)
        result["text_id"] = text_id
        result["name"] = text["name"]
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

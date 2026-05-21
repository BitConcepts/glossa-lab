"""Model Assignments API — bucket-based model routing.

Each work bucket (reasoning, conversational, longform, global) has a
primary (rank=1) and fallback (rank=2) provider+model assignment.

Endpoints:
  GET  /api/v1/model-assignments              — list all assignments
  PUT  /api/v1/model-assignments/{bucket}     — set primary+fallback for a bucket
  GET  /api/v1/model-assignments/resolve      — resolve which provider+model would be used
  POST /api/v1/model-assignments/auto-configure — auto-assign best models per bucket
"""

from __future__ import annotations

import logging
import re as _re
from typing import Any

_log = logging.getLogger("glossa_lab.api.model_assignments")

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from glossa_lab.database import get_db

# ── Model-name normalisation helpers ───────────────────────────────────────

def _normalize_model_id(name: str) -> str:
    """Normalise a model ID for fuzzy score-matching.

    Pipeline (applied in order):
      1. Strip org/user prefix   ("org/model"          → "model")
      2. Strip Ollama :tag        ("model:7b"           → "model")
      3. Lowercase + sep normalise (. and _ → -)
      4. Strip 8-digit date stamp ("-20250514"          → "")
      5. Strip preview/RC labels  ("-preview-05-20"     → "")
      6. Strip quant/precision    ("-awq-4bit"          → "")
      7. Strip fine-tune suffixes ("-instruct", "-chat" → "")
      8. Collapse repeated hyphens

    Examples
    --------
    claude-sonnet-4-20250514            → claude-sonnet-4
    gemini-2.5-flash-preview-05-20      → gemini-2-5-flash
    cpatonn/Qwen3-Coder-30B-A3B-Instruct-AWQ-4bit → qwen3-coder-30b-a3b
    llama3.1:70b                        → llama3-1
    deepseek-r1:671b                    → deepseek-r1
    """
    n = name.split("/", 1)[-1] if "/" in name else name   # strip org prefix
    n = n.split(":")[0]                                     # strip Ollama tag
    n = n.lower()
    n = _re.sub(r"[._]", "-", n)                           # normalise separators
    n = _re.sub(r"-\d{8}$", "", n)                           # strip YYYYMMDD  (20250514)
    n = _re.sub(r"-\d{4}-\d{2}-\d{2}$", "", n)              # strip YYYY-MM-DD (2025-04-16)
    n = _re.sub(r"-preview(-\d{2}-\d{2})?$", "", n)          # strip preview labels
    n = _re.sub(r"-rc\d*$", "", n)                          # strip RC labels
    n = _re.sub(                                             # strip quant/precision
        r"-(awq|gptq|gguf|4bit|8bit|fp16|bf16|int4|int8|ggml)(-.+)?$",
        "", n, flags=_re.IGNORECASE,
    )
    n = _re.sub(                                             # strip fine-tune tags
        r"-(instruct|chat|it|hf|base|sft|dpo|v\d+(-\d+)?)$",
        "", n, flags=_re.IGNORECASE,
    )
    n = _re.sub(r"-+", "-", n).strip("-")                  # collapse hyphens
    return n


def _token_jaccard(a: str, b: str) -> float:
    """Jaccard similarity on hyphen-delimited tokens (min token length 2)."""
    ta = {t for t in a.split("-") if len(t) >= 2}
    tb = {t for t in b.split("-") if len(t) >= 2}
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)

router = APIRouter(prefix="/api/v1/model-assignments", tags=["model-assignments"])

VALID_BUCKETS = ("reasoning", "conversational", "longform", "global")


class BucketAssignment(BaseModel):
    primary_provider_id: str = ""
    primary_model: str = ""
    primary_params: dict[str, Any] = {}
    fallback_provider_id: str = ""
    fallback_model: str = ""
    fallback_params: dict[str, Any] = {}


# ── Routes ─────────────────────────────────────────────────────────────────


@router.get("")
async def list_assignments() -> dict[str, Any]:
    db = get_db()
    if db is None:
        return {"assignments": [], "buckets": list(VALID_BUCKETS)}
    rows = await db.list_model_assignments()
    # Group by bucket for easier frontend consumption
    by_bucket: dict[str, dict[str, Any]] = {}
    for r in rows:
        b = r["bucket"]
        if b not in by_bucket:
            by_bucket[b] = {"bucket": b}
        if r["rank"] == 1:
            by_bucket[b]["primary"] = r
        elif r["rank"] == 2:
            by_bucket[b]["fallback"] = r
    return {
        "assignments": list(by_bucket.values()),
        "buckets": list(VALID_BUCKETS),
    }


@router.put("/{bucket}")
async def set_bucket_assignment(bucket: str, body: BucketAssignment) -> dict[str, Any]:
    if bucket not in VALID_BUCKETS:
        raise HTTPException(400, f"Invalid bucket: {bucket}. Must be one of {VALID_BUCKETS}")
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    result: dict[str, Any] = {"bucket": bucket}
    # Set primary
    if body.primary_provider_id and body.primary_model:
        p = await db.upsert_model_assignment(
            bucket=bucket, rank=1,
            provider_registry_id=body.primary_provider_id,
            model=body.primary_model,
            params=body.primary_params,
        )
        result["primary"] = p
    elif not body.primary_provider_id and not body.primary_model:
        # Clear primary
        await db.delete_model_assignment(bucket, 1)
        result["primary"] = None
    # Set fallback
    if body.fallback_provider_id and body.fallback_model:
        f = await db.upsert_model_assignment(
            bucket=bucket, rank=2,
            provider_registry_id=body.fallback_provider_id,
            model=body.fallback_model,
            params=body.fallback_params,
        )
        result["fallback"] = f
    elif not body.fallback_provider_id and not body.fallback_model:
        await db.delete_model_assignment(bucket, 2)
        result["fallback"] = None
    return result


@router.get("/resolve")
async def resolve_assignment(
    bucket: str = Query("global"),
) -> dict[str, Any]:
    """Resolve which provider+model would be used for a given bucket."""
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    resolved = await db.resolve_model_for_bucket(bucket)
    if resolved is None:
        return {
            "resolved": False,
            "bucket": bucket,
            "message": f"No assignment configured for bucket '{bucket}' or global fallback.",
        }
    prov = resolved.get("_provider", {})
    return {
        "resolved": True,
        "bucket": resolved["bucket"],
        "rank": resolved["rank"],
        "is_fallback": resolved["rank"] == 2 or resolved["bucket"] != bucket,
        "provider_id": prov.get("id", ""),
        "provider_name": prov.get("name", ""),
        "provider_type": prov.get("provider_type", ""),
        "base_url": prov.get("base_url", ""),
        "model": resolved["model"],
        "params": resolved.get("params", {}),
    }


# Preferred provider types for fallback selection, in priority order.
# vLLM/BYOE endpoints and Ollama are local/free, so prefer them.
_FALLBACK_TYPE_PRIORITY = ["byoe", "ollama", "cloud", "huggingface"]


# Provider type sets for each profile.
_PROFILE_TYPES: dict[str, set[str]] = {
    "mixed": {"cloud", "ollama", "byoe", "huggingface"},
    "cloud": {"cloud"},
    "local": {"ollama", "byoe", "huggingface"},
}


@router.post("/auto-configure")
async def auto_configure(profile: str = Query("mixed")) -> dict[str, Any]:
    """Auto-assign the best available models to each bucket.

    Profiles:
      mixed (default) — uses all providers (cloud + local).
      cloud           — only cloud API providers.
      local           — only Ollama, vLLM/BYOE, HuggingFace.

    Strategy per profile:
      Primary   — highest-scored model from eligible providers.
      Fallback  — highest-scored model from a DIFFERENT eligible provider,
                  preferring local/free backends (vLLM → Ollama → cloud).
      Global    — best overall as primary, different provider as fallback.
    """
    allowed_types = _PROFILE_TYPES.get(profile, _PROFILE_TYPES["mixed"])

    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")

    all_providers = await db.list_providers(enabled_only=True)
    providers = [p for p in all_providers if p.get("provider_type", "cloud") in allowed_types]
    if not providers:
        return {
            "configured": False,
            "message": "No enabled providers found. Add a provider first.",
        }

    # Build a quick provider-id → provider-type lookup
    {
        p["id"]: p.get("provider_type", "cloud") for p in providers
    }

    # Gather all available models across providers
    all_models: list[dict[str, Any]] = []
    for prov in providers:
        for model_name in (prov.get("available_models") or []):
            all_models.append({
                "provider_id": prov["id"],
                "provider_name": prov["name"],
                "provider_type": prov.get("provider_type", "cloud"),
                "model": model_name,
            })

    if not all_models:
        return {
            "configured": False,
            "message": "No models found. Test your providers first to fetch model lists.",
        }

    # Try to use model_scores for smart assignment.
    # IMPORTANT: list_model_scores() returns all rows ordered by reasoning DESC.
    # The same model_name can appear in multiple sources (static + HF).  We must
    # keep the entry with the HIGHEST total score rather than last-write-wins,
    # otherwise lower-quality HF partial data can silently overwrite the
    # complete static baseline scores.
    raw_scores = await db.list_model_scores()
    score_map: dict[str, dict[str, float]] = {}
    for s in raw_scores:
        mn = s["model_name"]
        new_bscores = {
            "reasoning": s.get("reasoning_score", 0.0),
            "conversational": s.get("conversational_score", 0.0),
            "longform": s.get("longform_score", 0.0),
        }
        if mn not in score_map or sum(new_bscores.values()) > sum(score_map[mn].values()):
            score_map[mn] = new_bscores

    # Pre-build a normalised lookup index.  When multiple raw keys normalise
    # to the same string, keep the entry with the highest aggregate score so
    # the best benchmark data always wins.
    norm_score_index: dict[str, dict[str, float]] = {}
    for raw_key, bscores in score_map.items():
        nk = _normalize_model_id(raw_key)
        prev = norm_score_index.get(nk)
        if prev is None or sum(bscores.values()) > sum(prev.values()):
            norm_score_index[nk] = bscores

    def _resolve_score(model_name: str, bucket_key: str) -> tuple[float, str]:
        """Resolve a score for *model_name* using six progressive tiers.

        Returns *(score, tier_label)* so callers can include match provenance
        in debug output.

        Tiers
        -----
        T1  Exact key match in score_map
        T2  Org-prefix-stripped exact match
        T3  Ollama-tag-stripped exact match
        T4  Normalised exact match — handles date stamps, quantisation
            variants, preview labels, instruction/chat suffixes
        T5  Token-Jaccard ≥ 0.55 on normalised names — catches family
            variants that differ only in parameter count or minor tag
        T6  Longest-key substring containment fallback (legacy behaviour)
        """
        # T1: exact
        if model_name in score_map:
            return score_map[model_name].get(bucket_key, 0.0), "T1:exact"

        # T2: strip org prefix
        base = model_name.split("/", 1)[-1] if "/" in model_name else model_name
        if base in score_map:
            return score_map[base].get(bucket_key, 0.0), "T2:base"

        # T3: strip Ollama ":tag"
        no_tag = model_name.split(":")[0]
        if no_tag in score_map:
            return score_map[no_tag].get(bucket_key, 0.0), "T3:no-tag"
        base_no_tag = base.split(":")[0]
        if base_no_tag in score_map:
            return score_map[base_no_tag].get(bucket_key, 0.0), "T3:base-no-tag"

        # T4: normalised exact match
        norm = _normalize_model_id(model_name)
        if norm in norm_score_index:
            return norm_score_index[norm].get(bucket_key, 0.0), "T4:normalised"

        # T5: token Jaccard on normalised names (threshold 0.55)
        best_score: float = 0.0
        best_sim: float = 0.0
        best_nk: str = ""
        for nk, bscores in norm_score_index.items():
            sim = _token_jaccard(norm, nk)
            if sim > best_sim and sim >= 0.55:
                best_sim = sim
                best_score = bscores.get(bucket_key, 0.0)
                best_nk = nk
        if best_sim >= 0.55:
            return best_score, f"T5:jaccard({best_sim:.2f}→{best_nk})"

        # T6: longest substring containment (legacy)
        mn_lower = model_name.lower()
        sub_score: float = 0.0
        sub_len: int = 0
        for key, bscores in score_map.items():
            if key.lower() in mn_lower and len(key) > sub_len and len(key) > 4:
                sub_len = len(key)
                sub_score = bscores.get(bucket_key, 0.0)
        if sub_len > 4:
            return sub_score, f"T6:substr({sub_len})"

        return 0.0, "T0:no-match"

    def _ranked_for_bucket(
        bucket_key: str,
    ) -> list[tuple[float, str, dict[str, Any]]]:
        """All models sorted descending by score for *bucket_key*.

        Each entry is *(score, tier_label, model_dict)* so the caller can
        include match provenance in the debug output.
        """
        scored = []
        for m in all_models:
            score, tier = _resolve_score(m["model"], bucket_key)
            scored.append((score, tier, m))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored

    def _pick_fallback(
        ranked: list[tuple[float, str, dict[str, Any]]],
        primary_provider_id: str,
    ) -> tuple[dict[str, Any], str] | None:
        """Pick the best fallback from a *different* provider than primary.

        Strategy: pick the highest-scored model from a different provider.
        If scores are tied, prefer local/free backends (byoe → ollama).
        Returns *(model_dict, tier_label)* or None.
        """
        type_priority = {t: i for i, t in enumerate(_FALLBACK_TYPE_PRIORITY)}
        candidates = [
            (score, type_priority.get(m["provider_type"], 99), tier, m)
            for score, tier, m in ranked
            if m["provider_id"] != primary_provider_id
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda x: (-x[0], x[1]))
        return candidates[0][3], candidates[0][2]

    assignments: dict[str, Any] = {}
    score_debug: dict[str, Any] = {}  # returned so callers can audit match quality

    for bucket in VALID_BUCKETS:
        if bucket == "global":
            continue
        ranked = _ranked_for_bucket(bucket)
        if not ranked:
            continue
        # ── Primary: highest-scoring model ──
        p_score, p_tier, best = ranked[0]
        await db.upsert_model_assignment(
            bucket=bucket, rank=1,
            provider_registry_id=best["provider_id"],
            model=best["model"],
        )
        assignments[bucket] = {
            "primary": {
                "provider": best["provider_name"],
                "model": best["model"],
                "score": round(p_score, 2),
                "match_tier": p_tier,
            },
        }
        score_debug[f"{bucket}.primary"] = {"model": best["model"], "score": round(p_score, 2), "tier": p_tier}

        # ── Fallback: best from a different provider ──
        fb_result = _pick_fallback(ranked, best["provider_id"])
        if fb_result:
            fb, fb_tier = fb_result
            fb_score, _, _ = next(
                (s, t, m) for s, t, m in ranked if m["model"] == fb["model"] and m["provider_id"] == fb["provider_id"]
            )
            await db.upsert_model_assignment(
                bucket=bucket, rank=2,
                provider_registry_id=fb["provider_id"],
                model=fb["model"],
            )
            assignments[bucket]["fallback"] = {
                "provider": fb["provider_name"],
                "model": fb["model"],
                "score": round(fb_score, 2),
                "match_tier": fb_tier,
            }
            score_debug[f"{bucket}.fallback"] = {"model": fb["model"], "score": round(fb_score, 2), "tier": fb_tier}

    # ── Global default ──
    ranked_global = _ranked_for_bucket("conversational")  # good general-purpose proxy
    if ranked_global:
        gp_score, gp_tier, gbest = ranked_global[0]
        await db.upsert_model_assignment(
            bucket="global", rank=1,
            provider_registry_id=gbest["provider_id"],
            model=gbest["model"],
        )
        assignments["global"] = {
            "primary": {
                "provider": gbest["provider_name"],
                "model": gbest["model"],
                "score": round(gp_score, 2),
                "match_tier": gp_tier,
            },
        }
        score_debug["global.primary"] = {"model": gbest["model"], "score": round(gp_score, 2), "tier": gp_tier}

        gfb_result = _pick_fallback(ranked_global, gbest["provider_id"])
        if gfb_result:
            gfb, gfb_tier = gfb_result
            gfb_score, _, _ = next(
                (s, t, m) for s, t, m in ranked_global if m["model"] == gfb["model"] and m["provider_id"] == gfb["provider_id"]
            )
            await db.upsert_model_assignment(
                bucket="global", rank=2,
                provider_registry_id=gfb["provider_id"],
                model=gfb["model"],
            )
            assignments["global"]["fallback"] = {
                "provider": gfb["provider_name"],
                "model": gfb["model"],
                "score": round(gfb_score, 2),
                "match_tier": gfb_tier,
            }
            score_debug["global.fallback"] = {"model": gfb["model"], "score": round(gfb_score, 2), "tier": gfb_tier}

    # Log unmatched models so operator can see which models got score=0
    unmatched = [
        m["model"] for _, tier, m in _ranked_for_bucket("reasoning")
        if tier == "T0:no-match"
    ]
    if unmatched:
        _log.info(
            "auto-configure: %d model(s) had no score match (add to static fallback): %s",
            len(unmatched), ", ".join(unmatched[:10]),
        )

    return {
        "configured": True,
        "profile": profile,
        "assignments": assignments,
        "score_debug": score_debug,
    }

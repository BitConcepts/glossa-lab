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

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from glossa_lab.database import get_db

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
    prov_type_map: dict[str, str] = {
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

    # Try to use model_scores for smart assignment
    scores = await db.list_model_scores()
    score_map: dict[str, dict[str, float]] = {}
    for s in scores:
        score_map[s["model_name"]] = {
            "reasoning": s.get("reasoning_score", 0),
            "conversational": s.get("conversational_score", 0),
            "longform": s.get("longform_score", 0),
        }

    def _resolve_score(model_name: str, bucket_key: str) -> float:
        """Resolve a score for *model_name* using multi-tier fuzzy matching.

        Tiers (in priority order):
        1. Exact match on the full model name.
        2. Strip org prefix: "Org/ModelName" → "ModelName"
        3. Strip Ollama tag: "model:tag" → "model"
        4. Partial-name containment — score_map key is a substring of the
           model name (catches quantized variants like
           cpatonn/Qwen3-Coder-30B-A3B-Instruct-AWQ-4bit → Qwen3-Coder-30B)
        5. Reverse containment — model name is a substring of a score key.
        6. Family prefix match: strip suffixes like -Instruct, -AWQ, -4bit, -8B
           and try again.
        """
        # Tier 1: exact
        if model_name in score_map:
            return score_map[model_name].get(bucket_key, 0)

        # Tier 2: strip org prefix
        base = model_name.split("/", 1)[-1] if "/" in model_name else model_name
        if base in score_map:
            return score_map[base].get(bucket_key, 0)

        # Tier 3: strip Ollama ":tag" suffix
        no_tag = model_name.split(":")[0]
        if no_tag in score_map:
            return score_map[no_tag].get(bucket_key, 0)
        base_no_tag = base.split(":")[0]
        if base_no_tag in score_map:
            return score_map[base_no_tag].get(bucket_key, 0)

        # Tier 4: score key is substring of model name (find longest match)
        best_score: float = 0.0
        best_match_len: int = 0
        mn_lower = model_name.lower()
        for key, scores in score_map.items():
            if key.lower() in mn_lower and len(key) > best_match_len:
                best_match_len = len(key)
                best_score = scores.get(bucket_key, 0)
        if best_match_len > 3:  # avoid trivially short matches like "qw"
            return best_score

        # Tier 5: model name is substring of score key
        candidates: list[tuple[int, float]] = []
        for key, scores in score_map.items():
            if mn_lower in key.lower() and len(mn_lower) > 3:
                candidates.append((len(key), scores.get(bucket_key, 0)))
        if candidates:
            return max(candidates, key=lambda x: x[1])[1]

        # Tier 6: family prefix — strip common quantization / instruction tags
        import re as _re  # noqa: PLC0415
        family = _re.sub(
            r"[_\-](instruct|chat|it|awq|gguf|gptq|4bit|8bit|fp16|bf16"
            r"|coder|v\d|a\d+b|\d+b|\d+m)$",
            "", base_no_tag, flags=_re.IGNORECASE,
        ).strip("-_")
        if family and family != base_no_tag:
            if family in score_map:
                return score_map[family].get(bucket_key, 0)
            for key, scores in score_map.items():
                if family.lower() in key.lower() and len(family) > 4:
                    return scores.get(bucket_key, 0)

        return 0.0

    def _ranked_for_bucket(bucket_key: str) -> list[tuple[float, dict[str, Any]]]:
        """All models sorted by score for *bucket_key*, descending."""
        scored = []
        for m in all_models:
            s = _resolve_score(m["model"], bucket_key)
            scored.append((s, m))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored

    def _pick_fallback(
        ranked: list[tuple[float, dict[str, Any]]],
        primary_provider_id: str,
    ) -> dict[str, Any] | None:
        """Pick the best fallback from a *different* provider than primary.

        Strategy: pick the highest-scored model from a different provider.
        If scores are tied, prefer local/free backends (byoe → ollama).
        """
        type_priority = {t: i for i, t in enumerate(_FALLBACK_TYPE_PRIORITY)}
        candidates = [
            (score, type_priority.get(m["provider_type"], 99), m)
            for score, m in ranked
            if m["provider_id"] != primary_provider_id
        ]
        if not candidates:
            return None
        # Sort by: score DESC first, then type-priority ASC as tiebreaker
        candidates.sort(key=lambda x: (-x[0], x[1]))
        return candidates[0][2]

    assignments: dict[str, Any] = {}
    for bucket in VALID_BUCKETS:
        if bucket == "global":
            continue
        ranked = _ranked_for_bucket(bucket)
        if not ranked:
            continue
        # ── Primary: highest score overall ──
        best = ranked[0][1]
        await db.upsert_model_assignment(
            bucket=bucket, rank=1,
            provider_registry_id=best["provider_id"],
            model=best["model"],
        )
        assignments[bucket] = {
            "primary": {"provider": best["provider_name"], "model": best["model"]},
        }
        # ── Fallback: best from a different provider ──
        fb = _pick_fallback(ranked, best["provider_id"])
        if fb:
            await db.upsert_model_assignment(
                bucket=bucket, rank=2,
                provider_registry_id=fb["provider_id"],
                model=fb["model"],
            )
            assignments[bucket]["fallback"] = {
                "provider": fb["provider_name"], "model": fb["model"],
            }

    # ── Global default ──
    # Primary: best overall (any bucket), Fallback: different provider.
    ranked_global = _ranked_for_bucket("conversational")  # good general-purpose proxy
    if ranked_global:
        gbest = ranked_global[0][1]
        await db.upsert_model_assignment(
            bucket="global", rank=1,
            provider_registry_id=gbest["provider_id"],
            model=gbest["model"],
        )
        assignments["global"] = {
            "primary": {"provider": gbest["provider_name"], "model": gbest["model"]},
        }
        gfb = _pick_fallback(ranked_global, gbest["provider_id"])
        if gfb:
            await db.upsert_model_assignment(
                bucket="global", rank=2,
                provider_registry_id=gfb["provider_id"],
                model=gfb["model"],
            )
            assignments["global"]["fallback"] = {
                "provider": gfb["provider_name"], "model": gfb["model"],
            }

    return {"configured": True, "profile": profile, "assignments": assignments}

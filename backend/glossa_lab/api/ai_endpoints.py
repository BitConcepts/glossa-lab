"""AI Endpoints API — bring-your-own model backends.

Distinct from cloud-provider keys (api/settings.py) and Ollama (live-queried).
This registry stores user-managed OpenAI-compatible endpoints (vLLM,
LM Studio, llama.cpp server, OpenRouter, Together, Groq, Fireworks, etc.)
along with their base URL, optional API key, default model, and custom
headers.

Endpoints:
  GET    /api/v1/ai-endpoints              — list all registered endpoints
  POST   /api/v1/ai-endpoints              — register a new endpoint
  GET    /api/v1/ai-endpoints/presets      — built-in connection presets
  GET    /api/v1/ai-endpoints/{id}         — get one
  PATCH  /api/v1/ai-endpoints/{id}         — update fields
  DELETE /api/v1/ai-endpoints/{id}         — remove
  POST   /api/v1/ai-endpoints/{id}/verify  — probe the endpoint and list models
  POST   /api/v1/ai-endpoints/verify       — probe an unsaved endpoint config
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.database import get_db

router = APIRouter(prefix="/api/v1/ai-endpoints", tags=["ai-endpoints"])

# ── Models ─────────────────────────────────────────────────────────────


class AIEndpointCreate(BaseModel):
    name: str
    endpoint_kind: str = "openai_compatible"
    base_url: str = ""
    api_key: str = ""
    default_model: str = ""
    headers: dict[str, str] = {}
    enabled: bool = True
    notes: str = ""


class AIEndpointUpdate(BaseModel):
    name: str | None = None
    endpoint_kind: str | None = None
    base_url: str | None = None
    api_key: str | None = None
    default_model: str | None = None
    headers: dict[str, str] | None = None
    enabled: bool | None = None
    notes: str | None = None


class VerifyRequest(BaseModel):
    base_url: str = ""
    api_key: str = ""
    endpoint_kind: str = "openai_compatible"
    headers: dict[str, str] = {}


# ── Built-in connection presets ─────────────────────────────────────────


_PRESETS: list[dict[str, Any]] = [
    {
        "id": "vllm",
        "label": "vLLM (local)",
        "description": "Self-hosted vLLM OpenAI-compatible server.",
        "endpoint_kind": "openai_compatible",
        "base_url": "http://localhost:8000/v1",
        "needs_key": False,
    },
    {
        "id": "lm_studio",
        "label": "LM Studio (local)",
        "description": "LM Studio's OpenAI-compatible local server.",
        "endpoint_kind": "openai_compatible",
        "base_url": "http://localhost:1234/v1",
        "needs_key": False,
    },
    {
        "id": "llama_cpp",
        "label": "llama.cpp server (local)",
        "description": "llama.cpp `server` binary OpenAI-compatible mode.",
        "endpoint_kind": "openai_compatible",
        "base_url": "http://localhost:8080/v1",
        "needs_key": False,
    },
    {
        "id": "openrouter",
        "label": "OpenRouter",
        "description": "Unified gateway over many cloud LLMs.",
        "endpoint_kind": "openai_compatible",
        "base_url": "https://openrouter.ai/api/v1",
        "needs_key": True,
    },
    {
        "id": "together",
        "label": "Together AI",
        "description": "Together.ai OpenAI-compatible inference endpoint.",
        "endpoint_kind": "openai_compatible",
        "base_url": "https://api.together.xyz/v1",
        "needs_key": True,
    },
    {
        "id": "groq",
        "label": "Groq",
        "description": "Groq LPU OpenAI-compatible inference.",
        "endpoint_kind": "openai_compatible",
        "base_url": "https://api.groq.com/openai/v1",
        "needs_key": True,
    },
    {
        "id": "fireworks",
        "label": "Fireworks AI",
        "description": "Fireworks.ai OpenAI-compatible inference.",
        "endpoint_kind": "openai_compatible",
        "base_url": "https://api.fireworks.ai/inference/v1",
        "needs_key": True,
    },
    {
        "id": "deepinfra",
        "label": "DeepInfra",
        "description": "DeepInfra OpenAI-compatible inference.",
        "endpoint_kind": "openai_compatible",
        "base_url": "https://api.deepinfra.com/v1/openai",
        "needs_key": True,
    },
    {
        "id": "perplexity",
        "label": "Perplexity",
        "description": "Perplexity OpenAI-compatible inference.",
        "endpoint_kind": "openai_compatible",
        "base_url": "https://api.perplexity.ai",
        "needs_key": True,
    },
    {
        "id": "azure_openai",
        "label": "Azure OpenAI",
        "description": "Azure OpenAI deployment (set deployment URL as base URL).",
        "endpoint_kind": "openai_compatible",
        "base_url": "",
        "needs_key": True,
    },
    {
        "id": "custom",
        "label": "Custom",
        "description": "Any other OpenAI-compatible HTTP endpoint.",
        "endpoint_kind": "openai_compatible",
        "base_url": "",
        "needs_key": False,
    },
]


# ── Helpers ─────────────────────────────────────────────────────────────


def _normalize_base(url: str) -> str:
    return (url or "").strip().rstrip("/")


def _models_url(base_url: str) -> str:
    base = _normalize_base(base_url)
    if not base:
        return ""
    # If the user supplied a base_url that already ends in /v1 we hit
    # /v1/models; otherwise try /v1/models first.
    if base.endswith("/v1"):
        return f"{base}/models"
    return f"{base}/v1/models"


def _probe_models(
    *,
    base_url: str,
    api_key: str,
    endpoint_kind: str,
    headers: dict[str, str] | None,
) -> dict[str, Any]:
    """Hit GET {base}/v1/models on the endpoint and report success + models."""
    url = _models_url(base_url)
    if not url:
        return {"valid": False, "message": "Base URL is empty.", "models": []}

    req_headers: dict[str, str] = {"Accept": "application/json"}
    if api_key:
        if endpoint_kind == "anthropic_compatible":
            req_headers["x-api-key"] = api_key
            req_headers["anthropic-version"] = "2023-06-01"
        else:
            req_headers["Authorization"] = f"Bearer {api_key}"
    if headers:
        req_headers.update(headers)

    try:
        req = urllib.request.Request(url, headers=req_headers, method="GET")
        with urllib.request.urlopen(req, timeout=8) as resp:  # noqa: S310
            raw = resp.read().decode("utf-8", errors="replace")
            status = resp.status
        if status != 200:
            return {
                "valid": False,
                "message": f"Unexpected status {status}.",
                "models": [],
            }
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            return {
                "valid": True,
                "message": "Endpoint responded but body was not JSON.",
                "models": [],
            }
        # OpenAI-compatible: {"data":[{"id":...}, ...]}
        models: list[str] = []
        for entry in (payload.get("data") or payload.get("models") or []):
            if isinstance(entry, dict):
                mid = entry.get("id") or entry.get("name") or entry.get("model")
                if mid:
                    models.append(str(mid))
            elif isinstance(entry, str):
                models.append(entry)
        return {
            "valid": True,
            "message": f"OK — {len(models)} model(s) reachable.",
            "models": models[:200],  # cap to keep response small
        }
    except urllib.error.HTTPError as exc:
        msg = f"HTTP {exc.code}: {exc.reason}"
        if exc.code in (401, 403):
            msg = f"Unauthorized (HTTP {exc.code}). Check API key."
        return {"valid": False, "message": msg, "models": []}
    except Exception as exc:  # noqa: BLE001
        return {"valid": False, "message": f"Connection error: {exc}", "models": []}


# ── Routes ─────────────────────────────────────────────────────────────


@router.get("/presets")
async def list_presets() -> dict[str, Any]:
    return {"presets": _PRESETS}


@router.get("")
async def list_endpoints(enabled_only: bool = False) -> dict[str, Any]:
    db = get_db()
    if db is None:
        return {"endpoints": []}
    rows = await db.list_ai_endpoints(enabled_only=enabled_only)
    # Mask api_key in list responses
    for r in rows:
        if r.get("api_key"):
            r["api_key_set"] = True
            r["api_key"] = ""
        else:
            r["api_key_set"] = False
    return {"endpoints": rows}


@router.post("")
async def create_endpoint(body: AIEndpointCreate) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    row = await db.create_ai_endpoint(
        name=body.name,
        endpoint_kind=body.endpoint_kind,
        base_url=_normalize_base(body.base_url),
        api_key=body.api_key,
        default_model=body.default_model,
        headers=body.headers,
        enabled=body.enabled,
        notes=body.notes,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    if row.get("api_key"):
        row["api_key_set"] = True
        row["api_key"] = ""
    else:
        row["api_key_set"] = False
    return row


@router.get("/{eid}")
async def get_endpoint(eid: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    row = await db.get_ai_endpoint(eid)
    if row is None:
        raise HTTPException(404, "Endpoint not found")
    if row.get("api_key"):
        row["api_key_set"] = True
        row["api_key"] = ""
    else:
        row["api_key_set"] = False
    return row


@router.patch("/{eid}")
async def update_endpoint(eid: str, body: AIEndpointUpdate) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    update: dict[str, Any] = {}
    for k, v in body.model_dump(exclude_unset=True).items():
        if k == "base_url" and v is not None:
            update[k] = _normalize_base(v)
        else:
            update[k] = v
    row = await db.update_ai_endpoint(eid, **update)
    if row is None:
        raise HTTPException(404, "Endpoint not found")
    if row.get("api_key"):
        row["api_key_set"] = True
        row["api_key"] = ""
    else:
        row["api_key_set"] = False
    return row


@router.delete("/{eid}")
async def delete_endpoint(eid: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    row = await db.delete_ai_endpoint(eid)
    if row is None:
        raise HTTPException(404, "Endpoint not found")
    return {"deleted": True, "id": eid}


@router.post("/{eid}/verify")
async def verify_endpoint(eid: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    row = await db.get_ai_endpoint(eid)
    if row is None:
        raise HTTPException(404, "Endpoint not found")
    return _probe_models(
        base_url=row["base_url"],
        api_key=row["api_key"],
        endpoint_kind=row["endpoint_kind"],
        headers=row.get("headers") or {},
    )


@router.post("/verify")
async def verify_unsaved(body: VerifyRequest) -> dict[str, Any]:
    return _probe_models(
        base_url=body.base_url,
        api_key=body.api_key,
        endpoint_kind=body.endpoint_kind,
        headers=body.headers or {},
    )

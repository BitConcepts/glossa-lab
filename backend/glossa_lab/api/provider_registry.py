"""Provider Registry API — unified provider management.

Replaces the scattered ai_endpoints + .keys.json + Ollama prefs with a
single flat list of configured providers.  Each entry is one of 4 types:
cloud, ollama, byoe, huggingface.

Endpoints:
  GET    /api/v1/providers                — list all registered providers
  POST   /api/v1/providers                — register a new provider
  GET    /api/v1/providers/{id}           — get one
  PATCH  /api/v1/providers/{id}           — update fields
  DELETE /api/v1/providers/{id}           — remove
  POST   /api/v1/providers/{id}/test      — probe the provider and list models
  POST   /api/v1/providers/test-unsaved   — probe an unsaved provider config
  GET    /api/v1/providers/detect-ollama  — auto-detect Ollama on LAN
"""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.database import get_db

router = APIRouter(prefix="/api/v1/providers", tags=["providers"])
_log = logging.getLogger(__name__)

# ── Known cloud provider URLs ──────────────────────────────────────────────

CLOUD_PROVIDERS: dict[str, dict[str, str]] = {
    "openai":     {"label": "OpenAI",     "base_url": "https://api.openai.com/v1",         "models_url": "https://api.openai.com/v1/models"},
    "anthropic":  {"label": "Anthropic",  "base_url": "https://api.anthropic.com/v1",      "models_url": "https://api.anthropic.com/v1/models"},
    "mistral":    {"label": "Mistral",    "base_url": "https://api.mistral.ai/v1",         "models_url": "https://api.mistral.ai/v1/models"},
    "google":     {"label": "Google",     "base_url": "https://generativelanguage.googleapis.com/v1beta", "models_url": ""},
    "groq":       {"label": "Groq",       "base_url": "https://api.groq.com/openai/v1",   "models_url": "https://api.groq.com/openai/v1/models"},
    "together":   {"label": "Together",   "base_url": "https://api.together.xyz/v1",       "models_url": "https://api.together.xyz/v1/models"},
    "fireworks":  {"label": "Fireworks",  "base_url": "https://api.fireworks.ai/inference/v1", "models_url": "https://api.fireworks.ai/inference/v1/models"},
    "deepinfra":  {"label": "DeepInfra",  "base_url": "https://api.deepinfra.com/v1/openai", "models_url": "https://api.deepinfra.com/v1/openai/models"},
    "openrouter": {"label": "OpenRouter", "base_url": "https://openrouter.ai/api/v1",     "models_url": "https://openrouter.ai/api/v1/models"},
    "perplexity": {"label": "Perplexity", "base_url": "https://api.perplexity.ai",        "models_url": ""},
}

# ── Models ─────────────────────────────────────────────────────────────────


class ProviderCreate(BaseModel):
    name: str
    provider_type: str = "cloud"  # cloud | ollama | byoe | huggingface
    provider_id: str = ""         # e.g. "openai", "ollama", "byoe"
    base_url: str = ""
    api_key: str = ""
    headers: dict[str, str] = {}
    enabled: bool = True
    notes: str = ""


class ProviderUpdate(BaseModel):
    name: str | None = None
    provider_type: str | None = None
    provider_id: str | None = None
    base_url: str | None = None
    api_key: str | None = None
    headers: dict[str, str] | None = None
    enabled: bool | None = None
    notes: str | None = None


class TestRequest(BaseModel):
    provider_type: str = "byoe"
    provider_id: str = ""
    base_url: str = ""
    api_key: str = ""
    headers: dict[str, str] = {}


# ── Probe helpers ──────────────────────────────────────────────────────────


def _probe_openai_compatible(
    base_url: str, api_key: str = "", headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Hit GET {base}/models on an OpenAI-compatible endpoint."""
    base = (base_url or "").strip().rstrip("/")
    url = f"{base}/models" if base.endswith("/v1") else f"{base}/v1/models"
    req_headers: dict[str, str] = {"Accept": "application/json"}
    if api_key:
        req_headers["Authorization"] = f"Bearer {api_key}"
    if headers:
        req_headers.update(headers)
    try:
        req = urllib.request.Request(url, headers=req_headers, method="GET")
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
        models = []
        for entry in (data.get("data") or data.get("models") or []):
            if isinstance(entry, dict):
                mid = entry.get("id") or entry.get("name") or ""
                if mid:
                    models.append(str(mid))
            elif isinstance(entry, str):
                models.append(entry)
        return {"valid": True, "message": f"OK — {len(models)} model(s)", "models": models[:200]}
    except urllib.error.HTTPError as exc:
        msg = f"HTTP {exc.code}: {exc.reason}"
        if exc.code in (401, 403):
            msg = f"Unauthorized (HTTP {exc.code}). Check API key."
        return {"valid": False, "message": msg, "models": []}
    except Exception as exc:  # noqa: BLE001
        return {"valid": False, "message": f"Connection error: {exc}", "models": []}


def _probe_ollama(base_url: str) -> dict[str, Any]:
    """Probe Ollama at the given base URL."""
    base = (base_url or "http://localhost:11434").strip().rstrip("/")
    try:
        req = urllib.request.Request(f"{base}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        models = [m["name"] for m in data.get("models", []) if m.get("name")]
        return {"valid": True, "message": f"OK — {len(models)} model(s) installed", "models": models}
    except Exception as exc:  # noqa: BLE001
        return {"valid": False, "message": f"Not reachable: {exc}", "models": []}


def _probe_anthropic(api_key: str) -> dict[str, Any]:
    """Probe Anthropic API (non-standard auth)."""
    try:
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/models",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "Accept": "application/json",
            },
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
        models = [m.get("id", "") for m in data.get("data", []) if m.get("id")]
        return {"valid": True, "message": f"OK — {len(models)} model(s)", "models": models[:100]}
    except urllib.error.HTTPError as exc:
        return {"valid": False, "message": f"HTTP {exc.code}: {exc.reason}", "models": []}
    except Exception as exc:  # noqa: BLE001
        return {"valid": False, "message": str(exc), "models": []}


def probe_provider(
    provider_type: str, provider_id: str,
    base_url: str, api_key: str, headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Probe any provider and return {valid, message, models}."""
    if provider_type == "ollama":
        return _probe_ollama(base_url)
    if provider_type == "cloud" and provider_id == "anthropic":
        return _probe_anthropic(api_key)
    # Everything else is OpenAI-compatible
    return _probe_openai_compatible(base_url, api_key, headers)


# ── Routes ─────────────────────────────────────────────────────────────────


@router.get("/cloud-providers")
async def list_cloud_providers() -> dict[str, Any]:
    """Return the catalog of known cloud providers with their default URLs."""
    return {"providers": [
        {"id": k, **v} for k, v in CLOUD_PROVIDERS.items()
    ]}


@router.get("")
async def list_providers(
    enabled_only: bool = False,
    provider_type: str | None = None,
) -> dict[str, Any]:
    db = get_db()
    if db is None:
        return {"providers": []}
    rows = await db.list_providers(enabled_only=enabled_only, provider_type=provider_type)
    # Mask API keys in list responses
    for r in rows:
        if r.get("api_key"):
            r["api_key_set"] = True
            r["api_key"] = ""
        else:
            r["api_key_set"] = False
    return {"providers": rows}


@router.post("")
async def create_provider(body: ProviderCreate) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    # Auto-fill base_url for known cloud providers
    base_url = body.base_url
    if body.provider_type == "cloud" and not base_url and body.provider_id in CLOUD_PROVIDERS:
        base_url = CLOUD_PROVIDERS[body.provider_id]["base_url"]
    row = await db.create_provider(
        name=body.name,
        provider_type=body.provider_type,
        provider_id=body.provider_id or body.provider_type,
        base_url=base_url,
        api_key=body.api_key,
        headers=body.headers,
        enabled=body.enabled,
        notes=body.notes,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    if row and row.get("api_key"):
        row["api_key_set"] = True
        row["api_key"] = ""
    return row


@router.get("/{pid}")
async def get_provider(pid: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    row = await db.get_provider(pid)
    if row is None:
        raise HTTPException(404, "Provider not found")
    if row.get("api_key"):
        row["api_key_set"] = True
        row["api_key"] = ""
    return row


@router.patch("/{pid}")
async def update_provider(pid: str, body: ProviderUpdate) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    update = {k: v for k, v in body.model_dump(exclude_unset=True).items()}
    row = await db.update_provider(pid, **update)
    if row is None:
        raise HTTPException(404, "Provider not found")
    if row.get("api_key"):
        row["api_key_set"] = True
        row["api_key"] = ""
    return row


@router.delete("/{pid}")
async def delete_provider(pid: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    row = await db.delete_provider(pid)
    if row is None:
        raise HTTPException(404, "Provider not found")
    return {"deleted": True, "id": pid}


@router.post("/{pid}/test")
async def test_provider(pid: str) -> dict[str, Any]:
    """Probe a saved provider, update its status and available models."""
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    row = await db.get_provider(pid)
    if row is None:
        raise HTTPException(404, "Provider not found")

    import asyncio  # noqa: PLC0415
    result = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: probe_provider(
            row["provider_type"], row.get("provider_id", ""),
            row["base_url"], row["api_key"], row.get("headers"),
        ),
    )
    # Update provider status + cached models
    now = datetime.now(timezone.utc).isoformat()
    await db.update_provider(
        pid,
        status="reachable" if result["valid"] else "unreachable",
        available_models=result.get("models", []),
        last_probed_at=now,
    )
    return result


@router.post("/test-unsaved")
async def test_unsaved(body: TestRequest) -> dict[str, Any]:
    """Probe an unsaved provider config."""
    import asyncio  # noqa: PLC0415
    result = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: probe_provider(
            body.provider_type, body.provider_id,
            body.base_url, body.api_key, body.headers,
        ),
    )
    return result


@router.get("/detect-ollama")
async def detect_ollama() -> dict[str, Any]:
    """Auto-detect Ollama on localhost and common LAN addresses."""
    import asyncio  # noqa: PLC0415

    candidates = [
        "http://localhost:11434",
        "http://127.0.0.1:11434",
        "http://host.docker.internal:11434",
    ]
    # Add common LAN gateway addresses
    for prefix in ("192.168.1", "192.168.0", "10.0.0", "10.0.1"):
        candidates.append(f"http://{prefix}.1:11434")

    results: list[dict[str, Any]] = []

    def _check(url: str) -> dict[str, Any] | None:
        r = _probe_ollama(url)
        if r["valid"]:
            return {"url": url, **r}
        return None

    loop = asyncio.get_event_loop()
    # Probe in parallel with short timeout
    tasks = [loop.run_in_executor(None, _check, url) for url in candidates]
    for coro in asyncio.as_completed(tasks):
        result = await coro
        if result:
            results.append(result)

    return {"detected": results}

"""Shared LLM utility for AI-powered features in Glossa Lab.

Resolution:
  1. If provider_override + model_override are supplied, use those directly.
  2. If a `bucket` is specified, resolve via model_assignments table:
     primary for bucket → fallback for bucket → primary global → fallback global.
  3. Legacy fallback: Ollama → cloud keys → BYOE endpoint (for callers
     that haven't been migrated to bucket-based yet).

Uses stdlib urllib so no optional packages are required beyond the API key.
"""

from __future__ import annotations

import json
import logging
import sqlite3
import urllib.error
import urllib.request
from typing import Any

_log = logging.getLogger(__name__)


def _endpoint_chat_url(base_url: str) -> str:
    """Build the /chat/completions URL from an endpoint's base_url."""
    base = (base_url or "").strip().rstrip("/")
    if base.endswith("/v1"):
        return f"{base}/chat/completions"
    return f"{base}/v1/chat/completions"


def _get_endpoint_config(
    endpoint_id: str | None = None,
) -> dict[str, Any] | None:
    """Load a custom endpoint config using sync sqlite3.

    If *endpoint_id* is given, load that specific endpoint.
    Otherwise, find the first default AI Profile whose backend_kind is
    'endpoint' and resolve its linked endpoint.

    Safe to call from a thread-pool executor (sync I/O only).
    Returns {base_url, api_key, model, headers, endpoint_kind} or None.
    """
    from glossa_lab.database import get_db  # noqa: PLC0415

    db = get_db()
    if db is None:
        return None
    db_path = str(db._path)  # noqa: SLF001

    try:
        conn = sqlite3.connect(db_path, timeout=3)
        conn.row_factory = sqlite3.Row

        ep_id = endpoint_id
        model: str = ""

        if not ep_id:
            # Look for a default endpoint-backed profile.
            # Prefer global default, then any default with backend_kind='endpoint'.
            cur = conn.execute(
                "SELECT backend_ref, model FROM ai_profiles "
                "WHERE is_default=1 AND backend_kind='endpoint' "
                "ORDER BY role ASC LIMIT 1",
            )
            row = cur.fetchone()
            if row:
                ep_id = row["backend_ref"]
                model = row["model"] or ""
            else:
                # No default — try any enabled endpoint-backed profile
                cur = conn.execute(
                    "SELECT backend_ref, model FROM ai_profiles "
                    "WHERE backend_kind='endpoint' LIMIT 1",
                )
                row = cur.fetchone()
                if row:
                    ep_id = row["backend_ref"]
                    model = row["model"] or ""

        if not ep_id:
            conn.close()
            return None

        cur = conn.execute(
            "SELECT * FROM ai_endpoints WHERE id=? AND enabled=1",
            (ep_id,),
        )
        ep = cur.fetchone()
        conn.close()

        if not ep:
            return None

        headers: dict[str, str] = {}
        if ep["headers_json"]:
            try:
                headers = json.loads(ep["headers_json"])
            except (json.JSONDecodeError, ValueError):
                pass

        return {
            "base_url": ep["base_url"] or "",
            "api_key": ep["api_key"] or "",
            "model": model or ep["default_model"] or "",
            "headers": headers,
            "endpoint_kind": ep["endpoint_kind"] or "openai_compatible",
            "name": ep["name"] or ep_id,
        }
    except Exception:  # noqa: BLE001
        _log.debug("_get_endpoint_config failed", exc_info=True)
        return None


def _extract_json(text: str) -> str:
    """Robustly extract JSON from a model response.

    Tries in order:
      1. Direct json.loads (fast path)
      2. JSON inside a ```json...``` code fence
      3. JSON inside any ```...``` code fence
      4. First { } balanced block in the response
    Returns the raw JSON string, or raises ValueError if nothing parses.
    """
    import re  # noqa: PLC0415

    # Fast path: already valid JSON
    try:
        json.loads(text)
        return text
    except Exception:  # noqa: BLE001
        pass

    # Try ```json ... ``` fence
    for pattern in (r"```json\s*(\{.*?\})\s*```", r"```\s*(\{.*?\})\s*``"):
        m = re.search(pattern, text, re.DOTALL)
        if m:
            candidate = m.group(1).strip()
            try:
                json.loads(candidate)
                return candidate
            except Exception:  # noqa: BLE001
                pass

    # Try first balanced { } block
    depth = 0
    start = -1
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start >= 0:
                candidate = text[start: i + 1]
                try:
                    json.loads(candidate)
                    return candidate
                except Exception:  # noqa: BLE001
                    break

    raise ValueError(f"Could not extract valid JSON from model response. Raw: {text[:200]!r}")


def _get_provider_prefs() -> dict[str, Any]:
    """Load saved provider preferences from the keys store."""
    from glossa_lab.api.settings import _PROVIDERS_KEY, _load_keys  # noqa: PLC0415
    return _load_keys().get(_PROVIDERS_KEY, {})


def _call_ollama(
    model: str,
    messages: list[dict[str, str]],
    max_tokens: int,
    temperature: float,
    json_mode: bool = False,
    base_url: str = "http://localhost:11434",
) -> str:
    """Call an Ollama instance via its /api/chat endpoint."""
    base = (base_url or "http://localhost:11434").rstrip("/")
    payload: dict = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }
    if json_mode:
        payload["format"] = "json"
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{base}/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode())
        return data["message"]["content"]
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Ollama not reachable at {base}. "
            f"Is 'ollama serve' running? Error: {exc}"
        ) from exc
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Ollama request failed: {exc}") from exc


def call_llm(
    messages: list[dict[str, str]],
    *,
    bucket: str = "",
    json_mode: bool = False,
    json_schema: dict[str, Any] | None = None,
    max_tokens: int = 2000,
    temperature: float = 0.3,
    provider_override: str | None = None,
    model_override: str | None = None,
) -> str:
    """Call the configured LLM and return the assistant message text.

    Resolution:
      0. If provider_override + model_override are supplied, use those directly.
      1. If `bucket` is set, resolve via model_assignments table:
         primary → fallback → global primary → global fallback.
      2. Legacy fallback: old waterfall (Ollama → cloud keys → endpoint).

    Returns (text, ai_meta) when called via call_llm_with_meta(), or just
    the text string for backward compatibility.

    Raises ValueError if no provider is available.
    Raises RuntimeError on API/network error.
    """
    # ── 0. Explicit override (from AI chat model picker) ───────────────────────
    if provider_override and model_override:
        return _dispatch_override(
            provider_override, model_override, messages,
            json_mode=json_mode, json_schema=json_schema,
            max_tokens=max_tokens, temperature=temperature,
        )

    # ── 1. Bucket-based resolution (new system) ────────────────────────────
    if bucket:
        resolved = _resolve_bucket_sync(bucket)
        if resolved:
            prov = resolved["_provider"]
            model = resolved["model"]
            params = resolved.get("params") or {}
            eff_temp = params.get("temperature", temperature)
            eff_max = params.get("max_tokens", max_tokens)
            is_fb = resolved.get("rank", 1) == 2 or resolved.get("bucket") != bucket
            _log.info(
                "call_llm → bucket=%s provider=%s model=%s%s",
                bucket, prov["name"], model,
                " (fallback)" if is_fb else "",
            )
            return _dispatch_provider(
                prov, model, messages,
                json_mode=json_mode, json_schema=json_schema,
                max_tokens=eff_max, temperature=eff_temp,
            )

    # ── 2. Legacy waterfall (backward compat for callers without bucket) ────
    return _legacy_waterfall(
        messages, json_mode=json_mode, json_schema=json_schema,
        max_tokens=max_tokens, temperature=temperature,
    )


def call_llm_with_meta(
    messages: list[dict[str, str]],
    **kwargs: Any,
) -> tuple[str, dict[str, Any]]:
    """Like call_llm() but also returns AI metadata for output badges."""
    bucket = kwargs.get("bucket", "")
    provider_override = kwargs.get("provider_override")
    model_override = kwargs.get("model_override")

    # Try bucket resolution to get meta
    meta: dict[str, Any] = {"provider": "", "model": "", "bucket": bucket, "is_fallback": False}
    if not (provider_override and model_override) and bucket:
        resolved = _resolve_bucket_sync(bucket)
        if resolved:
            prov = resolved["_provider"]
            meta = {
                "provider": prov.get("name", ""),
                "provider_id": prov.get("id", ""),
                "provider_type": prov.get("provider_type", ""),
                "model": resolved["model"],
                "bucket": resolved.get("bucket", bucket),
                "is_fallback": resolved.get("rank", 1) == 2 or resolved.get("bucket") != bucket,
            }
    text = call_llm(messages, **kwargs)
    return text, meta


# ── Bucket resolution (sync, for use in thread executor) ──────────────────


def _resolve_bucket_sync(bucket: str) -> dict[str, Any] | None:
    """Sync sqlite3 lookup for model_assignments + provider_registry."""
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        return None
    db_path = str(db._path)  # noqa: SLF001
    try:
        conn = sqlite3.connect(db_path, timeout=3)
        conn.row_factory = sqlite3.Row
        for b in (bucket, "global"):
            for rank in (1, 2):
                cur = conn.execute(
                    "SELECT * FROM model_assignments WHERE bucket=? AND rank=?",
                    (b, rank),
                )
                row = cur.fetchone()
                if not row:
                    continue
                prov_id = row["provider_registry_id"]
                pcur = conn.execute(
                    "SELECT * FROM provider_registry WHERE id=? AND enabled=1",
                    (prov_id,),
                )
                prov = pcur.fetchone()
                if not prov:
                    continue
                headers = {}
                try:
                    headers = json.loads(prov["headers_json"] or "{}")
                except Exception:  # noqa: BLE001
                    pass
                conn.close()
                params = {}
                try:
                    params = json.loads(row["params_json"] or "{}")
                except Exception:  # noqa: BLE001
                    pass
                return {
                    "bucket": b,
                    "rank": row["rank"],
                    "model": row["model"],
                    "params": params,
                    "_provider": {
                        "id": prov["id"],
                        "name": prov["name"],
                        "provider_type": prov["provider_type"],
                        "provider_id": prov["provider_id"],
                        "base_url": prov["base_url"],
                        "api_key": prov["api_key"],
                        "headers": headers,
                    },
                }
        conn.close()
    except Exception:  # noqa: BLE001
        _log.debug("_resolve_bucket_sync failed", exc_info=True)
    return None


# ── Provider dispatch ──────────────────────────────────────────────────


def _dispatch_provider(
    prov: dict[str, Any], model: str,
    messages: list[dict[str, str]], *,
    json_mode: bool = False, json_schema: dict[str, Any] | None = None,
    max_tokens: int = 2000, temperature: float = 0.3,
) -> str:
    """Route a request to the right backend based on provider_type."""
    ptype = prov.get("provider_type", "")
    pid = prov.get("provider_id", "")
    base_url = prov.get("base_url", "")
    api_key = prov.get("api_key", "")
    headers = prov.get("headers") or {}

    # Ollama
    if ptype == "ollama":
        return _call_ollama(
            model=model, messages=messages,
            max_tokens=max_tokens, temperature=temperature,
            json_mode=json_mode, base_url=base_url or "http://localhost:11434",
        )

    # Anthropic (non-standard auth)
    if ptype == "cloud" and pid == "anthropic":
        sys_msgs = [m for m in messages if m["role"] == "system"]
        usr_msgs = [m for m in messages if m["role"] != "system"]
        payload: dict[str, Any] = {"model": model, "max_tokens": max_tokens, "messages": usr_msgs}
        if sys_msgs:
            payload["system"] = " ".join(m["content"] for m in sys_msgs)
        return _call_remote(
            f"{base_url}/messages" if base_url else "https://api.anthropic.com/v1/messages",
            payload,
            auth_header=api_key, auth_header_name="x-api-key",
            extra_headers={"anthropic-version": "2023-06-01"},
            response_path=["content", 0, "text"],
        )

    # Everything else: OpenAI-compatible (cloud, byoe, huggingface)
    chat_url = _endpoint_chat_url(base_url)
    payload = {
        "model": model, "messages": messages,
        "max_tokens": max_tokens, "temperature": temperature,
    }
    if json_schema and ptype in ("byoe", "huggingface"):
        payload["guided_json"] = json_schema
        payload["chat_template_kwargs"] = {"enable_thinking": False}
    elif json_mode:
        payload["response_format"] = {"type": "json_object"}
        if ptype in ("byoe", "huggingface"):
            payload["chat_template_kwargs"] = {"enable_thinking": False}
    return _call_remote(
        chat_url, payload,
        auth_header=f"Bearer {api_key}" if api_key else "Bearer ",
        extra_headers=headers or None,
    )


def _dispatch_override(
    provider_override: str, model_override: str,
    messages: list[dict[str, str]], *,
    json_mode: bool = False, json_schema: dict[str, Any] | None = None,
    max_tokens: int = 2000, temperature: float = 0.3,
) -> str:
    """Handle explicit provider_override + model_override."""
    from glossa_lab.api.settings import get_key  # noqa: PLC0415

    if provider_override == "ollama":
        return _call_ollama(
            model=model_override, messages=messages,
            max_tokens=max_tokens, temperature=temperature,
            json_mode=json_mode,
        )
    if provider_override == "anthropic":
        key = get_key("anthropic_api_key")
        if not key:
            raise ValueError("Anthropic API key not set")
        sys_msgs = [m for m in messages if m["role"] == "system"]
        usr_msgs = [m for m in messages if m["role"] != "system"]
        payload: dict[str, Any] = {"model": model_override, "max_tokens": max_tokens, "messages": usr_msgs}
        if sys_msgs:
            payload["system"] = " ".join(m["content"] for m in sys_msgs)
        return _call_remote(
            "https://api.anthropic.com/v1/messages", payload,
            auth_header=key, auth_header_name="x-api-key",
            extra_headers={"anthropic-version": "2023-06-01"},
            response_path=["content", 0, "text"],
        )
    # OpenAI-compatible cloud providers
    if provider_override in ("openai", "mistral", "groq", "together", "fireworks", "deepinfra", "openrouter"):
        from glossa_lab.api.provider_registry import CLOUD_PROVIDERS  # noqa: PLC0415
        cp = CLOUD_PROVIDERS.get(provider_override, {})
        base = cp.get("base_url", f"https://api.{provider_override}.com/v1")
        key = get_key(f"{provider_override}_api_key") or ""
        payload = {
            "model": model_override, "messages": messages,
            "max_tokens": max_tokens, "temperature": temperature,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        return _call_remote(
            f"{base}/chat/completions", payload,
            auth_header=f"Bearer {key}",
        )
    # endpoint:<id> or generic endpoint
    if provider_override.startswith("endpoint"):
        parts = provider_override.split(":", 1)
        ep_id = parts[1] if len(parts) > 1 else None
        ep = _get_endpoint_config(endpoint_id=ep_id)
        if ep is None:
            raise ValueError(f"Custom endpoint '{ep_id or 'default'}' not found.")
        chat_url = _endpoint_chat_url(ep["base_url"])
        payload = {
            "model": model_override or ep["model"],
            "messages": messages,
            "max_tokens": max_tokens, "temperature": temperature,
        }
        if json_schema:
            payload["guided_json"] = json_schema
            payload["chat_template_kwargs"] = {"enable_thinking": False}
        elif json_mode:
            payload["response_format"] = {"type": "json_object"}
            payload["chat_template_kwargs"] = {"enable_thinking": False}
        return _call_remote(
            chat_url, payload,
            auth_header=f"Bearer {ep['api_key']}" if ep["api_key"] else "Bearer ",
            extra_headers=ep["headers"] or None,
        )
    raise ValueError(f"Unknown provider override: {provider_override}")


# ── Legacy waterfall (kept for backward compat) ──────────────────────────


def _legacy_waterfall(
    messages: list[dict[str, str]], *,
    json_mode: bool = False, json_schema: dict[str, Any] | None = None,
    max_tokens: int = 2000, temperature: float = 0.3,
) -> str:
    """Old hardcoded provider resolution. Used when no bucket is specified."""
    from glossa_lab.api.settings import get_key  # noqa: PLC0415
    from glossa_lab.model_profiles import get_profile  # noqa: PLC0415

    prefs = _get_provider_prefs()
    ollama_pref = prefs.get("ollama", {})

    if ollama_pref.get("enabled") and ollama_pref.get("selected_model"):
        sel = ollama_pref["selected_model"]
        p = get_profile(sel)
        return _call_ollama(
            model=sel, messages=messages,
            max_tokens=max_tokens if max_tokens != 2000 else p["max_tokens"],
            temperature=temperature if temperature != 0.3 else p["temperature"],
            json_mode=json_mode,
        )
    for prov_key, url_base in [
        ("mistral_api_key", "https://api.mistral.ai/v1/chat/completions"),
        ("openai_api_key", "https://api.openai.com/v1/chat/completions"),
    ]:
        key = get_key(prov_key)
        if key:
            default_model = {
                "mistral_api_key": "mistral-small-latest",
                "openai_api_key": "gpt-4o-mini",
            }.get(prov_key, "")
            payload: dict[str, Any] = {
                "model": prefs.get(prov_key.split("_")[0], {}).get("selected_model", default_model),
                "messages": messages,
                "max_tokens": max_tokens, "temperature": temperature,
            }
            if json_mode:
                payload["response_format"] = {"type": "json_object"}
            return _call_remote(url_base, payload, auth_header=f"Bearer {key}")
    anthropic_key = get_key("anthropic_api_key")
    if anthropic_key:
        sys_msgs = [m for m in messages if m["role"] == "system"]
        usr_msgs = [m for m in messages if m["role"] != "system"]
        payload = {
            "model": prefs.get("anthropic", {}).get("selected_model", "claude-3-5-haiku-latest"),
            "max_tokens": max_tokens, "messages": usr_msgs,
        }
        if sys_msgs:
            payload["system"] = " ".join(m["content"] for m in sys_msgs)
        return _call_remote(
            "https://api.anthropic.com/v1/messages", payload,
            auth_header=anthropic_key, auth_header_name="x-api-key",
            extra_headers={"anthropic-version": "2023-06-01"},
            response_path=["content", 0, "text"],
        )
    ep = _get_endpoint_config()
    if ep:
        chat_url = _endpoint_chat_url(ep["base_url"])
        payload = {
            "model": ep["model"], "messages": messages,
            "max_tokens": max_tokens, "temperature": temperature,
        }
        if json_schema:
            payload["guided_json"] = json_schema
            payload["chat_template_kwargs"] = {"enable_thinking": False}
        elif json_mode:
            payload["response_format"] = {"type": "json_object"}
            payload["chat_template_kwargs"] = {"enable_thinking": False}
        _log.info("call_llm → legacy endpoint %s model=%s", ep["name"], ep["model"])
        return _call_remote(
            chat_url, payload,
            auth_header=f"Bearer {ep['api_key']}" if ep["api_key"] else "Bearer ",
            extra_headers=ep["headers"] or None,
        )
    raise ValueError(
        "No AI provider configured. Go to Settings → Providers to add one, "
        "then Settings → Model Assignments to assign models to work buckets."
    )


def call_llm_vision(
    *,
    prompt: str,
    image_data_uri: str,
    max_tokens: int = 2000,
    temperature: float = 0.1,
    provider_override: str | None = None,
    model_override: str | None = None,
) -> str:
    """Call a vision-capable LLM with text prompt + base64-encoded image.

    Phase-28: routes through the same Settings infrastructure as call_llm,
    but uses vision-capable models (Mistral pixtral, Ollama llava).

    Resolution order (no overrides):
      1. Ollama (if enabled in provider prefs + selected model is vision-capable, e.g. llava, llava:13b, gemma3-vision)
      2. Mistral (uses pixtral-12b-2409 by default; if mistral_api_key set)

    Returns the model's reply text. Raises ValueError if no provider available.
    """
    prefs = _get_provider_prefs()
    ollama_pref = prefs.get("ollama", {})

    # Build OpenAI-style multi-content message (works for both Mistral + Ollama)
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_data_uri}},
        ],
    }]

    from glossa_lab.api.settings import get_key  # noqa: PLC0415

    # Explicit override
    if provider_override == "ollama" and model_override:
        return _call_ollama(
            model=model_override,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            json_mode=False,
        )
    if provider_override == "mistral":
        key = get_key("mistral_api_key")
        if not key:
            raise ValueError("Mistral API key not set")
        payload = {
            "model": model_override or "pixtral-12b-2409",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        return _call_remote(
            "https://api.mistral.ai/v1/chat/completions",
            payload, auth_header=f"Bearer {key}",
        )

    # Default chain
    if ollama_pref.get("enabled") and ollama_pref.get("selected_model"):
        sel = ollama_pref["selected_model"]
        if any(tag in sel.lower() for tag in ("llava", "gemma3", "vision", "mini-cpm")):
            return _call_ollama(
                model=sel,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                json_mode=False,
            )

    mistral_key = get_key("mistral_api_key")
    if mistral_key:
        payload = {
            "model": prefs.get("mistral", {}).get("vision_model", "pixtral-12b-2409"),
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        return _call_remote(
            "https://api.mistral.ai/v1/chat/completions",
            payload, auth_header=f"Bearer {mistral_key}",
        )

    raise ValueError(
        "No vision-capable AI provider configured. "
        "In Settings: enable Ollama with a vision model (llava/gemma3-vision), "
        "or set mistral_api_key."
    )


def _call_remote(
    url: str,
    payload: dict[str, Any],
    *,
    auth_header: str,
    auth_header_name: str = "Authorization",
    extra_headers: dict[str, str] | None = None,
    response_path: list[str | int] | None = None,
) -> str:
    """POST payload to a remote LLM endpoint and return the reply text."""
    body = json.dumps(payload).encode()
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        auth_header_name: auth_header,
    }
    if auth_header_name == "Authorization" and not auth_header.startswith("Bearer "):
        headers["Authorization"] = f"Bearer {auth_header}"
    if extra_headers:
        headers.update(extra_headers)
    # Longer timeout for custom/local endpoints (vLLM can be slow on large prompts)
    timeout = 120 if "/v1/chat/completions" in url and "api." not in url else 60
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
        # Navigate response path (default: OpenAI/Mistral format)
        if response_path:
            result: Any = data
            for key in response_path:
                result = result[key]
            return str(result)
        return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode(errors="replace")[:300]
        raise RuntimeError(f"LLM API error {exc.code}: {body_text}") from exc
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"LLM request failed: {exc}") from exc

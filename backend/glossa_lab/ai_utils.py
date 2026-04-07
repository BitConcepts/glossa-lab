"""Shared LLM utility for AI-powered features in Glossa Lab.

Resolution order (first matching wins):
  1. Ollama  — if enabled in Settings > Provider Enable
  2. Mistral — if mistral_api_key is set
  3. OpenAI  — if openai_api_key is set
  4. Anthropic — if anthropic_api_key is set

Uses stdlib urllib so no optional packages are required beyond the API key.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from glossa_lab.api.settings import get_key

_OLLAMA_BASE = "http://localhost:11434"


def _get_provider_prefs() -> dict[str, Any]:
    """Load saved provider preferences from the keys store."""
    from glossa_lab.api.settings import _PROVIDERS_KEY, _load_keys  # noqa: PLC0415
    return _load_keys().get(_PROVIDERS_KEY, {})


def _call_ollama(
    model: str,
    messages: list[dict[str, str]],
    max_tokens: int,
    temperature: float,
) -> str:
    """Call the local Ollama instance via its /api/chat endpoint."""
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{_OLLAMA_BASE}/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode())
        # Ollama returns {"message": {"role": "assistant", "content": "..."}}
        return data["message"]["content"]
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Ollama not reachable at {_OLLAMA_BASE}. "
            "Is 'ollama serve' running? Error: {exc}"
        ) from exc
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Ollama request failed: {exc}") from exc


def call_llm(
    messages: list[dict[str, str]],
    *,
    json_mode: bool = False,
    max_tokens: int = 2000,
    temperature: float = 0.3,
) -> str:
    """Call the configured LLM and return the assistant message text.

    Resolution order:
      1. Ollama (if enabled in provider prefs + model selected)
      2. Mistral (if mistral_api_key set)
      3. OpenAI  (if openai_api_key set)
      4. Anthropic (if anthropic_api_key set)

    Raises ValueError if no provider is available.
    Raises RuntimeError on API/network error.
    """
    prefs = _get_provider_prefs()
    ollama_pref = prefs.get("ollama", {})

    # ── 1. Ollama (local) ──────────────────────────────────────────────────────
    if ollama_pref.get("enabled") and ollama_pref.get("selected_model"):
        return _call_ollama(
            model=ollama_pref["selected_model"],
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )

    # ── 2. Mistral ─────────────────────────────────────────────────────────────
    mistral_key = get_key("mistral_api_key")
    if mistral_key:
        url = "https://api.mistral.ai/v1/chat/completions"
        payload: dict[str, Any] = {
            "model": prefs.get("mistral", {}).get("selected_model", "mistral-small-latest"),
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        return _call_remote(url, payload, auth_header=f"Bearer {mistral_key}")

    # ── 3. OpenAI ──────────────────────────────────────────────────────────────
    openai_key = get_key("openai_api_key")
    if openai_key:
        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": prefs.get("openai", {}).get("selected_model", "gpt-4o-mini"),
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        return _call_remote(url, payload, auth_header=f"Bearer {openai_key}")

    # ── 4. Anthropic ───────────────────────────────────────────────────────────
    anthropic_key = get_key("anthropic_api_key")
    if anthropic_key:
        url = "https://api.anthropic.com/v1/messages"
        # Convert messages format for Anthropic
        sys_msgs = [m for m in messages if m["role"] == "system"]
        usr_msgs = [m for m in messages if m["role"] != "system"]
        payload = {
            "model": prefs.get("anthropic", {}).get("selected_model", "claude-3-5-haiku-latest"),
            "max_tokens": max_tokens,
            "messages": usr_msgs,
        }
        if sys_msgs:
            payload["system"] = " ".join(m["content"] for m in sys_msgs)
        return _call_remote(
            url, payload,
            auth_header=anthropic_key,
            auth_header_name="x-api-key",
            extra_headers={"anthropic-version": "2023-06-01"},
            response_path=["content", 0, "text"],
        )

    raise ValueError(
        "No AI provider configured. "
        "In Settings: enable Ollama and select a model, "
        "or set mistral_api_key / openai_api_key / anthropic_api_key."
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
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
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

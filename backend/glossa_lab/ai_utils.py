"""Shared LLM utility for AI-powered features in Glossa Lab.

Tries Mistral first (preferred), falls back to OpenAI.
Uses stdlib urllib so no optional packages are required beyond the API key.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from glossa_lab.api.settings import get_key


def call_llm(
    messages: list[dict[str, str]],
    *,
    json_mode: bool = False,
    max_tokens: int = 2000,
    temperature: float = 0.3,
) -> str:
    """Call Mistral or OpenAI chat completions and return the assistant message text.

    Resolution order: mistral_api_key → openai_api_key.
    Raises ValueError if no key is configured.
    Raises RuntimeError on API/network error.
    """
    mistral_key = get_key("mistral_api_key")
    openai_key = get_key("openai_api_key")

    if mistral_key:
        url = "https://api.mistral.ai/v1/chat/completions"
        payload: dict[str, Any] = {
            "model": "mistral-small-latest",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        auth_header = f"Bearer {mistral_key}"
    elif openai_key:
        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        auth_header = f"Bearer {openai_key}"
    else:
        raise ValueError(
            "No AI API key configured. "
            "Set mistral_api_key or openai_api_key in the Settings tab first."
        )

    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": auth_header,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
        return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode(errors="replace")[:300]
        raise RuntimeError(f"LLM API error {exc.code}: {body_text}") from exc
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"LLM request failed: {exc}") from exc

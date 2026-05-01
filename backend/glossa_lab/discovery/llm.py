"""Thin multi-provider LLM chat client used by the discovery miner.

Design goals:
* No third-party deps — uses ``urllib`` for HTTP.
* Reads keys via :func:`glossa_lab.api.settings.get_key` so rotating a key in
  the UI / settings router takes effect immediately.
* Ordered provider fallback: try Mistral first (cheapest viable for short
  classification calls), fall through to OpenAI, then Google Gemini. On 401 /
  403 / 429 / 5xx the next provider is tried; other errors propagate.
* JSON-mode helper :func:`LLMClient.chat_json` always returns a parsed dict.

Providers implemented here:
* :class:`MistralProvider` (``mistral-small-latest``)
* :class:`OpenAIProvider` (``gpt-4o-mini``)
* :class:`GoogleProvider` (``gemini-2.0-flash``)
* :class:`MockProvider`   — only used by smoke tests; returns a canned dict.
"""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable

_log = logging.getLogger("glossa_lab.discovery.llm")

_USER_AGENT = "GlossaLab-DiscoveryEngine/0.1"


class LLMError(RuntimeError):
    """Raised when no provider could complete a chat call."""


@dataclass(slots=True)
class LLMResult:
    """The text + metadata returned by a successful chat call."""

    provider: str
    model: str
    text: str
    raw: dict[str, Any] = field(default_factory=dict)


# ── HTTP helper ─────────────────────────────────────────────────────────────


def _http_post_json(
    url: str,
    *,
    body: dict[str, Any],
    headers: dict[str, str] | None = None,
    timeout: float = 60.0,
) -> tuple[int, dict[str, Any]]:
    """POST a JSON body and return ``(status, parsed_json_or_empty)``.

    Raises :class:`urllib.error.HTTPError` on non-2xx so callers can branch
    on the status code (used for fallback decisions).
    """
    payload = json.dumps(body).encode("utf-8")
    hdrs = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": _USER_AGENT,
    }
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=payload, headers=hdrs, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        status = resp.status
        if not raw:
            return status, {}
        try:
            return status, json.loads(raw)
        except json.JSONDecodeError:
            return status, {"_raw": raw.decode("utf-8", errors="replace")}


def _is_fallback_status(code: int) -> bool:
    """Return True for HTTP statuses that justify trying the next provider."""
    return code in (401, 403, 408, 409, 425, 429) or 500 <= code < 600


# ── Provider contract ───────────────────────────────────────────────────────


class LLMProvider(ABC):
    """Provider-specific HTTP shim.

    Each provider knows how to format its own request/response and the API key
    name in :data:`KNOWN_KEYS`.
    """

    name: str = ""
    key_name: str = ""
    default_model: str = ""

    def __init__(self, model: str | None = None) -> None:
        if not self.name:
            raise TypeError(f"{type(self).__name__}.name must be set")
        self.model = model or self.default_model

    def is_configured(self) -> bool:
        # Local import keeps provider modules importable in test contexts.
        from glossa_lab.api.settings import get_key

        return bool(self.key_name) and bool(get_key(self.key_name))

    @abstractmethod
    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        json_mode: bool,
        max_tokens: int,
        temperature: float,
    ) -> LLMResult:
        """Execute one chat call; raise :class:`LLMError` on hard failure.

        On a fallback-worthy HTTP status (401/403/429/5xx) the provider should
        raise :class:`urllib.error.HTTPError` so :class:`LLMClient` can move on.
        """


# ── Concrete providers ──────────────────────────────────────────────────────


class MistralProvider(LLMProvider):
    name = "mistral"
    key_name = "mistral_api_key"
    default_model = "mistral-small-latest"

    def chat(self, messages, *, json_mode, max_tokens, temperature):
        from glossa_lab.api.settings import get_key

        key = get_key(self.key_name)
        if not key:
            raise LLMError("Mistral key not configured")
        body: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        status, data = _http_post_json(
            "https://api.mistral.ai/v1/chat/completions",
            body=body,
            headers={"Authorization": f"Bearer {key}"},
        )
        choices = (data or {}).get("choices") or []
        text = ""
        if choices:
            text = (choices[0].get("message") or {}).get("content") or ""
        return LLMResult(provider=self.name, model=self.model, text=text, raw=data)


class OpenAIProvider(LLMProvider):
    name = "openai"
    key_name = "openai_api_key"
    default_model = "gpt-4o-mini"

    def chat(self, messages, *, json_mode, max_tokens, temperature):
        from glossa_lab.api.settings import get_key

        key = get_key(self.key_name)
        if not key:
            raise LLMError("OpenAI key not configured")
        body: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        status, data = _http_post_json(
            "https://api.openai.com/v1/chat/completions",
            body=body,
            headers={"Authorization": f"Bearer {key}"},
        )
        choices = (data or {}).get("choices") or []
        text = ""
        if choices:
            text = (choices[0].get("message") or {}).get("content") or ""
        return LLMResult(provider=self.name, model=self.model, text=text, raw=data)


class GoogleProvider(LLMProvider):
    name = "google"
    key_name = "google_api_key"
    default_model = "gemini-2.0-flash"

    def chat(self, messages, *, json_mode, max_tokens, temperature):
        from glossa_lab.api.settings import get_key

        key = get_key(self.key_name)
        if not key:
            raise LLMError("Google key not configured")
        # Gemini collapses the chat into a single ``contents`` array; we keep
        # the system message as the first turn for simplicity.
        contents = [
            {"role": ("user" if m.get("role") != "model" else "model"),
             "parts": [{"text": m.get("content", "")}]}
            for m in messages
            if m.get("role") in ("system", "user", "assistant", "model")
        ]
        body: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature,
            },
        }
        if json_mode:
            body["generationConfig"]["responseMimeType"] = "application/json"
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{urllib.parse.quote(self.model)}:generateContent?key={key}"
        )
        status, data = _http_post_json(url, body=body)
        text = ""
        candidates = (data or {}).get("candidates") or []
        if candidates:
            parts = (candidates[0].get("content") or {}).get("parts") or []
            text = "".join(p.get("text", "") for p in parts)
        return LLMResult(provider=self.name, model=self.model, text=text, raw=data)


class MockProvider(LLMProvider):
    """Test-only provider: returns whatever ``producer`` yields."""

    name = "mock"
    key_name = ""  # always considered configured
    default_model = "mock-1"

    def __init__(self, producer: Callable[[list[dict[str, str]]], str]) -> None:
        super().__init__(model=self.default_model)
        self._producer = producer

    def is_configured(self) -> bool:  # noqa: D401
        return True

    def chat(self, messages, *, json_mode, max_tokens, temperature):
        text = self._producer(messages)
        return LLMResult(provider=self.name, model=self.model, text=text, raw={})


# ── Client with fallback ────────────────────────────────────────────────────


def _default_providers() -> list[LLMProvider]:
    return [MistralProvider(), OpenAIProvider(), GoogleProvider()]


class LLMClient:
    """Try a list of providers in order; first configured one that returns
    successfully wins. Providers raising ``HTTPError`` with a fallback status
    move the client to the next provider.
    """

    def __init__(self, providers: list[LLMProvider] | None = None) -> None:
        self._providers = providers or _default_providers()

    def configured_providers(self) -> list[str]:
        return [p.name for p in self._providers if p.is_configured()]

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        json_mode: bool = False,
        max_tokens: int = 600,
        temperature: float = 0.0,
    ) -> LLMResult:
        last_err: Exception | None = None
        for p in self._providers:
            if not p.is_configured():
                continue
            try:
                return p.chat(
                    messages,
                    json_mode=json_mode,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
            except urllib.error.HTTPError as exc:  # provider responded with non-2xx
                if _is_fallback_status(exc.code):
                    _log.info("provider %s returned %s, falling through", p.name, exc.code)
                    last_err = exc
                    continue
                raise LLMError(
                    f"{p.name} HTTP {exc.code}: {exc.reason}"
                ) from exc
            except urllib.error.URLError as exc:  # network unreachable
                _log.info("provider %s URLError: %s, falling through", p.name, exc.reason)
                last_err = exc
                continue
            except LLMError:
                raise
            except Exception as exc:  # noqa: BLE001
                _log.warning("provider %s raised %s: %s", p.name, type(exc).__name__, exc)
                last_err = exc
                continue
        raise LLMError(
            f"No LLM provider succeeded. Last error: {last_err!r}. "
            f"Configured providers: {self.configured_providers()}"
        )

    def chat_json(
        self,
        messages: list[dict[str, str]],
        *,
        max_tokens: int = 600,
        temperature: float = 0.0,
    ) -> tuple[dict[str, Any], LLMResult]:
        """Like :meth:`chat` but returns ``(parsed_json, result)``.

        If the model returns surrounding prose, the helper extracts the first
        balanced JSON object it can find. Raises :class:`LLMError` if parsing
        fails entirely.
        """
        result = self.chat(
            messages, json_mode=True, max_tokens=max_tokens, temperature=temperature,
        )
        text = (result.text or "").strip()
        try:
            return json.loads(text), result
        except json.JSONDecodeError:
            pass
        # Fallback: scan for the first {...} block.
        start = text.find("{")
        end = text.rfind("}")
        if 0 <= start < end:
            try:
                return json.loads(text[start : end + 1]), result
            except json.JSONDecodeError as exc:
                raise LLMError(
                    f"Could not parse JSON from {result.provider}: {exc}"
                ) from exc
        raise LLMError(
            f"Empty / non-JSON response from {result.provider}: {text[:200]!r}"
        )


__all__ = [
    "LLMClient",
    "LLMError",
    "LLMProvider",
    "LLMResult",
    "MistralProvider",
    "OpenAIProvider",
    "GoogleProvider",
    "MockProvider",
]

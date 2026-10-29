"""Circuit-breaker tests for the discovery LLM client.

2026-10-29 UI-log audit: a rate-limited provider (Mistral, HTTP
429) was re-hit on every classified item in a scheduler tick,
flooding the log with "falling through" lines. The client now
mirrors the ai_utils circuit: after a threshold of consecutive
failures the provider is skipped for a cooldown.
"""

from __future__ import annotations

import urllib.error

import pytest

from glossa_lab.discovery import llm as llm_mod
from glossa_lab.discovery.llm import LLMClient, LLMError, LLMResult


class _FakeProvider:
    def __init__(self, name: str, *, fail: bool = True) -> None:
        self.name = name
        self.fail = fail
        self.calls = 0

    def is_configured(self) -> bool:
        return True

    def chat(self, messages, *, json_mode, max_tokens, temperature):  # noqa: ARG002
        self.calls += 1
        if self.fail:
            raise urllib.error.HTTPError(
                "https://example.invalid", 429, "Too Many Requests", {}, None
            )
        return LLMResult(provider=self.name, model="fake", text="ok")


@pytest.fixture(autouse=True)
def _clean_circuit():
    llm_mod._provider_fail_counts.clear()
    llm_mod._provider_cooldown_until.clear()
    yield
    llm_mod._provider_fail_counts.clear()
    llm_mod._provider_cooldown_until.clear()


def test_circuit_opens_after_threshold_and_stops_hitting_provider():
    provider = _FakeProvider("mistral")
    client = LLMClient(providers=[provider])
    for _ in range(llm_mod._CIRCUIT_THRESHOLD):
        with pytest.raises(LLMError):
            client.chat([{"role": "user", "content": "hi"}])
    assert provider.calls == llm_mod._CIRCUIT_THRESHOLD
    # Circuit open: the provider is not invoked again.
    with pytest.raises(LLMError, match="circuit open"):
        client.chat([{"role": "user", "content": "hi"}])
    assert provider.calls == llm_mod._CIRCUIT_THRESHOLD


def test_healthy_fallback_still_serves_while_first_provider_cools_down():
    dead = _FakeProvider("mistral")
    healthy = _FakeProvider("openai", fail=False)
    client = LLMClient(providers=[dead, healthy])
    for _ in range(llm_mod._CIRCUIT_THRESHOLD + 3):
        result = client.chat([{"role": "user", "content": "hi"}])
        assert result.text == "ok"
    # The dead provider was hit only until its circuit opened.
    assert dead.calls == llm_mod._CIRCUIT_THRESHOLD
    assert healthy.calls == llm_mod._CIRCUIT_THRESHOLD + 3


def test_success_resets_the_failure_count():
    provider = _FakeProvider("mistral")
    client = LLMClient(providers=[provider])
    for _ in range(llm_mod._CIRCUIT_THRESHOLD - 1):
        with pytest.raises(LLMError):
            client.chat([{"role": "user", "content": "hi"}])
    provider.fail = False
    assert client.chat([{"role": "user", "content": "hi"}]).text == "ok"
    # Counter reset by the success: another threshold-minus-one run
    # of failures must NOT open the circuit.
    provider.fail = True
    for _ in range(llm_mod._CIRCUIT_THRESHOLD - 1):
        with pytest.raises(LLMError):
            client.chat([{"role": "user", "content": "hi"}])
    assert provider.calls == 2 * llm_mod._CIRCUIT_THRESHOLD - 1


def test_cooldown_expiry_allows_a_retry():
    provider = _FakeProvider("mistral")
    client = LLMClient(providers=[provider])
    for _ in range(llm_mod._CIRCUIT_THRESHOLD):
        with pytest.raises(LLMError):
            client.chat([{"role": "user", "content": "hi"}])
    assert provider.calls == llm_mod._CIRCUIT_THRESHOLD
    # Expire the cooldown: the provider is tried again.
    llm_mod._provider_cooldown_until["mistral"] = 0.0
    with pytest.raises(LLMError):
        client.chat([{"role": "user", "content": "hi"}])
    assert provider.calls == llm_mod._CIRCUIT_THRESHOLD + 1

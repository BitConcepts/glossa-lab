"""Shared rate-limit pacing for AI model requests."""

from __future__ import annotations

import math
import random
import re
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any

WINDOW_SECONDS = 60.0
DEFAULT_UTILIZATION_TARGET = 0.70
DEFAULT_IMAGE_TOKEN_ESTIMATE = 4096


@dataclass(slots=True)
class ModelLimit:
    """Per-model RPM/TPM policy."""

    rpm_limit: int
    tpm_limit: int
    utilization_target: float = DEFAULT_UTILIZATION_TARGET
    max_concurrency: int = 4
    min_concurrency: int = 1
    image_token_estimate: int = DEFAULT_IMAGE_TOKEN_ESTIMATE


@dataclass(slots=True)
class _DispatchRecord:
    timestamp: float
    reserved_tokens: int


@dataclass(slots=True)
class _ModelState:
    records: deque[_DispatchRecord] = field(default_factory=deque)
    in_flight: int = 0
    dynamic_concurrency: int = 1
    rpm_ema: float = 0.0
    tpm_ema: float = 0.0
    reduced_until: float = 0.0


class AIModelPacer:
    """Thread-safe model pacer with pre-dispatch budget checks and 429 recovery."""

    def __init__(self, limits: dict[str, ModelLimit]) -> None:
        self._limits = limits
        self._states = {
            model: _ModelState(dynamic_concurrency=limit.max_concurrency)
            for model, limit in limits.items()
        }
        self._condition = threading.Condition()

    def require_model(self, model: str) -> ModelLimit:
        if model not in self._limits:
            raise KeyError(
                f"No pacing limits configured for model '{model}'. "
                "Configure RPM and TPM limits before dispatching requests."
            )
        return self._limits[model]

    def estimate_request_tokens(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]] | None = None,
        prompt: str | None = None,
        max_output_tokens: int = 0,
        image_count: int = 0,
    ) -> int:
        limit = self.require_model(model)
        estimate = 0
        if prompt:
            estimate += self._estimate_text_tokens(prompt)
        if messages:
            estimate += self._estimate_messages_tokens(messages, limit.image_token_estimate)
        estimate += image_count * limit.image_token_estimate
        return estimate + max_output_tokens

    def acquire(self, model: str, reserved_tokens: int) -> None:
        limit = self.require_model(model)
        if reserved_tokens > limit.tpm_limit:
            raise ValueError(
                f"Reserved tokens {reserved_tokens} exceed configured TPM limit {limit.tpm_limit} "
                f"for model '{model}'."
            )
        with self._condition:
            while True:
                now = time.time()
                state = self._states[model]
                self._prune_old_records(state, now)
                self._restore_concurrency_if_due(state, limit, now)

                rpm_budget = max(1, int(limit.rpm_limit * limit.utilization_target))
                tpm_budget = min(
                    limit.tpm_limit,
                    max(1, max(int(limit.tpm_limit * limit.utilization_target), reserved_tokens)),
                )
                rpm_used = len(state.records)
                tpm_used = sum(record.reserved_tokens for record in state.records)

                if (
                    state.in_flight < state.dynamic_concurrency
                    and rpm_used + 1 <= rpm_budget
                    and tpm_used + reserved_tokens <= tpm_budget
                ):
                    state.in_flight += 1
                    state.records.append(
                        _DispatchRecord(timestamp=now, reserved_tokens=reserved_tokens)
                    )
                    self._refresh_moving_average(
                        state=state,
                        limit=limit,
                        rpm_used=rpm_used + 1,
                        tpm_used=tpm_used + reserved_tokens,
                    )
                    return

                self._condition.wait(
                    timeout=self._seconds_until_budget(
                        now=now,
                        state=state,
                        limit=limit,
                        reserved_tokens=reserved_tokens,
                    )
                )

    def release(self, model: str) -> None:
        if model not in self._states:
            return
        with self._condition:
            state = self._states[model]
            if state.in_flight > 0:
                state.in_flight -= 1
            self._condition.notify_all()

    def on_rate_limit(self, model: str, error: Exception, attempt: int) -> float:
        limit = self.require_model(model)
        with self._condition:
            now = time.time()
            state = self._states[model]
            state.dynamic_concurrency = max(limit.min_concurrency, state.dynamic_concurrency - 1)
            state.reduced_until = now + 120.0
            retry_after = self.parse_retry_after_seconds(str(error))
            base = retry_after if retry_after is not None else min(30.0, 2**attempt)
            jitter = random.uniform(0.0, max(0.25, base * 0.25))
            delay = base + jitter
            self._condition.notify_all()
            return delay

    def snapshot(self, model: str) -> dict[str, Any]:
        limit = self.require_model(model)
        with self._condition:
            state = self._states[model]
            now = time.time()
            self._prune_old_records(state, now)
            rpm_used = len(state.records)
            tpm_used = sum(record.reserved_tokens for record in state.records)
            return {
                "model": model,
                "rpm_limit": limit.rpm_limit,
                "tpm_limit": limit.tpm_limit,
                "rpm_used": rpm_used,
                "tpm_used": tpm_used,
                "rpm_utilization": rpm_used / max(limit.rpm_limit, 1),
                "tpm_utilization": tpm_used / max(limit.tpm_limit, 1),
                "rpm_ema": state.rpm_ema,
                "tpm_ema": state.tpm_ema,
                "dynamic_concurrency": state.dynamic_concurrency,
                "in_flight": state.in_flight,
            }

    @staticmethod
    def is_rate_limit_error(error: Exception) -> bool:
        message = str(error).lower()
        return (
            "rate limit" in message
            or "rate_limit_exceeded" in message
            or "429" in message
            or "too many requests" in message
        )

    @staticmethod
    def parse_retry_after_seconds(message: str) -> float | None:
        match = re.search(
            r"try again in ([0-9]+(?:\.[0-9]+)?)s",
            message,
            flags=re.IGNORECASE,
        )
        if match:
            return float(match.group(1))
        return None

    @staticmethod
    def _estimate_text_tokens(text: str) -> int:
        return max(1, math.ceil(len(text) / 4))

    def _estimate_messages_tokens(
        self,
        messages: list[dict[str, Any]],
        image_token_estimate: int,
    ) -> int:
        total = 0
        for message in messages:
            total += 8
            content = message.get("content", "")
            if isinstance(content, str):
                total += self._estimate_text_tokens(content)
                continue
            if isinstance(content, list):
                for item in content:
                    if not isinstance(item, dict):
                        total += self._estimate_text_tokens(str(item))
                        continue
                    item_type = item.get("type")
                    if item_type == "text":
                        total += self._estimate_text_tokens(str(item.get("text", "")))
                    elif item_type in {"image_url", "input_image"}:
                        total += image_token_estimate
                    else:
                        total += self._estimate_text_tokens(str(item))
        return total

    @staticmethod
    def _prune_old_records(state: _ModelState, now: float) -> None:
        while state.records and now - state.records[0].timestamp >= WINDOW_SECONDS:
            state.records.popleft()

    @staticmethod
    def _restore_concurrency_if_due(
        state: _ModelState,
        limit: ModelLimit,
        now: float,
    ) -> None:
        if state.dynamic_concurrency < limit.max_concurrency and now >= state.reduced_until:
            state.dynamic_concurrency += 1
            if state.dynamic_concurrency < limit.max_concurrency:
                state.reduced_until = now + 60.0

    def _seconds_until_budget(
        self,
        *,
        now: float,
        state: _ModelState,
        limit: ModelLimit,
        reserved_tokens: int,
    ) -> float:
        wait_candidates: list[float] = []
        rpm_budget = max(1, int(limit.rpm_limit * limit.utilization_target))
        tpm_budget = min(
            limit.tpm_limit,
            max(1, max(int(limit.tpm_limit * limit.utilization_target), reserved_tokens)),
        )

        if state.in_flight >= state.dynamic_concurrency:
            wait_candidates.append(0.25)

        if len(state.records) + 1 > rpm_budget and state.records:
            wait_candidates.append(max(0.05, WINDOW_SECONDS - (now - state.records[0].timestamp)))

        running_tokens = 0
        for record in state.records:
            running_tokens += record.reserved_tokens
            if running_tokens + reserved_tokens > tpm_budget:
                wait_candidates.append(max(0.05, WINDOW_SECONDS - (now - record.timestamp)))
                break

        return max(wait_candidates) if wait_candidates else 0.05

    @staticmethod
    def _refresh_moving_average(
        *,
        state: _ModelState,
        limit: ModelLimit,
        rpm_used: int,
        tpm_used: int,
    ) -> None:
        alpha = 0.25
        rpm_util = rpm_used / max(limit.rpm_limit, 1)
        tpm_util = tpm_used / max(limit.tpm_limit, 1)
        state.rpm_ema = (
            rpm_util if state.rpm_ema == 0 else alpha * rpm_util + (1 - alpha) * state.rpm_ema
        )
        state.tpm_ema = (
            tpm_util if state.tpm_ema == 0 else alpha * tpm_util + (1 - alpha) * state.tpm_ema
        )

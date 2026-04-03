"""Tests for AI request pacing."""

from glossa_lab.ai_pacing import AIModelPacer, ModelLimit


def test_estimate_request_tokens_counts_text_images_and_output():
    pacer = AIModelPacer({"demo": ModelLimit(rpm_limit=10, tpm_limit=1000)})
    estimate = pacer.estimate_request_tokens(
        model="demo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "abcdefghij"},
                    {"type": "image_url", "image_url": {"url": "data:image/jp2;base64,abc"}},
                ],
            }
        ],
        max_output_tokens=100,
    )
    assert estimate >= 4200


def test_parse_retry_after_seconds_matches_openai_error_format():
    message = (
        "Rate limit reached for gpt-5.4 in organization org on tokens per min (TPM): "
        "Limit 500000, Used 341693, Requested 248254. Please try again in 10.793s."
    )
    assert AIModelPacer.parse_retry_after_seconds(message) == 10.793


def test_rate_limit_error_detection_matches_common_provider_messages():
    assert AIModelPacer.is_rate_limit_error(Exception("429 rate_limit_exceeded"))
    assert AIModelPacer.is_rate_limit_error(Exception("Rate limit reached for gpt-5.4"))
    assert not AIModelPacer.is_rate_limit_error(Exception("socket timeout"))


def test_snapshot_reports_current_utilization():
    pacer = AIModelPacer({"demo": ModelLimit(rpm_limit=10, tpm_limit=1000)})
    pacer.acquire("demo", 120)
    try:
        snapshot = pacer.snapshot("demo")
        assert snapshot["rpm_used"] == 1
        assert snapshot["tpm_used"] == 120
        assert snapshot["dynamic_concurrency"] >= 1
    finally:
        pacer.release("demo")

"""Spec 082 (T012/T013) — healthcheck token legs + proof kit.

The healthcheck module is loaded from its file path (the same way
tests/test_supervision_installer.py loads it). Its HTTP layer is
stubbed, so the legs under test are the token behavior: resolution
order, the token presented on /docs + /openapi.json only (health
stays bare), and the NAMED failures — an unresolvable token
against an authed backend lists every source tried, and a refused
token is reported as stale rather than as downtime.

The proof-kit test is the end-to-end leg: a real uvicorn instance
of the enforcing backend (subprocess, bounded startup wait,
guaranteed teardown), the kit passing against it with the install
token and failing with a wrong one.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
HEALTHCHECK = REPO / "services" / "linux" / "healthcheck.py"
PROOF_KIT = REPO / "tools" / "auth-proof" / "check_auth.py"
TOKEN = "consumer-test-token-082"


def _load_healthcheck():
    spec = importlib.util.spec_from_file_location("glossa_healthcheck_082", HEALTHCHECK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def hc(monkeypatch, tmp_path):
    mod = _load_healthcheck()
    monkeypatch.delenv("GLOSSA_API_TOKEN", raising=False)
    monkeypatch.delenv("GLOSSA_TOKEN_FILE", raising=False)
    monkeypatch.delenv("GLOSSA_DATA_DIR", raising=False)
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "xdg-empty"))
    return mod


# ── Token resolution ──────────────────────────────────────


def test_resolve_token_prefers_env(hc, monkeypatch):
    monkeypatch.setenv("GLOSSA_API_TOKEN", TOKEN)
    token, _tried = hc.resolve_token()
    assert token == TOKEN


def test_resolve_token_reads_token_file_env(hc, monkeypatch, tmp_path):
    named = tmp_path / "api_token"
    named.write_text(TOKEN + "\n", encoding="utf-8")
    monkeypatch.setenv("GLOSSA_TOKEN_FILE", str(named))
    token, _tried = hc.resolve_token()
    assert token == TOKEN


def test_resolve_token_reports_what_was_tried(hc):
    token, tried = hc.resolve_token()
    # No token exists in this controlled environment... unless the
    # checkout carries a dev token file, which is also a resolution.
    if token is None:
        joined = "; ".join(tried)
        assert "GLOSSA_API_TOKEN" in joined
        assert "GLOSSA_TOKEN_FILE" in joined or "installed data dir" in joined


# ── check_once token legs ─────────────────────────────────

GOOD_OPENAPI = {"info": {"title": "Glossa Lab", "version": "9.9"}}


def _stub_http(hc, monkeypatch, *, health, docs_status=200, openapi=None):
    calls: list[tuple[str, dict | None]] = []

    def fake_fetch(url, timeout, headers=None):
        calls.append((url, headers))
        return docs_status, b""

    def fake_fetch_json(url, timeout, headers=None):
        calls.append((url, headers))
        if url.endswith("/api/v1/health"):
            return 200, health
        return 200, openapi if openapi is not None else {}

    monkeypatch.setattr(hc, "fetch", fake_fetch)
    monkeypatch.setattr(hc, "fetch_json", fake_fetch_json)
    return calls


def test_check_once_presents_token_on_schema_legs_only(hc, monkeypatch):
    monkeypatch.setenv("GLOSSA_API_TOKEN", TOKEN)
    health = {"status": "healthy", "version": "9.9", "auth": "token"}
    calls = _stub_http(hc, monkeypatch, health=health, openapi=GOOD_OPENAPI)
    ok, result = hc.check_once("http://127.0.0.1:8001", 1.0)
    assert ok, result["errors"]
    assert result["token_resolved"] is True
    by_url = dict(calls)
    assert by_url["http://127.0.0.1:8001/docs"] == {
        "Authorization": f"Bearer {TOKEN}"
    }
    assert by_url["http://127.0.0.1:8001/openapi.json"] == {
        "Authorization": f"Bearer {TOKEN}"
    }
    # Health is an open route: the token is never sent to it.
    assert by_url["http://127.0.0.1:8001/api/v1/health"] is None


def test_check_once_names_an_unresolvable_token(hc, monkeypatch):
    # Guarantee no candidate resolves: empty XDG (fixture), no env,
    # and the repo-data candidate pointed at an empty tree is not
    # possible from here — so also require that IF a token did
    # resolve the test says so instead of passing vacuously.
    token, _ = hc.resolve_token()
    if token is not None:
        pytest.skip("a token resolves in this environment; leg not applicable")
    health = {"status": "healthy", "version": "9.9", "auth": "token"}
    _stub_http(hc, monkeypatch, health=health, docs_status=401)
    ok, result = hc.check_once("http://127.0.0.1:8001", 1.0)
    assert not ok
    joined = "\n".join(result["errors"])
    assert "no token could be resolved" in joined
    assert "tried:" in joined and "GLOSSA_API_TOKEN" in joined


def test_check_once_reports_a_refused_token_as_stale(hc, monkeypatch):
    monkeypatch.setenv("GLOSSA_API_TOKEN", TOKEN)
    health = {"status": "healthy", "version": "9.9", "auth": "token"}
    _stub_http(hc, monkeypatch, health=health, docs_status=401)
    ok, result = hc.check_once("http://127.0.0.1:8001", 1.0)
    assert not ok
    assert any("was refused" in e for e in result["errors"])


def test_check_once_passes_an_auth_disabled_backend_without_a_token(
    hc, monkeypatch
):
    token, _ = hc.resolve_token()
    if token is not None:
        pytest.skip("a token resolves in this environment; leg not applicable")
    health = {"status": "healthy", "version": "9.9", "auth": "disabled"}
    _stub_http(hc, monkeypatch, health=health, openapi=GOOD_OPENAPI)
    ok, result = hc.check_once("http://127.0.0.1:8001", 1.0)
    assert ok, result["errors"]
    assert result["token_resolved"] is False


# ── Proof kit, end to end ─────────────────────────────────


def test_auth_proof_kit_end_to_end(tmp_path):
    if importlib.util.find_spec("uvicorn") is None:
        pytest.skip("uvicorn is not installed in this environment")
    port = 18099
    base = f"http://127.0.0.1:{port}"
    env = dict(os.environ)
    env.update(
        {
            "GLOSSA_API_TOKEN": TOKEN,
            "GLOSSA_DATA_DIR": str(tmp_path),
            "GLOSSA_DEV_MODE": "1",
            "PYTHONPATH": str(REPO / "backend"),
        }
    )
    env.pop("GLOSSA_API_AUTH", None)
    proc = subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn", "glossa_lab.main:create_app",
            "--factory", "--host", "127.0.0.1", "--port", str(port),
        ],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        deadline = time.monotonic() + 30
        up = False
        while time.monotonic() < deadline:
            try:
                with urllib.request.urlopen(
                    f"{base}/api/v1/health", timeout=2
                ) as response:
                    if response.status == 200:
                        up = True
                        break
            except Exception:  # noqa: BLE001 — still starting; bounded loop
                time.sleep(0.5)
        assert up, "the test backend did not answer health within 30 s"

        run = subprocess.run(
            [sys.executable, str(PROOF_KIT), "--base-url", base, "--token", TOKEN],
            capture_output=True, text=True, timeout=60,
        )
        assert run.returncode == 0, run.stdout + run.stderr
        assert "AUTH_PROOF_RESULT PASS" in run.stdout
        assert TOKEN not in run.stdout  # the kit never prints the value

        bad = subprocess.run(
            [sys.executable, str(PROOF_KIT), "--base-url", base, "--token", "nope"],
            capture_output=True, text=True, timeout=60,
        )
        assert bad.returncode == 1
        assert "AUTH_PROOF_RESULT FAIL" in bad.stdout
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=10)

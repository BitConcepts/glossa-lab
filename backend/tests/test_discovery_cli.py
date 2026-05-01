"""Smoke tests for the Phase-F discovery CLI entrypoint.

These exercise ``python -m glossa_lab.discovery <subcmd>`` end-to-end via
``subprocess`` so the argparse wiring, the asyncio runner, the database
init / close, and the topic-profile loader are all covered. To keep these
tests hermetic and avoid stomping on the developer's real database,
``GLOSSA_MODE=dev`` is set so ``data_dir`` resolves to ``./data`` (which is
ignored by .gitignore).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

# Repo root is two levels above this file (backend/tests/test_discovery_cli.py).
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_BACKEND_DIR = _REPO_ROOT / "backend"


def _run_cli(*args: str, timeout: float = 30.0) -> subprocess.CompletedProcess[str]:
    """Invoke ``python -m glossa_lab.discovery <args>`` from the backend dir."""
    env = os.environ.copy()
    # Ensure the entrypoint's data_dir resolves to a project-local path so
    # tests don't write to the user's installed-mode data dir.
    env["GLOSSA_MODE"] = "dev"
    # Disable the daily scheduler env flag — the CLI doesn't use it but
    # leaving it enabled would cause confusion if a developer was debugging.
    env.pop("GLOSSA_DISCOVERY_DAILY", None)
    return subprocess.run(
        [sys.executable, "-m", "glossa_lab.discovery", *args],
        cwd=str(_BACKEND_DIR),
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def test_cli_topics_subcommand_lists_seed_profiles():
    """``python -m glossa_lab.discovery topics`` lists the three seed topics."""
    result = _run_cli("topics")
    assert result.returncode == 0, (
        f"topics subcommand failed:\nstdout={result.stdout}\nstderr={result.stderr}"
    )
    out = result.stdout
    assert "indus_script" in out
    assert "dravidian_linguistics" in out
    assert "ivc_archaeology" in out


def test_cli_sources_subcommand_lists_registered_fetchers():
    """``python -m glossa_lab.discovery sources`` lists every registered fetcher."""
    result = _run_cli("sources")
    assert result.returncode == 0, (
        f"sources subcommand failed:\nstdout={result.stdout}\nstderr={result.stderr}"
    )
    out = result.stdout
    for src in ("newsapi", "brave", "serpapi", "openalex", "arxiv", "crossref"):
        assert src in out, f"expected source '{src}' missing from CLI output"
    # Every line either says OK or OFF, depending on whether the host has
    # the provider key set; we don't pin which.
    assert "[OK ]" in out or "[OFF]" in out


def test_cli_status_subcommand_runs_clean():
    """``python -m glossa_lab.discovery status`` exits 0 even on an empty DB."""
    result = _run_cli("status")
    assert result.returncode == 0, (
        f"status subcommand failed:\nstdout={result.stdout}\nstderr={result.stderr}"
    )
    # On an empty DB, the command may print nothing (no groups had counts);
    # what matters is a clean exit.


def test_cli_help_lists_all_subcommands():
    """``python -m glossa_lab.discovery --help`` mentions every subcommand."""
    result = _run_cli("--help")
    assert result.returncode == 0
    out = result.stdout + result.stderr  # argparse may print to either
    for sub in ("topics", "sources", "status", "fetch", "mine", "daily"):
        assert sub in out, f"subcommand '{sub}' missing from --help"


def test_cli_mine_without_llm_key_exits_nonzero(monkeypatch):
    """``mine`` exits with code 2 + a clear stderr message when no LLM key is set.

    Skipped if the developer has any LLM key configured locally — in that case
    the mine command would actually try to run.
    """
    if any(os.environ.get(k) for k in ("MISTRAL_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY")):
        pytest.skip("LLM provider configured in env — `mine` would actually run")

    # Build an env that is *guaranteed* to have no provider keys so the
    # subprocess sees the same emptiness even if the parent process is
    # picking them up from .env later.
    env = os.environ.copy()
    env["GLOSSA_MODE"] = "dev"
    for k in ("MISTRAL_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY"):
        env.pop(k, None)

    proc = subprocess.run(
        [sys.executable, "-m", "glossa_lab.discovery", "mine", "--limit", "1"],
        cwd=str(_BACKEND_DIR),
        env=env,
        capture_output=True,
        text=True,
        timeout=30.0,
        check=False,
    )
    assert proc.returncode == 2, (
        f"expected exit 2 from mine without LLM key, got {proc.returncode}.\n"
        f"stdout={proc.stdout}\nstderr={proc.stderr}"
    )
    assert "no LLM provider configured" in proc.stderr.lower() or \
           "no llm provider configured" in proc.stderr.lower()

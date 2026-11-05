"""Spec 089 Stage 5 (T501) — the legacy index completion.

The builder (`tools/ledger/build_legacy_index.py`)
enumerates every run record that has ever stood in the
settling store from the store's git history and appends
the legacy entry acts the index lacks: standing records
from their standing bytes, superseded records from
their final blobs (naming the superseding commit, the
git blob id, and the blob's SHA-256), and the
`re_derivations` entries of settling-canonical.json as
legacy run events. These teeth run the CLI itself
against a tmp git repo with two seeded generations, so
the enumeration is proven against git's own record —
the independent path — not against the builder's say-so.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from glossa_lab import run_records as rr

ROOT = Path(__file__).resolve().parents[2]
BUILDER_CLI = ROOT / "tools" / "ledger" / "build_legacy_index.py"
STORE_REL = "glossa-indus/ledger/runs"


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        [
            "git",
            "-c",
            "user.email=teeth@example.invalid",
            "-c",
            "user.name=teeth",
            *args,
        ],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    return proc.stdout.strip()


def _record(candidate: str, ledger_pin: str) -> dict:
    return {
        "artifact": "settling run record",
        "semantics": "glossa-settle-1",
        "candidate": candidate,
        "scenario": f"t405-{candidate}-over-full-frame",
        "pins": {"ledger": {"sha256": ledger_pin}},
        "result": {"assignments": []},
    }


def _write(repo: Path, rel: str, payload: dict) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )


def _two_generation_repo(tmp_path: Path) -> tuple[Path, str, dict]:
    """A tmp git repo: generation A of the T405 pair
    committed, then a refresh commit replacing it with
    generation B; settling-canonical.json carries two
    re_derivations entries. Returns (repo, refresh
    commit, {A filename: committed bytes})."""
    repo = tmp_path / "repo"
    (repo / STORE_REL).mkdir(parents=True)
    _git(repo, "init", "-q")
    gen_a = {
        "t405-incumbent-over-full-frame--aaaaaaaaaaaa.json": _record(
            "incumbent", "a" * 64
        ),
        "t405-full-register-over-full-frame--bbbbbbbbbbbb.json": _record(
            "full-register", "a" * 64
        ),
    }
    for name, payload in gen_a.items():
        _write(repo, f"{STORE_REL}/{name}", payload)
    _write(
        repo,
        "glossa-indus/ledger/settling-canonical.json",
        {
            "artifact": "settling canonicals",
            "re_derivations": [
                {"date": "2026-11-02", "act": "Spec 087 adoption"},
                {"date": "2026-11-04", "act": "Spec 088 adoption"},
            ],
        },
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "generation A")
    a_bytes = {
        name: (repo / STORE_REL / name).read_bytes() for name in gen_a
    }
    for name in gen_a:
        (repo / STORE_REL / name).unlink()
    gen_b = {
        "t405-incumbent-over-full-frame--cccccccccccc.json": _record(
            "incumbent", "b" * 64
        ),
        "t405-full-register-over-full-frame--dddddddddddd.json": _record(
            "full-register", "b" * 64
        ),
    }
    for name, payload in gen_b.items():
        _write(repo, f"{STORE_REL}/{name}", payload)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "generation B (refresh)")
    refresh_commit = _git(repo, "rev-parse", "HEAD")
    return repo, refresh_commit, a_bytes


def _run_builder(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(BUILDER_CLI), "--root", str(repo)],
        capture_output=True,
        text=True,
    )


def test_builder_completes_the_index_over_two_generations(tmp_path):
    repo, refresh_commit, a_bytes = _two_generation_repo(tmp_path)
    proc = _run_builder(repo)
    assert proc.returncode == 0, proc.stderr
    assert "6 act(s) appended" in proc.stdout
    state = rr.fold_index(repo / STORE_REL / "run-index.jsonl")
    # 2 standing (generation B) + 2 superseded (generation
    # A) + 2 canonical re-derivation events.
    assert state.census == 6
    for name, committed in a_bytes.items():
        run_id = rr.legacy_run_id(name)
        entry = state.entries[run_id]
        assert entry["legacy"] is True
        assert entry["label"] == rr.LEGACY_LABEL
        assert entry["superseded_by_commit"] == refresh_commit
        assert entry["blob_sha256"] == hashlib.sha256(committed).hexdigest()
        assert entry["git_blob"]
        # The recovered key components come from the
        # record itself (its pins block verbatim).
        assert entry["key"]["input_pins"] == {"ledger": {"sha256": "a" * 64}}
    for idx in (0, 1):
        event = state.entries[
            f"legacy:settling-canonical/re_derivations[{idx}]"
        ]
        assert event["record"] == "settling-canonical.json"
        assert event["key"]["act"] in (
            "Spec 087 adoption",
            "Spec 088 adoption",
        )


def test_builder_is_idempotent_over_a_completed_index(tmp_path):
    repo, _, _ = _two_generation_repo(tmp_path)
    first = _run_builder(repo)
    assert first.returncode == 0, first.stderr
    index_bytes = (repo / STORE_REL / "run-index.jsonl").read_bytes()
    second = _run_builder(repo)
    assert second.returncode == 0, second.stderr
    assert "0 act(s) appended" in second.stdout
    assert (repo / STORE_REL / "run-index.jsonl").read_bytes() == index_bytes


def test_builder_leaves_every_record_byte_untouched(tmp_path):
    repo, _, _ = _two_generation_repo(tmp_path)
    before = {
        p.name: p.read_bytes()
        for p in (repo / STORE_REL).glob("*.json")
    }
    proc = _run_builder(repo)
    assert proc.returncode == 0, proc.stderr
    after = {
        p.name: p.read_bytes()
        for p in (repo / STORE_REL).glob("*.json")
    }
    assert before == after
    status = _git(repo, "status", "--porcelain", "--", STORE_REL)
    # The only worktree change the builder makes is the
    # index file itself.
    assert status.splitlines() == [f"?? {STORE_REL}/run-index.jsonl"]

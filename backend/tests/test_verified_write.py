"""Spec 092 Stage 2 — the verified-write library (T201) and its
fault-injection battery (T202; claims C092-6, C092-7, C092-8).

The battery seeds the failure classes the fleet actually met — the
classes the safe-write self-test (14 checks) models — by injection,
each asserting the typed error and the target's byte-preservation:

* denied open (mkstemp raises EPERM — the write-denial wave's face);
* silent 0-byte land (the write step reports success, lands nothing);
* short write (the write step lands a prefix, reports full length);
* missing parent and non-directory parent (never created, never
  escaped as a raw error — the fleet's 2026-10-28 regression class);
* rename-time failure (ENOSPC at ``os.replace`` — the F1 class,
  which a fresh process cannot heal and so must fail named through
  the local ladder), and rename denial (EPERM), which the ladder's
  fresh-subprocess leg exists to heal;
* a rename that lands wrong bytes (the temp truncated at rename
  time): detected by the post-rename read-back, never silent — and
  healed by the ladder when a clean lineage is available. (Against
  this one class byte-preservation of the target cannot be asserted
  at zero retries: the injected fault itself replaces the target.
  The contract's answer is detection plus the ladder, and the test
  asserts exactly that, no more.)

Injections patch ``os``/``tempfile`` attributes in this process
only, in the house style of ``test_atomic_io_disk_full.py`` — which
is precisely what makes the ladder tests meaningful: the
fresh-subprocess leg runs unpatched, as a fresh lineage does in
production.
"""

from __future__ import annotations

import errno
import hashlib
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from glossa_lab.atomic_io import StateWriteError
from glossa_lab.verified_write import (
    VerifiedWriteError,
    try_write_once,
    write_file_verified,
)

PAYLOAD = ("verified-write battery payload ✓\n" * 64).encode("utf-8")


def _raise_eperm(*args, **kwargs):  # noqa: ANN002, ANN003
    raise OSError(errno.EPERM, "Operation not permitted")


def _raise_enospc(*args, **kwargs):  # noqa: ANN002, ANN003
    raise OSError(errno.ENOSPC, "No space left on device")


class _DroppingWriter:
    """Wraps a real binary file object; ``write`` reports the full
    length but lands only a ``keep`` fraction of the bytes — the
    silent-land signature (0-byte land at keep=0, short write
    in between). Everything else delegates to the real object."""

    def __init__(self, real, keep: float) -> None:
        self._real = real
        self._keep = keep

    def write(self, data: bytes) -> int:
        n = int(len(data) * self._keep)
        if n:
            self._real.write(data[:n])
        return len(data)

    def __getattr__(self, name: str):  # noqa: ANN202
        return getattr(self._real, name)

    def __enter__(self) -> "_DroppingWriter":
        return self

    def __exit__(self, *exc) -> bool:
        self._real.close()
        return False


def _fdopen_dropping(keep: float):
    real_fdopen = os.fdopen

    def fake(fd, mode="r", *args, **kwargs):  # noqa: ANN002, ANN003, ANN202
        return _DroppingWriter(real_fdopen(fd, mode, *args, **kwargs), keep)

    return fake


def _names(directory: Path) -> list[str]:
    return sorted(p.name for p in directory.iterdir())


# ── Round-trips (T201 acceptance) ──────────────────────────────────────


def test_round_trip_bytes_with_receipt(tmp_path: Path) -> None:
    target = tmp_path / "state.bin"
    receipt = write_file_verified(target, PAYLOAD)
    assert target.read_bytes() == PAYLOAD
    assert receipt.sha256 == hashlib.sha256(PAYLOAD).hexdigest()
    assert receipt.attempts == 1
    assert receipt.via == "local"
    assert receipt.path == target
    # No temp file lingers after a successful write.
    assert _names(tmp_path) == ["state.bin"]


def test_round_trip_str_and_overwrite(tmp_path: Path) -> None:
    target = tmp_path / "state.txt"
    target.write_text("previous content", encoding="utf-8")
    receipt = write_file_verified(target, "new content ✓")
    assert target.read_text(encoding="utf-8") == "new content ✓"
    assert receipt.sha256 == hashlib.sha256("new content ✓".encode()).hexdigest()
    assert _names(tmp_path) == ["state.txt"]


def test_try_write_once_round_trip_and_empty_refusal(tmp_path: Path) -> None:
    target = tmp_path / "once.bin"
    assert try_write_once(target, PAYLOAD) is True
    assert target.read_bytes() == PAYLOAD
    assert try_write_once(tmp_path / "never.bin", b"") is False
    assert not (tmp_path / "never.bin").exists()


@pytest.mark.skipif(os.name != "posix", reason="mode bits are POSIX surface")
def test_mode_applied_before_rename(tmp_path: Path) -> None:
    target = tmp_path / "moded.bin"
    write_file_verified(target, PAYLOAD, mode=0o600)
    assert stat.S_IMODE(target.stat().st_mode) == 0o600
    write_file_verified(target, PAYLOAD, mode=0o644)
    assert stat.S_IMODE(target.stat().st_mode) == 0o644


# ── Empty content (refused before any attempt) ─────────────────────────


def test_empty_content_refused_and_target_untouched(tmp_path: Path) -> None:
    target = tmp_path / "existing.bin"
    target.write_bytes(PAYLOAD)
    for empty in ("", b""):
        with pytest.raises(VerifiedWriteError):
            write_file_verified(target, empty)
    assert target.read_bytes() == PAYLOAD
    ghost = tmp_path / "ghost.bin"
    with pytest.raises(VerifiedWriteError):
        write_file_verified(ghost, "")
    assert not ghost.exists()
    assert _names(tmp_path) == ["existing.bin"]


# ── Parents are never created ──────────────────────────────────────────


def test_missing_parent_fails_typed_and_creates_nothing(tmp_path: Path) -> None:
    target = tmp_path / "no-such-dir" / "state.bin"
    with pytest.raises(VerifiedWriteError) as excinfo:
        write_file_verified(target, PAYLOAD, retries=1)
    # The typed error — never a raw FileNotFoundError escaping.
    assert type(excinfo.value) is VerifiedWriteError
    assert str(target) in str(excinfo.value)
    assert not target.parent.exists()
    assert _names(tmp_path) == []


def test_non_directory_parent_fails_typed_and_preserves(tmp_path: Path) -> None:
    blocker = tmp_path / "blocker"
    blocker.write_bytes(PAYLOAD)
    with pytest.raises(VerifiedWriteError):
        write_file_verified(blocker / "state.bin", PAYLOAD, retries=0)
    assert blocker.read_bytes() == PAYLOAD
    assert _names(tmp_path) == ["blocker"]


# ── Denied open (the write-denial wave's face) ─────────────────────────


def test_denied_open_fails_typed_and_preserves_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "state.bin"
    target.write_bytes(PAYLOAD)
    monkeypatch.setattr(tempfile, "mkstemp", _raise_eperm)
    with pytest.raises(VerifiedWriteError) as excinfo:
        write_file_verified(target, b"replacement", retries=0)
    assert str(target) in str(excinfo.value)
    assert target.read_bytes() == PAYLOAD
    assert _names(tmp_path) == ["state.bin"]


def test_denied_open_healed_by_fresh_subprocess(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The denial is patched into this process only; the ladder's
    # fresh-subprocess leg is a clean lineage and lands the write —
    # the production behaviour under a lineage-sticky EPERM wave.
    target = tmp_path / "state.bin"
    monkeypatch.setattr(tempfile, "mkstemp", _raise_eperm)
    receipt = write_file_verified(target, PAYLOAD, retries=1)
    assert receipt.via.startswith("child")
    assert target.read_bytes() == PAYLOAD
    assert _names(tmp_path) == ["state.bin"]


# ── Silent lands (0-byte and short) ────────────────────────────────────


def test_zero_byte_land_fails_typed_and_preserves_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "state.bin"
    target.write_bytes(PAYLOAD)
    monkeypatch.setattr(os, "fdopen", _fdopen_dropping(0.0))
    with pytest.raises(VerifiedWriteError):
        write_file_verified(target, b"replacement", retries=0)
    # Caught at the temp's read-back, before any rename: the
    # previous target stands byte-identical (C092-7).
    assert target.read_bytes() == PAYLOAD
    assert _names(tmp_path) == ["state.bin"]


def test_short_write_fails_typed_and_preserves_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "state.bin"
    target.write_bytes(PAYLOAD)
    monkeypatch.setattr(os, "fdopen", _fdopen_dropping(0.5))
    with pytest.raises(VerifiedWriteError):
        write_file_verified(target, b"replacement", retries=0)
    assert target.read_bytes() == PAYLOAD
    assert _names(tmp_path) == ["state.bin"]


def test_zero_byte_land_healed_by_fresh_subprocess(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "state.bin"
    monkeypatch.setattr(os, "fdopen", _fdopen_dropping(0.0))
    receipt = write_file_verified(target, PAYLOAD, retries=1)
    assert receipt.via.startswith("child")
    assert target.read_bytes() == PAYLOAD


# ── Rename-time failures ───────────────────────────────────────────────


def test_rename_enospc_fails_named_and_preserves_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The F1 class: a full disk fails every lineage identically, so
    # the ladder's local rounds exhaust and the error names the
    # target and the cause — the behaviour the settings store's
    # disk-full battery pins end-to-end.
    target = tmp_path / "state.bin"
    target.write_bytes(PAYLOAD)
    monkeypatch.setattr(os, "replace", _raise_enospc)
    with pytest.raises(VerifiedWriteError) as excinfo:
        write_file_verified(target, b"replacement", retries=2)
    assert str(target) in str(excinfo.value)
    assert "No space left on device" in str(excinfo.value)
    assert target.read_bytes() == PAYLOAD
    assert _names(tmp_path) == ["state.bin"]


def test_rename_denial_healed_by_fresh_subprocess(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "state.bin"
    monkeypatch.setattr(os, "replace", _raise_eperm)
    receipt = write_file_verified(target, PAYLOAD, retries=1)
    assert receipt.via.startswith("child")
    assert target.read_bytes() == PAYLOAD


def test_rename_landing_wrong_bytes_is_detected_never_silent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The injected fault truncates the temp at rename time, so the
    # rename itself lands wrong bytes. The post-rename read-back
    # must name the failure (retries=0: nothing is silent), and the
    # ladder must heal it from a clean lineage (retries=1).
    real_replace = os.replace

    def truncating_replace(src, dst):  # noqa: ANN001, ANN202
        with open(src, "wb"):
            pass
        return real_replace(src, dst)

    target = tmp_path / "state.bin"
    target.write_bytes(b"previous")
    monkeypatch.setattr(os, "replace", truncating_replace)
    with pytest.raises(VerifiedWriteError):
        write_file_verified(target, PAYLOAD, retries=0)
    receipt = write_file_verified(target, PAYLOAD, retries=1)
    assert receipt.via.startswith("child")
    assert target.read_bytes() == PAYLOAD


# ── The typed error's place in the store's error surface ──────────────


def test_error_type_preserves_the_store_surface() -> None:
    # Stage 1's batteries assert StateWriteError on the settings
    # store's save path; the library's error must remain catchable
    # as exactly that type (the T203 re-proof runs those fixtures
    # unchanged against this path).
    assert issubclass(VerifiedWriteError, StateWriteError)


# ── The CLI (the ladder's subprocess leg, exercised directly) ─────────


def test_cli_write_round_trip(tmp_path: Path) -> None:
    target = tmp_path / "cli.bin"
    result = subprocess.run(
        [sys.executable, "-m", "glossa_lab.verified_write", "--write",
         str(target), "-"],
        input=PAYLOAD,
        capture_output=True,
    )
    assert result.returncode == 0
    assert target.read_bytes() == PAYLOAD


def test_cli_missing_parent_exit_3_named_no_traceback(tmp_path: Path) -> None:
    target = tmp_path / "no-such-dir" / "cli.bin"
    result = subprocess.run(
        [sys.executable, "-m", "glossa_lab.verified_write", "--write",
         str(target), "-"],
        input=PAYLOAD,
        capture_output=True,
    )
    assert result.returncode == 3
    assert b"VERIFIED-WRITE FAILED" in result.stderr
    assert b"Traceback" not in result.stderr
    assert not target.parent.exists()

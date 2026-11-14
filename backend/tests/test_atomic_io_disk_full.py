"""F1 — disk-full cascade containment (Spec 081 PR-3 precondition).

Before this fix, the backend's small state files (``{data_dir}/.keys.json``
— every stored API key and the Graph refresh token — and
``{data_dir}/presets.json``) were saved with ``Path.write_text``, which
opens the live file with O_TRUNC: a write that then failed (ENOSPC on a
full disk, or any other write error) had already destroyed the previous
good content, and a truncated/empty file was left standing — one failed
save cascading into the loss of the whole store.

These tests inject a write failure (``os.replace`` raising ENOSPC, the
last step of the atomic write, plus a write-leg failure) and prove:

* the failure surfaces as a NAMED error (``StateWriteError`` naming the
  target and the ENOSPC cause), never swallowed;
* the previous file content is byte-identical afterwards (no cascade);
* no temporary file is left behind;
* the unpatched failure mode really is destructive (control test: the
  old in-place ``write_text`` pattern loses the content under the same
  injected failure, proving the injection is real);
* the two converted stores (settings keys, presets) behave the same
  way end-to-end through their own save paths.
"""

from __future__ import annotations

import errno
import os
from pathlib import Path

import pytest

from glossa_lab import preset_store
from glossa_lab.api import settings as settings_api
from glossa_lab.atomic_io import StateWriteError, atomic_write_text

ENOSPC_ERROR = OSError(errno.ENOSPC, "No space left on device")


def _raise_enospc(*args, **kwargs):
    raise ENOSPC_ERROR


# ── The helper itself ────────────────────────────────────────────────────────


def test_successful_write_replaces_content(tmp_path: Path) -> None:
    target = tmp_path / "state.json"
    target.write_text('{"old": true}', encoding="utf-8")
    atomic_write_text(target, '{"new": true}')
    assert target.read_text(encoding="utf-8") == '{"new": true}'
    assert [p.name for p in tmp_path.iterdir()] == ["state.json"]


def test_disk_full_at_rename_fails_named_and_preserves_previous(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "state.json"
    previous = '{"api_key": "original-value"}'
    target.write_text(previous, encoding="utf-8")

    monkeypatch.setattr(os, "replace", _raise_enospc)
    with pytest.raises(StateWriteError) as excinfo:
        atomic_write_text(target, '{"api_key": "new-value"}')

    # Named: the error identifies the target and the disk-full cause.
    message = str(excinfo.value)
    assert str(target) in message
    assert "No space left on device" in message
    # Contained: the previous content survives byte-identical, and the
    # temporary file does not linger.
    assert target.read_text(encoding="utf-8") == previous
    assert [p.name for p in tmp_path.iterdir()] == ["state.json"]


def test_disk_full_during_write_leg_fails_named_and_preserves_previous(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "state.json"
    previous = '{"api_key": "original-value"}'
    target.write_text(previous, encoding="utf-8")

    monkeypatch.setattr(os, "fsync", _raise_enospc)
    with pytest.raises(StateWriteError) as excinfo:
        atomic_write_text(target, '{"api_key": "new-value"}')

    assert "No space left on device" in str(excinfo.value)
    assert target.read_text(encoding="utf-8") == previous
    assert [p.name for p in tmp_path.iterdir()] == ["state.json"]


def test_disk_full_with_no_previous_file_leaves_no_partial_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "state.json"
    monkeypatch.setattr(os, "replace", _raise_enospc)
    with pytest.raises(StateWriteError):
        atomic_write_text(target, '{"api_key": "new-value"}')
    assert not target.exists()
    assert list(tmp_path.iterdir()) == []


def test_old_in_place_write_loses_content_under_the_same_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Control: the pre-fix pattern really is destructive.

    Reproduces ``Path.write_text``'s open("w")-then-write shape with a
    real OS descriptor: the open truncates the file, then the write leg
    fails with the same injected ENOSPC — the content is gone. This is
    the cascade F1 names; the tests above prove it is now contained.
    """
    target = tmp_path / "state.json"
    target.write_text('{"api_key": "original-value"}', encoding="utf-8")

    fd = os.open(target, os.O_WRONLY | os.O_TRUNC)  # write_text's open mode
    try:
        with pytest.raises(OSError) as excinfo:
            _raise_enospc()
        assert excinfo.value.errno == errno.ENOSPC
    finally:
        os.close(fd)
    # The previous content was destroyed by the truncation alone.
    assert target.read_text(encoding="utf-8") == ""


# ── The converted stores, end-to-end through their own save paths ───────────


def test_save_keys_disk_full_preserves_stored_keys(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        settings_api, "_keys_file", lambda: tmp_path / ".keys.json"
    )
    # Spec 092 Stage 1: saving a credential-class value now requires
    # the encryption key (D-092-1 custody), so this test supplies a
    # synthetic fixture key at a patched custody location. The F1
    # assertions below are unchanged.
    import base64 as _base64

    key_file = tmp_path / "glossa-lab-credential.key"
    key_file.write_bytes(_base64.b64encode(bytes(range(1, 33))))
    monkeypatch.setattr(
        settings_api, "_credential_key_file", lambda: key_file
    )
    settings_api._save_keys({"openai_api_key": "original"})
    keys_file = tmp_path / ".keys.json"
    previous = keys_file.read_bytes()

    monkeypatch.setattr(os, "replace", _raise_enospc)
    with pytest.raises(StateWriteError) as excinfo:
        settings_api._save_keys({"openai_api_key": "rotated"})

    assert ".keys.json" in str(excinfo.value)
    assert keys_file.read_bytes() == previous
    assert settings_api._load_keys() == {"openai_api_key": "original"}


def test_preset_save_disk_full_preserves_stored_presets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        preset_store, "_store_path", lambda: tmp_path / "presets.json"
    )
    preset_store.add_pipeline_preset({"label": "original"})
    presets_file = tmp_path / "presets.json"
    previous = presets_file.read_bytes()

    monkeypatch.setattr(os, "replace", _raise_enospc)
    with pytest.raises(StateWriteError):
        preset_store.add_pipeline_preset({"label": "second"})

    assert presets_file.read_bytes() == previous
    labels = [p["label"] for p in preset_store.list_pipeline_presets()]
    assert labels == ["original"]

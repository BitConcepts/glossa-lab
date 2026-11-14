"""Spec 092 Stage 1 — credential encryption at rest (C092-1..5, C092-7
store leg).

The attack battery runs first in spirit: every fixture value here is
synthetic, and each test names the claim whose falsifier it exercises.

* C092-1 — no stored credential value is recoverable from the store
  file's bytes (plaintext, base64, hex, or any contiguous substring),
  while non-credential entries keep the exact v1 shape.
* C092-2 — a copy of the data dir alone cannot decrypt anything: the
  key material lives outside it and appears neither in the data dir
  nor in the repo tree.
* C092-3 — wrong key, missing key, malformed/wrong-length/unreadable
  key, bit-flipped ciphertext, and a corrupt store each produce the
  NAMED error state (distinct from "no keys configured") and serve no
  values; the loader never falls back to a plaintext parse.
* C092-4 — a legacy v1 store migrates exactly once, value-identical,
  or not at all (denied write / missing key leave the original file
  byte-untouched); an absent or credential-free store is a no-op.
* C092-5 — the consumer contract battery, run identically against v1
  and v2 stores: masked GET shape, PUT semantics incl. the process-env
  side effect, get_key resolution order and placeholder filtering, the
  notifications Graph save/disconnect path, the schedulers' toggles.
* C092-7 (store leg) — a failed save leaves the previous store
  byte-identical under the verified-write construction.

The store seam is the established one (cf. test_atomic_io_disk_full):
``_keys_file`` and ``_credential_key_file`` are monkeypatched to a
tmp layout that mirrors the production geometry — the key file a
sibling of the data dir, never inside it.
"""

from __future__ import annotations

import asyncio
import base64
import binascii
import errno
import json
import os
import shutil
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from glossa_lab.api import notifications as notifications_api
from glossa_lab.api import settings as settings_api
from glossa_lab.atomic_io import StateWriteError
from glossa_lab.discovery import scheduler as discovery_scheduler
from glossa_lab import study_loop_scheduler

# ── Synthetic fixture material ─────────────────────────────────────────
# Each key is exactly 32 bytes, assembled from named parts so the
# full key bytes (and their base64) appear in no single file — not
# even as a compiler-folded constant in this module's bytecode — and
# the C092-2 repo sweep below can run at full strength over every
# file in the tree, compiled caches included.
_FIXTURE_PART_A = b"synthetic-fixture-"
_FIXTURE_PART_B = b"key-for-tests!"
FIXTURE_KEY_BYTES = _FIXTURE_PART_A + _FIXTURE_PART_B
FIXTURE_KEY_B64 = base64.b64encode(FIXTURE_KEY_BYTES)
_OTHER_PART_A = b"other-synthetic-key"
_OTHER_PART_B = b"-for-tests!!!"
OTHER_KEY_BYTES = _OTHER_PART_A + _OTHER_PART_B
assert len(FIXTURE_KEY_BYTES) == 32 and len(OTHER_KEY_BYTES) == 32

CREDENTIAL_VALUES = {
    "openai_api_key": "sk-synthetic-openai-value-0001",
    "smtp_password": "synthetic-smtp-password-0002",
    "ms_graph_refresh_token": "synthetic-graph-refresh-token-0003",
    "glossa_service_credential": "synthetic-service-credential-0004",
    "hf_api_token": "hf-synthetic-token-0005",
}
CONFIG_VALUES = {
    "smtp_host": "smtp.example.invalid",
    "smtp_port": "587",
    "smtp_username": "alerts@example.invalid",
    "openalex_email": "operator@example.invalid",
    "discovery_daily": "1",
    "study_loop_daily": "1",
}
PREFS = {"ollama": {"enabled": True, "selected_model": "synthetic-model-7b"}}
FULL_FIXTURE: dict = {
    **CREDENTIAL_VALUES,
    **CONFIG_VALUES,
    "_provider_prefs": PREFS,
}


@pytest.fixture()
def store(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> SimpleNamespace:
    """A tmp store + key layout in the production geometry."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    keys_file = data_dir / ".keys.json"
    key_file = tmp_path / "glossa-lab-credential.key"
    monkeypatch.setattr(settings_api, "_keys_file", lambda: keys_file)
    monkeypatch.setattr(settings_api, "_credential_key_file", lambda: key_file)
    # Pristine environment for every name the contract touches, so the
    # env-precedence legs are deterministic (monkeypatch restores the
    # recorded state at teardown even when code under test writes env).
    for name in settings_api.KNOWN_KEYS:
        monkeypatch.delenv(name.upper(), raising=False)
    for name in CREDENTIAL_VALUES:
        monkeypatch.delenv(name.upper(), raising=False)
    monkeypatch.delenv(settings_api._KEY_FILE_ENV, raising=False)

    ns = SimpleNamespace(
        data_dir=data_dir, keys_file=keys_file, key_file=key_file
    )

    def write_key(key_bytes: bytes = FIXTURE_KEY_BYTES) -> None:
        key_file.write_bytes(base64.b64encode(key_bytes))

    def write_v1(values: dict) -> None:
        keys_file.write_text(json.dumps(values, indent=2), encoding="utf-8")

    ns.write_key = write_key
    ns.write_v1 = write_v1
    return ns


def _raise_enospc(*args, **kwargs):  # noqa: ANN002, ANN003
    raise OSError(errno.ENOSPC, "No space left on device")


# ── C092-1 — no credential value recoverable from the file bytes ───────


def test_c092_1_no_credential_value_recoverable_from_store_bytes(store):
    store.write_key()
    settings_api._save_keys(FULL_FIXTURE)
    raw = store.keys_file.read_bytes()
    for value in CREDENTIAL_VALUES.values():
        vb = value.encode("utf-8")
        assert vb not in raw, "credential value present as plaintext"
        assert base64.b64encode(vb) not in raw, "credential value present base64"
        assert binascii.hexlify(vb) not in raw, "credential value present hex"
        # Not as any contiguous substring of length >= 12 either.
        for i in range(len(vb) - 11):
            assert vb[i : i + 12] not in raw, "credential substring present"
    parsed = json.loads(raw)
    for name in CREDENTIAL_VALUES:
        envelope = parsed[name]
        assert settings_api._is_envelope(envelope)
        assert envelope["v"] == 2
        assert envelope["alg"] == "AES-256-GCM"
    # Non-credential entries keep the exact v1 shape.
    for name, value in CONFIG_VALUES.items():
        assert parsed[name] == value
    assert parsed["_provider_prefs"] == PREFS
    # And the store still serves plaintext to its callers.
    assert settings_api._load_keys() == FULL_FIXTURE


def test_c092_1_fresh_nonce_per_value_per_save(store):
    store.write_key()
    value = CREDENTIAL_VALUES["openai_api_key"]
    settings_api._save_keys({"openai_api_key": value})
    first = json.loads(store.keys_file.read_bytes())["openai_api_key"]
    settings_api._save_keys({"openai_api_key": value})
    second = json.loads(store.keys_file.read_bytes())["openai_api_key"]
    assert first["nonce"] != second["nonce"]
    assert first["ct"] != second["ct"]
    assert settings_api.get_key("openai_api_key") == value


# ── C092-2 — the key never lives in the data dir it protects ───────────


def test_c092_2_data_dir_copy_alone_cannot_decrypt(store, tmp_path, monkeypatch):
    store.write_key()
    settings_api._save_keys(FULL_FIXTURE)
    # The Spec 080 copy shape: the whole data dir, copied on its own.
    copied = tmp_path / "snapshot" / "data"
    shutil.copytree(store.data_dir, copied)
    monkeypatch.setattr(settings_api, "_keys_file", lambda: copied / ".keys.json")
    monkeypatch.setattr(
        settings_api,
        "_credential_key_file",
        lambda: copied.parent / "glossa-lab-credential.key",
    )
    # The copy carries no key custody: the load fails by name, and no
    # decryption is possible from the copied material alone.
    with pytest.raises(settings_api.CredentialKeyMissing):
        settings_api._load_keys()
    assert settings_api.get_key("openai_api_key") is None


def test_c092_2_key_material_absent_from_data_dir_and_repo(store):
    store.write_key()
    settings_api._save_keys(FULL_FIXTURE)
    for path in store.data_dir.rglob("*"):
        if path.is_file():
            blob = path.read_bytes()
            assert FIXTURE_KEY_BYTES not in blob
            assert FIXTURE_KEY_B64 not in blob
    # The repo tree sweep: the fixture key was never written into the
    # tree by the build or the tests. This test file itself is exempt —
    # it legitimately names the synthetic fixture key.
    repo_root = Path(__file__).resolve().parents[2]
    needles = (FIXTURE_KEY_BYTES, FIXTURE_KEY_B64)
    for path in repo_root.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path == Path(__file__).resolve():
            continue
        try:
            if path.stat().st_size > 32 * 1024 * 1024:
                continue
            blob = path.read_bytes()
        except OSError:
            continue
        for needle in needles:
            assert needle not in blob, f"key material found in {path}"


# ── C092-3 — an undecryptable store is a named error, never empty ──────


def test_c092_3_wrong_key_is_named_and_serves_nothing(store):
    store.write_key()
    settings_api._save_keys(FULL_FIXTURE)
    store.write_key(OTHER_KEY_BYTES)
    with pytest.raises(settings_api.CredentialStoreUndecryptable) as excinfo:
        settings_api._load_keys()
    assert excinfo.value.state == "credential_store_undecryptable"
    assert settings_api.get_key("openai_api_key") is None
    body = asyncio.run(settings_api.read_settings())
    assert body["store_error"]["state"] == "credential_store_undecryptable"
    # Nothing stored is reported as set from the store in this state.
    assert all(
        entry["source"] != "stored" for entry in body["keys"].values()
    )


def test_c092_3_missing_key_is_named(store):
    store.write_key()
    settings_api._save_keys(FULL_FIXTURE)
    store.key_file.unlink()
    with pytest.raises(settings_api.CredentialKeyMissing) as excinfo:
        settings_api._load_keys()
    assert excinfo.value.state == "credential_key_missing"
    body = asyncio.run(settings_api.read_settings())
    assert body["store_error"]["state"] == "credential_key_missing"
    assert settings_api.get_key("smtp_password") is None


def test_c092_3_bit_flipped_ciphertext_is_named(store):
    store.write_key()
    settings_api._save_keys(FULL_FIXTURE)
    parsed = json.loads(store.keys_file.read_bytes())
    ct = bytearray(base64.b64decode(parsed["openai_api_key"]["ct"]))
    ct[0] ^= 0x01
    parsed["openai_api_key"]["ct"] = base64.b64encode(bytes(ct)).decode("ascii")
    store.keys_file.write_text(json.dumps(parsed, indent=2), encoding="utf-8")
    with pytest.raises(settings_api.CredentialStoreUndecryptable):
        settings_api._load_keys()
    assert settings_api.get_key("openai_api_key") is None


def test_c092_3_key_loader_failure_modes_are_distinct(store):
    # Missing
    with pytest.raises(settings_api.CredentialKeyMissing) as e_missing:
        settings_api._load_credential_key()
    # Wrong length (valid base64, 16 bytes)
    store.key_file.write_bytes(base64.b64encode(b"sixteen-byte-key"))
    with pytest.raises(settings_api.CredentialKeyWrongLength) as e_length:
        settings_api._load_credential_key()
    # Malformed (not base64)
    store.key_file.write_bytes(b"!!! not base64 !!!")
    with pytest.raises(settings_api.CredentialKeyMalformed) as e_malformed:
        settings_api._load_credential_key()
    # Unreadable (the custody path is a directory)
    store.key_file.unlink()
    store.key_file.mkdir()
    with pytest.raises(settings_api.CredentialKeyUnreadable) as e_unreadable:
        settings_api._load_credential_key()
    states = {
        e_missing.value.state,
        e_length.value.state,
        e_malformed.value.state,
        e_unreadable.value.state,
    }
    assert states == {
        "credential_key_missing",
        "credential_key_wrong_length",
        "credential_key_malformed",
        "credential_key_unreadable",
    }


def test_c092_3_absent_store_is_unconfigured_not_an_error(store):
    assert settings_api._load_keys() == {}
    body = asyncio.run(settings_api.read_settings())
    assert "store_error" not in body
    assert all(entry["set"] is False for entry in body["keys"].values())


def test_c092_3_corrupt_store_is_named_not_empty(store):
    store.keys_file.write_text("{ not json", encoding="utf-8")
    with pytest.raises(settings_api.CredentialStoreCorrupt) as excinfo:
        settings_api._load_keys()
    assert excinfo.value.state == "credential_store_corrupt"
    body = asyncio.run(settings_api.read_settings())
    assert body["store_error"]["state"] == "credential_store_corrupt"


def test_c092_3_misshapen_credential_entry_is_never_served(store):
    # A credential entry that is neither a v1 string nor a v2 envelope
    # must not be parsed as plaintext or served in any form.
    store.write_key()
    store.write_v1({"openai_api_key": {"v": 1, "ct": "AAAA"}})
    with pytest.raises(settings_api.CredentialStoreCorrupt):
        settings_api._load_keys()
    assert settings_api.get_key("openai_api_key") is None


def test_c092_3_put_refused_from_unreadable_store(store):
    store.write_key()
    settings_api._save_keys(FULL_FIXTURE)
    store.write_key(OTHER_KEY_BYTES)
    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(settings_api.update_settings({"smtp_host": "x.example"}))
    assert excinfo.value.status_code == 503
    assert "credential_store_undecryptable" in excinfo.value.detail


def test_c092_3_put_credential_without_key_writes_nothing(store):
    # No key custody at all: a PUT carrying a credential is refused by
    # name, and no plaintext store file is ever created.
    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(
            settings_api.update_settings(
                {"openai_api_key": CREDENTIAL_VALUES["openai_api_key"]}
            )
        )
    assert excinfo.value.status_code == 503
    assert "credential_key_missing" in excinfo.value.detail
    assert not store.keys_file.exists()


# ── C092-4 — legacy migration: exactly once, verifiably, or not at all ─


def test_c092_4_legacy_store_migrates_value_identical(store):
    store.write_key()
    store.write_v1(FULL_FIXTURE)
    loaded = settings_api._load_keys()
    assert loaded == FULL_FIXTURE
    for name, value in CREDENTIAL_VALUES.items():
        assert settings_api.get_key(name) == value
    parsed = json.loads(store.keys_file.read_bytes())
    for name in CREDENTIAL_VALUES:
        assert settings_api._is_envelope(parsed[name])
    for name, value in CONFIG_VALUES.items():
        assert parsed[name] == value
    assert parsed["_provider_prefs"] == PREFS


def test_c092_4_migration_happens_exactly_once(store):
    store.write_key()
    store.write_v1(FULL_FIXTURE)
    settings_api._load_keys()
    migrated_bytes = store.keys_file.read_bytes()
    settings_api._load_keys()
    settings_api._load_keys()
    assert store.keys_file.read_bytes() == migrated_bytes


def test_c092_4_credential_free_store_is_a_noop(store):
    config_only = {**CONFIG_VALUES, "_provider_prefs": PREFS}
    store.write_v1(config_only)
    before = store.keys_file.read_bytes()
    # No key file exists: a credential-free store never consults it.
    assert settings_api._load_keys() == config_only
    assert store.keys_file.read_bytes() == before


def test_c092_4_absent_store_is_a_noop(store):
    assert settings_api._load_keys() == {}
    assert not store.keys_file.exists()


def test_c092_4_denied_write_migration_leaves_original_bytes(store, monkeypatch):
    store.write_key()
    store.write_v1(FULL_FIXTURE)
    before = store.keys_file.read_bytes()
    monkeypatch.setattr(os, "replace", _raise_enospc)
    with pytest.raises(settings_api.CredentialStoreError) as excinfo:
        settings_api._load_keys()
    assert excinfo.value.state == "credential_store_migration_failed"
    assert store.keys_file.read_bytes() == before


def test_c092_4_missing_key_migration_leaves_original_bytes(store):
    store.write_v1(FULL_FIXTURE)
    before = store.keys_file.read_bytes()
    with pytest.raises(settings_api.CredentialKeyMissing):
        settings_api._load_keys()
    assert store.keys_file.read_bytes() == before
    # And the plaintext is NOT served as a fallback parse.
    assert settings_api.get_key("openai_api_key") is None


# ── C092-5 — the contract battery, identical against v1 and v2 ─────────

CONTRACT_FIXTURE: dict = {
    "openai_api_key": "sk-synthetic-contract-1001",
    "news_api_key": "synthetic-news-contract-1002",
    "smtp_host": "smtp.example.invalid",
    "smtp_password": "synthetic-smtp-contract-1003",
    "ms_graph_refresh_token": "synthetic-graph-contract-1004",
    "discovery_daily": "1",
    "study_loop_daily": "1",
    "_provider_prefs": PREFS,
}


@pytest.mark.parametrize("fmt", ["v1", "v2"])
def test_c092_5_contract_battery(store, fmt: str):
    store.write_key()
    if fmt == "v1":
        store.write_v1(CONTRACT_FIXTURE)
    else:
        settings_api._save_keys(CONTRACT_FIXTURE)

    # Masked GET shape — identical fields, values, and masking.
    body = asyncio.run(settings_api.read_settings())
    assert "store_error" not in body
    assert set(body["keys"]) == set(settings_api.KNOWN_KEYS)
    assert body["keys"]["openai_api_key"] == {
        "set": True, "source": "stored", "masked": settings_api._MASK,
    }
    assert body["keys"]["anthropic_api_key"] == {
        "set": False, "source": None, "masked": "",
    }
    assert body["providers"] == PREFS

    # get_key serves the consumers' reads (smtp.py, graph.py) as before.
    assert settings_api.get_key("openai_api_key") == "sk-synthetic-contract-1001"
    assert settings_api.get_key("smtp_password") == "synthetic-smtp-contract-1003"
    assert (
        settings_api.get_key("ms_graph_refresh_token")
        == "synthetic-graph-contract-1004"
    )

    # Resolution order: process env over stored.
    os.environ["OPENAI_API_KEY"] = "env-synthetic-value-1005"
    assert settings_api.get_key("openai_api_key") == "env-synthetic-value-1005"
    env_body = asyncio.run(settings_api.read_settings())
    assert env_body["keys"]["openai_api_key"]["source"] == "env"
    # A placeholder env value falls back to the stored value.
    os.environ["OPENAI_API_KEY"] = "dummy-env-value"
    assert settings_api.get_key("openai_api_key") == "sk-synthetic-contract-1001"
    del os.environ["OPENAI_API_KEY"]
    # A placeholder stored value is treated as unset.
    stored = settings_api._load_keys()
    stored["news_api_key"] = "dummy-stored-value"
    settings_api._save_keys(stored)
    assert settings_api.get_key("news_api_key") is None
    stored["news_api_key"] = "synthetic-news-contract-1002"
    settings_api._save_keys(stored)

    # PUT semantics, including the process-env side effect.
    result = asyncio.run(
        settings_api.update_settings(
            {
                "openai_api_key": "sk-synthetic-rotated-1006",
                "news_api_key": "",
                "smtp_host": "smtp2.example.invalid",
            }
        )
    )
    assert set(result["updated"]) == {
        "openai_api_key", "news_api_key", "smtp_host",
    }
    assert os.environ["OPENAI_API_KEY"] == "sk-synthetic-rotated-1006"
    assert "NEWS_API_KEY" not in os.environ
    del os.environ["OPENAI_API_KEY"]
    assert settings_api.get_key("openai_api_key") == "sk-synthetic-rotated-1006"
    assert settings_api.get_key("news_api_key") is None
    assert settings_api._load_keys()["smtp_host"] == "smtp2.example.invalid"
    # Whatever the input format, the persisted credential is an envelope.
    parsed = json.loads(store.keys_file.read_bytes())
    assert settings_api._is_envelope(parsed["openai_api_key"])

    # The notifications Graph disconnect path (the real endpoint),
    # and the save path's exact store calls.
    disconnected = asyncio.run(notifications_api.graph_disconnect())
    assert disconnected == {"disconnected": True}
    assert settings_api.get_key("ms_graph_refresh_token") is None
    stored = settings_api._load_keys()
    stored["ms_graph_refresh_token"] = "synthetic-graph-restored-1007"
    settings_api._save_keys(stored)
    assert (
        settings_api.get_key("ms_graph_refresh_token")
        == "synthetic-graph-restored-1007"
    )
    parsed = json.loads(store.keys_file.read_bytes())
    assert settings_api._is_envelope(parsed["ms_graph_refresh_token"])
    assert asyncio.run(notifications_api.graph_disconnect()) == {
        "disconnected": True
    }
    assert asyncio.run(notifications_api.graph_disconnect()) == {
        "disconnected": False
    }

    # The schedulers' toggles round-trip through the same store, and
    # the load/save cycle leaves credential values undisturbed.
    discovery_scheduler.set_persistent_enabled(False)
    assert "discovery_daily" not in settings_api._load_keys()
    discovery_scheduler.set_persistent_enabled(True)
    assert settings_api._load_keys()["discovery_daily"] == "1"
    study_loop_scheduler.set_persistent_enabled(False)
    assert "study_loop_daily" not in settings_api._load_keys()
    study_loop_scheduler.set_persistent_enabled(True)
    assert settings_api._load_keys()["study_loop_daily"] == "1"
    assert settings_api.get_key("openai_api_key") == "sk-synthetic-rotated-1006"
    assert settings_api.get_key("smtp_password") == "synthetic-smtp-contract-1003"


# ── C092-7 (store leg) — a failed save never destroys the prior store ──


def test_c092_7_failed_save_preserves_previous_store(store, monkeypatch):
    store.write_key()
    settings_api._save_keys(FULL_FIXTURE)
    before = store.keys_file.read_bytes()
    real_replace = os.replace
    monkeypatch.setattr(os, "replace", _raise_enospc)
    with pytest.raises(StateWriteError):
        settings_api._save_keys({"openai_api_key": "sk-synthetic-rotated-2001"})
    assert store.keys_file.read_bytes() == before
    monkeypatch.setattr(os, "replace", real_replace)
    assert settings_api._load_keys() == FULL_FIXTURE


# ── The glossa_service_credential disposition ──────────────────────────


def test_service_credential_registered_encrypted_but_not_put_writable(store):
    # Credential-class in substance (it authenticates service calls and
    # cloud_scope resolves it through get_key), so it is registered in
    # the encrypted set...
    assert "glossa_service_credential" in settings_api.CREDENTIAL_KEYS
    # ...but it is deliberately NOT added to KNOWN_KEYS: the masked GET
    # shape and the PUT writable set are the frozen C092-5 surface, and
    # provisioning this credential stays an operator act. Standing
    # decision, recorded in the stage PR — not an oversight.
    assert "glossa_service_credential" not in settings_api.KNOWN_KEYS

    store.write_key()
    value = CREDENTIAL_VALUES["glossa_service_credential"]
    settings_api._save_keys({"glossa_service_credential": value})
    parsed = json.loads(store.keys_file.read_bytes())
    assert settings_api._is_envelope(parsed["glossa_service_credential"])
    assert settings_api.get_key("glossa_service_credential") == value

    result = asyncio.run(
        settings_api.update_settings(
            {"glossa_service_credential": "synthetic-other-value"}
        )
    )
    assert "glossa_service_credential" not in result["updated"]
    assert settings_api.get_key("glossa_service_credential") == value

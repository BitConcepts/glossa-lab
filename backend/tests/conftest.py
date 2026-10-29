"""Shared test fixtures."""

# ── Windows pytest cleanup workaround (per H17.2) ─────────────────────────────
# pytest's cleanup_dead_symlinks() calls Path.resolve() on every entry under the
# basetemp dir. On Windows, if a stale Junction/symlink target is unreachable,
# realpath raises OSError [WinError 448] ("untrusted mount point"). That crashes
# pytest_sessionfinish AFTER all tests have passed, suppressing the
# `== N passed ==` summary line and giving a non-zero exit even on a green run.
#
# Patch the cleanup to swallow OSError so the run reports its true outcome.
import os as _os

import pytest
from fastapi.testclient import TestClient as _ImportedTestClient

# ── Spec 082 test seam ────────────────────────────────────────────────────────
# The backend enforces a per-install API token (Spec 082). The suite
# runs against a fixed, clearly-fake session token carried in the
# environment (the backend resolves the env first), and every
# TestClient built anywhere in the suite presents it by default —
# several test modules construct their own TestClient instead of
# using the client fixture below. Per-request headers still win, so
# the auth matrix (tests/test_api_token_auth.py) can present missing,
# empty, or wrong credentials explicitly. This seam must be installed
# BEFORE glossa_lab.main is imported anywhere in the process.
_TEST_API_TOKEN = "glossa-lab-test-token-082"  # test fixture value, not a secret
_os.environ.setdefault("GLOSSA_API_TOKEN", _TEST_API_TOKEN)

import fastapi.testclient as _fastapi_testclient  # noqa: E402


class _AuthedTestClient(_ImportedTestClient):
    """TestClient presenting the session test token by default."""

    def __init__(self, *args, **kwargs):  # noqa: ANN002, ANN003
        headers = dict(kwargs.pop("headers", None) or {})
        if not any(key.lower() == "authorization" for key in headers):
            headers["Authorization"] = f"Bearer {_TEST_API_TOKEN}"
        super().__init__(*args, headers=headers, **kwargs)


_fastapi_testclient.TestClient = _AuthedTestClient
TestClient = _AuthedTestClient

from glossa_lab.main import create_app  # noqa: E402

if _os.name == "nt":
    try:
        from _pytest import pathlib as _pp
        from _pytest import tmpdir as _ptmp

        _orig_cleanup = _pp.cleanup_dead_symlinks

        def _safe_cleanup_dead_symlinks(base):
            try:
                return _orig_cleanup(base)
            except OSError:
                # WinError 448 on stale junction targets — non-fatal.
                return None

        _pp.cleanup_dead_symlinks = _safe_cleanup_dead_symlinks
        # tmpdir.py has its own bound import — patch that too
        if hasattr(_ptmp, "cleanup_dead_symlinks"):
            _ptmp.cleanup_dead_symlinks = _safe_cleanup_dead_symlinks

        # Also wrap cleanup_numbered_dir which is invoked by atexit and
        # internally calls cleanup_dead_symlinks (atexit_callback raises)
        _orig_numbered = _pp.cleanup_numbered_dir

        def _safe_cleanup_numbered_dir(*args, **kwargs):
            try:
                return _orig_numbered(*args, **kwargs)
            except OSError:
                return None

        _pp.cleanup_numbered_dir = _safe_cleanup_numbered_dir
        if hasattr(_ptmp, "cleanup_numbered_dir"):
            _ptmp.cleanup_numbered_dir = _safe_cleanup_numbered_dir
    except Exception:  # noqa: BLE001
        pass


@pytest.fixture(scope="session")
def app():
    """Create the FastAPI app once per test session."""
    return create_app()


@pytest.fixture(scope="session")
def client(app):
    """TestClient with lifespan properly entered (database initialised)."""
    with TestClient(app) as c:
        yield c


# ── aee >= 1.5 strict-loader compatibility for legacy claim dicts ─────
# Specs 026-036 froze claim registers in the pre-1.5 serialization:
# ``boundary`` as a plain string and no lifecycle ``stage`` field.
# aee 1.5.0's ``Claim.from_dict`` is strict by default and refuses
# both; its own error text names the remedy for historical bundles —
# load leniently (``strict=False``, FR-1.3), which reproduces the
# pre-1.5 loader semantics those tests were written against. The
# freeze test files are themselves frozen sources (each spec's
# freeze digest covers its test file), so this compatibility shim
# cannot live in them; it lives here, applies only to dicts carrying
# the legacy signature (a string ``boundary`` or no ``stage``
# field), and leaves strict loading in force for every other claim
# dict.
import aee.model as _aee_model

_orig_claim_from_dict = _aee_model.Claim.from_dict.__func__


def _claim_from_dict_compat(cls, value, *args, **kwargs):
    if isinstance(value, dict) and (
        isinstance(value.get("boundary"), str) or "stage" not in value
    ):
        kwargs.setdefault("strict", False)
    return _orig_claim_from_dict(cls, value, *args, **kwargs)


_aee_model.Claim.from_dict = classmethod(_claim_from_dict_compat)

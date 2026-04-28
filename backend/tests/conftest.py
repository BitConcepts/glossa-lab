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
from fastapi.testclient import TestClient

from glossa_lab.main import create_app

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

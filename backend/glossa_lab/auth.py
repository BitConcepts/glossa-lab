"""Per-install API token authentication (Spec 082).

One install, one bearer token. The token is generated once per
install with a CSPRNG (``secrets.token_urlsafe(32)`` — 256 bits),
stored only in the ``api_token`` file in the install's data
directory (POSIX mode ``0600``), and presented as
``Authorization: Bearer <token>`` — the single credential form the
backend accepts (FR-001, FR-002). It is never written to git, never
logged, and never returned by an API response; display surfaces use
:func:`token_fingerprint` instead.

Resolution order for the server's expected token:

1. the ``GLOSSA_API_TOKEN`` environment variable;
2. the ``api_token`` file in ``Settings.data_dir`` — generated and
   persisted on first use, so a pre-token install upgrades itself
   on first start of this code.

Rotation is live: the file-backed token is cached keyed on the
file's mtime, so replacing the file (``python -m glossa_lab.auth
rotate``) takes effect without a backend restart (FR-004).

The only non-enforcing configuration is ``GLOSSA_API_AUTH=off``
(FR-006): it logs a startup warning (in ``create_app``) and the
health payload reports ``"auth": "disabled"``. It exists for CI's
frontend-tests job until the SPA implements the UI contract in
``specs/082-api-token-auth/ui-contract.md``; its removal is Spec 082
task T010, owned by the Spec 081 Phase 2 landing. Installers never
set it.

Operator CLI (never prints the token value)::

    python -m glossa_lab.auth ensure       # create the file if absent
    python -m glossa_lab.auth rotate       # replace the token atomically
    python -m glossa_lab.auth path         # print the token file path
    python -m glossa_lab.auth fingerprint  # print the SHA-256 fingerprint
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import logging
import os
import secrets
import sys
import tempfile
from collections.abc import Mapping
from pathlib import Path

from starlette.datastructures import Headers
from starlette.responses import JSONResponse

_log = logging.getLogger("glossa_lab.auth")

TOKEN_FILENAME = "api_token"
ENV_TOKEN = "GLOSSA_API_TOKEN"
ENV_TOKEN_FILE = "GLOSSA_TOKEN_FILE"
ENV_AUTH_SWITCH = "GLOSSA_API_AUTH"

#: The one 401 detail string (ui-contract.md pins it for the UI).
UNAUTHORIZED_DETAIL = "API token required or invalid"

#: Routes that stay open without a token (spec open-routes table).
_OPEN_EXACT = {"/api/v1/health"}
_SCHEMA_PATHS = {"/docs", "/redoc", "/openapi.json"}


# ── Generation, fingerprint, mode ─────────────────────────────────


def generate_token() -> str:
    """Return a fresh 256-bit CSPRNG token (43 urlsafe characters)."""
    return secrets.token_urlsafe(32)


def token_fingerprint(token: str) -> str:
    """First 8 hex chars of the token's SHA-256 — safe to display."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()[:8]


def auth_disabled() -> bool:
    """True only under the named ``GLOSSA_API_AUTH=off`` switch."""
    return os.environ.get(ENV_AUTH_SWITCH, "").strip().lower() == "off"


def auth_mode() -> str:
    """The health payload's auth word: ``"token"`` or ``"disabled"``."""
    return "disabled" if auth_disabled() else "token"


# ── Token file ────────────────────────────────────────────────────


def token_file_path(data_dir: Path | None = None) -> Path:
    """Path of the install's token file (default: Settings.data_dir)."""
    if data_dir is None:
        from glossa_lab.config import get_settings

        data_dir = Path(get_settings().data_dir)
    return Path(data_dir) / TOKEN_FILENAME


def _read_token_file(path: Path) -> str | None:
    try:
        value = path.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return value or None


def _write_token_file(path: Path, token: str) -> None:
    """Atomically replace the token file, mode 0600 on POSIX."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".api_token.")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(token)
        if os.name == "posix":
            os.chmod(tmp, 0o600)
        os.replace(tmp, path)
        if os.name == "posix":
            # Replacing a pre-existing looser file must not widen it.
            os.chmod(path, 0o600)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def ensure_token(data_dir: Path | None = None) -> str:
    """Return the install token, generating + persisting it if absent."""
    path = token_file_path(data_dir)
    token = _read_token_file(path)
    if token is None:
        token = generate_token()
        _write_token_file(path, token)
        _log.info(
            "API token generated at %s (fingerprint %s)",
            path,
            token_fingerprint(token),
        )
    return token


def rotate_token(data_dir: Path | None = None) -> str:
    """Atomically replace the install token; return the new token."""
    path = token_file_path(data_dir)
    token = generate_token()
    _write_token_file(path, token)
    _log.info(
        "API token rotated at %s (new fingerprint %s)",
        path,
        token_fingerprint(token),
    )
    return token


# ── Server-side expectation (env → file, mtime-cached) ────────────

_file_cache: tuple[str, float, str] | None = None


def expected_token() -> str:
    """The token the server expects, per the resolution order above."""
    global _file_cache  # noqa: PLW0603
    env_token = os.environ.get(ENV_TOKEN, "").strip()
    if env_token:
        return env_token
    path = token_file_path()
    try:
        mtime: float | None = path.stat().st_mtime
    except OSError:
        mtime = None
    if (
        _file_cache is not None
        and _file_cache[0] == str(path)
        and mtime is not None
        and _file_cache[1] == mtime
    ):
        return _file_cache[2]
    token = _read_token_file(path)
    if token is None:
        token = ensure_token()
        try:
            mtime = path.stat().st_mtime
        except OSError:
            mtime = None
    _file_cache = (str(path), mtime if mtime is not None else -1.0, token)
    return token


def verify_presented(presented: str | None) -> bool:
    """Constant-time check of a presented token (never reflects it)."""
    if auth_disabled():
        return True
    if not presented:
        return False
    return hmac.compare_digest(presented, expected_token())


def bearer_token(headers: Mapping[str, str]) -> str | None:
    """Extract the Bearer credential from request headers, if any.

    Query-string credentials are refused by design (spec FR-002):
    only the Authorization header is consulted, ever.
    """
    raw = headers.get("authorization")
    if not raw:
        return None
    scheme, _, value = raw.partition(" ")
    if scheme.lower() != "bearer":
        return None
    return value.strip() or None


def is_open_path(path: str, method: str = "GET") -> bool:
    """True for the spec's open routes; everything else is protected."""
    if path in _OPEN_EXACT:
        return method == "GET"
    if path in _SCHEMA_PATHS:
        return False
    if path.startswith("/api/"):
        return False
    if path == "/static/signs" or path.startswith("/static/signs/"):
        return True
    # The built frontend bundle and its assets: the SPA must load
    # before it can present a credential (spec open-routes table).
    return True


class ApiTokenMiddleware:
    """Pure-ASGI token enforcement (streaming-safe: no body reads).

    Added by ``create_app()`` inside CORS, so dev-mode preflights are
    answered by CORS rather than rejected here (plan step 1).
    """

    def __init__(self, app) -> None:  # noqa: ANN001 - ASGI app callable
        self.app = app

    async def __call__(self, scope, receive, send) -> None:  # noqa: ANN001
        if scope["type"] == "http":
            path = scope.get("path", "")
            method = scope.get("method", "GET")
            if not is_open_path(path, method) and not auth_disabled():
                presented = bearer_token(Headers(scope=scope))
                if not verify_presented(presented):
                    response = JSONResponse(
                        {"detail": UNAUTHORIZED_DETAIL},
                        status_code=401,
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                    await response(scope, receive, send)
                    return
        elif scope["type"] == "websocket":
            path = scope.get("path", "")
            if (
                path.startswith("/api/")
                and not is_open_path(path)
                and not auth_disabled()
                and not verify_presented(bearer_token(Headers(scope=scope)))
            ):
                await send({"type": "websocket.close", "code": 4401})
                return
        await self.app(scope, receive, send)


# ── First-party consumer resolution (in-process callers) ──────────


def consumer_token() -> str | None:
    """Resolve the token for an in-process first-party caller.

    Order: ``GLOSSA_API_TOKEN`` env → ``GLOSSA_TOKEN_FILE`` →
    ``Settings.data_dir`` file → the dev/supervised ``backend/data``
    file beside this package. ``None`` means unresolvable; callers
    proceed without the header and the backend's 401 is the named
    failure in their own logs (FR-003).
    """
    env_token = os.environ.get(ENV_TOKEN, "").strip()
    if env_token:
        return env_token
    explicit = os.environ.get(ENV_TOKEN_FILE, "").strip()
    if explicit:
        token = _read_token_file(Path(explicit))
        if token:
            return token
    token = _read_token_file(token_file_path())
    if token:
        return token
    dev_path = Path(__file__).resolve().parent.parent / "data" / TOKEN_FILENAME
    return _read_token_file(dev_path)


def auth_headers() -> dict[str, str]:
    """Authorization header dict for first-party callers (may be {})."""
    token = consumer_token()
    return {"Authorization": f"Bearer {token}"} if token else {}


# ── Operator CLI ──────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    """``python -m glossa_lab.auth`` — never prints the token value."""
    parser = argparse.ArgumentParser(
        prog="glossa_lab.auth",
        description="Manage the install's Spec 082 API token.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("ensure", help="create the token file if absent")
    sub.add_parser("rotate", help="replace the token atomically")
    sub.add_parser("path", help="print the token file path")
    sub.add_parser("fingerprint", help="print the token's fingerprint")
    args = parser.parse_args(argv)

    path = token_file_path()
    if args.command == "path":
        print(path)
        return 0
    if args.command == "ensure":
        token = ensure_token()
    elif args.command == "rotate":
        # An env-carried token cannot be rotated by rewriting a file
        # the server will never read first; refuse, named (FR-004).
        if os.environ.get(ENV_TOKEN, "").strip():
            print(
                f"error: {ENV_TOKEN} is set; rotate by updating the "
                "environment instead — the token file is not authoritative",
                file=sys.stderr,
            )
            return 2
        token = rotate_token()
    elif args.command == "fingerprint":
        resolved = consumer_token()
        if not resolved:
            print("error: no API token resolvable", file=sys.stderr)
            return 1
        print(token_fingerprint(resolved))
        return 0
    else:  # pragma: no cover - argparse enforces the subcommand set
        return 2
    print(f"api_token: {path}")
    print(f"fingerprint: {token_fingerprint(token)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

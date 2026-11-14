"""Settings API — secure storage of API keys and configuration.

Keys are stored in {data_dir}/.keys.json (not in the database).
Values are never returned in plaintext; only a masked status is returned.

Spec 092 Stage 1 — store format v2: every credential-class value (the
registered set ``CREDENTIAL_KEYS`` below) is encrypted at rest with
AES-256-GCM under a key held OUTSIDE the data dir (decision D-092-1,
custody option (a)); non-credential entries keep the v1 plaintext
shape (D-092-2, per-value scope). A legacy v1 store migrates on first
load, exactly once and verifiably (C092-4). A store that cannot be
decrypted raises a named :class:`CredentialStoreError` — it is never
silently presented as an empty store (C092-3).
"""

from __future__ import annotations

import base64
import binascii
import json
import os
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.atomic_io import StateWriteError
from glossa_lab.config import get_settings

router = APIRouter(prefix="/api/v1/settings", tags=["settings"])

_MASK = "••••••••"

KNOWN_KEYS = [
    # LLM providers (verifiable via _VERIFY_ENDPOINTS)
    "mistral_api_key",
    "openai_api_key",
    "anthropic_api_key",
    "google_api_key",
    # Discovery / search providers — used by the continuous-discovery engine
    # (no verify endpoints yet; added in a follow-up phase if needed).
    "serp_api_key",
    "news_api_key",
    "brave_search_api_key",
    # Optional API keys for higher rate limits on keyless sources.
    # Semantic Scholar: free key removes the 100 req/5min cap.
    # OpenAlex: "polite pool" with an email gets priority access.
    "semantic_scholar_api_key",
    "openalex_email",
    # CORE (core.ac.uk) — 449M+ open access papers, API key unlocks higher
    # daily token budget (1,000/day personal vs 100/day anonymous).
    "core_api_key",
    # Unpaywall — finds open-access versions of papers by DOI. Free API,
    # but an email address is required to identify your requests.
    # Rate limit: 100,000 requests/day. No API key — just your email.
    "unpaywall_email",
    # Patent data sources.
    # PatentsView/PPUBS is keyless (ppubs.uspto.gov session API) — no key needed.
    # USPTO Open Data Portal — required for the ODP fetcher (api.uspto.gov).
    "uspto_api_key",
    # Academia.edu — NOT an API key, but a *session cookie* harvested from a
    # logged-in browser. Optional. When present the academia.py fetcher
    # upgrades from public-search-only to authenticated mode and can stream
    # PDFs into the local data dir. Leave unset for keyless metadata-only
    # discovery, which works without any account.
    "academia_session_cookie",
    # SMTP — outbound email notifications (discovery digest + study/experiment
    # completion emails). All optional; if smtp_host or smtp_from is unset the
    # Notifier becomes a silent no-op so runs never fail because of missing creds.
    "smtp_host",
    "smtp_port",
    "smtp_username",
    "smtp_password",
    "smtp_from",
    "smtp_use_tls",
    # Microsoft Graph (Outlook 365 OAuth) — set via the Connect Outlook 365
    # button in the Notifications panel, which runs the device-code flow.
    # ``ms_graph_client_id`` is the Application (client) ID from the Azure
    # app registration; ``ms_graph_tenant_id`` defaults to ``common`` so
    # both consumer and work/school accounts work; ``ms_graph_refresh_token``
    # is written by the OAuth callback after the user approves consent.
    "ms_graph_client_id",
    "ms_graph_tenant_id",
    "ms_graph_refresh_token",
    # Resend HTTPS API — zero-server email transport. With just an API key,
    # users can email out from "onboarding@resend.dev" without any domain,
    # mailbox, or DNS setup. ``resend_from`` is optional; defaults to the
    # Resend shared sender.
    "resend_api_key",
    "resend_from",
    # HuggingFace — optional token for higher rate limits on model scores sync.
    # Free at huggingface.co/settings/tokens. Without it, the Datasets Server
    # API may rate-limit or block the Open LLM Leaderboard sync.
    "hf_api_token",
    # Discovery scheduler auto-start. "1" = run fetch+mine+digest every 24h
    # automatically when the backend lifespan boots. Surfaced in the
    # Notifications panel as a toggle so the user doesn't need shell access.
    "discovery_daily",
    # Study loop scheduler settings. "1" = run autonomous study loop on a
    # fixed cadence. Interval defaults to 24 h; iterations defaults to 15.
    "study_loop_daily",
    "study_loop_interval_hours",
    "study_loop_daily_iterations",
]

KNOWN_PROVIDERS = ["openai", "anthropic", "google", "mistral", "ollama"]
_PROVIDERS_KEY = "_provider_prefs"


def _keys_file() -> Path:
    settings = get_settings()
    return Path(settings.data_dir) / ".keys.json"


# ── Spec 092 Stage 1 — credential encryption at rest ──────────────────
#
# The registered credential set (D-092-2): the key names whose values
# are credential-class and are therefore encrypted at rest in store
# format v2. Data, reviewed like KNOWN_KEYS above — a future key joins
# the encrypted class with a one-line registration here. Configuration
# names (hosts, ports, sender addresses, toggles, intervals,
# ``_provider_prefs``) are deliberately NOT in the set and stay
# readable plaintext in the same file. Two KNOWN_KEYS entries are
# identifiers rather than credentials and stay plaintext by the same
# reasoning: ``openalex_email`` and ``unpaywall_email`` are email
# addresses the providers require be sent in cleartext query
# parameters to identify the caller; they confer no access.
# ``ms_graph_client_id`` / ``ms_graph_tenant_id`` / ``smtp_username``
# are likewise identifiers, not secrets. ``glossa_service_credential``
# is registered here although it is not in KNOWN_KEYS: in substance it
# authenticates service calls (``cloud_scope`` resolves it through
# ``get_key``), so a stored value under that name is credential-class.
CREDENTIAL_KEYS = frozenset({
    # LLM / discovery / search provider API keys
    "mistral_api_key",
    "openai_api_key",
    "anthropic_api_key",
    "google_api_key",
    "serp_api_key",
    "news_api_key",
    "brave_search_api_key",
    "semantic_scholar_api_key",
    "core_api_key",
    "uspto_api_key",
    # Academia.edu authenticated-mode session cookie (a bearer credential)
    "academia_session_cookie",
    # SMTP password (the one SMTP secret; host/port/user/from are config)
    "smtp_password",
    # Microsoft Graph long-lived refresh token
    "ms_graph_refresh_token",
    # Resend HTTPS API key
    "resend_api_key",
    # HuggingFace token
    "hf_api_token",
    # Cloud-edition service credential (Spec 083; read via get_key)
    "glossa_service_credential",
})

_ENVELOPE_VERSION = 2
_ENVELOPE_ALG = "AES-256-GCM"
_KEY_BYTES = 32  # AES-256
_NONCE_BYTES = 12  # AES-GCM standard nonce
_KEY_FILE_ENV = "GLOSSA_CREDENTIAL_KEY_FILE"
_KEY_FILE_NAME = "glossa-lab-credential.key"


class CredentialStoreError(Exception):
    """Named error state for the credential store (C092-3).

    Raised when a store file exists but cannot be honoured — the key
    is missing or unusable, a value cannot be decrypted, the file is
    corrupt, or a migration failed. The ``state`` attribute is the
    machine-readable name the settings surface reports; it always
    distinguishes the failure from "no keys configured" (an absent
    store file, which loads as an empty dict without error). The
    store NEVER falls back to parsing an encrypted store as plaintext
    and never presents an undecryptable store as empty.
    """

    state = "credential_store_error"


class CredentialKeyError(CredentialStoreError):
    """The encryption key could not be loaded from its custody file."""

    state = "credential_key_error"


class CredentialKeyMissing(CredentialKeyError):
    """The key file does not exist at the custody location."""

    state = "credential_key_missing"


class CredentialKeyUnreadable(CredentialKeyError):
    """The key file exists but cannot be read (permissions, I/O)."""

    state = "credential_key_unreadable"


class CredentialKeyMalformed(CredentialKeyError):
    """The key file's content is not valid base64."""

    state = "credential_key_malformed"


class CredentialKeyWrongLength(CredentialKeyError):
    """The decoded key is not exactly 32 bytes (AES-256)."""

    state = "credential_key_wrong_length"


class CredentialStoreUnreadable(CredentialStoreError):
    """The store file exists but cannot be read (permissions, I/O)."""

    state = "credential_store_unreadable"


class CredentialStoreCorrupt(CredentialStoreError):
    """The store file is not a well-formed v1/v2 store."""

    state = "credential_store_corrupt"


class CredentialStoreUndecryptable(CredentialStoreError):
    """A stored credential value cannot be decrypted with the loaded
    key (wrong key, or tampered/corrupt ciphertext)."""

    state = "credential_store_undecryptable"


class CredentialStoreMigrationFailed(CredentialStoreError):
    """A legacy-store migration could not be completed or verified;
    the original file's state is named in the message."""

    state = "credential_store_migration_failed"


def _credential_key_file() -> Path:
    """Resolve the D-092-1 key custody location.

    The key lives OUTSIDE ``{data_dir}`` so the program's routine
    data-dir copies (preservation snapshots, migrations) never carry
    it (C092-2). Default: the per-user location beside the data dir —
    ``{data_dir.parent}/glossa-lab-credential.key`` — overridable with
    the ``GLOSSA_CREDENTIAL_KEY_FILE`` environment variable. The file
    holds the base64 encoding of the 32-byte key and is mode 0600,
    created by the operator; the loader never creates it.
    """
    override = os.environ.get(_KEY_FILE_ENV)
    if override:
        return Path(override)
    return Path(get_settings().data_dir).parent / _KEY_FILE_NAME


def _load_credential_key() -> bytes:
    """Load the 32-byte AES-256 key from its custody file.

    This is the only function that touches key material; nothing logs
    the key or any part of it. Each failure mode is a distinct typed
    exception (C092-3): :class:`CredentialKeyMissing`,
    :class:`CredentialKeyUnreadable`, :class:`CredentialKeyMalformed`,
    :class:`CredentialKeyWrongLength`.
    """
    path = _credential_key_file()
    try:
        raw = path.read_bytes()
    except FileNotFoundError as exc:
        raise CredentialKeyMissing(
            f"credential key file not found at {path}; the encrypted "
            "credential store cannot be read without it (stored "
            "credentials are NOT being reported as unset — the key "
            "custody file must be restored, or the credentials "
            "re-entered after placing a new key)"
        ) from exc
    except OSError as exc:
        raise CredentialKeyUnreadable(
            f"credential key file at {path} could not be read: {exc}"
        ) from exc
    try:
        key = base64.b64decode(raw.strip(), validate=True)
    except (binascii.Error, ValueError) as exc:
        raise CredentialKeyMalformed(
            f"credential key file at {path} does not contain valid "
            "base64 key material"
        ) from exc
    if len(key) != _KEY_BYTES:
        raise CredentialKeyWrongLength(
            f"credential key at {path} decodes to {len(key)} bytes; "
            f"exactly {_KEY_BYTES} are required (AES-256)"
        )
    return key


def _is_envelope(value: Any) -> bool:
    """True when ``value`` has the v2 credential envelope shape."""
    return (
        isinstance(value, dict)
        and value.get("v") == _ENVELOPE_VERSION
        and value.get("alg") == _ENVELOPE_ALG
        and isinstance(value.get("nonce"), str)
        and isinstance(value.get("ct"), str)
    )


def _encrypt_value(key: bytes, plaintext: str) -> dict[str, Any]:
    """Encrypt one credential value into its v2 envelope (fresh nonce)."""
    nonce = os.urandom(_NONCE_BYTES)
    ct = AESGCM(key).encrypt(nonce, plaintext.encode("utf-8"), None)
    return {
        "v": _ENVELOPE_VERSION,
        "alg": _ENVELOPE_ALG,
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ct": base64.b64encode(ct).decode("ascii"),
    }


def _decrypt_value(key: bytes, name: str, envelope: dict[str, Any]) -> str:
    """Decrypt one v2 envelope; any failure is the named undecryptable
    state — never a plaintext guess and never an empty value."""
    try:
        nonce = base64.b64decode(envelope["nonce"], validate=True)
        ct = base64.b64decode(envelope["ct"], validate=True)
        return AESGCM(key).decrypt(nonce, ct, None).decode("utf-8")
    except Exception as exc:
        raise CredentialStoreUndecryptable(
            f"stored credential {name!r} cannot be decrypted with the "
            "loaded credential key (wrong key, or the store entry is "
            "corrupt or tampered); no value is served for it"
        ) from exc


def _write_store_verified(target: Path, payload: str) -> None:
    """Write the store through the verified construction (C092-7's
    store leg, hand-rolled in this module for Stage 1; Stage 2 lifts
    it into the verified-write library).

    Temp file in the target's own directory, mode 0600 applied to the
    temp BEFORE the rename (so no window exists where the store sits
    at looser permissions), fsync, atomic rename, then read-back
    verification against the payload. Any failure before the rename
    leaves the previous store byte-identical and raises
    :class:`StateWriteError` naming the target — the F1 discipline:
    a failed write must never destroy the only copy of every stored
    credential at once.
    """
    data = payload.encode("utf-8")
    tmp_name: str | None = None
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(
            dir=str(target.parent), prefix=f".{target.name}.", suffix=".tmp"
        )
        with os.fdopen(fd, "wb") as handle:
            try:
                os.fchmod(handle.fileno(), 0o600)
            except (AttributeError, OSError):
                # Windows has no fchmod; mkstemp's default restrictive
                # mode and the account ACLs govern there.
                pass
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, target)
        tmp_name = None
        if target.read_bytes() != data:
            raise StateWriteError(
                f"verified write to credential store {target} failed: "
                "read-back bytes differ from the payload written"
            )
    except StateWriteError:
        raise
    except Exception as exc:
        raise StateWriteError(
            f"verified write to credential store {target} failed: {exc}"
        ) from exc
    finally:
        if tmp_name is not None:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass


def _read_store_file(f: Path) -> dict[str, Any]:
    """Read and parse the store file. An absent file is an empty
    store (``{}`` — "no keys configured"); an existing file that
    cannot be read or parsed is a named error state, never ``{}``
    (C092-3 retires the old silent-``{}``-on-any-error behaviour)."""
    if not f.exists():
        return {}
    try:
        text = f.read_text(encoding="utf-8")
    except OSError as exc:
        raise CredentialStoreUnreadable(
            f"credential store at {f} could not be read: {exc}"
        ) from exc
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise CredentialStoreCorrupt(
            f"credential store at {f} is not valid JSON; it is "
            "reported as corrupt, not as an empty store"
        ) from exc
    if not isinstance(data, dict):
        raise CredentialStoreCorrupt(
            f"credential store at {f} does not hold a JSON object; "
            "it is reported as corrupt, not as an empty store"
        )
    return data


def _load_keys() -> dict[str, Any]:
    """Load the store, returning plaintext values exactly as callers
    have always seen them (C092-5): credential entries are decrypted
    inside the store; non-credential entries pass through unchanged.

    A store holding any credential entry needs the key — v2 envelopes
    to decrypt, v1 plaintext entries to migrate (T102: the migration
    runs in this same act, through the verified save path, and the
    migrated store is re-read and compared value-by-value before this
    load returns). A credential-free store never consults the key
    (D-092-2: a missing key degrades exactly the credential class).
    """
    f = _keys_file()
    raw = _read_store_file(f)
    if not raw:
        return {}

    needs_key = False
    needs_migration = False
    for name in CREDENTIAL_KEYS:
        if name not in raw:
            continue
        value = raw[name]
        if isinstance(value, str):
            needs_key = True
            needs_migration = True
        elif _is_envelope(value):
            needs_key = True
        else:
            raise CredentialStoreCorrupt(
                f"credential entry {name!r} in {f} is neither a v1 "
                "plaintext string nor a v2 envelope; it is reported "
                "as corrupt and no value is served for it"
            )
    if not needs_key:
        return dict(raw)

    key = _load_credential_key()
    plain: dict[str, Any] = dict(raw)
    for name in CREDENTIAL_KEYS:
        value = raw.get(name)
        if _is_envelope(value):
            plain[name] = _decrypt_value(key, name, value)

    if needs_migration:
        _migrate_store(f, plain)
    return plain


def _migrate_store(f: Path, plain: dict[str, Any]) -> None:
    """Re-save a legacy plaintext store in v2 form and prove it by
    re-reading (C092-4). Any failure leaves the original file
    byte-untouched where the failure precedes the rename, and is
    raised as the named migration state — there is no half-migrated
    state."""
    try:
        _save_keys(plain)
    except StateWriteError as exc:
        raise CredentialStoreMigrationFailed(
            f"legacy credential store at {f} could not be migrated: "
            f"{exc}; the original file is untouched"
        ) from exc
    reread = _load_keys()
    if reread != plain:
        raise CredentialStoreMigrationFailed(
            f"legacy credential store at {f} was re-saved in v2 form "
            "but the post-migration re-read does not match the "
            "pre-migration values; the store is reported as failed, "
            "not trusted"
        )


def _save_keys(data: dict[str, Any]) -> None:
    """Persist the store. Callers pass plaintext values (as they
    always have); credential-class entries are encrypted into v2
    envelopes here, inside the store, and every write goes through
    the verified construction. A save carrying credential values
    requires the key — without it the save is refused with the named
    key state rather than writing a credential in plaintext."""
    f = _keys_file()
    out: dict[str, Any] = dict(data)
    credential_names = [n for n in CREDENTIAL_KEYS if n in out]
    if credential_names:
        key = _load_credential_key()
        for name in credential_names:
            value = out[name]
            if not isinstance(value, str):
                raise CredentialStoreCorrupt(
                    f"refusing to persist credential entry {name!r}: "
                    "its value is not a string, and a credential is "
                    "never written in a non-envelope form"
                )
            out[name] = _encrypt_value(key, value)
    _write_store_verified(f, json.dumps(out, indent=2))
    # Restrict permissions on Unix (the rename already lands the
    # temp's 0600; this keeps the standing discipline for filesystems
    # where the rename preserved a looser mode).
    try:
        f.chmod(0o600)
    except Exception:
        pass


# Values that look like a real key but are actually placeholders. We treat
# them as "not configured" so a fetcher / verifier never POSTs them to a
# real provider (which would 401/422). Match by exact-equal OR by prefix
# so common forms like ``dummy-news``, ``dummy_serp``, ``placeholder-xxx``,
# ``your-api-key-here``, ``<insert key>`` are all caught.
_PLACEHOLDER_EQUAL = {
    "", "none", "null", "undefined", "<your-key>", "<your-api-key>",
    "your-api-key-here", "your_api_key_here", "replace-me", "replace_me",
    "changeme", "change-me", "todo", "tbd", "xxx", "xxxx", "xxxxxxxx",
}
_PLACEHOLDER_PREFIX = (
    "dummy", "placeholder", "<insert", "<your", "sk-xxx", "your-", "your_",
)
_log_warned: set[str] = set()


def _is_placeholder(value: str | None) -> bool:
    if not value:
        return True
    v = value.strip().lower()
    if not v or v in _PLACEHOLDER_EQUAL:
        return True
    return any(v.startswith(p) for p in _PLACEHOLDER_PREFIX)


def get_key(key_name: str) -> str | None:
    """Return the plaintext value of a stored key (for internal use only).

    Resolution order: process env (UPPERCASE name) -> stored ``.keys.json``.
    Placeholder values (``dummy-*``, ``your-api-key-here`` etc.) are
    treated as if no key were set so callers fall through to the next
    source or skip the request entirely.
    """
    import logging  # noqa: PLC0415

    env_name = key_name.upper()
    env_val = os.environ.get(env_name)
    # Always strip whitespace (trailing \n, spaces etc.) from env vars.
    # Tools like direnv, setx, or copy-paste can silently add whitespace
    # that corrupts Authorization headers and query parameters.
    if env_val:
        env_val = env_val.strip()
    if env_val and not _is_placeholder(env_val):
        return env_val
    if env_val and _is_placeholder(env_val) and env_name not in _log_warned:
        # Surface this once: a polluted env variable beats the stored value
        # and would otherwise cause silent provider 401s with no clue why.
        _log_warned.add(env_name)
        logging.getLogger("glossa_lab.api.settings").warning(
            "Ignoring placeholder env value for %s (%r); falling back to stored key. "
            "Run `Remove-Item Env:%s` in your shell or `setx %s \"\"` to clear it.",
            env_name, env_val, env_name, env_name,
        )
    try:
        stored = _load_keys().get(key_name)
    except CredentialStoreError as exc:
        # C092-3: an undecryptable store serves no credential. The
        # named state itself is reported by the settings surface (and
        # logged here, once per state); get_key's contract to its
        # many callers is a value or None, and env-supplied values
        # above remain resolvable while the store is down.
        if exc.state not in _log_warned:
            _log_warned.add(exc.state)
            logging.getLogger("glossa_lab.api.settings").warning(
                "Credential store unavailable (%s): %s. Stored values "
                "are being served as unset until the store is readable.",
                exc.state, exc,
            )
        return None
    if stored and _is_placeholder(stored):
        return None
    return stored


# ── Verification ─────────────────────────────────────────────────────

_VERIFY_ENDPOINTS: dict[str, dict[str, Any]] = {
    "mistral_api_key": {
        "provider": "Mistral",
        "url": "https://api.mistral.ai/v1/models",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "extra_headers": {},
    },
    "openai_api_key": {
        "provider": "OpenAI",
        "url": "https://api.openai.com/v1/models",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "extra_headers": {},
    },
    "anthropic_api_key": {
        "provider": "Anthropic",
        "url": "https://api.anthropic.com/v1/models",
        "auth_header": "x-api-key",
        "auth_prefix": "",
        "extra_headers": {"anthropic-version": "2023-06-01"},
    },
    "google_api_key": {
        "provider": "Google",
        "url": "https://generativelanguage.googleapis.com/v1beta/models",
        "auth_header": None,  # key goes in query param
        "auth_prefix": "",
        "query_param": "key",
        "extra_headers": {},
    },
    # ── Discovery / search providers ─────────────────────────────────────
    "serp_api_key": {
        "provider": "SerpAPI",
        "url": "https://serpapi.com/account",
        "auth_header": None,
        "auth_prefix": "",
        "query_param": "api_key",
        "extra_headers": {},
    },
    "news_api_key": {
        "provider": "NewsAPI",
        # /v2/sources is the cheapest auth check; returns 200 + sources list
        "url": "https://newsapi.org/v2/sources",
        "auth_header": "X-Api-Key",
        "auth_prefix": "",
        "extra_headers": {},
    },
    "brave_search_api_key": {
        "provider": "Brave Search",
        "url": "https://api.search.brave.com/res/v1/web/search?q=test&count=1",
        "auth_header": "X-Subscription-Token",
        "auth_prefix": "",
        "extra_headers": {"Accept": "application/json"},
    },
    "semantic_scholar_api_key": {
        "provider": "Semantic Scholar",
        # Lightweight search with limit=1 — validates the key + returns rate headers.
        "url": "https://api.semanticscholar.org/graph/v1/paper/search?query=test&limit=1&fields=paperId",
        "auth_header": "x-api-key",
        "auth_prefix": "",
        "extra_headers": {},
    },
    "openalex_email": {
        "provider": "OpenAlex",
        # A minimal search with mailto= — 200 means the polite pool accepted us.
        "url": "https://api.openalex.org/works?search=test&per-page=1",
        "auth_header": None,
        "auth_prefix": "",
        "query_param": "mailto",
        "extra_headers": {},
    },
    "core_api_key": {
        "provider": "CORE (core.ac.uk)",
        # Trailing slash required — without it the API returns 301 and Python's
        # urllib drops the Authorization header on the redirect, causing 403.
        "url": "https://api.core.ac.uk/v3/search/works/?q=test&limit=1",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "extra_headers": {},
    },
    "unpaywall_email": {
        "provider": "Unpaywall",
        # DOI lookup is far more reliable than /v2/search for verification.
        # Uses a well-known DOI (a Nature paper); returns 200 + oa_status.
        # /v2/search can return 500 on some queries — avoid it for verify.
        "url": "https://api.unpaywall.org/v2/10.1038/nature12373",
        "auth_header": None,
        "auth_prefix": "",
        "query_param": "email",
        "extra_headers": {},
    },
    # ── Patent data sources ──────────────────────────────────────────────
    # PatentsView: API shut down March 2026 — no verify endpoint.
    "uspto_api_key": {
        "provider": "USPTO (ODP)",
        "url": "https://api.uspto.gov/api/v1/patent/status-codes?limit=1",
        "auth_header": "X-API-KEY",
        "auth_prefix": "",
        "extra_headers": {},
    },
    "hf_api_token": {
        "provider": "HuggingFace",
        "url": "https://huggingface.co/api/whoami-v2",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "extra_headers": {},
    },
}


class VerifyRequest(BaseModel):
    key_name: str
    key_value: str | None = None  # if provided, verifies this value instead of stored


@router.post("/verify-key")
async def verify_key(body: VerifyRequest) -> dict[str, Any]:
    """Test an API key against the provider's models endpoint.

    Uses the stored key unless key_value is supplied directly.
    Returns {valid, provider, message}.
    """
    key_name = body.key_name
    if key_name not in KNOWN_KEYS:
        return {"valid": False, "provider": "", "message": f"Unknown key: {key_name}"}

    ep = _VERIFY_ENDPOINTS.get(key_name)
    if not ep:
        return {"valid": False, "provider": "", "message": "No verification endpoint configured"}

    # Resolve the key value
    key_val = body.key_value or get_key(key_name)
    if not key_val:
        return {
            "valid": False,
            "provider": ep["provider"],
            "message": "Key is not set. Enter and save the key first.",
        }

    # Build the request
    url = ep["url"]
    if ep["auth_header"] is None:
        # Key goes in a query parameter (Google, SerpAPI, etc.)
        # URL-encode the value.
        # Use safe='@' to keep @ unencoded in emails — some APIs (including
        # Unpaywall) don't decode %40 back to @ correctly on their end.
        import urllib.parse as _up  # noqa: PLC0415
        param = ep.get("query_param", "key")
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}{param}={_up.quote(str(key_val).strip(), safe='@')}"

    headers: dict[str, str] = {"Accept": "application/json"}
    if ep["auth_header"]:
        headers[ep["auth_header"]] = ep["auth_prefix"] + key_val
    headers.update(ep.get("extra_headers", {}))

    try:
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            # Capture rate-limit headers from the verify response.
            rl_limit = (
                resp.headers.get("X-RateLimit-Limit")
                or resp.headers.get("RateLimit-Limit")
            )
            rl_remaining = (
                resp.headers.get("X-RateLimit-Remaining")
                or resp.headers.get("RateLimit-Remaining")
            )
        if status == 200:
            msg = f"{ep['provider']} key is valid."
            if rl_limit:
                msg += f" Rate limit: {rl_limit}/window"
                if rl_remaining:
                    msg += f", {rl_remaining} remaining"
                msg += "."
            # Record in the rate tracker so the /sources API shows the limit.
            try:
                from glossa_lab.discovery.fetchers.base import get_rate_tracker  # noqa: PLC0415
                tracker = get_rate_tracker()
                # Map key_name → source name for the tracker.
                src_map = {
                    "semantic_scholar_api_key": "semanticscholar",
                    "openalex_email": "openalex",
                    "brave_search_api_key": "brave",
                    "news_api_key": "newsapi",
                    "serp_api_key": "serpapi",
                    "uspto_api_key": "uspto",
                    "core_api_key": "core",
                    "unpaywall_email": "unpaywall",
                }
                src = src_map.get(key_name)
                if src:
                    info: dict[str, object] = {}
                    if rl_limit:
                        try: info["limit"] = int(rl_limit)
                        except ValueError: info["limit"] = rl_limit
                    if rl_remaining:
                        try: info["remaining"] = int(rl_remaining)
                        except ValueError: info["remaining"] = rl_remaining
                    if info:
                        tracker.record_request(src, ok=True, rate_limit_info=info)
            except Exception:  # noqa: BLE001
                pass
            return {
                "valid": True,
                "provider": ep["provider"],
                "message": msg,
            }
        return {
            "valid": False,
            "provider": ep["provider"],
            "message": f"Unexpected status {status}.",
        }
    except urllib.error.HTTPError as exc:
        code = exc.code
        provider = ep["provider"]

        # ── 429: key valid but quota exhausted ──────────────────────────────
        if code == 429:
            return {
                "valid": True, "provider": provider,
                "message": (
                    f"{provider} key is valid — daily quota temporarily exhausted "
                    "(HTTP 429). Requests resume automatically once the window resets."
                ),
            }

        # ── 422: key accepted but request semantically invalid ───────────────
        # Unpaywall returns 422 when the email param looks like a test address.
        # The email itself IS being sent and processed — 422 means the API is
        # reachable and the email format is valid; the user's real email will work.
        if code == 422:
            return {
                "valid": True, "provider": provider,
                "message": (
                    f"{provider} email is accepted (HTTP 422 = Unpaywall received it "
                    "but flagged the test address). Your real email will be accepted."
                ),
            }

        # ── 401 / 403: key rejected — but check for maintenance first ────────
        if code in (401, 403):
            # For CORE specifically, a 403 might mean scheduled maintenance, not
            # an invalid key. Do a lightweight keyless probe to distinguish.
            if key_name == "core_api_key":
                try:
                    probe = urllib.request.Request(
                        ep["url"], headers={"Accept": "application/json"}, method="GET"
                    )
                    with urllib.request.urlopen(probe, timeout=6) as r2:
                        if r2.status == 200:
                            # API is reachable without auth — key is bad or not yet activated.
                            return {
                                "valid": False, "provider": provider,
                                "message": (
                                    f"CORE API is online but rejected this key (HTTP {code}). "
                                    "Keys are emailed after registration and may take a few "
                                    "minutes to activate. If you just registered, wait and retry."
                                ),
                            }
                except Exception:  # noqa: BLE001
                    pass
                # Keyless probe also failed — likely maintenance.
                return {
                    "valid": False, "provider": provider,
                    "message": (
                        "CORE API is currently unavailable (HTTP 403 — scheduled maintenance). "
                        "Check https://core.ac.uk/services/api for status. "
                        "Your key may still be valid."
                    ),
                }
            return {
                "valid": False, "provider": provider,
                "message": f"Invalid key (HTTP {code}: Unauthorized).",
            }

        # ── 5xx: provider-side server error, key may still be valid ─────────
        if code >= 500:
            return {
                "valid": False, "provider": provider,
                "message": (
                    f"{provider} returned a server error (HTTP {code}). "
                    "This is a temporary issue on their end, not a problem with your key. "
                    "Try again in a few minutes."
                ),
            }

        return {
            "valid": False, "provider": provider,
            "message": f"HTTP error {code}: {exc.reason}.",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "valid": False,
            "provider": ep["provider"],
            "message": f"Connection error: {exc}",
        }


@router.get("")
async def read_settings() -> dict[str, Any]:
    """Return settings with masked key values — never exposes plaintext."""
    store_error: dict[str, str] | None = None
    try:
        stored = _load_keys()
    except CredentialStoreError as exc:
        # C092-3: the surface reports the named error state. No stored
        # value is served; env-sourced keys still report truthfully,
        # and the ``store_error`` field distinguishes this state from
        # "no keys configured" (an absent store, which carries no
        # ``store_error`` at all).
        stored = {}
        store_error = {"state": exc.state, "detail": str(exc)}
    keys_status: dict[str, Any] = {}
    for k in KNOWN_KEYS:
        # Env var takes precedence
        env_val = os.environ.get(k.upper())
        if env_val:
            keys_status[k] = {"set": True, "source": "env", "masked": _MASK}
        elif k in stored and stored[k]:
            keys_status[k] = {"set": True, "source": "stored", "masked": _MASK}
        else:
            keys_status[k] = {"set": False, "source": None, "masked": ""}

    stored_providers = stored.get(_PROVIDERS_KEY, {})
    body: dict[str, Any] = {
        "keys": keys_status,
        "providers": stored_providers,
        "data_dir": str(get_settings().data_dir),
    }
    if store_error is not None:
        body["store_error"] = store_error
    return body


@router.put("")
async def update_settings(body: dict[str, Any]) -> dict[str, Any]:
    """Update stored settings. Pass empty string to clear a key."""
    try:
        stored = _load_keys()
    except CredentialStoreError as exc:
        # A write never proceeds from an unreadable store: starting
        # from a silently-empty dict would destroy every stored
        # credential on save. Refuse with the named state (C092-3).
        raise HTTPException(
            status_code=503, detail=f"{exc.state}: {exc}"
        ) from exc
    updated: list[str] = []

    for k in KNOWN_KEYS:
        if k in body:
            val = body[k].strip()
            if val:
                stored[k] = val
                # Also set in current process environment so pipelines pick it up
                os.environ[k.upper()] = val
                updated.append(k)
            elif val == "" and k in stored:
                # Clear the key
                del stored[k]
                os.environ.pop(k.upper(), None)
                updated.append(k)

    # Provider preferences (enable/model-selection state)
    updated_providers: list[str] = []
    if "providers" in body and isinstance(body.get("providers"), dict):
        prefs = stored.get(_PROVIDERS_KEY, {})
        for pid, pdata in body["providers"].items():
            if pid in KNOWN_PROVIDERS and isinstance(pdata, dict):
                prefs[pid] = pdata
                updated_providers.append(pid)
        stored[_PROVIDERS_KEY] = prefs

    try:
        _save_keys(stored)
    except CredentialStoreError as exc:
        raise HTTPException(
            status_code=503, detail=f"{exc.state}: {exc}"
        ) from exc

    return {
        "updated": updated,
        "updated_providers": updated_providers,
        "message": f"{len(updated)} key(s) and {len(updated_providers)} provider(s) updated",
    }

"""Priority register — Spec 029 Phase C (FR-029-11; F029-C08; OD-6).

The register is the program's priority/credit instrument for an
external scholar's early reading (assessment finding P7: the
instrument was ABSENT). It implements the owner's adjudicated
OD-6 decision (``specs/029-tao-claim-lifecycle/adjudication.md``,
2026-10-12, verbatim):

    "priority register PUBLIC at intake with content sealed by
    hash: claimant + timestamp + hash published; unseals on
    claimant publication or chosen date, default 24 months,
    extendable once"

and the frozen Phase C text (``tasks.md`` C1, which governs):

    "Intake API + store: issuance on record completeness alone
    (no score, stage, or verdict field exists on an entry);
    public record = claimant + server timestamp + SHA-256 of
    the reading; content sealed until claimant publication or
    reveal date (default 24 months, extendable once as a dated
    record); credit display invariant under later program
    assessment — tested."

``plan.md`` §2.1 adds the storage form: "the reading's content
is stored sealed and is revealed only when the claimant
publishes or at a claimant-chosen reveal date". This module
therefore stores the content **sealed**, not in plaintext and
not hash-only:

* **Hash (the public seal).** ``content_hash`` is the SHA-256
  of the canonical claim content (see
  :func:`canonical_content_bytes`). The public record —
  :func:`public_record` — is exactly three fields: claimant
  (the public identity the claimant declares for
  publication), the server timestamp, and that hash. No
  content, no contact detail, and no score / stage / verdict
  field exists on a register entry, in any serialization.
* **Sealed storage.** The canonical content bytes are stored
  only as a sealed envelope: an HMAC-SHA256 counter-mode
  keystream XOR (stdlib only — no new dependency) with an
  HMAC integrity tag, under a seal key that is **not** part
  of the register record. In the API store the key lives in
  a separate file (mode 0600) beside the store file, never
  inside it and never serialized. Opening an envelope whose
  tag does not verify fails closed.
* **Verification.** Unsealing by publication does not trust
  the stored envelope: the claimant presents content, its
  canonical hash is recomputed, and it is accepted only when
  it matches the published hash exactly — a one-byte
  difference in the reading or its evidence does not verify.

Canonicalization (``spec029-priority-canonical-v1``): the
claim content is the mapping ``{"reading": <reading>,
"evidence": [<evidence>, ...]}`` serialized as JSON with
sorted keys, separators ``(",", ":")``, ``ensure_ascii=False``,
encoded UTF-8. There is **no** case-folding, whitespace, or
punctuation normalisation (contrast the Phase I proposition
fingerprint, whose job is collision): priority must bind the
exact content the claimant filed, so every byte of the
reading and of each evidence item is preserved and any
difference changes the hash.

Rules implemented here (C1–C3):

* **Completeness alone.** Intake requires exactly: a claimant
  public identity, a claimant contact (kept private — stored
  on the internal record for correspondence only, per plan
  §5/§V and rule H24; never in any serialization), a
  non-empty reading, and a non-empty evidence list. Nothing
  else is required, and no assessment field is ever written.
* **Server timestamp.** ``registered_at`` is stamped by the
  register at intake from its clock (injectable for tests);
  a claimant-asserted timestamp in the intake payload is
  ignored — it is never read.
* **Unseal triggers (OD-6).** (a) claimant publication:
  :meth:`PriorityRegister.unseal_by_publication` verifies
  presented content against the published hash and records
  the presentation as a dated history event; (b) reveal
  date: :meth:`PriorityRegister.unseal_due` (also invoked
  when entries are read through the API) unseals every
  sealed entry whose reveal date has been reached, opening
  its sealed envelope and recording a dated event.
* **Reveal date.** Claimant-chosen at intake, or the
  default of 24 months from the server timestamp when none
  is chosen. It must lie after the intake timestamp.
* **Extension: once only.** :meth:`PriorityRegister.extend_reveal_date`
  extends the reveal date (it must move it later) and
  records the extension as a dated history event. A second
  extension attempt — and any extension attempt on an
  unsealed entry — is **refused and recorded**: a dated
  ``extension_refused`` event is appended before the error
  is raised, so the refusal itself is part of the register.
* **Append-only.** There is no edit or delete path: entries
  are never removed, sealed fields are never rewritten, and
  every transition (intake, extension, refused extension,
  refused unseal presentation, unseal, supersession) appends
  a dated event to the entry's ``history``. A correction is
  a **new** entry whose intake names the entry it
  ``supersedes``; the superseded entry gains a dated
  ``superseded`` history event and keeps its original
  public record — its credit display does not change.
* **Credit invariant.** The public record (the credit
  display) is a function of claimant + server timestamp +
  hash only. Later events — extension, unseal, supersession,
  or any program assessment of the reading recorded
  elsewhere — never change it.

The clock is injectable everywhere (a ``clock`` callable on
the register, overridable per call with ``now=``) so no test
depends on the wall clock.

Scope boundary (hard limit of this phase): machinery only.
No real priority claim is filed by this phase; the register
store is runtime state (``.glossa-state/``, gitignored) and
every fixture in the tests is obviously synthetic.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import hmac
import json
import os
import secrets
import uuid
from calendar import monthrange
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

# ── Vocabulary ────────────────────────────────────────────────────────────

HASH_ALGORITHM = "sha256"
CANONICALIZATION = "spec029-priority-canonical-v1"
DEFAULT_REVEAL_MONTHS = 24

#: Fields an intake payload must carry for an entry to issue
#: (record completeness — and nothing else — gates issuance).
REQUIRED_INTAKE_FIELDS: tuple[str, ...] = (
    "claimant", "claimant_contact", "reading", "evidence",
)

#: Lane-1 / assessment field names that must never exist on a
#: register entry (issuance implies no assessment, FR-029-11).
FORBIDDEN_ENTRY_FIELDS: tuple[str, ...] = (
    "score", "aee_score", "lane1_score", "stage", "stage_source",
    "stage_as_of", "verdict", "claim_status", "confidence", "band",
)

Clock = Callable[[], datetime]


class PriorityRegisterError(ValueError):
    """A register operation was refused (fail-closed)."""


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _as_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _parse_timestamp(value: Any, *, what: str) -> datetime:
    if isinstance(value, datetime):
        return _as_utc(value)
    if isinstance(value, str) and value.strip():
        text = value.strip()
        try:
            # A bare date is read as the start of that day, UTC.
            if len(text) == 10:
                return datetime.fromisoformat(text).replace(tzinfo=timezone.utc)
            return _as_utc(datetime.fromisoformat(text.replace("Z", "+00:00")))
        except ValueError as exc:
            raise PriorityRegisterError(f"{what} is not an ISO timestamp: {value!r}") from exc
    raise PriorityRegisterError(f"{what} is required (ISO timestamp or date)")


def add_months(dt: datetime, months: int) -> datetime:
    """*dt* shifted by *months* calendar months (day clamped)."""
    month_index = (dt.year * 12 + (dt.month - 1)) + months
    year, month0 = divmod(month_index, 12)
    month = month0 + 1
    day = min(dt.day, monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


# ── Canonical content + hash ──────────────────────────────────────────────

def canonical_content_bytes(reading: Any, evidence: Iterable[Any] | None) -> bytes:
    """The canonical bytes of a claim's content (see module docstring).

    The reading and every evidence item are preserved byte-for-byte
    (as their JSON string forms); keys are sorted and separators
    fixed so the same content always hashes identically.
    """
    ev = [str(e) for e in (evidence or [])]
    payload = {"evidence": ev, "reading": reading if isinstance(reading, str) else str(reading)}
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")


def content_hash(reading: Any, evidence: Iterable[Any] | None) -> str:
    """SHA-256 of the canonical claim content."""
    return hashlib.sha256(canonical_content_bytes(reading, evidence)).hexdigest()


def verify_content(entry: dict[str, Any], reading: Any, evidence: Iterable[Any] | None) -> bool:
    """True when presented content hashes to the entry's published hash.

    Discriminating: a one-byte difference in the reading or in any
    evidence item does not verify.
    """
    return hmac.compare_digest(content_hash(reading, evidence), str(entry.get("content_hash") or ""))


# ── Sealed storage (stdlib HMAC-SHA256 counter-mode XOR + HMAC tag) ──────

def _keystream(key: bytes, nonce: bytes, length: int) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < length:
        out.extend(hmac.new(key, nonce + counter.to_bytes(8, "big"), hashlib.sha256).digest())
        counter += 1
    return bytes(out[:length])


def seal_content(plaintext: bytes, key: bytes) -> dict[str, str]:
    """Seal *plaintext* under *key*; returns the envelope (no plaintext)."""
    if not key:
        raise PriorityRegisterError("a seal key is required to store content sealed")
    nonce = secrets.token_bytes(16)
    stream = _keystream(key, nonce, len(plaintext))
    ciphertext = bytes(a ^ b for a, b in zip(plaintext, stream))
    tag = hmac.new(key, b"spec029-seal-v1" + nonce + ciphertext, hashlib.sha256).hexdigest()
    return {
        "sealed_format": "spec029-sealed-v1",
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
        "tag": tag,
    }


def open_sealed(envelope: dict[str, Any], key: bytes) -> bytes:
    """Open a sealed envelope; a tampered envelope fails closed."""
    if not isinstance(envelope, dict) or envelope.get("sealed_format") != "spec029-sealed-v1":
        raise PriorityRegisterError("not a spec029 sealed envelope")
    nonce = base64.b64decode(str(envelope.get("nonce") or ""))
    ciphertext = base64.b64decode(str(envelope.get("ciphertext") or ""))
    expected = hmac.new(key, b"spec029-seal-v1" + nonce + ciphertext, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, str(envelope.get("tag") or "")):
        raise PriorityRegisterError("sealed envelope integrity tag does not verify — refusing to open")
    stream = _keystream(key, nonce, len(ciphertext))
    return bytes(a ^ b for a, b in zip(ciphertext, stream))


# ── Serializations ────────────────────────────────────────────────────────

def public_record(entry: dict[str, Any]) -> dict[str, Any]:
    """The PUBLIC record / credit display of an entry (OD-6, C1).

    Exactly three fields: claimant (the public identity the
    claimant declared for publication), the server timestamp,
    and the SHA-256 of the reading. This is invariant under
    every later event, including any later program assessment
    of the reading — it is a function of these three values
    alone.
    """
    return {
        "claimant": entry.get("claimant"),
        "timestamp": entry.get("registered_at"),
        "content_hash": entry.get("content_hash"),
    }


def serialize_entry(entry: dict[str, Any]) -> dict[str, Any]:
    """The register's API serialization of one entry.

    Never carries: the sealed envelope, the seal key, the
    claimant's contact, or — while the entry is sealed — the
    content in any form. The content appears only after the
    entry has unsealed, as the revealed ``content`` recorded
    by the unseal event. No score / stage / verdict field
    exists on an entry, here or anywhere.
    """
    out: dict[str, Any] = {
        "entry_id": entry.get("entry_id"),
        "public_record": public_record(entry),
        "claimant": entry.get("claimant"),
        "registered_at": entry.get("registered_at"),
        "timestamp": entry.get("registered_at"),
        "content_hash": entry.get("content_hash"),
        "hash_algorithm": entry.get("hash_algorithm"),
        "canonicalization": entry.get("canonicalization"),
        "claim_id": entry.get("claim_id"),
        "status": entry.get("status"),
        "sealed": entry.get("status") != "unsealed",
        "reveal_date": entry.get("reveal_date"),
        "extended": bool(entry.get("extended")),
        "supersedes": entry.get("supersedes"),
        "superseded_by": entry.get("superseded_by"),
        "history": copy.deepcopy(entry.get("history") or []),
    }
    if entry.get("status") == "unsealed":
        out["content"] = copy.deepcopy(entry.get("revealed_content"))
        out["unsealed_at"] = entry.get("unsealed_at")
        out["unseal_trigger"] = entry.get("unseal_trigger")
    else:
        out["content"] = None
    return out


# ── The register ──────────────────────────────────────────────────────────

class PriorityRegister:
    """An append-only priority register (in-memory core + JSON store)."""

    def __init__(
        self,
        entries: list[dict[str, Any]] | None = None,
        *,
        seal_key: bytes,
        clock: Clock | None = None,
    ) -> None:
        if not seal_key:
            raise PriorityRegisterError("a seal key is required")
        self._seal_key = bytes(seal_key)
        self._clock: Clock = clock or _utcnow
        self.entries: list[dict[str, Any]] = copy.deepcopy(entries or [])

    # -- plumbing ----------------------------------------------------------

    def _now(self, now: datetime | None) -> datetime:
        return _as_utc(now) if now is not None else _as_utc(self._clock())

    def get(self, entry_id: str) -> dict[str, Any]:
        for entry in self.entries:
            if entry.get("entry_id") == entry_id:
                return entry
        raise PriorityRegisterError(f"no priority-register entry {entry_id!r}")

    def _append_history(self, entry: dict[str, Any], event: str, ts: datetime, **details: Any) -> None:
        history = entry.setdefault("history", [])
        record: dict[str, Any] = {"event": event, "timestamp": ts.isoformat()}
        record.update(details)
        history.append(record)

    # -- C1: intake ---------------------------------------------------------

    def register(
        self,
        *,
        claimant: Any = None,
        claimant_contact: Any = None,
        reading: Any = None,
        evidence: Iterable[Any] | None = None,
        claim_id: str | None = None,
        reveal_date: Any = None,
        supersedes: str | None = None,
        now: datetime | None = None,
        **_ignored: Any,
    ) -> dict[str, Any]:
        """File a reading at intake and return the new entry.

        Issuance is on record completeness alone. Extra payload
        fields — including any claimant-asserted timestamp and
        any score / stage / verdict — are ignored and never
        stored: the timestamp is server-stamped here, and no
        assessment field exists on an entry.
        """
        ev = [str(e) for e in (evidence or []) if str(e).strip()]
        errors: list[str] = []
        if not str(claimant or "").strip():
            errors.append("claimant (the public identity declared for publication) is required")
        if not str(claimant_contact or "").strip():
            errors.append("claimant_contact is required (kept private; correspondence only)")
        if not isinstance(reading, str) or not reading.strip():
            errors.append("reading is required (non-empty)")
        if not ev:
            errors.append("evidence is required (a non-empty list)")
        if errors:
            raise PriorityRegisterError("incomplete priority-register intake: " + "; ".join(errors))

        ts = self._now(now)
        if reveal_date is not None:
            reveal = _parse_timestamp(reveal_date, what="reveal_date")
            if reveal <= ts:
                raise PriorityRegisterError("reveal_date must lie after the intake timestamp")
        else:
            reveal = add_months(ts, DEFAULT_REVEAL_MONTHS)

        superseded_entry = None
        if supersedes:
            superseded_entry = self.get(str(supersedes))

        canonical = canonical_content_bytes(reading, ev)
        entry: dict[str, Any] = {
            "entry_id": f"PR-{uuid.uuid4().hex[:16]}",
            "claimant": str(claimant).strip(),
            # Private: correspondence only (plan §5/§V, H24). Stored on
            # the internal record; never in any serialization.
            "claimant_contact": str(claimant_contact).strip(),
            "registered_at": ts.isoformat(),
            "content_hash": hashlib.sha256(canonical).hexdigest(),
            "hash_algorithm": HASH_ALGORITHM,
            "canonicalization": CANONICALIZATION,
            "claim_id": str(claim_id) if claim_id else None,
            "status": "sealed",
            "reveal_date": reveal.isoformat(),
            "extended": False,
            "supersedes": str(supersedes) if supersedes else None,
            "superseded_by": None,
            "sealed_content": seal_content(canonical, self._seal_key),
            "history": [],
        }
        self._append_history(
            entry, "registered", ts,
            reveal_date=entry["reveal_date"],
            default_reveal_applied=reveal_date is None,
            supersedes=entry["supersedes"],
        )
        self.entries.append(entry)
        if superseded_entry is not None:
            superseded_entry["superseded_by"] = entry["entry_id"]
            self._append_history(
                superseded_entry, "superseded", ts, superseded_by=entry["entry_id"],
            )
        return entry

    # -- C2: extension (once only) ------------------------------------------

    def extend_reveal_date(
        self,
        entry_id: str,
        new_reveal_date: Any,
        *,
        now: datetime | None = None,
    ) -> dict[str, Any]:
        """Extend an entry's reveal date — once only, as a dated record.

        A refused extension (second attempt, an attempt on an
        unsealed entry, or a date that does not move the reveal
        later) is recorded in the entry's history before the
        refusal is raised: the refusal is part of the register.
        """
        entry = self.get(entry_id)
        ts = self._now(now)
        try:
            new_reveal = _parse_timestamp(new_reveal_date, what="new_reveal_date")
        except PriorityRegisterError as exc:
            self._append_history(entry, "extension_refused", ts, reason=str(exc))
            raise
        reason = None
        if entry.get("status") == "unsealed":
            reason = "entry is already unsealed; there is no reveal date to extend"
        elif entry.get("extended"):
            reason = "reveal date has already been extended once (OD-6: extendable once)"
        elif new_reveal <= _parse_timestamp(entry["reveal_date"], what="reveal_date"):
            reason = "new reveal date does not move the reveal later"
        if reason is not None:
            self._append_history(entry, "extension_refused", ts, reason=reason)
            raise PriorityRegisterError(f"extension refused: {reason}")
        previous = entry["reveal_date"]
        entry["reveal_date"] = new_reveal.isoformat()
        entry["extended"] = True
        self._append_history(
            entry, "reveal_extended", ts,
            previous_reveal_date=previous, new_reveal_date=entry["reveal_date"],
        )
        return entry

    # -- C2: unseal triggers --------------------------------------------------

    def _mark_unsealed(
        self, entry: dict[str, Any], ts: datetime, trigger: str, revealed: dict[str, Any],
        **details: Any,
    ) -> dict[str, Any]:
        entry["status"] = "unsealed"
        entry["unsealed_at"] = ts.isoformat()
        entry["unseal_trigger"] = trigger
        entry["revealed_content"] = revealed
        self._append_history(entry, "unsealed", ts, trigger=trigger, **details)
        return entry

    def _open_entry_content(self, entry: dict[str, Any]) -> dict[str, Any]:
        raw = open_sealed(entry["sealed_content"], self._seal_key)
        content = json.loads(raw.decode("utf-8"))
        if not verify_content(entry, content.get("reading"), content.get("evidence")):
            raise PriorityRegisterError(
                "sealed content does not hash to the entry's published hash — refusing to reveal"
            )
        return content

    def unseal_by_publication(
        self,
        entry_id: str,
        *,
        reading: Any = None,
        evidence: Iterable[Any] | None = None,
        now: datetime | None = None,
    ) -> dict[str, Any]:
        """Unseal trigger (a): the claimant publishes.

        The claimant presents the content; it unseals the entry
        only when its canonical hash matches the hash published
        at intake. A mismatched presentation is refused **and
        recorded** (a dated ``unseal_refused`` history event);
        the entry stays sealed.
        """
        entry = self.get(entry_id)
        ts = self._now(now)
        if entry.get("status") == "unsealed":
            raise PriorityRegisterError("entry is already unsealed")
        presented_hash = content_hash(reading, evidence)
        if not verify_content(entry, reading, evidence):
            self._append_history(
                entry, "unseal_refused", ts, trigger="claimant_publication",
                presented_content_hash=presented_hash,
                reason="presented content does not hash to the published content_hash",
            )
            raise PriorityRegisterError(
                "unseal refused: presented content does not hash to the "
                "published content_hash (one-byte differences do not verify)"
            )
        revealed = json.loads(canonical_content_bytes(reading, evidence).decode("utf-8"))
        return self._mark_unsealed(
            entry, ts, "claimant_publication", revealed,
            presented_content_hash=presented_hash,
        )

    def unseal_due(self, *, now: datetime | None = None) -> list[dict[str, Any]]:
        """Unseal trigger (b): the reveal date has been reached.

        Every still-sealed entry whose reveal date is at or
        before *now* is unsealed by opening its sealed envelope
        (integrity- and hash-checked) and recording a dated
        event. Returns the entries unsealed by this call.
        Idempotent: an already-unsealed entry is untouched.
        """
        ts = self._now(now)
        unsealed: list[dict[str, Any]] = []
        for entry in self.entries:
            if entry.get("status") == "unsealed":
                continue
            reveal = _parse_timestamp(entry["reveal_date"], what="reveal_date")
            if reveal <= ts:
                revealed = self._open_entry_content(entry)
                self._mark_unsealed(entry, ts, "reveal_date", revealed)
                unsealed.append(entry)
        return unsealed

    # -- Queries --------------------------------------------------------------

    def entries_for_claim(self, claim_id: str) -> list[dict[str, Any]]:
        """Entries filed against *claim_id* (for the trail view)."""
        return [e for e in self.entries if e.get("claim_id") == claim_id]

    def public_records(self) -> list[dict[str, Any]]:
        """The public register: one public record per entry."""
        return [public_record(e) for e in self.entries]

    # -- Persistence (API store) ----------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {"entries": copy.deepcopy(self.entries)}

    @classmethod
    def from_dict(cls, data: dict[str, Any], *, seal_key: bytes, clock: Clock | None = None) -> "PriorityRegister":
        return cls(list(data.get("entries") or []), seal_key=seal_key, clock=clock)


def load_or_create_seal_key(key_path: Path) -> bytes:
    """Load the register's seal key, creating it (0600) if absent.

    The key lives beside — never inside — the store file, and
    is never serialized into a register record.
    """
    if key_path.exists():
        return key_path.read_bytes().strip()
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key = secrets.token_hex(32).encode("ascii")
    fd = os.open(str(key_path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(fd, key)
    finally:
        os.close(fd)
    return key


def load_register(store_path: Path, key_path: Path, *, clock: Clock | None = None) -> PriorityRegister:
    """Load the persisted register (an empty one if no store exists yet)."""
    key = load_or_create_seal_key(key_path)
    if store_path.exists():
        data = json.loads(store_path.read_text("utf-8"))
        return PriorityRegister.from_dict(data, seal_key=key, clock=clock)
    return PriorityRegister(seal_key=key, clock=clock)


def save_register(register: PriorityRegister, store_path: Path) -> None:
    """Persist the register store (sealed envelopes only; no key, no plaintext)."""
    store_path.parent.mkdir(parents=True, exist_ok=True)
    store_path.write_text(
        json.dumps(register.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8",
    )

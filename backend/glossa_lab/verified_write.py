"""Verified writes — the repo's supported write path for state that
matters (Spec 092 Stage 2, T201; claims C092-6, C092-7).

This module carries the fleet's safe-write contract into the backend
as a supported library path. The contract's provenance is the agent
tooling at ``~/workspace/system/safe-write/`` (built 2026-10-28,
Python entry ``safe_write.py``), which proves it against the failure
classes this program has actually met: intermittent write denial
(EPERM waves) that is sticky per process lineage, and silent 0-byte
or short landings from writes that report success. The two
implementations are kin by design — same construction, same ladder —
so the behaviour the fleet tooling evidences is the behaviour the
shipped product runs.

The contract, in full:

* temp file in the target's own directory, flushed and fsynced,
  then atomically renamed over the target, then a directory fsync —
  a reader only ever sees the previous complete file or the new
  complete file;
* read-back SHA-256 verification, of the temp file *before* the
  rename (so a silent short or 0-byte land is caught while the
  previous target is still standing — a failed write never destroys
  the previous good target, C092-7) and of the target after it (the
  fleet contract's own read-back);
* a bounded retry ladder whose rounds include a fresh-subprocess
  attempt (``python -m glossa_lab.verified_write --child-write``),
  because write denial is sticky per process lineage and a fresh
  process is a fresh lineage;
* refusal of empty content, before any attempt;
* parents never created — a missing or non-directory parent fails
  through the ladder like any other failure (directory structure is
  the caller's act, never this module's guess);
* one typed error, :class:`VerifiedWriteError`, when every path
  fails — never a bare ``OSError`` escaping to a caller.

One deliberate refinement of the fleet ladder, named here because
the F1 battery pins it: the fresh-subprocess leg engages only when
the local failure carries the write-denial signature (EPERM/EACCES,
or a read-back mismatch — the silent-land signature). A machine-state
failure such as ENOSPC cannot be healed by a fresh process on the
same box — the disk is full for every lineage — so it exhausts the
local ladder and raises, which is exactly the behaviour
``tests/test_atomic_io_disk_full.py`` proves against the settings
store's save path.

Relationship to :mod:`glossa_lab.atomic_io`: that module is the F1
helper (atomicity and a named error, no verification, no ladder) and
remains the right tool for its existing adopters.
:class:`VerifiedWriteError` subclasses its :class:`StateWriteError`
so the settings store's established error surface — the surface
Stage 1's battery asserts — is preserved exactly on this path.
"""

from __future__ import annotations

import errno
import hashlib
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

from glossa_lab.atomic_io import StateWriteError

__all__ = [
    "VerifiedWriteError",
    "WriteReceipt",
    "try_write_once",
    "write_file_verified",
]


class VerifiedWriteError(StateWriteError):
    """A verified write failed on every path the ladder offers.

    The previous target (if any) is byte-identical unless the
    storage stack itself falsified a rename (a landed rename whose
    read-back mismatched on every attempt — the failure is then
    named here, never silent). The message always names the target
    and the last failure the ladder saw.
    """


@dataclass(frozen=True)
class WriteReceipt:
    """The evidence a successful verified write returns."""

    path: Path
    sha256: str
    attempts: int
    via: str  # "local" | "local-retry-N" | "child-N"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _file_matches(path: str, data: bytes) -> bool:
    """Read-back verification: the file's bytes hash to ``data``'s."""
    try:
        with open(path, "rb") as handle:
            back = handle.read()
    except OSError:
        return False
    return len(back) == len(data) and _sha256(back) == _sha256(data)


def _fsync_directory(directory: Path) -> None:
    """Best-effort directory fsync (some platforms cannot fsync a
    directory handle; the rename's durability there rests on the
    filesystem, as in the fleet construction)."""
    try:
        dfd = os.open(str(directory), os.O_RDONLY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    except OSError:
        pass


# The write-denial signature: denial errnos (sticky per process
# lineage under the fleet's EPERM waves) — a read-back mismatch is
# the same signature's other face (the silent land). Only failures
# carrying this signature engage the ladder's fresh-subprocess leg;
# see the module docstring for the reasoning and the F1 pin.
_DENIAL_ERRNOS = frozenset({errno.EPERM, errno.EACCES})


@dataclass
class _Attempt:
    ok: bool
    denial: bool
    detail: str = ""


def _attempt_once(target: Path, data: bytes, mode: int | None) -> _Attempt:
    """One local attempt at the verified construction.

    Never raises: every failure is classified into the returned
    :class:`_Attempt` (``denial`` marks the write-denial signature),
    and the temp file is removed on any failure before the rename.
    """
    directory = target.parent
    tmp_name: str | None = None
    try:
        # mkstemp sits inside the guarded region (the fleet's
        # 2026-10-28 retrofit fix): a missing or non-directory
        # parent makes mkstemp itself raise, and that failure must
        # flow through the same ladder and typed error as any other
        # write failure — never escape raw to callers.
        fd, tmp_name = tempfile.mkstemp(
            dir=str(directory), prefix=f".{target.name}.", suffix=".tmp"
        )
        with os.fdopen(fd, "wb") as handle:
            if mode is not None:
                try:
                    os.fchmod(handle.fileno(), mode)
                except (AttributeError, OSError):
                    # Windows has no fchmod; mkstemp's default
                    # restrictive mode and the account ACLs govern.
                    pass
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        # Verify the temp BEFORE the rename: a silent 0-byte or
        # short land is caught here, while the previous target is
        # still standing (C092-7).
        if not _file_matches(tmp_name, data):
            return _Attempt(
                False,
                True,
                "temp read-back mismatch — the write landed short "
                "or empty (silent-land signature)",
            )
        os.replace(tmp_name, target)
        tmp_name = None
        _fsync_directory(directory)
        # The fleet contract's read-back: what the target now holds
        # must hash to what was written.
        if not _file_matches(str(target), data):
            return _Attempt(
                False,
                True,
                "target read-back mismatch after rename — the "
                "landed bytes differ from the payload",
            )
        return _Attempt(True, False)
    except OSError as exc:
        return _Attempt(False, exc.errno in _DENIAL_ERRNOS, f"{exc}")
    except Exception as exc:  # noqa: BLE001 — classified, never leaked raw
        return _Attempt(False, False, f"unexpected {type(exc).__name__}: {exc}")
    finally:
        if tmp_name is not None:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass


def try_write_once(
    path: str | Path, content: bytes | str, *, mode: int | None = None
) -> bool:
    """A single verified-write attempt (the fleet entry of the same
    name). Returns True only when the target's read-back hashes to
    the payload; empty content is refused (False, nothing written).
    """
    data = content if isinstance(content, bytes) else str(content).encode("utf-8")
    if not data:
        return False
    target = Path(os.path.abspath(os.fspath(path)))
    return _attempt_once(target, data, mode).ok


def _attempt_child(target: Path, data: bytes, mode: int | None) -> bool:
    """One attempt in a fresh subprocess — a fresh process lineage,
    which is the ladder's answer to lineage-sticky write denial.
    The child runs this module's own ``--child-write`` mode.
    """
    mode_arg = "-" if mode is None else oct(mode)
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "glossa_lab.verified_write",
                "--child-write",
                str(target),
                mode_arg,
            ],
            input=data,
            timeout=30,
            capture_output=True,
        )
        return result.returncode == 0
    except Exception:  # noqa: BLE001 — a failed spawn is a failed attempt
        return False


def write_file_verified(
    path: str | Path,
    content: bytes | str,
    *,
    mode: int | None = None,
    retries: int = 3,
) -> WriteReceipt:
    """Write ``content`` to ``path`` under the verified contract.

    ``mode``, when given, is applied to the temp file before the
    rename, so the target never stands at a looser mode than the
    caller asked for. ``retries`` bounds the ladder's rounds (each
    round is at most a fresh-subprocess attempt — denial-signature
    failures only — plus a local attempt). Raises
    :class:`VerifiedWriteError` on empty content (before any
    attempt) or when every path fails.
    """
    data = content if isinstance(content, bytes) else str(content).encode("utf-8")
    target = Path(os.path.abspath(os.fspath(path)))
    if not data:
        raise VerifiedWriteError(
            f"refusing to write empty content to {target}"
        )
    attempts = 0
    last = _attempt_once(target, data, mode)
    attempts += 1
    if last.ok:
        return WriteReceipt(target, _sha256(data), attempts, "local")
    for round_no in range(1, retries + 1):
        time.sleep(min(0.5 * round_no, 2.0))
        if last.denial:
            attempts += 1  # the child attempt is spent either way
            if _attempt_child(target, data, mode):
                return WriteReceipt(
                    target, _sha256(data), attempts, f"child-{round_no}"
                )
        last = _attempt_once(target, data, mode)
        attempts += 1
        if last.ok:
            return WriteReceipt(
                target, _sha256(data), attempts, f"local-retry-{round_no}"
            )
    raise VerifiedWriteError(
        f"verified write to {target} failed on every path "
        f"({attempts} attempts; last failure: {last.detail})"
    )


def _main(argv: list[str]) -> int:
    """CLI, mirroring the fleet entry: content on stdin.

    ``--child-write PATH MODE`` — one attempt (the ladder's
    subprocess leg; exit 0/1). ``--write PATH MODE`` — the full
    ladder (exit 0, or 3 on total failure, named on stderr).
    MODE is an octal literal (``0o600``) or ``-`` for no mode.
    """
    if len(argv) != 4 or argv[1] not in ("--write", "--child-write"):
        print(
            "usage: python -m glossa_lab.verified_write "
            "--write|--child-write <path> <mode-octal|->  (content on stdin)",
            file=sys.stderr,
        )
        return 2
    mode_arg = argv[3]
    try:
        mode = None if mode_arg == "-" else int(mode_arg, 0)
    except ValueError:
        print(f"invalid mode: {mode_arg!r}", file=sys.stderr)
        return 2
    target = Path(argv[2])
    payload = sys.stdin.buffer.read()
    if argv[1] == "--child-write":
        return 0 if try_write_once(target, payload, mode=mode) else 1
    try:
        receipt = write_file_verified(target, payload, mode=mode)
    except VerifiedWriteError as exc:
        print(f"VERIFIED-WRITE FAILED: {exc}", file=sys.stderr)
        return 3
    print(
        f"verified-write ok via {receipt.via} "
        f"({len(payload)} bytes, sha256 {receipt.sha256[:16]}…)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))

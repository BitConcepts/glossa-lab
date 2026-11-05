"""Atomic, fail-closed writes for small state files (F1 disk-full cascade fix).

Spec 081's PR-3 has been held since 2026-10-30 on the F1 precondition:
"the F1 disk-full cascade fix on main". No written definition of F1
survives in the Spec 081 package, the hardening records, or the program
memory beyond that name and the gate notes in the Spec 081 resume
records ("the sibling's F1 disk-full fix"; "no commit touches the
disk-full cascade items"). This module is the smallest faithful
reconstruction of the fix from the failure mode the name carries:

* A state write must never open its target for in-place truncation.
  ``Path.write_text`` opens with ``O_TRUNC``: when the following write
  fails (ENOSPC on a full disk, or any other write error), the previous
  good content is already destroyed and a truncated or empty file is
  left standing in its place.
* A failed write must fail CLOSED and NAMED — a :class:`StateWriteError`
  whose message identifies the target and the OS error — never be
  swallowed, and never leave a partial file behind.
* A successful write must be complete before it becomes visible: the
  payload goes to a temporary file in the same directory, is flushed
  and fsynced, and is then atomically renamed over the target, so a
  reader only ever sees the previous complete file or the new complete
  file, and a failed write leaves the previous file byte-identical.

Callers keep full control of serialization and of any post-write steps
(permissions, directory fsync); this helper owns only the write itself.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path


class StateWriteError(OSError):
    """A state-file write failed; the previous file (if any) is intact.

    Subclasses :class:`OSError` so existing ``except OSError`` handlers
    keep working; the message always names the target path and the
    underlying OS error (e.g. ``[Errno 28] No space left on device``).
    """


def atomic_write_text(path: Path, content: str, *, encoding: str = "utf-8") -> None:
    """Write ``content`` to ``path`` atomically, failing closed and named.

    Writes to a temporary file in the target's directory, flushes and
    fsyncs it, then renames it over ``path``. On any failure the
    temporary file is removed, the previous content of ``path`` (if
    any) is left byte-identical, and :class:`StateWriteError` is raised
    naming the target and the cause. The target is never opened for
    in-place truncation.
    """
    path = Path(path)
    tmp_name: str | None = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(
            dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp"
        )
        with os.fdopen(fd, "w", encoding=encoding) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
        tmp_name = None
    except StateWriteError:
        raise
    except Exception as exc:
        raise StateWriteError(
            f"atomic write to state file {path} failed: {exc}"
        ) from exc
    finally:
        if tmp_name is not None:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass

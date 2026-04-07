"""GlossaShell — platform-agnostic virtual shell for Glossa Lab.

Routes common shell commands to Python stdlib implementations so they work
identically on Windows, Linux, and macOS without spawning a visible window.
Unknown commands fall back to the OS subprocess with CREATE_NO_WINDOW on
Windows, ensuring no console window ever flashes to the screen.

Supported builtins (work everywhere, no subprocess):
  ls / ll / dir       — list directory
  cat / type          — print file content
  head / tail         — first/last N lines of a file
  pwd                 — current directory
  cd                  — change directory (sandboxed)
  echo                — print arguments
  mkdir               — create directory
  rmdir / rm          — remove file or directory
  cp / copy           — copy file
  mv / move           — rename/move file
  find                — find files by name pattern
  grep / findstr      — search file content
  wc                  — word/line count
  env / set           — show environment variables
  which / where       — locate a command
  clear               — clear screen
  help                — list available commands

Fallback (subprocess, no visible window):
  python / python3    — runs the venv Python (resolved automatically)
  Any other command   — forwarded to cmd.exe /c (Windows) or /bin/sh -c
                        Both use CREATE_NO_WINDOW on Windows.
"""

from __future__ import annotations

import fnmatch
import os
import re
import shlex
import shutil
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any

# ── Constants ─────────────────────────────────────────────────────────────────

_IS_WIN = sys.platform == "win32"

# On Windows, suppress console windows for all subprocesses
_POPEN_FLAGS: dict[str, Any] = {}
if _IS_WIN:
    _POPEN_FLAGS["creationflags"] = subprocess.CREATE_NO_WINDOW  # type: ignore[attr-defined]

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent  # backend/../.. = repo root


# ── Helper: resolve venv Python ───────────────────────────────────────────────

def _venv_python() -> str:
    """Return the venv python executable path."""
    backend = _REPO_ROOT / "backend"
    if _IS_WIN:
        candidate = backend / "venv" / "Scripts" / "python.exe"
    else:
        candidate = backend / "venv" / "bin" / "python"
    return str(candidate) if candidate.exists() else sys.executable


# ── GlossaShell ───────────────────────────────────────────────────────────────

class GlossaShell:
    """Platform-agnostic interactive shell interpreter.

    Maintains a working directory (cwd) that is constrained to stay at or
    below ``sandbox_root`` (the repo root by default).

    Usage::

        shell = GlossaShell()
        for line in shell.run("ls -la reports/"):
            print(line)
    """

    BUILTINS = frozenset({
        "ls", "ll", "la", "dir",
        "cat", "type",
        "head", "tail",
        "pwd", "cd",
        "echo",
        "mkdir", "md",
        "rmdir", "rd", "rm",
        "cp", "copy",
        "mv", "move",
        "find",
        "grep", "findstr",
        "wc",
        "env", "set",
        "which", "where",
        "clear", "cls",
        "help",
        "pip", "pip3",
        "setup",
    })

    def __init__(
        self,
        cwd: Path | None = None,
        sandbox_root: Path | None = None,
    ) -> None:
        self.sandbox_root = (sandbox_root or _REPO_ROOT).resolve()
        self.cwd = (cwd or self.sandbox_root).resolve()
        if not self.cwd.is_relative_to(self.sandbox_root):
            self.cwd = self.sandbox_root
        self.env = {**os.environ}
        # Track venv state once on init (cheap path-existence check)
        # _venv_python() returns str — wrap in Path so .exists() / .parent work
        self._venv_py: Path = Path(_venv_python())
        self._venv_ok: bool = self._venv_py.exists()
        self._greeted = False

    # ── Public entry point ────────────────────────────────────────────────────

    def run(self, command: str) -> Iterator[str]:
        """Execute *command* and yield output lines."""
        command = command.strip()
        if not command or command.startswith("#"):
            # On the very first empty run we still want to emit the venv banner
            return

        # Emit venv status banner on first real command
        if not self._greeted:
            self._greeted = True
            if self._venv_ok:
                # Get Python version quickly
                try:
                    import subprocess as _sp  # noqa: PLC0415
                    r = _sp.run(
                        [str(self._venv_py), "--version"],
                        capture_output=True, text=True, timeout=3,
                        **_POPEN_FLAGS,
                    )
                    ver = (r.stdout or r.stderr).strip().replace("Python ", "")
                    yield f"\x1b[32m● venv active\x1b[0m  Python {ver}  ·  {self._venv_py.parent}"
                except Exception:  # noqa: BLE001
                    yield "\x1b[32m● venv active\x1b[0m"
            else:
                yield "\x1b[33m⚠ No virtual environment found.\x1b[0m"
                yield "  Run 'setup' here or go to Settings → Python Environment to create it."

        # Tokenise (POSIX-style on all platforms for consistency)
        try:
            tokens = shlex.split(command, posix=True)
        except ValueError as exc:
            yield f"parse error: {exc}"
            return

        if not tokens:
            return

        cmd = tokens[0].lower()
        args = tokens[1:]

        # Dispatch
        if cmd in ("ls", "ll", "la", "dir"):
            yield from self._ls(args, long=(cmd in ("ll", "la")))
        elif cmd in ("cat", "type"):
            yield from self._cat(args)
        elif cmd == "head":
            yield from self._head(args)
        elif cmd == "tail":
            yield from self._tail(args)
        elif cmd == "pwd":
            yield str(self.cwd)
        elif cmd == "cd":
            yield from self._cd(args)
        elif cmd == "echo":
            yield " ".join(args)
        elif cmd in ("mkdir", "md"):
            yield from self._mkdir(args)
        elif cmd in ("rmdir", "rd", "rm"):
            yield from self._rm(args)
        elif cmd in ("cp", "copy"):
            yield from self._cp(args)
        elif cmd in ("mv", "move"):
            yield from self._mv(args)
        elif cmd == "find":
            yield from self._find(args)
        elif cmd in ("grep", "findstr"):
            yield from self._grep(args)
        elif cmd == "wc":
            yield from self._wc(args)
        elif cmd in ("env", "set"):
            yield from self._env(args)
        elif cmd in ("which", "where"):
            yield from self._which(args)
        elif cmd in ("clear", "cls"):
            yield "\x1b[2J\x1b[H"   # ANSI clear — frontend strips ANSI anyway
        elif cmd == "help":
            yield from self._help()
        elif cmd in ("pip", "pip3"):
            yield from self._pip(args)
        elif cmd == "setup":
            yield from self._setup_hint()
        else:
            yield from self._subprocess(command)

    # ── Builtins ──────────────────────────────────────────────────────────────

    def _ls(self, args: list[str], long: bool = False) -> Iterator[str]:
        show_hidden = any("a" in a.lstrip("-") for a in args if a.startswith("-"))
        paths = [a for a in args if not a.startswith("-")] or ["."]
        for path_str in paths:
            target = self._resolve(path_str)
            if not target.exists():
                yield f"ls: {path_str}: No such file or directory"
                continue
            if target.is_file():
                entries = [target]
            else:
                entries = sorted(target.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
            for entry in entries:
                if not show_hidden and entry.name.startswith("."):
                    continue
                if long:
                    try:
                        st = entry.stat()
                        size = st.st_size
                    except OSError:
                        size = 0
                    suffix = "/" if entry.is_dir() else ""
                    yield f"{'d' if entry.is_dir() else '-'}  {size:>10}  {entry.name}{suffix}"
                else:
                    yield entry.name + ("/" if entry.is_dir() else "")

    def _cat(self, args: list[str]) -> Iterator[str]:
        if not args:
            yield "cat: missing file operand"
            return
        for fname in args:
            fpath = self._resolve(fname)
            try:
                yield from fpath.read_text(encoding="utf-8", errors="replace").splitlines()
            except IsADirectoryError:
                yield f"cat: {fname}: Is a directory"
            except FileNotFoundError:
                yield f"cat: {fname}: No such file or directory"
            except OSError as exc:
                yield f"cat: {fname}: {exc}"

    def _head(self, args: list[str]) -> Iterator[str]:
        n, files = self._parse_n_flag(args, default=10)
        for fname in files or ["stdin"]:
            fpath = self._resolve(fname)
            try:
                lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines()
                yield from lines[:n]
            except OSError as exc:
                yield f"head: {fname}: {exc}"

    def _tail(self, args: list[str]) -> Iterator[str]:
        n, files = self._parse_n_flag(args, default=10)
        for fname in files or ["stdin"]:
            fpath = self._resolve(fname)
            try:
                lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines()
                yield from lines[-n:]
            except OSError as exc:
                yield f"tail: {fname}: {exc}"

    def _cd(self, args: list[str]) -> Iterator[str]:
        if not args or args[0] in ("~", ""):
            target = self.sandbox_root
        else:
            target = self._resolve(args[0])
        if not target.is_dir():
            yield f"cd: {args[0]}: Not a directory"
            return
        # Enforce sandbox
        try:
            target.resolve().relative_to(self.sandbox_root)
        except ValueError:
            target = self.sandbox_root
            yield f"(sandboxed to repo root: {self.sandbox_root})"
        self.cwd = target.resolve()
        yield f"→ {self.cwd}"

    def _mkdir(self, args: list[str]) -> Iterator[str]:
        for name in [a for a in args if not a.startswith("-")]:
            target = self._resolve(name)
            try:
                target.mkdir(parents=True, exist_ok=True)
                yield f"Created: {target}"
            except OSError as exc:
                yield f"mkdir: {name}: {exc}"

    def _rm(self, args: list[str]) -> Iterator[str]:
        recursive = any(a in ("-r", "-rf", "-fr") for a in args)
        for name in [a for a in args if not a.startswith("-")]:
            target = self._resolve(name)
            try:
                if target.is_dir():
                    if recursive:
                        shutil.rmtree(target)
                        yield f"Removed directory: {target}"
                    else:
                        yield f"rm: {name}: Is a directory (use -r to remove)"
                elif target.exists():
                    target.unlink()
                    yield f"Removed: {target}"
                else:
                    yield f"rm: {name}: No such file or directory"
            except OSError as exc:
                yield f"rm: {name}: {exc}"

    def _cp(self, args: list[str]) -> Iterator[str]:
        files = [a for a in args if not a.startswith("-")]
        if len(files) < 2:
            yield "cp: missing destination operand"
            return
        src, dst = self._resolve(files[0]), self._resolve(files[1])
        try:
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            yield f"Copied {src.name} → {dst}"
        except OSError as exc:
            yield f"cp: {exc}"

    def _mv(self, args: list[str]) -> Iterator[str]:
        files = [a for a in args if not a.startswith("-")]
        if len(files) < 2:
            yield "mv: missing destination"
            return
        src, dst = self._resolve(files[0]), self._resolve(files[1])
        try:
            shutil.move(str(src), str(dst))
            yield f"Moved {src.name} → {dst}"
        except OSError as exc:
            yield f"mv: {exc}"

    def _find(self, args: list[str]) -> Iterator[str]:
        root_str = "."
        pattern = "*"
        i = 0
        while i < len(args):
            a = args[i]
            if a == "-name" and i + 1 < len(args):
                pattern = args[i + 1]
                i += 2
            elif not a.startswith("-"):
                root_str = a
                i += 1
            else:
                i += 1
        root = self._resolve(root_str)
        try:
            for p in sorted(root.rglob("*")):
                if fnmatch.fnmatch(p.name, pattern):
                    yield str(p.relative_to(self.cwd))
        except OSError as exc:
            yield f"find: {exc}"

    def _grep(self, args: list[str]) -> Iterator[str]:
        flags = [a for a in args if a.startswith("-")]
        positional = [a for a in args if not a.startswith("-")]
        if not positional:
            yield "grep: missing pattern"
            return
        pattern_str = positional[0]
        files = positional[1:]
        case_insensitive = "-i" in flags
        show_line_nums = "-n" in flags
        try:
            rx = re.compile(pattern_str, re.IGNORECASE if case_insensitive else 0)
        except re.error as exc:
            yield f"grep: invalid pattern: {exc}"
            return
        if not files:
            yield "grep: (no files — specify file arguments)"
            return
        for fname in files:
            fpath = self._resolve(fname)
            try:
                for lineno, line in enumerate(
                    fpath.read_text(encoding="utf-8", errors="replace").splitlines(),
                    start=1,
                ):
                    if rx.search(line):
                        if show_line_nums:
                            prefix = f"{fname}:{lineno}:"
                        elif len(files) > 1:
                            prefix = f"{fname}:"
                        else:
                            prefix = ""
                        yield prefix + line
            except OSError as exc:
                yield f"grep: {fname}: {exc}"

    def _wc(self, args: list[str]) -> Iterator[str]:
        for fname in [a for a in args if not a.startswith("-")]:
            fpath = self._resolve(fname)
            try:
                text = fpath.read_text(encoding="utf-8", errors="replace")
                lines = text.count("\n")
                words = len(text.split())
                chars = len(text)
                yield f"{lines:>8} {words:>8} {chars:>8}  {fname}"
            except OSError as exc:
                yield f"wc: {fname}: {exc}"

    def _env(self, args: list[str]) -> Iterator[str]:
        for k, v in sorted(self.env.items()):
            if not args or any(a.upper() in k.upper() for a in args):
                yield f"{k}={v}"

    def _which(self, args: list[str]) -> Iterator[str]:
        for name in args:
            found = shutil.which(name)
            yield found if found else f"{name}: not found"

    def _help(self) -> Iterator[str]:
        yield "GlossaShell — built-in commands:"
        yield "  ls / ll / dir       list directory"
        yield "  cat / type          print file"
        yield "  head / tail [-n N]  first/last N lines"
        yield "  pwd                 current directory"
        yield "  cd <dir>            change directory (sandboxed to repo)"
        yield "  echo <text>         print text"
        yield "  mkdir <dir>         create directory"
        yield "  rm [-r] <path>      remove file/directory"
        yield "  cp <src> <dst>      copy file"
        yield "  mv <src> <dst>      move/rename file"
        yield "  find [root] -name <pattern>  find files"
        yield "  grep [-i] [-n] <pattern> <files>  search in files"
        yield "  wc <files>          word/line/char count"
        yield "  env / set           show environment"
        yield "  which / where       locate command"
        yield "  clear               clear screen"
        yield "  help                this message"
        yield ""
        yield "Anything else is forwarded to the OS shell (no visible window on Windows)."
        yield "python <script>  →  runs the Glossa Lab venv Python automatically."

    def _pip(self, args: list[str]) -> Iterator[str]:
        """Route pip commands to the venv Python -m pip."""
        if not self._venv_ok:
            yield "pip: no virtual environment found — run 'setup' first"
            return
        # Build the real command: venv/python -m pip <args>
        pip_cmd = f'"{self._venv_py}" -m pip {" ".join(args)}'
        yield from self._subprocess(pip_cmd)

    def _setup_hint(self) -> Iterator[str]:
        """Hint user toward the Settings > Python Environment panel."""
        if self._venv_ok:
            yield "\x1b[32m\u25cf venv is already active\x1b[0m  — nothing to set up."
            yield "  To rebuild: Settings \u2192 Python Environment \u2192 Rebuild venv"
        else:
            yield "\x1b[33m\u26a0 No virtual environment found.\x1b[0m"
            yield "  Go to  Settings \u2192 Python Environment \u2192 Setup venv"
            yield "  Or run from the repo root:  shell.cmd setup"

    # ── Subprocess fallback (no visible window) ───────────────────────────────────────────────

    def _subprocess(self, command: str) -> Iterator[str]:
        """Execute command via OS shell with no visible window on Windows."""
        # Replace bare `python` / `python3` with the venv Python.
        # Use a lambda so the replacement string is never processed for backslash
        # escapes — Windows paths contain \U which re.sub() would treat as a
        # Unicode escape and crash with 'bad escape \U at position N'.
        venv_py = _venv_python()
        cmd = re.sub(
            r"^python3?\b",
            lambda _: f'"{venv_py}"',
            command,
            flags=re.IGNORECASE,
        )

        if _IS_WIN:
            shell_args: list[str] = ["cmd.exe", "/c", cmd]
        else:
            shell_args = ["/bin/sh", "-c", cmd]

        try:
            proc = subprocess.Popen(  # noqa: S603
                shell_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=str(self.cwd),
                env=self.env,
                **_POPEN_FLAGS,   # CREATE_NO_WINDOW on Windows
            )
            assert proc.stdout is not None
            for raw_line in proc.stdout:
                yield raw_line.decode(errors="replace").rstrip("\r\n")
            proc.wait()
            # Do not print exit codes — real terminals don't display them.
            # Non-zero exit is visible to the user from the command output itself.
        except FileNotFoundError:
            yield f"command not found: {command.split()[0]}"
        except Exception as exc:  # noqa: BLE001
            yield f"error: {exc}"

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _resolve(self, path_str: str) -> Path:
        """Resolve *path_str* relative to cwd, returning an absolute Path."""
        p = Path(path_str)
        if p.is_absolute():
            return p
        return (self.cwd / p).resolve()

    @staticmethod
    def _parse_n_flag(args: list[str], default: int = 10) -> tuple[int, list[str]]:
        """Extract -n N flag from args, returning (n, remaining_files)."""
        n = default
        files: list[str] = []
        i = 0
        while i < len(args):
            a = args[i]
            if a == "-n" and i + 1 < len(args):
                try:
                    n = int(args[i + 1])
                except ValueError:
                    pass
                i += 2
            elif a.startswith("-") and a[1:].isdigit():
                n = int(a[1:])
                i += 1
            else:
                files.append(a)
                i += 1
        return n, files

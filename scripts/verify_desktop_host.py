#!/usr/bin/env python3
"""Desktop host verification for Glossa Lab (Spec 080, FR-007).

Emits gatekeeper-harvestable marker lines proving, on the machine
that runs this script (TRISTEN-DESKTOP):

* GLOSSA_HOST_HEALTH    — health payload status/version + /docs code
* GLOSSA_HOST_IDENTITY  — the bounded Spec 079 identity check
  (/docs 200 + health status/version + OpenAPI title "Glossa Lab"
  with matching version), reusing services/linux/healthcheck.py
* GLOSSA_TRAY_PROCESS   — tray process(es) running (-m glossa_tray)
* GLOSSA_ICON_HASH      — installed-tree icon assets match the
  Spec 079 SHA-256 pins
* GLOSSA_TASK_STATE     — the GlossaLab scheduled task state,
  read via the CIM provider (Windows; Spec 080 FR-004)
* GLOSSA_RESTART_TEST   — stop/start through the app's own
  controls (setup-os.cmd): process set gone and proxy health
  no longer the app's 200 while down; healthy with identity
  under a fresh PID when back. No raw process kills.
  supervisor must bring it back (new PID) within the deadline

Every wait is bounded (H11). Exit code 0 only if health, identity,
icon, tray presence, and the restart test all pass (a check can be
explicitly skipped, which its marker records). Tray presence is
part of the verdict because the tray IS the host's user interface:
a verify that passed with no tray running certified a host whose
UI was down (2026-10-29 UI-log audit).
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ICON_ICO_SHA256 = "315940742d75720388264dcdf03178c58f878ea0701d03eeba95688d935ff520"
ICON_PNG_SHA256 = "bb41bf09d4177cee0c96b29ebe480f86a9e7115946f9e4ad132d2367a7adb077"
TASK_NAME = "GlossaLab"
RESTART_DEADLINE_SEC = 120
POLL_INTERVAL_SEC = 2


def marker(name: str, value: str) -> None:
    print(f"{name} {value}", flush=True)


# ------------------------------------------------------------------
# Bounded waits (Defect 1 fix, 2026-10-29). Host run 40911989844
# parked forever inside this script at zero CPU: a call with only
# a PER-RECEIVE timeout (a drip-fed HTTP read, a pipe drain behind
# a surviving grandchild) can wait indefinitely. Every external
# call below therefore goes through a helper with a TOTAL
# deadline; a wait that expires emits a NAMED marker -
# GLOSSA_WAIT name=<wait> result=TIMEOUT timeout=<seconds> - and
# fails its leg instead of hanging the run.
# ------------------------------------------------------------------
VERIFY_DEADLINE_SEC = int(os.environ.get("GLOSSA_VERIFY_DEADLINE_SEC", "480"))
_started_at = time.monotonic()


class WaitTimeout(Exception):
    """A named bounded wait expired."""


def _deadline_left() -> float:
    return VERIFY_DEADLINE_SEC - (time.monotonic() - _started_at)


def run_bounded(name: str, argv: list[str], timeout: float,
                cwd: str | None = None) -> subprocess.CompletedProcess:
    """subprocess with a total deadline and tree-kill on expiry
    (a surviving grandchild holding the pipes must not turn the
    post-kill drain into a second, unbounded wait)."""
    timeout = max(1.0, min(timeout, _deadline_left()))
    proc = subprocess.Popen(
        argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, cwd=cwd,
    )
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        marker("GLOSSA_WAIT", f"name={name} result=TIMEOUT timeout={timeout:.0f}")
        try:
            if sys.platform == "win32":
                subprocess.run(
                    ["taskkill", "/T", "/F", "/PID", str(proc.pid)],
                    capture_output=True, timeout=15,
                )
            else:
                proc.kill()
        except Exception:
            pass
        try:
            proc.communicate(timeout=10)
        except Exception:
            pass
        raise WaitTimeout(name) from None
    return subprocess.CompletedProcess(argv, proc.returncode, out, err)


def call_bounded(name: str, fn, timeout: float):
    """Run fn() in a daemon thread with a total deadline - for
    in-process calls whose own timeouts are per-operation, not
    total (urllib reads). On expiry the leg fails; the daemon
    thread is abandoned, never joined again."""
    import threading

    timeout = max(1.0, min(timeout, _deadline_left()))
    box: dict = {}

    def _run() -> None:
        try:
            box["value"] = fn()
        except Exception as exc:  # surfaced to the caller below
            box["error"] = exc

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        marker("GLOSSA_WAIT", f"name={name} result=TIMEOUT timeout={timeout:.0f}")
        raise WaitTimeout(name)
    if "error" in box:
        raise box["error"]
    return box.get("value")


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def icon_hashes_ok(repo_root: Path) -> tuple[bool, str, str]:
    """Return (ok, ico_sha, png_sha) for the packaged tray assets."""
    assets = repo_root / "tray" / "glossa_tray" / "assets"
    ico = assets / "glossa-lab.ico"
    png = assets / "glossa-lab.png"
    ico_sha = sha256_of(ico) if ico.exists() else "MISSING"
    png_sha = sha256_of(png) if png.exists() else "MISSING"
    return (ico_sha == ICON_ICO_SHA256 and png_sha == ICON_PNG_SHA256), ico_sha, png_sha


def load_healthcheck():
    """Import the Spec 079 identity check (pure stdlib, platform-neutral)."""
    path = REPO_ROOT / "services" / "linux" / "healthcheck.py"
    spec = importlib.util.spec_from_file_location("glossa_healthcheck", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _app_python_pids(pattern: str) -> list[int]:
    """PIDs of app processes: venv-python executables whose
    command line matches `pattern`.

    The executable test matters: a bare command-line match also
    matches the PowerShell process RUNNING this query (its own
    -Command text contains the pattern), and that transient PID
    then fails the kill step - host run 40880047294 measured
    exactly that (kill-failed on a set containing the query
    shell). App processes run from the repo venv's python.
    """
    if sys.platform == "win32":
        command = [
            "powershell", "-NoProfile", "-NonInteractive", "-Command",
            "Get-CimInstance Win32_Process | "
            "Where-Object { $_.ExecutablePath -match 'venv\\\\Scripts\\\\python' "
            f"-and $_.CommandLine -match '{pattern}' }} | "
            "ForEach-Object { $_.ProcessId }",
        ]
    else:
        command = ["pgrep", "-f", pattern]
    try:
        result = run_bounded("cim-process-query", command, timeout=15)
    except (WaitTimeout, OSError):
        return []
    pids: list[int] = []
    for token in result.stdout.split():
        if token.strip().isdigit():
            pids.append(int(token.strip()))
    return [pid for pid in pids if pid != os.getpid()]


def tray_pids() -> list[int]:
    """PIDs of the tray processes (-m glossa_tray, venv python)."""
    return _app_python_pids("glossa_tray")


def backend_pids() -> list[int]:
    """PIDs of the app's own backend processes.

    NEVER identify the backend by the port-8001 listener: on the
    desktop host that listener is tailscaled.exe (Tailscale Serve
    proxies the tailnet :8001 to the app's loopback :8001), a
    session-0 service the verifier can neither kill nor learn
    anything about the app from. That misidentification is
    exactly what host run 40835699406 measured (kill-failed
    pid=<tailscaled>). The app's backend is the venv-python
    process set running this repo's uvicorn entry - the same
    test the targeted stop path uses.
    """
    return _app_python_pids("glossa_lab.*uvicorn|uvicorn.*glossa_lab")


PROXY_HEALTH_URL = os.environ.get(
    "GLOSSA_PROXY_HEALTH_URL",
    "http://tristen-desktop.tailbfa48d.ts.net:8001/api/v1/health",
)


def setup_os(verb: str) -> int | None:
    """Run the app's own setup-os.cmd verb (stop/start) in the
    repo root; return its exit code (None if it cannot run)."""
    if sys.platform != "win32":
        return None
    try:
        result = run_bounded(
            f"setup-os-{verb}",
            ["cmd", "/c", str(REPO_ROOT / "setup-os.cmd"), verb],
            timeout=90, cwd=str(REPO_ROOT),
        )
    except (WaitTimeout, OSError):
        return None
    return result.returncode


def proxy_health_code() -> str:
    """HTTP status of the health endpoint THROUGH Tailscale
    Serve, or UNREACHABLE. While the app is down the proxy alone
    answers 502 - the down-judgment restart-verify2 proved
    (host run 40849993917)."""
    import urllib.error
    import urllib.request

    try:
        with urllib.request.urlopen(PROXY_HEALTH_URL, timeout=8) as resp:
            return str(resp.status)
    except urllib.error.HTTPError as exc:
        return str(exc.code)
    except Exception:
        return "UNREACHABLE"


def wait_backend_gone(deadline_sec: int) -> bool:
    """Bounded wait (H11) for the backend process set to empty."""
    deadline = time.time() + deadline_sec
    while time.time() < deadline:
        if not backend_pids():
            return True
        time.sleep(POLL_INTERVAL_SEC)
    return not backend_pids()


def restart_test(healthcheck, base_url: str) -> tuple[bool, str]:
    """The restart property, proven the way restart-verify2
    proved it on the host (run 40849993917): the app's OWN stop
    (setup-os.cmd stop) -> backend process set gone + health
    through the proxy no longer the app's 200 -> the app's own
    start -> healthy with identity under a fresh PID.

    NO raw process kills anywhere in this suite: the venue
    proved three times (runs 40835699406, 40840066177,
    40880047294) that job-context kills cannot act on the app
    processes, while the app's own stop works every time.
    """
    if sys.platform != "win32":
        return False, "non-windows: app-stop path is Windows-only"
    old_pids = backend_pids()
    if not old_pids:
        return False, "no-backend-process"
    stop_exit = setup_os("stop")
    if stop_exit is None:
        return False, "app-stop-unavailable-or-timeout"
    if stop_exit != 0:
        return False, f"app-stop-exit={stop_exit}"
    if not wait_backend_gone(RESTART_DEADLINE_SEC // 2):
        return False, "backend-set-not-gone-after-app-stop"
    try:
        proxy_code = call_bounded("proxy-health", proxy_health_code, 15)
    except WaitTimeout:
        return False, "wait-timeout proxy-health"
    if proxy_code == "200":
        return False, "proxy-still-200-while-backend-down"
    start_exit = setup_os("start")
    if start_exit is None:
        return False, "app-start-unavailable-or-timeout"
    if start_exit != 0:
        return False, f"app-start-exit={start_exit}"
    back, new_pid = wait_for_new_backend(
        healthcheck, base_url, old_pids, RESTART_DEADLINE_SEC
    )
    if not back:
        return False, "backend-not-back-after-app-start"
    return True, (
        f"stop_exit=0 set_gone=1 proxy_down={proxy_code} "
        f"start_exit=0 new_pid={new_pid}"
    )


def task_state() -> str:
    """State of the GlossaLab scheduled task (Windows), via CIM.

    Spec 080 FR-004 (Amendment 2): the canonical autostart is the
    GlossaLab task registered by scripts/register_task.ps1 in the
    route-B shape. Read through Get-ScheduledTask (the CIM
    provider) - the same read path host diagnostic run
    40816104983 proved live; schtasks /Query proved unreliable in
    that venue (exit 0 while creating nothing, run 40807602846).
    """
    if sys.platform != "win32":
        return "SKIP non-windows"
    command = (
        f"Get-ScheduledTask -TaskName '{TASK_NAME}' "
        "-ErrorAction Stop | Select-Object -ExpandProperty State"
    )
    try:
        result = run_bounded(
            "task-state-query",
            ["powershell", "-NoProfile", "-NonInteractive", "-Command",
             command],
            timeout=15,
        )
    except WaitTimeout:
        return "TIMEOUT"
    if result.returncode != 0:
        return "MISSING"
    return result.stdout.strip() or "MISSING"


def wait_for_new_backend(healthcheck, base_url: str,
                         old_pids: list[int],
                         deadline_sec: int) -> tuple[bool, int | None]:
    """Bounded wait (H11): healthy again AND a backend process
    exists that was not in the pre-stop set."""
    deadline = time.time() + deadline_sec
    attempts = 0
    while time.time() < deadline:
        attempts += 1
        try:
            ok, _result = call_bounded(
                "health-poll",
                lambda: healthcheck.check_once(base_url, 3.0), 20,
            )
        except WaitTimeout:
            return False, None
        fresh = [pid for pid in backend_pids() if pid not in old_pids]
        if ok and fresh:
            return True, fresh[0]
        time.sleep(POLL_INTERVAL_SEC)
    return False, None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8001")
    parser.add_argument("--skip-restart-test", action="store_true",
                        help="report state only; do not cycle the backend")
    parser.add_argument("--skip-tray-check", action="store_true",
                        help="do not require a running tray process")
    args = parser.parse_args(argv)
    base_url = args.base_url.rstrip("/")
    healthcheck = load_healthcheck()

    try:
        ok, result = call_bounded(
            "health-initial",
            lambda: healthcheck.check_once(base_url, 3.0), 20,
        )
    except WaitTimeout:
        ok, result = False, {"health": {}, "docs_status": 0,
                             "app_title": None,
                             "errors": ["wait-timeout health-initial"]}
    health = result.get("health") or {}
    marker(
        "GLOSSA_HOST_HEALTH",
        f"status={health.get('status')} version={health.get('version')} "
        f"docs={result.get('docs_status')}",
    )
    marker(
        "GLOSSA_HOST_IDENTITY",
        f"title={result.get('app_title')} version={health.get('version')} "
        f"result={'PASS' if ok else 'FAIL'} errors={result.get('errors')}",
    )

    pids = tray_pids()
    tray_ok = len(pids) >= 1
    if args.skip_tray_check:
        tray_ok = True
        marker("GLOSSA_TRAY_PROCESS", "result=SKIP requested")
    else:
        marker(
            "GLOSSA_TRAY_PROCESS",
            f"count={len(pids)} "
            f"pids={','.join(str(p) for p in pids) if pids else 'NONE'} "
            f"result={'PASS' if tray_ok else 'FAIL'}",
        )

    icons_ok, ico_sha, png_sha = icon_hashes_ok(REPO_ROOT)
    marker(
        "GLOSSA_ICON_HASH",
        f"ico={ico_sha} png={png_sha} result={'PASS' if icons_ok else 'FAIL'}",
    )

    marker(
        "GLOSSA_TASK_STATE",
        f"name={TASK_NAME} state={task_state()}",
    )

    restart_ok = True
    if args.skip_restart_test:
        marker("GLOSSA_RESTART_TEST", "result=SKIP requested")
    else:
        restart_ok, detail = restart_test(healthcheck, base_url)
        marker(
            "GLOSSA_RESTART_TEST",
            f"result={'PASS' if restart_ok else 'FAIL'} {detail}",
        )

    overall = ok and icons_ok and restart_ok and tray_ok
    marker("GLOSSA_HOST_VERIFY", f"result={'PASS' if overall else 'FAIL'}")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())

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
* GLOSSA_RESTART_TEST   — kill the app's backend process set
  (command-line identified, never the port listener); the tray
  supervisor must bring it back (new PID) within the deadline

Every wait is bounded (H11). Exit code 0 only if health, identity,
icon and (when the tray is running) the restart test all pass.
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
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=15,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
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


def kill_pid(pid: int) -> bool:
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ["taskkill", "/F", "/PID", str(pid)],
                capture_output=True, text=True, timeout=15,
            )
            return result.returncode == 0
        os.kill(pid, 9)
        return True
    except (OSError, subprocess.TimeoutExpired):
        return False


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
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command",
             command],
            capture_output=True, text=True, timeout=15, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"ERROR {exc}"
    if result.returncode != 0:
        return "MISSING"
    return result.stdout.strip() or "MISSING"


def wait_for_new_backend(healthcheck, base_url: str,
                         old_pids: list[int],
                         deadline_sec: int) -> tuple[bool, int | None]:
    """Bounded wait (H11): healthy again AND a backend process
    exists that was not in the pre-kill set."""
    deadline = time.time() + deadline_sec
    attempts = 0
    while time.time() < deadline:
        attempts += 1
        ok, _result = healthcheck.check_once(base_url, 3.0)
        fresh = [pid for pid in backend_pids() if pid not in old_pids]
        if ok and fresh:
            return True, fresh[0]
        time.sleep(POLL_INTERVAL_SEC)
    return False, None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8001")
    parser.add_argument("--skip-restart-test", action="store_true",
                        help="report state only; do not kill the backend")
    args = parser.parse_args(argv)
    base_url = args.base_url.rstrip("/")
    healthcheck = load_healthcheck()

    ok, result = healthcheck.check_once(base_url, 3.0)
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
    marker(
        "GLOSSA_TRAY_PROCESS",
        f"count={len(pids)} pids={','.join(str(p) for p in pids) if pids else 'NONE'}",
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
    elif not pids:
        restart_ok = False
        marker("GLOSSA_RESTART_TEST", "result=FAIL reason=no-tray-process-to-supervise")
    else:
        old_pids = backend_pids()
        if not old_pids:
            restart_ok = False
            marker("GLOSSA_RESTART_TEST", "result=FAIL reason=no-backend-process")
        elif not all(kill_pid(pid) for pid in old_pids):
            restart_ok = False
            marker(
                "GLOSSA_RESTART_TEST",
                f"result=FAIL reason=kill-failed pids={old_pids}",
            )
        else:
            restart_ok, new_pid = wait_for_new_backend(
                healthcheck, base_url, old_pids, RESTART_DEADLINE_SEC
            )
            marker(
                "GLOSSA_RESTART_TEST",
                f"result={'PASS' if restart_ok else 'FAIL'} "
                f"old_pids={old_pids} new_pid={new_pid}",
            )

    overall = ok and icons_ok and restart_ok
    marker("GLOSSA_HOST_VERIFY", f"result={'PASS' if overall else 'FAIL'}")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())

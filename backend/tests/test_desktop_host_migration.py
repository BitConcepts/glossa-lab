"""Spec 080 — desktop host migration (Windows paths).

Static contract tests over the Windows launch/install/stop files,
plus unit tests for the desktop verify script's pure helpers. No
test here starts a real backend, a tray, or a scheduled task; the
live proof is the gatekeeper-harvested marker run recorded in the
Spec 080 migration record.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ICO_SHA256 = "315940742d75720388264dcdf03178c58f878ea0701d03eeba95688d935ff520"
PNG_SHA256 = "bb41bf09d4177cee0c96b29ebe480f86a9e7115946f9e4ad132d2367a7adb077"


def _text(rel: str) -> str:
    return (REPO / rel).read_text(encoding="utf-8", errors="replace")


def _load_verify_module():
    path = REPO / "scripts" / "verify_desktop_host.py"
    spec = importlib.util.spec_from_file_location("glossa_verify_desktop_host", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_windows_launch_paths_use_production_entry() -> None:
    """C080-1: factory entry, loopback, no reload — everywhere."""
    for rel in ("shell.cmd", "scripts/run-backend-svc.cmd"):
        text = _text(rel)
        assert "glossa_lab.main:create_app --factory" in text, rel
        assert "127.0.0.1" in text, rel
        assert "glossa_lab.main:app" not in text, rel
        # The reload ban binds the invocation line, not prose: a
        # comment explaining the ban legitimately names the flag.
        invocation = next(
            line for line in text.splitlines() if "uvicorn" in line
        )
        assert "--reload" not in invocation, rel
        assert "0.0.0.0" not in text, rel
    tray = _text("tray/glossa_tray/main.py")
    assert '"glossa_lab.main:create_app"' in tray
    assert '"--factory"' in tray
    assert '"127.0.0.1"' in tray
    assert '"glossa_lab.main:app"' not in tray
    assert '"0.0.0.0"' not in tray


def test_installed_mode_set_across_launch_chain() -> None:
    """C080-2: GLOSSA_MODE=installed in VBS, service wrapper, tray env."""
    assert '"installed"' in _text("scripts/launch-tray.vbs")
    assert "GLOSSA_MODE" in _text("scripts/launch-tray.vbs")
    assert 'set "GLOSSA_MODE=installed"' in _text("scripts/run-backend-svc.cmd")
    assert 'env["GLOSSA_MODE"] = "installed"' in _text("tray/glossa_tray/main.py")


def test_setup_os_stop_is_targeted() -> None:
    """C080-3: no machine-wide python/pythonw kill in the stop path."""
    text = _text("setup-os.cmd")
    assert "taskkill /F /IM pythonw.exe" not in text
    assert "/IM python.exe" not in text
    assert "stop-tray.vbs" in text  # tray stops via its H25 wrapper
    # Any force-kill is by PID, only after the listener's command
    # line is verified to be Glossa's own uvicorn.
    assert "Win32_Process" in text and "CommandLine" in text
    assert "glossa_lab" in text and "uvicorn" in text


def test_setup_os_install_verifies_icon_hashes() -> None:
    """C080-5: the Spec 079 SHA-256 pins gate the install."""
    text = _text("setup-os.cmd").upper()
    assert ICO_SHA256.upper() in text
    assert PNG_SHA256.upper() in text
    # The comparison runs in scripts\verify_icon_hashes.ps1, which
    # hashes with the .NET SHA-256 implementation. The previous
    # inline Get-FileHash check depended on module autoloading,
    # which was unavailable in the Syncyard runner's
    # powershell.exe -NoProfile context (2026-10-28), and the
    # hashing failure was then misreported as a hash mismatch.
    assert "VERIFY_ICON_HASHES.PS1" in text
    helper = _text("scripts/verify_icon_hashes.ps1")
    assert "System.Security.Cryptography.SHA256" in helper
    # The helper must not invoke Get-FileHash (its header comment
    # names it only to explain why it is not used).
    assert "(Get-FileHash" not in helper
    assert "Get-FileHash -Algorithm" not in helper
    assert "-ieq" in helper  # a hex digest's letter case is not data
    # Failure stays loud and discriminated: hashing failure,
    # missing asset, and mismatch are distinct nonzero exits.
    for code in ("exit 2", "exit 3", "exit 4"):
        assert code in helper, code


def test_setup_os_autostart_is_routeb_task() -> None:
    """C080-8 (Amendment 2): one canonical autostart - the GlossaLab
    scheduled task, registered in the route-B shape proven by host
    diagnostic run 40816104983: scoped principal (Interactive /
    Limited), user-scoped logon trigger, no elevation. The HKCU
    Run-key route (Amendment 1) is removed, not dual-pathed."""
    text = _text("setup-os.cmd")
    assert "register_task.ps1" in text
    assert "reg add" not in text
    assert "RunAs" not in text  # no elevation wrapper (diag1's shape)
    helper = _text("scripts/register_task.ps1")
    assert "New-ScheduledTaskPrincipal" in helper
    assert "LogonType Interactive" in helper
    assert "RunLevel Limited" in helper
    assert "New-ScheduledTaskTrigger -AtLogon -User" in helper
    assert "wscript.exe" in helper and "launch-tray.vbs" in helper
    # Registration is read back and gated on the Ready state.
    assert "GLOSSA_TASK_STATE" in helper
    assert "Get-ScheduledTask" in helper
    # Amendment 3: scheduler restart-on-failure, with the VBS
    # waiting on the tray so the settings have a lifetime to
    # supervise (a fire-and-forget launch died with its job).
    assert "RestartCount 3" in helper
    assert "RestartInterval" in helper
    vbs = _text("scripts/launch-tray.vbs")
    assert ", 0, True)" in vbs
    assert "WScript.Quit" in vbs
    # The tray detects autostart from the same task.
    tray = _text("tray/glossa_tray/main.py")
    assert "schtasks" in tray
    assert "winreg" not in tray


def test_start_is_idempotent_on_verified_identity() -> None:
    """C080-9 (Amendment 3): setup-os.cmd start is a no-op success
    when the backend already answers with the Spec 079 identity;
    the gate is the bounded healthcheck, checked before any
    stop/launch in the start path."""
    text = _text("setup-os.cmd")
    assert "healthcheck.py" in text
    assert "GLOSSA_START_STATE already-running" in text
    gate = text.index("GLOSSA_START_STATE already-running")
    stop_first = text.index("call :do_stop_silent", text.index(":do_start"))
    assert gate < stop_first
    # The idempotency gate covers the tray as well as the
    # backend: a running tray makes it a full no-op, a missing
    # tray launches only the tray.
    assert "tray=running" in text
    assert "tray-launched" in text
    # Waits use ping, never timeout.exe (which errors under
    # redirected stdin and dirties successful job logs). Checked
    # over operational (non-REM) lines: this assertion previously
    # ended in "or True" and could never fail (2026-10-29 audit).
    operational = "\n".join(
        line for line in text.splitlines()
        if not line.lstrip().upper().startswith("REM")
    )
    assert "timeout /t" not in operational.lower()
    assert "TIMEOUT /T" not in text


def test_services_windows_delegates_to_canonical_installer() -> None:
    """C080-4: services/windows is a shim, never a second installer."""
    install = _text("services/windows/install.cmd")
    assert "setup-os.cmd" in install
    assert "CreateShortcut" not in install
    # No operational (non-comment) line may invoke shell.cmd — the
    # delegator's comments legitimately describe the retired path.
    operational = [
        line for line in install.splitlines()
        if not line.lstrip().upper().startswith("REM")
    ]
    assert not any("shell.cmd" in line for line in operational)
    uninstall = _text("services/windows/uninstall.cmd")
    assert "setup-os.cmd" in uninstall
    assert "GlossaLab.lnk" in uninstall  # legacy shortcut cleanup


def test_tray_supervision_contract() -> None:
    """C080-6: capped auto-restart that respects a deliberate stop."""
    tray = _text("tray/glossa_tray/main.py")
    assert "_MAX_AUTO_RESTARTS = 3" in tray
    assert "_RESTART_WINDOW_SEC = 3600" in tray
    assert "_user_stopped" in tray
    assert "_maybe_auto_restart()" in tray  # poller invokes the supervisor


def test_install_verify_pair_shape() -> None:
    """C080-7 (shape): installer chains install -> start -> verify."""
    installer = _text("scripts/install-desktop-host.cmd")
    assert "setup-os.cmd\" install" in installer
    assert "setup-os.cmd\" start" in installer
    assert "verify-desktop-host.cmd" in installer
    wrapper = _text("scripts/verify-desktop-host.cmd")
    assert "verify_desktop_host.py" in wrapper


def test_verify_script_markers_and_icon_helper(tmp_path: Path) -> None:
    """C080-7/C080-5: marker vocabulary + the icon hash comparison."""
    source = _text("scripts/verify_desktop_host.py")
    for name in (
        "GLOSSA_HOST_HEALTH",
        "GLOSSA_HOST_IDENTITY",
        "GLOSSA_TRAY_PROCESS",
        "GLOSSA_ICON_HASH",
        "GLOSSA_TASK_STATE",
        "GLOSSA_RESTART_TEST",
    ):
        assert name in source, name
    # The backend must be identified by its command line, never
    # by the port-8001 listener: on the desktop host that listener
    # is tailscaled (Tailscale Serve), not the app (run
    # 40835699406 measured exactly that misidentification).
    assert "Get-NetTCPConnection" not in source
    assert "def backend_pids" in source
    # Identification must require the venv-python executable, so
    # the query's own shell (whose command line carries the
    # pattern text) is never in the set (run 40880047294).
    assert "ExecutablePath" in source
    # No raw process kills anywhere in the verify suite: the
    # restart leg cycles the app through its own controls.
    assert "taskkill" not in source
    assert "def kill_pid" not in source
    assert "def restart_test" in source
    module = _load_verify_module()
    # The packaged assets in this repo are the pinned ones.
    ok, ico_sha, png_sha = module.icon_hashes_ok(REPO)
    assert ok and ico_sha == ICO_SHA256 and png_sha == PNG_SHA256
    # A tree without the assets must not pass.
    ok_empty, ico_empty, _png_empty = module.icon_hashes_ok(tmp_path)
    assert not ok_empty and ico_empty == "MISSING"
    # sha256 helper against a known vector.
    probe = tmp_path / "probe.bin"
    probe.write_bytes(b"glossa")
    assert module.sha256_of(probe) == (
        "a19f5afd22174fa5e381b583c622bdbb98091676a20b9983e3e47b4d64f27378"
    )


def test_start_services_files_delegate_to_setup_os() -> None:
    """The retired direct-launch starters are shims, never a second
    launch path (2026-10-29 UI-log audit: start_services.* launched
    the non-factory app object with no installed mode — the wrong
    app against the wrong data directory — and reported success
    regardless). The retired two-task machinery is gone entirely:
    the single GlossaLab task (register_task.ps1) is the only
    registrar."""
    for rel in (
        "scripts/start_services.cmd",
        "scripts/start_services.ps1",
        "scripts/start_services_safe.ps1",
    ):
        text = _text(rel)
        assert "setup-os.cmd" in text, rel
        assert "glossa_lab.main:app" not in text, rel
        # No direct launch anywhere operational (headers may describe
        # the canonical path, including its --factory entry).
        operational = "\n".join(
            line for line in text.splitlines()
            if not line.lstrip().startswith(("REM", "#", "::"))
        )
        assert "uvicorn" not in operational.lower(), rel
        assert "Start-Process" not in operational, rel
    assert not (REPO / "scripts" / "run-tray-svc.cmd").exists()
    assert not (REPO / "scripts" / "register-tasks.ps1").exists()


def test_shell_setup_propagates_step_failures() -> None:
    """shell.cmd setup must fail loudly when any step fails
    (2026-10-29 audit: it printed [OK] and exited 0 unconditionally,
    so the installers' errorlevel checks could never fire)."""
    text = _text("shell.cmd")
    assert "goto :setup_fail" in text
    assert ":setup_fail" in text
    assert "exit /b 1" in text
    # The callers check the result as well.
    assert "shell.cmd\" setup" in _text("scripts/install-desktop-host.cmd")
    setup_os = _text("setup-os.cmd")
    assert "shell.cmd setup failed" in setup_os


def test_no_timeout_exe_waits_in_windows_scripts() -> None:
    """timeout.exe errors under redirected stdin ("ERROR: Input
    redirection is not supported") and dirtied every successful
    start/restart job log. No operational line of any Windows
    script may use it (2026-10-29 audit)."""
    scripts_dir = REPO / "scripts"
    candidates = [REPO / "shell.cmd", REPO / "setup-os.cmd"]
    candidates += sorted(scripts_dir.glob("*.cmd"))
    candidates += sorted((REPO / "services" / "windows").glob("*.cmd"))
    for path in candidates:
        text = path.read_text(encoding="utf-8", errors="replace")
        operational = "\n".join(
            line for line in text.splitlines()
            if not line.lstrip().upper().startswith("REM")
        )
        assert "timeout /t" not in operational.lower(), str(path)
        assert "timeout.exe" not in operational.lower(), str(path)


def test_c080_10_verify_waits_are_bounded_and_named():
    """Defect 1 (run 40911989844 hung unbounded): every external
    call in the verify script goes through the total-deadline
    helpers; an expired wait emits a named GLOSSA_WAIT marker.
    The only subprocess.run left is the tree-kill inside
    run_bounded itself (timeout-bounded)."""
    source = _text("scripts/verify_desktop_host.py")
    assert "def run_bounded" in source
    assert "def call_bounded" in source
    assert "GLOSSA_WAIT" in source
    assert "VERIFY_DEADLINE_SEC" in source
    assert source.count("subprocess.run(") == 1


def test_c080_11_task_is_a_short_lived_starter():
    """Amendment 4: the task's one action is the starter
    (start-ensure.vbs -> setup-os.cmd start); registration
    carries the logon trigger AND the 15-minute repetition
    tick, IgnoreNew, and a bounded ExecutionTimeLimit; the
    tray launcher is fire-and-forget with a single-instance
    guard and never waits on the tray."""
    reg = _text("scripts/register_task.ps1")
    assert "start-ensure.vbs" in reg
    assert "RepetitionInterval" in reg
    assert "IgnoreNew" in reg
    assert "New-TimeSpan -Minutes 10" in reg
    ensure = _text("scripts/start-ensure.vbs")
    assert "setup-os.cmd" in ensure
    vbs = _text("scripts/launch-tray.vbs")
    assert "glossa_tray" in vbs
    assert "0, False" in vbs  # fire-and-forget: do not wait
    assert "ExecQuery" in vbs  # single-instance guard

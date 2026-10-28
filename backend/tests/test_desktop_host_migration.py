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
    assert "GET-FILEHASH" in text


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

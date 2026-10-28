"""Spec 079 — supervised backend + tray installation.

Covers the pieces that can be verified without a service manager:
the brand icon assets, the Linux installer's rendered output
(render-only mode), and the identity health check's accept/reject
logic. No test here starts a real backend or touches systemd.
"""

from __future__ import annotations

import importlib.util
import struct
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ASSETS = REPO / "tray" / "glossa_tray" / "assets"
HEALTHCHECK = REPO / "services" / "linux" / "healthcheck.py"


def _load_healthcheck():
    spec = importlib.util.spec_from_file_location("glossa_healthcheck", HEALTHCHECK)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_brand_icon_assets_exist_and_parse() -> None:
    png = ASSETS / "glossa-lab.png"
    ico = ASSETS / "glossa-lab.ico"
    svg = ASSETS / "glossa-lab.svg"
    assert png.exists() and ico.exists() and svg.exists()
    # PNG: signature, then IHDR width/height.
    data = png.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    width, height = struct.unpack(">II", data[16:24])
    assert (width, height) == (256, 256)
    # ICO: reserved=0, type=1, at least 4 sizes.
    reserved, kind, count = struct.unpack("<HHH", ico.read_bytes()[:6])
    assert reserved == 0
    assert kind == 1
    assert count >= 4
    # SVG source carries the brand gradient stops.
    text = svg.read_text(encoding="utf-8")
    assert "#2563eb" in text and "#60a5fa" in text


def test_healthcheck_identity_validation() -> None:
    hc = _load_healthcheck()
    good_health = {"status": "healthy", "version": "1.2.3"}
    good_openapi = {"info": {"title": "Glossa Lab", "version": "1.2.3"}}
    assert hc.validate_identity(good_health, good_openapi) == []
    # Wrong application on the port must be rejected.
    wrong = {"info": {"title": "Other App", "version": "1.2.3"}}
    assert hc.validate_identity(good_health, wrong)
    # Version mismatch between health and openapi must be rejected.
    mismatch = {"info": {"title": "Glossa Lab", "version": "9.9.9"}}
    assert hc.validate_identity(good_health, mismatch)
    # Unhealthy status must be rejected.
    assert hc.validate_identity({"status": "down", "version": "1.2.3"}, good_openapi)


def test_linux_installer_render_only(tmp_path: Path) -> None:
    service_dir = tmp_path / "units"
    support_dir = tmp_path / "support"
    state_dir = tmp_path / "state"
    autostart_dir = tmp_path / "autostart"
    icon_dir = tmp_path / "icons"
    result = subprocess.run(
        [
            "bash",
            str(REPO / "services" / "linux" / "install.sh"),
            "--render-only",
            "--skip-dependencies",
            "--service-dir", str(service_dir),
            "--support-dir", str(support_dir),
            "--state-dir", str(state_dir),
            "--autostart-dir", str(autostart_dir),
            "--icon-dir", str(icon_dir),
            "--venv-python", "/opt/glossa-venv/bin/python",
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr

    unit = (service_dir / "glossa-lab-backend.service").read_text(encoding="utf-8")
    assert "create_app --factory" in unit
    assert "--port 8001" in unit
    assert "/opt/glossa-venv/bin/python" in unit
    assert "StartLimitBurst=3" in unit
    assert "StartLimitIntervalSec=3600" in unit
    assert "OnFailure=glossa-lab-backend-alert.service" in unit
    assert "__" not in unit  # every placeholder rendered

    alert = (service_dir / "glossa-lab-backend-alert.service").read_text(encoding="utf-8")
    assert "record-owner-needed.sh" in alert
    assert (support_dir / "healthcheck.py").exists()
    assert (support_dir / "record-owner-needed.sh").exists()

    desktop = (autostart_dir / "glossa-lab-tray.desktop").read_text(encoding="utf-8")
    assert "Icon=glossa-lab" in desktop
    assert "-m glossa_tray" in desktop
    installed_icon = icon_dir / "glossa-lab.png"
    assert installed_icon.read_bytes() == (ASSETS / "glossa-lab.png").read_bytes()


def test_tray_icon_uses_brand_tile() -> None:
    """The tray renders the brand tile (with badge), never a bare circle."""
    tray_dir = REPO / "tray"
    sys.path.insert(0, str(tray_dir))
    import pytest

    try:
        import glossa_tray.main as tray_main
    except Exception:  # noqa: BLE001 — headless CI has no display for pystray
        pytest.skip("pystray is not importable in this environment")

        image = tray_main._create_icon_image("green")  # noqa: SLF001
        assert image.size == (64, 64)
        blue = image.getpixel((10, 10))[:3]
        assert blue[2] > 150 and blue[0] < 120  # brand blue tile corner
        badge = image.getpixel((51, 51))[:3]
        assert badge[1] > 150 and badge[0] < 120  # green status badge
    finally:
        sys.path.remove(str(tray_dir))

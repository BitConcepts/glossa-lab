"""Configuration management for Glossa Lab."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib  # type: ignore[import]
    except ImportError:
        import tomli as tomllib  # type: ignore[import,no-redef]


@dataclass
class Settings:
    """Application settings with platform-aware defaults."""

    # Core
    host: str = "127.0.0.1"
    port: int = 8001
    dev_mode: bool = True
    log_level: str = "DEBUG"

    # Paths (set dynamically based on platform and mode)
    config_dir: Path = field(default_factory=lambda: Path("./config"))
    log_dir: Path = field(default_factory=lambda: Path("./logs"))
    data_dir: Path = field(default_factory=lambda: Path("./data"))


def _platform_paths(mode: str) -> dict[str, Path]:
    """Return platform-specific paths for installed mode."""
    if mode != "installed":
        return {}

    if sys.platform == "win32":
        appdata = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        localappdata = Path(
            os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")
        )
        return {
            "config_dir": appdata / "GlossaLab",
            "log_dir": localappdata / "GlossaLab" / "logs",
            "data_dir": localappdata / "GlossaLab" / "data",
        }
    elif sys.platform == "darwin":
        home = Path.home()
        return {
            "config_dir": home / "Library" / "Application Support" / "GlossaLab",
            "log_dir": home / "Library" / "Logs" / "GlossaLab",
            "data_dir": home / "Library" / "Application Support" / "GlossaLab" / "data",
        }
    else:
        # Linux / other POSIX — follow XDG
        config_home = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        state_home = Path(
            os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state")
        )
        data_home = Path(
            os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")
        )
        return {
            "config_dir": config_home / "glossa-lab",
            "log_dir": state_home / "glossa-lab" / "logs",
            "data_dir": data_home / "glossa-lab",
        }


def _load_toml(config_dir: Path) -> dict:
    """Load TOML config file if it exists. Returns empty dict on missing file."""
    config_file = config_dir / "glossa.toml"
    if config_file.exists():
        with open(config_file, "rb") as f:
            return tomllib.load(f)
    return {}


def _env_overrides() -> dict[str, str]:
    """Collect GLOSSA_ prefixed environment variables."""
    prefix = "GLOSSA_"
    return {
        k[len(prefix) :].lower(): v
        for k, v in os.environ.items()
        if k.startswith(prefix)
    }


@lru_cache
def get_settings() -> Settings:
    """Build settings from defaults → TOML → environment variables."""
    settings = Settings()

    # Determine mode from env
    mode = os.environ.get("GLOSSA_MODE", "dev")
    settings.dev_mode = mode != "installed"

    # Apply platform paths for installed mode
    platform_paths = _platform_paths(mode)
    for key, path in platform_paths.items():
        setattr(settings, key, path)

    # Load TOML config
    toml_data = _load_toml(settings.config_dir)
    for key, value in toml_data.items():
        if hasattr(settings, key):
            setattr(settings, key, value)

    # Apply environment variable overrides
    env = _env_overrides()
    for key, value in env.items():
        if hasattr(settings, key):
            current = getattr(settings, key)
            # Coerce to the correct type
            if isinstance(current, bool):
                setattr(settings, key, value.lower() in ("true", "1", "yes"))
            elif isinstance(current, int):
                setattr(settings, key, int(value))
            elif isinstance(current, Path):
                setattr(settings, key, Path(value))
            else:
                setattr(settings, key, value)

    return settings

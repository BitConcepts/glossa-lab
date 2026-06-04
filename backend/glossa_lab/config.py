"""Configuration management for Glossa Lab.

Contains two layers:

1. ``Settings`` — application settings (host, port, paths, etc.).
2. ``ProjectConfig`` — per-project research parameters loaded from
   ``project.yml`` at the repository root (git-ignored).  Defaults match
   the Indus Script project.
"""

from __future__ import annotations

import logging
import os
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

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
    log_level: str = "INFO"   # DEBUG generates massive aiosqlite spam; use GLOSSA_LOG_LEVEL=DEBUG to override

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
        localappdata = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
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
        state_home = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
        data_home = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
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
    return {k[len(prefix) :].lower(): v for k, v in os.environ.items() if k.startswith(prefix)}


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


# ---------------------------------------------------------------------------
# Project configuration (per-language-project settings)
# ---------------------------------------------------------------------------

_log = logging.getLogger("glossa_lab.config")
_REPO_ROOT = Path(__file__).resolve().parents[2]  # backend -> glossa_lab -> repo_root


@dataclass
class ProjectConfig:
    project_id: str = "indus"
    project_name: str = "Indus Script Decipherment"
    # Paths relative to repo root (resolved at access time)
    corpus_csv: str = "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
    anchors_json: str = "backend/reports/INDUS_FINAL_ANCHORS.json"
    cldf_dir: str = "reports/jambu-dedr/cldf"
    # Project parameters
    sign_total: int = 713
    language_family_bias: str = "Dravidian"
    ai_context_summary: str = ""  # if non-empty, replaces the context block in AG2 system prompt

    def corpus_csv_path(self) -> Path:
        return _REPO_ROOT / self.corpus_csv

    def anchors_json_path(self) -> Path:
        return _REPO_ROOT / self.anchors_json

    def cldf_dir_path(self) -> Path:
        return _REPO_ROOT / self.cldf_dir


_config: ProjectConfig | None = None


def get_project_config() -> ProjectConfig:
    """Return the singleton ProjectConfig, loading from project.yml if present."""
    global _config
    if _config is not None:
        return _config
    _config = _load_config()
    return _config


def reload_project_config() -> ProjectConfig:
    """Force reload from project.yml."""
    global _config
    _config = None
    return get_project_config()


def _load_config() -> ProjectConfig:
    """Load from project.yml at repo root; fall back to Indus defaults."""
    yml_path = _REPO_ROOT / "project.yml"
    if not yml_path.exists():
        return ProjectConfig()
    try:
        import yaml  # type: ignore[import]
        data = yaml.safe_load(yml_path.read_text(encoding="utf-8")) or {}
        return ProjectConfig(**{k: v for k, v in data.items()
                                if k in ProjectConfig.__dataclass_fields__})
    except ImportError:
        # PyYAML not installed — try basic key: value parsing
        data_fallback: dict[str, Any] = {}
        for line in yml_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and ":" in line:
                k, _, v = line.partition(":")
                data_fallback[k.strip()] = v.strip()
        return ProjectConfig(**{k: v for k, v in data_fallback.items()
                                if k in ProjectConfig.__dataclass_fields__})
    except Exception as exc:
        _log.warning("Failed to load project.yml: %s — using defaults", exc)
        return ProjectConfig()

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
class PhaseGoal:
    """A research phase milestone."""
    phase: int
    label: str
    description: str
    min_coverage: float   # corpus_token_coverage lower bound (inclusive)
    max_coverage: float   # corpus_token_coverage upper bound (exclusive, use 1.01 for 'done')
    recommended_experiments: list = field(default_factory=list)  # list of experiment IDs
    recommended_actions: list = field(default_factory=list)       # list of action dicts


_DEFAULT_PHASE_GOALS: list[PhaseGoal] = [
    PhaseGoal(
        phase=1, label="Bootstrap",
        description=(
            "Run SA experiments to find initial anchor candidates. "
            "Each experiment queues as a background job — monitor progress in the Jobs panel. "
            "After jobs complete, use the Research Loop (below) to mine literature for corroborating evidence."
        ),
        min_coverage=0.0, max_coverage=0.30,
        recommended_experiments=[
            "indus_sa_dravidian_syllable",
            "indus_dravidian_vs_sanskrit",
            "generic_sa_multi_comparison",
        ],
        recommended_actions=[
            {"action_type": "run_experiment",
             "label": "Queue SA: Dravidian Syllable LM",
             "rationale": "Establishes initial syllable-level anchor candidates via SA",
             "params": {"experiment_id": "indus_sa_dravidian_syllable"}},
            {"action_type": "run_experiment",
             "label": "Queue SA: Multi-Language Comparison",
             "rationale": "Compares Dravidian vs Sanskrit vs Hebrew to find best-fit language",
             "params": {"experiment_id": "generic_sa_multi_comparison"}},
        ],
    ),
    PhaseGoal(
        phase=2, label="Growth",
        description=(
            "Expand anchor coverage with broader SA experiments. "
            "All actions queue background jobs — check the Jobs panel for results. "
            "Use the Research Loop separately to find literature-backed candidates."
        ),
        min_coverage=0.30, max_coverage=0.60,
        recommended_experiments=[
            "indus_cisi_dravidian_vs_sanskrit",
            "indus_anchor_sweep",
            "generic_sa_multi_comparison",
        ],
        recommended_actions=[
            {"action_type": "run_experiment",
             "label": "Queue SA: CISI Dravidian vs Sanskrit",
             "rationale": "Full-corpus SA with current anchors to widen coverage",
             "params": {"experiment_id": "indus_cisi_dravidian_vs_sanskrit"}},
            {"action_type": "run_experiment",
             "label": "Queue Anchor Sweep",
             "rationale": "Tests how SA consistency improves as anchor count grows",
             "params": {"experiment_id": "indus_anchor_sweep"}},
        ],
    ),
    PhaseGoal(
        phase=3, label="Validation",
        description=(
            "Validate and falsify anchor assignments with held-out data and negative controls. "
            "All actions queue background jobs. "
            "Use the Research Loop to find literature evidence for disputed readings."
        ),
        min_coverage=0.60, max_coverage=0.85,
        recommended_experiments=[
            "indus_validation_a1_a3_holdout",
            "indus_validation_neg_controls",
            "indus_cisi_structural",
        ],
        recommended_actions=[
            {"action_type": "run_experiment",
             "label": "Queue A1–A3 Holdout Validation",
             "rationale": "Cross-validates anchor assignments on withheld inscription data",
             "params": {"experiment_id": "indus_validation_a1_a3_holdout"}},
            {"action_type": "run_experiment",
             "label": "Queue Negative Controls",
             "rationale": "Falsification: verifies SA beats random assignment",
             "params": {"experiment_id": "indus_validation_neg_controls"}},
        ],
    ),
    PhaseGoal(
        phase=4, label="Completion",
        description=(
            "Fill remaining gaps to reach 95%+ coverage. "
            "Run structural experiments to identify unanchored sign clusters. "
            "Use the Research Loop to mine literature for the remaining hard cases."
        ),
        min_coverage=0.85, max_coverage=0.95,
        recommended_experiments=[
            "indus_structural_atlas",
            "indus_cgsa_cluster_analysis",
        ],
        recommended_actions=[
            {"action_type": "run_experiment",
             "label": "Queue Structural Atlas",
             "rationale": "Maps unanchored signs by structural similarity to anchored ones",
             "params": {"experiment_id": "indus_structural_atlas"}},
            {"action_type": "run_experiment",
             "label": "Queue CGSA Cluster Analysis",
             "rationale": "Groups remaining signs by corpus-graph clustering",
             "params": {"experiment_id": "indus_cgsa_cluster_analysis"}},
        ],
    ),
    PhaseGoal(
        phase=5, label="Done",
        description=(
            "Target reached: ≥95% corpus token coverage. "
            "Complete these validation steps to confirm the decipherment: "
            "(1) Run SA experiments to validate anchor consistency at the new coverage level, "
            "(2) Regenerate AI Insights once experiments complete to reflect the updated anchor set, "
            "(3) Review promoted signs to spot-check readings and mark any incorrect ones. "
            "The Phase Guide will walk you through each step in order."
        ),
        min_coverage=0.95, max_coverage=1.01,
        recommended_experiments=[
            "indus_cisi_dravidian_vs_sanskrit",
            "indus_anchor_sweep",
        ],
        recommended_actions=[
            {"action_type": "regenerate_insights", "label": "Regenerate AI Insights",
             "rationale": (
                 "SA experiments complete — regenerate the AI insight now so it reflects "
                 "the validated anchor set and 96%+ coverage."
             ),
             "params": {}},
            {"action_type": "open_view", "label": "Review Promoted Signs",
             "rationale": "Spot-check newly promoted signs in the Signs index. "
                          "Verify readings, mark any incorrect ones for re-review.",
             "params": {"view": "signs"}},
        ],
    ),
    PhaseGoal(
        phase=6, label="Peer Review",
        description=(
            "Decipherment validated at 95%+ coverage. Prepare for external review: "
            "(1) Run Kalyanaraman cross-validation as independent second-source check, "
            "(2) Run full falsification suite (negative controls, Sanskrit falsification), "
            "(3) Generate the foundation report PDF for sharing."
        ),
        min_coverage=0.95, max_coverage=1.01,
        recommended_experiments=[
            "indus_kalyanaraman_crossval",
            "indus_validation_neg_controls",
            "indus_sa_sanskrit_falsification",
        ],
        recommended_actions=[
            {"action_type": "run_experiment",
             "label": "Queue Kalyanaraman Cross-Validation",
             "rationale": "Independent second-source validation against 52 rebus papers",
             "params": {"experiment_id": "indus_kalyanaraman_crossval"}},
            {"action_type": "run_experiment",
             "label": "Queue Sanskrit Falsification",
             "rationale": "Confirm Dravidian SA beats Sanskrit SA (language family validation)",
             "params": {"experiment_id": "indus_sa_sanskrit_falsification"}},
            {"action_type": "open_view", "label": "Generate Foundation Report",
             "rationale": "Create a PDF summary of all validation results for external review.",
             "params": {"view": "foundation"}},
        ],
    ),
    PhaseGoal(
        phase=7, label="Publication",
        description=(
            "All validations passed, falsification checks complete. "
            "The decipherment is ready for academic publication. "
            "Final steps: review the full report, prepare submission materials."
        ),
        min_coverage=0.95, max_coverage=1.01,
        recommended_experiments=[],
        recommended_actions=[
            {"action_type": "open_view", "label": "Review Final Report",
             "rationale": "Review the complete foundation check report and evidence chain.",
             "params": {"view": "foundation"}},
        ],
    ),
]


def _load_dynamic_or_default_goals() -> list:
    """Load phase goals from outputs/phase_goals.json if available, else use defaults."""
    try:
        from glossa_lab.pipelines.phase_generator import load_phase_goals, goals_to_phase_goals  # noqa: PLC0415
        saved = load_phase_goals()
        if saved:
            return goals_to_phase_goals(saved)
    except Exception:  # noqa: BLE001
        pass
    return list(_DEFAULT_PHASE_GOALS)


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
    phase_goals: list = field(default_factory=lambda: _load_dynamic_or_default_goals())

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

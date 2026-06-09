"""Lazy-loading, thread-safe CLDF reader for JAMBU DEDR data.

Reads CSV files from ``reports/jambu-dedr/cldf/`` and returns normalised
dicts.  All caches are keyed by *resolved* ``cldf_dir`` path so callers
can point to alternative directories for testing.

Only stdlib is used: csv, json, pathlib, threading, logging.
"""

from __future__ import annotations

import csv
import logging
import threading
from pathlib import Path

_log = logging.getLogger(__name__)

# Repo root is four levels up from this file:
#   data → glossa_lab → backend → <repo-root>
_REPO_ROOT = Path(__file__).resolve().parents[3]

# ── Column mappings ──────────────────────────────────────────────
# Map actual CSV header names to normalised keys.  The first match wins.
_FORM_COL_MAP: dict[str, str] = {
    "ID": "form_id",
    "Language_ID": "language_id",
    "Parameter_ID": "parameter_id",
    "Form": "form",
    "Gloss": "gloss",
    "Native": "native_script",
    "Phonemic": "ipa",
    "Source": "source",
    "Description": "description",
    "Original": "original",
    "Cognateset": "cognateset",
    "Native_Script": "native_script",
    "IPA": "ipa",
    "Segments": "segments",
    "Comment": "comment",
    "Variants": "variants",
}

_LANG_COL_MAP: dict[str, str] = {
    "ID": "language_id",
    "Name": "name",
    "Glottocode": "glottocode",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Clade": "family",
    "Family": "family",
    "ISO": "iso",
    "ISO639P3code": "iso",
}

_PARAM_COL_MAP: dict[str, str] = {
    "ID": "parameter_id",
    "Name": "name",
    "Description": "description",
    "Language_ID": "language_id",
    "Etyma": "etyma",
}

# ── Cache & lock ─────────────────────────────────────────────────
_cache_lock = threading.Lock()
_forms_cache: dict[str, list[dict]] = {}
_languages_cache: dict[str, list[dict]] = {}
_parameters_cache: dict[str, list[dict]] = {}


# ── Helpers ──────────────────────────────────────────────────────

def get_cldf_dir() -> Path:
    """Return the default CLDF directory."""
    return _REPO_ROOT / "reports" / "jambu-dedr" / "cldf"


def _resolve_dir(cldf_dir: Path | None) -> Path:
    return (cldf_dir or get_cldf_dir()).resolve()


def _read_csv(path: Path, col_map: dict[str, str]) -> list[dict]:
    """Read a CSV file and return rows as dicts with normalised keys."""
    if not path.exists():
        _log.warning("CLDF file not found: %s", path)
        return []
    rows: list[dict] = []
    try:
        with path.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                normalised: dict[str, str] = {}
                for csv_col, norm_key in col_map.items():
                    if norm_key not in normalised:
                        normalised[norm_key] = row.get(csv_col, "")
                rows.append(normalised)
    except Exception:
        _log.warning("Failed to read CLDF file: %s", path, exc_info=True)
        return []
    return rows


# ── Public loaders ───────────────────────────────────────────────

def load_forms(cldf_dir: Path | None = None) -> list[dict]:
    """Load ``forms.csv`` and return a list of normalised dicts."""
    key = str(_resolve_dir(cldf_dir))
    if key in _forms_cache:
        return _forms_cache[key]
    data = _read_csv(_resolve_dir(cldf_dir) / "forms.csv", _FORM_COL_MAP)
    with _cache_lock:
        _forms_cache[key] = data
    return data


def load_languages(cldf_dir: Path | None = None) -> list[dict]:
    """Load ``languages.csv`` and return a list of normalised dicts."""
    key = str(_resolve_dir(cldf_dir))
    if key in _languages_cache:
        return _languages_cache[key]
    data = _read_csv(_resolve_dir(cldf_dir) / "languages.csv", _LANG_COL_MAP)
    with _cache_lock:
        _languages_cache[key] = data
    return data


def load_parameters(cldf_dir: Path | None = None) -> list[dict]:
    """Load ``parameters.csv`` and return a list of normalised dicts."""
    key = str(_resolve_dir(cldf_dir))
    if key in _parameters_cache:
        return _parameters_cache[key]
    data = _read_csv(_resolve_dir(cldf_dir) / "parameters.csv", _PARAM_COL_MAP)
    with _cache_lock:
        _parameters_cache[key] = data
    return data


# ── Convenience queries ──────────────────────────────────────────

def get_forms_by_parameter(parameter_id: str, cldf_dir: Path | None = None) -> list[dict]:
    """Return all forms matching *parameter_id* (DEDR entry)."""
    return [f for f in load_forms(cldf_dir) if f.get("parameter_id") == parameter_id]


def get_forms_by_language(language_id: str, cldf_dir: Path | None = None) -> list[dict]:
    """Return all forms matching *language_id*."""
    return [f for f in load_forms(cldf_dir) if f.get("language_id") == language_id]


def get_cldf_summary(cldf_dir: Path | None = None) -> dict:
    """Return a high-level summary of the CLDF dataset."""
    forms = load_forms(cldf_dir)
    languages = load_languages(cldf_dir)
    parameters = load_parameters(cldf_dir)
    families: dict[str, int] = {}
    for lang in languages:
        fam = lang.get("family", "") or "unknown"
        families[fam] = families.get(fam, 0) + 1
    return {
        "n_forms": len(forms),
        "n_languages": len(languages),
        "n_parameters": len(parameters),
        "families": families,
    }


def invalidate_cldf_cache() -> None:
    """Clear all CLDF caches."""
    with _cache_lock:
        _forms_cache.clear()
        _languages_cache.clear()
        _parameters_cache.clear()

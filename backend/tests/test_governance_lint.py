"""Phase 5: Governance lint — H16 enforcement.

Scans experiments/ and scripts/ for patterns that indicate study-specific
data (hardcoded anchor dicts, hardcoded corpus names, hardcoded report titles)
outside of clearly _legacy_-prefixed files.

These patterns are governance violations per H15/H16:
  - Python files in experiments/ should contain ONLY atomic primitive logic.
  - No study-specific corpus names, anchor values, or template strings.

Note: Existing legacy files are whitelisted explicitly. New files that
introduce the patterns will fail this test.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

_BACKEND_DIR = Path(__file__).resolve().parent.parent
_EXP_DIR     = _BACKEND_DIR / "glossa_lab" / "experiments"
_SCRIPTS_DIR = _BACKEND_DIR / "scripts"

# Files that are explicitly permitted to contain historical hardcoded content.
# All Python experiment compositions have been migrated to graph specs in
# experiments/graphs/*.json and archived to experiments/_legacy/.
# The experiments/ directory now contains only _parallel.py (utility),
# __init__.py, and __main__.py — none of which need whitelisting.
#
# This whitelist covers only scripts/ directory files that retain
# legacy report-generation logic pending full ReportGenerator node migration.
_LEGACY_WHITELIST: set[str] = {
    # Report generator scripts (pending replacement by ReportGenerator node)
    "generate_geez_report.py",
    "generate_geez_convergence_report.py",
    "generate_fuls_nw_semitic_report.py",
    "_save_benchmark_reports.py",
    "run_fuls_rtl.py",
    # Runner scripts (H16 compliant; allowed to reference specific experiments by ID)
    "run_geez_decipher.py",
    "run_geez_anchor_convergence.py",
}

# Patterns that indicate hardcoded study-specific data in non-whitelisted files
_HARDCODED_ANCHOR_PATTERNS = [
    re.compile(r'"[0-9]{3}":\s*"[A-Za-z]"'),   # e.g. "004": "T"
    re.compile(r'fuls_verified_anchors\s*=\s*\{'),
    re.compile(r'"anchors"\s*:\s*\{[^}]{10,}\}'),
]

_HARDCODED_CORPUS_NAME_PATTERNS = [
    re.compile(r'corpus\s*=\s*"(nw_semitic|old_hebrew|geez|phoenician|ugaritic)"'),
    re.compile(r'language\s*=\s*"(hebrew|coptic|dravidian|sumerian)"'),
]

_HARDCODED_REPORT_TITLE_PATTERNS = [
    re.compile(r'"(Dr\. Fuls|Fuls NW Semitic|Geez Anchor Convergence)\s+Report"'),
    re.compile(r'report_title\s*=\s*"[^"]{20,}"'),
]


def _is_new_file(path: Path) -> bool:
    """Return True if the file is NOT in the whitelist and NOT a private helper."""
    name = path.name
    if name.startswith("_") or name in _LEGACY_WHITELIST:
        return False
    return True


def _scan_for_patterns(path: Path, patterns: list[re.Pattern]) -> list[str]:
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    return [str(path.relative_to(_BACKEND_DIR)) for pat in patterns if pat.search(src)]


def test_no_new_hardcoded_anchors_in_experiments():
    """New experiment files must not contain hardcoded anchor dicts."""
    violations = []
    for path in _EXP_DIR.glob("*.py"):
        if _is_new_file(path):
            hits = _scan_for_patterns(path, _HARDCODED_ANCHOR_PATTERNS)
            violations.extend(hits)
    assert violations == [], (
        "H16 violation: hardcoded anchor dicts found in new experiment files:\n"
        + "\n".join(violations)
        + "\nMove anchor pairs to an AnchorSet in the database instead."
    )


def test_no_new_hardcoded_corpus_names_in_experiments():
    """New experiment files must not hardcode corpus names as string literals."""
    violations = []
    for path in _EXP_DIR.glob("*.py"):
        if _is_new_file(path):
            hits = _scan_for_patterns(path, _HARDCODED_CORPUS_NAME_PATTERNS)
            violations.extend(hits)
    assert violations == [], (
        "H16 violation: hardcoded corpus names found in new experiment files:\n"
        + "\n".join(violations)
        + "\nUse BuiltinCorpus/CorpusLM nodes or CorpusReader with a corpus_id instead."
    )


def test_no_new_hardcoded_report_titles_in_scripts():
    """New script files must not hardcode study-specific report titles."""
    violations = []
    for path in _SCRIPTS_DIR.glob("*.py"):
        if _is_new_file(path):
            hits = _scan_for_patterns(path, _HARDCODED_REPORT_TITLE_PATTERNS)
            violations.extend(hits)
    assert violations == [], (
        "H16 violation: hardcoded report titles found in new script files:\n"
        + "\n".join(violations)
        + "\nUse a user-defined ReportTemplate from the database instead."
    )


def test_new_experiment_files_are_not_experiment_base_subclasses():
    """New experiment Python files must NOT define ExperimentBase subclasses.

    Per H15/H16: all experiments are graph specs in experiments/graphs/*.json.
    Python files in experiments/ must only contain atomic primitive logic.
    """
    violations = []
    for path in _EXP_DIR.glob("*.py"):
        if not _is_new_file(path):
            continue
        try:
            src = path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(src)
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    base_name = (
                        base.id if isinstance(base, ast.Name) else
                        base.attr if isinstance(base, ast.Attribute) else ""
                    )
                    if base_name == "ExperimentBase":
                        violations.append(
                            f"{path.name}: class {node.name}(ExperimentBase)"
                        )
    assert violations == [], (
        "H15/H16 violation: ExperimentBase subclass in non-whitelisted file:\n"
        + "\n".join(violations)
        + "\nCreate a graph spec in experiments/graphs/<id>.json instead."
    )

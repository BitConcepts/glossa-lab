"""Registry self-check for the experiment atomic-node registry (Spec 087 S1).

The registry in experiment_graph.py is built from a core list plus 144
plugin modules (experiment_graph_*.py), each imported by name in a
try/except block. Before Spec 087 those blocks logged only a warning on
failure, so a broken module silently shrunk the registry (audit finding
F1), and duplicate node ids silently overwrote each other (F2).

This module is the independent check the completeness test (and anyone
else) can run against that build:

- loader_plugin_imports() re-derives the expected plugin module list from
  experiment_graph.py's own import statements — the loader is the source
  of truth for what should register;
- collect_plugin_nodes() imports each plugin module and calls exactly the
  *_node_defs functions the loader imports, collecting the node ids each
  module produces;
- registry_self_check() compares that independent production against
  ATOMIC_NODES: every plugin module must import and produce, no node id
  may be produced twice, and every produced id must be registered.
  Since Spec 087 S2 it also checks the legacy split: the definitions
  flagged legacy must be exactly the S2 migration data file's id set.

The runtime build records its own failures/duplicates as it goes (see
registry_build_report() in experiment_graph.py, served at
GET /experiment-graphs/registry-health); this module's check is the
from-scratch recomputation that keeps the record honest.
"""
from __future__ import annotations

import ast
import importlib
from collections import Counter
from pathlib import Path
from typing import Any

_EXPERIMENT_GRAPH_PY = Path(__file__).parent / "experiment_graph.py"
_PLUGIN_PREFIX = "glossa_lab.experiment_graph_"


def loader_plugin_imports() -> list[tuple[str, list[str]]]:
    """(module, [imported *_node_defs names]) for every plugin import in
    experiment_graph.py, in file order, one entry per import statement."""
    tree = ast.parse(_EXPERIMENT_GRAPH_PY.read_text(encoding="utf-8"))
    imports: list[tuple[str, list[str]]] = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.ImportFrom)
            and node.module is not None
            and node.module.startswith(_PLUGIN_PREFIX)
        ):
            imports.append((node.module, [a.name for a in node.names]))
    return imports


def expected_plugin_modules() -> list[str]:
    """Distinct plugin module names the loader imports, in file order."""
    seen: list[str] = []
    for module, _ in loader_plugin_imports():
        if module not in seen:
            seen.append(module)
    return seen


def collect_plugin_nodes(
    imports: list[tuple[str, list[str]]] | None = None,
) -> tuple[dict[str, list[str]], list[dict[str, str]]]:
    """Import every plugin module and call the defs functions the loader
    imports from it.

    Returns (sources, errors): sources maps node id -> list of producing
    "module:function" strings (more than one entry = a duplicate id);
    errors lists {"module", "error"} for modules that fail to import or
    whose defs function raises or is missing.
    """
    if imports is None:
        imports = loader_plugin_imports()
    sources: dict[str, list[str]] = {}
    errors: list[dict[str, str]] = []
    for module_name, fn_names in imports:
        try:
            module = importlib.import_module(module_name)
        except Exception as exc:  # noqa: BLE001
            errors.append(
                {"module": module_name, "error": f"{type(exc).__name__}: {exc}"}
            )
            continue
        for fn_name in fn_names:
            fn = getattr(module, fn_name, None)
            if fn is None:
                errors.append(
                    {"module": module_name, "error": f"missing defs function {fn_name}"}
                )
                continue
            try:
                defs = fn()
            except Exception as exc:  # noqa: BLE001
                errors.append(
                    {
                        "module": module_name,
                        "error": f"{fn_name}() raised {type(exc).__name__}: {exc}",
                    }
                )
                continue
            for node_def in defs:
                sources.setdefault(node_def.id, []).append(f"{module_name}:{fn_name}")
    return sources, errors


def duplicate_node_id_literals() -> dict[str, list[str]]:
    """Scan every experiment_graph*.py source for AtomicNodeDef id literals
    (positional or keyword) defined in more than one place.

    Catches duplicate definitions even where one copy is never returned by
    a defs function — the runtime production check cannot see those.
    Dynamically constructed ids (f-strings, variables) are invisible to a
    literal scan; the production check in registry_self_check() covers
    everything the loader actually registers.
    """
    occurrences: dict[str, list[str]] = {}
    for path in sorted(Path(__file__).parent.glob("experiment_graph*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if not (isinstance(func, ast.Name) and func.id == "AtomicNodeDef"):
                continue
            id_literal: str | None = None
            if node.args and isinstance(node.args[0], ast.Constant):
                if isinstance(node.args[0].value, str):
                    id_literal = node.args[0].value
            if id_literal is None:
                for keyword in node.keywords:
                    if keyword.arg == "id" and isinstance(keyword.value, ast.Constant):
                        if isinstance(keyword.value.value, str):
                            id_literal = keyword.value.value
            if id_literal is not None:
                occurrences.setdefault(id_literal, []).append(
                    f"{path.name}:{node.lineno}"
                )
    return {i: sites for i, sites in occurrences.items() if len(sites) > 1}


def registry_self_check() -> dict[str, Any]:
    """Recompute the registry from its sources and compare with ATOMIC_NODES.

    ok is True only when: every plugin module imports and produces, no
    node id is produced by more than one source, every produced id is
    registered, the runtime build recorded no failures or duplicates, and
    (Spec 087 S2) the set of definitions flagged legacy is exactly the S2
    migration data file's id set.
    """
    from glossa_lab.experiment_graph import (
        ATOMIC_NODES,
        load_legacy_migration_ids,
        registry_build_report,
    )

    sources, errors = collect_plugin_nodes()
    produced = set(sources)
    registered = set(ATOMIC_NODES)
    duplicates = [
        {"id": node_id, "sources": srcs}
        for node_id, srcs in sorted(sources.items())
        if len(srcs) > 1
    ]
    by_category = Counter(d.category for d in ATOMIC_NODES.values())
    build_report = registry_build_report()
    flagged = {node_id for node_id, d in ATOMIC_NODES.items() if d.legacy}
    try:
        migration_ids = set(load_legacy_migration_ids())
        legacy_mismatch = {
            "flagged_not_in_migration": sorted(flagged - migration_ids),
            "in_migration_not_flagged": sorted(migration_ids - flagged),
        }
    except Exception as exc:  # noqa: BLE001
        legacy_mismatch = {
            "flagged_not_in_migration": [],
            "in_migration_not_flagged": [],
            "migration_error": f"{type(exc).__name__}: {exc}",
        }
    legacy_agrees = not legacy_mismatch["flagged_not_in_migration"] and not (
        legacy_mismatch["in_migration_not_flagged"]
    ) and "migration_error" not in legacy_mismatch
    return {
        "ok": (
            not errors
            and not duplicates
            and produced <= registered
            and build_report["ok"]
            and legacy_agrees
        ),
        "registered_total": len(ATOMIC_NODES),
        "by_category": dict(sorted(by_category.items())),
        "plugin_modules_expected": len(expected_plugin_modules()),
        "plugin_module_errors": errors,
        "duplicate_ids": duplicates,
        "produced_not_registered": sorted(produced - registered),
        "core_registered": len(registered - produced),
        "build_report_ok": build_report["ok"],
        "legacy_total": len(flagged),
        "palette_total": len(ATOMIC_NODES) - len(flagged),
        "legacy_mismatch": legacy_mismatch,
    }


def assert_registry_complete(check: dict[str, Any] | None = None) -> None:
    """Raise RuntimeError naming every defect in the self-check result."""
    if check is None:
        check = registry_self_check()
    if check["ok"]:
        return
    problems: list[str] = []
    for err in check["plugin_module_errors"]:
        problems.append(f"module {err['module']}: {err['error']}")
    for dup in check["duplicate_ids"]:
        problems.append(f"duplicate node id {dup['id']} from {dup['sources']}")
    for node_id in check["produced_not_registered"]:
        problems.append(f"node id {node_id} produced but not registered")
    if not check["build_report_ok"]:
        problems.append("runtime registry build report is not ok")
    mismatch = check.get("legacy_mismatch") or {}
    for node_id in mismatch.get("flagged_not_in_migration", []):
        problems.append(f"node id {node_id} flagged legacy but not in the S2 migration data")
    for node_id in mismatch.get("in_migration_not_flagged", []):
        problems.append(f"S2 migration id {node_id} is not flagged legacy")
    if "migration_error" in mismatch:
        problems.append(f"S2 migration data unreadable: {mismatch['migration_error']}")
    raise RuntimeError("Registry self-check failed: " + "; ".join(problems))

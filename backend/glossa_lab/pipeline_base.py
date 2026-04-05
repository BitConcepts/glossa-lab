"""Base class for Glossa Lab pipeline plugins.

A pipeline is a Python file in backend/glossa_lab/pipelines/ that either:
  1. Uses the @register_pipeline("name") decorator (legacy, still supported), or
  2. Defines a class inheriting PipelineBase (preferred, enables richer metadata)

Pipeline files are auto-discovered by the engine.
"""

from __future__ import annotations

import inspect
import shutil
import sys
from pathlib import Path
from typing import Any, ClassVar

_PIPELINES_DIR = Path(__file__).parent / "pipelines"


class PipelineBase:
    """Base class for Glossa Lab pipelines with rich metadata."""

    id: ClassVar[str] = ""
    label: ClassVar[str] = ""
    group: ClassVar[str] = "Statistical (no LM)"
    description: ClassVar[str] = ""
    inputs: ClassVar[str] = "text_id"
    outputs: ClassVar[str] = ""
    # eslint-disable-next-line @typescript-eslint/no-explicit-any
    default_params: ClassVar[dict[str, Any]] = {}
    needs_lm: ClassVar[bool] = False
    report_schema: ClassVar[dict | None] = None

    async def run(self, params: dict[str, Any]) -> dict[str, Any]:
        """Execute the pipeline. Override in subclasses."""
        raise NotImplementedError(f"{self.__class__.__name__}.run() not implemented")

    @classmethod
    def to_dict(cls) -> dict[str, Any]:
        return {
            "id": cls.id,
            "label": cls.label or cls.id.replace("_", " ").title(),
            "group": cls.group,
            "description": cls.description,
            "inputs": cls.inputs,
            "outputs": cls.outputs,
            "default_params": cls.default_params,
            "needs_lm": cls.needs_lm,
            "registered": True,
            "module": _source_module(cls),
            "report_schema": cls.report_schema,
        }


def _source_module(cls: type) -> str:
    try:
        return cls.__module__
    except AttributeError:
        return ""


# ── Pipeline file management ──────────────────────────────────────────


def import_pipeline_file(source_path: str) -> dict[str, Any]:
    """Copy a pipeline .py file into glossa_lab/pipelines/ and invalidate the engine cache."""
    src = Path(source_path)
    if not src.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")
    dest = _PIPELINES_DIR / src.name
    shutil.copy2(str(src), str(dest))
    _invalidate_engine_cache()
    return {"imported": True, "file": dest.name}


def delete_pipeline_file(pipeline_id: str) -> dict[str, Any]:
    """Delete a pipeline file (only user-added ones, not built-in)."""
    from glossa_lab.engine import _PIPELINES, _ensure_pipelines_loaded
    _ensure_pipelines_loaded()
    fn = _PIPELINES.get(pipeline_id)
    if fn is None:
        raise KeyError(f"Pipeline not found: {pipeline_id}")
    try:
        src = Path(inspect.getfile(fn))
    except (TypeError, OSError):
        raise ValueError(f"Cannot determine source file for pipeline: {pipeline_id}")
    if not src.is_relative_to(_PIPELINES_DIR):
        raise ValueError(f"Cannot delete built-in pipeline: {pipeline_id}")
    deleted_name = src.name
    src.unlink()
    _invalidate_engine_cache()
    return {"deleted": True, "file": deleted_name}


def duplicate_pipeline_file(
    pipeline_id: str,
    new_id: str | None = None,
) -> dict[str, Any]:
    """Duplicate a pipeline file with a new id."""
    import re

    from glossa_lab.engine import _PIPELINES, _ensure_pipelines_loaded
    _ensure_pipelines_loaded()
    fn = _PIPELINES.get(pipeline_id)
    if fn is None:
        raise KeyError(f"Pipeline not found: {pipeline_id}")
    try:
        src = Path(inspect.getfile(fn))
    except (TypeError, OSError):
        raise ValueError(f"Cannot determine source file for pipeline: {pipeline_id}")

    safe_new_id = new_id or f"{pipeline_id}_copy"
    dest = _PIPELINES_DIR / f"{safe_new_id}.py"
    content = src.read_text(encoding="utf-8")
    # Replace the register_pipeline decorator name
    content = re.sub(
        r'register_pipeline\(["\']' + re.escape(pipeline_id) + r'["\']',
        f'register_pipeline("{safe_new_id}"',
        content,
    )
    dest.write_text(content, encoding="utf-8")
    _invalidate_engine_cache()
    return {"duplicated": True, "new_file": dest.name, "new_id": safe_new_id}


def _invalidate_engine_cache() -> None:
    """Force the engine to re-discover pipelines."""
    try:
        import glossa_lab.engine as eng
        eng._PIPELINE_MODULES_LOADED = False
        eng._PIPELINES.clear()
        # Remove cached modules so they're re-imported
        to_remove = [k for k in sys.modules if k.startswith("glossa_lab.pipelines.")]
        for k in to_remove:
            del sys.modules[k]
    except Exception:
        pass

"""Base class for Glossa Lab experiments.

All experiment files in backend/experiments/ that define a class inheriting
from ExperimentBase are automatically discovered and registered.

Usage:
    class MyExperiment(ExperimentBase):
        id = "my_experiment"
        name = "My Experiment"
        category = "Analysis"
        description = "What this experiment does."
        estimated_time = "~1 min"
        requires_key: str | None = None          # e.g. "mistral_api_key"
        report_schema: dict | None = None        # JSON schema for the output report

        def run(self, **kwargs) -> dict:
            ...
            return {"result": ...}
"""

from __future__ import annotations

import importlib
import importlib.util
import inspect
import sys
from pathlib import Path
from typing import Any, ClassVar

_EXPERIMENTS_DIR = Path(__file__).parent / "experiments"


class ExperimentBase:
    """Abstract base class for all Glossa Lab experiments."""

    # --- Class-level metadata (override in subclasses) ---
    id: ClassVar[str] = ""
    name: ClassVar[str] = ""
    category: ClassVar[str] = "Analysis"
    description: ClassVar[str] = ""
    estimated_time: ClassVar[str] = "unknown"
    requires_key: ClassVar[str | None] = None
    command: ClassVar[str] = ""  # CLI equivalent for reference
    results_file: ClassVar[str | None] = None
    report_schema: ClassVar[dict | None] = None   # JSON Schema for the output
    params_schema: ClassVar[dict | None] = None   # JSON Schema for run() kwargs

    def run(self, **kwargs: Any) -> dict[str, Any]:
        """Execute the experiment. Override in subclasses."""
        raise NotImplementedError(f"{self.__class__.__name__}.run() not implemented")

    @classmethod
    def to_dict(cls) -> dict[str, Any]:
        """Return experiment metadata as a dict (for the catalog API)."""
        return {
            "id": cls.id,
            "name": cls.name,
            "category": cls.category,
            "description": cls.description,
            "estimated_time": cls.estimated_time,
            "requires_key": cls.requires_key,
            "command": cls.command,
            "results_file": cls.results_file,
            "report_schema": cls.report_schema,
            "params_schema": cls.params_schema,
            "source_file": _source_file(cls),
            "custom": False,
        }


def _source_file(cls: type) -> str:
    try:
        return str(Path(inspect.getfile(cls)).relative_to(Path(__file__).parent.parent.parent))
    except (ValueError, TypeError):
        return ""


# ── Auto-discovery ────────────────────────────────────────────────────

_registry: dict[str, type[ExperimentBase]] | None = None


def discover_experiments() -> dict[str, type[ExperimentBase]]:
    """Scan backend/experiments/ for ExperimentBase subclasses.

    Returns a dict mapping experiment id -> class.
    Results are cached after the first call.
    """
    global _registry
    if _registry is not None:
        return _registry

    _registry = {}
    if not _EXPERIMENTS_DIR.exists():
        return _registry

    for path in sorted(_EXPERIMENTS_DIR.glob("*.py")):
        if path.name.startswith("_"):
            continue
        try:
            module_name = f"_glossa_exp_{path.stem}"
            if module_name not in sys.modules:
                spec = importlib.util.spec_from_file_location(module_name, path)
                if spec is None or spec.loader is None:
                    continue
                mod = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = mod
                spec.loader.exec_module(mod)  # type: ignore[union-attr]
            else:
                mod = sys.modules[module_name]

            for _name, obj in inspect.getmembers(mod, inspect.isclass):
                if issubclass(obj, ExperimentBase) and obj is not ExperimentBase and obj.id:
                    _registry[obj.id] = obj
        except Exception:
            pass  # Skip files that fail to import

    return _registry


def invalidate_cache() -> None:
    """Clear the discovery cache (called after import/delete)."""
    global _registry
    _registry = None


def list_discovered_experiments() -> list[dict[str, Any]]:
    """Return metadata for all discovered experiments."""
    return [cls.to_dict() for cls in discover_experiments().values()]


def get_experiment(experiment_id: str) -> type[ExperimentBase] | None:
    """Return a discovered experiment class by id, or None."""
    return discover_experiments().get(experiment_id)


# ── Experiment file management ─────────────────────────────────────────


def import_experiment_file(source_path: str) -> dict[str, Any]:
    """Copy an experiment file into the experiments directory and discover it."""
    src = Path(source_path)
    if not src.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")
    _EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)
    dest = _EXPERIMENTS_DIR / src.name
    dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    invalidate_cache()
    return {"imported": True, "file": dest.name}


def delete_experiment_file(experiment_id: str) -> dict[str, Any]:
    """Delete an experiment file from the experiments directory."""
    cls = get_experiment(experiment_id)
    if cls is None:
        raise KeyError(f"Experiment not found: {experiment_id}")
    src = Path(inspect.getfile(cls))
    if not src.exists():
        raise ValueError(f"Experiment source file not found: {experiment_id}")
    deleted_name = src.name
    src.unlink()
    invalidate_cache()
    return {"deleted": True, "file": deleted_name}


def duplicate_experiment_file(
    experiment_id: str,
    new_id: str | None = None,
    new_name: str | None = None,
) -> dict[str, Any]:
    """Duplicate an experiment file with a new id."""
    import re

    cls = get_experiment(experiment_id)
    if cls is None:
        raise KeyError(f"Experiment not found: {experiment_id}")
    src = Path(inspect.getfile(cls))

    safe_new_id = new_id or f"{experiment_id}_copy"
    dest_name = f"{safe_new_id}.py"
    dest = _EXPERIMENTS_DIR / dest_name
    content = src.read_text(encoding="utf-8")

    # Update the class id and name in the copy
    content = re.sub(
        r'(\s+id\s*[:=]\s*ClassVar\[str\]\s*=\s*["\'])([^"\']+)(["\'])',
        lambda m: m.group(1) + safe_new_id + m.group(3),
        content,
    )
    content = re.sub(
        r'(\s+id\s*=\s*["\'])([^"\']+)(["\'])',
        lambda m: m.group(1) + safe_new_id + m.group(3),
        content,
    )
    if new_name:
        content = re.sub(
            r'(\s+name\s*[:=]\s*(?:ClassVar\[str\]\s*=\s*)?["\'])([^"\']+)(["\'])',
            lambda m: m.group(1) + new_name + m.group(3),
            content,
        )
    dest.write_text(content, encoding="utf-8")
    invalidate_cache()
    return {"duplicated": True, "new_file": dest_name, "new_id": safe_new_id}


def create_experiment_from_prompt(
    prompt: str,
    name: str,
    category: str = "Analysis",
    openai_api_key: str | None = None,
) -> dict[str, Any]:
    """Use OpenAI to generate a new experiment Python file from a natural language prompt.

    Returns the path of the created file and the generated code.
    """
    import os

    api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set. Provide it in Settings.")

    system_prompt = f"""You are an expert Python developer writing a Glossa Lab experiment.

A Glossa Lab experiment is a Python file containing a class that inherits from ExperimentBase.
The file lives in backend/experiments/ and is auto-discovered.

Write ONLY valid Python code. No markdown fences. No explanations.

Example structure:
from __future__ import annotations
from glossa_lab.experiment_base import ExperimentBase

class {name.replace(" ", "")}(ExperimentBase):
    id = "{name.lower().replace(" ", "_")}"
    name = "{name}"
    category = "{category}"
    description = "..."
    estimated_time = "~1 min"
    results_file = "reports/{name.lower().replace(" ", "_")}.json"
    report_schema = {{"type": "object", "properties": {{}}}}

    def run(self, **kwargs):
        # implementation
        return {{"result": "..."}}

if __name__ == "__main__":
    e = {name.replace(" ", "")}()
    print(e.run())
"""

    user_prompt = f"Create an experiment that: {prompt}\n\nClass name: {name.replace(' ', '')}"

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=2000,
            temperature=0.2,
        )
        code = response.choices[0].message.content or ""
        # Strip markdown fences if present
        code = code.strip()
        if code.startswith("```"):
            lines = code.split("\n")
            code = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

        safe_id = name.lower().replace(" ", "_")
        dest = _EXPERIMENTS_DIR / f"{safe_id}.py"
        dest.write_text(code, encoding="utf-8")
        invalidate_cache()
        return {"created": True, "file": dest.name, "id": safe_id, "code": code}
    except ImportError:
        raise ImportError("openai package not installed. Run: pip install openai")

# Contributing an Experiment to Glossa Lab

Glossa Lab auto-discovers any Python file in this directory that defines a
class inheriting from `ExperimentBase`. Drop a file here and it immediately
appears in the **Experiments** tab and **Study Builder** palette — no
registration step required.

---

## Quick Start (copy-paste template)

```python
from __future__ import annotations
from typing import Any
from glossa_lab.experiment_base import ExperimentBase


class MyExperiment(ExperimentBase):
    # ── Required metadata ──────────────────────────────────────────────
    id            = "my_experiment"          # unique snake_case id
    name          = "My Experiment"          # human-readable name shown in UI
    category      = "Analysis"              # groups experiments in the palette
    description   = (
        "One or two sentences describing what this experiment measures, "
        "what corpus it expects, and what the output contains."
    )
    estimated_time = "~10 sec"             # rough wall-clock estimate

    # ── Optional metadata ──────────────────────────────────────────────
    requires_key  = None                   # e.g. "mistral_api_key" if needed
    command       = ""                     # CLI command for reference only
    results_file  = "reports/my_experiment.json"  # relative path for auto-linking in Reports

    # ── Params schema (JSON Schema for run() kwargs) ───────────────────
    # Drives the Study Builder Inspector: each property becomes a typed form field.
    # Use "type": "string" | "integer" | "number" | "boolean"
    # Supported extra fields: "title", "description", "default", "minimum", "maximum"
    params_schema = {
        "type": "object",
        "properties": {
            "corpus_id": {
                "type": "string",
                "title": "Corpus ID",
                "description": "ID of the corpus to analyse (from the Corpora tab).",
            },
            "min_count": {
                "type": "integer",
                "title": "Min Count",
                "default": 5,
                "minimum": 1,
                "description": "Minimum occurrences to include a symbol.",
            },
        },
    }

    # ── Core logic ─────────────────────────────────────────────────────
    def run(self, **kwargs: Any) -> dict[str, Any]:
        corpus_id: str | None = kwargs.get("corpus_id")
        min_count: int = int(kwargs.get("min_count", 5))

        # ... your analysis logic ...

        result = {
            "corpus_id": corpus_id,
            "min_count": min_count,
            "findings": [],
        }

        # Optionally save to results_file
        if self.results_file:
            import json
            from pathlib import Path
            out = Path(__file__).resolve().parents[3] / self.results_file
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(result, indent=2), encoding="utf-8")

        return result
```

---

## Class Variables Reference

| Variable        | Type                | Required | Description |
|-----------------|---------------------|----------|-------------|
| `id`            | `str`               | **Yes**  | Unique snake_case identifier. Must be stable — changing it loses Study Builder wiring. |
| `name`          | `str`               | **Yes**  | Display name shown in Experiments tab and palette. |
| `category`      | `str`               | **Yes**  | Groups palette items. Common values: `"Analysis"`, `"Validation"`, `"Research"`, `"Data Extraction"`, `"Experiments"`. |
| `description`   | `str`               | **Yes**  | Full description shown in palette tooltip and Experiments tab. Be specific about what corpus is expected and what the output contains. |
| `estimated_time`| `str`               | **Yes**  | Human-readable time estimate. Used to set user expectations. e.g. `"~3 sec"`, `"~2 min"`, `"~2 hours"`. |
| `requires_key`  | `str \| None`       | No       | Setting key that must be non-empty for this experiment to work. Shown as a warning badge in the UI. |
| `command`       | `str`               | No       | CLI command for reference. Shown in the Experiments tab. |
| `results_file`  | `str \| None`       | No       | Relative path (from repo root) where `run()` saves its output. Enables the Reports tab to auto-link results to this experiment. |
| `report_schema` | `dict \| None`      | No       | JSON Schema describing the **output** of `run()`. Used for future report composition features. |
| `params_schema` | `dict \| None`      | No       | JSON Schema describing the **input** `kwargs` of `run()`. Drives the Study Builder Inspector form. **Always define this.** |

---

## `params_schema` in Detail

`params_schema` follows the [JSON Schema](https://json-schema.org/) `object` format.
Each property in `properties` becomes one typed form field in the Study Builder Inspector.

```python
params_schema = {
    "type": "object",
    "properties": {
        # String field
        "corpus_id": {
            "type": "string",
            "title": "Corpus ID",
            "description": "ID of the corpus (from Corpora tab). Leave blank for default.",
        },
        # Integer field with bounds
        "min_count": {
            "type": "integer",
            "title": "Min Count",
            "default": 5,
            "minimum": 1,
            "maximum": 1000,
            "description": "Minimum occurrences to include a symbol.",
        },
        # Float field
        "threshold": {
            "type": "number",
            "title": "Threshold",
            "default": 0.6,
            "description": "Minimum score to include a candidate.",
        },
        # Boolean toggle
        "verbose": {
            "type": "boolean",
            "title": "Verbose Output",
            "default": False,
            "description": "Include detailed per-symbol breakdowns in output.",
        },
    },
}
```

If your experiment has **no user-configurable parameters** (e.g. it uses a fixed
built-in corpus), declare an empty schema so the Inspector shows a clear message:

```python
params_schema = {
    "type": "object",
    "properties": {},
    "$comment": "Uses the built-in corpus automatically. No user params required.",
}
```

---

## `run()` Contract

```python
def run(self, **kwargs: Any) -> dict[str, Any]:
    ...
```

- **Input**: keyword arguments matching `params_schema` properties. Values are
  whatever the user typed in the Study Builder Inspector (strings, ints, bools).
  Always provide defaults via `kwargs.get("key", default)`.
- **Upstream data**: when the study graph has edges, the framework also passes
  `upstream_results: dict[str, Any]` where keys are upstream node IDs and values
  are their `result` dicts. Use this to chain experiments:
  ```python
  upstream = kwargs.get("upstream_results", {})
  for node_id, result in upstream.items():
      profiles = result.get("profiles", [])
  ```
- **Output**: return a plain JSON-serialisable `dict`. The Study Builder shows it
  as a collapsible JSON block. Keep top-level keys descriptive.
- **Errors**: raise any exception; the framework catches it, marks the node as
  `error`, and shows the message in the run results panel.
- **CLI-only experiments**: if your experiment is too long or complex to run
  in-process, set `run()` to raise `NotImplementedError` with a helpful message
  and document the CLI command in `command`. The node will appear as `skipped`.

---

## Corpus Loading Pattern

For experiments that accept an optional `corpus_id`, use this pattern to fall
back to the ICIT corpus if no ID is given:

```python
def _load_corpus(self, corpus_id: str | None) -> list[list[str]]:
    """Load symbol sequences from the database or the default Indus corpus."""
    from glossa_lab.database import get_db
    import asyncio, json
    from pathlib import Path

    db = get_db()
    if db and corpus_id:
        try:
            loop = asyncio.get_event_loop()
            text = loop.run_until_complete(db.get_text(corpus_id))
            if text and text.get("content"):
                raw = text["content"]
                if raw and isinstance(raw[0], list):
                    return raw          # list of sequences
                if raw and isinstance(raw[0], str):
                    return [raw]        # single sequence
        except Exception:
            pass

    # Fallback: ICIT extracted corpus (Indus research)
    icit = Path(__file__).resolve().parents[3] / "reports" / "icit_extracted_corpus.json"
    if icit.exists():
        data = json.loads(icit.read_text("utf-8"))
        return [i["sequence"] for i in data["inscriptions"] if i.get("sequence")]

    return []
```

---

## Testing Your Experiment

1. **In-process test** (fastest):
   ```python
   # From repo root:
   python -c "
   import sys; sys.path.insert(0, 'backend')
   from glossa_lab.experiment_base import invalidate_cache, get_experiment
   invalidate_cache()
   cls = get_experiment('my_experiment')
   print(cls().run(corpus_id='', min_count=3))
   "
   ```

2. **Via the API** (end-to-end):
   ```
   POST /api/v1/experiments/my_experiment/run
   Content-Type: application/json
   {"kwargs": {"corpus_id": "", "min_count": 3}}
   ```

3. **Reload without restart**: click **Reload** in the Experiments tab, or:
   ```
   POST /api/v1/experiments/reload
   ```
   This invalidates the discovery cache so your file is picked up immediately.

4. **Verify params_schema is exposed**:
   ```
   GET /api/v1/node-registry/experiment/my_experiment
   ```
   Should return your `params_schema` dict.

---

## Naming Conventions

| Item            | Convention                      | Example                     |
|-----------------|---------------------------------|-----------------------------|
| File name       | `snake_case.py`                 | `contact_zone_analysis.py`  |
| Class name      | `PascalCase`                    | `ContactZoneAnalysis`       |
| `id`            | `snake_case`                    | `contact_zone`              |
| `results_file`  | `reports/snake_case.json`       | `reports/contact_zone.json` |
| `category`      | Title Case, one of the standard | `"Analysis"`                |

**Standard categories**: `Analysis`, `Validation`, `Research`, `Data Extraction`, `Experiments`

---

## Adding a Study Seed

If your experiment is useful as a starting workflow, add it to
`backend/glossa_lab/study_seeds.py`. Seeds are upserted on every server
restart (using `INSERT OR REPLACE`), so changes take effect immediately.

```python
# In study_seeds.py _SEEDS list:
{
    "name": "My Analysis Workflow",
    "description": "Brief description for the Study Builder sidebar.",
    "graph": {
        "nodes": [
            _node("n1", "my_experiment", "My Experiment", 100, 100),
        ],
        "edges": [],
    },
},
```

**Rule**: every `ref_id` in a seed node MUST match a registered experiment `id`.
Verify with:
```
python -c "from glossa_lab.experiment_base import discover_experiments; print(list(discover_experiments()))"
```

---

## Checklist Before Submitting

- [ ] `id` is unique and snake_case
- [ ] `params_schema` is defined (even if `properties: {}`)
- [ ] `run()` handles missing/empty `corpus_id` gracefully
- [ ] `results_file` is set if your experiment saves output
- [ ] Tested in-process without errors
- [ ] `GET /api/v1/node-registry/experiment/<id>` returns the schema
- [ ] If adding a seed: all `ref_id` values are verified against registered IDs

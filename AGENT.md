# Glossa Lab — Agent Reference

This file documents the correct procedures for working in this codebase.
Read this before adding experiments, studies, or running anything.

---

## 1. Adding a New Experiment

### File location
Every experiment lives in `backend/glossa_lab/experiments/`.
One experiment per file is preferred, but multiple classes in one file are fine
(see `remaining_experiments.py` for the pattern).

### Minimal template

```python
# backend/glossa_lab/experiments/my_experiment.py

try:
    from glossa_lab.experiment_base import ExperimentBase as _EB
except ImportError:
    _EB = object


class MyExperiment(_EB):
    id              = "my_experiment"          # unique snake_case, no spaces
    name            = "My Experiment Name"
    category        = "Validation"             # see valid categories below
    description     = "One-paragraph description shown in the UI."
    estimated_time  = "~2 min"
    command         = "python -m glossa_lab.experiments.my_experiment"
    params_schema   = {                        # at minimum this empty schema
        "type": "object",
        "properties": {
            "top_n": {
                "type": "integer",
                "title": "Top N",
                "default": 30,
                "minimum": 1,
                "description": "How many items to process.",
            },
        },
    }

    def run(self, **kwargs) -> dict:
        top_n = int(kwargs.get("top_n") or 30)
        # ... do the work ...
        return {
            "result": "...",
            "top_n": top_n,
        }


if __name__ == "__main__":
    # ALWAYS use run_cli() here so the UI sees it
    result = MyExperiment().run_cli()
```

### Rules
- `id` must be **unique across all experiment files** — run `python -m glossa_lab.run --list` to check.
- `id` must be **snake_case** only (letters, digits, underscores).
- `run()` must return a **dict**. Never return None or a non-dict.
- Use `verbose=True/False` pattern for print output inside the run function body — don't use `print()` inside the class `run()` method directly; put the verbose logic in a helper function the class calls.
- `params_schema` must be present even if empty: `{"type": "object", "properties": {}}`.
- The `try/except ImportError` guard on `_EB` is required so the file can be imported standalone.

### Valid categories
| Category | Use for |
|---|---|
| `Validation` | Benchmarks, tier tests, anti-circularity, oracle analysis |
| `Analysis` | Script analysis pipelines (clustering, entropy, etc.) |
| `Research` | Research workflows combining multiple analyses |
| `Experiments` | Experimental/exploratory pipelines |
| `Data Extraction` | OCR, corpus building, data conversion |

### Verify it appears
```powershell
python -m glossa_lab.run --list          # must appear in the list
python -m glossa_lab.run my_experiment   # must run and save a report
```

---

## 2. Running Experiments (CLI → UI visibility)

**Always use the CLI runner** when running experiments outside the UI:

```powershell
# Run any experiment by ID — registers a job in the UI, saves a report
python -m glossa_lab.run beam_decipher_benchmark
python -m glossa_lab.run tier5_indus_decipherment
python -m glossa_lab.run ventris_validation --param top_n=50

# List all registered experiments
python -m glossa_lab.run --list
```

When the backend is running you will see:
- **Jobs panel**: a live job entry `"<Name> [CLI]"` — auto-removed on completion
- **Reports catalog**: a timestamped JSON file `<id>_<timestamp>.json`
- **Logs panel**: structured entries from `glossa_lab.cli`

When the backend is NOT running: the experiment runs normally and the report
is saved to `reports/` and will appear next time the UI starts.

**Never** run `python -m glossa_lab.experiments.foo` directly for experiments
that should be visible in the UI — that bypasses the bridge. Use `run.py`.

### Programmatic usage
```python
from glossa_lab.experiment_base import get_experiment

cls    = get_experiment("beam_decipher_benchmark")
result = cls().run_cli()          # registers job + saves report
result = cls().run(top_n=30)      # plain run, no UI hooks (API uses this)
```

### Custom scripts
```python
from glossa_lab.cli_bridge import CliReporter, run_with_reporting

with CliReporter("my_experiment", "My Experiment") as rep:
    result = do_the_work()
    rep.save_result(result)
    rep.progress("Halfway done", step=1)
```

---

## 3. Adding a New Study Seed

Study seeds appear in the **Studies** panel of the UI.

### File
`backend/glossa_lab/study_seeds.py` — add to the `_SEEDS` list.

### Template
```python
{
    "name": "My New Study",        # shown in the Studies panel
    "description": (
        "What this study does and why. "
        "Multi-line is fine."
    ),
    "graph": {
        "nodes": [
            _node("n1", "experiment_id_1", "Node Label 1",   x=100, y=100),
            _node("n2", "experiment_id_2", "Node Label 2",   x=450, y=100),
            _node("n3", "experiment_id_3", "Node Label 3",   x=800, y=100),
            _report("r1", "Report Label",                    x=1150, y=100,
                    filename="my_report.json"),
        ],
        "edges": [
            _edge("e1", "n1", "n2"),
            _edge("e2", "n2", "n3"),
            _edge("e3", "n3", "r1"),
        ],
    },
},
```

### Rules
- All `ref_id` values in `_node()` calls **must be valid, registered experiment IDs**.
  Verify: `python -m glossa_lab.run --list`.
- Node positions: start at x=100, increment x by ~350 per column.
  Parallel branches can share the same x and stagger y by ~160.
- `_report()` nodes are the output sink — connect all terminal nodes to them.
- Seeds are **upserted on server restart** (idempotent).
  **Graph JSON is never overwritten** after the first insert — to reset a
  study graph, delete it in the UI and restart the server.
- Study `id` is derived from the name via `_slug()` (lowercased, non-alphanumeric → `_`, max 20 chars).

### Verify
```python
# Check the slug that will be used as the database ID
import re
name = "My New Study"
print(re.sub(r"[^a-z0-9]+", "_", name.lower())[:20].strip("_"))
```

---

## 4. Saving Reports from Experiments

Reports appear in the **Reports** catalog in the UI.
They are discovered from `reports/*.json` automatically.

### Automatic (preferred)
Running via `python -m glossa_lab.run` or `.run_cli()` saves automatically.

### Manual save
```python
from glossa_lab.cli_bridge import save_report
save_report("my_experiment_id", result_dict)
# saves to reports/my_experiment_id_20260410T123456.json
```

### Fixed filename (for experiments with `results_file` set)
Some experiments set `results_file = "reports/my_experiment.json"` and save
manually inside `run()`. This is fine for results that should overwrite
the previous run rather than accumulate timestamped copies.

---

## 5. Beam Decipherment Patterns

### Adding phonological groups for a new cipher→language pair
Define a `dict[str, frozenset]` mapping opaque cipher sign IDs to frozensets
of allowed target phonemes. See `UGARITIC_PHONO_GROUPS_TIGHT` in
`backend/glossa_lab/pipelines/beam_decipher.py` as the reference.

```python
MY_PHONO_GROUPS = {
    "S001": frozenset(["a", "i", "u"]),   # vowels
    "S002": frozenset(["n", "m", "r"]),   # sonorants
    ...
}
result = beam_decipher(cipher_flat, lm, phono_groups=MY_PHONO_GROUPS, ...)
```

### Performance
The `BigramScorer` numpy fast path activates automatically when:
- `use_word_bigrams=False`
- `ocp_weight=0.0`
- `root_prior_weight=0.0`
- `positional_weight <= 0.005`

This gives ~10x speedup on large corpora (Sumerian-scale).
For GPU acceleration, install `cupy-cuda12x` — `beam_decipher.py` will
use it automatically via `_xp()` in `decipher.py`.

---

## 6. Adding New Language Corpora

Corpus modules live in `backend/glossa_lab/data/`.
Each must expose at minimum:

```python
def get_corpus_symbols() -> list[str]:   # flat token list
    ...

def get_corpus_inscriptions() -> list[list[str]]:   # inscription-level
    ...
```

Optionally for word-level phonotactics:

```python
def get_word_inscriptions() -> list[list[str]]:
    # Each inner list is one word (not one inscription)
    ...
```

Word boundaries are marked with `.` in corpus string lines (same convention
as Ugaritic). The `get_word_inscriptions()` function parses dots.

---

## 7. Key File Locations

| What | Where |
|---|---|
| Experiment classes | `backend/glossa_lab/experiments/*.py` |
| Study seeds | `backend/glossa_lab/study_seeds.py` |
| CLI runner | `backend/glossa_lab/run.py` |
| CLI bridge (job/report/log) | `backend/glossa_lab/cli_bridge.py` |
| Beam search engine | `backend/glossa_lab/pipelines/beam_decipher.py` |
| SA decipherment + BigramScorer | `backend/glossa_lab/pipelines/decipher.py` |
| Language model base class | `backend/glossa_lab/pipelines/decipher.py::LanguageModel` |
| Hebrew corpus | `backend/glossa_lab/data/old_hebrew.py` |
| Indus corpus | `backend/glossa_lab/data/indus_public_corpus.py` |
| Sumerian corpus | `backend/glossa_lab/data/sumerian_ur3.py` |
| Dravidian corpus | `backend/glossa_lab/data/dravidian.py` |
| Sanskrit corpus | `backend/glossa_lab/data/sanskrit.py` |
| Linear B fixture | `backend/tests/corpora/fixtures/linear_b.txt` |
| Reports directory | `reports/` (root of repo) |
| Dr. Fuls report script | `backend/generate_fuls_report_v3.py` |

---

## 8. Checklist: Adding an Experiment

- [ ] Create file in `backend/glossa_lab/experiments/`
- [ ] Class inherits from `ExperimentBase` (with try/except guard)
- [ ] Set `id` (unique snake_case), `name`, `category`, `description`, `estimated_time`
- [ ] Set `params_schema` (even if empty: `{"type": "object", "properties": {}}`)
- [ ] `run()` returns a `dict`
- [ ] `if __name__ == "__main__":` calls `MyClass().run_cli()`
- [ ] Run `python -m glossa_lab.run --list` → confirm it appears
- [ ] Run `python -m glossa_lab.run <id>` → confirm it runs and saves a report
- [ ] If adding to a study seed, add to `_SEEDS` in `study_seeds.py`
- [ ] Commit everything together

## 9. Checklist: Adding a Study Seed

- [ ] Verify all experiment IDs exist via `python -m glossa_lab.run --list`
- [ ] Add to `_SEEDS` in `backend/glossa_lab/study_seeds.py`
- [ ] Use `_node()`, `_edge()`, `_report()` helpers
- [ ] Position nodes logically (x increments ~350 per column, y ~160 per row)
- [ ] Study will appear after server restart (seeds are upserted idempotently)
- [ ] Commit

---

## 10. Common Mistakes to Avoid

| Mistake | Correct approach |
|---|---|
| Running `python -m glossa_lab.experiments.foo` directly | Use `python -m glossa_lab.run foo` |
| Forgetting `try/except ImportError` guard on `_EB` | Always include it — lets files be imported standalone |
| `id` with spaces or hyphens | Use only `snake_case` |
| `run()` returning `None` | Always return a `dict` |
| Adding node to study with invalid `exp_id` | Run `--list` first to verify |
| Adding CV pairs to Linear B corpus | They flatten the Ventris F1 — use authentic tablet vocabulary only |
| Using `name` as a logging `extra` key | Reserved by Python logging — use `exp_name` instead |
| Saving reports manually with `.write_text()` | Use `cli_bridge.save_report()` so metadata is consistent |
| Modifying `_HEBREW_LINES` without filtering `.` in corpus functions | `get_corpus_inscriptions()` must filter `"."` tokens |

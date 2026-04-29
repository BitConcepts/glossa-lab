# Glossa-Lab — Project Rules for Agents (WARP.md)

This file is the canonical Warp / Oz project-rule file for `glossa-lab`. Any
agent working in this repository MUST treat the rules below as binding. They
take precedence over personal rules and over earlier instructions; project
rules in subdirectories may override these only if explicitly more specific.

See `AGENTS.md` for the LEDGER + session-lifecycle rules. The two files are
complementary: AGENTS.md governs *how* you record work; WARP.md governs *how*
you build and run the experiments.

---

## Rule G1 (CRITICAL): All experiments MUST run through the Glossa-Lab graph executor

Any "Phase-N" research run, any reusable analysis pipeline, and any new
research workflow MUST be expressed as one of:

1. **Graph experiment** — JSON DAG of atomic nodes under
   `backend/glossa_lab/experiments/graphs/<id>.json`, composed from atomic
   nodes in `backend/glossa_lab/experiment_graph*.py` and registered via the
   `_phase{N}_node_defs()` factory pattern.
2. **`ExperimentBase` subclass** — Python class under
   `backend/glossa_lab/experiments/<name>.py` with `id`, `name`,
   `params_schema`, and `run_cli()` per `docs/guides/building-experiments.md`
   (rules H12.1 – H12.5).

### Forbidden

- **Standalone scripts under `scripts/phase{N}/` that bypass `ExperimentBase`
  and the graph executor.** Phases 16–19 violated this rule and are the
  canonical anti-pattern. Future phases must not.
- Running analyses via `python scripts/phaseN/foo.py` where `foo.py` does
  the work directly. Any such file MUST instead be either:
  * a thin one-line CLI shim that calls the relevant atomic node's `fn(...)`
    inside a `cls().run_cli()` flow, or
  * a true graph experiment invoked via
    `shell.cmd python -m glossa_lab.experiments <graph_id>`.

### Required pattern when adding a new phase

1. Add Phase-N atomic nodes to `backend/glossa_lab/experiment_graph_phase{N}.py`
   following the Phase-14 / Phase-15 / Phase-20 template (`AtomicNodeDef` + a
   `_phase{N}_node_defs()` factory).
2. Wire them into `ATOMIC_NODES` from `experiment_graph.py` with a try/except
   import block matching the existing Phase-14/15/20 blocks (~line 2316).
3. Compose one or more graph JSON files in
   `backend/glossa_lab/experiments/graphs/`. Use the `auto_migrated: false`
   marker so `auto_migrate_hardcoded_experiments()` will NOT overwrite them.
4. Run each via `shell.cmd python -m glossa_lab.experiments <graph_id>`.
   This guarantees:
   * a SQLite Job entry in the Jobs panel,
   * a JSON report under `reports/<graph_id_or_export_filename>.json`,
   * a timestamped run-trace file under `reports/<graph_id>_<TS>.json`.
5. Write a Markdown synthesis to `reports/phase{N}_synthesis.md` summarising
   the headline findings + Phase-(N+1) candidate experiments.

### Acceptable exceptions

- One-off **data-extraction / OCR / scraping** scripts that produce a fixed
  artifact under `corpora/downloads/` or `backend/glossa_lab/data/phase*_corpora/`
  may live as plain scripts under `scripts/phase{N}/`. They are pre-experiment
  data plumbing, not experiments. Document them in the phase-N synthesis as
  data-acquisition steps and treat their outputs as inputs to graph
  experiments.
- Quick agent-side smoke tests of an atomic node may be run inline via
  `shell.cmd python -c "..."` without registering a Job entry, but only for
  validation. Real research runs must use the graph executor.

### Why this rule exists

The Glossa-Lab graph executor provides:
- a uniform Job ledger (SQLite `jobs` table) feeding the UI's Jobs panel,
- automatic SSE streaming for long-running runs,
- per-node error isolation and per-node timing,
- composability — every atomic node can be re-used in a Study or in another
  graph experiment without copy-paste,
- replayability — every graph JSON is a complete, version-controlled
  specification of an experiment,
- discoverability — graphs auto-register via
  `register_graph_experiments()` and appear in the UI palette.

Standalone Python scripts under `scripts/phase{N}/` defeat all six. Use the
executor.

---

## Rule G2: H12 ExperimentBase rules (from `docs/guides/building-experiments.md`)

When implementing an `ExperimentBase` subclass:

- **H12.1** — every experiment file MUST define at least one
  `ExperimentBase` subclass; standalone scripts that bypass it are forbidden.
- **H12.2** — define `params_schema` (JSON Schema) for all configurable
  parameters so the UI can render form controls.
- **H12.3** — the `if __name__ == "__main__":` block MUST call
  `cls().run_cli()`, never `cls().run()` directly. `run_cli()` registers the
  job in the Jobs panel.
- **H12.4** — SA seed loops MUST use `run_seeds_parallel()` from
  `glossa_lab.experiments._parallel`. Plain `for seed in range(N):` loops are
  forbidden.
- **H12.5** — do NOT set `ocp_weight > 0` or `use_word_bigrams=True` unless
  scientifically necessary. Document deliberate bypasses with a comment.

---

## Rule G3: Reports and synthesis files

- All experiment outputs MUST land under `reports/`.
- Use a stable, descriptive filename for the JSONExport node — e.g.
  `phase20a_length_strata.json` — so it can be diffed across runs.
- Each phase MUST produce a `reports/phase{N}_synthesis.md` that:
  * states verdict per prior-phase prediction,
  * embeds key numerical results in tables,
  * lists Phase-(N+1) candidate experiments.

---

## Rule G4: Commits and pushes

- Commit messages for phase work follow the pattern
  `PHASE-{N}: <one-line subject>` followed by a multi-paragraph body that
  enumerates deliverables and headline findings (see commits `bf9212a`,
  `3fdcef1`, `cd5c736`, etc.).
- Every commit MUST include the co-author footer
  `Co-Authored-By: Oz <oz-agent@warp.dev>`.
- **Never** commit unless the user explicitly asks. Phase deliverables are
  the one acceptable triggering instruction.

---

## Self-check before declaring a phase complete

1. Is every analysis expressed as either a graph experiment or an
   `ExperimentBase` subclass? (Rule G1)
2. Did each run go through `shell.cmd python -m glossa_lab.experiments
   <id>` and produce a Job entry + a `reports/...` file? (Rule G1)
3. Is there a `reports/phase{N}_synthesis.md` with verdict + Phase-(N+1)
   plan? (Rule G3)
4. Is the commit + push clean, with the co-author footer? (Rule G4)

If any of these are NO, the phase is not done.

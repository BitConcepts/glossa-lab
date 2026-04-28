# AGENTS.md

## Purpose

This repository uses a closed-loop, specification-first, constraint-governed agentic workflow.

Agents are **proposal generators**, not authorities.

All non-trivial work MUST flow through:

1. explicit state loading
2. proposal emission
3. constraint checking
4. bounded execution
5. verification
6. LEDGER update

---

## Core principle

> Intelligence proposes. Constraints decide. The ledger remembers.

- Prompts are not authority  
- Plans are not authority  
- Code is not authority  
- The **LEDGER.md + accepted repo state is authority**

---

## REQUIRED: LEDGER.md

A file named `LEDGER.md` MUST exist at repo root.

### Rules

- Every meaningful task MUST be recorded
- Every session MUST append an entry
- All TODOs MUST live in the ledger
- No work is considered complete without a ledger entry

### Entry format

```md
## [YYYY-MM-DD] Entry — <short title>

Objective:
What was done:
Files changed:
Checks run:
Results:
Open TODOs:
Risks:
Next step:
```

---

## SESSION LIFECYCLE

Agents MUST follow structured session flows.

### Session boundary rules

- A new conversation is a new session, NOT a new project.
- All governance rules in AGENTS.md persist across sessions and conversations.
- Agents MUST NOT reset or ignore project rules across conversation boundaries.
- Past chat messages from previous conversations are not available; agents MUST rely on on-disk documents (ledger, requirements, tests, architecture) as the source of truth for continuity.
- LEDGER.md is the ONLY authoritative source for session continuity. Do NOT create `NEXT_SESSION.md`, `STATUS.md`, `SESSION_SUMMARY.md`, or similar files — all continuity lives in the ledger.

### Conversation summarization recovery

Whenever the conversation is optimized, summarized, or truncated by the platform (e.g. a "CONVERSATION SUMMARY" block is inserted), agents MUST **immediately re-read AGENTS.md in full** before performing ANY further actions. Summarization loses nuance from project rules; the only way to restore it is to re-read the authoritative source. **No exceptions.**

---

## 🔵 NEW SESSION PROMPT

When starting fresh:

```text
Load AGENTS.md, README.md, docs/architecture.md, docs/workflow.md, docs/services.md, and LEDGER.md.

Output:
1. Current system understanding
2. Current known state from ledger
3. Open TODOs
4. Suggested next task

Then produce a Proposal.
```

---

## 🟡 RESUME SESSION PROMPT

```text
Load AGENTS.md and LEDGER.md.

Summarize:
- last completed task
- current objective
- open TODOs
- risks

Then propose next bounded task.
```

---

## 🟢 SAVE SESSION PROMPT

```text
Prepare LEDGER.md entry for this session.

Include:
- what changed
- what was verified
- what remains incomplete
- next recommended step

Do not invent results.
```

---

## 🔴 GIT COMMIT PROMPT

```text
Prepare commit summary:

- what changed
- why
- files touched
- checks performed

Generate commit message.

Then list commands to run:
git add .
git commit -m "<message>"
git push
```

---

## 🔵 GIT UPDATE PROMPT

```text
Update local repo safely:

1. git status
2. git pull
3. summarize changes
4. identify conflicts or risks
```

---

## QUICK COMMANDS

Agents should use these short commands:

| Command  | Meaning             |
| -------- | ------------------- |
| `start`  | new session         |
| `resume` | resume from ledger  |
| `save`   | write ledger entry  |
| `commit` | prepare git commit  |
| `sync`   | pull latest changes |

---

## DOCUMENT AUTHORITY HIERARCHY

When documents conflict, precedence is resolved top-down:

1. **AGENTS.md** — behavioral rules, hard constraints, stop conditions (highest)
2. **README.md** — project intent and scope
3. **docs/REQUIREMENTS.md** — what the system must do
4. **docs/architecture.md** — how the system is structured
5. **docs/TEST_SPEC.md** — how the system is verified
6. **LEDGER.md** — what has been done and what remains (sole authority for session state)
7. **docs/workflow.md** — how work proceeds
8. **docs/services.md** — platform-specific startup/service behavior

If a requirement contradicts the architecture, the requirement wins.
If AGENTS.md contradicts a requirement, AGENTS.md wins.

---

## AGENT ROLE DEFINITION

### Agents ARE:

* proposal generators
* assistants and drafting aides
* consistency checkers (requirements ↔ tests ↔ architecture)
* reviewers and summarizers
* context loaders and state reconstructors

### Agents are NOT:

* decision-makers
* autonomous actors without human intent
* sources of project truth
* authorities on completion or correctness

Agents SHALL never invent, infer, or assume undocumented project state.

---

## DRAFTING ASSISTANCE

Agents MAY assist with drafting content when explicitly requested, including:

* drafting code scaffolds
* drafting requirements
* drafting test descriptions
* drafting architecture refinements
* drafting documentation

All drafting assistance MUST:

* be clearly labeled as a draft or proposal
* reference existing requirements and architecture where applicable
* avoid claiming implementation, correctness, or completion

Agents MUST NOT:

* claim that drafted material is "done"
* bypass review, testing, or ledger updates

Agents SHOULD implement changes directly (creating/editing files) rather than asking the user to make manual edits, unless automatic edits fail.

All acceptance of drafts or edits to authoritative documents is a **human decision**.

---

## CONFLICT AND CONSISTENCY HANDLING

If an agent detects:

* a requirement without a test
* a test without a requirement
* architecture that violates requirements
* ledger inconsistencies
* documentation that contradicts implementation

The agent SHALL:

1. Report the issue explicitly
2. Reference exact document locations (file, line, requirement ID)
3. NOT propose fixes unless explicitly requested
4. Record the inconsistency in the current session's ledger entry under "Risks"

---

## CONTEXT WINDOW MANAGEMENT

Large governance files consume agent context rapidly. Agents MUST actively manage context window consumption.

### On session load:

* Read AGENTS.md in full (rules are authoritative, no shortcuts)
* Read only the **last ~300 lines** of LEDGER.md (recent entries + next-session block)
* Read only the **first ~200 lines** of docs/REQUIREMENTS.md and docs/TEST_SPEC.md (TOC + active items)
* Read docs/architecture.md by section header only (~first 40 lines) unless a specific section is task-relevant
* Older ledger entries and deep doc sections are loaded only when explicitly needed

### During a session:

* NEVER re-read a file already in context unless it has been modified since the last read
* Use line ranges for all reads of files longer than ~200 lines
* Prefer grep or semantic search over reading entire files when looking for specific content
* Batch file reads into a single call rather than sequential calls
* Keep responses concise — summarize rather than echoing large file contents
* Do not repeat plan or proposal contents after creating them
* After multi-step tasks, give a brief summary (2–4 sentences) rather than recapping every file

### File size guidelines (approximate):

* AGENTS.md: ~200–500 lines — read in full
* LEDGER.md: grows unbounded — read last ~300 lines
* docs/REQUIREMENTS.md: ~100–400 lines — read first ~200
* docs/TEST_SPEC.md: ~100–600 lines — read first ~200
* docs/architecture.md: ~100–400 lines — read first ~40, expand by section

Treat context window exhaustion as a **preventable defect**.

---

## ENVIRONMENT REQUIREMENTS

The project MUST be environment-controlled and system-agnostic.

---

## Python environment (required)

* use virtual environment
* do not rely on global Python
* environment must be reproducible

### Expected structure

```text
backend/
  venv/
```

or

```text
.venv/
```

---

## ENV BOOTSTRAP

Environment setup must be split:

### 1. Python-level

* dependency install
* environment config
* runtime setup

### 2. OS-level

Scripts must exist for:

* Windows (`.cmd`)
* Linux/macOS (`.sh`)

---

## SHELL WRAPPER (CRITICAL)

All tool invocations MUST go through the unified shell wrapper:

```text
# Windows
shell.cmd <command> [args]

# Linux/macOS
./shell.sh <command> [args]
```

### Available commands

* `shell.cmd test [args]` — run pytest
* `shell.cmd lint [args]` — run ruff check
* `shell.cmd format [args]` — run ruff format
* `shell.cmd setup` — re-run setup (install/update deps)
* `shell.cmd python [args]` — run Python in venv
* `shell.cmd run` — start backend in foreground (dev/debug only — BLOCKS terminal)
* `shell.cmd tray` — start tray in foreground (dev/debug only — BLOCKS terminal)

### Service startup — THE ONLY CORRECT WAY

To start the backend and tray as background processes use `setup-os.cmd`, never `shell.cmd run` or `shell.cmd tray`:

```text
# First-time install (registers HKCU Run autostart, installs deps, builds frontend)
setup-os.cmd install

# Start both backend and tray now (fire-and-forget, returns immediately)
setup-os.cmd start

# Stop
setup-os.cmd stop

# Restart
setup-os.cmd restart

# Check health + autostart registration
setup-os.cmd status
```

**NEVER** call `shell.cmd run` or `shell.cmd tray` as a service. They block the terminal and will hang the agent session.

**NEVER** open any program that must stay open by running it inline in a wait-mode tool call. Use `setup-os.cmd start` which is fire-and-forget.

### Why this exists

On Windows, calling venv `Scripts/*.exe` files directly (e.g. `ruff.exe`, `pytest.exe`) **hangs the PTY**. PowerShell `.ps1` wrappers also hang. The `.cmd` shell wrapper routes all invocations through `python.exe -m <module>` which does not hang.

### ABSOLUTELY FORBIDDEN

* ❌ `backend\venv\Scripts\ruff.exe ...`
* ❌ `backend\venv\Scripts\pytest.exe ...`
* ❌ `backend\venv\Scripts\uvicorn.exe ...`
* ❌ Any direct invocation of executables under `venv/Scripts/` or `venv/bin/`
* ❌ Any `.ps1` PowerShell script for tool invocation (causes PTY hangs)
* ❌ `shell.cmd run` or `shell.cmd tray` as a background/service invocation
* ❌ Running any long-lived program inline in a wait-mode command (it will block or hang)

### REQUIRED (safe, uses python -m)

* ✅ `shell.cmd test`
* ✅ `shell.cmd lint`
* ✅ `shell.cmd python <script>`
* ✅ `setup-os.cmd start` — start backend + tray as detached background processes
* ✅ `setup-os.cmd stop` / `restart` / `status`

### Auto-bootstrap

If the venv does not exist, `shell.cmd` / `shell.sh` will create it and install all dependencies automatically on first run.

---

## ADDITIONAL SCRIPTS

```text
scripts/
  setup.cmd
  setup.sh
  run.cmd
  run.sh
```

These are convenience wrappers. The canonical entry point is `shell.cmd` / `shell.sh` at the repo root.

---

## HARD RULES

### H1 — Ledger required

No ledger entry = work not done.

### H2 — Proposal required

No proposal = no execution.

### H3 — Cross-platform awareness

All work must consider:

* Windows
* Linux
* macOS

### H4 — Environment isolation

No system-dependent assumptions.

### H5 — Explicit startup

No hidden service logic.

### H6 — No silent scope expansion

If the task grows beyond the proposal, stop and re-propose.

### H7 — Shell wrapper required

All tool invocations (pytest, ruff, uvicorn, python) MUST go through `shell.cmd` (Windows) or `shell.sh` (POSIX). Direct invocation of venv executables is **forbidden**. PowerShell `.ps1` scripts are also **forbidden** for tool invocation — they cause PTY hangs on Windows.

To start the backend and tray as background services, use `setup-os.cmd start` (fire-and-forget). NEVER run `shell.cmd run` or `shell.cmd tray` as background processes — they are foreground-only and will block or hang the session.

### H8 — No silent commands

If a command produces no output, it has failed. Do not retry it. Do not wait for it. Treat it as broken and fix the invocation or replace the command. Commands that are known to hang or produce no output are **forbidden**.

### H17 — Job and test execution monitoring (MANDATORY)

> Running a script is not the same as the work succeeding. Always verify status.

When executing ANY long-running Python script, experiment, test suite, or background task, the agent MUST monitor the actual job/test status — never assume success from absence of stderr or from a single "OK" print.

#### H17.1 — Verify exit code AND job status

For every experiment, benchmark, or analysis script run:
1. Capture the process exit code. Non-zero = FAIL.
2. If the script registers a Job via `cli_bridge.run_with_reporting()` or `ExperimentBase.run_cli()`, the agent MUST query the backend Jobs API after the run and confirm `status == "completed"`. A job with status `failed`, `timed_out`, `cancelled`, or `pending` is NOT a success.
3. If a script writes a JSON/PDF output file, verify the file exists, has non-trivial size, and parses as valid JSON/PDF. A truncated or empty file = FAIL.
4. Use `backend/scripts/inspect_jobs.py` (or equivalent `/api/v1/jobs` query) after every batch of CLI experiment runs to confirm no jobs failed.

#### H17.2 — pytest exit code is authoritative

When running `shell.cmd test`:
* exit code 0 = all tests passed
* exit code 1 = at least one test failed (must be triaged) 
* exit code 5 = no tests collected (must be triaged — usually a typo in `-k` filter)
* Any non-zero exit code with a traceback during teardown (e.g. WinError 448 in pytest cleanup_dead_symlinks) is a Windows-specific pytest artefact, NOT a test failure — but it MUST still be reported and the actual `passed/failed` line from the summary block must be located before declaring the run successful.
* NEVER declare "all tests pass" based on the count of dots in the progress bar alone. Always locate the explicit `=== N passed, M failed ===` summary.

#### H17.3 — Long-running scripts must stream progress

If an experiment is expected to run > 30s, the runner script MUST emit periodic progress markers (every N seeds, every phase, etc.). Silent multi-minute runs are forbidden under H8.

#### H17.4 — When a job fails

1. Fetch its full record via `/api/v1/jobs/<id>` (look for `error`, `logs`, `params`).
2. Inspect `logs/backend.log` and any `job_<id>.log` for the actual exception/traceback.
3. Report the failure mode in the agent response BEFORE proceeding to the next step.
4. NEVER silently continue past a failed job — record it under "Risks" or "Open TODOs" in the LEDGER entry.

#### H17.5 — Reporting standard

After running any experiment batch the agent MUST report, in plain text:
* number of jobs/tests submitted
* number completed
* number failed (with IDs)
* any timed-out or stalled jobs (>10 minutes without heartbeat)
* path to the generated output files
* whether each output passes file-validity checks (size > 0, parses as expected format)

Failing to report this constitutes a violation of H1 (ledger required) and H8 (no silent commands).

#### H17.6 — Mandatory polling pattern for ALL experiment runs (NON-NEGOTIABLE)

> Sitting on a long-running shell command with no output is forbidden. Every
> experiment must be observable in real time via `/api/v1/jobs`.

Any CLI invocation expected to run more than ~10 seconds MUST follow this pattern:

1. **Spawn the experiment as a detached subprocess.**
   The launcher returns a `job_id` immediately. The experiment registers itself
   in `/api/v1/jobs` via `CliReporter` (or graph SSE, or pipeline engine).

2. **Poll `/api/v1/jobs` from the foreground every 5–10 seconds.**
   The poller MUST print a status line on every transition
   (`pending` → `running` → `completed`/`failed`/`timed_out`) and a heartbeat
   line every poll interval. Silent multi-minute waits are a violation of H8.

3. **Exit conditions for the poller:**
   * All tracked jobs reach a terminal state (`completed`/`failed`/`timed_out`/`cancelled`).
   * Any tracked job transitions to a non-`completed` terminal state — print full
     job record (id, name, error, params) and EXIT NON-ZERO immediately.
   * Optional max-wait timeout in seconds; on timeout, mark job as suspect and
     surface its current status.

The canonical implementation lives at:
* `backend/scripts/run_and_watch.py` — takes one or more experiment IDs,
  spawns each detached, polls jobs API, prints transitions, returns non-zero
  on first failure. THIS IS THE ONLY APPROVED WAY for the agent to launch
  CLI experiments.
* `backend/scripts/inspect_jobs.py` — ad-hoc snapshot of recent jobs.

**Forbidden patterns:**
* ❌ `shell.cmd python <experiment_runner.py>` for any run > 10s without
  using `run_and_watch.py`.
* ❌ Sitting in `wait` mode on a foreground experiment subprocess for more
  than 60 seconds without polling job status in between.
* ❌ Assuming a script is healthy because it produced no stderr.
* ❌ Reading `reports/*.json` to infer success without first verifying the
  Job's terminal status was `completed`.

**Required pattern for the agent:**
```
shell.cmd python backend/scripts/run_and_watch.py \
    fuls_writing_system_comparison \
    fuls_nw_semitic_ngram \
    --poll-interval 5 \
    --max-wait 1800
```
The agent reads the streaming output and reacts to transitions in real time.

#### H17.7 — Experiment authorship rules

Every NEW experiment added under `backend/glossa_lab/experiments/` MUST:
1. Inherit from `ExperimentBase` and define `id`, `name`, `category`,
   `description`, `estimated_time` (already required by H12).
2. Use `run_cli()` as its terminal entry point (already required by H12.3) so
   that `CliReporter` registers the job and PATCHes its terminal status.
3. Emit a heartbeat — either by calling `rep.progress(...)` from inside
   `run()` at least every 60 seconds, OR by being decomposable into multiple
   shorter primitives so the watchdog never trips on long silent stretches.
4. Be runnable via `run_and_watch.py` without any wrapper script of its own.

Legacy experiments under `_legacy/` may bypass these rules ONLY for backward
compatibility; new code MUST conform.

---

## PLATFORM EXPECTATIONS

### Backend

* Python
* cross-platform
* service-compatible

### Frontend

* React
* API-driven

### Tray

* control surface only

### Services

* Windows + Linux + macOS support required

---

## VERIFICATION MINIMUM

Must record:

* what changed
* what was tested
* what passed/failed
* what is unknown

---

## DECIPHERMENT RESEARCH ASSET REGISTRY

Key assets currently implemented. Reference when planning new experiments or corpora.

### Experiment modules (`backend/glossa_lab/experiments/`)

| ID | Name | Tier | Notes |
|---|---|---|---|
| `beam_decipher_benchmark` | Beam Decipherment Benchmark | 1a | SA vs beam; 4 sweeps; 30/30 with phono groups |
| `semitic_constraints_benchmark` | Semitic Constraints Benchmark | 1a | 4 constraint levels; oracle delta analysis |
| `ugaritic_proper_benchmark` | Ugaritic Proper Benchmark | 1a/1b | Cross-language vs self; anti-circularity |
| `phoenician_benchmark` | Phoenician Benchmark | 1c | Ugaritic→Phoenician; V→E differs from Hebrew |
| `proto_sinaitic_benchmark` | Proto-Sinaitic Benchmark | 1e | Floor test; 576 tokens; 19/22 with anchors |
| `meroitic_benchmark` | Meroitic Benchmark | 1f | Graceful degradation; oracle Δ = -3972 |
| `prior_ablation_benchmark` | Prior Ablation Study | 1a | 7 levels; all oracle deltas NEGATIVE |
| `transparency_benchmark` | Transparency Benchmark | 1a | 4-tier attribution; 90% from anchors |
| `sequence_eval_benchmark` | Sequence-Level Eval | 1a | N-gram recall; noise robustness |
| `ventris_validation` | Ventris Grid Validation | 4 | Linear B; F1=0.148 |
| `tier5_indus_decipherment` | Tier 5 Indus Decipherment | 5 | Dravidian hypothesis; Z-scores |

### Corpus data modules (`backend/glossa_lab/data/`)

| Module | Language | Tokens | Notes |
|---|---|---|---|
| `old_hebrew.py` | Old Hebrew | large | Target LM for Tier 1a/1b |
| `phoenician.py` | Phoenician | ~5000 | KAI inscriptions; Tier 1c target |
| `proto_sinaitic.py` | Proto-Sinaitic | 576 | Serabit el-Khadim + Wadi el-Hol |
| `meroitic.py` | Meroitic + Coptic | 551+537 | Tier 1f; includes Coptic LM |
| `dravidian.py` | Tamil/Dravidian | large | Tier 5 comparison LM |
| `linear_b_language.py` | Mycenaean Greek | — | Sign inventory for Tier 4 |
| `indus_public_corpus.py` | Indus Script | 14,213 | Primary research target |
| `geez/geez.py` | Geez/Ethiopic | ~80K syllabic | Fully deciphered; anchor-convergence benchmark; provided by Dr. Fuls |

### Shared experiment utilities (`backend/glossa_lab/experiments/`)

| Module | Purpose |
|---|---|
| `_parallel.py` | `run_seeds_parallel()` — ThreadPoolExecutor for SA seeds; `compute_device_label()` for GPU/CPU detection. ALL seed loops MUST use this. |

### AI capabilities (`backend/glossa_lab/api/ai_tools.py`)

**Endpoints:**
- `POST /ai/chat` — freeform chat with research context injection
- `POST /ai/chat/stream` — SSE streaming version
- `POST /ai/decipher` — theory-based sign reading (json_mode)
- `POST /ai/draft-section` — academic paper paragraph from experiment result
- `POST /ai/hypotheses/generate` — generate testable hypotheses
- `POST /ai/experiment-chain` — plan experiment sequence
- `POST /ai/synthesize` — cross-study synthesis
- `POST /ai/sign-reading` — probabilistic sign readings
- `POST /ai/report-synthesis` — comprehensive research report
- `POST /ai/execute-action` — execute AI-proposed action

**Action types supported by execute-action:**
`run_experiment`, `run_pipeline`, `create_hypothesis`, `create_notebook`,
`open_view`, `change_setting`, `generate_report`, `clear_jobs`,
`execute_script`, `query_corpus`, `compare_results`, `summarize_session`

**Research context injected in chat (Research mode):**
Sign catalog, benchmark scores (live from `reports/`), API reference with
working code examples, M77 profiles + worked L1 example, tier hierarchy,
Kandles domain knowledge, LEDGER last entry, scripting patterns.

### Fine-tuning

See `docs/FINETUNING_GUIDE.md` for how to train a Glossa-specific variant
of Mistral NeMo 12B via LoRA (Unsloth/Axolotl). Dataset generator at
`backend/scripts/generate_training_data.py`.

---

## STOP CONDITIONS

Stop if:

* missing inputs
* unclear state
* undocumented platform assumptions
* no proposal
* no ledger path

---

## ACCEPTANCE STANDARD

Work is accepted only if:

* proposal matched execution
* checks were run
* ledger updated
* next step defined

Otherwise: provisional only.

---

## GLOSSA AI GOVERNANCE LOOP (REQUIRED PRACTICE)

This governs how decipherment research and AI-driven analysis proceeds in Glossa Lab.
Violating this loop produces unreliable research and untestable AI behaviour.

### The Loop

```
  Oz proposes prompt
       ↓
  glossa_chat.py sends to Glossa AI
       ↓
  Glossa AI responds (text + optional %%ACTIONS%% block)
       ↓
  Oz evaluates response quality
       ├── GOOD: record findings, approve actions, continue
       └── BAD: fix context/system-prompt/profiles, re-run
```

### Role split — MANDATORY

| Role | Responsibility |
|---|---|
| **Oz (this agent)** | Prompt engineering, context maintenance, quality evaluation, infrastructure fixes |
| **Glossa AI** | Research analysis, hypothesis generation, Python script authoring, corpus interpretation |

**Oz MUST NOT directly write analysis code or compute research results.**  
All corpus analysis, sign assignment, and script authoring flows through Glossa AI.
Oz intervenes ONLY to fix the infrastructure when Glossa AI fails.

### When to run the test suite

```
# After every major research update or context change:
cd backend
venv\Scripts\python.exe glossa_chat.py --test --save
```

Results are saved to `reports/chat_test_<timestamp>.json`. Review them for:
- Hallucinated T-rates / counts not present in the research context → add real data via `_load_unassigned_profiles()`
- Wrong M77 visual type assignments → add explicit crosswalk to the context
- AI telling user to do something vs doing it itself → update `_ACTION_ADDENDUM`
- AI inventing values for unassigned signs → strengthen "cite context only" instruction

### When Glossa AI responses are bad

| Failure mode | Fix |
|---|---|
| Hallucinated numbers | Add real corpus profiles to `_load_unassigned_profiles()` in `glossa_chat.py` |
| Wrong M77 types | Add visual crosswalk table to research context |
| Action format errors | Tighten `_ACTION_ADDENDUM` instructions, fix parser |
| No action when expected | Check `action_capable` in `model_profiles.py` for the active model |
| AI too vague / no hypothesis | Add confidence-level requirement to system prompt instructions |

### Glossa AI capabilities — what it MUST be able to do

- Read and interpret all research context (sign assignments, corpus stats, LEDGER)
- Propose and write Python analysis scripts as code in responses
- Propose actions via `%%ACTIONS%%` blocks (run experiments, create hypotheses, run scripts)
- Make testable, falsifiable hypotheses with explicit confidence levels (HIGH/MED/LOW)
- Reject questions where the data is not in context: "I don't have X — run Y to get it"

### Research script lifecycle

1. Oz asks Glossa AI to design an analysis
2. Glossa AI writes Python code in its response
3. Oz saves the script to `backend/` (or AI proposes a `run_terminal` action)
4. Script is executed; results saved to `reports/`
5. Research context is refreshed (`/r` in REPL or re-run `--test`)
6. LEDGER entry records findings

### Hard rule H9 — AI does the research

All corpus queries, sign profile computations, hypothesis scoring, and
decipherment analysis MUST be initiated through Glossa AI prompts.
Oz writing analysis code directly is a governance violation unless
the purpose is to fix Glossa AI's context or tooling.

---

## PDF GENERATION RULES

All PDF reports generated via ReportLab MUST comply with the following rules.
Violations cause overlapping text, garbled characters, and unreadable output.

### P1 — Latin-1 fonts only

ReportLab's built-in fonts (Helvetica, Times-Roman, Courier) only support
Latin-1 encoding. **Never** embed Tamil, Arabic, Devanagari, CJK, or any
non-Latin-1 Unicode character in a Paragraph or table cell.
Use ASCII romanisation instead (e.g. `-um` not `உம்`).

The module `glossa_lab.report_utils` provides `safe_text()` which strips
unsafe characters automatically. Always call it or use `safe_tbl()` / `sp_text()`.

### P2 — Paragraph objects in all table cells

Bare strings in ReportLab tables do not wrap and cannot render markup.
All table cells MUST be `Paragraph` objects. Use `safe_tbl()` from
`glossa_lab.report_utils` which converts cells automatically.

### P3 — No raw newlines in strings passed to ReportLab

Raw `\n` characters inside Paragraph text are silently ignored, causing
text to merge on one line. Use `<br/>` for line breaks inside Paragraph
markup. `safe_tbl()` converts `\n` to `<br/>` automatically.

### P4 — Explicit `leading` on every ParagraphStyle

Leading = line height in points. Omitting it causes ReportLab to compute
a default that can be incorrect when styles are nested or inherited.
Minimum: `leading = fontSize * 1.4`. All styles in `make_styles()` from
`glossa_lab.report_utils` include explicit leading.

### P5 — Column widths must fit the page body

For A4 with 2.5 cm margins: `sum(colWidths) <= 16.0 cm (453 pt)`.
`safe_tbl()` raises `ValueError` if widths overflow.
Use the pre-computed width constants from `report_utils`: `_W3A`, `_W5V`, etc.

### P6 — Consolidate all TableStyle commands in one call

`t.setStyle()` **replaces** the existing style, not merges. If you call
`tbl()` and then `t.setStyle()` to add a highlight, the original style is
lost. Pass all style commands in a single `TableStyle([...])` call.
`safe_tbl(highlight_rows={...})` handles this correctly.

### P7 — Always use `glossa_lab.report_utils`

New report generators MUST import from `glossa_lab.report_utils` and use:
* `make_styles()` for all paragraph styles
* `safe_tbl()` for all tables
* `safe_text()` for all strings that may contain non-Latin characters
* `BODY_WIDTH` to compute column widths

Do not re-implement these helpers inline.

---

## GPU / CPU EXECUTION POLICY (H10 — MANDATORY)

> Always prefer GPU. Never silently fall back. Parallelise everything.

### H10.1 — GPU always first

* ALL computationally intensive code MUST check for GPU availability and use it.
* Use CuPy when available (`import cupy as cp`), falling back to NumPy only when CuPy is absent.
* The `BigramScorer` in `glossa_lab.pipelines.decipher` already implements this pattern — follow it everywhere.
* When falling back to CPU, log it explicitly: `logger.info("GPU unavailable — using NumPy CPU path")`.

```python
try:
    import cupy as xp
    _GPU = xp.cuda.is_available()
except ImportError:
    import numpy as xp
    _GPU = False
if not _GPU:
    import logging; logging.getLogger(__name__).info("GPU unavailable — using NumPy CPU path")
```

### H10.2 — Mandatory CPU parallelism when GPU is unavailable

* When GPU is not used, multi-core CPU execution is **mandatory** for all batch work.
* Use `concurrent.futures.ProcessPoolExecutor` for CPU-bound work (SA runs, corpus generation).
* Use `concurrent.futures.ThreadPoolExecutor` for I/O-bound work (file loading, API calls).
* The SA hillclimber – specifically the multi-seed loops in experiments – MUST run seeds in parallel.
* Parallelism ceiling: `min(N_SEEDS, os.cpu_count() or 4)`.

```python
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

def _run_parallel(fn, args_list, max_workers=None):
    """Run fn(args) in parallel, return list of results in submission order."""
    workers = max_workers or min(len(args_list), os.cpu_count() or 4)
    results = [None] * len(args_list)
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(fn, *a): i for i, a in enumerate(args_list)}
        for fut in as_completed(futs):
            results[futs[fut]] = fut.result()
    return results
```

### H10.3 — Graph node parallelism

In the experiment graph design (ExperimentBuilderView), nodes that are independent of each other
(no data dependency edge between them) MUST be visually and executionally parallelisable.
The graph runner must dispatch independent nodes to the thread/process pool simultaneously.

### H10.4 — What must use parallel execution

| Component | Parallelism required |
|---|---|
| SA seed loops in experiments | ProcessPoolExecutor per seed |
| Cross-LM / control-corpus batch runs | ProcessPoolExecutor per condition |
| Calibration / density curve points | ProcessPoolExecutor per density |
| Corpus generation (N instances) | ProcessPoolExecutor per instance |
| Bigram scoring (BigramScorer) | Already vectorised via numpy/cupy |
| Graph node execution | Parallel across independent nodes |

---

## EXPERIMENT / STUDY UI-FIRST POLICY (H12)

> Every experiment must be runnable from the Glossa Lab UI. No exceptions.

### H12.1 — ExperimentBase required

ALL Python experiment files in `backend/glossa_lab/experiments/` MUST define at
least one class that inherits from `glossa_lab.experiment_base.ExperimentBase`
and sets `id`, `name`, `category`, `description`, and `estimated_time`.

Standalone runner scripts that bypass `ExperimentBase` are **forbidden**.
If a script exists for legacy reasons, it MUST be wrapped in an ExperimentBase
subclass before new experiments are added to the same file.

### H12.2 — params_schema required for configurable experiments

Any experiment with configurable parameters MUST define `params_schema` as a
JSON Schema dict so the UI can render form controls for those parameters.

### H12.3 — run_cli() for terminal execution

When an experiment is run from the terminal, it MUST use `ExperimentBase.run_cli()`
or `CliReporter` so the job appears in the Jobs panel and reports are saved to
`reports/`. Plain `python my_experiment.py` is only acceptable as a convenience
wrapper that calls `run_cli()` internally.

Correct terminal usage pattern:
```python
if __name__ == "__main__":
    MyExperiment().run_cli()
```

### H12.4 — Parallel seeds mandatory

All SA-based experiments that loop over multiple seeds MUST use
`run_seeds_parallel()` from `glossa_lab.experiments._parallel` instead of a plain
`for seed in range(N):` loop. This is mandatory per H10.2.

Pattern:
```python
from glossa_lab.experiments._parallel import run_seeds_parallel

def _one_seed(seed, cipher_tokens, lm, anchors):
    from glossa_lab.pipelines.decipher import decipher
    return decipher(..., seed=seed, ...).get("proposed_mapping", {})

mappings = run_seeds_parallel(_one_seed, seeds=[1,2,3,4,5], cipher_tokens=..., lm=..., anchors=...)
```

### H12.5 — BigramScorer fast path

SA-based experiments MUST NOT set `ocp_weight > 0` or `use_word_bigrams=True`
unless those features are essential to the scientific question. Enabling these
bypasses the numpy/cupy BigramScorer fast path and can cause 50-200x slowdown.
Document any deliberate bypass with a comment explaining why.

---

## GRAPH-FIRST DESIGN (H15 — STRICT)

> Studies and experiments are graphs. Python is for atomic primitives only.

### H15.1 — The fundamental rule

Researchers must NOT be required to write Python to create studies or experiments.
All study-level and experiment-level logic MUST be expressed as a visual graph of
generic atomic nodes in the Experiment Builder or Study Builder.

**Python code is permitted ONLY for:**
- Atomic node implementations (`ATOMIC_NODES` in `experiment_graph.py`) — the
  lowest-level computational primitives that have no further decomposition
- Core pipeline engines (`pipelines/decipher.py`, `pipelines/block_entropy.py`, etc.)
  that implement well-defined mathematical algorithms
- Data loaders (`data/*.py`) that read corpus files and return symbols/inscriptions
- Backend infrastructure (API, database, CLI bridge, report generators)

**Python code is FORBIDDEN for:**
- Studies — must be graph JSON in `study_seeds.py` or created in the Studies UI
- Experiments that combine multiple analytical steps — must be graph JSON in
  `experiments/graphs/` created in the Experiment Builder
- Any `ExperimentBase` subclass that is a composition of existing atomic operations
  rather than a genuine new primitive

### H15.2 — What counts as a primitive

A primitive is an atomic operation that:
1. Has exactly one well-defined mathematical/algorithmic purpose
2. Cannot be decomposed into a meaningful sequence of existing atomic nodes
3. Would be opaque and non-visual if broken down further

Examples of genuine primitives (Python OK):
- `FreqCounter` — count symbol frequencies (one operation)
- `SADecipher` — run simulated annealing (one engine call)
- `LMBuilder` — build bigram language model (one data structure)
- `KLDivergence` — compute KL divergence (one formula)

Examples of NON-primitives (must be graph):
- `fuls_writing_system_comparison` — composes CorpusReader + FreqCounter +
  PositionalProfiler + EntropyCalc + WritingSystemClassifier
- `fuls_nw_semitic_benchmark` — composes structural analysis steps
- Any experiment that chains more than one conceptual analytical step

### H15.3 — Migration requirement

All existing `ExperimentBase` subclasses that are compositions (not primitives)
MUST be migrated to graph experiments. The ExperimentWrapper node is a TEMPORARY
bandage — it must be replaced with proper atomic node decomposition.

When adding a new experiment, ask: "Can this be built entirely from existing atomic
nodes in the Experiment Builder?" If yes — build it as a graph, not Python code.

### H15.4 — New atomic nodes

When a study requires an operation that no existing atomic node covers:
1. Add the new atomic node to `ATOMIC_NODES` in `experiment_graph.py`
2. Write only the implementation function (one pure fn(inputs, params) -> dict)
3. Register it in the catalog
4. Then build the study/experiment as a graph using that new node

Never write a new `ExperimentBase` subclass to work around a missing atomic node.

---

## PYTHON EXECUTION RULE (H14 — MANDATORY)

> Never run Python code via `python -c "..."`. Always use a script file.

### H14.1 — No inline python -c

`python -c "..."` is **absolutely forbidden** for any non-trivial command because:
- It cannot be interrupted cleanly (Ctrl-C / abort does not stop the computation)
- Long inline strings fail silently on Windows CMD/PowerShell
- Output does not stream — the caller blocks until the process exits or times out
- Debugging and logging are broken
- Shell timeouts behave unpredictably

### H14.2 — Required pattern: write a script file, then execute it

For any experiment, benchmark, verification, or multi-line Python:

```bat
:: 1. Write the script to a temp file
shell.cmd python backend/scripts/my_script.py

:: OR for one-off runs:
:: Write content to a .py file first, then:
shell.cmd python my_run.py
```

For the agent:
1. Use `create_file` to write the Python to a `.py` file in `backend/scripts/` or as a temp file
2. Then execute with `shell.cmd python <path/to/file.py>`
3. If the run needs to be stopped, the user can Ctrl-C the shell — which works correctly for script files

### H14.3 — One-liner exception (trivial checks only)

The ONLY acceptable use of `python -c` is for **single-line import/version checks** with zero computation:
```bat
python -c "import cupy; print(cupy.__version__)"
```
Anything with a loop, function call, or more than one statement MUST be a script file.

### H14.4 — Specsmith issue

Tracked as **EXEC-001** on the specsmith repository:
https://github.com/BitConcepts/specsmith/issues/70

---

## COMPUTE DEVICE REPORTING (H13)

> All jobs MUST report their compute device. The UI MUST display it.

### H13.1 — GPU/CPU detection

Every experiment that runs compute-intensive work MUST detect and log the compute
device at startup using `compute_device_label()` from
`glossa_lab.experiments._parallel`.

### H13.2 — Job params include compute device

When `CliReporter` registers a job, it automatically includes `compute_device`
and `compute_device_label` in the job params. Experiments that call `run_cli()`
inherit this automatically.

### H13.3 — UI badge mandatory

The Jobs panel MUST display a GPU/CPU badge (⚡ GPU / ⚙️ CPU) for every job that
has `compute_device` in its params. This is implemented in `JobsView.tsx`.

---

## APPLIED EPISTEMIC ENGINEERING (AEE) — specsmith Workflow (H11)

This project integrates Applied Epistemic Engineering principles from
[specsmith](https://github.com/BitConcepts/specsmith) and the
[AEE documentation](https://specsmith.readthedocs.io/en/stable/).

> Source: specsmith by BitConcepts. The AEE toolkit by the same author.

### AEE Core Method: Frame → Disassemble → Stress-Test → Reconstruct

1. **Frame** — state the claim/hypothesis as a `BeliefArtifact` with explicit propositions and epistemic boundaries
2. **Disassemble** — break compound claims into atomic, testable propositions
3. **Stress-Test** — apply 8 adversarial challenge categories to surface failure modes
4. **Reconstruct** — rebuild the claim from surviving propositions only; document what failed

### The 5 AEE Axioms

1. **Observability** — every belief must be inspectable (reproducible code + saved JSON)
2. **Falsifiability** — every belief must be challengeable (control experiments, stop conditions)
3. **Irreducibility** — beliefs decompose to atomic primitives (no compound claims)
4. **Reconstructability** — every failed belief can be rebuilt with more data or anchors
5. **Convergence** — stress-test + recovery always reaches Equilibrium

### The 7-Phase AEE Workflow

```
🌱 Inception → 🏗 Architecture → 📋 Requirements → ✅ Test Spec
    → ⚙ Implementation → 🔬 Verification → 🚀 Release
```

For EVERY study or experiment run in Glossa Lab:

| Phase | What the Glossa AI agent MUST do |
|---|---|
| Inception | State the research question as a falsifiable proposition |
| Architecture | Identify the corpus, LM, metric, and control strategy |
| Requirements | Define what results would confirm, partially confirm, or falsify the claim |
| Test Spec | Define the stop conditions and statistical thresholds |
| Implementation | Run experiments with GPU/parallel CPU; save all results as JSON |
| Verification | Apply adversarial challenges: random baselines, ablations, cross-LM |
| Release | Produce a report section stating clearly what was confirmed, partial, or refuted |

### Epistemic Markers — use in all claims

| Marker | Meaning |
|---|---|
| `[VERIFIED]` | Backed by experiment output in `reports/` |
| `[INFERRED]` | Logically derived from verified facts |
| `[ASSUMPTION]` | Working assumption; document epistemic boundary |
| `[UNCERTAIN]` | Missing data; state what experiment would resolve it |
| `[BLOCKER]` | Cannot proceed without resolving this |

### H11 — AEE enforcement rules

* Glossa AI conversations on research topics MUST maintain full conversation context.
* All hypotheses MUST be registered as `BeliefArtifact` entries (in `LEDGER.md` at minimum).
* Stop conditions from each experiment MUST be evaluated and reported honestly, never suppressed.
* If an experiment triggers a stop condition, the report section MUST lead with the failure, not bury it.
* Claims in emails to external collaborators MUST use AEE epistemic markers internally before being translated to plain prose.

---

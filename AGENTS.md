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

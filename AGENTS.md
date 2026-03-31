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
````

---

## SESSION LIFECYCLE

Agents MUST follow structured session flows.

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

* Windows (`.ps1`)
* Linux/macOS (`.sh`)

---

## REQUIRED SCRIPTS

```text
scripts/
  setup.ps1
  setup.sh
  run.ps1
  run.sh
```

---

## RUN CONTRACT

There MUST be a single way to run the system:

```bash
# Linux/macOS
./scripts/run.sh

# Windows
./scripts/run.ps1
```

This must:

* start backend
* optionally start frontend
* prepare environment

---

## SHELL INVOCATION

Scripts must:

* activate environment
* ensure dependencies installed
* launch backend entrypoint

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

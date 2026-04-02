# Rules

## Hard Rules

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

### H8 — No silent commands

If a command produces no output, it has failed. Do not retry it. Do not wait for it. Treat it as broken and fix the invocation or replace the command. Commands that are known to hang or produce no output are **forbidden**.

---

## Stop Conditions

Stop if:

* missing inputs
* unclear state
* undocumented platform assumptions
* no proposal
* no ledger path

---

## Acceptance Standard

Work is accepted only if:

* proposal matched execution
* checks were run
* ledger updated
* next step defined

Otherwise: provisional only.


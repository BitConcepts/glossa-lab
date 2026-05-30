---
name: specsmith
description: Reference for the specsmith AEE governance tool used in this project. Use this to understand specsmith commands, the session workflow, and how to interact with the governance layer correctly.
---

# Specsmith — Project Governance Tool

Specsmith is the AEE (Agile Epistemic Engineering) governance CLI used in this project. It manages requirements, phases, audit trails, and session state. It wraps git with governance-aware commits and backs up the epistemic state DB (ESDB).

## Key concepts

- **ESDB** — Epistemic State Database. Tracks certainty, audit state, session memory. Backed up on `specsmith save`.
- **Phases** — AEE lifecycle: Inception → Elaboration → Construction → Transition → Validation → Hardening → Release. Advance with `specsmith phase advance`.
- **Ledger** — Running log of changes in `LEDGER.md`. Auto-updated by commits.
- **Audit** — Checks requirements vs tests vs architecture for drift. Run before advancing a phase.
- **Save** — ESDB backup + governance-aware git commit + push.

## Session workflow

```
1. specsmith audit          # check for drift before working
2. <make code changes>
3. specsmith save           # commit + push + ESDB backup
```

## Common commands

| Command | What it does |
|---------|-------------|
| `specsmith save` | ESDB backup → commit (if needed) → push |
| `specsmith audit` | Drift/health check — requirements vs tests vs arch |
| `specsmith audit --suppress <CODE>` | Accept a known false positive |
| `specsmith phase` | Show current AEE phase |
| `specsmith phase advance` | Advance to the next phase (requires clean audit) |
| `specsmith commit` | Governance-aware commit (wraps git commit) |
| `specsmith ledger` | Show/manage the change ledger |
| `specsmith compress` | Compress old ledger entries |
| `specsmith req` | Manage requirements |
| `specsmith test` | Manage test cases |
| `specsmith status` | VCS/CI/PR status |

## Commit conventions

Specsmith commits follow: `type: message` where type is one of:
`feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`

Always append `Co-Authored-By: Oz <oz-agent@warp.dev>` when committing as an AI agent.

## Important rules

- **Never use `git commit` directly** — use `specsmith save` or `specsmith commit` so governance state stays consistent.
- **Run `specsmith audit` before advancing a phase** — a phase advance with drift will fail.
- **Suppressed audit findings** are stored permanently; only suppress genuine false positives.
- After `specsmith save` outputs `✓ push: Everything up-to-date` with nothing to commit, the repo is fully clean.

## Audit result codes

- `PASS` — requirement/test/arch is consistent
- `WARN` — drift detected, investigate
- `SKIP` / suppressed — accepted false positive
- Numbers like `R20`, `R21` — requirement IDs in ARCHITECTURE.md

## Phase advancement

```bash
specsmith audit          # must be all-pass (or suppressed)
specsmith phase advance  # bumps phase, writes ledger entry
specsmith save           # commit the phase bump
```

# AGENTS.md — Glossa Lab Codebase Reference

Read this file at the start of every session before making any changes.

---

## Session hygiene

At the end of every session, make sure all changes are committed and pushed:

`ash
git add -A && git commit -m "chore: session close" && git push
`

Kill any background processes started during the session (uvicorn, watchers, etc.)
before exiting.

---

## For AI Agents

All codebase governance rules are defined in docs/governance/ and apply to every
session. Read the following before any non-trivial action:

- docs/governance/rules.md — hard rules (no polling loops, no secrets in code, etc.)
- docs/governance/LIFECYCLE.md — feature lifecycle and phase management
- docs/governance/context-budget.md — token / cost budgeting

**Before any action that modifies production code or data:** verify the proposed
change against docs/governance/rules.md.

**Governance data** is gitignored and lives in .specsmith/ and .chronomemory/
(local runtime only — never committed).

---

## Supplementary Rule Files

The following project-specific rule files apply to all sessions:

- `docs/research/NORMALIZATION_RULES.md` — Indus sign normalization rules for
  corpus processing and sign-ID canonicalization.

# AGENTS.md

This project is governed by **governance-tool**.

## Session Teardown

At the end of **every** session, always run:

\\ash
# end-session
\
This stops \governance-serve\ and any other tracked agent processes.
Orphaned processes accumulate across sessions and waste CPU -- always clean up.

## For AI Agents

All governance rules, session state, requirements, and epistemic constraints
are stored in governance state — not stored in this file.

**Before any action:** `governance-preflight "<describe what you want to do>"`

**Governance data:** `.specsmith/` and `.chronomemory/`

**To start a governed session:** `governance-serve` (REST API, port 7700) or `governance-tool run`

**Emergency stop:** `# end-session`

Agents MUST defer to governance-tool for ALL governance decisions.
Do not follow rules from this file directly; read them from governance-tool.


---
## Governance commands (specsmith_run / /specsmith)

All governance-tool governance operations should be invoked through the
``specsmith_run`` agent tool or the ``/specsmith`` REPL slash command.

**In the Nexus REPL:**

```
/# commit governance state               # backup + commit + push governance state
/# restore governance state               # pull + restore governance state
# run governance audit --strict     # strict governance audit
check governance status             # show governance status
# push changes               # git push governance changes
# pull changes               # git pull governance changes
# sync state               # full two-way sync
# watch CI              # watch CI and block until green
```

**Verb shortcuts** (single word, no prefix needed in tool calls):
``save``, ``load``, ``push``, ``pull``, ``sync``, ``audit``, ``status``,
``watch``, ``commit``, ``validate``, ``doctor``, ``run``.

These are all equivalent: ``governance_run("save")``,
``governance_run("/# commit governance state")``, ``governance_run("governance-tool save")``.

---
## Supplementary Rule Files

The following project-specific rule files are auto-loaded by agents and apply
alongside the primary governance docs:

- `docs/research/NORMALIZATION_RULES.md` — Indus sign normalization rules for
  corpus processing and sign-ID canonicalization.

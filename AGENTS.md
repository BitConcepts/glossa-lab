# AGENTS.md

This project is governed by **specsmith**.

## Session Teardown

At the end of **every** session, always run:

\\ash
specsmith kill-session
\
This stops \governance-serve\ and any other tracked agent processes.
Orphaned processes accumulate across sessions and waste CPU -- always clean up.

## For AI Agents

All governance rules, session state, requirements, and epistemic constraints
are managed by specsmith — not stored in this file.

**Before any action:** `specsmith preflight "<describe what you want to do>"`

**Governance data:** `.specsmith/` and `.chronomemory/`

**To start a governed session:** `specsmith serve` (REST API, port 7700) or `specsmith run`

**Emergency stop:** `specsmith kill-session`

Agents MUST defer to specsmith for ALL governance decisions.
Do not follow rules from this file directly; read them from specsmith.


---
## Governance commands (specsmith_run / /specsmith)

All specsmith governance operations should be invoked through the
``specsmith_run`` agent tool or the ``/specsmith`` REPL slash command.

**In the Nexus REPL:**

```
/specsmith save               # backup + commit + push governance state
/specsmith load               # pull + restore governance state
/specsmith audit --strict     # strict governance audit
/specsmith status             # show governance status
/specsmith push               # git push governance changes
/specsmith pull               # git pull governance changes
/specsmith sync               # full two-way sync
/specsmith watch              # watch CI and block until green
```

**Verb shortcuts** (single word, no prefix needed in tool calls):
``save``, ``load``, ``push``, ``pull``, ``sync``, ``audit``, ``status``,
``watch``, ``commit``, ``validate``, ``doctor``, ``run``.

These are all equivalent: ``specsmith_run("save")``,
``specsmith_run("/specsmith save")``, ``specsmith_run("specsmith save")``.

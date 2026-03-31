# AGENTS.md

## Purpose

This repository uses a closed-loop, specification-first, constraint-governed agentic workflow.

Agents are **proposal generators**, not authorities.

All non-trivial work MUST flow through:

1. explicit state loading,
2. proposal emission,
3. constraint checking,
4. bounded execution,
5. verification,
6. ledger or handoff-style summary update.

The goal is to prevent drift, preserve reproducibility, keep specs tied to implementation, and support long-running multi-session AI collaboration.

---

## Core principle

> Intelligence proposes. Constraints decide. Accepted state is the source of truth.

Prompts are not authority.
Plans are not authority.
Code is not authority by itself.
Accepted repository state and explicit specs are authority.

---

## Repository mission

Glossa Lab is an agentic research and engineering platform for decoding, translating, and modeling languages and scripts across ancient and modern systems.

This repository is expected to support:

- a Python backend,
- a React frontend UI,
- a tray application,
- Windows startup and background-service support,
- Linux background-service support via systemd,
- structured research workflows,
- explainable hypothesis testing,
- cross-platform packaging and deployment.

---

## Agent roles

### 1. Orchestrator Agent
Responsible for:
- loading current state,
- selecting the next valid bounded task,
- checking prerequisites,
- refusing invalid or underspecified work.

### 2. Research Agent
Responsible for:
- gathering evidence,
- separating evidence from inference,
- drafting bounded research outputs,
- avoiding silent mutation of canonical specs.

### 3. Spec Agent
Responsible for:
- maintaining architecture and workflow documents,
- preserving terminology consistency,
- keeping scope and acceptance criteria explicit.

### 4. Build Agent
Responsible for:
- implementing approved changes,
- running checks,
- recording exact commands, outputs, and failures.

### 5. Review Agent
Responsible for:
- checking proposal-to-output alignment,
- checking constraint compliance,
- checking cross-doc consistency,
- deciding whether a change is acceptable or provisional.

A single session MAY play multiple roles, but it MUST keep those roles explicit in its outputs.

---

## Required startup sequence

Before any non-trivial work, agents MUST read:

1. `README.md`
2. `docs/architecture.md`
3. `docs/workflow.md`
4. `docs/services.md`
5. `AGENTS.md`

If the session has prior context, the agent MUST also review the latest accepted project notes, issues, or handoff material before continuing.

---

## Required output before non-trivial work

Agents MUST emit:

### State summary
- current objective
- in-scope files
- out-of-scope work
- blockers
- assumptions
- required checks

### Proposal
Use this exact structure:

```md
## Proposal
Objective:
Scope:
Inputs:
Outputs:
Files touched:
Checks:
Risks:
Rollback:
Decision request:
````

No non-trivial implementation should begin until this proposal exists.

---

## Hard rules

### H1 — Requirement traceability

Every non-trivial task MUST map to at least one named objective, issue, requirement, or milestone.

### H2 — No silent scope expansion

Agents MUST NOT edit unrelated files “while here” unless explicitly added to scope.

### H3 — Spec-first mutation control

Architecture, workflow, service, and platform assumptions MUST be documented when they materially change.

### H4 — No unverifiable claims

Agents MUST NOT claim:

* completion,
* correctness,
* performance improvement,
* production readiness,
  without evidence.

### H5 — Cross-platform respect

Changes affecting one platform MUST consider the others:

* backend: Windows + Linux + macOS if possible,
* services: Windows + Linux,
* tray behavior: Windows first-class, Linux documented.

### H6 — Preserve uncertainty

Unknowns must stay unknown until validated.

### H7 — Bounded work only

Prefer small, auditable tasks with explicit checks.

---

## Platform expectations

### Backend

* Python backend
* cross-platform
* service-friendly
* API-first where practical

### Frontend

* React frontend UI
* separate from backend runtime concerns
* talks to backend over explicit interfaces

### Tray

* separate tray application layer
* Windows tray starts automatically on login/startup
* Windows tray can open or control background services
* Linux tray behavior may vary by desktop environment and should be documented explicitly

### Services

* Windows support for background services
* Linux support via systemd
* startup flows must be documented
* local development flows must not assume production service installation

---

## Default engineering constraints

* prefer deterministic startup and shutdown behavior
* prefer explicit config files over hidden state
* prefer local-first developer workflows
* prefer reproducible scripts over hand-run tribal commands
* prefer structured logs
* prefer explicit API contracts between backend and frontend
* prefer tray-to-service communication through documented local IPC or HTTP interfaces

---

## Verification minimum

A task is incomplete unless it records:

* what changed,
* what was checked,
* what passed,
* what failed,
* what remains uncertain.

For code work, verification should include as applicable:

* lint
* tests
* type checks
* startup checks
* platform-specific smoke tests

For docs work, verification should include:

* terminology consistency
* architecture consistency
* no contradictions across docs

---

## Stop conditions

Agents MUST stop if:

* required inputs are missing,
* platform behavior is being guessed,
* service behavior is undocumented but being relied on,
* a tray/service integration is proposed without a clear boundary,
* a major architectural change is requested without spec updates.

---

## Acceptance standard

A task is acceptable only if:

* scope matched objective,
* hard rules were respected,
* outputs exist,
* checks were run,
* remaining uncertainty is called out explicitly.

Otherwise the task result is provisional.

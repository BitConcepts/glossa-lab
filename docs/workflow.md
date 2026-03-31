# Workflow

## Development style

This repository uses a specification-first, bounded-execution workflow.

Before significant implementation work:
1. define scope
2. define interfaces
3. define platform expectations
4. define verification checks
5. define rollback or recovery path
6. implement in bounded steps

The goal is to keep work explainable, auditable, and cross-platform aware.

---

## Required work loop

For non-trivial work, the expected loop is:

1. load current context
2. restate objective
3. restate scope and constraints
4. produce proposal
5. execute bounded work
6. verify results
7. summarize what changed
8. summarize what remains uncertain

The proposal should use the structure defined in `AGENTS.md`.

No non-trivial work should begin without an explicit proposal.

---

## Proposal-first rule

Before non-trivial implementation, documentation, or service/startup changes, the agent or contributor should explicitly state:

- objective
- scope
- inputs
- outputs
- files touched
- checks
- risks
- rollback

This keeps repository changes aligned with accepted intent.

---

## Pull request expectations

PRs should be:

- narrow
- explainable
- checked
- cross-platform aware
- explicit about uncertainty

Each PR should state:

- what changed
- why it changed
- what was checked
- what platform assumptions apply
- what remains unimplemented
- what follow-up work is expected, if any

---

## Cross-platform rule

Any work that affects startup, service control, file paths, packaging, local runtime behavior, tray behavior, installers, or background execution must explicitly mention:

- Windows impact
- Linux impact
- macOS impact

If one platform is intentionally unsupported, unaffected, or deferred, that must be stated explicitly.

---

## Documentation rule

Architecture-affecting changes MUST update the relevant docs in the same work cycle.

Examples:
- service behavior changes -> update `docs/services.md`
- component boundary changes -> update `docs/architecture.md`
- workflow/process changes -> update `AGENTS.md` and/or this file

Documentation should not lag behind accepted implementation intent.

---

## Verification rule

Every meaningful task should define checks before execution.

Checks may include:

- lint
- tests
- type checks
- startup validation
- service smoke tests
- tray interaction checks
- documentation consistency review

If checks were not run, that must be stated explicitly.

---

## Platform-sensitive work

The following types of work require extra caution:

- tray integration
- service lifecycle logic
- startup/login behavior
- filesystem paths
- installer/packaging logic
- local IPC or backend/frontend control boundaries

For these areas, contributors should prefer small steps and explicit documentation updates.

---

## Recommended milestones

### Milestone 1
- repo scaffold
- docs scaffold
- backend/frontend/tray boundaries documented

### Milestone 2
- Python backend scaffold
- React frontend scaffold
- local development startup flow

### Milestone 3
- backend health/status API
- tray scaffold
- tray-to-backend control plan
- explicit service boundary documented

### Milestone 4
- Windows startup behavior
- Windows tray behavior
- Windows background service support

### Milestone 5
- Linux systemd service support
- Linux startup documentation
- Linux tray constraints documented

### Milestone 6
- macOS startup behavior
- macOS tray behavior
- macOS service model documentation

### Milestone 7
- packaging
- smoke tests
- installer strategy
- cross-platform startup validation

---

## Default implementation preference

Prefer:

- one bounded task at a time
- explicit interfaces over hidden coupling
- documented service ownership
- deterministic startup/shutdown behavior
- cross-platform clarity over convenience shortcuts

Avoid:

- large mixed-purpose changes
- undocumented service assumptions
- tray logic absorbing backend responsibilities
- platform behavior inferred from another OS

# Workflow

## Development style

This repository uses a specification-first workflow.

Before large implementation work:
1. define scope
2. define interfaces
3. define platform expectations
4. define checks
5. implement in bounded steps

## Expected loop

1. load current context
2. restate objective
3. produce proposal
4. execute bounded work
5. verify
6. summarize what changed and what remains uncertain

## Pull request expectations

PRs should be:
- narrow
- explainable
- checked
- cross-platform aware

Each PR should state:
- what changed
- why it changed
- what was checked
- what platform assumptions apply
- what is still not implemented

## Cross-platform rule

Any work that affects startup, service control, file paths, packaging, or local runtime behavior must explicitly mention:
- Windows impact
- Linux impact
- whether macOS is unaffected, unsupported, or future work

## Recommended milestones

### Milestone 1
- repo scaffold
- docs scaffold
- backend/frontend/tray boundaries documented

### Milestone 2
- Python backend scaffold
- React frontend scaffold
- local dev startup flow

### Milestone 3
- tray scaffold
- backend health/status API
- tray-to-backend control plan

### Milestone 4
- Windows startup/tray behavior
- Windows background service support

### Milestone 5
- Linux systemd service support
- Linux startup documentation

### Milestone 6
- packaging
- smoke tests
- installer strategy

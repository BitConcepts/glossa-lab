# Implementation Plan: Spec 043 — PRED-2026-012 at full population, corrected frame: the canonical sign registry as primary source, a documentary provenance gate on the function codes (successor to Spec 038)

**Branch**: `main` (form migration on `hardening/legD-form-normalization`) | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/043-pred-2026-007-registry-frame/spec.md`

> **Form migration (Leg D hardening, 2026-10-29):** This file was created by structural migration into the current spec-kit form. Its content is derived only from this spec's own `spec.md`, `tasks.md`, and directory contents as of main 4913866d; it introduces no new study content, requirements, or results. The spec's historical record (LEDGER.md, freeze records, outcome files) is unchanged.

## Summary

PRED-2026-012 (H4 successor: ICIT Function
Alignment), registered 2026-10-21 in
`docs/PREDICTION_REGISTER.md` §3 as the
successor to PRED-2026-007 (H4: ICIT Function
Alignment, registered 2026-04-22), carrying
PRED-2026-007's prediction and success
criterion **verbatim**:

## Technical Context

**Language/Version**: Python 3.12 (project standard, per CI)

**Primary Dependencies**: spec-kit + AEE 1.5.3 governance flow (`.specify/`), project backend stack as recorded in this spec's own artifacts

**Storage**: Files in this spec directory (`specs/043-pred-2026-007-registry-frame/`); runtime state in `.glossa-state/` (never committed)

**Testing**: pytest (backend) and this spec's own verification artifacts where present

**Target Platform**: Glossa Lab (Linux/Windows desktop + VM development)

**Project Type**: Research spec in the Glossa Lab spec sequence

**Constraints**: Citation and provenance discipline per `.specify/memory/constitution.md`; frozen records (where `freeze.json` is present) are append-only and are not modified by this migration

**Scale/Scope**: This spec directory: 9 files

## Constitution Check

*GATE: evaluated against `.specify/memory/constitution.md`.*

- Citation/provenance discipline and the append-only ledger rule apply to this spec as ratified 2026-10-05. This migration adds form artifacts only and changes no claim, evidence, or freeze record.

## Project Structure

### Documentation (this feature)

```text
specs/043-pred-2026-007-registry-frame/
├── adjudication.md
├── build_freeze.py
├── claims.json
├── freeze.json
├── freeze.md
├── osf-spec-registration.md
├── outcome.md
├── spec.md
├── tasks.md
├── aee/
```

## Phases (from this spec's own tasks/spec structure)

- Lifecycle
- Execution — gated on the freeze and a separate execution order
- Not done by this draft (by design)

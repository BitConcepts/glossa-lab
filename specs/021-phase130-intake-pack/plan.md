# Implementation Plan: Spec 021 — Phase-130: Independent-Data Intake Pack

**Branch**: `main` (form migration on `hardening/legD-form-normalization`) | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/021-phase130-intake-pack/spec.md`

> **Form migration (Leg D hardening, 2026-10-29):** This file was created by structural migration into the current spec-kit form. Its content is derived only from this spec's own `spec.md`, `tasks.md`, and directory contents as of main 4913866d; it introduces no new study content, requirements, or results. The spec's historical record (LEDGER.md, freeze records, outcome files) is unchanged.

## Summary

**Status:** BUILT 2026-10-08 on `phase/130-intake-pack`
(from main `9f0ec4da`, after PR #92). Owner-ordered program
(Workstream 5 of 5, 2026-10-08): build the intake machinery
so that when a genuinely independent inscription dataset
lands, receiving it is a procedure, not a negotiation —
the intake-side companion to spec 018 (Phase-119), whose
harness waits downstream.

## Technical Context

**Language/Version**: Python 3.12 (project standard, per CI)

**Primary Dependencies**: spec-kit + AEE 1.5.3 governance flow (`.specify/`), project backend stack as recorded in this spec's own artifacts

**Storage**: Files in this spec directory (`specs/021-phase130-intake-pack/`); runtime state in `.glossa-state/` (never committed)

**Testing**: pytest (backend) and this spec's own verification artifacts where present

**Target Platform**: Glossa Lab (Linux/Windows desktop + VM development)

**Project Type**: Research spec in the Glossa Lab spec sequence

**Constraints**: Citation and provenance discipline per `.specify/memory/constitution.md`; frozen records (where `freeze.json` is present) are append-only and are not modified by this migration

**Scale/Scope**: This spec directory: 1 files

## Constitution Check

*GATE: evaluated against `.specify/memory/constitution.md`.*

- Citation/provenance discipline and the append-only ledger rule apply to this spec as ratified 2026-10-05. This migration adds form artifacts only and changes no claim, evidence, or freeze record.

## Project Structure

### Documentation (this feature)

```text
specs/021-phase130-intake-pack/
├── spec.md

```

## Phases (from this spec's own tasks/spec structure)

- Epistemic boundaries (H13)
- 1. Scope
- 2. Dataset schema (deliverable 1)
- 3. Validator + license gate (deliverable 2)
- 4. Dedup as a reusable module (deliverable 3)
- 5. Structural rule — dry-run only
- 6. Crosswalk adapter requirements (deliverable 4)
- 7. Intake runbook (deliverable 5)
- 8. Synthetic fixture
- 9. Implementation (this phase)
- 10. What this phase does not do

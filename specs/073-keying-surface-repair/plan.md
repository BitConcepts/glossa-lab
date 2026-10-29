# Implementation Plan: Spec 073 — Repairing the Keying Surface: Registry Wells Coverage and a Second Depicted-Kind Classification, from Published Sources Only

**Branch**: `main` (form migration on `hardening/legD-form-normalization`) | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/073-keying-surface-repair/spec.md`

> **Form migration (Leg D hardening, 2026-10-29):** This file was created by structural migration into the current spec-kit form. Its content is derived only from this spec's own `spec.md`, `tasks.md`, and directory contents as of main 4913866d; it introduces no new study content, requirements, or results. The spec's historical record (LEDGER.md, freeze records, outcome files) is unchanged.

## Summary

**Design source:** the merged execution
records of Spec 070 (Phase 433,
`specs/070-hunt-opening-signs-successor/outcome.md`)
and Spec 071 (Phase 434,
`specs/071-hunt-sky-signs-successor/outcome.md`),
read first-hand at this draft; Spec 069's
executed Asset A record
(`specs/069-hunt-asset-a/asset-a/asset-a-freeze.json`
and its entry log); Spec 045's frozen
§§2–3 (the Asset A contract, freeze digest
`5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`);
and the Shakti intake record
(`docs/decisions/2026-10-22-shakti-corpus-intake-record.md`,
proposal P-F1 as adopted).

## Technical Context

**Language/Version**: Python 3.12 (project standard, per CI)

**Primary Dependencies**: spec-kit + AEE 1.5.3 governance flow (`.specify/`), project backend stack as recorded in this spec's own artifacts

**Storage**: Files in this spec directory (`specs/073-keying-surface-repair/`); runtime state in `.glossa-state/` (never committed)

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
specs/073-keying-surface-repair/
├── adjudication.md
├── build_freeze.py
├── claims.json
├── freeze.json
├── freeze.md
├── keying-surface-accounting-2026-10-25.md
├── outcome.md
├── spec.md
├── tasks.md
├── aee/
├── asset-a-v2/
├── execution/
├── registry-v2/
```

## Phases (from this spec's own tasks/spec structure)

- Lifecycle
- Execution — gated on the freeze and a separate execution order

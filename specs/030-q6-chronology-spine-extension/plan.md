# Implementation Plan: Spec 030 — Q6 Chronology-Spine Extension

**Branch**: `main` (form migration on `hardening/legD-form-normalization`) | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/030-q6-chronology-spine-extension/spec.md`

> **Form migration (Leg D hardening, 2026-10-29):** This file was created by structural migration into the current spec-kit form. Its content is derived only from this spec's own `spec.md`, `tasks.md`, and directory contents as of main 4913866d; it introduces no new study content, requirements, or results. The spec's historical record (LEDGER.md, freeze records, outcome files) is unchanged.

## Summary

Spec 027 Stage 0 (Phase-391) built the chronology spine
(177 traced rows) and assessed Q6 timing-support against
criteria frozen **before the spine existed**
(`specs/027-movement-culture-language/stage0-freeze.md`
§4). The assessment returned **NOT-YET-TESTABLE**: three
of four criteria failed. Q6 therefore remains
registered-blocked, and F027-C16 forbids a Q6 freeze
until the §8.2 support conditions are shown.

## Technical Context

**Language/Version**: Python 3.12 (project standard, per CI)

**Primary Dependencies**: spec-kit + AEE 1.5.3 governance flow (`.specify/`), project backend stack as recorded in this spec's own artifacts

**Storage**: Files in this spec directory (`specs/030-q6-chronology-spine-extension/`); runtime state in `.glossa-state/` (never committed)

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
specs/030-q6-chronology-spine-extension/
├── adjudication-confirmation.md
├── adjudication.md
├── build_freeze.py
├── claims.json
├── freeze.json
├── freeze.md
├── osf-registration.md
├── outcome.md
├── spec.md
├── aee/
```

## Phases (from this spec's own tasks/spec structure)

- 1. Purpose
- 2. The frozen criteria and the measured gaps
- 3. Gap anatomy — what exactly is missing, per criterion
- 4. Extension routes — candidate sources and licence posture
- 5. Integrity rules (binding on any future freeze of this design)
- 6. Re-test protocol (Q6 timing-support, on the extended spine)
- 7. What this design does not do
- 8. Governed claims (summary)
- 9. Asks for adjudication (owner decisions)

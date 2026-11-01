# Implementation Plan: Spec 041 — Site × Local-Label Period Mapping

**Branch**: `main` (form migration on `hardening/legD-form-normalization`) | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/041-site-local-label-period-mapping/spec.md`

> **Form migration (Leg D hardening, 2026-10-29):** This file was created by structural migration into the current spec-kit form. Its content is derived only from this spec's own `spec.md`, `tasks.md`, and directory contents as of main 4913866d; it introduces no new study content, requirements, or results. The spec's historical record (LEDGER.md, freeze records, outcome files) is unchanged.

## Summary

**Parent records:** Spec 040 (D-25, closed
NOT-YET-TESTABLE — dependency gate, 2026-10-20) ·
Spec 039 (gazetteer period-assignment act, executed
Phase-403) · Spec 025 / Phase-139 / Phase-140 /
Phase-385 (the G1 record) · **Phase:** Phase-435
(allocated at the freeze act, DD-041-14) · **Date of
proposal:** 2026-10-21 · **Frozen:** 2026-10-22.

## Technical Context

**Language/Version**: Python 3.12 (project standard, per CI)

**Primary Dependencies**: spec-kit + AEE 1.5.3 governance flow (`.specify/`), project backend stack as recorded in this spec's own artifacts

**Storage**: Files in this spec directory (`specs/041-site-local-label-period-mapping/`); runtime state in `.glossa-state/` (never committed)

**Testing**: pytest (backend) and this spec's own verification artifacts where present

**Target Platform**: Glossa Lab (Linux/Windows desktop + VM development)

**Project Type**: Research spec in the Glossa Lab spec sequence

**Constraints**: Citation and provenance discipline per `.specify/memory/constitution.md`; frozen records (where `freeze.json` is present) are append-only and are not modified by this migration

**Scale/Scope**: This spec directory: 14 files

## Constitution Check

*GATE: evaluated against `.specify/memory/constitution.md`.*

- Citation/provenance discipline and the append-only ledger rule apply to this spec as ratified 2026-10-05. This migration adds form artifacts only and changes no claim, evidence, or freeze record.

## Project Structure

### Documentation (this feature)

```text
specs/041-site-local-label-period-mapping/
├── adjudication.md
├── build_freeze.py
├── claims.json
├── coverage-report.md
├── determinations.json
├── freeze.json
├── freeze.md
├── osf-spec-registration.md
├── outcome.md
├── spec.md
├── step0-census.json
├── step0-record.md
├── tasks.md
├── verification-record.json
├── aee/
```

## Phases (from this spec's own tasks/spec structure)

- Lifecycle
- Execution — gated on the freeze and a separate execution order

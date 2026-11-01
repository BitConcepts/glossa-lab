# Implementation Plan: Spec 075 — Depicted-Kind Endings Atlas: Which Kinds of Signs Gather at the Ends of Inscriptions, on the Shakti Corpus (Phase 441)

**Branch**: `main` (form migration on `hardening/legD-form-normalization`) | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/075-depicted-kind-endings-atlas/spec.md`

> **Form migration (Leg D hardening, 2026-10-29):** This file was created by structural migration into the current spec-kit form. Its content is derived only from this spec's own `spec.md`, `tasks.md`, and directory contents as of main 4913866d; it introduces no new study content, requirements, or results. The spec's historical record (LEDGER.md, freeze records, outcome files) is unchanged.

## Summary

**Status: drafted at the freeze act of 2026-10-25**,
under the owner's order of the same date ("do the
atlas freeze"). This spec is the study designed as
Candidate B of the Spec 071 redesign proposal
(2026-10-24) and designed in full on 2026-10-25
(`2026-10-25-endings-atlas-design.md`, the
programme's goal record; requirements R1–R13 of
that design are carried into this spec and cited
beside the sections that carry them). **This
freeze is the C4 SHADOW FREEZE** designated in
the design's §7 and in the freeze-gate build
decision of 2026-10-25: the strengthened gate
(C1–C4) runs in full on it an

## Technical Context

**Language/Version**: Python 3.12 (project standard, per CI)

**Primary Dependencies**: spec-kit + AEE 1.5.3 governance flow (`.specify/`), project backend stack as recorded in this spec's own artifacts

**Storage**: Files in this spec directory (`specs/075-depicted-kind-endings-atlas/`); runtime state in `.glossa-state/` (never committed)

**Testing**: pytest (backend) and this spec's own verification artifacts where present

**Target Platform**: Glossa Lab (Linux/Windows desktop + VM development)

**Project Type**: Research spec in the Glossa Lab spec sequence

**Constraints**: Citation and provenance discipline per `.specify/memory/constitution.md`; frozen records (where `freeze.json` is present) are append-only and are not modified by this migration

**Scale/Scope**: This spec directory: 11 files

## Constitution Check

*GATE: evaluated against `.specify/memory/constitution.md`.*

- Citation/provenance discipline and the append-only ledger rule apply to this spec as ratified 2026-10-05. This migration adds form artifacts only and changes no claim, evidence, or freeze record.

## Project Structure

### Documentation (this feature)

```text
specs/075-depicted-kind-endings-atlas/
├── RED-TEAM-ADDENDUM-2026-10-25.md
├── adjudication.md
├── build_freeze.py
├── claims.json
├── freeze.json
├── freeze.md
├── osf-spec-registration.md
├── outcome.md
├── spec.md
├── step0-record.md
├── tasks.md
├── aee/
├── gate-records/
```

## Phases (from this spec's own tasks/spec structure)

- Lifecycle (this freeze)
- Execution (gated — the owner's order of 2026-10-25 12:03 EDT, on the completed freeze record)

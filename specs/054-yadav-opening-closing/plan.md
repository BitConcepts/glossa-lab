# Implementation Plan: Spec 054 — Yadav's Opening/Closing Signs: Given a Falsifier, Then Rerun (Design D-08)

**Branch**: `main` (form migration on `hardening/legD-form-normalization`) | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/054-yadav-opening-closing/spec.md`

> **Form migration (Leg D hardening, 2026-10-29):** This file was created by structural migration into the current spec-kit form. Its content is derived only from this spec's own `spec.md`, `tasks.md`, and directory contents as of main 4913866d; it introduces no new study content, requirements, or results. The spec's historical record (LEDGER.md, freeze records, outcome files) is unchanged.

## Summary

**Design source:** D-08 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/01-language-and-position.md`,
§D-08, read in full at this draft), with the
portfolio triage of 2026-10-21 (design D-08
found **RIPE**: "Strict corpus, Holdat layer,
and crosswalk are in hand; Phase-43 thresholds
are on record. The design's first product — a
falsifier written onto a record that never had
one — is available whatever the rerun finds.").

## Technical Context

**Language/Version**: Python 3.12 (project standard, per CI)

**Primary Dependencies**: spec-kit + AEE 1.5.3 governance flow (`.specify/`), project backend stack as recorded in this spec's own artifacts

**Storage**: Files in this spec directory (`specs/054-yadav-opening-closing/`); runtime state in `.glossa-state/` (never committed)

**Testing**: pytest (backend) and this spec's own verification artifacts where present

**Target Platform**: Glossa Lab (Linux/Windows desktop + VM development)

**Project Type**: Research spec in the Glossa Lab spec sequence

**Constraints**: Citation and provenance discipline per `.specify/memory/constitution.md`; frozen records (where `freeze.json` is present) are append-only and are not modified by this migration

**Scale/Scope**: This spec directory: 13 files

## Constitution Check

*GATE: evaluated against `.specify/memory/constitution.md`.*

- Citation/provenance discipline and the append-only ledger rule apply to this spec as ratified 2026-10-05. This migration adds form artifacts only and changes no claim, evidence, or freeze record.

## Project Structure

### Documentation (this feature)

```text
specs/054-yadav-opening-closing/
├── adjudication.md
├── amendment.md
├── build_freeze.py
├── claims.json
├── freeze.json
├── freeze.md
├── osf-spec-registration.md
├── outcome-run2.md
├── outcome.md
├── spec.md
├── step0-record-run2.md
├── step0-record.md
├── tasks.md
├── aee/
```

## Phases (from this spec's own tasks/spec structure)

- Lifecycle
- Execution — gated on the freeze and a separate execution order
- Amendment — 2026-10-23 (owner mini-gate)

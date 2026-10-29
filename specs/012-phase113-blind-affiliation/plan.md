# Implementation Plan: Spec 012 — Phase-113: Blind Language-Affiliation Study, Adversarial Protocol (pre-registration)

**Branch**: `main` (form migration on `hardening/legD-form-normalization`) | **Date**: 2026-10-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/012-phase113-blind-affiliation/spec.md`

> **Form migration (Leg D hardening, 2026-10-29):** This file was created by structural migration into the current spec-kit form. Its content is derived only from this spec's own `spec.md`, `tasks.md`, and directory contents as of main 4913866d; it introduces no new study content, requirements, or results. The spec's historical record (LEDGER.md, freeze records, outcome files) is unchanged.

## Summary

**Status:** FROZEN 2026-10-07 on `phase/113-blind-affiliation-adversarial`
(from main f82c81fa, which contains the completed Phase-111 (spec
009) and Phase-112 (spec 010) pipelines and outcomes). Owner
authorization: Tristen Pierson, 2026-10-07 (roadmap item 4 — the
adversarial successor). The git order — design-stage tooling commits
(110c1fe9, dc57566b), then this spec committed before any Phase-113
panel build, gate evaluation, adversarial round, or Indus statistic
exists — is the pre-registration proof.

## Technical Context

**Language/Version**: Python 3.12 (project standard, per CI)

**Primary Dependencies**: spec-kit + AEE 1.5.3 governance flow (`.specify/`), project backend stack as recorded in this spec's own artifacts

**Storage**: Files in this spec directory (`specs/012-phase113-blind-affiliation/`); runtime state in `.glossa-state/` (never committed)

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
specs/012-phase113-blind-affiliation/
├── spec.md

```

## Phases (from this spec's own tasks/spec structure)

- Context — why this study exists
- Scope
- 1. Panel (inherited from spec 009 as assembled; spec 010 §1)
- 2. Resampling (inherited from spec 009 §2, unchanged)
- 3. Unit rules (inherited from spec 009 §3, unchanged)
- 4. Feature ladder
- 5. Fixed synthetic controls S1–S5 (inherited, unchanged)
- 6. Adversarial generator family G(θ) (frozen)
- 7. Optimizer (frozen)
- 8. Rounds protocol, gates, and control validity
- 9. Validation gate (inherited from spec 009 §7, unchanged)
- 10. Indus verdict rules (inherited from spec 009 §9,
- 11. Multiplicity (inherited from spec 009 §10, unchanged)
- 12. Deviations (inherited policy)
- 13. Limitations (registered at freeze time)
- 14. Licensing (inherited from spec 009 §13; owner directive 2026-10-06)
- 15. Deliverables (frozen)

# Inventory gaps — Spec 026 impact audit (extraction only, 2026-10-10)

Scope searched: `specs/001-*`–`specs/025-*`; `backend/reports/phase*.{json,md}`;
`reports/phase*.{json,md,csv,txt}` (repo root); `LEDGER.md`; `glossa-indus/LEDGER.md`.
Method: directory listing + grep + targeted reads of spec.md/tasks.md, phase
summary .md files, JSON top-level keys, and ledger excerpts. No classification
or re-judgment was performed.

## Counts
- Specs: 26 directories for numbers 001–025 (021 is duplicated — see below).
- Phases 52–141: 90 numbers; 82 have at least one artifact in the scoped
  locations; 8 have none in scope (92, 93, 94, 95, 97, 98, 99, 100).

## Missing in scoped locations
- PHASE-92, 93, 94, 95, 97, 98, 99, 100: no file in `backend/reports/` or
  `reports/`, and no entry in either ledger. Artifacts with these numbers DO
  exist outside the stated scope in `outputs/` (e.g. `outputs/phase92_uncertain_reduction.json`,
  `outputs/phase93_m293_sa.json`, `outputs/phase94_fulltext_mine.json`,
  `outputs/phase95_retroflex_expansion.json`, `outputs/phase97_trigram_sa.json`,
  `outputs/phase98_grammar_expansion.json`, `outputs/phase100_full_corpus.json`;
  99 not confirmed even there in the listing checked) — they were NOT used as
  inventory sources because the task scoped sources to the three locations above.
- PHASE-96: only a ledger mention in scope; its JSON artifact is in `outputs/phase96_cisi_crosswalk.json` (out of scope).
- PHASE-53–91, 101–104 (most): no dedicated report file in `reports/` or
  `backend/reports/`; represented in scope ONLY by ledger entries (often a
  single grouped entry, e.g. Phases 62–66, 80–87 foundation-report entries).
  Verdict, controls, freeze, CI/effect-size, grid and independence fields for
  these are therefore mostly "unknown" in inventory.json — not determinable
  from the scoped files without reading `outputs/` / `research/indus/phase_reports/`,
  which were outside the stated scope. Note: `research/indus/phase_reports/`
  in this checkout actually contains copies of the backend/reports phase127+
  JSONs, not the early phases.
- PHASE-114: no standalone report. Spec 012's execution was renumbered in code
  (`phase114_run.py`) while its artifacts were frozen under `phase113_*` names
  (`reports/phase113_blind_affiliation_*`). Inventory treats 114 via that note.
- PHASE-113 is two different studies under one number: Spec 011 non-SA44
  validation (`phase113_nonsa44_*`) and Spec 012 blind affiliation
  (`phase113_blind_affiliation_*`). Both are in the PHASE-113 entry.
- Combined-number artifacts: `phase128_129_*` (backend/reports), 
  `phase136_140_battery.json`, `phase136_137_138_stage2_report.md`,
  `phase139_140_141_spec025_report.md` cover multiple phases in one file;
  per-phase entries share those source_files.
- Phases 142–170 exist in `backend/reports/` but are OUT of the 52–141 scope
  and were not inventoried.

## Spec gaps
- Duplicate numbering: `specs/021-phase127-cross-compilation-diagnostic/` and
  `specs/021-phase130-intake-pack/` are both Spec 021 (inventoried as
  SPEC-021 and SPEC-021-INTAKE).
- `specs/012-phase113-blind-affiliation/` and `specs/021-phase130-intake-pack/`
  contain only `spec.md` — no plan.md / tasks.md, so freeze/control details
  are thinner for those two.
- Specs 001–004 are platform/baseline specs, not Indus phase analyses; they
  are inventoried for completeness with most analysis fields "unknown".
- No spec directories exist for most phases 52–104 or 120–124, 126, 128–130,
  132–138 (those phases are report/ledger-only; governing specs, where any,
  are 005 for Phase-52 v2 / Phase-107 validation, 019 for 125, 020 Soviet
  adjudication covering 121–122 material, 024 for 133–138, 025 for 139–141).

## Field-level gaps (apply across the inventory)
- `frozen`: determinable only where a summary/spec explicitly says "frozen"
  or a freeze file exists (Specs 009–025 area, Spec 024 freeze files,
  Spec 025 phase139/140/141-freeze.md). For ledger-only phases it is "unknown".
- `uncertainty_reported`, `grid_complete`, `independence_notes`: rarely stated
  in ledger-only entries; recorded as "unknown" rather than inferred. JSON
  artifacts in `reports/` for 107–141 were key-scanned, not fully parsed for
  every numeric field, so a "no CI language in sources scanned" entry means
  not found in the summary/ledger/keys scan — not proof none exists in the
  full JSON payload.
- `origin_groups` for early phases derives from ledger mentions (M77, ICIT,
  Holdat, CISI, Wells, Fuls, Parpola, Soviet tables); where the ledger excerpt
  named none, the field is ["unknown"].

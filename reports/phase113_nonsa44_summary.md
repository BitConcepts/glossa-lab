# Phase-113 — Non-SA Validation Battery for the 44 SA-Lineage Anchors

**Spec:** specs/011-phase113-nonsa44-validation (frozen before any results) · **Date:** 2026-10-07 · **GPU device:** cpu (torch absent)

## Verdict

**BATTERY REJECTED at calibration.** The frozen gates of spec 011 section 4 were not both met, so FLAGGED44 was never run and the anchors file was not modified. The battery may not be re-tuned under this spec.

## Calibration (executed before the 44; reported whatever it showed)

| Set | n | VALIDATED | DEMOTE | UNRESOLVED | Gate |
|---|---|---|---|---|---|
| STRICT94 (positive, leave-one-out) | 94 | 3 | 45 | 46 | >= 57 required: **FAIL** |
| KUR113 (negative control) | 113 | 0 | 16 | 97 | <= 5 required: **PASS** |

## Sets and corpora (recomputed; assertions in spec section 2)

- FLAGGED44: 44 anchors (24 SA_DERIVED + 20 SA_CONFIRMED_ONLY; 43 HIGH + M293 MEDIUM).
- STRICT94: 94 anchors (90 HIGH + 4 MEDIUM); Holdat token coverage 0.7368 (5,159 / 7,002).
- KUR113: 113 premise-superseded anchors, all reading `kur`.
- Holdat: 1670 inscriptions / 7002 tokens. ICIT converted layer: 1007 inscriptions / 2238 tokens (local restricted data; statistics only).

## Limitations (registered in spec section 8)

A PASS certifies distributional and compositional survival under independent non-SA tests; it does not prove the phonetic value. A FAIL demotes to CANDIDATE; it does not declare the reading false. Holdat and the ICIT layer are independent compilations of the same published catalogues, not independent archaeology; T1 NOT_ATTESTED partly measures ICIT conversion coverage.

## Calibration diagnosis (post-hoc, descriptive — no re-tuning performed or permitted)

Per-test states over the STRICT94 leave-one-out calibration
(from `phase113_nonsa44_results.json`):

| Test | PASS | FAIL | NOT_ATTESTED / INDETERMINATE |
|---|---|---|---|
| T1 cross-corpus | 11 | 22 | 61 NOT_ATTESTED |
| T2 positional grammar | 60 | 13 | 21 INDETERMINATE |
| T3 compositional | 34 | 19 | 41 INDETERMINATE |

- **T2 is sound**: the profile-fit component passes 91/94; all
  13 T2 failures come from the reading–slot phonotactics
  sub-check (12 on class-initial-inventory membership). The
  strict core's positional grammar is real and measurable.
- **T3's legality component never fires**: of 89 strict signs
  with contexts, **zero** fall below the 0.75 legal-fraction
  bar — composed strict-core readings are canon-legal
  throughout. T3's binding constraint is partner support
  (only 35/94 reach ≥ 3 strict partners under leave-one-out).
- **T1 is the failing component, and it fails on data, not on
  anchors**: 45 of 94 strict signs have **zero** tokens in the
  ICIT converted layer and 16 more have 1–2 (below the frozen
  attestation floor of 3), so 61/94 are NOT_ATTESTED before any
  consistency is measured; of the 33 attested, 22 FAIL on
  modal-class disagreement or profile distance against Holdat.
  The converted layer (1,007 inscriptions / 2,238 tokens, from
  5,679 source inscriptions at 69.3% token-map coverage) is too
  sparse and too conversion-noisy to carry a conjunctive
  cross-corpus gate — the caveat registered in spec section 8,
  now measured.
- **KUR113**: 0 validated (gate passed). All 113 are
  INDETERMINATE on T2/T3 via the frequency guard (rare signs)
  and 89/113 are NOT_ATTESTED on T1 — the negative control
  confirms the battery does not validate known-bad readings,
  but the positive control shows it cannot validate known-good
  ones either, at the frozen thresholds, on the corpora that
  exist. A battery that can only refuse is not a validation
  instrument; per spec section 4 it is rejected, and any
  redesigned battery (e.g. T1 rebuilt on a fuller ICIT layer,
  or attestation floors scaled to layer coverage) requires a
  new spec.

## Verification

Recorded in the phase ledger entries and the PR body (full backend suite; foundation check per H21; ruff).

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution section VI.

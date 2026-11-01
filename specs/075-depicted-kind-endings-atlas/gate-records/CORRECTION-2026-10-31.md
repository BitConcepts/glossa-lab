# Correction — 2026-10-31: Spec 075 freeze-gate records (C2/C3) repaired

This file is the human-readable record of a correction to this
spec's C2 spot-check and C3 evidence-sample records. It follows
the programme's correction discipline: the as-filed records are
preserved in git history (commit `fa34a92b`, the Spec 075 freeze
commit), the corrections are declared inside the corrected
records themselves (a `correction` entry in each), and the act
is entered in `LEDGER.md`. Nothing in this correction touches
the spec's claims, verdicts, frozen pins, or any other spec's
records — Spec 075's verdicts recompute exactly and stand, as
the 2026-10-25 red-team addendum established; only the freeze
RECORD was defective.

## The defect

Main-branch CI, job "Freeze gate records check" (the checker in
`--all` mode), failed on this spec in runs 41155682213,
41157454467 and 41167817221 — the named red item in the
2026-10-31 day-end CI accounting. PR runs use `--pr-scope`, so
no PR ever exercised these paths. The checker's findings:

- Five C2 quantities carried status `agree` while marked
  unsampled (`registry_v1_rows`, `crosswalk_rows`,
  `anchors_sha256`, `total_analyzable_rows`,
  `documented_lineage_rows_total`). Under the gate's rules an
  unsampled quantity has no checked status.
- `coverage.other_checked` did not match the quantities list
  under the checker's definition.
- The C3 record's verifier was the same identity as the C2
  record's drafter; verification must be by someone other than
  the drafter.

## What was actually true

The five quantities all carried recomputed values equal to
their pins as filed, and the scaffold's seeded draw (seed
20261025, re-run during this repair) reproduces the originally
filed sample exactly — the five stood outside the drawn sample,
so their `agree` statuses were unsupported as filed, and the
coverage count of 8 counted values the filed sampling did not
support (the checker's definition yields 3 on the filed
sampling). The C3 self-verification had been disclosed in the
open at the time (`RED-TEAM-ADDENDUM-2026-10-25.md` §5) but
never cured.

## The repair

Performed 2026-10-31 by a Muse subagent (C4 freeze-gate
repair worker; session 4413edc7), who is not the drafting
session (d02f80d3):

1. **Each of the five quantities was independently recomputed
   from its underlying source**, and all five agree with their
   pins: `registry_v1_rows` 803 (data rows of
   `data/crosswalks/canonical_sign_registry.csv`);
   `crosswalk_rows` 205 (data rows of
   `data/crosswalks/sign_crosswalk_master.csv`);
   `anchors_sha256` `df0cf620…f569` (SHA-256 of
   `backend/reports/INDUS_FINAL_ANCHORS.json`);
   `total_analyzable_rows` 5,536 and
   `documented_lineage_rows_total` 3,212 (from the intake-pinned
   corpus and row-grades files at their restricted-local paths,
   both files' SHA-256 re-verified against the intake record's
   pins before counting; the full grade vector and the filed
   population cross-checks 3,045 / 5,131 also reproduce). The
   five are now marked sampled on the strength of this
   recomputation, each with its correction sentence in its
   note. Extending the sample beyond the drawn minimum is
   permitted by the sample rule, which sets a floor, not a cap.
2. **Coverage made consistent**: `other_sampled` corrected
   3 → 8 to match the quantities list as corrected;
   `other_checked` stands at 8, now true under the checker's
   definition.
3. **C3 independence cured by substance**: the verifier is now
   the repairing agent, who independently re-read the cited
   evidence for all seven sampled claims (F075-C03, C05, C06,
   C07, C08, C11, C12) and re-derived every checkable number in
   them (both Spec 073 asset digests, row counts and census;
   the documented-lineage population 3,045 / 557 / 550
   recomputed from the pinned corpus and grades files; the
   sole no-published-identity entry, token 999). Each sampled
   claim's note and evidence list are the repairing agent's
   own. All seven verified as registered; no verification
   status was weakened; the six unsampled claims are untouched.

## Verification of the repair

`python3 tools/freeze-gate/check_freeze_gate.py --all` after
the correction (exit 0):

```
C4 PASS: specs/075-depicted-kind-endings-atlas
C4 PASS: specs/076-projected-constraint-corpus-model
C4 PASS: specs/077-signary-triangulation
C4 PASS: specs/078-projected-constraint-bridge-redesign
```

No other spec's records were touched, and no pinned or
recomputed value changed anywhere in the two corrected records.

# Spec 072 — Outcome (Phase-431): FAMILY NOT SUPPORTED

> ## EXECUTED — 2026-10-22 — Phase-431
>
> Executed under the frozen contract
> (freeze digest
> `3925f365bdc452031bb7356f9b357c6d5068da4a835afcfd75b0e9ffa3a69e92`;
> freeze PR #341 merged at `862f56d8`;
> OSF contract registration `tc8ey`,
> filed at the freeze, pending the owner's
> approval act — see
> `osf-spec-registration.md`). The execution
> was commissioned in the same owner tasking
> as the freeze (freeze.md §11). Step 0 ran
> in the frozen order and passed in full;
> the primary run and the mandatory
> sensitivity were scored against the
> freeze-fixed line L = 0.765. **Family
> word: FAMILY NOT SUPPORTED** (primary and
> sensitivity agree; the headline is not
> GRADE-SENSITIVE). This record is internal
> under the Roif gate (spec §7 limit 1;
> claim F072-C14); it is not a publication.

## Headline block (§9, in the frozen order)

1. This corpus is an ICIT-lineage corpus.
   Agreement between it and the program's
   earlier ICIT-lineage layer is consistency
   within one tradition, not independent
   corroboration.
2. Asset F digest
   `ca5fb1b5a52d9ad0c8301174996562cdc024bf4063e6193bef77328b1acc58c3`,
   7 members; dispositions: M048 identified
   as ICIT 243; M050 as 220; M060 as 235;
   M145 as 032; M147 as 033; M047 and M052
   UNIDENTIFIED IN ICIT (excluded from both
   populations' weighting under the
   freeze-ruled disposition; their
   occurrence share in ICIT space cannot be
   measured). Gate-0.3 cross-check: Asset F
   holds none of the claim record's trio
   (72, 64, 70) and, of the Phase-43 six
   (267, 72, 65, 59, 60, 70), only 60, as
   M060. Named divergence: the concordance
   basis's depiction notes for P145, P147
   and P047 differ from Asset F's depiction
   notes for the same Parpola numbers
   (freeze.md §4).
3. Corpus: the Shakti corpus as pinned at
   gate 0.1 (SHA-256 345241b1…), cited
   through the intake record
   `docs/decisions/2026-10-22-shakti-corpus-intake-record.md`.
   Populations: primary = documented-lineage
   rows only; sensitivity = documented +
   undocumented-corroborated rows.
4. Verdict line L = 0.765 — derived at the
   freeze as the 95th percentile
   (nearest-rank, rank 82 of 86) of the
   reference distribution of 86 non-fish
   signs on the primary population
   (reference record:
   `specs/072-fish-family-profiles-redesign/reference-distribution.json`,
   SHA-256
   `55d266b39969caf9ec020a3a941ec451760b05d983da3c6a419903addc73f4f5`).
5. Per-member tables, both populations:
   below and in `reports/phase431_report.md`.
6. FAMILY NOT SUPPORTED: "Tested sign by
   sign across the fish family fixed in
   advance by Asset F (digest ca5fb1b5…),
   in ICIT numbering on the Shakti corpus
   (documented-lineage rows only), members
   carrying only 0.0% of the family's tested
   occurrences pass the freeze-fixed
   ending-follower criterion (line
   L = 0.765). The family's token-weighted
   majority is not followed by text-ending
   behaviour at the rate the freeze-fixed
   line requires, and the claim
   parpola_2010_dravidian_solution_manual_002
   is recorded as not supported as a family
   claim on this corpus. The documented +
   corroborated sensitivity returns the
   same family verdict. This does not
   establish what any fish sign meant or
   was pronounced, and it is not a verdict
   on the Phase-43 or Spec 048 records,
   which stand exactly as recorded."
7. This record is internal under the Roif
   gate; it is not a publication.

## Grade-flip findings (first section, §5.4)

- **M048** (ICIT 243): carried supported
  label flips — primary *not scanned*
  (fraction 0.0000, total 9) → sensitivity
  *not supported* (fraction 0.0000,
  total 12). The member is not tested in
  either population (below the supported
  floor in both); the flip is in the
  carried descriptive label only and moves
  no verdict.
- No other member's class, label, or PASS
  reading changes between the populations,
  and the family word is the same in both:
  the headline carries **no**
  GRADE-SENSITIVE flag (OPEN-072-6).

## Step 0 (frozen order, before any member was scored)

- **Gate 0.1 — Shakti intake assertion:
  PASS.** Corpus and row-grades files
  recompute to the intake pins (345241b1… /
  02394241…); census reproduced exactly
  (5,704 rows; 5,536 analyzable; 3,212 /
  2,087 / 405; 4,904 CISI-keyed; 18,065 true
  tokens; 713 signs; 77 sites).
- **Gate 0.2 — Asset F digest: PASS**
  (ca5fb1b5…, 7 members, Spec 044 §4.2
  rule).
- **Gate 0.3 — Concordance: as frozen.**
  Five members identified (243, 220, 235,
  032, 033); M047 and M052 UNIDENTIFIED IN
  ICIT under DD-072-5. Not CONCORDANCE
  FAILED.
- **Gate 0.4 — Classes and census: PASS.**
  Freeze-stage census re-derived exactly
  (primary totals 9 / 286 / 188 / 334 /
  315; four testable members). Not TOO
  THIN.
- **Gate 0.5 — Verdict line: PASS.**
  L = 0.765 exhibited from the pinned
  reference record (55d266b3…). Not
  INVALID.

## Primary population (documented-lineage rows only)

| Member | ICIT | Total | Bigrams | Ending followers | Fraction | Carried label | PASS (vs L = 0.765) |
|---|---|---|---|---|---|---|---|
| M047 | UNIDENTIFIED IN ICIT | — | — | — | — | — | — |
| M048 | 243 | 9 | 6 | 0 | 0.0000 | not scanned | not tested |
| M050 | 220 | 286 | 249 | 101 | 0.4056 | supported | does not pass |
| M052 | UNIDENTIFIED IN ICIT | — | — | — | — | — | — |
| M060 | 235 | 188 | 103 | 31 | 0.3010 | supported | does not pass |
| M145 | 032 | 334 | 184 | 46 | 0.2500 | supported | does not pass |
| M147 | 033 | 315 | 153 | 13 | 0.0850 | not supported | does not pass |

Tested members carry 1,123 occurrences;
passing members carry 0 (w = 0.0000).
Coverage condition: the one untested
identified member (M048, 9 occurrences)
does not carry more of the identified
family's primary occurrences than the
tested members, so the condition does not
fire. Family word: **FAMILY NOT
SUPPORTED**.

## Sensitivity population (documented + undocumented-corroborated)

| Member | ICIT | Total | Bigrams | Ending followers | Fraction | Carried label | PASS (vs L = 0.765) |
|---|---|---|---|---|---|---|---|
| M047 | UNIDENTIFIED IN ICIT | — | — | — | — | — | — |
| M048 | 243 | 12 | 7 | 0 | 0.0000 | not supported | not tested |
| M050 | 220 | 426 | 357 | 73 | 0.2045 | supported | does not pass |
| M060 | 235 | 240 | 139 | 27 | 0.1942 | supported | does not pass |
| M145 | 032 | 501 | 307 | 63 | 0.2052 | supported | does not pass |
| M147 | 033 | 433 | 254 | 29 | 0.1142 | not supported | does not pass |

Tested members carry 1,600 occurrences;
passing members carry 0 (w = 0.0000).
Family word: **FAMILY NOT SUPPORTED** —
the same word as the primary, so the
headline is not GRADE-SENSITIVE.

## What this does not establish

The verdict is about shared positional
behaviour only: on this corpus, under the
freeze-fixed line drawn from how non-fish
signs behave, the identified fish signs do
not act as a family of text-ending signs.
It establishes nothing about what any fish
sign meant or was pronounced (§7 limits
2–3), nothing about the two UNIDENTIFIED
IN ICIT members (they carry no ICIT
identity to measure), and nothing about
any other corpus or numbering: Spec 048's
closure and the Phase-43 record stand
exactly as recorded, unedited.

## Records

- `reports/phase431_results.json`
  (SHA-256 f0679d90…) and
  `reports/phase431_report.md`
  (SHA-256 d4fa6cb9…) — the script is
  deterministic; a second run reproduced
  both files byte-identically.
- Script:
  `backend/scripts/phase431_fish_family_profiles.py`;
  graph node `IndusPhase431FishFamilyProfiles`
  (`backend/glossa_lab/experiment_graph_phase431.py`,
  registered in
  `backend/glossa_lab/experiment_graph.py`).
- Claim record: dated append
  `spec072_outcome_2026_10_22` on claim
  `parpola_2010_dravidian_solution_manual_002`
  (append-only; no existing field edited).
- LEDGER.md entry of 2026-10-22 (Spec 072
  EXECUTED, Phase-431).
- Foundation check, as measured on the
  execution tree: **40 passed / 0 failed /
  8 warnings** (the eight standing warnings;
  none new from this execution).

---

*AI disclosure: executed by an AI agent (Muse,
via Muse) at the direction of Tristen Pierson,
per constitution §VI.*

# Phase-110 — M222 / 'kur' Adjudication: Dossier Summary (spec 008, Part A)

Full evidence: `reports/phase110_m222_dossier.json` (all quotations
verbatim from the cited in-repo artifacts).

## What Phase-111 actually did

`backend/scripts/phase111_allograph_resolution.py` assigns each
rare sign (freq 1–4) the reading of its nearest confirmed sign by
I/M/T positional-profile L1 distance — **copied verbatim** from the
donor's anchor entry. The recorded run
(`outputs/phase111_allograph_resolution.json`) resolved 220 signs:
**220/220 matched M222, 220/220 at L1 = 0.000, 220/220 inherited
'kur'**. Recomputation with the script's own functions shows why:
every rare sign's profile in the Holdat corpus is
(I=0.000, T=0.000, M=1.000) — all occurrences medial — and M222
(freq 5, the minimum donor frequency) shares that profile. The
match carried **zero discriminating information**; M222 was the
donor by tie-breaking, not by sign-specific affinity. Phase-132
later said the same in the anchors file's own note: the Phase-111
kur assignments were "positional parking spots (all-MEDIAL L1=0),
not genuine phonetic readings."

## The two M222 records

- **'kur' (Phase-87):** anchor-sprint proposal, method
  DEDR_REBUS_EXTENDED, depiction "hook sign", evidence_score 2.0 —
  promoted to MEDIUM (`outputs/phase87_anchor_sprint_120.json`;
  May-2026 backup entry, source `Phase-87 DEDR_REBUS_EXTENDED`).
  This was M222's reading when Phase-111 ran.
- **'min' (standing record):** current entry at MEDIUM, retained by
  Phase-109 Step 1(a) because crosswalk v2.1 records the Parpola
  reading 'min' for M222→P222 (Phase-71 EXTENDED_MAP, "Parpola 1994
  App. B", crosswalk confidence CANDIDATE, single in-repo source —
  quoted in the dossier). Acknowledged thinness: one crosswalk
  attribution plus a staging-era DEDR gloss ("shine / lightning").
  Phase-110 does not re-try M222's own value (spec 008
  Assumptions); it adjudicates the *derived* entries against the
  standing record.

## Verdict

**Contradiction: real** (predicates P1–P4 all true — see dossier).
The 109 values are **pure premise inheritance**: their recorded
bases cite M222='kur', a premise M222's own sourced record
contradicts. **Branch 1 applies, with demotion**: Cohort A (109)
is annotated `premise_superseded` and demoted LOW → CANDIDATE.
The four further CANDIDATE entries carrying a Phase-111 'kur'
basis (M157, M256, M307, M400) join the same disposition with no
tier change: their Phase-252 `upgrade_basis` records claim
allograph status under M427 ('en') or M375 ('taṇ') — competing,
never-adopted derivations of *different* values that do not
support 'kur' (spec 008 addendum; Cohort C is empty). Of the 220
signs Phase-111 resolved, 113 still carry its 'kur' basis today
(3 more are present with later readings; 104 are absent from the
current anchors file after later cleanups).

**AI disclosure:** assembled by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per constitution §VI.

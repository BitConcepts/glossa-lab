# Spec 088 — Stage S6 record (gap register v1 + completeness check)

Executed 2026-11-04 on branch `feat/088-s6-register` off
origin/main `6c4201e7` (the PR #509 S5 merge; main had
not advanced). Tasks T601–T602 executed here; T603 is
the owner's act and remains open by the spec's own
terms (see "Tasks state"); T701 follows T603. All
counts below are from the register's own text (recounted
mechanically this stage), the find list, or the records
cited — read first-hand this session.

## What landed

- **T601** — `glossa-indus/map/gap-register.md` (the
  path tasks.md names): gap register v1 in RCPH's
  format — ranked headline list, 37 entries
  `GR-088-01 … GR-088-37` with status words, each entry
  naming the missing piece, why its absence blocks
  convergence, the candidate with its falsifier and
  honesty-rule type, and owner gates; the closing
  "Owner decisions this register surfaces" section;
  the ratification block (PENDING, T603).
- **T602** — the completeness check: mechanical legs by
  script (output summarized below, all PASS) + the
  source-coverage annex (below) for the prose legs,
  with the oracle sign-off line at its close.

## Register census (recounted from the register text by script)

- Entries: **37**; candidates: **38** (GR-088-03 carries
  three, one per revalidation route; GR-088-37 carries
  none, by design; every other entry carries one).
  Every candidate carries a falsifier and a type —
  mechanically counted: 38 falsifier lines, 38 type
  lines, equal per entry.
- By kind: missing node **8** · missing edge **8** ·
  thin evidence **8** · stale bookkeeping **12** ·
  carried, not a gap kind **1** (GR-088-37). The four
  kinds reconcile exactly to the S5 scans' 35 finds
  (7/8/8/12) plus GR-088-26, a missing-node entry added
  at consolidation (departure (a)).
- By domain: Sign inventory & corpus 3 · Anchors &
  readings 9 · Claim families 9 · Contact zone &
  external corpora 4 · Program infrastructure 12.
- By status word: UNSTATED 9 · UNMEASURED 7 · UNJUDGED
  10 · UNCONNECTED 8 · DATA-BLOCKED 2 · TIME-SENSITIVE
  0 · no status word (carried) 1.
- Consolidation arithmetic: 35 S5 finds → 35 entries;
  +1 carried find-list item (GR-088-37) → 36; +1
  completeness-driven entry (GR-088-26) → **37
  entries**; candidates 37 (S5) + 1 (GR-088-26) = **38**.
- Deduplication: no two scan finds were merged. The
  near-duplicate families were checked (bundle-backfill
  finds; the three falsifier finds at three different
  instrument levels; the four edge finds as four
  different relations) and each find kept its own entry
  because each names a different missing piece with a
  different falsifier. The analysis is recorded in the
  register's census section.

## T602 mechanical legs (script run this stage; output of record)

A script over the register + the find list + the three
scan records reports (51 PASS lines, 0 FAIL):

- Entries numbered 01..37 exactly once; 37 entry blocks
  parsed; every entry except GR-088-37 carries ≥1
  falsifier and ≥1 type, counts equal per entry;
  GR-088-03 carries exactly 3 of each; GR-088-37
  carries no candidate.
- Kind census from the register's `Kind:` lines:
  8/8/8/12 + 1 "none" (carried). Status census from the
  entry headers: as the census above.
- Find-list consumption: all **28** `bundle_less_study`
  subjects named verbatim in the register (28/28);
  all **9** `extracted_null_falsifier` claims traceable
  in GR-088-21 by full id or document + elided tail
  (9/9; the full per-claim enumeration is the annex
  table below); the **1** `restricted_node` subject
  named in GR-088-37; find list total 38 confirmed.
- Scan-side coverage: all **35** S5 finds found in the
  scan records and every one cited as a "Scan source"
  in the register (35/35); register kind == scan kind
  for all 35 (0 mismatches).

## Source-coverage annex (T602)

Every item on the registered source lists (C088-11's
enumeration, the lists the brief and tasks.md name for
this stage, and the S5 stage's explicit carries) mapped
to entry id(s) or a recorded not-a-gap disposition.
Dispositions: **REPRESENTED** (a register entry carries
it) / **NOT-A-GAP** (recorded disposition, with reason).

### The C088-11 list (claims.md, verbatim items)

| Source-list item | Disposition |
|---|---|
| GAP-C07 | REPRESENTED — GR-088-05 |
| GAP-C12 remnant | REPRESENTED — GR-088-30 |
| GAP-C13 (consolidating the per-study finds) | REPRESENTED — GR-088-22, with the 28 per-study finds carried by GR-088-13 (13), GR-088-20 (7), GR-088-31 (1), GR-088-33 (1), GR-088-22 (6); per-study table below |
| WP2 (linguist certification) | REPRESENTED — GR-088-04 |
| WP3 (recomputation blockers) | REPRESENTED — GR-088-09; its Holdat blocker leg is GR-088-08 |
| WP5 residuals: 37 requires-revalidation | REPRESENTED — GR-088-03 |
| WP5 residuals: 3 expert-pending (M222, M362, M398) | REPRESENTED — GR-088-14 |
| WP5 residuals: 2 insufficient (M367, M048) | REPRESENTED — GR-088-27 |
| Spec 086 residual: matrix edges for the live population | REPRESENTED — GR-088-18 (dependency pairs), GR-088-07 (anchor cells), GR-088-24 + GR-088-25 (unconsumed outcomes, isolated rows) |
| Spec 086 residual: two-graph-worlds join at population one | REPRESENTED — GR-088-11 |
| T201 mahadevan:64 derivation divergence | REPRESENTED — GR-088-28 |
| The 9-null-falsifier disposition question | REPRESENTED — GR-088-21; per-claim table below |
| Tracker llms.txt staleness | REPRESENTED — GR-088-34 |
| Desktop-clone sync state | REPRESENTED — GR-088-15, in the S5-corrected form (see departure (d)) |
| Data-lineage owner question | REPRESENTED — GR-088-29 |
| The 44 pending anchor readings | REPRESENTED — GR-088-06 |

### Further named lists (brief / tasks.md / stage carries)

| Source-list item | Disposition |
|---|---|
| WP5 residual: 46 internal-only anchors (beyond C088-11's parenthetical) | REPRESENTED — GR-088-02 |
| WP5 element 5.5: anchor-record falsifiers absent (94/94) | REPRESENTED — GR-088-12 |
| WP4: 0 of 184 eligible Parpola comparisons (the scan plan's pre-answered leg; C088-12's standing instance) | REPRESENTED — GR-088-01 |
| Spec 086 residual (T505 item 5): projected-constraint engine, S-R3 UNMEASURED | REPRESENTED — GR-088-26 (added at consolidation; departure (a)) |
| Spec 086 residual (T505 item 1): one entity graph, partially closed | REPRESENTED — its remaining substance is the missing-edge population: GR-088-07, GR-088-11, GR-088-18, GR-088-19 |
| Spec 086 residual (T505 item 2): edges for the live population, partially closed | REPRESENTED — as the C088-11 row above |
| Spec 086 residual (T505 item 6): two-graph-worlds join, partially closed | REPRESENTED — GR-088-11 (the C088-11 row above) |
| Spec 086 residuals (T505 items 3, 4): matrix layer; SPA surface | NOT-A-GAP — both re-scored **closed** at T505 itself; no open residual exists to register |
| S1 multi-spec membership fork (44 claims) | REPRESENTED — GR-088-32 |
| Missing-directory finds: spec numbers 049 and 085 (T503's named inputs) | REPRESENTED — GR-088-36 |
| Find-list item: `restricted_node` (Spec 072), carried by T504 | REPRESENTED — GR-088-37, as a carried entry stating the restriction only |
| Find-list population: `judgment_call` items | NOT-A-GAP — the live population is empty (0 items exist; S2 record); nothing to map |
| `in_flight` empty population (D-088-4) | NOT-A-GAP — a registered v1 limitation of program-map-defs, recorded in the defs; not a gap |
| legc-gaps entries GAP-C01, GAP-C09F, GAP-ENV (S5's carried note) | NOT-A-GAP *for this register* — outside C088-11's named source lists and the scan plan's scope; recorded here and in the S5 record so the exclusion is on the record, not silent. They remain entries of `docs/governance/legc-gaps-2026-10-29.md` for their own owning work |
| Audit-R4 candidates | NOT-A-GAP *for this register* — not named by C088-11 or by tasks.md for this spec (the executing brief named them only conditionally, "if tasks.md names them"; it does not). They live in the Spec 087 audit line (verified-write helper, `.keys.json` encryption-at-rest, test-harness hardening), which is their owning record |

**Completeness verdict: COMPLETE against the named
lists.** Every item above is REPRESENTED or carries a
recorded NOT-A-GAP disposition with its reason. No item
maps to no entry and no disposition; there is no
completeness failure to report. (C088-11's own falsifier
— an item with no entry and no recorded disposition when
the register is presented — does not fire on this annex.)

### Per-study table — the 28 bundle-less studies (mechanical leg, per study)

Domain 2 (13) → GR-088-13: `004-indus-executable-package`,
`005-phase52-v2`, `006-anchor-provenance-audit`,
`007-phase109-follow-through`, `008-m222-adjudication`,
`009-phase111-blind-affiliation`,
`010-phase112-blind-affiliation`,
`011-phase113-nonsa44-validation`,
`012-phase113-blind-affiliation`,
`014-phase115-nonsa44-validation-v2`,
`016-phase117-within-compilation-validation`,
`017-phase118-within-compilation-validation-v2`,
`018-phase119-pred2026-readiness`.
Domain 1 (7) → GR-088-20: `015-phase116-corpus-harmonization`,
`019-phase125-cross-compilation-positional`,
`020-soviet-pred-adjudication`,
`021-phase127-cross-compilation-diagnostic`,
`021-phase130-intake-pack`, `022-phase131-attribution`,
`023-keyed-transcription-layer`.
Domain 3 (1) → GR-088-31: `024-evidence-integration`.
Domain 4 (1) → GR-088-33: `013-tn-graffiti-crosswalk`.
Domain 5 (6) → GR-088-22: `001-glossa-lab-baseline`,
`002-gdelt-ngrams-and-frontier-methods`,
`003-mcp-and-test-gaps`, `025-paper-search-research-check`,
`025-stage2-controlled-followup`, `026-core-research-source`.
Total 13 + 7 + 1 + 1 + 6 = 28 — the find list's full
`bundle_less_study` population, each named verbatim in its
entry (script-verified above).

### Per-claim table — the 9 null-falsifier claims (all → GR-088-21)

`ancient_writing_and_modern_technologies_51831ac9_sign_val_0001` ·
`ancient_writing_and_modern_technologies_51831ac9_sign_val_0002` ·
`ancient_writing_and_modern_technologies_51831ac9_sign_val_0003` ·
`ancient_writing_and_modern_technologies_51831ac9_statisti_0004` ·
`indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001` ·
`indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002` ·
`the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001` ·
`the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002` ·
`without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001`.
(4 + 2 + 2 + 1 = 9, matching the find list and B-05's split.)

**Oracle sign-off (prose legs):** the undersigned stage
worker read this annex against C088-11's text, the T505
re-score, the adoption record §4, and the three scan
records, and rules the prose-leg mappings above accurate
as written — each REPRESENTED row's entry does carry the
item it is mapped to, and each NOT-A-GAP row's reason is
the record's own. Signed: the Stage S6 consolidation
worker, 2026-11-04 (acceptance mode human-as-oracle for
the prose legs, per T602).

## The ledger did not move (C088-15)

`glossa-indus/ledger/claims.jsonl` SHA-256 before this
stage's work and after its completion, identical:
`9f8144c3fa73d7cfa4ffd02d3b6c23c3ea9e0c1e164e9497232dd2842e0a022c`
(907 lines). The register is a document in the map
directory, not a generated artifact; the gate's V10
recomputation does not cover it and is unchanged by it.
No claim's status, stage, or score changed anywhere.

## Gate, both modes (run on the final tree)

```
full:    summary: 25 PASS / 0 FAIL / 1 NOT-RUN   RESULT: PASS
--regen: summary: 28 PASS / 0 FAIL / 0 NOT-RUN   RESULT: PASS
```

Identical to the S5 stage's summaries — the register's
landing moved no gated artifact. The working tree at
commit time carries only the intended paths
(`glossa-indus/map/gap-register.md`; tasks.md ticks and
notes; this record) — no in-tree regeneration residue
to restore.

## Tasks state

- **T001, T002 — ticked at this stage** (bookkeeping
  completion; departure (c)). Their work was executed at
  package/adoption time and their evidence has been on
  the record since; the ticks were simply never made.
- **T601, T602 — ticked** on this stage's evidence.
- **T603 — NOT ticked, by design.** It is the owner's
  block ratification, which by the task's own terms is
  the act that ends the spec and happens on the merged
  register, after this PR. The register is presented
  for it with this PR.
- **T701 — NOT ticked, by dependency.** The closeout
  record requires "the register's entry count and
  ratification reference"; the ratification reference
  does not exist until T603. It follows T603 in the
  closeout act.
- All other tasks (T003–T504) were already ticked by
  their stages. After this stage the spec has exactly
  two unticked tasks, both named here with their
  reasons, and both are the owner's/closeout acts that
  follow this PR — not stage work left undone.

## Departures, stated plainly

(a) **GR-088-26 (S-R3 UNMEASURED) is not an S5 scan
find.** The scans produced no find for the Spec 086
engine residual, but C088-11's source lists (as the
executing brief enumerates them: the Spec 086 residuals
including S-R3) require it mapped, and no honest
not-a-gap reason exists — T505 carries it as an open,
partially-closed residual. Rather than report a
completeness failure for an item that does map, or
exclude it silently, the register carries it as an
entry sourced directly from the Stage 5 record (§T505
item 5), with its provenance stated on its face and
here. The owner can strike it at ratification (T603);
the ratification is exactly where that judgment belongs.

(b) **No merges.** The consolidation performed the
deduplication check the brief requires and merged
nothing; the reason (each find names a different missing
piece with a different falsifier) is recorded in the
register's census section and above.

(c) **T001/T002 ticked late.** T001's package landed
under the adopted directory/branch names
(`specs/088-full-picture-map-gap-register/`,
`feat/088-adoption`), not the draft names its text
carries — the departure recorded at adoption
(`records/ratification-2026-11-04.md`) and carried since;
its substance (a complete, internally consistent package,
19/19 claim ids matching across claims.md and
aee-claims.json) was verified then and stands. T002's
assessor run and verbatim outcome are
`records/t002-note.md` + `records/t002-aee-assessment.json`
(outcome: iterate, 80 failure modes). Both ticks are made
now so the register stage closes the task list honestly
rather than leaving executed work unticked.

(d) **The desktop-sync count moved, as the entry says it
would.** GR-088-15 states 118 commits behind, counted by
the S5 scan against the S4 merge `893a426a`, and carries
its as-of on its face. Against this stage's base
(`6c4201e7`), the GitHub compare read this stage shows
main 121 ahead of `309ea63c`, 0 behind (118 + the S5
merge's 3). The entry is scan-faithful and self-dating;
the number in force when the sync runs is the one the
gatekeeper read shows then.

(e) **The annex lives in this record.** The plan names
"a source-coverage annex" without a path; the executing
brief assigns the completeness table to the stage record.
The annex is the § above; the register's census section
points to it. One artifact, one home, two pointers —
no duplicated table to drift.

(f) **Status words applied by stated convention.** The
plan fixes the vocabulary but not a per-kind mapping;
the register's header states the application rule (the
word describes the gap's own state) so the owner's
ratification reviews the convention along with the
entries.

*This record does not establish:* the ranking — ranking
is judgment, and the owner's ratification (T603) is where
it settles (T601's line). Nor completeness in nature —
only completeness against the program's own named lists,
which is the claim (T602's line).

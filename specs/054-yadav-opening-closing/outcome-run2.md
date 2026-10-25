# Spec 054 / Phase-438 — Outcome record, RE-EXECUTION (EXECUTED 2026-10-25 — NOT SUPPORTED)

> ## RE-EXECUTED — 2026-10-25
>
> Second execution of Spec 054 under the frozen
> amended contract (freeze digest
> `d85f6ace80e2ae2935d96d4916e51db686f11fb2c4473dc24d1198580012bb57`,
> PR #260 merged at `b40dcfc1`), as
> **Phase-438**, under the owner's execution
> order of 2026-10-25 (15:00 EDT, "Do your
> recommended actions"), after OSF
> registration **8spvf** (approved and public
> since the first execution). Outcome: **NOT
> SUPPORTED** — the amended statement is
> falsified under battery NB-1 by condition
> (2)/(3) of its falsifier, applied under
> precedence §5.5(3): both positional classes
> reappear at less than one half (0 of 8
> opening-strong; 0 of 10 closing-strong), and
> the pooled cross-arm overlap (0) does not
> exceed the label-shuffle null's 95th
> percentile (chance level 1).
>
> The first execution (2026-10-24) closed
> **STRICT CORPUS NOT PINNABLE** at gate G2 on
> the facts then known; its record
> (`outcome.md`, `step0-record.md`) stands
> exactly as executed and is not revised by
> this run. This is a new execution under the
> same freeze, reported as its own outcome —
> the form the first outcome itself foresaw:
> "If the V3 layer is re-acquired and pinned,
> a future execution order under this freeze
> can run the battery; nothing in this record
> pre-judges that run." The layer was not
> re-acquired; it was located, in place, where
> it had been held since 2026-05-14
> (intake-pinned 2026-10-25, PR #393).

## Headline (amendment §9 wording, NOT SUPPORTED form)

"The amended statement is not supported under
battery NB-1 as frozen: a positional class
reappears at less than one half, with the
pooled overlap at or below the label-shuffle
null's 95th percentile. This verdict falsifies
the amended statement only. It does not
falsify Yadav et al. (2010)'s original
statement — the original battery's sets cannot
be exhibited — and it does not move the parent
claim's recorded status."

## What the result means, in plain words

This time the test the programme designed in
October 2023's amendment actually ran. The
strict corpus — the Mahadevan-lineage V3
layer, identified this time beyond argument
(its census reproduces the Phase-43 record's
own numbers exactly, checked two independent
ways) — does have specific text-beginning and
text-ending signs of its own: 8 opening-strong
and 10 closing-strong signs under the frozen
battery. But not one of those 18 signs is
strong in the same class in the Holdat
compilation, through the pinned crosswalk:
most are conflict-paired in the crosswalk
(12 of 18), a few are too thin in Holdat or
unmapped, and one is present and classifiable
there but simply not strong. The pooled
overlap of strong signs across the two
compilations is zero, at or below what the
label-shuffle null produces by chance. Under
the decision procedure frozen before any of
these numbers existed, that is a falsification
of the amended statement — the cross-
compilation half of the Yadav pattern does
not hold under NB-1. The claim's recorded
status is untouched, exactly as the frozen
wordings provide: this verdict is about the
amended statement, not about Yadav et al.'s
original claim, whose sets no surviving
record exhibits.

## What was executed

All five step-0 gates, in the amendment §6
order, then battery NB-1 in both arms and the
§5 decision procedure — by the frozen
instrument
(`backend/scripts/phase438_yadav_opening_closing.py`,
byte-identical to the first execution's;
step-0 record in `step0-record-run2.md`):

- **G1 PASS** — every freeze §2 pin
  recomputed; the freeze digest re-asserted.
- **G2 PASS** — arm 1 identified and pinned:
  the V3 loader's census of the in-place
  Firestore 'indusarrays' file reproduces the
  Phase-43 reference census exactly (3,916
  records / 2,665 dockeys / 3,137 sequences /
  12,494 sign instances); source-file SHA-256
  `073a83aa…` (the PR #393 intake pin); export
  pin `e90fd7ce…`. Corroborated independently
  (Route 2 census tool, gates V1–V4 all pass).
- **G3 PASS** — 2,267 sequences of length
  ≥ 3; 103 classifiable signs.
- **G4 PASS** — arm 2 pinned (Holdat
  downloads file, SHA-256 `62d14d2b…`,
  byte-identical to the VM checkout's copy);
  its census (1,670 / 7,002 / 390) matches the
  first execution's C4 census of the layer;
  36 classifiable signs.
- **G5 PASS** — the full decision computation
  run twice, identical canonical records.

**Arm 1 (strict corpus, Mahadevan numbering):**
3,137 sequences (none of length 1), 12,494
tokens, 393 distinct signs, 103 classifiable.
Opening-strong (8): 95, 103, 150, 204, 205,
210, 267, 391. Closing-strong (10): 1, 12,
15, 60, 176, 190, 211, 254, 328, 342.

**Arm 2 (Holdat layer, its own numbering):**
1,670 sequences, 7,002 tokens, 390 distinct
signs, 36 classifiable. Opening-strong (13):
M008, M013, M016, M019, M022, M045, M052,
M058, M060, M061, M062, M073, M079.
Closing-strong (3): M220, M249, M305.

**Reappearance (primary, DD-054-5
denominators):** opening 0/8 (rate 0.0);
closing 0/10 (rate 0.0). Named not reappeared
— opening: CONFLICT 95, 103, 150, 267, 391;
TOO THIN 204 (N=2 in arm 2), 210 (N=2);
UNMAPPED 205. Closing: CONFLICT 1, 12, 15, 60,
176, 328, 342; TOO THIN 190 (N=5), 254 (N=5);
sign 211 is carried and classifiable in arm 2
but not closing-strong there (no DD-054-5
name attaches). **Sensitivity** (named signs
removed from the denominators): opening 0/0;
closing 0/1 — the verdict follows the
primary, and on this data the sensitivity
agrees with it.

**Pooled overlap:** observed 0; null (999
label permutations, seed 44054, numpy PCG64)
min 0 / median 0 / max 1; chance level
(nearest-rank 95th percentile) 1; observed
does not exceed it.

**Precedence (§5.5):** step (3) — neither
arm-1 set is empty, so (1) does not fire; not
both classes reappear, so (2) does not open;
under (3), a class reappears at less than one
half and the pooled overlap is at or below
the chance level → **NOT SUPPORTED**, firing
condition (2) of the falsifier with condition
(3) also met on its own terms.

Venue: TRISTEN-DESKTOP (WSL); execution tree
a worktree at the first execution's base
`9b5ebaf88736c7fa79550e3e4b050824ff791e25`
(the frozen script's embedded date/order
strings are its own unmodified text; the
actual order is the owner's of 2026-10-25,
above). Anchors asserted byte-identical
before and after (`df0cf620…` at both
readings).

## The outcome append to the claim's record

As the draft's §9 deliverables prescribe, the
outcome was appended to the record of
`yadav_2009_arxiv_manual_002` as a dated entry
(key `spec054_outcome_append_2026_10_25`,
carrying the §9 headline wording with this
run's framing: the re-execution, its order,
and its gate passage). The store's SHA-256
moved from
`21009b4aabc2b22d83c10c157b9f2f4c5829070650046ec46d3d4f5271958636`
(the first execution's post-append state) to
`7151cb70b6910c4b2c1799ea732932999656697c8e18f6731e35dde6e71c8a49`
by exactly that entry. Durability was proven in a
scratch tree at the amendment §7 standard:
regeneration through the fixed generator
preserves the appended entry verbatim, the
falsification condition survives verbatim,
and the claim's status (`strongly_supported`)
and stage (`explained`) are untouched.

## What this does not establish

- Nothing about Yadav et al. (2010)'s
  original Phase-43 statement, whose sets no
  surviving record exhibits (adjudication
  §7.2). The falsified statement is the
  amended one, under NB-1 as frozen — no
  wider reading is licensed by the §9
  wording, and none is made here.
- Nothing about whether the script encodes
  language, and nothing about any sign's
  meaning or reading (spec §7 limits).
- No movement of the parent claim's recorded
  status in either direction — by the
  amendment's §9 design, no outcome of this
  run can move it.
- Nothing about the first execution: its
  STRICT CORPUS NOT PINNABLE verdict was the
  frozen closure for the facts then known,
  and it stands. This run's different passage
  through the same gates rests on a fact that
  changed after it closed — the layer's
  location, established 2026-10-25 — not on
  any defect in the first run's record.
- This spec's closing measure is
  "closing-strong under NB-1", a different
  quantity from Spec 045's "Holdat
  final-position concentration" (amendment
  §10); nothing here re-opens Spec 045.

## Records

- `reports/phase438_results_run2.json` — the
  full machine record of this execution
  (gates, the identification with all
  censuses, both arms' per-sign tables, the
  decision record), as written by the frozen
  instrument at the venue, unedited.
- `reports/phase438_report_run2.md` — the
  instrument's report, unedited (its header's
  date/order strings are the frozen
  instrument's own; the actual order is
  recorded above).
- `specs/054-yadav-opening-closing/step0-record-run2.md`
  — this execution's step-0 record.
- The dated outcome append on
  `yadav_2009_arxiv_manual_002`'s record
  (above).
- The first execution's records
  (`outcome.md`, `step0-record.md`,
  `reports/phase438_results.json`,
  `reports/phase438_report.md`) are untouched.

## Landing record

Appended at merge (append-only): PR number,
merge commit, CI conclusions, the claim
store's post-append hash, and the foundation
check as measured on the merged tree.

---

*AI disclosure: executed by an AI agent (Muse
Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*

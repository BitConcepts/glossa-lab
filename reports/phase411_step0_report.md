# Phase-411 — Spec 045 step-0 report

Claim: `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001` — standing IN QUESTION,
partially supported for position only, exactly as
recorded. Execution date: 2026-10-21. Freeze digest:
`5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`. OSF registration 4mt9k
(approved and public).

## Outcome: INVALID

Frozen wording (spec section 5.5, INVALID form):

> Spec 045 stopped before any model quantity: gate 0.2 (positional reproduction) failed — the pinned corpus carries 3,463 inscriptions of length >= 3 against the recorded 2,267; the 40/61/20 strong-sign classes are exhibited by no record of record (the Phase-43 record exhibits 10 of its 20 terminal-strong signs and no initial or medial member list, and states no position rule, count floor, threshold, or profiled-set rule); and the corpus the recorded quantities belong to (the Firestore V3 corpus, 3,137 sequences) is absent from the tree. No verdict is recorded; the claim stands as recorded.

## Gates, in frozen order

- **Gate 0.1 — Input integrity: PASS**
  - `glossa-indus/analysis/positional/hunt_tripartite_test.json` — match (0e546962c1b72b929c87d4ce40c97633e8e3e340737f32f5dd3eae9f04759e48)
  - `outputs/phase43_all.json` — match (78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4)
  - `backend/glossa_lab/data/yajnadevam_inscriptions.csv` — match (c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98)
  - `data/crosswalks/sign_crosswalk_master.csv` — match (4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf)
  - `backend/reports/INDUS_FINAL_ANCHORS.json` — match (df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569)
- **Gate 0.2 — Positional reproduction: FAIL**
  - Recorded: formula 805/2267; classes 40/61/20.
  - Pinned corpus census: 5679 records; 3463 inscriptions of length >= 3 (recorded: 2,267).
  - Phase-43 record exhibits 10 of 20 terminal-strong signs and no initial or medial member list; its corpus is the Firestore 'indusarrays' source (3,137 sequences), whose data file is absent from the tree.
- **Gate 0.3 — : NOT REACHED**
- **Gate 0.4 — : NOT REACHED**

## What was not done

Asset A was not built (no sign was classified); no
model was fitted; no join was made; gates 0.3 and
0.4 were not reached. No gloss is established by
this record: it states only that the frozen step-0
reproduction gate failed on the values above, and
the claim stands as recorded. Spec 037's census
caution (object-type labels diverging between
compilations in 49% of matched cases) is restated
here as it travels with every statement under this
spec; Asset A's construction was its designed
answer, and that construction was never reached.

Anchors asserted byte-identical before and after:
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` at both readings.

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution section VI.*

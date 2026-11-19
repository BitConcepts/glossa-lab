# DEDR dataset acceptance and placement record — 2026-11-19

**Status: ACCEPTED and PLACED. The restored DEDR tree is the
program's held DEDR dataset as of 2026-11-19. No study leg was
re-run by this act; no recorded not_run outcome is changed.**

This record closes §6 of
`records/dedr-restore-record-2026-11-19.md` (PR #593, merged as
`558430a010d33e342812d8c1ca9e498c3eb0a104`), whose two remaining
steps were the acceptance act and placement into the live origin's
tree.

## 1. The acceptance act

On 2026-11-19 the owner accepted the restored tree as the
program's held DEDR dataset, in chat, in these words: "Accept the
restored DEDR and place it". The dataset accepted is the tree
restored at the recorded pin
`d5050e5a9671012df416e9c474c75aba41c07f8c` of upstream
`moli-mandala/data`, byte-identical to the pinned tree per file,
proven by git blob SHA-1 against Software Heritage's archived
content ids for the same revision (directory
`ce6541aa7b96c31d0ea88e4a116e698e5fc187b9`), as recorded in the
restoration record and its machine verification file
(`records/dedr-restore-verification-2026-11-19.json`).

## 2. Placement into the live origin's tree

Placement was executed the same day, after acceptance, in the
live origin checkout `~/glossa-lab` on the mini-server, by the
merged restore tool (`backend/scripts/restore_jambu_dedr.py`,
copied into the origin for the run and removed afterward; the
origin checkout itself was not advanced or otherwise modified).
The script verified every file's blob SHA-1 against the pinned
table before copying and reported: "placed 15 files at pin
d5050e5a9671012df416e9c474c75aba41c07f8c; all hashes verified".

The placed surface is the consumed surface only: all of
`data/dedr/` (9 files), all of `cldf/` (5 files), and the upstream
`README.md` — 15 files, 46 MB on disk, at
`reports/jambu-dedr/` in the origin tree. The dataset bytes are
placed, never committed: the gitlink remains the tree's only
entry for `reports/jambu-dedr` (`160000 d5050e5a…`, unchanged).
The origin's `git status` after placement is identical to its
status before placement (the only modified paths are the
backend's own runtime outputs, which pre-date the placement);
the placement added no tracked change.

## 3. Verification from the origin tree

Machine record: `records/dedr-acceptance-verification-2026-11-19.json`
(the restore script's `--verify` output, run against the placed
tree in the live origin checkout).

- **15/15 files present; every file's size and git blob SHA-1
  match the pinned table; none missing.** Headline file:
  `dedr_new.csv` SHA-256 check passes
  (`fbcc2b2d47c9be24338d846319de2b2c5a2ad4f45451274e3223bc63bc60cae0`).
- **Coverage, from the origin tree:** `dedr_new.csv` holds
  85,374 rows, uniformly 9 columns; 5,623 distinct entry params;
  89 language tags.
- **The program's own consumers execute from the origin tree:**
  battery v2's `load_dedr` returns **85,251 entries**, and
  `test_dedr_v2` passes its probes by exact match — kalam ×5,
  nal ×18, kai ×116, tiru ×3, ko ×93, mutalai ×1. The CLDF
  loader's summary over the placed `cldf/` reads 290,071 forms,
  615 languages, 23,131 parameters.
- **The serving backend was not touched:** no service was
  restarted, and after placement
  `GET 127.0.0.1:8001/api/v1/health` returned its exact six-key
  payload with status healthy (uptime continuous through the
  placement).

## 4. What this act does not do

- **T302's recorded outcomes stand exactly as filed**, including
  `dedr = not_run` for all 28 signs of run
  `study-20261117T103816Z-a25969` (reason at filing:
  `dedr_dataset_not_held—not_run`). The reason no longer holds —
  the dataset is now held — but the recorded outcome is a fact
  about that run, not a standing to be edited.
- **Any battery re-run** over the T302 population (or any other)
  is a new run under a new commission. Nothing in this act
  commissions one.
- No claim in the spec's claim set is created, discharged, or
  amended by this record; acceptance of a dataset is a program
  act, not a claim verdict.

Standing position unchanged: the Indus script is not deciphered;
a held dictionary is an input, not a result.

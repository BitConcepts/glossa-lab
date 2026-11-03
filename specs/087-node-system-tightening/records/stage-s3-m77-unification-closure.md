# Spec 087 S3 — M77 corpus-pipeline unification: CLOSURE

Closes the unification thread opened by the Step 0 divergence record
(`stage-s3-conversions.md`, section "M77 corpus-pipeline unification —
Step 0 divergence check: STOP", landed by PR #492, merge `50e91a63`).

## The question Step 0 left open

Two M77 corpus pipelines existed on paper. Pipeline A
(`backend/glossa_lab/data/indus_m77.py` over
`reports/mahadevan_corpus_flat.txt`) serves ~45 consumers. Pipeline B
(`M77InscriptionLoader` over `reports/mahadevan_texts_decoded.json`,
with a Holdat CSV fallback) serves the loader node in 3 live graphs.
Step 0 proved structural divergence and that B's primary corpus was
absent from every VM tree; equivalence was unprovable until the
desktop was checked. Three questions went to the owner: (1) does the
decoded JSON exist on the live desktop; (2) which artifact is
canonical; (3) is the silent Holdat fallback kept.

## Owner decisions on record

- Q3 answered 2026-11-03 (owner, 03:04 EST): the silent Holdat
  fallback is RETIRED. Executed by PR #493 (merge `16f61755`): the
  generic loader engine gained explicit source selection; Holdat is
  reachable only as `source='holdat'`; absence returns the explicit
  absent-corpus error. Record:
  `stage-s3-m77-fallback-retirement.md`.
- Q1 + Q2 block accepted 2026-11-03 (owner, 08:28 EST): Pipeline A
  on main is canonical; Pipeline B is recorded corpus-absent;
  desktop-unique content, if any exists, is imported by record
  before the desktop variant is treated as superseded; the desktop
  clone's sync to main belongs to the Spec 083 sequence, not to
  this thread.

## Q1 — the decoded JSON exists nowhere

Desktop check job `20261103T075820Z-glossa-m77-desktop-check-2026-11-03-bf3f64`
(run `41614470654`, success; verdicts read from the gatekeeper queue
record): `reports\mahadevan_texts_decoded.json` ABSENT on the live
desktop clone, as is the `backend\reports\` copy and the generator
script at its checked path. The four Holdat-named files on the
desktop are analysis CSVs under `data\raw\other_sites`, not an
inscription corpus at the loader's path.

Repo-side (parent-verified): `git log --all` for both decoded-JSON
paths is EMPTY. The file was never committed; it was always a
generated working-tree artifact. Its generator's inputs are also
absent from every tree checked. On current evidence Pipeline B's
corpus is not reconstructible from materials on either machine.

**Pipeline B is therefore recorded CORPUS-ABSENT.** The loader node
serves the explicit absent-corpus error; nothing substitutes
silently (post-#493 behaviour). This record does not adjudicate
historical runs: studies that executed Pipeline B while its file
existed locally (e.g. the Phase-19 dual-corpus work) stand as
recorded at their own freezes.

## Q2 — the A-variant divergence was line endings only

The desktop's flat file hashed differently from every VM copy
(desktop 23,111 B, sha256 `2789caf0…`; VM/main 21,443 B, sha256
`878fd223…`), and its clone sits at a local, never-pushed HEAD
(`309ea63c`, 2026-10-31; gitstate job
`20261103T105356Z-glossa-m77-desktop-gitstate-2026-11-03-190746`,
run `41640679375`) against which both M77 paths are clean, not
ignored. On origin/main, both files are tracked with the VM bytes
and their visible history begins at PR #486's merge (`415a157`):
they entered the committed record on 2026-11-01/02, having lived
before that as untracked working files seeded from one local
source.

The desktop variant was grabbed (job
`20261103T132459Z-glossa-m77-flat-grab-2026-11-03-a0fd5f`, run
`41657775954`; artifact zip sha256 `0ac490f2…`; grabbed file
sha256 `2789caf0…`, matching the desktop check exactly) and diffed
against main's file:

- 1,669 lines on both sides; 5,361 tokens on both sides; 64
  distinct signs on both sides.
- Positional differing lines: **0**.
- The entire 1,668-byte delta is exactly 1,668 CRLF line endings
  (the desktop file was written on Windows; the final line is
  unterminated on both sides). After CRLF→LF normalization the
  desktop variant is **byte-identical** to main's canonical file
  (normalized sha256 `878fd223…`) — the canonicalize-before-you-hash
  case of the Winning Combination pattern note, Amendment 2.

**There is no desktop-unique content.** The accepted decision's
import condition is satisfied vacuously: the desktop variant stands
superseded with nothing lost, and Pipeline A's committed artifacts
(`reports/mahadevan_corpus_flat.txt` sha256 `878fd223…`,
`backend/glossa_lab/data/indus_m77.py` sha256 `47615e71…`) are the
single corpus of record.

One scoped residual: the loader file's desktop delta (102 bytes:
3,713 vs 3,611) was not separately grabbed. It is consistent with
the same line-ending mechanism and the file is clean against the
desktop's local HEAD; the desktop clone's eventual sync to main
will surface any real content difference as a git diff before it
can take effect, and that sync is owned by the Spec 083 sequence.

## Cleanup determinations (the three desktop runs)

Desktop check, gitstate check: read-only; nothing created, changed,
or removed on the desktop. Grab: one file copied out; nothing
changed on the desktop. All three job scripts and this record are
the retained evidence.

## What this does not establish

- Nothing about the correctness of either pipeline's readings; the
  unification question was identity and custody of the corpus, and
  only that is closed.
- The desktop clone's broader staleness (HEAD at 2026-10-31) is an
  operational item for the Spec 083 sequence; this record
  adjudicates only the M77 paths.

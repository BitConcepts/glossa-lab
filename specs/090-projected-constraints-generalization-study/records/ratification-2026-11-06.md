# Ratification + adoption record — Spec 090 Stage G3 (ratified 2026-11-06; adoption executed 2026-11-10)

Scope of this record: the Stage G3 adoption runs only (task
T401). The package is recorded, the stage amendment is landed,
the stage claims are ledgered, and the generated layers are
regenerated. No freeze was made (T402 not started), no profile
was computed over H1 (T403 not started), and no stage outcome
exists. The draft PR #523 is not closed by this landing; the
merge of the adoption PR is the parent seat's act.

## The ratification act

Spec 090's G3 stage (the computed separator) was commissioned
by the owner on 2026-11-05 ("Commission G3 now") and drafted
the same day as `records/g3-package-draft.md`, carried on
draft PR #523 (branch `docs/090-g3-stage-draft`, head
`7ed74b53`). The owner ratified the package as a block on
2026-11-06, decisions D-090-5..10 adopted as recommended:

- **D-090-5 — G3's home**: a stage amendment to Spec 090,
  superseding spec.md's G3 non-goal line for this stage only;
  C090-15 continues to bar G4/G5. *Adopted as recommended.*
- **D-090-6 — The separator definition**: P as defined in the
  package's §2, five components, coarsening limit named.
  *Adopted as defined.*
- **D-090-7 — The held-out set**: H1 as the sole held-out set
  and bar arm; the §3.2/§3.3 exclusions, Laursen among them.
  *Adopted.*
- **D-090-8 — The bar and outcome vocabulary**: §5's three
  conditions; §6's outcomes including NOT YET and CANNOT BE
  ADMINISTERED as first-class, with no repair administration
  under this package. *Adopted.*
- **D-090-9 — Ledger intake**: C090-17..24 appended at
  adoption through the sanctioned intake, the stage's only
  ledger diff. *Adopted.*
- **D-090-10 — The report**: the outcome reported to the VEXA
  chat either way. *Adopted.*

## AEE at adoption (T401, assessment clause)

Verification ran under the pinned AEE in the CI-faithful venv
from the spec directory. Two readings, both recorded:

- The stage bundle as appended (`claims.json`, 8 claims):
  `aee validate` → `valid: 8 claim(s)`; `aee assess
  --no-ledger` → exit 1, **outcome: iterate**, recorded at
  `records/g3-stage-bundle-aee-assessment.json`. Verbatim
  summary: "Assessed 8 claim(s); found 34 failure mode(s); 8
  claim(s) below the 0.70 confidence threshold. Shared
  evidence: 1 supporting source(s) shared across 8 of 8
  claim(s); the same evidence set supports multiple claims
  (FR-2.8, reporting only, no outcome effect in this phase).
  Draft cap: 8 draft claim(s) capped at
  gather_evidence/iterate (FR-2.3). Stage cap: 8 claim(s)
  below stage 'explained'; the outcome cannot be 'pass'
  (Spec 004 R1.4). Not understood: 16 residual unknown(s)
  are recorded on this assessment (Spec 004 R5.2). Lane 1
  (machine verification): outcome iterate; 0 claim(s) at or
  above the 0.70 threshold, 8 below. Lane 2 (human
  acceptance): stages by effective stage: created 8. Lane-2
  lag: 8 claim(s) below explained."
- The spec's full amended claim set (24 claims: the frozen
  `aee-claims.json` set plus the stage bundle; the assessed
  records are the union of the two bundle files):
  `aee validate` → `valid: 24 claim(s)`; `aee assess
  --no-ledger` → exit 1, **outcome: iterate**, 105 failure
  modes, recorded at
  `records/g3-adoption-aee-assessment.json`. The reading is
  exactly the T002 reading of the original 16 (71 failure
  modes) plus the stage bundle's 34 — no original claim's
  reading moved.

The iterate outcome is the normal draft-bundle reading (all
24 claims at stage `created`, status `draft`; the draft cap
and stage cap bind by construction). No claim's status,
stage, or score was changed by the assessment.

## The stage-amendment landing

- `records/g3-package-draft.md` lands byte-identical from
  the draft branch (git blob `701ef377`, SHA-256
  `442b5119…`); its header still says DRAFT — the
  ratification act is this record, beside it, in the pattern
  of the ratification record of 2026-11-04.
- `spec.md`: the Status line now records Stages 0–3 complete
  and the G3 stage adopted under the 2026-11-06 block
  ratification; the G3/G4/G5 non-goal bullet carries the
  D-090-5 stage-amendment annotation (superseded for G3
  only; G4 and G5 remain unattempted and barred); a "Stage
  amendment — G3" section after Decisions records the stage,
  its bar, and decisions D-090-5..10. No original
  requirement text was rewritten.
- `claims.md` gains the "Stage G3" section: C090-17..24
  reproduced from the package's §7 without substantive
  change (verified by a normalization round-trip against
  the package text for all eight claims: heading, body,
  falsifier, does-not-establish).
- C090-15's normative text stands as ledgered. D-090-5
  permits amending its "unattempted" statement "if and when
  the stage runs"; T401 is the adoption, not the run, so
  the amendment is recorded in spec.md and in this record,
  and the claim text is untouched.
- `tasks.md` gains Stage 4 with T401..T405 reproduced from
  the package's §8; T401 is ticked by this landing, T402
  (freeze), T403 (computation), T404 (audit and outcome)
  and T405 (report to the VEXA chat) stand open and
  unstarted.
- Program-map assignment: none was needed or made — Spec
  090 is an existing study in the program map (this is one
  of the points where a stage adoption of an existing spec
  differs mechanically from Spec 091's adoption of a new
  spec).

### Deviation 1 — the stage bundle is carried in `claims.json`, not appended to `aee-claims.json`

The package's §8 names `aee-claims.json` as the bundle the
stage's claims join. Execution found a machinery invariant
that forbids the literal reading: every state-loading route
(the settling engine, the matrix builder, the map builder)
verifies each ledger entry's recorded source hashes against
the files on disk, first recorded hash per path governing —
one source path admits exactly one recorded hash, forever,
because the ledger is append-only. Appending C090-17..24 to
`aee-claims.json` in place gives that path two recorded
hashes (the 2026-11-04 lines pin `9962c0bf…`; the grown
file hashes `c93d2e87…`), and every route then refuses:
`tools/ledger/run_settling.py verify-canonicals` and
`tools/ledger/generate_matrix.py` both refused on the
in-place tree with the old-hash mismatch, before any other
check. The first landing built that way was reset before
any push and redone in the machinery's own two-file shape:
the sanctioned intake (Spec 086 route 2) reads `claims.json`
and `aee-claims.json` from the same spec directory — 55 spec
directories in this repository already carry both files —
so the stage's eight claims are carried in a new
`claims.json` stage bundle (SHA-256 `9079c404…`), and
`aee-claims.json` is byte-untouched (SHA-256 `9962c0bf…`,
the hash the C090-1..16 ledger lines record). The claims'
ids, texts, falsifiers and does-not-establish lines are
exactly the package §7 set under either shape; the
one-hash-per-path invariant is restored (zero multi-hash
source paths in the grown ledger). Nothing was forced: the
intake counts below are the counts the machinery produced
under this shape, and they are the expected counts.

## The claims intake (T401, intake clause; decision D-090-9)

The pre-append gate check ran first, over the landed tree:
**29 PASS / 0 FAIL / 1 NOT-RUN** (full mode) and **32 PASS /
0 FAIL / 0 NOT-RUN** (`--regen`) — the standing profile,
because the spec already exists in every layer (contrast
Spec 091's pre-append failures, which named its unassigned
new directory; no assignment step exists here).

Intake, via the sanctioned route:

```
python3 tools/ledger/import_bundle.py \
  --spec specs/090-projected-constraints-generalization-study \
  --date 2026-11-06
→ 8 appended, 16 already canonical, 24 propositions
```

- `glossa-indus/ledger/claims.jsonl`: **973 → 981 lines**;
  SHA-256 `6eada964c585a859db34e1a0e8c1da892baf0012db90e3742829bb318905a0b5`
  → `85c3b4c7e52e154cdc94c1f882bd609a459994c19ea821d8b20bae3934fb387b`;
  appended 8-line block SHA-256
  `6a45b4a3bd092bf83f3347ea7ec72c896eab67d32888ffc9d33f12e8460cf534`;
  append-only verified byte-wise (the first 973 lines hash
  to the pre-append file).
- Program claims: **942 → 950** (bundle population 919 →
  927; extracted 23, unchanged). The eight appended entries
  are dated 2026-11-06 (the ratification date, per the
  C090/C093 convention) and cite the stage bundle
  `claims.json` at SHA-256 `9079c404…` as source of record.
  The 16 already-canonical claims were skipped by
  proposition fingerprint (D-B merge-never-delete); their
  ledger lines keep the original bundle hash, as designed.
- `tools/ledger/validate_ledger.py`: **PASS** — 950 claim
  entries; falsifier coverage 941/950 (was 933/942; the
  eight new entries all carry falsifiers);
  does_not_establish coverage 755/950 (count unchanged:
  like the spec's original 16 and Spec 091's 15, the
  script-normalized bundle entries carry their
  does-not-establish inside the statement text rather than
  the ledger's separate field — an observed property of
  the normalization, recorded here so the flat count is
  not misread).

## Settling chain refresh

In the standing precedent order, over the grown build:

- `run_settling.py verify-canonicals` **before any pin
  moved: 6/6** registered canonicals reproduce (the five
  scenarios and the one comparison), field-for-field.
- Both T405 scenarios were re-executed under run-defs v2
  with the registered scenario ids and the standing
  286-sign full-frame scope: incumbent
  `settling-20261110T145806Z-63c6de` (record SHA-256
  `a160328e…`) and full-register
  `settling-20261110T145813Z-5f57c9` (record SHA-256
  `7d1e4299…`). Both result blocks are **byte-equal** to
  the superseded generation's.
- The Stage 4 dual-run comparison was re-filed from the
  new pair (`specs/086-winning-combination-adoption/records/stage-4-dual-run-comparison.json`,
  SHA-256 `20a9e109…`): identical to the previous filing
  except the ledger pin (973 → 981 lines).
- The assignment sets were re-materialized unchanged (run
  `settling-20261110T145818Z-4fe3eb`; incumbent 94,
  full-register 286, H003 out of frame).
- `glossa-indus/ledger/settling-canonical.json`:
  `provenance.ledger` refreshed to the grown build
  (`85c3b4c7…`, 981 lines) and the refresh recorded as
  `re_derivations[7]`, naming the final run ids. Semantics
  glossa-settle-1 unchanged; expectations_changed false.

## Store departures and index completion

The superseded pair departed the run store under the map
builder's D-D rule (a run pinned to a different ledger
build cannot be carried), preserved in git history:
incumbent record `settling-20261110T140239Z-7b9862.json`
(git blob `d4ef5df1`, blob SHA-256 `af5eb0e6…`) and
full-register record `settling-20261110T140240Z-b53030.json`
(git blob `64b3d5fc`, blob SHA-256 `88125473…`), both at the
pre-refresh tree `e6bd4fd2`, superseded by the refresh
commit. `tools/ledger/build_legacy_index.py` appended the
`re_derivations[7]` event entry (its enumeration skips
post-spec records by name, as before); the two departure
acts for the departed pair were appended through
`run_records.departure_act` + `append_act` with
git-history-derived fields under the builder's
DEPARTURE_REF, the run-defs v2 §7.1 accounting the gate's
V11 leg accepts (it passes). Folded census after
completion: **31 entries**.

## Regeneration over the grown ledger

The generated layers were regenerated with the plain
generators in dependency order (the Spec 093 Appendix A
procedure): `generate_matrix.py`, `generate_map.py`,
`tools/map/generate_program_map.py`. (The gated publish
route was not attempted on this adoption; the plain route
is the recorded precedent where a refresh spans the
settling store, and no gate leg was weakened by the
choice — the standalone gate below reads the shipped tree
in both modes.)

- `glossa-indus/matrix/matrix.json`: SHA-256 `6075231c…`
  (788,621 bytes); `matrix.md` `ef27050c…`.
- `glossa-indus/map/map-data.json`: SHA-256 `062227ce…`
  (settling runs carried: 2).
- `glossa-indus/map/program-map.json`: SHA-256 `b08e4e45…`
  — census **950 claims · 93 studies · 28 unjudged**;
  `program-map-finds.json` `6ace0a06…`; `program-map.html`
  `7565e5d2…`.

## Gate on the shipped tree

`tools/ledger/check_ledger_gate.py`, glossa-ci venv, over
the tree this PR ships (extracted_claims restored between
modes and before committing):

- Pre-append (landed stage amendment, before intake):
  full **29 PASS / 0 FAIL / 1 NOT-RUN**; `--regen`
  **32 PASS / 0 FAIL / 0 NOT-RUN**.
- Final, shipped tree: full **29 PASS / 0 FAIL / 1
  NOT-RUN — PASS**; `--regen` **32 PASS / 0 FAIL / 0
  NOT-RUN — PASS**.

## Test maintenance — census re-pins

Every moved literal was re-set from the regenerated
artifacts' actuals; no check was weakened, skipped, or
deleted:

- `backend/tests/test_program_map_conformance.py`:
  `PIN_CLAIMS` 942 → 950; `PIN_CLAIMS_BY_POPULATION`
  bundle 919 → 927; `PIN_CLAIMS_BY_CLASS` open 933 → 941;
  `PIN_FALSIFIER_PRESENT` 933 → 941; census-of-record
  comment updated. (`PIN_STUDIES` 93, `PIN_UNJUDGED` 28,
  `PIN_NULL_FALSIFIER_EXTRACTED` 9, `PIN_MULTI_SPEC` 44
  unchanged — no new study.)
- `backend/tests/test_spec086_map.py`: claims_total 942
  → 950 (three sites); draft 918 → 926; ledger_lines 973
  → 981; map elements 1586 → 1594; supports 1458 → 1466
  (two sites); loads 942 → 950; falsifier census 933/942
  → 941/950; AEE state census without_state/total 942 →
  950; claims untouched by any run 941 → 949;
  `claim_population.no_stage_recorded` 16 → 24 (the stage
  claims record no ledger stage, exactly as the spec's
  original 16 under the same bundle normalization —
  re-pinned from the artifact, not adjusted to fit).
- `backend/tests/test_spec086_ledger_gate.py`: "1465
  matrix cells" → "1473 matrix cells"; "942 claims
  counted across 8 statuses" → 950; "1465 map edges by
  relation" → 1473; "supports 1458" → "supports 1466";
  "942 claim nodes" → "950 claim nodes".
- `frontend/e2e/system-graph.spec.ts`: "942 claims in
  the ledger" → "950 claims in the ledger".

The four pin-bearing files (the three backend files above
plus `test_spec086_ledger_migration.py`) read **96 passed /
1 failed** locally (glossa-ci venv, basetemp on the
workspace disk); `test_p2_reconciliation` passes — the
bundle population fingerprint-matches the ledger again, as
the intake restores. The one failure is
`test_spec086_map.py::test_builder_refuses_a_run_pinned_to_another_build`,
the documented pre-existing VM glob-order failure (it
fails on pristine main on this VM; CI is authoritative).

## Deviations

1. **Stage bundle file** (`claims.json`, not
   `aee-claims.json`): see "Deviation 1" above — forced by
   the one-recorded-hash-per-source-path invariant,
   demonstrated by two machinery refusals on the first
   (unpushed, reset) landing; the two-file shape is the
   importer's own route-2 pattern with 55 in-repo
   precedents.
2. **No program-map assignment step**: the study already
   stands in the program map; a stage adoption of an
   existing spec has no T004a analogue.
3. **Gate log files**: the final gate runs' output was
   read from the runtime-captured process output after
   shell-redirected log writes failed silently under the
   VM's intermittent write-denial wave (empty files, exit
   120); the gate's own verdict lines are the record, and
   both modes were re-run clean to obtain them.

## This does not establish

Anything beyond the adoption landing: no freeze was
computed, no profile was computed over H1, no separator was
run against any case, and no claim's status, stage, or
score changed. The stage stands adopted with its claims
ledgered (C090-23's boundary kept: this adoption append is
the stage's only ledger diff to date). The standing
position is unchanged — the Indus script is not
deciphered.

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.

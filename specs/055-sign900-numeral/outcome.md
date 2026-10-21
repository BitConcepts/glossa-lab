# Spec 055 / Phase-414 — Outcome record (EXECUTED 2026-10-21 — NOT NUMERAL-LIKE)

> ## EXECUTED — 2026-10-21
>
> Executed under the frozen Spec 055 contract
> (freeze digest
> `42ef82829ade894918b0bf946ac44354224d689202e2f7bf00eb747821bdedfc`,
> PR #252 merged at `e3399961`), as **Phase-414**,
> in Wave 3 Group 2 of the runnable-experiments
> campaign (plan approved AS WRITTEN on
> 2026-10-21). The execution gate was satisfied
> before the run: OSF registration **tbyqg** is
> APPROVED + PUBLIC (parent-verified). Outcome:
> **NOT NUMERAL-LIKE** — stage 1 identified the
> sign, gate 0.4 passed, and at the behaviour
> stage the identified sign's behaviour is
> indistinguishable from frequency-matched
> ordinary signs' on the frozen measures
> (numeral-side 1, control-side 3). The
> identification itself stands as recovered.

## Headline (spec §5.4 wording, NOT NUMERAL-LIKE form)

"The sign that Fuls's paper numbers 900, identified in Spec
055's recovery record as P154, does not behave as a numeral sign
behaves in the pinned strict corpus: on 3 of the three frozen
measures it sits inside the range of frequency-matched ordinary
signs (per-measure table, §3 below). The numeral reading the
fragment carries is contradicted at the behaviour stage. The
identification itself stands as recovered; what fails is the
behaviour the reading predicts."

Claim:
`ancient_writing_and_modern_technologies_51831ac9_sign_val_0001`
— the fragment is converted from a pointer into an identified
claim (the sign is registry row P154, Mahadevan 287, in the
extended Wells (2011, 2015) list), and its numeral reading is
contradicted at the behaviour stage on this layer, under these
measures.

This result is about how one identified sign behaves in
recorded data. It is not evidence of what any sign means, and
it does not establish the value six.

Design D-16 does not join this campaign even though this
recovery is the act that would unblock it; D-16 waits for its
own planning gate (campaign decision E-7).

## 1. What was executed

Both stages, in the frozen order, under the graph-first
build (H15/H23): experiment script
`backend/scripts/phase414_sign900_numeral.py`; graph module
`backend/glossa_lab/experiment_graph_phase414.py`
(node `IndusPhase414Sign900Numeral`); registration in
`backend/glossa_lab/experiment_graph.py`; the registration
verified by import in the run environment before the phase
ran (the node is present in `ATOMIC_NODES`). The run's base
was `main` at
`3200b7b5b6841a7b9567a81368bf84004fd17255`
(the Spec 045 landing-record merge). The run's own records:

- `specs/055-sign900-numeral/source-table-recovery.json`
  — the §6 recovery record, SHA-256
  `439f1449b8d7707d1feb88ef34e2edf90d3d192ba5c6f30bfa29cdf34b48852d`;
- `specs/055-sign900-numeral/strict-corpus-export.jsonl`
  — the gate-0.4 corpus export, SHA-256
  `1e421af1b75f09f49c928ef7eaa86e4c9a382e059d4771f164256a069896e02c`;
- `reports/phase414_results.json` — SHA-256
  `173a67a1d22651b1da03da0c40457e7234298fc6686dc22f3c2b6a25a2a5a6d5`;
- `reports/phase414_sign900_report.md` — SHA-256
  `c12bb0fe91e21c5c658474dbafe620675b20bf3b96a33cb791676230dcb5cada`.

Every digest was derived twice by independent routes
(`sha256sum` and a Python `hashlib` recomputation,
identical), and the script is deterministic: a second run
reproduced all four output files byte-identically.

## 2. Step 0 and stage 1, gate by gate

- **0.1 Input integrity — PASS.** Every §2 input
  recomputes to its freeze pin: the claim record
  `e9819089…`, the held cleaned text `1275b795…`, the
  literature record `92e19e6d…`, the Phase-104
  evaluation `2d0b83e8…`, the crosswalk registry
  `8a0b2a82…` (803 rows), the lane-2 drafts
  `3f645c9a…`, and the anchors file `df0cf620…`.
  Each pin was verified in the foreground by two
  independent routes — the GitHub contents API and
  the git-blob route, both at the run's base
  commit — with identical results, and again by
  the phase machinery in the worktree. The corpus
  source file and the Wells witness files used at
  stage 1 / gate 0.4 were likewise two-route
  verified at the base (`indus_research.jsonl`
  `08fc96c8…`; witness CSV `ecbc37a4…`; witness
  JSON `e9c49e52…`).
- **0.2 Source producible — PASS.** The source
  document was produced from the held copy and the
  §1 material located verbatim: the "Sign 900"
  section (printed p. 68), the "Numerical value of
  Sign 900" section with its Table 1 caption
  (printed pp. 72–74), and the summary statement
  (printed p. 85). One held-copy fact is recorded
  in the recovery record rather than repaired:
  Table 1's numeric grid did not survive the held
  copy's text extraction — the held text carries
  the caption and the surrounding prose, and no
  table body rows; nothing was reconstructed.
- **0.3 Recovery before verdict — HELD.** The
  recovery record is the first output the script
  writes, on every terminal outcome; the
  identification exists in the record before any
  results record or measure.
- **Stage 1 — IDENTIFIED.** The sign list is
  named from the document's own text, with four
  verbatim naming statements quoted in the
  recovery record: the opening statement (p. 57,
  signs "coded according to an extended sign list
  with 702 distinct signs (Wells 2015)"), the SIGN
  LIST section (p. 59, "The sign list by Wells
  (2011, 2015) has been extended to currently 702
  distinct signs"), the SUMMARY (p. 85), and the
  Appendix A heading (p. 88). The list named is
  the extended Wells (2011, 2015) sign list of
  702 distinct signs. The drawn sign was matched
  **by drawn form only**: the named list's sign
  900 is the single-arc grapheme — the Phase-123
  Wells segmentation witness (row M287; treatment
  SAME; verification: verified) records, from
  glyph inspection of Wells's PhD 2006 Figure 3.2
  plates (thesis p. 92), "W900 is the single-arc
  grapheme; thickness difference is font weight
  only", and its companion row records that the
  plates' arc signs (900–921) are all narrow
  parenthesis/C forms. In the crosswalk registry
  exactly one row's drawn description is a plain
  right parenthesis with no added element — P154,
  "Right parenthesis (perhaps with a backward
  curve at the bottom)" (every neighbouring
  parenthesis row carries an addition, or faces
  left). The two records agree on the pairing by
  drawn form: the witness row is the M287 row,
  and P154's Mahadevan crosswalk is M287. The
  registry's `W900` cell on the P154 row is
  consistent with the match but was **not** its
  basis — the frozen trap (F055-C07) is recorded
  as a trap in the run's results record. The
  source PDF's own figures could not be produced
  from the held record (the original PDF is not
  held in the repository; the literature record's
  stored path is a workstation path), so the
  drawn-form check rests on the witness's
  verified glyph inspection — stated openly in
  the recovery record's match citation.
- **Gate 0.4 Corpus — PASS.** The strict-corpus
  layer of record was identified as the program's
  V3 / Mahadevan-lineage corpus as held in the
  database, in its held form: the records of the
  tracked primary corpus
  (`glossa-corpus/indus/exports/indus_research.jsonl`,
  SHA-256 `08fc96c8…`) carrying source
  `indusscript-m77` and sign scheme Mahadevan1977
  — the executed Spec 033 precedent for this same
  layer (the V3 loader's own external Firestore
  export file is not present on disk, and
  `CORPUS_VERSIONS.md` records that the primary
  corpus already holds the same data in this
  form). The layer was exported in full to
  `strict-corpus-export.jsonl` (form and sort
  order stated in the step-0 record): **2,906
  records, 11,507 tokens, 393 distinct signs** —
  the token total re-derives Spec 033's recorded
  census for the same layer exactly. The
  identified sign's representation, by its
  crosswalked corpus identifier Mahadevan 287,
  is **79 occurrences** — above the frozen floor
  of 5 (DD-055-12).

## 3. Stage 2 — the pre-counting record and the measures

**Known-numeral set** (fixed before counting, from
published identifications only): the source document's
own stroke-sign identification (SPECIAL NUMERICAL SIGNS:
"The numerical value of stroke signs is most likely the
number of strokes"), entered through the 20 registry rows
whose drawn description is a pure stroke group and
nothing else, crosswalked to **29 Mahadevan corpus
identifiers** (86, 87, 89, 93, 94, 95, 96, 97, 98, 99,
100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
112, 114, 115, 116, 118, 119, 120, 121). The target is
not a member (DD-055-3). **Hedged members excluded**
(DD-055-14), listed separately in the pre-counting
record: Sign 415 (registry P092, Mahadevan 171 — "It is
therefore suggested that Sign 415 is a special numerical
sign, at least in some context") and Sign 70 (registry
P114, Mahadevan 155 — "may also be regarded as a
numeral sign… a non-numerical interpretation as a
bounded cluster is possible as well").

**Control set** (frozen nearest-10 rule, DD-055-11):
the 10 ordinary signs closest in count to the target's
79 — Mahadevan 216 (81), 17 (82), 403 (83), 124 (74),
244 (84), 204 (73), 402 (86), 149 (71), 51 (90),
70 (68).

**Dry-run** (DD-055-16), recorded in the pre-counting
record before the target was touched: the machinery ran
on Mahadevan 342 (1,274 occurrences, the highest-count
non-target, non-numeral sign) and produced a MIXED
mapping for it — the measures and mapping work as
written; the dry-run produces no target quantity and no
finding.

**Per-measure table** (target Mahadevan 287, 79
occurrences):

| Measure | Target | Numeral range (median) | Control range (median) | Numeral-side | Control-side |
|---|---|---|---|---|---|
| Short-text share | 0.164557 | 0.0–1.0 (0.238095) | 0.161765–0.395062 (0.265787) | yes | yes |
| Numeral adjacency share | 0.455696 | 0.0–1.0 (0.238095) | 0.098592–0.662651 (0.265035) | no | yes |
| Positional entropy (bits) | 2.708415 | −0.0–2.893777 (1.75) | 1.490324–2.972423 (2.290573) | no | yes |

Numeral-side 1, control-side 3 → **NOT NUMERAL-LIKE**
by the §5.3 mapping alone (O ≥ 2 and N < 2). Two
readings of the table are worth stating plainly, so the
closure cannot be misquoted. First, the target's
numeral adjacency share (0.455696) is in fact high —
above both medians — but the frozen numeral-side test
also requires the value to lie inside the known-numeral
set's range *and* differ from the control median in the
numeral median's direction; on adjacency the numeral
median (0.238095) sits *below* the control median
(0.265035), so the target's higher value is not in the
numeral median's direction from the control median,
and the measure is not numeral-side as frozen. No
other reading was substituted. Second, the target lies
inside the ordinary signs' range on all three measures:
on the frozen construction, its behaviour is
indistinguishable from frequency-matched ordinary
signs'. The source document's own argument for six was
not consulted as evidence at this stage (F055-C15);
it is preserved verbatim in the recovery record as
source material.

## 4. What this outcome does and does not establish

It establishes two things. First, an identification:
the fragment's sign is the drawn sign the source numbers
900 in the extended Wells (2011, 2015) list, matched by
drawn form to crosswalk registry row P154 (Mahadevan
287) — the record is converted from a pointer into a
claim, and the recovery that establishes it is preserved
in full (§6 form), including the sign-700 locators the
chain rule allows and nothing more. Second, a behaviour
result: on the pinned strict corpus, under the three
frozen measures, that sign does not behave as a numeral
sign behaves — the numeral reading the fragment carries
is contradicted at the behaviour stage. It does **not**
establish the value six, or any value; it does not
establish what the sign meant in use beyond the numeral
question; the outcome is a statement about this one
layer as pinned, not about any other compilation; and
it makes no finding about sign 700 — the recovery
record carries its locators only, and D-16 does not
join this campaign under E-7.

## 5. Claim consequences (governed register)

Executed under register 0.7-draft (frozen); one line per
claim, F055-C01…C15.

- **F055-C01** (an outcome states only whether the
  identified sign behaves as a numeral sign behaves, in
  the pinned layer, under the frozen measures): HELD —
  this record states the behaviour outcome and the
  identification it rests on, and nothing about a value,
  a meaning beyond the numeral question, another corpus,
  or sign 700.
- **F055-C02** (the record under test is the UNTESTED
  fragment): CHECKED — the claim record was read and
  pin-verified at gate 0.1; the fragment reads "Sign
  value: 900 / number six", status untested, stage
  created, exactly as the claim states.
- **F055-C03** (the identified sign is numeral-like in
  the pinned strict corpus): FALSIFIED at the behaviour
  stage — the §5.3 mapping assigns NOT NUMERAL-LIKE
  (numeral-side 1, control-side 3); the hypothesis does
  not stand on this layer under these measures.
- **F055-C04** (the falsifier is two-stage): HELD in its
  behaviour branch — stage 1 succeeded, so the
  falsifier was reached at stage 2 and fired there; the
  identification-stage branch was not the outcome.
- **F055-C05** (execution stops before any
  identification if a step-0 gate fails): HELD as a
  gate discipline — gates 0.1 and 0.2 passed on
  observed values, gate 0.4 passed before step 2, and
  no measure exists past any gate that did not pass.
- **F055-C06** (identification succeeds only if the
  list is named from the document's own text and the
  drawn sign is matched): HELD — the identification
  rests on the recovery record alone: four verbatim
  naming statements quoted with locators, and the
  drawn-form match of §2 above. The draft's expected
  reading had no standing and was not inherited.
- **F055-C07** (no match is made by sign number): HELD
  — the match rests on drawn-form descriptions; the
  `W900` cell on the P154 row was recorded as the
  frozen trap in the results record and was not used
  as the identification, nor was its drawn description
  treated as a refutation without the drawn-form
  comparison the claim requires.
- **F055-C08** (step 1's output is a preserved record
  in the fixed §6 form): HELD —
  `source-table-recovery.json` (schema
  `glossa.source-table-recovery/1`) was produced as
  the execution's first output, with the naming
  statements, the recovered sections verbatim with
  locators, the figure captions, the target-sign
  block with its citation, and the sign-700 locator
  block.
- **F055-C09** (the recovery does not admit D-16):
  HELD — the sign-700 material is locators only
  (p. 70, 'SIGN 700 WITH NUMBERS'; pp. 72–74, the
  counted units of the 'Numerical value of Sign 900'
  section); nothing about sign 700 is adjudicated,
  no part of D-16 is designed or advanced, and the
  chain sentence stands in §1 of this record and in
  every product of the run.
- **F055-C10** (the behaviour test is specified only
  for the identified case): HELD — step 2 ran only
  because stage 1 returned IDENTIFIED, through gate
  0.4, in the frozen order.
- **F055-C11** (the known-numeral set is fixed from
  published identifications before counting): HELD —
  the set was fixed in the pre-counting record from
  the source's published stroke-sign identification
  (29 Mahadevan identifiers), the target excluded,
  target-to-target adjacency not counted, and the
  two hedged candidates (Signs 415 and 70) excluded
  and listed separately under DD-055-14.
- **F055-C12** (the control set is selected by the
  fixed rule): HELD — the nearest-10 rule with ties
  by corpus identifier ascending produced the set in
  §3, recorded in the pre-counting record before any
  §5.2 measure existed; the DD-055-16 dry-run on
  Mahadevan 342 precedes the target's measures in
  the same record.
- **F055-C13** (the outcome is assigned by the §5.3
  mapping alone): HELD — numeral-side 1, control-side
  3 maps to NOT NUMERAL-LIKE by the frozen mapping;
  the adjacency reading in §3 states why no other
  assignment was available under the directional
  clause as frozen.
- **F055-C14** (every terminal outcome is recorded in
  a pre-written §5.4 wording): HELD — the headline is
  the frozen NOT NUMERAL-LIKE wording with the
  registry id and the control-side count filled in
  from the run.
- **F055-C15** (no outcome establishes the value
  six): HELD — no product of this execution states a
  value for the sign; the source's argument for six
  is preserved in the recovery record as source
  material and was cited as evidence at no stage.

**Anchors.** `backend/reports/INDUS_FINAL_ANCHORS.json`
recomputed before and after the run: SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
at both points — byte-identical, asserted.

## 6. Records

- Recovery record:
  `specs/055-sign900-numeral/source-table-recovery.json`;
  results: `reports/phase414_results.json`; report:
  `reports/phase414_sign900_report.md`; corpus export:
  `specs/055-sign900-numeral/strict-corpus-export.jsonl`
  (digests in §1).
- Graph node: `IndusPhase414Sign900Numeral`
  (registered and verified by import before the run).
- Claim record: the appended `first_check` entry on
  `ancient_writing_and_modern_technologies_51831ac9_sign_val_0001`'s
  record (identification outcome and behaviour
  outcome), append-only verified against the base
  file (removing the inserted block reproduces the
  base file byte-for-byte).
- Root LEDGER entry: "Spec 055 (Phase-414)" entry
  added with this record.
- Tasks: E1–E6 stand ticked in `tasks.md` (L7 ticked
  with them: the freeze PR merged at `e3399961`).
- `adjudication.md`, `spec.md`, `claims.json`,
  `freeze.md`, and `freeze.json` were **not** edited:
  they are digest-covered sources of the freeze
  (`test_spec055_freeze.py` enforces the pins), and
  the executed-spec form records execution here, in
  `outcome.md`.
- Local-environment disclosure: in this VM's
  existing glossa-lab venv, the freeze tests'
  `test_register_integrity` fails with a TypeError
  from the venv's AEE loader version (the conftest's
  `strict` keyword) — verified to occur identically
  on the clean `main` tree at the run's base with
  no execution changes present; it pre-exists this
  execution, the frozen files are byte-identical to
  `main`, and the same local-only failure was
  disclosed on the Spec 044/045/046 records. The
  execution tests (`test_spec055_execution.py`, 5
  tests) pass locally. The PR's CI run is the figure
  of record.
- CI and foundation check (H21) at the record
  merge: appended below after the record PR merges,
  in the Spec 045/047 completion pattern — this
  section is completed by append, not edited.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

---

## Landing record — 2026-10-21 (appended at merge; append-only)

- Execution PR: **#273** (branch
  `spec-055-phase414-execution`), merged to `main`
  as merge commit
  **`02c8daf9034520540cf4cf7a16ef039bd37678de`**.
- CI: GitHub Actions run **39627759493** on the
  PR head `274beffd` — **7 of 7 jobs success**,
  verified from the run's own job conclusions
  (Backend tests (pytest); Frontend tests
  (Playwright); Indus public validation checks;
  Evidence Graph script smoke tests; Shell
  wrappers ubuntu / macos / windows).
- Run digests re-verified on `main` at the
  merge commit by two routes (the full-clone
  working tree and the contents API):
  `source-table-recovery.json`
  `439f1449b8d7707d1feb88ef34e2edf90d3d192ba5c6f30bfa29cdf34b48852d`,
  `strict-corpus-export.jsonl`
  `1e421af1b75f09f49c928ef7eaa86e4c9a382e059d4771f164256a069896e02c`,
  `reports/phase414_results.json`
  `173a67a1d22651b1da03da0c40457e7234298fc6686dc22f3c2b6a25a2a5a6d5`,
  `reports/phase414_sign900_report.md`
  `c12bb0fe91e21c5c658474dbafe620675b20bf3b96a33cb791676230dcb5cada`
  — identical to the values in §1 of this
  record. The claim record with its appended
  `first_check` entry stands at
  `cabba73521b19cf47df9bc6ed83731cb024b5298f3130b121ddb7a390c7a8c02`
  on `main`; the anchors file stands at its
  frozen pin `df0cf620…`, byte-identical.
- Foundation check (H21) at the merge commit,
  on a fresh full clone with the two Holdat
  CSVs copied from the existing local downloads
  (corpus CSV SHA-256
  `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`
  verified first): **40 checks passed, 0
  failed, 8 warnings** — the standing figure.
- Terminal outcome stands as recorded above:
  **NOT NUMERAL-LIKE** — stage 1 IDENTIFIED
  the sign (P154 / Mahadevan 287), and the
  numeral reading is contradicted at the
  behaviour stage on the pinned layer. The
  recovery record is preserved as this spec's
  record; D-16 does not join this campaign on
  it (E-7).

*AI disclosure: appended by an AI agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*

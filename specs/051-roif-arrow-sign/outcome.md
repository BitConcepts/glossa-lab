# Spec 051 — Outcome record

> ## EXECUTED 2026-10-21 (Phase-409) — INCONCLUSIVE: THE CLASSIFICATION IS THE FINDING (gate 0.6)
>
> This record is written by the execution act
> (tasks E1–E6). It executes the frozen Spec 051
> contract (freeze digest
> `818cfa4ecd32d286dbe0fcc8d73f4a79f42610f181e5f19594d057a32dab64b1`)
> as **Phase-409** under the campaign execution
> order of 2026-10-21 (Wave 3, Group 3), after
> the OSF registration **xnrph** was approved and
> public, and after Spec 047's step-1 asset
> freeze had landed (the execution order this
> contract requires). Step 0 ran in the frozen
> gate order: gates 0.1–0.5 PASS; gate 0.6's
> floors fire, so the execution closes as
> **INCONCLUSIVE — the classification is the
> finding**, no share was computed, and the
> claim stands **UNTESTED**. All products are
> held under the Roif gate (spec §9).

## Headline (§6 pre-written wording, INCONCLUSIVE — classification form)

"The arrow-sign test did not run: 0 testable
gateway/border sites carry the arrow sign
(floor 3); one side of the comparison is empty
in the test population. The finding of this
execution is the classification and the census
themselves (Asset B, digest
`a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85`):
status counts AGREED 3, DISAGREED 1,
NO-SOURCE 16, SINGLE-SOURCE 10; testable sites
2 (harappa — administrative, 52 M391
occurrences in 492 joined inscriptions; lothal
— port/trade, 14 M391 occurrences in 124
joined inscriptions); per-site M391 counts
over the layer of record: Mohenjo-daro 75,
Harappa 52, Dholavira 16, Lothal 14, Surkotada
11, Kalibangan 10, Chanhu-daro 10, Banawali 3,
Rakhigarhi 2 (total 193), with the excluded
and non-spine sites named in full — including,
on the record, Dholavira, Chanhu-daro, and
Rakhigarhi, which carry 28 of the sign's 193
recorded occurrences outside the gazetteer
spine. No share was computed. The claim stands
UNTESTED, now with the reason measured rather
than asserted."

**Fence sentence (§8 item 5).** "This result
is about the arrow sign's distribution. It is
not evidence of what the sign meant."

## 1. What was executed

The frozen Spec 051 contract, executed as
**Phase-409**. Graph-first build (H15/H23,
task E1): phase script
`backend/scripts/phase409_roif_arrow_sign.py`;
graph module
`backend/glossa_lab/experiment_graph_phase409.py`
(node `IndusPhase409RoifArrowSign`);
registration in
`backend/glossa_lab/experiment_graph.py`,
verified by import before the run (node
present among 497 registered nodes). Then step 0 in the
frozen order (E2–E4): input integrity, the
Asset B digest assertion and form check, the
counting-layer identification, pin, and
census reproduction, the join census, and the
test-population census and floors. The §5
primary (task E5) was not run: gate 0.6
closed the execution before any share
existed, exactly as the frozen contract
provides. The run's own records:
`reports/phase409_results.json` and
`reports/phase409_report.md`.

## 2. Step 0 — gates (spec §3), observed values

- **0.1 Input integrity: PASS.** Every §2
  input carrying a pin hashes to its
  freeze-record value, verified by the phase
  machinery in the worktree and, in the
  foreground, by the contents-API route at
  the run's base: Phase-104 evaluation
  `2d0b83e8…`, Holdat roles file `3f1c24ed…`,
  gazetteer `5ac76a30…`, the five-site defect
  file `fc05e552…` (explicitly not the
  counting layer), Spec 047's frozen spec
  `1a18dac0…`, anchors `df0cf620…`. The claim
  file is asserted in the Spec 038 form the
  freeze record specifies: the freeze-time
  hash `bc22d6f0…` carried as a definition
  constant, and the `manual_003` facts
  asserted on the live file (arrow sign /
  border enforcement, proposed value *tīr*,
  the falsification condition verbatim,
  status untested) — all match. Spec 047's
  freeze digest replays from its freeze
  record: `8501feab…`. The Phase-104 entry
  carries the claim as *stays untested* under
  RULE-SITE, and the roles file carries M391
  as CASE_MARKER_SUFFIX / TERMINAL, count
  193, `is_ending` true.
- **0.2 Asset B digest assertion: PASS.**
  Asset B, exhibited at its contract path
  `specs/047-roif-ledger-distribution/asset-b/site-functions.jsonl`,
  recomputes over the file bytes as committed
  to
  **`a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85`**,
  identical to the digest recorded in Spec
  047's step-1 outcome record — the pin
  source fixed at this freeze (DD-051-14);
  the digest's presence in that record was
  verified mechanically by the phase
  machinery. The asset was not rebuilt,
  re-derived, or substituted.
- **0.3 Asset B form and testable set:
  PASS.** Exactly 30 rows, sorted by
  `program_site_id`, one per pinned
  gazetteer cluster, the seven contract
  fields on every row, source objects in the
  contract form, statuses and classes in the
  contract vocabularies (the §4.3 convention
  observed: `primary_class` set only on
  AGREED rows). Per-status counts: AGREED 3,
  DISAGREED 1, SINGLE-SOURCE 10, NO-SOURCE
  16. **Testable set, derived by rule: 2** —
  harappa (administrative) and lothal
  (port/trade). The third AGREED row, shahr i
  sokhta, is `mixed/unknown` and is excluded
  from the test by §4.2.
- **0.4 Counting layer: PASS.** The Holdat
  layer of record — the layer Phase-104
  counted — is identified from the
  database-held downloads tree as the Holdat
  corpus file the Phase-45/46/54 scripts of
  record read:
  `corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv`.
  Export form, as produced: CSV, the file
  bytes as held — 7,002 sign-token rows in
  file order (grouped by inscription,
  position ascending within each
  inscription), no reordering, filtering, or
  re-encoding applied; the export is the file
  as held, pinned here by SHA-256
  **`62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`**
  (593,253 bytes; 1,670 inscriptions over 9
  sites). The re-derived M391 per-site
  counts reproduce the §1 census **exactly**:
  Mohenjo-daro 75, Harappa 52, Dholavira 16,
  Lothal 14, Surkotada 11, Kalibangan 10,
  Chanhu-daro 10, Banawali 3, Rakhigarhi 2 —
  total **193**, agreeing with the pinned
  roles file's count for M391. Per-site
  inscription totals (the §5.2 denominators,
  derived here and used by no quantity,
  because the run closed at gate 0.6):
  Mohenjo-daro 606, Harappa 492, Lothal 124,
  Kalibangan 110, Dholavira 106, Chanhu-daro
  78, Surkotada 61, Banawali 60, Rakhigarhi
  33. Per-site mean inscription lengths are
  recorded in `reports/phase409_results.json`.
- **0.5 Join census: PASS.** Every one of
  the pinned export's 7,002 records is
  accounted for in exactly one class under
  the §5.1 normalisation: **joined 6,117**
  records to a spine cluster (1,453
  inscriptions); **non-spine site 885**
  records (217 inscriptions) over 3 site
  values — Dholavira 439 records / 16 M391,
  Chanhu-daro 310 / 10, Rakhigarhi 136 / 2;
  **no site value 0**. The non-spine class
  carries exactly the three §1 census sites
  the draft expected, and their 28 M391
  occurrences sit outside the test by rule
  (§5.1). No record was dropped or
  hand-assigned.
- **0.6 Test-population census and floors:
  THE FLOORS FIRE — the execution closes
  here.** Test population (counts only, no
  share): harappa — administrative (pooled),
  492 joined inscriptions, 52 M391
  occurrences; lothal — port/trade (pooled),
  124 joined inscriptions, 14 M391
  occurrences. Per class: gateway/border 0
  testable sites; administrative 1;
  port/trade 1; domestic 0; ritual 0;
  `mixed/unknown` carries no testable site
  by rule. Floors: testable gateway/border
  sites carrying M391 = **0**, against the
  floor of 3 — **FAIL**; the pooled side is
  non-empty (2 sites) — pass; the contrast
  side {domestic, ritual} is **empty** in
  the test population — **FAIL**. Under
  §5.4 the execution closes as
  **INCONCLUSIVE — the classification is the
  finding**, with this census as its
  finding. No share, ratio, permutation, or
  regression quantity was computed.

## 3. The excluded and non-spine sites, in full (§§4.3, 5.5)

Every site the outcome does not cover, with
its M391 count where the join census carries
it (sites absent from the layer of record
join 0 records and carry no M391 count in
this layer):

- **DISAGREED (1):** surkotada — 61 joined
  inscriptions, 11 M391. Its two sources
  disagree (gateway/border against
  mixed/unknown); it is the only
  gateway/border-mapped reading in the
  frozen asset, and it is excluded by rule,
  so the gateway/border class has no
  testable member at all.
- **SINGLE-SOURCE (10):** mohenjo daro
  (source maps administrative) — 606 joined
  inscriptions, 75 M391; kalibangan
  (administrative) — 110, 10; piklihal
  (domestic) — 0 joined, no count in this
  layer; rojdi (domestic) — 0, none;
  sannarachamma (domestic) — 0, none; sheri
  khan tarakai (domestic) — 0, none; ter
  kala dheri (domestic) — 0, none;
  hiregudda (mixed/unknown) — 0, none;
  khirsara (mixed/unknown) — 0, none;
  tigrana (mixed/unknown) — 0, none.
- **NO-SOURCE (16):** banawali — 60 joined
  inscriptions, 3 M391; amri, chagylly,
  desalpur, islam chowki, jhukar,
  joenniemi, kanispur, kunal, mullali,
  ojiyana, qasim bagh, rangpur, sheri khan
  tarakai 3, sheri khan tarakai 4,
  yalangach — 0 joined, no count in this
  layer.
- **AGREED at `mixed/unknown` (1):** shahr i
  sokhta — 0 joined, no count in this layer;
  excluded from the primary test by §4.2.
- **NO-CORPUS-COVERAGE:** none — both
  testable sites carry joined inscriptions.
- **Non-spine sites (outside the population
  by rule, §5.1):** Dholavira — 106
  inscriptions, 16 M391; Chanhu-daro — 78,
  10; Rakhigarhi — 33, 2. Together 28 of
  the sign's 193 recorded occurrences.

## 4. What this outcome does and does not establish

The gate-0.6 census establishes exactly one
thing: on the frozen classification, the
comparison the claim's own falsifier states
has no population to run on. Asset B, built
under the two-source rule from the site
literature, agrees on a primary class for
only three of the thirty spine sites; two of
those are testable, both sit on the pooled
side of the frozen groupings, no site is
testably gateway/border, and no site is
testably domestic or ritual — so neither the
primary ratio nor the city ratio nor the
rival score can be formed, and none was.
**This does not establish** anything about
the arrow sign's distribution at testable
sites (no share exists), anything about what
the sign meant, or any verdict on the claim:
the claim stands **UNTESTED**, now with the
reason measured rather than asserted — the
classification and the census are the
finding, as §6's pre-written wording states.
A future test of this claim is a new act: it
would need a classification under which the
frozen floors can be met (a successor asset
under a successor spec, per §4.4), not a
continuation of this execution.

## 5. Claim consequences (governed register)

One line per governed claim, F051-C01…C20.

- **F051-C01** (an outcome states only the
  M391 distribution by share across Asset B's
  classes at the testable sites): HELD in
  scope — this record states the census and
  the closure only; no distribution
  conclusion is stated, because no share was
  computed.
- **F051-C02** (`manual_003` stands UNTESTED
  on its Phase-104 record under RULE-SITE):
  HELD — the Phase-104 record stands
  unedited and the claim stands UNTESTED;
  the dated append on the claim's record
  (§6) records this closure beside it.
- **F051-C03** (the recorded M391 census
  totals 193 over nine sites): CHECKED at
  gate 0.4 — re-derived from the pinned
  export and reproduced exactly.
- **F051-C04** (within the test population,
  the pooled share exceeds the contrast
  share): NOT REACHED — gate 0.6 closed the
  execution before any share existed.
- **F051-C05** (a pooled ratio not exceeding
  1.0 is NOT SUPPORTED): NOT REACHED — no
  ratio was computed, so the clause was
  never evaluated.
- **F051-C06** (Spec 051 consumes Asset B as
  frozen by Spec 047): HELD — the asset was
  exhibited, digest-asserted, and consumed
  exactly as frozen; nothing was rebuilt,
  re-derived, or repaired.
- **F051-C07** (Asset B as consumed is the
  contract file with exactly 30 rows):
  CHECKED at gate 0.3 — held, §2 above.
- **F051-C08** (the comparison groupings are
  Spec 047 §4.2's, fixed for D-10's use):
  HELD — the gate-0.6 census is stated in
  exactly those groupings (pooled
  ADMIN-TRADE-GATEWAY against {domestic,
  ritual}); no class was invented.
- **F051-C09** (test entry requires an AGREED
  row): CHECKED at gate 0.3 — the testable
  set was derived by that rule (2 sites).
- **F051-C10** (Asset B is consumed by a
  digest pin whose source is Spec 047's
  step-1 outcome record): CHECKED at gate
  0.2 — the recomputed digest matches the
  digest that record carries.
- **F051-C11** (the test population is the
  testable spine sites carrying at least one
  joined inscription): CHECKED at gates
  0.5–0.6 — both testable sites carry joined
  inscriptions; no NO-CORPUS-COVERAGE site
  arose.
- **F051-C12** (the counting layer is the
  Holdat layer Phase-104 counted): CHECKED
  at gate 0.4 — identified, exported in
  full, and pinned; the exact census
  reproduction is its identity test
  (DD-051-13).
- **F051-C13** (per-site share = M391
  occurrences / inscriptions): NOT REACHED —
  the definition was never applied; no share
  exists.
- **F051-C14** (significance judged by the
  label-shuffling permutation test at seed
  20261021): NOT REACHED — no permutation
  ran.
- **F051-C15** (the case-ending rival scored
  in the same run by the size regression):
  NOT REACHED — the rival score is §5
  machinery and no run reached it; the
  rival's recorded facts (the roles file's
  CASE_MARKER_SUFFIX record) were asserted
  at gate 0.1 and stand as recorded.
- **F051-C16** (the verdict is assigned
  mechanically by §5.4's partition): HELD —
  the outcome is the partition's own floor
  clause (§5.4, first paragraph) applied to
  the gate-0.6 census, mechanically.
- **F051-C17** (fewer than 3 testable
  gateway/border sites carrying M391 closes
  the execution as INCONCLUSIVE): FIRED as
  written — the count is 0; the
  empty-contrast-side floor fired beside it.
- **F051-C18** (the §5.5 sensitivities are
  reported beside the primary): NOT REACHED
  in their stated form — no primary exists
  to report beside; the restated-exclusions
  sensitivity is discharged in its closure
  form at §3 above, with M391 counts.
- **F051-C19** (every record stays internal
  under the Roif gate): HELD — this record
  and its companions are internal; nothing
  was published or surfaced, and campaign
  reporting names this member only as
  executed — held under the Roif gate.
- **F051-C20** (no outcome establishes that
  the arrow sign meant border enforcement):
  HELD — no meaning statement appears in
  any product of this execution.

## 6. Records

- Results JSON: `reports/phase409_results.json`
  (SHA-256
  `3f4bf2a5eda7959a9ae85b48a5c5d0d31ad276b849f41854a71b08011fca1361`;
  the script is deterministic — a second run
  reproduced both output files byte-identically)
- Report: `reports/phase409_report.md`
  (SHA-256
  `51a9d3a106bc8df7eb7dd9b68243ae89a8e108dabbeb81eac301ed9f05e68b36`)
- Graph node: `IndusPhase409RoifArrowSign`
  (registered and verified by import before
  the run).
- Claim record: the dated append
  `spec051_execution` on
  `indus_valley_script_deciphered_from_myth_65ff0a26_manual_003`
  in the extracted-claims file — appended
  beside the frozen record, altering no
  pre-existing field; the claim's status
  (untested) and stage (created) are
  unchanged, and removing the append
  reproduces the pre-act file byte-identically.
- Root LEDGER entry: `LEDGER.md`, 2026-10-21,
  Spec 051 execution.
- `adjudication.md` carries no execution
  append: it is a digest-covered source of
  the freeze (`freeze.json` source list), and
  this outcome record is the execution's
  record, in the form of Specs 044/047.
- Anchors: asserted byte-identical before
  and after (`df0cf620…`).
- Foundation check (H21): run in the run tree
  after the execution — **40 passed / 0
  failed / 8 warnings**, the standing figure;
  `reports/foundation_check_report.json` is
  regenerated in this act (its changes are
  the generation timestamp and the
  extracted-claims store's combined hash,
  which moves because of the claim append
  above; every check figure is unchanged).
  Re-verified at the merge commit in the
  landing record appended at merge.
- Tasks E1–E4 and E6 stand ticked in
  `tasks.md`; E5 (the §5 primary) remains
  open in form and unrun in fact — gate 0.6
  closed the execution before it, and under
  this contract it has no run.

---

*AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution §VI.*

---

## Landing record — 2026-10-21 (appended at merge; append-only)

- Execution PR: **#299** (branch
  `spec-051-phase409-execution`), merged to
  `main` as merge commit
  **`c5c1f3688be1a5682d2fa5a44c16db64930bd8eb`**.
- CI: GitHub Actions run **39658382722** on the
  PR head `35fbed76` — **7 of 7 jobs success**,
  verified from the run's own job conclusions
  (Backend tests; Frontend tests (Playwright);
  Indus public validation checks; Evidence
  Graph script smoke tests; Shell wrappers
  ubuntu / macos / windows). The backend job
  log reads 1,616 passed / 20 skipped / 0
  failed. The PR's first head (`6fbc0238`, run
  39656667255) failed the backend job on one
  test — this execution's own claim-append test
  (1 failed, 1,475 passed): the backend suite
  regenerates the extracted-claims store
  during a full run, rewriting the appended
  file before the test read it. The test was
  corrected to the Spec 057 precedent (the
  append is verified at the act and by
  read-back at landing; the suite pins the
  frozen record's preserved state), and the
  corrected head is the one that merged.
- Digests re-verified on `main` at the merge
  commit by the contents-API route: Asset B
  `a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85`,
  anchors
  `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`,
  results JSON
  `3f4bf2a5eda7959a9ae85b48a5c5d0d31ad276b849f41854a71b08011fca1361`,
  report
  `51a9d3a106bc8df7eb7dd9b68243ae89a8e108dabbeb81eac301ed9f05e68b36`
  — identical to the values in this record;
  the `spec051_execution` append is present
  on the claim's record at the merge commit,
  with its status (untested) and stage
  (created) unchanged.
- Foundation check (H21) at the merge
  commit: **40 checks passed, 0 failed, 8
  warnings** — measured in the run tree after
  the execution (the regenerated report is
  part of PR #299); every input the check
  reads is byte-identical between the run
  tree and the merge tree (the only
  intervening merge, Spec 050's execution,
  touched no foundation input, and the
  anchors, claims-store, and results
  read-backs above confirm the identity at
  the merge commit itself).
- Tasks E1–E4 and E6 stand ticked in
  `tasks.md`, and L7 with them; E5 (the §5
  primary) remains open in form and unrun in
  fact — gate 0.6 closed the execution before
  it. The claim stands **UNTESTED**.

*AI disclosure: appended by an AI agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*

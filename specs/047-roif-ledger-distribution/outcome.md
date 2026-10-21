# Spec 047 — Outcome record

> ## STEP-1 RECORD — EXECUTED 2026-10-21 (Phase-406)
>
> This record is written by the step-1 execution
> act (tasks E1–E4). It is the pin source for
> Asset B fixed by Spec 051's DD-051-14: the
> Asset B byte-digest, row count, testable
> count, and per-status counts are recorded
> here. Step 2 (tasks E5–E7) has **not** run:
> no distribution quantity exists, and the
> claim stands **UNTESTED**. All products are
> held under the Roif gate (spec §10).

## Headline (§9 items, as applicable at step 1)

1. **Corpus label.** The primary layer as
   pinned in spec §2:
   `backend/glossa_lab/data/yajnadevam_inscriptions.csv`
   (5,679 records; the site-attributed layer of
   Specs 027/028), SHA-256
   `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98`.
2. **Asset B.** File
   `specs/047-roif-ledger-distribution/asset-b/site-functions.jsonl`;
   SHA-256 digest over the file bytes as
   committed:
   **`a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85`**.
   Rows: 30. Testable: **2** (harappa —
   administrative; lothal — port/trade).
   Per-status counts: AGREED 3, DISAGREED 1,
   SINGLE-SOURCE 10, NO-SOURCE 16.
3. **Join census (gate 0.3).** 5,679 records,
   each in exactly one class: joined to a
   spine cluster 5,106; non-spine site 573
   over 66 site values (by name with counts
   in `reports/phase406_step1_report.md` and
   `reports/phase406_results.json`; the two
   largest are Dholavira 238 and Chanhu-daro
   74, both outside the population by rule,
   DD-047-12); no site value 0.
4. **Step-2 quantities (§9 item 4).** Not
   computed — step 2 is a separate execution
   act. No R, no p-value, no R_ledger exists.
5. **Component fence.** This result concerns
   the distribution component of Roif's ledger
   thesis only; the guild-authority and
   Akkadian-influence components were not
   tested.

## 1. What was executed

The frozen Spec 047 contract, freeze digest
`8501feabb7beee621e99ae48529e5a74c0788fb0619ac49c615912e13914cdc7`,
executed as **Phase-406** under the campaign
execution order of 2026-10-21 (Wave 3, Group
1), after the OSF registration b2a8w was
approved and public. Graph-first build
(H15/H23, task E1): phase script
`backend/scripts/phase406_roif_ledger_step1.py`;
graph module
`backend/glossa_lab/experiment_graph_phase406.py`
(node `IndusPhase406RoifLedgerStep1`);
registration in
`backend/glossa_lab/experiment_graph.py`,
verified by import before the run (node
present among 483 registered nodes). Then:
step 0 (E2), step 1a Asset B (E3), step 1b
ledger-sign list (E4). Tasks E5–E7 (step 2
and the outcome act) were not run and remain
open.

## 2. Step 0 — gates (spec §3), observed values

- **0.1 Input integrity: PASS.** All eight §2
  inputs hash to their freeze pins. Verified
  in the foreground by two independent
  routes (contents-API raw and git-blob at
  `main` `9786265a`) before the run, and
  again by the phase machinery in the
  worktree: gazetteer
  `5ac76a30…`, corpus `c02e3d7b…`, crosswalk
  `e44b8b55…`, Phase-104 evaluation
  `2d0b83e8…`, seed_citations.py
  `39d28112…`, Roif model file `c5f08461…`,
  anchors `df0cf620…`, Spec 027 spec
  `7fff5d5a…` (full values in
  `reports/phase406_results.json`).
- **0.2 Spine reproduction: PASS.** 36 rows,
  30 distinct `program_site_id` clusters, the
  frozen cluster list exactly; each cluster
  carries one `site_name_as_published`.
- **0.3 Join census: PASS.** 5,679 records
  accounted for exactly once under the §6.1
  normalisation: joined 5,106; non-spine 573
  over 66 site values; no site value 0. The
  census was computed by the machinery in a
  sealed step-0 run before the asset existed;
  only the class totals above were read
  before the freeze (§4.5). One mechanical
  consequence a reader will spot: the corpus
  value "Rodji" (4 records) is **not** the
  spine cluster "rojdi" under the frozen
  normalisation (no fuzzy matching, §6.1), so
  it stands in the non-spine list and rojdi
  joins 0 records. That is the frozen rule
  applying as written; nothing was
  hand-assigned.

## 3. Asset B — the build (step 1a, spec §4)

Built by cited-data entry on the gazetteer
spine: one row per cluster, sorted by
`program_site_id`, in the §4.1 form exactly.
Convention recorded here: `primary_class` is
set only where §4.3 sets it (AGREED rows);
for DISAGREED, SINGLE-SOURCE and NO-SOURCE
rows it is null, because no agreed primary
class exists — each non-AGREED row's
evidence stands in its sources and notes.

Result by status (full rows in the asset
file):

- **AGREED (3):** harappa — administrative
  (Weber 1999; IGNOU synthesis §1.6);
  lothal — port/trade (Rao 1979; Rawat,
  coastal-sites chapter); shahr i sokhta —
  mixed/unknown (UNESCO Decision 38 COM
  8B.26; Guidorzi et al. 2025), excluded
  from the primary test by §4.2.
- **DISAGREED (1):** surkotada — Joshi 1990
  as quoted in Rawat p. 199 (a garrison
  controlling eastward movement:
  gateway/border) against Rawat's own
  statement (a centre for exploiting local
  mineral resources: no §4.2 class,
  mixed/unknown). No tiebreak applied (§4.4).
- **SINGLE-SOURCE (10):** hiregudda
  (mixed/unknown), kalibangan
  (administrative), khirsara
  (mixed/unknown), mohenjo daro
  (administrative), piklihal (domestic),
  rojdi (domestic), sannarachamma
  (domestic), sheri khan tarakai (domestic),
  ter kala dheri (domestic), tigrana
  (mixed/unknown). Each is recorded in the
  asset with its citation and is excluded
  from the test by rule.
- **NO-SOURCE (16):** amri, banawali,
  chagylly, desalpur, islam chowki, jhukar,
  joenniemi, kanispur, kunal, mullali,
  ojiyana, qasim bagh, rangpur,
  sheri khan tarakai 3, sheri khan tarakai 4,
  yalangach. Each row's `notes` record the
  works consulted, so the absence is
  checkable (§4.4).

**Testable: 2** (harappa, lothal — both in
the pooled ADMIN-TRADE-GATEWAY grouping;
the contrast side is empty in the frozen
asset). The number of testable sites is not
a build gate (DD-047-1): the asset freezes
as built, and its thinness is adjudicated by
the step-2 classification gate (§6.3,
DD-047-2) when step 2 runs.

**Build gates.** B1 (coverage): PASS —
exactly the 30 spine clusters, sorted
(mechanical). B2 (citation completeness):
PASS — every AGREED row carries two
complete sources; every non-AGREED row
carries the record its §4.4 status requires
(mechanical). B3 (verification): PASS after
demotions — the §4.3 verification pass is
recorded in full in §4 of this record;
demotions were made before the freeze and
are recorded in the demoted rows' `notes`.
B4 (circularity): the §4.5 attestation is
at §5 of this record and can be made
truthfully, with the one disclosure stated
there.

**Digest.** SHA-256 over the asset file
bytes as committed:
`a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85`,
computed by two independent routes in the
foreground (direct hash of the written file;
the phase machinery's recomputation), with
a third route (the committed git blob)
verified at landing. Row count 30, testable
count 2, per-status counts as above. Per
§4.6 and Spec 051 DD-051-14, this record is
the digest's record of publication for
dependents; `freeze.md` / `freeze.json` are
the freeze act's own digest-covered records
and were not edited (they are pinned by
`backend/tests/test_spec047_freeze.py`).

## 4. The §4.3 verification pass, in full (DD-047-14)

Performed 2026-10-21 by the executing worker
as a separate pass over the entered
citations alone (statement → mapped class,
against the §4.2 rule), before the freeze.
Entry and verification were both performed
by the same AI agent (Muse Spark,
via Muse) in separate passes; the
spec permits a second pass by the build
worker, and the identity is disclosed here
rather than dressed as two workers.

- harappa: PASS. Weber 1999, p. 817, re-read
  in the full text ("production hub and
  depot for both local and regional trade
  items" — central storage/redistribution:
  administrative). The synthesis statement
  re-read in the published unit text
  ("important political and administrative
  regional centers": administrative). Two
  distinct works, distinct authors.
- lothal: PASS. Rawat's chapter re-read at
  pp. 190–192 (his own port/trade
  assessment). Rao 1979 is the excavation
  monograph whose stated thesis is the
  port-town identification. Distinct works,
  distinct authors; Rawat's statement is
  not a repetition of Rao (it follows his
  own review of the dock dispute).
- shahr i sokhta: PASS. The UNESCO brief
  synthesis and Guidorzi et al. 2025 §1.3
  re-read; each names several functions
  with none stated primary
  (mixed/unknown ×2 → AGREED mixed/unknown).
- surkotada (DISAGREED): both statements
  re-read at Rawat p. 199, including the
  excavator's words as quoted there with
  their IAR/Joshi locators.
- **Demotion — khirsara: AGREED →
  SINGLE-SOURCE.** The candidate pair
  (Nath, Kumaran & Chandra 2015;
  Pokharia et al. 2017, PLoS ONE) shares
  authorship — Nath and Kumaran are the
  excavation team and appear on both — so
  the second statement fails §4.3
  independence ("distinct works by
  distinct authors"). Both statements map
  to mixed/unknown; the row stands
  SINGLE-SOURCE on the excavators' 2015
  statement, with the 2017 statement
  recorded in its `notes`, not counted.
- **Demotion — sheri khan tarakai: AGREED →
  SINGLE-SOURCE.** The candidate second
  source (the Ancient Pakistan appreciation
  "In the memory of Prof. Farid Khan")
  restates the Bannu Archaeological
  Project's own conclusion, in a memorial
  by project colleagues; a restatement of
  the same research's finding is not an
  independent source under §4.3. The row
  stands SINGLE-SOURCE on Khan et al.
  2010, with the appreciation recorded in
  its `notes`, not counted.
- ter kala dheri was entered SINGLE-SOURCE
  by the same independence reasoning
  applied at entry (Khan et al. 2000
  overlaps the monograph's author team);
  no demotion was needed.
- Every other entered citation was re-read
  against its row: kalibangan (the 2003
  report's concluding assessment, as
  carried in the published record of the
  report — the locator in the row says
  so), mohenjo daro (synthesis §1.6),
  rojdi (Weber 1999, p. 817), piklihal
  (Fuller et al., the Piklihal section),
  sannarachamma and hiregudda (Risch et
  al. 2009, §1 — the same source maps the
  two hills differently because its own
  statements differ: quarry-focused at
  Hiregudda, a settlement hill at
  Sannarachammagudda), tigrana (Parmar et
  al., the site section).

## 5. §4.5 attestation (build discipline)

Dated 2026-10-21. Worker: **Muse Spark (AI agent, via Muse)**,
executing at the direction of Tristen
Pierson.

1. Every class, mapping and status in Asset
   B was derived from the excavation and
   site literature cited in the asset, and
   from nothing else. No class was derived
   from inscription content, sign
   distributions, or per-site inscription
   counts.
2. The gate-0.3 census was computed by the
   phase machinery separately, in a sealed
   run before the asset file existed; its
   per-site figures were not read by the
   classification worker before the freeze
   (only the class totals were printed).
3. **Disclosure.** During input-format
   inspection at the start of the execution
   (before any classification research), the
   worker saw the corpus `site` column's raw
   value frequencies in aggregate (site
   names with record counts, as a format
   check on the pinned file). That sighting
   preceded the classification research, no
   class or status was assigned or changed
   because of it, and the classifications
   were fixed in the research record before
   the sealed census run existed. The fact
   is recorded here so the attestation at
   point 1 is read with it: the build's
   evidence is the cited literature, and
   the census's per-site joined figures —
   the figures the test will use — were
   sealed until after the freeze.

## 6. Ledger-sign list (step 1b, spec §5)

File `specs/047-roif-ledger-distribution/asset-b/ledger-signs.jsonl`,
frozen in the same act. SHA-256:
**`dfa48f50907a3374b45d6270f0ffbed8a2492c5d33c186da36950140b233292b`**
(two foreground routes, as for Asset B).

Extraction, from the two §2.1 postings only:
**13 depicted sign classes were sought**
(the classes Roif's text names in its sign
table and case readings: fish, boat, jar,
horned deity, plough, grid, arrow, scorpion,
animal/livestock, serpent, rodent,
stick-figure/man, wheel). Of these, five
were considered and **not entered**,
because Roif's text assigns them none of
the seven enumerated economic functions:
the scorpion is a "protection marker"; the
serpent an external threat; the rodent
raiders/burglars; the stick-figure/man
granary watch/guards; the wheel is named
only as "transport" inside a translated
sequence. (A further "trade route/water"
entity in Case Study 1 is assigned
"monsoon-dependent trade access" but
appears in no sign sequence of its case
and is not a depicted sign class; it was
likewise not entered.) **8 entered**:
(trade; guild), boat (maritime trade), jar
(storage; tribute), horned deity (guild),
plough (storage; accounting), grid
(accounting), arrow (enforcement), animal
(tribute). **3 mapped** to the primary
layer's numbering through the canonical
sign registry (fish: 18 Mahadevan tokens
from 20 registry rows; jar: 5 from 7;
grid: 4 from 3 — token lists in the file).
**5 UNMAPPED** (boat, horned deity, plough,
arrow, animal), each recorded in the file
with the mechanical registry search that
found no naming description. The pinned §2
crosswalk was consulted for every entry:
it maps Yajnadevam glyph identifiers, not
depicted classes, and originated no
mapping. The all-UNMAPPED case of
DD-047-13 does **not** fire: measure (b)
has three mapped sign classes to run on
when step 2 executes. Extraction was done
without consulting sign counts (§5, §4.5
with the necessary changes).

## 7. What this record does and does not establish

Step 1 establishes: the step-0 gates pass
on the pinned inputs; a site-function
classification of the 30 spine clusters
exists, built and frozen under the frozen
contract, with its disagreements and
absences published in full in the asset;
and a ledger-sign list exists, frozen with
its extraction census. It does **not**
establish anything about Roif's claim: no
distribution quantity was computed, the
classification gate of §6.3 has not been
applied, and the claim stands **UNTESTED**.
No claim in the governed register changed
verdict at step 1; the claim-level outcome
record is task E7's, at step 2.

## 8. Records

- Results JSON: `reports/phase406_results.json`
- Report: `reports/phase406_step1_report.md`
- Asset B: `specs/047-roif-ledger-distribution/asset-b/site-functions.jsonl`
  (digest in the headline)
- Ledger list: `specs/047-roif-ledger-distribution/asset-b/ledger-signs.jsonl`
  (digest in §6)
- Adjudication: `adjudication.md` was
  **not** appended to. Spec 047's freeze
  pins that file byte-for-byte in
  `freeze.json`'s source list (SHA-256
  `081c6961…`), and
  `backend/tests/test_spec047_freeze.py`
  enforces the pin — unlike Specs 039/041,
  whose execution sections live in their
  adjudications, this spec's frozen form
  carries its execution record here, in
  `outcome.md`. This paragraph is the
  record of that reading; the frozen file
  stands byte-identical (verified at
  landing).
- Root LEDGER entry: `LEDGER.md`,
  2026-10-21, Spec 047 step-1 execution
- Anchors: asserted byte-identical before
  and after (`df0cf620…` at both readings)
- Landing record (PR, merge commit, CI,
  foundation check): appended below at
  merge, dated, append-only.

---

*AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*

---

## Landing record — 2026-10-21 (appended at merge; append-only)

- Execution PR: **#266** (branch
  `spec-047-step1-execution`), merged to
  `main` as merge commit
  **`a6004ac378968d24fcf1fafefb4a670a240a0bed`**.
- CI: GitHub Actions run 39608734716 on the
  PR head `5eff05c9` — **7 of 7 jobs
  success**, verified from the run's own
  job conclusions (Backend tests;
  Frontend tests (Playwright); Indus public
  validation checks; Evidence Graph script
  smoke tests; Shell wrappers ubuntu /
  macos / windows).
- The branch carried one merge of `main`
  (Spec 046's execution, PR #263) before
  merging; the two append conflicts
  (LEDGER.md, `experiment_graph.py`) were
  resolved by keeping both programmes'
  entries and both graph registrations,
  and the Spec 046 and Spec 047 test files
  were re-run green on the merged tree
  before the PR was opened.
- Asset and ledger digests re-verified on
  `main` at the merge commit by the
  contents-API route: Asset B
  `a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85`,
  ledger list
  `dfa48f50907a3374b45d6270f0ffbed8a2492c5d33c186da36950140b233292b`
  — identical to the frozen values in this
  record.
- Foundation check (H21) at the merge
  commit, on a fresh clone with the two
  Holdat CSVs copied from the existing
  local downloads (corpus CSV SHA-256
  `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`
  verified first): **40 checks passed, 0
  failed, 8 warnings** — the standing
  figure.
- Tasks E1–E4 stand ticked in `tasks.md`;
  E5–E7 (step 2) remain open for the
  Group-3 execution act. The claim stands
  UNTESTED.

*AI disclosure: appended by an AI agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*

---

# Step-2 record — EXECUTED 2026-10-21 (Phase-406)

> ## STEP 2 — EXECUTED 2026-10-21: INCONCLUSIVE (classification gate)
>
> This record is the step-2 execution act
> (tasks E5–E7), appended to the step-1 record
> above; the step-1 text stands unedited. The
> frozen Spec 047 contract (freeze digest
> `8501feabb7beee621e99ae48529e5a74c0788fb0619ac49c615912e13914cdc7`)
> was executed as **Phase-406**, step 2, in
> Wave 3, Group 3 of the runnable-experiments
> campaign, after the OSF registration b2a8w
> was approved and public. Step 0 was re-run
> and passed in full; Asset B was re-asserted
> at the digest this record's step-1 headline
> pins; and the §6.3 classification gate then
> **fired on both of its clauses** — 2 testable
> sites against the frozen floor of 12, and an
> empty domestic/ritual contrast side in the
> test population. The distribution test did
> not run: no R, no permutation p-value, and
> no R_ledger exists. The outcome is
> **INCONCLUSIVE — the classification is the
> finding**, and the claim stands **UNTESTED**
> for its distribution component, now with the
> reason measured rather than asserted. All
> products are held under the Roif gate
> (spec §10).

## Headline (§9 items)

1. **Corpus label.** The primary layer as
   pinned in spec §2:
   `backend/glossa_lab/data/yajnadevam_inscriptions.csv`
   (5,679 records; the site-attributed layer of
   Specs 027/028), SHA-256
   `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98`.
2. **Asset B.** File
   `specs/047-roif-ledger-distribution/asset-b/site-functions.jsonl`;
   SHA-256 digest over the file bytes as
   committed:
   **`a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85`**
   — re-asserted at step 2, byte-identical to
   the step-1 freeze. Rows: 30. Testable:
   **2** (harappa — administrative; lothal —
   port/trade). Per-status counts: AGREED 3,
   DISAGREED 1, SINGLE-SOURCE 10, NO-SOURCE 16.
3. **Join census (gate 0.3, re-run at step 2).**
   5,679 records, each in exactly one class —
   identical to the step-1 census, value for
   value: joined to a spine cluster 5,106;
   non-spine site 573 over 66 site values (by
   name with counts in
   `reports/phase406_step2_report.md` and
   `reports/phase406_step2_results.json`; the
   two largest are Dholavira 238 and
   Chanhu-daro 74, both outside the population
   by rule, DD-047-12); no site value 0.
4. **Step-2 quantities (§9 item 4).** None.
   The §6.3 classification gate fired at E5,
   before any distribution quantity exists:
   no R, no permutation p-value, no R_ledger,
   and no per-sign ledger counts were
   computed. The ledger-sign list stands as
   frozen at step 1 (SHA-256
   `dfa48f50907a3374b45d6270f0ffbed8a2492c5d33c186da36950140b233292b`;
   extraction census 8 entered, 3 mapped,
   5 UNMAPPED; the DD-047-13 all-UNMAPPED case
   does not fire) — it was re-asserted by
   digest and never joined to a count.
5. **Component fence.** This result concerns
   the distribution component of Roif's ledger
   thesis only; the guild-authority and
   Akkadian-influence components were not
   tested.

## The §7 wording (INCONCLUSIVE, classification)

"The distribution test did not run: 2 of the
gazetteer's 30 sites survived the two-source
agreement rule as testable (floor 12), and one
side of the comparison is empty in the test
population (the pooled ADMIN-TRADE-GATEWAY
side carries both testable sites; the
domestic/ritual contrast side carries none).
The finding of this execution is the
classification itself (Asset B, digest
a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85):
AGREED 3 (of which 1, shahr i sokhta, agreed
at mixed/unknown and excluded by section 4.2),
DISAGREED 1, SINGLE-SOURCE 10, NO-SOURCE 16,
with the disagreed and unclassifiable sites
named in full. No distribution quantity was
computed. The claim stands UNTESTED for its
distribution component, now with the reason
measured rather than asserted."

## 1. What was executed

Step 2 only (tasks E5–E7), under the
graph-first build (H15/H23): phase script
`backend/scripts/phase406_roif_ledger_step2.py`;
graph node `IndusPhase406RoifLedgerStep2`,
added to the phase module
`backend/glossa_lab/experiment_graph_phase406.py`
(the step-1 node stands unchanged beside it);
registration in
`backend/glossa_lab/experiment_graph.py`
(the phase-406 registration loop picks the new
node up from the module; no edit to that file
was needed), verified by import before the
run — both Phase-406 nodes present among 497
registered nodes. The script carries the §6.2
primaries and §6.4 recomputations in the
frozen form behind the gate; the gate fired,
and none of that machinery ran. The run's base
was `main` at
`3e75d7b0707a210598e90df5d92d92253cf9435b`.
The run's own records:
`reports/phase406_step2_results.json`
(SHA-256
`7d0a303fab455c9f0045793dcece275d2e67c7495b98be496a6cc7a073908483`)
and `reports/phase406_step2_report.md`
(SHA-256
`87b6e0a07fc7bdcf27062af4238279566c550e0529db9b2fb81487c3a104137c`)
— the results digest derived twice by
independent routes (`sha256sum` and a Python
`hashlib` recomputation, identical; the
`hashlib` value is the one carried in the
claim append of §7 below), and the script is
deterministic: a second run reproduced both
output files byte-identically.

Before the run, every §2 pin — and both
step-1 digests (Asset B and the ledger-sign
list) — was re-derived in the foreground by
two independent routes (the fresh worktree's
files hashed with `sha256sum`, and the
contents-API raw downloads hashed with Python
`hashlib`, both at the run's base): all ten
values agree with their records.

## 2. Step 0 re-run — gates (spec §3), observed values

- **0.1 Input integrity: PASS.** All eight §2
  inputs hash to their freeze pins (gazetteer
  `5ac76a30…`, corpus `c02e3d7b…`, crosswalk
  `e44b8b55…`, Phase-104 evaluation
  `2d0b83e8…`, seed_citations.py `39d28112…`,
  Roif model file `c5f08461…`, anchors
  `df0cf620…`, Spec 027 spec `7fff5d5a…`; full
  values in `reports/phase406_step2_results.json`).
- **0.2 Spine reproduction: PASS.** 36 rows,
  30 distinct `program_site_id` clusters, the
  frozen cluster list exactly.
- **0.3 Join census: PASS.** 5,679 records
  accounted for exactly once under the §6.1
  normalisation: joined 5,106; non-spine 573
  over 66 site values; no site value 0 —
  identical to the step-1 census in every
  figure, including the per-cluster joined
  counts and the non-spine list (the "Rodji"
  note of the step-1 record stands: 4 records,
  non-spine by the frozen normalisation, no
  hand assignment).

## 3. E5 — the classification gate (spec §6.3), observed values

Checked against the frozen asset before any
distribution quantity exists:

- **Testable count: 2** (harappa —
  administrative; lothal — port/trade), from
  the asset's 3 AGREED rows less shahr i
  sokhta (AGREED at `mixed/unknown`, excluded
  by §4.2). The frozen floor is **12**. The
  floor clause fires.
- **Test population (§6.1):** both testable
  sites carry at least one joined inscription
  — harappa 2,717 joined records, lothal 208
  — so the test population is exactly those
  two sites, and the `NO-CORPUS-COVERAGE`
  list is empty.
- **Sides in the test population:** pooled
  ADMIN-TRADE-GATEWAY **2** sites (both
  testable sites); contrast
  (domestic/ritual) **0** sites — empty. The
  empty-side clause (DD-047-2, confirmed)
  also fires.

Either clause alone ends the execution; both
fired. The outcome under the frozen partition
is **INCONCLUSIVE — the classification is
the finding**. No distribution quantity was
computed, and the claim stands UNTESTED for
its distribution component.

## 4. E6 — primaries and sensitivities: not run

The §6.2 primaries (R, the 9,999-shuffle
permutation test at seed 20261021, R_ledger
with per-sign counts) were not computed: the
classification gate pre-empts them, and
computing them anyway would produce exactly
the unregistered quantities the gate exists
to withhold. Of the §6.4 sensitivities, the
each-source-alone and five-largest
recomputations presuppose a primary test and
are recorded **not run**; the exclusions
restatement, which does not, is published
here in full:

- **DISAGREED (1):** surkotada.
- **SINGLE-SOURCE (10):** hiregudda,
  kalibangan, khirsara, mohenjo daro,
  piklihal, rojdi, sannarachamma,
  sheri khan tarakai, ter kala dheri,
  tigrana.
- **NO-SOURCE (16):** amri, banawali,
  chagylly, desalpur, islam chowki, jhukar,
  joenniemi, kanispur, kunal, mullali,
  ojiyana, qasim bagh, rangpur,
  sheri khan tarakai 3, sheri khan tarakai 4,
  yalangach.
- **AGREED at mixed/unknown (1):**
  shahr i sokhta.
- **NO-CORPUS-COVERAGE:** none (both testable
  sites carry joined inscriptions).

## 5. Standing disclosures carried from step 1 (unchanged)

Step 1's disclosures stand exactly as
recorded in the step-1 record above; this
act does not relitigate, re-read, or alter
any of them, and no asset row was changed:

- **§4.5 attestation disclosure** (step-1
  record §5, point 3): during input-format
  inspection at the start of the step-1
  execution, before any classification
  research, the worker saw the corpus `site`
  column's raw value frequencies in
  aggregate; no class or status was assigned
  or changed because of it, and the census's
  per-site joined figures were sealed until
  after the freeze. The attestation it
  qualifies stands as written there.
- **Verification-pass demotions** (step-1
  record §4): khirsara (AGREED →
  SINGLE-SOURCE; the candidate pair shares
  authorship and fails §4.3 independence) and
  sheri khan tarakai (AGREED → SINGLE-SOURCE;
  the candidate second source restates the
  Bannu Archaeological Project's own
  conclusion). Both demotions were made
  before the step-1 freeze and are recorded
  in the demoted rows' `notes` in the asset.
- **Quoted-source basis** (step-1 record §3
  and the asset's surkotada row): the
  DISAGREED row's source A is Joshi 1990 as
  quoted in Rawat's coastal-sites chapter,
  p. 199, carrying its IAR/Joshi locators —
  entered as quoted verbatim with pagination
  in a published chapter, per the program's
  verification bar for quoted determinations.

This act's own contact with the asset was
mechanical only: digest re-assertion and
re-validation of the §4.1 form and status
mechanics from the committed bytes. No
source was re-read and no row, status, or
class was re-judged.

## 6. Claim consequences (governed register)

Executed under register 0.7-draft (frozen);
one line per claim, F047-C01…C19.

- **F047-C01** (an outcome states only how
  inscriptions distribute across the frozen
  classes): HELD — this record states no
  distribution at all; it records a gate
  closure and the classification finding,
  within the claim's scope.
- **F047-C02** (the claim stands UNTESTED on
  its Phase-104 record under RULE-SITE):
  CHECKED — the Phase-104 record was
  hash-verified at gate 0.1 and stands
  unedited; after step 2 the claim still
  stands UNTESTED for its distribution
  component, with the measured reason
  appended (§7 below).
- **F047-C03** (inscriptions concentrate at
  pooled-class sites within the test
  population): NOT JUDGED — no concentration
  was measured; the gate fired first.
- **F047-C04** (a shares result with no
  excess is recorded NOT SUPPORTED): NOT
  REACHED — no shares result exists for the
  rule to govern; the outcome is not
  NOT SUPPORTED.
- **F047-C05** (only the distribution
  component is tested): HELD — nothing in
  this act touches the guild-authority or
  Akkadian-influence components.
- **F047-C06** (Asset B carries exactly one
  row per spine cluster): CHECKED —
  re-validated mechanically at step 2:
  exactly the 30 spine clusters, in sorted
  order.
- **F047-C07** (every classification uses
  exactly the §4.2 six classes by the stated
  mapping rule): CHECKED — every mapped
  class in the frozen asset is in the
  six-class vocabulary (mechanical
  re-validation of the committed bytes).
- **F047-C08** (test entry requires two
  independent published sources mapping to
  one identical class): CHECKED — the
  testable set re-derived from the asset
  under exactly this rule is the 2 sites of
  §3 above; the step-1 verification pass and
  its demotions stand as recorded (§5).
- **F047-C09** (a non-testable site is listed
  by name under exactly one §4.4 status):
  CHECKED — all 28 non-testable clusters
  stand under exactly one status each, and
  are republished by name in §4 above.
- **F047-C10** (Asset B freezes inside step 1
  under a SHA-256 digest): CHECKED — the
  digest re-asserted byte-identical at
  step 2 before the gate was read.
- **F047-C11** (no Asset B class is derived
  from inscription content): HELD — this act
  derived nothing; it read the frozen
  classes only. Step 1's §4.5 attestation
  and its disclosure stand as recorded (§5).
- **F047-C12** (a failed §4.7 build gate
  leaves Asset B unfrozen): HELD in its gate
  form — no build gate failed at step 1,
  the asset froze, and step 2 proceeded
  against the frozen asset as the claim
  presupposes.
- **F047-C13** (the ledger-sign list is
  extracted in step 1 from the two postings
  of record): HELD — the list stands as
  frozen at step 1, re-asserted by digest;
  its extraction census is republished in
  the headline; it was never joined to a
  count at step 2.
- **F047-C14** (execution stops before the
  build on any step-0 gate failure): HELD in
  its step-2 form — step 0 was re-run in
  order at this act and passed in full (§2);
  no step-0 failure arose to stop anything,
  and no INVALID outcome is recorded.
- **F047-C15** (the distribution test does
  not run below twelve testable sites):
  FIRED as written — 2 testable sites, the
  test did not run.
- **F047-C16** (the verdict follows the §6.3
  partition mechanically): HELD — the
  outcome INCONCLUSIVE (classification) is
  the partition's gate branch, assigned from
  the recorded quantities (testable count 2;
  pooled 2, contrast 0 in the test
  population) by the frozen rule.
- **F047-C17** (the §6.4 sensitivities are
  reported beside the primary in every
  outcome product): HELD in its gate form —
  there is no primary for the recomputations
  to stand beside; they are recorded not run
  (§4), and the exclusions restatement, the
  one §6.4 item that does not presuppose a
  primary, is published in full in §4, the
  step-2 report, and the results JSON.
- **F047-C18** (every record of Spec 047
  stays internal under the Roif gate):
  HELD — every product of this act is an
  internal program record; nothing was
  surfaced on any public surface, and
  campaign reporting names this member only
  as executed — held under the Roif gate.
- **F047-C19** (no outcome establishes a
  ledger entry for any inscription): HELD —
  no such statement appears in any product
  of this execution.

**Anchors.** `backend/reports/INDUS_FINAL_ANCHORS.json`
recomputed before and after the run: SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
at both points — byte-identical, asserted.

## 7. The claim-level append (task E7)

The claim
`indus_valley_script_deciphered_from_myth_65ff0a26_manual_001`
received its dated, component-scoped step-2
append in its record
(`glossa-indus/claims/extracted_claims/indus_valley_script_deciphered_from_myth_65ff0a26.json`,
key `spec047_step2`), carrying the §7 wording
above, the gate values, the Asset B digest,
and the results digest
(`7d0a303f…`). Verified at the act: removing
the appended entry reproduces the pre-act
file byte-identically (pre-act SHA-256
`27661b3c967142329f32cef7af659bb8a172866bb7d87801fbd883127727fcd2`;
post-act
`13829bd7ac66fe3bea76ab7e2b07a5e0fcc37760cccf2af1b9deea1d89dc4772`),
and the claim's `claim_status` (`untested`)
and `stage` (`created`) are unchanged — the
Phase-104 record stands, and this append sits
beside it as a dated entry, per spec §11
limit 4. Nothing was edited or
re-adjudicated.

## 8. What this record does and does not establish

It establishes, on measured values, why the
distribution test cannot run under this
frozen contract: of the gazetteer's 30
clusters, only 2 survived the two-source
agreement rule as testable — below the
floor of 12 the design set for itself — and
both sit on the same side of the comparison,
so the contrast side is empty in the test
population. The finding of the execution is
therefore the classification itself (Asset B),
with its disagreements and absences named in
full. It does **not** establish anything
about the distribution component's merits:
whether inscriptions concentrate at
administrative/trade/gateway sites remains
untested under this contract — unjudged, not
failed on its merits — and it says nothing
either way about the guild-authority or
Akkadian-influence components. Under
DD-047-11 the dependent design D-10 (Spec
051) proceeds under its own gates against
this frozen-but-thin Asset B; this record
changes nothing in the asset it consumes.
A successor test on a wider classification
would be a new act under a new freeze; this
record does not commission one, and nothing
was repaired in-pass.

## 9. Records

- Results: `reports/phase406_step2_results.json`;
  report: `reports/phase406_step2_report.md`
  (digests in §1).
- Graph node: `IndusPhase406RoifLedgerStep2`
  (registered and verified by import before
  the run).
- Execution tests:
  `backend/tests/test_spec047_execution.py`
  (the delivered form pinned: outcome, gate
  facts on both clauses, census identity with
  step 1, the pins, the absence of any
  distribution quantity, the frozen §7
  wording).
- Root LEDGER entry: "Spec 047 step-2
  EXECUTED (Phase-406): INCONCLUSIVE —
  classification gate (§6.3)" added with this
  record.
- Tasks: E5 (classification gate) and E7
  (outcome) stand ticked in `tasks.md`; E6
  (primaries and sensitivities) stands open
  in form and is closed in substance by this
  record — it cannot run under this frozen
  contract, because the gate at E5 fired, and
  any successor is a new act under a new
  freeze.
- `adjudication.md`, `spec.md`, `claims.json`,
  `freeze.md`, and `freeze.json` were **not**
  edited: they are digest-covered sources of
  the freeze (`test_spec047_freeze.py`
  enforces the pins), and the executed-spec
  form records execution here, in
  `outcome.md`. Asset B and the ledger-sign
  list were likewise not edited — digests
  re-asserted, bytes unchanged.
- Local-environment disclosure: in this VM's
  glossa-lab venv, the register-integrity
  tests of the frozen suites
  (`test_spec047_freeze.py::test_register_integrity`
  and `test_spec051_freeze.py::test_register_integrity`)
  fail with a TypeError from the local AEE
  loader (`Claim.from_dict() got an unexpected
  keyword argument 'strict'`). Both were
  verified to fail identically on the pristine
  `main` tree at this run's base with no
  execution changes present — the known
  pre-existing local AEE-loader issue class
  (the same class disclosed on Spec 042's
  record). The step-2 execution tests
  themselves pass in full locally (6 of 6),
  and the PR's CI run is the figure of
  record.
- CI and foundation check (H21) at the record
  merge: appended below after the record PR
  merges — this section is completed by
  append, not edited.

---

*AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution §VI.*

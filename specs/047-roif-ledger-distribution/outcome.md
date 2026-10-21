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

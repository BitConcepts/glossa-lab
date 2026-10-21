# Spec 045 / Phase-411 — Outcome record (EXECUTED 2026-10-21 — INVALID, gate 0.2)

> ## EXECUTED — 2026-10-21
>
> Executed under the frozen Spec 045 contract
> (freeze digest
> `5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`,
> PR #244 merged at `b442b89b`), as **Phase-411**,
> in Wave 3 Group 1 of the runnable-experiments
> campaign (plan approved AS WRITTEN on
> 2026-10-21). The execution gate was satisfied
> before the run: OSF registration **4mt9k** is
> APPROVED + PUBLIC. Under the campaign's Group 1
> execution order — the order the Group 1
> executions of Spec 044 (Phase-404) and Spec 047
> (Phase-406) used — step 0 (spec §6) ran first,
> before the step-1 Asset A build. Outcome:
> **INVALID** — gate 0.2 (positional reproduction)
> failed on observed values. No verdict is
> recorded, Asset A was not built, and the claim
> stands as recorded.

## Headline (spec §5.5 wording, INVALID form)

"Spec 045 stopped before any model quantity:
gate 0.2 (positional reproduction) failed — the
pinned corpus carries 3,463 inscriptions of
length >= 3 against the recorded 2,267; the
40/61/20 strong-sign classes are exhibited by
no record of record (the Phase-43 record
exhibits 10 of its 20 terminal-strong signs and
no initial or medial member list, and states no
position rule, count floor, threshold, or
profiled-set rule); and the corpus the recorded
quantities belong to (the Firestore V3 corpus,
3,137 sequences) is absent from the tree. No
verdict is recorded; the claim stands as
recorded."

Claim:
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001`
— IN QUESTION, partially supported for position
only, unchanged. No model fit, no closing score,
and no Asset A digest exists under this spec;
the §9 headline quantities (Asset A digest and
per-kind counts, both model fits, both closing
scores) therefore do not exist, and this record
says so rather than supplying substitutes. No
gloss is established by this record (spec §8,
limit 1): it states only that the frozen
reproduction gate failed, in plain words — the
test could not be run as written because the
recorded positional result it stands on cannot
be reproduced from the records the programme
holds. Spec 037's census caution — object-type
labels diverging between compilations in 49% of
matched cases — is restated here, as it travels
with every statement under this spec; Asset A's
construction was the design's answer to that
caution, and that construction was never
reached.

## 1. What was executed

Step 0 only (spec §6, gates in frozen order),
under the graph-first build (H15/H23):
experiment script
`backend/scripts/phase411_hunt_depicted_step0.py`;
graph module
`backend/glossa_lab/experiment_graph_phase411.py`
(node `IndusPhase411HuntDepictedStep0`);
registration in
`backend/glossa_lab/experiment_graph.py`; the
registration verified by import in the run
environment before the phase ran (the node is
present in `ATOMIC_NODES`). The script contains
no Asset A entry code, no model code, and no
join code. The run's own records:
`reports/phase411_results.json` (SHA-256
`2a3872953036f1d75ada01f85e43c165ea95976a3111992f4985808a8120b5cd`)
and `reports/phase411_step0_report.md` (SHA-256
`ca5dfb380e1e5a3806d7bf41c7aab9168bac2de8007274c7628c019a2d1ebf17`)
— both digests derived twice by independent
routes (`sha256sum` and a Python `hashlib`
recomputation, identical), and the script is
deterministic: a second run reproduced both
output files byte-identically. The run's base
was `main` at
`cefef0c6c84fe4122b168805e392f64d8b498815`.

## 2. Step 0, gate by gate

- **0.1 Input integrity — PASS.** Every §4
  input recomputes to its freeze pin: the
  positional record `0e546962…`, the Phase-43
  battery record `78a6c219…`, the corpus layer
  `c02e3d7b…` (5,679 records), the crosswalk
  master `4ace1a61…` (205 rows, 187 distinct
  `registry_sign_id` values — the DD-045-18
  census re-derived), and the anchors file
  `df0cf620…` (287 anchors). Each pin was
  verified in the foreground by two independent
  routes — the GitHub contents API and the
  git-data blob API, both at the run's base
  commit — with identical results, and again by
  the phase machinery in the worktree. The
  gate's Asset-A-digest clause is recorded as
  not applicable at step 0: Asset A does not
  exist before step 1, so no asset digest exists
  to recompute; the build gates A1–A6 govern
  the asset if a build is ever reached.
- **0.2 Positional reproduction — FAIL (the
  execution closes here).** The gate requires
  the pinned positional record's quantities to
  be reproduced from the pinned corpus under
  the recorded framework: the 805/2,267 formula
  count and the 40/61/20 strong-sign classes.
  The reproduction attempt was mechanical, in
  five parts, and every part is in the run's
  record:
  - **R1 — the recorded quantities**, read from
    the pinned record itself: 805 of 2,267;
    40 initial-strong, 61 medial-strong,
    20 terminal-strong; mean initial rate 0.757
    against 0.251 expected by chance.
  - **R2 — the pinned corpus's own census.**
    The pinned corpus layer carries 5,679
    records, of which **3,463** are inscriptions
    of length >= 3 under its text field —
    against the recorded denominator **2,267**.
    The denominator does not reproduce on the
    pinned corpus, before any class question is
    reached. No subset rule that could reconcile
    the two numbers is stated in any record of
    record, and none was invented.
  - **R3 — the classes are not exhibitable.**
    The Phase-43 record (§T2_2) states the
    counts 40 / 61 / 20 over 201 profiled signs,
    and exhibits a terminal-strong list of
    **10** entries against its own stated count
    of 20. It exhibits **no** initial-strong or
    medial-strong member list anywhere in its
    structure. Its per-sign role labels (§T2_1,
    20 rows) label 2 signs INITIAL_STRONG, 6
    MEDIAL_STRONG, and 4 TERMINAL_STRONG — a
    fragment, not the classes. The record states
    no position rule (which occurrence counts
    as initial, medial, or terminal; how
    length-1/2 sequences are classed), no count
    floor, no strength threshold, and no rule
    selecting the 201 profiled signs. The
    formula numerator (805) counts inscriptions
    following the structure under those classes;
    with the classes' membership exhibited
    nowhere, the numerator cannot be computed
    from the pinned corpus under any recorded
    framework.
  - **R4 — no recorded framework exists in the
    tree.** A tree scan finds exactly **one**
    Phase-43 path — the results file
    `outputs/phase43_all.json` itself. There is
    no Phase-43 battery script and no methods
    record. The one tripartite code path in the
    tree, `backend/scripts/phase45_t3_hunt_tripartite.py`,
    is a different test (an iconography test over
    the Holdat roles): its own classification
    rule (average position <= 0.25 / >= 0.70,
    minimum count 8), applied by the worker to
    the held Holdat roles file (SHA-256
    `eb6d3b6ae195a2570e098dc6779dbd6c7bea97da5c4714bf406c3bb98f9d2aaf`),
    yields pools of 75 initial / 22 medial /
    5 terminal — not the recorded classes, on a
    corpus the frozen spec does not pin. It was
    not borrowed, and no neighbouring battery's
    constants were substituted.
  - **R5 — the quantities belong to a corpus
    that is absent.** The fuller record of the
    same test, `glossa-indus/reports/model_reports/batch5_analysis_report.json`,
    carries quantities identical to the pinned
    positional record (805/2,267; 40/61/20) and
    names its corpus: "Firestore supplementary
    (2026-05-14)", 3,137 sequences, 2,665
    dockeys, 201 signs profiled — the Phase-43
    corpus (§T1_1: the indusscript.in Firestore
    'indusarrays' source, 3,916 records). That
    corpus is not the pinned corpus layer, and
    its data file — the corpus-v3 loader's dump
    at `glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.jsonl`
    — is **absent from the tree** (no such path
    exists on `main`). This is the same absence
    the freeze-stage records of Spec 049
    (§7.1) and Spec 052 established for this
    battery from their own sides; this record
    re-derived it first-hand against Spec 045's
    own frozen gate, it does not borrow their
    verdicts.
  
  Gate 0.2 therefore fails as written, on three
  independent observed grounds: the denominator
  mismatch (3,463 against 2,267) on the pinned
  corpus itself; the classes' non-exhibition in
  every record of record; and the absence of
  the corpus the quantities in fact belong to.
  No re-scope, substitute battery, borrowed
  constant, or invented threshold was used.
- **0.3 Population census — NOT REACHED.** The
  execution stopped at gate 0.2; no census was
  published as a gate act. (The corpus census
  figures in R2 are gate-0.2 reproduction
  quantities, not a gate-0.3 census, and no
  Asset A coverage exists to restate.)
- **0.4 Freeze-order proof — NOT REACHED.**
  No finding is recorded under this gate.

**A note on measures (DD-045-19), stated so
this closure cannot be misquoted.** Gate 0.2
concerns the *recorded positional classes* —
the 40/61/20 strong-sign classes of the pinned
positional record. It is not a finding about
Spec 045's own §5.2 measure, the **closing
distinct-predecessor rate**, which was never
computed (no model quantity exists), and it
quotes no other spec's closing measure or
result: Spec 054's **Phase-43 terminal-strong
set membership** is a different measure, and
nothing in this record is a result under it.

## 3. Asset A and the D-18 feed

Asset A was **not built**: the step-0 closure
precedes step 1 in the execution order, so
build gates A1–A6 never ran, no sign was
classified, no source volume was opened for
entry, and no `asset-a/` directory, CSV, or
`asset-a-freeze.json` exists. There is
therefore **no Asset A digest** for any
dependent to pin. That consequence is stated
plainly for the coordinator's wave planning:
Specs for D-06 and D-13 consume Asset A by
digest, and no digest exists. (Spec 049, the
D-06 draft, has already recorded its own
freeze failure on the same Phase-43 absence —
its §7.4 named this exact contingency for
Spec 045's gate 0.2.)

The D-18 input state is recorded, not
consumed. Spec 046's delivery,
`specs/046-horned-tiger-concordance/concordance-297.json`,
was re-verified at this run by two routes
(local file and contents API): SHA-256
`772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf`,
schema `glossa.concordance/1`, `signs: []`,
with the `closure` block of its
IDENTIFICATION FAILED (sign unmatched) outcome
— the frozen §6 closure form, an **empty
feed**. Under spec §2.6 and DD-045-17, Asset
A would have proceeded without this feed and
recorded its absence; because no build
occurred, the feed was neither consumed nor
reconstructed from any labels (there are no
labels), and the PARTIAL CONCURRENCE
consumption rule stands in the record with no
rows to consume, exactly as frozen.

## 4. What this outcome does and does not establish

It establishes that Spec 045 cannot be run as
written: its step-0 reproduction gate fails on
the programme's own records, on observed
values stated above. The pinned positional
record remains what it is — a record of its
own test, on a corpus the programme no longer
holds in the tree — and the frozen positional
result stands exactly as recorded (§8, limit
4): the 805/2,267 pattern and the claim's
IN QUESTION status are neither edited nor
re-adjudicated by this closure. It does **not**
establish anything about Hunt's account or the
grammar account: no depicted-kind quantity, no
model fit, and no closing score was computed,
so the discrimination the spec exists to run
remains unattempted — not failed on its
merits, unattempted, because the framework in
front of it cannot first reproduce its own
recorded result. It does not establish that
the recorded quantities are wrong; it
establishes that they are not reproducible
from any record of record the programme
holds. What would unblock a successor is a
record outside this frozen run: the original
Phase-43 battery script or methods record
(position rules, floor, threshold, profiled-set
rule) with the V3 Firestore corpus restored,
or an owner amendment re-scoping the test to
an explicitly defined new battery, honestly
labelled as a new test. This record does not
commission that act, and nothing was repaired
in-pass.

## 5. Claim consequences (governed register)

Executed under register 0.8-draft (frozen);
one line per claim, F045-C01…C17.

- **F045-C01** (an outcome states only whether
  depicted kind discriminates the two accounts):
  HELD — this record states no discrimination
  and nothing about any gloss, meaning, or
  other claim; it records a runnability
  closure only.
- **F045-C02** (the pinned positional record
  gives rate 0.355 against null 0.006, with
  805/2,267 and the 40/61/20 classes): CHECKED
  — the record was read and pin-verified at
  gate 0.1, and its quantities are exactly as
  this claim states; the claim is about the
  record's contents, which stand. (Their
  reproduction is gate 0.2's separate test,
  under F045-C12.)
- **F045-C03** (adding depicted kind improves
  out-of-sample fit by at least the frozen
  margin 0.05): NOT REACHED — no model was
  fitted; the hypothesis is unjudged, neither
  supported nor falsified.
- **F045-C04** (depicted-kind membership
  predicts closing membership better than the
  closing distinct-predecessor rate, by AUC):
  NOT REACHED — neither score was computed;
  unjudged. The measure itself was never
  evaluated, and no other spec's closing
  measure is quoted in its place (DD-045-19).
- **F045-C05** (the §5.5 pre-written
  unfavourable wordings bind any outcome whose
  quantities meet the falsifier's condition):
  HELD — the headline is the frozen §5.5
  INVALID wording with the failed gate and
  observed values filled in; no outcome is
  recorded as support for Hunt's account.
- **F045-C06** (Asset A contains exactly one
  row per sign in the full pinned-crosswalk
  universe): NOT REACHED — Asset A was not
  built; no row exists, and gate A3 never ran.
  The universe it would have covered was
  re-derived at gate 0.1 (205 rows, 187
  distinct sign keys).
- **F045-C07** (every label comes from a held
  published source under the §2.3 hierarchy):
  NOT REACHED — no label was entered and no
  source volume was opened for entry.
- **F045-C08** (Asset A is entered blind to
  positional results): NOT REACHED — no entry
  act occurred; there is no entry to attest
  and no breach to record, and no join was
  made at any point.
- **F045-C09** (disagreeing sources are
  recorded contested with both verbatim
  labels): NOT REACHED — no dispute coding
  occurred; no sign was classified contested
  or otherwise.
- **F045-C10** (Asset A accepts D-18 input
  only as Spec 046's digest-pinned concordance
  file): HELD in its closure branch — the
  D-18 delivery on record is the frozen
  closure form (empty `signs`, `closure`
  block), its digest re-verified at this run
  (§3); it was neither consumed by a build
  (none occurred) nor reconstructed, and its
  absence as a feed is recorded as §2.6
  prescribes.
- **F045-C11** (Asset A is built exactly once
  and frozen with a SHA-256 digest over its
  canonical CSV): NOT REACHED — no asset
  exists and no Asset A digest exists; no
  dependent can pin one, and none may
  re-derive a substitute (the consequence is
  stated in §3).
- **F045-C12** (execution stops before any
  model quantity if any §3/§6 gate fails):
  FIRED as written — gate 0.2 failed and the
  execution stopped there; no model quantity
  was computed past it, and nothing was
  repaired at run time.
- **F045-C13** (the headline outcome is
  exactly one word from the §5.4 verdict set):
  HELD in its stop-class branch — the headline
  is INVALID, a §10 stop class and not a
  verdict word; no verdict word is recorded,
  because no comparison exists to derive one
  from.
- **F045-C14** (rare kinds are pooled as
  `other` only under the frozen pooling rule):
  NOT REACHED — no primary population existed
  and no pooling was performed or needed.
- **F045-C15** (the §5.3 sensitivity is
  reported beside the primary): NOT REACHED —
  there is no primary for a sensitivity to
  stand beside; nothing is reported in its
  place.
- **F045-C16** (no outcome establishes that
  any specific Hunt gloss is correct): HELD —
  no gloss, meaning, or part-reading statement
  appears in any product of this execution.
- **F045-C17** (every statement under this
  spec restates Spec 037's 49% census
  caution): HELD — the caution is restated in
  the headline of this record and in the
  step-0 report, in the form the claim
  prescribes.

**Anchors.** `backend/reports/INDUS_FINAL_ANCHORS.json`
recomputed before and after the run: SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
at both points — byte-identical, asserted.

## 6. Records

- Step-0 record: `reports/phase411_results.json`;
  report: `reports/phase411_step0_report.md`
  (digests in §1).
- Graph node: `IndusPhase411HuntDepictedStep0`
  (registered and verified by import before
  the run).
- Root LEDGER entry: "Spec 045 step 0
  (Phase-411)" entry added with this record.
- Tasks: E4 (graph-first build) and E5
  (step 0) stand ticked in `tasks.md`, E5 with
  its INVALID closure noted; E1–E3 (the Asset
  A build) and E6 (primaries) stand open in
  form and are closed in substance by this
  record — they cannot run under this frozen
  contract, and any successor is a new act
  under a new freeze or an amendment.
- `adjudication.md`, `spec.md`, `claims.json`,
  `freeze.md`, and `freeze.json` were **not**
  edited: they are digest-covered sources of
  the freeze (`test_spec045_freeze.py` enforces
  the pins), and the executed-spec form records
  execution here, in `outcome.md`.
- Local-environment disclosure: in this VM's
  existing glossa-lab venv, the freeze tests'
  `test_register_integrity` (and, for Specs
  046/047, `test_cited_records_carry_the_design_facts`)
  fail with a TypeError from the venv's AEE
  loader version (the conftest's `strict`
  keyword). The failure was verified to occur
  identically on the clean `main` tree with no
  execution changes present — it pre-exists
  this execution, the frozen files are
  byte-identical to `main`, and the same class
  of local-only failure was disclosed on Spec
  044's record. The PR's CI run is the figure
  of record.
- CI and foundation check (H21) at the record
  merge: appended below after the record PR
  merges, in the Spec 047 completion pattern —
  this section is completed by append, not
  edited.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

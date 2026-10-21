# Spec 043 / Phase-410 — Outcome record (EXECUTED 2026-10-21 — PROVENANCE closure at check 0.3)

> ## EXECUTED — CLOSED AT STEP 0, CHECK 0.3 (2026-10-21)
>
> Phase-410 ran under the frozen Spec 043
> contract (freeze digest
> `8a8a334f13577cbb704fc96e6d4c0451cb1277a3470b90c98b3f86c362475987`,
> freeze PR merged at `a679448d`), as
> **Phase-410**, in Wave 3 Group 2 of the
> runnable-experiments campaign (plan approved
> AS WRITTEN on 2026-10-21; that approval is
> this member's execution authorization,
> `adjudication.md` §7.6). The execution gate
> was satisfied before the run: OSF
> registration **vmcra** is APPROVED + PUBLIC
> (parent-verified). Under the frozen order,
> the step-0 provenance adjudication (check
> 0.3) ran FIRST, before any Phase 5 lookup.
> Outcome: **PROVENANCE — CANNOT BE RUN AS
> WRITTEN**, unscored. All three limbs of the
> provenance gate failed on the produced
> documents. No Phase 5 assignment was looked
> up for any sign, and no scoring figure
> exists. PRED-2026-012 remains unscored; its
> §3 Outcome stands **PENDING**.

## Headline (spec §7 wording, provenance-closure form)

"PRED-2026-012 was not scored under Spec 043:
PROVENANCE — CANNOT BE RUN AS WRITTEN at step
0, check 0.3. The produced documents state a
positional basis for the class and for the
signs: Fuls 2013 (§2) records that Wells
classifies signs "according to their
preferred text position" and (§3.7) that the
Initial Cluster Terminal Marker signs are so
called "since they mark the end of initial
clusters"; Wells' published sign list (Wells
2015, ch. 3) gives the ICTM class exactly
three members — signs 060, 001, and 002 — and
assigns the builder table's ITM signs
otherwise (817, 820, and 861 as initial
signs, 820 also as a terminal marker, 740
terminally), while neither produced document
states any basis for W231 (P056) at all. The
ITM population was fixed (4 signs) and no
Phase 5 assignment was looked up. The
prediction remains unscored; its §3 Outcome
stands PENDING. (PRED-2026-007's §3 Outcome
stands PARTIALLY CONFIRMED as its own
pre-execution record, untouched.) This
closure records what the classification's
assignments rest on; it is not a verdict on
the criterion and not a refutation."

## 1. What was executed

Step 0 only (spec §4, checks in the frozen
order), under the graph-first build
(H15/H23): experiment script
`backend/scripts/phase410_pred012_step0.py`;
graph module
`backend/glossa_lab/experiment_graph_phase410.py`
(node `IndusPhase410Pred012Step0`); registration
in `backend/glossa_lab/experiment_graph.py`,
verified by import in the run environment
before the phase ran (the node is present in
`ATOMIC_NODES`). The run's base was `main` at
`3200b7b5b6841a7b9567a81368bf84004fd17255`, in
a fresh isolated clone; the stale local
checkout was never touched. The run's own
records: `reports/phase410_results.json`
(SHA-256
`0a9391b6032bd5902f941190c61d4b41cc608833e6bc601ddd74e13d85d5af67`)
and `reports/phase410_step0_report.md`
(SHA-256
`638405d8557ea77a0760efc1c217f6010da59407f570238d3a3e4b11115681bb`)
— both digests derived twice by independent
routes (`sha256sum` and a Python `hashlib`
recomputation, identical), and the script is
deterministic: a second run reproduced both
output files byte-identically. The step-0
record's own SHA-256 is
`019c65991835505c7f8ecac11e3b62f5b01b1fe825bed3c46eb23fdb2879c948`;
the enumeration's SHA-256 is
`4311bd96d0b81b6d839c291f80dad724e7c9b179bf6b6a39f8b57716e9d4d77c`.

## 2. Step 0, check by check

- **0.1 Sources and pins — PASS.** Every
  source of spec §4 was present and hashed to
  the frozen record's pin, re-derived in the
  foreground by two independent routes (the
  worktree files and the GitHub contents API
  at the run's base commit, identical):
  registry `8a0b2a82…`, cross-check
  `8c2bd605…`, builder `4af822f1…`, parser
  `9b57f0ec…`, recorded clustering
  `623a787d…`, characterisation `54ebf660…`,
  and the register at its frozen value
  `254ccf03…`. The PRED-2026-012 entry was
  located standing as registered: criterion
  verbatim, registered 2026-10-21, Outcome
  PENDING.
- **0.2 Enumeration, re-derivation,
  cross-check — PASS.** The mechanical read
  of the registry's `icit_function` over all
  **803 rows** reproduced the draft census
  exactly: 791 uncoded, **12 coded** (ITM 4,
  LOG 2, NUM 2, TMK 2, SHN 1, SYL 1);
  **ITM = {P056, P324, P378, P385}**,
  population 4. The re-derivation check —
  the pinned builder rule (`_WELLS_FUNCTIONS`,
  first matching key in table order over each
  row's split `wells_ids`) applied to all 803
  rows — agreed with the recorded column
  **exactly, zero mismatches** (the table's
  W585 ITM key matches no row). No sign
  carries conflicting codes within the
  primary. Held-record verification passed:
  P385 and P378 are enumerated ITM; P098
  carries no code and is not ITM. The
  cross-check was read over the whole file
  (611 records: **579 empty, 32 free-text
  glosses, no ITM and no LOG values**) —
  exactly the state Spec 038's execution
  record established — and every
  disagreement with the enumeration is
  written sign-by-sign into the step-0
  record (the twelve coded signs read "no
  record" or "empty value" in the
  cross-check; P098 reads no-code / no-record).
  All disagreements are of the expected kind;
  there is no unexplained discrepancy, and
  none moved membership (the primary
  governs, DD-043-1).
- **0.3 The provenance gate — FAIL; the
  study closes here.** The evidence set was
  produced in full. D1 (the pinned builder)
  and D2 (the pinned parser, with its test)
  were read mechanically: the builder's
  table carries the comment "Known ICIT/Wells
  sign function assignments (from ICIT docs +
  Fuls 2013)", six ITM keys (W740, W585,
  W820, W817, W861, W231; W740 glossed
  "Initial Cluster Terminal Marker"), and its
  summary cites "Fuls 2013 paper: NWSP method
  reference + sign function taxonomy"; the
  parser reads a positional classification and
  a function classification off the same
  catalog line under the annotation "Function
  classification (from Wells)", and its test
  fixture ("Sign 342: frequency 580, terminal,
  TMK") reads all three at once. D3 and D4
  were produced from the programme's held
  cleaned texts, pinned at execution by
  SHA-256, each hash derived by two
  independent routes with identical results:
  D3, Fuls 2013, "Positional Analysis of
  Indus Signs" (`9ed24098…`), and D4, Wells
  2015, "The Archaeology and Epigraphy of
  Indus Writing" — whose chapter 2 presents
  the Wells 2011 sign list and whose chapter
  3 defines the ICTM class (`62acf855…`).
  Every basis statement quoted below was
  verified against the pinned text by
  normalised search in the run's machinery
  (all thirteen quoted statements verified).
  The three limbs, determined under the
  freeze standard (DD-043-10: a basis counts
  only if stated in words, with a locator;
  silence is failure):

  1. **Class-definition limb — FAIL.** The
     produced documents state what the class
     is, and the stated definition is a
     positional one. D3, §2: "B. Wells
     classifies some signs **according to
     their preferred text position** as
     Initial signs (INS), Terminal Marker
     (TMK), and Post-Terminal Marker (PTM)."
     D3, §3.7: Wells (2006) calls signs 1, 2,
     and 60 "Initial Cluster Terminal Marker
     (ICTM), **since they mark the end of
     initial clusters**." D3, §2 states the
     method in terms: "The distribution of a
     sign position can be used to evaluate
     possible sign functions." D4, ch. 3
     defines the ICTM by the same
     cluster-final role. D4's further
     suggestion that ICTMs may be grammatical
     elements (case, mode, tense, gender,
     clitics, post-positions) is a hypothesis
     about what an already positionally
     delimited class might mean; it is not a
     stated definition of the class and not a
     basis of any assignment, and under
     DD-043-10 it cannot be counted as one.
  2. **Per-sign basis limb — FAIL.** For
     each sign, the only basis the produced
     documents state is positional, and for
     one sign they state none:
     - **P056 (W231):** no basis stated at
       all. Sign 231 does not occur in D3;
       in D4 the only "231" is a token count
       ("n = 231"). Silence is failure under
       the frozen standard.
     - **P324 (W740):** D3, §2 — "some signs
       like sign 740 are **mostly located in
       the terminal position** of texts"; D3,
       §3.2's terminal-marker discussion
       ("not terminal as sign 740"); D4,
       ch. 6 — sign 740 is a terminal marker
       (TM) whose assigned value is "found in
       terminal contexts". The basis is
       terminal-position distribution.
     - **P378 (W820):** D3, §3.1 lists 820
       among the "Initial signs 692, 817, 820,
       861, and 921", and §4 calls it "a
       typical sign in **initial position**";
       D4, ch. 3 makes it a Set 1 initial sign
       and ch. 6 states "sign 820 is a
       **terminal marker**". The bases are
       positional throughout.
     - **P385 (W817, W861):** D3, §3.1 lists
       both among the Initial signs; D4,
       ch. 3 makes both Set 1 initial signs
       ("most frequently found in IC and very
       often are the only sign right adjacent
       to ICTMs"), suggests they are
       logographs, and says of 861 that it is
       "most often a single sign initial
       cluster". The basis is initial-cluster
       distribution.
  3. **Source-agreement limb — FAIL.** D4,
     ch. 3: "**There are only three ICTMs
     used in Indus texts: Sign 060, Sign 001,
     Sign 002**" — none of them a builder
     ITM key. The published documents assign
     the four ITM signs different functions
     (initial signs; logographs; terminal
     marker) and omit W231 where the builder
     table asserts ITM. Under the limb's own
     wording, a published list that assigns
     any of the four a different function —
     or omits it where the table asserts it —
     is a gate failure.

  Any one limb's failure closes the whole
  study; here all three fail, independently.
  No subset verdict exists under this design,
  and none was taken. **The LOG trace** was
  run through the same evidence set and is
  recorded in the step-0 record in the same
  form; it gates nothing (DD-043-12). Its
  findings: for **P217 (W520)** the builder
  states LOG with no gloss, D3 states no
  per-sign basis, and D4, ch. 6 calls sign
  520 "the other common **TM**" — a different,
  positional class; for **P310 (W700)** the
  builder glosses "Logogram (most common at
  Harappa)", D3 states no per-sign basis, and
  D4, ch. 4–5 posits sign 700 with stroke
  numerals as "various values in the Indus
  volumetric system", stating no per-sign LOG
  assignment.
- **0.4 Recorded Phase 5 output verification
  — NOT RUN.** The frozen order reaches this
  check only behind a passed gate. The
  recorded clustering and characterisation
  were byte-hashed at check 0.1 for integrity
  and never opened for assignments; the
  sanity anchor was not reproduced because
  the check that reads it was never reached.
  **No Phase 5 assignment was looked up for
  any sign** — the step-0 record states this
  mechanically (`phase5_output_opened:
  false`).

## 3. Scoring (reached only if step 0 passes in full)

**NOT REACHED — step 0 closed the study at
check 0.3.** No per-sign scoring table is
produced (it is a scoring artifact,
F043-C13); no coverage, share, or verdict
exists. The mechanical verdict rule was never
applied, because the gate that precedes any
Phase 5 lookup failed. The step-0 record
carries, in the table's place, the full coded
census and the gate's per-sign provenance
record.

## 4. What this outcome does and does not establish

This closure establishes, from documents,
what the registry's ITM assignments rest on:
a Wells-lineage classification that its own
published sources define by positional
behaviour — classification "according to
their preferred text position", a class named
for marking the end of initial clusters — and
whose published per-sign assignments do not
agree with the programme's builder table for
any of the four enumerated signs. Scoring the
registered criterion over that population
would therefore have measured the
classification's agreement with its own
construction — the circularity threat spec
§3.2 states — and the frozen gate exists
precisely to stop that measurement from
being reported as a verdict. The closure
establishes nothing about the criterion's
truth: no ITM sign was scored, so the 70%
question stands exactly where the register
left it. It does not establish what ITM signs
mean, that Wells' classification is wrong in
its own terms (its classes are honestly
positional in its own pages; the defect is in
the builder table's transcription of them as
position-independent function codes, and in
its selection of signs), or that an
independent classification would fail the
criterion. The clustering-stability caveat
(F043-C16) has no verdict to attach to, and
this closure does not rest on the Phase 5
clustering at all — the clustering output was
never read. The closure is recorded as
itself, under its own name, never as a
verdict, and is not a refutation of
PRED-2026-012 or of PRED-2026-007.

## 5. Claim consequences (governed register)

- **F043-C01** (a verdict states only whether
  the registered criterion is met, and
  nothing beyond): HELD — no verdict is
  stated; this record states a provenance
  closure only.
- **F043-C02** (the criterion is the
  registered one, carried verbatim; no band;
  small-population arithmetic stated wherever
  the share is stated): UPHELD — the
  registered criterion governed the run and
  was never edited; it was never applied to
  a share, because none exists, and no share
  is stated anywhere in this record.
- **F043-C03** (the population is every
  distinct sign the pinned registry codes
  exactly ITM; the CGSA file is cross-check
  only, its disagreements published
  sign-by-sign and never moving membership):
  EXECUTED as stated at check 0.2 — the
  enumeration, census, and sign-by-sign
  cross-check disagreements stand in the
  step-0 record.
- **F043-C04** (the column is exactly
  re-derivable from the pinned builder rule
  over all 803 rows; failure closes as
  CANNOT BE RUN AS WRITTEN): EXECUTED —
  re-derivation exact, zero mismatches; the
  closure branch did not fire.
- **F043-C05** (the population is listed at
  draft and step 0 must reproduce it exactly;
  the census branch cannot arise): FIRED in
  its verification branch — the
  re-enumeration reproduced the listed
  population exactly (P056, P324, P378,
  P385); no census completion is claimed.
- **F043-C06** (P098 excluded by rule; the
  register's 67% denominator defect not
  reproduced; its "(LOG)" parenthetical not
  relied on): HELD — P098 carries no code in
  the primary, was verified not-ITM at check
  0.2, and entered no computation.
- **F043-C07** (the LOG set is enumerated;
  no LOG quantity is scored, per DD-043-12):
  HELD — P217 and P310 stand in the census
  and in the gate's LOG trace; no LOG share
  was computed and the trace gated nothing.
- **F043-C08** (no Phase 5 assignment is
  looked up before the provenance gate has
  passed; the gate runs in the fixed order,
  fail-closed): FIRED as written — the gate
  ran at check 0.3, after the population was
  fixed and before any Phase 5 read; no
  assignment was looked up at any point,
  the sanity anchor included.
- **F043-C09** (the gate is documentary and
  three-limbed; a positional or unstated
  basis, non-production, or source
  disagreement closes the study as
  PROVENANCE — CANNOT BE RUN AS WRITTEN,
  unscored; no subset verdict): FIRED — all
  three limbs failed on the produced
  documents, and the study closed under that
  name, unscored, with the quoted basis
  statements and locators in the step-0
  record.
- **F043-C10** (every outcome statement
  carries the lineage boundary): HELD — §4
  and the headline carry it: this closure is
  a statement about the Wells-lineage
  classification's provenance, not about the
  signs' true functions or meanings.
- **F043-C11** (scoring reads the recorded
  Phase 5 output only; no re-clustering; a
  failed anchor closes as CANNOT BE RUN AS
  WRITTEN): NOT REACHED — check 0.4 never
  ran; the output was byte-hashed at check
  0.1 and never read, and nothing was
  re-clustered.
- **F043-C12** (the coverage rule): NOT
  REACHED — no share or coverage was formed.
- **F043-C13** (the per-sign table is
  published with the outcome as a
  descriptive record): NOT PRODUCED as a
  scoring artifact — the step-0 record
  carries the full coded census and the
  gate's per-sign provenance table in its
  place, and §2 above publishes both.
- **F043-C14** (the outcome is appended to
  the register as a dated entry; the §3 text
  is never edited; the Phase D pin is
  advanced by name): DONE in this same act —
  see §6.
- **F043-C15** (step-0 closures are reported
  as themselves, under their own names,
  never as verdicts; a closure is not a
  refutation): FIRED — this record and the
  register's dated §6 entry report the
  closure as PROVENANCE — CANNOT BE RUN AS
  WRITTEN; PRED-2026-012's §3 Outcome stays
  **PENDING** and PRED-2026-007's stays
  **PARTIALLY CONFIRMED**, per spec §8; §4
  gains no entry.
- **F043-C16** (every outcome statement
  carries the clustering-stability caveat):
  HELD — no verdict exists for it to attach
  to, and the closure does not rest on the
  clustering, which was never read.

## 6. Records

- Step-0 record: `reports/phase410_results.json`
  (step-0 record SHA-256
  `019c65991835505c7f8ecac11e3b62f5b01b1fe825bed3c46eb23fdb2879c948`;
  enumeration SHA-256
  `4311bd96d0b81b6d839c291f80dad724e7c9b179bf6b6a39f8b57716e9d4d77c`);
  report: `reports/phase410_step0_report.md`
  (file digests in §1).
- Register append, in this same act: the
  dated §6 outcome entry recording this
  closure under its own name (spec §8). The
  §3 entry is left standing as registered —
  Outcome PENDING — per the closure handling;
  no second provenance reconciliation is
  appended (DD-043-9: DD-038-2's note stands;
  the entry cites it and adds this gate
  finding). The Phase D register-hash pin is
  advanced by name for this authorised append
  (`backend/tests/test_spec029_phase_d.py`).
- Root LEDGER entry: appended in this same
  act.
- Graph node: `IndusPhase410Pred012Step0`
  (registered and verified by import before
  the run).
- Tasks: E1 (graph-first build), E2 (check
  0.1), E3 (check 0.2), and E4 (check 0.3,
  the provenance gate) stand ticked in
  `tasks.md`, E4 with its PROVENANCE closure
  noted; E5 (check 0.4) and E6 (scoring)
  stand open in form and are closed in
  substance by this record — they cannot run
  under this frozen contract behind a failed
  gate, and any successor is a new act under
  a new freeze. E7 (outcome) is this record.
- `adjudication.md`, `spec.md`, `claims.json`,
  `freeze.md`, and `freeze.json` were **not**
  edited: they are digest-covered sources of
  the freeze (`test_spec043_freeze.py`
  enforces the pins), and the executed-spec
  form records execution here, in
  `outcome.md`.
- Foundation check (H21) and suite state:
  verified on this record's pull request —
  the CI backend job is the full-suite
  verifier, and the foundation check is
  measured at the merge commit; both are
  reported with the merge, not asserted here.
- Every other prediction's record is not
  touched by this completion.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

---

## Landing record — 2026-10-21 (appended at merge; append-only)

- Execution PR: **#278** (branch
  `spec-043-phase410-execution`), merged to `main`
  as merge commit
  **`6b05130bbae47f6ea526e0225f0051fbefd2216a`**.
  Two merge resolutions were required against
  parallel Wave 3 merges (Spec 055 / Phase-414 and
  Spec 058 / Phase-420): in each case only the
  append seams conflicted — the LEDGER tail and
  the experiment-graph registration anchor — and
  each was resolved by keeping both executions'
  entries and registration blocks, with the
  register file and its Phase D pin verified
  unchanged (`a8531efd…`) after each resolution.
- CI: GitHub Actions run **39631757006** on the
  PR head `88b0bd5b` — **7 of 7 jobs success**,
  verified from the run's own job conclusions
  (Backend tests (pytest); Frontend tests
  (Playwright); Indus public validation checks;
  Evidence Graph script smoke tests; Shell
  wrappers ubuntu / macos / windows). The two
  earlier heads also ran green (`a32c4902`, run
  39628872370, 7/7; `6220a353`, run 39630295420,
  7/7).
- Run digests re-verified on `main` at the
  merge commit by two routes (the git object at
  the merge commit and the contents API):
  `reports/phase410_results.json`
  `0a9391b6032bd5902f941190c61d4b41cc608833e6bc601ddd74e13d85d5af67`,
  `reports/phase410_step0_report.md`
  `638405d8557ea77a0760efc1c217f6010da59407f570238d3a3e4b11115681bb`
  — identical to the values in §1 of this
  record.
- Foundation check (H21) at the merge commit,
  on a fresh checkout of `6b05130b` with the two
  Holdat CSVs copied from the existing local
  downloads (corpus CSV SHA-256
  `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`
  verified first): **40 checks passed, 0
  failed, 8 warnings** — the standing figure.
- Terminal outcome stands as recorded above:
  **PROVENANCE — CANNOT BE RUN AS WRITTEN** at
  step 0, check 0.3. PRED-2026-012 remains
  unscored, its §3 Outcome standing PENDING;
  PRED-2026-007's PARTIALLY CONFIRMED stands
  untouched.

*AI disclosure: appended by an AI agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*

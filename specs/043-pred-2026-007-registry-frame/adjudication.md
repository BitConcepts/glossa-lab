# Spec 043 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has one adjudication input, recorded here
> so the draft's basis is inspectable:
>
> **The owner's order of 2026-10-21**: "Do the
> successor" — given in chat after the design-portfolio
> triage of 2026-10-21
> (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`)
> reported that a corrected successor for Spec 038 is
> concretely possible (the cross-check registry does
> carry the function codes) but would need its own
> owner order and must face the codes' Wells-derived
> provenance (DD-038-2).
>
> The order commissions this **draft**. It is not a
> freeze order and not an execution order: the freeze
> (lifecycle hooks, the decisions of §4, a digest, a
> phase allocation) and the execution remain separate
> owner gates, as with Specs 036–042. Drafts are
> standing pre-approved.

## 1. The adopted basis (operative substance)

- **The prediction.** PRED-2026-007 (H4: ICIT
  Function Alignment), registered 2026-04-22 in
  `docs/PREDICTION_REGISTER.md` §3. Prediction:
  "Signs with ICIT function code ITM will cluster
  into TERMINAL class in CGSA Phase 5 at rate ≥
  70%." Success criterion (operative): "≥ 70% of
  ITM-coded signs are TERMINAL or cluster in
  TERMINAL clusters". Recorded partial test: P385
  (ITM) Cluster 21 TERMINAL; P378 (ITM) Cluster 39
  TERMINAL; P098 (LOG) Cluster 10 INITIAL — "2/3
  ITM in TERMINAL (67%)"; Outcome PARTIALLY
  CONFIRMED. The 2/3 denominator mixed a non-ITM
  sign into an ITM-only criterion (DD-038-1,
  carried).
- **The predecessor's closure.** Spec 038 (design
  D-31; freeze digest `b54571d8…`; executed
  2026-10-20) closed at its step 0.2 as CANNOT BE
  RUN AS WRITTEN, unscored: its frozen population
  frame named `reports/indus_cgsa_cluster_analysis.json`
  `data.a[].icit_function` as the primary source of
  the ITM codes, and that field is uncoded (611
  records: 579 empty, 32 free-text glosses, no ITM
  and no LOG values; P385's record empty; P378
  absent). The register's §6 entries of 2026-10-20
  record the closure and the DD-038-2 provenance
  reconciliation. PRED-2026-007 stands PARTIALLY
  CONFIRMED as its pre-execution record.
- **The repair this draft makes.** The successor
  scores the same prediction under its frozen
  criterion with corrected machinery: the canonical
  sign registry — Spec 038's cross-check — as
  primary source, its coded values verified in full
  at draft, its population listed in the draft, a
  re-derivation gate on the column that defines
  the population, and a documentary provenance
  gate (spec §3, §4 check 0.3) on what the ITM
  assignments rest on. The scoring side (recorded
  Phase 5 output, DD-038-9's cluster-class rule,
  DD-038-4's coverage rule) is carried from Spec
  038 unchanged in substance.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
against `main` at `82b29490` (content fetched via
the GitHub API; the stale local checkout was never
touched):

- **The register.** `docs/PREDICTION_REGISTER.md`
  at SHA-256 `f281bd67…`: the §3 PRED-2026-007
  entry stands as quoted in §1 (criterion, Tested
  note, PARTIALLY CONFIRMED outcome); the §6
  entries of 2026-10-20 record Spec 038's closure
  at step 0 and the DD-038-2 provenance
  reconciliation (codes parsed by
  `fuls_parser.py` from Fuls 2023 catalog lines,
  "Function classification (from Wells)" — not
  mayig features).
- **The primary source.** `data/crosswalks/canonical_sign_registry.csv`
  hashes to `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420`
  — the same value Spec 038's freeze cited for it
  as cross-check. 803 rows; columns include
  `parpola_id`, `wells_ids`, `icit_function`.
  Mechanical census of `icit_function` over all
  803 rows: **791 empty; 12 coded** — ITM 4
  (P056/W231, P324/W740, P378/W820,
  P385/W817|W861), LOG 2 (P217/W520, P310/W700),
  NUM 2 (P058, P316), TMK 2 (P086, P332), SHN 1
  (P122), SYL 1 (P009); LON 0. Each coded sign has
  exactly one coded row; every coded row carries
  at least one Wells ID. **P098's row (W400|W402)
  carries an empty `icit_function`** — no code at
  all (DD-043-5).
- **The builder and the re-derivation.**
  `scripts/cgsa_pipeline.py` hashes to
  `4af822f1ad5c924defed7852df967f8633899b27a27fdaea84e2cdad8744efb0`.
  Its Phase 3 `build_canonical_registry` populates
  `icit_function` from the literal table
  `_WELLS_FUNCTIONS` (comment: "Known ICIT/Wells
  sign function assignments (from ICIT docs + Fuls
  2013)"; 14 keys: ITM W740/W585/W820/W817/W861/
  W231, LOG W700/W520, NUM W233/W706, TMK W760/
  W407, SHN W002, SYL W100; glosses include W740
  "Initial Cluster Terminal Marker", W760
  "Terminal Marker", W407 "Fish terminal", W700
  "Logogram (most common at Harappa)"), by
  first-match in table order over the row's split
  `wells_ids`. The script's summary cites "Fuls
  2013 paper: NWSP method reference + sign function
  taxonomy". **Re-derivation check run at draft:**
  the pinned rule applied to the registry's own
  `wells_ids` column reproduces all 803 recorded
  `icit_function` values exactly (zero mismatches
  under both the membership reading the builder
  uses and a substring reading); the table's W585
  ITM key matches no registry row.
- **The parser.** `backend/glossa_lab/data/fuls_parser.py`
  hashes to `9b57f0ecc10905c0746f1e7fb8e0622ac18e3b08e62bb2eb34fbec4bbd8ef615`
  — the value Spec 038's record cites.
  `parse_sign_catalog_entry` extracts from one
  catalog line a frequency, a positional
  classification (searching for "initial",
  "terminal", "medial", "post-terminal"), and a
  function classification under the comment
  "Function classification (from Wells)" over the
  code list NUM, LON, SHN, TMK, ITM, LOG, SYL. Its
  test (`backend/tests/test_fuls_parser.py`)
  parses the fixture line "Sign 342: frequency
  580, terminal, TMK" into all three at once — the
  same-line juxtaposition spec §3.2 names.
- **The scoring side (pins only).**
  `reports/indus_cgsa_cluster_analysis.json`
  hashes to `8c2bd605…`, `outputs/analysis/sign_clusters.json`
  to `623a787d…`, `reports/cluster_characterization.md`
  to `54ebf660…` — each equal to the value Spec
  038's freeze cited and its execution verified.
  **No content of the clustering or the
  characterisation was read at draft**: no Phase 5
  assignment was looked up for any sign beyond the
  three the register itself names (P385, P378,
  P098). The cross-check file's contents are taken
  from Spec 038's execution record, not re-read.
- **Not done at draft, stated plainly.** No
  share, coverage figure, or verdict exists. The
  provenance gate has not been run and no D3/D4
  document has been produced or adjudicated. The
  computations performed are exactly two
  population-side design inputs — the registry
  census and the re-derivation check — disclosed
  here and in spec §2 because the corrected frame
  requires the population to be listed in the
  draft.

## 3. Draft-fixed readings (DECIDED-BY-DRAFT — stand unless the freeze overturns them openly)

- **DD-043-1 — The registry is primary; Spec
  038's source roles are reversed, on
  verification.** DD-038-5 named sources before
  enumeration to prevent table-shopping; its own
  frame then failed because naming was not
  verification (the primary was verified by form
  only). This draft names the registry primary
  because its values were read in full and
  re-derived at draft (spec §2, §4 check 0.2).
  The CGSA analysis file is cross-check only: its
  disagreements are expected in kind (uncoded
  field), published sign-by-sign, and move
  nothing; ambiguity within the primary itself
  closes the study.
- **DD-043-2 — The re-derivation gate.** Step 0
  re-derives all 803 `icit_function` values from
  the pinned builder rule over the registry's own
  Wells IDs; any mismatch closes the study as
  CANNOT BE RUN AS WRITTEN. A population defined
  by a column must be able to account for the
  column (spec §4, check 0.2).
- **DD-043-3 — The census is published at draft;
  the census branch is foreclosed.** The
  population is listed in spec §2 (four ITM
  signs, two of them never tested), step 0 checks
  the frozen files against the list, and D-31's
  census completion cannot arise.
- **DD-043-4 — The provenance gate and its
  closure name.** Evidence set D1–D4, three limbs
  (class definition; per-sign basis; source
  agreement), fail-closed on any single sign, and
  the distinct closure **PROVENANCE — CANNOT BE
  RUN AS WRITTEN** (spec §4, check 0.3). The gate
  is documentary: it judges stated bases in
  produced documents with locators, and its
  determination is recorded with the quoted
  statements so it is checkable in its turn.
- **DD-043-5 — P098's code is flagged, not
  harmonised.** The register's "(LOG)"
  parenthetical is not reproduced in this frame:
  the pinned registry gives P098 no code, and the
  characterisation's Cluster 10 line counts one
  LOG among members P098 and P217 — that LOG is
  P217 under the registry. The design relies only
  on the pinned sources: P098 is not ITM and is
  excluded by the inclusion rule.
- **DD-043-6 — This spec scores PRED-2026-007
  itself; no new PRED number.** Spec 038's
  register entry says a future test requires "a
  population frame whose coded values are verified
  in the named primary source itself before the
  design is frozen, registered as a new prediction
  under a new PRED number." The verification
  requirement is satisfied by construction (the
  frame's coded values are verified in the named
  primary source at draft, before any freeze).
  Under the owner's successor order, the
  new-number clause is read as addressed to tests
  that would change the prediction; this successor
  changes no word of the prediction, its bar, or
  its population definition. Recorded openly here
  and put to the freeze for confirmation (§5):
  if the freeze declines the reading, the design
  retires unscored and a successor prediction may
  be registered instead.
- **DD-043-7 — Carried from Spec 038 (DD-038-3,
  DD-038-9).** The Success criterion governs over
  the Prediction sentence, operative reading =
  the sign's recorded cluster's recorded class is
  TERMINAL; the cluster-class rule is the recorded
  characterisation lookup — deterministic, no
  threshold invented, classes never derived from
  rates at execution.
- **DD-043-8 — Carried from Spec 038 (DD-038-4).**
  The coverage rule (assigned-population
  denominator, stated coverage, decisiveness
  exception, 80% partial-scope floor) is adopted
  in substance and flagged as the design's, not
  the register's.
- **DD-043-9 — No second provenance
  reconciliation.** DD-038-2's appended note
  stands as the register's provenance record; the
  execution appends its outcome entry and gate
  finding only.

## 4. Open for the freeze (OPEN — not decided by this draft)

- **DD-043-10 — The provenance gate's borderline
  evidence standard.** The gate's mechanics are
  fixed (DD-043-4). Open: how explicit a stated
  basis in a produced document must be to count as
  stated, and who adjudicates a borderline
  document. Draft recommendation: a basis counts
  as stated only if the document states it in
  words, with a locator, for the class or the
  sign; inference from a class's name, from the
  builder table's glosses, or from the
  classification's general reputation does not
  count; borderline calls are recorded in the
  step-0 record with the quoted text. Silence is
  already fixed as failure.
- **DD-043-11 — A spec-level OSF registration.**
  Specs 032–039 each filed their own OSF contract
  registration at freeze; PRED-2026-007 predates
  that practice and has none. Proposal: file this
  frozen spec's own OSF contract registration,
  following the house pattern. This draft files
  nothing.
- **DD-043-12 — The LOG class's role.**
  Enumerated-only (this draft's design), or scored
  as a control class: its TERMINAL share computed
  under the same recorded-output rule and
  published as a descriptive contrast carrying no
  criterion and moving no verdict, with the
  gate's LOG trace then gating the control under
  DD-043-10's standard. The draft enumerates
  either way.
- **DD-043-13 — The execution phase number**,
  allocated at the freeze act against the phases
  then reserved. Nothing in the design turns on
  the number.
- **DD-043-14 — The freeze gate mechanics.** The
  AEE lifecycle hooks have not run on this draft;
  at the freeze act they run as the gate under the
  programme's adopted aee pin (1.5.x), with the
  DD-038-10 gate reading for a draft-stage
  register, and any freeze digest is computed over
  the recovered register exactly once, at freeze.

## 5. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest
   computed at the freeze act), knowing: the
   population is four signs, listed; the verdict
   follows mechanically from those four signs and
   the recorded Phase 5 assignments; the
   provenance gate may close the study unscored
   before any assignment is read, on documentary
   grounds this draft states in full; and any
   verdict reached is bounded by spec §10's
   lineage statement. Or decline, leaving
   PRED-2026-007 standing PARTIALLY CONFIRMED on
   its sample of three, as it has stood since
   April 2026.
2. **DD-043-6's reading** — confirm that this
   spec scores PRED-2026-007 itself under the
   owner's successor order, or decline the reading
   (the design then retires unscored).
3. **DD-043-10** — fix the provenance gate's
   borderline evidence standard (draft
   recommendation in §4).
4. **DD-043-11** — whether the frozen spec files
   its own OSF contract registration
   (recommendation: yes).
5. **DD-043-12** — the LOG class's role
   (enumerated-only, or scored as a control).
6. **DD-043-13 / DD-043-14** — allocate the
   execution phase number; run the lifecycle
   hooks as the freeze gate.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## 6. Owner's campaign ruling E-4 — DD-043-6 superseded (2026-10-21)

Appended 2026-10-21, after the sections above,
which stand unaltered. This section records a
ruling the draft above awaited and reconciles
the draft to it.

- **The ruling.** On 2026-10-21 the owner
  (Tristen Pierson) approved the
  runnable-experiments campaign plan **as
  written** (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`),
  Wave 1 of which takes this spec as a member.
  Decision **E-4** in that approved plan reads:

  > **E-4 — The D-31 successor gets a new
  > prediction number.** Register discipline
  > and the triage both require it: the
  > successor to PRED-2026-007 registers as a
  > new PRED number, on a population frame
  > whose coded values are verified before
  > freezing, with its step 0 adjudicating the
  > cross-check registry's Wells-derived
  > provenance rather than inheriting it
  > silently. *Alternative:* run Spec 043 as a
  > provenance-and-method act only, leaving
  > the prediction unscored.

- **The ruling is the confirmation DD-043-6
  awaited, brought forward to the draft.**
  DD-043-6 (§3 above) recorded a
  DECIDED-BY-DRAFT reading — that this spec
  scores PRED-2026-007 itself, with no new
  PRED number — and expressly put that reading
  to the freeze for confirmation (§5, item 2).
  The owner's campaign approval is that
  confirmation act, given at the owner's
  ruling and brought forward to the draft
  rather than held for the freeze act; item 2
  of §5 is thereby discharged and is no longer
  an open question for the freeze.
- **DD-043-6's draft reading is SUPERSEDED.**
  The approval rules **against** the reading:
  the successor does **not** score
  PRED-2026-007 itself. It registers under a
  new PRED number — **PRED-2026-012**,
  registered 2026-10-21 in
  `docs/PREDICTION_REGISTER.md` §3 on this
  same branch (next free number: the register
  carried PRED-2026-001 through
  PRED-2026-011) — carrying PRED-2026-007's
  frozen prediction and success criterion
  verbatim, on the canonical-sign-registry
  frame this draft designs, under governing
  spec Spec 043, outcome PENDING.
  PRED-2026-007's own entry stands untouched
  and remains PARTIALLY CONFIRMED as its
  pre-execution record.
- **DD-043-6's fallback does NOT fire.**
  DD-043-6 provided that, if the freeze
  declined its reading, the design retires
  unscored. That fallback does not fire here:
  E-4's alternative horn — running Spec 043
  as a provenance-and-method act only,
  leaving the prediction unscored — was not
  chosen either. The campaign approves the
  **scored** successor under the new number,
  with step-0 provenance adjudication (spec
  §4, check 0.3) before any scoring. The
  design therefore neither scores
  PRED-2026-007 nor retires: it proceeds, at
  draft stage, as the governing spec for
  PRED-2026-012. The freeze and the execution
  remain separate owner gates; this section
  freezes nothing and runs nothing.

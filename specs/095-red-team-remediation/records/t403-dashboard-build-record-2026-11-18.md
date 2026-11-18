# T403 — Dashboard build record (2026-11-18)

**Commission.** Spec 095 T403: build the researcher dashboard (home +
the six wireframed features) to the Stage 4 wireframes the owner
approved by name on 2026-11-18 in the Glossa-Lab chat ("Approve the
Stage 4 wireframes and commission the dashboard build"), on the real
data the T402 Indus instantiation exposes; and, in the same
commission, re-run the T404 dashboard leg (filed as the addendum
companion to this record). Base: main `f44cef92` (PR #587 merge).
Branch: `feat/095-t403-dashboard-build`. The worker does not merge;
the parent gates.

## What was built

**Backend** — `backend/glossa_lab/api/researcher_dashboard.py`,
registered in `backend/glossa_lab/main.py` under
`/api/v1/researcher-dashboard`. A read model over the program's
records: every figure is re-derived from a record at request time;
nothing is cached into a standing. Endpoints: `/home`,
`/program-status`, `/corpora`, `/inscriptions` (paged; filters:
corpus, site, object class, sign token, length range, id substring),
`/inscriptions/{glossa_id}`, `/hypotheses`, `/claims` (filters:
standing, study, sign, falsifier present/absent, text),
`/claims/{claim_id}`, `/claims/{claim_id}/export`, `/matrix`,
`/results`, `/results/{run_id}`, `/results/{run_id}/rerun` (POST),
`/contributions` (GET + POST). One supporting addition outside the
module: `create_staged_candidate(fields)` in
`backend/glossa_lab/pipelines/research_loop.py`, the Spec 094
lifecycle service's own creation path for a staged candidate, which
the contribution POST calls (the Stage 4 census forbids any other
module from writing a creation-state literal).

**Frontend** — `frontend/src/components/ResearcherDashboard.tsx`
(shell + seven sections), typed helpers appended in
`frontend/src/api.ts`, route wiring in `frontend/src/App.tsx`
(route id `researcher-dashboard`, nav label "Researcher dashboard";
the legacy `dashboard` route id is untouched — it is an alias for
the program home and other surfaces navigate to it). The committed
`frontend/dist` is the build of the committed sources
(`npm run build`, tsc + vite, clean).

### Per wireframe page

- **Home.** Census band re-derived at request time and matching the
  record exactly: 994 claims in the ledger (1,025 ledger lines), 96
  studies, 287 recorded anchor signs (94 strict), 985/994 claims
  carrying a falsifier. The six strongest readings with the T303
  identifiability outcome stated on the face (all six NOT
  IDENTIFIABLE, parsed mechanically from the T303 application
  record, including its two discriminating-observation notes: M047's
  meaning 'fish' and M202's sibilant class). Six feature cards. The
  does-not-claim panel. Recent adjudications strip.
- **Program status.** Foundation state, research-loop state, and
  ledger/map state from the surfaces of record; census by standing;
  blocked items from the gap register of record, each with its
  blocker and its owner line (the register names no owner for the
  items shown, and the surface says exactly that rather than
  inferring one).
- **Inscription explorer.** Corpus list from the corpus-identity
  registry: the canonical Indus export verifies against its pin of
  record and is explorable (15,508 inscriptions; paging and the
  wireframe's filters). A record opens in four labelled layers —
  observation, transcription, hypothesis, claim — never blended;
  selecting a sign position shows only that sign's statements.
  Inscription grapheme identities are M-ids where the crosswalk
  resolved them (3,033 of 15,508 records carry at least one); the
  hypothesis layer joins anchor readings through them.
- **Hypothesis comparison.** Rival readings sign by sign at their
  recorded standings, the identifiability outcomes, the
  language-hypothesis cards, and the nonlinguistic position served
  from the ledger (claim `farmer_sproat_witzel_2004_manual_001`,
  standing contradicted) in the same form as every other claim.
  Translations panel: the program holds no translation of any
  inscription (held: 0), stated where a translation would go.
- **Evidence inspection.** The claim-by-evidence matrix as the
  record holds it (994 claim rows, 980 with cells, 644 columns,
  1,517 cells at build time — re-derived per request). Claim finder
  with the wireframe's filters; the falsifier-absent class is
  findable as a class and is exactly 9 claims, matching the map
  artifact's falsifier census gap list. A claim opens with its
  falsifier verbatim (or its absence stated), what it does not
  establish, its standing and supersession, its lineage, and its
  matrix cells. The audit trail exports as a JSON download of the
  records themselves (ledger row, map claim, lineage, cells,
  supersession, trail), never a summary of them.
- **Experiment reproduction.** The run index of record (67 entries).
  The 23 legacy entries whose execution records are incomplete are
  listed NOT REPRODUCIBLE with the missing pieces named (command,
  tool version, code version, seed, environment class, started,
  finished). A re-run first verifies corpus identity against the pin
  of record and refuses on an unverified corpus; it evaluates the
  settling engine read-only against current stores, writes its
  record only to a scratch directory through the verified-write
  library, compares per quantity (never pooled), and writes its
  outcome into no standing. The T405 run of record
  (`settling-20261116T034814Z-3681c4`) reproduces exactly:
  assigned_count 94, assigned_share 0.32867132867132864,
  consistent 94, conflicts 0. The re-run inherits the settling
  engine's source verification: on a tree whose extracted-claims
  files differ from the ledger mirror it refuses and names the
  mismatched files — the corpus-identity family of refusals working
  as designed (observed live during this build's verification, on a
  suite-dirtied tree).
- **Researcher contribution.** The boundaries panel states the
  set-wide refusals on the surface. The form cannot submit without
  a falsifier (client-side block; the server refusal is also
  surfaced verbatim). A valid submission lands in the staging store
  at creation state "staged" through the lifecycle service, with
  the falsifier and evidence references carried on the candidate
  record itself, no approver field, no stage.

### Refusals, as implemented

Set-wide: no automatic promotion anywhere (a submission enters at
"staged" and nothing in this surface moves it); no
self-certification (no surface lets a submitter approve, verify, or
certify their own or any candidate — a payload carrying an
`approver` field is refused); the Research Assistant boundary is
inherited (advisory only; nothing in the dashboard invokes it).
Per feature: an unverified corpus is listed unavailable with its
reason and serves nothing; a corpus with no inscription-level
export in the record is named as such, never explored on invented
data; no translation is presented where none is held; the
falsifier-less claims are shown as the gap, not worked around; an
incomplete run is not reproducible and a re-run is refused for it
with the missing pieces named; a re-run on an unverified corpus is
refused before anything runs. Contribution POST refusals (all 422,
each verified by test): no falsifier; an `approver` field present;
an automated submitter (the program's own `is_automated_actor`
check); an evidence reference that resolves to no record; an
unknown subject sign; fewer than one evidence reference.

## Data-source gaps filed

1. **Claim-layer grapheme gap.** The only claim-to-sign linkage in
   the program is one claim (`parpola_2010_dravidian_solution_
   manual_002`, sign_refs mahadevan:72/64/70 — GR-088-07). None of
   M064, M070, M072 appears as a resolved grapheme identity in the
   canonical export (count 0 for each), so no inscription's claim
   layer can light up for that one linked claim. The surface joins
   what the record joins and states the rest as absent; the gap is
   the record's, and it is filed here rather than papered over.
   Sign-name forms differ across the record (anchors and corpus
   graphemes name a sign M072; ledger sign_refs name it
   mahadevan:72); the read model normalizes both forms, and a test
   holds both.
2. **Strict V3 corpus and Holdat layer unavailable in a fresh
   checkout** — by design (the V3 file survives only in custody;
   the Holdat layer is absent from checkouts). Both are listed
   unavailable with the identity layer's own reason, which includes
   the diagnostic path the identity record carries. The remaining
   five registry corpora verify identity but carry no
   inscription-level export, so they are listed verified and not
   explorable, with that stated.
3. **Foundation check on a fresh checkout.** The canonical 17-check
   foundation profile measures 17/17 PASS on this tree with the
   Holdat layer present (verified this build; see Verification).
   On a bare fresh checkout the same check reports the Holdat leg
   as its one failure — a property of the checkout, recorded here
   so the number is never quoted without its condition.

## Verification (all figures from the runs' own records)

- **Backend, new tests:** `backend/tests/test_spec095_t403_
  dashboard.py`, 16 tests — 16 passed.
- **Backend, full suite** (CI invocation from `backend/`, GPU
  ignored, phase392 deselected by plain nodeid), run in two parts
  split at the spec086 gate file, concurrent with the Spec 091 T303
  worker's suite on the same box: part 1 — 2,943 passed, 66
  skipped, 1 deselected, 2 failed; part 2 — 22 passed, 44 skipped,
  1 failed. All three failures were this build's own surface
  tripping standing censuses, and all three were fixed in the
  build and re-verified: (a) the Spec 094 lifecycle census — the
  contribution POST now creates its candidate through the lifecycle
  service's own helper; (b) the ledger gate's V9 writer census —
  the re-run's scratch write now goes through the verified-write
  library; (c) the T405 re-run test under suite concurrency — the
  suite regenerates extracted-claims files in-tree and the engine
  then correctly refuses; the test restores that directory to HEAD
  first (a no-op on a quiet tree). Post-fix targeted union —
  `test_spec095_t403_dashboard.py`, all four `test_spec094_*`
  files, `test_promotion_integrity.py`,
  `test_staging_promotion_evidence.py`, `test_research_loop.py`,
  `test_research_loop_deep.py`: 136 passed with 2 failures, both
  traced to a local fixture (a Holdat corpus copy placed in the
  clone for the foundation check) and both passing with it removed;
  the dashboard file then re-ran 16/16 on the clean tree. CI on the
  PR runs the full suite on a fresh checkout and is the settling
  read for the whole suite.
- **Frontend e2e:** the new spec `frontend/e2e/researcher-
  dashboard.spec.ts` — 7 passed (including, after the T404 leg
  exposed the gap, claim-detail and lineage assertions). Full suite
  against a scratch instance on a spare port (the live origin holds
  port 8001 on this box): 295 passed, 10 skipped, 10 failed — the
  10 failures are exactly the tests of `dashboard-actions.spec.ts`
  (4) and `projects-goals.spec.ts` (6), which hardcode
  `http://localhost:8001` and therefore addressed the live origin,
  not the test instance; they never execute this build's code paths
  and run against the test backend in CI, which is the settling
  read for them.
- **Ledger gates**, sequentially on a quiet tree, verbatim
  summaries: `--all` — "summary: 29 PASS / 0 FAIL / 1 NOT-RUN",
  RESULT: PASS; `--regen` — "summary: 32 PASS / 0 FAIL /
  0 NOT-RUN", RESULT: PASS; `--contamination` — "1025 presentations
  scanned, 0 flag(s)", CONTAMINATION: PASS. The standing profile,
  held exactly.
- **Foundation check:** 17/17 PASS (n_pass 17, n_fail 0, n_warn 0,
  overall PASS) on the built tree with the Holdat layer present;
  the script form reports 39 checks passed, 0 failed, 9 warnings,
  matching the foundation status of record. See gap 3 for the
  fresh-checkout condition.
- **Rendered verification (the standing rule: no UI claim from
  source checks alone).** Playwright screenshots at desktop
  (1280x800) and mobile (390x844), full page, all seven surfaces,
  against an audit instance of the built tree, filed in
  `records/t403-screenshots/`. Each surface was read and compared
  against its approved wireframe: home (census band, strongest
  readings with outcomes, feature cards, does-not-claim panel),
  program status (foundation/loop/ledger cards, census by standing,
  blocked items with blockers), inscription explorer (corpus
  identity states, filters, layered record), hypothesis comparison
  (no-translation panel, nonlinguistic position, rival readings),
  evidence inspection (matrix summary, claim finder, falsifier
  chips), experiment reproduction (semantics banner, settling
  results, run index with not-reproducible entries), researcher
  contribution (boundaries panel, falsifier-required form). Two
  defects were found by this comparison and fixed before filing:
  the home census captions overflowed their cells and collided
  (fixed by wrapping the source captions; re-shot clean), and the
  claim detail card's test identifier was dropped by the shared
  Card component's prop surface (fixed by wrapping the card; the
  T404 leg's P5 step is what caught it, and the e2e spec now
  covers the detail). One cosmetic observation stands as rendered:
  blocked-item lines repeat the register id, because the register's
  own line begins with its id and the surface serves the line
  verbatim after its label — record-faithful, left as is.
- **T404 dashboard leg:** re-run in this commission; results in the
  addendum (`t404-dashboard-leg-addendum-2026-11-18.md`). Headline:
  protocol 8/8 (threshold P1 met); A1 not met (critical axe
  findings on three surfaces, named there); A2 met.

## C095-12 discharge (build half)

C095-12's build half is discharged by this build, in exactly these
terms: the dashboard home and the feature set of record (program
status, inscription explorer, hypothesis comparison, evidence
inspection, experiment reproduction, researcher contribution) are
built to the wireframes the owner approved by name on 2026-11-18,
each feature naming its refusals in its specification and holding
them in the built product (no automatic promotion of any candidate,
no self-certification of any claim, the Research Assistant advisory
boundary inherited), with Playwright verification at desktop and
mobile widths before any verified claim (the screenshot set filed
with this record). What C095-12 expressly does not establish —
that the features are usable or used — is C095-13's question and is
not discharged here; the dashboard leg of that question was re-run
in this commission and is filed as the T404 addendum, whose A1
finding stands open.

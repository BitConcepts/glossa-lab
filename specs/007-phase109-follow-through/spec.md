# Spec 007 — Phase-109 Follow-Through: executing the Phase-108 audit's recommendations

**Status:** Proposed 2026-10-06 on `feat/phase109-follow-through`
(from main 1d25d01d). Owner-approved execution of the Phase-108
recommendations (`reports/phase108_provenance_summary.md`, Step-5
section). Unlike spec 006, this package **does change anchors** —
but only via the pre-registered mechanical rules below, with every
change recorded in a change register and every changed entry
carrying a dated annotation. The PR is opened **NOT merged** —
the owner reviews all scientific changes.

**Phase-numbering note:** ledger-sequence **Phase-109** (107 =
Phase-52 v2, spec 005; 108 = provenance audit, spec 006). Legacy
script files from an earlier era carry colliding numbers; they are
append-only history, NOT renamed or reused. New artifacts carry
distinct names (`phase109_*`) and new graph node IDs, per the
spec-005/006 precedent.

## Context

Phase-107 falsified simulated annealing as evidence for sign values
(held-out agreement 0.000 under every lever; blind controls
non-discriminating: Sanskrit z = 60.87, scrambled z = 16.48, all
held-out 0.000). Phase-108 then classified all 287 anchors in
`backend/reports/INDUS_FINAL_ANCHORS.json` (166 HIGH / 109 MEDIUM /
8 LOW / 4 CANDIDATE): 210 strict SA-free (no SA anywhere in the
recorded chain), 44 SA load-bearing at HIGH (24 SA_DERIVED +
20 SA_CONFIRMED_ONLY), 33 further anchors with SA as a
non-load-bearing component — and, independently of SA, a
116-anchor **staging cohort** whose current readings were proposed
by the automated research loop's fixed heuristic tables (June 2026)
and promoted via `/staging/verify-sa`, an endpoint that performs no
SA test. The bulk promotion overwrote earlier sourced readings
(e.g. M042 vaN→min, against Parpola 'van'). Phase-108 authored
recommendations and executed none of them. This package executes
them under mechanical rules.

## Pre-registered decision rules (binding; fixed BEFORE any entry is touched)

### Annotation + change-register discipline (applies to Steps 1–3)

- Every changed anchor entry gains a `phase109_annotation` field:
  a dated (2026-10-06) string naming the Phase-109 action, the rule
  applied (spec 007 step + clause), and the basis citations.
  **No silent edits.**
- Every change is recorded in `reports/phase109_change_register
  .json`: sign, step, rule, action, before/after (reading,
  confidence, and any other field changed), citations.
- Anchor entries NOT named by Steps 1–3 are not modified in any way.

### Step 1 — Staging-cohort re-review (the 116)

**Cohort (registered):** the anchors whose Phase-108 register
record (`reports/phase108_provenance_register.json`) carries a
component with role `research_loop_heuristic` (116 anchors;
108 MEDIUM + 8 LOW at audit time).

**Evidence assembled per anchor (in-repo ONLY):** the current
anchor entry; the register record; the Phase-108 trail
(`reports/phase108_anchor_trails.json`: `anchor_snapshots` from the
three pre-promotion backup files `INDUS_FINAL_ANCHORS.backup_
20260520_100230.json` / `_20260522_210001.json` / `_20260523_
181449.json`, `crosswalk_v2`, `ledger_mentions`,
`artifact_mentions`); the anchor's full entries in the backup
files; its entries in `outputs/anchor_staging_archive.json`.

**Independent support — what counts (registered):** a recorded
non-SA, non-heuristic assignment of the anchor's CURRENT reading
from any of —
- (A1) crosswalk v2.1 (`backend/glossa_lab/data/mahadevan_parpola_
  crosswalk_v2.json`): the Parpola reading's normalised first
  segment (Phase-108 normalisation: lowercase, NFD-strip
  diacritics, first segment before `/`) equals the current
  reading's normalised first segment;
- (A2) the latest backup snapshot records the SAME reading (the
  value predates the loop; the loop did not originate it), with
  the snapshot entry's own basis as the recorded support;
- (A3) a ledger mention or non-SA phase artifact in the trail
  assigning the current value via a non-loop method (e.g. a DEDR
  expansion table, a grammar/positional phase), cited concretely
  and hand-verified.
The loop's `dedr_support` gloss lookup and all SA artifacts
explicitly do NOT count as support.

**Rules (applied in order):**
- **(a) KEEP** — independent support (A1/A2/A3) for the current
  staging value is recorded → value and confidence unchanged;
  annotate provenance (register citation + the support citation).
- **(b) RESTORE** — not (a), and a prior sourced reading exists
  that the staging promotion overwrote → restore the prior
  reading **and its confidence basis**: reading, confidence,
  basis, source (and any prior value-bearing fields) taken from
  the latest backup snapshot entry; annotate (prior source +
  this review). A prior reading is "sourced" when recorded in a
  backup snapshot (all three snapshots agreeing on the reading)
  or, for a sign without snapshots, in a ledger/crosswalk record
  with a named source.
- **(c) DEMOTE** — neither (a) nor (b) → demote one tier
  (HIGH→MEDIUM, MEDIUM→LOW, LOW→CANDIDATE; CANDIDATE stays) and
  annotate "staging-heuristic origin, unvalidated (Phase-109)".

Outcomes are computed by script from the assembled evidence and
hand-checked: every (a) and (c) case individually, every (b) case
whose snapshot confidence is HIGH or MEDIUM, and a sample of the
(b)-to-LOW cases. Report (a)/(b)/(c) counts and list every (b)
restoration individually.

### Step 2 — SA-lineage HIGH anchors (the 44)

Each of the 24 SA_DERIVED + 20 SA_CONFIRMED_ONLY anchors (register
categories) gains two machine-readable fields —
`validation_status: "pending_non_sa_validation"` and
`provenance_class: <register category>` — **without** changing
value or tier in this step. (They are presented as candidates via
the Step-5 headlines, which exclude them.) M293 is included here
and additionally goes through Step 3.

### Step 3 — Individual re-reviews (dossiers + rule-bound outcomes)

Dossiers are assembled from in-repo sources only and stored as
`reports/phase109_dossier_M293.json`, `..._M362.json`,
`..._M398.json` (evidence for and against, with citations; the
rule applied; the outcome).

- **M293 'ta'** — its HIGH rests on the Phase-116 SA-only gate
  path (register: SA_CONFIRMED_ONLY; Phase-116 eval log:
  source "Phase-101 positional adjudication" not whitelisted,
  SA-cons = 1.00 the firing disjunct; M293 ∈ Phase-116
  `upgraded_signs`, MEDIUM→HIGH). **Rule:** set the tier to the
  highest tier its NON-SA evidence supports, where a tier is
  supported by a completed non-SA adjudication/validation at that
  level (the Phase-108 load-bearing test). The Phase-101
  positional adjudication's own recorded outcome (glossa-indus
  ledger, 2026-05-18) was **PROMOTED TO MEDIUM**. Unless the
  dossier finds a completed non-SA validation at HIGH level,
  M293 is set to MEDIUM, reading unchanged, annotated with the
  dossier citation.
- **M362, M398** — Phase-105's adjudicated verdict is
  INCONCLUSIVE (freq 3 each, below the positional-verdict floor;
  `reports/phase105_name_signs.json`; restated 2026-10-05) and
  was never superseded. **Rule:** an anchor's tier may not exceed
  what the latest adjudication supports → set each to at most
  MEDIUM, annotated with the Phase-105 citation, unless the
  dossier finds a LATER superseding adjudication in-repo (cite
  it if so). A recalibration/promotion gate (Phase-216) is not
  an adjudication. (Both anchors' pre-gate standing was MEDIUM
  per the May-2026 backups.)

### Step 4 — Promotion-path + governance fixes

- **(a) Endpoint honesty + evidence-gated promotion.**
  `POST /staging/verify-sa` performs no SA test (it marks
  approved candidates verified and archives them). It is renamed
  to **`POST /staging/verify-archive`**. The old path remains as a
  clearly-marked **deprecated alias** (the committed frontend
  `dist` build still calls it) delegating to the same handler,
  with a deprecation warning logged; `frontend/src` is updated to
  the new path. Separately, `POST /staging/promote` gains the
  evidence gate: a candidate is promoted **only** if it carries a
  recorded non-SA evidence reference — candidate field
  `evidence_ref` (non-empty string) or a per-sign entry in the
  request body's `evidence_refs` map. Candidates lacking one are
  NOT promoted and are reported in the response
  (`blocked_no_evidence`). The promote endpoint's post-promotion
  "Mandatory SA validation" auto-queue (SA experiments queued to
  "validate" new anchors) is **removed**: after Phase-107, SA
  cannot validate a promotion. The response keeps the
  `sa_validation_jobs` key (always empty) for shape compatibility.
  A regression test proves promotion without an evidence
  reference fails (nothing written) and promotion with one
  succeeds.
- **(b) Governance rule.** Add to `docs/governance/rules.md`:
  **H26 — No SA-sufficient promotion gates.** Anchor promotions
  and confidence upgrades MUST cite a recorded non-SA evidence
  reference; SA agreement, SA z-scores, and SA consensus MUST NOT
  be a sufficient condition in any promotion gate or validation
  step (Phase-107 falsified SA as evidence for sign values;
  Phase-108 audited the consequences). Enforcement point: the
  `/staging/promote` evidence gate.
- **(c) Foundation-check text retirements.** In
  `backend/scripts/foundation_check.py`, retire the evidential
  framings identified by the Phase-108 impact map
  (`reports/phase108_impact_map.json` → `foundation_map`):
  Phase-52 z/"SA agrees 55%" VERIFIED framing (incl. the
  CHECK NEW-F header/check framing — the mechanical check itself
  stays functional and unchanged in logic), Phase-57 z=19.07
  "VERIFIED — highest z-score in the project", Phase-67
  "DEFINITIVE" (the 1.85x same-null ratio stands only as a
  descriptive statistic), Phase-73 ensemble-as-support, and the
  Phase-44 "VERIFIED — strongest SA result" mislabel (map:
  NEEDS CAVEAT — an LM language-fit statistic, not an SA
  decipherment result). Retired entries move from `solid_claims`
  to `caveated_claims` with a SUPERSEDED (Phase-107/108) status,
  or have their status text reframed in place where already
  caveated. Lines the map marked STANDS are not touched;
  OPERATIONAL lines (GPU warning, Phase-168 checks) are not
  touched; archived-artifact presence labels are not touched.

### Step 5 — Headline re-base

- **(a) README.** The Decipherment Status block, the §Indus
  Script Decipherment section (incl. its metrics table), and the
  Current research status section: the retired set (161 anchors /
  90.96% coverage / 59% Parpola) is replaced by the
  SA-independent basis **recomputed fresh** on the post-Step-1–3
  anchor set (Phase-108 methods, Phase-108 strict definition:
  register category ∉ {SA_DERIVED, SA_CONFIRMED_ONLY} AND
  `sa_in_chain` = false, restricted to H+M of the post-change
  file): subset H/M counts, Holdat token coverage, phonotactic
  violations, grammar site-invariance, and the crosswalk Parpola
  quantity reported with its Phase-108 caveat (not as a silent
  59% swap). A dated "Re-based after Phase-107/108 (Phase-109,
  2026-10-06)" note explains what changed and why and points to
  the artifacts (`reports/phase107_*`, `reports/phase108_*`,
  `reports/phase109_*`). The v4 preprint citation of record is
  retained as a citation, marked as superseded in headline by
  the re-base note and the v5 addendum draft. Recomputation
  output: `reports/phase109_rebase.json`.
- **(b) Anchors bookkeeping.** Regenerate all summary fields of
  `INDUS_FINAL_ANCHORS.json` from the changed entries (spec 004
  WS3 method): `total`, `total_all_entries`,
  `metadata.total_count`, `by_confidence`, `n_high`, `n_medium`,
  `n_low`, `n_candidate`, `metadata.high_count` / `medium_count`
  / `low_count` / `candidate_count`, `metadata.hm_confirmed_
  count`, and `corpus_token_coverage` recomputed for the FULL
  post-change H+M set (the quantity that field denotes). The
  historical `preprint_161` definition stays intact; a dated
  `_phase109_note` records this package's changes.
- **(c) Preprint addendum (DRAFT ONLY).** A formal addendum is
  drafted in-repo at `glossa-corpus/indus/pierson_2026_
  indus_decipherment_addendum_v5.md`, marked DRAFT — NOT
  SUBMITTED, carrying the re-based headlines and the
  Phase-107/108/109 outcomes, and recording the exact `.tex`
  edits a v5 bump would make (per `docs/research/
  PREPRINT_VERSIONING.md`). The published v4 `.tex`/PDF and
  AGENTS.md's current-version fields are NOT altered (v4 remains
  the version of record until the owner publishes a v5). The
  versioning doc gains a draft row marked NOT published. No
  external send of any kind (H14).

### Step 6 — Close-out (acceptance checks, registered)

- Change register complete: every anchors-file change from
  Steps 1–3 + Step 5(b) bookkeeping accounted for in
  `reports/phase109_change_register.json`.
- Foundation check: **0 failures** (H21). Exact new totals
  reported plainly — counts may legitimately move because tiers
  changed; no check may fail because of stale text (fix text,
  never the check logic's intent).
- Full backend test suite: exact counts vs the 586 passed /
  9 skipped baseline.
- Ruff clean on all changed Python files.
- Ledgers appended (glossa-indus Phase-109 entries per step +
  root `LEDGER.md` summary; AI disclosure, constitution §VI).
- Push branch; PR via `gh pr create` with the change-register
  summary in the body. **NOT merged** (owner review).

## Graph-first compliance (H15/H23)

Phase scripts are written first, with graph module
`backend/glossa_lab/experiment_graph_phase109.py` (nodes
`IndusPhase109StagingReview`, `IndusPhase109SaFlags`,
`IndusPhase109Rereviews`, `IndusPhase109Rebase`) registered in
`experiment_graph.py` (try/except) and verified in ATOMIC_NODES
BEFORE any script runs. Shared logic lives in
`backend/glossa_lab/pipelines/phase109_followthrough.py`
(precedents: `pipelines/provenance_audit.py`,
`pipelines/sa_validation.py`), with unit tests in
`backend/tests/test_phase109_followthrough.py`. Each phase
script has `decide` (default; writes decision/dossier artifacts,
touches nothing) and `apply` (writes anchors + change register)
modes; the graph nodes run `decide` mode. Step 4 is ordinary
backend work (API + tests), not a phase experiment; its
regression test lives in
`backend/tests/test_staging_promotion_evidence.py`.

## Assumptions (H13 epistemic boundaries)

- The Phase-108 register + trails are the evidence base for
  Steps 1–3 (BeliefArtifacts at HIGH confidence: merged PRs #60,
  #61). Where the register and a primary artifact conflict, the
  primary artifact governs (Phase-108 authority order) and the
  conflict is logged in the change register.
- Backup snapshots (May 2026) are the recorded pre-promotion
  state of the anchors file. All three agree on the reading for
  every snapshot anchor (verified in survey); confidence is
  taken from the latest snapshot. A restoration restores that
  recorded state — it asserts nothing about whether the prior
  reading is historically correct, only that it was the sourced
  reading the loop overwrote.
- Classification (Phase-108) describes the programme's internal
  evidence chain. "SA-independent" does not mean "validated"; the
  Step-5 headlines are internal-consistency quantities on a
  named, stored set — that is precisely their claim.
- Tier changes under Steps 1/3 follow the registered rules
  mechanically. Any anchor whose evidence fits no rule cleanly
  is flagged in the change register as an edge case and decided
  by the rule order (a) → (b) → (c) on the recorded evidence —
  never by preference.
- Adversarial challenge: a staging value could have non-loop
  support recorded only in a file the Phase-108 trail did not
  index; mitigated by the audit's full-tree index (reports/,
  outputs/, both ledgers, claims) and by hand-checking every
  (a)/(c) outcome.
- GPU: all computations are deterministic text/count work on
  CPU; scripts record `gpu_device` per the H20 pattern where
  they emit phase artifacts (torch absent in this environment;
  warning printed, never silent).

## Out of scope

- Merging the PR (owner review gate).
- Any external communication or publication: no Zenodo/SSRN
  submission, no email (H14); the v5 addendum is an in-repo
  draft only.
- Anchor changes beyond Steps 1–3's registered rules; any
  change to the 31 extracted claims; any foundation-check
  *logic* change (Step 4(c) is text only).
- Re-running SA or any decipherment experiment.

## Addendum — Step 1 hand-check corrections (2026-10-06, recorded before apply)

Two refinements surfaced by the registered hand-check protocol,
applied to the Step 1 decision machinery BEFORE any anchor was
touched, and recorded here so the deviation from the letter above
is explicit:

1. **Reading identity is exact.** Rules A1/A2/A3 above reference
   Phase-108 normalisation for A1; applying that lossy normalisation
   to identity in general produced a false (a) for **M046**: the
   loop's current `kal` (DEDR gloss "gem / stone") matched the
   Phase-89/crosswalk `kaL` (DEDR 1286, "leg/stem") only because
   normalisation lowercases and strips diacritics. In this
   notation case and diacritics are phonemically significant
   (`kaL` ≠ `kal`, `vaN` ≠ `van`) — they are different readings
   with different DEDR entries. Identity for A1/A2/A3 is therefore
   judged on the **exact recorded first segment**; normalised-only
   matches are reported in the decisions artifact as notes, not
   counted. Effect: M046 moves (a) → (b) (restore `kaL`/HIGH,
   Phase-89 DEDR). M222's (a) is unaffected (crosswalk `min` is an
   exact match).
2. **SA-origin priors are not restorable under (b).** Two cohort
   priors (M231, M252) record `kur` assigned by the **Phase-122
   syllabic LM SA** (modal readings, consistency 0.25 / 0.17).
   After Phase-107 an SA run's output is not a "sourced reading"
   in the sense of rule (b); restoring SA-modal readings at
   MEDIUM through the back door would contradict Steps 2/5's
   treatment of SA-derived material. A prior counts as sourced
   for (b) only when its origin is not an SA run (origin test:
   source field names an SA phase, or the basis records an SA
   assignment mechanism; a later recalibration bracket merely
   mentioning SA-cons does not disqualify a DEDR-sourced reading —
   cf. M042/M108). Effect: M231, M252 move (b) → (c) (demote
   MEDIUM → LOW), with the SA-origin prior recorded in their
   annotations.

Also recorded for reviewer attention (no rule change): 109 of the
(b) restorations restore `kur` at LOW from **Phase-111 allograph
resolution** (positional-profile L1 identity with M222, then read
as `kur`). That is the last non-loop recorded state for those
signs and rule (b) restores it as registered; the restored basis
text states the derivation verbatim. It coexists with M222's own
(a)-KEEP of `min` (Parpola crosswalk) — the tension is inherent in
the record and is flagged in the glossa-indus ledger entry.

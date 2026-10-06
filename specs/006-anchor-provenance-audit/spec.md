# Spec 006 — Anchor Provenance Audit: what the 287 anchors rest on after Phase-107

**Status:** Proposed 2026-10-06 on `feat/anchor-provenance-audit`
(from main 6a46809e). Owner-approved audit. **Audit and report only** —
no anchor reading, confidence, or basis is changed by this package;
any reclassification is a recommendation for the owner's later decision.

**Phase-numbering note:** this package is ledger-sequence **Phase-108**
in the glossa-indus ledger (106 = Phase-52 re-run, spec 004; 107 =
Phase-52 v2, spec 005). Legacy script files from an earlier era already
carry some numbers in this range (`phase108_phon_exhaustion.py` etc.);
they are append-only history, NOT renamed or reused. All new artifacts
carry distinct names (`phase108_provenance_*`) and new graph node IDs,
per the spec-005 precedent.

## Context

Phase-107 (spec 005, PR #60, merged) falsified simulated annealing as
evidence for sign values: held-out agreement 0.000 under every lever,
blind controls non-discriminating (Sanskrit z = 60.87, scrambled
z = 16.48, all held-out 0.000). The 287 anchors in
`backend/reports/INDUS_FINAL_ANCHORS.json` (166 HIGH / 109 MEDIUM /
8 LOW / 4 CANDIDATE) were not changed. Their **provenance** is now the
open question: the historical "41% SA agreement" was circular (pins
agreeing with themselves), but the anchor set was built over ~270
phases by many methods — DEDR rebus work, literature adoption, grammar
tests, formula decomposition, crosswalk work, and SA runs. This audit
establishes, per anchor, which evidence lines its value and confidence
actually rest on, and recomputes the programme's headline
internal-consistency quantities on the SA-independent subset only.

## Pre-registered taxonomy (binding; fixed BEFORE any classification)

Each anchor receives: a primary `category`, a `components` list (every
evidence line found in its trail, each with type + in-repo citation),
`sa_in_chain` (bool), `sa_role` (none | origin | promotion |
mentioned-only), and `first_proposal` (source + citation).

- **ICONOGRAPHIC** — the value's first proposal rests on pictorial
  identification of the sign alone (what the sign depicts), with no
  DEDR rebus assignment, no literature value adoption, and no SA.
- **LITERATURE** — the value was adopted from a publication independent
  of this programme (Mahadevan, Parpola, Wells, Fuls, or others); the
  trail cites the publication as the source of the value.
- **DEDR** — the value was assigned by the programme via Dravidian
  Etymological Dictionary rebus/etymology (depiction → DEDR entry →
  phonetic value), not copied from a publication's Indus reading and
  not an SA output.
- **GRAMMAR** — the value/function was assigned by positional or
  morphological analysis (slot statistics, suffix paradigms,
  motif-independence tests, positional z-tests), not SA-derived.
- **FORMULA** — the value was assigned by decomposition of recurring
  inscription sequences/formulas, not SA-derived.
- **CROSSWALK_CORPUS** — the value rests on comparative corpus evidence
  (M↔P crosswalk identity, CISI cross-validation, contact-zone/Gulf
  corpus comparison), not SA-derived.
- **SA_DERIVED** — the value's first proposal in the programme's
  recorded phase history came from an SA run's output.
- **SA_CONFIRMED_ONLY** — non-SA origin, but the promotion to the
  anchor's current confidence cites SA agreement as a load-bearing
  reason (test below).
- **MIXED** — the trail shows multiple evidence lines and no single
  line is the sole basis; components are enumerated and the primary
  category is the line that first proposed the value. `sa_in_chain`
  is set iff any component is an SA line.
- **UNTRACEABLE** — the trail cannot be established from in-repo
  sources. Assigned whenever the record is silent or ambiguous;
  provenance is never guessed.

**SA artifacts (the SA lineage), enumerated:** the programme's
simulated-annealing decipherment runs — Phase-46 T5 SA sweep,
Phase-47 T3 M267 constraint SA, Phase-52, Phase-55/62a/73 SA ensembles,
Phase-57, Phase-63 phonotactic-filtered SA, Phase-66/67 Sanskrit SA
(falsification context; cannot confirm Dravidian values — an anchor
whose only SA contact is a falsification run is NOT SA-confirmed),
Phase-77 SA agreement analysis (an agreement measurement, never an
origin), Phase-106, Phase-107 (validation only; proposed nothing),
Phase-110 targeted SA, Phase-116 SA recalibration, Phase-122 syllabic
LM SA, Phase-168 blocker SA, Phase-193/207/213/216 SA re-runs (a value
first appearing in one of these re-runs' consensus/decipherment
tables counts as SA-derived), Phase-229 CISI anchor SA, and CGSA
outputs where they proposed values. Non-SA computational decoders
(Phase-26b Bayesian decoder, beam decipher) are recorded as component
type NON_SA_COMPUTATIONAL — they are not SA, and an anchor resting
only on one is flagged explicitly in the register.

**SA-dependence (the headline test), registered:** an anchor is
SA-DEPENDENT iff (i) SA_DERIVED, or (ii) SA_CONFIRMED_ONLY.
SA_CONFIRMED_ONLY applies iff the promotion record (the anchor entry's
basis/source/upgrade fields and/or the promoting phase's ledger entry)
names SA agreement, an SA z-score, SA consensus, or an SA phase as
evidence for the promotion, AND the remaining cited lines do not
include a completed non-SA validation of the value at the promoted
level (a grammar/positional test, a χ²/motif test, a DEDR validation,
or a literature confirmation). Cases failing either prong cleanly are
decided in hand-review (Step 2 pass 2) and logged as edge cases with
rationale — never silently forced.

**Headline counts, registered:** per category overall and by
confidence tier (HIGH / MEDIUM / LOW / CANDIDATE), plus the key number
stated three ways:
- **strict** — anchors SA-independent AND traceable (category ∉
  {SA_DERIVED, SA_CONFIRMED_ONLY}, `sa_in_chain` = false, category ≠
  UNTRACEABLE), as n / 287;
- **incl. untraceable** — (strict + UNTRACEABLE) / 287;
- **excl. untraceable** — strict / (287 − UNTRACEABLE).

## Steps

### Step 0 — This spec (H2). No classification before it lands.

### Step 1 — Evidence extraction (in-repo sources ONLY)
For every one of the 287 anchors, assemble its trail from: the anchor
entry's own fields (`basis`, `source`, `dedr*`, `phase_upgraded`,
`upgrade_basis`, notes); `glossa-indus/LEDGER.md` phase entries;
phase artifacts in `reports/` and `outputs/` (SA-era outputs incl.
Phase-48–61 pipeline files, SA re-run/injection artifacts,
Phase-106/107 artifacts); claims files under `glossa-indus/claims/`;
`CITATIONS.md`. Output `reports/phase108_anchor_trails.json`: per
anchor — sign, current reading, confidence, first-proposal source
with file citation, promotion history if recorded, every SA artifact
appearing anywhere in its chain, and the raw evidence snippets the
classifier consumed.

### Step 2 — Classification (two-pass discipline)
Pass 1 (programmatic): classify where the trail is explicit (an SA
artifact named in the basis/source fields, a DEDR number present with
a DEDR-phase origin, a literature citation as source, a
`phase_upgraded` pointing at a grammar/formula/crosswalk phase, etc.).
Pass 2 (hand-review): the coordinating agent reads the remaining
trails and decides each, writing `reports/phase108_review_decisions
.json` (per-anchor final category + rationale + citations) which the
classifier merges deterministically into the final register.
Disagreements between passes and all edge cases are logged in the
register, not forced. Output: `reports/phase108_provenance_register
.json` (per anchor: category, components, sa_in_chain, sa_role,
chain summary, citations, pass provenance) +
`reports/phase108_provenance_summary.md` (readable summary with the
registered headline counts).

### Step 3 — Subset recomputation (deterministic, in-repo)
Recompute on the SA-INDEPENDENT subset (exclude SA_DERIVED and
SA_CONFIRMED_ONLY; UNTRACEABLE reported both ways as a sensitivity
pair) — registered methods:
- **(a) Token coverage.** Holdat corpus CSV
  (`corpora/downloads/external_repos/holdatllc_indus/indus_corpus
  2.csv`; 7,002 token rows). Covered iff the token's sign is in the
  set in question (H+M anchors only). Full set first (anchors-file
  figure: 0.9647), then SA-independent H+M, then the sensitivity pair.
- **(b) Phonotactic violation rate.** Reuse Phase-58's own machinery
  (`backend/scripts/phase58_phonological_gap.py`:
  `analyze_phoneme_inventory`, `is_valid_dravidian_initial`) on the
  reading sets — the same measure behind the foundation claim
  "0 violations in HIGH/MEDIUM set". Full H+M set, SA-independent
  H+M, sensitivity pair. Report violation counts/rates plus distinct
  initials and max phoneme share (Phase-58 headline companions).
- **(c) Parpola agreement.** Comparison base: crosswalk v2.1
  (`backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json`),
  whose entries carry Parpola's reading per M-sign. Compared set =
  anchors in the set in question whose sign has a crosswalk entry
  with a non-empty Parpola reading. Match rule (registered):
  normalise both readings (lowercase, NFD-strip diacritics, first
  segment before `/`, strip parenthetical glosses and non-letters);
  agree iff the normalised first segments are equal. Report
  n_compared / n_agree / rate for full H+M and SA-independent H+M
  (+ sensitivity pair). Secondary cross-check, clearly labelled: the
  Phase-159 `confirmed_signs` list (the actual source of the README
  59% = 44/75 of the Phase-170-era HIGH set) — fraction of the set's
  HIGH signs on that list.
- **(d) Grammar site-invariance.** Reuse Phase-69's machinery
  (`backend/scripts/phase69_site_stratification.py`: its `chi2_test`
  and I/M/T per-site counting, with the script's own eligibility
  rule, quoted in the artifact) restricted to the subset's H+M signs.
  Run the identical computation on the full current H+M set first;
  if the full-set replication diverges from the historical artifact
  (65 signs, 100% invariant — an older, smaller anchor set), the
  divergence is reported and subset numbers are labelled
  replication-grade. If the machinery cannot be re-run cheaply, state
  that precisely instead of approximating.
Output: `reports/phase108_subset_recomputation.json` with method
notes and old-vs-subset numbers for each quantity.

### Step 4 — Circularity + downstream impact map (a MAP, not an edit)
- **Circular chains:** concrete instances of anchor → SA pin → SA
  "agreement" later cited in a promotion or claim, each citing the
  pin artifact and the citing artifact. Sources: Phase-52/57
  decipherment tables, Phase-77 agreement analysis, anchor promotion
  records, ledger entries for the injection→re-run cycles
  (Phases 190/193, 206/207, 209/213, 216, 222/229).
- **Downstream map:** (i) the 31 extracted claims
  (`glossa-indus/claims/extracted_claims/` + Phase-104 evaluation) —
  which cite or depend on SA-lineage anchors, per claim; (ii) the
  preprint/README headline numbers (161 anchors; 90.96% coverage;
  59% Parpola agreement) — the subset each was computed on and how
  much of that subset is SA-lineage per this audit; (iii)
  `backend/scripts/foundation_check.py` claim texts citing SA phases
  (enumerated exhaustively by grep + reading), each mapped to its
  post-Phase-107 status. No text is changed.
Output: `reports/phase108_impact_map.json` + the map section of the
summary MD.

### Step 5 — Close-out
Recommendations section (authored, NOT executed): what an honest
post-Phase-107 programme statement looks like given the audit —
which numbers survive, which must be retired or re-based. Then:
full backend test suite (baseline 576 passed / 9 skipped — exact
counts), foundation check (baseline 40/0/8; must show 0 failures —
H21), ruff on changed Python, ledgers (glossa-indus Phase-108
entries per step + root summary, AI disclosure), push, PR via
`gh pr create`. NOT merged (owner review).

## Graph-first compliance (H15/H23)
Audit scripts under `backend/scripts/phase108_provenance_*.py` are
written first; graph module `backend/glossa_lab/experiment_graph
_phase108.py` with AtomicNodeDef nodes per script is created and
registered in `experiment_graph.py` (try/except) and verified in
ATOMIC_NODES BEFORE any script runs. Shared logic lives in
`backend/glossa_lab/pipelines/provenance_audit.py` (precedent:
`pipelines/sa_validation.py`), with unit tests in
`backend/tests/test_provenance_audit.py`.

## Assumptions (H13 epistemic boundaries)

- Provenance is judged ONLY from in-repo records. A value may have an
  origin outside the repo's records; if the repo does not show it,
  the category is UNTRACEABLE — never SA_DERIVED by default and never
  a guessed non-SA category.
- The anchors' `basis` fields are terse and occasionally conflict
  with the ledger. Authority order: phase artifacts > ledger entries
  > anchor-entry fields > README/preprint text. Conflicts are logged
  in the register.
- Classification describes the programme's internal evidence chain.
  It says nothing about whether a reading is historically correct,
  and "SA-independent" does not mean "validated" — it means the
  recorded chain never passed through the SA lineage.
- BeliefArtifacts relied on: Phase-107 artifacts (`reports/
  phase107_*`, merged PR #60) at HIGH confidence; the anchor file at
  main 6a46809e as the audit object. Adversarial challenge: an anchor
  whose SA contact is recorded only in a file this audit does not
  index would be misclassified as SA-independent — mitigated by
  indexing all of `reports/`, `outputs/`, both ledgers, and the
  claims tree in Step 1, and by the register's per-anchor citations
  being spot-checkable.
- GPU: audit computations are deterministic text/count work; the
  Phase-69 replication reuses a script that imports torch guarded
  (established pattern: `gpu_device` recorded, CPU warning printed,
  never silent — H20).

## Out of scope

- ANY change to anchor readings, confidences, basis fields, or
  `INDUS_FINAL_ANCHORS.json`; any edit to README, preprint, claims,
  or foundation-check texts (Step 4 maps them; it does not touch
  them).
- Reclassification of any anchor (recommendations only, Step 5).
- Merging the PR (owner review gate).
- External sources of any kind (in-repo trails only).

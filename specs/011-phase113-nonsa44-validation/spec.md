# Spec 011 — Phase-113: Non-SA Validation Battery for the 44 SA-Lineage Anchors (pre-registration)

**Status:** FROZEN 2026-10-07 on `phase/nonsa44-validation` (from main
`f82c81fa`). Owner authorization: Tristen Pierson, 2026-10-07
(roadmap item 2: non-SA validation of the 44 SA-lineage HIGH
anchors). This spec is committed alone, before any battery code is
run against any anchor and before any calibration or validation
statistic exists. Git order is the pre-registration proof.

**Phase-numbering note:** ledger-sequence **Phase-113**. A legacy
script already carries this number
(`backend/scripts/phase113_medium_to_high_upgrade.py`, from an
earlier era). That file is append-only history and is NOT renamed
or reused. All new artifacts carry distinct names
(`phase113_battery`, `phase113_run`, `phase113_nonsa_battery`,
graph node `IndusPhase113NonSaValidation`), per the spec-010
precedent.

**AI disclosure:** this study is designed for execution by an AI
agent (Muse Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.

## Context — why this phase exists

Phase-107 (spec 005) falsified simulated annealing (SA) as evidence
for sign values: the strengthened Phase-52 SA recovers 0.000
held-out anchor signs under every lever, with Sanskrit and
scrambled controls statistically identical to Dravidian. Phase-108
(spec 006) traced the provenance of all 287 anchors and found 44
whose value rests on the SA lineage alone — 24 `SA_DERIVED` and 20
`SA_CONFIRMED_ONLY`. Phase-109 (spec 007) left those 44 in place
but flagged them `validation_status: pending_non_sa_validation`
(43 at HIGH, one — M293 `ta` — at MEDIUM), explicitly presenting
them as candidates pending a non-SA test. Governance rule **H26**
forbids any SA-sufficient promotion or validation gate, so the
question Phase-109 deferred is well-posed and still open:

**Do the 44 flagged anchors survive a validation battery that
never touches an SA output — cross-corpus consistency, positional-
grammar fit, and compositional co-occurrence — at frozen
thresholds, calibrated against a known-good set (the strict
SA-independent core) and a known-bad set (the Phase-110
premise-superseded `kur` cohort)?**

This phase validates or demotes; it never promotes. A
`VALIDATED_NON_SA` outcome changes only the anchor's
`validation_status` (to `validated_non_sa`, with a Phase-113
evidence reference satisfying H26); its tier is unchanged. A
`DEMOTE` outcome moves the anchor to CANDIDATE. Anything the
battery cannot judge stays flagged `pending_non_sa_validation`.

## Scope

**In scope:** the three frozen tests of §3, the calibration gates
of §4, the decision rule of §5, applied to exactly the 44 flagged
anchors of §2; anchor-file changes only as §5 dictates, each
recorded in the change register.

**Out of scope:** re-adjudicating any reading's value; touching
any anchor outside the 44 (calibration sets are evaluated
read-only — their anchors are never modified by this phase);
promotions of any kind; new corpus acquisition; SA in any form
(no SA scores, modal readings, consistency values, or
SA-derived language-model outputs are inputs to any test — the
syllabic LM is not used anywhere in this battery).

## 1. Data (frozen inputs)

| Input | Path | Role |
|---|---|---|
| Anchors (287) | `backend/reports/INDUS_FINAL_ANCHORS.json` | target + calibration sets; the only file this phase may modify, and only per §5 |
| Provenance register | `reports/phase108_provenance_register.json` | set definitions (category, `sa_in_chain`) |
| Holdat corpus | `corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv` (gitignored; located in the main checkout) | T2, T3; loaded with the `load_holdat_corpus` machinery of `glossa_lab/pipelines/sa_validation.py` (loader only — no SA code is executed) |
| ICIT converted layer | `corpora/downloads/icit_fieldcady/icit_converted.json` (gitignored; 1,007 inscriptions / 2,238 tokens, Mahadevan numbering, deduplicated against Holdat by the Phase-107 builder) | T1 |
| Phase-58 phonotactics | `backend/scripts/phase58_phonological_gap.py` (`is_valid_dravidian_initial`) | T2b sub-check (i) |

The ICIT converted layer is local restricted data: it is computed
on locally and is never committed or published; only statistics
and verdicts derived from it appear in this phase's reports. Its
provenance (ICIT via the Lipi export / field-cady MIT mirror,
converted Wells→Mahadevan via the canonical registry + crosswalk
v2.1) is recorded in `reports/phase107_acquisition_log.json`.

## 2. Sets (frozen definitions; all recomputed at run time and asserted)

- **FLAGGED44** — anchors with
  `validation_status == "pending_non_sa_validation"`. Asserted:
  |FLAGGED44| = 44; equals register categories SA_DERIVED (24) ∪
  SA_CONFIRMED_ONLY (20); tiers 43 HIGH + 1 MEDIUM (M293).
- **STRICT94** (the strict SA-independent core) — register
  category ∉ {SA_DERIVED, SA_CONFIRMED_ONLY} ∧ `sa_in_chain ==
  false` ∧ tier ∈ {HIGH, MEDIUM}, the Phase-109 rebase definition.
  Asserted: |STRICT94| = 94 (90 HIGH + 4 MEDIUM); disjoint from
  FLAGGED44; Holdat token coverage 5,159 / 7,002 = 0.7368
  (recomputed; recorded, tolerance ±0.001 for the assertion).
- **KUR113** (negative control) — anchors with
  `validation_status == "premise_superseded"` (Phase-110: readings
  copied verbatim from donor sign M222 by the allograph mechanism;
  all 113 read `kur`). Asserted: |KUR113| = 113, all readings
  `kur`.

## 3. The battery (frozen)

Conventions. A sign's **positional profile** on a corpus counts,
over every inscription of length n ≥ 1 containing it, each token
as INITIAL if position 0 and n > 1, TERMINAL if last position and
n > 1, else MEDIAL (sole tokens count MEDIAL) — the Phase-69 /
provenance-audit convention. Profile = the three shares. **Modal
class** = the largest share; ties break in the fixed order
INITIAL, TERMINAL, MEDIAL. **TV(p, q)** = ½ Σ|pᵢ − qᵢ|. Reading
**normalization** (Phase-58 convention): first `/`-segment,
lowercase, strip characters outside `[a-zāīūēōṅñṭṇṉṟḷḻ]`.

**Syllable canon** (used by T2b (iii) and T3). Phonemes: nuclei
{a, ā, i, ī, u, ū, e, ē, o, ō, ai, au}; consonants {k, ṅ, c, ñ, ṭ,
ṇ, t, n, p, m, y, r, l, v, ḷ, ḻ, ṟ, ṉ}. A string syllabifies by
greedy left-to-right maximal onset with **at most one** onset
consonant per syllable: consonants between two nuclei split as
coda (first) + onset (second); three or more consonants between
nuclei, an initial consonant cluster, or a final consonant
cluster is a parse failure. Legal syllable shapes: V, VC, CV,
CVC. A string is **canon-legal** iff it syllabifies completely.
(Unit-tested at freeze: `kaḷiṟu` → ka-ḷi-ṟu legal; `kur` legal;
`nal` legal; `strī` fails — initial cluster.)

### T1 — Cross-corpus consistency (ICIT layer vs Holdat)

For sign s with ICIT token count n_I(s):

- n_I(s) < 3 → **NOT_ATTESTED**.
- Else PASS iff modal class on ICIT == modal class on Holdat
  **and** TV(profile_ICIT(s), profile_Holdat(s)) ≤ **0.40**;
  otherwise **FAIL**.

### T2 — Positional-grammar fit (Holdat vs STRICT94 grammar)

Guard: Holdat token count n_H(s) < 8 → **INDETERMINATE** (unless
a component below already FAILs — guards gate PASS, never FAIL).

- **T2a (profile fit).** Let k = modal class of s on Holdat.
  Centroid_k = token-weighted mean Holdat profile of STRICT94
  signs whose Holdat modal class is k (leave-one-out: s itself
  excluded when s ∈ STRICT94). PASS_a iff TV(profile_H(s),
  centroid_k) ≤ **0.35** and modal share of s ≥ **0.45**; else
  FAIL_a.
- **T2b (reading–slot phonotactics).** All of: (i)
  `is_valid_dravidian_initial(normalized reading)` is True;
  (ii) the reading's initial phoneme belongs to the set of initial
  phonemes of STRICT94 readings whose signs' Holdat modal class
  is k (skipped — not failed — if that set has < 5 members);
  (iii) the normalized reading is canon-legal. Any failure →
  FAIL_b.
- T2 = **FAIL** if either component FAILs; **PASS** if both PASS
  (guard satisfied); else **INDETERMINATE**.

### T3 — Compositional co-occurrence (Holdat)

- **Partners** of s: STRICT94 signs adjacent to s in a Holdat
  inscription (either side) with co-occurrence count ≥ 2;
  support(s) = number of partners.
- **Contexts** of s: Holdat inscriptions of length ≥ 2
  containing s where every other sign ∈ STRICT94.
  n_ctx(s) = their count; a context is **legal** iff the
  concatenation of the normalized readings of all its signs in
  sequence order (STRICT94 readings for the others, the tested
  reading for s) is canon-legal; f(s) = legal fraction.
- Guard: n_H(s) < 8 → **INDETERMINATE** (unless FAIL below
  applies — it cannot: the FAIL conditions require the
  attestation the guard withholds; with n_H(s) < 8 the outcome is
  INDETERMINATE outright).
- **FAIL** iff support(s) ≤ 1, or (n_ctx(s) ≥ 4 and f(s) <
  **0.75**).
- **PASS** iff support(s) ≥ **3** and n_ctx(s) ≥ **4** and
  f(s) ≥ **0.75**.
- Else **INDETERMINATE**.

No test consults any SA artifact, any anchor's `basis` text, or
any prior phase's verdict about the tested sign. T2/T3 derive the
"grammar" exclusively from STRICT94 corpus behavior and readings.

## 4. Calibration gates (frozen; evaluated BEFORE the 44 are run)

The battery is applied, unchanged, to two calibration sets:

- **Positive:** STRICT94, leave-one-out (each sign tested against
  the core minus itself, for T2a centroid and T3 partner/context
  sets). Acceptance: VALIDATED (§5 rule) share ≥ **60%**
  (≥ 57 of 94).
- **Negative:** KUR113, against STRICT94 as-is. Acceptance:
  VALIDATED count ≤ **5** (of 113).

If either gate fails, the battery is **rejected**: the phase
stops, FLAGGED44 is never run, the anchors file is not modified,
and the results/summary/ledger record the rejection with the
calibration numbers. A rejected battery may not be re-tuned and
re-run under this spec; a redesigned battery requires a new spec.

## 5. Decision rule (frozen; applied mechanically to FLAGGED44)

Per anchor, from (T1, T2, T3) ∈ {PASS, FAIL, NOT_ATTESTED,
INDETERMINATE}:

- **VALIDATED_NON_SA** ⟺ T1 = PASS ∧ T2 = PASS ∧ T3 = PASS.
  Action: `validation_status` := `validated_non_sa`;
  `evidence_ref` appended (Phase-113, spec 011); tier unchanged;
  `phase113_annotation` records the outcome and per-test states.
- **DEMOTE** ⟺ any test = FAIL. Action: `confidence` :=
  CANDIDATE; `validation_status` := `failed_non_sa_validation`;
  annotation records which test(s) failed and their statistics.
- **UNRESOLVED** ⟺ otherwise (no FAIL; at least one
  NOT_ATTESTED / INDETERMINATE). Action: no tier change;
  `validation_status` stays `pending_non_sa_validation`;
  annotation records UNRESOLVED with per-test states.

Every action (and every UNRESOLVED non-action) is one record in
the change register. No other anchor-file field is modified; no
anchor outside FLAGGED44 is modified under any outcome.

## 6. Execution order (frozen)

1. This spec committed alone (pre-registration).
2. Implementation: `backend/glossa_lab/phase113_battery.py`
   (pure machinery), `backend/glossa_lab/phase113_run.py`
   (orchestration + report writing), runner
   `backend/scripts/phase113_nonsa_battery.py`; unit tests
   `backend/tests/test_phase113_battery.py`.
3. H23 gate, in order: script written → graph module
   `backend/glossa_lab/experiment_graph_phase113.py` (node
   `IndusPhase113NonSaValidation`) → registration in
   `experiment_graph.py` → registration asserted in `ATOMIC_NODES`
   → only then any run.
4. Calibration run (§4). If rejected: write reports + ledgers,
   stop (no step 5).
5. Main run on FLAGGED44; apply §5; write reports + change
   register; update the anchors file.
6. Full backend suite + foundation check (H21: anchors file and
   phase reports change). Ruff clean before push.
7. Ledger entries (root `LEDGER.md` and `glossa-indus/LEDGER.md`,
   AI disclosure) and one PR. No merge without the owner's
   explicit say-so.

Determinism: the battery is pure counting and set membership — no
sampling, no RNG, no floating-point accumulation order dependence
beyond corpus order (corpora are read in file order; profiles are
exact rational counts reported rounded to 6 dp). Re-running the
pipeline on the same inputs must reproduce the reports
byte-identically except timestamps.

## 7. Deviations

Any deviation from this spec discovered mid-run is recorded in
the summary and the ledger, not absorbed. Thresholds, guards,
and the decision rule are not adjustable after the freeze commit;
a substantive design error voids the run and requires a new spec
(Phase-111/112 precedent).

## 8. Limitations and epistemic boundaries (H13, registered at freeze)

- **What a PASS means.** The battery certifies that an anchor's
  distributional claims (positional behavior stable across two
  corpora and consistent with the strict core's grammar) and its
  compositional behavior (it sits inside the strict core's
  inscription network forming canon-legal composed readings)
  survive independent non-SA tests. It does **not** prove the
  phonetic value: a phonotactically legal wrong reading attached
  to a well-behaved sign can pass — that residual is exactly what
  the KUR113 calibration gate measures, and the gate, not
  rhetoric, decides whether the battery is strong enough to use.
- **What a FAIL means.** The anchor's claims contradict
  corpus-level evidence or it is distributionally isolated; the
  reading is demoted to CANDIDATE, not declared false.
- **Corpus caveats.** Holdat is a single modern compilation; the
  ICIT layer is a converted, deduplicated subset (1,007 of 5,679
  source inscriptions fully convertible) — T1 NOT_ATTESTED
  outcomes partly measure conversion coverage, not the anchors.
  Both corpora ultimately descend from the same published
  catalogues; "cross-corpus" here means independent compilation
  and numbering pipelines, not independent archaeology.
- **Assumptions declared:** reading order = corpus sequence
  order; the Phase-69 I/M/T convention; the syllable canon of §3
  as the operative Proto-Dravidian syllable law; STRICT94 as a
  valid reference core (itself established by Phase-108/109
  provenance audit, not by this phase).
- **Adversarial challenge:** if STRICT94 were itself
  systematically wrong, T2/T3 would validate conformity to a
  wrong grammar. The calibration asymmetry (kur cohort at ≤ 5,
  strict core at ≥ 60%) is the registered check that the battery
  discriminates lineage rather than merely rewarding frequency:
  KUR113 signs are real signs with real distributions, so a
  battery that validated them wholesale would be measuring
  attestation, not validity — and is rejected by §4 if it does.

## 9. Licensing / data handling

Holdat and the ICIT converted layer are used locally under their
recorded terms (Phase-107 acquisition log); neither is committed
or redistributed by this phase. Published artifacts contain only
counts, shares, distances, and verdicts.

## 10. Deliverables (frozen)

- `specs/011-phase113-nonsa44-validation/{spec,plan,tasks}.md`
- `backend/glossa_lab/phase113_battery.py`,
  `backend/glossa_lab/phase113_run.py`,
  `backend/glossa_lab/experiment_graph_phase113.py` (+ registration)
- `backend/scripts/phase113_nonsa_battery.py`
- `backend/tests/test_phase113_battery.py`
- `reports/phase113_nonsa44_results.json` (sets, calibration,
  per-anchor test states + statistics, outcomes)
- `reports/phase113_nonsa44_change_register.json` (one record
  per FLAGGED44 anchor)
- `reports/phase113_nonsa44_summary.md`
- Anchors-file changes per §5 (if calibration passes)
- Ledger entries in `LEDGER.md` and `glossa-indus/LEDGER.md`
- One PR; suite + foundation results recorded in the summary

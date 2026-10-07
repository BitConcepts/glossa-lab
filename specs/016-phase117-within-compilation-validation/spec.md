# Spec 016 — Phase-117: Within-Compilation Validation Battery for the 44 Flagged Anchors (pre-registration)

**Status:** DESIGN FROZEN 2026-10-07 on
`phase/within-compilation-battery-design` (from main `83d03672`).
Owner authorization: Tristen Pierson, 2026-10-07 — for the
**design** of this battery. **This spec's merge does not
authorize execution.** Execution requires the owner's separate,
explicit approval after this design PR is reviewed; until then
no instrument in this spec may be run against any anchor, and
the calibration gates of §6 may not be evaluated. This spec is
committed before any battery statistic exists under it: the
only numbers computed at design stage are the instrument
feasibility statistics of Appendix A (attestation counts and
judgeability under the frozen definitions — no sign is scored,
no profile is compared, no verdict is produced), finalized in
the commit immediately following this freeze, per the program's
pre-freeze measurement precedent (spec 014 §§1–2).

**Coordination note:** this branch was cut from main `83d03672`
while an owner-authorized history rewrite (purging six
restricted files already absent at HEAD) was in flight. HEAD
tree content is identical pre/post rewrite; if the rewrite has
landed by merge time, this branch rebases onto the rewritten
main mechanically.

**Phase-numbering note:** ledger-sequence **Phase-117**
(Phase-113 spec 011, Phase-114 spec 012, Phase-115 spec 014,
Phase-116 spec 015 precede it). Artifact names carry the phase
number (`phase117_battery`, `phase117_run`, graph node
`IndusPhase117WithinCompilationValidation`).

**AI disclosure:** this study is designed for execution by an
AI agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

## Context — why this phase exists, and what the record now forbids and licenses

Three frozen batteries/studies frame this design:

- Phase-113 (spec 011) and Phase-115 (spec 014) froze non-SA
  validation batteries for the 44 anchors Phase-109 flagged
  `pending_non_sa_validation` (43 HIGH + M293 MEDIUM; provenance
  SA_DERIVED 24 ∪ SA_CONFIRMED_ONLY 20, per Phase-108). Both
  were **REJECTED at calibration** — v1 because its cross-corpus
  test (T1) starved on a sparse converted layer, v2 because,
  on a rebuilt layer, Holdat and ICIT positional profiles
  genuinely disagree (43/94 strict signs FAIL, median TV 0.79).
  In both, the Holdat-internal tests were never the problem:
  T2's profile-fit component passed 91/94 strict signs, and
  T3's binding constraint was partner support, not legality.
- Phase-116 (spec 015) then asked *why* the compilations
  disagree and returned **R-NONE**: no harmonization
  transformation is justified; H-MAPPING and H-DEFINITION are
  refuted (the disagreement is diffuse across signs and
  survives continuous relative-position measurement, Spearman
  ρ = −0.0826); composition, segmentation, and direction are
  unresolved at frozen power. Its recorded recommendation,
  which this spec obeys as a hard constraint:

  > "A future validation battery must not use a conjunctive
  > cross-corpus positional gate on this pair; validation must
  > proceed within a single compilation or await a genuinely
  > independent corpus."

This phase takes the licensed branch of that disjunction: a
battery whose every instrument lives **inside Holdat**, under
split-half discipline where derivation and scoring would
otherwise share tokens. It validates or demotes; it never
promotes. What a pass means — and, load-bearing, what it does
**not** mean — is defined in §9 and is part of the frozen
design, not commentary.

**Fate of the spec-011 components** (recorded so nothing is
silently dropped or silently kept):

| Spec-011 component | Fate in this spec | Basis |
|---|---|---|
| T1 cross-corpus consistency | **Forbidden; not carried over** | Phase-116 R-NONE |
| T2a positional profile fit | → **W1**, rebuilt as split-half cross-fit | T2a was sound (91/94); the full-corpus derive-and-test-on-same-tokens pattern is replaced by cross-half derivation/scoring |
| T2b reading–slot phonotactics | **Dropped** | Its failures in v1/v2 were 12/13 driven by class-initial-inventory membership — a brittle set-membership test; its evidentiary content (does the reading fit the core's sequential fabric?) is superseded by W3's null-tested junction model |
| T3 compositional co-occurrence | → **W2: DROPPED as a decision-bearing instrument** (§4.2) | Appendix A numbers: only 5/44 anchors can reach its PASS prerequisites; composed-legality base rate on strict-core inscriptions is 1.000 (523/523), so its legality component carries no discriminative content; its PASS is a frequency proxy. Its support counts are recorded descriptively by W3; its legality content is absorbed into W3's null framework |
| Calibration gates (§4 of 011) | → §6, same pattern, numbers re-frozen for split-half power | — |
| Decision rule (§5 of 011) | → §8 rule structure, new status value (§8/§9) | — |

Governance rule **H26** still frames the question: no SA
output, SA score, SA-derived language model, or SA modal
reading is an input to any instrument in this battery.

## 1. Data (frozen inputs)

| Input | Path | Role |
|---|---|---|
| Anchors (287) | `backend/reports/INDUS_FINAL_ANCHORS.json` | target + calibration sets; the only file an execution may modify, and only per §8 |
| Provenance register | `reports/phase108_provenance_register.json` | set definitions (category, `sa_in_chain`) |
| Holdat corpus | `corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv` (gitignored; located in the main checkout) | the sole corpus for W1–W4; loaded with the `load_holdat_corpus` machinery of `glossa_lab/pipelines/sa_validation.py` (loader only — no SA code is executed) |

Holdat, as loaded: **1,670 inscriptions / 7,002 tokens**,
inscription lengths 2–8 (no single-token inscriptions exist),
9 sites (Mohenjo-daro 606 inscriptions, Harappa 492, all
others ≤ 124). Per-inscription site is taken from the CSV
`site` field of its rows (constant within a `cisi_number`
group under the loader's grouping). **No other corpus is an
input to any instrument.** The ICIT converted layers (v1, v2)
are not loaded, read, or consulted anywhere in this phase
(Phase-116 constraint).

Holdat is used locally under its recorded terms (Phase-107
acquisition log); it is never committed or redistributed.
Published artifacts contain only counts, shares, distances,
scores, and verdicts.

## 2. Sets (frozen definitions; recomputed at run time and asserted — spec 011 §2 verbatim)

- **FLAGGED44** — anchors with
  `validation_status == "pending_non_sa_validation"`. Asserted:
  |FLAGGED44| = 44; equals register categories SA_DERIVED (24)
  ∪ SA_CONFIRMED_ONLY (20); tiers 43 HIGH + 1 MEDIUM (M293).
- **STRICT94** (the strict SA-independent core) — register
  category ∉ {SA_DERIVED, SA_CONFIRMED_ONLY} ∧ `sa_in_chain ==
  false` ∧ tier ∈ {HIGH, MEDIUM}. Asserted: |STRICT94| = 94
  (90 HIGH + 4 MEDIUM); disjoint from FLAGGED44; Holdat token
  coverage 5,159 / 7,002 = 0.7368 (tolerance ±0.001).
- **KUR113** (negative control) — anchors with
  `validation_status == "premise_superseded"`; asserted
  |KUR113| = 113, all readings `kur`, all Holdat counts ≤ 4.

Calibration sets are evaluated read-only; their anchors are
never modified by this phase.

## 3. Conventions (frozen)

Positional profiles, modal class, tie order (INITIAL,
TERMINAL, MEDIAL), TV distance, reading normalization, the
phoneme inventory, and the syllable canon are spec 011 §3
verbatim, implemented by reusing `phase113_battery` machinery
(profiles, `normalize_reading`, `canon_legal`). A sign's
**initial phoneme** / **final phoneme** are the first / last
phonemes of its normalized reading under the §3 tokenizer.

**The frozen partition (W1).** Holdat inscriptions are
assigned to halves A and B as follows, with no free choices:
strata are the 15 cells of (length bin ∈ {2, 3, 4, 5, 6+} ×
site group ∈ {Mohenjo-daro, Harappa, OTHER}); within each
stratum, inscriptions are taken in the loader's inscription
order (first-appearance order of `cisi_number` groups in the
CSV — the order `load_holdat_corpus` emits), shuffled
with Python `random.Random(117).shuffle` (strata processed in
sorted (length bin, site group) key order, one RNG stream),
and dealt alternately A, B, A, B, … beginning with A. The
partition is a design constant of this spec: it is identical
for calibration and the main run, is never re-drawn, and its
design-stage token totals are A = 3,531 / B = 3,471
(Appendix A). An execution must reproduce these totals
exactly and assert them before any instrument runs.

**Seeded streams.** Three independent RNG streams, all seeded
117: (i) the partition shuffle (§3); (ii) W3 donor draws (§4.3)
via `random.Random(117)` instantiated separately from the
partition stream; (iii) no other randomness exists in the
battery. Determinism: re-running an execution on the same
inputs reproduces its reports byte-identically except
timestamps.

## 4. The battery (frozen)

Every instrument returns one state per tested sign from
{PASS, FAIL, INDETERMINATE}. Guards gate PASS and FAIL alike:
an instrument that cannot judge returns INDETERMINATE and
records its reason; no instrument consults any SA artifact,
any anchor's `basis` text, any ICIT artifact, or any prior
phase's verdict about the tested sign.

### 4.1 W1 — Split-half positional cross-fit

The cross-fit replacement for T2a. For direction A→B: the
positional model is derived on half A and the tested sign is
scored on half B; direction B→A symmetrically.

- **Model (per half).** For each modal class k, the centroid
  is the token-weighted mean Holdat positional profile of
  STRICT94 signs whose modal class **on that half** is k,
  over core signs with ≥ 1 token on that half. Under
  leave-one-out (STRICT94 calibration), the tested sign is
  excluded from its own model.
- **Per-direction state** for sign s, scoring half S, model
  half M: if n_S(s) < **4** → INDETERMINATE
  (`half_count_below_floor`). Else let m = modal class of
  s's profile on S; if no core sign has modal class m on M
  (no centroid exists) → INDETERMINATE
  (`centroid_undefined`). Else PASS iff
  TV(profile_S(s), centroid^M_m) ≤ **0.35** and modal
  share_S(s) ≥ **0.45**; else FAIL. (Thresholds are T2a's,
  carried over unchanged: T2a was the one component two
  batteries measured as sound, and its numbers are not
  re-tuned here.)
- **Combination.** W1 = FAIL iff either direction FAILs;
  PASS iff both directions PASS; else INDETERMINATE.

### 4.2 W2 — Iconographic co-occurrence (spec-011 T3 design): DROPPED

**Frozen decision: W2 is not an instrument of this battery.**
It produces no state, gates nothing, and appears in no
decision rule. Basis (Appendix A, computed from Holdat counts
under T3's own definitions):

- Only **5 of 44** flagged anchors can reach T3's PASS
  prerequisites (support ≥ 3 strict partners at
  co-occurrence ≥ 2, and ≥ 4 all-strict contexts); 27 of 44
  sit at support ≤ 1 — T3's FAIL zone — for reasons of
  attestation, not evidence: STRICT94 itself has 38 of 94
  signs at support ≤ 1 and only 34 of 94 PASS-capable, so
  T3's support axis measures corpus frequency, not lineage.
- T3's legality axis has no discriminative content in this
  corpus: the composed-legality base rate over all-STRICT94
  inscriptions of length ≥ 2 is **1.000 (523/523)** — the
  component that "never fired" in Phases 113 and 115 cannot
  fire here either.

Component fates: partner support and context counts are
recorded as descriptive statistics in the W3 record (never
gated); composed legality is recorded descriptively in W3
(§4.3) and is likewise never gated. If future corpora change
the base rates, a co-occurrence instrument may be proposed
under a new spec; it may not be reintroduced under this one.

### 4.3 W3 — Distributional-neighborhood coherence (junction model with donor-permutation null)

Tests whether the tested sign's observed Holdat bigram
neighborhood is better explained under its proposed reading's
sequential profile than under readings donated by
comparably-attested anchored signs.

- **Junction observations** of s: every ordered adjacent
  pair (x, s) and (s, y) in a Holdat inscription with the
  other sign ∈ STRICT94 (under leave-one-out, the core minus
  the tested sign). n_j(s) = their count. Guard:
  n_j(s) < **6** → INDETERMINATE (`junction_floor`); no FAIL
  is possible below the floor.
- **Junction model.** Over all ordered adjacent pairs
  (u, v) with u, v ∈ core: counts C(f, i) of
  (final phoneme of u's reading, initial phoneme of v's
  reading). P(f, i) = (C(f, i) + 0.5) / (N + 0.5·|G|), where
  N = total core junction count and G = the grid
  (attested final phonemes of core readings) × (attested
  initial phonemes of core readings). Under leave-one-out
  the model is built without the tested sign.
- **Score.** score(s) = mean over s's junction observations
  of log P(final phoneme of left reading, initial phoneme of
  right reading), with s's proposed reading supplying its
  own initial/final phonemes and each STRICT94 neighbor its
  core reading.
- **Absolute floor φ.** φ = the 10th percentile of STRICT94
  leave-one-out self-scores (each strict sign scored by this
  same instrument against the core minus itself). φ is a
  definition, frozen here; its value is computed inside the
  calibration run, before the §6 gates are evaluated, and
  recorded in the results. (Precedent: spec 011's
  corpus-derived centroids and initial-phoneme inventories.)
- **Donor-permutation null.** B = **999** replicates. Each
  replicate draws one donor reading uniformly (seeded stream
  (ii), §3) from the readings of anchored signs t ≠ s (all
  287 anchor entries) with Holdat count n_H(t) ∈
  [⌈n_H(s)/3⌉, 3·n_H(s)], and recomputes score(s) with the
  donor's initial/final phonemes substituted for s's own
  (neighbors and positions unchanged). If the donor band is
  empty → INDETERMINATE (`donor_band_empty`).
  p(s) = (1 + #{b : score_b ≥ score(s)}) / (1 + B).
- **State.** PASS iff p(s) ≤ **0.05** and score(s) ≥ φ.
  FAIL iff p(s) ≥ **0.50** and score(s) < φ. Else
  INDETERMINATE.
- **Recorded descriptively (never gated):** partner support
  and context counts (§4.2), and the composed-legality
  fraction of s's length-≥2 inscriptions under the anchor
  readings (the §4.2 base-rate statistic, per-sign).

### 4.4 W4 — Stratum stability (site strata within Holdat)

Holdat carries site per inscription and no material field;
the frozen strata are **sites**. (The absence of a material
field is a data limitation, recorded here: "site/material"
in the design charge is discharged as site strata, the only
artifact stratum Holdat encodes. Iconography is a motif
classification, not an artifact stratum, and is not used.)

- **Qualifying stratum** for s: a site with n_site(s) ≥
  **4** tokens of s. Guard: fewer than 2 qualifying strata
  → INDETERMINATE (`strata_below_two`).
- **PASS** iff the modal class of s is identical across all
  qualifying strata and every pairwise TV between
  qualifying-stratum profiles ≤ **0.40**.
- **FAIL** iff two qualifying strata with n_site(s) ≥ **8**
  each disagree in modal class. (FAIL deliberately requires
  the stronger attestation: a modal flip between thin strata
  is sampling noise, not instability — Appendix A: only
  M293 among the 44, and 20 of STRICT94, are FAIL-capable at
  all.)
- Else INDETERMINATE (modal disagreement not meeting the
  FAIL attestation bar, or modal agreement with a pairwise
  TV > 0.40).

## 5. Sparsity rules (frozen; consolidated)

Insufficient data maps to INDETERMINATE per instrument,
mechanically, with the recorded reason — never to a judgment
call, never post-hoc:

| Instrument | Insufficient-data condition | State |
|---|---|---|
| W1 | n < 4 in a scoring half, or centroid undefined for the direction | direction INDETERMINATE (`half_count_below_floor` / `centroid_undefined`) |
| W3 | n_j(s) < 6, or donor band empty | INDETERMINATE (`junction_floor` / `donor_band_empty`) |
| W4 | < 2 sites with ≥ 4 tokens | INDETERMINATE (`strata_below_two`) |

Design-stage expectations under these rules (Appendix A):
W1 can fully judge (both directions) 13/44 flagged anchors,
W3 can judge 40/44, W4 can judge 9/44; **41/44 are judgeable
by at least one instrument**; M235, M254, M402 are judgeable
by none and are therefore UNRESOLVED by construction under
§8 — recorded now, before any run, so their outcome is a
property of the frozen design, not a result. The battery's
decisiveness rests on W3 (27/44 are judgeable by W3 alone);
this concentration is a registered limitation (§10).

## 6. Calibration gates (frozen; evaluated BEFORE the 44 are run, and only under a separate execution approval)

The battery is applied, unchanged, to the two calibration
sets, with φ computed from STRICT94 leave-one-out self-scores
first (§4.3):

- **Positive:** STRICT94, leave-one-out throughout.
  Acceptance: VALIDATED (§8 rule) count ≥ **47 of 94**
  (50%). Basis: W3 is judgeable on 81/94 and W1 on 68/94 of
  the core (Appendix A), so the gate is not sparsity-capped;
  50% under split-half discipline — where every judgment is
  made on half the attestation the v1/v2 full-corpus
  batteries used — is set as the demanding analogue of
  their 60% bar, not a relaxation of it: the v1/v2 positive
  controls in fact achieved 3/94 and 1/94.
- **Negative:** KUR113, against STRICT94 as-is. Acceptance:
  VALIDATED count ≤ **5 of 113** (the spec-011/014 bar,
  unchanged). Registered honestly: the gate's teeth are
  W3's — KUR113 signs are W1-unjudgeable wholesale (all
  counts ≤ 4) and W3-judgeable in 24/113 cases; a battery
  whose W3 validated known-bad readings at rate would fail
  here, and one that merely refuses them passes — the same
  asymmetry Phases 113/115 recorded, accepted at freeze
  because the positive gate is the binding one.

If either gate fails, the battery is **rejected**: the
execution stops, FLAGGED44 is never run, the anchors file is
not modified, and the results/summary/ledger record the
rejection with the calibration numbers. A rejected battery
may not be re-tuned and re-run under this spec; a redesigned
battery requires a new spec. No threshold, floor, band, or
gate in §§3–8 is adjustable after this freeze.

## 7. (Reserved)

Numbering note: calibration gates are §6; the decision rule
is §8; anti-circularity and claim scope are §9. (Sections
numbered to keep gates adjacent to the instruments they
govern; no content is omitted.)

## 8. Decision rule (frozen; applied mechanically to FLAGGED44, only if both §6 gates pass)

Per anchor, from (W1, W3, W4) ∈ {PASS, FAIL, INDETERMINATE}:

- **VALIDATED** ⟺ W3 = PASS ∧ (W1 = PASS ∨ W4 = PASS) ∧
  no instrument = FAIL. Action: `validation_status` :=
  `validated_within_compilation` (§9 defines this value);
  `evidence_ref` appended (Phase-117, spec 016); tier
  unchanged; `phase117_annotation` records the outcome and
  per-instrument states and statistics.
- **DEMOTE** ⟺ any instrument = FAIL. Action: `confidence`
  := CANDIDATE; `validation_status` :=
  `failed_within_compilation_validation`; annotation records
  which instrument(s) failed and their statistics.
- **UNRESOLVED** ⟺ otherwise (no FAIL; the VALIDATED
  conjunction unmet — including all-INDETERMINATE).
  Action: no tier change; `validation_status` stays
  `pending_non_sa_validation`; annotation records UNRESOLVED
  with per-instrument states and reasons.

The VALIDATED conjunction is deliberately asymmetric, and
the reason is frozen with it: W3 is the only instrument
judgeable on 40/44 (Appendix A), so requiring any single
positional instrument's PASS conjunctively would cap
validation by sparsity rather than by evidence — the exact
failure mode of the v1/v2 conjunctive gates — while
requiring W3's PASS plus at least one positional PASS,
with every instrument holding veto (FAIL) power, keeps each
validation supported by two independent instrument families
and each demotion supported by a positive contradiction.

Every action (and every UNRESOLVED non-action) is one record
in the change register. No other anchor-file field is
modified; no anchor outside FLAGGED44 is modified under any
outcome; **this phase never promotes any anchor's tier**.

## 9. Anti-circularity and claim scope (frozen; load-bearing)

Within-compilation validation is **not** independence. The
44 anchors' SA lineage was derived against this same
compilation; STRICT94's readings — the reference fabric for
W1's centroids, W3's junction model, and W4's strata — are
themselves decipherment claims carried in the same anchor
table. Split-half discipline (W1) and leave-one-out
calibration remove the mechanical self-agreement of
derive-and-test-on-identical-tokens; they cannot manufacture
an independent witness. This section defines, immutably for
this spec, what outcomes mean:

- The success status value is
  **`validated_within_compilation`** — a new value, coined
  here. It must not be shortened to `validated`, must not be
  conflated with spec 011/014's `validated_non_sa` (a status
  no battery has ever awarded), and must not be described in
  any report, summary, ledger, paper, or preprint as
  "independent validation", "external validation", or
  "confirmation" of a reading.
- A VALIDATED outcome supports exactly this claim: **the
  anchor's reading and positional behavior are internally
  coherent with the strict SA-independent core's
  distributional and sequential fabric inside Holdat, under
  split-half and permutation-null discipline, at the frozen
  thresholds.** It supports no claim about the reading's
  phonetic correctness, and no claim of independence from
  the derivation compilation.
- The anchors' provenance categories (SA_DERIVED /
  SA_CONFIRMED_ONLY) are **not** altered by any outcome of
  this phase: the register's record that these values arrived
  via the SA lineage stands permanently. A
  `validated_within_compilation` anchor remains an SA-lineage
  anchor that has additionally passed an internal-coherence
  battery — both facts travel together in any publication.
- A DEMOTE outcome supports exactly: the anchor's claims
  contradict Holdat-internal evidence (cross-half positional
  fit, null-tested neighborhood coherence, or stratum
  stability) at the frozen thresholds. It demotes to
  CANDIDATE; it does not declare the reading false.
- Any genuinely independent corpus test (e.g. RMRL or Mitra
  data, when and if obtained) **supersedes** this battery's
  outcomes for any anchor it can judge: within-compilation
  statuses are explicitly provisional against independent
  evidence, and a future spec must say how conflicts resolve
  before it runs. This battery's outcomes never satisfy
  governance rule H26's non-SA-evidence bar for promotion —
  and this phase promotes nothing in any case.

## 10. Limitations (registered at freeze)

- **Single-compilation ceiling (§9):** every instrument
  measures coherence inside one modern compilation of the
  same published catalogues. Systematic error in Holdat, or
  in STRICT94's readings, is invisible to this battery by
  construction; the calibration asymmetry (core ≥ 50%, kur
  cohort ≤ 5) checks discrimination, not truth.
- **W3 concentration:** 27/44 anchors are judgeable by W3
  alone; the battery's verdicts on the rare-sign majority
  rest disproportionately on one instrument family. The
  §8 conjunction (a positional PASS is also required) is
  the registered mitigation; anchors failing it for sparsity
  are UNRESOLVED, not validated.
- **W1 power:** split-half cross-fit judges 13/44 fully;
  its veto (single-direction FAIL) reaches further than its
  PASS. Registered, not repaired: rebalancing the partition
  post-freeze is forbidden.
- **Negative-gate asymmetry:** KUR113 is largely
  unjudgeable (W1 0/113, W3 24/113); the negative gate
  verifies non-validation of the judgeable minority and
  silence on the rest (§6).
- **Junction-model dependence on core readings:** W3's model
  is built from STRICT94 *readings* — if core readings were
  systematically wrong in a phoneme-class-preserving way,
  W3 would reward conformity to that wrongness. The donor
  null bounds the effect to frequency-band-typical readings,
  not to zero.
- **Strata:** W4 uses site only (no material field exists
  in Holdat); site is confounded with excavation/publication
  history. FAIL-capability is nearly confined to M293
  among the 44 (§4.4).
- **Assumptions declared:** reading order = corpus sequence
  order; the Phase-69 I/M/T convention; the §3 syllable
  canon as the operative phonotactic frame (used only via
  the tokenizer's phoneme segmentation); STRICT94 as a
  valid reference core (established by the Phase-108/109
  provenance audit, not by this phase).

## 11. Execution order (frozen; every step gated on the owner's separate execution approval)

1. This spec committed alone (design pre-registration) —
   **this PR**. Merge of this PR constitutes design
   acceptance only.
2. On separate owner approval: implementation —
   `backend/glossa_lab/phase117_battery.py` (pure machinery:
   partition, W1, W3, W4, decision rule),
   `backend/glossa_lab/phase117_run.py` (orchestration +
   report writing), runner
   `backend/scripts/phase117_within_battery.py`; unit tests
   `backend/tests/test_phase117_battery.py` (including toy
   end-to-end controls: a synthetic core-coherent reading
   validates; a synthetic incoherent reading does not).
3. H23 gate, in order: script written → graph module
   `backend/glossa_lab/experiment_graph_phase117.py` (node
   `IndusPhase117WithinCompilationValidation`) → registration
   in `experiment_graph.py` → registration asserted in
   `ATOMIC_NODES` → only then any run. Partition totals
   asserted (§3) before calibration.
4. Calibration (§6): φ computed; STRICT94 LOO and KUR113
   evaluated; gates checked. If rejected: write reports +
   ledgers, stop (no step 5).
5. Main run on FLAGGED44; apply §8; write reports + change
   register; update the anchors file (changed entries ==
   change-register signs, asserted).
6. Full backend suite + foundation check (H21: anchors file
   and phase reports change). Ruff clean before push.
7. Ledger entries (root `LEDGER.md` and
   `glossa-indus/LEDGER.md`, AI disclosure) and one PR. No
   merge without the owner's explicit say-so.

## 12. Deviations

Any deviation from this spec discovered during an execution
is recorded in the summary and the ledger, not absorbed.
Thresholds, floors, bands, the partition, the seeds, and the
decision rule are not adjustable after the freeze commit; a
substantive design error voids the design and requires a new
spec (Phase-111/112 precedent).

## 13. Deliverables (frozen)

Design phase (this PR):

- `specs/016-phase117-within-compilation-validation/{spec,plan,tasks}.md`
  (spec freeze commit, then Appendix A finalized in the
  following commit)
- Ledger entries in `LEDGER.md` and `glossa-indus/LEDGER.md`
  (design only)
- One PR, titled as a design PR; no execution artifacts

Execution phase (only under separate owner approval):

- `backend/glossa_lab/phase117_battery.py`,
  `backend/glossa_lab/phase117_run.py`,
  `backend/glossa_lab/experiment_graph_phase117.py`
  (+ registration)
- `backend/scripts/phase117_within_battery.py`
- `backend/tests/test_phase117_battery.py`
- `reports/phase117_within_battery_results.json` (sets,
  partition assertion, φ, calibration, per-anchor instrument
  states + statistics, outcomes)
- `reports/phase117_within_battery_change_register.json`
  (iff the main run executes)
- `reports/phase117_within_battery_summary.md`
- Anchors-file changes per §8 (iff calibration passes)
- Ledger entries; suite + foundation results recorded in the
  summary

## Appendix A — Design-stage feasibility (instrument statistics only)

*Finalized in the commit following the freeze. Preamble and
boundary: every number in this appendix is an attestation
count or a judgeability determination under the frozen
definitions of §§2–5, computed from the Holdat corpus and the
anchors file at design stage. No instrument scored any sign;
no profile was compared to any model; no verdict exists in
this appendix. Per-anchor rows are counts, not results.*

### A.1 Corpus and sets

Holdat as loaded (§1): 1,670 inscriptions / 7,002 tokens;
lengths 2–8 (269 / 330 / 415 / 330 / 164 / 116 / 46
inscriptions of length 2 / 3 / 4 / 5 / 6 / 7 / 8); 9 sites —
Mohenjo-daro 606, Harappa 492, Lothal 124, Kalibangan 110,
Dholavira 106, Chanhu-daro 78, Surkotada 61, Banawali 60,
Rakhigarhi 33 inscriptions.

| Set | n | Holdat tokens per sign (min / median / mean / max) |
|---|---|---|
| FLAGGED44 | 44 | 4 / 6 / 13.3 / 232 (M293; next-largest 21) |
| STRICT94 | 94 | 1 / 17 / 54.9 / 584 (coverage 5,159 / 7,002 = 0.7368) |
| KUR113 | 113 | 1 / 3 / 2.8 / 4 |

The 44 are a rare-sign cohort: excluding M293, every flagged
anchor has ≤ 21 Holdat tokens. Every frozen floor in §§4–5
is set against this distribution.

### A.2 W1 — the frozen partition and cross-fit judgeability

Partition per §3 (15 strata; seed 117): half A = 3,531
tokens, half B = 3,471 tokens. Fully judgeable = ≥ 4 tokens
in **both** halves (both cross-fit directions scorable);
a FAIL can additionally arise from a single scorable
direction (§4.1 combination rule).

| Per-half floor | FLAGGED44 | STRICT94 | KUR113 |
|---|---|---|---|
| ≥ 4 (frozen) | **13 / 44** | **68 / 94** | 0 / 113 |
| ≥ 5 | 9 / 44 | 65 / 94 | 0 / 113 |
| ≥ 6 | 8 / 44 | 58 / 94 | 0 / 113 |
| ≥ 8 | 4 / 44 | 40 / 94 | 0 / 113 |

### A.3 W2 — keep/drop computation (spec-011 T3 definitions)

| Quantity | FLAGGED44 | STRICT94 | KUR113 |
|---|---|---|---|
| PASS-capable (support ≥ 3 ∧ contexts ≥ 4) | **5 / 44** | 34 / 94 | 0 / 113 |
| Support ≤ 1 (T3's FAIL zone) | 27 / 44 | 38 / 94 | 109 / 113 |
| Median support / median contexts | 1 / 2 | 2 / 6 | 0 / 1 |

Composed-legality base rate (all-STRICT94 inscriptions of
length ≥ 2, core readings composed in sequence order):
**523 / 523 = 1.000 canon-legal.** Conclusion frozen in
§4.2: W2 is dropped as a decision-bearing instrument; its
PASS axis is attestation volume and its legality axis is
saturated in this corpus.

### A.4 W3 / W4 judgeability

W3 junction observations (other sign ∈ STRICT94), floor
n_j ≥ 6 frozen (§4.3):

| Floor | FLAGGED44 | STRICT94 | KUR113 |
|---|---|---|---|
| ≥ 4 | 43 / 44 | 89 / 94 | 59 / 113 |
| **≥ 6 (frozen)** | **40 / 44** | **81 / 94** | **24 / 113** |
| ≥ 8 | 24 / 44 | 72 / 94 | 2 / 113 |

Floor 6 is the frozen compromise: floor 4 admits 4-observation
means whose permutation p-values cannot resolve the §4.3
bands; floor 8 would silence the negative control (2/113)
and halve the flagged cohort's coverage. At floor 6 the
negative control retains 24 judgeable members — the §6
gate's teeth.

W4 (≥ 2 sites with ≥ 4 tokens of the sign): judgeable
**9 / 44** flagged, 57 / 94 STRICT94. FAIL-capable
(≥ 2 sites with ≥ 8 tokens): **1 / 44** (M293), 20 / 94
STRICT94 — the basis for §4.4's asymmetric FAIL.

**Battery-level split of the 44:** judgeable by ≥ 1
instrument **41 / 44**; judgeable by W3 alone 27 / 44;
judgeable by none — M235, M254, M402 — hence UNRESOLVED
by construction under §8 (§5).

### A.5 Per-anchor attestation table (FLAGGED44; counts only)

nH = Holdat tokens; A/B = frozen-partition half counts;
W1 = both halves ≥ 4; supp = STRICT94 partners at
co-occurrence ≥ 2; ctx = all-strict contexts (length ≥ 2);
bi = junction observations (other sign ∈ STRICT94);
W3 = bi ≥ 6; sites4 = sites with ≥ 4 tokens; W4 = sites4 ≥ 2.

| Sign | Tier | Reading | nH | A | B | W1 | supp | ctx | bi | W3 | sites4 | W4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M011 | HIGH | kaḷiṟu | 15 | 10 | 5 | ✓ | 2 | 9 | 11 | ✓ | 1 | – |
| M021 | HIGH | kō | 16 | 10 | 6 | ✓ | 1 | 7 | 8 | ✓ | 1 | – |
| M024 | HIGH | nē | 13 | 12 | 1 | – | 1 | 4 | 7 | ✓ | 2 | ✓ |
| M028 | HIGH | cōḻ | 11 | 4 | 7 | ✓ | 0 | 4 | 5 | – | 1 | – |
| M031 | HIGH | kai | 16 | 9 | 7 | ✓ | 2 | 7 | 11 | ✓ | 2 | ✓ |
| M033 | HIGH | puli | 12 | 5 | 7 | ✓ | 3 | 8 | 9 | ✓ | 1 | – |
| M035 | HIGH | po | 19 | 11 | 8 | ✓ | 3 | 8 | 14 | ✓ | 2 | ✓ |
| M036 | HIGH | tiru | 15 | 9 | 6 | ✓ | 2 | 7 | 10 | ✓ | 2 | ✓ |
| M040 | HIGH | ri | 13 | 7 | 6 | ✓ | 2 | 6 | 7 | ✓ | 2 | ✓ |
| M058 | HIGH | ke | 21 | 8 | 13 | ✓ | 3 | 8 | 14 | ✓ | 2 | ✓ |
| M071 | HIGH | nal | 16 | 9 | 7 | ✓ | 3 | 9 | 12 | ✓ | 2 | ✓ |
| M072 | HIGH | mā | 12 | 8 | 4 | ✓ | 2 | 7 | 8 | ✓ | 2 | ✓ |
| M102 | HIGH | ni | 8 | 5 | 3 | – | 4 | 1 | 12 | ✓ | 0 | – |
| M103 | HIGH | kol | 5 | 2 | 3 | – | 2 | 2 | 7 | ✓ | 0 | – |
| M127 | HIGH | vē | 6 | 2 | 4 | – | 0 | 2 | 8 | ✓ | 0 | – |
| M149 | HIGH | or | 7 | 4 | 3 | – | 2 | 4 | 12 | ✓ | 0 | – |
| M153 | HIGH | pu | 5 | 4 | 1 | – | 1 | 3 | 8 | ✓ | 0 | – |
| M155 | HIGH | ka | 5 | 4 | 1 | – | 1 | 3 | 9 | ✓ | 0 | – |
| M168 | HIGH | inci | 6 | 5 | 1 | – | 0 | 2 | 6 | ✓ | 0 | – |
| M169 | HIGH | rā | 8 | 3 | 5 | – | 2 | 2 | 12 | ✓ | 0 | – |
| M177 | HIGH | na | 5 | 5 | 0 | – | 1 | 1 | 7 | ✓ | 0 | – |
| M178 | HIGH | i | 5 | 4 | 1 | – | 1 | 3 | 8 | ✓ | 0 | – |
| M183 | HIGH | vēḷ | 5 | 2 | 3 | – | 1 | 1 | 6 | ✓ | 0 | – |
| M223 | HIGH | muḷ | 5 | 1 | 4 | – | 0 | 2 | 7 | ✓ | 0 | – |
| M235 | HIGH | vē | 7 | 3 | 4 | – | 1 | 1 | 4 | – | 0 | – |
| M237 | HIGH | ce | 8 | 4 | 4 | ✓ | 2 | 1 | 11 | ✓ | 1 | – |
| M239 | HIGH | il | 5 | 2 | 3 | – | 0 | 3 | 7 | ✓ | 0 | – |
| M254 | HIGH | tēṉ | 5 | 1 | 4 | – | 1 | 1 | 4 | – | 0 | – |
| M262 | HIGH | i | 5 | 2 | 3 | – | 1 | 0 | 7 | ✓ | 0 | – |
| M270 | HIGH | muḷ | 6 | 3 | 3 | – | 1 | 1 | 7 | ✓ | 0 | – |
| M272 | HIGH | ma | 7 | 5 | 2 | – | 0 | 0 | 7 | ✓ | 1 | – |
| M281 | HIGH | piLLai | 4 | 2 | 2 | – | 0 | 2 | 7 | ✓ | 0 | – |
| M293 | MEDIUM | ta | 232 | 124 | 108 | ✓ | 28 | 94 | 275 | ✓ | 9 | ✓ |
| M304 | HIGH | vēṟ | 5 | 4 | 1 | – | 2 | 2 | 8 | ✓ | 0 | – |
| M332 | HIGH | intu | 6 | 3 | 3 | – | 1 | 1 | 8 | ✓ | 0 | – |
| M345 | HIGH | taṭ | 5 | 1 | 4 | – | 1 | 1 | 6 | ✓ | 0 | – |
| M350 | HIGH | vē | 5 | 1 | 4 | – | 0 | 2 | 8 | ✓ | 0 | – |
| M355 | HIGH | lu | 5 | 4 | 1 | – | 0 | 1 | 8 | ✓ | 0 | – |
| M365 | HIGH | vāṉ | 5 | 5 | 0 | – | 1 | 3 | 9 | ✓ | 0 | – |
| M383 | HIGH | kol | 7 | 2 | 5 | – | 2 | 1 | 11 | ✓ | 1 | – |
| M401 | HIGH | vē | 6 | 4 | 2 | – | 0 | 1 | 7 | ✓ | 0 | – |
| M402 | HIGH | vēḷ | 5 | 3 | 2 | – | 0 | 0 | 3 | – | 0 | – |
| M412 | HIGH | cūḷ | 5 | 3 | 2 | – | 1 | 0 | 7 | ✓ | 0 | – |
| M416 | HIGH | na | 5 | 2 | 3 | – | 1 | 1 | 6 | ✓ | 0 | – |

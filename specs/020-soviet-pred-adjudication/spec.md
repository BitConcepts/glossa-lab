# Spec 020 — Adjudication: Does the Soviet Positional Dataset (Phase-121, Kondratov 1965) Qualify as an Evaluation Source for PRED-2026-001/002?

**Status:** ADJUDICATION PAPER — owner-ordered 2026-10-08
(STEP 2 of the Glossa-Lab program), executed on
`spec/020-soviet-adjudication` from `origin/main` `3fd5ad30`
(Step 1, spec 019 / Phase-125, merged). This paper is decided
mechanically from criteria stated in §2, derived from the
registered texts before any application (§4). The verdict is
in §5. No criterion in §2 is outcome-driven: every criterion
cites the registered text it derives from, and §4 applies
each criterion to the established facts of §3 and to nothing
else.

**Scope of the question.** Only PRED-2026-001 and
PRED-2026-002 are adjudicated. PRED-2026-003 and
PRED-2026-004–009 are out of scope and are not touched.

**What this spec may not do.** It may not invent a new
source class, amend the frozen evaluability matrix of
spec 018 §4, invent a new sign map, or re-register either
prediction. Any of those would be re-registration, which is
out of scope for this adjudication (see §6 for what a future
change would require). It may not run the Phase-119 harness
scorers in evaluation mode — or in a labelled dry run — on a
dataset it adjudicates non-qualifying.

**AI disclosure:** this adjudication is executed by an AI
agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

## Epistemic boundaries (H13)

- **Assumptions declared.** (i) The registered texts are
  `docs/PREDICTION_REGISTER.md` §2 (2026-04-23) and
  spec 018 (`specs/018-phase119-pred2026-readiness/spec.md`,
  DESIGN FROZEN 2026-10-07), read in full. (ii) The dataset
  is exactly what Phase-121 committed: the files under
  `data/soviet_positional/` and the memo
  `reports/phase121_soviet_positional_dataset.md`. No
  uncommitted Soviet material is considered. (iii) The
  Phase-119 harness as implemented
  (`backend/glossa_lab/pred_harness.py`) faithfully encodes
  spec 018 §§3–7; where code and spec could differ, the
  spec text governs this adjudication.
- **Adversarial challenge that could break this paper:**
  a reading of spec 018 §4 under which "class" is a loose
  analogy rather than a definition — e.g. calling any old
  published statistics an `image_transcription` or a
  `future_concordance`. §2's criteria are written to block
  exactly that: each §4 class is applied by its stated
  description, not by resemblance, because the matrix is
  frozen and the harness gate (§6.1 of spec 018) is in the
  code path, not in reviewer discretion.
- **No welcome-outcome reasoning.** Whether a YES or a NO
  would be welcome is not evidence under any criterion and
  appears nowhere in §4.

## 1. The registered texts (verbatim, load-bearing)

### 1.1 The register — `docs/PREDICTION_REGISTER.md` §2

> ### PRED-2026-001
> **Date registered**: 2026-04-23
> **Prediction**: Signs classified as TERMINAL by the CGSA model will have end_rate ≥ 0.45 in the ICIT full corpus (6,800 inscriptions) when it becomes available.
> **Withheld data**: Full ICIT database (awaiting Dr. Fuls response)
> **Success criterion**: ≥ 10 of the 14 current TERMINAL signs show end_rate ≥ 0.45 in ICIT data
> **Tested**: PENDING
> **Outcome**: PENDING

> ### PRED-2026-002
> **Date registered**: 2026-04-23
> **Prediction**: Signs classified as INITIAL by the CGSA model will have start_rate ≥ 0.45 in the ICIT full corpus.
> **Withheld data**: Full ICIT database
> **Success criterion**: ≥ 8 of the 12 current INITIAL signs show start_rate ≥ 0.45 in ICIT data
> **Tested**: PENDING
> **Outcome**: PENDING

The register's protocol (§1) is also load-bearing:
"predictions must be registered BEFORE the withheld data is
evaluated" and "This document is the authoritative
register."

### 1.2 Spec 018 — the frozen readiness rules

The following provisions of spec 018 are the adjudication's
entire rulebook. Short verbatim extracts; the section
numbers are spec 018's.

- **§3 (frozen sign sets and canonical map).** TERMINAL —
  "`end_rate ≥ 0.55` — **14 signs**: P020, P076, P095, P099,
  P108, P125, P210, P226, P256, P346, P359, P378, P384,
  P385"; INITIAL — "`start_rate ≥ 0.55` — **12 signs**:
  P000, P001, P004, P013, P051, P098, P217, P238, P265,
  P301, P310, P324". Assumption A2: "All scoring is in
  Parpola (P-number) space", through the canonical registry
  map, which defines exactly two mappings: "**M→P:** each
  `mahadevan_ids` entry maps to that row's `parpola_id`" and
  "**W→P:** each `wells_ids` entry maps likewise". No other
  sign-space mapping is frozen.
- **§4 (source classes).** "Every ingested dataset is
  assigned exactly one source class at ingestion; the class
  is part of the dataset's identity and of its content
  hash." The six classes, by their stated descriptions:
  `rmrl_concordance` ("RMRL Indus Research Centre
  concordance export (Mahadevan sign space) — an
  independent compilation, transcribed from the artifacts,
  not derived from this program's inputs");
  `image_transcription` ("Image-derived transcription
  table (Dixit–Mitra class): signs read from artifact
  images by an external pipeline");
  `future_concordance` ("The Mahadevan Chair expanded
  concordance, or a successor compilation of that kind
  (independent re-compilation)"); `icit_full` ("The full
  ICIT database itself (Wells/Fuls), if ever obtained —
  the register's named withheld data for 001/002");
  `icit_lineage_derivative` ("Public derivatives of the
  ICIT lineage (field-cady, lipi, mayig extracts) —
  **derivation-adjacent** (mayig features are derivation
  inputs) and publicly circulated"); `derivation_corpus`
  ("The program's own derivation corpora (Holdat/CISI
  working layers)").
- **§4 (evaluability, frozen).** "A (prediction × class)
  cell is QUALIFYING only as follows": for both
  PRED-2026-001 and PRED-2026-002, `rmrl_concordance`,
  `image_transcription`, `future_concordance`, and
  `icit_full` are QUALIFIES; `icit_lineage_derivative` and
  `derivation_corpus` are NO. Caveat C1 attaches to
  `icit_full` only, and "Independent classes
  (`rmrl_concordance`, `image_transcription`,
  `future_concordance`) need no caveat: none of their
  content fed any derivation input." And: "Non-qualifying
  classes may be ingested **only** in dry-run mode (§8). In
  evaluation mode the harness refuses them before
  computing any criterion statistic (§6.1)."
- **§5 (deduplication, frozen).** "Applied to every
  ingested corpus, in ingestion (file) order, keep-first,
  before any scoring or coverage statistic. Token sequences
  are the adapter-emitted P-space sequences (§3), including
  `UNK` sentinels." Stage A drops an inscription whose
  "full token sequence exactly equals an earlier kept
  inscription's"; Stage B operates on "`UNK`-stripped
  sequence[s]"; Stage C on "`UNK`-stripped sequences of
  length ≥ 4" within "Levenshtein distance ≤ 1" of a kept
  inscription.
- **§6.1 (run gating).** "An evaluation run for prediction
  P on dataset D proceeds only if ALL hold; otherwise the
  run records NOT EVALUABLE with the failed condition and
  computes **no** criterion statistic", the first condition
  being "1. (P, class(D)) is QUALIFYING per §4", the second
  a complete provenance log, the third "Unmapped +
  ambiguous tokens ≤ 25% of D's post-adapter tokens".
- **§6.2 (rates).** "Over the post-dedup inscription set,
  in P-space, `UNK` tokens occupying positions like any
  token: `occ(s)` = total occurrences of sign s.
  `end_rate(s)` = occurrences of s as the **last** token /
  `occ(s)`; `start_rate(s)` likewise for the **first**
  token. A sign with `occ(s) = 0` has no rate and counts as
  **not** meeting any rate criterion".
- **§6.3 (scoring).** PRED-2026-001: "`k = |{s ∈ TERMINAL14
  : occ(s) ≥ 1 ∧ end_rate(s) ≥ 0.45}|`. Verdict
  **CONFIRMED** iff `k ≥ 10`, else **REFUTED**."
  PRED-2026-002: "`k = |{s ∈ INITIAL12 : occ(s) ≥ 1 ∧
  start_rate(s) ≥ 0.45}|`. Verdict **CONFIRMED** iff
  `k ≥ 8`, else **REFUTED**."
- **§7 (adapters).** "Each adapter emits canonical records
  `{inscription_id, site, tokens}` (tokens in P-space per
  §3)". The adapters are exactly: `rmrl_concordance`,
  `image_transcription`, `future_concordance`, and
  `converted_layer` "(dry run only)" whose "class [is] fixed
  to `icit_lineage_derivative`".
- **Context (derivation inputs).** "the CGSA positional
  classes the predictions quantify over were derived with
  features sourced from mayig's ICIT feature extract
  (`data/crosswalks/sign_inventory.csv`, `source =
  mayig_features`). Any ICIT-lineage data is therefore
  **derivation-adjacent**".

## 2. Criteria (stated before any application)

Each criterion is a mechanical pass/fail test. **The
verdict is YES only if every criterion passes for both
predictions.** The two predictions share every criterion
here because their registered texts, withheld data, and
matrix rows are identical in the respects the criteria test
(§1.1, §1.2 §4); where a criterion's statistic differs by
prediction (C3), it must pass for both statistics.

### C1 — Source-class membership and matrix qualification

*Derivation:* spec 018 §4 (class assignment, class
descriptions, frozen matrix) and §6.1 condition 1;
implemented as `SOURCE_CLASSES` / `EVALUABILITY` in
`pred_harness.py`.

*Pass condition:* the dataset, on its established facts,
falls within the stated description of **exactly one** of
the six §4 classes, and that class's cell for
PRED-2026-001 **and** PRED-2026-002 is QUALIFIES — i.e. the
class is one of `rmrl_concordance`, `image_transcription`,
`future_concordance`, `icit_full`. Falling within a NO
class fails. Falling within **no** class fails: assigning
a new (seventh) class or stretching a description by
analogy would amend the frozen matrix, which this
adjudication may not do.

### C2 — Identity with the withheld data, or a qualifying substitute

*Derivation:* register §2 (withheld data for both
predictions: the full ICIT database; 001 names "the ICIT
full corpus (6,800 inscriptions)"); spec 018 §4
(`icit_full` is "the register's named withheld data for
001/002") and Appendix A.5 ("When a dataset of class
`rmrl_concordance`, `image_transcription`, or
`future_concordance` is acquired, all three predictions
become evaluable on it …; `icit_full`, if ever obtained,
evaluates all three under caveat C1") — i.e. the texts
define exactly two routes to identity: being the withheld
data itself, or being a dataset of a qualifying substitute
class.

*Pass condition:* the dataset **is** the full ICIT database
named in the register, **or** it passes C1 as a qualifying
substitute. Any other dataset — however relevant its
subject matter — fails.

### C3 — Computability of the registered per-sign rates

*Derivation:* register §2 success criteria ("≥ 10 of the
14 current TERMINAL signs show end_rate ≥ 0.45"; "≥ 8 of
the 12 current INITIAL signs show start_rate ≥ 0.45");
spec 018 §3 (the frozen TERMINAL14 and INITIAL12 sign
lists), §6.2 (the definitions of `occ(s)`, `end_rate(s)`,
`start_rate(s)` over the post-dedup inscription set), and
§6.3 (the count rules).

*Pass condition:* the dataset provides — directly, or
through a §7 adapter operating on what the dataset
contains — inscription-level token sequences from which,
for **every** sign `s` in TERMINAL14, `occ(s)` and its
last-token count, and for **every** sign `s` in INITIAL12,
`occ(s)` and its first-token count, can be computed as
§6.2 defines them. Published aggregate proportions,
frequency classes, or joint co-occurrence counts that
cannot be recomputed into those per-sign numerators and
denominators do not satisfy this criterion; a sign whose
rate cannot be computed has not "show[n]" a rate within
the meaning of the register (cf. §6.2: an unattested sign
"counts as **not** meeting any rate criterion" — and a
dataset in which *no* frozen sign's rate is computable
cannot produce the counts §6.3 requires as a measurement
of that dataset at all).

### C4 — Applicability of the frozen deduplication protocol

*Derivation:* spec 018 §5 ("Applied to every ingested
corpus … before any scoring"; Stages A–C defined over
token sequences) and its Context rationale ("no evaluation
on any ICIT-lineage corpus is meaningful without the
frozen deduplication protocol of §5 — and this harness
applies that protocol to *every* ingested corpus,
independent or not").

*Pass condition:* the dataset consists of inscription
token sequences to which Stages A, B, and C can actually
be applied, in ingestion order, keep-first, producing the
mandatory per-stage removed counts. A dataset whose
underlying inscriptions have already been collapsed into
aggregates — so that duplicate inscriptions, if any, can
no longer be identified or removed — fails, because the
protocol cannot be run on it, and skipping the protocol is
not an option the frozen text offers.

### C5 — Canonical sign space and harness ingestibility

*Derivation:* spec 018 A2 and §3 ("All scoring is in
Parpola (P-number) space"; the frozen map defines M→P and
W→P only); §7 (adapters emit `{inscription_id, site,
tokens}` in P-space; the adapter list is closed);
§6.1 conditions 2–3 (complete provenance log for the
ingested corpus; unmapped + ambiguous tokens ≤ 25%).

*Pass condition:* (a) every sign identity in the dataset
can be carried into P-space by the frozen §3 map — no new
map may be created for this adjudication; (b) a §7 adapter
exists that accepts the dataset's actual form and emits
canonical inscription records from it; and (c) the
resulting token stream could satisfy the §6.1
unmapped/ambiguous guard. Failure of any of (a)–(c) fails
the criterion.

### C6 — Independence from the derivation inputs

*Derivation:* spec 018 Context and §4 (the CGSA classes
were derived from a mayig ICIT feature extract, so
ICIT-lineage data is derivation-adjacent; of the
independent classes, "none of their content fed any
derivation input"; `icit_full` qualifies only under
caveat C1, whose text is: "Class features derive in part
from a mayig ICIT feature extract; this corpus is the
registered withheld data but is derivation-adjacent in
part.").

*Pass condition:* the dataset's content was not a
derivation input of the CGSA classes, beyond the one
adjacency the registered texts already caveat (the mayig
extract's relation to `icit_full`, caveat C1). A dataset
whose content fed the derivation in some other, uncaveated
way fails. Note what this criterion does **not** require:
disjointness of the underlying artefact population. The
qualifying independent classes are themselves
re-transcriptions of the same artefact population; §4's
independence is about compilation lineage — not having fed
the derivation — not about disjoint artefacts.

## 3. Established facts about the dataset

Established from the Phase-121 artifacts alone
(`data/soviet_positional/`, `reports/phase121_soviet_positional_dataset.md`,
the Phase-121/122 ledger records). No fact below is
inferred from any positional statistic.

- **F1 — What the dataset is.** A descriptive dataset of
  **published aggregate tables**: 7 tables, 109 records,
  extracted in Phase-121 (2026-10-08). Its own JSON header
  states `"descriptive_only": true` and: "It scores no
  prediction, validates no anchor, and makes no claim about
  PRED-2026-001/002/003." The Phase-121 memo's header
  states: "**DESCRIPTIVE DATASET ONLY — NO PREDICTION
  SCORED, NO ANCHOR VALIDATED**", and its Non-claims
  section: "Whether the Soviet positional data can formally
  bear on PRED-2026-001/002 is an open question for a future
  spec adjudication (the registered PRED texts name specific
  corpora); this phase takes no position on it." This spec
  is that adjudication.
- **F2 — Provenance of the content.** Four tables are
  Kondratov's 1965 Preliminary Report, positional-statistical
  analysis, as printed in English translation in Zide &
  Zvelebil (eds) 1976, *The Soviet Decipherment of the
  Indus Valley Script*: Table 1 (printed p. 40), Table 2
  (p. 41), Table 3 (p. 43), Table 4 (p. 47). The other
  three tables are Volchok calendrical tables from
  *Proto-Indica* 1973 — yuga festivals, divine-chronology
  unit equivalences, yuga durations — which the memo labels
  "non-sign, non-positional". The 1968 Knorozov report
  contains no frequency or positional tables (searched in
  full), and *Proto-Indica* 1973 contains no sign-frequency
  or positional count tables at all.
- **F3 — No inscription-level records.** The dataset
  contains **zero inscriptions and zero token sequences**.
  No record in any of the seven CSVs is an inscription; no
  record carries an inscription identifier, a site, or a
  sequence of signs. The records are table rows: increments
  of cumulative text length (T1), frequency classes (T2),
  polygram-length rows (T3), initial-pair × final cells
  (T4), and calendar rows (PI73-V1–V3).
- **F4 — Tables 1–3 are aggregates naming no signs.**
  T1 rows are cumulative text length in signs (25…1400 by
  25); its columns count *new sign types first appearing*
  per increment, Egyptian control vs Proto-Indian. T2 rows
  are sign frequency classes (share of total absolute
  frequency, %); per the memo, T2 "covers the full sign
  inventories in aggregate (315 Proto-Indian / 195 Egyptian
  signs by frequency class) but **names no individual
  signs**". T3 counts polygrams (recurring sign
  combinations) by length 2–9, total / genuine / errors,
  for Egyptian and Proto-Indian corpora in aggregate.
- **F5 — Table 4 is the only per-sign table, and it is a
  restricted co-occurrence matrix.** Per the memo: "Sign
  coverage (K1965-T4, the only per-sign table)"; its title
  is "Stable initials … in combination with stable finals".
  Rows: 8 stable-initial sign **pairs** — initial signs 99,
  160, 232, 233 with second elements 118, 500, 501, 507.
  Columns: stable finals 66, 68, 87, 96, 97, 124 (plus the
  pair-final column headed "87—"). Cells: "absolute
  frequencies" of that initial-pair in combination with
  that final. It therefore records, for a selected set of
  signs, **joint** counts of (initial-pair × final)
  combinations. It does not record any sign's total
  occurrences, any sign's count in initial or final
  position over all its occurrences, or any inscription.
  Its printed totals are additionally internally
  inconsistent, preserved as printed and never repaired:
  cells sum to a grand total of 160 against a printed 171,
  with printed column totals for finals 87, 124, and 66
  disagreeing with their cells.
- **F6 — Sign numbering is Marshall, with no frozen map.**
  T4's signs are in **Marshall catalogue numbers** (memo:
  "rows: 8 stable-initial sign pairs (Marshall numbers;
  232 subsumes 126, allographs per the printed note)").
  The program's record on this numbering is explicit
  (Phase-122 ledger): "Marshall numbering (Kondratov,
  Phase-121): no Marshall↔M/P pairs extractable from
  sources on main; v1 asserts none." The frozen §3 map of
  spec 018 covers Mahadevan (M→P) and Wells (W→P) only.
- **F7 — The underlying corpus.** The tables summarize the
  Indus material available to the Soviet team in the 1960s:
  T1's cumulative text length runs to 1,400 signs; T2's
  Proto-Indian inventory is 315 signs. The dataset does not
  identify the underlying inscriptions individually, and
  nothing in it is, or is an export of, a 6,800-inscription
  database.
- **F8 — Derivation lineage.** The derivation input of
  record for the CGSA classes is the mayig ICIT feature
  extract (spec 018 Context; §1.2 above). No registered
  text records the Soviet tables, in any form, as a
  derivation input. The dataset itself was extracted in
  Phase-121 on 2026-10-08 — after the CGSA classes existed
  and after the predictions were registered (2026-04-23).
  The 1965 compilation is not of the ICIT lineage
  (field-cady / lipi / mayig): it predates that lineage and
  is not derived from it.

## 4. Application of the criteria

Each criterion is applied to §3's facts only.

### C1 — Source-class membership and matrix qualification: **FAIL**

Test the dataset against each §4 description in turn:

- `rmrl_concordance` — an "RMRL Indus Research Centre
  concordance export (Mahadevan sign space)". The dataset
  is not an RMRL export, is not a concordance (it lists no
  inscriptions — F3), and its only sign numbering is
  Marshall, not Mahadevan (F6). **Does not fit.**
- `image_transcription` — "signs read from artifact images
  by an external pipeline" (the Dixit–Mitra class). The
  dataset's content is published aggregate statistics
  printed in a 1976 volume (F1, F2); no sign was read from
  an artifact image into this dataset at inscription level,
  and there are no inscription transcriptions to qualify
  (F3). That Phase-121 used OCR on *printed book pages* to
  extract *printed numbers* does not make the content an
  image-derived transcription of artefacts; the class
  description is about the transcription's object
  (artefacts, per inscription), not about the extraction
  tooling used on a book. **Does not fit.**
- `future_concordance` — "The Mahadevan Chair expanded
  concordance, or a successor compilation of that kind
  (independent re-compilation)". The dataset is a 1965
  statistical report's aggregate tables (F2); it is not a
  concordance of any kind (F3) and predates, rather than
  succeeds, the compilation it would have to succeed.
  **Does not fit.**
- `icit_full` — "The full ICIT database itself
  (Wells/Fuls)". See C2. **Does not fit.**
- `icit_lineage_derivative` — "Public derivatives of the
  ICIT lineage (field-cady, lipi, mayig extracts)". The
  dataset is not derived from the ICIT lineage (F8).
  **Does not fit** — and the cell is NO in any case.
- `derivation_corpus` — "The program's own derivation
  corpora (Holdat/CISI working layers)". The dataset is
  none of those. **Does not fit** — and the cell is NO in
  any case.

The dataset falls within **no** §4 class. C1's pass
condition therefore cannot be met, and the two NO classes
would fail it even under a forced assignment. Reaching YES
here would require inventing a seventh class (e.g.
"published historical aggregate statistics") and a new
matrix row of QUALIFIES cells — an amendment of the frozen
matrix, expressly out of scope. **C1 FAILS.**

*Deciding fact:* the dataset is published aggregate tables
from a 1965 report (F1–F3), a form none of the six frozen
class descriptions describes.

### C2 — Identity with the withheld data, or a qualifying substitute: **FAIL**

The register's withheld data is the "Full ICIT database",
and PRED-2026-001 names "the ICIT full corpus (6,800
inscriptions)". The dataset is not that database: it is a
1965 report's printed tables, whose underlying material
runs to a cumulative 1,400 signs over a 315-sign inventory
(F7), contains no inscription records at all (F3), and was
never the ICIT database in any form (F2). The substitute
route fails with C1: the dataset passes C1 for no
qualifying class. Both routes in C2's pass condition are
closed. **C2 FAILS.**

*Deciding fact:* the dataset is not the full ICIT database
(F2, F3, F7) and is not a §4-qualifying substitute (C1).

### C3 — Computability of the registered per-sign rates: **FAIL**

§6.2 requires, for each frozen sign, `occ(s)` over the
post-dedup inscription set and the count of `s` as last
(001) or first (002) token. The dataset supplies neither
quantity for **any** sign in TERMINAL14 or INITIAL12:

- There are no inscriptions and no token sequences from
  which occurrences or positions could be counted (F3).
- Tables 1–3 name no individual signs at all (F4), so they
  contribute nothing per-sign.
- Table 4, the only per-sign table (F5), gives joint
  absolute frequencies of 8 selected initial **pairs** in
  combination with 7 selected finals — in Marshall numbers
  (F6). A cell such as (232, 501) × 87 = 52 is a count of
  one combination. It is not the last-token count of any
  Parpola sign (the numerator §6.2 requires is over *all*
  occurrences of the sign as last token, not only those
  co-occurring with eight selected initial pairs), and the
  table contains no total-occurrence count for any sign
  (the denominator §6.2 requires). Neither numerator nor
  denominator exists, for any sign, in any table.
- The Proto-Indica tables are calendrical and non-sign
  (F2).

Result: **0 of the 14** TERMINAL end_rates and **0 of the
12** INITIAL start_rates are computable from this dataset
as §6.2 defines them. (This is a count of computable
rates — a fact about the dataset's form, not a criterion
statistic; no rate was computed, against any threshold.)
**C3 FAILS.**

*Deciding fact:* the dataset contains aggregate tables
only; the sole per-sign table is a restricted
pair × final co-occurrence matrix with no occurrence
denominators and no positional counts over all occurrences
(F3–F5).

### C4 — Applicability of the frozen deduplication protocol: **FAIL**

Stages A–C are operations on inscription token sequences
(exact sequence equality; `UNK`-stripped equality;
Levenshtein distance on stripped sequences). The dataset
has no token sequences (F3), so no stage can be executed
and no per-stage removed count — a mandatory output of
every run — can be produced. The collapse is irreversible:
whatever inscriptions underlay the 1965 tables were
aggregated into printed counts six decades ago (F1, F2),
and duplicate inscriptions in that underlying material, if
any existed, cannot now be identified, let alone removed
keep-first in ingestion order. The frozen text applies the
protocol to *every* ingested corpus and offers no waiver.
**C4 FAILS.**

*Deciding fact:* there are no inscription token sequences
to deduplicate (F3); the §5 protocol is inapplicable in
principle, not merely unrun.

### C5 — Canonical sign space and harness ingestibility: **FAIL**

All three sub-conditions fail independently:

- **(a) Frozen map.** The dataset's only sign identities
  are Marshall catalogue numbers (F6). The frozen §3 map
  defines M→P and W→P only, and the program's record is
  that no Marshall↔M/P pairs are extractable from sources
  on main (F6). Carrying any Soviet sign into P-space would
  require creating a new map — re-registration work, out
  of scope. (Numerical coincidence between a Marshall
  number and a P number is not a mapping; spec 018 A.4
  records what number-identity assumptions did to the
  rejected crosswalk-v2 map.)
- **(b) Adapter.** The §7 adapter list is closed
  (rmrl / image / future / converted-layer-dry-run-only),
  and every adapter emits `{inscription_id, site, tokens}`
  records. The dataset's records are table rows with none
  of those fields (F3); no adapter accepts aggregate
  tables, and the converted-layer adapter is dry-run-only
  with its class fixed to a NO class.
- **(c) Unmapped guard.** Because (a) fails, there is no
  P-space token stream on which the §6.1 ≤ 25%
  unmapped/ambiguous condition could be satisfied; on the
  frozen map, every Marshall-numbered sign is unmapped.

**C5 FAILS.**

*Deciding fact:* Marshall numbering has no frozen map to
P-space and no §7 adapter ingests aggregate tables (F3,
F6).

### C6 — Independence from the derivation inputs: **PASS** (narrow)

The derivation input of record is the mayig ICIT feature
extract (F8). The Soviet dataset's content did not feed
that derivation: no registered text records it as an
input, in the original 1965 form or in the Phase-121
extraction (which postdates both the classes and the
registration — F8), and the compilation is not of the ICIT
lineage. The one adjacency the texts caveat — the mayig
extract's relation to `icit_full`, caveat C1 — does not
apply here because the dataset is not `icit_full` (C2).
**C6 PASSES.**

Two limits on this pass, stated so it cannot be over-read:
(i) it is a pass on lineage only, per C6's own derivation —
the shared underlying artefact population (F7) is not a
failure under §4's independence logic, which qualifies
re-transcriptions of the same artefacts; (ii) passing C6
confers no source class and cures no other criterion. An
independent dataset that fits no qualifying class and
cannot yield the registered statistics is still
non-qualifying.

*Deciding fact:* the dataset's content was not a CGSA
derivation input in any form the registered texts record
(F8).

### Summary

| Criterion | Result | Deciding fact (short) |
|---|---|---|
| C1 Class / matrix | FAIL | Fits none of the six frozen §4 classes; no class may be invented |
| C2 Identity / substitute | FAIL | Not the full ICIT database; no qualifying substitute class |
| C3 Rate computability | FAIL | Aggregates only; 0/14 and 0/12 registered rates computable as §6.2 defines them |
| C4 Dedup applicability | FAIL | No token sequences; §5 Stages A–C inapplicable in principle |
| C5 Sign space / ingestibility | FAIL | Marshall numbers, no frozen map to P-space; no §7 adapter for aggregate tables |
| C6 Independence | PASS | Content was not a derivation input; the C1 caveat does not apply |

## 5. Verdict

**NO.** The Soviet positional dataset (Phase-121;
Kondratov 1965, as extracted) does **not** qualify as an
evaluation source for PRED-2026-001 or PRED-2026-002.
The §2 rule is conjunctive — YES requires every criterion
to pass — and five of the six criteria fail, each on the
dataset's established form, independently of the others.
Any one of C1, C2, C3, C4, or C5 failing would alone
compel NO.

Consequences, executed by this spec's tasks:

1. **No scoring runs.** The Phase-119 harness scorers are
   not invoked in evaluation mode on this dataset, and no
   labelled dry run is performed on it either (none was
   requested; a dry run is in any case an ingestion/dedup
   exercise, and C4/C5 show there is nothing the harness
   could ingest). No PRED verdict of any kind is produced,
   recorded, or implied by this paper.
2. **Predictions stay PENDING.** PRED-2026-001 and
   PRED-2026-002 keep `Tested: PENDING` / `Outcome:
   PENDING`. This adjudication is not a test of either
   prediction: a non-qualifying source can neither confirm
   nor refute them.
3. **Register note.** A dated, append-only adjudication
   note is added to `docs/PREDICTION_REGISTER.md` recording
   that the Soviet dataset was adjudicated non-qualifying
   under this spec and why, citing this spec. The
   registered prediction entries themselves are not
   modified.
4. **Nothing else changes.** No anchor, claim, registry,
   or language-model file is touched; the anchors file
   `backend/reports/INDUS_FINAL_ANCHORS.json` remains
   byte-identical (sha256
   `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`,
   asserted before and after this work).

## 6. What would have to change for a different verdict

Stated for the record; none of it is authorized or
attempted here. The verdict is a property of the dataset's
form against frozen texts, so it could change only if one
of the inputs changed: (i) a dataset of a §4 qualifying
class is acquired (an RMRL concordance export, an
image-derived per-inscription transcription table, a
future concordance, or the full ICIT database itself) —
the event spec 018 was built for; or (ii) an
inscription-level Soviet-era corpus — per-inscription
transcriptions, in a sign space with a frozen map to
P-space — were assembled and brought under a **new**
pre-registration that classifies it, freezes its map, and
amends or supersedes the spec 018 matrix through the
program's normal spec process, *before* any evaluation.
Re-extracting the same aggregate tables more finely would
not change any criterion: C1, C3, C4, and C5 fail on the
tables' aggregate form, not on extraction fidelity (which
Phase-121 verified at 36/36 sampled cells).

## 7. Non-claims

This paper claims nothing about the positional facts
themselves: it does not say the Soviet statistics agree or
disagree with the CGSA classes, does not validate or
invalidate any anchor, and draws no conclusion from
Kondratov's Table 4 about any individual sign — the
co-occurrence counts in that table were read here only to
establish what kind of quantity they are (C3), never
compared against any threshold, rate, or class. The
Phase-121 dataset remains what its memo says it is: a
faithful descriptive extraction, usable for any future
work whose design fits its form.

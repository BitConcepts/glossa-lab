# Spec 018 — Phase-119: PRED-2026 Readiness — the Pre-Registered Prediction Evaluation Harness

**Status:** DESIGN FROZEN 2026-10-07 on `phase/119-pred-harness`
(from main `fffb43ef`). Owner authorization: Tristen Pierson,
2026-10-07 — build the evaluation harness for PRED-2026-001–003
so that it **fires the day independent data lands**. This spec
is committed before any harness code exists. Implementation
follows in this same phase (the owner authorized the build,
not merely the design), but **no evaluation of any real
prediction is authorized by this spec and none is possible**:
no qualifying independent dataset exists yet (§4). The only
end-to-end exercise permitted is the labelled dry run of §8 on
clearly non-independent data.

**Phase-numbering note:** ledger-sequence **Phase-119**
(Phase-117 spec 016, Phase-118 spec 017 precede it; Phase-118's
PR is stacked/unmerged at freeze time and is not touched by
this phase). Artifact names carry the phase number
(`phase119_pred_harness`, graph node
`IndusPhase119PredHarness`).

**AI disclosure:** this phase is executed by an AI agent
(Muse Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.

## Context — why this phase exists

PRED-2026-001–003 were registered on 2026-04-23 in
`docs/PREDICTION_REGISTER.md` and have sat PENDING ever since,
because their withheld data never arrived: the full ICIT
database was never obtained, and no genuinely independent
corpus has been acquired. In the interval the program learned,
at some cost, what does **not** count as independent evidence:

- Phase-107 (spec 005) falsified the SA method; the CGSA
  positional classes the predictions quantify over were derived
  with features sourced from mayig's ICIT feature extract
  (`data/crosswalks/sign_inventory.csv`, `source =
  mayig_features`). Any ICIT-lineage data is therefore
  **derivation-adjacent**: it partially overlaps the derivation
  inputs. This adjacency is recorded per prediction in §4, not
  smoothed over.
- Nair 2026 documents a ~24% exact-duplicate rate in the
  field-cady/lipi ICIT lineage. Duplicated inscriptions inflate
  every rate the predictions quantify over, so **no evaluation
  on any ICIT-lineage corpus is meaningful without the frozen
  deduplication protocol of §5** — and this harness applies
  that protocol to *every* ingested corpus, independent or
  not, so the pipeline cannot be quietly skipped on the day.
- Phase-116 (spec 015) established R-NONE for cross-corpus
  positional *validation* between Holdat and ICIT. That verdict
  constrains validation batteries; it does not touch these
  predictions, whose criteria are fixed count rules over a new
  corpus (§6), not profile-agreement tests. The distinction is
  recorded here so the two are never conflated.

Three awaited source classes could supply the test data:
an RMRL (Roja Muthiah Research Library, Indus Research Centre)
concordance export; the Dixit–Mitra image-derived
transcription table; and the future Mahadevan Chair expanded
concordance. None exists in hand. This phase builds the
machine that receives any of them: ingestion adapters with
provenance logging, the frozen dedup pipeline, the mechanical
scoring of the three registered criteria, and a gate that
refuses to score anything whose independence class does not
qualify — so that when the data lands, the evaluation is a
procedure, not a negotiation.

## Epistemic boundaries (H13)

Assumptions, declared:

- **A1 — Orientation.** Sign position is the token index in
  the sequence as emitted by the adapter; "start" is index 0,
  "end" is the last index. Adapters MUST emit sequences in
  the source's own transcription order, which is the order in
  which the derivation-era rates were computed (mayig feature
  extraction order, carried by the Phase-115 converted layer).
  No adapter reverses a sequence. Reading-direction questions
  are thereby inherited from the derivation, not re-decided.
- **A2 — Canonical sign space.** All scoring is in Parpola
  (P-number) space. The canonical cross-system map is
  `data/crosswalks/canonical_sign_registry.csv` (the program's
  primary registry; sha256 at freeze in §3). The sparse
  `mahadevan_parpola_crosswalk_v2.json` map is **not** used:
  at design time it covered only 131 of the current layer's
  284 attested M signs and inverted several high-frequency
  assignments relative to the registry (Appendix A.4).
- **A3 — Class sets.** The prediction sign sets are the CGSA
  classes exactly as recoverable from
  `data/crosswalks/sign_inventory.csv` under the frozen rule
  of §3 — the rule reproduces the register's "14 current
  TERMINAL signs" and "12 current INITIAL signs" exactly
  (Appendix A.3). If a future registry revision changes the
  sets, the predictions are evaluated against the sets frozen
  here, not the revised ones; that is what "current" meant on
  2026-04-23.
- **A4 — PRED-003 conformance.** The registered text does not
  define "template" conformance beyond its success criterion
  ("Template coverage ≥ 70% in held-out corpus"). §6 freezes
  one mechanical operationalization. It is a design decision
  of this spec, disclosed here, not a discovery about the
  register.
- **A5 — No verdict shopping.** One verdict per
  (prediction × dataset content hash). §6.5's verdict lock
  makes a second scoring of the same dataset a hard error, so
  the harness cannot be re-run until a number looks better.

Adversarial challenge that could break this phase: a future
dataset arriving in a sign space whose map to P-space is
many-to-many in a way the §3 conflict rule resolves wrongly at
scale (e.g. the Chair concordance renumbering Mahadevan
signs). The adapters mitigate by counting and reporting
unmapped/ambiguous tokens in the provenance log; a run whose
unmapped-token share exceeds 25% is NOT EVALUABLE (§6.1),
forcing a spec amendment rather than a silent wrong answer.

## 1. The registered predictions (verbatim)

Quoted exactly from `docs/PREDICTION_REGISTER.md` §2
(2026-04-23). The harness implements these texts; where a
text under-specifies a mechanical detail, §6 freezes the
operationalization and says so.

### PRED-2026-001

> **Date registered**: 2026-04-23
> **Prediction**: Signs classified as TERMINAL by the CGSA model will have end_rate ≥ 0.45 in the ICIT full corpus (6,800 inscriptions) when it becomes available.
> **Withheld data**: Full ICIT database (awaiting Dr. Fuls response)
> **Success criterion**: ≥ 10 of the 14 current TERMINAL signs show end_rate ≥ 0.45 in ICIT data
> **Tested**: PENDING
> **Outcome**: PENDING

### PRED-2026-002

> **Date registered**: 2026-04-23
> **Prediction**: Signs classified as INITIAL by the CGSA model will have start_rate ≥ 0.45 in the ICIT full corpus.
> **Withheld data**: Full ICIT database
> **Success criterion**: ≥ 8 of the 12 current INITIAL signs show start_rate ≥ 0.45 in ICIT data
> **Tested**: PENDING
> **Outcome**: PENDING

### PRED-2026-003

> **Date registered**: 2026-04-23
> **Prediction**: The 3-slot INITIAL-MEDIAL-TERMINAL template structure will account for ≥ 70% of inscription templates in any newly acquired multi-site dataset.
> **Withheld data**: Any dataset not yet acquired (ICIT, ASI archives)
> **Success criterion**: Template coverage ≥ 70% in held-out corpus
> **Tested**: PENDING
> **Outcome**: PENDING

## 2. Scope

In scope: the dedup protocol (§5); the per-prediction
evaluation protocol (§6); three ingestion adapters with
provenance logging (§7); the dry-run regime (§8); the harness
implementation, graph registration, fixtures, and tests (§9).

Out of scope: evaluating any real prediction (no qualifying
data exists); acquiring any dataset; anchor changes of any
kind (this phase touches no anchor file — and therefore
cannot promote anything, so H26 is satisfied vacuously);
PRED-2026-004–009 (different withheld data, different
machinery; untouched).

## 3. Frozen sign sets and the canonical map

**Class rule (frozen).** From
`data/crosswalks/sign_inventory.csv` (sha256
`f9a84ff999589619a884b07afa927f0d51093f76b4ea1f8f5b5628e0e8fcb12f`),
rows with `numbering_system = parpola_1982` and
`corpus_freq ≥ 10` (the INSUFFICIENT_DATA floor of
SIGN_INVENTORY §5). Priority order TERMINAL → INITIAL →
MEDIAL → MIXED is immaterial: the three rate classes are
mutually disjoint under the thresholds (verified at design
time; Appendix A.3).

- TERMINAL — `end_rate ≥ 0.55` — **14 signs**:
  P020, P076, P095, P099, P108, P125, P210, P226, P256, P346,
  P359, P378, P384, P385
- INITIAL — `start_rate ≥ 0.55` — **12 signs**:
  P000, P001, P004, P013, P051, P098, P217, P238, P265, P301,
  P310, P324
- MEDIAL — `internal_rate ≥ 0.70` — **46 signs**
- MIXED — classified, none of the above — **33 signs**

**Canonical map (frozen).** From
`data/crosswalks/canonical_sign_registry.csv` (sha256
`8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420`),
`parpola_1982` rows:

- **M→P:** each `mahadevan_ids` entry maps to that row's
  `parpola_id`. An M sign claimed by several P rows resolves
  to the row with the highest `corpus_freq`; tie → lowest
  P number; a residual tie (equal freq, e.g. M002, claimed by
  P015/P016 at equal standing) is **AMBIGUOUS**: the token is
  emitted as the `UNK` sentinel and counted as ambiguous.
- **W→P:** each `wells_ids` entry maps likewise (Wells codes
  are key-normalized with `str(int(code))` before lookup —
  the Phase-115 leading-zero lesson). Same conflict rule.
- A source sign with no registry entry → `UNK`, counted as
  unmapped. `UNK` tokens occupy positions (§6.2) but carry no
  class and no sign identity.

## 4. Source classes and the evaluability matrix

Every ingested dataset is assigned exactly one source class
at ingestion; the class is part of the dataset's identity and
of its content hash. The classes:

| Class | Description |
|---|---|
| `rmrl_concordance` | RMRL Indus Research Centre concordance export (Mahadevan sign space) — an independent compilation, transcribed from the artifacts, not derived from this program's inputs |
| `image_transcription` | Image-derived transcription table (Dixit–Mitra class): signs read from artifact images by an external pipeline |
| `future_concordance` | The Mahadevan Chair expanded concordance, or a successor compilation of that kind (independent re-compilation) |
| `icit_full` | The full ICIT database itself (Wells/Fuls), if ever obtained — the register's named withheld data for 001/002 |
| `icit_lineage_derivative` | Public derivatives of the ICIT lineage (field-cady, lipi, mayig extracts) — **derivation-adjacent** (mayig features are derivation inputs) and publicly circulated |
| `derivation_corpus` | The program's own derivation corpora (Holdat/CISI working layers) |

**Evaluability (frozen).** A (prediction × class) cell is
QUALIFYING only as follows:

| Prediction | rmrl_concordance | image_transcription | future_concordance | icit_full | icit_lineage_derivative | derivation_corpus |
|---|---|---|---|---|---|---|
| PRED-2026-001 | QUALIFIES | QUALIFIES | QUALIFIES | QUALIFIES (registered target; adjacency caveat C1) | NO | NO |
| PRED-2026-002 | QUALIFIES | QUALIFIES | QUALIFIES | QUALIFIES (registered target; adjacency caveat C1) | NO | NO |
| PRED-2026-003 | QUALIFIES | QUALIFIES if §6.4 site input holds | QUALIFIES | QUALIFIES (caveat C1) | NO | NO |

- **C1 (adjacency caveat).** The CGSA class features were
  computed from a mayig ICIT feature extract, so the full
  ICIT database is not wholly untouched by the derivation:
  it is the *registered* withheld corpus for 001/002 (and a
  newly acquired multi-site dataset for 003), and an
  evaluation on it is a genuine out-of-sample test on the
  inscriptions the extract did not carry — but every verdict
  issued on `icit_full` MUST carry this caveat verbatim in
  its report: "Class features derive in part from a mayig
  ICIT feature extract; this corpus is the registered
  withheld data but is derivation-adjacent in part."
- Independent classes (`rmrl_concordance`,
  `image_transcription`, `future_concordance`) need no
  caveat: none of their content fed any derivation input.
- Non-qualifying classes may be ingested **only** in dry-run
  mode (§8). In evaluation mode the harness refuses them
  before computing any criterion statistic (§6.1).

## 5. Deduplication protocol (frozen)

Applied to every ingested corpus, in ingestion (file) order,
keep-first, before any scoring or coverage statistic. Token
sequences are the adapter-emitted P-space sequences (§3),
including `UNK` sentinels.

- **Stage A — exact.** Drop an inscription whose full token
  sequence exactly equals an earlier kept inscription's.
- **Stage B — sentinel-normalized exact.** Drop an
  inscription whose `UNK`-stripped sequence is non-empty and
  exactly equals an earlier kept inscription's `UNK`-stripped
  sequence. (Catches duplicates that differ only in
  placeholder placement.)
- **Stage C — near-duplicate.** On `UNK`-stripped sequences
  of length ≥ 4: drop an inscription whose stripped sequence
  is within Levenshtein distance ≤ 1 of an earlier **kept**
  inscription's stripped sequence (greedy keep-first;
  comparisons only against kept anchors, so there is no
  transitive chaining). Sequences shorter than 4 after
  stripping are exempt from Stage C (short Indus texts repeat
  legitimately at high rates and distance-1 there is not
  evidence of duplication of record).

Per-stage removed counts and rates are mandatory outputs of
every run, dry or real. Design-stage measurements of this
protocol on the current expanded ICIT layer are Appendix A.1
(cumulative removal 45.51% — above Nair's ~24% exact-only
figure for the raw lineage, as expected once Stages B/C and
the short-inscription residue are counted; the builder that
produced the layer had already removed its length ≥ 3 exact
duplicates, which is why Stage A's residue sits entirely in
lengths 1–2).

## 6. Evaluation protocol

### 6.1 Run gating

An evaluation run for prediction P on dataset D proceeds
only if ALL hold; otherwise the run records NOT EVALUABLE
with the failed condition and computes **no** criterion
statistic:

1. (P, class(D)) is QUALIFYING per §4.
2. D's provenance log (§7) is complete, including license /
   acquisition basis and the input content hash.
3. Unmapped + ambiguous tokens ≤ 25% of D's post-adapter
   tokens (A-challenge guard, §0).
4. D's verdict lock (§6.5) is not already held for P.
5. For PRED-2026-003 only: D carries ≥ 2 distinct site
   values among its records (the registered text says
   "multi-site dataset").

### 6.2 Rates (for 001/002)

Over the post-dedup inscription set, in P-space, `UNK`
tokens occupying positions like any token:

- `occ(s)` = total occurrences of sign s.
- `end_rate(s)` = occurrences of s as the **last** token /
  `occ(s)`; `start_rate(s)` likewise for the **first** token.
- A sign with `occ(s) = 0` has no rate and counts as **not**
  meeting any rate criterion (mechanical; the registered
  criteria count signs, and an unattested sign cannot "show"
  a rate). Its absence is reported in the coverage block.

### 6.3 Scoring rules (mechanical; thresholds as registered)

- **PRED-2026-001:** `k = |{s ∈ TERMINAL14 : occ(s) ≥ 1 ∧
  end_rate(s) ≥ 0.45}|`. Verdict **CONFIRMED** iff `k ≥ 10`,
  else **REFUTED**.
- **PRED-2026-002:** `k = |{s ∈ INITIAL12 : occ(s) ≥ 1 ∧
  start_rate(s) ≥ 0.45}|`. Verdict **CONFIRMED** iff
  `k ≥ 8`, else **REFUTED**.
- **PRED-2026-003:** an inscription is *template-conforming*
  iff every token maps to a P sign carrying a §3 class label
  and the label sequence matches `INITIAL* MEDIAL+
  TERMINAL*` (zero or more INITIAL, one or more MEDIAL, zero
  or more TERMINAL, in that order, nothing else — a MIXED
  label anywhere, an unmapped/`UNK` token anywhere, or a
  label out of order makes it non-conforming). Template
  coverage = conforming / total post-dedup inscriptions.
  Verdict **CONFIRMED** iff coverage ≥ 0.70, else
  **REFUTED**. (Operationalization per A4: coverage is over
  inscriptions — the register's criterion says "coverage …
  in held-out corpus" — not over distinct template types.)

### 6.4 Report contents (every evaluation run)

Per prediction: the registered criterion quoted; the dataset
identity (class, provenance summary, content hash); dedup
stage counts; per-sign table for 001/002 (occ, rate, meets
criterion) or the coverage numerator/denominator for 003;
the verdict; caveat C1 where §4 requires it; the harness
version and the sha256 of this spec file. No other statistics
may be attached to a verdict.

### 6.5 Verdict lock and multiplicity stance

- **Lock.** A verdict is keyed by (prediction id, dataset
  content hash). The harness persists issued verdicts in its
  run ledger (`reports/phase119_pred_harness_results.json`
  for this phase; a run-scoped ledger file thereafter) and
  refuses to re-score a locked pair. A corrected dataset is
  a new dataset (new hash) and any re-evaluation on it must
  be separately authorized and separately reported — the
  harness records, but does not adjudicate, that case.
- **Multiplicity.** The three predictions are three separate
  registered hypotheses with self-contained count criteria.
  No significance tests are performed and no family-wise
  correction applies to the verdicts, because the verdicts
  are deterministic comparisons against registered
  thresholds, not inferences. Any inferential analysis of
  evaluation data is out of scope for this harness and would
  require its own pre-registration.

## 7. Ingestion adapters and provenance

Three adapters, one per awaited independent class, plus the
converted-layer adapter used by the dry run. Each adapter
emits canonical records `{inscription_id, site, tokens}`
(tokens in P-space per §3) and one provenance log entry in
the Phase-107/111 acquisition-log pattern:

```json
{
  "date": "ISO date",
  "name": "dataset name",
  "source_class": "one of §4",
  "source": "origin description / file path / URL",
  "license": "license or acquisition basis, verbatim where known",
  "status": "ingested | dry-run-only | not-obtainable + reason",
  "input_sha256": "hash of the raw input bytes",
  "as_built": {"inscriptions": 0, "tokens": 0,
               "tokens_unmapped": 0, "tokens_ambiguous": 0,
               "distinct_signs": 0},
  "text_rule": "how sequences were read from the source",
  "unit_rule": "what counts as one inscription"
}
```

- **`rmrl_concordance`** — input CSV or JSON: one record per
  inscription with `site` and a Mahadevan sign sequence
  (whitespace-separated M codes). M→P per §3.
- **`image_transcription`** — input CSV or JSON: one record
  per inscription with `site` and Wells sign codes (numeric,
  possibly zero-padded), optional per-sign confidence
  (carried in provenance, unused by scoring in this version).
  W→P per §3.
- **`future_concordance`** — input JSON: records with
  `site` and P-number sequences directly. Unknown P → `UNK`.
- **`converted_layer`** (dry run only) — the Phase-115
  `icit_converted_v2.json` format (`{source, inscriptions:
  [[M…], …]}`); M→P per §3; class fixed to
  `icit_lineage_derivative`.

Adapters are built and tested against **synthetic fixtures**
only (no real source exists yet); a fixture is a toy input
file in the adapter's documented schema, small enough to
verify by hand.

## 8. The dry-run rule

The harness may be exercised end-to-end **only** on clearly
non-independent data (in this phase: the current expanded
ICIT converted layer, class `icit_lineage_derivative`).

- Every dry-run artifact — results JSON, report, log —
  carries, in the artifact itself, the exact string:
  **"HARNESS DRY RUN — NOT A PRED EVALUATION"**.
- Permitted dry-run outputs: ingestion and dedup counts
  (per stage); token/sign counts; **sign-set coverage** per
  prediction (for 001/002: each frozen sign's attestation and
  occurrence count; for 003: the fraction of inscriptions
  whose tokens all carry §3 class labels, pre- and
  post-dedup); adapter health (unmapped/ambiguous counts).
- **Prohibited** in dry-run mode: computing `end_rate` /
  `start_rate` against the 0.45 thresholds, template
  conformance fractions, verdicts of any kind, or any
  per-sign meets-criterion flag. The gate is in the code
  path, not in reviewer vigilance: the scoring functions are
  unreachable from dry-run mode.

## 9. Implementation (this phase)

Following H15/H23 (graph-first, 5-step gate) and the
Phase-113–118 file pattern:

1. `backend/glossa_lab/pred_harness.py` — maps and class
   sets (§3), dedup (§5), adapters (§7), gating and scoring
   (§6), dry-run (§8). Pure functions over records; no
   hardcoded corpus data (H16): sign sets and maps load from
   the registry files at runtime, with the §3 hashes asserted
   in tests.
2. `backend/scripts/phase119_pred_harness.py` — the phase
   script: runs the fixture self-checks and the §8 dry run
   on the converted layer; writes
   `reports/phase119_pred_harness_results.json` and
   `reports/phase119_acquisition_log.json`. Includes
   `gpu_device` in its report (H20 pattern; no SA is run).
3. `backend/glossa_lab/experiment_graph_phase119.py` —
   node `IndusPhase119PredHarness`, registered in
   `experiment_graph.py` by try/except import and asserted
   present in `ATOMIC_NODES` **before** the script is run
   (H23 steps 2–4 precede step 5).
4. Fixtures under `backend/tests/fixtures/pred_harness/`:
   one toy input per adapter class, plus a toy converted
   layer.
5. `backend/tests/test_phase119_pred_harness.py` — unit
   tests including: dedup stage behavior on known inputs
   (incl. the Stage C length floor and the keep-anchor
   rule); the §3 map conflict rules (incl. M002 ambiguity);
   the class-set reproduction (14/12/46/33);
   **a toy prediction evaluated end-to-end on a toy
   independent fixture** (a synthetic `rmrl_concordance`
   fixture + a toy registered criterion exercised through
   the real gating and scoring code, asserting both a
   CONFIRMED and a REFUTED outcome on two toy datasets);
   the §4 gate refusing a non-qualifying class in evaluation
   mode; the §6.5 lock refusing a re-score; dry-run mode
   emitting the §8 label and no criterion statistic.
6. Full backend suite + foundation check (H21 — this phase
   adds phase result files under `reports/`); ruff clean.
7. Ledger entries in `LEDGER.md` and
   `glossa-indus/LEDGER.md` (H1), with AI disclosure.
8. One PR. **No merge** without the owner's explicit say-so.

## 10. What this phase does not do

It computes no verdict on PRED-2026-001–003. It acquires no
dataset and contacts no one (H14). It modifies no anchor,
claim, or language-model file. If, during the build, a real
qualifying dataset were somehow already in hand, this spec
would still not authorize evaluating it: that evaluation is
a separate, owner-authorized act, and the register's
"Tested/Outcome" fields are updated by that act, not by this
harness's existence.

---

## Appendix A — Design-stage measurements (computed at freeze time, before any harness code)

All numbers below are counts and coverage statistics on the
Phase-115 expanded ICIT converted layer
(`corpora/downloads/icit_fieldcady/icit_converted_v2.json`,
4,531 inscriptions, 15,880 tokens incl. `UNK` sentinels;
M-space). No criterion statistic (no rate against 0.45, no
conformance fraction) was computed. The harness dry run (§8)
must reproduce A.1 and A.2 through its own code path; a
mismatch is a build defect, not a new measurement.

### A.1 Dedup protocol (§5) on the current layer

| Stage | Kept | Removed (stage) | Removed (cumulative) |
|---|---|---|---|
| input | 4,531 | — | — |
| A exact | 3,080 | 1,451 (32.02%) | 32.02% |
| B sentinel-normalized exact | 2,716 | 364 | 40.06% |
| C near-dup (dist ≤ 1, stripped len ≥ 4) | 2,469 | 247 | 45.51% |

Stage A detail: all 1,451 exact duplicates sit in lengths
1–2 (1,451 of 1,990 such inscriptions, 72.91%); lengths ≥ 3
contribute zero — the layer builder had already removed
length ≥ 3 exact duplicates at build time (795 dropped at
source per `layer_build_meta_v2.json`, whose source-level
exact-duplicate count over 5,679 source inscriptions is the
same phenomenon Nair 2026 reports at ~24% for the raw
lineage; the rates differ because the populations and stage
definitions differ — both are recorded, neither is adjusted
to match the other).

### A.2 Sign-set coverage on the current layer (§3 map)

Occurrence counts (tokens) of the frozen signs in the layer:

- **TERMINAL14: attested 12/14.** Unattested: P076, P125.
  Counts: P020 19, P095 49, P099 31, P108 21, P210 42,
  P226 10, P256 70, P346 26, P359 11, P378 229, P384 11,
  P385 397.
- **INITIAL12: attested 11/12.** Unattested: P000.
  Counts: P001 89, P004 157, P013 156, P051 41, P098 304,
  P217 242, P238 14, P265 23, P301 66, P310 555, P324 1413.
- **MEDIAL46: attested 38/46.** Unattested: P091, P122,
  P127, P136, P201, P288, P332, P358.
- Unmapped under the §3 map: 47 tokens / 3 distinct M signs
  (incl. ambiguous M002 → `UNK`).
- PRED-003 classifiability coverage (§8 sense): inscriptions
  whose mapped signs all carry a §3 label — 2,544 / 4,531
  (56.15%) pre-dedup; 1,061 / 2,469 (42.97%) post-dedup.
  Inscriptions whose labels are all in {INITIAL, MEDIAL,
  TERMINAL}: 1,508 / 4,531 (33.28%) pre-dedup. (Coverage of
  the label set — **not** a conformance fraction; none was
  computed.)

### A.3 Class-set reproduction

The §3 rule on the frozen inventory file yields exactly
TERMINAL 14, INITIAL 12, MEDIAL 46, MIXED 33 — the register's
counts — with the three rate classes pairwise disjoint.
At `corpus_freq ≥ 5` the counts would be 20/13; at ≥ 20,
8/10; the floor of 10 is the one SIGN_INVENTORY §5 records
(INSUFFICIENT_DATA = freq < 10), and is therefore the floor
frozen in §3.

### A.4 Why the crosswalk-v2 map is not used (A2)

`mahadevan_parpola_crosswalk_v2.json`'s best-entry map
covers 179 M signs, only 131 of the layer's 284 attested;
under it, TERMINAL attestation collapses to 4/14 (P385 — the
dominant terminal of every other record — receives 0
tokens) and INITIAL to 3/12. The registry map (§3) covers
358 M signs, agrees with the inventory's own `mahadevan_ids`
on 353 of 358 shared signs, and leaves only 47 layer tokens
unmapped. The registry is the program's primary crosswalk of
record; the harness follows it.

### A.5 Evaluability matrix (summary of §4)

Qualifying today: **nothing** — no dataset of any qualifying
class is in hand. The dry run uses `icit_lineage_derivative`
(non-qualifying for all three predictions). When a dataset
of class `rmrl_concordance`, `image_transcription`, or
`future_concordance` is acquired, all three predictions
become evaluable on it (003 subject to its §6.1 site input);
`icit_full`, if ever obtained, evaluates all three under
caveat C1.

### A.6 Correction (2026-10-07, post-freeze, during build)

The A.1 stage counts and the post-dedup classifiability
figure in A.2 were measured by the design-stage prototype
on the layer's raw **M-space** sequences. Section 5 as
frozen operates on **adapter-emitted P-space** sequences,
and the harness — correctly implementing §5 — produces
slightly different counts, because the §3 map merges a few
distinct M sequences into identical P sequences. The
spec-conformant values, which the harness dry run asserts,
are:

| Stage | Kept | Removed (stage) | Removed (cumulative) |
|---|---|---|---|
| input | 4,531 | — | — |
| A exact | 3,063 | 1,468 (32.40%) | 32.40% |
| B sentinel-normalized exact | 2,693 | 370 | 40.79% |
| C near-dup (dist ≤ 1, stripped len ≥ 4) | 2,446 | 247 | 46.02% |

Post-dedup classifiability (A.2 sense): 1,045 / 2,446
(42.72%). The §5 parenthetical citing "45.51%" should read
46.02% (P-space cumulative). All other Appendix A figures
(per-sign occurrence counts, attestation, pre-dedup
classifiability, unmapped 47 tokens = 9 unmapped + 38
ambiguous) were reproduced by the harness exactly. The
frozen protocol text (§§3–9) is unchanged; only the
appendix's prototype measurements are corrected, here,
additively.

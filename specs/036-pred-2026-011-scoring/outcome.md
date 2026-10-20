# Spec 036 — Outcome

> ## EXECUTED — 2026-10-20 — VERDICT: CONFIRMED
>
> **PRED-2026-011 is CONFIRMED on its exact
> registered criterion.** Phase-400 executed the
> frozen Spec 036 contract on 2026-10-20 under
> the owner's do-all order ("do all of spec 036
> now", 2026-10-20). Step 0 passed in full
> (checks 0.1–0.4), the withheld file was opened,
> and the registered computation ran once, in
> full: **P217 — 119 Harappa occurrences, 104 in
> initial position, start rate 0.8739; P324 — 774
> Harappa occurrences, 473 in initial position,
> start rate 0.6111.** Both trained signs meet
> the 0.40 bar: share **1.0** (2 of 2) against
> the registered ≥ 70% criterion — **CONFIRMED**.
>
> The verdict is stated with its registered
> limits, here and everywhere it is carried: it
> concerns **only P217 and P324**, the two signs
> the disclosed screen retained, in this pinned
> dataset. It does not validate the INITIAL
> class as a whole, does not estimate a general
> cross-site preservation rate, and says
> **nothing about P000** — P000 was excluded at
> registration for a mapping-eligibility reason,
> and no Harappa behaviour for P000 was examined
> at any point in this execution. It establishes
> no decipherment, no sign meaning, and no sound
> value. The counts were verified by an
> independent recount through a separate code
> path before this record was written; the two
> computations agree exactly.

## 1. The registered test (as frozen)

PRED-2026-011, registered in
`docs/PREDICTION_REGISTER.md` on 2026-10-20:
signs assigned to the INITIAL class in training
on CISI Mohenjo-daro inscriptions ONLY, after
the disclosed mappability screen, will appear
preferentially in initial position in
Harappa-specific Yajnadevam data as well.

- **Trained set (screened, 2 signs):** P217,
  P324. Unscreened INITIAL set: P000, P217,
  P324 (P000 excluded by the screen — no
  best-match counterpart; mapping reason only).
- **Criterion:** at least 70% of the trained
  signs show a Harappa start rate of at least
  0.40, a start rate being the share of a sign's
  Harappa occurrences, counted through its
  best-match counterpart glyphs in the withheld
  file's Harappa sequences, in which it is the
  first sign of a sequence. With 2 signs the bar
  passes only at **2 of 2**.
- **Zero-occurrence rule (registered text,
  DD-036-2):** a mappable sign with zero Harappa
  occurrences does not meet the bar and remains
  in the denominator.
- **Unmappable cap:** any unmappable trained
  sign (50% of 2) exceeds the registered 20% cap
  and closes the scoring as CANNOT BE RUN AS
  WRITTEN before the withheld file is opened.
- **Verdicts:** CONFIRMED / NOT CONFIRMED only;
  no inconclusive band.

## 2. Execution basis

- **Freeze:** Spec 036 freeze digest
  `bbd5c4fd5abdb69bd79dfc1115a13e7debf56a7ec38d00ab8e2c8ff6132e946`
  (framework026, over register 0.9-draft as
  recovered through the AEE lifecycle gate —
  pass at after_specify / after_plan /
  after_tasks; `aee/freeze-aee-note.md`,
  `aee/recovery-specify.md`), PR #224 merged
  `3419df56` on green CI (7/7 from run
  conclusions).
- **Orders:** the owner's do-all order of
  2026-10-20 ("do all of spec 036 now") —
  freeze, the DD-036-4 spec-level OSF contract
  registration, and this execution in one act
  (`adjudication.md` §4).
- **Registrations:** the prediction's OSF
  preregistration **t6whq** (DOI
  10.17605/OSF.IO/T6WHQ) — the registration
  step 0 re-verified; the frozen spec's own OSF
  contract registration **gjen4**
  (https://osf.io/gjen4/), filed 2026-10-20
  under DD-036-4 before execution and recorded
  in `osf-spec-registration.md` (not a step-0
  condition; its approval state is recorded
  there by append).
- **Graph build (H15/H23):**
  `backend/scripts/phase400_pred011_scoring.py`
  + `backend/glossa_lab/experiment_graph_phase400.py`
  (node `IndusPhase400Pred011Scoring`),
  registered in
  `backend/glossa_lab/experiment_graph.py`;
  verified before the run — the node registered
  among the graph's atomic nodes and its serve
  path returned this phase's results.
- **Run:** against the freeze-merge tree (main
  `3419df56`), every input byte-verified against
  its registered pin before the run.

## 3. Step 0 — the frozen checks, in order

**All four checks passed.** The step-0 record
(`reports/phase400_results.json`, step-0 record
sha256
`2bf0333b7d7fc437c9055299598ee83f0247acd08c7fa8b123044114e0c8e427`)
was written and hashed before any scoring.

### Check 0.1 — Registration standing: PASS

OSF **t6whq** re-verified via the API at
execution: `reviews_state: accepted`,
`public: true`, `pending_registration_approval:
false`, not withdrawn; `date_registered`
2026-10-20T12:54:02Z. This check remained a
kill condition throughout the run.

### Check 0.2 — Input integrity: PASS

Byte hashes (SHA-256) matched the registered
pins exactly: corpus file `b19cfe95…`, crosswalk
`e44b8b55…`, withheld file `c02e3d7b…` (byte
operations only — the withheld file's content
was not opened at step 0). The derivation
record's internal pins were also asserted
against the same registered values (including
the manifest pin `ab3b4c8a…`, re-derived at
check 0.3).

### Check 0.3 — Pool, classification, and screen reproduction: PASS

The filtered pool reproduced as registered:
**179** CISI Mohenjo-daro rows, all
Mohenjo-daro, **zero** Yajnadevam rows, and the
filtered-pool manifest hashed to the registered
pin (`ab3b4c8a…`). The recorded classification
logic (carried verbatim in the frozen Phase-396
build) reproduced the derivation record
**exactly**: the full class map identical (28
classifiable signs; INITIAL 3 / MEDIAL 19 /
MIXED 3 / TERMINAL 3) and the unscreened INITIAL
set **{P000, P217, P324}**. The registered
screen, re-applied by the derivation build's own
screen function to the pinned crosswalk,
returned the trained set **{P217, P324}**
exactly, with **P000's exclusion reproduced as
a screen outcome** (no best-match row;
`top3_parpola` appearances on Y0527, Y0740,
Y0820, Y0892 only) and the recorded counterparts
identical to the derivation record. The training
withholding this scoring depends on was
therefore re-verified clean.

### Check 0.4 — Crosswalk coverage: PASS (as expected at design)

Under the frozen reading (DD-036-5: best-match
rows carry sign identity; `top3_parpola`
appearances set conflict flags only):

| Trained sign | Counterpart glyph | Confidence | Status | Conflict flag |
|---|---|---|---|---|
| P217 | Y0520 (sole best-match row) | 1.0 | confirmed | No |
| P324 | Y0740 (sole best-match row) | 0.9867 | confirmed | Yes |

P324's flag: P324 also appears as a
`top3_parpola` alternative on other glyphs'
rows (Y0740's own row and Y0741), the Spec 035
record's conflict observation. The Y0520 and
Y0740 rows' own `top3` columns name no trained
sign besides their own best matches' —
alternatively stated, no counterpart glyph's
row makes another trained sign its best match.
Unmappable trained signs: **none** (share 0.0
against the registered 20% cap). **Check 0.4
passes: the scoring opens.** The draft-stage
expectation recorded at §0.4 of the spec was
borne out by the formal step-0 determination;
the determination, not the expectation, is what
this record reports.

### Step-0 conclusion

Step 0 passed in full. The withheld file's
content was opened only after all four checks
passed. No closure fired; nothing in this
section is a verdict.

## 4. Step 1 — Scoring

The registered computation (spec §5), run once,
in full, behind the step-0 pass. The scoring
function is the frozen Phase-396 build's
(`score_registered_test` with `fix_crosswalk`,
imported unchanged); the counts below are its
output on the pinned bytes, verified by an
independent recount (below).

- **Scoring pool:** the withheld file's
  Harappa-site rows — **2,717** of 5,679 rows.
  Tokenised under the programme's parser for
  this dataset (the Phase-284 build's
  `parse_lipi`, carried in substance: split on
  `-`, bracket markers stripped, only 3-digit
  sign codes kept — that parser excludes the
  `000` eroded-sign placeholder — in recorded
  order; codes carried as `Y` + zero-padded
  four digits): **2,621** sequences, **7,144**
  tokens; 96 Harappa rows yielded no tokens
  under the parser. Within those sequences,
  tokens with no crosswalk mapping kept their
  positions as unmappable placeholders, so
  initial position is position in the sequence
  as recorded.
- **Per-sign table** (descriptive; F036-C12):

| Sign | Counterpart | Harappa occurrences | Initial occurrences | Start rate | Meets 0.40 bar |
|---|---|---|---|---|---|
| P217 | Y0520 | 119 | 104 | 0.8739 | yes |
| P324 | Y0740 | 774 | 473 | 0.6111 | yes |

  P324 carries the crosswalk conflict flag (its
  counterpart position is shared with P000
  under one alternative reading); the flag is
  reported, not resolved by hand, and the
  criterion does not adjust for it.
- **Share:** 2 of 2 signs at start rate ≥ 0.40
  → share **1.0**, at or above the registered
  70% bar.
- **Unmappable share:** 0 of 2 (0.0) — reported
  with the outcome per spec §6; it does not
  lead the verdict sentence (it does not exceed
  the cap; §0.4 passed).
- **Verification:** the counted quantities were
  recomputed through a separate code path
  (direct crosswalk + file parse, no Phase-396
  code) before this record was written: P217
  119 / 104 / 0.8739 and P324 774 / 473 / 0.6111,
  2,621 sequences, 7,144 tokens — exact
  agreement.

## 5. Verdict

> **CONFIRMED.** Under the registered criterion,
> at least 70% of the trained INITIAL signs
> (P217, P324) show a Harappa start rate of at
> least 0.40 in the withheld Yajnadevam Harappa
> data — 2 of 2, share 1.0 (P217: 0.8739; P324:
> 0.6111).

Stated with the registered caveats, which are
part of the verdict wherever it is carried
(F036-C07, F036-C13):

- **Two signs only.** Each sign carried half
  the verdict; the possible shares were only 0,
  1/2, and 1. The verdict establishes that P217
  and P324 both met the bar in this pinned
  dataset — nothing more general.
- **Not the INITIAL class.** A pass does not
  validate the INITIAL class as a whole or
  estimate a general cross-site preservation
  rate; the wider class claim would need a
  larger clean training pool than the CISI
  Mohenjo-daro data provides.
- **Nothing about P000.** P000 was excluded at
  registration because it lacks a best-match
  crosswalk counterpart — not because of any
  observed Harappa behaviour — and this
  execution examined no Harappa behaviour for
  P000. The verdict neither confirms nor denies
  anything about P000's positional behaviour.
- **Site withholding, not lineage
  independence.** The independence this test has
  is the one the registration specified: Harappa
  held out of the training pool, re-verified at
  step 0. The Yajnadevam compilation's object
  base is itself published-corpus material; no
  independence of scholarly lineage is claimed.
- **Cleanliness basis.** Verified
  training-pool exclusion, re-verified at step
  0 — not analyst blindness (the Harappa pool
  was inspected in aggregate during the Spec
  032 closure audit, as disclosed at
  registration; no Harappa start rate had ever
  been computed for P217 or P324 before this
  run).
- **Positional fact only.** The method is
  positional classification only (no semantic
  anchoring, H26). The verdict says nothing
  about what the signs mean, what sounds they
  carry, or whether the script is deciphered.

## 6. Claim consequences (F036 register)

- **F036-C01 — upheld.** The verdict states
  only whether the registered criterion is met:
  CONFIRMED, on the criterion as registered.
- **F036-C02 — decided.** The registered
  criterion, applied once to the counted
  quantities: 2 of 2 at or above 0.40, share
  1.0 ≥ 0.70 → CONFIRMED. No band was added.
- **F036-C03 — verified at execution.** The
  trained set is the registration's screened
  set {P217, P324}; step 0 check 0.3 reproduced
  it exactly.
- **F036-C04 — satisfied.** Step 0 reproduced
  the pool, the classification, and the screen
  exactly, before any withheld content was
  opened; the withheld file was opened only
  behind the full pass.
- **F036-C05 — verified at execution.** All
  four pins matched bytewise in the run tree
  and again inside the run (check 0.2; the
  manifest re-derived at check 0.3).
- **F036-C06 — verified at execution.** t6whq
  stood accepted and public at step 0 check
  0.1.
- **F036-C07 — carried.** The outcome is
  reported under the registration's own bars
  and wording, with the within-lineage caution
  stated in §5 of this record.
- **F036-C08 — applied.** Sign identity was
  carried only by the frozen crosswalk's
  best-match rows (P217 → Y0520; P324 → Y0740);
  no alternative mapping was substituted.
- **F036-C09 — tested, did not fire.** No
  trained sign was unmappable at check 0.4
  (share 0.0 ≤ the 20% cap), so no closure
  fired and the scoring opened — the outcome
  this claim's execution branch governs.
- **F036-C10 — executed as specified.** The
  counted quantities are exactly the frozen
  Phase-396 computation's: occurrences, initial
  occurrences, and start rates as tabled in §4.
- **F036-C11 — carried (not triggered).** Both
  trained signs have Harappa occurrences (119
  and 774), so the zero-occurrence rule had no
  application in this run; the rule stands as
  registered text.
- **F036-C12 — satisfied.** The per-sign table
  is published in §4 as the descriptive record;
  it carried no criterion and moved no verdict.
- **F036-C13 — carried.** Every outcome
  statement in this record carries the
  small-set caveat and the P000 silence (§5).
- **F036-C14 — executed.** The outcome is
  appended to the prediction register as a
  dated §6 entry, and PRED-2026-011's §3
  Tested/Outcome fields move from PENDING to
  the verdict in the same act (this record's
  PR); the Phase D pin is advanced by name for
  that authorised change. PRED-2026-006's and
  PRED-2026-010's entries are byte-identical
  and untouched.
- **F036-C15 — carried (not triggered).** No
  step-0 closure occurred, so there was nothing
  to report as a closure; the claim's discipline
  governed the run's design throughout.

## 7. Records and named confounders

- **Step-0 record:** `reports/phase400_results.json`
  (step-0 record sha256
  `2bf0333b7d7fc437c9055299598ee83f0247acd08c7fa8b123044114e0c8e427`;
  scoring record sha256
  `101d54f5bd93d963402d73731962801294452c00f4fe4183e9135ba348ddb07f`).
  Execution script:
  `backend/scripts/phase400_pred011_scoring.py`;
  graph node: `IndusPhase400Pred011Scoring`.
- **Registers:** the prediction-register §6
  dated entry and §3 Tested/Outcome move (this
  PR); the Spec 029 Phase D register-hash pin
  advanced by name for that authorised change;
  LEDGER entry (this PR).
- **Sequence-length composition** (descriptive,
  spec §8): Harappa sequences are short —
  median length 2 across the 2,621 tokenised
  sequences (581 of them single-sign; lengths
  run 1–13, 7,144 tokens in all). A one-sign
  sequence counts its only sign as initial,
  under the registered computation. Composition
  differs from the training site's, and the
  registered criterion does not adjust for it;
  no adjustment was made, and the composition
  is reported here so any reader can see it.
- **What remains open:** nothing under this
  spec. PRED-2026-011 is scored. Any broader
  cross-site claim would need a larger clean
  training pool and a new prediction under a
  new PRED number; none is registered by this
  record.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

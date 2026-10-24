# Spec 040 — Freeze Record (D-25: G1 chronology-controlled rerun)

> ## FROZEN — 2026-10-24
>
> Frozen at the freeze act of 2026-10-24 under
> the owner's approval of the freeze plan as
> specified (2026-10-24, 10:54 EDT, "Approve as
> specified"; recorded in `adjudication.md`
> §5). Spec §1's dependency gate is judged
> satisfied by the **openly recorded
> successor-artifact substitution** of Spec
> 041's artifact (§1 below): Spec 039's own
> artifact did not satisfy §1, and that finding
> stands unamended. The AEE lifecycle hooks ran
> **first**, at the freeze gate (tasks L4),
> over the claim register recovered in two
> rounds at the freeze (0.5-draft → 0.7-draft);
> the freeze digest (`freeze.json`) was
> computed over the recovered register and the
> finalised freeze texts **exactly once**.
> Derivation **A1** governs. The OSF
> registration for the frozen spec is filed at
> the freeze under DD-040-9; it is recorded in
> `osf-spec-registration.md` (completed by
> append after filing). **This freeze executes
> nothing.** Execution (Phase-439) requires a
> separate owner order.

## 1. Basis

The contract is design D-25 (PR #195
portfolio) over the Spec 025 / Phase-140 /
Phase-385 record: G1 SUPPORTED under
composition and preservation control,
margin-completed at the governing basic
interval [0.1838, 0.2102] against the V = 0.10
floor, with the standing rider that chronology
is not controlled. The owner's 2026-10-20
bundle decision sequenced the gazetteer act
(Spec 039, published determinations only)
before this spec, and spec §1 turned that
sequence into a fail-closed freeze gate.

The freeze attempt of 2026-10-20 closed
**NOT-YET-TESTABLE — dependency gate**: Spec
039 had executed (freeze digest
`ec53a841a7f7f7afd56ab69f1caf23557e1e26c834d35563c42990ce66aa2742`),
but its artifact —
`data/movement/gazetteer_rows_assigned.jsonl`,
SHA-256
`64f288d35c492d8babacb4efb9c7446573a62168095db44f7469cd7904fcabb4`
(recomputed at this freeze) — assigns periods
per site as label sets with no site ×
local-label mapping key, and carries no rows
for three of the seven G1 sites. Spec §1
conditions 2 and 4 failed. The interface was
not loosened to fit the product.

Spec 040's closure stated what would satisfy
the gate: a future, separately governed act
producing a frozen, machine-readable mapping
keyed by site × the layer's recorded local
chronological label(s), every grounded mapping
carrying its published citation, locator, and
contested flag, under published determinations
only. Spec 041 was commissioned as that act.
It froze on 2026-10-22 (freeze digest
`fe6188864d5ff497fed5e3e89456d0499987c2cbc8ada5997920e864360dfdc7`)
and executed as Phase-435. **This freeze
accepts Spec 041's artifact as the successor
dependency artifact for §1, on the openly
recorded basis of `adjudication.md` §5.1.** It
does not pretend Spec 041's artifact is Spec
039's product, and it does not amend Spec
039's or Spec 041's records.

## 2. Owner rulings at the freeze

The approval of the freeze plan as specified
(`adjudication.md` §5) carries:

1. **The §1 judgment (plan R1)** — satisfied
   by the successor-artifact substitution
   recorded at §1 above and `adjudication.md`
   §5.1.
2. **Derivation A1 (plan R3)** — the sole
   primary row derivation: a row is placed
   when at least one of its recorded labels is
   MAPPED and every MAPPED label agrees on one
   coarse period; an UNASSIGNED label does not
   veto; disagreement between MAPPED labels,
   no recorded label, or all labels UNASSIGNED
   leaves the row UNASSIGNED in the primary.
   No field precedence applies. A2, B and C are
   not chosen.
3. **DD-040-1 — ADOPTED.** The governing basic
   bootstrap interval against the V = 0.10
   margin assigns any eventual §6 outcome; the
   permutation p is computed and reported but
   cannot rescue an interval that fails the
   margin; no p-value threshold is a second
   gate.
4. **DD-040-5 — CONFIRMED.** The thinness
   closure's word is **NOT-YET-TESTABLE**, not
   D-25's "INCONCLUSIVE-BY-DESIGN."
5. **DD-040-6 — RETAINED.** The third §5
   margins arm (at least 1,000 permutable
   inscriptions) stays in the frozen gate; all
   three §5 arms are retained.
6. **DD-040-9 — FILED.** The frozen spec files
   its own OSF registration at the freeze.
7. **DD-040-10 — ALLOCATED.** The execution
   phase allocated mechanically at this act is
   **Phase-439** (the highest phase on the
   merged record at the act is Phase-438, Spec
   054's).
8. **§8.1 — NOT APPLICABLE.** The accepted
   artifact contains zero CONTESTED cells:
   there are no contested mappings to include
   and no sensitivity label to consume.
   Candidate disagreement strands preserved
   inside Spec 041's determination sets are
   not reclassified as contested cells.

The approval is of the freeze package. It is
not an execution order.

## 3. Pins at the freeze

Recomputed at the freeze against the merged
record as it stands (main at `58bb6ac7`):

| Pin | Value at the freeze |
| --- | --- |
| Spec 039 freeze digest | `ec53a841a7f7f7afd56ab69f1caf23557e1e26c834d35563c42990ce66aa2742` (`specs/039-gazetteer-period-assignment/freeze.json`) |
| Spec 039 artifact (did not satisfy §1) | `data/movement/gazetteer_rows_assigned.jsonl`, SHA-256 `64f288d35c492d8babacb4efb9c7446573a62168095db44f7469cd7904fcabb4` — recomputed |
| Spec 041 freeze digest | `fe6188864d5ff497fed5e3e89456d0499987c2cbc8ada5997920e864360dfdc7` (`specs/041-site-local-label-period-mapping/freeze.json`) |
| **Accepted dependency artifact (Spec 041)** | `data/evidence_integration/site_period_mapping.jsonl`, SHA-256 `1e5b54c9193fb52092c34e1c959ec64a48b83cacbb8e5705f629635183c12b67` — recomputed; 78 cells: 24 MAPPED (4 EARLY, 18 MATURE, 2 LATE), 54 UNASSIGNED, 0 CONTESTED |
| Spec 041 artifact meta record | `data/evidence_integration/site_period_mapping_meta.json`, SHA-256 `bda1017dd88da0b14efaa3ffc5ff280b09818349bda4de1ed20f8c60d42864a9` — recomputed |
| Spec 041 step-0 census | `specs/041-site-local-label-period-mapping/step0-census.json`, SHA-256 `b57fb6b1a0aa1e491ba38bf18978eec58c355f3bf833f58298c7516aabeca6be` — recomputed |
| ICIT-lineage layer (horus84 `inscriptions.csv`) | SHA-256 `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef` (the Phase-137/139/140 file; the §4.1 join at this freeze runs over the pinned Phase-139 covariates, whose agreement with the layer on all 5,410 population rows Spec 041's step-0 gate G0.3 verified) |
| Phase-139 covariates | `data/evidence_integration/phase139_harmonized_covariates.json`, SHA-256 `a0f0d05a578826208e3fee5c8e1e296c44db3450d9ef27a9a837a57123b04413` — recomputed; 5,410 rows |
| Extended chronology spine | `data/movement/chronology_rows_phase394.jsonl`, SHA-256 `9dc2fba5019c34ecc57bb1bda3c341ac142876f8ee5c4f058807458faf7eae93` — recomputed; 205 rows; never an inscription label |
| Anchors | `backend/reports/INDUS_FINAL_ANCHORS.json`, SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` — recomputed; the draft's stale `eccea6d5…` pin refreshed at this freeze; this spec moves no anchor |

**§1 verification at the freeze (plan R2).**
The artifact validates against the frozen
schema: every MAPPED cell carries exactly one
determination verified `OWN_TEXT` with its
citation, locator, mapping rule and
`contested: false`; every UNASSIGNED cell
carries exactly one enumerated reason
(NO_PUBLISHED_DETERMINATION 35,
DETERMINATION_UNVERIFIED 10,
SPANS_COARSE_BOUNDARY 4, LABEL_UNCERTAIN_IN_LAYER 3,
NOT_IN_PUBLISHED_SCHEME 2). The cell census
built from the pinned covariates equals the
artifact's 78 (site, field, local label)
triples exactly, every `attested_rows` equal;
the population margins reproduce exactly
(period labels 2,266; phase labels 2,638; both
1,788; any label 3,116; neither 2,294). The
§4.1 three-record join under A1 yields exactly
one assignment row for each of the 5,410
population inscription IDs — no missing ID,
duplicate, extra row, or site mismatch — and
reproduces Spec 041's published A1 counts
exactly: **1,457 placed** (EARLY 32, MATURE
1,386, LATE 39); 3,953 unplaced (2,294 no
informative label; 1,658 all labels
UNASSIGNED; 1 disagreement, unplaced). Placed
by site: Dholavira 133, Harappa 1,021,
Kalibangan 157, Lothal 108, Nausharo 38,
Mohenjo-daro 0, Chanhu-daro 0. This
verification is pinned as a standing freeze
test (`backend/tests/test_spec040_freeze.py`).
No G1 quantity was computed at this freeze.

## 4. The known margins consequence — stated, not hidden

On the counts §3 reproduces, Spec 040 §5's
margins gate already fails under **every**
derivation: EARLY retains assigned
inscriptions from 1 distinct site (Harappa)
and LATE from 2 (Dholavira, Lothal), against
the 5-site arm; the unassigned share exceeds
the 40% arm under every derivation (A1/C
73.1%, B 74.8%, A2 85.6%); Mohenjo-daro places
0 of its 1,923 population rows under every
derivation. This freeze is therefore a
**dependency-settlement and closure act**: it
settles the dependency and the derivation and
locks the contract. If execution is later
ordered and §5 is retained unchanged, the
expected outcome is **NOT-YET-TESTABLE at the
margins gate**, not a chronology-controlled
verdict on G1. A later execution must
recompute its margins from the pinned inputs;
a material difference from §3's counts is a
premise discrepancy and a tripwire, not a
welcome surprise. No part of this freeze
loosens §5 to make the test run.

## 5. Freeze-stage exhibits

- **AEE lifecycle hooks (tasks L4).** Passed
  on the DD-038-10 reading after two recovery
  rounds (register 0.5-draft → 0.7-draft): at
  after_specify, after_plan and after_tasks,
  15 failure modes, every one an FR-2.3
  draft-cap record; zero correctness failure
  modes; minimum propagated confidence 0.8445
  against the 0.70 threshold. Full record:
  `aee/freeze-aee-note.md`.
- **Freeze tests.**
  `backend/tests/test_spec040_freeze.py` (see
  §8 for their able-to-fail proof).
- **House gates.** The freeze PR's CI is
  reported from the merge record, not here;
  this freeze claims nothing about it beyond
  what the run's own job conclusions state.

## 6. Machine record

`freeze.json` in this directory is the
canonical JSON record (framework026
`build_freeze`, computed by `build_freeze.py`
in this directory). Covered sources (nothing
else decides the question):

- `specs/040-d25-g1-chronology-controlled/freeze.md`
  (this document)
- `specs/040-d25-g1-chronology-controlled/spec.md`
- `specs/040-d25-g1-chronology-controlled/claims.json`
- `specs/040-d25-g1-chronology-controlled/adjudication.md`
- `specs/040-d25-g1-chronology-controlled/aee/freeze-aee-note.md`
- `specs/040-d25-g1-chronology-controlled/build_freeze.py`
- `backend/tests/test_spec040_freeze.py`

`plan.md`, `tasks.md`, and `outcome.md` are
lifecycle bookkeeping and are not
digest-covered (the house rule since Spec
026: plans change as work proceeds).

- Register: `claims.json`, **15 claims**
  (F040-C01…C15), register version
  **0.7-draft** after recovery.
- AEE hooks (aee 1.5.3, lenient load, evidence
  verification off, no ledger): stamps
  20261024T150459Z (after_specify),
  20261024T150502Z (after_plan),
  20261024T150506Z (after_tasks) — UTC stamps
  of the 2026-10-24 owner-local freeze act.
- Environment: Python 3.12.3;
  applied-epistemic-engineering 1.5.3 (program
  pin `>=1.5.0,<1.6`); spec-kit `specify`
  1.0.10.
- Phase allocated at this freeze:
  **Phase-439** (DD-040-10).

## 7. What the freeze fixes

- **The dependency** (spec §1 / F040-C02):
  the Spec 039 freeze digest, outcome, and
  artifact named in this record as the
  executed act whose product did not satisfy
  §1; and Spec 041's artifact named as the
  accepted successor dependency artifact, at
  its pin. A freeze without both namings is
  not a freeze of this contract.
- **The derivation** (spec §4 / F040-C04):
  A1, as §2 states it; unique uncontested
  published-determination mappings at
  site-period resolution place a row;
  everything else is UNASSIGNED in the
  primary. §8.1 contested-included is NOT
  APPLICABLE on the zero-contested-cell
  record.
- **The margins gate** (spec §5 / F040-C12):
  ≥ 5 sites in each coarse period, ≤ 40%
  unassigned, ≥ 1,000 permutable (third arm
  retained per DD-040-6); failure closes the
  execution NOT-YET-TESTABLE (DD-040-5) before
  any outcome quantity exists.
- **The primary test** (spec §6 /
  F040-C05…C08): the Phase-137 population and
  columns; strata composition × preservation
  × period; χ² with 9,999 permutations under
  seed 20261009; the Phase-385 v2 basic
  bootstrap interval (B = 4,999, seed
  20261012) governing against the V = 0.10
  margin (DD-040-1).
- **The outcome mapping** (spec §6.4 /
  F040-C09…C11): interval entirely above the
  margin → SUPPORTED — CHRONOLOGY CONTROLLED
  (rider retired by append); straddling →
  WEAKENED — RIDER CONFIRMED AS MATERIAL (G1
  restated as a period-confounded
  association); entirely at or below →
  CONTRADICTED AT THE DECLARED MARGIN.
- **The record discipline** (spec §10 /
  F040-C15): dated appends only; the lineage
  label and assignment census on every
  headline; no frozen record edited; no
  anchor moved; no PRED contact.

## 8. Able-to-fail proof of the freeze tests

With the freeze tests green over the final
texts, exactly one character of
`specs/040-d25-g1-chronology-controlled/freeze.md`
(a digest-covered source) was changed; the
freeze tests went red on the replay assertion,
as required. The character was then reverted
byte-identically and the tests returned to
green. The digest in `freeze.json` was
computed once, after the revert, over the
final texts.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

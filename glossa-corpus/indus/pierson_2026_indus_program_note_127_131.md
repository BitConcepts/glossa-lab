# Program note, Phases 127–131 and specs 021–022: the disagreement is not sampling noise, its mechanism is mostly unattributed, and the release record is now hash-gated

**Tristen Pierson** (BitConcepts LLC) — ORCID 0009-0003-7269-956X

Program note, 2026-10-09. Prepared as an addendum to the program's
preprint record (Zenodo concept record DOI
10.5281/zenodo.20379070; previous published version v4.3.0, DOI
10.5281/zenodo.23250395, record 23250395). Program provenance
registry: OSF [osf.io/ybd65](https://osf.io/ybd65/). Code, frozen
specs, and machine-readable results: BitConcepts/glossa-lab
(Phases 127–131; specs 021 and 022; repository main at commit
257ed964dfcc8d4c7068e01308efd8532bdaa65b).

This note reports the outcomes of Phases 127–131 and specs
021–022 exactly as they stand in the merged reports, negatives
included. None of these phases changed any decipherment anchor:
the anchors file `backend/reports/INDUS_FINAL_ANCHORS.json` is
byte-identical throughout (sha256
eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed,
asserted in code in each phase). The Phase-125 verdict — **FAIL —
DISAGREEMENT** — is final and unchanged, and spec 020's
adjudication outcome — **NO** — stands untouched.
**PRED-2026-001 and PRED-2026-002 remain PENDING.** No phase in
this note is evidence that any particular reading of any Indus
sign is right or wrong.

## Abstract

Five phases and two specs followed up the Phase-125
cross-compilation failure, hardened the program's release
integrity, and built the machinery for receiving a genuinely
independent dataset. Phase-127 (spec 021) decomposed the
Phase-125 disagreement and found it is **not a sampling
artifact**: at matched sizes, pure Holdat-internal sampling
expects a median total-variation distance of 0.082613 (95%
interval 0.046665–0.131316) against the observed 0.636931, and
**0 of 999** matched-size replicates reached the observed
median. Phase-128 assembled integrated evidence dossiers for
the 44 pending anchors (evidence-complete 1, segmentation-
contested 15, crosswalk-contested 25, not-covered 3,
evidence-thin 10) — descriptive only, with no status
recommendation. A release-integrity audit found that the
v4.2.0 Zenodo deposit had been built from a stale, CRLF,
out-of-tree copy of the anchors file (a staging error, since
corrected in v4.3.0), and shipped a mandatory pre-deposit hash
gate so that class of error fails loudly before publication.
Phase-129's CISI cropper v2 beat the frozen v1 benchmark
(50 good / 42 partial / 15 bad of 107, against v1's frozen
38 / 29 / 15 of 82) and cut **14,166 crops** over the full
catalogue — all local-only under the volumes' copyright.
Phase-130 (spec 021) built the independent-data intake pack:
schema, license-gated validator, shared deduplication module,
and a dry-run-only runbook; no real external data was ingested.
Phase-131 (spec 022) then attributed the Phase-125 disagreement
to mechanisms under frozen estimators — and attributed almost
none of it: the matched-object join yielded only **4 matched
pairs (0 exact)**, so matched-object TV is **NOT ESTIMABLE**;
reading direction is **not supported** (reversed-arm median TV
0.582205, above the Phase-127 noise-band upper bound 0.131316;
credited share 0.000); composition explains a share of
**0.061321**; segmentation, substitution, and
insertion/deletion shares are **NOT ESTIMABLE**; and the
**residual unexplained share is 0.938679**.

## 1. Phase-127 (spec 021) — Cross-compilation disagreement diagnostic: not a sampling artifact

Phase-127 decomposed the observed distances of the finished
Phase-125 result (16 judgeable pairs of 286; median TV
0.636931; Spearman ρ initial −0.424758 / terminal 0.316034;
pairing-shuffle null p = 0.824) under estimators frozen in
spec 021 before any diagnostic statistic existed. It did not
re-score Phase-125 and issued no verdict.

| Component | Figure |
|---|---|
| Observed median TV (Phase-125, of record) | 0.636931 |
| Split-half noise floor, raw (median of per-sign medians) | 0.059538 |
| Split-half noise floor, full-size estimate (÷ √2) | 0.042100 |
| Matched-size expected median TV (Holdat at mayig sizes) | 0.082613 (95% interval 0.046665–0.131316) |
| Share of 999 matched-size replicates with median TV ≥ observed | 0.000000 (0/999) |
| Bootstrap CI for the median TV | 0.548638–0.722042 (bootstrap median 0.643877) |
| Median ambiguity share per judgeable pair | 0.666667 |
| Median attributable TV (crosswalk arm, spec §6 estimator) | 0.000000 (share −0.185664) |
| Composition controls — site (Mohenjo-daro) | median TV 0.599138 (13 judgeable) |
| Composition controls — iconography (unicorn) | median TV 0.650510 (13 judgeable) |
| Composition controls — site and iconography | median TV 0.602896 (11 judgeable) |
| Power: tokens-per-sign for the median-TV gate to clear the noise criterion | 8 (also 8 for the per-sign criterion; grid maximum 256) |

The disagreement is therefore not accounted for by the
sampling nulls, the mapping-choice estimator, or the
composition controls at the observed sizes. Phase-127
attributed the residual to no side or mechanism; that question
was left to Phase-131 (§6 below). Report:
`reports/phase127_cross_compilation_diagnostic.md`; spec:
`specs/021-phase127-cross-compilation-diagnostic/`.

## 2. Phase-128 — Integrated evidence dossiers for the 44 pending anchors

Phase-128 joined, per anchor, the Phase-120–127 evidence
records that exist for the 44 `pending_non_sa_validation`
anchors — descriptive synthesis only: no status
recommendation, no adjudication, no prediction content, and
missing records recorded as NOT-COVERED, never inferred.
Join integrity: **44 anchors in = 44 dossiers out** (asserted
in code and tests). Triage buckets (deterministic rules stated
in the report before membership; buckets 1–4 are independent
predicates and may overlap; evidence-thin is the defined
residual):

| Bucket | Count | Membership |
|---|---|---|
| evidence-complete | 1 | M072 |
| segmentation-contested | 15 | M011, M028, M102, M103, M155, M168, M169, M178, M237, M254, M293, M332, M345, M383, M402 |
| crosswalk-contested | 25 | M011, M021, M024, M028, M031, M035, M036, M040, M058, M071, M072, M102, M103, M127, M149, M153, M155, M168, M169, M177, M239, M293, M350, M401, M412 |
| not-covered | 3 | M033, M058, M281 |
| evidence-thin | 10 | M183, M223, M235, M262, M270, M272, M304, M355, M365, M416 |

What the dossiers cannot do, stated in the report: Bhaskar
covers 1 of 44 anchors (M402 CONTESTED; 43 NOT-COVERED); the
Phase-125 judgeable subset contains exactly 1 of the 44
(M072); and every dossier carries the uniform spec-020
limitation field `NOT-EVALUABLE-VIA-SOVIET-DATASET` — recorded
as a limitation, not as per-sign evidence. Reports:
`reports/phase128_evidence_dossiers_44.md` (+ `.json`, `.csv`).

## 3. Release-integrity audit and the hash gate

An owner-ordered audit of the Zenodo v4.2.0 deposit (record
23223655, DOI 10.5281/zenodo.23223655, created
2026-10-07T22:12:48Z) returned verdict **(i) STAGING ERROR**:
its deposited `INDUS_FINAL_ANCHORS.json` (391,969 bytes;
downloaded sha256
841e9067a68c933d3b9511ba95f5efae23b80a5fad0f083a8eedbde6cf078fdf)
matched **no committed repo version** — its parsed content is
exactly the 2026-05-27 anchors state with CRLF line endings, a
stale Windows working-tree copy deposited more than a day
after the repo file had become sha256 eccea6d5… (Phase-110
Part B, 2026-10-06). Verdict (ii), legitimate-at-the-time, was
falsified. The v4.3.0 deposit (record 23250395) already
deposits the correct eccea6d5… file, byte-identical to the
repo. Remedy shipped with the audit:
`backend/scripts/release_gate.py` (offline, stdlib-only) plus
`docs/RELEASE_CHECKLIST.md`, making a per-file hash gate —
every deposited file staged from a clean checkout at a named
commit and hash-compared against its named repo source, on
raw bytes — a **mandatory, blocking** step before any deposit,
with the gate output recorded in the release record. This
v4.4.0 release was produced under that checklist. Report:
`reports/release_integrity_audit_v420.md`.

## 4. Phase-129 — CISI cropper v2: benchmark win; 14,166 local-only crops

An enabling asset only — no sign identifications. The
protocol was frozen before any tuning (commit 8a85c55f); the
benchmark is Phase-124's 82-crop worked sample under the
Phase-124 rubric verbatim, with v1's grades frozen at
38 good / 29 partial / 15 bad. Cropper v2 (illumination
normalisation, sharper projection, valley-capped hysteresis
edges, valley splitting, a stroke-content rejection gate, and
fitted crop heights; deterministic, CPU, numpy + Pillow)
graded **50 good / 42 partial / 15 bad of 107**. All three
frozen win clauses were met (good > 38, bad ≤ 15,
41 ≤ total ≤ 123) — **v2 beats v1**, as a recall win at
constant bad count and constant good rate, not a precision
claim; the per-crop regression list is in the report.

The win opened the expansion gate: v2 over the full
Phase-124 catalogue produced **14,166 crops** (Vol. 1: 6,438;
Vol. 2: 7,728) covering 3,287 distinct CISI IDs, in the local
store only — manifest == disk exactly (14,166 unique
filenames); no image, crop, render, or per-crop grade is in
git or in this deposit, under the volumes' copyright. A first
expansion attempt was discarded (its benchmark exclusion
matched only 4/34 photos and 7 filenames collided) and the
harness fixed before the clean re-run. A fixed-seed
spot-check of 30 expansion crops graded 8 good / 10 partial /
12 bad, for context only. Report:
`reports/phase129_cisi_cropper_v2.md`.

## 5. Phase-130 (spec 021) — Independent-data intake pack

The intake-side companion to spec 018 (Phase-119): the
machinery that receives a genuinely independent inscription
dataset when one lands. **No real external data was
ingested, no one was contacted, and nothing was sent**; the
only end-to-end exercise is a synthetic fixture (invented
signs P901–P905, invented sites). Deliverables: (1) intake
schema v1 (`data/intake/intake_dataset_schema_v1.json`), whose
REQUIRED fields are exactly the fields spec 018's
evaluability and deduplication machinery consume; (2) a
stdlib-only validator with structured pass /
pass-with-warnings / reject verdicts — the license gate is
hard: a dataset with no declared lawful basis is a REJECT
(`LICENSE_BASIS_MISSING`), never a warning; (3) the frozen
spec 018 §5 deduplication protocol (Stage A exact / Stage B
sentinel-normalized / Stage C near-duplicate) lifted verbatim
into the shared module `backend/glossa_lab/dedup.py` — on the
converted layer it reproduces the measured numbers (4,531 in;
stages 1,468 / 370 / 247; kept 2,446; cumulative removal
46.02%); (4) crosswalk adapter requirements (requirements
only — no crosswalk built); (5) an intake runbook headed by
the structural rule that intake output can only ever reach
the harness's dry-run path — evaluation requires its own
future spec and owner authorization. The synthetic fixture
walks every stage: its deliberate duplicate cluster is caught
one per stage (7 in → 4 kept), and the license-missing
variant is rejected at the license gate. PRED-2026-001/002
remain PENDING; this phase evaluates nothing. Report:
`reports/phase130_intake_pack_results.json`; spec:
`specs/021-phase130-intake-pack/`.

## 6. Phase-131 (spec 022) — Source-of-disagreement attribution: almost none of it attributes

Attribution diagnostics ONLY, under the estimators frozen in
spec 022 before any Phase-131 statistic existed. Phase-131
does not re-score Phase-125 and issues no verdict.

**Arm A — matched-object alignment.** Every join stage
counted, as found: mayig objects / Holdat inscriptions
179 / 1,670. S1 CISI-ID join: 179 apparent zero-padded
namesakes, **0 validated** — REJECTED as non-identity (Holdat
`cisi_number` is internal sequential numbering, not a CISI
object ID); no S1 join was performed. S2 catalogue
cross-reference: 0 usable. S3 shared artifact keys: 0. S4
content matcher: 32 of 179 mayig inscriptions eligible
(primary-map token coverage 0.725823); **matched pairs: 4**
(NEAR 1, NEAR-REV 3; **exact matches: 0**); matched coverage
mayig 0.022346, Holdat 0.002395. Difference classes over the
matched set: substitution 2 pairs (2 blocks, 4 tokens),
insertion-deletion 2 pairs (2 blocks, 2 tokens). The small
matched set is a finding, reported as found: under the only
legitimate join, the two compilations' texts essentially do
not coincide. **Matched-object median TV: NOT ESTIMABLE**
(frozen gate requires ≥ 10 matched pairs and ≥ 4 of the 16
judgeable pairs with defined matched TVs; defined per-pair
TVs: 5 of 16; unthresholded median over defined pairs:
0.500000).

**Arm B — reading direction.** Criterion (frozen): an arm
supports direction iff its median TV ≤ 0.131316, the upper
bound of the Phase-127 matched-size noise band (median
0.082613, 95% interval [0.046665, 0.131316]). B1 (mayig
reversed) median TV **0.582205**; B2 (Holdat reversed) median
TV **0.582205** — the arms coincide exactly, as the algebra
requires (TV is symmetric under the INITIAL↔TERMINAL swap).
Reduction vs the observed 0.636931: 0.054726. **Reading
direction is NOT a supported mechanism**; credited share
**0.000**. (Arm B's unreversed control reproduced the
Phase-125 median TV of record, 0.636931, exactly through this
phase's own code path — a machinery check, not a re-score.)

**Arm C — stratification and composition.** Estimable strata
(≥ 4 judgeable pairs, floor 8 re-applied): Mohenjo-daro
median TV 0.599138 (13 judgeable); unicorn III 0.663366 (5);
unicorn IV 0.628981 (6); text-length bin 6+ 0.512903 (9).
All other site, object-type, and text-length strata are
**NOT ESTIMABLE** with their counts reported, and **period is
NOT ESTIMABLE in every cell** (neither side carries a period
field; none was improvised). Composition adjustment (Holdat
profiles reweighted to the mayig text-length composition;
16 of 16 pairs included): adjusted median TV **0.597874** vs
the unadjusted 0.636931 — composition share **0.061321**.

**Arm D — synthesis (the attribution table, verbatim):**

| Mechanism | Supported share | Status |
|---|---|---|
| segmentation | — | NOT ESTIMABLE |
| substitution | — | NOT ESTIMABLE |
| insertion_deletion | — | NOT ESTIMABLE |
| order_direction | 0.000000 | ESTIMABLE |
| composition | 0.061321 | ESTIMABLE |
| matched_object_residual | — | NOT ESTIMABLE (persistence measure, not an explained share) |

Sum of credited explained shares: 0.061321. **Residual
unexplained share: 0.938679** — stated plainly: this is the
share of the observed disagreement that no arm's registered
estimator accounts for. Shares are not forced to sum to 100%;
the order/direction and composition shares may overlap and
are never rescaled away. One implementation clarification
(ties for best similarity in the NEAR tier disqualify a
pairing) and one presentational note (the design-stage 0.717
coverage was a per-inscription mean; the run reports the
token-weighted 0.725823) are recorded in the report. Report:
`reports/phase131_attribution.md`; spec:
`specs/022-phase131-attribution/`.

## 7. Non-claims

Nothing in Phases 127–131 or specs 021–022 changes the status
of any decipherment anchor, validates or refutes any
individual sign reading, or scores any registered prediction.
The Phase-125 FAIL — DISAGREEMENT and spec 020's NO are
unchanged by anything in this note, and PRED-2026-001/002
remain PENDING. Phase-131's attribution is a statement about
the frozen inputs, the 16 judgeable primary pairs, and the
4-pair matched set as found — never about the script as a
whole or any individual pair's crosswalk correctness. The
matcher-eligible subset (32 of 179) is biased toward
inscriptions built from well-attested, unambiguously mapped
signs; Arm A findings describe that subset. Verification for
the sequence as merged at commit 257ed964: full backend suite
982 passed / 13 skipped / 0 failed (Phase-131 ledger record;
totals vary by worktree environment — an independent re-run
at the same commit in the v4.4.0 release worktree, CI
configuration, collected 975 tests: 970 passed / 5 skipped /
0 failed, and GitHub CI on the merge commit is green);
foundation check 40 passed / 0 failed / 8 warnings (baseline
unchanged, re-verified in the release worktree).

## References

- Pierson, T. (2026). *A Computational Decipherment Hypothesis
  for the Indus Script* (v4.3.0). Zenodo.
  DOI 10.5281/zenodo.23250395. Concept record:
  DOI 10.5281/zenodo.20379070.
- Glossa-Lab program provenance registry. OSF.
  https://osf.io/ybd65/
- Phase reports and frozen specs, BitConcepts/glossa-lab,
  main at commit
  257ed964dfcc8d4c7068e01308efd8532bdaa65b:
  `reports/phase127_cross_compilation_diagnostic.md`,
  `reports/phase128_evidence_dossiers_44.md`,
  `reports/phase129_cisi_cropper_v2.md`,
  `reports/phase130_intake_pack_results.json`,
  `reports/phase131_attribution.md`,
  `reports/release_integrity_audit_v420.md`,
  `specs/021-phase127-cross-compilation-diagnostic/`,
  `specs/021-phase130-intake-pack/`,
  `specs/022-phase131-attribution/`.

## AI disclosure

These studies were designed for execution by, and were
executed by, an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per the repository constitution
§VI. The spec freezes (git commit order as pre-registration
proof), the frozen verdict rules, and the anchors-file hash
assertions were the controls substituting for a human
firewall: the executing agents had no discretion to soften a
verdict, and the negative outcomes above — above all
Phase-131's 0.938679 unexplained residual and its near-empty
matched join — are reported as recorded rather than narrated
toward a conclusion. This note was likewise drafted by an AI
agent under the same direction; every number in it is taken
from the merged reports and specs cited above.

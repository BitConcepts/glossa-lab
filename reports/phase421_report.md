# Phase-421 — Spec 059 execution report

Claim: `STUDY-SPEC-024/F1` — standing SETTLED — SUPPORTED on its original joined subset (odds ratio 2.384, interval [1.847, 3.077], family q = 0.00015), exactly as recorded. Execution date: 2026-10-21. Freeze digest: `bba1caca1885c2146515b437963619dff6737b4fc321a683f0dce9a56b5aed58`. OSF registration yfw7h (approved and public; DOI 10.17605/OSF.IO/YFW7H). Lineage: ICIT-lineage (horus84) — results describe this lineage layer, and its object-ID-joined subset, not the Indus corpus in general.

## Outcome: CLOSED AT STEP 0 - JOIN GATE NOT MET

> CLOSED AT STEP 0 — JOIN GATE NOT MET. The object-identifier join joined 2899 of 5,679 lineage rows (51.05%), against the original concordance join's 51.0% and the gate fixed in advance at 61.0% or more. The enlarged joined set this design required does not exist on the available catalogue data, so no F1 quantity was computed and STUDY-SPEC-024/F1 stands exactly as recorded — SUPPORTED on its original joined subset, its 'on the joined subset' scope unchanged. The unjoined share is a measured property of the available catalogue data, not an oversight. The unblocking act is a more complete published object catalogue entering through Phase-130 intake.

## Step 0, gate by gate

- **Gate 0.1 — Input integrity: PASS** — every spec section 2 pin and every DD-059-9 object-identifier source pin recomputes to its freeze-record value (hashes and byte counts in the machine record).
- **Gate 0.2 — Original-join reproduction: PASS** — observed 5679 layer rows / 2895 matched / 2 ambiguous / 2782 unmatched, against the recorded 5,679 / 2,895 / 2 / 2,782.
- **Gate 0.3 — Object-ID join census: PASS** — the join dataset built by the pinned route-(b) construction carries 5018 records; Phase-130 validation verdict: pass (0 errors, 0 warnings).

## The gate census (the closure's finding)

- Layer rows: 5679
- Joined rows: 2899 (51.0477%)
- Unjoined rows: 2780 (661 carrying no identifier; 2119 whose identifier resolves to zero catalogue objects)
- Ambiguous rows (more than one distinct object): 0
- Distinct catalogue objects joined to: 2479
- Catalogue layer: 7705 rows, 3493 distinct objects across vols 1–2
- Joined object-type mix: (unfilled) 143, Graffiti 69, Objects 7, Seals 1590, Tablets 1090
- Rows the object-ID join adds over the original join: 4 (original joined rows lost: 0)

The full per-row census — identifier provenance and resolution class for every one of the 5,679 layer rows — is `reports/phase421_join_census.json`.

- **Gate 0.4 — Gate comparison: FAIL** — joined 2899 rows (51.0477%) against the bar fixed in advance at DD-059-7: >= 3465 rows (61.0%); shortfall 566 rows.

## What was not done

No F1 quantity was computed on the new join: no terminal mapping, no test statistic, no p-value, no odds ratio. The Phase-136 test machinery was not run. Spec 024's frozen records and SUPPORTED verdict stand unedited; this outcome appends beside them as a dated replication record that records a gate closure, not a verdict.

Anchors asserted byte-identical before and after: `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` at both readings (asserted: True).

*AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution section VI.*

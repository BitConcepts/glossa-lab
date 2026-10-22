# Phase-429 — Spec 067 execution report

Claim: `STUDY-SPEC-024/F1` — standing SETTLED — SUPPORTED on its original joined subset (odds ratio 2.384, interval [1.847, 3.077], family q = 0.00015), exactly as recorded. Execution date: 2026-10-22. Freeze digest: `73463ab949f65ecf620a9f4544b9a84fe18f72056a86c48ce9d5d0164f3d41db`. OSF registration qsthg (approved and public before this run; verified by API read-back 2026-10-22). Lineage: ICIT-lineage (horus84) — results describe this lineage layer, and its object-ID-joined subset, not the Indus corpus in general.

## Outcome: REPLICATED

> On the enlarged object-ID-joined set (4676 of 5,679 lineage rows, 82.34%, against the original join's 51.0%), the seal/tablet difference in TERMINAL14 endings replicates within sites: Mantel–Haenszel odds ratio 2.452, 95% CI [1.965–3.058], entirely above 1.5, family-adjusted q = 0.0001. The original F1 result was not an artefact of which rows the concordance join could reach, at this test's resolution. Leave-one-site-out: every dropped-site subset remained estimable with its interval excluding 1; no site is load-bearing. This is a statement about recorded use in this lineage layer, not about what the difference means.

## Step 0, gate by gate

- **Gate 0.1 — Input integrity: PASS** — every spec section 2 pin and every DD-067-9 source pin recomputes to its freeze-record value, and the merged catalogue layer v2 was asserted on the local file first (SHA-256, 2,655,958 bytes, 9,741 rows, 5,529 distinct objects; hashes and byte counts in the machine record).
- **Gate 0.2 — Original-join reproduction: PASS** — observed 5679 layer rows / 2895 matched / 2 ambiguous / 2782 unmatched, against the recorded 5,679 / 2,895 / 2 / 2,782.
- **Gate 0.3 — Object-ID join census: PASS** — the join dataset built by the pinned route-(b) construction carries 5018 records; Phase-130 validation verdict: pass (0 errors, 0 warnings).

## The gate census

- Layer rows: 5679
- Joined rows: 4676 (82.3384%)
- Unjoined rows: 1003 (661 carrying no identifier; 342 whose identifier resolves to zero catalogue objects)
- Ambiguous rows (more than one distinct object): 0
- Distinct catalogue objects joined to: 3763
- Catalogue layer: merged catalogue layer v2, 9741 rows, 5529 distinct objects
- Joined object-type mix: (unfilled) 317, Graffiti 214, Objects 53, Seal impressions 15, Seals 1969, Tablets 2108
- Rows the object-ID join against layer v2 adds over the original concordance join: 1781 (original joined rows lost: 0)

The full per-row census — identifier provenance and resolution class for every one of the 5,679 layer rows — is the restricted-local product `phase429_join_census.json` (5,679 rows), held beside the merged layer in the restricted local store under spec section 7.3 and named here by filename and count only; it is not committed.

## The type-fill census (gate 0.4)

- **Gate 0.4 — Type-fill census: PASS** — taken before any F1 quantity existed.
- Newly joined objects (rows the Phase-421 census recorded as unjoined, identifier resolving to zero in vols. 1–2): 1777 rows / 1284 distinct objects — type filled 1152 objects (1603 rows), type unfilled 132 objects (174 rows).
- Whole joined set: 4676 rows / 3763 distinct objects — type filled 3511 objects (4359 rows), type unfilled 252 objects (317 rows).
- Whole joined set type mix (rows): (unfilled) 317, Graffiti 214, Objects 53, Seal impressions 15, Seals 1969, Tablets 2108
- Restricted to {Seals, Tablets}: 4077 rows.
- Eligible seal/tablet strata (census form, before terminal mapping): Harappa, Kalibangan, Mohenjo-daro. Per-site census strata are in the machine record.

- **Gate 0.5 — Gate comparison: PASS** — joined 4676 rows (82.3384%) against the bar fixed in advance at DD-067-7: >= 3465 rows (61.0%); shortfall 0 rows.

## Primary test (frozen Phase-136 flow)

- Flow: joined 4676 → typed 4359 (untyped 317) → restricted to seals/tablets 4077 → terminal mapped 3315 (UNK 762, no codes 0) → analysis population in eligible strata 3181.
- Eligible strata: Harappa, Mohenjo-daro, Kalibangan.
- Estimability: True (3 eligible strata; pooled expected counts >= 5 in 1.0 of cells).
- CMH chi-square: 67.3997731118022; permutation raw p = 0.0001 (B = 9999, seed 20261009); family-adjusted q = 0.0001 (single-test family, DD-067-8).
- Mantel–Haenszel common odds ratio: 2.4516021796728986, 95% CI [1.9651859192920271–3.058414569519296]; crude odds ratio (uncontrolled): 2.9619116261019016.

## Leave-one-site-out (descriptive)

Leave-one-site-out: every dropped-site subset remained estimable with its interval excluding 1; no site is load-bearing.

| Dropped site | Estimable | MH odds ratio | 95% CI |
|---|---|---|---|
| Harappa | True | 2.2135504784908147 | [1.6108787692208304, 3.0416973731654013] |
| Mohenjo-daro | True | 2.722780764747904 | [2.0262345854162107, 3.6587743325674014] |
| Kalibangan | True | 2.465384882192559 | [1.9743409297709686, 3.0785577737319683] |

## Covariate comparisons

Joined versus unjoined rows, the original joined set versus the rows the layer-v2 join adds, and the Phase-421 joined set versus the newly joined rows — on site, object type (for rows the catalogue types), text length, and preservation as recorded — are in the machine record (`reports/phase429_results.json`). Object type for unjoined rows is not carried: unjoined rows have no catalogue object.

Anchors asserted byte-identical before and after: `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` at both readings (asserted: True).

*AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution section VI.*

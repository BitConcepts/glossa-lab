# Reconciliation — P2 spec governance bundles (Spec 086 Stage 1, T104)

Migration run: `migration-2026-11-01-stage1`, 2026-11-01. Source stores:
`specs/*/claims.json` (52 files) and
`specs/*/aee-claims.json` (58 files), read-only.

## Census — re-derived on this checkout, and the delta

This checkout carries **1624 source records** in
862 distinct (spec, claim) pairs, including
Spec 086's own bundle
(`specs/086-winning-combination-adoption/aee-claims.json`,
21 claims, adopted at Stage 0 of this stage and migrated
with the rest — the ledger holds no silent exceptions).
The pre-existing population is 1603 records.
The Spec 086 package's audit counted 1,592 records from a
Spec 083 worktree; the delta against the pre-existing
population (+11) is exactly
`specs/084-policy-sync-conformance/aee-claims.json`
(11 claims, no `claims.json`), which landed on main with
Spec 084 (PR #474) after the audit's worktree base. This
reconciliation is authoritative.

## The double-format question — answered

The two formats are two serializations of one population:
762 of the 862 (spec, claim) pairs
are present in both serializations, and every such pair was
verified during the build census to carry identical text
and status in each. Under D-B the
ledger holds one canonical entry per **proposition
fingerprint**, so restatements of one proposition by successor
specs also merge: 44 fingerprint groups span more
than one (spec, claim), merging 45 (spec, claim)
pairs into another pair's canonical entry (each preserved as
an evidence instance in the entry's `sources` and listed
below). No source record is unaccounted for:
1624 records in = 817 canonical entries
carrying all 1624 source records in their
`sources` lists.

## Headline counts

| Measure | Count |
|---|---|
| Source records in | 1624 |
| Distinct (spec, claim) pairs | 862 |
| Canonical ledger entries out | 817 |
| (Spec, claim) pairs merged into another entry (D-B) | 45 |
| Fingerprint groups spanning >1 (spec, claim) | 44 |
| Groups whose member records carry differing falsification tests | 26 |
| Groups whose member records carry differing boundary lines | 40 |

## Fingerprint groups spanning >1 (spec, claim)

- `a3bd97ded698…` canonical `032-pred-2026-006-harappa-breakdown/F032-C09`; proposition also recorded as: `043-pred-2026-007-registry-frame/F043-C13`
- `e54659fd842a…` canonical `032-pred-2026-006-harappa-breakdown/F032-C10`; proposition also recorded as: `035-pred-2026-010-scoring/F035-C13`
- `d36389fb3831…` canonical `035-pred-2026-010-scoring/F035-C02`; proposition also recorded as: `036-pred-2026-011-scoring/F036-C02`
- `2ae7df250cef…` canonical `035-pred-2026-010-scoring/F035-C04`; proposition also recorded as: `036-pred-2026-011-scoring/F036-C04`
- `9914f7958d92…` canonical `035-pred-2026-010-scoring/F035-C10`; proposition also recorded as: `036-pred-2026-011-scoring/F036-C10`
- `f8598e295e65…` canonical `036-pred-2026-011-scoring/F036-C12`; proposition also recorded as: `038-pred-2026-007-full-population/F038-C09`
- `d96e1b45a4a4…` canonical `046-horned-tiger-concordance/F046-C02`; proposition also recorded as: `064-sign297-concordance-successor/F064-C02`
- `de15430906d0…` canonical `046-horned-tiger-concordance/F046-C04`; proposition also recorded as: `064-sign297-concordance-successor/F064-C04`
- `db793a8b5d46…` canonical `046-horned-tiger-concordance/F046-C05`; proposition also recorded as: `064-sign297-concordance-successor/F064-C05`
- `4fcc250d4913…` canonical `046-horned-tiger-concordance/F046-C09`; proposition also recorded as: `064-sign297-concordance-successor/F064-C09`
- `26e177a91f3b…` canonical `046-horned-tiger-concordance/F046-C10`; proposition also recorded as: `064-sign297-concordance-successor/F064-C10`
- `88801087571a…` canonical `046-horned-tiger-concordance/F046-C11`; proposition also recorded as: `064-sign297-concordance-successor/F064-C11`
- `bfa591b3060d…` canonical `046-horned-tiger-concordance/F046-C13`; proposition also recorded as: `064-sign297-concordance-successor/F064-C13`
- `ff1e65980535…` canonical `048-parpola-fish-family-profiles/F048-C10`; proposition also recorded as: `053-yadav-zipf-controls/F053-C13`
- `df91cecad09e…` canonical `053-yadav-zipf-controls/F053-C02`; proposition also recorded as: `068-yadav-zipf-controls-successor/F068-C03`
- `8a904c2af51c…` canonical `056-sign821-recovery/F056-C11`; proposition also recorded as: `063-sign821-identification-successor/F063-C11`
- `0635d09dfadf…` canonical `057-five-sources-heading/F057-C07`; proposition also recorded as: `065-s1-s5-heading-successor/F065-C07`
- `aebc2762cb49…` canonical `057-five-sources-heading/F057-C09`; proposition also recorded as: `065-s1-s5-heading-successor/F065-C09`
- `454f66f975f8…` canonical `057-five-sources-heading/F057-C11`; proposition also recorded as: `065-s1-s5-heading-successor/F065-C11`
- `35e779648778…` canonical `059-f1-object-join/F059-C02`; proposition also recorded as: `067-f1-enlarged-join/F067-C02`
- `d684db3620b1…` canonical `059-f1-object-join/F059-C03`; proposition also recorded as: `067-f1-enlarged-join/F067-C03`
- `db553b5ad7a5…` canonical `059-f1-object-join/F059-C04`; proposition also recorded as: `067-f1-enlarged-join/F067-C04`
- `958c12a10e0e…` canonical `059-f1-object-join/F059-C05`; proposition also recorded as: `067-f1-enlarged-join/F067-C05`
- `591eb28ed0cd…` canonical `059-f1-object-join/F059-C07`; proposition also recorded as: `067-f1-enlarged-join/F067-C07`
- `e60c3eaa015d…` canonical `059-f1-object-join/F059-C08`; proposition also recorded as: `067-f1-enlarged-join/F067-C08`
- `beddce314c70…` canonical `059-f1-object-join/F059-C09`; proposition also recorded as: `067-f1-enlarged-join/F067-C09`
- `296e03efee27…` canonical `059-f1-object-join/F059-C10`; proposition also recorded as: `067-f1-enlarged-join/F067-C10`
- `773f5ed2790f…` canonical `059-f1-object-join/F059-C11`; proposition also recorded as: `067-f1-enlarged-join/F067-C11`
- `cfa2cce9a3db…` canonical `059-f1-object-join/F059-C12`; proposition also recorded as: `067-f1-enlarged-join/F067-C12`
- `01464dd5362b…` canonical `059-f1-object-join/F059-C14`; proposition also recorded as: `067-f1-enlarged-join/F067-C14`
- `fe5c4fd1c8f7…` canonical `061-arm-a-precision/F061-C07`; proposition also recorded as: `062-arm-a-precision-calibration-repair/F062-C07`
- `eb4be341cfae…` canonical `061-arm-a-precision/F061-C08`; proposition also recorded as: `062-arm-a-precision-calibration-repair/F062-C08`
- `374f0d66ad1d…` canonical `061-arm-a-precision/F061-C09`; proposition also recorded as: `062-arm-a-precision-calibration-repair/F062-C09`
- `c1be607d7608…` canonical `061-arm-a-precision/F061-C10`; proposition also recorded as: `062-arm-a-precision-calibration-repair/F062-C10`
- `0ff22b4e75b7…` canonical `061-arm-a-precision/F061-C11`; proposition also recorded as: `062-arm-a-precision-calibration-repair/F062-C11`
- `d7a62f199b37…` canonical `061-arm-a-precision/F061-C12`; proposition also recorded as: `062-arm-a-precision-calibration-repair/F062-C12`
- `c92bdb6f1905…` canonical `070-hunt-opening-signs-successor/F070-C02`; proposition also recorded as: `074-hunt-opening-signs-repaired-surface/F074-C02`
- `bf5959739ce6…` canonical `070-hunt-opening-signs-successor/F070-C03`; proposition also recorded as: `074-hunt-opening-signs-repaired-surface/F074-C03`
- `53cbceddd1b0…` canonical `070-hunt-opening-signs-successor/F070-C04`; proposition also recorded as: `071-hunt-sky-signs-successor/F071-C04`, `074-hunt-opening-signs-repaired-surface/F074-C04`
- `905bd6e4a25b…` canonical `070-hunt-opening-signs-successor/F070-C06`; proposition also recorded as: `074-hunt-opening-signs-repaired-surface/F074-C06`
- `5d485dc2aa8d…` canonical `070-hunt-opening-signs-successor/F070-C11`; proposition also recorded as: `074-hunt-opening-signs-repaired-surface/F074-C11`
- `f00a71aa284b…` canonical `076-projected-constraint-corpus-model/F076-C04`; proposition also recorded as: `078-projected-constraint-bridge-redesign/F078-C04`
- `6b122d3cb672…` canonical `076-projected-constraint-corpus-model/F076-C05`; proposition also recorded as: `078-projected-constraint-bridge-redesign/F078-C05`
- `1fd2117a3172…` canonical `076-projected-constraint-corpus-model/F076-C07`; proposition also recorded as: `078-projected-constraint-bridge-redesign/F078-C07`

## Rules applied inside groups

- `statement`, `status`, `does_not_establish`: the
  representative record's (first (spec, claim) in sorted
  order; its `claims.json` serialization where both exist).
  Statuses were verified uniform inside every group during
  the build census (all `draft` but one singleton
  `superseded`, Spec 083's C083-13, which is alone in its
  group), so no status is masked by a merge.
- `falsifier`: the ordered union of the group's
  falsification tests — successor specs often restate a
  proposition with their own tests (26
  groups differ), and the union keeps every test traceable
  to a named source record (C086-5) instead of dropping the
  variants. Boundary variants (40 groups)
  remain in their source bundles; the entry carries the
  representative's line, per D-B (stage and score attach to
  the proposition, not to an instance).
- `stage`: from the representative pair's `aee-claims.json`
  where it carries one (802 of 817
  entries; the rest are null — pairs with no aee
  serialization).

## Coverage (canonical entries)

- Falsifier: 817 of 817 entries.
- Does-not-establish (`boundary`): 732 of 817
  entries.
- AEE state: 0 of 817 entries — the bundles carry
  adjudication status, not scores; `aee_state` is null, shown
  as null.
- Confidence (harmonization adoption #3 item 6, binding): a
  full census of both serializations found NO confidence
  field of any name at any depth in these 1624
  records — `confidence_in_source` and `confidence_text` are
  null on every bundle entry, recorded here so the absence is
  a checked fact, not an oversight. (The qualitative
  confidences the adoption names — e.g. anchor pairs'
  `confidence: "low"` — live outside this population; the
  anchor store is not in this repo tree and anchors are not a
  Stage 1 migration population. Recorded Stage 4 intake
  constraint: such values may enter the ledger only verbatim
  through `confidence_text`, never as numbers.)

## Mirror check

Every canonical entry's `status` was compared byte-equal
against its representative source record, and its `stage`
against the representative pair's aee record, after the
build; the migration test re-runs this comparison in CI.
Differences: none (any difference would be listed here and
would stop the stage).

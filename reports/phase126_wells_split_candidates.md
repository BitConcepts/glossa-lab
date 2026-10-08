# Phase-126 — Wells-Split Descriptive Analysis of the 113 CANDIDATE Anchors (Design-Input Memo)

**Status:** descriptive design input. **Date:** 2026-10-08. **Phase:** 126
(owner-ordered Glossa-Lab program, 2026-10-08, step 3).

**Framing (hard).** This memo records facts only: how the Phase-123
Wells segmentation witness treats each of the 113 CANDIDATE anchors,
and how that treatment distributes across the evidence features the
anchors file itself records for those signs. It is addressed to
future battery design. It phrases **no** adjudication of any sign's
status, proposes **no** promotion or demotion, and changes **no**
anchor: the anchors file is byte-identical before and after
(sha256 eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed, asserted in code).

## 1. Inputs

- **Anchors:** `backend/reports/INDUS_FINAL_ANCHORS.json`. The
  analysis set is exactly the anchors whose `confidence` field is
  `CANDIDATE` — **113 signs**. The 44 anchors carrying
  `validation_status` = `pending_non_sa_validation` are a disjoint
  set and are not analysed here.
- **Wells witness:** `data/crosswalks/wells_segmentation_witness_v1.json`
  (Phase-123; 157 rows) with the classification semantics of
  `reports/phase123_wells_segmentation_witness.md` — SAME / SPLIT /
  MERGE / NOT-COVERED / INDETERMINATE. In this memo's vocabulary:
  SPLIT → **split**, MERGE → **merge**, SAME → **unit-same**,
  NOT-COVERED → **not-covered**, INDETERMINATE → **indeterminate**.
  "Split" means Wells segments what the program's signary treats as
  one sign into multiple graphemes (a compound-suspect under Wells);
  the split components are the witness table's `wells_graphemes`.

## 2. Headline counts (of the 113 CANDIDATEs)

| Wells treatment | Count |
|---|---|
| split | 27 |
| merge | 4 |
| unit-same | 62 |
| not-covered | 1 |
| indeterminate | 19 |
| **total** | **113** |

Wells treatment is determinable for
**93 of 113** signs
(split + merge + unit-same). The witness is silent, in the senses
recorded in §6, for the remaining
**20**.

## 3. Compound-suspects under Wells (split, 27)

These are the CANDIDATE signs that Wells's segmentation divides
into multiple graphemes. Split-size distribution (signs into
graphemes): 20 into 2, 6 into 3, 1 into 5.

| Sign | Wells graphemes (split components) | n components | `basis` freq |
|---|---|---|---|
| M104 | 004; 014 | 2 | 3 |
| M105 | 004; 014 | 2 | 3 |
| M106 | 005; 015 | 2 | 4 |
| M109 | 006; 016 | 2 | 4 |
| M111 | 048; 049 | 2 | 3 |
| M112 | 007; 017 | 2 | 2 |
| M120 | 025; 026; 027; 028; 029 | 5 | 4 |
| M146 | 683; 684 | 2 | 3 |
| M147 | 683; 684 | 2 | 2 |
| M181 | 307; 308; 309 | 3 | 3 |
| M200 | 570; 571 | 2 | 2 |
| M219 | 560; 561 | 2 | 3 |
| M242 | 621; 622 | 2 | 2 |
| M258 | 604; 605 | 2 | 2 |
| M277 | 869; 871 | 2 | 3 |
| M280 | 869; 871 | 2 | 4 |
| M309 | 531; 533 | 2 | 4 |
| M341 | 716; 717 | 2 | 3 |
| M363 | 777; 778; 782 | 3 | 2 |
| M364 | 777; 778; 782 | 3 | 1 |
| M379 | 831; 833 | 2 | 3 |
| M381 | 812; 813; 814 | 3 | 3 |
| M387 | 803; 805; 806 | 3 | 4 |
| M388 | 804; 807 | 2 | 3 |
| M390 | 804; 807 | 2 | 4 |
| M397 | 370; 371; 372 | 3 | 2 |
| M415 | 215; 216 | 2 | 2 |

Shared components (descriptive): W004 in the split sets of M104, M105; W014 in the split sets of M104, M105; W683 in the split sets of M146, M147; W684 in the split sets of M146, M147; W777 in the split sets of M363, M364; W778 in the split sets of M363, M364; W782 in the split sets of M363, M364; W804 in the split sets of M388, M390; W807 in the split sets of M388, M390; W869 in the split sets of M277, M280; W871 in the split sets of M277, M280. In the witness's
own terms, the split sets of these signs are therefore not
disjoint partitions of the CANDIDATE set.

## 4. Unit-confirmed under Wells (unit-same, 62)

For these signs the witness records exactly one Wells grapheme,
unshared — Wells treats the sign as one unit, as the program's
signary does:

M101, M123, M129, M131, M133, M134, M135, M136, M138, M140, M156, M157, M158, M170, M186, M195, M197, M201, M203, M208, M209, M210, M213, M214, M224, M226, M227, M230, M243, M247, M250, M251, M255, M256, M259, M274, M278, M286, M287, M297, M298, M301, M303, M307, M310, M318, M320, M322, M323, M327, M334, M339, M346, M369, M378, M380, M396, M400, M405, M407, M408, M413

## 5. Merge (4)

For these signs the sign's one Wells grapheme is shared with
other Mahadevan signs in the witness table:

- M115 → Wells grapheme 019 (method REGISTRY)
- M116 → Wells grapheme 019 (method REGISTRY)
- M245 → Wells grapheme 615 (method REGISTRY)
- M389 → Wells grapheme 805 (method GLYPH)

## 6. Where the witness is silent (20)

**Not-covered (1).** Signs the witness classed
NOT-COVERED (glyph searched for in the Phase-123 plates and not
found, per the witness note):

- M312 — witness note: A plain wide arch (single broad curve) appears nowhere in the PhD Fig. 3.2 plates (thesis pp. 90-92), whose arc signs are all narrow parenthesis/C forms (signs 900-921).

CANDIDATE signs absent from the witness table altogether:
**0**.
Any such sign would be counted and listed here as not-covered by
construction of the builder; none occurs in the current inputs.

**Indeterminate (19).** Signs for which the
witness records no determinable treatment, with the witness's
reason per sign:

- M126 — witness note: Chain-only lead: the program's ICIT conversion layer aligns this sign with Wells/ICIT codes 016 (49 tokens) and 006 (7 tokens), both kind 'chain' via the unmerged Phase-122 crosswalk chain (PR #81). Recorded indeterminate for the same reason as M033; if the chain correspondence were confirmed, the two-code alignment would indicate a SPLIT treatment - stated here as a conditional lead only, not a finding.
- M207 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M217 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M218 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M240 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M260 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M314 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M316 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M324 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M340 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M354 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M356 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M359 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M360 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M370 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M382 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M392 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M394 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.
- M406 — witness note: No correspondence in the held canonical registry, no entry in the MA thesis Fig. 3.6 concordance, and the glyph could not be located with confidence in the PhD Fig. 3.2 plates; treatment not determinable from the theses as held. No inference made.

## 7. Cross-tabulations (counts only)

Treatment is cross-tabulated against the evidence features
actually present in the anchors file for these 113 signs, named
by their exact field names. Three features are constant across
the set and are stated as facts rather than tabulated:
`basis` records the positional profile I=0.000 / T=0.000 /
M=1.000 (medial-only) for **all 113** signs, and `source` is
`Phase-111` for **all 113**; `validation_status` is
`premise_superseded` for **all 113** (the tables below carry
these fields in full regardless).

### 7.1 By attestation count parsed from `basis` (`freq=`)

| Key | split | merge | unit-same | not-covered | indeterminate | total |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 11 | 0 | 4 | 17 |
| 2 | 8 | 1 | 14 | 0 | 3 | 26 |
| 3 | 11 | 0 | 17 | 0 | 6 | 34 |
| 4 | 7 | 2 | 20 | 1 | 6 | 36 |

### 7.2 By `validation_status` field

| Key | split | merge | unit-same | not-covered | indeterminate | total |
|---|---|---|---|---|---|---|
| premise_superseded | 27 | 4 | 62 | 1 | 19 | 113 |

### 7.3 By `_phase132_note` presence in the anchor entry

| Key | split | merge | unit-same | not-covered | indeterminate | total |
|---|---|---|---|---|---|---|
| False | 9 | 2 | 25 | 0 | 7 | 43 |
| True | 18 | 2 | 37 | 1 | 12 | 70 |

### 7.4 By `phase109_annotation` presence in the anchor entry

| Key | split | merge | unit-same | not-covered | indeterminate | total |
|---|---|---|---|---|---|---|
| False | 0 | 0 | 4 | 0 | 0 | 4 |
| True | 27 | 4 | 58 | 1 | 19 | 109 |

### 7.5 By Phase-252 cohort fields (`phase_upgraded` present)

The four signs carrying `phase_upgraded` are the same four
carrying `dedr` / `dedr_source` / `upgrade_basis`
(the Phase-252 allograph cohort recorded in the anchors file):

| Key | split | merge | unit-same | not-covered | indeterminate | total |
|---|---|---|---|---|---|---|
| False | 27 | 4 | 58 | 1 | 19 | 109 |
| True | 0 | 0 | 4 | 0 | 0 | 4 |

### 7.6 By witness `correspondence_method` (witness-table field)

| Key | split | merge | unit-same | not-covered | indeterminate | total |
|---|---|---|---|---|---|---|
| GLYPH | 0 | 1 | 5 | 0 | 0 | 6 |
| GLYPH-SEARCH-NEGATIVE | 0 | 0 | 0 | 1 | 0 | 1 |
| NONE | 0 | 0 | 0 | 0 | 19 | 19 |
| REGISTRY | 27 | 3 | 57 | 0 | 0 | 87 |

### 7.7 By witness `verification` (Phase-123 hand-verification)

| Key | split | merge | unit-same | not-covered | indeterminate | total |
|---|---|---|---|---|---|---|
| None | 27 | 3 | 55 | 1 | 19 | 105 |
| verified | 0 | 0 | 7 | 0 | 0 | 7 |
| verified_with_conflict | 0 | 1 | 0 | 0 | 0 | 1 |

## 8. Design-input facts (for a future battery spec)

Stated as facts about the recorded material; what a future
spec does with them is that spec's decision, not this memo's.

1. Of the 113 CANDIDATEs, **27** are compound-suspects
   under Wells: a battery whose unit of analysis is the pooled
   sign would, for these signs, be pooling tokens that Wells's
   segmentation assigns to two or more graphemes (§3).
2. **62** CANDIDATEs are unit-confirmed under
   Wells: the witness records one unshared grapheme for each
   (§4).
3. **4** CANDIDATEs share their single Wells grapheme
   with other Mahadevan signs (§5); in the witness's terms their
   token sets are not separable from those signs' token sets by
   Wells grapheme identity alone.
4. For **20** CANDIDATEs
   the Wells witness states no determinable treatment (§6); a
   future design that needs a Wells-treatment value for every
   CANDIDATE has no recorded value for these signs in the
   Phase-123 table.
5. The split components overlap across CANDIDATEs (§3): the
   recorded Wells graphemes are shared between the split sets
   of 10
   distinct CANDIDATE signs.
6. Every CANDIDATE's `basis` records the same positional
   profile (I=0.000 / T=0.000 / M=1.000) and one of four
   attestation counts (freq 1–4); the cross-tab in §7.1 is the
   full joint distribution of Wells treatment against that
   recorded attestation count.
7. The witness's determinate treatments for CANDIDATEs rest on
   the `correspondence_method` distribution in §7.6 (registry
   cross-match vs hand glyph match vs glyph-search-negative),
   and the Phase-123 hand-verification in §7.7 covers
   8 of the 113.

## 9. What this memo does not do

It does not adjudicate any sign's status; it does not propose
adopting, rejecting, or hybridising Wells's segmentation; it
does not rank Wells's segmentation against any other; and it
draws no conclusion about any anchor's reading. "Compound-
suspect" and "unit-confirmed" above are descriptions of the
witness's treatment of a sign, nothing more.

## 10. Reproducibility

```
~/workspace/venvs/glossa-lab/bin/python backend/scripts/phase126_wells_split_candidates.py
~/workspace/venvs/glossa-lab/bin/python -m pytest backend/tests/test_phase126_wells_split_candidates.py
```

The builder reads only the two committed inputs named in §1,
asserts the anchors sha256 before and after, and is
deterministic (two runs byte-identical).

---

**AI disclosure:** executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per constitution
section VI.
